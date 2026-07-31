"""The L0 gate: issue recall over all 61 questions, decomposed by path.

Reports three numbers, never one. Retrieval alone is what the retrieval stack earns; call
1's proposals alone is roughly what a model already knows and is the baseline to beat; the
union is what the pipeline actually runs on. A union number by itself cannot answer whether
retrieval belongs in the system, and that is the question this run exists to answer.

Questions with no gold are bucketed, not zeroed. The card corpus covers 51 형법각칙
articles; a procedural question has none by construction, and scoring it 0.0 would report
a scope decision as a retrieval failure.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.eval.issue_recall import (
    INVENTORY_PATH,
    PROJECT_ROOT,
    SCORABLE,
    bucket_counts,
    load_issue_gold,
    missed_articles,
    summarise_paths,
)
from idpr.neural.fact_graph import proposed_articles, retrieval_queries
from idpr.retrieval import DEFAULT_TOP_K_ARTICLES, LexicalIndex, retrieve_candidate_articles
from idpr.rulebase.cards import card_corpus

DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "retrieval_l0_recall_report.json"

#: The plan's verification #5 checklist. An asset, not a literal: a verification list that
#: names articles does not belong in the code that reports against it.
SMOKE_CHECKS_PATH = PROJECT_ROOT / "data" / "eval" / "smoke_checks.json"


def load_fact_graphs(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    graphs: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if "fact_graph" in row:
            graphs[row["sub_question_id"]] = row["fact_graph"]
    return graphs


def load_inventory(path: Path) -> dict[str, dict]:
    return {
        json.loads(line)["sub_question_id"]: json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--top-k", type=int, nargs="+", default=[12, DEFAULT_TOP_K_ARTICLES, 24])
    parser.add_argument("--no-dense", action="store_true")
    parser.add_argument("--no-rerank", action="store_true")
    args = parser.parse_args()

    corpus = card_corpus()
    gold = load_issue_gold()
    # The same gold minus the attempt articles (제254·300·342조). Those are in the gold by
    # the reviewer's decision and are structurally unreachable by similarity -- the statute
    # text shares no vocabulary with any fact pattern -- so reporting both isolates how much
    # of the miss is that known limit rather than ranking quality.
    gold_without_attempt = load_issue_gold(with_attempt=False)
    inventory = load_inventory(args.inventory)
    graphs = load_fact_graphs(args.fact_graphs)

    encoder = reranker = None
    if not args.no_dense or not args.no_rerank:
        from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

        if not args.no_dense:
            encoder = SentenceTransformerEncoder()
        if not args.no_rerank:
            reranker = CrossEncoderReranker()

    propositions = [card.proposition for card in corpus.by_id.values()]
    lexical = LexicalIndex.build(propositions)

    report: dict = {
        "questions": len(inventory),
        "fact_graphs_available": len(graphs),
        "buckets": bucket_counts(gold),
        "dense_model": encoder.name if encoder else None,
        "reranker_model": reranker.name if reranker else None,
        "by_top_k": {},
    }

    per_question_articles: dict[int, dict[str, list[str]]] = {}
    for top_k in args.top_k:
        retrieval_only: dict[str, list[str]] = {}
        proposals_only: dict[str, list[str]] = {}
        union: dict[str, list[str]] = {}

        for case_id, record in inventory.items():
            graph = graphs.get(case_id)
            if graph is not None:
                queries = retrieval_queries(graph)
                proposals = proposed_articles(graph, corpus=corpus)
            else:
                # No call-1 output for this question: retrieval still runs, on the raw
                # question. Reported as such rather than skipped.
                queries = [record.get("question_prompt", ""), record["question_text"]]
                queries = [query for query in queries if query]
                proposals = []

            result = retrieve_candidate_articles(
                queries,
                corpus=corpus,
                proposed=proposals,
                top_k_articles=top_k,
                encoder=encoder,
                reranker=reranker,
                lexical=lexical,
            )
            retrieval_only[case_id] = list(result.retrieved)
            proposals_only[case_id] = list(result.proposed)
            union[case_id] = list(result.articles)

        per_question_articles[top_k] = union
        paths = {
            "retrieval": retrieval_only,
            "proposals": proposals_only,
            "union": union,
        }
        report["by_top_k"][str(top_k)] = {
            "paths": summarise_paths(gold, paths),
            "paths_without_attempt_articles": summarise_paths(gold_without_attempt, paths),
            "missed_articles": missed_articles(gold, union),
            # Per question, so a miss can be read back without re-running the GPU job.
            "candidates": {
                case_id: {
                    "retrieval": retrieval_only[case_id],
                    "proposals": proposals_only[case_id],
                    "gold": list(gold[case_id].articles),
                }
                for case_id in sorted(union)
                if gold[case_id].bucket == SCORABLE
            },
        }

    # Smoke case: the items the plan names, plus the compound offence.
    smoke = json.loads(SMOKE_CHECKS_PATH.read_text(encoding="utf-8"))
    smoke_case = smoke["sub_question_id"]
    smoke_checks = smoke["checks"]
    smoke_articles = per_question_articles.get(
        DEFAULT_TOP_K_ARTICLES, per_question_articles[args.top_k[0]]
    ).get(smoke_case, [])
    covered = set(corpus.by_article())
    report["smoke_case"] = {
        "sub_question_id": smoke_case,
        "candidate_articles": smoke_articles,
        "checks": {
            name: {
                "articles": wanted,
                "recovered": sorted(set(wanted) & set(smoke_articles)),
                "missing_from_corpus": sorted(set(wanted) - covered),
                "missed_by_retrieval": sorted(
                    (set(wanted) & covered) - set(smoke_articles)
                ),
            }
            for name, wanted in smoke_checks.items()
        },
    }

    scorable = [item for item in gold.values() if item.bucket == SCORABLE]
    report["scorable_question_ids"] = sorted(item.sub_question_id for item in scorable)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"buckets={report['buckets']}")
    for top_k, block in report["by_top_k"].items():
        paths = block["paths"]
        bare = block["paths_without_attempt_articles"]
        print(
            f"top_k={top_k:>3} "
            f"retrieval={paths['retrieval']['macro_recall']:.3f} "
            f"proposals={paths['proposals']['macro_recall']:.3f} "
            f"union={paths['union']['macro_recall']:.3f} "
            f"(n={paths['union']['questions']}) "
            f"| 준용조문 제외 union={bare['union']['macro_recall']:.3f}"
        )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
