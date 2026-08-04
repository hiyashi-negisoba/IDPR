# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.interference_with_exercise_of_right.full.v1_candidate`
- predicate: 113개
- rule: 168개
- NormCard: 32개

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

### `interference_with_exercise_of_right_case_roles(case_id: String, defendant_id: String, right_holder_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art323_forced_execution_evasion_scope(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323.forced_execution_evasion_scope`

### `satisfied_art323_forced_execution_evasion_scope(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`

### `not_satisfied_satisfied_art323_forced_execution_evasion_scope(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`

### `assess_art323_sec1_1_abstract_danger_offense(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec1_1.abstract_danger_offense`

### `satisfied_art323_sec1_1_abstract_danger_offense(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.abstract_danger_offense`

### `not_satisfied_satisfied_art323_sec1_1_abstract_danger_offense(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.abstract_danger_offense`

### `assess_art323_sec1_1_conduct_and_object(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec1_1.conduct_and_object`

### `satisfied_art323_sec1_1_conduct_and_object(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.conduct_and_object`

### `not_satisfied_satisfied_art323_sec1_1_conduct_and_object(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.conduct_and_object`

### `assess_art323_sec1_1_no_unlawful_appropriation_intent(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

### `satisfied_art323_sec1_1_no_unlawful_appropriation_intent(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

### `not_satisfied_satisfied_art323_sec1_1_no_unlawful_appropriation_intent(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

### `assess_art323_sec2_1_subject_genuine_status_offense(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

### `satisfied_art323_sec2_1_subject_genuine_status_offense(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

### `not_satisfied_satisfied_art323_sec2_1_subject_genuine_status_offense(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

### `assess_art323_sec2_2_coowned_property_excluded(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.coowned_property_excluded`

### `satisfied_art323_sec2_2_coowned_property_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.coowned_property_excluded`

### `not_satisfied_satisfied_art323_sec2_2_coowned_property_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.coowned_property_excluded`

### `assess_art323_sec2_2_corporate_system_records_other(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.corporate_system_records_other`

### `satisfied_art323_sec2_2_corporate_system_records_other(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.corporate_system_records_other`

### `not_satisfied_satisfied_art323_sec2_2_corporate_system_records_other(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.corporate_system_records_other`

### `assess_art323_sec2_2_electronic_records(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.electronic_records`

### `satisfied_art323_sec2_2_electronic_records(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.electronic_records`

### `not_satisfied_satisfied_art323_sec2_2_electronic_records(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.electronic_records`

### `assess_art323_sec2_2_joint_possession_object(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.joint_possession_object`

### `satisfied_art323_sec2_2_joint_possession_object(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.joint_possession_object`

### `not_satisfied_satisfied_art323_sec2_2_joint_possession_object(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.joint_possession_object`

### `assess_art323_sec2_2_manifestly_no_right_possession_excluded(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

### `satisfied_art323_sec2_2_manifestly_no_right_possession_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

### `not_satisfied_satisfied_art323_sec2_2_manifestly_no_right_possession_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

### `assess_art323_sec2_2_nominee_owner_not_subject(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

### `satisfied_art323_sec2_2_nominee_owner_not_subject(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

### `not_satisfied_satisfied_art323_sec2_2_nominee_owner_not_subject(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

### `assess_art323_sec2_2_nonpossessory_claim_precedent(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

### `satisfied_art323_sec2_2_nonpossessory_claim_precedent(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

### `not_satisfied_satisfied_art323_sec2_2_nonpossessory_claim_precedent(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

### `assess_art323_sec2_2_official_custody_exception(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.official_custody_exception`

### `satisfied_art323_sec2_2_official_custody_exception(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.official_custody_exception`

### `not_satisfied_satisfied_art323_sec2_2_official_custody_exception(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.official_custody_exception`

### `assess_art323_sec2_2_possession_actual_control(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.possession_actual_control`

### `satisfied_art323_sec2_2_possession_actual_control(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.possession_actual_control`

