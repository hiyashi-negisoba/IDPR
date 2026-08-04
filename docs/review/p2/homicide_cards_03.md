# 살인·존속살해 RuleIR 카드 검수 3

- unit: `homicide`
- articles: art250, art254, art255
- cards: 31–45 / 242
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #7 `art250_sec1_10.officer_omission_murder`: all_demoted (status=`valid`)
- #8 `art250_sec1_11.indirect_perpetration_attempt`: `art250_sec1_11.indirect_perpetration_attempt_use_act` (status=`valid`)
- #9 `art250_sec1_17.direct_active_euthanasia_legality`: `art250_sec1_17.direct_active_euthanasia_negative` (status=`valid`)
- #10 `art250_sec1_19.excessive_execution_death`: `art250_sec1_19.excessive_execution_death_precedent` (status=`valid`)
- #11 `art250_sec1_21.death_penalty_threshold`: `art250_sec1_21.death_penalty_special_circumstances_majority` (status=`valid`)
- #12 `art250_sec1_3.birth_onset`: `art250_sec1_3.birth_labor_theory` (status=`valid`)
- #13 `art250_sec1_3.death_onset`: `art250_sec1_3.pulse_cessation_organ_removal` (status=`valid`)
- #14 `art250_sec1_3.organ_transplant_law_effect`: `art250_sec1_3.organ_transplant_law_limited_effect` (status=`valid`)
- #15 `art250_sec2_10.arson_death_parricide_concurrence`: `art250_sec2_10.arson_death_parricide_imaginary_concurrence` (status=`valid`)
- #16 `art250_sec2_6.adoptee_biological_parent_offense`: `art250_sec2_6.adoption_type_determines_offense` (status=`valid`)
- #17 `art250_sec2_6.deceased_spouse_lineal_ascendant_offense`: `art250_sec2_6.deceased_spouse_lineal_ascendant_ordinary_murder` (status=`valid`)
- #18 `art250_sec2_9.nonstatus_accomplice_liability`: `art250_sec2_9.nonstatus_accomplice_parricide_coprincipal_punished_ordinary` (status=`valid`)
- #19 `art250_sec2_9.status_instigator_nonstatus_principal`: `art250_sec2_9.status_instigator_parricide_accomplice` (status=`valid`)
- #20 `art255_sec4.preparation_desistance`: `art255_sec4.preparation_desistance_doctrinal_variants` (status=`valid`)

## 31. `art250_sec1_14.medical_negligence_concurrent_cause`

- proposition: 폭행행위가 사망 결과의 유력한 원인이면 의사의 수술지연 등 과실이 사망의 공동원인이더라도 폭력행위와 사망 사이 인과관계가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행행위가 사망의 유력한 원인인지와 의료과실의 기여 정도를 구체적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_50` / `Ⅰ.14`: “비록 의사의 수술지연 등 과실이 피해자 사망의 공동원인이 되 었다 하더라도, 피고인의 행위가 사망의 결과에 대한 유력한 원인이 된 이상 그 폭력행위와 치사의 결과 사이에는 인과관계가 있다”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 32. `art250_sec1_14.omission_counterfactual_causation`

- proposition: 작위의무를 이행하였다면 결과가 발생하지 않았을 것이라는 관계가 인정되면, 작위를 하지 않은 부작위와 사망 결과 사이에 인과관계가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 작위의무 이행 시 결과 회피 가능성에 관한 반사실적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_51` / `Ⅰ.14`: “이와 같 이 작위의무를 이행하였다면 결과가 발생하지 않았을 것이라는 관계가 인정될 경우에는 작위를 하지 않은 부작위와 사망의 결과 사이에 인과관계가 있다”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 33. `art250_sec1_14.recovery_possibility_assistance`

- proposition: 피해자가 매우 위독했더라도 회복 가능성이 전혀 없었던 것이 아니라면 방조행위와 사망 사이에 합법칙적 연관 또는 상당인과관계를 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 회복 가능성과 방조행위가 사망 결과에 미친 연관성을 개별 증거에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_51` / `Ⅰ.14`: “설령 피해자가 매우 위독한 상태였더라도 회복할 가능성이 전혀 없었던 것이 아닌 이상 피고인B, C의 범행과 피해자의 사망 사이에 합법칙적 연관 내지 상 당인과관계를 인정할 수 있다”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 34. `art250_sec1_14.shipmaster_rescue_duty`

- proposition: 선박침몰 등 조난의 급박한 상황에서 선박 운항을 지배하는 선장 등은 적극적 구호활동으로 승객 등의 사망을 방지할 작위의무가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 선박 운항 지배자의 지위, 조난 상황의 급박성 및 가능한 구호활동의 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_51` / `Ⅰ.14`: “선박침몰 등과 같은 조난사고로 급박한 상황이 발생한 경우 선 박 운항을 지배하는 선장 등은 적극적 구호활동을 통해 승객 등의 사망 결과를 방지하여야 할 작위의무가 있다는 점”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 35. `art250_sec1_14.time_gap`

