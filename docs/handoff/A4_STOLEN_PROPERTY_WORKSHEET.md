# A4 장물죄 family — 결재 완료 · 설치됨

> **2026-08-15 v1 결재: 여섯 항목 승인, ⑤만 한 번 더 조여 설치 완료.**
> 아래는 v1 검수 원문이며, 최종 반영은 이렇다.
>
> | | v1 판정 | 설치 결과 |
> |---|---|---|
> | ① | 승인 | 취득·보관만 저작. 양도·운반은 미저작 scope |
> | ② | 승인 | `legal_element.stolen_property_status` — 경제적 동일성 예외 포함, 판례 authority 3건 |
> | ③ | 승인 | 두 행위태양을 `legal_element`로 저작 |
> | ⑥ | 신설 승인 + **중복 제거 지시** | 아래 참조 |
> | ④ | typed gap 승인 | `gap.stolen_property_self_principal_exclusion` |
> | ⑤ | 승인 + **condition 재조임** | 아래 참조 |
>
> **⑥ — generic intent와 conjunct로 걸지 않았다.** v1 초안은
> `all(intent, knowledge_of_stolen_property_status)`였는데, generic intent의 계약이 이미
> 장물성 인식을 포함하므로 같은 명제를 두 target이 각각 답하게 된다. 지시대로 장물죄용
> mental predicate **하나**가 취득·보관 의사와 장물성의 미필적 인식을 함께 소유하도록
> 저작했다 — `legal_element.stolen_property_dealing_intent`. 취득 시점 기준(2004도6084)도
> 그 안에 들어갔고, 왜 generic intent를 함께 걸지 않는지는 정의 주석에 남겼다.
>
> **⑤ — episode 순서는 candidate join만 소유한다.** 지적대로 순서만으로는 "선행 보관이
> 후행 시점까지 계속되었는가"가 보장되지 않는다(중간에 반환되었다가 다른 원인으로 다시
> 점유한 경우). 그래서 두 층으로 나눴다.
>
> * join: `ordered_cross_episode` — same actor + 선행 episode가 후행보다 이르거나 같음.
>   순서는 `factual_episode_order`로만 읽고, 그 목록에 없는 episode는 비교하지 않는다
>   (모르는 것을 "앞선다"로 읽으면 순서 제약이 사실상 무제약이 된다).
> * condition: "후행 영득·처분의 대상이 **선행 장물보관으로 계속 보관 중이던** 바로 그
>   재물인가" — 계속성은 여기가 진다.
>
> 런타임 확장 범위는 비교 함수 하나였고, 평가 시점과 해소 시점이 같은 join을 쓰도록 두
> 호출부에 모두 순서를 넘겼다.

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

제362조 제1항은 취득·**양도**·운반·보관을 한 조문에 담고 있고, 제2항(알선)과 제363조(상습),
제364조(업무상과실), 제365조(친족상도례)는 이번에 열지 않는다. `r10_p2_q1`이 요구하는 것은
**보관**이고, 취득은 그 짝으로서 흡수 관계를 표현하는 데 필요하다.

**v0 정정:** v0은 현행 문언을 `양여`로 잘못 적었다. 현행 제362조 제1항은 "취득, **양도**,
운반 또는 보관"이다.

> **검수 ① — v1에서 유지 (v0 승인됨).** 양도·운반은 미저작 scope로 남긴다.
> (제362조 제1항의 네 행위태양 중 둘만 여는 것이므로, 나머지 둘은 후보가 아예 생기지 않는다.)

---

## 2. 새 predicate — 네 개 (v0은 셋이라고 했다)

| 필요한 것 | 처리 |
|---|---|
| 장물성 | **신규** `legal_element.stolen_property_status` |
| 취득행위 | **신규** `legal_element.stolen_property_acquisition_conduct` |
| 보관행위 | **신규** `legal_element.stolen_property_custody_conduct` |
| **장물 인식** | **신규** `legal_element.knowledge_of_stolen_property_status` ← v0 누락 |
| 기본 고의 | 재사용 `legal_element.intent` |

### 2-1. 장물성 — v0에서 exclusion이 판례와 충돌했다