### `not_satisfied_satisfied_art323_sec2_2_possession_actual_control(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.possession_actual_control`

### `assess_art323_sec2_2_prohibited_gold_products_excluded(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

### `satisfied_art323_sec2_2_prohibited_gold_products_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

### `not_satisfied_satisfied_art323_sec2_2_prohibited_gold_products_excluded(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

### `assess_art323_sec2_2_property_movables_real_estate(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.property_movables_real_estate`

### `satisfied_art323_sec2_2_property_movables_real_estate(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.property_movables_real_estate`

### `not_satisfied_satisfied_art323_sec2_2_property_movables_real_estate(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.property_movables_real_estate`

### `assess_art323_sec2_2_protected_possession_potential_value(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

### `satisfied_art323_sec2_2_protected_possession_potential_value(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

### `not_satisfied_satisfied_art323_sec2_2_protected_possession_potential_value(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

### `assess_art323_sec2_2_registered_sale_seller_not_subject(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

### `satisfied_art323_sec2_2_registered_sale_seller_not_subject(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

### `not_satisfied_satisfied_art323_sec2_2_registered_sale_seller_not_subject(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

### `assess_art323_sec2_2_rescinded_sale_recovery(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

### `satisfied_art323_sec2_2_rescinded_sale_recovery(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

### `not_satisfied_satisfied_art323_sec2_2_rescinded_sale_recovery(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

### `assess_art323_sec2_2_retained_title_sale(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.retained_title_sale`

### `satisfied_art323_sec2_2_retained_title_sale(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.retained_title_sale`

### `not_satisfied_satisfied_art323_sec2_2_retained_title_sale(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.retained_title_sale`

### `assess_art323_sec2_2_rightful_possession_definition(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.rightful_possession_definition`

### `satisfied_art323_sec2_2_rightful_possession_definition(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.rightful_possession_definition`

### `not_satisfied_satisfied_art323_sec2_2_rightful_possession_definition(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.rightful_possession_definition`

### `assess_art323_sec2_2_self_property_owner(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec2_2.self_property_owner`

### `satisfied_art323_sec2_2_self_property_owner(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.self_property_owner`

### `not_satisfied_satisfied_art323_sec2_2_self_property_owner(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.self_property_owner`

### `assess_art323_sec2_2_title_transfer_criteria(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_2.title_transfer_criteria`

### `satisfied_art323_sec2_2_title_transfer_criteria(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.title_transfer_criteria`

### `not_satisfied_satisfied_art323_sec2_2_title_transfer_criteria(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.title_transfer_criteria`

### `assess_art323_sec2_3_concealment(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_3.concealment`

### `satisfied_art323_sec2_3_concealment(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.concealment`

### `not_satisfied_satisfied_art323_sec2_3_concealment(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.concealment`

### `assess_art323_sec2_3_consensual_transfer_not_taking(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

### `satisfied_art323_sec2_3_consensual_transfer_not_taking(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

### `not_satisfied_satisfied_art323_sec2_3_consensual_transfer_not_taking(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

### `assess_art323_sec2_3_destruction(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_3.destruction`

### `satisfied_art323_sec2_3_destruction(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.destruction`

### `not_satisfied_satisfied_art323_sec2_3_destruction(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.destruction`

### `assess_art323_sec2_3_risk_to_right_exercise(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

### `satisfied_art323_sec2_3_risk_to_right_exercise(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

### `not_satisfied_satisfied_art323_sec2_3_risk_to_right_exercise(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

### `assess_art323_sec2_3_taking(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec2_3.taking`

### `satisfied_art323_sec2_3_taking(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.taking`

### `not_satisfied_satisfied_art323_sec2_3_taking(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_3.taking`

### `assess_art323_sec3_conditional_intent_sufficient(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec3.conditional_intent_sufficient`

### `satisfied_art323_sec3_conditional_intent_sufficient(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.conditional_intent_sufficient`

