# 살인·존속살해 RuleIR 카드 검수 10

- unit: `homicide`
- articles: art250, art254, art255
- cards: 136–150 / 242
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

## 136. `art250_sec1_20.robbery_concealment_not_retaliatory`

- proposition: 강도범행 후 범행 은폐 목적으로 피해자를 살해한 경우 보복목적 살인이 아니라 강도살인죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 범행 은폐 목적과 보복 목적의 구별 및 강도범행과 살해의 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_101` / `Ⅰ.20`: “강도범행 후 범행 은폐의 목적으로 피해자를 살해하여도 보복목적 살인이 아니라 강도살인죄가 성립한다.”

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

## 137. `art250_sec1_20.same_intent_preparation_to_completion`

- proposition: 동일인을 살해하려는 동일한 의사발동에서 나온 예비행위 또는 공격행위가 범의 갱신 없이 살인기수에 이른 경우, 시간·장소·방법의 동일 여부와 무관하게 포괄하여 단순한 1개의 살인기수죄로 처단한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 동일한 의사발동 및 범의 갱신 부재는 평가가 필요하고, 주석이 소개한 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “그 예비행위 내지 공격행 위가 동일한 의사발동에서 나왔고 그 사이에 범의의 갱신이 없는 한, 각 행위가 같은 일시·장소에서 행하여졌거나 또는 다른 장소에서 행하여졌거나를 막론하 고 또 그 방법이 동일하거나 여부를 가릴 것 없이, 그 살해의 목적을 달성할 때 까지의 행위는 모두 실행행위의 일부로서 이를 포괄적으로 보고 단순한 한 개 의 살인기수죄로 처단할 것”

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

## 138. `art250_sec1_20.same_person_homicide_stages`

- proposition: 동일인에 대한 살인예비·살인미수·살인기수 및 동일인에 대한 상해·살인은 법조경합 관계이므로 하나의 살인죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일 피해자에 대한 예비·미수·기수 또는 상해·살인의 법조경합 예외를 기록한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “동일인에 대한 살인예비, 살인미수 및 살인기수와 동일인에 대한 상해·살인은 법조경합의 관계에 있으므로, 하나의 살인죄만 성립하게 된다.”

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

## 139. `art250_sec1_20.sequential_hammer_killing`

- proposition: 여러 피해자를 차례로 쇠망치로 강타해 살해한 경우 피해법익이 다르고 각 피해자에 대한 살해의사가 각각 성립하면, 동일 장소·방법으로 시간적으로 접착된 행위라도 포괄적 1죄가 아니며 경합범으로 처단한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 포괄일죄 배제의 전제가 되는 피해자별 살해의사와 보호법익을 검토해야 하며 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “이와 같은 경우에는 피해법익이 다 르고 각 피해자를 살해하려는 의사가 각각 성립한 것이어서 단일한 범의하의 행위라고는 할 수 없으니, 동일한 장소에서 동일한 방법에 의하여 시간적으로 접착된 행위라고 하더라도 이를 포괄적인 1죄라고는 할 수 없다고 보아, 경합범 으로 처단한 원심 판단을 수긍하였다.”

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

## 140. `art250_sec1_20.sequential_shooting_victims`

- proposition: 단일 범의 아래 동일 장소·방법으로 시간적으로 접착된 상황에서 각 피해자의 머리에 실탄을 순차 발사하여 살해한 경우에도 피해자 수에 따라 각 살인죄를 구성한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 개별 판례 입장이므로 원판례 확인 전에는 보고된 선례로만 취급한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “피고인이 휴대하 고 있던 권총에 실탄 6발을 장전하여 처와 자식들의 머리에 각기 1발씩 순차로 발사하여 살해하였다면 피해자들의 수에 따라 각 살인죄를 구성한다고 보았다.”

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

## 141. `art250_sec1_20.single_act_multiple_victims`

- proposition: 1개의 행위로 여러 사람을 살해한 경우 여러 개의 살인죄가 성립하고 상상적 경합 관계가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위의 단일성 및 상상적 경합 해당 여부의 적용은 사실관계 검토가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.20_99` / `Ⅰ.20`: “따라서 1개의 행위로 여러 사람을 살해한 때에는 여러 개의 살인죄가 성립 하여 상상적 경합 관계에 있게 된다.”

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

