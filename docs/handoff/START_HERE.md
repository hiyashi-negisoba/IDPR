# 다음 세션 시작점

기준: 2026-08-16 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00
검증: `593 passed, 16 skipped` (conda **base**, `/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q`)

## 한 줄 상태

**Call 3가 B 계약으로 얼렸다. 다음 일은 두 가지다 — ① IDPR-B와 CoT를 사람이 직접 읽고
질적으로 비교한다 ② 그 결과에 따라 라우터/규칙베이스를 조인다.**

채점(LLM judge)은 **아직 한 번도 돌리지 않았다.** 사용자 결정이다 — 라우터를 조이기 전에
쓰면 한 번뿐인 채점을 낭비한다. 이번 세션 API 호출 0건.

## 읽는 순서

1. **이 문서**
2. `docs/v2_plan/ANSWERPLAN_SPEC.md` — Call 3 payload의 계약. §4 계약과 §6 N/P ablation
3. `prompts/v2_call3_irac.md` — 활성 프롬프트(B). 이전 A본은
   `prompts/candidates/v2_call3_irac_A_frozen.md`
4. `NEXT_SESSION.md` — append-only 역사 로그. 그 안의 "다음 작업" 지시는 전부 만료다

---

## 1. 지금 손에 있는 것

| 아티팩트 | 경로 | 내용 |
|---|---|---|
| **IDPR-B (채점 대상)** | `experiments/v2_unknown_reduction_26/frozen_B/` | 답안 26 + plan. `answers.jsonl` `sha256:8e057342…` |
| **N 조건 plan** | `…/ablation_N/answer_plan/` | 카드 없이 만든 plan. **call3는 아직 안 돌렸다** |
| **CoT** | `experiments/results/cot_26_8192/chain_of_thought_outputs.jsonl` | 26문항, `max_tokens=8192`, `temperature=0.0` |

`frozen_B`는 사본이다. 체인을 다시 돌려 `call3/`을 덮어써도 채점 대상은 이 사본이다.

## 2. Call 3 B 계약 — 무엇이 확정이고 무엇이 열렸나

사용자 승인 사항이다. 바꾸려면 다시 승인을 받는다.

* `analysis`가 **"성립한다"/"성립하지 않는다"로 적은 것은 확정**이다. 절대 뒤집지 않는다
* **UNRESOLVED는 모델이 논증 후 결론까지** 간다. 어느 요건이 왜 결박되지 않았는지를 밝힌 뒤
* `analysis`에 없는 죄는 **쟁점 제기·검토까지만**. 최종 죄책으로 확정 금지
* 죄수는 symbolic이 준 것이 우선, 없는 부분만 자유 정리
* 판례 법리는 **그 요건에 관한 것이지 죄의 정의가 아니다**
* 같은 행위자·죄명이 다른 occurrence로 열리면 **합치지 않는다.** 사건 원문 인용으로 갈라 부른다

## 3. 이번에 닫은 것 — 커밋 2건

`b05fd98` · `222808f`

배점의 28.7%(판례 15.6 · 죄수 8.2 · 학설 4.9)가 **입력을 한 번도 받지 못하고 있었다.**
기계는 다 만들어져 있었고 체인이 인자를 안 넘겼을 뿐이다.

| | 이전 | 지금 |
|---|---:|---:|
| payload 판례 법리 / 학설 | 0 / 0 | **396 / 18** |
| 답안 길이 중앙값 | 1,760자 | **2,266자** |
| 결론 누락 | 0 → (B 1차) 4항목 | **1항목·1문항** |
| 각칙 조문 누출 | 126건 | **9건**(기초범죄 상속, 정당) |

* 카드 회수(P) + 학설 trigger + 흡수 pair 단계를 체인에 배선. `run_v2_axis_closure_e2e.sh`
* 공유 요건의 조문이 다른 죄로 번지던 것 차단 — 죄의 `statutory_refs` + `derivation.base`까지가
  범위, 총칙은 어디서나 허용
* 제355조 횡령/배임처럼 **항이 갈리는 죄**를 카드 회수에서 분리. issue 범위와 명제 양쪽,
  **명제 필터는 tier와 무관하게** 건다(fallback에서 오염 부활 방지)
* 입장이 하나뿐이거나 중복인 대립은 학설로 내보내지 않는다

## 4. 다음 작업 — 순서대로

### 4-1. 사람이 직접 읽는 질적 비교 (최우선)

`frozen_B/answers.jsonl`과 `cot_26_8192/chain_of_thought_outputs.jsonl`을 나란히 놓고
**사람이 읽는다.** 자동 지표로 대신하지 않는다 — §6에 그 이유가 있다.

열람 가능한 사례는 dev 2건뿐이다(§7). 나머지는 답안 텍스트만 보고 형식·논증 밀도를 본다.

### 4-2. N 조건 call3 (ablation, 무료)

`ablation_N/answer_plan/answer_plans.jsonl`로 call3만 돌리면 SPEC §6의 P−N이 완성된다.
symbolic anchor가 P와 **완전히 동일**함은 확인했다(state·결론목록 전량 일치). 로컬 vLLM만 쓴다.

### 4-3. 라우터/규칙베이스 조이기

`scripts/audit_v2_offense_coverage.py`가 이 축의 진단 도구다.

```
저작된 죄명 69개 · rubric 죄명 173건 (26문항)
  라우팅됨        68 (39.3%)
  저작O·라우팅X   45 (26.0%)   <- 라우터 recall
  저작X           60 (34.7%)   <- 규칙베이스 커버리지
```

**공백의 절반 이상이 라우터가 아니라 규칙베이스다.** 죄명 자체가 저작돼 있지 않으면 Call 1이
열 수가 없고 Call 3도 살릴 수 없다. 라우터만 조이면 26.0%가 상한이다.

