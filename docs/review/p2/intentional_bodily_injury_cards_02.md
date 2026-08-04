# 상해·특수상해·상해치사 RuleIR 카드 검수 2

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 16–30 / 104
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

## 16. `art257.sexual_offense_psychiatric_injury_case`

- proposition: 강제추행 피해자가 충격으로 급성 스트레스 반응과 우울장애 증세를 보여 1개월 이상 정신과 치료가 필요하다는 진단을 받고 실제 치료를 받은 경우 상해 성립을 긍정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 정신적 증상, 치료 필요성 및 실제 치료 사실의 증명 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_12` / `Ⅰ.3`: “강제추행의 피해자가 충격으로 급성 스트레스 반응과 우울장애의 증세를 보여 1개월 이상 의 정신과적 치료를 요한다는 진단을 받고 실제로 그 후 정신과적 치료를 받은 경우”

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

## 17. `art257.std_infection_case`

- proposition: 성병에 감염된 경우 상해 성립을 긍정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 감염 사실만으로는 개별 사건에서의 감염 경로와 인과관계가 확정되지 않는다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_12` / `Ⅰ.3`: “성병에 감염된 경우”

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

## 18. `art257.subjective_pain_diagnosis_assessment`

- proposition: 주관적 통증 호소 등에 주로 의존하여 의학적 가능성만으로 발급된 상해진단서는 진단 시점, 발급 경위, 상해 원인과의 일치, 기존 질환과의 관계, 발급 근거 및 진료 경과 등을 면밀히 살펴 증명력을 판단하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주관적 호소에 의존한 진단서에 관한 구체적 증명력 판단 기준의 적용은 법률 검토가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_10` / `Ⅰ.3`: “특히 상해진단서가 주로 통증이 있다는 피해자의 주관적인 호소 등에 의존하여 의학 적인 가능성만으로 발급된 때에는 그 진단 일자 및 진단서 작성일자가 상해 발 생 시점과 시간상으로 근접하고”
  - `comm_001692_제257조_Ⅰ.3_10` / `Ⅰ.3`: “피해자가 상해 사건 이후 진료를 받은 시점, 진료를 받게 된 동기와 경위, 그 이후의 진료 경과 등을 면밀히 살펴 논리와 경험법칙에 따라 그 증명력을 판단하여야 한다고 본다.”

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

## 19. `art257.zolpidem_unconsciousness_case`

- proposition: 졸피뎀이 섞인 커피를 마신 피해자가 곧 의식을 잃고 약 4시간 뒤 깨어난 경우 상해 성립을 긍정한 사례로 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 약물 투여와 의식상실의 인과관계 및 상해 해당성을 개별 증거로 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_14` / `Ⅰ.3`: “피고인으로부터 향정신성의약품인 졸피뎀 성분의 수면제가 섞인 커피를 받아 마신 다 음 곧바로 정신을 잃고 깊이 잠들었다가 약 4시간 뒤에 깨어난 경우”

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

## 20. `art257_sec1_1.offense_elements`

- proposition: 상해죄는 고의로 사람의 신체를 상해함으로써 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 고의 및 신체 상해 해당성은 개별 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.1_0` / `Ⅰ.1`: “상해죄는 고의로 사람의 신체를 상해함으로써 성립한다.”

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

## 21. `art257_sec1_2.animal_not_object`

- proposition: 동물은 상해죄의 객체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 동물을 상해죄 객체에서 제외하는 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_1` / `Ⅰ.2`: “동물 도 상해죄의 객체가 될 수 없으므로”

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

## 22. `art257_sec1_2.coerced_self_injury_holding`

