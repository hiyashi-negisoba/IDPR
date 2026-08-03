# 살인·존속살해 RuleIR 카드 검수 5

- unit: `homicide`
- articles: art250, art254, art255
- cards: 61–75 / 242
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

## 61. `art250_sec1_15.object_error`

- proposition: 구체적 사실의 착오 중 객체의 착오는 발생한 결과에 대한 고의 성립에 영향을 미치지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 객체의 착오의 효과를 정리한 해설상 명제다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_66` / `Ⅰ.15`: “구체적 사실의 착오인 경우에 객체의 착오 는 발생한 결과에 대한 고의의 성립에 영향이 없”

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

## 62. `art250_sec1_15.omission_intent_inference`

- proposition: 부진정부작위범의 작위의무자에게 고의가 있었는지는 진술만이 아니라 작위의무 발생근거, 법익침해의 태양·위험성, 사태지배 정도, 요구된 작위의무와 이행 용이성, 부작위 동기·경위·형태 및 결과와의 상관관계 등을 종합하여 추인한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 부작위 고의의 추인에 필요한 종합 판단 요소다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_65` / `Ⅰ.15`: “작위의무의 발생근거, 법익침해의 태양과 위험성, 작위의무자의 법익침해에 대한 사태지배의 정도, 요구되는 작위의무의 내용과 그 이행의 용이성, 부작위에 이르게 된 동기와 경위, 부작위의 형태와 결 과발생 사이의 상관관계 등을 종합적으로 고려하여 작위의무자의 심리상태를 추인하여야 할 것이다.”

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

## 63. `art250_sec1_15.omission_intent_requirements`

- proposition: 부진정부작위범의 고의는 결과발생 방지를 위한 법적 작위의무자가 의무 이행으로 결과를 쉽게 방지할 수 있음을 예견하고도 결과발생을 용인·방관하면서 의무를 이행하지 않는다는 인식이 있으면 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 부진정부작위범의 고의 요건에 관한 보고된 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_65` / `Ⅰ.15`: “법익침해의 결과발생 을 방지할 법적 작위의무를 가지고 있는 자가 그 의무를 이행함으로써 그 결과 발생을 쉽게 방지할 수 있었음을 예견하고도 결과발생을 용인하고 이를 방관한 채 그 의무를 이행하지 아니한다는 인식을 하면 족하며”

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

## 64. `art250_sec1_15.pillow_suffocation_robbery_murder`

- proposition: 도망하려는 피해자를 침대에 엎드리게 한 뒤 베개로 약 3분간 머리를 누르고, 피해자가 움직임을 멈춘 뒤에도 계속 누른 후 사망을 확인한 사안에서는 단순 위협 목적이 아니라 살해의 고의를 인정하여 강도살인 유죄를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 베개로 장시간 압박한 강도살인 사안의 보고된 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “고인이 단순히 위협할 목적으로 피해자의 몸을 누르고 있었다고 볼 수는 없고, 살해의 고의가 있었다고 판단하여 강도살인의 공소사실을 유죄로 인정한 원심은 정당하며”

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

## 65. `art250_sec1_15.prolonged_assault_child`

- proposition: 7세 아동을 장시간 무차별적으로 폭행하여 사망하게 한 울산계모 사건에서, 폭행 강도·부위·시간·피해아동의 취약성 및 생명위험 인식 등을 종합하여 미필적 살인의 고의를 인정하고 살인죄로 의율한 항소심 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 울산계모 사건으로 소개된 항소심의 구체적 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_59` / `Ⅰ.15`: ““피고인이 이 사건 폭행과정에서 피해자의 사망”
  - `comm_001692_제250조_Ⅰ.15_59` / `Ⅰ.15`: “이라는 결과 발생을 충분히 인식 또는 예견하였고, 나아가 미필적으로나마 그 결과 발생을 용인하였다.”고 판단하였다.”

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

## 66. `art250_sec1_15.repeated_head_assault_wood_stones`

