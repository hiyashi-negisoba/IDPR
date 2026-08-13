# V2 restart — next session entry point

기준: 2026-08-12, commit 전 working tree checkpoint.

## 최신 checkpoint — Call 1.5-P 이후 1~4번 정상화 완료

아래의 과거 checkpoint보다 이 절과 각 experiment audit가 우선한다. 기존 Call 1/1.5/2
prompt는 변경하지 않았다.

- canonical factual binding: safely bound 56/74, general Call 2 531 target. Cartesian
  4,998 대비 89%대 감소를 유지한다.
- participation: necessary-counterpart gate 후 49 target. 동일 logical route의
  instigation/aiding 동시 TRUE는 `CONFLICTING_PARTICIPATION_MODE`다.
- conflict isolation: 사건 전체 skip을 제거했다. `r12_p2_q1_ga`의 participation 8개만
  quarantine하고 base liability 6개를 보존하여 26/26 Scallop이 실행된다.
- participation universe reviewed positive coverage는 13/23이다. 누락 10개는 binding 4,
  Call 1.5-P omission 3, cross-offense 2, composite 1로 ownership을 분리했으며 host repair하지
  않았다.
- indirect principal: offline gold participant 없이 Call 1.5-P 요청 span과 Call 1.5
  actor-action span의 overlap으로 candidate를 연다. 전체 1 candidate, job 222907 live request
  2회. `r14_p1_q3` direction TRUE, utilized predicates 6 UNKNOWN, dependency UNKNOWN이다.
- completion: extortion과 quasi robbery policy를 추가했다. mixed direct COMPOSE의 명시된
  offense-family component suspension을 runtime/checker/planner/Scallop에 일관되게 일반화했다.
  `r13_p1_q1` 甲 준강도는 attempted, 공갈은 근거 없는 completed에서 unresolved가 됐다.
- 최신 Scallop: `experiments/v2_call15_directscope_26_causal/scallop_v9_completion_normalized/results.jsonl`.
- audits: `participation_call2_v2/qualitative_audit.md`,
  `participation_universe_coverage_audit.md`, `completion_normalization_audit.md`.
- verification: **178 passed, 16 skipped**, focused Ruff, `git diff --check` 통과.

다음 작업은 기존 5번 doctrine activation과 6번 absorption/competition을 하나의 symbolic
최종책임 단계로 처리하는 것이다. 그 뒤 Call 3를 시작하기 전에 사용자에게 별도 Call 3
prompt 설계 스펙을 요청한다.

## 최신 checkpoint — Call 1.5 v8 / evidence-gated derived materialization

- Call 1.5 v8: 26/26 contract-valid, direct bindings 74, model 재호출 없음.
- production planner는 base-only closure expansion을 금지한다. Derived candidate는 registry의
  `candidate_materialization`에 저술된 둘 이상의 same-episode typed binding 조합 또는
  same-episode distinct-actor peer binding이 있을 때만 생성한다.
- zero-binding case는 더 이상 planner를 중단하지 않고 각 빈 seed를 `UNBOUND_SEED`로 보존한다.
  host가 neural binding을 합성하지 않는다.
- v8 planner: direct 74 + derived physical 5 = top-level/assessment 79, Call 2 neural target 475,
  relation 13, `UNBOUND_SEED` 52. 26/26 reproducibility audit errors 0.
- Call 1 gold survivor: direct 48/74, evidence-gated derived 후 51/74. Closure-only gold는
  3/17 복구했고, 생성 unique 3/physical 5 모두 rubric case/ref 범위 안이다.
- historical Cartesian baseline 대비 top-level 815→79(90.3% 감소), assessment 849→79
  (90.7% 감소), neural 4,998→475(90.5% 감소).
- artifacts:
  `experiments/v2_call15_fullcase_26_v8/evaluation_instance_plan.jsonl`,
  `evaluation_instance_plan.audit.json`, `derived_materialization_audit.{json,md}`.
- 검증: 전체 local `151 passed, 16 skipped`; focused Ruff와 `git diff --check` 통과.

## 한 줄 상태

G0 rollback, 26문항 수동 GOLD occurrence, Call 1, occurrence-aware planner와 Call 2의
predicate/relation/Article263 경계는 유지한다. participation을
`local typed relation -> deterministic host dependency compiler`로 구현했고 synthetic,
real-Gemma gate, partial smoke까지 통과했지만, full에서 occurrence fragment와 legal
realization node가 일치하지 않는 계약 문제가 드러났다. 동시에 Gemma가 명시된 exact-offense
경계를 대규모 후보 universe에서 안정적으로 지키지 못했다. participation 계약과 prompt는
이 상태로 동결했다. production acceptance는 계속 실패지만, 별도 degraded diagnostic
경로로 raw full Call 2를 끝까지 기록하고 유효한 17개 case의 Scallop과 Call 3까지 실행했다.
그 뒤 rubric-supervised normalization으로 Article263 transport를 회귀 고정하고,
question-assumption carrier, KCL completion policy 8개, decisive-predicate partial gold audit까지
구현했다. IssuePlanner/AnswerPlan과 Call 3는 아직 건드리지 않는다.

## 고정된 파이프라인과 범위

```text
Case -> Call 1 routing -> Step 7
     -> manual GOLD factual occurrence
     -> occurrence-aware planner
     -> Call 2 predicate / relation / participation / Article263
     -> CaseTruths -> Scallop -> Call 3
```

- Call 수는 3회다. Call 2 내부 physical shard 수는 별도다.
- Call 2 predicate truth, DSL, Scallop semantics는 이번 작업에서 바꾸지 않았다.
- GOLD에는 actor, factual occurrence, source span/text만 있다. 죄명, predicate truth,
  participation role, 기수, 법률 결론은 없다.
- Gemma participation request는 exact offense의 local typed relation 하나만 보고
  `TRUE | FALSE | UNKNOWN` 하나만 반환한다.
- Gemma edge 방향은 사실상 행위 방향이고, host edge 방향은 legal dependency 방향이다.
- co-principal은 edge가 아니라 group node다.
- host는 missing/extra/duplicate, 복수 derivative role, co/derivative 충돌, self-loop,
  dangling endpoint, cycle을 hard-fail하며 repair/tie-break하지 않는다.
- UNKNOWN은 FALSE로 바꾸지 않는다. raw assessment에는 보존하고 positive participation
  fact를 생성하지 않는다.

## 완료 및 검증 evidence

- `data/v2/gold_occurrences.jsonl`: 26문항, 67 occurrences.
- `data/v2/gold_article263_pairs.jsonl`: caller binding 1 pair.
- Call 1 실제 Gemma: 26/26 성공, Step 7 closure recall 74/86 (86.05%).
- Call 1 artifact: `experiments/v2_restart_rebuild/call1/router_output.jsonl`.
- 최신 planner: `experiments/v2_restart_rebuild/evaluation_instance_plan.jsonl`.
- 최신 planner audit: 26/26, errors 0, collision 0.
- latest planner cardinality: top-level 815, assessment instance 849, semantic predicate 5,838,
  neural predicate request 4,998, relation 423, participation local target 5,859.
- focused participation synthetic: 14 passed. direct root + instigation/aiding chain,
  multi-level DAG, co-group, self-loop, 2/3-cycle, dangling, duplicate role, overlap을 포함한다.
- 전체 로컬 suite: `93 passed, 6 skipped`.
- real-Gemma semantic gate: 6 tests passed. 내부 participation 요청은 forward/reverse
  instigation, aiding exclusivity, co-principal positive/negative, unrelated offense,
  base-only evidence의 derived-offense negative를 포함한다.
- `call2_smoke_local_typed_v4`: 26/26 생성 및 audit 성공. 96 physical requests,
  predicate 77, relation 47, participation 48, audit errors 0.
- 최신 전체 로컬 회귀검증: `119 passed, 13 skipped`.

## 현재 구현

- core: `src/idpr/v2/runtime/participation_grounding.py`
  - `ParticipationLocalTarget(kind, members)`
  - `ParticipationLocalAssessment(target, truth)`
  - `participation_local_targets(...)`
  - 정확히 한 target의 payload/schema/validator
  - `compile_participation_bindings(...)`
- planner/runner/audit/Scallop adapter는 `participation_local_targets`와
  `participation_local_assessments` 형식으로 맞췄다.
- prompt는 사건별 반례나 few-shot 없이 일반 typed-relation 규칙만 가진다.
- aiding은 principal의 독립적 선행 범의 이후 실행 원조로 한정해 instigation과의 정의
  중첩을 제거했다.
