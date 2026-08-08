# IDPR v2.1.0 Design Proposal

**Status:** Proposed  
**Version:** v2.1.0  
**Target backend:** Scallop  
**Purpose:** v1의 article/unit-centric RuleIR을 대체할 compositional criminal-law representation과 neuro-symbolic runtime을 제안한다.  
**Scope:** 형법 중심. 조문번호와 개별 법리의 최종 매핑은 본 문서의 범위 밖이며 별도 법률 검수 단계에서 확정한다.

---

## 0. Executive Summary

IDPR v2.1.0은 법률지식의 정의와 구체적 사건의 판단을 분리한다.

핵심 구조는 다음과 같다.

```text
Definition Language
    ↓ compile
Typed Legal IR
    ↓ backend compilation
Scallop Program
    ↓ case grounding
Neuro-Symbolic Runtime
    ↓
LiabilityResult
```

v1은 법률 단위별 predicate와 rule을 직접 구성하고 neural assessment가 각 predicate의 충족 여부를 판단한 뒤 symbolic engine이 issue-level outcome을 합성하는 구조였다. 이 구조는 작동했지만 다음 문제가 반복되었다.

- 동일하거나 유사한 법적 관념이 죄종별 predicate로 중복된다.
- predicate의 truth orientation과 법적 효과가 혼합될 수 있다.
- `component`, `bar`, `waiver`, `boundary` 같은 역할 정보가 neural assessment에 노출되면서 판단 극성이 뒤집힐 수 있다.
- 미수와 공범처럼 구성요건 판단 이전에 개입하는 구조를 단순 후처리로 표현하기 어렵다.
- 다른 issue 또는 module에 대한 dependency가 문자열 수준으로 연결되어 누락 가능성이 있다.
- article-specific RuleIR이 늘어날수록 법적 구조의 재사용성이 낮아진다.

v2.1.0의 핵심 원칙은 다음 한 문장으로 요약한다.

> **Neural models may ground facts and evaluative legal elements. They may not assign legal effects.**

Neural model은 사건에서 사실을 추출하고 법적 평가가 필요한 명제를 판단한다. 범죄의 구성, 변형, 위법성 조각, 책임 조각, 가벌성 면제, 공범 종속성, 죄책 결론은 typed symbolic semantics가 담당한다.

---

# 1. Design Goals

v2.1.0은 다음을 목표로 한다.

1. 공통 법적 predicate를 죄종 간에 재사용한다.
2. 범죄를 monolithic article unit이 아니라 typed components의 조합으로 표현한다.
3. 법적 정의 문법과 사건 판단 runtime을 분리한다.
4. neural grounding과 symbolic legal effect를 명시적으로 분리한다.
5. 구성요건, 위법성, 책임, 가벌성을 서로 다른 typed stage로 표현한다.
6. 미수와 공범을 별도 범죄 정의의 폭발 없이 orthogonal axis로 처리한다.
7. dependency를 issue ID가 아니라 필요한 법적 상태의 type으로 표현한다.
8. symbolic provenance를 보존한다.
9. Scallop의 probabilistic/differentiable execution을 향후 사용할 수 있도록 설계한다.
10. 최종 결론뿐 아니라 결론이 어느 stage에서 형성되거나 기각되었는지 추적 가능하게 한다.

---

# 2. Non-Goals

v2.1.0은 다음을 목표로 하지 않는다.

- 모든 형법 조문과 판례를 즉시 완전하게 모델링하지 않는다.
- 법적 평가를 전부 deterministic rule로 환원하지 않는다.
- 상당인과관계, 고의, 예견가능성, 폭행·협박의 정도 등 evaluative legal element에서 neural judgment를 제거하지 않는다.
- 최종 자연어 법률답안을 symbolic language와 동일한 granularity로 제한하지 않는다.
- Scallop 자체의 semantics를 수정한다고 주장하지 않는다.
- 모든 파생 범죄를 사전에 별도 `OffenseDef`로 materialize하지 않는다.

본 제안은 **criminal-law definition language와 typed legal IR을 정의하고 이를 Scallop으로 compile하는 구조**를 목표로 한다.

---

# 3. Architectural Separation

## 3.1 Definition Layer

Definition Layer는 사건과 무관한 법률지식을 정의한다.

