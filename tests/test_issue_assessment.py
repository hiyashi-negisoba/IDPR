"""Issue-first Call-2 uses a small exact-key schema and fact-linked statuses."""

from __future__ import annotations

import pytest

from idpr.neural.issue_assessment import (
    SCHEMA_VERSION,
    IssueAssessmentError,
    issue_assessment_request,
    issue_assessment_schema,
    issue_status_rows,
    validate_issue_assessments,
)


def _graph():
    return {
        "case_id": "case-1",
        "entities": [{"entity_id": "p1", "label": "갑", "entity_type": "person"}],
        "facts": [
            {
                "fact_id": "f1",
                "relation": "act",
                "arguments": ["p1"],
                "source": {"quote": "갑이 물건을 가져갔다."},
            }
        ],
    }


def test_schema_requires_every_issue_exactly_once():
    schema = issue_assessment_schema(
        case_id="case-1", issue_ids=["art329.Ⅱ.element_issue"], fact_ids=["f1"]
    )
    assessments = schema["properties"]["assessments"]
    assert assessments["required"] == ["art329.Ⅱ.element_issue"]
    assert assessments["additionalProperties"] is False


def test_request_keeps_rules_inside_one_issue_not_as_separate_tasks():
    request = issue_assessment_request(
        case={"sub_question_id": "case-1", "question_text": "사례", "question_prompt": ""},
        fact_graph=_graph(),
        issues=[
            {
                "issue_id": "art329.Ⅱ.element_issue",
                "question": "타인의 재물인가?",
                "rules": ["타인 소유이면서 타인 점유인 재물이다.", "점유는 사실상 지배다."],
            }
        ],
    )
    assert len(request["issues"]) == 1
    assert len(request["issues"][0]["rules"]) == 2
    assert "source_refs" not in repr(request)
    assert "comment_id" not in repr(request)


def test_request_keeps_retrieved_details_inside_the_parent_issue():
    request = issue_assessment_request(
        case={"sub_question_id": "case-1", "question_text": "사례", "question_prompt": ""},
        fact_graph=_graph(),
        issues=[
            {
                "issue_id": "art329.Ⅱ.element_issue",
                "question": "타인의 재물인가?",
                "rules": ["타인 소유이면서 타인 점유인 재물이다."],
                "details": [
                    {"id": "detail.1", "proposition": "특정 사안의 판단기준이다."}
                ],
            }
        ],
    )
    assert request["issues"][0]["details"] == [
        {"id": "detail.1", "proposition": "특정 사안의 판단기준이다."}
    ]
    assert "source_refs" not in repr(request)


def test_validation_couples_status_to_fact_evidence():
    payload = {
        "version": SCHEMA_VERSION,
        "case_id": "case-1",
        "assessments": {
            "art329.Ⅱ.element_issue": {
                "status": "satisfied",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": [],
            }
        },
    }
    with pytest.raises(IssueAssessmentError, match="requires basis facts"):
        validate_issue_assessments(
            payload,
            case_id="case-1",
            issue_ids=["art329.Ⅱ.element_issue"],
            fact_ids=["f1"],
        )


def test_valid_unknown_requires_only_a_concrete_missing_fact():
    payload = {
        "version": SCHEMA_VERSION,
        "case_id": "case-1",
        "assessments": {
            "art329.Ⅱ.element_issue": {
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["물건의 소유자와 점유자"],
            }
        },
    }
    validate_issue_assessments(
        payload,
        case_id="case-1",
        issue_ids=["art329.Ⅱ.element_issue"],
        fact_ids=["f1"],
    )


def test_issue_status_rows_preserves_issue_assessment_order():
    payload = {
        "assessments": {
            "i2": {"status": "unknown"},
            "i1": {"status": "satisfied"},
        }
    }
    assert issue_status_rows(payload) == (
        ("i2", "unknown"),
        ("i1", "satisfied"),
    )
