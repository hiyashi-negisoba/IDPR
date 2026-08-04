# 공무집행방해 RuleIR 카드 검수 2

- unit: `obstruction_of_official_duty`
- articles: art136
- cards: 16–30 / 54
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art136_sec2_3.lawful_performance_requirements`

- proposition: 보호대상이 되는 적법한 직무집행이 되려면 해당 행위가 공무원의 추상적·일반적 권한 및 구체적 직무권한 내에 속하고, 직무행위의 유효요건으로 법정된 중요한 방식과 절차를 준수해야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 적법한 직무집행의 권한·절차 요건을 정리한 카드다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_10` / `Ⅱ.3`: “ⅰ) 첫 번째 당해 행위가 본죄의 객체가 되는 공무원의 추상적·일반적인 권한 내에 속 할 것, ⅱ) 두 번째 당해 행위가 본죄의 객체가 되는 공무원의 구체적인 직무권 한 내에 속할 것, ⅲ) 세 번째 당해 행위가 직무행위의 유효요건으로 법정되어 있는 중요한 방식과 절차를 준수하였을 것”
  - `comm_001692_제136조_Ⅱ.3_28` / `Ⅱ.3`: “공무원의 직무행위의 형식적인 적법요건으로 법령상의 일정한 방식과 절차를 따를 것을 요구하는 경우 이러한 방식과 절차를 반드시 준수하여야 한다.”

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

## 17. `art136_sec2_3.lawfulness_time_of_act`

- proposition: 공무집행 적법성은 행위 당시의 구체적 상황을 기초로 객관적·합리적으로 판단하며, 사후의 순수한 객관적 기준만으로 판단하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 행위 당시의 상황 평가가 필요한 reported precedent 기준이다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_10` / `Ⅱ.3`: “공무원의 공무집행 이 적법한지는 행위 당시의 구체적 상황에 기초하여 객관적·합리적으로 판단하 여야”
  - `comm_001692_제136조_Ⅱ.3_36` / `Ⅱ.3`: “공무집행방해죄는 공무원의 적법한 공무집행이 전제로 되는데, 추상적 인 권한에 속하는 공무원의 어떠한 공무집행이 적법한지는 행위 당시의 구체적 상황에 기하여 객관적·합리적으로 판단하여야 하고 사후적으로 순수한 객관적 인 기준에서 판단할 것은 아니라고 판시하였다.”

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

## 18. `art136_sec2_3.minor_procedural_violation`

- proposition: 행정법상 사소한 절차규정 위반 또는 직무집행의 형식적 흠결만으로 곧바로 형법상 적법성과 보호가치가 부정되는 것은 아니다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사소한 절차 위반과 형법상 보호가치의 관계는 개별 사안에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_10` / `Ⅱ.3`: “행정법상 사소한 절차규정을 위반하였다고 하여 위법한 공무집행 으로 볼 수 없다고 판시하였다”
  - `comm_001692_제136조_Ⅱ.3_28` / `Ⅱ.3`: “당해 행위가 근거법령상의 방식과 절차를 준수하 지 아니하였다고 하여 곧바로 형법상의 적법성이 부정되는 것은 아니다.”
  - `comm_001692_제136조_Ⅱ.3_9` / `Ⅱ.3`: “직무집행이 형식적으로 적법하지 아니한 것만으로 곧바로 그 직무집행이 형법상 적법하지 아니하다고 볼 수 있는 것은 아니고 형식적 적법성도 형법상 보호가치의 존부의 관점에서 판단하여야 한다.”

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

## 19. `art136_sec2_3.protective_room_exception`

