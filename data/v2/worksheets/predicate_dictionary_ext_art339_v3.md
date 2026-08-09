# Predicate 사전 확장 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외) v3

[predicate_dictionary_ext_art339_v2.md](predicate_dictionary_ext_art339_v2.md)에 대한
사용자 검수 1건을 반영한다. v2는 그대로 둔다 — 이력 추적용. v2의 "339 자체는 미발동"
결론이 틀렸다 — `commencement_of_execution`이라는, intent와는 다른 predicate에서 실제로
발동한다. `completion.py`·`pipeline.py`를 추가로 직접 읽어 검증했고, 그 과정에서 사용자가
지목한 두 번째 문제(robbery 미수+rape 기수 → 339 기수 표현 가능성)가 예상보다 더 깊은
곳(COMPLETED state의 슬롯 누출)까지 번진다는 것도 확인했다. **이번 정정으로 art339의
CompletionPolicy 구조는 확정에서 미확정(active HOLD)으로 강등한다.**

---

## 정정 6 — v2의 "339 자체는 미발동" 결론이 틀렸다: `commencement_of_execution` 충돌은
실제로 발동한다

**v2 오류**: v2는 Elements 슬롯(object/conduct/mental/result/causation)만 대조하고
"겹치는 id 없음 → 미발동"이라고 결론냈다. 그러나 `legal_element.commencement_of_
execution`(25조)은 **Elements 슬롯에 나타나는 predicate가 아니라, 각 offense 자신의
CompletionPolicy `attempted.when`에만 나타나는 predicate**다(pilot·배치⑦-⑫ 전체가
"25조 재사용"으로 매 offense마다 동일하게 참조) — v2의 slot 대조표는 이 predicate를
애초에 포함하지 않았다.

**실제 반례(사용자 제시, 코드로 재확인)**:

```text
robbery 실행착수 = TRUE   (강도는 시작됨)
rape 실행착수    = FALSE  (강간은 아직 착수 안 됨)
vaginal_intercourse_conduct = FALSE
```

법적으로 이건 **339의 미수조차 아니다** — 강간의 실행행위 자체가 시작되지 않았으므로.
그런데 v1/v2가 쓴 `339.ATTEMPTED.when = ALL(commencement_of_execution,
NOT(vaginal_intercourse_conduct))`에서 `commencement_of_execution`이 참조하는 truth
값이 (실제로는 "robbery의 착수"에서 비롯된 것이라도) 하나의 `CaseTruths` 슬롯
`(339_instance, "legal_element.commencement_of_execution")`으로만 저장되므로, 이
formula는 "무엇의 착수인가"를 구별하지 못한 채 TRUE를 받아들여 339를 ATTEMPTED로 잘못
판정할 수 있다.

**코드로 확인**: `src/idpr/v2/runtime/completion.py`의 `resolve_completion()`(174-178행)이
`states[name]["when"]`을 `truths.predicate_view(instance)` — 즉 339라는 **단일 top-level
instance**로 스코프된 flat mapping — 에 대해서만 평가한다. `offense.robbery`·`offense.rape`가
COMPOSE 안에서 각각 별도 `OffenseInstanceKey`를 받는 게 아니라 339 하나의 instance 아래
묶이므로, 두 offense가 각자 공유하는 `commencement_of_execution`을 이 evaluation 층위에서
구별할 방법이 없다 — v2가 (마땅히) relation에 대해 확인했던 "local_key 네임스페이스 부재"가
CompletionPolicy `when` 평가에서도 똑같이 반복된다.

---

## 정정 7 — (사용자 지적 확장) COMPLETED state가 object/conduct 슬롯을 suspend하지
않으므로, robbery의 `property_taking`이 339 COMPLETED에서 암묵적으로 새어 들어와 요구된다

**사용자 질문**: "robbery component가 attempted 상태여도 rape completed이면 339
completed를 표현 가능한가?" — `pipeline.py`를 직접 읽어 확인한 답은 **현재 초안으로는
불가능하다.**

