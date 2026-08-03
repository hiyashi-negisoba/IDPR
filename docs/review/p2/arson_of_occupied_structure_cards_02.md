# 현주건조물등방화 RuleIR 카드 검수 2

- unit: `arson_of_occupied_structure`
- articles: art164
- cards: 16–30 / 52
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

## 16. `art164_sec2_1.integrated_building_residential_or_presence_character`

- proposition: 건물 일부가 주거로 사용되거나 일체를 이루는 건조물 일부에 사람이 현존하면, 전체 건조물에 주거성 또는 현존건조물성이 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 건물 부분들의 일체성 및 주거·현존 상태를 평가해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “관공서, 학교, 공장, 점포는 사람이 주거로 사용하는 것이”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “라고 말할 수 없으나 그 건물 일부에 사람의 주거로 사용되는 숙직실이 설치되”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “어 있는 경우에는 그 건물 전체에 대하여 주거성이 인정된다.”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “일체를 이루는 건조물 등 일부에 사람이 현존한다면 건조물 전체가 사람이 현존하는 건조물이 된다.”

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

## 17. `art164_sec2_1.medium_ignition_attempt`

- proposition: 행위로 매개물에 불이 붙어 연소작용이 계속될 수 있는 상태가 되었다면, 곧바로 진화되어 건조물 자체에 불이 옮겨 붙지 않았더라도 방화죄의 실행 착수가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 매개물의 연소 지속 가능 상태를 평가해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “범인의 행위로 인하여 매개물에 불이 붙게 됨으로써 연소작용이 계속될 수 있는 상태에 이르렀다면 그것이 곧바로 진화되는 등의 사정으로 인하여 목 적물인 건조물 자체에 불이 옮겨 붙지 못하였다고 하더라도 방화죄의 실행의 착수가 인정된다.”

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

## 18. `art164_sec2_1.no_attempt_before_ignition`

- proposition: 방화 목적물 또는 그 도화물체에 아직 점화하지 않은 때에는 방화 실행의 착수가 아니라 예비로 처벌될 수 있을 뿐이다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 점화 전 행위는 실행 착수와 구별하여 보존한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_9` / `Ⅱ.1`: “아직 방화의 목적물 내지 그 도화물체에 점화하지 않은 때에는 불을 놓는 것에 해당하지 않 고, 이때에는 본죄의 예비로 처벌될 수 있을 뿐이다.”

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

## 19. `art164_sec2_1.omission_arson`

- proposition: 소화하기 쉬운 기존 화력을 방치하여 목적물 연소를 야기하는 부작위에 의한 방화도 가능하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 소화 가능성, 방치 및 연소 결과의 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_6` / `Ⅱ.1`: “용이하게 소화할 수 있는 기발 화력을 방치하여 목적물의 연소를 야기하는 부작위에 의한 방화도 가능하다.”

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

## 20. `art164_sec2_1.person_excludes_offender_and_accomplice`

- proposition: 현주건조물등방화죄에서 사람은 범인 및 공범을 제외한 자연인을 뜻한다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 범인 범주에는 공범이 포함된다는 한정이 명시되어 있다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “‘사람’이란 범인 이외의 모든 자연인을 말한다. 범인에는 공범이 포함된다.”

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

## 21. `art164_sec2_1.present_person`

- proposition: 사람이 현존한다는 것은 방화 당시 범인 외의 자가 건조물 등 내부에 사실상 존재하는 것을 말하며, 존재 권원이나 이유는 묻지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 방화 당시 내부의 사실상 존재 여부를 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “‘사람이 현존하는’이란 범인이 방화할 당시, 범인 이외의 자가 건조물 등 내부에 있는 것을 말한다. 사실상 존재하면 족하고 존재할 권리 유무, 현존하는 이유를 묻지 않는다.”

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

## 22. `art164_sec2_1.protected_object`

- proposition: 현주건조물등방화죄의 객체는 사람이 주거로 사용하거나 사람이 현존하는 건조물, 기차, 전차, 자동차, 선박, 항공기 또는 지하채굴시설이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 객체 범위와 주거 또는 현존 요건을 구분하여 검토한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “본죄의 객체는 사람이 주거로 사용하거나 사람이 현존하는 건조물, 기차, 전차, 자동차, 선박, 항공기 또는 지하채굴시설이다.”

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

## 23. `art164_sec2_1.residence_daily_life_place`

