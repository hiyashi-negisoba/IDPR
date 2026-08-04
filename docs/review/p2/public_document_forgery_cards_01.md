# 공문서등위조·변조 RuleIR 카드 검수 1

- unit: `public_document_forgery`
- articles: art225
- cards: 1–15 / 43
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art225.approved_private_document`

- proposition: 사문서에 공무소나 공무원이 인준·확인한 경우 그 문서 전체는 공문서로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인준·확인의 주체와 그 효력이 문서 전체에 미치는지를 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “사문서에 공무소나 공무원이 인”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “준·확인하는 경우 그 문서 전체를 공문서로 보아야 할 것이다.”

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

## 2. `art225.contractual_delegate_not_official`

- proposition: 공무원·공무소가 아닌 자는 계약 등에 따라 공무 관련 업무 일부를 대행하더라도, 법률 또는 특별법상 공무원 등으로 의제되는 경우를 제외하면 공무원 또는 공무소가 될 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 작성주체의 법률·특별법상 의제 여부와 단순 계약상 대행 여부를 구별해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “문서 작성의 주체가 공무원과 공무소가 아닌 경우에는 형법 또는 특별법에 의”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “하여 공무원 등으로 의제되는 경우 (예컨대 한국은행법 제106조, 외국환거래법 제23”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “를 제외하고 계약 등에 의하여 공무와 관련되는 업무를 일부 대행하는 경우”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “가 있더라도 공무원 또는 공무소가 될 수 없다.”

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

## 3. `art225.essential_form_defect`

- proposition: 법령상 일정 형식이 요구되는 문서가 중요한 형식을 결여한 내용을 표시한 경우 공문서라고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 요구된 형식이 중요한 형식인지와 해당 형식의 결여 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “법령상 일정한 형식에 따라 작성할 것이 요구되는 경우 그 중요한 형식을 결여”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “하는 내용을 표시한 문서는 공문서라고 할 수 없다.”

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

## 4. `art225.false_original_not_alteration_object`

- proposition: 이미 허위로 작성된 공문서는 공문서변조죄의 객체가 되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 원문서가 이미 허위로 작성되었는지는 변조 대상성 판단에서 별도의 사실 분류로 확인한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.2_5` / `Ⅱ.2`: “이미 허위로 작성된 공문서는 공문서변조죄”
  - `comm_001692_제225조_Ⅱ.2_5` / `Ⅱ.2`: “의 객체가 되지 않는다.”

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

## 5. `art225.foreign_official_document`

- proposition: 우리나라의 공무소·공무원이 작성한 문서가 아닌 외국 공문서는 원칙적으로 본죄의 객체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 국내 공무소·공무원 작성 여부에 관한 원칙적 객체 범위를 나타내며, 국제협약·조약 관련 경쟁 견해는 별도 카드에서 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “공문서는 우리나라의 공무소·공무원이 작성한 문서를 말한다. 따라서 외국의 공”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “무소 또는 공무원이 작성한 공문서는 본죄의 객체가 될 수 없다.”

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

## 6. `art225.inferable_author`

- proposition: 문서상 작성명의인이 명시되지 않아도 문서의 형식·내용 등 자체로 작성자를 추지할 수 있으면 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서 자체의 형식과 내용만으로 작성자를 추지할 수 있는지를 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “문서상 작성명의인이 명시되어 있”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “지 않더라도 문서의 형식, 내용 등 그 문서 자체에 의하여 누가 작성하였는지를 추지할 수 있을 정도의 것이면 충분하”

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

## 7. `art225.minor_form_defect`

- proposition: 경미한 형식만 결여한 문서는 공문서로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 형식 결여가 경미한지 여부는 문서에 요구되는 형식의 기능을 고려하여 평가해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “그러나 경미한 형식을 결여”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “한 것에 그친 문서는 공문서라고 해야 한다.”

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

## 8. `art225.nonexistent_nominee_document`

