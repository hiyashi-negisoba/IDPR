"""Stage execution for one actor/offense occurrence (build-order steps 6A + 6B).

    Completion -> Elements -> Unlawfulness -> [OffenseRealization] -> Culpability
               -> [OffenseEstablishment] -> Punishability -> [LiabilityResult]

Once a gate does not pass, the remaining stages are `not_reached` and are NOT speculatively
evaluated (v2.2.0 section 24: alternative reasoning is a generation-layer operation, never a
symbolic execution mode). "Does not pass" covers `unresolved` as well as `fails` -- an unresolved
Unlawfulness does not license reasoning about culpability.

Completion sits ahead of the chain rather than inside it (section 14: it is an orthogonal axis).
It decides *which obligations exist* before Elements decides whether they are met, which is what
makes 미수 expressible without the forbidden `completed failed -> attach attempt label` move. Three
completion outcomes stop the run before Elements, all for the same reason: there is no honest
program to evaluate.

    unresolved       which obligations exist is unknown -- evaluating anyway would pick one
                     reading of the law and present it as the answer
    not_applicable   no completion state obtains, so this offense has no shape here at all
    punishable=False the state obtains but is not a punishable legal shape (불능범, 예비 불벌);
                     computing 구성요건해당성 for it is exactly the hypothetical reasoning
                     section 24 keeps out of symbolic state

Execution order note for step 6C, fixed here so it does not get rediscovered: ATTRIBUTE precedes
Completion, which precedes Elements (v2.2.0 section 18). Co-principal attribution can change which
completion state is derived, so it cannot be applied afterwards. File order (completion before
participation) is unrelated to execution order.
"""

from __future__ import annotations

from typing import Iterator

from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import FALSE, TRUE, evaluate, fold_all
from idpr.v2.expressions import SLOT_NAMES
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.relations import evaluate_relation, iter_relation_instances
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.effects import ActiveDoctrineRefs, resolve_stage
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.stages import (
    CompletionRequirementObligation,
    LiabilityEvaluation,
    LiabilityResult,
    Obligation,
    ObligationOutcome,
    OffenseEstablishment,
    OffenseRealization,
    RelationObligation,
    SlotObligation,
    StageResult,
    not_reached,
)
from idpr.v2.runtime.truths import CaseTruths

_ELEMENTS_STATE = {TRUE: "satisfied", FALSE: "failed"}
_ELEMENTS_GATE = {TRUE: "passes", FALSE: "fails"}


