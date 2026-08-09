# Predicate 사전 확장 — 배치 ⑦ 각칙 공무원·사법 범죄 (제122·127·129·130·133·136·137·151·152조) v2

[predicate_dictionary_ext_batch07_v1.md](predicate_dictionary_ext_batch07_v1.md)에 대한 사용자
검수 6건(필수 수정 4 + 확인 2) 반영. v1의 정정 1·3·5·6은 그대로 유지, 아래 항목만 바뀐다.

---

## 필수 수정 1 — `ONE_OF` → `ANY`(133①, 130)

**v1 오류**: `ONE_OF`는 정확히 하나만 TRUE여야 하는데, 뇌물공여의 의사표시→약속→실제 공여가
한 사건에서 순차적으로 모두 TRUE가 될 수 있다(교섭 과정에서 의사표시하고, 약속하고, 결국
공여까지 이르는 경우) — 그러면 `ONE_OF`가 위반되어 Elements 자체가 실패해버린다. 세 행위태양은
상호 배타가 보장되지 않으므로 `ANY`가 맞다.

```text
offense.bribery_offering(133①) — ANY(bribe_promise, bribe_giving, bribe_offer_expression...)
    (정확한 최종 형태는 필수 수정 2 참고 — offer_expression이 made/arrived로 다시 갈린다)

third_party_benefit_causation / _demand / _promise (130) — ANY(...)로 결합
    (세 행위태양 사이에 배타성 보장이 없다는 점은 129·130·133 전부 동일 — 이 배치에서
    `ONE_OF`를 쓴 곳은 133① 하나뿐이었지만, 원칙 확인 차원에서 130도 명시)
```

---

## 필수 수정 2 — `bribe_offer_expression`을 made/arrived로 분리(Completion을 위해)

**v1 오류**: canonical_meaning에 "상대방 도달 필요"를 넣어놓고 주석으로만 "미도달은
CompletionPolicy 참고"라고 적었는데, 정작 도달 여부를 가르는 leaf가 없어 Completion이
이 조건을 판정할 방법이 없었다. 행위 predicate 자체가 도달까지 포함하면 완성/미완성을
구별할 수 없다.

```text
ground_fact.bribe_offer_expression_made       공여의 의사표시를 하였다(발신)
ground_fact.bribe_offer_expression_arrived    그 의사표시가 상대방에게 도달하였다

offense.bribery_offering(133①) CompletionPolicy:
    states.completed.when =
        ANY(bribe_promise, bribe_giving,
            ALL(bribe_offer_expression_made, bribe_offer_expression_arrived))
    states.attempted.when =
        ALL(bribe_offer_expression_made, NOT(bribe_offer_expression_arrived))
    states.attempted.punishable = false
```

**필수 수정 1과 결합해 구조가 정리된다**: `bribe_promise`/`bribe_giving`/도달까지 확인된
`bribe_offer_expression`은 CompletionPolicy가 갈라 담당하고, Elements(`job_relatedness`/
`quid_pro_quo`/`official_or_arbitrator_status`)는 state와 무관하게 항상 요구된다 — v1이
"Elements = ALL(..., ONE_OF(행위태양))"로 conduct 판정까지 Elements에 욱여넣었던 것 자체가
6B(Completion이 conduct 갈래를 담당, Elements는 state 불변)의 원칙과 어긋났다. **conduct
alternative는 Elements가 아니라 CompletionPolicy states로 처리한다**가 이번 수정의 핵심.

---

## 필수 수정 3 — `act_for_anothers_benefit_not_self` → 긍정형 predicate + `NOT()`

**v1 오류**: 정정 3(doctrine→legal_element 재분류)을 적용하면서 이름을 부정형으로
지었다 — 배치① 12조 정정("부정형 predicate을 만들지 않는다, `NOT()`이 담당")을 그새
스스로 어겼다.

```text
legal_element.self_benefit_purpose
    (133②) 제3자가 자기 이득을 위하여 청탁이나 중개·알선 명목으로 금품을 수수하였다
    (긍정형)

offense.bribery_delivery(133②) Elements에 NOT(self_benefit_purpose) 포함
```

---

## 필수 수정 4 — 151조 친족특례: Culpability DEFEAT ↔ Punishability EXEMPT 중 하나로 확정

**v1 오류**: `doctrine.relative_cohabiting_family_exemption`을 "Culpability DEFEAT"라고
표에 적어놓고, 바로 아래 설명에서는 "범죄는 완성되나 처벌만 면제된다"고 썼다 — 이 둘은
DSL상 서로 다른 stage다. 후자의 서술("범죄 성립은 유지, 처벌만 면제")이 **Punishability
EXEMPT**의 정의 그 자체이고 Culpability DEFEAT("책임 자체가 조각")와는 양립하지 않는다.

