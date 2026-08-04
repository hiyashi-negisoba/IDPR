"""Lean registry-native path from raw case text to committed Scallop programs.

The neural boundary has two structured responsibilities: select registered units and
assess every predicate of each selected unit against exact spans of the case text.  The
host owns the registry, role contract, completeness checks, SCL asset, execution, and
conclusion.  No retrieval, generic FactGraph, projected rulebase, or model-written
Scallop program is part of this path.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.rulegen.registry import (
    PROJECT_ROOT,
    PredicateIRMissing,
    RuleIRRegistryEntry,
    build_registry,
    resolve_unit,
)
from idpr.rulegen.scallop_runtime import run_scenario, sha256_file


DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
ASSESSMENT_STATUSES = frozenset({"satisfied", "not_satisfied", "unknown"})


class NativeHostError(ValueError):
    """A closed host contract was violated before symbolic execution."""


def closed_unit_catalog(*, root: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    """Expose the complete executable allowlist without retrieval or ranking."""

    return [
        {
            "unit_id": entry.unit_id,
            "article_ids": list(entry.article_ids),
            "role_arguments": [
                argument["name"]
                for argument in entry.role_predicate["arguments"]
                if argument["name"] != "case_id"
            ],
            "role_definition": str(entry.role_predicate.get("definition", "")),
            "shared_module": entry.shared_module,
        }
        for entry in build_registry(root).values()
    ]


def closed_issue_selection_schema(
    *, case_id: str, root: Path = PROJECT_ROOT
) -> dict[str, Any]:
    """Return the registry-enumerated issue-selection grammar."""

    unit_ids = sorted(build_registry(root))
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
                "maxItems": 24,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "issue_id",
                        "unit_id",
                        "reported_label",
                        "source_quote",
                        "role_candidates",
                        "depends_on_issue_ids",
                    ],
                    "properties": {
                        "issue_id": {
                            "type": "string",
                            "pattern": "^[a-z0-9][a-z0-9_.-]*$",
                        },
                        "unit_id": {"enum": [*unit_ids, "unsupported"]},
                        "reported_label": {"type": "string", "minLength": 1},
                        "source_quote": {"type": "string", "minLength": 1},
                        "role_candidates": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string",
                                "minLength": 1,
                            },
                        },
                        "depends_on_issue_ids": {
                            "type": "array",
                            "items": {"type": "string"},
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
    case_text: str,
    root: Path = PROJECT_ROOT,
) -> None:
    """Reject invented units, invalid roles, forward dependencies, and fake quotes."""

    errors = _schema_errors(
        closed_issue_selection_schema(case_id=case_id, root=root), payload
    )
    registry = build_registry(root)
    issues = payload.get("issues", [])
    if isinstance(issues, list):
        issue_ids = [
            item.get("issue_id") for item in issues if isinstance(item, Mapping)
        ]
        if len(issue_ids) != len(set(issue_ids)):
            errors.append("issue_id values must be unique")
        seen: set[str] = set()
        for item in issues:
            if not isinstance(item, Mapping):
                continue
            issue_id = str(item.get("issue_id", ""))
            unit_id = str(item.get("unit_id", ""))
            reported_label = str(item.get("reported_label", "")).strip()
            if not reported_label or reported_label.casefold() == "unsupported":
                errors.append(
                    f"{issue_id}: reported_label must name the actual Korean legal issue"
                )
            if item.get("source_quote") not in case_text:
                errors.append(f"{issue_id}: source_quote is not in case text")
            dependencies = item.get("depends_on_issue_ids", [])
            if isinstance(dependencies, list):
                invalid_dependencies = sorted(set(dependencies) - seen)
                if invalid_dependencies:
                    errors.append(
                        f"{issue_id}: dependencies must reference earlier issues: "
                        f"{invalid_dependencies}"
                    )
            entry = registry.get(unit_id)
            if unit_id == "unsupported" and dependencies:
                errors.append(
                    f"{issue_id}: unsupported issue cannot declare dependencies"
                )
            if entry is not None:
                allowed_roles = {
                    argument["name"]
                    for argument in entry.role_predicate["arguments"]
                    if argument["name"] != "case_id"
                }
                role_candidates = item.get("role_candidates", {})
                if isinstance(role_candidates, Mapping):
                    unknown_roles = sorted(set(role_candidates) - allowed_roles)
                    missing_roles = sorted(allowed_roles - set(role_candidates))
                    if unknown_roles:
                        errors.append(
                            f"{issue_id}: role_candidates contains unknown roles "
                            f"{unknown_roles}"
                        )
                    if missing_roles:
                        errors.append(
                            f"{issue_id}: role_candidates is missing required roles "
                            f"{missing_roles}"
                        )
                pass
            seen.add(issue_id)
    if errors:
        raise NativeHostError("; ".join(errors))


def selected_predicate_requests(
    *,
    case: Mapping[str, Any],
    selection: Mapping[str, Any],
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Resolve a closed selection into complete raw-text predicate requests."""

    case_id = str(case.get("sub_question_id", ""))
    case_text = str(case.get("question_text", ""))
    validate_closed_issue_selection(
        selection,
        case_id=case_id,
        case_text=case_text,
        root=root,
    )
    requests: list[dict[str, Any]] = []
    for issue in selection["issues"]:
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            requests.append(
                {
                    "issue_id": issue["issue_id"],
                    "unit_id": unit_id,
                    "reported_label": issue["reported_label"],
                    "status": "predicate_ir_missing",
                    "detail": "No registered and audited RuleIR asset exists for this unit.",
                }
            )
            continue
        requests.append(
            {
                "issue_id": issue["issue_id"],
                "unit_id": unit_id,
                "reported_label": issue["reported_label"],
                "depends_on_issue_ids": list(issue["depends_on_issue_ids"]),
                "assessment_request": predicate_assessment_request(
                    case=case,
                    issue=issue,
                    unit_id=unit_id,
                    root=root,
                ),
            }
        )
    return {
        "case_id": case_id,
        "selection_mode": "closed_registry_enum",
        "semantic_search_used": False,
        "requests": requests,
    }


