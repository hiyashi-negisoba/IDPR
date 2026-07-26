"""재산죄 10단위 — 죄명별 성립요건 조건식 정리 (API 0회).

component 재분해(절도 소유/점유, 배임 고의/불법이득의사, 강도 재물강취/이득강취 트랙,
횡령 보관자지위/타인소유, 권리행사방해 자기소유/타인점유 등)를 마친 뒤, 각 단위의 최종
`elements_satisfied`·`established` 논리를 사람이 읽는 불리언 조건식으로 옮긴다. 사용자가
마지막에 이 문서 하나로 전체 구조를 검토할 수 있게 하는 것이 목적이라 규칙을 한 줄씩
옮기지 않고 component 단위로만 요약한다.
"""

from __future__ import annotations

import sys
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
    UNIT_TRACKS,
    UNITS,
    UnitBuilder,
    read_json,
)

PROP = ROOT / "data/rulegen/property"
OUT_DOC = PROP / "RuleIR_죄종별_조건식.md"


def component_label(level: str) -> str:
    return LEVEL_COMPONENTS[level][0]


def formula_for(unit: str, builder: "UnitBuilder") -> str:
    tracks = UNIT_TRACKS.get(unit, {})
    track_levels = {level for levels in tracks.values() for level in levels}
    active = builder.active_components()
    shared = [level for level in active if level not in track_levels]
    shared_names = " ∧ ".join(component_label(level) for level in shared) or "(공유 component 없음)"
    if not tracks:
        return f"{unit}_elements_satisfied = {shared_names}"
    branches = []
    for track_name, levels in tracks.items():
        track_active = [level for level in levels if level in active]
        track_names = " ∧ ".join(component_label(level) for level in track_active)
        branches.append(f"[{shared_names} ∧ {track_names}]  ← '{track_name}' 트랙")
    joined = "\n           OR ".join(branches)
    return f"{unit}_elements_satisfied =\n           {joined}"


def main() -> None:
    manifest = read_json(UNIT_MANIFEST)
    phase_rows = read_json(PHASE_MAP)["rows"]
    lines = [
        "# 재산죄 10단위 — 죄종별 성립요건 조건식",
        "",
        "component 재분해를 마친 뒤의 최종 구조다. `established`는 모든 단위에서 공통이다:",
        "",
        "```",
        "<unit>_established =",
        "    <unit>_elements_satisfied",
        "    ∧ case_assessment_complete",
        "    ∧ ¬<unit>_has_negative   (bar 카드 충족 또는 필수요건 명시적 not_satisfied)",
        "    ∧ ¬<unit>_has_conflict   (같은 쟁점에 satisfied·not_satisfied 동시 증명,",
        "                              또는 대안 트랙 두 개가 동시에 충족되는 경우)",
        "```",
        "",
        "아래는 단위마다 달라지는 `elements_satisfied`(component AND/OR 구조)와",
        "bar·waiver·boundary·가중 플래그 개수다. component 이름 옆 숫자는 그 요건을",
        "인정하는 카드(대안적 인정경로) 개수 — 그 안은 전부 OR다.",
        "",
    ]

    for entry in manifest["units"]:
        unit = entry["issue_tag"]
        if unit in DEFERRED_UNITS:
            continue
        card_set = read_json(UNITS / f"{unit}.json")
        builder = UnitBuilder(unit, card_set, phase_rows)
        rule_ir = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")

        lines += [f"## {entry['label']} (`{unit}`, {', '.join(entry['articles'])})", ""]
        lines += ["```", formula_for(unit, builder), "```", ""]

        lines += ["| component | 인정경로 카드 수 |", "|---|---:|"]
        for level in builder.active_components():
            members = [card for card in builder.cards_at(level)
                       if not builder.negative_kind(card)]
            lines.append(f"| {component_label(level)} | {len(members)} |")
        lines.append("")

        bars = len(builder.cards_of_kind("bar"))
        waivers = len(builder.cards_of_kind("waiver"))
        boundaries = len(builder.cards_of_kind("boundary"))
        aggravation = builder.aggravation_kinds()
        counts = [f"bar {bars}", f"waiver {waivers}", f"boundary {boundaries}"]
        if aggravation:
            counts.append("가중 " + "·".join(f"{kind}({len(cards)})"
                                            for kind, cards in aggravation.items()))
        lines.append("역할 분포: " + " / ".join(counts))
        lines += ["", f"규칙 {len(rule_ir['rules'])}개 / 술어 {len(rule_ir['predicates'])}개", "",
                  "---", ""]

    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"→ {OUT_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
