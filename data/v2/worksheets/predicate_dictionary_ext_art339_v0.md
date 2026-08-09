# Predicate 사전 확장 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외) v0

배치⑦-⑫는 워크시트(`data/v2/worksheets/각칙/{article}.md`)를 1차 재료로 썼으나, 339조는
카드 자체가 없다(워크시트 스크립트 대상 아님). 원본 형법 주석서(`law_id=001692`,
`comm_001692_제339조_*`, 9개 chunk — Ⅰ.개설/Ⅱ.주체/Ⅲ.1·2(강간의 의미·기회)/
Ⅳ.상해치사상/Ⅴ.미수범/Ⅵ.공범/Ⅶ.1·2(특별법))를 직접 열람해 authoring한다.

**착수 전 확인한 사실 — 스키마 fixture가 이미 이 조문을 겨냥하고 있었다.**
`docs/contracts/v2/examples/derived_offenses.yaml`(`derived_offense.robbery_rape`,
2026-08-08 addition, section 20.4)과 `completion_policies.yaml`의
`completion_policy.robbery_homicide`(같은 COMPOSE 계열의 자매 fixture, 338조)가
"두 개의 완전한 독립 OffenseDef(강도·강간)를 causal_nexus가 아니라
`relation.occasion_identity`(conduct-conduct 결합)로 묶는" 구조를 스키마 검증용으로
이미 실증해두었다 — 이번 배치가 그 구조를 실제 predicate id로 채우는 첫 사례다.
**fixture의 predicate id(`ground_fact.forcible_intercourse`,
`ground_fact.attempt_commencement` 등)는 스키마 검증용 placeholder일 뿐, 배치⑨가
이미 확정한 원칙("fixture predicate 이름을 real typing 근거로 그대로 쓰지 않는다")에
따라 아래에서는 배치⑩·G절이 실제로 확정한 predicate id로 전부 교체한다.**

---

## 구조 판단 — COMPOSE(강도 base_offense 전체 + 297 강간 base_offense 전체), 신규 아님

원문 Ⅰ이 정면으로 "강도죄와 강간죄의 결합범"이라고 확정한다. G절(337·338)이 이미
"base offense(강도) + 결과(상해/사망) ground_fact"를 COMPOSE로 확정했지만, 339는
결과 하나가 아니라 **또 다른 완전한 base offense(297 강간)의 element 세트 전체**가
붙는다는 점이 다르다 — 그러나 `DerivedOffenseDef.derivation.kind: compose`는 이미
`components`에 `{kind: offense, ref: ...}`를 두 개 넣는 것을 fixture 수준에서
지원하고 있으므로(위 확인), 이건 새 스키마 능력이 아니라 **기존 COMPOSE 메커니즘을
"완전한 두 offense를 결합하는" 방식으로 사용하는 것뿐**이다(self-check3, "predicate
재사용 가능성을 없는 schema typing 문제로 격상하지 않는다"의 반대 방향 적용 — 여기서는
실제로 격상할 이유가 없다는 걸 fixture로 직접 확인).

