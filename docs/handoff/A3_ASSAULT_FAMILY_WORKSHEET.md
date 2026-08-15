# A3 폭행죄 family 저작 워크시트 — 검수 요청

기준: 2026-08-15 · 지시서 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) §4 P0-R3
직접 영향: `r11_p1_q1` (乙의 준강도치상 불성립 → 폭행치상, 丙·甲은 질적 초과로 책임 없음)

**설치 전 검수 문서다.** 카드마다 초안과 판정 요청이 붙어 있다. 아직 아무것도 저작하지 않았다.

---

## 0. 이 워크시트가 여는 것과 열지 않는 것

`gap.assault_offense_family`가 지목한 세 ref를 저작한다.

```text
offense.assault
offense.special_assault
derived_offense.assault_causing_injury_or_death
```

폭행죄 계열 전체(존속폭행·상습폭행 등)를 여는 것이 아니다. **질적 초과 pair의 한 축을
만드는 데 필요한 최소**만 저작한다 — pair가 없어서 `r11_p1_q1`이 미해결로 남아 있는 것이
이 gap의 실제 결과이기 때문이다.

---

## 1. 새 predicate — 하나만 필요하다

기존 저작을 훑은 결과 **새로 만들 predicate는 하나**다. 나머지는 전부 재사용한다.

| 필요한 것 | 처리 |
|---|---|
| 폭행행위 | **신규** `ground_fact.assault_conduct` |
| 사람 객체 | 재사용 `legal_element.natural_person_victim_status` |
| 단체·다중 위력 | 재사용 `legal_element.group_or_multiple_force` |
| 위험한 물건 휴대 | 재사용 `legal_element.dangerous_object_carriage` |
| 고의 | 재사용 `legal_element.intent` |
| 상해 결과 | 재사용 `legal_element.injury_result` |
| 사망 결과 | 재사용 `ground_fact.death_of_victim` |
| 중한 결과 귀속 | 재사용 `primitive.aggravated_result_attribution` |

### 신규 predicate 초안

```yaml
- id: ground_fact.assault_conduct
  arguments: [{name: actor, type: entity}, {name: victim, type: entity}]
  canonical_meaning: "사람의 신체에 대한 유형력 행사"
  semantic_sort: conduct
  legal_standard: >-
    사람의 신체에 대하여 유형력을 행사하였는지 여부. 상해의 결과가 발생하였는지는
    여기서 묻지 않는다.
  authority_refs: [{authority_basis: statute_text, citation: "형법 제260조 제1항"}]
```

`ground_fact.injury_conduct`("상해의 수단이 되는 유형력 또는 그 밖의 방법을 사용")와 별개로
두는 이유는, 그쪽이 이미 상해를 전제한 수단 개념이라 폭행죄의 실행행위를 그것으로 대신하면
폭행치상에서 같은 사실이 두 층에 겹쳐 들어가기 때문이다.

> **검수 ①** `ground_fact.assault_conduct`를 위 문안으로 신설하는 데 동의하는가?
> 특히 `legal_standard`의 마지막 문장("상해의 결과가 발생하였는지는 여기서 묻지 않는다")이
> 폭행과 상해를 가르는 자리로 충분한가?

---

## 2. `offense.assault` — 폭행죄 (제260조 제1항)

```yaml
- id: offense.assault
  identity: {name: "폭행죄", statutory_refs: ["형법 제260조 제1항"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제260조 제1항"}]
  elements:
    object: {op: ref, ref: legal_element.natural_person_victim_status}
    conduct: {op: ref, ref: ground_fact.assault_conduct}
    mental: {op: ref, ref: legal_element.intent}
```

법정형은 2년 이하 징역, 500만원 이하 벌금, 구류 또는 과료 → `fine_or_greater`.

**반의사불벌(제260조 제3항)은 저작하지 않는다.** 현재 v2에 소추조건을 표현하는 층이 없고,
`r11_p1_q1`은 성립 여부만 묻는다. 없는 것을 없다고 두는 편이, 처벌조건을 구성요건 자리에
끼워 넣는 것보다 낫다.

> **검수 ②** 이 구성요건으로 충분한가? 반의사불벌을 이번에 열지 않는 데 동의하는가?

---

