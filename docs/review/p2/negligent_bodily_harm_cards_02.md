# 과실치사·업무상과실치사상 RuleIR 카드 검수 2

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 16–30 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 16. `art268.business_definition`

- proposition: 업무상과실치사상죄의 업무는 사회생활상 하나의 지위에서 계속적으로 종사하는 사무를 말하고, 수행 직무 자체의 위험성 때문에 안전배려가 의무 내용인 경우뿐 아니라 사람의 생명·신체 위험 방지가 의무 내용인 업무도 포함한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 계속성, 사회생활상 지위, 안전배려 또는 위험방지 의무의 내용을 개별 업무별로 확인한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_2` / `Ⅰ.2`: “업무상 과실치사상죄에 있어서의 업무라 함은 사람의 사회생활면에 있어서의 하나의 지위로서 계속적으로 종사하는 업무를 말한다.”
  - `comm_001692_제268조_Ⅰ.2_2` / `Ⅰ.2`: “수행하는 직무 자체가 위험성을 갖기 때문에 안전배려를 의무의 내용으로 하는 경우는 물론 사람의 생명·신체의 위험을 방지하는 것을 의무의 내용으로 하는 업무도 포함한다.”
  - `comm_001692_제268조_Ⅰ.2_5` / `Ⅰ.2`: “업무상과실치상죄에 있어서의 ‘업무’란 사람의 사회생활면에서 하나의 지위로서 계속적으로 종사하는 사무를 말하고, 여기에는 수행하는 직무 자체가 위험성을 갖기 때문에 안전배려를 의무의 내용으로 하는 경우는 물론 사람의 생명·신체의 위험을 방지하는 것을 의무내용으로 하는 업무도 포함”

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

## 17. `art268.business_no_license_requirement`

- proposition: 업무상과실치사상죄의 업무성에는 반복·계속 의사 또는 사실이 있으면 각별한 경험이나 법규상 면허가 필요하지 않고, 수입을 위한 직업·영업일 필요도 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 불법·무면허 활동이 업무인지에 관한 별도 대립 카드를 함께 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_2` / `Ⅰ.2`: “반복 계속의 의사 또는 사실이 있는 한 그 사무에 대한 각별한 경험이나 법규상의 면허를 필요로 하지 아니한다.”
  - `comm_001692_제268조_Ⅰ.2_5` / `Ⅰ.2`: “반드시 수입을 얻기 위한 직업·영업일 필요는 없고, 사회생활을 유지하면서 종사하는 것이면 공무, 사무, 본무, 겸무, 주된 직업의 부수적 업무도 사무에 해당한다.”

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

## 18. `art268.child_near_road_duty`

- proposition: 운전자가 도로 가까이 있는 유아 또는 학교 인근 정차 차량 사이에서 어린이 등이 갑자기 나타날 수 있는 상황을 인식한 경우, 즉시 정차 가능한 정도로 대폭 감속하고 전방·측면을 주시하며 필요시 경음하는 등 사고방지 조치를 취할 주의의무가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 아동의 위치, 외관상 인식 가능성, 차폐물 및 즉시 정차 가능 속도를 구체적으로 확인한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_20` / `Ⅰ.2`: “유아의 곁을 통과하는 운전자는 아동이 차량의 접근 시 돌연 진로전면에 뛰어나오는 돌발사고를 예상하여 그 아이의 곁을 통과할 때에는 즉시 정차시킬 수 있는 시속 4~5㎞의 초저속도로 감속하거나 그 아이의 직전에서 일단 정차하여 사고를 미연에 방지할 주의의무가 있다.”
  - `comm_001692_제268조_Ⅰ.2_22` / `Ⅰ.2`: “정차 중인 차량 사이로 어린이 등 장애물이 갑자기 나타나는 것도 충분히 예견할 수 있는 상황이었으므로, 그에 대비하여 급박한 상황에서 즉시 정차할 수 있을 정도로 속도를 대폭 줄이고, 전방뿐만이 아니라 측면, 특히 좌측을 예의주시하며 필요할 경우 경음기를 울리는 등 조치를 하면서 진행하여야 할 주의의무가 있다.”

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

## 19. `art268.crossing_guard_safe_opening`

- proposition: 복선 건널목 안내원은 한쪽 선로 열차가 통과한 뒤 반대방향 또는 후속 열차가 없음을 확인한 후 건널목을 개방해야 하며, 안전확인을 태만히 하여 개방에 착수한 후 보행자가 선로에 진입하여 열차와 접촉한 경우 피해자에게 중대한 과실이 있어도 안내원의 과실과 사고 사이 인과관계를 부정할 수 없다는 견해가 제시되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 개방행위, 보행자 진입 및 열차 접촉 사이의 구체적 시간관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_50` / `Ⅰ.2`: “건널목 안내원은 한쪽 선의 열차가 통과한 것을 확인한 후, 곧바로 차단기를 개방할 것이 아니라 반대방향에서 오는 열차나 후속열차가 없다는 사실을 확인한 다음 비로소 건널목을 개방해야 할 주의의무를 진다.”
  - `comm_001692_제268조_Ⅰ.2_50` / `Ⅰ.2`: “피해자에게 중대한 과실이 있다고 하더라도 안전확인을 태만히 한 건널목 안내원에게 과실이 있는 이상, 인과관계를 부정할 수 없으며 책임을 면할 수 없다.”

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

