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

from typing import Iterator, Mapping

from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import FALSE, TRUE, TruthValue, evaluate, fold_all
from idpr.v2.expressions import SLOT_NAMES
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.relations import evaluate_relation, iter_relation_instances
from idpr.v2.runtime.completion import CompletionResult, component_instance_for
from idpr.v2.runtime.effects import ActiveDoctrineRefs, resolve_stage
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.stages import (
    CompletionRequirementObligation,
    ComponentSlotObligation,
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

ELEMENTS_STATE = {TRUE: "satisfied", FALSE: "failed"}
ELEMENTS_GATE = {TRUE: "passes", FALSE: "fails"}
"""Public since step 6C: `runtime/participation.py`'s derivative Elements builder
(`_resolve_derivative_elements`) needs the same TruthValue -> legal/gate state mapping this module
already uses for the direct/co-principal path's Elements. Same promotion precedent as
`evaluate._fold_all` -> `fold_all` when a second caller needed it (Step 5)."""


class _PredicateViewWithOverrides(Mapping[str, TruthValue]):
    """A case view with a narrowly scoped symbolic Elements source substitution.

    CaseTruths stays immutable.  The only callers are Article 33's constitutive-status
    obligation and Article 151's linked-offender result; they provide the override and its
    matching provenance explicitly to `resolve_liability()`.
    """

    def __init__(self, base: Mapping[str, TruthValue], overrides: Mapping[str, TruthValue]) -> None:
        self._base = base
        self._overrides = overrides

    def __getitem__(self, ref: str) -> TruthValue:
        if ref in self._overrides:
            return self._overrides[ref]
        return self._base[ref]

    def __iter__(self) -> Iterator[str]:
        return iter(set(self._base) | set(self._overrides))

    def __len__(self) -> int:
        return len(set(self._base) | set(self._overrides))


def resolve_liability(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
    *,
    element_truth_overrides: Mapping[str, TruthValue] | None = None,
    element_provenance: tuple[ObligationOutcome, ...] = (),
) -> LiabilityEvaluation:
    """Run one instance to a `LiabilityEvaluation`, under an already-derived completion judgement.

    `completion` is an input, not something computed here: deriving it is `completion.
    resolve_completion()`'s job, and (step 6C) co-principal attribution runs before that derivation
    (section 18) by producing a new `CaseTruths` for `resolve_completion()` to read -- see
    `runtime/participation.py`. Passing it in keeps the "who did what" and "what does the law
    require" decisions outside the stage machinery.

    Assumes an already type-checked registry and a successfully compiled offense, exactly as
    `evaluate.evaluate()` and `relations.evaluate_compiled_offense()` do.
    """
    if completion.state in ("unresolved", "not_applicable") or completion.punishable is False:
        return _stopped(instance, completion, "completion", elements=not_reached())

    elements, decisive_obligation = _resolve_elements(
        compiled,
        instance,
        completion,
        truths,
        element_truth_overrides=element_truth_overrides,
        element_provenance=element_provenance,
    )
    return resolve_from_elements(
        registry, active, instance, completion, truths, elements, decisive_obligation
    )


def resolve_from_elements(
    registry: DefinitionRegistry,
    active: ActiveDoctrineRefs,
    instance: OffenseInstanceKey,
    completion: CompletionResult | None,
    truths: CaseTruths,
    elements: StageResult,
    decisive_obligation: Obligation | None,
) -> LiabilityEvaluation:
    """The one place Unlawfulness -> Culpability -> Punishability runs, given an already-computed
    Elements stage.

    Two callers, step 6C: the direct/co-principal path (`resolve_liability` above, `elements` built
    from slot+relation obligations, `completion` always a real `CompletionResult`) and the
    derivative-participation path (`runtime.participation.resolve_derivative_liability`, `elements`
    built from a principal-dependency + own-requirement obligation pair, `completion` always
    `None` -- accessories never derive one). `completion` is never branched on here, only threaded
    through to `_stopped()`/the final `LiabilityEvaluation` -- accepting `None` is a pure type
    widening, not a logic change.
    """
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
    completion: CompletionResult | None,
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
    *,
    element_truth_overrides: Mapping[str, TruthValue] | None = None,
    element_provenance: tuple[ObligationOutcome, ...] = (),
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
    outcomes = tuple(
        _iter_obligations(
            compiled,
            instance,
            completion,
            truths,
            element_truth_overrides=element_truth_overrides,
            element_provenance=element_provenance,
        )
    )
    elements_truth = fold_all(outcome.truth for outcome in outcomes)
    failed = [outcome.obligation for outcome in outcomes if outcome.truth == FALSE]

    stage = StageResult(
        evaluation_state="evaluated",
        legal_state=ELEMENTS_STATE.get(elements_truth, "unresolved"),
        gate_state=ELEMENTS_GATE.get(elements_truth, "unresolved"),
        provenance=outcomes,
    )
    return stage, decisive_obligation(failed)


def _iter_obligations(
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    truths: CaseTruths,
    *,
    element_truth_overrides: Mapping[str, TruthValue] | None = None,
    element_provenance: tuple[ObligationOutcome, ...] = (),
) -> Iterator[ObligationOutcome]:
    """The obligations this completion state actually imposes.

    A suspended slot or relation is DROPPED from the iteration, not yielded as TRUE. The difference
    is not cosmetic: substituting TRUE would rewrite a FALSE result into a satisfied element, which
    is the exact move section 14 forbids, and it would also be indistinguishable from the
    evaluator's genuine vacuous-truth case (an un-authored, empty slot).
    """
    predicate_view: Mapping[str, TruthValue] = truths.predicate_view(instance)
    if element_truth_overrides:
        predicate_view = _PredicateViewWithOverrides(predicate_view, element_truth_overrides)
    relation_view = truths.relation_view(instance)

    yield from element_provenance

    if completion.component_suspended_slots:
        yield from _iter_component_scoped_slot_obligations(compiled, instance, completion, truths)
    else:
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
        requirement_view: Mapping[str, TruthValue] = predicate_view
        if completion.additional_requirements_instance is not None:
            requirement_view = truths.predicate_view(completion.additional_requirements_instance)
        yield ObligationOutcome(
            obligation=CompletionRequirementObligation(state=completion.state),
            truth=evaluate(completion.additional_requirements, requirement_view),
        )


def _iter_component_scoped_slot_obligations(
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    truths: CaseTruths,
) -> Iterator[ObligationOutcome]:
    """Evaluate offense-family component contributions separately when Article 339 suspends one.

    The normal path intentionally evaluates merged top-level slots once.  This branch is narrower:
    it is reachable only through a checked component suspension and reads each offense-family
    component's
    existing OffenseInstanceKey predicate view.  No component truth store or general nested
    completion framework is introduced.
    """
    for component in compiled.components:
        if (
            component.component_kind != "offense"
            or component.resolved_kind not in ("offense", "derived_offense")
        ):
            raise ValueError(
                "component-scoped completion requires offense-family components; "
                f"found {component.local_key!r} on {compiled.id!r}"
            )
        component_instance = component_instance_for(
            compiled, instance, component.local_key, component.source_ref
        )
        predicate_view = truths.predicate_view(component_instance)
        suspended = completion.component_suspended_slots.get(component.local_key, frozenset())
        for slot in SLOT_NAMES:
            if slot in completion.suspended_slots or slot in suspended:
                continue
            yield ObligationOutcome(
                obligation=ComponentSlotObligation(local_key=component.local_key, slot=slot),
                truth=evaluate(component.compiled_content.slots.get(slot), predicate_view),
            )


def decisive_obligation(failed: list[Obligation]) -> Obligation | None:
    """Exactly one FALSE obligation names itself; several name none.

    No ranking is introduced to break the tie (v2.2.0 section 14 keeps semantic scheduling out of
    the runtime). Every failure stays in `provenance` either way.

    Public since step 6C: `runtime/participation.py`'s derivative Elements builder folds exactly
    two obligations (principal-dependency, own-requirement) and needs the same "exactly one FALSE
    names itself" rule -- same promotion precedent as `ELEMENTS_STATE`/`ELEMENTS_GATE` above.
    """
    return failed[0] if len(failed) == 1 else None


def _decisive_doctrine(stage: StageResult) -> str | None:
    """The doctrine that closed this gate, when exactly one did."""
    firing = [effect.doctrine_ref for effect in stage.effects if effect.truth == TRUE]
    return firing[0] if len(firing) == 1 else None
