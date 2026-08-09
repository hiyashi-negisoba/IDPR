# Predicate 사전 확장 — 배치 ② 총칙 고의·과실·사실의착오·인과관계·부작위·동시범 (제13·14·15·17·18·19조) v2

[predicate_dictionary_ext_batch02_v1.md](predicate_dictionary_ext_batch02_v1.md)에 대한 사용자
검수 3건 반영. v1은 그대로 둔다. 13·14·17조는 v1 그대로(변경 없음), 15·18·19조가 바뀐다.

---

## 정정 1 — 제15조: `mistake_bundle`을 확정하지 않는다, 부착 대상도 정정

**v1 오류 1 — 부착 대상 오기술**: "`intent`(13조)의 element_modules에 붙여"라고 썼는데,
`element_modules`는 `LegalElementDef`가 아니라 **`OffenseDef`**에 붙고, `placement`로
그 offense의 slot(이 경우 `mental`)에 기여분을 매핑하는 구조다(`SCHEMA_NOTES.md`의
COMPOSE bundle-placement 메커니즘). 정확히는:

```text
OffenseDef.element_modules:
  - ref: bundle.mistake_bundle
    placement:
      (mistake_bundle의 leaf-ref) → mental slot
```

**v1 오류 2 — 결론을 앞서갔다.** `bundle.mistake_bundle`을 "2패스에서 (a)로 확정할 것을
제안"까지 썼는데, 이건 검증 안 된 가정을 확정처럼 적은 것이다. 현재 `ElementBundleDef`는
"여러 leaf predicate를 조합해 offense slot 요구사항에 기여하는" 구조이지,
`perceived_fact`/`actual_fact` 두 사실을 비교해서 **`intent`의 법적 효과 자체를
변환**(다른 객체·다른 구성요건에 대해서도 고의를 인정)하는 transformation primitive가
아니다. `negligence_bundle`/`omission_bundle`은 "여러 leaf가 전부 있어야 만족되는
합성 요건"이라 이 구조에 정확히 맞지만, mistake는 "두 사실을 비교해 다른 predicate(intent)의
판정을 바꾼다"는 다른 종류의 논리라 같은 template가 그대로 맞는지 증명되지 않았다.

**v2(수정)** — 단계를 낮춘다:

```text
확정: mistake를 위한 shared Elements module이 필요하다(v2.1 설계 문서 7절의 예정 그대로)
미확정: 그 module이 기존 ElementBundleDef 하나로 표현 가능한가

ground_fact.perceived_fact / ground_fact.actual_fact / legal_element.mistake_within_same_construct
    → predicate 후보 자체는 v1 그대로 유지(타입 판정도 변경 없음)

2패스 저작 시 순서:
  1차 시도: bundle.mistake_bundle(ElementBundleDef)을 offense의 element_modules에
            {ref, placement→mental} 형태로 붙여 표현이 되는지 실제로 작성해본다.
  실패 시: ElementBundleDef 확장이나 별도 primitive가 필요한 architecture-compatibility
            issue로 승격한다(신규 MistakeDef 같은 새 top-level kind를 이번에 미리
            제안하지는 않는다 — 실제로 막혀야 승격).
```

---

## 정정 2 — 제18조: `omission_bundle`은 4-constituent 그대로, 선택적 부착 설명 삭제

**v1의 내부 모순**: `bundle.omission_bundle = ALL(duty_to_act, possibility_to_act,
failure_to_act, equivalence_to_commission)`으로 복구해놓고, 바로 아래서
"`equivalence_to_commission`은 특정 행위태양 요구 offense에서만 선택적으로 요구 →
bundle 자체를 그 offense에 붙일지의 문제"라고 적어 스스로 어긋났다. `omission_bundle`을
안 붙이면 `duty_to_act`/`possibility_to_act`/`failure_to_act`까지 전부 같이 사라져
단순결과범의 부작위(예: 부작위에 의한 살인)에서 보증인지위·작위가능성·부작위 자체를
판단할 수 없게 된다 — 원래 v2.1 설계도 4개를 처음부터 하나의 묶음으로 예정해뒀다.

**v2(수정)**:

```text
bundle.omission_bundle (ElementBundleDef, 변경 없음)
    requires = ALL(duty_to_act, possibility_to_act, failure_to_act,
                    equivalence_to_commission)
    → 모든 부진정부작위범 offense가 이 bundle 전체를 element_modules로 붙인다.
      선택적 constituent 없음.

equivalence_to_commission의 legal_standard 서술:
    "단순결과범(살인죄·상해죄 등 결과발생만 요구하는 구성요건)에서는 통상 쉽게 충족되고,
    특정 행위태양을 요구하는 구성요건(사기죄의 기망, 강제추행죄의 추행 등)에서는
    실질적 쟁점이 된다" — bundle 부착 여부의 문제가 아니라 이 predicate **하나의 판단
    난이도**가 offense마다 다르다는 서술로 legal_standard 안에만 남긴다.
```

---

## 정정 3 — 제19조: `concurrent_independent_acts`/`same_object_of_result` typing 재분류

**v1 오류**: 두 predicate를 `ground_fact`로 뒀는데, canonical_meaning을 다시 보면 이미
"의사연락 **없이**"(소극적 판단), "**구성요건적** 실행행위"(구성요건 해당성 판단),
"**사회적·규범적** 의미에서 동일"(규범적 동일성 판단)까지 포섭하고 있다 — 배치①에서
확정한 typing 기준("사건에서 관찰·추출되는 사실" → ground_fact / "그 사실을 법적 기준에
포섭한 판단" → legal_element)을 그대로 적용하면 legal_element다.

**v2(수정)**:

```text
legal_element.concurrent_independent_acts
    2인 이상이 의사연락 없이 각자 별개의 구성요건적 실행행위를 하였다

legal_element.same_object_of_result
    그 행위들이 동일한 객체(사회적·규범적 의미에서 동일)에 결과를 발생시켰다

legal_element.causal_origin_unascertained  (v1 그대로, 변경 없음)
    결과 발생의 원인이 된 행위가 어느 것인지 판명되지 않았다(법원이 심리 후
    확정하는 상태 — 엔진의 UNKNOWN이 아니다)

CompletionPolicy state (변경 없음):
    when = ALL(concurrent_independent_acts, same_object_of_result,
                causal_origin_unascertained)
    → attempted
```

v1의 핵심 정정("runtime UNKNOWN ≠ causal_origin_unascertained = TRUE")과 263조 특례를
Participation 검토(배치⑤/⑨)로 이월한 판단은 그대로 유지 — 이번엔 typing만 고친다.

---

## 배치② v2 요약

신규 스키마·DSL primitive는 여전히 없음. `negligence_bundle`/`omission_bundle`은
확정, `mistake_bundle`은 "구조 후보"로 낮춰 2패스에서 실증 후 확정하기로 함, 19조는
predicate 2개의 typing만 수정. 이번 라운드로 배치②를 마감한다.
