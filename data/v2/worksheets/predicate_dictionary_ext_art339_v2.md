# Predicate 사전 확장 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외) v2

[predicate_dictionary_ext_art339_v1.md](predicate_dictionary_ext_art339_v1.md)에 대한
사용자 검수 2건을 반영한다. v1은 그대로 둔다 — 이력 추적용. 첫째는 v1이 정정1을 적용하며
v0의 다른 부분(suspends)을 실수로 삭제한 것, 둘째는 실제 컴파일러 코드(`src/idpr/v2/
compile.py`, `expressions.py`, `truths.py`, `identity.py`, `relations.py`)를 직접 읽고
repro 스크립트로 검증해 확정한 **새로운 architecture-compatibility 발견**이다.

---

## 정정 4 — v1 최종 구조에서 `attempted.suspends`가 삭제된 채 남았다

**v1 오류**: 정정1(completion selector를 causation에서 vaginal_intercourse_conduct로
교체)을 적용하면서 v0에 있던 `suspends` 필드 자체를 최종 코드 블록에서 빠뜨렸다. 338
fixture(`completion_policy.robbery_homicide`)의 `attempted` state가 `suspends: [result,
causation]`를 명시하는 것과 대조하면, 339의 `ATTEMPTED`도 rape_part의 미완성 slot(간음이
아직 발생하지 않았으므로 그 result와 causation)을 명시적으로 suspend해야 한다 — completion
selector만 바꾸고 suspension 자체를 삭제하면 안 됐다.

**v2(정정) — `suspends`를 fixture와 동일하게 복원.**

```text
robbery_rape.ATTEMPTED.when = ALL(
    legal_element.commencement_of_execution (강간행위 착수, 25조 재사용),
    NOT(vaginal_intercourse_conduct)
)
robbery_rape.ATTEMPTED.punishable = true (원문 Ⅴ, 342조 재사용)
robbery_rape.ATTEMPTED.suspends = [result, causation]
    (rape_part가 채우는 두 슬롯 — vaginal_intercourse_conduct(result)/coercion_induced_
    sexual_act_causation(causation). robbery_part는 애초에 이 두 슬롯에 기여하지 않으므로
    이 suspend는 rape_part에만 영향을 준다.)
robbery_rape.ATTEMPTED.relations = [
    {relation: occasion_identity, left: robbery_part, right: rape_part, disposition: RETAIN}
    (강도의 기회에 강간행위가 이루어졌을 것은 미수에서도 그대로 요구됨 — 338 fixture 주석과
    동일 근거)
]
```

---

## 정정 5 — COMPOSE(offense, offense)에서 두 component가 같은 predicate id를 같은 slot에
쓰면 컴파일러가 그 둘을 하나로 뭉갠다(실재 확인, 339 자체는 트리거 안 됨)

**사용자 가설**: 339가 처음으로 "두 완전한 OffenseDef가 같은 shared predicate id를 각각
독립적으로 요구하는" 사례일 수 있고, 예컨대 robbery_part.intent=TRUE·rape_part.intent=
FALSE를 CaseTruths가 독립적으로 보존하지 못한다면 concrete architecture gap이라는 것.

**코드로 직접 확인한 결과 — 메커니즘 자체는 실재한다.**

1. `src/idpr/v2/compile.py`의 `_compile_compose`(283-294행)는 `kind: offense`인 컴포넌트
   여러 개를 COMPOSE할 때, 각 컴포넌트의 이미 컴파일된 `.slots[slot]`(CanonicalExpr)을
   `expressions.combine_all(*contributions)`로 그대로 ALL-결합한다 — local_key로 네임
   스페이스를 씌우지 않고 원본 leaf ref 문자열을 그대로 전달한다.
2. `src/idpr/v2/expressions.py`(9-10행)가 명시하듯 ALL/ANY는 "children을 frozenset으로
   보관(commutative; idempotency falls out of frozenset dedup for free)" — 즉 같은 leaf
   ref가 두 컴포넌트에서 각각 나와도 최종 CanonicalExpr에서는 **하나로 합쳐진다.**
