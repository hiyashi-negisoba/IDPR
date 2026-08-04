# 살인·존속살해 RuleIR 카드 검수 15

- unit: `homicide`
- articles: art250, art254, art255
- cards: 211–225 / 242
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #7 `art250_sec1_10.officer_omission_murder`: all_demoted (status=`valid`)
- #8 `art250_sec1_11.indirect_perpetration_attempt`: `art250_sec1_11.indirect_perpetration_attempt_use_act` (status=`valid`)
- #9 `art250_sec1_17.direct_active_euthanasia_legality`: `art250_sec1_17.direct_active_euthanasia_negative` (status=`valid`)
- #10 `art250_sec1_19.excessive_execution_death`: `art250_sec1_19.excessive_execution_death_precedent` (status=`valid`)
- #11 `art250_sec1_21.death_penalty_threshold`: `art250_sec1_21.death_penalty_special_circumstances_majority` (status=`valid`)
- #12 `art250_sec1_3.birth_onset`: `art250_sec1_3.birth_labor_theory` (status=`valid`)
- #13 `art250_sec1_3.death_onset`: `art250_sec1_3.pulse_cessation_organ_removal` (status=`valid`)
- #14 `art250_sec1_3.organ_transplant_law_effect`: `art250_sec1_3.organ_transplant_law_limited_effect` (status=`valid`)
- #15 `art250_sec2_10.arson_death_parricide_concurrence`: `art250_sec2_10.arson_death_parricide_imaginary_concurrence` (status=`valid`)
- #16 `art250_sec2_6.adoptee_biological_parent_offense`: `art250_sec2_6.adoption_type_determines_offense` (status=`valid`)
- #17 `art250_sec2_6.deceased_spouse_lineal_ascendant_offense`: `art250_sec2_6.deceased_spouse_lineal_ascendant_ordinary_murder` (status=`valid`)
- #18 `art250_sec2_9.nonstatus_accomplice_liability`: `art250_sec2_9.nonstatus_accomplice_parricide_coprincipal_punished_ordinary` (status=`valid`)
- #19 `art250_sec2_9.status_instigator_nonstatus_principal`: `art250_sec2_9.status_instigator_parricide_accomplice` (status=`valid`)
- #20 `art255_sec4.preparation_desistance`: `art255_sec4.preparation_desistance_doctrinal_variants` (status=`valid`)

## 211. `art254.attempts_punishable`

- proposition: 제250조, 제252조 및 제253조의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 조문 인용에 따른 열거형 미수 처벌 규정이다.
- bounded sources:

  - `raw_001692_제254조_p001` / `raw_pdf.page_1`: “제250조, 제252조 및 제253조의 미수범은 처벌한다.”

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

## 212. `art254.electronic_device_attachment`

- proposition: 제254조의 미수범은 전자장치 부착 등에 관한 법률이 정하는 특정범죄인 살인범죄로서 전자장치 부착명령 대상이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 전자장치 부착명령의 구체적 요건 및 현행 법률상 적용 범위는 별도 검토가 필요하다.
- bounded sources:

  - `raw_001692_제254조_p001` / `raw_pdf.page_1`: “본죄에           
           해당하는  미수범 역시 전자장치  부착 등에  관한 법률이 정하는  특정범죄(살인범”
  - `raw_001692_제254조_p001` / `raw_pdf.page_1`: “죄)로서 전자장치 부착명령  대상이다.”

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

## 213. `art255_sec2_1.hiring_killers_holding`

- proposition: 소개된 판례는 살인을 위하여 다른 사람들을 고용하고 대가 지급을 약속한 경우, 살인 목적 및 준비에 관한 고의와 살인 실현을 위한 준비행위를 인정하여 살인예비죄 성립을 인정하였다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 고용 및 대가 지급 약속이라는 좁은 사실관계에 관한 소개된 판례 결론으로 보존하며, 원판례 확인 전 일반화하지 않는다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.1_1` / `Ⅱ.1`: “甲이 ⼄을 살해하기 위하여 丙, 丁 등을 고용하면서 그들에게 대가의 지급을 약속한 경우, 甲에게는 살인죄를 범 할 목적 및 살인의 준비에 관한 고의뿐만 아니라 살인죄의 실현을 위한 준비행 위를 하였음을 인정할 수 있다는 이유로 살인예비죄의 성립을 인정하였다.”

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

## 214. `art255_sec2_1.preparation_definition`

- proposition: 예비는 범죄실현을 위한 준비행위로서 아직 실행의 착수에 이르지 않은 일체의 행위를 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실행의 착수 전 단계인지 여부의 구체적 포섭에는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.1_1` / `Ⅱ.1`: “예비란 범죄실현을 위한 준비행위로서 아직 실행의 착수에 이르지 않은 일체의 행위를 말한다.”

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

## 215. `art255_sec2_1.preparation_external_act`

