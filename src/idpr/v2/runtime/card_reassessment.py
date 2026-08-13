"""Atomic card-informed reassessment for an existing UNKNOWN Call 2 target.

This is a recovery boundary, not a second router.  The host fixes one existing target,
one factual occurrence and one reviewed issue.  Legal materials provide standards only;
they are never evidence that the facts in those materials occurred in the current case.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    PredicateAssessment,
    PredicateDefinition,
)


class CardReassessmentError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True, slots=True)
class LegalMaterial:
    material_id: str
    proposition: str
    role: str
    source_card_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "material_id": self.material_id,
            "proposition": self.proposition,
            "role": self.role,
            "source_card_ids": list(self.source_card_ids),
        }


@dataclass(frozen=True, slots=True)
class CardReassessmentTarget:
    target: AssessmentTarget
    evidence_source_text: str
    evidence_source_start: int
    evidence_source_end: int
    question_assumptions: tuple[Mapping[str, Any], ...]
    issue_id: str
    issue_question: str
    materials: tuple[LegalMaterial, ...]
    projection_targets: tuple[AssessmentTarget, ...]

    def __post_init__(self) -> None:
        if not self.evidence_source_text:
            raise CardReassessmentError(["evidence_source_text must not be empty"])
        if self.evidence_source_start < 0 or self.evidence_source_end <= self.evidence_source_start:
            raise CardReassessmentError(["evidence source span is invalid"])
        if not self.issue_id or not self.issue_question or not self.materials:
            raise CardReassessmentError(
                ["one reviewed issue and at least one legal material are required"]
            )
        material_ids = [value.material_id for value in self.materials]
        if len(material_ids) != len(set(material_ids)):
            raise CardReassessmentError(["legal material ids contain duplicates"])
        if not self.projection_targets or self.target not in self.projection_targets:
            raise CardReassessmentError(
                ["projection_targets must include the assessed target"]
            )


@dataclass(frozen=True, slots=True)
class CardReassessment:
    target: CardReassessmentTarget
    truth: TruthValue
    evidence_quotes: tuple[str, ...]
    applied_material_ids: tuple[str, ...]
    missing_information: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "assessment_target": self.target.target.as_dict(),
            "projection_targets": [value.as_dict() for value in self.target.projection_targets],
            "issue_id": self.target.issue_id,
            "truth": self.truth,
            "evidence_quotes": list(self.evidence_quotes),
            "applied_material_ids": list(self.applied_material_ids),
            "missing_information": list(self.missing_information),
        }


def card_reassessment_payload(
    target: CardReassessmentTarget,
    predicate: PredicateDefinition,
) -> dict[str, Any]:
    if target.target.predicate_ref != predicate.predicate_ref:
        raise CardReassessmentError(["target and predicate definition refs differ"])
    return {
        "assessment_target": target.target.as_dict(),
        "original_truth": UNKNOWN,
        "evidence_occurrence": {
            "actor_id": target.target.instance_key.actor_id,
            "source_text": target.evidence_source_text,
            "source_span": {
                "start": target.evidence_source_start,
                "end": target.evidence_source_end,
            },
        },
        "question_assumptions": [dict(value) for value in target.question_assumptions],
        "predicate_definition": predicate.as_dict(),
        "reviewed_issue": {
            "issue_id": target.issue_id,
            "question": target.issue_question,
            "legal_materials": [value.as_dict() for value in target.materials],
        },
    }


def card_reassessment_schema(target: CardReassessmentTarget) -> dict[str, Any]:
    material_ids = [value.material_id for value in target.materials]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "truth",
            "evidence_quotes",
            "applied_material_ids",
            "missing_information",
        ],
        "properties": {
            "truth": {"type": "string", "enum": [FALSE, TRUE, UNKNOWN]},
            "evidence_quotes": {
                "type": "array",
                "maxItems": 4,
                "items": {"type": "string", "minLength": 1, "maxLength": 1000},
            },
            "applied_material_ids": {
                "type": "array",
                "maxItems": len(material_ids),
                "items": {"type": "string", "enum": material_ids},
            },
            "missing_information": {
                "type": "array",
                "maxItems": 4,
                "items": {"type": "string", "minLength": 1, "maxLength": 500},
            },
        },
    }


def validate_card_reassessment_output(
    payload: Any,
    *,
    target: CardReassessmentTarget,
) -> CardReassessment:
    if not isinstance(payload, Mapping):
        raise CardReassessmentError(["response must be an object"])
    required = {
        "truth",
        "evidence_quotes",
        "applied_material_ids",
        "missing_information",
    }
    errors: list[str] = []
    if set(payload) != required:
        errors.append(f"response fields must be exactly {sorted(required)}")
    truth = payload.get("truth")
    if truth not in {TRUE, FALSE, UNKNOWN}:
        errors.append("truth must be TRUE, FALSE, or UNKNOWN")

    def strings(name: str, *, limit: int) -> tuple[str, ...]:
        raw = payload.get(name)
        if not isinstance(raw, list) or len(raw) > limit:
            errors.append(f"{name} must be an array with at most {limit} items")
            return ()
        if any(not isinstance(value, str) or not value.strip() for value in raw):
            errors.append(f"{name} must contain nonempty strings")
            return ()
        values = tuple(raw)
        if len(values) != len(set(values)):
            errors.append(f"{name} contains duplicates")
        return values

    evidence_quotes = strings("evidence_quotes", limit=4)
    applied_material_ids = strings(
        "applied_material_ids", limit=len(target.materials)
    )
    missing_information = strings("missing_information", limit=4)
    allowed_materials = {value.material_id for value in target.materials}
    outside = set(applied_material_ids) - allowed_materials
    if outside:
        errors.append(f"applied_material_ids contains unknown ids: {sorted(outside)}")
    for quote in evidence_quotes:
        if quote not in target.evidence_source_text:
            errors.append(f"evidence quote is not an exact source substring: {quote!r}")
    if truth in {TRUE, FALSE}:
        if not evidence_quotes:
            errors.append(f"{truth} requires at least one exact evidence quote")
        if not applied_material_ids:
            errors.append(f"{truth} requires at least one applied legal material")
        if missing_information:
            errors.append(f"{truth} requires empty missing_information")
    if truth == UNKNOWN:
        if not missing_information:
            errors.append("UNKNOWN requires concrete missing_information")
        if applied_material_ids and not evidence_quotes:
            errors.append(
                "UNKNOWN with applied legal materials requires an exact evidence quote"
            )
    if errors:
        raise CardReassessmentError(errors)
    return CardReassessment(
        target=target,
        truth=truth,
        evidence_quotes=evidence_quotes,
        applied_material_ids=applied_material_ids,
        missing_information=missing_information,
    )


def merge_unknown_reassessments(
    original: Iterable[PredicateAssessment],
    recoveries: Iterable[CardReassessment],
) -> tuple[PredicateAssessment, ...]:
    """Replace only exact original UNKNOWN keys; project shared GroundFacts explicitly."""
    values = tuple(original)
    index = {value.target: value for value in values}
    if len(index) != len(values):
        raise CardReassessmentError(["original assessments contain duplicate targets"])
    replacement: dict[AssessmentTarget, TruthValue] = {}
    for recovery in recoveries:
        for target in recovery.target.projection_targets:
            current = index.get(target)
            if current is None:
                raise CardReassessmentError(
                    [f"recovery projection target is absent: {target.as_dict()}"]
                )
            if current.truth != UNKNOWN:
                raise CardReassessmentError(
                    [f"recovery cannot replace non-UNKNOWN target: {target.as_dict()}"]
                )
            previous = replacement.get(target)
            if previous is not None and previous != recovery.truth:
                raise CardReassessmentError(
                    [f"conflicting recovery truths for target: {target.as_dict()}"]
                )
            replacement[target] = recovery.truth
    return tuple(
        PredicateAssessment(value.target, replacement.get(value.target, value.truth))
        for value in values
    )


__all__ = [
    "CardReassessment",
    "CardReassessmentError",
    "CardReassessmentTarget",
    "LegalMaterial",
    "card_reassessment_payload",
    "card_reassessment_schema",
    "merge_unknown_reassessments",
    "validate_card_reassessment_output",
]