```text
GroundFactDef
LegalElementDef
ElementBundleDef
OffenseDef
DoctrineDef
QualifierDef
RelationDef
CompletionPolicyDef
ParticipationPolicyDef
```

이 레이어의 질문은 다음과 같다.

> 법은 어떤 구성요소로 이루어져 있는가?

## 3.2 Executable Legal IR

Definition Language는 compiler를 거쳐 typed Legal IR로 변환된다.

Typed Legal IR은 다음 정보를 보존해야 한다.

- type information
- source definition
- normalized predicate reference
- logical expression tree
- `QUALIFY` / `COMPOSE` derivation
- stage attachment
- relation type
- dependency type
- exported component boundary
- provenance path

Compiler는 이 IR을 Scallop program으로 변환한다.

## 3.3 Case Runtime

Runtime은 구체적 사건에 법률지식을 적용한다.

```text
Case Text
    ↓
Neural Call 1
    ↓
GroundFacts
    ↓
Neural Call 2
    ↓
ElementAssessments
    ↓
Participation / Completion Resolution
    ↓
Element Aggregation
    ↓
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

Definition syntax와 runtime object syntax는 동일할 필요가 없다. 오히려 두 문법을 분리하는 것이 설계상 바람직하다.

---

# 4. Core Invariants

## 4.1 Neural models do not assign legal effects

Neural model이 직접 다음을 출력해서는 안 된다.

```text
bar
waiver
component
boundary
defeat_unlawfulness
exempt_punishment
guilty
not_guilty
```

Neural model은 canonical proposition의 grounding만 수행한다.

## 4.2 Canonical positive predicates

가능한 모든 groundable predicate는 긍정형의 명확한 truth condition을 가져야 한다.

권장:

```text
current_unlawful_attack(attacker, defender)
owner_consent(owner, act)
public_official(actor)
injury_result(victim)
```

비권장:

```text
no_bar_to_liability
offender_unlawful_culpable
absence_of_exception
not_exempt
```

법적 효과는 predicate 이름이 아니라 symbolic operator와 stage semantics가 결정한다.

## 4.3 Missing evidence is not negation

`NOT(A)`는 strong negation으로 해석한다.

```text
A = supported
→ NOT(A) = failed

A = contradicted
→ NOT(A) = satisfied

A = unresolved
→ NOT(A) = unresolved
```

다음 규칙을 invariant로 둔다.

> `NOT` never converts missing or unresolved evidence into satisfaction.

Negation-as-failure는 v2.1.0에서 허용하지 않는다.

## 4.4 Legal stage and evaluation state are distinct

`not_reached`는 법적 결과가 아니다.

예:

```text
StageResult<Unlawfulness> {
    evaluation_state: not_reached
    legal_state: null
}
```

따라서 `not_reached`를 `UnlawfulnessState` 또는 `CulpabilityState`의 legal value로 정의하지 않는다.

## 4.5 OffenseRealization, OffenseEstablishment, LiabilityResult are distinct

```text
OffenseRealization
= Elements satisfied
  + Unlawfulness preserved

OffenseEstablishment
= OffenseRealization
  + Culpability preserved or legally sufficient

LiabilityResult
= OffenseEstablishment
  + Punishability assessment
