# Predicate 사전 확장 — 배치 ⑦ 각칙 공무원·사법 범죄 (제122·127·129·130·133·136·137·151·152조) v3

[predicate_dictionary_ext_batch07_v2.md](predicate_dictionary_ext_batch07_v2.md)에 대한 사용자
검수 2건 반영. 나머지(ANY 수정, made/arrived 분리, positive self_benefit_purpose,
151 EXEMPT, offender_status HOLD, 철회·시정 GroundFact)는 v2 그대로 확정.

---

## 수정 1 — 133① `attempted.when`이 `completed`와 겹친다(6B exact-one 위반)

**v2 오류**: `bribe_promise=TRUE, bribe_offer_expression_made=TRUE,
bribe_offer_expression_arrived=FALSE`인 사건에서 `completed.when`(`bribe_promise`가
`ANY`의 한 갈래로 TRUE)과 `attempted.when`(`made ∧ NOT(arrived)`)이 동시에 TRUE가 된다 —
6B가 정한 `|T|==1`만 허용 규칙(정의된 state가 둘 다 참이면 `unresolved`) 위반. 의사표시가
도달하지 않았어도 같은 사건에서 약속·공여가 **별도로** 성립했다면 그건 진짜 completed이지
attempted가 아닌데, 지금 `attempted.when`이 그 경우를 걸러내지 못한다.

```text
states.attempted.when =
    ALL(
        bribe_offer_expression_made,
        NOT(bribe_offer_expression_arrived),
        NOT(bribe_promise),
        NOT(bribe_giving)
    )
```

`completed.when`은 v2 그대로 유지 — 겹침은 `attempted`가 `completed`의 여집합이 아니었던
게 원인이므로 `attempted` 쪽만 좁히면 된다.

---

## 수정 2 — "conduct 갈래는 Completion의 일"은 일반원칙이 아니라 133①에 한정된 판단

**v2 오류**: 필수 수정 2 설명을 "conduct alternative는 Elements가 아니라 CompletionPolicy가
담당한다"는 general rule처럼 썼는데, 바로 다음 문단(130의 `third_party_benefit_*`)이
Elements의 `ANY`로 남겨둔 것과 정면으로 모순된다. 두 조문에 다른 처리를 해놓고 한쪽만
원칙인 것처럼 적은 것.

**정확한 기준**:

```text
행위태양별로 completion 시점·punishable 여부가 달라지는 경우
    → CompletionPolicy states로 갈라야 한다(133① — 의사표시는 도달해야 completed,
      미도달이면 attempted+불벌이라는 state별 차이가 있다)

단순 대체적 구성요건 행위이고 모든 갈래의 completion 효과가 동일한 경우
    → Elements의 ANY로 충분하다(130 — 공여하게 함/요구/약속 중 무엇이든 그 자체로
      바로 완성, state별 차이 없음)
```

이건 **133①에 한정된 처리**이지 배치⑦ 전체 원칙이 아니다 — v2 문서의 해당 문장을 이
기준으로 좁혀 읽는다.

---

## 배치⑦ v3 — 최종 확정, 종료

나머지 항목(ANY 수정, `bribe_offer_expression_made`/`_arrived` 분리, `self_benefit_purpose`
긍정형+`NOT()`, 151 친족특례 Punishability EXEMPT, `offender_status_of_object` HOLD,
`correction_before_examination_end` GroundFact 재분류)은 v2 그대로 확정. 배치⑦(122·127·
129·130·133·136·137·151·152조) predicate 사전은 이 v3으로 종료 — 다음은 배치⑧(방화·문서:
164·225·227·231·234·239조).
