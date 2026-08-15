# A4 장물죄 family 저작 워크시트 — 검수 요청

기준: 2026-08-15 · 지시서 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) §4 P0-R4
직접 영향: `r10_p2_q1` (장물보관죄 성립 → 이후 영득 → 횡령은 불가벌적 사후행위)

**설치 전 검수 문서다.** 아직 아무것도 저작하지 않았다.

---

## 0. 먼저 정정할 사실 — 카드는 없다

`representation_gaps.yaml`의 `gap.stolen_property_offense_family`는 이렇게 적고 있다.

> 2026-08-06에 장물죄 트랙이 보류된 이후 그대로다. **카드는 이미 존재한다.**

**확인 결과 사실이 아니다.** `card_catalog_v2.json`에 `art362`·`art365` 카드가 하나도 없다
(art36x 대역에 있는 것은 `art360`과 `art366`뿐이고, 카탈로그 전체에서 "장물"이 걸리는 5건은
점유이탈물횡령 등에서 부수적으로 언급된 것이다). rulegen 캠페인 산출물에도 art362 요청이 없다.

그래서 A3보다 검수 부담이 크다. **조문에서 직접 저작해야 하고, 근거는 판례·주석이 아니라
조문 문언과 제 초안**이다. 이 점을 감안해 카드마다 근거를 명시했다.

---

## 1. 저작 범위

`gap.stolen_property_offense_family`가 지목한 두 ref만 저작한다.

```text
offense.stolen_property_acquisition   (장물취득죄)
offense.stolen_property_custody       (장물보관죄)
```

제362조 제1항은 취득·양여·운반·보관을 한 조문에 담고 있고, 제2항(알선)과 제363조(상습),
제364조(업무상과실), 제365조(친족상도례)는 이번에 열지 않는다. `r10_p2_q1`이 요구하는 것은
**보관**이고, 취득은 그 짝으로서 흡수 관계를 표현하는 데 필요하다.

> **검수 ①** 양여·운반을 지금 저작하지 않고 취득·보관 둘만 여는 데 동의하는가?
> (제362조 제1항의 네 행위태양 중 둘만 여는 것이므로, 나머지 둘은 후보가 아예 생기지 않는다.)

---

## 2. 새 predicate — 세 개

| 필요한 것 | 처리 |
|---|---|
| 장물성 | **신규** `legal_element.stolen_property_status` |
| 취득행위 | **신규** `ground_fact.stolen_property_acquisition_conduct` |
| 보관행위 | **신규** `ground_fact.stolen_property_custody_conduct` |
| 고의 | 재사용 `legal_element.intent` |

### 2-1. 장물성 — 이 워크시트에서 가장 중요한 카드

```yaml
- id: legal_element.stolen_property_status
  arguments: [{name: property, type: entity}]
  canonical_meaning: "재산범죄로 영득된 재물"
  legal_standard: >-
    그 재물이 재산범죄로 영득된 재물 자체인지 여부. 본범이 처벌되는지, 본범의 공소시효가
    지났는지는 묻지 않는다.
  semantic_exclusions:
    - "재산범죄로 얻은 재물을 처분하여 얻은 대가나 그것으로 바꾼 물건은 장물이 아니다."
    - "재산범죄가 아닌 범죄로 얻은 물건은 장물이 아니다."
  authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]
```

두 exclusion을 넣은 이유는 이 predicate가 **TRUE로 과잉 판정되기 쉬운 모양**이기 때문이다.
"범죄와 관련된 물건"으로 넓게 읽히면 뇌물·도박자금까지 장물이 되고, 대체물까지 포함되면
`r10_p2_q1`의 흡수 관계가 엉뚱한 물건에 붙는다.

동시에 exclusion이 흔한 TRUE 경로를 막지 않는지도 봐야 한다 — `means_or_object_defect`가
exclusion 둘로 TRUE·FALSE 경로를 각각 막아 45건 중 TRUE 1건이 된 전례가 있다.

> **검수 ②** 이 `legal_standard`와 두 exclusion으로 장물성을 안정적으로 판정할 수 있는가?
> 특히 "본범이 처벌되는지는 묻지 않는다"를 legal_standard에 넣은 것이 맞는가, 아니면
> exclusion으로 내려야 하는가?

### 2-2. 두 행위태양

```yaml
- id: ground_fact.stolen_property_acquisition_conduct
  arguments: [{name: actor, type: entity}, {name: property, type: entity}]
  canonical_meaning: "장물의 사실상 처분권 취득"
  semantic_sort: conduct
  legal_standard: >-
    그 재물에 대한 사실상의 처분권을 이전받았는지 여부. 대가를 지급하였는지는 묻지 않는다.
  authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]

- id: ground_fact.stolen_property_custody_conduct
  arguments: [{name: actor, type: entity}, {name: property, type: entity}]
  canonical_meaning: "위탁에 의한 장물의 보관"
  semantic_sort: conduct
  legal_standard: >-
    본범 또는 그를 위하여 그 재물을 맡아 두었는지 여부. 처분권을 이전받은 경우는 취득이지
    보관이 아니다.
  authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]
```

마지막 문장이 취득과 보관을 가른다. 이 구분이 `r10_p2_q1`의 핵심이다 — 보관으로 시작해서
나중에 영득했기 때문에 사후행위 문제가 생기는 것이고, 처음부터 취득이었다면 그 논점 자체가
없다.

> **검수 ③** 두 행위태양의 경계를 이 문장으로 긋는 것이 맞는가?

---

## 3. 두 offense

