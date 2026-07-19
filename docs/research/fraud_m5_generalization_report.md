# 사기죄 M5 다중 사례 일반화 및 매뉴얼 Paraphrase 보고

작성일: 2026-07-19

> **후속 개편:** 이 문서의 일반화 계약은 유지하되, 현재 M5 출력은 unit별 독립 IRAC이
> 아니라 단일 전체 IRAC이다. 카드 적용문 재작성 모델 호출도 제거해 활성 호출은 FactGraph와
> 카드 assessment 2회다. 상세 내용은 `fraud_m5_neural_prompt_and_whole_irac.md`에 있다.

## 결론

개선 M5의 사건 입력, 프로파일 routing, 카드계획, IRACPlan 컴파일을 데이터 기반 구조로
일반화했다. 기존 KCL 용도기망 사례의 동작을 유지하면서, 매뉴얼에서 만든 5개 중립
paraphrase를 같은 코드 경로에 연결했다. 이 작업에서는 외부 API와 로컬 LLM을 모두 호출하지
않았다.

이번 일반화의 범위는 **사기죄 안의 복수 사실유형**이다. KCL 형사법 61문항 전체로 확장할 때
러너와 M5 단계 계약은 재사용할 수 있지만, 죄명별 NormCard·RuleIR·reasoning-plan registry는
별도로 검수해 추가해야 한다.

## 일반화 구조

과거 구현은 `loan_purpose` 카드 13장, 당사자 乙·B, 수술비 차용 문구와 5개 IRAC 단위가
코드에 고정돼 있었다. 현재 사건은 다음 계약만 제공한다.

- 적용 가능한 프로파일과 반드시 활성화할 프로파일
- 검수된 `reasoning_plan_id`
- 피고인·피기망자·처분자·재산소유자·수익자 역할 힌트
- 대상 거래, 답안 제목, 생성 제한
- 원자료 식별자와 provenance

호스트는 사건 계약과 FactGraph를 검증한 뒤 registry에서 계획을 선택한다. 계획은 카드 순서,
카드별 기대 방향, 5개 IRAC 단위, 질문·쟁점·RAG query template을 가진다. 따라서 neural
stage가 임의로 법리 범위를 넓힐 수 없고, 같은 역할을 맡는 사람은 동일 entity로 고정된다.

| Plan | 활성 프로파일 | 카드 | 용도 |
|---|---|---:|---|
| `loan_purpose` | 용도기망 | 13 | 기존 KCL 회귀 기준 |
| `loan_repayment_property` | 변제의사·능력 | 13 | 전형적 차용금 교부 |
| `loan_extension_benefit` | 변제의사·능력 + 재산상 이익 | 14 | 변제기 연장 |
| `implicit_service_benefit` | 묵시적 기망 + 재산상 이익 | 14 | 무전취식 |
| `ordinary_contract_property` | 계약이행 | 14 | 공급계약금 |
| `triangular_property_delivery` | 삼각사기 | 17 | 제3자 재물 교부 |

모든 계획은 동일한 객체, 기망, 착오·처분·취득·인과, 주관적 요건의 5단 IRAC 구조를 사용한다.
특수 프로파일은 항상 켜지는 규칙이 아니라 사건 router가 명시적으로 선택할 때만 공통 core에
추가된다.

## M5 실행 경로

일반화된 한 사건의 실행 순서는 다음과 같다.

1. 사건 JSON을 `fraud_case.schema.json`으로 검증한다.
2. 모델 FactGraph의 역할과 프로파일을 사건 계약에 맞춰 검증한다.
3. host가 `reasoning_plan_id`에 해당하는 카드만 선택한다.
4. 모델은 선택된 카드의 `satisfied | not_satisfied | unknown`과 근거 사실을 평가한다.
5. 검증된 평가만 Scallop fact가 되어 법률결론을 계산한다.
6. host가 registry에서 IRACPlan과 동적 slot schema를 컴파일한다.
7. 모델은 카드별 application slot만 작성하고, host가 검수 법리·인용·소결·최종결론을 조립한다.

이번 작업에서는 2번과 4번의 실제 모델 호출을 하지 않았다. 테스트는 합성 FactGraph와
registry 기대 상태로 3~7번의 배선 및 Scallop 실행 가능성을 검증한 것이다. 따라서 통과 결과는
neural 추출·판단 정확도를 뜻하지 않는다.

