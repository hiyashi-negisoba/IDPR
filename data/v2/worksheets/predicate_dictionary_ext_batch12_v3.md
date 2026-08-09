# Predicate 사전 확장 — 배치 ⑫ 절도·강도 나머지 (제330·331·332·334·335·337·338·342·343·344·356·360조) v3

[predicate_dictionary_ext_batch12_v2.md](predicate_dictionary_ext_batch12_v2.md)에 대한
사용자 검수 3건을 반영한다. v2는 그대로 둔다 — 이력 추적용. 정정13은 배치⑨·⑩이 이미
확정해둔 층위 구분(Elements=`ElementExpression`은 `GroundFact`/`LegalElement` leaf만,
`RelationDef`는 별도 obligation)을 335·337·338에서 다시 어긴 것 — 신규 원칙이 아니라
같은 drift의 재발.

---

## 정정 13 — `relation.causal_nexus`/`relation.occasion_identity`를 Elements.requires 안에 넣으면 안 된다

**v2 오류**: 335·337·338 모두 `requires = ALL(..., occasion_identity)` /
`ALL(..., causal_nexus, occasion_identity)`처럼 `RelationDef`(occasion_identity·
causal_nexus)를 `GroundFact`/`LegalElement` leaf와 같은 `ElementExpression`
트리 안에 섞었다. 배치⑨(259)·배치⑩(301)이 이미 "`relation.causal_nexus`와
`relation.occasion_identity`를 하나로 합치면 안 된다"는 정정에서 확정해둔 건
사실 더 근본적인 구분이었다 — **Relation은 `Elements`(ElementExpression) 층이
아니라 `DerivedOffenseDef`의 별도 obligation**이라는 것. `ElementExpression`의
leaf는 `GroundFactDef`/`LegalElementDef`만이고, `RelationDef`는 그 트리 밖에서
독립적으로 평가되는 구조적 관계 obligation이다 — 이번 배치에서 이 경계를 다시
어겼다.

**v3(정정) — Elements와 Relations를 분리한다.**

### F(335) 재정정

```text
335.elements.requires = ALL(
    commencement_of_execution,
    ANY(
        ALL(taking_conduct, purpose_to_resist_recapture),
        purpose_to_avoid_arrest,
        purpose_to_conceal_evidence
    ),
    robbery_level_violence
)
335.relations = [occasion_identity]

335.COMPLETED.when = taking_conduct
335.ATTEMPTED.when = ALL(commencement_of_execution, NOT(taking_conduct))
```

(정정10의 Elements/Completion 분리 결론 자체는 그대로 유지 — 이번 정정은
`occasion_identity`를 `elements.requires`에서 `relations`로 옮기는 것만
추가한다.)

### G-1(337) 재정정

```text
337.elements.requires = ALL(
    base_offense.requires,
    injury_result,
    ANY(injury_intent, aggravated_result_attribution)
)
337.relations = [causal_nexus, occasion_identity]
```

### G-2(338) 재정정

```text
338.elements.requires = ALL(
    base_offense.requires,
    death_of_victim,
    ANY(homicide_intent, aggravated_result_attribution)
)
338.relations = [causal_nexus, occasion_identity]
```

**이건 새 구조가 아니라 Step 5/6B가 이미 확정해둔 relation-first 계약으로
복귀하는 것뿐이다** — predicate 정의(injury_result/injury_intent/death_of_
victim/homicide_intent/aggravated_result_attribution/causal_nexus/occasion_
identity)와 CompletionPolicy를 301과 함께 2-pass로 미룬다는 정정11의 결론은
그대로 유지, 이번엔 그 predicate들을 `elements`/`relations` 어느 필드에
배치하는지만 바로잡는다.

---

## 정정 14 — 360조 친족상도례 서술에서 "행위자-소유자 바인딩"은 삭제, 배치 안 한다는 사실만 남긴다

**v2 오류**: 정정12에서 361조 인용은 바로잡았지만 "준용되는 328조 상당 판단을
'행위자-소유자' 쌍방향으로만 바인딩한다"는 표현이 남아있었다 — 그런데 328조
(및 그걸 준용하는 344·361조) 자신이 이미 procedure scope 밖(소추조건, 배치⑪
확정)으로 재분류되어 있으므로, **애초에 Rulebase 층위에서 바인딩할 predicate나
relation 자체가 없다.** "쌍방향으로 바인딩한다"는 표현은 마치 실제로 바인딩
대상이 되는 predicate/relation이 존재하는 것처럼 읽혀 I절의 procedure-scope
원칙과 충돌한다.

**v3(정정) — J절(360) 친족상도례 단락, 다시 작성**:

