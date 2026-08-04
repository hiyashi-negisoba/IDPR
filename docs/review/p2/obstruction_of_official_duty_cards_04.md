# 공무집행방해 RuleIR 카드 검수 4

- unit: `obstruction_of_official_duty`
- articles: art136
- cards: 46–54 / 54
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art136_sec3_1.article136_2_offense`

- proposition: 제136조 제2항의 직무·사직강요죄는 공무원에게 직무상 행위를 강요 또는 저지하거나 사직하게 할 목적으로 폭행 또는 협박함으로써 성립하는 범죄이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무상 행위의 권한 범위와 적법성, 사직 강요의 포섭은 평가적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.1_56` / `Ⅲ.1`: “공무원에 대하여 그 직무상의 행위를 강요 또는 저지하거나 그 직을 사퇴하게 할 목적으로 폭행 또는 협박을 함으로써 성립하는 범죄이다.”

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

## 47. `art136_sec3_2.subject_unrestricted`

- proposition: 직무·사직강요죄의 주체에는 제한이 없으며 공무원도 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체의 제한 없음과 공무원이 주체가 될 수 있다는 범위만을 반영한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.2_57` / `Ⅲ.2`: “본죄의 주체에는 제한이 없다. 공무원도 본죄의 주체가 될 수 있다.”

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

## 48. `art136_sec3_3.future_officer_object`

- proposition: 직무·사직강요죄의 객체는 현재 직무를 집행 중인 공무원일 필요 없이 장래 직무를 집행할 공무원이면 충분하다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현재 직무집행 여부가 아니라 장래 직무집행 예정 공무원인지 여부를 객체 요건으로 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.3_58` / `Ⅲ.3`: “다만 직무를 집행하는 공무원일 것을 요하지 아니하고 장래에 직무 를 집행할 공무원이면 족하다”

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

## 49. `art136_sec3_4.article136_2_purpose`

- proposition: 직무·사직강요죄는 공무원에게 직무상 행위를 강요·저지하거나 사직하게 할 목적을 필요로 하는 목적범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 목적의 존재 여부와 목적의 세 유형은 별도로 확인한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.4_59` / `Ⅲ.4`: “본죄는 ‘공무원에 대하여 그 직무상의 행위를 강요 또는 저지하거나 그 직을 사 퇴하게 할 목적’을 필요로 하는 목적범이다.”

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

## 50. `art136_sec3_4.nonofficial_act_coercion`

- proposition: 공무원의 직무상 행위에 해당하지 않는 행위를 강요할 목적으로 폭행·협박한 경우에는 직무·사직강요죄가 성립하지 않고 강요죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무상 행위 해당 여부 및 강요죄 성립 여부는 각각 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.4_59` / `Ⅲ.4`: “공무원의 직무상의 행위에 해당하지 아 니하는 행위를 강요할 목적으로 공무원에게 폭행이나 협박을 한 경우에는 본죄 가 성립하지 아니하고 강요죄가 성립할 수 있다.”

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

## 51. `art136_sec3_4.official_act_scope`

- proposition: 직무·사직강요죄의 직무상 행위는 처분행위에 한정되지 않고 공무원이 직무상 수행할 수 있는 모든 행위를 포함한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 행위가 공무원이 직무상 수행할 수 있는 행위인지 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.4_59` / `Ⅲ.4`: “‘직무상의 행위’란 협의의 공무집행방해죄와 마찬가지로 권리를 설정하 고 의무를 부과하는 등 일정한 법률상의 효과를 발생시키는 행위인 처분행위에 한하지 아니하고 널리 공무원이 직무상 수행할 수 있는 모든 행위를 포함한다.”

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

## 52. `art136_sec3_5.act.violence_or_threat`

- proposition: 직무·사직강요죄의 행위는 공무원에 대한 폭행 또는 협박이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행 또는 협박 해당성은 구체적 사실관계에 대한 법적 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.5_61` / `Ⅲ.5`: “공무원에 대하여 폭행이나 협박을 하는 것이다.”

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

## 53. `art136_sec3_5.completion.abstract_danger`

- proposition: 직무·사직강요죄는 직무상 행위의 강요·저지 또는 사직을 목적으로 공무원에게 폭행 또는 협박을 하면 기수에 이르며, 공무원이 목적대로 직무행위를 하거나 하지 않거나 또는 사직하는지 여부는 성립에 영향을 주지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 목적의 존재와 그 내용은 구체적 사실관계에 대한 평가가 필요하며, 결과 발생은 성립요건으로 취급하지 않는다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.5_61` / `Ⅲ.5`: “상적 위험범으로서 공무원에 대하여 그 직무상의 행위를 강요 또는 저지하거나 그 직을 사퇴하게 할 목적으로 폭행 또는 협박을 함으로써 곧바로 기수에 이른 다고 보아야 한다.”
  - `comm_001692_제136조_Ⅲ.5_61` / `Ⅲ.5`: “따라서 폭행이나 협박을 받은 공무원이 행위자가 목 (통설) 적한 대로 직무상의 행위를 하든 하지 아니하든 또는 공무원 직을 사퇴하든 하 지 아니하든 본죄의 성립에 영향이 없다.”

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

## 54. `art136_sec3_6.assault_threat_absorption`

- proposition: 직무·사직강요죄가 성립하면 폭행죄 또는 협박죄는 흡수되어 별도의 죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 직무·사직강요죄 성립을 전제로 폭행죄 또는 협박죄의 별도 성립을 배제하는 흡수관계로 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅲ.6_62` / `Ⅲ.6`: “본죄가 성립할 때 폭행죄나 협박죄는 본죄에 흡수되어 별도의 죄를 구성하지 아니한다.”

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
