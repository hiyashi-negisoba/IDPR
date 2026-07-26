# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.extortion.full.v1_candidate`
- predicate: 102개
- rule: 204개
- NormCard: 41개

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

### `extortion_case_roles(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art350_sec1_defective_disposition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec1.defective_disposition`

### `satisfied_art350_sec1_defective_disposition(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`

### `assess_art350_sec1_extortion_definition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec1.extortion_definition`

### `satisfied_art350_sec1_extortion_definition(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.extortion_definition`

### `assess_art350_sec3_object(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec3.object`

### `satisfied_art350_sec3_object(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.object`

### `assess_art350_sec3_own_property_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec3.own_property_exception`

### `satisfied_art350_sec3_own_property_exception(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.own_property_exception`

### `assess_art350_sec3_possessed_property_object_affirmative(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

### `satisfied_art350_sec3_possessed_property_object_affirmative(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

### `assess_art350_sec3_real_estate_object(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec3.real_estate_object`

### `satisfied_art350_sec3_real_estate_object(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산도 공갈죄의 객체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.real_estate_object`

### `assess_art350_sec4_1_means_threat_or_violence(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec4_1.means_threat_or_violence`

### `satisfied_art350_sec4_1_means_threat_or_violence(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.means_threat_or_violence`

### `assess_art350_sec4_1_objective_fear_assessment(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_1.objective_fear_assessment`

### `satisfied_art350_sec4_1_objective_fear_assessment(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.objective_fear_assessment`

### `assess_art350_sec4_1_objectively_insufficient_threat(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

### `satisfied_art350_sec4_1_objectively_insufficient_threat(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

### `assess_art350_sec4_1_robbery_boundary(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_1.robbery_boundary`

### `satisfied_art350_sec4_1_robbery_boundary(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.robbery_boundary`

### `assess_art350_sec4_2_actual_intent_or_feasibility_not_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

### `satisfied_art350_sec4_2_actual_intent_or_feasibility_not_required(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

### `assess_art350_sec4_2_implied_or_indirect_threat(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

### `satisfied_art350_sec4_2_implied_or_indirect_threat(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

### `assess_art350_sec4_2_right_exercise_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_2.right_exercise_exception`

### `satisfied_art350_sec4_2_right_exercise_exception(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.right_exercise_exception`

### `assess_art350_sec4_2_third_party_harm_notice(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_2.third_party_harm_notice`

### `satisfied_art350_sec4_2_third_party_harm_notice(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.third_party_harm_notice`

### `assess_art350_sec4_2_threat_definition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_2.threat_definition`

### `satisfied_art350_sec4_2_threat_definition(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.threat_definition`

### `assess_art350_sec4_2_threat_to_third_party(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_2.threat_to_third_party`

### `satisfied_art350_sec4_2_threat_to_third_party(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.threat_to_third_party`

### `assess_art350_sec4_4_separate_victim_disposition_authority(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

### `satisfied_art350_sec4_4_separate_victim_disposition_authority(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

### `assess_art350_sec4_4_victim_capacity(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec4_4.victim_capacity`

### `satisfied_art350_sec4_4_victim_capacity(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_4.victim_capacity`

### `assess_art350_sec5_1_threat_fear_disposition_gain(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

### `satisfied_art350_sec5_1_threat_fear_disposition_gain(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

### `assess_art350_sec5_2_fear_causation_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_2.fear_causation_required`

### `satisfied_art350_sec5_2_fear_causation_required(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_2.fear_causation_required`

### `assess_art350_sec5_2_no_fear_attempt(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_2.no_fear_attempt`

### `satisfied_art350_sec5_2_no_fear_attempt(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_2.no_fear_attempt`

### `assess_art350_sec5_2_preexisting_fear_maintained(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

### `satisfied_art350_sec5_2_preexisting_fear_maintained(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

### `assess_art350_sec5_3_complete_suppression_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

### `satisfied_art350_sec5_3_complete_suppression_robbery(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

### `assess_art350_sec5_3_delivery_tacit_acquiescence(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

### `satisfied_art350_sec5_3_delivery_tacit_acquiescence(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

### `assess_art350_sec5_3_third_party_receipt_relationship(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

### `satisfied_art350_sec5_3_third_party_receipt_relationship(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

### `assess_art350_sec6_no_overall_property_decrease(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec6.no_overall_property_decrease`

### `satisfied_art350_sec6_no_overall_property_decrease(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec6.no_overall_property_decrease`

### `assess_art350_sec6_2_consideration_does_not_negate_extortion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

### `satisfied_art350_sec6_2_consideration_does_not_negate_extortion(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

### `assess_art350_sec6_2_satisfied_consideration_causation_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

