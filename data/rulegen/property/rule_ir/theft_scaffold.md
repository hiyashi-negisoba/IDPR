# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.theft.full.v1_candidate`
- predicate: 220개
- rule: 351개
- NormCard: 66개

## Predicate

### `provable(case_id: String, assessment_id: String)`

해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `case_assessment_complete(case_id: String, defendant_id: String)`

라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `distinct_entity(case_id: String, left_entity_id: String, right_entity_id: String)`

두 역할에 배정된 entity가 서로 다른 사람임

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `theft_case_roles(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art329_sec2_theft_exception_ownership_or_self_possession(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

### `satisfied_art329_sec2_theft_exception_ownership_or_self_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

### `not_satisfied_satisfied_art329_sec2_theft_exception_ownership_or_self_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

### `assess_art329_sec2_theft_object_anothers_property_in_possession(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

### `satisfied_art329_sec2_theft_object_anothers_property_in_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

### `not_satisfied_satisfied_art329_sec2_theft_object_anothers_property_in_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

### `assess_art329_sec2_1_co_owned_property_taking(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_1.co_owned_property_taking`

### `satisfied_art329_sec2_1_co_owned_property_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.co_owned_property_taking`

### `not_satisfied_satisfied_art329_sec2_1_co_owned_property_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.co_owned_property_taking`

### `assess_art329_sec2_1_inherited_estate_not_ownerless(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

### `satisfied_art329_sec2_1_inherited_estate_not_ownerless(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

### `not_satisfied_satisfied_art329_sec2_1_inherited_estate_not_ownerless(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

### `assess_art329_sec2_1_other_person_legal_entity(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_1.other_person_legal_entity`

### `satisfied_art329_sec2_1_other_person_legal_entity(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.other_person_legal_entity`

### `not_satisfied_satisfied_art329_sec2_1_other_person_legal_entity(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.other_person_legal_entity`

### `assess_art329_sec2_1_ownerless_property_exception(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_1.ownerless_property_exception`

### `satisfied_art329_sec2_1_ownerless_property_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 절도죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.ownerless_property_exception`

### `not_satisfied_satisfied_art329_sec2_1_ownerless_property_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 무주물은 절도죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.ownerless_property_exception`

### `assess_art329_sec2_1_vehicle_internal_ownership_agreement(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

### `satisfied_art329_sec2_1_vehicle_internal_ownership_agreement(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

### `not_satisfied_satisfied_art329_sec2_1_vehicle_internal_ownership_agreement(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

### `assess_art329_sec2_2_carrier_control_based_possession(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

### `satisfied_art329_sec2_2_carrier_control_based_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

### `not_satisfied_satisfied_art329_sec2_2_carrier_control_based_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

### `assess_art329_sec2_2_clerk_subordinate_possession(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

### `satisfied_art329_sec2_2_clerk_subordinate_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

### `not_satisfied_satisfied_art329_sec2_2_clerk_subordinate_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

### `assess_art329_sec2_2_criminal_possession_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.criminal_possession_definition`

### `satisfied_art329_sec2_2_criminal_possession_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.criminal_possession_definition`

### `not_satisfied_satisfied_art329_sec2_2_criminal_possession_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.criminal_possession_definition`

### `assess_art329_sec2_2_dead_person_possession_continuing(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

### `satisfied_art329_sec2_2_dead_person_possession_continuing(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

### `not_satisfied_satisfied_art329_sec2_2_dead_person_possession_continuing(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

### `assess_art329_sec2_2_dead_person_possession_limited(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

### `satisfied_art329_sec2_2_dead_person_possession_limited(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

### `not_satisfied_satisfied_art329_sec2_2_dead_person_possession_limited(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

### `assess_art329_sec2_2_joint_custodian_unilateral_taking(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

### `satisfied_art329_sec2_2_joint_custodian_unilateral_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

### `not_satisfied_satisfied_art329_sec2_2_joint_custodian_unilateral_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

### `assess_art329_sec2_2_possession_assistant_control(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.possession_assistant_control`

### `satisfied_art329_sec2_2_possession_assistant_control(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_assistant_control`

### `not_satisfied_satisfied_art329_sec2_2_possession_assistant_control(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_assistant_control`

### `assess_art329_sec2_2_possession_control_and_intent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.possession_control_and_intent`

### `satisfied_art329_sec2_2_possession_control_and_intent(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_control_and_intent`

### `not_satisfied_satisfied_art329_sec2_2_possession_control_and_intent(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_control_and_intent`

### `assess_art329_sec2_2_possession_factual_control_standard(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

### `satisfied_art329_sec2_2_possession_factual_control_standard(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

### `not_satisfied_satisfied_art329_sec2_2_possession_factual_control_standard(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

### `assess_art329_sec2_2_possession_intent_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.possession_intent_definition`

### `satisfied_art329_sec2_2_possession_intent_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_intent_definition`

### `not_satisfied_satisfied_art329_sec2_2_possession_intent_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.possession_intent_definition`

### `assess_art329_sec2_2_property_in_managed_place(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.property_in_managed_place`

### `satisfied_art329_sec2_2_property_in_managed_place(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.property_in_managed_place`

### `not_satisfied_satisfied_art329_sec2_2_property_in_managed_place(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.property_in_managed_place`

### `assess_art329_sec2_2_sealed_deposit_entrustment_nature(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

### `satisfied_art329_sec2_2_sealed_deposit_entrustment_nature(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

### `not_satisfied_satisfied_art329_sec2_2_sealed_deposit_entrustment_nature(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

### `assess_art329_sec2_2_sole_custodian_coowned_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

### `satisfied_art329_sec2_2_sole_custodian_coowned_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

### `not_satisfied_satisfied_art329_sec2_2_sole_custodian_coowned_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

### `assess_art329_sec2_2_temporary_separation_possession(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.temporary_separation_possession`

### `satisfied_art329_sec2_2_temporary_separation_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.temporary_separation_possession`

### `not_satisfied_satisfied_art329_sec2_2_temporary_separation_possession(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.temporary_separation_possession`

### `assess_art329_sec2_2_unfound_transit_lost_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

