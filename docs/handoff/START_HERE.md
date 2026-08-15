# 다음 세션 시작점

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00
검증: `557 passed, 16 skipped` (conda **base**, `/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q`)

## 읽는 순서

1. **이 문서** — 지금 어디에 있고 다음에 뭘 하는가
2. [`PHASE_A12_DESIGN.md`](PHASE_A12_DESIGN.md) — **2026-08-15 결재된 A1·A2 계약과 시공 기록.**
   §1~§5는 결정 기록, §6이 A1의 남은 구조(ROUTE 재사용)다.
   승인 대기 중인 것: [`ROUTE_DEPENDENCY_PROMPT.md`](ROUTE_DEPENDENCY_PROMPT.md)(프롬프트),
   [`ARTICLE151_PENALTY_WORKSHEET.md`](ARTICLE151_PENALTY_WORKSHEET.md)(법률 검수).
3. [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) — 사용자 저작 지시서. §11-bis에 2026-08-15
   갱신(감사 시점에 보이지 않던 세 건)이 있다. B2·B3·B4는 닫혔고 A3·A4가 남았다.
4. [`AXIS_CLOSURE.md`](AXIS_CLOSURE.md) — 구조 감사의 정본. 맨 뒤
   「production E2E 관통 (2026-08-15 06:00)」 절이 최신 상태다.
5. [`CODEBASE_AUDIT.md`](CODEBASE_AUDIT.md) — 닫힌 pipeline 감사 10건. 참조용.
6. `NEXT_SESSION.md` — append-only 역사 로그. **그 안의 "다음 작업" 지시는 전부 만료**했다.

## 한 줄 상태

pipeline stage 간 연결 축은 닫혔다. production E2E가 Call 2 → Call 3까지 26/26 관통했고
경로 손실 0이다. 남은 위험은 **저작했다고 믿는 규칙이 실제 runtime에 존재하는가**로 이동했고,
그 감사가 `RULEBASE_AUDIT.md`다. **structural freeze는 그 문서의 Phase A를 닫은 뒤에 선언한다.**

## 닫힌 것 (다시 열지 말 것)

- 코드베이스 감사 10건 + 재검수 3+1건 — 커밋 `02f3253`…`64fecbf`
- P0-A external opener: doctrine 39/39 · participation mode 27/27 · candidate probe 4/4 asked
- participation TRUE relation 17건, active doctrine 5건 — downstream 경로 손실 0
- completion semantics — 법률 검수 완료. `attempted.when = commencement AND NOT(completion)`은
  **유지**한다(형법 제25조 제1항이 비기수성을 미수범 구성요건으로 규정). `commencement=TRUE +
  completion UNKNOWN` 16건은 결함이 아니라 정당한 3-valued unresolved state다.

## 다음 세션이 할 일

`RULEBASE_AUDIT.md` §9의 Phase A → B → C. 요약:

| | 항목 | 성격 | 직접 영향 사례 |
|---|---|---|---|
| A1 | 제151조 linked-liability route | 배선 + typed representation | `r10_p2_q2` |
| A2 | intended-object factual representation | 새 factual representation | `r10_p2_q1`, `r12_p2_q1_ga` 외 9 |
| A3 | 폭행죄 family 저작 | Definition Layer | `r11_p1_q1` |
| A4 | 장물죄 family 저작 | Definition Layer | `r10_p2_q1` |
| B1–B5 | single-source·checker·traversal hardening | 결정론적 | — |
| C | unsupported schema field fail-closed 처리 | 계약 | — |

