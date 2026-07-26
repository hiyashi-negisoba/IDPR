"""재산죄 core 확정 — 승격 카드 잔여 재작성 + 파서가 놓친 사용자 취지 반영.

파서 오류 하나를 바로잡는다. `art355_sec5_2.real_estate_sale_other_affairs`에 대한 답변은

  "판례는 (1)인데 학계는 (2)를 강력주장함. 그냥그렇다고 우리는 판례를 따라가긴하니까.."

였는데 파서가 `picked: ["1","2"]`로 읽어 다수의견과 반대의견을 **둘 다** 실무규칙으로 올렸다.
두 카드는 서로 모순된다(매도인이 타인 사무처리자인가 아닌가). 취지는 명확하다 — 실무는 판례를
따르므로 (1)이 규칙이고 (2)는 학설 소개다.

나머지는 승격 카드 중 학설 어법이 남은 것들의 재작성이다.

API 0회.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

# 파서가 취지를 놓친 것 — 원문 답변을 근거로 정정
PARSER_FIX = {
    "art355_sec5_2.real_estate_sale_dissent": {
        "action": "demote",
        "raw_answer": "판례는 (1)인데 학계는 (2)를 강력주장함. 그냥그렇다고 우리는 판례를 따라가긴하니까..",
        "reason": "파서가 ['1','2'] 둘 다 선택으로 읽었으나 취지는 '실무는 판례를 따른다'이다. "
                  "(1) 다수의견이 실무규칙이고 (2) 반대의견은 학설 소개로 내린다. 두 카드를 함께 "
                  "core에 두면 매도인의 타인 사무처리자 지위에 관해 서로 모순되는 규칙이 된다.",
    },
}

# 학설 어법 제거 — 선택된 견해를 규칙 문장으로
REWRITE = {
    "art323_sec3.conditional_intent_sufficient":
        "권리행사방해죄의 고의는 미필적 고의로도 충분하다.",
    "art355_sec3_3.completion_expression_theory":
        "횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.",
    "art357_sec3_5.attempt_majority":
        "부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 "
        "배임수증재죄의 미수가 성립한다.",
    "art366_sec3_2.emotional_use_majority_position":
        "감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 "
        "해당하여 재물손괴죄가 성립한다.",
}

# 실체 요건이 아니어서 내리는 것
DEMOTE = {
    "art355_sec4_3.fake_capital_academic_invalidity":
        "상법상 가장납입의 사법적 효력(회사 설립무효 원인)에 관한 진술로, 횡령죄 구성요건이 아니다. "
        "형사 판단에 쓰이는 것은 같은 절의 '가장납입으로 자본이 실질적으로 증가하지 않으면 "
        "불법영득의사를 인정하기 어렵다' 쪽이며 그 카드는 core에 남아 있다.",
}


def main() -> None:
    core = json.loads((PROP / "property_core_set_final_v6.json").read_text(encoding="utf-8"))
    rows = {r["card_id"]: r for r in core["rows"]}
    stats, ledger = Counter(), []

    for cid, fix in PARSER_FIX.items():
        r = rows.get(cid)
        if r and r["final_role"] not in ("context_only", "deferred_track"):
            r.update(final_role="context_only", demoted_at="parser_fix", reason=fix["reason"])
            stats["parser_fix_demoted"] += 1
            ledger.append({"card_id": cid, "kind": "parser_fix", **fix})

    for cid, why in DEMOTE.items():
        r = rows.get(cid)
        if r and r["final_role"] not in ("context_only", "deferred_track"):
            r.update(final_role="context_only", demoted_at="finalize", reason=why)
            stats["demoted"] += 1
            ledger.append({"card_id": cid, "kind": "demote", "reason": why})

    for cid, prop in REWRITE.items():
        r = rows.get(cid)
        if r and r["final_role"] not in ("context_only", "deferred_track"):
            ledger.append({"card_id": cid, "kind": "rewrite",
                           "prev": r["proposition"], "new": prop})
            r["prev_proposition"] = r["proposition"]
            r["proposition"] = prop
            r["rewrite_reason"] = ("학설 어법 제거 — 선택된 견해를 실무규칙으로 진술")
            r.pop("rewrite_pending", None)
            stats["rewritten"] += 1

    left = [r for r in rows.values() if r.get("rewrite_pending")
            and r["final_role"] not in ("context_only", "deferred_track")]
    kept = [r for r in rows.values() if r["final_role"] not in ("context_only", "deferred_track")]
    core["rows"] = list(rows.values())
    core["version"] = "7.0.0"
    core["counts"]["core_final"] = len(kept)
    core["status"] = "reviewed_core_set_candidate"
    (PROP / "property_core_set_final_v7.json").write_text(
        json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PROP / "core_finalize_ledger.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stats": dict(stats), "entries": ledger,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print(f"  학설 어법 잔존: {len(left)}장")
    print(f"\n재산죄 core {len(kept)}장 (이전 429)")
    print(f"  그중 학설선택 승격분 {sum(1 for r in kept if r.get('promoted_from_variant'))}장")
    print(f"  극성 {Counter(r['polarity'] for r in kept).most_common()}")


if __name__ == "__main__":
    main()
