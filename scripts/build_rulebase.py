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
from idpr.rulebase.facts import (  # noqa: E402
    FACT_PREDICATES,
    VOCABULARIES,
    scl_fact_layer,
    vocabulary_size,
)
from idpr.rulebase.formalization import (  # noqa: E402
    CONCURRENCE_SEED,
    MODEL_ASSESS,
    NARRATIVE,
    SKELETON_META,
    STAGE_SEED,
    route_corpus,
    routing_summary,
)
from idpr.rulebase.review import (  # noqa: E402
    parse_review,
    review_summary,
    verdict_map,
)
from idpr.rulebase.skeleton import (  # noqa: E402
    CONCURRENCE,
    CONTEXT,
    CORE,
    DEFEATER,
    PARTICIPATION,
    PRESUMED,
    STAGE,
    derive_skeleton,
    example_slot_for_role,
    skeleton_summary,
    strip_outline_numbering,
)

OUT_DIR = PROJECT_ROOT / "data/rulebase"
SKELETON_PATH = OUT_DIR / "element_skeleton.json"
REVIEW_PATH = OUT_DIR / "element_skeleton_review.md"
CENSUS_PATH = OUT_DIR / "card_census.json"
FACT_LAYER_PATH = OUT_DIR / "fact_layer.scl"
TRIAGE_PATH = OUT_DIR / "card_routing.json"
ROLE_REVIEW_PATH = OUT_DIR / "role_review.json"


def build_role_review_payload(verdicts, classifications, corpus) -> dict:
    """The reviewer's card-level verdicts, plus which queue items are still open.

    Emitted as a build artefact rather than kept only in the markdown so that the roles
    the symbolic layer consumes come from one parsed source. The open items are listed
    because a queue item with no annotation keeps its automatic role, and that needs to
    be visible rather than assumed.
    """
    reviewed_items = {verdict.item for verdict in verdicts}
    blocking = sorted(
        (c for c in classifications if c.review_priority == "blocking"),
        key=lambda c: (c.article, c.slot),
    )
    advisory = sorted(
        (c for c in classifications if c.review_priority == "advisory"),
        key=lambda c: (c.article, c.slot),
    )
    labelled = [
        (f"B{index}", c) for index, c in enumerate(blocking, 1)
    ] + [(f"A{index}", c) for index, c in enumerate(advisory, 1)]
    open_items = [
        {
            "item": item,
            "slot": c.slot,
            "article": c.article,
            "automatic_role": c.role,
            "cards": c.card_count,
        }
        for item, c in labelled
        if item not in reviewed_items
    ]
    return {
        "version": "1.0.0",
        "summary": review_summary(verdicts),
        "open_queue_items": open_items,
        "card_roles": [
            {
                "card_id": verdict.card_id,
                "role": verdict.role,
                "slot": verdict.slot,
                "article": verdict.article,
                "item": verdict.item,
                "card_index": verdict.card_index,
                "applies_to_whole_slot": verdict.applies_to_whole_slot,
                "tentative": verdict.tentative,
                "conditional": verdict.conditional,
                "has_question": verdict.has_question,
                "comment": verdict.comment,
                "proposition": corpus.by_id[verdict.card_id].proposition,
            }
            for verdict in sorted(
                verdicts, key=lambda v: (v.article, v.slot, v.card_index)
            )
        ],
    }


