# 강간 RuleIR 카드 검수 3

- unit: `rape`
- articles: art297
- cards: 31–45 / 56
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art297_sec4_3.completion`

- proposition: 남성 성기가 여성 성기에 삽입되거나 결합되는 순간 강간죄는 기수가 되며, 완전한 삽입·결합, 성적 만족 또는 사정은 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 삽입 또는 결합의 발생 여부와 완전한 삽입·결합 또는 사정의 불요를 구분하여 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.3_17` / `Ⅳ.3`: “남성의 성기가 여성의 성기에 삽입되거나 결합되는 순간 기수가 되고, 성기의 완전한 삽입, 결합이나 행위자의 성적 만족, 사정은 필요하지 않다.”

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

## 32. `art297_sec4_3.voluntary_abandonment`

- proposition: 행위자가 자의로 강간 범행의 실행을 중지한 경우 중지미수가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 실행 중지가 자의에 의한 것인지에 대한 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.3_17` / `Ⅳ.3`: “행위자가 자의로 강간 범행의 실행을 중지한 경우에는 ‘중지미수’가 (형법 제26조) 성립한다.”

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

## 33. `art297_sec4_4.successive_co_perpetration_negative`

- proposition: 선행자와의 공동가공 의사에 기한 기능적 행위지배를 후행자에게 인정할 수 없으면 승계적 공동정범은 성립할 수 없다는 대법원 취지가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판시의 원문과 적용된 사실관계를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.4_18` / `Ⅳ.4`: ““후행자에 대해서는 선행자와의 공동가공 의사에 기한 기능적 행위지배를 인정할 수 없으므로 승계적 공동정범 이 성립할 수 없다.”는 취지로 판시하고 있다.”

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

## 34. `art297_sec4_4.successive_perpetrator_quasi_rape`

- proposition: 선행자의 행위를 이용하여 피해자를 간음한 후행자에게는 준강간죄가 성립할 여지가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 준강간죄 성립 여부는 선행행위 이용, 피해자의 상태, 및 후행자의 인식에 관한 사실평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.4_18` / `Ⅳ.4`: “선행자의 행위를 이용하여 피해자를 간음한 후행자에 대해서는 준강간죄가 성립할 여지가 있다.”

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

## 35. `art297_sec5.consent_assessment`

- proposition: 성관계 승낙 여부는 행위 경위와 태양, 피해자 연령, 범행 당시 정황 등을 종합해 성적 자유 또는 성적 자기결정권 침해 여부를 기준으로 구체적·개별적으로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정을 종합하는 평가적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅴ_19` / `Ⅴ`: “승낙이 있 었는지 여부는 그 행위의 경위 및 태양, 피해자의 연령, 범행 당시의 정황 등 여 러 사정을 종합적으로 고려하여 그 행위로 인한 피해자의 성적 자유 또는 성적 자기결정권이 침해되었는지를 기준으로 삼아 구체적·개별적으로 판단하여야 한 다.”

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

## 36. `art297_sec5.prior_communications_not_consent`

- proposition: 피해자가 범행 무렵까지 피고인과 전화·문자 연락을 하고 호감을 보인 정황만으로 성관계 승낙 또는 묵인을 인정할 수는 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 연락 또는 호감 정황만으로는 승낙을 추론하지 않는 제한이다.
- bounded sources:

  - `comm_001692_제297조_Ⅴ_19` / `Ⅴ`: “범행 무렵까지 피해자가 피고인과 수시로 전화 통화나 문자메시지를 주고 받았다거나 그 내용 중에 피해자가 피고인에 대하여 호감을 가진 것으로 인정 할 만한 내용이 있다고 하여 피해자가 피고인과의 성관계를 승낙 내지 묵인하 였다고 볼 수는 없다.”

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

## 37. `art297_sec5.valid_consent`

- proposition: 피해자 본인의 성관계 승낙은 구성요건 해당성을 조각하며, 친권자 등의 승낙은 강간죄 성립에 영향을 주지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 본인 승낙의 존재와 범위는 개별 사실관계에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅴ_19` / `Ⅴ`: “피해자의 승낙은 구성요건 해당성을 조각하는 양해에 해당한다. ‘성관계의 승낙’ 은 본인의 승낙에 한정되고, 친권자 등의 승낙이 있더라도 본죄의 성립에는 지 장이 없다.”

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

## 38. `art297_sec5.withdrawn_consent`

- proposition: 피해자가 사전에 성관계를 승낙했더라도 동의를 번복하면 승낙이 있다고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사전 승낙과 번복 사실을 구별하여 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅴ_19` / `Ⅴ`: “피해자는 사전에 성관계를 승낙하였다고 하더라도 그 동의를 번복할 수 있고, 승낙을 번복한 경우에는 승낙이 있다고 볼 수 없다.”

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