### `satisfied_art350_sec6_2_satisfied_consideration_causation_exception(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

### `assess_art350_sec7_1_attempt_threat_notification(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec7_1.attempt_threat_notification`

### `satisfied_art350_sec7_1_attempt_threat_notification(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec7_1.attempt_threat_notification`

### `assess_art350_sec7_2_completion_fear_disposition_causal_link(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

### `satisfied_art350_sec7_2_completion_fear_disposition_causal_link(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

### `assess_art350_sec7_3_completion_bank_transfer(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec7_3.completion.bank_transfer`

### `satisfied_art350_sec7_3_completion_bank_transfer(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec7_3.completion.bank_transfer`

### `assess_art350_sec7_3_completion_property_and_benefit(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

### `satisfied_art350_sec7_3_completion_property_and_benefit(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

### `assess_art350_sec8_1_right_enforcement_method_standard(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

### `satisfied_art350_sec8_1_right_enforcement_method_standard(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

### `assess_art350_sec8_2_extortion_loss_despite_payment_duty(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

### `satisfied_art350_sec8_2_extortion_loss_despite_payment_duty(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

### `assess_art350_sec8_2_no_right_extortion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.no_right_extortion`

### `satisfied_art350_sec8_2_no_right_extortion(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.no_right_extortion`

### `assess_art350_sec8_2_permissible_range_purpose_means(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

### `satisfied_art350_sec8_2_permissible_range_purpose_means(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

### `assess_art350_sec8_2_permitted_threat_no_extortion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

### `satisfied_art350_sec8_2_permitted_threat_no_extortion(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

### `assess_art350_sec8_2_right_exercise_total_assessment(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

### `satisfied_art350_sec8_2_right_exercise_total_assessment(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

### `assess_art350_sec8_2_rightful_claim_excessive_method(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

### `satisfied_art350_sec8_2_rightful_claim_excessive_method(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

### `assess_art350_sec9_illicit_gain_intent_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec9.illicit_gain_intent.required`

### `satisfied_art350_sec9_illicit_gain_intent_required(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec9.illicit_gain_intent.required`

### `assess_art350_sec9_intent_objective_elements(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art350_sec9.intent.objective_elements`

### `satisfied_art350_sec9_intent_objective_elements(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec9.intent.objective_elements`

### `extortion_object_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.rightful_claim_excessive_method`

### `extortion_conduct_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.permissible_range_purpose_means`

### `extortion_causation_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

행위와 결과의 연결(인과·귀속)이 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

### `extortion_intent_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_completion_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`

### `extortion_elements_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.own_property_exception`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.right_exercise_exception`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`

### `extortion_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.own_property_exception`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.actual_intent_or_feasibility_not_required`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.right_exercise_exception`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6.no_overall_property_decrease`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.own_property_exception`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.actual_intent_or_feasibility_not_required`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.right_exercise_exception`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6.no_overall_property_decrease`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec3.own_property_exception`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.right_exercise_exception`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`

### `extortion_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.own_property_exception`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.actual_intent_or_feasibility_not_required`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.right_exercise_exception`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6.no_overall_property_decrease`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_established(case_id: String, defendant_id: String, coerced_person_id: String, disposer_id: String, owner_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

### `extortion_requirement_waived(case_id: String, defendant_id: String, issue_id: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`, `art350_sec6.no_overall_property_decrease`

### `extortion_boundary_shift(case_id: String, defendant_id: String, issue_id: String)`

이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec5_3.complete_suppression_robbery`

### `extortion_refers_to_crime(case_id: String, defendant_id: String, crime_name: String)`

이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec5_3.complete_suppression_robbery`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

## Rules