## 142. `art250_sec1_21.attempt_punishable`

- proposition: 살인미수범은 처벌한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 미수 처벌의 서술 근거다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_104` / `Ⅰ.21`: “미수범은 처벌하 고”

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

## 143. `art250_sec1_21.brutal_led_murder_no_plan`

- proposition: 사전 치밀한 계획이 아니고 피고인이 다소 반성하는 태도가 있더라도, 사체를 수백 개로 훼손·암매장한 사안에서 사형 선고가 심히 부당하지 않다고 본 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 구체적 판결례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_120` / `Ⅰ.21`: “피해자 C를 살해한 후 피해자 의 신원이 파악되지 않도록 사체를 수백 개로 토막내어 숲 속에 암매장하였고”
  - `comm_001692_제250조_Ⅰ.21_120` / `Ⅰ.21`: “비록 이 사건 살인 범행이 사전에 치밀하게 계획된 범행이 아니고 피고인이 다 소 반성하는 태도를 보이고 있다는 점을 고려한다고 하더라도 피고인에게 사형 을 선고한 원심의 양형이 심히 부당하다고 볼 수 없다.”

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

## 144. `art250_sec1_21.child_victims_repeat_offense`

- proposition: 방어하기 어려운 여자 어린이 2명을 유인·강제추행 후 살해하고 치밀하게 사체를 훼손·유기하며 동종 범행 반복으로 재범위험성이 큰 사정 등을 종합하여 사형 선고를 정당하다고 본 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 구체적 판결례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_118` / `Ⅰ.21`: “자신의 힘으로 스스로를 방어하기 힘든 여자 어린이 2명을 유인하여 강제추행한 다음 살해한 점, 그 후 이를 은폐하기 위하여 치밀한 계획 아래 사체들을 여러 토막 으로 절단하고”
  - `comm_001692_제250조_Ⅰ.21_118` / `Ⅰ.21`: “동일한 범행을 반복한 점에 비추 어 재범의 위험성이 매우 큰 점 등을 종합적으로 고려하여 피고인에게 사형을 선고한 조치는 정당한 것으로 받아들일 수밖에 없다.”

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

## 145. `art250_sec1_21.death_penalty_exceptional_punishment`

- proposition: 사형은 누구라도 정당하다고 인정할 특별한 사정이 있고 양형조건에 관한 모든 사정의 철저한 심리를 거쳐 사형 정당화가 밝혀진 경우에만 선고할 수 있다는 기존 법리가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사형의 예외성과 심리요건에 관한 보고된 기존 법리다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_122` / `Ⅰ.21`: “사형의 선고는 범행에 대한 책임의 정도와 형 벌의 목적에 비추어 볼 때 누구라도 그것이 정당하다고 인정할 수 있는 특별한 사정이 있는 경우에만 허용되고, 형법 제51조가 규정한 사항을 중심으로 양형의 조건이 되는 모든 사정에 대한 철저히 심리를 거쳐 사형의 선고가 정당화될 수 있음이 밝혀진 경우에 한하여 비로소 사형을 선고할 수 있다”

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

## 146. `art250_sec1_21.death_penalty_special_circumstances_explicit`

