"""예외형(polarity=exception) core 카드의 긍정형 질의문 초안 — 결정 B-2 (승인용).

결정B는 `polarity == "negative"`만 큐에 담았다(`rebuild_decision_b.py:70`). 그런데 merge가
부정형 명제 중 **구성요건 배제 사유**를 exception으로 재분류했기 때문에, 그 카드들은 부정형
명제를 그대로 들고 있으면서도 질의문 심사를 한 번도 받지 않았다. 조립된 core 427장 기준으로
polarity가 negative/exception인 카드 127장 중 **44장에 승인된 질의문이 없다.**

  · standard_input 32장 → 질의문 필요(부정형 명제가 모델에 도달하면 안 된다)
  · deterministic_rule 12장 → 질의 불요(모델에 묻지 않고 규칙으로 판정), 사유를 남겨 면제

질의문 작성 규칙은 결정B와 같다. 사실만 묻고 법적 평가를 넣지 않는다. 카드가 부정형이므로
질의는 긍정형 사실로 쓰고, 질의가 참일 때 그 카드(규칙)가 발동하는지를 함께 적는다. 부정형
질의로 이중부정을 만들지 않는다.

승인 전에는 어디에도 배선하지 않는다. API 0회.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"
SETS = PROP / "core_norm_card_sets"
APPROVED = PROP / "property_negative_query_final.json"
OUT_JSON = PROP / "property_exception_query_drafts.json"
OUT_DOC = PROP / "결정B2_예외형질의문승인.md"

SATISFIED = "satisfied"  # 질의가 참이면 이 카드(규칙)가 발동한다
NOT_SATISFIED = "not_satisfied"  # 질의가 참이면 이 카드(규칙)는 발동하지 않는다

# card_id → (질의문, 발동방향, 작성 근거)
QUERIES: dict[str, tuple[str, str, str]] = {
    "art323_sec2_2.manifestly_no_right_possession_excluded": (
        "그 물건을 점유하고 있던 사람은 절취 등 위법한 방법으로 그 점유를 취득하였다.",
        SATISFIED,
        "'점유할 권리 없음이 외관상 명백'은 평가어라 점유 취득 경위라는 사실로 바꿨다."),
    "art323_sec2_2.nominee_owner_not_subject": (
        "그 물건은 명의신탁된 것이고 피고인은 명의신탁자이며, 대외적인 소유 명의는 "
        "명의수탁자에게 있었다.",
        SATISFIED,
        "명의신탁의 유효성 평가는 빼고 신탁 사실과 대외적 명의 귀속만 묻는다."),
    "art323_sec2_2.registered_sale_seller_not_subject": (
        "그 부동산 또는 자동차·중기·건설기계에 관하여 매수인 명의로 소유권이전등기 또는 "
        "이전등록이 마쳐졌다.",
        SATISFIED,
        "소유권유보특약의 효력은 카드가 판단한다. 등기·등록 완료라는 사실만 묻는다."),
    "art328_sec4_1.night_burglary_resident_kinship_exception": (
        "피고인은 재물의 소유자 또는 점유자와 친족관계에 있으나, 침입한 주거의 주거자와는 "
        "친족관계가 없다.",
        SATISFIED,
        "친족관계의 존부는 신분관계 사실이다. 카드는 주거자와의 친족관계가 불필요하다는 규칙."),
    "art329_sec5_2.fuel_consumption_incidental_use": (
        "차량을 일시 사용하는 과정에서 소비된 연료의 양은 그 사용에 통상 수반되는 정도를 "
        "넘지 않았다.",
        SATISFIED,
        "'특별히 많은 경우'의 반대 사실을 양(量)으로 묻는다."),
    "art329_sec5_2.use_theft_possession_not_completely_lost": (
        "피고인은 그 재물을 극히 단시간 사용한 뒤 곧 원래의 장소로 돌려놓았다.",
        SATISFIED,
        "'소지가 완전히 상실되지 않고 곧 환원될 상태'를 반환이라는 행태 사실로 바꿨다."),
    "art329_sec6.consent_no_taking": (
        "피해자는 피고인이 그 재물을 가져가는 것에 동의하였다.",
        SATISFIED,
        "승낙의 유효성 평가는 별도 카드가 맡고, 여기서는 동의 사실만 묻는다."),
    "art337_sec3.injury_result_violence_intent": (
        "피고인은 피해자에게 폭행을 가한다는 점을 인식하고 그 행위를 하였다.",
        SATISFIED,
        "결과적 가중범의 최소 요건인 폭행의 고의를 인식 사실로 묻는다."),
    "art343_sec3.abandonment_before_execution_denied": (
        "피고인은 강도의 예비 또는 음모를 마친 뒤 실행의 착수에 이르기 전에 스스로 범행을 "
        "그만두었다.",
        SATISFIED,
        "중지미수 성립 여부는 카드가 판단한다. 착수 전 자의적 포기라는 사실만 묻는다."),
    "art350_sec4_2.right_exercise_exception": (
        "피고인은 피해자에 대하여 그 금액에 관한 채권을 가지고 있었고, 요구한 금액은 그 "
        "채권액을 넘지 않았다.",
        SATISFIED,
        "'권리행사'라는 평가를 채권 존재와 요구액이라는 두 사실로 분해했다."),
    "art350_sec5_2.no_fear_attempt": (
        "피해자가 재물을 교부한 것은 피고인의 협박 때문이 아니라 동정심 등 다른 사정 "
        "때문이었다.",
        SATISFIED,
        "외포심 부존재를 교부의 원인이라는 사실로 묻는다. "
        "art350_sec7_2.completion.other_cause_disposition_attempt와 사실상 같은 조건이다."),
    "art350_sec5_3.complete_suppression_robbery": (
        "피고인의 협박 정도는 피해자의 반항을 불가능하게 하거나 억압할 정도였다.",
        SATISFIED,
        "강도·공갈의 경계를 가르는 협박의 정도는 판례가 사실인정 대상으로 삼는 항목이다."),
    "art350_sec7_2.completion.other_cause_disposition_attempt": (
        "피해자가 재물을 교부한 원인은 협박으로 생긴 두려움이 아니라 연민 등 다른 사정이었다.",
        SATISFIED,
        "기수·미수를 가르는 인과 사실을 묻는다. art350_sec5_2.no_fear_attempt와 중복 후보."),
    "art355_sec1_2.embezzlement_illegal_appropriation_exclusion": (
        "피고인은 그 재물을 일시 사용할 의사였거나 위탁자를 위한 의사로 처분하였다.",
        SATISFIED,
        "불법영득의사 부존재의 근거 사실(의사의 내용)을 긍정형으로 묻는다."),
    "art355_sec3_3.deceptive_means_no_fraud": (
        "피고인의 기망은 자신이 이미 보관하고 있던 재물을 처분하거나 그 처분을 숨기기 위한 "
        "것이었다.",
        SATISFIED,
        "'재산적 처분행위가 없다'는 부정형을 기망의 대상·목적이라는 사실로 바꿨다."),
    "art355_sec4_1.business_loss_alone_insufficient": (
        "피고인은 그 판단이 본인에게 재산상 손해를 가할 수 있음을 알면서 그 행위를 하였다.",
        NOT_SATISFIED,
        "인식 없는 손해 발생·단순 과실이라는 이중부정을 피하려 인식 존재를 물어 방향을 뒤집었다."),
    "art355_sec4_1.justified_refusal_exception": (
        "피고인은 반환을 거부할 당시 그 재물에 관하여 동시이행항변권·유치권 또는 상계할 채권을 "
        "가지고 있었다.",
        SATISFIED,
        "'정당한 이유'를 판례가 열거한 세 권리의 보유 사실로 특정했다."),
    "art355_sec4_1.later_return_intent_irrelevant": (
        "피고인은 그 금원을 사용할 당시 나중에 반환하거나 변상할 의사를 가지고 있었다.",
        SATISFIED,
        "카드는 그 사정만으로는 불법영득의사가 부정되지 않는다는 규칙이므로 사정의 존재를 묻는다."),
    "art355_sec4_1.no_breach_of_trust_without_awareness": (
        "피고인은 자신의 행위가 맡은 임무에 위배된다는 점을 인식하고 있었다.",
        NOT_SATISFIED,
        "인식 부존재를 묻지 않고 인식 존재를 물어 이중부정을 없앴다."),
    "art355_sec4_1.preoffense_setoff_only": (
        "피고인은 그 금원을 인출하기 전에 자신의 채권과 상계하는 정산을 마쳐 두었다.",
        NOT_SATISFIED,
        "카드가 유보한 '범행 전 상계정산 등 특별한 사정'의 존재를 묻는다."),
    "art355_sec4_3.organization_representative_litigation_exception": (
        "그 사건의 실질적 이해관계는 단체에 있었고 분쟁이 단체의 업무와 직접 관련되어, 단체를 "
        "위하여 소송을 수행하거나 고소에 대응할 필요가 있었다.",
        SATISFIED,
        "예외 요건 세 가지를 사실 진술로 묶었다. 지출의 적법성 평가는 카드가 한다."),
    "art355_sec5_2.individual_delegation_exception": (
        "그 계약에는 단순한 권리이전이나 담보설정을 넘어 상대방의 재산을 관리·처리해 주기로 하는 "
        "약정이 포함되어 있었다.",
        SATISFIED,
        "'신임관계를 인정할 개별 요소'를 약정 내용이라는 사실로 특정했다."),
    "art355_sec5_2.pre_sale_right_delegated_management_exception": (
        "수분양권 매도인은 매수인을 위하여 분양대금 납입이나 명의변경 등 매수인의 재산상 사무를 "
        "대행하기로 약정하였다.",
        SATISFIED,
        "위임약정 포함 여부를 대행 대상 사무로 구체화했다."),
    "art355_sec5_2.real_estate_transfer_exception": (
        "매수인은 그 부동산 매매대금 중 중도금까지 지급하였다.",
        SATISFIED,
        "판례가 타인 사무성을 인정하는 분기점인 중도금 지급 사실을 묻는다."),
    "art356_sec2_2.administrative_illegality": (
        "피고인이 반복·계속하여 행한 그 사무는 필요한 면허 또는 인가를 받지 않은 상태에서 "
        "이루어졌다.",
        SATISFIED,
        "행정절차상 불법의 존재를 묻고, 그것이 업무성을 깨뜨리지 않는다는 판단은 카드가 한다."),
    "art357_sec3_2.corporate_control_transfer_exception": (
        "그 청탁은 사회복지법인 또는 학교법인의 운영권을 넘기고 양수인 측 임원을 선임하는 데 "
        "대한 대가에 관한 것이었다.",
        SATISFIED,
        "청탁의 대상이라는 사실만 묻는다. 부정성 판단은 카드가 한다."),
    "art357_sec3_2.giver_not_necessarily_liable": (
        "증재자는 자신의 정당한 업무에 관하여 부탁하였으나, 그 부탁 내용은 수재자가 맡은 임무에 "
        "반하는 것이었다.",
        SATISFIED,
        "증재자·수재자 각각의 사정을 병렬로 묻는다. 필요적 공범 법리는 카드가 처리한다."),
    "art357_sec3_2.permitted_favor_request": (
        "피고인이 받은 부탁의 내용은 담당자의 직무권한 범위 안에서 편의를 보아 달라거나 규정이 "
        "허용하는 범위에서 선처해 달라는 것이었다.",
        SATISFIED,
        "부탁의 내용을 사실로 묻는다."),
    "art357_sec3_3.principal_not_third_party_precedent": (
        "재물 또는 재산상 이익이 귀속된 상대방은 피고인에게 그 사무처리를 위임한 본인이었다.",
        SATISFIED,
        "제3자 해당성 평가 대신 귀속 상대방이 누구인지를 묻는다."),
    "art360_sec2_2.mistaken_bank_transfer_embezzlement_holding": (
        "그 금원은 송금인의 착오로 피고인의 은행계좌에 입금된 것이다.",
        SATISFIED,
        "착오 입금 사실을 묻는다. 횡령·점유이탈물횡령의 구별은 카드가 한다."),
    "art366.special_medium_record_limited_view": (
        "손괴 대상은 컴퓨터 등 정보처리장치에 사용되기 위하여 문서 이외의 매체에 기록된 것이다.",
        SATISFIED,
        "한정해석의 기준을 기록 매체와 용도라는 사실로 묻는다."),
    "art366_sec3_2.wall_graffiti_functional_efficiency_limit": (
        "그 낙서로 건조물의 미관이 손상되어 원상회복에 상당한 비용과 노력이 필요하게 되었다.",
        SATISFIED,
        "'현저한 효용 침해'를 원상회복 부담이라는 사실로 바꿨다(판례의 인정 근거)."),
}

# card_id → 질의 면제 사유 (deterministic_rule — 모델에 묻지 않는다)
WAIVERS: dict[str, str] = {
    "art323_sec2_2.coowned_property_excluded":
        "공유 여부는 다른 카드가 확정하는 소유관계 사실이고, 이 카드는 그 결과에 규칙을 적용한다.",
    "art323_sec2_2.official_custody_exception":
        "공무소 보관명령의 존재는 기록으로 확정되는 사항이라 규칙으로 판정한다.",
    "art323_sec2_2.prohibited_gold_products_excluded":
        "금제품 해당 여부는 물건의 법적 성질 판정이라 사실 질의로 물을 것이 없다.",
    "art328_sec6_3.disabled_victim_abuse_crimes_no_application":
        "적용 제외를 시행일·죄명·피해자 지위로 판정하는 적용범위 규칙이다.",
    "art328_sec6_3.special_property_crime_no_exclusion":
        "특별법에 배제 규정이 있는지는 법령 조회 사항이라 사실 질의 대상이 아니다.",
    "art329_sec2_1.inherited_estate_not_ownerless":
        "상속재산의 국가 귀속은 민법 규정의 효과라 규칙으로 판정한다.",
    "art335_sec2.preparation_stage_exclusion":
        "절취행위 착수 여부는 다른 카드가 판단하고, 이 카드는 그 결과에 규칙을 적용한다.",
    "art335_sec2.property_interest_exclusion":
        "객체가 재물인지 재산상 이익인지는 객체 판정 카드의 결과를 받는다.",
    "art335_sec3_2.arrest_or_concealment_no_control":
        "목적이 무엇인지는 목적 판정 카드가 맡고, 이 카드는 요건 배제 규칙만 담당한다.",
    "art357_sec1_3.receipt.no_breach_or_loss_requirement":
        "요건 제외 규칙이지 사실 질문이 아니다(결정B 면제 사유와 같은 축).",
    "art357_sec3_1.subject_no_external_authority":
        "요건 제외 규칙이라 물을 사실이 없다.",
    "art360_sec2_3.reporting_noncompliance_alone":
        "법정 절차 이행 여부는 다른 카드가 확정하고, 이 카드는 그것만으로 성립하지 않는다는 규칙이다.",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(SETS.glob("*.json")):
        for card in read_json(path)["cards"]:
            cards[card["id"]] = card

    approved = read_json(APPROVED)
    covered = {item.get("card_id") for item in approved["items"]}
    covered |= {item.get("card_id") for item in approved["no_query_needed"]}

    gap = {card_id for card_id, card in cards.items()
           if card["polarity"] in ("negative", "exception") and card_id not in covered}
    drafted = set(QUERIES) | set(WAIVERS)
    if gap != drafted:
        missing, extra = sorted(gap - drafted), sorted(drafted - gap)
        raise SystemExit(f"초안 대상 불일치\n  누락 {missing}\n  잉여 {extra}")

    for card_id in QUERIES:
        if cards[card_id]["formalization"] != "standard_input":
            raise SystemExit(f"{card_id}는 standard_input이 아니다 — 질의문이 아니라 면제 대상")
    for card_id in WAIVERS:
        if cards[card_id]["formalization"] != "deterministic_rule":
            raise SystemExit(f"{card_id}는 deterministic_rule이 아니다 — 면제할 수 없다")

    items = [{
        "card_id": card_id,
        "article": card_id.split("_")[0].split(".")[0],
        "polarity": cards[card_id]["polarity"],
        "proposition": cards[card_id]["proposition"],
        "neural_query": query,
        "card_status_when_query_satisfied": direction,
        "authoring_note": note,
        "origin": "결정B2 신규(예외형 누락분)",
        "human_review": {"decision": None, "approved_query": None, "notes": None},
    } for card_id, (query, direction, note) in sorted(QUERIES.items())]

    waived = [{
        "card_id": card_id,
        "proposition": cards[card_id]["proposition"],
        "reason": reason,
    } for card_id, reason in sorted(WAIVERS.items())]

    OUT_JSON.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "basis": "core_norm_card_sets (검토완료 core 427장)",
        "gap_cause": ("결정B 큐가 polarity=='negative'만 담았고, merge가 부정형 명제 일부를 "
                      "exception으로 재분류해 심사에서 빠졌다"),
        "counts": {"queries": len(items), "waivers": len(waived),
                   "core_negative_or_exception": sum(
                       1 for card in cards.values()
                       if card["polarity"] in ("negative", "exception"))},
        "status": "pending_user_approval",
        "items": items,
        "no_query_needed": waived,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 검토 B-2 — 예외형 카드 질의문 승인 요청",
        "",
        f"결정B는 `polarity == \"negative\"`만 심사 큐에 담았습니다. 그런데 merge 단계가 부정형 "
        f"명제 중 **구성요건 배제 사유**를 `exception`으로 재분류했기 때문에, 그 카드들은 부정형 "
        f"명제를 그대로 들고 질의문 심사를 건너뛰었습니다. 검토완료 core 427장을 RuleIR 입력 "
        f"형식으로 조립하면서 드러났습니다.",
        "",
        f"- core 중 negative/exception: **{sum(1 for c in cards.values() if c['polarity'] in ('negative', 'exception'))}장**",
        f"- 그중 승인된 질의문 보유: {len(covered & set(cards))}장",
        f"- **누락 {len(gap)}장** → 질의문 초안 {len(items)}건(standard_input) + 질의 면제 "
        f"{len(waived)}건(deterministic_rule)",
        "",
        "질의문은 결정B와 같은 규칙으로 썼습니다. 사실만 묻고 법적 평가는 넣지 않으며, 카드가 "
        "부정형이므로 질의는 긍정형으로 쓰고 발동 방향을 함께 적었습니다.",
        "",
        "고칠 문장은 **수정:** 뒤에 적어 주시면 됩니다. 승인 전에는 배선하지 않습니다.",
        "",
        "---",
        "",
        "## 1부. 질의문 초안 (32건)",
        "",
    ]
    for index, item in enumerate(items, start=1):
        direction = ("이 **카드(규칙)가 발동**합니다" if item["card_status_when_query_satisfied"]
                     == SATISFIED else "이 **카드(규칙)는 발동하지 않습니다**")
        lines += [
            f"### {index}. `{item['card_id']}` ({item['polarity']})",
            "",
            "**카드 원문**",
            f"> {item['proposition']}",
            "",
            "**질의문**",
            f"> {item['neural_query']}",
            "",
            f"**극성**: 질의가 참이면 → {direction}",
            "",
            f"**작성 근거**: {item['authoring_note']}",
            "",
            "**수정:** ",
            "",
        ]
    lines += ["---", "", "## 2부. 질의 면제 (12건 — deterministic_rule)", "",
              "모델에 묻지 않고 규칙으로 판정하는 카드입니다. 면제가 아니라 질의가 필요하다고 "
              "보시면 그 번호를 적어 주십시오.", ""]
    for index, item in enumerate(waived, start=1):
        lines += [
            f"### {index}. `{item['card_id']}`",
            "",
            f"> {item['proposition']}",
            "",
            f"**면제 사유**: {item['reason']}",
            "",
            "**수정:** ",
            "",
        ]
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")

    print(f"질의문 초안 {len(items)}건 / 면제 {len(waived)}건")
    print(f"  → {OUT_JSON.relative_to(ROOT)}")
    print(f"  → {OUT_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
