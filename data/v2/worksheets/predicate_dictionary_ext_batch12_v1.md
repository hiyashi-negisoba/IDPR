# Predicate 사전 확장 — 배치 ⑫ 절도·강도 나머지 (제330·331·332·334·335·337·338·342·343·344·356·360조) v1

[predicate_dictionary_ext_batch12_v0.md](predicate_dictionary_ext_batch12_v0.md)에 대한
사용자 검수(필수 수정 9건 + HOLD 축소 2건)를 전부 반영한다. v0은 그대로 둔다 — 이력
추적용. 이번 v1의 오류들은 대부분 **앞선 배치에서 이미 확정한 DSL 원칙으로부터의
drift**였다 — 신규 원칙이 아니라 재적용 누락.

---

## 정정 1 — 331조 1항의 `nighttime` 삭제는 오류, 복원한다

**v0 오류**: "1항·2항 요건을 함께 사용한 경우... 포괄일죄"를 다루는 원문 Ⅳ.2가 실은
**2항**(흉기휴대·합동)이 주간에 이루어진 경우를 논하는 절인데, 이걸 1항에도 적용되는
서술로 잘못 읽고 "nighttime은 1항 요건에서 제외한다"고 썼다. 그러나 형법 제331조
1항은 **조문 자체가 명문으로 "야간에" 문·담 등을 손괴할 것을 요구**하고, art331.md
원문 자체도 1항 절의 제목을 "Ⅱ. 손괴 후 **야간주거침입절도**(제1항)"라고 달아 1항이
D-1(330, 야간주거침입절도)의 가중유형임을 명시한다. 2항만 야간·주간 불문(주간이면
경합범, 야간이면 포괄일죄로 흡수)이라는 원문 Ⅳ.2의 논의를 1항에 잘못 전이시킨 것.

**v1(정정)**:

```text
331_para1.requires = ALL(
    nighttime_entry,                        (정정5, 아래에서 재정의)
    damage_to_entry_barrier,
    dwelling_or_managed_premises_object,
    trespass_entry,
    taking_conduct,
    unlawful_appropriation_intent,
    intent
)
```

2항은 그대로 야간·주간 불문(원문 Ⅳ.2가 실제로 다루는 대상) — 변경 없음.

---

## 정정 2 — 344절(I절)이 배치⑪ v0의 폐기된 predicate를 다시 참조했다, 전부 삭제

**v0 오류**: 배치⑪ 최종본(v3, predicate·doctrine 내용은 v2와 동일)을 확인하지 않고
**v0**(초안, 아직 검수 전)을 근거로 344절을 작성했다. 실제 배치⑪ v2 정정에서 328조는
2025.12.31.자 개선입법 시행으로 더 이상 형면제(EXEMPT) 구조가 아니라 "친족 간이면
고소가 있어야 공소제기 가능"이라는 **단일 소추조건(친고죄) 구조**로 개편되었고,
`doctrine.close_kin_property_offense_exemption`과 관련 게이팅 predicate 전부
삭제, **328조 전체가 predicate 사전 population 대상에서 제외**(procedure scope
밖, HOLD 아님 — 애초에 대상 아님)로 재분류되었다. v0의 I절은 이 폐기된
`legal_element.kinship_status_within_statutory_range`/`doctrine.close_kin_
property_offense_exemption`을 그대로 재참조하고, 이미 해소된 "헌법불합치·시행중지
상태 확인" HOLD까지 되살렸다 — 이중 오류.

**v1(정정) — I절 전체 재작성**:

> **제344조 친족간의 범행 (준용조문) — population 대상 아님.**
>
> 328조와 마찬가지로 344조는 predicate 사전 population 대상이 아니다(procedure
> scope 밖, HOLD 아님 — 애초에 대상 아님). 344조는 328조의 규정(소추조건 —
> 친고죄)을 329~332조(및 그 미수범)에 그대로 준용하는 지시 조문일 뿐 자체
> 구성요건이 없고, 328조 자신도 이미 형법상 실체적 법적 상태(EXEMPT 등)를 담고
> 있지 않으므로 344조에 대응하는 predicate·doctrine을 만들지 않는다.
>
> 카드 4장(article328_theft_offenses_scope, robbery_no_family_benefit,
> kinship_with_owner_and_possessor, kinship_only_one_holder_no_application)은
> 전부 이 준용 범위(어느 죄에 적용되는지, 누구와의 친족관계인지)에 대한 사실관계
> 서술이며, 328조 자신이 procedure scope 밖으로 확정된 이상 344조 역시 그 사실을
> authoring 메모로만 남긴다.
>
> **강도죄(333·334·335·337·338)에는 준용되지 않는다**(카드 robbery_no_family_
> benefit) — D·E·F·G절 어디에도 328/344 관련 predicate가 등장하지 않는 것은
> 누락이 아니라 이 준용 범위 확정에 따른 의도된 결과다.
>
> **범위 밖**: 354·361·365조(장물죄 관련, 328조가 준용 대상으로 언급하지만 51개
> 조문 워크시트 범위 밖)는 배치⑪이 이미 명시한 대로 여전히 범위 밖. 328조①의
> 개선입법 반영 여부 확인은 **배치⑪에서 이미 완료**되었으므로(위 설명대로 procedure
> scope 밖으로 재분류 완료) 이번 배치에서 다시 HOLD로 올리지 않는다.

**360절(J-2)의 "친족상도례" 단락도 동일하게 수정** — `kinship_status_within_
statutory_range` predicate 바인딩 언급을 삭제하고, "328/344는 population 대상이
아니므로 360이 준용 대상이라는 사실만 여기 authoring 메모로 남긴다"로 축약한다
(J절 재작성, 아래 정정9와 함께 반영).

**하단 HOLD/architecture-compatibility 종합 목록에서도 "art328① 헌법불합치·시행중지
상태 확인" 관련 서술이 있다면 제거** — 배치⑪에서 이미 해소된 사안이라 이번 배치의
확인 대상이 아니다(v0에는 이 항목을 직접 올리지 않았으나, I절 오류로 인해 암묵적으로
되살아난 상태였으므로 명시적으로 제거를 확인해둔다).

---

## 정정 3 — 343조 목적요건에 `legal_element.intent`(13조)를 재정의하지 않는다, `purpose_to_commit_target_offense`(28조, 배치④ 확정) 재사용

**v0 오류**: "강도(단순강도·특수강도·약취강도·해상강도 — 준강도는 제외)를 범할
목적이 있다"는 요건을 `legal_element.intent`(13조 재사용)의 canonical_meaning으로
써넣었다 — 이건 13조 고의(구성요건적 사실에 대한 인식·의욕)를 "특정 범죄를 범할
목적"이라는 **다른 개념**으로 조용히 재정의한 것이다. 배치④(28조 예비음모)가 이미
이 정확한 요건을 위해 `legal_element.purpose_to_commit_target_offense`를
확정해뒀다(`predicate_dictionary_ext_batch04_v2.md`, "PREPARATION_OR_CONSPIRACY.
requires = purpose_to_commit_target_offense") — 새로 만들 필요도, 13조로 대체할
필요도 없었다.

**v1(정정)**:

```text
343.requires = ALL(
    ANY(preparatory_conduct, conspiracy_agreement),
    purpose_to_commit_target_offense
)
```

**"target이 강도죄군이라는 것은 343 authoring의 조건이지 predicate의 canonical_
meaning을 바꾸는 게 아니다.** `purpose_to_commit_target_offense`는 28조가 이미
"목적하는 죄를 범할 목적"이라는 general한 정의로 확정해둔 predicate이고, 343조가
그 목적의 대상(target offense)을 "강도(단순강도·특수강도·약취강도·해상강도 —
준강도 제외)"로 한정하는 것은 343조 자신의 `PREPARATION_OR_CONSPIRACY` state를
어느 target offense 집합에 대해 인스턴스화하는지의 authoring 문제다 — F-1(335조
저작 시 이미 확정)이 "준강도는 절도의 파생 offense이지 333/334조의 하위분류가
아니므로 애초에 이 target 집합에 들어오지 않는다"고 설명한 구조 그대로 유지된다
(canonical_meaning 재정의 없이 그대로 성립).

---

## 정정 4 — 330·331·334 CompletionPolicy에 exact-one 겹침이 다시 생겼다

