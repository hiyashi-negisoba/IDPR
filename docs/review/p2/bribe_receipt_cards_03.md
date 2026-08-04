# 수뢰·사전수뢰 RuleIR 카드 검수 3

- unit: `bribe_receipt`
- articles: art129
- cards: 31–45 / 55
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art129_sec1_2.determine_appropriation_intent`

- proposition: 영득할 의사로 뇌물을 수령한 것인지 여부는 뇌물 교부 경위, 반환 기회가 있었는데도 반환하지 않았는지 여부 및 반환 경위 등을 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 제시된 고려 요소는 영득의사 판단을 위한 평가 요소이며 기계적으로 충족 여부를 산정할 수 없다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “영득할 의사로 뇌물을 수령한 것인지 여부를 판단함에 있어서는 뇌물을 교부받은 경위, 언제든지 그 뇌물을 반환할 기회가 있었음에도 반환하지 아니하였는지 여부, 그 뇌물을 반환하게 된 경위 등을 고려하여야 한다.”

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

## 32. `art129_sec1_2.excessive_amount_later_return`

- proposition: 영득의사로 뇌물을 수령한 이상, 액수가 예상보다 많아 나중에 반환하였더라도 뇌물죄 성립에는 영향이 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사후 반환 일반론보다 좁은, 예상 초과 액수를 이유로 한 반환의 경우에 관한 카드다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_8` / `Ⅰ.2`: “이처럼 영득의 의사로 뇌물을 수령한 이상 그 액수가 피고인이 예상한 것 보다 너무 많은 액수여서 후에 이를 반환하였다고 하더라도 뇌물죄의 성립에는 영향이 없다.”

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

## 33. `art129_sec1_2.intent.status_and_quid_pro_quo`

- proposition: 수뢰죄에는 수뢰자가 공무원 또는 중재인이라는 신분을 인식하고, 직무관련성 및 대가관계가 있는 뇌물의 수수·요구·약속이라는 사실을 인식하는 고의가 필요하며 미필적 고의로 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 신분, 직무관련성 및 대가관계에 관한 인식은 개별 사실관계에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_6` / `Ⅰ.2`: “수뢰죄는 수죄자가 자신이 공무원 또는 중재인이라는 신분에 대한 인식이 필요하다.”
  - `comm_001692_제129조_Ⅰ.2_6` / `Ⅰ.2`: “직무에 관하여 뇌물을 수수, 요구 또는 약속한다는 사실에 대한 고의, 즉 직무관 련성과 대가관계에 대한 인식이 있어야 하고, 미필적 고의로도 충분하다.”

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

## 34. `art129_sec1_2.later_return_after_appropriation`

- proposition: 피고인이 영득의 의사로 뇌물을 수령한 이상, 사후 반환은 뇌물죄 성립에 영향을 미치지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 수령 당시 영득의사가 있었는지가 선행하여 검토되어야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “그러나 일단 피고인이 영득의 의사로 뇌물을 수령한 이상 후에 이를 반환하였 다고 하더라도 뇌물죄의 성립에는 영향이 없다.”

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

## 35. `art129_sec1_2.no_appropriation_immediate_return`

- proposition: 뇌물인 줄 모르고 받았다가 알게 된 즉시 반환하거나, 반환할 의사로 어쩔 수 없이 일시 보관하였다가 반환하는 등 영득의 의사가 없다고 인정되면 뇌물을 수수하였다고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 영득의사 부재와 즉시 반환 또는 반환 목적의 일시 보관 여부는 구체적 경위에 대한 평가를 요한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_8` / `Ⅰ.2`: “뇌물인 지 모르고 이를 수수하였다가 뇌물임을 알고 즉시 반환하거나, 증뢰자가 일방적 으로 뇌물을 두고 가므로 후일 기회를 보아 반환할 의사로 어쩔 수 없이 일시 보관하다가 반환하는 등 그 영득의 의사가 없었다고 인정되는 경우라면 뇌물을 수수하였다고 할 수 없다.”
  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “뇌물을 수수한다는 것은 영득의 의사로 금품을 수수하는 것을 말하므로, 뇌물인 지 모르고 이를 수수하였다가 뇌물임을 알고 즉시 반환하거나, 증뢰자가 일방적 으로 뇌물을 두고 가므로 후일 기회를 보아 반환할 의사로 어쩔 수 없이 일시 보관하다가 반환하는 등 그 영득의 의사가 없었다고 인정되는 경우라면 뇌물을 수수하였다고 할 수 없다.”

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

