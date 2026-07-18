# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.fraud.article347.full.v1_candidate`
- predicate: 201개
- rule: 342개
- NormCard: 88개

## Predicate

### `provable(case_id: String, assessment_id: String)`

해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `case_assessment_complete(case_id: String, defendant_id: String)`

사건 라우터가 선택한 공통·프로파일 쟁점의 유한한 평가 묶음이 완결되어 최종 결론 계층의 폐쇄세계 검사를 허용함

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `distinct_entity(case_id: String, left_entity_id: String, right_entity_id: String)`

사건의 entity resolution에서 두 역할이 서로 다른 실체임이 확인됨

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_deception_fraud_causal_link_deception_property_disposition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

### `satisfied_deception_fraud_causal_link_deception_property_disposition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

### `assess_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

### `satisfied_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

### `assess_deception_fraud_causal_link_no_disposition_no_deception(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

### `satisfied_deception_fraud_causal_link_no_disposition_no_deception(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

### `assess_deception_fraud_definition_deceived_person_unspecified(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.deceived-person-unspecified`

### `satisfied_deception_fraud_definition_deceived_person_unspecified(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deceived-person-unspecified`

### `assess_deception_fraud_definition_deceived_person_victim_distinct(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

### `satisfied_deception_fraud_definition_deceived_person_victim_distinct(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

### `assess_deception_fraud_definition_deception_content_basis_fact(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-content-basis-fact`

### `satisfied_deception_fraud_definition_deception_content_basis_fact(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-content-basis-fact`

### `assess_deception_fraud_definition_deception_counterparty_is_other(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

### `satisfied_deception_fraud_definition_deception_counterparty_is_other(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 기망의 상대방은 타인이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

### `assess_deception_fraud_definition_deception_good_faith_mistake(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

### `satisfied_deception_fraud_definition_deception_good_faith_mistake(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

### `assess_deception_fraud_definition_deception_means_unrestricted(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-means-unrestricted`

### `satisfied_deception_fraud_definition_deception_means_unrestricted(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-means-unrestricted`

### `assess_deception_fraud_definition_deception_object_facts(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-object-facts`

### `satisfied_deception_fraud_definition_deception_object_facts(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-object-facts`

### `assess_deception_fraud_definition_deception_target_human(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.deception-target-human`

### `satisfied_deception_fraud_definition_deception_target_human(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deception-target-human`

### `assess_deception_fraud_definition_exploitation_existing_mistake(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

### `satisfied_deception_fraud_definition_exploitation_existing_mistake(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

### `assess_deception_fraud_definition_implicit_deception(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.definition.implicit-deception`

### `satisfied_deception_fraud_definition_implicit_deception(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.implicit-deception`

### `assess_deception_fraud_definition_notice_duty_violation_omission(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

### `satisfied_deception_fraud_definition_notice_duty_violation_omission(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

### `assess_deception_fraud_definition_other_includes_corporation(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.definition.other-includes-corporation`

### `satisfied_deception_fraud_definition_other_includes_corporation(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.other-includes-corporation`

### `assess_deception_fraud_element_deception_must_create_false_belief(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

### `satisfied_deception_fraud_element_deception_must_create_false_belief(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

### `assess_deception_fraud_element_deception_not_legal_act_important_part(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

### `satisfied_deception_fraud_element_deception_not_legal_act_important_part(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

### `assess_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

### `satisfied_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

### `assess_deception_fraud_element_omission_deception_guarantor_equivalence(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

### `satisfied_deception_fraud_element_omission_deception_guarantor_equivalence(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

### `assess_deception_fraud_element_omission_deception_independent_error(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.element.omission-deception-independent-error`

### `satisfied_deception_fraud_element_omission_deception_independent_error(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.omission-deception-independent-error`

### `assess_deception_fraud_element_omission_deception_legal_notice_duty(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

### `satisfied_deception_fraud_element_omission_deception_legal_notice_duty(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

### `assess_deception_fraud_element_transaction_purpose_no_impairment(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

### `satisfied_deception_fraud_element_transaction_purpose_no_impairment(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

### `assess_deception_fraud_element_victim_negligence_no_bar(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `deception.fraud.element.victim-negligence-no-bar`

