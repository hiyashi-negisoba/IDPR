# 살인·존속살해 RuleIR 카드 검수 6

- unit: `homicide`
- articles: art250, art254, art255
- cards: 76–90 / 242
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

## 76. `art250_sec1_16.defensive_counterattack`

- proposition: 정당방위의 방어행위에는 순수한 수비적 방어뿐 아니라 적극적 반격을 포함하는 반격방어도 포함되지만, 자기 또는 타인의 법익침해 방위를 위한 상당한 이유가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 적극적 반격이 방어행위인지와 상당한 이유의 유무는 사실관계 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_70` / `Ⅰ.16`: “정당방위의 성립요건으로서의 방어행위에는 순수한 수비적 방어뿐 아니라 적 극적 반격을 포함하는 반격방어의 형태도 포함되나, 그 방어행위는 자기 또는 타인의 법익침해를 방위하기 위한 행위로서 상당한 이유가 있어야 한다.”

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

## 77. `art250_sec1_16.domestic_violence_killing`

- proposition: 지속적 가정폭력과 살해 위협이 있었더라도 도피 또는 일시적 회피 가능성이 있고, 피해자가 앉아 작업 중인 뒤에서 노끈으로 목을 졸라 살해한 경우 정당방위, 사회상규상 허용행위 및 공포·경악·흥분·당황에 의한 과잉방위는 인정되기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 지속적 가정폭력 상황의 구체적 시간적 위험과 회피 가능성에 한정된 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_77` / `Ⅰ.16`: “피고인의 행위는 자신의 생명 또는 신체에 대한 현재의 부당한 침해를 방위하”
  - `comm_001692_제250조_Ⅰ.16_77` / `Ⅰ.16`: “기 위한 행위로서 사회통념상 상당성을 인정하기는 어렵다.”
  - `comm_001692_제250조_Ⅰ.16_77` / `Ⅰ.16`: “피고인이 피해자를 살해한 행위가 피해자의 가정폭력으로부터 자신을 보호하기 위한 정당방위에 해당한다거나 사회상규에 반하지 않는 행위라고 보”

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

## 78. `art250_sec1_16.excessive_defense_continuous_act`

- proposition: 현재의 부당한 침해에 대한 최초 방위는 상당하였더라도 침해 계속이 불가능하거나 현저히 곤란해진 뒤 목을 계속 졸라 사망하게 한 경우, 연속된 전후행위를 하나로 보아 과잉방위에 해당할 수 있다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 침해 지속 가능성과 연속 행위의 평가에 관한 좁은 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_73` / `Ⅰ.16`: “피고인 甲의 위와 같 은 방위행위로 말미암아 뒤로 넘어져 피고인 甲의 몸 아래 깔려 더 이상 침해행 위를 계속하는 것이 불가능하거나 또는 적어도 현저히 곤란한 상태에 빠졌음에 도 피고인 甲이 A의 몸 위에 타고앉아 그의 목을 계속하여 졸라 누름으로써 결 국 A로 하여금 질식하여 사망에 이르게 한 행위는 정당방위의 요건인 상당성 을 결여한 행위”
  - `comm_001692_제250조_Ⅰ.16_73` / `Ⅰ.16`: “방위의사에서 비롯된 피고인 甲의 위와 같이 연속된 전후행위는 하나 로서 형법 제21조 제2항 소정의 과잉방위에 해당한다”

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

## 79. `art250_sec1_16.mutual_fight`

- proposition: 서로 공격할 의사로 싸우다가 상대방의 선제공격에 대항한 행위는 방위행위와 공격행위 성격을 함께 가지므로 정당방위 또는 과잉방위가 성립할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 상호 공격 의사와 대응행위의 공격성은 구체적 사실로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_70` / `Ⅰ.16`: “서로 공격할 의사로 싸우다가 상대방으로부터 먼저 공격을 받고 이 에 대항하여 가해한 행위는 방위행위인 동시에 공격행위의 성격을 가지므로, 정 당방위 또는 과잉방위가 성립될 수 없다.”

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

## 80. `art250_sec1_16.mutual_fight_excessive_weapon`

