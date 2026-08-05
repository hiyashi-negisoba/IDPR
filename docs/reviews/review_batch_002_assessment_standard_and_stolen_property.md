# 검수 배치 002 — 법률검수 판정

## C. 새 역할 `assessment_standard`

### C-01 컴파일 동작

판정: **O — 단, “모델이 스스로 포섭”한다는 설명은 수정**

> comment: `assessment_standard`를 결론 relation에 연결하지 않고 판단기준으로만 보존하는 설계는 타당합니다.
> 다만 “모델이 기준을 알고 스스로 포섭한다”는 표현은 Neural–Symbolic–Neural 원칙상 위험합니다. 모델은 판단기준을 자연어로 설명할 수는 있어도, 그 기준에 따른 최종 법적 충족 여부를 새로 결정해서는 안 됩니다.
>
> 권고 구조:
>
> * `assessment_standard`: 판단기준·정의
> * `assessment_facts`: 사건에서 인정된 세부 사실
> * `assessment_result`: 기준에 따른 충족·불충족·미확정
>
> 현재 `assessment_result`가 없다면 symbolic conclusion은 `undetermined`로 남겨야 합니다. 생성 모델이 기준만 보고 무죄·유죄를 독자적으로 확정하면 심볼릭 엔진이 결론을 소유한다는 원칙이 무너집니다.

### C-02 적용 대상 7건

판정: **O**

> comment: 제시된 7건은 모두 현재 문언만으로는 최종 차단결론이 아니라 정의 또는 심사기준에 가깝습니다. 전부 `assessment_standard`로 이관하는 것이 맞습니다.
>
> 특히 `mental_disorder_requirements`는 심신장애의 판단구조를 설명할 뿐 심신상실 또는 심신미약이 실제 인정되었다는 결론이 아니므로 직접 bar가 될 수 없습니다.

---

# D. 배치 001 후속 결정

## D-01 조건부 O 카드 처리

판정: **X — (가) 일괄 유지 반대. 카드별 임시 분류 후 (다) 분리**

> comment: 제시된 항목은 실제로 8건입니다. 이 8건을 모두 “구체적 사실상황”이라는 이유로 현행 bar에 두는 것은 위험합니다. 카드 문언의 완결성이 서로 다릅니다.
>
> 임시 조치는 다음처럼 나누는 것이 적절합니다.

### 현행 차단 역할 잠정 유지 가능

1. `labor_dispute_incidental_act`

   * 적법하게 개시된 쟁의행위
   * 목적 공지·준비를 위한 부수행위
   * 관행적 방식
   * 수단·방법의 적정성
     가 모두 카드 평가대상에 포함된다면 정당행위의 완결된 조건군에 가깝습니다.

2. `omission_escape_guarantor`

   * 일반인이고 보증인적 지위가 없으며
   * 행위가 단순 불인계에 그친 경우
     부작위범의 작위의무 결여를 직접 나타냅니다.

3. `active_conduct_requirement`

   * 사건 행위가 소극적 거동·불복종에 그쳤다는 것까지 평가한다면 폭행·협박 요건 결여를 직접 나타냅니다.

### `assessment_standard` 또는 배제 쪽이 안전

4. `mutual_fight_excessive_weapon`

   * “정당방위가 허용될 수 있다”는 가능성만 표현하며, 실제 반격의 필요성과 상당성까지 결론짓지 않습니다.

5. `advance_directive_life_sustaining_treatment`

   * 사전의료지시의 효력 판단기준이지, 적법한 치료중단의 전체 요건 충족 결론이 아닙니다.

6. `life_sustaining_treatment_withdrawal`

   * 전문의 소견 등을 종합하여 신중히 판단해야 한다는 기준과 최종 허용 가능성이 섞여 있습니다.

7. `presumed_will_life_sustaining_treatment`

   * 환자의 의사 추정에 관한 중간요건이지 살인죄 차단의 완결결론이 아닙니다.