```

이 구분은 공범 종속성과 가벌성 분리를 위해 필수적이다.

---

# 5. Predicate System

## 5.1 GroundFactDef

`GroundFactDef`는 사건에서 직접 추출 가능한 정규화된 사실명제다.

```text
weapon_used(actor, weapon)
knife_placed_near_neck(actor, victim)
property_transferred(from, to, property)
victim_expressed_fear(victim)
person_relation(person_a, person_b, relation)
```

Call 1은 이 vocabulary를 기준으로 사건을 구조화한다.

## 5.2 LegalElementDef

`LegalElementDef`는 법적 기준에 따라 평가해야 하는 명제다.

```text
robbery_level_threat(actor, victim)
deception(actor, victim)
causal_nexus(event, result)
foreseeable_result(actor, result)
appropriation_intent(actor)
current_unlawful_attack(attacker, defender)
```

일반적인 형태:

```text
LegalElementDef {
    id
    arguments
    canonical_meaning
    grounded_by
    legal_standard
    authority_refs
}
```

## 5.3 Assessment

GroundFact와 LegalElement는 같은 evidence semantics를 사용할 수 있다.

```text
Assessment<T> {
    target: T

    evidence_state:
        explicitly_supported
        inferentially_supported
        contradicted
        unresolved

    rationale
    evidence
    provenance
}
```

필요한 경우 host/compiler가 이를 symbolic truth representation으로 정규화한다.

---

# 6. Fixed Offense Slots

v2.1.0은 `OffenseDef` 내부에 고정 element slot을 둔다.

```text
subject
object
conduct
circumstance
result
causation
mental
```

예:

```text
OffenseDef {
    identity

    elements {
        subject
        object
        conduct
        circumstance
        result
        causation
        mental
    }

    element_modules
    exports
    qualifiers
    composition_metadata
}
```

각 slot은 독자적인 텍스트가 아니라 normalized predicate 또는 expression을 참조한다.

`mental`은 고의, 인식, 목적 등 명확한 주관적 구성요건을 중심으로 사용한다.

과실, 부작위, 착오처럼 복합 법리를 단순 slot 하나로 축약하지 않는다.

---

# 7. Shared Element Modules

일부 법리는 여러 predicate가 결합된 reusable module로 정의한다.

예:

```text
negligence_bundle {
    requires {
        duty_of_care
        foreseeability
        avoidability
        breach_of_duty
    }
}
```

```text
omission_bundle {
    requires {
        duty_to_act
        possibility_to_act
        failure_to_act
        equivalence_to_commission
    }
}
```

착오는 특정 죄종의 negative predicate로 넣기보다 Elements-stage shared doctrine 또는 module로 처리한다.

```text
perceived_fact
actual_fact
    ↓
mistake doctrine
    ↓
effect on mental element
```

---

# 8. Element Expression Grammar

slot 내부는 단순 `ElementRef[]`가 아니라 expression tree를 가진다.

```text
ElementExpression :=
      ElementRef
    | ALL(ElementExpression...)
    | ANY(ElementExpression...)
    | NOT(ElementExpression)
    | ONE_OF(ElementExpression...)
```

## 8.1 ALL

```text
ALL(A, B, C)
```

모든 하위 expression이 충족되어야 한다.

## 8.2 ANY

```text
ANY(A, B, C)
```

하나 이상 충족되면 된다.

사기죄의 기망행위처럼 여러 manifestation이 병존할 수 있는 경우 `ONE_OF`보다 `ANY`가 적절하다.

```text
deception :=
    ANY(
        affirmative_falsehood,
        deceptive_concealment,
        implied_deceptive_conduct
    )
```

## 8.3 ONE_OF

```text
ONE_OF(A, B, C)
```

정확히 하나만 충족되는 상호배타적 법적 선택지에 한정한다.

기본 operator가 아니라 restricted operator로 취급한다.

## 8.4 NOT

```text
NOT(A)
```

명시적 부정만을 의미한다.

unresolved 또는 missing evidence를 true로 변환하지 않는다.

---

# 9. Definition-Time Legal Constructors

## 9.1 QUALIFY

`QUALIFY`는 기존 범죄의 동일성을 유지하면서 요건을 추가하거나 typed하게 변형한다.

```text
QUALIFY
    : OffenseDef × QualifierDef
    → DerivedOffenseDef
```

v2.1.0에서 `QualifierDef`는 단일 `target_slot`이 아니라 typed slot patches를 가진다.

```text
QualifierDef {
    additions {
        subject?
        object?
        conduct?
        circumstance?
        result?
        causation?
        mental?
    }
}
```

예:

```text
offense occupational_embezzlement :=
    QUALIFY(
        embezzlement,
        occupational_status
    )
```

진정신분범의 신분요건은 기본 `OffenseDef.subject`에 직접 위치시킨다.

부진정신분범은 `QUALIFY`를 이용한 qualified offense structure로 표현할 수 있다.

## 9.2 COMPOSE

`COMPOSE`는 독립적으로 정의된 components를 특정 관계 아래 결합해 새로운 offense definition을 만든다.

```text
COMPOSE
    : ComponentDef[]
      × RelationDef[]
    → DerivedOffenseDef