- derived offense는 base offense 관계를 자동 전이하지 않는 exact-offense scope rule을
  명시했다.

## full에서 확인된 실패와 진단

### full v1

`experiments/v2_restart_rebuild/call2_full_local_typed_v1`은 artifact를 완성하지 못했다.
`kcl_criminal_r11_p1_q1`에서 unrelated occurrence 관계를
`derived_offense.aggravated_injury` instigation으로 여러 개 TRUE 판정해 동일 accessory의
복수 derivative relation으로 host가 reject했다.

### full v2

`experiments/v2_restart_rebuild/call2_full_local_typed_v2`도 artifact를 완성하지 못했다.
같은 사건의 `derived_offense.nighttime_dwelling_theft`에서 다음이 함께 나타났다.

- 甲의 한 교사 occurrence가 乙의 계획, 침입, 취거 occurrence 각각을 principal로 TRUE.
- 乙의 한 교사 occurrence가 丙의 절도 망보기와 무관한 공갈 occurrence를 모두 principal로
  TRUE.
- 무관한 rape/bribery/dereliction 등 여러 offense에도 participation TRUE가 발생.
- case 전체 participation truth 분포는 TRUE 58, FALSE 1,493, UNKNOWN 321이었고,
  첫 multiple-derivative invariant에서 hard failure했다.

여기에는 서로 다른 두 원인이 있다.

1. **계약 문제:** factual occurrence는 한 offense realization의 계획·실행 조각일 수 있다.
   하나의 factual action edge가 동일 principal actor의 여러 occurrence fragment와 TRUE가
   되어도 현재 compiler는 서로 다른 legal principal instance로 본다. 어느 fragment가
   legal realization node인지 local truth만으로 결정할 수 없다.
2. **모델 한계:** exact-offense boundary를 일반 규칙과 live negative gate로 명시해도,
   5,859개 전체 후보에서는 Gemma가 행위 관계를 무관 offense로 전이했다. 여기서 사건별
   문구나 few-shot을 추가하는 것은 overfitting이므로 중단했다.

## 동결 후 degraded diagnostic 실행

production hard-fail은 그대로 유지했다. 별도 opt-in diagnostic mode만 추가하여 compiler가
거부한 case를 repair하거나 direct route로 바꾸지 않고 `REJECTED`로 보존했다.

- Call 2: `experiments/v2_restart_rebuild/call2_full_local_typed_diagnostic_v3`
  - 26 cases, predicate 5,182, relation 423, participation 5,859.
  - physical requests 6,184, exact correspondence audit errors 0.
  - participation truth: TRUE 175, FALSE 4,368, UNKNOWN 1,316.
  - valid 17 cases, rejected 9 cases.
  - rejection: cycle 2, multiple derivative 4, overlapping co-group 1,
    co/derivative conflict 2.
- Scallop: `experiments/v2_restart_rebuild/scallop_local_typed_diagnostic_v3/results.jsonl`
  - 17 cases executed, 9 cases `SKIPPED_REJECTED_PARTICIPATION`.
  - 213 liability traces, 8 established, derivative links 11, co sources 0.
- symbolic rubric proxy:
  `experiments/v2_restart_rebuild/scallop_local_typed_diagnostic_v3/rubric_proxy_audit.json`
  - established 8, rubric candidate scope 밖 1, outside rate 12.5%.
  - rejected participation 9개는 명시적으로 skipped.
- Call 3: `experiments/v2_restart_rebuild/call3_local_typed_diagnostic_v3/answers.jsonl`
  - valid 17 cases, 17 physical requests, total tokens 57,378.
  - rejected 9 case ID는 manifest에 남고 Call 3 입력에서 제외됐다.
  - content audit에서 1개 답안이 금지된 내부명 `occurrence_id`, `elements_state`를 노출했다.
- full-rubric Sonnet judge는 실행하지 않았다. 17개 답안과 전체 rubric을 외부 API로
  전송하는 작업은 별도 사용자 승인이 필요하다는 보안 차단이 걸렸다.

이 diagnostic 결과는 pipeline 후단 관찰용이며 production acceptance evidence가 아니다.

## 보존하되 승인하지 않는 실패 artifact

- 기존 `call2_full`, `call2_full_v3`, `call2_full_v4`, `call2_smoke_v5`는 이전 계약 실패
  분석용이다.
- `call2_full_local_typed_v1`, `call2_full_local_typed_v2`는 runner가 case-level hard
  failure 전에 중단했으므로 완성된 grounding artifact가 아니다.
- `call2_smoke_local_typed_v4`는 partial structural evidence일 뿐 Scallop 입력이 아니다.
- `call2_full_local_typed_diagnostic_v3` 및 그 Scallop/Call 3 결과는 degraded diagnostic이며
  production artifact가 아니다.
- 위 결과를 Scallop/Call 3 acceptance evidence로 사용하지 않는다.

## rubric-supervised failure debug

KCL rubric을 runtime input이나 prompt few-shot으로 사용하지 않고, 26-case offline
supervision으로 Call 2 이후 failure ownership을 추적했다. LLM judge는 사용하지 않았다.

- report: `docs/analysis/V2_RUBRIC_SUPERVISED_FAILURE_DEBUG.md`
- evidence JSON/Markdown:
  `experiments/v2_restart_rebuild/rubric_supervision_debug_v1/evidence_packet.*`
- reproducible builder: `scripts/build_v2_rubric_supervision_debug.py`
- rubric 735 atoms, conclusion-like 222.
- reviewed issue ref 86개 중 74개만 planner/Call 2에 도달했고 12개는 upstream miss.
- reached gold refs의 predicate도 TRUE 187 / FALSE 8 / UNKNOWN 985로 UNKNOWN 83.5%.
- Call 2 전체 UNKNOWN은 4,612/5,188이다.
- Article263 pair 1개는 Call 2에서 `case_truths`로 투영되어 Scallop까지 전달된다. 별도
  `article263_assessments`를 runner가 직접 읽지 않는다는 이유로 handoff 누락이라고 한 초기
  진단은 정정했다. 실제 문제는 `causal_origin_unascertained=FALSE` 의미 오판이다.
- rubric 13 cases/92 atoms가 미수·중지·불능미수·예비를 요구하지만 authored completion
  policy는 4 offense뿐이다.
- rubric 6 cases/43 atoms가 간접정범을 요구하지만 current participation/Result IR에는
  indirect-perpetrator form이 없다.
- Scallop active doctrine row는 0이다. rubric의 양해/승낙, 불법원인급여, 우연방위,
  적법성 착오 등 branch가 authored doctrine universe에 없다.
- `offense.use_of_forged_private_document`는 객체가 실제 위조문서라는 dependency를 요구하지
  않아 base forgery가 없어도 행사죄가 성립할 수 있다.
- established 8개를 rubric과 질적으로 대조하면 3개 정합, 4개 충돌, 1개는 조건부 branch를
  단일 결론으로 평탄화했다.

확인된 모델 오류와 계약 오류를 분리했다. 준강간의 명시적 항거불능 부정을 TRUE로 읽은
것과 B가 자기 명의로 작성한 문서를 무권한 위조로 읽은 것은 모델/semantic error다. 반면
question prompt의 명시적 전제를 predicate evidence에서 제외한 것, 불법원인급여·간접정범을
occurrence-local predicate로 물은 것, completion/doctrine
coverage 부재는 host/RuleIR 계약 문제다.

## normalization 구현 결과

- question assumptions: `src/idpr/v2/question_assumptions.py`,
  `data/v2/question_assumptions.jsonl`. GOLD occurrence에 행위를 추가하지 않고 문항의 명시적
  사실 전제만 별도 운반한다. 현재 exact carrier는 `r10_p2_q3`, `r14_p2_q4` 두 건이다.
- completion: 기존 4개 policy에 homicide, ancestral homicide, rape, quasi rape, theft,
  special theft, injury, robbery 8개를 추가했다. completed 실패를 attempt로 바꾸는 fallback은
  없고 위험성 없는 불능행위를 punishable attempt로 repair하지 않는다.
- planner core dry-run: top-level 815, assessment 849, relation 423은 유지되고 predicate는
  5,182 -> 5,838이다. registry hash 변경으로 기존 Call 1 manifest lineage가 정상 거부됐으며
  새 full artifact는 아직 생성하지 않았다.
