# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.breach_of_trust.full.v1_candidate`
- predicate: 90개
- rule: 173개
- NormCard: 36개

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

### `breach_of_trust_case_roles(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art355_breach_confidential_information(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.breach.confidential-information`

### `satisfied_art355_breach_confidential_information(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`

### `assess_art355_breach_duty_definition(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.breach.duty-definition`

### `satisfied_art355_breach_duty_definition(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.duty-definition`

### `assess_art355_breach_invalid_act_risk(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.breach.invalid-act-risk`

### `satisfied_art355_breach_invalid_act_risk(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.invalid-act-risk`

### `assess_art355_breach_other_affairs_processor(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.breach_other_affairs_processor`

### `satisfied_art355_breach_other_affairs_processor(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach_other_affairs_processor`

### `assess_art355_breach_right_transfer_general(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.breach_right_transfer_general`

### `satisfied_art355_breach_right_transfer_general(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach_right_transfer_general`

### `assess_art355_sec1_1_breach_of_trust(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_1.breach_of_trust`

### `satisfied_art355_sec1_1_breach_of_trust(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_1.breach_of_trust`

### `assess_art355_sec1_2_breach_of_trust_betrayal_theory(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

### `satisfied_art355_sec1_2_breach_of_trust_betrayal_theory(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

### `assess_art355_sec1_3_breach_of_trust_case_concrete_risk_of_loss(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

### `satisfied_art355_sec1_3_breach_of_trust_case_concrete_risk_of_loss(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

### `assess_art355_sec3_breach_of_trust_objective_elements(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

### `satisfied_art355_sec3_breach_of_trust_objective_elements(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

### `assess_art355_sec4_1_breach_of_trust_intent_elements(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

### `satisfied_art355_sec4_1_breach_of_trust_intent_elements(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

### `assess_art355_sec4_1_breach_of_trust_intent_no_purpose(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

### `satisfied_art355_sec4_1_breach_of_trust_intent_no_purpose(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

### `assess_art355_sec4_1_business_judgment_intent(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.business_judgment_intent`

### `satisfied_art355_sec4_1_business_judgment_intent(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.business_judgment_intent`

### `assess_art355_sec4_1_business_loss_alone_insufficient(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

### `satisfied_art355_sec4_1_business_loss_alone_insufficient(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

### `assess_art355_sec4_1_double_sale_unjustified_rescission_intent(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

### `satisfied_art355_sec4_1_double_sale_unjustified_rescission_intent(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

### `assess_art355_sec4_1_no_breach_of_trust_without_awareness(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

### `satisfied_art355_sec4_1_no_breach_of_trust_without_awareness(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

### `assess_art355_sec4_1_role_violation_intent(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.role_violation_intent`

### `satisfied_art355_sec4_1_role_violation_intent(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.role_violation_intent`

### `assess_art355_sec4_2_breach_for_principal_no_illicit_gain(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

### `satisfied_art355_sec4_2_breach_for_principal_no_illicit_gain(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

### `assess_art355_sec4_2_breach_illicit_gain_intent(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

### `satisfied_art355_sec4_2_breach_illicit_gain_intent(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

### `assess_art355_sec4_2_breach_illicit_gain_separate_requirement(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

### `satisfied_art355_sec4_2_breach_illicit_gain_separate_requirement(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

### `assess_art355_sec4_2_mixed_motives_primary_purpose(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

### `satisfied_art355_sec4_2_mixed_motives_primary_purpose(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

### `assess_art355_sec4_2_third_party_benefit_sufficient(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

### `satisfied_art355_sec4_2_third_party_benefit_sufficient(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

### `assess_art355_sec5_2_assigned_claim_proceeds_embezzlement(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

### `satisfied_art355_sec5_2_assigned_claim_proceeds_embezzlement(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

### `assess_art355_sec5_2_individual_delegation_exception(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.individual_delegation_exception`

### `satisfied_art355_sec5_2_individual_delegation_exception(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.individual_delegation_exception`

### `assess_art355_sec5_2_leasehold_transfer(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.leasehold_transfer`

### `satisfied_art355_sec5_2_leasehold_transfer(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.leasehold_transfer`

### `assess_art355_sec5_2_movable_sale_double_disposition(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