```

`ComponentDef`는 최소 다음을 허용한다.

```text
ComponentDef :=
      PrimitiveDef
    | ElementBundleDef
    | ExportedComponentDef
    | OffenseDef
```

예: 결과적 가중범

```text
COMPOSE(
    base = robbery,

    components = [
        injury_result,
        aggravated_result_attribution
    ],

    relations = [
        causal_nexus
    ]
)
```

예: 결합범

```text
COMPOSE(
    components = [
        robbery,
        rape
    ],

    relations = [
        statutory_nexus
    ]
)
```

`COMPOSE`는 naïve Boolean conjunction이 아니다.

단순히 `robbery AND injury`가 아니라 필요한 actor, event, victim, temporal, causal, statutory relation을 함께 요구한다.

## 9.3 PROJECT

`PROJECT`는 legal semantic constructor가 아니라 structural reuse utility다.

```text
PROJECT
    : StructuredDef × ExportKey
    → ExportedComponentDef
```

명시적으로 export된 부분만 projection할 수 있다.

```text
offense injury {
    exports {
        result: injury_result
    }
}
```

```text
PROJECT(injury, result)
→ injury_result
```

normalized primitive가 이미 존재한다면 직접 primitive를 참조하는 것을 우선한다.

## 9.4 INHERIT

`INHERIT`는 v2.1.0 core legal algebra에 포함하지 않는다.

필요한 경우 compiler 내부의 implementation utility로만 사용한다.

legal semantics를 갖는 `QUALIFY`와 코드 중복 방지를 위한 inheritance를 구분한다.

---

# 10. RelationDef

`RelationDef`는 first-class definition object다.

```text
RelationDef<A, B> {
    id
    left_type
    right_type

    evaluation:
        structural
        evaluative
}
```

## 10.1 StructuralRelation

예:

```text
same_actor
same_victim
same_object
same_event
temporal_order
```

entity/event binding으로 deterministic하게 판정 가능한 관계다.

symbolic runtime이 처리한다.

## 10.2 EvaluativeRelation

예:

```text
causal_nexus
foreseeability
statutory_nexus
```

법적 평가가 필요한 경우 `LegalElementAssessment`의 대상이 된다.

따라서 relation type 자체가 neural workload를 결정할 수 있다.

```text
StructuralRelation
→ symbolic evaluation

EvaluativeRelation
→ neural assessment
```

---

# 11. DoctrineDef and Typed Stage Effects

`DoctrineDef`는 처음으로 법적 effect를 발생시키는 definition object다.

예:

```text
doctrine self_defense {
    stage: unlawfulness

    requires {
        current_unlawful_attack
        defensive_act
        proportionality
    }

    effect:
        DEFEAT<Unlawfulness>
}
```

```text
doctrine personal_punishment_exemption {
    stage: punishability

    requires {
        qualifying_condition
    }

    effect:
        EXEMPT<Punishability>
}
```

v2.1.0의 최소 runtime effect algebra는 다음과 같다.

```text
DEFEAT<S>
MODIFY<S, M>
EXEMPT<Punishability>
```

`BAR`는 v2.1.0 core operator로 두지 않는다.

법적으로 다른 효과를 하나의 추상 category로 다시 섞는 것을 방지한다.

---

# 12. Stage Type System

## 12.1 Elements

```text
ElementsState =
    satisfied
    failed
    unresolved
```

Elements는 doctrine effect 하나가 뒤집는 stage가 아니라 `ElementAssessment`의 aggregation 결과다.

## 12.2 Unlawfulness

```text
UnlawfulnessState =
    preserved
    defeated
    unresolved
```

대표 effect:

```text
DEFEAT<Unlawfulness>
```

## 12.3 Culpability

```text
CulpabilityState =
    preserved
    defeated
    diminished
    unresolved
```

대표 effects:

```text
DEFEAT<Culpability>
MODIFY<Culpability, M>
```

`diminished`는 범죄성립을 자동 부정하지 않는다.

## 12.4 Punishability

```text
PunishabilityState =
    punishable
    exempted
    modified
    unresolved
