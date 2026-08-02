"""L0 output: candidate articles and normalized issues consumed downstream.

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

from idpr.candidates import candidate_issues
from idpr.eval.input_formatter import scoped_question_text
from idpr.eval.issue_recall import (
    INVENTORY_PATH,
    PROJECT_ROOT,
    SCORABLE,
    bucket_counts,
    load_issue_gold,
    missed_articles,
    recall,
)
from idpr.issue_pipeline import issue_candidate_row
from idpr.neural.article_select import attempt_article_map
from idpr.neural.fact_graph import retrieval_queries
from idpr.retrieval import (
    DEFAULT_TOP_K_ARTICLES,
    DenseIndex,
    LexicalIndex,
    retrieve_candidate_articles_via_issues,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import ELEMENT_ISSUE, compile_issue_catalog_v2

DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
DEFAULT_SELECTION = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "l0_candidates.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "data" / "eval" / "l0_union_report.json"


def retrieval_admission_issues(issues: tuple, *, mode: str) -> tuple:
    """Choose which issue functions may admit an article; downstream scope stays complete."""
    if mode == "all":
        return issues
    if mode == "elements":
        return tuple(issue for issue in issues if issue.function == ELEMENT_ISSUE)
    raise ValueError(f"unknown retrieval admission mode: {mode}")


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def gold_for_inventory(gold: dict, inventory: dict) -> dict:
    """Limit evaluation metadata to cases actually present in this invocation."""
    return {case_id: gold[case_id] for case_id in inventory if case_id in gold}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-k-articles", type=int, default=DEFAULT_TOP_K_ARTICLES)
    parser.add_argument(
        "--retrieval-admission",
        choices=("all", "elements"),
        default="all",
        help="experimental article ranking scope; selected articles still load all issue functions",
    )
    parser.add_argument(
        "--checks",
        type=Path,
        help="optional case-specific coverage checklist for diagnostic reporting",
    )
    parser.add_argument("--no-retrieval", action="store_true",
                        help="model selection only -- the fallback if the union is too slow")
    args = parser.parse_args()

    corpus = card_corpus()
    issues, placements = compile_issue_catalog_v2(corpus)
    retrieval_issues = retrieval_admission_issues(issues, mode=args.retrieval_admission)
    attempt_map = attempt_article_map()
    gold = load_issue_gold()
    inventory = {row["sub_question_id"]: row for row in _rows(args.inventory)}
    run_gold = gold_for_inventory(gold, inventory)
    graphs = {row["sub_question_id"]: row["fact_graph"] for row in _rows(args.fact_graphs)
              if "fact_graph" in row}
    selection = {row["sub_question_id"]: row["selected"] for row in _rows(args.selection)
                 if "error" not in row}

    encoder = reranker = lexical = None
    if not args.no_retrieval:
        from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

        encoder = SentenceTransformerEncoder()
        reranker = CrossEncoderReranker()
        retrieval_issue_ids = {issue.issue_id for issue in retrieval_issues}
        retrieval_card_ids = {
            placement.card_id
            for placement in placements
            if placement.issue_id in retrieval_issue_ids
        }
        search_documents = tuple(
            card.proposition for card in corpus.cards if card.id in retrieval_card_ids
        )
        lexical = LexicalIndex.build(search_documents)
        dense = DenseIndex.build(search_documents, encoder)
    else:
        dense = None

    per_question: dict[str, list[str]] = {}
    scopes = {}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for index, (case_id, record) in enumerate(sorted(inventory.items()), start=1):
            retrieved: list[str] = []
            retrieved_issue_ids: list[str] = []
            if not args.no_retrieval:
                graph = graphs.get(case_id)
                queries = (
                    retrieval_queries(graph)
                    if graph is not None
                    else [
                        query
                        for query in (
                            record.get("question_prompt", ""),
                            scoped_question_text(
                                record["question_text"],
                                record.get("question_prompt", ""),
                            ),
                        )
                        if query
                    ]
                )
                retrieval = retrieve_candidate_articles_via_issues(
                    queries,
                    corpus=corpus,
                    issues=retrieval_issues,
                    top_k_articles=args.top_k_articles,
                    encoder=encoder,
                    reranker=reranker,
                    lexical=lexical,
                    dense=dense,
                )
                retrieved = list(retrieval.retrieved_articles)
                retrieved_issue_ids = list(retrieval.retrieved_issue_ids)

            candidates = candidate_issues(
                selected=selection.get(case_id, ()),
                retrieved=retrieved,
                corpus=corpus,
                attempt_map=attempt_map,
            )
            scopes[case_id] = candidates
            per_question[case_id] = list(candidates.articles)
            handle.write(
                json.dumps(
                    issue_candidate_row(
                        case_id,
                        candidates,
                        retrieved_issue_ids=retrieved_issue_ids,
                    ),
                    ensure_ascii=False,
                )
                + "\n"
            )
            handle.flush()
            print(f"[{index}/{len(inventory)}] {case_id} "
                  f"{len(candidates.articles)} articles / "
                  f"{len(candidates.initial_issues)} initial issues")

    scores = [
        recall(run_gold[q].articles, articles)
        for q, articles in per_question.items()
        if q in run_gold and run_gold[q].bucket == SCORABLE
    ]
    scores = [s for s in scores if s is not None]
    sizes = [len(a) for a in per_question.values()]
    initial_issues = [len(scope.initial_issues) for scope in scopes.values()]
    anchors = [
        sum(len(issue.anchor_card_ids) for issue in scope.initial_issues)
        for scope in scopes.values()
    ]

    report = {
        "mode": "model_selection_only" if args.no_retrieval else "union",
        "top_k_articles": None if args.no_retrieval else args.top_k_articles,
        "retrieval_admission": args.retrieval_admission,
        "questions": len(per_question),
        "buckets": bucket_counts(run_gold),
        "macro_recall": round(st.mean(scores), 4) if scores else None,
        "fully_recovered": sum(1 for s in scores if s == 1.0),
        "scorable": len(scores),
        "articles_per_question": {"median": int(st.median(sizes)), "max": max(sizes)},
        "initial_issues_per_question": {
            "median": int(st.median(initial_issues)),
            "max": max(initial_issues),
        },
        "anchor_rules_per_question": {
            "median": int(st.median(anchors)),
            "max": max(anchors),
        },
        "missed_articles": missed_articles(run_gold, per_question),
    }
    if args.checks:
        checks = json.loads(args.checks.read_text(encoding="utf-8"))
        check_case = checks["sub_question_id"]
        check_articles = per_question.get(check_case, [])
        covered = set(corpus.by_article())
        report["diagnostic_checks"] = {
            "sub_question_id": check_case,
            "candidate_articles": check_articles,
            "checks": {
                name: {
                    "articles": wanted,
                    "recovered": sorted(set(wanted) & set(check_articles)),
                    "missing_from_corpus": sorted(set(wanted) - covered),
                    "missed": sorted((set(wanted) & covered) - set(check_articles)),
                }
                for name, wanted in checks["checks"].items()
            },
        }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nmode={report['mode']} recall={report['macro_recall']} "
          f"({report['fully_recovered']}/{report['scorable']} fully recovered) "
          f"articles={report['articles_per_question']} "
          f"issues={report['initial_issues_per_question']} "
          f"anchors={report['anchor_rules_per_question']}")
    for name, block in report.get("diagnostic_checks", {}).get("checks", {}).items():
        print(f"  check {name}: recovered={block['recovered']} missed={block['missed']} "
              f"out_of_corpus={block['missing_from_corpus']}")
    print(f"wrote {args.out} / {args.report}")


if __name__ == "__main__":
    main()
