# M5 구조화 IRAC 생성 개선 보고서

> **후속 개편:** 이 문서는 3회 호출형 M5의 동결 기록이다. 이후 카드별 application 재작성
> 호출을 제거하고, `FactGraph → 카드 assessment` 2회 호출과 단일 전체 IRAC host compiler로
> 변경했다. 현재 구조는 `fraud_m5_neural_prompt_and_whole_irac.md`에 정리했다.

## 목적

최초 M5에서 발생한 카드 ID 오기, authority ID 오기 및 필수 카드 누락을 M6의 추가
ClaimGraph 호출 없이 제거할 수 있는지 확인했다. 최초 매트릭스의 M5와 M6 결과는 비교
기준으로 보존하고, 개선 M5만 독립 실행했다.

## 변경

기존 M5는 IRACPlan 전체를 제공한 뒤 모델에게 자유 본문과 provenance 배열을 함께
생성하게 했다. 개선 M5는 다음 경계를 사용한다.

```text
IRACPlan
  -> 카드별 application 슬롯을 고정한 동적 JSON Schema
  -> Gemma는 13개 카드의 사안 적용문만 생성
  -> 호스트가 검수된 proposition, provenance, 단락 소결을 삽입
  -> LongFormLegalAnswer
```

- 카드 ID는 동적 스키마의 필수 property이므로 누락하거나 바꿀 수 없다.
- 카드·사실·authority metadata는 모델 출력에서 받지 않고 IRACPlan에서 복사한다.
- 법리 문장은 모델이 다시 쓰지 않고 검수된 NormCard proposition을 사용한다.
- 단락 순서와 소결, 전체 결론은 호스트가 결정론적으로 조립한다.
- 생성 문장에 내부 ID나 JSON 필드명이 섞이면 컴파일을 거부한다.

## 실행 결과

최종 실행은 Slurm job `210098`, `COMPLETED (0:0)`이다. 모델과 Scallop 자산, 사건 입력은
최초 매트릭스와 같다.

| 방법 | 모델 호출 | Warm E2E | 답안 생성 | 정적 위반 | ClaimGraph |
|---|---:|---:|---:|---:|---|
| 최초 M5 | 3 | 47.250초 | 20.793초 | 4개 | 없음 |
| 개선 M5 | 3 | 32.905초 | 6.544초 | 0개 | 없음 |
| 최초 M6 | 6 | 124.561초 | 21.716초 | 최종 0개 | 2회 |

개선 M5는 최초 M5보다 14.344초, 약 30.4% 짧았고 M6보다 91.656초, 약 73.6% 짧았다.
답안 단계 prompt는 14,093토큰에서 5,402토큰으로 줄었다. 최종 답안은 13개 카드와 5개
단락을 모두 포함하며 기존에 빠졌던 `처분행위를 하게 할 의사`도 명시했다.

기존 정적 스키마는 서버 준비 단계에서 워밍업했지만, 개선 M5의 카드별 동적 스키마는
IRACPlan이 만들어진 뒤 생성되므로 사전 워밍업하지 않았다. 따라서 32.905초와 답안 생성
6.544초에는 동적 grammar의 최초 컴파일 비용도 포함된다. 기존 M5와 완전히 동일한 스키마
캐시 조건은 아니며, 개선 M5에 불리한 보수적 측정이다.

기계 기록은
[`fraud_m5_structured_report.json`](../../data/e2e/fraud/irac_matrix/fraud_m5_structured_report.json),
사람이 읽는 답안은
[`m5_irac_plan_answer.md`](../../data/e2e/fraud/irac_matrix/m5_irac_plan_answer.md)에 있다.

## 질적 검토

최종 답안은 객체·역할, 용도기망, 착오·처분, 인과관계·기수, 편취고의를 순서대로
검토한다. provenance ID는 본문에 노출되지 않았고, 모든 단락이 법리-적용-소결 구조를
갖춘다. 기존 M5의 ID 오기와 부정형 카드 누락은 재발하지 않았다.

개발 중간 실행 job `210097`에서는 자유 `synthesis_text`가 카드 적용을 반복하고 JSON 경계
문자열을 문장에 포함했다. 정적 위반 수만 보면 0개였지만 사람 검토에서 부적합하다고
판단했다. 해당 슬롯을 제거하고 내부 필드명 누출 검사를 추가한 뒤 job `210098`을 최종
결과로 채택했다.

## 해석과 한계

이번 결과는 최초 M5의 네 오류가 IRACPlan 법리 자체의 누락이 아니라, 계획을 자유생성
답안으로 옮기는 인터페이스의 문제였음을 뒷받침한다. 구조적으로 강제할 수 있는 coverage와
provenance는 추가 LLM verifier 없이 해결하는 편이 효율적이다.

그러나 `정적 위반 0개`는 자연어 의미가 항상 정확하다는 뜻이 아니다. 모델이 지정된 카드
슬롯 안에서 사실을 잘못 적용하거나 서로 모순되는 문장을 쓰는 오류는 여전히 가능하다.
ClaimGraph는 전수 런타임 단계보다 표본 평가 또는 불확실 사례의 fallback으로 두는 것이
현재 비용 구조에 적합하다.

또한 형법 제347조 제1항 명시, beneficiary attribution 전용 카드, 5단락 분류 정책은 이번
인터페이스 수정 범위가 아니다. 이는 IRACPlan 자체의 사람 검수와 후속 개정 대상으로 남는다.

## 아키텍처 결정

개선 M5를 IDPR의 기본 장문 생성 아키텍처로 확정한다.

```text
FactGraph -> NormCard assessment -> Scallop -> IRACPlan
          -> 필수 카드별 neural application -> host compile
```

M6의 ClaimGraph 재검증과 부분재생성은 모든 사건에서 실행하지 않는다. 사람 gold와의 정밀
평가, 새 프로파일, `unknown` 또는 상충이 많은 사건, 정적 검사를 통과했지만 의미 오류가
의심되는 사건에 한해 evaluator 또는 fallback으로 사용한다. 이 결정은 M5의 neural application이
완전하다는 뜻이 아니라, 고위험 불변조건은 M5의 스키마와 host compiler로 강제하고 남은 의미
오류는 표본평가로 측정하는 것이 현재 비용과 지연시간에 맞다는 뜻이다.

현재 구현은 이 아키텍처의 `loan_purpose` 단일 사건 proof다. 다른 사기 유형으로 확장하려면
사건별 카드계획과 IRAC 단위를 먼저 일반화해야 하며, 단순히 새 사건 원문을 기존 스크립트에
넣어서는 안 된다. 구체적인 확장 순서는
[`fraud_manual_case_inventory.md`](fraud_manual_case_inventory.md)에 정리한다.
