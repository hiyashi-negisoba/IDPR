# Phase 3 최종 파이프라인·생성 핸드오버

## 인계 기준

- 작업 브랜치: `experiment/phase3-upstream-precision-20260802`
- 최종 생성 코드: `2c7a317` — Call 2 계약 v2.2까지 포함
- 최종 E2E 검증기: `7b6d546`
- 원 동결 태그: `phase3-e2e-freeze-v1` — 변경하지 않음
- 개발 스모크는 `kcl_criminal_r10_p1_q1_ga`와
  `CASE_KCL1730_2026_BRIBERY_FRAUD_002` 두 건뿐이다.
- 59문항은 개발·튜닝에 사용하지 않았고 `218352`에서 처음 열어 생성한다.
- 결과 품질을 본 뒤 이 59문항에 검색·프롬프트·법리표를 다시 맞추면 holdout 오염이다.

검색을 무기한 쥐어짜며 범위를 넘고 61문항을 관찰한 이전 작업의 경위·반성·복구 경계는
`docs/2026-08-02_post_phase3_search_incident.md`에 기록되어 있다. 해당 실험은
`experiment/post-phase3-search-squeeze-20260802`의 `c1d7abf`에 격리되어 있으며 최종
파이프라인에 섞지 않았다.

## 마지막 일반화 설계 변경

### 1. unknown provenance와 재시도 라우팅

Call 2 계약은 `unknown`을 다음 네 원인으로 구분한다.

- `record_absent`: 사건 원문에도 필요한 사실이 없음
- `fact_graph_omission`: 원문에는 있으나 FactGraph가 구조화하지 못함
- `rule_gap`: facts는 있으나 제공 법률 기준이 부족함
- `issue_too_coarse`: 한 issue가 서로 다른 판단을 결합함

법률 detail 재검색은 `rule_gap`에만 실행한다. 나머지는 각각 원문 부재 유지, Call-1 진단,
카탈로그 검토 대상으로 manifest에 남긴다. 자유로운 LLM 재작성이나 FactGraph 전체
back-parse는 도입하지 않았다.

실제 E2E에서 확정 판정에도 `unknown_reason`이 붙는 guided-output 결함을 발견해 계약을
v2.2로 올렸다. 모든 판정은 필드를 출력하되 `satisfied/not_satisfied`는 오직
`not_applicable`, 실제 `unknown`만 위 네 원인을 허용한다. JSON Schema와 호스트 검증기가
같이 강제하고 진단 집계는 실제 unknown 원인만 센다.

### 2. 범죄단계와 기수 결론 분리

`data/rulebase/stage_issue_semantics.json`이 46개 stage issue 전부를 검토된 의미로
분류한다. 제목 정규식이나 사건별 분기는 없다.

- 기수 issue가 실제로 평가된 죄명만 `completion_reached/refuted`로 결박한다.
- 기수 불성립과 미수 처벌규정 및 나머지 요소가 결합하면 `offense_attempted`가 된다.
- 상위 요소가 미확정이면 유죄를 강제하지 않고 `attempt_to_consider`로 보존한다.
- 기수 판단이 unknown이면 `offense_stage_unresolved`가 된다.
- 기수 issue가 없는 죄명에는 기존의 완화된 support gate를 유지한다.
- 모든 commentary element slot을 논리곱으로 강제하지 않는다.

최종 게이트도 이 경계를 따른다. KCL에서 기수 불성립은 final/established로 바뀌지 않아야
하고, 미수 검토는 보존해야 한다. 별도의 신경망 요소가 미확정인데 E2E 스모크를 맞추려고
`offense_attempted` 유죄를 강제하지 않는다.

### 3. 재산 이전·점유 취득 경위

FactGraph v2.1에 `transfers[]`와 서술 술어 `property_transfer`를 추가했다.

- 이동 경위: 자발적교부, 무승낙이동, 보관위탁, 점유이탈, 반환
- 명시 목적: 보관, 전달, 사용허락, 채무변제, 대가교환, 무상양도, 목적미기재
- 이전자·수령자·대상·원문 인용 및 선택적 act 연결을 기록한다.