- decisive partial gold: `data/eval/v2_call2_decisive_predicate_partial_gold.jsonl`의 명시 근거
  8개를 `scripts/audit_v2_call2_decisive_partial_gold.py`로 대조했다. 준강간의 명시적 부정
  문장이 diagnostic 요청에서 누락됐음을 발견해 historical ownership을 semantic error 2,
  model undercall 4, evidence scope missing 2로 바로잡았다. 해당 문장은 같은 GOLD occurrence
  source에 복원했으며 새 run에서 처음으로 의미 gate가 된다.
- contextual truth variation은 118개, 그중 ground fact는 33개다. intent처럼 offense-sensitive한
  legal element가 있으므로 118개 전부를 오류로 보지 않고 triage 후보로만 기록한다.
- Call 1 lineage는 full registry hash가 아니라 실제 router catalog fingerprint가 소유한다.
  기존 manifest는 ordered catalog ID exact match의 legacy mode로만 재사용된다. 새 planner
  artifact/audit는 26/26, errors 0이다.
- GroundFact는 `(case, actor, occurrence, predicate)`당 한 번만 neural 평가하고 모든 소비
  offense instance로 host projection한다. semantic predicate target 5,838개 중 neural request
  target은 4,998개다. LegalElement는 계속 instance-local이다. predicate prompt의 기존 일반
  예시 두 개도 제거했다.
- indirect principal dependency runtime은 이미 있으나 production grounding relation과 Scallop
  lowering이 없다. 피해자 A·결재권자처럼 피이용자가 현재 GOLD liable actor/instance에 없는
  사례가 있어 source-local factual participant identity가 선행한다. instigator/aider를
  재사용하지 않고 typed utilization relation을 participation identity/local-unresolved 변경과
  함께 연결할 때까지 HOLD다.
- doctrine/card bridge offline audit: KCL-26 issue tag 80개 중 77개가 commentary target,
  75개가 candidate card에 도달하지만 explicit symbolic bridge는 0개다. 총칙 corpus-gap tag는
  21개다. 카드는 설명 근거로 재사용하되 `exception`/`defeater` metadata만으로 doctrine을
  발화하지 않는다. artifact는 `experiments/v2_restart_rebuild/doctrine_card_bridge_audit_v1/`.
- real-Gemma focused gate: 준강간 explicit negative와 Article 263 pair relation carrier는
  통과했다. 사문서위조 authority/content 경계는 같은 seed에서도 TRUE/FALSE가 오가므로
  non-strict known-instability로 기록했고 추가 prompt 튜닝이나 host repair를 하지 않았다.
- `call2_full_groundfact_v6_diagnostic`: exact audit errors 0, semantic predicate 5,838 / neural
  predicate request 4,998 / relation 423 / participation 5,859. participation reject는 8건이고
  artifact status는 `DEGRADED_DIAGNOSTIC`이다. partial gold는 4 match / 3 undercall / 1 error였지만
  남은 Article 263 error는 pair relation evidence 미운반으로 확인됐다.
- Article 263 `MULTI_OCCURRENCE_RELATION` source/span carrier를 pair binding에 추가했다.
  `call2_article263_carrier_v7` case-only 재실행은 세 truth 모두 TRUE, audit errors 0이다. 다만
  underlying `injury_result`가 occurrence-local request에서 UNKNOWN이어서 Scallop completion은
  여전히 unresolved다.
- `scallop_groundfact_v6_diagnostic`: 18 succeeded / 8 rejected-participation skip, active doctrine
  0, established 10. rubric과 직접 정합한 establishment는 횡령·위계공무집행방해·현주건조물
  방화 3개다. 나머지는 indirect route 평탄화, bribe role 오류, forged-document dependency,
  잘못된 special injury, mistake branch 부재가 드러났다. Scallop runtime/parity 오류 증거는 없다.
- Article 263 shared-result v8: 기존 dedicated physical request에 법정의제 세 truth와 구분된
  `shared_result_truths=[injury_result]`를 추가했다. known pair-level truth는 occurrence-local
  UNKNOWN만 refine하고 TRUE/FALSE 충돌은 hard-fail한다. E2E runner가 기존 dedicated Article
  263 Scallop backend를 실제로 호출하도록 연결했고 backend의 single-instance EDB scope bug도
  수정했다. 두 endpoint 모두 completion completed + statutory obligation TRUE까지 도달한다.
  남은 blocker는 Gemma가 focused request에서도 양쪽 injury `intent`를 UNKNOWN으로 둔 known
  undercall이다. host repair/prompt tuning은 하지 않는다.
- source-local factual participant identity를 liable actor와 분리했다.
  `FactualParticipantKey(case_id, fpart:*)`와
  `data/v2/gold_factual_participants.jsonl`의 6개 exact-span identity에는 offense/role/mode/truth가
  없다. 기존 GOLD actor와 label이 같아도 자동 병합하지 않고 top-level planner universe에도
  넣지 않는다. production registry에 offense별 indirect-capability metadata가 아직 없으므로
  card 문자열 검색 또는 모든 offense 곱으로 utilization target을 만드는 것은 HOLD다.
- decisive partial gold는 15개다. 새 `dp:013`~`dp:015`는 밀침·상해를 성기 삽입으로, 장래
  거짓말 지시를 선서 증인의 허위진술로, 강도치사를 성기 삽입으로 읽은 ground-fact false
  positive다. v6 historical 대조는 4 match / 7 undercall / 4 semantic error이고 ground-fact
  contextual variation은 0이다.

## 다음 판단점

IssuePlanner/AnswerPlan 설계는 아직 시작하지 않는다. 먼저 rubric supervision으로 확인된
앞단 결함의 scope를 다음 순서로 결정한다.

1. decisive partial gold를 명시 근거 범위에서 더 확장하되 결론에서 leaf를 역산하지 않는다.
   ground-fact variation은 host projection으로 닫혔으므로 명시적 legal-element undercall과
   semantic reversal을 우선한다.
2. source-local factual participant identity 분리는 완료됐다. 다음은 card prose가 아니라
   explicit offense-level metadata로 indirect-capability 범위를 authoring할 수 있는지 확정한다.
   그 뒤에만 factual-action-direction typed utilization relation + deterministic host dependency
   lowering을 연결한다. ordinary liability instance로 암묵 변환하지 않는다.
3. forged-document dependency는 document identity/link 없이 새 predicate 하나로 덮지 않는다.
   선행 forgery realization dependency를 표현할 host relation을 먼저 정한다.
4. commentary/card metadata는 retrieval provenance로 사용하고, 필요한 branch마다 stable id,
   typed requires, effect/stage, instance binding을 별도 authoring하는 deterministic bridge를
   설계한다. KCL issue tag 자체는 runtime fact로 사용하지 않는다.
5. 그 뒤 새 Call 2를 실행하고 partial-gold audit, participation compile, Scallop 질적 대조를
   거친 후에만 rubric-supervised IssuePlanner/AnswerPlan으로 간다.

현재 truth/registry만으로 complete unique realization grouping은 불가능하다. TRUE-only
projection은 815개 중 19개이고 26문항 중 13문항에 confirmed candidate가 없으며, UNKNOWN을
포함하면 790개가 살아 후보 폭증이 유지된다. prompt 튜닝, full 재실행, 외부 rubric judge는
위 debugging 동안 보류한다.

## 다음 세션에 보낼 메시지

> `docs/handoff/NEXT_SESSION.md`와
> `docs/analysis/V2_RUBRIC_SUPERVISED_FAILURE_DEBUG.md`부터 읽어. KCL rubric은 runtime이나
> few-shot이 아니라 offline supervision으로만 사용한다. IssuePlanner는 아직 만들지 마.
> Article263 transport, question-assumption carrier, completion 8개, decisive partial-gold audit은
> 완료됐다. Call 1 catalog lineage 분리와 ground-fact occurrence-level projection도 완료됐다.
> v6 diagnostic full/Scallop과 Article263 shared-result/dedicated lowering v8까지 완료됐다.
> source-local factual participant identity는 liable actor와 분리 완료됐다. 다음은 card prose를
> runtime 판단으로 쓰지 않고 explicit offense-level indirect-capability metadata를 authoring할
> 근거와 범위를 확정해. 그 뒤에만 factual-action-direction typed utilization -> deterministic
> host dependency -> Scallop lowering으로 가. forged-document는 identity link 없이 leaf를 하나
> 추가해 덮지 마.
> IssuePlanner/Call3/judge는 계속 보류해.

## 2026-08-12 indirect-principal structural lowering delta

이전 섹션에서 HOLD했던 indirect-principal 경로를 아래 순서 그대로 구현했다.

1. offense-level `indirect_principal_capability` metadata
2. offense-free factual action-direction relation
3. deterministic host dependency
4. dedicated indirect-principal runtime
5. dedicated Scallop lowering/parity

