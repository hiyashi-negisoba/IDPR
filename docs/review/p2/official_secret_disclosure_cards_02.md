# 공무상비밀누설 RuleIR 카드 검수 2

- unit: `official_secret_disclosure`
- articles: art127
- cards: 16–27 / 27
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art127_sec3_4.secret_not_obtained_in_course_of_duties`

- proposition: 누설정보를 직무집행상 지득하지 않고 직무와 무관하게 우연히 알게 된 경우에는 피고인의 직무상 비밀로 볼 수 없다고 본 사안이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 정보 취득 경위와 직무집행 사이의 관련성을 사실관계에 따라 검토해야 하는 소개된 사안이다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_14` / `Ⅲ.4`: “피고인의 직무상 비밀이라 볼 수 없다고 판단한 원심을 유지한 사안.”

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

## 17. `art127_sec3_4.traffic_records_insufficient_secrecy`

- proposition: 교통사고 수사기록이 피의사실·당사자 인적사항·상해 정도·신병처리 지휘내용에 그치고 수사목적 방해나 개인정보 침해 우려가 있다고 보기 부족한 경우 직무상 비밀에 해당하지 않는다는 하급심 판단을 유지한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수사보안·수사목적 방해 및 개인정보 침해 우려의 유무는 기록 내용과 공개 상황에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_11` / `Ⅲ.4`: “그 내용이 공개되는 경우 수사의 보안 또는 기밀을 침해하여 수사의 목적을 방해할 우려가 있거나 개인의 사생활 등 이해관계를 침해할 우려가 있는 개인정보를 담고 있는 것으 로 보기에는 부족하다고 보아 직무상 비밀에 해당하지 아니한다고 본 하급심을 유지한 사안.”

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

## 18. `art127_sec3_4.vehicle_owner_information_not_official_secret`

- proposition: 자동차 소유자 정보는 공개되지 않은 측면이 있더라도 재산 소유 주체 정보에 불과하여 실질적 비밀보호 가치나 국가기능 위협이 인정되지 않으므로, 잠복수사 차량의 소유관계 정보도 제127조의 법령에 의한 직무상 비밀에 해당하지 않는다고 본 사안이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 비공개 측면만으로는 충분하지 않다는 소개된 사안으로서, 정보의 실질적 보호가치와 국가기능 관련 위험을 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_14` / `Ⅲ.4`: “피고인이 제공한 차량 소유관계에 관한 정보가 형법 제127조에서 정한 ‘법령에 의한 직무 상 비밀’에 해당한다고 볼 수 없다”

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

## 19. `art127_sec4.disclosure.interofficial_transmission`

- proposition: 국가기능에 위험이 발생하리라고 볼 만한 특별한 사정이 인정되지 않는 한, 해당 설명에서 전제된 행위는 비밀의 누설에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 제공된 인용문은 ‘위와 같은 행위’의 선행 사실을 포함하지 않으므로, 적용 대상 행위와 특별한 사정의 판단 기준을 원문 맥락에서 검토해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅳ_15` / `Ⅳ`: “국가기능에 위험이 발생 하리라고 볼 만한 특별한 사정이 인정되지 않는 한, 위와 같은 행위가 비밀의 누설에 해당한다고 볼 수 없다.”

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

## 20. `art127_sec4.disclosure.known_recipient`

- proposition: 이미 비밀을 알고 있는 사람에게 비밀을 알리는 것은 누설에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 누설 불성립 설명과 불능미수로 보는 견해의 관계는 현재 자료만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제127조_Ⅳ_15` / `Ⅳ`: “이미 비밀을 알고 있는 사람에게 비밀을 알리는 것은 누설에 해당 하지 아니한다.”

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

## 21. `art127_sec4.disclosure.omission`

- proposition: 비밀을 모르는 제3자가 비밀 기재 서류를 열람하는 것을 묵인하는 행위는 부작위에 의한 누설에 해당한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제3자의 서류 열람을 묵인한 부작위도 누설의 방식으로 명시된다.
- bounded sources:

  - `comm_001692_제127조_Ⅳ_15` / `Ⅳ`: “비밀을 알지 못하는 제3자가 비밀이 기 재된 서류를 열람하는 것을 묵인하는 행위는 부작위에 의한 누설에 해당한다.”

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

