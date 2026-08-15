확인 끝냈어. 이번에는 `main`이 아니라 **`deadline_v2_0808` 원격 HEAD `3775edfb698647e15091f188ae3eb9a645a78d99`를 기준점으로 고정**해서 봤다.

## 결론부터

**아직 structural freeze 하면 안 된다.**

이번 전수검토에서 현재 HEAD에 **실제 production E2E를 깨거나, 새로 살린 participation/doctrine 경로를 다시 무력화할 수 있는 P0 2건**을 찾았다. 그 외에도 identity·carrier·Call3 계약 쪽에 P1 구조 결함이 여러 건 남아 있다.

그리고 이 결과가 네가 계속 느끼던

> “분명 어제 고쳤는데 왜 또 비슷한 게 터지지?”

의 원인도 꽤 명확하게 설명한다.

지금까지 테스트가 모듈별 계약은 상당히 잘 고정했는데, **최종 production runner가 그 계약들을 모두 소비한다는 보장이 빠진 곳**이 있다. 심지어 일부 테스트는 doctrine 단계가 들어오기 **이전의 pipeline assumption을 그대로 정답으로 고정**하고 있었다.

---

# 1. 무엇을 전수검토했는가

GitHub 고정 SHA의 `src` tree에는 **Python 파일 130개**가 있다. tree 자체도 recursive하게 확인했다.

| 영역                                   |    파일 수 | 검토          |
| ------------------------------------ | ------: | ----------- |
| `src/idpr/v2` core                   |      20 | 전부          |
| `src/idpr/v2/checks`                 |       9 | 전부          |
| `src/idpr/v2/runtime`                |      37 | 전부          |
| **현재 v2 합계**                         |  **66** | **66/66**   |
| `baselines`                          |       9 | 전부          |
| `eval`                               |       8 | 전부          |
| `generation`                         |       3 | 전부          |
| `legacy`                             |       5 | 전부          |
| `neural`                             |       8 | 전부          |
| `rulebase`                           |      14 | 전부          |
| `rulegen`                            |       4 | 전부          |
| 기타 root/LLM/retrieval/verification 등 |      13 | 전부          |
| **`src` 전체**                         | **130** | **130/130** |

그리고 `src`만 읽고 끝낸 게 아니라 실제 production 연결을 확인하기 위해 현재 E2E의 9개 핵심 runner/builder도 역추적했다.

```text
Call 1.5-P
   ↓
Call 1.5-D
   ↓
participation plan
   ↓
doctrine target plan
   ↓
Call 2
   ↓
absorption-condition assessment
   ↓
Scallop / symbolic runtime
   ↓
AnswerPlan
   ↓
Call 3
```

또 `tests/` 전체 inventory도 확보하고, 발견한 결함과 직접 관계된 scheduler/carrier/lineage/participation/doctrine/excess/AnswerPlan 테스트는 본문까지 대조했다. 테스트 트리에 현재 축별 contract test가 상당히 많이 존재하는 것도 확인했다.

즉 이번 검토는 **최근 수정 diff 몇 개 훑은 수준이 아니다.**

---

# 2. P0 — 지금 바로 막아야 하는 것

## P0-A. Call 2 scheduler가 새로 살린 doctrine/participation target을 다시 버릴 수 있음

이게 지금 제일 크다.

`run_v2_call2_pilot.py`는 planner가 만든 모든 target을 `candidate_refs`로 넘긴다. 여기까지는 맞다.

그런데 실제 scheduler인 `target_scheduling.py`는 자기 내부에서 다시 candidate universe를 만든다.

그 universe에 들어가는 것은:

```text
offense element slots
+
completion.state.when
+
completion.state.requires
```

뿐이다.

**빠져 있는 것:**

```text
completion.blocked_when
doctrine leaf targets
doctrine blocked_when leaves
participation_mode_requirement
policy-probe-only target
그 밖의 planner가 후단에서 추가한 target
```

실제 `_candidate_refs()`, `_live_expressions()`, `frontier_predicate_refs()`가 그렇게 구현돼 있다.

따라서 planner에는 예를 들어