### `not_satisfied_satisfied_art323_sec3_conditional_intent_sufficient(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.conditional_intent_sufficient`

### `assess_art323_sec3_no_intent_to_appropriate_required(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

### `satisfied_art323_sec3_no_intent_to_appropriate_required(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

### `not_satisfied_satisfied_art323_sec3_no_intent_to_appropriate_required(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

### `assess_art323_sec3_subjective_awareness(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec3.subjective_awareness`

### `satisfied_art323_sec3_subjective_awareness(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.subjective_awareness`

### `not_satisfied_satisfied_art323_sec3_subjective_awareness(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.subjective_awareness`

### `assess_art323_sec7_family_exception_victim(case_id: String, assessment_id: String, defendant_id: String, right_holder_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art323_sec7.family_exception_victim`

### `satisfied_art323_sec7_family_exception_victim(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec7.family_exception_victim`

### `not_satisfied_satisfied_art323_sec7_family_exception_victim(case_id: String, defendant_id: String, right_holder_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec7.family_exception_victim`

### `interference_with_exercise_of_right_object_ownership_satisfied(case_id: String, defendant_id: String, right_holder_id: String)`

객체 요건 중 타인 소유가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`

### `interference_with_exercise_of_right_object_possession_satisfied(case_id: String, defendant_id: String, right_holder_id: String)`

객체 요건 중 타인 점유가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`

### `interference_with_exercise_of_right_conduct_satisfied(case_id: String, defendant_id: String, right_holder_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`

### `interference_with_exercise_of_right_intent_satisfied(case_id: String, defendant_id: String, right_holder_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

### `interference_with_exercise_of_right_elements_satisfied(case_id: String, defendant_id: String, right_holder_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

### `interference_with_exercise_of_right_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_3.consensual_transfer_not_taking`

### `interference_with_exercise_of_right_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec1_1.no_unlawful_appropriation_intent`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.consensual_transfer_not_taking`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.no_intent_to_appropriate_required`, `art323_sec3.subjective_awareness`, `art323_sec7.family_exception_victim`

### `interference_with_exercise_of_right_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec1_1.no_unlawful_appropriation_intent`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.consensual_transfer_not_taking`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.no_intent_to_appropriate_required`, `art323_sec3.subjective_awareness`, `art323_sec7.family_exception_victim`

### `interference_with_exercise_of_right_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_3.consensual_transfer_not_taking`

### `interference_with_exercise_of_right_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec1_1.no_unlawful_appropriation_intent`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.consensual_transfer_not_taking`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.no_intent_to_appropriate_required`, `art323_sec3.subjective_awareness`, `art323_sec7.family_exception_victim`

### `interference_with_exercise_of_right_established(case_id: String, defendant_id: String, right_holder_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

### `interference_with_exercise_of_right_requirement_waived(case_id: String, defendant_id: String, issue_id: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`, `art323_sec3.no_intent_to_appropriate_required`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

## Rules