capability metadata는 exact offense에 명시된 `legally_possible: true`만 읽는다. metadata 부재는
법적 불가능이 아니라 unauthored/out-of-scope이며, derived offense는 base offense에서 이를
상속하지 않는다. card 문구, rubric tag, statute, participation mode로 후보를 활성화하는
fallback은 없다. 현재 명시한 범위는
`false_public_document_creation`, `private_document_forgery`, `forcible_indecency`,
`obstruction_of_right_exercise`, `derived_offense.fraud` 다섯 개다.

factual utilization target은 `(case, utilizer actor, occurrence) -> source-local factual
participant`이며 offense/role/liability를 담지 않는다. 요청도 행위 지시·야기·이용의 사실적
방향에 대한 `TRUE/FALSE/UNKNOWN`만 받는다. 실제 간접정범 dependency는 이 relation과 exact
participant/offense의 `UtilizedParticipantOutcome`을 host가 결합해 산출한다. 누락·중복·identity
불일치·capability 불일치는 hard-fail하고 UNKNOWN은 보존한다. instigator/aider policy나 그
intent predicate는 재사용하지 않았다.

Scallop에는 `v2_indirect_principal_dependency_truth` 전용 relation/program을 추가했다.
`v2_derivative_link`로 우회하지 않으며 host dependency와 Scallop row의 exact correspondence 및
truth parity를 검증한다. planner dry-run은 기존 주요 count를 바꾸지 않았고 factual utilization
target 10개를 추가했으며 audit errors는 0이다. `r13_p2_q1`의 fraud target이 0인 것은 현재 Step 7
closure에 `derived_offense.fraud`가 없는 기존 issue miss이며 metadata나 rubric으로 repair하지
않았다. 丙 participant span은 乙의 전달·요청과 丙의 카드 사용을 함께 포함하도록 사실 근거만
확장했다.

아직 real-Gemma Call 2를 새로 실행하지 않았다. 특히 production
`UtilizedParticipantOutcome` producer는 남아 있다. 이를 rubric 결론이나 one-shot 법적 stage
질문으로 채우지 말고, participant를 ordinary liability actor로 승격하지 않은 채 predicate-level
truth에서 exact offense별 내부 outcome을 계산하는 경계를 설계해야 한다. 이 경계가 닫히기
전에도 IssuePlanner/Call3/judge는 계속 보류한다.

검증 결과는 full local suite `130 passed, 13 skipped`, planner audit `SUCCEEDED` / errors 0이다.

## 2026-08-12 utilized-participant outcome production delta

위에 남아 있던 production 경계를 닫았다. 새 producer는 factual participant를
`OffenseInstanceKey` 또는 ordinary `LiabilityEvaluation`으로 변환하지 않고,
`(FactualParticipantKey, exact offense)` namespace에서 구성요건 predicate truth를 받아
협은 `UtilizedParticipantOutcome`만 산출한다. relation truth 누락은 FALSE가 아니라
UNKNOWN으로 보존하고, active doctrine도 같은 participant predicate view에서 계산한다.
다른 과실범은 명시 truth가 있을 때만 사용하며 추론하지 않는다. completion-bearing
capability offense는 participant전용 completion 계약 전까지 hard-fail한다.

planner/runner/audit/Scallop handoff를 이 경계에 연결했다. 현재 exact frontier는 outcome
target 5개, participant predicate target 26개이며 planner audit errors는 0이다. full non-smoke
Call 2 artifact는 이 outcome과 deterministic indirect dependency를 내고, Scallop runner는 전용
parity program으로 낮춘다. 한 utilizer instance에 participant dependency가 여러 개이면 authored fold
policy 없이 임의 병합하지 않고 hard-fail한다. serialized dependency의 truth/status 열거값도
역직렬화 시 검증한다.

지시어만 있던 factual participant span 5개를 판단 결론 없이 완전한 사실 문장으로
확장했다. `false_public_document_creation`은 형법 제13조와 제227조의 명시적
구성요건 구조에 맞춰 `intent`를 정신적 slot에 추가했다. 이로 인해 전체
planner count는 final assessment 5840, neural request 5000이 되었고 outcome frontier는 5/26으로
고정됐다.

검증은 focused `46 passed`, full local `137 passed, 16 skipped`, Python compile/Ruff/
`git diff --check` 기준으로 완료했다. real-Gemma는 `IDPR_VLLM_BASE_URL`/
`IDPR_VLLM_MODEL`이 설정되지 않아 실행하지 않았고, 새 outcome prompt는 명시적
`--prompt-approved`도 필요하다. 따라서 다음 게이트는 prompt 검토/승인 후 live 3-case
semantic gate와 full Call 2를 순서대로 실행하는 것이다. IssuePlanner/Call3/judge는 그 전까지
계속 보류한다.

## 2026-08-12 Call 1.5 direct factual-scope normalization

KCL substantive 26문항을 전수 감사해 원문의 사실 번호, 추가 가정, 밑줄 치환, 선행 사실
의존성을 host가 직접형 factual scope로 조립하도록 `scoped_question_text`를 수정했다. Call 1의
74 survivor, Call 1.5 primary prompt, recovery prompt는 freeze했다. rubric/gold는 model input이나
production selector로 사용하지 않았다.

핵심 수정은 `r14_p2_q2`의 old/new 밑줄 사실 동시 노출 제거, 번호 없는 r13 문항의 명시적
책임 행위자 기반 사실 블록 선택, 그리고 `r12_p2_q1_na` 등 선행 사실을 명시적으로 전제하는
문항의 dependency closure다. 전체 결과와 26문항 분류는
`experiments/v2_call15_directscope_26_causal/scope_audit.md`가 정본이다.

동일 입력 행의 model nondeterminism을 개선 효과로 세지 않기 위해 실제 scope가 바뀐 3개만
재실행 결과로 교체한 causal artifact를 만들었다. 결과는 direct 78 bindings, explicit gold
50/57, safe derived 6 unique/10 physical 전부 gold-relevant, 최종 Call 1 survivor 56/74다.
이전 51/74보다 5개 늘었다. planner는 top-level 88, neural Call 2 543으로 Cartesian 815/4,998
대비 각각 89.2%/89.1% 감소다.

새 grouping 감사에서 qualifier component 없이 열리던 세 rule도 제거했다:
`theft+dwelling -> nighttime dwelling theft`, `theft+dwelling -> special theft`,
`robbery+dwelling -> special robbery`. host text interpretation은 추가하지 않았고, 동일 episode의
복수 행위자 theft -> special theft candidate만 유지했다.

남은 50 UNBOUND 전부의 atomic recovery는 8 non-empty였지만 gold 관련은 harboring 한 건뿐이고
그마저 actor coverage가 불완전하므로 merge하지 않았다. 현재 canonical artifact는
`experiments/v2_call15_directscope_26_causal/issue_bindings.jsonl`, planner/audit도 같은 디렉터리에
있다. 검증은 full local `156 passed, 16 skipped`다. job 221593의 live vLLM을 사용했다.

## 2026-08-12 binding-scoped Call 2 / Scallop result

canonical 56/74 binding과 543-target planner를 job 221593 live vLLM에 실행했다. 기존 runner가
`gold_occurrences` identity를 강제하던 배선을 제거하고 명시적 planner-evidence mode를 추가했다.
이 모드에서는 offline gold occurrence, factual participant, Article 263 pair가 model input에
들어가지 않는다. 26/26, 99 physical requests, 543 predicate truths, 16 relation truths, contract
errors 0이다. TRUE/FALSE/UNKNOWN은 231/46/266이며 이전 Cartesian diagnostic의
597/31/5,216과 직접 비교 시 candidate pruning 효과와 model accuracy를 혼동하지 않는다.

reviewed partial gold 15개를 source-span으로 binding identity에 offline 재결합한 결과는 match 4,
undercall 5, semantic error 1, negative target pruned 4, positive target pruned 1이다. positive miss는
`r10_p1_q2` Article 263 causal-origin-unascertained로, binding-scoped multi-episode relation carrier
부재가 ownership이다. participation은 기존 5,859 targets/8 rejected에서 0/0이 되었지만 이는
true-link recall도 없는 상태다. Scallop이 planner를 무시하고 88 participation candidates를
재생성하던 bug는 고쳐 serialized planner targets만 소비하게 했다.

Scallop은 26/26, 88 instances, established 18, element failure 52, completion failure 18,
active doctrine 0이다. rubric outside proxy는 4/18이다. 상세 정본은
`experiments/v2_call15_directscope_26_causal/call2_full_v1/qualitative_audit.md`다. Call 1.5는
freeze하고 다음 구조적 blocker는 gold 없이 만드는 Article263 multi-binding relation carrier와
offense-free typed factual participation candidate producer다.

