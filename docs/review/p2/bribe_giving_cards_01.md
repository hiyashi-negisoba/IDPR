# 뇌물공여 RuleIR 카드 검수 1

- unit: `bribe_giving`
- articles: art133
- cards: 1–15 / 26
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art133.bribery_delivery_offense`

- proposition: 증뢰물전달죄는 증뢰행위에 제공할 목적으로 제3자에게 금품을 교부하거나 그 사정을 알면서 교부받음으로써 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 교부자와 사정을 알면서 교부받는 자의 각 성립 경로 및 증뢰행위 제공 목적을 분리하여 검토한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.1_0` / `Ⅰ.1`: “같 은 조 제2항의 증뢰물전달죄는 증뢰자가 그와 같은 행위에 공할 목적으로 제3 자에게 금품을 교부하거나 그 정을 알면서 교부를 받음으로써 (제3자뇌물교부죄)( 성립하는 범죄”

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

## 2. `art133.bribery_offering_offense`

- proposition: 뇌물공여죄는 제129조 내지 제132조에 기재된 뇌물을 약속·공여하거나 공여의 의사를 표시함으로써 성립하는 범죄이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 약속, 공여, 공여의 의사표시라는 열거된 행위 유형을 별도의 성립 경로로 검토한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.1_0` / `Ⅰ.1`: “형법 제133조 제1항의 뇌물공여죄는 형법 제129조 내지 제132조에 기재 (증뢰죄) 한 뇌물을 약속, 공여 또는 공여의 의사를 표시함으로써 성립하는 범죄이다.”

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

## 3. `art133_sec1_2.acquisition`

- proposition: 뇌물의 취득은 뇌물에 대한 사실상의 처분권을 획득하는 것을 의미하며, 물건의 법률상 소유권 취득은 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법률상 소유권과 사실상 처분권을 분리한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “여기서 취득이란 뇌물수수와 마찬가지의 의미이다. 즉 뇌물에 대한 사실상의 처 분권을 획득하는 것을 의미하고, 뇌물인 물건의 법률상 소유권까지 취득하여야 하는 것은 아니다.”

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

## 4. `art133_sec1_2.aider_as_third_party`

- proposition: 수뢰자에 대한 뇌물 전달 취지로 증뢰자로부터 뇌물을 받은 제3자가 증뢰자 또는 수뢰자의 공동정범 정도에 이르지 않는 방조범이면, 그 제3자는 증뢰물전달죄의 제3자에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 방조와 공동정범의 경계는 개별 관여 정도에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_4` / `Ⅰ.2`: “증뢰자나 수뢰자의 공동정범의 정도에 이 르지 않는 방조범은 위 제3자에 해당한다고 보아야 한다.”

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

## 5. `art133_sec1_2.delivery_completed_on_receipt`

- proposition: 증뢰물전달죄는 제3자가 전달될 금품임을 알면서 교부받은 때 성립하며, 실제 전달 여부, 전달 의사 여부 또는 증뢰자를 기망한 사실은 성립에 영향을 미치지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 제3자의 전달금품 인식과 교부 시점을 확인해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_4` / `Ⅰ.2`: “증뢰물전달죄는 증뢰자나 수뢰자가 아닌 제3자가 증뢰자로부터 수뢰자 (전달자) 에게 전달될 금품인 점을 알면서 그 금품을 교부받으면 그때에 바로 죄가 성립 하고, 그 제3자가 그 금품을 실제로 수뢰자에게 전달하였는지 여부나 제3자가 위 교부받은 금품의 실제 전달 의사가 있었는지 혹은 그에 관하여 증뢰자를 기 망한 사실이 있었는지 여부 등은 죄의 성립에 영향이 없다.”

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

## 6. `art133_sec1_2.expression_arrival`

- proposition: 공여의 의사표시는 상대방에게 도달하여 알 수 있는 상태에 있으면 기수가 되며, 상대방이 현실적으로 인식하지 못하거나 거절하거나 표시 내용대로 수수할 수 없는 상태여도 성립에 영향이 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 도달 및 상대방이 알 수 있는 상태를 완성 시점으로 다룬다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_3` / `Ⅰ.2`: “공여의 의사표시는 상대방에 도달하여 상대방이 알 수 있는 상태에 있으면 기 수가 되므로, 상대방이 그 의사표시를 현실적으로 인식하지 못한 경우나 이를 거 절한 경우 혹은 의사표시 내용대로 뇌물을 수수할 수 있는 상태에 있지 못한 경 우에도 죄의 성립에 영향이 없다.”

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

## 7. `art133_sec1_2.expression_not_arrived`

- proposition: 공여의 의사표시가 상대방에게 도달하지 않은 경우에는 미수이나 미수범 처벌규정이 없어 죄가 되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 도달하지 않은 의사표시에 대한 미수 처벌규정 부재를 명시한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_3` / `Ⅰ.2`: “그러나 의사표시가 상대방에게 도달조차 하지 않은 경우에는 미수가 될 것이지만 미수범 처벌규정이 없어 죄가 되지 않는다.”

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

## 8. `art133_sec1_2.expression_of_offering`

- proposition: 공여의 의사표시는 상대방에게 뇌물을 제공하겠다는 의사의 표시이고, 구두·서면, 명시적·묵시적 방법 모두 가능하며 뇌물의 종류·수량·액수를 구체적으로 표시할 필요는 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 표시 방법 및 뇌물 특정 정도에 관한 정의 카드다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “공여의 의사표시란 상대방에게 뇌물을 제공하겠다는 의사의 표시이다.”
  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “의사 다) 표시의 방법으로는 구두, 서면 어떤 것이든 상관없고 명시적·묵시적인 방법 어느 것이나 무방하고, 뇌물의 종류, 수량, 액수를 구체적으로 표시할 필요도 없다.”

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

## 9. `art133_sec1_2.family_member_recipient`

- proposition: 공여 또는 공여의 의사표시의 상대방은 공무원 또는 중재인이지만, 그 처 또는 자녀 등 생활이익을 같이하는 자에게 한 경우에도 죄의 성립에 지장이 없다고 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 생활이익 공동 여부 및 공무원과의 관계를 사실관계별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_3` / `Ⅰ.2`: “공여와 공여의 의사표시의 상대방은 공무원 또는 중재인이지만 처 또는 자 라) 녀 등 그와 생활이익을 같이 하는 자에게 하더라도 죄의 성립에 지장이 없는 것 은 수뢰죄에 있어서와 마찬가지이다.”

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

