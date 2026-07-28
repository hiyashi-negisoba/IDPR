"""P2(비재산 형법각칙) RuleIR 8-Level 층위 분류 및 페이즈 맵 생성기 (API 0회).

P1(재산죄)에서 검증된 L0~L7 층위 구조를 P2 31개 조문 1,280개 Core 규범 카드 전체에 적용한다.

레벨 정의 (범죄 성립 판단의 단계적 제어 흐름):
  L0 적격·객체·신분  (사람의 시기·종기, 공문서/사문서 객체, 공무원/친족 신분 등)
  L1 실행행위       (살해·상해·방화·허위작성·폭행협박·위증·도피 등)
  L2 인과·결과귀속  (결과적 가중범 및 별도 제2행위 개입 인과관계)
  L3 주관적 요건    (살인 고의, 행사 목적, 도피 목적, 위계 인식 등)
  L4 범죄단계       (간접정범 실행 착수, 독립연소 기수, 미수)
  L5 가중·특수유형  (존속살해, 현주건조물방화, 특수강간, 업무상과실 등)
  L6 위법성·책임    (정당행위, 안락사 위법성 조각, 자기비호 책임 조각)
  L7 처벌·소추      (친족간 특례 제151조 제2항, 제155조 제4항 등)
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REM = PROJECT_ROOT / "data/rulegen/p2/remediated"
OUT_JSON = PROJECT_ROOT / "data/rulegen/p2/p2_rule_ir_phase_map.json"
OUT_MD = PROJECT_ROOT / "docs/research/p2_rule_ir_phase_map.md"

LEVELS: dict[str, str] = {
    "L0": "적격·객체·신분",
    "L1": "실행행위",
    "L2": "인과·결과귀속",
    "L3": "주관적 요건",
    "L4": "범죄단계",
    "L5": "가중·특수유형",
    "L6": "위법성·책임",
    "L7": "처벌·소추",
}


def assign_p2_level(card: dict[str, Any]) -> tuple[str, str]:
    cid = card.get("id", "")
    prop = card.get("proposition", "")
    
    if "relative_exemption" in cid or "친족" in prop or "소추" in prop or "친족간" in prop:
        return "L7", "처벌·소추 사유 (친족간 특례/소추조건)"
    if "justification" in cid or "legality" in cid or "위법성" in prop or "정당행위" in prop or "안락사" in prop:
        return "L6", "위법성·책임 조각 사유"
    if "parricide" in cid or "arson_death" in cid or "special_" in cid or "aggravat" in cid or "존속" in prop or "현주건조물" in prop or "특수" in prop or "치사" in prop:
        return "L5", "가중·특수 구성요건 및 결과적 가중"
    if "attempt" in cid or "completion" in cid or "onset" in cid or "착수" in prop or "기수" in prop or "미수" in prop:
        return "L4", "범죄 수행 단계 (착수/기수/미수)"
    if "intent" in cid or "awareness" in cid or "purpose" in cid or "고의" in prop or "인식" in prop or "목적" in prop:
        return "L3", "주관적 구성요건 (고의/목적/인식)"
    if "causal" in cid or "liability" in cid or "인과" in prop or "귀속" in prop:
        return "L2", "인과관계 및 결과귀속"
    if "object" in cid or "scope" in cid or "status" in cid or "subject" in cid or "객체" in prop or "시작" in prop or "신분" in prop or "사람" in prop:
        return "L0", "행위 객체 및 주체 신분 요건"
    return "L1", "실체적 실행행위 요건"


def main() -> None:
    cards_by_level: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cards_by_art_level: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    stats = Counter()

    for jf in sorted(REM.glob("*/*.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        art = jf.parts[-2]
        for c in data.get("cards", []):
            if c.get("formalization") in ("deterministic_rule", "standard_input"):
                lvl, reason = assign_p2_level(c)
                c["assigned_level"] = lvl
                c["level_reason"] = reason
                cards_by_level[lvl].append(c)
                cards_by_art_level[art][lvl].append(c)
                stats[lvl] += 1

    total_core = sum(stats.values())
    
    # Save JSON Phase Map
    out_payload = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_core_cards": total_core,
        "level_counts": dict(stats),
        "level_definitions": LEVELS,
        "articles": {
            art: {lvl: [c["id"] for c in cs] for lvl, cs in lvls.items()}
            for art, lvls in cards_by_art_level.items()
        }
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Generate Markdown Summary Artifact
    md = [
        "# P2(비재산 형법각칙) RuleIR 8-Level 층위 구조 설계서",
        "",
        f"총 **{total_core}개 Core 규범 규칙**을 범죄 성립 판단 8단계 레벨(L0~L7) 구조로 분류 완결하였습니다.",
        "",
        "## 1. 레벨별 규칙 분포 및 정의",
        "",
        "| 레벨 | 층위 명칭 | 카드 수 | 주요 대상 법리 예시 |",
        "| --- | --- | --- | --- |"
    ]

    for lvl, name in LEVELS.items():
        cnt = stats[lvl]
        sample = cards_by_level[lvl][0]["proposition"] if cards_by_level[lvl] else "-"
        md.append(f"| **{lvl}** | {name} | {cnt}장 | {sample[:40]}... |")

    md.extend([
        "",
        "## 2. 조문별 층위 구조 배치 현황",
        "",
        "| 조문 (Issue Tag) | L0 (객체/신분) | L1 (실행행위) | L2 (인과) | L3 (주관) | L4 (단계) | L5 (가중) | L6 (위법성) | L7 (처벌) | 합계 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    ])

    for art, lvls in sorted(cards_by_art_level.items()):
        l_cnts = [len(lvls.get(l, [])) for l in LEVELS]
        tot = sum(l_cnts)
        md.append(f"| `{art}` | {l_cnts[0]} | {l_cnts[1]} | {l_cnts[2]} | {l_cnts[3]} | {l_cnts[4]} | {l_cnts[5]} | {l_cnts[6]} | {l_cnts[7]} | **{tot}** |")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"✅ P2 Phase Map 생성 완료: {total_core}장 -> {OUT_JSON}")
    print(f"✅ 설계서 산출 완료: {OUT_MD}")


if __name__ == "__main__":
    main()
