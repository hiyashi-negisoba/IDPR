# Predicate 사전 확장 — 배치 ⑫ 절도·강도 나머지 (제330·331·332·334·335·337·338·342·343·344·356·360조) v4

[predicate_dictionary_ext_batch12_v3.md](predicate_dictionary_ext_batch12_v3.md)에 대한
사용자 검수 3건을 반영한다. v3은 그대로 둔다 — 이력 추적용. 정정16은 정정11이 이미
선언한 "predicate만 확정하고 조립은 2-pass로 미룬다"는 원칙을 바로 다음 문단에서
`ANY(...)`로 조립해버려 스스로 어긴 것 — 원칙 선언과 실제 표기가 어긋난 자기모순이었다.

---

## 정정 16 — 337·338의 `ANY(injury_intent, aggravated_result_attribution)`이 이미 301 HOLD를 선결한다, branch별로 완전히 분리한다

**v3 오류**: 정정11에서 "구체 CompletionPolicy 분리는 301과 함께 2-pass로
미룬다"고 선언해놓고, 바로 아래 `elements.requires` 공식에서
`ANY(injury_intent, aggravated_result_attribution)`처럼 두 variant(고의상해/
치상, 살인/치사)를 **하나의 `requires` 트리 안에서 이미 조립**했다. 301 HOLD가
실제로 미루고 있는 건 정확히 "고의형+결과적가중형을 별도 `DerivedOffenseDef`
2개로 할지, 단일 definition 내부 두 갈래(`ANY`)로 할지"이므로, `ANY(...)`를
쓰는 순간 이미 후자(단일 definition 내부 갈래)를 선택해버린 것과 같다 —
"predicate만 확정한다"는 선언과 실제 표기가 자기모순이었다.

**v4(정정) — 공통 predicate와 branch별 predicate를 목록으로만 나열하고,
`ALL`/`ANY`/`NOT`으로 조립하지 않는다.**

### G-1(337) — 조립 없이 나열

**공통(base_offense 위에 얹는 부분, variant 무관)**:
- `legal_element.injury_result`(배치⑨·⑩ 재사용) — 상해의 결과가 발생하였다
- `relation.causal_nexus`(6B·259·301 재사용, elements 밖 별도 obligation, 정정13 유지)
- `relation.occasion_identity`(6B 재사용, elements 밖 별도 obligation, 정정13 유지)

**고의상해 branch**: `legal_element.injury_intent`(배치⑩ 301 신규, 재사용) —
상해의 결과에 대한 고의(base offense 자신의 intent와는 별개)

**치상(결과적가중범) branch**: `primitive.aggravated_result_attribution`
(259·301 재사용) — 결과에 대한 예견가능성과 상당인과관계

두 branch를 `ANY`로 묶을지, 아니면 `occupational_embezzlement`/`occupational_
breach_of_trust`(정정9)처럼 애초에 별도 `DerivedOffenseDef` 2개(예:
`robbery_causing_intentional_injury`/`robbery_causing_injury_by_negligence`류
가칭)로 분리할지는 **여기서 결정하지 않는다** — 301의 기존 HOLD가 이미 이
질문 자체를 담고 있고, 337은 그 질문의 세 번째 사례로 이월될 뿐이다.

### G-2(338) — 조립 없이 나열

**공통**:
- `ground_fact.death_of_victim`(259 재사용) — 피해자가 사망하였다
- `relation.causal_nexus`(6B·259 재사용, elements 밖 별도 obligation)
- `relation.occasion_identity`(6B 재사용, elements 밖 별도 obligation)

**살인 branch**: `legal_element.homicide_intent`(신규) — 사망의 결과에 대한
고의(base offense 자신의 intent와는 별개, 301의 `injury_intent` 분리와 정확히
같은 이유)

**치사(결과적가중범) branch**: `primitive.aggravated_result_attribution`(259
재사용) — 결과에 대한 예견가능성과 상당인과관계

337과 마찬가지로 두 branch의 조립 방식(단일 definition 내부 `ANY` vs 별도
`DerivedOffenseDef` 2개)은 301 HOLD에 네 번째 사례로 이월한다.

**정정13(Elements/Relations 분리)은 그대로 유지** — `causal_nexus`/`occasion_
identity`는 여전히 `elements.requires` 밖의 별도 obligation이다. 이번 정정은
그 위에서 `elements.requires` 자체를 조립하지 않는 것까지 한 단계 더 나아간
것이다.

---

## 정정 17 — HOLD 목록에서 J-2-1/J-2-2는 (B) 순수 구조 선택이 아니라 (A) predicate 재사용 확인이다

