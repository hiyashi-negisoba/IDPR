"""벌크 검토서를 **사람이 읽을 수 있는 마크다운**으로 생성 (API 0회).

JSON 큐는 검수자에게 부적합했다(줄바꿈 없음, 카드 내용 없음, 지적 21%가 영어,
무엇을 결정하는지 불명확). 이 스크립트는 같은 데이터를 검수자 관점으로 다시 낸다.

설계 원칙
  - **기본은 권고 수용, 예외만 표시.** 452건을 일일이 판정하지 않는다. 훑으면서
    "이건 아니다" 싶은 것만 표시하면 나머지는 critic 권고대로 처리된다.
  - **결정의 결과를 먼저 보여준다.** 그 카드가 Scallop 규칙이 되는지(=성립/불성립
    결론에 영향) 아니면 RAG 문맥일 뿐인지를 항목마다 명시한다.
  - **카드 실제 내용을 붙인다.** 명제 + 출처 원문 인용. 지적만 보고는 판단 불가.
  - **한국어 구조 문장을 앞에 둔다.** 원 지적이 영어여도 무엇을 묻는지는 한국어로.
  - 영향 큰 것(실행 core) 먼저.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DS = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
OUT = PROJECT_ROOT / "data/rulegen/property"

FORM_KO = {
    "deterministic_rule": "결정론 규칙",
    "standard_input": "모델 판단 입력",
    "policy_variant": "학설 선택지",
    "context_only": "RAG 문맥",
}
IMPACT = {
    "deterministic_rule": ("**실행 core** — Scallop 규칙이 되어 성립/불성립 결론에 직접 영향", 0),
    "standard_input": ("**실행 core** — 모델 판단 입력으로 결론에 직접 영향", 0),
    "policy_variant": ("학설 선택지 — 어느 규칙을 쓸지 결정", 1),
    "context_only": ("RAG 문맥 — 결론에 유입되지 않음", 2),
}
# 지적 유형 → 검수자에게 묻는 것(한국어). 원 지적이 영어여도 이 문장이 앞에 온다.
ASK = {
    "overgeneralization": "이 카드가 **출처보다 넓게 일반화**했다는 지적입니다. 판례의 구체적 사실관계 제한을 떼고 일반 법리처럼 썼는지 봐주세요.",
    "source_scope": "이 카드가 **출처 범위를 벗어났다**는 지적입니다.",
    "source_entailment": "**출처가 이 명제를 지지하지 않는다**는 지적입니다.",
    "rule_mismatch": "카드 명제와 출처 규범이 **어긋난다**는 지적입니다.",
    "formalization_error": "이 카드의 **극성·규범종류·형식화 분류가 틀렸다**는 지적입니다.",
    "missing_variant": "**경쟁 견해가 빠졌다**는 지적입니다.",
    "collapsed_variant": "**서로 다른 견해를 한 카드에 뭉갰다**는 지적입니다.",
    "authority_mismatch": "출처가 판례를 인용하므로 **권위 표시를 올려야 한다**는 지적입니다(판례 인덱스 대조 필요).",
}


def load_cards() -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for p in DS.glob("art*/*/norm_cards/*.json"):
        art = p.parts[-4]
        out[(art, p.stem)] = json.loads(p.read_text(encoding="utf-8")).get("cards", [])
    return out


def resolve(cards: list[dict[str, Any]], part: int, target_path: str | None):
    tp = (target_path or "").replace("/", ".")
    m = re.search(r"cards[\.\[](\d+)", tp)
    if not m:
        return None
    seg = cards[(part - 1) * 50: part * 50]
    i = int(m.group(1))
    return seg[i] if i < len(seg) else None


def quote_of(card: dict[str, Any]) -> str:
    qs = [r.get("quote", "") for r in card.get("source_refs", []) if r.get("quote")]
    return qs[0][:300] if qs else "(인용 없음)"


def main() -> None:
    cards_by = load_cards()
    items: list[dict[str, Any]] = []

    # finding 축
    for sp in sorted(DS.glob("art*/*/sol/*.json")):
        art = sp.parts[-4]
        m = re.match(r".+\.normcards\.(.+)\.part(\d+)\.critic\.json$", sp.name)
        if not m:
            continue
        mod, part = m.group(1), int(m.group(2))
        cards = cards_by.get((art, mod), [])
        for f in json.loads(sp.read_text(encoding="utf-8")).get("findings", []):
            ftype = f.get("type", "other")
            if ftype not in ASK:
                continue
            card = resolve(cards, part, f.get("target_path"))
            if card is None:
                continue          # 카드 대상 아님 → 에이전트 처리분
            form = card.get("formalization", "")
            impact, rank = IMPACT.get(form, ("분류 미상", 3))
            items.append({
                "rank": rank, "article": art, "module": mod, "type": ftype,
                "card_id": card.get("id"), "form": form, "polarity": card.get("polarity"),
                "impact": impact,
                "proposition": card.get("proposition", ""),
                "quote": quote_of(card),
                "ask": ASK[ftype],
                "finding": (f.get("message") or "").strip(),
                "reco": (f.get("recommended_action") or "").strip(),
                "severity": f.get("severity"),
            })

    items.sort(key=lambda x: (x["rank"], x["article"], x["module"]))
    high = [x for x in items if x["rank"] == 0]
    rest = [x for x in items if x["rank"] > 0]

    def render(rows: list[dict[str, Any]], title: str, intro: str) -> str:
        g: list[str] = [f"# {title}\n", intro, ""]
        g.append("## 이 문서를 보는 법\n")
        g.append("- **기본은 아래 '권고'대로 처리됩니다.** 전부 판정하실 필요 없습니다.")
        g.append("- 훑으시다가 **권고가 틀렸다 싶은 것만** `결정:` 칸에 적어주세요.")
        g.append("- 비워두시면 = 권고 수용. `반대` 또는 이유를 적으시면 = 제가 다시 봅니다.")
        g.append("- 각 항목의 **영향**이 그 카드가 결론에 흘러드는지 알려줍니다.\n")
        cur = None
        for i, x in enumerate(rows, 1):
            k = (x["article"], x["module"])
            if k != cur:
                cur = k
                g.append(f"\n---\n\n## {x['article']} / {x['module']}\n")
            g.append(f"### {i}. `{x['card_id']}`\n")
            g.append(f"- **영향**: {x['impact']}")
            g.append(f"- **분류**: {FORM_KO.get(x['form'], x['form'])} · 극성 {x['polarity']}\n")
            g.append(f"**카드 명제**\n> {x['proposition']}\n")
            g.append(f"**출처 원문**\n> {x['quote']}\n")
            g.append(f"**무엇을 봐주셔야 하나**\n{x['ask']}\n")
            g.append(f"<details><summary>원 지적 (critic, 심각도 {x['severity']})</summary>\n")
            g.append(f"\n{x['finding']}\n\n</details>\n")
            g.append(f"**권고 (기본값)**\n{x['reco'] or '(없음)'}\n")
            g.append("**결정:** \n")
        return "\n".join(g) + "\n"

    (OUT / "REVIEW_1_결론에_영향.md").write_text(render(
        high, "재산죄 카드 검토 ① — 결론에 영향 있는 것",
        f"총 {len(high)}건. 이 카드들은 **Scallop 규칙 또는 모델 판단 입력**이 되어 "
        "성립/불성립 결론에 직접 흘러듭니다. 여기만 보셔도 됩니다."), encoding="utf-8")
    (OUT / "REVIEW_2_영향_적음.md").write_text(render(
        rest, "재산죄 카드 검토 ② — 영향 적은 것",
        f"총 {len(rest)}건. 학설 선택지이거나 RAG 문맥으로만 쓰이는 카드입니다. "
        "시간 남으실 때 보시면 됩니다."), encoding="utf-8")

    print(f"① 결론 영향 {len(high)}건 → REVIEW_1_결론에_영향.md")
    print(f"② 영향 적음 {len(rest)}건 → REVIEW_2_영향_적음.md")


if __name__ == "__main__":
    main()
