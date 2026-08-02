"""Fixed-case diagnostic for the historical Phase-2/Phase-3 comparison."""

from __future__ import annotations

from scripts.run_issue_assessment import prepare_issue_case


SMOKE_CASE_ID = "kcl_criminal_r10_p1_q1_ga"
SMOKE_ARTICLES = ("art298", "art297", "art301", "art319")


def test_default_smoke_reduces_193_cards_to_14_assessable_issues():
    _, _, scope = prepare_issue_case(case_id=SMOKE_CASE_ID, articles=SMOKE_ARTICLES)
    issues = scope.initial_issues
    assert len(issues) == 14
    assert {issue.article for issue in issues} == set(SMOKE_ARTICLES)
    assert all(issue.anchor_card_ids for issue in issues)
