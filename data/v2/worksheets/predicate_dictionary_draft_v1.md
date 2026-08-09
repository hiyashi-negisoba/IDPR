# Predicate 사전 초안 v1 — v0 피드백 반영

v0([predicate_dictionary_draft_v0.md](predicate_dictionary_draft_v0.md))에 대한 법률
검수 피드백([predicate_dictionary_draft_v0_feedback.md](predicate_dictionary_draft_v0_feedback.md))을
전부 반영한 개정판. v0는 삭제하지 않고 그대로 둔다 — 무엇이 왜 바뀌었는지 추적하는
이력이다.

**이번 개정의 원칙(피드백이 명시)**: 법률 검수 결과는 반영하되, **현재 v2.2 DSL로 표현
가능한 사항은 기존 구조(`ElementExpression`/`DoctrineDef`/`CompletionPolicyDef`/
`RelationDef`/`DerivedOffenseDef` 등) 안에서 처리하고 신규 type/effect/state를 만들지
않는다.** 이번 15개 조문에서 처음 마주친 복잡한 사례를 이유로 곧바로 스키마를 확장하지
않고, 기존 구조로 정말 표현 불가능한 사례가 반복 확인될 때만 architecture gap으로
올린다.

---

## 1. 횡령의 불법영득의사 — 의사는 공유, 객관적 표현은 별도

**v0**: 절도·강도·횡령을 하나의 `unlawful_appropriation_intent`로 묶을지 질문만 해둠.
**v1(확정)**: 의사 자체는 공유하고, 횡령의 "객관적 표현" 요건은 별도 legal element로 분리.

```text
legal_element.unlawful_appropriation_intent   (절도·강도·횡령 공유)
legal_element.embezzlement_manifestation       (신규, 횡령 전용)

embezzlement.requires =
    unlawful_appropriation_intent AND embezzlement_manifestation
```

두 번째 것은 별종의 고의가 아니라 **고의를 현실화한 객관적 실행행위**다 — 새 mens rea
상위 타입 계층은 만들지 않는다. 강도의 재산상 이익 취득(재물이 아니라 이익)은 객체구조가
달라 `unlawful_appropriation_intent` 하나로 평탄화하지 않고 별도 legal_element 필요
여부를 2패스에서 확인한다(v0의 "검수 필요" 유지, 확정 아님).

---

## 2. 사기·공갈의 처분행위 — 공유하되 인과관계는 죄별로, 관계성은 RelationDef 우선 검토

**v1(확정)**: `property_disposition`은 공유, causal nexus는 죄별로 분리 유지(v0 방향
그대로). `disposer_identity_match`는 predicate가 아니라 기존 `RelationDef`로 표현
가능한지 먼저 검토 — 확정 predicate로 세우지 않는다.

```text
legal_element.property_disposition        (사기·공갈 공유)
legal_element.disposition_authority        (신규, "처분권한/지위" — disposer_identity_match 대체 후보)

fraud:      deception → mistake → property_disposition
extortion:  threat_or_violence → fear_or_defective_will → property_disposition
```

`disposer_identity_match`가 실제로 "피해자-처분자 두 주체 사이의 구조적·평가적 관계"를
뜻한다면 `RelationDef`가 predicate보다 자연스럽다 — 2패스 조립 시 relation binding으로
먼저 시도하고, 그걸로 표현이 안 될 때만 legal_element로 남긴다. 새 role type system은
만들지 않는다.

---

## 3. 강도·공갈의 권리행사 — 분리 확정, 선행 predicate만 공유 가능

**v1(확정, v0 판단 유지)**: 강도(구성요건 부정)와 공갈(위법성조각)의 권리행사를 하나의
`DoctrineDef`로 합치지 않는다는 v0 판단에 동의. 선행 사실·평가는 공유 가능하지만 법적
처리는 각 죄의 기존 Elements/Unlawfulness 구조에서 별도로 저작한다.

```text
ground_fact.valid_claim_exists
ground_fact.claim_scope
legal_element.means_socially_acceptable
```