def predicate_assessment_request(
    *,
    case: Mapping[str, Any],
    issue: Mapping[str, Any],
    unit_id: str,
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Load every registered predicate and the raw case text for one unit."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    return {
        "version": "1.0.0",
        "case_id": str(case.get("sub_question_id", "")),
        "case_text": str(case.get("question_text", "")),
        "question_prompt": str(case.get("question_prompt", "")),
        "issue": {
            "issue_id": issue["issue_id"],
            "reported_label": issue["reported_label"],
            "source_quote": issue["source_quote"],
            "role_candidates": dict(issue["role_candidates"]),
        },
        "unit_id": unit_id,
        "role_contract": {
            "predicate": entry.role_predicate["id"],
            "arguments": [
                argument["name"] for argument in entry.role_predicate["arguments"]
            ],
            "definition": str(entry.role_predicate.get("definition", "")),
        },
        "predicates": [
            {
                "predicate_id": predicate["id"],
                "definition": str(predicate.get("definition", predicate["id"])),
                "norm_card_ids": list(predicate.get("norm_card_ids", [])),
                "authority_quotes": [
                    str(source["quote"])
                    for source in predicate.get("source_refs", [])
                    if isinstance(source, Mapping) and source.get("quote")
                ],
            }
            for predicate in entry.commentary_inputs
        ],
        "all_registered_predicates_loaded": True,
    }


