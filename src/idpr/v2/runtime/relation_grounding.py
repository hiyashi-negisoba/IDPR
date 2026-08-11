"""Exact-key Call 2 grounding for evaluative COMPOSE relations."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2 import relations
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.evaluate import TruthValue
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.truths import CaseTruths

_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})


class RelationGroundingError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class RelationDefinition:
    relation_ref: str
    canonical_meaning: str
    legal_standard: str
    left_type: str
    right_type: str

    def as_dict(self) -> dict[str, str]:
        return {
            "relation_ref": self.relation_ref,
            "canonical_meaning": self.canonical_meaning,
            "legal_standard": self.legal_standard,
            "left_type": self.left_type,
            "right_type": self.right_type,
        }


@dataclass(frozen=True)
class RelationAssessmentTarget:
    key: RuntimeRelationKey
    left_endpoint_ref: str
    right_endpoint_ref: str
    left_view: str
    right_view: str

    def as_dict(self) -> dict[str, Any]:
        instance = self.key.instance
        definition = self.key.definition_key
        return {
            "instance_key": {
                "case_id": instance.case_id,
                "actor_id": instance.actor_id,
                "offense_ref": instance.offense_ref,
                "occurrence_id": instance.occurrence_id,
            },
            "relation_key": {
                "occurrence_path": list(definition.occurrence_path),
                "relation_ref": definition.relation_ref,
                "left_local_key": definition.left_local_key,
                "right_local_key": definition.right_local_key,
            },
            "endpoints": {
                "left_ref": self.left_endpoint_ref,
                "right_ref": self.right_endpoint_ref,
                "left_view": self.left_view,
                "right_view": self.right_view,
            },
        }


@dataclass(frozen=True)
class RelationAssessment:
    target: RelationAssessmentTarget
    truth: TruthValue

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.target.as_dict(),
            "truth": self.truth,
        }


def relation_assessment_targets(
    registry: DefinitionRegistry, instances: Iterable[OffenseInstanceKey]
) -> tuple[RelationAssessmentTarget, ...]:
    output: list[RelationAssessmentTarget] = []
    seen: set[RuntimeRelationKey] = set()
    for instance in instances:
        compiled = compile_offense(registry, instance.offense_ref)
        if not isinstance(compiled, CompiledOffense):
            raise RelationGroundingError([f"cannot compile {instance.offense_ref!r}"])
        for definition_key, binding in relations.iter_relation_instances(compiled):
            key = RuntimeRelationKey(instance, definition_key)
            if key in seen:
                raise RelationGroundingError([f"duplicate relation target: {key!r}"])
            seen.add(key)
            output.append(
                RelationAssessmentTarget(
                    key,
                    binding.left.source_ref,
                    binding.right.source_ref,
                    binding.left_view,
                    binding.right_view,
                )
            )
    return tuple(output)


def relation_definitions(
    registry: DefinitionRegistry, refs: Iterable[str]
) -> tuple[RelationDefinition, ...]:
    output: list[RelationDefinition] = []
    for ref in dict.fromkeys(refs):
        entry = registry.get(ref)
        if entry is None or entry.kind != "relation":
            raise RelationGroundingError([f"unknown relation definition: {ref!r}"])
        payload = entry.payload
        output.append(
            RelationDefinition(
                ref,
                str(payload["canonical_meaning"]),
                str(payload["legal_standard"]),
                str(payload["left_type"]),
                str(payload["right_type"]),
            )
        )
    return tuple(output)


def shard_relation_targets_by_occurrence(
    targets: Iterable[RelationAssessmentTarget], *, max_targets: int
) -> tuple[tuple[RelationAssessmentTarget, ...], ...]:
    if max_targets <= 0:
        raise RelationGroundingError(["max_targets must be positive"])
    shards: list[tuple[RelationAssessmentTarget, ...]] = []
    current: list[RelationAssessmentTarget] = []
    current_occurrence_id: str | None = None
    for target in targets:
        occurrence_id = target.key.instance.occurrence_id
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


def relation_request_payload(
    *,
    evidence_occurrence: GoldOccurrence,
    definitions: Iterable[RelationDefinition],
    targets: Iterable[RelationAssessmentTarget],
) -> dict[str, Any]:
    target_values = tuple(targets)
    if not target_values:
        raise RelationGroundingError(["empty relation request is a host no-op"])
    refs = {value.relation_ref for value in definitions}
    errors: list[str] = []
    for target in target_values:
        instance = target.key.instance
        if (
            instance.occurrence_id != evidence_occurrence.occurrence_id
            or instance.actor_id != evidence_occurrence.actor_id
        ):
            errors.append("relation target differs from evidence occurrence identity")
        if target.key.definition_key.relation_ref not in refs:
            errors.append("relation target has no supplied definition")
    if errors:
        raise RelationGroundingError(errors)
    return {
        "evidence_occurrence": evidence_occurrence.as_dict(),
        "relation_catalog": [value.as_dict() for value in definitions],
        "relation_targets": [value.as_dict() for value in target_values],
    }


def relation_schema(targets: Iterable[RelationAssessmentTarget]) -> dict[str, Any]:
    count = len(tuple(targets))
    if count == 0:
        raise RelationGroundingError(["empty relation target set has no schema"])
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["truths"],
        "properties": {
            "truths": {
                "type": "array",
                "minItems": count,
                "maxItems": count,
                "items": {"type": "string", "enum": sorted(_TRUTHS)},
            },
        },
    }


def validate_relation_output(
    payload: Any, *, targets: Iterable[RelationAssessmentTarget]
) -> tuple[RelationAssessment, ...]:
    expected = tuple(targets)
    if not isinstance(payload, Mapping) or set(payload) != {"truths"}:
        raise RelationGroundingError(["relation response shape mismatch"])
    truths = payload["truths"]
    if (
        not isinstance(truths, list)
        or len(truths) != len(expected)
    ):
        raise RelationGroundingError(["relation response cardinality mismatch"])
    output: list[RelationAssessment] = []
    for index, (target, truth) in enumerate(zip(expected, truths, strict=True)):
        if truth not in _TRUTHS:
            raise RelationGroundingError([f"truths[{index}] is invalid"])
        output.append(RelationAssessment(target, truth))
    return tuple(output)


def add_relation_assessments(
    base: CaseTruths, assessments: Iterable[RelationAssessment]
) -> CaseTruths:
    relation = dict(base.relation)
    for assessment in assessments:
        key = assessment.target.key
        if key in relation:
            raise RelationGroundingError([f"duplicate relation projection: {key!r}"])
        relation[key] = assessment.truth
    return CaseTruths(predicate=base.predicate, relation=relation)


__all__ = [
    "RelationAssessment",
    "RelationAssessmentTarget",
    "RelationDefinition",
    "RelationGroundingError",
    "add_relation_assessments",
    "relation_assessment_targets",
    "relation_definitions",
    "relation_request_payload",
    "relation_schema",
    "shard_relation_targets_by_occurrence",
    "validate_relation_output",
]
