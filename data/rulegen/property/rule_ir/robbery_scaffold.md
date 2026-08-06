# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.robbery.full.v1_candidate`
- predicate: 328개
- rule: 555개
- NormCard: 98개

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

### `robbery_case_roles(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art333_illegal_cause_debt_evasion_robbery_murder(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

### `satisfied_art333_illegal_cause_debt_evasion_robbery_murder(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

### `not_satisfied_satisfied_art333_illegal_cause_debt_evasion_robbery_murder(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

### `assess_art333_sec2_1_robbery_violence_incapacitating_attack(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

### `satisfied_art333_sec2_1_robbery_violence_incapacitating_attack(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

### `not_satisfied_satisfied_art333_sec2_1_robbery_violence_incapacitating_attack(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

### `assess_art333_sec2_1_violence_threat_resistance_suppression(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

### `satisfied_art333_sec2_1_violence_threat_resistance_suppression(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

### `not_satisfied_satisfied_art333_sec2_1_violence_threat_resistance_suppression(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

### `assess_art333_sec2_2_drug_induced_incapacitation_violence(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

### `satisfied_art333_sec2_2_drug_induced_incapacitation_violence(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

### `not_satisfied_satisfied_art333_sec2_2_drug_induced_incapacitation_violence(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

### `assess_art333_sec2_2_incidental_incapacitation_no_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

### `satisfied_art333_sec2_2_incidental_incapacitation_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

### `not_satisfied_satisfied_art333_sec2_2_incidental_incapacitation_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

### `assess_art333_sec2_2_preexisting_incapacitation_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

### `satisfied_art333_sec2_2_preexisting_incapacitation_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

### `not_satisfied_satisfied_art333_sec2_2_preexisting_incapacitation_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

### `assess_art333_sec2_3_apparent_capacity_threat(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

### `satisfied_art333_sec2_3_apparent_capacity_threat(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

### `not_satisfied_satisfied_art333_sec2_3_apparent_capacity_threat(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

### `assess_art333_sec2_3_diversion_or_insult_violence_no_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

### `satisfied_art333_sec2_3_diversion_or_insult_violence_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

### `not_satisfied_satisfied_art333_sec2_3_diversion_or_insult_violence_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

### `assess_art333_sec2_3_lesser_threat_extortion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

### `satisfied_art333_sec2_3_lesser_threat_extortion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

### `not_satisfied_satisfied_art333_sec2_3_lesser_threat_extortion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

### `assess_art333_sec2_3_objective_resistance_suppression(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

### `satisfied_art333_sec2_3_objective_resistance_suppression(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

### `not_satisfied_satisfied_art333_sec2_3_objective_resistance_suppression(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

### `assess_art333_sec2_3_snatching_forceful_attack(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

### `satisfied_art333_sec2_3_snatching_forceful_attack(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

### `not_satisfied_satisfied_art333_sec2_3_snatching_forceful_attack(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

### `assess_art333_sec2_3_subjective_intent_insufficient(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

### `satisfied_art333_sec2_3_subjective_intent_insufficient(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

### `not_satisfied_satisfied_art333_sec2_3_subjective_intent_insufficient(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

### `assess_art333_sec2_3_weapon_presentation_context(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_3.weapon_presentation_context`

### `satisfied_art333_sec2_3_weapon_presentation_context(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.weapon_presentation_context`

### `not_satisfied_satisfied_art333_sec2_3_weapon_presentation_context(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.weapon_presentation_context`

### `assess_art333_sec2_4_target_person_obstructing_taking(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

### `satisfied_art333_sec2_4_target_person_obstructing_taking(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

### `not_satisfied_satisfied_art333_sec2_4_target_person_obstructing_taking(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

### `assess_art333_sec3_forcible_taking(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3.forcible_taking`

### `satisfied_art333_sec3_forcible_taking(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3.forcible_taking`

### `not_satisfied_satisfied_art333_sec3_forcible_taking(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3.forcible_taking`

### `assess_art333_sec3_1_real_estate_as_robbery_property_negative(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

### `satisfied_art333_sec3_1_real_estate_as_robbery_property_negative(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

### `not_satisfied_satisfied_art333_sec3_1_real_estate_as_robbery_property_negative(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

### `assess_art333_sec3_2_post_taking_assault_no_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

### `satisfied_art333_sec3_2_post_taking_assault_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

### `not_satisfied_satisfied_art333_sec3_2_post_taking_assault_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

### `assess_art333_sec3_2_voluntary_delivery_attempt(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

### `satisfied_art333_sec3_2_voluntary_delivery_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

### `not_satisfied_satisfied_art333_sec3_2_voluntary_delivery_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

### `assess_art333_sec3_3_completed_theft_quasi_robbery_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

### `satisfied_art333_sec3_3_completed_theft_quasi_robbery_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

### `not_satisfied_satisfied_art333_sec3_3_completed_theft_quasi_robbery_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

### `assess_art333_sec3_3_continuing_force_after_theft_intent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

### `satisfied_art333_sec3_3_continuing_force_after_theft_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

### `not_satisfied_satisfied_art333_sec3_3_continuing_force_after_theft_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

### `assess_art333_sec3_3_continuing_force_single_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

### `satisfied_art333_sec3_3_continuing_force_single_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

### `not_satisfied_satisfied_art333_sec3_3_continuing_force_single_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

### `assess_art333_sec3_3_rape_fear_state_property_provision(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

### `satisfied_art333_sec3_3_rape_fear_state_property_provision(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

### `not_satisfied_satisfied_art333_sec3_3_rape_fear_state_property_provision(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

### `assess_art333_sec3_3_rape_force_subsequent_taking_precedent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

### `satisfied_art333_sec3_3_rape_force_subsequent_taking_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

### `not_satisfied_satisfied_art333_sec3_3_rape_force_subsequent_taking_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

### `assess_art333_sec3_3_unconsciousness_prior_force_no_causation(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

### `satisfied_art333_sec3_3_unconsciousness_prior_force_no_causation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

### `not_satisfied_satisfied_art333_sec3_3_unconsciousness_prior_force_no_causation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

### `assess_art333_sec4_1_apparent_property_benefit(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec4_1.apparent_property_benefit`

### `satisfied_art333_sec4_1_apparent_property_benefit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_1.apparent_property_benefit`

### `not_satisfied_satisfied_art333_sec4_1_apparent_property_benefit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_1.apparent_property_benefit`

### `assess_art333_sec4_1_property_benefit(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec4_1.property_benefit`

### `satisfied_art333_sec4_1_property_benefit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_1.property_benefit`

### `not_satisfied_satisfied_art333_sec4_1_property_benefit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_1.property_benefit`

### `assess_art333_sec4_2_debt_evasion_benefit_transfer(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

### `satisfied_art333_sec4_2_debt_evasion_benefit_transfer(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

### `not_satisfied_satisfied_art333_sec4_2_debt_evasion_benefit_transfer(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

### `assess_art333_sec4_2_debt_evasion_disposition_not_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

### `satisfied_art333_sec4_2_debt_evasion_disposition_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

### `not_satisfied_satisfied_art333_sec4_2_debt_evasion_disposition_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

### `assess_art333_sec5_determine_illegal_benefit_intent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

### `satisfied_art333_sec5_determine_illegal_benefit_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

### `not_satisfied_satisfied_art333_sec5_determine_illegal_benefit_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

### `assess_art333_sec5_illegal_benefit_intent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec5.illegal_benefit_intent`

### `satisfied_art333_sec5_illegal_benefit_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec5.illegal_benefit_intent`

### `not_satisfied_satisfied_art333_sec5_illegal_benefit_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec5.illegal_benefit_intent`

### `assess_art333_sec6_attempt_commencement_violence_intimidation(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

### `satisfied_art333_sec6_attempt_commencement_violence_intimidation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

### `not_satisfied_satisfied_art333_sec6_attempt_commencement_violence_intimidation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

### `assess_art333_sec6_attempt_debt_evasion_killing(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

### `satisfied_art333_sec6_attempt_debt_evasion_killing(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

### `not_satisfied_satisfied_art333_sec6_attempt_debt_evasion_killing(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

### `assess_art333_sec6_attempt_intent_arising_after_subjugation(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

### `satisfied_art333_sec6_attempt_intent_arising_after_subjugation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

### `not_satisfied_satisfied_art333_sec6_attempt_intent_arising_after_subjugation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

### `assess_art333_sec6_attempt_unattained_objective(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec6.attempt_unattained_objective`

### `satisfied_art333_sec6_attempt_unattained_objective(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_unattained_objective`

### `not_satisfied_satisfied_art333_sec6_attempt_unattained_objective(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_unattained_objective`

### `assess_art333_sec6_no_attempt_insufficient_violence_intimidation(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

### `satisfied_art333_sec6_no_attempt_insufficient_violence_intimidation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

### `not_satisfied_satisfied_art333_sec6_no_attempt_insufficient_violence_intimidation(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

### `assess_art333_sec6_no_attempt_without_violence_intimidation_commencement(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

### `satisfied_art333_sec6_no_attempt_without_violence_intimidation_commencement(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

### `not_satisfied_satisfied_art333_sec6_no_attempt_without_violence_intimidation_commencement(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

### `assess_art333_sec7_1_completion_exclusive_control_transfer(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

### `satisfied_art333_sec7_1_completion_exclusive_control_transfer(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

### `not_satisfied_satisfied_art333_sec7_1_completion_exclusive_control_transfer(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

### `assess_art333_sec7_1_completion_exclusive_control_within_victim_domain(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

### `satisfied_art333_sec7_1_completion_exclusive_control_within_victim_domain(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

### `not_satisfied_satisfied_art333_sec7_1_completion_exclusive_control_within_victim_domain(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

### `assess_art333_sec7_1_completion_no_safe_escape_requirement(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

### `satisfied_art333_sec7_1_completion_no_safe_escape_requirement(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

### `not_satisfied_satisfied_art333_sec7_1_completion_no_safe_escape_requirement(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

### `assess_art333_sec7_1_completion_recovery_does_not_negate(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

### `satisfied_art333_sec7_1_completion_recovery_does_not_negate(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

### `not_satisfied_satisfied_art333_sec7_1_completion_recovery_does_not_negate(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

### `assess_art333_sec7_2_completion_forcible_gain(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art333_sec7_2.completion_forcible_gain`

### `satisfied_art333_sec7_2_completion_forcible_gain(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_2.completion_forcible_gain`

### `not_satisfied_satisfied_art333_sec7_2_completion_forcible_gain(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_2.completion_forcible_gain`

