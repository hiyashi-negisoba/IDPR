# Predicate 사전 확장 — 배치 ⑨ 생명·신체 (제250·254·255·257·259·263·267·268·258의2조) v2

[predicate_dictionary_ext_batch09_v1.md](predicate_dictionary_ext_batch09_v1.md)에 대한
사용자 검수 1건 반영 — 정정1의 결론(두 층 인과관계 모델, schema addendum 불필요)은
확정, `death_causation`의 재사용 범위만 한 단계 더 좁힌다. 나머지는 v1 그대로.

---

## 정정 10 — `death_causation`을 250·267·268에 그대로 재사용하지 않는다:
`legal_element.result_causation`(신규, death-agnostic) 도입

**v1의 미해결 문제**: 268의 result slot은 `ANY(death_of_victim, injury_result)`인데
causation을 `death_causation`(canonical_meaning이 "사망의 결과가 살해 행위에
인과적으로 귀속된다"로 death 한정) 하나로 두면 치상(injury) 분기의 인과관계를 표현할
방법이 없다. `ANY(death_causation, injury_causation)`처럼 결과별로 별도 causation
predicate를 만드는 대안은 사용자가 지적한 대로 **branch mismatch**를 허용한다 —
`death_of_victim=TRUE`이면서 `injury_causation=TRUE`인 것처럼 slot별 평가만으로는
막히지 않는 잘못된 조합이 통과할 수 있다.

**`death_causation` 자체 재확인 — 정의를 고칠지 새로 만들지 판정.** fixture
canonical_meaning("사망의 결과가 **살해 행위**에 인과적으로 귀속된다")은 이미
"사망"·"살해 행위"로 한정돼 있어 generic이 아니다 — 사용자가 세운 판정 기준
("실제로 death에 한정돼 있다 → 수정하지 말고 신규 정의")을 그대로 적용하면 답은
**신규 정의**다(canonical_meaning 불변 원칙, `death_causation`은 그대로 둔다).

**v2(수정)**:

```text
legal_element.result_causation (신규)
    해당 행위와 그 offense가 요구하는 구성요건적 결과 사이에 법적으로 요구되는
    인과관계(상당인과관계)가 인정된다

250  result = death_of_victim              causation = result_causation
267  result = death_of_victim              causation = result_causation
268  result = ANY(death_of_victim,
                   injury_result)          causation = result_causation
```

**250도 `death_causation`이 아니라 `result_causation`을 쓴다** — 사용자 예시가
명시한 그대로. `result_causation` 하나가 "행위→그 offense의 결과" 판단을 모두
담당하므로, 268처럼 result가 `ANY`로 분기해도 causation은 분기하지 않고 그 판단
하나가 어느 쪽 result에도 적용된다(잘못된 branch 조합 자체가 애초에 생기지 않는다 —
causation predicate가 result별로 나뉘어 있지 않으므로 "무엇의 원인인지"를 slot 조합이
아니라 판정 시점의 사실관계가 자연히 결정한다).

`legal_element.death_causation`(fixture)은 정의를 그대로 둔다 — 삭제하지 않지만
250/267/268의 predicate 사전에서는 더 이상 참조하지 않는다. 실사용 여부(다른 곳에서
"살해행위→사망"만을 좁게 가리켜야 하는 자리가 나오면 그때 재사용)는 2패스 이후 확인.

**259는 영향 없음** — COMPOSE의 `relation.causal_nexus`는 base(injury)·가중결과(death)
사이의 관계이지 offense 내부 causation slot이 아니므로 이번 정정과 무관, v1 그대로.

---

## 정정 1 확정 — schema addendum 없음, 두 층 인과관계 모델 그대로

v1이 스키마에서 확인한 사실(`offense_def.schema.json`에 `relations` 필드 없음,
`derived_offense_def.schema.json`의 `derivation`에만 존재)과 그로부터 도출한 두 층
구조가 **사용자 확인으로 확정**됐다:

```text
base OffenseDef 내부 conduct→result   →  elements.causation의 LegalElement
                                         (250/267/268 = result_causation, 위 정정10)
COMPOSE된 DerivedOffenseDef 컴포넌트 간  →  RelationDef(relation.causal_nexus)
                                         (259 = base offense.injury ↔ 가중결과 death)
```

`OffenseDef.relations` 신설 같은 스키마 확장은 고려하지 않는다 — 지금 스키마가 이미
표현하는 모델을 그대로 쓰는 것이 맞다는 게 사용자의 명시적 판단.

---

## 배치⑨ v2 요약

인과관계 이층 모델(base offense=LegalElement / COMPOSE=RelationDef)은 v1대로 확정,
스키마 변경 없음도 확정. `death_causation`의 재사용 범위만 좁혀 250·267·268이
`legal_element.result_causation`(신규, death-agnostic)을 공유하도록 정정했다 —
`death_causation` 자체 정의는 손대지 않는다(canonical_meaning 불변 원칙). 나머지
정정 2-9(v1)는 그대로 유지. 신규 스키마·DSL primitive는 여전히 없음 — `result_
causation`도 기존 `LegalElementDef` 형태 안에서 표현된다.