- proposition: 명의자인 공무소 또는 공무원이 실재하지 않아도, 일반인이 실재하는 공무소·공무원이 작성한 것으로 오인할 우려가 있고 문서의 형식·외관상 그렇게 보이면 공문서로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인의 오인 우려 및 문서의 형식·외관을 구체적 사실에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “공무소 또는 공무원이 실”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “재하지 아니하여도 그 공무소나 소속 공무원이 실재하는 것처럼 일반인이 오인”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “할 우려가 있고, 또한 그 공문서의 형식이나 외관에 의해 실재하는 공무원이 작”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “성한 것처럼 보이는 경우 공문서로 보고 있다.”

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

## 9. `art225.official_document_definition`

- proposition: 공문서는 공무소 또는 공무원이 그 명의로 직무상 작성하는 문서이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공문서성의 기본 정의로서 작성명의와 직무상 작성 여부를 분리하여 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “공문서는 공무소 또는 공무원이 그 명의로 직무상 작성하는 문서를 말한다.”

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

## 10. `art225.personal_debt_document_not_public`

- proposition: 개인 채무부담의 의사표시 문서는 다른 사정이 없으면 경험칙이나 논리칙상 공적 문서로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 개인 채무부담 문서인지와 공적 문서성을 달리 볼 수 있는 다른 사정의 존재는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.2_5` / `Ⅱ.2`: “개인 채무부담의 의견표시인 문서는 다른 사정이 없는 한 경험칙이나 논리칙상 공적 문서로 볼 수 없다.”

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

## 11. `art225.private_economic_official_document`

- proposition: 공무소 또는 공무원이 직무상 작성한 문서는 공법상 관계 또는 사법상 관계에 따라 작성되었는지를 불문하고 공문서이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공법상·사법상 관계의 구분은 공문서성 판단을 배제하지 않으나 직무상 작성 여부는 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “는 공무원이 직무상 작성한 문서가 공문서이므로 공법상 관계로 작성된 것”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “이든 사법상 관계로 작성된 것이든 상관없다.”

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

## 12. `art225.private_intent_document`

- proposition: 사인의 의사를 표시한 문서라도 작성명의인이 공무원이면 공문서에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서가 표시하는 의사와 문서의 작성명의인을 구별하여 사실관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “사인의 의사를 표시한 문서라도 문서의 작성”
  - `comm_001692_제225조_Ⅱ.1_2` / `Ⅱ.1`: “명의인이 공무원이면 공문서에 해당한다.”

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

## 13. `art225.scope_of_document_authority`

- proposition: 공무소·공무원의 문서 작성 권한은 법령·내규·관례의 근거와 무관하게 직무집행 범위 안에서 작성되었으면 공문서성을 인정한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무집행 범위 내 작성인지와 권한 근거의 유형을 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “공무소, 공무원의 문서 작성 권한은 법령에 의한 것이든 내규에 의한 것이든, 관”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “례에 의한 것이든 상관없이 그 직무집행의 범위 내에서 작성되었으면 공문서라”
  - `comm_001692_제225조_Ⅱ.1_3` / `Ⅱ.1`: “고 해야 한다.”

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

## 14. `art225_sec2.official_document_drawing_definition`

- proposition: 공문서·공도화는 공무소 또는 공무원이 그 명의로 권한 내에서 소정의 형식에 따라 작성한 문서·도화이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공문서·공도화의 작성 주체, 명의, 권한 및 형식 요건을 함께 충족하는지 확인하는 정의 카드다.
- bounded sources:

  - `comm_001692_제225조_Ⅱ_1` / `Ⅱ`: “공문서·공도화는 공무소, 공무원이 그 명의로”
  - `comm_001692_제225조_Ⅱ_1` / `Ⅱ`: “권한 내에서 소정의 형식에 따라 작성한 문서·도화이다.”

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

## 15. `art225_sec3_1.alteration_definition`

- proposition: 공문서 변조는 유효하게 진정한 공무소 등의 명의 문서가 성립한 뒤 권한 없이 변경을 가하는 것이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 진정 문서의 선행 성립과 이후 무권한 변경을 분리하여 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “변조는 일단 유효하게 진정한 공무”
  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “소 등 명의의 문서가 성립된 것을 전제로 하고 그 이후에 권한 없이 변경을 가”
  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “하는 것을 말한다.”

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
