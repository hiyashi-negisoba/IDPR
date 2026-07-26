"""core scope 최종 확정 — 자동 표지 강등(1차) + 에이전트 전수 판독(2차)을 합친다.

1차 `audit_core_scope.py`는 사기 정답 646장으로 검증된 표지만 발화시킨다. 정밀도 97.8%
대신 재현율 48%라 놓친 강등이 남는다. 2차는 그 잔존분 598장을 전수 판독한 결과이며
`core_scope_pass2_decisions.json`에 카드 단위로 기록돼 있다.

판독 기준은 사기와 같다. 핵심 물음 하나다 — **사건 사실만 주면 적용되는 일반 규칙인가,
아니면 특정 사안의 결론인가.** 후자는 RAG 문맥으로 내린다.

주의: 사기(646장)는 죄명 하나의 주석서였고 core 88장이 남았다. 재산죄 1,112장은 조문 17개
(죄명 약 12개)이므로 총량 비교는 무의미하다. 죄명당으로 환산해서 봐야 한다.

API 0회.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"
AUDIT = PROP / "core_scope_audit.json"
PASS2 = PROP / "core_scope_pass2_decisions.json"
OUT = PROP / "property_core_set_final.json"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    pass2 = json.loads(PASS2.read_text(encoding="utf-8"))
    demoted2 = {d["card_id"]: d["reason"] for d in pass2["demotions"]}

    rows = []
    for r in audit["rows"]:
        if r["to"] == "context_only":
            stage, reason, role = "auto", r["reason"], "context_only"
        elif r["card_id"] in demoted2:
            stage, reason, role = "manual", demoted2[r["card_id"]], "context_only"
        else:
            stage, reason, role = "kept", None, r["from"]
        rows.append({**{k: r[k] for k in
                        ("article", "module", "card_id", "polarity", "proposition")},
                     "merge_role": r["from"], "final_role": role,
                     "demoted_at": stage if role == "context_only" else None,
                     "reason": reason})

    core = [r for r in rows if r["final_role"] != "context_only"]
    per_art = Counter(r["article"] for r in core)
    print(f"merge core {len(rows)}장 → 1차 자동 {audit['counts']['demoted']} + "
          f"2차 판독 {len(demoted2)} 강등 → **최종 core {len(core)}장** "
          f"({len(core)/len(rows):.1%})")
    print("\n조문별 최종 core")
    for a, n in sorted(per_art.items(), key=lambda x: -x[1]):
        print(f"  {a:8s} {n:4d}")
    print("\n2차 강등 사유")
    for k, v in Counter(demoted2.values()).most_common():
        print(f"  {v:4d}  {k}")
    print("\n최종 core 역할", Counter(r["final_role"] for r in core).most_common())
    print("최종 core 극성", Counter(r["polarity"] for r in core).most_common())

    OUT.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "1차 표지 자동강등(사기 646장 검증) + 2차 에이전트 전수 판독",
        "criteria_source": audit["criteria_source"],
        "counts": {"merge_core": len(rows),
                   "demoted_auto": audit["counts"]["demoted"],
                   "demoted_manual": len(demoted2),
                   "core_final": len(core)},
        "per_article_core": dict(sorted(per_art.items())),
        "rows": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