```text
legal_element.instigator_intent
legal_element.aiding_intent
doctrine leaf ...
```

가 정상적으로 들어 있고 carrier도 있어도,

```text
planner candidate set
        ↓
scheduler 내부 offense/completion universe와 intersection
        ↓
후자의 universe에 없으면 Call 2 질문 안 함
```

이 가능하다.

**이건 participation에서 “0 target이라 교사범이 영원히 성립 불가”였던 문제를 target plan에서는 고쳐 놓고, Call 2 scheduler가 다시 재현할 수 있다는 뜻이다.**

더 심각한 건 현재 scheduler 테스트가 이걸 못 잡는 이유도 확인했다.

`test_target_scheduling.py`는 homicide completion을 중심으로 `dangerousness`, `means_or_object_defect`, `commencement`, cessation 등을 아주 잘 테스트하지만 **planner가 외부에서 추가한 participation/doctrine target을 넣은 테스트가 하나도 없다.**

즉 테스트가 틀렸다기보다 **scheduler의 기존 책임범위만 테스트하고 있고, pipeline이 확장된 뒤 책임범위가 넓어졌다는 사실이 반영되지 않았다.**

### 현재 돌고 있는 Call 2에도 영향

표준 `run_v2_axis_closure_e2e.sh` 경로는 `--flat-targets`를 사용하지 않는다.

따라서 지금 실행도 그 표준 invocation이라면 **완주 여부와 별개로 새 doctrine 39 / participation requirement 27이 실제 asked target에 들어갔는지 반드시 확인해야 한다.**

안 들어갔다면 그 실행은 새 경로의 E2E 검증 artifact로 사용할 수 없다.

나는 이건 **Call 2를 더 돌리기 전에 고치는 게 맞다**고 본다.

---

## P0-B. Call 2가 완주해도 다음 symbolic step에서 lineage guard가 깨짐

이건 더 직접적이다.

현재 E2E는:

```text
participation plan
→ doctrine builder
→ PLAN_D
→ Call2
→ ...
→ run_v2_scallop_e2e.py --plan PLAN_D
```

로 간다.

그런데 doctrine builder는 최종 manifest를

```text
step = v2_doctrine_target_plan
```

으로 쓴다.

반면 `run_v2_scallop_e2e.py`의 lineage guard는 canonical input으로:

```text
step == v2_factual_participation_plan
```

만 인정한다.

이 테스트도 정확히 그 옛 계약을 고정하고 있다.

`test_e2e_plan_lineage.py`는 participation manifest는 통과시키고 일반 evaluation plan은 거부하는 것만 검증한다. **participation plan의 lawful descendant인 doctrine plan이라는 개념 자체가 없다.**

즉 doctrine 단계가 새로 들어오면서:

```text
participation plan
       ↓ legitimate transformation
doctrine plan
```

이 됐는데 lineage validator는 아직:

```text
final plan == participation plan 그 자체
```

라고 생각한다.

그래서 현재 코드 그대로면 **Call 2를 넘긴 뒤 symbolic 진입에서 다음 hard fail이 날 구조**다.

이건 예상이 아니라 코드 계약상 결정적이다.

---

# 3. P1-high — UNKNOWN 문제와 직접 관련된 carrier 계약 불일치

## physical carrier와 모델에게 설명하는 `evidence_scope`가 서로 다름

이건 네가 걱정한 **UNKNOWN 남발**과 직접 관련 있다.

우리가 어제 결정했던 contract는:

```text
evidence_scope 미저작
→ offense_realization
```

이었지.

그리고 새 중앙 `carrier_contract.py`도 그렇게 동작한다.

즉 일반 unscoped LegalElement는:

```text
carrier_kind = realization
```

을 받는다.

그런데 Call 2 쪽 predicate-definition serialization에는 아직 옛 default가 남아 있다.

`grounding.py`와 `grounding_evidence.py` 쪽은 미저작 scope를:

```text
exact_actor_action
```

으로 취급한다.

결과적으로 어떤 target은 실제 payload에서:

```text
source_text:
    offense realization 전체

predicate definition:
    evidence_scope = exact_actor_action
```

