# 현주건조물등방화 RuleIR 카드 검수 1

- unit: `arson_of_occupied_structure`
- articles: art164
- cards: 1–15 / 47
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

## 1. `art164.arson_property_damage_absorption`

- proposition: 방화행위로 건조물 등을 손괴한 경우, 그 손괴는 방화의 불가벌적 수반행위로서 법조경합 관계에 따라 방화죄에 흡수된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 방화행위에 수반된 건조물 등 손괴에 한정된 흡수 관계로 검토한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.4_16` / `Ⅱ.4`: “방화행위로 건조물 등을 손괴한 경우 손괴는 방화의 불가벌적 수반행위로서 법 조경합관계가 되므로 방화죄에 흡수된다.”

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

## 2. `art164.fire_insurance_claim_concurrence`

- proposition: 화재보험금 편취를 목적으로 방화한 후 보험금을 청구한 경우, 보험사기방지특별법위반죄와 방화죄는 실체적 경합 관계에 있으며, 보험금을 받았으면 보험사기는 기수이고 받지 못하였으면 미수이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 보험금 청구 여부, 실제 수령 여부 및 방화 목적의 사실인정이 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.4_16` / `Ⅱ.4`: “화재보험금 편취를 목적으로 방화한 경우, 보험금 청구를 하였다면 보험사기방지 특별법위반죄와 방화죄의 실체적 경 (보험금을 받았으면 기수, 받지 못하였으면 미수) 합관계에 있고”

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

## 3. `art164.pre_claim_insurance_fraud_no_attempt`

- proposition: 화재보험금 편취 목적의 방화라도 보험금 청구 전에는 보험사기방지특별법위반죄의 실행 착수를 인정하기 어려워 방화죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 보험금 청구 전 행위가 보험사기방지특별법위반죄의 실행 착수에 해당하는지에 관한 적용은 별도 검토한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.4_16` / `Ⅱ.4`: “보험금 청구를 하기 전이라면 보험사기방지특별법위반죄의 실행 의 착수를 인정하기 어려우므로 방화죄만 성립한다.”

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

## 4. `art164_sec2_1.accomplices_residence_general_building`

- proposition: 공범이 각자 또는 함께 거주하는 건조물에 방화한 경우에는 현주건조물등방화죄가 아니라 일반건조물방화죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 공범 관계와 실제 거주 관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “공범이 각자 자신이 살고 있는 건조물에 방화한 때, 공범이 함께 살고 있는 건조물에 방화한 때에는 일반건조물방화죄에 해당한다.”

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

## 5. `art164_sec2_1.arson_act`

- proposition: 방화의 실행행위는 불을 놓아 목적물을 불태우는 것이며, 불을 놓는 것은 화력으로 객체 연소를 야기하거나 불태움에 원인력을 부여하는 행위이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 화력과 목적물 연소 사이의 원인력 부여를 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_6` / `Ⅱ.1`: “방화죄의 실행행위는 ‘불을 놓아 목적물을 불태우는 것’이다. ‘불을 놓아’라는 것은 화력을 이용하여 객체의 연소를 야기하는 행위 또는 목적”
  - `comm_001692_제164조_Ⅱ.1_6` / `Ⅱ.1`: “물의 불태움에 원인력을 부여하는 행위를 말한다.”

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

## 6. `art164_sec2_1.attempt_commencement_ignition`

- proposition: 방화죄의 실행 착수는 직접 목적물에 점화하거나 매개물을 이용하여 목적물에 도화시킬 때 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 직접 점화 또는 매개물 도화 여부를 개별 사실관계에서 판단해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “직접 목적물에 점화하거나 매개물을 이용하 여 목적물에 도화시킬 때 실행의 착수가 있다고 볼 것이다.”

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

## 7. `art164_sec2_1.building`

- proposition: 방화죄의 건조물은 토지에 정착되고 벽 또는 기둥과 지붕 또는 천장으로 구성되어 사람이 내부에 기거하거나 출입할 수 있는 공작물이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 구조 및 기거·출입 가능성에 관한 사실 판단이 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_4` / `Ⅱ.1`: “형법상 방화죄의 객체인 건조물은 토지에 정착되고 벽 또는 기둥과 지붕 또는 천장”
  - `comm_001692_제164조_Ⅱ.1_4` / `Ⅱ.1`: “으로 구성되어 사람이 내부에 기거하거나 출입할 수 있는 공작물을 말하고”

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

## 8. `art164_sec2_1.building_integrity`

- proposition: 외관상 복수 건물이라도 근접하고 복도로 연결된 경우에는 물리적·기능적 관점을 통합하여 하나의 건조물인지 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 근접성·연결성 및 기능적 일체성을 함께 평가해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_5` / `Ⅱ.1`: “외관상 복수의 건물로 보이는 경우에도 그것이 근접하고 또 복도 등으로 접속”
  - `comm_001692_제164조_Ⅱ.1_5` / `Ⅱ.1`: “되어 있는 경우에는 전체를 일체의 것으로서 1개의 건조물로 볼 수 있는 경우가 있다. 이 경우 일체성의 판단 기준으로서 물리적 관점과 기능적 관점을 통합하”
  - `comm_001692_제164조_Ⅱ.1_5` / `Ⅱ.1`: “여 판단하여야 할 것이다.”

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