## 22. `art127_sec4.disclosure.specificity`

- proposition: 누설은 어느 관청에 속한 비밀인지 알 수 있을 정도로 구체적으로 고지되어야 하며, 막연한 고지는 누설이 아니다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 고지 내용의 구체성 부족은 누설 해당성을 부정하는 명시적 한계다.
- bounded sources:

  - `comm_001692_제127조_Ⅳ_15` / `Ⅳ`: “어느 관청에 속한 비밀인지 알려질 수 있을 정도로 구체적인 고지여야 하고 막연한 고지는 누설이 아니다.”

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

## 23. `art127_sec4.disclosure.unaware_third_party`

- proposition: 누설은 비밀을 아직 알지 못하는 제3자에게 임의로 알려주는 행위이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 누설의 상대방이 아직 비밀을 알지 못하는 제3자인지를 확인하는 정의 카드다.
- bounded sources:

  - `comm_001692_제127조_Ⅳ_15` / `Ⅳ`: “누설이란 비밀을 아직 이를 모르는 제3자에게 임의로 알려주는 행위를 의미한 다.”

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

## 24. `art127_sec6.statutorily_required_corruption_report`

- proposition: 법령에 의한 직무상 비밀이 다른 공직자의 부패행위에 관한 것이어서 수사기관 등에 신고하는 과정에서 누설된 경우에는 법령에 의한 정당행위로 위법성이 조각된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법령상 신고 과정에서의 누설에 한정된 정당행위 예외로 검토한다.
- bounded sources:

  - `comm_001692_제127조_Ⅵ_18` / `Ⅵ`: “이를 수사기관 등에 신고하는 과정에서 직무상 비밀이 누설되더라도 법령에 의한 정당행위로서 위법성이 조각된다.”

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

## 25. `art127_sec7.bribery_disclosure_imaginary_concurrence`

- proposition: 공무원이 뇌물을 수수하고 그 대가로 비밀을 누설한 경우에는 본죄와 수뢰후부정처사죄가 상상적 경합이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 뇌물 수수의 대가로 비밀을 누설한 경우에 한정된 죄수 관계 설명이다.
- bounded sources:

  - `comm_001692_제127조_Ⅶ_19` / `Ⅶ`: “공무원이 뇌물을 수수하고 그 대가로 비밀을 누설한 경우에는 본죄와 수뢰후부 정처사죄의 상상적 경합이 된다.”

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

## 26. `art127_sec7.special_law_priority`

- proposition: 특별법에서 직무상 비밀 누설을 처벌하는 경우에는 법조경합으로 본죄가 성립하지 않고 특별법이 우선 적용된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 특별법상 직무상 비밀 누설 처벌규정이 적용되는 경우에 한정된 법조경합 설명이다.
- bounded sources:

  - `comm_001692_제127조_Ⅶ_19` / `Ⅶ`: “특별법에서 직무상 비밀의 누설을 처벌하는 경우에는 법조경합으로 본죄가 성립하지 아니하고 특별법이 우선 적용된다고 보아야 한다.”

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

## 27. `art127_sec7.special_offense_absorption`

- proposition: 공무원의 비밀누설이 간첩죄·외교상비밀누설죄 등 특별규정에 해당하는 경우 본죄는 흡수되어 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 간첩죄·외교상비밀누설죄 등 특별규정에 해당하는 비밀누설에 관한 흡수 관계 설명이다.
- bounded sources:

  - `comm_001692_제127조_Ⅶ_19` / `Ⅶ`: “공무원의 비밀누설이 간첩죄, 외교상비밀누설죄 등 특 (형법 제98조)(제113조 제1항) 별규정에 해당하는 경우에는 본죄는 이에 흡수되어 별도로 성립하지 아니한 다.”

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