## 36. `art129_sec1_2.requested_bribe_appropriation`

- proposition: 공무원이 먼저 뇌물을 요구하여 증뢰자가 제공한 돈을 받은 경우, 받은 돈 전부에 대한 영득의사가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원의 선행 요구와 그 요구에 따른 제공 및 수령의 관계를 구체적으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.2_9` / `Ⅰ.2`: “피고인이 먼저 뇌물을 요구하여 증뢰자가 제공하는 돈을 받았다면 피고인에게 는 받은 돈 전부에 대한 영득의 의사가 인정된다.”

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

## 37. `art129_sec1_4.business_opportunity_completion`

- proposition: 투기적 사업 참여 기회를 뇌물로 제공받은 경우 뇌물수수죄의 기수시기는 투기적 사업 참여행위가 종료된 때이며, 이후 경제사정 변동으로 이득을 얻지 못해도 죄 성립에 영향이 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 투기적 사업 참여 기회의 제공 여부 및 참여행위 종료 시점은 구체적 사실관계에서 검토가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “뇌물로 투기적 사업에 참여할 기회를 제공받은 경우에도 뇌물수수 죄의 기수 시기는 투기적 사업에 참여하는 행위가 종료된 때로 보아야 하고, 그 행위가 종료된 후 경제사정의 변동 등으로 인하여 당초의 예상과는 달리 그 사업 참여로 인한 아무런 이득을 얻지 못한 경우라도 뇌물수수죄의 성립에는 아무런 영향이 없다.”

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

## 38. `art129_sec1_4.demand_completion_upon_awareness`

- proposition: 뇌물요구죄는 상대방이 뇌물 요구 의사표시를 인지한 때 기수에 이르며, 상대방의 거절은 그 성립을 막지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상대방의 요구 의사표시 인지와 그 이후 거절 여부를 구별하는 완성시기 관계다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_13` / `Ⅰ.4`: “뇌물요구죄도 즉시범이므로 뇌물의 의사표시를 상대방이 인지한 때 기수가 된다. 상대방이 요구의 의사표시를 인지한 이상 상대방이 요구를 거절하더라 도 뇌물요구죄는 성립한다.”

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

## 39. `art129_sec1_4.interest_free_loan_completion`

- proposition: 공무원이 공여자로부터 무이자로 돈을 차용한 경우 차용 당시 금융이익 상당 뇌물수수죄가 기수에 이르고, 변제하지 않아 금융이익을 계속 얻더라도 계속 수수하는 것으로 보지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 무이자 차용의 금융이익성 및 차용 시점은 구체적 거래 조건에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “공무원이 공여자로부터”
  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “돈을 차용한 경우 차용 당시에 금융이익 상당 의 뇌물을 수수하여 뇌물수수죄가 기수에 이른 것으로 보아야 하므로, 공소시효 는 무이자로 돈을 차용한 때부터 기산한다.”
  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “공무원이 공여자로부터 돈을 차용 한 후 변제를 하지 아니하여 차용기간 중 금융이익 상당의 재산상 이익을 계속 하여 얻고 있다고 하더라도 이를 계속하여 뇌물을 수수하고 있는 것으로 볼 수 없으므로, 돈을 차용한 시점에 이미 뇌물수수죄가 기수에 이른 것으로 보아야”

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

## 40. `art129_sec1_4.post_receipt_check_dishonor`

- proposition: 뇌물로 공여된 당좌수표가 수수 후 부도되어도 죄의 성립에는 영향이 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 수수 후 당좌수표 부도라는 사후 사정은 이미 성립한 죄에 영향을 주지 않는 예외적 시간관계다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “뇌물로 공여된 당좌수표가 수수 후 부도가 되었다 하더라도 죄의 성립에 영 향이 없다.”

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

