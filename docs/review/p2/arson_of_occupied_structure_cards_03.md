# 현주건조물등방화 RuleIR 카드 검수 3

- unit: `arson_of_occupied_structure`
- articles: art164
- cards: 31–45 / 52
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #2 `art164_sec2_1.post_killing_arson`: `art164_sec2_1.post_killing_arson_precedent` (status=`valid`)
- #3 `art164_sec2_1.completion`: `art164_sec2_1.completion_independent_combustion_variant` (status=`valid`)
- #4 `art164_sec3_2.attempted_basic_arson_subject`: `art164_sec3_2.attempted_basic_arson_included` (status=`valid`)
- #5 `art164_sec3_6.intentional_fire_death_murder_concurrence`: `art164_sec3_6.intentional_fire_death_murder_concurrence_affirmative` (status=`valid`)
- #15 `art250_sec2_10.arson_death_parricide_concurrence`: `art250_sec2_10.arson_death_parricide_specialty_precedent` (status=`valid`)

## 31. `art164_sec2_3.multiple_buildings_one_act`

- proposition: 1개의 방화행위로 여러 현주건조물을 불태운 경우 1개의 현주건조물방화죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 복수 현주건조물에 대한 결과가 하나의 방화행위에서 발생했는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.3_14` / `Ⅱ.3`: “1개의 방화행위 에 의하여 수개의 현주건조물을 불태운 경우에는 1개의 현주건조물방화죄가 성 립한다.”

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

## 32. `art164_sec2_3.multiple_objects_separate_acts_concurrence`

- proposition: 수개의 방화행위로 수개의 목적물을 각각 불태운 경우 원칙적으로 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 별개의 방화행위인지 및 각 목적물에 대한 개별 침해가 있는지 검토해야 하며, 원칙에 대한 예외는 이 카드의 범위에 포함되지 않는다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.3_14` / `Ⅱ.3`: “수 개의 방화행위에 의해 수 개의 목적물을 각각 불태운 경우에는 수 개의 재산 적 법익을 침해한 것이므로 원칙적으로 경합범이 된다.”

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

## 33. `art164_sec2_3.same_area_sequential_arson`

- proposition: 같은 구역의 여러 건조물에 동일 기회에 차례로 방화한 때에는 1개의 방화죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 같은 구역 및 동일 기회에 해당하는지는 구체적 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.3_14` / `Ⅱ.3`: “같은 구역 내에 있는 수개의 건조물을 동일한 기회에 차례로 방화한 때 에도 1개의 방화죄만 성립한다.”

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

## 34. `art164_sec2_3.sequential_ignition_same_object`

- proposition: 동일 목적물의 여러 곳에 순차 점화하더라도 통상 단일한 방화행위로 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 순차 점화가 단일 방화행위인지 여부는 구체적 시간적·장소적 연속성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.3_14` / `Ⅱ.3`: “동일 목적물을 순차 여러 군데에 점화하여도 통상 단일한 방화행위로 인정된다.”

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

## 35. `art164_sec2_3.unit_of_offense_public_safety`

- proposition: 방화죄의 죄수는 방화행위의 단일성과 주된 보호법익인 공공의 안전을 기준으로 판단하며, 피해물건 수는 부수적 기준이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 방화행위의 단일성과 동일 기회 여부의 적용에는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.3_14` / `Ⅱ.3`: “방화죄의 죄수는 방화행위의 단일성과 함께 주된 보호법익인 공공의 안전을 기 준으로 판단하여야 한다. 피해물건의 개수는 부수적 기준에 불과하다.”

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

## 36. `art164_sec3_1.fire_death_injury`

- proposition: 현주건조물등방화치사상죄는 형법 제164조 제1항의 현주건조물 등에 방화하여 사람을 상해 또는 사망에 이르게 한 경우 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제164조 제1항의 현주건조물 등에 대한 방화와 사람의 상해 또는 사망 결과를 연결하는 기본 구성요건 설명이다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.1_18` / `Ⅲ.1`: “본죄는 형법 제164조 제1항의 현주건조물 등에 방화하여 사람을 상해나 사망에 이르게 한 경우에 성립한다.”

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

## 37. `art164_sec3_1.fire_death_injury_foreseeability`

- proposition: 현주건조물에 방화하여 그 안 거주자의 사망 또는 상해를 예견할 수 있는 경우 현주건조물등방화치사상죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 거주자의 사망 또는 상해 결과에 대한 예견가능성은 구체적 사실관계에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.1_18` / `Ⅲ.1`: “현주건조물에 방화하여 그 결과로 그 안에 거 주하던 사람이 사망하거나 상해를 입을 것을 예견할 수 있었던 경우, 즉 예견가 능성이 있는 때에는 본죄에 해당한다.”

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

## 38. `art164_sec3_1.intentional_killing_fire_death_holding`

- proposition: 사람을 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우 현주건조물방화치사죄로 의율하고 살인죄와 상상적 경합으로 의율하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 commentary에 보고된 판례 입장이다. 원판례를 사용자 제공 primary precedent index에서 확인하기 전에는 경쟁 학설에 대한 정책 선택 근거로 사용하지 않는다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.1_18` / `Ⅲ.1`: “사람을 살해할 목적으로 현주건조물에 방화하여 사망 에 이르게 한 경우에는 현주건조물방화치사죄로 의율하여야 하고 이와 더불어 살인 죄와의 상상적 경합범으로 의율할 것은 아니라고 할 것이고”

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

