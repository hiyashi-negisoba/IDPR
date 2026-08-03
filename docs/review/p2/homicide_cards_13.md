# 살인·존속살해 RuleIR 카드 검수 13

- unit: `homicide`
- articles: art250, art254, art255
- cards: 181–195 / 242
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

## 181. `art250_sec1_7.poisoning_victim_statement_credibility`

- proposition: 맹독성 농약의 색깔·냄새, 용기의 상태, 피해자의 농약 경험 등에 비추어 피해자가 이를 음료수로 잘못 알고 마셨다는 진술을 쉽게 믿기 어려운 경우, 그 진술에 기초한 살인 유죄판단은 재검토되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자 진술의 신빙성은 농약의 외관·용기·피해자 경험 등 구체적 사정에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.7_19` / `Ⅰ.7`: “이를 음료수로 잘못 알고 마셨다는 피해자”
  - `comm_001692_제250조_Ⅰ.7_19` / `Ⅰ.7`: “의 진술은 선뜻 믿기 어렵다.”

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

## 182. `art250_sec1_8.death_time_integrated_assessment`

- proposition: 시반·시강·위 내용물에 의한 사망시간 추정의 개별적 의문만으로 전체의 종합적 증명력을 부인하고 제3자 범행가능성 배제 정황 및 다른 유죄 간접증거를 모두 배척하는 것은 심리미진 또는 논리와 경험의 법칙 위반이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사망시간 감정의 개별 의문과 다른 간접증거의 종합적 증명력은 함께 평가한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_26` / `Ⅰ.8`: “사망시간의 추정”
  - `comm_001692_제250조_Ⅰ.8_26` / `Ⅰ.8`: “을 위한 시반·시강 및 위 내용물의 감정이 갖는 개별적 의문점에 기해 그 전”
  - `comm_001692_제250조_Ⅰ.8_26` / `Ⅰ.8`: “체가 갖는 종합적 증명력을 부인하고, 제3자의 범행가능성을 배제할 수 있는 정”
  - `comm_001692_제250조_Ⅰ.8_26` / `Ⅰ.8`: “황증거 및 유죄에 관한 다른 간접증거들의 증명력을 모두 배척한 것이 심리미”
  - `comm_001692_제250조_Ⅰ.8_26` / `Ⅰ.8`: “진 내지 논리와 경험의 법칙을 위반했다는 이유이다.”

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

## 183. `art250_sec1_8.direct_and_circumstantial_evidence`

- proposition: 범죄사실은 직접증거만이 아니라 직접증거와 간접증거를 종합하여 논리와 경험의 법칙에 따라 증명되었다고 판단할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 직접증거와 간접증거의 종합 및 논리·경험칙 적용은 기록에 따른 법적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_28` / `Ⅰ.8`: “법관은 반드시 직접증거로 만 범죄사실에 대한 증명이 있는지를 판단하는 것은 아니고, 직접증거와 간접증 거를 종합적으로 고찰하여 논리와 경험의 법칙에 따라 범죄사실에 대한 증명이 있는 것으로 판단할 수 있다.”

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

## 184. `art250_sec1_8.financial_gain_motive_caution`

- proposition: 고의 교통사고에 의한 배우자 살해 여부가 문제된 사건에서, 고액 보험금 수령이 예상된다는 금전적 이유만으로 살해 동기를 인정해서는 안 되고 다른 간접사실의 증명 정도와 함께 면밀히 살펴야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 고의 교통사고에 의한 배우자 살해가 문제된 사안의 금전적 동기 평가에 관한 보고된 판례 기준으로 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “액의 보험금 수령이 예상된다는 금전적 이유만으로 살해 동기를 인정할 수 있”
  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “는지는 다른 간접사실들의 증명 정도와 함께 더욱 면밀히 살펴볼 필요가 있다.”

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

## 185. `art250_sec1_8.financial_motive_family_killing`

- proposition: 금전적 이득만으로 살인 동기가 수긍되려면 행위자가 절박한 경제적 곤란·궁박 상태에 있거나 탐욕적이고 인명을 가벼이 여기는 범죄적 악성·잔혹함이 있는 등의 사정이 보통 필요하며, 그렇지 않으면 금전 외적 살해 이유가 인정될 만한 사정이 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 금전적 이득이 살인 동기로 수긍될 수 있는 사정의 평가에는 사실관계별 법적 판단이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “금전적 이득만이 살인의 범행 동기가 되는 것은, 범인이 매우 절박한 경제적 곤란이나 궁박 상태에 몰려 있어 살인이라는 극단적 방법을 통”
  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “해서라도 이를 모면하려고 시도할 정도라거나 범인의 인성이 원래부터 탐욕적”
  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “이고 인명을 가벼이 여기는 범죄적 악성과 잔혹함이 있는 경우 등이 대부분이”
  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “그렇지 않은 경우는 증오 등 인간관계의 갈등이나 치정 등 피해자를 살해할 금전 외적인 이유가 있어서 금전적 이득은 오히려 부차적이거나 적어도 금전 외적인 이유가 금전적 이득에 버금갈 정도라고 인정될 만한 사정이 있어야 살”
  - `comm_001692_제250조_Ⅰ.8_21` / `Ⅰ.8`: “인의 동기로서 수긍할 정도가 된다고 할 것이다.”

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

## 186. `art250_sec1_8.objective_evidence_despite_weak_motive`

- proposition: 살인 범행의 동기가 미약하거나 다소 불분명하더라도 객관적 증거들이 충분하면 유죄로 판단할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 동기의 명확성과 객관적 증거의 충분성은 개별 기록에 따라 평가한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_23` / `Ⅰ.8`: “범행의 동기가 미약하거나 다소 불분명하더라도 객관적 증거들이 충분하면 유죄로 판”
  - `comm_001692_제250조_Ⅰ.8_23` / `Ⅰ.8`: “단할 수 있다.”

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