## 41. `art129_sec1_4.promise_completion_upon_acceptance`

- proposition: 상대방의 뇌물공여 의사표시가 선행한 경우, 공무원이 그 청약을 명시적 또는 묵시적으로 수락하는 의사를 표시하면 뇌물약속죄가 기수에 이른다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 묵시적 수락 의사표시의 존재는 사실관계에 따른 해석이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_13` / `Ⅰ.4`: “뇌물약속죄도 즉시범이므로 상대방의 뇌물공여 의사표시가 선행할 때에는 공무원이 그 청약을 명시적·묵시적으로 수락하는 의사를 표시한 때 뇌물약속죄는 기수에 이른다.”

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

## 42. `art129_sec1_4.unpurchased_investment_opportunity`

- proposition: 미수 처벌규정이 없으므로, 공여자가 뇌물로 매수를 제시한 투기적 사업 주식을 수뢰자가 매수하지 못해 사업 참여행위가 종료되지 않은 경우 뇌물수수죄로 처벌할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주식 매수 실패와 사업 참여행위 미종료라는 한정된 사실관계의 부정적 결론이며, 단순한 긍정사실 부재로 확장해서는 안 된다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.4_12` / `Ⅰ.4`: “반면에 미수를 처벌하는 규정은 없으므로 공여자가 뇌물로 매수를 제시한 투기 적 사업의 주식을 수뢰자가 매수하지 못한 이상 수뢰자가 투기적 사업에 참여 하는 행위가 종료되지 않아 기수에 이르렀다고 할 수 없어 뇌물수수죄로 처벌 할 수 없다.”

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

## 43. `art129_sec1_5.comprehensive_single_offense`

- proposition: 단일하고 계속적 범의로 이루어지고 동일 법익을 침해한 반복 수뢰행위는 포괄일죄로 처벌하며, 그러한 범의의 단일성과 계속성을 인정할 수 없으면 각 범행은 별죄로서 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 단일·계속된 범의와 동일 법익 침해의 구체적 사실상 판단이 필요하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.5_14` / `Ⅰ.5`: “단일하고 계속적 범의에 의하여 이루어지고 동일법익을 침해한 때에는 포괄일 죄로 처벌함이 상당하고, 그러한 범의의 단일성과 계속성을 인정할 수 없을 때 에는 각 범행마다 별개의 죄가 성립하는 것으로서 경합범으로 처단하여야 한다.”

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

## 44. `art129_sec1_5.comprehensive_time_interval`

- proposition: 단일하고 계속된 범의 아래 동종 범행을 일정 기간 반복하고 피해법익도 동일하다면, 수수일자 사이에 상당한 기간이 있어도 포괄일죄가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수수일자 사이의 기간은 단독으로 결정적이지 않으며, 단일·계속된 범의 및 동일 법익은 별도로 판단해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.5_14` / `Ⅰ.5`: “수뢰죄에 있어서 단일하고도 계속된 범의 아래 동종의 범행을 일정기간 반복하 여 행하고 그 피해법익도 동일한 것이라면 돈을 받은 일자가 상당한 기간에 걸 쳐 있고, 돈을 받은 일자 사이에 상당한 기간이 끼어 있다 하더라도 각 범행을 통틀어 포괄일죄로 볼 것이다.”

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

## 45. `art129_sec1_5.different_appraisers_no_comprehensive_offense`

- proposition: 서로 다른 감정평가법인이 각자의 이해관계에 따라 다른 일시·장소에서 제공한 뇌물을 그때그때 수수한 사안에서는 단일하고 계속된 범의 아래 5회 수수하였다고 보기 어려워 포괄일죄가 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 서로 다른 제공자·이해관계, 수수 일시·장소 및 각 수수의 개별성을 해당 사안의 증거에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.5_15` / `Ⅰ.5`: “관리 팀장은 각기 다른 일시에 다른 장소에서 그때그때 각 감정평가법인이 제공하는 뇌물을 수수한 사실이 인정될 뿐이므로, 관리팀장이 단일하고 계속된 범의 아래 에서 5회에 걸쳐 뇌물을 수수하였다고 볼 수는 없으므로 포괄일죄가 아니다.”

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
