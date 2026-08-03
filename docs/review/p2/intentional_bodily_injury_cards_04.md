# 상해·특수상해·상해치사 RuleIR 카드 검수 4

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 46–60 / 104
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

## 46. `art257_sec1_6.old_education_law_corporal_punishment`

- proposition: 초·중등교육법 시행 전 사안에서 교사의 교육목적 달성을 위한 체벌은 방법과 정도가 사회상규에 벗어나지 않으면 정당행위에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 초·중등교육법 시행 전이라는 시간적 범위 및 사회상규 판단을 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_29` / `Ⅰ.6`: “교사의 교육목적 달성을 위한 처벌로서 그 체벌의 방법과 정도가 사회상 규에 벗어나지 않으면 정당행위에 해당하되”

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

## 47. `art257_sec1_6.old_education_law_injurious_corporal_punishment`

- proposition: 초·중등교육법 시행 전 사안에서도 교사의 체벌이 상해에 이른 경우 일반적으로 용인되는 교육업무상의 정당행위를 벗어나 위법하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 원문과 상해 결과의 인정 기준을 확인해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_29` / `Ⅰ.6`: “상해에 이른 경우에는 일반적으로 용인되는 교육업무상의 정당한 행위를 벗어난 것으로서 위법하다고 보았다.”

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

## 48. `art257_sec1_6.parental_corporal_punishment`

- proposition: 친권자의 체벌은 자녀 보호·교양을 위해 불가피한 경우 극히 제한된 범위에서 사회상규에 반하지 않는 행위로만 허용될 수 있다는 견해가 제시된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 출처의 견해 제시에 한정되며, 불가피성 및 제한된 범위는 개별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_27` / `Ⅰ.6`: “친권자의 체벌은 자녀의 보호 또는 교양을 위하여 불가피한 경우에 극히 제한된 범위에서 사회상규에 반하지 아니하는 행위로서 허 용된다고 봄이 타당할 것이다.”

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

## 49. `art257_sec1_6.passenger_risk_consent`

- proposition: 운전 미숙 또는 음주 사실을 알면서 동승하는 등 운전 위험을 감수하고 동승한 경우 과실상해에 대한 승낙으로 위법성이 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 운전 위험에 관한 인식과 위험 감수의 범위를 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_24` / `Ⅰ.6`: “운전자가 운전을 할 줄 모른다거나 음주한 사실을 알면서 동승하는 등 운전에 대한 위험성을 감수하고 동승한 경우에 는 과실에 의한 상해에 대하여 피해자의 승낙으로 위법성이 조각될 수 있다.”

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

## 50. `art257_sec1_6.pre_amendment_teacher_guidance`

- proposition: 개정 전 시행령 적용 사안에서 교사의 폭행·욕설 지도행위는 교육상 필요와 불가피성, 그리고 방법·정도의 객관적 타당성을 모두 갖춘 경우에만 법령에 의한 정당행위가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 개정 전 시행령의 적용 시점 및 보고된 판례의 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_28` / `Ⅰ.6`: “학생에 대한 폭 행, 욕설에 해당되는 지도행위는 교육상 불가피한 때, 즉 학생의 잘못된 언행을 교정하려는 목적에서 다른 교육적 수단으로는 교정이 불가능하였던 경우에만 허용되고, 그 방법과 정도에서도 사회통념상 용인될 수 있을 만한 객관적 타당 성을 갖추었던 경우에만 법령에 의한 정당행위로 볼 수 있다.”

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

## 51. `art257_sec1_6.self_injury_not_constitutive`

- proposition: 자상행위는 상해죄의 구성요건에 해당하지 않으므로 타인이 자상에 관여하는 방조·교사 행위도 범죄가 되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 출처는 자상행위와 그 방조·교사 관여의 비범죄성을 직접 서술한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_22` / `Ⅰ.6`: “자상(⾃傷)행위의 경우 상해죄의 구성요건에 해당하지 아니하므로 타인이 이를 방조하거나 교사하는 등 자상에 관여하는 행위도 범죄로 되지 아니한다.”

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

## 52. `art257_sec1_6.sport_rules_consent`

