# 강간등상해·치상 RuleIR 카드 검수 2

- unit: `sexual_offense_injury_or_death`
- articles: art301
- cards: 16–30 / 34
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #28 `art301_sec4_6.pregnancy_injury`: `art301_sec4_6.unwanted_pregnancy_not_injury_holding` (status=`valid`)
- #29 `art301_sec7.special_rape_attempt_result`: `art301_sec7.special_rape_injury_completed` (status=`valid`)

## 16. `art301_sec4_2.minor_injury_exclusion`

- proposition: 상처가 극히 경미하여 치료할 필요가 없고, 치료 없이도 일상생활에 아무런 지장이 없으며, 시간이 지나 자연적으로 치유될 수 있는 정도이면 상해에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상처의 경미성, 치료 필요성, 일상생활 지장 및 자연치유 가능성을 구체적 사실에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.2_4` / `Ⅳ.2`: “상처가 극히 경미하여 굳이 치료할 필요가 없고, 치료를 받지 않 더라도 일상생활을 하는 데 아무런 지장이 없으며, 시일이 경과함에 따라 자연 적으로 치유될 수 있는 정도”

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

## 17. `art301_sec4_4.injury_recognition_factors`

- proposition: 상해 인정 여부에서는 상처가 일상생활에서 흔히 발생할 수 있는지, 별다른 치료 없이 단기간 내 자연치유되는지, 그리고 피해자가 피해 후 곧바로 상처를 자각하여 의사에게 호소했는지를 고려한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 제공된 인용문이 명시한 상해 인정 요소에 한정한 평가 기준이다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.4_11` / `Ⅳ.4`: “상해의 인정 여부에 중요한 영향을 미친 요소를 추출하여 본다면, ⅰ) 상처가 일상생활에서 흔히 발생할 수 있는 것인지 여부 및 별다른 치료 없이도 단기간 내에 자연치유가 되는 것인지 여부, ⅱ) 피해자가 피해를 당한 후 곧바로 상처”
  - `comm_001692_제301조_Ⅳ.4_11` / `Ⅳ.4`: “를 자각하고 의사에게 호소하였는지 여부”

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

## 18. `art301_sec4_4.minor_broader_injury`

- proposition: 판례는 피해자가 미성년자인 경우 상해의 범위를 다소 넓게 인정하는 경향이 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글이 보고한 판례 경향이며, 원판례 확인 전에는 commentary-reported precedent로 유지한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.4_11` / `Ⅳ.4`: “판례는 피해자가 미성년자인 경우”
  - `comm_001692_제301조_Ⅳ.4_11` / `Ⅳ.4`: “에는 상해의 범위를 다소 넓게 인정하는 경향이 있다.”

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

## 19. `art301_sec4_5.drug_induced_consciousness_impairment`

- proposition: 수면유도 약물로 피해자가 일시적 수면 또는 의식불명 상태가 되고 건강상태가 불량하게 변경되거나 생활기능 장애가 초래되면, 외부 상처가 없거나 자연 회복하더라도 상해에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 약물 투여, 건강상태의 불량한 변경, 생활기능 장애 및 그 경과를 사실관계와 의료자료로 검토해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.5_12` / `Ⅳ.5`: “그 약물로 인하여 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래되었다면 자연적으로 의식을 회복하거나 외부 적으로 드러난 상처가 없더라도 이는 상해에 해당”

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

## 20. `art301_sec4_5.functional_impairment_injury`

- proposition: 외부 상처가 없더라도 육체적·정신적 생리기능 훼손, 예컨대 보행불능·수면장애·식욕감퇴 등의 기능장애가 발생하면 상해로 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 외부 상처의 유무만으로 상해를 배제하지 않으며, 생리기능 훼손 및 기능장애의 사실적 존재는 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.5_12` / `Ⅳ.5`: “적으로 어떤 상처가 발생하지 않았다고 하더라도 생리적 기능 (육체적 기능 및 정 이 훼손된 경우, 즉 보행불능, 수면장애, 식욕감퇴 등의 기능 신적 기능도 포함) 장애를 일으킨 경우”

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

## 21. `art301_sec4_5.ptsd_as_injury`

- proposition: 심각한 외상 후 나타나는 외상 후 스트레스 장애도 상해로 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 외상 후 스트레스 장애의 존재와 상해 해당성은 진단 및 구체적 증상 자료를 토대로 검토해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.5_12` / `Ⅳ.5`: “범죄, 전쟁, 자연재해 등 심각한 외상을 경험한 후에 나 타나는 정신병리학적 반응인 ‘외상 후 스트레스 장애’”

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

## 22. `art301_sec4_5.ptsd_causation_assessment`

- proposition: 성범죄 후 외상 후 스트레스 장애의 상해 여부 및 인과관계는 피해자가 필연적으로 겪는 정도의 증상인지, 의사 진단·소견, 범행 내용, 구체적 증상, 치료 내용과 경과, 기존 정신과 치료 전력 등을 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 외상 후 스트레스 장애의 상해 해당성과 범행 사이 인과관계는 열거된 사정을 종합하는 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.5_12` / `Ⅳ.5`: “성폭력범죄를 당한 피해자가 필연적으로 겪 는 정도의 증상으로 볼 수 있는지를 고려한 것이 있고, 그 외에 의사의 진단 서 내지 소견을 기초로 범행의 내용, 피해자의 구체적인 증상, 치료의 내용과 경 과, 피해자의 기존 정신과 치료 전력 등을 고려하여”

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

## 23. `art301_sec4_7.pubic_hair_cutting_not_injury`

- proposition: 음모 모근을 남기고 모간 일부만 잘라 외관 변형이 생긴 경우, 수치심이나 폭행 해당 가능성과 별개로 건강상태의 병리적 불량 변경이나 생활기능 장애가 없으므로 강제추행치상죄의 상해에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 외관 변형과 수치심만으로는 상해를 인정하지 않는 범위를 건강상태의 병리적 변경 또는 생활기능 장애 기준에 따라 검토한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.7_15` / `Ⅳ.7`: “피해자의 음모의 모근 부분을 남기고 모간 부분만을”
  - `comm_001692_제301조_Ⅳ.7_15` / `Ⅳ.7`: “일부 잘라냄으로써 음모의 전체적인 외관에 변형만 생겼다면, 이로 인하여 피해 자에게 수치심을 야기하기는 하겠지만, 병리적으로 보아 피해자의 신체의 건강 상태가 불량하게 변경되거나 생활기능에 장애가 초래되었다고 할 수는 없으므 로”

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

