"""Call 2's dynamic grammar and evidence-coupling contracts."""

from __future__ import annotations

import json

import pytest

from idpr.neural.card_assessment import (
    CardAssessmentError,
    assessment_request,
    card_assessment_schema,
    card_status_rows,
    validate_card_assessments,
)
from idpr.neural.fact_graph import assessment_facts

CARDS = ("art298_sec3_3.indirect", "art319_sec2.enclosure")
FACTS = ("fact_001", "fact_002")


def _valid() -> dict:
    return {
        "version": "1.0.0",
        "case_id": "case-1",
        "assessments": {
            CARDS[0]: {
                "status": "satisfied",
                "basis_fact_ids": ["fact_001"],
                "counter_fact_ids": [],
                "missing_facts": [],
            },
            CARDS[1]: {
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["출입 당시 관리자의 의사"],
            },
        },
    }


def test_schema_requires_every_candidate_card_and_no_other_card():
    schema = card_assessment_schema(case_id="case-1", card_ids=CARDS, fact_ids=FACTS)
    assessments = schema["properties"]["assessments"]
    assert assessments["required"] == list(CARDS)
    assert set(assessments["properties"]) == set(CARDS)
    assert assessments["additionalProperties"] is False


def test_schema_contains_only_fields_consumed_downstream():
    schema = card_assessment_schema(case_id="case-1", card_ids=CARDS, fact_ids=FACTS)
    blob = json.dumps(schema)
    for removed in ("rationale", "confidence", "authority_comment_ids"):
        assert removed not in blob
    fields = schema["$defs"]["assessment"]["properties"]
    assert set(fields) == {
        "status",
        "basis_fact_ids",
        "counter_fact_ids",
        "missing_facts",
    }


def test_schema_closes_evidence_ids_at_decoding_time():
    schema = card_assessment_schema(case_id="case-1", card_ids=CARDS, fact_ids=FACTS)
    item = schema["$defs"]["assessment"]
    assert item["properties"]["basis_fact_ids"]["items"]["enum"] == list(FACTS)
    assert schema["properties"]["assessments"]["properties"][CARDS[0]] == {
        "$ref": "#/$defs/assessment"
    }


def test_validator_accepts_complete_directional_assessments():
    payload = _valid()
    validate_card_assessments(
        payload, case_id="case-1", card_ids=CARDS, fact_ids=FACTS
    )
    assert card_status_rows(payload) == (
        (CARDS[0], "satisfied"),
        (CARDS[1], "unknown"),
    )


@pytest.mark.parametrize(
    ("card", "status", "field", "message"),
    [
        (CARDS[0], "satisfied", "basis_fact_ids", "requires at least one basis"),
        (CARDS[0], "not_satisfied", "counter_fact_ids", "requires at least one counter"),
        (CARDS[1], "unknown", "missing_facts", "requires missing_facts"),
    ],
)
def test_validator_couples_status_to_directional_evidence(card, status, field, message):
    payload = _valid()
    payload["assessments"][card]["status"] = status
    payload["assessments"][card][field] = []
    with pytest.raises(CardAssessmentError, match=message):
        validate_card_assessments(
            payload, case_id="case-1", card_ids=CARDS, fact_ids=FACTS
        )


def test_validator_rejects_missing_extra_and_unknown_references():
    payload = _valid()
    payload["assessments"].pop(CARDS[1])
    payload["assessments"]["invented.card"] = payload["assessments"][CARDS[0]]
    payload["assessments"][CARDS[0]]["basis_fact_ids"] = ["fact_999"]
    with pytest.raises(CardAssessmentError) as exc_info:
        validate_card_assessments(
            payload, case_id="case-1", card_ids=CARDS, fact_ids=FACTS
        )
    message = str(exc_info.value)
    assert CARDS[1] in message
    assert "invented.card" in message
    assert "fact_999" in message


def test_schema_inputs_must_be_nonempty_unique_and_case_safe():
    with pytest.raises(CardAssessmentError, match="duplicate card_ids"):
        card_assessment_schema(
            case_id="case-1", card_ids=(CARDS[0], CARDS[0]), fact_ids=FACTS
        )
    with pytest.raises(CardAssessmentError, match="fact_ids must not be empty"):
        card_assessment_schema(case_id="case-1", card_ids=CARDS, fact_ids=())
    with pytest.raises(CardAssessmentError, match="safe identifier"):
        card_assessment_schema(case_id="bad id", card_ids=CARDS, fact_ids=FACTS)


def test_host_mints_one_evidence_id_per_grounded_assertion():
    graph = {
        "acts": [{"actor": "entity_0", "source_quote": "행위"}],
        "results": [{"entity": "entity_1", "source_quote": "결과"}],
        "roles": [{"entity": "entity_0", "source_quote": "역할"}],
        "relations": [],
        "holdings": [{"entity": "entity_1", "source_quote": "보유"}],
    }
    facts = assessment_facts(graph)
    assert [fact["fact_id"] for fact in facts] == [
        "fact_001",
        "fact_002",
        "fact_003",
        "fact_004",
    ]
    assert [fact["kind"] for fact in facts] == ["act", "result", "role", "holding"]


def test_request_keeps_only_whitelisted_case_fields_and_reviewed_card_payload():
    case = {
        "sub_question_id": "case-1",
        "question_text": "甲이 출입하였다.",
        "question_prompt": "죄책을 논하라.",
        "rubric_summary": ["정답지"],
        "supporting_precedents": ["gold"],
    }
    graph = {
        "case_id": "case-1",
        "entities": [{"entity_id": "entity_0", "mentions": ["甲"]}],
        "acts": [{"actor": "entity_0", "source_quote": "甲이 출입하였다."}],
        "results": [],
        "roles": [],
        "relations": [],
        "holdings": [],
    }
    request = assessment_request(
        case=case,
        fact_graph=graph,
        cards=[
            {
                "id": CARDS[0],
                "proposition": "검수된 명제",
                "source_refs": [{"comment_id": "comm_secret", "quote": "원문"}],
            }
        ],
    )
    assert set(request) == {
        "case_id",
        "question_text",
        "question_prompt",
        "entities",
        "facts",
        "cards",
    }
    assert request["cards"] == [{"id": CARDS[0], "proposition": "검수된 명제"}]
    blob = json.dumps(request, ensure_ascii=False)
    for forbidden in (
        "rubric_summary",
        "supporting_precedents",
        "source_refs",
        "comment_id",
        "comm_secret",
    ):
        assert forbidden not in blob
