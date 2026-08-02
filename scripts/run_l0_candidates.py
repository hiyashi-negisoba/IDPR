"""L0 output: reviewed article scope and normalized issues consumed downstream, for all 61.

This is the artifact Phase 3 reads. It exists as a file rather than an in-memory step for
the reason every other stage boundary here does: the two sources need different models and
one GPU cannot hold both, so the union has to be assembled from artifacts.

Retrieval runs over every question, not only the scorable ones. Its ranked candidates are
persisted independently from the active scope: in the default reviewed policy, only Call
1.5-approved articles open an issue hierarchy. The recall report cannot be
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
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2

DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
DEFAULT_SELECTION = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "l0_candidates.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "data" / "eval" / "l0_union_report.json"
REVIEWED_SELECTION = "reviewed_selection"
LEGACY_UNION = "legacy_union"
RETRIEVAL_ONLY = "retrieval_only"


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _retrieval_lane(row: dict) -> tuple[list[str], list[str]]:
    """Return raw ranked articles and issue ids from current or legacy L0 artifacts."""
    issue_ids = list(dict.fromkeys(row.get("retrieved_issue_ids", ())))
    if "retrieved_articles" in row:
        articles = list(dict.fromkeys(row["retrieved_articles"]))
    elif issue_ids:
        articles = list(dict.fromkeys(issue_id.split(".", 1)[0] for issue_id in issue_ids))
    else:
        articles = list(dict.fromkeys(row.get("from_retrieval", ())))
    return articles, issue_ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument(
        "--retrieval-candidates",
        type=Path,
        help="reuse a persisted retrieval lane instead of loading retrieval models",
    )
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-k-articles", type=int, default=DEFAULT_TOP_K_ARTICLES)
    parser.add_argument(
        "--routing-policy",
        choices=[REVIEWED_SELECTION, LEGACY_UNION, RETRIEVAL_ONLY],
        default=REVIEWED_SELECTION,
        help=(
            "reviewed_selection activates only Call 1.5 output; legacy_union also "
            "activates every retrieved article; retrieval_only creates a shortlist artifact"
        ),
    )
    parser.add_argument(
        "--checks",
        type=Path,
        help="optional case-specific coverage checklist for diagnostic reporting",
    )
    parser.add_argument("--no-retrieval", action="store_true",
                        help="model selection only -- the fallback if the union is too slow")
    args = parser.parse_args()
    if args.no_retrieval and args.retrieval_candidates:
        parser.error("--no-retrieval and --retrieval-candidates are mutually exclusive")
    if args.no_retrieval and args.routing_policy == RETRIEVAL_ONLY:
        parser.error("retrieval_only requires a retrieval source")

    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    attempt_map = attempt_article_map()
    gold = load_issue_gold()
    inventory = {row["sub_question_id"]: row for row in _rows(args.inventory)}
    graphs = {row["sub_question_id"]: row["fact_graph"] for row in _rows(args.fact_graphs)
              if "fact_graph" in row}
    selection = {row["sub_question_id"]: row["selected"] for row in _rows(args.selection)
                 if "error" not in row}
    persisted_retrieval = {
        row["sub_question_id"]: _retrieval_lane(row)
        for row in (
            _rows(args.retrieval_candidates) if args.retrieval_candidates else []
        )
    }

    encoder = reranker = lexical = None
    live_retrieval = not args.no_retrieval and not args.retrieval_candidates
    if live_retrieval:
        from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder

        encoder = SentenceTransformerEncoder()
        reranker = CrossEncoderReranker()
        search_documents = tuple(card.proposition for card in corpus.cards)
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
            if case_id in persisted_retrieval:
                retrieved, retrieved_issue_ids = persisted_retrieval[case_id]
            elif args.retrieval_candidates:
                raise ValueError(f"retrieval artifact is missing {case_id}")
            elif live_retrieval:
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
                    issues=issues,
                    top_k_articles=args.top_k_articles,
                    encoder=encoder,
                    reranker=reranker,
                    lexical=lexical,
                    dense=dense,
                )
                retrieved = list(retrieval.retrieved_articles)
                retrieved_issue_ids = list(retrieval.retrieved_issue_ids)

            active_selected = (
                () if args.routing_policy == RETRIEVAL_ONLY else selection.get(case_id, ())
            )
            active_retrieved = (
                retrieved
                if args.routing_policy in {LEGACY_UNION, RETRIEVAL_ONLY}
                else ()
            )
            candidates = candidate_issues(
                selected=active_selected,
                retrieved=active_retrieved,
                corpus=corpus,
                attempt_map=attempt_map,
            )
            active_articles = set(candidates.articles)
            active_retrieved_issue_ids = [
                issue_id
                for issue_id in retrieved_issue_ids
                if issue_id.split(".", 1)[0] in active_articles
            ]
            scopes[case_id] = candidates
            per_question[case_id] = list(candidates.articles)
            handle.write(
                json.dumps(
                    issue_candidate_row(
                        case_id,
                        candidates,
                        retrieved_articles=retrieved,
                        retrieved_issue_ids=active_retrieved_issue_ids,
                    ),
                    ensure_ascii=False,
                )
                + "\n"
            )
            handle.flush()
            print(f"[{index}/{len(inventory)}] {case_id} "
                  f"{len(candidates.articles)} articles / "
                  f"{len(candidates.initial_issues)} initial issues")

    scores = [recall(gold[q].articles, a) for q, a in per_question.items()
              if gold[q].bucket == SCORABLE]
    scores = [s for s in scores if s is not None]
    sizes = [len(a) for a in per_question.values()]
    initial_issues = [len(scope.initial_issues) for scope in scopes.values()]
    anchors = [
        sum(len(issue.anchor_card_ids) for issue in scope.initial_issues)
        for scope in scopes.values()
    ]

    report = {
        "mode": args.routing_policy,
        "retrieval_source": (
            "none"
            if args.no_retrieval
            else "artifact" if args.retrieval_candidates else "live"
        ),
        "top_k_articles": None if args.no_retrieval else args.top_k_articles,
        "questions": len(per_question),
        "buckets": bucket_counts(gold),
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
        "missed_articles": missed_articles(gold, per_question),
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
