# 공무집행방해 RuleIR 카드 검수 1

- unit: `obstruction_of_official_duty`
- articles: art136
- cards: 1–15 / 54
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art136.intent.conditional_intent`

- proposition: 공무집행방해죄에서 위 사실관계에 관한 인식이 불확정적이어도 미필적 고의가 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 불확정적 인식이 미필적 고의에 이르는지는 행위 당시의 사정에 대한 평가를 요한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.5_47` / `Ⅱ.5`: “그 인식이 불확 정적인 것이라도 이른바 미필적 고의로 인정될 수 있다.”

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

## 2. `art136.intent.officer_and_violence_awareness`

- proposition: 공무집행방해죄의 고의는 상대방이 직무를 집행하는 공무원이라는 사실 및 그에 대하여 폭행 또는 협박한다는 사실의 인식을 내용으로 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상대방의 공무원성·직무집행 사실 및 폭행·협박 사실에 관한 인식은 구체적 사실관계에 따라 평가한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.5_47` / `Ⅱ.5`: “본죄의 고의는 상대방이 직무를 집행하는 공무원이라는 사실과 그에 대하여 폭 행이나 협박을 한다는 사실을 인식하는 것을 그 내용으로 한다.”

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

## 3. `art136.intent.taxi_driver_conditional_intent`

- proposition: 택시 운전자가 약 30cm 전방에 선 의무경찰이 안전하게 피하도록 하지 않은 채 좌회전하여 충격한 사안에서는, 운전자가 충격 결과를 용인한 미필적 고의가 인정될 수 있다고 한 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 좁은 사안의 대법원 판단이다. 적용 전 원판결과 사용자의 primary precedent index를 대조해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.5_47` / `Ⅱ.5`: “그대로 좌회전을 하는 경우 그로부터 불과 30㎝ 앞에서 서 있던 의무경찰을 충격하리라는 것을 쉽게 알고도 이러한 결과발생을 용인하는 내심의 의사, 즉 미필적 고의를 인정할 수 있다고 보았다.”

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

## 4. `art136_sec1.special_offense_displacement`

- proposition: 특수한 공무집행을 보호하는 특별규정의 구성요건과 형법 제136조 제1항의 구성요건이 동시에 충족되는 경우, 특별규정이 정한 죄만 성립하고 제136조 제1항의 죄는 성립하지 않는 경우가 많다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 특별규정의 적용 범위와 제136조 제1항 배제 여부는 개별 특별법의 구성요건 및 관계에 관한 법률적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅰ_0` / `Ⅰ`: “그 규정들이 정한 죄가 성립할 뿐 형법 제136조 제1항의 죄는 성립하지 아니한다고 보아야 할 경우가 많을 것이다.”

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

## 5. `art136_sec2_1.offense_conduct`

- proposition: 공무집행방해죄는 직무를 집행하는 공무원에 대하여 폭행 또는 협박함으로써 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행 또는 협박의 존재와 상대방이 직무를 집행하는 공무원인지의 관계를 확인하는 기본 구성 설명이다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.1_2` / `Ⅱ.1`: “직무를 집행하는 공무원에 대하여 폭행 또는 협박을 함으로써 성립하는 범죄이”

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

## 6. `art136_sec2_1.violence`

- proposition: 공무집행방해죄에서 폭행은 사람에 대한 유형력의 행사로 충분하고, 반드시 신체에 대한 유형력 행사일 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 개별 행위가 사람에 대한 유형력 행사에 해당하는지는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.1_2` / `Ⅱ.1`: “여기서의 폭행은 사람에 대한 유형력의 행사로 족하고 반드시 그 신체에 대한 것임을 요하지 아”

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

## 7. `art136_sec2_2.subject.unrestricted`

- proposition: 공무집행방해죄의 주체에는 제한이 없고, 직무집행행위의 상대방뿐 아니라 직무집행과 관계없는 제3자나 방해 대상 직무집행행위를 하지 않는 다른 공무원도 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체의 범위에 관한 서술로, 직무집행행위의 상대방 여부나 공무원 여부에 따른 주체 제한을 두지 않는다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.2_3` / `Ⅱ.2`: “본죄의 주체에는 아무런 제한이 없다.”
  - `comm_001692_제136조_Ⅱ.2_3` / `Ⅱ.2`: “직무집행행위와 관계가 없는 제3자도 본죄의 주체 가 될 수 있다.”
  - `comm_001692_제136조_Ⅱ.2_3` / `Ⅱ.2`: “방해의 대상이 되는 직무집행행위를 하지 아니하는 다른 공무원도 본죄의 주체가 될 수 있다.”

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