```yaml
- id: legal_element.stolen_property_status
  arguments: [{name: property, type: entity}]
  canonical_meaning: "재산죄인 범죄행위에 의하여 영득된 재물"
  legal_standard: >-
    그 재물이 재산죄인 범죄행위에 의하여 영득된 재물 자체인지 여부.
  semantic_exclusions:
    - "재산상 이익은 재물이 아니므로 장물이 될 수 없다."
    - >-
      원장물과 경제적 동일성이 인정되지 않는 처분대가나 대체물은 장물이 아니다. 다만
      금전이나 자기앞수표처럼 동일한 금전적 가치가 유지되는 경우에는 물리적 동일성이
      없어도 장물성이 유지될 수 있다.
  authority_refs:
    - {authority_basis: statute_text, citation: "형법 제362조 제1항"}
    - {authority_basis: judicial_precedent, citation: "대법원 2004도5904"}
    - {authority_basis: judicial_precedent, citation: "대법원 98도2579"}
```

**v0에서 무엇이 틀렸나 — 두 가지.**

1. exclusion을 "처분대가나 바꾼 물건은 장물이 아니다"로 **단정**했다. 원칙은 맞지만 금전·
   자기앞수표의 대체성 때문에, 예치 후 같은 가치의 현금을 인출한 경우처럼 물리적 동일성이
   사라져도 장물성이 유지되는 예외가 있다(98도2579). 단정하면 그 사안을 구조적으로 놓친다.
2. `authority_refs`가 `statute_text` 하나였다. 장물의 의미·처분대가·금전 대체성은 조문 문언이
   아니라 판례법리다.

**그리고 한 문장을 뺐다.** v0의 "본범이 처벌되는지, 공소시효가 지났는지는 묻지 않는다"는
법리로는 그럴듯하나 이번 검수에서 근거를 확보하지 못했다. 근거 없는 문장을 `statute_text`
아래 active legal standard로 두지 않는다 — 판례·주석 근거가 확보되면 그때 다시 넣는다.

> **검수 ②-v1** 위 canonical meaning·legal_standard·exclusion 2건·authority 3건으로 확정하는가?

### 2-2. 두 행위태양 — 경계 문장을 다시 씀

```yaml
- id: ground_fact.stolen_property_acquisition_conduct
  arguments: [{name: actor, type: entity}, {name: property, type: entity}]
  canonical_meaning: "점유를 이전받아 사실상 처분권을 획득"
  semantic_sort: conduct

- id: ground_fact.stolen_property_custody_conduct
  arguments: [{name: actor, type: entity}, {name: property, type: entity}]
  canonical_meaning: "타인을 위하여 장물을 맡아 사실상 점유·관리"
  semantic_sort: conduct
```

경계는 이렇게 긋는다.

> 취득: 자기에게 **독립적인 사실상 처분권**이 이전된 경우
> 보관: 타인을 위하여 맡아 **점유·관리**하고 있는 경우

v0의 "본범 또는 그를 위하여 맡아 두었는지"는 위탁자를 본범으로 좁혔는데, 본범이 아닌 사람의
위탁도 보관이 될 수 있으므로 "타인을 위하여"가 맞다.

### ⚠ 여기서 A3와 같은 문제가 다시 나온다 — GroundFactDef는 근거를 실을 수 없다

A3의 `assault_conduct`에서 확인된 것이 그대로 적용된다. **`GroundFactDef` 스키마에는
`legal_standard`도 `authority_refs`도 없고, 주석서 `source_refs`가 필수다.** 그런데
commentary corpus에 제362조 코멘트가 없다(art362·art365 카드가 없다는 §0의 사실과 같은 뿌리).

취득의 정의("점유를 이전받아 사실상 처분권 획득")도 조문 문언이 아니라 판례다. 그러니 A3와
같이 **`legal_element`로 저작**해야 근거를 실을 수 있다. `legal_element.robbery_level_violence`가
이미 그 선례다(폭행 conduct인데 legal_element).

> **검수 ③-v1** 두 행위태양을 `ground_fact.*`가 아니라 `legal_element.*`로 저작하는 데
> 동의하는가? (동의하면 id는 `legal_element.stolen_property_acquisition_conduct` /
> `..._custody_conduct`가 되고, 각각 판례 authority를 붙인다.)

---

## 2-3. v0이 놓친 것 — 장물이라는 인식

지적대로 이것이 v0의 가장 큰 누락이다. 확인 결과는 이렇다.

`legal_element.intent`의 저작된 계약은 다음과 같다.

```yaml
canonical_meaning: "객관적 구성요건요소 인식+실현 용인(고의)"
legal_standard: "행위자가 구성요건적 사실을 인식하고 그 실현을 의욕하거나 용인하였는지 여부"
```