### `interference_with_exercise_of_right.art323.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323.forced_execution_evasion_scope`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323.forced_execution_evasion_scope`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323.forced_execution_evasion_scope`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323.forced_execution_evasion_scope`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.abstract_danger_offense`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.abstract_danger_offense`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.abstract_danger_offense`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec1_1.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.abstract_danger_offense`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.conduct_and_object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.conduct_and_object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.conduct_and_object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec1_1.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.conduct_and_object`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec1_1.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec1_1.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_1.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_1.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_1.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_1.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.coowned_property_excluded`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.coowned_property_excluded`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.coowned_property_excluded`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.coowned_property_excluded`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.corporate_system_records_other`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.corporate_system_records_other`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.corporate_system_records_other`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.corporate_system_records_other`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.electronic_records`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.electronic_records`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.electronic_records`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.electronic_records`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.joint_possession_object`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.joint_possession_object`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.joint_possession_object`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.joint_possession_object`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.official_custody_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.official_custody_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.official_custody_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.official_custody_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.possession_actual_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.possession_actual_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.possession_actual_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.possession_actual_control`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.015.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.property_movables_real_estate`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.property_movables_real_estate`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.property_movables_real_estate`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.016.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.property_movables_real_estate`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.017.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.018.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.019.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.retained_title_sale`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.retained_title_sale`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.retained_title_sale`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.020.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.retained_title_sale`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rightful_possession_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rightful_possession_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rightful_possession_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.021.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.rightful_possession_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.self_property_owner`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.self_property_owner`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.self_property_owner`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.022.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.self_property_owner`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.title_transfer_criteria`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.title_transfer_criteria`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_2.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.title_transfer_criteria`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_2.card.023.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_2.title_transfer_criteria`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.concealment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.concealment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.concealment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_3.card.024.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.concealment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_3.card.025.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.destruction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.destruction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.destruction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_3.card.026.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.destruction`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_3.card.027.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec2_3.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec2_3.card.028.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec2_3.taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.conditional_intent_sufficient`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.conditional_intent_sufficient`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec3.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.conditional_intent_sufficient`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec3.card.029.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.conditional_intent_sufficient`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec3.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec3.card.030.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.subjective_awareness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec3.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.subjective_awareness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec3.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.subjective_awareness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec3.card.031.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec3.subjective_awareness`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec7.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec7.family_exception_victim`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec7.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec7.family_exception_victim`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `interference_with_exercise_of_right.art323_sec7.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec7.family_exception_victim`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `interference_with_exercise_of_right.art323_sec7.card.032.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리행사방해죄에서 친족상도례 적용을 위한 피해자는 범인 소유 목적물에 점유 또는 권리를 가진 사람이며, 범행 당시 범인과 그 사람 사이에 친족관계가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art323_sec7.family_exception_victim`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `interference_with_exercise_of_right.art323_sec2_1.component.interference_with_exercise_of_right_object_ownership_satisfied.01`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_ownership_satisfied.02`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.

연결 NormCard: `art323_sec2_2.self_property_owner`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_ownership_satisfied.03`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.

연결 NormCard: `art323_sec2_2.title_transfer_criteria`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec1_1.component.interference_with_exercise_of_right_object_possession_satisfied.01`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.

연결 NormCard: `art323_sec1_1.abstract_danger_offense`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec1_1.component.interference_with_exercise_of_right_object_possession_satisfied.02`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.

연결 NormCard: `art323_sec1_1.conduct_and_object`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.03`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.

연결 NormCard: `art323_sec2_2.corporate_system_records_other`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.04`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.

연결 NormCard: `art323_sec2_2.electronic_records`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.05`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.

연결 NormCard: `art323_sec2_2.joint_possession_object`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.06`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.

연결 NormCard: `art323_sec2_2.nonpossessory_claim_precedent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.07`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.

연결 NormCard: `art323_sec2_2.possession_actual_control`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.08`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.

연결 NormCard: `art323_sec2_2.property_movables_real_estate`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.09`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.

연결 NormCard: `art323_sec2_2.protected_possession_potential_value`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.10`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.

연결 NormCard: `art323_sec2_2.rescinded_sale_recovery`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.11`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.

연결 NormCard: `art323_sec2_2.retained_title_sale`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.component.interference_with_exercise_of_right_object_possession_satisfied.12`

이 규칙은 **객체 요건 중 타인 점유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.

연결 NormCard: `art323_sec2_2.rightful_possession_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323.component.interference_with_exercise_of_right_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.

연결 NormCard: `art323.forced_execution_evasion_scope`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_3.component.interference_with_exercise_of_right_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.

연결 NormCard: `art323_sec2_3.concealment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_3.component.interference_with_exercise_of_right_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.

연결 NormCard: `art323_sec2_3.destruction`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_3.component.interference_with_exercise_of_right_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.

