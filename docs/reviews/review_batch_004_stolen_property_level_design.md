# 검수 배치 004 — 법률검수 판정

## J-01 track 구조 확정

판정: **O — 빈 track 등록 및 `positive_path_missing` 처리 승인**

> comment: `transfer`와 `brokering`을 빈 튜플로 등록하고 가짜 component나 가짜 LEVEL을 만들지 않는 것이 맞습니다. 현재 두 track에는 실제 양도행위·알선행위가 있었다는 긍정 component가 없고, 정의 카드만 존재합니다.
>
> 다만 빈 track의 실행 의미를 다음처럼 고정해야 합니다.

```text
track_status = positive_path_missing
established = unavailable
not_established = 승인된 track-scoped bar가 직접 발화한 경우에만 가능
otherwise = unsupported_due_to_rulebase_gap
```

> 이 상태는 track 자체의 삭제나 불성립이 아닙니다.
>
> * 취득·운반·보관 track은 정상 실행
> * 양도·알선이 실제 쟁점으로 선택된 사건에서는 symbolic verdict를 `unsupported`
> * 양도·알선이 쟁점이 아닌 사건에서는 전체 장물죄 verdict에 영향 없음
>
> Registry audit에는 다음 오류를 남기는 것이 적절합니다.

```text
TRACK_POSITIVE_COMPONENT_MISSING:
  stolen_property.transfer
  stolen_property.brokering
```

---

## J-02 공유요건의 내부 분해

판정: **X — 제안된 4개 레벨로는 부족하며 카드 배치 일부가 잘못됨**

> comment: “서로 다른 요건 차원을 한 LEVEL의 OR로 묶어서는 안 된다”는 문제의식은 전적으로 맞습니다. 다만 제안된 4개 레벨의 카드 구성에는 세 가지 문제가 있습니다.

### 1. `instigator_aider_subject`는 일반 주체 component가 될 수 없음

`instigator_aider_subject`는 다음 명제입니다.

```text
본범의 교사범 또는 방조범도 장물죄의 주체가 될 수 있다.
```

이를 주체 LEVEL의 단독 카드로 두고 모든 LEVEL을 AND로 결합하면 다음과 같은 잘못된 결과가 됩니다.

```text
장물죄 성립
→ 피고인이 본범의 교사범 또는 방조범이어야 함
```

그러나 일반적인 제3자 장물범은 본범의 교사범·방조범이 아니어도 됩니다.

따라서 두 선택지 중 하나가 필요합니다.

#### 권고안 A — 일반 주체 적격 component 신설

```text
actor_is_person_other_than_principal_offender
```

그리고 다음은 그 하위 인정 사례 또는 requirement clarification으로 둡니다.

```text
instigator_or_aider_is_not_principal_executor
→ subject_eligible
```

#### 권고안 B — 주체 LEVEL을 positive mandatory level에서 제거

본범 정범·공동정범이면 track-scoped 또는 unit-scoped bar를 발화시키고, 그 bar가 없는 경우 별도의 주체 positive component를 요구하지 않는 방식입니다.

다만 명시적 긍정 증명을 중시하는 현재 RuleBase 구조에서는 **권고안 A가 더 적절**합니다.

현재 카드만으로는 주체 LEVEL의 positive coverage도 불완전합니다.

### 2. `chain_stolen_property`는 객체 유형 카드가 아님

다음 두 카드는 재물이 어떤 형태인지에 관한 객체 유형입니다.

```text
tangible_property
embodied_security
```

반면 `chain_stolen_property`는 다음을 뜻합니다.

```text
앞선 장물죄로 취득된 장물도 다시 후속 장물죄의 장물이 될 수 있다.
```

이는 객체의 유체성이나 증권 여부가 아니라 **장물의 발생 원인·장물성의 연쇄**에 관한 명제입니다.

따라서 다음처럼 분리해야 합니다.