공갈에서는 `right_exists`만으로 범죄를 차단하지 않는다 — 권리가 있어도 사회통념상
용인되지 않는 정도의 폭행·협박이면 공갈죄가 성립할 수 있다. 원칙: **same concept ≠
same legal effect, predicate dedup ≠ DoctrineDef dedup.** Elements 단계의 차이는
`NEGATE_ELEMENT` 같은 신규 effect가 아니라 기존 `ElementExpression`/offense
derivation/doctrine 구조로 표현한다.

---

## 4. 각칙 Completion ↔ 총칙 25-29조 — 신규 predicate·gate 없이 기존 CompletionPolicy로

### `result_not_occurred` 삭제 — CompletionPolicy.when이 직접 표현

**v0**: `ground_fact.result_not_occurred`를 미수 공통 predicate로 제안.
**v1**: **삭제한다.** 제25조는 "실행행위를 종료하지 못한 경우"와 "결과가 발생하지 않은
경우"를 모두 포함해 하나의 raw fact로 좁히기엔 넓다. "미완성"이라는 상태를 predicate로
역수입하지 않고, 각 죄의 `CompletionPolicyDef.states.*.when`이 그 죄의 미완성 조건을
직접 표현한다:

```text
theft.CompletionPolicy:
    completed.when  = ...
    attempted.when  = commencement_of_execution AND ...

fraud.CompletionPolicy:
    completed.when  = ...
    attempted.when  = commencement_of_execution AND ...
```

### `commencement_of_execution` — ground_fact가 아니라 legal_element

**v1(확정)**: 실행의 착수는 관찰사실이 아니라 법적 기준에 대한 포섭 판단이다.

```text
legal_element.commencement_of_execution   (ground_fact 아님 — 재분류)
```

### `criminal_realization_intent` — 신규 생성 보류, 재사용 우선 확인

각 범죄에 이미 저작된 고의·목적 요소(예: 각칙 A절의 `fraud_mistake.gain_purpose`,
`art333_sec5.illegal_benefit_intent` 계열)를 재사용할 수 있는지 2패스에서 먼저 확인한다.
새 relation도 만들지 않는다. v0의 `ground_fact.criminal_realization_intent`는 **삭제**.

### 제29조(미수범의 처벌) — 기존 `punishable`로 표현, 신규 gate 없음

`attempted ≠ punishable attempt`라는 법적 구별은 유지하되, `offense_specific_attempt_
authorization` 같은 신규 predicate/gate를 만들지 않고 기존 `CompletionPolicyDef.states.
*.punishable`로 표현한다.

### 미수·중지미수·불능미수의 처벌효과 — `punishable` + `punishability_note`만 사용

**v1(확정, 신규 SentencingEffect 없음)**:

```text
ATTEMPTED
    punishable = offense-specific(각 조문의 미수처벌 규정에 따라 저작)

ABANDONED_ATTEMPT
    punishable = true
    punishability_note = "필요적 감경 또는 면제"

IMPOSSIBLE_ATTEMPT
    punishable = dangerousness(legal_element)에 따라 state/condition에서 판정
    punishability_note = "법정 감면·면제 효과 기록"
```

`punishable`에 구체적 형량·감면 폭 계산까지 억지로 싣지는 않는다 — 그 구체 폭은
`punishability_note`(자유 텍스트)로만 남긴다.

---

## 5. 심신장애(10조) + 원인에 있어서 자유로운 행위(ALIC) — 기존 doctrine.requires 구조로

**v1(확정)**: 문제는 사실의 부정이 아니라 제10조 1·2항의 효과가 적용되는지 여부다.
`effect = SUPPRESS` 같은 신규 override 체계는 만들지 않는다 — 심신상실·심신미약
doctrine의 `requires`에 ALIC 적용 여부를 반영해서, 그 조건이 성립하면 해당 doctrine의
DEFEAT/MODIFY가 **발생하지 않도록** 표현한다(신규 effect 없이 requires expression만으로).