## 20. `art268.crosswalk_green_signal_stop`

- proposition: 운전자는 보행자용 신호에 따라 횡단보도를 횡단하는 보행자가 있으면 차량의 횡단보도 진입 선후와 관계없이 일시정지 등 조치로 보행자 통행을 방해하지 않아야 한다. 다만 차량이 먼저 진입했고 계속 진행해도 보행자 횡단을 방해하거나 통행에 위험을 초래하지 않는 경우에는 진행할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보행자 존재, 신호 상태, 차량 선진입 및 실제 방해·위험 여부를 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_13` / `Ⅰ.2`: “모든 차의 운전자는 신호기의 지시에 따라 횡단보도를 횡단하는 보행자가 있을 때에는 횡단보도에의 진입 선후를 불문하고 일시정지하는 등의 조치를 취함으로써 보행자의 통행이 방해되지 아니하도록 하여야 한다고 설시하였다.”
  - `comm_001692_제268조_Ⅰ.2_19` / `Ⅰ.2`: “다만 자동차가 횡단보도에 먼저 진입한 경우로서 그대로 진행하더라도 보행자의 횡단을 방해하지 않거나 통행에 위험을 초래하지 않을 상황이라면 그대로 진행할 수 있다.”

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

## 21. `art268.crosswalk_signal_transition`

- proposition: 보행자 신호가 녹색에서 정지신호로 바뀔 무렵 횡단보도를 통과하는 운전자는 이미 진입한 보행자의 존재와 동태를 살피고 서행하는 등 언제라도 정지할 태세로 운전할 업무상 주의의무가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 신호 전환 시점, 이미 진입한 보행자의 존재 및 회피 가능성을 구체적으로 확인한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_14` / `Ⅰ.2`: “보행자 신호가 녹색신호에서 정지신호로 바뀔 무렵 전후에 횡단보도를 통과하는 자동차 운전자는 보행자가 교통신호를 철저히 준수할 것이라는 신뢰만으로 자동차를 운전할 것이 아니라 좌우에서 이미 횡단보도에 진입한 보행자가 있는지 여부를 살펴보고 또한 그의 동태를 두루 살피면서 서행하는 등하여 그와 같은 상황에 있는 보행자의 안전을 위해 어느 때라도 정지할 수 있는 태세를 갖추고 자동차를 운전하여야 할 업무상의 주의의무가 있다.”

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

## 22. `art268.duty_scope`

- proposition: 업무상 주의의무는 법령상 의무뿐 아니라 관습상·조리상 요구되는 주의의무에도 미치며, 후자의 경우 업무 성질과 구체적 상황을 고려한 결과 예견가능성을 전제로 정상의 주의의무로 나타날 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 법령 외 주의의무의 구체적 내용은 직무·상황별 카드로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_9` / `Ⅰ.2`: “업무상 요구되는 주의의무의 범위는 법령의 규정이 있는 경우뿐만 아니라 관습상·조리상 요구되는 일체의 주의의무에 미친다. 관습상·조리상 요구되는 주의의무는 업무의 성질과 구체적 상황을 고려하여 결과에 대한 예견가능성을 전제로 요구되는 정상의 주의의무로 나타날 수도 있다.”

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

## 23. `art268.emergency_treatment_risk_balance`

- proposition: 긴급성 때문에 충분한 회피조치를 취할 수 없었던 경우에는 충분한 준비 없이 치료하여 의도하지 않은 결과가 발생하였더라도 의사에게 책임을 물을 수 없을 수 있으며, 긴급 치료의 필요 여부는 긴급 치료의 이익과 충분한 준비 없는 치료의 위험을 비교형량하여 전자의 이익이 큰 경우에 허용된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 긴급성의 시점, 준비 가능 조치 및 지연 위험을 객관적 자료로 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_68` / `Ⅰ.2`: “위험한 결과의 발생에 관하여 예견가능하였다 하더라도 긴급성 때문에 충분한 회피조치를 강구할 수 없었다면 의사의 책임을 물을 수 없다고 본다.”
  - `comm_001692_제268조_Ⅰ.2_68` / `Ⅰ.2`: “긴급한 치료를 요하는지 여부는 긴급한 치료에 의한 이익과 충분한 준비 없이 치료함으로 인한 위험을 비교형량하여 전자의 이익이 크다고 판단한 경우에 허용될 것”

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

