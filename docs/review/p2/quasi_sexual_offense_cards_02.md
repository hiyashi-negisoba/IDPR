# 준강간·준강제추행 RuleIR 카드 검수 2

- unit: `quasi_sexual_offense`
- articles: art299
- cards: 16–26 / 26
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #27 `art299_sec7.changed_circumstances_concurrence`: `art299_sec7.changed_circumstances_rape_only` (status=`valid`)

## 16. `art299_sec5.impossible_attempt_actual_state_absent`

- proposition: 피고인이 피해자가 심신상실 또는 항거불능 상태라고 인식하고 그 상태를 이용해 간음할 의사로 간음했으나 실제로 그러한 상태가 없었던 경우, 행위 당시 인식 사정을 기준으로 일반인이 결과 발생 위험성을 인정하면 준강간 불능미수가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위 당시 피고인의 인식과 일반인의 객관적 위험성 판단을 각각 사실평가 입력으로 검토해야 한다. 해당 설명이 판례의 직접 보고인지 여부는 원문 확인 전까지 확정하지 않는다.
- bounded sources:

  - `comm_001692_제299조_Ⅴ_10` / `Ⅴ`: “피고인이 행위 당시에 인식한 사정을 놓고 일반인이 객관적으로 판단하여 보았을 때 정신적·신체적 사정으로 인하여 성적인 자기방어를 할 수 없는 사람의 성적 자기결”
  - `comm_001692_제299조_Ⅴ_10` / `Ⅴ`: “정권을 침해하여 준강간의 결과가 발생할 위험성이 있었다면 불능미수가 성립한다.”

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

## 17. `art299_sec6.dolus_eventualis`

- proposition: 본죄의 고의는 미필적 고의로도 족하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 미필적 고의 해당성은 개별 사정에 따른 내심의 인식과 용인 판단을 필요로 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅵ_11` / `Ⅵ`: “미필적 고의로도 족하다.”

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

## 18. `art299_sec6.formal_response_not_consent`

- proposition: 피해자가 정신적·육체적으로 정상적인 판단이 불가능한 상황에서 한 형식적인 '괜찮다'는 답변은 피고인과의 성행위에 동의하는 취지의 답변으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판단의 사실관계와 원판결을 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅵ_11` / `Ⅵ`: “피해자의 ‘괜 찮다.’는 답변은 이미 정신적으로나 육체적으로 정상적인 판단이 불가능한 상황에 서 형식적인 답변을 한 것에 불과해 보일 뿐 피고인과의 성행위에 동의하는 취지 의 답변으로 볼 수 없다.”

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

## 19. `art299_sec6.genuine_consent_belief`