### `assess_art333_sec8_right_exercise_robbery_negative(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

### `satisfied_art333_sec8_right_exercise_robbery_negative(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

### `not_satisfied_satisfied_art333_sec8_right_exercise_robbery_negative(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

### `assess_art334_sec1_nighttime_home_intrusion_robbery_aggravated_combination(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

### `satisfied_art334_sec1_nighttime_home_intrusion_robbery_aggravated_combination(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

### `not_satisfied_satisfied_art334_sec1_nighttime_home_intrusion_robbery_aggravated_combination(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

### `assess_art334_sec1_nighttime_robbery_damage_irrelevant(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

### `satisfied_art334_sec1_nighttime_robbery_damage_irrelevant(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

### `not_satisfied_satisfied_art334_sec1_nighttime_robbery_damage_irrelevant(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

### `assess_art334_sec2_1_weapon_awareness_not_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

### `satisfied_art334_sec2_1_weapon_awareness_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

### `not_satisfied_satisfied_art334_sec2_1_weapon_awareness_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

### `assess_art334_sec2_1_weapon_carried_fists_used(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

### `satisfied_art334_sec2_1_weapon_carried_fists_used(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

### `not_satisfied_satisfied_art334_sec2_1_weapon_carried_fists_used(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

### `assess_art334_sec2_1_weapon_direct_use_not_required(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

### `satisfied_art334_sec2_1_weapon_direct_use_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

### `not_satisfied_satisfied_art334_sec2_1_weapon_direct_use_not_required(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

### `assess_art334_sec3_daytime_weapon_or_joint_robbery_attempt_on_violence_threat(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

### `satisfied_art334_sec3_daytime_weapon_or_joint_robbery_attempt_on_violence_threat(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

### `not_satisfied_satisfied_art334_sec3_daytime_weapon_or_joint_robbery_attempt_on_violence_threat(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

### `assess_art334_sec3_nighttime_home_intrusion_attempt_on_intrusion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

### `satisfied_art334_sec3_nighttime_home_intrusion_attempt_on_intrusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

### `not_satisfied_satisfied_art334_sec3_nighttime_home_intrusion_attempt_on_intrusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

### `assess_art335_sec1_aggravated_robbery_offenses_apply(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

### `satisfied_art335_sec1_aggravated_robbery_offenses_apply(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

### `not_satisfied_satisfied_art335_sec1_aggravated_robbery_offenses_apply(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

### `assess_art335_sec2_actor_thief(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec2.actor_thief`

### `satisfied_art335_sec2_actor_thief(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.actor_thief`

### `not_satisfied_satisfied_art335_sec2_actor_thief(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.actor_thief`

### `assess_art335_sec2_preparation_stage_exclusion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec2.preparation_stage_exclusion`

### `satisfied_art335_sec2_preparation_stage_exclusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.preparation_stage_exclusion`

### `not_satisfied_satisfied_art335_sec2_preparation_stage_exclusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.preparation_stage_exclusion`

### `assess_art335_sec2_property_interest_exclusion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec2.property_interest_exclusion`

### `satisfied_art335_sec2_property_interest_exclusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.property_interest_exclusion`

### `not_satisfied_satisfied_art335_sec2_property_interest_exclusion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec2.property_interest_exclusion`

### `assess_art335_sec3_special_purpose(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec3.special_purpose`

### `satisfied_art335_sec3_special_purpose(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3.special_purpose`

### `not_satisfied_satisfied_art335_sec3_special_purpose(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3.special_purpose`

### `assess_art335_sec3_1_pre_control_violence_is_robbery_exception(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

### `satisfied_art335_sec3_1_pre_control_violence_is_robbery_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

### `not_satisfied_satisfied_art335_sec3_1_pre_control_violence_is_robbery_exception(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

### `assess_art335_sec3_1_recapture_opponent_need_not_act(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

### `satisfied_art335_sec3_1_recapture_opponent_need_not_act(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

### `not_satisfied_satisfied_art335_sec3_1_recapture_opponent_need_not_act(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

### `assess_art335_sec3_1_recapture_resistance_after_exclusive_control(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

### `satisfied_art335_sec3_1_recapture_resistance_after_exclusive_control(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

### `not_satisfied_satisfied_art335_sec3_1_recapture_resistance_after_exclusive_control(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

### `assess_art335_sec3_2_anticipated_arrest_violence(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

### `satisfied_art335_sec3_2_anticipated_arrest_violence(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

### `not_satisfied_satisfied_art335_sec3_2_anticipated_arrest_violence(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

### `assess_art335_sec3_2_arrest_or_concealment_no_control(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

### `satisfied_art335_sec3_2_arrest_or_concealment_no_control(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

### `not_satisfied_satisfied_art335_sec3_2_arrest_or_concealment_no_control(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

### `assess_art335_sec3_2_escape_arrest_accomplice(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

### `satisfied_art335_sec3_2_escape_arrest_accomplice(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

### `not_satisfied_satisfied_art335_sec3_2_escape_arrest_accomplice(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

### `assess_art335_sec3_3_concealing_crime_traces(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec3_3.concealing_crime_traces`

### `satisfied_art335_sec3_3_concealing_crime_traces(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_3.concealing_crime_traces`

### `not_satisfied_satisfied_art335_sec3_3_concealing_crime_traces(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_3.concealing_crime_traces`

### `assess_art335_sec3_4_purpose_achievement_irrelevant(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

### `satisfied_art335_sec3_4_purpose_achievement_irrelevant(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

### `not_satisfied_satisfied_art335_sec3_4_purpose_achievement_irrelevant(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

### `assess_art335_sec4_objective_capacity(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec4.objective_capacity`

### `satisfied_art335_sec4_objective_capacity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.objective_capacity`

### `not_satisfied_satisfied_art335_sec4_objective_capacity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.objective_capacity`

### `assess_art335_sec4_police_officer_general_person_standard(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec4.police_officer_general_person_standard`

### `satisfied_art335_sec4_police_officer_general_person_standard(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.police_officer_general_person_standard`

### `not_satisfied_satisfied_art335_sec4_police_officer_general_person_standard(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.police_officer_general_person_standard`

### `assess_art335_sec4_violence_resistance_threshold(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec4.violence_resistance_threshold`

### `satisfied_art335_sec4_violence_resistance_threshold(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.violence_resistance_threshold`

### `not_satisfied_satisfied_art335_sec4_violence_resistance_threshold(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec4.violence_resistance_threshold`

### `assess_art335_sec5_violence_threat_target(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec5.violence_threat_target`

### `satisfied_art335_sec5_violence_threat_target(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec5.violence_threat_target`

### `not_satisfied_satisfied_art335_sec5_violence_threat_target(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec5.violence_threat_target`

### `assess_art335_sec6_1_days_later_no_opportunity(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

### `satisfied_art335_sec6_1_days_later_no_opportunity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

### `not_satisfied_satisfied_art335_sec6_1_days_later_no_opportunity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

### `assess_art335_sec6_1_opportunity_temporal_spatial_proximity(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

### `satisfied_art335_sec6_1_opportunity_temporal_spatial_proximity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

### `not_satisfied_satisfied_art335_sec6_1_opportunity_temporal_spatial_proximity(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

### `assess_art335_sec6_2_opportunity_definition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec6_2.opportunity_definition`

### `satisfied_art335_sec6_2_opportunity_definition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_definition`

### `not_satisfied_satisfied_art335_sec6_2_opportunity_definition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_definition`

### `assess_art335_sec6_2_opportunity_pursuit_or_uncertain_custody(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

### `satisfied_art335_sec6_2_opportunity_pursuit_or_uncertain_custody(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

### `not_satisfied_satisfied_art335_sec6_2_opportunity_pursuit_or_uncertain_custody(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

### `assess_art335_sec6_2_opportunity_safe_escape_limit(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

### `satisfied_art335_sec6_2_opportunity_safe_escape_limit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

### `not_satisfied_satisfied_art335_sec6_2_opportunity_safe_escape_limit(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

### `assess_art335_sec7_attempt_punishable(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art335_sec7.attempt_punishable`

### `satisfied_art335_sec7_attempt_punishable(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄의 미수범은 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7.attempt_punishable`

### `not_satisfied_satisfied_art335_sec7_attempt_punishable(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도죄의 미수범은 처벌된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7.attempt_punishable`

### `assess_art335_sec7_1_attempt_theft_act_standard(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

### `satisfied_art335_sec7_1_attempt_theft_act_standard(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

### `not_satisfied_satisfied_art335_sec7_1_attempt_theft_act_standard(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

### `assess_art335_sec7_1_supreme_court_completion_by_theft(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

### `satisfied_art335_sec7_1_supreme_court_completion_by_theft(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

### `not_satisfied_satisfied_art335_sec7_1_supreme_court_completion_by_theft(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

### `assess_art335_sec8_weapon_acquired_during_violence_reported_precedent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

### `satisfied_art335_sec8_weapon_acquired_during_violence_reported_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

### `not_satisfied_satisfied_art335_sec8_weapon_acquired_during_violence_reported_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

### `assess_art337_sec2_subject_robber_and_attempted_robber(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

### `satisfied_art337_sec2_subject_robber_and_attempted_robber(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

### `not_satisfied_satisfied_art337_sec2_subject_robber_and_attempted_robber(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

### `assess_art337_sec3_injury_result_violence_intent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art337_sec3.injury_result_violence_intent`

### `satisfied_art337_sec3_injury_result_violence_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3.injury_result_violence_intent`

### `not_satisfied_satisfied_art337_sec3_injury_result_violence_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3.injury_result_violence_intent`

### `assess_art337_sec3_2_injury_concrete_victim_condition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

### `satisfied_art337_sec3_2_injury_concrete_victim_condition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

### `not_satisfied_satisfied_art337_sec3_2_injury_concrete_victim_condition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

### `assess_art337_sec3_2_injury_threshold(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art337_sec3_2.injury_threshold`

### `satisfied_art337_sec3_2_injury_threshold(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.injury_threshold`

### `not_satisfied_satisfied_art337_sec3_2_injury_threshold(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.injury_threshold`

### `assess_art337_sec3_2_robbery_occasion_ended(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

### `satisfied_art337_sec3_2_robbery_occasion_ended(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

### `not_satisfied_satisfied_art337_sec3_2_robbery_occasion_ended(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

### `assess_art337_sec3_2_trivial_injury_excluded(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

### `satisfied_art337_sec3_2_trivial_injury_excluded(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

