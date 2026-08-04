"""Neural contracts for unit-conditioned role binding and core assessment."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


STATUSES = ("satisfied", "not_satisfied", "unknown")


class CoreContractError(ValueError):
    pass


def core_issue_selection_schema(
    *, case_id: str, unit_ids: Sequence[str]
) -> dict[str, Any]:
    """Select issues only; legal role binding deliberately happens later."""

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "case_id", "issues"],
        "properties": {
            "version": {"const": "3.0.0"},
            "case_id": {"const": case_id},
            "issues": {
                "type": "array",
                "minItems": 1,
                "maxItems": 16,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "issue_id", "unit_id", "reported_label", "subject",
                        "conduct_claims",
                    ],
                    "properties": {
                        "issue_id": {
                            "type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]*$"
                        },
                        "unit_id": {"enum": [*unit_ids, "unsupported"]},
                        "reported_label": {"type": "string", "minLength": 1},
                        "subject": {
                            "type": "object", "additionalProperties": False,
                            "required": ["label", "source_quotes"],
                            "properties": {
                                "label": {"type": "string", "minLength": 1},
                                "source_quotes": {
                                    "type": "array", "minItems": 1, "maxItems": 6,
                                    "uniqueItems": True,
                                    "items": {"type": "string", "minLength": 1},
                                },
                            },
                        },
                        "conduct_claims": {
                            "type": "array", "minItems": 1, "maxItems": 8,
                            "items": {
                                "type": "object", "additionalProperties": False,
                                "required": ["claim", "source_quotes"],
                                "properties": {
                                    "claim": {
                                        "type": "string", "minLength": 1,
                                        "maxLength": 800,
                                    },
                                    "source_quotes": {
                                        "type": "array", "minItems": 1,
                                        "maxItems": 8, "uniqueItems": True,
                                        "items": {"type": "string", "minLength": 1},
                                    },
                                },
                            },
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
    case_text: str,
    unit_ids: Sequence[str],
) -> None:
    errors = [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(
            core_issue_selection_schema(case_id=case_id, unit_ids=unit_ids)
        ).iter_errors(payload)
    ]
    issues = payload.get("issues", [])
    issue_ids = [item.get("issue_id") for item in issues if isinstance(item, Mapping)]
    if len(issue_ids) != len(set(issue_ids)):
        errors.append("issue_id values must be unique")
    conduct_keys: list[tuple[str, str, tuple[str, ...]]] = []
    for item in issues:
        if not isinstance(item, Mapping):
            continue
        subject = item.get("subject", {})
        if isinstance(subject, Mapping):
            for quote in subject.get("source_quotes", []):
                if quote not in case_text:
                    errors.append(
                        f"{item.get('issue_id')}: subject evidence is not an exact "
                        f"contiguous substring of case text: {quote!r}"
                    )
        for conduct in item.get("conduct_claims", []):
            if not isinstance(conduct, Mapping):
                continue
            quotes = tuple(str(quote) for quote in conduct.get("source_quotes", []))
            for quote in quotes:
                if quote in case_text:
                    continue
                errors.append(
                    f"{item.get('issue_id')}: conduct evidence is not an exact "
                    f"contiguous substring of case text: {quote!r}"
                )
            conduct_keys.append((
                str(subject.get("label")), str(item.get("unit_id")), quotes,
            ))
        if item.get("unit_id") == "unsupported" and str(
            item.get("reported_label", "")
        ).strip().lower() == "unsupported":
            errors.append(f"{item.get('issue_id')}: unsupported requires a descriptive label")
    if len(conduct_keys) != len(set(conduct_keys)):
        errors.append("the same subject/unit/conduct quote is assigned to duplicate issues")
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
        "required": ["entity_id", "source_quotes", "reason"],
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
                    "required": [
                        "track_id", "applies_to_entity_id", "source_quotes", "reason"
                    ],
                    "properties": {
                        "track_id": {"enum": track_ids},
                        "applies_to_entity_id": {"type": "string", "minLength": 1},
                        "source_quotes": {
                            "type": "array", "minItems": 1, "maxItems": 6,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "reason": {"type": "string", "minLength": 1, "maxLength": 600},
                    },
                },
            },
            "entities": {
                "type": "array", "minItems": 1, "maxItems": 32,
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["entity_id", "label", "source_quotes"],
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
                "type": "array", "maxItems": 64,
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": [
                        "relation_id", "subject_id", "relation", "object_id",
                        "source_quote",
                    ],
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
    entities = payload.get("entities", [])
    entity_ids = [item.get("entity_id") for item in entities if isinstance(item, Mapping)]
    if len(entity_ids) != len(set(entity_ids)):
        errors.append("entity_id values must be unique")
    known = set(entity_ids)
    for entity in entities:
        if isinstance(entity, Mapping):
            for quote in entity.get("source_quotes", []):
                if quote not in case_text:
                    errors.append(f"entity {entity.get('entity_id')}: ungrounded quote {quote!r}")
    bindings = payload.get("role_bindings", {})
    defendant_entity_id = None
    if isinstance(bindings, Mapping):
        for role, binding in bindings.items():
            if isinstance(binding, Mapping):
                if binding.get("entity_id") not in known:
                    errors.append(f"{role}: binding points to unknown entity")
                for quote in binding.get("source_quotes", []):
                    if quote not in case_text:
                        errors.append(f"{role}: ungrounded quote {quote!r}")
        defendant = bindings.get("defendant_id")
        if isinstance(defendant, Mapping):
            defendant_entity_id = defendant.get("entity_id")
            entity = next(
                (item for item in entities if item.get("entity_id") == defendant_entity_id),
                {},
            )
            entity_quotes = entity.get("source_quotes", [])
            binding_quotes = defendant.get("source_quotes", [])
            subject_quotes = subject.get("source_quotes", [])
            subject_evidence_preserved = any(
                evidence == quote or evidence in quote or quote in evidence
                for evidence in subject_quotes
                for quote in [*entity_quotes, *binding_quotes]
            )
            if entity.get("label") != subject.get("label"):
                errors.append(
                    "defendant entity label must equal the selected issue subject label"
                )
            if not subject_evidence_preserved:
                errors.append(
                    "defendant entity or binding must preserve exact evidence for the "
                    "selected issue subject"
                )
    relation_ids: list[Any] = []
    for relation in payload.get("relations", []):
        if not isinstance(relation, Mapping):
            continue
        relation_ids.append(relation.get("relation_id"))
        if relation.get("subject_id") not in known or relation.get("object_id") not in known:
            errors.append(f"{relation.get('relation_id')}: relation uses unknown entity")
        if relation.get("source_quote") not in case_text:
            errors.append(f"{relation.get('relation_id')}: ungrounded source_quote")
    if len(relation_ids) != len(set(relation_ids)):
        errors.append("relation_id values must be unique")
    track_ids = []
    for selection in payload.get("track_selections", []):
        if not isinstance(selection, Mapping):
            continue
        track_ids.append(selection.get("track_id"))
        if selection.get("applies_to_entity_id") != defendant_entity_id:
            errors.append(
                f"{selection.get('track_id')}: track must apply to the issue defendant"
            )
        for quote in selection.get("source_quotes", []):
            if quote not in case_text:
                errors.append(f"{selection.get('track_id')}: ungrounded track quote")
    if len(track_ids) != len(set(track_ids)):
        errors.append("track_id values must be unique")
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
        "required": ["status", "source_quotes", "reason", "missing_facts"],
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
    assessments = payload.get("assessments", {})
    if isinstance(assessments, Mapping):
        for predicate_id, item in assessments.items():
            if not isinstance(item, Mapping):
                continue
            quotes = item.get("source_quotes", [])
            if any(quote not in case_text for quote in quotes):
                errors.append(f"{predicate_id}: source quote is not in case text")
            status = item.get("status")
            if status == "satisfied" and not quotes:
                errors.append(f"{predicate_id}: satisfied requires source quote")
            if status == "not_satisfied" and not quotes:
                errors.append(f"{predicate_id}: not_satisfied requires counter quote")
            if status == "unknown" and not item.get("missing_facts"):
                errors.append(f"{predicate_id}: unknown requires missing_facts")
            if status != "unknown" and item.get("missing_facts"):
                errors.append(f"{predicate_id}: non-unknown cannot report missing_facts")
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