## 2026-08-12 Article 263 binding-pair transport delta

위의 Article 263 blocker는 해결했다. 같은 factual episode의 서로 다른 injury binding이 공통
factual target을 가질 때만 factual pair candidate를 만들며, host는 Article 263 요건을 판정하지
않는다. KCL-26에서 후보는 `r10_p1_q2` 甲/乙→B 한 쌍뿐이다. 일반 planner 수치는 문항별
2~71, 합계 top-level 88 / neural 543 그대로이고 Article 263 전용 요청만 1회 추가됐다.

job 221593 live vLLM 전체 재실행은 26/26, 100 physical requests, projected truth
TRUE/FALSE/UNKNOWN 236/40/273이다. 전용 모델은 Article 263 세 predicate와 shared injury를
TRUE로 판정했고 partial gold는 match 5, undercall 5, semantic error 1, negative pruned 4,
positive pruned 0이 됐다. Scallop은 26/26, established 18, outside proxy 4/18이며 해당 두 injury
instance는 mental UNKNOWN 때문에 여전히 elements unresolved다.

정본은 `experiments/v2_call15_directscope_26_causal/call2_full_v2/`와
`experiments/v2_call15_directscope_26_causal/scallop_v2/`다. 검증은 full local
`159 passed, 16 skipped`다. 다음 구조적 blocker는 offense-free typed factual participation
candidate producer이며, participation 0은 true-link recall도 0인 상태로 계속 명시한다.

## 2026-08-12 qualitative Scallop / E2E readiness audit

26문항을 rubric과 수작업 대조한 정본은
`experiments/v2_call15_directscope_26_causal/e2e_readiness_audit.md`다. Call 1 closure는
74/86, safely bound는 56/86이며 Scallop 실행은 26/26이지만 어떤 establishment라도 있는
문항은 13/26뿐이다. 88 instances는 established 18 / elements unresolved 42 / elements failed
10 / completion stop 18이다. 18 establishments 중 보수적으로 약 절반만 rubric과 유용하거나
부분적으로 일치하고, 나머지는 명시적 rubric 충돌·wrong actor/mode·wrong completion·흡수되지
않은 base offense다. 이는 정식 accuracy가 아니라 failure-ownership 수작업 판단이다.

정상화된 것은 factual scope audit, binding identity/span, non-Cartesian planner, evidence-gated
closure, gold-free production evidence, typed UNKNOWN/UNBOUND, Article 263 carrier다. 아직
정상화되지 않은 것은 target scope 대 dependency context(`r12_p2_q1_na` leakage), participation
0, canonical indirect-principal 0, active doctrine 0, completion form, absorption/competition이다.
따라서 milestone은 `normalized grounding pipeline, pre-final-E2E`이며 canonical Call 3/final
rubric judge를 실행할 단계는 아니다.

## 2026-08-13 card IR / concurrence normalization delta

각론 카드 1,848장과 reviewed issue 383개를 v2 `OffenseInstanceKey`에 연결하는 host-safe bridge를
추가했다. 기존 issue-first retrieval의 `card -> reviewed parent issue -> article` 경계를 그대로
재사용하며, current instance의 authored statutory identity로 article scope를 먼저 제한한 뒤 해당
binding/derived source의 exact episode quote로 issue를 검색한다. issue당 detail card는 최대 2장이다.
검색 결과는 candidate/context일 뿐 predicate truth, doctrine activation, completion, participation,
concurrence effect를 만들지 않는다. 기존 Call 1/1.5/1.5-P/Call 2 prompt는 변경하지 않았다.

canonical 87 top-level instance offline audit 결과 71개는 exact article join, 16개 derived instance는
identity 미작성으로 `UNMAPPED_DERIVED_ARTICLE` 보존이다. physical/unique issue candidate는
213/107, unique anchor 119, selected detail 210이다. 기능별 physical 분포는 element 133,
support 27, concurrence 21, guard 18, stage 8, participation 6이다. 이는 카드 활용의 가장 큰
효과가 현재 Call 2 semantic undercall/UNKNOWN의 구성요건 해석 보강이고, 그 밖에 completion,
participation, 위법성·책임, 경합·흡수, Call 3 Rule 근거를 단계별로 보완할 수 있음을 보여준다.
현재 Call 2 UNKNOWN 중 exact article/card join 가능한 것은 199 targets / 64 predicate refs다.
정본은 `experiments/v2_call15_directscope_26_causal/card_issue_join_v1/`와
`docs/analysis/v2_card_ir_and_concurrence_normalization_ko.md`다.

DerivedOffenseDef에 identity를 바로 추가하면 frozen Call 1 catalog fingerprint가 바뀌므로 하지
않았다. 후속 authoring은 router-visible definition 변경이 아니라 reviewed
`definition_ref -> card article` metadata로 분리해야 한다. atomic card-informed predicate
reassessment는 기존 Call 2 prompt 수정이므로 정확한 prompt/schema를 먼저 제시하고 사용자
승인을 받은 뒤 live job 222907에 태워야 한다.

경합·흡수는 occurrence-aware typed reducer 경계를 구현했다. exact DefinitionRef pair와 same
factual episode가 있어야 후보를 열고, condition TRUE일 때만 absorption/상상적 경합을 적용한다.
FALSE는 효과 없음, UNKNOWN은 두 instance를 모두 유지한 typed unresolved다. 복수 parent/cycle
conflict도 host가 고르지 않고 unresolved로 보존한다. legacy `concurrence.yaml` 12개를 감사한
결과 exact one-to-one article mapping 4, ambiguous 3, missing v2 offense side 5이며 condition card
10개가 approved issue anchor다. 그러나 source status가 `awaiting_legal_review`이고 exact pair,
episode constraint, instance-scoped assessment가 아직 authoring되지 않아 production-ready rule은
0개다. 현재 E2E에는 효과를 발화시키지 않는다. 정본은
`experiments/v2_call15_directscope_26_causal/concurrence_identity_v1/`다.

## 2026-08-13 doctrine·경합 트랙: 정책 저작과 probe compiler

### 확정된 것

KCL-26 감사 결과 저작 공백이 지배적이라는 것이 먼저 드러났다. 저작된 12개 doctrine이
실제로 결정적인 문항은 2개(우연방위·피해자 승낙)뿐이고, 미저작 법리가 15개 문항에 걸린다.
착오 9, 신분·제33조 6, 공범의 초과 4, 불가벌적 사후행위 2다. 인과관계는 과대계상이었다 --
`relation.causal_nexus`가 이미 결과적 가중범에 물려 있고, 루브릭이 요구하는 학설 대립
서술은 Call 3 소관이다.

active doctrine 0의 원인도 확정했다. Scallop 결함이 아니라 dead loop다. closure가 12개
doctrine을 모든 사건에 후보로 열지만 활성화는 leaf가 non-UNKNOWN이어야 하고, 그 31개
leaf를 planner가 한 번도 target으로 만들지 않는다.

### 저작·구현된 것

- **제33조 본문**: `constitutive_status_refs` 런타임이 이미 있었고 권리행사방해만 저작돼
  있었다. 수뢰·위증·허위공문서작성 3개 진정신분범을 추가했다.
- **특별관계 흡수**: planner가 derived binding을 materialize할 때 기록해 둔
  `source_binding_ids`를 되읽어 base를 흡수한다. KCL-26에서 5개(절도→특수절도).
  행위자 일치를 요구하는 것이 핵심이다 -- 한 episode에 甲乙丙 절도가 모두 있다.
- **mistake_policy / excess_policy / aggravating_status_participation**: 새 kind 2개와
  offense 필드 1개. 7개 검수 항목 전부 반영. 부합설은 법정적 부합설로 profile 고정,
  위전착은 culpability, 제33조 단서는 가중죄 realization 자체 생성, 초과는 derivation
  부재를 질적 초과로 읽지 않고 결과적 가중범은 예견가능성으로 분기.
- **세 런타임**: 모두 모델을 부르지 않는다. 이미 받은 truth 아니면 저작된 구조만 읽는다.
- **`v2_accessory_excess_effect`**: 전용 Scallop relation, host 분류와 파리티 검증. 실행 확인.
- **`policy_probes.py`**: 정책이 `probe` 블록으로 필요 입력을 선언하고 planner는 법리를
  모른 채 그것만 읽는다. 정책마다 planner 분기를 만들면 doctrine dead loop를 종류별로
  반복하게 되므로 공통 compiler 하나로 접었다. `supply` 축이 뉴럴 부하를 통제한다.

