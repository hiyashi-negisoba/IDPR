from __future__ import annotations

import pytest
from jsonschema import Draft202012Validator

from idpr.generation.issue_answer import (
    IssueAnswerError,
    attach_issue_answer_provenance,
    build_call3_request,
    issue_answer_model_request,
    issue_answer_model_schema,
    render_issue_answer_markdown,
    validate_issue_answer,
)


def _request(
    *,
    element_unaddressed: bool = False,
    attempt: bool = False,
    element_supported: bool = True,
):
    case = {
        "sub_question_id": "case-1",
        "question_text": "甲이 A를 밀쳤다.",
        "question_prompt": "甲의 죄책을 논하시오.",
    }
    graph = {
        "case_id": "case-1",
        "acts": [
            {
                "actor": "entity_0",
                "act_label": "유형력행사",
                "source_quote": "甲이 A를 밀쳤다.",
            }
        ],
        "results": [],
        "roles": [],
        "relations": [],
        "holdings": [],
    }
    packet = {
        "case_id": "case-1",
        "issues": [
            {
                "issue_id": "art298.Ⅱ.element_issue",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "폭행·협박",
                "function": "element_issue",
                "runtime": "assess_issue",
                "status": "satisfied",
                "basis_fact_ids": ["fact_001"],
                "counter_fact_ids": [],
                "missing_facts": [],
                "anchor_rules": [
                    {
                        "rule_id": "card.rule",
                        "proposition": "폭행 또는 협박이 필요하다.",
                        "basis_card_ids": ["card.rule"],
                        "origin": "reviewed_card",
                    }
                ],
                "detail_rules": [],
            },
            {
                "issue_id": "art298.Ⅲ.stage_issue",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "실행의 착수",
                "function": "stage_issue",
                "runtime": "relation_condition",
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["신체 접촉이 시작되었는지"],
                "anchor_rules": [
                    {
                        "rule_id": "card.stage",
                        "proposition": "유형력 행사 시 착수한다.",
                        "basis_card_ids": ["card.stage"],
                        "origin": "reviewed_card",
                    }
                ],
                "detail_rules": [],
            },
            {
                "issue_id": "art298.Ⅵ.concurrence_issue",
                "article": "art298",
                "article_label": "제298조",
                "offense": "강제추행",
                "title": "추가 피해자",
                "function": "concurrence_issue",
                "runtime": "relation_condition",
                "symbolic_condition": False,
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["추가 피해자가 있는지"],
                "anchor_rules": [],
                "detail_rules": [],
            },
        ],
        "symbolic_runtime": {
            "relations": {
                "element_supported": (
                    [["case-1", "art298", "art298.Ⅱ.element_issue"]]
                    if element_supported
                    else []
                ),
                "element_refuted": [],
                "offense_established": (
                    [["case-1", "art298"]] if element_supported else []
                ),
                "offense_undetermined": [],
                "final_offense": (
                    [["case-1", "art298"]] if element_supported else []
                ),
                "attempt_to_consider": (
                    [["case-1", "art298"]] if attempt else []
                ),
                "is_absorbed": [],
                "concurrent_offenses": [],
                "element_unaddressed": (
                    [["case-1", "art298", "art298.Ⅱ.element_issue"]]
                    if element_unaddressed
                    else []
                ),
            }
        },
    }
    return build_call3_request(case=case, fact_graph=graph, reasoning_packet=packet)


def test_call3_request_keeps_rubric_shape_without_leaking_the_rubric_or_raw_relations():
    request = _request()
    assert request["rubric_supplied"] is False
    assert len(request["required_sections"]) == 1
    section = request["required_sections"][0]
    assert [issue["function"] for issue in section["issues"]] == [
        "element_issue",
        "stage_issue",
    ]
    assert section["symbolic_directive"] == "final_offense_candidate"
    assert section["presentation_mode"] == "full"
    assert request["suppressed_sections"] == []
    assert "offense_established" not in repr(request)
    assert section["issues"][0]["basis_facts"][0]["statement"] == "甲이 A를 밀쳤다."


