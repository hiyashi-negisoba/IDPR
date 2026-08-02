#!/usr/bin/env python3
"""Measure whether cross-query support can replace max-over-queries retrieval fusion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from idpr.neural.fact_graph import retrieval_queries
from idpr.retrieval import DenseIndex, LexicalIndex, retrieve_candidate_articles_via_issues
from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2


def aggregate_rankings(
    rankings: Sequence[Sequence[str]], *, mode: str, cutoff: int | None = None, k: int = 60
) -> list[str]:
    """Aggregate article ranks without comparing cross-encoder scores across queries."""
    articles = tuple(dict.fromkeys(article for ranking in rankings for article in ranking))
    positions = {
        article: [
            rank
            for ranking in rankings
            for rank, candidate in enumerate(ranking, start=1)
            if candidate == article and (cutoff is None or rank <= cutoff)
        ]
        for article in articles
    }
    if mode == "rrf":
        scores = {
            article: sum(1.0 / (k + rank) for rank in ranks)
            for article, ranks in positions.items()
        }
        return sorted(articles, key=lambda article: (-scores[article], article))
    if mode == "support_then_best":
        return sorted(
            articles,
            key=lambda article: (
                -len(positions[article]),
                min(positions[article], default=10**9),
                article,
            ),
        )
    raise ValueError(f"unknown aggregation mode: {mode}")


def _rows(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--articles-per-query", type=int, default=51)
    args = parser.parse_args()

    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    encoder = SentenceTransformerEncoder()
    reranker = CrossEncoderReranker()
    documents = tuple(card.proposition for card in corpus.cards)
    lexical = LexicalIndex.build(documents)
    dense = DenseIndex.build(documents, encoder)

    output_rows: list[dict] = []
    for row in _rows(args.fact_graphs):
        case_id = row["sub_question_id"]
        queries = retrieval_queries(row["fact_graph"])
        query_rows: list[dict] = []
        rankings: list[list[str]] = []
        for index, query in enumerate(queries, start=1):
            result = retrieve_candidate_articles_via_issues(
                [query],
                corpus=corpus,
                issues=issues,
                top_k_articles=args.articles_per_query,
                encoder=encoder,
                reranker=reranker,
                lexical=lexical,
                dense=dense,
            )
            articles = list(result.retrieved_articles)
            rankings.append(articles)
            query_rows.append(
                {
                    "query": query,
                    "articles": articles,
                    "top_issues": [
                        {
                            "article": issue_by_id[issue_id].article,
                            "issue_id": issue_id,
                            "score": result.issue_scores[issue_id],
                        }
                        for issue_id in result.retrieved_issue_ids
                    ],
                }
            )
            print(f"{case_id} [{index}/{len(queries)}] {query[:70]}")
        output_rows.append(
            {
                "sub_question_id": case_id,
                "queries": query_rows,
                "aggregates": {
                    "rrf_all": aggregate_rankings(rankings, mode="rrf"),
                    "rrf_top10": aggregate_rankings(rankings, mode="rrf", cutoff=10),
                    "support_top10_then_best": aggregate_rankings(
                        rankings, mode="support_then_best", cutoff=10
                    ),
                },
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output_rows),
        encoding="utf-8",
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
