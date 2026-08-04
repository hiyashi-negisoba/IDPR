# 직무유기 RuleIR 카드 검수 4

- unit: `dereliction_of_duty`
- articles: art122
- cards: 46–49 / 49
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art122_sec3_5.human_rights_order_and_dereliction_imaginary_concurrence`

- proposition: 소개된 판시에 따르면, 인권옹호직무명령불준수죄와 직무유기죄는 법조경합상 특별관계가 아니라 상상적 경합관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 판시이므로 원판결 및 적용 사실관계 확인이 필요하다.
- bounded sources:

  - `comm_001692_제122조_Ⅲ.5_23` / `Ⅲ.5`: “인권옹호직무명령불준수 죄가 직무유기죄에 대하여 법조경합 중 특별관계에 있다고 보기는 어렵고 양죄 는 상상적 경합관계에 있다고 판시하였다.”

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

## 47. `art122_sec4.military_dereliction_requirements`

- proposition: 군형법 제24조의 직무유기죄가 성립하려면 지휘관으로서 직무를 버린다는 주관적 인식과 직무 또는 직장을 유기하는 객관적 행위가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주관적 인식 및 객관적 유기행위의 충족 여부는 구체적 사실관계 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅳ_24` / `Ⅳ`: “군형법 제24조 소정의 직무유기죄가 성립하려면 지휘관으로서의 직무를 버린다는 주관적인 인식과 직무 또는 직장을 유기하는 객관적인 행위가 있어야 하고”

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

## 48. `art122_sec4.military_inadequate_performance_not_sufficient`

- proposition: 군 지휘관의 대응조치가 미흡하거나 부적절하여 부당한 결과가 발생하였다는 사유만으로는 군형법 제24조의 직무유기죄 성립을 인정할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 부적절한 직무집행과 직무 또는 직장의 유기를 구별하는 적용 기준을 법률 검토로 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅳ_24` / `Ⅳ`: “위와 같이 직무집행의 내용이 적정하지 못하였기 때문에 부당한 결과가 초래되었다고 하여 그 사유만으로 직무유기죄의 성립을 인정할 수 없다.”

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

## 49. `art122_sec4.specific_crimes_act_recognition_threshold`

- proposition: 특정범죄 가중처벌 등에 관한 법률 제15조의 ‘인지’는 확인되지 않은 제보 등에 따라 해당 죄를 범하였을 수도 있다는 의심을 품은 것만으로는 인정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: ‘인지’ 여부는 제보의 확인 정도와 인식 내용에 관한 사실평가를 필요로 하므로 standard input으로 유지한다.
- bounded sources:

  - `comm_001692_제122조_Ⅳ_24` / `Ⅳ`: “단순히 확인되지 않은 제보 등 에 의하여 이러한 죄를 범하였을 수도 있다는 의심을 품은 것만으로는 위 법에 서 규정하고 있는 ‘인지’가 있었다고 할 수 없다.”

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