### `satisfied_art329_sec2_2_unfound_transit_lost_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

### `not_satisfied_satisfied_art329_sec2_2_unfound_transit_lost_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

### `assess_art329_sec2_2_unlawful_possession_protected(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

### `satisfied_art329_sec2_2_unlawful_possession_protected(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

### `not_satisfied_satisfied_art329_sec2_2_unlawful_possession_protected(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

### `assess_art329_sec3_1_deceptive_taking_without_delivery(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

### `satisfied_art329_sec3_1_deceptive_taking_without_delivery(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

### `not_satisfied_satisfied_art329_sec3_1_deceptive_taking_without_delivery(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

### `assess_art329_sec3_1_taking_transfer_of_control(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

### `satisfied_art329_sec3_1_taking_transfer_of_control(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

### `not_satisfied_satisfied_art329_sec3_1_taking_transfer_of_control(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

### `assess_art329_sec3_3_completion_control_and_disposal(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

### `satisfied_art329_sec3_3_completion_control_and_disposal(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

### `not_satisfied_satisfied_art329_sec3_3_completion_control_and_disposal(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

### `assess_art329_sec3_3_completion_property_circumstances(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec3_3.completion.property_circumstances`

### `satisfied_art329_sec3_3_completion_property_circumstances(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_3.completion.property_circumstances`

### `not_satisfied_satisfied_art329_sec3_3_completion_property_circumstances(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_3.completion.property_circumstances`

### `assess_art329_sec4_intent_conditional_intent_sufficient(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

### `satisfied_art329_sec4_intent_conditional_intent_sufficient(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

### `not_satisfied_satisfied_art329_sec4_intent_conditional_intent_sufficient(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

### `assess_art329_sec4_intent_general_object_selection(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec4.intent.general_object_selection`

### `satisfied_art329_sec4_intent_general_object_selection(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.general_object_selection`

### `not_satisfied_satisfied_art329_sec4_intent_general_object_selection(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.general_object_selection`

### `assess_art329_sec4_intent_mistake_abandoned_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

### `satisfied_art329_sec4_intent_mistake_abandoned_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

### `not_satisfied_satisfied_art329_sec4_intent_mistake_abandoned_property(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

### `assess_art329_sec4_intent_theft_intent_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec4.intent.theft_intent_definition`

### `satisfied_art329_sec4_intent_theft_intent_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.theft_intent_definition`

### `not_satisfied_satisfied_art329_sec4_intent_theft_intent_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.theft_intent_definition`

### `assess_art329_sec5_1_unlawful_appropriation_required(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

### `satisfied_art329_sec5_1_unlawful_appropriation_required(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

### `not_satisfied_satisfied_art329_sec5_1_unlawful_appropriation_required(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

### `assess_art329_sec5_2_collateral_taking_unlawful_appropriation(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

### `satisfied_art329_sec5_2_collateral_taking_unlawful_appropriation(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

### `not_satisfied_satisfied_art329_sec5_2_collateral_taking_unlawful_appropriation(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

### `assess_art329_sec5_2_fuel_consumption_incidental_use(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

### `satisfied_art329_sec5_2_fuel_consumption_incidental_use(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

### `not_satisfied_satisfied_art329_sec5_2_fuel_consumption_incidental_use(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

### `assess_art329_sec5_2_use_theft_long_possession_or_abandonment(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

### `satisfied_art329_sec5_2_use_theft_long_possession_or_abandonment(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

### `not_satisfied_satisfied_art329_sec5_2_use_theft_long_possession_or_abandonment(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

### `assess_art329_sec5_2_use_theft_minor_value_consumption_and_prompt_return(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

### `satisfied_art329_sec5_2_use_theft_minor_value_consumption_and_prompt_return(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

### `not_satisfied_satisfied_art329_sec5_2_use_theft_minor_value_consumption_and_prompt_return(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

### `assess_art329_sec5_2_use_theft_possession_not_completely_lost(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

### `satisfied_art329_sec5_2_use_theft_possession_not_completely_lost(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

### `not_satisfied_satisfied_art329_sec5_2_use_theft_possession_not_completely_lost(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

### `assess_art329_sec5_2_use_theft_value_consumption_or_delayed_return(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `satisfied_art329_sec5_2_use_theft_value_consumption_or_delayed_return(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `not_satisfied_satisfied_art329_sec5_2_use_theft_value_consumption_or_delayed_return(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `assess_art329_sec6_consent_manifestation(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec6.consent_manifestation`

### `satisfied_art329_sec6_consent_manifestation(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec6.consent_manifestation`

### `not_satisfied_satisfied_art329_sec6_consent_manifestation(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec6.consent_manifestation`

### `assess_art329_sec6_consent_no_taking(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art329_sec6.consent_no_taking`

### `satisfied_art329_sec6_consent_no_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec6.consent_no_taking`

### `not_satisfied_satisfied_art329_sec6_consent_no_taking(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec6.consent_no_taking`

### `assess_art330_sec1_definition_nighttime_residential_trespass_theft(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

### `satisfied_art330_sec1_definition_nighttime_residential_trespass_theft(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

### `not_satisfied_satisfied_art330_sec1_definition_nighttime_residential_trespass_theft(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

### `assess_art330_sec1_variant_timing_entry_standard(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec1.variant.timing_entry_standard`

### `satisfied_art330_sec1_variant_timing_entry_standard(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec1.variant.timing_entry_standard`

### `not_satisfied_satisfied_art330_sec1_variant_timing_entry_standard(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec1.variant.timing_entry_standard`

### `assess_art330_sec2_nighttime_objective(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec2.nighttime.objective`

### `satisfied_art330_sec2_nighttime_objective(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간은 일몰 후부터 일출 전까지를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec2.nighttime.objective`

### `not_satisfied_satisfied_art330_sec2_nighttime_objective(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간은 일몰 후부터 일출 전까지를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec2.nighttime.objective`

### `assess_art330_sec3_restaurant_permitted_entry_no_intrusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

### `satisfied_art330_sec3_restaurant_permitted_entry_no_intrusion(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

### `not_satisfied_satisfied_art330_sec3_restaurant_permitted_entry_no_intrusion(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

