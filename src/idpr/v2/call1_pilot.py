"""Pure measurement helpers for the Step 8 Call 1 calibration pilot."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Mapping, Sequence

from idpr.v2.closure import compile_closure
from idpr.v2.registry import DefinitionRegistry


def article_definition_refs(
    registry: DefinitionRegistry, article_catalog: Iterable[Mapping[str, object]]
) -> dict[str, tuple[str, ...]]:
    """Project catalog articles to directly authored offense identities.

    This deliberately uses only ``OffenseDef.identity.statutory_refs``.  A
    DerivedOffenseDef has no identity field, so it is not guessed into this
    article-level proxy.  Empty projections remain auditable ``out_of_registry``
    rows rather than being treated as router misses.
    """
    labels = {
        str(article["key"]): str(article["label"])
        for article in article_catalog
        if isinstance(article.get("key"), str) and isinstance(article.get("label"), str)
    }
    mapped: dict[str, list[str]] = {key: [] for key in labels}
    for entry in registry.by_kind.get("offense", ()):
        identity = entry.payload.get("identity")
        if not isinstance(identity, Mapping):
            continue
        statutory_refs = identity.get("statutory_refs")
        if not isinstance(statutory_refs, Sequence) or isinstance(statutory_refs, str):
            continue
        for article_key, article_label in labels.items():
            if any(
                isinstance(statutory_ref, str) and article_label in statutory_ref
                for statutory_ref in statutory_refs
            ):
                mapped[article_key].append(entry.id)
    return {key: tuple(sorted(set(refs))) for key, refs in mapped.items()}


def case_calibration(
    registry: DefinitionRegistry,
    *,
    seeds: Sequence[str],
    gold_articles: Iterable[str],
    mapped_refs_by_article: Mapping[str, Sequence[str]],
) -> dict[str, Any]:
    """Measure one valid router response without altering its emitted order."""
    ordered_seeds = tuple(seeds)
    full_closure = compile_closure(registry, ordered_seeds)
    prefix_seeds = ordered_seeds[:10]
    prefix_closure = compile_closure(registry, prefix_seeds)
    full_candidates = frozenset(full_closure.candidate_offense_refs)
    prefix_candidates = frozenset(prefix_closure.candidate_offense_refs)

    articles: list[dict[str, Any]] = []
    for article in sorted(set(gold_articles)):
        mapped_refs = tuple(mapped_refs_by_article.get(article, ()))
        if not mapped_refs:
            articles.append({
                "article": article,
                "mapped_refs": [],
                "status": "out_of_registry",
                "raw_success": None,
                "closure_success": None,
                "prefix10_closure_success": None,
                "additional_recovery": None,
            })
            continue
        mapped = frozenset(mapped_refs)
        raw_success = bool(mapped & set(ordered_seeds))
        closure_success = bool(mapped & full_candidates)
        prefix_success = bool(mapped & prefix_candidates)
        articles.append({
            "article": article,
            "mapped_refs": list(mapped_refs),
            "status": "survives" if closure_success else "router_or_closure_miss",
            "raw_success": raw_success,
            "closure_success": closure_success,
            "prefix10_closure_success": prefix_success,
            "additional_recovery": closure_success and not prefix_success,
        })

    return {
        "seeds": list(ordered_seeds),
        "prefix10": list(prefix_seeds),
        "full15": list(ordered_seeds[:15]),
        "mandatory_offense_refs": sorted(full_closure.mandatory_offense_refs),
        "candidate_offense_refs": sorted(full_candidates),
        "prefix10_candidate_offense_refs": sorted(prefix_candidates),
        "gold_articles": articles,
    }


def summarize_calibrations(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate only reportable article paths; retain failed rows separately."""
    counters: Counter[str] = Counter()
    seed_counts: list[int] = []
    frontier_counts: list[int] = []
    probe_counts: list[int] = []
    for row in rows:
        if row.get("error"):
            counters["failed_cases"] += 1
            continue
        seed_counts.append(len(row.get("seeds") or ()))
        closure = row.get("closure") or {}
        frontier_counts.append(int(closure.get("ground_fact_frontier_count", 0) or 0))
        probe_counts.append(int(closure.get("probe_count", 0) or 0))
        calibration = row.get("calibration") or {}
        for article in calibration.get("gold_articles") or ():
            if article.get("status") == "out_of_registry":
                counters["out_of_registry_articles"] += 1
                continue
            counters["mapped_articles"] += 1
            if article.get("raw_success"):
                counters["raw_successes"] += 1
            if article.get("closure_success"):
                counters["closure_successes"] += 1
            if article.get("additional_recovery"):
                counters["additional_recovery"] += 1
            if not article.get("closure_success"):
                counters["router_or_closure_misses"] += 1

    def distribution(values: Sequence[int]) -> dict[str, float | int | None]:
        if not values:
            return {"min": None, "max": None, "mean": None}
        return {
            "min": min(values),
            "max": max(values),
            "mean": round(sum(values) / len(values), 2),
        }

    mapped = counters["mapped_articles"]
    return {
        **dict(sorted(counters.items())),
        "raw_survival_rate": round(counters["raw_successes"] / mapped, 4) if mapped else None,
        "closure_survival_rate": (
            round(counters["closure_successes"] / mapped, 4) if mapped else None
        ),
        "seed_count": distribution(seed_counts),
        "ground_fact_frontier_count": distribution(frontier_counts),
        "probe_count": distribution(probe_counts),
    }


__all__ = ["article_definition_refs", "case_calibration", "summarize_calibrations"]
