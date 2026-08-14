"""Evidence-scoped participation candidate materialization from Call 1.5-P."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import product
from typing import Any

from idpr.v2.factual_interaction import FactualInteraction
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.issue_binding import IssueBindingResult
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import ParticipationLocalTarget


class FactualParticipationError(ValueError):
    pass


@dataclass(frozen=True)
class FactualParticipationPlan:
    targets: tuple[ParticipationLocalTarget, ...]
    evidence_occurrences: tuple[GoldOccurrence, ...]
    skipped_interaction_ids: tuple[str, ...]
    candidate_episodes: tuple[tuple[OffenseInstanceKey, str], ...] = ()
    """새로 만든 participation candidate instance와 그 factual episode.

    직접 결박된 instance는 planner가 이미 episode를 기록하지만, 여기서 만드는 후보는
    planner의 binding이 아니어서 그 기록이 없다. 최종 책임 단계(경합·초과)는 episode 없이는
    후보를 열 수 없고, 없는 것을 나중에 사실에서 다시 읽어 내면 그 단계가 사건 텍스트를
    두 번째로 해석하게 된다. 그래서 만든 자리에서 함께 나른다.
    """


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _participation_occurrence_id(
    interaction: FactualInteraction,
    actor_id: str,
    offense_ref: str,
    identity_discriminator: str | None,
) -> str:
    identity = f"{offense_ref}\0{identity_discriminator or ''}"
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:10]
    suffix = interaction.interaction_id.removeprefix("finteraction:")
    return f"participation_binding:{suffix}:{actor_id}:{digest}"


def materialize_factual_participation_candidates(
    *,
    case_id: str,
    plan_row: Mapping[str, Any],
    binding_result: IssueBindingResult,
    interactions: Iterable[FactualInteraction],
    responsibility_actor_ids: Sequence[str],
    registry: DefinitionRegistry,
) -> FactualParticipationPlan:
    """Join interactions to same-episode or nearest-next offense bindings."""
    if plan_row.get("participation_local_targets"):
        raise FactualParticipationError(
            "factual participation materializer requires an empty prior target universe"
        )
    responsibility = frozenset(responsibility_actor_ids)
    if not responsibility:
        raise FactualParticipationError("responsibility actor universe is empty")

    episode_by_occurrence = {
        binding.binding_id: binding.factual_episode_id
        for binding in binding_result.bindings
    }
    for value in plan_row.get("derived_binding_candidates", []):
        episode_by_occurrence[str(value["binding_id"])] = str(
            value["factual_episode_id"]
        )
    top_level = tuple(_instance(value) for value in plan_row["top_level_instances"])
    if any(value.case_id != case_id for value in top_level):
        raise FactualParticipationError("top-level instance crossed a case boundary")
    active_offenses_by_actor: dict[str, set[str]] = {}
    for instance in top_level:
        active_offenses_by_actor.setdefault(instance.actor_id, set()).add(
            instance.offense_ref
        )

    def is_necessary_counterpart_candidate(
        offense_ref: str, actor_ids: Iterable[str]
    ) -> bool:
        offense = registry.get(offense_ref)
        if offense is None or offense.kind not in {"offense", "derived_offense"}:
            raise FactualParticipationError(
                f"{case_id}: participation endpoint is not an offense"
            )
        counterpart_refs = frozenset(
            (offense.payload.get("participation_constraints") or {}).get(
                "necessary_counterpart_offense_refs"
            )
            or ()
        )
        return bool(
            counterpart_refs
            and any(
                active_offenses_by_actor.get(actor_id, set()) & counterpart_refs
                for actor_id in actor_ids
            )
        )
    anchors_by_episode_actor: dict[
        tuple[str, str], list[OffenseInstanceKey]
    ] = {}
    for instance in top_level:
        episode_id = episode_by_occurrence.get(instance.occurrence_id)
        if episode_id is None:
            raise FactualParticipationError(
                f"{case_id}: top-level instance has no factual episode lineage"
            )
        anchors_by_episode_actor.setdefault(
            (episode_id, instance.actor_id), []
        ).append(instance)
    episode_rank = {
        value.factual_episode_id: index
        for index, value in enumerate(binding_result.factual_episodes)
    }
    if set(episode_by_occurrence.values()) - set(episode_rank):
        raise FactualParticipationError(
            f"{case_id}: binding refers to an unknown factual episode"
        )

    def nearest_next_anchor_episode(
        interaction: FactualInteraction,
        actor_ids: Iterable[str],
    ) -> str | None:
        """Return one structural continuation episode, never the whole scope."""
        current_rank = episode_rank[interaction.factual_episode_id]
        actors = frozenset(actor_ids)
        candidates = {
            episode_id
            for episode_id, actor_id in anchors_by_episode_actor
            if actor_id in actors and episode_rank[episode_id] > current_rank
        }
        if not candidates:
            return None
        return min(candidates, key=episode_rank.__getitem__)

    occurrence_by_id = {
        str(value["occurrence_id"]): GoldOccurrence(
            str(value["occurrence_id"]),
            str(value["actor_id"]),
            str(value["source_text"]),
            int(value["source_span"]["start"]),
            int(value["source_span"]["end"]),
        )
        for value in plan_row["occurrences"]
    }
    created_occurrences: dict[str, GoldOccurrence] = {}
    created_episodes: dict[OffenseInstanceKey, str] = {}
    targets: list[ParticipationLocalTarget] = []
    seen_targets: set[ParticipationLocalTarget] = set()
    used_interactions: set[str] = set()

    def participant_instances(
        interaction: FactualInteraction,
        actor_id: str,
        offense_ref: str,
        *,
        prefer_existing: bool = True,
        fallback_episode_id: str | None = None,
        identity_discriminator: str | None = None,
    ) -> tuple[OffenseInstanceKey, ...]:
        existing = tuple(
            value
            for value in anchors_by_episode_actor.get(
                (interaction.factual_episode_id, actor_id), []
            )
            if value.offense_ref == offense_ref
        )
        if not existing and fallback_episode_id is not None:
            existing = tuple(
                instance
                for instance in anchors_by_episode_actor.get(
                    (fallback_episode_id, actor_id), []
                )
                if instance.offense_ref == offense_ref
            )
        if existing and prefer_existing:
            # Multiple direct realizations remain distinct candidate identities.
            return existing
        occurrence_id = _participation_occurrence_id(
            interaction, actor_id, offense_ref, identity_discriminator
        )
        evidence_text = "\n".join(value.source_quote for value in interaction.evidence)
        start = min(value.source_start for value in interaction.evidence)
        end = max(value.source_end for value in interaction.evidence)
        created = GoldOccurrence(
            occurrence_id, actor_id, evidence_text, start, end
        )
        previous = created_occurrences.get(occurrence_id)
        if previous is not None and previous != created:
            raise FactualParticipationError(
                f"{case_id}: participation evidence identity collision"
            )
        created_occurrences[occurrence_id] = created
        instance = OffenseInstanceKey(case_id, actor_id, offense_ref, occurrence_id)
        # 후보의 factual home은 이 가담 행위가 일어난 episode다. principal을 뒤 episode에서
        # 찾아왔더라도 가담자가 그리로 옮겨 가지는 않는다.
        created_episodes[instance] = interaction.factual_episode_id
        return (instance,)

    def add(target: ParticipationLocalTarget, interaction_id: str) -> None:
        if target not in seen_targets:
            seen_targets.add(target)
            targets.append(target)
        used_interactions.add(interaction_id)

    interaction_values = tuple(interactions)
    for interaction in interaction_values:
        if interaction.source_actor_id not in responsibility:
            continue
        if interaction.interaction_type in {
            "request_or_instruction",
            "means_information_or_assistance",
        }:
            relation_kind = (
                "instigation"
                if interaction.interaction_type == "request_or_instruction"
                else "aiding"
            )
            for target_actor in interaction.target_actor_ids:
                principal_anchors = anchors_by_episode_actor.get(
                    (interaction.factual_episode_id, target_actor), []
                )
                if not principal_anchors:
                    # A request/help episode and its execution may be split.  Only the
                    # nearest later episode with an active binding is a structural
                    # continuation candidate; later episodes must not inherit it.
                    fallback_episode_id = nearest_next_anchor_episode(
                        interaction, (target_actor,)
                    )
                    principal_anchors = anchors_by_episode_actor.get(
                        (fallback_episode_id, target_actor), []
                    ) if fallback_episode_id is not None else []
                for principal in principal_anchors:
                    if is_necessary_counterpart_candidate(
                        principal.offense_ref,
                        (interaction.source_actor_id,),
                    ):
                        continue
                    actor = participant_instances(
                        interaction,
                        interaction.source_actor_id,
                        principal.offense_ref,
                        prefer_existing=False,
                        identity_discriminator=principal.occurrence_id,
                    )[0]
                    add(
                        ParticipationLocalTarget(
                            relation_kind, (actor, principal)
                        ),
                        interaction.interaction_id,
                    )
            continue

        member_actor_ids = tuple(
            dict.fromkeys(
                actor_id
                for actor_id in (
                    interaction.source_actor_id,
                    *interaction.target_actor_ids,
                )
                if actor_id in responsibility
            )
        )
        if len(member_actor_ids) < 2:
            continue
        anchor_offenses = tuple(
            dict.fromkeys(
                instance.offense_ref
                for actor_id in member_actor_ids
                for instance in anchors_by_episode_actor.get(
                    (interaction.factual_episode_id, actor_id), []
                )
            )
        )
        if not anchor_offenses:
            fallback_episode_id = nearest_next_anchor_episode(
                interaction, member_actor_ids
            )
            anchor_offenses = tuple(
                dict.fromkeys(
                    instance.offense_ref
                    for actor_id in member_actor_ids
                    for instance in anchors_by_episode_actor.get(
                        (fallback_episode_id, actor_id), []
                    )
                )
            ) if fallback_episode_id is not None else ()
        else:
            fallback_episode_id = None
        for offense_ref in anchor_offenses:
            if is_necessary_counterpart_candidate(
                offense_ref, member_actor_ids
            ):
                continue
            member_options = tuple(
                participant_instances(
                    interaction,
                    actor_id,
                    offense_ref,
                    fallback_episode_id=fallback_episode_id,
                )
                for actor_id in member_actor_ids
            )
            for members in product(*member_options):
                add(
                    ParticipationLocalTarget("co_principal_group", tuple(members)),
                    interaction.interaction_id,
                )

    all_occurrence_ids = set(occurrence_by_id)
    if all_occurrence_ids & set(created_occurrences):
        raise FactualParticipationError(
            f"{case_id}: participation occurrence collides with planner evidence"
        )
    return FactualParticipationPlan(
        tuple(targets),
        tuple(created_occurrences.values()),
        tuple(
            value.interaction_id
            for value in interaction_values
            if value.interaction_id not in used_interactions
        ),
        tuple(created_episodes.items()),
    )


def derived_co_principal_targets(
    registry: DefinitionRegistry,
    targets: Iterable[ParticipationLocalTarget],
) -> tuple[ParticipationLocalTarget, ...]:
    """Open authored same-episode derived groups after a base co-group is discovered.

    The original planner can materialize ``special_theft`` only when both actors already
    have direct theft bindings.  Call 1.5-P may create the missing member later.  This
    function closes exactly that ordering gap from the derived definition's
    ``distinct_actor_binding_sets``; it performs no case-text or liability inference.
    """
    values = tuple(targets)
    existing = set(values)
    output: list[ParticipationLocalTarget] = []
    derived_entries = registry.by_kind.get("derived_offense", ())
    for target in values:
        if target.kind != "co_principal_group":
            continue
        for entry in derived_entries:
            metadata = entry.payload.get("candidate_materialization")
            if not isinstance(metadata, Mapping):
                continue
            peer_sets = metadata.get("distinct_actor_binding_sets") or ()
            if [target.offense_ref] not in peer_sets:
                continue
            derivation = entry.payload.get("derivation") or {}
            if derivation.get("base") != target.offense_ref:
                continue
            candidate = ParticipationLocalTarget(
                "co_principal_group",
                tuple(
                    OffenseInstanceKey(
                        member.case_id,
                        member.actor_id,
                        entry.id,
                        member.occurrence_id,
                    )
                    for member in target.members
                ),
            )
            if candidate not in existing:
                existing.add(candidate)
                output.append(candidate)
    return tuple(output)


__all__ = [
    "FactualParticipationError",
    "FactualParticipationPlan",
    "derived_co_principal_targets",
    "materialize_factual_participation_candidates",
]
