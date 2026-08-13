"""r12_p2_q1_ga / r10_p2_q1 shape: 甲이 乙을 노렸는데 결과가 C에게 발생한 사안."""

from pathlib import Path

import pytest

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.mistake import (
    MistakeFinding,
    MistakePolicyError,
    apply_mistake_policy,
)
from idpr.v2.runtime.truths import CaseTruths

INTENT = "legal_element.intent"
ACTUAL = OffenseInstanceKey("case", "甲", "offense.injury", "binding:002")


@pytest.fixture(scope="module")
def policy():
    registry = load_definitions(Path("data/v2/definitions"))
    return registry.get("mistake_policy.korean_law_concrete_fact")


def _truths(intent_truth=FALSE) -> CaseTruths:
    return CaseTruths(predicate={(ACTUAL, INTENT): intent_truth})


def _finding(**overrides) -> MistakeFinding:
    values = {
        "instance": ACTUAL,
        "divergence_truth": TRUE,
        "divergence_kind_truth": TRUE,
        "intent_toward_intended_object": TRUE,
    }
    values.update(overrides)
    return MistakeFinding(**values)


def test_object_misidentification_preserves_intent_toward_the_actual_victim(policy) -> None:
    """Call 2 rightly says 甲 had no intent toward C; 법정적 부합설 attributes it anyway."""
    result = apply_mistake_policy(_truths(), [_finding()], policy=policy)
    assert result.predicate[(ACTUAL, INTENT)] == TRUE


def test_method_divergence_takes_the_same_branch_under_statutory_conformity(policy) -> None:
    result = apply_mistake_policy(
        _truths(), [_finding(divergence_kind_truth=FALSE)], policy=policy
    )
    assert result.predicate[(ACTUAL, INTENT)] == TRUE


def test_without_divergence_the_policy_is_silent(policy) -> None:
    """An ordinary case must not have its intent rewritten just because a policy exists."""
    for divergence in (FALSE, UNKNOWN):
        result = apply_mistake_policy(
            _truths(), [_finding(divergence_truth=divergence)], policy=policy
        )
        assert result.predicate[(ACTUAL, INTENT)] == FALSE


def test_no_intent_toward_the_intended_object_means_nothing_to_attribute(policy) -> None:
    """부합설은 있는 고의를 옮기는 법리이지, 없는 고의를 만드는 법리가 아니다."""
    for intent in (FALSE, UNKNOWN):
        result = apply_mistake_policy(
            _truths(), [_finding(intent_toward_intended_object=intent)], policy=policy
        )
        assert result.predicate[(ACTUAL, INTENT)] == FALSE


def test_unknown_divergence_kind_is_preserved_not_repaired(policy) -> None:
    truths = _truths(intent_truth=UNKNOWN)
    result = apply_mistake_policy(
        truths, [_finding(divergence_kind_truth=UNKNOWN)], policy=policy
    )
    assert result.predicate[(ACTUAL, INTENT)] == UNKNOWN


def test_the_original_truths_are_never_mutated(policy) -> None:
    truths = _truths()
    apply_mistake_policy(truths, [_finding()], policy=policy)
    assert truths.predicate[(ACTUAL, INTENT)] == FALSE


def test_the_policy_refines_a_planned_target_and_never_adds_one(policy) -> None:
    unplanned = OffenseInstanceKey("case", "甲", "offense.injury", "binding:999")
    with pytest.raises(MistakePolicyError, match="never assessed"):
        apply_mistake_policy(_truths(), [_finding(instance=unplanned)], policy=policy)


def test_a_non_mistake_definition_is_rejected() -> None:
    registry = load_definitions(Path("data/v2/definitions"))
    with pytest.raises(MistakePolicyError, match="not a mistake policy"):
        apply_mistake_policy(_truths(), [], policy=registry.get("offense.injury"))