### `assess_art330_sec4_entry_attempt_examples(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec4.entry_attempt_examples`

### `satisfied_art330_sec4_entry_attempt_examples(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec4.entry_attempt_examples`

### `not_satisfied_satisfied_art330_sec4_entry_attempt_examples(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec4.entry_attempt_examples`

### `assess_art330_sec4_entry_before_theft_commencement(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec4.entry_before_theft_commencement`

### `satisfied_art330_sec4_entry_before_theft_commencement(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec4.entry_before_theft_commencement`

### `not_satisfied_satisfied_art330_sec4_entry_before_theft_commencement(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec4.entry_before_theft_commencement`

### `assess_art330_sec5_completion_at_theft_completion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art330_sec5.completion-at-theft-completion`

### `satisfied_art330_sec5_completion_at_theft_completion(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec5.completion-at-theft-completion`

### `not_satisfied_satisfied_art330_sec5_completion_at_theft_completion(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec5.completion-at-theft-completion`

### `assess_art331_sec2_1_locking_device_building_part(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec2_1.locking-device-building-part`

### `satisfied_art331_sec2_1_locking_device_building_part(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_1.locking-device-building-part`

### `not_satisfied_satisfied_art331_sec2_1_locking_device_building_part(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_1.locking-device-building-part`

### `assess_art331_sec2_2_key_opening_special_theft_exception(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

### `satisfied_art331_sec2_2_key_opening_special_theft_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

### `not_satisfied_satisfied_art331_sec2_2_key_opening_special_theft_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

### `assess_art331_sec2_3_first_paragraph_completion_timing(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

### `satisfied_art331_sec2_3_first_paragraph_completion_timing(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

### `not_satisfied_satisfied_art331_sec2_3_first_paragraph_completion_timing(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

### `assess_art331_sec3_1_toy_gun_not_weapon_exception(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

### `satisfied_art331_sec3_1_toy_gun_not_weapon_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

### `not_satisfied_satisfied_art331_sec3_1_toy_gun_not_weapon_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

### `assess_art331_sec3_1_weapon_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec3_1.weapon_definition`

### `satisfied_art331_sec3_1_weapon_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.weapon_definition`

### `not_satisfied_satisfied_art331_sec3_1_weapon_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.weapon_definition`

### `assess_art331_sec3_1_weapon_objective_assessment(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

### `satisfied_art331_sec3_1_weapon_objective_assessment(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

### `not_satisfied_satisfied_art331_sec3_1_weapon_objective_assessment(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

### `assess_art331_sec3_2_carrying_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec3_2.carrying_definition`

### `satisfied_art331_sec3_2_carrying_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_2.carrying_definition`

### `not_satisfied_satisfied_art331_sec3_2_carrying_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_2.carrying_definition`

### `assess_art331_sec3_2_carrying_period_and_notice(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

### `satisfied_art331_sec3_2_carrying_period_and_notice(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

### `not_satisfied_satisfied_art331_sec3_2_carrying_period_and_notice(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

### `assess_art331_sec3_3_group_offense_scene_presence(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

### `satisfied_art331_sec3_3_group_offense_scene_presence(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

### `not_satisfied_satisfied_art331_sec3_3_group_offense_scene_presence(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

### `assess_art332_sec1_habitual_offender_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1.habitual_offender_definition`

### `satisfied_art332_sec1_habitual_offender_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1.habitual_offender_definition`

### `not_satisfied_satisfied_art332_sec1_habitual_offender_definition(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1.habitual_offender_definition`

### `assess_art332_sec1_1_aggregate_theft_types(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_1.aggregate_theft_types`

### `satisfied_art332_sec1_1_aggregate_theft_types(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.aggregate_theft_types`

### `not_satisfied_satisfied_art332_sec1_1_aggregate_theft_types(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.aggregate_theft_types`

### `assess_art332_sec1_1_different_offense_types(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_1.different_offense_types`

### `satisfied_art332_sec1_1_different_offense_types(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.different_offense_types`

### `not_satisfied_satisfied_art332_sec1_1_different_offense_types(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.different_offense_types`

### `assess_art332_sec1_1_habituality_same_type(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_1.habituality_same_type`

### `satisfied_art332_sec1_1_habituality_same_type(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.habituality_same_type`

### `not_satisfied_satisfied_art332_sec1_1_habituality_same_type(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_1.habituality_same_type`

### `assess_art332_sec1_2_habituality_not_repetition_alone(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

### `satisfied_art332_sec1_2_habituality_not_repetition_alone(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

### `not_satisfied_satisfied_art332_sec1_2_habituality_not_repetition_alone(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

### `assess_art332_sec1_2_habituality_totality_factors(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_2.habituality-totality-factors`

### `satisfied_art332_sec1_2_habituality_totality_factors(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.habituality-totality-factors`

### `not_satisfied_satisfied_art332_sec1_2_habituality_totality_factors(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.habituality-totality-factors`

### `assess_art332_sec1_2_incidental_or_economic_theft_exception(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

### `satisfied_art332_sec1_2_incidental_or_economic_theft_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

### `not_satisfied_satisfied_art332_sec1_2_incidental_or_economic_theft_exception(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

### `assess_art332_sec1_2_single_offense_past_history(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_2.single-offense-past-history`

### `satisfied_art332_sec1_2_single_offense_past_history(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.single-offense-past-history`

### `not_satisfied_satisfied_art332_sec1_2_single_offense_past_history(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_2.single-offense-past-history`

### `assess_art332_sec1_3_old_conviction_special_circumstances(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

### `satisfied_art332_sec1_3_old_conviction_special_circumstances(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

### `not_satisfied_satisfied_art332_sec1_3_old_conviction_special_circumstances(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

### `assess_art342_attempts_punishable(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art342.attempts_punishable`

### `satisfied_art342_attempts_punishable(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법 제329조 내지 제341조의 미수범은 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art342.attempts_punishable`

### `not_satisfied_satisfied_art342_attempts_punishable(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법 제329조 내지 제341조의 미수범은 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art342.attempts_punishable`