### `satisfied_deception_fraud_element_victim_negligence_no_bar(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.element.victim-negligence-no-bar`

### `assess_deception_fraud_standard_advertising_important_concrete_falsehood(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

### `satisfied_deception_fraud_standard_advertising_important_concrete_falsehood(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

### `assess_deception_fraud_standard_advertising_tolerable_exaggeration(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

### `satisfied_deception_fraud_standard_advertising_tolerable_exaggeration(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

### `assess_deception_fraud_standard_deception_concrete_circumstances(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

### `satisfied_deception_fraud_standard_deception_concrete_circumstances(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

### `assess_deception_fraud_standard_easily_detectable_lie(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

### `satisfied_deception_fraud_standard_easily_detectable_lie(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

### `assess_deception_fraud_standard_implicit_deception_explanatory_value(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

### `satisfied_deception_fraud_standard_implicit_deception_explanatory_value(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

### `assess_deception_fraud_standard_implicit_omission_deception_distinction(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

### `satisfied_deception_fraud_standard_implicit_omission_deception_distinction(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

### `assess_deception_fraud_standard_intent_to_defraud_loan_inference(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

### `satisfied_deception_fraud_standard_intent_to_defraud_loan_inference(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

### `assess_deception_fraud_standard_loan_lender_anticipated_risk(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

### `satisfied_deception_fraud_standard_loan_lender_anticipated_risk(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

### `assess_deception_fraud_standard_loan_purpose_materiality(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

### `satisfied_deception_fraud_standard_loan_purpose_materiality(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

### `assess_deception_fraud_standard_loan_subsequent_default(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

### `satisfied_deception_fraud_standard_loan_subsequent_default(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

### `assess_deception_fraud_standard_precedent_notice_duty_materiality(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

### `satisfied_deception_fraud_standard_precedent_notice_duty_materiality(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

### `assess_deception_fraud_standard_vague_opinion_not_deception(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

### `satisfied_deception_fraud_standard_vague_opinion_not_deception(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

### `assess_fraud_damage_acquisition_delivery_factual_control(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

### `satisfied_fraud_damage_acquisition_delivery_factual_control(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

### `assess_fraud_damage_acquisition_delivery_of_property(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

### `satisfied_fraud_damage_acquisition_delivery_of_property(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

### `assess_fraud_damage_acquisition_money_delivery_full_amount(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

### `satisfied_fraud_damage_acquisition_money_delivery_full_amount(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

### `assess_fraud_damage_acquisition_property_concept_reported_precedent(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

### `satisfied_fraud_damage_acquisition_property_concept_reported_precedent(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

### `assess_fraud_damage_acquisition_property_disposition_types(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.property_disposition_types`

### `satisfied_fraud_damage_acquisition_property_disposition_types(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.property_disposition_types`

### `assess_fraud_damage_acquisition_property_loss_negative_view(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

### `satisfied_fraud_damage_acquisition_property_loss_negative_view(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

### `assess_fraud_damage_acquisition_protected_economic_interest(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.protected_economic_interest`

### `satisfied_fraud_damage_acquisition_protected_economic_interest(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.protected_economic_interest`

### `assess_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

### `satisfied_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

### `assess_fraud_damage_acquisition_subsequent_return_irrelevant(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

### `satisfied_fraud_damage_acquisition_subsequent_return_irrelevant(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

### `assess_fraud_general_object_causation_required(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_general_object.causation_required`

### `satisfied_fraud_general_object_causation_required(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_general_object.causation_required`

### `assess_fraud_general_object_deception_error_causation(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_general_object.deception_error_causation`

### `satisfied_fraud_general_object_deception_error_causation(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_general_object.deception_error_causation`

### `assess_fraud_intent_contract_breach_distinction(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_intent.contract_breach_distinction`

### `satisfied_fraud_intent_contract_breach_distinction(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.contract_breach_distinction`

### `assess_fraud_intent_illegal_appropriation_definition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_intent.illegal_appropriation_definition`

### `satisfied_fraud_intent_illegal_appropriation_definition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.illegal_appropriation_definition`

### `assess_fraud_intent_no_disposition_inducement_intent(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

### `satisfied_fraud_intent_no_disposition_inducement_intent(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

### `assess_fraud_intent_precedent_illegal_appropriation_intent(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