```text
shared_object_type:
  tangible_property
  embodied_security
  관계 = OR

shared_stolen_character_or_provenance:
  chain_stolen_property
  predicate_property_crime 등
  관계 = 별도 장물성 인정 경로
```

`chain_stolen_property` 하나가 satisfied되었다는 이유로 재물성까지 자동 충족되어서는 안 됩니다.

### 3. 고의 카드 두 장은 OR가 아님

```text
intent_and_knowledge
knowledge_timing_instant_offenses
```

첫 카드는 필요한 주관적 요소의 **내용**을 설명하고, 두 번째 카드는 그 인식이 존재해야 하는 **시점**을 설명합니다.

따라서 대안관계가 아닙니다.

```text
장물성 인식 존재
AND 해당 행위 시점에 인식 존재
```

가 되어야 합니다.

더구나 `knowledge_timing_instant_offenses`는 취득·양도·알선 같은 즉시범적 track에 관한 시점 법리이므로 모든 track의 공유 LEVEL로 두면 안 됩니다. 운반·보관은 계속행위 중 뒤늦게 장물성을 알게 된 경우가 별도로 문제되기 때문입니다.

권고 구조:

```text
shared_mens_rea_content:
  actual_awareness_of_stolen_character

acquisition_knowledge_timing:
  awareness_at_delivery

transfer_knowledge_timing:
  awareness_at_transfer

brokering_knowledge_timing:
  awareness_at_brokering_act

transport_knowledge_timing:
  awareness_at_start
  OR later_awareness_and_continued_transport

custody_knowledge_timing:
  awareness_at_start
  OR later_awareness_and_continued_custody
```

### 4. 의사합치와 그 시점도 OR가 아님

```text
prior_possessor_consensus
consensus_at_time_of_act
```

후자는 전자의 대안이 아니라 시간적 한정입니다.

```text
의사합치 존재
AND 그 의사합치가 실행행위 당시에 존재
```

두 레벨로 나누거나, 다음과 같은 하나의 완성된 사실 predicate로 합쳐야 합니다.

```text
prior_possessor_consensus_at_time_of_act
```

현재 두 카드를 OR로 묶으면 “의사합치는 필요하다”는 추상적 법리만 satisfied되어도 실제 시점의 합치가 없는데 요건이 충족될 수 있습니다.

### 권고 shared 구조

```text
S0_subject_eligibility
S1_object_type
S2_stolen_character_or_provenance
S3_awareness_of_stolen_character
S4_prior_possessor_consensus
S5_consensus_timing
```

다만 `S3`의 구체적 인식시점은 각 track으로 내려보내는 편이 더 정확합니다.

---

## J-03 track별 행위와 고의시점 분리

판정: **다른 지시 — 분리 원칙은 O, 제시된 카드는 추가 분리 후 적재**

> comment: 객관적 실행행위와 장물성 인식의 시점을 별도 LEVEL로 두고 AND로 결합하는 것은 맞습니다. 문서에 인용된 취득·보관 카드 역시 하나는 현실적 점유이전·수취이고 다른 하나는 인식시점이므로 같은 OR LEVEL에 둘 수 없습니다.

그러나 `acquisition.knowledge_at_delivery`도 그대로 component에 넣으면 안 됩니다.

### 1. `acquisition.knowledge_at_delivery`도 복합 카드임

이 카드에는 세 가지 효과가 들어 있습니다.

```text
계약 체결 당시 인식은 불필요
현실적 인도 당시 인식은 필요
취득 후 비로소 인식한 경우 취득죄 불성립
```

따라서 다음처럼 분리해야 합니다.

```text
acquisition.knowledge_not_required_at_contract
  role = requirement_waived

acquisition.actual_knowledge_at_delivery
  role = component
  level = acquisition_knowledge_timing

acquisition.only_later_knowledge
  role = bar
  scope = acquisition track
```

