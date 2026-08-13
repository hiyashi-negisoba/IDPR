"""Predicate-level internal outcomes for source-local utilized participants.

This module deliberately does not construct ``OffenseInstanceKey`` or ``LiabilityEvaluation``.
A factual participant is not an answer-facing actor.  The only exported legal value is the narrow
``UtilizedParticipantOutcome`` consumed by the Article 34 host dependency compiler.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2 import expressions
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue, evaluate, fold_all
from idpr.v2.gold_factual_identity import GoldFactualParticipant
from idpr.v2.indirect_principal import has_authored_indirect_principal_capability
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.relations import RelationInstanceKey, iter_relation_instances
from idpr.v2.runtime import completion as completion_mod
from idpr.v2.runtime.effects import ActiveDoctrineRefs, resolve_stage_from_predicate_view
from idpr.v2.runtime.grounding import predicate_definitions
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey
from idpr.v2.runtime.stages import UtilizedParticipantOutcome

_TRUTHS = frozenset({TRUE, FALSE, UNKNOWN})


class UtilizedParticipantOutcomeError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class UtilizedParticipantOutcomeTarget:
    """One source-local participant evaluated against one exact capable offense."""

    participant: FactualParticipantKey
    offense_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "participant": {
                "case_id": self.participant.case_id,
                "participant_id": self.participant.participant_id,
            },
            "offense_ref": self.offense_ref,
        }


@dataclass(frozen=True)
class UtilizedParticipantPredicateTarget:
    outcome_target: UtilizedParticipantOutcomeTarget
    predicate_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {**self.outcome_target.as_dict(), "predicate_ref": self.predicate_ref}


@dataclass(frozen=True)
class UtilizedParticipantPredicateAssessment:
    target: UtilizedParticipantPredicateTarget
    truth: TruthValue

    def as_dict(self) -> dict[str, Any]:
        return {**self.target.as_dict(), "truth": self.truth}


def utilized_participant_outcome_targets(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
    participants: Iterable[GoldFactualParticipant],
) -> tuple[UtilizedParticipantOutcomeTarget, ...]:
    """Create the sparse participant x exact-capable-offense outcome universe."""

    instance_values = tuple(instances)
    participant_values = tuple(participants)
    errors: list[str] = []
    if len(instance_values) != len(set(instance_values)):
        errors.append("outcome instances contain duplicates")
    if len({value.participant_id for value in participant_values}) != len(participant_values):
        errors.append("factual participants contain duplicate ids")
    case_ids = {value.case_id for value in instance_values}
    if len(case_ids) > 1:
        errors.append("outcome instances span multiple cases")
    if errors:
        raise UtilizedParticipantOutcomeError(errors)
    if not instance_values or not participant_values:
        return ()

    case_id = next(iter(case_ids))
    offense_refs = tuple(
        dict.fromkeys(
            value.offense_ref
            for value in instance_values
            if has_authored_indirect_principal_capability(registry, value.offense_ref)
        )
    )
    return tuple(
        UtilizedParticipantOutcomeTarget(
            FactualParticipantKey(case_id, participant.participant_id),
            offense_ref,
        )
        for participant in participant_values
        for offense_ref in offense_refs
    )


def _compiled_target(
    registry: DefinitionRegistry,
    target: UtilizedParticipantOutcomeTarget,
) -> CompiledOffense:
    if not has_authored_indirect_principal_capability(registry, target.offense_ref):
        raise UtilizedParticipantOutcomeError(
            [f"outcome offense lacks authored capability: {target.offense_ref!r}"]
        )
    compiled = compile_offense(registry, target.offense_ref)
    if not isinstance(compiled, CompiledOffense):
        raise UtilizedParticipantOutcomeError(
            [f"outcome offense does not compile: {target.offense_ref!r}"]
        )
    if completion_mod.completion_policy_for(registry, target.offense_ref) is not None:
        raise UtilizedParticipantOutcomeError(
            [
                (
                    "completion-bearing utilized offense needs a dedicated participant "
                    f"completion contract: {target.offense_ref!r}"
                )
            ]
        )
    return compiled


def utilized_participant_predicate_targets(
    registry: DefinitionRegistry,
    outcome_targets: Iterable[UtilizedParticipantOutcomeTarget],
    *,
    active_doctrines_by_target: Mapping[
        UtilizedParticipantOutcomeTarget, ActiveDoctrineRefs
    ] | None = None,
) -> tuple[UtilizedParticipantPredicateTarget, ...]:
    """Select only predicates actually consumed by exact Elements or active doctrines."""

    target_values = tuple(outcome_targets)
    active_doctrines_by_target = active_doctrines_by_target or {}
    if len(target_values) != len(set(target_values)):
        raise UtilizedParticipantOutcomeError(["duplicate utilized outcome target"])
    output: list[UtilizedParticipantPredicateTarget] = []
    for target in target_values:
        compiled = _compiled_target(registry, target)
        refs: set[str] = set()
        for slot in expressions.SLOT_NAMES:
            refs.update(expressions.canonical_leaf_refs(compiled.slots[slot]))
        for doctrine_ref in active_doctrines_by_target.get(target, frozenset()):
            entry = registry.get(doctrine_ref)
            if entry is None or entry.kind != "doctrine":
                raise UtilizedParticipantOutcomeError(
                    [f"active utilized doctrine is invalid: {doctrine_ref!r}"]
                )
            refs.update(expressions.leaf_refs(entry.payload["requires"]))
        output.extend(
            UtilizedParticipantPredicateTarget(target, ref) for ref in sorted(refs)
        )
    return tuple(output)


def utilized_participant_request_payload(
    registry: DefinitionRegistry,
    *,
    participant: GoldFactualParticipant,
    outcome_target: UtilizedParticipantOutcomeTarget,
    predicate_targets: Iterable[UtilizedParticipantPredicateTarget],
    active_doctrine_refs: ActiveDoctrineRefs = frozenset(),
) -> dict[str, Any]:
    """Build one exact-offense predicate request with no liability conclusion field."""

    target_values = tuple(predicate_targets)
    expected = utilized_participant_predicate_targets(
        registry,
        (outcome_target,),
        active_doctrines_by_target={outcome_target: active_doctrine_refs},
    )
    if target_values != expected:
        raise UtilizedParticipantOutcomeError(
            ["participant predicate request does not exactly equal expected target frontier"]
        )
    if participant.participant_id != outcome_target.participant.participant_id:
        raise UtilizedParticipantOutcomeError(
            ["participant evidence differs from outcome target identity"]
        )
    definitions = predicate_definitions(
        registry, (value.predicate_ref for value in target_values)
    )
    return {
        "utilized_participant_evidence": participant.as_dict(),
        "exact_offense_ref": outcome_target.offense_ref,
        "predicate_definitions": [value.as_dict() for value in definitions],
        "assessment_targets": [value.as_dict() for value in target_values],
        "assessment_contract": {
            "task": "assess_each_predicate_from_participant_evidence",
            "truth_values": [TRUE, FALSE, UNKNOWN],
            "legal_effect": "none_until_host_outcome_fold",
        },
    }


def utilized_participant_schema(
    predicate_targets: Iterable[UtilizedParticipantPredicateTarget],
) -> dict[str, Any]:
    targets = tuple(predicate_targets)
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["assessments"],
        "properties": {
            "assessments": {
                "type": "array",
                "minItems": len(targets),
                "maxItems": len(targets),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["predicate_ref", "truth"],
                    "properties": {
                        "predicate_ref": {
                            "type": "string",
                            "enum": [value.predicate_ref for value in targets],
                        },
                        "truth": {"type": "string", "enum": sorted(_TRUTHS)},
                    },
                },
            }
        },
    }


def validate_utilized_participant_output(
    payload: Any,
    *,
    predicate_targets: Iterable[UtilizedParticipantPredicateTarget],
) -> tuple[UtilizedParticipantPredicateAssessment, ...]:
    targets = tuple(predicate_targets)
    if not isinstance(payload, Mapping) or set(payload) != {"assessments"}:
        raise UtilizedParticipantOutcomeError(["response must contain exactly assessments"])
    raw_values = payload["assessments"]
    if not isinstance(raw_values, list):
        raise UtilizedParticipantOutcomeError(["assessments must be an array"])
    by_ref: dict[str, TruthValue] = {}
    for raw in raw_values:
        if (
            not isinstance(raw, Mapping)
            or set(raw) != {"predicate_ref", "truth"}
            or raw.get("truth") not in _TRUTHS
            or not isinstance(raw.get("predicate_ref"), str)
        ):
            raise UtilizedParticipantOutcomeError(["invalid participant predicate assessment"])
        ref = raw["predicate_ref"]
        if ref in by_ref:
            raise UtilizedParticipantOutcomeError(
                [f"duplicate participant predicate assessment: {ref!r}"]
            )
        by_ref[ref] = raw["truth"]
    expected_refs = tuple(value.predicate_ref for value in targets)
    if set(by_ref) != set(expected_refs) or len(by_ref) != len(expected_refs):
        raise UtilizedParticipantOutcomeError(
            ["participant predicate assessments do not exactly equal expected targets"]
        )
    return tuple(
        UtilizedParticipantPredicateAssessment(target, by_ref[target.predicate_ref])
        for target in targets
    )


def produce_utilized_participant_outcomes(
    registry: DefinitionRegistry,
    outcome_targets: Iterable[UtilizedParticipantOutcomeTarget],
    assessments: Iterable[UtilizedParticipantPredicateAssessment],
    *,
    relation_truths: Mapping[
        tuple[UtilizedParticipantOutcomeTarget, RelationInstanceKey], TruthValue
    ] | None = None,
    active_doctrines_by_target: Mapping[
        UtilizedParticipantOutcomeTarget, ActiveDoctrineRefs
    ] | None = None,
    different_negligence_truths: Mapping[
        UtilizedParticipantOutcomeTarget, TruthValue
    ] | None = None,
) -> tuple[UtilizedParticipantOutcome, ...]:
    """Fold exact predicate truths into internal outcomes without creating liable actors."""

    targets = tuple(outcome_targets)
    relation_truths = relation_truths or {}
    active_doctrines_by_target = active_doctrines_by_target or {}
    different_negligence_truths = different_negligence_truths or {}
    target_set = set(targets)
    errors: list[str] = []
    if set(active_doctrines_by_target) - target_set:
        errors.append("active doctrine map contains an unknown outcome target")
    if set(different_negligence_truths) - target_set:
        errors.append("different-negligence map contains an unknown outcome target")
    compiled_relation_keys: dict[
        UtilizedParticipantOutcomeTarget, set[RelationInstanceKey]
    ] = {}
    for target in targets:
        compiled_relation_keys[target] = {
            key for key, _binding in iter_relation_instances(_compiled_target(registry, target))
        }
    for (target, relation_key), truth in relation_truths.items():
        if target not in target_set or relation_key not in compiled_relation_keys.get(target, set()):
            errors.append("relation truth contains an unknown participant/offense relation key")
        if truth not in _TRUTHS:
            errors.append("invalid utilized participant relation truth")
    if errors:
        raise UtilizedParticipantOutcomeError(errors)
    expected_predicates = utilized_participant_predicate_targets(
        registry,
        targets,
        active_doctrines_by_target=active_doctrines_by_target,
    )
    values = tuple(assessments)
    if tuple(value.target for value in values) != expected_predicates:
        raise UtilizedParticipantOutcomeError(
            ["participant assessments do not exactly equal expected predicate targets"]
        )
    if len({value.target for value in values}) != len(values):
        raise UtilizedParticipantOutcomeError(["duplicate participant predicate assessment"])
    truth_by_target = {value.target: value.truth for value in values}
    output: list[UtilizedParticipantOutcome] = []
    for target in targets:
        compiled = _compiled_target(registry, target)
        predicate_view = {
            value.predicate_ref: truth_by_target[value]
            for value in expected_predicates
            if value.outcome_target == target
        }
        negligence_truth = different_negligence_truths.get(target, FALSE)
        if negligence_truth not in _TRUTHS:
            raise UtilizedParticipantOutcomeError(["invalid different-negligence truth"])
        if negligence_truth == TRUE:
            status = "different_negligence_offense"
        elif negligence_truth == UNKNOWN:
            status = "unresolved"
        else:
            relation_values = [
                relation_truths.get((target, key), UNKNOWN)
                for key, _binding in iter_relation_instances(compiled)
            ]
            elements_truth = fold_all(
                [
                    *(evaluate(compiled.slots[slot], predicate_view) for slot in expressions.SLOT_NAMES),
                    *relation_values,
                ]
            )
            if elements_truth == FALSE:
                status = "elements_failure"
            elif elements_truth == UNKNOWN:
                status = "unresolved"
            else:
                status = "liable_exact_offense"
                for stage, defeated_status in (
                    ("unlawfulness", "unlawfulness_defeat"),
                    ("culpability", "culpability_defeat"),
                    ("punishability", "punishability_defeat"),
                ):
                    result = resolve_stage_from_predicate_view(
                        stage,
                        active_doctrines_by_target.get(target, frozenset()),
                        registry,
                        predicate_view,
                    )
                    if result.gate_state == "fails":
                        status = defeated_status
                        break
                    if result.gate_state == "unresolved":
                        status = "unresolved"
                        break
        output.append(UtilizedParticipantOutcome(target.participant, target.offense_ref, status))
    return tuple(output)


__all__ = [
    "UtilizedParticipantOutcomeError",
    "UtilizedParticipantOutcomeTarget",
    "UtilizedParticipantPredicateAssessment",
    "UtilizedParticipantPredicateTarget",
    "produce_utilized_participant_outcomes",
    "utilized_participant_outcome_targets",
    "utilized_participant_predicate_targets",
    "utilized_participant_request_payload",
    "utilized_participant_schema",
    "validate_utilized_participant_output",
]
