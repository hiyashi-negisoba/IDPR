# 과실치사·업무상과실치사상 RuleIR 카드 검수 3

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 31–45 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 31. `art268.multiple_victims_imaginary_concurrence`

- proposition: 하나의 업무상 과실 또는 중과실 행위로 여러 사람을 사망 또는 상해에 이르게 한 경우 수개의 죄의 상상적 경합이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 하나의 업무상 과실 또는 중과실 행위와 복수의 사망·상해 결과가 있는 경우의 죄수 관계를 기술한 카드다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.1_107` / `Ⅲ.1`: “1개의 업무상 과실 혹은 중과실 행위로 수인을 사망이 나 상해에 이르게 하면 수개의 죄의 상상적 경합이 된다.”

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

## 32. `art268.nonperiodic_owner_not_work`

- proposition: 건물 소유자가 비정기적으로 수리하거나 일부를 임대한 사정만으로는 안전관리 사무에 계속 종사하는 지위가 인정되지 않아 업무상과실치상죄의 업무로 보기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소유자에게 별도 법령상·계약상 안전관리 지위가 있는지는 이 카드의 범위 밖에서 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_5` / `Ⅰ.2`: “안전배려 내지 안전관리 사무에 계속적으로 종사하여 위와 같은 지위로서의 계속성을 가지지 아니한 채 단지 건물의 소유자로서 건물을 비정기적으로 수리하거나 건물의 일부분을 임대하였다는 사정만으로는 업무상과실치상죄에 있어서의 ‘업무’로 보기 어렵다.”

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

## 33. `art268.occupational_negligence_definition`

- proposition: 업무상 과실은 해당 업무의 종류나 성질상 요구되는 주의의무를 태만히 하여 결과발생을 예견하거나 회피하지 못한 경우를 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 예견가능성·회피가능성의 사실판단이 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_9` / `Ⅰ.2`: “업무상 과실이란 해당 업무의 종류나 성질상 요구되는 주의의무를 태만히 함으로써 결과발생을 예견하거나 회피하지 못한 경우를 말한다.”

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

## 34. `art268.pedestrian_reliance_limited`

- proposition: 보행자에 대한 교통사고에서는 신뢰의 원칙이 철저히 적용되지 않는다는 판례 경향이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보행신호, 횡단보도, 보행자의 외관상 취약성 및 위험장소 여부를 세분하여 판례 원문으로 검증해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_12` / `Ⅰ.2`: “판례는 보행자에 대한 사고에서는 신뢰의 원칙을 철저하게 적용하지는 않는 것으로 이해되고 있다.”

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

## 35. `art268.permitted_risk`

- proposition: 사회적 유용성과 필요성상 허용된 위험의 경우에는 결과예견의무와 결과회피의무를 이행하지 않았더라도 과실을 인정하지 않아 주의의무가 제한될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 허용범위는 업무영역별 구체적 위험·필요성에 따라 별도로 판단해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_11` / `Ⅰ.2`: “‘허용된 위험’의 법리는 사회적 유용성과 필요성이라는 관점에서 일정한 정도의 위험에 대해서는 사회가 그 위험을 감수하여 결과예견의무와 결과회피의무를 이행하지 않았다고 해도 과실을 인정하지 않는 경우를 말한다.”

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

## 36. `art268.personal_capacity_no_exemption`

- proposition: 행위자가 실제로 업무상 필요한 주의를 기울일 능력이 부족하였더라도 사회적 역할과 지위에서 해당 업무에 참여한 이상 업무상 과실은 배제되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 무능력 상태의 자초성 및 직무 인수 경위를 사실관계에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_10` / `Ⅰ.2`: “행위자가 실제로는 업무상 필요한 주의를 기울일 만한 능력을 갖고 있지 않았더라도 사회적인 역할과 지위에서 해당 업무에 참여한 이상 업무상 과실이 배제되지 않는다.”

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

## 37. `art268.professional_benchmark`

