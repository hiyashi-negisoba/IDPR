# 제3자뇌물제공 RuleIR 카드 검수 3

- unit: `third_party_bribery`
- articles: art130
- cards: 31–38 / 38
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art130_sec3.third_party_knowledge_not_required`

- proposition: 제3자가 뇌물임을 인식할 필요는 없고, 제3자에게 공여하게 된 동기도 묻지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제3자 측 인식 및 제3자 공여 동기를 별도 성립요건으로 요구하지 않는다는 카드다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_8` / `Ⅲ`: “제3자가 뇌물임을 인식할 것을 필요로 하지 않고, 이를 제3자에게 공여하게 된 동기도 묻지 않는다.”

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

## 32. `art130_sec3.third_party_organizations`

- proposition: 제3자는 자연인에 한정되지 않으며 법인 또는 법인격 없는 단체도 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제3자 범위에 자연인 외 법인과 법인격 없는 단체를 포함하는 정의 카드다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_8` / `Ⅲ`: “제3자는 자연인에 한하지 않고 법인이든 법인격 없는 단체이든 무관하므로”

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

## 33. `art130_sec3_가.controlled_consulting_account`

- proposition: 정비사업전문관리업체 대표이사가 실질적으로 장악한 컨설팅회사 명의 계좌로, 시공사 선정 관련 청탁을 한 건설회사로부터 돈을 받은 경우 직접 뇌물을 수수한 것으로 볼 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 계좌 명의 회사의 실질적 장악 및 금원의 직접 수수와 같은지에 관한 사회통념상 평가가 필요하다. 보도된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.가_10` / `Ⅲ.가`: “정비사업전문관리업체의 대표이사인 피고인이 자신이 실질적으로 장악하고 있는 컨설팅회사 명의 계좌로 시공사로 선정되도록 도와달라는 부탁을 한 건설회사로부터 돈을 받은 경우 사회통념상 피고인에게 직접 뇌물을 수수한 것으로 볼 수 있다.”

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

## 34. `art130_sec3_가.public_official_controlled_company_account`

- proposition: 공무원이 실질적 경영자인 회사가 청탁 명목 금원을 회사 명의 예금계좌로 송금받은 경우, 공무원이 직접 받은 것과 같이 평가되어 뇌물수수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원의 회사에 대한 실질적 경영관계와 회사 계좌 송금을 공무원의 직접 수수와 같게 평가할 수 있는지 판단이 필요하다. 보도된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.가_10` / `Ⅲ.가`: “공무원이 실질적인 경영자로 있는 회사가 청탁 명목의 금원을 회사 명의의 예금계좌로 송금받은 경우에 사회통념상 위 공무원이 직접 받은 것과 같이 평 가할 수 있어 뇌물수수죄가 성립한다.”

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

## 35. `art130_sec3_가.redevelopment_manager_corporate_bribe`

- proposition: 공무원으로 의제되는 정비사업전문관리업자의 임직원이 직무 관련 뇌물을 해당 법인에 공여하게 한 경우, 법인을 사실상 1인 회사처럼 운영하거나 경제적·실질적 이해관계를 같이하여 법인 공여가 곧 임직원 공여와 같다고 평가되는 경우에 한하여 뇌물수수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 법인에 대한 공여를 임직원에 대한 직접 공여와 같게 평가할 수 있는지 사회통념상·경제적·실질적 이해관계 판단이 필요하다. 보도된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.가_10` / `Ⅲ.가`: “위 임·직원이 법 인인 정비사업전문관리업자를 사실상 1인 회사로서 개인기업과 같이 운영하거 나, 사회통념상 정비사업전문관리업자에 뇌물을 공여한 것이 곧 그 임·직원에게 공여한 것과 같다고 볼 수 있을 정도로 경제적·실질적 이해관계를 같이하는 것 으로 평가되는 경우에 한하여 형법 제129조 제1항의 뇌물수수죄가 성립한다.”

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

## 36. `art130_sec4_2.contract_demand_imaginary_concurrence`

- proposition: 공무원이 직무관련자에게 제3자와 계약 체결을 요구하여 계약을 체결하게 한 행위가 제3자뇌물수수죄와 직권남용권리행사방해죄 구성요건에 모두 해당하면 상상적 경합 관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무관련성, 계약 체결 요구, 양 죄의 구성요건 해당성 및 사회관념상 하나의 행위인지는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅳ.2_14` / `Ⅳ.2`: “공무원이 직무관련자에게 제3자와 계약을 체결하도록 요구하여 계약을 체결 3. 하게 한 행위가 본죄의 구성요건과 직권남용권리행사방해죄의 구성요건에 모두 해당하는 경우에는 사회관념상 하나의 행위가 수 개의 죄에 해당하여 상상적 경합의 관계에 있다.”

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

## 37. `art130_sec4_2.different_third_party_no_intent_severance`

- proposition: 제3자뇌물수수죄에서 금품·이익을 수수하는 제3자가 다르다는 사정만으로 범의가 단절된다고 보기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 수수 제3자의 상이함만으로 범의 단절을 추론하지 않으며, 범의 판단에는 추가 사실관계의 평가가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅳ.2_14` / `Ⅳ.2`: “제3자뇌물수수죄에 있어서는 금품 기타 이익을 수수하는 제3자가 다르다는 4. 사정만으로 범의가 단절된다고 보기 어렵다.”

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

## 38. `art130_sec4_2.third_party_receipt_not_required`

- proposition: 제3자뇌물수수죄에서는 제3자가 실제로 수수하였는지 또는 뇌물성을 알았는지는 문제되지 않으며, 제3자가 수수를 거절하여도 죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제3자의 실제 수수, 뇌물성 인식 또는 수수 거절은 이 카드가 다루는 성립 판단의 장애사유가 아니라는 예외적 관계를 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅳ.2_14` / `Ⅳ.2`: “충분하므로 제3자가 실제로 이를 수수하였는지 여부 혹은 뇌물인 정을 알았는 지 여부는 문제되지 않고, 제3자가 수수를 거절한 경우에도 본죄가 성립하는 것 은 뇌물공여죄의 경우와 마찬가지이다.”

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
