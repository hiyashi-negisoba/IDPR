"""Contracts for the experimental upstream article reconciler."""

from __future__ import annotations

import pytest

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.article_reconcile import (
    ArticleReconcileError,
    reconciliation_payload,
    reconciliation_schema,
    validate_reconciliation,
)


def test_schema_is_closed_to_the_union_candidates():
    schema = reconciliation_schema(["art298", "art319"])
    selected = schema["properties"]["selected"]
    assert selected["maxItems"] == 2
    assert selected["items"]["properties"]["article"]["enum"] == ["art298", "art319"]


def test_payload_has_only_scoped_case_and_candidate_evidence():
    payload = reconciliation_payload(
        case_id="c1",
        question_text="甲은 A를 밀었다.",
        question_prompt="甲의 죄책을 논하라.",
        candidates=[
            {
                "article": "art257",
                "label": "제257조",
                "offense": "상해",
                "admission_channels": ["retrieval"],
                "retrieval_rank": 1,
                "retrieved_issue": "상해의 결과",
                "retrieved_rules": ["생리적 기능 훼손"],
            }
        ],
    )
    assert_no_leaked_fields(payload)
    assert set(payload) == {"case_id", "case_text", "question_prompt", "candidates"}


def test_payload_rejects_evaluation_metadata():
    with pytest.raises(ValueError, match="non-whitelisted"):
        reconciliation_payload(
            case_id="c1",
            question_text="facts",
            question_prompt="prompt",
            candidates=[{"article": "art257", "rubric_summary": "leak"}],
        )


def test_response_cannot_restore_an_article_outside_the_union():
    with pytest.raises(ArticleReconcileError):
        validate_reconciliation(
            {"selected": [{"article": "art999", "reason": "x"}]},
            allowed_articles=["art257"],
        )


def test_response_keeps_first_reason_and_requires_nonempty_selection():
    articles, entries = validate_reconciliation(
        {
            "selected": [
                {"article": "art257", "reason": "first"},
                {"article": "art257", "reason": "second"},
            ]
        },
        allowed_articles=["art257"],
    )
    assert articles == ("art257",)
    assert entries == ({"article": "art257", "reason": "first"},)
    with pytest.raises(ArticleReconcileError):
        validate_reconciliation({"selected": []}, allowed_articles=["art257"])
