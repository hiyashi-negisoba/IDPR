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
from idpr.v2.issue_binding import FactualAction, IssueBindingResult
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


def _participant_id(factual_action_id: str, actor_id: str) -> str:
    """Identify a participant by the actor's own atomic action, not the request.

    Several actors can direct the same person to perform the same action.  That
    does not create several participant facts or several predicate universes;
    the factual direction relations remain distinct through their utilizer
    realization keys.
    """

    digest = hashlib.sha256(f"{factual_action_id}\0{actor_id}".encode()).hexdigest()[:12]
    return f"fparticipant:{digest}"


def materialize_factual_utilization_candidates(
    *,
    case_id: str,
    plan_row: Mapping[str, Any],
    binding_result: IssueBindingResult,
    interactions: Iterable[FactualInteraction],
    registry: DefinitionRegistry,
) -> FactualUtilizationPlan:
    """Materialize only explicit, action-local utilization probes.

    The Call 1.5-P request must overlap the responsible utilizer's *focal*
    factual action.  The addressed participant is represented by that person's
    later atomic action in the same episode, never by the whole episode text.
    A legal realization remains the dependency identity, while its focal-action
    carrier is the physical Call 2 evidence identity.
    """

    if plan_row.get("factual_utilization_targets") or plan_row.get(
        "utilized_participant_outcome_targets"
    ):
        raise FactualUtilizationPlanError("utilization plan is already populated")
    raw_provenance = plan_row.get("instance_provenance")
    if not isinstance(raw_provenance, list):
        raise FactualUtilizationPlanError(
            "action/realization utilization requires instance_provenance"
        )
    provenance_by_instance: dict[OffenseInstanceKey, Mapping[str, Any]] = {}
    for raw in raw_provenance:
        if not isinstance(raw, Mapping) or not isinstance(raw.get("instance_key"), Mapping):
            raise FactualUtilizationPlanError("instance provenance is malformed")
        try:
            instance = _instance(raw["instance_key"])
        except (KeyError, TypeError, ValueError) as exc:
            raise FactualUtilizationPlanError("instance provenance has an invalid key") from exc
        previous = provenance_by_instance.get(instance)
        if previous is not None and previous != raw:
            raise FactualUtilizationPlanError("instance provenance duplicates an instance")
        provenance_by_instance[instance] = raw

    raw_occurrences = plan_row.get("occurrences")
    if not isinstance(raw_occurrences, list):
        raise FactualUtilizationPlanError("plan occurrences are malformed")
    occurrence_actor_by_id: dict[str, str] = {}
    for raw in raw_occurrences:
        if not isinstance(raw, Mapping):
            raise FactualUtilizationPlanError("plan occurrence is malformed")
        occurrence_id = raw.get("occurrence_id")
        actor_id = raw.get("actor_id")
        if not isinstance(occurrence_id, str) or not occurrence_id or not isinstance(actor_id, str):
            raise FactualUtilizationPlanError("plan occurrence has an invalid identity")
        if occurrence_id in occurrence_actor_by_id:
            raise FactualUtilizationPlanError("plan occurrence identity is duplicated")
        occurrence_actor_by_id[occurrence_id] = actor_id

    episode_by_id = {
        value.factual_episode_id: value for value in binding_result.factual_episodes
    }
    instances = tuple(_instance(value) for value in plan_row["top_level_instances"])
    if any(value.case_id != case_id for value in instances):
        raise FactualUtilizationPlanError("top-level instance crossed a case boundary")

    action_by_id: dict[str, FactualAction] = {
        action.factual_action_id: action
        for episode in binding_result.factual_episodes
        for action in episode.factual_actions
    }
    if len(action_by_id) != sum(
        len(episode.factual_actions) for episode in binding_result.factual_episodes
    ):
        raise FactualUtilizationPlanError("factual action identity is duplicated")
    actions_by_episode_actor: dict[tuple[str, str], list[FactualAction]] = {}
    for action in action_by_id.values():
        actions_by_episode_actor.setdefault(
            (action.factual_episode_id, action.source_actor_id), []
        ).append(action)
    for values in actions_by_episode_actor.values():
        values.sort(key=lambda value: value.sequence_index)

    capable_by_episode_actor: dict[
        tuple[str, str], list[tuple[OffenseInstanceKey, FactualAction, str]]
    ] = {}
    for instance in instances:
        provenance = provenance_by_instance.get(instance)
        if provenance is None:
            raise FactualUtilizationPlanError("top-level instance has no episode lineage")
        episode_id = provenance.get("factual_episode_id")
        if not isinstance(episode_id, str) or episode_id not in episode_by_id:
            raise FactualUtilizationPlanError("top-level instance has an invalid episode lineage")
        if has_authored_indirect_principal_capability(registry, instance.offense_ref):
            focal_action_id = provenance.get("focal_action_id")
            # A derived realization has multiple source actions but no authored focal
            # action.  It cannot be silently treated as a factual direction action.
            if focal_action_id is None:
                continue
            if not isinstance(focal_action_id, str):
                raise FactualUtilizationPlanError("focal action identity is malformed")
            focal_action = action_by_id.get(focal_action_id)
            if focal_action is None or focal_action.factual_episode_id != episode_id:
                raise FactualUtilizationPlanError("focal action has broken episode lineage")
            # The liable actor may be a participant in an action performed by
            # somebody else (e.g. receipt).  That does not make the liable actor a
            # factual utilizer for Article 34 direction.
            if focal_action.source_actor_id != instance.actor_id:
                continue
            carrier_ids = provenance.get("carrier_ids")
            if not isinstance(carrier_ids, Mapping):
                raise FactualUtilizationPlanError(
                    "focal utilization action lacks explicit carrier provenance"
                )
            evidence_id = carrier_ids.get("focal_action")
            if not isinstance(evidence_id, str) or not evidence_id:
                raise FactualUtilizationPlanError(
                    "focal utilization action lacks an explicit focal-action carrier"
                )
            if occurrence_actor_by_id.get(evidence_id) != instance.actor_id:
                raise FactualUtilizationPlanError(
                    "focal utilization carrier does not resolve to the utilizer actor"
                )
            capable_by_episode_actor.setdefault((episode_id, instance.actor_id), []).append(
                (instance, focal_action, evidence_id)
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
            (instance, focal_action, evidence_id)
            for instance, focal_action, evidence_id in capable
            if any(
                evidence.source_start < fragment.source_end
                and fragment.source_start < evidence.source_end
                for evidence in interaction.evidence
                for fragment in focal_action.source_fragments
            )
        )
        if not capable:
            continue
        episode = episode_by_id.get(interaction.factual_episode_id)
        if episode is None:
            raise FactualUtilizationPlanError("interaction has an unknown factual episode")
        used_for_interaction = False
        for instance, focal_action, evidence_id in capable:
            for actor_id in interaction.target_actor_ids:
                if actor_id not in episode.participants:
                    raise FactualUtilizationPlanError(
                        "interaction target is outside its episode"
                    )
                for participant_action in actions_by_episode_actor.get(
                    (interaction.factual_episode_id, actor_id), ()
                ):
                    if participant_action.sequence_index <= focal_action.sequence_index:
                        continue
                    # GoldFactualParticipant carries one exact source span.  Do not
                    # fuse separate action fragments back into an episode-wide carrier.
                    if len(participant_action.source_fragments) != 1:
                        continue
                    fragment = participant_action.source_fragments[0]
                    participant_id = _participant_id(
                        participant_action.factual_action_id, actor_id
                    )
                    participant = GoldFactualParticipant(
                        participant_id,
                        actor_id,
                        fragment.source_quote,
                        fragment.source_start,
                        fragment.source_end,
                    )
                    previous = participants.get(participant_id)
                    if previous is not None and previous != participant:
                        raise FactualUtilizationPlanError(
                            "factual participant identity collision"
                        )
                    participants[participant_id] = participant
                    participant_key = FactualParticipantKey(case_id, participant_id)
                    target = FactualUtilizationTarget(
                        FactualActionKey(
                            case_id, instance.actor_id, instance.occurrence_id
                        ),
                        participant_key,
                        evidence_id,
                    )
                    outcome = UtilizedParticipantOutcomeTarget(
                        participant_key, instance.offense_ref
                    )
                    if target not in targets:
                        targets.append(target)
                    if outcome not in outcomes:
                        outcomes.append(outcome)
                    used_for_interaction = True
        if used_for_interaction and interaction.interaction_id not in used:
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
