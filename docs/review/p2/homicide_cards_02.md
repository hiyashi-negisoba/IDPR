# 살인·존속살해 RuleIR 카드 검수 2

- unit: `homicide`
- articles: art250, art254, art255
- cards: 16–30 / 242
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

## 16. `art250_sec1_12.deadly_herb_attempt_holding`

- proposition: 초우뿌리나 부자를 달인 물을 피해자에게 마시게 하여 살해하려 했지만 미수에 그친 행위는 살인미수죄로 판단된 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 판단이므로 적용 전 원판결과 사실관계 및 위험성 판단을 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.12_44` / `Ⅰ.12`: “피고인이 ‘초우뿌리’나 ‘부자’를 달인 물을 피해자에게 마시게 하여 피해자를 살해하려 했지만 미수에 그친 행위를 살인미수죄로 판단했다.”

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

## 17. `art250_sec1_12.impossible_attempt_danger`

- proposition: 실행 수단 또는 대상의 착오로 사실상 결과 발생이 불가능하더라도 평가상 결과발생 가능성인 위험성이 있으면 불능미수범으로 처벌될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 위험성 판단은 개별 수단·대상과 행위 당시 사정에 대한 평가를 요구한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.12_44` / `Ⅰ.12`: “실행의 수단 또 는 대상의 착오로 인하여 사실상 결과의 발생이 불가능하더라도 위험성, 즉 평 가상의 결과발생 가능성이 있는 때에는 불능미수범으로 벌하도록 하”

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

## 18. `art250_sec1_12.impossible_attempt_danger_assessment`

- proposition: 불능미수의 위험성은 행위 당시 피고인이 인식한 사정을 바탕으로 일반인이 객관적으로 결과 발생 가능성이 있는지를 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위 당시 인식 사정과 일반인의 객관적 평가를 함께 검토해야 하는 평가 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.12_44` / `Ⅰ.12`: “이와 같은 ‘위험성’은 피고인이 행위 당시에 인식한 사정을 놓고 일반인이 객관 적으로 판단하여 결과 발생의 가능성이 있는지 여부를 따져야 한다.”

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

## 19. `art250_sec1_12.impossible_crime_no_danger`

- proposition: 위험성이 없는 행위는 행위자에게 살의가 있더라도 불능범으로서 범죄가 되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 살의의 존재만으로 위험성 없는 행위를 처벌할 수 없다는 예외로 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.12_44` / `Ⅰ.12`: “그러한 위험성도 없는 행위는 비록 행위자가 살의를 가지고 행하여도 불능범으로서 범죄가 되지 않는다.”

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

## 20. `art250_sec1_12.insufficient_pesticide_further_inquiry`

- proposition: 사용한 농약량이 치사량에 현저히 미달한 것으로 보이는 경우에는 치사량을 더 심리하여 장애미수와 위험성 있는 불능미수 중 어느 경우인지 가려야 하며, 이를 하지 않고 장애미수 책임을 인정한 원심은 심리미진이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 치사량 심리와 장애미수·불능미수의 구별에 관한 보고된 판례 판단으로서 원판결 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.12_46` / `Ⅰ.12`: “원심으로서는 이 사건 종자소독약의 치사량을 좀더 심리한 다음 피고인의 행위가 어느 경우에 해당하 는지를 가렸어야 한다고 하여, 장애미수의 책임을 인정한 원심판결에 심리를 다 하지 않은 흠이 있다는 취지로 파기환송하였다.”

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

## 21. `art250_sec1_13.attempt.bleeding_fear_not_voluntary`

- proposition: 많은 피가 흘러나오는 것에 놀라거나 두려움을 느끼는 것은 일반 사회통념상 범죄 완수의 장애 사정에 해당하므로, 이를 자의에 의한 중지미수로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 출혈 상황이 행위자의 자유로운 중지가 아니라 범죄 완수의 장애 사정인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_48` / `Ⅰ.13`: “많은 피가 흘러나 오는 것에 놀라거나 두려움을 느끼는 것은 일반 사회통념상 범죄를 완수함에 장애가 되는 사정에 해당한다고 보아야 할 것이므로, 이를 자의에 의한 중지미 수라고 볼 수 없다.”

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

## 22. `art250_sec1_13.attempt.bleeding_report_fear_not_voluntary`

- proposition: 피해자의 출혈을 보고 놀라 신고와 병원 후송이 이루어지게 한 뒤 체포를 두려워 도주한 경우는 중지미수로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 출혈을 본 놀람, 체포 두려움 및 이후 조치의 구체적 경위를 해당 사례 범위에서 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_47` / `Ⅰ.13`: “피해 자가 입에서 피를 흘리는 것을 보고 놀란 나머지 범행현장에서 자고 있던 A를 깨워서 A로 하여금 119에 신고하여 피해자를 병원에 후송하게 하고 피고인은 체포될 것이 두려워서 도망을 친 경우라면, 이를 중지미수라고 볼 수 없다.”

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

## 23. `art250_sec1_13.attempt.fire_fear_not_voluntary`

- proposition: 치솟는 불길, 자신의 신체안전에 대한 위해 또는 범행 발각 시 처벌에 대한 두려움은 일반 사회통념상 범죄 완수의 장애 사정에 해당하므로, 이를 자의에 의한 중지미수로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 불길, 신체안전 위해 및 발각·처벌 두려움이 중지의 동기가 된 구체적 사정을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_48` / `Ⅰ.13`: “치솟 는 불길에 놀라거나 자신의 신체안전에 대한 위해 또는 범행 발각시의 처벌 등 에 두려움을 느끼는 것은 일반 사회통념상 범죄를 완수함에 장애가 되는 사정에 해당한다고 보아야 할 것이므로, 이를 자의에 의한 중지미수라고는 볼 수 없다.”

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