## 3. `offense.special_assault` — 특수폭행죄 (제261조)

특수상해(제258조의2)와 가중사유가 **완전히 같다**(단체·다중의 위력 또는 위험한 물건 휴대).
그래서 기존 `qualifier.special_injury_method`를 그대로 쓸 수 있지만, **쓰지 않기를 권고한다.**

qualifier의 id와 description이 "제258조의2의 … 가중"으로 조문에 묶여 있어서, 폭행죄가
그것을 참조하면 하나의 qualifier가 두 조문의 가중을 겸하게 된다. 지금까지 지켜 온
single-source 원칙과 반대 방향이다.

```yaml
# qualifiers.yaml
- id: qualifier.special_assault_method
  description: "형법 제261조의 단체·다중 위력 또는 위험한 물건 가중"
  additions:
    circumstance:
      op: any
      args:
        - {op: ref, ref: legal_element.group_or_multiple_force}
        - {op: ref, ref: legal_element.dangerous_object_carriage}

# derived_offenses.yaml
- id: derived_offense.special_assault
  identity: {name: "특수폭행죄", statutory_refs: ["형법 제261조"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제261조"}]
  derivation:
    kind: qualify
    base: offense.assault
    qualifier: qualifier.special_assault_method
  flattened_elements:
    object: {op: ref, ref: legal_element.natural_person_victim_status}
    conduct: {op: ref, ref: ground_fact.assault_conduct}
    circumstance:
      op: any
      args:
        - {op: ref, ref: legal_element.group_or_multiple_force}
        - {op: ref, ref: legal_element.dangerous_object_carriage}
    mental: {op: ref, ref: legal_element.intent}
```

**gap 파일이 `offense.special_assault`로 적었지만 `derived_offense.special_assault`가 맞다.**
QUALIFY 파생이므로 특수상해·특수절도와 같은 자리에 둔다. gap 파일의 ref를 고친다.

> **검수 ③** 가중사유 predicate는 공유하되 **qualifier는 조문별로 따로 두는** 이 방향에
> 동의하는가? (동의하지 않으면 `qualifier.special_injury_method`를 재사용하고 description을
> 두 조문으로 넓힌다.)

---

## 4. `derived_offense.assault_causing_injury` / `..._death` — 폭행치사상 (제262조)

gap 파일은 `derived_offense.assault_causing_injury_or_death` 하나로 적었지만, **둘로 나누기를
권고한다.** 현주건조물방화치사상이 이미 같은 조문(제164조 제2항)에서
`arson_causing_injury` / `arson_causing_death` 둘로 저작되어 있다. 결과가 다르면 별 offense로
두는 것이 이 레포의 기존 관용구다.

```yaml
- id: derived_offense.assault_causing_injury
  identity: {name: "폭행치상죄", statutory_refs: ["형법 제262조"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제262조"}]
  candidate_materialization:
    episode_constraint: same
    binding_sets:
      - [offense.assault, offense.injury]
  derivation:
    kind: compose
    components:
      - {kind: offense, ref: offense.assault, local_key: assault_part}
      - {kind: primitive, ref: primitive.aggravated_result_attribution,
         local_key: result_attribution, slot: causation}
      - {kind: exported_component, ref: exported_component.injury_result,
         local_key: aggravated_result, slot: result}
    relations:
      - {relation: relation.causal_nexus, left: assault_part, right: aggravated_result,
         left_view: event, right_view: event}
  flattened_elements:
    object: {op: ref, ref: legal_element.natural_person_victim_status}
    conduct: {op: ref, ref: ground_fact.assault_conduct}
    result: {op: ref, ref: legal_element.injury_result}
    causation: {op: ref, ref: legal_element.aggravated_result_attribution}
    mental: {op: ref, ref: legal_element.intent}
```

`assault_causing_death`는 `exported_component.death_of_victim`으로 같은 형태를 쓴다.

### ⚠ 이 카드의 법률 쟁점 — `mental` 슬롯

결과적 가중범의 `mental`에 `legal_element.intent`가 들어가 있다. 상해치사죄
(`injury_causing_death`)도 그렇게 저작되어 있으므로 형태는 일관된다. 여기서 이 고의는
**중한 결과가 아니라 기본범죄(폭행)에 대한 고의**를 뜻한다.

