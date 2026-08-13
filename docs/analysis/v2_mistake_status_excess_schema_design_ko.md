# 착오·제33조 단서·공범의 초과 스키마 설계안

각 항목 끝에 `> 검수:` 로 판정해 주시면 됩니다. YAML 저작은 스키마 확정 후에 합니다.
지금 저작하면 스키마 검증에서 전부 거부되므로 순서를 바꿀 수 없습니다.

## 0. 왜 기존 축에 못 얹는가

| 항목 | 시도 가능한 기존 축 | 왜 안 되는가 |
|---|---|---|
| 착오 | `DoctrineDef` | `stage`가 위법성·책임·처벌조건 3개뿐. 착오의 효과는 **고의 조각**이라 Elements 단계다. DEFEAT를 위법성에 걸면 효과 지점이 어긋난다 |
| 제33조 단서 | `participation_constraints.constitutive_status_refs` | 본문 전용이다. 본문은 비신분자가 신분자의 죄를 **같이** 실현하는 구조인데, 단서는 가담자가 정범과 **다른 죄**(존속살해)를 성립시킨다 |
| 공범의 초과 | `participation_policy.modes` | 스키마가 `additionalProperties: false`에 modes 4개 고정. 그리고 초과는 mode가 아니라 **교사 내용과 실현 죄의 비교**다 |

---

## 1. 착오 (9문항)

### 1.1 문제

현재 `legal_element.intent`는 단일 predicate다. 甲이 乙을 상해하려다 C를 乙로 오인해
C를 상해한 경우, Call 2는 "C에 대한 상해의 고의"를 묻고 모델은 자연스럽게 FALSE를 낸다.
甲은 C를 해칠 생각이 없었기 때문이다. 법정적 부합설에 따르면 답은 고의기수 인정이다.

즉 **사실(불일치)과 규범(부합설)이 한 predicate에 뭉쳐 있는 것**이 원인이다.

### 1.2 제안: 두 층으로 분리

**층 1 — 사실.** 인식 대상과 발생 대상의 불일치를 relation으로 표현한다.
`relations.yaml`의 기존 3개와 같은 형식이고, `evaluation: structural`이다.
host가 binding에서 확인할 수 있으므로 뉴럴 호출이 늘지 않는다.

```yaml
- id: relation.intended_object_divergence
  left_type: entity      # 행위자가 인식·의도한 대상
  right_type: entity     # 실제로 결과가 발생한 대상
  evaluation: structural
  canonical_meaning: 행위자가 인식한 대상과 결과가 발생한 대상이 다른 관계
  legal_standard: 행위 당시 행위자가 향하고자 한 대상과 결과가 귀속된 대상이 동일인이 아닌지 여부
```

**층 2 — 유형.** 객체의 착오와 방법의 착오를 가르는 predicate 1개.
이건 사실 판단이라 Call 2가 답할 수 있다.

```yaml
- id: legal_element.object_misidentification
  arguments: [{name: actor, type: entity}, {name: object, type: entity}]
  canonical_meaning: 행위자가 대상 자체를 다른 사람·물건으로 잘못 알아본 경우
  legal_standard: 행위자가 목표한 대상 그 자체를 오인하였는지(객체의 착오),
    아니면 목표는 옳게 인식하였으나 실행이 빗나가 다른 대상에 결과가 발생하였는지(방법의 착오)
  authority_refs: [{authority_basis: statute_text, citation: 형법 제13조}]
```

**층 3 — 규범.** 부합설 선택을 **명시적으로 저작한 규칙**으로 둔다. 여기가 핵심이다.

```yaml
# 신설 kind: mistake_policy
- id: mistake_policy.concrete_fact_statutory_conformity
  scope: same_statutory_offense      # 동일 구성요건 내 불일치에만 적용
  divergence_relation: relation.intended_object_divergence
  doctrine_choice: 법정적 부합설
  effect:
    object_misidentification: intent_preserved   # 객체의 착오 -> 발생사실 고의기수
    method_divergence: intent_preserved          # 방법의 착오 -> 판례·다수설 동일 결론
  authority_refs:
    - {authority_basis: commentary_reported_precedent, citation: 대법원 1984. 1. 24. 선고 83도2813}
```

효과가 `intent_preserved`면 런타임이 `legal_element.intent`를 FALSE로 접지 않고 유지한다.
**host가 고의를 만들어내는 게 아니라, 저작된 학설 선택을 적용**하는 것이다.

> 검수 ①-a: 학설을 이렇게 **저작물로 고정**하는 게 맞습니까, 아니면 Call 3에서 학설
> 대립을 서술하게 두고 심볼릭은 unresolved로 남기는 게 맞습니까?
> (루브릭은 대립 서술을 요구하므로 후자도 근거가 있습니다.)

> 검수 ①-b: `effect`를 구성요건 부합설·구체적 부합설로 바꿔 끼울 수 있게 두었습니다.
> 방법의 착오에서 구체적 부합설은 결론이 달라지는데, 이 축이 필요합니까?

### 1.3 위법성조각사유의 전제사실에 관한 착오 (위전착)

`r12_p1_q2`(오상승낙), `r14_p2_q4`(적법성의 착오)가 여기다. 위 층과 구조가 다르다.
행위자가 **위법성조각사유의 사실적 전제**를 오인한 것이므로, 판례는 `정당한 이유` 유무로
갈린다.

```yaml
- id: doctrine.mistaken_justifying_circumstance
  stage: culpability
  requires:
    op: all
    args:
      - {op: ref, ref: legal_element.belief_in_justifying_circumstance}
      - {op: ref, ref: legal_element.justifiable_ground_for_mistake}   # 기존 재사용
  effect: {effect: DEFEAT, stage: culpability}
```

