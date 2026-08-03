# 주거침입·퇴거불응 RuleIR 카드 검수 6

- unit: `dwelling_intrusion`
- articles: art319
- cards: 76–90 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 76. `art319_sec5_3.justification.emergency_escape`

- proposition: 맹견의 추격이나 강도를 피하여 타인의 가옥에 몸을 피한 경우 긴급피난에 해당하여 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 추격 또는 강도 위험, 피난의 필요성 및 긴급피난 성립 여부를 구체적 사실에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.3_50` / `Ⅴ.3`: “맹견의 추격이나 강도를 피하여 타인의 가옥에 몸을 피한 경우에는, 긴급피난에 해당하여 위법성이 조각된다.”

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

## 77. `art319_sec5_3.justification.fire_suppression`

- proposition: 화재 초기 진화를 위하여 담을 넘어 이웃집에 들어가거나 다른 이웃집 지붕 위로 올라가 물을 뿌린 경우 긴급피난 또는 피해자의 추정적 승낙으로 위법성이 조각될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 화재 진화의 긴급성, 침입 또는 출입 수단의 상당성, 긴급피난 또는 추정적 승낙의 성립 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.3_50` / `Ⅴ.3`: “외출 중인 이웃집에 화재가 발생한 경우 그 불 을 초기에 진화하기 위해 담을 타 넘어 그 집에 들어간 경우 또는 이웃집에 불이 나자 불을 끄기 위해 다른 이웃집의 슬라브지붕 위로 올라가 물을 뿌린 경우에 는 긴급피난 또는 피해자의 추정적 승낙에 의해 위법성이 조각될 수 있다.”

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

## 78. `art319_sec5_3.justification.general`

- proposition: 주거침입행위가 정당방위·긴급피난·자구행위 등에 해당하면 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 정당방위·긴급피난·자구행위 해당 여부와 위법성 조각 요건의 충족은 사실관계에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.3_50` / `Ⅴ.3`: “주거침입행위가 정당방위, 긴급피난, 자구행위 등에 해당하면 위법성이 조각된다.”

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

## 79. `art319_sec5_3.rightless_possessor.peace`

- proposition: 점유권원이 없는 자의 점유라도 주거의 평온은 보호되므로, 권리자가 권리실행을 위한 자력구제 수단으로 건조물에 침입하면 건조물침입죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 판례 입장이므로, 건조물침입죄 성립 범위와 원판결의 사실관계·판시를 사용자 제공 1차 판례 색인에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.3_50` / `Ⅴ.3`: “점유할 권리 없는 자의 점유 라 하여도 그 주거의 평온은 보호되므로 권리자가 그 권리실행으로서 자력구제의 수 단으로 건조물에 침입하였다면 건조물침입죄가 성립한다.”

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

## 80. `art319_sec5_3.self_help.right_holder_negative`

- proposition: 사법상 권리자라 하더라도 주거침입죄와 관련하여 자구행위를 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사법상 권리 보유만으로 주거침입 관련 자구행위의 위법성 조각을 인정하지 않는다는 제한이다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.3_50` / `Ⅴ.3`: “사법상의 권리자라 할지라도 주거침입죄와 관련하여 자구행위를 할 수 없다.”

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

## 81. `art319_sec6_1.continuing_offense`

- proposition: 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 계속범이라는 성격 및 평온 침해 지속 기간에 관한 설명을 별도 검토 단위로 유지한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.1_51` / `Ⅵ.1`: “주거침입죄는 계속범이므로 사실상 주거의 평온에 대한 침해가 계속되는 동 안 주거침입죄가 계속하여 성립한다.”

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

## 82. `art319_sec6_1.no_separate_refusal_after_completed_intrusion`

- proposition: 주거침입죄 기수 후 퇴거요구에 불응하더라도 별도로 퇴거불응죄는 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 주거침입죄 기수 후의 퇴거불응에 한정된 별도 퇴거불응죄 성립 배제 설명이다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.1_51` / `Ⅵ.1`: “따라서 주거침입죄의 기수 이후에 퇴거요 구에 불응한 경우에도 별도로 퇴거불응죄가 성립하지 않는다.”

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

## 83. `art319_sec6_1.post_final_conviction_continuance_separate_offense`

- proposition: 무단침입으로 유죄판결이 확정된 뒤에도 퇴거하지 않고 계속 거주하면, 판결확정 이후의 침입행위 및 위법상태 계속으로 별도의 주거침입죄가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 판결 확정, 퇴거 여부, 계속 거주 및 확정 후 위법상태의 관계를 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.1_51` / `Ⅵ.1`: “그 판결이 확정된 후에도 퇴거하지 않은 채 계속하여 그 주택에 거주한 경우 에는, 판결 확정 이후의 주거침입행위 및 그로 인한 위법상태가 계속되고 있기 때문에 별도의 주거침입죄가 된다.”

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

