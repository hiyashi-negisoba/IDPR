# 강간등상해·치상 RuleIR 카드 검수 1

- unit: `sexual_offense_injury_or_death`
- articles: art301
- cards: 1–15 / 34
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #28 `art301_sec4_6.pregnancy_injury`: `art301_sec4_6.unwanted_pregnancy_not_injury_holding` (status=`valid`)
- #29 `art301_sec7.special_rape_attempt_result`: `art301_sec7.special_rape_injury_completed` (status=`valid`)

## 1. `art301.assault_before_forced_indecency_no_result_injury`

- proposition: 폭행으로 상해를 입힌 다음 강제추행을 한 경우에는 강제추행치상죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해가 강제추행 전에 발생한 시간적 순서가 핵심이며, 상해 결과를 강제추행치상 결과로 연결하지 않는 예외로 검토한다.
- bounded sources:

  - `comm_001692_제301조_Ⅸ_23` / `Ⅸ`: “폭행으로 상해를 입힌 다음 강제추행을 한 경우에는 강제추행치상죄가 성립하지 않는다”

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

## 2. `art301.death_absorbs_injury`

- proposition: 강간으로 피해자에게 상해를 입힌 후 그로 인해 사망한 경우 상해는 사망에 흡수되어 강간치사죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해와 사망 사이의 인과관계 및 사망 결과의 발생을 확인한 경우에만 적용하며, 상해 결과를 별도 범죄 결과로 병과하지 않는 취지다.
- bounded sources:

  - `comm_001692_제301조_Ⅸ_23` / `Ⅸ`: “강간으로 피해자에게 상해를 입힌 후에 그로 인해 사망한 경우에는 상해는 사망에 흡수되어 강간치사죄만 성립한다.”

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

## 3. `art301.no_abandonment_offense_after_rape_injury`

- proposition: 강간치상죄를 범한 자가 실신한 피해자를 구호하지 않고 방치했더라도 포괄적으로 강간치상죄만 구성하고 별도 유기죄는 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강간치상죄와 피해자 방치 행위의 포괄적 평가 여부를 검토하는 예외 카드이며, 별도 유기죄 성립을 배제하는 범위에 한정된다.
- bounded sources:

  - `comm_001692_제301조_Ⅸ_23` / `Ⅸ`: “강간치상죄를 범한 자가 실신한 피해자를 구호하지 않고 방치하였더라도 그 행 위는 포괄적으로 강간치상죄만 구성할 뿐 따로 유기죄를 구”
  - `comm_001692_제301조_Ⅸ_23` / `Ⅸ`: “성하지는 않는다.”

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

## 4. `art301.post_rape_new_intent_separate_concurrence`

- proposition: 강간 등 행위가 종료된 뒤 새로 상해 고의가 생겨 상해한 경우에는 강간 등 죄와 상해죄의 실체적 경합범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강간 등 행위의 종료와 새 상해 고의의 발생은 사실관계 평가가 필요하며, 해당 경우 결과적 가중범으로 포괄하지 않는 예외로 검토한다.
- bounded sources:

  - `comm_001692_제301조_Ⅸ_23` / `Ⅸ`: “강간 등 행위가 종료된 후 새롭게 상해의 고의가 생겨 사람을 상해한 경우에는 강간 등 죄와 상해죄의 실체적 경합범이 성립한다.”

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

## 5. `art301_sec2.attempt_injury`