8. `voluntary_accompaniment`

   * 임의동행의 적법성 판단기준과 위법한 동행의 구체적 결과가 한 카드에 혼재합니다.

> 최종적으로는 (다) 카드 분리가 정답입니다.
> 분리 전에는 1·2·3만 잠정 차단 역할에 남기고 4~8은 `assessment_standard` 또는 `excluded_pending_split`로 두는 것을 권고합니다.
>
> P2의 기존 `waiver`가 위법성·책임조각을 의미한다면 `labor_dispute_incidental_act`의 현 역할은 그 의미와 정합합니다. 다만 역할명 자체는 장기적으로 `justification_bar`로 바꾸는 것이 안전합니다.

## D-02 카드 분리 3건의 잠정 조치

판정: **O**

> comment: 분리 완료까지 `excluded_cards`로 배제하는 것이 가장 안전합니다. 세 카드 모두 한 카드 안에 상반되거나 서로 다른 효과가 들어 있어, 현 상태로 발화시키면 false positive 또는 false negative가 발생합니다.
>
> 단, `excluded`가 영구 삭제를 의미하지 않도록 다음 상태를 별도로 두는 것이 좋습니다.
>
> `excluded_pending_split`
>
> 이렇게 해야 법률적으로 틀린 카드와 구조상 분리가 필요한 카드를 구별할 수 있습니다.

## D-03 A-19 죄수효과

판정: **O**

> comment: `post_outcome`으로 이관하는 것이 맞습니다. 명제는 살인죄를 부정하거나 강도죄로 이동시키는 것이 아니라:
>
> * 결합범 성립 부정
> * 독립 살인죄 성립 유지
> * 선행 강도죄 또는 강간죄 성립 유지
> * 양 죄의 실체적 경합
>
> 을 나타냅니다.
>
> 따라서 post-outcome payload에 최소한 다음 정보가 필요합니다.
>
> * `preserved_units`
> * `excluded_combined_offense`
> * `concurrence_type = real_concurrence`
>
> 단순 자연어 설명만 저장하면 이후 죄수 계산에는 사용할 수 없습니다.

## D-04 공문서위조·변조 통합 유닛

판정: **O — 단, `post_outcome`보다 `subtype_outcome` 권고**

> comment: 등록 유닛이 `public_document_forgery` 하나이고 위조·변조를 내부 subtype으로 다룬다면 자기 자신을 target으로 하는 boundary는 부적절합니다.
>
> 기존 문서의 주요 부분이 변경되어 동일성이 상실되면 변조가 아니라 위조로 평가될 수 있으므로, 이 카드는 죄 전체의 성립·불성립보다 내부 적용유형을 확정하는 효과입니다.
>
> 새 역할을 최소화한다면 `post_outcome`으로 처리할 수 있지만, 의미상으로는 다음과 같은 내부 subtype relation이 더 정확합니다.
>
> `public_document_offense_subtype(case, forgery)`
>
> 따라서:
>
> * 당장: `post_outcome` 승인
> * 장기: `subtype_outcome` 또는 unit 내부 component로 이전 권고

## D-05 `quasi_sexual_offense` target

판정: **O — 라벨만이 아니라 사건별 subtype도 보존**

> comment: 등록 유닛이 준강간·준강제추행을 통합한 `quasi_sexual_offense`라면 boundary target은 그대로 두어도 됩니다.
>
> 다만 답안 라벨만 “준강간”으로 바꾸는 것만으로는 부족합니다. symbolic output에 다음과 같이 subtype을 함께 저장해야 합니다.
>
> * `target_unit = quasi_sexual_offense`
> * `target_subtype = quasi_rape`
> * `display_label = 준강간`
>
> 사건이 간음이 아니라 추행인 경우에는 같은 유닛 내 `quasi_indecent_act`로 나뉘어야 하므로, 라벨을 유닛 전체에 고정해서는 안 됩니다.

## D-06 P2 `requirement_waived` 신설

판정: **O**

