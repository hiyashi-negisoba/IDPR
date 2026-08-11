from __future__ import annotations

import pytest

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    GroundingContractError,
    PredicateDefinition,
    call2_request_payload,
    case_truths_from_assessments,
    shard_assessment_targets_by_occurrence,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey


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
    assert set(payload) == {"evidence_occurrence", "predicate_catalog", "assessment_targets"}
    assert "case_text" not in payload
    assert "occurrence_catalog" not in payload
    assert payload["evidence_occurrence"]["source_text"] == "甲의 1번 행위"


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