**문언상으로는 장물성 인식을 포함한다.** 장물성은 객관적 구성요건요소이고, "용인"은 미필적
고의까지 담는 표현이다. 그러므로 형식적으로는 generic intent로 충분하다고 말할 수 있다.

**그럼에도 전용 predicate 신설을 권고한다.** 이유는 A3 ⑤와 같은 종류지만 여기서 더 나쁘다.

* A3의 결과적 가중범에서는 generic intent가 잘못 읽히면 성립이 **좁아진다**(FALSE로).
* 여기서는 반대로 **넓어질 수 있다**. "물건을 취득할 의사"는 거의 항상 TRUE이고, 장물성 인식을
  따로 묻지 않으면 그 TRUE가 장물죄 고의를 통과시킨다.
* 그리고 "장물일지도 모른다는 미필적 인식으로 충분하다"는 **장물죄 고유의 기준**이라
  generic intent의 문언에서 읽히지 않는다. 이 기준을 명시하지 않으면 모델이 확정적 인식을
  요구하는 쪽으로 읽어 반대 방향 오류도 난다.

```yaml
- id: legal_element.knowledge_of_stolen_property_status
  arguments: [{name: actor, type: entity}, {name: property, type: entity}]
  canonical_meaning: "장물이라는 인식"
  legal_standard: >-
    행위 당시 그 재물이 장물임을 인식하였는지 여부. 장물임을 확정적으로 알 필요는 없고
    장물일지도 모른다는 미필적 인식으로 충분하다.
  authority_refs:
    - {authority_basis: statute_text, citation: "형법 제362조 제1항"}
    - {authority_basis: judicial_precedent, citation: "대법원 2004도5904"}
```

그러면 신규 predicate는 **3개가 아니라 4개**이고, 두 offense의 `mental`은
`all(intent, knowledge_of_stolen_property_status)`가 된다.

> **검수 ⑥ (신설)** 전용 인식 predicate를 신설하는 데 동의하는가?
> 동의하지 않으면 generic intent만 쓰되, 그 선택을 authoring-review item으로 기록한다.

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
    conduct: {op: ref, ref: legal_element.stolen_property_acquisition_conduct}
    mental:
      op: all
      args:
        - {op: ref, ref: legal_element.intent}
        - {op: ref, ref: legal_element.knowledge_of_stolen_property_status}

- id: offense.stolen_property_custody
  identity: {name: "장물보관죄", statutory_refs: ["형법 제362조 제1항"]}
  article151_penalty_threshold:
    class: fine_or_greater
    authority_refs: [{authority_basis: statute_text, citation: "형법 제362조 제1항"}]
  elements:
    object: {op: ref, ref: legal_element.stolen_property_status}
    conduct: {op: ref, ref: legal_element.stolen_property_custody_conduct}
    mental:
      op: all
      args:
        - {op: ref, ref: legal_element.intent}
        - {op: ref, ref: legal_element.knowledge_of_stolen_property_status}
```

법정형은 7년 이하 징역 또는 1천500만원 이하 벌금 → `fine_or_greater`.

### ④ 본범자 배제 — v0의 처리는 거절되었다

**v0에서 무엇이 틀렸나.** "본범이면 애초에 binding이 안 만들어진다"로 해결하려 했다. 그 절반은
맞다 — Call 2에게 "이 사람이 본범인가"를 묻지 않는다는 것. 그러나 그 결론은 **법적 exclusion을
candidate generation에 숨기는 것**이 된다. `r13_p2_q1`에서 후보가 안 생겨 정답이 나오는 것은
좋은 관찰이지만, 그 우연을 이 규범의 semantic owner로 인정할 수는 없다.

게다가 조건이 v0이 생각한 것보다 좁고 구체적이다. 자기 범죄의 정범에는 **공동정범과 합동범이
포함**되고, 단순히 같은 범죄집단 소속이었다는 것만으로는 부족하다. 즉 필요한 것은

```text
actor가 어떤 재산범죄를 범했는가                                    ← 이것이 아니다
이 장물을 발생시킨 바로 그 선행 재산범죄의 정범·공동정범·합동범인가   ← 이것이다
```

A1의 participant-level dependency를 재사용할 수 있지만 **그대로 복사할 수는 없다.**
A1은 `participant → 선행범죄 성립`이면 충분했는데, 여기서는
`property ↔ 그 property를 발생시킨 선행범죄 ↔ 그 범죄에서의 actor 가담형태`라는
object-specific provenance가 더 필요하다.

> **검수 ④-v1** 이번 A4에서 그 dependency를 열지, 아니면
> `gap.stolen_property_self_principal_exclusion`으로 typed gap을 남길지 정해 주십시오.
>
> **권고는 typed gap.** 이 dependency는 A1보다 한 단계 무겁고(객체 provenance가 추가된다),
> `r10_p2_q1`을 닫는 데는 필요하지 않다. 다만 gap으로 남기는 이상 `r13_p2_q1`이 지금 맞는
> 답을 내는 것은 **우연이지 규칙이 아니라고** 그 항목에 명시한다.

## 4. 불가벌적 사후행위 — 이 저작의 실제 목적

```yaml
  - rule_id: absorption.embezzlement_by_stolen_property_custody
    status: approved
    kind: absorption
    # first가 흡수되는 쪽(child)이다.
    first_offense_ref: offense.embezzlement
    second_offense_ref: offense.stolen_property_custody
    occurrence_constraint: ordered_cross_episode   # v0은 same_episode였다
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

