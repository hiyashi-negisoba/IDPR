# `intent_scope` 검수안 (설치 전 · 승인 대기)

기준: `experiments/v2_rulebase_regen_26/` · 2026-08-16
선행: [`UNKNOWN_DIAGNOSIS.md`](UNKNOWN_DIAGNOSIS.md) mode B → [`INTENT_SCOPE_WORKSHEET.md`](INTENT_SCOPE_WORKSHEET.md)
확정된 판정: Q1 (a) · Q2 제한 승인 · Q3 (b) · Q4 제외 · Q5 선택적 제외 · Q6 잔류 · 하이브리드 방향

**설치된 변경 없음.** 이 문서는 ① typed metadata schema와 실제 필요한 consumer 목록,
② scope-aware payload와 **모델이 실제로 보는 문안 전문** 두 덩어리다.

`legal_element.intent`의 정본(canonical_meaning · legal_standard)은 **한 글자도 바꾸지 않는다.**
바뀌는 것은 use-site가 "죄의 성립요소인 사실"을 target별로 확정해 주는 것뿐이다.

---

## 0. 워크시트에서 정정할 것 두 가지

**① Q4는 override가 필요 없다.** 지시한 provenance 규칙(가중측에서만 기여한 leaf를 제외,
base가 함께 기여하면 잔류)을 그대로 구현해 결과적 가중범 8개 전부에 돌렸다. 강간치상의
`ground_fact.injury_conduct`는 가중측(`exported_component.injury_conduct`)에서만 기여하고
base인 `offense.rape` 쪽 기여가 없어서 **자동으로 빠진다.** 워크시트가 "authored override가
필요한 반례"라고 적은 것은 `local_key` 관례에 묶여 있을 때의 이야기였고, 관례를 provenance로
바꾸면 사라진다. Q6의 잔류도 같은 규칙 하나로 함께 성립한다 — 상해치사의 `injury_result`와
방화치사의 `burning_result`는 base 기여가 있어 잔류한다.