검증은 `242 passed, 16 skipped`.

### 남긴 공백 (`data/v2/representation_gaps.yaml`)

세 항목 모두 테스트가 지킨다. 저작되면 테스트가 실패하며 갱신을 요구한다.

1. **intended-object identity** -- `factual_targets`를 의도한 대상으로 재해석하는 것은
   검수에서 명시적으로 거부됐다. 그 필드는 상대방·수령자·관련 participant까지 포함한다.
   `legal_element.object_misidentification`도 같은 공백의 하류라 열지 않았다. 목표 대상이
   확정되지 않은 채 객체/방법의 착오를 물으면 모델이 identity를 지어내 답한다.
   향후 설계는 `directed_action_target`/`actual_result_bearer`를 각각 사실로 결박하고
   차이만 host가 structural하게 계산하는 것이다.
2. **폭행죄 family** (제260·261·262조) -- 각칙 워크시트가 art259에서 art263으로 건너뛴다.
   `r11_p1_q1` 질적 초과가 미해결로 남는다.
3. **장물죄 family** (제362조) -- 카드는 있으나 v2 저작이 보류 상태다. `r10_p2_q1`
   불가벌적 사후행위 흡수 pair를 만들 수 없다.

### 다음 세션 (이 절은 아래 2026-08-13 최종 책임 뷰 절이 대체한다)

doctrine 트랙은 여기까지다. 남은 것은 두 갈래다.

**경합·최종 책임 뷰.** 특별관계 흡수는 구현했으나 아직 E2E에 발화시키지 않았다. legacy
concurrence 12개 중 KCL-26에서 실제 발화 가능한 것은 인장위조←사문서위조 1쌍뿐이고
(나머지 3개는 두 죄가 서로 다른 문항에 흩어져 있다), 그마저 binding:002와 binding:004가
같은 factual episode인지 확인이 필요하다. 상상적 경합 legacy 4개는 v2 offense 측 결손이다.

**세 런타임의 파이프라인 관통.** 정의·런타임·Scallop·probe까지 갖췄지만 호출자가 없다.
probe compiler 기준 남은 gap은 mistake 2개뿐이고 둘 다 위 1번 공백이 원인이다. excess는
provenance가 준비됐고, 제33조 단서는 필요한 status leaf가 이미 planner target에 있다.

그 뒤가 Call 1.5-D 프롬프트 승인과 222907 라이브 실행이다. 프롬프트는 아직 작성하지
않았고, 활성 프롬프트이므로 전문 승인이 필요하다.

## 2026-08-13 최종 책임 뷰: 경합·초과·제33조 단서 관통

위 두 갈래(경합 발화, 세 런타임 관통)를 하나의 심볼릭 단계로 묶어 E2E에 연결했다.
`src/idpr/v2/runtime/final_responsibility.py`가 인스턴스별 liability chain 뒤에서 한 번 돌고,
`run_v2_scallop_e2e.py`가 `--plan`으로 그것을 호출한다. 모델을 새로 부르지 않았고 Call 2
artifact는 `call2_v8_indirect_principal`을 그대로 재사용했다.

제33조 단서만 chain **앞**에서 적용된다. derivative link의 가담자 instance를 가중죄로 바꾼 뒤
평가하며, 전환 대상이 평가 universe에 없으면 만들지 않고 marker를 남긴다.

정본은 `experiments/v2_call15_directscope_26_causal/final_responsibility_v10/audit.md`다.
`liability_results`는 `scallop_v9_completion_normalized`와 26/26 완전히 동일하다 -- 이 단계는
기존 인스턴스 결론을 바꾸지 않고 그 위에 층을 얹는다.

### 발화 결과와 그 원인

- 특별관계 흡수: plan 수준 후보 5(절도→특수절도, `r13_p1_q1`/`r13_p2_q1`), 발화 0. 어느
  instance도 성립까지 가지 못한다. 앞단 undercall의 하류이지 흡수 로직의 문제가 아니다.
- 저작된 경합: `data/v2/concurrence_rules.yaml`을 신설하고 legacy 인장위조←사문서위조 1쌍을
  exact DefinitionRef로 옮겼다. `status: approved`만 런타임에 도달한다. 검수에서 조건을
  "그 문서의 구성부분이 된 인영의 위조"로 좁힌 뒤 승인됐다(인과 자체 제작은 독립한 사인위조죄).
  KCL-26에서는 `r12_p2_q1_da`의 두 위조죄가 성립하지 않아 후보가 열리지 않는다.
- 공범의 초과: **1건 발화**. 검수에서 join을 factual episode에서 참가 링크로 교체했다. 후보는
  확정된 derivative link의 principal이 그 realization **이후** episode에서 실현한, 교사 대상과
  다른 죄다. `r11_p1_q1`이 甲 `offense.theft` -> 乙 `offense.injury`,
  `qualitative / no_liability_for_excess`로 판정되고 전용 Scallop relation parity도 통과했다.
  폭행치상 미저작(`gap.assault_offense_family`)은 그대로 남겼다 -- 분류는 맞고 죄명이 다르다.
- 제33조 단서: **probe target wiring 완료**, 발화는 여전히 0.
  `runtime/policy_probe_targets.py`가 저작된 참가 probe를 Call 2 target으로 낮춘다. KCL-26에서
  정확히 3개(`r12_p2_q1_ga` 甲 교사·방조, `r13_p1_q3` 丁 교사)가 열리고 assessment target은
  531 -> 534다. 발화 0의 원인이 leaf 부재에서 **살인 참가 link 0**으로 바뀌었다 --
  `r12_p2_q1_ga`는 mode 충돌 격리, `r13_p1_q3`는 참가 truth가 link를 만들지 못했다. 그래서 그
  3개 target만을 위한 live Call 2 재실행은 하지 않았다(바뀌는 결론이 없다).
  `optional` 요구(초과 예견가능성)는 열지 않았다 -- 전부 열면 target이 31개 더 는다.
  공동정범 mode는 소비 경로가 없어 `participation_probe_unreachable_modes`로 남겼다.
- 표현 공백: `UNRESOLVED_MISTAKE_BINDING` 25(전 문항, `gap.intended_object_identity`).
  기존 `UNRESOLVED_AGGRAVATING_STATUS` 4건은 사라졌다 -- 살인 참가 후보가 없는 문항에서 뜬
  false positive였고, 이제 공백 보고가 후보 범위를 본다.

### 부수 정상화

- planner가 top-level instance마다 `instance_provenance`(factual episode + source binding)를
  기록한다. Call 1.5-P가 만드는 participation candidate instance도 자기 episode를 함께 나른다.
  없으면 가담자 instance가 최종 책임 단계에서 통째로 빠진다.
- participation target 49개는 frozen v7과 완전히 동일하다.

- 초과 효과 소비: `no_liability_for_excess`는 Call 3 메모가 아니라 심볼릭 결론으로 처리한다.
  가담자의 전체 liability를 뒤집지 않고 **초과한 죄로 가는 귀속 edge만** 차단하며, `unresolved`는
  무책으로 접지도 중한 죄를 세우지도 않는다. 초과가 경합보다 먼저 돈다 -- 귀속이 차단된 죄는
  흡수 자리에 서면 안 된다. 뷰가 `final_instances`와 `attribution_withheld_instances`를 낸다.

검증은 로컬 전체 `260 passed, 16 skipped`.

### 검수 완료 항목

`docs/analysis/v2_concurrence_and_excess_review_ko.md`의 두 카드는 답변을 받아 반영됐다.
① 조건을 좁힌 뒤 승인, ② 링크 기반 join으로 교체, ③ 초과 효과는 final responsibility가
소비(귀속 edge만 차단). 각 카드의 "검수 결과" 절과 위 delta가 정본이다.

### 다음 세션

1번(제33조 단서 wiring)은 완료했다. 남은 것은 아래다.

1. **흡수 조건 assessment 채널.** 인장위조 규칙은 승인됐으나 조건
   (`condition.forged_seal_impression_is_a_constituent_part_of_the_document`)을 물을 곳이 없어
   후보가 열려도 UNKNOWN이다. Call 2 target 추가이므로 프롬프트 승인 게이트에 걸린다.
2. **참가 recall.** 제33조 단서도 초과도 이제 참가 link에 걸려 있다. KCL-26에서 살인 참가
   후보 2문항 모두 link가 0이라 두 법리 다 발화하지 못한다. 앞단 참가 정확도가 다음 병목이다.