## 187. `art250_sec1_8.scientific_evidence_reliability`

- proposition: 공소사실을 뒷받침하는 과학적 증거방법이 사실인정에 상당한 정도의 구속력을 가지려면, 전제사실의 진실성, 과학적으로 정당한 추론, 오류 가능성의 부재 또는 극소성이 인정되고, 공인된 표준 검사기법에 의한 분석 및 채취·보관·분석 전 과정에서 자료 동일성과 조작·훼손·첨가 부재가 담보되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 과학적 증거의 전제사실, 추론, 오류 가능성 및 자료 동일성은 전문적·사실적 검토가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_25` / `Ⅰ.8`: “공소사실을 뒷받침하는 과학적 증거방법은 전제로 하는 사실이 모두 진실인 것이 입증되고 추론의 방법이 과학적으로 정당하여 오류 가능성이 전혀 없거나 무시할 정도로 극소한 것으로 인정되는 경우라야 법관이 사실인정”
  - `comm_001692_제250조_Ⅰ.8_25` / `Ⅰ.8`: “을 하는 데 상당한 정도로 구속력을 가진다 할 것인데”
  - `comm_001692_제250조_Ⅰ.8_25` / `Ⅰ.8`: “방법이 전문적인 지식·기술·경험을 가진 감정인에 의하여 공인된 표준 검사기”
  - `comm_001692_제250조_Ⅰ.8_25` / `Ⅰ.8`: “법으로 분석을 거쳐 법원에 제출된 것이어야 할 뿐만 아니라, 채취·보관·분석 등 모든 과정에서 자료의 동일성이 인정되고 인위적인 조작·훼손·첨가가 없었”
  - `comm_001692_제250조_Ⅰ.8_25` / `Ⅰ.8`: “다는 것이 담보되어야 한다.”

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

## 188. `art250_sec1_8.third_party_access`

- proposition: 피고인이 여관방을 잠그고 나왔고 시정장치가 손상되지 않았더라도 제3자가 그 방의 열쇠를 가지고 있었다면 제3자 침입 가능성이 있으므로, 위 정황증거 및 간접사실의 증명력은 현저히 감소한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 제3자 열쇠 보유와 침입 가능성은 해당 정황증거의 증명력을 평가하는 사안 한정 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.8_24` / `Ⅰ.8`: “누군가 제3자가 그 방의 열쇠를 갖고 있다면 시”
  - `comm_001692_제250조_Ⅰ.8_24` / `Ⅰ.8`: “정장치의 손상 없이 그 방에 침입할 수 있는 것이다.”
  - `comm_001692_제250조_Ⅰ.8_24` / `Ⅰ.8`: “이 여관방에서 나갈 때 문을 잠갔다거나 시정장치가 손상되지 않았다는 정황증”
  - `comm_001692_제250조_Ⅰ.8_24` / `Ⅰ.8`: “거 내지 간접사실은 그 증명력이 현저히 감소되었다고 보아야 한다.”

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

## 189. `art250_sec1_9.bodyless_circumstantial_proof`

