"""재산죄 RuleIR 법리 검토 문서 — `human_rule_ir_review` 게이트 (API 0회).

사기가 밟은 순서 중 에이전트 검토(`agent_rule_ir_review`)를 먼저 끝내고, 사용자가 판단해야 하는
것만 남겨 문서로 낸다. 규칙 2,174개를 한 줄씩 읽히지 않는다 — 규칙은 카드에서 기계적으로 조립되므로
검토할 것은 **카드가 규칙 구조에서 어떤 자리를 차지하는가**뿐이다.

사용자 판단이 필요한 것 둘:
  1. 부정·예외 카드 138장의 **역할 지정**(`rule_ir_card_roles.json`) — 저지·요건불요·경계획정·
     인정경로 중 무엇인가. 이 지정이 규칙 구조를 정한다.
  2. 얇은 component — 인정 경로가 1~2장뿐인 구성요건 단계

에이전트 검토에서 이미 고친 것은 문서에 근거만 남긴다(정규식 분류 폐기, 강도 객체 레벨 오배정).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_property_rule_ir import (  # noqa: E402
    DEFERRED_UNITS,
    LEVEL_COMPONENTS,
    OUT_DIR,
    PHASE_MAP,
    UNIT_MANIFEST,
    UNITS,
    UnitBuilder,
    read_json,
)

PROP = ROOT / "data/rulegen/property"
OUT_JSON = PROP / "rule_ir_review_queue.json"
OUT_DOC = PROP / "RuleIR_법리검토.md"
THIN_THRESHOLD = 2

KIND_LABELS = {
    "bar": "저지 — 요건 결여·배제 사유",
    "boundary": "경계획정 — 이 죄 불성립 + 다른 죄로",
    "waiver": "요건 불요 — 성립을 막지 않음",
}


def main() -> None:
    phase_rows = read_json(PHASE_MAP)["rows"]
    manifest = read_json(UNIT_MANIFEST)
    units: list[dict[str, Any]] = []

    for entry in manifest["units"]:
        unit = entry["issue_tag"]
        if unit in DEFERRED_UNITS:
            continue
        card_set = read_json(UNITS / f"{unit}.json")
        builder = UnitBuilder(unit, card_set, phase_rows)
        rule_ir = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")

        components = []
        for level in builder.active_components():
            members = [card for card in builder.cards_at(level)
                       if not builder.negative_kind(card)]
            components.append({
                "level": level,
                "component": builder.component_id(level),
                "label": LEVEL_COMPONENTS[level][0],
                "cards": [{"id": card["id"], "proposition": card["proposition"]}
                          for card in members],
                "thin": len(members) <= THIN_THRESHOLD,
            })
        roles = builder.card_roles
        classified = {kind: [{"id": card["id"], "proposition": card["proposition"],
                              "rationale": roles[card["id"]]["rationale"],
                              "refers_to": roles[card["id"]]["refers_to"]}
                             for card in builder.cards_of_kind(kind)]
                      for kind in KIND_LABELS}
        classified["component"] = [
            {"id": card["id"], "proposition": card["proposition"],
             "rationale": roles[card["id"]]["rationale"], "refers_to": None}
            for card in card_set["cards"]
            if roles.get(card["id"], {}).get("role") == "component"]
        aggravation = {kind: [card["id"] for card in cards]
                       for kind, cards in builder.aggravation_kinds().items()}
        units.append({
            "unit": unit, "label": entry["label"], "articles": entry["articles"],
            "cards": len(card_set["cards"]),
            "predicates": len(rule_ir["predicates"]), "rules": len(rule_ir["rules"]),
            "components": components, "classified": classified,
            "aggravation": aggravation,
        })

    totals = Counter()
    for item in units:
        for kind, cards in item["classified"].items():
            totals[kind] += len(cards)
        totals["thin"] += sum(1 for component in item["components"] if component["thin"])

    OUT_JSON.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "gate": "human_rule_ir_review",
        "counts": {"units": len(units),
                   "rules": sum(item["rules"] for item in units),
                   **{f"negative_{kind}": totals[kind] for kind in KIND_LABELS},
                   "thin_components": totals["thin"]},
        "units": units,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 재산죄 RuleIR 법리 검토 요청",
        "",
        f"단위 {len(units)} / 규칙 {sum(item['rules'] for item in units):,}개가 계약·Scallop 런타임을 "
        "통과했습니다. 규칙은 카드에서 기계적으로 조립되므로 규칙을 한 줄씩 보실 필요는 없습니다. "
        "**부정·예외 카드 138장의 역할 지정**만 확인해 주시면 됩니다 — 그것이 규칙 구조를 정합니다.",
        "",
        "## 역할 넷",
        "",
        "| 역할 | 뜻 | 장수 |",
        "|---|---|---:|",
        f"| `bar` | 요건 결여·배제 — 충족되면 성립을 막는다 | {totals['bar']} |",
        f"| `waiver` | 요건 불요 — 성립을 막지 않고 면제만 기록 | {totals['waiver']} |",
        f"| `boundary` | 이 죄가 아니라 다른 죄로 — 후속 죄명 명시 | {totals['boundary']} |",
        f"| `component` | 요건 인정 경로 — 구성요건 단계에 든다 | {totals['component']} |",
        "",
        "## 이 표가 왜 중요한가",
        "",
        "처음에 이 역할을 명제 문언 정규식으로 판정했는데 잘못이었습니다. 그러면 법리 판단이 문자열 "
        "매칭으로 결정되고 그 결과가 그대로 Scallop 규칙에 박힙니다. 실제로 두 가지가 터졌습니다.",
        "",
        "**① 요건불요 카드가 성립 저지로 배선돼 결론이 뒤집혔습니다.** "
        "`art323_sec1_1.no_unlawful_appropriation_intent`(\"권리행사방해죄 성립에는 불법영득의사가 "
        "요구되지 않는다\")가 저지 사유가 되어, 그 카드가 충족되면 오히려 불성립이 됐습니다.",
        "",
        "**② 후속 죄명에 \"폭행\"·\"협박\"이 잡혔습니다.** \"폭행·협박으로 재물을 탈취\"의 폭행은 "
        "행위 수단인데 죄명으로 읽혔습니다.",
        "",
        "그래서 정규식을 걷어내고 **138장을 전수 판독해 카드마다 역할과 근거를 적었습니다**"
        "(`data/rulegen/property/rule_ir_card_roles.json`). 사기 조립기의 `BAR_CARD_IDS`가 손으로 "
        "열거된 목록이었던 것과 같은 자리입니다. 조립기는 이 표에 없는 카드를 만나면 멈춥니다.",
        "",
        "아래에서 **역할이 틀린 카드만** 지적해 주시면 됩니다.",
        "",
        "---",
        "",
    ]
    for kind, label in (("boundary", "경계획정"), ("waiver", "요건 불요"),
                        ("component", "요건 인정 경로"), ("bar", "저지")):
        cards = [(item, card) for item in units for card in item["classified"].get(kind, [])]
        lines += [f"## `{kind}` — {label} ({len(cards)}장)", ""]
        if kind == "boundary":
            lines += ["이 죄의 불성립과 함께 **후속 죄명**을 규칙 인수로 배출합니다"
                      "(`<unit>_refers_to_crime`). 같은 단위 안의 유형 전환(강도→준강도, "
                      "특수절도→야간주거침입절도)은 다른 죄가 아니므로 여기 넣지 않고 `bar`로 "
                      "두었습니다.", ""]
        elif kind == "waiver":
            lines += ["성립을 막지 않고 `<unit>_requirement_waived`로 무엇이 면제되는지만 "
                      "기록합니다.", ""]
        elif kind == "component":
            lines += ["부정·예외 극성이지만 실제로는 요건을 **인정하는** 경로라 구성요건 단계에 "
                      "넣었습니다.", ""]
        for item, card in cards:
            head = f"- `{card['id']}` ({item['unit']})"
            if card["refers_to"]:
                head += f" → **{card['refers_to']}**"
            lines += [head, f"  - {card['proposition']}", f"  - 근거: {card['rationale']}"]
        lines += ["", "**수정:** ", "", "---", ""]

    lines += ["## 얇은 component — 인정 경로가 1~2장", "",
              f"구성요건 단계 **{totals['thin']}개**가 카드 1~2장으로만 인정됩니다. 그 단계의 판단이 "
              "사실상 카드 하나에 걸린다는 뜻이라, 카드가 부족한 것인지 그 단계 자체가 얇은 것인지 "
              "확인이 필요합니다.", "",
              "| 단위 | 단계 | 카드 |", "|---|---|---:|"]
    for item in units:
        for component in item["components"]:
            if component["thin"]:
                lines.append(f"| `{item['unit']}` | {component['level']} "
                             f"{component['label']} | {len(component['cards'])} |")
    lines += ["", "**수정:** ", "", "---", "", "## 참고 — 단위별 구조", ""]
    for item in units:
        lines += [f"### {item['label']} (`{item['unit']}`)", "",
                  f"카드 {item['cards']} / 술어 {item['predicates']} / 규칙 {item['rules']}", "",
                  "| 단계 | 카드 | 대표 명제 |", "|---|---:|---|"]
        for component in item["components"]:
            head = component["cards"][0]["proposition"][:60] if component["cards"] else "—"
            lines.append(f"| {component['level']} {component['label']} | "
                         f"{len(component['cards'])} | {head}… |")
        counts = {kind: len(cards) for kind, cards in item["classified"].items() if cards}
        if counts:
            lines += ["", "역할 분포: "
                      + " / ".join(f"{kind} {count}" for kind, count in counts.items())]
        if item["aggravation"]:
            lines += ["", "가중 플래그: "
                      + " / ".join(f"`{kind}` {len(ids)}장"
                                   for kind, ids in item["aggravation"].items())]
        lines += [""]

    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"단위 {len(units)} / 저지 {totals['bar']} / 경계획정 {totals['boundary']} "
          f"/ 요건불요 {totals['waiver']} / 인정경로 {totals['component']} "
          f"/ 얇은 단계 {totals['thin']}")
    print(f"  → {OUT_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
