"""build-order step 6C -- idpr.v2.runtime.participation: ATTRIBUTE (co-principal), the 3-valued
principal-realization read, and derivative (instigator/aider) liability."""

from __future__ import annotations

from idpr.v2 import compile as compilemod
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation import (
    apply_attribution,
    principal_realization_truth,
    resolve_derivative_liability,
)
from idpr.v2.runtime.pipeline import resolve_liability
from idpr.v2.runtime.stages import (
    LiabilityEvaluation,
    OffenseRealization,
    ParticipationDependencyObligation,
    ParticipationRequirementObligation,
    StageResult,
    not_reached,
)
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.participation import participation_policy_for
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

_GAP = OffenseInstanceKey("C1", "甲", "offense.robbery", "o1")
_EUL = OffenseInstanceKey("C1", "乙", "offense.robbery", "o1")

_ROBBERY_REFS = (
    "ground_fact.property_taking",
    "legal_element.robbery_level_violence",
    "legal_element.appropriation_intent",
)


def _compiled(registry=None):
    registry = registry or load_definitions()
    compiled = compilemod.compile_offense(registry, "offense.robbery")
    assert isinstance(compiled, compilemod.CompiledOffense), compiled
    return compiled


def _completed() -> CompletionResult:
    return CompletionResult(state="completed", punishable=True)


# --------------------------------------------------------------------------------------------
# apply_attribution -- slot-scoped, predicate-level, fold_any merge (decisions #1/#2)
# --------------------------------------------------------------------------------------------


def test_attribution_only_touches_leaves_of_attributable_slots() -> None:
    registry = load_definitions()
    compiled = _compiled(registry)
    truths = CaseTruths(
        predicate={
            (_GAP, "legal_element.appropriation_intent"): TRUE,
            (_EUL, "legal_element.appropriation_intent"): FALSE,
        }
    )
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    # "mental" is not in participation_policy.standard's attributable_slots ([conduct]) -- 甲's own
    # value must survive untouched even though 乙's differs.
    assert attributed.predicate[(_GAP, "legal_element.appropriation_intent")] == TRUE


def test_attribution_merges_conduct_leaves_with_fold_any() -> None:
    registry = load_definitions()
    compiled = _compiled(registry)
    truths = CaseTruths(
        predicate={
            (_GAP, "ground_fact.property_taking"): FALSE,
            (_EUL, "ground_fact.property_taking"): TRUE,
        }
    )
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    # 乙 performed the taking; 일부실행 전부책임 -- 甲's attributed view sees it as TRUE too.
    assert attributed.predicate[(_GAP, "ground_fact.property_taking")] == TRUE


def test_attribution_target_already_true_stays_true_even_if_source_false() -> None:
    registry = load_definitions()
    compiled = _compiled(registry)
    truths = CaseTruths(
        predicate={
            (_GAP, "legal_element.robbery_level_violence"): TRUE,
            (_EUL, "legal_element.robbery_level_violence"): FALSE,
        }
    )
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    assert attributed.predicate[(_GAP, "legal_element.robbery_level_violence")] == TRUE


def test_attribution_both_unknown_stays_unknown() -> None:
    registry = load_definitions()
    compiled = _compiled(registry)
    truths = CaseTruths(predicate={})
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    assert attributed.predicate[(_GAP, "ground_fact.property_taking")] == UNKNOWN


def test_attribution_returns_a_new_case_truths_original_untouched() -> None:
    registry = load_definitions()
    compiled = _compiled(registry)
    original_predicate = {
        (_GAP, "ground_fact.property_taking"): FALSE,
        (_EUL, "ground_fact.property_taking"): TRUE,
    }
    truths = CaseTruths(predicate=dict(original_predicate))
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    assert attributed is not truths
    assert dict(truths.predicate) == original_predicate


def _rebuild(by_kind: dict) -> DefinitionRegistry:
    by_id: dict = {}
    frozen = {}
    for kind, entries in by_kind.items():
        frozen[kind] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen)


def _mutate_offense(registry: DefinitionRegistry, offense_id: str, mutator) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    for index, entry in enumerate(by_kind["offense"]):
        if entry.id == offense_id:
            payload = dict(entry.payload)
            mutator(payload)
            by_kind["offense"][index] = DefinitionEntry(
                id=payload["id"], kind="offense", payload=payload, source_file=entry.source_file
            )
            break
    else:
        raise KeyError(offense_id)
    return _rebuild(by_kind)


