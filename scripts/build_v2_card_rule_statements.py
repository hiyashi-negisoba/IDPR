#!/usr/bin/env python3
"""Retrieve reviewed-card norm sentences for the P condition (ANSWERPLAN_SPEC 5.5).

The search unit is `(offence instance, predicate)` and so is the output key.  Attaching
cards to the instance instead would lose which element made that offence stand, fail or
stay open, and that distinction is the reason this channel exists.

Three tiers, in order:

1. **Bridge.**  `data/v2/card_target_issue_bridge.yaml` fixes the parent issue for a
   reviewed `(offense_ref, predicate_ref)` route.  A retrieval score never chooses the
   parent issue.
2. **Article family.**  Without a route, the instance's authored statutory identity scopes
   the issue family, and the hybrid ranks cards only inside it.
3. **Nothing.**  No route and no article scope means no cards.  The plan then carries the
   authored `legal_standard` and `governing_provision` alone, which is exactly the N
   condition for that finding.

The output is a retrieval artifact, not a plan: `scripts/build_v2_answer_plan.py --rule-
statements` injects it.  Nothing here reads the dataset's gold `supporting_precedents` or
its rubrics, and nothing here can change a truth -- statements are copied verbatim from
reviewed cards and land only in `rule_statements[]`.

`--dry-run` runs the tier assignment on CPU without loading either model, which is how the
search scope is sized before spending a GPU allocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import _episode_quotes, instance_ref
from idpr.v2.runtime.card_issue_bridge import project_offense_articles
from idpr.v2.runtime.grounding import predicate_definitions

BE_SNAPSHOT = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/models--google--embeddinggemma-300m/"
    "snapshots/57c266a740f537b4dc058e1b0cda161fd15afa75"
)
CE_SNAPSHOT = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/models--BAAI--bge-reranker-v2-m3/"
    "snapshots/953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"
)
DENSE_CACHE = ROOT / "data/eval/cache/cards_embeddinggemma-300m_7512d150955707d6.json"

TIER_BRIDGE = "bridge_route"
TIER_ARTICLE = "article_family"
TIER_NONE = "no_grounds"


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


#: The query is the occurrence's exact factual quote (SPEC 5.5-2), which is the same span
#: the plan shows the writer.  Reusing the plan's own extractor keeps the two from drifting.
episode_quotes = _episode_quotes


def targets_for_case(
    registry: Any,
    e2e_row: dict[str, Any],
    call2_row: dict[str, Any],
    binding_row: dict[str, Any],
    plan_row: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Every `(instance, predicate)` the plan will show, in all three truth lists.

    Scope follows SPEC 5.4-3: not only established instances, and not only satisfied
    findings.  Explaining why an element failed or stayed open is where the norm behind it
    matters most.
    """
    truths = call2_row.get("case_truths") or []
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for entry in e2e_row.get("liability_results") or []:
        instance = entry.get("instance_key") or {}
        ref = instance_ref(instance)
        offense_ref = str(instance.get("offense_ref", ""))
        quotes = episode_quotes(
            binding_row,
            str(instance.get("occurrence_id", "")),
            plan_row,
        )
        for row in truths:
            if instance_ref(row.get("instance_key") or {}) != ref:
                continue
            predicate_ref = str(row.get("predicate_ref", ""))
            if not predicate_ref or (ref, predicate_ref) in seen:
                continue
            seen.add((ref, predicate_ref))
            out.append(
                {
                    "instance_ref": ref,
                    "offense_ref": offense_ref,
                    "predicate_ref": predicate_ref,
                    "truth": str(row.get("truth", "")),
                    "episode_quotes": quotes,
                }
            )
    return out


