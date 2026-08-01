"""Dry-run preparation for the issue-first smoke stays tied to Phase-2 artifacts."""

from __future__ import annotations

from scripts.run_call2_issue_smoke import DEFAULT_ARTICLES, prepare_issue_smoke


def test_default_smoke_reduces_193_cards_to_14_assessable_issues():
    _, _, issues = prepare_issue_smoke(
        case_id="kcl_criminal_r10_p1_q1_ga", articles=DEFAULT_ARTICLES
    )
    assert len(issues) == 14
    assert {issue.article for issue in issues} == set(DEFAULT_ARTICLES)
    assert all(issue.anchor_card_ids for issue in issues)
