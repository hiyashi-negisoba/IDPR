# 살인·존속살해 RuleIR 카드 검수 11

- unit: `homicide`
- articles: art250, art254, art255
- cards: 151–165 / 242
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

## 151. `art250_sec1_21.indeterminate_midpoint_nonaggravation`

- proposition: 피고인만 항소하여 불이익변경금지 원칙이 적용되는 경우, 부정기형을 파기하고 정기형을 선고할 때에는 부정기형의 장기와 단기의 중간형을 기준으로 위반 여부를 판단한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 불이익 여부 판단에는 절차적 적용 검토가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_124` / `Ⅰ.21`: “피고인이 항소심 선고 이전에 19세에 도달하여 제1심에서 선고한 부정기형”
  - `comm_001692_제250조_Ⅰ.21_124` / `Ⅰ.21`: “을 파기하고 정기형을 선고함에 있어 불이익변경금지 원칙 위반 여부를 판단하 는 기준은 부정기형의 장기와 단기의 중간형이 되어야 한다고 판단하였다.”

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

## 152. `art250_sec1_21.juvenile_age_at_fact_judgment`

- proposition: 소년법상 19세 미만인 자 해당 여부는 사실심판결 선고 시를 기준으로 판단하므로, 제1심 부정기형 선고 후 항소심 선고 전 19세에 도달하면 정기형을 선고하여야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 보고된 판례의 시간기준 규칙이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_123` / `Ⅰ.21`: “소년법 제60조 제1항에”
  - `comm_001692_제250조_Ⅰ.21_123` / `Ⅰ.21`: “정한 ‘소년’은 소년법 제2조에 정한 19세 미만인 자를 의미하는 것으로, 이에 해”
  - `comm_001692_제250조_Ⅰ.21_123` / `Ⅰ.21`: “당하는지는 사실심판결 선고 시를 기준으로 판단하여야 하므로, 제1심에서 부정”
  - `comm_001692_제250조_Ⅰ.21_123` / `Ⅰ.21`: “기형을 선고받은 피고인이 항소심 선고 이전에 19세에 도달하는 경우 정기형이 선고되어야 한다.”

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

## 153. `art250_sec1_21.leader_spontaneous_joining`

- proposition: 수괴의 의사와 관계없이 우발적으로 일어난 살인은 사전 계획하거나 지시한 수괴가 중한 책임을 지는 일반적 계획범행과 다르다는 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 수괴 책임 판단에 한정된다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_114` / `Ⅰ.21`: “이 사건 살인의 경우는 계획적 범행에 있어 사전에 범행계획을 세우거나 범행을 지시한 수괴가 중한 책임을 지게 되는 일반적인 경우와는 다른 바로서 이 사건은 수괴인 피고인 B 의 의사와는 관계없이 전혀 우발적으로 일어난 것이고”

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

## 154. `art250_sec1_21.murder_proceeds_forfeiture`

- proposition: 살인죄 범행으로 생긴 재산 등은 범죄수익은닉의 규제 및 처벌 등에 관한 법률이 정하는 몰수·추징의 대상이 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 몰수·추징 대상 가능성에 관한 법률 적용 서술이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_126` / `Ⅰ.21`: “본죄는 범죄수익은닉의 규제 및 처벌 등에 관한 법률 제2조 제1호 가목이 정하는 ‘특정범죄’에 해당하므로, 본죄의 범행에 의해 생긴 재산 등은 범죄 수익은닉의 규제 및 처벌 등에 관한 법률이 정하는 몰수·추징의 대상이 될 수 있다.”

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

## 155. `art250_sec1_21.murder_recidivism_assessment`

