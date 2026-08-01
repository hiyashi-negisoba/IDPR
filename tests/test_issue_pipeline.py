from __future__ import annotations

import pytest

from idpr.candidates import candidate_issues
from idpr.issue_pipeline import (
    IssuePipelineError,
    build_issue_reasoning_packet,
    initial_issue_payloads,
    issue_candidate_row,
    scope_from_l0_row,
)
from idpr.rulebase.cards import PROJECT_ROOT, card_corpus


def _bundle(scope):
    return {
        "version": "2.0.0",
        "case_id": "case-1",
        "assessments": {
            issue.issue_id: {
                "status": "unknown",
                "basis_fact_ids": [],
                "counter_fact_ids": [],
                "missing_facts": ["구체적 사실"],
            }
            for issue in scope.initial_issues
        },
    }


def test_l0_row_rehydrates_the_same_issue_scope_without_card_ids():
    corpus = card_corpus()
    scope = candidate_issues(selected=["art329"], corpus=corpus)
    row = {
        "articles": list(scope.articles),
        "from_model": ["art329"],
        "from_retrieval": [],
        "issue_ids": list(scope.issue_ids),
    }
    rebuilt = scope_from_l0_row(row, corpus=corpus)
    assert rebuilt.issue_ids == scope.issue_ids
    row["card_ids"] = []
    with pytest.raises(IssuePipelineError, match="flat card_ids"):
        scope_from_l0_row(row, corpus=corpus)


def test_initial_payloads_and_reasoning_packet_remain_issue_keyed():
    corpus = card_corpus()
    scope = candidate_issues(selected=["art329"], corpus=corpus)
    payloads = initial_issue_payloads(scope, corpus=corpus)
    assert {item["issue_id"] for item in payloads} == {
        issue.issue_id for issue in scope.initial_issues
    }
    packet = build_issue_reasoning_packet(
        scope=scope,
        assessment_bundle=_bundle(scope),
        symbolic_runtime={"relations": {}},
        corpus=corpus,
    )
    assert {item["issue_id"] for item in packet["issues"]} == {
        issue.issue_id for issue in scope.initial_issues
    }
    assert "card_status" not in repr(packet)
    assert "card_assessments" not in repr(packet)


def test_reasoning_packet_rejects_partial_issue_assessments():
    scope = candidate_issues(selected=["art329"])
    bundle = _bundle(scope)
    bundle["assessments"].pop(next(iter(bundle["assessments"])))
    with pytest.raises(IssuePipelineError, match="differ"):
        build_issue_reasoning_packet(
            scope=scope,
            assessment_bundle=bundle,
            symbolic_runtime={},
        )


def test_general_runtime_scripts_do_not_import_flat_card_boundaries():
    forbidden = (
        "candidate_articles(",
        "from idpr.neural.card_assessment",
        "card_status_rows",
        "render_card_statuses",
    )
    for relative in (
        "scripts/run_l0_candidates.py",
        "scripts/run_call2_issue_smoke.py",
        "src/idpr/issue_pipeline.py",
    ):
        source = (PROJECT_ROOT / relative).read_text(encoding="utf-8")
        assert all(name not in source for name in forbidden), relative


def test_l0_serialization_contains_issue_ids_and_no_flat_card_ids():
    scope = candidate_issues(selected=["art329"])
    row = issue_candidate_row("case-1", scope)
    assert row["issue_ids"] == list(scope.issue_ids)
    assert row["initial_issue_ids"]
    assert "card_ids" not in row