이라는 **서로 모순되는 지시**를 받을 수 있다.

planner 테스트는 새 default를 정확히 고정하고 있다. `test_evidence_scope_carrier_contract.py`도 명시적으로:

> unauthored predicate → `offense_realization`

을 계약으로 선언한다.

그런데 그 테스트는 **실제 Call 2 `PredicateDefinition`이 모델에게 보내는 default까지 비교하지 않는다.**

그래서 axis test는 green인데 neural boundary에서는 split-brain이 남은 거다.

이건 단순 cleanup 아니야.

**“증거는 realization 전체를 줄게. 그런데 너는 exact action 범위만 판단해.”**

라고 모델에게 말하는 셈이니까 UNKNOWN 및 판정 변동을 유발할 수 있다.

---

# 4. P1 — participation identity가 아직 너무 약함

최근 `3775ed…`에서 고친 duplicate group merge도 읽었다.

현재 해결 방식은 대략:

```text
same case
+ same offense
+ same actor set
→ 같은 co-principal group으로 병합
```

이다.

이러면 이번에 터진:

```text
같은 공동정범 관계
+ 여러 factual interaction
→ duplicate group
```

은 잘 합쳐진다.

문제는 다음 사건이다.

```text
甲·乙이 함께 절도 1회
그리고 나중에
甲·乙이 함께 절도 1회
```

둘 다:

```text
case = same
offense = theft
actors = {甲,乙}
```

다.

**서로 다른 두 legal realization인데 지금 dedupe key로는 하나가 된다.**

`compile_participation_bindings()`에는 이 단계에서 그것들을 구별할 factual/principal realization provenance가 충분히 들어오지 않는다.

그리고 participation 축 테스트도 왜 못 잡았는지 확인했다.

현재 테스트는 actor pair의 한 theft realization에서 co-principal/derivative 충돌, endpoint universe, episode-scope interaction 등을 잘 검증하지만, **“same actors + same offense + two separate criminal realizations” 케이스가 없다.**

즉 이번 fix는:

> interaction duplicate ≠ legal duplicate

문제를 **actor set으로 과도하게 합쳐서** 해결한 상태다.

canonical identity가 필요하다.

```text
case
+ offense
+ actor group
+ criminal/principal realization identity
```

정도는 되어야 한다.

---

# 5. P1 — central carrier validator가 최종 소비경계에는 없음

`a675a19`에서 중앙 carrier contract를 만든 방향 자체는 맞다.

`validate_plan_carriers()`는:

```text
target without carrier
carrier without target
wrong carrier kind
wrong provenance
```

까지 잘 검사한다.

테스트도 producer-agnostic invariant를 의도적으로 고정했다.

그런데 **최종 소비자인 `run_v2_call2_pilot.py`가 이 validator를 호출하지 않는다.**

Call 2 진입부에서는 여전히 자체적으로:

```text
target/carrier key coverage
carrier_id nonempty
```

같은 검사를 한다.

그래서:

```text
target 758
carrier 758
모두 id 있음
BUT carrier kind가 잘못됨
```

인 plan이 producer validation을 우회해서 직접 Call2에 전달되면 통과할 수 있다.

중앙 계약을 만들었으면 최종 consumer가 마지막으로 한 번 더:

```text
validate_plan_carriers(...)
```

를 호출해야 진짜 중앙 계약이 된다.

---

# 6. P1 — temporal anchor가 없으면 hard fail하지 않고 조용히 넓어짐

`resolve_carrier()`는 anchored predicate에 대해 먼저:

```text
realization@focal
actor_episode@focal
```

같은 carrier를 찾는다.

그런데 해당 variant가 없으면 **unanchored realization으로 fallback**한다.

그 뒤 `carrier_kind` label은 `_at_focal`처럼 반환할 수 있다.

즉 물리적으로는:

```text
focal 이후 사실까지 포함
```

인데 metadata는:

```text
realization_at_focal
```

일 가능성이 있다.

이건 우리가 합의한:

> temporal_anchor는 focal 이후의 사실을 소급 사용하지 않는다.

