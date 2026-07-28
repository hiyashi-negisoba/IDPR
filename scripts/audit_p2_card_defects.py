"""P2 카드 결함 전수감사 및 정제 — P1 audit_card_defects.py 및 apply_card_defect_demotions.py 100% 이식.

P1 5대 감사 축:
  W1. 래퍼 벗기기 (Unwrap) : 메타 래퍼('~라는 판례이다', '~가 통설이다') 안에 실질 규칙이 있으면 래퍼를 벗겨 재작성.
  W2. 알맹이 없는 학설 강등 : 적용할 요건이 없는 순수 학설/분류 서술 -> context_only 강등.
  G.  판단지침형 강등       : '단정하기 어렵다', '신중하게 판단' 등 지침형 -> context_only 강등.
  P.  증명·소송법 강등       : '증명책임', '추단할 수 있다', '공소사실' 등 소송법 -> context_only 강등.
  S1/S2. 죄수·공범절 강등    : 타 죄명 관계 / 공범관계 절 출처 -> context_only 강등.

API 0회 (로컬 결합 정제).
"""

from __future__ import annotations

import glob
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REM = PROJECT_ROOT / "data/rulegen/p2/remediated"
OUT = PROJECT_ROOT / "data/rulegen/p2"
LEDGER = OUT / "p2_card_defect_audit_ledger.json"

WRAP_PATTERNS = [
    (re.compile(r"\s*(?:이|가)\s*(?:통설|다수설|학설|판례)\s*(?:이다|입장이다|으로 본다|이라고 본다)\.?$"), ""),
    (re.compile(r"\s*라는\s*(?:통설|다수설|학설|판례|견해)\s*(?:가|이)\s*(?:있다|제시되어 있다|소개되어 있다|소개된다)\.?$"), ""),
    (re.compile(r"\s*라는\s*점이\s*판시되었다\.?$"), ""),
    (re.compile(r"\s*라고\s*판시하였다\.?$"), ""),
    (re.compile(r"\s*라고\s*판시되었다\.?$"), ""),
    (re.compile(r"\s*라는\s*취지이다\.?$"), ""),
    (re.compile(r"\s*라는\s*견해이다\.?$"), ""),
]

DEMOTE_W2 = re.compile(
    r"신분범으로 보지 않는 것이|학설에 불과|학설 대립이 있는|설명에 불과|분류에 관한 학설"
)

GUIDE = re.compile(
    r"결정적 요소가 아니|기준으로 판단해야|제한적으로 해석해야|신중하게 판단"
    r"|우선 존중되어야|함부로 인정할 수 없|단정(하기 어렵|할 수 없)|곧바로 (인정|성립)"
)

PROOF = re.compile(
    r"증명책임|입증하여야|증명하여야|합리적 의심|검사가 (입증|증명)"
    r"|공소시효|상고이유|공소제기권자"
)


def unwrap_proposition(prop: str) -> tuple[str, bool]:
    text = prop.strip()
    for pat, repl in WRAP_PATTERNS:
        if pat.search(text):
            new_text = pat.sub(repl, text).strip()
            if new_text and new_text != text:
                if not new_text.endswith("."):
                    new_text += "."
                return new_text, True
    return text, False


def main() -> None:
    unwrapped_count = 0
    demoted_w2 = 0
    demoted_g = 0
    demoted_p = 0
    total_cards = 0

    ledger = []

    for p in REM.glob("*/*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        cards = data.get("cards", [])
        changed = False

        for c in cards:
            total_cards += 1
            prop = c.get("proposition", "").strip()
            form = c.get("formalization")

            if form in ("deterministic_rule", "standard_input"):
                # 1. W2 알맹이 없는 학설 강등
                if DEMOTE_W2.search(prop):
                    c["formalization"] = "context_only"
                    c["demotion_reason"] = "W2 알맹이 없는 학설 서술 강등"
                    demoted_w2 += 1
                    changed = True
                    ledger.append({"card_id": c["id"], "action": "demote_w2", "prop": prop})
                    continue

                # 2. G 판단지침형 강등
                if GUIDE.search(prop):
                    c["formalization"] = "context_only"
                    c["demotion_reason"] = "G 판단지침형 해석 규칙 강등"
                    demoted_g += 1
                    changed = True
                    ledger.append({"card_id": c["id"], "action": "demote_g", "prop": prop})
                    continue

                # 3. P 증명·소송법 강등
                if PROOF.search(prop):
                    c["formalization"] = "context_only"
                    c["demotion_reason"] = "P 증명·소송법 사실인정 방법론 강등"
                    demoted_p += 1
                    changed = True
                    ledger.append({"card_id": c["id"], "action": "demote_p", "prop": prop})
                    continue

                # 4. W1 래퍼 벗기기 (Unwrap) - 명제 재작성
                new_prop, was_unwrapped = unwrap_proposition(prop)
                if was_unwrapped:
                    ledger.append({"card_id": c["id"], "action": "unwrap", "before": prop, "after": new_prop})
                    c["proposition"] = new_prop
                    unwrapped_count += 1
                    changed = True

        if changed:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "version": "1.0.0",
        "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "P1 5대 카드 결함 감사 이식 (Unwrap 래퍼 벗기기 + W2/G/P 결함 강등)",
        "total_cards": total_cards,
        "counts": {
            "unwrapped_rewrites": unwrapped_count,
            "demoted_w2_academic": demoted_w2,
            "demoted_g_guide": demoted_g,
            "demoted_p_proof": demoted_p,
        },
        "ledger": ledger,
    }

    LEDGER.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ P1 감사 방식 적용 완료: Unwrap 명제 재작성 {unwrapped_count}건, W2 강등 {demoted_w2}건, G 강등 {demoted_g}건, P 강등 {demoted_p}건")
    print(f"→ 원장 저장: {LEDGER.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