## 매뉴얼 Paraphrase 5건

검수 완료 매뉴얼 인덱스에서 다음 작성례를 수작업으로 중립화했다.

| 사건 | 원자료 | 제거한 결론성 정보 | 계획 |
|---|---|---|---|
| 차용금 | leaf 046, case 1 | 변제 의사·능력 부재 단정, 기망·편취 | `loan_repayment_property` |
| 변제기 연장 | leaf 047, case 1 | 변제 불능·재산상 이익 결론 | `loan_extension_benefit` |
| 무전취식 | leaf 050, case 1 | 기망·이익 취득 결론 | `implicit_service_benefit` |
| 공급계약금 | leaf 052, case 1 | 선적 의사·능력 부재 단정, 편취 | `ordinary_contract_property` |
| 택배물 교부 | leaf 063, case 1 | 전달 의사 부재 단정, 기망 | `triangular_property_delivery` |

금액, 당사자, 행위 순서와 객관적 사정은 유지했다. 원문 전문은 저장하지 않았고 각 사례에
`manual_id`, `leaf_id`, 순번, 물리면, 원문 segment 문자 수와 SHA-256을 기록했다. 검증기가
실제 인덱스를 다시 읽어 5개 hash를 모두 대조한다.

이 5건은 독립 gold가 아니라 challenge input이다. 특히 차용금과 공급계약금은 결론성 내심
문구를 제거했으므로 실제 모델이 `unknown`을 남기는 것이 타당할 수 있다. 이후 평가는 사람이
카드별 gold를 붙인 뒤 false positive와 누락을 함께 측정해야 한다.

## 실행과 검증

사례 집합에서 하나를 선택해 기존 러너를 사용할 수 있다.

```bash
python scripts/run_fraud_irac_matrix.py \
  --case-path data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.json \
  --case-id manual_fraud_063_01_parcel_triangular \
  --methods m5_irac_plan \
  --base-url <local-vllm-url> --model <served-model> \
  --run-dir <run-dir> --report-path <report-path>
```

SLURM에서는 `IDPR_CASE_PATH`, `IDPR_CASE_ID`, `IDPR_METHODS`로 같은 선택을 전달한다. 이번
작업에서는 위 모델 실행 명령을 호출하지 않았다.

수행한 검증은 다음과 같다.

- 패러프레이즈 원문 provenance: 5/5 문자 수와 SHA-256 일치
- 사건·registry·FactGraph·assessment·IRACPlan schema/host 검증: 통과
- 5개 계획의 합성 Scallop runtime: 5/5 `fraud_established` 도달, 충돌·불성립 출력 없음
- 기존 KCL M5 회귀 포함 전체 테스트: `108 passed`
- `compileall`: 통과
- `git diff --check`: 통과
- Ruff: 환경에 설치되어 있지 않아 미실행

## 산출물

- 사건 계약: `docs/contracts/fraud_case.schema.json`
- 계획 계약: `docs/contracts/fraud_reasoning_plan_registry.schema.json`
- 계획 registry: `data/rulegen/fraud/fraud_m5_reasoning_plan_registry.json`
- host planning 모듈: `src/idpr/fraud_planning.py`
- 일반화 러너: `scripts/run_fraud_irac_matrix.py`
- 패러프레이즈 기계 자료: `data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.json`
- 패러프레이즈 사람용 자료: `data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.md`
- provenance 검증기: `scripts/validate_fraud_manual_paraphrases.py`
- 일반화·Scallop 테스트: `tests/test_fraud_planning_generalization.py`

## 남은 실험

다음 단계는 코드 일반화가 아니라 neural 품질 평가다. 사람은 5개 사건의 카드별 상태와 허용
결론을 먼저 정하고, 그 뒤 명시적으로 승인한 로컬 모델 실험에서 FactGraph, 카드평가, Scallop
결론, 최종 M5 답안을 비교해야 한다. 소송사기와 제347조의2 혼합 사례는 현재 registry에 넣지
않았으며 별도 법률 검수 전에는 실행 대상으로 취급하지 않는다.