def resolve_liability(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Run one instance to a `LiabilityEvaluation`, under an already-derived completion judgement.

    `completion` is an input, not something computed here: deriving it is `completion.
    resolve_completion()`'s job, and in step 6C attribution will run before that derivation
    (section 18). Passing it in keeps the "who did what" and "what does the law require" decisions
    outside the stage machinery.

    Assumes an already type-checked registry and a successfully compiled offense, exactly as
    `evaluate.evaluate()` and `relations.evaluate_compiled_offense()` do.
    """
    if completion.state in ("unresolved", "not_applicable") or completion.punishable is False:
        return _stopped(instance, completion, "completion", elements=not_reached())

    elements, decisive_obligation = _resolve_elements(compiled, instance, completion, truths)
    if elements.gate_state != "passes":
        return _stopped(
            instance,
            completion,
            "elements",
            elements=elements,
            decisive_obligation=decisive_obligation,
        )

    unlawfulness = resolve_stage("unlawfulness", active, registry, instance, truths)
    if unlawfulness.gate_state != "passes":
        return _stopped(
            instance, completion, "unlawfulness", elements=elements, unlawfulness=unlawfulness
        )

    realization = OffenseRealization(
        instance=instance, elements=elements, unlawfulness=unlawfulness
    )

    culpability = resolve_stage("culpability", active, registry, instance, truths)
    if culpability.gate_state != "passes":
        return _stopped(
            instance,
            completion,
            "culpability",
            elements=elements,
            unlawfulness=unlawfulness,
            culpability=culpability,
            realization=realization,
        )

    establishment = OffenseEstablishment(
        instance=instance, realization=realization, culpability=culpability
    )

    punishability = resolve_stage("punishability", active, registry, instance, truths)
    if punishability.gate_state != "passes":
        return _stopped(
            instance,
            completion,
            "punishability",
            elements=elements,
            unlawfulness=unlawfulness,
            culpability=culpability,
            punishability=punishability,
            realization=realization,
            establishment=establishment,
        )

    return LiabilityEvaluation(
        instance=instance,
        completion=completion,
        elements=elements,
        unlawfulness=unlawfulness,
        culpability=culpability,
        punishability=punishability,
        realization=realization,
        establishment=establishment,
        liability_result=LiabilityResult(
            instance=instance, establishment=establishment, punishability=punishability
        ),
        decisive_stage=None,
    )


def _stopped(
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    decisive_stage: str,
    *,
    elements: StageResult,
    unlawfulness: StageResult | None = None,
    culpability: StageResult | None = None,
    punishability: StageResult | None = None,
    realization: OffenseRealization | None = None,
    establishment: OffenseEstablishment | None = None,
    decisive_obligation: Obligation | None = None,
) -> LiabilityEvaluation:
    """Build the evaluation for a path that stopped at `decisive_stage`.

    Stages after the stopping point are `not_reached` -- never re-run under a hypothetical
    assumption. The conclusions passed in are exactly those whose gate did pass, so a stopped path
    never fabricates an `OffenseRealization` for an offense that was not realized.
    """
    stopper = punishability or culpability or unlawfulness
    return LiabilityEvaluation(
        instance=instance,
        completion=completion,
        elements=elements,
        unlawfulness=unlawfulness or not_reached(),
        culpability=culpability or not_reached(),
        punishability=punishability or not_reached(),
        realization=realization,
        establishment=establishment,
        liability_result=None,
        decisive_stage=decisive_stage,
        decisive_obligation=decisive_obligation,
        decisive_doctrine=None if stopper is None else _decisive_doctrine(stopper),
    )


def _resolve_elements(
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    truths: CaseTruths,
) -> tuple[StageResult, Obligation | None]:
    """Elements as an aggregation over individually-recorded obligations.

    With no suspensions the fold is `fold_all` over exactly the same multiset of truths that
    `relations.evaluate_compiled_offense()` folds, so the resulting TruthValue is identical (a
    regression test pins that for the completed state). Obligations are evaluated one by one only
    so a decisive one can be named -- not to re-derive the semantics.

    Under a suspending completion state the two deliberately diverge, and that divergence is the
    whole point: `evaluate_compiled_offense` is v2.1, it knows nothing about cases or completion,
    and it must stay that way. Completion semantics live here and nowhere else.

    Elements carries no `effects`: section 12.1 keeps doctrines off this stage entirely, and the
    schema's DoctrineDef stage enum has no `elements` member.
    """
    outcomes = tuple(_iter_obligations(compiled, instance, completion, truths))
    elements_truth = fold_all(outcome.truth for outcome in outcomes)
    failed = [outcome.obligation for outcome in outcomes if outcome.truth == FALSE]

    stage = StageResult(
        evaluation_state="evaluated",
        legal_state=_ELEMENTS_STATE.get(elements_truth, "unresolved"),
        gate_state=_ELEMENTS_GATE.get(elements_truth, "unresolved"),
        provenance=outcomes,
    )
    return stage, _decisive_obligation(failed)


def _iter_obligations(
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    truths: CaseTruths,
) -> Iterator[ObligationOutcome]:
    """The obligations this completion state actually imposes.

    A suspended slot or relation is DROPPED from the iteration, not yielded as TRUE. The difference
    is not cosmetic: substituting TRUE would rewrite a FALSE result into a satisfied element, which
    is the exact move section 14 forbids, and it would also be indistinguishable from the
    evaluator's genuine vacuous-truth case (an un-authored, empty slot).
    """
    predicate_view = truths.predicate_view(instance)
    relation_view = truths.relation_view(instance)

    for slot in SLOT_NAMES:
        if slot in completion.suspended_slots:
            continue
        yield ObligationOutcome(
            obligation=SlotObligation(slot=slot),
            truth=evaluate(compiled.slots.get(slot), predicate_view),
        )
    for key, _binding in iter_relation_instances(compiled):
        if completion.relation_dispositions.get(key) == "suspend":
            continue
        yield ObligationOutcome(
            obligation=RelationObligation(
                key=RuntimeRelationKey(instance=instance, definition_key=key)
            ),
            truth=evaluate_relation(key, relation_view),
        )
    if completion.additional_requirements is not None:
        yield ObligationOutcome(
            obligation=CompletionRequirementObligation(state=completion.state),
            truth=evaluate(completion.additional_requirements, predicate_view),
        )


def _decisive_obligation(failed: list[Obligation]) -> Obligation | None:
    """Exactly one FALSE obligation names itself; several name none.

    No ranking is introduced to break the tie (v2.2.0 section 14 keeps semantic scheduling out of
    the runtime). Every failure stays in `provenance` either way.
    """
    return failed[0] if len(failed) == 1 else None


def _decisive_doctrine(stage: StageResult) -> str | None:
    """The doctrine that closed this gate, when exactly one did."""
    firing = [effect.doctrine_ref for effect in stage.effects if effect.truth == TRUE]
    return firing[0] if len(firing) == 1 else None