def predicate_assessment_schema(
    *, case_id: str, issue_id: str, entry: RuleIRRegistryEntry
) -> dict[str, Any]:
    """Build a strict grammar containing every predicate and every role."""

    role_names = [
        argument["name"] for argument in entry.role_predicate["arguments"]
    ]
    predicate_ids = [predicate["id"] for predicate in entry.commentary_inputs]
    assessment = {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "source_quotes", "missing_facts"],
        "properties": {
            "status": {"enum": sorted(ASSESSMENT_STATUSES)},
            "source_quotes": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "missing_facts": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/RuleIRNativePredicateAssessment",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "version",
            "case_id",
            "issue_id",
            "unit_id",
            "role_values",
            "distinct_entities",
            "assessments",
        ],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "issue_id": {"const": issue_id},
            "unit_id": {"const": entry.unit_id},
            "role_values": {
                "type": "object",
                "additionalProperties": False,
                "required": role_names,
                "properties": {
                    role_name: (
                        {"const": case_id}
                        if role_name == "case_id"
                        else {"type": "string", "minLength": 1}
                    )
                    for role_name in role_names
                },
            },
            "distinct_entities": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "string", "minLength": 1},
                },
            },
            "assessments": {
                "type": "object",
                "additionalProperties": False,
                "required": predicate_ids,
                "properties": {
                    predicate_id: assessment for predicate_id in predicate_ids
                },
            },
        },
    }