- proposition: 피해자를 협박하여 자상하게 한 경우, 피고인에게 상해 결과 인식이 있고 협박이 피해자의 의사결정 자유를 상실시킬 정도이면 상해죄를 구성한다는 대법원 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 협박의 강도와 상해 결과 인식은 평가적 판단을 요하며, reported holding은 primary precedent index로 확인이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_3` / `Ⅰ.2`: “피고인이 피해자를 협박하여 그로 하여금 자상케 한 경우에 피고인에게 상해의 결과 에 대한 인식이 있고 또 그 협박의 정도가 피해자의 의사결정의 자유를 상실케 함에 족한 것인 이상 피고인에 대하여 상해죄를 구성한다.”

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

## 23. `art257_sec1_2.corporation_not_object`

- proposition: 법인은 상해죄의 객체에 포함될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 법인을 상해죄 객체에서 제외하는 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_1` / `Ⅰ.2`: “법인은 신체를 지닌 자연인이 아니므로 상해죄의 객체에 포함될 수 없다.”

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

## 24. `art257_sec1_2.corpse_not_object`

- proposition: 사체는 상해죄의 객체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 생명 없는 사체를 상해죄 객체에서 제외하는 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_1` / `Ⅰ.2`: “신체는 생명 있는 사람의 신체를 말하므로, 사체는 상해죄의 객체가 될 수 없고”

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

## 25. `art257_sec1_2.fetus_not_object`

- proposition: 상해죄의 객체는 출생한 사람에 한정되므로 태아는 상해죄의 객체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 태아 자체를 상해죄의 직접 행위객체로 보지 않는 기본 객체 범위 카드다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_1` / `Ⅰ.2`: “사람은 살아 있는 사람을 의미하므로 상해죄의 객체는 출생한 사람에 제한되고, 태아는 상해죄의 객체가 될 수 없다.”

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

## 26. `art257_sec1_2.indirect_perpetration_self_injury`

- proposition: 타인을 강요하거나 기망하여 의사에 반해 자상하게 한 경우 상해죄의 간접정범이 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 강요·기망 및 피해자 의사에 반한 자상 여부는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_3` / `Ⅰ.2`: “타인을 강요하거나 기망하여 그 의사에 반하여 자상하게 한 때에는 구성요건에 해당하지 않는 타인의 행위를 이용하여 상해죄를 실현하는 것으로서 상해죄의 간접정범이 성립할 수 있다.”

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

## 27. `art257_sec1_2.object_natural_person_other`

- proposition: 상해죄의 행위객체는 자연인인 타인의 신체이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 상해죄 객체의 기본 범위를 자연인인 타인의 신체로 한정하는 카드다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_1` / `Ⅰ.2`: “행위의 객체는 사람의 신체이다. 여기서 사람이란 자연인인 타인을 의미한다.”

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

## 28. `art257_sec1_2.self_injury_not_punishable_principle`

- proposition: 자기의 신체를 상해하는 자상은 원칙적으로 죄가 되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 자기 신체에 대한 자상을 원칙적으로 처벌 대상에서 제외하는 카드다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.2_3` / `Ⅰ.2`: “따라서 자기의 신체를 상해하는 행위, 즉 자상은 원칙적으로 죄가 되지 않는다.”

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

## 29. `art257_sec1_4.dolus_eventualis_acceptance`

- proposition: 상해 결과를 의욕하지 않았더라도 그 결과의 발생을 감수·용인하고 폭행에 나아갔다면 상해죄가 성립한다는 취지로 이해할 수도 있어 보인다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 원문이 '이해할 수도 있어 보인다'고 조건적으로 서술하므로 적용 및 권위 확인이 필요하다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_18` / `Ⅰ.4`: “상해의 고의는 미필적 고의로도 충분하므로 상해의 결과를 의욕하지 않았더라 도 그 결과의 발생을 감수·용인하고 폭행에 나아갔다면 상해죄가 성립한다는 취지로 이해할 수도 있어 보인다.”

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

## 30. `art257_sec1_4.injury_attempt`

- proposition: 상해의 고의가 있었으나 사람을 상해한 때에 이르지 못하고 폭행의 결과가 발생한 데 그쳤다면 상해미수죄가 될 것이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상해에 이르지 못한 경우와 폭행 결과의 구별을 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.4_18` / `Ⅰ.4`: “상해의 고의가 있었으나 사람을 상해한 때에 이 르지 못하고 폭행의 결과가 발생한 데 그쳤다면 상해미수죄가 될 것이다.”

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
