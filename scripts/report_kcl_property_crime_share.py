"""Report how much of a KCL question set is reachable with property-crime rules alone.

The split is read off the rubric gold, not off this repository's own tags or retrieval, so
it answers "what does the benchmark ask" rather than "what did we happen to find".  A
question counts as property-only when every gold article it carries falls inside a
property-crime chapter; mixed questions are reported separately because a property-only
rule base answers part of them and silently misses the rest.

Questions whose rubric names no offence at all are not failures and are not scored here;
they are reported as their own bucket.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from idpr.eval.issue_recall import load_issue_gold


ARTICLE_RE = re.compile(r"^art(?P<number>\d+)")


def load_chapters(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload["property_chapters"])


def article_number(article: str) -> int:
    match = ARTICLE_RE.match(article)
    if match is None:
        raise ValueError(f"unrecognised article id: {article}")
    return int(match["number"])


def chapter_of(article: str, chapters: list[dict[str, Any]]) -> dict[str, Any] | None:
    number = article_number(article)
    for chapter in chapters:
        if chapter["first_article"] <= number <= chapter["last_article"]:
            return chapter
    return None


def classify(articles: tuple[str, ...], chapters: list[dict[str, Any]]) -> str:
    if not articles:
        return "no_gold_offence"
    hits = [chapter_of(article, chapters) is not None for article in articles]
    if all(hits):
        return "property_only"
    if any(hits):
        return "mixed"
    return "non_property_only"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument(
        "--chapters",
        type=Path,
        default=Path("data/eval/criminal_code_property_chapters.json"),
    )
    parser.add_argument(
        "--case-ids-from",
        type=Path,
        default=None,
        help="restrict the report to the questions listed in this inventory; gold still "
             "comes from --inventory, which is the one that back-references the rubric",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    chapters = load_chapters(args.chapters)
    gold = load_issue_gold(inventory_path=args.inventory)
    if args.case_ids_from is not None:
        wanted = [
            str(json.loads(line)["sub_question_id"])
            for line in args.case_ids_from.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        missing = sorted(set(wanted) - set(gold))
        if missing:
            raise ValueError(f"requested questions absent from the gold inventory: {missing}")
        gold = {case_id: gold[case_id] for case_id in wanted}

    buckets: dict[str, list[str]] = {
        "property_only": [],
        "mixed": [],
        "non_property_only": [],
        "no_gold_offence": [],
    }
    per_question: list[dict[str, Any]] = []
    for case_id, item in gold.items():
        bucket = classify(item.articles, chapters)
        buckets[bucket].append(case_id)
        per_question.append({
            "sub_question_id": case_id,
            "bucket": bucket,
            "gold_articles": list(item.articles),
            "property_articles": [
                article for article in item.articles
                if chapter_of(article, chapters) is not None
            ],
            "crimes": list(item.crimes),
            "out_of_corpus_crimes": list(item.out_of_corpus_crimes),
            "rubric_items": item.rubric_items,
        })

    scorable = [row for row in per_question if row["bucket"] != "no_gold_offence"]
    report = {
        "version": "1.0.0",
        "inventory": str(args.inventory),
        "chapters": str(args.chapters),
        "questions": len(per_question),
        "counts": {name: len(ids) for name, ids in buckets.items()},
        "share_of_scorable": (
            {
                name: round(len(buckets[name]) / len(scorable), 4)
                for name in ("property_only", "mixed", "non_property_only")
            }
            if scorable
            else {}
        ),
        "case_ids": buckets,
        "questions_detail": sorted(per_question, key=lambda row: row["sub_question_id"]),
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    print(json.dumps({
        "questions": report["questions"],
        "counts": report["counts"],
        "share_of_scorable": report["share_of_scorable"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
