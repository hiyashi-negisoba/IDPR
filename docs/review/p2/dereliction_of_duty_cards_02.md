# 직무유기 RuleIR 카드 검수 2

- unit: `dereliction_of_duty`
- articles: art122
- cards: 16–30 / 49
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art122.traffic_investigation_abandonment`

- proposition: 중요법규 위반으로 인적 피해가 발생했거나 발생 가능성이 높은 교통사고에 관하여 수사서류 작성, 피해자료 확보, 보고, 입건 및 송치를 하지 않고 가해자를 훈방한 경우, 의식적 직무 방임·포기로 직무유기에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사고의 중요성, 각 수사의무 및 훈방 조치의 결합을 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “피고인의 위와 같은 행동은 직무에 관한 의식적인 방임 내지 포기 등에 해당하여 피고인이 정당한 사유 없이 교통사고 수사직무를 수”
  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “행하지 아니하였다고 보아야 한다.”

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

## 17. `art122.unapproved_delegation_no_supervision`

- proposition: 업무담당자가 승인 없이 장기간 업무와 관인·열쇠 등을 부하에게 맡기고 확인·감독도 하지 않은 경우, 관례상 정당한 위임 범위를 벗어난 의식적 직무 포기로서 직무유기죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 적법하거나 관례상 허용되는 위임과 의식적 직무 포기를 구별해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “이는 부대관례에 따른 정당”
  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “한 위임의 정도를 벗어난 직무의 의식적인 포기로서 직무유기죄에 해당한다.”

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

## 18. `art122_sec1_1.establishment_requirements`

- proposition: 직무유기죄는 공무원의 추상적 충근의무 태만 일반으로 성립하는 것이 아니라, 국가기능 저해, 국민 피해의 구체적 위험성 및 불법·책임비난 정도가 높은 법익침해가 모두 충족된 경우에 한하여 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 보고한 판시 내용이다. 국가기능 저해, 국민 피해의 구체적 위험성 및 높은 불법·책임비난 정도의 충족 여부는 사실관계 평가를 필요로 하며, 원판례 확인 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “직무유기죄는 공무원이 법령·내규 등에 의한 추상적 충근의무를 태만”
  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “히 하는 일체의 경우에 성립하는 것이 아니라, 직장의 무단이탈이나 직무의 의”
  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “식적인 포기 등과 같이 국가의 기능을 저해하고 국민에게 피해를 야기시킬 구”
  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “체적 위험성이 있고 불법과 책임비난의 정도가 높은 법익침해의 경우에 한하여 성립한다고 판시하였다. 즉 ⅰ) 국가의 기능 저해, ⅱ) 국민에게 피해를 야기시”
  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “킬 구체적 위험성, ⅲ) 불법과 책임비난의 정도가 높은 법익침해라는 요건이 모”
  - `comm_001692_제122조_Ⅰ.1_1` / `Ⅰ.1`: “두 충족되어야 한다.”

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

## 19. `art122_sec2_1.definition_criminal_public_official`

- proposition: 직무유기죄에서 공무원은 법령에 따라 국가·지방자치단체·공공단체와 공법상 근무관계에서 공직을 수행하는 자이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 근무관계와 공직 수행의 해당 여부는 개별 법령 및 직무 성질에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “여기서 공무원은 법령에 의하여 국가나 지방자치단체 및 공공단체와 공법상 근무관계에서 공직을 수행 하는 자라고 할 것이다.”

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

## 20. `art122_sec2_1.exception_sick_leave_official`

- proposition: 병가 중인 공무원은 구체적인 작위의무나 국가기능 저해의 구체적 위험성이 없어 직무유기죄의 주체가 될 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 병가 중이라는 사정만이 아니라 구체적 작위의무 및 국가기능 저해의 구체적 위험성 유무를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.1_5` / `Ⅱ.1`: “병가 중인 공무원은 구체적인 작위의무 내지 국가기능 저해에 대한 구체적 위험성이 있다고 할 수 없기 때문에 본죄의 주체가 될 수 없다.”

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

## 21. `art122_sec2_1.exception_simple_laborer_not_official`

- proposition: 청소부·인부·사환 등 단순한 기계적·육체적 노무에 종사하는 자는 형법상 공무원 개념에서 제외된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 단순 기계적·육체적 노무 종사자를 공무원 정의에서 제외하는 명시적 예외다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “청소부, 인부, 사환 등과 같이 단순한 기계적, 육체적 노무에 종사하는 자는 형법상의 공무원 개념에는 제외된다.”

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

## 22. `art122_sec2_1.offender_public_official`

- proposition: 직무유기죄는 공무원이라는 특수신분을 가진 자만 행위주체가 될 수 있는 진정신분범 및 진정직무범죄이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행위주체의 특수신분 요건을 나타내는 카드이며, 공무원 해당 여부는 별도 정의 및 예외 카드에 따라 검토한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “직무유기죄는 공무원이라는 특수한 신분을 가진 자만이 구성요건요소로서의 행 위주체가 될 수 있는 진정신분범, 진정직무범죄에 해당한다.”

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

## 23. `art122_sec2_1.standard_public_corporation_employee`

