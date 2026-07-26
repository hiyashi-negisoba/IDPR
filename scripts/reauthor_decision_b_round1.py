"""1차 검토 반영분 재작성 — 사용자 문장 전사(轉寫)를 걷어낸다.

사용자 지시(2026-07-23): "내껄 따라하라는게 아니라 인간 전문가의 해석은 그렇다고."
코멘트는 **법률 전문가의 해석 입력**이지 승인할 문안이 아니다. 앞판은 제안 문장을 그대로
옮겨 적었고, 그 결과 방금 세운 규칙(질의문은 순수 사실만)을 스스로 어긴 곳이 남았다.
15번 "허가를 받아 **유효한 거래였다**"의 유효성은 법적 평가다.

23번은 카드 명제 자체를 전문가 해석대로 재작성한다. 주석서 원문은 "종래 **사용상태**"라고
쓰지만, 전문가 해석은 선행 점유취득 범죄의 불가벌적 사후행위 문제로 읽는다. 출처범위
critic이 걸 수 있는 변경이므로 원장에 근거를 남긴다.

API 0회.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

# 사용자 문장을 전사했던 것 → 사실 진술로 다시 씀
REAUTHOR: dict[str, tuple[str, str, str]] = {
    "art355_sec5_3.land_transaction_permit_no_contract_effect": (
        "그 토지매매는 토지거래허가구역 내의 거래로서 관할 관청의 허가를 받았다.",
        "not_satisfied",
        "앞판은 '허가를 받아 유효한 거래였다'로 옮겼는데 유효성은 법적 평가다. 허가 취득이라는 "
        "사실만 남긴다."),
    "art355_sec6.embezzlement_status_offense": (
        "행위자는 그 재물을 맡아 보관하고 있던 사람이다.",
        "not_satisfied",
        "'위탁관계에 의하여'는 이 카드가 판단할 요건이라 뺀다(사용자 지적). 보관 사실만 묻는다."),
    "art357_sec3_4.no_acquisition_intent": (
        "재물을 수수한 사람은 이를 자기 것으로 가질 의사로 받았다.",
        "not_satisfied",
        "'불법영득의사'는 법적 개념어다. 취득 의사라는 사실로 묻는다."),
    "art357_sec4.giver_view_justification": (
        "증재자는 자신이 한 청탁이 부정한 청탁이라는 점을 인식하고 있었다.",
        "not_satisfied",
        "전문가 해석(증재자 측 사실인식)을 문장으로 다시 씀."),
    "art366_sec3_2.movement_no_objective_use_value": (
        "소유자가 우연히 놓아두거나 방치해 둔 물건을 행위자가 다른 곳으로 옮겼다.",
        "satisfied",
        "옮긴 사실만 묻는다. '즉시 본래 용법대로 쓸 수 없게 되었는지'는 카드가 판단한다."),
}

# 카드 명제 자체 재작성 (전문가 해석 채택)
CARD_REWRITE = {
    "art366_sec3_2.document_removal_without_owner_intent": {
        "new_proposition":
            "문서가 이미 소유자의 의사에 반하여 행위자의 점유로 넘어간 뒤에 그 문서의 상태를 "
            "변경하거나 제거한 행위는 선행 점유취득 범죄의 불가벌적 사후행위이므로 별도로 "
            "문서손괴죄를 구성하지 않는다.",
        "new_query":
            "그 문서는 소유자의 의사에 반하여 이미 행위자의 점유로 넘어가 있었고, 행위자는 그 뒤에 "
            "문서의 상태를 변경하거나 제거하였다.",
        "status": "satisfied",
        "basis": "사용자(법률 검수자) 해석 — 결정B 1차 23번",
        "risk": "주석서 원문은 '종래 **사용상태**가 소유자 의사에 반하거나 무관한' 경우로 읽히고, "
                "짝 카드(소유자 의사에 따라 게시된 문서를 떼어내면 손괴)와 대칭이다. 이 재작성은 "
                "원문 문언을 벗어나므로 출처범위 critic이 지적할 수 있다. 전문가 해석 채택으로 기록.",
    },
}


def main() -> None:
    p = PROP / "property_negative_query_drafts_v3.json"
    src = json.loads(p.read_text(encoding="utf-8"))
    ledger = []

    for it in src["items"]:
        cid = it["card_id"]
        if cid in REAUTHOR:
            q, st, why = REAUTHOR[cid]
            ledger.append({"card_id": cid, "kind": "질의문 재작성",
                           "from": it["neural_query"], "to": q, "why": why})
            it["neural_query"], it["card_status_when_query_satisfied"] = q, st
            it["revision"] = why
        if cid in CARD_REWRITE:
            r = CARD_REWRITE[cid]
            ledger.append({"card_id": cid, "kind": "카드 명제 재작성",
                           "from": it["proposition"], "to": r["new_proposition"],
                           "why": r["basis"], "risk": r["risk"]})
            it["prev_proposition"] = it["proposition"]
            it["proposition"] = r["new_proposition"]
            it["neural_query"] = r["new_query"]
            it["card_status_when_query_satisfied"] = r["status"]
            it["revision"] = f"{r['basis']} — 카드 명제까지 재작성"
            it["source_scope_risk"] = r["risk"]

    src["version"] = "3.1.0"
    src["reauthored_at"] = datetime.now(timezone.utc).isoformat()
    p.write_text(json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (PROP / "결정B_1차반영_원장.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "principle": "사용자 코멘트는 법률 전문가의 해석 입력이며 승인할 문안이 아니다. "
                     "에이전트가 해석을 반영해 문장을 직접 작성한다.",
        "entries": ledger,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"재작성 {len(ledger)}건 (질의문 {sum(1 for e in ledger if e['kind']=='질의문 재작성')} + "
          f"카드명제 {sum(1 for e in ledger if e['kind']=='카드 명제 재작성')})")
    for e in ledger:
        print(f"  · {e['card_id']} [{e['kind']}]")


if __name__ == "__main__":
    main()
