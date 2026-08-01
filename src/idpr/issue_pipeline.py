"""Canonical issue-first boundaries for the general KCL pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from idpr.candidates import IssueCandidateSet, candidate_issues
from idpr.neural.fact_graph import fact_tuples
from idpr.neural.issue_assessment import issue_status_rows
from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.compile_scl import QUERY_RELATIONS, compile_rulebase
from idpr.rulebase.scallop import (
    render_fact_layer,
    render_issue_statuses,
    run_program,
    runtime_version,
)


class IssuePipelineError(ValueError):
    """Raised when two persisted issue-first stage boundaries disagree."""


def issue_candidate_row(
    case_id: str,
    candidates: IssueCandidateSet,
    *,
    retrieved_issue_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Persist the issue hierarchy only; flat card ids are not a stage boundary."""
    return {
        "sub_question_id": case_id,
        **candidates.as_dict(),
        "issue_ids": list(candidates.issue_ids),
        "initial_issue_ids": [
            issue.issue_id for issue in candidates.initial_issues
        ],
        "deferred_issue_ids": [
            issue.issue_id for issue in candidates.deferred_issues
        ],
        "retrieved_issue_ids": list(retrieved_issue_ids),
    }


def scope_from_l0_row(
    row: Mapping[str, Any], *, corpus: CardCorpus | None = None
) -> IssueCandidateSet:
    """Rebuild and verify the full issue scope from one persisted L0 row."""
    corpus = corpus or card_corpus()
    scope = candidate_issues(
        selected=tuple(row.get("from_model", ())),
        retrieved=tuple(row.get("from_retrieval", ())),
        corpus=corpus,
    )
    expected_articles = tuple(row.get("articles", ()))
    expected_issues = tuple(row.get("issue_ids", ()))
    errors: list[str] = []
    if expected_articles and expected_articles != scope.articles:
        errors.append("persisted articles differ from the live issue scope")
    if expected_issues and expected_issues != scope.issue_ids:
        errors.append("persisted issue_ids differ from the live issue catalog")
    if "card_ids" in row:
        errors.append("flat card_ids are forbidden in an issue-first L0 row")
    if errors:
        raise IssuePipelineError("; ".join(errors))
    return scope


def initial_issue_payloads(
    scope: IssueCandidateSet,
    *,
    corpus: CardCorpus | None = None,
    details_by_issue: Mapping[str, Sequence[str]] | None = None,
) -> list[dict[str, object]]:
    """Model payloads for initial issues, with optional same-issue details."""
    corpus = corpus or card_corpus()
    details_by_issue = details_by_issue or {}
    known = {issue.issue_id for issue in scope.initial_issues}
    outside = set(details_by_issue) - known
    if outside:
        raise IssuePipelineError(
            f"details refer to non-initial issues: {sorted(outside)}"
        )
    return [
        issue.model_payload(
            corpus.by_id,
            detail_card_ids=details_by_issue.get(issue.issue_id, ()),
        )
        for issue in scope.initial_issues
    ]


def run_issue_symbolic(
    *,
    case_id: str,
    fact_graph: Mapping[str, Any],
    assessment_bundle: Mapping[str, Any],
    work_dir: Path,
    corpus: CardCorpus | None = None,
    name: str = "issue_runtime",
) -> dict[str, Any]:
    """Run validated issue assessments through the canonical Scallop boundary."""
    corpus = corpus or card_corpus()
    program = (
        compile_rulebase(corpus=corpus)
        + render_fact_layer(
            case_id,
            fact_tuples(fact_graph, case_id=case_id),
        )
        + render_issue_statuses(case_id, issue_status_rows(assessment_bundle))
    )
    results = run_program(program, QUERY_RELATIONS, work_dir, name=name)
    return {
        "scli_version": runtime_version(),
        "observed_nonempty": {
            relation: bool(rows) for relation, rows in results.items()
        },
        "relations": {
            relation: [list(row) for row in rows]
            for relation, rows in results.items()
        },
    }


def build_issue_reasoning_packet(
    *,
    scope: IssueCandidateSet,
    assessment_bundle: Mapping[str, Any],
    symbolic_runtime: Mapping[str, Any],
    corpus: CardCorpus | None = None,
    details_by_issue: Mapping[str, Sequence[str]] | None = None,
) -> dict[str, Any]:
    """Deterministic issue-level handoff for the later answer-generation phase."""
    corpus = corpus or card_corpus()
    details_by_issue = details_by_issue or {}
    assessments = assessment_bundle.get("assessments", {})
    if not isinstance(assessments, Mapping):
        raise IssuePipelineError("assessment_bundle.assessments must be an object")
    expected = {issue.issue_id for issue in scope.initial_issues}
    if set(assessments) != expected:
        raise IssuePipelineError(
            "assessment issue ids differ from the initial issue scope"
        )

    units: list[dict[str, Any]] = []
    for issue in scope.initial_issues:
        assessment = assessments[issue.issue_id]
        detail_ids = tuple(details_by_issue.get(issue.issue_id, ()))
        outside = set(detail_ids) - set(issue.retrieval_card_ids)
        if outside:
            raise IssuePipelineError(
                f"{issue.issue_id}: details outside issue: {sorted(outside)}"
            )
        units.append(
            {
                "issue_id": issue.issue_id,
                "article": issue.article,
                "article_label": issue.article_label,
                "offense": issue.offense,
                "title": issue.title,
                "status": assessment["status"],
                "basis_fact_ids": list(assessment["basis_fact_ids"]),
                "counter_fact_ids": list(assessment["counter_fact_ids"]),
                "missing_facts": list(assessment["missing_facts"]),
                "anchor_rules": [
                    {
                        "card_id": card_id,
                        "proposition": corpus.by_id[card_id].proposition,
                    }
                    for card_id in issue.anchor_card_ids
                ],
                "detail_rules": [
                    {
                        "card_id": card_id,
                        "proposition": corpus.by_id[card_id].proposition,
                    }
                    for card_id in detail_ids
                ],
            }
        )
    return {
        "version": "1.0.0",
        "case_id": assessment_bundle.get("case_id"),
        "articles": list(scope.articles),
        "issues": units,
        "symbolic_runtime": dict(symbolic_runtime),
    }
