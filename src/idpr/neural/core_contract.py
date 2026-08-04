"""Neural contracts for unit-conditioned role binding and core assessment."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


STATUSES = ("satisfied", "not_satisfied", "unknown")


class CoreContractError(ValueError):
    pass


def core_fact_inventory_schema(*, case_id: str) -> dict[str, Any]:
    """Extract grounded actors and atomic facts without choosing legal units."""

    actor = {
        "type": "object", "additionalProperties": False,
        "required": ["actor_id", "label", "source_quotes"],
        "properties": {
            "actor_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]*$"},
            "label": {"type": "string", "minLength": 1, "maxLength": 120},
            "source_quotes": {
                "type": "array", "minItems": 1, "maxItems": 8,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    fact = {
        "type": "object", "additionalProperties": False,
        "required": [
            "fact_id", "fact_type", "focus_actor_id", "related_actor_ids",
            "claim", "source_quotes",
        ],
        "properties": {
            "fact_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]*$"},
            "fact_type": {
                "enum": [
                    "act", "statement", "transfer", "result", "state",
                    "relationship", "omission",
                ]
            },
            "focus_actor_id": {"type": "string", "minLength": 1},
            "related_actor_ids": {
                "type": "array", "maxItems": 12, "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
            "claim": {"type": "string", "minLength": 1, "maxLength": 800},
            "source_quotes": {
                "type": "array", "minItems": 1, "maxItems": 8,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    return {
        "type": "object", "additionalProperties": False,
        "required": ["version", "case_id", "actors", "facts"],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "actors": {"type": "array", "minItems": 1, "maxItems": 32, "items": actor},
            "facts": {"type": "array", "minItems": 1, "maxItems": 96, "items": fact},
        },
    }


def validate_core_fact_inventory(
    payload: Mapping[str, Any], *, case_id: str, case_text: str
) -> None:
    errors = [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(
            core_fact_inventory_schema(case_id=case_id)
        ).iter_errors(payload)
    ]
    actors = payload.get("actors", [])
    actor_ids = [item.get("actor_id") for item in actors if isinstance(item, Mapping)]
    if len(actor_ids) != len(set(actor_ids)):
        errors.append("actor_id values must be unique")
    known_actors = set(actor_ids)
    facts = payload.get("facts", [])
    fact_ids = [item.get("fact_id") for item in facts if isinstance(item, Mapping)]
    if len(fact_ids) != len(set(fact_ids)):
        errors.append("fact_id values must be unique")
    for fact in facts:
        if not isinstance(fact, Mapping):
            continue
        referenced = [fact.get("focus_actor_id"), *fact.get("related_actor_ids", [])]
        unknown = [actor_id for actor_id in referenced if actor_id not in known_actors]
        if unknown:
            errors.append(f"{fact.get('fact_id')}: unknown actor references {unknown}")
    if errors:
        raise CoreContractError("; ".join(errors))


def core_issue_selection_schema(
    *, case_id: str, unit_ids: Sequence[str], actor_ids: Sequence[str],
    fact_ids: Sequence[str],
) -> dict[str, Any]:
    """Classify the closed grounded inventory; role binding happens later."""

    return {
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
                        "issue_id", "unit_id", "reported_label",
                        "subject_actor_id", "fact_ids",
                    ],
                    "properties": {
                        "issue_id": {
                            "type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]*$"
                        },
                        "unit_id": {"enum": [*unit_ids, "unsupported"]},
                        "reported_label": {"type": "string", "minLength": 1},
                        "subject_actor_id": {"enum": list(actor_ids)},
                        "fact_ids": {
                            "type": "array", "minItems": 1, "maxItems": 24,
                            "uniqueItems": True, "items": {"enum": list(fact_ids)},
                        },
                    },
                },
            },
        },
    }


def validate_core_issue_selection(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    unit_ids: Sequence[str],
    inventory: Mapping[str, Any],
) -> None:
    actor_ids = [str(item["actor_id"]) for item in inventory["actors"]]
    fact_ids = [str(item["fact_id"]) for item in inventory["facts"]]
    errors = [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(
            core_issue_selection_schema(
                case_id=case_id, unit_ids=unit_ids,
                actor_ids=actor_ids, fact_ids=fact_ids,
            )
        ).iter_errors(payload)
    ]
    issues = payload.get("issues", [])
    issue_ids = [item.get("issue_id") for item in issues if isinstance(item, Mapping)]
    if len(issue_ids) != len(set(issue_ids)):
        errors.append("issue_id values must be unique")
    for item in issues:
        if not isinstance(item, Mapping):
            continue
        if item.get("unit_id") == "unsupported" and str(
            item.get("reported_label", "")
        ).strip().lower() == "unsupported":
            errors.append(f"{item.get('issue_id')}: unsupported requires a descriptive label")
    if errors:
        raise CoreContractError("; ".join(errors))


def role_binding_schema(
    *, case_id: str, issue_id: str, profile: Mapping[str, Any]
) -> dict[str, Any]:
    role_names = [
        item["name"] for item in profile["role_contract"]["arguments"]
        if item["name"] != "case_id"
    ]
    track_ids = [item["track_id"] for item in profile["tracks"]]
    binding = {
        "type": "object",
        "additionalProperties": False,
        "required": ["entity_id", "reason"],
        "properties": {
            "entity_id": {"type": "string", "minLength": 1},
            "source_quotes": {
                "type": "array", "minItems": 1, "maxItems": 4,
                "items": {"type": "string", "minLength": 1},
            },
            "reason": {"type": "string", "minLength": 1, "maxLength": 500},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "version", "case_id", "issue_id", "unit_id", "track_selections",
            "entities", "role_bindings", "relations",
        ],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "issue_id": {"const": issue_id},
            "unit_id": {"const": profile["unit_id"]},
            "track_selections": {
                "type": "array", "minItems": 1, "maxItems": len(track_ids),
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["track_id", "reason"],
                    "properties": {
                        "track_id": {"enum": track_ids},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 600},
                    },
                },
            },
            "entities": {
                "type": "array", "minItems": 1, "maxItems": 32,
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["entity_id", "label"],
                    "properties": {
                        "entity_id": {"type": "string", "minLength": 1},
                        "label": {"type": "string", "minLength": 1},
                        "source_quotes": {
                            "type": "array", "minItems": 1, "maxItems": 8,
                            "items": {"type": "string", "minLength": 1},
                        },
                    },
                },
            },
            "role_bindings": {
                "type": "object", "additionalProperties": False,
                "required": role_names,
                "properties": {name: binding for name in role_names},
            },
            "relations": {
                "type": "array", "maxItems": 16,
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["relation_id", "subject_id", "relation", "object_id"],
                    "properties": {
                        "relation_id": {"type": "string", "minLength": 1},
                        "subject_id": {"type": "string", "minLength": 1},
                        "relation": {"type": "string", "minLength": 1},
                        "object_id": {"type": "string", "minLength": 1},
                        "source_quote": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def validate_role_binding(
    payload: Mapping[str, Any],
    *,
    case_text: str,
    case_id: str,
    issue_id: str,
    profile: Mapping[str, Any],
    subject: Mapping[str, Any],
) -> None:
    errors = [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(
            role_binding_schema(case_id=case_id, issue_id=issue_id, profile=profile)
        ).iter_errors(payload)
    ]
    if errors:
        raise CoreContractError("; ".join(errors))


def binding_track_ids(binding: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(item["track_id"]) for item in binding["track_selections"])


def selected_track_closure(
    profile: Mapping[str, Any], selected_tracks: Sequence[str]
) -> tuple[str, ...]:
    by_id = {item["track_id"]: item for item in profile["tracks"]}
    relation_to_track = {
        item["elements_relation"]: item["track_id"] for item in profile["tracks"]
    }
    unknown = sorted(set(selected_tracks) - set(by_id))
    if unknown:
        raise CoreContractError(f"unknown tracks for {profile['unit_id']}: {unknown}")
    result: list[str] = []

    def visit(track_id: str) -> None:
        for path in by_id[track_id]["paths"]:
            for relation in path["depends_on_elements"]:
                dependency = relation_to_track.get(relation)
                if dependency is None:
                    raise CoreContractError(
                        f"{track_id}: unresolved elements dependency {relation}"
                    )
                visit(dependency)
        if track_id not in result:
            result.append(track_id)

    for selected in selected_tracks:
        visit(selected)
    return tuple(result)


def assessment_groups(
    profile: Mapping[str, Any],
    selected_tracks: Sequence[str],
    *,
    max_predicates: int = 12,
) -> tuple[dict[str, Any], ...]:
    if max_predicates < 1:
        raise CoreContractError("max_predicates must be positive")
    predicates = {
        item["predicate_id"]: item for item in profile["model_input_predicates"]
    }
    by_track = {item["track_id"]: item for item in profile["tracks"]}
    seen: set[str] = set()
    groups = []
    for track_id in selected_track_closure(profile, selected_tracks):
        ordered = []
        for path in by_track[track_id]["paths"]:
            for predicate_id in path["components"]:
                if predicate_id not in seen:
                    seen.add(predicate_id)
                    ordered.append(predicates[predicate_id])
        for offset in range(0, len(ordered), max_predicates):
            groups.append({
                "group_id": f"{track_id}.{offset // max_predicates + 1:02d}",
                "track_id": track_id,
                "predicates": ordered[offset:offset + max_predicates],
            })
    return tuple(groups)


def core_assessment_schema(
    *, case_id: str, predicate_ids: Sequence[str]
) -> dict[str, Any]:
    assessment = {
        "type": "object", "additionalProperties": False,
        "required": ["status", "reason"],
        "properties": {
            "status": {"enum": list(STATUSES)},
            "source_quotes": {
                "type": "array", "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
            "reason": {"type": "string", "minLength": 1, "maxLength": 1200},
            "missing_facts": {
                "type": "array", "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    return {
        "type": "object", "additionalProperties": False,
        "required": ["version", "case_id", "assessments"],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "assessments": {
                "type": "object", "additionalProperties": False,
                "required": list(predicate_ids),
                "properties": {predicate_id: assessment for predicate_id in predicate_ids},
            },
        },
    }


def validate_core_assessments(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    case_text: str,
    predicate_ids: Sequence[str],
) -> None:
    errors = [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(
            core_assessment_schema(case_id=case_id, predicate_ids=predicate_ids)
        ).iter_errors(payload)
    ]
    if errors:
        raise CoreContractError("; ".join(errors))


def context_packet(
    profile: Mapping[str, Any], predicate_ids: Sequence[str], *, max_sources: int = 6
) -> dict[str, Any]:
    """Bounded predicate-conditioned authority lookup; it cannot alter the predicate set."""

    by_id = {item["predicate_id"]: item for item in profile["model_input_predicates"]}
    unknown = sorted(set(predicate_ids) - set(by_id))
    if unknown:
        raise CoreContractError(f"context requested for unknown predicates: {unknown}")
    return {
        "mode": "selected_predicate_context_only",
        "predicate_set_mutable": False,
        "external_search_used": False,
        "items": {
            predicate_id: {
                "authority_card_ids": by_id[predicate_id]["authority_card_ids"],
                "source_refs": by_id[predicate_id]["source_refs"][:max_sources],
            }
            for predicate_id in predicate_ids
        },
    }
