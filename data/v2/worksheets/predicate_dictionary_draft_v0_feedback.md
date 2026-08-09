이번 단계에서 반드시 고쳐야 할 것이 있습니다. 다만 **법률 검수 결과를 반영하되, 현재 v2.2 DSL로 표현 가능한 사항은 기존 구조 안에서 처리하고 신규 type/effect/state를 추가하지 않는 것**을 원칙으로 합니다. 특히 **제10조 심신미약의 효과**, **미수의 `result_not_occurred`**, **`ground_fact`와 법적 평가의 혼재**는 전체 predicate 사전으로 확장되기 전에 수정하는 편이 좋습니다.

## 1. 횡령의 불법영득의사 — 공유하되, 객관적 표현은 별도 predicate

문서는 절도·강도와 횡령의 불법영득의사를 같은 predicate로 묶을지 묻고 있습니다.

**판정: 같은 의사 개념은 공유하고, 횡령의 객관적 표현은 별도 legal element로 두는 것이 맞습니다.**

횡령에서 판례가 말하는 불법영득의사는 보관 중인 타인의 재물을 자기 소유물처럼 사실상·법률상 처분하려는 의사입니다. 한편 횡령행위는 그 영득의사가 외부에 인식될 수 있도록 객관적으로 표현된 행위를 요구합니다. 즉 두 번째 것은 “별도의 종류의 고의”가 아니라 **고의를 현실화한 객관적 실행행위**입니다. ([법제처][1])

따라서 현재 DSL에서는 다음 정도로 분리하면 충분합니다.

```text
legal_element.unlawful_appropriation_intent
legal_element.embezzlement_manifestation

embezzlement:
  requires:
    unlawful_appropriation_intent
    AND embezzlement_manifestation
```

다만 강도의 재산상 이익까지 `unlawful_appropriation_intent` 하나로 평탄화하지는 않는 것이 좋습니다. 재물의 영득과 재산상 이익의 취득은 객체구조가 다르므로, 실제 predicate 사전에서 같은 법적 의미인지 확인하여 필요한 경우 별도 `LegalElementDef`로 둡니다.

**별도의 mens rea 상위 타입 계층은 이번 단계에서 만들지 않습니다.**

---

## 2. 사기·공갈의 처분행위 — 공유 가능, 인과관계는 분리

**판정: `property_disposition`은 공유하고, causal nexus는 각 죄별로 둡니다. `disposer_identity_match`는 단순 predicate보다 기존 `RelationDef`로 표현 가능한지 먼저 검토하는 것이 좋습니다.**

문서가 현재 `property_disposition`과 `disposer_identity_match`를 공유 후보로 잡은 것은 좋은 방향입니다.

사기와 공갈 모두 피해자 측의 재산적 처분이 필요합니다. 사기에서는 피기망자의 행위가 기망→착오와 재산취득 결과를 매개하는 처분행위여야 하고, 공갈에서도 피공갈자가 해당 재물·이익을 처분할 지위나 능력을 가지고 있어야 합니다. ([법제처][2]) ([법제처][3])

공통 predicate는 예컨대 다음처럼 둘 수 있습니다.

```text
legal_element.property_disposition
legal_element.disposition_authority
```

반면 죄별 인과구조는 각각의 offense definition / relation binding에서 유지합니다.

```text
fraud:
  deception
    → mistake
    → property_disposition

extortion:
  threat_or_violence
    → fear_or_defective_will
    → property_disposition
```

현재의

```text
legal_element.disposer_identity_match
```

가 실제로 두 주체 사이의 구조적·평가적 관계를 뜻한다면 기존 `RelationDef`로 올리는 편이 더 자연스럽습니다.

또한 피해자와 처분자를 같은 개념으로 합치지 않아야 합니다. 다만 이를 위해 **새로운 role type system을 추가할 필요는 없고**, 현재 component와 relation으로 필요한 구별이 가능한지 먼저 확인합니다.

---

## 3. 강도·공갈의 권리행사 — 같은 DoctrineDef로 합치지 않음

**판정: 동의합니다. 자연어 표현이 같더라도 predicate dedup과 법률효과의 dedup은 별개입니다.**

공유 가능한 선행 사실·평가가 있다면 재사용할 수 있습니다.