빠진 것 중 반복되는 것: 협박 · 강요 · 제3자뇌물교부/취득 · 뇌물수수 · 장물 · 합동절도 ·
주거침입강간(치상/중지미수) · 체포 · 수뢰후부정처사.

### 4-4. 채점

위가 끝난 뒤 **한 번만** 돌린다. 기존 자산으로 충분하다 — 새로 만들지 말 것.

* `scripts/run_phase3_llm_judge.py` — `--methods-manifest` / `--case-id-file` /
  `--sealed-inventory` / `--expected-cases`. 방식 여럿을 한 매니페스트에 넣으면 익명화와
  job 셔플을 이미 한다
* `scripts/slurm/run_phase3_v2_idpr_judge.sh` — 실행 래퍼(preflight 포함)
* `scripts/build_v2_diagnostic_judge_inputs.py` — Call 3 `answer` → `generated_response`
* `scripts/aggregate_eval_matrix.py`, `data/eval/phase3_method_outputs*.json` 규약

## 5. 다시 하지 말 것

| 시도 | 결과 |
|---|---|
| 죄명 커버리지를 `[가-힣]{2,12}죄` 정규식으로 뽑기 | 숫자에서 잘리고 죄수 개념이 섞인다. `scripts/audit_v2_offense_coverage.py`를 쓸 것 |
| 흡수 pair 단계를 켜서 죄수 배점 먹기 | pair는 열리는데 **저작된 흡수규칙이 2개뿐**이라 26문항에서 pair 1건, 그마저 UNKNOWN. 죄수는 프롬프트가 진다 |
| 옛 카드 회수 산출물 재사용 | occurrence id가 `binding:*`→`realization:*`로 개명돼 키 일치율 0%. 현행 run으로 다시 회수해야 한다 |
| judge 입력 빌더 새로 만들기 | 이미 다 있다(§4-4). 감사 없이 만들어 지웠다 |
| intent target에 owning offense 사실 주입 / carrier 신설 등 | 이전 축의 실패 4건. `NEXT_SESSION.md` 참조 |

## 6. 이번 세션 자동 지표의 신뢰도 — 낮다

죄명 추출이 깨져 있어서 **같은 질문에 네 번 다른 답을 냈다.** 고치고 테스트 6개로 묶었지만
(`tests/test_offense_coverage_extraction.py`), 잔여 결함이 남아 있다.

* "저작X" 목록에 `문서죄`·`수수죄`·`개장죄`처럼 **여전히 문장 조각으로 의심되는 항목**이 있다.
  확인하려면 rubric 원문을 봐야 하는데 sealed라 못 본다
* `성폭법위반죄` 같은 특별법 명칭이 우리 저작명과 다른 형태일 수 있다
* 답안 죄명 재현율(IDPR-B 48.6% / CoT 39.3%)은 **rubric 점수가 아니라 프록시**다. 항목 유형
  8종 중 죄명이 걸리는 것은 일부이고, 법리·적용·판례 항목은 이 지표가 전혀 보지 못한다

**이 수치로 CoT와의 우열을 결론짓지 말 것.** 사람이 읽는 것(§4-1)이 이 단계의 판단 근거다.

## 7. 정책 (변경 불가)

* **sealed-59**: `kcl_criminal_r10_p1_q1_ga`와 `kcl_criminal_r14_p1_q2` 두 dev case만 열 수 있다
* **프롬프트·정의 승인 게이트**: 활성 프롬프트와 정의 전문은 사용자 승인 후에만 설치한다
* **API 승인 게이트**: 채점 등 유료 호출은 비용 추정과 함께 승인을 받는다
* 긴 작업·GPU 작업은 길이 무관 **항상 sbatch**, `IDPR_HF_HOME` 필수. job 백그라운드 폴링 금지
* pytest는 conda **base**

## 8. 실행 방법

```bash
# 체인 (vLLM service allocation 안에서 CPU job step으로)
IDPR_STEP8_SERVICE_JOB_ID=<job> IDPR_AXIS_RUN_ROOT=<RUN> \
IDPR_CALL1_ARTIFACT=.../v2_rulebase_regen_26/call1/router_output.jsonl \
IDPR_CALL15_ARTIFACT=.../v2_rulebase_regen_26/call15/issue_binding.jsonl \
IDPR_BASE_PLAN=<RUN>/plan/evaluation_instance_plan.jsonl \
IDPR_AXIS_SKIP="..." \
  srun --jobid=<job> --ntasks=1 --cpus-per-task=2 /bin/bash \
  scripts/slurm/run_v2_axis_closure_e2e.sh --execution-approved

# 카드 회수 (GPU)
IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface \
IDPR_PYTHON=/data5/jaehoonjeong/miniconda3/bin/python \
IDPR_CARD_RUN_ROOT=<RUN> sbatch --export=ALL scripts/slurm/run_v2_card_rule_statements.sh

# 죄명 커버리지
PYTHONPATH=src python scripts/audit_v2_offense_coverage.py \
  --plan-artifact <RUN>/plan_concurrence/evaluation_instance_plan.jsonl \
  --case-id-file data/inventory/substantive_26_case_ids.txt \
  --answers IDPR-B=<RUN>/frozen_B/answers.jsonl \
  --answers CoT=experiments/results/cot_26_8192/chain_of_thought_outputs.jsonl
```

* `--cpus-per-task`는 **2**다. 8을 요청하면 서비스 job의 할당을 넘어 step 생성이 실패한다
* 실행 디렉터리 이름을 바꾸면 plan lineage가 끊긴다. 이번에도 `v2_h1`→`v2_unknown_reduction_26`
  개명 때문에 한 번 멈췄다 — plan을 같은 입력으로 재생성하면 바이트가 같으므로 복구된다
