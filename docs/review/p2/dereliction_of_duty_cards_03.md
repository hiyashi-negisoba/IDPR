# 직무유기 RuleIR 카드 검수 3

- unit: `dereliction_of_duty`
- articles: art122
- cards: 31–45 / 49
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art122_sec2_3.disciplinary_decision_delay_no_offense`

- proposition: 교육기관·교육행정기관·지방자치단체 또는 교육연구기관의 장이 법률상·사실상 장애 없이 징계의결서 통보일부터 법정 시한이 지나도록 집행을 유보하였더라도, 그 유보가 직무에 관한 의식적인 방임 또는 포기에 해당하지 않으면 직무유기죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 법정 시한 경과 및 법률상·사실상 장애의 부재만으로 고의를 추정하지 않으며, 유보의 의식적인 방임 또는 포기 해당성을 별도로 평가해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.3_10` / `Ⅱ.3`: “교육기관·교육행정기관·지방자치단체 또는 교육연구기관의 장이 징계의결을 집행하지 못할 법률상·사실상의 장애가 없는데 도 징계의결서를 통보받은 날로부터 법정 시한이 지나도록 집행을 유보하는 모 든 경우에 직무유기죄가 성립하는 것은 아니고, 그러한 유보가 직무에 관한 의식 적인 방임이나 포기에 해당한다고 볼 수 있는 경우에 한하여 직무유기죄가 성립 한다고 보아야 한다.”

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

## 32. `art122_sec2_3.intent_conscious_abandonment`

- proposition: 직무유기죄 성립에는 직무를 유기한다는 인식이 필요하며, 단순히 태만·분망·착각 등으로 부당한 결과를 초래한 경우에는 고의가 성립하지 않는다. 그 인식에는 의식적인 방임 또는 포기와 같은 적극적 요소가 요구된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 의식적인 방임 또는 포기에 해당하는지는 개별 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.3_10` / `Ⅱ.3`: “본죄의 성립에는 직무를 유기한다는 인식이 있을 것을 요한다.”
  - `comm_001692_제122조_Ⅱ.3_10` / `Ⅱ.3`: “단 순히 직무집행과 관련하여 태만·분망·착각 기타 일신상의 사유로 부당한 결과 를 초래한데 불과한 경우는 고의가 성립하지 않는다. 그리고 여기에서의 인식은 비록 목적하는 것은 아닐지라도 의식적인 방임 내지 포기 등과 같이 적극적인 요소가 있음을 요한다.”

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

## 33. `art122_sec2_5.instigation_per_public_official`

- proposition: 직무유기교사죄는 피교사 공무원별로 하나의 죄가 성립하므로, 공소사실은 피교사 공무원별로 사실을 특정할 수 있게 기재해야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피교사 공무원별 죄수 및 공소사실 특정 단위를 기계적으로 구분하는 범위의 카드다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.5_17` / `Ⅱ.5`: “직무유기교사죄는 피교사자인 공무원별로 1개의 죄가 성립하므로 피교사자인 공”
  - `comm_001692_제122조_Ⅱ.5_17` / `Ⅱ.5`: “무원별로 사실을 특정할 수 있도록 공소사실을 기재하여야 한다.”

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

## 34. `art122_sec2_5.repeated_abandonment_comprehensive_single_offense`

- proposition: 직무유기의 위법상태가 계속되는 동안 추가된 수차례의 직무유기행위는 포괄일죄가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 계속되는 위법상태와 그 기간 중 추가된 직무유기행위라는 범위 내에서만 포괄일죄 관계를 정리한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.5_17` / `Ⅱ.5`: “직무유기의 위법상태가 계속 존재하는 상”
  - `comm_001692_제122조_Ⅱ.5_17` / `Ⅱ.5`: “태에서 그 이후 더해지는 수차에 걸친 직무유기행위는 포괄일죄가 된다.”

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

## 35. `art122_sec3_2.false_document_concealment_absorption`

- proposition: 위법사실을 적극 은폐할 목적으로 허위공문서를 작성·행사한 경우에는 직무위배의 위법상태가 허위공문서작성 행위에 포함되어 허위공문서작성죄만 성립하고 직무유기죄는 별도로 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위공문서작성·행사의 적극적 은폐 목적과 직무위배 상태의 포함 관계를 개별 사실관계에서 평가해야 하는 commentary-reported precedent이다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.2_19` / `Ⅲ.2`: “그 직무위배의 위법상태는 허위로 공문서를 작성할 당시부터 그 속에 포함”
  - `comm_001692_제122조_Ⅲ.2_19` / `Ⅲ.2`: “되어 허위공문서작성죄만 성립하고 직무유기죄는 따로 성립하지 아니한다.”

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