3. **검수 대기 두 건**: `optional` probe 요구를 열 것인가(예산), 제33조 단서의 공동정범
   저작을 좁힐 것인가 아니면 group node 소비 경로를 만들 것인가.

Call 3는 이 typed 결과를 **설명만** 한다 -- "乙의 상해는 甲의 교사 범위를 질적으로 초과하므로
그 부분에 대한 책임은 없다". 초과 판정 자체를 Call 3가 하지 않는다.

그 뒤가 Call 1.5-D 프롬프트 승인과 222907 라이브 실행이다. 프롬프트는 아직 작성하지 않았고,
활성 프롬프트이므로 전문 승인이 필요하다. IssuePlanner/Call3/judge는 계속 보류한다.

## 2026-08-13 Call 1.5-D doctrine activation: cue catalog / contract 저작

active doctrine 0의 dead loop를 닫는 경로를 설계 검수까지 마치고 앞단 두 모듈을 구현했다.
**모델은 아직 부르지 않았다.**

- 설계 정본: `docs/analysis/v2_call15d_doctrine_activation_design_ko.md` (카드 A~E 검수 완료).
- 프롬프트 전문: `docs/analysis/v2_call15d_prompt_review_ko.md` (카드 F 검수 대기, 미설치).
- cue 카탈로그: `data/v2/doctrine_raising_cues.yaml` v2, cue 14개 / doctrine 13개 / leaf 32개.

### 검수로 바뀐 것

1. `competing_duty_stated`와 `legal_or_occupational_basis_stated` 문구를 좁혔다. 단순 등장으로
   TRUE가 되는 lexical cue를 피하되 법적 판단은 넣지 않는다.
2. **`actor_mental_condition_stated`를 두 cue로 분리했다.** 지속적 정신질환·장애는 `actor`
   scope, 음주·약물 등 일시적 상태는 `episode` scope다. 합쳐 두면 episode 1의 만취가
   episode 7의 별개 범행까지 번진다 -- 초과에서 닫은 문제를 반대 방향으로 다시 만드는 것이었다.
   actor scope는 age / persistent mental disorder / hearing-speech impairment 셋뿐이고 테스트가
   그 집합을 고정한다.
3. 위전착 cue를 신설했다. registry의 13개 doctrine이 전부 raising path를 갖게 됐고,
   `test_every_authored_doctrine_has_a_raising_path`가 회귀로 지킨다.
4. v1은 top-level 87개 instance에만 leaf를 연다. 참가 후보 45개는 link 확정 후 후속
   materialize가 맞는 구조이고 지금은 deferred다.
5. Call 2 증분 재검수 게이트는 `Δtarget ≤ 300`이다. 비용만이 아니라 semantic safety gate다.

### 구현 상태

- `src/idpr/v2/doctrine_cues.py` -- 카탈로그 파서, 요청 payload, 출력 schema/검증. 완료.
  payload에 doctrine ref·조문·scope가 들어가지 않는 것을 테스트가 확인한다.
- `src/idpr/v2/runtime/doctrine_raising.py` -- cue -> `RaisedDoctrine`. actor scope 투영 시
  `source_episode_id`/`target_episode_id`를 분리해 provenance를 보존한다. 완료.
- planner target 확장과 러너 스크립트는 Call 1.5-D 실행 후 착수한다.
- `tests/test_doctrine_cues.py` 14개. 전체 `274 passed, 16 skipped`.

### 다음 세션

1. 카드 F(프롬프트 전문) 승인 -> `prompts/v2_call15d_doctrine_cue.md` / `_user.md` 설치.
2. `scripts/run_v2_call15_doctrine_cues.py` 작성 후 43회 실행(episode 본문 총 9천 자 수준).
3. raised set과 exact 증분 target 목록·수 보고 -> `Δtarget ≤ 300`이면 Call 2 증분 실행.
4. 그 뒤 흡수 조건 assessment 채널.

freeze 유지: §33 probe wiring, participation prompt/model tuning, live Call 2 재실행,
optional excess foreseeability probe, co_principal unreachable mode(marker 보존).

## 2026-08-13 Call 1.5-D doctrine activation: 실행과 첫 active doctrine

**active doctrine 0이 처음으로 깨졌다(1건).** 정본 audit는
`experiments/v2_call15_directscope_26_causal/doctrine_e2e_v11/audit.md`다.

관통 확인 범위는 `cue TRUE -> RaisedDoctrine -> doctrine leaf Call 2 target -> leaf truth ->
active doctrine`까지다. 그 다음(stage effect -> liability)은 `r14_p2_q1` 乙의 elements가
unresolved라 unlawfulness가 not_reached이기 때문에 실행되지 않았다. 이것은 doctrine handoff
결함이 아니라 stage ordering이 정상 작동한 결과이므로 doctrine 축은 여기서 사실상 freeze한다.
KCL-26의 우연한 predicate truth가 elements를 통과해 주어야만 architecture를 승인할 이유는 없다.

### 실행 결과

- Call 1.5-D v4: 43/43 episode, cue 13개, **UNKNOWN 0**, TRUE 10건.
- raised doctrine 9건(6종). `NOT_MATERIALIZED` 5건 -- 전부 피해자이거나 해당 episode에 instance가
  없는 행위자다. identity gate가 실제로 일한다.
- Δ Call 2 target **19** (게이트 300). 534 -> 553.
- Scallop: active doctrine 1, established 19 유지(변화 없음, trace로 설명됨).
- `candidate_doctrine_refs` 26문항 합계 **325 -> 9**.

### 두 번의 실패에서 확정된 것

1. **guided-decoding schema에 식별자를 `const`로 못 박는다.** 1차 실행은 43/43이 계약 위반으로
   떨어졌고 원인이 전부 하나였다 -- 모델이 `factual_episode:001`을 `:001`로 되돌려 주었다.
2. **exact-substring 검증은 canonical 문자열 하나로 통일한다.** prompt와 검증이 같은 문자열을
   본다(`canonical_episode_text`). 모델 출력의 개행만 고쳐 통과시키는 repair는 하지 않는다.
   원본 fragment span은 별도로 보존한다.

### cue 카탈로그 v4에서 확정된 경계

- 위전착 cue는 **철회**했다(`raising_status: representation_gap`). 두 번 좁혔는데도 사람의
  동일성 착오를 잡았고 실제로 target 8개를 열었다. `gap.justifying_premise_vs_object_identity`로
  남겼다. 테스트는 "제기 경로 **또는** 명시된 표현 공백"을 요구한다 -- 절대조건이 아니다.
- coercion cue는 문구를 더 조이지 않고 **downstream materialization gate**로 막는다. 주체가 이
  사건의 법적 instance를 가진 행위자가 아니면 leaf를 열지 않는다. 텍스트 의미의 재판단이 아니라
  identity check이므로 compiler의 일이다.

### additive delta merge (신규 계약)

case 단위 교체는 부적절하다. target 19개를 추가하려고 문항 전체를 다시 물으면 무관한 predicate가
stochastic drift로 뒤집힌다(이번에 8개, liability 2건 회귀). 정본은
`scripts/merge_v2_call2_additive_delta.py`이며 append-only다: baseline key overwrite 금지, delta는
baseline에 없던 key만, delta 내 중복 hard-fail, truth마다 `source_run` provenance, 두 run의
model/prompt/evidence-mode fingerprint 비교(baseline manifest 부재 시 명시적 플래그와 기록).

무결성: 22문항 bit-identical, 신규 19, overwrite/삭제/flip 0.

### 다음 세션

**흡수 condition assessment 채널.** 인장위조 규칙은 승인됐으나 조건
(`condition.forged_seal_impression_is_a_constituent_part_of_the_document`)을 물을 곳이 없어 후보가
열려도 UNKNOWN이다. Call 2 target 추가이므로 프롬프트 승인 게이트에 걸린다. 이번 doctrine
경로에서 만든 것들을 그대로 재사용할 수 있다 -- authored 조건 -> target materialize ->
additive delta merge.

`r14_p2_q1`의 elements unresolved는 doctrine 때문에 뚫지 않는다. 원인(구성요건 predicate 6개
UNKNOWN)만 audit에 남겼다.

---

## 2026-08-13 (3) 흡수 condition 채널 -- 관통 완료, freeze

`runtime/concurrence_condition.py` + `scripts/build_v2_concurrence_condition_pairs.py` +
`scripts/run_v2_absorption_condition_pairs.py`. Article 263과 같은 pair carrier이며 ordinary
predicate Call 2에 얹지 않는다.

