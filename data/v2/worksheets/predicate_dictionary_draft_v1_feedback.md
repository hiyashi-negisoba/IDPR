# Predicate 사전 초안 v1 — 재검토 피드백

이번 v1은 **Gate ①의 방향을 충족한다.** 특히 법률 검수 결과를 반영하면서도 신규 type/effect/state를 추가하지 않고 기존 v2.2 DSL 안에서 정리한 점은 적절하다.

다만 freeze 전에 **3개 항목만 수정**하는 것이 좋다. 아래 수정도 모두 현재 DSL 안에서 가능하며 schema/runtime 변경은 필요 없다.

---

## 1. CompletionPolicy — 제29조 취지는 반영하되 `punishable`에 expression을 넣지 않음

v1의 기본 방향:

```text
attempted ≠ punishable attempt
```

은 맞다.

다만 다음 예시는 그대로 두면 오해가 생긴다.

```text
ABANDONED_ATTEMPT
    punishable = true

IMPOSSIBLE_ATTEMPT
    punishable = dangerousness(...)
```

현재 `CompletionPolicyDef`에서 `punishable`은 case-time expression이 아니라 **각 state에 저작되는 bool**이다. 따라서 `offense_specific_attempt_punishable` 같은 신규 predicate/gate를 만들거나 `dangerousness` expression을 `punishable` 필드에 넣지 않는다.

### 수정 원칙

각 offense의 `CompletionPolicyDef`를 저작할 때 해당 죄의 미수처벌 여부를 state의 `punishable`에 직접 반영한다.

```text
offense A — 미수처벌 규정 있음

ATTEMPTED
    punishable = true

ABANDONED_ATTEMPT
    punishable = true
    punishability_note = "처벌되는 경우 필요적 감경 또는 면제"
```

미수처벌 규정이 없는 offense에서는 해당 미수 state를 저작하더라도 `punishable = false`로 둔다.

불능미수에서 위험성처럼 **사건마다 달라지는 조건은 `punishable`이 아니라 state의 `when`에 둔다.**

예를 들어 필요한 경우:

```text
IMPOSSIBLE_ATTEMPT_DANGEROUS
    when = ... AND dangerousness
    punishable = true

IMPOSSIBLE_ATTEMPT_NON_DANGEROUS
    when = ... AND NOT(dangerousness)
    punishable = false
```

처럼 기존 CompletionPolicy의 state/when 구조로 표현한다. 실제 state 명칭과 분해는 각 offense 저작 시 결정한다.

**결론:** 제29조 반영은 필요하지만 신규 authorization predicate/gate는 만들지 않는다.

---

## 2. 횡령의 보관자 지위 — `entrustment_relationship`을 삭제하지 않되 새 LegalElement composition도 만들지 않음

v1에서:

```text
legal_element.custody_of_anothers_property
    (entrustment_relationship을 대체)
```

라고 정리한 부분은 수정하는 것이 좋다.

법률 검수상 `entrustment_relationship`과 `custody_of_anothers_property`을 구별할 필요가 있다면 predicate 사전에서도 둘을 보존한다.

```text
legal_element.entrustment_relationship
legal_element.custody_of_anothers_property
```

다만 다음과 같은 새 구조는 만들지 않는다.

```text
custody_of_anothers_property.requires = ...
```

현재 `LegalElementDef` 자체에 다른 LegalElement를 `requires`시켜 작은 rule program처럼 만드는 것이 우리 DSL의 composition 방식은 아니다.

필요한 조합은 기존 `ElementExpression`에서 한다.

```text
embezzlement.requires =
    ALL(
        custody_of_anothers_property,
        entrustment_relationship,
        ...
    )
```

또는 법률 검수 결과 `custody_of_anothers_property`의 legal standard 안에 위탁신임관계 판단이 완전히 포함되는 것으로 확정되면 하나의 LegalElement로 둘 수도 있다.

**이번 단계에서 확정할 것은 “두 개념을 성급히 동의어로 삭제하지 않는다”까지다. 조합 방식은 기존 ElementExpression을 사용한다.**

---

## 3. Predicate Dictionary 전체에 GroundFact / LegalElement typing pass 한 번 더

v1에서 일부 재분류한 방향은 맞다. 다만:

> 이전 피드백에서 문제로 지적되지 않았으므로 GroundFact로 유지

는 최종 typing 기준이 될 수 없다.

이번 15개 pilot의 모든 후보를 **이름이 아니라 `canonical_meaning` 기준으로 한 번 더 검토**하는 것이 좋다.

기준은 단순하다.

```text
사건에서 관찰·추출되는 사실
→ GroundFact

그 사실을 법적 기준에 포섭한 판단
→ LegalElement
```

### 우선 재검토할 후보

```text
instigator_intent
aiding_intent
valid_claim_exists
claim_scope
infringement_situation
defensive_act
voluntary_cessation_or_prevention
means_or_object_defect
```

예를 들어:

```text
"갑이 계약서를 작성했다"
"을이 1,000만원을 지급했다"
"행위자가 공격을 중단했다"
```

는 GroundFact가 될 수 있다.

반면:

```text
"유효한 채권이 존재한다"
"현재의 부당한 침해가 있다"
"자의로 실행을 중지했다"
"교사의 고의가 있다"
```

처럼 이미 법적 기준에 대한 평가를 포함하면 LegalElement가 자연스럽다.

따라서 `instigator_intent` / `aiding_intent`는 canonical meaning이 실제 교사·방조의 고의를 뜻한다면 `LegalElementDef`로 올린다.

`means_or_object_defect`처럼 이름만으로는 판단하기 어려운 항목은 강제로 이동하지 않는다. raw 사실만 담는지 결과발생 불가능성이라는 법적 평가까지 담는지를 보고 결정한다.

**새 타입은 필요 없다. 기존 GroundFactDef / LegalElementDef 사이의 typing 문제다.**

---

## 그대로 유지해도 되는 항목

### 1. 불법영득의사 / 횡령 manifestation

현재 정리 그대로 유지한다.

```text
legal_element.unlawful_appropriation_intent
legal_element.embezzlement_manifestation
```

별도 mens rea hierarchy는 만들지 않는다.

### 2. `property_disposition` 공유 + 죄별 causal structure

현재 방향 그대로 유지한다.

`disposer_identity_match`는 2-pass에서 기존 `RelationDef`로 먼저 표현해보고 필요할 때만 별도 LegalElement로 남긴다.

새 role type system은 만들지 않는다.

### 3. 강도·공갈의 권리행사 분리

현재 원칙을 유지한다.

```text
same concept ≠ same legal effect
predicate dedup ≠ DoctrineDef dedup
```

다만 `valid_claim_exists`와 `claim_scope`의 GroundFact/LegalElement typing은 위 typing pass에서 다시 본다.

### 4. `result_not_occurred` 삭제

현재 수정 그대로 유지한다.

일반적인 `offense_not_completed` derived predicate도 새로 만들지 않고 각 offense의 `CompletionPolicyDef.states.*.when`에서 기수·미수 조건을 직접 저작한다.

`commencement_of_execution`을 LegalElement로 재분류한 것도 유지한다.

### 5. 심신미약

현재 구조 그대로 유지한다.

```text
Culpability:
    MODIFY → diminished

punishability_note:
    "임의적 감경"
```

`MAY_REDUCE` 같은 새 sentencing effect는 만들지 않는다.

### 6. 오상방위·오상과잉방위

현재 HOLD를 유지한다.

```text
MistakeDef X
variant state X
new effect algebra X
```

실제 authoring에서 기존 DSL이 서로 다른 법률결론을 표현하지 못하는 구체적 반례가 확인될 때 architecture issue로 올린다.

### 7. 준강도류

현재대로 `DerivedOffenseDef / QUALIFY / COMPOSE`를 먼저 사용해본다.

`RECLASSIFY` / `REDIRECT` 같은 신규 effect는 추가하지 않는다.

---

## ALIC는 수정사항이 아니라 2-pass 확인사항으로만 유지

현재 후보:

```text
legal_element.foreseeable_risk_at_self_induction
legal_element.voluntary_self_induced_impairment
legal_element.offense_committed_in_resulting_impairment
```

중 세 번째가 관계적인 의미를 가진다는 지적은 이해할 수 있다.

하지만 문장이 relational하게 보인다는 이유만으로 바로 `RelationDef`로 옮길 필요는 없다. 현재 `RelationDef`는 실제로 두 component occurrence 사이의 독립된 relation obligation을 보존해야 할 때 사용한다.

따라서:

```text
offense_committed_in_resulting_impairment
→ LegalElementDef로 충분한지
→ 실제 두 component 사이 RelationDef binding이 필요한지
```

를 2-pass에서 직접 표현해본 뒤 결정한다.

**이번 Gate의 필수 수정사항은 아니다.**

---

# Gate ① 최종 판정

v1의 predicate-first 방식과 “신규 DSL primitive를 만들지 않는다”는 원칙은 승인 가능하다.

freeze 전에 필요한 수정은 다음 **3개뿐**이다.

```text
1. CompletionPolicy 예시 수정
   - punishable은 bool
   - 제29조는 offense별 policy authoring으로 반영
   - dangerousness 같은 case-time 조건은 state.when에서 처리
   - 신규 authorization gate 없음

2. 횡령 predicate 수정
   - entrustment_relationship을 성급히 삭제하지 않음
   - 필요하면 custody_of_anothers_property와 둘 다 보존
   - LegalElement.requires 같은 새 composition 없음
   - 기존 ElementExpression으로 조합

3. 15개 pilot predicate 전체 typing pass
   - canonical meaning 기준
   - GroundFact / LegalElement 경계 재검토
   - 신규 타입 없음
```

그 외 항목은 현재 v1대로 유지하면 된다.

이번 Gate의 목적은 법적으로 복잡한 개념을 만날 때마다 DSL을 확장하는 것이 아니라, **실제 Rulebase를 기존 v2.2 표현력 안에서 일관되게 저작할 수 있는지 확인하는 것**이다. 이 세 가지 수정 후에는 같은 방식으로 다음 범위의 predicate 사전 작성으로 진행하면 된다.