def test_call3_answer_validation_binds_order_conclusion_and_provenance():
    request = _request()
    answer = {
        "version": "1.0.0",
        "case_id": "case-1",
        "title": "甲의 죄책",
        "sections": [
            {
                "section_id": "offense_art298",
                "heading": "제298조 강제추행",
                "analyses": [
                    {
                        "analysis_id": "art298.Ⅱ.element_issue",
                        "heading": "폭행·협박",
                        "issue": "폭행 또는 협박이 문제된다.",
                        "rule": "폭행 또는 협박이 필요하다.",
                        "application": "甲이 A를 밀친 행위는 유형력 행사이다.",
                        "conclusion": "요건이 충족된다.",
                        "issue_status": "satisfied",
                    },
                    {
                        "analysis_id": "art298.Ⅲ.stage_issue",
                        "heading": "실행의 착수",
                        "issue": "실행의 착수가 문제된다.",
                        "rule": "유형력 행사가 개시되어야 한다.",
                        "application": "신체 접촉 시점이 확인되지 않는다.",
                        "conclusion": "현재 사실로는 미확정이다.",
                        "issue_status": "unknown",
                    },
                ],
                "conclusion": "강제추행죄가 성립한다.",
                "cited_fact_ids": ["fact_001"],
                "cited_issue_ids": [
                    "art298.Ⅱ.element_issue",
                    "art298.Ⅲ.stage_issue",
                ],
                "cited_rule_ids": ["card.rule", "card.stage"],
                "stated_conclusion": "established",
            }
        ],
        "overall_conclusion": "甲에게 강제추행죄가 성립한다.",
    }
    validate_issue_answer(answer, request=request)
    answer["sections"][0]["analyses"][0]["application"] = "fact_id를 그대로 노출한다."
    with pytest.raises(IssueAnswerError, match="internal identifier"):
        validate_issue_answer(answer, request=request)


def test_unaddressed_element_overrides_a_raw_established_relation_for_call3():
    request = _request(element_unaddressed=True)
    section = request["required_sections"][0]
    assert section["symbolic_directive"] == "undetermined"
    assert section["stated_conclusion"] == "undetermined"


def test_host_overall_conclusion_preserves_attempt_review_directive():
    request = _request(attempt=True)
    answer = attach_issue_answer_provenance({"sections": [{}]}, request=request)
    assert answer["sections"][0]["conclusion"] == (
        "제298조 강제추행: 기수는 성립하지 않으며, "
        "미수 성립 및 유형은 추가 검토가 필요하다."
    )
    assert answer["sections"][0]["stated_conclusion"] == "undetermined"
    assert answer["overall_conclusion"] == (
        "제298조 강제추행: 기수 불성립, 미수 여부 검토."
    )


def test_model_schema_keeps_only_prose_and_host_attaches_controls():
    request = _request()
    schema = issue_answer_model_schema(request)
    section_schema = schema["properties"]["sections"]["prefixItems"][0]
    assert section_schema["properties"]["heading"] == {"const": "제298조 강제추행"}
    assert "section_id" not in section_schema["properties"]
    assert "stated_conclusion" not in section_schema["properties"]
    assert "conclusion" not in section_schema["properties"]
    analyses_schema = section_schema["properties"]["analyses"]
    assert analyses_schema["minItems"] == 2
    assert analyses_schema["maxItems"] == 2
    assert analyses_schema["items"] is False
    assert analyses_schema["prefixItems"][0]["properties"]["heading"] == {
        "const": "폭행·협박"
    }
    assert "analysis_id" not in analyses_schema["prefixItems"][0]["properties"]
    assert "issue_status" not in analyses_schema["prefixItems"][0]["properties"]
    assert "cited_issue_ids" not in section_schema["properties"]
    assert "overall_conclusion" not in schema["properties"]

    model_answer = {
        "version": "1.0.0",
        "case_id": "case-1",
        "title": "甲의 죄책",
        "sections": [
            {
                "heading": "강제추행죄",
                "analyses": [
                    {
                        "heading": "폭행·협박",
                        "issue": "폭행 또는 협박이 문제된다.",
                        "rule": "폭행 또는 협박이 필요하다.",
                        "application": "甲은 A를 밀쳤다.",
                        "conclusion": "요건이 충족된다.",
                    },
                    {
                        "heading": "실행의 착수",
                        "issue": "실행의 착수가 문제된다.",
                        "rule": "유형력 행사가 개시되어야 한다.",
                        "application": "신체 접촉 시점은 확인되지 않는다.",
                        "conclusion": "현재 사실로는 미확정이다.",
                    },
                ],
            }
        ],
    }
    answer = attach_issue_answer_provenance(model_answer, request=request)
    assert answer["sections"][0]["heading"] == "제298조 강제추행"
    assert answer["sections"][0]["section_id"] == "offense_art298"
    assert answer["sections"][0]["analyses"][0]["analysis_id"] == (
        "art298.Ⅱ.element_issue"
    )
    assert answer["sections"][0]["analyses"][0]["issue_status"] == "satisfied"
    assert answer["sections"][0]["cited_issue_ids"] == [
        "art298.Ⅱ.element_issue",
        "art298.Ⅲ.stage_issue",
    ]
    assert answer["sections"][0]["cited_fact_ids"] == ["fact_001"]
    assert answer["sections"][0]["cited_rule_ids"] == ["card.rule", "card.stage"]
    assert answer["sections"][0]["conclusion"] == "제298조 강제추행: 성립한다."
    assert answer["sections"][0]["stated_conclusion"] == "established"
    assert answer["overall_conclusion"] == "제298조 강제추행: 성립."
    validate_issue_answer(answer, request=request)

    model_errors = list(Draft202012Validator(schema).iter_errors(model_answer))
    assert any("was expected" in error.message for error in model_errors)


