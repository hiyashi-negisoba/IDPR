"""Build the hierarchical issue-first card catalog and a focused legal review table."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

from idpr.candidates import assessable_card_ids
from idpr.rulebase.cards import PROJECT_ROOT, card_corpus
from idpr.rulebase.issue_catalog_v2 import (
    ASSESS_ISSUE,
    ISSUE_CATALOG_VERSION,
    CardPlacement,
    IssuePacket,
    compile_issue_catalog_v2,
    issue_catalog_payload,
    issue_catalog_summary,
)

DEFAULT_OUT = PROJECT_ROOT / "data/rulebase/issue_catalog_v2.json"
DEFAULT_REVIEW = PROJECT_ROOT / "data/rulebase/issue_catalog_v2_review.md"
DEFAULT_FOCUS = ("art297", "art298", "art301", "art319", "art329")
SMOKE_FOCUS = frozenset({"art297", "art298", "art301", "art319"})


def _escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_review(
    issues: Sequence[IssuePacket],
    placements: Sequence[CardPlacement],
    focus: Sequence[str],
) -> str:
    corpus = card_corpus()
    cards_by_id = corpus.by_id
    focus_set = set(focus)
    selected = [issue for issue in issues if issue.article in focus_set]
    selected_placements = [
        item for item in placements if item.issue_id.split(".", 1)[0] in focus_set
    ]
    assess = [issue for issue in selected if issue.runtime == ASSESS_ISSUE]
    priority = [
        issue
        for issue in selected
        if issue.review_required and issue.runtime == ASSESS_ISSUE
    ]
    policy_counts = Counter(item.load_policy for item in selected_placements)
    smoke_cards = [card for card in corpus.cards if card.article in SMOKE_FOCUS]
    assessable_ids = assessable_card_ids(corpus)
    smoke_issues = [issue for issue in issues if issue.article in SMOKE_FOCUS]
    smoke_assess = [issue for issue in smoke_issues if issue.runtime == ASSESS_ISSUE]
    lines = [
        "# Issue catalog v2 — 카드 재적재 검수",
        "",
        f"버전 `{ISSUE_CATALOG_VERSION}`. 원본 RuleIR 1,848장은 수정하지 않았다.",
        "",
        "런타임의 기본 단위는 카드가 아니라 `issue packet`이다. 일반법리 anchor만 "
        "issue와 함께 적재하고, 세부 판단기준·구체 사실패턴은 관련 사실이 있을 때만 검색한다.",
        "",
        "## 축소 결과",
        "",
        f"- 전체: 카드 {len(placements)}장 → issue {len(issues)}개 → 기본 평가 issue "
        f"{sum(issue.runtime == ASSESS_ISSUE for issue in issues)}개",
        f"- 검수 조문: 카드 {len(selected_placements)}장 → issue {len(selected)}개 → "
        f"기본 평가 issue {len(assess)}개",
        f"- 현재 4조문 스모크: Call-2 카드 {sum(card.id in assessable_ids for card in smoke_cards)}장 "
        f"→ 기본 평가 issue {len(smoke_assess)}개",
        f"- 검수 조문 load policy: "
        + ", ".join(f"{key}={value}" for key, value in policy_counts.most_common()),
        f"- 검수 조문 구체 사실패턴: "
        f"{sum(len(issue.case_pattern_card_ids) for issue in selected)}장",
        f"- 우선 법률 검수: {len(priority)}개 기본 평가 issue",
        "",
        "`anchor_context`는 질문이 아니라 해당 issue 판단에 함께 주는 일반법리다. "
        "`retrieval_candidate`는 사건 사실과 관련될 때만 붙인다.",
        "",
        "## 우선 법률 검수 큐",
        "",
        "| issue | 제목 | anchors | cards | cases | 검수 사유 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for issue in priority:
        lines.append(
            "| "
            + " | ".join(
                _escape(value)
                for value in (
                    issue.issue_id,
                    issue.title,
                    len(issue.anchor_card_ids),
                    len(issue.member_card_ids),
                    len(issue.case_pattern_card_ids),
                    "; ".join(issue.review_reasons),
                )
            )
            + " |"
        )
    lines += ["", "> comment:", ""]

    for article in focus:
        article_issues = [issue for issue in selected if issue.article == article]
        if not article_issues:
            continue
        article_cards = sum(len(issue.member_card_ids) for issue in article_issues)
        article_assess = sum(issue.runtime == ASSESS_ISSUE for issue in article_issues)
        lines += [
            f"## {article} — 카드 {article_cards}장 / 기본 평가 issue {article_assess}개",
            "",
            "| issue | 제목 | function | runtime | anchors | retrieve | cases | review |",
            "|---|---|---|---|---:|---:|---:|---|",
        ]
        for issue in article_issues:
            lines.append(
                "| "
                + " | ".join(
                    _escape(value)
                    for value in (
                        issue.issue_id,
                        issue.title,
                        issue.function,
                        issue.runtime,
                        len(issue.anchor_card_ids),
                        len(issue.retrieval_card_ids),
                        len(issue.case_pattern_card_ids),
                        "yes" if issue.review_required else "",
                    )
                )
                + " |"
            )
        lines += ["", "### anchor 일반법리", ""]
        lines += [
            "| issue | card id | proposition |",
            "|---|---|---|",
        ]
        for issue in article_issues:
            for card_id in issue.anchor_card_ids:
                lines.append(
                    "| "
                    + " | ".join(
                        _escape(value)
                        for value in (
                            issue.issue_id,
                            card_id,
                            cards_by_id[card_id].proposition,
                        )
                    )
                    + " |"
                )
        lines += ["", "> comment:", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--focus", nargs="+", default=list(DEFAULT_FOCUS))
    args = parser.parse_args()

    issues, placements = compile_issue_catalog_v2()
    payload = issue_catalog_payload(issues, placements)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.review.parent.mkdir(parents=True, exist_ok=True)
    args.review.write_text(
        render_review(issues, placements, args.focus), encoding="utf-8"
    )
    print(json.dumps(issue_catalog_summary(issues, placements), ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")
    print(f"wrote {args.review}")


if __name__ == "__main__":
    main()