```yaml
- id: offense.stolen_property_acquisition
  identity: {name: "장물취득죄", statutory_refs: ["형법 제362조 제1항"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]
  elements:
    object: {op: ref, ref: legal_element.stolen_property_status}
    conduct: {op: ref, ref: ground_fact.stolen_property_acquisition_conduct}
    mental: {op: ref, ref: legal_element.intent}

- id: offense.stolen_property_custody
  identity: {name: "장물보관죄", statutory_refs: ["형법 제362조 제1항"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]
  elements:
    object: {op: ref, ref: legal_element.stolen_property_status}
    conduct: {op: ref, ref: ground_fact.stolen_property_custody_conduct}
    mental: {op: ref, ref: legal_element.intent}
```

법정형은 7년 이하 징역 또는 1천500만원 이하 벌금 → `fine_or_greater`.

**본범자는 장물죄의 주체가 될 수 없다**(자기 재산범죄의 사후처분). 이것을 `subject` 슬롯의
predicate로 저작하지 **않는** 것을 권고한다. 그 명제는 "이 사람이 본범인가"라는 cross-offense
판단이고, 지금 그것을 물으면 제151조에서 방금 제거한 것과 같은 종류의 잘못된 질문이 된다 —
Call 2에게 다른 사람의 법적 지위를 묻는 것이다.

`r13_p2_q1`이 이미 그 경우인데, gap 파일이 기록한 대로 **후보가 아예 생기지 않는 것으로**
정답이 충족된다. 본범인 사람에게는 장물 binding이 만들어지지 않기 때문이다.

> **검수 ④** 본범자 배제를 구성요건으로 저작하지 않고 binding 단계의 사실 문제로 두는 데
> 동의하는가? 필요하다고 보시면 A1에서 만든 **cross-actor dependency 경로**로 저작할 수 있다
> (같은 사람인지가 아니라 그 사람의 선행 재산범죄 성립 여부를 묻는 구조).

---

## 4. 불가벌적 사후행위 — 이 저작의 실제 목적

```yaml
  - rule_id: absorption.embezzlement_by_stolen_property_custody
    status: approved
    kind: absorption
    # first가 흡수되는 쪽(child)이다.
    first_offense_ref: offense.embezzlement
    second_offense_ref: offense.stolen_property_custody
    occurrence_constraint: same_episode
    actor_constraint: same
    condition_ref: condition.embezzled_object_is_the_same_property_held_in_custody
    condition_statement: >-
      횡령의 대상이 된 재물이 장물보관죄에서 보관하고 있던 바로 그 재물인가.
    legal_standard: >-
      두 행위의 객체가 동일한 재물인지만 본다. 보관이 적법하였는지, 영득의사가 언제
      생겼는지는 여기서 판단하지 않는다.
    basis: >-
      장물보관죄가 성립한 후 그 보관 중인 장물을 영득한 행위는 이미 성립한 장물보관죄의
      위법상태를 이용한 것에 불과하여 별도의 횡령죄를 구성하지 않는다.
```

`condition_statement`가 **관계만** 지는 것은 인장위조 흡수 규칙에서 확정된 원칙 그대로다.
보관의 적법성이나 영득의사 발생시점은 흡수되는 쪽 instance의 elements가 이미 판단했다.

### ⚠ occurrence_constraint

`same_episode`로 두었다. 그런데 `r10_p2_q1`의 사실관계는 **보관과 이후 영득이 시간적으로
떨어져** 있다. Call 1.5가 그 둘을 다른 factual episode로 나누면 이 규칙은 발화하지 않는다.

인장위조 규칙은 두 행위가 사실상 한 장면이라 문제가 없었지만, 여기서는 "나중에"가 사안의
핵심이다. 대안은 `occurrence_constraint`에 episode를 넘는 값을 새로 두는 것인데, 그러면
흡수 규칙이 사건 전체로 넓어져 무관한 두 죄가 만날 위험이 생긴다.

> **검수 ⑤** 여기가 이 워크시트에서 가장 위험한 자리다. 세 선택지 중 무엇으로 갈까.
>
> **(가)** `same_episode` 유지 — 규칙은 정확하되 사안에 따라 발화하지 않을 수 있다
> **(나)** episode를 넘는 제약값 신설 — 발화하지만 오작동 여지가 생긴다
> **(다)** 이번에는 규칙을 `status: draft`로 저작만 하고 발화시키지 않는다
>
> **권고는 (가)** — 실제로 발화하지 않으면 그것이 측정으로 드러나고, 그때 episode 경계를
> 다시 보는 편이 낫다. 지금 제약을 넓히면 왜 넓혔는지 근거 없이 남는다.

---

## 5. 설치 시 함께 바뀌는 것

| 파일 | 변경 |
|---|---|
| `legal_elements.yaml` | `stolen_property_status` 1건 |
| `ground_facts.yaml` | 행위태양 2건 |
| `offenses.yaml` | offense 2건 |
| `concurrence_rules.yaml` | 흡수 규칙 1건 |
| `representation_gaps.yaml` | `gap.stolen_property_offense_family` 삭제 + **"카드는 이미 존재한다" 기술 정정** |
| `binding_seed_cues.yaml` | 새 offense 2건 cue |
| Call 1 routing universe | **바뀐다** |

---

## 6. 검수 항목 요약

| | 내용 | 권고 |
|---|---|---|
| ① | 취득·보관 둘만 저작(양여·운반 제외) | 둘만 |
| ② | 장물성 legal_standard와 exclusion 2건 | 초안대로 |
| ③ | 취득/보관 경계 문장 | 초안대로 |
| ④ | 본범자 배제를 구성요건으로 저작하지 않음 | 저작 안 함 |
| ⑤ | 흡수 규칙의 occurrence_constraint | (가) `same_episode` |