## 10. `art133_sec1_2.independent_third_party`

- proposition: 증뢰물전달죄의 제3자는 증뢰자·수뢰자 등 행위자 또는 그와 공동정범 관계에 있는 자 이외의 자를 뜻하므로, 증뢰자와 독립한 제3자 지위에 있다고 보기 어려운 자에게 전달 목적으로 뇌물을 교부한 경우에는 제3자뇌물교부죄나 제3자뇌물취득죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 독립한 제3자성 및 공동정범 관계는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_4` / `Ⅰ.2`: “제3자는 증뢰자나 수뢰자 등 행위자 혹은 그와 공동정범의 관계에 있는 자 이외 의 자를 의미한다. 따라서 증뢰자가 그와 독립한 제3자의 지위에 있다고 보기 어려운 자에게 수뢰자에 대한 전달의 목적으로 뇌물을 교부한 행위는 형법 제 133조에 따른 증뢰물교부죄나 증뢰물취득죄는 성립하지 않는다.”

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

## 11. `art133_sec1_2.intent_for_bribery_offering`

- proposition: 제133조 제1항 증뢰죄의 고의는 공무원이나 중재인에게 뇌물을 약속·공여하거나 공여의 의사표시를 한다는 점에 대한 인식과 의사이고, 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행위 대상과 행위 유형에 관한 인식·의사를 검토한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_5` / `Ⅰ.2`: “형법 제133조 제1항 증뢰죄의 고의는 공무원이나 중재인에게 뇌물을 약속, 공여 또는 그 공여의 의사표시를 한다는 점에 대한 인식과 의사를 말하고, 미필적 고 의로도 충분하다.”

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

## 12. `art133_sec1_2.intent_for_delivery_recipient`

- proposition: 증뢰물취득죄는 금품을 교부받는다는 고의 외에 그 금품이 증뢰에 공할 금품이라는 인식도 있어야 하며, 수뢰자에게 전달될 금품임을 알면서 증뢰자로부터 받은 때 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 금품 수령 인식과 증뢰 목적 인식을 별도로 확인한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_5` / `Ⅰ.2`: “따라서 수뢰자에게 전달될 금품이라는 정을 알면서 증뢰물취득자가 증뢰자로부터 금품을 받은 때에 증뢰 물취득죄가 성립하는 것이므로, 금품을 교부받는다는 점에 대한 고의 이외에 그 것이 증뢰에 공할 금품이라는 점에 대한 인식도 있어야 한다.”

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

## 13. `art133_sec1_2.nonofficial_recipient_at_official_request`

- proposition: 공여자가 공무원의 요구에 따라 비공무원에게 뇌물을 공여하고, 공무원과 비공무원이 뇌물수수죄 공동정범 관계이며 공여자가 이를 인식한 경우 공여자에게 뇌물공여죄의 고의가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원과 비공무원의 공동정범 관계 및 공여자의 인식을 확인해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_5` / `Ⅰ.2`: “공여자가 공무원의 요구에 따라 비공무원에게 뇌물을 공여한 경우 공무원과 비 공무원 사이의 관계가 형법 제129조 제1항 뇌물수수죄의 공동정범에 해당하고 공여자가 이러한 사실을 인식하였다면 공여자에게 형법 제133조 제1항, 제129조 제1항에서 정한 뇌물공여죄의 고의가 인정된다.”

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

## 14. `art133_sec1_2.object_distinction`

- proposition: 제133조 제1항 증뢰죄의 객체는 뇌물이고, 제2항 증뢰물전달죄의 객체는 금품이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제1항과 제2항의 객체 구별을 유지한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “형법 제133조는 제1항 증뢰죄의 객체는 뇌물이고, 같은 조 제2항 증뢰물전달죄 의 객체는 금품이다.”

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

## 15. `art133_sec1_2.offering`

- proposition: 뇌물공여의 공여는 뇌물을 취득하게 하는 것으로, 수수할 수 있는 상태에 두면 충분하고 현실적인 취득은 요구되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현실적 취득 여부와 수수 가능한 상태를 구별한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “뇌물공여에서 말하는 공여는 수수에 대응하는 행위개념으로 부정한 이익인 나) 뇌물을 취득하게 하는 것이다. 수수할 수 있는 상태에 두면 충분하고 현실적으 로 취득할 것을 요구하지 않는다.”

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
