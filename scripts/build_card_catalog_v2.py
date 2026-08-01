"""Build the provisional runtime-oriented card catalog and a focused review document."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

from idpr.rulebase.card_catalog_v2 import (
    ALWAYS_ASSESS,
    CATALOG_VERSION,
    RELATION_CONDITION,
    RETRIEVE_ASSESS,
    RETRIEVE_ONLY,
    STATIC,
    CatalogCard,
    catalog_payload,
    compile_card_catalog_v2,
)
from idpr.rulebase.cards import PROJECT_ROOT

DEFAULT_OUT = PROJECT_ROOT / "data/rulebase/card_catalog_v2.json"
DEFAULT_REVIEW = PROJECT_ROOT / "data/rulebase/card_catalog_v2_review.md"
DEFAULT_FOCUS = ("art297", "art298", "art301", "art319")


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _runtime_counts(cards: Sequence[CatalogCard]) -> str:
    counts = Counter(card.runtime for card in cards)
    order = (ALWAYS_ASSESS, RETRIEVE_ASSESS, RETRIEVE_ONLY, RELATION_CONDITION, STATIC)
    return ", ".join(f"{name}={counts.get(name, 0)}" for name in order)


def render_review(cards: Sequence[CatalogCard], focus: Sequence[str]) -> str:
    focus_set = set(focus)
    focus_order = {article: index for index, article in enumerate(focus)}
    selected = sorted(
        (card for card in cards if card.article in focus_set),
        key=lambda card: focus_order[card.article],
    )
    priority = [
        card
        for card in selected
        if card.function == "canonical_element" or card.review_required
    ]
    lines = [
        "# Card catalog v2 — 재분류 검수",
        "",
        f"버전 `{CATALOG_VERSION}`. 원본 RuleIR 카드는 수정하지 않았다.",
        "",
        "`canonical_element`는 카드 자체가 `norm_kind=element`일 때만 부여한다. "
        "slot이 core라는 이유로 하위 판례·사례 카드가 core를 상속하지 않는다.",
        "",
        "## 요약",
        "",
        f"- 전체 카드: {len(cards)}",
        f"- 상세 검수 대상: {len(selected)} ({', '.join(focus)})",
        f"- 전체 runtime: {_runtime_counts(cards)}",
        f"- 대상 runtime: {_runtime_counts(selected)}",
        f"- 대상 중 자동분류 검수 필요: {sum(c.review_required for c in selected)}",
        f"- 우선 검수 큐(구성요건 후보 ∪ 자동분류 주의): {len(priority)}",
        "",
        "먼저 아래 우선 검수 큐를 확인한다. 상세 문맥이 필요하면 각 element group 표를 "
        "보고, `> comment:`에 잘못된 분류와 원하는 "
        "`function/form/runtime/gate_effect`를 적는다.",
        "",
        "## 우선 검수 큐",
        "",
        "| article | group | id | kind | function | form | runtime | 주의 사유 | proposition |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for card in priority:
        reasons = "; ".join(card.review_reasons)
        if card.function == "canonical_element" and not reasons:
            reasons = "canonical_element 후보 확인"
        lines.append(
            "| "
            + " | ".join(
                _escape(value)
                for value in (
                    card.article,
                    card.element_group,
                    card.card_id,
                    card.norm_kind,
                    card.function,
                    card.form,
                    card.runtime,
                    reasons,
                    card.proposition,
                )
            )
            + " |"
        )
    lines += ["", "> comment:", ""]
    for article in focus:
        article_cards = [card for card in selected if card.article == article]
        lines += [f"## {article}", ""]
        groups = list(dict.fromkeys(card.element_group for card in article_cards))
        for group in groups:
            group_cards = [card for card in article_cards if card.element_group == group]
            lines += [f"### {group}", ""]
            lines += [
                "| id | kind | polarity | function | form | runtime | gate | proposition |",
                "|---|---|---|---|---|---|---|---|",
            ]
            for card in group_cards:
                lines.append(
                    "| "
                    + " | ".join(
                        _escape(value)
                        for value in (
                            card.card_id,
                            card.norm_kind,
                            card.polarity,
                            card.function,
                            card.form,
                            card.runtime,
                            card.gate_effect,
                            card.proposition,
                        )
                    )
                    + " |"
                )
            reasons = sorted(
                {reason for card in group_cards for reason in card.review_reasons}
            )
            if reasons:
                lines += ["", "자동분류 주의: " + "; ".join(reasons)]
            lines += ["", "> comment:", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--focus", nargs="+", default=list(DEFAULT_FOCUS))
    args = parser.parse_args()

    cards = compile_card_catalog_v2()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(catalog_payload(cards), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.review.parent.mkdir(parents=True, exist_ok=True)
    args.review.write_text(render_review(cards, args.focus), encoding="utf-8")
    print(json.dumps(catalog_payload(cards)["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")
    print(f"wrote {args.review}")


if __name__ == "__main__":
    main()
