# 준강간·준강제추행 RuleIR 카드 검수 1

- unit: `quasi_sexual_offense`
- articles: art299
- cards: 1–15 / 26
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #27 `art299_sec7.changed_circumstances_concurrence`: `art299_sec7.changed_circumstances_rape_only` (status=`valid`)

## 1. `art299.attempt_commencement`

- proposition: 본죄의 실행 착수는 심신상실 또는 항거불능 상태를 이용한 간음·유사간음·추행의 수단이라고 할 수 있는 행동을 개시한 때이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 어떤 구체적 행동이 간음·유사간음·추행의 수단에 해당하는지는 개별 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “본죄의 실행의 착수시기는 심신상실 또는 항거불능의 상태를 이용하여 간음이”
  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “나 유사간음 또는 추행의 수단이라고 할 수 있는 행동을 개시한 때”

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

## 2. `art299.offense_characterization`

- proposition: 준강간·준강제추행죄는 사람의 심신상실 또는 항거불능 상태를 이용하여 간음 또는 추행함으로써 성립하는 범죄이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 심신상실 또는 항거불능 상태의 구체적 범위와 그 상태를 이용하였는지 여부는 별도 법률 검토가 필요하다.
- bounded sources:

  - `comm_001692_제299조_Ⅰ_0` / `Ⅰ`: “본죄는 사람의 심신상실 또는 항거불능의 상태를 이용하여 간음 또는 추행을 함으로써 성립하는 범죄”

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

## 3. `art299.principal.unrestricted`

- proposition: 본죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체의 성별 또는 신분 제한이 없다는 범위에서만 기계적으로 열거 가능한 관계로 정리했다.
- bounded sources:

  - `comm_001692_제299조_Ⅱ_1` / `Ⅱ`: “본죄의 주체에는 아무런 제한이 없다. 남성과 여자 모두 본죄의 주체가 된다.”

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

## 4. `art299.successive_participant_only_art299`

- proposition: 타인이 폭행·협박으로 피해자를 항거불능에 빠뜨린 뒤 그 사실을 알고 가담하여 간음·유사간음·추행한 자는, 타인과의 공동가공 의사에 기한 기능적 행위지배를 인정할 수 없으면 강간죄·유사강간죄·강제추행죄는 성립하지 않고 본죄만 성립한다는 견해가 제시된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 후행 가담자의 공동가공 의사 및 기능적 행위지배의 인정 여부와 해당 결론의 판례상 지위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “타인과의 공동가공 의사에 기한 기능적 행”
  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “위지배를 인정할 수 없으므로 강간죄나 유사강간죄 또는 강제추행죄는 성립”
  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “하지 않고, 본죄만 성립한다고 봄이 타당하다.”

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

## 5. `art299.use_awareness_and_facilitation`

- proposition: 제299조에서 상태의 이용은 행위자가 피해자의 심신상실 또는 항거불능 상태를 인식하고, 그 상태 때문에 간음 또는 추행이 용이해졌음을 의미한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상태 인식과 상태로 인한 행위 용이성은 구체적 사실관계에 따라 평가한다.
- bounded sources:

  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “‘이용’이라 함은 행위자가 심신상실이나 항거불능”
  - `comm_001692_제299조_Ⅳ_8` / `Ⅳ`: “의 상태에 있는 피해자를 인식하고 또한 그러한 상태 때문에 간음이나 추행이 용이하게 되었음을 의미한다.”

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

## 6. `art299_sec3_1.object_incapacitated_person`

- proposition: 본죄의 객체는 심신상실 또는 항거불능 상태에 있는 사람이며, 사람은 성별을 불문한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 객체의 상태 및 성별 비한정에 관한 서술이다. 심신상실과 항거불능의 구체적 범위는 이 카드의 인용 범위를 넘어 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.1_2` / `Ⅲ.1`: “본죄의 객체는 심신상실 또는 항거불능의 상태에 있는 ‘사람’이다. ‘사람’은 남성”
  - `comm_001692_제299조_Ⅲ.1_2` / `Ⅲ.1`: “과 여성을 불문한다.”

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

## 7. `art299_sec3_2.blackout_not_dispositive`

- proposition: 음주 또는 약물로 성관계 당시 상황을 기억하지 못하는 피해자에 대하여 알코올 블랙아웃 가능성만으로 심신상실 또는 항거불능 상태가 아니라고 단정해서는 안 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 알코올 블랙아웃 가능성은 심신상실 또는 항거불능 배제의 단독 근거가 아니다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_5` / `Ⅲ.2`: “준강간 또는 준강제추행의 피”
  - `comm_001692_제299조_Ⅲ.2_5` / `Ⅲ.2`: “해자가 음주 또는 약물로 인하여 성관계 당시의 상황을 기억하지 못하는 경우”
  - `comm_001692_제299조_Ⅲ.2_5` / `Ⅲ.2`: “에 알코올 블랙아웃의 가능성을 인정하여 심신상실 또는 항거불능의 상태가 아”
  - `comm_001692_제299조_Ⅲ.2_5` / `Ⅲ.2`: “니라고 단정하여서는 아니 된다.”

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