> comment: P2에 기존 `waiver`와 별개의 `requirement_waived`를 신설하고, 배제했던 긍정 확인 법리를 되살리는 것이 맞습니다.
>
> 적용대상:
>
> * 방화 당시 사람의 실제 현존 불요
> * 객체의 착오가 고의를 조각하지 않음
> * 방법의 착오가 고의를 조각하지 않음
> * 의도하지 않은 피해자에게 결과가 발생해도 고의 귀속이 유지되는 경우
> * 일정한 시간적 간격이 고의 또는 인과관계를 당연히 조각하지 않는다는 법리
>
> 다만 모두 동일한 `requirement_waived`로 처리하기보다 내부 `waived_requirement` 값을 지정해야 합니다.
>
> 예:
>
> * `actual_presence`
> * `identity_match_between_intended_and_actual_victim`
> * `exact_method_match`
> * `temporal_immediacy`
>
> 이 역할은 결론을 직접 성립시키는 것이 아니라, 특정 필수요건으로 잘못 간주된 사항을 AND 목록에서 제거하는 효과여야 합니다.

## D-07 중지미수 불인정

판정: **O — `post_outcome` 승인**

> comment: 예비·음모죄가 이미 완성된 후에는 중지미수에 따른 형 감면 또는 면제 효과가 발생하지 않는다는 내용이므로, 본죄 구성요건 판단보다 후속 법률효과에 가깝습니다.
>
> 다만 `post_outcome` 안에서:
>
> * `defense_or_mitigation = voluntary_abandonment`
> * `availability = denied`
>
> 를 구조화해야 합니다. 자연어 문구만 두면 다른 감면사유와 구별되지 않습니다.

---

# E. 장물죄 146장 역할 배치안

## E-01 `component` 44장

판정: **X — 그룹 전체 승인 불가, 재분류 필요**

> comment: 이 그룹은 component, bar, assessment standard, waiver, proof requirement, procedural outcome이 혼재합니다. “이 중 하나라도 satisfied이면 해당 component가 충족된다”는 컴파일은 특히 위험합니다.

### component로 유지 가능한 카드

* `sec3_1.instigator_aider_subject`
* `sec3_2.tangible_property`
* `sec3_2.embodied_security`
* `sec3_2.chain_stolen_property`
* `sec3_3.acquisition.actual_possession`
* `sec3_3.acquisition.knowledge_at_delivery`
* `sec3_3.transport.consent_and_delivery`
* `sec3_3.custody.actual_receipt`
* `sec3_3.custody.knowledge`
* `sec4_1.intent_and_knowledge`
* `sec4_1.prior_possessor_consensus`
* `sec4_1.consensus_at_time_of_act`
* `sec4_1.knowledge_timing_instant_offenses`

### `assessment_standard`로 이동

* `sec3_2.precedent_definition`
* `sec3_2.real_estate`
* `sec3_2.deceptive_bank_transfer`
* `sec3_2.prohibited_goods`
* `sec3_2.minor_principal`
* `sec3_2.foreign_offense`
* `sec3_2.registered_imported_car`
* `sec3_2.illegal_cause_benefit_fraud`
* `sec3_2.money_traceability`
* `sec3_3.acquisition.delivery_despite_price`
* `sec3_3.transfer.unaware_a_to_aware_b`
* `sec3_3.transport.short_distance`
* `sec3_3.transport.knowledge_midway`
* `sec3_3.brokering.act_suffices_precedent`
* `sec3_3.brokering.unsuccessful_jewelry_sale`
* `sec4_1.abnormal_timber_transaction_knowledge`
* `sec4_1.market_price_identity_check_insufficient`
* `sec4_1.taxi_driver_no_presumption`

이 중 사례형 판례 카드는 일반 component로 직접 OR 연결하면 사실관계가 일부 유사하다는 이유로 요건 전체가 충족될 위험이 있습니다. `evidentiary_standard`를 `assessment_standard`의 subtype으로 두는 것이 좋습니다.

### `bar`로 이동