**v0 오류**: `ATTEMPTED.when = commencement_of_execution` / `COMPLETED.when =
taking_conduct`로만 적어, 절취가 완료된 사건에서 `commencement_of_execution`도
계속 TRUE이므로 `ATTEMPTED`와 `COMPLETED`가 동시에 성립해버린다. 배치⑨·⑩이 이미
"`attempted.when`에 `NOT(...)`을 추가해 completed와의 겹침을 제거한다"는 6B
exact-one 원칙을 확정해뒀는데(133①의 `NOT(bribe_promise), NOT(bribe_giving)`,
301의 `NOT(injury_intent)`), 이번 배치에서 D-1·D-2·E-1 세 곳 모두 이 원칙을
빠뜨렸다.

**v1(정정) — D-1(330)**:

```text
ATTEMPTED.when = ALL(commencement_of_execution(trespass_entry 기준), NOT(taking_conduct))
COMPLETED.when = taking_conduct
```

**D-2(331) 1항·2항 동일 원칙**:

```text
331_para1: ATTEMPTED.when = ALL(commencement_of_execution(damage_to_entry_barrier 기준), NOT(taking_conduct))
           COMPLETED.when = taking_conduct
331_para2: ATTEMPTED.when = ALL(commencement_of_execution(taking_conduct 착수, 물색행위), NOT(taking_conduct))
           COMPLETED.when = taking_conduct
```

**E-1(334) — 별도 state 두 개 대신, 하나의 `ATTEMPTED.when` 안에서 `ANY`로 갈래를
둔다(구조 정정, 아래 별도 설명).**

```text
334.ATTEMPTED.when = ALL(
    ANY(
        commencement_of_execution(trespass_entry 기준),           (야간 전체 + 1항)
        commencement_of_execution(robbery_level_violence 착수)     (주간 흉기휴대·합동, 2항)
    ),
    NOT(property_disposition류(333 재사용, 재물·이익 취득))
)
334.COMPLETED.when = property_disposition류(333 재사용)
```

v0이 "334_para1"/"334_para2, 주간"/"334_para2, 야간" 세 갈래를 별도 state처럼
서술했던 건 CompletionPolicy 설계상 부정확했다 — `ATTEMPTED`는 334조 전체에 대해
**하나의 state**이고, 착수 시점을 가르는 기준(주거침입 시 vs 폭행·협박 시)만
사실관계별로 `ANY`의 두 가지로 갈리는 것이지 별도 state가 아니다(state를 나누는
건 `punishable`이나 법적 효과가 달라질 때만 — 25-27조 원칙 재확인).

---

## 정정 5 — `nighttime AT trespass_entry`는 현재 DSL에 없는 문법이다, 새 연산자 없이 닫는다

**v0 오류**: "야간"이 "침입행위 시점"에 결합되어야 한다는 사실관계를 `nighttime
AT trespass_entry`라는 표기로 쓰고, 이를 표현 불가능한 것처럼 HOLD로 올렸다 —
`AT` 같은 시점 결합 연산자는 이 DSL에 없고, 이 한 사례 때문에 새 temporal
primitive를 만들 필요가 없다.

**v1(정정)**: 시점을 predicate 자체의 정의 안에 미리 접어 넣는다.

```text
legal_element.nighttime_entry(신규)
    = 침입행위(trespass_entry)가 일몰 후부터 일출 전까지의 시간대에 이루어졌다
```

D-1(330)·E-1(334, 1항 및 2항 중 야간에 이루어진 경우)이 이 하나의 predicate를
공유한다 — `nighttime`(v0의 별도 시점-비종속 정의)은 폐기하고
`nighttime_entry`로 대체한다. 새 연산자(`AT`) 없이 기존 `LegalElementDef`
하나로 닫힌다.

---

## 정정 6 — 335조 F-5는 신규 completion-linkage architecture gap이 아니다, HOLD 해제

**v0 오류**: "base offense(절도)의 completion state가 그대로 파생 offense(준강도)의
completion state를 결정한다"는 링크를 8차 addendum `derivative_mode.requires`로
표현 가능한지 확인이 필요한 신규 architecture gap으로 올렸다. 그러나
`derivative_mode.requires`는 **교사·방조(derivative liability, 33조/34조 계열)의
정범 실현 여부를 파생 책임 성립 조건에 반영하는 필드**이지 `DerivedOffenseDef`
자신의 completion 전달 장치가 아니다 — 서로 다른 메커니즘을 섞었다.

**v1(정정) — 335조 자신의 CompletionPolicy를 기존 case truths로 직접 저작한다,
별도 링크 메커니즘 불필요.**