## 9. `art164_sec2_1.burning_result`

- proposition: 불태움은 화력에 의한 건조물 등의 훼손 또는 손괴를 뜻하며, 불태움 결과가 발생하면 방화죄는 기수에 이른다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 기수 판단에 관한 아래 경쟁 견해 및 보고된 판례와 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_7` / `Ⅱ.1`: “‘불태움’이란 일반적으로 화력에 의한 건조물 등의 훼손 내지 손괴를 의미한다.”
  - `comm_001692_제164조_Ⅱ.1_7` / `Ⅱ.1`: “불태움의 결과가 발생함으로써 본죄는 기수가 된다.”

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

## 10. `art164_sec2_1.combustion_without_flame`

- proposition: 독립연소에서 연소는 반드시 불꽃을 수반할 필요가 없고, 불에 타지 않는 재질도 고온 산화로 열이 주변 발화점에 전달되어 가연 부분 전체에 순차 번지는 상태이면 독립연소 상태가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 열 전달과 순차적 확산 상태에 관한 전문적 사실 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “연소라고 하여도 반드시 불꽃을 수반하는 것에 한하지 않고 가연 부분 이 불에 타지 않는 재질이라도 고온에 산화되어 주변 발화점까지 열이 전해져 가연 부분 전체에 순차 번지는 상태에 있으면 독립연소의 상태라 할 수 있다.”

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

## 11. `art164_sec2_1.derelict_building_not_building_precedent`

- proposition: 지붕·문짝·창문이 없고 담장 및 일부 벽체가 붕괴되어 기거·취침에 사용할 수 없는 철거 대상 폐가는 제164조의 건조물이 아니라 물건에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- prior note: 보고된 판례의 원문 및 적용 대상 조문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_4` / `Ⅱ.1`: “지붕과 문짝, 창문이 없고 담장과 일부 벽체가 붕괴된 철거 대상 건물로서 사실”
  - `comm_001692_제164조_Ⅱ.1_4` / `Ⅱ.1`: “상 기거·취침에 사용할 수 없는 상태의 폐가는 형법 제164조의 건조물이 아닌 제167조의 물건에 해당한다.”

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

## 12. `art164_sec2_1.entry_for_arson_not_attempt`

- proposition: 방화 목적으로 타인의 주거에 침입한 것만으로는 방화 실행에 착수한 것으로 볼 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- prior note: 침입만으로는 점화 또는 도화에 이르지 않은 경우를 분리한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “방화의 목적으로 타인의 주거에 침입한 것만으로는 방화의 실행에 착수했다고 볼 수 없다.”

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

## 13. `art164_sec2_1.extinguished_medium_attempt`

- proposition: 방화 목적으로 매개물에 점화하여 연소작용을 계속할 수 있는 상태가 된 뒤 진화되어 주택에 불이 옮겨 붙지 않은 경우에도 방화의 착수가 인정되어 방화미수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- prior note: 방화 목적, 매개물 점화 및 연소 지속 가능 상태를 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “방화의 목적으로 매개물에 점화하여 그 연소 작용을 계속할 수 있 는 상태에 놓인 경우에도 방화죄의 실행의 착수가 인정되고, 이것이 그대로 진 화되어 목적물인 주택에 옮겨 붙지 않고 끝난 경우에도 방화의 착수가 인정되 므로 방화미수죄가 성립한다.”

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

## 14. `art164_sec2_1.independent_combustion_ceiling_case`

- proposition: 피해자 사체 위의 옷가지 등에 불을 붙여 방 안과 천정으로 불길이 옮겨 붙은 경우, 이후 진화되었더라도 천정에 옮겨 붙은 때 현주건조물방화죄의 기수가 된다는 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- prior note: 소개된 사례의 사실관계 및 1차 판례 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_8` / `Ⅱ.1`: “도중에 진화되었 다고 하더라도 일단 천정에 옮겨 붙은 때에 이미 현주건조물방화죄의 기수에 이른 것이 라고 한 사례”

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

## 15. `art164_sec2_1.independent_combustion_completion_precedent`

- proposition: 현주건조물방화죄는 화력이 매개물을 떠나 건조물 스스로 연소할 수 있는 상태에 이르면 기수에 이른다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- prior note: 보고된 판례 입장으로 보존하며 원문 확인 후 경쟁 학설과의 정책 선택이 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_8` / `Ⅱ.1`: “현주건조물방화죄는 화력이 매개물을 떠나 목적물인 건조물 스스로 연소할 수 있는 상태에 이름으로써 기수가 된다”

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
