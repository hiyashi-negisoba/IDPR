from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import AnswerPlanError, _check_ground_fact_canonicalization

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")

_GROUND_FACT = "ground_fact.vaginal_intercourse_conduct"
_LEGAL_ELEMENT = "legal_element.robbery_level_violence"


def _row(occurrence_id: str, predicate_ref: str, truth: str, actor: str = "甲") -> dict:
    return {
        "instance_key": {
            "case_id": "case",
            "actor_id": actor,
            "offense_ref": "offense.test",
            "occurrence_id": occurrence_id,
        },
        "predicate_ref": predicate_ref,
        "truth": truth,
    }


def test_disagreeing_ground_fact_truths_about_one_episode_hard_fails() -> None:
    """The exact r10_p1_q1_ga shape: two bindings, one episode, opposite truths."""
    assessments = [
        _row("binding:002", _GROUND_FACT, "UNKNOWN"),
        _row("binding:004", _GROUND_FACT, "FALSE"),
    ]
    episode_by_occurrence = {"binding:002": "factual_episode:002", "binding:004": "factual_episode:002"}
    with pytest.raises(AnswerPlanError, match="CROSS_INSTANCE_GROUND_FACT_CONFLICT"):
        _check_ground_fact_canonicalization(REGISTRY, assessments, episode_by_occurrence)


def test_agreeing_ground_fact_truths_about_one_episode_pass() -> None:
    assessments = [
        _row("binding:002", _GROUND_FACT, "TRUE"),
        _row("binding:004", _GROUND_FACT, "TRUE"),
    ]
    episode_by_occurrence = {"binding:002": "factual_episode:002", "binding:004": "factual_episode:002"}
    _check_ground_fact_canonicalization(REGISTRY, assessments, episode_by_occurrence)


def test_different_episodes_may_legitimately_disagree() -> None:
    assessments = [
        _row("binding:001", _GROUND_FACT, "TRUE"),
        _row("binding:002", _GROUND_FACT, "FALSE"),
    ]
    episode_by_occurrence = {
        "binding:001": "factual_episode:001",
        "binding:002": "factual_episode:002",
    }
    _check_ground_fact_canonicalization(REGISTRY, assessments, episode_by_occurrence)


def test_legal_element_divergence_across_instances_is_not_this_guards_concern() -> None:
    """LegalElements stay offense-instance local; only GroundFact identity is canonical."""
    assessments = [
        _row("binding:001", _LEGAL_ELEMENT, "TRUE"),
        _row("binding:002", _LEGAL_ELEMENT, "FALSE"),
    ]
    episode_by_occurrence = {
        "binding:001": "factual_episode:001",
        "binding:002": "factual_episode:001",
    }
    _check_ground_fact_canonicalization(REGISTRY, assessments, episode_by_occurrence)


def test_occurrence_with_unknown_episode_identity_is_not_treated_as_a_conflict() -> None:
    """A derived-binding occurrence absent from the episode map is unmapped, not condemned."""
    assessments = [
        _row("binding:002", _GROUND_FACT, "TRUE"),
        _row("derived_binding:001", _GROUND_FACT, "FALSE"),
    ]
    episode_by_occurrence = {"binding:002": "factual_episode:002"}
    _check_ground_fact_canonicalization(REGISTRY, assessments, episode_by_occurrence)
