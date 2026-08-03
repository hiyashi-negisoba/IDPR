# 상해·특수상해·상해치사 RuleIR 카드 검수 3

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 31–45 / 104
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

## 31. `art257_sec1_4.intent_definition`

- proposition: 상해의 고의란 사람의 생리적 기능을 해한다는 인식·인용을 말하며, 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 인식·인용 및 미필적 고의 여부는 구체적 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_18` / `Ⅰ.4`: “상해 의 고의란 사람의 생리적 기능을 해한다는 인식·인용을 말한다. 반드시 확정적 일 필요는 없고 미필적 고의로 충분하다.”

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

## 32. `art257_sec1_4.intent_element`

- proposition: 상해죄가 성립하기 위한 주관적 구성요건으로 상해의 고의가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해죄의 주관적 구성요건에 관한 commentary synthesis다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_18` / `Ⅰ.4`: “상해죄가 성립하기 위한 주관적 구성요건으로 상해의 고의가 있어야 한다.”

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

## 33. `art257_sec1_4.intent_only_violence_result`

- proposition: 상해의 고의 없이 폭행의 고의로 상해 결과가 발생하였다면 상해죄가 아니라 폭행치상죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상해의 고의 부재와 폭행의 고의 및 상해 결과의 구별은 사실관계 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_18` / `Ⅰ.4`: “그러므로 상해의 고의 없이 폭행의 고의로 상해의 결과가 발생하였다면 폭행치 상죄가 성립한다.”

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

## 34. `art257_sec1_4.object_method_mistake`

- proposition: 구성요건 착오 중 구체적 사실의 착오인 객체의 착오나 방법의 착오는 고의를 조각하지 않고 상해죄의 성립을 방해하지 않는다는 것이 판례의 태도이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 판례 원문을 사용자 제공 primary precedent index에서 확인하기 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_19` / `Ⅰ.4`: “구성요건 착오 중 구체적 사실의 착오로서 이른바 객체의 착오나 방법의 착오 는 고의를 조각하지 않고, 상해죄의 성립을 방해하지 않는다는 것이 판례의 태 도이다.”

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

## 35. `art257_sec1_4.unintended_victim`

- proposition: 목적한 사람이 아닌 다른 사람에게 상해를 입혔다고 하더라도 상해의 고의가 인정되고 과실상해죄에 해당한다고 할 수는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 객체의 착오 관련 판례 태도에서 도출된 commentary-reported precedent이며, 원문 판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_19` / `Ⅰ.4`: “따라서 목적한 사람이 아닌 다른 사람에게 상해를 입혔다고 하더라도 상해의 고의가 인정되고, 과실상해죄에 해당한다고 할 수는 없다.”

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

## 36. `art257_sec1_5.causation.objective_attribution`

- proposition: 객관적 귀속론에 따르면 상해행위와 결과 사이에 합법칙적 조건관계가 있고 결과를 상해행위에 귀속할 수 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 객관적 귀속론의 조건관계 및 귀속 판단은 기계적으로 열거할 수 없는 평가를 포함한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.5_20` / `Ⅰ.5`: “객관적 귀속론에 의하면, 상해행위과 결과 사이에 합법칙적 조건 관계가 있어야 하고, 상해결과를 상해행위에 귀속시킬 수 있어야 한다.”

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

## 37. `art257_sec1_5.causation.result_and_causation`

- proposition: 상해죄 성립에는 상해의 고의가 있는 행위로 인하여 발생한 인과관계 있는 상해 결과가 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해 결과와 행위 사이의 인과관계는 개별 사실관계에 대한 평가가 필요하므로 standard input으로 유지한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.5_20` / `Ⅰ.5`: “상해죄의 성립에는 상해의 고의가 있는 행위로 인하여 발생하는 인 과관계 있는 상해의 결과가 있어야 한다.”

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

## 38. `art257_sec1_5.causation.tooth_injury_disparity`

- proposition: 왜소한 중년 부인이 건강한 거구 남성의 뺨을 두 차례 때린 사안에서, 병약한 치아 등 특별한 사정이 없는 한 구타와 치아 탈구 사이 인과관계는 인정되기 어렵다는 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 신체 조건, 타격의 강도 및 치아의 기존 상태가 특정된 좁은 보고 사례이며, 다른 상해 유형에 일반화하지 않는다. 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.5_20` / `Ⅰ.5`: “피고인의 구타로 곧바로 피해자의 치아가 탈구된다는 것이 그 힘의 차이로 보아 쉽게 수긍되지 않는다는 이유로 원래 병약한 상태의 치아였 다는 등의 특별한 사정이 없는 한 그 인과관계가 인정되기 어렵다고 한 사례”

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

## 39. `art257_sec1_6.defensive_force_not_new_attack`

