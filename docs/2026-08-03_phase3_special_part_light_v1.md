# Phase 3 각칙 경량판 v1 구현 기록

## 분기와 목적

- 브랜치: `experiment/phase3-special-part-light-20260803`
- 기준 커밋: V2 answer-visibility `4d48b2e`
- 장기 통합 파이프라인은 기존 브랜치에서 계속 보존한다.
- 이 분기는 형법 각칙의 조문별 구성요건 Coverage와 논리 일관성을 우선하는 실험판이다.

기존 V5를 축약하지 않고 V2에서 새로 갈라졌다. V5의 미수·공범·죄수·기본범 관계 및
가시성 예외는 이식하지 않는다.

## 실행 경로

```text
V2 FactGraph + broad L0 후보
  → grounded special-part planner
  → 선택된 조문의 초기 구성요건 issue만 평가
  → 같은 조문의 상태만으로 host 결론 계산
  → 선택 조문 전부를 독립 section으로 작성
```

planner는 먼저 설문을 `article_local` 또는 `direct_legal_analysis`로 라우팅한다. 절차법의
배경 사실에 범죄행위가 있어도 각칙 조문을 선택하지 않으며, 반대로 불성립·인과관계 불명은
논해야 할 각칙 쟁점이므로 버리지 않는다. 후보 catalog 밖의 조문을 출력할 수 없고, 선택마다
행위자·원문 exact quote·직접 관련 이유를 요구한다. 미수 처벌조항 자동 확장은 비활성화한다. Call 2의 unknown detail
재검색은 유지하지만 Scallop, stage/participation/concurrence followup, prerequisite 및 section
visibility는 실행하지 않는다.

조문 결론은 다음과 같이 결정한다.

- 어느 구성요건이든 `not_satisfied`: 불성립
- 모든 구성요건이 `satisfied`: 성립
- 그 밖에 `unknown` 포함: 판단 유보

답안 모델은 결론·조문명·issue명·provenance ID를 작성하지 않는다. 호스트가 계획과 판정에
따라 이를 다시 붙이고 검증한다.

## 총칙·절차법 진단

경량화가 범위 밖 문항에도 주는 영향을 보기 위해 전체 문항은 결과 파일에 남긴다. planner가
`direct_legal_analysis`로 라우팅한 문항은 `light_direct_out_of_scope_diagnostic` 경로로 같은
Gemma backbone이 짧은 직접 답안을 만든다. 이 경로는 IDPR 각칙 성능으로 주장하지 않는다.

최종 보고는 반드시 다음 세 묶음으로 나눈다.

1. 각칙 article-local 주평가
2. 총칙·절차법 direct 진단
3. 두 경로를 합친 전체 평균

즉, 총칙·절차법 결과도 관찰하지만 직접 경로의 개선을 각칙 rulebase의 성과로 섞지 않는다.

## 재현 실행

스모크는 절차법 1문항과 실체법 1문항을 함께 실행한다. 최초 진단 실행 `218683`은 절차법의
배경 절도행위를 각칙으로 잘못 선택하고, 인과관계가 불명인 실체법 조문은 누락했다. 이 결과를
성능 결과로 사용하지 않고 위 route 계약을 v1.1로 보강했다.

```bash
sbatch scripts/slurm/run_special_part_light.sh
```

스모크 검증 후 전체 59문항 실행은 동일 스크립트와 환경에서 다음처럼 제출한다.

```bash
IDPR_FULL=1 sbatch scripts/slurm/run_special_part_light.sh
```

입력 FactGraph와 broad L0 후보는 V2가 이미 생성한 봉인 산출물을 재사용한다. 생성 모델은
V2와 동일한 로컬 `google/gemma-4-26B-A4B-it` snapshot과 `inv_ass_env`를 사용하며, 로컬
워크스테이션에서 모델을 실행하지 않는다.

## 검증 기준

- 기존 V2 경로 테스트가 그대로 통과할 것
- planner 선택이 broad 후보의 부분집합일 것
- exact quote가 원문에 존재할 것
- attempt expansion이 다시 생기지 않을 것
- 경량 Call 2가 Scallop binary 없이 실행될 것
- planner 선택 article 수와 답안 section 수가 같을 것
- section 및 overall 결론이 host 판정과 같을 것
- direct 진단과 article-local 결과의 route가 산출물에 구분될 것

Gemini judge에서는 Coverage와 Consistency를 주 지표로 보고 Precision을 보조 지표로 둔다.
Hallucination 점수는 참고하되 존재하지 않는 ID·조문과 같은 기계 검증 가능한 오류는 별도
deterministic incident count로 기록한다.
