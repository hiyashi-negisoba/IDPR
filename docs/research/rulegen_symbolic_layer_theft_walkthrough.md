# 절도죄로 본 symbolic layer — 카드에서 Scallop까지

작성일: 2026-07-26 · 대상: `theft` 단위(카드 66 / 술어 151 / 규칙 308 / Scallop 2,700줄)
산출물: `data/rulegen/property/rule_ir/theft_rule_ir_candidate.json` ·
`rules/generated/property_theft_v1_candidate.scl`

목적은 하나다 — **symbolic layer가 완료되었는지 판단할 수 있게** 한 죄명의 전 경로를 실제 산출물로
보인다. 아래 모든 코드는 조립된 파일에서 그대로 떠 온 것이고 설명용으로 새로 쓴 것이 아니다.

---

## 1. 카드 한 장이 무엇이 되는가

카드 `art329_sec3_1.taking_transfer_of_control`을 따라간다.

**주석서 원문** (`comm_001692_제329조_Ⅲ.1_13`)
> 단지 재물을 타인의 지배로부터 이탈하게 하는 것만으로는 절취라고 볼 수 없고 자기 또는 제3자의
> 지배 아래 두는 것을 요한다.

**NormCard** — `formalization: standard_input`, `polarity: positive`, `norm_kind: definition`,
레벨 L1(실행행위)
> 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의
> 지배 아래로 옮기는 것을 뜻한다.

이 한 장이 **술어 2개와 규칙 5개**를 만든다.

### 술어 2개

```scallop
// 이 카드의 사건별 적용 평가 — 외부(neural)가 채우는 입력
type assess_art329_sec3_1_taking_transfer_of_control(String, String, String, String, String, String)
//   (case_id, assessment_id, defendant_id, owner_id, possessor_id, status)

// 증명 가능한 평가에서 이 조건이 충족됨 — 규칙이 도출하는 파생
type satisfied_art329_sec3_1_taking_transfer_of_control(String, String, String, String)
//   (case_id, defendant_id, owner_id, possessor_id)
```

`assess_*`는 **사실 입력**이고 `satisfied_*`는 **판단 결과**다. 이 둘을 분리하는 이유가 아래
규칙 1에 있다.

### 규칙 5개

**① 조건 승격** — 평가가 `satisfied`이고 **증명 가능할 때만** 조건이 선다.

```scallop
rel satisfied_art329_sec3_1_taking_transfer_of_control(case_id, defendant_id, owner_id, possessor_id) =
  assess_art329_sec3_1_taking_transfer_of_control(case_id, assessment_025, defendant_id, owner_id, possessor_id, "satisfied") and
  provable(case_id, assessment_025)
```

`provable`이 절차·증거 게이트다. 위법수집증거로 얻은 사실은 `provable`이 서지 않으므로 실체법
규칙에 도달하지 못한다 — **절차 레이어가 실체 판단을 차단하는 지점이 여기 한 곳**이다.

**② 미확정 보존** — 평가가 `unknown`이면 부정으로 접지 않고 쟁점으로 남긴다.

```scallop
rel theft_undetermined(case_id, defendant_id, "art329_sec3_1.taking_transfer_of_control") =
  assess_...(case_id, unknown_assessment_025, ..., "unknown") and provable(case_id, unknown_assessment_025)
```

**③ 충돌 노출** — 같은 카드에 `satisfied`와 `not_satisfied`가 모두 증명되면 임의로 하나를 고르지
않고 충돌을 드러낸다.

```scallop
rel theft_conflict(case_id, defendant_id, "art329_sec3_1.taking_transfer_of_control") =
  assess_...(case_id, positive_025, ..., "satisfied") and provable(case_id, positive_025) and
  assess_...(case_id, negative_025, ..., "not_satisfied") and provable(case_id, negative_025)
```

**④ 구성요건 단계 연결** — 이 카드의 조건이 실행행위 단계를 인정하는 한 경로가 된다.

```scallop
rel theft_conduct_satisfied(case_id, defendant_id, owner_id, possessor_id) =
  satisfied_art329_sec3_1_taking_transfer_of_control(case_id, defendant_id, owner_id, possessor_id)
```

**⑤ 필수요건 부정** — 이 요건이 명시적으로 `not_satisfied`면 불성립 사유가 된다.

```scallop
rel theft_not_established(case_id, defendant_id, "art329_sec3_1.taking_transfer_of_control") =
  assess_...(case_id, mandatory_negative_021, ..., "not_satisfied") and provable(case_id, mandatory_negative_021)
```

