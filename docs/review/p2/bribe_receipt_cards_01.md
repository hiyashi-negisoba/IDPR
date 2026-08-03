# 수뢰·사전수뢰 RuleIR 카드 검수 1

- unit: `bribe_receipt`
- articles: art129
- cards: 1–15 / 55
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art129.bribery_giving_despite_coercion`

- proposition: 뇌물 공여에는 완전한 자유의사가 반드시 필요한 것은 아니며, 의사결정에 하자가 있어도 임의의 의사로 재물을 교부하였다고 볼 수 있으면 증뢰죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 임의의 의사 및 의사결정상 하자의 정도는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_21` / `Ⅰ.6`: “뇌물죄의 성립에는 뇌물의 교부 내지 공여의 여부에 대하여 반드시 완 전한 자유의사의 존재를 필요로 하는 것은 아니고, 의사결정상에 어느 정도의 하자가 있다 할지라도 임의의 의사로 재물을 교부하였다고 볼 수 있는 한 뇌물 공여죄가 성립한다”

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

## 2. `art129.coercion_independent_bribery_decision`

- proposition: 공무원의 해악 고지와 금품 제공 사이에 상당인과관계가 없고 교부자가 별도 이해관계에 따라 독자적으로 금품을 제공한 경우, 교부자에게 증뢰죄가 성립하고 공무원에게는 공갈미수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 상당인과관계와 독자적 결정의 인정에는 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_21` / `Ⅰ.6`: “해악의 고지와 공여자의 금품제공 사이에 상당인과관계가 인정되지 않고 오히려 교부자가 별도의 이해 관계에서 독자적 결정에 따라 금품을 제공한 것으로 인정된다면 교부자에게는 증뢰죄가 성립하고, 이를 수수한 공무원의 경우 공갈미수죄가 성립한다.”

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

## 3. `art129.contract_payment_bribery_or_embezzlement`

- proposition: 공무원이 수의계약 상대방으로부터 돈을 수수한 경우 뇌물인지 계약금액을 부풀린 사전 약정에 따른 횡령인지 여부는 당사자 의사와 계약의 내용·성격을 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인용된 범위에서는 당사자 의사와 계약 내용·성격까지만 확인되므로 추가 판단요소는 원자료 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_22` / `Ⅰ.6`: “그 돈의 성격을 공 무원의 직무와 관련하여 수수된 뇌물로 볼 것인지, 아니면 적정한 금액보다 과 다하게 부풀린 금액으로 계약을 체결하기로 공사업자 등과 사전 약정하여 이를 횡령한 것으로 볼 것인지 여부는, 돈을 공여하고 수수한 당사자들의 (국고손실) 의사, 계약의 내용과 성격”

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

## 4. `art129.extortion_provider_not_bribe_giver`

- proposition: 직무집행 의사 없이 또는 직무처리 대가관계 없이 공무원이 공갈한 경우, 교부자가 해악 고지로 외포되어 금품을 제공했다면 교부자는 공갈 피해자일 뿐 뇌물공여죄가 성립하지 않는다는 다수 학설 및 대법원 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대법원 입장은 commentary 보고에 근거하므로 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_17` / `Ⅰ.6`: “이러한 경우에 재물의 교부자가 공무원의 해악의 고지로 인하여 외포된 결과 금품을 제공한 것이라면, 교부자가 뇌물을 공여할 의사가 있었다거 나 협박의 정도가 피해자의 반항을 억압할 수 있는 정도의 것이 아니어서 피해 자의 의사결정의 자유가 완전히 박탈된 것이 아니더라도 공갈죄의 피해자가 될 뿐 뇌물공여죄는 성립하지 않는다는 것이 다수의 학설 및 대법원의 입장이다.”

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

## 5. `art129.extortion_without_duty_or_consideration`

- proposition: 공무원이 직무집행 의사 없이 또는 직무처리와 대가적 관계 없이 타인을 공갈하여 재물을 교부하게 한 경우 공갈죄만 성립하고 뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무집행 의사, 대가관계 및 공갈행위의 사실인정이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_17` / `Ⅰ.6`: “공무원이 직무집행의 의사 없이 또는 직무처리와”
  - `comm_001692_제129조_Ⅰ.6_17` / `Ⅰ.6`: “대가적 관계없이 타인을 가) 공갈하여 재물을 교부하게 한 경우에는 공갈죄만이 성립할 뿐 뇌물수수죄는 성 립하지 않고”

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

## 6. `art129.illicit_benefit_as_bribe`

- proposition: 뇌물죄의 객체인 이익은 반드시 합법적일 필요가 없으므로 장물도 뇌물이 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 이익의 적법성은 뇌물 객체성의 배제 사유가 아니라는 정의적 관계다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_21` / `Ⅰ.6`: “뇌물죄의 객체인 이익은 반드시 합법적인 것일 필요가 없으므로 장물도 뇌물이 될 수 있다.”

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

## 7. `art129.internal_distribution_of_embezzled_proceeds`

- proposition: 공동정범들이 범행으로 취득한 돈을 공모에 따라 내부 분배한 것에 그치는 공범자 간 수수행위에는 별도 뇌물죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공동정범 관계와 내부 분배에 그치는지의 판단이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_22` / `Ⅰ.6`: “공범자끼리 수수한 행위가 공동정범들 사이의 범 행에 의하여 취득한 돈을 공모에 따라 내부적으로 분배한 것에 지나지 않는다 면 별도로 그 돈의 수수행위에 관하여 뇌물죄가 성립하는 것은 아니다.”

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

## 8. `art129.mixed_bribe_nonofficial_gratuity`

