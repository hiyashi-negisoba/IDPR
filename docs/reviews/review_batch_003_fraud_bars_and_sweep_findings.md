# 검수 배치 003 — 법률검수 판정

## G. 사기 BAR 23장

### G-01 미수를 불성립으로 처리하는 3장

판정: **다른 지시 — 문제 진단은 O, 임시 `post_outcome`은 조건부 승인**

> comment: 세 카드를 죄 전체의 `bar`에서 제거해야 한다는 판단은 맞습니다. 형법 제352조는 사기죄의 미수범을 처벌하므로, 기수요건이 결여되었다는 이유만으로 사기죄 전체를 `not_established`로 처리해서는 안 됩니다. 실제 판결에서도 형법 제347조와 제352조를 적용하여 사기미수를 독립적으로 처벌합니다.
>
> 다만 세 카드가 모두 자동으로 “미수 성립”을 도출하는 것도 정확하지 않습니다. 인과관계나 결과가 없다는 사실만으로는 부족하고, 적어도 사기죄의 실행의 착수와 고의가 인정되어야 합니다.

권고 구조:

```text
fraud_deception_satisfied
AND fraud_intent_satisfied
AND execution_commenced
AND completion_causation_not_satisfied
→ fraud_attempt_established
```

각 카드의 적절한 효과:

1. `fraud_general_object.causation_required`

   * `fraud_completion_bar`
   * 미수 성립을 직접 확정하지 않음

2. `fraud_general_object.deception_error_causation`

   * 실행의 착수와 고의가 별도로 인정된 경우에만 `fraud_attempt_candidate`

3. `fraud_stages_participation.no_causation_attempt`

   * 문언상 미수 결과 카드로 사용할 수 있으나, 실행의 착수와 고의를 부모 tuple로 요구

현재 트랙 기능이 없다면 임시 `post_outcome`에 다음처럼 구조화할 수 있습니다.

```text
completed_offense = false
attempt_review_required = true
attempt_established = 별도 요건 충족 시에만 true
```

단순히 `기수 부정·미수 성립`을 한 묶음으로 고정해서는 안 됩니다.

---

### G-02 절도죄·횡령죄로 이동하는 3장

판정: **O — boundary로 변경**

> comment: 세 카드 모두 단순한 사기죄 불성립 사유가 아니라 동일 사실관계가 다른 죄명으로 평가되어야 한다는 내용이므로 `boundary`가 맞습니다.

```text
fraud_mistake.no_capacity_theft
→ theft

fraud_mistake.trick_theft_directness
→ theft

general_object.fraud.standard.own-possession-other-property-embezzlement
→ embezzlement
```

다만 boundary가 발화했다고 해서 target 범죄가 곧바로 성립하는 것은 아닙니다.

권고 출력:

```text
fraud_not_established
referred_issue(theft)
target_verdict = pending_separate_evaluation
```

즉 사기죄 유닛은 “절도 또는 횡령 검토로 이동해야 한다”까지만 계산하고, 절도·횡령 유닛이 자기 구성요건을 별도로 판단해야 합니다.

---

### G-03 실제 발화한 3장

판정: **O — 제안대로 재분류**

> comment: 세 카드가 사람 상대 사기 사건에서도 발화했다는 것은 모델 평가의 우연한 오류라기보다, **규범의 참 여부와 사건사실의 충족 여부를 동일한 `satisfied` 값으로 표현한 구조적 오류**입니다.

#### 1. `deception-target-human`

`assessment_standard`로 이관하는 것이 맞습니다.

이 카드는 다음 일반법리를 설명합니다.

```text
기망의 상대방은 착오와 처분행위를 할 수 있는 사람이어야 한다.
```

그 자체는 개별 사건의 상대방이 기계였다는 사실이 아닙니다. 따라서 다음 두 predicate를 분리해야 합니다.

```text
deception_target_eligibility_standard
actual_target_lacks_human_cognition
```

두 번째가 인정되어야 사기죄의 해당 경로를 차단할 수 있습니다.

#### 2. `deception-must-create-false-belief`

긍정형 필수 component로 재작성하는 것이 맞습니다.

```text
deception_created_or_maintained_false_belief
```

이 component가 불충족되어야 기망요건이 결여됩니다. “허위관념을 발생시키지 않은 행위는 기망이 아니다”라는 법리 문장 자체를 bar로 평가하면 안 됩니다.