## 24. `art268.forward_observation`

- proposition: 운전자는 전방 및 상황상 필요한 좌우를 주시하여 위험을 미리 발견하고 적절한 조치를 취해야 하며, 보행자 발견 직후 정차가 불가능했더라도 사전 주시를 다했으면 미리 발견하여 사고를 방지할 수 있었던 경우 주의의무위반이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 시야, 발견 가능 거리, 반응시간 및 대체 회피조치를 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_17` / `Ⅰ.2`: “운전자가 보행자를 발견한 직후 급히 정차조치를 취하여 사고발생을 방지할 수 있는 상황이 아니었다고 하여도, 사전에 전방주시를 게을리 하지 않았으면 미리 피해자를 발견하여 적절한 조치를 취할 수 있었다고 인정되는 경우 주의의무위반이 된다.”
  - `comm_001692_제268조_Ⅰ.2_21` / `Ⅰ.2`: “자동차운전자가 전방만을 보고 좌우에 대한 주시의무를 태만히 하여 도로 좌측에서 우측으로 횡단하려는 피해자를 뒤늦게 발견한 탓으로 사고를 발생케 하였고 좌우를 살피면서 운행하였더라면 사고를 미연에 방지할 수 있었다면 운전수에게 과실이 있다 할 것이다.”

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

## 25. `art268.general_requirements`

- proposition: 업무상과실치사상죄가 성립하려면 과실, 행위자 이외의 다른 사람의 사망 또는 신체상 상해 결과, 그리고 과실과 결과 사이의 인과관계 등 일반적 요건이 충족되어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 결과 및 인과관계는 별도 카드의 구체적 기준과 함께 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_2` / `Ⅰ.2`: “본죄도 다른 과실범과 마찬가지로 그 성립을 위해서 과실, 결과발생, 과실과 결과 사이의 인과관계 등 일반적인 요건이 충족되어야 한다.”
  - `comm_001692_제268조_Ⅰ.2_102` / `Ⅰ.2`: “행위자 이외의 다른 사람이 사망하거나 신체에 상해가 발생하여야 한다.”

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

## 26. `art268.horizontal_medical_division`

- proposition: 의사들이 대등한 지위에서 각자의 의료영역을 나누어 환자 진료 일부를 분담한 경우, 분담받은 다른 의사의 전적인 과실로 발생한 결과에 대해서는 주된 의사의 책임을 인정할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 의사 간 대등성, 의료영역 분담 및 상대방 과실의 전속성을 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_16` / `Ⅰ.2`: “서로 대등한 지위에서 각자의 의료영역을 나누어 환자 진료의 일부를 분담하였다면, 진료를 분담받은 다른 의사의 전적인 과실로 환자에게 발생한 결과에 대하여는 책임을 인정할 수 없다.”
  - `comm_001692_제268조_Ⅰ.2_69` / `Ⅰ.2`: “서로 대등한 지위에서 각자의 의료영역을 나누어 환자 진료의 일부를 분담하였다면, 진료를 분담받은 다른 의사의 전적인 과실로 환자에게 발생한 결과에 대하여는 책임을 인정할 수 없다.”

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

## 27. `art268.industrial_safety_general_duty`

- proposition: 산업안전보건법상 안전·보건조치 의무 이행에 필요한 조치를 다하지 않으면 해당 벌칙 구성요건에 해당하면서 업무상과실치상죄의 업무상 과실에도 해당할 수 있고, 산업안전보건법상 의무위반이 인정되지 않더라도 해당 업무가 요구하는 일반적 주의의무를 게을리한 사정이 있으면 산업재해 영역에서 업무상 과실이 인정될 여지가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 시점의 산업안전보건법령, 역할별 법정 의무 및 일반적 위험방지 의무를 분리해 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_98` / `Ⅰ.2`: “위 의무를 이행하기 위해 필요한 조치를 다하지 않는 경우 산업안전보건법 소정의 벌칙 규정의 구성요건에 해당하면서 업무상 과실치상죄의 업무상 과실에도 해당된다.”
  - `comm_001692_제268조_Ⅰ.2_98` / `Ⅰ.2`: “산업안전보건법에서 정한 의무 위반 사실이 인정되지 않아도 해당 업무가 요구하는 일반적인 주의의무를 게을리 한 사정이 있다면 산업재해 영역에서 업무상 과실이 인정될 여지도 있다.”

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

