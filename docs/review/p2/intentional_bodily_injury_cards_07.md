# 상해·특수상해·상해치사 RuleIR 카드 검수 7

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 91–104 / 104
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

## 91. `art263.unidentified_injury_cause_exception`

- proposition: 상해 동시범에서 상해의 원인행위가 판명되지 않은 경우에는 각자를 미수범이 아니라 공동정범의 예에 따라 처벌한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: ‘공동정범의 예에 의한다’의 의미와 제263조의 법적 성질은 이 인용문만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제263조_Ⅰ_0` / `Ⅰ`: “형법 제263조는 상해의 동시범에 대한 특례를 인정하여 상해의 원인된 행위가 판명되지 아니한 때에는 각자를 미수범으로서가 아니라 공동정범의 예 에 의해 처벌하도록 함으로써 개인책임의 원칙을 수정하고 있다.”

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

## 92. `art263_sec3_1.co_perpetration_contact`

- proposition: 행위자들 사이에 의사연락이 있어 공동정범이 성립하면 제263조의 적용 문제는 발생하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 의사연락에 따른 공동정범 성립은 제263조 적용 문제를 배제하는 별도 예외로 보존한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.1_3` / `Ⅲ.1`: “범인들 사이에 의사연락이 있어 공동정범이 성립하는 경우에도 위 규정 의 적용문제는 아예 생기지 않는다.”

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

## 93. `art263_sec3_1.independent_acts`

- proposition: 제263조 특례 적용을 위해서는 두 개 이상의 행위가 의사연락 없이 같은 객체에 대하여 이루어지는 독립행위의 경합이 있어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 독립행위 경합의 설명된 구성요소를 별도 카드로 보존한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.1_3` / `Ⅲ.1`: “독립행위가 경합한다는 것은 두 개 이상의 행위가 서로 의사의 연락 없이 같은 객체에 대하여 행하여지는 것을 말한다.”

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

## 94. `art263_sec3_1.no_clear_assault_act`

- proposition: 가해행위를 한 사실 자체가 분명하지 않은 사람에게는 제263조를 적용할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 가해행위 사실이 분명하지 않은 경우를 명시적 적용 배제 카드로 유지한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.1_3` / `Ⅲ.1`: “가 해행위를 한 것 자체가 분명하지 않은 경우에는 형법 제263조가 적용될 여지가 없고”

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

## 95. `art263_sec3_1.reported_case_temporal_separation`

- proposition: 시간적 차이가 있는 독립행위가 경합한 경우에도 제263조를 적용할 수 있다는 대법원 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 시간적 차이가 있는 행위에 관한 소개된 대법원 입장은 원판결과 사용자 주된 판례 인덱스로 확인해야 한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.1_3` / `Ⅲ.1`: “대법원은 “시간적 차이가 있는 독립된 상해행위나 폭행행위가 경합하여 사망의 결과가 일어나고 그 사망의 원인된 행위가 판명되지 않은 경우에는 공동정범의 예에 의하여 처벌 할 것이다”고 하여 다수설과 같이 이시의 독립행위가 경합한 때에도 적용을 긍정 하고 있다.”

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

## 96. `art263_sec3_1.reported_case_temporally_separated_death`

- proposition: 시간적 차이가 있는 독립된 상해 또는 폭행행위가 경합하여 사망 결과가 발생하고 그 원인행위가 판명되지 않은 경우, 가해행위 사실이 분명한 자는 동시범 규정에 따라 공동정범의 예로 처벌한다는 대법원 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사망 결과, 원인행위 불명, 가해행위 사실의 명확성 및 공동정범의 예의 의미를 원판결로 확인해야 한다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.1_3` / `Ⅲ.1`: “시간적 차이가 있는 독립된 상해행위나 폭행행위가 경합하여 사망의 결과가 일어나 고 그 사망의 원인된 행위가 판명되지 않은 경우에는 동시범 규정에 따라 공동정범 의 예에 의하여 처벌할 것이지만”

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

## 97. `art263_sec3_2.injury_result`

