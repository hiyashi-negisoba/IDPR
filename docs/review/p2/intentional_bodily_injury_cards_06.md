# 상해·특수상해·상해치사 RuleIR 카드 검수 6

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 76–90 / 104
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

## 76. `art259_sec1_1.causation.evasion_or_surgical_delay_holding`

- proposition: 반복된 상해를 피하여 도로를 건너 도망하다 차량에 치여 사망한 경우 및 폭행으로 인한 장파열 피해자에 대한 의사의 수술 지연이 사망의 공동원인이 된 경우, 판례는 인과관계를 인정하였다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 두 보고된 사례에 한정된 판례 소개다. 적용 전 각 판례 원문과 사실관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_2` / `Ⅰ.1`: “판례는 거듭되는 상해행위를 피하려고 도로를 건너 도망가다가 차량에 치 어 사망한 경우, 피고인의 폭행으로 장파열에 의한 복막염의 상해를 입은 피 해자에 대한 의사의 수술 지연이 사망의 공동원인이 된 경우에 인과관계를 인 정하였다.”

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

## 77. `art259_sec1_1.causation.indirect_causes`

- proposition: 상해행위가 사망의 직접 원인이 아니더라도 그로부터 발생한 다른 간접 원인이 결합하여 사망 결과가 발생한 경우, 판례는 인과관계를 인정한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간접 원인의 발생 및 결합이 사망 결과와 갖는 관계는 사실관계별 평가가 필요하다. 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_1` / `Ⅰ.1`: “판례는 상해행위가 피해자를 사망하게 한 직접적 원인은 아니었다 하더라 도 이로부터 발생된 다른 간접적 원인이 결합되어 사망의 결과를 발생하게 한 경우에도 인과관계를 인정한다.”

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

## 78. `art259_sec1_1.causation.intervening_act`

- proposition: 상해 후 피해자나 제3자의 행위가 개입하여도 그 개입이 통상 예견 가능하거나 상해행위가 사망의 직접적이고 유력한 원인인 경우, 인과관계가 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 통상 예견 가능성 및 직접적·유력한 원인성은 평가적 판단을 필요로 한다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_2` / `Ⅰ.1`: “상해행위 이후 피해자나 제3자의 행위가 개 입된 경우에도 그와 같은 사실이 통상 예견할 수 있는 것이거나, 상해 행위가 사망의 결과에 대한 직접적이고 유력한 원인이 된 이상 인과관계를 인정할 수 있다.”

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

## 79. `art259_sec1_1.causation.medical_condition_treatment`

- proposition: 피해자의 지병, 입원치료 중 합병증, 또는 피해자나 부모의 불충분한 치료가 사망에 영향을 준 경우에도 판례는 상해행위와 사망 사이의 인과관계를 인정한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 각 사정이 사망에 미친 영향과 상해행위와의 관계를 개별적으로 평가해야 한다. 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_1` / `Ⅰ.1`: “피해자의 지병이 사망 결과에 영향을 준 경우, 병원에서 입원치료를 받다가 합병증으로 사망에 이른 경우, 피해자나 피해자의 부모가 충분한 치료를 하지 아니한 결과로 사망한 경우에도 인과관계가 인정 된다.”

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

## 80. `art259_sec1_1.causation.victim_negligence_no_proximate_cause`

- proposition: 상해 종료 후 피해자 자신의 부주의가 사망 원인이 되어 상해행위가 사망의 직접적이고 유력한 원인이라고 할 수 없는 경우, 상당인과관계는 인정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 부주의라는 개입 사정만으로 인과관계가 부정되는 것은 아니며, 상해행위의 직접적·유력한 원인성에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_2` / `Ⅰ.1`: “피해자가 상해 행위가 끝난 이후에 자신의 부주의가 원인이 되어 사 망하였거나”
  - `comm_001692_제259조_Ⅰ.1_2` / `Ⅰ.1`: “상해 행위가 사망의 결과 고로 사망한 경우 등) 에 대한 직접적이고 유력한 원인이 되었다고 할 수 없으므로 상당인과관계를 인정할 수 없을 것이다.”

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

## 81. `art259_sec1_2.foreseeability_forceful_blow`

- proposition: 주먹으로 안면이나 흉부 등 인체의 중요한 부위를 두개골 결손 등을 가져올 정도로 강하게 타격하면 사망에 이를 수 있음은 누구나 예견할 수 있다는 대법원 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 대법원 입장이므로 원판례 확인 전에는 commentary-reported precedent로 취급한다. 타격 부위와 강도에 대한 사실판단이 필요하다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.2_3` / `Ⅰ.2`: “대법원은 주먹으로 안면이나 흉부와 같이 인체의 중요한 부위에 두개골 결손 등을 가져올 정도로 강하게 타격하면 이로 인하여 정신의 흥분과 혈압의 항진 을 초래하여 사망에 이를 수 있다는 것은 누구나 예견할 수 있다고 한다.”

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

## 82. `art259_sec2_1.murder_intent_exception`

