"""L0 output: the candidate articles and assessable cards call 2 consumes, for all 61.

This is the artifact Phase 3 reads. It exists as a file rather than an in-memory step for
the reason every other stage boundary here does: the two sources need different models and
one GPU cannot hold both, so the union has to be assembled from artifacts.

Retrieval runs over every question, not only the scorable ones. The recall report cannot be
computed for a question with no gold, but the pipeline still has to produce candidates for
it, and a report that quietly covered 31 of 61 would leave the other 30 with no input.
"""

from __future__ import annotations

import argparse
import json
import statistics as st
from pathlib import Path

from idpr.candidates import assessable_card_ids, candidate_articles
from idpr.eval.issue_recall import (
    INVENTORY_PATH,
    PROJECT_ROOT,
    SCORABLE,
    bucket_counts,
    load_issue_gold,
    missed_articles,
    recall,
)
from idpr.neural.article_select import attempt_article_map
from idpr.neural.fact_graph import retrieval_queries
from idpr.retrieval import DEFAULT_TOP_K_ARTICLES, LexicalIndex, retrieve_candidate_articles
from idpr.rulebase.cards import card_corpus

DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
DEFAULT_SELECTION = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "l0_candidates.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "data" / "eval" / "l0_union_report.json"
SMOKE_CHECKS_PATH = PROJECT_ROOT / "data" / "eval" / "smoke_checks.json"


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K_ARTICLES)
    parser.add_argument("--no-retrieval", action="store_true",
                        help="model selection only -- the fallback if the union is too slow")
    args = parser.parse_args()

    corpus = card_corpus()
    assessable = assessable_card_ids(corpus)
    attempt_map = attempt_article_map()
    gold = load_issue_gold()
    inventory = {row["sub_question_id"]: row for row in _rows(args.inventory)}
    graphs = {row["sub_question_id"]: row["fact_graph"] for row in _rows(args.fact_graphs)
              if "fact_graph" in row}
    selection = {row["sub_question_id"]: row["selected"] for row in _rows(args.selection)
                 if "error" not in row}

    encoder = reranker = lexical = None
    if not args.no_retrieval:
        from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

        encoder = SentenceTransformerEncoder()
        reranker = CrossEncoderReranker()
        lexical = LexicalIndex.build([card.proposition for card in corpus.by_id.values()])

    per_question: dict[str, list[str]] = {}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for index, (case_id, record) in enumerate(sorted(inventory.items()), start=1):
            retrieved: list[str] = []
            if not args.no_retrieval:
                graph = graphs.get(case_id)
                queries = (
                    retrieval_queries(graph)
                    if graph is not None
                    else [q for q in (record.get("question_prompt", ""), record["question_text"]) if q]
                )
                retrieved = list(
                    retrieve_candidate_articles(
                        queries,
                        corpus=corpus,
                        top_k_articles=args.top_k,
                        encoder=encoder,
                        reranker=reranker,
                        lexical=lexical,
                    ).retrieved
                )

            candidates = candidate_articles(
                selected=selection.get(case_id, ()),
                retrieved=retrieved,
                corpus=corpus,
                assessable=assessable,
                attempt_map=attempt_map,
            )
            per_question[case_id] = list(candidates.articles)
            handle.write(
                json.dumps(
                    {"sub_question_id": case_id, **candidates.as_dict(),
                     "card_ids": list(candidates.card_ids)},
                    ensure_ascii=False,
                )
                + "\n"
            )
            handle.flush()
            print(f"[{index}/{len(inventory)}] {case_id} "
                  f"{len(candidates.articles)} articles / {len(candidates.cards)} cards")

    scores = [recall(gold[q].articles, a) for q, a in per_question.items()
              if gold[q].bucket == SCORABLE]
    scores = [s for s in scores if s is not None]
    sizes = [len(a) for a in per_question.values()]
    cards = [len(candidate_articles(selected=(), retrieved=a, corpus=corpus,
                                    assessable=assessable, attempt_map=attempt_map).cards)
             for a in per_question.values()]

    smoke = json.loads(SMOKE_CHECKS_PATH.read_text(encoding="utf-8"))
    covered = set(corpus.by_article())
    smoke_articles = per_question.get(smoke["sub_question_id"], [])
    report = {
        "mode": "model_selection_only" if args.no_retrieval else "union",
        "top_k_articles": None if args.no_retrieval else args.top_k,
        "questions": len(per_question),
        "buckets": bucket_counts(gold),
        "macro_recall": round(st.mean(scores), 4) if scores else None,
        "fully_recovered": sum(1 for s in scores if s == 1.0),
        "scorable": len(scores),
        "articles_per_question": {"median": int(st.median(sizes)), "max": max(sizes)},
        "cards_per_question": {"median": int(st.median(cards)), "max": max(cards)},
        "missed_articles": missed_articles(gold, per_question),
        "smoke_case": {
            "sub_question_id": smoke["sub_question_id"],
            "candidate_articles": smoke_articles,
            "checks": {
                name: {
                    "articles": wanted,
                    "recovered": sorted(set(wanted) & set(smoke_articles)),
                    "missing_from_corpus": sorted(set(wanted) - covered),
                    "missed": sorted((set(wanted) & covered) - set(smoke_articles)),
                }
                for name, wanted in smoke["checks"].items()
            },
        },
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nmode={report['mode']} recall={report['macro_recall']} "
          f"({report['fully_recovered']}/{report['scorable']} fully recovered) "
          f"articles={report['articles_per_question']} cards={report['cards_per_question']}")
    for name, block in report["smoke_case"]["checks"].items():
        print(f"  smoke {name}: recovered={block['recovered']} missed={block['missed']} "
              f"out_of_corpus={block['missing_from_corpus']}")
    print(f"wrote {args.out} / {args.report}")


if __name__ == "__main__":
    main()