```text
ground_fact.valid_claim_exists
ground_fact.claim_scope
legal_element.means_socially_acceptable
```

그러나 이후의 법적 처리는 각 죄의 기존 Elements / Unlawfulness 구조에 맞게 별도로 저작해야 합니다.

특히 공갈의 경우 단순히 `right_exists`만으로 범죄를 차단하면 안 됩니다. 재물·이익을 받을 권리가 있더라도 사회통념상 용인되지 않는 정도의 폭행·협박으로 이를 취득하면 공갈죄가 성립할 수 있습니다. ([법제처][5])

따라서 이번 단계의 원칙은 다음이면 충분합니다.

```text
same concept ≠ same legal effect
predicate dedup ≠ DoctrineDef dedup
```

**`NEGATE_ELEMENT` 같은 신규 effect는 추가하지 않습니다.** Elements 단계의 차이는 현재 `ElementExpression`, offense derivation, 기존 doctrine 구조로 먼저 표현합니다.

---

## 4. 각칙 Completion과 총칙 제25~29조 — 기존 CompletionPolicy 안에서 정리

각칙의 기수시점과 총칙의 미수 규율을 연결해야 한다는 방향은 맞습니다. 다만 이를 위해 새로운 completion predicate나 별도 authorization gate를 만들 필요는 없습니다.

### `result_not_occurred`는 일반 미수 predicate로 쓰기에는 좁음

현재:

```text
ground_fact.result_not_occurred
```

는 일반 미수의 공통 조건으로 쓰기에는 좁습니다. 형법 제25조는 실행행위를 종료하지 못한 경우와 결과가 발생하지 않은 경우를 모두 포함합니다. ([법제처][6])

따라서 `completion.offense_not_completed`라는 새 derived predicate를 추가하기보다, **각 죄의 `CompletionPolicyDef.when`이 해당 죄의 미완성 조건을 직접 표현하도록 정리**하는 것이 현재 설계와 맞습니다.

```text
theft CompletionPolicy:
  completed.when = ...
  attempted.when = commencement_of_execution AND ...

fraud CompletionPolicy:
  completed.when = ...
  attempted.when = commencement_of_execution AND ...
```

즉 “미완성”은 CompletionPolicy가 판정할 상태를 다시 predicate로 역수입하지 않습니다.

### `commencement_of_execution`은 ground fact가 아님

실행의 착수는 관찰사실 하나가 아니라 법적 기준에 대한 포섭 판단입니다. 따라서 raw `GroundFactDef`보다는 `LegalElementDef`로 두는 것이 현재 Call2/Call3 경계와 맞습니다.

```text
legal_element.commencement_of_execution
```

`criminal_realization_intent` 역시 raw fact로 중복 생성하기보다 각 범죄에 이미 저작된 고의·목적 요소를 재사용할 수 있는지 먼저 확인합니다. 이를 위해 새 relation을 만들 필요는 없습니다.

### 제29조는 반영하되 별도 gate는 만들지 않음

형법 제29조의 취지는 반드시 반영해야 합니다. 다만 현재 `CompletionPolicyDef`의 state에는 이미 `punishable`이 있으므로:

```text
attempted state:
  punishable = true / false
```

를 각 offense의 미수처벌 규정에 맞게 저작하면 됩니다.

즉:

```text
attempted
≠
punishable attempt
```

이라는 법적 구별은 유지하되, **`offense_specific_attempt_authorization`이라는 신규 predicate/gate를 만들지 않고 기존 CompletionPolicy의 `punishable`로 표현합니다.**

---

## 5. 심신장애와 원인에 있어서 자유로운 행위 — 기존 doctrine 조건으로 처리

원인에 있어서 자유로운 행위 때문에 심신장애 상태 자체를 false로 만들어서는 안 된다는 지적은 맞습니다. 문제는 사실의 부정이 아니라 제10조 제1·2항의 효과가 적용되는지 여부입니다. ([법제처][7])

다만 이를 위해:

```text
effect = SUPPRESS
targets = ...
```

같은 신규 effect/override 체계를 만들 필요는 없습니다.

현재 DSL에서는 심신상실·심신미약 doctrine의 `requires`에 원인에 있어서 자유로운 행위의 적용 여부를 반영하여, 해당 조건이 성립하면 그 doctrine의 `DEFEAT` 또는 `MODIFY`가 발생하지 않도록 표현하는 방식을 먼저 사용합니다.

