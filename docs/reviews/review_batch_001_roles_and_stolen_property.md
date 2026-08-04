# 검수 배치 001 — 법률검수 판정

## 배치 A — 기존 룰베이스 차단 역할 재검토

### A-01 `residence_without_actual_presence`

판정: **O**

> comment: `bar`에서 배제해야 합니다. “실제 현존이 필요하지 않다”는 것은 현주건조물방화죄의 객체요건을 완화·확인하는 긍정 법리입니다. 다만 완전 제외보다는 `requirement_waived` 또는 positive/component-support 역할을 신설할 수 있다면 그쪽이 더 정확합니다.

### A-02 `no_breach_or_loss_requirement`

판정: **O**

> comment: 재산죄 체계의 `waiver`가 “해당 요건 불요”를 의미한다면 유지가 타당합니다. 다만 P2의 waiver와 이름이 동일하면서 의미가 반대이므로 장기적으로는 `requirement_waived`로 명칭을 통일하는 편이 안전합니다.

### A-03 `co_resident_common_space`

판정: **다른 지시 — 카드 분리**

> comment: 하나의 카드에 서로 다른 결론이 혼재합니다.
> ① 공동거주자의 공동생활 장소 이용은 일정한 경우 불성립이라는 명제와
> ② 공동거주관계가 없는 외부인의 출입은 성립할 수 있다는 명제를 분리해야 합니다.
> 전자는 조건부 `bar`, 후자는 주거침입 성립을 지지하는 positive/component 카드가 적절합니다. 현 상태의 단일 `bar`는 유지하면 안 됩니다.

### A-04 `labor_dispute_incidental_act`

판정: **O — bar 유지**

> comment: 명제상 정당행위의 구체적 성립 가능성을 표현합니다. 카드가 “수단·방법의 적정성을 벗어나지 않는 부수행위”라는 사실까지 모두 충족한 경우를 나타낸다면 위법성조각 `bar`가 맞습니다. 단순히 정당행위의 일반 판단기준만 담은 카드라면 결과 카드와 기준 카드를 분리해야 합니다.

### A-05 `no_property_damage_element`

판정: **O**

> comment: 횡령죄에서 재산상 손해의 현실적 발생이 별도 구성요건이 아니라는 확인 법리이므로 재산죄형 waiver가 적합합니다.

### A-06 `right_exercise_total_assessment`

판정: **X — 현재 bar 유지 반대**

> comment: 이 카드는 위법성조각의 결론이 아니라 “전체적으로 관찰하여 사회통념상 용인 가능한지 판단한다”는 심사기준입니다. 이것이 satisfied되었다는 이유만으로 공갈죄를 차단해서는 안 됩니다.
> `assessment_standard`로 두고, 별도로 `socially_acceptable_means_satisfied`와 같은 결과 predicate가 인정될 때만 bar가 발화해야 합니다.

### A-07 `omission_escape_guarantor`

판정: **O — 조건부 bar 유지**

> comment: “체포·인계할 보증인적 지위가 없는 일반인의 단순 불인계”라는 사실이 인정되었다면 부작위에 의한 범인도피죄의 작위의무가 결여되므로 bar가 타당합니다. 다만 적극적인 은닉·도피행위까지 함께 차단하지 않도록 `omission_path`에만 결박해야 합니다.

### A-08 `object_error`

판정: **O**

> comment: `bar`에서 배제해야 합니다. 객체의 착오는 살인의 고의 성립에 영향을 주지 않는다는 판례가 확인됩니다. positive 또는 `intent_not_negated` 계열이 적합합니다.

### A-09 `defensive_counterattack`

판정: **다른 지시 — 기준 카드와 조각 결과 카드 분리**

> comment: 적극적 반격도 정당방위가 될 수 있다는 부분은 허용범위를 설명하지만, “상당한 이유”가 있어야 한다는 제한도 함께 포함합니다. 카드 전체가 만족됐다는 의미가 방위의 상당성까지 인정되었다는 것이라면 bar가 가능하지만, 현 문언만으로는 일반 기준 카드에 가깝습니다.