- proposition: 수수·요구·약속된 금품에 직무행위 대가성과 직무 외 행위 사례성이 불가분적으로 결합된 경우 그 전부가 직무행위 대가성을 가진다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 불가분적 결합 여부는 별도 사실평가를 전제로 하며, 결합이 인정된 후의 법적 귀결을 정리한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_24` / `Ⅰ.6`: “공무원이 수수·요구 또는 약속한 금품에 그 직무행위에 대한 대가로서의 성질 과 직무 외의 행위에 대한 사례로서의 성질이 불가분적으로 결합되어 있는 경 우에는 그 수수·요구 또는 약속한 금품 전부가 불가분적으로 직무행위에 대한 대가로서의 성질을 가진다.”

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

## 9. `art129.political_contribution_specific_official_act`

- proposition: 정치자금 명목으로 법정 절차를 거쳐 수수된 금품도, 정치활동 일반 지원이 아니라 특정 구체적 직무행위에 관하여 유리한 처분을 기대하거나 사례로 제공되어 직무행위 대가의 실체를 가지면 뇌물성이 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특정 직무행위와 대가적 실체의 인정에는 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_23` / `Ⅰ.6`: “정치인의 정치활동 전반에 대 한 지원의 성격을 갖는 것이 아니라 공무원으로서의 정치인의 특정한 구체적 직무행위와 관련하여 제공자에게 유리한 행위를 기대하거나 혹은 그에 대한 사 례로서 이루어짐으로써 정치인인 공무원의 직무행위에 대한 대가로서의 실체를 가진다면 뇌물성이 인정된다.”

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

## 10. `art129.political_funds_definition`

- proposition: 정치자금법상 수수가 금지되는 정치자금은 정치활동을 위하여 정치활동을 하는 사람에게 제공되는 일체의 금전 등을 말하며, 정치활동을 위하여 제공된 것인지에 따라 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 정치활동을 위한 제공인지 여부는 개별 사정에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_23` / `Ⅰ.6`: “정치자금법에서 수수를 금지하는 정치자금은 정치활동을 위하여 정치활동을 하는 자에게 제공되는 금전 등 일체를 의미한다. 금품이 정치자금에 해당하는지 는 그 금품이 정치활동을 위하여 제공되었는지에 달려 있다.”

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

## 11. `art129.political_funds_with_bribery_substance`

- proposition: 정치자금·선거자금·성금 명목의 금품이라도 정치인인 공무원의 직무행위에 대한 대가라는 실체가 있으면 뇌물성을 잃지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 명목과 달리 직무행위 대가의 실체가 있는지는 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_23` / `Ⅰ.6`: “정치자금, 선거자금, 성금 등의 명목으로 이루어진 금품의 수수라 하더라도, 그것이 정치인인 공무원의 직무행위에 대한 대가로서의 실체를 가지는 한 뇌물 로서의 성격을 잃지 않는다.”

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

## 12. `art129.special_fund_internal_distribution_no_bribery`

- proposition: 대통령과 국정원장이 공모하여 특별사업비를 횡령한 뒤 그 취득금을 내부 분배한 것에 불과하고 뇌물 고의도 인정되기 어려운 경우 대통령의 뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 사건의 공모·내부분배 및 고의 판단에 한정된 보고된 판단이다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_22` / `Ⅰ.6`: “대통령과 국정원장이 공모하여 특별사업비를 횡령한 다음 횡령 범행에 의하여 취득한 돈을 공모에 따라 내부적으로 분배한 것에 불과하여 대통령이 국정원장으로부터 뇌물을 수수하였다고 볼 수 없고 뇌물에 관한 고의가 있었다 고 보기 어려우므로 뇌물수수죄는 성립하지 않는다.”

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

## 13. `art129.tax_investigation_forbearance_bribery`

- proposition: 세무공무원이 세무조사 중 가공계상 사실을 묵인하고 세부조사를 하지 않는 조건으로 회사 대표로부터 금원을 받은 경우, 직무집행 의사와 직무처리에 대한 대가관계가 인정되어 공무원은 뇌물수수죄, 대표는 뇌물공여죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 사실관계에 한정된 보고된 판단으로 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_19` / `Ⅰ.6`: “피고인에게 세무조사라는 직무집행의 의사가 있었고, 과다계상된 손금항 목에 대한 조사를 하지 않고 이를 묵인하는 조건으로, 다시 말하면 그 직무처리 에 대한 대가관계로서 금품을 제공받았으므로, 피고인이 직무에 관하여 뇌물을 수수하고, 대표이사는 위와 같은 경위로 피고인에게 위 금원을 교부하여 공무원 의 직무에 관하여 뇌물을 공여한 사실을 인정하기에 충분하다.”

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

## 14. `art129.voluntary_special_fund_gift`

- proposition: 국정원장이 자발적이고 적극적으로 금품을 교부하고, 대통령이 종전에 받은 것과 성격이 다른 돈임을 미필적으로 인식하여 수수한 경우가 언급되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인용문이 결론 이전에서 끝나므로 해당 사안의 정확한 결론은 원판례 또는 완전한 인용문으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.6_22` / `Ⅰ.6`: “국정원장이 자발적이 고 적극적으로 뇌물을 교부하였고 대통령도 이를 별다른 이의 없이 수수하여 그 돈이 종전에 받았던 것과는 성격이 다르다고 미필적으로 인식하였고”

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

## 15. `art129_sec1.basic_offense`

- proposition: 수뢰죄는 공무원 또는 중재인이 직무에 관하여 뇌물을 수수·요구 또는 약속한 때 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공무원 또는 중재인, 직무 관련성, 뇌물의 수수·요구·약속을 열거한 기본 구성요건 카드다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ_0` / `Ⅰ`: “수뢰죄는 공무원 또는 중재인이 그 직무에 관하여 뇌물을 수수, 요구 또는 약속 한 때에 성립한다.”

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