`relation.causal_nexus`는 쓰지 않는다 — 강간행위는 강도의 "결과"가 아니라 강도와
병렬적인 별개의 행위(conduct)이므로, G절의 causal_nexus(event-event, "결과가
발생하였다")가 아니라 fixture가 명시하는 대로 **conduct-conduct 결합**
(`left_view: conduct, right_view: conduct`)인 `relation.occasion_identity` 하나만
필요하다. 이 점에서 339는 G(337·338)보다 F(335, occasion_identity만 쓰고 causal_
nexus는 안 씀)에 구조적으로 더 가깝다.

---

## A. 주체 — G-1과 동일 패턴, 신규 predicate 없음

| 근거 | 처리 |
|---|---|
| 원문 Ⅱ: "강도강간죄의 주체는 강도인바... 단순강도죄, 특수강도죄, 준강도죄, 약취강도죄의 강도가 모두 여기에 포함됨은 물론이다." | `base_offense = ANY(333 강도, 334 특수강도, 335 준강도, 336 인질강도)` — G-1(337조 주체)의 base_offense 목록과 **완전히 동일**. 336조(인질강도)는 51개 조문 워크시트 범위 밖이라 population 대상은 아니나, 339의 "강도" 개념이 336까지 포함한다는 사실은 G-1과 같은 이유로 authoring 메모로만 남긴다(배치⑪ 확정 원칙 재적용). |
| 원문 Ⅱ: "강도의 실행행위에 착수한 후임을 요하고 예비·음모의 단계에 그친 자는 이에 해당하지 않으나, 일단 강도에 착수한 이상 그 기수·미수를 불문한다." | base_offense.requires에 이미 내장된 `legal_element.commencement_of_execution`(강도) 이상 요구 구조가 이 배제를 그대로 표현 — G-1과 동일, 별도 predicate 불필요 |
| 원문 Ⅱ 후단: 강간범이 간음행위 종료 후 재물탈취의 범의가 생겨 소지품을 강취한 경우 → 강도강간죄 아니고 강간죄·강도죄의 실체적 경합 | 339 Elements가 성립하지 않는 경계 사례 — 아래 C절에서 occasion_identity의 방향성으로 자연히 배제됨을 확인 |

339조 자체의 신분범적 성격("강도강간죄는 일종의 신분범")은 base_offense.requires를
그대로 요구하는 구조 자체가 이미 표현하므로, D-3(상습절도 부진정신분범)식 별도
QUALIFY도 필요 없다 — G-1의 주체 처리와 정확히 같다.

---

## B. 강간 요소 — 297(배치⑩)의 확정 predicate 세트를 그대로 재사용, 신규 없음

| id (배치⑩ 확정, 재사용) | 근거 원문 |
|---|---|
| `legal_element.natural_person_victim_status` | 원문에 명시 언급 없으나 297 재사용 시 자동 포함(자연인·타인, 정의 불변) |
| `legal_element.coercive_conduct` | art339_Ⅲ.1("강간의 의미는 강간죄에서와 같다") |
| `legal_element.directness_of_coercion_by_offender` | art339_Ⅱ("주체는 강도") — 339의 주체 자체가 강도이므로 이 predicate는 구조적으로 자동 충족되는 방향이나, canonical_meaning을 재정의하지 않고 그대로 재사용(불변성 원칙) |
| `legal_element.coercion_sufficiency_for_rape` | art339_Ⅲ.1 |
| `ground_fact.vaginal_intercourse_conduct` | art339_Ⅲ.1 |
| `legal_element.coercion_induced_sexual_act_causation` | art339_Ⅲ.1, Ⅲ.2 |
| `legal_element.intent`(13조 재사용, 강간의 고의) | art339_Ⅵ("특히 강간에 대한 고의가 있어야") |

**"강도의 폭행·협박을 그대로 이용하는 경우"도 새 predicate 없이 흡수된다.**
art339_Ⅲ.1이 "강도 과정에서 이루어진 폭행·협박으로 야기된 항거불능 상태를
이용하여 간음행위를 하는 경우... 도 당연히 포함된다"고 명시하는데,
`coercive_conduct`/`coercion_induced_sexual_act_causation`의 canonical_meaning
(배치⑩ 확정)은 애초에 "별도의" 폭행·협박일 것을 요구하지 않는다 — 강도의 폭행·협박과
동일한 사실관계 인스턴스가 두 predicate(base_offense의 `robbery_level_violence`와
339의 `coercive_conduct`)를 동시에 충족시켜도 무방하다(같은 conduct가 서로 다른
offense의 서로 다른 leaf를 동시에 충족하는 것은 이 DSL에서 이미 정상 동작 — G절이
강도 자체를 base_offense로 재사용할 때와 같은 논리).

**유사강간(297조의2)·준강간(299)은 population하지 않는다.**
- art339_Ⅲ.1: 유사강간 포함 여부는 "긍정설·부정설 대립"하나 "부정적으로 해석함이
  타당" — 297조의2 자체가 51개 조문 워크시트 범위 밖이라(형법전 내부 조문이지만
  워크시트 대상이 아님) population하지 않는 게 애초에 맞고, 학설도 부정설이 우세하므로
  339의 conduct는 `vaginal_intercourse_conduct`(297) 하나로 확정한다.
- art339_Ⅲ.1: 299(준강간)의 "간음"이 별도로 포함되는지는 "논의의 실익이 커 보이지
  않는다"고 원문이 직접 정리한다 — 항거불능 상태를 이용한 간음이 이미 위 문단에서
  `coercion_induced_sexual_act_causation`으로 흡수되므로, 299의 독자 predicate
  (`mental_incapacity_or_physical_helplessness_status`/`exploitation_of_incapacity`,
  배치⑩ 확정)를 별도로 끌어올 필요가 없다.