- proposition: 업무상 주의의무는 일반사회인이 아니라 행위자가 속한 직업 또는 생활영역 내 일반적 보통인을 표준으로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 직업영역의 일반적 보통인과 구체적 업무환경을 특정해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_10` / `Ⅰ.2`: “여기서 주의의무는 일반사회인을 기준으로 하는 것이 아니라 행위자가 속해 있는 직업이나 생활영역 내의 일반적 보통인을 표준으로 삼는다.”

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

## 38. `art268.rail_engineer_crossing_person`

- proposition: 전용노선을 진행하는 열차라도 횡단자 또는 선로 인근 어린아이를 발견한 경우 구체적 사정에 따라 정차·감속·경적 등 사고방지 조치를 취할 업무상 의무가 있으며, 통행인이 열차 접근을 개의치 않고 선로를 횡단하려는 위험이 있다고 믿을 만한 이유가 있으면 통행인의 과실 여부와 관계없이 충돌회피 조치를 취해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 국내 판례 소개의 구체적 위험기준과 일본 판례 소개의 특별위험 기준을 조화할 법률검토가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_45` / `Ⅰ.2`: “전용노선을 진행하는 기차일지라도 위 노선을 횡단하는 자를 발견한 경우에 기관사로서는 구체적 사정에 따라 정차하거나 경적을 울리는 등 그 횡단자에 대한 사고의 미연방지책을 강구할 업무상 의무가 있다.”
  - `comm_001692_제268조_Ⅰ.2_46` / `Ⅰ.2`: “통행인이 전차의 접근을 개의치 않고 선로를 횡단하려고 하는 위험이 있다고 믿을 만한 이유가 있을 때에는 통행인에게 과실이 있든지 없든지 관계없이 충돌을 피하는 데에 필요한 주의를 해야 할 의무가 있으며, 감속·급정차 등 임기응변의 조치를 취할 의무가 있다는 취지의 법리를 인정하고 있다.”
  - `comm_001692_제268조_Ⅰ.2_47` / `Ⅰ.2`: “선로우측 1m 지점에 서 있는 어린아이를 보고도 정차하지 아니하고 그대로 진행한 기관차의 기관사는 업무상의 주의의무를 다하였다고 할 수 없다고 판시하고 있다.”

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

## 39. `art268.rail_worker_reliance`

- proposition: 철도 공사관계자 등이 위험성과 합리적 피양방법을 숙지하고 열차접근 시 피양하도록 정해진 경우, 승무원은 특별한 사정이 없으면 그들이 피양조치를 할 것을 신뢰할 수 있다. 다만 관계자가 피양하지 못해 당황한 경우 또는 차량 접근을 알아차리지 못해 위험한 상태임을 쉽게 알 수 있는 경우에는 감속·급정차·서행·파수 등 조치가 필요할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공사관계자의 숙련·교육, 피양 가능성, 승무원의 인식 가능성을 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_51` / `Ⅰ.2`: “동력차승무원 혹은 조차장의 입환작업의 계원들은 특별한 사정이 없는 한, 궤도주변의 위험한 위치에 있는 자가 위험에 대처하여 합리적인 피양조치를 취할 것이라고 신뢰하여도 괜찮을 것이다.”
  - `comm_001692_제268조_Ⅰ.2_51` / `Ⅰ.2`: “특히 철교 위와 같은 데에서 관계자가 피양하지 못해 당황하고 있을 경우에만 급정차·감속 등의 조치를 취할 필요가 있을 뿐이다.”
  - `comm_001692_제268조_Ⅰ.2_52` / `Ⅰ.2`: “공사관계자가 차량의 접근을 알아차리지 못해서 위험한 상태에 있다는 사실을 용이하게 알 수 있을 경우에만 서행 혹은 파수를 하게 하는 등의 조치가 필요하게 된다.”

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

## 40. `art268.red_crosswalk_reliance`

- proposition: 교통이 빈번한 도로에서 횡단보도 보행신호가 적색이고 특별한 사정이 없는 경우, 운전자에게 보행자가 적색신호를 무시하고 갑자기 진입할 것까지 예견하여 방어조치를 취할 업무상 주의의무는 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특별사정과 보행자·위험장소 인식 여부가 있으면 적용되지 않을 수 있다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_14` / `Ⅰ.2`: “자동차운전자에게 보행자가 동 적색신호를 무시하고 갑자기 뛰어나오거나 반대차선상에 정지하여 있는 차량의 뒤로 보행자가 횡단보도를 건너오리라는 것까지 미리 예견하여 운전하여야 할 업무상의 주의의무까지는 없다고 설시하였다.”
  - `comm_001692_제268조_Ⅰ.2_22` / `Ⅰ.2`: “횡단보도의 신호가 적색인 상태에서 정차한 차량 사이로 보행자가 건너오지 않을 것으로 신뢰할 수 있었다 할 것이고, 이러한 신뢰의 원칙이 배제될 특별한 사정은 없다는 이유로 원심을 파기하였다.”

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

## 41. `art268.reliance_known_or_unreliable_other`