### A-10 `mutual_fight_excessive_weapon`

판정: **O — 조건부 bar 유지**

> comment: 예상 범위를 현저히 넘은 흉기 공격을 새로운 부당한 침해로 보고 그에 대한 방위가 허용된다는 구체적 예외 법리입니다. 다만 “허용될 수 있다”만으로 자동 조각하지 말고, 실제 방위행위의 필요성·상당성 predicate가 추가로 충족되어야 합니다.

### A-11 `self_defense_social_adequacy`

판정: **X — 직접 bar 반대**

> comment: 정당방위의 상당성 판단요소를 열거한 일반 심사기준일 뿐, 상당성이 실제 충족되었다는 결론은 아닙니다. `assessment_standard`로 분리하고 `self_defense_proportionality_satisfied`가 인정될 때 bar가 발화해야 합니다.

### A-12 `victim_consent`

판정: **O**

> comment: 일반 살인의 피해자 승낙은 단순한 위법성조각 사유가 아니라 촉탁·승낙살인이라는 별도 구성요건으로 이동시키는 사유이므로 boundary가 적절합니다.

### A-13 `advance_directive_life_sustaining_treatment`

판정: **O — 조건부 bar 유지**

> comment: 사전의료지시의 존재만으로 자동 차단하면 안 됩니다. 회복불가능한 사망 단계, 유효한 사전의료지시, 의사 변경의 특별사정 부재, 중단행위의 의료적 적정성이 함께 충족될 때에만 bar가 발화해야 합니다.

### A-14 `life_sustaining_treatment_withdrawal`

판정: **O — 조건부 bar 유지**

> comment: 적법한 연명치료 중단이 인정되는 완성된 조건군이라면 살인죄의 위법성 또는 구성요건 귀속을 차단하는 역할이 가능합니다. 다만 “전문의 소견을 종합하여 판단한다”는 기준 부분과 최종 허용 결론은 분리하는 것이 좋습니다.

### A-15 `presumed_will_life_sustaining_treatment`

판정: **O — 조건부 bar 유지**

> comment: 환자의 의사 추정이 적법하게 성립하고 다른 연명치료 중단 요건까지 충족된 경우에 한해 차단해야 합니다. 추정의사 하나만으로 살인죄 전체가 불성립해서는 안 됩니다.

### A-16 `mental_disorder_requirements`

판정: **X — 직접 bar 반대**

> comment: 심신장애의 생물학적·심리학적 요건을 설명하는 정의 카드입니다.
> 다음과 같이 분리해야 합니다.

* 심신상실 인정 → 책임조각 bar
* 심신미약 인정 → 감경 post_outcome
* 두 요소 중 하나 결여 → 심신장애 주장을 배척하지만 살인죄 성립은 차단하지 않음

### A-17 `withdrawal_before_execution`

판정: **O — 보류**

> comment: 명제가 비어 있으므로 법률검수 자체가 불가능합니다. 실행 자산에서는 `disabled/data_error`로 차단하고, 빈 카드가 bar로 컴파일되지 않도록 해야 합니다.

### A-18 `arson_homicide_resident_building`

판정: **O**

> comment: 명제의 법적 효과가 일반 살인죄와의 상상적 경합이 아니라 현주건조물방화치사죄로 의율하는 것이라면 boundary가 적합합니다. 다만 살해 목적이 있었다는 이유만으로 살인 평가가 완전히 소멸하는지, 적용한 판례의 정확한 죄수론 문언은 원전 판결과 추가 대조할 필요가 있습니다.

### A-19 `murder_after_completed_robbery_or_rape`

판정: **X — 현재의 단순 boundary 유지 반대**

> comment: 카드 문언 자체는 “선행 강도·강간이 완료된 뒤 별도 살해한 경우 결합범이 아니라 살인죄와 선행범죄의 실체적 경합”이라고 합니다. 따라서 살인죄에서 robbery로 이동시키는 boundary는 반대 방향입니다.
> 이 카드는 다음과 같은 `concurrence/post_outcome`이어야 합니다.

