# 상해·특수상해·상해치사 RuleIR 카드 검수 5

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 61–75 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #21 `art257_sec1_2.prenatal_injury_postnatal_result`: `art257_sec1_2.prenatal_injury_postnatal_result_negative` (status=`valid`)
- #22 `art257.pregnancy_injury`: `art257.pregnancy_not_injury` (status=`valid`)
- #23 `art257.drug_method`: `art257.drug_intangible_method` (status=`valid`)
- #24 `art259_sec1_1.second_act_liability`: `art259_sec1_1.second_act.single_offense_holding` (status=`valid`)

## 61. `art257_sec2.registry_entry_without_parentage`

- proposition: 가족관계등록부상 피고인이 피해자의 친생자로 기재되어 있어도 실제 친자관계가 없으면 법률상 친자관계가 생기지 않아 피해자는 존속상해죄의 직계존속이 될 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 등록 기재와 실제 친자관계의 불일치 여부 및 그 법률상 효과에 관한 사실판단과 법률 검토가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅱ_31` / `Ⅱ`: “가족관계등록부상 피고인이 피해자의 친 생자로 기재되어 있다고 하더라도 실제로는 친자관계가 없는 경우 법률상 친자 관계가 생길 수는 없으므로 피해자는 이 죄의 직계존속에 해당할 수 없다.”

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

## 62. `art257_sec3.attempted_injury_or_ancestral_injury`

- proposition: 상해죄와 존속상해죄는 상해의 고의가 있는 경우 수단이 폭행이든 그 밖의 방법이든 미수에 그치면 미수범으로 처벌한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해의 고의와 미수에 그친 사실이 확인되면 적용되는 상해죄·존속상해죄 미수 처벌 관계를 정리한 카드다.
- bounded sources:

  - `comm_001692_제257조_Ⅲ_32` / `Ⅲ`: “상해죄와 존속상해죄는 상해의 고의가 있는 이상 그 수단이 폭행이든 그 밖의 방법이든 미수에 그친 경우에는 미수범으로 처벌한다.”

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

## 63. `art2582_2_sec1.dangerous_object_carriage`

- proposition: 위험한 물건을 휴대하여 상해, 존속상해, 중상해 또는 존속중상해의 죄를 범하면 특수상해죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 인용문이 열거한 기초 범죄와 위험한 물건 휴대의 결합을 독립된 대안적 구성요건 경로로 보존한다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅰ_0` / `Ⅰ`: “이 죄는 단체 또는 다중의 위력을 보이거나 위험한 물건을 휴대하여 상해, 존속 상해, 중상해, 존속중상해의 죄를 범함으로써 성립한다.”

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

## 64. `art2582_2_sec1.group_or_multiple_force`

- proposition: 단체 또는 다중의 위력을 보이며 상해, 존속상해, 중상해 또는 존속중상해의 죄를 범하면 특수상해죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 인용문이 열거한 기초 범죄와 단체 또는 다중의 위력 표시의 결합을 별도 구성요건 경로로 보존한다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅰ_0` / `Ⅰ`: “이 죄는 단체 또는 다중의 위력을 보이거나 위험한 물건을 휴대하여 상해, 존속 상해, 중상해, 존속중상해의 죄를 범함으로써 성립한다.”

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

## 65. `art2582_2_sec2.favorable_law_change`

- proposition: 개정 전 폭력행위 등 처벌에 관한 법률 제3조 제1항을 삭제하고 같은 구성요건을 형법 제258조의2 제1항에 신설하면서 법정형을 종전보다 낮춘 경우, 대법원은 이를 형법 제1조 제2항의 범죄 후 법률변경으로 형이 구법보다 경해진 경우에 해당한다고 해석한 것으로 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 법률변경의 반성적 조치 여부와 구법·신법의 구성요건 동일성 및 법정형 경감 여부는 사실 및 법률 비교를 요구한다. 소개된 대법원 태도는 원판례로 확인이 필요하다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅱ_1` / `Ⅱ`: “대법원은 개정 전 폭력행위 등 처벌에 관한 법률 제3조 제1항과 신설된 형법 제 258조의2 제1항의 관계에 대하여, 개정 전 폭력행위 등 처벌에 관한 법률 제3조 제1항을 삭제하고 같은 구성요건을 형법 제258조의2 제1항에 신설하면서 법정형 을 종전보다 낮게 규정한 것은 종전의 형벌규정이 과중하다는 데에서 나온 반 성적 조치로서 형법 제1조 제2항의 ‘범죄 후 법률의 변경에 의하여 형이 구법보 다 경한 때’에 해당한다고 해석하여 구법과 신법의 관계로 보고 있다.”

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

## 66. `art2582_2_sec2.no_abolition_dangerous_object_injury`

