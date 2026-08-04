# 살인·존속살해 RuleIR 카드 검수 14

- unit: `homicide`
- articles: art250, art254, art255
- cards: 196–210 / 242
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

## 196. `art250_sec2_6.birth_registration_effective_as_adoption`

- proposition: 양친자 관계를 창설하려는 명백한 의사와 그 밖의 입양 성립요건이 모두 있으면, 친생자 출생신고도 입양의 효력이 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 양친자 관계 창설 의사와 그 밖의 입양 성립요건을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “당사자 사이에 양친자 관계를 창설하려는 명백한 의사가 있고 기 타 입양의 성립요건이 모두 구비된 경우에는 요식성을 갖춘 입양신고 대신 친 생자 출생신고가 있더라도 입양의 효력이 있다고 한다.”

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

## 197. `art250_sec2_6.collateral_relatives_excluded`

- proposition: 백부모·숙부모 등 방계혈족을 살해한 경우에는 존속살해죄가 아니라 보통살인죄가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 방계혈족에 관한 명시적 제외 및 보통살인죄 귀결 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “그러나 백부모 (伯⽗母), 숙부모(叔⽗母) 등은 방계혈족에 지나지 않으므로, 이들을 살해하여도 존속살해죄에 해당하지 않고 보통살인죄가 된다.”

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

## 198. `art250_sec2_6.lineal_ascendant_scope`

- proposition: 직계존속에는 부모와 조부모·증조부모·외조부모·외증조부모 등이 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 직계존속의 열거된 인적 범위를 정리한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “직계존속이란 원래 혈통이 직상직하(直上直下)의 형 태로 연결되는 혈족으로서, 부모는 물론이고 부모와 동일한 항렬 이상에 속하는 존속 즉 조부모, 증조부모, 외조부모, 외증조부모 등이 포함된다.”

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

## 199. `art250_sec2_6.lineal_relationship_strict_interpretation`

- proposition: 행위자에게 불리한 직계존비속관계의 존재는 엄격하게 해석하여야 하며, 가족관계등록부 등에 친생자로 신고되어도 법률상 친자관계가 없으면 직계존속이 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 법률상 친자관계의 존재와 엄격해석 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “직계존비속관계의 존재는 행위자에게 불리한 개념이므로, 엄격하게 해석하여야 한다.”
  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “이러한 공부에 친생 (公簿) 자로 출생신고가 되어 있더라도 법률상 친자관계가 없으면 직계존속이 아니 다.”

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

## 200. `art250_sec2_6.nonmarital_child_biological_father_before_recognition`

- proposition: 인지 전 혼인외 출생자가 생부를 살해한 경우에는 직계비속관계가 없어 보통살인이 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인지 절차 및 행위 당시 신분관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “그러나 혼인외 출생자와 생부 (⽣⽗) 사이에는 인지절차를 거치지 않는 한 직계비속관계가 없으므로, 인지 이전의 혼인외 출생자가 그의 생부를 살해한 때에는 보통살인이 된다.”

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

## 201. `art250_sec2_6.nonmarital_child_biological_mother`

- proposition: 혼인외 출생자가 생모를 살해한 경우에는 출생으로 법률상 친족관계가 생기므로 존속살해가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 혼인외 출생자와 생모 사이의 법률상 친족관계 및 적용 사실을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “출생으로 당연히 법률상의 친족관계가 생기므로 혼인외 출생자가 그의 생모를 살해한 때에는 존속살해가 성립한다.”

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

## 202. `art250_sec2_6.object_lineal_ascendant_self_or_spouse`

- proposition: 존속살해죄의 객체는 자기 또는 배우자의 직계존속이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 존속살해죄 객체의 기본 범위를 정리한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “존속살해죄의 객체는 ‘자기 또는 배우자의 직계존속’이다.”

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

## 203. `art250_sec2_6.spouse_legal_spouse_only`

- proposition: 존속살해죄에서 배우자는 법률상 배우자만을 뜻하며 사실상 배우자는 포함되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 배우자의 법률상 지위에 관한 범위 제한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_136` / `Ⅱ.6`: “배우자도 법률상 배우자만을 의미하고 사실상 배우자는 포함되지 않는 다.”

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

## 204. `art250_sec2_6.status_at_commencement_sufficient`

- proposition: 배우자의 직계존속이라는 신분관계는 살해행위의 착수 당시 존재하면 충분하다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 배우자의 직계존속 신분관계의 기준 시점을 정리한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_136` / `Ⅱ.6`: “다만 배우자의 직계존속이라는 신분관계는 살해행위의 착수 당시에 있으 면 충분하”

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

## 205. `art250_sec2_6.step_parent_excluded`

- proposition: 계부모는 직계존속이 아니므로 존속살해죄의 행위객체에서 제외된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 계부모의 객체 해당성을 명시적으로 배제한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “계부모는 직계존속이”
  - `comm_001692_제250조_Ⅱ.6_135` / `Ⅱ.6`: “아니므로, 존속살해죄의 행위객체에서 제외된다.”

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

## 206. `art250_sec2_8.intent_knowledge_lineal_status`

- proposition: 존속살해죄가 성립하려면 자기 또는 배우자의 직계존속을 살해한다는 고의가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 직계존속 관계에 대한 인식 여부는 개별 사실관계에서 판단한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.8_138` / `Ⅱ.8`: “존속살해죄 성립을 위해서는 자기 또는 배우자의 직계존속을 살해한다는 고의 가 있어야 한다.”

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

## 207. `art250_sec2_8.no_knowledge_lineal_status`

- proposition: 살해 객체가 자기 또는 배우자의 직계존속임을 인식하지 못한 경우에는 존속살해죄가 아니라 보통살인죄의 죄책을 진다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 직계존속성 인식의 부재가 실제로 인정되는지는 개별 사실관계에서 판단한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.8_138` / `Ⅱ.8`: “살해의 객체가 자기 또는 배우자의 직계존속임을 인식하지 못한 경우에는 형법 제15조 제1항에 의해 보통살인죄의 죄책을 진다.”

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

## 208. `art250_sec2_9.nonstatus_accomplice_ordinary_murder_punishment_outcome`

- proposition: 비신분자가 존속살해에 가담한 경우, 위 두 견해 모두 비신분자를 보통살인죄로 처벌한다는 결론에는 차이가 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 두 견해의 처벌 결론이 같다는 해설상의 정리다. 각 견해의 성립죄명 및 제33조 적용 구조는 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.9_139` / `Ⅱ.9`: “양 견해 모두 비신분자가 보통살인죄로 처벌된다는 결론에서는 차이가 없다.”

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

## 209. `art250_sec2_9.nonstatus_accomplice_wife_with_biological_son_precedent`

- proposition: 실자와 함께 남편을 살해한 처는 존속살해죄의 공동정범이라는 취지의 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 좁은 판례 취지이며, 제2설에 가깝다는 평가는 원문 판례 확인 전에는 확정할 수 없다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.9_139` / `Ⅱ.9`: “판례는 실자와 더불어 남편을 살해한 처는 존속살해죄의 공동정범이라는 (實⼦) 취지로 판시하여 제2설의 입장에 가깝다고 보인다.”

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

## 210. `art254.attempt_penalty_mitigation`

- proposition: 제254조의 미수범은 기수범보다 형을 감경할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 형 감경 가능 여부와 구체적 감경 적용에는 재판상 판단이 필요하다.
- bounded sources:

  - `raw_001692_제254조_p001` / `raw_pdf.page_1`: “본죄의 규정에  해당하는  미수범은 기수범보다   그 형을 감경할 수 있다.”

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
