"""Registry-native host path from predicate assessment to Scallop conclusions.

The model selects closed unit ids and assesses every registered commentary predicate.
It never selects cards, emits Scallop code, or writes the legal conclusion.  The host
loads the whole unit contract, validates grounded evidence, executes the committed SCL,
and exposes only runtime-derived directives to the writer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.neural.fact_graph import assessment_facts
from idpr.neural.issue_assessment import (
    issue_assessment_request,
    validate_issue_assessments,
)
from idpr.rulegen.registry import (
    PROJECT_ROOT,
    PredicateIRMissing,
    build_registry,
    resolve_unit,
)
from idpr.rulegen.scallop_runtime import run_scenario


DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"


class NativeHostError(ValueError):
    """A closed host contract was violated before symbolic execution."""


def closed_issue_selection_schema(
    *, case_id: str, root: Path = PROJECT_ROOT
) -> dict[str, Any]:
    """Return the no-search, registry-enumerated model output grammar."""

    unit_ids = sorted(build_registry(root).keys())
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/RuleIRNativeIssueSelection",
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "case_id", "issues"],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "issues": {
                "type": "array",
                "minItems": 1,
                "maxItems": 16,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "issue_id", "unit_id", "reported_label", "source_quote",
                        "role_candidates",
                    ],
                    "properties": {
                        "issue_id": {
                            "type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]*$"
                        },
                        "unit_id": {"enum": [*unit_ids, "unsupported"]},
                        "reported_label": {"type": "string", "minLength": 1},
                        "source_quote": {"type": "string", "minLength": 1},
                        "role_candidates": {
                            "type": "object",
                            "additionalProperties": {"type": "string", "minLength": 1},
                        },
                    },
                },
            },
        },
    }


def validate_closed_issue_selection(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    question_text: str,
    root: Path = PROJECT_ROOT,
) -> None:
    """Reject invented units, duplicate issues, and ungrounded issue spotting."""

    schema = closed_issue_selection_schema(case_id=case_id, root=root)
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]
    issues = payload.get("issues", [])
    if isinstance(issues, list):
        ids = [item.get("issue_id") for item in issues if isinstance(item, Mapping)]
        if len(ids) != len(set(ids)):
            errors.append("issue_id values must be unique")
        for item in issues:
            if isinstance(item, Mapping) and item.get("source_quote") not in question_text:
                errors.append(f"{item.get('issue_id')}: source_quote is not in case text")
    if errors:
        raise NativeHostError("; ".join(errors))


def selected_predicate_requests(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    selection: Mapping[str, Any],
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Resolve a closed selection without retrieval or a generic fallback."""

    case_id = str(case.get("sub_question_id", ""))
    validate_closed_issue_selection(
        selection,
        case_id=case_id,
        question_text=str(case.get("question_text", "")),
        root=root,
    )
    requests = []
    for issue in selection["issues"]:
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            requests.append({
                "issue_id": issue["issue_id"],
                "unit_id": unit_id,
                "status": "predicate_ir_missing",
                "detail": f"No registered RuleIR for {issue['reported_label']}",
            })
            continue
        requests.append({
            "issue_id": issue["issue_id"],
            "unit_id": unit_id,
            "assessment_request": predicate_assessment_request(
                case=case, fact_graph=fact_graph, unit_id=unit_id, root=root
            ),
        })
    return {
        "case_id": case_id,
        "selection_mode": "closed_registry_enum",
        "semantic_search_used": False,
        "requests": requests,
    }