- proposition: 격투 중 상대방 공격이 통상 예상 범위를 넘어 살인의 흉기 등을 사용한 경우에는 부당한 침해가 되어 정당방위가 허용될 수 있다는 대법원 법리가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 대법원 법리이므로 원판결 확인 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_71` / `Ⅰ.16`: “격투를 하는 자 중의 한 사람의 공격이 그 격투에서 당연히 예상을 할 수 있는 정도를 초과하여 살인의 흉기 등을 사용하 여 온 경우에는 이는 역시 부당한 침해라고 아니할 수 없으므로, 이에 대하여는 정당방위를 허용하여야 한다.”

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

## 81. `art250_sec1_16.necessity_defense_life`

- proposition: 살인죄에서는 원칙적으로 긴급피난으로 위법성이 조각되지 않으며, 다수 생명을 구하기 위한 소수 살해도 긴급피난으로 정당화될 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 살인 상황에서 긴급피난 정당화의 원칙적 배제를 검토하는 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_69` / `Ⅰ.16`: “본죄에서는, 원칙적으로 긴급피난에 의해 위법성이 조각되지 (형법 제22조) 않는다.”
  - `comm_001692_제250조_Ⅰ.16_69` / `Ⅰ.16`: “다수인의 생명을 구하기 위하여 소수의 사 람들을 살해하는 것도 긴급피난에 의하여 정당화될 수 없다.”

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

## 82. `art250_sec1_16.planned_killing_not_self_defense`

- proposition: 계획·준비하여 반항하기 어려운 피해자를 심장에 찔러 살해한 행위는 사회통념상 상당성을 인정하기 어려워 정당방위행위로 평가될 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 계획성, 피해자의 반항 가능성 및 공격 방법에 한정된 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_74` / `Ⅰ.16`: “피고인들이 사전에 공모하여 범행을 준비하고, 술에 취하여 잠들어 있는 피해 자의 양팔을 눌러 꼼짝 못하게 한 후 피해자를 깨워 피해자가 제대로 반항할 수 없는 상태에서 식칼로 피해자의 심장을 찔러 살해한다는 것은, 당시의 상황에 비추어도 사회통념상 상당성을 인정하기가 어렵다고 하지 않을 수 없고”
  - `comm_001692_제250조_Ⅰ.16_74` / `Ⅰ.16`: “피고인들의 행위가 위 (중략) 에서 본 바와 같이 그 상당성을 결여한 것인 이상 정당방위행위로 평가될 수는 없는 것이므로”

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

## 83. `art250_sec1_16.self_defense_social_adequacy`

- proposition: 정당방위가 성립하려면 침해와 방위로 침해되는 법익의 종류·정도, 침해 방법, 침해의 완급 등 구체적 사정을 참작하여 방위행위가 사회적으로 상당해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 방위행위의 상당성은 구체적 사정에 관한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_70` / `Ⅰ.16`: “침해행위에 의하여 침해되는 법익의 종류, 정도, 침해의 방법, 침해행위의 완 급과 방위행위에 의하여 침해될 법익의 종류, 정도 등 일체의 구체적 사정들을 참작하여 방위행위가 사회적으로 상당한 것이어야 한다.”

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

## 84. `art250_sec1_16.stabbing_after_assault`

- proposition: 피해자로부터 폭행·협박을 받았더라도 그 정도에 비추어 칼로 찔러 사망하게 한 행위가 방위행위의 한도를 넘고 사회통념상 용인될 수 없으면 정당방위 또는 과잉방위가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박의 정도와 치명적 대응의 비례성에 한정된 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_75` / `Ⅰ.16`: “피해자의 폭행·협박의 정도에 비추어 피고인이 칼로 피해자를 찔러 즉”
  - `comm_001692_제250조_Ⅰ.16_75` / `Ⅰ.16`: “하게 한 행위는 피해자의 폭력으로부터 자신을 보호하기 위한 방위행위로서의 한도를 넘어선 것”

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

## 85. `art250_sec1_16.victim_consent`

- proposition: 살인죄에서 피해자의 승낙은 위법성을 조각하지 않고 형벌 감경의 효과에 그친다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 피해자 승낙의 효과를 위법성조각이 아닌 형벌 감경으로 구분하는 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.16_69` / `Ⅰ.16`: “피해자의 승낙은 (형법 제252조 제1항) 위법성을 조각시키는 게 아니라, 단지 형벌을 감경시켜 주는 효과에 그친다.”

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

## 86. `art250_sec1_17.advance_directive_life_sustaining_treatment`

