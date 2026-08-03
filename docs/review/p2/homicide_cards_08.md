# 살인·존속살해 RuleIR 카드 검수 8

- unit: `homicide`
- articles: art250, art254, art255
- cards: 106–120 / 242
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

## 106. `art250_sec1_19.conspiracy_definition`

- proposition: 공모는 일정한 법정 형식을 요구하지 않고, 2인 이상이 범죄에 공동가공하여 실현하려는 의사의 결합이 있으면 성립하며, 전체 모의 과정이 없어도 순차적 또는 암묵적 의사 결합으로 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 암묵적 의사결합의 인정은 정황 평가를 요한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_87` / `Ⅰ.19`: “공모는 법률상 어떤 정형을 요구하는 것이 아니고 2인 이상이 공모하여 범죄에 공동 가공하여 범죄를 실현하려는 의사의 결합만 있으면 된다. 비록 전체적인 모의과 정이 없었더라도 여러 사람 사이에 순차적으로 또는 암묵적으로 상통하여 그 의사의 결합이 이루어지면 공모관계가 성립한다.”

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

## 107. `art250_sec1_19.conspiracy_joint_principal_functional_control`

- proposition: 구성요건행위를 직접 분담하지 않은 공모자도 전체 범죄에서의 지위·역할 및 범죄경과에 대한 지배·장악력 등에 비추어 본질적 기여를 통한 기능적 행위지배가 인정되면 공모공동정범이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 본질적 기여와 기능적 행위지배는 평가적 판단사항이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_87` / `Ⅰ.19`: “구성요건행위를 직접 분담하여 실행하지 아 니한 공모자가 공모공동정범으로 인정되기 위하여는, 전체 범죄에 있어서 그가 차지하는 지위·역할이나 범죄경과에 대한 지배 내지 장악력 등을 종합하여 그 가 단순한 공모자에 그치는 것이 아니라 범죄에 대한 본질적 기여를 통한 기능 적 행위지배가 존재하는 것으로 인정되어야 한다.”

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

## 108. `art250_sec1_19.conspiracy_liability`

- proposition: 공모가 이루어진 경우 실행행위에 직접 관여하지 않은 사람도 다른 공모자의 행위에 대하여 공동정범으로서 형사책임을 진다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 적용 전 유효한 공모관계와 공동정범 요건을 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_88` / `Ⅰ.19`: “이와 같은 공모가 이루어진 이 상, 실행행위에 직접 관여하지 않은 사람도 다른 공모자의 행위에 대하여 공동 정범으로서 형사적 책임을 진다.”

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

## 109. `art250_sec1_19.instigated_injury_instead_of_murder`

- proposition: 살인을 교사하였으나 피교사자가 상해행위만 한 경우 교사자는 상해죄의 교사범이 되는 동시에 교사의 미수에 해당하며, 상상적 경합으로 더 무거운 살인예비·음모죄로 처벌한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피교사자가 실제 실행한 상해행위의 범위와 경합 관계를 확인한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “살인을 교사하였는데 피교사자가 상해행위만 한 경우, 교사자는 피교사자가 실”
  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “행한 범위에서 책임을 지기 때문에 상해죄의 교사범이 되는 것은 물론이지만, 형법 제31조 제2항이 정하는 ‘교사의 미수’에도 해당하고 양자는 상상적 경합 관”
  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “계에 있으므로, 형이 더 무거운 살인예비·음모죄에 의하여 처벌하여야 한다.”

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

## 110. `art250_sec1_19.instigation_indirect_facts_proof`

- proposition: 피고인이 교사사실을 부인하면 교사사실과 상당한 관련성이 있는 간접사실을 증명하는 방법으로 이를 증명할 수 있고, 관련 간접사실인지는 경험칙에 바탕을 둔 합리적 판단으로 정한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간접사실의 상당한 관련성은 경험칙에 따른 평가를 요한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “피고인이 교사사실을 부인하는 경우, 사물의 성질”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “상 그와 상당한 관련성이 있는 간접사실을 증명하는 방법에 의하여 이를 증명”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “무엇이 상당한 관련성이 있는 간접사실에 해당할 것인”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “가는 정상적인 경험칙에 바탕을 두고 치밀한 관찰력이나 분석력에 의하여 사실”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “의 연결 상태를 합리적으로 판단하는 방법에 의해야 한다.”

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

## 111. `art250_sec1_19.instigation_murder_completed`

- proposition: 살인의사가 없던 사람을 교사하여 살인을 결의하게 하고 피교사자가 살인죄를 범한 경우 살인교사죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 교사로 인한 결의 형성과 피교사자의 실행 여부를 확인한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “살인을 할 의사가 없던 사람을 교사하여 살인을 결의하게 하고 나아가 피교사자”
  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “가 살인죄를 범한 경우 살인교사죄가 성립한다.”

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

## 112. `art250_sec1_19.instigation_no_execution`

- proposition: 피교사자가 살인을 승낙하지 않았거나 승낙하였더라도 실행의 착수에 이르지 않은 경우, 교사자는 살인예비·음모죄에 준하여 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피교사자의 승낙 및 실행착수 여부를 확인한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_93` / `Ⅰ.19`: “자가 살인을 승낙하지 않았거나, 승낙하기는 하였지만 실행의 착수에 이르지 않은 경우 교사자는 살인예비·음모죄에 준하여 처벌된다.”

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

