# 살인·존속살해 RuleIR 카드 검수 7

- unit: `homicide`
- articles: art250, art254, art255
- cards: 91–105 / 242
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

## 91. `art250_sec1_18.actio_libera_in_causa`

- proposition: 범행을 예견하고도 자의로 심신장애를 야기한 뒤 살인을 저지른 경우에는 형법 제10조 제3항에 따라 심신장애로 인한 감경을 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 범행 예견과 자의적 심신장애 야기 여부를 개별적으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_85` / `Ⅰ.18`: “대마초 흡연시에 이미 범행을 예견하고도 자의로 심신장애를 야기한 경우 에 해당하므로, 형법 제10조 제3항에 의해 심신장애로 인한 감경 등을 할 수 없 다고 보았다.”

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

## 92. `art250_sec1_18.compulsion_no_responsibility`

- proposition: 저항할 수 없는 폭력 또는 자기·친족의 생명·신체에 대한 위해를 방어할 능력이 없는 협박으로 강요된 행위 등 적법행위의 기대가능성이 없는 경우에는 행위자의 책임을 물을 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 저항 불가능성, 방어 능력의 부재 및 적법행위 기대가능성은 구체적 강요 상황에 따라 판단한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_86` / `Ⅰ.18`: “저항할 수 없는 폭력, 자기·친족의 생명·신체에 대한 위해를 방어할 능력이 없 는 협박에 의해 강요된 행위, 행위자에게 위법성의 인식이 없거나 (형법 제12조) 적법행위에 대한 기대가능성이 없는 경우에는, 행위자의 책임을 물을 (제15조) 수 없다.”

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

## 93. `art250_sec1_18.impulse_control_personality_defect_exception`

- proposition: 원칙적으로 충동조절장애와 같은 성격적 결함은 형의 감면사유인 심신장애에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 성격적 결함에 관한 원칙을 다루며, 매우 심각한 경우의 별도 예외와 병합하지 않는다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “원칙적으로 충동조절 장애와 같은 성격적 결함은 형의 감면사유인 심신장애에 해당하지 않는다.”

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

## 94. `art250_sec1_18.mental_appraisal_when_suspected`

- proposition: 심신장애가 의심되는데도 정신감정을 하지 않고 규범적 요소에만 기초하여 심신장애 주장을 배척하는 것은 위법하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 심신장애 의심의 정도와 정신감정 필요성은 절차적 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_85` / `Ⅰ.18`: “심신장애의 의심이 있음에도 정신감정을 하지 않고 규범적 요소들에만 기초하여 심신장애 주장을 배척하는 것은 위법하다고 본다.”

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

## 95. `art250_sec1_18.mental_disability_judicial_assessment`

- proposition: 심신장애의 유무와 정도는 법률적 판단이므로 법원은 전문감정 의견에 반드시 기속되지 않으며, 정신질환의 종류·정도, 범행 경위와 전후 행동 등 제반 사정을 종합하여 독자적으로 판단할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 전문감정과 범행 전후의 정황을 포함한 제반 사정을 종합하는 평가 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “심신장애의 유무 및 정도의 판단 은 법률적 판단으로서 반드시 전문감정인의 의견에 기속되어야 하는 것은 아니고”
  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “병의 종류 및 정도, 범행의 동기 및 원인, 범행의 경위 및 수단과 태양, 범행 전후의 피고인의 행동, 증거인멸 공작의 유무, 범행 및 그 전후의 상황에 관 한 기억의 유무 및 정도, 반성의 빛 유무, 수사 및 공판정에서의 방어 및 변소의 방법과 태도, 정신병 발병 전의 피고인의 성격과 그 범죄와의 관련성 유무 및 정 도 등을 종합하여 법원이 독자적으로 판단할 수 있다”

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

## 96. `art250_sec1_18.mental_disorder_normal_capacity_exception`

- proposition: 정신적 장애가 있더라도 범행 당시 정상적인 사물변별능력이나 행위통제능력이 있으면 심신장애로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 정신적 장애의 존재와 범행 당시 심신장애 성립은 구별하여 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “정신적 장애가 있는 자라고 하여도 범행 당시 정상 적인 사물변별능력이나 행위통제능력이 있었다면 심신장애로 볼 수 없다.”

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

## 97. `art250_sec1_18.mental_disorder_requirements`

- proposition: 심신장애는 정신병 또는 비정상적 정신상태와 같은 정신적 장애라는 생물학적 요소와, 그 장애로 사물변별능력 및 행위통제능력이 결여되거나 감소한 심리학적 요소를 모두 요구한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 생물학적 요소와 심리학적 요소의 충족 여부는 개별 사실관계에 따라 평가한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “형법 제10조에 규정된 심신장애는 생물학적 요소로서 정신병 또는 비정상적 정 신상태와 같은 정신적 장애가 있는 외에 심리학적 요소로서 이와 같은 정신적 장애로 말미암아 사물에 대한 변별능력과 그에 따른 행위통제능력이 결여되거 나 감소되었음을 요하므로”

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

## 98. `art250_sec1_18.pathological_personality_defect`

- proposition: 충동조절장애·인격장애·소아기호증 등의 비정상적 정신상태는 병적인 경우 심신장애에 해당할 수 있으나, 성격적 결함인 경우에는 심신상실이나 심신미약에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 비정상적 정신상태가 병적인 상태인지 단순 성격적 결함인지는 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “병적인 것인 경 우에는 심신장애에 해당할 수 있으나 성격적인 결함인 경우에는 심신상실이나 나아가 심신미약에도 해당하지 않는다고 본다.”

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

## 99. `art250_sec1_18.responsibility_capacity`

- proposition: 살인죄 성립을 위해 행위자에게 책임능력이 있어야 하며, 책임능력 판단의 기준 시점은 범행 당시이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 책임능력의 존재는 개별 행위와 범행 당시의 사정을 바탕으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_83` / `Ⅰ.18`: “살인죄가 성립하기 위해서는 행위자에게 책임능력이 있어야 한다.”
  - `comm_001692_제250조_Ⅰ.18_83` / `Ⅰ.18`: “임능력 판단의 기준 시점은 범행 당시여야 한다.”

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

