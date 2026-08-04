# 수뢰·사전수뢰 RuleIR 카드 검수 4

- unit: `bribe_receipt`
- articles: art129
- cards: 46–55 / 55
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art129_sec1_5.retired_official_no_bribe_receipt`

- proposition: 공무원이 재직 중 직무 관련 뇌물수수를 약속하고 퇴직 후 이를 수수한 경우, 약속과 수수가 시간적으로 근접·연속되어도 뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 퇴직 시점, 약속 및 수수의 내용, 그리고 별론으로 언급된 죄의 성립 여부는 분리하여 검토해야 하며, 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅰ.5_16` / `Ⅰ.5`: “공무원이 직무와 관련하여 뇌물수수를 약속하였다가 퇴직 이후 이를 수수 하는 경우에는 뇌물약속과 뇌물수수가 시간적으로 근접하여 연속되어 있다고 하더라도 뇌물약속죄 및 사후수뢰죄의 성립은 별론으로 하고, 뇌물수수죄는 성 립하지 않는다.”

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

## 47. `art129_sec2_1.prior_bribery_elements`

- proposition: 사전수뢰죄는 장래 공무원 또는 중재인이 될 사람이 담당할 직무에 관하여 청탁을 받고 뇌물을 수수·요구·약속한 뒤 공무원 또는 중재인이 된 때 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원 또는 중재인이 된 때의 법적 성격과 취임 전·후 행위의 죄수관계는 제공된 commentary 문구만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.1_25` / `Ⅱ.1`: “공무원 또는 중재인이 될 자가 그 담 당할 직무에 관하여 청탁을 받고 뇌물을 수수, 요구 또는 약속한 후 공무원 또 는 중재인이 된 때 사전수뢰죄가 성립한다.”

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

## 48. `art129_sec2_2.abstract_business_relocation_request`

- proposition: 기업 이전 절차의 마무리 및 이전 과정에서의 행정적·재정적 지원 정도의 청탁은 사전수뢰죄의 구체적이고 특정된 청탁으로 보기 어려워 사전수뢰죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 제시된 청탁 내용에 관한 좁은 결론으로 유지하며, 원전 판례 확인 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.2_27` / `Ⅱ.2`: “‘기업 의 이전 절차의 마무리 및 이전 과정에서의 행정적·재정적 지원’ 정도는 사전수 뢰죄의 구체적이고 특정된 청탁으로 보기 어려우므로, 사전수뢰죄가 성립하지 않는다.”

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

## 49. `art129_sec2_2.application_exam_insufficient`

- proposition: 임명직 공무원이 되기 위해 채용원을 제출하거나 공무원 시험에 응시 중인 사람은, 채용 가능성이 현저하다고 볼 특별한 사정이 없는 한 사전수뢰죄의 주체가 되기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 채용 가능성이 현저한 특별사정의 존재는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.2_26` / `Ⅱ.2`: “공무원으로 되기 위하여 채용원을 제출하거나 공무원 시험에 응시 중에 있는 자는 그 채용가능성이 현저하다고 볼 만한 특별한 사정 이 없는 한 사전수뢰죄의 주체가 되기 어렵다.”

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

## 50. `art129_sec2_2.post_office_request_no_retroaction`

- proposition: 공무원이 되기 전에 청탁을 받은 사실이 증명되지 않으면, 공무원이 된 후 청탁을 받았더라도 이를 취임 전으로 소급하여 사전수뢰죄가 성립한다고 볼 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 취임 전 청탁 사실의 증명 여부와 취임 후 청탁 사실을 시간적으로 구별한다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.2_28` / `Ⅱ.2`: “공무원이 되기 전에 청탁을 받은 사실이 증명되지 않는다면 공무원이 된 후 에 청탁을 받았다고 하더라도 공무원이 되기 전으로 소급하여 사전수뢰죄가 성 립한다고 볼 수 없다.”

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

## 51. `art129_sec2_2.prior_bribery_request_specificity`

