#!/usr/bin/env python3
"""Build the criminal-law rulebase from the reviewed RuleIR cards.

Deterministic: same cards in, same artefacts out. Nothing here calls a model.

Currently emits the card census and the derived element skeleton, including the review
queue a legal reviewer needs to settle. The Datalog emission stage is added on top of
these same artefacts.

Usage::

    PYTHONPATH=src python scripts/build_rulebase.py            # write artefacts
    PYTHONPATH=src python scripts/build_rulebase.py --check     # report only, no writes
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulebase.cards import load_card_corpus  # noqa: E402
from idpr.rulebase.skeleton import (  # noqa: E402
    CORE,
    PRESUMED,
    derive_skeleton,
    skeleton_summary,
    strip_outline_numbering,
)

OUT_DIR = PROJECT_ROOT / "data/rulebase"
SKELETON_PATH = OUT_DIR / "element_skeleton.json"
REVIEW_PATH = OUT_DIR / "element_skeleton_review.md"
CENSUS_PATH = OUT_DIR / "card_census.json"


def build_card_census(corpus) -> dict:
    by_article = corpus.by_article()
    return {
        "live_cards": len(corpus.cards),
        "standard_input": len(corpus.standard_input_cards()),
        "deterministic_rule": len(corpus.deterministic_cards()),
        "articles": len(by_article),
        "slots": len(corpus.by_slot()),
        "by_norm_kind": dict(Counter(c.norm_kind for c in corpus.cards).most_common()),
        "by_polarity": dict(Counter(c.polarity for c in corpus.cards).most_common()),
        "by_doctrinal_status": dict(
            Counter(c.doctrinal_status for c in corpus.cards).most_common()
        ),
        "by_source_unit": dict(Counter(c.unit for c in corpus.cards).most_common()),
        "per_article": {
            article: {
                "cards": len(cards),
                "standard_input": sum(1 for c in cards if c.is_standard_input),
                "slots": len({c.slot for c in cards}),
            }
            for article, cards in by_article.items()
        },
    }


def build_skeleton_payload(classifications) -> dict:
    return {
        "version": "1.0.0",
        "summary": skeleton_summary(classifications),
        "slots": [
            {
                "slot": c.slot,
                "article": c.article,
                "role": c.role,
                "section_title": c.title,
                "title_role": c.title_role,
                "has_element_card": c.has_element_card,
                "cards": c.card_count,
                "standard_input": c.standard_input_count,
                "needs_review": c.needs_review,
                "review_priority": c.review_priority,
                "review_reason": c.review_reason,
            }
            for c in sorted(classifications, key=lambda x: (x.article, x.slot))
        ],
    }


def render_review_markdown(classifications) -> str:
    summary = skeleton_summary(classifications)
    blocking = [c for c in classifications if c.review_priority == "blocking"]
    advisory = [c for c in classifications if c.review_priority == "advisory"]

    lines = [
        "# 요건 스켈레톤 검수 요청 — `slot_core` / `slot_presumed`",
        "",
        "RuleIR 카드에는 '이 카드가 어느 죄의 어느 요건인가'가 없습니다. 주석서 목차",
        "(`section_title`)와 `norm_kind` 두 신호로 자동 도출했고, 아래는 **자동 판정이",
        "닿지 않은 항목만** 추린 것입니다.",
        "",
        f"- 전체 슬롯 **{summary['slots']}** / 조문 **{summary['articles']}**",
        "- 자동 분류: "
        + ", ".join(f"`{r}` {n}" for r, n in summary["by_role"].items()),
        f"- 검수 대상 **{summary['needs_review']}건** "
        f"(blocking {len(blocking)}, advisory {len(advisory)})",
        "",
        "## 판정이 필요한 이유",
        "",
        "`slot_core`는 **적극적 충족을 요구**하고 `slot_presumed`는 **반증이 있을 때만**",
        "죄의 성립을 막습니다. 모든 요건에 적극적 충족을 요구하면, 시험 답안이 자명한",
        "주체·객체를 논하지 않으므로 그 슬롯이 영구히 `unknown`이 되어 어떤 죄도",
        "성립하지 않습니다. 그래서 이 구분이 파이프라인의 동작 여부를 좌우합니다.",
        "",
        "역할별 의미:",
        "",
        "| 역할 | 죄 성립에 미치는 효과 |",
        "|---|---|",
        "| `core` | 충족되지 않으면 죄 불성립 (행위·고의·인과관계 등) |",
        "| `presumed` | 반증되지 않으면 충족으로 취급 (주체·객체) |",
        "| `stage` | 기수/미수 판단에만 사용 |",
        "| `defeater` | 충족되면 죄 성립을 저지 (위법성·책임) |",
        "| `concurrence` | 죄수 관계 판단 재료 |",
        "| `context` | 성립 판단에 미사용 (의의·판례 예시) |",
        "| `participation` | 총칙 공범 영역 — 현재 규칙 없음 |",
        "",
        "## blocking — 역할을 특정하지 못한 슬롯",
        "",
        "자동 판정이 제목에서 역할을 읽어내지 못했습니다. `제안 역할`은 `norm_kind`만으로",
        "둔 잠정값이니 맞는지 봐 주세요.",
        "",
        "| 조문 | 슬롯 | 주석서 제목 | 카드 | 제안 역할 | 사유 |",
        "|---|---|---|---:|---|---|",
    ]
    for c in sorted(blocking, key=lambda x: (x.article, x.slot)):
        reason = c.review_reason.split(":", 1)[0]
        title = strip_outline_numbering(c.title).replace("|", r"\|")
        lines.append(
            f"| {c.article} | `{c.slot}` | {title} | {c.card_count} | `{c.role}` | {reason} |"
        )

    lines += [
        "",
        "## advisory — 역할은 맞을 듯하나 편성이 이상한 슬롯",
        "",
        "`norm_kind: element` 카드가 죄수·위법성·공범 절에 편성되어 있습니다. 제목 기준",
        "역할을 그대로 썼으니 반대 판단이 필요하면 알려 주세요.",
        "",
        "| 조문 | 슬롯 | 주석서 제목 | 카드 | 적용 역할 |",
        "|---|---|---|---:|---|",
    ]
    for c in sorted(advisory, key=lambda x: (x.article, x.slot)):
        title = strip_outline_numbering(c.title).replace("|", r"\|")
        lines.append(
            f"| {c.article} | `{c.slot}` | {title} | {c.card_count} | `{c.role}` |"
        )

    element_free = summary["articles_without_core_slot"]
    lines += [
        "",
        "## 참고 — `core` 슬롯이 없는 조문",
        "",
        f"`{'`, `'.join(element_free)}`" if element_free else "(없음)",
        "",
        "미수범 규정(제254·300·342조)과 친족상도례(제328·344조)는 고유 구성요건이 없는",
        "조문이므로 `core` 슬롯이 없는 것이 정상입니다. 이 목록에 다른 조문이 나타나면",
        "스켈레톤 누락입니다.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report the census and skeleton without writing artefacts",
    )
    args = parser.parse_args()

    corpus = load_card_corpus()
    classifications = derive_skeleton(corpus)
    census = build_card_census(corpus)
    summary = skeleton_summary(classifications)

    print("=== card census ===")
    print(
        f"live cards {census['live_cards']} "
        f"(standard_input {census['standard_input']}, "
        f"deterministic_rule {census['deterministic_rule']})"
    )
    print(f"articles {census['articles']}, slots {census['slots']}")
    print()
    print("=== element skeleton ===")
    for role, count in summary["by_role"].items():
        print(f"  {role:15} {count:4}")
    print(
        f"review queue {summary['needs_review']} "
        f"({summary['review_by_priority']})"
    )
    print(f"articles without a core slot: {summary['articles_without_core_slot']}")

    if args.check:
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CENSUS_PATH.write_text(
        json.dumps(census, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    SKELETON_PATH.write_text(
        json.dumps(
            build_skeleton_payload(classifications),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    REVIEW_PATH.write_text(render_review_markdown(classifications), encoding="utf-8")
    print()
    for path in (CENSUS_PATH, SKELETON_PATH, REVIEW_PATH):
        print(f"wrote {path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
