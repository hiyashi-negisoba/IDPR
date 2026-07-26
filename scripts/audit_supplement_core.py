"""보강 3조문(제330·332·333조) core scope 감사 + 검토문서 생성 (API 0회).

재산죄 벌크에 쓴 축을 그대로 적용한다 — 죄수·다른죄 관계 절 / 공범·총칙 / 구체사안 /
판단지침형(G) / 증명·소송법(P) / 타법률 / 메타서술 / 근사중복. 판정은 카드 단위로 명시해
검토 가능하게 남긴다(자동 표지 regex는 재산죄에서 재현율 48%였고, 여기서는 145장 전수 판독이
더 싸다).

조문 성격상 주의할 점 둘.
  · 제332조는 조문 자체가 상습성(가중유형)을 정하므로 '상습범'이라는 낱말이 총칙 표지에 걸려도
    구성요건이다. 자동 표지를 그대로 돌리면 조문 전체가 날아간다.
  · 제333조 Ⅹ(죄수)와 Ⅸ(공범)이 94장 중 33장이다. 축 기준대로 내리되, KCL 문항이 실제로 묻는
    쟁점(상습절도-주거침입 관계, 현금카드 강취 후 인출)은 강등하지 않고 사용자 확인으로 올린다.

산출: 감사 원장 + 벌크 검토문서(학설선택·질의문·확인항목 한 문서).
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MERGE_ROOT = ROOT / ".cache/llm/runs/rulegen_downstream"
PROP = ROOT / "data/rulegen/property"
AUDIT = PROP / "supplement_core_audit.json"
REVIEW = PROP / "보강3조문_검토요청.md"
ARTICLES = ("art330", "art332", "art333")

# ── 강등 (축 → {card_id: 사유}) ──────────────────────────────────────────
DEMOTE: dict[str, dict[str, str]] = {
    "죄수·다른죄 관계": {
        "art332_sec1_1.vehicle_use_absorbed": "자동차등 불법사용의 흡수 여부는 죄수 판단이다.",
        "art332_sec4.habitual_offense.inclusive_single_offense": "포괄일죄 여부는 죄수 판단이다.",
        "art332_sec4.habitual_offense.concurrent_crimes_view": "경합범설은 죄수 학설이다.",
        "art332_sec4.habitual_theft.highest_penalty_offense":
            "죄수 판단이고 명제가 '인용문에서 이들 죄로 지칭된'이라는 메타 서술로 시작한다.",
        "art333_sec10_1.single_offense_multiple_property_single_possession": "Ⅹ 죄수 절.",
        "art333_sec10_1.multiple_robberies_multiple_victims_possession": "Ⅹ 죄수 절.",
        "art333_sec10_1.combined_taking_forcible_gain_single_robbery": "Ⅹ 죄수 절.",
        "art333_sec10_2.theft_robbery_comprehensive_single_offense": "Ⅹ 죄수 절.",
        "art333_sec10_2.theft_robbery_single_offense_limitation":
            "Ⅹ 죄수 절이고 '항상 당연히 인정되는 것은 아니다'라는 판단지침형이다.",
        "art333_sec10_4.assault_intimidation_absorption": "Ⅹ 죄수 절 — 폭행·협박의 흡수.",
        "art333_sec10_4.injury_before_robbery_intent": "Ⅹ 죄수 절 — 상해죄와의 경합.",
        "art333_sec10_4.police_assault_concurrence": "Ⅹ 죄수 절 — 공무집행방해죄와의 경합.",
        "art333_sec10_5.restraint_forcible_taking_no_separate_arrest": "Ⅹ 죄수 절 — 체포죄.",
        "art333_sec10_5.confinement_separate_concurrence": "Ⅹ 죄수 절 — 감금죄 학설.",
        "art333_sec10_5.confinement_absorbed": "Ⅹ 죄수 절 — 감금죄 학설.",
        "art333_sec10_5.confinement_not_absorbed_precedent": "Ⅹ 죄수 절 — 감금죄 판례.",
        "art333_sec10_6.post_rape_robbery_separate_concurrence":
            "Ⅹ 죄수 절이고 강도강간(제339조)은 커버 범위 밖이다.",
        "art333_sec10_6.post_forced_molestation_robbery_separate_concurrence": "Ⅹ 죄수 절.",
        "art333_sec10_6.robbery_during_rape_execution":
            "Ⅹ 죄수 절 — 강도강간죄 성립 여부는 제339조 쟁점이다.",
        "art333.payment_evasion_fraud": "Ⅹ.7 죄수 절 — 사기죄 성립 여부.",
        "art333.payment_evasion_fraud_robbery_absorption": "Ⅹ.7 죄수 절 학설.",
        "art333.payment_evasion_fraud_robbery_concurrence": "Ⅹ.7 죄수 절 학설.",
        "art333.payment_evasion_closely_connected_robbery_only": "Ⅹ.7 죄수 절 학설.",
        "art333_sec10_8.robber_principal_receiving_stolen_goods_exception":
            "Ⅹ.8 죄수 절 — 장물죄 성립 여부.",
        "art333_sec10_8.robbery_accomplice_purchase_receiving_stolen_goods": "Ⅹ.8 죄수 절.",
        "art333_sec10_9.proceeds_disposition_nonpunishable_subsequent_act":
            "Ⅹ.9 죄수 절 — 불가벌적 사후행위.",
        "art333_sec10_9.bankbook_withdrawal_fraud_new_infringement": "Ⅹ.9 죄수 절.",
        "art333_sec10_9.bankbook_fraud_real_concurrence": "Ⅹ.9 죄수 절.",
    },
    "공범·총칙": {
        "art332_sec2.recidivism_aggravation": "누범 가중은 총칙(제35조) 양형 문제다.",
        "art332_sec2.partial_conduct_recidivism_period": "누범기간 판단은 총칙 문제다.",
        "art332_sec3.nonhabitual_accomplice_general_theft": "공범과 신분(제33조) — 총칙 축.",
        "art332_sec3.nonhabitual_accomplice_habitual_theft": "공범과 신분 — 총칙 축.",
        "art332_sec3.precedent_nonhabitual_accomplice": "공범과 신분 판례 — 총칙 축.",
        "art332_sec3.habitual_accomplice_habitual_theft": "공범과 신분 — 총칙 축.",
        "art332_sec3.habitual_accomplice_general_theft": "공범과 신분 — 총칙 축.",
        "art333_sec9_2.co_conspirator_independent_act": "Ⅸ 공범 절 — 공모관계 이탈·초과실행.",
        "art333_sec9_2.theft_conspiracy_robbery_exception": "Ⅸ 공범 절 — 공모의 범위.",
        "art333_sec9_2.unforeseeable_co_offender_violence": "Ⅸ 공범 절 — 예견가능성.",
        "art333_sec9_4.aider-club-information": "Ⅸ.4 방조 — 총칙 축이고 구체사안이다.",
        "art333_sec9_4.aider-gun-provision": "Ⅸ.4 방조 — 총칙 축이다.",
    },
    "구체사안": {
        "art330_sec3.nonpermanent_tobacco_shop_building": "담배가게 구조물이라는 개별 사안 판례.",
        "art330_sec3.employee_no_intrusion": "사진관 종업원 사안 판례.",
        "art330_sec4.screen_or_door_commencement": "방충망·다세대주택 출입문 사안 판례.",
        "art330_sec4.gas_pipe_or_doorbell_no_commencement": "가스배관·초인종 사안 판례.",
        "art330_sec5.cafe-passbook-possession-completion": "카페 통장 사안 판례.",
        "art333_sec3_2.case_assault_unrelated_to_taking": "주점 도우미 이불 사안 판례.",
        "art333_sec3_3.incidental_taking_after_assault_precedent": "말다툼·시계 사안 판례.",
        "art333_sec3_3.killing_for_payment_taking_precedent":
            "택시요금·술값 사안이고 '판례는 ~로 본다'는 메타 서술이다.",
        "art333_sec5.no_illegal_appropriation_temporary_bag_taking": "손가방·속옷 반환 사안 판례.",
        "art333_sec5.illicit_intent_low_bar_tab_case": "술값 액수라는 개별 사정 판례.",
        "art333_sec5.illicit_intent_owner_like_firearm_disposition":
            "소총 교부 사안이고 군용물특수강도는 커버 범위 밖이다.",
        "art333_sec7_1.completion.road_and_home_invasion_context":
            "노상강도·주거침입강도 두 사안을 대비한 서술이고 '어려울 수 있다'로 끝난다.",
        "art333_sec8.credit_collection_robbery_injury":
            "채권회수 의뢰 사안이고 '판례가 소개되어 있다'는 메타 서술이다.",
    },
    "판단지침형(G)": {
        "art332_sec1_2.mental-disorder-not-dispositive":
            "'단정할 수 없고'라는 해석 지침이라 모델에게 물을 사실이 없다.",
        "art332_sec1_3.old_convictions_alone_insufficient":
            "'미흡할 수 있다'는 해석 지침이다.",
        "art333_sec5.illicit_intent_bar_debt_evasion_case":
            "'보기 어려운 경우가 있다'는 해석 지침이다.",
    },
    "증명·소송법(P)": {
        "art332_sec1_2.juvenile-protection-history":
            "'상습성 인정 증거에는 제한이 없다'는 증거법 진술이다.",
        "art332_sec4.res_judicata.prior_habitual_theft_conviction":
            "기판력·면소는 소송법 쟁점이다(절차 트랙 대상).",
        "art332_sec4.res_judicata.prior_basic_theft_conviction":
            "기판력 범위는 소송법 쟁점이다(절차 트랙 대상).",
    },
    "타법률": {
        "art332_sec5_1.expired_suspended_sentence_exception": "특정범죄가중처벌법 제5조의4 요건.",
        "art332_sec5_1.expunged_sentence_exception": "형의 실효 등에 관한 법률 효과.",
        "art332_sec5_2.special_act_combined_offense": "성폭력처벌법 제3조 해석.",
        "art332_sec5_2.special_act_injury_result": "성폭력처벌법 법정형.",
        "art332_sec5_2.special_act_death_result": "성폭력처벌법 법정형.",
        "art332_sec5_2.specific_violent_crime_recidivist": "특정강력범죄법 적용요건.",
        "art332_sec5_2.specific_violent_crime_recidivist_enhancement": "특정강력범죄법 누범가중.",
    },
}

# ── 근사중복 (강등하고 유지 카드를 가리킨다) ────────────────────────────
DUP_MERGE: dict[str, tuple[str, str]] = {
    "art333_sec4_2.creditor_killing_no_benefit_transfer": (
        "art338_sec2.debt_evasion_no_robbery",
        "채무면탈 목적 채권자 살해 시 이익 이전이 없다는 같은 규칙이다. 제338조 카드가 이미 core이고 "
        "결정B에서 질의문 승인까지 받았으므로 그쪽을 남긴다."),
}

# ── 사용자 확인 항목 (축은 강등이지만 KCL 문항이 그 쟁점을 묻는다) ──────
USER_CHECK: dict[str, str] = {
    "art332_sec5_1.residential_intrusion_absorption":
        "죄수 축이지만 KCL이 묻는 쟁점이다. 재산죄 검토에서 같은 축의 art329_sec8_3(주간 주거침입과 "
        "상습절도)을 core로 살리셨으므로, 짝이 되는 이 카드도 살릴지 확인이 필요하다.",
    "art332_sec5_1.unsuccessful_theft_intrusion_absorption":
        "위와 같은 축. 절도에 이르지 않고 주거침입에 그친 경우의 흡수 여부다.",
    "art333_sec10_3.home_invasion_not_absorbed":
        "죄수 축이지만 제334조 제1항(야간주거침입 특수강도)과의 경계를 정하는 규칙이라 특수강도 "
        "판정에 쓰인다.",
    "art333_sec10_2.card_robbery_atm_withdrawal_separate_theft":
        "죄수 축이지만 KCL `credit_card_crime` 태그가 현금카드 강취 후 인출을 묻는다.",
    "art333_sec7_2.completion_credit_card_false_signature":
        "매출전표 허위서명이라는 개별 사안이지만 강제이득죄 기수시기의 전형례이고 "
        "`credit_card_crime` 태그와 맞물린다.",
}

# ── 학설선택 (그룹) ────────────────────────────────────────────────────
DOCTRINE_GROUPS: dict[str, dict[str, Any]] = {
    "art330.night_timing": {
        "label": "제330조 — 야간의 기준시점",
        "question": "침입·절취 중 어느 행위가 야간이어야 하는가.",
        "options": {
            "art330_sec1.variant.timing_entry_standard":
                "침입기준설 — 야간 침입이면 절취가 주간이어도 성립 (다수설·판례)",
            "art330_sec1.variant.timing_theft_standard":
                "절도기준설 — 절도행위 시가 야간이어야 함",
            "art330_sec1.variant.timing_theft_standard_daytime_theft_exclusion":
                "절도기준설의 귀결 — 야간 침입·주간 절취는 주거침입죄와 절도죄",
            "art330_sec1.variant.timing_both_acts_night":
                "양행위설 — 침입과 절취가 모두 야간이어야 함",
        },
        "recommend": ["art330_sec1.variant.timing_entry_standard"],
        "why": "주석서가 다수설이자 판례 입장으로 소개한다. 나머지는 학설 소개로 내린다.",
    },
    "art330.night_meaning": {
        "label": "제330조 — 야간의 의미",
        "question": "야간을 일몰~일출로 객관적으로 볼 것인가, 심리적 야간성을 따질 것인가.",
        "options": {
            "art330_sec2.nighttime.objective": "일몰 후부터 일출 전까지 (통설·판례)",
            "art330_sec2.nighttime.psychological_exception":
                "심리학적 해석 — 심리적으로 야간이 아니면 불성립",
        },
        "recommend": ["art330_sec2.nighttime.objective"],
        "why": "통설·판례이고 사실 판단이 명확하다(일몰·일출 시각).",
    },
    "art330.commencement": {
        "label": "제330조 — 실행의 착수시기",
        "question": "주거침입 시에 착수하는가, 물색행위가 있어야 하는가.",
        "options": {
            "art330_sec4.entry_before_theft_commencement":
                "주거침입 시 착수 (판례·소개된 견해)",
            "art330_sec4.theft_or_search_required":
                "물색행위 필요 — 없으면 주거침입죄만 성립",
        },
        "recommend": ["art330_sec4.entry_before_theft_commencement"],
        "why": "주석서가 판례 입장으로 소개한다. 야간주거침입절도는 침입이 절취에 선행하는 구조다.",
    },
    "art333.resistance_standard": {
        "label": "제333조 — 반항억압 판단 기준",
        "question": "객관적으로 반항억압에 족한지, 범인의 주관적 예견으로 족한지.",
        "options": {
            "art333_sec2_3.subjective_view_attempt":
                "주관설 — 경미한 폭행이라도 범인이 억압 가능하다고 예견하면 미수 착수",
        },
        "recommend": [],
        "why": ("객관설은 이미 core에 있다(`art333_sec2_3.objective_resistance_suppression`, "
                "`subjective_intent_insufficient`). 주관설만 학설로 남으므로 내리는 것을 제안한다."),
    },
    "art333.real_estate": {
        "label": "제333조 — 부동산의 재물성",
        "question": "부동산이 강도죄의 재물인가, 재산상 이익으로 볼 것인가.",
        "options": {
            "art333_sec3_1.real_estate_as_robbery_property_negative":
                "소극설 — 부동산은 도취죄의 재물이 아니다 (주석서가 타당하다고 소개)",
            "art333_sec3_1.real_estate_rights_as_property_benefit":
                "부동산에 관한 권리를 강취하면 재산상 이익 강취로 본다",
        },
        "recommend": ["art333_sec3_1.real_estate_as_robbery_property_negative",
                      "art333_sec3_1.real_estate_rights_as_property_benefit"],
        "why": ("두 카드는 대립이 아니라 보완이다 — 재물성은 부정하고 권리는 재산상 이익으로 "
                "포섭한다. 둘 다 규칙으로 세우는 것을 제안한다."),
    },
    "art333.voluntary_delivery": {
        "label": "제333조 — 반항억압 없이 교부한 경우 기수·미수",
        "question": "객관적으로 억압에 족한 폭행이 있었으나 피해자가 억압되지 않은 채 교부한 경우.",
        "options": {
            "art333_sec3_2.voluntary_delivery_attempt":
                "귀찮음·연민으로 교부 → 인과관계 없어 강도미수",
            "art333_sec3_2.objective_violence_completed_robbery":
                "객관적 폭행 + 목적 실현 → 실제 억압 여부와 무관하게 기수",
            "art333_sec3_2.objective_violence_voluntary_delivery_attempt":
                "공포심 아래 교부 → 강취가 아니라 갈취이므로 미수",
        },
        "recommend": ["art333_sec3_2.voluntary_delivery_attempt"],
        "why": ("공갈죄와의 경계를 정하는 core 카드(`art333_sec2_3.lesser_threat_extortion`)와 "
                "정합한다. 다만 세 견해의 실무적 우열이 주석서에 명시되지 않아 확인이 필요하다."),
    },
    "art333.rape_force_taking": {
        "label": "제333조 — 강간의 폭행 후 재물 탈취",
        "question": "강간 목적 폭행으로 제압한 뒤 탈취 범의가 생긴 경우 강도인가.",
        "options": {
            "art333_sec3_3.rape_force_subsequent_taking_precedent":
                "판례 — 강도죄 성립을 인정",
            "art333_sec3_3.rape_force_not_taking_means_doctrine":
                "다수 학설 — 강도 아니고 강간죄와 절도죄의 경합",
        },
        "recommend": ["art333_sec3_3.rape_force_subsequent_taking_precedent"],
        "why": "실무는 판례를 따른다. 다수 학설은 학설 소개로 내린다.",
    },
    "art333.prior_state_use": {
        "label": "제333조 — 선행행위로 조성된 상태의 이용",
        "question": "선행 폭행·약물로 실신·심신상실 상태를 만든 뒤 탈취 범의가 생긴 경우.",
        "options": {
            "art333_sec3_3.prior_force_sustained_fear_taking":
                "선행 폭행이 다른 목적이었어도 지속되는 공포 상태를 이용하면 강도",
            "art333_sec3_3.unconsciousness_prior_force_no_causation":
                "탈취 목적 없는 선행행위와 탈취 사이에는 인과관계가 없어 강도 불성립",
            "art333_sec3_3.unconsciousness_prior_state_use_robbery":
                "자기 선행행위로 조성한 상태를 이용한 것이므로 강도 (반대 견해)",
        },
        "recommend": ["art333_sec3_3.unconsciousness_prior_state_use_robbery"],
        "why": ("core에 이미 `continuing_force_after_theft_intent`(절도 착수 후 폭행으로 탈취)와 "
                "`rape_fear_state_property_provision`(공포 상태 이용)이 있어 '자기 선행행위 상태 "
                "이용 = 강취'와 정합한다. 다만 살인 후 취거 사안의 취급이 갈리므로 확인이 필요하다."),
    },
    "art333.debt_evasion_disposition": {
        "label": "제333조 — 채무면탈형 강제이득에 처분행위가 필요한가",
        "question": "피해자의 처분행위(외관)가 요건인가.",
        "options": {
            "art333_sec4_2.debt_evasion_disposition_required": "적극설 — 처분행위 외관 필요",
            "art333_sec4_2.debt_evasion_disposition_not_required":
                "소극설 — 불필요 (주석서가 통설로 소개)",
        },
        "recommend": ["art333_sec4_2.debt_evasion_disposition_not_required"],
        "why": "주석서가 통설로 소개한다. 채권자 살해형 사안을 포섭하려면 소극설이어야 한다.",
    },
    "art333.right_exercise": {
        "label": "제333조 — 권리행사와 강도",
        "question": "권리 실행을 위한 폭행·협박으로 취득한 경우.",
        "options": {
            "art333_sec8.right_exercise_robbery_affirmative":
                "권리남용·사회통념 초과 폭행이면 위법성 조각 안 되어 강도 성립",
            "art333_sec8.right_exercise_robbery_negative":
                "권리 있는 이익은 불법이익이 아니므로 폭행죄·협박죄만 성립",
        },
        "recommend": ["art333_sec8.right_exercise_robbery_affirmative"],
        "why": ("공갈죄 쪽 core 카드(`art350_sec4_2.right_exercise_exception`)와 층이 맞는다 — "
                "권리행사라도 수단이 한도를 넘으면 범죄가 된다."),
    },
}

# ── 명제 재작성 (예시·메타 제거) ───────────────────────────────────────
REWRITE: dict[str, tuple[str, str]] = {
    "art330_sec4.entry_attempt_examples": (
        "주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 "
        "야간주거침입절도죄의 실행에 착수한 것으로 본다.",
        "빗장 사안 예시를 떼어 규칙만 남겼다. 예시는 RAG 문맥으로 남는다."),
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_cards() -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    for article in ARTICLES:
        for path in sorted((MERGE_ROOT / article / article / "norm_cards").glob("*.json")):
            for card in read_json(path)["cards"]:
                cards[card["id"]] = {**card, "article": article,
                                     "module": path.stem}
    return cards


def main() -> None:
    cards = load_cards()
    demote_reason = {cid: (axis, why)
                     for axis, entries in DEMOTE.items()
                     for cid, why in entries.items()}
    grouped = {cid: gid for gid, group in DOCTRINE_GROUPS.items() for cid in group["options"]}

    unknown = ((set(demote_reason) | set(grouped) | set(USER_CHECK) | set(DUP_MERGE)
                | set(REWRITE)) - set(cards))
    if unknown:
        raise SystemExit(f"존재하지 않는 card_id: {sorted(unknown)}")

    rows, stats = [], Counter()
    for cid, card in sorted(cards.items()):
        merge_role = card["formalization"]
        if merge_role == "context_only":
            role, axis, why = "context_only", "merge 판정", "merge가 이미 문맥으로 판정했다."
        elif cid in demote_reason:
            axis, why = demote_reason[cid]
            role = "context_only"
        elif cid in DUP_MERGE:
            target, why = DUP_MERGE[cid]
            role, axis = "context_only", "근사중복"
            why = f"{why} 유지 카드: {target}"
        elif cid in USER_CHECK:
            role, axis, why = "user_check", "확인요청", USER_CHECK[cid]
        elif cid in grouped:
            role, axis = "doctrine_choice", "학설선택"
            why = f"학설 그룹 {grouped[cid]}"
        else:
            role, axis, why = merge_role, "core 유지", ""
        stats[role] += 1
        stats[f"axis:{axis}"] += 1
        rows.append({"card_id": cid, "article": card["article"], "module": card["module"],
                     "polarity": card["polarity"], "norm_kind": card["norm_kind"],
                     "merge_role": merge_role, "audit_role": role, "axis": axis,
                     "reason": why, "proposition": card["proposition"]})

    core = [r for r in rows if r["audit_role"] in ("standard_input", "deterministic_rule")]
    per_article = Counter(r["article"] for r in core)

    AUDIT.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "재산죄 벌크와 동일 축으로 145장 전수 판독 (에이전트)",
        "articles": list(ARTICLES),
        "counts": {"merged": len(rows), "core_pending_review": len(core),
                   "context_only": stats["context_only"],
                   "doctrine_choice": stats["doctrine_choice"],
                   "user_check": stats["user_check"],
                   "per_article_core": dict(sorted(per_article.items()))},
        "axis_tally": {k[5:]: v for k, v in sorted(stats.items()) if k.startswith("axis:")},
        "doctrine_groups": DOCTRINE_GROUPS,
        "rewrites": {cid: {"new": new, "reason": why} for cid, (new, why) in REWRITE.items()},
        "duplicate_merges": {cid: {"kept": kept, "reason": why}
                             for cid, (kept, why) in DUP_MERGE.items()},
        "rows": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ── 검토문서 ────────────────────────────────────────────────────────
    negatives = [r for r in core if r["polarity"] in ("negative", "exception")]
    by_article = defaultdict(list)
    for r in core:
        by_article[r["article"]].append(r)

    lines = [
        "# 보강 3조문 검토 요청 — 제330조·제332조·제333조",
        "",
        f"강도 기본조문 등 3조문을 보강 추출했습니다(71 chunks, 실지출 $4.87). NormCard **145장**이 "
        f"나왔고, 재산죄 벌크와 **같은 축으로 전수 판독**했습니다.",
        "",
        "| 구분 | 장수 |",
        "|---|---:|",
        f"| merge 산출 | {len(rows)} |",
        f"| 자동 강등(축 판정) | {stats['context_only']} |",
        f"| **학설선택 필요** | **{stats['doctrine_choice']}** |",
        f"| **확인 필요** | **{stats['user_check']}** |",
        f"| core 잔존 | {len(core)} |",
        "",
        "축별 강등 내역",
        "",
        "| 축 | 장수 |",
        "|---|---:|",
    ]
    for axis, count in sorted(((k[5:], v) for k, v in stats.items() if k.startswith("axis:")),
                              key=lambda x: -x[1]):
        if axis in ("core 유지", "학설선택", "확인요청"):
            continue
        lines.append(f"| {axis} | {count} |")
    lines += [
        "",
        "제332조는 조문 자체가 상습성(가중유형)을 정하므로 '상습범'이 총칙 표지에 걸려도 구성요건으로 "
        "남겼습니다. 반대로 특가법·성폭력처벌법·특정강력범죄법 조문은 타법률 축으로 내렸습니다.",
        "",
        "---",
        "",
        f"## 1부. 학설선택 {len(DOCTRINE_GROUPS)}건",
        "",
        "각 그룹에서 **실무규칙으로 세울 것**을 골라 주십시오. 제 제안을 ✅로 표시했습니다. "
        "고르지 않은 카드는 학설 소개(RAG 문맥)로 내려갑니다.",
        "",
    ]
    for index, (gid, group) in enumerate(DOCTRINE_GROUPS.items(), start=1):
        lines += [f"### {index}. {group['label']}", "",
                  f"**쟁점**: {group['question']}", ""]
        for cid, label in group["options"].items():
            mark = "✅ " if cid in group["recommend"] else ""
            lines += [f"- {mark}`{cid}`", f"  - {label}",
                      f"  - 명제: {cards[cid]['proposition']}"]
        lines += ["", f"**제안 근거**: {group['why']}", "", "**선택:** ", ""]

    lines += ["---", "", f"## 2부. 확인 필요 {len(USER_CHECK)}건", "",
              "축 기준으로는 강등이지만 KCL 문항이 그 쟁점을 묻습니다. "
              "**살릴지(core) 내릴지(문맥)** 알려주십시오.", ""]
    for index, (cid, why) in enumerate(USER_CHECK.items(), start=1):
        lines += [f"### {index}. `{cid}`", "",
                  f"> {cards[cid]['proposition']}", "",
                  f"**쟁점**: {why}", "", "**판단:** ", ""]

    lines += ["---", "", f"## 3부. core 잔존 {len(core)}장 (참고 — 확인만)", "",
              "축에 걸리지 않아 규칙으로 세울 카드입니다. 이 중 부정형·예외형 "
              f"**{len(negatives)}장**은 승인해 주시면 결정B와 같은 방식으로 긍정형 질의문 초안을 "
              "따로 올리겠습니다(부정형 명제는 모델에 그대로 보내지 않습니다).", ""]
    for article in ARTICLES:
        items = by_article.get(article, [])
        if not items:
            continue
        lines += [f"### {article} — {len(items)}장", ""]
        for r in sorted(items, key=lambda r: r["card_id"]):
            flag = " ⚠️부정형" if r["polarity"] in ("negative", "exception") else ""
            lines += [f"- `{r['card_id']}`{flag}", f"  - {r['proposition']}"]
        lines += [""]

    if REWRITE:
        lines += ["---", "", "## 4부. 명제 재작성 (반영함)", ""]
        for cid, (new, why) in REWRITE.items():
            lines += [f"### `{cid}`", "", f"**전**: {cards[cid]['proposition']}", "",
                      f"**후**: {new}", "", f"**근거**: {why}", ""]
    if DUP_MERGE:
        lines += ["---", "", "## 5부. 근사중복 병합 (반영함)", ""]
        for cid, (kept, why) in DUP_MERGE.items():
            lines += [f"- `{cid}` → 유지 `{kept}`", f"  - {why}", ""]

    REVIEW.write_text("\n".join(lines), encoding="utf-8")

    print(f"merge {len(rows)}장 → core 잔존 {len(core)}장 "
          f"/ 강등 {stats['context_only']} / 학설선택 {stats['doctrine_choice']} "
          f"/ 확인 {stats['user_check']}")
    print(f"  조문별 core {dict(sorted(per_article.items()))}")
    print(f"  부정형·예외형 core {len(negatives)}장")
    print(f"  → {AUDIT.relative_to(ROOT)}")
    print(f"  → {REVIEW.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
