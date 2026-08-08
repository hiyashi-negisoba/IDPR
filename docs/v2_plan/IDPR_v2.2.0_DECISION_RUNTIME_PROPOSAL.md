# IDPR v2.2.0 Decision Runtime Proposal

**Status:** Proposed  
**Version:** v2.2.0  
**Prerequisite:** IDPR v2.1.0 Definition / Type System  
**Target backend:** Scallop  
**Scope:** compiled legal program 이후의 case-time neuro-symbolic decision runtime

---

## 0. Executive Summary

IDPR v2.1.0이 **법률을 어떻게 정의하고 typed legal program으로 compile할 것인가**를 다룬다면 v2.2.0은 **컴파일된 법률 프로그램을 구체적 사건에 어떻게 적용할 것인가**를 다룬다.

```text
Case
  ↓
Call 1: High-Recall Offense Routing
  ↓
Offense Seeds
  ↓
Compiler-Driven Closure / Probe Generation
  ↓
Call 2: GroundFact Grounding
  ↓
Impossibility-Only Pruning
  ↓
Call 3: LegalElement Assessment
  ↓
Lean Symbolic Execution
  ↓
LiabilityResult
  ↓
Writer
```

핵심 원칙은 네 가지다.

> **Call 1은 최소한의 high-recall router다.**

> **Call 2는 사건의 factual structure만 grounding한다.**

> **Call 3는 canonical LegalElement를 legal standard에 따라 평가한다.**

> **Symbolic runtime은 최대한 lean하게 유지하며 실제 법적 effect와 liability만 계산한다.**

---

# 1. Goals

v2.2.0은 다음을 목표로 한다.

1. 쟁점 라우팅의 recall을 최대한 유지한다.
2. unnecessary branches는 compiler와 factual grounding을 이용해 안전하게 제거한다.
3. factual extraction과 legal evaluation의 책임을 분리한다.
4. neural call을 최대 3회로 제한한다.
5. legal effect와 liability composition은 symbolic runtime이 담당한다.
6. symbolic runtime은 generation을 위해 불필요한 구조를 추가하지 않는다.
7. 각 단계의 오류를 독립적으로 localization할 수 있게 한다.
8. 변호사시험형 사례에서 작은 가능성도 성급하게 제거하지 않는다.
9. writer policy는 symbolic correctness / coverage 확인 후 calibration한다.

---

# 2. Three-Call Architecture

## 2.1 Call 1 — High-Recall Offense Routing

Call 1의 역할은 하나다.

> **사건에서 검토할 가능성이 있는 offense definition의 seed를 넓게 선택한다.**

Call 1은 factual extraction도 legal element assessment도 하지 않는다.

권장 최소 output:

```text
LegalSeed {
    definition_id
}
```

예:

```text
[
    "offense.fraud",
    "offense.embezzlement"
]
```

모델이 표면적으로 죄명 또는 조문명을 출력하더라도 host layer에서 canonical `OffenseDef` ID로 resolve할 수 있다.

Call 1이 출력하지 않는 것:

```text
actor
event
fact span
confidence
rationale
participation mode
doctrine
legal element
verdict
```

Call 1의 성공 기준은 exact issue matching이 아니다.

```text
Gold offense g
seed s

success iff
g ∈ closure(s)
```

즉 핵심 metric은 **gold legal path가 compiler closure 이후에도 살아 있는가**다.

---

# 3. Call 1 Pilot Calibration

v2.2.0 구현 전에 소규모 pilot test를 수행한다.

목적은 모델이 얼마나 세밀한 granularity로 offense candidate를 분리하는지 확인하고 Call 1 contract를 조정하는 것이다.

권장 규모:

```text
20–30 representative cases
```

확인 항목:

```text
- base offense까지 잡는가
- qualified / derived offense까지 직접 잡는가
- 경쟁 죄명을 얼마나 넓게 제시하는가
- 완전히 무관한 죄를 얼마나 추가하는가
- 복수 행위자가 있는 사건에서 offense candidate를 어떻게 나누는가
- base offense만 잡았을 때 compiler closure가 gold path를 복구하는가
```

pilot의 목적은 학습이 아니라 **router contract calibration**이다.

결과에 따라 다음을 조정할 수 있다.

```text
maximum candidate count
surface offense naming policy
canonical ID resolver
router prompt strictness
```

---

# 4. Compiler-Driven Activation

Call 1 output은 hard gate가 아니다.