필요한 법적 평가 predicate는 예컨대 다음처럼 분해할 수 있습니다.

```text
legal_element.foreseeable_risk_at_self_induction
legal_element.voluntary_self_induced_impairment
legal_element.offense_committed_in_resulting_impairment
```

이들이 하나의 ALIC 적용요건을 구성하는지는 predicate 사전 검수에서 확정합니다.

### 심신미약의 법률내용은 수정 필요

초안의:

```text
diminished_capacity_modify
= 형을 감경한다
```

는 현행법 내용과 맞지 않고, 제10조 제2항은 “형을 감경할 수 있다”는 임의적 감경입니다. ([법제처][7])

다만 현재 DSL은 양형 계산을 구조화하지 않으므로 `MAY_REDUCE` 같은 새 sentencing effect를 추가하지 않습니다.

현재 구조에서는:

```text
Culpability:
  MODIFY → diminished
```

를 유지하고, 임의적 감경이라는 구체적 형 효과는 필요한 경우 기존 `punishability_note` 등 비구조화 영역에 남깁니다.

---

## 6. 오상방위·오상과잉방위 — 지금 새 Mistake 타입을 만들지 않음

오상방위를 실제 정당방위 성립으로 처리하거나 제16조 법률의 착오에 자동 귀속시키는 것은 피해야 한다는 지적은 유지합니다. 오상방위의 법률효과에는 견해 대립이 있고, 제16조와 동일한 문제로 단순화하기 어렵습니다. ([법제처][8]) ([법제처][9])

그러나 이번 predicate population 단계에서 이를 해결하기 위해:

```text
MistakeDef
variant_group
doctrinal_variant state
```

같은 신규 schema/state를 만들지는 않습니다.

이번 단계에서는 다음까지만 합니다.

```text
- 정당화사유의 전제사실에 관한 착오라는 논점을 별도 후보로 보존
- 실제 사실과 인식 사실을 필요한 LegalElement/GroundFact 수준에서 분리
- 현재 DoctrineDef / ElementExpression으로 확정적으로 표현 가능한 범위만 저작
- 법률효과의 variant를 선택해야만 표현 가능한 부분은 HOLD
```

오상과잉방위도 동일합니다. 현재 DSL로 표현 불가능하다는 구체적 사례가 누적되기 전에는 별도 mistake algebra를 도입하지 않습니다.

---

## 7. 미수·중지미수·불능미수 — CompletionPolicy + 기존 Punishability 구조 유지

**판정: Completion과 처벌 여부를 분리하는 현재 기본 설계는 유지합니다. 새로운 `SentencingEffect` 타입은 만들지 않습니다.**

현행법상 보통 미수, 중지미수, 불능미수의 형 효과가 서로 다르다는 점은 법률내용으로 보존해야 합니다. ([법제처][6])

그러나 현재 Rulebase의 목표는 구체적 형량·감면 폭 계산이 아닙니다. 따라서:

```text
CompletionPolicyDef
  state
  punishable
  punishability_note
```

의 현재 구조 안에서 처리합니다.

예를 들어:

```text
ATTEMPTED
  punishable = offense-specific

ABANDONED_ATTEMPT
  punishable = true
  punishability_note = 필요적 감경 또는 면제

IMPOSSIBLE_ATTEMPT
  punishable = dangerousness에 따라 state/condition에서 판정
  punishability_note = 법정 감면·면제 효과 기록
```

처럼 저작할 수 있습니다.

핵심은 `punishable`에 형량 효과까지 억지로 싣지 않는 것이지만, 그렇다고 **별도의 SentencingEffect algebra를 이번 단계에서 추가하지는 않습니다.**

---

# 추가로 지금 발견된 세 가지

## ① `ground_fact`가 너무 많은 법적 결론을 먹고 있음

이 부분은 반드시 재점검하는 것이 좋습니다.

초안에는 예컨대:

```text
ground_fact.criminal_realization_intent
ground_fact.joint_execution_intent
ground_fact.joint_execution_conduct
ground_fact.object_ownership_other
```

가 들어가는데, 고의·기능적 행위지배·법적 소유관계처럼 규범적 평가가 핵심인 항목은 raw fact로 두기 어렵습니다.