- proposition: 실행행위와 사망 사이의 인과관계가 있으면 사망까지 수일 또는 수개월이 걸렸더라도 살인죄 성부에 영향을 주지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시간 간격 자체가 아니라 실행행위와 사망 사이의 인과관계 존재를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_49` / `Ⅰ.14`: “인과관계가 있으면 양자 사이의 시간적 장단은 범죄의”
  - `comm_001692_제250조_Ⅰ.14_49` / `Ⅰ.14`: “성부에 영향이 없으므로, 수일, 수개월 뒤에 사망하였어도 살인죄는 성립한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 36. `art250_sec1_14.victim_negligence_complications`

- proposition: 상해로 급성신부전증이 발생하고 그 합병증이 직접 사인인 패혈증 등을 유발한 경우, 직접사인 유발에 피해자 과실이 개재했더라도 통상 예견 가능하면 범행과 사망 사이 인과관계가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자 과실과 합병증의 구체적 경과가 통상 예견 가능한지 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_49` / `Ⅰ.14`: “비록 그 직접사 인의 유발에 피해자 자신의 과실이 개재되었더라도 이는 통상 예견할 수 있는 것으로 인정되므로, 피고인들의 이 사건 범행과 피해자의 사망과의 사이에는 인 과관계가 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 37. `art250_sec1_15.bra_strangulation_rape_victim`

- proposition: 브래지어로 강간 피해자의 목을 조른 경우 사망 결과에 대한 범의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 브래지어를 사용한 교살 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “브래지어로 강간 피해자의 목을 졸랐다면, 이로 인하여 사망하리라는 범의는 있”
  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “었다고 인정된다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 38. `art250_sec1_15.bus_attack_police`

- proposition: 탈취한 시내버스를 시속 50km로 경찰기동대원을 향해 돌진시키고 피하는 대원들을 따라 일부러 핸들을 틀어 들이받은 사안에서 미필적 살의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 버스를 경찰기동대원에게 돌진시킨 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “피고인에게 미필적인 살의가 있었다고 본 제1심판결과 원심”
  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “의 조치는 정당하다고 보았다”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 39. `art250_sec1_15.captain_omission_conditional_intent`

- proposition: 침몰 상황에서 선장이 승객 구조의무와 지체 시 승객 익사 가능성을 알면서도 퇴선 요청을 묵살하고 승객을 대기시킨 채 먼저 퇴선하며 구조정보도 제공하지 않은 경우, 부작위에 의한 살인의 미필적 고의가 인정된다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 침몰 선장의 구조 부작위에 관한 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_66` / `Ⅰ.15`: “피고인 A의 이와 같은 행태는 자신의 부작위로 인하여 승객 등이 사망에 이를 수 있음을 예견하고도 이를 용인하는 내심의 의사에서 비롯되었다고 할 것이므로, 부작위에 의한 살인의 미필적 고의가 인정된다는 취지로 판단하였다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 40. `art250_sec1_15.causal_course_error_essential`

- proposition: 인식한 인과과정과 실제 인과과정 사이에 본질적 차이가 있으면 인과과정의 착오로서 고의 성립에 영향을 미칠 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 본질적 차이의 판단은 개별 사안의 법률평가를 요구한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_67` / `Ⅰ.15`: “양자 사이에 본질적 차이가 있을 때에는, 인과과정의 착오 (인과과정의 로서 고의의 성립에 영향을 미칠 수 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 41. `art250_sec1_15.causal_course_error_nonessential`

- proposition: 행위자가 인식한 인과과정과 실제 발생한 인과과정 사이 차이가 본질적이지 않으면 고의에 영향을 미치지 않아 살인기수죄가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 차이가 본질적인지에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_67` / `Ⅰ.15`: “행위자가 인식한 인과과정과 실제 발생한 인과과정 사이에 차이 이”
  - `comm_001692_제250조_Ⅰ.15_67` / `Ⅰ.15`: “있지만, 그 차이가 본질적인 것이라고 할 수 없으므로 살인기수죄가 인정된 다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 42. `art250_sec1_15.caution_recognizing_murder_intent`

- proposition: 결과가 매우 중대하고 동기·방법·정황의 비난 가능성이 크더라도 그러한 사정만으로 살인의 고의를 쉽게 인정해서는 안 되며, 인정에는 신중해야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 살인의 고의 인정에 대한 제한적 판단 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_53` / `Ⅰ.15`: “한 사정을 이유로 살인의 고의를 쉽게 인정할 것은 아니며 이를 인정할 때에는 신중을 기하여야 한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 43. `art250_sec1_15.child_neck_compression`

- proposition: 만 6세 여아의 목을 손목으로 3~4분간 누른 경우 질식사 위험은 일반적으로 예상 가능하므로 살해의 고의를 인정해야 한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 6세 아동의 목 압박 시간에 관한 구체적 사례 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “만 6세 된 여아의 목을 손목으로 3분 내지 4분간 누르게 되면 질식사할 위험이 있”
  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “음은 일반적으로 예상할 수 있는 것이므로 살해의 고의가 있었다고 보아야 한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 44. `art250_sec1_15.child_strangulation_abandonment_attempt`

- proposition: 9세 여아의 목을 스카프로 졸라 실신시킨 후 현장에 버려두고 떠난 경우, 사망 가능성을 인식하지 못했다고 볼 수 없어 살인의 범의를 인정하여 살인미수죄로 처단할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 아동 교살 후 유기 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “그와 같은 자신의 가해행위로 인하여 피해자가 사”
  - `comm_001692_제250조_Ⅰ.15_58` / `Ⅰ.15`: “망에 이를 수도 있다는 사실을 인식하지 못하였다고 볼 수 없으므로, 적어도 그 범행 당시에는 피고인에게 살인의 범의가 있었다 할 것이니, 피고인의 행위를 살인미수죄로 처단한 원심의 조치는 옳다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 45. `art250_sec1_15.conditional_intent_sufficient`

- proposition: 살인죄의 고의에는 확정적 고의가 반드시 필요한 것은 아니고 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 미필적 고의의 충족 가능성을 명시한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_52` / `Ⅰ.15`: “살인죄의 고의는 반드시 확정적 고의임을 필요로 하지 않고 미필적 고의로도 충분하다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```