### `theft_object_ownership_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

객체 요건 중 타인 소유가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`

### `theft_object_possession_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

객체 요건 중 타인 점유가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`

### `theft_conduct_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`

### `theft_intent_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`

### `theft_appropriation_intent_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

주관적 요건 중 불법영득·이득의사가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `theft_completion_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`

### `theft_elements_satisfied(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `theft_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec6.consent_no_taking`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art332_sec1_1.different_offense_types`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.incidental-or-economic-theft-exception`

### `theft_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`, `art329_sec6.consent_manifestation`, `art329_sec6.consent_no_taking`, `art330_sec1.definition.nighttime_residential_trespass_theft`, `art330_sec1.variant.timing_entry_standard`, `art330_sec2.nighttime.objective`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art330_sec4.entry_attempt_examples`, `art330_sec4.entry_before_theft_commencement`, `art330_sec5.completion-at-theft-completion`, `art331_sec2_1.locking-device-building-part`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec2_3.first_paragraph_completion_timing`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art331_sec3_1.weapon_definition`, `art331_sec3_1.weapon_objective_assessment`, `art331_sec3_2.carrying_definition`, `art331_sec3_2.carrying_period_and_notice`, `art331_sec3_3.group_offense_scene_presence`, `art332_sec1.habitual_offender_definition`, `art332_sec1_1.aggregate_theft_types`, `art332_sec1_1.different_offense_types`, `art332_sec1_1.habituality_same_type`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.habituality-totality-factors`, `art332_sec1_2.incidental-or-economic-theft-exception`, `art332_sec1_2.single-offense-past-history`, `art332_sec1_3.old_conviction_special_circumstances`, `art342.attempts_punishable`

### `theft_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`, `art329_sec6.consent_manifestation`, `art329_sec6.consent_no_taking`, `art330_sec1.definition.nighttime_residential_trespass_theft`, `art330_sec1.variant.timing_entry_standard`, `art330_sec2.nighttime.objective`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art330_sec4.entry_attempt_examples`, `art330_sec4.entry_before_theft_commencement`, `art330_sec5.completion-at-theft-completion`, `art331_sec2_1.locking-device-building-part`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec2_3.first_paragraph_completion_timing`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art331_sec3_1.weapon_definition`, `art331_sec3_1.weapon_objective_assessment`, `art331_sec3_2.carrying_definition`, `art331_sec3_2.carrying_period_and_notice`, `art331_sec3_3.group_offense_scene_presence`, `art332_sec1.habitual_offender_definition`, `art332_sec1_1.aggregate_theft_types`, `art332_sec1_1.different_offense_types`, `art332_sec1_1.habituality_same_type`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.habituality-totality-factors`, `art332_sec1_2.incidental-or-economic-theft-exception`, `art332_sec1_2.single-offense-past-history`, `art332_sec1_3.old_conviction_special_circumstances`, `art342.attempts_punishable`

### `theft_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec6.consent_no_taking`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art332_sec1_1.different_offense_types`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.incidental-or-economic-theft-exception`

### `theft_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`, `art329_sec6.consent_manifestation`, `art329_sec6.consent_no_taking`, `art330_sec1.definition.nighttime_residential_trespass_theft`, `art330_sec1.variant.timing_entry_standard`, `art330_sec2.nighttime.objective`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art330_sec4.entry_attempt_examples`, `art330_sec4.entry_before_theft_commencement`, `art330_sec5.completion-at-theft-completion`, `art331_sec2_1.locking-device-building-part`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec2_3.first_paragraph_completion_timing`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art331_sec3_1.weapon_definition`, `art331_sec3_1.weapon_objective_assessment`, `art331_sec3_2.carrying_definition`, `art331_sec3_2.carrying_period_and_notice`, `art331_sec3_3.group_offense_scene_presence`, `art332_sec1.habitual_offender_definition`, `art332_sec1_1.aggregate_theft_types`, `art332_sec1_1.different_offense_types`, `art332_sec1_1.habituality_same_type`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.habituality-totality-factors`, `art332_sec1_2.incidental-or-economic-theft-exception`, `art332_sec1_2.single-offense-past-history`, `art332_sec1_3.old_conviction_special_circumstances`, `art342.attempts_punishable`

### `theft_established(case_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

### `theft_requirement_waived(case_id: String, defendant_id: String, issue_id: String, value: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec6.consent_manifestation`

### `theft_boundary_shift(case_id: String, defendant_id: String, issue_id: String, value: String)`

이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.unfound_transit_lost_property`

### `theft_refers_to_crime(case_id: String, defendant_id: String, crime_name: String)`

이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.unfound_transit_lost_property`

### `theft_aggravation(case_id: String, defendant_id: String, kind: String)`