- proposition: 살인범죄 재범 위험성은 직업과 환경, 범행 전 행적, 범행 동기·수단, 범행 후 정황 및 개전의 정 등 여러 사정을 종합하여 객관적으로 판단하고 판결시를 기준으로 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 예측판단의 요소와 시점에 관한 보고판례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_125` / `Ⅰ.21`: “살인범죄의 재범의 위험성 유무는 피부착명령 청구자의 직업과 환경, 당해 범행 이전의 행적, 범행의 동기, 수단, 범행 후의 정 황, 개전의 정 등 여러 사정을 종합적으로 평가하여 객관적으로 판단하여야 하 고, 이러한 판단은 장래에 대한 가정적 판단이므로 판결시를 기준으로 하여야 한다.”

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

## 156. `art250_sec1_21.murder_recidivism_substantial_probability`

- proposition: 전자장치 부착명령에서 살인범죄 재범 위험성이란 단순한 재범 가능성이 아니라 장래 다시 살인범죄를 범하여 법적 평온을 깰 상당한 개연성을 의미한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 재범위험성은 예측적·평가적 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_124` / `Ⅰ.21`: “‘살인범죄를 다시 범할 위험성’이란 재범할 가능성만으로는 부족하 고 피부착명령청구자가 장래에 다시 살인범죄를 범하여 법적 평온을 깨뜨릴 상 당한 개연성이 있음을 의미한다.”

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

## 157. `art250_sec1_21.ordinary_homicide_penalty`

- proposition: 보통살인죄의 법정형은 사형, 무기 또는 5년 이상의 징역이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법정형 서술의 검토 단위다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_104` / `Ⅰ.21`: “보통살인죄의 법정형은 사형, 무기 또는 5년 이상의 징역이다.”

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

## 158. `art250_sec1_21.organized_cult_murders`

- proposition: 공범을 가담시키고 사전에 계획하여 실행을 주도한 조직적·잔혹한 다수범행의 주범에 대한 사형 양형을 수긍한 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 구체적 판결례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_119` / `Ⅰ.21`: “공범들을 범행에 가담시키고 사전에 범행을 치밀하게 계획 하고 나아가 그 실행행위도 주도한 주범인 점”
  - `comm_001692_제250조_Ⅰ.21_119` / `Ⅰ.21`: “다수의 공범들이 관여하고 치밀하게 계획된 조직적인 범행이며 범행수법이 잔혹하고 무자비하며”
  - `comm_001692_제250조_Ⅰ.21_119` / `Ⅰ.21`: “피고인에 대하여 사형을 선고한 원심의 형의 양정은 수긍될 수밖에 없다.”

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

## 159. `art250_sec1_21.planned_double_murder`

- proposition: 계획·준비된 2명 살해와 살해 후 피해자 가족에 대한 범행 등의 사안에서 범행계획·준비·잔혹성, 피해결과 및 살해 후 행태를 고려하여 사형을 정당화할 특별한 사정이 있다고 본 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 구체적 사안의 제한된 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_117` / `Ⅰ.21`: “이 사건 범행의 동기와 경위, 범행계획의 내용과 대상, 범행의 준비 정도와 그 수단, 범 행의 잔혹성, 피해자들과의 관계, 피해자 B, C가 살해당하고 피해자 A 또한 극 심한 신체적·정신적 고통과 후유증을 겪게 된 점”
  - `comm_001692_제250조_Ⅰ.21_117` / `Ⅰ.21`: “이 사건은 피고인에 대한 극형의 선고가 정당화될 수 있는 특별한 사정이 있다.”

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

## 160. `art250_sec1_21.principal_vs_accomplices`

- proposition: 범행 모의를 주도하고 다른 피고인들의 실행행위를 지시·통제한 피고인에게 사형을, 나머지 피고인들에게 무기징역을 선고한 양형이 과중하지 않다고 본 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공동피고인 간 역할 차이에 관한 보고판례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_121` / `Ⅰ.21`: “특히 피고인 甲은 피고인들 중 최연장자로서 2등 항해사의 지위에 있으면서 이 사건 범행의 모의를 주도하 고, 다른 피고인들의 구체적인 실행행위를 지시하고 통제하였다는 점에서 더욱 무거운 책임을 묻지 않을 수 없다.”
  - `comm_001692_제250조_Ⅰ.21_121` / `Ⅰ.21`: “피고인 A에 대하여 사형을 선고한 제1심판결을 유지하고, 나머지 피고인들에 대하여 무 기징역형을 선고한 원심의 양형은 결코 너무 무거워 부당하다고 할 수 없다.”

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

## 161. `art250_sec1_21.prisoner_homicide_death_reversal`

