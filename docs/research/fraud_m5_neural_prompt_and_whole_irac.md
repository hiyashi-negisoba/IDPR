# M5 Neural Prompt 및 전체 IRAC 개편

작성일: 2026-07-19

> 두 활성 프롬프트의 **전문과 runtime payload 구조**는
> [`fraud_m5_prompt_full_review.md`](fraud_m5_prompt_full_review.md)에 별도로 정리했다.

## 결론

M5의 활성 모델 호출을 3회에서 2회로 줄였다. IRACPlan의 다섯 unit은 독립된 IRAC 단락이
아니라 구성요건 누락을 막는 내부 coverage ledger로 유지한다. 최종 답안은 사기죄 성부 전체를
하나의 IRAC으로 조립하고, Application 안에서 unit별 검토를 수행한다.

이번 변경에는 외부 API와 로컬 모델을 사용하지 않았다. 과거 5건의 검증된 IRACPlan을 새
host compiler에 재생해 구조만 확인했다. 따라서 아래 변경이 neural 정확도를 실제로 높였다는
주장은 아직 하지 않는다.

## 활성 호출

### 1. FactGraph 추출

- 프롬프트: [`prompts/fraud_fact_graph_extract.md`](../../prompts/fraud_fact_graph_extract.md)
- 입력: 사건 본문, 질문, 대상 거래, 역할 힌트, 허용·필수 프로파일
- 출력: 인물·역할, 원자적 사실, 원문 인용, epistemic status, profile, 미확인 사실
- 모델의 책임: 사건 본문을 추가 법률지식 없이 구조화

프롬프트에 다음 경계를 추가했다.

1. 인물관계의 주체·객체·소유·지위 귀속을 원문 문법과 맥락에 따라 신중하게 판정한다.
2. `그 말을 듣고`, `이에 따라` 같은 명시적 인과 연결을 statement에 보존한다.
3. `unresolved_questions`는 빠진 사실의 추출 메모일 뿐이고, 이미 명시된 인과·역할관계를
   다시 미확인으로 만들 수 없다.

### 2. 카드별 assessment

- 프롬프트: [`prompts/fraud_standard_assess.md`](../../prompts/fraud_standard_assess.md)
- 입력: FactGraph, host가 선택한 NormCard와 출처, 카드별 assessment context
- 출력: 카드별 `satisfied / not_satisfied / unknown`, 근거·반대 fact, missing facts,
  rationale
- 모델의 책임: 사건 사실이 카드의 법리 기준을 충족하는지 판정

기존 입력은 카드의 추상적 proposition만 제공했다. 이 때문에 “편취의 범의는 행위 당시를
기준으로 판단한다”처럼 법리인 문장을 사건에서 참인지 평가하는 혼동이 발생했다. 이제 각
카드에는 다음 번역 정보를 함께 제공한다.

```json
{
  "card_id": "...",
  "unit_id": "irac_intent",
  "unit_issue": "편취의 범의와 재산적 이득 목적",
  "adjudication_question": "A에게 행위 당시 편취 범의와 처분 유도 의사가 있었는가?",
  "unit_satisfied_status": "satisfied"
}
```

즉 모델은 법리 문장 자체의 참·거짓이 아니라 `adjudication_question`에 따라 그 법리를
사건 사실로 번역한다. 부정형 카드에는 `unit_satisfied_status=not_satisfied`가 들어가므로
극성도 명확해진다.

평가 프롬프트에는 다음 규칙도 추가했다.

1. `unresolved_questions`를 증거나 `unknown` 지시로 사용하지 않는다.
2. 복수의 합리적 해석이 남으면 `unknown`을 유지하고, 강하게 뒷받침되는 좁은 추론만 한다.
3. 피고인이 처분을 요청하고 상대방이 그 요청에 따라 처분했다면 처분 유도 의사의 근거로
   평가한다.
4. 동일 사실연쇄의 카드 상태가 다르면 그 법적 범위와 빠진 사실을 설명한다.
5. rationale에서 관계를 신중히 확인하고, 세미콜론·콜론·쉼표나 내부 필드명으로 시작하지
   않는다.
6. `unknown`의 `missing_facts`는 향후 확인해야 할 사실·증거 목록으로 작성한다.

## 제거한 호출

기존 세 번째 호출은 IRACPlan의 카드별 `application_bridge`, 즉 assessment rationale을 다시
자연어로 고쳐 쓰는 작업이었다. 5건의 실제 산출물에서는 대부분 rationale을 그대로 복사했고,
삼각사기 역할 전도와 문장 형식 오류를 새로 만들기도 했다.

