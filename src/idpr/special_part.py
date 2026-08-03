"""Closed-world planning boundary for the article-local special-part pipeline."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from idpr.candidates import IssueCandidateSet, candidate_issues
from idpr.issue_pipeline import issue_candidate_row
from idpr.rulebase.cards import CardCorpus, card_corpus


PIPELINE_MODE = "special_part_light"
MAX_PLANNED_ARTICLES = 12


class SpecialPartPlanError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def planner_schema(candidate_articles: Sequence[str]) -> dict[str, Any]:
    """Constrain planning to assessable articles already found by broad retrieval."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["selected", "scope_note"],
        "properties": {
            "selected": {
                "type": "array",
                "minItems": 0,
                "maxItems": min(MAX_PLANNED_ARTICLES, len(candidate_articles)),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["article", "actor", "source_quote", "reason"],
                    "properties": {
                        "article": {"type": "string", "enum": list(candidate_articles)},
                        "actor": {"type": "string", "minLength": 1, "maxLength": 80},
                        "source_quote": {"type": "string", "minLength": 1, "maxLength": 400},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 300},
                    },
                },
            },
            "scope_note": {"type": "string", "minLength": 1, "maxLength": 400},
        },
    }


def assessable_article_scope(
    articles: Sequence[str], *, corpus: CardCorpus | None = None
) -> IssueCandidateSet:
    """Load only standalone constituent-element issues; never expand attempt articles."""
    return candidate_issues(
        selected=tuple(dict.fromkeys(articles)),
        attempt_map={},
        corpus=corpus or card_corpus(),
    )


def planner_payload(
    *,
    case_id: str,
    question_text: str,
    question_prompt: str,
    broad_articles: Sequence[str],
    corpus: CardCorpus | None = None,
) -> tuple[dict[str, Any], tuple[str, ...]]:
    """Expose the case and compact element summaries, but no rubric or gold fields."""
    corpus = corpus or card_corpus()
    broad_scope = assessable_article_scope(broad_articles, corpus=corpus)
    grouped: dict[str, list[Any]] = {}
    for issue in broad_scope.initial_issues:
        grouped.setdefault(issue.article, []).append(issue)
    candidate_articles = tuple(
        article for article in broad_scope.articles if grouped.get(article)
    )
    summaries = []
    for article in candidate_articles:
        issues = grouped[article]
        summaries.append(
            {
                "article": article,
                "article_label": issues[0].article_label,
                "offense": issues[0].offense,
                "constituent_issues": [
                    {
                        "title": issue.title,
                        "anchor_rules": [
                            corpus.by_id[card_id].proposition
                            for card_id in issue.anchor_card_ids
                        ]
                        + [rule.proposition for rule in issue.reviewed_anchor_rules],
                    }
                    for issue in issues
                ],
            }
        )
    return (
        {
            "case_id": case_id,
            "case_text": question_text,
            "question_prompt": question_prompt,
            "candidate_articles": summaries,
        },
        candidate_articles,
    )


def validate_plan(
    output: Mapping[str, Any], *, candidate_articles: Sequence[str], question_text: str
) -> tuple[tuple[str, ...], tuple[dict[str, str], ...]]:
    """Reject minted articles, duplicate selections, and evidence not quoted by the case."""
    errors: list[str] = []
    raw = output.get("selected")
    if not isinstance(raw, list):
        raise SpecialPartPlanError(["selected must be an array"])
    allowed = set(candidate_articles)
    seen: set[str] = set()
    entries: list[dict[str, str]] = []
    for index, item in enumerate(raw):
        where = f"selected[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{where}: not an object")
            continue
        article = item.get("article")
        actor = item.get("actor")
        quote = item.get("source_quote")
        reason = item.get("reason")
        if article not in allowed:
            errors.append(f"{where}: article is outside the broad candidate pool")
        elif article in seen:
            errors.append(f"{where}: duplicate article {article}")
        else:
            seen.add(str(article))
        for name, value in (("actor", actor), ("source_quote", quote), ("reason", reason)):
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{where}: {name} is required")
        if isinstance(quote, str) and quote.strip() and quote.strip() not in question_text:
            errors.append(f"{where}: source_quote is not an exact case-text substring")
        if article in allowed and isinstance(actor, str) and isinstance(quote, str) and isinstance(reason, str):
            entries.append(
                {
                    "article": str(article),
                    "actor": actor.strip(),
                    "source_quote": quote.strip(),
                    "reason": reason.strip(),
                }
            )
    if len(entries) > MAX_PLANNED_ARTICLES:
        errors.append(f"selected exceeds {MAX_PLANNED_ARTICLES} articles")
    if errors:
        raise SpecialPartPlanError(errors)
    return tuple(entry["article"] for entry in entries), tuple(entries)


def planned_candidate_row(
    *,
    case_id: str,
    selected_articles: Sequence[str],
    entries: Sequence[Mapping[str, str]],
    scope_note: str,
    broad_articles: Sequence[str],
    usage: Mapping[str, Any] | None = None,
    corpus: CardCorpus | None = None,
) -> dict[str, Any]:
    scope = assessable_article_scope(selected_articles, corpus=corpus)
    row = issue_candidate_row(case_id, scope)
    row.update(
        {
            "pipeline_mode": PIPELINE_MODE,
            "scope_status": "in_scope" if scope.articles else "out_of_scope",
            "broad_articles": list(broad_articles),
            "planner_entries": [dict(entry) for entry in entries],
            "scope_note": scope_note,
            "planner_usage": dict(usage or {}),
        }
    )
    return row
