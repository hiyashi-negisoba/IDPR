# 사기죄 Paraphrase 5건 M5·M6 비교

작성일: 2026-07-19

> **후속 개편:** 이 문서의 수치와 답안은 3회 호출·구성요건별 IRAC을 사용한 동결 실험이다.
> 이후 M5를 2회 호출과 단일 전체 IRAC 구조로 개편했다. 새 구조와 host-only replay는
> `docs/research/fraud_m5_neural_prompt_and_whole_irac.md`를 참조한다. 새 프롬프트의 neural
> 효과는 아직 모델로 재실험하지 않았다.

## 실험 범위

수작업으로 중립화한 사기죄 사례 5건을 로컬 `Gemma-4-26B-A4B-it`에 태워 개선 M5와
M6을 비교했다. 외부 API는 사용하지 않았다. 각 방법은 FactGraph와 13~17개 카드평가부터
독립적으로 다시 실행했으며, 사람의 카드별 gold는 아직 제공하지 않았다. 따라서 아래 평가는
정량 성능 확정치가 아니라 실제 출력의 탐색적 비교다.

warm latency는 모델 서버 시작과 정적 schema warmup을 제외하고 사건 입력부터 최종 답안까지의
시간이다. Scallop, IRACPlan 컴파일, M6 ClaimGraph와 repair는 포함한다.

## 답안 원문

| 사건 | M5 | M6 |
|---|---|---|
| 1. 차용 당시 변제 의사·능력 | [M5 답안](manual_fraud_046_01_loan_repayment/m5_irac_plan_answer.md) | [M6 답안](manual_fraud_046_01_loan_repayment/m6_claim_verified_answer.md) |
| 2. 변제기 연장 | [M5 답안](manual_fraud_047_01_loan_extension/m5_irac_plan_answer.md) | [M6 답안](manual_fraud_047_01_loan_extension/m6_claim_verified_answer.md) |
| 3. 무전취식 | [M5 답안](manual_fraud_050_01_unpaid_dining/m5_irac_plan_answer.md) | [M6 답안](manual_fraud_050_01_unpaid_dining/m6_claim_verified_answer.md) |
| 4. 전선 공급계약금 | [M5 답안](manual_fraud_052_01_supply_deposit/m5_irac_plan_answer.md) | [M6 답안](manual_fraud_052_01_supply_deposit/m6_claim_verified_answer.md) |
| 5. 택배물 삼각사기 | [M5 답안](manual_fraud_063_01_parcel_triangular/m5_irac_plan_answer.md) | [M6 답안](manual_fraud_063_01_parcel_triangular/m6_claim_verified_answer.md) |

Markdown은 사람 검토용으로 내부 `fact_`, `comm_`, 카드 ID를 숨겼다. 원본 답안 JSON과 각
사건의 `report.json`에는 provenance가 보존돼 있다.

## 정량 결과

| 사건 | M5 결론 | M5 초 | M5 상태 | M6 결론 | M6 초 | M6 위반 전→후 |
|---|---|---:|---|---|---:|---:|
| 1. 차용금 | undetermined | 31.386 | completed | undetermined | 132.183 | 9→22 |
| 2. 변제기 연장 | undetermined | 35.959 | completed | undetermined | 129.564 | 12→2 |
| 3. 무전취식 | undetermined | 30.629 | completed | undetermined | 109.852 | 9→9 |
| 4. 공급계약금 | undetermined | 32.420 | completed | undetermined | 119.297 | 10→4 |
| 5. 삼각사기 | undetermined | 36.429 | completed | undetermined | 110.173 | 5→3 |

| 집계 | M5 | M6 |
|---|---:|---:|
| 평균 warm latency | 33.365초 | 120.214초 |
| 중앙값 | 32.420초 | 119.297초 |
| 사건당 모델 호출 | 3회 | 6회 |
| 5건 모델 호출 | 15회 | 30회 |
| 총 prompt+completion tokens | 72,172 | 320,343 |
| 평균 Scallop latency | 4.417초 | 4.403초 |
| 최종 답안 계약 위반 | 0 | 1 |
| M6 ClaimGraph 잔여 위반 | 해당 없음 | 40 |

M6는 M5보다 평균 3.60배 느리고, 모델 token은 4.44배 사용했다. Scallop 시간은 사실상
동일하므로 차이는 ClaimGraph 추출, 부분 repair, 재추출 모델 호출에서 발생했다. M6은 5건
모두 repair를 실행했지만 어느 사건도 ClaimGraph 잔여 위반 0개가 되지 않았다. 무전취식의
최종 답안 계약 위반 1건은 ClaimGraph 잔여 위반 9건에도 포함된 동일한 필수 카드 누락이므로
두 수치를 합산하지 않는다.

두 방법은 각 사건에서 독립적으로 FactGraph와 카드평가를 생성했음에도 카드 상태 개수가 모두
같았다. 사건별 `satisfied / not_satisfied / unknown`은 각각 `5/0/8`, `6/0/8`, `5/0/9`,
`10/0/4`, `10/0/7`이었고, Scallop은 전부 `undetermined`를 출력했다.

## 사건별 한줄평

### 1. 차용 당시 변제 의사·능력

- **M5:** 경제사정만으로 변제 의사와 편취 범의를 단정하지 않아 `unknown`을 안정적으로
  보존했지만, 돈을 빌려달라고 한 사실이 있는데 처분 유도 의사까지 미확인으로 둔 것은 다소
  과도하게 보수적이다.