죄명·기망·불법영득의사 같은 규범 결론은 FactGraph에 넣지 않는다. 이 사실은 Call 2가
사기·횡령·절도·점유이탈물횡령과 그 관계를 판정할 때 공통으로 사용한다.

## 검토한 레버의 최종 처분

| 레버 후보 | 처분 | 최종 경계 |
|---|---|---|
| 검색 article top-k `18 → 10` | 제한 반영 | 검색 알고리즘과 전역 기본값 18은 유지한다. 두 스모크에서 핵심을 보존하며 후보·토큰을 줄인 top-10만 E2E와 `218352`의 봉인 실행 파라미터로 사용한다. |
| Call 1.5 선택과 검색 선택의 새 LLM 조율 gate | 폐기 | 선택형·precision 선택형·전 후보 결정행렬 모두 실제 핵심 조문을 누락했다. 현행 합집합 뒤에 새 LLM 탈락 gate를 두지 않는다. |
| 검색어 간 반복 지지/vote | 폐기 | 같은 FactGraph에서 파생된 상관 검색어를 독립 증거처럼 세어 무관 조문이 상승하고 핵심이 밀렸다. |
| element issue만으로 article 입장 순위 산정 | 폐기 | top-18 후보와 쟁점 수가 오히려 늘어 precision 이득이 없었다. 입장 후 전체 hierarchy를 복구하는 현행 구조를 유지한다. |
| 더 작은 고정 k·문항별 동적 k | 폐기 | 두 스모크에 맞춘 과적합이므로 채택하지 않았다. |
| 후보 검토 범위와 답안 노출 범위 분리 | 반영 | Call 2·Scallop 후보는 보존하고 Call 3에서 `full/compact/hidden`으로 표시 강도만 결정한다. |
| 긍정 근거·반대 근거 기반 material visibility | 반영 | 긍정 구성요건 지지 부재, 반증 우세, 물적 grounding 부족 후보를 숨기고 미확정 후보는 복수 사실연결이 있을 때만 compact로 남긴다. |
| 결과적 가중범·결합범 prerequisite gate | 반영 | 검수된 선행 기본범에 gap 없는 성립 신호가 있어야 독립 죄명으로 노출한다. |
| typed unknown 및 원인별 후속 라우팅 | 반영 | `rule_gap`만 legal detail 재검색으로 보내고 원문 부재·FactGraph 누락·coarse issue는 서로 다른 진단으로 남긴다. |
| stage 의미표와 기수/미수/미확정 분리 | 반영 | 46개 stage issue의 검수된 의미표를 쓰며, 미확정 상위 요소를 무시해 미수 유죄를 강제하지 않는다. |
| 재산 이전 경위·목적의 서술 FactGraph | 반영 | 죄명 결론 없이 이전자·수령자·대상·경위·목적·원문 근거만 구조화한다. |
| status와 `unknown_reason`의 스키마 결박 | 반영 | 비-unknown은 `not_applicable`, unknown만 네 진단 원인을 허용한다. |
| 사건별 조문 블랙리스트·예시·특별 임계값 | 미도입 | 두 스모크를 맞히는 하드코딩과 휴리스틱은 만들지 않았다. |
| full ClaimGraph back-parse·자유 LLM 재작성 루프 | 미도입 | 승인된 v1 범위를 넘는 복잡도와 오류 은폐 위험 때문에 결정론적 계약 검증까지만 사용한다. |

따라서 production 경로에 들어간 핵심은 “검색 순위 자체를 더 쥐어짜기”가 아니라,
top-10의 제한된 후보 예산 위에서 신경망 판정의 불확실성을 보존하고 Scallop 결론 및
답안 가시성을 물적 근거에 맞게 결박하는 일반 규칙들이다.

## 최종 검증과 출력 대조

### 회귀 및 E2E

- 전체 회귀 `218351`: `540 passed in 170.83s`, exit `0:0`.
- E2E 모델 실행 `218347`: 정확히 두 스모크를 Call 1 → Call 1.5 → 현행 L0 top-10 →
  Call 2 → Scallop → Call 3으로 새로 생성했다.