- proposition: 성관계 등에 대하여 피해자의 자유롭고 진정한 의사에 기한 승낙이 있다고 믿었다면 본죄의 고의를 인정하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 승낙에 관한 믿음의 존재와 그 대상이 자유롭고 진정한 의사에 기한 승낙인지에 대한 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제299조_Ⅵ_11` / `Ⅵ`: “성관계 등에 대한 피해자의 자유롭고 진정한 의사에 기한 승낙이 있다고 믿었다면 고의를 인정하기 어렵다.”

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

## 20. `art299_sec6.intent`

- proposition: 본죄의 고의는 피해자의 심신상실 또는 항거불능 상태 및 그 상태를 이용한 구성요건적 결과 발생 가능성을 인식하고 위험을 용인하는 내심의 의사이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 심신상실 또는 항거불능 상태와 이를 이용한 결과 발생 가능성에 관한 인식 및 위험 용인의 사실판단이 필요하다.
- bounded sources:

  - `comm_001692_제299조_Ⅵ_11` / `Ⅵ`: “본죄의 고의는 피해자가 심신상실 또는 항거불능의 상태에 있고 그러한 상태를 이용하여 간음이나 유사간음 또는 추행한다는 구성요건적 결과 발생의 가능성을 인식하고 그러한 위험을 용인하는 내심의 의사이다.”

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

## 21. `art299_sec7.unit_of_crime_per_act`

- proposition: 본죄는 원칙적으로 각 간음행위, 유사간음행위, 추행행위마다 하나의 범죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 각 행위별 죄수 판단의 원칙으로 검토한다.
- bounded sources:

  - `comm_001692_제299조_Ⅶ_12` / `Ⅶ`: “본죄도 성적 자기결정권이라는 인격적 법익을 침해하는 범죄이므로, 원칙적으로 각 간음행위, 유사간음행위, 추행행위마다 하나의 범죄가 성립한다.”

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

## 22. `art299_sec8.attempt_preparation_punishment`

- proposition: 준강간죄의 미수범과 예비·음모범 및 준유사강간·준강제추행죄의 미수범은 처벌한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 범죄유형과 행위단계의 열거된 조합에 한정하여 처벌 가능성을 검토한다.
- bounded sources:

  - `comm_001692_제299조_Ⅷ_13` / `Ⅷ`: “준강간죄의 미수범과 예비·음모범, 준유사강간·준강제추행죄의 미수범은 처벌한 다.”

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

## 23. `art299_sec8.noncomplaint_prosecution`

- proposition: 본죄는 피해자의 고소가 없더라도 공소를 제기하고 처벌할 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 피해자의 고소를 요구하는 친고죄 취급에 대한 예외로 검토한다.
- bounded sources:

  - `comm_001692_제299조_Ⅷ_13` / `Ⅷ`: “따라서 피해자의 고소가 없더라도 공소를 제기하고 처벌 제306조) 할 수 있다.”

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

## 24. `art299_sec8.noncomplaint_retroactivity`

- proposition: 친고죄 폐지는 개정 법률 시행일인 2013년 6월 19일 이후 최초로 저지른 범죄부터 적용된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 범행 시점과 2013년 6월 19일을 기계적으로 비교하는 적용범위 카드다.
- bounded sources:

  - `comm_001692_제299조_Ⅷ_13` / `Ⅷ`: “다만 친고죄 폐지는 개정 법률이 시행된 2013. 6. 19. 이후 최초로 저지른 범죄부터 적용된다.”

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

## 25. `art299_sec8.quasi_indecent_act_indictment_amendment`

- proposition: 강제추행으로 기소된 피고인에 대하여 준강제추행 해당 가능성이나 공소장변경이 심리에서 논의·공방되지 않아 방어권 행사의 기회가 없었던 경우, 원칙적으로 공소장변경 절차 없이 준강제추행 유죄를 인정하기 어렵다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 방어권 행사 기회, 심리상 공방 여부 및 공소장변경 절차의 충족 여부는 개별 기록에 대한 평가가 필요하다. 소개된 대법원 판단은 primary precedent index로 확인해야 한다.
- bounded sources:

  - `comm_001692_제299조_Ⅷ_13` / `Ⅷ`: “피고인으로서는 준강제추행의 범죄사실이 심판 의 대상이 되리라고 예상할 수 있었거나 그에 대한 방어권을 행사할 기회를 부 여받았다고 보기 어렵다.”는 취지로 판시하여, 원칙적으로 공소장변경 절차를 거쳐야 한다고 판단하였다.”

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

## 26. `art299_sec7.changed_circumstances_rape_only`

- proposition: 준강간죄의 구성요건이 갖추어진 상태에서 실행에 착수한 뒤 피해자가 깨는 등 사정 변화 후 폭행·협박으로 간음한 경우, 강간죄만 성립한다고 보는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 실체적 경합을 부정하고 강간죄만 인정하는 경쟁 견해로서, 채택 전 법리 검토가 필요하다.
- bounded sources:

  - `comm_001692_제299조_Ⅶ_12` / `Ⅶ`: “강 간죄만 성립한다고 보는 견해도 있다.”

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