#### 3. `no-disposition-no-deception`

이 역시 긍정형 필수 component로 전환해야 합니다.

다만 카드명과 명제를 함께 재검토해야 합니다. 사기죄는 기망행위, 착오, 처분행위 및 그 사이의 인과관계를 요구합니다. 대법원도 기망·착오·재산적 처분행위 사이의 인과관계가 필요하다고 봅니다.

권고 분리:

```text
deception_caused_mistake
mistake_caused_disposition
property_disposition_occurred
```

현재의 `no-disposition-no-deception`은 기망의 존재와 처분행위·인과관계의 존재를 혼동할 가능성이 있습니다. 기망행위는 있었지만 처분행위에 이르지 않아 사기미수가 되는 경우도 있으므로, “처분행위 없음 → 기망 없음”으로 컴파일해서는 안 됩니다.

---

### G-04 나머지 14장

판정: **X — 14장 일괄 bar 유지 반대**

> comment: 일부는 구체적인 구성요건 결여를 나타내므로 bar가 가능하지만, 다수는 일반 판단기준·판례 사례 또는 증거평가 기준입니다. 전부 bar로 두면 G-03과 같은 사고가 반복됩니다.

#### 직접 bar 유지 가능

1. `fraud_intent.no_disposition_inducement_intent`

   * 처분행위를 유발할 고의가 실제로 없다는 사건 평가라면 주관적 구성요건을 차단

2. `fraud_mistake.no_thought_no_error`

   * 피해자가 아무런 관념을 형성하지 않았다는 사건사실까지 평가한다면 착오 component 차단
   * 다만 정의 문장만 평가하는 현재 방식이면 `assessment_standard`

3. `fraud_mistake.property_limited_disposition`

   * 실제 행위가 재산적 처분행위에 해당하지 않는다는 사건 평가라면 disposition component 차단
   * 일반 정의만 담은 상태라면 `assessment_standard`

4. `general_object.fraud.standard.own-property-not-object`

   * 구체적으로 행위자 자신의 재물·재산상 이익만 문제되는 경우라면 객체 또는 타인재산성 경로 차단

5. `general_object.fraud.standard.public-interest-only-no-fraud`

   * 침해된 대상이 순수한 공익에 그치고 피해자의 재산적 처분·손해가 없다는 사실까지 확정하는 카드라면 bar 가능

#### `assessment_standard` 또는 `evidentiary_standard`로 이동

* `deception.fraud.causal-link.loan-purpose-not-sole-trigger`
* `deception.fraud.element.transaction-purpose-no-impairment`
* `deception.fraud.standard.advertising-tolerable-exaggeration`
* `deception.fraud.standard.easily-detectable-lie`
* `deception.fraud.standard.loan-lender-anticipated-risk`
* `deception.fraud.standard.loan-subsequent-default`
* `deception.fraud.standard.vague-opinion-not-deception`
* `fraud_mistake.omission_not_all_nonclaims`
* `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

이 카드들은 대부분 “어떤 사정만으로 기망·고의·위법성이 인정되거나 부정되는 것은 아니다” 또는 “전체 사정을 고려한다”는 성격입니다. 예컨대 차용 후 채무불이행만으로 차용 당시 편취의 범의를 단정할 수 없다는 판례 법리는 증거평가 기준이지, 채무불이행 사실이 있는 모든 사건에서 사기죄를 자동 차단하는 규칙이 아닙니다.

#### 특별히 분리할 카드

`special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

다음 두 부분을 분리해야 합니다.

```text
right_exercise_social_acceptability_standard
right_exercise_means_actually_socially_acceptable
```

첫 번째는 기준, 두 번째가 인정된 경우에만 위법성 또는 기망성을 차단해야 합니다.

#### 결론

14장 중 현 문언 그대로 일괄 bar를 유지하는 것은 승인할 수 없습니다. 최소한 `norm_kind=definition/standard`인 카드는 사건사실 predicate와 분리해야 합니다.

---

# H. 26문항 실행이 드러낸 구조적 사실

## H-01 평가의 85.5%가 unknown

판정: **O — 평가 단계 재설계 필요, 단 top-k 검색으로 해결하지 말 것**

> comment: 제시된 수치만으로도 미확정의 주원인이 규칙 부족보다 평가 단계에 있다는 진단은 타당합니다. 유닛당 수십~141장의 카드를 평면적으로 전량 평가하면, 모델이 핵심 요건과 참고 법리·예외·판례 사례를 같은 중요도로 처리하게 됩니다.