---

## C. 강도의 기회 — `relation.occasion_identity`(G 재사용), 신규 HOLD 아님

| id | canonical_meaning | 근거 |
|---|---|---|
| `relation.occasion_identity`(6B 재사용, G-1/G-2와 동일 정의) | 결과/행위가 base offense(강도)의 "기회"에 발생·행하여졌다 | art339_Ⅲ.2 |

**F-3-1 HOLD와는 무관 — 오히려 F-3-1의 반대쪽 절반을 강화 확인한다.** 배치⑫ HOLD
목록의 F-3-1은 335조 "**절도**의 기회"가 G의 "**강도**의 기회"와 canonical_meaning을
공유하는지 확인이 필요하다는 것이었다. 339조 원문은 문언 자체가 "**강도**의 기회"
(art339_Ⅲ.2, "강간행위는 강도의 기회에 행하여짐을 요한다")이므로 G-1/G-2와 **정확히
동일한 표현**을 쓴다 — 파라미터화 여부를 검토할 필요 없이 그대로 재사용 확정. F-3-1은
335 쪽(절도의 기회)만 남은 채로 유지, 339는 새 HOLD를 만들지 않는다.

**원문이 나열한 5개 유형(ⅰ~ⅴ) 중 ⅴ만 배제되는 이유 — 새 predicate·게이팅 불필요.**
ⅰ)강도의 폭행·협박 자체로 강간, ⅱ)강도 착수 후 미완료 상태에서 강간, ⅲ)강도 완료 후
강간, ⅳ)강간 계속 중 강도 → 전부 occasion_identity 성립. ⅴ)강간을 완료한 후 새로운
범의로 강도 → occasion_identity 불성립("이미 종료된 후 새로운 강도의 범의"). 이 배제는
F-2(335 `purpose_to_resist_recapture`)가 "배타적 지배 확립"을 predicate 자체에
내장해 별도 `NOT()` 게이팅 없이 경계를 표현한 것과 같은 방식으로, occasion_identity의
기존 legal_standard(시간적·장소적 밀접성 — F-3에서 이미 "안전하게 도피하여 더는 추적·
체포위협을 느끼지 않을 정도로 경과했다면 인정되지 않는다"로 확정)가 **애초에 이미
방향성을 내포**한다 — ⅴ)은 강간 시점에 base offense(강도)가 아직 존재하지 않으므로
"강도의 기회"라는 관계 자체가 성립할 수 없다. 새 predicate나 HOLD를 만들 필요가
없다(self-check2, 다른 predicate가 이미 결론을 구조적으로 만들어낸다).

원문 Ⅱ 후단(강간 후 재물탈취 범의 → 강간죄·강도죄 실체적 경합)도 같은 이유로
배제된다 — 이 경우는 애초에 강도(base_offense)가 강간보다 늦게 성립하므로
occasion_identity 판단 이전에 339 자체가 구성되지 않는다.

---

## D. CompletionPolicy — fixture `completion_policy.robbery_homicide` 패턴 그대로, id만 교체

원문 Ⅴ가 정면으로 확정한다: "강도강간죄의 미수는 강도행위의 미수를 의미하는 것이
아니라 강간행위의 미수를 말한다... 강도가 기수라도 강간이 미수이면 강도강간죄의
미수이며, 이와 반대로 강도가 미수라도 강간이 기수이면 강도강간죄의 기수이다." 이건
G-1/G-2("상해/사망의 결과 발생 여부가 결정, 재물탈취 완료 여부 무관")와 **동형 패턴**
— "첨부된 컴포넌트의 완성 여부가 결정, base offense는 착수만 있으면 충분"이라는
구조를 강간(297) 쪽에 적용한 것뿐이다. `completion_policies.yaml`의
`completion_policy.robbery_homicide`(338조 fixture)가 이 정확한 구조를 이미 스키마
수준에서 검증해두었으므로, predicate id만 실제 확정본으로 교체해 그대로 옮긴다.