`legal_element.justifiable_ground_for_mistake`는 `doctrine.mistake_of_law_defeat`가 이미
쓰는 것을 **그대로 재사용**한다. 조문별로 재정의하지 않는다.

> 검수 ①-c: 판례(정당한 이유설)를 따르면 위전착은 책임 단계에서 처리하는 게 맞습니다.
> 다만 제한적 책임설을 따르면 고의가 조각되어 Elements 단계입니다. 어느 쪽으로 고정할까요?

---

## 2. 제33조 단서 (2문항: `r12_p2_q1_ga`, `r14_p1_q1`)

### 2.1 문제

甲(직계비속)이 乙에게 甲의 아버지 살해를 교사했다. 乙은 보통살인, 甲은 **존속살해교사**다.
현재 derivative mode는 `requires_conclusion: offense_realization`으로 **정범이 실현한 그 죄**에
고정되어 있다. 가담자가 정범보다 무거운 다른 죄를 지는 경로가 구조적으로 없다.

### 2.2 제안

`OffenseDef.participation_constraints`에 축 하나를 추가한다.
가감적 신분자가 가담했을 때 어느 죄로 올라가는지를 **가중죄 쪽에** 저작한다.

```yaml
- id: offense.ancestral_homicide
  participation_constraints:
    aggravating_status_participation:          # 형법 제33조 단서
      base_offense_ref: offense.homicide       # 정범이 실현한 죄
      status_ref: legal_element.lineal_ascendant_of_self_or_spouse_status
      applies_to_modes: [instigator, aider, co_principal]
```

런타임 의미: 정범이 `offense.homicide`를 실현했고, 가담자 본인에게 `status_ref`가 TRUE면,
가담자의 죄책은 `offense.ancestral_homicide`의 해당 mode로 성립하고 그 형으로 처벌한다.
가담자에게 status가 FALSE/UNKNOWN이면 아무 일도 일어나지 않는다.

> 검수 ②-a: 제33조 단서는 **성립과 과형을 동시에** 결정한다는 판례 취지를 반영해
> 성립 자체를 존속살해교사로 올렸습니다. 성립은 보통살인교사, 과형만 존속살해로 보는
> 견해도 있는데 어느 쪽으로 저작할까요?

> 검수 ②-b: `applies_to_modes`에 `co_principal`을 넣었습니다. 단서가 공동정범에도
> 적용되는지 다툼이 있는데 빼는 게 맞습니까?

---

## 3. 공범의 초과 (4문항)

### 3.1 문제

甲이 절도를 교사했는데 乙이 특수절도를 했다(양적 초과) / 폭행치상까지 했다(질적 초과).
현재 참여 표현에는 "甲이 乙을 교사했다"는 있어도 **"무엇을 교사했다"가 없다.**
비교 대상이 없으니 초과 판정이 불가능하다.

### 3.2 제안

두 가지가 필요하다.

**(1) 교사·공모의 내용을 typed로 보존.** 이건 Call 1.5-P가 이미 뽑는
`request_or_instruction` interaction에 offense 축을 더하는 게 아니라 — 그러면 Call 1.5-P가
법적 판단을 하게 된다 — host가 **교사자에게 열린 offense binding**을 그대로 쓴다.

```text
甲의 instigator 후보 = (甲 -> 乙, offense.theft)      # Call 1이 甲에게 연 seed
乙의 정범 성립      = derived_offense.special_theft   # 실제 실현
                     offense.assault_causing_injury
```

**(2) 초과 판정 규칙.** 두 죄의 관계로만 결정하므로 뉴럴 호출이 필요 없다.

```yaml
# 신설 kind: excess_policy (단일 정책, 죄명별 저작 아님)
- id: excess_policy.standard
  quantitative:                # 양적 초과
    condition: realized_offense_derives_from_instigated_offense
    effect: liable_for_instigated_offense_only
  qualitative:                 # 질적 초과
    condition: realized_offense_shares_no_derivation_with_instigated_offense
    effect: no_liability_for_excess
```

`realized_offense_derives_from_instigated_offense`는 이미 있는 `derivation.base` 사슬로
판정된다. 절도→특수절도는 qualify 관계이므로 양적 초과, 절도→폭행치상은 무관하므로
질적 초과다. **host가 텍스트를 해석하지 않는다.**

> 검수 ③-a: 양적/질적을 derivation 사슬 유무로 가르는 게 법적으로 충분합니까?
> 강도 교사에 살인이 실현된 경우처럼 사슬은 없지만 결과적 가중범 관계가 있는 사안이
> 걱정됩니다.

> 검수 ③-b: 양적 초과에서 통설은 "교사한 범위 내 책임"인데, 결과적 가중범의
> 예견가능성이 있으면 중한 죄의 교사가 된다는 견해도 있습니다. 어느 쪽입니까?

---

## 4. 저작하지 못한 것

**불가벌적 사후행위 (`r10_p2_q1`)** — 장물죄가 v2에 저작되어 있지 않습니다.
"장물보관죄 성립 후 횡령은 불가벌적 사후행위"라는 흡수 규칙은 pair의 한 축이 없어
저작이 불가능합니다. 장물죄 저작이 선행조건입니다.

**`r13_p2_q1`** — 확인해 보니 규칙이 필요 없습니다. 루브릭이 요구하는 것은
① 절취 카드 사용 사기죄는 불가벌적 사후행위가 **아니다**(= 흡수 규칙 부재가 곧 정답)와
② 본범의 장물취득죄 불성립(= 장물죄 미저작이라 애초에 후보가 생기지 않음)입니다.
현재 상태로 둘 다 맞습니다.