연결 NormCard: `art323_sec2_3.risk_to_right_exercise`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_3.component.interference_with_exercise_of_right_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.

연결 NormCard: `art323_sec2_3.taking`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec3.component.interference_with_exercise_of_right_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.

연결 NormCard: `art323_sec3.conditional_intent_sufficient`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec3.component.interference_with_exercise_of_right_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.

연결 NormCard: `art323_sec3.subjective_awareness`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기와 타인의 공유에 속하는 물건은 타인의 물건이므로 권리행사방해죄의 자기 물건에 해당하지 않는다.

연결 NormCard: `art323_sec2_2.coowned_property_excluded`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도범인의 점유처럼 점유할 권리 없는 자의 점유임이 외관상 명백한 경우는 권리행사방해죄의 보호대상인 타인의 점유에 포함되지 않는다.

연결 NormCard: `art323_sec2_2.manifestly_no_right_possession_excluded`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 유효한 명의신탁 관계에서 대외적으로 명의수탁자만 소유자로 취급되는 경우, 명의신탁자는 제3자인 임차인에 대한 관계에서 권리행사방해죄의 주체가 될 수 없다.

연결 NormCard: `art323_sec2_2.nominee_owner_not_subject`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 물건이라도 공무소 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 물건인 경우 권리행사방해죄는 성립하지 않는다.

연결 NormCard: `art323_sec2_2.official_custody_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소유와 소지가 모두 금지된 금제품은 권리행사방해죄의 객체가 될 수 없다.

연결 NormCard: `art323_sec2_2.prohibited_gold_products_excluded`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산이나 등록으로 소유권이 이전되는 자동차·중기·건설기계에서는 대금 완납 시까지 매도인에게 소유권을 유보하는 특약이 있어도 등기 또는 등록이 마쳐지면 매수인에게 소유권이 이전되므로 매도인은 권리행사방해죄의 주체가 될 수 없다.

연결 NormCard: `art323_sec2_2.registered_sale_seller_not_subject`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.art323_sec2_3.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우에는 취거에 해당하지 않는다.

연결 NormCard: `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `interference_with_exercise_of_right.component.l0o.mandatory_negative.01`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 진정신분범이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 자기 물건은 범인 소유의 물건을 말한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, 등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.

연결 NormCard: `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`

검토 메모: 구성요건 L0o에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `interference_with_exercise_of_right.component.l0p.mandatory_negative.02`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄는 자기의 물건 또는 전자기록 등 특수매체기록을 취거·은닉·손괴하여 타인의 권리행사를 방해하는 범죄이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 법인이 설치·운영하는 전산망 시스템에서 생성·처리·저장·출력되는 전자기록 등 특수매체기록은 법인의 임직원과의 관계에서 타인의 전자기록 등에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 전자기록에는 전기적 기록과 자기적 기록이 포함되고, 특수매체기록에는 전자적 기록 외에 광기술 또는 레이저기술을 이용한 기록도 포함되지만 마이크로필름과 디스크 자체는 기록이 아니라 물건이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 타인의 점유 목적이 된 물건이면 충분하므로 자기와 타인이 공동점유하는 물건도 권리행사방해죄의 객체에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 판례는 타인의 권리의 목적이 된 자기 물건의 권리에 점유를 수반하지 않는 채권도 포함된다고 해석한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법 제323조의 점유는 물건에 대한 사실상의 지배 상태 또는 현실적 소지라는 형법상 점유를 의미한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 물건에는 동산과 부동산이 모두 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 법정절차를 통한 분쟁 해결 시까지 잠정적으로 보호할 가치 있는 점유는 권리행사방해죄의 보호대상인 타인의 점유에 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 매매계약이 해제·해지되어 물권이 원소유자에게 회복된 경우, 매도인이 매매목적물을 매수인으로부터 임의로 취거하면 자기 물건에 대한 권리행사방해죄가 될 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 소유권유보부매매는 동산 매매에서 목적물을 인도하면서 대금 완납 시까지 소유권을 매도인에게 유보하기로 하는 특약이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄에서 타인의 점유는 정당한 원인에 기하여 물건을 점유하는 권리 있는 자의 점유를 의미하며, 본권이 없는 절도범인의 점유는 이에 해당하지 않는다.

