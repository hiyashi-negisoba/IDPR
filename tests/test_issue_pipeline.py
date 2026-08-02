from __future__ import annotations

import pytest

from idpr.candidates import candidate_issues
from idpr.issue_pipeline import (
    IssuePipelineError,
    build_issue_reasoning_packet,
    followup_issues,
    generation_issues,
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


def test_followup_issues_are_limited_to_live_articles_and_relation_roles():
    scope = candidate_issues(
        selected=["art297", "art298"],
        attempt_map={},
    )
    runtime = {
        "relations": {
            "offense_established": [["case-1", "art298"]],
            "offense_undetermined": [],
            "final_offense": [["case-1", "art298"]],
            "attempt_to_consider": [],
            "element_unaddressed": [],
        }
    }
    selected = followup_issues(scope, symbolic_runtime=runtime)
    assert selected
    assert {issue.article for issue in selected} == {"art298"}
    assert {issue.function for issue in selected} <= {
        "guard_issue",
        "stage_issue",
        "concurrence_issue",
        "participation_issue",
    }
    assert all(issue.anchor_card_ids for issue in selected)


def test_symbolic_relation_followup_requires_both_live_offenses():
    scope = candidate_issues(
        selected=["art122", "art227"],
        attempt_map={},
    )
    target = "art122.Ⅲ.2a.concurrence_issue"
    one_live = {
        "relations": {
            "offense_established": [["case-1", "art122"]],
            "offense_undetermined": [],
            "final_offense": [["case-1", "art122"]],
            "attempt_to_consider": [],
            "element_unaddressed": [],
        }
    }
    assert target not in {
        issue.issue_id
        for issue in followup_issues(scope, symbolic_runtime=one_live)
    }

    both_live = {
        "relations": {
            "offense_established": [
                ["case-1", "art122"],
                ["case-1", "art227"],
            ],
            "offense_undetermined": [],
            "final_offense": [
                ["case-1", "art122"],
                ["case-1", "art227"],
            ],
            "attempt_to_consider": [],
            "element_unaddressed": [],
        }
    }
    assert target in {
        issue.issue_id
        for issue in followup_issues(scope, symbolic_runtime=both_live)
    }


def test_reasoning_packet_accepts_scoped_followup_assessments():
    scope = candidate_issues(selected=["art298"], attempt_map={})
    bundle = _bundle(scope)
    followup = next(
        issue for issue in scope.deferred_issues if issue.anchor_card_ids
    )
    bundle["assessments"][followup.issue_id] = {
        "status": "unknown",
        "basis_fact_ids": [],
        "counter_fact_ids": [],
        "missing_facts": ["구체적 사실"],
    }
    packet = build_issue_reasoning_packet(
        scope=scope,
        assessment_bundle=bundle,
        symbolic_runtime={"relations": {}},
    )
    by_id = {issue["issue_id"]: issue for issue in packet["issues"]}
    assert by_id[followup.issue_id]["function"] == followup.function
    assert isinstance(by_id[followup.issue_id]["symbolic_condition"], bool)


def test_generation_plan_omits_speculative_unknown_deferred_issues():
    scope = candidate_issues(selected=["art298"], attempt_map={})
    bundle = _bundle(scope)
    stage = next(
        issue for issue in scope.deferred_issues if issue.function == "stage_issue"
    )
    concurrence = next(
        issue
        for issue in scope.deferred_issues
        if issue.function == "concurrence_issue"
    )
    for issue in (stage, concurrence):
        bundle["assessments"][issue.issue_id] = {
            "status": "unknown",
            "basis_fact_ids": [],
            "counter_fact_ids": [],
            "missing_facts": ["구체적 사실"],
        }
    planned = {
        issue.issue_id
        for issue in generation_issues(
            scope.issues,
            assessment_bundle=bundle,
        )
    }
    assert stage.issue_id in planned
    assert concurrence.issue_id not in planned


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
