# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.breach_of_trust_bribe.full.v1_candidate`
- predicate: 99개
- rule: 198개
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

### `breach_of_trust_bribe_case_roles(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art357_protected_interest_integrity(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357.protected_interest.integrity`

### `satisfied_art357_protected_interest_integrity(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`

### `assess_art357_sec1_2_third_party_acquisition(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec1_2.third_party_acquisition`

### `satisfied_art357_sec1_2_third_party_acquisition(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_2.third_party_acquisition`

### `assess_art357_sec1_3_receipt_no_breach_or_loss_requirement(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

### `satisfied_art357_sec1_3_receipt_no_breach_or_loss_requirement(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

### `assess_art357_sec1_3_receipt_required_elements(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec1_3.receipt.required_elements`

### `satisfied_art357_sec1_3_receipt_required_elements(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_3.receipt.required_elements`

### `assess_art357_sec1_4_actual_acquisition(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec1_4.actual_acquisition`

### `satisfied_art357_sec1_4_actual_acquisition(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_4.actual_acquisition`

### `assess_art357_sec3_1_future_duty_expected(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_1.future_duty_expected`

### `satisfied_art357_sec3_1_future_duty_expected(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.future_duty_expected`

### `assess_art357_sec3_1_mere_contractual_debt_exclusion(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

### `satisfied_art357_sec3_1_mere_contractual_debt_exclusion(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

### `assess_art357_sec3_1_no_status_at_request(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_1.no_status_at_request`

### `satisfied_art357_sec3_1_no_status_at_request(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.no_status_at_request`

### `assess_art357_sec3_1_status_assessment(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_1.status_assessment`

### `satisfied_art357_sec3_1_status_assessment(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.status_assessment`

### `assess_art357_sec3_1_subject_no_external_authority(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec3_1.subject_no_external_authority`

### `satisfied_art357_sec3_1_subject_no_external_authority(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.subject_no_external_authority`

### `assess_art357_sec3_1_subject_trust_relationship(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_1.subject_trust_relationship`

### `satisfied_art357_sec3_1_subject_trust_relationship(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.subject_trust_relationship`

### `assess_art357_sec3_1_trust_relationship_sources(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec3_1.trust_relationship_sources`

### `satisfied_art357_sec3_1_trust_relationship_sources(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.trust_relationship_sources`

### `assess_art357_sec3_2_contract_counterparty_request(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.contract_counterparty_request`

### `satisfied_art357_sec3_2_contract_counterparty_request(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.contract_counterparty_request`

### `assess_art357_sec3_2_giver_not_necessarily_liable(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

### `satisfied_art357_sec3_2_giver_not_necessarily_liable(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

### `assess_art357_sec3_2_improper_request_standard(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.improper_request_standard`

### `satisfied_art357_sec3_2_improper_request_standard(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.improper_request_standard`

### `assess_art357_sec3_2_improper_solicitation_comprehensive_assessment(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

### `satisfied_art357_sec3_2_improper_solicitation_comprehensive_assessment(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

### `assess_art357_sec3_2_paid_news_request(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.paid_news_request`

### `satisfied_art357_sec3_2_paid_news_request(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.paid_news_request`

### `assess_art357_sec3_2_permitted_favor_request(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.permitted_favor_request`

### `satisfied_art357_sec3_2_permitted_favor_request(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.permitted_favor_request`

### `assess_art357_sec3_2_request_concerning_duty(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.request_concerning_duty`

### `satisfied_art357_sec3_2_request_concerning_duty(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.request_concerning_duty`

### `assess_art357_sec3_2_request_consideration_link(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.request_consideration_link`

### `satisfied_art357_sec3_2_request_consideration_link(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.request_consideration_link`

### `assess_art357_sec3_2_scope_of_duty(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.scope_of_duty`

### `satisfied_art357_sec3_2_scope_of_duty(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.scope_of_duty`

### `assess_art357_sec3_2_self_rights_protection_not_improper(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

### `satisfied_art357_sec3_2_self_rights_protection_not_improper(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

### `assess_art357_sec3_3_account_control_acquisition(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.account_control_acquisition`

### `satisfied_art357_sec3_3_account_control_acquisition(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.account_control_acquisition`