* `sec3_2.double_sale_real_estate`
* `sec3_2.property_interest`
* `sec3_2.extortion_attempt`
* `sec3_2.good_faith_third_party_fraud`
* `sec3_3.acquisition.account_withdrawal`
* `sec5_2.principal_excluded`
* `sec5_2.failed_principal_no_brokering`
* `sec5_2.real_estate_breach_of_trust`
* `sec5_2.oil_diversion_prior_agreement`

단, 각 bar는 전체 장물죄가 아니라 관련 행위태양 또는 장물성 component만 차단해야 합니다. 예컨대 `acquisition.account_withdrawal`은 장물취득 경로를 부정하는 것이지 장물보관·운반 등 다른 유형까지 모두 부정해서는 안 됩니다.

### `post_outcome`으로 이동

* `sec5_1.brokering_initial_transport_storage`
* `sec5_2.thief_fraudulent_sale`
* `sec6_2.storage_conviction_without_indictment_amendment`

`thief_fraudulent_sale`은 장물죄 component가 아니라 후속 사기죄의 독립 성립에 관한 죄수효과입니다. 장물을 비장물인 것처럼 속여 매도해 새로운 매수인의 법익을 침해한 경우 장물취득죄와 사기죄가 경합한다는 대법원 판례도 확인됩니다.

`storage_conviction_without_indictment_amendment`는 실체법 구성요건이 아니라 공소장변경 없이 인정 가능한 죄명 범위에 관한 절차법 카드이므로 `procedural_outcome`이 더 정확합니다.

### `proof_standard` 또는 별도 증명요건으로 이동

* `sec6_1.stolen_character_proof`

장물성이 명확히 증명되어야 한다는 명제는 구성요건 자체라기보다 유죄인정의 증명요건입니다. 이를 component로 두면 “명확히 증명되어야 한다는 법리가 참”이라는 이유로 장물성이 인정되는 역전이 발생합니다.

### 카드 분리 필요

* `sec3_2.foreign_offense`
* `sec3_3.transport.knowledge_midway`
* `sec3_3.custody.knowledge`

각 카드에 긍정 경로와 부정·예외 경로가 함께 들어 있습니다.

## E-02 `bar` 34장

판정: **X — 다수는 맞지만 최소 6장은 bar가 아님**

### bar 유지 가능

다음은 원칙적으로 bar가 적절합니다.

* `principal_offender_excluded`
* `co_principal_disposal_excluded`
* `special_robbery_conspirator_brokerage`
* `information_data`
* `computer_fraud_deposit_claim`
* `nominee_real_estate`
* `acquisitive_prescription`
* `temporary_use`
* `acquisition.predicate_completion`
* `acquisition.from_victim`
* `acquisition.account_holder_principal`
* `acquisition.shared_use`
* `transfer.to_victim`
* `transport.victim_return`
* `transport.bank_transfer`
* `no_later_knowledge_acquisition`
* `co_principal_excluded`
* `embezzlement_conspiracy`
* `breach_of_trust_no_receiving`
* `intent_concurrence_required`
* `secret_taking_against_principal`
* `defrauding_principal_no_receiving`
* `lost_property_embezzlement`

단, 죄 전체가 아니라 각각 관련 component 또는 행위태양에만 국소적으로 적용해야 합니다.

### variant로 이동

* `instigator_aider_acquisition_negative`
* `completion_theory`
* `embezzlement_purchaser_aiding`
* `voidable_transaction_negative`
* `illegal_cause_benefit_recovery_right`

대립 견해 카드가 기본 bar로 자동 발화하면 채택되지 않은 학설이 결론을 차단하게 됩니다.

### 카드 분리 필요

* `good_faith_acquisition`

  * 일반 선의취득으로 장물성 소멸
  * 도품·유실물 반환청구기간 중 장물성 유지
    를 분리해야 합니다.

* `accession_processing`

  * 동일성 유지 시 장물성 존속
  * 첨부로 제3자 소유권 취득 시 장물성 소멸
    을 분리해야 합니다.