```

대표 effects:

```text
EXEMPT<Punishability>
MODIFY<Punishability, M>
```

범죄성립과 처벌 가능성은 최종 결과에서도 분리한다.

---

# 13. Intermediate Legal Conclusions

v2.1.0은 다음 중간 conclusion type을 명시적으로 둔다.

## 13.1 OffenseRealization

```text
OffenseRealization<X> {
    actor
    offense: X
    elements
    unlawfulness
    realization_state
    provenance
}
```

의미:

```text
Elements = satisfied
AND
Unlawfulness = preserved
```

## 13.2 OffenseEstablishment

```text
OffenseEstablishment<X> {
    realization
    culpability
    establishment_state
    provenance
}
```

의미:

```text
OffenseRealization = established
AND
Culpability ∈ {preserved, diminished}
```

## 13.3 LiabilityResult

```text
LiabilityResult {
    offense
    actor

    offense_establishment
    punishability

    decisive_stage
    decisive_element?
    decisive_doctrine?
    provenance
}
```

예:

```text
LiabilityResult {
    offense: theft

    offense_establishment:
        established

    punishability:
        exempted

    decisive_stage:
        punishability
}
```

구성요건 실패:

```text
LiabilityResult {
    offense: fraud

    offense_establishment:
        not_established

    decisive_stage:
        elements

    decisive_element:
        deception
}
```

위법성 조각:

```text
LiabilityResult {
    offense: injury

    offense_establishment:
        not_established

    decisive_stage:
        unlawfulness

    decisive_doctrine:
        self_defense
}
```

---

# 14. Completion as an Orthogonal Runtime Axis

미수는 `completed offense failed → attach attempt label`로 처리하지 않는다.

그렇게 하면 미수범 처벌규정이 존재하는 범죄에서 기수 구성요건의 미완성 때문에 판단이 조기에 종료된다.

따라서 Completion은 Elements aggregation 이전에 개입한다.

```text
OffenseDef
    +
CompletionPolicyDef
    +
Case Assessments
        ↓
Completion Resolution
        ↓
OffenseFormInstance
        ↓
Element Aggregation
```

## 14.1 CompletionPolicyDef

```text
CompletionPolicyDef {
    completed
    attempt
    preparation
    abandoned_attempt
    impossible_attempt
}
```

각 form의 punishability와 필요한 legal conditions를 정의한다.

## 14.2 CompletionResult

```text
CompletionResult {
    offense
    actor

    form:
        completed
        attempted
        abandoned_attempt
        impossible_attempt
        preparation
        unresolved

    decisive_conditions
    applicable_effects
    provenance
}
```

핵심은 다음과 같다.

```text
OffenseDef<fraud>
×
CompletionForm<attempt>
→
OffenseFormInstance<fraud, attempt>
```

`attempted_fraud`를 별도 정적 `OffenseDef`로 무한 생성하지 않는다.

---

# 15. Participation as an Orthogonal Runtime Axis

Participation은 단순 최종 label이 아니다.

특히 공동정범은 Elements aggregation의 입력을 바꿀 수 있다.

```text
GroundFacts
    ↓
Participation Assessment
    ↓
Attribution
    ↓
Actor-bound facts/elements
    ↓
Element Aggregation
```

## 15.1 Participation hierarchy

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

## 15.2 Co-principal

공동정범은 attribution-based semantics를 가진다.

예:

```text
ATTRIBUTE(
    property_taking(by=乙),
    to=甲,
    basis=co_principal
)
```

```text
ATTRIBUTE(
    violence(by=甲),
    to=乙,
    basis=co_principal
)
```

다른 공동자의 행위를 actor-specific Elements 판단에 귀속시킨다.

## 15.3 Instigator and Aider

교사와 방조는 attribution이 아니라 derivative participation이다.

```text
CoPrincipal
→ attribution

Instigator
→ derivative liability

Aider
→ derivative liability
```

교사범이 종속해야 하는 대상은 정범의 최종 `LiabilityResult`가 아니다.

필요한 doctrinal level까지의 typed result에 종속한다.

대표적으로:

```text
requires:
    OffenseRealization<principal, X>