3. `src/idpr/v2/runtime/truths.py`(84행) `CaseTruths.predicate`는
   `Mapping[tuple[OffenseInstanceKey, str], TruthValue]` — predicate ref는 순수 문자열
   키이고, `OffenseInstanceKey`(`identity.py`)는 case/actor/offense_ref/occurrence 수준
   에서만 구분되지 COMPOSE 내부의 local_key까지는 내려가지 않는다.
4. 대조로 **relation은 이 문제를 이미 해결해뒀다** — `relations.py`의
   `RelationInstanceKey.occurrence_path`(58-60행)가 정확히 "top-level offense id +
   local_key chain… 같은 ref가 다른 local_key 아래 두 번 나타날 수 있고, 그 둘을
   구별해야 한다"는 목적으로 설계돼 있다. `compile.py` 모듈 docstring(6-8행)도 이
   구별을 relation binding에 대해서만 명시한다 — element leaf에는 이 메커니즘이
   없다.

**repro (`docs/contracts/v2/examples/offenses.yaml`의 실제 fixture가 아니라, 두 컴포넌트가
같은 mental id를 쓰는 최소 반례를 직접 구성):**

```text
offense.toy_robbery.elements.mental = ref(legal_element.intent)
offense.toy_rape.elements.mental    = ref(legal_element.intent)   # 의도적으로 동일 id
derived_offense.toy = compose(robbery_part=toy_robbery, rape_part=toy_rape)

compile_offense(...).slots['mental']  ==  ('ref', 'legal_element.intent')   # 하나로 합쳐짐
compile_offense(...).slots['conduct'] ==  ('all', {ref(robbery_conduct), ref(rape_conduct)})
                                            # id가 다르면 정상적으로 둘 다 유지됨(대조군)
```

`mental` 슬롯이 정말로 하나의 leaf로 합쳐진다 — 두 component가 같은 predicate id를 같은
slot에서 쓰면, 컴파일된 offense는 그 사실을 딱 하나의 CaseTruths 조회로만 답할 수 있고
"A는 TRUE, B는 FALSE"를 표현할 방법이 없다.

**그러나 339 자체는 이 gap을 트리거하지 않는다 — 확정된 predicate 사전을 전 슬롯 대조한
결과.**

| slot | robbery_part(333, 재산죄 pilot 확정) | rape_part(297, 배치⑩ 확정) | 충돌? |
|---|---|---|---|
| object | `ground_fact.property_taking` | `legal_element.natural_person_victim_status` | 없음 |
| conduct | `ground_fact.property_taking` + `legal_element.robbery_level_violence` | `legal_element.coercive_conduct` + `legal_element.directness_of_coercion_by_offender` + `legal_element.coercion_sufficiency_for_rape` | 없음 |
| mental | `legal_element.unlawful_appropriation_intent`(재산죄 전용, 329·333·355 공유) | `legal_element.intent`(13조, 전역) | **없음 — 서로 다른 id** |
| result | (없음, 333 fixture·pilot 모두 result 슬롯 안 씀) | `ground_fact.vaginal_intercourse_conduct` | 없음 |
| causation | (없음) | `legal_element.coercion_induced_sexual_act_causation` | 없음 |

333(강도)의 mens rea가 13조 `legal_element.intent`가 아니라 재산죄 전용
`unlawful_appropriation_intent`로 이미 분리 확정돼 있었기 때문에(재산죄 pilot v0/v1,
"절도·강도·횡령 공유") 339에서 우연히 충돌을 피한 것이지, **설계가 이 문제를 의도적으로
막은 게 아니다.** robbery_part의 mens rea가 (가상으로) `legal_element.intent`만으로
표현되는 offense였다면 339는 그 즉시 이 gap의 첫 실제 피해 사례가 됐을 것이다.