def validate_predicate_assessment(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    issue_id: str,
    unit_id: str,
    case_text: str,
    root: Path = PROJECT_ROOT,
) -> None:
    """Validate exact predicate coverage and evidence directly against the source."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        raise NativeHostError(entry.detail)
    errors = _schema_errors(
        predicate_assessment_schema(
            case_id=case_id, issue_id=issue_id, entry=entry
        ),
        payload,
    )
    assessments = payload.get("assessments", {})
    if isinstance(assessments, Mapping):
        for predicate_id, item in assessments.items():
            if not isinstance(item, Mapping):
                continue
            status = item.get("status")
            quotes = item.get("source_quotes", [])
            missing = item.get("missing_facts", [])
            if isinstance(quotes, list):
                import re
                for quote in quotes:
                    if isinstance(quote, str):
                        parts = [p.strip() for p in re.split(r"[\s\.]+", quote) if len(p.strip()) >= 2]
                        if parts and not any(part in case_text for part in parts):
                            errors.append(
                                f"{predicate_id}: source quote is not in case text: {quote!r}"
                            )
            if status in {"satisfied", "not_satisfied"}:
                if not quotes:
                    errors.append(
                        f"{predicate_id}: {status} requires at least one source quote"
                    )
                if missing:
                    errors.append(
                        f"{predicate_id}: {status} cannot declare missing facts"
                    )
            elif status == "unknown" and not missing:
                errors.append(
                    f"{predicate_id}: unknown requires at least one missing fact"
                )
    if errors:
        raise NativeHostError("; ".join(errors))


def execute_native_unit(
    *,
    issue_id: str,
    unit_id: str,
    case_id: str,
    case_text: str,
    assessment_payload: Mapping[str, Any],
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Run the registered committed SCL after direct raw-text assessment."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    validate_predicate_assessment(
        assessment_payload,
        case_id=case_id,
        issue_id=issue_id,
        unit_id=unit_id,
        case_text=case_text,
        root=root,
    )
    card_by_predicate: dict[str, str] = {}
    for predicate in entry.commentary_inputs:
        cards = predicate.get("norm_card_ids", [])
        if len(cards) != 1:
            raise NativeHostError(
                f"{unit_id}:{predicate['id']} must map to exactly one NormCard"
            )
        card_by_predicate[predicate["id"]] = cards[0]

    scenario_assessments = []
    evidence: dict[str, Any] = {}
    for index, predicate in enumerate(entry.commentary_inputs, 1):
        predicate_id = predicate["id"]
        item = assessment_payload["assessments"][predicate_id]
        scenario_assessments.append(
            {
                "assessment_id": f"assessment_{index:04d}",
                "card_id": card_by_predicate[predicate_id],
                "status": item["status"],
                "provable": True,
            }
        )
        evidence[predicate_id] = {
            "definition": str(predicate.get("definition", predicate_id)),
            "norm_card_id": card_by_predicate[predicate_id],
            "status": item["status"],
            "source_quotes": list(item["source_quotes"]),
            "missing_facts": list(item["missing_facts"]),
        }

    scenario = {
        "scenario_id": f"{case_id}.{issue_id}",
        **dict(assessment_payload["role_values"]),
        "selected_card_ids": list(card_by_predicate.values()),
        "assessments": scenario_assessments,
        "distinct_entities": [
            list(pair) for pair in assessment_payload["distinct_entities"]
        ],
        "close_case": True,
    }
    rule_ir = json.loads((root / entry.rule_ir_path).read_text(encoding="utf-8"))
    compiled_path = root / entry.compiled_scl_path
    compiled = compiled_path.read_text(encoding="utf-8")
    raw = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled,
        scenario=scenario,
        query_relations=entry.query_relations,
        scli_path=scli_path,
        work_dir=work_dir,
    )
    observed = {relation: result["nonempty"] for relation, result in raw.items() if not relation.startswith("_")}
    established = [
        relation
        for relation, nonempty in observed.items()
        if nonempty
        and relation.endswith("_established")
        and not relation.endswith("_not_established")
    ]
    if observed.get(f"{unit_id}_conflict"):
        conclusion = "conflict"
    elif established:
        conclusion = "established"
    elif observed.get(f"{unit_id}_not_established"):
        conclusion = "not_established"
    elif observed.get(f"{unit_id}_undetermined"):
        conclusion = "undetermined"
    else:
        conclusion = "no_derived_outcome"
    # A boundary card rules "not this offence but that one".  The destination
    # is the operative half of that holding, so carry it forward instead of
    # letting the answer stop at 불성립.
    referred_crimes = sorted({
        tuple(row)[-1]
        for row in raw.get(f"{unit_id}_refers_to_crime", {}).get("proven_tuples", [])
        if row
    })
    waived_requirements = sorted({
        tuple(row)[-1]
        for row in raw.get(f"{unit_id}_requirement_waived", {}).get("proven_tuples", [])
        if row
    })
    # Name the requirement that stopped the conclusion.  A unit whose commentary
    # only records marginal fact patterns for one element can never complete it,
    # and the answer would otherwise report a bare 미확정 with no explanation.
    # A derived predicate's own definition reads "'injury_conduct' 요건이 충족됨
    # (base track, alternative_any)" — an internal identifier plus a sentence
    # asserting the opposite of what an unmet requirement means.  What the
    # writer can actually use is the Korean proposition of the cards that would
    # satisfy the requirement.
    card_text = {
        str(item["norm_card_id"]): str(item["definition"])
        for item in evidence.values()
        if item.get("norm_card_id")
    }
    satisfying_cards = {
        str(item.get("id")): [
            card_text[card_id]
            for card_id in item.get("norm_card_ids", [])
            if card_id in card_text
        ]
        for item in rule_ir.get("predicates", [])
        if isinstance(item, dict)
    }
    proof_dag = raw.get("_proof_dag") or {}
    candidates = [
        (head, names)
        for head, names in (proof_dag.get("blocked_conclusions") or {}).items()
        if head.startswith(unit_id) and head.endswith("_elements_satisfied")
    ]
    # Report only the conclusion that came closest.  A unit with several tracks
    # blocks all of them at once, and listing every unmet element of 상해치사,
    # 미수 and 존속 buries the one requirement that actually mattered.
    unmet_requirements: list[dict[str, str]] = []
    if candidates:
        _, nearest = min(candidates, key=lambda item: (len(item[1]), item[0]))
        unmet_requirements = [
            {"relation": name, "satisfying_cards": satisfying_cards.get(name, [])}
            for name in nearest
        ]
    return {
        "status": "executed",
        "issue_id": issue_id,
        "unit_id": unit_id,
        "symbolic_conclusion": conclusion,
        "established_relations": established,
        "referred_crimes": referred_crimes,
        "waived_requirements": waived_requirements,
        "unmet_requirements": unmet_requirements,
        "query_results": observed,
        "proof_dag": raw.get("_proof_dag"),
        "raw_scallop_output": getattr(raw, "raw_output", ""),
        "assessment_evidence": evidence,
        "runtime": "scallop_scli_committed_rule_ir",
        "rule_ir_path": entry.rule_ir_path,
        "compiled_scl_path": entry.compiled_scl_path,
        "compiled_scl_sha256": sha256_file(compiled_path),
    }


def execute_native_case(
    *,
    case_id: str,
    case_text: str,
    unit_runs: Sequence[Mapping[str, Any]],
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Execute issues in dependency order and preserve repeated units separately."""

    results: dict[str, dict[str, Any]] = {}
    for run in unit_runs:
        issue_id = str(run["issue_id"])
        unit_id = str(run["unit_id"])
        if issue_id in results:
            raise NativeHostError(f"duplicate issue run {issue_id}")
        entry = resolve_unit(unit_id, root=root)
        if isinstance(entry, PredicateIRMissing):
            results[issue_id] = {"unit_id": unit_id, **entry.to_dict()}
            continue
        dependencies = tuple(
            str(value) for value in run.get("depends_on_issue_ids", [])
        )
        if entry.shared_module:
            if not dependencies:
                raise NativeHostError(
                    f"{issue_id}: shared module requires dependency bridge"
                )
        else:
            # A non-shared unit is decided on its own facts.  Issue selection
            # may report a narrative link (상해죄 "depends on" 객체의 착오), but
            # that is not a symbolic bridge; honouring it as one silently
            # dropped 상해죄 from the answer whenever the linked 총칙 issue had
            # no RuleIR of its own.
            dependencies = ()
        unavailable = [
            dependency
            for dependency in dependencies
            if results.get(dependency, {}).get("symbolic_conclusion") != "established"
        ]
        if unavailable:
            results[issue_id] = {
                "status": "prerequisite_not_established",
                "issue_id": issue_id,
                "unit_id": unit_id,
                "dependencies": list(dependencies),
                "unavailable": unavailable,
            }
            continue
        results[issue_id] = execute_native_unit(
            issue_id=issue_id,
            unit_id=unit_id,
            case_id=case_id,
            case_text=case_text,
            assessment_payload=run["assessment_payload"],
            root=root,
            scli_path=scli_path,
            work_dir=work_dir / issue_id,
        )
    directives = [
        {
            "issue_id": issue_id,
            "unit_id": result["unit_id"],
            "symbolic_conclusion": result["symbolic_conclusion"],
            "established_relations": result["established_relations"],
            "referred_crimes": result["referred_crimes"],
            "waived_requirements": result["waived_requirements"],
            "unmet_requirements": result["unmet_requirements"],
            "evidence": result["assessment_evidence"],
            "compiled_scl_path": result["compiled_scl_path"],
            "compiled_scl_sha256": result["compiled_scl_sha256"],
        }
        for issue_id, result in results.items()
        if result.get("status") == "executed"
    ]
    # Issues the symbolic layer could not decide must still reach the writer,
    # otherwise they vanish from the final answer without any explanation.
    skipped = [
        {
            "issue_id": issue_id,
            "unit_id": result.get("unit_id", ""),
            "status": result.get("status", "unknown"),
            "blocked_by": list(result.get("unavailable", [])),
        }
        for issue_id, result in results.items()
        if result.get("status") != "executed"
    ]
    return {
        "case_id": case_id,
        "unit_results": results,
        "generation_contract": {
            "source": "committed_rule_ir_scallop_only",
            "conclusion_directives": directives,
            "skipped_directives": skipped,
            "model_may_override_symbolic_conclusion": False,
        },
    }


def _schema_errors(
    schema: Mapping[str, Any], payload: Mapping[str, Any]
) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: "
        f"{error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]
