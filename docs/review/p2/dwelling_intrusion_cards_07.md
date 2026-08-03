# 주거침입·퇴거불응 RuleIR 카드 검수 7

- unit: `dwelling_intrusion`
- articles: art319
- cards: 91–104 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 91. `art319_sec7_3.ability_to_leave`

- proposition: 퇴거불응의 구성요건적 부작위가 되려면 행위자에게 퇴거의 작위의무를 이행할 일반적·개별적 행위가능성이 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 일반적·개별적 행위가능성은 구체적 사정에 따라 평가한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “부작위범의 성격상 행위자는 퇴거의 작위의무를 이행할 수 있는 일반적·개별적 행위가능성이 있어야 거기에 대한 불응이 구성요건적 부작위가 된다.”

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

## 92. `art319_sec7_3.debt_dispute_motive`

- proposition: 채무를 부인하는 피해자가 피고인을 만나주지 않고 경찰관을 동원하여 내보내려 하였다는 사정에 분노하여 퇴거요구에 불응한 동기나 목적은, 피해자의 주거생활 평온 침해를 정당화할 이유가 될 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문, 사실관계 및 판단 범위를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “판례는, 피해자가 피고인의 아들로부터 금원을 차용하고도 차용증이나 영수증이 없음을 기화로 채무를 부인하면서 피고인을 만나주지도 않으려고 할 뿐만 아니 라, 피고인이 담을 넘어 피해자의 주거에 침입한 것으로 단정하고 경찰관을 동 원하여 몰아내려고 하므로 분노를 이기지 못하여 퇴거요구에 응하지 않았다고 하더라도, 그러한 동기나 목적이 피해자의 주거생활의 평온이라는 법익침해를 정당화할 만한 이유가 될 수는 없다고 하였다.”

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

## 93. `art319_sec7_3.impossible_leaving`

- proposition: 퇴거요구를 받은 사람이 객관적·주관적으로 그 요구에 응할 수 없거나, 퇴거가 인간 일반 또는 행위자 개인에게 실현 불가능하면 퇴거불응죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 헌법재판소 관련 원문과 적용 범위를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “헌법재 판소도 퇴거요구를 받은 자가 퇴거요구에 응할 수 있는 객관적·주관적 사정하 에 있어야 한다고 한다. 퇴거요구가 인간 일반으로서 또는 행위자 개인으로 서 실현 불가능한 것이면 퇴거불응죄는 성립하지 않는다.”

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

## 94. `art319_sec7_3.justified_demand`

- proposition: 퇴거불응죄의 퇴거요구는 정당한 퇴거요구여야 하며, 정당하지 않은 퇴거요구에 불응한 경우에는 퇴거불응죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 퇴거요구의 정당성은 구체적 권원과 체류 상황을 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_58` / `Ⅶ.3`: “퇴거요구는 정당한 퇴거요구에 국한되고, 정당하지 않은 퇴거요구에 응하지 않 은 경우는 퇴거불응죄가 성립하지 않는다.”

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

## 95. `art319_sec7_3.lawful_lockout_demand`

- proposition: 근로자 직장점거가 쟁의 목적 달성에 필요한 범위에서 제한적으로 개시되어 적법하더라도, 사용자가 적법하게 직장폐쇄를 하면 사업장에 대한 물권적 지배권이 전면 회복되어 사용자에게 점거 근로자에 대한 퇴거요구 권한이 생긴다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 직장폐쇄의 적법성과 선행 점거의 적법성은 노동관계 법원에 따라 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “그러나 사용자가 이에 대응하여 적법 하게 직장폐쇄를 하게 되면, 사용자의 사업장에 대한 물권적 지배권이 전면적으 로 회복되므로 사용자는 점거 중인 근로자들에 대하여 정당하게 사업장으로부 터의 퇴거를 요구할 수 있게 된다.”

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

## 96. `art319_sec7_3.lawful_lockout_noncompliance`

- proposition: 적법하게 직장폐쇄를 단행한 사용자로부터 퇴거요구를 받고도 불응하여 직장점거를 계속한 행위는 퇴거불응죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 적법한 직장폐쇄와 퇴거요구의 존재가 전제되는 적용 기준이다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_61` / `Ⅶ.3`: “적법하게 직장폐쇄를 단행한 사용자로부터 퇴거요구를 받고도 불응한 채 직장점거를 계속하는 행위는 퇴거불응죄에 해당한다.”

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

## 97. `art319_sec7_3.no_justifiable_reason`

- proposition: 퇴거불응죄가 성립하려면 퇴거에 불응할 정당한 사유가 없어야 하며, 정당한 사유가 있으면 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 정당한 사유의 존재는 개별 법익과 체류 사정을 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “퇴거에 불응할 정당한 사유가 없어야 하고, 정당한 사유가 있는 경우에는 퇴거 불응죄가 성립하지 않는다.”

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

## 98. `art319_sec7_3.open_place_manager_demand`

