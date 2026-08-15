# `legal_element.intent` scope worksheet (v0 · 검수용)

기준: `experiments/v2_rulebase_regen_26/` · 정의 스냅샷 2026-08-15 · 2026-08-16 작성
선행: [`UNKNOWN_DIAGNOSIS.md`](UNKNOWN_DIAGNOSIS.md) mode B

**설치된 변경 없음.** 정의·프롬프트·planner를 건드리지 않았다. 이 문서는 전수 inventory와
scope 표, 그리고 A(구조 무변경) 가능 여부 판정이며, 문안은 아래 검수 결과를 받아서 만든다.

원칙: **`legal_element.intent`를 죄별 predicate로 복제하지 않는다.** predicate identity는
공유하고, 각 offense instance가 "고의의 대상이 되는 객관적 구성요건 범위"를 제공한다.

---

## 1. 전수 inventory — authored consumer 33개

`legal_element.intent`를 mental 자리에서 소비하는 곳은 정확히 33개다(offenses 13 + derived 20).
그 밖의 참조는 `mistake_policies.yaml` 하나뿐이고, 이는 소비처가 아니라 **정책의 입력 선언**이다
(`mistake_policy.korean_law_concrete_fact.probe.requires`가 `intent`를 neural_predicate로 요구).
qualifiers·completion_policies·doctrines·excess_policies에는 참조가 없다.

| 분류 | 수 | 판별 기준(저작 구조에서) |
|---|---:|---|
| **BASE** | 13 | `offenses.yaml`의 `elements.mental` |
| **QUALIFY** | 8 | `derivation.kind = qualify` |
| **COMPOSE-결과적가중** | 6 | components에 `primitive.aggravated_result_attribution` 있음 |
| **COMPOSE-고의결합** | 6 | `kind = compose`이고 위 primitive 없음 |

네 번째 분류는 지시받은 세 축에 없던 것이다. 강도상해·강도살인·강간상해·강도강간류는
compose이지만 중한 결과가 **고의범**이라 결과적 가중범과 scope 규칙이 반대다. 이것을 한
묶음으로 다루면 강도살인의 사망을 고의 대상에서 빼는 잘못을 저지른다.

---

## 2. 분류별 scope 규칙 초안

공통 출발점: **소유 offense의 객관적 slot**(`subject` · `object` · `conduct` · `result` ·
`causation` · `circumstance`) leaf 전체. 여기서 아래를 뺀다.

| 분류 | 포함 | 제외 | 근거 |
|---|---|---|---|
| BASE | 객관 leaf 전체 | — | 구성요건적 고의의 정의 그대로 |
| QUALIFY | 객관 leaf 전체 + **가중 circumstance** | — | 위험한 물건 휴대 등은 인식 대상. 특수폭행에서 흉기 인식 없이 특수폭행 고의를 인정할 수 없다 |
| COMPOSE-결과적가중 | **기본범죄 부분의 객관 leaf** | 가중결과 leaf + `aggravated_result_attribution` | 제15조 제2항. 중한 결과는 고의 대상이 아니라 예견가능성·인과의 대상 |
| COMPOSE-고의결합 | 객관 leaf 전체 | — (단 §4 Q3) | 중한 결과가 고의범이므로 결과도 인식 대상 |

**"result slot 통째 제외"는 틀린다.** 상해치사의 result slot은 `{death_of_victim(가중),
injury_result(기본범죄 상해죄의 결과)}` 혼합이고, 방화치사도 `{death_of_victim(가중),
burning_result(기본범죄)}`다. 제외 단위는 slot이 아니라 **component가 기여한 leaf**다.

---

## 3. 소비처별 표

객관 leaf 수와, 위 규칙으로 **저작 구조에서 자동 유도되는 제외**를 적었다.
`판정` 열: `자동` = 추가 저작 없이 유도 가능 / `검수` = §4의 질문이 걸림.

### 3.1 BASE (13)