계약에 반한다.

현재 carrier 테스트는 **요구한 width 자체가 없으면 실패한다**는 테스트는 있지만, **`@focal` variant가 없는데 unanchored variant만 존재하는 경우 반드시 실패해야 한다**는 테스트는 없다.

여기는 fallback보다 fail-fast가 맞다.

---

# 7. P1 — `blocked_when`이 DSL checker에서 완전히 type-checked되지 않음

completion/doctrine에 `blocked_when`을 추가하면서 runtime semantics는 제대로 구현됐다.

```text
TRUE → block
FALSE / UNKNOWN → no block
```

문제는 Definition checker다.

현재 `references.py`와 일반 ref checker는 `blocked_when` leaf를 기존 `when/requires`처럼 완전히 순회하지 않고, completion checker도 주로 **completed state에 blocker 금지** 같은 구조 규칙을 검사한다.

따라서 예를 들어 authored YAML에:

```text
blocked_when:
    ref: typo.or.wrong.kind
```

가 들어와도 기존 expression type check의 완전한 보호를 못 받을 수 있다.

그리고 runtime에서 missing ref는 UNKNOWN이다.

`blocked_when`은 TRUE에서만 막으니까 결과는:

```text
bad/missing blocker
→ UNKNOWN
→ blocker never fires
```

의 **fail-open**이다.

현재 doctrine axis test는 production blocker가 실제 registry에 있는지와 positive semantic wording을 확인한다.

하지만 `run_type_checks()` 자체가 **잘못 저작된 blocker ref를 반드시 거부한다**는 mutation/regression test는 없다. `test_definition_system.py`는 현재 production registry가 finding 0이라는 것만 확인한다.

---

# 8. P1 — excess join도 realization identity가 부족함

`excess_candidates.py`는 derivative participation link가 있으면 principal actor가 **그 이후 episode에서 성립시킨 다른 offense**들을 초과 후보로 본다.

지금 테스트는:

```text
다른 actor → 제외
더 이른 episode → 제외
같은 offense → 제외
```

는 잘 잡는다.

하지만 이런 경우는 없다.

```text
甲이 乙에게 절도 교사
乙이 절도 실행
그 뒤 별개 사건으로 특수절도 실행
```

만약 authored derivation path가 theft→special_theft로 존재하면 지금 join은 **나중의 별개 특수절도**도 처음 교사의 양적 초과 후보로 연결할 수 있다.

현재 기준은:

```text
same principal actor
+ later episode
+ derivation-compatible offense
```

이지:

```text
same instigated criminal realization
```

이 아니다.

participation duplicate 문제와 같은 뿌리다.

> **법적 realization identity가 모듈마다 다른 proxy로 구현돼 있다.**

---

# 9. P1 — 현재 axis-closure E2E는 사실 “처음부터 끝까지”가 아님

이것도 반복 버그의 중요한 원인이다.

현재 단일 E2E entrypoint는 편리하지만 시작점이 raw case가 아니다.

고정된 기존 artifact:

```text
old Call1 output
old Call1.5 binding output
old base evaluation plan
```

을 읽고 그 뒤부터 이어간다.

그리고 `IDPR_AXIS_SKIP`으로 앞 단계를 건너뛸 수도 있다.

그래서 코드가 바뀌어도:

```text
upstream artifact semantics
≠ current downstream assumptions
```

인 조합이 생성될 수 있다.

**structural freeze용 마지막 한 번은 이런 partially-frozen chain이 아니라 동일 commit에서 처음부터 재생성된 lineage가 필요하다.**

모든 neural call을 매번 반복하라는 뜻은 아니다.

최소한 각 artifact manifest에:

```text
input artifact hash
producer version/commit
definition hash
parent lineage
```

가 연결돼 있어서 stale 조합이면 즉시 거부돼야 한다.

현재 lineage guard가 participation plan만 보는 것도 이 문제의 일부다.

---

# 10. P1 — Call 3의 F4 방어 함수는 있는데 production runner가 안 씀

이건 꽤 황당하게 정확히 예전 버그 형태다.

