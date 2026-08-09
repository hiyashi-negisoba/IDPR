"""Participation / Attribution (build-order step 6C) -- v2.1.0 section 15, v2.2.0 section 18/22.

Two runtime entry points, one per mode family that needs anything beyond `resolve_liability()`
as it already exists:

    Direct principal    -- nothing here. Callers use `resolve_liability()` unchanged.
    Co-principal         -- `apply_attribution()` below, then `resolve_completion()` /
                            `resolve_liability()` exactly as today, fed the returned CaseTruths.
    Instigator / Aider   -- `resolve_derivative_liability()` below.

No orchestrator here decides WHICH mode applies to which actor in a case -- that is case-fact
grouping (who committed with whom, who instigated whom), and deciding it is step 7/8's closure/probe
territory, the same reason `ActiveDoctrineRefs` is caller-supplied rather than derived in step 6A.
"""

from __future__ import annotations

from typing import Iterable, Literal

from idpr.v2 import expressions, participation
from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue, evaluate, fold_all, fold_any
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.runtime import pipeline
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import (
    LiabilityEvaluation,
    Obligation,
    ObligationOutcome,
    ParticipationDependencyObligation,
    ParticipationRequirementObligation,
    StageResult,
)
from idpr.v2.runtime.truths import CaseTruths

DerivativeMode = Literal["instigator", "aider"]


def apply_attribution(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    offense_ref: str,
    target: OffenseInstanceKey,
    sources: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
) -> CaseTruths:
    """ATTRIBUTE (section 15.2) as a predicate-view merge, scoped to `attributable_slots`' leaf
    refs -- never a slot-truth substitution, so the existing ATTRIBUTE -> Completion -> Elements
    order (section 18) keeps working on an ordinary `CaseTruths` unmodified.

    For each leaf ref referenced by an attributable slot, the target's truth becomes the 3-valued
    OR (`fold_any`) of its own truth and every source's truth for that same ref -- 일부실행
    전부책임: either co-principal's own conduct satisfies the shared element. Relation truths are
    untouched; attribution is predicate-level only (decision #1).

    Returns a NEW `CaseTruths`; `truths` itself is never mutated. No-op (returns `truths` as-is)
    when there is no participation policy, or `co_principal` is disabled/empty for this offense --
    same "absence is the ordinary case" precedent as `completion.completion_policy_for(None)`.
    """
    policy = participation.participation_policy_for(registry)
    offense_entry = registry.get(offense_ref)
    if policy is None or offense_entry is None:
        return truths

    slots = participation.effective_attributable_slots(policy, offense_entry)
    if not slots:
        return truths

    leaves = frozenset().union(
        *(expressions.canonical_leaf_refs(compiled.slots.get(slot)) for slot in slots)
    )
    if not leaves:
        return truths

    sources = tuple(sources)
    new_predicate = dict(truths.predicate)
    for ref in leaves:
        values = [truths.predicate.get((target, ref), UNKNOWN)]
        values.extend(truths.predicate.get((source, ref), UNKNOWN) for source in sources)
        new_predicate[(target, ref)] = fold_any(values)
    return CaseTruths(predicate=new_predicate, relation=truths.relation)


def principal_realization_truth(principal: LiabilityEvaluation) -> TruthValue:
    """The 3-valued read of a principal's existing stage results (decision #4) -- not a new
    exception type.

        TRUE     principal.realization exists (its gate already passed).
        FALSE    a stage is CONFIRMED to have stopped it: elements or unlawfulness
                 gate_state == "fails", or completion.state == "not_applicable".
        UNKNOWN  everything else: completion.state == "unresolved", completion.punishable is
                 False (elements were never computed for that shape at all -- section 24 forbids
                 computing them hypothetically, so whether they would have been satisfied is
                 genuinely unknown, not a confirmed non-event), or elements/unlawfulness
                 gate_state == "unresolved".

    `principal.completion` can itself be None (the principal was resolved via
    `resolve_derivative_liability` -- chained participation). In that case the completion-specific
    branches are skipped and the read falls through to `principal.elements`/`.unlawfulness`
    gate_state, which `_resolve_derivative_elements()` populates with the same
    `ELEMENTS_STATE`/`ELEMENTS_GATE` shape as the direct path, so the read stays correct either way.
    """
    if principal.realization is not None:
        return TRUE

    completion = principal.completion
    if completion is not None:
        if completion.state == "not_applicable":
            return FALSE
        if completion.state == "unresolved":
            return UNKNOWN
        if completion.punishable is False:
            return UNKNOWN

    if principal.elements.gate_state == "fails":
        return FALSE
    if principal.elements.gate_state == "unresolved":
        return UNKNOWN
    if principal.unlawfulness.gate_state == "fails":
        return FALSE
    return UNKNOWN


def resolve_derivative_liability(
    registry: DefinitionRegistry,
    policy: DefinitionEntry,
    mode: DerivativeMode,
    principal: LiabilityEvaluation,
    instance: OffenseInstanceKey,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Decision #3: the accessory's own Elements never re-runs the principal's `CompiledOffense`.

    Elements = `principal_realization_truth(principal)` AND the mode's own `requires` (required by
    the 8th schema addendum -- always authored, evaluated against the accessory's OWN predicate
    view, never the principal's). Everything after Elements is `pipeline.resolve_from_elements()`
    -- the same function the direct/co-principal path runs through, so Unlawfulness/Culpability/
    Punishability are never re-implemented here.

    `completion=None` always: the derivative path never derives a `CompletionResult` for the
    accessory (accessories skip Completion entirely). The principal's own completion is already
    reachable via `principal.completion` if ever needed -- never copied onto the accessory's
    `LiabilityEvaluation`.
    """
    elements, obligation = _resolve_derivative_elements(policy, mode, principal, instance, truths)
    return pipeline.resolve_from_elements(
        registry, active, instance, None, truths, elements, obligation
    )


def _resolve_derivative_elements(
    policy: DefinitionEntry,
    mode: DerivativeMode,
    principal: LiabilityEvaluation,
    instance: OffenseInstanceKey,
    truths: CaseTruths,
) -> tuple[StageResult, Obligation | None]:
    """Exactly two obligations, always both -- `requires` is required on `derivative_mode`, so
    there is no conditional branch here for its absence. Mirrors `pipeline._resolve_elements()`'s
    shape, over a different (smaller) obligation set."""
    mode_payload = policy.payload["modes"][mode]
    predicate_view = truths.predicate_view(instance)
    outcomes = (
        ObligationOutcome(
            obligation=ParticipationDependencyObligation(mode=mode),
            truth=principal_realization_truth(principal),
        ),
        ObligationOutcome(
            obligation=ParticipationRequirementObligation(mode=mode),
            truth=evaluate(expressions.canonicalize(mode_payload["requires"]), predicate_view),
        ),
    )
    truth = fold_all(outcome.truth for outcome in outcomes)
    failed = [outcome.obligation for outcome in outcomes if outcome.truth == FALSE]

    stage = StageResult(
        evaluation_state="evaluated",
        legal_state=pipeline.ELEMENTS_STATE.get(truth, "unresolved"),
        gate_state=pipeline.ELEMENTS_GATE.get(truth, "unresolved"),
        provenance=outcomes,
    )
    return stage, pipeline.decisive_obligation(failed)


__all__ = [
    "DerivativeMode",
    "apply_attribution",
    "principal_realization_truth",
    "resolve_derivative_liability",
]
