# 살인·존속살해 RuleIR 카드 검수 9

- unit: `homicide`
- articles: art250, art254, art255
- cards: 121–135 / 242
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

## 121. `art250_sec1_19.unforeseen_killing_exception`

- proposition: 여러 명이 가벼운 상해 또는 폭행의 범의로 범행하던 중 1인이 살인의 결과를 발생시킨 경우, 나머지 사람들이 살인을 전혀 예측하지 못했다면 그들에게 살인죄 책임을 물을 수 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 살인 결과의 예견 가능성과 별개의 결과적 가중범 책임을 구분하여 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_89` / `Ⅰ.19`: “여러 명이 가벼운 상해 또는 폭행 등의 범의로 범행 중 1인이 살인의 결과를 발 생케 한 경우, 그 나머지 사람들은 상해 또는 폭행죄 등과 결과적 가중범의 관 계에 있는 상해치사 또는 폭행치사 등의 죄책은 면할 수 없다고 하더라도 살인 등에 관해서는 전혀 예측하지 못하였다 할 것이므로 그들에게 살인죄의 책임을 물을 수는 없다.”

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

## 122. `art250_sec1_19.withdrawal_before_execution`

- proposition: 살인 공모에 가담했더라도 다른 공모자가 실행에 착수하기 전에 공모관계에서 이탈하면 이후 다른 공모자의 살인행위에 대해 공동정범 책임을 지지 않으며, 이탈 의사는 반드시 명시적일 필요가 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이탈 시점과 이탈 의사 표시의 객관적 의미를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_88` / `Ⅰ.19`: “살인죄의 범행 모의에는 가담하였더라도 다른 공모자들이 실행에 착수하기 전에 그 공모관계에서 이탈하였다면 그 이후 다른 공모자들의 살인행 위에 관하여는 공동정범으로서의 책임을 지지 않고, 그 이탈의 표시는 반드시 명시적임을 요하지 않는다고 본다.”

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

## 123. `art250_sec1_19.withdrawal_mere_flight_insufficient`

- proposition: 사전 공모에 따른 행위에 관하여 공모자가 총을 버리고 도망간 사정만으로는 공모관계에서 이탈하였다고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 도주 외에 공모 영향력을 제거한 사정이 있는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “피고인 B, C, D가 당시 총을 버리고 도망갔다고 하더라도 그것만으로는 공”
  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “모관계에서 이탈한 것으로 볼 수 없다.”

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

## 124. `art250_sec1_19.withdrawal_remove_influence`

- proposition: 공모에 주도적으로 참여하여 다른 공모자의 실행에 영향을 미친 사람은 범행 저지를 위한 적극적 노력 등으로 자신의 영향력을 제거하지 않으면 공모관계에서 이탈했다고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주도성, 영향력 및 영향력 제거 노력은 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_88` / `Ⅰ.19`: “공모자가 공 모에 주도적으로 참여하여 다른 공모자의 실행에 영향을 미친 때에는 범행을 저지하기 위하여 적극적으로 노력하는 등 실행에 미친 영향력을 제거하지 않는 한 공모관계에서 이탈하였다고 할 수 없다.”

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

## 125. `art250_sec1_2.omission_homicide_guarantor_status`

- proposition: 부작위에 의한 살인죄는 주체에게 보증인적 지위가 요구되는 진정신분범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 부작위에 의한 살인죄의 주체 요건으로서 보증인적 지위를 명시한 commentary synthesis다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.2_2` / `Ⅰ.2`: “부작위에 의한 살인죄의 경우, 주체의 요건으로 보증인적 지위를 요하므로 진정신분범이 된다.”

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

## 126. `art250_sec1_20.adjacent_multiple_homicides`

- proposition: 동일 장소에서 동일 방법으로 시간적으로 접착하여 여러 사람을 살해한 경우 여러 살인죄의 실체적 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시간적 접착과 행위 수의 평가는 개별 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “반면 동일한 장소에서 동일한 방법에 의해 시간적으로 접착되어 여러 사람을 살해한 때에는, 여러 개 살인죄의 실체적 경합범이 된다.”

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

## 127. `art250_sec1_20.arson_homicide_resident_building`

