# 살인·존속살해 RuleIR 카드 검수 1

- unit: `homicide`
- articles: art250, art254, art255
- cards: 1–15 / 242
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

## 1. `art250.causation.autopsy-alternative-causes`

- proposition: 부검의가 유력한 사망원인을 지시하더라도 다른 사인의 가능성을 가볍게 배제해서는 안 되며, 부검소견에 주로 의지하여 유죄를 인정하려면 다른 가능한 사망원인을 모두 배제하는 치밀한 논증이 필요하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 부검소견을 중심으로 사망원인과 유죄를 인정하는 경우의 증명 평가 기준으로, 가능한 대체 사인의 배제 논증을 검토해야 한다. 소개된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.6_14` / `Ⅰ.6`: “부검의가 사체에 대한 부검을 실시한 후 어떤 것을 유력한 사망원인으로 지시한다고 하여 그 밖의 다른 사인 이 존재할 가능성을 가볍게 배제하여서는 아니 되고, 특히 형사재판에서 위 부 검의의 소견에 주로 의지하여 유죄의 인정을 하기 위해서는 다른 가능한 사망 원인을 모두 배제하기 위한 치밀한 논증의 과정을 거치지 않으면 아니 된다.”

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

## 2. `art250.causation.strangulation-remand`

- proposition: 피해자의 사망원인이 충분히 증명되지 않은 교살 혐의 사건에서, 대법원은 원심이 필요한 심리를 다하지 않았다고 보아 원심판결을 파기환송하였다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 교살 혐의 사건에 한정하여 소개된 파기환송 판단이다. 구체적 사정과 판례 원문을 확인하기 전에는 일반적 사망원인 증명 기준으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.6_17` / `Ⅰ.6`: “대법원은 아래와 같은 사정 등을 들어, 피해자의 사망 원인이 충분히 증명되지 않았다는 취지로 판단하면서 원심 판결에 필요한 심리를 다하지 않은 잘못이 있다고 보아 원심판결을 파기환송하였다.”

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

## 3. `art250.parricide.definition`

- proposition: 존속살해죄는 자기 또는 배우자의 직계존속을 살해함으로써 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 존속살해죄의 행위와 피해자 관계를 한정하는 기본 정의다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.1_130` / `Ⅱ.1`: “존속살해죄는 자기 또는 배우자의 직계존속을 살해함으로써 성립한다.”

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

## 4. `art250.parricide.status_offense`

- proposition: 존속살해죄는 객체가 자기 또는 배우자의 직계존속이고 행위주체가 비속이라는 신분으로 형이 가중되는 부진정 신분범이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직계존속 및 비속 신분관계의 해당 여부와 부진정 신분범으로서의 적용 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.1_130` / `Ⅱ.1`: “존속살해죄는 그 객체가 보통 사람이 아니라 자기 또는 배우자의 직계존속으로 규정된 범죄로서, 행위주체가 비속이라는 신분에 의하여 형이 가중되는 부진정 신분범이라고 할 수 있다.”

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

## 5. `art250_sec1_1.murder_intentional_killing`

- proposition: 살인죄는 고의로 사람을 살해하여 사람의 생명을 끊는 범죄이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살인죄의 기본 정의를 나타내는 후보이며, 고의 및 생명침해 사실의 충족 여부는 별도 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.1_1` / `Ⅰ.1`: “살인죄는 고의로 사람을 살해하는 것, 즉 사람의 생명을 끊는 것이다.”

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

## 6. `art250_sec1_1.ordinary_murder_victim`

- proposition: 살인 피해자가 보통의 사람인 경우 보통살인죄가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 피해자 분류에 관한 서술적 정의이며, 보통의 사람 범위와 다른 살인유형과의 구별은 현재 인용 범위 밖이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.1_1` / `Ⅰ.1`: “그 피해자 가 보통의 사람인 경우가 보통살인죄”

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

## 7. `art250_sec1_10.captain_evacuation_omission_holding`

- proposition: 침몰 선박의 선장이 승객 구조를 지휘·통제할 권한과 승객 사망을 쉽게 방지할 가능성이 있었음에도 퇴선조치를 이행하지 않아 승객 사망을 초래한 경우, 그 부작위는 작위에 의한 살인의 실행행위와 동일하게 평가될 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판단의 원문 확인 전에는 commentary-reported precedent로만 취급하며, 지휘·통제 권한 및 결과방지 가능성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_41` / `Ⅰ.10`: “피고인 A의 위와 같은 부작위는 작위에 의한 살인의 실행행위와 동일하게 평가할 수 있고, 승객 등의 사망 또는 상해의 결과는 작위 행위에 의해 결과가 발생한 것과 규범적으로 동일한 가치가 있다.”

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

## 8. `art250_sec1_10.captain_rescue_omission_duty`

- proposition: 선박 침몰 등 조난으로 승객이나 승무원이 생명 위협에 스스로 대처할 보호능력이 없는 급박한 상황에서는, 선박 운항 또는 구체적 구조행위를 지배하는 선장·선원에게 적극적 구호활동으로 사망 결과를 방지할 작위의무가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보호능력 상실, 급박성 및 선박 운항 또는 구체적 구조행위에 대한 지배 여부를 사실적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_40` / `Ⅰ.10`: “선박침몰 등과 같은 조난사고로 승객이나 다른 승무원들이 스스로 생명에 대한 위협에 대처할 수 없는 급박한 상황이 발생한 경우에는, 선박의 운항을 지배하고 있는 선장이나 갑판 또는 선 내에서 구체적인 구조행위를 지배하고 있는 선원들은 적극적인 구호활동을 통 해 보호능력이 없는 승객이나 다른 승무원의 사망 결과를 방지하여야 할 작위 의무가 있다.”

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