```

정범에게 개인적 책임조각사유가 존재하더라도 정범의 위법한 구성요건 실현 자체가 존재할 수 있기 때문이다.

## 15.4 Typed Participation Dependency

```text
ParticipationResult<X> {
    actor
    target_offense: X

    mode:
        principal
        co_principal
        instigator
        aider

    basis:
        direct
        attribution
        derivative

    principal_dependency?
    attributed_components[]
    state
    provenance
}
```

dependency는 문자열 issue ID가 아니라 type으로 요구한다.

예:

```text
Instigation requires OffenseRealization<X>
```

그런데 runtime에 `ElementsResult<X>`만 존재한다면 validation error다.

```text
TYPE ERROR:
Instigation requires OffenseRealization<X>,
but only ElementsResult<X> is available.
```

---

# 16. Runtime Dependency DAG

v2.1.0 runtime은 완전한 직선 pipeline이 아니라 typed dependency DAG다.

일반적인 단독정범 기수:

```text
GroundFacts
    ↓
LegalElementAssessment
    ↓
Completion Resolution
    ↓
Element Aggregation
    ↓
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

공동정범:

```text
GroundFacts
    ↓
Participation Assessment
    ↓
Attribution
    ↓
LegalElementAssessment
    ↓
Completion Resolution
    ↓
Element Aggregation
```

교사범:

```text
Principal OffenseRealization
        ↓
Derivative Participation
        ↓
Actor-specific Establishment
```

미수:

```text
Case Assessments
    ↓
Completion Resolution
    ↓
OffenseFormInstance<Attempt>
    ↓
Attempt-specific Element Aggregation
```

---

# 17. Definition-Time and Runtime Operators

## 17.1 Definition-time logical expressions

```text
ALL
ANY
NOT
ONE_OF
```

## 17.2 Definition-time legal constructors

```text
QUALIFY
COMPOSE
```

## 17.3 Structural utility

```text
PROJECT
```

## 17.4 Runtime legal effects

```text
DEFEAT
MODIFY
EXEMPT
```

## 17.5 Runtime attribution

```text
ATTRIBUTE
```

이들 operator는 phase별로 분리한다.

Definition-time operator와 runtime effect를 동일한 namespace 또는 동일한 semantic class로 취급하지 않는다.

---

# 18. Derived Definition Provenance

Compiler는 `QUALIFY` 또는 `COMPOSE` 결과를 flatten한 element set만 남겨서는 안 된다.

예:

```text
DerivedOffenseDef {
    id: robbery_causing_injury

    derivation:
        COMPOSE(
            robbery,
            injury_result,
            causal_nexus
        )

    flattened_elements:
        ...
}
```

다음 provenance path를 보존해야 한다.

```text
Liability
    ↓
DerivedOffense
    ↓
COMPOSE
├─ robbery
├─ injury_result
└─ causal_nexus
```

이는 설명가능성과 향후 differentiable analysis에서 중요하다.

---

# 19. Scallop Backend

v2.1.0의 제안은 Scallop을 수정하는 것이 아니라 다음 구조를 취한다.

```text
Criminal-Law Definition Language
    ↓
Typed Legal IR
    ↓
Compiler
    ↓
Scallop
```

초기 workshop 구현은 deterministic symbolic execution을 사용할 수 있다.

향후에는 neural grounding에 probability 또는 differentiable score를 부여하여 Scallop의 provenance와 differentiable reasoning을 활용할 수 있다.

예:

```text
GroundFact probability
    ↓
LegalElement probability
    ↓
StageResult
    ↓
LiabilityResult
```

이를 통해 최종 죄책에 대해 어떤 predicate가 결정적이었는지 단순 importance가 아니라 **법적 derivation path와 함께** 추적할 수 있다.

```text
intent
    ↓
Elements
    ↓
Liability

current_unlawful_attack
    ↓
self_defense
    ↓
DEFEAT<Unlawfulness>
    ↓
Liability
```

향후 목표는 최종 결과에서 다음과 같은 sensitivity를 분석하는 것이다.

```text
Liability
    ↑
StageEffect
    ↑
LegalElement
    ↑
GroundFact
    ↑
Case Text
```

이때 두 predicate가 동일하게 중요한 것이 아니라 **어떤 doctrinal stage를 거쳐 결론에 영향을 주는지**가 provenance에 남는다.

---

# 20. Validation Cases

v2.1.0의 core grammar는 다음 구조를 표현할 수 있어야 한다.

## 20.1 진정신분범

대표 패턴:

```text
subject:
    status_requirement(actor)
```

신분이 base offense 자체의 element다.

