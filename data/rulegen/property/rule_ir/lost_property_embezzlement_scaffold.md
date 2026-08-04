# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.lost_property_embezzlement.full.v1_candidate`
- predicate: 59개
- rule: 86개
- NormCard: 14개

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

### `lost_property_embezzlement_case_roles(case_id: String, defendant_id: String, owner_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art360_sec1_1_offense_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art360_sec1_1.offense_definition`

### `satisfied_art360_sec1_1_offense_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`

### `not_satisfied_satisfied_art360_sec1_1_offense_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`

### `assess_art360_sec2_1_subject_unrestricted(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art360_sec2_1.subject.unrestricted`

### `satisfied_art360_sec2_1_subject_unrestricted(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 주체에는 제한이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_1.subject.unrestricted`

### `not_satisfied_satisfied_art360_sec2_1_subject_unrestricted(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 주체에는 제한이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_1.subject.unrestricted`

### `assess_art360_sec2_2_lost_possession_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_2.lost_possession_property`

### `satisfied_art360_sec2_2_lost_possession_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.lost_possession_property`

### `not_satisfied_satisfied_art360_sec2_2_lost_possession_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.lost_possession_property`

### `assess_art360_sec2_2_managed_place_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_2.managed_place_property`

### `satisfied_art360_sec2_2_managed_place_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`

### `not_satisfied_satisfied_art360_sec2_2_managed_place_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`

### `assess_art360_sec2_2_mistaken_bank_transfer_embezzlement_holding(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

### `satisfied_art360_sec2_2_mistaken_bank_transfer_embezzlement_holding(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

### `not_satisfied_satisfied_art360_sec2_2_mistaken_bank_transfer_embezzlement_holding(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

### `assess_art360_sec2_2_object(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art360_sec2_2.object`

### `satisfied_art360_sec2_2_object(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.object`

### `not_satisfied_satisfied_art360_sec2_2_object(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.object`

### `assess_art360_sec2_2_original_possessor_recovery(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_2.original_possessor_recovery`

### `satisfied_art360_sec2_2_original_possessor_recovery(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.original_possessor_recovery`

### `not_satisfied_satisfied_art360_sec2_2_original_possessor_recovery(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.original_possessor_recovery`

### `assess_art360_sec2_2_ownerless_property_exclusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

### `satisfied_art360_sec2_2_ownerless_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

### `not_satisfied_satisfied_art360_sec2_2_ownerless_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

### `assess_art360_sec2_2_public_transport_found_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_2.public_transport_found_property`

### `satisfied_art360_sec2_2_public_transport_found_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.public_transport_found_property`

### `not_satisfied_satisfied_art360_sec2_2_public_transport_found_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.public_transport_found_property`

### `assess_art360_sec2_3_completion_external_expression(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_3.completion_external_expression`

### `satisfied_art360_sec2_3_completion_external_expression(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.completion_external_expression`

### `not_satisfied_satisfied_art360_sec2_3_completion_external_expression(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.completion_external_expression`

### `assess_art360_sec2_3_embezzlement_act(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_3.embezzlement_act`

### `satisfied_art360_sec2_3_embezzlement_act(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.embezzlement_act`

### `not_satisfied_satisfied_art360_sec2_3_embezzlement_act(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.embezzlement_act`

### `assess_art360_sec2_3_later_appropriation_intent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_3.later_appropriation_intent`

### `satisfied_art360_sec2_3_later_appropriation_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.later_appropriation_intent`

### `not_satisfied_satisfied_art360_sec2_3_later_appropriation_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.later_appropriation_intent`

### `assess_art360_sec2_3_mistake_property_status_punishable(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

### `satisfied_art360_sec2_3_mistake_property_status_punishable(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

### `not_satisfied_satisfied_art360_sec2_3_mistake_property_status_punishable(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

### `assess_art360_sec2_3_reporting_noncompliance_alone(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

### `satisfied_art360_sec2_3_reporting_noncompliance_alone(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

### `not_satisfied_satisfied_art360_sec2_3_reporting_noncompliance_alone(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_object_satisfied(case_id: String, defendant_id: String, owner_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`

### `lost_property_embezzlement_conduct_satisfied(case_id: String, defendant_id: String, owner_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.mistake_property_status_punishable`

### `lost_property_embezzlement_completion_satisfied(case_id: String, defendant_id: String, owner_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_3.later_appropriation_intent`

### `lost_property_embezzlement_elements_satisfied(case_id: String, defendant_id: String, owner_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

### `lost_property_embezzlement_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.object`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`, `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.object`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`, `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.object`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`, `art360_sec2_3.reporting_noncompliance_alone`

### `lost_property_embezzlement_established(case_id: String, defendant_id: String, owner_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

### `lost_property_embezzlement_boundary_shift(case_id: String, defendant_id: String, issue_id: String)`

이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.public_transport_found_property`

### `lost_property_embezzlement_refers_to_crime(case_id: String, defendant_id: String, crime_name: String)`

이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.public_transport_found_property`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

## Rules

