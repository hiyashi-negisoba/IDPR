"""결정 B 1차 검토(1~25번) 반영 + 전수 결함수정 → v3 재발행.

사용자 지적의 핵심은 개별 문장이 아니라 **결함 하나**였다. 질의문이 사실이 아니라
**카드 자신이 내리는 법적 평가**를 모델에게 되묻고 있었다.

  카드: 동산매매 매도인은 타인 사무처리자가 아니므로 배임죄가 성립하지 않는다
  질의(구): 동산 매도인이 타인의 사무를 처리하는 자의 지위에 있었다   ← 카드의 결론을 되물음
  질의(신): 행위자는 동산 매매의 매도인이고 인도 없이 제3자에게 처분하였다  ← 사실

1~25번에서 6건을 지적받았고, 같은 패턴을 99건 전수 스캔해 13건을 더 찾아 함께 고쳤다.

극성 라벨도 고쳤다. 구판은 `not_satisfied`를 "불성립"으로 적었는데 이것이 **카드 불발동**인지
**범죄 불성립**인지 읽히지 않았다(사용자 지적 25번). 실제 의미는 카드 발동 여부이며 범죄 성립
여부와는 무관하다 — 사기 앵커에서 질의가 참이면 카드는 미발동이지만 범죄는 오히려 성립 방향이다.

API 0회.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

# --- 1차 검토(1~25) 사용자 기입 원문 ------------------------------------
COMMENTS: dict[int, str] = {
    4: "지금 질의문 초안이 성립한다는건 불법영득의사가 인정되지 않아 무죄라는거지? 1번 2번 신규랑은 "
       "방향이 다른데 이건 괜찮은거임? 그러니까 수정된 명제들끼리의 방향은?",
    5: "이건 강도치사죄에서 판단하는거지 거기 위에서만? 모든 규칙에 대한게 아니지?",
    12: "동산 매도인은 타인의 사무처리하는자가 애초에 아니므로, 배임죄가 성립하지 않는다는 취지야. "
        "그러니까 그냥 두사람 관계가 동산 매도/매수인의 관계인지만 봐도 되는거지. 지금은 좀 잘못된듯.",
    13: "이것도 위에랑 마찬가지로 그런 면에서 어색함. 애초에 주권발행 전 주식양도인이 제3자 대항요건을 "
        "갖추어줄 채무를 가지고 있었지만 그것은 본인의 사무이지 타인의 사무처리하는자 라는 요건에 "
        "해당하지 않아서 배임이 아니라는 취지이기 때문에 적절하지 않은 사실진술이다. "
        "지금 이러한 조건걸 기반의 처리를 잘 못하는거같네.",
    14: "이것도 마찬가지임",
    15: "토지거래허가구역 내의 토지매매에 있어서, 토지매매가 관청의 허가를 받아 유효한 거래였다. "
        "가 적절하지 않을까? 지금 대체로 좀 불안불안하네",
    16: "행위자는 타인의 재물을 보관하는 자이다. 정도가 정확할듯 위탁관계라는건 굳이 긁어부스럼일듯",
    18: "취득한 자에게 불법영득의사가 있었다. 가 적절하지",
    19: "증재자의 입장에서 이것이 부정한 청탁이라는 사실인식이 있었다.",
    23: "이것도 좀 애매한데, 지금 카드원문에서 말하는건 이미 행위자 손에 들어온 이 문서자체가 소유자 "
        "의사에 반하는(절도든 강도든 ...) 형태로 점유이전이 된 경우에는 그 이후에 상태 변경 및 제거는 "
        "불가벌적 사후행위에 해당하므로 죄가 안된다는것이 요지 같아. 그런측면에서 다시 작성해야할 듯.",
    24: "이건 너무 예외적인 케이스에대한 카드같고, 부정한다면 너무 이상할거같아. 이건 그냥 '정보처리장치에 "
        "연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우에 대해서만 "
        "전자기록손괴죄가 성립한다' 가 맞을듯. 지금도 사실진술과 명제가 불일치하잖아. 질의문이라고 해서 "
        "무조건 사실진술로 만들어내는것은 이런 문제가 있다고. 내 지적을 이해하긴하는거야지금?",
    25: "이것도 좀.. 위와같은 문제가 있어. '소유자가 우연히 놓아두거나 방치한 물건을 다른곳으로 옮겨두었다' "
        "뭐 이런식으로 해야하는거 아니야? 그리고 내가 지금 이걸 검토하면서 계속 헷갈리는게 극성 표현이 "
        "질의가 참일떄 불성립이라는게 카드가 불성립이라는건지 범죄가 불성립이라는건지가 너무 헷갈리거든지금? "
        "그래서 작성을못하겠어.",
}
REVIEWED_THROUGH = 25

# --- 질의문 교체 (card_id → 새 질의, 새 status, 근거) --------------------
FIX: dict[str, tuple[str, str, str]] = {
    "art328_sec3_1.in_law_relationship_not_kinship": (
        "피고인의 딸과 피해자의 아들이 혼인하여 피고인과 피해자는 사돈지간이다.",
        "satisfied", "전수스캔: 친족 해당 여부는 이 카드가 내리는 결론 → 혼인 사실만 묻는다"),
    "art355_sec5_2.movable_sale_double_disposition": (
        "행위자는 동산 매매계약의 매도인이고, 목적물을 매수인에게 인도하지 않은 채 이를 제3자에게 처분하였다.",
        "satisfied", "사용자 12번"),
    "art355_sec5_2.pre_certificate_stock_transfer": (
        "행위자는 주권발행 전 주식의 양도인이고, 양수인을 위한 제3자 대항요건을 갖추어 주지 않은 채 "
        "그 주식을 타인에게 처분하였다.", "satisfied", "사용자 13번"),
    "art355_sec5_2.registered_movable_sale_disposition": (
        "행위자는 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인이고, 소유권이전등록을 마치지 "
        "않은 채 그 목적물을 제3자에게 처분하였다.", "satisfied", "사용자 14번"),
    "art355_sec5_3.land_transaction_permit_no_contract_effect": (
        "토지거래허가구역 내의 토지매매에서 그 매매는 관청의 허가를 받아 유효한 거래였다.",
        "not_satisfied", "사용자 15번 (제안 문장 채택)"),
    "art355_sec6.embezzlement_status_offense": (
        "행위자는 타인의 재물을 보관하는 자이다.", "not_satisfied", "사용자 16번 (제안 문장 채택)"),
    "art357_sec3_4.no_acquisition_intent": (
        "재물을 수수한 자에게 불법영득의 의사가 있었다.", "not_satisfied", "사용자 18번 (제안 문장 채택)"),
    "art357_sec4.giver_view_justification": (
        "증재자의 입장에서 이것이 부정한 청탁이라는 사실인식이 있었다.",
        "not_satisfied", "사용자 19번 (제안 문장 채택)"),
    "art366_sec3_2.document_removal_without_owner_intent": (
        "그 문서의 종래 사용상태는 소유자의 의사에 따른 것이었다.",
        "not_satisfied", "사용자 23번 — 다만 카드 원문 해석 확인 필요(아래 결정사항 A)"),
    "art366_sec3_2.movement_no_objective_use_value": (
        "소유자가 우연히 놓아두거나 방치한 물건을 행위자가 다른 곳으로 옮겨 즉시 본래 용법대로 "
        "사용할 수 없게 하였다.", "satisfied", "사용자 25번 (제안 문장 채택)"),
    # --- 전수 스캔으로 추가 발견한 동일 결함 13건 ---
    "art355.embezzlement.object-excludes-property-interest": (
        "횡령의 대상이 된 것은 권리·재산상 이익이나 기업비밀·정보가 아니라 유체물 또는 "
        "관리 가능한 동력이었다.", "not_satisfied", "전수스캔"),
    "art355.embezzlement_illegal_name_trust": (
        "명의수탁자와 명의신탁자의 관계는 부동산실명법에 위반되어 무효인 명의신탁약정에 기초한 것이었다.",
        "satisfied", "전수스캔"),
    "art355_sec5_2.assigned_claim_proceeds_embezzlement": (
        "행위자는 채권을 양도한 뒤 그 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 "
        "임의로 처분하였다.", "satisfied", "전수스캔"),
    "art355_sec5_2.leasehold_transfer": (
        "행위자는 임차권을 양도한 자로서 임대인에 대한 통지 등으로 양수인의 임차인 지위를 "
        "보전할 의무를 부담하고 있었다.", "satisfied", "전수스캔"),
    "art355_sec5_2.pre_sale_right_transfer": (
        "수분양권 매도인과 매수인의 약정은 단순 매매를 넘어 매도인이 매수인의 재산상 사무 처리를 "
        "대행하는 위임약정까지 포함하는 것이었다.", "not_satisfied", "전수스캔"),
    "art357_sec3_1.no_status_at_request": (
        "행위자는 부정한 청탁을 받을 당시 이미 그 사무를 담당하고 있었다.", "not_satisfied", "전수스캔"),
    "art357_sec3_2.self_rights_protection_not_improper": (
        "그 청탁은 행위자 자신의 권리를 확보하기 위한 것이었다.", "satisfied", "전수스캔"),
    "art357_sec4.giving_to_business_handler": (
        "재물을 교부받은 상대방은 그 임무에 해당하는 사무를 실제로 담당하고 있던 사람이었다.",
        "not_satisfied", "전수스캔"),
    "art366.corpse_exclusion": (
        "손괴의 대상이 된 물건은 사체 또는 해부용 사체였다.", "satisfied", "전수스캔"),
}

# 카드 문언 자체를 긍정형으로 재작성해야 하는 후보 (질의문 손질로는 해결 안 됨)
CARD_REWRITE = ["art366_sec3_2.electronic_record_power_cutoff_exception"]

POL = {
    "satisfied": "이 **카드(규칙)가 발동**합니다 — 카드의 조건이 충족됩니다",
    "not_satisfied": "이 **카드(규칙)가 발동하지 않습니다** — 카드의 조건이 충족되지 않습니다",
}


def main() -> None:
    src = json.loads((PROP / "property_negative_query_drafts_v2.json").read_text(encoding="utf-8"))
    items = src["items"]

    # 1) 사용자 응답 영구 기록
    resp = {"version": "1.0.0", "round": 1, "reviewed_through": REVIEWED_THROUGH,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "note": "결정B_질의문승인_v2.md 1~25번. 공란 = 승인(문서 규칙). 기입 12건은 원문 그대로 보존.",
            "approved_blank": [n for n in range(1, REVIEWED_THROUGH + 1) if n not in COMMENTS],
            "items": [{"n": n, "card_id": items[n - 1]["card_id"], "comment": c}
                      for n, c in sorted(COMMENTS.items())]}
    (PROP / "결정B_사용자응답_1차.json").write_text(
        json.dumps(resp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2) 질의문 교체
    applied = 0
    for it in items:
        if it["card_id"] in FIX:
            q, st, why = FIX[it["card_id"]]
            it["prev_neural_query"] = it["neural_query"]
            it["prev_status"] = it["card_status_when_query_satisfied"]
            it["neural_query"], it["card_status_when_query_satisfied"] = q, st
            it["revision"] = why
            applied += 1
        it["round1_reviewed"] = items.index(it) + 1 <= REVIEWED_THROUGH

    src["version"] = "3.0.0"
    src["counts"]["질의문_수정"] = applied
    src["card_rewrite_candidates"] = CARD_REWRITE
    (PROP / "property_negative_query_drafts_v3.json").write_text(
        json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 3) v3 문서 — 26번부터 + 1~25 중 수정된 것 재확인
    rest = [(n, it) for n, it in enumerate(items, 1) if n > REVIEWED_THROUGH]
    recheck = [(n, it) for n, it in enumerate(items, 1)
               if n <= REVIEWED_THROUGH and "revision" in it]

    g = ["# 검토 B (3판) — 26번부터", "",
         f"1~25번은 받았습니다. 공란 {len(resp['approved_blank'])}건은 승인 처리했고, "
         f"기입하신 {len(COMMENTS)}건은 `결정B_사용자응답_1차.json`에 원문 그대로 보관했습니다.", "",
         "## 먼저 — 극성 표시를 고쳤습니다 (25번 지적)", "",
         "구판의 `불성립`은 **카드 불발동**인지 **범죄 불성립**인지 읽히지 않았습니다. "
         "실제 의미는 **카드(규칙)가 발동하는가**이고, **범죄 성립 여부와는 무관**합니다. "
         "범죄 성립은 Scallop이 카드들을 종합해 계산하며 이 표시가 관여하지 않습니다.", "",
         "예를 들어 사기 앵커에서는 질의가 참이면 카드는 **미발동**이지만 범죄는 오히려 성립 방향입니다. "
         "그래서 앞으로는 `카드 발동` / `카드 미발동`으로만 적습니다.", "",
         f"## 그리고 — 같은 결함 {applied}건을 일괄 수정했습니다", "",
         "12·13·14·19·23·25번에서 지적하신 것은 개별 문장 문제가 아니라 **결함 하나**였습니다. "
         "질의가 사실이 아니라 **카드 자신이 내리는 법적 평가**를 모델에게 되묻고 있었습니다. "
         "99건 전수를 스캔해 26번 이후에서 같은 것 13건을 더 찾아 함께 고쳤습니다.", "",
         "---", ""]

    if recheck:
        g += [f"## A. 1~25번 중 수정한 것 — 재확인 {len(recheck)}건", ""]
        for n, it in recheck:
            g += [f"### R{n}. `{it['card_id']}`", "",
                  f"**카드 원문**", f"> {it['proposition']}", "",
                  f"**구 질의문** (폐기)", f"> ~~{it['prev_neural_query']}~~", "",
                  f"**새 질의문**", f"> {it['neural_query']}", "",
                  f"**극성**: 질의가 참이면 → {POL[it['card_status_when_query_satisfied']]}", "",
                  f"*근거: {it['revision']}*", "", "**수정:** ", ""]
        g += ["---", ""]

    g += [f"## B. 26번부터 — {len(rest)}건", "",
          "- 맞으면 비워두시면 승인입니다.", "- 틀리면 `수정:` 뒤에 고쳐 적어주세요.",
          "- 🔧 표시는 이번에 제가 위 결함으로 고친 것입니다.", ""]
    for n, it in rest:
        tags = []
        if it["double_negative"]:
            tags.append("⚠️이중부정")
        if it["origin"] == "신규":
            tags.append("🆕신규")
        if "revision" in it:
            tags.append("🔧수정됨")
        g += [f"### {n}. `{it['card_id']}` {' '.join(tags)}", "",
              "**카드 원문 (부정형)**", f"> {it['proposition']}", ""]
        if "prev_neural_query" in it:
            g += ["**구 질의문** (폐기)", f"> ~~{it['prev_neural_query']}~~", ""]
        g += ["**질의문 초안 (긍정형)**", f"> {it['neural_query']}", "",
              f"**극성**: 질의가 참이면 → {POL[it['card_status_when_query_satisfied']]}", "",
              "**수정:** ", ""]
    (PROP / "결정B_질의문승인_v3.md").write_text("\n".join(g) + "\n", encoding="utf-8")

    print(f"사용자 응답 기록: 기입 {len(COMMENTS)}건 + 공란승인 {len(resp['approved_blank'])}건")
    print(f"질의문 수정 {applied}건 (사용자 지적 {sum(1 for v in FIX.values() if '사용자' in v[2])} "
          f"+ 전수스캔 {sum(1 for v in FIX.values() if '전수스캔' in v[2])})")
    print(f"→ 결정B_질의문승인_v3.md — 재확인 {len(recheck)}건 + 남은 {len(rest)}건")
    print(f"카드 재작성 후보: {CARD_REWRITE}")


if __name__ == "__main__":
    main()