### `not_satisfied_satisfied_art337_sec3_2_trivial_injury_excluded(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

### `assess_art337_sec4_completion_injury_result(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art337_sec4.completion_injury_result`

### `satisfied_art337_sec4_completion_injury_result(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec4.completion_injury_result`

### `not_satisfied_satisfied_art337_sec4_completion_injury_result(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art337_sec4.completion_injury_result`

### `assess_art338_sec1_robbery_death_result_aggravated(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

### `satisfied_art338_sec1_robbery_death_result_aggravated(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

### `not_satisfied_satisfied_art338_sec1_robbery_death_result_aggravated(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

### `assess_art338_sec1_robbery_murder_intent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec1.robbery_murder_intent`

### `satisfied_art338_sec1_robbery_murder_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec1.robbery_murder_intent`

### `not_satisfied_satisfied_art338_sec1_robbery_murder_intent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec1.robbery_murder_intent`

### `assess_art338_sec2_debt_evasion_no_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

### `satisfied_art338_sec2_debt_evasion_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

### `not_satisfied_satisfied_art338_sec2_debt_evasion_no_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

### `assess_art338_sec2_debt_evasion_robbery(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec2.debt_evasion_robbery`

### `satisfied_art338_sec2_debt_evasion_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec2.debt_evasion_robbery`

### `not_satisfied_satisfied_art338_sec2_debt_evasion_robbery(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec2.debt_evasion_robbery`

### `assess_art338_sec3_delayed_death_no_effect(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art338_sec3.delayed_death_no_effect`

### `satisfied_art338_sec3_delayed_death_no_effect(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.delayed_death_no_effect`

### `not_satisfied_satisfied_art338_sec3_delayed_death_no_effect(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.delayed_death_no_effect`

### `assess_art338_sec3_opportunity_immediate_flight_killing(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

### `satisfied_art338_sec3_opportunity_immediate_flight_killing(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

### `not_satisfied_satisfied_art338_sec3_opportunity_immediate_flight_killing(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

### `assess_art338_sec3_opportunity_new_intent_after_completion(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

### `satisfied_art338_sec3_opportunity_new_intent_after_completion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

### `not_satisfied_satisfied_art338_sec3_opportunity_new_intent_after_completion(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

### `assess_art338_sec4_murder_completion_controls_attempt(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

### `satisfied_art338_sec4_murder_completion_controls_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

### `not_satisfied_satisfied_art338_sec4_murder_completion_controls_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

### `assess_art338_sec4_robbery_death_attempt_excluded(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

### `satisfied_art338_sec4_robbery_death_attempt_excluded(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

### `not_satisfied_satisfied_art338_sec4_robbery_death_attempt_excluded(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

### `assess_art338_sec4_robbery_murder_attempt(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art338_sec4.robbery_murder_attempt`

### `satisfied_art338_sec4_robbery_murder_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.robbery_murder_attempt`

### `not_satisfied_satisfied_art338_sec4_robbery_murder_attempt(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art338_sec4.robbery_murder_attempt`

### `assess_art343_sec1_robbery_scope(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art343_sec1.robbery_scope`

### `satisfied_art343_sec1_robbery_scope(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec1.robbery_scope`

### `not_satisfied_satisfied_art343_sec1_robbery_scope(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec1.robbery_scope`

### `assess_art343_sec2_preparation_definition(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art343_sec2.preparation_definition`

### `satisfied_art343_sec2_preparation_definition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2.preparation_definition`

### `not_satisfied_satisfied_art343_sec2_preparation_definition(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2.preparation_definition`

### `assess_art343_sec2_1_contingent_intent_sufficient_precedent(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

### `satisfied_art343_sec2_1_contingent_intent_sufficient_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

### `not_satisfied_satisfied_art343_sec2_1_contingent_intent_sufficient_precedent(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

### `assess_art343_sec2_2_preparation_examples(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art343_sec2_2.preparation_examples`

### `satisfied_art343_sec2_2_preparation_examples(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_2.preparation_examples`

### `not_satisfied_satisfied_art343_sec2_2_preparation_examples(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_2.preparation_examples`

### `assess_art343_sec2_3_home_invasion_robbery_departure(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

### `satisfied_art343_sec2_3_home_invasion_robbery_departure(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

### `not_satisfied_satisfied_art343_sec2_3_home_invasion_robbery_departure(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

### `assess_art343_sec3_abandonment_before_execution_denied(case_id: String, assessment_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String, status: String)`

이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

### `satisfied_art343_sec3_abandonment_before_execution_denied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

### `not_satisfied_satisfied_art343_sec3_abandonment_before_execution_denied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

### `robbery_object_property_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

객체 요건 중 재물(강취 대상)이 인정됨 — 재물강취 트랙 전용

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

### `robbery_object_benefit_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`

### `robbery_conduct_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`

### `robbery_causation_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

행위와 결과의 연결(인과·귀속)이 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`

### `robbery_intent_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`

### `robbery_completion_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

### `robbery_completion_property_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

기수 요건 중 재물강취 기수(배타적 지배 취득)가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`

### `robbery_completion_benefit_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

기수 요건 중 이득강취 기수(이익 이전)가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_2.completion_forcible_gain`

### `robbery_elements_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

### `robbery_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`, `art333_sec7_1.completion.no_safe_escape_requirement`, `art333_sec7_1.completion.recovery_does_not_negate`, `art333_sec7_2.completion_forcible_gain`, `art333_sec8.right_exercise_robbery_negative`, `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`, `art334_sec1.nighttime_robbery_damage_irrelevant`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_carried_fists_used`, `art334_sec2_1.weapon_direct_use_not_required`, `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`, `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`, `art335_sec1.aggravated_robbery_offenses_apply`, `art335_sec2.actor_thief`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec3.special_purpose`, `art335_sec3_1.pre_control_violence_is_robbery_exception`, `art335_sec3_1.recapture_opponent_need_not_act`, `art335_sec3_1.recapture_resistance_after_exclusive_control`, `art335_sec3_2.anticipated_arrest_violence`, `art335_sec3_2.arrest_or_concealment_no_control`, `art335_sec3_2.escape_arrest_accomplice`, `art335_sec3_3.concealing_crime_traces`, `art335_sec3_4.purpose_achievement_irrelevant`, `art335_sec4.objective_capacity`, `art335_sec4.police_officer_general_person_standard`, `art335_sec4.violence_resistance_threshold`, `art335_sec5.violence_threat_target`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_1.opportunity_temporal_spatial_proximity`, `art335_sec6_2.opportunity_definition`, `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`, `art335_sec6_2.opportunity_safe_escape_limit`, `art335_sec7.attempt_punishable`, `art335_sec7_1.attempt_theft_act_standard`, `art335_sec7_1.supreme_court_completion_by_theft`, `art335_sec8.weapon_acquired_during_violence.reported_precedent`, `art337_sec2.subject_robber_and_attempted_robber`, `art337_sec3.injury_result_violence_intent`, `art337_sec3_2.injury_concrete_victim_condition`, `art337_sec3_2.injury_threshold`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art337_sec4.completion_injury_result`, `art338_sec1.robbery_death_result_aggravated`, `art338_sec1.robbery_murder_intent`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec2.debt_evasion_robbery`, `art338_sec3.delayed_death_no_effect`, `art338_sec3.opportunity_immediate_flight_killing`, `art338_sec3.opportunity_new_intent_after_completion`, `art338_sec4.murder_completion_controls_attempt`, `art338_sec4.robbery_death_attempt_excluded`, `art338_sec4.robbery_murder_attempt`, `art343_sec1.robbery_scope`, `art343_sec2.preparation_definition`, `art343_sec2_1.contingent_intent_sufficient_precedent`, `art343_sec2_2.preparation_examples`, `art343_sec2_3.home_invasion_robbery_departure`, `art343_sec3.abandonment_before_execution_denied`

### `robbery_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`, `art333_sec7_1.completion.no_safe_escape_requirement`, `art333_sec7_1.completion.recovery_does_not_negate`, `art333_sec7_2.completion_forcible_gain`, `art333_sec8.right_exercise_robbery_negative`, `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`, `art334_sec1.nighttime_robbery_damage_irrelevant`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_carried_fists_used`, `art334_sec2_1.weapon_direct_use_not_required`, `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`, `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`, `art335_sec1.aggravated_robbery_offenses_apply`, `art335_sec2.actor_thief`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec3.special_purpose`, `art335_sec3_1.pre_control_violence_is_robbery_exception`, `art335_sec3_1.recapture_opponent_need_not_act`, `art335_sec3_1.recapture_resistance_after_exclusive_control`, `art335_sec3_2.anticipated_arrest_violence`, `art335_sec3_2.arrest_or_concealment_no_control`, `art335_sec3_2.escape_arrest_accomplice`, `art335_sec3_3.concealing_crime_traces`, `art335_sec3_4.purpose_achievement_irrelevant`, `art335_sec4.objective_capacity`, `art335_sec4.police_officer_general_person_standard`, `art335_sec4.violence_resistance_threshold`, `art335_sec5.violence_threat_target`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_1.opportunity_temporal_spatial_proximity`, `art335_sec6_2.opportunity_definition`, `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`, `art335_sec6_2.opportunity_safe_escape_limit`, `art335_sec7.attempt_punishable`, `art335_sec7_1.attempt_theft_act_standard`, `art335_sec7_1.supreme_court_completion_by_theft`, `art335_sec8.weapon_acquired_during_violence.reported_precedent`, `art337_sec2.subject_robber_and_attempted_robber`, `art337_sec3.injury_result_violence_intent`, `art337_sec3_2.injury_concrete_victim_condition`, `art337_sec3_2.injury_threshold`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art337_sec4.completion_injury_result`, `art338_sec1.robbery_death_result_aggravated`, `art338_sec1.robbery_murder_intent`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec2.debt_evasion_robbery`, `art338_sec3.delayed_death_no_effect`, `art338_sec3.opportunity_immediate_flight_killing`, `art338_sec3.opportunity_new_intent_after_completion`, `art338_sec4.murder_completion_controls_attempt`, `art338_sec4.robbery_death_attempt_excluded`, `art338_sec4.robbery_murder_attempt`, `art343_sec1.robbery_scope`, `art343_sec2.preparation_definition`, `art343_sec2_1.contingent_intent_sufficient_precedent`, `art343_sec2_2.preparation_examples`, `art343_sec2_3.home_invasion_robbery_departure`, `art343_sec3.abandonment_before_execution_denied`