### `extortion.art350_sec1.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.defective_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec1.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.defective_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec1.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.defective_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec1.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.extortion_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec1.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.extortion_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec1.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.extortion_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec3.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec3.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec3.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec3.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.own_property_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec3.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.own_property_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec3.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.own_property_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec3.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec3.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec3.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec3.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산도 공갈죄의 객체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.real_estate_object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec3.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.real_estate_object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec3.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.real_estate_object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_1.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.means_threat_or_violence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_1.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.means_threat_or_violence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_1.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.means_threat_or_violence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_1.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objective_fear_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_1.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objective_fear_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_1.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objective_fear_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_1.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_1.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_1.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_1.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_1.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_1.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.right_exercise_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.right_exercise_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.right_exercise_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.third_party_harm_notice`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.third_party_harm_notice`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.third_party_harm_notice`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_2.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_to_third_party`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_2.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_to_third_party`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_2.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_to_third_party`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_4.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_4.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_4.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec4_4.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.victim_capacity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec4_4.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.victim_capacity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec4_4.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.victim_capacity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_1.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_1.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_1.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_2.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.fear_causation_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_2.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.fear_causation_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_2.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.fear_causation_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_2.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.no_fear_attempt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_2.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.no_fear_attempt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_2.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.no_fear_attempt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_2.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_2.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_2.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_3.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_3.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_3.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_3.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_3.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_3.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec5_3.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec5_3.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec5_3.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec6.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6.no_overall_property_decrease`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec6.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6.no_overall_property_decrease`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec6.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6.no_overall_property_decrease`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec6_2.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec6_2.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec6_2.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec6_2.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec6_2.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec6_2.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec7_1.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_1.attempt_threat_notification`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec7_1.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_1.attempt_threat_notification`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec7_1.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_1.attempt_threat_notification`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec7_2.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec7_2.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec7_2.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec7_3.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.bank_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec7_3.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.bank_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec7_3.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.bank_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec7_3.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec7_3.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec7_3.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_1.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_1.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_1.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.no_right_extortion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.no_right_extortion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.no_right_extortion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec8_2.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec8_2.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec8_2.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec9.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.illicit_gain_intent.required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec9.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.illicit_gain_intent.required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec9.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.illicit_gain_intent.required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec9.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.intent.objective_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `extortion.art350_sec9.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.intent.objective_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `extortion.art350_sec9.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.intent.objective_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `extortion.art350_sec3.component.extortion_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.

연결 NormCard: `art350_sec3.object`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec3.component.extortion_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.

연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec3.component.extortion_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산도 공갈죄의 객체가 될 수 있다.

연결 NormCard: `art350_sec3.real_estate_object`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec8_2.component.extortion_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.

연결 NormCard: `art350_sec8_2.no_right_extortion`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec8_2.component.extortion_object_satisfied.05`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.

연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec1.component.extortion_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.

연결 NormCard: `art350_sec1.defective_disposition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec1.component.extortion_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.

연결 NormCard: `art350_sec1.extortion_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_1.component.extortion_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.

연결 NormCard: `art350_sec4_1.means_threat_or_violence`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_1.component.extortion_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.

연결 NormCard: `art350_sec4_1.objective_fear_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_2.component.extortion_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.

연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_2.component.extortion_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.

연결 NormCard: `art350_sec4_2.third_party_harm_notice`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_2.component.extortion_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.

연결 NormCard: `art350_sec4_2.threat_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_2.component.extortion_conduct_satisfied.08`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.

연결 NormCard: `art350_sec4_2.threat_to_third_party`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_4.component.extortion_conduct_satisfied.09`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.

연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec4_4.component.extortion_conduct_satisfied.10`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.

연결 NormCard: `art350_sec4_4.victim_capacity`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec5_1.component.extortion_conduct_satisfied.11`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.

연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec5_3.component.extortion_conduct_satisfied.12`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.

연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec5_3.component.extortion_conduct_satisfied.13`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.

연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec6_2.component.extortion_conduct_satisfied.14`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.

연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec8_1.component.extortion_conduct_satisfied.15`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.

연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec8_2.component.extortion_conduct_satisfied.16`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.

연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec8_2.component.extortion_conduct_satisfied.17`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.

연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec5_2.component.extortion_causation_satisfied.01`

이 규칙은 **행위와 결과의 연결(인과·귀속)이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.

연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec9.component.extortion_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.

연결 NormCard: `art350_sec9.illicit_gain_intent.required`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec9.component.extortion_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.

연결 NormCard: `art350_sec9.intent.objective_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec7_1.component.extortion_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.

연결 NormCard: `art350_sec7_1.attempt_threat_notification`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec7_2.component.extortion_completion_satisfied.02`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.

연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec7_3.component.extortion_completion_satisfied.03`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.

연결 NormCard: `art350_sec7_3.completion.bank_transfer`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec7_3.component.extortion_completion_satisfied.04`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.

연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `extortion.art350_sec3.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기의 재물 또는 재산상 이익에 대해서는 공갈죄가 성립하지 않는다.

연결 NormCard: `art350_sec3.own_property_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec4_1.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec4_1.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec4_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 해악 실현이 위법하지 않더라도 외포시켜 불법으로 재산상 이익을 취득하면 공갈죄가 성립할 수 있으나, 행위가 권리행사인 경우에는 위법성이 조각될 수 있다.