> **친족상도례 — 360에 대한 328조의 적용은 361조를 통해 이루어진다.** 현행법상
> 소추조건(친고죄)이므로 Rulebase predicate/relation binding은 하지 않는다 —
> 328/344와 마찬가지로 361조도 procedure scope 밖이다. 355(위탁관계 기반)와
> 달리 360은 신분관계 요건 자체가 없어 "행위자-소유자 관계가 기준"이라는
> 점은 실체법 predicate가 아니라 **procedure authoring memo**로만 남긴다
> (2-pass에서 형사소송 절차 저작을 하게 될 경우를 위한 참고 기록일 뿐, 이
> predicate 사전이나 `data/v2/definitions/`의 대상이 아니다).

---

## 정정 15 — 최종 요약의 "architecture-compatibility 2건"이라는 표현이 과대평가다

**v2 오류**: D-2-1(dangerous_weapon_carriage 재사용)·F-3-1(occasion_identity
재사용)을 "architecture-compatibility 2건"으로 불렀다 — 그러나 이 둘은 기존
DSL 메커니즘이 이 조합을 실제로 지원하는지 코드 수준에서 확인해야 하는 33조
단서·34조류의 **진짜 gap**이 아니라, "같은 이름의 predicate를 다른 조문에서
재사용해도 되는가"라는 **2-pass 저작 시 확인**에 불과하다(배치⑧이 이미
"재사용 가능성을 없는 schema typing 문제로 격상하지 않는다"고 확정한 것과
같은 성격) — 배치⑪ v3이 "HOLD/architecture-compatibility"라는 하나의 이름
아래 성격이 다른 항목을 섞지 않도록 (A)architecture-compatibility/(B)순수
구조·학설 선택으로 이미 분리해뒀는데, 이번 배치 요약에서 그 구분을 다시
흐렸다.

**v3(정정) — 최종 요약 표현 수정**: "architecture-compatibility 2건(D-2-1,
F-3-1)" → **"predicate/relation 재사용 확인 2건(D-2-1, F-3-1) — 2-pass에서
확정, architecture gap 아님"**으로 바꾼다. HOLD 종합 목록 자체의 항목·내용은
변경 없음(명칭만 정정, 배치⑪ v3과 동일한 종류의 교정).

---

## 갱신된 HOLD / 2-pass 확인 목록 (v3 최종, 명칭만 정정)

```text
(A) predicate/relation 재사용 확인 (2-pass에서 확정, architecture gap 아님)
    - art331 dangerous_weapon_carriage ↔ 배치⑨ 258의2 dangerous_object_carriage
      재사용 여부(D-2-1)
    - art335 occasion_identity("절도의 기회") ↔ 337·338 occasion_identity
      ("강도의 기회") 재사용 여부(F-3-1)

(B) 순수 구조 선택 (스키마는 이미 지원, 2-pass 실제 저작 시 어느 쪽을 택할지만 결정)
    - 301조 결합범+결과적가중범 병존 구조에 337·338을 동일 유형 사례로 추가
      (정정11, 신규 항목 아님)
    - art360 property_of_another ↔ 366 object_ownership_other 재사용 여부(J-2-1)
    - art360 embezzlement_manifestation을 355/356/360 세 조문이 공유하는 것의
      확정 여부(J-2-2)
```

**architecture-compatibility(33조 단서, 34조, 151조 offender_status_of_object,
263조 특례, 257·298조 자상·도구 간접정범, 250조 비신분자 존속살해 가담, art323
소유자 아닌 자의 가담↔33조 본문 공동정범)는 배치⑤-⑪에서 이월된 기존 항목
그대로 — 이번 배치는 이 범주에 아무것도 추가하지 않는다**(정정15로 명확히
확인).

---

## self-check 체크리스트 재적용 메모 (v3)

7번(stage 라벨-설명 일치)을 이번에 다시 적용했다: `relation.causal_nexus`/
`relation.occasion_identity`가 "Elements의 legal_element처럼 보이지만 실은
RelationDef obligation"이라는 층위 자체가 라벨(`relation.*` 접두)과 실제 배치
위치가 어긋나 있었다는 걸 정정13에서 재확인 — predicate id의 네임스페이스
접두(`relation.`)가 이미 층위를 명시하고 있었는데도 문서 본문에서
`elements.requires`에 섞어 쓴 건 라벨을 무시한 배치 오류였다.

---

## 배치⑫ v3 — 최종 확정, 종료

D절(330·331·332)·E절(334)·F절(335, 정정13으로 Elements/Relations 분리 완료)·
G절(337·338, 정정13으로 Elements/Relations 분리 완료 + CompletionPolicy는 301과
함께 2-pass HOLD)·H절(342·343)·I절(344, population 대상 아님)·J절(356·360,
정정14로 친족상도례 서술 수정)이 확정되었다. 신규 스키마·DSL primitive 없음
(확정, 변경 없음). HOLD/2-pass 확인 목록은 (A) predicate/relation 재사용 확인
2건 + (B) 순수 구조 선택 3건 — 명칭만 정정, 항목·내용은 v2와 동일. 다음은
art339(강도강간, 카드 없음 — 51개 조문 중 유일하게 원본 주석서를 직접 열람해
authoring해야 하는 조문, 다음 세션 시작점).
