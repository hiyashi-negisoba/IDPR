# 사기죄 Core + Profile 구성 결과

작성일: 2026-07-19

> 이 문서는 사용자와 합의한 구조가 실제 코드에 어떻게 반영됐는지 설명한다.
> API나 로컬 LLM을 호출하지 않고 구현·검증했다.

## 1. 확정된 구조

사기죄 처리에는 완제품 plan 여섯 개를 사용하지 않는다.

```text
현재 사건의 처리 범위 = 항상 적용되는 fraud_core + 해당 사건에만 필요한 profile 0개 이상
```

- 일반 사건: `fraud_core`
- 차용 목적 사건: `fraud_core + loan_purpose`
- 변제 의사·능력과 재산상 이익이 함께 문제되는 사건:
  `fraud_core + loan_repayment + property_benefit`
- 삼각사기이면서 다른 특수 쟁점도 있는 사건: `fraud_core + triangular + 해당 profile`
- 기존 profile에 맞지 않는 사건: 우선 core를 적용하고, 없는 특수규칙은 coverage gap으로 남긴다.

따라서 profile은 상시 켜지는 분류가 아니다. 사건 사실에 해당할 때만 core에 추가된다.
여러 profile이 동시에 해당하면 하나를 고르는 것이 아니라 함께 조합한다.

## 2. 항상 적용하는 Core

Core는 최종 답안에서 다음 다섯 묶음을 항상 검토한다.

1. 객체와 역할
2. 기망
3. 착오와 처분
4. 취득·인과관계·기수
5. 행위 당시 고의, 처분 유도 의사와 재산적 이득 목적

이 다섯 묶음을 코드에서는 `unit`이라고 부른다. Unit은 모델이 사실을 추출하기 위한 질문이 아니라,
누락 없이 최종 IRAC을 구성하기 위한 목차다.

## 3. 선택 가능한 Profile

현재 registry에는 다음 profile이 있다.

| Profile | Core에 추가하는 특수 쟁점 |
|---|---|
| `loan_purpose` | 차용 목적 고지의 중요성 |
| `loan_repayment` | 차용 또는 연장 당시 변제 의사·능력 |
| `contract_performance` | 장래 급부의 이행 의사·능력과 단순 불이행 구별 |
| `implicit_deception` | 행동에 의한 묵시적 기망 |
| `property_benefit` | 재물 이외의 구체적 재산상 이익 |
| `triangular` | 피기망자·처분자와 재산 피해자가 다른 구조 및 처분 지위 |

일반 재물 취득 경로는 별도 profile이 아니라 core가 담당한다. 위 profile은 사건에 따라 복수 조합할 수 있다.

삼각사기 profile에서는 비관련 카드였던 `contract_breach_distinction`을 제거했다.
계약 불이행이 실제 쟁점인 사건에서는 `contract_performance` profile이 이를 담당한다.

## 4. 두 번째 모델 호출이 판단하는 것

주석서에서 만든 전체 사기죄 NormCard는 88개다. 그러나 한 사건의 두 번째 호출이 88개 또는 과거
합집합 24개를 모두 판단하지 않는다.

1. Host가 FactGraph의 profile을 바탕으로 core와 profile을 조합한다.
2. 조합된 카드 중 `standard_input`만 두 번째 호출에 보낸다.
3. 모델은 카드별 별도 질문을 새로 받지 않는다. 검수된 `proposition` 자체를 사건 사실에 적용한다.
4. 모델은 지지 사실, 반박 사실, 누락 사실을 먼저 구분하고 `satisfied / not_satisfied / unknown`을 정한다.

현재 회귀 사례의 두 번째 호출 규모는 다음과 같다.

| 조합 | 전체 법리 카드 | 모델 평가 카드 |
|---|---:|---:|
| core만 적용하는 일반형 | 13 | 9 |
| core + 차용 목적 | 15 | 11 |
| core + 차용 변제 + 재산상 이익 | 17 | 12 |
| core + 묵시적 기망 + 재산상 이익 | 16 | 11 |
| core + 계약 이행 | 14 | 10 |
| core + 삼각사기 | 16 | 10 |

## 5. Scallop이 계산하는 것

`deterministic_rule`은 모델에게 상태 판정을 맡기지 않는다. 현재 Scallop은 다음 조건을 구조적으로
도출한다.

- 피기망자와 처분자가 같은 entity인지
- 피기망자·처분자와 재산 피해자가 다른 삼각사기 구조인지
- 기망, 착오와 처분이 연결되는지
- 구체적인 재산상 이익의 취득이 인정되는지
- 기망·착오·처분·취득의 순차적 인과관계가 완성되는지
- 재물 또는 이익 이전이 기수 단계에 이르렀는지

즉 neural 부분은 풍부한 사건평가를 만들고, symbolic 부분은 검수된 법적 결합관계를 강제한다.

## 6. Payload 정리

- `generation_instructions`는 모델 payload에서 제거했다. 사건 범위는 `question_prompt`와 `target`,
  자료 경계는 system prompt가 담당한다.
- `status_semantics`는 두 번째 호출 payload에서 제거했다. 상태 정의는 검수된 system prompt와
  JSON Schema에서 한 번만 관리한다.
- 과거 case JSON의 두 필드는 재현용 artifact에 남을 수 있지만 활성 호출에는 전달되지 않는다.
- 과거 `reasoning_plan_id`도 artifact 호환용으로 읽을 수 있으나, routing에는 사용하지 않는다.
  실제 plan ID는 core와 활성 profile에서 host가 합성한다.

## 7. IRAC에서의 분리

IRACPlan은 두 종류를 구별해 기록한다.

- `card_assessments`: 모델이 사건 사실에 적용한 standard 카드와 근거
- `deterministic_rules`: Scallop이 결합한 법리와 권위 자료

Rule 단락에는 두 종류의 법리를 모두 반영한다. Application 단락에서는 실제 모델 평가와 사건 사실을
적용하고, deterministic 규칙은 이미 계산된 구조를 설명하는 데 사용한다.

## 8. 검증 결과

- planning 일반화 테스트: 5건 통과
- neural end-to-end 테스트: 20건 통과
- IRAC matrix 테스트: 22건 통과
- 실제 `scli 0.2.4` runtime 테스트: 6건 통과
- Scallop 골든 시나리오: 9건 전부 예상 결과와 일치
- KCL 사기 사례 replay: 11개 standard 평가만 입력해 `fraud_established` 도출
- 저장소 전체 테스트: 116건 통과

골든 일반형은 과거처럼 14개 법적 판단을 직접 주입하지 않는다. 9개 standard 판단과 역할 정보만
입력하고, 동일성·인과관계·기수는 Scallop이 도출하도록 검증했다.

## 9. 남아 있는 호환 코드

전체 88-card RuleIR에는 과거 실행 결과 재현을 위한 deterministic 카드의 `assess_*` 입력 관계가
아직 남아 있다. 현재 M5 router와 두 번째 모델 호출은 이 관계를 선택하거나 입력하지 않으므로 활성
경로에서는 사용되지 않는다. 완전 제거는 전역 RuleIR의 기존 실험 artifact와 테스트를 함께 이관하는
별도 정리 작업이다.