가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`, `art330_sec1.variant.timing_entry_standard`, `art330_sec2.nighttime.objective`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art330_sec4.entry_attempt_examples`, `art330_sec4.entry_before_theft_commencement`, `art330_sec5.completion-at-theft-completion`, `art331_sec2_1.locking-device-building-part`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec2_3.first_paragraph_completion_timing`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art331_sec3_1.weapon_definition`, `art331_sec3_1.weapon_objective_assessment`, `art331_sec3_2.carrying_definition`, `art331_sec3_2.carrying_period_and_notice`, `art331_sec3_3.group_offense_scene_presence`, `art332_sec1.habitual_offender_definition`, `art332_sec1_1.aggregate_theft_types`, `art332_sec1_1.different_offense_types`, `art332_sec1_1.habituality_same_type`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.habituality-totality-factors`, `art332_sec1_2.incidental-or-economic-theft-exception`, `art332_sec1_2.single-offense-past-history`, `art332_sec1_3.old_conviction_special_circumstances`, `art342.attempts_punishable`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

## Rules

### `theft.art329_sec2.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_1.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.co_owned_property_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_1.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.co_owned_property_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_1.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.co_owned_property_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_1.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.co_owned_property_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_1.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_1.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_1.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_1.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_1.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.other_person_legal_entity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_1.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.other_person_legal_entity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_1.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.other_person_legal_entity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_1.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.other_person_legal_entity`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_1.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 절도죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.ownerless_property_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_1.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.ownerless_property_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_1.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.ownerless_property_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_1.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 무주물은 절도죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 절도죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.ownerless_property_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_1.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_1.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_1.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_1.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.criminal_possession_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.criminal_possession_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.criminal_possession_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.criminal_possession_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_assistant_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_assistant_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_assistant_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_assistant_control`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_control_and_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_control_and_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_control_and_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.015.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_control_and_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.016.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_intent_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_intent_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_intent_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.017.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.possession_intent_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.property_in_managed_place`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.property_in_managed_place`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.property_in_managed_place`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.018.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.property_in_managed_place`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.019.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.020.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.temporary_separation_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.temporary_separation_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.temporary_separation_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.021.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.temporary_separation_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.022.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2_2.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec2_2.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec2_2.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec2_2.card.023.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec3_1.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec3_1.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec3_1.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec3_1.card.024.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec3_1.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec3_1.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec3_1.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec3_1.card.025.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec3_3.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec3_3.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec3_3.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec3_3.card.026.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec3_3.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.property_circumstances`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec3_3.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.property_circumstances`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec3_3.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.property_circumstances`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec3_3.card.027.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec3_3.completion.property_circumstances`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec4.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec4.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec4.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec4.card.028.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec4.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.general_object_selection`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec4.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.general_object_selection`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec4.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.general_object_selection`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec4.card.029.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.general_object_selection`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec4.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec4.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec4.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec4.card.030.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec4.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.theft_intent_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec4.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.theft_intent_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec4.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.theft_intent_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec4.card.031.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec4.intent.theft_intent_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_1.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_1.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_1.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_1.card.032.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.033.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.034.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.035.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.036.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.037.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec5_2.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec5_2.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec5_2.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec5_2.card.038.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec6.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_manifestation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec6.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_manifestation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec6.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_manifestation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec6.card.039.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_manifestation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec6.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_no_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art329_sec6.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_no_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art329_sec6.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_no_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art329_sec6.card.040.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art329_sec6.consent_no_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec1.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec1.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec1.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec1.card.041.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec1.card.042.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.variant.timing_entry_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec1.card.042.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.variant.timing_entry_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec1.card.042.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.variant.timing_entry_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec1.card.042.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec1.variant.timing_entry_standard`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec2.card.043.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간은 일몰 후부터 일출 전까지를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec2.nighttime.objective`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec2.card.043.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec2.nighttime.objective`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec2.card.043.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec2.nighttime.objective`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec2.card.043.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간은 일몰 후부터 일출 전까지를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간은 일몰 후부터 일출 전까지를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec2.nighttime.objective`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec3.card.044.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec3.card.044.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec3.card.044.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec3.card.044.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec4.card.045.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_attempt_examples`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec4.card.045.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_attempt_examples`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec4.card.045.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_attempt_examples`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec4.card.045.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_attempt_examples`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec4.card.046.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_before_theft_commencement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec4.card.046.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_before_theft_commencement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec4.card.046.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_before_theft_commencement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec4.card.046.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec4.entry_before_theft_commencement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art330_sec5.card.047.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec5.completion-at-theft-completion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art330_sec5.card.047.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec5.completion-at-theft-completion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art330_sec5.card.047.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec5.completion-at-theft-completion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art330_sec5.card.047.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art330_sec5.completion-at-theft-completion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec2_1.card.048.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_1.locking-device-building-part`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec2_1.card.048.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_1.locking-device-building-part`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec2_1.card.048.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_1.locking-device-building-part`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec2_1.card.048.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_1.locking-device-building-part`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec2_2.card.049.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec2_2.card.049.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec2_2.card.049.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec2_2.card.049.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec2_3.card.050.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec2_3.card.050.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec2_3.card.050.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec2_3.card.050.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_1.card.051.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_1.card.051.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_1.card.051.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_1.card.051.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_1.card.052.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_1.card.052.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_1.card.052.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_1.card.052.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_1.card.053.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_1.card.053.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_1.card.053.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_1.card.053.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_2.card.054.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_2.card.054.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_2.card.054.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_2.card.054.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_2.card.055.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_2.card.055.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_2.card.055.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_2.card.055.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art331_sec3_3.card.056.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art331_sec3_3.card.056.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art331_sec3_3.card.056.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art331_sec3_3.card.056.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1.card.057.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1.habitual_offender_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1.card.057.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1.habitual_offender_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1.card.057.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1.habitual_offender_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1.card.057.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1.habitual_offender_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_1.card.058.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.aggregate_theft_types`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_1.card.058.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.aggregate_theft_types`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_1.card.058.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.aggregate_theft_types`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_1.card.058.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.aggregate_theft_types`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_1.card.059.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_1.card.059.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_1.card.059.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_1.card.059.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_1.card.060.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.habituality_same_type`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_1.card.060.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.habituality_same_type`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_1.card.060.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.habituality_same_type`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_1.card.060.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_1.habituality_same_type`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_2.card.061.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_2.card.061.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_2.card.061.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_2.card.061.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_2.card.062.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-totality-factors`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_2.card.062.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-totality-factors`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_2.card.062.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-totality-factors`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_2.card.062.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.habituality-totality-factors`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_2.card.063.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_2.card.063.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_2.card.063.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_2.card.063.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_2.card.064.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.single-offense-past-history`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_2.card.064.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.single-offense-past-history`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_2.card.064.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.single-offense-past-history`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_2.card.064.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_2.single-offense-past-history`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art332_sec1_3.card.065.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art332_sec1_3.card.065.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art332_sec1_3.card.065.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art332_sec1_3.card.065.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art342.card.066.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법 제329조 내지 제341조의 미수범은 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art342.attempts_punishable`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `theft.art342.card.066.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art342.attempts_punishable`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `theft.art342.card.066.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art342.attempts_punishable`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `theft.art342.card.066.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법 제329조 내지 제341조의 미수범은 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제329조 내지 제341조의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art342.attempts_punishable`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `theft.art329_sec2.component.theft_object_ownership_satisfied.01`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_1.component.theft_object_ownership_satisfied.02`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.

연결 NormCard: `art329_sec2_1.co_owned_property_taking`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_1.component.theft_object_ownership_satisfied.03`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.