문제는 `legal_element.intent`가 generic이라 Call 2가 "무엇에 대한 고의인가"를 스스로 정한다는
점이다. 폭행치상 사안에서 모델이 이것을 "상해의 고의"로 읽으면 FALSE가 돌아오고, 그러면
폭행치상이 성립하지 않는다 — 결과적 가중범의 요건을 정반대로 뒤집는다.

기존 결과적 가중범들이 이미 같은 구조를 쓰고 있으므로 **이번에 바꾸지 않는 것을 권고**하되,
이 위험은 기록해 둔다. 착오 정책의 `intent_toward_intended_object`와 같은 뿌리이고, 같은
authoring-review item으로 묶는 것이 맞다고 본다.

> **검수 ④** 둘로 나누는 데 동의하는가?
> **검수 ⑤** generic `intent`를 그대로 쓰고 위험만 기록하는 데 동의하는가?

---

## 5. 질적 초과 pair — 이 저작의 실제 목적

`excess_policies.yaml`에 이미 이렇게 적혀 있다.

> `r11_p1_q1`의 폭행치상은 여기에 넣지 못했다. 폭행죄와 폭행치상죄가 v2에 저작되어
> 있지 않아 pair의 한 축이 없다.

이제 축이 생기므로 pair를 넣는다.

```yaml
    - instigated_offense_ref: offense.theft
      realized_offense_ref: derived_offense.assault_causing_injury
      authority_refs:
        - authority_basis: commentary_reported_precedent
          citation: 케이스노트 형법총칙 교사의 착오 질적 초과
```

`r11_p1_q1`의 rubric은 甲(절도 교사)과 丙(공동범행)에 대해 각각 질적 초과를 요구한다.
甲 쪽은 위 pair가 그대로 처리한다.

**丙 쪽은 이 pair로 처리되지 않는다.** 丙은 교사자가 아니라 공동정범이고, 현재 초과 정책의
`probe.applies_to`는 `participation_candidate`이되 질적 초과 분기는 교사 관계를 전제로
`instigated_offense_ref`를 provenance로 받는다. 공동정범의 질적 초과를 표현하려면 정책
자체에 분기를 하나 더 저작해야 하고, 그것은 이 워크시트의 범위를 넘는다.

> **검수 ⑥** 이번에는 甲 쪽(교사 질적 초과) pair만 넣고, 丙 쪽(공동정범 질적 초과)은
> 별도 검수로 미루는 데 동의하는가? 그렇게 하면 `r11_p1_q1`은 **부분적으로만** 닫힌다.

---

## 6. 설치 시 함께 바뀌는 것

| 파일 | 변경 |
|---|---|
| `ground_facts.yaml` | `assault_conduct` 1건 추가 |
| `qualifiers.yaml` | `special_assault_method` 1건 추가 |
| `offenses.yaml` | `offense.assault` 1건 추가 |
| `derived_offenses.yaml` | `special_assault`, `assault_causing_injury`, `assault_causing_death` 3건 |
| `excess_policies.yaml` | pair 1건 추가 |
| `representation_gaps.yaml` | `gap.assault_offense_family` 삭제 (ref 이름 정정 포함) |
| `binding_seed_cues.yaml` | 새 offense 4건의 cue 필요 — Call 1.5가 seed cue 없이는 결박 못 한다 |
| Call 1 routing universe | **바뀐다** → Call 1 재실행 대상 |

seed cue 문안은 승인 후 별도로 올린다(짧고 기계적이라 이 검수를 늘릴 이유가 없다).

---

## 7. 검수 항목 요약

| | 내용 | 권고 |
|---|---|---|
| ① | `ground_fact.assault_conduct` 신설 문안 | 신설 |
| ② | 폭행죄 구성요건 / 반의사불벌 미저작 | 그대로 |
| ③ | 특수폭행 qualifier를 조문별로 분리 | 분리 |
| ④ | 폭행치사상을 상해·사망 둘로 분할 | 분할 |
| ⑤ | 결과적 가중범 `mental`의 generic intent 유지 + 위험 기록 | 유지 |
| ⑥ | 공동정범 질적 초과는 별도 검수로 이월 | 이월 |