* `breach_of_trust_bribe`

  * “배임죄는 원칙적으로 본범이 되기 어렵다”는 부정명제
  * “배임수재의 수증물이 재물이면 본범 가능”이라는 긍정명제
    를 분리해야 합니다.

### bar에서 제외하고 component 또는 requirement waiver로 이동

* `later_knowledge_transport_storage`

이 카드는 운반·보관 개시 후 장물성을 알게 된 경우에도 이후 계속행위에 죄가 성립할 수 있다는 **성립 긍정 법리**입니다. bar에 두면 배치 001과 동일한 극성 역전 사고가 발생합니다.

## E-03 `post_outcome` 22장

판정: **O — 단, 일부는 variant gate 필요**

> comment: 그룹의 성격은 대체로 적절합니다. 장물보관 후 임의처분이 별도 횡령죄를 구성하지 않는다는 대법원 판례도 명확합니다.

### 그대로 post_outcome 가능

* `nonprincipal_group_member_acquisition`
* `subsequent_participant`
* `used_to_defraud`
* `cashier_check_payment`
* `acquisition.subsequent_custody`
* `transport.acquirer_self_transport`
* `custody.embezzlement`
* `acquisition_transfer_nonpunishable_followup`
* `returned_property_later_brokering`
* `instigator_aider_concurrence`
* `storage_disposal_nonpunishable`
* `bribe_receipt_imaginary_concurrence`

### variant gate 필요

* `embezzlement_purchaser_concurrence`
* `transport_storage_inclusive_offense`
* `transport_storage_absorption`
* `later_brokering_concurrent_offenses`
* `pursuit_right_theory`
* `resale_fraud_nonpunishable`
* `acquisition_brokering_relationship`
* `storage_embezzlement_real_concurrence`
* `concealment_evidence_imaginary_concurrence`

이들은 선택된 견해가 있을 때만 post-outcome으로 발화해야 합니다.

### 분리 필요

* `resale_fraud_nonabsorption`

카드 설명은 “견해가 제시되어 있다”고 되어 있으므로 권위가 판례인지 학설인지 먼저 확정해야 합니다. 대법원은 적어도 장물임을 숨기고 제3자에게 매도하여 대금을 편취한 사안에서 새로운 법익침해를 이유로 사기죄와 장물취득죄의 경합을 인정한 바 있습니다.

## E-04 variant 22장

판정: **X — 지금 단계에서 견해 채택 후 컴파일하지 말 것**

> comment: 이 그룹은 하나의 정책으로 일괄 채택할 수 없습니다. `variant`는 역할이 아니라 **규범 선택 상태**입니다. 견해가 채택되지 않은 상태에서도 모델에게 학설 소개용으로는 전달할 수 있지만, symbolic conclusion에는 연결하면 안 됩니다.

권고 상태:

* `variant_status = unselected`
* `effect_on_conclusion = none`
* `available_views = [...]`
* 판례 견해가 명확한 경우에만 `default_selected_by_authority`
* 연구자가 특정 학설 체계를 채택한 경우 `selected_by_policy`

### 즉시 분리해야 하는 카드

* `acquisition.food_consumption`

  * 공동섭취 부정설
  * 단독섭취 긍정설
  * 소비 일반 긍정설

* `transfer.knowledge_and_subsequent_transfer`

  * 취득 당시 인식 필요 여부
  * 인식 후 양도의 별죄 여부
    는 서로 다른 논점입니다.

* `brokering.completion_doctrines`

  * 주선행위설
  * 계약성립설
  * 점유이전설

* `acquisition_brokering_relationship`

  * 경합범설
  * 상상적 경합설

한 카드 안에 여러 견해가 있으면 선택 relation이 카드 단위로 작동할 수 없습니다.

### 권위 확인 후 기본선택 가능 후보

* `embezzlement_purchaser_receiving`
* `brokering.completion_doctrines`
* `resale_fraud_concurrence`

다만 카드 문언의 “판례가 소개되어 있다”만으로 자동 선택하지 말고 판례번호와 판시사항을 직접 결박해야 합니다.

