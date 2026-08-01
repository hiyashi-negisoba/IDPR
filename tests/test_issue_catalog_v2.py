"""The runtime catalog loads issues first and commentary cards underneath them."""

from __future__ import annotations

from idpr.rulebase.issue_catalog_v2 import (
    ANCHOR_CONTEXT,
    ASSESS_ISSUE,
    compile_issue_catalog_v2,
    issue_catalog_summary,
)
from idpr.rulebase.cards import card_corpus


def test_every_live_card_is_placed_in_exactly_one_issue():
    corpus = card_corpus()
    issues, placements = compile_issue_catalog_v2(corpus)
    assert len(placements) == len(corpus.cards) == 1_848
    assert len({item.card_id for item in placements}) == 1_848
    assert {item.card_id for item in placements} == set(corpus.by_id)
    assert sum(len(issue.member_card_ids) for issue in issues) == 1_848


def test_case_patterns_are_never_loaded_as_issue_anchors():
    issues, placements = compile_issue_catalog_v2()
    by_id = {item.card_id: item for item in placements}
    assert any(item.case_pattern for item in placements)
    for issue in issues:
        assert not set(issue.anchor_card_ids) & set(issue.case_pattern_card_ids)
        assert all(by_id[card_id].load_policy == ANCHOR_CONTEXT for card_id in issue.anchor_card_ids)


def test_theft_object_is_one_issue_with_rules_and_retrievable_cases():
    issues, _ = compile_issue_catalog_v2()
    issue = next(item for item in issues if item.issue_id == "art329.Ⅱ.element_issue")
    assert issue.title == "타인의 재물"
    assert issue.runtime == ASSESS_ISSUE
    assert "art329_sec2.theft_object_anothers_property_in_possession" in issue.anchor_card_ids
    assert len(issue.member_card_ids) == 23
    assert issue.retrieval_card_ids
    assert issue.case_pattern_card_ids


def test_focus_articles_assess_issues_instead_of_every_card():
    issues, placements = compile_issue_catalog_v2()
    focus = {"art297", "art298", "art301", "art319"}
    focus_cards = [item for item in placements if item.issue_id.split(".", 1)[0] in focus]
    assess = [
        issue for issue in issues if issue.article in focus and issue.runtime == ASSESS_ISSUE
    ]
    assert len(focus_cards) == 222
    assert len(assess) == 14
    assert len(assess) < len(focus_cards) / 10


def test_offense_name_container_splits_into_constituent_leaf_issues():
    issues, _ = compile_issue_catalog_v2()
    article = [issue for issue in issues if issue.article == "art136"]
    assert not any(issue.issue_id == "art136.Ⅱ.element_issue" for issue in article)
    assert {
        "art136.Ⅱ.2.element_issue",
        "art136.Ⅱ.3.element_issue",
        "art136.Ⅱ.4.element_issue",
        "art136.Ⅱ.5.element_issue",
    } <= {issue.issue_id for issue in article}


def test_causal_relation_is_an_element_not_concurrence():
    issues, _ = compile_issue_catalog_v2()
    issue = next(item for item in issues if item.issue_id == "art250.Ⅰ.14.element_issue")
    assert issue.title == "인과관계"


def test_separate_refusal_to_leave_variant_is_triggered_not_always_assessed():
    issues, _ = compile_issue_catalog_v2()
    issue = next(item for item in issues if item.issue_id == "art319.Ⅶ.element_issue")
    assert issue.runtime != ASSESS_ISSUE


def test_model_payload_contains_only_issue_and_anchor_rules():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue = next(item for item in issues if item.issue_id == "art329.Ⅱ.element_issue")
    payload = issue.model_payload(corpus.by_id)
    assert set(payload) == {"issue_id", "question", "rules"}
    assert len(payload["rules"]) == len(issue.anchor_card_ids) <= 4
    assert all(
        corpus.by_id[card_id].proposition in payload["rules"]
        for card_id in issue.anchor_card_ids
    )
    assert all(
        corpus.by_id[card_id].proposition not in payload["rules"]
        for card_id in issue.retrieval_card_ids
    )


def test_model_payload_accepts_only_retrieved_children_as_details():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue = next(item for item in issues if item.issue_id == "art329.Ⅱ.element_issue")
    detail_id = issue.retrieval_card_ids[0]
    payload = issue.model_payload(corpus.by_id, detail_card_ids=[detail_id])
    assert payload["details"] == [corpus.by_id[detail_id].model_payload()]

    import pytest

    with pytest.raises(ValueError, match="not retrieval children"):
        issue.model_payload(corpus.by_id, detail_card_ids=[issue.anchor_card_ids[0]])


def test_summary_records_the_large_card_to_issue_reduction():
    issues, placements = compile_issue_catalog_v2()
    summary = issue_catalog_summary(issues, placements)
    assert summary["cards"] == 1_848
    assert summary["issues"] < summary["cards"] / 4
    assert summary["by_runtime"]["assess_issue"] < summary["cards"] / 10
    assert summary["case_patterns"] > 0