| offense | 객관 leaf | 자동 제외 | 판정 |
|---|---:|---|---|
| `arson_of_occupied_structure` 현주건조물방화 | 2 | — | 자동 |
| `homicide` 살인 | 4 | — | 자동 |
| `injury` 상해 | 3 | — | 자동 |
| `assault` 폭행 | 2 | — | 자동 |
| `breach_of_trust` 배임 | 3 | — | 자동 |
| `rape` 강간 | 6 | — | 자동 |
| `forcible_indecency` 강제추행 | 6 | — | 자동 |
| `quasi_rape` 준강간 | 3 | — | 자동 |
| `quasi_forcible_indecency` 준강제추행 | 3 | — | 자동 |
| `false_public_document_creation` 허위공문서작성 | 3 | — | **검수 Q2** (`purpose_to_use_as_genuine` 공존) |
| `ancestral_homicide` 존속살해 | 4 | — | **검수 Q2** (`awareness_of_lineal_ascendant_status` 공존) |
| `ancestral_injury` 존속상해 | 4 | — | **검수 Q2** |
| `harboring_or_escape` 범인은닉·도피 | 5 | — | **검수 Q5** (circumstance에 주관적 요소 혼입) |

### 3.2 QUALIFY (8) — 전부 상해·폭행·배임 계열

| derived_offense | 객관 leaf | 판정 |
|---|---:|---|
| `special_assault` 특수폭행 | 4 (흉기·다중 포함) | 자동 |
| `aggravated_injury` 중상해 | 4 | 자동 |
| `special_injury` 특수상해 | 5 | 자동 |
| `special_aggravated_injury` 특수중상해 | 6 | 자동 |
| `occupational_breach_of_trust` 업무상배임 | 4 | 자동 |
| `aggravated_ancestral_injury` 존속중상해 | 5 | **검수 Q2** |
| `special_ancestral_injury` 특수존속상해 | 6 | **검수 Q2** |
| `special_aggravated_ancestral_injury` 특수존속중상해 | 7 | **검수 Q2** |

### 3.3 COMPOSE-결과적가중 (6)

| derived_offense | 객관 leaf | 자동 제외 | 판정 |
|---|---:|---|---|
| `assault_causing_injury` 폭행치상 | 4 | `injury_result` · `aggravated_result_attribution` | 자동 |
| `assault_causing_death` 폭행치사 | 4 | `death_of_victim` · `aggravated_result_attribution` | 자동 |
| `injury_causing_death` 상해치사 | 5 | `death_of_victim` · `aggravated_result_attribution` | 자동 (`injury_result`는 기본범죄라 **잔류**) |
| `arson_causing_injury` 방화치상 | 4 | `injury_result` · `aggravated_result_attribution` | 자동 (`burning_result` 잔류) |
| `arson_causing_death` 방화치사 | 4 | `death_of_victim` · `aggravated_result_attribution` | 자동 |
| `rape_causing_injury_by_aggravated_result` 강간치상 | 9 | `injury_result` · `aggravated_result_attribution` | **검수 Q4 — 규칙이 샌다** |

### 3.4 COMPOSE-고의결합 (6) — 전부 검수 Q3

| derived_offense | 객관 leaf | 같은 mental 자리의 전용 고의 |
|---|---:|---|
| `robbery_causing_intentional_injury` 강도상해 | 6 | `injury_intent` · `unlawful_appropriation_intent` |
| `robbery_causing_intentional_homicide` 강도살인 | 7 | `homicide_intent` · `unlawful_appropriation_intent` |
| `rape_causing_intentional_injury` 강간상해 | 8 | `injury_intent` |
| `robbery_rape` 강도강간 | 9 | `unlawful_appropriation_intent` |
| `special_robbery_rape` 특수강도강간 | 12 | `unlawful_appropriation_intent` |
| `quasi_robbery_rape` 준강도강간 | 9 | `unlawful_appropriation_intent` · `purpose_*` 3개 |

---

## 4. 검수 질문 — 카드 단위

각 카드는 그 자리에서 판정할 수 있게 적었다. `> comment:`로 답해 주면 된다.

