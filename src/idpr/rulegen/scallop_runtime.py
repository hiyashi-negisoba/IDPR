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


def validate_scenario(
    rule_ir: Mapping[str, Any], scenario: Mapping[str, Any]
) -> None:
    errors: list[str] = []
    scenario_id = scenario.get("scenario_id")
    if not isinstance(scenario_id, str) or not SCENARIO_ID.fullmatch(scenario_id):
        errors.append("scenario_id must be a safe lowercase identifier")
    actor_values: list[str] = []
    for field in ACTOR_FIELDS:
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
    actors = [str(scenario[field]) for field in ACTOR_FIELDS]
    case_id, defendant_id = actors[:2]
    card_inputs = _card_input_predicates(rule_ir)
    lines = ["", f"// runtime scenario: {scenario['scenario_id']}"]
    lines.append(_fact("fraud_case_roles", actors))

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


def run_scenario(
    *,
    rule_ir: Mapping[str, Any],
    compiled_source: str,
    scenario: Mapping[str, Any],
    query_relations: Sequence[str],
    scli_path: Path,
    work_dir: Path,
) -> dict[str, dict[str, Any]]:
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

    results: dict[str, dict[str, Any]] = {}
    for relation in query_relations:
        completed = subprocess.run(
            [str(scli_path), "--query", relation, str(program_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if completed.returncode != 0:
            raise ScallopRuntimeError(
                f"scli failed for {scenario['scenario_id']}:{relation}: "
                f"{completed.stderr.strip() or completed.stdout.strip()}"
            )
        output = completed.stdout.strip()
        results[relation] = {
            "nonempty": _query_output_nonempty(output, relation),
            "output": output,
        }
    return results


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
