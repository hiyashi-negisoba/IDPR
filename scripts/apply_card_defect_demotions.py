"""카드 결함 감사 결과 반영 — 재산죄 core 3차 강등 (사용자 승인 2026-07-23).

`audit_card_defects.py`가 찾은 축을 확정 적용한다. 사용자 결정: S1·S2·W2에 더해
**G(판단지침형)·P(증명·소송법)도 강등**한다.

강등 축
  S1 죄수·다른죄 관계 절     다른 죄명의 성부는 이 조문의 요건이 아니다
  S2 공범관계 절            형법총칙 영역(총칙 코퍼스 확보 전까지 future work)
  W2 알맹이 없는 학설 서술    적용할 요건이 없고 긍정형 전환 시 명제가 뒤집힌다
  G  판단지침형             '곧바로 인정할 수 없다' — 모델에게 물을 사실이 없다
  P  증명·소송법             사실인정 방법론이지 실체 요건이 아니다

W1(래퍼 벗기기)은 강등이 아니라 명제 재작성이다. 실질 규칙이 안에 있다.
D(근사중복)는 쌍 중 하나를 남기고 병합한다 — 어느 쪽을 남길지는 문언이 더 완전한 쪽.

사기 core 88장의 G축 1장(`deception.fraud.standard.loan-lender-anticipated-risk`)은
**여기서 건드리지 않는다**. 승인된 RuleIR(`fraud_full_rule_ir_post_sol_human_decision.json`,
status=approved_for_scallop_runtime)의 4개 규칙에 단독 근거로 배선돼 있어 강등하면 RuleIR
재생성이 따른다. 별도 결정 사항으로 보고한다.

API 0회.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"
AUDIT = PROP / "card_defect_audit.json"
FINAL = PROP / "property_core_set_final.json"
OUT = PROP / "property_core_set_final_v2.json"

AXIS_REASON = {
    "S1_죄수·다른죄_절": "죄수·다른 죄와의 관계 절 — 다른 죄명의 성부는 이 조문의 요건이 아님",
    "S2_공범관계_절": "공범관계 절 — 형법총칙 영역(총칙 코퍼스 필요, future work)",
    "W2_강등": "알맹이 없는 학설 서술 — 적용 요건이 없고 긍정형 전환 시 명제가 뒤집힘",
    "G_판단지침형": "판단지침형 — 해석 지침이지 사실에 적용할 규칙이 아님(사용자 결정)",
    "P_증명·소송법": "증명·소송법 — 사실인정 방법론이지 실체 요건이 아님(사용자 결정)",
}
DEMOTE_AXES = list(AXIS_REASON)

# 근사중복: 남길 카드 → 흡수할 카드 (문언이 더 완전한 쪽을 남긴다)
DUP_MERGE = {
    "art355_sec4_1.justified_refusal_exception": "art355_sec3_3.justified_refusal_exception",
    "art357_sec4.giving_offense_definition": "art357_sec1_1.giving_offense_definition",
    "art355_sec4_2.restricted_funds_off_purpose_embezzlement": "art355_sec4_1.restricted_purpose_funds",
    "art355_sec4_2.owner_benefit_disposition_no_appropriation": "art355_sec4_1.owner_benefit_exception",
}


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    final = json.loads(FINAL.read_text(encoding="utf-8"))

    demote: dict[str, str] = {}
    for axis in DEMOTE_AXES:
        for cid in audit["property"]["by_axis"].get(axis, []):
            demote.setdefault(cid, AXIS_REASON[axis])
    for absorbed, keeper in ((v, k) for k, v in DUP_MERGE.items()):
        demote.setdefault(absorbed, f"근사중복 병합 — {keeper}가 같은 취지를 더 완전하게 담음")

    unwrap = audit["unwrap_rewrites"]
    rows, rewritten = [], 0
    for r in final["rows"]:
        cid = r["card_id"]
        if r["final_role"] != "context_only" and cid in demote:
            r = {**r, "final_role": "context_only", "demoted_at": "defect_audit",
                 "reason": demote[cid]}
        elif cid in unwrap and r["final_role"] != "context_only":
            r = {**r, "prev_proposition": r["proposition"], "proposition": unwrap[cid],
                 "rewrite_reason": "메타 래퍼 제거 — 실질 규칙만 남김"}
            rewritten += 1
        rows.append(r)

    core = [r for r in rows if r["final_role"] != "context_only"]
    before = final["counts"]["core_final"]
    print(f"core {before} → {len(core)}장 (강등 {before - len(core)}, 명제 재작성 {rewritten})")
    print("\n강등 사유별")
    for k, v in Counter(demote.values()).most_common():
        print(f"  {v:3d}  {k}")
    print("\n조문별 최종 core")
    for a, n in sorted(Counter(r["article"] for r in core).items(), key=lambda x: -x[1]):
        print(f"  {a:8s} {n:4d}")
    print("\n극성", Counter(r["polarity"] for r in core).most_common())

    OUT.write_text(json.dumps({
        "version": "2.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": "property_core_set_final.json",
        "method": "1차 표지 자동강등 + 2차 전수 판독 + 3차 결함감사(절 출처·학설·지침·증명·중복)",
        "counts": {"merge_core": final["counts"]["merge_core"],
                   "demoted_auto": final["counts"]["demoted_auto"],
                   "demoted_manual": final["counts"]["demoted_manual"],
                   "demoted_defect_audit": before - len(core),
                   "core_final": len(core), "propositions_rewritten": rewritten},
        "defect_demotions": demote,
        "duplicate_merges": DUP_MERGE,
        "per_article_core": dict(sorted(Counter(r["article"] for r in core).items())),
        "rows": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