- proposition: 살인예비에는 단순한 범죄실현 의사나 계획 외에 객관적으로 실행행위를 가능하게 하거나 용이하게 하는 준비행위가 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 단순 의사·계획과 객관적 준비행위를 구별하는 요소 카드다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.1_1` / `Ⅱ.1`: “단순히 범죄를 실현할 의사나 계획만으로는 부 족하고 객관적으로 실행행위를 가능하게 하거나 용이하게 하는 준비행위가 있어 야 한다.”

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

## 216. `art255_sec2_1.preparation_substantial_contribution`

- proposition: 소개된 판례에 따르면 준비행위는 물적인 것에 한정되거나 특별한 정형을 가질 필요는 없지만, 객관적으로 살인죄 실현에 실질적으로 기여할 수 있는 외적 행위여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: ‘실질적으로 기여’하는지 여부는 평가적 판단을 요하며, 소개된 판시의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.1_1` / `Ⅱ.1`: “위와 같은 준비행위는 물적인 것에 한정되지 아니하며 특별한 정형이 있는 것도 아니지만, 단순히 범행의 의사 또는 계획만으로는 그것이 있다고 할 수 없 고 객관적으로 보아서 살인죄의 실현에 실질적으로 기여할 수 있는 외적 행위를 필요로 한다고 판시하였다.”

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

## 217. `art255_sec2_1.sickle_execution_commencement_boundary`

- proposition: 소개된 사례에서 피고인이 낫을 들고 피해자에게 접근한 행위는 살인의 실행행위 착수로 인정되어 살인예비가 아니라 살인미수에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 낫을 들고 피해자에게 접근한 구체적 사례의 예비 단계 부정 경계로서 보존하며, 다른 접근행위에 기계적으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.1_1` / `Ⅱ.1`: “피고인이 낫을 들고 피해자에게 접근함으로써 살인의 실행행위에 착수하였다고 할 것이 므로 이는 살인미수에 해당한다.”

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

## 218. `art255_sec2_2.conspiracy_agreement_required`

- proposition: 합의에 이르지 않은 단순한 범죄의사의 표명이나 교환만으로는 음모가 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실제 합의 없이 의사만 표명하거나 교환한 경우를 음모 성립에서 배제하는 한정이다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.2_2` / `Ⅱ.2`: “합 의를 이루지 않은 이상 단순한 범죄의사의 표명이나 교환으로는 음모라고 할 수 없다.”

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

## 219. `art255_sec2_2.conspiracy_definition`

- proposition: 음모는 2인 이상의 사람 사이에 성립하는 범죄실행의 합의이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 음모의 정의상 당사자 수와 범죄실행 합의의 존재를 확인하는 기본 관계다.
- bounded sources:

  - `comm_001692_제255조_Ⅱ.2_2` / `Ⅱ.2`: “음모란 2인 이상의 사람 사이에 성립하는 범죄실행의 합의를 말한다.”

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

## 220. `art255_sec3.conditional_murder_purpose`

- proposition: 살해를 일정 사태 발생과 연관시키는 조건부 목적도 살인예비·음모죄의 목적이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 조건부 목적이 구체적 살인의 목적에 해당하는지는 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “살해를 일정한 사태 발생과 연관시키는 조건부 목적이라도 무방하다.”

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

## 221. `art255_sec3.murder_purpose`

- proposition: 살인예비·음모죄에는 살인죄, 존속살해죄 또는 위계·위력에 의한 살인죄를 범할 목적이 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 범행 목적의 존재는 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “살인예비·음모죄가 성립하기 위해서는 주관적 구성요건으로 살인죄, 존속살해죄 또는 위계·위력에 의한 살인죄를 범할 목적이 있어야 한다.”

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

## 222. `art255_sec3.online_murder_notice_insufficient`

- proposition: 인터넷에 살인 범행 예고 내용을 게시한 사정만으로는 당연히 살인예비·음모죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인터넷 게시 외에 목적, 대상자의 구체성, 준비행위 및 준비 고의에 관한 사실을 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “이와 같은 살인 범행을 예고하는 내용을 인터넷에 게시한 경우 그 사정만으로 당연히 본죄에 해당한다고 할 수는 없다.”

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

## 223. `art255_sec3.preparation_intent`

- proposition: 살인예비죄에는 살인죄를 범할 목적 외에 살인의 준비에 관한 고의가 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 살인의 준비에 관한 고의는 개별 행위와 정황에 따라 평가가 필요하다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “살인예비죄가 성립하기 위하여는 형법 제255조 에서 명문으로 요구하는 살인죄를 범할 목적 외에도, 살인의 준비에 관한 고의 가 있어야 한다.”

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

## 224. `art255_sec3.specific_target_requirement`

- proposition: 살인예비·음모가 되려면 시기가 미정이더라도 적어도 살해 대상자가 구체적으로 확정된 상태에서의 준비행위여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 대상자의 구체적 확정 여부는 개별 준비행위와 정황을 평가하여 검토한다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “적어도 살해할 대상자가 누구인지는 구체적으로 확정되어 있는 사정 하에서의 준비행위만이 살인예비·음모에 해당할 수 있다.”

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

## 225. `art255_sec3.undetermined_target_negative_holding`

- proposition: 간첩이 간첩행동을 저해하는 자를 살해할 의도로 권총을 휴대하고 남하하였더라도 살해대상 인물이 결정되지 않은 경우 살인예비죄로 처단할 수 없다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문과 사실관계를 사용자 제공 1차 판례 색인으로 확인하기 전에는 commentary-reported precedent로만 취급한다.
- bounded sources:

  - `comm_001692_제255조_Ⅲ_3` / `Ⅲ`: “살해대상인물이 결정되지 않은 이상 살인예비죄로 처단할 수 없다고 본다.”

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