현재 설계 원칙에 맞게:

```text
GroundFact
  → LegalElement
  → symbolic stage / doctrine
```

의 경계를 지킵니다.

특히 `joint_execution_conduct = 기능적 행위지배가 있었다`처럼 이미 법적 평가가 들어간 명제는 `LegalElementDef` 후보로 재분류하는 것이 맞습니다.

---

## ② `duty_of_other_affairs`를 횡령/배임 공통 predicate로 흘리지 않음

초안상 해당 predicate의 근거는 배임 계열이고, 횡령에는 별도의 “타인의 재물을 보관하는 자”라는 신분요건이 있습니다.

따라서:

```text
breach_of_trust:
  duty_of_other_affairs

breach_of_trust_bribe:
  duty_of_other_affairs

embezzlement:
  custody_of_anothers_property
```

로 분리합니다.

---

## ③ 준강도 등 offense 전환처럼 보이는 규칙 — 새 effect를 만들지 말고 기존 derivation부터 사용

현재:

```text
doctrine.quasi_robbery
doctrine.complete_suppression_becomes_robbery
```

처럼 보이는 후보는 단순 doctrine인지 derived offense인지 다시 분류할 필요가 있습니다.

하지만 이를 이유로:

```text
RECLASSIFY
REDIRECT
```

같은 신규 first-class effect를 추가하지 않습니다.

현재 DSL에 이미 있는 `DerivedOffenseDef`, `QUALIFY`, `COMPOSE`로 표현 가능한지 먼저 검수합니다. 실제 규칙을 이 구조로 표현할 수 없다는 구체적 사례가 확인될 때만 architecture gap으로 올립니다.

---

## 이번 게이트 결론

**Predicate-first 방향은 승인할 수 있습니다. 다만 전체 범위로 확장하기 전에 아래 사항을 predicate 사전 v0에 반영하는 것이 좋습니다.**

우선 수정할 것은 다음 네 가지입니다.

1. **제10조 심신미약의 법률내용을 “임의적 감경”으로 수정**하되 신규 `MAY_REDUCE` effect는 만들지 않음
2. **`result_not_occurred`를 일반 미수 공통 GroundFact로 사용하지 않고 각 offense의 CompletionPolicy 조건으로 재작성**
3. **제29조의 미수처벌 여부를 반영**하되 별도 authorization gate가 아니라 기존 `CompletionPolicyDef.punishable`을 사용
4. **`ground_fact` / `legal_element` 경계를 전체 초안에서 재점검**

7개 충돌점은 다음과 같이 정리합니다.

```text
1. 불법영득의사
   → 공유 가능한 LegalElement만 공유
   → 횡령의 객관적 표현은 별도

2. 처분행위
   → property_disposition 공유
   → 죄별 causal relation 분리
   → 관계 조건은 기존 RelationDef 사용 가능성 검수

3. 권리행사
   → 선행 predicate는 공유 가능
   → 죄별 법적 처리는 분리
   → 신규 effect 추가 없음

4. Completion
   → 총칙의 미수 규율과 각칙의 기수조건을 기존 CompletionPolicyDef에서 연결
   → derived completion predicate 추가 없음

5. ALIC
   → 기존 doctrine의 requires/effect 구조 안에서 우선 표현
   → SUPPRESS/override 체계 추가 없음

6. 오상방위
   → 별도 논점으로 보존
   → 현재 타입으로 표현 가능한 부분만 저작
   → MistakeDef/variant state는 만들지 않고 필요한 부분은 HOLD

7. 미수 효과
   → CompletionPolicy + 기존 Punishability 구조 유지
   → 구체적 감면·면제 내용은 note로 보존
   → SentencingEffect 추가 없음
```

이번 gate의 목적은 **실제 predicate를 통해 기존 DSL이 어디까지 자연스럽게 표현되는지 확인하는 것**입니다. 따라서 법률적 오류와 predicate 경계는 지금 고치되, population 과정에서 처음 마주친 복잡한 사례를 이유로 곧바로 새로운 type/effect/state를 추가하지 않습니다. 기존 구조로 표현 불가능한 사례가 반복해서 확인될 때만 별도 설계 변경 대상으로 올립니다.