- 구조 계약 manifest:
  `experiments/results/phase3_final_design_e2e_v4/freeze_manifest.json` — `passed`.
- 설계 비교:
  `experiments/results/phase3_final_design_e2e_v4/final_design_comparison.json` — `passed`.
- manifest는 생성 코드 `2c7a317a...`와 검증기 `7b6d5462...`를 분리 기록하고,
  모델·파라미터·프롬프트·Scallop·입출력 SHA-256과 단계별 시간을 포함한다.

Slurm의 `218347` 자체는 구조 계약을 통과한 뒤 옛 비교 게이트가 제297조를 반드시
`offense_attempted`로 확정하라고 요구하여 exit 1로 끝났다. 실제 출력은 별도 요소가
`not_satisfied`여서 `attempt_to_consider`였고, 기수·final은 아니었다. 유죄를 강제하는
과도한 게이트를 일반 계약으로 고친 뒤 동일 산출물을 `7b6d546` 검증기로 재검증해 전 항목
통과시켰다. 모델 산출물을 고치거나 재사용 fallback으로 오류를 숨기지 않았다.

앞선 실패 제출도 보존한다.

- `218302`: vLLM 0.17이 Gemma 4를 인식하지 못해 모델 호출 전 실패.
- `218304`: vLLM 0.22에서 Call 1/1.5 통과 후 HF 캐시 경로 누락으로 L0 전 실패.
- `218306`: 올바른 환경에서 E2E 중 확정 판정의 `unknown_reason` 오염을 발견해 중단.
- 실패 산출물 `_v1`~`_v3`은 삭제하지 않았으며 최종 근거는 `_v4`뿐이다.

### 직접 읽은 출력 비교

KCL 스모크는 기존 v2의 가시 section 5개에서 2개로 줄었다. 제297조를 기수 성립이라고
쓰던 오류가 사라져 “기수 불성립, 미수 성립 및 유형 추가 검토”로 결박됐다. 제257조는
미확정 보충 검토로 남았다. 상위 Call 1/L0가 잡지 못한 주거침입강간치상 쟁점을 뒤에서
인위적으로 복원하지 않았다.

사용자 스모크는 기존 v2의 가시 section 3개에서 1개로 줄었다. 무관한 제133조와 미확정
제355조를 답안에서 제거하고 제347조 사기만 성립시켰다. FactGraph는 다음 두 이전을 원문
인용과 함께 기록했다.

- `甲 → 丙`: `자발적교부`, 목적 `전달`
- `丙 → 채권자`: `자발적교부`, 목적 `채무변제`

Call 2 v2.2 일관성도 직접 확인했다. KCL은 최종 unknown 14개와 원인 14개
(`rule_gap=5`, `record_absent=9`)가 정확히 일치했고 비-unknown 54개는 모두
`not_applicable`이었다. 사용자 스모크는 unknown 0개, 51개 판정 전부
`not_applicable`이었다. status/reason 불일치는 두 문항 모두 0개였다.

이 검증은 구조·배선·정합성과 답안 가시성 비교다. 루브릭 점수나 검색 recall을 통과
조건으로 사용하지 않았다.

## 59문항 생성 잡

| Slurm job | 상태 기준 시각 | 역할 | 산출물 |
|---:|---|---|---|
| `218351` | COMPLETED | 최종 전체 pytest | `logs/idpr_tdd_218351.{out,err}` |
| `218352` | RUNNING, 2026-08-03 00:42 KST | 봉인된 59문항 전체 생성 | `experiments/results/phase3_final_59` |

`218352`는 `afterok:218351`로 제출했고 n05에서 실제 실행 중이다. 이미
`final_59_inventory.jsonl` 59행을 물리적으로 생성했으며 Call 1 모델 서버를 기동했다.
전체 경로는 Call 1 → Call 1.5 → L0 top-10 → Call 2 → Scallop → Call 3이고,
Call 1/1.5도 새로 실행하므로 새 FactGraph 계약이 전 문항에 적용된다.

실행 환경은 다음으로 고정했다.