## 20.2 부진정신분범

대표 패턴:

```text
QUALIFY(
    base_offense,
    status_or_relation_qualifier
)
```

qualifier는 typed slot patches를 적용한다.

## 20.3 결과적 가중범

대표 패턴:

```text
COMPOSE(
    base_offense,
    aggravated_result,
    result_nexus,
    result_attribution
)
```

중한 결과의 독립 범죄 전체를 import하지 않는다.

가능한 경우 normalized result primitive를 직접 재사용한다.

## 20.4 결합범

대표 패턴:

```text
COMPOSE(
    offense_A,
    offense_B,
    statutory_nexus
)
```

단순 `A AND B`가 아니라 필요한 relation을 함께 요구한다.

## 20.5 미수범

대표 패턴:

```text
OffenseDef<X>
×
CompletionForm<Attempt>
→
OffenseFormInstance<X, Attempt>
```

기수 Elements 실패 후 attempt label을 붙이는 방식은 허용하지 않는다.

## 20.6 공동정범

대표 패턴:

```text
Participation<CoPrincipal>
→ ATTRIBUTE
→ Actor-specific Elements
```

## 20.7 교사범

대표 패턴:

```text
Participation<Instigator>
requires:
    OffenseRealization<Principal, X>
```

정범의 최종 `LiabilityResult`가 아니라 필요한 doctrinal level의 typed dependency를 요구한다.

---

# 21. Migration Principles from v1

v1의 모든 card를 그대로 v2 predicate로 변환하지 않는다.

v2 migration은 다음 순서로 진행해야 한다.

```text
v1 cards
    ↓
semantic normalization
    ↓
GroundFactDef / LegalElementDef / DoctrineDef / RelationDef
    ↓
deduplication
    ↓
shared predicate registry
    ↓
OffenseDef assembly
```

특히 다음 v1 role은 neural-visible semantics로 유지하지 않는다.

```text
component
bar
waiver
boundary
```

각 card의 실제 법적 의미를 다음 중 하나로 재분류한다.

```text
normalized predicate
element module
doctrine
qualifier
relation
completion condition
participation condition
punishability effect
post-offense relation
```

---

# 22. Proposed v2.1.0 Object Inventory

```text
Definition Layer
────────────────────────────────
GroundFactDef
LegalElementDef
PrimitiveDef
ElementBundleDef
ExportedComponentDef
OffenseDef
DerivedOffenseDef
DoctrineDef<S>
QualifierDef
RelationDef<A, B>
CompletionPolicyDef
ParticipationPolicyDef
```

```text
Runtime Layer
────────────────────────────────
GroundFact
Assessment<GroundFact>
ElementAssessment
ParticipationResult
AttributionResult
CompletionResult
OffenseFormInstance
StageResult<Elements>
StageResult<Unlawfulness>
OffenseRealization
StageResult<Culpability>
OffenseEstablishment
StageResult<Punishability>
LiabilityResult
```

---

# 23. Proposed v2.1.0 Semantic Inventory

```text
Logical Expressions
────────────────────────────────
ALL
ANY
NOT
ONE_OF
```

```text
Definition Constructors
────────────────────────────────
QUALIFY
COMPOSE
```

```text
Structural Utility
────────────────────────────────
PROJECT
```

```text
Runtime Effects
────────────────────────────────
DEFEAT
MODIFY
EXEMPT
ATTRIBUTE
```

---

# 24. Acceptance Criteria for v2.1.0 Freeze

v2.1.0은 다음 조건이 충족되면 design freeze할 수 있다.

### Type system

- Definition-time object와 runtime object가 분리되어 있다.
- `GroundFactDef`와 `LegalElementDef`가 구분되어 있다.
- `OffenseDef`와 case-specific result가 구분되어 있다.
- `OffenseRealization`, `OffenseEstablishment`, `LiabilityResult`가 구분되어 있다.
- stage별 legal state가 서로 다른 type으로 정의되어 있다.
- `not_reached`가 legal state가 아닌 evaluation metadata로 정의되어 있다.

### Predicate semantics

- predicate는 canonical positive truth condition을 가진다.
- neural assessment가 legal effect를 출력하지 않는다.
- unresolved를 negation으로 변환하지 않는다.
- shared predicate registry를 죄종 간 재사용할 수 있다.