Router가 offense seed를 주면 compiler가 v2.1.0의 legal definition graph를 이용해 필요한 구조를 확장한다.

```text
IssueSeed
    ↓
Structural Closure
    ↓
Core + Probe Frontier
```

activation을 위해 별도의 수작업 legal knowledge를 중복 작성하지 않는다.

> **Activation metadata should not duplicate legal knowledge already encoded in definitions.**

---

# 5. Offense-Side Closure

Offense-side expansion은 v2.1.0의 derivation structure에서 compiler가 자동 유도한다.

```text
D = QUALIFY(B, Q)
delta(D, B) = additions introduced by Q
```

```text
D = COMPOSE(B, C, R)
delta(D, B) = C + R
```

compiler는 이 delta에서 Call 2로 평가할 수 있는 minimal GroundFact frontier를 찾아 probe를 만든다.

예:

```text
COMPOSE(
    robbery,
    injury_result,
    causal_nexus
)
```

에서:

```text
probe = injury_result
```

`causal_nexus` 같은 evaluative relation은 Call 3로 defer한다.

---

# 6. Probe-Guided Legal Closure

v2.2.0은 neighboring legal structure를 처음부터 full activation하지 않는다.

```text
neighboring structure
        ↓
minimal factual probe
        ↓
Call 2
        ↓
probe survives?
        ↓
conditional expansion
```

개념적 closure state:

```text
MANDATORY
PROBE
CONDITIONAL
DEFERRED
```

- **MANDATORY**: seed 자체를 판단하는 데 필요한 core definition과 structural dependencies.
- **PROBE**: 인접한 qualified / composed / completion / participation / doctrine branch의 가능성을 확인하기 위한 factual frontier.
- **CONDITIONAL**: probe가 살아남으면 full branch를 활성화.
- **DEFERRED**: 법적 평가가 필요한 relation이나 LegalElement로 Call 3까지 미룸.

---

# 7. Doctrine Activation

Doctrine에는 별도의 manually authored `activation_signature`를 두지 않는다.

```text
DoctrineDef<SelfDefense> {
    stage: Unlawfulness

    requires:
        current_unlawful_attack
        defensive_act
        proportionality
}
```

compiler는 doctrine의 existing requirements를 역으로 추적해 GroundFact frontier를 계산한다.

```text
DoctrineDef
    ↓ dependency traversal
GroundFact probe set
```

doctrine activation은 다음을 사용한다.

```text
stage-level doctrine pool
+
compiler-derived factual probes
```

Call 1이 doctrine을 직접 예측할 필요는 없다.

---

# 8. Call 2 — GroundFact Grounding

Call 2의 역할:

> **사건을 typed factual representation으로 옮긴다.**

입력:

```text
Case
+
deduplicated GroundFactDefs
    ├─ core facts
    └─ probe facts
```

출력:

```text
CaseGrounding {
    entities
    events
    facts
}
```

Call 2가 actor, entity, event, relation binding을 담당한다.

예:

```text
Entity:
    甲 : person
    乙 : person
    A  : person

Event:
    e1 : statement
    e2 : transfer

GroundFact:
    false_statement(
        actor=甲,
        victim=A,
        event=e1
    )

    property_transfer(
        from=A,
        to=甲,
        event=e2
    )
```

---

# 9. Call 2 Responsibility Boundary

Call 2는 factual interpretation만 한다.

허용:

```text
entity resolution
coreference resolution
event extraction
actor-event binding
property binding
temporal binding
factual inference
```

금지:

```text
fraud committed
aiding established
self-defense applies
robbery-level threat exists
legal causal nexus satisfied
guilty / not guilty
```

> **FACTUAL INTERPRETATION is allowed. LEGAL EVALUATION is not.**

---

# 10. GroundFact Assessment Semantics

권장 상태:

```text
explicitly_supported
inferentially_supported
contradicted
unresolved
```

단 `inferentially_supported`는 factual inference만 의미한다.

```text
absence of evidence
≠
evidence of absence
```

사건에 무기 사용이 언급되지 않았다는 이유만으로:

```text
weapon_used = contradicted
```

라고 하면 안 된다.

기본은:

```text
weapon_used = unresolved
```

이다.

---

# 11. Fact-Aware Pruning

Call 2 이후 compiler/runtime는 factual grounding을 이용해 branch를 prune한다.

v2.2.0에서 pruning은 일반적인 relevance filtering이 아니다.

> **Pruning requires a proof of impossibility, not a lack of support.**

현재 grounding 아래에서 법적으로 가능한 derivation이 하나라도 남아 있으면 branch를 보존한다.