* 살인죄 유지
* 선행 강도죄 또는 강간죄 유지
* 결합범인 강도살인·강간살인은 부정
* 양 죄는 실체적 경합

### A-20 `military_minor_restraint`

판정: **O**

> comment: 구체적 사실관계가 카드 명제와 일치하고 경미성·목적·수단의 상당성이 모두 인정된 경우 정당행위에 의한 bar가 맞습니다.

### A-21 `old_education_law_corporal_punishment`

판정: **O — 역사법 적용 제한 필요**

> comment: 당시 법령 및 판례가 적용되는 구사건에 한해서 정당행위 bar가 가능합니다. 현행 사건에 일반화되지 않도록 `temporal_scope` 또는 적용 법령 시점을 반드시 결박해야 합니다.

### A-22 `no_intent_to_appropriate_required`

판정: **O**

> comment: 권리행사방해죄에서 불법영득의사가 필요하지 않다는 확인 법리이므로 재산죄 waiver가 맞습니다.

### A-23 `voluntary_accompaniment`

판정: **O — 공무집행 적법성 component에 한정**

> comment: 자발성이 객관적으로 입증되지 않거나 퇴거를 제지한 경우 적법한 공무집행이 아니므로 공무집행방해죄의 전제가 결여됩니다. bar가 가능하지만, “임의동행 일반”이 아니라 `lawful_official_duty` component를 부정하는 구조로 설계하는 편이 정확합니다.

### A-24 `active_conduct_requirement`

판정: **O — 조건부 bar 유지**

> comment: 소극적 거동이나 단순 불복종에 그쳤다는 사실이 인정되면 폭행·협박 구성요건이 결여되므로 bar가 맞습니다. “적극적 행위가 필요하다”는 일반 명제만 만족되었다고 차단하지 말고, 사건 사실이 소극적 거동에 불과하다는 predicate와 결합해야 합니다.

### A-25 `immediate_self_recovery_assessment`

판정: **X — 직접 bar 반대**

> comment: 자력탈환의 직시성 판단요소를 제시한 기준 카드입니다. 직시성이 실제 인정되었다는 결과가 아니므로 `assessment_standard`가 적합합니다.

### A-26 `justifiable_act_requirements`

판정: **X — 직접 bar 반대**

> comment: 정당행위의 일반 요건을 열거하는 법리 카드입니다. 모든 요건이 실제 충족되었다는 별도의 conclusion predicate가 있어야 bar가 발화합니다.

### A-27 `possession_protection_destruction`

판정: **O**

> comment: 부당한 점유침탈 배제, 위험방지 목적, 비과도성 및 사회적 상당성까지 인정되는 구체적 사안이라면 정당행위 bar가 맞습니다.

### A-28 `socially_acceptable_act`

판정: **X — 직접 bar 반대**

> comment: 사회상규에 위배되지 않는 행위의 추상적 정의일 뿐입니다. 정의가 참이라는 이유로 개별 손괴행위의 위법성이 조각될 수 없습니다.

### A-29 `presumed_consent`

판정: **X — 직접 bar 반대**

> comment: 추정적 승낙의 정의 카드입니다. 개별 사건에서 객관적 사정상 피해자가 당연히 승낙했을 것이라는 평가가 별도로 인정되어야 bar가 됩니다.

### A-30 `name_change_new_document_forgery`

판정: **O**

> comment: 변조죄가 아니라 위조죄가 성립한다는 죄명 전환 법리이므로 boundary로 변경해야 합니다. 다만 현재 유닛명이 이미 `public_document_forgery`라면 target이 자기 자신이 되는지 확인하고, 실제 출발 유닛이 `public_document_alteration`인지 정합성을 점검해야 합니다.

### A-31 `direct_violence_threat`

판정: **O — target 명칭 재검토**

