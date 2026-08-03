# 살인·존속살해 RuleIR 카드 검수 16

- unit: `homicide`
- articles: art250, art254, art255
- cards: 226–240 / 242
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

## 226. `art255_sec5.preparation_accomplice_negative`

- proposition: 예비죄에 대한 종범 성립은 판례가 부정하는 취지이고, 학설도 살인예비죄 방조의 가벌성을 부정한다고 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 판례의 부정 취지와 학설의 가벌성 부정이 소개된 범위에 한정한다. 판례 원문 및 종범 부정의 법리적 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제255조_Ⅴ_5` / `Ⅴ`: “예비죄에 대하여 종범이 성립할 수 있는가에 대해서 판례는”
  - `comm_001692_제255조_Ⅴ_5` / `Ⅴ`: “이를 부정하는 취지이다. 학설상으로도 살인예비죄의 방조는 그 가벌성을 부 정해야 한다고 본다.”

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

## 227. `art255_sec5.preparation_co_perpetration`

- proposition: 살인예비행위를 공동으로 한 경우 살인예비죄의 공동정범을 인정한다는 통설과 이에 가까운 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 통설과 판례에 가까운 입장이 함께 소개된 commentary-reported authority이므로, 공동정범 인정의 정확한 판례 범위와 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제255조_Ⅴ_5` / `Ⅴ`: “통설은 살인예비행위를 공동 으로 한 경우 살인예비죄의 공동정범을 인정한다. 판례도 이에 가까운 입장으 로 보인다.”

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

## 228. `art255_sec6.attempt_or_completion_absorption`

- proposition: 살인예비·음모가 살인미수 또는 살인기수 단계에 이르면 예비·음모죄는 미수 또는 기수죄에 흡수되어 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살인예비·음모와 살인미수 또는 살인기수의 보충관계 및 별도 성립 배제를 다룬다.
- bounded sources:

  - `comm_001692_제255조_Ⅵ_6` / `Ⅵ`: “살인예비·음모죄와 살인미수 및 살인기수는 보충관계에 있으므로, 예비·음모가 발전하여 미수 또는 기수의 단계에 이른 때에는 본죄는 이에 흡수되어 별도로 성립하지 않는다.”

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

## 229. `art255_sec6.multiple_preparations_single_offense`

- proposition: 하나의 살인범죄 실행을 위한 여러 예비행위는 상호 보완되어 전체로 하나의 준비행위가 되므로 하나의 살인예비죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일한 하나의 살인범죄 실행을 위한 복수 예비행위의 죄수 관계에 한정된 정리다.
- bounded sources:

  - `comm_001692_제255조_Ⅵ_6` / `Ⅵ`: “하나의 살인범죄 실행을 위해 여러 개의 예비행위가 있었던 경우에는 하나의 살인예비죄가 성립한다. 여러 개의 예비행위는 상호 보완되어 전체로서 하나의 준비행위가 되기 때문이다.”

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

## 230. `art250_sec1_11.indirect_perpetration_attempt_use_act`

- proposition: 배달인을 도구로 독극물을 보내는 간접정범에서는 원칙적으로 이용자의 이용행위가 개시된 때 실행의 착수가 있다는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 간접정범의 독극물 전달 사안에서 실행 착수 시점을 이용자의 이용행위 개시로 보는 견해다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.11_43` / `Ⅰ.11`: “간접정범에서는 원칙적으로 이용자의 이용행위가 개시된 때에 실행의 착수가 있다는 견해”

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

## 231. `art250_sec1_17.direct_active_euthanasia_negative`

- proposition: 적극적·직접적 안락사는 남용 위험, 생명경시, 절대적 생명보호 원칙 위배 및 진통제로 고통 완화 가능성 때문에 허용될 수 없다는 부정설이 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 적극적·직접적 안락사의 허용을 부정하는 학설상 견해다. 긍정설 및 보고된 판례와 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.17_80` / `Ⅰ.17`: “부정설은, 이를 허용하는 경우 남용의 위험이 있고 생명 경시 현상이 나타날 수 있으며, 절대적 생명보호의 원칙에 위배될 뿐만 아니라 고통은 대부분 진통제 투여에 의하여 진정시킬 수 있다는 등의 취지이다.”

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

## 232. `art250_sec1_19.excessive_execution_death_precedent`

- proposition: 상해 또는 중상해를 교사받은 자가 이를 넘어 살인을 실행한 경우, 일반적으로 교사자는 상해죄 또는 중상해죄의 책임을 지되 피해자 사망 결과에 대한 과실 또는 예견가능성이 있으면 상해치사죄 책임도 질 수 있다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: reported precedent의 원판결 확인 전에는 경쟁 견해와의 선택을 유보한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “교사자에게 피해자의 사망이라는 결과에 대하여 과실 내지 예견가능성이 있는 때에는 상해치사죄의 죄책을 지울 수 있”
  - `comm_001692_제250조_Ⅰ.19_94` / `Ⅰ.19`: “다는 것이 판례의 입장이다.”

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

## 233. `art250_sec1_21.death_penalty_special_circumstances_majority`