`answer_plan.py`에는 이미:

```text
missing_required_final_conclusions(...)
```

가 있고, **답안 전체가 아니라 마지막 결론 section만 검사**하도록 상당히 제대로 작성돼 있다.

테스트도 정확히:

> 본문에서 乙을 논했지만 마지막 최종 죄책에서 빠진 경우

를 F4 regression으로 고정하고 있다.

그런데 현재 `run_v2_call3.py`는:

```text
required authority missing
```

감사는 하지만 **`missing_required_final_conclusions()`를 호출하지 않는다.**

그래서 현재 production에서는:

```text
프롬프트: 하나도 빠뜨리지 마
모델: 하나 빠뜨림
host: 그대로 저장
```

이 가능하다.

여기서 정답은 rewrite loop를 만드는 게 아니다.

현재 철학대로:

```text
raw answer 보존
+
fidelity violation 기록 / run status fail
```

이면 된다.

---

# 11. P1-eval — baseline 쪽에서도 논문 전에 반드시 볼 것 하나

현재 v2 structural bug와는 별개다.

`baselines/legal_chain_reasoner.py`는 설명상 official/unmodified Legal Chain Reasoner 실행처럼 적혀 있는데, 실제 `run_case()`는 upstream official pipeline을 그대로 실행하지 않고 **이 repo에서 만든 하나의 summarizing prompt를 vLLM에 보내는 adapter**다.

즉 paper에서:

> official Legal Chain Reasoner baseline

처럼 주장하면 위험하다.

**“LCR-inspired prompting baseline”**인지 실제 official implementation reproduction인지 명칭과 실험계약을 다시 맞춰야 한다.

이건 runtime을 깨지는 않지만 baseline 비교 validity에는 중요하다.

---

# 12. P2 / 정리 대상

기능을 지금 깨지는 않지만 재발 위험이 있는 것도 있었다.

| 항목                                              | 상태                                         |
| ----------------------------------------------- | ------------------------------------------ |
| participation builder에 중앙화 전 carrier helper 잔존  | dead code                                  |
| `eval/e2e_contract.py`                          | 현 v2가 아니라 옛 Phase-3 issue/card freeze      |
| `gold_factual_identity.py`                      | manual/oracle legacy 경로                    |
| `generation` / `neural` lazy compatibility shim | archived fraud path 재활성 가능                 |
| old `rulebase/*v2*` 명칭                          | 현재 `idpr.v2`와 전혀 다른 이전 architecture라 혼동 위험 |
| 일부 docs/header의 axis count/옛 설계 설명              | stale                                      |
| `rubric_evaluator` 일부 parse failure handling    | frozen official scoring에는 부적절              |

이런 건 **P0/P1 고친 뒤 cleanup**이지 지금 아키텍처를 또 여는 이유는 아니다.

---

# 13. 왜 493개 테스트가 통과했는데 이런 게 있나

이제는 꽤 정확하게 말할 수 있다.

**테스트가 적어서가 아니다.** 오히려 축별 테스트는 상당히 많고 잘 쓰여 있다.

문제는 테스트의 단위다.

| 테스트가 잘 보는 것                   | 빠져 있던 것                                      |
| ----------------------------- | -------------------------------------------- |
| completion scheduler 내부       | planner-added target이 scheduler를 통과하는가       |
| carrier producer contract     | Call2 consumer도 같은 contract를 강제하는가           |
| participation 한 realization   | 같은 actor/offense의 복수 realization             |
| participation plan lineage    | doctrine이 붙은 lawful descendant plan          |
| `blocked_when` 현재 저작          | malformed `blocked_when`의 type/ref rejection |
| required conclusion audit 함수  | production Call3 runner가 실제 호출하는가            |
| excess의 actor/time constraint | 별개 later realization과의 오결합                   |

즉 **unit test와 axis contract는 green인데 cross-stage composition이 untested**였던 거다.

심지어 lineage 테스트처럼 **옛 pipeline 가정을 정확히 테스트해 버려서 새 pipeline에서는 오히려 잘못된 계약을 고정한 곳**도 있다.