def predicate_assessment_request(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    unit_id: str,
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Load every predicate for one model-selected registered unit."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    issues = []
    for predicate in entry.commentary_inputs:
        sources = predicate.get("source_refs", [])
        rules = [
            str(source.get("quote"))
            for source in sources
            if isinstance(source, Mapping) and source.get("quote")
        ] or [str(predicate.get("definition", predicate["id"]))]
        issues.append({
            "issue_id": predicate["id"],
            "question": str(predicate.get("definition", predicate["id"])),
            "rules": rules,
            "stage_kind": "rule_ir_predicate",
            "details": [
                {"id": card_id, "proposition": str(predicate.get("definition", ""))}
                for card_id in predicate.get("norm_card_ids", [])
            ],
        })
    request = issue_assessment_request(case=case, fact_graph=fact_graph, issues=issues)
    request["unit_id"] = unit_id
    request["role_contract"] = {
        "predicate": entry.role_predicate["id"],
        "arguments": [item["name"] for item in entry.role_predicate["arguments"]],
    }
    request["query_relations"] = list(entry.query_relations)
    request["all_registered_predicates_loaded"] = True
    return request


def execute_native_unit(
    *,
    unit_id: str,
    case_id: str,
    role_values: Mapping[str, str],
    fact_graph: Mapping[str, Any],
    assessment_payload: Mapping[str, Any],
    distinct_entities: Sequence[Sequence[str]] = (),
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Validate a complete predicate assessment and run the registered program."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    fact_ids = tuple(item["fact_id"] for item in assessment_facts(fact_graph))
    predicate_ids = tuple(item["id"] for item in entry.commentary_inputs)
    validate_issue_assessments(
        assessment_payload,
        case_id=case_id,
        issue_ids=predicate_ids,
        fact_ids=fact_ids,
    )
    expected_roles = [item["name"] for item in entry.role_predicate["arguments"]]
    unknown_roles = sorted(set(role_values) - set(expected_roles))
    missing_roles = [name for name in expected_roles if name not in role_values]
    if unknown_roles or missing_roles or role_values.get("case_id") != case_id:
        raise NativeHostError(
            f"{unit_id}: invalid role tuple; missing={missing_roles}, "
            f"unknown={unknown_roles}, case_id={role_values.get('case_id')!r}"
        )

    card_by_predicate: dict[str, str] = {}
    for predicate in entry.commentary_inputs:
        cards = predicate.get("norm_card_ids", [])
        if len(cards) != 1:
            raise NativeHostError(
                f"{unit_id}:{predicate['id']} must map to exactly one NormCard"
            )
        card_by_predicate[predicate["id"]] = cards[0]
    assessments = []
    evidence: dict[str, Any] = {}
    for index, predicate_id in enumerate(predicate_ids, 1):
        item = assessment_payload["assessments"][predicate_id]
        assessments.append({
            "assessment_id": f"assessment_{index:04d}",
            "card_id": card_by_predicate[predicate_id],
            "status": item["status"],
            "provable": True,
        })
        evidence[predicate_id] = {
            "norm_card_id": card_by_predicate[predicate_id],
            "status": item["status"],
            "basis_fact_ids": list(item["basis_fact_ids"]),
            "counter_fact_ids": list(item["counter_fact_ids"]),
            "missing_facts": list(item["missing_facts"]),
        }
    scenario = {
        "scenario_id": f"{case_id}.{unit_id}",
        **dict(role_values),
        "selected_card_ids": list(card_by_predicate.values()),
        "assessments": assessments,
        "distinct_entities": [list(pair) for pair in distinct_entities],
        "close_case": True,
    }
    rule_ir = json.loads((root / entry.rule_ir_path).read_text(encoding="utf-8"))
    compiled = (root / entry.compiled_scl_path).read_text(encoding="utf-8")
    raw = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled,
        scenario=scenario,
        query_relations=entry.query_relations,
        scli_path=scli_path,
        work_dir=work_dir,
    )
    observed = {relation: result["nonempty"] for relation, result in raw.items()}
    established = [
        relation for relation, nonempty in observed.items()
        if nonempty and relation.endswith("_established")
        and not relation.endswith("_not_established")
    ]
    if observed.get(f"{unit_id}_conflict"):
        status = "conflict"
    elif established:
        status = "established"
    elif observed.get(f"{unit_id}_not_established"):
        status = "not_established"
    elif observed.get(f"{unit_id}_undetermined"):
        status = "undetermined"
    else:
        status = "no_derived_outcome"
    return {
        "status": "executed",
        "unit_id": unit_id,
        "symbolic_conclusion": status,
        "established_relations": established,
        "query_results": observed,
        "assessment_evidence": evidence,
        "runtime": "scallop_scli",
    }


def execute_native_case(
    *,
    case_id: str,
    fact_graph: Mapping[str, Any],
    unit_runs: Sequence[Mapping[str, Any]],
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Execute model-selected units in order, including explicit outcome bridges."""

    results: dict[str, dict[str, Any]] = {}
    for run in unit_runs:
        unit_id = str(run["unit_id"])
        entry = resolve_unit(unit_id, root=root)
        if isinstance(entry, PredicateIRMissing):
            results[unit_id] = entry.to_dict()
            continue
        dependencies = tuple(str(value) for value in run.get("depends_on", []))
        if entry.shared_module and not dependencies:
            raise NativeHostError(f"{unit_id}: shared module requires depends_on bridge")
        unavailable = [
            dependency for dependency in dependencies
            if results.get(dependency, {}).get("symbolic_conclusion") != "established"
        ]
        if unavailable:
            results[unit_id] = {
                "status": "prerequisite_not_established",
                "unit_id": unit_id,
                "dependencies": list(dependencies),
                "unavailable": unavailable,
            }
            continue
        results[unit_id] = execute_native_unit(
            unit_id=unit_id,
            case_id=case_id,
            role_values=run["role_values"],
            fact_graph=fact_graph,
            assessment_payload=run["assessment_payload"],
            distinct_entities=run.get("distinct_entities", ()),
            root=root,
            scli_path=scli_path,
            work_dir=work_dir / unit_id,
        )
    directives = [
        {
            "unit_id": unit_id,
            "symbolic_conclusion": result["symbolic_conclusion"],
            "established_relations": result["established_relations"],
            "evidence": result["assessment_evidence"],
        }
        for unit_id, result in results.items()
        if result.get("status") == "executed"
    ]
    return {
        "case_id": case_id,
        "unit_results": results,
        "generation_contract": {
            "source": "scallop_derivation_only",
            "conclusion_directives": directives,
            "model_may_override_symbolic_conclusion": False,
        },
    }
