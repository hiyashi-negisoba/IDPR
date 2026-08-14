"""Typed evidence carriers for instance-scoped Call 2 assessment.

The binding producer already distinguishes an actor's own action fragments from the
context needed to understand that action.  Preserve that distinction instead of
expanding a request to the untyped full case or factual episode.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.grounding import AssessmentTarget

_ACTOR_ARGUMENTS = frozenset(
    {"actor", "witness", "offender", "disposer", "possessor", "official"}
)


def actor_bound_ground_fact(
    registry: DefinitionRegistry, predicate_ref: str
) -> bool:
    """Whether a GroundFact attributes conduct or status to the fixed actor."""
    entry = registry.get(predicate_ref)
    if entry is None or entry.kind != "ground_fact":
        return False
    return any(
        isinstance(value, Mapping) and value.get("name") in _ACTOR_ARGUMENTS
        for value in entry.payload.get("arguments", ())
    )


def direct_bindings(issue_row: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    """Index authored direct bindings without treating derived instances as facts."""
    return {
        str(binding["binding_id"]): binding
        for seed in issue_row.get("seed_results", ())
        if isinstance(seed, Mapping)
        for binding in seed.get("bindings", ())
        if isinstance(binding, Mapping) and binding.get("binding_id")
    }


def _quotes(binding: Mapping[str, object], field: str) -> tuple[str, ...]:
    values = binding.get(field, ())
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        return ()
    return tuple(
        str(value["source_quote"])
        for value in values
        if isinstance(value, Mapping) and value.get("source_quote")
    )


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value.strip()))


def actor_aware_realization_context(
    *,
    registry: DefinitionRegistry,
    target: AssessmentTarget,
    plan_row: Mapping[str, object],
    issue_row: Mapping[str, object],
) -> dict[str, object] | None:
    """Build a provenance-only realization carrier for an offense-level predicate.

    Actor-bound GroundFacts deliberately receive no realization context: they remain
    attached to the exact actor-action source.  LegalElements and non-actor GroundFacts
    receive the target actor's authored action and context fragments from the same
    factual episode.  Peer actor bindings are excluded, not silently copied.
    """
    if actor_bound_ground_fact(registry, target.predicate_ref):
        return None

    bindings = direct_bindings(issue_row)
    occurrence_id = target.instance_key.occurrence_id
    derived_by_id = {
        str(value["binding_id"]): value
        for value in plan_row.get("derived_binding_candidates", ())
        if isinstance(value, Mapping) and value.get("binding_id")
    }
    provenance = derived_by_id.get(occurrence_id)
    if provenance is None:
        anchor = bindings.get(occurrence_id)
        if anchor is None:
            return None
        episode_id = str(anchor.get("factual_episode_id", occurrence_id))
        source_ids = (occurrence_id,)
    else:
        episode_id = str(provenance.get("factual_episode_id", occurrence_id))
        source_ids = tuple(str(value) for value in provenance.get("source_binding_ids", ()))

    actor_id = target.instance_key.actor_id
    selected: list[Mapping[str, object]] = []
    for source_id in source_ids:
        binding = bindings.get(source_id)
        if binding is not None and str(binding.get("actor_id")) == actor_id:
            selected.append(binding)

    # Same-actor bindings in the same episode are admissible realization context.  They
    # can carry intent, status, object, or result facts split from the raising binding.
    for binding in bindings.values():
        if (
            str(binding.get("actor_id")) == actor_id
            and str(binding.get("factual_episode_id")) == episode_id
            and binding not in selected
        ):
            selected.append(binding)
    if not selected:
        return None

    actor_actions = _deduplicate(
        [quote for binding in selected for quote in _quotes(binding, "actor_action_fragments")]
    )
    contexts = _deduplicate(
        [quote for binding in selected for quote in _quotes(binding, "context_fragments")]
    )
    excluded_peer_ids = sorted(
        str(binding_id)
        for binding_id, binding in bindings.items()
        if str(binding.get("factual_episode_id")) == episode_id
        and str(binding.get("actor_id")) != actor_id
    )
    if not actor_actions and not contexts:
        return None
    return {
        "carrier_policy": "actor_aware_realization_v1",
        "target_actor_id": actor_id,
        "factual_episode_id": episode_id,
        "same_actor_action_evidence": actor_actions,
        "context_evidence": contexts,
        "source_binding_ids": [str(value.get("binding_id")) for value in selected],
        "excluded_peer_actor_binding_ids": excluded_peer_ids,
        "attribution_rule": (
            "same_actor_action_evidence만 target actor의 행위로 귀속한다. "
            "context_evidence는 관계·상황 이해에만 사용하고 target actor의 별도 행위로 "
            "확장하지 않는다. 제외된 peer binding의 행위는 이 target에 귀속하지 않는다."
        ),
    }


def source_binding_realization_context(
    *,
    registry: DefinitionRegistry,
    target: AssessmentTarget,
    plan_row: Mapping[str, object],
    issue_row: Mapping[str, object],
) -> dict[str, object] | None:
    """Use only the planner-authored source bindings for an offense-level predicate.

    This is the narrow production candidate between a one-sentence occurrence and the
    broad same-actor episode carrier.  It follows explicit derived provenance but never
    admits a sibling binding merely because it shares an episode id.
    """
    if actor_bound_ground_fact(registry, target.predicate_ref):
        return None
    bindings = direct_bindings(issue_row)
    occurrence_id = target.instance_key.occurrence_id
    derived = next(
        (
            value
            for value in plan_row.get("derived_binding_candidates", ())
            if isinstance(value, Mapping)
            and str(value.get("binding_id", "")) == occurrence_id
        ),
        None,
    )
    source_ids = (
        tuple(str(value) for value in derived.get("source_binding_ids", ()))
        if derived is not None
        else (occurrence_id,)
    )
    actor_id = target.instance_key.actor_id
    selected = [
        bindings[source_id]
        for source_id in source_ids
        if source_id in bindings and str(bindings[source_id].get("actor_id")) == actor_id
    ]
    if not selected:
        return None
    actor_actions = _deduplicate(
        [quote for binding in selected for quote in _quotes(binding, "actor_action_fragments")]
    )
    contexts = _deduplicate(
        [quote for binding in selected for quote in _quotes(binding, "context_fragments")]
    )
    if not actor_actions and not contexts:
        return None
    return {
        "carrier_policy": "source_binding_realization_v1",
        "target_actor_id": actor_id,
        "same_actor_action_evidence": actor_actions,
        "context_evidence": contexts,
        "source_binding_ids": [str(value.get("binding_id")) for value in selected],
        "attribution_rule": (
            "planner가 이 realization의 source로 명시한 binding만 사용한다. "
            "context_evidence는 target actor의 별도 행위로 확장하지 않는다."
        ),
    }


__all__ = [
    "actor_aware_realization_context",
    "actor_bound_ground_fact",
    "direct_bindings",
    "source_binding_realization_context",
]
