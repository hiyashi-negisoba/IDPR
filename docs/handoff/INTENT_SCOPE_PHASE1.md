# intent scope 1차 검수안 (설치 전 · 승인 대기)

기준: `experiments/v2_rulebase_regen_26/` · 2026-08-16
선행: [`UNKNOWN_DIAGNOSIS.md`](UNKNOWN_DIAGNOSIS.md) → [`INTENT_SCOPE_WORKSHEET.md`](INTENT_SCOPE_WORKSHEET.md)
→ [`INTENT_SCOPE_PROPOSAL.md`](INTENT_SCOPE_PROPOSAL.md)

**설치된 변경 없음.**

앞 검수안(`INTENT_SCOPE_PROPOSAL.md`)은 33개 consumer 전부를 한 번에 일반화했다. 이 문서는
그것을 1차 범위로 줄인 것이다. 앞 문서는 폐기하지 않고 **2차 설계 기록으로 남긴다** —
보류한 13개를 나중에 열 때 거기서부터 시작한다.

**1차의 저작 변경은 0건이다.** typed metadata schema도, `intent_scope` 블록도, checker 6항목도
1차에서는 만들지 않는다.

---

## 1. 이번에 고치는 것 하나

`legal_element.intent` target이 **무엇에 대한 고의인지 지정하지 않는다.** 그것뿐이다.

폭행치상에서 지금 모델이 받는 물음은 사실상 "甲에게 고의가 있었는가"이고, 바꾸면
"甲이 **사람의 신체에 유형력을 행사한다는 사실**을 인식·용인하였는가"가 된다.
상해 결과와 그 귀속은 물음에서 빠진다.

`legal_element.intent`의 정본(canonical_meaning · legal_standard · arguments)은 불변이다.
intent target 개수도 instance당 1개 그대로다.

---

## 2. 1차 대상 경계 — 저작 없이 구조로만 정한다

scope를 실어 보내는 것은 아래 **두 조건을 모두 만족하는 offense**뿐이다.

1. `mental` slot의 predicate가 `legal_element.intent` **하나뿐**일 것
2. `linked_offender_dependency`가 **없을** 것

조건 1은 전용 mental이 어느 객관 요건을 대신 소유하는지 판정할 필요를 없앤다(존속 인식,
`injury_intent`, 목적범의 목적이 전부 여기서 걸러진다). 조건 2는 host가 계산한 법적 결론이
고의의 대상으로 섞여 들어가는 경우를 없앤다(범인은닉).

**둘 다 이미 저작에 있는 필드다.** 새로 쓰는 것도, 목록을 손으로 관리하는 것도 없다.
조건에 걸린 offense는 `assessment_scope`를 받지 않고 **현행 동작 그대로** 간다.

### 1차 20개 / 2차 보류 13개

| | offense |
|---|---|
| **1차 (20)** | `assault` · `injury` · `homicide` · `rape` · `forcible_indecency` · `quasi_rape` · `quasi_forcible_indecency` · `arson_of_occupied_structure` · `breach_of_trust` · `special_assault` · `aggravated_injury` · `special_injury` · `special_aggravated_injury` · `occupational_breach_of_trust` · `assault_causing_injury` · `assault_causing_death` · `injury_causing_death` · `arson_causing_injury` · `arson_causing_death` · `rape_causing_injury_by_aggravated_result` |
| **2차 보류 (13)** | 존속 계열 5 · 고의결합범 3(`robbery_causing_intentional_injury` · `robbery_causing_intentional_homicide` · `rape_causing_intentional_injury`) · 강도강간 계열 3 · `false_public_document_creation` · `harboring_or_escape` |

보류 13개 중 강도강간 계열 3개와 허위공문서작성은 앞 검수안 기준으로는 **override가 필요
없다고 판정된 것**이다(Q1 (a), Q2). 조건 1에 걸려 함께 보류될 뿐이므로, 2차에서 저작 없이
바로 편입될 수 있다.

---

## 3. scope 산출 규칙 — 둘뿐

| | 규칙 | 근거 |
|---|---|---|
| **R1** | scope = owning offense의 객관 slot(`subject`·`object`·`conduct`·`result`·`causation`·`circumstance`) leaf 전체 | 제13조 "죄의 성립요소인 사실" |
| **R2** | 가중결과 component에서**만** 기여한 leaf 제외. base component가 함께 기여하면 잔류 | 제15조 제2항 |

R2의 가중측 판정은 `derivation.components` 중 `primitive.aggravated_result_attribution`가 있는
composition에서 `kind: offense` component를 base로 두고 나머지 기여분을 가중측으로 본다.
`local_key` 문자열은 보지 않는다.