- proposition: 사형 선고 시에는 양형조건이 되는 모든 사항을 참작하여 특별한 사정이 있음을 명확히 밝혀야 한다는 대법원 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특별한 사정의 입증 수준은 별도 이견 카드와 함께 검토한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_105` / `Ⅰ.21`: “사형을 선고함에 있어서는 범인의 연령, 직업과 경력, 성행, 지능, 교 육정도, 성장과정, 가족관계, 전과의 유무, 피해자와의 관계, 범행의 동기, 사전계 획의 유무, 준비의 정도, 수단과 방법, 잔인하고 포악한 정도, 결과의 중대성, 피 해자의 수와 피해감정, 범행 후의 심정과 태도, 반성과 가책의 유무, 피해회복의 정도, 재범의 우려 등 양형의 조건이 되는 모든 사항을 참작하여 위와 같은 특 별한 사정이 있음을 명확하게 밝혀야 한다.”

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

## 147. `art250_sec1_21.death_penalty_thorough_inquiry`

- proposition: 사형 선택 여부를 심사할 때에는 피고인의 양형조건에 관한 객관적 자료와 범행 전후 정신·심리상태에 관한 전문의견 등을 통해 깊이 있는 심리를 거쳐야 하며, 간이한 심리만으로 사형을 선고한 판단은 필요한 심리를 다하지 않은 위법으로 파기될 수 있다는 대법원 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 두 후보는 사형 심리의 충실성에 관한 상호 보완적 보고판례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_105` / `Ⅰ.21`: “피고인의 주관적인 양형요소인 성행과 환경, 지능, 재범의 위험성, 개선 교화 가능성 등을 심사할 수 있는 객관적인 자료를 확보하여 이를 통하여 사형 선택 여부를 심사하여야 할 것은 물론이고, 피고인이 범행을 결의하고 준비하며 실행할 당시를 전후한 피고인의 정신상태나 심리상태의 변화 등에 대하여서도 정신의학이나 심리학 등 관련 분야의 전문적인 의견을 들어 보는 등 깊이 있는 심리를 하여 본 다음에 그 결과를 종합하여 양형에 나아가야 한다.”
  - `comm_001692_제250조_Ⅰ.21_110` / `Ⅰ.21`: “피고인의 양형조건에 대한 조사나 심리를 별도 로 해 봄이 없이 수사기록에 나타난 양형자료만을 토대로 하여 간이한 심리만 을 끝으로 피고인에게 사형을 선고해 버린 제1심을 유지한 원심판결에는 사형의 양정에 관한 법리를 오해하여 형의 양정에 관한 필요한 심리를 다하지 아니한 위법이 있다.”고 판시하여 원심판결을 파기하였다.”

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

## 148. `art250_sec1_21.death_penalty_unavoidable`

- proposition: 사형은 여러 양형사정을 참작하여 죄책이 심히 중대하고 죄형균형이나 일반예방상 극형이 불가피한 경우에만 허용될 수 있다는 대법원 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_105` / `Ⅰ.21`: “사형을 선택함에 있어서는 범행의 동기, 태양, 죄질, 범행의 수단, 잔 악성, 결과의 중대성, 피해자의 수, 피해감정, 범인의 연령, 전과, 범행후의 정황, 범인의 환경, 교육 및 생육과정 등 여러 사정을 참작하여 죄책이 심히 중대하고 죄형의 균형이나 범죄의 일반예방적 견지에서도 극형이 불가피하다고 인정되는 경우에 한하여 허용될 수 있는 것”

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

## 149. `art250_sec1_21.foreign_acquittal_detention_credit`

- proposition: 외국 법원에서 무죄판결을 받은 사람의 미결구금 기간은 외국에서 유죄판결에 따라 형이 실제 집행된 경우가 아니므로 형법 제7조 산입 대상이 될 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 형법 제7조 적용 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_124` / `Ⅰ.21`: “형사사건으로 외국 법원에 기소되었다가 무죄판결을 받은 사람은, 설령 그가 무 죄판결을 받기까지 상당 기간 미결구금되었더라도 이를 유죄판결에 의하여 형 이 실제로 집행된 것으로 볼 수는 없으므로, ‘외국에서 형의 전부 또는 일부가 집행된 사람’에 해당한다고 볼 수 없고, 그 미결구금 기간은 형법 제7조에 의한 산입의 대상이 될 수 없다고 판단하였다.”

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

## 150. `art250_sec1_21.homicide_sentencing_considerations`

- proposition: 살인죄 양형에서는 범행의 계획성, 동기와 목적, 피해자와의 관계 및 피해자의 역할·과오, 범행 후 정황에 따른 불법 및 책임 정도를 구분하여 반영하는 것이 중요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 양형요소의 평가와 비교형량이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_104` / `Ⅰ.21`: “따라서 살인죄의 양형에서는 범행의 계획성 여부, 동기와 목적, 피해자와의 관계 및 피해자의 역할과 과오, 범행 후의 정황에 따른 불법 및 책 임의 정도를 구분하여 양형에 반영시키는 것이 중요하다.”

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