### Q1. 하나의 intent가 두 죄의 고의를 지는 것을 허용하는가

강도강간(9 leaf)에서 mental은 `{intent, unlawful_appropriation_intent}`뿐이다. 불법영득의사를
빼면 **강도의 고의와 강간의 고의를 `intent` 하나가 동시에 진다.** scope를 명시하면 물음은
"甲이 폭행·협박으로 재물을 취거하고 또한 강간한다는 사실을 인식·용인하였는가"가 되어
복합 명제가 된다. "target 하나에 명제 하나" 원칙과 충돌한다.

선택지: (a) 허용한다 — compose 죄의 고의는 원래 결합적이다 / (b) 허용하지 않고 이 여섯 죄를
gap으로 올린다 / (c) scope를 component 단위로 쪼개 target을 복수로 만든다(= 구조 변경).

> comment:

### Q2. 별도 인식 predicate가 있는 요건을 intent scope에서 빼는가

존속살해는 `awareness_of_lineal_ascendant_status`가 존속성 인식을 이미 소유한다. intent scope에
`lineal_ascendant_of_self_or_spouse_status`를 남기면 같은 명제를 두 target이 나눠 진다.
허위공문서작성의 `purpose_to_use_as_genuine`도 같은 구조다(다만 이쪽은 목적범의 초과주관적
요소라 성격이 다르다).

제안: **다른 mental predicate가 특정 객관 leaf의 인식을 명시적으로 소유하면 그 leaf를
intent scope에서 뺀다.** 단 이 대응관계(어느 mental이 어느 객관 leaf를 덮는가)는 현재
저작에 **없다**. 채택하면 §5의 typed metadata가 필요해진다.

> comment:

### Q3. 고의결합범에서 전용 고의와 generic intent의 분담

강도상해 mental = `{intent, injury_intent, unlawful_appropriation_intent}`.
`injury_intent`가 상해 부분을 지므로 `intent`는 강도 부분(폭행·협박·취거)만 져야 자연스럽다.
그러나 어느 객관 leaf가 `injury_part`에서 왔는지는 `flattened_elements`에 남지 않는다
(`derivation.components`의 `local_key`로만 추적 가능).

선택지: (a) intent scope = 객관 leaf 전체(중복 감수) / (b) 전용 고의가 덮는 component의 leaf를
제외(= Q2와 같은 metadata 필요).

> comment:

### Q4. 강간치상에서 상해 야기 행위는 고의 대상인가

강간치상의 derivation은 가중결과 쪽에서 **`exported_component.injury_conduct`를 conduct 자리에도
기여**시킨다. §2 규칙은 `local_key = aggravated_result`인 component만 제외하므로
`ground_fact.injury_conduct`가 intent scope에 **남는다**. 즉 "강간의 고의"를 묻는 자리에
상해를 야기한 행위의 인식이 섞인다.

이 한 건이 §5 판정의 핵심 반례다 — 규칙이 local_key 관례에 의존하고 있고, 관례가
지켜지지 않는 곳에서 바로 샌다.

> comment:

### Q5. 범인은닉죄의 circumstance를 고의 대상으로 볼 것인가

circumstance = `{act_directed_at_another_offender, for_the_offenders_benefit,
omission_requires_guarantor_status}`. 두 번째는 **주관적 요소**이고 세 번째는 부작위범의
**규범적 지위**다. 객관 slot에 있다는 이유로 전부 intent scope에 넣으면 물음이 왜곡된다.
이 죄는 실측에서 intent 4/4 UNKNOWN이다.

> comment:

### Q6. 결과적 가중범의 기본범죄 결과는 잔류가 맞는가

상해치사에서 `injury_result`(기본범죄 상해의 결과)는 intent scope에 남고 `death_of_victim`만
빠진다. 방화치사에서 `burning_result`도 같다. 제15조 제2항의 취지에 부합한다고 보았다.

> comment:

---

## 5. A(구조 무변경) 가능성 판정