연결 NormCard: `art350_sec4_2.right_exercise_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec5_2.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄가 성립하려면 협박 또는 폭행과 외포 사이 및 외포와 재산적 처분행위 사이에 인과관계가 있어야 하며, 협박·폭행을 원인으로 하지 않은 외포심에 따른 재산적 처분행위에는 공갈죄가 성립하지 않는다.

연결 NormCard: `art350_sec5_2.fear_causation_required`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec5_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박 또는 폭행을 하였으나 상대방이 외포심을 일으키지 않거나 자선심 등 다른 이유로 재물을 교부한 경우에는 공갈미수죄가 성립한다.

연결 NormCard: `art350_sec5_2.no_fear_attempt`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec5_3.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec6_2.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다.

연결 NormCard: `art350_sec6_2.satisfied_consideration_causation_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec8_2.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다.

연결 NormCard: `art350_sec8_2.permitted_threat_no_extortion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec8_2.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다.

연결 NormCard: `art350_sec8_2.right_exercise_total_assessment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `extortion.art350_sec1.mandatory_negative.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄에서는 공갈로 상대방의 하자 있는 의사를 형성하고, 그에 기한 재산적 처분행위를 통하여 재물 또는 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.defective_disposition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec1.mandatory_negative.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄는 사람을 공갈하여 재물의 교부 또는 재산상 이익의 취득을 얻는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec1.extortion_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec3.mandatory_negative.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 객체는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.object`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec3.mandatory_negative.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 이전하는 처분행위를 하게 할 수 있기 때문이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.possessed_property_object_affirmative`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec3.mandatory_negative.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산도 공갈죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec3.real_estate_object`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_1.mandatory_negative.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.means_threat_or_violence`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_1.mandatory_negative.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_1.objective_fear_assessment`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_2.mandatory_negative.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해악의 고지는 명시적일 필요가 없고 언어·거동으로도 가능하며, 피공갈자 외 제3자를 통하여 간접적으로 할 수도 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.implied_or_indirect_threat`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_2.mandatory_negative.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자의 행위에 의한 해악 고지가 공갈이 되려면, 행위자가 제3자의 해악행위 결의에 영향을 미칠 수 있는 입장임을 상대방에게 알게 하거나 상대방이 이를 추측할 수 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.third_party_harm_notice`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_2.mandatory_negative.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 협박은 공포심을 일으킬 목적으로 상대방에게 해악을 통고하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_2.mandatory_negative.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방 또는 그 가족·친구 등 제3자에 대한 해악의 통고도 상대방을 외포하게 하기에 족하면 협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_2.threat_to_third_party`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_4.mandatory_negative.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피공갈자와 재산상 피해자가 동일인이 아닌 경우, 피공갈자는 공갈 목적 재물 또는 재산상 이익을 처분할 사실상 또는 법률상 권한이나 지위가 있어야 하며, 피공갈자와 재산 처분행위자는 동일하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.separate_victim_disposition_authority`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec4_4.mandatory_negative.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈의 상대방에는 법인이 포함되며, 공갈의 상대방은 의사능력이 있는 사람에 한정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec4_4.victim_capacity`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec5_1.mandatory_negative.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄 성립에는 협박으로 상대방이 외포하고, 그로 인하여 재산적 처분행위를 하여 행위자 또는 제3자가 재물이나 재산상 이익을 취득하여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_1.threat_fear_disposition_gain`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec5_2.mandatory_negative.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 사정으로 이미 외포심을 가진 사람에게 그 외포심을 유지·확실하게 하여 재산적 처분행위를 하게 한 경우에는 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_2.preexisting_fear_maintained`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec5_3.mandatory_negative.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.delivery_tacit_acquiescence`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec5_3.mandatory_negative.017`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제3자가 재물의 교부 또는 재산상 이익을 받는 경우에도, 피공갈자와 처분행위자가 같은 사람이고 제3자가 공갈자의 사자·대리인 또는 공갈자가 특별히 수익하게 하려는 제3자인 관계가 있으면 공갈죄가 성립할 수 있으며, 그러한 관계가 없으면 공갈죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec5_3.third_party_receipt_relationship`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec6_2.mandatory_negative.018`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec6_2.consideration_does_not_negate_extortion`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec7_1.mandatory_negative.019`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 공여하게 하는 수단으로 사람을 외포시키기에 족한 해악을 고지한 때 공갈죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_1.attempt_threat_notification`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec7_2.mandatory_negative.020`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 기수에는 공갈행위, 그로 인한 상대방의 외포, 그리고 그 외포로 인한 재산적 처분행위가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_2.completion.fear_disposition_causal_link`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec7_3.mandatory_negative.021`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자를 공갈하여 행위자가 지정한 예금계좌에 송금하게 한 경우에는 입금과 동시에 행위자가 자유롭게 처분할 수 있는 상태가 되어 그때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.bank_transfer`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec7_3.mandatory_negative.022`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 객체인 갈취죄는 재물 교부를 받은 때, 재산상 이익이 객체인 이득죄는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec7_3.completion.property_and_benefit`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec8_1.mandatory_negative.023`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_1.right_enforcement_method_standard`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec8_2.mandatory_negative.024`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.extortion_loss_despite_payment_duty`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec8_2.mandatory_negative.025`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.no_right_extortion`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec8_2.mandatory_negative.026`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.permissible_range_purpose_means`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec8_2.mandatory_negative.027`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec8_2.rightful_claim_excessive_method`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec9.mandatory_negative.028`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.illicit_gain_intent.required`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.art350_sec9.mandatory_negative.029`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공갈죄의 고의는 모든 객관적 구성요건요소에 대한 인식을 의미하고, 미필적 인식으로도 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art350_sec9.intent.objective_elements`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `extortion.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분
- 실행행위 요건이 충족됨
- 행위와 결과의 연결(인과·귀속)이 인정됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `extortion.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art350_sec3.own_property_exception`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.right_exercise_exception`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `extortion.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.own_property_exception`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_1.objectively_insufficient_threat`, `art350_sec4_1.robbery_boundary`, `art350_sec4_2.actual_intent_or_feasibility_not_required`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.right_exercise_exception`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.fear_causation_required`, `art350_sec5_2.no_fear_attempt`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.complete_suppression_robbery`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6.no_overall_property_decrease`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec6_2.satisfied_consideration_causation_exception`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.permitted_threat_no_extortion`, `art350_sec8_2.right_exercise_total_assessment`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `extortion.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `extortion.art350_sec4_2.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 실제로 해악을 실현할 의사를 가졌는지 또는 해악의 실현이 가능한지는 공갈죄 성립에 영향을 미치지 않는다.

연결 NormCard: `art350_sec4_2.actual_intent_or_feasibility_not_required`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `extortion.art350_sec6.requirement_waived.002`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공갈죄에서는 피공갈자의 하자 있는 의사에 기한 재물 교부 자체가 재산상 손해에 해당하므로, 피해자 전체 재산의 감소가 반드시 요구되지는 않는다.

연결 NormCard: `art350_sec6.no_overall_property_decrease`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `extortion.art350_sec4_1.boundary_shift.001`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `extortion.art350_sec4_1.boundary_shift.002`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `extortion.art350_sec5_3.boundary_shift.003`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `extortion.art350_sec4_1.refers_to_crime.001`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다.

연결 NormCard: `art350_sec4_1.objectively_insufficient_threat`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `extortion.art350_sec4_1.refers_to_crime.002`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다.

연결 NormCard: `art350_sec4_1.robbery_boundary`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `extortion.art350_sec5_3.refers_to_crime.003`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 협박으로 상대방의 의사가 완전히 억압되어 임의성 있는 재물 교부로 평가할 수 없는 경우에는, 외관상 교부 형식이 있어도 강도죄가 성립한다.

연결 NormCard: `art350_sec5_3.complete_suppression_robbery`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `extortion.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art350_sec1.defective_disposition`, `art350_sec1.extortion_definition`, `art350_sec3.object`, `art350_sec3.possessed_property_object_affirmative`, `art350_sec3.real_estate_object`, `art350_sec4_1.means_threat_or_violence`, `art350_sec4_1.objective_fear_assessment`, `art350_sec4_2.implied_or_indirect_threat`, `art350_sec4_2.third_party_harm_notice`, `art350_sec4_2.threat_definition`, `art350_sec4_2.threat_to_third_party`, `art350_sec4_4.separate_victim_disposition_authority`, `art350_sec4_4.victim_capacity`, `art350_sec5_1.threat_fear_disposition_gain`, `art350_sec5_2.preexisting_fear_maintained`, `art350_sec5_3.delivery_tacit_acquiescence`, `art350_sec5_3.third_party_receipt_relationship`, `art350_sec6_2.consideration_does_not_negate_extortion`, `art350_sec7_1.attempt_threat_notification`, `art350_sec7_2.completion.fear_disposition_causal_link`, `art350_sec7_3.completion.bank_transfer`, `art350_sec7_3.completion.property_and_benefit`, `art350_sec8_1.right_enforcement_method_standard`, `art350_sec8_2.extortion_loss_despite_payment_duty`, `art350_sec8_2.no_right_extortion`, `art350_sec8_2.permissible_range_purpose_means`, `art350_sec8_2.rightful_claim_excessive_method`, `art350_sec9.illicit_gain_intent.required`, `art350_sec9.intent.objective_elements`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