### ⚠ occurrence_constraint — v0의 (가)는 거절되었다

법리 자체는 오히려 v0보다 강해졌다. 절도범에게서 장물보관을 의뢰받아 보관하다가 임의처분한
사안에서, 장물보관죄 성립 시 이미 소유물추구권 침해가 발생했으므로 이후 횡령은 불가벌적
사후행위라는 판례가 있다(대법원 76도3067, 2004년 재확인). `basis`에 그 근거를 넣는다.

그래서 더더욱 `same_episode`를 쓸 수 없다. **이 법리가 적용되는 전형 자체가 시간적으로
후행하는 사안**이기 때문이다.

```text
장물을 보관함  →  시간이 흐름  →  나중에 임의처분·영득
```

`same_episode`는 법적 요건이 아니라 현재 representation의 우연한 경계다. 그것을 규칙의
occurrence constraint로 두면 **알고 있는 false negative를 규칙에 저작**하게 된다.

필요한 제약은 의미적으로 이것이다.

```text
same actor
same property            ← condition이 이미 진다
장물보관이 먼저 성립       ← 순서가 있다
그 보관상태 중의 후행 영득
```

즉 unrestricted `cross_episode`가 아니라 **ordered cross-episode**다.

### 구현 상태 — 지금 런타임에 그 값이 없다

`runtime/concurrence.py`가 받는 값은 `same_episode`와 `same_realization` **둘뿐**이고, 그 밖의
값은 예외를 던진다. 그래서 이 결재를 그대로 설치하려면 런타임 확장이 먼저다.

다행히 필요한 입력은 이미 plan에 있다 — `factual_episode_order`가 Call 1.5가 정한 서사 순서를
싣고 있고, 초과 판정이 이미 그 순서를 쓴다. 그러니 다음이 가능하다.

```text
ordered_cross_episode:
  actor_constraint: same
  second(장물보관)의 episode가 first(횡령)의 episode보다 앞서거나 같다
  순서는 factual_episode_order로만 판단한다 (문자열 정렬이나 id 규칙에 기대지 않는다)
```

> **검수 ⑤-v1** 위 `ordered_cross_episode`를 런타임에 추가하고 규칙을 `approved`로 설치하는가?
> 아니면 규칙을 `status: draft`로 저작만 하고 런타임 확장은 별도로 가는가?
>
> **권고는 런타임 추가 후 approved.** draft로 두면 A4를 저작하고도 `r10_p2_q1`은 그대로
> 닫히지 않는다 — 이 저작의 목적이 바로 그 사안이다. 확장 범위도 좁다(비교 함수 하나).

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

## 6. 검수 항목 요약 (v1)

| | 내용 | v0 판정 | v1 권고 |
|---|---|---|---|
| ① | 취득·보관만 저작 (`양여`→`양도` 정정) | 승인 | 유지 |
| ②-v1 | 장물성 — 대체물 exclusion 완화 + 판례 authority 3건 + 근거 없는 문장 삭제 | 수정 요구 | 개정안대로 |
| ③-v1 | 두 행위태양을 `legal_element`로 저작 (GroundFactDef는 근거를 실을 수 없다) | 수정 요구 | 개정안대로 |
| ⑥ | 장물 인식 predicate 신설 | **v0 누락** | 신설 |
| ④-v1 | 본범자 배제 | 현재안 거절 | typed gap |
| ⑤-v1 | 흡수 규칙 occurrence 제약 | (가) 거절 | `ordered_cross_episode` 신설 후 approved |

설치는 위 여섯 항목이 확정된 뒤에 한 번에 한다.