앞 검수안의 R3(host-resolved 제외)는 **1차에 필요 없다.** 그 규칙이 필요한 유일한 죄가
범인은닉이고, 조건 2로 이미 보류되기 때문이다.

### 산출 결과 — 1차 20개 중 실제로 물어진 것

| offense | intent scope | 제외 |
|---|---|---|
| `assault` 폭행 **(U 8/9)** | 유형력 행사 · 자연인 타인 | — |
| `injury` 상해 **(U 7/9)** | 상해 수단 행위 · 상해 결과 · 자연인 타인 | — |
| `assault_causing_injury` 폭행치상 **(U 6/8)** | 유형력 행사 · 자연인 타인 | `injury_result` · `aggravated_result_attribution` |
| `rape` 강간 (U 2/3) | 강간죄 객관 6개 | — |
| `rape_causing_injury_by_aggravated_result` 강간치상 | 강간죄 객관 6개 | `injury_conduct` · `injury_result` · `aggravated_result_attribution` |
| `homicide` 살인 | 살해행위 · 사망 · 인과관계 · 자연인 타인 | — |
| `arson_of_occupied_structure` 방화 | 현주건조물 객체 · 독립연소 | — |
| `quasi_rape` 준강간 | 준강간죄 객관 3개 | — |
| `breach_of_trust` 배임 | 배임죄 객관 3개 | — |

상해치사·방화치사 등 나머지 11개는 이번 실행에서 intent가 물어지지 않았으나 규칙은 같다.
상해치사에서 `injury_result`가 잔류하고 `death_of_victim`이 빠지는 것도 R2가 처리한다.

---

## 4. 실측 커버리지

`intent` asked 42 · UNKNOWN 28 중,

```
1차 대상      asked 34   TRUE 11   FALSE 0   UNKNOWN 23
2차 보류      asked  8   TRUE  3   FALSE 0   UNKNOWN  5
```

**UNKNOWN 28건 중 23건(82%)이 1차로 덮인다.** 지목한 세 죄(폭행 8 · 상해 7 · 폭행치상 6 =
21건)에 강간 2건이 더해진 것이다. 보류 13개가 안고 가는 UNKNOWN은 5건뿐이고, 그 5건은
현행 동작 그대로이므로 이번 재측정에서 **대조군 역할**을 한다 — 1차 대상만 움직이고
보류군이 그대로면 변화의 원인이 scope라는 근거가 된다.

---

## 5. payload와 문안 전문

### 5.1 payload