- proposition: 말목과 돌로 피해자의 머리를 반복하여 구타해 사망하게 한 경우, 범행이 우발적이더라도 살인의 결과발생을 인식한 살인의 범의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 말목과 돌을 이용한 반복 두부 구타 사안의 보고된 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “위 범행이 우발적이라 할지라도 살인의 결과발생을 인”
  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “식하고 저지른 소행으로서 살인의 범의가 있었다고 봄이 상당하다.”

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

## 67. `art250_sec1_15.repeated_stabbing_nonvital_areas`

- proposition: 치명적 부위가 아닌 허벅지나 종아리 등을 주로 찔렀더라도 칼로 약 20회 힘껏 찔러 과다실혈로 사망하게 한 경우 살인의 미필적 고의를 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 반복 찌르기 및 과다실혈 사망이라는 구체적 사례의 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_55` / `Ⅰ.15`: “칼로 피해자를 20여 회나 힘껏 찔러 그로 인하여 피해자가 과다 실혈로 사망하게 된 이 상, 피고인 A, B가 자기들의 가해행위로 인하여 피해자가 사망할 수도 있다는 사실 을 인식하지 못하였다고는 볼 수 없다. 오히려 살인의 미필적 고의가 있었다고 볼 수 있을 뿐”

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

## 68. `art250_sec1_15.single_punch_kick_no_murder_intent`

- proposition: 경찰관을 피하려고 복부를 한 차례 때리고 발로 차 차량에서 추락시켜 사망하게 한 사실만으로는 살해 결의를 속단할 수 없으므로, 살인죄가 아니라 상해치사죄로 처단해야 한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 차량에서 추락한 피해자 사망의 구체적 상해치사 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_63` / `Ⅰ.15`: “위 사실만으로는 가해자가 피해자를 살해할 것을 결의하였다고 속단할 수 없는 것이므로, 결국 이러한 경우에 가해”
  - `comm_001692_제250조_Ⅰ.15_63` / `Ⅰ.15`: “자는 상해치사죄로 처단할 것이고 살인죄로 처단할 것이 아니라고 보았다.”

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

## 69. `art250_sec1_15.strangulation_vulnerable_victim`

- proposition: 건장한 군인이 왜소한 피해자의 급소인 목을 15~20초간 강하게 졸라 설골이 부러질 정도의 폭력을 행사한 경우 최소한 살인의 미필적 고의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 취약성과 목 졸림의 강도에 관한 좁은 사례 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “이러한 폭력의 태양 및 정도에 비추어 보면, 이 사건 범행 당시 피고인에게 최소한 살인의 미필적 고의는 있었다고 판단하”
  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “여 이 사건 살인의 공소사실을 유죄로 인정한 원심 판단은 정당하고”

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

## 70. `art250_sec1_15.unforeseen_cooffender_murder`

- proposition: 공동 폭행의 피고인들이 가벼운 상해 또는 폭행만을 의도했고 공동피고인의 살인행위가 전혀 예기치 못한 경우, 나머지 피고인들에게 공동피고인의 살인행위 책임을 물을 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 예기치 못한 공동피고인의 살인행위에 관한 책임 제한 사례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_62` / `Ⅰ.15`: “공동피고인 甲의 살인 등 소위는 피고인 등이 전연 예기치 않은 바로서 공동피고인의 살인 등 소위에 대하여 피고인 등에게 그 책임을 물을 수”

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

## 71. `art250_sec1_15.vehicle_hammer_attack_acquittal`

- proposition: 임대차 분쟁 상대방을 향해 차량을 진행시키고 쇠망치를 휘두른 사안에서, 차량 속도가 높지 않고 머리를 조준해 가격했다고 보기 어려우며 피고인이 살해 결의를 했다고 단정하기 어려운 경우 살인미수는 무죄로 판단할 수 있다는 항소심 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 차량과 쇠망치 사용 사안에서 살인미수 무죄를 지지한 항소심 소개다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_64` / `Ⅰ.15`: “항소심법원 역시 다음과 같은 사정 등을 들어 이 부분을”
  - `comm_001692_제250조_Ⅰ.15_64` / `Ⅰ.15`: “무죄로 판단한 원심의 판단을 지지하면서 검사의 이 부분 항소를 배척하였다.”

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

