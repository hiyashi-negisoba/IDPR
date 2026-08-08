"""Stage execution for one actor/offense occurrence (build-order step 6A).

    Elements -> Unlawfulness -> [OffenseRealization] -> Culpability
             -> [OffenseEstablishment] -> Punishability -> [LiabilityResult]

Once a gate does not pass, the remaining stages are `not_reached` and are NOT speculatively
evaluated (v2.2.0 section 24: alternative reasoning is a generation-layer operation, never a
symbolic execution mode). "Does not pass" covers `unresolved` as well as `fails` -- an unresolved
Unlawfulness does not license reasoning about culpability.

Execution order note for step 6C, fixed here so it does not get rediscovered: ATTRIBUTE precedes
Completion, which precedes Elements (v2.2.0 section 18). Co-principal attribution can change which
form is even reached, so it cannot be applied afterwards. File order (completion before
participation) is unrelated to execution order.
"""

from __future__ import annotations

from typing import Iterator

from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import FALSE, TRUE, evaluate, fold_all
from idpr.v2.expressions import SLOT_NAMES
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.relations import evaluate_relation, iter_relation_instances
from idpr.v2.runtime.effects import ActiveDoctrineRefs, resolve_stage
from idpr.v2.runtime.identity import OffenseFormKey, OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.stages import (
    FormProgram,
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
    program: FormProgram,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Run one instance/form to a `LiabilityEvaluation`.

    Assumes an already type-checked registry and a successfully compiled offense, exactly as
    `evaluate.evaluate()` and `relations.evaluate_compiled_offense()` do.
    """
    _reject_unimplemented_form(program)
    form_key = OffenseFormKey(instance=instance, form=program.form)

    elements, decisive_obligation = _resolve_elements(compiled, instance, truths)
    if elements.gate_state != "passes":
        return _stopped(
            form_key,
            "elements",
            elements=elements,
            decisive_obligation=decisive_obligation,
        )

    unlawfulness = resolve_stage("unlawfulness", active, registry, instance, truths)
    if unlawfulness.gate_state != "passes":
        return _stopped(form_key, "unlawfulness", elements=elements, unlawfulness=unlawfulness)

    realization = OffenseRealization(
        form_key=form_key, elements=elements, unlawfulness=unlawfulness
    )

    culpability = resolve_stage("culpability", active, registry, instance, truths)
    if culpability.gate_state != "passes":
        return _stopped(
            form_key,
            "culpability",
            elements=elements,
            unlawfulness=unlawfulness,
            culpability=culpability,
            realization=realization,
        )

    establishment = OffenseEstablishment(
        form_key=form_key, realization=realization, culpability=culpability
    )

    punishability = resolve_stage("punishability", active, registry, instance, truths)
    if punishability.gate_state != "passes":
        return _stopped(
            form_key,
            "punishability",
            elements=elements,
            unlawfulness=unlawfulness,
            culpability=culpability,
            punishability=punishability,
            realization=realization,
            establishment=establishment,
        )

    return LiabilityEvaluation(
        form_key=form_key,
        elements=elements,
        unlawfulness=unlawfulness,
        culpability=culpability,
        punishability=punishability,
        realization=realization,
        establishment=establishment,
        liability_result=LiabilityResult(
            form_key=form_key, establishment=establishment, punishability=punishability
        ),
        decisive_stage=None,
    )


def _stopped(
    form_key: OffenseFormKey,
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
        form_key=form_key,
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


def _reject_unimplemented_form(program: FormProgram) -> None:
    """Refuse a form whose semantics step 6B has not landed yet, rather than ignoring the fields.

    Accepting `suspended_slots` and evaluating every slot anyway would be the worst outcome: the
    caller believes a suspension took effect and gets a wrong answer with no signal.
    """
    if (
        program.form != "completed"
        or program.suspended_slots
        or program.relation_dispositions
        or program.extra is not None
    ):
        raise NotImplementedError(
            f"form program {program.form!r} needs completion semantics (build-order step 6B); "
            "step 6A evaluates the completed form only and will not silently ignore "
            "suspended_slots / relation_dispositions / extra"
        )


def _resolve_elements(
    compiled: CompiledOffense, instance: OffenseInstanceKey, truths: CaseTruths
) -> tuple[StageResult, Obligation | None]:
    """Elements as an aggregation over individually-recorded obligations.

    The fold is `fold_all` over exactly the same multiset of truths that
    `relations.evaluate_compiled_offense()` folds, so the resulting TruthValue is identical (a
    regression test pins that). Obligations are evaluated one by one only so a decisive one can be
    named -- not to re-derive the semantics.

    Elements carries no `effects`: section 12.1 keeps doctrines off this stage entirely, and the
    schema's DoctrineDef stage enum has no `elements` member.
    """
    outcomes = tuple(_iter_obligations(compiled, instance, truths))
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
    compiled: CompiledOffense, instance: OffenseInstanceKey, truths: CaseTruths
) -> Iterator[ObligationOutcome]:
    predicate_view = truths.predicate_view(instance)
    relation_view = truths.relation_view(instance)

    for slot in SLOT_NAMES:
        yield ObligationOutcome(
            obligation=SlotObligation(slot=slot),
            truth=evaluate(compiled.slots.get(slot), predicate_view),
        )
    for key, _binding in iter_relation_instances(compiled):
        yield ObligationOutcome(
            obligation=RelationObligation(
                key=RuntimeRelationKey(instance=instance, definition_key=key)
            ),
            truth=evaluate_relation(key, relation_view),
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