- proposition: 사람을 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우 현주건조물방화치사죄로 의율하며 살인죄와 상상적 경합으로 의율하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 현주건조물 해당성, 방화와 사망의 관계 및 살해 목적의 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_100` / `Ⅰ.20`: “사람을 살해할 목적으로 현주건조물에 방화하여 사망에 이르게 한 경우”
  - `comm_001692_제250조_Ⅰ.20_100` / `Ⅰ.20`: “에는 현주건조물방화치사죄로 의율하여야 하고 이와 더불어 살인죄와의 상상적 경합범으로 의율할 것은 아니다.”

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

## 128. `art250_sec1_20.clothing_damage_absorbed`

- proposition: 살인행위에 따른 의복 손괴는 불가벌적 수반행위로서 재물손괴죄가 살인죄에 흡수된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살인행위에 수반된 의복 손괴에 한정된 흡수 관계다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “살인행위에 따른 의복 손괴는 불가벌적 수반행위로서 재물손괴죄는 살인죄에 흡수된다.”

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

## 129. `art250_sec1_20.corpse_abandonment_separate`

- proposition: 사람을 살해한 뒤 사체를 다른 장소로 옮겨 유기한 경우 사체유기죄가 별도로 성립하며, 이를 불가벌적 사후행위로 볼 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사체를 다른 장소로 옮겨 유기한 경우에 한정된 별도 성립 관계다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “그러나 사람을 살해한 자가 그 사체를 다른 장소로 옮겨 유기하였을 때에는 별도로 사체유기죄가 성립하고, 이와 같은 사체유기를 불가벌적 사후행 위로 볼 수는 없다.”

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

## 130. `art250_sec1_20.corpse_left_at_scene`

- proposition: 살해 목적 수행 중 사체 발견을 어렵게 하려는 의사로 인적 드문 장소로 피해자를 유인하거나 끌고 가 살해한 뒤 사체를 그대로 두고 도주한 경우, 사체 발견이 현저히 곤란해졌더라도 별도 사체은닉죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사체를 그대로 둔 채 도주한 사실관계와 별도 은닉행위의 유무를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_100` / `Ⅰ.20`: “사체를 그대로 둔 채 도주한 경우에는, 비록 결과적으로 사체의 발견이 현저하게 곤란을 받게 되는 사정이 있다 하더라도 별도로 사체은닉죄가 성립되지 않는다”

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

## 131. `art250_sec1_20.debt_evasion_no_robbery_murder`

- proposition: 채무가 명백하고 채권자의 상속인이 존재하며 채권 확인 방법도 확보된 경우, 채무 면탈 의사로 채권자를 살해하여도 재산상 이익 지배가 이전되었다고 보기 어려워 강도살인죄는 성립하지 않고 살인죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 주석 인용문의 '이러한 경우'에 해당하는 채무 및 재산상 이익 지배 관련 전제사실을 원문 맥락에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_101` / `Ⅰ.20`: “이러한 경우에는 강도살인죄가 성립할 수 없다. 이 경우 살인죄만 성립한다고 보아야 한다.”

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

## 132. `art250_sec1_20.homicide_count_by_victims`

- proposition: 살인죄의 죄수는 피해자 수에 따라 결정된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피해자별 살인죄 성립의 기본 죄수 기준으로 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “생명은 전속적 법익이므로, 살인죄의 죄수는 피해자의 수에 따라 결정되어야 한 다.”

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

## 133. `art250_sec1_20.kidnapped_minor_injury_rape_attempted_murder`

- proposition: 미성년자 피해자를 약취한 후 강간 목적으로 가혹행위와 상해를 가하고 강간 및 살인미수를 한 경우, 약취 미성년자 상해 관련 특정범죄가중처벌법위반죄와 강간 및 살인미수 관련 성폭력처벌법위반죄는 상해 결과가 후행 행위 과정에서 발생했더라도 실체적 경합관계이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 각 죄의 구성요건 충족 및 상해 결과와 후행 행위의 관계를 사실관계별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_102` / `Ⅰ.20`: “의 결과가 피해자에 대한 강간 및 살인미수행위 과정에서 발생한 것이라 하더”
  - `comm_001692_제250조_Ⅰ.20_102` / `Ⅰ.20`: “라도 위 각 죄는 서로 실체적 경합범 관계에 있다고 보았다.”

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

## 134. `art250_sec1_20.murder_after_completed_robbery_or_rape`

- proposition: 살인죄가 강도살인죄나 강간살인죄 등 결합범의 일부가 되려면 살인행위가 강도 또는 강간 등의 기회에 이루어져야 하며, 선행 범죄가 완료된 뒤 살해하면 별도 살인죄와 선행 강도죄 또는 강간죄는 실체적 경합관계이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 선행 범죄의 완료 시점과 살인행위가 해당 범죄의 기회에 이루어졌는지를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_101` / `Ⅰ.20`: “의 결합범에 법조경합을 이루기 위해서는, 살인행위가 강도 또는 강간 등의 기”
  - `comm_001692_제250조_Ⅰ.20_101` / `Ⅰ.20`: “회에 이루어져야 한다. 강도 또는 강간범죄가 완료된 후에는 살해행위가 별도의 살인죄를 구성하게 되며, 선행하는 강도죄 또는 강간죄와 실체적 경합관계에 서”

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

## 135. `art250_sec1_20.retaliatory_murder_purpose`

- proposition: 피고인의 자백 없이 보복 목적의 존재를 판단할 때에는 피해자와의 관계, 수사단서 제공에 대한 반응, 불이익 내용과 정도, 범행 경위·수단·방법·태양, 전후 정황 등 객관적 사정을 종합 고려해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 보복 목적은 객관적 정황의 종합 평가가 필요한 판단 요소다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_102` / `Ⅰ.20`: “인에게 보복의 목적이 있었는지 여부는 피해자와의 인적 관계, 수사단서의 제공 등 보복의 대상이 된 피해자의 행위에 대한 피고인의 반응과 이후 수사 또는 재”
  - `comm_001692_제250조_Ⅰ.20_102` / `Ⅰ.20`: “판과정에서의 태도 변화, 수사단서의 제공 등으로 피고인이 입게 된 불이익의 내용과 그 정도”

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