def test_host_replaces_model_authored_offense_and_issue_headings():
    request = _request()
    model_answer = {
        "version": "1.0.0",
        "case_id": "case-1",
        "title": "甲의 죄책",
        "sections": [
            {
                "heading": "제337조 강도상해",
                "analyses": [
                    {
                        "heading": "상해 결과",
                        "issue": "폭행 여부가 문제된다.",
                        "rule": "폭행 또는 협박이 필요하다.",
                        "application": "甲은 A를 밀쳤다.",
                        "conclusion": "유형력이 인정된다.",
                    },
                    {
                        "heading": "기수",
                        "issue": "착수 여부가 문제된다.",
                        "rule": "유형력 행사가 개시되어야 한다.",
                        "application": "접촉 시점은 불분명하다.",
                        "conclusion": "현재 사실로는 미확정이다.",
                    },
                ],
            }
        ],
    }
    answer = attach_issue_answer_provenance(model_answer, request=request)
    assert answer["sections"][0]["heading"] == "제298조 강제추행"
    assert [row["heading"] for row in answer["sections"][0]["analyses"]] == [
        "폭행·협박",
        "실행의 착수",
    ]
    validate_issue_answer(answer, request=request)


def test_call3_hides_an_article_with_no_positive_element_support():
    request = _request(element_supported=False)
    assert request["required_sections"] == []
    assert request["suppressed_sections"][0]["reason"] == (
        "no_positive_element_support"
    )
    assert "suppressed_sections" not in issue_answer_model_request(request)
    # Exercise the host-side empty answer contract as well: hidden candidates remain in
    # request diagnostics but do not require invented prose.
    answer = attach_issue_answer_provenance(
        {
            "version": "1.0.0",
            "case_id": "case-1",
            "title": "甲의 죄책",
            "sections": [],
        },
        request=request,
    )
    assert answer["overall_conclusion"].startswith("현재 제공된 사실")


def test_markdown_renders_one_integrated_irac_per_offense():
    request = _request()
    model_answer = {
        "version": "1.0.0",
        "case_id": "case-1",
        "title": "甲의 죄책",
        "sections": [
            {
                "section_id": "offense_art298",
                "heading": "강제추행죄",
                "analyses": [
                    {
                        "analysis_id": "art298.Ⅱ.element_issue",
                        "heading": "폭행·협박",
                        "issue": "폭행 또는 협박이 있었는지가 문제된다.",
                        "rule": "폭행 또는 협박이 필요하다.",
                        "application": "甲이 A를 밀친 것은 유형력 행사이다.",
                        "conclusion": "폭행 요건은 충족된다.",
                        "issue_status": "satisfied",
                    },
                    {
                        "analysis_id": "art298.Ⅲ.stage_issue",
                        "heading": "실행의 착수",
                        "issue": "실행의 착수 시점이 문제된다.",
                        "rule": "유형력 행사가 개시되어야 한다.",
                        "application": "신체 접촉 시점은 확인되지 않는다.",
                        "conclusion": "실행의 착수 여부는 미확정이다.",
                        "issue_status": "unknown",
                    },
                ],
            }
        ],
    }
    answer = attach_issue_answer_provenance(model_answer, request=request)
    markdown = render_issue_answer_markdown(answer)
    assert markdown.count("### 쟁점 (Issue)") == 1
    assert markdown.count("### 법리 (Rule)") == 1
    assert markdown.count("### 사안의 적용 (Application)") == 1
    assert markdown.count("### 결론 (Conclusion)") == 1
    assert "- **폭행·협박**" in markdown
    assert "**소결:** 폭행 요건은 충족된다." in markdown


def test_markdown_groups_unresolved_offenses_as_compact_supplement():
    request = _request(element_unaddressed=True)
    model_answer = {
        "version": "1.0.0",
        "case_id": "case-1",
        "title": "甲의 죄책",
        "sections": [
            {
                "heading": "모델이 쓴 잘못된 제목",
                "analyses": [
                    {
                        "heading": "폭행·협박",
                        "issue": "폭행 여부가 문제된다.",
                        "rule": "폭행이 필요하다.",
                        "application": "甲은 A를 밀쳤다.",
                        "conclusion": "유형력은 인정된다.",
                    },
                    {
                        "heading": "실행의 착수",
                        "issue": "착수 여부가 문제된다.",
                        "rule": "실행행위가 필요하다.",
                        "application": "접촉 시점은 불분명하다.",
                        "conclusion": "착수 여부는 미확정이다.",
                    },
                ],
            }
        ],
    }
    answer = attach_issue_answer_provenance(model_answer, request=request)
    markdown = render_issue_answer_markdown(answer)
    assert "## 보충적 검토" in markdown
    assert "### 제298조 강제추행" in markdown
    assert "### 법리 (Rule)" not in markdown
    assert "접촉 시점은 불분명하다" not in markdown
