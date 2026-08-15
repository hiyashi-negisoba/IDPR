# 다음 세션 시작점

기준: 2026-08-16 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00
검증: `585 passed, 16 skipped` (conda **base**, `/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q`)

## 한 줄 상태

**residual UNKNOWN 축이 닫혔다. Call 2를 이 상태로 확정하고 뒷단으로 간다** —
symbolic(Scallop) → AnswerPlan → Call 3. 그 단계의 지시는 사용자가 따로 준비한다.

UNKNOWN **288 → 236 (48.4% → 42.1%)**, TRUE 286 → 299. 정본 아티팩트는
`experiments/v2_unknown_reduction_26/`(Call 2까지).

## 읽는 순서

1. **이 문서**
2. [`UNKNOWN_DIAGNOSIS.md`](UNKNOWN_DIAGNOSIS.md) — 288을 A/B/C/D로 가른 진단. 아래 §3의
   "정당/부당" 분류가 여기서 나왔다
3. `data/v2/representation_gaps.yaml` — 못 고치는 것이 왜 못 고치는지. 특히
   `gap.participant_status_not_bound`
4. [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) — 사용자 저작 지시서
5. `NEXT_SESSION.md` — append-only 역사 로그. 그 안의 "다음 작업" 지시는 전부 만료다

---

## 1. 이번에 얼린 것 — 커밋 6건

| 커밋 | 내용 | UNKNOWN |
|---|---|---:|
| `94c7a3c` | 사다리는 assessed UNKNOWN에서 멈춘다 | 288→276 |
| `6a73827` | 취거·점유를 행위자 에피소드 폭으로 | →263 |
| `57a8271` | 고의를 행위자 에피소드 폭으로 | →255 |
| `4acf973` | 주거침입을 행위자 에피소드 폭으로 | →252 |
| `aa4d82a` | 뇌물 요구 문안 + `gap.participant_status_not_bound` 등록 | →252 |
| `85e4a10` | blocker는 막을 state가 성립한 뒤에 묻는다 | →236 |

프롬프트는 한 줄도 바꾸지 않았다. 전부 저작(`evidence_scope`)이거나 스케줄링이다.

## 2. 시도했다가 되돌린 것 넷 — 다시 하지 말 것

| 시도 | 결과 |
|---|---|
| intent target에 owning offense의 대상 사실을 payload로 주입 | intent U 28→31, 공통 target 10.8% 오염. **순손해** |
| `aggravated_result_attribution`·`dangerous_weapon_carriage` 폭 확대 | 효과 1건, 부작용 10건 |
| 뇌물 `약속`·`수수` 문안 재작성 | 순효과 1건인데 결정된 FALSE를 TRUE로 뒤집음. 법률 검수 전까지 보류 |
| `participant_status`·`related_party_action` carrier 신설 | carrier는 실제로 넓어졌는데 신분 predicate 불변, 8.3% 오염 → gap으로 승격 |

세 번째 것 때문에 `bribe_promise`("약속")와 `bribe_acceptance`("수수")는 여전히 한 단어다.
스키마가 요구하는 긍정 진리조건 문장이 아니므로 **문안 검수가 남아 있다**.

## 3. 남은 236의 성격 — 대부분 손대면 안 되거나 이 축 밖이다

| | 건수 | 조치 |
|---|---:|---|
| instance 전멸 | 44 | **고치면 안 됨.** 답하면 없는 범죄를 인정하는 것 |
| 신분·상대방 행위 미결박 | 16 | `gap.participant_status_not_bound`. Call 1.5가 소유 |
| 고의 계열 잔여 | 34 | 폭 레버 소진. 남은 길은 "행위에서 고의 추단 허용"인데 프롬프트가 추단을 금지한다 — 아키텍처 판단 |
| 법적 평가(인과·귀속) | 12 | 사실 확인으로 답할 물음이 아님 |
| 꼬리 | ~100 | predicate 40여 개에 흩어짐. 단일 수정 불가 |

**mental 자리 FALSE는 여전히 0이다(100건).** 이것은 결함이 아니다 — 고의의 부정은
`intent=FALSE`가 아니라 착오·책임 쪽으로 가도록 저작돼 있다(`mistake_policy`는
`intent_preserved`). 그 자리에서 FALSE를 목표로 삼으면 이중 판단이 된다.

## 4. 다음 작업 — 뒷단

Call 2를 확정하고 `symbolic → answer_plan → call3`을 돈다. 직전 정본
`experiments/v2_final_e2e_26/`은 Call 3까지 있으나 rulebase가 다르므로 비교용으로만 본다
(Call 3의 exit 2는 실패가 아니라 감사 게이트다).

## 5. 실행 방법

```bash
# Call 2까지 (plan 재생성이 필요하면 기반 planner부터)
PYTHONPATH=src python scripts/run_v2_evaluation_instance_planner.py \
  --call1-artifact <call1> --call1-manifest <manifest> --call15-artifact <call15> \
  --out <RUN>/plan/evaluation_instance_plan.jsonl \
  --manifest-out <RUN>/plan/evaluation_instance_plan.manifest.json

IDPR_STEP8_SERVICE_JOB_ID=<job> IDPR_AXIS_RUN_ROOT=<RUN> \
IDPR_CALL1_ARTIFACT=... IDPR_CALL15_ARTIFACT=... IDPR_BASE_PLAN=<RUN>/plan/... \
IDPR_AXIS_SKIP="call15p call15d dependency_route linked_offender_call2 absorption symbolic answer_plan call3" \
  srun --jobid=<job> --ntasks=1 --cpus-per-task=2 /bin/bash \
  scripts/slurm/run_v2_axis_closure_e2e.sh --execution-approved
```

* `evidence_scope`를 바꾸면 carrier가 plan에 구워지므로 **기반 planner부터** 다시 돌린다.
  축 체인만 돌리면 옛 carrier로 계약 위반이 나며 멈춘다
* 실행 디렉터리 이름을 바꾸면 plan lineage가 끊긴다. 옮길 때 plan 체인을 같이 옮긴다
* 분포 비교: `scripts/audit_v2_call2_distribution.py`,
  실패 유형 분해: `scripts/audit_v2_unknown_failure_modes.py`

## 6. 측정 규약 (이번 세션에서 확립)

* **무변경 재실행의 변동은 595건 중 2건(0.3%)이다.** 그 이상은 전부 변경이 만든 것이다
* 판정은 항상 둘을 같이 본다 — 대상 predicate의 T/F/U, 그리고 **손대지 않은 predicate의
  변동률**. 후자가 효과보다 크면 되돌린다
* UNKNOWN 감소만 보지 않는다. asked 분모와 TRUE/FALSE 후퇴를 함께 읽는다. 스케줄링 수정은
  분모를 줄이는 방식이므로 비율만 보면 과대평가된다

## 7. 실행 환경 (변경 없음)

* pytest: conda **base** — `/data5/jaehoonjeong/miniconda3/bin/python`
* 긴 작업·GPU 작업은 길이 무관 **항상 sbatch**. job 진행상황 백그라운드 폴링 금지
* sbatch에 `IDPR_HF_HOME` 필수

## 8. 정책 (변경 불가)

* **sealed-59**: `kcl_criminal_r10_p1_q1_ga`와 `kcl_criminal_r14_p1_q2` 두 dev case만 열 수
  있다. 이번 축의 진단은 사례 본문을 한 번도 열지 않고 target metadata만으로 했다
* **프롬프트·정의 승인 게이트**: 활성 프롬프트와 정의 전문은 사용자 승인 후에만 설치한다