주석서 인용·카드 id가 모든 규칙에 주석으로 붙어 있어 규칙에서 원문까지 역추적된다.

## 2. 역할이 다른 카드는 다르게 배선된다

| 역할 | 예 | 규칙에서 하는 일 |
|---|---|---|
| positive 요건 | `taking_transfer_of_control` | component 인정 경로 + 필수요건 부정 |
| `bar` 저지 | `consent_no_taking`("승낙이 있으면 절취 아님") | `theft_not_established`를 낳는다 |
| `component` | `unlawful_appropriation_required`(부정형이지만 요건 요구) | 주관 단계 인정 경로 + 필수요건 부정 |
| `boundary` | `sole_custodian_coowned_property`(절도 아니라 횡령) | 불성립 + `boundary_shift` + **`refers_to_crime("횡령")`** |
| `waiver` | (절도엔 없음) | `requirement_waived`만 기록, 성립을 막지 않는다 |
| 가중(L5) | `habitual_offender_definition` | 기본범 성립 **위에서** `aggravation("habitual")` |

경계획정 카드가 셋을 동시에 낳는 것이 핵심이다.

```scallop
rel theft_not_established(case_id, defendant_id, "art329_sec2_2.sole_custodian_coowned_property") = satisfied_...(...)
rel theft_boundary_shift(case_id, defendant_id, "art329_sec2_2.sole_custodian_coowned_property") = satisfied_...(...)
rel theft_refers_to_crime(case_id, defendant_id, "횡령") = satisfied_...(...)
```

"절도는 아니다"로 끝나지 않고 "**횡령으로 가라**"가 규칙에 남는다. 후속 죄명은 정규식으로 뽑지
않고 카드별 역할 표(`rule_ir_card_roles.json`)에 사람이 지정한 값이다.

가중은 기본범을 전제로만 켜진다 — 꺼지면 자동으로 단순절도로 남는다.

```scallop
rel theft_aggravation(case_id, defendant_id, "habitual") =
  theft_established(case_id, defendant_id, owner_id, possessor_id) and
  satisfied_art332_sec1_habitual_offender_definition(case_id, defendant_id, owner_id, possessor_id)
```

## 3. 결론이 서는 순서 (스트라텀 5층)

```scallop
// L0~L4 구성요건 단계를 AND 결합 — 부정을 쓰지 않는다
rel theft_elements_satisfied(case_id, defendant_id, owner_id, possessor_id) =
  theft_object_satisfied(...) and theft_conduct_satisfied(...) and
  theft_intent_satisfied(...) and theft_completion_satisfied(...)

// 불성립·충돌을 2항으로 요약
rel theft_has_negative(case_id, defendant_id) = theft_not_established(case_id, defendant_id, _)
rel theft_has_conflict(case_id, defendant_id) = theft_conflict(case_id, defendant_id, _)

// 유일한 부정 사용 규칙 — 완결 게이트 뒤에서만
rel theft_established(case_id, defendant_id, owner_id, possessor_id) =
  theft_elements_satisfied(...) and case_assessment_complete(case_id, defendant_id) and
  ~theft_has_negative(case_id, defendant_id) and ~theft_has_conflict(case_id, defendant_id)

// 공유 수정요소(친족상도례·업무자 신분)로 넘기는 브리지
rel property_crime_established(case_id, "theft", defendant_id, owner_id, possessor_id) =
  theft_established(case_id, defendant_id, owner_id, possessor_id)
```

`case_assessment_complete`가 없으면 요건이 다 충족돼도 성립이 서지 않는다. 라우터가 고른 평가
묶음이 완결됐다는 선언이 있어야 "없는 사실"을 "부정된 사실"로 읽지 않는다.

## 4. 규칙 308개의 내역

| 규칙 종류 | 개수 | 무엇 |
|---|---:|---|
| 조건 승격 | 66 | 카드마다 1개 (카드 수와 같다) |
| 미확정 | 66 | 카드마다 1개 |
| 충돌 | 66 | 카드마다 1개 |
| component 연결 | 30 | 요건 인정 경로 |
| 필수요건 부정 | 30 | 요건 카드의 not_satisfied |
| 가중 플래그 | 26 | L5 카드 |
| 저지 | 15 | bar·boundary 카드 |
| 경계획정 기록 | 2 + 2 | `boundary_shift` + `refers_to_crime` |
| 최종 결론 | 5 | elements / has_negative / has_conflict / established / bridge |