- proposition: 제263조 특례 적용을 위해 상해 결과가 발생하여야 하며, 폭행에 그치고 상해에 이르지 않은 경우에는 적용될 여지가 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해 결과의 발생과 폭행에 그친 경우의 비적용을 구분하는 적용 범위 카드다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.2_4` / `Ⅲ.2`: “상해의 결과가 발생하여야 한다. 폭행에 그쳤을 뿐 상해에 이르지 않았을 때에 는 적용될 여지가 없다.”

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

## 98. `art263_sec3_2.mixed_intent_injury`

- proposition: 한 사람은 폭행의 고의로, 다른 사람은 상해의 고의로 폭행하여 상해 결과가 발생한 경우 각각 폭행치상과 상해의 기수로 처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 각 행위자의 고의 내용과 상해 결과 발생 여부에 대한 사실평가가 필요하며, 제263조의 적용 구조는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제263조_Ⅲ.2_4` / `Ⅲ.2`: “1인은 폭행의 고의로, 1인은 상해의 고의로 폭행하여 상해의 결과가 발생하였 다면, 폭행치상과 상해의 기수로 각 처벌받게 된다.”

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

## 99. `art263_sec4_2.negligent_death_reported_precedent`

- proposition: 과실치사가 문제된 사안에서 제263조 특례 적용을 부정한 것으로 보이는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문, 사실관계, 판시 이유 및 적용 범위가 확인되지 않아 commentary-reported precedent로만 유지한다.
- bounded sources:

  - `comm_001692_제263조_Ⅳ.2_8` / `Ⅳ.2`: “판례도 과실치사가 문제된 사안에서 특례의 적용을 부정한 것으로 보인다.”

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

## 100. `art263_sec5.resulting_offense`

- proposition: 제263조에 따라 공동정범의 예로 처벌할 때 경합된 행위가 상해이면 상해기수죄가 되고, 폭행이면 폭행치상죄가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 경합된 행위의 유형과 결과 범죄의 관계만을 기술한다. 제263조 적용요건 및 공동정범의 법적 효과는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제263조_Ⅴ_11` / `Ⅴ`: “경합된 행위가 상해인 경우에는 상해기수죄가 되고, 폭행인 경우에는 폭행치상죄가 된다.”

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

## 101. `art257_sec1_2.prenatal_injury_postnatal_result_negative`

- proposition: 태아 상태의 침해가 출생 후 상해 결과를 발생시킨 경우에도, 침해 당시 행위객체인 사람이 존재하지 않았으므로 상해죄 성립을 부정하는 것이 타당하다는 견해가 소개되어 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 침해 당시 사람인 객체의 존재를 요구하여 성립을 부정하는 통설 소개이며, 긍정 견해와 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_2` / `Ⅰ.2`: “상해죄는 계속범이 아닌 상태범으로서 법익침해 당시 에 행위객체인 ‘사람’이 존재하고 있어야 하는데 침해행위가 이루어질 당시의 행 위객체인 태아를 사람으로 볼 수는 없을 뿐만 아니라”
  - `comm_001692_제257조_Ⅰ.2_2` / `Ⅰ.2`: “부정설이 우리나라의 통설이다.”

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

## 102. `art257.pregnancy_not_injury`

- proposition: 부녀의 임신은 생리적 현상의 결과일 뿐 생리적 기능 장애를 야기하지 않는다는 이유로 상해에 해당하지 않는다는 일반적 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 의사에 반하는 임신의 상해 해당성에 관한 경쟁 견해 중 하나이며, 채택 전 검토가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “녀에 대한 임신의 경우 생리적 기능 훼손설의 입장에서는 비록 외관에 중대한 변경을 가져 왔더라도 생리적 현상의 결과일 뿐 그로 인하여 생리적 기능에 대”
  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “한 장애를 야기한 것은 아니라는 이유로 상해에 해당하지 않는다고 보는 것이 일반적인 견해”

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

## 103. `art257.drug_intangible_method`

- proposition: 약물 투여로 환각상태나 일시적 의식불명 상태에 이르게 하는 행위는 폭행이 아닌 무형적 방법에 의한 상해라는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 약물 투여 행위의 방법론적 분류에 관한 경쟁 견해 중 하나이며, 채택 전 검토가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “이에 관하여는 폭행이 아닌 무형적 방법에 의한 것으로 보는 견해”

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

## 104. `art259_sec1_1.second_act.single_offense_holding`

- proposition: 피고인이 상해 후 피해자를 사망한 것으로 오인하여 자살로 위장하려고 추락시켜 사망하게 한 일련의 행위는, 판례상 포괄하여 단일의 상해치사죄에 해당한다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 대립 견해와 별도로 보존한 보고된 판례 입장이다. 사용자의 1차 판례 인덱스에서 원문 확인 후에만 판례 지향 정책을 선택해야 한다.
- bounded sources:

  - `comm_001692_제259조_Ⅰ.1_2` / `Ⅰ.1`: “판례는 위와 같은 일련의 피고인의 행위는 포괄하여 단일의 상해치사죄에 해당한다고 본다.”

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