**결론 — architecture-compatibility 목록에 신규 추가, 339 자체는 population 진행,
발동 여부는 실제 authoring 시점(2-pass)에 재확인.**

```text
신규 발견 — COMPOSE(offense, offense)의 element-leaf 재사용 충돌
(compile.py의 slot 병합이 local_key로 네임스페이스를 씌우지 않아, 두 완전한 offense
 component가 같은 slot에서 같은 predicate id를 쓰면 CaseTruths가 둘을 구별하지 못한다 —
 relation은 RelationInstanceKey.occurrence_path로 이미 해결했으나 element leaf는 대응
 메커니즘이 없음. repro로 실증.)

현재 영향: 없음 — 339(유일한 두-완전-offense COMPOSE 사례)의 확정 predicate 세트는
robbery_part·rape_part 사이에 겹치는 id가 하나도 없다(위 표).

watch 조건: 2-pass에서 실제 `derived_offense.robbery_rape` YAML을 저작할 때, 그리고
향후 다른 조문이 "두 완전한 offense를 COMPOSE"하는 패턴을 다시 쓰게 될 때, 두 component의
전 슬롯 predicate id가 겹치지 않는지 매번 확인해야 한다. 겹치는 사례가 실제로 나오면
그때는 (a) `compile.py`에 local_key 네임스페이스 메커니즘을 추가하거나(relation과 대칭),
(b) 겹치는 predicate를 offense별로 분리 재정의(canonical_meaning 불변 원칙과 충돌하므로
선호 안 함)하는 두 방향 중 (a)를 우선 검토해야 한다.
```

이건 33조 단서·34조처럼 "predicate 사전만으로는 못 닫는" 유형이 아니라 **컴파일러 자체의
동작을 코드로 직접 반증(counter-example)해서 확인한 gap**이라는 점에서 기존 HOLD 항목들과
성격이 다르다 — 이번 배치 HOLD 목록에는 (C) "컴파일러 메커니즘 확인, 현재 미발동"으로
별도 분류해 올린다.

---

## self-check 체크리스트 재적용 메모 (v2)

- **정정 적용 시 이전 필드를 실수로 삭제하지 않는다**(신규 항목, 정정4에서 얻음): 한
  필드(completion selector)를 고치면서 근처의 다른 필드(suspends)를 함께 다시 쓰다가
  누락하는 오류 — 정정할 땐 "바뀌는 부분만" 최소 diff로 표현하고 나머지는 원본을 그대로
  복사해야 한다.
- **architecture-compatibility 주장은 실제 코드 실행으로 검증한다**(신규 항목, 정정5에서
  얻음): "가능성이 높다"는 추정이 아니라 실제 repro를 돌려 컴파일된 결과를 눈으로
  확인했다 — 그리고 검증 결과가 사용자의 가설을 부분적으로만 확인시켜줬다(메커니즘은
  실재, 339 자체는 미발동)는 것까지 정직하게 기록했다. gap의 "존재"와 "이 조문에서의
  발동 여부"는 별개 질문이다.

---

## 최종 확정 predicate (v2)

정정1-3(v1) 그대로 유지 + 정정4(suspends 복원) + 정정5(신규 architecture-compatibility
(C) 항목 1건, 컴파일러 메커니즘 확인·339 자체는 미발동). 신규 predicate 0건·신규
스키마 0건은 여전히 유지 — 정정5는 predicate가 아니라 컴파일러 동작에 관한 확인사항이다.

HOLD/2-pass 확인 목록(art339):
- (기존, 정정2) robbery-side COMPOSE 구조(component ref 여러 개 vs 공통 base 재사용) —
  337·338과 함께 2-pass 재확인.
- (신규, 정정5, (C)분류) COMPOSE(offense, offense)의 element-leaf 재사용 충돌 메커니즘 —
  339 자체는 미발동, 2-pass 실제 저작 및 향후 유사 패턴 재사용 시 슬롯별 id 겹침 확인 필수.