def test_attribution_is_a_noop_without_a_participation_policy() -> None:
    registry = load_definitions()
    by_kind = {k: v for k, v in registry.by_kind.items() if k != "participation_policy"}
    registry = _rebuild(by_kind)
    compiled = _compiled(registry)
    truths = CaseTruths(predicate={(_EUL, "ground_fact.property_taking"): TRUE})
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    assert attributed is truths


def test_attribution_is_a_noop_when_co_principal_disabled_for_this_offense() -> None:
    registry = _mutate_offense(
        load_definitions(), "offense.robbery",
        lambda p: p.__setitem__("participation_constraints", {"disabled_modes": ["co_principal"]}),
    )
    compiled = _compiled(registry)
    truths = CaseTruths(predicate={(_EUL, "ground_fact.property_taking"): TRUE})
    attributed = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    assert attributed is truths


def test_attribution_end_to_end_turns_a_failed_element_into_a_satisfied_one() -> None:
    """The money test for decisions #1/#2 together: apply_attribution -> resolve_completion (via
    the ordinary no-policy `completed` default, unchanged) -> resolve_liability, all fed exactly as
    they exist today -- 甲's own conduct fails, attribution from 乙 makes it pass."""
    registry = load_definitions()
    compiled = _compiled(registry)
    truths = CaseTruths(
        predicate={
            (_GAP, "ground_fact.property_taking"): FALSE,
            (_GAP, "legal_element.robbery_level_violence"): TRUE,
            (_GAP, "legal_element.appropriation_intent"): TRUE,
            (_EUL, "ground_fact.property_taking"): TRUE,
        }
    )

    unattributed = resolve_liability(registry, compiled, _GAP, _completed(), frozenset(), truths)
    assert unattributed.elements.gate_state == "fails"
    assert unattributed.liability_result is None

    attributed_truths = apply_attribution(registry, compiled, "offense.robbery", _GAP, [_EUL], truths)
    attributed = resolve_liability(registry, compiled, _GAP, _completed(), frozenset(), attributed_truths)
    assert attributed.elements.gate_state == "passes"
    assert attributed.liability_result is not None


# --------------------------------------------------------------------------------------------
# principal_realization_truth -- the 3-valued read (decision #4)
# --------------------------------------------------------------------------------------------


def _principal(
    *,
    realization=None,
    completion=None,
    elements=None,
    unlawfulness=None,
) -> LiabilityEvaluation:
    return LiabilityEvaluation(
        instance=_GAP,
        completion=completion if completion is not None else _completed(),
        elements=elements if elements is not None else not_reached(),
        unlawfulness=unlawfulness if unlawfulness is not None else not_reached(),
        culpability=not_reached(),
        punishability=not_reached(),
        realization=realization,
    )


def test_principal_realization_truth_true_when_realization_exists() -> None:
    elements = StageResult(evaluation_state="evaluated", legal_state="satisfied", gate_state="passes")
    unlawfulness = StageResult(evaluation_state="evaluated", legal_state="preserved", gate_state="passes")
    principal = _principal(
        realization=OffenseRealization(instance=_GAP, elements=elements, unlawfulness=unlawfulness),
        elements=elements,
        unlawfulness=unlawfulness,
    )
    assert principal_realization_truth(principal) == TRUE


def test_principal_realization_truth_false_when_elements_confirmed_failed() -> None:
    elements = StageResult(evaluation_state="evaluated", legal_state="failed", gate_state="fails")
    principal = _principal(elements=elements)
    assert principal_realization_truth(principal) == FALSE


def test_principal_realization_truth_unknown_when_elements_unresolved() -> None:
    elements = StageResult(evaluation_state="evaluated", legal_state="unresolved", gate_state="unresolved")
    principal = _principal(elements=elements)
    assert principal_realization_truth(principal) == UNKNOWN


def test_principal_realization_truth_false_when_unlawfulness_confirmed_defeated() -> None:
    elements = StageResult(evaluation_state="evaluated", legal_state="satisfied", gate_state="passes")
    unlawfulness = StageResult(evaluation_state="evaluated", legal_state="defeated", gate_state="fails")
    principal = _principal(elements=elements, unlawfulness=unlawfulness)
    assert principal_realization_truth(principal) == FALSE