## 8. `art136_sec2_3.concrete_authority_requirements`

- proposition: 직무집행에 필요한 법정요건 또는 명령·할당·지정·위임 등의 법적 전제를 충족하지 못하면 해당 공무원에게 구체적 직무권한이 인정되지 않고, 그 집행은 적법한 직무집행이 아니다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적 권한의 법정요건과 법적 전제 충족 여부를 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_14` / `Ⅱ.3`: “직무집행을 하기 위하여는 일정한 법정요건을 갖추는 것이 필요할 때 그 요건 을 충족하지 아니한다면 그 직무를 집행하는 공무원에게 구체적인 직무권한이 있다고 할 수 없다.”
  - `comm_001692_제136조_Ⅱ.3_14` / `Ⅱ.3`: “해당 공무원이 직무를 담당할 수 있는 법적 전제로서 명령, 할당, 지정, 위임 등 이 있어야 함에도 이러한 전제를 충족하지 못한 경우에도 그 공무원에게 구체 적인 직무권한이 있다고 할 수 없다.”

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

## 9. `art136_sec2_3.duty_execution_scope`

- proposition: 직무집행은 강제적·권력적 사무에 한정되지 않고 공공성을 가진 직무를 포함하며, 공무원이 대내외적으로 직무를 행하는 경우와 직무집행을 위하여 근무 중인 상태, 직무와 시간적·내용적으로 밀접불가분인 준비행위 및 일시적 휴식 상태도 포함될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무와 준비·근무·휴식 상태의 시간적·내용적 밀접성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_4` / `Ⅱ.3`: “강제적·권력적인 직무이든 그 밖의 직무이든 그 직무가 공공성을 갖고 있는 이상 본죄의 보호대상으로 할 필요가 있으므로, 직무집행을 강제적·권력적 성격을 띤 사무의 집행만으로 한정하여 해석할 수 없다.”
  - `comm_001692_제136조_Ⅱ.3_5` / `Ⅱ.3`: “공무원이 대내외적으 로 직무를 행하는 것이 모두 직무집행에 포함되는 것으로 해석하여야 한다.”
  - `comm_001692_제136조_Ⅱ.3_6` / `Ⅱ.3`: “직무 의 개시 전이라도 직무집행과 시간적·내용적으로 밀접불가분의 관계에 있는 준 비행위를 하고 있다면 이를 본죄의 보호대상에 포함하여야 한다.”

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

## 10. `art136_sec2_3.flagrante_arrest_requirements`

- proposition: 현행범 체포에는 행위의 가벌성, 범죄의 현행성·시간적 밀착성, 범인·범죄의 명백성 및 도망 또는 증거인멸 우려로서의 체포 필요성이 요구되고, 그 적법성은 체포 당시의 구체적 상황을 기초로 객관적으로 판단하며 사후 범인 인정에 따라 판단하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 현행범성·체포 필요성은 체포 당시의 구체적 사실에 따라 평가한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_16` / `Ⅱ.3`: “현행범인으로 체포하기 위해서는 행위의 가벌성, 범죄의 현행 성·시간적 밀착성, 범인·범죄의 명백성 이외에 체포의 필요성 즉 도망 또는 증 거인멸의 염려가 있어야 하며”
  - `comm_001692_제136조_Ⅱ.3_16` / `Ⅱ.3`: “현행범인 체포의 요건을 갖추었는지는 체포 당시의 구체적 상황을 기초로 객관 적·합리적으로 판단하여야 하며, 사후에 범인으로 인정되었는지에 따라 판단할 것은 아니어서”
  - `comm_001692_제136조_Ⅱ.3_37` / `Ⅱ.3`: “대법원은 현행범체포 의 적법성도 체포 당시의 구체적 상황을 기초로 객관적으로 판단하여야 하고 사후에 범인으로 인정되었는지에 의할 것은 아니라고 판시하였다.”

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

## 11. `art136_sec2_3.flagrante_arrest_unlawfulness`

- proposition: 체포 당시 현행범인이라고 인정할 만한 충분한 이유가 없거나 체포요건 충족에 관한 수사주체의 판단이 경험칙상 현저히 합리성을 잃은 경우 체포는 위법하며, 사후적으로 긴급구속의 실체적 요건이 갖추어져도 당시 검거행위가 적법해지는 것은 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수사주체의 재량과 합리성 상실 여부를 사실관계별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_16` / `Ⅱ.3`: “현행범인이라고 인정할만한 충분한 이유가 있었다고 보기 어려 운 경우에는 그 체포는 위법하다고 본 다음”
  - `comm_001692_제136조_Ⅱ.3_16` / `Ⅱ.3`: “체포 당시의 상황으로 보 아서도 그 요건의 충족 여부에 관한 검사나 사법경찰관 등의 판단이 경험칙에 비추어 현저히 합리성을 잃은 경우에는 그 체포는 위법하다고 보아야 한다”
  - `comm_001692_제136조_Ⅱ.3_36` / `Ⅱ.3`: “경찰관의 검거행위가 적법한 공무집행으로 인정 되려면 검거 당시 긴급구속 사유가 있어야 하는데 그 당시 이러한 사유가 없었 던 이상 사후적으로 긴급구속의 실체적 요건이 구비되었다고 하여 이러한 검거 행위가 적법하게 되는 것은 아니라고 판시하였다.”

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