- proposition: 일반적으로 개방된 장소라도 관리자는 필요에 따라 출입을 제한할 수 있으므로, 관리자의 퇴거요구에도 건조물에서 퇴거하지 않으면 퇴거불응죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 관리자의 제한 권한과 퇴거요구의 정당성은 장소와 관리 관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_59` / `Ⅶ.3`: “일반적으로 개방되어 있는 장소라 하더라도 관리자가 필요에 따라 그 출입을 제한할 수 있는 것이므로 관리자의 퇴거요구에도 불구하고 건조물에서 퇴거하 지 않는 것은 사실상 건조물의 평온을 해하는 것으로서 퇴거불응죄를 구성한 다.”

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

## 99. `art319_sec7_3.refusal_delay`

- proposition: 퇴거요구를 받은 적법 체류자도 즉시 퇴거하여야 하고, 유책한 지체가 있으면 퇴거불응이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 유책한 지체 여부는 퇴거 가능성 및 요구에 응할 수 있는 시간과 함께 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_59` / `Ⅶ.3`: “일단 퇴거요구를 받은 자는 비록 그 때까지 적 법하게 주거공간에 체류하던 자라도 즉시 퇴거하여야 한다. 만약 유책한 지 체가 있게 되면 일단 퇴거불응이 된다.”

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

## 100. `art319_sec7_3.time_to_comply`

- proposition: 거동이 어렵거나 목욕탕에서 옷을 모두 벗고 있는 사람은 퇴거요구에 응할 수 있는 시간 동안에는, 요구 후 시간이 지체되더라도 위법한 체류로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 응할 수 있는 시간의 상당성은 행위자의 구체적 퇴거 가능성에 따라 판단한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_60` / `Ⅶ.3`: “따라서 상대방이 거동이 어려운 사정이 있거나 목욕탕에서 옷을 모두 벗고 있는 경우에는, 퇴거요구 후 시간이 지체되었을지라도 퇴거요구에 응 할 수 있는 시간 동안은 위법한 체류라고 할 수 없다.”

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

## 101. `art319_sec7_3.unlawful_lockout_noncompliance`

- proposition: 사용자의 직장폐쇄가 정당한 쟁의행위로 인정되지 않는 경우, 사용자가 직장폐쇄를 이유로 적법한 쟁의행위로 사업장을 점거 중인 근로자에게 퇴거요구를 하여도 근로자가 불응해 직장점거를 계속한 경우 퇴거불응죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 적법한 쟁의행위 점거 및 부당한 직장폐쇄라는 제한된 사실관계에 한정된다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.3_61` / `Ⅶ.3`: “반면 사용자의 직장폐쇄가 정당한 쟁의행위로 인정되지 아니하는 경우에는, 근로자가 평소 출입이 허용되는 사업장 안으로 들어가더라도 건조물침입죄를 구성하지 않고, 사용자가 직장폐쇄를 이유로 적법한 쟁의행위로서 사업장을 점거 중인 근로자들에게 퇴거요구를 하였는데 피고인들이 이에 불응한 채 직장점거를 계 속하였더라도 퇴거불응죄가 성립하지 않는다.”

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

## 102. `art319_sec7_4.intent`

- proposition: 퇴거불응죄의 고의가 인정되려면 거주자 등의 퇴거요구 및 그 정당성, 자신의 체류 정당성 결여를 인식하면서도 퇴거요구에 불응하려는 의사가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 퇴거요구의 정당성, 체류 정당성 결여 및 불응 의사에 대한 사실관계 평가는 evaluative judgment를 필요로 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.4_62` / `Ⅶ.4`: “즉 거주자 등의 퇴거요구가 있다는 사실과 그러한 요구가 정당한 요구라는 사실 및 자신의 체류에 대한 정 당성이 결여되어 있다는 사실을 인식하였음에도 불구하고 퇴거요구에 불응하려 는 의사가 있어야 한다.”

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

## 103. `art319_sec2_1.dwelling_concept_sleeping`

- proposition: 주거는 사람이 기거하고 침식에 사용하는 장소라는 다수설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 주거를 기거·침식 사용 장소로 보는 다수설이다. 일상생활 점거설과의 선택은 보류한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_9` / `Ⅱ.1`: “ⅰ) 사람이 기거하고 침식에 사용되는 장소를 말한 다는 다수설”

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

## 104. `art319_sec5_2.private_arrest_home_entry_affirmative`

- proposition: 사인이 현행범인 체포를 위해 타인의 주거에 들어간 행위도 당시의 구체적 사정과 정당행위의 일반적 요건에 따라 위법성조각이 가능하다는 긍정설이 있다.
- current metadata: formalization=`context_only`, polarity=`exception`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 사인의 현행범 체포를 위한 타인 주거 출입에 위법성조각을 인정할지 선택이 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_46` / `Ⅴ.2`: “사인이 현행범인 체포를 위해 타인의 주거에 들어간 행위는 행”
  - `comm_001692_제319조_Ⅴ.2_46` / `Ⅴ.2`: “위 당시의 구체적 사정을 고려하여 위법성조각이 가능하다고 한다.”

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
