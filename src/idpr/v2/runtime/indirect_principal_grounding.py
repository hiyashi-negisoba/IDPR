"""Factual action-direction grounding for indirect-principal candidates.

The neural proposition here is deliberately offense-free: did one reviewed actor occurrence
direct, cause, or procure the source-local participant's described action?  Exact-offense legal
capability is used only to decide whether this sparse factual relation is worth requesting.  A
positive relation remains just a fact and cannot itself establish an indirect principal.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.evaluate import TruthValue
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.indirect_principal import has_authored_indirect_principal_capability
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import (
    FactualActionKey,
    FactualParticipantKey,
    OffenseInstanceKey,
)
from idpr.v2.runtime.stages import UtilizedParticipantOutcome

_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})


class IndirectPrincipalGroundingError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class FactualUtilizationTarget:
    utilizer_action: FactualActionKey
    utilized_participant: FactualParticipantKey

    @property
    def case_id(self) -> str:
        return self.utilizer_action.case_id

    def as_dict(self) -> dict[str, Any]:
        return {
            "relation_kind": "factual_action_direction",
            "utilizer_action": {
                "case_id": self.utilizer_action.case_id,
                "actor_id": self.utilizer_action.actor_id,
                "occurrence_id": self.utilizer_action.occurrence_id,
            },
            "utilized_participant": {
                "case_id": self.utilized_participant.case_id,
                "participant_id": self.utilized_participant.participant_id,
            },
        }


@dataclass(frozen=True)
class FactualUtilizationAssessment:
    target: FactualUtilizationTarget
    truth: TruthValue

    def as_dict(self) -> dict[str, Any]:
        return {**self.target.as_dict(), "truth": self.truth}


@dataclass(frozen=True)
class IndirectPrincipalDependency:
    """Exact-offense host projection of relation truth plus participant outcome."""

    utilizer_instance: OffenseInstanceKey
    utilized_participant: FactualParticipantKey
    relation_truth: TruthValue
    utilized_outcome: UtilizedParticipantOutcome
    truth: TruthValue
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "utilizer_instance": {
                "case_id": self.utilizer_instance.case_id,
                "actor_id": self.utilizer_instance.actor_id,
                "offense_ref": self.utilizer_instance.offense_ref,
                "occurrence_id": self.utilizer_instance.occurrence_id,
            },
            "utilized_participant": {
                "case_id": self.utilized_participant.case_id,
                "participant_id": self.utilized_participant.participant_id,
            },
            "relation_truth": self.relation_truth,
            "utilized_outcome_status": self.utilized_outcome.status,
            "dependency_truth": self.truth,
            "reason": self.reason,
        }


def factual_utilization_targets(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
    participants: Iterable[GoldFactualParticipant],
) -> tuple[FactualUtilizationTarget, ...]:
    """Create sparse offense-free relation targets behind an explicit capability gate."""

    instance_values = tuple(instances)
    participant_values = tuple(participants)
    if len(instance_values) != len(set(instance_values)):
        raise IndirectPrincipalGroundingError(["utilization instances contain duplicates"])
    if len({value.participant_id for value in participant_values}) != len(participant_values):
        raise IndirectPrincipalGroundingError(["factual participants contain duplicate ids"])
    if not instance_values or not participant_values:
        return ()
    case_ids = {value.case_id for value in instance_values}
    # GoldFactualParticipant intentionally has no case id; the caller supplies the case-local set.
    if len(case_ids) != 1:
        raise IndirectPrincipalGroundingError(["utilization instances span multiple cases"])
    case_id = next(iter(case_ids))
    eligible_actions = tuple(
        dict.fromkeys(
            FactualActionKey(value.case_id, value.actor_id, value.occurrence_id)
            for value in instance_values
            if has_authored_indirect_principal_capability(registry, value.offense_ref)
        )
    )
    output = tuple(
        FactualUtilizationTarget(
            action,
            FactualParticipantKey(case_id, participant.participant_id),
        )
        for action in eligible_actions
        for participant in participant_values
    )
    if len(output) != len(set(output)):
        raise IndirectPrincipalGroundingError(["duplicate factual utilization target"])
    return output


def factual_utilization_request_payload(
    *,
    occurrences: Iterable[GoldOccurrence],
    participants: Iterable[GoldFactualParticipant],
    targets: Iterable[FactualUtilizationTarget],
) -> dict[str, Any]:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise IndirectPrincipalGroundingError(
            ["one utilization request must contain exactly one factual relation"]
        )
    target = target_values[0]
    occurrence_matches = [
        value
        for value in occurrences
        if value.occurrence_id == target.utilizer_action.occurrence_id
    ]
    participant_matches = [
        value
        for value in participants
        if value.participant_id == target.utilized_participant.participant_id
    ]
    errors: list[str] = []
    if len(occurrence_matches) != 1:
        errors.append("utilizer occurrence must resolve exactly once")
    elif (
        target.utilizer_action.case_id != target.case_id
        or occurrence_matches[0].actor_id != target.utilizer_action.actor_id
    ):
        errors.append("utilizer action differs from reviewed occurrence identity")
    if len(participant_matches) != 1:
        errors.append("utilized participant must resolve exactly once")
    if target.utilized_participant.case_id != target.case_id:
        errors.append("utilization endpoints differ in case identity")
    if errors:
        raise IndirectPrincipalGroundingError(errors)
    return {
        "utilizer_occurrence_evidence": occurrence_matches[0].as_dict(),
        "utilized_participant_evidence": participant_matches[0].as_dict(),
        "factual_relation_target": target.as_dict(),
        "relation_contract": {
            "direction": "utilizer_action_to_utilized_participant_action",
            "predicate": (
                "the utilizer actor intentionally directed, caused, or procured the utilized "
                "participant to perform the participant action described by the evidence"
            ),
            "legal_effect": "none",
        },
    }


def factual_utilization_schema(target: FactualUtilizationTarget) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["relation_assessment"],
        "properties": {
            "relation_assessment": {
                "type": "object",
                "additionalProperties": False,
                "required": ["relation_kind", "truth"],
                "properties": {
                    "relation_kind": {"const": "factual_action_direction"},
                    "truth": {"type": "string", "enum": sorted(_TRUTHS)},
                },
            }
        },
    }


def validate_factual_utilization_output(
    payload: Any,
    *,
    target: FactualUtilizationTarget,
) -> FactualUtilizationAssessment:
    if not isinstance(payload, Mapping) or set(payload) != {"relation_assessment"}:
        raise IndirectPrincipalGroundingError(
            ["response must contain exactly relation_assessment"]
        )
    raw = payload["relation_assessment"]
    if (
        not isinstance(raw, Mapping)
        or set(raw) != {"relation_kind", "truth"}
        or raw.get("relation_kind") != "factual_action_direction"
        or raw.get("truth") not in _TRUTHS
    ):
        raise IndirectPrincipalGroundingError(["invalid factual utilization assessment"])
    return FactualUtilizationAssessment(target, raw["truth"])


def _dependency_truth(
    relation_truth: TruthValue,
    outcome: UtilizedParticipantOutcome,
) -> tuple[TruthValue, str]:
    if relation_truth == "UNKNOWN":
        return "UNKNOWN", "factual_utilization_unresolved"
    if relation_truth != "TRUE":
        raise IndirectPrincipalGroundingError(
            ["FALSE factual utilization does not create a dependency"]
        )
    if outcome.status in {
        "elements_failure",
        "unlawfulness_defeat",
        "culpability_defeat",
        "punishability_defeat",
        "different_negligence_offense",
    }:
        return "TRUE", outcome.status
    if outcome.status == "liable_exact_offense":
        return "FALSE", outcome.status
    return "UNKNOWN", "utilized_participant_outcome_unresolved"


def compile_indirect_principal_dependencies(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
    participants: Iterable[GoldFactualParticipant],
    assessments: Iterable[FactualUtilizationAssessment],
    outcomes: Iterable[UtilizedParticipantOutcome],
    *,
    expected_targets: Iterable[FactualUtilizationTarget] | None = None,
) -> tuple[IndirectPrincipalDependency, ...]:
    """Project factual direction into exact-offense dependencies without repair."""

    instance_values = tuple(instances)
    participant_values = tuple(participants)
    if expected_targets is None:
        target_values = factual_utilization_targets(
            registry, instance_values, participant_values
        )
    else:
        target_values = tuple(expected_targets)
        if len(target_values) != len(set(target_values)):
            raise IndirectPrincipalGroundingError(["expected utilization targets duplicate"])
        case_ids = {value.case_id for value in instance_values}
        participant_keys = (
            {
                FactualParticipantKey(next(iter(case_ids)), participant.participant_id)
                for participant in participant_values
            }
            if len(case_ids) == 1
            else set()
        )
        eligible_actions = {
            FactualActionKey(value.case_id, value.actor_id, value.occurrence_id)
            for value in instance_values
            if has_authored_indirect_principal_capability(registry, value.offense_ref)
        }
        if any(
            value.utilizer_action not in eligible_actions
            or value.utilized_participant not in participant_keys
            for value in target_values
        ):
            raise IndirectPrincipalGroundingError(
                ["expected utilization target is outside eligible evidence endpoints"]
            )
    assessment_values = tuple(assessments)
    errors: list[str] = []
    if tuple(value.target for value in assessment_values) != target_values:
        errors.append("utilization assessments do not exactly equal expected targets")
    if len({value.target for value in assessment_values}) != len(assessment_values):
        errors.append("duplicate factual utilization assessment")
    outcome_values = tuple(outcomes)
    outcome_by_key = {
        (value.participant, value.offense_ref): value for value in outcome_values
    }
    if len(outcome_by_key) != len(outcome_values):
        errors.append("duplicate utilized participant outcome")
    participant_keys = (
        {
            FactualParticipantKey(target_values[0].case_id, value.participant_id)
            for value in participant_values
        }
        if target_values
        else set()
    )
    for outcome in outcome_values:
        if outcome.participant not in participant_keys:
            errors.append("utilized outcome has an unknown participant endpoint")
        if not has_authored_indirect_principal_capability(
            registry, outcome.offense_ref
        ):
            errors.append("utilized outcome offense lacks authored capability")
    if errors:
        raise IndirectPrincipalGroundingError(errors)

    instances_by_action: dict[FactualActionKey, list[OffenseInstanceKey]] = {}
    for instance in instance_values:
        if not has_authored_indirect_principal_capability(
            registry, instance.offense_ref
        ):
            continue
        action = FactualActionKey(
            instance.case_id, instance.actor_id, instance.occurrence_id
        )
        instances_by_action.setdefault(action, []).append(instance)

    output: list[IndirectPrincipalDependency] = []
    for assessment in assessment_values:
        if assessment.truth == "FALSE":
            continue
        for instance in instances_by_action.get(
            assessment.target.utilizer_action, ()
        ):
            outcome = outcome_by_key.get(
                (assessment.target.utilized_participant, instance.offense_ref)
            )
            if outcome is None:
                errors.append(
                    "missing utilized outcome for positive/unresolved relation: "
                    f"{assessment.target.utilized_participant}/{instance.offense_ref}"
                )
                continue
            truth, reason = _dependency_truth(assessment.truth, outcome)
            output.append(
                IndirectPrincipalDependency(
                    instance,
                    assessment.target.utilized_participant,
                    assessment.truth,
                    outcome,
                    truth,
                    reason,
                )
            )
    if errors:
        raise IndirectPrincipalGroundingError(errors)
    if len(output) != len(set(output)):
        raise IndirectPrincipalGroundingError(
            ["duplicate indirect-principal dependency"]
        )
    return tuple(output)


__all__ = [
    "FactualUtilizationAssessment",
    "FactualUtilizationTarget",
    "IndirectPrincipalDependency",
    "IndirectPrincipalGroundingError",
    "compile_indirect_principal_dependencies",
    "factual_utilization_request_payload",
    "factual_utilization_schema",
    "factual_utilization_targets",
    "validate_factual_utilization_output",
]
