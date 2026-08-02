"""Evaluate L0 retrieval over normalized issue documents instead of flat cards."""

from __future__ import annotations

import argparse
import json
import statistics as st
from pathlib import Path
from typing import Sequence

from idpr.candidates import candidate_issues
from idpr.eval.issue_recall import (
    INVENTORY_PATH,
    PROJECT_ROOT,
    SCORABLE,
    load_issue_gold,
    missed_articles,
    summarise_paths,
)
from idpr.eval.input_formatter import scoped_question_text
from idpr.neural.fact_graph import proposed_articles, retrieval_queries
from idpr.retrieval import (
    DEFAULT_TOP_K_ISSUES,
    DenseIndex,
    LexicalIndex,
    issue_index_documents,
    retrieve_candidate_issues,
    retrieve_candidate_issues_from_cards,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2

DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data/eval/fact_graphs.jsonl"
DEFAULT_SELECTION = PROJECT_ROOT / "data/eval/article_selection.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data/eval/issue_retrieval_l0_report.json"


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _stats(values: Sequence[int]) -> dict[str, int | float]:
    return {
        "median": st.median(values) if values else 0,
        "max": max(values, default=0),
        "mean": round(st.mean(values), 2) if values else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--top-k",
        type=int,
        nargs="+",
        default=[6, 8, 12, DEFAULT_TOP_K_ISSUES, 24, 36, 48, 60, 72],
    )
    parser.add_argument("--no-dense", action="store_true")
    parser.add_argument("--no-rerank", action="store_true")
    parser.add_argument(
        "--index-mode",
        choices=("member_cards", "anchor_rules"),
        default="member_cards",
    )
    args = parser.parse_args()
    if any(value < 1 for value in args.top_k):
        parser.error("--top-k values must be positive")

    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    indexed, anchor_documents = issue_index_documents(issues, corpus=corpus)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    documents = (
        tuple(card.proposition for card in corpus.cards)
        if args.index_mode == "member_cards"
        else anchor_documents
    )
    inventory = {row["sub_question_id"]: row for row in _rows(args.inventory)}
    graphs = {
        row["sub_question_id"]: row["fact_graph"]
        for row in _rows(args.fact_graphs)
        if "fact_graph" in row
    }
    selections = {
        row["sub_question_id"]: tuple(row["selected"])
        for row in _rows(args.selection)
        if "error" not in row
    }
    gold = load_issue_gold()
    gold_without_attempt = load_issue_gold(with_attempt=False)

    encoder = reranker = None
    if not args.no_dense or not args.no_rerank:
        from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

        if not args.no_dense:
            encoder = SentenceTransformerEncoder()
        if not args.no_rerank:
            reranker = CrossEncoderReranker()
    lexical = LexicalIndex.build(documents)
    dense = DenseIndex.build(documents, encoder) if encoder is not None else None
    max_k = max(args.top_k)

    ranked_by_case: dict[str, tuple[str, ...]] = {}
    proposals_by_case: dict[str, tuple[str, ...]] = {}
    for index, (case_id, record) in enumerate(sorted(inventory.items()), start=1):
        graph = graphs.get(case_id)
        queries = (
            retrieval_queries(graph)
            if graph is not None
            else tuple(
                text
                for text in (
                    record.get("question_prompt", ""),
                    scoped_question_text(
                        record.get("question_text", ""),
                        record.get("question_prompt", ""),
                    ),
                )
                if text
            )
        )
        proposals = selections.get(
            case_id,
            proposed_articles(graph, corpus=corpus) if graph is not None else (),
        )
        retrieve = (
            retrieve_candidate_issues_from_cards
            if args.index_mode == "member_cards"
            else retrieve_candidate_issues
        )
        result = retrieve(
            queries,
            corpus=corpus,
            issues=issues if args.index_mode == "member_cards" else indexed,
            proposed=proposals,
            top_k_issues=max_k,
            encoder=encoder,
            reranker=reranker,
            lexical=lexical,
            dense=dense,
        )
        ranked_by_case[case_id] = tuple(result.issue_scores)
        proposals_by_case[case_id] = tuple(proposals)
        print(f"[{index}/{len(inventory)}] {case_id}")

    report: dict = {
        "questions": len(inventory),
        "index_mode": args.index_mode,
        "indexed_issues": len(issues),
        "indexed_documents": (
            "all member card propositions projected to parent issue"
            if args.index_mode == "member_cards"
            else "article label + offense + issue title + anchor rules"
        ),
        "excluded_without_anchor": len(issues) - len(indexed),
        "dense_model": encoder.name if encoder else None,
        "reranker_model": reranker.name if reranker else None,
        "by_top_k_issues": {},
    }
    for top_k in args.top_k:
        retrieval_only: dict[str, list[str]] = {}
        proposals_only: dict[str, list[str]] = {}
        union: dict[str, list[str]] = {}
        issue_hits: dict[str, list[str]] = {}
        scopes = {}
        for case_id in inventory:
            selected_issue_ids = list(ranked_by_case[case_id][:top_k])
            issue_hits[case_id] = selected_issue_ids
            retrieved_articles = list(
                dict.fromkeys(issue_by_id[issue_id].article for issue_id in selected_issue_ids)
            )
            proposals = list(proposals_by_case[case_id])
            retrieval_only[case_id] = retrieved_articles
            proposals_only[case_id] = proposals
            union[case_id] = list(dict.fromkeys((*retrieved_articles, *proposals)))
            scopes[case_id] = candidate_issues(
                selected=proposals,
                retrieved=retrieved_articles,
                corpus=corpus,
            )

        paths = {
            "retrieval": retrieval_only,
            "proposals": proposals_only,
            "union": union,
        }
        actual_articles = [len(scope.articles) for scope in scopes.values()]
        initial_issues = [len(scope.initial_issues) for scope in scopes.values()]
        anchors = [
            sum(len(issue.anchor_card_ids) for issue in scope.initial_issues)
            for scope in scopes.values()
        ]
        block = {
            "paths": summarise_paths(gold, paths),
            "paths_without_attempt_articles": summarise_paths(
                gold_without_attempt, paths
            ),
            "missed_articles": missed_articles(gold, union),
            "retrieved_articles_per_question": _stats(
                [len(items) for items in retrieval_only.values()]
            ),
            "runtime_articles_per_question": _stats(actual_articles),
            "initial_issues_per_question": _stats(initial_issues),
            "anchor_rules_per_question": _stats(anchors),
            "candidates": {
                case_id: {
                    "retrieved_issue_ids": issue_hits[case_id],
                    "retrieved_articles": retrieval_only[case_id],
                    "proposed_articles": proposals_only[case_id],
                    "runtime_articles": list(scopes[case_id].articles),
                    "gold_articles": list(gold[case_id].articles),
                }
                for case_id in sorted(inventory)
                if gold[case_id].bucket == SCORABLE
            },
        }
        report["by_top_k_issues"][str(top_k)] = block

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for top_k, block in report["by_top_k_issues"].items():
        paths = block["paths"]
        print(
            f"top_k_issues={top_k:>2} "
            f"retrieval={paths['retrieval']['macro_recall']:.3f} "
            f"proposals={paths['proposals']['macro_recall']:.3f} "
            f"union={paths['union']['macro_recall']:.3f} "
            f"runtime_articles={block['runtime_articles_per_question']} "
            f"initial_issues={block['initial_issues_per_question']}"
        )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
