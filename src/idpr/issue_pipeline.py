"""Canonical issue-first boundaries for the general KCL pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from idpr.candidates import IssueCandidateSet, candidate_issues
from idpr.neural.fact_graph import fact_tuples
from idpr.neural.issue_assessment import issue_status_rows
from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.compile_scl import QUERY_RELATIONS, compile_rulebase
from idpr.rulebase.doctrine import UNCONDITIONAL, load_doctrine
from idpr.rulebase.issue_catalog_v2 import (
    ASSESS_ISSUE,
    RELATION_CONDITION,
    RETRIEVE_GUARD,
    STAGE_ISSUE,
    IssuePacket,
)
from idpr.rulebase.scallop import (
    render_fact_layer,
    render_issue_statuses,
    run_program,
    runtime_version,
)


class IssuePipelineError(ValueError):
    """Raised when two persisted issue-first stage boundaries disagree."""


def _symbolic_condition_card_ids(corpus: CardCorpus) -> set[str]:
    doctrine = load_doctrine(corpus.by_article())
    return {
        condition
        for _, _, condition in (
            *doctrine.absorbed_by,
            *doctrine.imaginative_concurrence,
        )
        if condition != UNCONDITIONAL
    }


def generation_issues(
    issues: Sequence[IssuePacket],
    *,
    assessment_bundle: Mapping[str, Any],
    corpus: CardCorpus | None = None,
) -> tuple[IssuePacket, ...]:
    """Keep mandatory elements and legally material followups for Call 3."""
    corpus = corpus or card_corpus()
    assessments = assessment_bundle.get("assessments", {})
    if not isinstance(assessments, Mapping):
        raise IssuePipelineError("assessment_bundle.assessments must be an object")
    condition_ids = _symbolic_condition_card_ids(corpus)
    return tuple(
        issue
        for issue in issues
        if issue.issue_id in assessments
        and (
            issue.runtime == ASSESS_ISSUE
            or assessments[issue.issue_id].get("status") != "unknown"
            or issue.function == STAGE_ISSUE
            or bool(set(issue.member_card_ids) & condition_ids)
        )
    )


def _relation_articles(
    symbolic_runtime: Mapping[str, Any], relation: str
) -> set[str]:
    relations = symbolic_runtime.get("relations", {})
    if not isinstance(relations, Mapping):
        raise IssuePipelineError("symbolic_runtime.relations must be an object")
    rows = relations.get(relation, ())
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise IssuePipelineError(f"symbolic relation {relation} must be an array")
    articles: set[str] = set()
    for row in rows:
        if (
            isinstance(row, Sequence)
            and not isinstance(row, (str, bytes))
            and len(row) >= 2
        ):
            articles.add(str(row[1]))
    return articles


def followup_issues(
    scope: IssueCandidateSet,
    *,
    symbolic_runtime: Mapping[str, Any],
    retrieved_issue_ids: Sequence[str] = (),
    corpus: CardCorpus | None = None,
) -> tuple[IssuePacket, ...]:
    """Select the small post-element set needed before answer generation.

    The first Call-2 pass deliberately contains constituent elements only.  Once that
    pass has produced symbolic offense signals, relation and defence issues are useful
    only for articles that remain live.  Selecting them here keeps stage, participation,
    concurrence, and guards out of unrelated candidate articles while ensuring Call 3
    does not have to perform fresh legal assessment while writing.
    """
    corpus = corpus or card_corpus()
    active_articles: set[str] = set()
    for relation in (
        "offense_established",
        "offense_undetermined",
        "final_offense",
        "attempt_to_consider",
    ):
        active_articles.update(_relation_articles(symbolic_runtime, relation))
    # An article with only unknown elements does not appear in the four relations above,
    # but its uncertainty must still be explained rather than silently dropped.
    active_articles.update(_relation_articles(symbolic_runtime, "element_unaddressed"))

    doctrine = load_doctrine(corpus.by_article())
    condition_requirements: dict[str, frozenset[str]] = {}
    for first, second, condition in (
        *doctrine.absorbed_by,
        *doctrine.imaginative_concurrence,
    ):
        if condition != UNCONDITIONAL:
            condition_requirements[condition] = frozenset((first, second))
    configured_condition_ids = set(condition_requirements)

    retrieved = set(retrieved_issue_ids)
    selected: list[IssuePacket] = []
    for issue in scope.deferred_issues:
        if issue.article not in active_articles or not (
            issue.anchor_card_ids or issue.reviewed_anchor_rules
        ):
            continue
        configured_conditions = set(issue.member_card_ids) & configured_condition_ids
        if configured_conditions and not any(
            condition_requirements[condition] <= active_articles
            for condition in configured_conditions
        ):
            # A binary relation is not a live question until both offences survive the
            # element pass.  This is also what prevents an article-local umbrella issue
            # from deciding a relation to an offence that never entered the case.
            continue
        if issue.runtime in {RELATION_CONDITION, RETRIEVE_GUARD}:
            selected.append(issue)
        elif issue.issue_id in retrieved:
            selected.append(issue)
    return tuple(selected)


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
    article_local = row.get("pipeline_mode") == "special_part_light"
    scope = candidate_issues(
        selected=tuple(row.get("from_model", ())),
        retrieved=tuple(row.get("from_retrieval", ())),
        corpus=corpus,
        attempt_map={} if article_local else None,
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
    article_local: bool = False,
) -> dict[str, Any]:
    """Deterministic issue-level handoff for the later answer-generation phase."""
    corpus = corpus or card_corpus()
    details_by_issue = details_by_issue or {}
    assessments = assessment_bundle.get("assessments", {})
    if not isinstance(assessments, Mapping):
        raise IssuePipelineError("assessment_bundle.assessments must be an object")
    required = {issue.issue_id for issue in scope.initial_issues}
    known = {issue.issue_id for issue in scope.issues}
    supplied = set(assessments)
    if not required <= supplied or not supplied <= known:
        raise IssuePipelineError(
            "assessment issue ids differ from scope: they must contain the initial "
            "issues and stay inside the selected hierarchy"
        )

    symbolic_condition_card_ids = (
        set() if article_local else _symbolic_condition_card_ids(corpus)
    )
    planned_for_generation = (
        {issue.issue_id for issue in scope.initial_issues}
        if article_local
        else {
            issue.issue_id
            for issue in generation_issues(
                scope.issues,
                assessment_bundle=assessment_bundle,
                corpus=corpus,
            )
        }
    )

    units: list[dict[str, Any]] = []
    for issue in scope.issues:
        if issue.issue_id not in supplied:
            continue
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
                "function": issue.function,
                "runtime": issue.runtime,
                "symbolic_condition": bool(
                    set(issue.member_card_ids) & symbolic_condition_card_ids
                ),
                "include_in_generation": issue.issue_id in planned_for_generation,
                "status": assessment["status"],
                "basis_fact_ids": list(assessment["basis_fact_ids"]),
                "counter_fact_ids": list(assessment["counter_fact_ids"]),
                "missing_facts": list(assessment["missing_facts"]),
                "anchor_rules": [
                    {
                        "rule_id": card_id,
                        "proposition": corpus.by_id[card_id].proposition,
                        "basis_card_ids": [card_id],
                        "origin": "reviewed_card",
                    }
                    for card_id in issue.anchor_card_ids
                ]
                + [
                    {
                        "rule_id": rule.rule_id,
                        "proposition": rule.proposition,
                        "basis_card_ids": list(rule.basis_card_ids),
                        "origin": "legal_review",
                    }
                    for rule in issue.reviewed_anchor_rules
                ],
                "detail_rules": [
                    {
                        "rule_id": card_id,
                        "proposition": corpus.by_id[card_id].proposition,
                        "basis_card_ids": [card_id],
                        "origin": "retrieved_detail",
                    }
                    for card_id in detail_ids
                ],
            }
        )
    return {
        "version": "1.0.0",
        "pipeline_mode": "special_part_light" if article_local else "general_issue_scallop",
        "case_id": assessment_bundle.get("case_id"),
        "articles": list(scope.articles),
        "issues": units,
        "symbolic_runtime": dict(symbolic_runtime),
    }
