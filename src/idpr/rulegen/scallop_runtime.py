"""Validated fact ingestion and native Scallop CLI execution."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence


ASSESSMENT_STATUSES = {"satisfied", "not_satisfied", "unknown"}
SCENARIO_ID = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
ACTOR_FIELDS = (
    "case_id",
    "defendant_id",
    "deceived_person_id",
    "disposer_id",
    "property_owner_id",
    "beneficiary_id",
)
# 역할 tuple을 제외한, 모든 unit이 공유하는 system input 술어.
FIXED_SYSTEM_INPUTS = frozenset(
    {"provable", "case_assessment_complete", "distinct_entity"}
)


class ScallopFactValidationError(ValueError):
    """Raised before untrusted or incomplete facts can reach Scallop."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("Invalid Scallop facts:\n- " + "\n- ".join(self.errors))


class ScallopRuntimeError(RuntimeError):
    """Raised when the pinned native runtime cannot evaluate a scenario."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _role_contract(rule_ir: Mapping[str, Any]) -> tuple[str, tuple[str, ...]]:
    """역할 술어와 행위자 필드를 RuleIR에서 읽는다 (죄명마다 다르다).

    사기는 `fraud_case_roles`와 6개 슬롯이었다. 재산죄 단위는 `<issue_tag>_case_roles`와
    단위별 슬롯을 쓴다. RuleIR이 그 계약을 이미 담고 있으므로 여기서 되짚고, 없으면 사기
    기본값으로 떨어진다(기존 호출 동작 불변).

    P2 unit은 서명을 데이터로 선언하므로 술어 이름이 `issue_tag`에서 유도되지 않는다
    (`arson_of_occupied_structure` → `arson_case_roles`). 이름으로 못 찾으면 고정 3개를
    제외한 system input 술어에서 서명을 읽는다. 이름을 추측해 6슬롯 사기 tuple로 조용히
    떨어지면 다른 arity의 사실을 만들어내므로 그 경로를 먼저 막는다.
    """

    predicate_id = f"{rule_ir.get('issue_tag', 'fraud')}_case_roles"
    declared: list[Mapping[str, Any]] = []
    for predicate in rule_ir.get("predicates", []):
        if predicate.get("id") == predicate_id:
            return predicate_id, tuple(
                argument["name"] for argument in predicate.get("arguments", [])
            )
        if (
            predicate.get("origin") == "system"
            and predicate.get("role") == "input"
            and predicate.get("id") not in FIXED_SYSTEM_INPUTS
        ):
            declared.append(predicate)
    if len(declared) == 1:
        return str(declared[0]["id"]), tuple(
            argument["name"] for argument in declared[0].get("arguments", [])
        )
    return "fraud_case_roles", ACTOR_FIELDS


def validate_scenario(
    rule_ir: Mapping[str, Any], scenario: Mapping[str, Any]
) -> None:
    errors: list[str] = []
    scenario_id = scenario.get("scenario_id")
    if not isinstance(scenario_id, str) or not SCENARIO_ID.fullmatch(scenario_id):
        errors.append("scenario_id must be a safe lowercase identifier")
    _, actor_fields = _role_contract(rule_ir)
    actor_values: list[str] = []
    for field in actor_fields:
        value = scenario.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{field} must be a non-empty string")
        else:
            actor_values.append(value)

    card_inputs = _card_input_predicates(rule_ir)
    selected = scenario.get("selected_card_ids", [])
    if not isinstance(selected, list) or any(
        not isinstance(card_id, str) or not card_id for card_id in selected
    ):
        errors.append("selected_card_ids must be a list of non-empty strings")
        selected = []
    selected_set = set(selected)
    if len(selected_set) != len(selected):
        errors.append("selected_card_ids must not contain duplicates")
    unknown_selected = sorted(selected_set - set(card_inputs))
    if unknown_selected:
        errors.append(f"selected_card_ids contains unknown cards: {unknown_selected}")

    assessments = scenario.get("assessments", [])
    if not isinstance(assessments, list):
        errors.append("assessments must be a list")
        assessments = []
    assessment_ids: set[str] = set()
    provable_cards: set[str] = set()
    for index, assessment in enumerate(assessments):
        label = f"assessments[{index}]"
        if not isinstance(assessment, Mapping):
            errors.append(f"{label} must be an object")
            continue
        assessment_id = assessment.get("assessment_id")
        if not isinstance(assessment_id, str) or not assessment_id:
            errors.append(f"{label}.assessment_id must be a non-empty string")
        elif assessment_id in assessment_ids:
            errors.append(f"duplicate assessment_id {assessment_id}")
        else:
            assessment_ids.add(assessment_id)
        card_id = assessment.get("card_id")
        if card_id not in selected_set:
            errors.append(f"{label}.card_id must be selected by the router")
        if card_id not in card_inputs:
            errors.append(f"{label}.card_id is not an approved commentary input")
        status = assessment.get("status")
        if status not in ASSESSMENT_STATUSES:
            errors.append(f"{label}.status must be satisfied/not_satisfied/unknown")
        provable = assessment.get("provable")
        if not isinstance(provable, bool):
            errors.append(f"{label}.provable must be boolean")
        elif provable and isinstance(card_id, str):
            provable_cards.add(card_id)

    distinct_pairs = scenario.get("distinct_entities", [])
    if not isinstance(distinct_pairs, list):
        errors.append("distinct_entities must be a list")
        distinct_pairs = []
    actor_set = set(actor_values)
    for index, pair in enumerate(distinct_pairs):
        label = f"distinct_entities[{index}]"
        if not (
            isinstance(pair, list)
            and len(pair) == 2
            and all(isinstance(value, str) and value for value in pair)
        ):
            errors.append(f"{label} must contain two non-empty entity IDs")
            continue
        left, right = pair
        if left == right:
            errors.append(f"{label} is reflexive; an entity cannot be distinct from itself")
        if left not in actor_set or right not in actor_set:
            errors.append(f"{label} must refer to entities in the actor tuple")

    close_case = scenario.get("close_case")
    if not isinstance(close_case, bool):
        errors.append("close_case must be boolean")
    elif close_case:
        if not selected_set:
            errors.append("a closed case must contain at least one router-selected card")
        missing = sorted(selected_set - provable_cards)
        if missing:
            errors.append(
                "case_assessment_complete is forbidden until every selected card has "
                f"a provable assessment: {missing}"
            )

    if errors:
        raise ScallopFactValidationError(errors)


def render_scenario_facts(
    rule_ir: Mapping[str, Any], scenario: Mapping[str, Any]
) -> str:
    """Render only contract-validated input relations, never arbitrary model code."""

    validate_scenario(rule_ir, scenario)
    role_predicate, actor_fields = _role_contract(rule_ir)
    actors = [str(scenario[field]) for field in actor_fields]
    case_id, defendant_id = actors[:2]
    card_inputs = _card_input_predicates(rule_ir)
    lines = ["", f"// runtime scenario: {scenario['scenario_id']}"]
    lines.append(_fact(role_predicate, actors))

    for assessment in scenario["assessments"]:
        assessment_id = assessment["assessment_id"]
        arguments = [
            case_id,
            assessment_id,
            *actors[1:],
            assessment["status"],
        ]
        lines.append(_fact(card_inputs[assessment["card_id"]], arguments))
        if assessment["provable"]:
            lines.append(_fact("provable", [case_id, assessment_id]))

    emitted_pairs: set[tuple[str, str]] = set()
    for left, right in scenario.get("distinct_entities", []):
        for pair in ((left, right), (right, left)):
            if pair not in emitted_pairs:
                lines.append(_fact("distinct_entity", [case_id, *pair]))
                emitted_pairs.add(pair)

    if scenario["close_case"]:
        lines.append(_fact("case_assessment_complete", [case_id, defendant_id]))
    return "\n".join(lines) + "\n"


class ScallopScenarioResult(dict):
    """Dictionary mapping query relations to outputs, preserving proof_dag as metadata attribute."""
    def __init__(
        self,
        *args,
        proof_dag: dict[str, Any] | None = None,
        raw_output: str = "",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.proof_dag = proof_dag or {}
        self.raw_output = raw_output

    def __getitem__(self, key: Any) -> Any:
        if key == "_proof_dag":
            return self.proof_dag
        return super().__getitem__(key)

    def get(self, key: Any, default: Any = None) -> Any:
        # ``dict.get`` bypasses ``__getitem__``, so the proof DAG has to be
        # surfaced here as well or every ``raw.get("_proof_dag")`` caller
        # silently receives ``None``.
        if key == "_proof_dag":
            return self.proof_dag
        return super().get(key, default)

    def __contains__(self, key: Any) -> bool:
        if key == "_proof_dag":
            return True
        return super().__contains__(key)


def run_scenario(
    *,
    rule_ir: Mapping[str, Any],
    compiled_source: str,
    scenario: Mapping[str, Any],
    query_relations: Sequence[str],
    scli_path: Path,
    work_dir: Path,
) -> ScallopScenarioResult:
    facts = render_scenario_facts(rule_ir, scenario)
    predicate_ids = {
        predicate["id"] for predicate in rule_ir.get("predicates", [])
    }
    unknown_queries = sorted(set(query_relations) - predicate_ids)
    if unknown_queries:
        raise ScallopFactValidationError(
            [f"query_relations contains unknown predicates: {unknown_queries}"]
        )
    work_dir.mkdir(parents=True, exist_ok=True)
    program_path = work_dir / f"{scenario['scenario_id']}.scl"
    program_path.write_text(compiled_source + facts, encoding="utf-8")

    # Compiling a large generated program dominates runtime.  Ask the pinned CLI
    # for every relation once, then parse only the requested public relations,
    # instead of recompiling the identical program once per query.
    completed = subprocess.run(
        [str(scli_path), "--output-all", str(program_path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode != 0:
        raise ScallopRuntimeError(
            f"scli failed for {scenario['scenario_id']}: "
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )
    output = completed.stdout.strip()
    relations_tuples = parse_scallop_relations(output)
    results = ScallopScenarioResult(raw_output=output)
    for relation in query_relations:
        tuples = relations_tuples.get(relation, set())
        # ``output`` is deliberately not repeated per relation: it is the same
        # ``--output-all`` dump for every query and copying it once per query
        # inflated native reports by hundreds of kilobytes.
        results[relation] = {
            "nonempty": len(tuples) > 0,
            "proven_tuples": [list(t) for t in sorted(tuples)],
        }
    proof_dag = extract_proof_dag(rule_ir=rule_ir, relations_tuples=relations_tuples, query_relations=query_relations)
    results.proof_dag = proof_dag
    return results


def parse_scallop_relations(output: str) -> dict[str, set[tuple[str, ...]]]:
    """Parse all relations and their proven tuples from scli --output-all stdout."""

    results: dict[str, set[tuple[str, ...]]] = {}
    pattern = re.compile(r"(?m)^\s*([a-zA-Z0-9_]+)\s*:\s*\{(.*?)\}")
    for match in pattern.finditer(output):
        rel_name = match.group(1)
        raw_body = match.group(2).strip()
        tuples: set[tuple[str, ...]] = set()
        if raw_body:
            # Match tuple patterns like ("a", "b") or ("a", "b", "c")
            tuple_pattern = re.compile(r"\((.*?)\)")
            for t_match in tuple_pattern.finditer(raw_body):
                items = [
                    item.strip().strip('"').strip("'")
                    for item in t_match.group(1).split(",")
                    if item.strip()
                ]
                if items:
                    tuples.add(tuple(items))
        results[rel_name] = tuples
    return results


def extract_proof_dag(
    *,
    rule_ir: Mapping[str, Any],
    relations_tuples: dict[str, set[tuple[str, ...]]],
    query_relations: Sequence[str],
) -> dict[str, Any]:
    """Extract causal proof trace (fired rules, proven tuples, causal antecedents)."""

    proven_relations = {rel for rel, tuples in relations_tuples.items() if tuples}
    fired_rules: list[str] = []
    proof_tree: dict[str, list[dict[str, Any]]] = {}
    # Which requirement stopped a conclusion.  Without this a unit that misses a
    # single element reports a bare 미확정, and the answer has nothing to say
    # about why.
    blocked: dict[str, set[str]] = {}

    for rule_entry in rule_ir.get("rules", []):
        rule_id = str(rule_entry.get("id", ""))
        head = rule_entry.get("head", {})
        head_name = str(head.get("predicate") or head.get("name") or "")
        body = rule_entry.get("body", [])

        # Rule fires if all positive body atoms are proven relations
        body_names = [str(atom_entry.get("predicate") or atom_entry.get("name") or "") for atom_entry in body if not atom_entry.get("negated")]
        if body_names and all(b_name in proven_relations for b_name in body_names):
            if head_name in proven_relations:
                fired_rules.append(rule_id)
                if head_name not in proof_tree:
                    proof_tree[head_name] = []
                proof_tree[head_name].append({
                    "rule_id": rule_id,
                    "antecedents": body_names,
                    "description": rule_entry.get("description", ""),
                })
        elif head_name.endswith(("_elements_satisfied", "_established")) \
                and head_name not in proven_relations:
            missing = [name for name in body_names if name not in proven_relations]
            if missing:
                blocked.setdefault(head_name, set()).update(missing)

    return {
        "fired_rules": sorted(set(fired_rules)),
        "proven_relations": sorted(proven_relations),
        "proof_tree": proof_tree,
        "blocked_conclusions": {
            head: sorted(names) for head, names in sorted(blocked.items())
        },
    }


def runtime_version(scli_path: Path) -> str:
    completed = subprocess.run(
        [str(scli_path), "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return completed.stdout.strip()


def _card_input_predicates(rule_ir: Mapping[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    duplicates: set[str] = set()
    for predicate in rule_ir.get("predicates", []):
        if predicate.get("origin") != "commentary" or predicate.get("role") != "input":
            continue
        for card_id in predicate.get("norm_card_ids", []):
            if card_id in result:
                duplicates.add(card_id)
            result[card_id] = predicate["id"]
    if duplicates:
        raise ScallopFactValidationError(
            [f"multiple input predicates implement cards: {sorted(duplicates)}"]
        )
    return result


def _fact(predicate: str, values: Sequence[str]) -> str:
    arguments = ", ".join(json.dumps(value, ensure_ascii=False) for value in values)
    return f"rel {predicate}({arguments})"


def _query_output_nonempty(output: str, relation: str) -> bool:
    match = re.search(rf"(?ms)^\s*{re.escape(relation)}\s*:\s*\{{(.*?)\}}\s*$", output)
    if match is None:
        raise ScallopRuntimeError(f"cannot parse scli query output for {relation}: {output}")
    return bool(match.group(1).strip())
