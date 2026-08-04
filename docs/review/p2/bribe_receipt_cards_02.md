# 수뢰·사전수뢰 RuleIR 카드 검수 2

- unit: `bribe_receipt`
- articles: art129
- cards: 16–30 / 55
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art129_sec1_1.acceptance_awareness_appropriation`

- proposition: 수수 외관만으로는 부족하고, 수뢰자가 뇌물성을 인식하지 못하거나 영득의사 없이 수수한 경우에는 수수가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 영득의사 필요 여부에 관한 미해결 견해 대립은 별도 법률검토가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_2` / `Ⅰ.1`: “수수의 외관이 있는 것만으로는 충분하지 않다. 수뢰자가 뇌물인 사실을 인식 나) 하지 못하거나 영득의 의사가 없이 수수한 경우가 이에 해당한다.”

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

## 17. `art129_sec1_1.acceptance_no_legal_title`

- proposition: 뇌물수수는 뇌물에 대한 사실상 처분권을 획득하는 것을 뜻하며, 물건의 법률상 소유권 취득까지 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법률상 소유권의 이전 여부와 별도로 사실상 처분권 획득 여부를 확인한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_1` / `Ⅰ.1`: “뇌물수수는 뇌물을 취득하는 것이고, 여기에서 취득이란 뇌물에 대한 사실상 의 처분권을 획득하는 것을 의미하고, 뇌물인 물건의 법률상 소유권까지 취득하 여야 하는 것은 아니다.”

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

## 18. `art129_sec1_1.acceptance_tangible_intangible`

- proposition: 뇌물의 수수는 뇌물을 받는 것이며, 유형 이익은 점유 이전 또는 취득으로, 무형 이익은 현실로 받은 때 수수가 이루어진다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 이익의 유형·무형 구분과 현실 수령 또는 점유 이전·취득 시점을 확인한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_1` / `Ⅰ.1`: “뇌물의 수수란 뇌물을 받는 것을 말한다. 유형의 이익인 때에는 점유의 이 가) 전이나 취득으로 수수가 이루어지며, 무형의 이익인 때에는 이를 현실로 받은 때에 수수가 된다.”

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

## 19. `art129_sec1_1.arbitrator_statutory_basis`

- proposition: 중재인은 법령에 근거하여 중재 직무를 담당하는 사람을 말하며, 사실상 중재행위를 하는 사람은 포함되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법령상 근거 없는 사실상 중재행위자는 이 정의에서 제외된다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_1` / `Ⅰ.1`: “중재인은 중재법, 노동조합 및 노동관계조정법 등 법령에 근거를 가지고 중재의 직무를 담당하는 자를 말하고, 사실상 중재행위를 하는 자를 포함되지 않는다.”

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

## 20. `art129_sec1_1.car_lease_intangible_benefit`

- proposition: 뇌물로 제공된 자동차가 리스회사에 반환해야 하는 리스차량이라 수뢰자가 실질적 처분권을 갖지 못하면 자동차 자체의 수수는 부정되나, 무상으로 사용·수익하는 무형 이익은 뇌물이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 리스 반환의무, 실질적 처분권 및 무상 사용·수익의 범위를 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_2` / `Ⅰ.1`: “뇌물로 제공된 자동차가 리스차량으로 리스회사에서 반환을 요구할 경우 응 할 수밖에 없는 경우라면 법률상 소유권은 물론 실질적 처분권도 갖지 않으므 로 자동차 자체를 뇌물로 수수한 것으로 볼 수 없고 금전적인 부담이 전혀 없는 상태에서 자동차를 뇌물수수자의 의사대로 사용·수익할 수 있는 무형의 이익을 뇌물로 볼 수 있다.”

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

## 21. `art129_sec1_1.demand`