### `satisfied_art355_sec5_2_movable_sale_double_disposition(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

### `assess_art355_sec5_2_pre_certificate_stock_transfer(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

### `satisfied_art355_sec5_2_pre_certificate_stock_transfer(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

### `assess_art355_sec5_2_real_estate_double_sale_majority(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

### `satisfied_art355_sec5_2_real_estate_double_sale_majority(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

### `assess_art355_sec5_2_real_estate_sale_intermediate_payment(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

### `satisfied_art355_sec5_2_real_estate_sale_intermediate_payment(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

### `assess_art355_sec5_2_real_estate_transfer_exception(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

### `satisfied_art355_sec5_2_real_estate_transfer_exception(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

### `assess_art355_sec5_2_registered_movable_sale_disposition(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

### `satisfied_art355_sec5_2_registered_movable_sale_disposition(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

### `assess_art355_sec5_2_right_transfer_ordinary_duty(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

### `satisfied_art355_sec5_2_right_transfer_ordinary_duty(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

### `assess_art355_sec5_2_trust_relationship_threshold(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

### `satisfied_art355_sec5_2_trust_relationship_threshold(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

### `assess_art355_sec9_partnership_victim_breach(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec9.partnership_victim_breach`

### `satisfied_art355_sec9_partnership_victim_breach(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec9.partnership_victim_breach`

### `assess_art356_sec3_2_assistant_other_affairs(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec3_2.assistant_other_affairs`

### `satisfied_art356_sec3_2_assistant_other_affairs(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec3_2.assistant_other_affairs`

### `assess_art356_sec3_2_business_other_affairs_definition(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

### `satisfied_art356_sec3_2_business_other_affairs_definition(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

### `assess_art356_sec3_2_other_affairs_origin(case_id: String, assessment_id: String, defendant_id: String, principal_id: String, beneficiary_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec3_2.other_affairs_origin`

### `satisfied_art356_sec3_2_other_affairs_origin(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec3_2.other_affairs_origin`

### `breach_of_trust_object_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`

### `breach_of_trust_conduct_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.duty-definition`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec5_2.individual_delegation_exception`, `art355_sec9.partnership_victim_breach`

### `breach_of_trust_intent_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`

### `breach_of_trust_appropriation_intent_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

