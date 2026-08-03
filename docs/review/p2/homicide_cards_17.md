# 살인·존속살해 RuleIR 카드 검수 17

- unit: `homicide`
- articles: art250, art254, art255
- cards: 241–242 / 242
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

## 241. `art250_sec2_9.status_instigator_parricide_accomplice`

- proposition: A가 B를 교사 또는 방조하여 A의 부를 살해하게 한 경우, A는 존속살해죄의 교사 또는 방조범이고 B는 보통살인죄의 정범이라는 통설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 신분자인 A에게 존속살해의 교사 또는 방조범을 인정하는 견해다. 공범종속성원칙에 따라 A도 보통살인죄 교사범이라고 보는 대립 견해와 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.9_139` / `Ⅱ.9`: “ⅱ) A가 B를 교사 또는 방조하여 A의 부를 살해하게 하면 A는 존속살해죄의 교사 또 는 방조범, B는 보통살해죄의 정범이 된다고 본다.”

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

## 242. `art255_sec4.preparation_desistance_doctrinal_variants`

- proposition: 실행 착수 전 예비·음모를 자발적으로 중지하거나 실행 착수를 포기한 경우 중지미수 규정을 적용할지에 관하여 부정설과 긍정설의 대립이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 실행 착수 전 예비·음모의 자발적 중지 또는 실행 착수 포기에 중지미수 규정을 적용할지에 관한 학설 대립으로, 어느 견해도 선택하지 않았다.
- bounded sources:

  - `comm_001692_제255조_Ⅳ_4` / `Ⅳ`: “학설상으로는 이를 부정하는 견해와 긍정하는 견해”

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