- proposition: 상해 공동정범 중 1인이 살인의 고의로 피해자를 살해한 경우, 나머지 사람에게 상해치사죄 책임이 인정되더라도 살인죄 책임을 물을 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공동 상해와 특정 공동정범의 살인의 고의 여부 및 나머지 공동정범의 책임 범위를 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제259조_Ⅱ.1_4` / `Ⅱ.1`: “상해의 공동정범 가운데 1인이 살인의 고의로 사람을 살해한 경우 나머지 사람 들이 상해치사죄의 죄책을 면할 수 없다고 하더라도 살인죄의 책임을 물을 수 는 없다.”

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

## 83. `art259_sec2_3.multiple_victims_concurrence`

- proposition: 두 사람에게 각각 칼을 휘둘러 한 사람을 사망에 이르게 하고 다른 사람에게 상처를 입힌 경우 상해치사죄와 상해죄의 경합범이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 서로 다른 피해자에 대한 칼 휘두름, 사망 결과 및 상처 결과가 함께 있는 경우에 한정된 경합범 서술이다.
- bounded sources:

  - `comm_001692_제259조_Ⅱ.3_6` / `Ⅱ.3`: “두 사람에게 각각 칼을 휘둘러 한 사람을 사망에 이르게 하고, 또 다른 한 사람 에게는 상처를 입힌 때에는 상해치사죄와 상해죄의 경합범이 된다.”

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

## 84. `art259_sec2_3.robbery_resulting_death_exclusion`

- proposition: 강도행위 중 상해의 고의로 사람을 상해하여 사망하게 한 경우 강도치사죄만 성립하고 별도로 상해치사죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강도행위 중 상해 고의와 사망 결과가 있는 경우 상해치사죄의 별도 성립을 배제하는 예외 서술이다.
- bounded sources:

  - `comm_001692_제259조_Ⅱ.3_6` / `Ⅱ.3`: “강도행위 시에 상해의 고의로써 사람을 상해하여 사망에 이르게 한 경우에는 강도치사죄 가 성립할 뿐이고 별도로 상해치사죄를 구성하지는 않는다.”

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

## 85. `art263.exception.other_result_crimes`

- proposition: 강간치상죄, 강도치상죄, 체포감금치상죄, 현주건조물방화치상죄 및 낙태치상죄에는 제263조 특례를 적용할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 치상죄에 대한 제263조 특례의 비적용 범위를 정리한 예외 카드다. 인용문상 '등'의 범위는 확장하지 않는다.
- bounded sources:

  - `comm_001692_제263조_Ⅳ.4_10` / `Ⅳ.4`: “강간치상죄나 강도치상죄까지 확대하여 적용되 지는 않는다.”
  - `comm_001692_제263조_Ⅳ.4_10` / `Ⅳ.4`: “기본 범죄형이 다른 체포감금치상, 현주건조물방화치상, 낙태치상 등에 대하여 도 마찬가지로 특례를 적용할 수 없다.”

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

## 86. `art263.identified_cause_exclusion`

- proposition: 원인행위가 판명되거나 특정인의 폭행이 상해 원인이 아님이 적극 증명된 경우, 그 특정인에게는 제263조가 적용되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 원인행위 판명 및 특정 행위자의 비원인 적극 증명은 제263조 적용을 배제하는 별도 예외로 유지한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.3_5` / `Ⅲ.3`: “원인된 행위가 판명된 때에는 각자가 자 기의 행위로부터 발생한 결과에 대하여 책임을 지게 될 뿐 형법 제263조가 적 용될 여지는 없다. 또 상해가 수인의 행위자 중 특정인의 폭행에 의한 것이 아 니라는 점이 적극적으로 증명된 경우에도 그 특정인에 대하여는 형법 제263조 의 적용이 없다.”

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

## 87. `art263.individual_causation_rebuttal`

- proposition: 피고인은 자신의 행위와 상해 결과 사이에 개별 인과관계가 없음을 입증하여 상해 결과에 대한 책임에서 벗어날 수 있다는 헌법재판소 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 헌법재판소 판단은 commentary-reported precedent로만 제시되어 있다. 입증 구조와 원문상 정확한 판단 범위의 확인이 필요하다.
- bounded sources:

  - `comm_001692_제263조_Ⅰ_0` / `Ⅰ`: “피고인도 자신의 행위와 상해의 결과 사이에 개별 인과관계가 존재하지 않음을 입증하여 상해의 결과에 대한 책임에서 벗어날 수 있는 점”

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

## 88. `art263.individual_liability_principle`

- proposition: 동시범에서는 각자가 단독정범이므로 원칙적으로 자기 행위로 발생한 결과에 대해서만 책임지고, 결과발생의 원인행위가 판명되지 않으면 각자는 미수범으로 처벌된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제263조 특례 전의 일반 원칙으로 제시된 설명이다. 원인행위 판명 여부는 증거평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제263조_Ⅰ_0` / `Ⅰ`: “동시범은 각자가 단독정범에 불과하므로 개인책임의 원리에 따라 각자 는 자기의 행위에 의하여 발생한 결과에 대하여만 책임을 지게 된다. 만약 이 경우 결과발생의 원인된 행위가 누구의 것인지 판명되지 아니한 때에는 책임원 칙상 각자는 미수범으로 처벌받는 것이 원칙이다.”

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

## 89. `art263.simultaneous_offenders_definition`

- proposition: 의사연락 없이 2인 이상이 동일한 객체에 대하여 개별적으로 동시에 죄를 범한 경우는 동시범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동시범의 설명상 정의를 분리한 카드다. 동시성의 구체적 시간적·장소적 기준은 이 인용문만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제263조_Ⅰ_0` / `Ⅰ`: “2인 이상이 의사연락 없이 동일한 객체에 대하여 개별적으로 동시에 죄를 범한 경우를 동시범이라고 한다.”

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

## 90. `art263.unidentified_causal_act`

- proposition: 제263조 특례 적용을 위해 상해의 원인이 된 행위가 판명되지 않아야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제263조 적용의 원인행위 미판명 요건을 제한적으로 반영한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.3_5` / `Ⅲ.3`: “원인된 행위가 판명되지 않아야 한다.”

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