IRACPlan이 법리, 카드 상태, fact provenance, unit 결론과 Scallop 최종 결론을 이미 고정하므로
이 호출의 정보 이득이 없다. 현재 M5는 assessment rationale을 host에서 문장 형식만 정규화해
직접 사용한다. 선행 세미콜론·콜론·쉼표·하이픈을 제거하고, 공백과 종결부호를 결정론적으로
정리한다.

## 전체 IRAC

최종 출력은 다음 네 구획만 가진다.

1. **Issue:** 대상 사기죄의 전체 성립 여부
2. **Rule:** 선택된 모든 카드의 법리를 구성요건 순서로 정리
3. **Application:** 객체·역할, 기망, 착오·처분, 인과·기수, 주관적 요건을 하위 항목으로 적용
4. **Conclusion:** Scallop의 전체 결론을 한 번만 제시

Application의 하위 항목에는 unit별 소결이 남지만, 각 unit을 별도의 IRAC으로 취급하지 않는다.
Rule도 각 단락마다 반복하지 않는다. 최종 Markdown에서는 기존의 별도 `종합 결론`을 다시
붙이지 않아 결론 중복을 막는다.

## 5건 Host Replay

저장된 기존 IRACPlan을 모델 호출 없이 새 compiler에 통과시킨 결과다. 신경망 출력을 다시
만든 것이 아니므로 기존의 의미 오류를 그대로 포함한다.

| 사건 | 전체 IRAC 답안 |
|---|---|
| 차용 당시 변제 의사·능력 | [보기](../../data/e2e/fraud/manual_paraphrases/experiments/m5_whole_irac_host_replay/manual_fraud_046_01_loan_repayment/m5_whole_irac_answer.md) |
| 변제기 연장 | [보기](../../data/e2e/fraud/manual_paraphrases/experiments/m5_whole_irac_host_replay/manual_fraud_047_01_loan_extension/m5_whole_irac_answer.md) |
| 무전취식 | [보기](../../data/e2e/fraud/manual_paraphrases/experiments/m5_whole_irac_host_replay/manual_fraud_050_01_unpaid_dining/m5_whole_irac_answer.md) |
| 전선 공급계약금 | [보기](../../data/e2e/fraud/manual_paraphrases/experiments/m5_whole_irac_host_replay/manual_fraud_052_01_supply_deposit/m5_whole_irac_answer.md) |
| 택배물 삼각사기 | [보기](../../data/e2e/fraud/manual_paraphrases/experiments/m5_whole_irac_host_replay/manual_fraud_063_01_parcel_triangular/m5_whole_irac_answer.md) |

## 검증할 가설

다음 실제 5건 재실행에서는 구버전 M5와 새 M5를 비교해야 한다.

1. 무전취식에서 묵시적 기망, 순차적 인과관계, 처분 유도 의사의 과도한 `unknown`이 감소하는가
2. 삼각사기에서 관계 방향이 보존되고 명시적 인과관계가 `satisfied`로 일관되게 평가되는가
3. 직접 진술이 없는 주관적 요건에서 객관적 사실에 근거한 추론과 보수적 `unknown`의 균형이
   개선되는가
4. M5 모델 호출이 사건당 2회로 기록되고 latency와 token 사용이 줄어드는가
5. 전체 IRAC이 KCL 장문답안의 가독성과 논리적 일관성을 개선하는가

사람의 카드별 gold가 없으므로 상태 정확도는 여전히 확정할 수 없다. 다음 실행 전 최소한
무전취식과 삼각사기의 카드 상태·역할·인과관계 gold를 먼저 고정하는 편이 안전하다.

## 정적 검증

- 전체 회귀 테스트: `115 passed`
- 5개 기존 IRACPlan의 host-only 전체 IRAC compile: 5/5 통과
- 각 답안의 I/R/A/C 네 구획 및 단일 결론: 5/5 통과
- 선행 세미콜론·전각 세미콜론: 0건
- 패러프레이즈 원문 hash 및 provenance: 5/5 통과
- `compileall`, Slurm shell 문법, JSON 구문, `git diff --check`: 통과
- 외부 API 호출: 0회
- 로컬 모델 호출: 0회

M6은 과거 비교를 위한 연구용 경로로 보존되어 있으며 아직 새 전체 IRAC 계약으로 이관하지
않았다. 다시 사용할 경우 ClaimGraph의 단락 단위와 repair 계약을 네 구획 구조에 맞춰 별도로
개편해야 한다.
