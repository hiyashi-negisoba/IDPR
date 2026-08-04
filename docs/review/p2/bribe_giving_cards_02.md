# 뇌물공여 RuleIR 카드 검수 2

- unit: `bribe_giving`
- articles: art133
- cards: 16–26 / 26
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art133_sec1_2.official_duty_relation_quid_pro_quo`

- proposition: 증뢰죄와 증뢰물전달죄의 성립에는 상대방 공무원의 직무와의 관련성 및 대가성이 필요하며, 그 상대방 공무원의 직무를 기준으로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무관련성과 대가성은 개별 제공 경위에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “즉 증뢰죄, 증뇌물전달죄 모두 직무관련성과 대가성이 있어야 하고, 이는 뇌물 또는 금품의 상대방인 공무원의 직무와 관련하여 죄의 성립을 판단 하여야 한다.”

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

## 17. `art133_sec1_2.receiver_bribery_not_required`

- proposition: 뇌물공여죄의 성립에 상대방의 뇌물수수죄 성립은 반드시 필요하지 않으며, 공무원이 물건의 뇌물성을 인식하지 못하여 수뢰죄가 성립하지 않는 경우에도 증뢰죄는 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방의 받아들이는 행위와 상대방 수뢰죄 성립을 구별해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “뇌물공여죄가 성립하기 위하여 뇌물을 공여하는 행위와 상대방 측에서 금전적 으로 가치가 있는 그 물품 등을 받아들이는 행위가 필요할 뿐 반드시 상대방 측 에서 뇌물수수죄가 성립하여야 하는 것은 아니다. 따라서 공무원이 증뢰자가 제 공한 물건의 뇌물성을 미처 인식하지 못한 경우 등의 이유로 수뢰죄는 성립하 지 않는 경우에도 증뢰죄가 성립할 수 있다.”

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

## 18. `art133_sec1_2.refused_sponsorship_money`

- proposition: 공여자가 제안한 후원금 명목의 금품 제공 의사를 공무원이 거절한 뒤 제3자가 그 금품을 받은 경우, 사회통념상 제3자가 사후에 공무원에게 전달해 주겠다는 명목으로 취득한 것으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원의 거절 시점, 제3자 수령 경위 및 전달 명목의 존재를 검토해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_5` / `Ⅰ.2`: “제3자의 주선으 로 공무원을 만난 공여자가 제안한 후원금 명목의 금품 제공 의사를 공무원이 거절한 이상, 그 후 제3자가 공여자로부터 위 금품을 받았다고 하더라도 그 때 에는 사회통념상 제3자가 그 돈을 사후에 공무원에게 전달하여 주겠다는 명목 으로 취득한 것으로 볼 수는 없다.”

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

## 19. `art133_sec1_2.scope_of_official_duty`

- proposition: 직무는 공무원이 지위에 수반하여 공무원으로서 취급하는 일체의 사무로서, 권한에 속한 행위뿐 아니라 밀접한 관계가 있는 경우 및 직무와 관련하여 사실상 처리하는 행위도 포함한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 권한, 밀접한 관계 및 사실상 처리 여부의 평가는 기계적으로 확정할 수 없다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “직무의 의미도 수뢰죄의 경우와 마찬가지로 공무원이 그 지위에 수반하여 공무 로서 취급하는 일체의 사무를 말하는 것으로서, 그 권한에 속하는 직무행위 뿐 만 아니라 이와 밀접한 관계가 있는 경우 및 그 직무와 관련하여 사실상 처리하 고 있는 행위까지 포함한다.”

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

## 20. `art133_sec1_2.self_benefit_intermediary`