다만 다음과 같이 구분해야 합니다.

```text
전량 자산 보존 ≠ 모든 카드를 한 번의 평면 프롬프트에서 동일하게 평가
```

top-k retrieval을 사용하지 않고도 전량평가 원칙을 유지할 수 있습니다.

### 권고: 계층형 전량평가

1. **필수 component skeleton 우선 평가**

   * 객체
   * 행위
   * 고의
   * 인과관계
   * 기수·미수
   * 위법성·책임

2. **각 component와 연결된 카드만 해당 단계에서 평가**

   * 모든 카드는 최종적으로 어느 단계엔가 포함
   * 검색으로 일부를 삭제하지 않음

3. **정의·판단기준은 사실평가 대상에서 제외**

   * `assessment_standard`는 모델에게 법리로 제공
   * `satisfied/not_satisfied`의 사건 판정 대상이 아님

4. **variant는 선택된 견해만 결론 평가**

   * 미선택 견해는 설명용으로만 보존

5. **선행 component가 충족되거나 쟁점화된 경우에만 예외·bar 평가**

   * 예: 기망행위가 전혀 문제되지 않으면 광고 과장 허용한계 카드 수십 장을 평가할 필요 없음

6. **미확정 원인을 구조화**

   * `fact_missing`
   * `role_binding_failed`
   * `standard_only_no_application_result`
   * `conflicting_assessments`
   * `required_component_unknown`

이는 top-k 우회가 아니라 Rule graph에 따른 **deterministic staged evaluation**입니다.

---

## H-02 미확정 유닛의 누락 요건

판정: **O — component별 진단 데이터로 활용**

> comment: 누락된 항목이 절도 고의·점유·불법영득의사, 살인미수·중지미수, 횡령 실행행위·고의·기수 등 핵심 component에 집중되어 있다는 점은 H-01의 진단을 뒷받침합니다.

다만 “카드가 unknown이었다”만 기록하지 말고 다음처럼 구분해야 합니다.

```text
component_status:
  satisfied
  not_satisfied
  unknown_due_to_missing_fact
  unknown_due_to_model_nonassessment
  unsupported_by_rulebase
  contract_degraded
```

특히 지문에 충분한 사실이 있는데 모델이 핵심 카드를 `unknown`으로 평가한 것과, 지문 자체에 사실이 없는 경우는 성능 문제의 성격이 다릅니다.

권고 측정치:

* component recall
* fact-supported unknown rate
* fact-missing unknown rate
* 필수 component별 평가 누락률
* 죄종별 평균 활성 카드 수
* 기준·사례 카드가 차지하는 토큰 비중

---

## H-03 쟁점 단위 강등

판정: **O — 사건 전체 폐기 제거 승인**

> comment: 하나의 쟁점에서 역할 결박 또는 인용 계약이 실패했다는 이유로 다른 정상 쟁점까지 폐기하는 것은 법률적으로도 시스템적으로도 부적절합니다. 쟁점 단위로 격리하고 나머지 유닛의 symbolic verdict를 보존하는 수정은 타당합니다.

다만 “자율 논증으로 넘긴다”는 표현은 다음 상태를 명시해야 합니다.

```text
issue_status = contract_degraded
symbolic_verdict = unavailable
generation_mode = nonbinding_fallback
```

최종 답안에서도 다음을 구분해야 합니다.

* RuleBase가 판정한 쟁점
* 계약 결함으로 RuleBase가 판정하지 못한 쟁점
* 후자의 모델 논증은 심볼릭 결론이 아니라 잠정 분석이라는 표시

모델이 fallback에서 단정적 유·무죄 결론을 내고 이를 symbolic verdict처럼 합치면 안 됩니다.

또한 결함 쟁점의 원문과 오류 원인을 보존해야 합니다.

```text
degraded_reason:
  unsupported_role
  quote_not_grounded
  missing_dependency
  missing_required_role
```

---

# I. `polarity=exception` activation gate

판정: **O — 당분간 `enforce: false`, 단 무기한 유지 금지**

> comment: 즉시 `enforce: true`로 전환하여 36개 유닛 중 25개를 중단시키는 것은 운영상 과도합니다. 현재는 감사 경고 모드로 두고, 교정된 카드부터 승인 목록에 넣는 방식이 타당합니다.