---

# 12. Three-Valued Pruning Semantics

Call 2 상태를 pruning 시 다음처럼 추상화한다.

```text
explicitly_supported
inferentially_supported
        ↓
       TRUE

contradicted
        ↓
       FALSE

unresolved
        ↓
      UNKNOWN
```

```text
ALL(A, B)

FALSE present      → FALSE
all TRUE           → TRUE
otherwise          → UNKNOWN
```

```text
ANY(A, B)

TRUE present       → TRUE
all FALSE          → FALSE
otherwise          → UNKNOWN
```

```text
NOT(TRUE)    → FALSE
NOT(FALSE)   → TRUE
NOT(UNKNOWN) → UNKNOWN
```

branch state:

```text
TRUE     → OPEN
FALSE    → PRUNE
UNKNOWN  → KEEP
```

---

# 13. Pruning Must Respect Alternative Legal Forms

offense family 전체를 조기에 제거하면 안 된다.

```text
Completed Fraud
    disposition = FALSE
→ PRUNE
```

하지만:

```text
Attempted Fraud
→ may remain KEEP / OPEN
```

따라서:

```text
OffenseFamily
├─ CompletedForm     PRUNED
└─ AttemptForm       KEEP
```

이면 offense family 자체는 살아 있어야 한다.

> **A parent branch may be pruned only when every legally valid child derivation is impossible.**

이 원칙은 completion, participation, qualifier, composition에도 동일하게 적용한다.

---

# 14. No Semantic Scheduling in v2.2.0

v2.2.0에서는 surviving branch를 중요도에 따라 model-based hard scheduling하지 않는다.

```text
PRUNE
= proven impossible

KEEP / OPEN
= Call 3 eligible
```

비용은 다음으로 줄인다.

```text
predicate deduplication
dependency-aware batching
context packing
shared-standard grouping
```

semantic importance에 따른 추가 pruning은 v2.2.0 범위에서 제외한다.

---

# 15. Call 3 — LegalElement Assessment

Call 3의 logical evaluation unit은 하나의 canonical `LegalElementDef`다.

이 단위는 orchestration layer가 보장한다.

입력:

```text
canonical LegalElement proposition
+
supplied legal standard
+
Call 2 GroundFacts
```

출력:

```text
LegalElementAssessment
```

---

# 16. Call 3 Required Contract

Call 3 prompt의 exact wording은 구현 영역에 맡긴다.

다만 다음 invariant는 반드시 지켜야 한다.

## 16.1 Canonical proposition orientation

Call 3는 주어진 canonical proposition의 truth만 평가한다.

## 16.2 No legal effect exposure

Call 3가 알 필요가 없는 정보:

```text
component
bar
waiver
boundary
DEFEAT
EXEMPT
final offense result
final verdict
```

## 16.3 Standard and facts are separated

```text
Target Proposition
Legal Standard
Relevant GroundFacts
```

Call 3의 역할은 supplied legal standard를 grounded facts에 적용하는 것이다.

## 16.4 GroundFacts are the factual substrate

Call 3는 Call 2의 GroundFacts를 primary factual substrate로 사용한다.

원문 제공 여부는 experimental variable로 둔다.

```text
A. GroundFacts only
B. GroundFacts + evidence spans
C. GroundFacts + full case
```

어떤 variant를 쓰더라도 새로운 factual premise를 조용히 생성해서는 안 된다.

## 16.5 Rationale-first

```text
legal standard 이해
→ relevant facts 확인
→ standard-to-fact application
→ rationale
→ evidence state 결정
```

## 16.6 Evidence state

```text
explicitly_supported
inferentially_supported
contradicted
unresolved
```

## 16.7 GroundFact provenance

```text
LegalElementAssessment {
    target
    evidence_state
    supporting_ground_facts
    rationale
}
```

## 16.8 Call 3 must not repair the legal program

Call 3는 supplied `LegalElementDef` 또는 legal standard를 수정·보충·대체하지 않는다.

```text
invalid schema / type
→ validation error

valid but indeterminate
→ unresolved
```

---

# 17. Lean Symbolic Runtime

Call 3 이후부터 symbolic runtime이 actual legal composition을 수행한다.

> **The symbolic runtime should remain as lean as possible.**

Symbolic runtime이 해야 하는 것:

```text
logical composition
completion resolution
participation / attribution
stage effects
offense realization
offense establishment
punishability
liability determination
```

Symbolic runtime이 하지 않는 것:

```text
issue importance ranking
answer ordering
hypothetical branching
alternative argument generation
discourse planning
writer-specific reasoning expansion
```

---

# 18. Direct Participation and Attribution

```text
Participation
├─ DirectParticipation
│  ├─ principal
│  └─ co_principal
│
└─ DerivativeParticipation
   ├─ instigator
   └─ aider
```

공동정범은 attribution semantics를 가진다.

```text
Direct Participation Resolution
        ↓
Attribution
        ↓
Actor-specific factual / legal view
```

> **Attribution precedes actor-specific Completion and Elements.**

---

# 19. Completion Resolution

Attribution 이후 actor/offense별 Completion을 resolve한다.

```text
OffenseDef
+
CompletionPolicy
+
Case assessments
+
Attributed components
↓
CompletionResult
```

```text
OffenseDef<X>
×
CompletionForm<F>
→
OffenseFormInstance<X, F>
```

Completion은 어떤 element expression을 평가할 것인지 결정한다.

---

# 20. Elements Aggregation

입력:

```text
GroundFacts
LegalElementAssessments
Attributed components
CompletionResult
```

출력:

```text
ElementsResult {
    actor
    offense
    form

    state:
        satisfied
        failed
        unresolved

    provenance
}
```

aggregation은 v2.1.0의 `ALL / ANY / NOT / ONE_OF` semantics를 따른다.

---

# 21. Unlawfulness and OffenseRealization

```text
Elements = satisfied
+
Unlawfulness = preserved
↓
OffenseRealization
```

`OffenseRealization`은 derivative participation이 참조할 수 있는 typed legal state다.

---

# 22. Derivative Participation

교사와 방조는 principal conduct attribution으로 처리하지 않는다.

```text
CoPrincipal
→ attribution

Instigator / Aider
→ derivative liability
```

예:

```text
requires:
    OffenseRealization<Principal, X>
```

accessory는 자기 own stage path를 가진다.

```text
Principal OffenseRealization
        ↓
Derivative Participation
        ↓
Accessory Elements
        ↓
Accessory Unlawfulness
        ↓
Accessory OffenseRealization
        ↓
Accessory Culpability
        ↓
Accessory Punishability
```

> **Derivative participation depends on a typed principal legal state. It does not copy the principal's LiabilityResult.**

---

# 23. Final Stage Execution

각 actor/offense path는 최종적으로 다음을 따른다.

```text
Elements
    ↓
Unlawfulness
    ↓
OffenseRealization
    ↓
Culpability
    ↓
OffenseEstablishment
    ↓
Punishability
    ↓
LiabilityResult
```

각 actor는 자기 own `Unlawfulness / Culpability / Punishability`를 유지한다.

---

# 24. No Symbolic Alternative Trace

v2.2.0 symbolic runtime은 hypothetical / alternative trace를 별도로 생성하지 않는다.

예:

```text
Elements = unresolved
```

이면 symbolic result는 그대로:

```text
Elements = unresolved
Unlawfulness = not_reached
Culpability = not_reached
```

이다.

symbolic runtime이 hypothetical branch를 다시 실행하지 않는다.

> **Alternative reasoning is a generation-layer discourse operation, not a symbolic execution mode.**

---

# 25. Writer Boundary

Writer는 symbolic runtime 이후에 위치한다.

writer가 어떤 context를 받을지는 v2.2.0 구현 후 empirical calibration 대상으로 둔다.

후보:

```text
W1
Case
+
Symbolic Results
```

```text
W2
Case
+
GroundFacts
+
LegalElementAssessments
+
Symbolic Results
```

```text
W3
W2
+
Relevant Legal Standards / Definitions
```

또한:

```text
full case
vs
evidence spans only
```

도 별도 실험 변수로 둘 수 있다.

v2.2.0 단계에서 writer constraint를 고정하지 않는다.

결정은 다음을 보고 내린다.

```text
symbolic correctness
symbolic coverage
error localization
noise / over-expansion
writer consistency
```

---

# 26. Responsibility Localization

```text
쟁점 seed를 놓침
→ Call 1 / activation

필요한 derived branch가 열리지 않음
→ compiler closure / probe

사실을 잘못 추출함
→ Call 2

가능한 branch를 잘못 prune함
→ pruning semantics

사실은 맞지만 법적 기준 적용을 틀림
→ Call 3

assessment는 맞지만 liability가 틀림
→ symbolic program / compiler

liability는 맞지만 설명이 틀림
→ writer
```