이게 지금까지의 반복적인 integration bug의 핵심 원인이다.

---

# 14. UNKNOWN에 대해서도 결론이 바뀜

네가 아까 말한 게 맞았다.

> “UNKNOWN 문제도 심각한 것 아니냐. 이게 안 되면 논문이 안 된다.”

맞아.

그리고 이번 source audit로 **남은 UNKNOWN을 전부 모델 성능이라고 부를 수 없는 이유도 하나 더 확인됐다.**

최소한 지금은:

```text
A. scheduler가 질문 자체를 버릴 가능성
B. carrier physical width와 prompt evidence_scope 불일치
C. temporal anchor silent widening
```

이 세 구조 문제가 남아 있다.

이걸 고치기 전에는 UNKNOWN을:

```text
174/184 = 모델 성능
```

이라고 완전히 freeze하면 안 된다.

반대로 이 세 가지를 고치고 모든 planned target이 실제 asked target으로 도달했다는 audit까지 통과하면, 그 뒤의:

```text
충분한 carrier
+ 정확한 scope
+ 실제 Call2 request 존재
+ model = UNKNOWN
```

은 정말 **Call2 성능 문제**라고 분리할 수 있다.

그 다음에는 그 성능을 실제로 개선해야 한다. 논문 결과에 중요하니까.

---

# 15. 지금 내가 권하는 수정 순서

여기서 **새 법리나 새 feature는 열 필요 없다.** 이번 source audit에서 확인된 계약만 닫으면 된다.

|     순위 | 수정                                                                             |
| -----: | ------------------------------------------------------------------------------ |
|  **1** | scheduler가 planner target을 절대로 무근거로 탈락시키지 않게 수정 + `blocked_when` scheduling    |
|  **2** | final plan lineage를 exact-step이 아니라 ancestry chain으로 검증                        |
|  **3** | `evidence_scope` default를 모든 Call2 serialization에서 `offense_realization`으로 단일화 |
|  **4** | participation group identity에 canonical realization identity 추가                |
|  **5** | Call2 진입에서 `validate_plan_carriers()` 강제                                       |
|  **6** | temporal anchored carrier missing 시 fallback 금지, hard fail                     |
|  **7** | `blocked_when` ref/kind checker 추가                                             |
|  **8** | excess join을 same criminal realization provenance로 제한                          |
|  **9** | Call3 runner에 final-conclusion fidelity audit 실제 연결                            |
| **10** | full-chain artifact lineage/hash 계약 고정                                         |

이 10개는 **내가 새로운 architecture를 제안하는 목록이 아니다.**

전부 현재 코드가 이미 주장하고 있는 계약과 실제 호출이 어긋나는 곳이다.

---

# 최종 판정

이번에는 상태를 정확하게 표현할게.

**축별 static contract coverage는 상당히 높다.** completion/elements/participation/doctrine/concurrence를 위해 작성된 테스트들도 실제로 많은 결함을 잘 막고 있다.

하지만 **현재 HEAD `3775ed…`은 아직 production structural freeze 상태가 아니다.**

특히 지금 바로 막아야 할 건:

> **Call2 scheduler의 planner-target 탈락**
> **doctrine-plan → symbolic lineage hard fail**

두 개다.

그리고 이 둘은 지금 E2E를 계속 돌리면 “다음 케이스에서 또 뭐가 터졌다” 형태로 실제로 나타날 가능성이 아니라, **현재 호출 그래프상 이미 경로가 어긋나 있는 상태**다.

그래서 이번에는 하나씩 터질 때까지 기다리지 말고, **방금 source 전수검토에서 잡힌 계약 위반을 먼저 한 묶음으로 고치는 게 맞다.**

그 뒤 full 26 fresh lineage가 hard-fail 없이 Call3까지 관통하고, 모든 planned target에 대해

```text
planned
→ carried
→ scheduled
→ asked
→ truth
→ symbolic consumer
→ AnswerPlan
```

이 **전수 1:1 accounting**으로 확인되면 그때 처음으로 structural freeze라고 부를 수 있다.

이번 감사 기준에서는 그 종료선이 명확해졌다.