## 39. `art164_sec3_2.fire_related_death_injury_causation`

- proposition: 방화치사상의 상해·사망은 불에 타는 경우뿐 아니라 연기·가스 질식, 무너지는 건조물로 인한 상해·압사, 피난 중 추락, 화재 충격으로 인한 사망의 경우에도 인과관계가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 결과 발생 경로라도 구체적 사안에서 방화와 결과 사이의 인과관계 평가는 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.2_19` / `Ⅲ.2`: “상해 또는 사망의 결과에 대한 인과관계는 사람이 불에 타죽은 경 우뿐만 아니라 연기나 가스에 의해 질식사하거나 넘어지는 건조물 등에 의해 상해를 입거나 압사한 경우, 불을 피하여 뛰어내리거나 불에 대한 쇼크로 사망 한 경우에도 인정된다.”

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

## 40. `art164_sec3_2.person_excludes_offenders_accomplices`

- proposition: 현주건조물등방화치사상죄의 객체인 사람은 범인과 공범 이외의 모든 자연인이므로, 방화 공동정범 또는 공범이 사상된 경우에는 본죄에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 사상자가 범인 또는 공범인지 여부를 구분하는 객체 범위 제한이다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.2_19` / `Ⅲ.2`: “객체인 ‘사람’은 범인과 공범 이외의 모든 자연인을 말한다. 따라서 방화의 공동 정범 또는 공범이 사상된 경우에는 본죄에 해당하지 않는다.”

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

## 41. `art164_sec3_2.unforeseeable_firefighting_injury`

- proposition: 피해자가 화상을 입으면서 진화할 것을 전혀 예상할 수 없고 일반인에게도 그러한 진화작업이 이례적이면, 그 결과는 예견 가능한 결과라고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 진화행위가 전혀 예상할 수 없었는지 및 일반인에게 이례적인지에 관한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.2_19` / `Ⅲ.2`: “피해자가 화상을 입어가면서 진화할 것을 전혀 예상할 수 없었고, 일반인도 그와 같은 화상을 입어가면서 진화작업에 열중하는 것이 이례적이라면 예견할 수 있는 결과라고 할 수 없다.”

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

## 42. `art164_sec3_3.multiple_victims_imaginary_concurrence`

- proposition: 1개의 행위로 여러 사람에게 사망 또는 상해가 발생하면 각 치사죄 또는 각 치상죄의 상상적 경합이 되고, 사망과 상해가 함께 발생하면 치사죄와 치상죄의 상상적 경합이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 복수 피해자, 사망·상해 결과 및 단일 행위 여부의 적용에는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.3_20` / `Ⅲ.3`: “1개의 행위로 사망 또는 상해가 별개로 여러 사람에게 생긴 때에는 각 치사죄의 상상적 경합 또는 치상죄의 상상적 경합이 되고, 사망과 상해가 동시에 생긴 경 우 치사죄와 치상죄의 상상적 경합이 된다.”

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

## 43. `art164_sec3_4.intentional_killing_no_death`

- proposition: 사람을 살해할 생각으로 현주건조물에 방화하였으나 사망하지 않은 경우 현주건조물방화죄와 살인미수죄의 상상적 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 살해 의도와 사망 결과 부재의 사실인정이 필요하며, 상상적 경합의 근거는 현재 commentary synthesis에 한정된다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.4_21` / `Ⅲ.4`: “사람을 살해할 생각으로 현주건조물에 방화하 였으나 사망하지 않은 경우 현주건조물방화죄와 살인미수죄의 상상적 경합범이 된다.”

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

## 44. `art164_sec3_5.accomplice_aggravated_result_foreseeability`

- proposition: 현존건조물방화치상죄와 같은 부진정결과적가중범에서 집단 방화 과정 중 일부가 고의로 살상을 가하여도 다른 집단원에게 사상 결과의 예견가능성이 있으면 다른 집단원도 치사상의 책임을 면할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 다른 집단원별로 사상 결과의 예견가능성을 평가해야 하며, 일부 집단원의 고의 살상만으로 책임을 자동 확정하지 않는다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.5_22` / `Ⅲ.5`: “일부 집단원이 고의행위로 살상을 가한 경우에도 다른 집단원에게 그 사상의 결과가 예견가능한 것이었다면 다른 집단원도 그 결과에 대하여 현존건조물방화치사 상의 책임을 면할 수 없다.”

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

## 45. `art164_sec3_5.aider_aggravated_result_foreseeability`

- proposition: 현주건조물등방화치사상죄의 교사범 또는 방조범은 기본범죄의 교사·방조 외에 중한 결과에 대한 예견가능성이 인정되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 교사 또는 방조 사실과 별개로 중한 결과에 대한 예견가능성을 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.5_22` / `Ⅲ.5`: “교사범과 방조범의 성립도 가능하다. 이때 기본범죄를 교사하거나 방조하는 것 외에 중한 결과에 대한 예견가능성이 인정되어야 한다.”

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