## 8. `art299_sec3_2.drug_administration_violence_exception`

- proposition: 간음·추행 목적으로 마취제·수면제 등을 사용하여 피해자를 심신상실 또는 항거불능에 빠뜨린 경우 그 투여가 폭행에 해당할 수 있어 본죄가 아니라 강간죄·유사강간죄 또는 강제추행죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 마취제·수면제 등의 투여가 폭행에 해당하는지는 개별 사안에서 평가해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_7` / `Ⅲ.2`: “위와 같은 마취제 등의 투여가 ‘폭행’에 해당할 수 있으므로, 본죄가 아니라 강간죄나 유사강간죄 또는 강제추행죄가 성립한다”

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

## 9. `art299_sec3_2.existing_incapacity_used`

- proposition: 이미 존재한 심신상실 또는 항거불능 상태를 이용하여 간음·유사간음·추행하면 본죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 기존의 심신상실 또는 항거불능 상태를 이용한 행위라는 성립 관계를 나타낸다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_7` / `Ⅲ.2`: “이미 존재한 심신상실이나 항거불능의 상태를 이용하여 간음·유사간음·”
  - `comm_001692_제299조_Ⅲ.2_7` / `Ⅲ.2`: “추행하였다면 본죄가 성립한다.”

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

## 10. `art299_sec3_2.incapacity_origin_irrelevant`

- proposition: 본죄 성립에서 심신상실 또는 항거불능 상태에 이르게 된 원인은 묻지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 상태에 이르게 된 원인의 유형을 별도 성립요건으로 요구하지 않는다는 범위의 관계다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_6` / `Ⅲ.2`: “본죄의 성립에 있어 심신상실이나 항거불능의 상태에 이르게 된 ‘원인’은 묻지 않는다.”

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

## 11. `art299_sec3_2.memory_not_dispositive`

- proposition: 피해자가 피해 사실을 기억하더라도 항거불능 상태가 아니라고 단정해서는 안 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 기억 유무만으로 항거불능을 배제하지 않고 당시의 대응 가능성을 평가해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_4` / `Ⅲ.2`: “피해자가 피해사실을 기억하고 있더라도 항거불능 상태가 아니라고 단정하여서”
  - `comm_001692_제299조_Ⅲ.2_4` / `Ⅲ.2`: “는 아니 된다.”

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

## 12. `art299_sec3_2.mental_incapacity_definition`

- proposition: 심신상실은 정신기능 장애로 성적 행위에 관한 정상적 판단능력이 없는 상태를 뜻한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 정상적 판단능력의 유무는 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_3` / `Ⅲ.2`: “‘심신상실’이란 정신기능의 장애로 인하여 성적 행위에 대한 정상적인 판단능력이 없는 상태를 의미”

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

## 13. `art299_sec3_2.religious_psychological_resistance`

- proposition: 종교지도자의 절대적 권위로 인한 정신적 혼란, 종교적 유익성에 대한 믿음 또는 지옥에 갈 것이라는 맹신 등으로 거절이 절대적으로 불가능하거나 현저히 곤란한 경우 심리적 항거불능이 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 판단으로서 원판례 확인 전에는 commentary-reported precedent에 그친다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_6` / `Ⅲ.2`: “피고인에게 반항하는 것이 절대적으로 불가능하거나 현저하게 곤란”
  - `comm_001692_제299조_Ⅲ.2_6` / `Ⅲ.2`: “한 심리적 항거불능 상태에 있었다고 판단하여 심리적 항거불능을 인정하였다.”

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

## 14. `art299_sec3_2.resistance_incapacity_definition`

- proposition: 항거불능은 심신상실 이외 원인으로 심리적 또는 물리적으로 반항이 절대적으로 불가능하거나 현저히 곤란한 상태를 의미한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 심리적 또는 물리적 반항 곤란성은 개별 사정에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_3` / `Ⅲ.2`: “‘항거불능’의 상태란 심신상실 이외의 원인으로 심리적 또는 물리적으로 반항이 절대적으로 불가능하거나 현저히 곤란한 경우를 의”

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

## 15. `art299_sec3_2.sleep_or_unconsciousness`

- proposition: 피해자가 깊은 잠에 빠졌거나 술·약물 등으로 일시적으로 의식을 잃은 상태는 심신상실 또는 항거불능 상태에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 의식 상실의 정도와 정상적 판단·대응·조절능력의 행사 가능성을 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅲ.2_3` / `Ⅲ.2`: “피해자가 깊은 잠에 빠져 있거”
  - `comm_001692_제299조_Ⅲ.2_3` / `Ⅲ.2`: “나 술·약물 등에 의해 일시적으로 의식을 잃은 상태 또는 완전히 의식을 잃지는 않”
  - `comm_001692_제299조_Ⅲ.2_3` / `Ⅲ.2`: “았더라도 그와 같은 사유로 정상적인 판단능력과 대응·조절능력을 행사할 수 없는 상태에 있었다면 준강간죄 또는 준강제추행죄에서의 심신상실 또는 항거불능 상태에 해당한다.”

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
