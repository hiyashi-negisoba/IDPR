"""Lean neural contracts for the core RuleIR pipeline."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


STATUSES = ("satisfied", "not_satisfied", "unknown")


class CoreContractError(ValueError):
    pass


def _errors(payload: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return [
        f"{'.'.join(str(x) for x in error.path) or '$'}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]


def core_issue_selection_schema(
    *, case_id: str, unit_ids: Sequence[str]
) -> dict[str, Any]:
    """Select only a closed unit, its subject, and the conduct being assessed."""

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["case_id", "issues"],
        "properties": {
            "case_id": {"const": case_id},
            "issues": {
                "type": "array",
                "minItems": 1,
                "maxItems": 16,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["unit_id", "issue_label", "subject", "conduct"],
                    "properties": {
                        "unit_id": {"enum": [*unit_ids, "unsupported"]},
                        "issue_label": {
                            "type": "string", "minLength": 1, "maxLength": 160
                        },
                        "subject": {
                            "type": "string", "minLength": 1, "maxLength": 120
                        },
                        "conduct": {
                            "type": "string", "minLength": 1, "maxLength": 1200
                        },
                    },
                },
            },
        },
    }


def validate_core_issue_selection(
    payload: Mapping[str, Any], *, case_id: str, unit_ids: Sequence[str]
) -> None:
    errors = _errors(
        payload, core_issue_selection_schema(case_id=case_id, unit_ids=unit_ids)
    )
    if errors:
        raise CoreContractError("; ".join(errors))


def core_unit_analysis_schema(
    *, case_id: str, issue_id: str, profile: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind roles, select tracks, and assess every core predicate in one call."""

    role_names = [
        item["name"]
        for item in profile["role_contract"]["arguments"]
        if item["name"] != "case_id"
    ]
    track_ids = [item["track_id"] for item in profile["tracks"]]
    predicate_ids = [
        item["predicate_id"] for item in profile["model_input_predicates"]
    ]
    assessment = {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "reason"],
        "properties": {
            "status": {"enum": list(STATUSES)},
            "reason": {"type": "string", "minLength": 1, "maxLength": 1200},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "case_id", "issue_id", "selected_tracks", "role_values", "assessments"
        ],
        "properties": {
            "case_id": {"const": case_id},
            "issue_id": {"const": issue_id},
            "selected_tracks": {
                "type": "array",
                "minItems": 1,
                "maxItems": len(track_ids),
                "uniqueItems": True,
                "items": {"enum": track_ids},
            },
            "role_values": {
                "type": "object",
                "additionalProperties": False,
                "required": role_names,
                "properties": {
                    name: {"type": "string", "minLength": 1, "maxLength": 160}
                    for name in role_names
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


def validate_core_unit_analysis(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    issue_id: str,
    profile: Mapping[str, Any],
) -> None:
    errors = _errors(
        payload,
        core_unit_analysis_schema(
            case_id=case_id, issue_id=issue_id, profile=profile
        ),
    )
    tracks = payload.get("selected_tracks", [])
    if isinstance(tracks, list) and len(tracks) != len(set(tracks)):
        errors.append("selected_tracks must be unique")
    if errors:
        raise CoreContractError("; ".join(errors))


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


def needed_predicate_ids(
    profile: Mapping[str, Any], selected_tracks: Sequence[str]
) -> tuple[str, ...]:
    tracks = {item["track_id"]: item for item in profile["tracks"]}
    return tuple(dict.fromkeys(
        component
        for track_id in selected_track_closure(profile, selected_tracks)
        for path in tracks[track_id]["paths"]
        for component in path["components"]
    ))