- Python/vLLM: `/data5/jaehoonjeong/miniconda3/envs/inv_ass_env`의 vLLM 0.22.0
- 모델 snapshot: 로컬 `google/gemma-4-26B-A4B-it` snapshot `01e5b3ee...`
- served model: `idpr-gemma-4-26b-a4b`
- retrieval cache: `/data5/jaehoonjeong/.cache/huggingface`

### 59문항 scope

`scripts/build_phase3_final_eval_inventory.py`가 원 61 KCL 입력에서 다음 두 개발 항목을
제외하고 평가용 필드 없이 정확히 59개를 만든다.

- `kcl_criminal_r10_p1_q1_ga`: 실제 KCL 개발 스모크
- `kcl_criminal_r14_p1_q2`: 사용자 작성 대체 스모크가 대표한 뇌물전달·사기·위탁재산
  법리군의 원 KCL 항목

생성 inventory에는 `sub_question_id`, `question_text`, `question_prompt`만 있으며 rubric은
없다. 완료 시 `generation_manifest.json`에 Git SHA, 모델, Slurm ID, 파라미터, 단계 시간,
프롬프트·Scallop·모든 산출물 SHA-256이 기록된다.

## 후임자 확인 절차

```bash
squeue -j 218352 -o '%.18i %.24j %.2t %.10M %R'
sacct -j 218351,218352 --format=JobID,JobName,State,Elapsed,ExitCode
tail -n 50 logs/phase3_final_59_218352.out
tail -n 50 logs/phase3_final_59_218352.err
```

`218352` 성공 후 다음을 확인한다.

1. `phase3_final_59/idpr_nsn_outputs.jsonl`이 정확히 59행이고 ID가 중복되지 않는지 확인한다.
2. `phase3_final_59/generation_manifest.json`의 `cases=59`, 모델·Git SHA·해시를 확인한다.
3. Call 1 admission fallback, Call 2 재시도 오류, 실패 case가 없는지 manifest와 case별
   artifact를 확인한다.
4. 오류 없이 완료됐으면 결과를 수정하지 말고 baseline과 judge 평가 입력으로 봉인한다.

잡이 실패하면 로그와 마지막 완성 case부터 실행·계약 원인을 진단한다. 결과 품질이 기대보다
낮다는 이유만으로 검색·프롬프트·법리표를 수정해 같은 59문항을 재생성하지 않는다. 계약 또는
실행 결함을 고쳐야 한다면 결함·영향범위·새 SHA를 별도 사고 기록에 남기고 전량 재생성한다.

## Future work — baseline 및 LLM-as-a-judge

평가 구현과 실행은 이번 작업 범위 밖이며 후임자가 수행한다.

1. `218352` 완료본과 기존 baseline 결과를 동일 59 ID로 inner join한다.
2. judge 입력은 문제, 공개 rubric, 익명화된 답안만 포함한다. IDPR의 FactGraph, 검색 후보,
   Scallop relation, provenance ID, method 이름은 judge에 노출하지 않는다.
3. 답안 순서를 무작위화하고 위치를 바꾼 대칭 pairwise 평가를 수행한다. 가능하면 복수 seed
   또는 복수 judge로 일관성을 기록한다.
4. rubric 항목별 충족, 법률 오류, 무관 쟁점, 결론 일관성, 전체 선호를 분리해 저장한다.
5. judge 모델·snapshot, system/user prompt, temperature, max tokens, schema, 실행 시각과 모든
   입력·출력 해시를 manifest로 고정한다.
6. paired bootstrap 신뢰구간과 baseline별 McNemar/승패 집계를 보고하고 judge 실패·동률·파싱
   실패를 임의로 제외하지 않는다.
7. 최종 평가는 성능 보고에만 사용한다. 같은 holdout을 보고 현 파이프라인을 다시 최적화하지
   않는다. 후속 개선이 필요하면 별도 개발셋과 새 holdout을 만든다.

이 문서가 Phase 3 설계 종료점이다. 후임자의 첫 작업은 파이프라인을 더 고치는 것이 아니라,
`218352`의 완결성과 manifest를 확인한 다음 동결된 평가 프로토콜을 실행하는 것이다.