연결 NormCard: `art329_sec2_1.inherited_estate_not_ownerless`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_1.component.theft_object_ownership_satisfied.04`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.

연결 NormCard: `art329_sec2_1.other_person_legal_entity`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_1.component.theft_object_ownership_satisfied.05`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.

연결 NormCard: `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.01`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.02`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.

연결 NormCard: `art329_sec2_2.clerk_subordinate_possession`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.03`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.

연결 NormCard: `art329_sec2_2.criminal_possession_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.04`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.

연결 NormCard: `art329_sec2_2.dead_person_possession_continuing`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.05`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.

연결 NormCard: `art329_sec2_2.dead_person_possession_limited`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.06`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.

연결 NormCard: `art329_sec2_2.joint_custodian_unilateral_taking`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.07`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.

연결 NormCard: `art329_sec2_2.possession_assistant_control`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.08`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.

연결 NormCard: `art329_sec2_2.possession_control_and_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.09`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.

연결 NormCard: `art329_sec2_2.possession_factual_control_standard`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.10`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.

연결 NormCard: `art329_sec2_2.possession_intent_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.11`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.

연결 NormCard: `art329_sec2_2.property_in_managed_place`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.12`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.

연결 NormCard: `art329_sec2_2.sealed_deposit_entrustment_nature`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.13`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.

연결 NormCard: `art329_sec2_2.temporary_separation_possession`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2_2.component.theft_object_possession_satisfied.14`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.

연결 NormCard: `art329_sec2_2.unlawful_possession_protected`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec3_1.component.theft_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec3_1.component.theft_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.

연결 NormCard: `art329_sec3_1.taking_transfer_of_control`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec4.component.theft_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec4.component.theft_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.

연결 NormCard: `art329_sec4.intent.general_object_selection`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec4.component.theft_intent_satisfied.03`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.

연결 NormCard: `art329_sec4.intent.theft_intent_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec5_1.component.theft_appropriation_intent_satisfied.01`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec5_2.component.theft_appropriation_intent_satisfied.02`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.

연결 NormCard: `art329_sec5_2.collateral_taking_unlawful_appropriation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec5_2.component.theft_appropriation_intent_satisfied.03`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.

연결 NormCard: `art329_sec5_2.use_theft_long_possession_or_abandonment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec5_2.component.theft_appropriation_intent_satisfied.04`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.

연결 NormCard: `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec3_3.component.theft_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec3_3.component.theft_completion_satisfied.02`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.

연결 NormCard: `art329_sec3_3.completion.property_circumstances`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `theft.art329_sec2.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 소유 재물이 타인 점유 아래 있거나 타인 소유 재물이 자기 점유 아래 있는 경우에는, 권리행사방해죄 또는 횡령죄 성립 여부는 별론으로 하고 절도죄는 성립하지 않는다.

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec2_1.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 절도죄의 객체가 될 수 없다.

연결 NormCard: `art329_sec2_1.ownerless_property_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec2_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec2_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec4.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인이 소유권을 포기하여 버린 물건이라고 오인하여 취득한 경우에는 절도죄의 고의가 인정되지 않는다.

연결 NormCard: `art329_sec4.intent.mistake_abandoned_property`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec5_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.

연결 NormCard: `art329_sec5_2.fuel_consumption_incidental_use`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec5_2.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 무단사용으로 인한 가치 소모가 무시할 수 있을 정도로 경미하고 사용 후 곧 반환한 경우에는 소유권 또는 본권 침해 의사를 인정할 수 없어 불법영득의사가 인정되지 않는다.

연결 NormCard: `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec5_2.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.

연결 NormCard: `art329_sec5_2.use_theft_possession_not_completely_lost`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art329_sec6.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.

연결 NormCard: `art329_sec6.consent_no_taking`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art330_sec3.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art331_sec2_2.bar.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art331_sec3_1.bar.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art332_sec1_1.bar.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art332_sec1_2.bar.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.art332_sec1_2.bar.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `theft.component.l0o.mandatory_negative.01`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공유자 중 1인이 다른 공유자 또는 제3자가 점유하는 공유물을 임의로 탈취하면 절도죄가 성립하며, 합유물과 총유물도 같다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 피상속인 사망 후 상속인이 없는 상속재산은 국가에 귀속하므로 무주물이 아니다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 자동차 등의 등록명의자가 아닌 자라도 당사자 사이에 그 자가 소유권을 보유하기로 한 특별한 약정이 있으면 내부관계에서는 소유권을 보유할 수 있다.

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`

