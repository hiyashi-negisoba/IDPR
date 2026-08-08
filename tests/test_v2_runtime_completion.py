"""build-order step 6B -- idpr.v2.runtime.completion: deriving CompletionResult from case truths.

The point of these tests is not that the derivation returns the right label; it is that the
derivation has no ordering in it. Every test below would still pass if the states were declared in
a different order, and several would fail if any fallback or priority were reintroduced.
"""

from __future__ import annotations

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime.completion import (
    CompletionResult,
    completion_policy_for,
    resolve_completion,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

_HOMICIDE_ROBBERY = "derived_offense.robbery_homicide"
_INJURY = "offense.injury"


def _registry() -> DefinitionRegistry:
    return load_definitions()


def _compiled(registry, ref):
    compiled = compilemod.compile_offense(registry, ref)
    assert isinstance(compiled, compilemod.CompiledOffense), compiled
    return compiled


def _instance(ref: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("C1", "甲", ref, "o1")


def _resolve(ref: str, **predicate_truths) -> CompletionResult:
    registry = _registry()
    instance = _instance(ref)
    truths = CaseTruths(
        predicate={(instance, name): value for name, value in predicate_truths.items()}
    )
    return resolve_completion(
        completion_policy_for(registry, ref), _compiled(registry, ref), instance, truths
    )


# --------------------------------------------------------------------------------------------
# the derivation rule
# --------------------------------------------------------------------------------------------


def test_completed_and_attempted_are_derived_from_truths_not_from_each_others_failure():
    """The reason the whole `FormProgram` layer was removed.

    Both states are derived from the same case truths by their own `when`. Neither reads the
    other's result, so `attempted` can never be reached as a fallback from `completed` failing --
    the `completed offense failed -> attach attempt label` pattern section 14 forbids is not merely
    unused here, it is unexpressible.
    """
    completed = _resolve(
        _HOMICIDE_ROBBERY,
        **{
            "ground_fact.death_of_victim": TRUE,
            "ground_fact.attempt_commencement": TRUE,
        },
    )
    attempted = _resolve(
        _HOMICIDE_ROBBERY,
        **{
            "ground_fact.death_of_victim": FALSE,
            "ground_fact.attempt_commencement": TRUE,
        },
    )

    assert completed.state == "completed"
    assert attempted.state == "attempted"
    # In the completed case the attempt condition evaluated FALSE on its own merits -- it was not
    # skipped because completed won.
    assert dict((o.state, o.truth) for o in completed.provenance)["attempted"] == FALSE


def test_confirmed_true_state_decides_despite_other_unknown_conditions():
    """|T| == 1 terminates regardless of U -- the same three-valued principle as doctrine pools.

    Uses independently-worded conditions on purpose. The shipped fixtures are authored so that a
    TRUE `completed` forces the others FALSE (they share the negated result predicate), which is
    good authoring but would never exercise this rule. The conservative alternative (any UNKNOWN ->
    unresolved) would collapse ordinary cases the moment an evaluative predicate like 위험성 went
    unassessed -- the failure mode step 6A's first draft had.
    """
    result = _resolve_with_states(
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
            },
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
                "punishable": True,
                "suspends": ["result"],
            },
        },
        **{
            "ground_fact.injury_occurred": TRUE,
            "ground_fact.attempt_commencement": UNKNOWN,
        },
    )

    assert result.state == "completed"
    assert dict((o.state, o.truth) for o in result.provenance)["attempted"] == UNKNOWN


def test_two_true_conditions_yield_unresolved_never_a_priority_winner():
    """Overlapping conditions are an authoring defect, reported -- not resolved by ranking."""
    result = _resolve_with_states(
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
            },
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
                "suspends": ["result"],
            },
        },
        **{"ground_fact.injury_occurred": TRUE},
    )

    assert result.state == "unresolved"
    assert sorted(o.state for o in result.provenance if o.truth == TRUE) == [
        "attempted",
        "completed",
    ]


def test_no_condition_true_and_none_unknown_is_not_applicable():
    """Everything known, nothing matches: this offense has no completion state here at all."""
    result = _resolve(
        _INJURY,
        **{
            "ground_fact.injury_occurred": FALSE,
            "ground_fact.attempt_commencement": FALSE,
            "legal_element.impossibility_without_danger": FALSE,
        },
    )

    assert result.state == "not_applicable"


def test_missing_truths_yield_unresolved_not_not_applicable():
    """Section 4.3 again: absent evidence is not negation, so an unassessed case is unresolved."""
    result = _resolve(_INJURY)

    assert result.state == "unresolved"