## 100. `art250_sec1_18.self_induced_methamphetamine_impairment`

- proposition: 필로폰 투약으로 인한 환각 상태에서 타인의 생명에 위해를 가할 수 있음을 예견하고도 스스로 심신미약 상태를 야기하여 살인을 저지른 경우에는 심신장애 감경을 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 필로폰 투약, 타인 생명 위해의 예견, 자초한 심신미약 및 살인 범행이라는 보고된 사실관계 범위에서 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_86` / `Ⅰ.18`: “필로폰 투약으로 인한 환각상태에서 흉기를 휘두르는 등으로 인해 주 변 사람의 생명에 위해를 가할 수 있다는 점을 예견하고도 스스로 심신미약 상 태를 야기한 후 살인의 범행을 저지른 이상 형법 제10조 제3항에 의하여 심신장 애로 인한 감경을 할 수 없다고”

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

## 101. `art250_sec1_18.severe_impulse_control_disorder_exception`

- proposition: 충동조절장애와 같은 성격적 결함이라도 매우 심각하여 본래 의미의 정신병자와 동등하다고 평가할 수 있으면, 그로 인한 범행은 심신장애로 인한 범행으로 본다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 성격적 결함의 원칙적 배제에 대한 매우 심각한 경우의 명시적 예외로서 별도 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.18_84` / `Ⅰ.18`: “충동조절장애와 같은 성격적 결함이라 할지라도, 그것이 매우 심각하여 원래의 의미의 정신병을 가진 사람과 동등하다고 평가할 수 있는 경우에는, 그로 인한 범행은 심신장애로 인한 범행으로 보아야 한다.”

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

## 102. `art250_sec1_19.aiding_forms`

- proposition: 살인방조행위에는 물질적 방조뿐 아니라 정범의 범행결의를 강화하는 정신적 방조도 포함되며, 실행착수 전 장래 실행행위를 예상하여 이를 용이하게 한 경우도 방조범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 정신적 또는 사전 방조가 실행을 실제로 용이하게 했는지 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “방조행위는 유형적·물질적 방조뿐만 아니라 정범에게 범행의 결의를 강화하도”
  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “록 하는 것과 같은 무형적·정신적 방조행위까지도 이에 해당한다.”
  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “실행 착수 전에 장래의 실행행위”
  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “를 예상하고 이를 용이하게 하는 행위를 하여 방조하는 경우에도 방조범이 성”

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

## 103. `art250_sec1_19.aiding_murder`

- proposition: 살인죄 정범이 범행한다는 점을 알면서 그 실행행위를 용이하게 하는 행위를 한 사람은 살인방조범으로 처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 정범 범행 인식과 실행 용이화의 연결을 확인한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “살인죄의 정범이 범행을 한다는 정을 알면서 그 실행행위를 용이하게 하는 행”
  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “위를 한 사람은 살인의 방조범으로 처벌된다.”

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

## 104. `art250_sec1_19.aiding_murder_intent`

- proposition: 살인방조범이 성립하려면 방조자가 정범의 살인 실행행위를 방조한다는 고의와 정범 행위가 구성요건에 해당한다는 점에 관한 정범의 고의가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 방조자의 고의와 정범의 고의를 구별하여 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “범의 성립을 위해서는, 정범의 살인 실행행위를 방조한다는 이른바 방조의 고의”
  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “와, 정범의 행위가 구성요건에 해당하는 행위인 점에 대한 정범의 고의가 있어”

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

## 105. `art250_sec1_19.aiding_principal_intent_conditional_knowledge`

- proposition: 살인방조에서 정범의 고의는 정범이 실현할 범죄의 구체적 내용을 인식할 필요 없이 미필적 인식 또는 예견으로 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 미필적 인식 또는 예견의 인정은 구체적 정황 평가를 요한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_96` / `Ⅰ.19`: “어 정범의 고의는 정범에 의하여 실현되는 범죄의 구체적 내용을 인식할 것을 요하는 것은 아니고, 미필적 인식 또는 예견으로 족하다.”

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