def test_principal_realization_truth_unknown_when_unlawfulness_unresolved() -> None:
    elements = StageResult(evaluation_state="evaluated", legal_state="satisfied", gate_state="passes")
    unlawfulness = StageResult(evaluation_state="evaluated", legal_state="unresolved", gate_state="unresolved")
    principal = _principal(elements=elements, unlawfulness=unlawfulness)
    assert principal_realization_truth(principal) == UNKNOWN


def test_principal_realization_truth_false_when_completion_not_applicable() -> None:
    principal = _principal(completion=CompletionResult(state="not_applicable"))
    assert principal_realization_truth(principal) == FALSE


def test_principal_realization_truth_unknown_when_completion_unresolved() -> None:
    principal = _principal(completion=CompletionResult(state="unresolved"))
    assert principal_realization_truth(principal) == UNKNOWN


def test_principal_realization_truth_unknown_when_completion_not_punishable() -> None:
    # Elements were never computed for this shape at all (section 24) -- genuinely unknown, not a
    # confirmed non-event. The flagged reading from the plan.
    principal = _principal(completion=CompletionResult(state="preparation", punishable=False))
    assert principal_realization_truth(principal) == UNKNOWN


def test_principal_realization_truth_falls_through_when_principal_completion_is_none() -> None:
    # Chained participation: the principal was itself resolved via resolve_derivative_liability,
    # so principal.completion is None. The read must fall through to elements/unlawfulness.
    elements = StageResult(evaluation_state="evaluated", legal_state="failed", gate_state="fails")
    principal = LiabilityEvaluation(
        instance=_GAP,
        completion=None,
        elements=elements,
        unlawfulness=not_reached(),
        culpability=not_reached(),
        punishability=not_reached(),
    )
    assert principal_realization_truth(principal) == FALSE


# --------------------------------------------------------------------------------------------
# resolve_derivative_liability -- decision #3
# --------------------------------------------------------------------------------------------

_TEO = OffenseInstanceKey("C1", "丙", "offense.robbery", "o1")  # 丙: the instigator


def _principal_truths(realized: bool) -> dict:
    if realized:
        return {(_GAP, ref): TRUE for ref in _ROBBERY_REFS}
    return {(_GAP, ref): FALSE for ref in _ROBBERY_REFS}


def _resolved_principal(realized: bool, registry) -> LiabilityEvaluation:
    compiled = _compiled(registry)
    truths = CaseTruths(predicate=_principal_truths(realized))
    return resolve_liability(registry, compiled, _GAP, _completed(), frozenset(), truths)


def test_derivative_liability_reaches_full_result_through_the_shared_tail() -> None:
    registry = load_definitions()
    policy = participation_policy_for(registry)
    principal = _resolved_principal(True, registry)
    assert principal.realization is not None  # sanity: principal truly realized

    truths = CaseTruths(predicate={(_TEO, "ground_fact.instigation_conduct"): TRUE})
    evaluation = resolve_derivative_liability(
        registry, policy, "instigator", principal, _TEO, frozenset(), truths
    )
    assert evaluation.completion is None
    assert evaluation.decisive_stage is None
    assert evaluation.liability_result is not None
    assert evaluation.establishment is not None
    assert evaluation.realization is not None


def test_derivative_liability_stops_at_elements_when_own_requirement_false() -> None:
    registry = load_definitions()
    policy = participation_policy_for(registry)
    principal = _resolved_principal(True, registry)

    truths = CaseTruths(predicate={(_TEO, "ground_fact.instigation_conduct"): FALSE})
    evaluation = resolve_derivative_liability(
        registry, policy, "instigator", principal, _TEO, frozenset(), truths
    )
    assert evaluation.decisive_stage == "elements"
    assert evaluation.decisive_obligation == ParticipationRequirementObligation(mode="instigator")
    assert evaluation.completion is None


def test_derivative_liability_stops_at_elements_when_principal_not_realized() -> None:
    registry = load_definitions()
    policy = participation_policy_for(registry)
    principal = _resolved_principal(False, registry)
    assert principal.realization is None  # sanity: principal did not realize

    truths = CaseTruths(predicate={(_TEO, "ground_fact.instigation_conduct"): TRUE})
    evaluation = resolve_derivative_liability(
        registry, policy, "instigator", principal, _TEO, frozenset(), truths
    )
    assert evaluation.decisive_stage == "elements"
    assert evaluation.decisive_obligation == ParticipationDependencyObligation(mode="instigator")