def build_triage_payload(routings, corpus) -> dict:
    """Every card's routing decision, grouped by route with the proposition inline.

    The propositions are included because the routes feed hand-authored artefacts next
    (the stage table and ``concurrence.yaml``), and those cannot be drafted from card ids.
    """
    by_id = corpus.by_id
    grouped: dict[str, list[dict]] = {}
    for routing in sorted(routings, key=lambda r: (r.article, r.slot, r.card_id)):
        grouped.setdefault(routing.route, []).append(
            {
                "card_id": routing.card_id,
                "article": routing.article,
                "slot": routing.slot,
                "norm_kind": routing.norm_kind,
                "corpus_formalization": routing.corpus_formalization,
                "open_texture_markers": list(routing.open_texture_markers),
                "frames_matched": list(routing.frames_matched),
                "proposition": by_id[routing.card_id].proposition,
            }
        )
    return {
        "version": "1.0.0",
        "summary": routing_summary(routings),
        "fact_layer": {
            "predicates": len(FACT_PREDICATES),
            "labels": vocabulary_size(),
            "vocabularies": {name: len(labels) for name, labels in VOCABULARIES.items()},
        },
        "by_route": grouped,
    }


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


_ROLE_CHOICES = "`core` / `presumed` / `stage` / `defeater` / `concurrence` / `context`"


def _render_slot_cards(slot: str, corpus) -> list[str]:
    """Every card in a slot, verbatim, so the role can actually be judged.

    The role question is 'do these propositions state a requirement the prosecution must
    prove?', which is unanswerable from the slot title and card count alone.
    """
    cards = corpus.by_slot().get(slot, ())
    lines = [
        "",
        "| # | norm_kind | polarity | formalization | 명제 |",
        "|---:|---|---|---|---|",
    ]
    for index, card in enumerate(cards, start=1):
        proposition = card.proposition.replace("|", r"\|")
        lines.append(
            f"| {index} | {card.norm_kind} | {card.polarity} | "
            f"{card.formalization} | {proposition} |"
        )
    return lines


#: Per-role reviewer guidance: why the example slot got its role, and what the role does
#: to the offence gate. The order here is the order the examples are rendered in.
_ROLE_EXAMPLE_NOTES: tuple[tuple[str, str, str], ...] = (
    (
        CORE,
        "카드가 모두 '이것이 있어야 죄가 된다'를 말합니다. 고의는 사안마다 다투어지므로 "
        "검사가 적극적으로 증명해야 하는 요건입니다.",
        "이 슬롯이 `satisfied`가 되지 않으면 해당 죄는 성립하지 않습니다.",
    ),
    (
        PRESUMED,
        "요건이기는 하나 사안에서 거의 다투어지지 않습니다. 카드도 '주체는 절도범이다'라는 "
        "확인과, 그에 해당하지 않는 경우를 짚는 예외로 구성되어 있습니다.",
        "답안이 언급하지 않아도 통과하고, 카드가 `not_satisfied`로 명시 반증될 때만 죄의 "
        "성립을 막습니다.",
    ),
    (
        STAGE,
        "요건의 충족 여부가 아니라 **언제 기수가 되는가**를 말합니다.",
        "성립 게이트에는 들어가지 않고 기수/미수 판정에만 쓰입니다.",
    ),
    (
        DEFEATER,
        "충족되면 죄의 성립을 **저지**하는 사유입니다. 요건과 방향이 반대입니다.",
        "`satisfied`가 되면 다른 요건이 모두 충족되어도 죄가 성립하지 않습니다.",
    ),
    (
        CONCURRENCE,
        "계속범·포괄일죄처럼 **다른 죄 또는 다른 행위와의 관계**를 말합니다.",
        "성립 판단에는 쓰이지 않고, 죄수 정의(`absorbed_by`)의 초안 재료가 됩니다.",
    ),
    (
        PARTICIPATION,
        "공범·신분 등 형법총칙 영역입니다. 총칙 주석서를 적재하지 않았으므로 대응 규칙이 "
        "없습니다.",
        "성립 판단에 쓰이지 않습니다. 서술 재료로만 남습니다.",
    ),
    (
        CONTEXT,
        "죄의 정의·연혁·판례 예시입니다. 증명의 대상이 아닙니다.",
        "성립 판단에 쓰이지 않고 Rule 문단 서술에만 쓰입니다.",
    ),
)