현재 한 카드 그대로 component에 넣으면 requirement waiver와 bar 효과가 사라지거나, 반대로 카드 전체의 추상적 법리만 참이라는 이유로 인식시점 component가 충족될 수 있습니다.

### 2. `custody.knowledge`는 최소 3개로 분리

```text
custody.knowledge_at_start
  role = component

custody.later_knowledge_and_continued_storage
  role = component
  같은 고의시점 LEVEL에서 위 카드와 OR

custody.rightful_possession_after_later_knowledge
  role = bar
  scope = custody track
```

세 번째 카드를 `requirement_waived`로 보내면 안 됩니다.

`requirement_waived`는 어떤 요건이 불필요하다는 의미이고 성립을 막지 않습니다. 반면 점유할 권한이 있어 계속 보관하여도 장물보관죄가 성립하지 않는다는 명제는 **보관 track을 실제로 차단**하므로 `bar`입니다.

### 3. track 결합

분리 완료 후에는 다음처럼 AND가 맞습니다.

```text
acquisition:
  common_requirements
  AND acquisition_actual_possession
  AND acquisition_knowledge_at_delivery

custody:
  common_requirements
  AND custody_actual_receipt
  AND (
        custody_knowledge_at_start
        OR custody_later_knowledge_and_continued_storage
      )
```

따라서 J-03의 핵심 설계는 승인하지만, `acquisition.knowledge_at_delivery`까지 분리 대상에 추가해야 합니다.

---

## J-04 운반죄의 승낙요건 중복

판정: **X — 카드를 그대로 둔 채 일부 의미만 컴파일하는 방식 반대**

> comment: `transport.consent_and_delivery`는 승낙과 현실적 수여라는 서로 다른 요건을 한 카드에 담고 있습니다. 문서도 이 카드가 공유 승낙요건과 운반 고유 행위를 함께 서술한다고 확인하고 있습니다.

카드를 그대로 평가하면서 결과만 “운반행위 LEVEL에 연결”한다고 해도, 카드의 만족 여부는 여전히 다음 두 사실에 의존합니다.

```text
승낙 존재
AND 현실적 수여 존재
```

따라서 승낙이 없고 현실적 수여만 있는 사건에서는 운반행위 자체도 불충족으로 평가될 수 있습니다. 컴파일 대상 LEVEL만 바꾸는 것으로 카드 문언의 결합조건이 제거되지는 않습니다.

반드시 분리해야 합니다.

```text
transport.actual_delivery_or_receipt
  role = component
  level = transport_act

transport.prior_possessor_consent
  role = component
  level = shared_or_transport_consensus

transport.mere_contract_insufficient
  role = assessment_standard
  또는 actual_delivery requirement의 반대 설명
```

공유 의사합치 LEVEL을 유지한다면 두 번째 카드는 공유 LEVEL과 결합하거나 중복 제거할 수 있습니다. 그러나 **원카드를 그대로 두고 승낙 문구만 무시하는 처리는 승인할 수 없습니다.**

이 카드는 기존 11장 외의 추가 분리 대상입니다.

---

## J-05 LEVEL 코드 명명

판정: **X — 전역 딕셔너리라면 unit namespace를 포함한 의미적 코드 권고**

> comment: 제안된 `L0a`, `L1a`, `L0t`, `L0c`는 현재 코드와 당장 충돌하지 않을 수 있지만, 전역 딕셔너리를 사용하는 구조에서는 다음 문제가 있습니다.

* 다른 재산죄에서 같은 접미사를 사용할 가능성
* `L0`, `L0b`, `L0i`, `L0p`가 실제 단계 순서를 표현하지 않음
* 객체 유형과 장물성 출처가 추가로 분리되면 코드 의미가 더 불명확해짐
* 디버깅·proof DAG에서 코드만 보고 요건 의미를 알기 어려움

장물죄에 namespace를 붙인 semantic code를 권고합니다.