- proposition: 외관상 상호 싸움처럼 보여도 일방의 위법한 공격에 대항한 유형력 행사가 새로운 적극적 공격으로 평가되지 않고 사회관념상 상당하면 위법성이 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 일방 공격, 저항수단, 새로운 적극적 공격 여부 및 상당성을 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_21` / `Ⅰ.6`: “실제로는 한쪽 당사자가 일방적으로 위법한 공격을 가하고 상대방은 이러한 공격으로부터 자신을 보호하고 이를 벗어나 기 위한 저항수단으로서 유형력을 행사한 경우에는 그 행위가 새로운 적극적인 공 격이라고 평가되지 아니하는 한 사회관념상 허용될 수 있는 상당성이 있는 행위로 서 위법성이 조각되고”

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

## 40. `art257_sec1_6.disciplinary_injury`

- proposition: 징계행위가 교육목적상 필요·적절하고 사회통념상 용인될 정도여야 하므로, 피징계자를 상해에 이르게 한 징계는 원칙적으로 상해죄의 위법성을 조각할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 교육목적상 필요·적절성 및 사회통념상 용인 가능성은 평가가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_26` / `Ⅰ.6`: “징계 권 행사의 범위는 교육목적을 달성하는 데 필요하고 적절하여 사회통념상 용인될 수 있을 정도에 그쳐야 하므로, 징계권의 행사로 피징계자를 상해에까지 이르게 하 는 것은 이미 징계행위의 방법이 정당하지 않았거나 징계권의 범위를 넘었다고 보아야 하기 때문에, 원칙적으로 상해죄의 위법성을 조각한다고 할 수 없다.”

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

## 41. `art257_sec1_6.insufficient_medical_explanation`

- proposition: 정확하거나 충분한 설명 없이 받은 수술 승낙은 수술의 위법성을 조각할 유효한 승낙이 될 수 없다는 대법원 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 대법원 사례의 원문 및 설명의 정확성·충분성 기준을 확인해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_25` / `Ⅰ.6`: “위 승낙은 부정확 또는 불충분한 설명을 근거로 이루어진 것으로서 수술의 위법성을 조각할 유효한 승 낙이라고 볼 수 없다.”

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

## 42. `art257_sec1_6.military_detention_beating`

- proposition: 상관이 훈련 중 부하 방위병을 감금·구타한 행위가 훈육권 또는 징계권 범위를 넘으면 위법하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 훈육권 또는 징계권의 범위 초과 여부는 사실관계와 원전 확인이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_28` / `Ⅰ.6`: “상관 이 부하인 방위병을 훈련 중에 감금, 구타한 행위는 훈육권 내지 징계권의 범위 를 넘어선 것으로 위법하고”

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

## 43. `art257_sec1_6.military_minor_restraint`

- proposition: 야간에 술에 취하여 신병들에게 행패를 부리는 피해자를 소대장이 제지하는 과정에서 군대 질서 유지 목적으로 한 경미한 폭행은 사회상규에 위배되지 않는 행위로 위법성이 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 사례의 구체적 전제와 경미한 폭행 및 질서유지 목적의 판단을 원전으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_28` / `Ⅰ.6`: “군대 내의 질서를 지키려는 목적에서 행한 경미한 폭”
  - `comm_001692_제257조_Ⅰ.6_28` / `Ⅰ.6`: “행은 사회상규에 위배되지 않는 행위로서 위법성이 조각될 수 있지만”

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

## 44. `art257_sec1_6.military_unauthorized_punishment_order`

- proposition: 상사 계급자가 얼차려 결정권자가 아니고 부대 지침상 허용되지 않은 얼차려를 지시한 경우, 그 지시행위는 정당행위에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 결정권 및 부대 지침의 적용 내용은 보고된 판례 원문과 당시 규정을 확인해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_28` / `Ⅰ.6`: “상사 계급의 피고인이 부대원들에게 얼차려를 지시할 당시 얼차려의 결정권자도 아니었고 소속 부대의 얼차려 지침상 허용되 는 얼차려도 아닌 경우 그 얼차려 지시 행위는 정당행위에 해당하지 않는다고 한다.”

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

## 45. `art257_sec1_6.mutual_fight_no_self_defense`

- proposition: 방어행위가 아닌 상해는 정당방위가 될 수 없고, 서로 싸워 상대방에게 상해를 가한 경우에는 위법성이 조각되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 행위가 방어인지 상호 공격인지에 관한 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_21` / `Ⅰ.6`: “방 어를 위한 행위가 아닌 상해는 정당방위가 될 수 없고, 따라서 싸움에 의하여 서로 상대방에게 상해를 가한 때에는 위법성이 조각되지 않는다.”

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