- proposition: 뇌물의 요구는 뇌물을 수수할 의사로 상대방에게 교부를 청구하는 것이고, 뇌물공여 의사표시나 제공 약속의 청구 및 묵시적·간접적 요구도 포함된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행동에 의한 묵시적·간접적 청구가 요구에 해당하는지는 표현과 맥락을 평가한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_4` / `Ⅰ.1`: “뇌물의 요구는 뇌물을 수수할 의사로 상대방에 대하여 교부를 청구하는 것이다. 뇌물공여의 의사표시나 제공의 약속을 청구하는 것도 요구의 개념에 포함된다고 본다. 언어적 표현 대신 행동 등을 통한 묵시적, 간접적인 방법의 요구도 가능하다.”

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

## 22. `art129_sec1_1.demand_active_intent`

- proposition: 뇌물 교부를 요구하는 의사가 적극적으로 인정되어야 하므로, 단순히 뇌물수수 의사를 넌지시 암시하여 제공을 유도한 정도만으로는 요구죄 성립을 인정하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 객관적으로 드러나는 적극적 요구 의사표시가 있었는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_4` / `Ⅰ.1`: “뇌물의 교부를 요구하는 의사가 본죄의 성립요건인 이상 그와 같은 의사 가 있음이 적극적으로 인정되어야 한다. 따라서 뇌물수수 의사가 있음을 넌지시 암시하고 뇌물제공을 유도하는 정도에 불과할 뿐 객관적으로 드러나는 적극적 뇌물요구의 의사표시가 있었다고 보기 어려운 경우에는 본죄의 성립을 인정하 기 어렵다.”

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

## 23. `art129_sec1_1.indirect_payment`

- proposition: 제3자가 공여자를 대신해 수뢰자에게 지급하고 공여자로부터 상환받는 방식이라도, 공여자와 수뢰자 사이에 금품 제공의 의사합치가 있고 수뢰자가 그 지급방법을 양해하면 직접 수수가 없다는 이유만으로 뇌물수수죄를 면할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 금품 제공 의사합치와 수뢰자의 지급방법 양해 여부를 확인해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_3` / `Ⅰ.1`: “공여자와 수뢰자 사이에 금품 제공에 관한 의사의 합치가 존 재하고 또한 그러한 지급방법에 관하여 수뢰자가 양해하였다고 인정되는 한, 공 여자와 수뢰자 사이에 직접 금품이 수수되지 아니하였다는 사정만으로는 뇌물 수수죄의 죄책을 면할 수 없다.”

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

## 24. `art129_sec1_1.invalid_appointment_official`

- proposition: 법령상 임명권자에게 임용되어 공무에 종사한 사람이 사후에 임용결격자로 밝혀져 최초 임용행위가 무효인 경우에도 뇌물죄의 공무원에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 임명권자에 의한 임용, 공무 종사, 임용결격 및 무효의 사실관계 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_1` / `Ⅰ.1`: “법령에 기한 임명권자에 의하여 임용되어 공무에 종사 하여 온 사람이 나중에 그가 임용결격자이었음이 밝혀져 당초의 임용행위가 무 효라고 하더라도 뇌물죄에서의 공무원에 해당한다.”

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

## 25. `art129_sec1_1.promise`

- proposition: 뇌물의 약속은 양 당사자 사이 뇌물수수의 합의로서 명시적일 필요는 없으나, 장래 공무원의 직무와 관련하여 뇌물을 주고받겠다는 의사표시가 확정적으로 합치하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 묵시적 합의와 확정적 의사표시 합치 여부는 개별 의사소통의 맥락을 검토한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_5` / `Ⅰ.1`: “형법 제129조의 구성요건인 뇌물의 ‘약속’은 양 당사자 사이의 뇌물수수의 합의 를 말하고, 여기에서 ‘합의’란 그 방법에 아무런 제한이 없고 명시적일 필요도 없고 묵시적으로도 가능하다. 다만, 장래 공무원의 직무와 관련하여 뇌물을 주 고 받겠다는 양 당사자의 의사표시가 확정적으로 합치하여야 한다.”

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

## 26. `art129_sec1_1.promise_unknown_amount`

- proposition: 뇌물약속죄에서 목적물인 이익은 약속 당시 현존할 필요가 없고 예기 가능한 것이면 충분하며, 이익 가액이 확정되지 않아도 약속죄 성립에는 영향이 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 약속 당시 이익의 예기 가능성과 장래 수수를 기약하는 합의 여부를 확인해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_5` / `Ⅰ.1`: “뇌물약속죄에 있어서 뇌물을 약속한다 함은 뇌물의 수수를 장래에 기약하는 것 이므로, 뇌물의 목적물인 이익은 약속 당시에 현존할 필요는 없고 약속 당시에 예기할 수 있는 것이라도 무방하다. 뇌물의 목적물이 이익인 경우에는 그 가액 이 확정되어 있지 않아도 뇌물약속죄가 성립하는 데는 영향이 없다.”

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

