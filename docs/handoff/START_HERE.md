# 다음 세션 시작점

기준: 2026-08-16 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00
검증: `585 passed, 16 skipped` (conda **base**, `/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q`)

## 한 줄 상태

**Phase A~C가 닫혔고 Call 1 → Call 2 재생성이 완주했다.** 그 결과가 새 structural baseline이다
(§4). 다음 작업은 **residual UNKNOWN 저작 개선**이며, 그 전에 freeze용 deterministic cleanup이
하나 남아 있다(§6).

여기서 `intent`나 `means_or_object_defect`를 먼저 건드리면 "구조 수정으로 좋아진 것"과
"저작 개선으로 좋아진 것"의 경계가 섞인다. baseline을 얼려 두고 시작한다.

## 읽는 순서

1. **이 문서** — 무엇이 닫혔고 다음에 무엇을 도는가
2. [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) — 사용자 저작 지시서. §11-bis에 2026-08-15
   갱신(감사 시점에 보이지 않던 세 건)이 있다.
3. 결재 기록 5건 — 재검수 대상이 아니라 **왜 그렇게 되었는지**를 찾을 때 본다.
   [`PHASE_A12_DESIGN.md`](PHASE_A12_DESIGN.md) ·
   [`ROUTE_DEPENDENCY_PROMPT.md`](ROUTE_DEPENDENCY_PROMPT.md) ·
   [`A3_ASSAULT_FAMILY_WORKSHEET.md`](A3_ASSAULT_FAMILY_WORKSHEET.md) ·
   [`A4_STOLEN_PROPERTY_WORKSHEET.md`](A4_STOLEN_PROPERTY_WORKSHEET.md) ·
   [`ARTICLE151_PENALTY_WORKSHEET.md`](ARTICLE151_PENALTY_WORKSHEET.md)
4. [`AXIS_CLOSURE.md`](AXIS_CLOSURE.md) · [`CODEBASE_AUDIT.md`](CODEBASE_AUDIT.md) — 이전 축의 감사 정본
5. `NEXT_SESSION.md` — append-only 역사 로그. 그 안의 "다음 작업" 지시는 전부 만료다.

---

## 1. 2026-08-15에 닫힌 것 (다시 열지 말 것)

### Phase A

| | 내용 |
|---|---|
| A1 | 제151조 linked-offender. ROUTE를 재사용 가능한 operation으로 일반화하고, Call 1.5가 사람을 결박한 뒤 dependency planner가 재호출한다. 신분은 participant 수준 `Article151PredecessorStatus`이고 ordinary liability가 아니다. Scallop parity path는 **만들지 않았다** — 최종 죄책은 기존 offense program 소유 |
| A2 | 객체 동일성. `directed_action_target`/`actual_result_bearer`에서 host가 structural divergence를 세고, TRUE인 instance에서만 `object_misidentification`을 연다. 착오 정책 production 호출부 연결됨 |
| A3 | 폭행죄 family (폭행·특수폭행·폭행치상·폭행치사) + 질적 초과 pair |
| A4 | 장물죄 family (취득·보관) + 불가벌적 사후행위 흡수 규칙 (`ordered_cross_episode`) |

### Phase B·C

| | 내용 |
|---|---|
| B2 | 제263조 authority 단일화 — 감사는 2중이라 했으나 실제 **4중**이었다 |
| B3 | `blocked_when` traversal — latent이 아니라 **active blocker**였다. defeat doctrine 5개가 영원히 발동 불가였다 |
| B4 | `candidate_materialization` ref checker |
| B5 | 제33조 co-principal — 구현하지 않고 `gap.co_principal_status_redirection`으로 승격 |
| C | `grounded_by` / `disabled_modes`를 저작하면 checker가 실패한다. 둘 다 사용량 0인 지금이 막기 가장 싼 시점이었다 |

### 새로 저작된 정의 — **Call 1 routing universe가 바뀌었다**

```text
offense.assault / derived_offense.special_assault
derived_offense.assault_causing_injury / derived_offense.assault_causing_death
offense.stolen_property_acquisition / offense.stolen_property_custody
```

predicate 6건, qualifier 1건, 흡수 규칙 1건, 질적 초과 pair 1건, seed cue 6건이 함께 들어갔다.
`article151_penalty_threshold`는 63개 offense 전부에 저작되었다(법률 검수 완료).

---

## 2. 남은 gap — 다섯 건, 전부 typed

큰 "범죄군 없음" gap은 사라졌고 실제 미지원 법리만 남았다. **각 항목의 `consequence`를 읽어라**
— 어떤 KCL 문항이 왜 부분적으로만 닫히는지가 거기 적혀 있다.