> comment: 행위자가 직접 폭행·협박하지 않고 제3자가 조성한 항거불능 상태를 이용한 경우 일반 강간죄가 아니라 준강간죄 검토로 이동한다는 구조는 boundary가 타당합니다. target은 추상적인 `quasi_sexual_offense`보다 실제 죄명 유닛인 `quasi_rape` 등에 정확히 결박하는 것이 좋습니다.

### A-32 `valid_consent`

판정: **다른 지시 — 카드 분리 후 일부 bar**

> comment: 두 명제가 혼재합니다.

* 피해자 본인의 유효한 성관계 승낙 → 강간죄 구성요건 배제 bar
* 친권자 등 제3자의 승낙 → 강간죄 성립에 영향 없음

첫 번째는 bar, 두 번째는 `consent_not_effective` 또는 positive 확인 법리로 분리해야 합니다. 특히 피해자의 연령·의사능력·승낙의 자유성 등을 별도 요건으로 두어야 합니다.

### A-33 `no_safe_escape_requirement`

판정: **O**

> comment: 강취 직후 안전지역까지 이탈할 필요가 없다는 기수시점 확인 법리이므로 재산죄 waiver가 적합합니다.

### A-34 `abandonment_before_execution_denied`

판정: **O**

> comment: 예비·음모죄는 해당 행위로 완성되므로 중지미수가 성립하지 않는다는 법리입니다. 다만 `waiver`보다 `defense_unavailable` 또는 post_outcome이 의미상 명확합니다.

### A-35 `spouse_delivery_inference`

판정: **O — boundary 변경**

> comment: 제3자뇌물제공죄의 독립적 제3자 귀속이 아니라 공무원 본인에게 전달된 것으로 평가하는 내용이라면 뇌물수수죄 쪽으로 이동시키는 boundary가 맞습니다. 다만 “전달된 것으로 본다”는 사실추론 카드와 최종 죄명 이동 카드를 분리하는 것이 안전합니다.

### A-36 `spouse_insurance_opportunity`

판정: **O — boundary 변경**

> comment: 처에게 형식적으로 제공된 보험모집 기회가 실질적으로 공무원 자신이 받은 경제적 이익으로 평가되는 사안이라면 뇌물수수죄로 이동하는 boundary가 타당합니다.

---

## 배치 B — 장물죄 신규 적재

### B-01 역할 어휘

판정: **O — 단, 명칭 개선 권고**

> comment: 기존 아키텍처 중 하나를 선택해야 한다면 재산죄 어휘를 사용하는 것이 맞습니다. 장물죄는 형법상 재산범죄 계열이고, 기존 재산죄 빌더의 requirement waiver·boundary·refers-to 구조와도 더 잘 맞습니다.
> 다만 P2와 재산죄에서 `waiver`의 의미가 반대인 상태는 계속해서 사고를 발생시킬 수 있으므로 다음처럼 명시적으로 분리하는 것이 바람직합니다.

* `requirement_waived`: 특정 요건 불요, 성립 차단 아님
* `justification_bar`: 위법성조각
* `excuse_bar`: 책임조각
* `element_failure`: 구성요건 결여
* `boundary_shift`: 다른 죄명으로 이동
* `concurrence_outcome`: 흡수·경합·불가벌적 사후행위

### B-02 장물보관 후 횡령

판정: **X — post_outcome 취지는 찬성하나 횡령죄 boundary 방식은 반대**

> comment: 장물보관죄 성립을 전제로 후속 횡령행위를 불가벌적 사후행위로 처리해야 한다는 핵심 문제의식은 맞습니다. 따라서 장물죄 유닛에서 이 카드를 `bar`로 두어서는 안 됩니다.

다만 횡령죄 유닛에서 장물보관죄로 단순 `boundary` 이동시키는 것도 정확하지 않습니다. 후속 횡령행위가 장물보관죄의 구성요건으로 “죄명이 전환”되는 것이 아니라, 이미 성립한 장물보관죄에 흡수되어 별도의 횡령죄를 처벌하지 않는 죄수론적 효과이기 때문입니다.

