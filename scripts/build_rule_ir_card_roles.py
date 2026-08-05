"""부정·예외 카드의 규칙 내 역할 — 카드별 명시 표 (API 0회).

사기 조립기의 `BAR_CARD_IDS`가 손으로 열거된 목록이었던 것과 같은 자리다. 처음에 이 자리를
정규식 분류기로 채웠는데 잘못이었다 — 카드의 법리적 역할을 명제 문언 매칭으로 정하면 그 판정이
그대로 Scallop 규칙 구조에 박힌다. "폭행"이 후속 죄명으로 잡히거나 "요건이 요구되지 않는다"가
성립 저지가 되는 일이 실제로 일어났다. 그래서 정규식을 걷어내고 138장을 전수 판독해 역할과 근거를
카드마다 적는다.

성립을 막는 역할:
  bar        요건 결여·배제 — 충족되면 이 죄의 성립을 막는다
  boundary   이 죄가 아니라 **다른 죄**로 간다 — 불성립 + 후속 죄명(`value`)

성립을 만드는 역할:
  component  요건 인정 경로 — 긍정 방향 예외·한정이라 구성요건 단계에 든다

어느 쪽도 아닌 역할 — 결론 밖에서 보고만 한다(검수 002):
  waiver              요건 불요 — 성립을 막지 않는다. 무엇이 면제되는지만 기록한다
  assessment_standard 판단기준·정의 — 요건을 **어떻게 재는지**만 말한다. 기준이 참이라는
                      이유로 죄가 차단되면 정의만으로 무죄가 난다(배치 001에서 7건 적발)
  proof_standard      증명·특정 요건 — 유죄 인정의 조건이지 구성요건 자체가 아니다
  subtype_outcome     같은 죄 안의 의율유형 — 죄 전체의 성립은 유지된다
  post_outcome        구성요건 판단 뒤의 죄수·처벌 효과. 불가벌적 사후행위는 구성요건
                      불성립이 아니라 별도 처벌만 배제되는 것이므로 여기 둔다

튜플의 둘째 자리(`value`)는 역할마다 뜻이 다르다 — boundary면 후속 죄명, 보고 역할이면
답안에 그대로 노출되는 우리말 값(무엇을 재는 기준인지, 무엇이 면제되는지)이다. 이 값이 비면
카드 ID가 답안에 새기 때문에 보고 역할에는 반드시 적는다. 죄명은 명제에서 문언으로 확인한
것만 적는다. 같은 단위 안의 유형 전환(강도→준강도, 특수절도→야간주거침입절도)은 다른 죄가
아니므로 boundary로 적지 않는다.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PROP = ROOT / "data/rulegen/property"
UNITS = PROP / "rule_ir_units"
PHASE_MAP = PROP / "rule_ir_phase_map.json"
OUT = PROP / "rule_ir_card_roles.json"

# card_id → (role, refers_to, 근거)
ROLES: dict[str, tuple[str, str | None, str]] = {
    # ── 배임 ────────────────────────────────────────────────────────────
    "art355_sec4_1.business_loss_alone_insufficient": (
        "bar", None, "손해 결과나 과실만으로는 책임을 물을 수 없다 — 임무위배 인식 결여로 저지."),
    "art355_sec4_1.no_breach_of_trust_without_awareness": (
        "bar", None, "임무위배 인식이 없으면 성립 부정."),
    "art355_sec4_2.breach_for_principal_no_illicit_gain": (
        "bar", None, "본인 이익을 위한 처리는 불법이득의사 결여."),
    "art355_sec5_2.assigned_claim_proceeds_embezzlement": (
        "bar", None, "채권양도인의 임의처분은 채무불이행에 그쳐 재산죄가 성립하지 않는다."),
    "art355_sec5_2.individual_delegation_exception": (
        "component", None, "신임관계를 인정할 개별 요소가 있으면 사무의 타인성을 인정하는 "
                           "긍정 방향 경로다."),
    "art355_sec5_2.leasehold_transfer": (
        "bar", None, "자기 채무 이행의무는 타인 사무가 아니다."),
    "art355_sec5_2.movable_sale_double_disposition": (
        "bar", None, "동산 매도인은 타인 사무처리자가 아니다."),
    "art355_sec5_2.pre_certificate_stock_transfer": (
        "bar", None, "대항요건 구비 채무는 자기 사무다."),
    "art355_sec5_2.real_estate_transfer_exception": (
        "component", None, "부동산 양도의 소유권이전의무에 예외적으로 타인 사무성을 인정하는 "
                           "긍정 경로다(중도금 지급 관행)."),
    "art355_sec5_2.registered_movable_sale_disposition": (
        "bar", None, "등록 이전 의무자도 타인 사무처리자가 아니다."),
    "art355_sec5_2.right_transfer_ordinary_duty": (
        "bar", None, "통상 계약상 급부의무는 타인 사무가 아니다."),

    # ── 배임수증재 ──────────────────────────────────────────────────────
    "art357_sec1_3.receipt.no_breach_or_loss_requirement": (
        "waiver", "임무위배·재산상 손해", "임무위배·손해는 배임수재의 요건이 아니다 — 성립을 막지 않는다."),
    "art357_sec3_1.mere_contractual_debt_exclusion": (
        "bar", None, "이익대립 계약상 채무만으로는 타인의 사무가 아니다."),
    "art357_sec3_1.no_status_at_request": (
        "bar", None, "지위 취득 전 청탁은 주체 요건 결여."),
    "art357_sec3_1.subject_no_external_authority": (
        "waiver", "대외적 권한·포괄위탁", "대외적 권한·포괄위탁은 요건이 아니다."),
    "art357_sec3_2.giver_not_necessarily_liable": (
        "component", None, "증재자에게 정당한 청탁이 수재자에게는 부정한 청탁이 될 수 있다는 "
                           "부정성 인정 경로다."),
    "art357_sec3_2.permitted_favor_request": (
        "bar", None, "직무권한 내 편의·허용 범위 선처 부탁은 부정한 청탁이 아니다."),
    "art357_sec3_2.self_rights_protection_not_improper": (
        "bar", None, "자기 권리 확보 행위는 부정한 청탁이 아닐 수 있다."),
    "art357_sec3_3.principal_not_third_party_precedent": (
        "bar", None, "위임한 본인은 제3자가 아니므로 제3자 취득 요건이 결여된다."),
    "art357_sec3_3.unrelated_payment_no_offense": (
        "bar", None, "청탁과 무관한 수령은 성립하지 않는다."),
    "art357_sec3_4.no_acquisition_intent": (
        "bar", None, "취득 의사 결여."),
    "art357_sec3_5.no_corrupt_performance_required": (
        "waiver", "부정행위의 실행", "부정행위까지 나아갈 것은 기수 요건이 아니다."),
    "art357_sec4.giver_view_justification": (
        "bar", None, "증재자 관점에서 부정성이 부정되면 증재죄가 성립하지 않는다."),
    "art357_sec4.giving_to_business_handler": (
        "bar", None, "사무처리자가 아닌 자에 대한 공여는 성립하지 않는다."),

    # ── 횡령 ────────────────────────────────────────────────────────────
    "art355.embezzlement.object-excludes-property-interest": (
        "bar", None, "재물이 아닌 권리·이익·정보는 객체가 아니다."),
    "art355.embezzlement_illegal_name_trust": (
        "bar", None, "무효인 명의신탁은 보호할 위탁관계가 아니다."),
    "art355_sec1_2.embezzlement_illegal_appropriation_exclusion": (
        "bar", None, "일시사용·손괴·은닉 의사 또는 위탁자를 위한 의사는 불법영득의사 결여."),
    "art355_sec3_3.deceptive_means_no_fraud": (
        "waiver", "기망수단 사용 시 사기죄의 별도 성립", "횡령 성립을 막지 않고 사기죄의 별도 성립만 배제한다 — 죄수 판단이므로 "
                        "이 단위의 저지 사유가 아니다."),
    "art355_sec3_3.no_property_damage_element": (
        "waiver", "재산상 손해의 발생", "재산상 손해 발생은 횡령의 요건이 아니다."),
    "art355_sec3_3.simple_destruction_exception": (
        "bar", None, "손괴는 그 자체로 불법영득의사의 표현이 아니다."),
    "art355_sec4_1.discretionary_funds_no_presumption": (
        "bar", None, "재량 보관금은 증빙 부재만으로 불법영득의사를 추단할 수 없다."),
    "art355_sec4_1.explained_fund_use_no_inference": (
        "bar", None, "합리적 설명·자료가 있으면 불법영득의사를 인정할 수 없다."),
    "art355_sec4_1.justified_refusal_exception": (
        "bar", None, "동시이행·유치·상계권 행사는 정당한 반환거부."),
    "art355_sec4_1.representative_corporate_debt_payment": (
        "bar", None, "권한 내 회사채무 이행은 불법영득의사가 없다."),
    "art355_sec4_2.mere_destruction_not_appropriation": (
        "bar", None, "손괴 의사만으로는 불법영득의사를 구성하지 않는다."),
    "art355_sec4_2.owner_benefit_disposition_no_appropriation": (
        "bar", None, "소유자 이익을 위한 처분은 불법영득의사가 없다."),
    "art355_sec4_3.accounting_only_adjustment": (
        "bar", None, "장부상 정리에 불과하면 불법영득의사가 없다."),
    "art355_sec4_3.fake_capital_no_real_increase": (
        "bar", None, "자본 실질 증가가 없으면 불법영득의사를 인정하기 어렵다."),
    "art355_sec4_3.objectively_not_grossly_improper_expenditure": (
        "bar", None, "객관적으로 심히 부당하지 않은 지출은 불법영득의사가 부정된다."),
    "art355_sec4_3.organization_representative_litigation_exception": (
        "bar", None, "예외 요건을 갖춘 변호사비용 지출은 허용되어 횡령이 아니다."),
    "art355_sec4_3.slush_fund_concealment": (
        "bar", None, "비자금 은닉·차명관리만으로는 불법영득의사를 인정할 수 없다."),
    "art355_sec5.retention_lien_no_illicit_intent": (
        "bar", None, "유치권·동시이행 항변 행사에 의한 반환거부는 구성요건해당성이 없다."),
    "art356_sec2_2.unrelated_possession": (
        "bar", None, "업무와 무관한 보관은 업무상횡령의 가중요건을 채우지 못한다. 단순횡령 성립은 "
                     "별론이고 이 단위의 가중 판정에서만 저지한다."),

    # ── 공갈 ────────────────────────────────────────────────────────────
    "art350_sec3.own_property_exception": (
        "bar", None, "자기 재물·이익은 객체가 아니다."),
    "art350_sec4_1.objectively_insufficient_threat": (
        "boundary", "절도", "외포시키기에 부족한 행위는 공갈이 아니고 절도가 문제된다."),
    "art350_sec4_1.robbery_boundary": (
        "boundary", "강도", "반항억압 정도에 이르면 공갈이 아니라 강도다."),
    "art350_sec4_2.actual_intent_or_feasibility_not_required": (
        "waiver", "해악 실현의 의사·가능성", "해악 실현 의사·가능성은 성립에 영향이 없다."),
    "art350_sec4_2.right_exercise_exception": (
        "bar", None, "권리행사인 경우 위법성이 조각될 수 있다."),
    "art350_sec5_2.fear_causation_required": (
        "bar", None, "협박·폭행이 원인이 아닌 외포에 의한 처분은 성립하지 않는다."),
    "art350_sec5_2.no_fear_attempt": (
        "bar", None, "외포심이 생기지 않았거나 다른 이유로 교부한 경우는 기수가 아니라 미수다 — "
                     "같은 죄의 미수이므로 후속 죄명을 적지 않는다."),
    "art350_sec5_3.complete_suppression_robbery": (
        "boundary", "강도", "의사가 완전히 억압되면 공갈이 아니라 강도다."),
    "art350_sec6.no_overall_property_decrease": (
        "waiver", "전체 재산의 감소", "전체 재산의 감소는 요건이 아니다."),
    "art350_sec6_2.satisfied_consideration_causation_exception": (
        "bar", None, "상당한 대가에 만족한 교부는 인과관계가 부정되어 미수에 그친다."),
    "art350_sec8_2.permitted_threat_no_extortion": (
        "bar", None, "사회통념상 허용 범위의 위협적 언사는 공갈이 아니다."),
    "art350_sec8_2.right_exercise_total_assessment": (
        "assessment_standard", "권리행사와 공갈의 한계 판단",
        "권리행사와 공갈의 한계를 어떻게 재는지에 관한 기준일 뿐, 조각이 인정되었다는 결론이 "
        "아니다(검수 002 C-02)."),

    # ── 권리행사방해 ────────────────────────────────────────────────────
    "art323_sec1_1.no_unlawful_appropriation_intent": (
        "waiver", "불법영득의사", "불법영득의사는 요건이 아니다."),
    "art323_sec2_2.coowned_property_excluded": (
        "bar", None, "공유물은 자기 물건이 아니다."),
    "art323_sec2_2.manifestly_no_right_possession_excluded": (
        "bar", None, "권리 없음이 명백한 점유는 보호대상이 아니다."),
    "art323_sec2_2.nominee_owner_not_subject": (
        "bar", None, "명의신탁자는 주체가 아니다."),
    "art323_sec2_2.official_custody_exception": (
        "bar", None, "공무소 보관명령 물건은 제외된다."),
    "art323_sec2_2.prohibited_gold_products_excluded": (
        "bar", None, "금제품은 객체가 아니다."),
    "art323_sec2_2.registered_sale_seller_not_subject": (
        "bar", None, "등기·등록이 마쳐지면 매도인은 주체가 아니다."),
    "art323_sec2_3.consensual_transfer_not_taking": (
        "bar", None, "점유자 의사에 기한 이전은 취거가 아니다."),
    "art323_sec3.no_intent_to_appropriate_required": (
        "waiver", "영득의사", "영득죄가 아니므로 영득의사를 요하지 않는다."),

    # ── 점유이탈물횡령 ──────────────────────────────────────────────────
    "art360_sec2_2.managed_place_property": (
        "boundary", "절도", "관리 장소 내 물건은 점유이탈물이 아니고 절도의 객체다."),
    "art360_sec2_2.mistaken_bank_transfer_embezzlement_holding": (
        "boundary", "횡령", "착오 입금 금원은 횡령의 객체이고 점유이탈물이 아니다."),
    "art360_sec2_2.original_possessor_recovery": (
        "boundary", "절도", "원점유자의 점유가 존속하면 절도가 성립한다."),
    "art360_sec2_2.ownerless_property_exclusion": (
        "bar", None, "무주물은 타인 소유가 아니다."),
    "art360_sec2_2.public_transport_found_property": (
        "boundary", "절도", "승무원의 점유가 인정되면 절도로 처벌된다."),
    "art360_sec2_3.reporting_noncompliance_alone": (
        "bar", None, "법정 절차 미이행만으로는 성립하지 않는다."),

    # ── 업무자 신분(공유 모듈) ──────────────────────────────────────────
    "art356_sec2_2.administrative_illegality": (
        "component", None, "행정절차상 불법이 있어도 업무성을 인정하는 긍정 경로다."),
    "art356_sec2_2.illegal_business": (
        "bar", None, "법이 절대적으로 금지하는 행위는 업무가 되지 못한다."),

    # ── 손괴 ────────────────────────────────────────────────────────────
    "art366.corpse_exclusion": ("bar", None, "사체는 제366조의 객체가 아니다."),
    "art366.no_utility_property_exclusion": (
        "bar", None, "이용가치·효용이 전혀 없으면 재물성이 부정될 수 있다."),
    "art366.ownerless_property_exclusion": ("bar", None, "무주물은 타인성이 없다."),
    "art366.public_document_used_by_office": (
        "boundary", "공용서류무효(제141조)", "공용서류는 제366조 객체에서 빠지고 제141조가 "
                                        "별도로 규율한다 — 다른 조문으로의 전환이라 boundary가 "
                                        "bar보다 정확하다."),
    "art366.special_medium_record_limited_view": (
        "component", None, "특수매체기록의 범위를 한정하는 객체 판정 기준이다."),
    "art366.transmitting_or_processing_information_exclusion": (
        "bar", None, "전송·처리 중 정보는 객체가 아니다."),
    "art366_sec3_2.document_removal_without_owner_intent": (
        "bar", None, "새로운 사용 지장이 없으면 문서손괴가 아니다."),
    "art366_sec3_2.electronic_record_power_cutoff_exception": (
        "bar", None, "전원 차단은 기록 손상이 없으면 별도 성립하지 않는다."),
    "art366_sec3_2.mere_functional_interference_not_destruction": (
        "bar", None, "변형·손상 없는 기능 훼손은 손괴가 아니다."),
    "art366_sec3_2.movement_no_objective_use_value": (
        "bar", None, "객관적 이용가치가 없으면 효용침해를 인정할 수 없다."),
    "art366_sec3_2.wall_graffiti_functional_efficiency_limit": (
        "component", None, "낙서는 기능적 효용이 현저히 침해된 경우에 성립한다는 인정 기준이다."),
    "art366_sec4_1.intent_absence": ("bar", None, "고의 결여."),
    "art366_sec5_2.immediate_self_recovery_assessment": (
        "assessment_standard", "자력탈환의 직시성 판단",
        "자력탈환의 직시성을 판단하는 기준이지 직시성이 인정되었다는 결론이 아니다(검수 002 C-02)."),
    "art366_sec5_2.justifiable_act_requirements": (
        "assessment_standard", "정당행위의 요건",
        "정당행위의 요건을 열거한 기준이지 그 요건이 충족되었다는 결론이 아니다(검수 002 C-02)."),
    "art366_sec5_2.possession_protection_destruction": (
        "bar", None, "점유 보호를 위한 절단은 정당행위가 된다."),
    "art366_sec5_2.socially_acceptable_act": (
        "assessment_standard", "사회상규 불위배 판단",
        "사회상규 불위배를 재는 기준이지 위배되지 않았다는 결론이 아니다(검수 002 C-02)."),
    "art366_sec5_5.presumed_consent": (
        "assessment_standard", "추정적 승낙의 판단",
        "추정적 승낙의 판단 기준이지 승낙이 추정된다는 결론이 아니다(검수 002 C-02)."),

    # ── 강도류 ──────────────────────────────────────────────────────────
    "art333_sec2_2.incidental_incapacitation_no_robbery": (
        "bar", None, "혼취가 탈취 방법이 아니면 강도가 아니다."),
    "art333_sec2_2.preexisting_incapacitation_exception": (
        "bar", None, "타인의 행위로 이미 혼취된 상태의 이용은 강도의 폭행이 아니다."),
    "art333_sec2_3.diversion_or_insult_violence_no_robbery": (
        "boundary", "절도", "주의 전환·모욕 목적의 폭행이면 절도와 폭행·협박죄가 된다."),
    "art333_sec2_3.lesser_threat_extortion": (
        "boundary", "공갈", "반항억압에 이르지 않고 공포심만 일으켰으면 공갈이다."),
    "art333_sec2_3.subjective_intent_insufficient": (
        "bar", None, "객관적으로 반항억압에 이르지 못하면 주관적 의사만으로는 성립하지 않는다."),
    "art333_sec3_1.real_estate_as_robbery_property_negative": (
        "component", None, "부동산은 재물이 아니지만 그 권리 취득은 재산상 이익의 강취로 포섭하는 "
                           "객체 판정 경로다 — 성립을 막지 않는다."),
    "art333_sec3_2.post_taking_assault_no_robbery": (
        "bar", None, "탈취 후 구타가 강취와 무관하면 강도가 아니다."),
    "art333_sec3_2.voluntary_delivery_attempt": (
        "bar", None, "반항억압 없는 교부는 강취의 인과관계가 없어 미수에 그친다."),
    "art333_sec3_3.completed_theft_quasi_robbery_exception": (
        "bar", None, "절도 기수 후의 폭행은 본래의 강도가 아니라 준강도로 간다. 준강도는 같은 "
                     "단위의 가중 유형이므로 후속 죄명으로 적지 않고 여기서는 본래 강도만 저지한다."),
    "art333_sec3_3.unconsciousness_prior_force_no_causation": (
        "boundary", "절도", "탈취 목적 없는 선행행위와 탈취 사이에 인과관계가 없으면 절도다."),
    "art333_sec6.no_attempt_insufficient_violence_intimidation": (
        "bar", None, "폭행·협박의 정도가 부족하면 착수가 인정되지 않는다."),
    "art333_sec6.no_attempt_without_violence_intimidation_commencement": (
        "bar", None, "폭행·협박에 착수하지 않으면 강도의 착수가 없다."),
    "art333_sec7_1.completion.no_safe_escape_requirement": (
        "waiver", "안전지역으로의 이탈", "안전지역 이탈은 기수 요건이 아니다."),
    "art333_sec7_1.completion.recovery_does_not_negate": (
        "waiver", "탈환되지 않았을 것", "탈환은 기수 인정에 영향이 없다."),
    "art333_sec8.right_exercise_robbery_negative": (
        "boundary", "폭행 또는 협박", "취득할 권리가 있는 이익은 불법한 이익이 아니다(대법원 "
                                  "소극설) — 카드 문언이 후속 죄명(폭행죄·협박죄)을 명시한다."),
    "art334_sec2_1.weapon_awareness_not_required": (
        "waiver", "상대방의 흉기 인식", "상대방의 흉기 인식은 요건이 아니다."),
    "art334_sec2_1.weapon_direct_use_not_required": (
        "waiver", "흉기의 직접 사용", "흉기의 직접 사용은 요건이 아니다."),
    "art335_sec2.preparation_stage_exclusion": (
        "bar", None, "절취 착수 전 예비단계의 폭행은 준강도가 아니다."),
    "art335_sec2.property_interest_exclusion": (
        "bar", None, "재산상 이익 취득 목적의 폭행은 준강도가 아니다."),
    "art335_sec3_1.pre_control_violence_is_robbery_exception": (
        "component", None, "배타적 지배 확립 전 폭행은 준강도가 아니라 본래의 강도라는 인정 "
                           "경로다 — 강도 성립을 막지 않는다."),
    "art335_sec3_2.arrest_or_concealment_no_control": (
        "waiver", "재물에 대한 사실상 지배의 취득", "체포면탈·흔적인멸 목적에서는 재물 지배 취득이 요건이 아니다."),
    "art335_sec6_1.days_later_no_opportunity": (
        "bar", None, "수일 후의 폭행은 절도의 기회가 아니다."),
    "art335_sec6_2.opportunity_safe_escape_limit": (
        "bar", None, "안전한 도피 후에는 기회의 계속성이 인정되지 않는다."),
    "art337_sec3.injury_result_violence_intent": (
        "component", None, "치상죄에도 폭행의 고의는 있어야 한다는 요건 요구 — 가중 플래그의 "
                           "전제조건이다."),
    "art337_sec3_2.robbery_occasion_ended": (
        "bar", None, "기회가 종료된 뒤의 상해는 가중요건을 채우지 못한다."),
    "art337_sec3_2.trivial_injury_excluded": (
        "bar", None, "극히 경미한 상처는 상해가 아니다."),
    "art338_sec2.debt_evasion_no_robbery": (
        "boundary", "살인", "이익 이전이 인정되지 않으면 강도살인이 아니라 살인죄에 그친다."),
    "art338_sec3.opportunity_new_intent_after_completion": (
        "bar", None, "종료 후 새 범의의 살해는 강도의 기회가 아니다."),
    "art338_sec4.robbery_death_attempt_excluded": (
        "waiver", "강도치사죄의 미수 처벌", "강도치사죄에 미수범이 없다는 적용범위 규칙이다."),
    "art343_sec1.robbery_scope": (
        "component", None, "예비죄의 '강도' 범위를 정하는 적용범위 규칙(준강도 제외)."),
    "art343_sec3.abandonment_before_execution_denied": (
        "post_outcome", "중지미수 감면 불가",
        "예비·음모죄가 완성된 뒤에는 중지미수 감면을 쓸 수 없다는 사후 법률효과이지 "
        "성립 판단이 아니다(검수 002 D-07)."),

    # ── 절도류 ──────────────────────────────────────────────────────────
    "art329_sec2.theft_exception_ownership_or_self_possession": (
        "bar", None, "자기 소유·자기 점유 사안은 절도가 아니다. 권리행사방해·횡령 성립은 별론이라 "
                     "후속 죄명을 단정하지 않는다."),
    "art329_sec2_1.inherited_estate_not_ownerless": (
        "component", None, "상속재산의 국가 귀속으로 타인성을 인정하는 경로다."),
    "art329_sec2_1.ownerless_property_exception": (
        "bar", None, "무주물은 객체가 아니다."),
    "art329_sec2_2.sole_custodian_coowned_property": (
        "boundary", "횡령", "단독보관자의 영득은 절도가 아니라 횡령이다."),
    "art329_sec2_2.unfound_transit_lost_property": (
        "boundary", "점유이탈물횡령", "발견 전 유실물의 취거는 점유이탈물횡령이다."),
    "art329_sec4.intent.mistake_abandoned_property": (
        "bar", None, "포기물로 오인한 취득은 고의가 없다."),
    "art329_sec5_1.unlawful_appropriation_required": (
        "component", None, "불법영득의사를 주관적 요건으로 요구하는 규칙이다."),
    "art329_sec5_2.fuel_consumption_incidental_use": (
        "bar", None, "일시 사용에 수반된 연료 소비는 별도로 문제 삼지 않는다."),
    "art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return": (
        "bar", None, "경미한 소모 후 즉시 반환은 영득의사가 없다."),
    "art329_sec5_2.use_theft_possession_not_completely_lost": (
        "bar", None, "소지가 상실되지 않고 곧 환원될 상태면 사용절도로 불처벌."),
    "art329_sec6.consent_manifestation": (
        "waiver", "승낙의 명시적 표시", "승낙의 표시 방식을 정하는 해석 기준일 뿐 그 자체로 요건을 인정하는 "
                       "경로가 아니다 — L6(위법성·책임) 카드라 component로 두면 component_layer가 "
                       "L0~L4만 순회해 어떤 규칙에도 안 걸린다(component 재분해 중 발견). "
                       "waiver로 두어 해석기준 사실만 기록한다."),
    "art329_sec6.consent_no_taking": (
        "bar", None, "피해자의 승낙이 있으면 절취가 아니다."),
    "art330_sec3.restaurant_permitted_entry_no_intrusion": (
        "bar", None, "허용된 출입은 침입이 아니어서 야간주거침입절도 가중요건을 채우지 못한다."),
    "art331_sec2_2.key-opening-special-theft-exception": (
        "bar", None, "열쇠로 통상 방법으로 침입한 경우는 특수절도가 아니다. 야간주거침입절도로 "
                     "가는 것은 같은 단위의 다른 가중 유형이므로 후속 죄명으로 적지 않는다."),
    "art331_sec3_1.toy_gun_not_weapon_exception": (
        "bar", None, "장난감 권총은 흉기가 아니다."),
    "art332_sec1_1.different_offense_types": (
        "bar", None, "죄종을 달리하는 경력은 절도 상습성의 근거가 되지 않는다."),
    "art332_sec1_2.habituality-not-repetition-alone": (
        "bar", None, "반복만으로는 상습성이 인정되지 않는다."),
    "art332_sec1_2.incidental-or-economic-theft-exception": (
        "bar", None, "우발적 동기·경제사정에서 비롯된 경우는 상습성이 부정된다."),
}

# 성립을 막는 역할과 결론 밖에서 보고만 하는 역할을 분리한다.  판단기준·증명요건·
# 내부 의율유형·죄수효과는 어느 것도 죄의 성부를 결정하지 않는다.
VALID_ROLES = ("bar", "waiver", "boundary", "component",
               "assessment_standard", "proof_standard",
               "subtype_outcome", "post_outcome")
REPORTING_ROLES = ("waiver", "assessment_standard", "proof_standard",
                   "subtype_outcome", "post_outcome")
ROLE_GLOSSARY = {
    "bar": "요건 결여·배제 — 성립을 막는다",
    "waiver": "요건 불요 — 성립을 막지 않는다",
    "boundary": "이 죄가 아니라 다른 죄로 — refers_to에 죄명",
    "component": "요건 인정 경로 — 구성요건 단계에 든다",
    "assessment_standard": "판단기준·정의 — 요건을 어떻게 재는지만 말하고 결론을 내지 않는다",
    "proof_standard": "증명·특정 요건 — 유죄 인정의 조건이지 구성요건 자체가 아니다",
    "subtype_outcome": "같은 죄 안의 의율유형 — 죄 전체의 성립은 유지된다",
    "post_outcome": "구성요건 판단 뒤의 죄수·처벌 효과",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    phase_rows = read_json(PHASE_MAP)["rows"]
    levels = {row["card_id"]: row["level"] for row in phase_rows}
    needed: dict[str, dict[str, Any]] = {}
    for path in sorted(UNITS.glob("*.json")):
        payload = read_json(path)
        unit = payload["issue_tag"]
        if unit == "relative_property_crime_exception":
            continue
        for card in payload["cards"]:
            if card["polarity"] in ("negative", "exception") \
                    or levels.get(card["id"]) == "L6":
                needed[card["id"]] = {"unit": unit, "level": levels.get(card["id"]),
                                      "polarity": card["polarity"],
                                      "proposition": card["proposition"]}

    missing = sorted(set(needed) - set(ROLES))
    extra = sorted(set(ROLES) - set(needed))
    if missing or extra:
        raise SystemExit(f"역할 표 불일치\n  누락 {missing}\n  잉여 {extra}")
    for card_id, (role, value, _) in ROLES.items():
        if role not in VALID_ROLES:
            raise SystemExit(f"{card_id}: 알 수 없는 역할 {role}")
        if (role == "boundary") != bool(value and role == "boundary"):
            raise SystemExit(f"{card_id}: boundary는 후속 죄명을 반드시 가진다")
        # 보고 역할의 값은 답안에 그대로 노출된다. 비워 두면 카드 ID가 새어 나간다.
        if role in REPORTING_ROLES and not value:
            raise SystemExit(f"{card_id}: {role}은 답안에 노출할 우리말 값이 필요하다")
        if role in ("bar", "component") and value:
            raise SystemExit(f"{card_id}: {role}은 값을 갖지 않는다")

    entries = {card_id: {**needed[card_id], "role": role,
                         "refers_to": value if role == "boundary" else None,
                         "value": value, "rationale": rationale}
               for card_id, (role, value, rationale) in sorted(ROLES.items())}
    tally = Counter(entry["role"] for entry in entries.values())
    OUT.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "138장 전수 판독으로 역할·근거를 카드마다 지정 (정규식 분류 폐기)",
        "roles": ROLE_GLOSSARY,
        "counts": {"cards": len(entries), **dict(sorted(tally.items()))},
        "cards": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"역할 지정 {len(entries)}장: " +
          " / ".join(f"{role} {count}" for role, count in sorted(tally.items())))
    print(f"  → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