### `satisfied_fraud_intent_precedent_illegal_appropriation_intent(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

### `assess_fraud_intent_third_party_acquisition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_intent.third_party_acquisition`

### `satisfied_fraud_intent_third_party_acquisition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.third_party_acquisition`

### `assess_fraud_intent_time_of_conduct(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_intent.time_of_conduct`

### `satisfied_fraud_intent_time_of_conduct(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.time_of_conduct`

### `assess_fraud_mistake_conscious_nonexercise(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.conscious_nonexercise`

### `satisfied_fraud_mistake_conscious_nonexercise(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.conscious_nonexercise`

### `assess_fraud_mistake_deceived_disposer_identity(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.deceived_disposer_identity`

### `satisfied_fraud_mistake_deceived_disposer_identity(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 처분행위자는 동일인이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.deceived_disposer_identity`

### `assess_fraud_mistake_disposition_definition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.disposition_definition`

### `satisfied_fraud_mistake_disposition_definition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.disposition_definition`

### `assess_fraud_mistake_disposition_directness(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.disposition_directness`

### `satisfied_fraud_mistake_disposition_directness(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.disposition_directness`

### `assess_fraud_mistake_disposition_intent_act_awareness(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

### `satisfied_fraud_mistake_disposition_intent_act_awareness(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

### `assess_fraud_mistake_disposition_omission(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.disposition_omission`

### `satisfied_fraud_mistake_disposition_omission(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.disposition_omission`

### `assess_fraud_mistake_error_definition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.error_definition`

### `satisfied_fraud_mistake_error_definition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.error_definition`

### `assess_fraud_mistake_error_disposition_motivation(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.error_disposition_motivation`

### `satisfied_fraud_mistake_error_disposition_motivation(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.error_disposition_motivation`

### `assess_fraud_mistake_error_doubt_ignorance(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.error_doubt_ignorance`

### `satisfied_fraud_mistake_error_doubt_ignorance(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.error_doubt_ignorance`

### `assess_fraud_mistake_factual_act_disposition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.factual_act_disposition`

### `satisfied_fraud_mistake_factual_act_disposition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.factual_act_disposition`

### `assess_fraud_mistake_gain_purpose(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.gain_purpose`

### `satisfied_fraud_mistake_gain_purpose(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 사건 적용 평가가 충족됨: 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.gain_purpose`

### `assess_fraud_mistake_invalid_act_disposition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.invalid_act_disposition`

### `satisfied_fraud_mistake_invalid_act_disposition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.invalid_act_disposition`

### `assess_fraud_mistake_no_capacity_theft(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.no_capacity_theft`

### `satisfied_fraud_mistake_no_capacity_theft(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.no_capacity_theft`

### `assess_fraud_mistake_no_thought_no_error(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.no_thought_no_error`

### `satisfied_fraud_mistake_no_thought_no_error(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.no_thought_no_error`

### `assess_fraud_mistake_omission_not_all_nonclaims(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

### `satisfied_fraud_mistake_omission_not_all_nonclaims(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

### `assess_fraud_mistake_property_disposition_element(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.property_disposition_element`

### `satisfied_fraud_mistake_property_disposition_element(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.property_disposition_element`

### `assess_fraud_mistake_property_limited_disposition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.property_limited_disposition`

### `satisfied_fraud_mistake_property_limited_disposition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.property_limited_disposition`

### `assess_fraud_mistake_sequential_causation(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.sequential_causation`

### `satisfied_fraud_mistake_sequential_causation(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.sequential_causation`

### `assess_fraud_mistake_triangular_fraud_definition(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_mistake.triangular_fraud_definition`

### `satisfied_fraud_mistake_triangular_fraud_definition(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.triangular_fraud_definition`

### `assess_fraud_mistake_trick_theft_directness(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.trick_theft_directness`

### `satisfied_fraud_mistake_trick_theft_directness(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.trick_theft_directness`

### `assess_fraud_mistake_unaware_error(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `fraud_mistake.unaware_error`

### `satisfied_fraud_mistake_unaware_error(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.unaware_error`

### `assess_fraud_stages_participation_attempt_deceptive_act(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_stages_participation.attempt_deceptive_act`

### `satisfied_fraud_stages_participation_attempt_deceptive_act(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_stages_participation.attempt_deceptive_act`