- proposition: 제3자가 자기 이득을 위하여 공무원 사건·사무에 관한 청탁이나 증뢰자와 수뢰자 사이의 중개·알선 명목으로 금품을 수수하는 경우에는 다른 범죄가 성립할 수 있어도 증뢰물전달죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 자기 이득 목적과 전달 목적을 구별하고, 다른 범죄의 성립 여부는 별도 검토한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_5` / `Ⅰ.2`: “제3자 가 자기 자신의 이득을 취하기 위하여 공무원이 취급하는 사건이나 사무에 관 하여 청탁한다는 명목으로 금품을 수수하는 경우 또는 증뢰자와 수뢰자 사이를 중개, 알선한다는 명목으로 금품을 수수하는 경우에는 변호사법 제111조 위반죄 혹은 특정범죄 가중처벌 등에 관한 법률 제3조의 알선수재죄가 성립할 수 있어 도 증뢰물전달죄는 성립하지 않는다.”

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

## 21. `art133_sec1_2.specific_duty_authority_allegation`

- proposition: 증뢰죄로 될 사실을 적시할 때 개별 직무행위와의 대가관계까지 적시할 필요는 없으나, 적어도 어떠한 공무원의 직무권한에 관한 것인지는 구체적으로 적시하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공소사실 또는 사실 적시의 구체성 충족 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “증뢰죄로 될 사실의 적시에 있어서는 개개의 직무행위와 대가관계에 있는 사실까지 적시할 필요는 없어도 적어도 공무원의 어떠한 직무권한에 관한 것인 가는 구체적으로 적시할 필요가 있다.”

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

## 22. `art133_sec1_2.substantive_use_disposal_authority`

- proposition: 수수자가 법률상 소유권 취득요건을 갖추지 못했더라도 제공물의 점유를 취득하고 반환을 요구받지 않아 실질적 사용·처분권한을 갖게 된 경우에는 물건 자체를 뇌물로 받은 것으로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 점유, 반환 요구 관계 및 실질적 처분권한을 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “뇌물수수자가 법률상 소유권 취득의 요건을 갖추지는 않았더 라도 뇌물로 제공된 물건에 대한 점유를 취득하고 뇌물공여자 또는 법률상 소 유자로부터 반환을 요구받지 않는 관계에 이른 경우에는 그 물건에 대한 실질 적인 사용·처분권한을 갖게 되어 그 물건 자체를 뇌물로 받은 것으로 보아야 한 다.”

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

## 23. `art133_sec1_2.third_party_advance_payment`

- proposition: 제3자가 증뢰자와 의사 합치 아래 증뢰자를 대신하여 자신의 자금으로 수뢰자에게 먼저 지급하고 증뢰자로부터 상환받는 방식으로 공여한 경우에도, 증뢰자를 주체로 하는 증뢰죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 증뢰자와 제3자 사이 의사 합치 및 상환 구조를 검토해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “따라서 제3자가 증뢰자와 의사 합치 하에 증뢰자를 대신하여 먼저 자 신의 자금으로 수뢰자에게 지급한 다음 증뢰자로부터 그 돈을 상환받는 방식으로 공여가 이루어진 경우에도 증뢰자를 주체로 하는 증뢰죄가 성립할 수 있다.”

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

## 24. `art133_sec1_2.unilateral_offer`

- proposition: 상대방의 수수행위 없이 일방적인 공여의 제공 또는 의사표시에 그친 경우에는 뇌물공여죄가 아니라 뇌물공여의사표시죄에 해당한다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 수수행위의 존재 여부에 따라 공여죄와 의사표시죄를 구별한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_2` / `Ⅰ.2`: “상대방의 수수행위 없이 일방적인 공여의 제공이나 의사표시에 그친 경우에는 뇌물공여 죄가 아닌 뇌물공여의사표시죄에 해당하게 된다.”

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

## 25. `art133_sec1_2.unrestricted_offender`

- proposition: 뇌물공여죄의 주체에는 제한이 없고, 공무원도 자신의 직무와 관계되지 않는 범위에서는 다른 공무원에 대한 뇌물공여죄의 주체가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원 공여자의 자신의 직무 관련성 범위를 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.2_1` / `Ⅰ.2`: “뇌물공여죄의 주체는 제한이 없으므로 공무원이라도 다른 공무원에게 뇌물을 공여하는 입장에 있을 때에는 자신의 직무와 관계되지 않는 범위 내에서 본죄 의 주체가 될 수 있다.”

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

## 26. `art133_sec1_3.delivery_offense_absorbed`

- proposition: 제3자가 증뢰자로부터 교부받은 금품을 그대로 수뢰자에게 전달한 경우, 제133조 제2항의 증뢰물전달죄는 제133조 제1항의 증뢰죄에 흡수되어 증뢰죄 1죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 금품이 그대로 전달된 경우에 한정된 흡수관계를 제시한다. 실제 공여, 일부 공여, 별도 범의가 있는 경우의 죄수는 추가 검토가 필요하다.
- bounded sources:

  - `comm_001692_제133조_Ⅰ.3_6` / `Ⅰ.3`: “위와 같이 제3자가 증뢰자로부터 교부받은 금품 을 그대로 수뢰자에게 전달하였다면, 증뢰죄의 경우에도 형법 제133조 제2항의 증뢰물전달죄의 범행이 형법 제133조 제1항 증뢰죄의 범행에 흡 (제3자뇌물교부죄) 수되어 증뢰죄 1죄만이 성립한다고 보아야 한다.”

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