## 12. `art136_sec2_3.future_duty_exception`

- proposition: 장래의 직무집행을 예상하여 폭행·협박을 가하는 행위나 장래 직무수행만 예상될 뿐 직무수행에 근접하지 않은 상태의 공무원은 공무집행방해죄의 보호대상이 아니며, 직무수행을 위하여 출근 중인 공무원도 이에 해당한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 직무수행과의 근접성 판단이 필요한 예외다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_6` / `Ⅱ.3`: “그러나 장래의 직무집 행을 예상하여 폭행·협박을 가하는 행위는 공무집행방해죄에 해당하지 아니한 다.”
  - `comm_001692_제136조_Ⅱ.3_9` / `Ⅱ.3`: “장래의 직무수행이 예상되는 상황이나 직무수행에 근접하지 아니한 상 태에 있는 공무원은 본죄의 객체가 되지 아니한다. 예를 들어 직무수행을 위 하여 출근 중인 공무원은 본죄의 객체가 될 수 없다.”

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

## 13. `art136_sec2_3.identity_check_no_id_card`

- proposition: 불심검문의 경위·현장상황·경찰관 복장·상대방의 신분확인 요구 여부 등을 종합하여 상대방이 검문자가 경찰관이고 검문 이유가 범죄행위에 관한 것임을 충분히 알았다고 보이면, 공무원증을 제시하지 않아도 불심검문은 위법하지 않다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방의 인식 여부를 객관적 정황으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_25` / `Ⅱ.3`: “불심검문을 하게 된 경위, 불심검문 당시의 현장상황과 검문을 하는 경찰관들의 복장, 피고인이 공무원증 제시나 신분 확인을 요구하였는지 여부 등을 종합적으로 고려하여”
  - `comm_001692_제136조_Ⅱ.3_34` / `Ⅱ.3`: “검문하 는 사람이 경찰관이고 검문하는 이유가 범죄행위에 관한 것임을 행위자가 충분히 알고 있었다고 보이는 경우에는 신분증을 제시하지 아니하였더라도 그 불심검문이 위법한 공무집행이라고 할 수 없다고 보았다.”

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

## 14. `art136_sec2_3.internal_assignment_and_superior_direction`

- proposition: 직무집행의 편의를 위한 내부적 사무분담 범위를 벗어나거나 상급 공무원의 지휘명령에 따라 사무를 수행한다는 사정만으로 그 사무가 공무원의 추상적·일반적 권한 범위 밖이라고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 내부 사무분담과 상급 지휘의 구체적 법적 효과를 검토해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_11` / `Ⅱ.3`: “직무집행의 편의에 따라 마련된 내부적인 사무분담의 범위를 벗어난다고 하여 공무원의 추상적·일반적인 권한 내에 속하지 아니한다고 볼 것은 아니다.”
  - `comm_001692_제136조_Ⅱ.3_11` / `Ⅱ.3`: “상급 공무원의 지휘명령에 따라 사무를 수행한다는 이유만으로 그 사무 가 공무원의 추상적·일반적인 권한 내에 속하지 아니한다고 볼 수는 없는 것이다.”

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

## 15. `art136_sec2_3.lawful_performance_prerequisite`

- proposition: 공무집행방해죄의 성립에는 공무원의 적법한 공무집행이 전제되어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 적법한 직무집행의 전제요건을 나타내는 병합 카드다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_10` / `Ⅱ.3`: “본죄는 공무원의 적법한 공무집행을 전제로 하고”
  - `comm_001692_제136조_Ⅱ.3_9` / `Ⅱ.3`: “대법원도 본죄는 공무원의 직무집행이 적법한 경우에 한하여 성립한다고 판시 함으로써 직무집행의 적법성이 요구된다는 점을 분명히 하였다.”

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