```text
335.COMPLETED.when = taking_conduct
335.ATTEMPTED.when = ALL(commencement_of_execution, NOT(taking_conduct))
```

`taking_conduct`는 F-1이 이미 재사용을 확정한 329(절도)의 predicate이고, 335가
그 predicate를 **자신의 requires에도 직접 요구**한다(F-1 base offense 재사용
구조 자체는 그대로 유지) — 즉 base offense state를 "복사해오는" 별도 링크가
아니라, 335 자신의 `CompletionPolicy`가 자신이 요구하는 predicate(`taking_
conduct`)를 그대로 판정 기준으로 쓰는 것뿐이다. 폭행·협박(`robbery_level_
violence`)·목적(F-2)·기회(F-3, `occasion_identity`)는 335의 Elements/Relations가
별도로 요구하며 completion 판정 자체에는 관여하지 않는다(완성된 절도 + 목적을
가진 폭행·협박이 있으면 335 자체가 성립하고, 그 성립의 기수·미수는 오직
`taking_conduct` 하나로 판정된다는 뜻 — 2004도5074 전합의 "절취행위 기준설"과
정확히 일치).

**F-5-1 architecture-compatibility 확인사항은 이번 정정으로 해제한다** — 신규
completion-linkage 메커니즘이 필요하지 않다는 게 확인되었으므로 HOLD 목록에서
제거한다(아래 종합 목록 갱신).

---

## 정정 7 — 335조 `purpose_to_resist_recapture`에서 객관적 "배타적 지배 확립"을 분리한다

