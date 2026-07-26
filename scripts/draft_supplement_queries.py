"""보강 3조문 부정형·예외형 카드의 긍정형 질의문 초안 — 결정 B-3 (승인용).

보강분 core 59장 중 부정형·예외형이면서 아직 승인된 질의문이 없는 카드는 19장이다.
standard_input 13장은 질의문을 쓰고, deterministic_rule 6장은 질의를 면제한다.

작성 규칙은 결정 B·B-2와 같다. 사실만 묻고 법적 평가는 넣지 않으며, 카드가 부정형이므로 질의는
긍정형으로 쓴다. 부정형 질의로 이중부정을 만들지 않고, 그렇게 하면 어색해지는 경우에는 방향을
뒤집어 `not_satisfied`로 적는다.

결정 B-2에서 받은 지적을 반영해 **발동 시 결론**을 함께 적는다. 제350조 준강도-강도 경계 카드에서
"카드 발동"이 공갈죄 배제인지 강도죄 성립인지 모호했던 문제다.

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
APPROVED = ("property_negative_query_final.json", "property_exception_query_final.json")
OUT_JSON = PROP / "supplement_query_drafts.json"
OUT_DOC = PROP / "결정B3_보강조문_질의문승인.md"

SATISFIED = "satisfied"
NOT_SATISFIED = "not_satisfied"

# card_id → (질의문, 발동방향, 발동 시 결론, 작성 근거)
QUERIES: dict[str, tuple[str, str, str, str]] = {
    "art330_sec3.restaurant_permitted_entry_no_intrusion": (
        "피고인은 일반인의 출입이 허용된 영업장에 영업주의 승낙을 받아 통상적인 출입방법으로 "
        "들어갔다.",
        SATISFIED,
        "침입행위가 아니므로 야간주거침입절도죄가 아니라 절도죄에 그친다",
        "'범죄 목적을 알았다면 승낙하지 않았을 것'이라는 가정적 평가는 빼고, 출입 경로와 승낙이라는 "
        "사실만 묻는다."),
    "art332_sec1_1.different_offense_types": (
        "피고인의 전력과 이번 범행은 절도·강도·사기 등 서로 다른 유형의 범죄로 이루어져 있다.",
        SATISFIED,
        "절도의 상습성이 인정되지 않아 상습절도죄가 성립하지 않는다",
        "동종성 판단의 기초가 되는 범죄 유형 구성이라는 사실을 묻는다."),
    "art332_sec1_2.habituality-not-repetition-alone": (
        "이번 범행은 동기·수단·범행 간격 등에 비추어 피고인의 절도 습벽이 발현된 것으로 볼 "
        "사정이 있다.",
        NOT_SATISFIED,
        "반복 사실만으로는 상습성이 인정되지 않는다",
        "'반복만으로는 부족하다'를 그대로 물으면 이중부정이 된다. 습벽 발현 사정의 존재를 물어 "
        "방향을 뒤집었다."),
    "art332_sec1_2.incidental-or-economic-theft-exception": (
        "피고인의 절도행위는 모두 우발적인 동기나 급박한 경제적 사정에서 비롯된 것이다.",
        SATISFIED,
        "절도 습성의 발현이 아니어서 상습범으로 보지 않는다",
        "동기라는 사실을 묻는다. 습성 발현 여부의 평가는 카드가 한다."),
    "art333_sec2_3.diversion_or_insult_violence_no_robbery": (
        "그 폭행·협박은 피해자의 주의를 다른 데로 돌리기 위한 것이었거나, 재물을 가져간 뒤 모욕 "
        "또는 적개심을 표시하기 위한 것이었다.",
        SATISFIED,
        "강도죄가 아니라 폭행죄 또는 협박죄와 절도죄가 성립한다",
        "폭행·협박의 목적이라는 사실을 묻는다."),
    "art333_sec2_3.lesser_threat_extortion": (
        "그 폭행·협박은 피해자에게 두려움을 일으키는 정도였고, 피해자는 스스로 결정하여 재물을 "
        "건넸다.",
        SATISFIED,
        "강도죄가 아니라 공갈죄가 성립한다",
        "강도·공갈의 경계를 폭행의 정도와 교부의 임의성이라는 두 사실로 물었다."),
    "art333_sec2_3.subjective_intent_insufficient": (
        "그 폭행·협박의 정도는 같은 상황에 놓인 일반인의 반항을 억압할 만한 것이었다.",
        NOT_SATISFIED,
        "범인에게 반항억압의 의사가 있었더라도 강도죄가 성립하지 않는다",
        "'객관적으로 이르지 못한 경우'를 그대로 물으면 부정형이 된다. 객관적 정도를 물어 방향을 "
        "뒤집었다. core의 객관설 카드와 같은 사실을 쓴다."),
    "art333_sec3_1.real_estate_as_robbery_property_negative": (
        "강취의 대상은 부동산이다.",
        SATISFIED,
        "부동산은 도취죄의 재물이 아니므로 재물 강취로는 강도죄가 성립하지 않는다",
        "객체가 무엇인지만 묻는다. 부동산에 관한 권리를 취득한 경우는 같은 절의 재산상 이익 카드가 "
        "받는다."),
    "art333_sec3_2.post_taking_assault_no_robbery": (
        "그 구타는 재물의 탈환을 막거나 체포를 면하거나 증거를 없애기 위한 것이었다.",
        NOT_SATISFIED,
        "탈취 후의 구타만으로는 강도죄가 성립하지 않는다",
        "'관련 없다면'을 그대로 물으면 부정형이 된다. 구타의 목적을 물어 방향을 뒤집었다."),
    "art333_sec3_2.voluntary_delivery_attempt": (
        "피해자가 재물을 건넨 것은 반항이 억압되어서가 아니라 귀찮음이나 연민 때문이었다.",
        SATISFIED,
        "강취의 인과관계가 없어 강도미수에 그친다",
        "교부의 원인이라는 사실을 묻는다. 제350조 공갈 쪽 같은 축 카드와 문형을 맞췄다."),
    "art333_sec3_3.unconsciousness_prior_force_no_causation": (
        "피고인은 재물을 탈취할 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 "
        "빠지게 하였고, 그 후에 비로소 재물을 가져갈 마음을 먹었다.",
        SATISFIED,
        "선행행위와 탈취 사이에 인과관계가 없어 강도죄가 아니라 절도죄가 성립한다"
        "(살해 후 취거는 살인죄와 절도죄의 경합)",
        "선행행위의 목적과 범의 발생 시점이라는 두 사실을 묻는다. 강간 사안 카드"
        "(`rape_force_subsequent_taking_precedent`)와 갈리는 지점은 피해자의 의식 유무이므로 "
        "'심신상실 상태'를 질의에 남겼다."),
    "art333_sec6.no_attempt_insufficient_violence_intimidation": (
        "피고인이 개시한 폭행·협박은 사회통념상 피해자의 반항을 억압할 만한 정도였다.",
        NOT_SATISFIED,
        "강도죄의 실행 착수가 인정되지 않는다",
        "착수 판단의 기준이 되는 폭행 정도를 물어 방향을 뒤집었다."),
    "art333_sec8.right_exercise_robbery_negative": (
        "피고인이 취득한 재산상 이익은 피고인이 피해자에 대하여 실제로 가지고 있던 권리의 범위 "
        "안에 있었다.",
        SATISFIED,
        "불법한 이익이 아니어서 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다",
        "권리의 존재와 이익의 범위라는 사실을 묻는다. 사용자 정정(대법원 소극설)을 반영한 카드다."),
}

# card_id → 질의 면제 사유 (deterministic_rule — 모델에 묻지 않는다)
WAIVERS: dict[str, str] = {
    "art333_sec2_2.incidental_incapacitation_no_robbery":
        "혼취를 어떤 목적으로 야기했는지는 같은 절의 폭행 판정 카드가 확정하고, 이 카드는 그 결과에 "
        "인과관계 규칙을 적용한다.",
    "art333_sec2_2.preexisting_incapacitation_exception":
        "혼취 상태를 누가 야기했는지는 선행 사실이고, 이 카드는 그 경우 폭행 요건에서 배제한다는 "
        "규칙이다.",
    "art333_sec3_3.completed_theft_quasi_robbery_exception":
        "절도 기수 여부와 폭행의 목적은 각각 다른 카드가 판정하고, 이 카드는 그 조합을 준강도로 "
        "돌리는 경계 규칙이다.",
    "art333_sec6.no_attempt_without_violence_intimidation_commencement":
        "폭행·협박에 착수했는지는 다른 카드가 판정하고, 이 카드는 그것이 없으면 착수를 부정하는 "
        "요건 규칙이다.",
    "art333_sec7_1.completion.no_safe_escape_requirement":
        "요건 제외 규칙이라 모델에 물을 사실이 없다(안전지역 이탈은 기수 요건이 아니다).",
    "art333_sec7_1.completion.recovery_does_not_negate":
        "탈환 사실은 사건 경과로 확정되고, 이 카드는 그것이 기수 인정에 영향을 주지 않는다는 "
        "규칙이다.",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(SETS.glob("*.json")):
        for card in read_json(path)["cards"]:
            cards[card["id"]] = card

    covered: set[str] = set()
    for name in APPROVED:
        payload = read_json(PROP / name)
        covered |= {item["card_id"] for item in payload["items"]}
        covered |= {item["card_id"] for item in payload["no_query_needed"]}

    gap = {card_id for card_id, card in cards.items()
           if card["polarity"] in ("negative", "exception") and card_id not in covered}
    drafted = set(QUERIES) | set(WAIVERS)
    if gap != drafted:
        raise SystemExit(f"초안 대상 불일치\n  누락 {sorted(gap - drafted)}\n"
                         f"  잉여 {sorted(drafted - gap)}")
    for card_id in QUERIES:
        if cards[card_id]["formalization"] != "standard_input":
            raise SystemExit(f"{card_id}는 standard_input이 아니다")
    for card_id in WAIVERS:
        if cards[card_id]["formalization"] != "deterministic_rule":
            raise SystemExit(f"{card_id}는 deterministic_rule이 아니다")

    items = [{
        "card_id": card_id,
        "article": card_id.split("_")[0].split(".")[0],
        "polarity": cards[card_id]["polarity"],
        "proposition": cards[card_id]["proposition"],
        "neural_query": query,
        "card_status_when_query_satisfied": direction,
        "conclusion_when_fired": conclusion,
        "authoring_note": note,
        "origin": "결정B3 신규(보강 3조문)",
        "human_review": {"decision": None, "approved_query": None, "notes": None},
    } for card_id, (query, direction, conclusion, note) in sorted(QUERIES.items())]

    waived = [{"card_id": card_id, "proposition": cards[card_id]["proposition"],
               "reason": reason} for card_id, reason in sorted(WAIVERS.items())]

    OUT_JSON.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "basis": "core_norm_card_sets (검토완료 core 481장, 보강 3조문 포함)",
        "counts": {"queries": len(items), "waivers": len(waived),
                   "core_total": len(cards),
                   "already_covered": len(covered & set(cards))},
        "status": "pending_user_approval",
        "items": items,
        "no_query_needed": waived,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 검토 B-3 — 보강 3조문 질의문 승인 요청",
        "",
        f"보강 3조문(제330·332·333조) 검토를 반영해 core가 **481장**이 됐습니다(재산죄 422 + 보강 59). "
        f"그중 부정형·예외형이면서 승인된 질의문이 없는 카드가 **{len(gap)}장**입니다.",
        "",
        f"- 질의문 초안 **{len(items)}건** (standard_input)",
        f"- 질의 면제 **{len(waived)}건** (deterministic_rule — 모델에 묻지 않음)",
        "",
        "결정 B-2에서 주신 지적을 반영해 **발동 시 결론**을 함께 적었습니다. "
        "제350조 카드에서 '카드 발동'이 공갈죄 배제인지 강도죄 성립인지 모호했던 문제입니다.",
        "",
        "고칠 문장은 **수정:** 뒤에 적어 주십시오. 승인 전에는 배선하지 않습니다.",
        "",
        "---",
        "",
        f"## 1부. 질의문 초안 ({len(items)}건)",
        "",
    ]
    for index, item in enumerate(items, start=1):
        fires = item["card_status_when_query_satisfied"] == SATISFIED
        direction = ("이 **카드(규칙)가 발동**합니다" if fires
                     else "이 **카드(규칙)는 발동하지 않습니다**")
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
            f"**발동 시 결론**: {item['conclusion_when_fired']}",
            "",
            f"**작성 근거**: {item['authoring_note']}",
            "",
            "**수정:** ",
            "",
        ]
    lines += ["---", "", f"## 2부. 질의 면제 ({len(waived)}건 — deterministic_rule)", "",
              "모델에 묻지 않고 규칙으로 판정하는 카드입니다. 질의가 필요하다고 보시면 번호를 "
              "적어 주십시오.", ""]
    for index, item in enumerate(waived, start=1):
        lines += [f"### {index}. `{item['card_id']}`", "",
                  f"> {item['proposition']}", "",
                  f"**면제 사유**: {item['reason']}", "", "**수정:** ", ""]
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")

    print(f"질의문 초안 {len(items)}건 / 면제 {len(waived)}건 "
          f"(core {len(cards)}장 중 부정형·예외형 미보유 {len(gap)}장)")
    print(f"  → {OUT_JSON.relative_to(ROOT)}")
    print(f"  → {OUT_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