- proposition: 범행 동기·경위, 계획·준비, 수단, 잔혹성, 인명 경시 태도, 피해자 관계·수와 결과 등을 종합하여 법정 최고형이 불가피한 경우 사형 선고를 정당화할 특별한 사정이 인정될 수 있다는 전원합의체 다수의견이 소개되어 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 반대의견의 증명기준 및 현재위협 요건과 경쟁한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.21_115` / `Ⅰ.21`: “범행 동기와 경위, 범행 계획의 내용과 대상, 범행의 준비 정도와 수단, 범행의 잔혹성, 피고인이 내보인 극단적인 인명 경시 태도, 피해자들과의 관계, 피해자의 수와 피해결과의 중대함”
  - `comm_001692_제250조_Ⅰ.21_115` / `Ⅰ.21`: “법정 최고형의 선고가 불가피하므로 피고인에 대한 사형 선고가 정당화될 수 있는 특별한 사정이 있다.”

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

## 234. `art250_sec1_3.birth_labor_theory`

- proposition: 진통설은 규칙적 진통을 동반하여 태아의 분만이 개시된 때를 살인죄상 사람의 시기로 본다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 출생 시기에 관한 경쟁 학설 중 진통설을 별도 보존한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_3` / `Ⅰ.3`: “진통설은 규칙적 진통을 동반하면서 태아의 분만이 개시된 때를 사”
  - `comm_001692_제250조_Ⅰ.3_3` / `Ⅰ.3`: “람의 시기라고 한다.”

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

## 235. `art250_sec1_3.pulse_cessation_organ_removal`

- proposition: 맥박종지설에서는 뇌사자는 아직 살아 있는 사람이므로 뇌사자로부터 장기를 적출하면 살인죄 구성요건에 해당한다고 본다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 맥박종지설의 장기적출 관련 귀결을 별도 보존한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_8` / `Ⅰ.3`: “맥박종지설에서는 뇌사자는 아직 살아 있는 사람이므로, 뇌사자로부터 장기를 적출하는 경우 살인 죄의 구성요건에 해당한다고 본다.”

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

## 236. `art250_sec1_3.organ_transplant_law_limited_effect`

- proposition: 장기등 이식에 관한 법률의 뇌사자 장기이식 허용만으로 사람의 종기를 뇌사로 단정할 필연적 이유는 없고, 이는 장기적출을 명문화하여 법적 불안정을 해소하거나 제한된 위법성조각사유가 된다는 반대 입장이 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 장기이식법의 효과를 사람의 종기와 분리하는 반대 입장을 보존한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_9` / `Ⅰ.3`: “장기등 이식에 관한 법률이 뇌사자의 장기이식을 법적으로 허용한 다고 해서 사람의 종기를 뇌사로 단정해야 할 필연적 이유는 되지 않고”
  - `comm_001692_제250조_Ⅰ.3_9` / `Ⅰ.3`: “단지 뇌사자의 장기 적출을 명문화함으로써 법적 불안정상태를 해소한 것이라거나, 살해금지를 제한된 범위에서 법적으로 허용해 주는 위법성조각사유 중 하나가 될 뿐이라는 등의 반대 입장”

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

## 237. `art250_sec2_10.arson_death_parricide_imaginary_concurrence`

- proposition: 개정 형법 이후 현주건조물방화치사와 존속살해죄는 상상적 경합범이 성립하고 중한 죄인 존속살해죄로 처벌된다는 학설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 현주건조물방화치사와 존속살해의 관계에 관한 학설상 상상적 경합 견해로서, 인용문이 불완전하므로 원문 및 개정 후 법정형을 확인해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.10_141` / `Ⅱ.10`: “다만 학설상 으로는 현주건조물방화죄와 존속살해죄의 상상적 경합범이 성립한다 (중한 죄인 는 견해가 있다.”

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

## 238. `art250_sec2_6.adoption_type_determines_offense`

- proposition: 개정 민법 시행 후 일반양자가 실부모를 살해하면 존속살해죄, 친양자인 경우에는 보통살인죄가 성립한다는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 실부모 살해에 관한 경쟁 견해 중 하나이며, 개정 민법 시행 후 입양 유형을 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_136` / `Ⅱ.6`: “ⅲ) 개정 민법 시행 이 후 일반양자의 경우에는 존속살해죄가, 친양자의 경우에는 보통살인죄가 성립한 다는 견해”

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

## 239. `art250_sec2_6.deceased_spouse_lineal_ascendant_ordinary_murder`

- proposition: 사망한 배우자의 직계존속은 포함되지 않아, 이를 살해한 경우 보통살인죄만 성립한다는 다수설이 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 사망한 배우자의 직계존속에 관한 다수설로서 반대 견해와 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.6_136` / `Ⅱ.6`: “배우자의 직계존속이라 함은 생존배우자의 직계존속을 의미하고 사망한 배 우자의 직계존속은 포함하지 않으므로, 이 경우에는 보통살인죄만 성립한다는 것이 다수설이다.”

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

## 240. `art250_sec2_9.nonstatus_accomplice_parricide_coprincipal_punished_ordinary`

- proposition: 비신분자가 존속살해에 가담한 경우에도 존속살해죄의 공동정범이지만 형법 제33조 단서에 따라 보통살인죄로 처벌된다는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 비신분자에게 존속살해 공동정범 성립을 인정하되 제33조 단서에 따라 보통살인죄로 처벌하는 견해다. 대립 견해 및 소개된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.9_139` / `Ⅱ.9`: “따라서 이 경우 비신분자도 형법 제33조 본문에 의해 존속살해죄의 공동정범이 되지만 형법 제33조 단서에 의해 보통살인죄로 처벌된다고 한다.”

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