- proposition: 미필적 고의, 흉기·위험물 미사용, 피해자 1명 및 유사사건과의 형평을 고려하지 않고 사형을 선택한 것은 사형 선택 요건에 관한 법리오해와 심리미진에 따른 현저히 부당한 양형일 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 구체적 파기 판단의 제한된 사정이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_107` / `Ⅰ.21`: “이와 같이 피고인이 미필적 고의로 이 사건 범행을 저질렀다는 점은 중요한 양 형요소에 해당한다. 여기에 피고인이 살인 범행에 흉기나 위험한 물건을 사용하 지 않았다는 점과 이 사건의 피해자가 한 사람에 그쳤다는 점 또한 중요한 사정 으로 다른 유사사건에서의 양형과 그 형평성을 비교할 수 있다.”
  - `comm_001692_제250조_Ⅰ.21_108` / `Ⅰ.21`: “사형의 선택기준이나 다른 유사사건과의 일반적 양형의 균형상 원심이 피고 인에 대하여 사형을 선택한 것은 사형 선택의 요건에 관한 법리오해와 심리미진 으로 형의 양정이 심히 부당하다고 인정할 현저한 사유가 있는 때에 해당한다.”

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

## 162. `art250_sec1_21.second_life_sentence`

- proposition: 무기징역 집행 중 다시 무기징역을 선고하는 사정만으로 그 형이 무의미하다고 볼 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 양형 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_108` / `Ⅰ.21`: “무기 징역형 집행 중 다시 무기징역형을 선고한다는 사정만으로 그 형이 무의미하다 고 볼 것은 아니다.”

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

## 163. `art250_sec1_21.sequential_offense_planning`

- proposition: 연속된 범행에서는 전체 범행의 사전·치밀한 계획 여부와 최초 범행 후 은폐 또는 흥분 상태에서 후속 범행이 우발적으로 이루어졌는지를 면밀히 심리·확정하여 양형조건을 달리하여야 한다는 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 후속범행의 계획성과 우발성은 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_113` / `Ⅰ.21`: “사전에 모든 범행이 치밀하게 계획되어 이루어 진 경우와 단순히 우발적이고 순간적인 감정으로 인하여 이루어진 경우, 그리고 최초 범행은 사전 계획하에 실행에 옮겨졌으나 그에 잇따른 범행은 당초 범행 을 은폐하거나 또는 흥분된 상태에서 순간적으로 범의가 일어나 우발적으로 저 질러진 경우에 있어서 각 그 양형조건을 달리 한다고 할 것이므로”

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

## 164. `art250_sec1_21.spontaneous_single_offense`

- proposition: 계획 없이 우발적·일회적으로 범행하였고 범행 후 깊이 뉘우치는 사정은 사형 선택에서 고려할 양형사정이라는 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인용된 양형사정만 기록한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_115` / `Ⅰ.21`: “이 사건 범행의 방법이 계획된 의도에서 이루어진 것이 아니고 술에 다소 취한 흥분한 상태에서 일어난 우발적인 일회적인 것이고 위 에 나타난 피고인의 환경, 생육 과정과 이 사건 범행 후 전비(前⾮)를 깊이 뉘우 치며 피해자의 명복을 빌고 있는 점”

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

## 165. `art250_sec1_21.treatment_custody_not_attachment_risk`

- proposition: 치료감호와 부착명령을 함께 선고할 때 치료감호의 재범 위험성이 인정된다는 이유만으로 부착명령을 위한 살인범죄 재범 위험성을 단정해서는 안 되며, 별도로 판단해야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 두 제도의 위험성 판단을 분리하는 보고판례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_125` / `Ⅰ.21`: “법원이 치료감호와 부착명령을 함께 선고할 경우에는 치료감호의 요건으로서 재범의 위험성과는 별도로, 치료감호를 통한 치료 경과에도 불구하고 부착명령 의 요건으로서 재범의 위험성이 인정되는지를 따져보아야 하고”
  - `comm_001692_제250조_Ⅰ.21_125` / `Ⅰ.21`: “치료감호를 위한 재범의 위험성이 인정된다 하여 부착명령을 위한 재범의 위험성도 인정된다고 섣불리 단정하여서는 안 된다.”

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