| gap | 영향 |
|---|---|
| `gap.co_principal_qualitative_excess` | `r11_p1_q1`의 丙 갈래. 甲(교사)은 닫혔다 |
| `gap.special_assault_aggravated_result` | 제262조의 특수폭행 갈래. KCL-26에 해당 사안 미확인 |
| `gap.stolen_property_self_principal_exclusion` | `r13_p2_q1`이 지금 맞는 답을 내는 것은 **우연이지 규칙이 아니다** |
| `gap.co_principal_status_redirection` | 제33조 단서를 공동정범에 적용 불가 |
| `gap.justifying_premise_vs_object_identity` | 의도적으로 닫아 둔 cue (검수 ②) |

---

## 3. authoring-review로 남긴 것 — 재생성 결과를 보고 판단한다

1. **결과적 가중범의 generic `intent`** — `legal_element.intent`가 "기본범죄 고의"인지
   "중한 결과 고의"인지 Call 2가 스스로 정한다. 폭행치상에서 후자로 읽히면 성립이 뒤집힌다.
   기존 결과적 가중범 전체가 같은 구조라 개별 수정하지 않았다.
2. **`intent_toward_intended_object`** — 착오 정책이 instance의 generic intent를 읽는다.
   Call 2가 "실제 피해자에 대한 고의"로 읽으면 정책이 침묵한다(틀린 귀속보다 안전한 방향).
3. **`ground_fact.means_or_object_defect`** — 45 asked / TRUE 1 · FALSE 0. 이전 세션 이월분.

셋 다 **재생성 후 실제 병목으로 드러날 때** 검수한다. 지금 고치면 근거 없이 고치는 것이다.
그리고 1·2는 UNKNOWN이 아니라 **잘못된 방향의 TRUE/FALSE**로 나타나므로 UNKNOWN 통계만
보면 놓친다.

---

## 4. 새 structural baseline (2026-08-15 재생성, `experiments/v2_rulebase_regen_26/`)

```text
                이번        직전(v2_final_e2e_26)
planned         635         758
asked           595         697
TRUE            286 48.1%   256 36.7%
FALSE            21  3.5%    25  3.6%
UNKNOWN         288 48.4%   416 59.7%
```

**UNKNOWN 감소를 모델 성능 개선으로 읽지 말 것.** 구조적으로 잘못 열리던 target의 제거와,
새로 도달 가능해진 target의 실제 평가가 합쳐진 재생성 결과다. 모델은 같고 프롬프트도 계약
문구 하나 외에 그대로다.

축별 판정과 그 근거는 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) §11-quater에 있다. 요약:

* **A1** dependency ROUTE 4/4 reachable. `r10_p2_q2`에서 `offender_status_of_object = TRUE`
* **A2/제263조** pair 생성, `asked 6 / TRUE 4 / UNKNOWN 2`. 객체 불일치 TRUE 3건
* **A3/A4** 신규 죄 `asked 80 / TRUE 45 / FALSE 1 / UNKNOWN 34`

### 재생성 중 드러난 것 — 다음 사람이 반드시 알아야 할 두 가지

**① A3가 겹치는 seed를 들여오자 unauthored structural assumption 다섯 개가 연쇄로 드러났다.**
전부 "서사 분할이나 추출 필드를 법적 요건으로 쓰고 있었다"는 같은 형태다. 감사보고서
§11-quater의 표가 사슬 전체를 담고 있다. 앞으로 비슷한 증상이 나오면 그 표부터 볼 것.

**② A1 관련 수정 후에는 기반 planner부터 다시 돌려야 한다.**
`linked_offender_dependencies`는 축 체인이 아니라
`scripts/run_v2_full_regeneration.sh`의 `plan` 단계가 만들고, 축 체인의 `plan_participation`은
그것을 `deepcopy`해 나른다. 축 체인만 돌리면 **옛 값으로 조용히 통과한다** -- 이번에 한 번
그렇게 속았다.

### 재생성 실행 방법

```bash
# 상류 (Call 1 → Call 1.5 → planner)
IDPR_STEP8_SERVICE_JOB_ID=<job> IDPR_REGEN_SKIP="" \
  srun --jobid=<job> --ntasks=1 --cpus-per-task=2 /bin/bash \
  scripts/slurm/run_v2_full_regeneration.sh --execution-approved

# 축 체인 (participation → doctrine → dependency ROUTE → Call 2 → 제151조 신분)
IDPR_STEP8_SERVICE_JOB_ID=<job> \
IDPR_AXIS_RUN_ROOT=.../v2_rulebase_regen_26 \
IDPR_CALL1_ARTIFACT=.../call1/router_output.jsonl \
IDPR_CALL15_ARTIFACT=.../call15/issue_binding.jsonl \
IDPR_BASE_PLAN=.../plan/evaluation_instance_plan.jsonl \
  srun --jobid=<job> --ntasks=1 --cpus-per-task=2 /bin/bash \
  scripts/slurm/run_v2_axis_closure_e2e.sh --execution-approved
```