## 36. `art122_sec3_2.false_document_farmland_neglect_real_concurrence`

- proposition: 농지 일시전용허가를 위해 허위 현장출장복명서와 심사의견서를 작성한 행위가 농지불법전용 사실 은폐를 직접 목적으로 한 것이 아닌 경우, 허위공문서작성·행사죄와 직무유기죄는 실체적 경합범 관계이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위공문서작성·행사의 목적 및 직무위배 상태가 해당 작위에 포함되는지 여부에 따라 흡수 관계와 실체적 경합 관계를 구별하여 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.2_19` / `Ⅲ.2`: “허위공문서작성, 동 행사죄와 직무유기죄가 실체적 경합범관계에 있다.”

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

## 37. `art122_sec3_2.farmland_illegal_conversion_inaction`

- proposition: 농지불법전용 사실을 알게 된 담당자가 보고하여 원상회복명령·고발 등 적절한 조치를 가능하게 할 의무가 있음에도 이를 외면하고 아무 조치를 하지 않은 경우 직무유기죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 담당자의 조치 의무, 인식, 조치 가능성 및 직무저버림 여부의 적용에는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.2_19` / `Ⅲ.2`: “피고인이 농지불법전용사실을 애써 외면하고 아무런 조치를 취하”
  - `comm_001692_제122조_Ⅲ.2_19` / `Ⅲ.2`: “지 않은 것은 자신의 직무를 저버린 행위로서 농지의 보전, 관리에 관한 국가의 기능을 저해하며 국민에게 피해를 야기시킬 가능성이 있어 직무유기죄가 성립”

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

## 38. `art122_sec3_3.evidence_destruction_absorption`

- proposition: 증거인멸죄만 성립하고 부작위범인 직무유기죄는 따로 성립하지 않는다고 판시되었다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 증거인멸 작위와 직무위배 상태의 포함 관계 및 판례 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.3_20` / `Ⅲ.3`: “이와 같은 경우에는 작위범인 증거인멸죄만이 성립하고 부작위범인 직무유기죄는 따로 성립하”
  - `comm_001692_제122조_Ⅲ.3_20` / `Ⅲ.3`: “지 아니한다고 판시하였다.”

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

## 39. `art122_sec3_3.indictment_scope_overlapping_offenses`

- proposition: 동시에 성립한다고 할 수 없는 두 범죄 중 하나로 공소가 제기된 경우, 법원은 현실적 심판대상이 아닌 미기소 범죄의 성립을 이유로 공소제기된 범죄가 성립하지 않는다고 판단할 수 없고 공소제기된 내용에 대하여 판단하여야 한다는 취지로 이해된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 해설의 이해로 제시된 내용이므로 관련 판례 원문과 법조경합 관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.3_21` / `Ⅲ.3`: “두 개의 범죄가 동시에 성립한다고 할 수 는 없지만 공소제기권자가 그중 하나의 범죄로 공소를 제기한 이상 법원은 공 소제기 되지 않아 현실적 심판대상이 아닌 범죄에 대하여 그 성립을 인정하고 이를 이유로 공소제기된 범죄가 성립하지 않는다고 판단할 수는 없고 공소제기 된 내용에 대하여 판단을 하여야 한다는 취지로 이해된다.”

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

## 40. `art122_sec3_3.offender_escape_absorption`