- proposition: 복싱·레슬링·유도 등 상해가 예견되는 운동경기에서 규칙을 지켜 경기한 경우 그에 수반된 상해는 승낙에 의해 위법성이 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 경기 규칙 준수와 해당 상해가 경기 수반 위험인지의 판단이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.6_24` / `Ⅰ.6`: “복싱·레슬링·유 도 등과 같이 신체의 상해를 예견할 수 있는 운동경기의 경우에 규칙을 지키고 경 기를 하는 이상 이에 수반된 상해는 피해자의 승낙에 의하여 위법성이 조각된다고 할 수 있다.”

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

## 53. `art257_sec1_7.assault_absorbed_by_injury`

- proposition: 상해의 고의로 폭행을 가한 후 상해한 경우 폭행은 상해죄에 흡수된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해의 고의와 폭행 후 상해 발생의 사실관계를 전제로 하는 흡수 관계다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “상해의 고의로 폭행을 가한 후에 상해한 경우 폭행은 상해 죄에 흡수된다.”

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

## 54. `art257_sec1_7.different_victims_separate_offenses`

- proposition: 상해행위가 동일한 일시·장소와 동일한 목적 아래 이루어졌더라도 피해자가 다르면 피해자별로 별개의 상해죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피해자별 상해 및 피해자 동일성의 사실판단을 전제로 하는 죄수 판단이다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “상해를 입힌 행위가 동일한 일시, 장소에서 동일한 목적으로 저질러 진 것이라 하더라도 피해자가 다르면 피해자별로 별개의 상해죄를 구성한다.”

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

## 55. `art257_sec1_7.injury_absorbed_by_murder`

- proposition: 상해 후 살인한 경우 상해는 살인의 수반행위로서 살인죄와 법조경합 관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상해와 살인의 시간적·행위적 관계 및 수반행위 해당성을 검토해야 하며, 상해죄의 별도 성립을 제한하는 관계다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “상해 후 살인한 경우 상해는 살인의 수반행위로서 살인죄와 법 조경합 관계에 있다고 본다.”

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

## 56. `art257_sec1_7.personal_legal_interest_count`

- proposition: 상해죄의 보호법익은 일신전속적 법익이므로 침해된 법익 수에 따라 죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 침해법익 수에 따른 죄수 판단의 기초 명제다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “상해죄의 보호법익은 일신전속적 법익이므로 침해법익의 수에 따라 죄가 성립한 다.”

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

## 57. `art257_sec1_7.single_act_multiple_injuries`

- proposition: 1개의 행위로 여러 사람을 상해하면 여러 상해죄의 상상적 경합이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 하나의 행위인지 및 각 피해자에 대한 상해 성립 여부의 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “따라서 1개의 행위로 여러 사람을 상해하면 여러 개 상해죄의 상상적 경합이 된다.”

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

## 58. `art257_sec1_7.threat_absorbed_by_injury`

- proposition: 같은 시간·장소에서 동일한 피해자를 상해하면서 한 협박은 특별한 사정이 없으면 상해의 단일한 고의 아래 이루어진 폭언으로서 상해죄에 흡수된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 동일한 시간·장소·피해자 및 특별한 사정의 존부를 검토해야 하며, 흡수에 따른 별도 협박죄 불성립을 의미하는 제한 규범이다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.7_30` / `Ⅰ.7`: “같은 시간, 장소에서 동일한 피해자를 상해하면서 협박한 경우 특별한 사정이 없는 한 협박은 상해의 단일한 고의 아래 이루어진 하나의 폭언에 불과하여 상 해죄에 흡수되고”

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

## 59. `art257_sec2.ancestral_injury_elements`

- proposition: 존속상해죄는 자기 또는 배우자의 직계존속의 신체를 상해함으로써 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 존속상해죄의 행위 및 피해자 관계에 관한 기본 구성요건으로 검토한다.
- bounded sources:

  - `comm_001692_제257조_Ⅱ_31` / `Ⅱ`: “이 죄는 자기 또는 배우자의 직계존속의 신체를 상해함으로써 성립하는 범죄이 다.”

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

## 60. `art257_sec2.legal_ascendant_scope`

- proposition: 존속상해죄의 배우자와 직계존속은 법률상 개념이므로 사실상 배우자나 사실상 직계존속은 포함되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사실상 관계가 법률상 배우자 또는 직계존속 요건을 충족하지 않는다는 명시적 배제 규범이다.
- bounded sources:

  - `comm_001692_제257조_Ⅱ_31` / `Ⅱ`: “존속상해죄에서 말하는 배우자, 직계존속은 모두 법률상의 개념이고, 사실상의 배우자나 직계존속은 포함되지 않는다.”

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