**v0 오류**: mental predicate(목적)의 canonical_meaning 안에 "이미 배타적 지배가
확립된 후"라는 **객관적 사실 상태**를 함께 집어넣었다 — mental predicate는 목적
그 자체(주관적 요소)만 판단해야 하고, 그 목적이 유효하게 준강도의 요건으로
작동하는지를 가르는 객관적 게이팅은 별도 leaf로 분리해야 한다. 그리고 이미
`taking_conduct`(F-1에서 재사용 확정된 329 predicate, "타인 점유 재물을... 자기
점유로 옮겼다")가 "재물에 대한 사실상 지배를 확보했다"는 객관적 사실을 담고
있으므로, 신규 predicate 없이 그대로 재사용하면 된다.

**v1(정정)**:

```text
legal_element.purpose_to_resist_recapture(정정 — 목적만, 객관적 상태 서술 삭제)
    = 절도가 탈취한 재물을 피해자 측으로부터 탈환당하지 않기 위하여 대항할
      목적을 가지고 있다

quasi_robbery.requires 中 목적요건 =
    ANY(
        ALL(taking_conduct, purpose_to_resist_recapture),
        purpose_to_avoid_arrest,
        purpose_to_conceal_evidence
    )
```

"배타적 지배 미확립 상태에서의 폭행은 본래의 강도(333/334)"라는 카드의 결론은
이제 `taking_conduct AND purpose_to_resist_recapture`가 모두 성립하지 않으면
(예: 아직 절도 자체가 미완성이거나, 재물 확보 전 단계) 이 ANY 갈래가 실패하고
다른 목적 갈래도 없으면 335 자체가 성립하지 않는다는 구조로 그대로 표현된다 —
신규 predicate도, 새 게이팅 메커니즘도 필요 없다. 나머지 두 목적(체포면탈·증거
인멸)은 카드가 이미 확정한 대로 재물 지배 취득을 요건으로 하지 않으므로
`taking_conduct`와 결합하지 않는다.

---

## 정정 8 — 337·338에서 base-offense 내부 인과관계(`result_causation`)와 COMPOSE 인과관계(`relation.causal_nexus`)가 다시 섞였다

**v0 오류**: 337에 `legal_element.result_causation`과 `relation.causal_nexus`를
둘 다 넣고, 338은 `death_of_victim`(가중결과 자체) 없이 `result_causation`만으로
사망 완성을 표현했다. 배치⑨가 이미 확정한 인과관계 이층 모델을 다시 어겼다 —
**단일 base OffenseDef 내부(conduct→result)는 `legal_element.result_causation`
(250·267·268 전용), COMPOSE된 `DerivedOffenseDef` 컴포넌트 간(base↔가중결과)은
`relation.causal_nexus`**(259·301이 이미 이 원칙으로 확정) — 337·338은 COMPOSE
구조이므로 `result_causation`을 쓸 자리가 아니다. 또한 338의 사망 완성은
"result_causation" 하나로 뭉뚱그릴 게 아니라, 259가 이미 확정한 `ground_fact.
death_of_victim`(가중결과 그 자체)을 그대로 재사용해야 했다.

**v1(정정) — 259·301과 동일한 COMPOSE 패턴으로 재작성, `result_causation` 삭제.**

### G-1(337) 재작성

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.injury_result`(배치⑨·⑩ 재사용) | 상해의 결과가 발생하였다 | 배치⑨·⑩ |
| `legal_element.injury_intent`(배치⑩ 301 신규, 재사용) | 상해의 결과에 대한 고의(미필적 고의로 족하다) — base offense(강도) 자신의 intent와는 별개의 predicate | 배치⑩ |
| `primitive.aggravated_result_attribution`(259·301 재사용, "치상" 변형) | 결과에 대한 예견가능성과 상당인과관계 | 배치⑧·⑨·⑩ |
| `relation.causal_nexus`(6B·259·301 재사용) | base(강도)의 수단행위(폭행·협박)와 상해 결과 사이의 인과관계 | 배치⑨·⑩ |
| `relation.occasion_identity`(6B 재사용) | 상해 결과가 강도의 "기회"에 발생하였다 | 배치⑨·⑩ |

```text
337.base_offense = ANY(333 강도, 334 특수강도, 335 준강도, 336 인질강도[범위 밖, 참조만])
337.requires = ALL(
    base_offense.requires,
    injury_result,
    ANY(
        injury_intent,
        ALL(aggravated_result_attribution, NOT(injury_intent))
    ),
    causal_nexus,
    occasion_identity
)
```

`NOT(injury_intent)`를 치상(결과적가중범) 갈래에 추가해 강도상해(고의)/강도치상
(결과적가중범) 두 갈래가 겹치지 않게 한다 — 301이 이미 확정한 exact-one 패턴
(self-check5, 6B) 그대로 재사용.

### G-2(338) 재작성

| id | canonical_meaning | 출처 |
|---|---|---|
| `ground_fact.death_of_victim`(259 재사용) | 피해자가 사망하였다 | 배치⑨ |
| `legal_element.homicide_intent`(신규, "살인" 변형 전용) | 사망의 결과에 대한 고의 — base offense(강도) 자신의 intent와는 별개의 predicate(301의 `injury_intent` 분리와 정확히 같은 이유) | art338_sec4.robbery_murder_attempt |
| `primitive.aggravated_result_attribution`(259 재사용, "치사" 변형) | — | art338_Ⅲ |
| `relation.causal_nexus`(6B·259 재사용) | base(강도)의 수단행위와 사망 결과 사이의 인과관계 | art338_Ⅲ |
| `relation.occasion_identity`(6B 재사용) | 사망 결과가 강도의 "기회"에 발생하였다 | art338_Ⅲ |

```text
338.base_offense = ANY(333 강도, 334 특수강도, 335 준강도, 336 인질강도[범위 밖, 참조만])
338.requires = ALL(
    base_offense.requires,
    death_of_victim,
    ANY(
        homicide_intent,
        ALL(aggravated_result_attribution, NOT(homicide_intent))
    ),
    causal_nexus,
    occasion_identity
)
```

**CompletionPolicy(337·338 공통) — 정정 8 반영, `result_causation` 언급 삭제.**

```text
337.COMPLETED.when = injury_result (재물탈취 완료 여부 무관)
337.ATTEMPTED.when = ALL(commencement_of_execution(상해행위 착수), NOT(injury_result))
    — 강도의 기수·미수 불문(카드 확정), 상해미수 기준
337_치상(aggravated_result_attribution 갈래).ATTEMPTED.punishable = false (결과적가중범 미수 불가)

338.COMPLETED.when = ALL(death_of_victim, homicide_intent)
338.ATTEMPTED.when = ALL(commencement_of_execution(살인행위 착수), NOT(death_of_victim))
    — 강도의 기수·미수 불문
338_치사(aggravated_result_attribution 갈래).ATTEMPTED.punishable = false
```

---

## 정정 9 — 356조는 하나의 `ANY(횡령, 배임)` 대신 두 개의 `DerivedOffenseDef`로 분리한다

**v0 오류**: `356.base_offense = ANY(355 횡령, 355 배임)`로 하나의 offense 안에서
base를 ANY로 묶었다 — 이러면 업무상횡령과 업무상배임이라는 **서로 다른 죄종
identity**가 하나의 offense_ref로 합쳐져 버린다(법정형·구성요건이 다른 두 개의
별개 범죄를 하나의 정의로 뭉갬).

**v1(정정)**:

```text
occupational_embezzlement(업무상횡령) = QUALIFY(embezzlement[355], business_status)
occupational_breach_of_trust(업무상배임) = QUALIFY(breach_of_trust[355], business_status)
```

두 개의 독립된 `DerivedOffenseDef`로 분리하고, 각각 355의 두 갈래(횡령/배임) 중
하나만을 base로 QUALIFY한다 — `business_status`(J-1이 이미 확정한 신규 legal_
element, exception 카드 3장 반영 포함)의 정의·내용은 그대로 유지되고, 이번
정정은 offense 조립 구조만 바로잡는다.

---

## HOLD 축소 1 — 331조 합동범을 30조 Participation과 합칠 이유 없음

**v0**: `joint_commission_by_two_or_more`가 30조(공동정범) predicate의 특수
적용인지, 331조 2항 고유의 "현장성" 요건이 추가된 독립 legal_element인지
architecture-compatibility 확인사항으로 올렸다.

**v1(축소)**: 이건 확인이 필요한 gap이 아니다 — `joint_commission_by_two_or_
more`는 331조(및 334조 2항, E-1)의 **객관적 가중 구성요건 요소**(Elements 층의
`legal_element`)로 그대로 두면 된다. 판례(98도321 전합)가 "공동정범의 일반
이론에 비추어"라고 말하는 것은 30조 법리를 **참고**한다는 뜻이지 30조 predicate를
그대로 가져다 재사용해야 한다는 뜻이 아니다 — 331조 2항 자신의 구성요건("2명
이상이 합동")이 이미 완결된 legal_standard(현장적 공동정범설 포함)를 갖고
있으므로, 30조와 별도로 두는 게 오히려 정확하다(30조가 다루는 것은 "공범자
사이의 책임 귀속" 문제이고, 331조 2항의 이 predicate는 "가중처벌을 발생시키는
행위태양 자체가 성립했는가"라는 Elements 문제 — 서로 다른 질문). D-2·E-1의
predicate 정의는 그대로 유지, HOLD 항목에서만 제거한다.

## HOLD 축소 2 — 332/335 법정형 선택을 Step 7 orchestrator 문제로 과대평가하지 않는다

**v0**: 상습절도(332)·준강도(335)의 "base offense 종류에 따라 적용 법정형이
분기"하는 구조를 architecture-compatibility 확인사항으로 올렸다.

**v1(축소)**: 현재 DSL은 애초에 **구체적 법정형 계산기를 만들고 있지 않다**(배치⑥
36조 확정 — `statutory_refs`는 인용 문자열일 뿐 법적 효과가 없다는 원칙과 동일선상).
"단순절도 상습범이면 333조 예에 의하고, 특수절도 상습범이면 334조 예에 의한다"는
서술도 형량 계산이 아니라 **offense identity 자체가 무엇으로 확정되는지**의
문제이므로, predicate 사전이나 architecture-compatibility 확인사항으로 다룰 게
아니라 **offense 조립 시의 authoring note**로 낮춘다 — base offense가 무엇으로
사실관계상 확정되는지에 따라 332/335 자신의 `offense_ref`가 결정된다는 사실은
D-3·F-6에 그대로 authoring 메모로 남기되(내용 삭제 안 함), HOLD 종합 목록에서는
제거한다.

---

## 갱신된 HOLD / 2-pass 확인 목록 (v1 최종)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례, 257·298조
자상·도구 간접정범, 250조 비신분자 존속살해 가담, 301조 결합범+결과적가중범
병존, 299조 예비음모 conduct 갈래 제한, art323 소유자 아닌 자의 가담↔33조 본문
공동정범, art319 계절적 미사용 별장 서브타입 재분류, art319 퇴거불응 미수)에
이번 배치로 다음 **2건만** 추가된다(v0의 4건 중 F-5-1은 정정6으로 해제, D-2의
합동범·D-3/F-6의 법정형 선택은 위 HOLD 축소로 제거):

1. **art331 `dangerous_weapon_carriage`를 배치⑨ 258의2 `dangerous_object_
   carriage`와 같은 predicate로 재사용할지 확인(D-2-1)** — 두 조문의 판례 정의
   문구를 대조하면 확정 가능한 성격.
2. **art335 `occasion_identity`("절도의 기회")를 337·338(G절, "강도의 기회")과
   같은 predicate로 재사용할지 확인(F-3-1)** — canonical_meaning 불변 원칙에
   따라 신중히 검토.

**구조 선택 문제(gap 아님, 그대로 유지)**: art360 `property_of_another`와 366
`object_ownership_other`의 재사용 여부(J-2-1), art360 `embezzlement_
manifestation`을 355/356/360 세 조문이 공유하는 것의 확정 여부(J-2-2).

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음, 확정.** v0에서 유일하게 "미확정"으로 남겼던 F-5-1(준강도 completion-
linkage)이 정정6으로 완전히 해소되었다 — `DerivedOffenseDef` 자신의
`CompletionPolicy`가 자신이 요구하는 predicate를 그대로 판정 기준으로 삼는
기존 방식으로 충분했다. 나머지 전부 기존 `LegalElementDef`/`GroundFactDef`/
`DerivedOffenseDef`(COMPOSE·QUALIFY 재사용)/6B `RelationDef`(causal_nexus·
occasion_identity 재사용)/`primitive.aggravated_result_attribution`(배치⑧
확정)/25조 Completion predicate로 표현된다.

---

## self-check 체크리스트 재적용 메모 (정정 후 재검증)

1. **카드 분해**: 정정 없음(v0 판단 유지) — 335 목적요건 3분리, 331/334 흉기·합동
   분리 모두 그대로.
2. **doctrine 자격 검사**: 정정6으로 재확인 — 335는 doctrine도 아니고 별도
   completion-linkage가 필요한 특수 구조도 아닌, **표준적인 `DerivedOffenseDef`
   + 자체 CompletionPolicy**였다. v0이 "특수 링크가 필요하다"고 과대평가한 것
   자체가 이번 배치의 핵심 교정 지점.
3. **긍정형 이름**: 정정7 이후 `purpose_to_resist_recapture`가 더 이상 객관적
   상태를 섞지 않게 되어, mental predicate와 objective predicate의 경계가
   명확해졌다 — positive-predicate 원칙 재확인.
4. **`ONE_OF` 사용 전 배타성 증명**: 여전히 `ONE_OF` 미사용. D-1·D-2·E-1·F·G의
   `ATTEMPTED`/`COMPLETED`는 이제 전부 `NOT(...)`으로 exact-one이 명시적으로
   보장된다(정정4·정정8) — v0에서 빠졌던 부분을 전부 메움.
5. **CompletionPolicy state 반례 대입**: 337에 "강도 자체는 미수인데 상해는
   기수인 사건"을 대입 — `injury_result`가 강도의 기수·미수와 무관하게
   독립적으로 판정되므로 337은 정상적으로 COMPLETED가 된다(카드·원문이 명시한
   "재물탈취 목적 달성 불요"와 일치, 재확인 완료).
6. **일반원칙 서술 전 인접 대조**: 337 ↔ 259/301(COMPOSE 이층 모델)을 다시
   대조해 `result_causation`이 아니라 `causal_nexus`가 맞다는 걸 재확인(정정8).
   335 ↔ 28조(343 예비음모 목적요건)를 대조해 `purpose_to_commit_target_
   offense` 재사용을 확인(정정3).
7. **stage 라벨-설명 일치**: 356의 `business_status`는 여전히 legal_element로
   유지(정정9는 offense 조립 구조만 변경, stage 분류는 그대로).

---

## 배치⑫ v1 — 최종 확정, 종료

D절(330·331·332)·E절(334)·F절(335)·G절(337·338)·H절(342·343)·I절(344, population
대상 아님)·J절(356·360)이 정정 1-9 반영으로 확정되었다. 신규 스키마·DSL primitive
없음(확정). HOLD/2-pass 확인 목록은 2건으로 축소(D-2-1, F-3-1) + 기존 구조 선택
문제 2건(J-2-1, J-2-2) 유지. 다음은 art339(강도강간, 카드 없음 — 51개 조문 중
유일하게 원본 주석서를 직접 열람해 authoring해야 하는 조문, v0의 마지막 절 그대로
다음 세션 시작점).