검토 메모: 구성요건 L0o에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.component.l0p.mandatory_negative.02`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, 그것이 불가능하면 운반자의 단독점유가 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점원이 주인의 지시·감독 아래 기계적 보조자로 상품을 감수하는 데 그치는 경우 점원은 형법상 점유자가 아니므로, 점원이 상품을 독점적 점유 아래 옮기면 횡령죄가 아니라 절도죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 재물에 대한 현실적이고 순수한 사실상 지배관계이며 민법상 점유와 반드시 일치하지 않는다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 재물을 탈취하는 행위는 사자의 점유를 침해한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 사자의 점유는 침해행위 전체의 형법상 효과와 구체적 사실 및 현실적 사회관념을 종합하여, 사망 직후에도 피해자 점유를 계속 보호하는 것이 부합하는 경우에만 인정되며 사망 후 상당 시간이 지난 사체나 소지물까지 계속되는 것은 아니다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공동보관자 중 1인이 다른 공동보관자의 동의 없이 불법영득의사로 재물을 공동보관 상태에서 자신의 단독점유로 옮기면 절도죄를 구성한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, 본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법상 점유에는 사실상의 지배라는 물리적 요소와 점유의 의사라는 정신적 요소가 필요하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법상 재물의 사실상 지배 여부는 재물의 크기·형상·개성 및 점유자와 재물의 시간적·장소적 관계 등을 종합하여 사회통념에 따라 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 물건을 방치한 장소가 타인의 관리 아래 있으면 그 물건은 관리자의 점유에 속하므로 제3자의 취거는 점유이탈물횡령이 아니라 절도에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 수치인에게 점유가 이전된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 물건이 일시적으로 소지 또는 감수에서 벗어나도 사회통념상 점유자의 실력적 지배 아래 있으면 점유는 유지된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유는 적법한 권원에 기초할 필요가 없고, 권원 없는 자라도 현실적 실력지배가 있으면 그 점유는 절도죄의 객체로 보호된다.

연결 NormCard: `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`

검토 메모: 구성요건 L0p에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.component.l1.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다.

연결 NormCard: `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.component.l3.mandatory_negative.04`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 직접적 고의일 필요가 없고 미필적 고의로도 충분하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 주거에 침입하여 훔칠 만한 물건이 있으면 무엇이든 훔치겠다는 일반적 인식으로 물색한 경우에도 절도죄의 고의가 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다.

연결 NormCard: `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`

검토 메모: 구성요건 L3에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.component.l3a.mandatory_negative.05`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 일시사용 목적으로 점유를 침탈했더라도 반환 의사 없이 상당한 장시간 점유하거나 원래 장소와 다른 곳에 유기한 경우에는 일시사용으로 볼 수 없어 불법영득의사가 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 타인의 물건을 무단사용하여 물건 자체의 경제적 가치가 상당히 소모되거나, 사용 후 다른 곳에 버리거나, 곧 반환하지 않고 장시간 점유한 경우에는 소유권 또는 본권 침해 의사가 인정되어 불법영득의사가 인정될 수 있다.

연결 NormCard: `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 구성요건 L3a에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.component.l4.mandatory_negative.06`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다.

연결 NormCard: `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`

검토 메모: 구성요건 L4에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `theft.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체 요건 중 타인 소유가 인정됨
- 객체 요건 중 타인 점유가 인정됨
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의
- 주관적 요건 중 불법영득·이득의사가 인정됨
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `theft.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec6.consent_no_taking`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art332_sec1_1.different_offense_types`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `theft.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art329_sec2.theft_exception_ownership_or_self_possession`, `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.ownerless_property_exception`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.sole_custodian_coowned_property`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unfound_transit_lost_property`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.mistake_abandoned_property`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.fuel_consumption_incidental_use`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_minor_value_consumption_and_prompt_return`, `art329_sec5_2.use_theft_possession_not_completely_lost`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`, `art329_sec6.consent_manifestation`, `art329_sec6.consent_no_taking`, `art330_sec1.definition.nighttime_residential_trespass_theft`, `art330_sec1.variant.timing_entry_standard`, `art330_sec2.nighttime.objective`, `art330_sec3.restaurant_permitted_entry_no_intrusion`, `art330_sec4.entry_attempt_examples`, `art330_sec4.entry_before_theft_commencement`, `art330_sec5.completion-at-theft-completion`, `art331_sec2_1.locking-device-building-part`, `art331_sec2_2.key-opening-special-theft-exception`, `art331_sec2_3.first_paragraph_completion_timing`, `art331_sec3_1.toy_gun_not_weapon_exception`, `art331_sec3_1.weapon_definition`, `art331_sec3_1.weapon_objective_assessment`, `art331_sec3_2.carrying_definition`, `art331_sec3_2.carrying_period_and_notice`, `art331_sec3_3.group_offense_scene_presence`, `art332_sec1.habitual_offender_definition`, `art332_sec1_1.aggregate_theft_types`, `art332_sec1_1.different_offense_types`, `art332_sec1_1.habituality_same_type`, `art332_sec1_2.habituality-not-repetition-alone`, `art332_sec1_2.habituality-totality-factors`, `art332_sec1_2.incidental-or-economic-theft-exception`, `art332_sec1_2.single-offense-past-history`, `art332_sec1_3.old_conviction_special_circumstances`, `art342.attempts_punishable`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `theft.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `theft.art329_sec6.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다.

연결 NormCard: `art329_sec6.consent_manifestation`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `theft.art329_sec2_2.boundary_shift.001`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `theft.art329_sec2_2.boundary_shift.002`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `theft.art329_sec2_2.refers_to_crime.001`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공동소유 재물이라도 공동점유가 아니라 공동소유자 중 1인의 단독보관 아래 있으면 그 보관자의 영득은 절도가 아니라 횡령에 해당한다.

연결 NormCard: `art329_sec2_2.sole_custodian_coowned_property`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `theft.art329_sec2_2.refers_to_crime.002`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 고속버스 운전사나 지하철 승무원은 승객이 두고 내린 유실물을 현실적으로 발견하기 전에는 점유를 개시하지 않으므로, 다른 승객이 발견하여 가져가면 절도가 아니라 점유이탈물횡령에 해당한다.

연결 NormCard: `art329_sec2_2.unfound_transit_lost_property`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `theft.aggravation.attempt.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 형법 제329조 내지 제341조의 미수범은 처벌된다.

연결 NormCard: `art342.attempts_punishable`

검토 메모: 기본범이 성립한 위에 attempt 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 상습범은 범행을 반복누행하는 습벽을 가진 자를 말한다.

연결 NormCard: `art332_sec1.habitual_offender_definition`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 단순절도, 야간주거침입절도 및 특수절도는 모두 동종의 절도행위이므로, 해당 죄나 미수죄를 범한 경우 각 죄별 상습성을 따로 인정하지 않고 포괄하여 하나의 상습범이 성립한다.

연결 NormCard: `art332_sec1_1.aggregate_theft_types`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.

연결 NormCard: `art332_sec1_1.different_offense_types`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 상습성은 동종 형태의 행위를 반복누행하는 습벽을 의미한다.

연결 NormCard: `art332_sec1_1.habituality_same_type`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절도의 상습성은 수회의 절도행위 반복만으로 바로 인정되지 않고, 반복누행을 통하여 절도 습벽이 발현된 경우에만 인정된다.

연결 NormCard: `art332_sec1_2.habituality-not-repetition-alone`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절도 습벽은 행위자의 연령·성격·직업·환경·전과와 범행의 동기·수단·방법·장소, 시간 간격, 범행 내용 및 유사성 등 여러 사정을 종합하여 판단한다.

연결 NormCard: `art332_sec1_2.habituality-totality-factors`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 수회의 절도 전과 또는 절도행위가 있어도 모두 우발적 동기 또는 급박한 경제사정에서 비롯되어 평소 절도 습성의 발현으로 보기 어려우면 상습범으로 볼 수 없다.

연결 NormCard: `art332_sec1_2.incidental-or-economic-theft-exception`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.008`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 문제된 범행이 1회여도 과거 범행경력에 비추어 절도 습벽이 인정되면 상습범이 성립할 수 있다.

