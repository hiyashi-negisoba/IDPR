# Predicate 사전 확장 — 배치 ② 총칙 고의·과실·사실의착오·인과관계·부작위·동시범 (제13·14·15·17·18·19조) v0

[predicate_dictionary_ext_batch01_v1.md](predicate_dictionary_ext_batch01_v1.md)(9·11·12·16조,
확정)의 연장. 이 배치는 형량이 크고(6개 조문, 원문 1,464줄) 학설 대립이 매우 촘촘하다 —
워크시트 Ⅳ/Ⅴ류 절(판례 사례 나열, 학설 비교)은 predicate 후보로 뽑지 않고
`legal_standard` 본문 재료로만 흡수한다는 원칙(mossy-doodling-breeze.md, "조문 내부
구조도 규칙적이다" 절)을 이번에 가장 강하게 적용해야 했다.

**이 배치의 특징 — 두 종류의 결론이 섞여 있다.**

1. 13·14·18조: **신규 재사용 가능한 predicate를 실제로 만들어야 한다.** 이유는 두 조문이
   "고의/과실/부작위"라는, 모든 offense가 전제하지만 어느 각칙 카드도 명시적으로
   담고 있지 않은 **기초 주관적·행위 요건**을 규정하기 때문이다(아래 "구조적 공백" 절).
2. 15·17조: 신규 predicate가 **필요 없다** — 기존 `legal_element.intent`(13조)의
   legal_standard 확장, 또는 기존 `causal_nexus` RelationDef의 legal_standard 확장으로
   흡수된다.
3. 19조: **구조 검토가 먼저 필요하다** — 33/34/35-36조와 같은 "architecture-compatibility
   검수" 대상으로 재분류를 제안한다(아래 "19조" 절에서 근거 설명).

---

## 구조적 공백 발견 — `legal_element.intent`/`legal_element.negligence`가 지금까지 존재하지 않았다

`docs/contracts/v2/examples/*.json`(36개 fixture 인스턴스, 15개 조문 pilot 포함)을 직접
grep해 확인: **주관적 고의/과실을 나타내는 predicate가 `instigator_intent`/`aiding_intent`
(교사·방조 전용) 말고는 하나도 없다.** `card_catalog_v2.json`의 art250(살인) canonical_element
카드도 마찬가지다 — `no_murder_intent_no_murder`(고의 없으면 살인죄 불성립, 부정형 서술),
`intent_knowledge_lineal_status`(존속살해의 신분 인식) 같은 **주변부·가중요건 카드는
있어도, "살인의 고의가 있어야 한다"는 기본 카드 자체가 없다.** 이는 카드 저작 방식이
"각칙 조문마다 특유한 쟁점"만 카드화하고 모든 고의범에 공통되는 기초 요건(고의 자체)은
총칙(13조)이 규정할 것을 전제로 비워둔 것으로 읽힌다 — 즉 13·14조가 이 공백을 메우는
게 맞다.

---

## 제13조 고의 (Elements, 주관적 요건)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.intent` | 행위자가 객관적 구성요건요소(주체·객체·행위·결과 등, 신분범이면 신분사실 포함)에 해당하는 사실을 인식하고 그 실현을 용인(또는 의욕)하였다 | Ⅱ.1-Ⅱ.2, Ⅳ.1-Ⅳ.2 |

**신규·재사용 predicate.** 모든 고의범 offense의 `requires`에 (그 offense 고유의
canonical_element들과 나란히) `ALL(..., intent)`로 들어갈 것을 제안한다. 학설 대립
(인식설/의사설, 가능성설/개연성설/용인설/감수설, 확정적/불확정적/택일적/개괄적 고의,
사전고의/사후고의)은 predicate로 쪼개지 않고 판례가 채택한 용인설 기준(canonical_meaning에
반영)만 predicate 정의로 삼고, 나머지는 전부 `legal_standard`(및 이 predicate의 근거
조항 목록에 담긴 죄명별 적용례 — Ⅵ절)로 흡수한다.

**검수 필요 — 신분범/가중적 구성요건의 "인식 대상"은 별도 predicate 없이 canonical_meaning
서술로 흡수했다.** 존속살해의 직계존속 인식(`intent_knowledge_lineal_status`, 이미
카드로 존재)처럼 특정 offense가 요구하는 추가 인식 대상은 그 offense 자체의 카드가
담당하고, `legal_element.intent`는 일반형만 규정한다 — 신분범은 `ALL(intent,
(그 offense 카드가 만드는 신분인식 legal_element))`처럼 **두 predicate를 병렬**로 쓰면
되는지, 아니면 `intent`의 object를 offense마다 다르게 저작(같은 id, 다른 legal_standard
인스턴스?)해야 하는지 — 이 DSL은 `LegalElementDef`가 전역 정의라 후자는 구조적으로
불가능하다(2패스에서 실제로 병렬 방식이 동작하는지 확인 필요, 신규 primitive는 아님).

---

## 제14조 과실 (Elements, 주관적 요건 — 과실범 전용)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.negligence` | 행위자가 사회생활상 요구되는 객관적 주의의무(결과예견의무·결과회피의무)를 위반하여 죄의 성립요소인 사실을 인식하지 못하였거나 구성요건적 결과 발생을 회피하지 못하였다 | Ⅰ.1, Ⅱ |

**신규·재사용 predicate.** 13조의 `intent`와 대칭 관계 — 과실범(art267 과실치사, art268
업무상과실·중과실치사상, art366 손괴 계열 등 이번 트랙 대상 조문들)의 `requires`에
`negligence`가 들어간다. 허용된 위험·신뢰의 원칙(Ⅱ.1의 방대한 교통사고 판례군)은 별도
predicate나 doctrine이 아니라 **"주의의무위반이 있었는지"를 판단하는 기준**이므로
`negligence`의 `legal_standard`에 흡수한다 — 이 판례들이 "의무 없음"을 결론짓는 사례를
쌓아둔 것이지, 별도의 위법성조각/구성요건조각 gate를 만드는 게 아니기 때문이다(워크시트
Ⅱ.1 "다) 기준"이 이 흡수를 명시적으로 지지: 허용된 위험의 법적 성격 논쟁 자체가
"객관적 주의의무의 제한원리"로 수렴).

**검수 필요 — 업무상과실/중과실을 별도 predicate로 분리할지.** 워크시트 Ⅰ.2가 업무상과실
(업무자에게 요구되는 주의의무가 가중)·중과실(극히 근소한 주의만으로도 예견 가능했던
경우)을 보통과실과 **다른 처벌 수위**로 명시한다(art268 업무상과실치사상 등 이미 카드
존재). `LegalElementDef.legal_standard`가 predicate당 하나뿐이라는 이 DSL의 제약을
고려하면, 세 가지 선택지가 있다: (a) `negligence` 하나에 legal_standard로 세 기준을 다
담고 offense별 판단(구조 단순, 표현력 약함), (b) `professional_negligence`/
`gross_negligence`를 별도 legal_element로 신설(13조 신분범 문제와 유사한 병렬 구조),
(c) `negligence`의 canonical_meaning 자체를 파라미터화(이 DSL에 없는 기능). **(a)를
잠정 제안**하되(art268 카드가 이미 업무상/중과실을 별도로 카드화해뒀으므로 predicate
사전이 다시 나눌 필요가 없을 수 있다는 관찰), 2패스 실제 저작 시 재확인.

---

## 제15조 사실의 착오 — 신규 predicate 없음, 두 갈래로 흡수

**Ⅲ.1(제1항, 구성요건적 착오)**: "가벼운 사실을 인식하고 무거운 결과가 발생하면 무거운
죄로 벌하지 않는다"는 규정은 **`intent`(13조)의 object가 무엇인지에 대한 해석 규칙**이다
— 별도 predicate가 아니라 `legal_element.intent`의 legal_standard에 "가중적
구성요건요소(신분 등)에 대한 인식이 없으면 기본 구성요건의 고의만 인정된다"는 기준으로
흡수한다. art250의 `intent_knowledge_lineal_status` 카드가 정확히 이 규칙의 개별
적용례다 — 새 카드/predicate가 필요한 게 아니라 이미 있는 카드가 15조 제1항의 실증이다.

**Ⅴ-Ⅵ(부진정 결과적가중범, 공범과 결과적가중범)**: 판례가 인정하는 부진정 결과적가중범
(현주건조물방화치사상 등 — 이번 배치 밖, 각칙 배치⑧에서 다룸)은 그 offense의
`ElementExpression`을 `ANY(foreseeability_of_aggravated_result, intent)`처럼 저작해야
하는지 여부가 **offense마다 다르다**(판례가 인정한 목록과 부정한 목록이 갈림, 워크시트
Ⅱ.2 참고) — predicate 사전 차원에서 일괄 결정하지 않고, 각 결과적가중범 offense를
2패스에서 저작할 때 개별 판단한다는 점만 기록.

**Ⅱ.1 인과관계의 착오**: 새 predicate 없이 기존(Step 5) `causal_nexus` RelationDef의
legal_standard에 "행위자가 인과과정의 본질적 부분을 인식한 이상 실제 인과과정과 다소
차이가 있어도 고의를 부정하지 않는다"는 기준으로 흡수.

**신규 predicate 1건 — 결과적가중범 전용**:

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.foreseeability_of_aggravated_result` | 기본범죄로부터 중한 결과가 발생할 것을 예견할 수 있었다(중한 결과에 대한 과실) | Ⅰ.3, Ⅲ.4 |

art259(상해치사)·art337/338(강도상해치사/강도살인치사, 각칙 배치⑫)·art301(강간등
상해치사, 배치⑩) 등 모든 결과적가중범 offense가 공유하는 predicate.

---

## 제17조 인과관계 — 신규 predicate 없음

Ⅱ.1-Ⅱ.2(상당인과관계설/객관적귀속이론)와 Ⅳ(대법원의 상당인과관계설 채택 + 유형별
판단)는 전부 Step 5가 이미 만든 `causal_nexus` RelationDef의 `legal_standard` 재료다
— 새 relation이나 predicate를 만들지 않는다. 17조의 역할은 "그 relation의 판단기준
본문을 공급하는 것"으로 확정.

---

## 제18조 부작위범 (Elements, 행위 요건 — 부진정부작위범 전용)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.guarantor_status` | 행위자가 법령·계약(사무관리 포함)·선행행위·신의칙(조리)에 의하여 결과발생을 방지할 보증인적 지위(작위의무)에 있었다 | Ⅲ.2 |
| `ground_fact.capacity_to_perform_required_act` | 행위자가 그 구체적 상황에서 요구되는 행위를 현실적·물리적으로 행할 수 있었다(개별적 작위가능성) | Ⅲ.1 |
| `legal_element.act_equivalence` | 부작위에 의한 구성요건실현이 그 구성요건이 요구하는 수단·방법에 의한 실현과 동등하게 평가된다(작위와의 동가치성) | Ⅲ.2 |

**신규·재사용 predicate 3개.** art250(살인)의 `omission_guarantor_status` 카드가 이미
정확히 이 첫 번째 predicate의 개별 적용 사례임을 확인했다 — 13조의 신분범 논점과
같은 패턴: 각칙 카드가 총칙 predicate를 개별 offense에 적용한 흔적이 먼저 있었고, 이번에
그 일반형을 총칙에서 공급하는 것.

**검수 필요 — `act_equivalence`는 모든 부진정부작위범에 필요한가.** 워크시트가 명시:
"행위태양의 동가치성은 살인죄·상해죄 등 **단순결과범**에서는 거의 문제되지 않고,
거동범이나 사기죄의 '기망'·강제추행죄의 '추행'처럼 **특정 행위태양을 요구하는
구성요건**에서 특별히 문제된다." → `requires`에서 이 predicate를 항상 넣을지, 특정
행위태양 요구 offense에서만 선택적으로 넣을지는 offense별 판단(2패스 대상). predicate
자체는 필요.

**진정부작위범(퇴거불응죄 art319-2 등)은 이 배치의 대상이 아니다.** 진정부작위범은
구성요건 자체가 부작위 형식이라 그 각칙 카드 자체가 이미 요건을 담고 있고, 위 3개
predicate(부진정부작위범 전용)가 적용되지 않는다.

---

## 제19조 독립행위의 경합(동시범) — **architecture-compatibility 검수로 재분류 제안**

마스터플랜(mossy-doodling-breeze.md)은 17-19조를 "Elements(relation·conduct 유형)"로
뭉뚱그렸지만, 워크시트를 직접 읽어보니 **19조는 33/34/35-36조와 같은 성격의 구조 검토
대상**이다 — 계획 문서가 예상하지 못한 지점이라 명시적으로 보고한다.

**왜 architecture 이슈인가.** 19조의 본문 규정 자체가 이미 하나의 법적 효과다: "2인
이상의 독립행위가 경합하여 결과가 발생했는데 원인된 행위가 판명되지 않으면(=causation이
factually UNKNOWN), 각 행위자를 **미수범으로 처벌**한다." 그리고 263조(상해 특례)는
이를 뒤집어 "원인 불명이면 **공동정범의 예에 의한다**"(전원 기수범 취급)로 규정한다.

이건 v2.2.0의 기존 Completion 상태 규칙(Gate①, `|T|==0, U != ∅ → unresolved`)과
**정면으로 다르다** — 지금 런타임은 causal_nexus가 UNKNOWN이면 Completion을 `unresolved`로
둘 뿐, 19조처럼 "UNKNOWN을 미수범이라는 **확정된** 법적 결론으로 전환"하지 않는다. 즉
19조는:

```text
ground_fact.concurrent_independent_acts             2인 이상이 의사연락 없이 각자 별개의
                                                      행위(구성요건적 실행행위)를 하였다
ground_fact.same_object_of_result                    그 행위들이 동일한 객체에 결과를
                                                      발생시켰다(사회적·규범적 동일성)
legal_element.causal_origin_unascertained            결과 발생의 원인이 된 행위가 판명되지
                                                      않았다(causal_nexus가 각 행위자에
                                                      대해 개별적으로 UNKNOWN)

doctrine.concurrent_causation_default_attempt         원인불명이면 각자 미수범으로 처벌(19조 본문)
doctrine.injury_concurrent_causation_co_principal_fiction
    상해의 결과인 경우 원인불명이면 공동정범의 예에 의한다(263조 특례, 19조에 대한
    예외 — Participation의 apply_attribution/6C 런타임과 실제로 연결해야 하는지,
    아니면 별도 legal fiction effect가 필요한지 구조 검토 필요)
```

**이번 배치에서 predicate 후보만 제시하고 구조 결정은 보류한다** — 33/34/35-36조와
합쳐 "architecture-compatibility 검수 그룹"으로 다루자고 제안(원래 계획서가 33/34/35-36만
이 그룹으로 지정했던 것에 19조를 추가). Completion의 UNKNOWN 처리 규칙 자체를 손댈지,
아니면 19조 전용 특수 CompletionPolicy state로 표현 가능한지가 핵심 질문.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**13·14·18조는 없음** — 기존 `LegalElementDef`/`GroundFactDef`로 전부 표현된다.
**19조는 미정** — 위 architecture-compatibility 검토 결과에 따라 신규 CompletionPolicy
state 패턴이 필요할 수 있다(신규 effect/필드가 필요한지는 아직 판단 이르다).