- proposition: 사전수뢰죄의 청탁은 장래 직무행위를 의뢰하는 것을 말하며, 그 직무행위가 부정할 필요도 청탁이 명시적일 필요도 없지만, 직무행위는 특정될 필요는 없어도 어느 정도 구체성을 가져야 하고 작위·부작위를 불문한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 청탁의 묵시성 및 요구되는 구체성은 개별 의사표시와 직무 관련 사실에 따라 평가하여야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.2_27` / `Ⅱ.2`: “청탁이라 함은 공무원에 대하여 일정한 직 무행위를 할 것을 의뢰하는 것을 말하는 것으로서 그 직무행위가 부정한 것인 가는 묻지 않으며, 그 청탁이 반드시 명시적이어야 하는 것도 아니다. 또한 이 경우에 직무행위는 특정될 필요는 없으나 어느 정도 구체성은 있어야 하며 작위, 부작위를 불문한다.”

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

## 52. `art129_sec2_2.prospective_official_probability`

- proposition: 사전수뢰죄의 주체는 단순한 공직 취임 가능성만으로는 부족하고, 공무원 또는 중재인이 될 것이 예정되어 있거나 적어도 어느 정도의 공직취임 개연성을 갖춘 사람이어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공직취임 개연성의 충족 여부는 구체적 사정을 평가하여야 한다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.2_26` / `Ⅱ.2`: “공직 취 임의 가능성만으로는 부족하고 최소한의 개연성을 갖춘 자만이 주체가 된다.”
  - `comm_001692_제129조_Ⅱ.2_26` / `Ⅱ.2`: “공무원 또는 중재인이 될 것이 예정되어 있는 자뿐만 아니라 공직취 임이 확실하지는 않지만 어느 정도 개연성이 있어야 한다.”

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

## 53. `art129_sec2_3.prior_bribery_intent`

- proposition: 사전수뢰죄의 고의는 행위자가 자신이 장래 공무원 또는 중재인이 될 사람이라는 점과 담당 직무에 관하여 청탁을 받고 뇌물을 수수·요구·약속한다는 점의 인식 또는 의사이며, 공직취임 개연성의 존재와 이에 대한 미필적 인식으로 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사전수뢰죄의 고의 및 공직취임 개연성에 관한 인식 요건을 별도 검토 단위로 유지한다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.3_29` / `Ⅱ.3`: “사전수뢰죄의 고의는 행위자 자신이 공무원 또는 중재인이 될 자라는 사실에 대한 인식 및 담당할 직무에 관하여 청탁을 받고 뇌물을 수수·요구·약속한다는 사실에 대한 인식 또는 의사이다. 공무원이나 중재인이 될 수 있는 객관적인 개 연성의 존재 및 그러한 개연성에 대한 미필적 인식만으로도 충분하다.”

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

## 54. `art129_sec2_4.false_prospective_official_fraud_only`

- proposition: 공무원 또는 중재인이 될 것처럼 상대방을 기망하여 사전수뢰죄에 해당하는 행위를 했더라도 실제로 공무원 또는 중재인이 되는 요건을 갖추지 못하면 사기죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실제로 공무원 또는 중재인이 되는 요건을 갖추지 못한 경우 사전수뢰죄 성립을 배제하는 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.4_30` / `Ⅱ.4`: “무원 또는 중재인이 될 것처럼 상대방을 기망하여 본죄를 범하였으면 ‘공무원이 나 중재인이 된다’는 요건을 갖추지 못한 이상 사기죄만 성립한다.”

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

## 55. `art129_sec2_4.sequential_demand_promise_receipt_absorption`

- proposition: 같은 사람이 뇌물의 요구·약속·수수를 순차적으로 한 경우 뇌물수수죄만 성립하고, 뇌물요구죄와 뇌물약속죄는 뇌물수수죄에 흡수된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일인에 의한 요구·약속·수수의 순차성 및 흡수 여부를 평가 입력으로 다룬다.
- bounded sources:

  - `comm_001692_제129조_Ⅱ.4_30` / `Ⅱ.4`: “같은 사람에 대하여 요 구·약속·수수를 순차적으로 하는 경우에는 뇌물수수죄만 성립하고, 뇌물요구죄 또는 뇌물약속죄는 뇌물수수죄에 흡수되므로”

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