def test_derivation_is_symmetric_under_declaration_order():
    """No hidden priority: permuting the states in the policy changes nothing."""
    registry = _registry()
    ref = _INJURY
    policy = completion_policy_for(registry, ref)
    reversed_states = dict(reversed(list(policy.payload["states"].items())))
    permuted = DefinitionEntry(
        id=policy.id,
        kind=policy.kind,
        payload={**policy.payload, "states": reversed_states},
        source_file=policy.source_file,
    )
    instance = _instance(ref)
    truths = CaseTruths(
        predicate={
            (instance, "ground_fact.injury_occurred"): FALSE,
            (instance, "ground_fact.attempt_commencement"): TRUE,
            (instance, "legal_element.impossibility_without_danger"): FALSE,
        }
    )
    compiled = _compiled(registry, ref)

    original = resolve_completion(policy, compiled, instance, truths)
    permuted_result = resolve_completion(permuted, compiled, instance, truths)

    assert original.state == permuted_result.state == "attempted"


# --------------------------------------------------------------------------------------------
# what a derived state carries
# --------------------------------------------------------------------------------------------


def test_attempted_state_carries_suspensions_and_the_authored_relation_disposition():
    """강도살인미수: result+causation suspended, yet occasion_identity RETAINED.

    This is the fixture that rules out inferring relation dispositions from slot topology -- 강도의
    기회에 살해행위가 있었을 것은 미수에서도 요구되므로, "suspended slot에 닿는 relation은
    suspend" 같은 규칙이었다면 정확히 반대 답을 냈을 것이다.
    """
    result = _resolve(
        _HOMICIDE_ROBBERY,
        **{
            "ground_fact.death_of_victim": FALSE,
            "ground_fact.attempt_commencement": TRUE,
        },
    )

    assert result.state == "attempted"
    assert result.punishable is True
    assert result.suspended_slots == frozenset({"result", "causation"})
    assert list(result.relation_dispositions.values()) == ["retain"]
    assert next(iter(result.relation_dispositions)).relation_ref == "relation.occasion_identity"
    assert result.additional_requirements == ("ref", "ground_fact.attempt_commencement")


def test_non_punishable_state_is_derived_and_named_not_silently_dropped():
    """불능범: the case IS an impossible attempt; that it carries no punishment is a separate fact.

    Omitting the state from the policy would have said something different -- that this offense has
    no such legal state at all -- and would have left the runtime with nothing to report.
    """
    result = _resolve(
        _INJURY,
        **{
            "ground_fact.injury_occurred": FALSE,
            "ground_fact.attempt_commencement": TRUE,
            "legal_element.impossibility_without_danger": TRUE,
        },
    )

    assert result.state == "impossible_attempt"
    assert result.punishable is False


def test_offense_without_a_completion_policy_resolves_to_completed():
    """Most offenses have no CompletionPolicyDef; that is not the same as having no state."""
    registry = _registry()
    ref = "offense.embezzlement"
    instance = _instance(ref)

    assert completion_policy_for(registry, ref) is None
    result = resolve_completion(None, _compiled(registry, ref), instance, CaseTruths())

    assert result.state == "completed"
    assert result.suspended_slots == frozenset()


# --------------------------------------------------------------------------------------------
# invariants
# --------------------------------------------------------------------------------------------


def test_unresolved_completion_result_carries_no_program():
    """A judgement that was never reached cannot suspend obligations.

    Without the invariant, `CompletionResult("unresolved", suspended_slots={"result"})` constructs
    happily and the pipeline would drop an obligation on the authority of nothing.
    """
    for kwargs in (
        {"punishable": True},
        {"suspended_slots": frozenset({"result"})},
        {"additional_requirements": ("ref", "ground_fact.attempt_commencement")},
    ):
        with pytest.raises(ValueError):
            CompletionResult(state="unresolved", **kwargs)
    with pytest.raises(ValueError):
        CompletionResult(state="not_applicable", punishable=False)


def test_derived_state_must_carry_punishability():
    with pytest.raises(ValueError):
        CompletionResult(state="attempted")


def _resolve_with_states(states: dict, **predicate_truths) -> CompletionResult:
    """Run the derivation against a synthetic `states` block on offense.injury's policy.

    Used only for conditions the shipped fixtures cannot produce (independently-worded or
    overlapping conditions), so that the derivation rule is tested on the inputs that actually
    exercise it rather than on inputs the fixtures happen to make unreachable.
    """
    registry = _registry()
    policy = completion_policy_for(registry, _INJURY)
    synthetic = DefinitionEntry(
        id=policy.id,
        kind=policy.kind,
        payload={**policy.payload, "states": states},
        source_file=policy.source_file,
    )
    instance = _instance(_INJURY)
    truths = CaseTruths(
        predicate={(instance, name): value for name, value in predicate_truths.items()}
    )
    return resolve_completion(synthetic, _compiled(registry, _INJURY), instance, truths)