### `lost_property_embezzlement.art360_sec1_1.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec1_1.offense_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec1_1.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec1_1.offense_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec1_1.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec1_1.offense_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec1_1.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec1_1.offense_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_1.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 주체에는 제한이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_1.subject.unrestricted`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_1.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_1.subject.unrestricted`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_1.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_1.subject.unrestricted`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_1.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 주체에는 제한이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_1.subject.unrestricted`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.lost_possession_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.lost_possession_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.lost_possession_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.lost_possession_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.object`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_2.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_2.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_2.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.completion_external_expression`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.completion_external_expression`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_3.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.completion_external_expression`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_3.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.completion_external_expression`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.embezzlement_act`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.embezzlement_act`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_3.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.embezzlement_act`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_3.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.embezzlement_act`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_3.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_3.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_3.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_3.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec2_3.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `lost_property_embezzlement.art360_sec2_3.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `lost_property_embezzlement.art360_sec2_3.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `lost_property_embezzlement.art360_sec1_1.component.lost_property_embezzlement_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.

연결 NormCard: `art360_sec1_1.offense_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_1.component.lost_property_embezzlement_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 주체에는 제한이 없다.

연결 NormCard: `art360_sec2_1.subject.unrestricted`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_2.component.lost_property_embezzlement_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.

연결 NormCard: `art360_sec2_2.lost_possession_property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_2.component.lost_property_embezzlement_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.

연결 NormCard: `art360_sec2_2.object`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_3.component.lost_property_embezzlement_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.

연결 NormCard: `art360_sec2_3.completion_external_expression`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_3.component.lost_property_embezzlement_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.

연결 NormCard: `art360_sec2_3.embezzlement_act`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_3.component.lost_property_embezzlement_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.

연결 NormCard: `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_3.component.lost_property_embezzlement_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `lost_property_embezzlement.art360_sec2_2.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.art360_sec2_2.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.art360_sec2_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.art360_sec2_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 무주물은 타인 소유의 재물이 아니므로 점유이탈물횡령죄의 객체가 아니다.

연결 NormCard: `art360_sec2_2.ownerless_property_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.art360_sec2_2.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.art360_sec2_3.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 유실물·표류물·매장물에 관하여 법정 절차를 밟지 않았다는 사정만으로 점유이탈물횡령죄가 성립하는 것은 아니다.

연결 NormCard: `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `lost_property_embezzlement.component.l0.mandatory_negative.01`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 유실물·표류물·타인의 점유를 이탈한 재물 또는 매장물을 횡령함으로써 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 주체에는 제한이 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물이란 원래 점유자의 의사에 기하지 않고 그 점유를 벗어난 타인 소유 재물이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄의 객체는 타인 소유의 점유이탈물이다.

연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`

검토 메모: 구성요건 L0에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `lost_property_embezzlement.component.l1.mandatory_negative.02`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령죄는 불법영득의사를 외부에 표현하는 행위로 완성된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 점유이탈물횡령의 행위는 불법영득의사로 점유이탈물을 자기의 사실상 지배 아래 두는 행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.

연결 NormCard: `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `lost_property_embezzlement.component.l4.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 불법영득의사 없이 점유이탈물을 습득했더라도, 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수가 된다.

연결 NormCard: `art360_sec2_3.later_appropriation_intent`

검토 메모: 구성요건 L4에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `lost_property_embezzlement.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분
- 실행행위 요건이 충족됨
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `lost_property_embezzlement.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `lost_property_embezzlement.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.managed_place_property`, `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`, `art360_sec2_2.object`, `art360_sec2_2.original_possessor_recovery`, `art360_sec2_2.ownerless_property_exclusion`, `art360_sec2_2.public_transport_found_property`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`, `art360_sec2_3.reporting_noncompliance_alone`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `lost_property_embezzlement.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `lost_property_embezzlement.art360_sec2_2.boundary_shift.001`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `lost_property_embezzlement.art360_sec2_2.boundary_shift.002`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `lost_property_embezzlement.art360_sec2_2.boundary_shift.003`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `lost_property_embezzlement.art360_sec2_2.boundary_shift.004`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `lost_property_embezzlement.art360_sec2_2.refers_to_crime.001`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 간수·관리 등 실력적 지배가 미치는 장소 안에 방치되거나 유류된 물건은 관리자의 점유에 속하여 점유이탈물이 아니고, 영득 시 절도죄의 객체가 된다.

연결 NormCard: `art360_sec2_2.managed_place_property`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `lost_property_embezzlement.art360_sec2_2.refers_to_crime.002`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.

연결 NormCard: `art360_sec2_2.mistaken_bank_transfer_embezzlement_holding`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `lost_property_embezzlement.art360_sec2_2.refers_to_crime.003`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 원점유자가 물건 소재를 알고 다시 찾을 가능성이 있는 경우에는 타인의 점유가 존속하므로, 이를 영득하면 점유이탈물횡령죄가 아니라 절도죄가 성립한다.

연결 NormCard: `art360_sec2_2.original_possessor_recovery`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `lost_property_embezzlement.art360_sec2_2.refers_to_crime.004`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 운전사나 승무원이 유실물을 현실적으로 발견한 뒤 제3자가 가져가면 운전사·승무원의 점유가 인정되어 절도죄로 처벌된다.

연결 NormCard: `art360_sec2_2.public_transport_found_property`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `lost_property_embezzlement.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art360_sec1_1.offense_definition`, `art360_sec2_1.subject.unrestricted`, `art360_sec2_2.lost_possession_property`, `art360_sec2_2.object`, `art360_sec2_3.completion_external_expression`, `art360_sec2_3.embezzlement_act`, `art360_sec2_3.later_appropriation_intent`, `art360_sec2_3.mistake_property_status_punishable`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