### 조건 저작에서 확정된 원칙

**각 neural target은 자기 몫의 atomic proposition 하나만 판단한다.** 초안 조건("권한 없이
현출되거나 부정사용된 인영")은 두 명제를 지고 있었고 그중 하나는 흡수되는 쪽 instance의
element였다. 해소 시점에 그 instance가 established라는 사실이 이미 권한 없는 위조·부정사용을
보장하므로, 조건이 지는 것은 관계 하나뿐이다.

- `condition.unauthorized_seal_impression_is_constituent_part_of_document` (subtype-neutral).
  `offense.seal_forgery_or_misuse`가 위조와 부정사용을 한 정의에 담으므로 조건이 그 구별을
  다시 지지 않는다.
- `condition_statement`/`legal_standard`를 규칙에 저작하고 loader가 요구한다. `condition.*`는
  registry definition이 아니라 규칙이 지고 가는 문자열이다.
- `actor_constraint`(rule-level, loader가 명시 저작 요구). host-global invariant로 박지 않는다.
- 프롬프트 음성 사례는 **부재를 부정으로 읽는 경로를 열지 않도록** 저작한다. "원문이 현출 여부를
  밝히지 않으면 제작·보유 사실만으로 현출 또는 비현출을 추론하지 않는다."

### 실행 결과 (`absorption_e2e_v12`)

pair 후보 1건(`r12_p2_q1_da` 甲, binding:004 -> binding:002), 모델 UNKNOWN, 계약 위반 0.
`condition_truths`가 `resolve_concurrence`까지 live로 도착했다. 흡수는 발화하지 않았고 독립된
blocker가 둘이다 -- 이번 run을 직접 막은 것은 establishment 부재(두 위조죄 모두 elements 정지),
그와 별개로 condition이 UNKNOWN이라 성립했더라도 확정되지 않았을 것이다. reducer 분기는 unit
test가 지고 live 데이터가 지지 않는다. E2E 출력의 `concurrence_condition_truths` +
`both_instances_established`가 "도착 안 함"과 "도착했으나 법적 전제 미충족"을 구별한다.

### lineage guard (신규)

정본 E2E는 `--plan`에 참가 병합 plan만 받는다(`require_participation_plan_lineage`).
`evaluation_instance_plan.jsonl`을 넘기면 참가 instance가 조용히 빠져 **오류 없이 다른 답**이
나온다. manifest step 1차, 행 필드 2차, `--allow-non-participation-plan`이 유일한 탈출구.

### 현재 상태 -- substantive reasoning E2E는 닫혔다

Call 1 / 1.5 / 1.5-P / 1.5-D, Call 2 atomic assessment, 참가(성능 gap 알려짐), 간접정범, 기수,
착오(일부 표현 공백), §33, 초과, doctrine activation, 경합·흡수, final responsibility -- 전부
관통. 더 이상 법리를 붙이는 단계가 아니다.

### 다음

정본 결과 -> Final Responsibility 정리 -> **AnswerPlan -> Call 3 -> 26문항 full E2E**.

---

## 2026-08-13 (4) AnswerPlan + Call 3 -- E2E 관통, fidelity 실패 3건 고정

`docs/v2_plan/ANSWERPLAN_SPEC.md`(스키마) + `docs/analysis/v2_call3_prompt_review_ko.md`
(프롬프트 검수, 카드 A~G 전부 승인)가 설계 정본이다. 정본 run은
`experiments/v2_call15_directscope_26_causal/answer_plan_v1/`(26/26)과 `call3_dev_v1/`
(dev 2건 답안 + audit)이며, 관행과 달리 **git에 넣었다** -- 다음 라운드의 전후 비교 기준점이라서다.

### rubric 역설계로 확정한 것

KCL-26 rubric 735항목의 **유형 집계**가 스키마를 결정했다(sealed-24는 문면 미열람, dev 2건만
열람). 결론 23.4% / 언급 20.8% / 판례 15.6% / 법리 14.8% / 쟁점제기 9.7% / 조문 8.8% /
죄수 7.9% / 학설대립 5.4%. 여기서 나온 초안 대비 델타가 7개다 -- decisive finding에
`legal_standard`+`governing_provision` 동봉, 판례 법리 슬롯 신설, 흡수 쌍 **양쪽** 보존,
선결 의존 순서, contested points, 죄명별 명시 결론, 분량은 plan의 쟁점 수로만.

**판례 근거는 우리 카드 코퍼스로 간다.** 데이터셋 gold precedent는 배제 확정 -- oracle이고,
판시사항이 결론을 담고 있고, 문항당 5만 자라 어차피 검색기가 필요하다. 카드 1,848장 중 638장이
판례 유래 명제이고, rubric 판례 항목 115개 중 **113개가 사건번호를 요구하지 않으므로** 형태가
정확히 맞는다. 회수 시점은 **Scallop 이후 plan 조립 시점**이다(Call 2 truth 채널로는 이미
`card_call2_ab_v1`에서 부결).

### 세 개의 잠금 (계약 §4-7/8/9, 테스트가 지킨다)

gold precedent 미열람 / 문항별 rubric 수치 필드 금지 / `contested_points`는
`origin ∈ {authored_doctrine, reviewed_card}`만. 없으면 §6의 P−N ablation이 rule base 기여도가
아니라 평가 자료의 반사가 된다.

### 계약이 잡은 production 결함 5개

전부 실제 결함이었고 전부 고쳤다.

1. **ref fallback.** 파생죄명 25개 전부 `identity` 블록이 없어 죄명이 `derived_offense.*`로
   샜다. 저작된 seed-cue 카탈로그를 라벨 출처로 쓰고, 없으면 폴백하지 않고 **실패**시킨다.
   `derived_offense.special_theft`(특수절도죄)와 `robbery_causing_injury_by_aggravated_result`
   (강도치상죄) 2건은 승인받아 저작 -- join audit이 이미 `UNMAPPED_DERIVED_ARTICLE`로 지목한
   동일 gap이다.
2. **FALSE vs UNKNOWN.** 계약이 predicate 재구성으로 판정해 오탐했다. **gate가 relation
   obligation에서 실패할 수 있으므로** predicate 목록은 증거가 못 된다. gate를 직접 읽는다.
3. **폴백 분기.** 그 수정이 드러낸 것 -- run이 도달하지 못한 instance가 전부 불성립으로
   떨어지고 있었다. 도달 못 한 것은 미확정이다.
4. **원시 record 노출.** 초과·상상적경합·제33조 단서가 dict 그대로 나가 ref가 샜다. 죄명
   산문으로 렌더링. 가담 형태도 `instigator` -> 교사범.
5. **저작 메모 노출.** `canonical_meaning` 5개에 워크시트 주석이 박혀 있었다("death-agnostic
   패턴", "(+NOT())", "아래 B-7"). 저작된 `legal_standard`로 폴백한다.

### Call 3 dev 실행 -- 관통했고 위반 3건

서비스 222907, 문항당 1회, 후처리 0, 2,146/2,171자. 내부 ID 누출 0, 단일 통합 IRAC, 법리·포섭
전개 모두 통과. **흡수 pair와 participation은 이번 2건에 없어 미검증이다.**

카드 회수는 **의도적으로 붙이지 않았다.** 근거 빈약은 이 run의 결함이 아니다.

- **F1** (`r14_p1_q2`): 丙 사기죄가 plan에서 `확정하기 어렵다`인데 최종 결론이 "성립하지
  않는다"로 단정. 가장 강하게 금지한 전환이다.
- **F2** (`r10_p1_q1_ga`): 강간치상죄가 plan에서 `성립하지 않는다`(gate 실패)인데 답안은
  "확정할 수 없다"로 완화. F1과 방향만 반대이고 뿌리는 같다 -- **최종 결론 문단에서 재진술할 때**
  상태 어휘가 anchor를 벗어난다.
- **F3** (`r10_p1_q1_ga`): 준 인용 `대법원 2018도13877 전원합의체`를 "2018. 4. 12. 선고
  **2017도16488** 전원합의체"로 바꿔 썼다.

### 다음 세션

1. 프롬프트 카드 2장 검수(승인 게이트): ① 최종 결론에서도 anchored state를 plan 표현 그대로
   재진술 ② authority citation은 verbatim-only, 날짜·사건번호 보완 금지.
2. 같은 dev 2건 재실행 -> **F1/F2/F3 = 0 확인**.
3. 그때 N 조건 동결. **지금은 동결하지 않는다.**
4. 그 뒤 SPEC §5.5 카드 회수를 붙여 P 조건 실행 -> 26문항 full E2E.