다만 `enforce: false`가 단순 경고에 그치면 위험 카드가 계속 결론을 뒤집을 수 있으므로, 전체 유닛 차단과 무제한 허용 사이에 중간 게이트가 필요합니다.

### 권고 단계

#### 1단계 — 현재

```text
enforce = false
audit_warning = true
```

추가로 각 실행 결과에 다음을 기록:

```text
unreviewed_exception_polarity_cards_fired
unreviewed_exception_polarity_cards_reached
```

#### 2단계 — 카드 단위 제한

미승인 `polarity=exception` 카드가 발화하더라도:

* `bar`
* `boundary`
* P2의 차단형 `waiver`

효과는 바로 결론에 연결하지 않고 `quarantined_effect`로 보존합니다.

즉 유닛 전체를 중단하지 않으면서도 미검수 카드가 유·무죄를 뒤집는 것은 막습니다.

```text
card_evaluated = satisfied
legal_effect = quarantined_pending_review
```

#### 3단계 — 점진적 enforce

* 교정 완료 카드 → `approved`
* 법적 효과 확인 카드 → 정상 컴파일
* 미검수 카드 → quarantine
* 88장 전량 처리 후 `enforce = true`

### 우선순위

88장을 동일 순서로 검토하지 말고 다음 순서로 처리해야 합니다.

1. 실제 26문항에서 발화한 카드
2. `bar`로 연결된 카드
3. `boundary`로 연결된 카드
4. P2 차단형 `waiver`
5. 도달 가능하지만 아직 발화하지 않은 카드
6. 현재 비활성·미도달 카드

### 최종 판단

`enforce: false` 유지 자체는 승인합니다. 다만 미승인 카드의 차단 효과까지 그대로 허용하는 의미의 `false`여서는 안 됩니다. **유닛 중단은 하지 않되, 미검수 카드의 결론 효과만 격리하는 soft enforcement**를 추가하는 것이 적절합니다.

---

# 종합 승인표

| 항목   | 판정                         |
| ---- | -------------------------- |
| G-01 | 수정 후 승인 — 기수 차단과 미수 성립 분리  |
| G-02 | O                          |
| G-03 | O                          |
| G-04 | X — 14장 재분류                |
| H-01 | O — 계층형 전량평가               |
| H-02 | O                          |
| H-03 | O — nonbinding fallback 명시 |
| I    | O — 경고 모드 유지 + 카드 효과 격리    |

# 장물죄 원장 착수 전 빌더 설계에 관한 확인

이번 문서의 8개 판정란과 별도로, 질문하신 두 신규 기능에 대해서도 방향을 확인합니다.

## 1. Component-scoped bar

**도입해야 합니다.**

현재처럼 track 전체만 차단할 수 있으면 다음과 같은 오판이 생깁니다.

```text
장물취득 경로의 요건 결여
→ 장물보관·운반·알선까지 전부 불성립
```

bar에 최소한 다음 scope가 필요합니다.

```text
effect_scope:
  unit
  track
  component
  subtype
```

예:

```text
card = acquisition.account_withdrawal
effect = bar
scope = component
target = stolen_goods_acquisition
```

장물성 자체가 소멸한 경우처럼 모든 행위태양에 공통되는 사유만 unit 또는 공통 object component를 차단해야 합니다.

## 2. Variant selection state

**장물죄 146장 배치 전에 도입해야 합니다.**

variant 카드를 일반 component 또는 bar로 먼저 배치하면, 이후 선택 상태를 추가해도 이미 생성된 SCL과 원장의 의미를 다시 전수검토해야 합니다.

최소 상태:

```text
variant_status:
  selected
  unselected
  authority_default
  policy_selected
  rejected
```

컴파일 원칙:

```text
selected / authority_default / policy_selected
→ 결론 relation 연결 가능

unselected
→ 설명·비교용으로만 노출

rejected
→ 실행 자산에서 제외
```

같은 `variant_group`에서 상호 배타적인 두 견해가 동시에 선택되지 않도록 registry audit도 필요합니다.

따라서 **component-scoped bar와 variant selection을 먼저 구현하고, 그 후 장물죄 146장을 배치하는 순서가 맞습니다.** 반쯤 적재한 뒤 조립기 의미론을 바꾸는 것보다 현재 멈춘 판단이 타당합니다.