권고 구조:

1. 장물보관죄의 구성요건 판단은 독립적으로 완료
2. 후속 횡령죄의 구성요건 판단도 필요하다면 별도로 수행
3. 동일 행위자·동일 장물·선행 장물보관 성립·후속 영득행위 조건 확인
4. `embezzlement_punishment_suppressed_by_post_offense`
5. 최종 출력: “장물보관죄는 성립하고, 후속 횡령은 불가벌적 사후행위로 별죄를 구성하지 않는다.”

즉 `boundary`가 아니라 **cross-unit concurrence/absorption rule**이 적합합니다.

### B-03-a 극성과 규범종류 혼동

판정: **O**

> comment: `polarity`와 `norm_kind`는 반드시 분리해야 합니다.

권고 스키마:

* `polarity`: `positive | negative`
* `norm_kind`: `element | exception | justification | excuse | requirement_waiver | boundary | concurrence | evidentiary_rule | assessment_standard`
* 필요하면 `effect_on_offense`: `supports | defeats | neutral | redirects | suppresses_additional_offense`

현재처럼 `exception`을 polarity 값으로 허용하면 극성 기반 감사뿐 아니라 빌더의 성립·불성립 연결도 불안정해집니다.

### B-03-b 죄수론 견해 병합

판정: **O**

> comment: 경합범설과 상상적 경합설은 결론이 서로 다르므로 반드시 별개 카드로 분리해야 합니다. 같은 `variant_group`에 넣되 다음 메타데이터가 필요합니다.

* `view_id`
* `authority_type`
* `is_majority_view`
* `is_precedent_view`
* `mutually_exclusive_with`
* `selection_policy`

시스템이 아무 기준 없이 두 견해를 동시에 발화시키지 않도록 사건별 적용 견해 또는 기본 권위 우선순위를 정해야 합니다.

### B-03-c 권위 표시 과장

판정: **O**

> comment: 판결문이 직접 판시한 명제와 해설자가 판례를 재구성한 명제를 구분해야 합니다. “판례에 따르면”이라는 출력은 권위 출처가 실제 판결인 경우에만 허용해야 합니다.

권고 값:

* `binding_statute`
* `supreme_court_holding`
* `lower_court_holding`
* `commentary_interpretation`
* `academic_view`
* `editorial_synthesis`

판례 번호나 판시사항과 직접 연결되지 않는 카드는 `commentary_interpretation` 이하로 내려야 합니다.

### B-03-d 누락된 대립 견해

판정: **O — 출처 검증 조건부**

> comment: 주석에 실제로 명시된 경쟁 견해라면 누락 카드와 coverage gap을 보충해야 합니다. 다만 단순히 카드 수를 맞추기 위해 생성하지 말고, 각 견해마다 다음을 확인해야 합니다.

* 정확한 논점
* 결론 차이
* 다수설·소수설·판례의 구별
* 근거 출처
* 상호 배타성
* 실제 사건 결론에 미치는 효과

특히 `영득의사 불요`, `미수 불벌`, `운반죄의 기수시점`, `양도죄 부정의 근거`는 서로 다른 층위의 법리이므로 하나의 exception 묶음으로 처리하면 안 됩니다.

---

# 최종 승인 요약

## 제안대로 승인

A-01, A-02, A-04, A-05, A-07, A-08, A-10, A-12, A-13, A-14, A-15, A-17, A-18, A-20, A-21, A-22, A-23, A-24, A-27, A-30, A-31, A-33, A-34, A-35, A-36

B-01, B-03-a, B-03-b, B-03-c, B-03-d

## 제안 또는 현재 역할에 반대

A-06, A-11, A-16, A-19, A-25, A-26, A-28, A-29

B-02의 `boundary` 구현 부분

## 카드 분리 또는 구조 변경 필요

A-03, A-09, A-16, A-19, A-32, B-02

## 즉시 실행 자산에서 차단할 데이터 결함

A-17