#: A correctly-titled slot whose cards nonetheless point at a different role. Shown so the
#: reviewer knows that pointing out a misclassification *outside* the queue is welcome.
_BORDERLINE_SLOT = "art329_sec3_1"


def render_role_examples(classifications, corpus) -> list[str]:
    """One worked example per role, drawn from slots the derivation settled on its own."""
    lines = [
        "## 분류 예시 — 자동 분류가 판정한 실제 슬롯",
        "",
        "아래는 검수 대상이 **아닌**, 자동 분류가 확정한 슬롯들입니다. 각 역할이 실제로",
        "어떤 카드 묶음에 붙는지 보시고 같은 기준으로 판정해 주세요.",
    ]
    for role, why, effect in _ROLE_EXAMPLE_NOTES:
        example = example_slot_for_role(role, classifications)
        if example is None:
            continue
        title = strip_outline_numbering(example.title)
        lines += [
            "",
            f"### `{role}` 예시 — {example.article} · `{example.slot}` "
            f"— {title or '(제목 없음)'}",
            "",
            f"- 왜 `{role}`인가: {why}",
            f"- 심볼릭에서의 효과: {effect}",
        ]
        lines += _render_slot_cards(example.slot, corpus)

    borderline = next(
        (c for c in classifications if c.slot == _BORDERLINE_SLOT), None
    )
    if borderline is not None and not borderline.needs_review:
        lines += [
            "",
            "### 경계 사례 — 제목과 내용이 어긋난 슬롯",
            "",
            f"{borderline.article} · `{borderline.slot}` "
            f"— {strip_outline_numbering(borderline.title)}: 제목이 '개념'이라 "
            f"**`{borderline.role}`**로 분류됐지만, 카드는 절취의 성립 범위를 정하고 있어",
            "행위 요건(`core`)에 가깝습니다. 이런 슬롯은 검수 대기열에 올라오지 않으므로,",
            "눈에 띄면 슬롯 ID만 알려 주세요.",
        ]
        lines += _render_slot_cards(borderline.slot, corpus)
    return lines


def render_review_markdown(classifications, corpus) -> str:
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
        "## 무엇을 답해 주시면 되는지",
        "",
        f"각 항목마다 역할 하나만 골라 주세요: {_ROLE_CHOICES}.",
        "제안 역할이 맞으면 넘어가셔도 됩니다. 판단 기준은 **'이 명제들이 검사가",
        "증명해야 하는 요건을 말하는가'** 입니다.",
        "",
        "- 요건을 말한다 → 그 요건이 통상 다투어지면 `core`, 자명하면 `presumed`",
        "- 미수·기수 시기를 말한다 → `stage`",
        "- 성립을 저지하는 사유를 말한다 → `defeater`",
        "- 다른 죄와의 관계를 말한다 → `concurrence`",
        "- 요건이 아니라 의의·판례 예시·처벌 규정이다 → `context`",
        "",
        "---",
        "",
    ]
    lines += render_role_examples(classifications, corpus)
    lines += [
        "",
        "---",
        "",
        "## blocking — 역할을 특정하지 못한 슬롯",
        "",
        "제목에서 역할을 읽어내지 못했습니다. `제안 역할`은 `norm_kind`만으로 둔 잠정값입니다.",
    ]
    for index, c in enumerate(sorted(blocking, key=lambda x: (x.article, x.slot)), 1):
        title = strip_outline_numbering(c.title)
        reason = c.review_reason.split(":", 1)[0]
        lines += [
            "",
            f"### B{index}. {c.article} · `{c.slot}` — {title or '(제목 없음)'}",
            "",
            f"- 제안 역할: **`{c.role}`**  |  카드 {c.card_count}장 "
            f"(standard_input {c.standard_input_count})  |  사유: {reason}",
        ]
        lines += _render_slot_cards(c.slot, corpus)

    lines += [
        "",
        "---",
        "",
        "## advisory — 역할은 맞을 듯하나 편성이 이상한 슬롯",
        "",
        "`norm_kind: element` 카드가 죄수·위법성·공범 절에 편성되어 있습니다. 제목 기준",
        "역할을 그대로 적용했으니, 반대 판단이 필요한 것만 지적해 주세요.",
    ]
    for index, c in enumerate(sorted(advisory, key=lambda x: (x.article, x.slot)), 1):
        title = strip_outline_numbering(c.title)
        lines += [
            "",
            f"### A{index}. {c.article} · `{c.slot}` — {title or '(제목 없음)'}",
            "",
            f"- 적용 역할: **`{c.role}`**  |  카드 {c.card_count}장 "
            f"(standard_input {c.standard_input_count})",
        ]
        lines += _render_slot_cards(c.slot, corpus)

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