## 28. `art268.medical_allowed_risk`

- proposition: 의료행위는 허용된 위험 법리가 적용되는 전형적 영역으로 해석되지만, 사회적 유용성만으로 발생한 모든 법익침해가 정당화되는 것은 아니며 구체적 사건에서는 의료행위 위험성과 질병 치유가능성을 비교형량하여 허용 한계를 개별적·구체적으로 검토해야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 비교형량의 지표와 허용 한계는 법률검토로 구체화해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_63` / `Ⅰ.2`: “의료행위는 허용된 위험의 법리가 적용되는 전형적인 경우라고 해석되고 있다.”
  - `comm_001692_제268조_Ⅰ.2_63` / `Ⅰ.2`: “구체적인 사건에 있어서는 당해 의료행위의 위험성과 질병의 치유가능성을 비교형량하여 그 허용될 수 있는 한계를 개별적·구체적으로 검토하지 않으면 안 되는 것으로서”

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

## 29. `art268.medical_negligence_test`

- proposition: 의료사고에서 의사 과실은 결과 예견 가능성 및 회피 가능성이 있었는지를 검토하여 판단하며, 동일 업무·직무 종사 일반인의 주의 정도를 표준으로 의료수준·진료환경·조건 및 의료행위 특수성을 고려한다. 그 기준은 의학 최고수준이 아니라 당시 통상 일반의 의사에게 일반적으로 알려지고 시인된 의학지식·기술의 규범적 수준이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 당시 의료수준과 진료환경을 소급적으로 평가하지 않도록 전문감정 및 진료기록 검토가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_62` / `Ⅰ.2`: “의료사고에 있어서 의사의 과실을 인정하기 위해서는 의사가 결과발생을 예견할 수 있었음에도 불구하고 그 결과발생을 예견하지 못하였고 그 결과발생을 회피할 수 있었음에도 불구하고 그 결과발생을 회피하지 못한 과실이 검토되어야 한다.”
  - `comm_001692_제268조_Ⅰ.2_65` / `Ⅰ.2`: “의사의 이와 같은 주의의무의 내용과 정도 및 과실의 유무는 의료행위를 할 당시 의료기관 등 임상의학 분야에서 실천되고 있는 의료행위의 수준을 기준으로 삼되 그 의료수준은 같은 업무와 직무에 종사하는 통상의 의사에게 의료행위 당시 일반적으로 알려져 있고 또 시인되고 있는 의학의 수준, 진료환경과 조건, 의료행위의 특수성 등을 고려하여 규범적인 수준으로 파악되어야 한다고 판시하였다.”
  - `comm_001692_제268조_Ⅰ.2_65` / `Ⅰ.2`: “의사의 주의의무의 기준으로서 의학의 최고수준에 있어서의 주의의무가 요구된다는 것은 아니다.”

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

## 30. `art268.medical_transfer_duty`

- proposition: 환자에게 적절한 치료나 조치를 취하기 어려운 사정이 있거나 의료설비·의료환경의 불충분으로 평균적 의료수준의 치료가 불가능한 경우, 의사는 다른 전문의의 협력을 구하거나 전문 치료가 가능한 병원으로 신속히 전원시키는 등의 조치를 해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 전원 가능성, 시간적 긴급성, 수용병원 접근성 및 환자 상태를 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_66` / `Ⅰ.2`: “환자에게 적절한 치료를 하거나 그러한 조치를 취하기 어려운 사정이 있다면 신속히 전문적인 치료를 할 수 있는 다른 병원으로의 전원조치 등을 취하여야 한다.”
  - `comm_001692_제268조_Ⅰ.2_68` / `Ⅰ.2`: “의료설비나 의료환경이 불충분하기 때문에 평균적인 의료수준의 치료가 불가능한 경우에는 다른 전문의의 협력을 구한다거나 설비가 완비된 병원에 환자를 전송할 의무가 있다.”
  - `comm_001692_제268조_Ⅰ.2_89` / `Ⅰ.2`: “의사는 환자에게 적절한 치료를 하거나 그러한 조치를 하기 어려운 사정이 있다면 신속히 전문적인 치료를 할 수 있는 다른 병원으로 전원시키는 등의 조치를 하여야 한다.”

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