```text
공유:
  SP_S0_SUBJECT
  SP_S1_OBJECT_TYPE
  SP_S2_STOLEN_CHARACTER
  SP_S3_KNOWLEDGE
  SP_S4_CONSENSUS
  SP_S5_CONSENSUS_TIMING

취득:
  SP_A0_ACT
  SP_A1_KNOWLEDGE_TIMING

운반:
  SP_T0_ACT
  SP_T1_KNOWLEDGE_TIMING

보관:
  SP_C0_ACT
  SP_C1_KNOWLEDGE_TIMING

양도:
  positive_path_missing

알선:
  positive_path_missing
```

`SP`는 `stolen_property`의 namespace입니다.

기존 builder가 반드시 `L숫자` 형식을 요구한다면 다음처럼 최소한 unit 접두어를 붙이는 것이 좋습니다.

```text
SP_L0S
SP_L1O
SP_L2P
SP_L3K
SP_L4C
SP_L0A
SP_L1A
SP_L0T
SP_L1T
SP_L0C
SP_L1C
```

핵심은 번호 자체보다 **전역적으로 고유하고 proof output에서 의미가 추적되는 코드**입니다.

---

## J-06 저작 파이프라인의 L6 의존성

판정: **다른 지시 — 단순 구현 참고가 아니라 구조 결함이므로 함께 수정 필요**

> comment: 역할 지정 대상 카드를 `LEVEL == L6`인지로 결정하는 구조는 이번 설계와 정면으로 충돌합니다. 문서도 LEVEL과 역할이 별개의 결정이라고 전제하고 있는데, non-component 카드를 모두 L6로 보내야 역할 지정이 반영되는 구조라면 실제 구현에서는 둘이 다시 결합되어 있습니다.

LEVEL과 role은 다음처럼 직교해야 합니다.

```text
role:
  component
  bar
  boundary
  waiver
  assessment_standard
  post_outcome
  variant

component_level:
  component 카드에만 존재
  그 밖의 역할은 null
```

권고 데이터 예시:

```json
{
  "card_id": "sec3_3.transfer.definition",
  "role": "assessment_standard",
  "component_level": null
}
```

```json
{
  "card_id": "sec3_3.acquisition.actual_possession",
  "role": "component",
  "component_level": "SP_A0_ACT"
}
```

`build_rule_ir_card_roles.py`의 역할 지정 대상 선택 기준도 다음처럼 바꾸는 것이 맞습니다.

```text
현재:
  LEVEL == L6

수정:
  explicit role mapping이 없는 카드
  또는 role_review_required == true
```

Registry audit에는 다음 검사를 추가해야 합니다.

```text
role == component
→ component_level 필수

role != component
→ component_level은 null 또는 compile_effect_scope만 보유

role이 없고 active 상태
→ activation 차단
```

모든 비-component 카드를 편의상 L6로 밀어 넣으면 다음 문제가 생깁니다.

* `assessment_standard`, `bar`, `waiver`, `post_outcome`이 동일한 법적 층으로 오인됨
* 추후 L6가 위법성·책임 단계로 다시 사용될 때 충돌
* 역할 누락 카드가 LEVEL 때문에 우연히 감지되거나 누락됨
* LEVEL 변경이 역할 변경까지 암묵적으로 일으킴

따라서 J-06은 “판단 불요”로 넘기기보다 **장물죄 원장 적재 전에 decoupling해야 하는 선행 작업**으로 보는 것이 맞습니다.

---

# 수정된 권고 LEVEL 구조

## 공유요건

