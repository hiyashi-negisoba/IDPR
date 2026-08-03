from __future__ import annotations

import pytest

from idpr.generation.issue_answer import build_call3_request
from idpr.issue_pipeline import scope_from_l0_row
from idpr.special_part import (
    PIPELINE_MODE,
    SpecialPartPlanError,
    planned_candidate_row,
    planner_payload,
    planner_schema,
    validate_plan,
)


def test_planner_exposes_only_articles_with_standalone_element_issues():
    payload, articles = planner_payload(
        case_id="case-1",
        question_text="甲이 A를 폭행하여 추행하였다.",
        question_prompt="甲의 죄책을 논하시오.",
        broad_articles=("art298", "art300", "art342"),
    )
    assert articles == ("art298",)
    assert [row["article"] for row in payload["candidate_articles"]] == ["art298"]
    assert planner_schema(articles)["properties"]["selected"]["items"]["properties"][
        "article"
    ] == {"type": "string", "enum": ["art298"]}


def test_planner_requires_an_exact_case_quote_and_closed_candidate_article():
    valid = {
        "route": "article_local",
        "selected": [
            {
                "article": "art298",
                "actor": "甲",
                "source_quote": "甲이 A를 폭행하여 추행하였다",
                "reason": "폭행과 추행 행위가 직접 기재되어 있다.",
            }
        ],
        "scope_note": "강제추행 구성요건만 독립 검토한다.",
    }
    articles, entries = validate_plan(
        valid,
        candidate_articles=("art298",),
        question_text="甲이 A를 폭행하여 추행하였다.",
    )
    assert articles == ("art298",)
    assert entries[0]["actor"] == "甲"

    invalid = {**valid, "selected": [{**valid["selected"][0], "source_quote": "없는 사실"}]}
    with pytest.raises(SpecialPartPlanError, match="exact case-text substring"):
        validate_plan(
            invalid,
            candidate_articles=("art298",),
            question_text="甲이 A를 폭행하여 추행하였다.",
        )

    direct = {
        "route": "direct_legal_analysis",
        "selected": [],
        "scope_note": "증거능력을 묻는 절차법 설문이다.",
    }
    assert validate_plan(
        direct,
        candidate_articles=("art298",),
        question_text="증거로 사용할 수 있는가?",
    ) == ((), ())
    with pytest.raises(SpecialPartPlanError, match="must not select articles"):
        validate_plan(
            {**valid, "route": "direct_legal_analysis"},
            candidate_articles=("art298",),
            question_text="甲이 A를 폭행하여 추행하였다.",
        )


def test_planned_scope_never_reintroduces_attempt_expansion():
    row = planned_candidate_row(
        case_id="case-1",
        selected_articles=("art298",),
        entries=(),
        scope_note="독립 각칙 조문",
        broad_articles=("art298", "art300"),
    )
    assert row["pipeline_mode"] == PIPELINE_MODE
    assert row["articles"] == ["art298"]
    assert row["from_attempt_expansion"] == []
    assert scope_from_l0_row(row).articles == ("art298",)


def test_article_local_answer_keeps_planned_article_and_uses_only_its_issue_statuses():
    case = {
        "sub_question_id": "case-1",
        "question_text": "甲이 A를 밀쳤다.",
        "question_prompt": "甲의 죄책을 논하시오.",
    }
    graph = {
        "case_id": "case-1",
        "acts": [
            {"actor": "entity_0", "act_label": "유형력행사", "source_quote": "甲이 A를 밀쳤다."}
        ],
        "results": [],
        "roles": [],
        "relations": [],
        "holdings": [],
    }
    packet = {
        "pipeline_mode": PIPELINE_MODE,
        "case_id": "case-1",
        "issues": [
            {
                "issue_id": "art298.element.one",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "행위",
                "function": "element_issue",
                "runtime": "assess_issue",
                "include_in_generation": True,
                "status": "satisfied",
                "basis_fact_ids": ["fact_001"],
                "counter_fact_ids": [],
                "missing_facts": [],
                "anchor_rules": [
                    {
                        "rule_id": "rule.one",
                        "proposition": "폭행 또는 협박으로 추행해야 한다.",
                        "basis_card_ids": ["rule.one"],
                        "origin": "reviewed_card",
                    }
                ],
                "detail_rules": [],
            },
            {
                "issue_id": "art298.element.two",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "고의",
                "function": "element_issue",
                "runtime": "assess_issue",
                "include_in_generation": True,
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["추행의 고의"],
                "anchor_rules": [],
                "detail_rules": [],
            },
            {
                "issue_id": "art298.stage",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "미수",
                "function": "stage_issue",
                "runtime": "relation_condition",
                "include_in_generation": False,
                "status": "satisfied",
                "basis_fact_ids": ["fact_001"],
                "counter_fact_ids": [],
                "missing_facts": [],
                "anchor_rules": [],
                "detail_rules": [],
            },
        ],
        "symbolic_runtime": {"engine": "disabled_article_local", "relations": {}},
    }
    request = build_call3_request(case=case, fact_graph=graph, reasoning_packet=packet)
    assert request["pipeline_mode"] == PIPELINE_MODE
    assert request["suppressed_sections"] == []
    assert request["cross_offense_directives"] == {
        "absorbed_articles": [],
        "concurrent_pairs": [],
    }
    assert len(request["required_sections"]) == 1
    section = request["required_sections"][0]
    assert [issue["title"] for issue in section["issues"]] == ["행위", "고의"]
    assert section["stated_conclusion"] == "undetermined"
    assert section["presentation_mode"] == "full"