- proposition: 상대방의 규칙 위반을 이미 인식한 경우, 노인·장애인·어린아이 등 상대방의 규칙준수를 기대할 수 없는 사정을 외관상 인지할 수 있는 경우, 또는 경험칙상 위험상황이 예상되는 장소임을 인식한 경우에는 신뢰의 원칙을 원용할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방의 취약성 또는 위험장소를 실제로 인식했거나 외관상 인식할 수 있었는지를 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_15` / `Ⅰ.2`: “상대방의 규칙 위반을 이미 인식한 경우에도 신뢰의 원칙을 원용할 수 없다.”
  - `comm_001692_제268조_Ⅰ.2_15` / `Ⅰ.2`: “운전자가 외견상 상대방의 규칙준수를 기대할 수 없는 경우라고 인지할 수 있을 때에만 신뢰의 원칙을 원용하지 못하는 것이다.”
  - `comm_001692_제268조_Ⅰ.2_16` / `Ⅰ.2`: “평소의 경험지식에 비추어 볼 때 위험상황이 예상되는 경우에도 신뢰의 원칙을 원용할 수 없다.”

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

## 42. `art268.reliance_principle_general`

- proposition: 위험 업무 종사자가 스스로 주의의무를 다하고 타인도 주의의무를 다할 것이라고 신뢰하는 것이 상당하면, 타인의 주의의무 위반으로 법익침해 결과가 발생해도 그 결과에 책임지지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 자기 주의의무 이행과 신뢰 상당성은 각각 독립적으로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_11` / `Ⅰ.2`: “스스로 주의의무를 다하면서 타인도 주의의무를 다 할 것이라고 신뢰하는 것이 상당한 경우에는 비록 타인이 주의의무를 준수하지 않음으로 말미암아 법익침해의 결과가 발생한다고 해도 자신은 그 결과에 대해 책임을 지지 않는 것을 말한다.”

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

## 43. `art268.road_reliance_principle`

- proposition: 도로교통에서 교통규칙을 준수한 운전자는 다른 교통관여자도 교통규칙을 준수할 것을 신뢰하면 족하고, 상대방의 교통규칙 위반까지 예견하여 방어조치를 취할 의무는 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 보행자·어린이·위험장소·상대방 위반 인식 등 제한사유 카드를 함께 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_11` / `Ⅰ.2`: “도로교통에서의 신뢰의 원칙은 스스로 교통규칙을 준수한 운전자는 다른 교통관여자도 교통규칙을 준수할 것을 신뢰하면 족하고 그가 교통규칙을 위반할 것까지 예견하여 이에 대한 방어조치를 취할 의무는 없다는 것을 말한다.”

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

## 44. `art268.secondary_rail_accident_prevention`

- proposition: 제1사고 발생을 알고 다른 열차의 현장 접근 전 그 진입을 막을 유효한 조치를 취할 수 있는 자가 이를 하지 않고 시간을 허비하면 그 부작위는 제2사고의 원인이 되어 과실책임을 부담할 수 있으며, 사고로 인한 실신·보행불능의 중상 등으로 적절한 조치를 할 수 없는 경우를 제외하면 당황하여 판단력을 잃었다는 사정은 면책사유가 되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 조치권한·가능시간·통신수단 및 제2사고 회피 가능성을 개별적으로 증명해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_56` / `Ⅰ.2`: “당해 열차의 현장진입을 저지하기 위한 유효한 조치를 취할 수 있는 입장에 놓여 있는 자가 사고의 발생을 알면서도 그와 같은 조치를 취하려고 생각하지 않고 시간을 헛되이 보냈을 때에는 이와 같은 자의 부작위도, 발생한 제2사고에 대한 하나의 원인이 되는 것으로서 과실책임을 부담해야 할 것이다.”
  - `comm_001692_제268조_Ⅰ.2_56` / `Ⅰ.2`: “사고로 인한 심신의 고장, 실신·보행불능의 중상 때문에 적절한 조치를 취할 수 없는 경우를 제외하고는 당황한 나머지 판단력을 잃었다는 따위의 사정은 주의의무의 준수가능성을 부정할 면책사유로는 될 수 없다고 해석된다.”

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

## 45. `art268.ship_collision_other_fault`

- proposition: 선박 충돌사고에서 상대 선박에 중대한 과실이 있어도 자기 선박의 항행책임자 측이 상대방 과실 또는 접근을 인식하고 사고회피 조치를 취할 수 있었다면 감속·통신 등 결과회피를 위해 최선을 다할 의무가 있어 과실책임을 면할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방 위반의 인식, 회피수단 및 회피가능성을 별도로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_58` / `Ⅰ.2`: “상대방의 과실을 인정하고, 사고회피의 조치를 취할 수 있었다고 인정되는 한 결과회피를 위하여 최선을 다할 의무가 있으며, 과실책임을 면할 수 없는 것으로 해석해야 할 것이다.”
  - `comm_001692_제268조_Ⅰ.2_60` / `Ⅰ.2`: “다른 선박의 존재를 탐지할 수 있는 충분한 여유가 있는 시기에 우선 적당한 정도로 속력을 줄여 양 선박이 가지고 있는 무선전화를 활용해야 할 의무가 있고, 상대방의 선장에게 중대한 운행상의 과실이 있었다고 하더라도 위 의무를 다하기만 했다면 충돌을 회피할 수가 있었을 경우에는 과실책임을 면할 수가 없다.”

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
