"""Rewrite a validated flat L0 artifact as lossless issue-first rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.candidates import candidate_issues
from idpr.eval.issue_recall import PROJECT_ROOT
from idpr.issue_pipeline import issue_candidate_row
from idpr.rulebase.cards import card_corpus

DEFAULT_PATH = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in args.input.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    corpus = card_corpus()
    migrated: list[dict] = []
    for row in rows:
        scope = candidate_issues(
            selected=row.get("from_model", ()),
            retrieved=row.get("from_retrieval", ()),
            corpus=corpus,
        )
        if tuple(row.get("articles", ())) != scope.articles:
            raise ValueError(
                f"{row.get('sub_question_id')}: article scope changed during migration"
            )
        migrated.append(
            issue_candidate_row(
                row["sub_question_id"],
                scope,
                retrieved_issue_ids=(),
            )
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False) + "\n" for row in migrated
        ),
        encoding="utf-8",
    )
    print(
        f"wrote {len(migrated)} issue-first rows to {args.out}; "
        "retrieved_issue_ids remain empty because the source predates issue projection"
    )


if __name__ == "__main__":
    main()
