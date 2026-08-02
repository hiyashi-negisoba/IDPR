# Phase 3 최종 파이프라인·생성 핸드오버

## 인계 기준

- 작업 브랜치: `experiment/phase3-upstream-precision-20260802`
- 최종 설계 후보 커밋: `78effee`
- 원 동결 태그: `phase3-e2e-freeze-v1` — 변경하지 않음
- 개발 스모크: `kcl_criminal_r10_p1_q1_ga`,
  `CASE_KCL1730_2026_BRIBERY_FRAUD_002`
- 이후 파이프라인 설계 변경은 계약·재현성 결함이 확인된 경우가 아니면 하지 않는다.
  최종 59문항 결과를 보고 파라미터나 법리표를 다시 맞추면 holdout 오염이다.

## 마지막 설계 변경

### 1. unknown provenance와 재시도 라우팅

Call 2 계약은 `unknown`을 다음 네 원인으로 구분한다.

- `record_absent`: 사건 원문에도 필요한 사실이 없음
- `fact_graph_omission`: 원문에는 있으나 FactGraph가 구조화하지 못함
- `rule_gap`: facts는 있으나 제공 법률 기준이 부족함
- `issue_too_coarse`: 한 issue가 서로 다른 판단을 결합함

법률 detail 재검색은 `rule_gap`에만 실행한다. 나머지는 각각 원문 부재 유지,
Call-1 진단, 카탈로그 검토 대상으로 manifest에 남긴다. 자유로운 LLM 재작성이나
FactGraph 전체 back-parse는 도입하지 않았다.

### 2. 범죄단계와 기수 결론 분리

`data/rulebase/stage_issue_semantics.json`이 46개 stage issue 전부를 검토된 의미로
분류한다. 제목 정규식이나 사건별 분기는 없다.

- 기수 issue가 실제로 평가된 죄명만 `completion_reached/refuted`로 결박한다.
- 기수 불성립과 미수 처벌규정이 결합하면 `offense_attempted`가 된다.
- 기수 판단이 unknown이면 `offense_stage_unresolved`가 된다.
- 기수 issue가 없는 죄명에는 기존의 완화된 support gate를 유지한다.
- 모든 commentary element slot을 논리곱으로 강제하지 않는다.

Call 3는 `offense_attempted`를 `attempt_review`로 번역하므로, 실행착수만 인정된 죄를
기수 성립이라고 호스트가 결박하던 문제가 해소된다.

### 3. 재산 이전·점유 취득 경위

FactGraph v2.1에 `transfers[]`와 서술 술어 `property_transfer`를 추가했다.

- 이동 경위: 자발적교부, 무승낙이동, 보관위탁, 점유이탈, 반환
- 명시 목적: 보관, 전달, 사용허락, 채무변제, 대가교환, 무상양도, 목적미기재
- 이전자·수령자·대상·원문 인용 및 선택적 act 연결을 기록한다.

죄명·기망·불법영득의사 같은 규범 결론은 FactGraph에 넣지 않는다. 이 사실은 Call 2가
사기·횡령·절도·점유이탈물횡령과 그 관계를 판정할 때 공통으로 사용한다.

## 검증 및 생성 잡

세 잡은 동일 커밋에서 `afterok`으로 연결했다.

| 순서 | Slurm job | 역할 | 성공 시 산출물 |
|---:|---:|---|---|
| 1 | `218301` | 전체 pytest 회귀 | `logs/idpr_tdd_218301.{out,err}` |
| 2 | `218304` | 두 스모크 Call 1→1.5→L0→Call 2→Scallop→Call 3와 기존 출력 비교 | `experiments/results/phase3_final_design_e2e_v2` |
| 3 | `218305` | 봉인된 59문항 전체 생성 | `experiments/results/phase3_final_59` |

전체 회귀 `218301`은 `538 passed in 174.61s`로 통과했다.

첫 E2E 제출 `218302`는 모델 호출 전에 잘못 지정한 vLLM 0.17 환경이 Gemma 4를
인식하지 못해 실패했다. 연결된 `218303`은 취소했다. 검증된 기존 vLLM 0.22.0 환경
`/data5/jaehoonjeong/miniconda3/envs/inv_ass_env`로 바로잡은 실행이 `218304→218305`다.

`218302`의 추가 게이트는 다음을 확인한다.