## 24. `art301_sec4_7.pubic_hair_pulling_injury`

- proposition: 음모를 잡아당겨 음부 부근에 염증을 발생시키거나 음모를 모근부터 뽑는 경우 상해에 해당한다고 볼 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 염증 발생 또는 모근부터의 발모라는 구체적 사실이 상해 판단에 필요한지 검토한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.7_15` / `Ⅳ.7`: “음모를 잡아당김으로써 음부 부근에 염증을 발생하게 하거나 음모를 모근부터 잡아 뽑는 경우는 상해에 해당한다고 볼 수 있다.”

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

## 25. `art301_sec5_1.intentional_rape_injury`

- proposition: 강간 등 상해죄는 강간 등 범행과 상해에 대한 고의가 요구되는 고의범이고, 미필적 고의로도 족하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 강간 등 범행 및 상해에 대한 고의와 미필적 고의 충족 여부는 구체적 사실관계에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제301조_Ⅴ.1_16` / `Ⅴ.1`: “강간 등 ‘상해’죄는 강간죄, 유사강간죄, 강제추행죄 또는 준강간·준유사강간·준강제추행죄와 상해 죄가 결합된 고의범이므로, 강간 등의 범행과 상해의 점에 대한 고의가 요구된 다. 고의는 미필적 고의로도 족하다.”

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

## 26. `art301_sec5_2.fleeing_traffic_injury`

- proposition: 피해자가 강간 등 범행을 피해 도망가다가 자동차에 치여 상해를 입은 경우 인과관계와 예견가능성이 충분히 인정되어 강간 등 치상죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 도주와 교통사고 상해가 결합된 좁은 사실유형에 관한 인과관계 및 예견가능성 판단이다.
- bounded sources:

  - `comm_001692_제301조_Ⅴ.2_18` / `Ⅴ.2`: “피해자가 강간 등 범행을 피해 도망가던 중 자동차에 치어 상해를 입은 경 우에는 인과관계나 예견가능성을 충분히 인정할 수 있으므로, 본죄가 성립한다.”

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

## 27. `art301_sec5_2.injury_foreseeability_assessment`

- proposition: 상해 결과의 예견가능성은 폭행·협박 정도, 피해자의 나이와 대응상태 등 당시 구체적 상황을 종합하여 엄격히 판단하며, 일반인이 예견하기 어려운 이례적 결과는 인정하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 예견가능성 판단 요소와 이례적 결과의 취급은 사실관계별 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅴ.2_17` / `Ⅴ.2`: “‘예 (豫⾒可能性)(형법 제15조 제2항) 견가능성’의 유무는 폭행·협박의 정도, 피해자의 나이나 대응상태 등 당시의 구 체적 상황을 종합하여 엄격하게 판단하여야 하고, 통상적으로 일반인이 예견하 기 어려운 결과로서 이례적인 일에 속할 때에는 이를 인정하기 어렵다.”

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

## 28. `art301_sec5_2.rape_injury_causation_foreseeability`

- proposition: 강간 등 치상죄는 강간 등 행위와 상해 결과 사이 인과관계 및 결과발생에 대한 예견가능성을 요한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인과관계와 예견가능성은 구체적 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅴ.2_17` / `Ⅴ.2`: “강간 등의 행위와 상해의 결과발생 사이에 인과관계 (因果關係) 와 결과발생에 대한 예견가능성이 있어야 한다.”

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

## 29. `art301_sec5_2.rape_injury_result_aggravation`

- proposition: 강간 등 치상죄는 강간 등 범행의 고의는 필요하지만 상해 결과에 대한 고의는 요구되지 않는 결과적 가중범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강간 등 범행에 대한 고의와 상해 결과에 대한 고의 불요를 구별하는 결과적 가중범 구조다.
- bounded sources:

  - `comm_001692_제301조_Ⅴ.2_17` / `Ⅴ.2`: “강간 등 ‘치상’죄는 강간죄 등에 상해의 중한 결과가 발생한 결과적 가중범이므 로, 강간 등 범행에 대한 고의가 요구되나, 상해의 결과에 대하여는 고의가 요구 되지는 아니하고”

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

## 30. `art301_sec6.intentional_injury_conspirator_intent`

- proposition: 고의범인 강간 등 상해죄에서 공모자에게도 상해에 대한 고의가 필요하므로, 그 고의를 인정하기 어려우면 공동정범으로 처벌할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공모자의 상해 고의 인정은 개별 사정에 대한 평가가 필요하며, 고의가 인정되지 않는다는 실제 판단이 있어야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅵ_19` / `Ⅵ`: “고의범으로서 ‘상해에 대한 고의’를 필요로 하는 ‘강간 등 상해죄’의 경우에는 공모자에게도 그에 대한 고의가 필요하므로, 고의 를 인정하기 어려울 경우에는 공동정범으로 처벌할 수 없다.”

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
