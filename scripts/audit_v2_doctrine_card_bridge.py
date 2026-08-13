#!/usr/bin/env python3
"""Audit the KCL issue-tag -> commentary -> card path without treating it as RuleIR.

This is an offline supervision audit.  KCL issue tags select commentary material for
coverage analysis; they are never emitted as runtime facts.  In particular, finding a
card for an article does not activate a doctrine: a DoctrineDef still needs an authored
condition, effect, and offense-instance binding.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _article_key(law_id: str, article_no: str) -> str | None:
    # card_catalog_v2 is the Criminal Act corpus.  An article number alone must
    # never join a special statute that happens to use the same number.
    if law_id != "001692":
        return None
    match = re.search(r"제0*(\d+)조(?:의0*(\d+))?", article_no)
    if match is None:
        return None
    base, sub = match.groups()
    return f"art{int(base)}" if sub is None else f"art{int(base)}{int(sub)}_{int(sub)}"


def build_audit(
    *,
    gold_path: Path,
    manifest_path: Path,
    cards_path: Path,
) -> dict[str, Any]:
    case_ids = {row["sub_question_id"] for row in _jsonl(gold_path)}
    manifest = _jsonl(manifest_path)
    cards = json.loads(cards_path.read_text())["cards"]
    cards_by_article: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        cards_by_article[card["article"]].append(card)

    rows: list[dict[str, Any]] = []
    selected_articles: set[str] = set()
    article_with_cards: set[str] = set()
    for item in manifest:
        selected_cases = sorted(case_ids.intersection(item["sub_question_ids"]))
        if not selected_cases:
            continue
        targets = []
        candidate_cards: list[dict[str, Any]] = []
        for target in item["targets"]:
            article_key = _article_key(target["law_id"], target["article_no"])
            matched = [] if article_key is None else cards_by_article.get(article_key, [])
            if article_key is not None:
                selected_articles.add(article_key)
                if matched:
                    article_with_cards.add(article_key)
            candidate_cards.extend(matched)
            targets.append(
                {
                    "target_id": target["target_id"],
                    "target_path": target["target_path"],
                    "article_key": article_key,
                    "card_count": len(matched),
                }
            )
        rows.append(
            {
                "issue_tag": item["tag"],
                "case_ids": selected_cases,
                "commentary_status": item["status"],
                "limitation": item.get("limitation", ""),
                "targets": targets,
                "candidate_card_count": len(candidate_cards),
                "reviewed_candidate_card_count": sum(
                    not card["review_required"] for card in candidate_cards
                ),
                "card_functions": dict(
                    sorted(Counter(card["function"] for card in candidate_cards).items())
                ),
                # There is deliberately no tag/card -> DoctrineDef mapping in the current
                # repository.  Keep this explicit so card availability cannot be mistaken
                # for a symbolic activation contract.
                "symbolic_bridge_status": "NOT_AUTHORED",
            }
        )

    status_counts = Counter(row["commentary_status"] for row in rows)
    return {
        "scope": {
            "case_count": len(case_ids),
            "issue_tag_count": len(rows),
            "runtime_use_of_kcl_issue_tags": False,
        },
        "summary": {
            "commentary_status_counts": dict(sorted(status_counts.items())),
            "tags_with_commentary_targets": sum(bool(row["targets"]) for row in rows),
            "tags_with_candidate_cards": sum(row["candidate_card_count"] > 0 for row in rows),
            "selected_article_count": len(selected_articles),
            "articles_with_candidate_cards": len(article_with_cards),
            "explicit_symbolic_bridge_count": 0,
        },
        "contract": {
            "safe_now": [
                "issue-tag metadata selects commentary targets for offline coverage supervision",
                "article identity selects candidate cards for authoritative explanation retrieval",
                "review_required and card function remain provenance/audit metadata",
            ],
            "not_implied": [
                "a candidate card is an active doctrine",
                "exception or defeater function supplies a RuleIR condition",
                "KCL issue tags may be injected as production runtime facts",
            ],
            "required_for_symbolic_bridge": [
                "stable branch or doctrine id",
                "typed requires expression over grounded predicates or relations",
                "effect and liability stage",
                "actor/offense-instance binding rule",
                "source card ids and review status",
            ],
        },
        "issue_tags": rows,
    }


def _markdown(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    no_cards = [
        row
        for row in audit["issue_tags"]
        if row["targets"] and row["candidate_card_count"] == 0
    ]
    unavailable = [row for row in audit["issue_tags"] if not row["targets"]]
    gaps = [
        row
        for row in audit["issue_tags"]
        if row["commentary_status"] == "mapped_with_corpus_gap"
    ]
    lines = [
        "# V2 doctrine/card bridge audit",
        "",
        "이 자료는 KCL issue tag를 runtime 입력으로 사용하지 않는 offline coverage audit이다.",
        "주석서나 카드가 존재한다는 사실은 symbolic doctrine activation을 뜻하지 않는다.",
        "",
        "## Summary",
        "",
        f"- KCL-26 issue tags: {audit['scope']['issue_tag_count']}",
        f"- commentary target 보유: {summary['tags_with_commentary_targets']}",
        f"- candidate card 보유: {summary['tags_with_candidate_cards']}",
        f"- target articles/card-covered articles: {summary['selected_article_count']}/{summary['articles_with_candidate_cards']}",
        f"- explicit symbolic bridge: {summary['explicit_symbolic_bridge_count']}",
        f"- corpus-gap tags: {len(gaps)}",
        "",
        "## Boundary",
        "",
        "카드는 조문별 설명·판례·적용기준을 회수하는 근거로 즉시 재사용할 수 있다. 그러나",
        "RuleIR로 내리려면 branch id, typed requires, effect/stage, instance binding, source card",
        "provenance를 별도로 authoring해야 한다. `exception`/`defeater` 분류만 보고 host가",
        "결론을 발화시키는 것은 금지한다.",
        "",
        "## Commentary target은 있으나 candidate card가 없는 tag",
        "",
    ]
    lines.extend(
        f"- `{row['issue_tag']}`: "
        + ", ".join(target["target_path"] for target in row["targets"])
        for row in no_cards
    )
    lines.extend(["", "## 현재 commentary target이 없는 tag", ""])
    lines.extend(f"- `{row['issue_tag']}`" for row in unavailable)
    lines.extend(["", "## 총칙 corpus gap tag", ""])
    lines.extend(
        f"- `{row['issue_tag']}` ({', '.join(row['case_ids'])})" for row in gaps
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, default=Path("data/v2/gold_occurrences.jsonl"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl"),
    )
    parser.add_argument(
        "--cards", type=Path, default=Path("data/rulebase/card_catalog_v2.json")
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/v2_restart_rebuild/doctrine_card_bridge_audit_v1"),
    )
    args = parser.parse_args()
    audit = build_audit(gold_path=args.gold, manifest_path=args.manifest, cards_path=args.cards)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    )
    (args.output_dir / "audit.md").write_text(_markdown(audit))
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
