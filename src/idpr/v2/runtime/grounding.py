"""Occurrence-scoped Call 2 predicate assessment and CaseTruths projection."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from idpr.v2.evaluate import TruthValue
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

PredicateKind = Literal["ground_fact", "legal_element"]
_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})


class GroundingContractError(ValueError):
    """A Call 2 request, response, or exact-key projection is invalid."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class PredicateDefinition:
    predicate_ref: str
    kind: PredicateKind
    canonical_meaning: str
    arguments: tuple[Mapping[str, Any], ...]
    legal_standard: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "predicate_ref": self.predicate_ref,
            "kind": self.kind,
            "canonical_meaning": self.canonical_meaning,
            "arguments": [dict(argument) for argument in self.arguments],
        }
        if self.legal_standard is not None:
            value["legal_standard"] = self.legal_standard
        return value


@dataclass(frozen=True)
class AssessmentTarget:
    instance_key: OffenseInstanceKey
    predicate_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "instance_key": instance_key_dict(self.instance_key),
            "predicate_ref": self.predicate_ref,
        }


@dataclass(frozen=True)
class PredicateAssessment:
    target: AssessmentTarget
    truth: TruthValue

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.target.as_dict(),
            "truth": self.truth,
        }


def instance_key_dict(instance: OffenseInstanceKey) -> dict[str, str]:
    return {
        "case_id": instance.case_id,
        "actor_id": instance.actor_id,
        "offense_ref": instance.offense_ref,
        "occurrence_id": instance.occurrence_id,
    }


def predicate_definitions(
    registry: DefinitionRegistry, refs: Iterable[str]
) -> tuple[PredicateDefinition, ...]:
    """Resolve only the selected instance-bound predicate kinds."""
    values: list[PredicateDefinition] = []
    seen: set[str] = set()
    for ref in refs:
        if ref in seen:
            raise GroundingContractError([f"duplicate selected predicate ref: {ref!r}"])
        seen.add(ref)
        entry = registry.get(ref)
        if entry is None or entry.kind not in {"ground_fact", "legal_element"}:
            raise GroundingContractError([f"invalid selected predicate ref: {ref!r}"])
        meaning = entry.payload.get("canonical_meaning")
        arguments = entry.payload.get("arguments")
        if not isinstance(meaning, str) or not isinstance(arguments, list):
            raise GroundingContractError([f"malformed predicate definition: {ref!r}"])
        standard = entry.payload.get("legal_standard")
        values.append(
            PredicateDefinition(
                predicate_ref=ref,
                kind=entry.kind,
                canonical_meaning=meaning,
                arguments=tuple(dict(argument) for argument in arguments),
                legal_standard=standard if isinstance(standard, str) else None,
            )
        )
    return tuple(values)


def assessment_targets(
    instances: Iterable[OffenseInstanceKey], predicate_refs: Iterable[str]
) -> tuple[AssessmentTarget, ...]:
    """Stable instance-major product used for deterministic sharding."""
    instance_values = tuple(instances)
    refs = tuple(predicate_refs)
    if len(instance_values) != len(set(instance_values)):
        raise GroundingContractError(["assessment instances contain duplicates"])
    if len(refs) != len(set(refs)):
        raise GroundingContractError(["selected predicate refs contain duplicates"])
    return tuple(AssessmentTarget(instance, ref) for instance in instance_values for ref in refs)


def shard_assessment_targets(
    targets: Iterable[AssessmentTarget], *, max_targets: int
) -> tuple[tuple[AssessmentTarget, ...], ...]:
    """Deterministically shard one logical Call 2 stage into physical requests."""
    if max_targets <= 0:
        raise GroundingContractError(["max_targets must be positive"])
    values = tuple(targets)
    return tuple(
        values[index : index + max_targets]
        for index in range(0, len(values), max_targets)
    )


def shard_assessment_targets_by_occurrence(
    targets: Iterable[AssessmentTarget], *, max_targets: int
) -> tuple[tuple[AssessmentTarget, ...], ...]:
    """Preserve target order while making every physical request evidence-homogeneous."""
    if max_targets <= 0:
        raise GroundingContractError(["max_targets must be positive"])
    shards: list[tuple[AssessmentTarget, ...]] = []
    current: list[AssessmentTarget] = []
    current_occurrence_id: str | None = None
    for target in targets:
        occurrence_id = target.instance_key.occurrence_id
        if current and (
            occurrence_id != current_occurrence_id or len(current) == max_targets
        ):
            shards.append(tuple(current))
            current = []
        if not current:
            current_occurrence_id = occurrence_id
        current.append(target)
    if current:
        shards.append(tuple(current))
    return tuple(shards)