---

# 27. Runtime Overview

```text
CASE
 │
 ▼
Call 1
High-Recall Offense Routing
 │
 ▼
Offense Seeds
 │
 ▼
Compiler Structural Closure
 │
 ├─ mandatory core
 ├─ offense probes
 ├─ doctrine probes
 ├─ completion probes
 └─ participation probes
 │
 ▼
Call 2
GroundFact Grounding
 │
 ▼
Impossibility-Only Pruning
 │
 ▼
Surviving LegalElementDefs
 │
 ▼
Call 3
LegalElement Assessment
 │
 ▼
Direct Participation / Attribution
 │
 ▼
Completion
 │
 ▼
Elements
 │
 ▼
Unlawfulness
 │
 ▼
OffenseRealization
 │
 ├─ derivative participation dependencies
 │
 ▼
Culpability
 │
 ▼
OffenseEstablishment
 │
 ▼
Punishability
 │
 ▼
LiabilityResult
 │
 ▼
Writer
```

실제 구현은 actor/offense별 typed dependency DAG로 구성할 수 있다.

---

# 28. Acceptance Criteria

## Call 1
- offense seed 수준으로 제한된다.
- actor / fact / doctrine extraction을 수행하지 않는다.
- pilot calibration이 수행된다.
- closure-based survival을 평가할 수 있다.

## Activation
- QUALIFY / COMPOSE derivation에서 probe를 자동 유도할 수 있다.
- doctrine에 별도 activation signature를 요구하지 않는다.
- existing legal definitions에서 probe를 계산한다.
- activation knowledge를 중복 작성하지 않는다.

## Call 2
- entity / event / actor binding을 생성한다.
- GroundFact vocabulary에 맞춰 사건을 grounding한다.
- legal evaluation을 수행하지 않는다.
- unresolved와 contradicted를 구분한다.
- factual provenance를 유지한다.

## Pruning
- FALSE가 증명된 branch만 제거한다.
- UNKNOWN은 유지한다.
- completion / participation alternative가 살아 있으면 parent offense를 제거하지 않는다.
- lack of support만으로 branch를 제거하지 않는다.

## Call 3
- canonical LegalElement만 평가한다.
- downstream legal effect를 보지 않는다.
- legal standard와 GroundFacts를 분리한다.
- rationale-first protocol을 따른다.
- evidence state와 GroundFact provenance를 반환한다.
- legal program을 repair하지 않는다.

## Symbolic Runtime
- completion / participation / stage effect / liability만 수행한다.
- hypothetical discourse branch를 만들지 않는다.
- actor-specific stage path를 유지한다.
- derivative participation은 typed principal dependency를 사용한다.
- writer convenience를 위해 불필요하게 확장되지 않는다.

## Writer
- v2.2.0 core runtime 이후 calibration한다.
- symbolic correctness / coverage를 보고 context variant를 결정한다.
- alternative argument generation은 writer의 역할로 남긴다.

---

# 29. Proposed Implementation Order

v2.1.0 구현 및 검증 이후 v2.2.0을 시작한다.

```text
1. Call 1 pilot calibration
2. minimal offense seed router
3. closure / probe compiler
4. GroundFact request planner
5. Call 2 grounding schema
6. impossibility-only pruner
7. LegalElement request planner
8. Call 3 assessment contract
9. direct participation / attribution runtime
10. completion runtime
11. stage execution
12. derivative participation runtime
13. LiabilityResult integration
14. symbolic correctness / coverage audit
15. writer-context ablation
```

---

# 30. Summary

v2.2.0은 compiled criminal-law program 위에서 사건별 의사결정을 수행하는 neuro-symbolic runtime을 정의한다.

```text
Call 1
"What offenses may matter?"

Call 2
"What happened?"

Call 3
"What do those facts mean under the supplied legal standard?"

Symbolic Runtime
"What legal consequence follows?"

Writer
"How should this reasoning be expressed?"
```

핵심 원칙:

```text
high-recall routing
compiler-driven activation
probe-guided closure
impossibility-only pruning
canonical LegalElement assessment
lean symbolic execution
generation-layer discourse freedom
```

---

## Proposed Decision

**Adopt IDPR v2.2.0 as the target case-time decision architecture after v2.1.0 implementation and validation.**

개발은 반드시 v2.1.0의 Definition Language / Typed Legal IR / compiler foundation부터 시작한다.

v2.2.0은 그 foundation 위에 올라가는 후속 runtime milestone로 취급한다.
