# Current handoff

기준: 2026-08-08 · 브랜치 `deadline_v2_0808` · 데드라인 **2026-08-19 21:00**(1주 연장)

## Step 6C (Participation / Attribution) 완료 — 8차 addendum, `tests/test_v2_*.py` 총 228개 (2026-08-08, 새 세션)

v2.2.0 case-time runtime의 세 번째 단계를 끝냈다. **다음 세션 시작점은 Step 7(Closure / Probe
compiler)이다.** 승인된 계획서는
[`/home/jaehoonjeong/.claude/plans/linked-foraging-rivest.md`](file:///home/jaehoonjeong/.claude/plans/linked-foraging-rivest.md)
(ExitPlanMode 리뷰에서 2건 정정 후 승인 — 아래 "승인 시 정정" 절).

Definition Layer(스키마 + axis 5)는 이미 구축돼 있었다 — 이번 단계는 순수하게 runtime
(`src/idpr/v2/runtime/participation.py` 신규)이었고, 스키마는 발견된 공백 하나(아래)만 8차
addendum으로 메꿨다.

### 런타임 계약 — 사용자가 직접 확정한 4가지

1. **공동정범 ATTRIBUTE는 slot-scoped, predicate-level이다.** `attributable_slots`가 가리키는
   slot이 참조하는 leaf predicate ref만, 상대 공동정범의 truth와 `fold_any`(3치 OR)로 병합한다.
   slot-truth 통째 대입이 아니다 — ATTRIBUTE → Completion → Elements 순서(v2.2.0 §18)를 그대로
   유지하기 위해 predicate 층에서 처리.
2. **attribution은 새 `CaseTruths`를 만든다, 새 view 타입을 만들지 않는다.** `apply_attribution()`이
   `CaseTruths` → `CaseTruths`. `resolve_completion()`/`.predicate_view()` 시그니처 불변 — 원본은
   손대지 않는다.
3. **교사·방조는 정범의 `CompiledOffense`를 재평가하지 않는다.** accessory의 Elements =
   `principal_realization_truth(principal)`(3치) AND 자체 `requires`(8차 addendum). 그 이후
   (Unlawfulness→Culpability→Punishability)는 direct/co-principal 경로와 **완전히 동일한 코드**를
   재사용 — 별도 accessory engine 없음.
4. **`principal_dependency`는 정범의 기존 StageResult를 읽는 3치 판정**이지 새 예외 계층이 아니다.
   확정 존재→TRUE, 확정 불성립→FALSE, 정범 자체가 unresolved→UNKNOWN. §15.4의 "TYPE ERROR"는
   `requires_conclusion`이 이미 const로 고정돼 있어 저작 단계에서 구조적으로 불가능 — 런타임 대응
   불필요.

### 스키마 8차 addendum — `derivative_mode.requires` 신규, **필수**

`participation_policy_def.schema.json`의 `derivative_mode`(교사/방조)에 `basis`/`requires_conclusion`
뿐이고 교사·방조 **자신의** 요건(교사의 고의, 방조행위 존재 등)을 저작할 필드가 없었다 — 6C 설계
중 발견, SCHEMA_NOTES/양쪽 설계문서/CURRENT.md/fixture 어디에도 언급 없음을 확인 완료. `requires`
(element_expression)를 추가했고, `completion_policy_def.schema.json`의 `states.*.requires`와 달리
**필수**로 뒀다 — optional이면 교사/방조 mode가 `requires` 없이 저작 가능해지고, 그러면 런타임
Elements가 principal_realization_truth 하나만으로 satisfied가 되어 정범 성공 사실만으로 책임이
성립해버린다(§15.3의 derivative liability 취지 붕괴). 사용자가 계획서 검토 중 직접 지적해 확정.
상세 근거는 `SCHEMA_NOTES.md` 8차 수정 절.

### 승인 시 정정 (계획서 초안 2건, 사용자가 ExitPlanMode에서 지적)

1. **`LiabilityEvaluation.completion`을 `CompletionResult | None`으로.** 초안은 derivative 경로에서도
   `principal.completion`을 그대로 복제해 넣으려 했는데, 이건 accessory가 자기 completion 판단을
   가진 것처럼 기록을 왜곡한다 — derivative 경로는 Completion 자체를 거치지 않는다(결정 #3). →
   derivative 경로는 `completion=None`. 정범의 completion이 필요하면 `principal.completion`으로
   이미 접근 가능, 복제하지 않는다.
2. **`derivative_mode.requires`를 optional이 아니라 required로.** 위 8차 addendum 절 참고 — 사용자가
   초안 검토 중 직접 지적.

### 신규/변경 파일

- **`src/idpr/v2/runtime/participation.py`(신규)** — `apply_attribution`(ATTRIBUTE, co-principal),
  `principal_realization_truth`(3치 판정), `resolve_derivative_liability`(교사/방조).
  `resolve_derivative_liability`가 `pipeline.resolve_from_elements()`를 직접 재사용해 Unlawfulness
  이후를 재구현하지 않는다.
- **`src/idpr/v2/participation.py`(신규, Definition Layer)** — `participation_policy_for`
  (`completion_policy_for` 미러), `effective_attributable_slots`(`checks/participation.py`에
  inline돼 있던 로직을 승격 — Step 4가 `replay_slot`을 `compile.py`로 승격한 것과 같은 전례).
  `checks/participation.py`는 이제 이 함수를 호출하는 얇은 wrapper.
- `src/idpr/v2/expressions.py` — `canonical_leaf_refs`(canonical tuple form 전용 leaf walker,
  기존 `leaf_refs`는 raw dict form용 — `compiled.slots[...]`는 이미 canonical이라 attribution이
  기존 `leaf_refs`를 쓰면 항상 빈 집합을 얻는다).
- `src/idpr/v2/runtime/pipeline.py` — `resolve_liability`의 elements-gate-check 이후 전체를
  `resolve_from_elements(...)`로 추출(행위 변경 없음), `runtime/participation.py`가 두 번째
  호출자가 되므로 `ELEMENTS_STATE`/`ELEMENTS_GATE`/`decisive_obligation`을 공개로 승격(Step 5의
  `_fold_all → fold_all` 승격과 같은 전례). `_stopped`의 `completion` 파라미터도
  `CompletionResult | None`로 확장.
- `src/idpr/v2/runtime/stages.py` — `ParticipationDependencyObligation`/
  `ParticipationRequirementObligation` 신규(`Obligation` union에 편입, 3종 → 5종),
  `LiabilityEvaluation.completion`을 `CompletionResult | None`으로 확장.
- `src/idpr/v2/checks/references.py` — `_check_participation_policy` 신규(axis 1,
  `modes.{instigator,aider}.requires`의 leaf가 ground_fact/legal_element인지 검사, 기존
  `completion_policy`의 `states.*.requires` 패턴과 동일). `_HANDLERS`에 `participation_policy` 편입.
- fixture **43 → 45 인스턴스**: `ground_fact.instigation_conduct`/`ground_fact.aiding_conduct`
  신규 + `participation_policies.yaml`의 instigator/aider 양쪽에 `requires` 추가. 부정 케이스 1개
  추가(`requires` 없는 `derivative_mode` 거부 확인, `tests/test_v2_schema.py`).

### 검증

`tests/test_v2_runtime_participation.py`(20개) 신규 + 기존 208개 갱신
(`test_v2_runtime_stages.py`의 Obligation union 카운트 3→5, `test_v2_expressions.py`에
`canonical_leaf_refs` 4개, `test_v2_schema.py`에 8차 addendum 부정/긍정 케이스 2개, corpus 카운트
43→45 갱신 2곳) = **총 228개 전부 통과**(`/data5/jaehoonjeong/miniconda3/bin/python`, 미니콘다
base). 45개 인스턴스 corpus **8축 전부 0 findings**(`test_real_corpus_is_fully_type_clean`).

**mutation 검증 3건** — 각 버그를 되살렸을 때 해당 회귀 테스트가 실제로 실패함을 확인:
(a) `principal_realization_truth`를 항상 TRUE로 하드코딩 → 9개 테스트 실패(3치 판정 관련 전부),
(b) `apply_attribution`의 `fold_any`를 단순 override로 교체 → attribution end-to-end 테스트 2건
실패, (c) `derivative_mode.requires`를 스키마에서 다시 optional로 → 8차 addendum 부정 케이스
테스트 실패. 전부 확인 후 원상복구.

### 미해결 (의도적, 6C 범위 밖)

- **어느 actor가 어느 mode인지 결정하는 오케스트레이터는 만들지 않았다.** case 사실에서 "누가
  누구와 공동했는가/누가 누구를 교사했는가"를 판단하는 건 6A의 `ActiveDoctrineRefs`와 같은 이유로
  step 7/8(closure/probe)의 일 — 호출자가 명시 공급.
- **직접교사(간접정범 아님 — 교사자를 다시 교사)** 등 chained participation은 코드가 우연히
  허용하지만(`principal_realization_truth`가 `principal.completion is None`일 때도 폴백하도록
  설계됨) 명시적으로 테스트하지 않았다.

## Step 6B (Completion) 완료 — form 추상화 폐기, 7차 addendum, `tests/test_v2_*.py` 총 203개 (2026-08-08, 같은 세션)

**6B의 blocker였던 "form selection semantics"는 풀린 게 아니라 폐기됐다.** 사용자 결정으로
`FormProgram`/`OffenseFormKey` 추상화 자체를 걷어내고 Completion을 원안 구조로 되돌렸다. 승인된
계획서는
[`/home/jaehoonjeong/.claude/plans/wobbly-forging-hennessy.md`](file:///home/jaehoonjeong/.claude/plans/wobbly-forging-hennessy.md)
(ExitPlanMode 리뷰에서 2건 정정 후 승인 — 아래 "승인 시 정정" 절).

**이건 신규 설계가 아니라 원안 복귀다.** v2.1.0 §14.2가 이미
`CompletionResult { form: completed|attempted|...|unresolved, decisive_conditions, provenance }`
라는 **도출되는 typed legal result**로 쓰고 있었고, selectable-program 층은 그 위에 나중에
얹힌 것이었다. ~~다음 세션 시작점은 Step 6C(Participation / Attribution)다.~~ **6C도 같은
브랜치에서 완료됨 — 문서 최상단 "Step 6C 완료" 절 참고.**

### 왜 form 층이 unsound했는가 (재발굴 방지)

미수 program에는 결과·인과 obligation이 없으므로 **기수 사건에서도 attempt program이 통과한다.**
따라서 selection 규칙이 tie를 깨야 하는데, 자연스러운 규칙("completed 먼저 보고 실패하면
attempt")이 정확히 §14가 금지한 `기수 실패 → attempt 라벨 부착` 패턴이다. 즉 form selection은
어렵게 푸는 문제가 아니라 **만들지 말았어야 할 문제**였다.

대체 설계: 각 state가 **자기 도출조건 `when`을 저작**하고, 상태는 조건들의 **집합**에서 도출된다.

```text
T = { s : when_s = TRUE },  U = { s : when_s = UNKNOWN }

|T| == 1          →  그 s              (U 무관 — 확정이 미확정을 이긴다)
|T| >= 2          →  unresolved        (조건 중첩 = 저작 결함, provenance 기록, 승자 안 뽑음)
|T| == 0, U != ∅  →  unresolved
|T| == 0, U == ∅  →  not_applicable
```

`attempted.when`은 `completed`의 평가 *결과*를 읽지 않는다(둘 다 case truths만 본다) — fallback이
안 쓰이는 게 아니라 **표현 불가능**하다. 코드 어디에도 순서가 없고,
`test_derivation_is_symmetric_under_declaration_order`가 선언 순서 무관을 기계적으로 고정한다.

### 스키마 7차 addendum (`completion_policy_def.schema.json` 전면 개편)

`forms` → **`states`** 개칭(`attempt` → `attempted`). 개칭 이유는 스타일이 아니라 `form`이라는
단어가 남으면 "선택 가능한 프로그램 집합"이라는 폐기된 독법이 데이터에 살아남기 때문. 필드:

| 필드 | 의미 |
|---|---|
| `when`(신규, 필수) | 이 state의 도출조건. leaf는 ground_fact/legal_element뿐 — Completion이 Elements보다 **먼저** 오므로 slot 결과 참조는 순환. |
| `suspends`(신규) | 이 state에서 obligation이 *존재하지 않는* slot. fold에서 **제외**, TRUE 치환 아님. |
| `relations`(신규) | relation 처분 `{relation, left, right, path?, disposition}`. |
| `punishable`(기존) | 형태의 문제. Punishability stage의 EXEMPT(효과의 문제)와 별개. |
| `requires`(기존) | 이 state가 **추가**하는 obligation. |

**기존 description 두 문장이 실제로 모순이라 교정**: (1) `requires`의 `"in addition to — never
instead of — the base offense elements"`는 `suspends`와 정면 충돌, (2) `forms`의 "punishable:false
말고 키를 생략하라"는 이제 둘이 다른 뜻(키 생략 = 그 법적 상태 자체가 없음 / punishable:false =
도출되지만 불벌 → **Completion에서 즉시 종료**). 상세는 `SCHEMA_NOTES.md` 7차 수정 절.

### 승인 시 정정 (계획서 초안 2건, 사용자가 ExitPlanMode에서 지적)

1. **v2.1 `evaluate_compiled_offense`를 건드리지 않는다.** 초안은 여기에 keyword-only
   `suspended_slots`/`relation_dispositions`를 달려 했는데, 그러면 같은 의미론이 두 군데 생기고
   정의 층이 case-time 개념(completion state)을 알게 된다. → completion semantics는 runtime
   `_iter_obligations` **한 곳에만** 산다. 따라오는 결과: 6A의
   `test_elements_truth_matches_evaluate_compiled_offense`는 두 경로 fold 일치를 고정하는데
   suspension이 있으면 **의도적으로 달라진다** → `completed` 범위로 축소하고 "일반 불변식이
   아니다"를 docstring에 명시(조용히 삭제하지 않음).
2. **axis 8의 affectedness 자동 추론 폐기.** 초안의 leaf_refs 교집합 방식은 relation endpoint가
   Step 5에서 확정한 **relation-scoped view**라 leaf 집합과 대응 보장이 없다. → 규칙 단순화:
   `suspends`가 비면 처분 저작 불필요, 비어 있지 않으면 **그 offense의 relation instance 전건**에
   `retain|suspend` 명시. corpus가 bounded라 부담이 작고, 법적 판단을 사람이 했다는 증거가
   relation마다 남는다.

   정정 2가 옳았다는 실증이 fixture에 있다: **강도살인미수는 result+causation을 suspend하지만
   `occasion_identity`는 RETAIN이다**(강도의 기회에 살해행위가 있었을 것은 미수에서도 요구됨).
   자동 추론이었다면 정확히 반대 답을 냈다.

### 신규/변경 파일

- **`src/idpr/v2/runtime/completion.py`(신규)** — `CompletionState`(7치) /
  `CompletionCandidateOutcome`(§14.2 `decisive_conditions`) / `CompletionResult` /
  `resolve_completion` / `completion_policy_for`. `__post_init__` 불변식: 도출되지 않은
  state(`unresolved`/`not_applicable`)는 program(punishable·suspends·requires·dispositions)을
  **못 들고 다닌다**.
- **`src/idpr/v2/checks/completion.py`(신규, axis 8)** — 7축 → **8축**. Finding 9종. 유일하게
  남은 구조 탐지는 `completion_unsupported_slot_suspension`(suspended slot에 독립 복수 component
  contribution → **거부**, 강도강간미수 conduct가 그 사례)이고 그것도 아무것도 결정하지 않는다.
  일반 조건 중첩은 정적으로 판정 안 함(결정불가능) — 완전 동일 `when`만 잡고 나머지는 런타임
  `unresolved`.
- `runtime/identity.py` — `OffenseFormKey` **삭제**. 런타임 identity는
  `OffenseInstanceKey(case, actor, offense_ref, occurrence_id)` 하나뿐.
- `runtime/stages.py` — `FormProgram`/`completed_program()` 삭제,
  `FormRequirementObligation` → `CompletionRequirementObligation(state)`, 결론 3종 +
  `LiabilityEvaluation`의 `form_key` → `instance`, `LiabilityEvaluation.completion` 필드 추가
  (completion은 legal judgement이므로 trace에 남는다), `decisive_stage`에 `"completion"` 허용
  (단 `STAGE_NAMES`에는 없음 — Completion은 orthogonal axis이지 5번째 stage가 아님).
- `runtime/pipeline.py` — `program: FormProgram` → `completion: CompletionResult`,
  `_reject_unimplemented_form` 삭제, 진입 분기 3종(unresolved / not_applicable /
  `punishable is False` → 4 stage 전부 `not_reached`, `decisive_stage="completion"`).
- `checks/references.py` — `states.*.when` / `states.*.requires` / `relations[].relation` 참조 검사.
- fixture **36 → 43 인스턴스**: `offense.homicide` + `derived_offense.robbery_homicide`(강도살인,
  결합범이고 미수 명문 제342조 — 결과적가중범 `robbery_causing_injury`와 달리 미수가 인정되므로
  이쪽에 policy를 붙였다) + ground_fact 2 + legal_element 2 + completion_policy 2.

### 검증

`tests/test_v2_runtime_completion.py`(13) + `tests/test_v2_check_completion.py`(12) 신규 +
기존 178 갱신 = **총 203개 전부 통과**(`/data5/jaehoonjeong/miniconda3/bin/python`, 미니콘다
base). 43개 인스턴스 corpus **8축 전부 0 findings**.

**mutation 검증 3건** — 각 버그를 되살렸을 때 해당 회귀 테스트가 실제로 실패함을 확인:
(a) `|T|>=2`에 우선순위 tie-break 부활 → `test_two_true_conditions_yield_unresolved_never_a_priority_winner`
실패, (b) suspended slot을 TRUE 치환 →
`test_suspended_slot_is_dropped_from_the_fold_not_rewritten_to_true` 실패, (c) 미선언 relation을
조용한 `retain` 기본값으로 → axis 8 테스트 2건 실패.

폐기된 추상화를 검증하던 3개 테스트는 의도적으로 제거/교체했다(`OffenseFormKey` 래핑,
`FormProgram` 2건, `test_non_completed_form_program_is_rejected_until_6b` — 마지막 것은 6B가
실제 semantics를 넣었으므로 가드의 존재이유가 사라짐).

**무관한 기존 실패 1건**: `tests/test_property_rule_ir.py::test_scallop_golden_scenarios[theft]`.
v1 자산(`idpr.rulegen` + `scripts.*`)만 쓰고 `idpr.v2`를 import하지 않으며, `src/idpr/v2/` 밖에서
`idpr.v2`를 import하는 코드는 레포에 없다(grep 확인). 이번 변경과 무관하다고 판단하지만
**clean tree에서 직접 재현 확인은 못 했다**(스태시 후 재실행이 타임아웃).

### 6C 착수 시 주의

실행 순서는 그대로 `ATTRIBUTE → Completion → Elements`(v2.2.0 §18, pipeline docstring에 명시).
`resolve_completion(policy, compiled, instance, truths)` 시그니처가 이미 instance/truths를 받으므로
6C에서 attributed view를 넘기는 확장이 가능하다 — **지금 그 인자를 미리 달아두지 않았다**(6A 정정
#10과 같은 원칙: 받아놓고 무시하는 인자를 만들지 않는다).

### 미해결 (의도적, 6B 범위 밖)

- §14.2의 `applicable_effects`(미수 감경 등) — Open Question #5(양형 포함 범위) 미확정이라 지금
  필드를 만들면 죽은 필드가 된다. `punishability_note`(자유 텍스트)만 유지.
- **occurrence-scoped suspension** — `suspends`는 flattened slot 전체를 없앤다. COMPOSE의 한 slot에
  독립 복수 component가 기여하면(강도강간의 `conduct`) 지금은 axis 8이 **거부**한다. 강도강간미수를
  실제로 표현하려면 이 기능이 필요하고, 그때 별도 설계 대상이다.
- `when`의 착수 predicate가 `requires`에도 다시 나타나는 중복 — 런타임상 no-op이지만 구조적으로는
  옳다(`when`=도출조건, `requires`=그 상태의 obligation). fixture 주석에 근거를 남겼다.

## Step 6A (Runtime semantics) 완료 — v2.2.0 착수, `tests/test_v2_*.py` 총 178개 (2026-08-08, 새 세션)

v2.2.0 case-time runtime의 첫 단계를 끝냈다. **다음 세션 시작점은 Step 6B(Completion)이고, 착수
전에 닫아야 할 설계가 하나 남아 있다(아래 "6B 착수 전 blocker").** 승인된 계획서는
[`/home/jaehoonjeong/.claude/plans/radiant-doodling-flute.md`](file:///home/jaehoonjeong/.claude/plans/radiant-doodling-flute.md)
(사용자가 **5라운드**에 걸쳐 정정한 끝에 확정 — 아래 "설계 정정" 절이 그 기록).

**스키마 변경 없음.** `*.schema.json`을 하나도 건드리지 않았다. 6B가 필요로 하는 7차 addendum
(`completion_policy_def.schema.json`의 `suspends` / `relations`)은 **아직 저작하지 않았고 별도
승인 대상**이다.

### 단계 번호 재정의 (이전 문서의 "6·7·8"을 대체)

v2.1.0 26절의 6·7·8이 runtime semantics 하나의 umbrella로 묶였다. 이전 절들이 "Step 7"을 두 뜻
(Completion / closure·probe)으로 쓰고 있었으므로 여기서 통일한다:

```text
Step 6A  Runtime identity / truths / stages / effects   [완료]
Step 6B  Completion                                     [완료 — 문서 최상단 절 참고]
Step 6C  Participation / Attribution                    [완료 — 문서 최상단 절 참고]
Step 7   Closure / Probe compiler                       ← 다음 시작점
Step 8   Call 1 (router) 이후 뉴럴 단계
```

### 신규/변경 파일

- **`src/idpr/v2/runtime/`(신규 패키지)** — case-time 층. 층 방향 규칙: `runtime`이 `idpr.v2`를
  import하고 **역방향은 절대 없다**(`test_definition_layer_never_imports_the_runtime`이
  `src/idpr/v2/*.py`를 실제로 스캔해 기계적으로 강제).
  - `identity.py` — `OffenseInstanceKey(case, actor, offense_ref, occurrence_id)` /
    `OffenseFormKey(instance, form)` / `RuntimeRelationKey(instance, RelationInstanceKey)`.
  - `truths.py` — `CaseTruths` + lazy read-only view 2개. v2.1 함수가 지금 받는 타입 그대로 넘겨
    시그니처 변경을 피한다.
  - `stages.py` — state literal 4종 + `GateState` + `AppliedEffect` + `StageResult` +
    Obligation 3종 + `FormProgram` + 결론 3종 + `LiabilityEvaluation`.
  - `effects.py` — `ActiveDoctrineRefs` / `resolve_stage` / `StageEffectError`.
  - `pipeline.py` — `resolve_liability(...) -> LiabilityEvaluation`.
- `src/idpr/v2/evaluate.py` — `_fold_any` → 공개 `fold_any` 승격(로직 변경 없음). Step 5가
  `fold_all`을 승격한 것과 같은 근거: 3치 의미론의 소스는 이 파일 하나로 유지.

### 설계 정정 (사용자가 5라운드에 걸쳐 지적, 전부 반영 — 재발굴 방지용 기록)

1. **doctrine을 stage별 전역 pool로 소비하면 거의 모든 사건이 `unresolved`로 붕괴한다.** 초안은
   `registry.by_kind["doctrine"]`을 stage로만 필터해 전부 평가했는데, 절도 사건에서 정당방위·
   긴급피난·인적처벌면제까지 평가되고 미probe doctrine의 `requires`는 대부분 UNKNOWN이라
   Unlawfulness가 `unresolved`가 된다. → 런타임은 `ActiveDoctrineRefs`를 **받는다**(Step 7의
   closure가 생산할 자리; 6A에서는 호출자가 명시 공급). `DoctrineDef`를 `OffenseDef`에
   hard-link하지 않는 것과 case-time에 전부 평가하는 것은 **별개 문제**다.
2. **stage 상태는 doctrine 개별이 아니라 pool 전체의 fold다.** `self_defense=TRUE,
   necessity=UNKNOWN`이 `unresolved`가 되면 안 된다 — 확정된 DEFEAT는 다른 justification의
   미해결과 무관하게 stage를 종결시킨다. 정확히 3치 ANY라 `fold_any`를 재사용.
3. **`legal_state`와 `gate_state`는 다른 질문이다.** MODIFY가 UNKNOWN이면 실제 상태는
   "preserved 또는 diminished 중 모름"이지 `preserved`가 아니다 — `preserved`로 적으면 symbolic
   runtime이 실제보다 강한 법적 결론을 낸다. 반면 §13.2가 둘 다 establishment를 인정하므로
   gate는 통과한다. → 두 필드로 분리. DEFEAT/EXEMPT의 UNKNOWN은 결론을 바꾸므로 gate도 막는다.
4. **`StageResult`의 불변식은 타입이 아니라 `__post_init__`이 강제한다.** `S | None` 선언만으론
   `StageResult("evaluated", None, None)`이 그대로 생성돼 불변식이 주석으로만 남는다. 3항 동치
   (`not_reached ⇔ legal_state is None ⇔ gate_state is None`) + `not_reached`면 `effects=()`까지
   검사한다(도달 안 한 stage에 effect가 남으면 그건 hypothetical이고 v2.2.0 §24 위반).
5. **`form`을 `OffenseInstanceKey`에 넣으면 순환이 생긴다.** 미수 여부를 판단하려면 truths를 먼저
   읽어야 하는데 그 truths의 키에 이미 form이 들어 있게 된다. 같은 사실을 form별로 두 벌 저장하는
   문제도 있다. → **`OffenseInstanceKey`(사실 층) / `OffenseFormKey`(프로그램 선택 층) 2층 분리.**
   relation truth도 base instance에 붙는다(`causal_nexus` 성립 여부는 form과 무관한 명제이고,
   그 form이 그걸 요구하는지는 CompletionPolicy의 일).
6. **`occurrence_id`가 없으면 같은 사건·같은 actor·같은 죄종 두 번이 한 키로 충돌한다.**
   죄수론(Open Q #6) 이전에 case-time fact attribution 자체가 두 occurrence를 구별해야 한다.
7. **`decisive_element`는 relation 실패를 가리킬 수 없다.** predicate 전부 TRUE인데
   `causal_nexus`가 FALSE면 Elements는 failed인데 FALSE leaf가 없다. → `decisive_obligation`으로
   일반화. **단 `PredicateObligation(ref)`는 계산 불가능** — `NOT(A)` with `A=TRUE`,
   `ONE_OF(A,B)` with 둘 다 TRUE도 FALSE leaf 없이 FALSE다. `evaluate()`는 최종 TruthValue만
   반환하므로 pipeline이 tree를 다시 걷는 건 두 번째 evaluator이고 unsound. → 실제 union은
   `SlotObligation | RelationObligation | FormRequirementObligation`. predicate 수준 provenance가
   필요해지면 정식 `evaluate_with_trace()`를 따로 만든다.
8. **`OffenseRealization`을 실패한 경우에도 만들면 "실현되지 않은 실현"이 생긴다.** 이름이 곧 법적
   명제인 층에서 §4.5의 구분이 무너진다. → **evaluation trace와 legal conclusion을 타입으로 분리**:
   `LiabilityEvaluation`은 항상 존재하고, `OffenseRealization`/`OffenseEstablishment`/
   `LiabilityResult`는 각자의 gate가 실제로 통과했을 때만 생성된다. `decisive_stage`도
   `str | None`(완주한 path엔 결정적 실패 stage가 없음).
9. **`FormProgram`이 `CompletionPolicy.punishable`을 흘리면 법률지식이 컴파일에서 증발한다.**
   미수·예비 처벌규정 유무를 런타임이 나중에 다시 알아내야 한다. → 필드로 보존.
   **Punishability stage의 EXEMPT와 다른 것이다**: `punishable`은 이 미완성 *형태*가 애초에
   처벌 가능한 법적 형태인가(형태의 문제), EXEMPT는 성립한 죄에 면제가 있는가(효과의 문제).
10. **아직 구현 안 된 optional 인자를 미리 달지 않는다.** 초안은 `evaluate_compiled_offense`에
    `suspended_slots`/`relation_dispositions`를 6A에 달고 semantics는 6B에서 채우려 했는데, 그건
    "받아놓고 무시하는 인자"다. → **6A에서 그 함수를 아예 손대지 않고**, pipeline이 비-completed
    program을 `NotImplementedError`로 **거부**한다(무시 아님).

### 6B 착수 전 blocker — form *선택* 의미론이 아직 없다 [해소됨 — 문제 자체가 폐기]

> **이 절은 역사적 기록이다.** 아래에서 "6B 착수 전에 설계·승인받아야 한다"고 예고한 form
> selection semantics는 설계된 게 아니라 **폐기됐다** — `FormProgram`/`OffenseFormKey` 추상화를
> 걷어내니 문제가 함께 사라졌다. 문서 최상단 "Step 6B 완료" 절 참고. 아래 "relation은 slot
> topology에서 자동 유도하지 않는다"는 결론은 유효하지만, 그 구현 방식(affectedness 구조 탐지)은
> 더 단순한 규칙으로 대체됐다(`suspends`가 있으면 relation 전건 명시).

6A/계획서가 정의한 건 전부 `FormProgram` = **"이 form을 선택했다면 무엇을 평가하는가"**다.
**"어느 form을 선택하는가"는 미정이고, 이걸 닫기 전에 6B 구현에 들어가면 안 된다.**

문제가 드러나는 지점: 기수 사건에서도 attempt program이 통과한다(결과·인과 obligation이 없으므로).

```text
Form evaluation semantics   선택된 form에서 무엇을 평가하는가   [정의됨]
Form selection semantics    어느 form을 선택하는가              [미정]
```

`"completed 먼저 검사하고 실패하면 attempt"` 같은 순서를 런타임 코드에 숨기면 §14가 금지한
"기수 실패 → attempt 라벨 부착" 패턴이 구현 디테일로 되살아난다. 필요하면 `CompletionPolicyDef`가
priority / exclusion / guard를 **명시적으로 저작**해야 한다. → **6B는 `CompletionPolicy 7차
addendum + form selection`을 먼저 설계·승인받고 시작한다.**

또 6B 구현 시 확정된 것 두 가지(계획서에 상세):
- **relation은 slot topology에서 자동 유도하지 않는다.** compiler는 relation이 suspend된 obligation에
  영향받는지 **구조 탐지만** 하고, affected relation은 form policy가 `retain|suspend`를 명시하지
  않으면 컴파일/타입체크 실패(unaffected는 retain 기본). 결과범 미수에서 result만 suspend되는데
  `causal_nexus`는 사라져야 하므로 "양 endpoint suspended" 휴리스틱은 불건전. → axis 8
  `checks/completion_forms.py` 신설 예정(최종 acceptance는 7축이 아니라 **8축** 0 findings).
- **애매하면 조용히 실행하지 말고 거부한다.** suspended slot에 독립적인 복수 component
  contribution이 있어 전체 suspend를 안전하게 정당화 못 하면 unsupported Finding. 원칙 한 줄:
  컴파일러는 구조 탐지까지만 하고 법적 판단은 자동으로 하지 않는다.

### 병행 트랙 — Criminal-Law Definition Population (승인됨, 미착수)

계획서 Track 2가 승인됐다. 요지만(상세는 계획서):
- `card_catalog_v2.json` 1848장을 `function`×`form`으로 갈라 **저작 대상 ~496장**
  (canonical_element 201 / exception 197 / stage 77 / defeater 17 / participation 4, 전부
  abstract_rule), `application_standard`+`precedent_pattern` 729장은 새 predicate가 아니라
  `LegalElementDef.legal_standard` 본문 재료로 **흡수**, concurrence 136(죄수론)은 보류,
  narrative+skeleton_meta 360은 폐기.
- 카드 51개 조문은 전부 각칙이고 **총칙 카드는 0장**. 카드 공백 = KCL eval 공백이라 각칙 251조문
  전면 확장은 채점 신호를 늘리지 않는다. 구조 stress 유형은 art339(강도강간)만 결손.
- **형소(5,373 chunk)는 범위 밖** — 시간이 아니라 스키마 부재(v2 stage 대수가 실체법 전용).
- 실적재는 `data/v2/definitions/`에 두고 `docs/contracts/v2/examples/`(스키마 fixture 36개)는
  동결. `load_definitions(definitions_dir=...)`가 이미 파라미터화돼 있어 loader 신규 구현 불필요.
- 저작은 predicate-first 2패스, **검수 게이트는 predicate 사전 먼저**.

### 검증

`tests/test_v2_runtime_{identity,truths,stages,effects,pipeline}.py` 47개 신규 + 기존 131개 =
**총 178개 전부 통과**(`/data5/jaehoonjeong/miniconda3/bin/python`, 미니콘다 base). 기존 131개
무회귀가 "v2.1 public behavior에 breaking change 없음"의 실증이다.

위 정정 중 7건은 **mutation 검증**도 했다 — 각 버그를 코드에 일부러 되살렸을 때 해당 회귀
테스트가 실제로 실패하는 것을 확인(정정 1·2·3·4·7·8·10). `test_elements_truth_matches_evaluate_compiled_offense`는
intent×relation 9조합 전부에서 v2.1 `evaluate_compiled_offense`와 일치함을 확인해, 의무별 개별
평가가 두 번째 의미론이 아니라 decisive obligation 지목용일 뿐임을 고정한다.

## Step 5 (Relation evaluator) 완료 — v2.1.0 실행 의미론 종료, `tests/test_v2_*.py` 총 131개 (2026-08-08, 같은 세션)

26절 구현 순서 5번 "Relation evaluator"를 끝냈다. **이로써 v2.1.0 트랙이 끝난다 — 다음 세션
시작점은 6번 "Runtime stage objects"이고, 그 지점부터 v2.2.0(case-time runtime)이다.** 승인된
구현 계획서는
[`/home/jaehoonjeong/.claude/plans/resilient-stirring-pancake.md`](file:///home/jaehoonjeong/.claude/plans/resilient-stirring-pancake.md)
(사용자가 4라운드에 걸쳐 정정·조건부 승인한 끝에 확정).

**스키마 변경 있음(6차 addendum)** — Step 2에서 "DEFERRED BY DESIGN"으로 유예했던
relation 타입 검증을 이번에 닫았다. 상세 근거는
[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)의
"Step 5(Relation evaluator) 착수 시 스키마 수정 (6차 수정)" 절.

### 사용자가 확정한 Step 5의 경계 — v2.1과 v2.2가 갈리는 지점

Step 5는 좁은 relation lookup 하나로 끝나지 않는다. **v2.1.0이 완결되어야 하는 것은
"truth value가 주어지면 끝까지 실행 가능한 typed legal program"이다**:

```text
predicate truths + relation truths + CompiledOffense  →  TRUE / FALSE / UNKNOWN
```

그 truths 자체를 사건에서 *생산*하는 것(structural relation을 CaseGraph에서 resolve,
evaluative relation을 neural assessment로 라우팅)과 actor/offense별 stage 결과로 조직하는 것이
v2.2.0이다. 그래서 `ElementsState`/`OffenseRealization` 같은 stage object는 **의도적으로 만들지
않았다** — `relations.py`는 bare `TruthValue`만 반환한다.

### 핵심 설계 결정: semantic type을 정의 객체가 아니라 relation binding이 선언한다

Step 2/Step 4가 두 번 "vocabulary가 없어서 못 한다"고 미뤘던 relation lowering인데, 실제로
부족했던 건 vocabulary가 아니라 **타입을 어디에 붙일지에 대한 모델**이었다. 기존 fixture 두
개가 "정의 객체당 고정 타입 하나" 설계를 바로 반증한다 — 같은 `offense.robbery`가
`causal_nexus`에서는 **event**로, `occasion_identity`에서는 **conduct**로 쓰이고 둘 다 법적으로
옳다(인과관계는 사건 사이, 기회의 동일성은 행위 사이). → `relation_binding`이
`left_view`/`right_view`를 명시적으로 저작하고, structured(offense)는 relation-scoped
projection으로, atomic(ground_fact/legal_element)은 자기 `semantic_sort`로 검사한다. 상세는
SCHEMA_NOTES 6차 addendum. `semantic_types: [conduct, event]`처럼 집합을 주는 대안은 타입
시스템을 약화시켜서(무엇이든 통과) 사용자가 명시적으로 기각했다.

### 신규/변경 파일

- **`src/idpr/v2/checks/relation_types.py`(신규, axis 7)** — relation lowering.
  endpoint마다 **두 조건을 독립적으로** 검사(한쪽 통과가 다른 쪽을 면제하지 않음):
  (A) `binding.left_view == RelationDef.left_type`, (B) 그 endpoint가 실제로 그 view를 제공
  가능한가. Finding 코드 3개: `relation_view_type_mismatch`,
  `relation_view_unsupported_by_component_kind`, `relation_endpoint_untyped`.
  `checks/__init__.py`의 `run_type_checks`에 7번째 축으로 편입(6축 → 7축).
- **`src/idpr/v2/relations.py`(신규)** — `RelationInstanceKey`, `iter_relation_instances`,
  `evaluate_relation`, `evaluate_compiled_offense`.
- `src/idpr/v2/compile.py` — `CompiledRelationBinding`에 `left_view`/`right_view` 추가(계산
  없이 통과) + 방어적 `relation_binding_missing_view` Finding.
- `src/idpr/v2/evaluate.py` — `_fold_all` → 공개 `fold_all`(로직 변경 없음).

### 설계 정정 (사용자가 ExitPlanMode 리뷰에서 지적, 전부 반영 — 재발굴 방지용 기록)

1. **`None = permissive` typing은 lowering contract 위반이었다.** 초안은 leaf-kind
   (primitive/exported_component/bundle)에 "검사할 typing이 없으면 통과"를 뒀는데, 이건 위
   조건 (B)를 통째로 포기하는 것 — `exported_component + view="whatever"`가 PASS가 된다.
   → atomic predicate에 `semantic_sort`를 도입해 실제로 검사하고, 선언이 없으면 통과가 아니라
   `relation_endpoint_untyped`로 **보고**한다. 회귀 테스트:
   `test_atomic_endpoint_without_semantic_sort_is_untyped_not_silently_accepted`.
2. **relation truth 키가 nested 재사용에서 충돌했다(실제 버그).** 초안 키는
   `(defining offense id, relation, left local_key, right local_key)`였는데, 같은 `DerivedX`를
   한 COMPOSE 안에서 `left_x`/`right_x` 두 번 쓰면 두 occurrence의 내부 relation이 **같은 키로
   붕괴**한다 — 공급된 truth 하나가 두 occurrence 모두를 대답해버린다. Step 4가 local_key
   occurrence를 그렇게 공들여 보존한 걸 Step 5에서 되잃는 셈. → `RelationInstanceKey`에
   **전체 occurrence path**(top-level id + 거쳐온 local_key 연쇄)를 넣었다. 회귀 테스트:
   `test_same_definition_reused_under_two_local_keys_gets_two_distinct_keys`.
   (이 path는 **definition-occurrence identity 전용**이다 — case/actor namespacing은 Step 6+.)
3. **nested offense를 통째로 재평가하면 slots 이중 평가.** `D2 = COMPOSE(D1, C)` 컴파일 후
   `D2.slots`는 이미 `D1.slots`를 흡수했으므로 nested를 `evaluate_compiled_offense`로 다시
   부르면 그 slots를 두 번 본다(3치 ALL이 idempotent라 값은 안 틀리지만 구조가 틀림). 잃으면
   안 되는 건 nested의 **relation obligation**이지 slots가 아니었다. → **slots는 top-level에서
   한 번, relations만 재귀**. 회귀 테스트:
   `test_slots_are_evaluated_exactly_once_never_again_per_nested_component`.
4. **compile 실패 entry는 skip(중복 diagnostics 방지).** axis 7이 compile findings를 다시
   forward하면 axis 2(operators)와 같은 진단이 `run_type_checks()` 출력에 두 번 뜬다. compile
   실패의 소유권은 compiler/operator axis에 남긴다. 회귀 테스트:
   `test_compile_failure_is_skipped_not_re_reported`.
5. **`compile_offense()`의 standalone crash-safety를 새 필드에도 유지.** view 누락 시 `KeyError`가
   아니라 Finding + 전체 엔트리 무효화(Step 4의 "성공한 CompiledOffense는 절대 부분적이지
   않음" 불변식 그대로 확장). 회귀 테스트:
   `test_relation_binding_missing_view_returns_findings_not_raise`.
6. **3치 ALL fold를 복제하지 않는다.** `evaluate.py`의 `_fold_all`을 공개 `fold_all`로 승격해
   `evaluate()`와 `evaluate_compiled_offense()`가 공유 — `evaluate.py`가 3치 Boolean semantics의
   유일한 소스로 남는다.

### 용어 경계 (모듈 docstring에도 명시)

`evaluate_relation()`은 "이 사건에서 causal_nexus가 성립하는가"를 **계산하지 않는다** — 이미
공급된 relation truth를 lookup할 뿐이고, 없으면 `UNKNOWN`(4.3 invariant). 실제 판정은 v2.2.0
(structural은 CaseGraph resolve, evaluative는 neural assessment).

### Step 6(v2.2.0) 착수 방향 — runtime identity는 기존 키를 뜯어고치는 게 아니라 한 층 위에 씌운다

Step 5가 남긴 identity 경계를 Step 6 시작 전에 명시적으로 못박아둔다:

```text
v2.1 RelationInstanceKey
    = definition occurrence identity          (top-level offense id + local_key 연쇄)

v2.2 Runtime identity
    = case / actor / offense-instance namespace
      + definition occurrence identity        (위 키를 그대로 품는다)
```

즉 Step 6에서 `RelationInstanceKey`를 **수정하지 말 것** — 이 키는 "이 정의 트리 안의 어느
relation occurrence인가"라는 질문에 이미 정확히 답하고 있고, 그 답은 사건이 무엇이든 변하지
않는다. 사건마다 달라지는 건 "누구에 대해, 어느 offense instance에 대해 이 정의를 적용하는가"
이므로, runtime 키는 `(case, actor, offense_instance) + RelationInstanceKey` 형태로 **감싸는**
방향이 맞다. 지금 키에 case/actor 필드를 끼워넣으면 definition layer가 case를 알게 되어
v2.1/v2.2 분리가 그 지점에서 깨진다.

`tests/test_v2_check_relation_types.py`(10개) + `tests/test_v2_relations.py`(15개) +
`test_v2_compile.py` 2개 추가 = 기존 104 + 27 → **총 131개 전부 통과**
(`/data5/jaehoonjeong/miniconda3/bin/python`, 미니콘다 base 환경). 실제 36개 인스턴스 corpus는
7축 전부 0 findings. 위 정정 1~3은 **mutation 검증**도 했다 — 각 버그를 코드에 일부러 되살렸을
때 해당 회귀 테스트가 실제로 실패하는 것을 확인(테스트가 형식만 갖춘 게 아님).

## Step 4 (QUALIFY / COMPOSE compiler) 완료 — `src/idpr/v2/compile.py` + 12개 테스트 통과, `tests/test_v2_*.py` 총 104개 (2026-08-08, 같은 세션)

26절 구현 순서 4번 "QUALIFY / COMPOSE compiler"를 끝냈다. ~~다음 세션 시작점은 이제 5번
"Relation evaluator"다.~~ **5번도 같은 세션에서 완료됨 — 문서 최상단 "Step 5 완료" 절 참고.**
승인된 구현 계획서는
[`/home/jaehoonjeong/.claude/plans/curious-meandering-unicorn.md`](file:///home/jaehoonjeong/.claude/plans/curious-meandering-unicorn.md)
(사용자가 4라운드에 걸쳐 정정한 끝에 확정 — 아래 "설계 정정" 절 참고).

**스키마 변경 없음** — `*.schema.json`을 건드리지 않았다. `SCHEMA_NOTES.md`는 Step 2 완료 시점의
"compiler/relation evaluator(4/5) 설계 시점에 다시 열 것"이라는 표기만 "5(Relation evaluator)
설계 시점에 다시 열 것"으로 갱신(4번은 끝났고 다시 열지 않기로 확정했으므로) — 아래 참고.

### 핵심 발견: Type checker의 `replay_slot`은 검증 전용이었지, 공개 컴파일 산출물이 아니었다

axis 2(`checks/operators.py`)는 이미 QUALIFY/COMPOSE의 slot 값을 authored data로부터 재귀
계산하는 `replay_slot`을 갖고 있었지만, 이건 "저장된 `flattened_elements`가 맞는지 검증"만 하는
내부 헬퍼였다. 반면 COMPOSE의 `derivation.relations`(local_key로 두 컴포넌트를 잇는 배열)는
axis 1(`checks/references.py`)이 구조(local_key 존재/self-loop 금지)만 확인할 뿐, 그 local_key가
실제로 "무엇"을 가리키는지 resolve하는 코드는 어디에도 없었다 — 이게 이번 단계의 진짜 신규
작업이었다.

### `src/idpr/v2/compile.py` (신규 모듈)

`replay_slot`류 로직 전체를 `checks/operators.py`에서 옮겨와 `compile_offense(registry, ref) ->
CompiledOffense | list[Finding] | DerivationCycle | None`로 공개했다. `checks/operators.py`는
이제 이 함수를 호출해 `flattened_elements`와 비교만 하는 얇은 wrapper로 축소됨(Finding 코드/
조건은 기존과 동일 — 기존 92개 테스트가 전부 그대로 통과해 무회귀를 확인했다).

산출물 타입 3개:
- `CompiledComponentInstance{local_key, component_kind, resolved_kind, source_ref,
  compiled_content}` — COMPOSE의 컴포넌트 한 occurrence.
- `CompiledRelationBinding{relation_ref, left, right}` — `left`/`right`가 global ref가 아니라
  위 instance 객체 자체를 가리킨다.
- `CompiledOffense{id, slots, components, relations}` — `slots`만으로 완결되지 않는다: `CompiledOffense
  = Slots + Required Relation Bindings`, 절대 `Slots`만으로 취급하지 말 것(dataclass docstring에
  못박음, 나중에 runtime 코드가 `.relations`를 조용히 무시하는 걸 방지하려는 목적).

### 설계 정정 (사용자가 ExitPlanMode 리뷰에서 4라운드에 걸쳐 지적, 전부 반영 완료)

1. **local_key를 곧바로 global ref로 축약하면 안 됨.** local_key는 "이 composition 안의 특정
   component *occurrence*"를 식별하려고 만든 것 — 같은 ref(예: `offense.robbery`)가 서로 다른
   local_key로 두 번 들어와도 컴파일러가 이를 하나로 collapse하면 relation이 다시 구분 불가능해
   진다. → `CompiledComponentInstance`가 local_key당 하나씩 독립 생성되고, relation binding도
   instance 객체 자체를 참조(global ref 비교 아님). 회귀 테스트:
   `test_duplicate_ref_different_local_keys_stay_distinct_instances`.
2. **저작 시점 컴포넌트 범주(`component.kind`)와 실제 resolve된 정의 객체 kind를 섞지 않음.**
   `component_kind="offense"`가 실제로는 `OffenseDef` 또는 `DerivedOffenseDef` 둘 중 하나로
   resolve될 수 있으므로 `resolved_kind` 필드로 분리. 회귀 테스트:
   `test_component_kind_vs_resolved_kind_and_nested_compose_not_flattened`(중첩 COMPOSE가 부모
   레벨로 flatten되지 않는 것도 같은 테스트에서 확인).
3. **성공한 `CompiledOffense`는 절대 부분적이지 않음.** 컴포넌트/relation binding 하나라도
   실패하면 전체 엔트리가 `list[Finding]`(또는 cycle이면 `DerivationCycle`)을 반환 — "일부
   slot만 비고 나머지는 정상" 같은 반쯤 유효한 산출물은 없음. `Finding`/`DerivationCycle`은
   `CompiledComponentInstance.compiled_content` 안에 절대 들어가지 않음. 회귀 테스트:
   `test_one_broken_component_fails_the_whole_entry_never_a_partial_compiled_offense`.
4. **bundle-kind 컴포넌트가 relation의 endpoint여도 컴파일 단계에서 거부하지 않음.**
   `RelationDef.left_type`/`right_type`이 실제로 bound된 endpoint와 맞는지 검사하는 "relation
   lowering"은 3계층 분리(Compiler → Type checking/lowering → Relation evaluator)의 2번째
   층이며, 이번 단계 스코프가 아니다 — 여전히 어떤 컴포넌트도 그 필드와 비교할 semantic type을
   선언하지 않으므로(vocabulary 자체가 없음) **Step 5(Relation evaluator)로 명시적 재이관**.
   회귀 테스트: `test_bundle_as_relation_endpoint_compiles_without_type_validation`.
5. **방어적 체크 2개 추가**(compile.py가 axis 1 없이 단독 호출될 수 있으므로): (a) 같은
   local_key가 두 번 쓰이면 조용히 덮어쓰지 않고 `Finding("duplicate_local_key", ...)`, (b)
   `relation_ref`가 존재하고 `RelationDef`로 resolve되는지 구조적으로만 확인(타입 호환성 아님)
   하고 아니면 `Finding("relation_ref_unresolved", ...)`. 회귀 테스트:
   `test_duplicate_local_key_is_rejected_not_silently_overwritten`,
   `test_relation_ref_must_resolve_to_a_relation`,
   `test_malformed_relation_binding_returns_findings_not_raise`.

### 3계층 분리 (Step 5 경계 — 재발굴 방지용으로 명시적으로 기록)

1. **Compiler(이번 단계, 완료)**: local_key → `CompiledComponentInstance` 보존. 거부 없음.
2. **Type checking / relation lowering(스코프 아님, 아직 미착수)**: `RelationDef.left_type`/
   `right_type`이 실제로 bound된 endpoint의 kind와 맞는지 검사 — semantic type vocabulary가
   아직 없어서 못 함.
3. **Relation evaluator(Step 5)**: 실제 relation semantics 수행.

`tests/test_v2_compile.py`(12개 테스트, `/data5/jaehoonjeong/miniconda3/bin/python` 미니콘다
base 환경) + 기존 92개 = `tests/test_v2_*.py` 총 **104개 전부 통과**.

## Step 3 (Expression evaluator) 완료 — `src/idpr/v2/evaluate.py` + 23개 테스트 통과 (2026-08-08, 같은 세션)

26절 구현 순서 3번 "Expression evaluator"를 끝냈다. **다음 세션 시작점은 이제 4번
"QUALIFY / COMPOSE compiler"다.** 승인된 구현 계획서는
[`/home/jaehoonjeong/.claude/plans/polished-conjuring-turing.md`](file:///home/jaehoonjeong/.claude/plans/polished-conjuring-turing.md).

**스키마 변경 없음** — step 2(5차 addendum)와 달리 이번 단계는 `element_expression`
문법을 건드리지 않았다. `SCHEMA_NOTES.md` 업데이트 없음.

`src/idpr/v2/evaluate.py`: `TruthValue = Literal["TRUE","FALSE","UNKNOWN"]` +
`evaluate(expr: CanonicalExpr, truths: Mapping[str, TruthValue]) -> TruthValue`.
`expressions.py`의 `CanonicalExpr`(step 2에서 이미 구현된 canonicalize 출력)를 그대로
입력으로 받는다 — 두 번째 tree-walker를 새로 만들지 않고 step 2가 이미 세운 계약
(`replay_slot`이 `CanonicalExpr`를 반환, `check_operators`가 비교 전 `canonicalize` 호출)을
재사용. `None`(빈 slot) → `TRUE`(vacuous truth), 누락된 ref → `UNKNOWN`(4.3 invariant —
missing evidence is not negation). ALL/ANY/NOT은 v2.2.0 문서 12절의 3치 진리표를 그대로
구현.

**ONE_OF의 3치 의미론 — 문서에 없어 이번에 확정한 설계 결정** (v2.1.0/v2.2.0 어디에도
ONE_OF의 truth table이 없음, 사용자에게 명시적으로 질의 후 확정):

```text
true_count = TRUE인 자식 수
unknown_count = UNKNOWN인 자식 수

true_count >= 2      → FALSE   (이미 2개 이상 참이면 어떤 completion으로도 못 고침)
unknown_count == 0   → true_count == 1이면 TRUE, 아니면 FALSE
그 외                 → UNKNOWN
```

ALL/ANY/NOT과 동일한 원리("모든 completion에서 같은 결론이면 확정, 아니면 UNKNOWN")를
ONE_OF의 "정확히 하나"(8.3절) 명제에 그대로 적용한 것 — "자식 중 UNKNOWN이 하나라도 있으면
무조건 UNKNOWN"이라는 더 무딘 규칙보다 정밀함(예: `ONE_OF(TRUE, TRUE, UNKNOWN)`은 이미 2개
참이라 세 번째 값과 무관하게 `FALSE`로 확정).

**중요한 경계 — truth-functional, leaf-joint 아님**: 이 completion은 각 자식의 *이미
평가된* `TruthValue`에 대한 completion이지, 그 자식들이 참조하는 leaf ref 자체에 대한 joint
completion이 아니다. `evaluate()`는 각 자식을 독립적으로 평가한 뒤 그 결과값만 보고 fold한다
— 형제 자식들이 같은 leaf ref를 공유하는지 들여다보지 않는다(ALL/ANY/NOT도 동일한 원칙).
결과: `ONE_OF(A, NOT(A))`에서 `A = UNKNOWN`이면 `UNKNOWN`으로 평가된다(leaf-joint 분석을
했다면 `A`의 모든 completion에서 `A`/`NOT(A)` 중 정확히 하나가 참이므로 `TRUE`라고 판단했을
것과 다름). 사용자가 직접 지정한 경계이며, `test_v2_evaluate.py::
test_one_of_is_truth_functional_not_leaf_joint`로 회귀 고정.

`tests/test_v2_evaluate.py`(23개 테스트, `/data5/jaehoonjeong/miniconda3/bin/python`
미니콘다 base 환경) — ALL/ANY/NOT 진리표, ONE_OF 6가지 조합 + 계획서의
`ONE_OF(A, ONE_OF(B,C))` vs `ONE_OF(A,B,C)` 반례를 evaluation 레벨에서 재확인, 위 경계
회귀 테스트, 누락 ref 기본값, 빈 slot vacuous truth, `canonicalize`의 ALL/ANY flatten이
evaluate 결과를 바꾸지 않음(flatten-safety), nested mixed-operator 통합 테스트. 전체
`tests/test_v2_*.py` 92개 전부 통과(기존 69 + 신규 23).

## Step 2 (Type checker) 완료 — 스키마 addendum 5차 수정 + `src/idpr/v2/` 구현 + 69개 테스트 통과 (2026-08-08, 같은 세션)

26절 구현 순서 2번 "Type checker"를 끝냈다. **다음 세션 시작점은 이제 3번
"Expression evaluator"다.** 승인된 구현 계획서는
[`/home/jaehoonjeong/.claude/plans/modular-seeking-glade.md`](file:///home/jaehoonjeong/.claude/plans/modular-seeking-glade.md)
(총 6라운드 조건부 승인 끝에 확정), 스키마 근거는
[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)의
"Type checker 설계 중 발견된 추가 스키마 결함" 절.

### 스키마 addendum (Phase 0, 5차 수정)

Type checker 설계를 시작하자마자 스키마 자체에 5개 결함이 더 있다는 게
드러나 5라운드 재검토 끝에 확정, 전부 반영·재검증 완료(36개 인스턴스 그대로,
부정 케이스 11개 신규 확인):

- `component_ref`에 composition-local `local_key` 필수 추가, `slot`(단수,
  primitive/exported_component)과 `placement`(맵, bundle — 여러 predicate를
  여러 slot에 나눠 붙일 수 있어야 하므로)를 kind별로 분리.
- `compose.relations`를 bare id 배열에서 `[{relation, left, right}]`(left/right는
  `local_key`)로 재구성 — 어떤 두 컴포넌트를 잇는 relation인지 이제 명시적.
- `OffenseDef.element_modules`를 `[{ref, placement}]`로 재정의 — bare id
  목록(죽은 metadata)이 아니라 실제 실행 의미를 갖는 attachment로.
- `ExportedComponentDef`는 `source_offense.exports[export_key]`로 완전히
  resolve 가능함을 재확인(compiler-only 아님) — Type checker가 이걸 활용하는
  공용 `resolve_export` 리졸버를 `registry.py`에 둔다.
- `element_expression` leaf 허용 kind(`ground_fact|legal_element`만)와
  `LegalElementDef.grounded_by` 허용 kind(`ground_fact`만)를 미검증
  allowance 제거로 축소.

### `src/idpr/v2/` 구현 (Phase 1)

`schema.py`(referencing.Registry 기반 구조 검증), `expressions.py`(element_expression
tree walk + canonicalize/combine_all), `registry.py`(스키마 검증 + id 인덱스 +
`resolve_export`), `findings.py`(`Finding`/`TypeCheckError`), `checks/`
아래 6개 축(`references`/`operators`/`stage_effect`/`exports`/`participation`/
`derivation`). `tests/test_v2_*.py` 9개 파일, **69개 테스트 전부 통과**
(미니콘다 base 환경, `/data5/jaehoonjeong/miniconda3/bin/python` — `.venv`
아님). 실제 36개 인스턴스 corpus는 6축 전부 0 findings.

axis 2(operator typing)의 핵심 불변식: `flattened_elements`는 최종
top-level 비교(`check_operators`의 actual side, `operators.py` 단 한 줄)에서만
읽고, 다른 entry의 기대값을 계산할 때는 (그 entry가 `DerivedOffenseDef`이더라도)
항상 그 entry 자신의 `derivation`을 재귀적으로 다시 replay(`replay_slot`,
memoized + cycle-safe)한다 — 계획서 라운드 4/5/6이 이 지점의 실수를 세 번
교정했고, 구현 중 `grep flattened_elements src/idpr/v2/`로 재확인함(읽는
곳은 `operators.py`의 actual-side 한 줄과 `references.py`가 그 필드 자체의
참조 무결성을 구조적으로 검사하는 한 곳, 총 두 곳뿐 — 후자는 axis1의
독립적인 관심사라 불변식 위반이 아님).

**구현 중 실제로 잡힌 버그**: COMPOSE의 `kind=primitive` 컴포넌트를 replay할
때 처음엔 `PrimitiveDef` 자신의 id를 그대로 leaf ref로 썼는데, 실제로는 그
`PrimitiveDef.ref`(감싸고 있는 실제 predicate)로 resolve해야 했다 — 스키마
상으로는 멀쩡하지만 실행 의미가 틀린 전형적 사례, Type checker가 정확히
이런 걸 compiler 이전에 잡으려고 존재하는 단계라는 걸 보여주는 사례.

### DEFERRED BY DESIGN (버그 아님, 의도적 유예 — 나중에 재발견하지 말 것)

- **`RelationDef.left_type`/`right_type` ↔ bound component의 semantic type
  일치 검증** — `local_key` 덕분에 relation이 "어느 두 컴포넌트를 잇는지"는
  이제 정확히 알지만, 어느 component(`GroundFactDef`/`OffenseDef`/
  `ExportedComponentDef` 등)도 `RelationDef.left_type`/`right_type`과 비교할
  semantic type 자체를 선언하지 않는다. → ~~2026-08-08 Step 4 완료 시점에 재확인: 여전히 못
  함(vocabulary 부재), relation evaluator(26절 순서 5)로 재이관 확정.~~ **종료됨 — 2026-08-08
  Step 5에서 닫혔다. 부족했던 건 vocabulary가 아니라 "타입을 어디에 붙일지"였다(정의 객체가
  아니라 relation binding이 선언): 문서 최상단 "Step 5 완료" 절 + SCHEMA_NOTES 6차 addendum
  참고. 이 항목은 더 이상 열린 유예가 아니다.**
- **`modifier_ref` → 실제 `ModifierDef` 존재 확인** — `ModifierDef` 객체
  자체가 아직 설계되지 않았음(Open Question #4, v2.1.0 문서 25절). 지금은
  `modifier_ref` 재사용 시 stage 일관성만 self-consistency로 검사. →
  **`ModifierDef` 설계 시점에 다시 열 것.**

이 둘은 스키마 결함이 아니라 "아직 그 대상 객체/타입 vocabulary가 존재하지
않아서" 생기는 자연스러운 경계다.

## Step 1 스키마 재검토 반영 완료 — 4개 수정 + 3개 확정 + fixture 26→36개 (2026-08-08, 새 세션)

사용자가 `SCHEMA_NOTES.md`를 검토하고 Type checker(2번) 착수 전에 고칠 지점을
지적 — 전부 반영 완료, 재검증 통과. 상세 근거는
[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)의
"2026-08-08 재검토" 절.

- **수정 1**: `ParticipationPolicyDef`를 offense-keyed(`{id, offense, modes}`)에서
  shared/global(`{id, modes}`)로 바꿈 — 공범론은 범죄마다 반복 연결하는 게 아니라
  General Part로 공유. offense별 제한이 필요할 때만
  `OffenseDef.participation_constraints`(옵션)로 좁게 override. 또한
  `derivative_mode.requires_conclusion`을 자유 enum(3택1)에서
  `offense_realization` const로 고정 — 15.3의 typed dependency 불변식을
  type checker가 아니라 definition language 자체에서 틀리게 쓸 수 없게 함.
- **수정 2**: `MODIFY.modification`(자유 문자열) → `modifier_ref`(symbolic id) +
  `note`(설명, 런타임 비소비)로 분리. 자유 문자열 MODIFY는 symbolic runtime이
  해석 불가능해서 effect algebra의 목적 자체를 깼기 때문.
- **수정 3**: `ExportedComponentDef.resolved_ref` 필드 완전 제거 — 이건
  `DerivedOffenseDef.flattened_elements`와 같은 성격의 컴파일러 캐시라 Definition
  YAML에 사람이 손으로 쓰면 두 번째 진실 소스가 생김. Compiled IR(step 4) 전용.
- **수정 4**: `OffenseDef.composition_metadata` 필드 제거 — 컴파일러 미존재,
  fixture 어디에도 안 쓰임, placeholder를 스키마에 남겨둘 이유 없음.
- **확정 A**: `element_expression`은 canonical schema에서 이미 문법이 하나뿐임을
  재확인(flat-list "implicit ALL"은 JSON Schema branch가 아니라 저작 단계
  normalize로만 처리하기로).
- **확정 B**: 전체 13개 스키마 파일의 `$id`/`$ref`를 `idpr/v2/<Name>`에서
  `https://schemas.idpr.local/v2/<Name>` absolute URI로 전환.
- **확정 C**: `authority_basis` enum은 provisional 유지 — compiler semantics에
  영향을 주게 되는 순간 별도 설계 절을 먼저 연다는 원칙만 기록, 스키마 변경 없음.
- **fixture**: section 20.1(진정신분범, `offense.bribery_taking`)과
  20.4(composite offense + statutory nexus, `derived_offense.robbery_rape` +
  `relation.occasion_identity`)를 신규 추가. MODIFY의 새 모양을 실제로
  exercising하는 `doctrine.diminished_capacity`도 추가(이전엔 MODIFY fixture가
  전무했음). 결과 26 → **36개 인스턴스**, 검증 통과. 부정 케이스도 3개 →
  **8개**로 확장(새 필드 모양들이 실제로 옛 값을 거부하는지 확인).

## Step 1 (Definition schema) 완료 — JSON Schema 12개 + YAML fixture 26개 검증 통과 (2026-08-08, 같은 세션)

26절 구현 순서 1번 "Definition schema"를 끝냈다. **다음 세션 시작점은 이제 2번
"Type checker"다.**

- `docs/contracts/v2/common.schema.json` + Definition Layer 객체별 스키마 12개
  (`ground_fact_def`/`legal_element_def`/`primitive_def`/`element_bundle_def`/
  `exported_component_def`/`offense_def`/`derived_offense_def`/`doctrine_def`/
  `qualifier_def`/`relation_def`/`completion_policy_def`/`participation_policy_def`
  `.schema.json`) 작성 완료. JSON Schema(draft 2020-12)로 구조 검증, `$id`
  기준 cross-file `$ref`.
- 사람이 직접 저작하는 정의 파일은 **YAML**(사용자 결정) — 스키마 파일 자체는
  JSON Schema 그대로.
- `docs/contracts/v2/examples/*.yaml` 12개 파일·26개 인스턴스로 `jsonschema`
  검증 통과. section 20 validation case 중 20.2(부진정신분범)/20.3(결과적
  가중범)/20.5(미수범)/20.6·20.7(공동정범·교사범)을 실제 fixture로 exercising.
  부정 케이스 3개(v1식 `role`/`card_role` 필드 삽입, DoctrineDef stage/effect.stage
  불일치)도 실제로 거부되는 것 확인 — 특히 `role: "bar"`를 아무 v2 스키마에
  넣어도 `additionalProperties: false`가 구조적으로 막는다는 게 핵심 검증
  포인트(v1 극성 버그 재발 방지가 이번 개편의 목적이었으므로).
- 문서에 문법이 없어 이번에 확정한 판단 8가지(`PrimitiveDef`/`ExportedComponentDef`/
  `ParticipationPolicyDef` 모양, `element_expression`을 모든 요건 자리에 통일해서
  쓰기로 한 것 등) 전부 **[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)에
  근거와 함께 기록**. ~~다음 세션 시작 전에 검토할 것.~~ **이 검토는 끝났다 —
  위 "Step 1 스키마 재검토 반영 완료" 절 참고. `SCHEMA_NOTES.md`는 더 이상
  열린 검토 대상이 아니라 확정된 기록.**

### 다음 세션 시작점 — Type checker (26절 2번) [완료됨 — 위 "Step 2 완료" 절 참고]

**이 절은 역사적 기록이다. 여기서 예고한 Type checker는 같은 세션 안에서
바로 이어서 구현 완료됨 — 다음 세션 시작점은 이제 3번 Expression evaluator
(문서 최상단 절 참고).**

`docs/contracts/v2/*.schema.json`이 잡아주는 건 **구조(모양)뿐**이다. 아직
검증되지 않은 것: 15.4가 요구하는 typed dependency 체크("교사는
`OffenseRealization<X>`을 요구하는데 실제로는 `ElementsResult<X>`만 있으면
TYPE ERROR" — participation_policy_def.schema.json이 `requires_conclusion`을
`offense_realization` const로 고정해뒀지만, 실제 사건에서 정범이 도달한 게
`OffenseRealization`인지 아닌지 판정하는 건 여전히 type checker의 일), `NOT`이
unresolved/missing evidence를 satisfaction으로 바꾸지 않는다는 4.3의 invariant,
id 참조 무결성(예: `OffenseDef.qualifiers`에 적힌 id가 실제 존재하는
`QualifierDef`인지, `ExportedComponentDef.export_key`가 `source_offense`의
`exports` 맵에 실제 존재하는지 등) 등 — 전부 구조 스키마가 아니라 별도 Python
코드가 담당해야 하는 **의미 타입체크**다. `src/idpr/v2/`(신규 패키지, v1
코드는 그대로 둔다) 아래에 구현할 것으로 예상. **스키마 재검토가 끝났으므로
다음 세션은 SCHEMA_NOTES.md를 다시 검토할 필요 없이 바로 Type checker 설계에
착수하면 된다.**

## v2 킥오프 — v1 동결, DSL 대개편 착수 (2026-08-08, 새 세션)

**사용자 결정: v1(article/unit-centric RuleIR)을 reproducible baseline으로 동결하고,
`deadline_v2_0808` 브랜치에서 v2 DSL로 대대적 개편을 시작한다.** 데드라인이 8/11에서
8/19 21:00으로 1주 늘어난 게 계기. 핵심은 v1에서 반복적으로 터진 문제(이 문서 아카이브본
전체가 그 기록이다) 하나하나를 땜질하는 대신, 애초에 그런 버그가 나올 수 없는 **규격화된
형법 DSL**을 만드는 것.

### 브랜치/커밋 상태

- `main`이 `antigravity-0804`를 fast-forward merge해 `0268635`를 가리킴 — v1의 최종
  상태(assess 프롬프트 극성 버그 A+B+C 수정 + homicide art250_sec1_15 카드 role 정정까지
  전부 포함).
- `deadline_v2_0808`는 그 `main`(`0268635`)에서 분기. 지금부터 이 브랜치가 v2 작업 공간.
- `antigravity-0804` 로컬 브랜치는 아직 정리 안 됨(main과 동일 커밋이라 그대로 둬도 무해).
- v1의 이전 `CURRENT.md`(1442줄, 극성 버그 포렌식·라우팅 버그 해결·judge 재설계 등 전체
  경위)는 [`docs/archive/history/2026-08-08_v1_final_handoff_pre_v2_dsl.md`](../archive/history/2026-08-08_v1_final_handoff_pre_v2_dsl.md)에
  그대로 보존. **v1 관련 세부 경위가 필요하면 이 파일을 볼 것 — 지금부터 이 CURRENT.md는
  v2 전용으로 리셋한다.**

### v2 설계 문서 — 필독

- [`docs/v2_plan/IDPR_v2.1.0_DESIGN_PROPOSAL.md`](../v2_plan/IDPR_v2.1.0_DESIGN_PROPOSAL.md)
  — **지금 볼 문서.** Definition Language → Typed Legal IR → Scallop → Case Runtime
  4단 분리, canonical positive predicate, `bar`/`waiver`/`boundary`/`component` 같은
  neural-visible legal-effect role 전면 폐기, `QUALIFY`/`COMPOSE`/`PROJECT` definition-time
  constructor, `DEFEAT`/`MODIFY`/`EXEMPT`/`ATTRIBUTE` runtime effect, Completion/Participation을
  orthogonal runtime axis로 분리하는 게 골자.
- [`docs/v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md`](../v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md)
  — **지금 착수 안 함.** v2.1.0이 정한 typed legal program을 사건에 적용하는 3-call
  runtime(Call1 high-recall routing → Call2 GroundFact grounding → Call3 LegalElement
  assessment → lean symbolic execution). v2.1.0 freeze 이후에 다시 열 것.

핵심 원칙 한 문장(v2.1.0 문서 그대로): **"Neural models may ground facts and evaluative
legal elements. They may not assign legal effects."** — v1에서 반복된 극성 버그(카드
role이 neural assessment에 노출되며 판단이 뒤집히는 문제, 이번 세션 직전까지 homicide/
obstruction/harboring_offender 등에서 손으로 하나씩 잡던 바로 그 패턴)의 근본 원인을
아키텍처 레벨에서 차단하려는 설계다.

### 구현 순서 (26절) — 1~5번 완료(v2.1.0 종료), 지금은 6번부터(v2.2.0 시작)

v2.1.0 문서 26절 "Proposed Implementation Boundary"의 권장 순서를 그대로 따른다.
**1~5번 완료 — 위 "Step 5 완료"~"Step 1 완료" 절과 `docs/contracts/v2/SCHEMA_NOTES.md` 참고.
5번에서 v2.1.0 트랙이 끝났고(주어진 truth value로 끝까지 실행 가능한 typed legal program),
6번부터는 v2.2.0 case-time runtime이다 — 착수 전
[`docs/v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md`](../v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md)를
다시 열 것.**

```text
1. Definition schema   [완료]
2. Type checker         [완료]
3. Expression evaluator [완료]
4. QUALIFY / COMPOSE compiler   [완료]
5. Relation evaluator   [완료]  ← 여기까지 v2.1.0
6. Runtime stage objects   [완료 — Step 6A]  (여기부터 v2.2.0)
7. Completion resolution   [= Step 6B, 완료]
8. Participation / attribution   [= Step 6C, 완료]
9. Scallop compilation
10. Neural grounding adapters
11. Writer integration
```

**주의**: 위 26절 원본 번호는 이제 문서 최상단의 6A/6B/6C · Step 7(closure·probe) · Step 8(Call 1)
체계로 대체됐다. 6·7·8이 runtime semantics 하나로 묶였고, "Step 7"이라는 이름은 이제
closure/probe compiler를 뜻한다 — 이 표의 7번(Completion)과 혼동하지 말 것.

**1번 "Definition schema"의 구체 내용**: 22절 "Proposed v2.1.0 Object Inventory"에 나열된
Definition Layer 객체들(`GroundFactDef`, `LegalElementDef`, `PrimitiveDef`,
`ElementBundleDef`, `ExportedComponentDef`, `OffenseDef`, `DerivedOffenseDef`,
`DoctrineDef<S>`, `QualifierDef`, `RelationDef<A,B>`, `CompletionPolicyDef`,
`ParticipationPolicyDef`)의 실제 JSON/YAML 문법을 확정하는 게 첫 작업 — 25절 "Open
Questions After v2.1.0"의 1번("각 schema의 실제 JSON/YAML 문법")과 정확히 같은 항목.
6~8절(Fixed Offense Slots, Shared Element Modules, Element Expression Grammar)과 9절
(QUALIFY/COMPOSE/PROJECT)의 구조를 스키마로 얼마나 정확히 반영하는지가 이후 type
checker/compiler 단계 전체의 기반이 된다.

**착수 전 참고**:
- 24절 "Acceptance Criteria for v2.1.0 Freeze"가 이 트랙 전체의 완료 기준. 스키마
  설계 단계에서부터 이 기준(특히 "Type system"·"Predicate semantics" 항목)을 염두에
  둘 것.
- 21절 "Migration Principles from v1" — v1 카드를 그대로 v2 predicate로 옮기지 않는다.
  `v1 cards → semantic normalization → GroundFactDef/LegalElementDef/DoctrineDef/
  RelationDef → deduplication → shared predicate registry → OffenseDef assembly` 순서를
  지킬 것. 특히 `component`/`bar`/`waiver`/`boundary` role은 v2에서 neural-visible
  semantics로 유지하지 않는다 — 각 카드의 실제 법적 의미를 normalized predicate/element
  module/doctrine/qualifier/relation/completion condition/participation condition/
  punishability effect/post-offense relation 중 하나로 재분류해야 한다.
- v1의 실제 자산(RuleIR unit, norm card set, 승인 원장 등)은 `main`/`antigravity-0804`
  (`0268635`)와 이 브랜치 양쪽에 그대로 남아 있다 — migration 원료로 참고하되, 구조를
  그대로 이식하지 않는다.
- v1 아키텍처 문서(`docs/handoff/DESIGN.md`, `docs/handoff/RECOVERY.md`,
  `docs/handoff/RULEIR_RISKS.md`)는 article/unit-centric RuleIR 시절 기록이라 v2
  설계와 전제가 다르다. 참고는 가능하지만 v2 스키마 설계의 근거로 직접 인용하지 말 것.

### 미해결 (v2.1.0 문서 25절, 설계 진행하며 순차 확정)

스키마 문법(위 1번)을 제외한 나머지 11개는 이후 단계에서 확정한다: `ElementAssessment`
status representation, probability 도입 layer, `MODIFY` payload taxonomy, 양형 포함
범위, 죄수론/post-offense relation algebra, 대향범·집합범·합동범 actor-structure,
상습범·포괄일죄 연결, 예비·음모 CompletionPolicy, 판례/법률 reference authority schema,
routing activation scope 단위, alternative legal trace 포함 여부, 개별 조문·doctrine
법률 검수. **프롬프트 승인 게이트는 v2에서도 동일하게 적용** — 특히 향후 neural grounding
adapter(v2.2.0 대상) 프롬프트는 설치 전 사용자 승인 필요.