```text
robbery_rape.COMPLETED.when = coercion_induced_sexual_act_causation
    (즉 강간행위가 기수에 이름 — 강도의 기수·미수 무관)

robbery_rape.ATTEMPTED.when = ALL(
    legal_element.commencement_of_execution (강간행위 착수, 25조 재사용),
    NOT(coercion_induced_sexual_act_causation)
)
robbery_rape.ATTEMPTED.punishable = true (원문 Ⅴ, 342조 재사용 — G-1의 결과적가중범
    branch와 달리 339는 결과적가중범이 아니라 고의범 결합범 단일 구조이므로
    punishable=false 예외가 없다)
robbery_rape.ATTEMPTED.suspends = [rape_part의 result/causation에 해당하는 slot]
robbery_rape.ATTEMPTED.relations = [
    {relation: occasion_identity, left: robbery_part, right: rape_part,
     disposition: RETAIN}
    (강도의 기회에 강간행위가 이루어졌을 것은 미수에서도 그대로 요구됨 — fixture
     주석이 338조에 대해 남긴 설명과 동일 근거)
]
```

339는 F-6(335, base offense 종류에 따라 333/334조 중 처단형 선택)식 분기가
**필요 없다** — 339 자체가 무기 또는 10년 이상의 징역이라는 독자 법정형을 가지므로,
base가 어느 강도 유형이든 339의 법정형은 변하지 않는다(F와의 대비점으로 명시).

---

## E. 상해·살해와의 관계 — 339 내부 아님, occurrence-level 상상적·실체적 경합

원문 Ⅳ가 정면으로 확정: 강도가 상해·살해의 **고의**를 가지고 강간하여 상해·살인한 때는
"강도강간죄와 강도상해죄 또는 강도살인죄와의 **상상적 경합**", 고의 없는 **결과적
가중범**(치상·치사)의 경우도 "강도강간죄와 강도치상죄" 또는 "강도강간죄와
강도치사죄"의 **상상적 경합**, 강간 후 비로소 상해·살해의 고의가 생겨 상해·살인한
경우는 "강도강간죄와 강도상해죄 또는 강도살인죄의 **실체적 경합**"이다.

**G절(337·338)과 근본적으로 다른 지점 — 339는 결과적가중범 branch를 아예 갖지 않는다.**
개설(원문 Ⅰ)이 명시: "현행 형법은 구 형법과 달리 강도강간치사죄에 관한 규정을 두고
있지 않다." 337·338은 상해/사망을 자기 Elements 내부의 branch(정정16, 조립은
2-pass로 이월했지만 predicate 자체는 337·338 소속)로 가졌지만, 339는 상해·사망
결과가 발생해도 그건 **별도의 offense(337 또는 338)이고 339와는 occurrence 단위에서
상상적/실체적 경합으로만 연결**된다 — predicate 사전 population 대상이 아니다(9조
검수2 patttern, occurrence/죄수 판단은 범위 밖). 이 구분(339 Elements 자체에는
상해·사망 predicate가 없음)을 명시적으로 남긴다 — G절 패턴을 기계적으로 따라가 339에도
결과적가중범 branch를 만드는 오류를 방지하기 위한 authoring 메모.

특별법(성폭력처벌법 제9조, 강간등살인·치사)이 별도로 강도강간살인·치사를 규정하지만
이건 형법전 밖 — 범위 밖(아래 G절).

---

## F. 공범 — 기존 원칙 재적용, 신규 없음

원문 Ⅵ: "강간에 대한 고의가 있어야 하므로... 공동가공의 의사가 없는 다른 공범자는
강도강간죄의 공범으로서의 죄책을 지지 않는다." 배치⑨ 250·배치⑫ G-2가 이미 확정한
"ATTRIBUTE는 conduct 전용, intent는 각자 자기 CaseTruths로 개별 평가" 원칙의 재적용
— 새 predicate 불필요. 판례 두 사례(갑이 협박하며 강간 의사 표명 + 을이 실행 / 신고를
막기 위해 감시만 한 공범)는 모두 "강간에 대한 공동가공의 의사"가 명시적 의사표명이나
묵시적 의사연락으로 인정되는지의 사실판단 문제 — `legal_element.intent`(339, 강간의
고의)를 30조 공동정범 법리로 개별 평가할 때의 증거 판단 기준일 뿐, predicate 층의
새 구조가 아니다.

---

## G. 범위 밖(predicate 아님)