### `assess_art357_sec3_3_actual_acquisition_required(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec3_3.actual_acquisition_required`

### `satisfied_art357_sec3_3_actual_acquisition_required(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.actual_acquisition_required`

### `assess_art357_sec3_3_benefit_consideration_link(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.benefit_consideration_link`

### `satisfied_art357_sec3_3_benefit_consideration_link(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.benefit_consideration_link`

### `assess_art357_sec3_3_mixed_consideration_entire_benefit(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

### `satisfied_art357_sec3_3_mixed_consideration_entire_benefit(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

### `assess_art357_sec3_3_nominal_stock_sale_consideration(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

### `satisfied_art357_sec3_3_nominal_stock_sale_consideration(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

### `assess_art357_sec3_3_post_resignation_receipt(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.post_resignation_receipt`

### `satisfied_art357_sec3_3_post_resignation_receipt(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.post_resignation_receipt`

### `assess_art357_sec3_3_principal_not_third_party_precedent(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

### `satisfied_art357_sec3_3_principal_not_third_party_precedent(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

### `assess_art357_sec3_3_principal_payment_direct_receipt_equivalent(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

### `satisfied_art357_sec3_3_principal_payment_direct_receipt_equivalent(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

### `assess_art357_sec3_3_unrelated_payment_no_offense(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

### `satisfied_art357_sec3_3_unrelated_payment_no_offense(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

### `assess_art357_sec3_4_illegal_appropriation_intent_separate(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

### `satisfied_art357_sec3_4_illegal_appropriation_intent_separate(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

### `assess_art357_sec3_4_intent_elements(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_4.intent_elements`

### `satisfied_art357_sec3_4_intent_elements(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_4.intent_elements`

### `assess_art357_sec3_4_no_acquisition_intent(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_4.no_acquisition_intent`

### `satisfied_art357_sec3_4_no_acquisition_intent(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_4.no_acquisition_intent`

### `assess_art357_sec3_5_attempt_majority(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec3_5.attempt_majority`

### `satisfied_art357_sec3_5_attempt_majority(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_5.attempt_majority`

### `assess_art357_sec3_5_completion_time(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec3_5.completion_time`

### `satisfied_art357_sec3_5_completion_time(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_5.completion_time`

### `assess_art357_sec3_5_no_corrupt_performance_required(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

### `satisfied_art357_sec3_5_no_corrupt_performance_required(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

### `assess_art357_sec4_giver_view_justification(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec4.giver_view_justification`

### `satisfied_art357_sec4_giver_view_justification(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec4.giver_view_justification`

### `assess_art357_sec4_giving_completion_actual_provision(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec4.giving_completion_actual_provision`

### `satisfied_art357_sec4_giving_completion_actual_provision(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec4.giving_completion_actual_provision`

### `assess_art357_sec4_giving_offense_definition(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art357_sec4.giving_offense_definition`

### `satisfied_art357_sec4_giving_offense_definition(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec4.giving_offense_definition`

### `assess_art357_sec4_giving_to_business_handler(case_id: String, assessment_id: String, receiver_id: String, giver_id: String, principal_id: String, status: String)`

