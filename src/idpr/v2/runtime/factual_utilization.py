"""Evidence-scoped indirect-principal candidates from Call 1.5-P interactions.

This producer performs no Article 34 or offense-elements judgment.  It only joins an
explicit request/instruction to an authored-capable binding of the requesting actor
in the same factual episode and carries the addressed participant's episode evidence.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from idpr.v2.factual_interaction import FactualInteraction
from idpr.v2.gold_factual_identity import GoldFactualParticipant
from idpr.v2.indirect_principal import has_authored_indirect_principal_capability
from idpr.v2.issue_binding import IssueBindingResult
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import FactualActionKey, FactualParticipantKey, OffenseInstanceKey
from idpr.v2.runtime.indirect_principal_grounding import FactualUtilizationTarget
from idpr.v2.runtime.utilized_participant_outcome import (
    UtilizedParticipantOutcomeTarget,
    UtilizedParticipantPredicateTarget,
    utilized_participant_predicate_targets,
)


class FactualUtilizationPlanError(ValueError):
    pass


@dataclass(frozen=True)
class FactualUtilizationPlan:
    participants: tuple[GoldFactualParticipant, ...]
    targets: tuple[FactualUtilizationTarget, ...]
    outcome_targets: tuple[UtilizedParticipantOutcomeTarget, ...]
    predicate_targets: tuple[UtilizedParticipantPredicateTarget, ...]
    used_interaction_ids: tuple[str, ...]


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _participant_id(interaction_id: str, actor_id: str) -> str:
    digest = hashlib.sha256(f"{interaction_id}\0{actor_id}".encode()).hexdigest()[:12]
    return f"fparticipant:{digest}"


def materialize_factual_utilization_candidates(
    *,
    case_id: str,
    plan_row: Mapping[str, Any],
    binding_result: IssueBindingResult,
    interactions: Iterable[FactualInteraction],
    registry: DefinitionRegistry,
) -> FactualUtilizationPlan:
    """Materialize only explicit, same-episode action-direction probes."""

    if plan_row.get("factual_utilization_targets") or plan_row.get(
        "utilized_participant_outcome_targets"
    ):
        raise FactualUtilizationPlanError("utilization plan is already populated")
    episode_by_occurrence = {
        value.binding_id: value.factual_episode_id for value in binding_result.bindings
    }
    for value in plan_row.get("derived_binding_candidates", []):
        episode_by_occurrence[str(value["binding_id"])] = str(value["factual_episode_id"])
    episode_by_id = {
        value.factual_episode_id: value for value in binding_result.factual_episodes
    }
    instances = tuple(_instance(value) for value in plan_row["top_level_instances"])
    if any(value.case_id != case_id for value in instances):
        raise FactualUtilizationPlanError("top-level instance crossed a case boundary")

    binding_by_id = {value.binding_id: value for value in binding_result.bindings}
    capable_by_episode_actor: dict[tuple[str, str], list[OffenseInstanceKey]] = {}
    for instance in instances:
        episode_id = episode_by_occurrence.get(instance.occurrence_id)
        if episode_id is None:
            raise FactualUtilizationPlanError("top-level instance has no episode lineage")
        if has_authored_indirect_principal_capability(registry, instance.offense_ref):
            capable_by_episode_actor.setdefault((episode_id, instance.actor_id), []).append(
                instance
            )

    participants: dict[str, GoldFactualParticipant] = {}
    targets: list[FactualUtilizationTarget] = []
    outcomes: list[UtilizedParticipantOutcomeTarget] = []
    used: list[str] = []
    for interaction in interactions:
        if interaction.interaction_type != "request_or_instruction":
            continue
        capable = capable_by_episode_actor.get(
            (interaction.factual_episode_id, interaction.source_actor_id), ()
        )
        capable = tuple(
            instance
            for instance in capable
            if instance.occurrence_id in binding_by_id
            and any(
                evidence.source_start < fragment.source_end
                and fragment.source_start < evidence.source_end
                for evidence in interaction.evidence
                for fragment in binding_by_id[
                    instance.occurrence_id
                ].actor_action_fragments
            )
        )
        if not capable:
            continue
        episode = episode_by_id[interaction.factual_episode_id]
        if len(episode.source_fragments) != 1:
            # A participant outcome request needs one exact, contiguous evidence carrier.
            # Non-contiguous episodes remain explicitly unrepresented.
            continue
        fragment = episode.source_fragments[0]
        for actor_id in interaction.target_actor_ids:
            if actor_id not in episode.participants:
                raise FactualUtilizationPlanError("interaction target is outside its episode")
            participant_id = _participant_id(interaction.interaction_id, actor_id)
            participant = GoldFactualParticipant(
                participant_id,
                actor_id,
                fragment.source_quote,
                fragment.source_start,
                fragment.source_end,
            )
            previous = participants.get(participant_id)
            if previous is not None and previous != participant:
                raise FactualUtilizationPlanError("factual participant identity collision")
            participants[participant_id] = participant
            participant_key = FactualParticipantKey(case_id, participant_id)
            for instance in capable:
                target = FactualUtilizationTarget(
                    FactualActionKey(case_id, instance.actor_id, instance.occurrence_id),
                    participant_key,
                )
                outcome = UtilizedParticipantOutcomeTarget(
                    participant_key, instance.offense_ref
                )
                if target not in targets:
                    targets.append(target)
                if outcome not in outcomes:
                    outcomes.append(outcome)
            if interaction.interaction_id not in used:
                used.append(interaction.interaction_id)

    predicate_targets = utilized_participant_predicate_targets(registry, outcomes)
    return FactualUtilizationPlan(
        tuple(participants.values()),
        tuple(targets),
        tuple(outcomes),
        predicate_targets,
        tuple(used),
    )


__all__ = [
    "FactualUtilizationPlan",
    "FactualUtilizationPlanError",
    "materialize_factual_utilization_candidates",
]