| LEVEL                    | 요건              | 현재 카드 처리                                   |
| ------------------------ | --------------- | ------------------------------------------ |
| `SP_S0_SUBJECT`          | 본범 정범 이외의 적격 주체 | 일반 positive 카드 추가 필요                       |
| `SP_S1_OBJECT_TYPE`      | 재물의 객체 적격성      | `tangible_property` OR `embodied_security` |
| `SP_S2_STOLEN_CHARACTER` | 재산범죄로 영득된 장물성   | `chain_stolen_property` 등 출처 카드            |
| `SP_S3_KNOWLEDGE`        | 장물성 인식의 내용      | 실제 인식 평가 predicate 필요                      |
| `SP_S4_CONSENSUS`        | 앞선 점유자와 의사합치    | 실제 의사합치                                    |
| `SP_S5_CONSENSUS_TIMING` | 행위 당시 합치        | S4와 AND 또는 하나의 통합 predicate                |

## track 고유요건

| track       | 행위                    | 고의시점                     |
| ----------- | --------------------- | ------------------------ |
| acquisition | `SP_A0_ACT`           | `SP_A1_KNOWLEDGE_TIMING` |
| transport   | `SP_T0_ACT`           | `SP_T1_KNOWLEDGE_TIMING` |
| custody     | `SP_C0_ACT`           | `SP_C1_KNOWLEDGE_TIMING` |
| transfer    | positive path missing | positive path missing    |
| brokering   | positive path missing | positive path missing    |

운반 track에도 고의시점 LEVEL이 필요합니다. 현재 운반 카드 중에는 운반 도중 장물성을 알게 된 후 계속 운반한 경우를 다루는 법리가 있으므로, 운반행위 하나만 두고 일반 고의 LEVEL에 맡기면 시점 판단이 누락됩니다.

---

# 추가로 확인된 coverage gap

이번 LEVEL 검토를 통해 기존의 양도·알선 외에도 다음 공백이 확인됩니다.

## 1. 일반 주체 적격 positive component

`instigator_aider_subject`는 특수한 주체 가능 사례일 뿐 일반적인 제3자의 주체 적격성을 포괄하지 않습니다.

```text
missing_card_slot:
  shared component
  function: actor is not principal offender
```

## 2. 운반죄의 고의시점 positive component

현재 `transport.consent_and_delivery`만으로는 장물성 인식 및 그 시점을 증명하지 못합니다.

```text
missing_or_split_slot:
  transport knowledge at start
  OR later knowledge plus continued transport
```

## 3. 실제 장물성 인식을 나타내는 공통 factual component

`intent_and_knowledge`가 단순히 “장물죄는 고의범이다”라는 일반법리라면 실제 사건의 인식 사실을 증명하지 못합니다.

```text
missing_card_slot:
  actual awareness that property was stolen
```

이 세 공백도 registry coverage report에 표시해야 합니다.

---

# 최종 판정표

| 항목   | 판정                               |
| ---- | -------------------------------- |
| J-01 | O                                |
| J-02 | X — shared 구조 재분해                |
| J-03 | 수정 후 O — 취득·보관 카드 모두 분리          |
| J-04 | X — 카드 분리 필수                     |
| J-05 | X — namespaced semantic LEVEL 권고 |
| J-06 | 구조 수정 필요 — LEVEL과 role 분리        |

# 다음 단계 수정

문서의 다음 단계에는 “카드 11장 분리”라고 되어 있으나, 이번 검수 결과 최소한 다음 두 카드가 추가됩니다.

```text
acquisition.knowledge_at_delivery
transport.consent_and_delivery
```

따라서 고정된 11장으로 진행하지 말고:

```text
기존 분리 대상
+ acquisition.knowledge_at_delivery
+ transport.consent_and_delivery
+ 일반 주체 component coverage gap
+ 운반 고의시점 coverage gap
```

을 반영한 뒤 원장을 적재해야 합니다.

또한 작업 순서는 다음이 안전합니다.

1. LEVEL과 role의 L6 결합 제거
2. component-scoped bar 및 variant 상태 기능 확인
3. 카드 분리
4. coverage gap 등록
5. namespaced LEVEL 확정
6. 원장 적재
7. SCL 생성
8. track별 positive/negative/unsupported golden test