`src/idpr/v2/runtime/pipeline.py`의 `_iter_obligations()`(263-269행)는 `SLOT_NAMES`
(subject/object/conduct/circumstance/result/causation/mental) 중 **그 completion
state가 suspend하지 않은 슬롯 전부**를 `compiled.slots.get(slot)`(COMPOSE로 이미 병합된
전체 표현식)로 평가해 `fold_all`한다. v1/v2가 쓴 `339.COMPLETED`는 `suspends`를 전혀
선언하지 않았다 — 즉 `object`(`ALL(property_taking, natural_person_victim_status)`)와
`conduct`(`ALL(property_taking, robbery_level_violence, coercive_conduct, ...)`)가
그대로 평가되고, 둘 다 `property_taking`을 포함한다. **`property_taking`(robbery의 재물
탈취 완료 여부)이 suspend되지 않으므로, 339가 COMPLETED로 판정되려면 robbery 자신도
완전히 기수여야 한다는 뜻이 되어버린다** — 원문 Ⅴ "강도가 미수라도 강간이 기수면
강도강간죄의 기수"와 정면으로 충돌한다.

**더 나쁜 소식 — 고치려 해도 flat SLOT_NAMES로는 못 고친다.** `property_taking`을
빼내려면 `object`·`conduct` 슬롯을 통째로 suspend해야 하는데, 그 두 슬롯에는
rape_part의 `natural_person_victim_status`·`coercive_conduct` 등도 같이 들어있다 —
슬롯이 offense 전체에 대해 flat하게 하나씩만 존재하고 component별로 나뉘지 않으므로
(`_compile_compose`가 슬롯을 병합할 때 local_key 정보를 버림, 정정5와 같은 근본 원인),
"robbery 쪽 conduct 요건만 suspend, rape 쪽 conduct 요건은 유지"를 표현할 방법이
없다.

**이건 배치⑫ F-5-1(335조)이 이미 남긴 HOLD와 같은 계열이지만 한 단계 더 심각하다.**
F-5-1은 "base offense(절도)의 completion이 derived offense(준강도)의 completion을
결정하는 링크가 8차 addendum `derivative_mode.requires`로 표현 가능한지"를 물었다 — 335는
base가 절도 **하나**였다. 339는 base(강도)와 attached(강간) **둘 다 완전한 offense**라서,
"한쪽만 미수 허용, 다른 쪽은 기수 강제"를 표현하려면 슬롯이 아니라 **component 단위**로
completion을 따로 추적해야 하는데 현재 컴파일러는 그 층위 자체가 없다.

---

## 재분류 — future watch가 아니라 active HOLD, art339는 완전히 닫지 않는다

배치⑫ 스타일의 (A)/(B)/(C) 분류를 다음과 같이 갱신한다.