연결 NormCard: `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`

검토 메모: 구성요건 L0p에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `interference_with_exercise_of_right.component.l1.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 담보권 실행 등을 위한 경매를 면탈할 목적으로 재산을 은닉하는 행위는 강제집행면탈죄의 규율 대상에는 포함되지 않으나, 권리행사방해죄는 성립할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하거나 현저히 곤란하게 하는 상태에 두는 행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 물건 전부 또는 일부의 용익적 또는 가치적 효용을 해하는 행위이며, 물리적 훼손 외의 방법으로 효용을 해하는 경우도 포함한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 타인의 권리행사를 방해한다는 것은 현실적인 방해 결과가 아니라 권리행사가 방해될 우려가 있는 상태에 이르는 것을 의미한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 취거는 점유자의 의사에 반하여 목적물을 점유자의 지배로부터 자기 또는 제3자의 지배로 옮기는 행위이다.

연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `interference_with_exercise_of_right.component.l3.mandatory_negative.04`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 권리행사방해죄의 고의는 미필적 고의로도 충분하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 행위자는 타인의 점유 또는 권리의 목적이 된 자기 물건이라는 점 및 취거·은닉·손괴로 타인의 권리행사를 방해한다는 점을 인식해야 한다.

연결 NormCard: `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

검토 메모: 구성요건 L3에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `interference_with_exercise_of_right.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체 요건 중 타인 소유가 인정됨
- 객체 요건 중 타인 점유가 인정됨
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의

연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `interference_with_exercise_of_right.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_3.consensual_transfer_not_taking`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `interference_with_exercise_of_right.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec1_1.no_unlawful_appropriation_intent`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.coowned_property_excluded`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.manifestly_no_right_possession_excluded`, `art323_sec2_2.nominee_owner_not_subject`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.official_custody_exception`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.prohibited_gold_products_excluded`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.registered_sale_seller_not_subject`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.consensual_transfer_not_taking`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.no_intent_to_appropriate_required`, `art323_sec3.subjective_awareness`, `art323_sec7.family_exception_victim`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `interference_with_exercise_of_right.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `interference_with_exercise_of_right.art323_sec1_1.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄의 성립에는 불법영득의사가 요구되지 않는다.

연결 NormCard: `art323_sec1_1.no_unlawful_appropriation_intent`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `interference_with_exercise_of_right.art323_sec3.requirement_waived.002`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리행사방해죄는 영득죄가 아니므로 불법영득의 의사를 요하지 않는다.

연결 NormCard: `art323_sec3.no_intent_to_appropriate_required`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `interference_with_exercise_of_right.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art323.forced_execution_evasion_scope`, `art323_sec1_1.abstract_danger_offense`, `art323_sec1_1.conduct_and_object`, `art323_sec2_1.subject_genuine_status_offense`, `art323_sec2_2.corporate_system_records_other`, `art323_sec2_2.electronic_records`, `art323_sec2_2.joint_possession_object`, `art323_sec2_2.nonpossessory_claim_precedent`, `art323_sec2_2.possession_actual_control`, `art323_sec2_2.property_movables_real_estate`, `art323_sec2_2.protected_possession_potential_value`, `art323_sec2_2.rescinded_sale_recovery`, `art323_sec2_2.retained_title_sale`, `art323_sec2_2.rightful_possession_definition`, `art323_sec2_2.self_property_owner`, `art323_sec2_2.title_transfer_criteria`, `art323_sec2_3.concealment`, `art323_sec2_3.destruction`, `art323_sec2_3.risk_to_right_exercise`, `art323_sec2_3.taking`, `art323_sec3.conditional_intent_sufficient`, `art323_sec3.subjective_awareness`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