주관적 요건 중 불법영득·이득의사가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`

### `breach_of_trust_completion_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.invalid-act-risk`

### `breach_of_trust_elements_satisfied(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

### `breach_of_trust_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`

### `breach_of_trust_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`, `art356_sec3_2.assistant_other_affairs`, `art356_sec3_2.business_other_affairs_definition`, `art356_sec3_2.other_affairs_origin`

### `breach_of_trust_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`, `art356_sec3_2.assistant_other_affairs`, `art356_sec3_2.business_other_affairs_definition`, `art356_sec3_2.other_affairs_origin`

### `breach_of_trust_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`

### `breach_of_trust_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`, `art356_sec3_2.assistant_other_affairs`, `art356_sec3_2.business_other_affairs_definition`, `art356_sec3_2.other_affairs_origin`

### `breach_of_trust_established(case_id: String, defendant_id: String, principal_id: String, beneficiary_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

### `breach_of_trust_aggravation(case_id: String, defendant_id: String, kind: String)`

가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec3_2.assistant_other_affairs`, `art356_sec3_2.business_other_affairs_definition`, `art356_sec3_2.other_affairs_origin`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

## Rules

### `breach_of_trust.art355.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.confidential-information`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.confidential-information`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.confidential-information`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.duty-definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.duty-definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.duty-definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.invalid-act-risk`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.invalid-act-risk`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.invalid-act-risk`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_other_affairs_processor`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_other_affairs_processor`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_other_affairs_processor`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_right_transfer_general`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_right_transfer_general`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_right_transfer_general`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec1_1.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.breach_of_trust`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec1_1.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.breach_of_trust`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec1_1.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.breach_of_trust`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec1_2.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec1_2.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec1_2.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec1_3.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec1_3.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec1_3.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec3.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec3.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec3.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_judgment_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_judgment_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_judgment_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_1.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.role_violation_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_1.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.role_violation_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_1.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.role_violation_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_2.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_2.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_2.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_2.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_2.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_2.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_2.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_2.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_2.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_2.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_2.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_2.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec4_2.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec4_2.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec4_2.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.individual_delegation_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.individual_delegation_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.individual_delegation_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.leasehold_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.leasehold_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.leasehold_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec5_2.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec5_2.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec5_2.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355_sec9.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec9.partnership_victim_breach`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art355_sec9.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec9.partnership_victim_breach`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art355_sec9.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec9.partnership_victim_breach`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art356_sec3_2.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.assistant_other_affairs`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art356_sec3_2.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.assistant_other_affairs`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art356_sec3_2.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.assistant_other_affairs`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art356_sec3_2.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art356_sec3_2.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art356_sec3_2.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art356_sec3_2.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.other_affairs_origin`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust.art356_sec3_2.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.other_affairs_origin`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust.art356_sec3_2.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_2.other_affairs_origin`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust.art355.component.breach_of_trust_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.

연결 NormCard: `art355.breach_other_affairs_processor`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355.component.breach_of_trust_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.

연결 NormCard: `art355.breach_right_transfer_general`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec5_2.component.breach_of_trust_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.

연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec5_2.component.breach_of_trust_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.

연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec5_2.component.breach_of_trust_object_satisfied.05`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.

연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec5_2.component.breach_of_trust_object_satisfied.06`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.

연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355.component.breach_of_trust_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.

연결 NormCard: `art355.breach.duty-definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec1_1.component.breach_of_trust_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.

연결 NormCard: `art355_sec1_1.breach_of_trust`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec1_2.component.breach_of_trust_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.

연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec1_3.component.breach_of_trust_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.

연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec3.component.breach_of_trust_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.

연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec5_2.component.breach_of_trust_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.

연결 NormCard: `art355_sec5_2.individual_delegation_exception`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec9.component.breach_of_trust_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.

연결 NormCard: `art355_sec9.partnership_victim_breach`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.component.breach_of_trust_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.component.breach_of_trust_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.component.breach_of_trust_intent_satisfied.03`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.

연결 NormCard: `art355_sec4_1.business_judgment_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.component.breach_of_trust_intent_satisfied.04`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.

연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.component.breach_of_trust_intent_satisfied.05`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.

연결 NormCard: `art355_sec4_1.role_violation_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_2.component.breach_of_trust_appropriation_intent_satisfied.01`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.

연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_2.component.breach_of_trust_appropriation_intent_satisfied.02`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.

연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_2.component.breach_of_trust_appropriation_intent_satisfied.03`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.

연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_2.component.breach_of_trust_appropriation_intent_satisfied.04`

이 규칙은 **주관적 요건 중 불법영득·이득의사가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.

연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355.component.breach_of_trust_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.

연결 NormCard: `art355.breach.confidential-information`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355.component.breach_of_trust_completion_satisfied.02`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.

연결 NormCard: `art355.breach.invalid-act-risk`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust.art355_sec4_1.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다.

연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec4_1.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다.

연결 NormCard: `art355_sec4_1.no_breach_of_trust_without_awareness`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec4_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 본인의 이익을 위하여 사무를 처리한 때에는 불법이득의 의사가 없어 배임죄가 성립하지 않는다.

연결 NormCard: `art355_sec4_2.breach_for_principal_no_illicit_gain`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권양도인이 양도 채권을 직접 추심하여 받은 금전을 양수인에게 지급하지 않고 임의 처분한 것은 권리이전계약상 채무불이행에 불과하여 횡령죄가 성립하지 않는다.

연결 NormCard: `art355_sec5_2.assigned_claim_proceeds_embezzlement`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.

연결 NormCard: `art355_sec5_2.leasehold_transfer`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 동산매매에서 매도인은 매수인에 대한 타인 사무처리자 지위에 있지 않으므로, 목적물을 인도하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

연결 NormCard: `art355_sec5_2.movable_sale_double_disposition`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 주권발행 전 주식 양도인이 제3자 대항요건을 갖추어 줄 채무는 자기 사무이므로, 그 요건을 갖추지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

연결 NormCard: `art355_sec5_2.pre_certificate_stock_transfer`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자동차 등 권리이전에 등기·등록이 필요한 동산의 매도인도 매수인에 대한 타인 사무처리자가 아니므로 소유권이전등록을 하지 않고 타인에게 처분하여도 배임죄가 성립하지 않는다.

연결 NormCard: `art355_sec5_2.registered_movable_sale_disposition`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355_sec5_2.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리이전계약이나 담보설정계약에서 통상적 계약관계상 급부의무에 불과한 경우에는 배임죄에서의 타인 사무가 아니다.

연결 NormCard: `art355_sec5_2.right_transfer_ordinary_duty`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust.art355.mandatory_negative.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.confidential-information`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355.mandatory_negative.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위는 구체적 사정에 비추어 법령·계약·신의성실상 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 본인과의 신임관계를 저버리는 행위이다. 단순한 형식적 법령·절차 위반만으로 충분하지 않고, 사무의 내용과 거래유형 및 보호법익을 고려한 경제적·실질적 손해 위험이 평가되어야 하며, 절차 준수만으로 실질적 임무위배가 배제되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.duty-definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355.mandatory_negative.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임행위가 법률상 무효라도 경제적 관점에서 본인에게 현실 손해 또는 손해와 같은 정도의 구체적·현실적 위험이 있으면 배임죄가 문제될 수 있다. 반대로 사실상 손해와 법률상 책임 가능성이 명백히 없으면 배임죄는 성립하지 않으며, 추상적 위험만 있는 경우에는 배임미수 가능성이 문제된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach.invalid-act-risk`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355.mandatory_negative.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 주체는 신의성실 원칙상 신임관계에 기초하여 타인의 재산적 이익을 보호·관리하는 것이 전형적·본질적 내용인 타인의 사무처리자에 한정되고, 대외적 대리권이나 포괄적 위탁사무는 반드시 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_other_affairs_processor`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355.mandatory_negative.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매·교환 등 권리이전계약의 이행채무는 원칙적으로 자기 사무이나, 중도금을 지급받아 계약의 구속력에서 벗어날 수 없는 부동산 매도인은 양수인의 재산적 이익을 보호·관리할 신임관계에 있어 소유권이전의무가 타인의 사무로 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.breach_right_transfer_general`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec1_1.mandatory_negative.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 타인의 사무를 처리하는 자가 임무위배행위로 재산상 이익을 취득하거나 제3자로 하여금 취득하게 하여 본인에게 손해를 가하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.breach_of_trust`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec1_2.mandatory_negative.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.breach_of_trust_betrayal_theory`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec1_3.mandatory_negative.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec3.mandatory_negative.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 객관적 구성요건은 타인의 사무를 처리하는 자가 임무위배행위를 하여 재산상 이익을 취득하고 본인에게 재산상 손해를 가하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3.breach_of_trust.objective_elements`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_1.mandatory_negative.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_elements`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_1.mandatory_negative.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.breach_of_trust_intent_no_purpose`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_1.mandatory_negative.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.business_judgment_intent`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_1.mandatory_negative.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.double_sale_unjustified_rescission_intent`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_1.mandatory_negative.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.role_violation_intent`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_2.mandatory_negative.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 배임의 불법이득의 의사는 자기 또는 제3자의 이익을 꾀할 목적으로 업무상 임무에 위배된 행위를 하는 의사를 뜻한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_intent`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_2.mandatory_negative.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.breach_illicit_gain_separate_requirement`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_2.mandatory_negative.017`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본인을 위한 의사와 자기 또는 제3자의 재산상 이득을 위한 의사가 결합된 경우에는 어느 의사가 주된 것인지에 따라 배임죄 성립을 결정하고, 본인을 위한 의사가 부수적이면 배임죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mixed_motives_primary_purpose`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec4_2.mandatory_negative.018`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자 자신이 재산상 이익을 취득할 의사가 없더라도 제3자 등으로 하여금 보상을 받게 할 의사가 있으면 불법이득의 의사가 없다고 볼 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_benefit_sufficient`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec5_2.mandatory_negative.019`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 권리이전 또는 담보설정계약을 넘어 위임 등 배임죄상 신임관계를 인정할 개별 요소가 있으면 이를 근거로 사무의 타인성을 인정할 여지가 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.individual_delegation_exception`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec5_2.mandatory_negative.020`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_double_sale_majority`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec5_2.mandatory_negative.021`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 양도계약에서 중도금 지급 등으로 계약이 본격 이행 단계에 이르면, 계약이 취소·해제되지 않는 한 매도인은 매수인의 재산보전에 협력하는 신임관계에 있으므로 배임죄의 타인 사무처리자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_sale_intermediate_payment`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec5_2.mandatory_negative.022`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.real_estate_transfer_exception`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec5_2.mandatory_negative.023`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임죄의 타인 사무처리자가 되려면 당사자 관계의 전형적·본질적 내용이 통상 계약의 이익대립관계를 넘어 신임관계에 기초하여 타인 재산을 보호·관리하는 데 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5_2.trust_relationship_threshold`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.art355_sec9.mandatory_negative.024`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상호출자 공동사업 약정이 조합계약에 해당하고 조합원이 분담한 업무를 처리하면서 임무위배로 재산을 이전등기한 경우, 배임 피해자는 개별 조합원이 아니라 동업체인 조합이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec9.partnership_victim_breach`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의
- 주관적 요건 중 불법영득·이득의사가 인정됨
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `breach_of_trust.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `breach_of_trust.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.business_loss_alone_insufficient`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.no_breach_of_trust_without_awareness`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_for_principal_no_illicit_gain`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.assigned_claim_proceeds_embezzlement`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.leasehold_transfer`, `art355_sec5_2.movable_sale_double_disposition`, `art355_sec5_2.pre_certificate_stock_transfer`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.registered_movable_sale_disposition`, `art355_sec5_2.right_transfer_ordinary_duty`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`, `art356_sec3_2.assistant_other_affairs`, `art356_sec3_2.business_other_affairs_definition`, `art356_sec3_2.other_affairs_origin`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `breach_of_trust.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `breach_of_trust.aggravation.occupational.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무를 처리하는 자에는 고유 권한으로 처리하는 사람뿐 아니라 보조기관으로서 직접 또는 간접으로 그 처리 사무를 담당하는 사람도 포함된다.

연결 NormCard: `art356_sec3_2.assistant_other_affairs`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `breach_of_trust.aggravation.occupational.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상배임죄에서 업무상 타인의 사무를 처리하는 자는 업무자가 업무 수행으로 타인의 사무를 처리하는 지위에 있는 경우이며, 그 신임관계가 업무상 지위와 결부되어 성립한다.

연결 NormCard: `art356_sec3_2.business_other_affairs_definition`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `breach_of_trust.aggravation.occupational.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상 타인의 사무 처리는 업무상 지위에 따라 당연히 사무를 처리하게 된 경우와 업무자에 대한 위임자의 구체적 위임행위로 사무를 처리하게 된 경우 모두에 해당한다.

연결 NormCard: `art356_sec3_2.other_affairs_origin`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `breach_of_trust.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art355.breach.confidential-information`, `art355.breach.duty-definition`, `art355.breach.invalid-act-risk`, `art355.breach_other_affairs_processor`, `art355.breach_right_transfer_general`, `art355_sec1_1.breach_of_trust`, `art355_sec1_2.breach_of_trust_betrayal_theory`, `art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss`, `art355_sec3.breach_of_trust.objective_elements`, `art355_sec4_1.breach_of_trust_intent_elements`, `art355_sec4_1.breach_of_trust_intent_no_purpose`, `art355_sec4_1.business_judgment_intent`, `art355_sec4_1.double_sale_unjustified_rescission_intent`, `art355_sec4_1.role_violation_intent`, `art355_sec4_2.breach_illicit_gain_intent`, `art355_sec4_2.breach_illicit_gain_separate_requirement`, `art355_sec4_2.mixed_motives_primary_purpose`, `art355_sec4_2.third_party_benefit_sufficient`, `art355_sec5_2.individual_delegation_exception`, `art355_sec5_2.real_estate_double_sale_majority`, `art355_sec5_2.real_estate_sale_intermediate_payment`, `art355_sec5_2.real_estate_transfer_exception`, `art355_sec5_2.trust_relationship_threshold`, `art355_sec9.partnership_victim_breach`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