- **M6:** 문장은 M5보다 약간 간결하지만 결론과 법리 적용은 개선되지 않았고, repair 후
  ClaimGraph가 임의 ID를 생성해 위반이 9개에서 22개로 오히려 늘었다.

### 2. 변제기 연장

- **M5:** 변제기 연장을 구체적 재산상 이익으로 포착하고 불확실한 범의를 보존한 점은 좋지만,
  일부 application이 세미콜론으로 시작하고 “금원 차용” 카드 `C2-04`를 연장행위에 그대로
  적용한 법리 범위 문제는 사람 검수가 필요하다.
- **M6:** 가시 문장은 더 정돈됐으나 같은 `undetermined`이고 잔여 위반 2개가 남아, 추가
  호출 비용을 정당화할 정도의 개선은 아니다.

### 3. 무전취식

- **M5:** 결제수단이 없었고 주문·취식 후 지급하지 않은 사실까지 있는데도 묵시적 기망과
  행위시 의사를 전부 미확인으로 둬, 사실에서 합리적인 추론을 하는 neural standard가 지나치게
  약하게 작동했다.
- **M6:** 같은 과소추론을 반복했고 repair 후에도 위반 9개가 그대로라 M5 대비 실질적 이득이
  없다. 음식·주류를 재물과 서비스 이익 중 어떻게 분류할지도 사람 검수 대상이다.

### 4. 전선 공급계약금

- **M5:** “미생산 상태”와 “이미 생산 중이라는 말”을 정확히 추출해 기망·착오·계약금 교부의
  객관적 연쇄를 모두 충족시켰고, 제거된 내심사실 때문에 편취 범의만 미확인으로 둔 5건 중
  가장 설득력 있는 출력이다.
- **M6:** 가시 답안은 가장 매끄럽지만 결론은 M5와 같고 잔여 위반 4개가 있어, 약 3.68배
  latency를 감수할 만큼의 내용 개선은 확인되지 않았다.

### 5. 택배물 삼각사기

- **M5:** 삼각사기의 역할 분리는 대부분 포착했지만 “B가 A의 직원이라는 말”을 한 단락에서
  “A가 B의 직원이라는 인식”으로 뒤집었고, 원문이 “그 말을 듣고 건넸다”고 명시했는데도
  인과관계를 미확인으로 둔 명백한 neural application 오류가 있다.
- **M6:** 같은 역할 전도와 과도한 `unknown`을 반복했다. 첫 시도에서는 ClaimGraph를 57개
  이상으로 과잉 분할해 token limit에 걸렸고, 15개로 제한한 재실행에서도 위반 3개가 남았다.

## 종합 판단

이번 5건에서는 **M5를 기본 아키텍처로 유지하는 판단이 강화됐다.** M5는 모든 사례에서
카드·사실·소결의 구조적 계약을 통과했고 M6보다 훨씬 빠르며, M6이 실체법 결론이나 가시 답안의
법적 정확성을 일관되게 개선하지 못했다.

다만 M5의 정적 위반 0개는 neural 적용이 정확하다는 뜻이 아니다. 무전취식의 과소추론,
삼각사기의 역할 전도, 명시된 인과관계의 누락처럼 schema가 잡지 못하는 오류가 확인됐다.
카드별 사람 gold와 역할·인과관계의 사실 gold를 함께 두어야 실제 성능을 측정할 수 있다.

M6은 현재 기본 생성 경로가 아니라 연구용 evaluator 후보로만 남기는 편이 타당하다. 사용하려면
다음 문제가 먼저 해결돼야 한다.

1. `unknown` 단락의 application support를 ClaimGraph가 표현하는 계약
2. repair 뒤 임의 provenance ID와 inexact quote 방지
3. 한 번의 repair가 위반을 늘리면 원문을 보존하는 rollback 정책
4. 역할 전도와 명시적 인과관계 누락을 검출하는 사실 수준 verifier

## 실행 중 발견·수정한 배선 결함

- 전부 `unknown`인 IRAC 단위가 빈 `required_fact_ids`를 허용하지 않던 문제를 수정했다.
- M6 patch의 중복 provenance ID를 host가 순서 보존 정규화하도록 수정했다.
- ClaimGraph를 단락당 3개, 총 15개 claim으로 제한해 과잉 추출을 막았다.
- Slurm 사례 목록은 쉼표 대신 콜론 구분자로 전달하도록 수정했다.
- 사람용 Markdown에서 내부 provenance 표식만 제거하고 원본 JSON은 보존했다.

최종 산출물은 job `210102`의 1번, job `210105`의 2~4번, job `210106`의 5번 결과다.
`210105`는 2~4번 보고서를 정상 게시한 뒤 5번의 과잉 ClaimGraph에서 종료됐고, 5번은 수정 후
`210106`에서 별도로 완결했다.

## 최종 검증

- 전체 회귀 테스트: `112 passed`
- 패러프레이즈 원문 hash 및 provenance: 5/5 통과
- 사람용 답안: 5건 × 2방법 = 10개, 내부 fact·card·commentary ID 노출 0건
- 기계 답안: 10개, 사건별 실행 보고서: 5개
- 집계 JSON과 5개 원시 보고서의 latency·호출 수·token 합계 대조: 일치
- `compileall`, Slurm shell 문법, `git diff --check`: 통과
- 외부 API 호출: 0회