## 72. `art250_sec1_15.vital_area_knife_attempt`

- proposition: 사람의 생명을 쉽게 빼앗을 수 있는 과도로 생명과 직결되는 목 부위를 찌른 살인미수 사안에서, 흉기 소지 경위와 상해 부위를 고려하여 살인의 고의를 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 살인미수의 과도 및 목 부위 사안에 한정된 판례 소개다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_54` / `Ⅰ.15`: “범행의 수단이 사람의 생명을 쉽게 빼앗을 수 있는 과도인 점, 피고인이 과도를 소지하게 된 동기와 경위, 피해자 B의 상해 부위가 생명과 직 결되는 목 부위인 점 등을 고려하여 피고인에게 살인의 고의가 있었다고 인정 한 원심 판단을 수긍하였다.”

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

## 73. `art250_sec1_15.wooden_club_head_strike`

- proposition: 무게 7kg, 길이 153cm의 목재로 피해자의 머리를 상당한 강도로 타격하여 사망에 이르게 한 경우, 행위수단·부위·상해 및 사망원인에 비추어 살인의 미필적 고의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 목재로 머리를 타격한 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_56` / `Ⅰ.15`: “이와 같은 점을 고려”
  - `comm_001692_제250조_Ⅰ.15_56` / `Ⅰ.15`: “하여 보면 피고인에 대하여 최소한 살인의 미필적 고의가 있었다고 하는 원심”
  - `comm_001692_제250조_Ⅰ.15_56` / `Ⅰ.15`: “의 판단은 정당하다.”

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

## 74. `art250_sec1_16.child_danger_alternatives`

- proposition: 부부싸움 중 자녀에게 실제 생명·신체 위험을 초래할 만큼 위급한 상황이 아니고 비치명적 제지 또는 회피 수단이 있었는데 상대방의 목을 졸라 사망하게 한 경우, 과잉방위 또는 공포·경악·흥분·당황에 의한 과잉방위는 인정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 자녀에 대한 급박한 위험 및 대체 수단의 유무에 한정된 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_76` / `Ⅰ.16`: “실제 아들의 생명이나 신체에 위험을 초래할 만큼 위급한 상황에 이르렀다고 인정되지는 않”
  - `comm_001692_제250조_Ⅰ.16_76` / `Ⅰ.16`: “는데도 피해자의 목을 눌렀던 것”
  - `comm_001692_제250조_Ⅰ.16_76` / `Ⅰ.16`: “피고인의 과잉방위 주장은 이유 없다.”

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

## 75. `art250_sec1_16.defense_ends_after_subdual`

- proposition: 침입자가 저항·공격하지 못하고 도망하려 하여 부당한 침해가 종료한 뒤, 제압된 침입자를 계속 폭행하는 행위는 방위의사보다 공격의사가 지배적이고 사회통념상 상당성이 없어 정당방위가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 침해 종료, 제압 이후 행위 및 공격의사 우위에 관한 좁은 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_78` / `Ⅰ.16`: “그로써 피해자의 부당한 침해는 일단 종료한 상황이었다.”
  - `comm_001692_제250조_Ⅰ.16_78` / `Ⅰ.16`: “그를 일단 제압한 이후의 후속 가해행위는 법익침해로”
  - `comm_001692_제250조_Ⅰ.16_78` / `Ⅰ.16`: “부터 자신과 가족을 보호하고 그로부터 벗어나기 위한 방위의사를 상쇄할 정도”
  - `comm_001692_제250조_Ⅰ.16_78` / `Ⅰ.16`: “로 공격의사가 지배적이었다.”
  - `comm_001692_제250조_Ⅰ.16_78` / `Ⅰ.16`: “정당방위가 성립하지 않는다.”

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
