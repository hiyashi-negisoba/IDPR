"""Measure whether legacy article-level concurrence relations can enter v2 safely."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.card_issue_bridge import criminal_act_article_key


def build_audit(*, definitions: Path, concurrence: Path, review: Path) -> dict[str, Any]:
    registry = load_definitions(definitions)
    refs_by_article: dict[str, list[str]] = defaultdict(list)
    for entry in registry.by_kind.get("offense", ()):
        identity = entry.payload.get("identity") or {}
        for statutory_ref in identity.get("statutory_refs") or ():
            key = criminal_act_article_key(str(statutory_ref))
            if key is not None:
                refs_by_article[key].append(entry.id)

    approved = json.loads(review.read_text())
    approved_cards = {
        str(card_id)
        for decision in approved.get("decisions", ())
        for card_id in decision.get("anchor_card_ids", ())
    }
    payload = yaml.safe_load(concurrence.read_text())
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for kind, key in (
        ("absorption", "absorbed_by"),
        ("imaginative_concurrence", "imaginative_concurrence"),
    ):
        for index, value in enumerate(payload.get(key) or ()):
            articles = (
                (str(value["child"]), str(value["parent"]))
                if kind == "absorption"
                else tuple(str(item) for item in value["offenses"])
            )
            mapped = tuple(tuple(refs_by_article.get(article, ())) for article in articles)
            if any(not refs for refs in mapped):
                identity_status = "MISSING_V2_OFFENSE_SIDE"
            elif any(len(refs) != 1 for refs in mapped):
                identity_status = "AMBIGUOUS_ARTICLE_TO_OFFENSE"
            else:
                identity_status = "EXACT_ONE_TO_ONE"
            counts[identity_status] += 1
            condition = str(value["condition"])
            condition_status = (
                "APPROVED_ISSUE_ANCHOR"
                if condition in approved_cards
                else "NOT_IN_APPROVED_ISSUE_ANCHORS"
            )
            counts[condition_status] += 1
            production_ready = (
                identity_status == "EXACT_ONE_TO_ONE"
                and condition_status == "APPROVED_ISSUE_ANCHOR"
                and "awaiting" not in str(payload.get("status", ""))
            )
            rows.append(
                {
                    "legacy_rule": f"{key}[{index}]",
                    "kind": kind,
                    "articles": list(articles),
                    "mapped_offense_refs": [list(refs) for refs in mapped],
                    "condition_card_id": condition,
                    "condition_status": condition_status,
                    "identity_status": identity_status,
                    "production_ready": production_ready,
                    "remaining_requirements": [
                        "exact DefinitionRef pair authoring",
                        "same factual episode binding",
                        "instance-scoped condition assessment",
                    ],
                }
            )
    return {
        "source_status": payload.get("status"),
        "summary": {
            "legacy_rule_count": len(rows),
            **dict(sorted(counts.items())),
            "production_ready": sum(row["production_ready"] for row in rows),
        },
        "contract": {
            "legacy_article_relation_is_not_v2_rule": True,
            "unknown_condition_keeps_both_instances": True,
            "default_without_authored_relation": "retain separately established instances",
        },
        "rules": rows,
    }


def _markdown(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    lines = [
        "# V2 concurrence identity audit",
        "",
        f"- legacy source status: `{audit['source_status']}`",
        f"- legacy rules: {summary['legacy_rule_count']}",
        f"- exact one-to-one article mapping: {summary.get('EXACT_ONE_TO_ONE', 0)}",
        f"- ambiguous article mapping: {summary.get('AMBIGUOUS_ARTICLE_TO_OFFENSE', 0)}",
        f"- missing v2 offense side: {summary.get('MISSING_V2_OFFENSE_SIDE', 0)}",
        f"- approved condition anchor: {summary.get('APPROVED_ISSUE_ANCHOR', 0)}",
        f"- production-ready rules: {summary['production_ready']}",
        "",
        "Article relation은 v2 rule이 아니다. exact `DefinitionRef` pair, same factual episode,",
        "instance-scoped condition assessment를 별도로 authoring해야 한다.",
        "",
        "## Rules",
        "",
    ]
    for row in audit["rules"]:
        lines.append(
            f"- `{row['legacy_rule']}` {row['articles']} -> "
            f"{row['mapped_offense_refs']}: {row['identity_status']}, "
            f"condition={row['condition_status']}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definitions", type=Path, default=Path("data/v2/definitions"))
    parser.add_argument(
        "--concurrence", type=Path, default=Path("data/rulebase/concurrence.yaml")
    )
    parser.add_argument(
        "--review", type=Path, default=Path("data/rulebase/issue_rule_review.json")
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/v2_call15_directscope_26_causal/concurrence_identity_v1"),
    )
    args = parser.parse_args()
    audit = build_audit(
        definitions=args.definitions,
        concurrence=args.concurrence,
        review=args.review,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    )
    (args.output_dir / "audit.md").write_text(_markdown(audit))
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