**② 자동 규칙이 하나 더 필요하다(신규, 승인 요청).** 범인은닉죄의 object slot은
`legal_element.offender_status_of_object`인데, 이것은 A1이 계산하는 **host-resolved legal
result**다(`linked_offender_dependency.resolved_element`). 이것을 scope에 남기면 "대상자가
벌금 이상의 죄를 범한 자라는 **법적 결론**을 인식했는가"를 묻게 되어, 지적한 금지사항에
정확히 해당한다. 이미 planner가 같은 필드를 근거로 이 요건을 질문 대상에서
빼고 있으므로([evaluation_instance_planner.py:447-449](../../src/idpr/v2/runtime/evaluation_instance_planner.py#L447-L449)),
scope 산출도 **같은 저작 필드를 재사용**해 자동 제외한다. 새 저작이 필요 없다.

> comment:

---

## 1. 자동 규칙 (metadata 없이 적용)

| | 규칙 | 근거 |
|---|---|---|
| **R1** | 기본 scope = owning offense의 객관 slot(`subject`·`object`·`conduct`·`result`·`causation`·`circumstance`) leaf 전체 | 제13조의 "죄의 성립요소인 사실" |
| **R2** | 가중결과 component에서**만** 기여한 leaf 제외. base component가 함께 기여하면 잔류 | Q4·Q6. 제15조 제2항 |
| **R3** | `linked_offender_dependency.resolved_element` 제외 | §0② |

R2의 가중측 판정은 `derivation.components` 중 `primitive.aggravated_result_attribution`가
있는 composition에서, `kind: offense`인 component를 base로 두고 나머지(primitive ·
exported_component) 기여분을 가중측으로 본다. **`local_key` 문자열은 보지 않는다.**

이 세 규칙만으로 consumer 33개 중 **24개가 확정된다.**

---

## 2. `intent_scope` typed metadata — schema

R1~R3으로 유도할 수 없는 것만 저작한다. **24개 자동 case에는 쓰지 않는다.**

```yaml
# offenses.yaml / derived_offenses.yaml 의 use-site에 선택적으로 추가
intent_scope:
  exclude:
    - leaf: <predicate ref>            # leaf 와 component 중 정확히 하나
      component: <local_key>           #
      reason: delegated_to_specific_mental | non_objective_requirement
      owner_ref: <mental predicate ref>  # reason=delegated 일 때만, 필수
```

**제시한 형태에서 하나 좁혔다.** `ref_or_component` 한 필드 대신 `leaf:` / `component:`를
두고 정확히 하나만 허용한다. 다형 필드는 checker가 "이 문자열이 leaf인가 local_key인가"를
추론해야 하고, 그 추론이 두 번째 권위가 되기 때문이다.

`reason`은 두 값뿐이다. `aggravated_result`는 R2가 자동으로 하므로 **저작 값에 넣지 않는다** —
넣을 수 있게 두면 자동 규칙과 저작이 같은 일을 두 곳에서 하게 된다.

### checker가 강제할 것 (신규 test)

1. `leaf` / `component` 중 정확히 하나. 둘 다 또는 둘 다 아님은 실패.
2. `leaf`는 그 offense의 객관 slot에 **실재**해야 한다. 없으면 실패 — 저작이 낡아 조용히
   무효가 되는 것을 막는다.
3. `component`는 그 offense의 `derivation.components`의 `local_key`여야 한다.
4. `reason: delegated_to_specific_mental`이면 `owner_ref` 필수이고, 그 ref는 **같은 offense의
   `mental` slot에 실재**해야 한다.
5. `reason: non_objective_requirement`에는 `owner_ref`를 쓸 수 없다.
6. R2·R3가 이미 제외하는 leaf를 다시 저작하면 실패(중복 권위 금지).

---

## 3. metadata가 실제로 필요한 consumer — 9개

나머지 24개는 저작하지 않는다.

### 3.1 `delegated_to_specific_mental` — 존속 계열 5개

`awareness_of_lineal_ascendant_status`가 존속성이라는 객관적 가중사실의 **인식을 명시적으로
소유**한다. 제15조 제1항의 구조 그대로다.

```yaml
# offense.ancestral_homicide / offense.ancestral_injury
# derived_offense.aggravated_ancestral_injury
# derived_offense.special_ancestral_injury
# derived_offense.special_aggravated_ancestral_injury
intent_scope:
  exclude:
    - leaf: legal_element.lineal_ascendant_of_self_or_spouse_status
      reason: delegated_to_specific_mental
      owner_ref: legal_element.awareness_of_lineal_ascendant_status
```

`false_public_document_creation`은 **저작하지 않는다.** `purpose_to_use_as_genuine`는 제227조의
초과주관적 목적이지 어떤 객관 leaf의 인식을 대신 소유하는 predicate가 아니다(Q2 확정).
`unlawful_appropriation_intent`·`purpose_to_*` 계열도 같은 이유로 전부 저작 대상이 아니다.

### 3.2 `delegated_to_specific_mental` — 고의결합범 3개

component 단위 위임이다.

```yaml
# derived_offense.robbery_causing_intentional_injury
intent_scope:
  exclude:
    - component: injury_part
      reason: delegated_to_specific_mental
      owner_ref: legal_element.injury_intent

# derived_offense.rape_causing_intentional_injury  → 위와 동일

# derived_offense.robbery_causing_intentional_homicide
intent_scope:
  exclude:
    - component: homicide_part
      reason: delegated_to_specific_mental
      owner_ref: legal_element.homicide_intent
```

강도강간·특수강도강간·준강도강간 3개는 **저작하지 않는다.** `unlawful_appropriation_intent`는
취거·재물·폭행협박의 인식을 대체하지 않으므로(Q3 확정), generic intent가 강도 부분과 강간
부분을 함께 진다. Q1 (a)에 따라 하나의 명제로 둔다.

### 3.3 `non_objective_requirement` — 범인은닉·도피 1개

```yaml
# offense.harboring_or_escape
intent_scope:
  exclude:
    - leaf: legal_element.for_the_offenders_benefit
      reason: non_objective_requirement
    - leaf: legal_element.omission_requires_guarantor_status
      reason: non_objective_requirement
```

`offender_status_of_object`는 R3가 자동으로 뺀다. `act_directed_at_another_offender`는 잔류하며,
§5의 렌더링 계약이 "법적 결론이 아니라 사실"을 묻도록 강제한다.

---

## 4. 산출되는 scope — 이번 실행에서 intent가 물어진 죄 전부

`+` 포함 · `−` 제외(사유). UNKNOWN 상위 3개가 전부 자동 case다.

| offense | intent scope | 제외 |
|---|---|---|
| `assault` 폭행 **(U 8/9)** | `assault_conduct` · `natural_person_victim_status` | — |
| `injury` 상해 **(U 7/9)** | `injury_conduct` · `injury_result` · `natural_person_victim_status` | — |
| `assault_causing_injury` 폭행치상 **(U 6/8)** | `assault_conduct` · `natural_person_victim_status` | `injury_result`, `aggravated_result_attribution` [R2] |
| `harboring_or_escape` 범인은닉 (U 4/4) | `concealment_or_escape_conduct` · `act_directed_at_another_offender` | `offender_status_of_object` [R3], `for_the_offenders_benefit`·`omission_requires_guarantor_status` [저작] |
| `rape` 강간 (U 2/3) | 강간죄 객관 6개 전부 | — |
| `homicide` 살인 | `killing_conduct` · `death_of_victim` · `result_causation` · `natural_person_victim_status` | — |
| `ancestral_homicide` 존속살해 | `killing_conduct` · `death_of_victim` · `result_causation` | `lineal_ascendant_status` [저작] |
| `arson_of_occupied_structure` 방화 | `arson_target_status` · `burning_result` | — |
| `rape_causing_injury_by_aggravated_result` 강간치상 | 강간죄 객관 6개 | `injury_conduct`·`injury_result`·`aggravated_result_attribution` [R2] |
| `robbery_causing_intentional_injury` 강도상해 | `taking_conduct` · `possession` · `robbery_level_violence` | `injury_part` 기여 3개 [저작] |
| `robbery_causing_intentional_homicide` 강도살인 | `taking_conduct` · `possession` · `robbery_level_violence` | `homicide_part` 기여 4개 [저작] |
| `quasi_rape` 준강간 | 준강간죄 객관 3개 | — |
| `breach_of_trust` 배임 | 배임죄 객관 3개 | — |
| `false_public_document_creation` 허위공문서작성 | 허위공문서작성죄 객관 3개 | — |

폭행치상이 목표한 모습이 되었다 — **상해 결과와 그 귀속이 고의 대상에서 빠지고 폭행
사실만 남는다.**

---

## 5. Call 2 payload와 문안 전문

### 5.1 payload 확장

scope는 `predicate_catalog`가 아니라 **target에 실린다.** catalog는 predicate당 하나여서 폭행과
폭행치상이 같은 shard에 오면 구분할 수 없기 때문이다([grounding.py:391-410](../../src/idpr/v2/runtime/grounding.py#L391-L410)).

```json
{
  "instance_key": {
    "case_id": "...", "actor_id": "甲",
    "offense_ref": "derived_offense.assault_causing_injury",
    "occurrence_id": "realization:001"
  },
  "predicate_ref": "legal_element.intent",
  "assessment_scope": {
    "owner_offense_ref": "derived_offense.assault_causing_injury",
    "included": [
      {"ref": "legal_element.natural_person_victim_status",
       "canonical_meaning": "출생 후 사망하지 않은 자연인, 타인"},
      {"ref": "legal_element.assault_conduct",
       "canonical_meaning": "사람의 신체에 대한 유형력 행사"}
    ]
  }
}
```

제외된 leaf는 **payload에 싣지 않는다.** "이것은 판단하지 마라"를 명시하면 그 사실이 오히려
증거로 읽힌다.

어떤 predicate가 scope를 받는지는 runtime에 ref를 박지 않고 정의가 선언한다. `legal_element.intent`
정의에 필드 하나만 더한다(정본 문안은 불변).

```yaml
- id: legal_element.intent
  # canonical_meaning · legal_standard · arguments · authority_refs 전부 그대로
  assessment_scope_source: objective_elements   # 신규, 현재 이 predicate 하나만 사용
```

> comment: (runtime 상수로 박지 않고 정의가 선언하는 이 방식이 맞는지)

### 5.2 system prompt에 추가되는 문안 — 전문

[`prompts/v2_call2_grounding.md`](../../prompts/v2_call2_grounding.md)의 LegalElement 관련 줄
바로 아래에 아래 네 줄을 넣는다. **기존 줄은 삭제·수정하지 않는다.**

```text
- LegalElement target에 `assessment_scope`가 있으면, `included`에 열거된 사실만 인식·용인의
  대상이다. 열거되지 않은 사실은 이 target에서 판단하지 않으며, 그것이 발생했는지 여부는
  이 target의 값에 영향을 주지 않는다.
- `included` 전부에 대해 행위자의 인식·용인이 carrier에서 확인되거나 필연적으로 도출되면
  TRUE다. `included` 중 어느 하나라도 행위자가 인식하지 못하였거나 용인하지 않았음이
  carrier에서 직접 확인되면 FALSE다. 어느 쪽도 확정할 수 없으면 UNKNOWN이다.
- `included`의 각 항목은 그 `canonical_meaning`이 가리키는 **사실**에 대한 인식을 묻는
  것이다. 행위자가 그 사실의 법적 성질이나 죄명을 알았는지는 묻지 않는다.
- `assessment_scope`가 없는 LegalElement target은 종전과 같이 판단한다.
```

세 번째 줄이 Q5의 렌더링 계약이다. 둘째 줄은 **FALSE 경로를 처음으로 명시**한다 — mental
자리 100건에서 FALSE가 0이었던 것과 직접 맞물린다.

### 5.3 모델이 실제로 보게 되는 것 — 폭행치상 실물

```text
[predicate_catalog]  ← 정본, 변경 없음
  predicate_ref: legal_element.intent
  kind: legal_element
  canonical_meaning: 객관적 구성요건요소 인식+실현 용인(고의)
  legal_standard: 행위자가 구성요건적 사실을 인식하고 그 실현을 의욕하거나 용인하였는지 여부
  arguments: [actor, act]
  evidence_scope: offense_realization

[assessment_targets[k]]
  instance_key: {甲, derived_offense.assault_causing_injury, realization:001}
  predicate_ref: legal_element.intent
  assessment_scope.included:
    - 출생 후 사망하지 않은 자연인, 타인
    - 사람의 신체에 대한 유형력 행사
```

즉 모델이 받는 물음은 이제 "甲에게 고의가 있었는가"가 아니라 **"甲이 타인의 신체에 유형력을
행사한다는 사실을 인식·용인하였는가"**다. 상해 결과와 그 귀속은 물음에 없다.

### 5.4 건드리지 않는 것

* `legal_element.intent`의 canonical_meaning · legal_standard · arguments — 불변
* intent target의 개수 — instance당 1개 유지(Q1 (a)). symbolic conjunction 변경 없음
* `mistake_policy.korean_law_concrete_fact.probe.requires`가 소비하는 intent truth의 identity —
  불변. 착오 정책은 종전과 같은 truth를 읽는다
* 다른 predicate의 payload — `assessment_scope` 없는 target은 종전 그대로

---

## 6. 변경 범위 요약

| 대상 | 변경 |
|---|---|
| `legal_elements.yaml` | `legal_element.intent`에 `assessment_scope_source` 1줄 |
| `offenses.yaml` | 3개 offense에 `intent_scope` 블록 |
| `derived_offenses.yaml` | 6개 derived offense에 `intent_scope` 블록 |
| compile/planner | 객관 leaf 수집 + R1~R3 + override 적용, scope를 target에 적재 |
| `grounding.py` | `AssessmentTarget`에 optional scope, payload 직렬화 |
| `prompts/v2_call2_grounding.md` | 4줄 추가 (기존 줄 불변) |
| tests | §2 checker 6항목 + scope 산출 골든 |

신규 predicate **0개**, 정본 문안 변경 **0건**, intent target 수 변화 **없음**.

---

## 7. 승인을 구하는 항목

1. §0② **R3 신설**(host-resolved element 자동 제외) — 새 저작 없이 기존 필드 재사용
2. §2 **`leaf:`/`component:` 분리** — 제시한 `ref_or_component` 다형 필드에서 좁힌 것
3. §2 `reason`에서 **`aggravated_result` 값을 빼는 것** — R2가 자동이므로 저작 대상 아님
4. §3 **metadata 9개 consumer 목록**이 이것으로 맞는지(24개는 저작하지 않음)
5. §5.1 **`assessment_scope_source` 선언 방식**
6. §5.2 **prompt 추가 4줄 전문**

승인되면 설치하고, [`INTENT_SCOPE_WORKSHEET.md`](INTENT_SCOPE_WORKSHEET.md) §6의 재측정
계약대로 frozen baseline `635/595/286/21/288` 대비 회귀까지 확인한다.