### Definition language

- fixed slots를 지원한다.
- shared element modules를 지원한다.
- nested `ALL / ANY / NOT / ONE_OF`를 지원한다.
- `QUALIFY`가 typed slot patch를 지원한다.
- `COMPOSE`가 primitive, bundle, exported component, offense를 받을 수 있다.
- relation이 structural/evaluative로 구분된다.
- derived definition의 provenance를 보존한다.

### Runtime

- Completion이 Elements aggregation 전에 개입할 수 있다.
- Participation이 Elements aggregation 전에 attribution을 적용할 수 있다.
- derivative participation이 typed dependency를 요구할 수 있다.
- stage effect가 잘못된 stage에 적용될 경우 type error가 발생한다.
- 범죄성립과 가벌성이 분리된다.

### Backend

- Typed Legal IR에서 Scallop으로 compile 가능한 구조다.
- deterministic execution을 우선 구현할 수 있다.
- provenance를 보존한다.
- 향후 probabilistic/differentiable grounding을 추가해도 core schema를 다시 설계할 필요가 없다.

---

# 25. Open Questions After v2.1.0

다음은 v2.1.0 이후 세부 spec에서 확정한다.

1. 각 schema의 실제 JSON/YAML 문법
2. `ElementAssessment`의 exact status representation
3. probability를 어느 layer에서 처음 도입할지
4. `MODIFY` payload의 typed taxonomy
5. punishment modification과 sentencing을 어디까지 포함할지
6. 죄수론과 post-offense relation의 별도 algebra
7. 대향범, 집합범, 합동범의 actor-structure type
8. 상습범의 definition qualifier와 포괄일죄 relation의 연결 방식
9. 예비·음모의 exact CompletionPolicy 표현
10. 판례와 법률 reference의 authority/provenance schema
11. routing이 activation scope를 어떤 단위로 제한할지
12. alternative legal trace를 v2.1.x에 포함할지
13. 개별 형법 규정과 doctrine의 법률 검수

---

# 26. Proposed Implementation Boundary

v2.1.0 문서 승인 후 바로 전체 pipeline을 다시 작성하지 않는다.

권장 구현 순서는 다음과 같다.

```text
1. Definition schema
2. Type checker
3. Expression evaluator
4. QUALIFY / COMPOSE compiler
5. Relation evaluator
6. Runtime stage objects
7. Completion resolution
8. Participation / attribution
9. Scallop compilation
10. Neural grounding adapters
11. Writer integration
```

초기 개발에서는 작은 hand-authored legal subset으로 compiler와 runtime을 먼저 검증한다.

---

# 27. Summary

IDPR v2.1.0은 기존의 article-specific RuleIR을 **reusable legal primitives와 typed legal constructors를 사용하는 compositional legal representation**으로 전환한다.

핵심 변화는 세 가지다.

첫째, 법률의 정의와 사건의 판단을 분리한다.

```text
Definition Language
→ Typed Legal IR
→ Scallop
→ Case Runtime
```

둘째, neural model의 역할을 factual/evaluative grounding으로 제한하고 legal effect는 symbolic semantics가 독점한다.

```text
Case Text
→ GroundFact
→ LegalElement
→ Symbolic Legal Composition
```

셋째, 형사책임을 하나의 Boolean으로 환원하지 않고 typed stages와 intermediate conclusions로 표현한다.

```text
Elements
→ Unlawfulness
→ OffenseRealization
→ Culpability
→ OffenseEstablishment
→ Punishability
→ LiabilityResult
```

이 구조는 미수, 공범, 결과적 가중범, 신분범, 결합범을 하나의 공통 type system 안에서 표현할 수 있게 하며 최종 결론의 doctrinal provenance를 보존한다.

장기적으로는 Scallop의 differentiable execution을 이용해 최종 죄책에서 decisive predicate까지의 경로를 역으로 추적할 수 있는 기반을 제공한다.

---

## Proposed Decision

**Adopt IDPR v2.1.0 as the target architecture for the `deadline_v2` branch, subject to schema-level validation and legal review of concrete doctrine mappings.**

v1은 reproducible baseline으로 동결하고 v2.1.0은 별도 branch에서 구현한다.