**형법 해석론상으로도 후자가 맞다** — 151조 2항의 친족특례는 통설·판례상 **인적
처벌조각사유**로 분류된다(같은 성격의 328조 친족상도례와 동일 계보). 범죄(구성요건해당성·
위법성·책임)는 그대로 완성되고, 신분관계라는 인적 사정 때문에 국가형벌권 행사만
면제된다 — 이건 9·11·12·16조(배치①, 행위자 자신의 책임 인정 자체가 안 되는 경우)와
질적으로 다른 층이다.

```text
doctrine.relative_cohabiting_family_exemption
    stage = Punishability, effect = EXEMPT   (Culpability DEFEAT 아님 — 확정)
```

---

## 확인 5 — `offender_status_of_object`를 최종 표에서 HOLD/compatibility candidate로 표시

v1 본문(정정 4)은 이미 이걸 cross-actor dependency 확인 대상으로 정확히 짚었지만, "배치⑦
v1 최종 predicate 표"에는 다른 확정 legal_element들과 같은 줄로 나열해뒀다 — 표기상
구분이 안 됐다. v2 최종 표(아래)에서 별도 표시로 수정.

## 확인 6 — `correction_before_examination_end`: GroundFact로 재검토

"신문이 끝나기 전에 허위진술을 철회·시정하였다"는 규범적 포섭 판단이 아니라 **사건·시점에
대한 사실 확인**(그 시점에 그런 진술이 있었는가)에 가깝다 — 총칙 typing 기준("법적 포섭·평가가
들어가면 legal_element")을 다시 적용하면 `ground_fact`가 맞다.

```text
legal_element.correction_before_examination_end  →  ground_fact.correction_before_examination_end
```

---

## 배치⑦ v2 최종 predicate 표 — 이번에 바뀐 항목만(나머지는 v1 표 그대로)

| id | canonical_meaning | 비고 |
|---|---|---|
| `ground_fact.bribe_offer_expression_made` | 공여 의사표시(발신) | 필수 수정 2, `bribe_offer_expression` 대체 |
| `ground_fact.bribe_offer_expression_arrived` | 의사표시 도달 | 필수 수정 2, 신규 |
| `legal_element.self_benefit_purpose` | 자기이득 목적(긍정형) | 필수 수정 3, `act_for_anothers_benefit_not_self` 대체 → Elements에는 `NOT(self_benefit_purpose)`로 결합 |
| `doctrine.relative_cohabiting_family_exemption` | 친족특례, **Punishability EXEMPT**로 확정 | 필수 수정 4 |
| `legal_element.offender_status_of_object` | **HOLD — cross-actor dependency 확인 전까지 확정 legal_element 아님**(정정 4/34조와 같은 목록) | 확인 5 |
| `ground_fact.correction_before_examination_end` | 철회·시정(GroundFact로 재분류) | 확인 6 |

Elements/CompletionPolicy 결합 구조 최종본(133①):

```text
offense.bribery_offering(133①)
    Elements = ALL(job_relatedness, quid_pro_quo, official_or_arbitrator_status)
        -- conduct alternative는 Elements에서 제거(필수 수정 2)
    CompletionPolicy.states.completed.when =
        ANY(bribe_promise, bribe_giving,
            ALL(bribe_offer_expression_made, bribe_offer_expression_arrived))
    CompletionPolicy.states.attempted.when =
        ALL(bribe_offer_expression_made, NOT(bribe_offer_expression_arrived))
    CompletionPolicy.states.attempted.punishable = false

third_party_benefit_causation / _demand / _promise (130) — ANY(...)로 Elements 안에 결합
    (완성/미완성 구별이 카드에 없으므로 133①처럼 CompletionPolicy로 뺄 이유는 없음 — Elements
    안의 ANY로 충분)
```

---

## 이번 배치 v2 요약

신규 스키마·DSL primitive 필요 여부는 v1과 동일하게 **없음**. 이번 수정은 전부 기존
`ANY`/`ALL`/`NOT` 조합과 CompletionPolicy `states.when`/`punishable` 재배치로 해결됐다 —
오히려 필수 수정 2가 "conduct 갈래는 Elements가 아니라 Completion의 일"이라는 6B 원칙을
133①에 처음으로 제대로 적용한 사례가 됐다.

architecture-compatibility 후보는 v1과 동일하게 `offender_status_of_object`
하나(34조와 같은 목록, 2-pass 착수 전 확인)로 유지 — 이번엔 최종 표에도 HOLD로
명시했으니 배치⑦은 이걸로 마감.