연결 NormCard: `art332_sec1_2.single-offense-past-history`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.habitual.009`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 장기간 경과한 전과를 근거로 상습성을 인정하려면 그 전과와 종합하여 현재 범행이 절도 습벽의 발로라고 인정할 특별한 사정이 있어야 한다.

연결 NormCard: `art332_sec1_3.old_conviction_special_circumstances`

검토 메모: 기본범이 성립한 위에 habitual 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하여 타인의 재물을 절취함으로써 성립하는 범죄이다.

연결 NormCard: `art330_sec1.definition.nighttime_residential_trespass_theft`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 절취가 주간에 이루어진 경우에도 성립한다.

연결 NormCard: `art330_sec1.variant.timing_entry_standard`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간은 일몰 후부터 일출 전까지를 의미한다.

연결 NormCard: `art330_sec2.nighttime.objective`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 방법으로 출입한 경우, 범죄 목적이나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.

연결 NormCard: `art330_sec3.restaurant_permitted_entry_no_intrusion`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 주거침입이 완성되지 않고 주거침입행위의 실행에 착수한 단계에 그친 경우에도 야간주거침입절도죄의 실행에 착수한 것으로 본다.

연결 NormCard: `art330_sec4.entry_attempt_examples`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 착수한 것으로 본다.

연결 NormCard: `art330_sec4.entry_before_theft_commencement`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.nighttime_residential.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입절도죄의 기수시기는 절취행위를 완료한 때이다.

연결 NormCard: `art330_sec5.completion-at-theft-completion`

검토 메모: 기본범이 성립한 위에 nighttime_residential 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 주거 등에의 침입을 막기 위해 문에 장치한 잠금장치 등 통상적인 방법으로 문을 쉽게 열 수 없게 한 시설물도 건조물 일부로 본다.

연결 NormCard: `art331_sec2_1.locking-device-building-part`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간에 잠금장치를 훼손하지 않고 열쇠 등으로 통상의 용법에 따라 열고 침입한 경우에는 특수절도죄가 성립하지 않고 야간주거침입절도죄에 해당한다.

연결 NormCard: `art331_sec2_2.key-opening-special-theft-exception`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제1항 위반죄의 기수 시기는 절취행위가 완료한 때이다.

연결 NormCard: `art331_sec2_3.first_paragraph_completion_timing`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 흉기의 성질을 가져야 하므로 장난감 권총을 흉기처럼 가장한 경우에는 흉기가 아니다.

연결 NormCard: `art331_sec3_1.toy_gun_not_weapon_exception`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 제331조 제2항의 흉기는 본래 살상용·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건이다.

연결 NormCard: `art331_sec3_1.weapon_definition`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 물건이 흉기에 해당하는지는 본래 용도, 크기·모양, 개조 여부 및 구체적 범행과정에서의 사용 방법 등을 종합하여 사회통념에 따라 객관적으로 판단한다.

연결 NormCard: `art331_sec3_1.weapon_objective_assessment`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 휴대는 몸 가까이에 소지하는 것을 말하며, 즉시 사용할 수 있을 정도로 가까우면 반드시 몸에 지니지 않아도 된다.

연결 NormCard: `art331_sec3_2.carrying_definition`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.008`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절취행위의 개시부터 종료까지 어느 시점에 휴대가 인정되면 충분하고, 휴대 사실을 공연히 표시할 필요는 없다.

연결 NormCard: `art331_sec3_2.carrying_period_and_notice`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.aggravation.special.009`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 공모자는 합동범이 되지 않는다.

연결 NormCard: `art331_sec3_3.group_offense_scene_presence`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `theft.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art329_sec2.theft_object_anothers_property_in_possession`, `art329_sec2_1.co_owned_property_taking`, `art329_sec2_1.inherited_estate_not_ownerless`, `art329_sec2_1.other_person_legal_entity`, `art329_sec2_1.vehicle_internal_ownership_agreement`, `art329_sec2_2.carrier_control_based_possession`, `art329_sec2_2.clerk_subordinate_possession`, `art329_sec2_2.criminal_possession_definition`, `art329_sec2_2.dead_person_possession_continuing`, `art329_sec2_2.dead_person_possession_limited`, `art329_sec2_2.joint_custodian_unilateral_taking`, `art329_sec2_2.possession_assistant_control`, `art329_sec2_2.possession_control_and_intent`, `art329_sec2_2.possession_factual_control_standard`, `art329_sec2_2.possession_intent_definition`, `art329_sec2_2.property_in_managed_place`, `art329_sec2_2.sealed_deposit_entrustment_nature`, `art329_sec2_2.temporary_separation_possession`, `art329_sec2_2.unlawful_possession_protected`, `art329_sec3_1.deceptive_taking_without_delivery`, `art329_sec3_1.taking_transfer_of_control`, `art329_sec3_3.completion.control_and_disposal`, `art329_sec3_3.completion.property_circumstances`, `art329_sec4.intent.conditional_intent_sufficient`, `art329_sec4.intent.general_object_selection`, `art329_sec4.intent.theft_intent_definition`, `art329_sec5_1.unlawful_appropriation_required`, `art329_sec5_2.collateral_taking_unlawful_appropriation`, `art329_sec5_2.use_theft_long_possession_or_abandonment`, `art329_sec5_2.use_theft_value_consumption_or_delayed_return`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