- proposition: 개정 전 폭력행위 등 처벌에 관한 법률 시행 당시 위험한 물건을 이용하여 상해를 가한 후 같은 법 제3조 제1항이 삭제되었더라도, 소개된 판례 태도에 따르면 이를 형의 폐지로 보아 면소를 선고하지 않고 신설 형법 제258조의2 제1항을 적용하여 그에 따른 형을 선고하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 형의 폐지 및 면소 결론을 부정하는 좁은 보고된 판례 태도이다. 행위시법, 삭제된 조항, 신설 조항 및 적용 대상이 원판례와 일치하는지 확인이 필요하다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅱ_1` / `Ⅱ`: “이러한 판례의 태도에 따르면, 개정 전 폭력행위 등 처벌에 관한 법률 시행 당시에 위 험한 물건을 이용하여 상해를 가한 후에 같은 법 제3조 제1항이 삭제되었다 하 더라도, 이를 형의 폐지로 보아 피고인에 대하여 면소를 선고할 것이 아니라 신 설된 형법 제258조의2 제1항을 적용하여 그에 따른 형을 선고하여야 한다.”

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

## 67. `art2582_2_sec3.attempt_punishable`

- proposition: 특수상해죄와 특수존속상해죄의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 특수상해죄와 특수존속상해죄에 한정된 미수범 처벌 관계를 정리한 카드다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅲ_2` / `Ⅲ`: “특수상해죄, 특수존속상해죄의 미수범은 처벌한다”

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

## 68. `art2582_2_sec3.habitual_offender_aggravation`

- proposition: 특수상해죄, 특수중상해죄 및 특수존속상해죄의 상습범은 가중처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상습범 해당 범죄유형에 대한 가중처벌 관계를 정리한 카드다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅲ_2` / `Ⅲ`: “특수상해죄나 특수중상해죄, 특수중존속상해죄의 상습범은 가중처벌되고”

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

## 69. `art2582_2_sec3.qualification_suspension`

- proposition: 특수상해죄 및 그 상습범과 미수범에 대해서는 10년 이하의 자격정지를 병과할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 자격정지 병과 여부와 기간의 적용에는 개별 양형 판단이 필요하다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅲ_2` / `Ⅲ`: “특수상해죄 및 그 상습범과 미수범에 대해서는 10년 이하의 자격정지를 병 항”

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

## 70. `art2582_2_sec3.recidivist_aggravation`

- proposition: 일정한 요건을 충족한 특수상해죄 또는 특수존속상해죄의 누범은 폭력행위 등 처벌에 관한 법률 제3조 제4항 제3호에 따라 가중처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인용된 폭력행위 등 처벌에 관한 법률상의 구체적 누범 요건을 현 자료만으로 열거할 수 없다.
- bounded sources:

  - `comm_001692_제258조의2_Ⅲ_2` / `Ⅲ`: “일정한 요건을 충족한 특수상해죄나 특수존속상해죄의 누범은 폭력행위 등 처 벌에 관한 법률 제3조 제4항 제3호에 따라 가중처벌된다.”

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

## 71. `art259_sec1.basic_offense_and_death`

- proposition: 상해행위로 사람을 사망에 이르게 한 경우 상해치사죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 상해와 사망 결과의 기본 구성을 나타내는 요소 카드이며, 인과관계와 사망 결과에 대한 과실은 별도 카드에서 검토한다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ_0` / `Ⅰ`: “이 죄는 사람의 신체를 상해하여 사망에 이르게 함으로써 성립한다.”

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

## 72. `art259_sec1.causation_and_foreseeability`

- proposition: 상해치사죄가 성립하려면 상해행위와 사망 결과 사이의 인과관계 및 사망 결과에 대한 예견가능성, 즉 과실이 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 인과관계와 사망 결과의 예견가능성은 구체적 행위, 개입 사정 및 결과 발생 경위에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ_0` / `Ⅰ`: “이 죄가 성립하기 위해서는 결과적 가중범의 일반원리에 따라 상해행위와 사망의 결과 사이의 인과관계와 사망의 결과에 대한 예견가능성, 즉 과실이 있어야 한다.”

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

## 73. `art259_sec1.intentional_death_murder_exception`

- proposition: 사망 결과에 고의가 있으면 상해치사죄는 성립하지 않고 살인죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 사망 결과에 대한 고의가 인정되는지 여부를 검토하여 상해치사죄 적용을 배제하고 살인죄 성립 여부를 판단한다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ_0` / `Ⅰ`: “사망의 결과에 대하여 고의가 있는 때에는 이 죄가 성 립하지 아니하고 살인죄가 성립할 뿐이다.”

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

## 74. `art259_sec1.no_injury_intent_classification`

- proposition: 폭행의 고의만으로 사망 결과가 발생한 경우에는 폭행치사죄가 되고, 폭행이나 상해의 고의 없이 사망 결과가 발생한 경우에는 과실치사죄가 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 상해의 고의가 없는 경우의 범죄 분류를 나타내며, 폭행 고의 또는 무고의 여부는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ_0` / `Ⅰ`: “폭행의 고의만 있고 사망의 결과로 결과적 가중범이 되는 경우에는 폭행치사죄가 되고, 폭행이나 상해의 고의가 없 이 사망의 결과가 발생한 경우에는 과실치사죄가 된다.”

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

## 75. `art259_sec1.result_aggravated_offense`

- proposition: 상해치사죄는 상해에는 고의가 있으나 사망 결과는 고의 없이 발생한 상해죄의 결과적 가중범이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 상해에 대한 고의와 사망 결과에 대한 고의의 유무는 구체적 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ_0` / `Ⅰ`: “상해에 대 하여는 고의가 있었으나 사망의 결과가 고의 없이 발생한 경우로서 상해죄에 대한 결과적 가중범이다.”

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
