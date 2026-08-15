"""Occurrence-scoped Call 2 predicate assessment and CaseTruths projection."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from idpr.v2.evaluate import TruthValue
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.question_assumptions import QuestionAssumption
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.carrier_contract import effective_evidence_scope
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
    semantic_exclusions: tuple[str, ...] = ()
    #: 폭은 carrier 계약이 소유한다. 여기 기본값을 따로 두면 그것이 두 번째 권위가 되므로,
    #: 값을 반드시 받아 적는다.
    evidence_scope: str = "offense_realization"
    temporal_anchor: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "predicate_ref": self.predicate_ref,
            "kind": self.kind,
            "canonical_meaning": self.canonical_meaning,
            "arguments": [dict(argument) for argument in self.arguments],
        }
        if self.legal_standard is not None:
            value["legal_standard"] = self.legal_standard
        if self.semantic_exclusions:
            value["semantic_exclusions"] = list(self.semantic_exclusions)
        value["evidence_scope"] = self.evidence_scope
        if self.temporal_anchor is not None:
            value["temporal_anchor"] = self.temporal_anchor
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
        exclusions = tuple(
            str(value) for value in entry.payload.get("semantic_exclusions", ())
        )
        # 미저작 predicate의 폭은 carrier 계약이 정한다. 여기서 옛 기본값을 따로 들고 있으면
        # 모델이 받는 지시와 실제로 받는 증거의 폭이 갈라진다.
        evidence_scope = effective_evidence_scope(registry, ref)
        temporal_anchor = entry.payload.get("temporal_anchor")
        values.append(
            PredicateDefinition(
                predicate_ref=ref,
                kind=entry.kind,
                canonical_meaning=meaning,
                arguments=tuple(dict(argument) for argument in arguments),
                legal_standard=standard if isinstance(standard, str) else None,
                semantic_exclusions=exclusions,
                evidence_scope=evidence_scope,
                temporal_anchor=(
                    temporal_anchor if isinstance(temporal_anchor, str) else None
                ),
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


def _ground_fact_carrier_id(
    target: AssessmentTarget,
    *,
    episode_by_occurrence: Mapping[str, str],
    carrier_by_target: Mapping[AssessmentTarget, str] | None,
) -> str:
    """Return the authored evidence carrier used to canonicalize one GroundFact.

    ``carrier_by_target`` is the realization/action-aware path.  It is deliberately
    keyed by the *logical* target rather than just occurrence identity: two predicates
    on one legal realization can legitimately have different factual carriers.  Once a
    caller opts into this path, silently falling back to the factual episode for a
    missing target would recreate the cross-action contamination this boundary exists
    to prevent, so every GroundFact target must be assigned a non-empty carrier.

    Without the map, retain the frozen episode-level behavior for historical planner
    and Call 2 artifacts.
    """
    if carrier_by_target is not None:
        carrier_id = carrier_by_target.get(target)
        if not isinstance(carrier_id, str) or not carrier_id:
            raise GroundingContractError(
                [
                    (
                        "carrier_by_target must assign every GroundFact target a non-empty "
                        f"carrier id: {target.as_dict()}"
                    )
                ]
            )
        return carrier_id
    return episode_by_occurrence.get(
        target.instance_key.occurrence_id, target.instance_key.occurrence_id
    )


def grounding_request_targets(
    registry: DefinitionRegistry,
    targets: Iterable[AssessmentTarget],
    *,
    episode_by_occurrence: Mapping[str, str] | None = None,
    carrier_by_target: Mapping[AssessmentTarget, str] | None = None,
) -> tuple[AssessmentTarget, ...]:
    """Deduplicate GroundFact questions at their authored factual carrier.

    With ``carrier_by_target``, a carrier is an action or legal-realization scope
    selected upstream for this exact target.  Thus a GroundFact is shared only when
    its case, actor, predicate, and carrier all match.  This permits direct and
    derived consumers of one realization to share one answer while keeping two
    distinct actions inside a broad factual episode separate.

    If no carrier map is supplied, canonicalize at factual-episode identity exactly
    as earlier artifacts did.  LegalElements remain offense-instance local.  The
    first GroundFact target is retained only as an internal projection anchor; its
    offense id is not exposed in the neural payload.
    """
    episodes = episode_by_occurrence or {}
    output: list[AssessmentTarget] = []
    seen_ground: set[tuple[str, str, str, str]] = set()
    seen_targets: set[AssessmentTarget] = set()
    for target in targets:
        if target in seen_targets:
            raise GroundingContractError(["assessment targets contain duplicates"])
        seen_targets.add(target)
        kind = registry.kind_of(target.predicate_ref)
        if kind == "ground_fact":
            instance = target.instance_key
            key = (
                instance.case_id,
                instance.actor_id,
                _ground_fact_carrier_id(
                    target,
                    episode_by_occurrence=episodes,
                    carrier_by_target=carrier_by_target,
                ),
                target.predicate_ref,
            )
            if key in seen_ground:
                continue
            seen_ground.add(key)
        elif kind != "legal_element":
            raise GroundingContractError(
                [f"invalid assessment predicate kind: {target.predicate_ref!r}"]
            )
        output.append(target)
    return tuple(output)


def expand_ground_fact_assessments(
    registry: DefinitionRegistry,
    assessments: Iterable[PredicateAssessment],
    *,
    expected_targets: Iterable[AssessmentTarget],
    episode_by_occurrence: Mapping[str, str] | None = None,
    carrier_by_target: Mapping[AssessmentTarget, str] | None = None,
) -> tuple[PredicateAssessment, ...]:
    """Project each carrier-level GroundFact answer to all consuming offense instances.

    The optional carrier map must be the same assignment used to make the physical
    requests.  Otherwise the legacy factual-episode projection is preserved.
    """
    episodes = episode_by_occurrence or {}
    expected = tuple(expected_targets)
    request_targets = grounding_request_targets(
        registry,
        expected,
        episode_by_occurrence=episodes,
        carrier_by_target=carrier_by_target,
    )
    values = tuple(assessments)
    if tuple(value.target for value in values) != request_targets:
        raise GroundingContractError(
            ["request assessments do not exactly cover deduplicated grounding targets"]
        )
    direct = {value.target: value.truth for value in values}
    shared: dict[tuple[str, str, str, str], TruthValue] = {}
    for value in values:
        if registry.kind_of(value.target.predicate_ref) != "ground_fact":
            continue
        instance = value.target.instance_key
        shared[
            (
                instance.case_id,
                instance.actor_id,
                _ground_fact_carrier_id(
                    value.target,
                    episode_by_occurrence=episodes,
                    carrier_by_target=carrier_by_target,
                ),
                value.target.predicate_ref,
            )
        ] = value.truth
    output: list[PredicateAssessment] = []
    for target in expected:
        if registry.kind_of(target.predicate_ref) == "ground_fact":
            instance = target.instance_key
            key = (
                instance.case_id,
                instance.actor_id,
                _ground_fact_carrier_id(
                    target,
                    episode_by_occurrence=episodes,
                    carrier_by_target=carrier_by_target,
                ),
                target.predicate_ref,
            )
            output.append(PredicateAssessment(target, shared[key]))
        else:
            output.append(PredicateAssessment(target, direct[target]))
    return tuple(output)


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
    targets: Iterable[AssessmentTarget],
    *,
    max_targets: int,
    carrier_by_target: Mapping[AssessmentTarget, str] | None = None,
) -> tuple[tuple[AssessmentTarget, ...], ...]:
    """Preserve target order while making every physical request carrier-homogeneous.

    Legacy callers shard by logical occurrence.  The action-realization planner
    supplies a target carrier map, allowing a focal-action GroundFact and a
    realization-level LegalElement for one logical occurrence to travel in
    separate requests without changing their symbolic identity.
    """
    if max_targets <= 0:
        raise GroundingContractError(["max_targets must be positive"])
    shards: list[tuple[AssessmentTarget, ...]] = []
    current: list[AssessmentTarget] = []
    current_carrier_id: str | None = None
    for target in targets:
        carrier_id = (
            carrier_by_target.get(target)
            if carrier_by_target is not None
            else target.instance_key.occurrence_id
        )
        if not isinstance(carrier_id, str) or not carrier_id:
            raise GroundingContractError(
                [f"target is missing a physical evidence carrier: {target.as_dict()}"]
            )
        if current and (
            carrier_id != current_carrier_id or len(current) == max_targets
        ):
            shards.append(tuple(current))
            current = []
        if not current:
            current_carrier_id = carrier_id
        current.append(target)
    if current:
        shards.append(tuple(current))
    return tuple(shards)


def call2_request_payload(
    *,
    evidence_occurrence: GoldOccurrence,
    question_assumptions: Iterable[QuestionAssumption] = (),
    predicates: Iterable[PredicateDefinition],
    targets: Iterable[AssessmentTarget],
    carrier_id: str | None = None,
    realization_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one shard whose only factual evidence is one gold occurrence span."""
    predicate_values = tuple(predicates)
    predicate_by_ref = {value.predicate_ref: value for value in predicate_values}
    predicate_refs = set(predicate_by_ref)
    target_values = tuple(targets)
    if not target_values:
        raise GroundingContractError(["an empty target set is a host no-op"])
    errors: list[str] = []
    expected_carrier_id = carrier_id or evidence_occurrence.occurrence_id
    if evidence_occurrence.occurrence_id != expected_carrier_id:
        errors.append(
            "request evidence occurrence differs from explicit carrier id: "
            f"{evidence_occurrence.occurrence_id!r} != {expected_carrier_id!r}"
        )
    for target in target_values:
        if carrier_id is None and target.instance_key.occurrence_id != evidence_occurrence.occurrence_id:
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
    payload = {
        "evidence_occurrence": evidence_occurrence.as_dict(),
        "question_assumptions": [value.as_dict() for value in question_assumptions],
        "predicate_catalog": [value.as_dict() for value in predicate_values],
        "assessment_targets": [
            (
                {
                    "occurrence_key": {
                        "case_id": target.instance_key.case_id,
                        "actor_id": target.instance_key.actor_id,
                        "occurrence_id": target.instance_key.occurrence_id,
                    },
                    "predicate_ref": target.predicate_ref,
                }
                if predicate_by_ref[target.predicate_ref].kind == "ground_fact"
                else target.as_dict()
            )
            for target in target_values
        ],
    }
    if realization_context is not None:
        target_actors = {target.instance_key.actor_id for target in target_values}
        if target_actors != {str(realization_context.get("target_actor_id"))}:
            raise GroundingContractError(
                ["realization context actor differs from request target actor"]
            )
        payload["realization_context"] = dict(realization_context)
    return payload


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
    "expand_ground_fact_assessments",
    "grounding_request_targets",
    "instance_key_dict",
    "predicate_definitions",
    "shard_assessment_targets",
    "shard_assessment_targets_by_occurrence",
    "validate_call2_output",
]