**v3 오류**: 갱신된 HOLD 목록에서 J-2-1(`property_of_another` ↔ 366
`object_ownership_other`)·J-2-2(`embezzlement_manifestation` 355/356/360
공유)를 (B) "순수 구조 선택" 항목에 넣었다 — 그러나 이 둘은 "어느 구조를
택할지"의 문제가 아니라 D-2-1·F-3-1과 똑같이 **"같은 이름의 predicate를
재사용해도 되는가"라는 predicate 재사용 확인** 문제다. 분류 라벨이 실제
성격과 어긋났다.

**v4(정정) — 최종 HOLD 목록 재분류**:

```text
(A) predicate/relation 재사용 확인 (2-pass에서 확정, architecture gap 아님)
    - art331 dangerous_weapon_carriage ↔ 배치⑨ 258의2 dangerous_object_carriage
      재사용 여부(D-2-1)
    - art335 occasion_identity("절도의 기회") ↔ 337·338 occasion_identity
      ("강도의 기회") 재사용 여부(F-3-1)
    - art360 property_of_another ↔ 366 object_ownership_other 재사용 여부(J-2-1)
    - art360 embezzlement_manifestation을 355/356/360 세 조문이 공유하는 것의
      확정 여부(J-2-2)

(B) 순수 구조 선택 (스키마는 이미 지원, 2-pass 실제 저작 시 어느 쪽을 택할지만 결정)
    - 301/337/338 — 고의형(강간등상해/강도상해/강도살인)과 결과적가중형(강간등
      치상/강도치상/강도치사)을 별도 DerivedOffenseDef 2개로 할지, 단일
      definition 내부 두 갈래로 할지(정정11·정정16, 337·338이 세 번째·네 번째
      사례로 추가됨)
```

---

## 정정 18 — 360 친족상도례 단락에서 "2-pass 절차 저작" 여지를 남기는 문구를 삭제한다

**v3 오류**: "행위자-소유자 관계가 기준이라는 점은... 2-pass에서 형사소송
절차 저작을 하게 될 경우를 위한 참고 기록일 뿐"이라고 써서, 마치 2-pass에서
형사소송 절차를 저작할 가능성이 아직 열려 있는 것처럼 읽히게 했다 — 그러나
328/344/361은 이미 procedure scope 밖으로 **확정**되었으므로(배치⑪, 이번 배치
I절) 그런 여지 자체를 남길 이유가 없다.

**v4(정정) — J절(360) 친족상도례 단락, 마지막 문장만 교체**:

> **친족상도례 — 360에 대한 328조의 적용은 361조를 통해 이루어진다.** 현행법상
> 소추조건(친고죄)이므로 Rulebase predicate/relation binding은 하지 않는다 —
> 328/344와 마찬가지로 361조도 procedure scope 밖이다. 355(위탁관계 기반)와
> 달리 360은 신분관계 요건 자체가 없어, **행위자-소유자 관계가 기준이라는
> 점은 procedure 관련 참고 authoring memo로만 보존하며, `data/v2/definitions/`
> 에는 적재하지 않는다.**

---

## self-check 체크리스트 재적용 메모 (v4)

2번(doctrine 자격 검사, 이번엔 "조립 자격 검사"로 확장 적용): 정정16 적용 전
"predicate만 확정한다"고 선언한 문단과 그 아래 실제 조립 공식을 대조해보니
불일치가 있었다 — **원칙을 선언한 직후에는 그 선언이 실제로 지켜졌는지 같은
절 안에서 즉시 재확인해야 한다**는 걸 이번 정정에서 얻는다(정정10·11이 겪은
"정정 직후 반례 대입 누락"과 같은 계열의 오류지만, 이번엔 반례가 아니라
자기 원칙과 자기 표기 사이의 정합성 검사가 빠졌다는 점이 다르다).

---

## 배치⑫ v4 — 최종 확정, 종료

D절(330·331·332)·E절(334)·F절(335)·G절(337·338, 정정16으로 branch별 predicate만
나열하고 조립은 301과 함께 2-pass HOLD로 완전히 이월)·H절(342·343)·I절(344,
population 대상 아님)·J절(356·360, 정정18로 최종 문구 정리)이 확정되었다. 신규
스키마·DSL primitive 없음(확정, 변경 없음). HOLD/2-pass 확인 목록: (A) predicate/
relation 재사용 확인 4건(D-2-1, F-3-1, J-2-1, J-2-2) + (B) 순수 구조 선택 1건
(301/337/338 결합범+결과적가중범 병존). 다음은 art339(강도강간, 카드 없음 — 51개
조문 중 유일하게 원본 주석서를 직접 열람해 authoring해야 하는 조문, 다음 세션
시작점).
