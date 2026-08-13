"""공범의 초과 분류. r11_p1_q1 / r13_p1_q1 / r12_p2_q1_ga / r14_p2_q1 형태."""

from pathlib import Path

import pytest

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.excess import (
    NOT_EXCESS,
    QUALITATIVE,
    QUANTITATIVE_ORDINARY,
    QUANTITATIVE_RESULT_AGGRAVATED,
    UNRESOLVED,
    UNRESOLVED_EXCESS_RELATION,
    ExcessPolicyError,
    classify_excess,
)


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


@pytest.fixture(scope="module")
def policy(registry):
    return registry.get("excess_policy.korean_law_standard")


def _classify(registry, policy, instigated, realized, foreseeability=UNKNOWN):
    return classify_excess(
        registry,
        policy,
        instigated_offense_ref=instigated,
        realized_offense_ref=realized,
        participant_foreseeability=foreseeability,
    )


def test_theft_instigation_realized_as_special_theft_is_quantitative(registry, policy) -> None:
    """r13_p1_q1: 절도 교사에 특수절도가 실현된 양적 초과."""
    result = _classify(registry, policy, "offense.theft", "derived_offense.special_theft")
    assert result.classification == QUANTITATIVE_ORDINARY
    assert result.effect == "liable_for_instigated_scope"


def test_result_aggravated_realization_branches_on_the_participants_foreseeability(
    registry, policy
) -> None:
    """검수 ③-b. 강도 교사에 강도치사가 실현된 경우 일률적으로 기본 범위로 자르지 않는다."""
    pair = ("offense.robbery", "derived_offense.robbery_causing_death_by_aggravated_result")
    assert _classify(registry, policy, *pair, TRUE).effect == "liable_for_aggravated_result"
    assert _classify(registry, policy, *pair, FALSE).effect == "liable_for_instigated_scope"

    unknown = _classify(registry, policy, *pair, UNKNOWN)
    assert unknown.classification == QUANTITATIVE_RESULT_AGGRAVATED
    assert unknown.effect == UNRESOLVED


def test_an_unauthored_pair_is_unresolved_not_qualitative(registry, policy) -> None:
    """검수 ③-a, the decision this module exists to enforce.

    폭행치상은 v2에 저작되어 있지 않다. derivation이 없다는 이유로 질적 초과라고 판정하면
    r11_p1_q1에 대해 근거 없이 '아무 책임 없음'이라는 법적 결론을 내게 된다.
    """
    result = _classify(registry, policy, "offense.theft", "offense.dwelling_intrusion")
    assert result.classification == UNRESOLVED_EXCESS_RELATION
    assert result.effect == UNRESOLVED


def test_an_authored_incompatible_pair_is_qualitative(registry, policy) -> None:
    result = _classify(registry, policy, "offense.theft", "offense.injury")
    assert result.classification == QUALITATIVE
    assert result.effect == "no_liability_for_excess"


def test_a_compose_chain_without_the_aggravated_marker_is_not_quantitative(
    registry, policy
) -> None:
    """준강도는 절도를 딛고 서지만 폭행·협박이라는 독립한 불법이 더해진다. 사슬이 있다는
    이유만으로 '교사한 범위 안'이라고 읽으면 그 불법까지 삼킨다."""
    result = _classify(registry, policy, "offense.theft", "derived_offense.quasi_robbery")
    assert result.classification == UNRESOLVED_EXCESS_RELATION


def test_realizing_exactly_what_was_instigated_is_not_excess(registry, policy) -> None:
    result = _classify(registry, policy, "offense.theft", "offense.theft")
    assert result.classification == NOT_EXCESS


def test_a_non_excess_definition_is_rejected(registry) -> None:
    with pytest.raises(ExcessPolicyError, match="not an excess policy"):
        _classify(registry, registry.get("offense.theft"), "offense.theft", "offense.injury")
