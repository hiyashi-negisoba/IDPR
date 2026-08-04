# RuleIR predicate 계약: 재산죄 구조를 비재산죄에 그대로 쓸 수 있는가

> 이 문서는 RuleIR 확장 시의 구조적 위험을 설명한다. 수치와 구현 상태는 작성 당시 기준이며,
> 현재 차단 결점과 수리 순서는 [`CURRENT.md`](CURRENT.md)를 우선한다.

작성 근거: `data/rulegen/rule_ir_registry_manifest.json`에 등록된 11개 unit의 RuleIR candidate
JSON과 `rules/generated/*.scl` 전수 실측. 추정 없음.

## 결론 먼저

**"재산죄의 명명과 인자 구조를 그대로 따른다"는 명제는 성립하지 않는다.** 재산죄 11개 unit
사이에서도 인자 구조가 이미 서로 다르기 때문이다. 그대로 따를 수 있는 것은 이름이 아니라
**계층 형태**다.

## 실측 1: role tuple은 이미 죄종마다 다르다

| unit | role predicate 인자 |
|---|---|
| fraud | case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, beneficiary_id |
| robbery | case_id, defendant_id, coerced_person_id, owner_id, possessor_id |
| extortion | case_id, defendant_id, coerced_person_id, disposer_id, owner_id |
| theft | case_id, defendant_id, owner_id, possessor_id |
| embezzlement | case_id, defendant_id, entrustor_id, owner_id |
| breach_of_trust | case_id, defendant_id, principal_id, beneficiary_id |
| breach_of_trust_bribe | case_id, receiver_id, giver_id, principal_id |
| property_damage | case_id, defendant_id, owner_id |
| lost_property_embezzlement | case_id, defendant_id, owner_id |
| interference_with_exercise_of_right | case_id, defendant_id, right_holder_id |
| occupational_status | case_id, defendant_id |

arity가 2에서 6까지 흩어져 있다. `breach_of_trust_bribe`는 `defendant_id`조차 없다.

## 실측 2: 실제로 불변인 계약

이름이 아니라 형태가 계약이다. 11개 unit 전부가 예외 없이 지킨다.

```text
system input   provable(case_id, assessment_id)
system input   case_assessment_complete(case_id, defendant_id)
system input   distinct_entity(case_id, left_entity_id, right_entity_id)
system input   <unit>_case_roles(case_id, ...role ids)            ← 죄종별 가변

commentary     assess_<card_slug>(case_id, assessment_id, ...roles, status)   ← 3상태
derived        satisfied_<card_slug>(case_id, ...roles)
derived        <component>_satisfied(case_id, ...roles)

결론           <unit>_elements_satisfied(case_id, ...roles)
결론           <unit>_established(case_id, ...roles)
결론           <unit>_not_established(case_id, defendant_id, norm_card_id)
결론           <unit>_undetermined(case_id, defendant_id, norm_card_id)
결론           <unit>_conflict(case_id, defendant_id, norm_card_id)
```

주목할 비대칭이 있다. 성립 계열은 role tuple 전체를 인자로 받지만, 불성립·미확정·충돌 계열은
`(case_id, defendant_id, norm_card_id)` **3항 고정**이다. 부정 결론은 어느 카드 때문인지만
남기고 역할 구조를 버린다. 이 비대칭은 죄종과 무관하므로 방화에도 그대로 쓸 수 있다.

`<unit>_established`는 `elements_satisfied and case_assessment_complete and ~has_negative and
~has_conflict`로 닫힌다. 이 폐쇄세계 게이트도 공통이다.

## 실측 3: 재산죄에 없는 것 두 가지

### 갭 A — 단계(stage) 결론이 없다

미수 카드는 실재한다. `art330_sec4.entry_attempt_examples`, `art333_sec6.attempt_commencement_
violence_intimidation`, `art342.attempts_punishable` 등이 assess_ 카드로 들어가 있다. 그런데
**결론층에는 미수 relation이 없다.** 미수 카드가 기수 카드와 같은 `theft_established` 하나로
수렴한다.

방화는 D4에서 "기본·미수·치사상 subtype 분리 출력"을 이미 승인받았다. 재산죄를 그대로 따르면
그 승인을 위반한다.

### 갭 B — outcome bridge가 없다

`occupational_status`는 manifest에서 `shared_module: true`이지만, 컴파일된 SCL은 다른 unit의
어떤 relation도 참조하지 않는다. 자기 카드만 평가한다. 즉 D5에서 승인한 canonical outcome
bridge는 **설계만 있고 구현체가 없다.**

방화 승인 원장의 post_outcome 12장 중 8장이 다른 unit(homicide, robbery, property_damage)을
참조한다. bridge 없이 컴파일하면 이 12장은 결론에 아무 영향을 주지 못한다.

## 실측 4: 인자 과다 설계가 결론층에서 죽는 사례

`fraud_case_roles`는 `deceived_person_id`와 `disposer_id`를 별도 인자로 선언한다. 그런데
컴파일된 유일한 `fraud_established` head는 두 자리에 같은 변수를 넣는다.

