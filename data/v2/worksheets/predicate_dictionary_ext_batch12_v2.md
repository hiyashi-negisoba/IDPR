# Predicate 사전 확장 — 배치 ⑫ 절도·강도 나머지 (제330·331·332·334·335·337·338·342·343·344·356·360조) v2

[predicate_dictionary_ext_batch12_v1.md](predicate_dictionary_ext_batch12_v1.md)에 대한
사용자 검수 3건을 반영한다. v1은 그대로 둔다 — 이력 추적용. 이번 v2의 오류 2건(335
Elements 과잉 요구, 338 Completed 공식 오류)은 **정정을 적용하면서 그 정정이 다른
곳에 만드는 부작용을 반례로 검증하지 않은** 같은 종류의 실수다 — self-check5
(CompletionPolicy state 반례 대입)를 정정 직후 다시 하지 않은 게 원인.

---

## 정정 10 — 335 Elements가 `taking_conduct`를 직접 요구하면 절도미수+폭행·협박(준강도미수) 자체가 봉쇄된다

**v1 오류**: 정정6에서 "335가 `taking_conduct`를 자신의 requires에도 직접
요구한다"고 썼다. 이러면 `taking_conduct`(절도 기수)가 335 **Elements 자체의
성립조건**이 되어버려, 절도가 아직 미수인 사건(폭행·협박은 있었으나 재물취거는
실패)에서는 335 Elements 자체가 실패하고 `ATTEMPTED` 판정까지 갈 수조차 없다 —
그런데 카드(art335_sec7.attempt_punishable, art335_sec7_1)와 2004도5074 전합이
정면으로 확정하는 게 바로 **준강도미수**(절도가 미수인 경우 준강도도 미수)다.
`taking_conduct`는 335 **전체의 필수 Elements가 아니라 completion selector**로만
써야 했다.

**v2(정정) — Elements와 Completion을 분리한다.**

```text
335.requires(Elements) = ALL(
    commencement_of_execution(절도, 즉 329/330/331 중 하나의 실행착수 이상
                               — 예비단계 제외, art335_sec2.preparation_stage_
                               exclusion을 그대로 커버),
    ANY(                                                        (목적요건, 정정7 유지)
        ALL(taking_conduct, purpose_to_resist_recapture),
        purpose_to_avoid_arrest,
        purpose_to_conceal_evidence
    ),
    robbery_level_violence,
    occasion_identity
)

335.COMPLETED.when = taking_conduct
335.ATTEMPTED.when = ALL(commencement_of_execution, NOT(taking_conduct))
```

`taking_conduct`는 이제 두 곳에서만 등장한다 — (1) 목적요건의 `ALL(taking_conduct,
purpose_to_resist_recapture)` 갈래(재물탈환 목적에만 배타적 지배 확보가 전제된다는
카드 요건, 정정7 그대로 유지), (2) `Completion`의 selector. **Elements의 최상위
`requires`에는 `taking_conduct`가 직접 나타나지 않는다** — base offense 연결은
`commencement_of_execution`(실행착수 이상)만으로 충분하고, 이건 절도가 미수든
기수든 335 Elements 자체는 성립할 수 있다는 뜻이다(그 위에서 completion만
`taking_conduct`로 갈린다).

체포면탈·증거인멸 목적 갈래(`purpose_to_avoid_arrest`/`purpose_to_conceal_
evidence`)는 원래부터 `taking_conduct`와 결합되지 않으므로 이번 정정과 무관 —
절도미수 상태에서 체포면탈 목적으로 폭행한 경우 이미 v1에서도 정상적으로 335
Elements를 충족했었다(정정10이 고치는 건 재물탈환 목적 갈래가 아니라 **base
offense 연결부**였다는 점에 주의).

---

## 정정 11 — 337·338 CompletionPolicy가 301의 미해결 HOLD(결합범/결과적가중범 병존 구조)를 선결해버렸다, predicate 정의까지만 확정한다

**v1 오류**: G-1·G-2에 구체적 `COMPLETED.when`/`ATTEMPTED.when` 공식을
variant(고의/결과적가중범)별로 나누어 확정했다. 그런데 301(강간등 상해치상)이
이미 남겨둔 HOLD — "결합범(고의)+결과적가중범(과실) 병존을 별도
`DerivedOffenseDef` 2개로 할지 단일 `DerivedOffenseDef` 내 두 갈래로 할지는
2-pass에서 결정" — 이 아직 살아있는 상태에서 337·338의 CompletionPolicy를
먼저 확정해버리면 그 구조 선택을 **predicate 사전 단계에서 암묵적으로
선결**하는 셈이다. 게다가 그 공식 자체에 **명백한 오류**가 있었다 —

```text
338.COMPLETED.when = ALL(death_of_victim, homicide_intent)
```

이 공식은 `homicide_intent`(고의)가 없는 **강도치사**(결과적가중범, 사망에 대한
고의 없이 `aggravated_result_attribution`만으로 성립하는 갈래)가 영원히
`COMPLETED`에 도달하지 못하게 만든다 — 카드(art338_sec4.robbery_death_attempt_
excluded)가 명시하는 "살인의 고의가 없는 강도치사죄" 자체를 봉쇄하는 실질적
오류. 정정10과 마찬가지로 self-check5(반례 대입)를 다시 하지 않아 발생했다.

