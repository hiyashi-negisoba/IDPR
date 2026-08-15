"""공범의 초과 후보. 2026-08-13 검수로 join이 factual episode에서 참가 링크로 바뀌었다.

교사행위와 정범의 실행은 시간적으로 분리되는 것이 정상이고, 판례가 찾는 것은 "교사행위로
정범이 실행을 결의하고 실제 실행했는가"라는 연결관계다. 그 연결은 derivative link가 이미
확정했으므로 여기서 episode 일치를 다시 요구하지 않는다.
"""

from pathlib import Path

import pytest

from idpr.v2.evaluate import UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.excess import QUANTITATIVE_ORDINARY, classify_excess
from idpr.v2.runtime.excess_candidates import (
    ExcessCandidateError,
    plan_accessory_excess_candidates,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

ORDER = ("factual_episode:001", "factual_episode:002", "factual_episode:003")
ACCESSORY = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")
PRINCIPAL = OffenseInstanceKey("case", "乙", "offense.theft", "binding:002")
REALIZED = OffenseInstanceKey("case", "乙", "derived_offense.special_theft", "binding:003")
LINK = (ACCESSORY, PRINCIPAL, "instigator")


def _plan(links, established, episodes, order=ORDER):
    return plan_accessory_excess_candidates(
        links, established, episode_by_instance=episodes, episode_order=order
    )


def test_the_instigation_and_the_execution_may_sit_in_different_episodes() -> None:
    """이것이 검수로 바뀐 지점이다. 예전 same-episode join은 여기서 후보를 닫았다.

    닫히면 안 되는 것은 **교사행위와 실행** 사이의 간격이다. 실행과 그 실행이 넘어선 죄는
    한 실현이므로 같은 episode에 있다.
    """
    candidates = _plan(
        (LINK,),
        (PRINCIPAL, REALIZED),
        {
            ACCESSORY: "factual_episode:001",
            PRINCIPAL: "factual_episode:002",
            REALIZED: "factual_episode:002",
        },
    )
    assert len(candidates) == 1
    assert candidates[0].instigated_offense_ref == "offense.theft"
    assert candidates[0].realized_offense_ref == "derived_offense.special_theft"


def test_a_crime_outside_the_linked_execution_is_marked_not_asserted() -> None:
    """정범이 그 실행 뒤 다른 자리에서 저지른 죄는 근거가 다르다.

    파생 경로(절도 → 특수절도)가 저작되어 있다는 것만으로 별개 실현을 앞선 교사에 묶으면
    아무도 주장하지 않은 사실을 host가 짓는 것이 된다. 그렇다고 닫으면 교사한 절도와 정범의
    상해 사이의 질적 초과 -- 실제 판례 형태 -- 가 함께 닫힌다. 판정에 필요한 "교사받은 그
    실현"의 신원을 상류가 주지 않으므로, 여기서 정하지 않고 근거의 차이를 실어 나른다.
    """
    same_execution = _plan(
        (LINK,),
        (PRINCIPAL, REALIZED),
        {
            ACCESSORY: "factual_episode:001",
            PRINCIPAL: "factual_episode:002",
            REALIZED: "factual_episode:002",
        },
    )
    assert [value.same_execution for value in same_execution] == [True]

    later = _plan(
        (LINK,),
        (PRINCIPAL, REALIZED),
        {
            ACCESSORY: "factual_episode:001",
            PRINCIPAL: "factual_episode:002",
            REALIZED: "factual_episode:003",
        },
    )
    assert [value.same_execution for value in later] == [False]


def test_the_provenance_feeds_the_classifier_without_any_new_judgment() -> None:
    """후보의 요점: 두 값 모두 상류가 이미 정했고 여기서는 나르기만 한다."""
    registry = load_definitions(Path("data/v2/definitions"))
    policy = registry.get("excess_policy.korean_law_standard")
    candidate = _plan(
        (LINK,),
        (PRINCIPAL, REALIZED),
        {
            ACCESSORY: "factual_episode:001",
            PRINCIPAL: "factual_episode:002",
            REALIZED: "factual_episode:002",
        },
    )[0]

    assessment = classify_excess(
        registry,
        policy,
        instigated_offense_ref=candidate.instigated_offense_ref,
        realized_offense_ref=candidate.realized_offense_ref,
        participant_foreseeability=UNKNOWN,
    )
    assert assessment.classification == QUANTITATIVE_ORDINARY


def test_only_the_linked_principal_actor_can_exceed() -> None:
    """같은 사건의 다른 사람이 저지른 죄는 이 교사의 초과가 아니다."""
    other = OffenseInstanceKey("case", "丙", "offense.extortion", "binding:004")
    assert (
        _plan(
            (LINK,),
            (PRINCIPAL, other),
            {
                ACCESSORY: "factual_episode:001",
                PRINCIPAL: "factual_episode:002",
                other: "factual_episode:002",
            },
        )
        == ()
    )


def test_an_offense_before_the_linked_execution_is_not_excess() -> None:
    earlier = OffenseInstanceKey("case", "乙", "offense.extortion", "binding:005")
    assert (
        _plan(
            (LINK,),
            (PRINCIPAL, earlier),
            {
                ACCESSORY: "factual_episode:001",
                PRINCIPAL: "factual_episode:002",
                earlier: "factual_episode:001",
            },
        )
        == ()
    )


def test_realizing_exactly_what_was_instigated_produces_no_candidate() -> None:
    assert (
        _plan(
            (LINK,),
            (PRINCIPAL,),
            {ACCESSORY: "factual_episode:001", PRINCIPAL: "factual_episode:002"},
        )
        == ()
    )


def test_an_instance_without_an_episode_is_fatal() -> None:
    with pytest.raises(ExcessCandidateError, match="lack factual episode ids"):
        _plan((LINK,), (PRINCIPAL,), {ACCESSORY: "factual_episode:001"})


def test_an_unordered_episode_is_fatal() -> None:
    with pytest.raises(ExcessCandidateError, match="not ordered"):
        _plan(
            (LINK,),
            (PRINCIPAL,),
            {ACCESSORY: "factual_episode:001", PRINCIPAL: "factual_episode:009"},
        )
