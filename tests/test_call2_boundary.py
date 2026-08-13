from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.question_assumptions import QuestionAssumption
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    GroundingContractError,
    PredicateDefinition,
    call2_request_payload,
    case_truths_from_assessments,
    expand_ground_fact_assessments,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets_by_occurrence,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _occurrence(number: int, actor: str = "甲") -> GoldOccurrence:
    text = f"{actor}의 {number}번 행위"
    return GoldOccurrence(f"gocc:{number:03d}", actor, text, 0, len(text))


def _target(number: int, predicate: str = "ground_fact.p") -> AssessmentTarget:
    return AssessmentTarget(
        OffenseInstanceKey("case", "甲", "offense.test", f"gocc:{number:03d}"), predicate
    )


PREDICATE = PredicateDefinition("ground_fact.p", "ground_fact", "시험 사실", ())


def test_request_contains_only_one_occurrence_span_and_never_full_case_text() -> None:
    payload = call2_request_payload(
        evidence_occurrence=_occurrence(1), predicates=(PREDICATE,), targets=(_target(1),)
    )
    assert set(payload) == {
        "evidence_occurrence",
        "question_assumptions",
        "predicate_catalog",
        "assessment_targets",
    }
    assert "case_text" not in payload
    assert "occurrence_catalog" not in payload
    assert payload["evidence_occurrence"]["source_text"] == "甲의 1번 행위"
    assert payload["question_assumptions"] == []
    assert payload["assessment_targets"] == [
        {
            "occurrence_key": {
                "case_id": "case",
                "actor_id": "甲",
                "occurrence_id": "gocc:001",
            },
            "predicate_ref": "ground_fact.p",
        }
    ]


def test_request_keeps_question_assumption_separate_from_occurrence_evidence() -> None:
    assumption = QuestionAssumption("qassump:001", "P의 직무집행은 적법하다", 0, 15)
    payload = call2_request_payload(
        evidence_occurrence=_occurrence(1),
        question_assumptions=(assumption,),
        predicates=(PREDICATE,),
        targets=(_target(1),),
    )
    assert payload["evidence_occurrence"]["source_text"] == "甲의 1번 행위"
    assert payload["question_assumptions"] == [assumption.as_dict()]


def test_request_rejects_cross_occurrence_or_cross_actor_targets() -> None:
    with pytest.raises(GroundingContractError):
        call2_request_payload(
            evidence_occurrence=_occurrence(1), predicates=(PREDICATE,), targets=(_target(2),)
        )
    wrong_actor = AssessmentTarget(
        OffenseInstanceKey("case", "乙", "offense.test", "gocc:001"), "ground_fact.p"
    )
    with pytest.raises(GroundingContractError):
        call2_request_payload(
            evidence_occurrence=_occurrence(1), predicates=(PREDICATE,), targets=(wrong_actor,)
        )


def test_sharding_preserves_total_order_without_crossing_occurrences() -> None:
    targets = (_target(1, "p1"), _target(1, "p2"), _target(2, "p1"), _target(1, "p3"))
    shards = shard_assessment_targets_by_occurrence(targets, max_targets=2)
    assert tuple(target for shard in shards for target in shard) == targets
    assert [len(shard) for shard in shards] == [2, 1, 1]
    assert all(len({target.instance_key.occurrence_id for target in shard}) == 1 for shard in shards)


@pytest.mark.parametrize("truths", ([], ["TRUE", "FALSE"], ["INVALID"]))
def test_compact_response_missing_extra_or_invalid_truth_hard_fails(truths: list[str]) -> None:
    with pytest.raises(GroundingContractError):
        validate_call2_output(
            {"truths": truths}, targets=(_target(1),)
        )


def test_compact_response_extra_field_hard_fails() -> None:
    with pytest.raises(GroundingContractError):
        validate_call2_output(
            {"truths": ["TRUE"], "telemetry": [0.5]},
            targets=(_target(1),),
        )


def test_compact_response_reconstructs_exact_unique_case_truth_key() -> None:
    targets = (_target(1, "p1"), _target(1, "p2"))
    assessments = validate_call2_output(
        {"truths": ["TRUE", "UNKNOWN"]},
        targets=targets,
    )
    projected = case_truths_from_assessments(assessments, expected_targets=targets)
    assert list(projected.predicate) == [
        (targets[0].instance_key, "p1"),
        (targets[1].instance_key, "p2"),
    ]


def test_ground_fact_is_asked_once_then_projected_to_all_offense_consumers() -> None:
    first = AssessmentTarget(
        OffenseInstanceKey("case", "甲", "offense.theft", "gocc:001"),
        "ground_fact.taking_conduct",
    )
    second = AssessmentTarget(
        OffenseInstanceKey("case", "甲", "offense.robbery", "gocc:001"),
        "ground_fact.taking_conduct",
    )
    legal = AssessmentTarget(
        OffenseInstanceKey("case", "甲", "offense.robbery", "gocc:001"),
        "legal_element.robbery_level_violence",
    )
    semantic_targets = (first, second, legal)
    request_targets = grounding_request_targets(REGISTRY, semantic_targets)
    assert request_targets == (first, legal)

    predicates = predicate_definitions(
        REGISTRY,
        ("ground_fact.taking_conduct", "legal_element.robbery_level_violence"),
    )
    payload = call2_request_payload(
        evidence_occurrence=_occurrence(1),
        predicates=predicates,
        targets=request_targets,
    )
    assert "offense_ref" not in payload["assessment_targets"][0]["occurrence_key"]
    assert "instance_key" in payload["assessment_targets"][1]

    request_assessments = validate_call2_output(
        {"truths": ["TRUE", "FALSE"]}, targets=request_targets
    )
    expanded = expand_ground_fact_assessments(
        REGISTRY, request_assessments, expected_targets=semantic_targets
    )
    assert [value.truth for value in expanded] == ["TRUE", "TRUE", "FALSE"]


def test_ground_fact_dedups_across_bindings_that_share_a_factual_episode() -> None:
    """A base and a derived offense are separate bindings but can be the same episode.

    This is the exact shape of the r10_p1_q1_ga cross-instance conflict: rape (binding:002) and
    aggravated-result rape (binding:004) both raise `ground_fact.vaginal_intercourse_conduct`
    about factual_episode:002.  Without episode identity the two bindings look unrelated and the
    same GroundFact gets asked twice, with no guarantee the two answers agree.
    """
    base = AssessmentTarget(
        OffenseInstanceKey("case", "甲", "offense.rape", "binding:002"),
        "ground_fact.vaginal_intercourse_conduct",
    )
    derived = AssessmentTarget(
        OffenseInstanceKey(
            "case", "甲", "derived_offense.rape_causing_injury_by_aggravated_result", "binding:004"
        ),
        "ground_fact.vaginal_intercourse_conduct",
    )
    episode_by_occurrence = {"binding:002": "factual_episode:002", "binding:004": "factual_episode:002"}

    request_targets = grounding_request_targets(
        REGISTRY, (base, derived), episode_by_occurrence=episode_by_occurrence
    )
    assert request_targets == (base,)

    request_assessments = validate_call2_output({"truths": ["TRUE"]}, targets=request_targets)
    expanded = expand_ground_fact_assessments(
        REGISTRY,
        request_assessments,
        expected_targets=(base, derived),
        episode_by_occurrence=episode_by_occurrence,
    )
    assert [value.truth for value in expanded] == ["TRUE", "TRUE"]
