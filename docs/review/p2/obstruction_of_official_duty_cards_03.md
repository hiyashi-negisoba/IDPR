# 공무집행방해 RuleIR 카드 검수 3

- unit: `obstruction_of_official_duty`
- articles: art136
- cards: 31–45 / 54
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art136_sec2_4.passive_resistance_not_assault`

- proposition: 닫힌 문을 열어주지 않거나 풀려난 맹견을 묶지 않거나 체포를 방해하려고 앉거나 누워 있는 것만으로는 폭행에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 부작위 또는 소극적 거동만으로는 폭행이 아니라는 제한적 판단이다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_45` / `Ⅱ.4`: “공무원의 출입을 막기 위하 여 닫혀 있는 문을 열어주지 아니하거나 풀려진 맹견을 묶지 아니하는 경우 또 는 체포를 방해하기 위하여 앉거나 누워있는 것만으로는 폭행에 해당한다고 할 수 없다.”

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

## 32. `art136_sec2_4.preplaced_obstacles_not_assault`

- proposition: 경찰관 진입에 대비해 부재 중 미리 바닥에 윤활유나 철판조각을 뿌려 둔 것만으로는, 면전에서 공무집행 방해 의도로 뿌리는 등 특별한 사정이 없는 한 경찰관에 대한 폭행에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 사전 설치 장애물 사안의 판단이며, 특별한 사정의 범위는 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_43` / `Ⅱ.4`: “피고인 등의 위와 같은 행위를 가리켜 피해자들에 대한 폭행에 해당한다고 볼 수 없다고 판단하였다.”

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

## 33. `art136_sec2_4.self_harm_not_assault_or_threat`

- proposition: 경찰관의 임의동행 요구에 피고인이 방 안에서 면도칼로 자해하며 죽겠다고 말한 행위는 자해자학행위일 수 있으나 경찰관에 대한 폭행 또는 협박으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 구체적 사실관계의 소극적 판단이므로 원판례와 사실적 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_42` / `Ⅱ.4`: “자해자학행위는 될지언정 경찰관에 대한 폭행이나 협박으로는 볼 수 없다고 판단하였다.”

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

## 34. `art136_sec2_4.station_disturbance_as_assault`

- proposition: 지구대에서 장시간 큰 소리로 경찰관을 모욕하고 출입문을 반복하여 두드리거나 잡아당기는 등 소란을 피운 행위는 정도에 따라 공무원에 대한 간접적 유형력 행사로서 폭행에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 사안별 판단이며, 원판례 확인 전에는 해당 사실관계 범위를 넘겨 적용하지 않는다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_42` / `Ⅱ.4`: “피고인이 밤늦은 시 각에 술에 취하여 위와 같이 한참 동안 소란을 피운 행위는 그 정도에 따라 공 무원에 대한 간접적인 유형력의 행사로서 폭행에 해당한다고 보았다.”

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

## 35. `art136_sec2_4.third_party_threat`

- proposition: 제3자에 대한 협박이라도 간접적으로 공무원에게 공포심을 일으켜 공무원의 직무집행을 방해할 정도이면 공무원에 대한 협박이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 제3자에 대한 해악고지가 공무원에게 간접적 공포심을 일으키는지 및 직무집행 방해 정도인지는 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_43` / `Ⅱ.4`: “제3자에 대한 협박도 그것이 간접적으로 공무원에게 공포심을 일으키게 하는 것 이어서 공무원의 직무집행을 방해할 정도라면 공무원에 대한 협박이 될 수 있다.”

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

## 36. `art136_sec2_4.threat_definition`

- proposition: 공무집행방해죄의 협박은 상대방에게 공포심을 일으킬 목적으로 해악을 고지하는 것을 의미하며, 해악의 내용·성질 및 고지 방법은 제한되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 공포심 유발 목적과 해악 고지의 해당성은 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_43` / `Ⅱ.4`: “본죄에서 협박이란 상대방에게 공포심을 일으키게 할 목적으로 해악을 고지하는 것을 의미한다. 고지하는 해악의 내용이나 성질이 어떠한지를 불문한다. 그리고 고지의 방법도 언어, 문서, 직접, 간접, 명시, 암시를 가리지 아니한다.”

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

## 37. `art136_sec2_4.threat_objective_factors`

- proposition: 협박의 해악은 경위, 주위상황, 행위자 성향, 당사자 친숙도 및 지위 등 행위 당시 사정을 종합하여 객관적으로 상대방에게 공포심을 일으키기에 충분한 정도인지로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 복수 사정을 종합하는 객관적 충분성 판단이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_43` / `Ⅱ.4`: “고지하는 해악의 내용은 그 경위, 주위상황, 행위자의 성향, 행위자와 상대방과의 친숙의 정 도, 지위 등 상호관계를 비롯한 행위 당시의 여러 사정을 종합적으로 고려하여, 객관적으로 상대방으로 하여금 공포심을 일으키게 하기에 족한 정도이면 된다.”

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

## 38. `art136_sec2_4.vehicle_departure_not_assault`

