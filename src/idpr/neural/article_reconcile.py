"""Upstream reconciliation of LLM-selected and retrieved article candidates.

The reconciler is deliberately narrower than Call 2.  It decides whether a candidate
article has a concrete path into the scoped question; it never decides whether the
article's elements are satisfied.  Candidate identifiers remain host-minted and closed
by guided decoding.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "0.1.0-experiment"


class ArticleReconcileError(ValueError):
    """Raised when a reconciliation response violates its closed candidate contract."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def reconciliation_schema(candidate_articles: Iterable[str]) -> dict[str, Any]:
    """Return a schema that permits only articles admitted by either upstream channel."""
    articles = list(dict.fromkeys(candidate_articles))
    if not articles:
        raise ValueError("candidate_articles must not be empty")
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["selected"],
        "properties": {
            "selected": {
                "type": "array",
                "minItems": 1,
                "maxItems": len(articles),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["article", "reason"],
                    "properties": {
                        "article": {"type": "string", "enum": articles},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 300},
                    },
                },
            }
        },
    }


def reconciliation_matrix_schema(candidate_articles: Iterable[str]) -> dict[str, Any]:
    """Force an explicit keep/drop decision for every candidate in the union."""
    articles = list(dict.fromkeys(candidate_articles))
    if not articles:
        raise ValueError("candidate_articles must not be empty")
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["decisions"],
        "properties": {
            "decisions": {
                "type": "array",
                "minItems": len(articles),
                "maxItems": len(articles),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["article", "decision", "reason"],
                    "properties": {
                        "article": {"type": "string", "enum": articles},
                        "decision": {"type": "string", "enum": ["keep", "drop"]},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 300},
                    },
                },
            }
        },
    }


def reconciliation_payload(
    *,
    case_id: str,
    question_text: str,
    question_prompt: str,
    candidates: Sequence[Mapping[str, Any]],
    upstream_hypotheses: Sequence[str] = (),
) -> dict[str, Any]:
    """Build the input whitelist: scoped case text plus auditable candidate evidence."""
    allowed_keys = {
        "article",
        "label",
        "offense",
        "admission_channels",
        "model_reason",
        "retrieval_rank",
        "retrieved_issue",
        "retrieved_rules",
    }
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, candidate in enumerate(candidates):
        unknown = set(candidate) - allowed_keys
        if unknown:
            raise ValueError(f"candidates[{index}] has non-whitelisted keys: {sorted(unknown)}")
        article = candidate.get("article")
        if not isinstance(article, str) or not article:
            raise ValueError(f"candidates[{index}].article is required")
        if article in seen:
            raise ValueError(f"duplicate candidate article: {article}")
        seen.add(article)
        normalized.append(dict(candidate))
    if not normalized:
        raise ValueError("candidates must not be empty")
    payload = {
        "case_id": case_id,
        "case_text": question_text,
        "question_prompt": question_prompt,
        "candidates": normalized,
    }
    hypotheses = list(dict.fromkeys(value.strip() for value in upstream_hypotheses if value.strip()))
    if hypotheses:
        payload["upstream_hypotheses"] = hypotheses
    return payload


def validate_reconciliation(
    payload: Mapping[str, Any], *, allowed_articles: Iterable[str]
) -> tuple[tuple[str, ...], tuple[dict[str, str], ...]]:
    """Validate and deduplicate a model response without inventing a fallback selection."""
    allowed = set(allowed_articles)
    raw = payload.get("selected")
    if not isinstance(raw, list) or not raw:
        raise ArticleReconcileError(["selected must be a non-empty array"])

    errors: list[str] = []
    seen: dict[str, dict[str, str]] = {}
    for index, item in enumerate(raw):
        where = f"selected[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{where}: not an object")
            continue
        article = item.get("article")
        reason = item.get("reason")
        if article not in allowed:
            errors.append(f"{where}: {article!r} is not an admitted candidate")
            continue
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where}: reason is required")
            continue
        seen.setdefault(article, {"article": article, "reason": reason.strip()})
    if errors:
        raise ArticleReconcileError(errors)
    entries = tuple(seen.values())
    return tuple(entry["article"] for entry in entries), entries


def validate_reconciliation_matrix(
    payload: Mapping[str, Any], *, allowed_articles: Iterable[str]
) -> tuple[tuple[str, ...], tuple[dict[str, str], ...], tuple[dict[str, str], ...]]:
    """Require one auditable decision per candidate, with neither omissions nor duplicates."""
    allowed_order = tuple(dict.fromkeys(allowed_articles))
    allowed = set(allowed_order)
    raw = payload.get("decisions")
    if not isinstance(raw, list):
        raise ArticleReconcileError(["decisions must be an array"])

    errors: list[str] = []
    seen: dict[str, dict[str, str]] = {}
    for index, item in enumerate(raw):
        where = f"decisions[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{where}: not an object")
            continue
        article = item.get("article")
        decision = item.get("decision")
        reason = item.get("reason")
        if article not in allowed:
            errors.append(f"{where}: {article!r} is not an admitted candidate")
            continue
        if article in seen:
            errors.append(f"{where}: duplicate decision for {article}")
            continue
        if decision not in {"keep", "drop"}:
            errors.append(f"{where}: decision must be keep or drop")
            continue
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where}: reason is required")
            continue
        seen[article] = {
            "article": article,
            "decision": decision,
            "reason": reason.strip(),
        }
    missing = [article for article in allowed_order if article not in seen]
    if missing:
        errors.append(f"missing decisions: {missing}")
    if errors:
        raise ArticleReconcileError(errors)
    decisions = tuple(seen[article] for article in allowed_order)
    kept_entries = tuple(
        {"article": entry["article"], "reason": entry["reason"]}
        for entry in decisions
        if entry["decision"] == "keep"
    )
    if not kept_entries:
        raise ArticleReconcileError(["matrix must keep at least one candidate"])
    return (
        tuple(entry["article"] for entry in kept_entries),
        kept_entries,
        decisions,
    )