- KCL 제297조가 기수 성립/final이 아니라 미수 검토로 배선됨
- 사용자 스모크에서 전달 목적의 재산 이전이 원문 근거로 추출됨
- 두 답안의 visible section 수가 기존 v2보다 물적으로 팽창하지 않음
- 답안 계약과 실제 section이 존재함

`218303`은 이 게이트가 실패하면 실행되지 않는다. 최종 생성은 Call 1과 Call 1.5도 새로
실행하므로 새 FactGraph 계약이 실제 59문항에 적용된다. 검색 후보는 승인된 실험값 top-10을
사용하며, 결과를 본 뒤 다시 조정하지 않는다.

### 59문항 scope

`scripts/build_phase3_final_eval_inventory.py`가 원 61 KCL 입력에서 다음 두 개발 항목을
제외하고 평가용 필드 없이 정확히 59개를 만든다.

- `kcl_criminal_r10_p1_q1_ga`: 실제 KCL 개발 스모크
- `kcl_criminal_r14_p1_q2`: 사용자 작성 대체 스모크가 대표한 뇌물전달·사기·위탁재산
  법리군의 원 KCL 항목

생성 inventory에는 `sub_question_id`, `question_text`, `question_prompt`만 있으며 rubric은
없다. `generation_manifest.json`에는 Git SHA, 모델, Slurm ID, 파라미터, 단계 시간,
프롬프트·Scallop·모든 산출물 SHA-256이 기록된다.

## 후임자 확인 절차

```bash
squeue -j 218301,218304,218305 -o '%.18i %.20j %.2t %.10M %R'
sacct -j 218301,218304,218305 --format=JobID,JobName,State,Elapsed,ExitCode
```

성공 후 다음을 확인한다.

1. `phase3_final_design_e2e_v2/freeze_manifest.json`의 status가 passed인지 확인한다.
2. `phase3_final_design_e2e_v2/final_design_comparison.json`의 `passed`가 true인지 확인한다.
3. `phase3_final_59/idpr_nsn_outputs.jsonl`이 정확히 59행이고 ID가 중복되지 않는지 확인한다.
4. `phase3_final_59/generation_manifest.json`의 해시와 `cases=59`를 확인한다.
5. 실패 case나 이전 산출물 fallback이 없는지 Call 1 admission과 case별 artifact를 확인한다.

잡이 실패하면 해당 로그와 마지막 완성 case부터 원인을 진단한다. 결과 품질이 기대보다 낮다는
이유만으로 검색·프롬프트·법리표를 수정하여 같은 59문항을 재생성하지 않는다. 계약 또는 실행
결함을 고쳐야 하는 경우에는 결함·영향범위·새 SHA를 별도 사고 기록에 남긴 뒤 전량 재생성한다.

## Future work — baseline 및 LLM-as-a-judge

평가 구현과 실행은 이번 작업 범위 밖이며 후임자가 수행한다.

1. `218303` 완료본과 기존 baseline 결과를 동일 59 ID로 inner join한다.
2. judge 입력은 문제, 공개 rubric, 익명화된 답안만 포함한다. IDPR의 FactGraph, 검색 후보,
   Scallop relation, provenance ID, method 이름은 judge에 노출하지 않는다.
3. 답안 순서를 무작위화하고 위치를 바꾼 대칭 pairwise 평가를 수행한다. 가능하면 복수 seed 또는
   복수 judge로 일관성을 기록한다.
4. rubric 항목별 충족, 법률 오류, 무관 쟁점, 결론 일관성, 전체 선호를 분리해 저장한다.
5. judge 모델·snapshot, system/user prompt, temperature, max tokens, schema, 실행 시각과 모든
   입력·출력 해시를 manifest로 고정한다.
6. paired bootstrap 신뢰구간과 baseline별 McNemar/승패 집계를 보고하고, judge 실패·동률·파싱
   실패를 임의로 제외하지 않는다.
7. 최종 평가 결과는 성능 보고에만 사용한다. 같은 holdout을 보고 현 파이프라인을 다시 최적화하지
   않는다. 후속 개선이 필요하면 별도 개발셋과 새 holdout을 만든다.

이 문서가 Phase 3 설계 종료점이다. 후임자의 첫 작업은 파이프라인을 더 고치는 것이 아니라,
연결된 생성 잡의 완결성과 manifest를 확인한 다음 동결된 평가 프로토콜을 실행하는 것이다.