scope는 `predicate_catalog`가 아니라 **target에 실린다.** catalog는 predicate당 하나여서 폭행과
폭행치상이 같은 shard에 오면 구분할 수 없다([grounding.py:391-410](../../src/idpr/v2/runtime/grounding.py#L391-L410)).

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

제외된 leaf는 payload에 싣지 않는다. "이것은 판단하지 마라"를 명시하면 그 사실이 오히려
증거로 읽힌다.

어떤 predicate가 scope를 받는지는 runtime에 ref를 박지 않고 정의가 선언한다. 정본 문안은
그대로 두고 필드 하나만 더한다.

```yaml
- id: legal_element.intent
  # canonical_meaning · legal_standard · arguments · authority_refs 전부 그대로
  assessment_scope_source: objective_elements   # 신규, 현재 이 predicate 하나만 사용
```

### 5.2 system prompt 추가 문안 — 전문

[`prompts/v2_call2_grounding.md`](../../prompts/v2_call2_grounding.md)의 LegalElement 관련 줄
바로 아래에 넣는다. **기존 줄은 삭제·수정하지 않는다.**

```text
- LegalElement target에 `assessment_scope`가 있으면, `included`에 열거된 사실만 인식·용인의
  대상이다. 열거되지 않은 사실은 이 target에서 판단하지 않으며, 그것이 발생했는지 여부는
  이 target의 값에 영향을 주지 않는다.
- `included` 전부에 대해 행위자의 인식·용인이 carrier에서 확인되거나 필연적으로 도출되면
  TRUE다. `included` 중 어느 하나라도 행위자가 인식하지 못하였거나 용인하지 않았음이
  carrier에서 직접 확인되면 FALSE다. 어느 쪽도 확정할 수 없으면 UNKNOWN이다.
- `included`의 각 항목은 그 `canonical_meaning`이 가리키는 사실에 대한 인식을 묻는 것이다.
  행위자가 그 사실의 법적 성질이나 죄명을 알았는지는 묻지 않는다.
- `assessment_scope`가 없는 LegalElement target은 종전과 같이 판단한다.
```

세 번째 줄은 범인은닉을 보류한 뒤에도 남긴다. 1차 대상에도 규범적 색채가 있는 요건이
있기 때문이다(`arson_target_status`의 현주건조물 해당성, `possession`의 점유 등). 넷째 줄이
보류 13개의 현행 동작을 보장한다.

둘째 줄은 **FALSE 경로를 처음으로 명시**한다. mental 자리 100건에서 FALSE가 0이었던 것과
직접 맞물린다.

### 5.3 모델이 실제로 보게 되는 것 — 폭행치상

```text
[predicate_catalog]  ← 정본, 변경 없음
  predicate_ref: legal_element.intent
  canonical_meaning: 객관적 구성요건요소 인식+실현 용인(고의)
  legal_standard: 행위자가 구성요건적 사실을 인식하고 그 실현을 의욕하거나 용인하였는지 여부

[assessment_targets[k]]
  instance_key: {甲, derived_offense.assault_causing_injury, realization:001}
  predicate_ref: legal_element.intent
  assessment_scope.included:
    - 출생 후 사망하지 않은 자연인, 타인
    - 사람의 신체에 대한 유형력 행사
```

---

## 6. 변경 범위

| 대상 | 변경 |
|---|---|
| `legal_elements.yaml` | `legal_element.intent`에 `assessment_scope_source` 1줄 |
| `offenses.yaml` · `derived_offenses.yaml` | **없음** |
| compile/planner | 객관 leaf 수집 + R1·R2, 1차 조건 판정, scope를 target에 적재 |
| `grounding.py` | `AssessmentTarget`에 optional scope, payload 직렬화 |
| `prompts/v2_call2_grounding.md` | 4줄 추가 (기존 줄 불변) |
| tests | 1차 조건 판정 골든(20/13 분할), R2 산출 골든(결과적 가중범 8개), scope 없는 target 불변 |

신규 predicate 0개 · 정본 문안 변경 0건 · **저작(yaml element) 변경 0건** · intent target 수 변화 없음.

---

## 7. 2차로 넘긴 것

승인 후 별도 검수 항목으로 남긴다. 지금 gap으로 등록하지는 않는다(그 자체가 저작이므로).

1. **존속 계열 5** — `awareness_of_lineal_ascendant_status`가 소유하는 leaf 제외. delegated marker 필요
2. **고의결합범 3** — component 단위 위임(`injury_intent`→`injury_part` 등). delegated marker 필요
3. **강도강간 계열 3 · 허위공문서작성** — marker 불필요. 조건 1만 완화하면 편입
4. **범인은닉** — circumstance의 주관적 요소·보증인 지위 제외, host-resolved 제외(R3),
   `act_directed_at_another_offender`의 사실적 렌더링. 이번 검수에서 가장 논점이 많았던 건

설계 초안은 [`INTENT_SCOPE_PROPOSAL.md`](INTENT_SCOPE_PROPOSAL.md) §2·§3에 그대로 있다.

---

## 8. 재측정 계약

frozen baseline `planned 635 / asked 595 / TRUE 286 / FALSE 21 / UNKNOWN 288`.

* **1차 대상군**(asked 34 · U 23)과 **보류군**(asked 8 · U 5)을 나눠서 본다.
  보류군이 함께 움직이면 원인이 scope가 아니다.
* mental 자리 전체 100건의 TRUE/FALSE/UNKNOWN 이동을 본다. 특히 **FALSE가 0에서 움직이는지**.
* 기존 TRUE 286 · FALSE 21의 후퇴를 먼저 확인한다. `assault_conduct` 17/17 TRUE처럼 손대지
  않은 predicate가 움직이면 저작이 아닌 다른 것이 바뀐 것이다.
* 결과적 가중범에서 intent가 TRUE였던 3건을 개별 추적한다. 중한 결과 고의로 읽히고 있었다면
  일부는 **FALSE 또는 UNKNOWN으로 바뀌는 것이 정상**이다.
* asked 분모가 변하면 비율 비교를 중단하고 분모부터 설명한다.

---

## 9. 승인을 구하는 항목

1. §2 **1차 경계 조건 두 개**(mental이 intent 단독 · linked_offender_dependency 없음)와 20/13 분할
2. §5.1 **`assessment_scope_source` 선언 방식**(runtime 상수 대신 정의가 선언)
3. §5.2 **prompt 추가 4줄 전문**