- proposition: 작위범인 범인도피죄만 성립하고 부작위범인 직무유기죄는 따로 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 범인도피 작위에 직무위배 상태가 포함되는지와 판례 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.3_20` / `Ⅲ.3`: “작위범인 범인도피죄만이 성립하고 부작위범인 직무유기죄는 따로 성립하지 아니한다는 것이 판례이다.”

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

## 41. `art122_sec3_3.office_abuse_prosecutorial_choice`

- proposition: 검사는 재량에 따라 의무 없는 일을 하게 함으로 인한 직권남용권리행사방해죄로 공소를 제기할 수도 있고, 그 경우 법원이 그 공소범위 내에서 직권남용권리행사방해죄로 인정하여 처벌하는 것은 가능하다고 판시되었다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공소제기 범위 및 두 행위 태양에 관한 판례 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.3_21` / `Ⅲ.3`: “공소제기권자인 검사는 위와 같은 사 안에 있어 재량에 따라 의무 없는 일을 하게 함으로 인한 직권남용권리행사방 해죄로 공소를 제기할 수도 있는 것이므로 그 경우 법원이 그 공소범위 내에서 직권남용권리행사방해죄로 인정하여 처벌하는 것은 가능하다는 판시”

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

## 42. `art122_sec3_3.office_abuse_two_modes_absorption`

- proposition: 권리행사방해와 의무 없는 일을 하게 함의 두 행위 태양에 모두 해당하는 것으로 기소된 경우, 권리행사를 방해함으로 인한 직권남용권리행사방해죄만 성립하고 의무 없는 일을 하게 함으로 인한 직권남용권리행사방해죄는 따로 성립하지 않는다고 판시되었다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 직권남용권리행사방해죄의 두 행위 태양 사이 관계와 판례 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.3_21` / `Ⅲ.3`: “위 두 가지 행위 태양에 모두 해당하는 것으로 기소된 경우 권리행사를 방해함으로 인한 직권남용권리행사방 해죄만 성립하고 의무 없는 일을 하게 함으로 인한 직권남용권리행사방해죄는 따로 성립하지 않는다고 판시”

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

## 43. `art122_sec3_4.deceptive_obstruction_excludes_dereliction`

- proposition: 직무위배의 위법 상태가 위계에 의한 공무집행방해에 포함되는 경우, 작위범인 위계에 의한 공무집행방해죄만 성립하고 부작위범인 직무유기죄는 별도로 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무위배의 위법 상태가 위계에 의한 공무집행방해에 포함되는지 여부는 구체적 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.4_22` / `Ⅲ.4`: “직무위배의 위법 상태가 위계에 의 한 공무집행방해 속에 포함되어 있는 것이라고 보아야 할 것이므로, 이와 같은 경우에는 작위범인 위계에 의한 공무집행방해죄만이 성립하고 부작위범인 직무 유기죄는 따로 성립하지 아니한다.”

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

## 44. `art122_sec3_5.building_instigation_excludes_dereliction`

- proposition: 위법건축물을 예방·단속할 직무상 의무가 있는 읍장이 그 건축을 교사한 경우, 그 직무위배의 위법상태가 건축법위반 교사행위에 내재하면 직무유기죄는 별도로 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판시의 직무상 의무, 교사행위 및 위법상태 내재성 요건을 원판결로 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.5_23` / `Ⅲ.5`: “발생하지 않도록 예방·단속하게 하여야 할 직무상 의무있는 읍장이 위법건축물을 건축하도록 교사한 경우에도 그 직무위배의 위법상태는 건축법위반 교사행위에 내재하고 있는 것이므로 직무유기죄는 따로 성립하지 아니한다.”

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

## 45. `art122_sec3_5.dereliction_and_instigation_concurrent_offenses`

- proposition: 동일한 사실에 관하여 자신의 직무를 유기하면서 타인에게도 직무유기를 교사한 경우, 직무유기죄와 직무유기교사죄의 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판시의 동일 사실관계 및 경합범 판단을 원판결로 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.5_23` / `Ⅲ.5`: “동일한 사실에 관하여 자신의 직무를 유기하면서 타인에게도 직무유기를 교사 한 경우 직무유기죄와 직무유기교사죄의 경합범이 된다.”

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