## 9. `art250_sec1_10.detained_minor_omission_killing`

- proposition: 미성년자를 유인하여 포박·감금한 자가 감금 상태 계속 중 살해의 범의를 가지고 위험 방지 없이 피해자를 방치하여 사망하게 한 경우, 그 부작위는 살인죄의 구성요건적 행위로 평가될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 감금에 따른 보호지위, 살해 범의의 발생 시점 및 위험방지 가능성은 해당 사실관계에 맞추어 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_37` / `Ⅰ.10`: “나아가 그 감금상태가 계속된 어느 시점에서 피고인에 게 살해의 범의가 생겨 위험 발생을 방지함 없이 포박 감금상태에 있던 피감금 자를 그대로 방치함으로써 사망케 하였다면, 피고인의 부작위는 살인죄의 구성 요건적 행위를 충족하는 것이라고 평가하기에 충분하다고 보았다.”

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

## 10. `art250_sec1_10.omission_death_prevention_causation`

- proposition: 요구되는 개별적·구체적 구호의무 이행으로 사망 결과를 쉽게 방지할 수 있었고, 그 작위를 하였다면 결과가 발생하지 않았을 관계가 인정되면, 부작위와 사망 결과 사이 인과관계가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 요구되는 구호조치의 구체적 내용 및 해당 조치가 사망을 방지했을 반사실적 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_40` / `Ⅰ.10`: “이와 같이 작위의무를 이행하였다면 그 결과가 발생하지 않았을 것이라는 관계가 인정될 경우에는 그 작위를 하지 않은 부작위와 사망의 결과 사이에 인 과관계가 있는 것”

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

## 11. `art250_sec1_10.omission_equivalence_general`

- proposition: 법익침해 결과를 방지할 법적 작위의무가 있는 자가 의무 이행으로 결과를 쉽게 방지할 수 있었음에도 결과 발생을 용인하고 방관하여 의무를 이행하지 않은 경우, 그 부작위가 작위와 동등한 형법적 가치가 있으면 부작위범으로 처벌할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 작위의무, 결과방지 가능성, 결과 용인 및 작위등가성은 개별 사실관계에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_37` / `Ⅰ.10`: “형법이 금지하고 있는 법익침해의 결과발생 을 방지할 법적인 작위의무를 지고 있는 자가, 그 의무를 이행함으로써 결과발 생을 쉽게 방지할 수 있었음에도 불구하고 그 결과의 발생을 용인하고 이를 방 관한 채 그 의무를 이행하지 아니한 경우에, 그 부작위가 작위에 의한 법익침해 와 동등한 형법적 가치가 있는 것이어서 그 범죄의 실행행위로 평가될 만한 것 이라면, 작위에 의한 실행행위와 동일하게 부작위범으로 처벌할 수 있다.”

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

## 12. `art250_sec1_10.omission_guarantor_status`

- proposition: 부작위에 의한 살인죄가 성립하려면 행위자가 피해자의 생명을 보호할 보증인적 지위에 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 보증인적 지위의 존재와 범위는 구체적 관계 및 위험지배 사정에 대한 법적 평가를 요한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.10_37` / `Ⅰ.10`: “결국 부작위에 의한 살인죄가 성립되려면, 행위자가 피해자의 생명을 보호해야 할 보증인적 지위에 있어야 한다.”

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

## 13. `art250_sec1_11.attempt_commencement`

- proposition: 살인죄의 실행행위 착수시기는 행위자가 살의를 가지고 타인의 생명을 위태롭게 하는 행위를 직접 개시한 때이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 살의, 생명위태화 및 직접 개시 여부에는 구체적 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “살인죄의 실행행위 착수시기는, 행위자가 살의를 가지고 타인의 생명을 위태롭 게 하는 행위를 직접 개시했을 때이다.”

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

## 14. `art250_sec1_11.completed_murder`

- proposition: 살인죄는 생명 침해라는 일정한 결과가 발생하여야 기수가 인정되는 결과범·침해범이며, 살해행위로 피해자가 사망하면 기수에 이른다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사망 결과 발생에 따른 기수 판단을 위한 결과범·침해범 설명이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “살인죄는 보호법익에 대해 일정한 결과가 발생하여야 기수범이 인정되는 결과 범이고, 생명이라는 보호법칙을 침해해야 비로소 기수범을 인정하는 침해범이 다.”
  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “반면 살해행위로 인하여 피해자가 사망한 때에, 본죄는 기수에 이른다.”

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

## 15. `art250_sec1_11.weapon_approach_attempt`

- proposition: 살인의 고의로 흉기를 들고 피해자에게 접근한 경우에는 살인의 실행행위 착수가 인정되어 살인미수에 해당한다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 판례 입장이므로 적용 전 원판례 및 구체적 접근 행위의 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “판례는 살인의 고의를 가지고 흉기를 들고”
  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “접근하는 단계에서부터 실행의 착수를 인정하고 있다.”

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