## 113. `art250_sec1_19.instigation_strict_proof`

- proposition: 살인의 교사 사실은 범죄사실을 구성하므로 이를 인정하려면 엄격한 증명이 요구된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 교사 사실을 구성하는 증거의 엄격한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “살인의 ‘교사’ 사실은 범죄사실을 구성하는 것으로서 이를 인정하기 위해서는 엄”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “격한 증명이 요구된다.”

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

## 114. `art250_sec1_19.joint_principal_charge_aiding_conviction`

- proposition: 공동정범으로 기소된 범죄사실도 공소사실 동일성 범위에서 더 가벼운 방조사실이 인정되고 피고인의 방어에 실질적 불이익이 없다면, 공소장 변경 없이 직권으로 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공소사실 동일성과 방어상 실질적 불이익 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_97` / `Ⅰ.19`: “피고인의 방어에 실질적 불이익을 주지 않는다면 공소장 변경 없이 직권으”
  - `comm_001692_제250조_Ⅰ.19_97` / `Ⅰ.19`: “로 공동정범으로 기소된 범죄사실을 방조사실로 인정할 수 있는 것이다.”

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

## 115. `art250_sec1_19.joint_principal_requirements`

- proposition: 살인 공동정범은 공동가공의 의사와 공동의사에 기한 기능적 행위지배를 통한 범죄 실행이라는 주관적·객관적 요건을 충족해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공동가공의사와 기능적 행위지배의 사실상 평가는 별도 법률검토가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_87` / `Ⅰ.19`: “공동정범이 성립하기 위해서는 주관적 요건으로서 공 동가공의 의사와 객관적 요건으로서 공동의사에 기한 기능적 행위지배를 통한 범죄의 실행사실이 필요하다.”

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

## 116. `art250_sec1_19.joint_processing_intent_insufficient_acquiescence`