- proposition: 공법인의 직원이라도 사무 성질이 사경제적이어서 특별한 형법상 보호가치가 없으면 형법상 공무원에 해당하지 않으며, 직무유기죄에서 공법인 직원을 공무원으로 보는 것은 법령의 명시적 근거가 있는 경우에 한정하는 견해가 제시된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공법인 사무의 성질, 형법상 보호가치 및 명시적 법령 근거를 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “공법인일지라도 그 목”
  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “적으로 하는 사무의 성질이 사경제적이고 사법인의 사무와 다름이 없어 형법상 특별한 보호가치가 없는 경우에는 그 직원이라 할지라도 형법상의 공무원에는 해당한다고 볼 수 없다.”
  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “직무유기죄에 있어서 공”
  - `comm_001692_제122조_Ⅱ.1_4` / `Ⅱ.1`: “무원으로 보는 공법인의 직원은 법령에 명시적 근거가 있는 경우에 한한다고 보는 것이 타당하다.”

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

## 24. `art122_sec2_2.abstract_or_derivative_duty`

- proposition: 공무원 신분관계에서 인정되는 추상적 의무 및 부수적·파생적 직무는 직무유기죄의 직무에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 해당 의무가 추상적·부수적 의무인지 본래의 구체적 직무인지 구분하여 검토한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_7` / `Ⅱ.2`: “공무원인 신분관계로 인해 인정되는 추상적 의무는 직무에 해당하지 않는다.”
  - `comm_001692_제122조_Ⅱ.2_7` / `Ⅱ.2`: “본죄의 직무에는 공무원인 신분관계로 인하여 부수적·파생적으로 발생하는 직 무는 여기에 포함되지 않는다.”

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

## 25. `art122_sec2_2.conscious_abandonment`

- proposition: 직무유기란 정당한 이유 없이 직무에 관한 의식적인 방임 또는 포기 등으로 직무를 수행하지 않은 경우를 의미한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 의식적인 방임 또는 포기와 정당한 이유의 부재는 구체적 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_8` / `Ⅱ.2`: “직무를 유기한 때라 함은 직무에 관한 의식적인 방임 내지는 포기 등 정당한 이 유 없이 그 직무를 수행하지 아니한 경우를 의미한다.”

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

## 26. `art122_sec2_2.duty_legal_basis`

- proposition: 직무는 법령에 의해 공무원에게 부여된 의무이고, 그 내용은 성문 법령의 근거 또는 특별한 지시나 명령이 있어야 하며, 그러한 직무집행의무가 확정되지 않으면 직무유기죄 성립을 인정할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 법령상 근거, 특별 지시·명령, 그리고 해당 사안에서의 직무집행의무 확정을 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_6` / `Ⅱ.2`: “직무는 법령에 의해 공무원에게 부여된 의무를 말한다. 직무의 내용은 성문에 의한 법령에 근거가 있거나 특별한 지시 또는 명령이 있어야 한다.”
  - `comm_001692_제122조_Ⅱ.2_6` / `Ⅱ.2`: “직무집행의 의무가 있음을 확정한 후가 아니면 직무유기죄의 성립을 인정할 수 없다.”

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

## 27. `art122_sec2_2.duty_specific_original`

- proposition: 직무유기죄의 직무는 공무원이 그 지위에 따라 맡은 공무원법상 본래의 구체적 직무를 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 개별 공무원의 구체적 직무 해당성은 지위와 담당 사무를 바탕으로 검토한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_6` / `Ⅱ.2`: “직무유기죄에 있어서의 직무는 공무원이 그 지위에 따라 맡은 공무원법상의 본래의 구체적인 직무를 말한다.”

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

## 28. `art122_sec2_2.mere_negligence_or_defective_performance`

- proposition: 태만·분망·착각 등으로 직무집행을 성실히 하지 못한 것, 형식적 또는 소홀한 직무집행, 법정절차 미이행이나 직무내용 부실만으로는 직무유기죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 단순한 불성실·절차위반·부실 수행과 의식적인 방임 또는 포기를 구별해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_8` / `Ⅱ.2`: “태만, 분망, 착각 등으로 인하여 직무집행을 성실 히 이행하지 아니한 것에 불과한 경우나 형식적으로 또는 직무를 소홀히 집행 하였기 때문에 성실한 직무수행을 못한 것으로 귀착되는 경우에는 직무유기죄 가 성립하지 아니한다. 직무를 수행함에 있어서 직무집행에 따른 법정 절차를 이행하지 않았거나, 내용이 부실하다고 하여도 본죄는 성립하지 않는다.”

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

## 29. `art122_sec2_2.reporting_crime_within_duty`

- proposition: 범법행위 감시의무가 직무내용의 일부인 공무원은 범법행위를 알게 되면 수사관서에 고발할 의무가 본래 직무에 해당하고, 이를 은폐하기 위해 고발하지 않으면 직무유기죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 감시의무가 실제 직무내용의 일부인지, 범법행위 인지와 은폐 목적이 있었는지를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_8` / `Ⅱ.2`: “범법행위에 대한 감시의무가 그 직무내용의 일부를 이루고 있는 경우에 는 그 직무를 행함에 있어 범법행위가 있음을 알게 되었을 때 이를 수사관서에 고발하여야 할 의무는 그 본래의 직무에 해당한다고 보아야 할 것이다. 따라서 그러한 지위에 있는 공무원이 범법행위를 인지하고서도 이를 은폐하기 위하여 수사관서에 고발하지 아니한 경우에는 직무유기죄가 성립할 수 있을 것이다.”

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

## 30. `art122_sec2_2.unlawful_superior_order`

- proposition: 상관의 직무집행 명령이 법령에 근거가 없거나 위법하면 그 명령에 따른 직무집행의무는 인정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명령의 법령상 근거와 위법성은 구체적 명령 내용 및 관련 법령을 기준으로 검토한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.2_6` / `Ⅱ.2`: “상관의 직무집행 명령 이 법령에 근거가 없거나 위법한 경우라면 그 직무집행 의무가 있다고 볼 수 없다.”

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