- proposition: 사람이 주거로 사용한다는 것은 범인 외의 사람이 일상생활의 장소로 사용하는 것을 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일상생활 장소인지에 관한 사실 평가가 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “‘사람이 주거로 사용’한다는 것은 범인 이외의 사람이 일상생활의 장소로 사용하”
  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “는 것을 말한다.”

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

## 24. `art164_sec2_1.residence_factual_use`

- proposition: 주거 사용은 사실적으로 판단하므로, 주거 사용을 포기한 폐가나 영업 중단 후 잠가 둔 호텔은 주거용 건조물이 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사용 포기 및 영업 중단 상태를 사실적으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “‘사용한다’는 것은 사실적 의미로 해석하여야 한다. 따라서 주인이 주거로 사용”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “할 것을 포기한 농촌의 폐가나 영업을 중단하고 문을 잠가 둔 호텔은 주거로 사”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “용하는 건조물이라고 할 수 없다.”

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

## 25. `art164_sec2_1.residence_nonrequired_indicia`

- proposition: 주거성 판단에서 지속적 현존, 주거 목적 건축, 동일인의 계속 거주 또는 주민등록은 필수 요건이 아니며, 일상생활 장소인지가 기준이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정은 주거성의 필요조건이 아니라는 점을 반영한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “밤낮으로 끊임없이 사람이 현존할 것을 요하지 않고, 주택으로 사용하는 것을 주된 목적으로 하거나 주거로 사용하기 위하여 건조된 것일 필”
  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “요가 없다. 항상 동일인이 거주할 것을 요하지 않는다. 주민등록이 되어 있을 것”
  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “을 요하지 않고”

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

## 26. `art164_sec2_1.residence_temporary_or_seasonal_use`

- proposition: 장기여행 중인 가옥, 사용 가능한 상태로 유지된 별장·전원주택, 일시 취침용 객실이나 산장·콘도미니엄도 주거로 사용하는 장소가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 실제 사용 가능 상태와 사용 양태를 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “전 가족이 장기여행으로 부재중인 가”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “옥, 주말이나 일정한 계절에만 사용하는 별장, 전원주택일지라도 가재도구를 곧 사용할 수 있는 상태로 유지하고 있다면 사람이 주거로 사용하는 건조물이라고 할 수 있다.”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “일시 취침에 사용하는 술집의 객실, 일시 머물다 가는 산장, 콘도미니엄 등도 주거로 사용하”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “는 장소로 볼 수 있다.”

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

## 27. `art164_sec2_1.residence_without_actual_presence`

- proposition: 주거로 사용되는 건조물은 방화 당시 사람이 실제 현존할 필요가 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주거 사용과 실제 현존은 대체적 객체 요건으로 구분된다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “사람이 주거로 사용하는 건조물인 경우에는 방화 당시 사람이 현존할 필요는 없다.”

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

## 28. `art164_sec2_1.sole_offender_home_general_building`

- proposition: 범인이 혼자 사는 집에 방화한 경우에는 현주건조물등방화죄가 아니라 일반건조물방화죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위자가 유일한 거주자인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “범인이 혼자 살고 있는 집”
  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “에 방화한 때는 본죄에 해당하지 않고 일반건조물방화죄가 성립한다.”

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

## 29. `art164_sec2_1.temporal_residence_or_presence`

- proposition: 객체는 행위 당시 사람이 주거로 사용하거나 사람이 현존하는 것이어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위 당시의 주거 사용 또는 현존 사실을 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_2` / `Ⅱ.1`: “본죄의 객체가 되는 건조물 등은 행위 당시 사람이 주거로 사용하거나 사람이 현존하는 것이어야 한다.”

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

## 30. `art164_sec2_2.mental_weakness_serial_arson_case`

- proposition: 정신분열증세 및 억제하기 어려운 방화 충동으로 사물변별 또는 의사결정 능력이 미약한 상태에서 6일간 8차례 연속 방화를 한 경우, 심신미약을 인정하여 형법 제10조 제2항을 적용한 조치는 정당하다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 사실관계에 한정된 심신미약 판단례이며, 판례 원문 및 구체적 사실관계 확인이 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.2_13` / `Ⅱ.2`: “피고인을 심신미약자로 인정하고 형법 제10 조 제2항을 적용하여 처단한 조치는 정당하다.”

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