`--cpus-per-task`는 allocation 한도(현재 2)를 넘기면 job step이 만들어지지 않는다.
Call 1.5는 `--max-tokens 4096`이 필요하다 -- 죄가 늘면서 2048에서 잘렸다.

분포 확인:

```bash
python scripts/audit_v2_call2_distribution.py --plan <plan_doctrine> --call2 <call2>
```

---

## 5. 다음 작업 — residual UNKNOWN 저작 개선

실측 병목이 authoring-review 목록과 겹친다. 순서는 이렇게 간다.

**① `legal_element.intent` (28/42 UNKNOWN, 1위).**
결과적 가중범에서 이 고의가 기본범죄에 대한 것인지 중한 결과에 대한 것인지 모델이 스스로
정한다. 폭행치상에서 후자로 읽히면 성립이 정반대로 뒤집힌다. 기본범죄 고의의 scope를
저작이 명시적으로 소유하게 한다.

**② `ground_fact.means_or_object_defect` (25/31 UNKNOWN, 2위).**
exclusion 둘이 TRUE·FALSE 양쪽 경로를 과도하게 막는지 재저작 검수. `dangerousness`(13/14)가
그 하류다.

**③ FALSE 희소성 (3.5%).**
**목표를 "FALSE 비율을 올리는 것"으로 잡지 말 것.** 정답 분포를 모르므로 그것은 측정할 수
없는 목표다. 찾는 것은 *명확한 반증이 있는데도 UNKNOWN으로 빠지는 systematic pattern*이고,
predicate·프롬프트별 failure mode로 분해해야 보인다.

①~③ 모두 저작 검수가 필요하므로 문안을 만들어 승인받은 뒤 설치한다.

---

## 6. freeze 전 남은 deterministic cleanup

**cue 카탈로그 완결성.** 라우팅 가능한 죄 중 16건이 cue 없이 남아 있다. cue가 없으면 Call 1이
그 죄를 고르는 순간 Call 1.5가 **그 사건에서 예외로 죽는다** -- 이번 재생성에서 실제로 그렇게
멈췄고, 그때 라우팅된 5건만 채웠다.

16건은 `data/v2/binding_seed_cues.yaml`의 `unauthored_cue_offense_refs`에 명시했고,
`tests/test_binding_seed_cue_catalog.py`가 "cue가 있거나 미저작으로 선언되어 있거나" 둘 중
하나를 강제한다. 그래서 지금은 조용히 죽지는 않지만, **freeze 전에 16건을 저작해야 한다.**
cue는 binding을 유도하는 자산이라 검수가 필요하고, 그래서 미검수 16개를 한꺼번에 써 넣지
않았다.

---

## 7. 실행 환경 (변경 없음)

* pytest: conda **base** — `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기
* 긴 작업·GPU 작업은 **길이 무관 항상 sbatch**. nohup은 고아 프로세스가 된다
* sbatch에 `IDPR_HF_HOME` 필수. 안 넘기면 빈 홈캐시로 새서 job이 실패한다
* job 진행상황 백그라운드 폴링 금지
* 체인은 `IDPR_AXIS_SKIP`으로 이어 돌린다

## 8. 정본 artifact

**현재 정본: `experiments/v2_rulebase_regen_26/`** (Call 2까지). symbolic·AnswerPlan·Call 3은
아직 돌리지 않았다 -- 이번 사이클은 최종 Call 2까지가 범위였다.

직전 정본 `experiments/v2_final_e2e_26/`은 Call 3까지 있으나 rulebase가 다르다. 비교용으로만
본다. Call 3의 exit 2는 실패가 아니라 감사 게이트다.

## 9. 정책 (변경 불가)

* **sealed-59**: `kcl_criminal_r10_p1_q1_ga`와 `kcl_criminal_r14_p1_q2` 두 dev case만 열 수 있다.
  나머지 59건은 채점 전용. **sealed-59를 열어 UNKNOWN을 분류하지 않는다.**
* **프롬프트·정의 승인 게이트**: 활성 프롬프트와 정의 전문은 사용자 승인 후에만 설치한다.
* 새 정적 감사를 임의로 열지 않는다. 실제 E2E 결과에서 문제가 나온 지점만 본다.