### `robbery_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`, `art333_sec7_1.completion.no_safe_escape_requirement`, `art333_sec7_1.completion.recovery_does_not_negate`, `art333_sec7_2.completion_forcible_gain`, `art333_sec8.right_exercise_robbery_negative`, `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`, `art334_sec1.nighttime_robbery_damage_irrelevant`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_carried_fists_used`, `art334_sec2_1.weapon_direct_use_not_required`, `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`, `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`, `art335_sec1.aggravated_robbery_offenses_apply`, `art335_sec2.actor_thief`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec3.special_purpose`, `art335_sec3_1.pre_control_violence_is_robbery_exception`, `art335_sec3_1.recapture_opponent_need_not_act`, `art335_sec3_1.recapture_resistance_after_exclusive_control`, `art335_sec3_2.anticipated_arrest_violence`, `art335_sec3_2.arrest_or_concealment_no_control`, `art335_sec3_2.escape_arrest_accomplice`, `art335_sec3_3.concealing_crime_traces`, `art335_sec3_4.purpose_achievement_irrelevant`, `art335_sec4.objective_capacity`, `art335_sec4.police_officer_general_person_standard`, `art335_sec4.violence_resistance_threshold`, `art335_sec5.violence_threat_target`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_1.opportunity_temporal_spatial_proximity`, `art335_sec6_2.opportunity_definition`, `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`, `art335_sec6_2.opportunity_safe_escape_limit`, `art335_sec7.attempt_punishable`, `art335_sec7_1.attempt_theft_act_standard`, `art335_sec7_1.supreme_court_completion_by_theft`, `art335_sec8.weapon_acquired_during_violence.reported_precedent`, `art337_sec2.subject_robber_and_attempted_robber`, `art337_sec3.injury_result_violence_intent`, `art337_sec3_2.injury_concrete_victim_condition`, `art337_sec3_2.injury_threshold`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art337_sec4.completion_injury_result`, `art338_sec1.robbery_death_result_aggravated`, `art338_sec1.robbery_murder_intent`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec2.debt_evasion_robbery`, `art338_sec3.delayed_death_no_effect`, `art338_sec3.opportunity_immediate_flight_killing`, `art338_sec3.opportunity_new_intent_after_completion`, `art338_sec4.murder_completion_controls_attempt`, `art338_sec4.robbery_death_attempt_excluded`, `art338_sec4.robbery_murder_attempt`, `art343_sec1.robbery_scope`, `art343_sec2.preparation_definition`, `art343_sec2_1.contingent_intent_sufficient_precedent`, `art343_sec2_2.preparation_examples`, `art343_sec2_3.home_invasion_robbery_departure`, `art343_sec3.abandonment_before_execution_denied`

### `robbery_established(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

### `robbery_quarantined_effect(case_id: String, defendant_id: String, issue_id: String)`

극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`

### `robbery_track_property_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

