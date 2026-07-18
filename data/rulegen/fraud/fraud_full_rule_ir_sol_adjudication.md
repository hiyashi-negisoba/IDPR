# 사기죄 full RuleIR Sol 지적 재검토

## 결론

Sol은 1회 호출되었고 13개 지적과 `reject` 판정을 반환했다. 에이전트가 원문
NormCard, 승인된 역할 정책, RuleIR 생성기와 출력 규칙을 다시 대조했다. 11개는
수용 또는 수정수용했고, 2개는 법리·기존 승인 정책과 맞지 않아 불수용했다. 추가
API 호출 없이 모든 정정은 에이전트가 직접 했다.

## 항목별 판정

| No. | Sol 지적 | 재판정 | 반영 내용 |
|---:|---|---|---|
| 1 | `missing_subject_role_gate` | 불수용, 계약 명료화 | 사기죄는 일반범이고 법적 주체는 이미 `defendant_id`다. 별도 신분요건을 만들 근거가 없다. 오독을 만든 미정의 `subject_id`는 전체 actor tuple에서 삭제했다. 책임능력 등은 형법총칙 future work다. |
| 2 | `positive_survives_negative_outcome` | 수용 | 구성요건 AND 결과를 `fraud_elements_satisfied`라는 성립 후보로 분리했다. 완결된 사건에서 불성립 사유가 없을 때만 `fraud_established`를 출력한다. |
| 3 | `card_conflict_can_feed_positive_component` | 수용 | 모든 카드 충돌을 `fraud_has_conflict`로 모으고, 최종 성립은 이 relation이 없을 때만 허용한다. 충돌 카드의 positive support가 중간 component를 만들더라도 확정 성립에는 도달하지 못한다. |
| 4 | `non_element_loss_gate_in_final` | 수용 | 현실적 재산상 손해 불요 법리는 사실적 구성요건이 아니므로 최종 AND에서 삭제했다. |
| 5 | `loss_card_evidence_bypass` | 수용 | `fraud_no_separate_loss_gate` predicate와 자동 파생 rule을 모두 삭제했다. 취득 외 추가 손해 gate를 두지 않는 방식으로만 구현한다. |
| 6 | `deception_definition_sufficient_alone` | 수용 | 일반 기망 경로는 신의칙 위반·실제 착오 유발에 관한 사건 적용 평가와 재산적 처분 지향성을 함께 요구한다. 법률 정의가 옳다는 확인만으로는 기망 component가 나오지 않는다. |
| 7 | `mistake_definition_sufficient_alone` | 수용 | 일반 착오 경로는 구체적 사실불일치 인식과 그 착오가 처분 동기를 형성·확정했다는 판단을 함께 요구한다. |
| 8 | `acquisition_examples_sufficient_alone` | 수용 | 계약·노무·채무면제 예시 카드를 취득 component의 독립 경로에서 삭제했다. 이 카드는 RAG 판단 지원과 카드 상태 추적에만 남는다. |
| 9 | `invalid_benefit_definition_sufficient_for_acquisition` | 수정수용 | 해당 입력의 의미를 “무효 여부와 별개로 특정 수익자가 구체적·외형적 재산상 이익을 실제 취득했는가”라는 사건 적용 평가로 좁혔다. 단순한 법률상 무효 명제만으로는 satisfied가 될 수 없다. |
| 10 | `ordinary_role_adapter_overunifies_owner` | 불수용 | 승인된 정책은 피기망자=처분자이고, 재산소유자가 다르면 삼각사기 권능 심사를 요구한다. 일반형에서 동일 owner 변수를 쓰는 것은 이 분기 자체를 구현한 것이며, 이를 풀면 삼각사기 권능 gate를 우회한다. |
| 11 | `triangular_branch_lacks_distinct_owner_constraint` | 수용 | 삼각사기 adapter에 `distinct_entity(case_id, deceived_person_id, property_owner_id)`를 추가했다. |
| 12 | `third_party_branch_lacks_distinct_beneficiary_constraint` | 수용 | 제3자취득 adapter에 `distinct_entity(case_id, defendant_id, beneficiary_id)`를 추가했다. |
| 13 | `intent_standard_used_as_element` | 수용 | 단순 채무불이행과 구별되는 의도적 기망, 행위시 고의, 재산적 이득 목적을 결합했다. 또한 “처분 유도 의사가 없음”이라는 배제조건이 명시적으로 `not_satisfied`이고 증명 가능할 때만 처분 유도 의사를 긍정한다. |

## 최종 결론 계층

최종 계층만 폐쇄세계 검사를 쓴다. 사건 라우터가 관련 공통 쟁점과 선택 프로파일을
확정하고 그 유한한 평가 묶음이 모두 수집된 경우에만
`case_assessment_complete(case_id, defendant_id)`를 공급한다.

1. 공통 component AND -> `fraud_elements_satisfied`
2. 명시적 불성립 -> `fraud_has_negative`
3. 카드 또는 결론 충돌 -> `fraud_has_conflict`
4. 평가 묶음 완결 + 성립 후보 + 불성립 없음 + 충돌 없음 -> `fraud_established`

부정은 4번의 최종 층에서만 사용한다. 관련 없는 프로파일의 relation 부재를
`false`로 해석하지 않으며, 관련 있지만 판단 불가능한 쟁점은 계속 `unknown`으로 남긴다.

## 사용자 재검수 포인트

1. 일반형에서 재산소유자를 피기망자·처분자와 같은 ID로 두고, 다른 경우에는 반드시 삼각사기로 보내는 정책
2. 행위시 고의 + 처분 유도 의사 + 재산적 이득 목적을 주관적 요건으로 묶은 방식
3. `case_assessment_complete`를 관련 쟁점이 모두 수집된 뒤에만 공급하는 실행 계약

이 세 항목이 승인되면 다음 단계는 RuleIR의 Scallop 컴파일과 최소 사실 fixture를 이용한
성립·불성립·unknown·conflict 실행 테스트다.