- proposition: 공동가공의 의사는 타인의 범행을 인식하면서 이를 제지하지 않고 용인하는 것만으로는 부족하고, 공동의 의사로 특정 범죄행위를 하기 위한 일체성과 상호 이용의 관계를 내용으로 해야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 단순 용인과 공동가공의사의 구별은 구체적 사실관계 평가를 요한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_87` / `Ⅰ.19`: “공동가공의 의사는 타인의 범행을 인식하면서도 이를 제지하지 아니하고 용인하는 것만으로는 부족하고, 공동의 의사로 특정한 범죄행위를 하기 위해 일체가 되어 서로 다른 사람의 행위를 이용하여 자기의 의사를 실행에 옮기는 것을 내용으로 하는 것이어야 한다.”

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

## 117. `art250_sec1_19.military_beating_case`

- proposition: 피해자 사망을 예견한 계속 폭행 사건에서, 주범과 비교하여 폭행 정도·횟수가 현저히 적고 사망 결과를 용인할 동기나 위험한 행위태양이 부족하며 피해자 구조를 시도한 B·C·D에 대해서는 살인의 고의 및 공동정범 법리 오해를 이유로 살인죄 인정 원심을 파기환송한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 사례의 사실관계에 한정된 reported precedent이며 원판결 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_90` / `Ⅰ.19`: “대법원은 피고인 A의 살인죄를 인정한 반면, 피고인 B, C, D 부분에 대해서는 살인죄의 고의와 공동정범에 관한 법리 오해 등을 이유로 삼아, 살인죄를 인정 한 원심판결을 파기환송하였다.”
  - `comm_001692_제250조_Ⅰ.19_91` / `Ⅰ.19`: “피고인 B, C, D는 피해자가 쓰러지자 더 이상의 폭행을 중단하고 피해자에게 물을 먹이려 하거나 오줌에 젖은 속옷을 갈아입히고 나아가 피고인 A의 폭행을 적극적으로 제지하기까지 하였다.”

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

## 118. `art250_sec1_19.omission_aiding_child_abuse_homicide`

- proposition: 공동정범의 공동가공의사와 기능적 행위지배가 인정되기 어려운 부모라도, 다른 부모의 구타로 자녀가 사망할 위험을 예견하면서 보호·양육의무를 이행하지 않고 구타를 제지하지 않아 살인을 용이하게 한 경우 살인방조 책임이 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보호·양육의무, 사망 위험 예견 및 부작위의 용이화 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_98` / `Ⅰ.19`: “피고인 丙은 피고인 ⼄의 구타행위로 甲이 사망할 가능성 내지 위험이 있음을 예견하면서도, 민법 제913조 및 아동복지법 제5조에 따른 보호·양육의무를 다하지 않은 채 피고인 ⼄의 구타행위를 제지하지 않고 용인하는 부작위 등을 통하여 피고인 ⼄의 살”
  - `comm_001692_제250조_Ⅰ.19_98` / `Ⅰ.19`: “인 범행을 방조하였다고 보아, 피고인 丙에게 살인방조의 책임을 인정하였다.”

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

## 119. `art250_sec1_19.robbery_murder_shared_intent`

- proposition: 강도살인죄 공동정범의 성립에는 강도 부분뿐 아니라 살인 부분에 관한 고의의 공동이 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 살인 부분에 관한 고의 공동의 증거를 독립적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_90` / `Ⅰ.19`: “강도살인죄는 고의범이므로 강 도살인죄의 공동정범이 성립하기 위하여는 강도의 점 뿐 아니라 살인의 점에 관한 고의의 공동이 필요하다.”

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

## 120. `art250_sec1_19.school_murder_conspiracy_evidence`

- proposition: 실제 살인을 실행하지 않은 A에 대하여 공범 B 진술의 신빙성이 부족하고 대화에 구체적 범행공모를 인정할 증거가 부족한 인천 초등생 살해사건에서, A가 살인 실행 가능성을 진지하게 인식하고 지시·공모했다고 보기 어렵다는 원심 판단을 대법원이 수긍한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 증거평가 사례이므로 원판결 및 구체적 증거관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_92` / `Ⅰ.19`: “이 사건 범행을 공모하였다고 볼 만한 정도의 구체성을 가진 대화가 이뤄졌다고 볼 증거가 부족하다는 사정 등을 들어 피고인들이 이 사건 범행 당일 새벽까지 대화 를 나눌 때까지는 피고인 A가 피고인 B의 실제 살인 범행 실행에 대한 가능성을 진지하게 인식하면서 이를 지시하거나 범행계획을 모의하는 등의 방법으로 공모하 였다고 보기 어렵다고 판단하였다. 대법원은 그와 같은 원심의 판단을 수긍하였다.”

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