A1은 이번 세션의 0-TRUE 감사에서 코드로 확인했다 — `resolve_article_151_liability()`는
[`statutory.py:42`](../../src/idpr/v2/runtime/statutory.py#L42)에 있는데 **레포 전체에 호출부가
없다**. 제263조 경로만 `orchestration.py`가 부른다. `data/v2/definitions/offenses.yaml`에
폭행죄·장물죄 family가 없는 것도 확인했다(A3·A4).

### 반드시 지킬 것

- **758 target을 invariant로 보지 않는다.** A2~A4가 들어가면 target universe가 바뀌는 것이
  정상이다. 변경을 전부 모은 뒤 **Call 2는 마지막에 한 번만** 돌린다.
- 특정 KCL 정답을 host heuristic으로 박아 넣지 않는다. 기존 DSL의 offense/derivation 구조로만
  처리한다.
- 순수 결정론적 hardening(B1·B2·B4)만으로는 neural 단계를 재실행하지 않는다. 새 offense family가
  Call 1 routing universe를 바꾸거나 새 factual identity가 Call 1.5 schema를 바꾸면 그
  upstream부터 재생성한다.

## 넘기지 않는 것 — 검수·미측정으로 남긴 항목

- `ground_fact.means_or_object_defect` — 45 asked / TRUE 1 · UNKNOWN 44 · **FALSE 0**.
  `legal_standard`가 없고 exclusion 둘이 흔한 TRUE·FALSE 경로를 각각 막는다. schema 위반은
  아니므로 **법률/definition authoring review**로 남긴다. 승인 없이 정의·프롬프트를 고치지 않았다.
- 나머지 0-TRUE predicate(`bribe_promise` 0/10, `dangerous_weapon_carriage`, `job_relatedness`)
  — 사실 부재냐 Call 2 판독 실패냐를 sealed-59 없이 가를 수 없다. **미측정**.
- `AXIS_CLOSURE.md` 「검수가 남은 항목」 5건 (상상적 경합 저작 0개 포함).

## 실행 환경

- pytest: conda **base** — `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기.
- 긴 작업·GPU 작업은 **길이 무관 항상 sbatch**. nohup은 고아 프로세스가 된다.
- sbatch에 `IDPR_HF_HOME` 필수. 안 넘기면 빈 홈캐시로 새서 job이 실패한다.
- 체인: [`scripts/slurm/run_v2_axis_closure_e2e.sh`](../../scripts/slurm/run_v2_axis_closure_e2e.sh)
  (9단계, `IDPR_AXIS_SKIP`으로 이어 돌린다). vLLM allocation 안에서 CPU job step으로 돈다.
- job 진행상황 백그라운드 폴링 금지.

## 정본 artifact

production E2E 루트: `experiments/v2_final_e2e_26/`

| 단계 | 경로 |
|---|---|
| plan (758 target) | `plan_doctrine/evaluation_instance_plan.jsonl` |
| Call 2 | `call2/grounding_output.jsonl` |
| symbolic | `scallop/results.jsonl` |
| AnswerPlan | `answer_plan/answer_plans.jsonl` |
| Call 3 | `call3/` |
| 체인 로그 | `chain.log` |

Call 1.5 binding 95 · action 215는 직전 정본 `experiments/v2_action_realization_26_e2e/`에서
그대로 입력으로 쓴다.

Call 3 단계가 exit 2로 끝난 것은 실패가 아니라 **감사 게이트**다 —
`required_final_conclusion_audit` 1건, `required_authority_audit` 2건 미충족을 fidelity 결함으로
보고한 것이고 답안은 26/26 생성되었다.

## 측정 유의점

- 동일 입력·동일 프롬프트에서도 Call 2 결과가 약 9% 흔들린다. 20~30건 규모 총계 변화는
  노이즈와 구분되지 않는다. 판단은 결정론적인 symbolic 출력으로 한다.
- 현재 76% unresolved와 rulebase coverage는 **별개 축**이다. 없는 offense family는 UNKNOWN을
  늘리는 게 아니라 평가할 branch 자체를 없애므로 UNKNOWN 통계 바깥에 있다.

## 정책 (변경 불가)

- **sealed-59**: `kcl_criminal_r10_p1_q1_ga`와 `kcl_criminal_r14_p1_q2` 두 dev case만 디버깅용으로
  열 수 있다. 나머지 59건은 채점 전용. 새 dev case는 사용자 명시 승인 필요.
  **sealed-59를 열어 UNKNOWN을 분류하지 않는다.**
- **프롬프트 승인 게이트**: 활성 프롬프트·정의 전문은 사용자 승인 후에만 설치·실험한다.
- 새 정적 감사를 임의로 열지 않는다. 실제 E2E 결과에서 문제가 나온 지점만 본다.