## 84. `art319_sec6_1.repeat_entry_inclusive_crime`

- proposition: 주거침입 후 잠시 나왔다가 다시 들어간 경우 포괄일죄가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 재출입의 시간적·사실적 연속성 판단이 필요하므로 포괄일죄 적용은 사실평가 입력으로 유지한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.1_51` / `Ⅵ.1`: “주거침입죄는 계속범이므로 주거침입 후 잠시 나왔다가 다시 들어간 경우 포괄일죄가 된다.”

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

## 85. `art319_sec6_2.combined_offense_absorption`

- proposition: 주거침입을 목적범죄와 결합한 독립범죄로 규정하는 경우 주거침입은 결합범에 흡수되어 별도 주거침입죄가 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 독립한 결합범으로 규정된 범죄인지 여부를 확인한 경우에만 적용하는 흡수 예외다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.2_52` / `Ⅵ.2`: “주거침입죄를 그 목적범죄와 결합시켜 하나의 독립한 범죄로 규정하는 경우에 는, 주거침입이 가중적 구성요건 요소로서 당해 결합범에 흡수되어 독자적인 의 미를 갖지 않으므로 별도로 주거침입죄가 성립하지 않는다.”

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

## 86. `art319_sec6_2.daytime_entry_no_night_intrusion_theft`

- proposition: 주거침입이 주간에 이루어진 경우 야간주거침입절도죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 침입 시각의 인정과 야간주거침입절도죄의 시간적 요건 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.2_52` / `Ⅵ.2`: “주거침입이 주간에 이루어진 경우에는 야간주거침입절도죄가 성립하지 않는다고 해석하는 것이 타당하다고 하였다.”

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

## 87. `art319_sec6_2.instrumental_intrusion_real_concurrence`

- proposition: 주거침입이 다른 범죄의 수단으로 이루어진 경우 수단인 주거침입죄와 목적범죄는 원칙적으로 실체적 경합관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주거침입이 목적범죄의 수단인지와 결합범 규정이 있는지는 개별 범죄구성 및 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.2_52` / `Ⅵ.2`: “수단이 되는 주거침입죄와 목적이 되는 주된 범죄 는 원칙적으로 실체적 경합관계에 서게 된다.”

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

## 88. `art319_sec6_2.night_intrusion_theft_attempt_on_entry`

- proposition: 야간에 타인의 재물을 절취할 목적으로 사람의 주거에 침입하면, 침입 단계에서 이미 야간주거침입절도 범죄행위의 실행에 착수한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 야간성, 타인 재물 절취 목적 및 주거침입의 사실적 인정이 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.2_53` / `Ⅵ.2`: “야간에 타인의 재물을 절취할 목적으로 사람의 주거에 침입한 경우에는 주거에 침입한 단계에 서 이미 야간주거침입절도 범죄행위의 실행에 착수한 것으로 보아야 한다.”

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

## 89. `art319_sec6_2.special_theft_entry_absorption`

- proposition: 야간에 주거 일부를 손괴하고 침입한 뒤 절취한 경우 특수절도죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 야간성, 주거 일부 손괴, 침입 및 절취의 충족 여부와 별도 주거침입죄 배제 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅵ.2_53` / `Ⅵ.2`: “야간에 주거의 일부를 손괴하고 침입한 후 절취한 경우에는 특수절도죄만 성립 한다.”

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

## 90. `art319_sec7_1.refusal_to_leave_elements`

- proposition: 퇴거불응죄는 사람의 주거, 관리하는 건조물, 선박, 항공기 또는 점유하는 방실에서 퇴거요구를 받고 이에 응하지 않음으로써 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 퇴거요구와 이에 대한 불응이라는 기본 성립 구조를 기록한다. 퇴거요구의 명시성 및 체류 목적·기간에 따른 적용 범위는 현재 후보의 정확한 인용 범위를 넘어 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.1_56` / `Ⅶ.1`: “퇴거불응죄는 사람의 주거, 관리하는 건조물, 선박, 항공기 또는 점유하는 방실 에서 퇴거요구를 받고 응하지 아니함으로써 성립하는 범죄이다.”

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
