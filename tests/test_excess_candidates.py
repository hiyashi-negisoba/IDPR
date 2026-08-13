"""r13_p1_q1 shape: 甲 was bound to 절도, 乙 realized 특수절도 in the same episode."""

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

EPISODE = "factual_episode:001"
ACCESSORY = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")
PRINCIPAL = OffenseInstanceKey("case", "乙", "derived_offense.special_theft", "derived_binding:002")


def _episodes(*instances, episode=EPISODE):
    return dict.fromkeys(instances, episode)


def test_an_accessory_and_a_differently_realizing_principal_pair_up() -> None:
    candidates = plan_accessory_excess_candidates(
        (ACCESSORY,), (PRINCIPAL,), episode_by_instance=_episodes(ACCESSORY, PRINCIPAL)
    )
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.instigated_offense_ref == "offense.theft"
    assert candidate.realized_offense_ref == "derived_offense.special_theft"


def test_the_provenance_feeds_the_classifier_without_any_new_judgment() -> None:
    """The whole point of the candidate: two values upstream already fixed, carried, not re-decided."""
    registry = load_definitions(Path("data/v2/definitions"))
    policy = registry.get("excess_policy.korean_law_standard")
    candidate = plan_accessory_excess_candidates(
        (ACCESSORY,), (PRINCIPAL,), episode_by_instance=_episodes(ACCESSORY, PRINCIPAL)
    )[0]

    assessment = classify_excess(
        registry,
        policy,
        instigated_offense_ref=candidate.instigated_offense_ref,
        realized_offense_ref=candidate.realized_offense_ref,
        participant_foreseeability=UNKNOWN,
    )
    assert assessment.classification == QUANTITATIVE_ORDINARY


def test_an_actor_is_not_their_own_accessory() -> None:
    self_principal = OffenseInstanceKey(
        "case", "甲", "derived_offense.special_theft", "derived_binding:002"
    )
    assert (
        plan_accessory_excess_candidates(
            (ACCESSORY,), (self_principal,), episode_by_instance=_episodes(ACCESSORY, self_principal)
        )
        == ()
    )


def test_a_different_episode_is_not_excess() -> None:
    episodes = {ACCESSORY: EPISODE, PRINCIPAL: "factual_episode:002"}
    assert (
        plan_accessory_excess_candidates((ACCESSORY,), (PRINCIPAL,), episode_by_instance=episodes)
        == ()
    )


def test_realizing_exactly_what_was_instigated_produces_no_candidate() -> None:
    same = OffenseInstanceKey("case", "乙", "offense.theft", "binding:003")
    assert (
        plan_accessory_excess_candidates(
            (ACCESSORY,), (same,), episode_by_instance=_episodes(ACCESSORY, same)
        )
        == ()
    )


def test_an_instance_without_an_episode_is_fatal() -> None:
    with pytest.raises(ExcessCandidateError, match="lack factual episode ids"):
        plan_accessory_excess_candidates(
            (ACCESSORY,), (PRINCIPAL,), episode_by_instance={ACCESSORY: EPISODE}
        )