- proposition: 강간 등이 미수에 그친 경우에도 그 수단이 된 폭행으로 피해자가 상해를 입으면 본죄가 성립하며, 미수가 자의중지인지 실행 미완료인지는 가리지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행과 상해 결과의 관계 및 미수 경위의 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제301조_Ⅱ_1` / `Ⅱ`: “간 등이 ‘미수’에 그친 경우에도 그 수단이 된 폭행에 의하여 피해자가 상해를 입었으면 본죄가 성립하는데, 미수에 그친 것이 행위자가 자의로 실행에 착수한 행위를 중지한 경우이든 실행에 착수하여 행위를 종료하지 못한 경우이든 가리 지 않는다.”

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

## 6. `art301_sec2.object_victim`

- proposition: 본죄의 객체인 사람은 강간 등의 피해자를 의미한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 객체가 선행 강간 등 범죄의 피해자로 한정된다는 정의 카드다.
- bounded sources:

  - `comm_001692_제301조_Ⅱ_1` / `Ⅱ`: “본죄의 객체는 ‘사람’으로 규정되어 있지만 이는 강간 등의 피해자를 의미한다.”

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

## 7. `art301_sec2.subject_predicate_offenses`

- proposition: 본죄의 주체는 열거된 강간·유사강간·강제추행·준강간 등 범죄를 범한 자 또는 그 미수에 그친 자이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 선행 범죄 또는 그 미수 여부를 확인하는 주체 요건 카드다.
- bounded sources:

  - `comm_001692_제301조_Ⅱ_1` / `Ⅱ`: “본죄의 주체는 강간죄, 유사강간죄, 강제추행죄, (형법 제297조)(제297조의2)(제298조) 준강간죄·준유사강간·준강제추행죄, 16세 미만 미성년자에 대한 간음· (제299조) 추행죄를 범한 자 또는 그 미수에 그친 자이다.”

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

## 8. `art301_sec3.continuing_criminal_stage`

- proposition: 상해 결과는 강간 등 실행 중, 실행 직후 또는 실행범의 포기 직후로서 사회통념상 범죄행위가 완료되지 않은 단계의 행위로 발생하여야 하며, 강간 등이 기수에 이르기 전 원인행위가 반드시 있어야 하는 것은 아니다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 사회통념상 범죄행위 완료 여부와 실행 직후 해당 여부는 평가적 판단을 요구한다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “강간 등 범행의 실행 중이거나 실행 직후 또는 실행의 범의를 포기한 직후로서 사회통념상 범죄행위가 완료되지 아니하였다고 볼 수 있는 단계에서의 행위로 상해의 결과가 발생하여야 하고, 반드시 강간 등이 기수에 이르기 전에 원인되 는 행위가 있어야 하는 것은 아니다.”

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

## 9. `art301_sec3.injury_occasion_categories`

- proposition: 강간 등의 기회에 발생한 상해에는 강간 등 자체에 기인한 경우, 그 수단인 폭행으로 발생한 경우 및 강간 등에 수반하여 발생한 경우가 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 인용문이 열거한 상해 발생 경로를 한정하여 기록한다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “여기에는 ⅰ) 강간 등 그 자체에 기인하는 경우, ⅱ) 그 수단으로 행해진 폭행으 로 인하여 발생한 경우, ⅲ) 나아가 강간 등에 수반하여 일어난 경우가 포함된 다.”

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

## 10. `art301_sec3.injury_occasion_causation`

- proposition: 본죄 성립을 위해서는 강간 등의 죄 외에, 강간 등의 기회 또는 시간적·장소적으로 밀접하게 관련된 행위로 발생한 상해 결과가 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 강간 등의 기회 및 시간적·장소적 밀접관련성은 구체적 사정에 대한 평가를 요구한다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “본죄가 성립하기 위해서는 강간 등의 죄가 성립하는 외에 상해의 결과가 발생 하여야 하는데, 상해의 결과는 강간 등의 기회에 또는 이와 시간적·장소적으로 밀접하게 관련된 행위에 의하여 생긴 것이어야 한다.”

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

## 11. `art301_sec3.post_rape_injury_connection`

- proposition: 강간 후에도 피해자의 심리적 저항불능 상태가 해소되지 않은 상태에서 강간범의 상해행위가 있으면, 시간적·공간적 간격이 있더라도 강간상해죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 심리적 저항불능 상태의 지속과 시간적·공간적 간격의 법적 의미는 구체적 사실에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “강간범행 이후에도 피해자를 계속 끌고 다니거나 차량에 태우고 함께 이동하는 등으로 강간범행으로 인한 피해자의 심 리적 저항불능 상태가 해소되지 않은 상태에서 강간범의 상해행위가 있었다면 강간행위와 상해행위 사이에 다소의 시간적·공간적 간격이 있더라도 강간상해 죄가 성립한다고 할 수 있다.”

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

## 12. `art301_sec3.result_after_completion`

- proposition: 강간 등이 완료되기 전에 고의 또는 과실에 의한 상해 원인행위가 있으면, 상해 결과가 강간 등의 완료 후 발생하여도 본죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 원인행위의 완료 전 발생과 결과의 완료 후 발생이라는 시간관계를 기록한다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “강간 등이 완료되기 전에 고의 또는 과실에 의한 상해의 원인이 되는 행위가 있 으면 상해의 결과는 강간 등이 완료된 후에 발생하여도 본죄가 성립한다.”

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

## 13. `art301_sec3.unrelated_injury_exception`

- proposition: 강간 등의 기회가 아닌 다른 사정으로 상해 결과가 발생한 경우 본죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 상해 결과가 강간 등의 기회와 무관한 다른 사정에 의한 것인지는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제301조_Ⅲ_2` / `Ⅲ`: “반면 강간 등 기회가 아닌 다른 사정에 의하여 상해의 결과가 발생한 경우 본죄 는 성립하지 않는다.”

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

## 14. `art301_sec4_2.delayed_diagnosis_case`

- proposition: 대법원이 강제추행치상죄를 유죄로 판단한 원심판결에 상해에 관한 법리오해가 있다고 보아 이를 파기·환송한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 사례의 구체적 사실관계와 판결 원문을 확인하기 전에는 일반화된 상해 판단 기준으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.2_6` / `Ⅳ.2`: “대법원은 강제추행치상죄를 유죄로 판단한 원심판결에 상해에 관한 법리오해의 위법이 있다고 보아, 이를 파기·환송함.”

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

## 15. `art301_sec4_2.injury_diagnosis_evidence`

- proposition: 상해진단서는 특별한 사정이 없으면 피해자 진술과 함께 상해 사실의 유력한 증거가 되며, 합리적 근거 없이 그 증명력을 함부로 배척할 수 없다. 다만 객관성·신빙성을 의심할 사정이 있으면 그 증명력을 매우 신중히 판단해야 한다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 진단서 자체만으로 결론을 자동화하지 않고, 객관성·신빙성을 의심할 구체적 사정을 함께 평가해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.2_5` / `Ⅳ.2`: “상해진단서는 특별한 사정이 없는 한 피해자의 진술과 더불어 피고인의 상해 사실에 대한 유력한 증거가 되고, 합리적인 근거 없이 그 증명력을 함부로 배척 할 수 없다. 다만 대법원은 상해진단서의 객관성과 신빙성을 의심할 만한 사 정이 있는 때에는 증명력을 판단하는 데 매우 신중하여야 한다고 판시하고 있다.”

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
