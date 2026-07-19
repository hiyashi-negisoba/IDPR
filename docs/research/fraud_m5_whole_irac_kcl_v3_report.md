# M5 전체 IRAC KCL 재실험 보고서

작성일: 2026-07-19

## 1. 목적

관계 판단, `unknown`, 내부 메타데이터 비노출 규칙을 반영한 현재 M5를 기존 KCL
사기죄 문항에 다시 적용했다. 외부 API는 사용하지 않았고, Slurm에서 로컬
`google/gemma-4-26B-A4B-it`를 vLLM으로 실행했다.

입력 문항은 乙이 형사처벌을 피하기 위한 금품 자금을 마련하려고 B에게 딸의 수술비인
것처럼 말해 3천만 원을 빌린 사안이다. 평가 범위는 乙의 B에 대한 사기죄로 제한했다.

## 2. 실제 M5 경로

M5의 모델 호출은 두 번이다.

1. 사건 본문을 FactGraph로 구조화한다.
2. host가 선택한 13개 NormCard를 사건 사실에 적용한다.

카드 검색·선택 자체는 모델이 하지 않는다. 사건 계약의 `reasoning_plan_id=loan_purpose`에
따라 host가 검수된 13개 카드 계획을 확정하고, 두 번째 호출의 모델은 그 카드들을 평가한다.
이후 Scallop이 구성요건 게이트와 최종 결론을 계산하고, host가 하나의 전체 IRAC을 작성한다.
추가 장문작성 모델 호출은 없다.

현재 활성 system prompt 전문과 사건별 payload 구조는
`docs/research/fraud_m5_prompt_full_review.md`에 있다.

## 3. 시행착오와 수정

첫 실행 job `210278`에서 모델은 부정형 카드
`fraud_intent.no_disposition_inducement_intent`를 `not_satisfied`로 판단하면서도 그 명제를
반증하는 사실을 `counter_fact_ids`에 넣지 않아 계약 검증에서 중단됐다.

법적 판단을 host가 임의 보정하지 않았다. assessment prompt에 부정형 명제를 깨는 적극적
사실은 `basis_fact_ids`가 아니라 `counter_fact_ids`에 넣고, 출력 전에 모든
`not_satisfied` 항목을 자체 점검하라는 규칙을 추가했다. 재실행 job `210285`에서는 해당
카드에 기망 발언과 대여 사실 두 개를 counter fact로 정확히 배치해 검증을 통과했다.
실패 시에도 원시 출력을 확인할 수 있도록 `assessment_model_output.json`을 validation 전에
보존하도록 runner도 수정했다.

## 4. 실행 결과

| 항목 | 결과 |
|---|---:|
| 상태 | completed |
| 최종 결론 | 사기죄 성립 |
| 모델 호출 | 2회 |
| prompt tokens | 7,645 |
| completion tokens | 2,918 |
| FactGraph 호출 | 6.695초 |
| 카드 assessment 호출 | 15.057초 |
| Scallop | 4.474초 |
| IRACPlan + 답안 host compile | 0.006초 미만 |
| warm E2E | 26.262초 |
| 답안 계약 위반 | 0건 |

Scallop의 규칙 계산 자체보다 매 실행의 native CLI 시작 비용이 포함되어 4.47초가 걸렸다.
IRAC 계획과 최종 문장 조립은 사실상 무시할 수 있는 수준이고, 전체 병목은 두 모델 호출이다.

## 5. 질적 검토

최종 답안은 하나의 `Issue - Rule - Application - Conclusion` 구조를 유지하고,
Application 내부에서 객체·역할, 용도 기망, 착오·처분, 인과관계·기수, 고의·이득 목적을
차례로 검토했다. 용도를 속인 발언, B의 3천만 원 대여, 실제 뇌물 자금 목적을 연결하여
사기죄 성립 결론을 낸 흐름은 문항의 핵심 쟁점에 부합한다.

다음 두 항목은 중간 FactGraph의 질적 한계다.

- 수술비 명목이라고 말한 사실을 `representation`이 아니라 `mistake`로 분류했다.
- 丙의 2천만 원 소비와 乙의 기망 사이 관계를 불필요한 `unresolved_questions`로 남겼다.

두 항목은 statement 원문과 target role에는 영향을 주지 않아 카드 판정과 최종 답변을
오염시키지 않았다. 그러나 fact-kind 정확도와 target 쟁점에 직접 필요하지 않은 미확인
질문의 억제는 다수 사례 gold annotation에서 별도로 측정해야 한다.

카드 assessment는 13개 전부 확정 판단이며 confidence도 모두 1.0이다. 특히 “진정한 용도를
알았다면 B가 빌려주지 않았을 관계”와 행위시 편취 범의를 사실에서 좁게 추론했다. 이 사안에서는
설득력 있지만, 일률적인 과신인지 확인하려면 반대사실이 있거나 진정한 용도의 중요성이
불명확한 사례가 필요하다. 이 문항에서는 `unknown`이 발생하지 않았다.

## 6. 비노출 검사

최종 Markdown에서 다음 문자열은 모두 0건이었다.

- `unresolved_questions`, `assessment_context`
- `basis_fact_ids`, `counter_fact_ids`, `missing_facts`
- `authority_comment_ids`
- `fact_*`, `comm_*`

선행 세미콜론·콜론·쉼표도 없었다. 미확인 사실은 내부 추론과 향후 수사상 보완점으로는
활용하되, 내부 필드명이나 처리 단계가 답안에 그대로 노출되지 않는 경계가 작동했다.

## 7. 산출물

- 사람용 최종 답안:
  `data/e2e/fraud/experiments/m5_whole_irac_kcl_v3/m5_irac_plan_answer.md`
- 기계 실행 보고서:
  `data/e2e/fraud/experiments/m5_whole_irac_kcl_v3/report.json`
- 검증 FactGraph와 assessment:
  `.cache/e2e/fraud_irac_matrix/kcl_m5_whole_irac_v3/m5_irac_plan/`

한줄평: 현재 M5는 이 KCL 용도기망 사안에서 두 번의 neural 호출만으로 핵심 법리와 사실을
일관된 전체 IRAC으로 연결했지만, FactGraph label과 confidence calibration은 별도 평가가
필요하다.

## 8. 회귀 검증

- 전체 테스트: `116 passed`
- 수동 paraphrase provenance: 5/5 일치
- Python compileall: 통과
- Slurm shell 문법: 통과
- `git diff --check`: 통과