- proposition: 살인죄처럼 법정형이 무거운 범죄도 직접증거 없이 간접증거만으로 유죄를 인정할 수 있고, 시체가 발견되지 않아도 관련 간접증거를 상호 관련하에 종합적으로 고찰하여 살인 공소사실을 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간접증거의 상호 관련성과 종합 고찰은 평가적 판단이므로 standard input으로 유지한다. 소개된 판례 입장은 원문 판례 index로 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.9_31` / `Ⅰ.9`: “살인죄 등과 같이 법정형이 무거 운 범죄의 경우에도 직접증거 없이 간접증거만에 의하여 유죄를 인정할 수 있 고, 피해자의 시체가 발견되지 아니하였더라도 간접증거를 상호 관련하에서 종 합적으로 고찰하여 살인죄의 공소사실을 인정할 수 있다.”

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

## 190. `art250_sec1_9.bodyless_insufficient_linkage`

- proposition: 시신이 없고 사망 경위·살해방법·피고인의 구체적 행동 및 원인행위가 불명하며, 피고인 행위와 사망을 직접 연결할 객관적 흔적이나 의미 있는 정황적 접점이 부족하고 다른 사망 가능성을 배제할 수 없는 사안에서는 살인죄 책임을 인정하기 어렵다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대안적 사망 원인 또는 제3자 범행 가능성을 배제할 수 없는 구체 사안의 소개된 판단이다. 해당 대법원 판단의 원문과 사실관계 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.9_35` / `Ⅰ.9`: “이와 같이 살인의 범행방법이나 사망경위가 밝혀지지 않은 사정 아 래에서는 감금과정에서의 반항 억압 또는 도주 방지를 위한 폭행 과정에서 B가 사망하였을 가능성, 독자적인 제3자의 범행 가능성도 배제할 수 없는 점 등의 여러 사정을 종합하여, 살인죄의 죄책을 인정하기 어렵다고 보았다.”

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

## 191. `art250_sec1_9.bodyless_summary_requirements`

- proposition: 시신 없는 살인사건에서 유죄를 인정하려면 피해자의 사망, 피고인의 살의, 피고인 행위에 의한 피해자 사망이 요구된다고 판례 입장을 정리할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시체 없는 살인사건의 요건을 요약한 소개된 판례 입장이다. 각 요건의 증명 충족 여부와 원문 판례의 적용 범위는 검토가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.9_32` / `Ⅰ.9`: “시신 없는 살인사건의 공소사실을 유죄로”
  - `comm_001692_제250조_Ⅰ.9_32` / `Ⅰ.9`: “인정하기 위해서는 ⅰ) 피해자가 사망하였을 것, ⅱ) 피고인이”
  - `comm_001692_제250조_Ⅰ.9_32` / `Ⅰ.9`: “피해자에 대한 살의를 가지고 있었을 것, ⅲ) 피고인의 행위에”
  - `comm_001692_제250조_Ⅰ.9_32` / `Ⅰ.9`: “의하여 피해자가 사망하였을 것이 요구된다고 정리”

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

## 192. `art250_sec2_10.parricide_ordinary_murder_specialty`

- proposition: 존속살해죄가 성립하면 특별관계에 있는 보통살인죄는 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 존속살해죄가 성립하는 경우 보통살인죄를 별도로 구성하지 않는 특별관계 규율이다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.10_141` / `Ⅱ.10`: “존속살해죄와 보통살인죄의 관계는 특별관계이므로, 존속살해죄가 성립하면 보 통살인죄는 별도로 성립하지 않는다.”

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

## 193. `art250_sec2_5.parricide_improper_status_offense`

- proposition: 존속살해죄는 신분으로 인하여 형벌이 가중되는 부진정신분범이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 존속살해죄의 신분범 성격 및 형벌가중 구조에 관한 해설상 분류이다. 신분 없는 가담자, 객체의 착오, 입양관계 등 구체적 적용 문제는 현재 근거만으로 결정하지 않는다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.5_134` / `Ⅱ.5`: “존속살해죄는 신분범인데, 구체적으로는 그 신분으로 인하여 형벌의 가중만을 가져오므로 부진정신분범이다.”

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

## 194. `art250_sec2_6.adoption_creates_lineal_relationship`

- proposition: 입양으로 양부모 및 그 직계존속과 양자 및 그 직계비속 사이에 직계존비속의 법정혈족관계가 형성된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 입양에 따른 법정혈족관계의 범위를 정리한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “입양으로 인해 양부모 및 그 직계존속과 양자 및 그 직계비속 사이에 직계존 비속의 법정혈족관계가 형성된다.”

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

## 195. `art250_sec2_6.adoption_requirements_not_met`

- proposition: 입양 의사가 있었더라도 입양요건을 갖추지 않은 경우에는 직계존비속 관계에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 입양 의사와 입양 성립요건의 충족 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “나아가 입양 의사가 있었 더라도 입양요건을 갖추지 않은 경우에는 직계존비속 관계에 해당하지 않는다.”

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