**부분적으로 가능하다. 그러나 순수 A로는 전부 덮지 못한다.**

### 가능한 근거

* Call 2 target은 이미 `offense_ref`를 들고 있다([grounding.py:59-68](../../src/idpr/v2/runtime/grounding.py#L59-L68)).
* `compile_offense()`가 COMPOSE component를 `local_key` 단위로 보존하고 slot 기여를 component별로
  조립한다([compile.py:72-93](../../src/idpr/v2/compile.py#L72-L93)). 따라서 "가중결과 component가
  기여한 leaf"를 request 조립 시점에 계산할 수 있다.
* §3 기준 **33개 중 19개가 추가 저작 없이 자동 유도된다.** 더 중요한 것은 실측 분포다 —
  이번 실행에서 intent가 물어진 14개 죄 중, UNKNOWN 28건의 **21건(75%)이 자동 유도 가능한
  죄**(폭행 8 · 상해 7 · 폭행치상 6)에서 나왔다.

### 그럼에도 순수 A가 아닌 이유 — 실패 지점 넷

1. **local_key 관례 의존.** 가중결과 식별이 `local_key = aggravated_result`라는 **명명 관례**에
   기대고 있다. 강간치상(Q4)에서 이미 샌다. 관례는 checker가 강제하지 않으므로 다음 저작에서
   조용히 깨진다.
2. **mental ↔ 객관 leaf 대응이 미저작**(Q2·Q3). 어느 전용 고의가 어느 객관 요건을 덮는지는
   어디에도 없다. 추론하면 그것이 두 번째 권위가 된다.
3. **slot이 주관/객관을 구분하지 않는다**(Q5). `circumstance`에 주관적 요소와 규범적 지위가
   섞여 있어 "객관 slot = 고의 대상"이 성립하지 않는다.
4. **payload 계약 변경은 어차피 필요하다.** `predicate_catalog`는 predicate당 하나이고 한 shard의
   모든 target이 공유한다([grounding.py:391-410](../../src/idpr/v2/runtime/grounding.py#L391-L410)).
   폭행과 폭행치상이 같은 shard에 오면 scope가 달라야 하므로, scope는 catalog가 아니라
   **target에 실려야** 한다. 즉 "프롬프트 문안만 고치기"로는 끝나지 않는다.
   (`realization_context` 선례가 있으나 production Call 2는 현재 보내지 않는다.)

### 권고

**하이브리드.** predicate는 복제하지 않고, scope를 target에 싣는 payload 확장을 하되,
scope 산출은 최대한 기존 구조에서 유도한다. 저작이 추가로 소유해야 하는 것은 §4에서
"검수"로 표시된 것뿐이며, 그것도 **죄별 intent 정의가 아니라 사용처의 typed marker**
형태여야 한다(예: 가중결과 component 표시, 전용 mental이 덮는 component 표시).

Q1~Q6의 답에 따라 marker가 하나로 끝날 수도, 둘이 될 수도 있다. 그래서 문안보다 이 판정이
먼저다.

---

## 6. 재측정 계약 (변경 설치 후)

frozen baseline `planned 635 / asked 595 / TRUE 286 / FALSE 21 / UNKNOWN 288`.

* `intent` UNKNOWN 28/42의 감소만 보지 않는다. **mental 자리 전체(100건, 현재 FALSE 0)**의
  TRUE/FALSE/UNKNOWN 이동을 함께 본다.
* 기존 TRUE 286과 FALSE 21의 **후퇴**를 먼저 확인한다. 특히 `assault_conduct` 17/17 TRUE처럼
  손대지 않은 predicate가 움직이면 저작이 아닌 다른 것이 바뀐 것이다.
* 결과적 가중범에서 intent가 TRUE인 3건이 유지되는지 본다 — §2 위험(중한 결과 고의로
  읽히는 것)이 실재했다면 이 3건 중 일부는 **FALSE 또는 UNKNOWN으로 바뀌는 것이 정상**이다.
* asked 분모가 변하면 비율 비교를 중단하고 분모부터 설명한다.