## 27. `art129_sec1_1.subject_current_official_arbitrator`

- proposition: 수뢰죄의 주체는 현재 공무원 또는 중재인의 지위에 있는 사람이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현재 공무원 또는 중재인 지위 여부를 확인하는 주체 요건이다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_1` / `Ⅰ.1`: “수뢰죄의 주체는 공무원 또는 중재인이다. 현재 공무원 또는 중재인의 지위에 있는 자만이 본죄의 주체가 된다.”

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

## 28. `art129_sec1_1.third_party_direct_receipt_equivalence`

- proposition: 공무원의 사자·대리인이 뇌물을 받거나, 제3자의 수령으로 공무원이 지출을 면하는 등 사회통념상 공무원이 직접 받은 것과 같이 평가할 관계가 있으면 제3자뇌물제공죄가 아니라 단순수뢰죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사자·대리 관계 또는 공무원의 지출 면제와 직접수령 동가성은 사회통념에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.1_3` / `Ⅰ.1`: “그 다른 사람이 공무원의 사자 또는 대리인으로서 뇌물을 받은 경우나 그 밖에 예컨대 평소 공무원이 그 다른 사람의 생활비 등을 부담하고 있었다거나 혹은 그 다른 사람에 대하여 채무를 부담하고 있었다는 등의 사정이 있어서 그 다른 사람이 뇌물을 받음으로써 공무원은 그만큼 지출을 면하게 되는 경우 등 사회통념상 그 다른 사람이 뇌물을 받은 것을 공무원이 직접 받은 것과 같이 평가할 수 있 는 관계가 있는 경우에는 제130조의 제3자뇌물제공죄가 아니라 제129조 제1항의 단순수뢰죄가 성립한다.”

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

## 29. `art129_sec1_2.charitable_appearance_appropriation`

- proposition: 공여자의 기부를 공무원이 주선하거나 전달하는 정도를 넘어 공여자 자금으로 공무원이 기부한 것과 같은 외관을 취한 경우, 자선적 동기라도 영득의사가 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 단순 주선·전달과 공무원 자신의 기부 외관 사이의 경계는 사실관계 평가를 요한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “다만 뇌물은 불법한 보수나 부정한 이익이면 족하므로, 자선적 동기라 하더 라도 공여자가 기부하는 것을 공무원이 주선하거나 전달하는 정도를 넘어 공여 자의 자금으로 공무원이 기부를 하는 것과 같은 외관을 취한 경우라면 영득의 사가 인정될 수 있다.”

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

## 30. `art129_sec1_2.charitable_transfer_no_appropriation`

- proposition: 공무원이 불우이웃돕기 성금이나 연극제에 전달할 의사로 금품을 받고 실제 수수한 돈 그대로 전달한 경우, 공여자에게 미필적 뇌물공여 의사가 있더라도 공무원의 영득의사를 인정하기 어려워 뇌물수수죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 전달 의사와 실제 동일 금액 전달의 사실인정이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “불우이웃돕기 성금이나 연극제에 전달해 줄 의사로 금품을 받았고 그 후 실제 로 불우이웃돕기 단체나 연극제 임원에게 수수한 돈이 그대로 전달되었다면, 공여 자는 미필적으로나마 뇌물공여의 의사로 돈을 교부했다고 하더라도 공무원이 영득 할 의사로 돈을 수수하였다고 보기 어려우므로 뇌물수수죄는 성립하지 않는다.”

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