대안적 실행형태 'property' 트랙의 component가 공유 component와 함께 모두 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`

### `robbery_track_benefit_satisfied(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

대안적 실행형태 'benefit' 트랙의 component가 공유 component와 함께 모두 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec7_2.completion_forcible_gain`

### `robbery_property_not_established(case_id: String, defendant_id: String, issue_id: String)`

'property' track에 국한된 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_property_has_negative(case_id: String, defendant_id: String)`

'property' track에 국한된 불성립 사유의 존재를 2항으로 요약함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_property_established(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

완결 게이트 뒤에 'property' track의 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

### `robbery_benefit_not_established(case_id: String, defendant_id: String, issue_id: String)`

'benefit' track에 국한된 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_benefit_has_negative(case_id: String, defendant_id: String)`

'benefit' track에 국한된 불성립 사유의 존재를 2항으로 요약함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

### `robbery_benefit_established(case_id: String, defendant_id: String, coerced_person_id: String, owner_id: String, possessor_id: String)`

완결 게이트 뒤에 'benefit' track의 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

### `robbery_requirement_waived(case_id: String, defendant_id: String, issue_id: String, value: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`, `art333_sec7_1.completion.recovery_does_not_negate`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_direct_use_not_required`, `art335_sec3_2.arrest_or_concealment_no_control`, `art338_sec4.robbery_death_attempt_excluded`

### `robbery_boundary_shift(case_id: String, defendant_id: String, issue_id: String, value: String)`

이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec8.right_exercise_robbery_negative`, `art338_sec2.debt_evasion_no_robbery`

### `robbery_post_outcome(case_id: String, defendant_id: String, issue_id: String, outcome_subtype: String, value: String)`

구성요건 판단 뒤에 오는 죄수·처벌 효과

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

### `robbery_refers_to_crime(case_id: String, defendant_id: String, crime_name: String)`

이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec8.right_exercise_robbery_negative`, `art338_sec2.debt_evasion_no_robbery`

### `robbery_aggravation(case_id: String, defendant_id: String, kind: String)`

가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`, `art334_sec1.nighttime_robbery_damage_irrelevant`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_carried_fists_used`, `art334_sec2_1.weapon_direct_use_not_required`, `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`, `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`, `art335_sec1.aggravated_robbery_offenses_apply`, `art335_sec2.actor_thief`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec3.special_purpose`, `art335_sec3_1.pre_control_violence_is_robbery_exception`, `art335_sec3_1.recapture_opponent_need_not_act`, `art335_sec3_1.recapture_resistance_after_exclusive_control`, `art335_sec3_2.anticipated_arrest_violence`, `art335_sec3_2.arrest_or_concealment_no_control`, `art335_sec3_2.escape_arrest_accomplice`, `art335_sec3_3.concealing_crime_traces`, `art335_sec3_4.purpose_achievement_irrelevant`, `art335_sec4.objective_capacity`, `art335_sec4.police_officer_general_person_standard`, `art335_sec4.violence_resistance_threshold`, `art335_sec5.violence_threat_target`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_1.opportunity_temporal_spatial_proximity`, `art335_sec6_2.opportunity_definition`, `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`, `art335_sec6_2.opportunity_safe_escape_limit`, `art335_sec7.attempt_punishable`, `art335_sec7_1.attempt_theft_act_standard`, `art335_sec7_1.supreme_court_completion_by_theft`, `art335_sec8.weapon_acquired_during_violence.reported_precedent`, `art337_sec2.subject_robber_and_attempted_robber`, `art337_sec3.injury_result_violence_intent`, `art337_sec3_2.injury_concrete_victim_condition`, `art337_sec3_2.injury_threshold`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art337_sec4.completion_injury_result`, `art338_sec1.robbery_death_result_aggravated`, `art338_sec1.robbery_murder_intent`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec2.debt_evasion_robbery`, `art338_sec3.delayed_death_no_effect`, `art338_sec3.opportunity_immediate_flight_killing`, `art338_sec3.opportunity_new_intent_after_completion`, `art338_sec4.murder_completion_controls_attempt`, `art338_sec4.robbery_death_attempt_excluded`, `art338_sec4.robbery_murder_attempt`, `art343_sec1.robbery_scope`, `art343_sec2.preparation_definition`, `art343_sec2_1.contingent_intent_sufficient_precedent`, `art343_sec2_2.preparation_examples`, `art343_sec2_3.home_invasion_robbery_departure`, `art343_sec3.abandonment_before_execution_denied`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

## Rules

### `robbery.art333.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_1.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_1.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_1.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_1.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_1.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_1.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_1.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_1.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_2.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_2.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_2.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_2.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_2.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_2.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_2.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_2.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_2.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_2.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_2.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_2.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_3.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.weapon_presentation_context`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_3.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.weapon_presentation_context`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_3.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.weapon_presentation_context`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_3.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_3.weapon_presentation_context`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec2_4.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec2_4.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec2_4.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec2_4.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3.forcible_taking`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3.forcible_taking`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3.forcible_taking`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3.card.015.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3.forcible_taking`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_1.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_1.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_1.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_1.card.016.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_2.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_2.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_2.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_2.card.017.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_2.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_2.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_2.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_2.card.018.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.019.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.020.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.021.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.022.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.023.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_3.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec3_3.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec3_3.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec3_3.card.024.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec4_1.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.apparent_property_benefit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec4_1.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.apparent_property_benefit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec4_1.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.apparent_property_benefit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec4_1.card.025.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.apparent_property_benefit`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec4_1.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.property_benefit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec4_1.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.property_benefit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec4_1.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.property_benefit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec4_1.card.026.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_1.property_benefit`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec4_2.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec4_2.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec4_2.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec4_2.card.027.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec4_2.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec4_2.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec4_2.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec4_2.card.028.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec5.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec5.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec5.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec5.card.029.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec5.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.illegal_benefit_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec5.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.illegal_benefit_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec5.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.illegal_benefit_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec5.card.030.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec5.illegal_benefit_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.031.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.032.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.033.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_unattained_objective`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_unattained_objective`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_unattained_objective`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.034.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.attempt_unattained_objective`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.035.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec6.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec6.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec6.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec6.card.036.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec7_1.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec7_1.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec7_1.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec7_1.card.037.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec7_1.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec7_1.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec7_1.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec7_1.card.038.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec7_1.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec7_1.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec7_1.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec7_1.card.039.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec7_1.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec7_1.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec7_1.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec7_1.card.040.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec7_2.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_2.completion_forcible_gain`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec7_2.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_2.completion_forcible_gain`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec7_2.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_2.completion_forcible_gain`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec7_2.card.041.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec7_2.completion_forcible_gain`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec8.card.042.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art333_sec8.card.042.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art333_sec8.card.042.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art333_sec8.card.042.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec1.card.043.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec1.card.043.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec1.card.043.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec1.card.043.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec1.card.044.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec1.card.044.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec1.card.044.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec1.card.044.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec2_1.card.045.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec2_1.card.045.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec2_1.card.045.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec2_1.card.045.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec2_1.card.046.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec2_1.card.046.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec2_1.card.046.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec2_1.card.046.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec2_1.card.047.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec2_1.card.047.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec2_1.card.047.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec2_1.card.047.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec3.card.048.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec3.card.048.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec3.card.048.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec3.card.048.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art334_sec3.card.049.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art334_sec3.card.049.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art334_sec3.card.049.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art334_sec3.card.049.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec1.card.050.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec1.card.050.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec1.card.050.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec1.card.050.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec2.card.051.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.actor_thief`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec2.card.051.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.actor_thief`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec2.card.051.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.actor_thief`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec2.card.051.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.actor_thief`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec2.card.052.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec2.card.052.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec2.card.052.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec2.card.052.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec2.card.053.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec2.card.053.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec2.card.053.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec2.card.053.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3.card.054.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3.special_purpose`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3.card.054.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3.special_purpose`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3.card.054.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3.special_purpose`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3.card.054.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3.special_purpose`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_1.card.055.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_1.card.055.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_1.card.055.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_1.card.055.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_1.card.056.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_1.card.056.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_1.card.056.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_1.card.056.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_1.card.057.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_1.card.057.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_1.card.057.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_1.card.057.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_2.card.058.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_2.card.058.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_2.card.058.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_2.card.058.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_2.card.059.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_2.card.059.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_2.card.059.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_2.card.059.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_2.card.060.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_2.card.060.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_2.card.060.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_2.card.060.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_3.card.061.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_3.concealing_crime_traces`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_3.card.061.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_3.concealing_crime_traces`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_3.card.061.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_3.concealing_crime_traces`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_3.card.061.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_3.concealing_crime_traces`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec3_4.card.062.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec3_4.card.062.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec3_4.card.062.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec3_4.card.062.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec4.card.063.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.objective_capacity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec4.card.063.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.objective_capacity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec4.card.063.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.objective_capacity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec4.card.063.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.objective_capacity`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec4.card.064.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.police_officer_general_person_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec4.card.064.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.police_officer_general_person_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec4.card.064.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.police_officer_general_person_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec4.card.064.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.police_officer_general_person_standard`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec4.card.065.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.violence_resistance_threshold`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec4.card.065.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.violence_resistance_threshold`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec4.card.065.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.violence_resistance_threshold`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec4.card.065.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec4.violence_resistance_threshold`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec5.card.066.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec5.violence_threat_target`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec5.card.066.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec5.violence_threat_target`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec5.card.066.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec5.violence_threat_target`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec5.card.066.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec5.violence_threat_target`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec6_1.card.067.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec6_1.card.067.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec6_1.card.067.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec6_1.card.067.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec6_1.card.068.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec6_1.card.068.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec6_1.card.068.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec6_1.card.068.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec6_2.card.069.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec6_2.card.069.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec6_2.card.069.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec6_2.card.069.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec6_2.card.070.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec6_2.card.070.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec6_2.card.070.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec6_2.card.070.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec6_2.card.071.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec6_2.card.071.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec6_2.card.071.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec6_2.card.071.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec7.card.072.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄의 미수범은 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7.attempt_punishable`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec7.card.072.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7.attempt_punishable`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec7.card.072.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7.attempt_punishable`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec7.card.072.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도죄의 미수범은 처벌된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도죄의 미수범은 처벌된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7.attempt_punishable`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec7_1.card.073.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec7_1.card.073.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec7_1.card.073.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec7_1.card.073.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec7_1.card.074.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec7_1.card.074.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec7_1.card.074.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec7_1.card.074.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art335_sec8.card.075.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art335_sec8.card.075.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art335_sec8.card.075.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art335_sec8.card.075.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec2.card.076.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec2.card.076.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec2.card.076.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec2.card.076.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec3.card.077.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3.injury_result_violence_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec3.card.077.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3.injury_result_violence_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec3.card.077.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3.injury_result_violence_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec3.card.077.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3.injury_result_violence_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec3_2.card.078.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec3_2.card.078.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec3_2.card.078.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec3_2.card.078.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec3_2.card.079.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_threshold`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec3_2.card.079.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_threshold`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec3_2.card.079.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_threshold`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec3_2.card.079.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.injury_threshold`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec3_2.card.080.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec3_2.card.080.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec3_2.card.080.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec3_2.card.080.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec3_2.card.081.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec3_2.card.081.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec3_2.card.081.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec3_2.card.081.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art337_sec4.card.082.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec4.completion_injury_result`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art337_sec4.card.082.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec4.completion_injury_result`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art337_sec4.card.082.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec4.completion_injury_result`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art337_sec4.card.082.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art337_sec4.completion_injury_result`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec1.card.083.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec1.card.083.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec1.card.083.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec1.card.083.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec1.card.084.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_murder_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec1.card.084.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_murder_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec1.card.084.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_murder_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec1.card.084.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec1.robbery_murder_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec2.card.085.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec2.card.085.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec2.card.085.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec2.card.085.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec2.card.086.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_robbery`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec2.card.086.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_robbery`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec2.card.086.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_robbery`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec2.card.086.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec2.debt_evasion_robbery`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec3.card.087.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.delayed_death_no_effect`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec3.card.087.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.delayed_death_no_effect`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec3.card.087.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.delayed_death_no_effect`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec3.card.087.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.delayed_death_no_effect`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec3.card.088.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec3.card.088.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec3.card.088.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec3.card.088.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec3.card.089.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec3.card.089.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec3.card.089.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec3.card.089.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec4.card.090.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec4.card.090.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec4.card.090.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec4.card.090.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec4.card.091.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec4.card.091.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec4.card.091.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec4.card.091.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art338_sec4.card.092.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_murder_attempt`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art338_sec4.card.092.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_murder_attempt`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art338_sec4.card.092.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_murder_attempt`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art338_sec4.card.092.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art338_sec4.robbery_murder_attempt`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec1.card.093.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec1.robbery_scope`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec1.card.093.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec1.robbery_scope`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec1.card.093.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec1.robbery_scope`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec1.card.093.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec1.robbery_scope`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec2.card.094.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2.preparation_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec2.card.094.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2.preparation_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec2.card.094.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2.preparation_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec2.card.094.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2.preparation_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec2_1.card.095.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec2_1.card.095.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec2_1.card.095.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec2_1.card.095.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec2_2.card.096.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_2.preparation_examples`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec2_2.card.096.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_2.preparation_examples`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec2_2.card.096.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_2.preparation_examples`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec2_2.card.096.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_2.preparation_examples`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec2_3.card.097.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec2_3.card.097.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec2_3.card.097.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec2_3.card.097.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art343_sec3.card.098.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `robbery.art343_sec3.card.098.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `robbery.art343_sec3.card.098.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `robbery.art343_sec3.card.098.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `robbery.art333_sec3_1.component.robbery_object_property_satisfied.01`

이 규칙은 **객체 요건 중 재물(강취 대상)이 인정됨 — 재물강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333.component.robbery_object_benefit_satisfied.01`

이 규칙은 **객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 마약구입대금 또는 장물 대가를 임치받아 보관하던 사람이 그 반환을 면하기 위하여 채권자 또는 임치인을 살해한 경우 강도살인죄가 성립한다.

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec4_1.component.robbery_object_benefit_satisfied.02`

이 규칙은 **객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 재산상 이득은 사법상 유효한 이득에 한정되지 않으며, 외견상 재산상 이득을 얻을 사실관계가 인정되면 성립할 수 있다.

연결 NormCard: `art333_sec4_1.apparent_property_benefit`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec4_1.component.robbery_object_benefit_satisfied.03`

이 규칙은 **객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄의 재산상 이익은 재물 이외의 일체의 재산적 가치와 이득으로서 적극적·소극적, 영구적·일시적 이익을 모두 포함한다.

연결 NormCard: `art333_sec4_1.property_benefit`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec4_2.component.robbery_object_benefit_satisfied.04`

이 규칙은 **객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 처분행위 필요 여부와 별도로, 재산상 이익이 사실상 피해자에게 불리하게 범인 또는 제3자에게 이전된 것으로 볼 상태가 조성되어야 하며, 단순히 일시적으로 채권자 추급을 면한 정도를 넘어 채권 추급을 받지 않거나 현저히 곤란하게 한 상태가 필요하다.

연결 NormCard: `art333_sec4_2.debt_evasion_benefit_transfer`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec4_2.component.robbery_object_benefit_satisfied.05`

이 규칙은 **객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.

연결 NormCard: `art333_sec4_2.debt_evasion_disposition_not_required`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_1.component.robbery_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_1.component.robbery_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.

연결 NormCard: `art333_sec2_1.violence_threat_resistance_suppression`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_2.component.robbery_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.

연결 NormCard: `art333_sec2_2.drug_induced_incapacitation_violence`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_3.component.robbery_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.

연결 NormCard: `art333_sec2_3.apparent_capacity_threat`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_3.component.robbery_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.

연결 NormCard: `art333_sec2_3.objective_resistance_suppression`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_3.component.robbery_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.

연결 NormCard: `art333_sec2_3.snatching_forceful_attack`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_3.component.robbery_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.

연결 NormCard: `art333_sec2_3.weapon_presentation_context`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_4.component.robbery_conduct_satisfied.08`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.

연결 NormCard: `art333_sec2_4.target_person_obstructing_taking`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec3.component.robbery_conduct_satisfied.09`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.

연결 NormCard: `art333_sec3.forcible_taking`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec3_3.component.robbery_causation_satisfied.01`

이 규칙은 **행위와 결과의 연결(인과·귀속)이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec3_3.component.robbery_causation_satisfied.02`

이 규칙은 **행위와 결과의 연결(인과·귀속)이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.

연결 NormCard: `art333_sec3_3.continuing_force_single_robbery`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec3_3.component.robbery_causation_satisfied.03`

이 규칙은 **행위와 결과의 연결(인과·귀속)이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.

연결 NormCard: `art333_sec3_3.rape_fear_state_property_provision`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec3_3.component.robbery_causation_satisfied.04`

이 규칙은 **행위와 결과의 연결(인과·귀속)이 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.

연결 NormCard: `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec5.component.robbery_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec5.component.robbery_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.

연결 NormCard: `art333_sec5.illegal_benefit_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec6.component.robbery_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec6.component.robbery_completion_satisfied.02`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.

연결 NormCard: `art333_sec6.attempt_debt_evasion_killing`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec6.component.robbery_completion_satisfied.03`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.

연결 NormCard: `art333_sec6.attempt_intent_arising_after_subjugation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec6.component.robbery_completion_satisfied.04`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.

연결 NormCard: `art333_sec6.attempt_unattained_objective`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec7_1.component.robbery_completion_property_satisfied.01`

이 규칙은 **기수 요건 중 재물강취 기수(배타적 지배 취득)가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄는 피해자의 재물 점유를 배제하고 재물을 자기 지배하에 이전한 때 기수가 된다.

연결 NormCard: `art333_sec7_1.completion.exclusive_control_transfer`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec7_1.component.robbery_completion_property_satisfied.02`

이 규칙은 **기수 요건 중 재물강취 기수(배타적 지배 취득)가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피해자의 일반적 사실상 지배·관리 영역 안에서 물건을 취득했더라도 범인이 그 물건에 대한 배타적 지배를 취득한 것으로 평가되면 강도 기수가 된다.

연결 NormCard: `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec7_2.component.robbery_completion_benefit_satisfied.01`

이 규칙은 **기수 요건 중 이득강취 기수(이익 이전)가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강제이득죄는 폭행·협박으로 재산상 이익을 취득한 것으로 평가되는 때, 즉 외관상 재산상 이익 이전이 일어난 때 기수가 된다.

연결 NormCard: `art333_sec7_2.completion_forcible_gain`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `robbery.art333_sec2_2.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec2_2.bar.002`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인의 행위로 이미 피해자가 혼취상태에 빠진 후 이를 이용하여 재물을 탈취한 경우에는 강도죄의 폭행에 해당하지 않는다.

연결 NormCard: `art333_sec2_2.preexisting_incapacitation_exception`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art333_sec2_3.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec2_3.bar.004`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art333_sec2_3.bar.005`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 이르지 못한 경우에는 범인에게 주관적 반항억압 의사가 있어도 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec2_3.subjective_intent_insufficient`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art333_sec3_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec3_2.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec3_3.bar.008`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도 기수로 범인의 재물에 대한 배타적 지배가 성립한 뒤, 탈환 방지·체포 면탈·증거인멸 목적으로 폭행·협박을 한 경우에는 준강도에 해당한다.

연결 NormCard: `art333_sec3_3.completed_theft_quasi_robbery_exception`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art333_sec3_3.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec6.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec6.bar.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art333_sec8.bar.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art335_sec2.bar.013`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art335_sec2.bar.014`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art335_sec6_1.bar.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art335_sec6_2.bar.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art337_sec3_2.bar.017`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art337_sec3_2.bar.018`

이 규칙은 **극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — 평가는 되었으나 성립·불성립을 만들지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 기록만 한다.

### `robbery.art338_sec2.bar.019`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.art338_sec3.bar.020`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `robbery.component.l1.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 사람의 반항을 억압할 정도의 혼취·상해·살인 등 인신 공격행위는 폭행죄상 폭행 개념에 미달하거나 이를 초과하더라도 강도죄의 폭행에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강도죄의 폭행·협박은 재물탈취의 방법으로 행사되어 상대방의 반항을 억압할 정도이어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 약물을 유효한 약제인 것처럼 속여 스스로 복용하게 하는 등의 방법으로 혼취상태에 빠뜨려 재물을 탈취하는 경우도 강도죄의 폭행에 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 객관적으로 반항억압 외관을 갖추고 일반인이 피해자가 처한 사정에서 완구권총 등을 진짜 무기라고 오인하는 것이 보통인 경우에는 실제 가해능력이 없어도 강도죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 반항억압 여부는 피해자와 같은 상황에 놓인 일반인을 기준으로, 범행 시각·장소, 범인과 피해자의 성별·연령·체력 등 구체적 사정을 고려하여 객관적으로 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 날치기 과정에서 급격한 공격으로 기대되는 피해자의 반항을 억압하여 불가능하게 한 경우에는 반항억압에 족한 폭행으로 재물을 탈취한 강도에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 흉기를 겨누거나 제시한 행위만으로 반항억압 정도라고 단정할 수 없고, 당시 언동, 피해자의 나이·성별 및 범행 시간·장소 등 구체적 사정에 따라 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강도죄에서 폭행·협박의 상대방은 재물탈취 목적 수행에 장애가 되는 자이면 되고, 재물의 소유자·점유자 또는 재물을 보호할 지위에 있는 자일 필요는 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강취는 피해자의 반항을 억압함에 족한 폭행·협박의 방법으로 피해자의 의사에 반하여 재물의 점유를 탈취하여 자기 또는 제3자의 지배로 이전하는 것이다.

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `robbery.component.l2.mandatory_negative.04`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 처음에는 강도 범의 없이 절도에 착수하였더라도, 피해자 저항을 폭행·협박으로 제압하여 재물탈취를 수행하거나 탈취 재물의 점유를 확보하기 위해 폭행·협박을 사용한 경우에는 강취로 볼 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박이 재물탈취 범의 발생 전후로 계속되어 전체적·실질적으로 단일한 재물탈취 범의의 실현행위로 평가되는 경우에는 포괄하여 강도 일죄가 성립하며, 그 폭행으로 상해 결과가 발생하면 강도상해죄 일죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강간 피해자가 범인의 폭행·협박으로 공포 상태에 빠져 있는 것을 이용해 금품을 강탈하거나, 범행 중지와 자발적 퇴거를 간청하며 제공한 금품을 수령한 경우에는 강도가 된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 이를 탈취한 경우에도 강도죄가 성립한다.

연결 NormCard: `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`

검토 메모: 구성요건 L2에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `robbery.component.l3.mandatory_negative.05`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 채권자를 폭행·협박하여 채무를 면탈하는 강도죄에서 불법이득의사는 피고인과 피해자 관계, 채무 종류·액수, 폭행 경위·정도·방법 및 폭행 후 정황 등 범행 전후 객관적 사정을 종합하여 신중하고 면밀하게 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 강도죄가 성립하려면 불법영득 또는 불법이득의 의사가 있어야 한다.

연결 NormCard: `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`

검토 메모: 구성요건 L3에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `robbery.component.l4.mandatory_negative.06`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 강도행위는 재물탈취 또는 재산상 불법이득을 목적으로 피해자의 반항을 억압할 만한 폭행·협박을 개시한 때 실행에 착수한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 채무면탈을 위한 채권자 살해행위가 강도죄를 구성하는 경우에는 살해행위에 착수한 때 강도살인죄의 실행에 착수한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 폭행·협박으로 피해자를 제압한 후 재물탈취 또는 재산상 이익 취득의 범의가 생긴 경우에는 그 범의가 생긴 시점을 강도 실행의 착수 시기로 본다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 피해자의 반항을 억압할 만한 폭행·협박을 가하였으면 실제로 반항을 억압하거나 재물탈취 또는 불법이득 목적을 이루지 못했더라도 강도미수죄가 성립한다.

연결 NormCard: `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 구성요건 L4에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `robbery.core.outcome.track.property`

이 규칙은 **대안적 실행형태 'property' 트랙의 component가 공유 component와 함께 모두 충족됨**을 도출한다.

필요한 전제:

- 실행행위 요건이 충족됨
- 행위와 결과의 연결(인과·귀속)이 인정됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름
- 객체 요건 중 재물(강취 대상)이 인정됨 — 재물강취 트랙 전용
- 기수 요건 중 재물강취 기수(배타적 지배 취득)가 인정됨

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 공유 component와 'property' 트랙 전용 component를 AND 결합한다.

### `robbery.core.outcome.elements_satisfied.property`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 대안적 실행형태 'property' 트랙의 component가 공유 component와 함께 모두 충족됨

연결 NormCard: `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`

검토 메모: 'property' 트랙이 충족되면 구성요건 전체가 충족된 것으로 본다(대안적 실행형태이므로 트랙끼리는 OR).

### `robbery.core.outcome.track.benefit`

이 규칙은 **대안적 실행형태 'benefit' 트랙의 component가 공유 component와 함께 모두 충족됨**을 도출한다.

필요한 전제:

- 실행행위 요건이 충족됨
- 행위와 결과의 연결(인과·귀속)이 인정됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름
- 객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용
- 기수 요건 중 이득강취 기수(이익 이전)가 인정됨

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec7_2.completion_forcible_gain`

검토 메모: 공유 component와 'benefit' 트랙 전용 component를 AND 결합한다.

### `robbery.core.outcome.elements_satisfied.benefit`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 대안적 실행형태 'benefit' 트랙의 component가 공유 component와 함께 모두 충족됨

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec7_2.completion_forcible_gain`

검토 메모: 'benefit' 트랙이 충족되면 구성요건 전체가 충족된 것으로 본다(대안적 실행형태이므로 트랙끼리는 OR).

### `robbery.core.outcome.track_conflict.property_benefit`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 대안적 실행형태 'property' 트랙의 component가 공유 component와 함께 모두 충족됨
- 대안적 실행형태 'benefit' 트랙의 component가 공유 component와 함께 모두 충족됨

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 서로 배타적이어야 할 두 트랙이 동시에 완전히 충족되면 어느 실행형태인지 모호해지므로 임의로 하나를 고르지 않고 충돌로 보류한다.

### `robbery.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `robbery.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art333.illegal_cause_debt_evasion_robbery_murder`, `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_2.preexisting_incapacitation_exception`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec2_3.lesser_threat_extortion`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.subjective_intent_insufficient`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_1.real_estate_as_robbery_property_negative`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.completed_theft_quasi_robbery_exception`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec4_1.apparent_property_benefit`, `art333_sec4_1.property_benefit`, `art333_sec4_2.debt_evasion_benefit_transfer`, `art333_sec4_2.debt_evasion_disposition_not_required`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec7_1.completion.exclusive_control_transfer`, `art333_sec7_1.completion.exclusive_control_within_victim_domain`, `art333_sec7_1.completion.no_safe_escape_requirement`, `art333_sec7_1.completion.recovery_does_not_negate`, `art333_sec7_2.completion_forcible_gain`, `art333_sec8.right_exercise_robbery_negative`, `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`, `art334_sec1.nighttime_robbery_damage_irrelevant`, `art334_sec2_1.weapon_awareness_not_required`, `art334_sec2_1.weapon_carried_fists_used`, `art334_sec2_1.weapon_direct_use_not_required`, `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`, `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`, `art335_sec1.aggravated_robbery_offenses_apply`, `art335_sec2.actor_thief`, `art335_sec2.preparation_stage_exclusion`, `art335_sec2.property_interest_exclusion`, `art335_sec3.special_purpose`, `art335_sec3_1.pre_control_violence_is_robbery_exception`, `art335_sec3_1.recapture_opponent_need_not_act`, `art335_sec3_1.recapture_resistance_after_exclusive_control`, `art335_sec3_2.anticipated_arrest_violence`, `art335_sec3_2.arrest_or_concealment_no_control`, `art335_sec3_2.escape_arrest_accomplice`, `art335_sec3_3.concealing_crime_traces`, `art335_sec3_4.purpose_achievement_irrelevant`, `art335_sec4.objective_capacity`, `art335_sec4.police_officer_general_person_standard`, `art335_sec4.violence_resistance_threshold`, `art335_sec5.violence_threat_target`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_1.opportunity_temporal_spatial_proximity`, `art335_sec6_2.opportunity_definition`, `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`, `art335_sec6_2.opportunity_safe_escape_limit`, `art335_sec7.attempt_punishable`, `art335_sec7_1.attempt_theft_act_standard`, `art335_sec7_1.supreme_court_completion_by_theft`, `art335_sec8.weapon_acquired_during_violence.reported_precedent`, `art337_sec2.subject_robber_and_attempted_robber`, `art337_sec3.injury_result_violence_intent`, `art337_sec3_2.injury_concrete_victim_condition`, `art337_sec3_2.injury_threshold`, `art337_sec3_2.robbery_occasion_ended`, `art337_sec3_2.trivial_injury_excluded`, `art337_sec4.completion_injury_result`, `art338_sec1.robbery_death_result_aggravated`, `art338_sec1.robbery_murder_intent`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec2.debt_evasion_robbery`, `art338_sec3.delayed_death_no_effect`, `art338_sec3.opportunity_immediate_flight_killing`, `art338_sec3.opportunity_new_intent_after_completion`, `art338_sec4.murder_completion_controls_attempt`, `art338_sec4.robbery_death_attempt_excluded`, `art338_sec4.robbery_murder_attempt`, `art343_sec1.robbery_scope`, `art343_sec2.preparation_definition`, `art343_sec2_1.contingent_intent_sufficient_precedent`, `art343_sec2_2.preparation_examples`, `art343_sec2_3.home_invasion_robbery_departure`, `art343_sec3.abandonment_before_execution_denied`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `robbery.art333_sec2_2.track_bar.property.001`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec2_3.track_bar.property.002`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec3_2.track_bar.property.003`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec3_2.track_bar.property.004`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec3_3.track_bar.property.005`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec6.track_bar.property.006`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec6.track_bar.property.007`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art333_sec8.track_bar.property.008`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art335_sec6_1.track_bar.property.009`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art335_sec6_2.track_bar.property.010`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art338_sec2.track_bar.property.011`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.art338_sec3.track_bar.property.012`

이 규칙은 **'property' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'property' track에서 성립을 부정한다.

### `robbery.property.has_negative`

이 규칙은 **'property' track에 국한된 불성립 사유의 존재를 2항으로 요약함**을 도출한다.

필요한 전제:

- 'property' track에 국한된 명시적 불성립 사유가 존재함

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 'property' track에 국한된 불성립 사유를 완결 게이트가 검사할 2항 relation으로 모은다.

### `robbery.outcome.property.established`

이 규칙은 **완결 게이트 뒤에 'property' track의 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 대안적 실행형태 'property' 트랙의 component가 공유 component와 함께 모두 충족됨
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 'property' track에 국한된 불성립 사유의 존재를 2항으로 요약함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 'property' track의 component가 모두 충족되고, 완결 게이트 뒤 이 track 전용 불성립 사유와 사건 전체의 충돌이 모두 없을 때만 이 track의 확정 성립을 낸다.

### `robbery.core.outcome.established.union.property`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 'property' track의 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 'property' track의 확정 성립을 죄명 전체의 확정 성립으로 합친다(순수 OR, 부정 없음).

### `robbery.art333_sec2_2.track_bar.benefit.001`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 다른 목적으로 피해자를 혼취상태에 빠뜨린 뒤 우발적으로 재물을 탈취한 경우, 혼취가 재물탈취 방법으로 사용된 것이 아니므로 강도죄가 성립하지 않는다.

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec2_3.track_bar.benefit.002`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec3_2.track_bar.benefit.003`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소지품 탈취 후의 구타가 재물탈취와 관련하여 반항억압, 재물 탈환, 체포면탈 또는 증거인멸에 객관적 효과를 미친 것이 아니라면 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec3_2.post_taking_assault_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec3_2.track_bar.benefit.004`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적으로 반항억압에 족한 폭행·협박이 있었더라도 피해자가 귀찮음이나 연민으로 반항 의사 억압 없이 재물을 교부한 경우에는 인과관계가 없어 강도미수죄만 성립한다.

연결 NormCard: `art333_sec3_2.voluntary_delivery_attempt`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec3_3.track_bar.benefit.005`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec6.track_bar.benefit.006`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 개시한 폭행·협박이 사회통념상 피해자의 반항을 억압할 만한 정도가 아니면 강도 실행의 착수가 인정되기 어렵다.

연결 NormCard: `art333_sec6.no_attempt_insufficient_violence_intimidation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec6.track_bar.benefit.007`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취에 착수하였더라도 폭행·협박 자체에 착수하지 않으면 강도죄의 실행 착수가 인정되지 않는다.

연결 NormCard: `art333_sec6.no_attempt_without_violence_intimidation_commencement`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art333_sec8.track_bar.benefit.008`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art335_sec6_1.track_bar.benefit.009`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art335_sec6_2.track_bar.benefit.010`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art338_sec2.track_bar.benefit.011`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.art338_sec3.track_bar.benefit.012`

이 규칙은 **'benefit' track에 국한된 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 'benefit' track에서 성립을 부정한다.

### `robbery.benefit.has_negative`

이 규칙은 **'benefit' track에 국한된 불성립 사유의 존재를 2항으로 요약함**을 도출한다.

필요한 전제:

- 'benefit' track에 국한된 명시적 불성립 사유가 존재함

연결 NormCard: `art333_sec2_2.incidental_incapacitation_no_robbery`, `art333_sec2_3.diversion_or_insult_violence_no_robbery`, `art333_sec3_2.post_taking_assault_no_robbery`, `art333_sec3_2.voluntary_delivery_attempt`, `art333_sec3_3.unconsciousness_prior_force_no_causation`, `art333_sec6.no_attempt_insufficient_violence_intimidation`, `art333_sec6.no_attempt_without_violence_intimidation_commencement`, `art333_sec8.right_exercise_robbery_negative`, `art335_sec6_1.days_later_no_opportunity`, `art335_sec6_2.opportunity_safe_escape_limit`, `art338_sec2.debt_evasion_no_robbery`, `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 'benefit' track에 국한된 불성립 사유를 완결 게이트가 검사할 2항 relation으로 모은다.

### `robbery.outcome.benefit.established`

이 규칙은 **완결 게이트 뒤에 'benefit' track의 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 대안적 실행형태 'benefit' 트랙의 component가 공유 component와 함께 모두 충족됨
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 'benefit' track에 국한된 불성립 사유의 존재를 2항으로 요약함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 'benefit' track의 component가 모두 충족되고, 완결 게이트 뒤 이 track 전용 불성립 사유와 사건 전체의 충돌이 모두 없을 때만 이 track의 확정 성립을 낸다.

### `robbery.core.outcome.established.union.benefit`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 'benefit' track의 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 'benefit' track의 확정 성립을 죄명 전체의 확정 성립으로 합친다(순수 OR, 부정 없음).

### `robbery.art333_sec7_1.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물강취죄의 기수에는 범행현장을 이탈하여 경계망을 돌파하고 안전지역으로 나갈 것이 필요하지 않다.

연결 NormCard: `art333_sec7_1.completion.no_safe_escape_requirement`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art333_sec7_1.requirement_waived.002`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박으로 탈취물에 대한 배타적 지배를 취득하였다면, 피해자가 범행현장 가까운 곳에서 이를 다시 탈환하였더라도 강도 기수 인정에는 영향이 없다.

연결 NormCard: `art333_sec7_1.completion.recovery_does_not_negate`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art334_sec2_1.requirement_waived.003`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art334_sec2_1.requirement_waived.004`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art335_sec3_2.requirement_waived.005`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art338_sec4.requirement_waived.006`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `robbery.art333_sec2_3.boundary_shift.001`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `robbery.art333_sec2_3.boundary_shift.002`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `robbery.art333_sec3_3.boundary_shift.003`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `robbery.art333_sec8.boundary_shift.004`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `robbery.art338_sec2.boundary_shift.005`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `robbery.art343_sec3.post_outcome.001`

이 규칙은 **구성요건 판단 뒤에 오는 죄수·처벌 효과**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 불가벌적 사후행위 등은 구성요건 불성립과 구별해 별도로 기록한다.

### `robbery.art333_sec2_3.refers_to_crime.001`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물절취 때의 폭행·협박이 단지 주의를 다른 데로 돌리기 위한 것이거나, 탈취 후 모욕적 의사 또는 적개심 표시만을 위한 것이라면 강도죄가 아니라 폭행 또는 협박죄와 절도죄가 성립한다.

연결 NormCard: `art333_sec2_3.diversion_or_insult_violence_no_robbery`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `robbery.art333_sec2_3.refers_to_crime.002`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취 목적의 폭행·협박이 반항억압 정도에 이르지 않고 공포심만 일으켜 피해자가 자신의 의사에 따라 재물을 제공한 경우에는 공갈죄가 성립할 뿐 강도죄는 성립하지 않는다.

연결 NormCard: `art333_sec2_3.lesser_threat_extortion`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `robbery.art333_sec3_3.refers_to_crime.003`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 경합범이 성립한다.

연결 NormCard: `art333_sec3_3.unconsciousness_prior_force_no_causation`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `robbery.art333_sec8.refers_to_crime.004`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.

연결 NormCard: `art333_sec8.right_exercise_robbery_negative`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `robbery.art338_sec2.refers_to_crime.005`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `robbery.aggravation.death.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도치사죄는 결과적 가중범으로서 살해의 고의는 필요하지 않으나 폭행·협박행위의 고의를 요한다.

연결 NormCard: `art338_sec1.robbery_death_result_aggravated`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄는 강도의 실행 중 또는 그 기회에 그 수단인 행위나 그 밖의 행위로 사람을 살해함으로써 성립하는 고의범이다.

연결 NormCard: `art338_sec1.robbery_murder_intent`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 있고 채권 존재를 확인할 방법이 확보된 경우, 채무자가 채무면탈 목적으로 채권자를 살해하여도 재산적 이익의 지배를 취득하였다고 보기 어려워 강도가 될 수 없고 단순 살인죄에 그칠 수 있다.

연결 NormCard: `art338_sec2.debt_evasion_no_robbery`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.

연결 NormCard: `art338_sec2.debt_evasion_robbery`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.

연결 NormCard: `art338_sec3.delayed_death_no_effect`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 재물강취가 종료된 뒤라도 발각을 두려워 퇴거하면서 사람을 살해하거나 추적해 온 피해자를 살해한 경우에는 강도의 기회에 살인한 것으로 볼 수 있다.

연결 NormCard: `art338_sec3.opportunity_immediate_flight_killing`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도 범행이 종료된 뒤 상당한 시간이 경과하여 새로운 범의로 저지른 살해행위는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art338_sec3.opportunity_new_intent_after_completion`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.008`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도살인죄의 기수·미수는 강도행위의 기수 여부가 아니라 살인행위의 기수·미수에 따라 정한다.

연결 NormCard: `art338_sec4.murder_completion_controls_attempt`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.009`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 살인의 고의가 없는 강도치사죄에는 미수범이 인정되지 않는다.

연결 NormCard: `art338_sec4.robbery_death_attempt_excluded`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.death.010`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도가 살의로 가해행위를 하였으나 살해 목적을 이루지 못한 살인미수의 경우 강도살인죄의 미수가 된다.

연결 NormCard: `art338_sec4.robbery_murder_attempt`

검토 메모: 기본범이 성립한 위에 death 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 주체는 단순강도·특수강도·준강도·인질강도의 강도범을 포함하며, 강도의 기수·미수와 관계없이 강도행위의 실행착수가 있으면 주체가 될 수 있다.

연결 NormCard: `art337_sec2.subject_robber_and_attempted_robber`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 적어도 폭행의 고의는 있어야 한다.

연결 NormCard: `art337_sec3.injury_result_violence_intent`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다.

연결 NormCard: `art337_sec3_2.injury_concrete_victim_condition`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다.

연결 NormCard: `art337_sec3_2.injury_threshold`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다.

연결 NormCard: `art337_sec3_2.robbery_occasion_ended`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다.

연결 NormCard: `art337_sec3_2.trivial_injury_excluded`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.injury.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 형법 제337조 위반죄는 상해 결과가 발생함으로써 기수가 되며, 재물탈취 목적의 달성은 요구되지 않는다.

연결 NormCard: `art337_sec4.completion_injury_result`

검토 메모: 기본범이 성립한 위에 injury 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 제343조의 ‘강도’에는 단순강도, 특수강도, 약취강도 및 해상강도가 포함되나 준강도는 제외된다.

연결 NormCard: `art343_sec1.robbery_scope`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다.

연결 NormCard: `art343_sec2.preparation_definition`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.

연결 NormCard: `art343_sec2_1.contingent_intent_sufficient_precedent`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다.

연결 NormCard: `art343_sec2_2.preparation_examples`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 주거침입강도 목적으로 흉기를 휴대하고 목적지를 향하여 출발하면 강도예비죄가 성립하며, 목적지 도달이나 주거침입 후 기회 관망은 필요하지 않다.

연결 NormCard: `art343_sec2_3.home_invasion_robbery_departure`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.preparation.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.

연결 NormCard: `art343_sec3.abandonment_before_execution_denied`

검토 메모: 기본범이 성립한 위에 preparation 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도는 강도상해치상죄, 강도살인치사죄 및 강도강간죄의 적용을 받는 강도에 해당한다.

연결 NormCard: `art335_sec1.aggravated_robbery_offenses_apply`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다.

연결 NormCard: `art335_sec2.actor_thief`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다.

연결 NormCard: `art335_sec2.preparation_stage_exclusion`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다.

연결 NormCard: `art335_sec2.property_interest_exclusion`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.

연결 NormCard: `art335_sec3.special_purpose`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 재물을 탈취하였더라도 아직 배타적 지배가 확립되지 않은 상태에서 지배 확보를 위하여 폭행·협박을 한 경우는 준강도가 아니라 본래의 강도이다.

연결 NormCard: `art335_sec3_1.pre_control_violence_is_robbery_exception`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적은 폭행·협박 사실이 있으면 충분하며, 그 상대방이 실제로 재물탈환 행위를 하였을 필요는 없다.

연결 NormCard: `art335_sec3_1.recapture_opponent_need_not_act`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.008`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 재물탈환 항거 목적의 준강도는 절도범이 재물을 자신의 배타적 지배 아래로 옮긴 뒤 피해자의 추적을 피할 목적으로 폭행·협박을 한 경우에 해당한다.

연결 NormCard: `art335_sec3_1.recapture_resistance_after_exclusive_control`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.009`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방이 현실적으로 체포행위에 착수하지 않았거나 범인이 체포를 예상하여 먼저 폭행·협박한 경우에도 체포 면탈 목적이 인정될 수 있다.

연결 NormCard: `art335_sec3_2.anticipated_arrest_violence`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.010`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 체포 방지 또는 범죄 흔적 인멸 목적의 경우에는 재물에 대한 지배 취득이 요건이 아니다.

연결 NormCard: `art335_sec3_2.arrest_or_concealment_no_control`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.011`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 체포 면탈 목적에는 절도범 자신뿐 아니라 공범자의 체포를 면탈하게 하는 경우도 포함된다.

연결 NormCard: `art335_sec3_2.escape_arrest_accomplice`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.012`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다.

연결 NormCard: `art335_sec3_3.concealing_crime_traces`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.013`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 목적은 주관적 구성요소이므로 그 목적의 달성 여부는 기수·미수와 관계없다.

연결 NormCard: `art335_sec3_4.purpose_achievement_irrelevant`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.014`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 일반적·객관적으로 반항 억압 정도로 인정되면 충분하고, 현실적으로 또는 실제로 상대방을 제압하였을 필요는 없다.

연결 NormCard: `art335_sec4.objective_capacity`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.015`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 경찰관에게 현실적으로 체포수행 의사를 제압하기 부족한 폭행·협박이라도 일반인의 의사를 제압하기에 족한 정도이면 준강도의 폭행·협박에 해당한다.

연결 NormCard: `art335_sec4.police_officer_general_person_standard`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.016`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박은 사람의 반항을 억압할 정도, 즉 체포수행 의사 또는 재물탈환 의사를 제압할 정도여야 한다.

연결 NormCard: `art335_sec4.violence_resistance_threshold`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.017`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 폭행·협박 상대방은 절도 피해자에 한정되지 않고, 재물 탈환 항거·체포 면탈·범죄 흔적 인멸 목적 달성에 필요한 모든 공격대상을 포함한다.

연결 NormCard: `art335_sec5.violence_threat_target`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.018`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

연결 NormCard: `art335_sec6_1.days_later_no_opportunity`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.019`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 폭행·협박은 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여져야 한다.

연결 NormCard: `art335_sec6_1.opportunity_temporal_spatial_proximity`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.020`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 판례상 절도의 기회는 절도범과 피해자 측이 현장에 있거나, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있거나, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 의미한다.

연결 NormCard: `art335_sec6_2.opportunity_definition`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.021`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 피해자 측이 추적태세에 있거나 범인이 일단 체포되었어도 아직 신병확보가 확실하지 않은 경우에는 절도의 기회에 해당한다.

연결 NormCard: `art335_sec6_2.opportunity_pursuit_or_uncertain_custody`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.022`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 절도범이 원래 범행현장에서 안전하게 도피하여 더 이상 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있으면 절도의 기회 계속성을 인정하기 어렵다.

연결 NormCard: `art335_sec6_2.opportunity_safe_escape_limit`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.023`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도죄의 미수범은 처벌된다.

연결 NormCard: `art335_sec7.attempt_punishable`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.024`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.

연결 NormCard: `art335_sec7_1.attempt_theft_act_standard`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.025`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다.

연결 NormCard: `art335_sec7_1.supreme_court_completion_by_theft`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.quasi.026`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.

연결 NormCard: `art335_sec8.weapon_acquired_during_violence.reported_precedent`

검토 메모: 기본범이 성립한 위에 quasi 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 단순강도와 주거침입이 결합된 가중유형이다.

연결 NormCard: `art334_sec1.nighttime_home_intrusion_robbery_aggravated_combination`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.

연결 NormCard: `art334_sec1.nighttime_robbery_damage_irrelevant`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서는 상대방이 흉기휴대를 인식할 것이 요구되지 않는다.

연결 NormCard: `art334_sec2_1.weapon_awareness_not_required`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 휴대한 흉기를 제시하지 않고 주먹 등으로만 폭행·협박하여 상대방을 제압한 경우에도 제334조 제2항 특수강도죄에 해당할 수 있다.

연결 NormCard: `art334_sec2_1.weapon_carried_fists_used`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.005`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 흉기휴대 특수강도에서 휴대한 흉기를 피해자에게 제시하거나 겨누는 등 폭행·협박의 방법으로 직접 사용할 필요는 없다.

연결 NormCard: `art334_sec2_1.weapon_direct_use_not_required`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.006`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 주간에 이루어진 흉기휴대·합동강도죄는 폭행·협박 시에 실행에 착수한다.

연결 NormCard: `art334_sec3.daytime_weapon_or_joint_robbery_attempt_on_violence_threat`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.aggravation.special.007`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.

연결 NormCard: `art334_sec3.nighttime_home_intrusion_attempt_on_intrusion`

검토 메모: 기본범이 성립한 위에 special 가중요건이 충족되면 플래그를 켠다.

### `robbery.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art333_sec2_1.robbery_violence_incapacitating_attack`, `art333_sec2_1.violence_threat_resistance_suppression`, `art333_sec2_2.drug_induced_incapacitation_violence`, `art333_sec2_3.apparent_capacity_threat`, `art333_sec2_3.objective_resistance_suppression`, `art333_sec2_3.snatching_forceful_attack`, `art333_sec2_3.weapon_presentation_context`, `art333_sec2_4.target_person_obstructing_taking`, `art333_sec3.forcible_taking`, `art333_sec3_3.continuing_force_after_theft_intent`, `art333_sec3_3.continuing_force_single_robbery`, `art333_sec3_3.rape_fear_state_property_provision`, `art333_sec3_3.rape_force_subsequent_taking_precedent`, `art333_sec5.determine_illegal_benefit_intent`, `art333_sec5.illegal_benefit_intent`, `art333_sec6.attempt_commencement_violence_intimidation`, `art333_sec6.attempt_debt_evasion_killing`, `art333_sec6.attempt_intent_arising_after_subjugation`, `art333_sec6.attempt_unattained_objective`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