```text
(D) 339에서 실제로 발동 확인된 architecture-compatibility 항목 (active HOLD,
    2-pass 착수 전 반드시 해소해야 함 — future watch 아님)

  D-1. commencement_of_execution 충돌 (정정6)
       robbery_part와 rape_part가 각자의 CompletionPolicy에서 같은 25조 predicate를
       쓰는데, 339의 top-level CompletionPolicy가 이를 구별 없이 참조하면 "강도만
       착수, 강간은 미착수" 사건이 339의 미수로 오판될 수 있다. 해소 전에는 339의
       ATTEMPTED.when을 이 형태로 확정할 수 없다.

  D-2. COMPLETED state의 슬롯 누출 (정정7)
       flat SLOT_NAMES 기반 suspend 메커니즘이 component 단위가 아니라서, robbery
       미수+rape 기수 = 339 기수(원문 Ⅴ)를 표현하면 rape 쪽 object/conduct 요건까지
       함께 새나간다. F-5-1(335)과 같은 계열이나 "두 완전한 offense COMPOSE"라서
       더 심각 — component-scoped completion/suspension 메커니즘 자체가 없으면
       구조적으로 막힌다.

  둘 다 predicate 사전으로 닫을 수 있는 문제가 아니라 컴파일러/런타임 설계(compile.py
  slot 병합, completion.py의 instance 스코프)의 변경 여부를 요구하는 문제다 — 2-pass
  착수 전에 (a) component-scoped predicate/completion 네임스페이스를 compile.py·
  completion.py에 추가하거나, (b) 이 특정 패턴(두 완전한 offense를 completion까지
  독립적으로 유지한 채 COMPOSE)을 현재 DSL이 지원하지 않는다고 확정하고 다른 표현
  방식(예: 339를 QUALIFY 계열로 재설계하거나, robbery/rape 각각을 별도로 평가한 뒤
  orchestrator 층에서 결합)을 찾아야 한다.

(C, 정정5 유지) COMPOSE(offense, offense)의 element-leaf 재사용 충돌 — 339의 실제
  predicate 세트에서는 미발동(mental 등 Elements 슬롯 레벨 predicate는 로버리·레이프가
  서로 다른 id를 쓰므로) — 이 항목만 future-watch로 유지, D-1·D-2와는 성격이 다르다.

(기존, 정정2 유지) robbery-side COMPOSE 구조(component ref 여러 개 vs 공통 base 재사용)
  — 337·338과 함께 2-pass 재확인.
```

**art339는 이번 라운드에서 predicate·구조 확정을 완료 처리하지 않는다.** B절(강간 요소
predicate 재사용)·A절(주체)·C절(occasion_identity relation)은 그대로 유효하지만,
**D절(CompletionPolicy)은 미확정으로 되돌린다** — v1/v2가 제시한 구체 formula
(`COMPLETED.when = vaginal_intercourse_conduct`, `ATTEMPTED.when = ALL(commencement_
of_execution, NOT(...))`)는 D-1·D-2가 해소되기 전까지 **잠정 초안**으로만 남기고, "확정"
표기를 붙이지 않는다.

---

## self-check 체크리스트 재적용 메모 (v3)

- **shared predicate 충돌 검사는 Elements 슬롯만으로 끝나지 않는다**(신규 항목, 정정6에서
  얻음): CompletionPolicy `when` 절이 참조하는 predicate(특히 25조 `commencement_of_
  execution`처럼 전역 재사용되는 것)도 같은 검사 대상이다 — Elements 슬롯 대조표 하나로
  "충돌 없음"을 결론 내리면 안 된다.
- **"고칠 수 있어 보인다"는 인상만으로 구조를 확정하지 않는다**(신규 항목, 정정7에서
  얻음): `suspends`를 추가하면 될 것 같았던 문제가, 실제로 어느 슬롯을 suspend해야
  하는지 따라가 보니 다른 component의 요건까지 함께 새는 구조적 막다른 길이었다 —
  "필드 하나 더 쓰면 된다"는 해결책은 그 필드가 실제로 원하는 세분화 수준을 제공하는지
  코드로 확인한 뒤에만 채택한다.

---

## 최종 상태 (v3) — art339 부분 확정, CompletionPolicy는 active HOLD로 이월

확정: A절(주체, base_offense candidate 목록)·B절(강간 요소, `offense.rape[297]`
component ref 재사용)·C절(occasion_identity relation, "강도의 기회")·정정3(component ref
authoring 원칙). **미확정(active HOLD, D-1·D-2)**: CompletionPolicy 전체 구조 — 339가
"두 완전한 offense를 completion 층위까지 독립적으로 유지한 채 COMPOSE"하는 첫 사례라서,
현재 compile.py/completion.py가 제공하는 flat slot·단일 instance 스코프 메커니즘만으로는
원문 Ⅴ의 완성/미수 규칙을 정확히 표현할 수 없다. 신규 predicate 0건은 유지(이 gap은
predicate가 아니라 컴파일러/런타임 설계 문제) — 다만 2-pass 착수 전에 D-1·D-2를 337·338·
335의 관련 HOLD(F-5-1, 정정2)와 함께 반드시 먼저 해소해야 한다.