**v2(정정) — predicate 정의(branch별 leaf)까지만 이 배치에서 확정하고, 구체
CompletionPolicy 분리는 301과 함께 2-pass로 미룬다.**

### G-1(337) — predicate만 확정

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.injury_result`(배치⑨·⑩ 재사용) | 상해의 결과가 발생하였다 | 배치⑨·⑩ |
| `legal_element.injury_intent`(배치⑩ 301 신규, 재사용) | 상해의 결과에 대한 고의(미필적 고의로 족하다) — base offense(강도) 자신의 intent와는 별개 | 배치⑩ |
| `primitive.aggravated_result_attribution`(259·301 재사용, "치상" 변형) | 결과에 대한 예견가능성과 상당인과관계 | 배치⑧·⑨·⑩ |
| `relation.causal_nexus`(6B·259·301 재사용) | base(강도)의 수단행위와 상해 결과 사이의 인과관계 | 배치⑨·⑩ |
| `relation.occasion_identity`(6B 재사용) | 상해 결과가 강도의 "기회"에 발생하였다 | 배치⑨·⑩ |

```text
337.base_offense = ANY(333 강도, 334 특수강도, 335 준강도, 336 인질강도[범위 밖, 참조만])
337.requires = ALL(
    base_offense.requires,
    injury_result,
    ANY(injury_intent, aggravated_result_attribution),
    causal_nexus,
    occasion_identity
)
```

### G-2(338) — predicate만 확정

| id | canonical_meaning | 출처 |
|---|---|---|
| `ground_fact.death_of_victim`(259 재사용) | 피해자가 사망하였다 | 배치⑨ |
| `legal_element.homicide_intent`(신규, "살인" 변형 전용) | 사망의 결과에 대한 고의 — base offense(강도) 자신의 intent와는 별개(301의 `injury_intent` 분리와 정확히 같은 이유) | art338_sec4.robbery_murder_attempt |
| `primitive.aggravated_result_attribution`(259 재사용, "치사" 변형) | — | art338_Ⅲ |
| `relation.causal_nexus`(6B·259 재사용) | base(강도)의 수단행위와 사망 결과 사이의 인과관계 | art338_Ⅲ |
| `relation.occasion_identity`(6B 재사용) | 사망 결과가 강도의 "기회"에 발생하였다 | art338_Ⅲ |

```text
338.base_offense = ANY(333 강도, 334 특수강도, 335 준강도, 336 인질강도[범위 밖, 참조만])
338.requires = ALL(
    base_offense.requires,
    death_of_victim,
    ANY(homicide_intent, aggravated_result_attribution),
    causal_nexus,
    occasion_identity
)
```

`ANY(injury_intent, aggravated_result_attribution)`/`ANY(homicide_intent,
aggravated_result_attribution)`에서 v1에 있던 `NOT(injury_intent)`/`NOT
(homicide_intent)` 게이팅은 **이번엔 넣지 않는다** — 그 겹침 제거가 필요한
지점은 Elements가 아니라 CompletionPolicy(어느 state로 갈리는지) 층위이므로,
CompletionPolicy 자체를 HOLD로 미루는 이상 여기서 미리 게이팅을 확정하면 또
같은 종류의 선결 오류가 된다.

**CompletionPolicy — 구체 공식 확정하지 않음, HOLD로 이월.** 301의 기존 HOLD
항목("결합범+결과적가중범 병존을 별도 `DerivedOffenseDef` 2개로 할지 단일
`DerivedOffenseDef` 내 두 갈래로 할지")에 337·338을 **동일 유형의 세 번째·네
번째 사례**로 추가한다(신규 HOLD 항목 아님, 기존 항목 확장) — 아래 종합 목록
갱신.

**신규 스키마 여부에는 영향 없음** — predicate 층위(injury_result/injury_
intent/death_of_victim/homicide_intent/aggravated_result_attribution/causal_
nexus/occasion_identity)는 전부 기존 정의 재사용이고, 미확정인 건 그
predicate들을 CompletionPolicy에서 어떻게 조립하느냐(variant 2개 vs 1개
내부 분기)뿐이다 — 이건 기존 `DerivedOffenseDef`/`CompletionPolicyDef`로
양쪽 다 표현 가능한 구조 선택 문제이지 architecture gap이 아니다(301과 동일
성격).

---

## 정정 12 — 360조의 친족상도례 준용 근거는 344조가 아니라 361조다

**v1 오류**: 정정2에서 J절(360)의 친족상도례 서술을 "328/344는 population
대상이 아니므로..."로 고쳤는데, **360조(점유이탈물횡령)에 328조를 준용하는
governing provision은 344조가 아니라 361조**다 — 344조는 329~332조(절도죄군)에
대한 준용이고, 355~360조(횡령·배임죄군)에 대한 준용은 361조(친족간의 범행,
동력)가 별도로 규정한다. 조문 번호를 잘못 인용했다.

**v2(정정) — J절(360) 친족상도례 단락**:

> **친족상도례 — 328조가 361조를 통해 준용되나, 위탁관계 불요이므로
> "행위자-소유자"만 필요(원문 확정, I절과 대조).** 355(위탁관계 기반)와 달리
> 360은 신분관계 요건이 없으므로 준용되는 328조 상당 판단을 "행위자-소유자"
> 쌍방향으로만 바인딩한다. **361조(51개 조문 워크시트 범위 밖) 자신도 328조와
> 마찬가지로 procedure scope 밖**(소추조건 준용 지시 조문일 뿐 자체
> 구성요건이 없음)이라 predicate를 만들 필요는 없지만, governing provision
> 식별 자체는 344조가 아니라 361조로 정확히 기록해야 한다(I절이 확정한
> "328/344는 population 대상 아님" 원칙과 별개로, 360조 자신의 준용조문
> 인용은 361조가 맞다).

**I절(344) 서술은 변경 없음** — 344조는 여전히 절도죄군(329~332)에 대한 준용
근거로 정확했고, 이번 정정은 J절(360)의 인용 오류만 바로잡는다.

---

## 갱신된 HOLD / 2-pass 확인 목록 (v2 최종)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례, 257·298조
자상·도구 간접정범, 250조 비신분자 존속살해 가담, **301조 결합범+결과적가중범
병존**, 299조 예비음모 conduct 갈래 제한, art323 소유자 아닌 자의 가담↔33조 본문
공동정범, art319 계절적 미사용 별장 서브타입 재분류, art319 퇴거불응 미수)에
이번 배치로 다음이 추가·갱신된다:

1. **art331 `dangerous_weapon_carriage`를 배치⑨ 258의2 `dangerous_object_
   carriage`와 같은 predicate로 재사용할지 확인(D-2-1)** — v1과 동일, 유지.
2. **art335 `occasion_identity`("절도의 기회")를 337·338(G절, "강도의 기회")과
   같은 predicate로 재사용할지 확인(F-3-1)** — v1과 동일, 유지.
3. **기존 "301조 결합범+결과적가중범 병존" HOLD 항목에 337·338을 동일 유형
   사례로 추가**(신규 항목 아님, 정정11) — 2-pass에서 301·337·338 세 조문을
   함께 결정.

**구조 선택 문제(gap 아님, 그대로 유지)**: art360 `property_of_another`와 366
`object_ownership_other`의 재사용 여부(J-2-1), art360 `embezzlement_
manifestation`을 355/356/360 세 조문이 공유하는 것의 확정 여부(J-2-2).

---

## self-check 체크리스트 재적용 메모 (v2, 반례 대입 강화)

1-4, 6-7번은 v1과 동일(변경 없음). **5번(CompletionPolicy state 반례 대입)을
이번엔 정정 직후 실제로 다시 수행**했다:
- 335: "절도미수(taking_conduct=FALSE) + 체포면탈 목적 폭행"을 대입 — 정정10
  이후 구조에서는 Elements가 `commencement_of_execution`(TRUE)만 요구하므로
  성립하고, Completion은 `ATTEMPTED`(taking_conduct=FALSE이므로)로 정확히
  귀결됨을 확인. v1 구조(taking_conduct가 Elements에 직접 있던 상태)로
  대입했다면 이 사건에서 Elements 자체가 실패해 335가 아예 성립하지 않는
  오류가 났을 것 — 정정 전후 차이를 실제로 반례로 검증.
- 338: "강도 기수 + 사망 결과 발생 + 살인 고의 없음(과실 또는 결과적가중범
  귀속만)"을 대입 — v1의 `COMPLETED.when = ALL(death_of_victim, homicide_
  intent)`였다면 이 사건은 `homicide_intent=FALSE`라서 COMPLETED 판정
  자체가 불가능했을 것(강도치사가 아예 존재할 수 없는 오류). v2는
  CompletionPolicy 구체 공식을 확정하지 않고 predicate만 정의했으므로 이
  반례가 2-pass 저작 시 검증 대상으로 남는다(HOLD로 명시적으로 이월했으므로
  "조용히 빠뜨림"이 아님).

---

## 배치⑫ v2 — 최종 확정, 종료

D절(330·331·332)·E절(334)·F절(335, 정정10 반영)·G절(337·338, predicate만 확정
+ CompletionPolicy는 301과 함께 2-pass HOLD)·H절(342·343)·I절(344, population
대상 아님)·J절(356·360, 정정12로 361조 인용 정정)이 확정되었다. 신규 스키마·DSL
primitive 없음(확정, 변경 없음). HOLD/2-pass 확인 목록은 architecture-
compatibility 2건(D-2-1, F-3-1) + 구조 선택 3건(301/337/338 병존 구조 통합,
J-2-1, J-2-2) — v1 대비 337·338 관련 HOLD가 신규 추가되는 대신 기존 301 HOLD에
통합되어 목록 항목 수 자체는 늘지 않는다. 다음은 art339(강도강간, 카드 없음 —
51개 조문 중 유일하게 원본 주석서를 직접 열람해 authoring해야 하는 조문, 다음
세션 시작점).