## 39. `art297_sec6.intent`

- proposition: 강간죄에는 폭행·협박으로 피해자를 강간한다는 인식과 의사가 필요하고, 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행위자의 인식·의사 및 미필적 고의 여부는 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅵ_20` / `Ⅵ`: “본죄가 성립하기 위해서 폭행·협박으로 피해자를 강간한다는 점에 대한 인식과 의사가 있어야 한다. 고의는 미필적 고의로도 충분하다.”

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

## 40. `art297_sec6.mistake_of_consent`

- proposition: 피해자 승낙이 없음에도 승낙이 있다고 오인한 경우 강간죄의 고의가 조각된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 승낙이 있었다는 오인의 존재와 그 대상은 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅵ_20` / `Ⅵ`: “피해자의 승낙이 없음 에도 있는 것으로 오인한 경우에는 고의가 조각된다.”

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

## 41. `art297_sec7.continuous_acts_single_offense`

- proposition: 동일한 폭행·협박으로 피해자의 항거불가능 또는 현저한 곤란 상태가 계속되는 상황에서 수회 간음한 경우, 시간적·장소적 근접성과 범의의 단일성·계속성이 인정되면 포괄 일죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시간적·장소적 근접성 및 범의의 단일성·계속성은 사안별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅶ_21` / `Ⅶ`: “동일한 폭행·협박으로 피해자 의 항거가 불가능하거나 현저히 곤란한 상태가 계속되는 상황에서 수회에 걸쳐 간음한 경우, 예를 들면 피해자를 여관에 감금하여 하룻밤 동안 수회 간음한 경우 처럼 시간적·장소적으로 가까워 범의의 단일성과 계속성을 인정할 수 있을 (犯意) 때에는 포괄하여 일죄가 성립한다.”

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

## 42. `art297_sec7.multiple_victims_multiple_offenses`

- proposition: 피해자가 여러 명이면 동일한 장소에서 동일한 폭행·협박에 의한 경우에도 각 피해자에 따라 수개의 강간죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일 장소와 동일 폭행·협박만으로 복수 피해자에 대한 죄수 성립이 하나로 합쳐지지 않는다.
- bounded sources:

  - `comm_001692_제297조_Ⅶ_21` / `Ⅶ`: “피해자가 여러 명인 경우에는 비록 동일한 장소에서 동일 한 폭행·협박에 의한 것이라고 하더라도 각 피해자에 따라 수개의 죄가 성립한다.”

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

## 43. `art297_sec7.new_violence_separate_offense`

- proposition: 항거불능 상태가 종료된 후 다시 폭행·협박을 가하여 간음한 경우 별개의 강간죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 항거불능 상태의 종료와 새로운 폭행·협박의 존재가 확인된 경우의 죄수 관계를 정리한다.
- bounded sources:

  - `comm_001692_제297조_Ⅶ_21` / `Ⅶ`: “항거불능의 상태가 종료된 후 다시 폭행·협 박을 가하여 간음한 경우에는 별개의 강간죄가 성립한다.”

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

## 44. `art297_sec9.abduction_for_marriage_rape`

- proposition: 결혼을 목적으로 여자를 약취하여 강간한 경우 강간죄와 결혼을 위한 약취죄는 실체적 경합범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 결혼 목적의 약취죄 및 강간죄의 각 구성요건 충족 여부를 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_26` / `Ⅸ`: “결혼을 목적으로 여자를 약취하여 강간한 경우에는 본죄와 ‘결혼을 위한 약취죄 ’의 실체적 경합범이 성립한다.”

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

## 45. `art297_sec9.confinement_rape_attempted_case`

- proposition: 피해자가 주행 중인 자동차에서 탈출할 수 없는 상태를 이용하여 약 50km 강제연행한 후 강간하려다 미수에 그친 사안에서, 협박이 감금죄와 강간미수죄의 실행착수에 동시에 해당하면 두 죄는 상상적 경합에 해당한다고 한 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 특정 판시이다. 사용자 제공 1차 판례 인덱스로 원문 및 사실관계의 동일성을 확인한 뒤 적용해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: ““협박은 감금죄의 실행의 착수임과 동시에 강간미수죄의 실행의 착수이며, 감금죄와 강간미수죄는 하나의 행위에 의하여 실현된 경우로서 형법 제40조의 상상적 경합에 해당한다.”고 판단하였다.”

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