def assign_tier(
    registry: Any,
    routes: dict[tuple[str, str], str],
    issue_by_id: dict[str, Any],
    issues_by_article: dict[str, list[Any]],
    target: dict[str, Any],
) -> dict[str, Any]:
    """Decide the tier and the candidate issue scope.  No card is scored here."""
    route_issue = routes.get((target["offense_ref"], target["predicate_ref"]))
    if route_issue is not None and route_issue in issue_by_id:
        return {**target, "tier": TIER_BRIDGE, "issue_ids": [route_issue]}

    if not target["episode_quotes"]:
        return {**target, "tier": TIER_NONE, "issue_ids": [], "reason": "no episode quote"}

    projection = project_offense_articles(registry, target["offense_ref"])
    family = [
        issue.issue_id
        for key in projection.article_keys
        for issue in issues_by_article.get(key, ())
    ]
    if not family:
        return {**target, "tier": TIER_NONE, "issue_ids": [], "reason": projection.status}
    return {**target, "tier": TIER_ARTICLE, "issue_ids": family}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--e2e-results", type=Path, required=True)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument(
        "--plan-artifact",
        type=Path,
        required=True,
        help="planner provenance used to resolve derived occurrence source_binding_ids",
    )
    parser.add_argument("--bridge", type=Path, default=ROOT / "data/v2/card_target_issue_bridge.yaml")
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--top-k-cards", type=int, default=2)
    parser.add_argument("--shortlist", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true", help="tier assignment only, no model")
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    issues_by_article: dict[str, list[Any]] = {}
    for issue in issues:
        issues_by_article.setdefault(issue.article, []).append(issue)

    bridge_doc = yaml.safe_load(args.bridge.read_text(encoding="utf-8"))
    routes = {
        (str(row["offense_ref"]), str(row["predicate_ref"])): str(row["issue_id"])
        for row in bridge_doc["routes"]
    }
    if len(routes) != len(bridge_doc["routes"]):
        raise ValueError("bridge contains duplicate routes")

    e2e = {row["sub_question_id"]: row for row in rows(args.e2e_results)}
    call2 = {row["sub_question_id"]: row for row in rows(args.call2_artifact)}
    bindings = {row["sub_question_id"]: row for row in rows(args.issue_bindings)}
    plans = {row["sub_question_id"]: row for row in rows(args.plan_artifact)}
    missing = set(e2e) - (set(call2) & set(bindings) & set(plans))
    if missing:
        raise ValueError(f"artifacts do not cover the same cases: {sorted(missing)[:3]}")

    pending: list[dict[str, Any]] = []
    for case_id, e2e_row in e2e.items():
        for target in targets_for_case(
            registry,
            e2e_row,
            call2[case_id],
            bindings[case_id],
            plans[case_id],
        ):
            assigned = assign_tier(registry, routes, issue_by_id, issues_by_article, target)
            pending.append({"case_id": case_id, **assigned})

    tiers = Counter(str(value["tier"]) for value in pending)
    reasons = Counter(str(value.get("reason", "")) for value in pending if value["tier"] == TIER_NONE)
    truths = Counter(f"{value['tier']}/{value['truth']}" for value in pending)
    summary: dict[str, Any] = {
        "cases": len(e2e),
        "targets": len(pending),
        "tiers": dict(tiers),
        "tier_by_truth": dict(truths),
        "no_grounds_reasons": dict(reasons),
        "searched": tiers[TIER_BRIDGE] + tiers[TIER_ARTICLE],
    }

    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    for path in (BE_SNAPSHOT, CE_SNAPSHOT, DENSE_CACHE):
        if not path.exists():
            raise RuntimeError(f"RETRIEVAL_UNAVAILABLE: missing {path}")

    from idpr.retrieval import (
        DenseIndex,
        LexicalIndex,
        issue_retrieval_queries,
        reciprocal_rank_fusion,
    )
    from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

    encoder = SentenceTransformerEncoder(model_id=str(BE_SNAPSHOT), batch_size=32)
    reranker = CrossEncoderReranker(model_id=str(CE_SNAPSHOT), batch_size=32)
    cards = tuple(corpus.cards)
    card_index = {card.id: index for index, card in enumerate(cards)}
    lexical = LexicalIndex.build(tuple(card.proposition for card in cards))
    dense = DenseIndex(json.loads(DENSE_CACHE.read_text(encoding="utf-8")))

    searchable = [value for value in pending if value["tier"] != TIER_NONE]
    for value in searchable:
        predicate = predicate_definitions(registry, (value["predicate_ref"],))[0]
        focus = tuple(
            text
            for text in (predicate.canonical_meaning, predicate.legal_standard or "")
            if text
        )
        facts = tuple({"assertion": {"source_quote": quote}} for quote in value["episode_quotes"])
        if value["tier"] == TIER_BRIDGE:
            # The bridge fixed one parent issue, so its title legitimately prefixes the query.
            queries = issue_retrieval_queries(
                issue_by_id[value["issue_ids"][0]], facts or ({"assertion": {}},), focus_texts=focus
            )
            value["query"] = queries[0] if queries else " ".join(focus)
        else:
            # The article family holds many issues and none of them is chosen yet.  Prefixing
            # with an arbitrary member would tilt the ranking toward that member's offence,
            # so the query stays what SPEC 5.5-2 says it is: the occurrence quote and the
            # predicate's own meaning.
            value["query"] = " ".join(dict.fromkeys((*focus, *value["episode_quotes"])))

    query_vectors = encoder.encode([value["query"] for value in searchable], is_query=True)
    shortlists: list[list[int]] = []
    for value, vector in zip(searchable, query_vectors):
        candidate_ids = dict.fromkeys(
            card_id
            for issue_id in value["issue_ids"]
            for card_id in issue_by_id[issue_id].retrieval_card_ids
        )
        candidates = [card_index[card_id] for card_id in candidate_ids if card_id in card_index]
        if not candidates:
            shortlists.append([])
            continue
        lexical_scores = lexical.scores(value["query"])
        dense_scores = dense.scores(vector)
        fused = reciprocal_rank_fusion(
            (
                sorted(candidates, key=lambda i: (-lexical_scores[i], i)),
                sorted(candidates, key=lambda i: (-dense_scores[i], i)),
            )
        )
        shortlists.append(sorted(candidates, key=lambda i: (-fused[i], i))[: args.shortlist])

    pairs = [
        (value["query"], cards[index].proposition)
        for value, shortlist in zip(searchable, shortlists)
        for index in shortlist
    ]
    scores = (
        [float(score) for score in reranker._load().predict(pairs, batch_size=32, show_progress_bar=False)]
        if pairs
        else []
    )

    # First pass: for each case, which target holds the best claim on each card.
    best_card_score: dict[tuple[str, str], tuple[float, str]] = {}
    offset = 0
    for value, shortlist in zip(searchable, shortlists):
        window = scores[offset : offset + len(shortlist)]
        offset += len(shortlist)
        owner = f"{value['instance_ref']}|{value['predicate_ref']}"
        for index, score in sorted(
            zip(shortlist, window), key=lambda pair: (-pair[1], cards[pair[0]].id)
        )[: args.top_k_cards]:
            key = (value["case_id"], cards[index].id)
            if score > best_card_score.get(key, (-1e9, ""))[0]:
                best_card_score[key] = (score, owner)

    offset = 0
    by_case: dict[str, list[dict[str, Any]]] = {case_id: [] for case_id in e2e}
    selected_counts: Counter[str] = Counter()
    for value, shortlist in zip(searchable, shortlists):
        window = scores[offset : offset + len(shortlist)]
        offset += len(shortlist)
        ranked = sorted(zip(shortlist, window), key=lambda pair: (-pair[1], cards[pair[0]].id))
        chosen = [
            (index, score)
            for index, score in ranked
            # One card speaks once per case.  The same proposition repeated under three
            # elements of the same offence is noise the writer has to re-read, not grounds.
            if best_card_score.get((value["case_id"], cards[index].id), (-1e9, ""))
            == (score, f"{value['instance_ref']}|{value['predicate_ref']}")
        ][: args.top_k_cards]
        if not chosen:
            selected_counts[TIER_NONE] += 1
            continue
        selected_counts[str(value["tier"])] += 1
        by_case[value["case_id"]].append(
            {
                "instance_ref": value["instance_ref"],
                "predicate_ref": value["predicate_ref"],
                "truth": value["truth"],
                "tier": value["tier"],
                "statements": [
                    {
                        # Verbatim: SPEC 4-6 forbids summarising or synthesising a card.
                        "statement": cards[index].proposition,
                        "origin": "reviewed_card",
                        "source_id": cards[index].id,
                        "rerank_score": score,
                    }
                    for index, score in chosen
                ],
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for case_id, entries in by_case.items():
            handle.write(
                json.dumps({"sub_question_id": case_id, "rule_statements": entries}, ensure_ascii=False)
                + "\n"
            )

    summary["targets_with_cards"] = sum(selected_counts[tier] for tier in (TIER_BRIDGE, TIER_ARTICLE))
    summary["selected_by_tier"] = dict(selected_counts)
    summary["cards_per_target"] = args.top_k_cards
    args.out.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