### `assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

### `satisfied_fraud_stages_participation_completion_deception_disposition_transfer(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

### `assess_fraud_stages_participation_no_causation_attempt(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_stages_participation.no_causation_attempt`

### `satisfied_fraud_stages_participation_no_causation_attempt(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_stages_participation.no_causation_attempt`

### `assess_fraud_stages_participation_property_fraud_completion_control(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

### `satisfied_fraud_stages_participation_property_fraud_completion_control(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

### `assess_general_object_fraud_definition_property_benefit(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.definition.property-benefit`

### `satisfied_general_object_fraud_definition_property_benefit(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.definition.property-benefit`

### `assess_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

### `satisfied_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

### `assess_general_object_fraud_element_object_other_possessed_other_property(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

### `satisfied_general_object_fraud_element_object_other_possessed_other_property(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

### `assess_general_object_fraud_element_property_benefit_concrete(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.element.property-benefit-concrete`

### `satisfied_general_object_fraud_element_property_benefit_concrete(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 구체적인 이익이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.element.property-benefit-concrete`

### `assess_general_object_fraud_exception_public_interest_property_equivalence(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

### `satisfied_general_object_fraud_exception_public_interest_property_equivalence(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

### `assess_general_object_fraud_standard_later_cancellation_no_effect(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

### `satisfied_general_object_fraud_standard_later_cancellation_no_effect(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

### `assess_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

### `satisfied_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

### `assess_general_object_fraud_standard_own_property_not_object(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.standard.own-property-not-object`

### `satisfied_general_object_fraud_standard_own_property_not_object(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.standard.own-property-not-object`

### `assess_general_object_fraud_standard_public_interest_only_no_fraud(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

### `satisfied_general_object_fraud_standard_public_interest_only_no_fraud(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

### `assess_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

### `satisfied_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

### `assess_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id: String, assessment_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String, status: String)`

현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `satisfied_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_object_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.exception.public-interest-property-equivalence`

### `fraud_deception_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

사건에 적용되는 기망 기준이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.loan-purpose-materiality`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`

### `fraud_mistake_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

피기망자에게 법적 의미의 착오가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.unaware_error`

### `fraud_disposition_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

착오에 기한 재산적 처분행위가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.conscious_nonexercise`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.invalid_act_disposition`

### `fraud_acquisition_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

재물 교부 또는 재산상 이익의 취득이 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_mistake.property_disposition_element`

### `fraud_causal_chain_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.sequential_causation`

### `fraud_deceived_disposer_identity_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

피기망자와 처분행위자가 동일한 행위주체임

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_mistake.deceived_disposer_identity`

### `fraud_completion_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.property_fraud_completion_control`

### `fraud_third_party_acquisition_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.third_party_acquisition`

### `fraud_triangular_authority_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

### `fraud_unlawful_appropriation_intent_supported(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

불법영득의사가 요구되는 유형에서 그 의사가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

### `fraud_disposition_inducement_intent_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

피기망자로 하여금 재산적 처분행위를 하게 할 의사가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

### `fraud_intent_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

고의의 기망과 재산적 이득 목적이 함께 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.gain_purpose`

### `fraud_elements_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