def call2_request_payload(
    *,
    evidence_occurrence: GoldOccurrence,
    predicates: Iterable[PredicateDefinition],
    targets: Iterable[AssessmentTarget],
) -> dict[str, Any]:
    """Build one shard whose only factual evidence is one gold occurrence span."""
    predicate_values = tuple(predicates)
    predicate_refs = {value.predicate_ref for value in predicate_values}
    target_values = tuple(targets)
    if not target_values:
        raise GroundingContractError(["an empty target set is a host no-op"])
    errors: list[str] = []
    for target in target_values:
        if target.instance_key.occurrence_id != evidence_occurrence.occurrence_id:
            errors.append(
                "target occurrence differs from the request evidence occurrence: "
                f"{target.instance_key.occurrence_id!r} != "
                f"{evidence_occurrence.occurrence_id!r}"
            )
        if target.instance_key.actor_id != evidence_occurrence.actor_id:
            errors.append(
                "target actor differs from the request evidence actor: "
                f"{target.instance_key.actor_id!r} != {evidence_occurrence.actor_id!r}"
            )
        if target.predicate_ref not in predicate_refs:
            errors.append(f"unknown selected predicate: {target.predicate_ref!r}")
    if errors:
        raise GroundingContractError(errors)
    return {
        "evidence_occurrence": evidence_occurrence.as_dict(),
        "predicate_catalog": [value.as_dict() for value in predicate_values],
        "assessment_targets": [target.as_dict() for target in target_values],
    }


def call2_schema(targets: Iterable[AssessmentTarget]) -> dict[str, Any]:
    target_values = tuple(targets)
    if not target_values:
        raise GroundingContractError(["an empty target set has no response schema"])
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["truths"],
        "properties": {
            "truths": {
                "type": "array",
                "minItems": len(target_values),
                "maxItems": len(target_values),
                "items": {"type": "string", "enum": sorted(_TRUTHS)},
            },
        },
    }


def _parse_instance_key(value: Any, *, where: str, errors: list[str]) -> OffenseInstanceKey | None:
    fields = {"case_id", "actor_id", "offense_ref", "occurrence_id"}
    if not isinstance(value, Mapping) or set(value) != fields:
        errors.append(f"{where} must contain exactly {sorted(fields)}")
        return None
    if not all(isinstance(value[field], str) and value[field] for field in fields):
        errors.append(f"{where} fields must be nonempty strings")
        return None
    return OffenseInstanceKey(
        value["case_id"], value["actor_id"], value["offense_ref"], value["occurrence_id"]
    )


def validate_call2_output(
    payload: Any, *, targets: Iterable[AssessmentTarget]
) -> tuple[PredicateAssessment, ...]:
    """Validate exact ordered keys; the model cannot select instances or predicates."""
    expected = tuple(targets)
    if not isinstance(payload, Mapping):
        raise GroundingContractError(["response must be an object"])
    errors: list[str] = []
    if set(payload) != {"truths"}:
        errors.append("response must contain exactly truths")
    raw_values = payload.get("truths")
    if not isinstance(raw_values, list):
        errors.append("truths must be an array")
        raw_values = []
    if len(raw_values) != len(expected):
        errors.append(f"truths must contain exactly {len(expected)} entries")
    values: list[PredicateAssessment] = []
    for index, truth in enumerate(raw_values):
        where = f"truths[{index}]"
        if not isinstance(truth, str) or truth not in _TRUTHS:
            errors.append(f"{where} must be one of {sorted(_TRUTHS)}")
            continue
        if index < len(expected):
            values.append(PredicateAssessment(expected[index], truth))
    if errors:
        raise GroundingContractError(errors)
    return tuple(values)


def case_truths_from_assessments(
    assessments: Iterable[PredicateAssessment],
    *,
    expected_targets: Iterable[AssessmentTarget],
) -> CaseTruths:
    """Exact-total projection into the sole predicate truth store."""
    values = tuple(assessments)
    expected = tuple(expected_targets)
    actual_targets = tuple(value.target for value in values)
    if actual_targets != expected:
        raise GroundingContractError(["assessment keys do not exactly cover expected targets"])
    mapping = {(value.target.instance_key, value.target.predicate_ref): value.truth for value in values}
    if len(mapping) != len(values):
        raise GroundingContractError(["assessment projection contains duplicate keys"])
    return CaseTruths(predicate=mapping)


__all__ = [
    "AssessmentTarget",
    "GroundingContractError",
    "PredicateAssessment",
    "PredicateDefinition",
    "assessment_targets",
    "call2_request_payload",
    "call2_schema",
    "case_truths_from_assessments",
    "instance_key_dict",
    "predicate_definitions",
    "shard_assessment_targets",
    "shard_assessment_targets_by_occurrence",
    "validate_call2_output",
]