- **유사강간(297조의2)** — B절에서 이미 제외 확정.
- **특수강도강간·강간등살인·치사(성폭력처벌법 §3②·§9①·§15)** — 형법전 밖 특별법
  가중(art339_Ⅶ.1). 법정형이 사형/무기징역까지 올라가는 가중 유형이나 형법 339조
  자체의 구성요건이 아니다(배치⑨ "특정강력범죄 가중은 특별법" 원칙 재적용).
- **특정범죄가중처벌법 §5의5(재범자 가중)·특정강력범죄처벌법 §3(누범가중)**
  (art339_Ⅶ.2) — 35조 누범(배치⑥ 확정)의 특별법 가중판. 36조와 마찬가지로 절차·양형
  계산 사항, predicate 사전 population 대상 아님.

---

## 이번 배치 신규 스키마·predicate 필요 여부 — **둘 다 없음(최초 사례)**

배치⑦-⑫는 매 배치 최소 1개 이상의 신규 predicate id를 만들어왔다. **339는 신규
predicate id가 0건이다** — base_offense 세트(G-1 재사용), 강간 element 세트(배치⑩
재사용), occasion_identity relation(G 재사용), CompletionPolicy 구조(G-1/G-2 재사용
패턴)까지 전부 이미 확정된 조각의 순수 조립으로 충분했다. 카드 없이 원문만으로
authoring해야 하는 유일한 조문이 오히려 predicate-first 방법론이 "카드가 하는 일"을
"이미 확정된 predicate 사전 자체가 대신할 수 있는가"를 시험하는 사례가 됐고, 결과는
긍정 — 스키마 fixture(`derived_offense.robbery_rape`)가 이 조립 가능성을 미리
검증해뒀다는 사실이 이 결론의 근거를 하나 더 보탠다.

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입)

- **positive-predicate + NOT() 원칙**: 새 predicate가 없어 해당 없음.
- **canonical_meaning 불변성**: B절에서 297 predicate 7개를 전부 그대로 재사용,
  재정의 없음(directness_of_coercion_by_offender가 339 주체 구조상 자동 충족되는
  방향이라는 언급도 canonical_meaning 자체는 건드리지 않았음을 재확인).
- **fixture predicate 이름을 real typing 근거로 쓰지 않는다**: 위 "착수 전 확인한
  사실" 절에서 `ground_fact.forcible_intercourse`/`ground_fact.attempt_commencement`
  등 fixture 고유 이름을 배치⑩·25조 확정 이름으로 전량 교체 완료.
- **HOLD와 source-resolution 구분**: 이번 배치에 새 HOLD 없음 — C절에서 F-3-1을
  재확인했을 뿐 새로 만들지 않았고, E절의 상해·살해 경합도 기존 33조 죄수/경합 원칙
  범위 안(범위 밖으로 명확히 분류, HOLD 아님).
- **schema typing 과잉확장 금지**: "두 완전한 offense를 COMPOSE"가 새 스키마 문제로
  보일 수 있었으나 fixture로 이미 지원 확인 — 격상하지 않음.
- **구조적으로 이미 커버된 결론은 doctrine 재생성 금지**: 유형 ⅴ 배제·강간후재물취거
  배제 모두 occasion_identity의 기존 legal_standard가 이미 만들어내는 결론 —
  별도 doctrine·exclusion predicate 만들지 않음.
- **cross-offense transition 서술 금지**: E절에서 "그러므로 337/338이 성립한다"는
  표현 대신 "별도 offense이고 occurrence 단위에서 경합 관계로 연결"로 서술.
- **ATTRIBUTE는 conduct 전용, mental state는 actor-specific**: F절에서 재확인.

---

## 최종 확정 predicate (v0)

339 = COMPOSE(`base_offense`=ANY(333/334/335, +336 참조), `rape_part`=297의 7개
predicate 전량 재사용) + `relations = [occasion_identity]`(G 재사용, "강도의 기회").
**신규 predicate 0건, 신규 스키마 0건, 신규 HOLD 0건** — 배치⑦-⑫ 전체를 통틀어 가장
낮은 신규성이며, 이는 카드 없는 예외 조문이 오히려 predicate 사전의 재사용 밀도를
검증하는 사례가 됐다는 뜻으로 해석한다.

art339가 끝나면 각칙 51개 조문 + art339 전체가 완료되고, predicate 사전 전체(각칙 +
총칙 34개 조문)에 대한 최종 통합 검수 게이트로 넘어간다(CURRENT.md 기존 계획대로).