이 카드의 사건별 적용 평가: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art357_sec4.giving_to_business_handler`

### `satisfied_art357_sec4_giving_to_business_handler(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_object_satisfied(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_2.third_party_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`

### `breach_of_trust_bribe_conduct_satisfied(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec4.giving_offense_definition`

### `breach_of_trust_bribe_intent_satisfied(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`

### `breach_of_trust_bribe_completion_satisfied(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`

### `breach_of_trust_bribe_elements_satisfied(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

### `breach_of_trust_bribe_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.no_acquisition_intent`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.no_breach_or_loss_requirement`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_no_external_authority`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_4.no_acquisition_intent`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec3_5.no_corrupt_performance_required`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`, `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.no_breach_or_loss_requirement`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_no_external_authority`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_4.no_acquisition_intent`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec3_5.no_corrupt_performance_required`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`, `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.no_acquisition_intent`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.no_breach_or_loss_requirement`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_no_external_authority`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_4.no_acquisition_intent`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec3_5.no_corrupt_performance_required`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`, `art357_sec4.giving_to_business_handler`

### `breach_of_trust_bribe_established(case_id: String, receiver_id: String, giver_id: String, principal_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

### `breach_of_trust_bribe_requirement_waived(case_id: String, defendant_id: String, issue_id: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`, `art357_sec3_1.subject_no_external_authority`, `art357_sec3_5.no_corrupt_performance_required`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

## Rules

### `breach_of_trust_bribe.art357.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357.protected_interest.integrity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357.protected_interest.integrity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357.protected_interest.integrity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec1_2.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_2.third_party_acquisition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec1_2.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_2.third_party_acquisition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec1_2.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_2.third_party_acquisition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec1_3.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec1_3.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec1_3.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec1_3.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.required_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec1_3.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.required_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec1_3.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.required_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec1_4.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_4.actual_acquisition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec1_4.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_4.actual_acquisition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec1_4.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_4.actual_acquisition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.future_duty_expected`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.future_duty_expected`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.future_duty_expected`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.no_status_at_request`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.no_status_at_request`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.no_status_at_request`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.status_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.status_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.status_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_no_external_authority`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_no_external_authority`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_no_external_authority`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_trust_relationship`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_trust_relationship`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_trust_relationship`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_1.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.trust_relationship_sources`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_1.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.trust_relationship_sources`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_1.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.trust_relationship_sources`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.contract_counterparty_request`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.contract_counterparty_request`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.contract_counterparty_request`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_request_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_request_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_request_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.paid_news_request`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.paid_news_request`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.paid_news_request`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.permitted_favor_request`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.permitted_favor_request`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.permitted_favor_request`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_concerning_duty`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_concerning_duty`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_concerning_duty`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_consideration_link`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_consideration_link`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_consideration_link`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.scope_of_duty`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.scope_of_duty`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.scope_of_duty`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_2.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_2.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_2.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.account_control_acquisition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.account_control_acquisition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.account_control_acquisition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.actual_acquisition_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.actual_acquisition_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.actual_acquisition_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.benefit_consideration_link`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.benefit_consideration_link`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.benefit_consideration_link`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.post_resignation_receipt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.post_resignation_receipt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.post_resignation_receipt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_3.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_3.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_3.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_4.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_4.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_4.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_4.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.intent_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_4.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.intent_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_4.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.intent_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_4.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.no_acquisition_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_4.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.no_acquisition_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_4.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.no_acquisition_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_5.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.attempt_majority`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_5.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.attempt_majority`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_5.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.attempt_majority`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_5.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.completion_time`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_5.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.completion_time`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_5.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.completion_time`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec3_5.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec3_5.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec3_5.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec4.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giver_view_justification`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec4.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giver_view_justification`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec4.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giver_view_justification`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec4.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_completion_actual_provision`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec4.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_completion_actual_provision`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec4.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_completion_actual_provision`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec4.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_offense_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec4.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_offense_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec4.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_offense_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec4.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_to_business_handler`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `breach_of_trust_bribe.art357_sec4.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_to_business_handler`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `breach_of_trust_bribe.art357_sec4.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_to_business_handler`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `breach_of_trust_bribe.art357_sec1_2.component.breach_of_trust_bribe_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.

연결 NormCard: `art357_sec1_2.third_party_acquisition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_1.component.breach_of_trust_bribe_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.

연결 NormCard: `art357_sec3_1.future_duty_expected`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_1.component.breach_of_trust_bribe_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.

연결 NormCard: `art357_sec3_1.status_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_1.component.breach_of_trust_bribe_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.

연결 NormCard: `art357_sec3_1.subject_trust_relationship`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_1.component.breach_of_trust_bribe_object_satisfied.05`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.

연결 NormCard: `art357_sec3_1.trust_relationship_sources`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.06`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.

연결 NormCard: `art357_sec3_3.account_control_acquisition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.07`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.

연결 NormCard: `art357_sec3_3.actual_acquisition_required`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.08`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.

연결 NormCard: `art357_sec3_3.benefit_consideration_link`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.09`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.

연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.10`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.

연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.11`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.

연결 NormCard: `art357_sec3_3.post_resignation_receipt`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_3.component.breach_of_trust_bribe_object_satisfied.12`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.

연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357.component.breach_of_trust_bribe_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.

연결 NormCard: `art357.protected_interest.integrity`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec1_3.component.breach_of_trust_bribe_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.

연결 NormCard: `art357_sec1_3.receipt.required_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec1_4.component.breach_of_trust_bribe_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.

연결 NormCard: `art357_sec1_4.actual_acquisition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.

연결 NormCard: `art357_sec3_2.contract_counterparty_request`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.

연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.

연결 NormCard: `art357_sec3_2.improper_request_standard`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.

연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.08`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.

연결 NormCard: `art357_sec3_2.paid_news_request`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.09`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.

연결 NormCard: `art357_sec3_2.request_concerning_duty`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.10`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.

연결 NormCard: `art357_sec3_2.request_consideration_link`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_2.component.breach_of_trust_bribe_conduct_satisfied.11`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.

연결 NormCard: `art357_sec3_2.scope_of_duty`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec4.component.breach_of_trust_bribe_conduct_satisfied.12`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.

연결 NormCard: `art357_sec4.giving_offense_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_4.component.breach_of_trust_bribe_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.

연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_4.component.breach_of_trust_bribe_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.

연결 NormCard: `art357_sec3_4.intent_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_5.component.breach_of_trust_bribe_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.

연결 NormCard: `art357_sec3_5.attempt_majority`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_5.component.breach_of_trust_bribe_completion_satisfied.02`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.

연결 NormCard: `art357_sec3_5.completion_time`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec4.component.breach_of_trust_bribe_completion_satisfied.03`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.

연결 NormCard: `art357_sec4.giving_completion_actual_provision`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `breach_of_trust_bribe.art357_sec3_1.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 통상의 민사상 계약에서 이익이 대립하는 관계에 따른 채무를 부담하는 것만으로는 타인의 사무에 해당하지 않는다.

연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_1.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 원칙적으로 타인의 사무처리자 지위를 취득하기 전에 부정한 청탁을 받은 경우에는 배임수재죄의 주체에 해당하지 않는다.

연결 NormCard: `art357_sec3_1.no_status_at_request`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 직무권한 범위 안에서 편의를 봐 달라는 부탁이나 규정이 허용하는 범위에서 최대한 선처를 바란다는 부탁은 부정한 청탁이 아니다.

연결 NormCard: `art357_sec3_2.permitted_favor_request`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.

연결 NormCard: `art357_sec3_2.self_rights_protection_not_improper`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_3.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 개정 형법이 적용되는 경우에도 특별한 사정이 없는 한 사무처리를 위임한 타인은 제3자에 포함되지 않는다.

연결 NormCard: `art357_sec3_3.principal_not_third_party_precedent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_3.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부정한 청탁이 있었더라도 이를 받아들이지 않고 청탁과 관계없이 돈을 받은 경우에는 배임수재죄가 성립하지 않는다.

연결 NormCard: `art357_sec3_3.unrelated_payment_no_offense`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec3_4.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 취득할 의사 없이 보관 목적으로 받거나 특별한 사정으로 일시 수령 후 즉시 반환하는 등 취득 의사를 인정하기 어려운 경우에는 영득의 의사가 없어 배임수재죄가 성립할 수 없다.

연결 NormCard: `art357_sec3_4.no_acquisition_intent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec4.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다.

연결 NormCard: `art357_sec4.giver_view_justification`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357_sec4.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다.

연결 NormCard: `art357_sec4.giving_to_business_handler`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `breach_of_trust_bribe.art357.mandatory_negative.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357.protected_interest.integrity`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec1_2.mandatory_negative.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 2016년 개정 후에는 행위자가 직접 취득하는 경우뿐 아니라 제3자로 하여금 재물 또는 재산상 이익을 취득하게 하는 행위도 처벌할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_2.third_party_acquisition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec1_3.mandatory_negative.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_3.receipt.required_elements`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec1_4.mandatory_negative.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec1_4.actual_acquisition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_1.mandatory_negative.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 신임관계에 기한 사무 범위에 속하고 장래 담당할 것이 합리적으로 기대되는 임무에 관하여 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 후 그 임무를 현실적으로 담당하게 되면 배임수재죄 성립을 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.future_duty_expected`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_1.mandatory_negative.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위는 법령의 구체적 규정, 정관 및 업무의 성격과 내용을 면밀히 검토하여 판단해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.status_assessment`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_1.mandatory_negative.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄의 주체인 타인의 사무를 처리하는 자란, 타인과의 대내관계에서 신의성실 원칙상 그 사무를 처리할 신임관계가 존재한다고 인정되는 자이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.subject_trust_relationship`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_1.mandatory_negative.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 사무처리자 지위의 신임관계는 법령의 규정, 법률행위, 관습 또는 사무관리에 의하여 발생할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_1.trust_relationship_sources`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 위탁을 받아 계약 관련 사무를 처리하는 사람이 특정인으로부터 계약 상대방이 되게 해 달라는 부탁과 그 대가로 돈을 받은 경우, 특별한 사정이 없는 한 부정한 청탁에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.contract_counterparty_request`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄와 배임증재죄가 통상 필요적 공범 관계에 있더라도 수재자와 증재자가 반드시 함께 처벌되어야 하는 것은 아니며, 증재자에게 정당한 업무 청탁이 수재자에게는 부정한 청탁이 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.giver_not_necessarily_liable`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁은 업무상 배임 수준에 이를 필요는 없고 사회상규 또는 신의성실 원칙에 반하는 내용이면 충분하며, 청탁 내용, 대가의 액수ㆍ형식 및 거래의 청렴성 등을 종합해 판단하고 반드시 명시적일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_request_standard`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관한 부정한 청탁 여부는 청탁 내용, 관련하여 취득한 재물·재산상 이익의 종류·액수·형식, 제공 방법과 태양 및 거래의 청렴성 등을 종합하여 개별적·구체적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.improper_solicitation_comprehensive_assessment`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보도 대상자가 언론사 기자에게 유료기사 게재를 청탁하는 행위는 광고를 언론보도처럼 가장하도록 하는 것으로서 부정한 청탁에 해당하며, 기사의 내용이 객관적 사실에 부합하더라도 같다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.paid_news_request`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 임무에 관하여 부정한 청탁을 받을 것을 요건으로 하며, 사무처리자가 부정한 청탁을 받았더라도 임무와 관계없이 받은 경우에는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_concerning_duty`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄에서 취득하는 재물 또는 재산상 이익은 부정한 청탁에 대한 대가 또는 사례여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.request_consideration_link`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_2.mandatory_negative.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 임무에 관하여란 위탁관계에 따른 본래 사무뿐 아니라 그와 밀접한 관계가 있는 범위의 사무를 포함하고, 고유 권한자뿐 아니라 보조기관으로 직접 또는 간접으로 처리 사무를 담당하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_2.scope_of_duty`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.017`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 증재자가 입금한 계좌의 통장 또는 인출 가능한 카드 등을 교부받아 언제든 인출할 수 있고 예금에 대한 실질적 사용·처분권한을 가지면, 예금된 돈을 취득한 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.account_control_acquisition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.018`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 현실적 취득을 뜻하며, 단순한 요구 또는 약속만으로는 취득에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.actual_acquisition_required`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.019`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 또는 재산상 이익의 취득은 부정한 청탁에 대한 대가·사례 또는 묵인조로 받은 경우처럼 부정한 청탁과 관련되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.benefit_consideration_link`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.020`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공여 금품에 부정한 청탁의 대가 성질과 다른 행위에 대한 사례 성질이 불가분적으로 결합된 경우, 그 전부가 불가분적으로 부정한 청탁의 대가 성질을 가진다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.mixed_consideration_entire_benefit`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.021`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주식 매각의 형식으로 대금이 교부되었더라도 매도 주식의 재산적 가치가 거의 없다면, 그 대금은 부정한 청탁의 대가로 교부된 것으로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.nominal_stock_sale_consideration`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.022`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 받은 뒤 업무를 떠나거나 사직한 후 재물 또는 재산상 이익을 수수하더라도, 그것이 청탁의 대가이면 배임수재죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.post_resignation_receipt`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_3.mandatory_negative.023`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 외형상 사무처리를 위임한 타인에게 이익이 지급되었더라도, 사회통념상 그 타인의 수령을 부정한 청탁을 받은 사람이 직접 받은 것과 동일하게 평가할 수 있으면 배임수재죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_3.principal_payment_direct_receipt_equivalent`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_4.mandatory_negative.024`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.illegal_appropriation_intent_separate`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_4.mandatory_negative.025`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 사무를 처리하는 자로서 임무에 관한 부정한 청탁이 있고 재물 또는 재산상 이익을 취득한다는 점에 대한 의사를 가져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_4.intent_elements`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_5.mandatory_negative.026`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부정한 청탁을 전제로 재물 또는 재산상 이익을 요구·약속하거나 공여의 의사를 표시한 경우에는 배임수증재죄의 미수가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.attempt_majority`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec3_5.mandatory_negative.027`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임수재죄는 부정한 청탁을 받고 재물 또는 재산상 이익을 취득한 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec3_5.completion_time`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec4.mandatory_negative.028`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_completion_actual_provision`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.art357_sec4.mandatory_negative.029`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art357_sec4.giving_offense_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `breach_of_trust_bribe.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `breach_of_trust_bribe.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.no_acquisition_intent`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_to_business_handler`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `breach_of_trust_bribe.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.no_breach_or_loss_requirement`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.mere_contractual_debt_exclusion`, `art357_sec3_1.no_status_at_request`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_no_external_authority`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.permitted_favor_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_2.self_rights_protection_not_improper`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_not_third_party_precedent`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_3.unrelated_payment_no_offense`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_4.no_acquisition_intent`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec3_5.no_corrupt_performance_required`, `art357_sec4.giver_view_justification`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`, `art357_sec4.giving_to_business_handler`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `breach_of_trust_bribe.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `breach_of_trust_bribe.art357_sec1_3.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다.

연결 NormCard: `art357_sec1_3.receipt.no_breach_or_loss_requirement`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `breach_of_trust_bribe.art357_sec3_1.requirement_waived.002`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 사무처리자에게 제3자에 대한 대외적 권한이나 포괄적 위탁사무가 요구되지는 않는다.

연결 NormCard: `art357_sec3_1.subject_no_external_authority`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `breach_of_trust_bribe.art357_sec3_5.requirement_waived.003`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 배임수재죄의 기수에는 청탁에 상응하는 부정행위 또는 배임행위까지 나아갈 것이 요구되지 않는다.

연결 NormCard: `art357_sec3_5.no_corrupt_performance_required`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `breach_of_trust_bribe.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art357.protected_interest.integrity`, `art357_sec1_2.third_party_acquisition`, `art357_sec1_3.receipt.required_elements`, `art357_sec1_4.actual_acquisition`, `art357_sec3_1.future_duty_expected`, `art357_sec3_1.status_assessment`, `art357_sec3_1.subject_trust_relationship`, `art357_sec3_1.trust_relationship_sources`, `art357_sec3_2.contract_counterparty_request`, `art357_sec3_2.giver_not_necessarily_liable`, `art357_sec3_2.improper_request_standard`, `art357_sec3_2.improper_solicitation_comprehensive_assessment`, `art357_sec3_2.paid_news_request`, `art357_sec3_2.request_concerning_duty`, `art357_sec3_2.request_consideration_link`, `art357_sec3_2.scope_of_duty`, `art357_sec3_3.account_control_acquisition`, `art357_sec3_3.actual_acquisition_required`, `art357_sec3_3.benefit_consideration_link`, `art357_sec3_3.mixed_consideration_entire_benefit`, `art357_sec3_3.nominal_stock_sale_consideration`, `art357_sec3_3.post_resignation_receipt`, `art357_sec3_3.principal_payment_direct_receipt_equivalent`, `art357_sec3_4.illegal_appropriation_intent_separate`, `art357_sec3_4.intent_elements`, `art357_sec3_5.attempt_majority`, `art357_sec3_5.completion_time`, `art357_sec4.giving_completion_actual_provision`, `art357_sec4.giving_offense_definition`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