사기죄의 공통 구성요건·역할·귀속 component가 모두 충족된 잠정 성립 후보

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_established(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

승인된 사기죄 core 구성요건과 역할·인과·기수 조건이 모두 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `fraud_intent.contract_breach_distinction`, `fraud_intent.time_of_conduct`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.gain_purpose`, `fraud_mistake.property_disposition_element`, `fraud_mistake.sequential_causation`, `fraud_stages_participation.completion_deception_disposition_transfer`, `general_object.fraud.element.object-other-possessed-other-property`

### `fraud_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-target-human`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.gain_purpose`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.trick_theft_directness`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 사기 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-target-human`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.gain_purpose`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.trick_theft_directness`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

### `fraud_role_structure_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.triangular_fraud_definition`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

### `fraud_beneficiary_attribution_satisfied(case_id: String, defendant_id: String, deceived_person_id: String, disposer_id: String, property_owner_id: String, beneficiary_id: String)`

본인 또는 제3자에게 귀속되는 취득 구조가 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.gain_purpose`

## Rules

### `fraud.core_deception.card.001.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-unspecified`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-content-basis-fact`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 기망의 상대방은 타인이다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.008.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-means-unrestricted`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-object-facts`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-target-human`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.implicit-deception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.other-includes-corporation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-independent-error`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.victim-negligence-no-bar`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.039.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_disposition_types`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.042.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.protected_economic_interest`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_rights_exercise.card.043.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.044.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.045.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.causation_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.046.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.deception_error_causation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.047.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.contract_breach_distinction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.048.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.illegal_appropriation_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.049.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.050.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_third_party_acquisition.card.051.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.third_party_acquisition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.052.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.time_of_conduct`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.053.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.conscious_nonexercise`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.054.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 처분행위자는 동일인이어야 한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.055.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.056.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_directness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.057.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.058.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_omission`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.059.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.060.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_disposition_motivation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.061.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_doubt_ignorance`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.062.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.factual_act_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.063.satisfied`

이 규칙은 **증명 가능한 사건 적용 평가가 충족됨: 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가**을 도출한다.

필요한 전제:

- 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.gain_purpose`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.064.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.invalid_act_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.065.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_capacity_theft`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.066.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_thought_no_error`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.067.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.068.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_disposition_element`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.069.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_limited_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.070.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.sequential_causation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.071.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.triangular_fraud_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.072.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.trick_theft_directness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.073.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.unaware_error`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.074.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.attempt_deceptive_act`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.075.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.076.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.no_causation_attempt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.077.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.078.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.079.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.080.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.081.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 구체적인 이익이어야 한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.property-benefit-concrete`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_public_interest.card.082.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.083.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.084.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.085.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-property-not-object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_public_interest.card.086.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.087.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_rights_exercise.card.088.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.component.fraud_object_satisfied.01`

이 규칙은 **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.

연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_public_interest.component.fraud_object_satisfied.02`

이 규칙은 **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.

연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_deception_satisfied.03`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.

연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_loan.component.fraud_deception_satisfied.04`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.

연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_advertising.component.fraud_deception_satisfied.05`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.

연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_implicit_deception.component.fraud_deception_satisfied.06`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.

연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_loan.component.fraud_deception_satisfied.07`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.

연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_rights_exercise.component.fraud_deception_satisfied.08`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.

연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.03`

이 규칙은 **피기망자에게 법적 의미의 착오가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.

연결 NormCard: `fraud_mistake.error_doubt_ignorance`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.04`

이 규칙은 **피기망자에게 법적 의미의 착오가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.

연결 NormCard: `fraud_mistake.unaware_error`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.01`

이 규칙은 **착오에 기한 재산적 처분행위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.

연결 NormCard: `fraud_mistake.disposition_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_disposition_satisfied.02`

이 규칙은 **착오에 기한 재산적 처분행위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.

연결 NormCard: `fraud_mistake.conscious_nonexercise`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.03`

이 규칙은 **착오에 기한 재산적 처분행위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.

연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.04`

이 규칙은 **착오에 기한 재산적 처분행위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.

연결 NormCard: `fraud_mistake.factual_act_disposition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.05`

이 규칙은 **착오에 기한 재산적 처분행위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.

연결 NormCard: `fraud_mistake.invalid_act_disposition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_delivery.component.fraud_acquisition_satisfied.01`

이 규칙은 **재물 교부 또는 재산상 이익의 취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.

연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_delivery.component.fraud_acquisition_satisfied.02`

이 규칙은 **재물 교부 또는 재산상 이익의 취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.

연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_benefit.component.fraud_acquisition_satisfied.03`

이 규칙은 **재물 교부 또는 재산상 이익의 취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 사건 적용 평가가 충족됨: 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가

연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_acquisition_satisfied.04`

이 규칙은 **재물 교부 또는 재산상 이익의 취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.

연결 NormCard: `fraud_mistake.property_disposition_element`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_causal_chain_satisfied.01`

이 규칙은 **기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.

연결 NormCard: `fraud_mistake.sequential_causation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_deceived_disposer_identity_satisfied.01`

이 규칙은 **피기망자와 처분행위자가 동일한 행위주체임**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 처분행위자는 동일인이어야 한다.

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.stage_attempt_completion.component.fraud_completion_satisfied.01`

이 규칙은 **사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.

연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.stage_attempt_completion.component.fraud_completion_satisfied.02`

이 규칙은 **사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.

연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.structure_third_party_acquisition.component.fraud_third_party_acquisition_satisfied.01`

이 규칙은 **제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.

연결 NormCard: `fraud_intent.third_party_acquisition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.structure_triangular.component.fraud_triangular_authority_satisfied.01`

이 규칙은 **피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.

연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_intent.component.fraud_unlawful_appropriation_intent_supported.01`

이 규칙은 **불법영득의사가 요구되는 유형에서 그 의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.

연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_deception.component.fraud_deception_satisfied.01`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가
- 증명 가능한 사건 적용 평가가 충족됨: 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.definition.deception-good-faith-mistake`

검토 메모: 일반 기망 경로는 정의의 추상적 타당성만으로는 부족하고, 특정 행위의 신의칙 위반·실제 착오 유발과 재산적 처분 지향성을 함께 요구한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.01`

이 규칙은 **피기망자에게 법적 의미의 착오가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 사건 적용 평가가 충족됨: 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가
- 증명 가능한 사건 적용 평가가 충족됨: 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가

연결 NormCard: `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`

검토 메모: 일반 착오 경로는 구체적인 사실불일치 인식과 그 인식의 처분동기 형성·확정을 함께 요구한다. 정의 명제만으로 착오를 인정하지 않는다.

### `fraud.profile_omission.component.fraud_deception_satisfied`

이 규칙은 **사건에 적용되는 기망 기준이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.
- 증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.
- 증명 가능한 평가에서 다음 조건이 충족됨: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.

연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`

검토 메모: 부작위 기망은 보증인적 지위·독립 착오·법률상 고지의무가 함께 확인된 경로다.

### `fraud.object_property_benefit.component.fraud_object_satisfied`

이 규칙은 **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.
- 증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 구체적인 이익이어야 한다.

연결 NormCard: `general_object.fraud.definition.property-benefit`, `general_object.fraud.element.property-benefit-concrete`

검토 메모: 재물 외 재산상 이익 branch는 경제적 가치 증가와 구체성을 함께 요구한다.

### `fraud.core_intent.component.disposition_inducement_intent_satisfied`

이 규칙은 **피기망자로 하여금 재산적 처분행위를 하게 할 의사가 인정됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

검토 메모: '처분행위를 하게 할 의사가 없음'이라는 배제조건이 명시적으로 not_satisfied이고 증명 가능할 때만 처분 유도 의사를 긍정한다.

### `fraud.core_intent.component.fraud_intent_satisfied`

이 규칙은 **고의의 기망과 재산적 이득 목적이 함께 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 사건 적용 평가가 충족됨: 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가
- 증명 가능한 사건 적용 평가가 충족됨: 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가
- 증명 가능한 사건 적용 평가가 충족됨: 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가
- 피기망자로 하여금 재산적 처분행위를 하게 할 의사가 인정됨

연결 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.gain_purpose`

검토 메모: 단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적을 함께 요구한다.

### `fraud.profile_loan.component.fraud_intent_satisfied`

이 규칙은 **고의의 기망과 재산적 이득 목적이 함께 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.
- 증명 가능한 사건 적용 평가가 충족됨: 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가
- 증명 가능한 사건 적용 평가가 충족됨: 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가
- 피기망자로 하여금 재산적 처분행위를 하게 할 의사가 인정됨

연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.gain_purpose`

검토 메모: 차용금 사건에서는 객관적 사정으로 추론한 편취 범의와 재산적 이득 목적을 결합한다.

### `fraud.core_deception.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-unspecified`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-unspecified`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-content-basis-fact`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-content-basis-fact`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-means-unrestricted`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-means-unrestricted`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-object-facts`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-object-facts`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-target-human`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-target-human`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.implicit-deception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.implicit-deception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.other-includes-corporation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.other-includes-corporation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-independent-error`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-independent-error`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.victim-negligence-no-bar`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.element.victim-negligence-no-bar`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-purpose-materiality`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_factual_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.delivery_of_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_disposition_types`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_disposition_types`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.042.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.protected_economic_interest`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.042.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.protected_economic_interest`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_rights_exercise.card.043.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_rights_exercise.card.043.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.044.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.044.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.045.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.causation_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.045.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.causation_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.046.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.deception_error_causation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.046.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_general_object.deception_error_causation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.047.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.contract_breach_distinction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.047.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.contract_breach_distinction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.048.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.illegal_appropriation_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.048.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.illegal_appropriation_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.049.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.049.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.050.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.050.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_third_party_acquisition.card.051.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.third_party_acquisition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_third_party_acquisition.card.051.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.third_party_acquisition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.052.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.time_of_conduct`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.052.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.time_of_conduct`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.053.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.conscious_nonexercise`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.053.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.conscious_nonexercise`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.054.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.054.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.055.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.055.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.056.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_directness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.056.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_directness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.057.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.057.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_intent_act_awareness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.058.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_omission`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.058.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_omission`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.059.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.059.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.060.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_disposition_motivation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.060.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_disposition_motivation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.061.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_doubt_ignorance`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.061.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_doubt_ignorance`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.062.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.factual_act_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.062.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.factual_act_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.063.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.gain_purpose`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.063.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.gain_purpose`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.064.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.invalid_act_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.064.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.invalid_act_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.065.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_capacity_theft`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.065.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_capacity_theft`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.066.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_thought_no_error`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.066.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.no_thought_no_error`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.067.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.067.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.068.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_disposition_element`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.068.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_disposition_element`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.069.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_limited_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.069.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_limited_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.070.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.sequential_causation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.070.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.sequential_causation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.071.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.triangular_fraud_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.071.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.triangular_fraud_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.072.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.trick_theft_directness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.072.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.trick_theft_directness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.073.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.unaware_error`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.073.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.unaware_error`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.074.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.attempt_deceptive_act`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.074.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.attempt_deceptive_act`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.075.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.075.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.076.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.no_causation_attempt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.076.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.no_causation_attempt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.077.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.077.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.property_fraud_completion_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.078.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.078.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.079.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.079.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.080.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.080.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.081.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.property-benefit-concrete`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.081.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.property-benefit-concrete`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_public_interest.card.082.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_public_interest.card.082.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.083.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.083.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.084.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.084.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.085.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-property-not-object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.085.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.own-property-not-object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_public_interest.card.086.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_public_interest.card.086.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.087.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.087.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_rights_exercise.card.088.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_rights_exercise.card.088.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.

연결 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.

연결 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.

연결 NormCard: `deception.fraud.definition.deception-target-human`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.

연결 NormCard: `deception.fraud.element.deception-must-create-false-belief`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.

연결 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_advertising.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.

연결 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.

연결 NormCard: `deception.fraud.standard.easily-detectable-lie`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_loan.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.

연결 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_loan.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.

연결 NormCard: `deception.fraud.standard.loan-subsequent-default`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.

연결 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.

연결 NormCard: `fraud_general_object.causation_required`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.

연결 NormCard: `fraud_general_object.deception_error_causation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_intent.bar.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.

연결 NormCard: `fraud_intent.no_disposition_inducement_intent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.

연결 NormCard: `fraud_mistake.no_capacity_theft`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_mistake_disposition.bar.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.

연결 NormCard: `fraud_mistake.no_thought_no_error`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_omission.bar.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.

연결 NormCard: `fraud_mistake.omission_not_all_nonclaims`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_mistake_disposition.bar.017`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.

연결 NormCard: `fraud_mistake.property_limited_disposition`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.018`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.

연결 NormCard: `fraud_mistake.trick_theft_directness`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.019`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.

연결 NormCard: `fraud_stages_participation.no_causation_attempt`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.020`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.

연결 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.object_property_delivery.bar.021`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.

연결 NormCard: `general_object.fraud.standard.own-property-not-object`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.object_public_interest.bar.022`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.

연결 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_rights_exercise.bar.023`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.

연결 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.mandatory_negative.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 실질적으로 작용했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_deception.mandatory_negative.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 인식을 실제로 일으켰는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_intent.mandatory_negative.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 평가되는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.contract_breach_distinction`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_intent.mandatory_negative.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_intent.time_of_conduct`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.disposition_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 가졌는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.error_disposition_motivation`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_intent.mandatory_negative.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 목적의사가 있었는지를 사건 사실에 적용한 평가. 단순히 법률명제 자체가 옳다는 뜻이 아니라, 현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.gain_purpose`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.property_disposition_element`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_mistake.sequential_causation`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.stage_attempt_completion.mandatory_negative.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.object_property_delivery.mandatory_negative.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.structure_ordinary.role_structure`

이 규칙은 **일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨**을 도출한다.

필요한 전제:

- 피기망자와 처분행위자가 동일한 행위주체임

연결 NormCard: `fraud_mistake.deceived_disposer_identity`

검토 메모: 일반형은 피기망자·처분자·재산소유자에 같은 entity ID를 사용한다.

### `fraud.structure_triangular.role_structure`

이 규칙은 **일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨**을 도출한다.

필요한 전제:

- 피기망자와 처분행위자가 동일한 행위주체임
- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.
- 피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨
- 사건의 entity resolution에서 두 역할이 서로 다른 실체임이 확인됨

연결 NormCard: `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.triangular_fraud_definition`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 삼각사기는 피기망자=처분자를 유지하면서 별도 재산소유자와 그 재산을 처분할 권능 또는 지위를 요구한다.

### `fraud.structure_self_acquisition.beneficiary_attribution`

이 규칙은 **본인 또는 제3자에게 귀속되는 취득 구조가 충족됨**을 도출한다.

필요한 전제:

- 고의의 기망과 재산적 이득 목적이 함께 인정됨

연결 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.gain_purpose`

검토 메모: 피고인과 수익자에 같은 entity ID를 쓰는 본인취득 경로다.

### `fraud.structure_third_party_acquisition.beneficiary_attribution`

이 규칙은 **본인 또는 제3자에게 귀속되는 취득 구조가 충족됨**을 도출한다.

필요한 전제:

- 제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨
- 사건의 entity resolution에서 두 역할이 서로 다른 실체임이 확인됨

연결 NormCard: `fraud_intent.third_party_acquisition`

검토 메모: 제3자취득은 도구·대리 관계 또는 제3자 취득 의사를 별도 귀속 gate로 요구한다.

### `fraud.core.outcome.elements_satisfied`

이 규칙은 **사기죄의 공통 구성요건·역할·귀속 component가 모두 충족된 잠정 성립 후보**을 도출한다.

필요한 전제:

- 사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨
- 사건에 적용되는 기망 기준이 충족됨
- 피기망자에게 법적 의미의 착오가 인정됨
- 착오에 기한 재산적 처분행위가 인정됨
- 재물 교부 또는 재산상 이익의 취득이 인정됨
- 기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨
- 사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨
- 고의의 기망과 재산적 이득 목적이 함께 인정됨
- 일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨
- 본인 또는 제3자에게 귀속되는 취득 구조가 충족됨

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.loan-purpose-materiality`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.property_disposition_element`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.unaware_error`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.exception.public-interest-property-equivalence`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 공통 core는 세부 사기유형을 직접 분기하지 않는다. profile과 adapter가 채운 canonical component, 역할 구조 및 수익 귀속 interface만 AND 결합한다.

### `fraud.core.outcome.conflict.established_and_not_established`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 사기죄의 공통 구성요건·역할·귀속 component가 모두 충족된 잠정 성립 후보
- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 성립 후보와 명시적 불성립 사유가 함께 도출되면 최종 확정 전에 conflict를 노출한다.

### `fraud.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 사기 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-target-human`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.time_of_conduct`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.gain_purpose`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.trick_theft_directness`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `fraud.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `fraud.core.outcome.established`

이 규칙은 **승인된 사기죄 core 구성요건과 역할·인과·기수 조건이 모두 충족됨**을 도출한다.

필요한 전제:

- 사기죄의 공통 구성요건·역할·귀속 component가 모두 충족된 잠정 성립 후보
- 사건 라우터가 선택한 공통·프로파일 쟁점의 유한한 평가 묶음이 완결되어 최종 결론 계층의 폐쇄세계 검사를 허용함
- 해당 피고인에 관해 하나 이상의 명시적 사기 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.loan-purpose-materiality`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_intent.contract_breach_distinction`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.property_disposition_element`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.unaware_error`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.exception.public-interest-property-equivalence`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤의 최종 층에서만 사용한다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
