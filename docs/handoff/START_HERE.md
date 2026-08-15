# 다음 세션 시작점

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00
검증: `570 passed, 16 skipped` (conda **base**, `/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q`)

## 한 줄 상태

**Phase A·B·C가 전부 닫혔다.** 다음 작업은 **전체 재생성 한 사이클**이고, 설계 결재가 남은
항목은 없다. 재생성 순서와 함정은 §4에 있다.

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

## 4. 다음 작업 — 전체 재생성 한 사이클

```text
Call 1 (1회)   ← 필수. offense 6개가 늘어 routing universe가 바뀌었다
→ Call 1.5 (1회)  ← 필수. binding 계약에 사실 3개가 늘었다
→ dependency ROUTE  ← 신규. linked_offender가 결박된 case에서만 돈다
→ deterministic planner
→ rule→target accounting
→ Call 2 (1회)
→ symbolic → AnswerPlan → Call 3
```

### 반드시 지킬 것

* **Call 1을 건너뛰지 마라.** 옛 router manifest는 이제 lineage 검증에서 실패하고 그것이
  의도된 동작이다(`tests/test_call1_catalog_lineage.py`). 재사용하면 존재하지 않던 죄로
  라우팅된 seed 위에 새 rulebase를 얹게 된다.
* **758 target은 invariant가 아니다.** offense 6개와 사실 3개가 늘었으므로 늘어나는 것이 정상.
* Call 2는 **마지막에 한 번만.**

### 착수 전에 해야 할 한 가지 — 체인에 단계가 빠져 있다

dependency ROUTE는 스크립트와 계약이 모두 있고 테스트도 있지만,
[`scripts/slurm/run_v2_axis_closure_e2e.sh`](../../scripts/slurm/run_v2_axis_closure_e2e.sh)에
**단계가 추가되어 있지 않다.** 넣지 않으면 제151조는 재생성을 돌려도 UNKNOWN 그대로다.

넣어야 할 자리와 흐름:

```text
planner 산출 (linked_offender_dependencies 포함)
→ scripts/run_v2_dependency_route.py
     --plan <planner 산출> --inventory data/inventory/kcl_criminal_v1_draft.jsonl
     --base-url ... --model ... --out <경로>
→ 산출물의 predicate_targets 를 Call 2에 태운다
→ linked_offender.article151_predecessor_status()
→ linked_offender.article151_status_truths()
→ symbolic 러너가 plan row의 `article151_status_truths`로 읽는다
```

마지막 줄은 이미 배선되어 있다(`scripts/run_v2_scallop_e2e.py`). 비어 있으면 아무 일도
하지 않으므로, 단계를 넣기 전에도 나머지 재생성은 정상으로 돈다 — 제151조만 닫히지 않는다.

---

## 5. 실행 환경 (변경 없음)

* pytest: conda **base** — `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기
* 긴 작업·GPU 작업은 **길이 무관 항상 sbatch**. nohup은 고아 프로세스가 된다
* sbatch에 `IDPR_HF_HOME` 필수. 안 넘기면 빈 홈캐시로 새서 job이 실패한다
* job 진행상황 백그라운드 폴링 금지
* 체인은 `IDPR_AXIS_SKIP`으로 이어 돌린다

## 6. 정본 artifact (직전 사이클 — 재생성하면 대체된다)

`experiments/v2_final_e2e_26/` · plan 758 target · Call 2 26/26 · Call 3 26/26
Call 3의 exit 2는 실패가 아니라 감사 게이트다.

## 7. 정책 (변경 불가)

* **sealed-59**: `kcl_criminal_r10_p1_q1_ga`와 `kcl_criminal_r14_p1_q2` 두 dev case만 열 수 있다.
  나머지 59건은 채점 전용. **sealed-59를 열어 UNKNOWN을 분류하지 않는다.**
* **프롬프트·정의 승인 게이트**: 활성 프롬프트와 정의 전문은 사용자 승인 후에만 설치한다.
* 새 정적 감사를 임의로 열지 않는다. 실제 E2E 결과에서 문제가 나온 지점만 본다.