술어 151개 = 시스템 입력 4 + 카드 입력 66 + 카드 조건 66 + component 4 + 결론·요약·플래그 11.

---

## 5. symbolic layer가 완료되었는가 — 정직한 답

**닫힌 것.**
- 카드 → 술어 → 규칙 → Scallop 경로가 전 단위에서 결정론적으로 돌고, 계약 검증과 런타임 골든
  54/54를 통과한다. 규칙에서 주석서 원문까지 역추적된다.
- 미확정·충돌이 부정과 구별되고, 부정은 완결 게이트 뒤 한 규칙에서만 쓰인다.
- 가중유형이 기본범과 분리돼 켜졌다 꺼진다.
- 경계획정이 후속 죄명까지 규칙에 남는다.

**닫히지 않은 것 셋.**

**① component 세분도가 사기보다 훨씬 거칠다 — 가장 큰 문제.** 사기는 component 13개에 카드
32장(component당 2~8장)이지만, 절도는 component 4개에 30장이고 **객체 단계 하나에 19개 카드가
OR로 붙는다**. component 내부가 OR이므로 **19개 중 하나만 인정되면 객체 요건 전체가 충족**된다.
"형법상 점유에는 사실상 지배와 점유 의사가 필요하다" 한 장만 satisfied되면 타인성·재물성을 묻지
않고 객체 단계가 켜진다는 뜻이다. 법리적으로 절도의 객체는 "타인 소유 **AND** 타인 점유"인데
지금 구조는 그 AND를 표현하지 못한다.

| 단위 | component | 카드 | 한 component 최대 분기 |
|---|---:|---:|---:|
| theft | 4 | 30 | **19** |
| property_damage | 4 | 38 | 18 |
| embezzlement | 4 | 42 | 16 |
| extortion | 5 | 29 | 16 |
| 권리행사방해 | 3 | 23 | 16 |
| (참조) 사기 | 13 | 32 | 8 |

원인은 component를 레벨 맵(L0~L4)에서 유도했기 때문이다. 레벨은 **스트라텀 순서**를 정하는 데는
맞지만 **구성요건 단위**로는 너무 굵다. 사기처럼 죄명별로 component를 쪼개야 한다 — 절도라면
객체를 `타인의 재물성` / `타인의 점유` 둘로, 행위를 `점유 배제` / `지배 이전` 둘로 나누는 식이다.
이건 법리 작업이고 카드 배정이 필요하다.

**② deterministic_rule 카드도 `assess_*` 입력을 요구한다.** 사기는 그런 카드를
`fraud_case_roles`에서 상징적으로 도출했는데(역할 배정만으로 조건이 섬), 여기서는 모든 카드가
평가 입력을 받는다. "형법상 점유에는 사실상 지배와 점유 의사가 필요하다" 같은 정의 카드에도 사건별
평가가 들어와야 조건이 선다. 계약은 통과하지만(입력 술어 `kind`만 다르다) **누가 그 사실을 공급할
것인가가 RuleIR 안에 없다**. 지금은 배선 단계의 약속으로만 남아 있다.

**③ 최종 죄명 확정 술어(`charge`)가 없다.** 레벨 설계 문서 §1에는
`charge(case_id, defendant_id, label)`을 두기로 했는데 조립기가 만들지 않는다. 지금은
`theft_established` + `theft_aggravation(kind)` 두 관계를 읽어서 밖에서 "상습절도"인지 "단순절도"인지
조합해야 한다. 그 조합 규칙(가중 여러 개가 동시에 켜졌을 때의 우선순위 포함)이 symbolic layer 안에
없다.

**④ 이월된 것** — 친족상도례(카드 25장)는 브리지 술어를 받는 쪽 규칙이 없다(A4 절차 레이어 결정).
`provable`·`case_assessment_complete`·`<unit>_case_roles`는 외부가 채우는 시스템 입력이고,
그 공급자(절차 레이어·라우터)는 아직 없다.

**판단**: 규칙 골격과 계약은 완료됐고 실행도 된다. 그러나 ①의 OR 폭 때문에 **지금 상태로 사건을
넣으면 요건 충족이 실제보다 쉽게 인정된다.** symbolic layer를 "완료"로 부르려면 ①의 component
재분해가 선행돼야 한다. ②③은 배선 단계에서 메울 수 있지만 ①은 법리 작업이다.

관련: `rulegen_rule_ir_phases.md`(레벨 구조) · `rulegen_rule_ir_units.md`(단위 설계) ·
`data/rulegen/property/RuleIR_법리검토.md`(역할 표 검토)