```text
rel fraud_established(case_id, defendant_id, deceived_person_id, deceived_person_id,
                      property_owner_id, beneficiary_id) = ...
```

이것은 버그가 아니라 법리적으로 옳다. 사기죄에서 처분행위는 기망당한 자가 해야 하므로
피기망자와 처분행위자는 항상 같다. 삼각사기에서 갈라지는 것은 처분행위자가 아니라 재산상
피해자다. 다만 결과적으로 **6항 tuple의 4번째 인자는 결론층에서 아무 일도 하지 않는다.**

교훈: 법리상 항상 일치하는 역할을 별도 인자로 두면 인자가 죽는다. 방화 role tuple 설계에서
같은 실수를 반복하면 안 된다.

## 리스크 A: 파이프라인 일관성

| # | 리스크 | 실측 근거 | 완화 |
|---|---|---|---|
| A1 | role tuple arity가 unit마다 달라 호스트가 FactGraph를 EDB로 주입할 때 unit별 분기가 필요해지고, 이는 하드코딩 금지 규칙과 충돌한다 | manifest는 `role_predicate` 이름만 선언하고 인자 서명을 선언하지 않는다 | manifest에 `role_signature`(인자명·순서·타입)를 추가해 주입기가 데이터만 읽고 동작하게 한다 |
| A2 | 방화가 4-track이면 query relation이 5개가 아니라 track별로 늘어난다 | `registry.py`는 `query_relations`가 비어있지 않기만 요구하고 개수를 고정하지 않는다 | 구조적으로 수용 가능. manifest에 track↔relation 매핑을 선언하면 된다 |
| A3 | 경량화 관점에서 로드 단위가 track까지 쪼개지면 로드량이 늘어난다 | — | 결정론적 로드이므로 의미 검색은 여전히 불필요하다. 비용은 predicate 수이지 지연이 아니다 |
| A4 | unit마다 role tuple을 새로 설계하면 25개 P2 unit에서 설계 편차가 누적된다 | 재산죄 11개에서 이미 발생 | role 어휘 자체를 외부 자산으로 고정하고 unit이 그중에서 고르게 한다 |

## 리스크 B: 법리 정확성

| # | 리스크 | 결과 | 심각도 |
|---|---|---|---|
| B1 | 단계를 분리하지 않으면 방화 기수·미수·치사상이 하나의 `established`로 수렴한다 | 법정형이 7년 이상에서 사형·무기까지 달라지는 세 결론이 구별되지 않는다 | 높음. D4 승인 위반 |
| B2 | outcome bridge 없이 post_outcome 카드를 컴파일하면 죄수·경합 규칙이 결론에 도달하지 못한다 | 방금 확정한 대법원 96도485 재정(존속살해 상상적 경합)이 런타임에서 실행되지 않는다. 법리 검수 결과가 사장된다 | 높음 |
| B3 | 재산죄 role 어휘를 방화에 재사용하면 방화의 '사람'이 owner/possessor에 억지로 매핑된다 | 승인된 `person_scope` component(범인·공범 제외)를 표현할 자리가 없다. 방화는 공공위험범이고 객체가 건조물이지 재물이 아니다 | 높음 |
| B4 | 역할을 과다 선언하면 결론층에서 강제 통일되어 죽은 인자가 생긴다 | fraud의 `disposer_id`가 실례 | 낮음. 설계 시 회피 가능 |
| B5 | 불성립·미확정·충돌이 3항 고정이라 역할별 구분이 사라진다 | 피해자가 여럿인 방화치사상에서 "누구에 대해 불성립인지"가 결론에 남지 않는다 | 중간. 재산죄에서도 동일하나 방화는 다수 피해자가 흔하다 |

## 권고

1. **명명 규칙은 그대로 따른다.** unit_id 유래 relation 이름, 4개 system input, 성립/불성립
   비대칭, 폐쇄세계 게이트는 죄종과 무관한 형태이므로 방화도 동일하게 간다.
2. **role tuple은 방화 고유로 새로 설계한다.** 재산죄에서 빌려오지 않는다. 방화는 공공위험범이라
   객체가 건조물이고, 치사상 track에서만 피해자가 등장한다.
3. **track별 결론 분리를 manifest에 선언한다.** 이것이 B1의 유일한 해법이고 registry는 이미
   수용 가능하다.
4. **outcome bridge는 방화 unit 안에서 만들지 않는다.** 별도 공유 자산으로 분리하되, 그 전까지
   post_outcome 12장은 `predicate_ir_missing`으로 정직하게 보고한다.

## 미결 질문

- 방화 첫 컴파일 범위를 base/attempt/completed까지로 하고 aggravated_result와 post_outcome을
  다음 단계로 미룰 것인가, 아니면 bridge까지 한 번에 만들 것인가?
- role tuple 후보: `arson_case_roles(case_id, defendant_id, structure_id, occupant_id)`를
  base/attempt/completed에 쓰고, 치사상은 `victim_id`가 추가된 별도 tuple을 쓰는 안.
  법리적으로 `occupant_id`와 `victim_id`가 항상 일치하지는 않으므로 분리가 맞는지 확인이 필요하다.
