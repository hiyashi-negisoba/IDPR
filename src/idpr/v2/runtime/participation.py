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

from collections.abc import Iterable
from typing import Literal

from idpr.v2 import expressions, participation
from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue, evaluate, fold_all, fold_any
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.runtime import pipeline
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.indirect_principal_grounding import IndirectPrincipalDependency
from idpr.v2.runtime.stages import (
    CoPrincipalConstitutiveStatusObligation,
    IndirectPrincipalDependencyObligation,
    LiabilityEvaluation,
    Obligation,
    ObligationOutcome,
    ParticipationDependencyObligation,
    ParticipationRequirementObligation,
    StageResult,
    UtilizedParticipantOutcome,
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


def resolve_co_principal_liability(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    offense_ref: str,
    target: OffenseInstanceKey,
    sources: Iterable[OffenseInstanceKey],
    completion,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Resolve a co-principal without turning an actor-specific status into a target fact.

    Conduct attribution remains the existing ATTRIBUTE transformation.  Article 33's explicit
    `constitutive_status_refs`, if any, instead get their Elements value from one obligation per
    frozen ref.  The returned evaluation therefore sees the legal effect in its slot expression,
    while both the input and the attributed `CaseTruths` retain the target's own status truth.
    """
    policy = participation.participation_policy_for(registry)
    offense = registry.get(offense_ref)
    sources = tuple(sources)
    attributed_truths = apply_attribution(registry, compiled, offense_ref, target, sources, truths)
    if policy is None or offense is None:
        return pipeline.resolve_liability(
            registry, compiled, target, completion, active, attributed_truths
        )

    overrides: dict[str, TruthValue] = {}
    outcomes: list[ObligationOutcome] = []
    for ref in participation.constitutive_status_refs(offense):
        candidates = (target, *sources)
        values = tuple(truths.predicate.get((candidate, ref), UNKNOWN) for candidate in candidates)
        satisfying = tuple(
            candidate for candidate, value in zip(candidates, values, strict=True) if value == TRUE
        )
        truth = fold_any(values)
        overrides[ref] = truth
        outcomes.append(ObligationOutcome(
            obligation=CoPrincipalConstitutiveStatusObligation(
                ref=ref, satisfying_instances=satisfying
            ),
            truth=truth,
        ))

    return pipeline.resolve_liability(
        registry,
        compiled,
        target,
        completion,
        active,
        attributed_truths,
        element_truth_overrides=overrides,
        element_provenance=tuple(outcomes),
    )


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


def indirect_principal_dependency_truth(
    utilised: LiabilityEvaluation | UtilizedParticipantOutcome,
    negligence_evaluation: LiabilityEvaluation | None = None,
) -> tuple[TruthValue, str]:
    """Article 34's concrete, direction-reversed dependency classification.

    This is intentionally not `NOT(principal_realization_truth(...))`: a confirmed Elements
    failure, Unlawfulness defeat, Culpability defeat, and a realised different negligence offense
    have distinct legal provenance.  `negligence_evaluation` is caller-selected; this runtime
    never infers negligence from an offense id or asks a model to classify it.
    """
    if isinstance(utilised, UtilizedParticipantOutcome):
        if negligence_evaluation is not None:
            return UNKNOWN, "dedicated_outcome_cannot_mix_negligence_evaluation"
        if utilised.status in {
            "elements_failure",
            "unlawfulness_defeat",
            "culpability_defeat",
            "punishability_defeat",
            "different_negligence_offense",
        }:
            return TRUE, utilised.status
        if utilised.status == "liable_exact_offense":
            return FALSE, utilised.status
        return UNKNOWN, "utilized_participant_outcome_unresolved"
    if negligence_evaluation is not None:
        if negligence_evaluation.instance.offense_ref == utilised.instance.offense_ref:
            return UNKNOWN, "negligence_outcome_not_a_different_offense"
        if negligence_evaluation.liability_result is not None:
            return TRUE, "different_negligence_offense"
        return UNKNOWN, "different_negligence_outcome_unresolved"
    if utilised.elements.gate_state == "fails":
        return TRUE, "target_elements_failure"
    if utilised.unlawfulness.gate_state == "fails":
        return TRUE, "unlawfulness_defeat"
    if utilised.culpability.gate_state == "fails":
        return TRUE, "culpability_defeat_after_realization"
    if utilised.punishability.gate_state == "fails":
        return TRUE, "punishability_defeat"
    if utilised.liability_result is not None:
        return FALSE, "utilised_actor_liable"
    return UNKNOWN, "utilised_actor_outcome_unresolved"


def resolve_indirect_principal_liability(
    registry: DefinitionRegistry,
    dependency: IndirectPrincipalDependency,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Run Article 34 from a compiled utilization dependency, never an accessory mode."""

    instance = dependency.utilizer_instance
    if dependency.utilized_outcome.participant != dependency.utilized_participant:
        raise ValueError("indirect dependency participant identity mismatch")
    if dependency.utilized_outcome.offense_ref != instance.offense_ref:
        raise ValueError("indirect dependency exact-offense identity mismatch")
    outcomes = (
        ObligationOutcome(
            obligation=IndirectPrincipalDependencyObligation(reason=dependency.reason),
            truth=dependency.truth,
        ),
    )
    truth = fold_all(outcome.truth for outcome in outcomes)
    failed = [outcome.obligation for outcome in outcomes if outcome.truth == FALSE]
    elements = StageResult(
        evaluation_state="evaluated",
        legal_state=pipeline.ELEMENTS_STATE.get(truth, "unresolved"),
        gate_state=pipeline.ELEMENTS_GATE.get(truth, "unresolved"),
        provenance=outcomes,
    )
    return pipeline.resolve_from_elements(
        registry,
        active,
        instance,
        None,
        truths,
        elements,
        pipeline.decisive_obligation(failed),
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
            obligation=ParticipationDependencyObligation(
                mode=mode, principal_instance=principal.instance
            ),
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
    "indirect_principal_dependency_truth",
    "principal_realization_truth",
    "resolve_co_principal_liability",
    "resolve_derivative_liability",
    "resolve_indirect_principal_liability",
]