- proposition: 영장 없이 경찰 보호실에 유치하는 것은 원칙적으로 위법하나, 정신착란자·주취자·자살기도자 등 응급구호 필요자를 24시간 이내 보호하는 시설로 제한 운영되고 보호조치 요건 및 가족 등에 대한 지체 없는 통지가 충족되는 경우는 제외된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보호조치의 응급성, 시간 제한 및 통지 요건을 별도로 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_18` / `Ⅱ.3`: “관직무집행법상 정신착란자, 주취자, 자살기도자 등 응급의 구호를 요하는 자를 24시간을 초과하지 아니하는 범위 내에서 경찰관서에 보호조치할 수 있는 시설”
  - `comm_001692_제136조_Ⅱ.3_29` / `Ⅱ.3`: “피고인이 보호실에 유치될 당시 피고인이 응급의 구호를 요한다고 믿을만한 상당한 이유가 있었다든지 피고인이 보호실에 유치된 후 경찰관이 지체 없이 그 사실을 피고인의 가족 등에게 통지하였다고 볼 수 없다면, 피고인을 적법하게 보호조치한 것이 아니어서”

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

## 20. `art136_sec2_3.public_official_definition`

- proposition: 공무원이란 법령에 의하여 국가 또는 공공기관의 공무에 종사하는 자 및 법령에 의하여 공무에 종사하는 자로 간주되는 자를 의미하며, 외국의 공무원은 공무집행방해죄의 객체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공무원 객체의 인적 범위를 정리한 카드다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_4` / `Ⅱ.3`: “공무원이란 법령에 의하여 국가 또 는 공공기관의 공무에 종사하는 자를 의미한다. 공무원의 신분을 갖고 있는 자 뿐만 아니라 법령에 의하여 공무에 종사하는 자로 간주되는 자도 본죄의 객체 가 된다.”
  - `comm_001692_제136조_Ⅱ.3_4` / `Ⅱ.3`: “본죄는 우리나라의 공무를 보호하기 위한 범죄이므로 외국의 공무원은 본죄의 객체가 될 수 없다.”

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

## 21. `art136_sec2_3.voluntary_accompaniment`

- proposition: 임의동행은 상대방의 동의 또는 승낙을 요건으로 하고, 상대방은 요구를 거절하거나 동행 후 언제든 경찰관서에서 퇴거할 자유가 있으며, 자발적 의사에 따른 동행임이 객관적으로 명백히 입증되지 않거나 퇴거를 제지하면 적법한 공무집행으로 보기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 임의성은 동의의 객관적 입증과 이탈·퇴거 자유의 실질적 보장에 따라 검토한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.3_20` / `Ⅱ.3`: “임의동행은 상대방의 동의 또는 승낙을 그 요건으로 하는 것이므로 경찰관”
  - `comm_001692_제136조_Ⅱ.3_20` / `Ⅱ.3`: “경찰관으로부터 임의동행 요구를 받은 경우 상대방은 이를 거절할 수 있을 뿐만 아니 라 임의동행 후 언제든지 경찰관서에서 퇴거할 자유가 있고”
  - `comm_001692_제136조_Ⅱ.3_30` / `Ⅱ.3`: “오로지 피의자의 자발적인 의사에 의하여 수사관서 등에의 동행이 이루어졌음이 객관적인 사정에 의하여 명백하게 입증된 경우에 한하여, 비로소 그 적법성을 인정하여야 한”

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

## 22. `art136_sec2_4.abstract_danger_offense`

- proposition: 공무집행방해죄는 추상적 위험범으로서 직무집행 중인 공무원에 대한 폭행 또는 협박이 있으면 성립하며, 구체적 직무방해 결과의 발생은 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 공무원에 대한 폭행 또는 협박이 확인된 경우 구체적 공무방해 결과 또는 위험의 발생을 별도 요건으로 요구하지 않는 관계다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_46` / `Ⅱ.4`: “본죄 는 추상적 위험범으로서 공무원에 대한 폭행이나 협박을 하면 곧바로 기수에 이르 고 폭행이나 협박으로 인하여 공무방해의 결과나 그 구체적 위험이 발생할 것을 요 하지 아니한다고 보아야 한다.”

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

## 23. `art136_sec2_4.active_conduct_requirement`

- proposition: 공무집행방해죄의 폭행·협박은 적극적 행위에 의하여야 하며, 소극적 거동이나 불복종은 폭행·협박에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 행위가 적극적 행위인지 소극적 거동 또는 불복종인지의 구별은 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_45` / `Ⅱ.4`: “본죄의 폭행·협박은 적극적인 행위에 의할 것을 요한다. 소극적인 거동이나 불 복종은 폭행·협박에 해당하지 아니한다.”

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

## 24. `art136_sec2_4.active_confinement_or_dog_release`

- proposition: 공무원이 나가지 못하도록 문을 닫거나 맹견을 풀어 놓는 행위는 적극적 행위로서 폭행에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 문을 닫은 목적 및 맹견을 풀어 놓은 행위의 상황별 유형력 해당성 검토가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_45` / `Ⅱ.4`: “공무원이 나가지 못하도록 문을 닫거나 맹견을 풀어 놓는 것은 적극적인 행위로서 폭행에 해당할 수 있다.”

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