## E-05 `assessment_standard` 17장

판정: **O — 단, 3장은 다른 역할로 이동**

### assessment_standard 유지

* `conduct_types`
* `object_movable_property`
* `pursuit_right_definition`
* `illegal_state_definition`
* `acquisition_completion_theory`
* `substitute_property`
* `shopping_cart`
* `acquisition.definition`
* `acquisition.loan_for_use`
* `knowledge.conditional_intent`
* `transfer.definition`
* `transport.definition`
* `custody.definition`
* `brokering.definition`
* `inference_of_knowledge`
* `intent_concurrence_implied`

### `requirement_waived`로 이동

* `indictment_underlying_offense_unspecified`

이는 단순 정의라기보다 장물의 출처가 된 구체적 본범 죄명을 특정할 필요가 없다는 증명·특정요건 불요 법리입니다.

### 추가 주의

* `object_movable_property`의 문언이 “객체는 재물”이라면 카드 ID의 `movable_property`와 맞지 않습니다. 부동산도 일부 장물 행위태양의 객체가 될 수 있다는 내부 카드와 충돌할 수 있으므로 ID 또는 명제를 교정해야 합니다.
* `shopping_cart`는 일반 정의가 아니라 판례 사례형 증거판단이므로 `evidentiary_standard` subtype이 적합합니다.

## E-06 `waiver` 7장

판정: **O — 단, 2장은 variant gate, 1장은 proof requirement**

### waiver 유지

* `predicate_property_crime`
* `conditional_knowledge`
* `no_specific_principal_offense_knowledge`
* `knowledge_of_recovery_right`
* `principal_and_victim_identification_not_required`

### variant gate 필요

* `transport.completion`
* `no_independent_gain_intent`

학설 또는 필자 견해를 기본 waiver로 자동 적용하면 반대견해를 배제하게 됩니다.

### 역할 세분화 권고

`principal_and_victim_identification_not_required`는 실체적 주관요건 불요와 공소사실 특정·증명 불요가 혼동될 수 있습니다. 다음을 구분해야 합니다.

* 피고인이 본범자·피해자를 구체적으로 인식할 필요 없음
* 법원이 장물성을 인정하기 위해 본범자·피해자를 특정할 필요 없음
* 공소사실에 어느 정도 특정이 필요한지

동일한 카드로 처리하면 실체법과 절차법이 섞입니다.

---

# F. 장물죄 구조 설계

## F-01 cross-unit 흡수 구조

판정: **O — shared module 채택**

> comment: 제안한 (나)가 원칙적으로 맞습니다. 장물보관죄와 횡령죄의 결과를 호스트가 Python 조건문으로 조합하면, 최종 죄수결론은 Scallop이 아니라 호스트가 소유하게 됩니다.
>
> 대법원은 장물보관죄가 성립한 경우 이미 소유자의 추구권이 침해되므로 그 후 임의처분은 불가벌적 사후행위이고 별도 횡령죄가 성립하지 않는다고 봅니다.

### 권고 shared module

`property_crime_concurrence` 또는 `post_offense_absorption`

입력 bridge relation:

* `offense_established(case_id, actor_id, unit_id, act_id)`
* `offense_object(case_id, unit_id, property_id)`
* `act_time(case_id, act_id, time_order)`
* `custody_basis(case_id, actor_id, property_id, entrustor_id)`
* `same_property(property_id_1, property_id_2)`
* `later_disposal(case_id, actor_id, property_id)`
* `new_independent_victim(case_id, act_id, victim_id)`
* `new_independent_legal_interest(case_id, act_id)`

출력:

* `offense_absorbed(case_id, absorbed_unit, absorbing_unit, rule_id)`
* `punishment_suppressed(case_id, unit_id, reason)`
* `concurrence_outcome(case_id, type, units)`
* `post_offense_rule_fired(case_id, rule_id)`

장물보관 후 횡령 규칙 예시 의미:

* 동일 행위자
* 동일 재물
* 선행 장물보관죄 성립
* 후행 임의처분
* 새로운 독립 법익침해 없음
* 별도 횡령죄의 처벌 또는 독립 성립 출력 억제

### 중요한 정정

shared module은 각 유닛의 **구성요건 verdict를 소급 변경해서는 안 됩니다.**

가령 횡령죄의 추상적 구성요건이 충족된다고 평가되더라도 최종 결과는:

* `embezzlement_elements_satisfied = true`
* `embezzlement_separately_punishable = false`
* `reason = nonpunishable_post_offense`

처럼 구별하는 것이 좋습니다.

`embezzlement_not_established`로 덮어쓰면 구성요건 불성립과 불가벌적 사후행위를 혼동합니다.

### 호스트의 역할

호스트는 다음만 담당해야 합니다.

* 유닛 결과를 bridge fact로 직렬화
* shared SCL 실행
* shared module 결과 병합
* proof lineage 보존

법률 규칙 자체를 Python `if`로 계산해서는 안 됩니다.

## F-02 최종 역할 어휘

판정: **O — 단, 두 역할 추가 권고**

현재 여섯 역할은 기본 뼈대로 타당합니다.

추가 권고:

| 역할                | 뜻              | 결론 영향       |
| ----------------- | -------------- | ----------- |
| `proof_standard`  | 증명·특정 요건       | 유죄 인정 가능성   |
| `subtype_outcome` | 동일 유닛 내부 의율 유형 | 죄 전체 성립은 유지 |

또한 `post_outcome`은 하나의 자유문장 통이 아니라 최소한 다음 subtype을 가져야 합니다.

* `absorption`
* `nonpunishable_post_offense`
* `real_concurrence`
* `imaginary_concurrence`
* `inclusive_offense`
* `procedural_reclassification`
* `mitigation_unavailable`

## F-03 polarity/norm_kind 교정 범위

판정: **O**

> comment: 장물죄 16장은 적재 전에 바로 교정하고, 기존 룰베이스 142건은 별도 배치에서 전수검토하는 것이 현실적으로 타당합니다.
>
> 다만 기존 142건이 실행 중인 자산이라면 단순히 다음 배치로 미루기만 해서는 안 됩니다. 그 사이 오판을 방지하기 위해 activation gate를 두어야 합니다.

권고 임시 조치:

1. `polarity = exception`인 기존 카드 목록을 registry warning으로 노출
2. 해당 카드가 `bar` 또는 component로 자동 컴파일되는 경우 실행 차단
3. 수동 승인된 카드만 예외적으로 활성화
4. 별도 배치에서 `polarity`를 positive/negative로 복구
5. `norm_kind=exception`은 독립 유지

---

# 최종 결론

## 그대로 승인

* C-02
* D-02
* D-03
* D-04의 당장 `post_outcome` 처리
* D-05
* D-06
* D-07
* E-03의 역할 방향
* E-05의 대다수
* E-06의 역할 방향
* F-01 shared module
* F-02
* F-03

## 수정 후 승인

* C-01
* D-01
* E-01
* E-02
* E-04
* E-05 일부
* E-06 일부

## 가장 중요한 구현 원칙

1. `assessment_standard`는 생성 모델이 결론을 대신 내리게 하는 우회로가 되어서는 안 됩니다.
2. `component`의 OR 경로에는 실제 구성요건 충족 카드만 들어가야 합니다.
3. 부정 사례·판례 사례·증명기준·절차법 카드를 component에 섞어서는 안 됩니다.
4. variant는 역할이 아니라 선택 상태이며, 미선택 견해는 결론에 연결하지 않아야 합니다.
5. 불가벌적 사후행위는 본죄의 구성요건 불성립과 구별하여 `punishment_suppressed` 또는 별도 죄수결과로 표현해야 합니다.
6. cross-unit 죄수결론은 shared Scallop module이 계산하고 호스트는 bridge와 실행만 담당해야 합니다.