- proposition: 회복불가능한 사망 단계에 대비한 사전의료지시가 있고 환자의 의사 변경 특별사정이 없으면, 진료 중단 시점에 직접 자기결정권을 행사하지 않았더라도 사전의료지시에 의한 자기결정권 행사로 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사전의료지시의 존재, 내용, 유효성 및 의사 변경 특별사정 여부에 대한 증거 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “사전의료지시를 한 후 환자의 의사가 바뀌었다고 볼 만한 특별한 사정이 없는 한 사전의료지시에 의하여 자기결정권을 행사한 것으로 인”
  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “정할 수 있다.”

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

## 87. `art250_sec1_17.life_sustaining_treatment_withdrawal`

- proposition: 회복불가능한 사망 단계에 이른 환자가 존엄·가치 및 행복추구권에 기초한 자기결정권을 행사한 것으로 인정되면, 특별한 사정이 없는 한 연명치료 중단이 허용될 수 있으며, 해당 단계 여부는 전문의 의학적 소견을 종합하여 신중히 판단해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 보고한 연명치료 중단 기준이다. 회복불가능한 사망 단계와 자기결정권 행사는 개별 의료기록에 대한 평가를 요구한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_81` / `Ⅰ.17`: “복불가능한 사망의 단계에 이른 후에 환자가 인간으로서의 존엄과 가치 및 행”
  - `comm_001692_제250조_Ⅰ.17_81` / `Ⅰ.17`: “복추구권에 기초하여 자기결정권을 행사하는 것으로 인정되는 경우에는 특별한 사정이 없는 한 연명치료의 중단이 허용될 수 있다.”
  - `comm_001692_제250조_Ⅰ.17_81` / `Ⅰ.17`: “환자가 회복불가능한 사망의 단계에 이르렀는지 여부는 주치의의 소견뿐 아니라 사실조회, 진료기록 감정 등에 나타난 다른 전문의사의 의학적 소견을 종합하여 신중하게 판단하여”

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

## 88. `art250_sec1_17.presumed_will_life_sustaining_treatment`

- proposition: 사전의료지시 없이 회복불가능한 사망 단계에 진입한 경우에도, 환자의 평소 가치관·신념상 중단이 객관적으로 최선의 이익에 부합하여 환자가 중단을 선택했을 것으로 볼 수 있으면 중단에 관한 의사를 추정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 환자의 추정 의사는 평소 가치관·신념 및 객관적 최선의 이익에 관한 사실 평가를 전제로 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “환자의 평소 가치”
  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “관이나 신념 등에 비추어 연명치료를 중단하는 것이 객관적으로 환자의 최선의 이익에 부합한다고 인정되어 환자에게 자기결정권을 행사할 수 있는 기회가 주”
  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “어지더라도 연명치료의 중단을 선택하였을 것이라고 볼 수 있는 경우에는, 그 연명치료 중단에 관한 환자의 의사를 추정할 수 있다고 인정하는 것이 합리적”
  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “이고 사회상규에 부합된다.”

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

## 89. `art250_sec1_17.statutory_life_sustaining_treatment_exception`

- proposition: 연명의료결정 관련 법률의 요건과 절차에 따라 행해진 연명의료중단시술은 형법 제20조의 법령에 의한 행위로서 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 법률의 구체적 적용 요건과 절차 충족 여부를 확인해야 한다. 현재 source scope에는 해당 연명의료결정 관련 법률의 원문이 포함되어 있지 않다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “이 법률상 요건과 절차에 따라 행해진 안락사시술”
  - `comm_001692_제250조_Ⅰ.17_82` / `Ⅰ.17`: “은 형법 제20조의 ‘법령에 의한 행위’로서 그 위법성이 조각된다.”

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

## 90. `art250_sec1_17.supreme_court_active_euthanasia`

- proposition: 대법원 1957. 7. 26. 선고 4290형상126 판결은 안락사가 되지 않는다는 취지로 판단하였다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 보고한 판례 취지일 뿐 판결 원문은 현재 source scope에 없다. 적극적·직접적 안락사에 대한 적용 범위는 원문 대조가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_80` / `Ⅰ.17`: “대법원 1957. 7. 26. 선고 4290형상126 판결은”
  - `comm_001692_제250조_Ⅰ.17_80` / `Ⅰ.17`: “안락사가 되지 않는다는 취지로 판단하였다”

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