- proposition: 교통단속 경찰관이 차량 발판에 올라타다가 자신의 부주의로 상해를 입고, 운전자가 정차 과정에서 경찰관이 탄 채로 약간 진행한 것만으로는 경찰관에 대한 폭행이라고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 좁은 사실관계의 판단이므로 운전행위와 경찰관 상해의 구체적 경위를 원판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_42` / `Ⅱ.4`: “이것만으로 교통단속 경찰관에게 폭행을 가 한 것이라 할 수 없다고 판단하였다.”

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

## 39. `art136_sec2_6.illegal_duty_act.other_offenses`

- proposition: 위법한 직무를 집행하는 공무원에 대한 폭행·협박이 공무집행방해죄 구성요건에 해당하지 않거나 위법성이 조각되어도 폭행죄·협박죄 구성요건에는 해당할 수 있으나, 정당방위 또는 정당행위로 그 위법성도 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행죄·협박죄 해당성과 정당방위 또는 정당행위에 따른 위법성 조각은 사안별 평가가 필요하다. 공무집행방해죄의 적법성 위치에 관한 선택과 분리하여 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.6_49` / `Ⅱ.6`: “위법하게 직무를 직행하는 공무원에 대한 폭행 또는 협박 행위가 본죄의 구성요 건에 해당하지 아니하거나 위법성이 조각되더라도 폭행죄나 협박죄의 구성요건에 는 해당할 수 있는데, 이러한 공무원에 대한 폭행 또는 협박 행위는 정당방위나 정당행위에 해당하여 폭행죄나 협박죄의 위법성도 조각되는 경우가 있을 수 있다.”

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

## 40. `art136_sec2_7.assault_threat_absorption`

- proposition: 공무집행방해죄가 성립하면 폭행죄 또는 협박죄는 법조경합으로 흡수되어 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공무집행방해죄 성립이 전제되는 경우의 폭행죄·협박죄 처리 관계를 나타낸다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_51` / `Ⅱ.7`: “본죄와 폭행죄 또는 협박죄 사이에는 법조경합의 관계에 있다. 따라서 본죄가 성립하는 경우에는 폭행죄나 협박죄는 본죄에 흡수되어 별도로 성립하지 아니 한다.”

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

## 41. `art136_sec2_7.injury_ideal_concurrence`

- proposition: 직무를 집행하는 공무원을 때리고 차서 상해를 가한 경우 공무집행방해죄와 상해죄는 상상적 경합이라는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판단은 때리고 차서 상해를 가한 사안에 한정되어 있으므로 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_52` / `Ⅱ.7`: “대법원도 직 무를 집행하는 공무원을 때리고 차서 상해를 가한 사안에 대하여 본죄와 상해 죄의 상상적 경합을 인정하였다.”

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

## 42. `art136_sec2_7.military_criminal_act_special_relation`

- proposition: 직무수행 중인 군인 등에 대한 폭행·협박이 군형법 제60조 제1항의 구성요건을 충족하면, 특별관계에 따라 직무수행자폭행죄만 성립하고 공무집행방해죄는 별도로 성립하지 않는다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 군형법 제60조 제1항의 구성요건 충족 여부 및 소개된 대법원 판단의 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_53` / `Ⅱ.7`: “양 죄는 법조경합 의 한 형태인 특별관계에 있다고 보아 직무수행 중인 군인 등에게 폭행 또는 협 박을 한 경우에는 군형법 제60조 제1항에서 정한 직무수행자폭행죄만이 성립하 고 본죄는 별도로 성립하지 아니한다고 보았다.”

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

## 43. `art136_sec2_7.multiple_officers_same_duty`

- proposition: 동일한 공무를 집행하는 여러 공무원에 대한 폭행·협박은 공무원 수에 따라 여러 공무집행방해죄가 성립하고, 동일한 장소와 기회에 이루어져 사회관념상 하나의 행위이면 각 죄는 상상적 경합 관계라는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무 수 기준설 및 공무원 수 기준설과의 관계, 그리고 소개된 대법원 판단의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_50` / `Ⅱ.7`: “동일한 공무를 집행하는 여러 명의 공무원에 대하여 폭행 또는 협박 행위가 이루어진 경우에는 공무를 집행하는 공무원의 수에 따라 여러 개의 공 무집행방해죄가 성립하고, 위와 같은 폭행 또는 협박 행위가 동일한 장소에서 동일한 기회에 이루어진 것으로서 사회관념상 1개의 행위로 평가되는 경우에는 여러 개의 공무집행방해죄는 상상적 경합범의 관계에 있다고 보았다.”

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

## 44. `art136_sec2_7.public_duty_not_business_obstruction`

- proposition: 공무원이 직무상 수행하는 공무를 방해하는 행위는 업무방해죄로 의율할 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무의 직무상 수행 여부와 소개된 대법원 판단의 원문을 검토해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_51` / `Ⅱ.7`: “따 라서 공무원이 직무상 수행하는 공무를 방해하는 행위에 대해서는 업무방해죄 로 의율할 수는 없다고 해석함이 상당하다.”

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

## 45. `art136_sec2_7.special_public_duty_provisions`

- proposition: 다른 법률이 특수한 공무집행 담당 공무원에 대한 폭행·협박을 처벌하는 규정을 둔 경우, 해당 특별법 위반죄에 공무집행방해죄가 흡수되어 별도로 성립하지 않는다는 견해가 제시되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 특별법의 적용 요건과 공무집행방해죄와의 흡수관계는 개별 특별법 규정별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.7_52` / `Ⅱ.7`: “경우에는, 본죄는 공직선거법위반죄나 철도안전법위반죄 또는 소방기본법위반죄에 흡수되어 별도 로 성립하지 아니한다고 보아야 한다.”

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
