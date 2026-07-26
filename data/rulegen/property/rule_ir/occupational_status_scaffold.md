# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.occupational_status.full.v1_candidate`
- predicate: 32개
- rule: 53개
- NormCard: 10개

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

### `occupational_status_case_roles(case_id: String, defendant_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art356_dual_status(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art356.dual_status`

### `satisfied_art356_dual_status(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`

### `assess_art356_offense_character(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art356.offense_character`

### `satisfied_art356_offense_character(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.offense_character`

### `assess_art356_sec2_1_business_continuity_status(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_1.business_continuity_status`

### `satisfied_art356_sec2_1_business_continuity_status(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무에는 계속성과 사회생활상의 지위가 요구된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_1.business_continuity_status`

### `assess_art356_sec2_1_business_definition(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_1.business_definition`

### `satisfied_art356_sec2_1_business_definition(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_1.business_definition`

### `assess_art356_sec2_1_business_no_livelihood_or_formal_office(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

### `satisfied_art356_sec2_1_business_no_livelihood_or_formal_office(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

### `assess_art356_sec2_1_employee_assistant_business_status(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

### `satisfied_art356_sec2_1_employee_assistant_business_status(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

### `assess_art356_sec2_1_incidental_business_relation(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_1.incidental_business_relation`

### `satisfied_art356_sec2_1_incidental_business_relation(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_1.incidental_business_relation`

### `assess_art356_sec2_2_administrative_illegality(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art356_sec2_2.administrative_illegality`

### `satisfied_art356_sec2_2_administrative_illegality(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.administrative_illegality`

### `assess_art356_sec2_2_illegal_business(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_2.illegal_business`

### `satisfied_art356_sec2_2_illegal_business(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.illegal_business`

### `assess_art356_sec3_3_status_awareness(case_id: String, assessment_id: String, defendant_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec3_3.status_awareness`

### `satisfied_art356_sec3_3_status_awareness(case_id: String, defendant_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec3_3.status_awareness`

### `occupational_status_object_satisfied(case_id: String, defendant_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec3_3.status_awareness`

### `occupational_status_elements_satisfied(case_id: String, defendant_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec3_3.status_awareness`

### `occupational_status_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.illegal_business`

### `occupational_status_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec2_2.illegal_business`, `art356_sec3_3.status_awareness`

### `occupational_status_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec2_2.illegal_business`, `art356_sec3_3.status_awareness`

### `occupational_status_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.illegal_business`

### `occupational_status_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec2_2.illegal_business`, `art356_sec3_3.status_awareness`

### `occupational_status_established(case_id: String, defendant_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec3_3.status_awareness`

## Rules

### `occupational_status.art356.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.dual_status`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.dual_status`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.dual_status`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.offense_character`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.offense_character`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.offense_character`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_1.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무에는 계속성과 사회생활상의 지위가 요구된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_continuity_status`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_1.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_continuity_status`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_1.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_continuity_status`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_1.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_1.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_1.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_1.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_1.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_1.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_1.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_1.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_1.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_1.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.incidental_business_relation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_1.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.incidental_business_relation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_1.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.incidental_business_relation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_2.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.administrative_illegality`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_2.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.administrative_illegality`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_2.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.administrative_illegality`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec2_2.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.illegal_business`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec2_2.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.illegal_business`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec2_2.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.illegal_business`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356_sec3_3.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_3.status_awareness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `occupational_status.art356_sec3_3.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_3.status_awareness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `occupational_status.art356_sec3_3.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_3.status_awareness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `occupational_status.art356.component.occupational_status_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.

연결 NormCard: `art356.dual_status`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356.component.occupational_status_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.

연결 NormCard: `art356.offense_character`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_1.component.occupational_status_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무에는 계속성과 사회생활상의 지위가 요구된다.

연결 NormCard: `art356_sec2_1.business_continuity_status`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_1.component.occupational_status_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.

연결 NormCard: `art356_sec2_1.business_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_1.component.occupational_status_object_satisfied.05`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.

연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_1.component.occupational_status_object_satisfied.06`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.

연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_1.component.occupational_status_object_satisfied.07`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.

연결 NormCard: `art356_sec2_1.incidental_business_relation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_2.component.occupational_status_object_satisfied.08`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.

연결 NormCard: `art356_sec2_2.administrative_illegality`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec3_3.component.occupational_status_object_satisfied.09`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.

연결 NormCard: `art356_sec3_3.status_awareness`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `occupational_status.art356_sec2_2.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다.

연결 NormCard: `art356_sec2_2.illegal_business`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `occupational_status.art356.mandatory_negative.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.dual_status`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356.mandatory_negative.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.offense_character`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_1.mandatory_negative.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무에는 계속성과 사회생활상의 지위가 요구된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_continuity_status`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_1.mandatory_negative.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 사회생활상 지위에 기초하여 반복 또는 계속적으로 행하는 사무이며, 법령ㆍ계약ㆍ관례 또는 사실상 근거 여부를 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_definition`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_1.mandatory_negative.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무는 반드시 직무ㆍ직업으로 행해지거나 생활수단일 필요가 없고, 고유 업무인지 겸무인지 또는 사실상 수행되는 사무인지도 불문한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.business_no_livelihood_or_formal_office`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_1.mandatory_negative.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 다른 업무자에게 고용되거나 보조기관으로 사무를 수행하는 사람도 계속성과 사회생활상 지위를 갖추면 업무자에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.employee_assistant_business_status`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_1.mandatory_negative.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래 사무에 부수하여 편의상 수행하는 사무도 업무가 될 수 있으나, 본래 사무와 밀접한 관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_1.incidental_business_relation`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec2_2.mandatory_negative.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.administrative_illegality`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.art356_sec3_3.mandatory_negative.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무자 지위에 관한 인식은 미필적 인식으로 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec3_3.status_awareness`

검토 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `occupational_status.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec3_3.status_awareness`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `occupational_status.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art356_sec2_2.illegal_business`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `occupational_status.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec2_2.illegal_business`, `art356_sec3_3.status_awareness`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `occupational_status.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art356.dual_status`, `art356.offense_character`, `art356_sec2_1.business_continuity_status`, `art356_sec2_1.business_definition`, `art356_sec2_1.business_no_livelihood_or_formal_office`, `art356_sec2_1.employee_assistant_business_status`, `art356_sec2_1.incidental_business_relation`, `art356_sec2_2.administrative_illegality`, `art356_sec3_3.status_awareness`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