## 25. `art136_sec2_4.assault_against_assistant`

- proposition: 공무원의 지휘 아래 있고 직무집행과 밀접불가분 관계에 있는 보조자에게 가한 유형력은 공무집행방해죄의 폭행에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 보조자의 지휘관계와 직무집행과의 밀접불가분성은 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_41` / `Ⅱ.4`: “공무원의 지휘 아래 있어서 직무집행과 밀접불가분의 관계에 있는 보조 자에게 가해지는 유형력도 본죄의 폭행에 해당한다.”

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

## 26. `art136_sec2_4.assault_definition`

- proposition: 공무집행방해죄의 폭행은 공무원에 대한 직·간접적인 불법적 유형력 행사이며, 공무원의 신체에 대한 유형력 행사로 한정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 직접·간접 유형력 및 공무원에 대한 행사 해당성은 개별 사실관계에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_41` / `Ⅱ.4`: “본죄에서 폭행이란 공무원에 대한 직·간접적인 불법적인 유형력의 행사를 의미 한다. 본죄의 폭행은 공무원의 신체에 대한 유형력의 행사로 한정되는 것이 아니다.”

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

## 27. `art136_sec2_4.assault_not_against_officer_exception`

- proposition: 직무집행과 관련된 물건 또는 제3자에 대한 유형력 행사라도 그것이 공무원에게 행하여진 것으로 인정되지 않으면 공무원에 대한 폭행이 아니다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 물건 또는 제3자에 대한 유형력이 공무원에 대한 것으로 인정되는지 별도 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_41` / `Ⅱ.4`: “공무원의 직무집행과 관련성 있는 물건 또는 제3자에 대한 유형력의 행사가 이루어지더라도 이것이 공무원에 대 하여 행하여진 것이라고 인정될 수 없는 경우에는 본죄의 공무원에 대한 폭행에 해 당하지 아니한다.”

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

## 28. `art136_sec2_4.noise_as_assault`

- proposition: 집회·시위 과정의 일시적 상당한 소음만으로는 음향에 의한 폭행이 아니지만, 의사전달수단의 합리적 범위를 넘어 상대방에게 고통을 줄 의도로 음향을 이용한 경우 폭행이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 음향 이용의 목적 및 의사전달수단으로서의 합리적 범위는 개별 사안에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_41` / `Ⅱ.4`: “의사전달수단으로서 합리적 범위를 넘어서 상대방에게 고통 을 줄 의도로 음향을 이용하였다면 이를 폭행으로 인정할 수 있다.”

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

## 29. `art136_sec2_4.noise_assault_factors`

- proposition: 음향에 의한 폭행 해당성은 음량·음높이·지속시간·종류·행위자 의도·음향 발생원과 공무원의 거리 및 당시 주변 상황을 종합 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정을 종합하는 평가기준이므로 기계적 관계로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_41` / `Ⅱ.4`: “음량의 크기 나 음의 높이, 음향의 지속시간, 종류, 음향발생 행위자의 의도, 음향 발생원과 직무를 집행 중인 공무원과의 거리, 음향발생 당시의 주변 상황을 종합적으로 고려하여 판단하여야 한다.”

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

## 30. `art136_sec2_4.nontrivial_assault_or_threat`

- proposition: 폭행·협박은 공무원의 직무집행을 방해할 만한 정도여야 하며, 공무원이 전혀 개의치 않을 정도로 경미한 협박은 협박에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 경미한 협박의 한계에 관한 판시이므로 원판례와 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제136조_Ⅱ.4_45` / `Ⅱ.4`: “그 협박이 경미하여 상대방이 전 혀 개의치 아니할 정도인 경우에는 협박에 해당하지 아니한다고 판시하였다.”

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