```text
legal_element.foreseeable_risk_at_self_induction     (원인행위 시 위험 예견)
legal_element.voluntary_self_induced_impairment       (자의에 의한 원인행위)
legal_element.offense_committed_in_resulting_impairment (그 장애 상태에서 범행)
```

이 세 개가 하나의 ALIC 적용요건 묶음을 구성하는지는 다음 predicate 사전 검수에서
확정한다(HOLD 아님 — legal_element 후보로는 확정, 조합 방식만 미확정).

### 심신미약 법률내용 수정 — "형을 감경할 수 있다"(임의적)

**v0 오류**: `diminished_capacity_modify = 형을 감경한다`는 현행법과 맞지 않는다.
제10조 2항은 **임의적 감경**이다.

**v1(수정)**:
```text
doctrine.diminished_capacity_modify
    Culpability: MODIFY → diminished
    punishability_note: "임의적 감경(형을 감경할 수 있다)"
```
신규 `MAY_REDUCE` 같은 sentencing effect는 만들지 않는다 — 현재 DSL이 양형 계산을
구조화하지 않으므로, 임의적이라는 성격은 `punishability_note`(비구조화 영역)에 남긴다.
`MODIFY` 자체는 그대로 유지한다.

---

## 6. 오상방위·오상과잉방위 — 신규 Mistake 타입 없음, HOLD 유지

**v1(확정, v0 문제의식 유지)**: 오상방위를 정당방위 성립으로 자동 인정하거나 16조
법률의 착오에 자동 귀속시키지 않는다는 v0 지적은 유지 — 법률효과에 견해 대립이 있고
16조와 단순 동일시하기 어렵다.

다만 이를 위해 `MistakeDef` / `variant_group` / `doctrinal_variant state` 같은 신규
schema·state는 **이번 단계에서 만들지 않는다.** 이번 단계에서는 다음까지만 한다:

```text
- 정당화사유의 전제사실에 관한 착오라는 논점을 별도 후보로 보존
- 실제 사실과 인식 사실을 필요한 legal_element/ground_fact 수준에서 분리
- 현재 DoctrineDef / ElementExpression으로 확정적으로 표현 가능한 범위만 저작
- 법률효과의 variant를 선택해야만 표현 가능한 부분은 HOLD
```

현재 DSL로 표현 불가능하다는 구체적 사례가 반복 확인되기 전에는 별도 mistake algebra를
도입하지 않는다. 오상과잉방위도 동일하게 HOLD.

---

## 추가로 발견된 세 가지 (v0에는 없던 지점)

### ① `ground_fact` ↔ `legal_element` 경계 재분류

규범적 평가가 핵심인 항목은 raw fact가 아니다. 다음 4개를 `ground_fact`에서
`legal_element`로 재분류한다:

| v0 (ground_fact) | v1 | 사유 |
|---|---|---|
| `criminal_realization_intent` | **삭제**(위 4절 — 재사용 우선 확인) | 신규 생성 보류 |
| `joint_execution_intent` | `legal_element.joint_execution_intent` | 공동가공의 의사는 규범적 평가(판례상 공모 인정 여부) |
| `joint_execution_conduct` | `legal_element.joint_execution_conduct` | "기능적 행위지배"는 이미 법적 평가가 들어간 명제 |
| `object_ownership_other` | `legal_element.object_ownership_other` | "타인 소유"는 소유권 귀속에 대한 법적 판단 |

`GroundFact → LegalElement → symbolic stage/doctrine`의 경계를 전체 초안에서
재점검했고, 위 4개 외 나머지 ground_fact 후보(`mental_disorder_at_act_time`,
`infringement_situation`, `defensive_act`, `voluntary_cessation_or_prevention`,
`means_or_object_defect`, `instigation_conduct`, `aiding_conduct`, `instigator_intent`,
`aiding_intent`, `taking_conduct`, `actual_acquisition` 등)는 이번 피드백에서 문제로
지적되지 않았으므로 ground_fact로 유지한다 — 단 `instigator_intent`/`aiding_intent`
(교사·방조의 고의)는 다음 검수 라운드에서 같은 기준으로 한 번 더 점검할 후보로
표시해둔다(확정 아님, 재분류 강제 아님).