## 24. `art250_sec1_13.attempt.rope_loosening_and_pursuit`

- proposition: 피해자가 목이 졸려 기절하는 것을 보고 놀라거나 두려움을 느껴 끈을 풀어 준 것은 일반 사회통념상 범죄 완수의 장애 사정에 해당할 수 있으며, 도주하는 피해자를 잡으려 쫓아간 사정이 있으면 끈을 느슨하게 풀어 준 것만으로 실행행위를 종국적으로 중지하였다고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 끈을 푼 동기와 이후 피해자 추격을 포함한 제반 사정이 종국적 중지 여부 판단에 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_48` / `Ⅰ.13`: “피해자가 목이 졸려 기절하는 것을 보고 놀라 거나 두려움을 느껴 끈을 풀어 준 것이라면, 이는 일반 사회통념상 범죄를 완수 함에 장애가 되는 사정에 해당한다고 보아야 한다.”
  - `comm_001692_제250조_Ⅰ.13_48` / `Ⅰ.13`: “피고인이 도망 가는 피해자를 잡으려고 쫓아갔으나 잡지 못한 점 등 기록에 나타난 제반 사정 으로 미루어, 목에 묶여 있는 끈을 느슨하게 풀어 주었다는 것만으로 피고인이 이 사건 범행에 대한 실행행위를 종국적으로 중지하였다고 볼 수도 없다.”

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

## 25. `art250_sec1_13.attempt.victim_ruse_fear_not_voluntary`

- proposition: 추가 실행행위로 나아가지 않은 이유가 피해자의 임기응변 및 피해자의 과다출혈로 인한 두려움이라면 자유로운 의사에 따른 실행행위 중지로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 대응과 행위자의 두려움이 실행 중지를 유발한 구체적 사정인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_47` / `Ⅰ.13`: “더 이상의 실행행위로 나아가지 않은 것은 피해자의 임기응변 및 피해자의 과 다출혈로 인한 피고인의 두려움 때문이라고 보아야 한다. 이는 피고인이 자유로 운 의사에 따라 범죄의 실행행위를 중지한 경우에 해당한다고 볼 수 없다.”

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

## 26. `art250_sec1_13.attempt.voluntary_abandonment_definition`

- proposition: 행위자가 자의로 실행에 착수한 행위를 중지하거나 결과 발생을 자의로 방지한 경우에는 장애미수가 아니라 중지미수가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: ‘자의’ 여부와 실행행위 또는 결과 발생 방지의 해당 여부는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_47` / `Ⅰ.13`: “행위자가 자의로 실행에 착수한 행위를 중지하였거나 결과의 발생을 자의 (⾃意) 로 방지한 경우에는, 장애미수가 아니라 중지미수가 된다.”

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

## 27. `art250_sec1_13.attempt.voluntary_abandonment_social_notion`

- proposition: 범죄 실행행위에 착수한 뒤 범죄가 완수되기 전에 자유로운 의사에 따라 실행행위를 중지하였고, 그 중지가 일반 사회통념상 범죄 완수의 장애 사정에 의한 것이 아니라면 중지미수에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 일반 사회통념상 장애 사정인지와 자유로운 의사에 따른 중지인지는 사실관계별 판단이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.13_47` / `Ⅰ.13`: “범죄의 실행행위에 착수하고 그 범죄가 완수되기 전에 자기의 자유로운 의사에 따라 범죄의 실행행위를 중지한 경우에 그 중지가 일반 사회통념상 범 죄를 완수함에 장애가 되는 사정에 의한 것이 아니라면 이는 중지미수에 해당 한다.”

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

## 28. `art250_sec1_14.actual_course_difference`

- proposition: 사망이 예상과 다른 방법으로 발생했어도 예상한 인과경과와 실제 진행의 차이가 일반 생활경험상 예견 범위 내이고 다른 행위로 평가될 본질적 차이가 아니면 살인죄 책임에 영향이 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 예상 경과와 실제 경과의 차이가 예견 범위 및 본질적 차이 기준을 충족하는지 평가해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_50` / `Ⅰ.14`: “예상했던 인과관계의 진행과 실제 진행과의 차이가 일반적인 생활경험에 의해 예견할 수 있는 범위 내로서 다른 행위로 평가될 수 있을 정도의 본질적인 차이라고는 볼 수 없다.”

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

## 29. `art250_sec1_14.death_causation_attempt`

- proposition: 살인죄의 기수에는 실행행위로 사망 결과가 발생하고 그 인과관계가 인정되어야 하며, 인과관계가 없으면 살인미수에 그친다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사망 결과와 실행행위 사이의 인과관계 판단이 필요한 살인 기수·미수 구별 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_49` / `Ⅰ.14`: “살인의 실행행위에 의하여 사망이라는 결과가 발생할 것을 요하고, 그 인과관계가 인정되지 않으면 본죄의 미 수에 그친다.”

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

## 30. `art250_sec1_14.foreseeable_intervening_fact`

- proposition: 살해행위와 사망 사이에 다른 사실이 개재하여 그 사실이 직접 사인이 되었더라도, 그 개재 사실이 통상 예견 가능한 것이면 인과관계가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 개재 사실의 통상 예견 가능성은 사안별 평가가 필요하며, 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.14_49` / `Ⅰ.14`: “살인의 실행행위와 피 해자의 사망과의 사이에 다른 사실이 개재되어 그 사실이 치사의 직접적인 원 인이 되었다고 하더라도, 그와 같은 사실이 통상 예견할 수 있는 것에 지나지 않는다면 살인의 실행행위와 피해자의 사망과의 사이에 인과관계가 있는 것”

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