#: The marker the reviewer's annotations use. Its presence makes the review document a
#: hand-edited legal artefact rather than build output.
_ANNOTATION_MARKER = "> comment:"


def _review_is_annotated() -> bool:
    return (
        REVIEW_PATH.is_file()
        and _ANNOTATION_MARKER in REVIEW_PATH.read_text(encoding="utf-8")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report the census and skeleton without writing artefacts",
    )
    parser.add_argument(
        "--rewrite-review",
        action="store_true",
        help=(
            "regenerate element_skeleton_review.md even when it carries the reviewer's "
            "annotations. Discards them -- they are legal review, not build output."
        ),
    )
    args = parser.parse_args()

    corpus = load_card_corpus()
    classifications = derive_skeleton(corpus)
    census = build_card_census(corpus)
    summary = skeleton_summary(classifications)
    routings = route_corpus(corpus)
    routing = routing_summary(routings)
    verdicts = parse_review(corpus=corpus) if REVIEW_PATH.is_file() else ()
    review = review_summary(verdicts)

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
    print()
    print("=== fact layer ===")
    print(f"  {len(FACT_PREDICATES)} predicates, {vocabulary_size()} closed labels")
    print()
    print("=== card routing ===")
    for route, count in routing["by_route"].items():
        print(f"  {route:18} {count:5}")
    print(
        f"open-textured {routing['open_textured']} "
        f"({routing['open_textured_by_corpus_label']})"
    )
    print(
        f"symbolic seeds {routing['symbolic_seed_cards']} cards "
        f"over {routing['symbolic_seed_articles']} articles; "
        f"routing disagrees with formalization on {routing['contradicting_cards']}"
    )

    print()
    print("=== reviewed card roles ===")
    print(
        f"  {review['verdicts']} verdicts over {review['items']} queue items "
        f"({summary['needs_review']} queued)"
    )
    for role, count in review["by_role"].items():
        print(f"  {role:15} {count:4}")
    print(f"  slots split across roles: {len(review['slots_split_across_roles'])}")

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
    written = [CENSUS_PATH, SKELETON_PATH]
    if _review_is_annotated() and not args.rewrite_review:
        print(
            f"\nskipped {REVIEW_PATH.relative_to(PROJECT_ROOT)}: it carries the "
            f"reviewer's annotations. Pass --rewrite-review to regenerate it, which "
            f"discards them."
        )
    else:
        REVIEW_PATH.write_text(
            render_review_markdown(classifications, corpus), encoding="utf-8"
        )
        written.append(REVIEW_PATH)
    TRIAGE_PATH.write_text(
        json.dumps(
            build_triage_payload(routings, corpus), ensure_ascii=False, indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    FACT_LAYER_PATH.write_text(scl_fact_layer() + "\n", encoding="utf-8")
    ROLE_REVIEW_PATH.write_text(
        json.dumps(
            build_role_review_payload(verdicts, classifications, corpus),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    written += [TRIAGE_PATH, FACT_LAYER_PATH, ROLE_REVIEW_PATH]
    print()
    for path in written:
        print(f"wrote {path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