### ② `duty_of_other_affairs`를 횡령/배임 공통으로 흘리지 않음

**v0 오류**: A-2 표에서 355(횡령)와 357(배임수재)이 `duty_of_other_affairs`를
공유하는 것으로 적었다. **v1(수정)**: 횡령은 "타인의 재물을 보관하는 자"라는 별도
신분요건이라 분리한다.

```text
breach_of_trust(배임):        duty_of_other_affairs
breach_of_trust_bribe(357):   duty_of_other_affairs
embezzlement(355):            custody_of_anothers_property   (신규, entrustment_relationship을 대체)
```

`legal_element.custody_of_anothers_property`가 v0의 `legal_element.entrustment_
relationship`을 흡수한다 — 같은 개념을 가리키던 두 이름 중 하나로 정리.

### ③ 준강도류 — Doctrine인지 DerivedOffenseDef인지 재분류, 신규 effect 금지

```text
doctrine.quasi_robbery                      (art333_sec3_3)
doctrine.complete_suppression_becomes_robbery  (art350_sec5_3)
```

둘 다 "원래 성립할 죄가 다른 죄로 전환된다"는 offense 전환처럼 보인다. **v1**: 이걸
`RECLASSIFY`/`REDIRECT` 같은 신규 first-class effect로 풀지 않는다 — 기존
`DerivedOffenseDef`/`QUALIFY`/`COMPOSE`로 표현 가능한지 2패스에서 먼저 검토하고,
정말 표현 불가능한 구체 사례가 확인될 때만 architecture gap으로 올린다. 지금은 두
항목 모두 "Doctrine vs DerivedOffenseDef 분류 미정"으로 표시.

---

## 갱신된 요약

```text
각칙(A절): 공유 legal_element 4(불법영득의사/처분행위/처분권한/의사·이익 분리 검토) +
          조문별 legal_element/ground_fact 13(criminal_realization 계열 제외, 4개
          ground_fact→legal_element 재분류 반영) + doctrine 3(2개는 분류 미정)
총칙(B절): 10조 6(diminished_capacity 내용 수정, ALIC 3개 legal_element로 재정의) +
          21조 5(오상방위/오상과잉방위 HOLD 유지) +
          25-27조 5(result_not_occurred 삭제, criminal_realization_intent 삭제,
          commencement_of_execution legal_element로 재분류) +
          30-32조 6(joint_execution 2개 legal_element로 재분류, instigation/aiding_
          conduct는 기존 fixture 재사용 그대로)
```

**이번 게이트에서 v0 대비 실제로 바뀐 것**: 신규 타입/이펙트/상태는 하나도 추가되지
않았다 — 전부 기존 `ElementExpression`/`DoctrineDef.requires`/`CompletionPolicyDef.
{when,punishable,punishability_note}`/`RelationDef`/`DerivedOffenseDef` 안에서
재배치됐다. 이게 이번 gate의 목적이었다: **실제 predicate를 통해 기존 DSL이 어디까지
자연스럽게 표현되는지 확인하는 것.**

### 다음 라운드로 넘기는 미확정 항목(HOLD, 이번엔 손대지 않음)

1. 오상방위·오상과잉방위의 법률효과 variant — Mistake 타입 신설 여부는 반복 사례 확인 후
2. `disposer_identity_match` → `RelationDef`로 표현 가능한지 2패스에서 직접 시도
3. `quasi_robbery`/`complete_suppression_becomes_robbery`의 Doctrine vs DerivedOffenseDef 분류
4. 강도 재산상 이익 취득에 별도 legal_element가 필요한지(객체구조 차이)
5. ALIC 3개 legal_element가 하나의 요건 묶음으로 합성되는 방식
6. `instigator_intent`/`aiding_intent`의 ground_fact/legal_element 경계 재점검
