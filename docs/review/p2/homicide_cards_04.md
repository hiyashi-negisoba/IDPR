# 살인·존속살해 RuleIR 카드 검수 4

- unit: `homicide`
- articles: art250, art254, art255
- cards: 46–60 / 242
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

## 46. `art250_sec1_15.confinement_omission_conditional_intent`

- proposition: 피해자가 사망할 가능성을 인식하면서도 사경의 피해자를 병원으로 옮기지 않고 방치한 경우, 사망 결과를 용인한 살인의 미필적 고의가 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사경 피해자를 이송하지 않고 방치한 부작위 사례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_66` / `Ⅰ.15`: “피고인이 위와 같은 결과 발생의 가능성을 인정하고 있으면서도 피해자를 병원에 옮기지 않고 사경에 이른 피해자를 그대로 방치한 소위 (所爲) 에는 그로 인하여 피해자가 사망하는 결과가 발생하더라도 용인할 수밖에 없다 는 내심의 의사 즉 살인의 미필적 고의가 있었다고 볼 수 있다.”

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

## 47. `art250_sec1_15.continued_club_head_assault`

- proposition: 각목으로 피해자의 머리를 여러 차례 강타하고 피해자가 쓰러진 뒤에도 계속 머리를 때려 사망하게 한 경우 살인의 범의를 인정하기에 충분하다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 계속된 각목 두부 폭행 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_57` / `Ⅰ.15`: “피고인에게는 살인의 범의가 있었다고 보기에 충분하다.”

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

## 48. `art250_sec1_15.doctor_treatment_withdrawal_aiding`

- proposition: 위 치료중단 사건에서 담당의사들은 살인죄의 고의는 인정되지만, 보호자의 부작위 살해행위에 대한 방조범의 죄책만 진다는 대법원 결론이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 치료중단 사안에서 공동정범이 아닌 방조범으로 본 보고된 결론이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “B, C가 살인죄의 공동정범”
  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “이 아니라 A의 부작위에 의한 살해행위에 대한 방조범의 죄책만 진다고 봄으”

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

## 49. `art250_sec1_15.doctor_treatment_withdrawal_intent`

- proposition: 인공호흡기를 부착한 중환자에 대한 치료를 중단하고 인공호흡기 제거를 지시한 담당의사들이 사망 가능성·위험성을 예견·인식한 경우, 보호자 요청으로 마지못해 치료를 중단했더라도 미필적 살인의 고의를 부정하기 어렵다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 치료중단 담당의사의 고의에 관한 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_59` / `Ⅰ.15`: “이 비록 A의 요청에 의하여 마지못해 치료를 중단하였더라도 그 당시 피해자”
  - `comm_001692_제250조_Ⅰ.15_59` / `Ⅰ.15`: “의 사망이라는 결과 발생에 대한 미필적 인식 내지 예견마저 없었다고 보기는 어려우므로, 피고인들에게 정범의 고의가 없다고 본 원심의 판단은 잘못된 것”

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

## 50. `art250_sec1_15.generalized_intent_burial_holding`

- proposition: 살해 의도의 구타로 직접 사망하지 않고 죄적 인멸 목적의 매장행위로 사망하였더라도, 전 과정을 개괄적으로 보아 처음 예견한 피해자 살해가 실현되면 살인죄 책임을 면할 수 없다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 경쟁 학설과 별도로 보존한 매장행위 사안의 보고된 대법원 판시다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_68` / `Ⅰ.15`: “피고인들이 살해의 의도로 행한 구타 행위에 의하여 직접 사망한 것이 아니라 죄적을 인멸할 목적으로 행한 매장행위에 의하여 사망하게 되었다 하더라도, 전 과정을 개괄적으로 보면 피해자의 살해라는 처음에 예견된 사실이 결국은 실현된 것으로서 피고인들은 살인죄의 죄책 을 면할 수 없다.”

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

## 51. `art250_sec1_15.group_assault_weapons_conditional_intent`

- proposition: 치명적 부위를 낫이나 칼로 찌르지 않았더라도 쇠파이프·각목으로 머리와 몸을 마구 때리고 낫으로 팔과 다리를 난자한 경우 사망 가능성에 대한 인식, 즉 미필적 살인의 고의를 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 집단 폭행의 구체적 수단과 부위에 기초한 판례 소개다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_55` / `Ⅰ.15`: “쇠파이프와 각목으로 피해자들의 머리와 몸을 마구 때리고 낫으로 팔과 다리를 난 자한 이상”
  - `comm_001692_제250조_Ⅰ.15_55` / `Ⅰ.15`: “, 위 피고인들이 자기들의 가”
  - `comm_001692_제250조_Ⅰ.15_55` / `Ⅰ.15`: “해행위로 인하여 피해자들이 사망할 수도 있다는 사실을 인식하지 못하였다고 볼 수 없다(오히려 살인의 미필적 고의가 있었다고 볼 수 있다).”

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

## 52. `art250_sec1_15.inducing_young_children_to_drown`

- proposition: 자살 의미를 이해할 능력이 없고 피고인의 말에 복종하는 어린 자녀들에게 함께 죽자고 권유하여 물에 들어오게 해 익사시킨 경우, 직접 물에 밀어 넣지 않았더라도 살인죄의 범의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 어린 자녀를 권유하여 익사시킨 사안의 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_61` / `Ⅰ.15`: “비록 피해자들을 물속에 직접 밀어서 빠뜨리지는 않았더라도, 자살의 의미를 이해할 능력이 없고 피고인의 말”
  - `comm_001692_제250조_Ⅰ.15_61` / `Ⅰ.15`: “이라면 무엇이나 복종하는 어린 자식들을 권유하여 익사하게 한 이상, 살인죄의 범의는 있었음이 분명하다.”

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

## 53. `art250_sec1_15.loaded_shotgun_reject_accident`

- proposition: 사냥과 무관한 상황에서 실탄이 장전된 엽총을 안전장치 없이 방아쇠에 손을 댄 채 사용하여 피해자를 사망하게 한 경우, 단순 오발사고라는 변소를 배척하고 살인의 고의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 장전 엽총 사용에 관한 오발 변소 배척 사례다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “인의 변소처럼 피해자를 겁주려고 협박하다가 피해자의 접촉행위로 생겨난 단”
  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “순한 오발사고가 아니라, 살인의 고의가 있는 범죄행위였다고 보기에 그 증거가 충분하다.”

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

## 54. `art250_sec1_15.martial_arts_vital_point_strike`

- proposition: 무술교관 출신 피고인이 인체 급소를 잘 알면서 무술 방법으로 피해자의 울대를 가격하여 사망하게 한 경우 살인의 범의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 무술교관의 울대 가격 사안에 관한 보고된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “피고인이 무술교관 출신으로서 인체의 급소를 잘 알고 있으면서도, 무술의 방”
  - `comm_001692_제250조_Ⅰ.15_60` / `Ⅰ.15`: “법으로 피해자의 울대를 가격하여 피해자를 사망케 한 행위에 살인의 범의가 있다고 판단하여 살인의 점에 관한 공소사실을 유죄로 인정한 조치는 정당하”

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

## 55. `art250_sec1_15.method_error_precedent`

- proposition: 판례는 방법의 착오가 있어도 살인의 범의 성립에 방해되지 않는다는 취지로 판시하여 기본적으로 법정적 부합설의 입장으로 소개된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 경쟁 학설과 별개로 해설이 소개한 판례 입장이다; 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_67` / `Ⅰ.15`: “판례는 방법의 착오가 있는 경우에도 살인 범의의 성립에 방해가 되지 않는다 는 취지로 판시함으로써, 기본적으로 법정적 부합설의 입장인 것으로 보인다.”

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

## 56. `art250_sec1_15.murder_intent_definition`

- proposition: 살인죄의 고의는 살아 있는 사람이라는 객체 인식과 자신의 행위로 사망 결과가 초래될 수 있다는 인식 및 인용을 의미하며, 인과관계 인식도 그 내용이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살인의 고의 내용을 정리한 해설상 정의다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_52` / `Ⅰ.15`: “살인죄의 고의는 사람을 살해한다는 인식과 의사를 의미한다. 즉 ‘살아 있는 사람’이라는 객체에 대한 인식과 함께, 자신의 행위로 인해 사망의 결과가 초래될 수 있다는 인식 및 인용이 있어야 한다. 인과관계의 인식도 고의의 내용이 된다.”

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

## 57. `art250_sec1_15.murder_intent_objective_circumstances`

- proposition: 피고인이 살인의 범의는 없고 상해 또는 폭행의 범의만 있었다고 다투는 경우, 살인의 범의는 범행 경위·동기·흉기 유무·종류·용법·공격 부위와 반복성·사망 결과·발생가능성 등 객관적 사정을 종합해 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 개별 사실의 종합평가를 요구하는 판례 소개 기준이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_53` / `Ⅰ.15`: “피고인에게 범행 당시 살인의 범의가 있 었는지 여부는, 피고인이 범행에 이르게 된 경위, 범행의 동기, 준비된 흉기의 유무·종류·용법, 공격의 부위와 반복성, 사망의 결과, 발생가능성 정도 등 범행 전후의 객관적인 사정을 종합하여 판단해야 한다.”

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

## 58. `art250_sec1_15.neck_stabbing_conditional_intent`

- proposition: 날카로운 과도로 생명과 직결되는 목 부위를 강하게 찔러 치명적 상처 및 사망 가능성이 큰 사정들을 종합하면 미필적·순간적 살인의 고의를 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 목 부위 과도 찌르기라는 좁은 사례의 판례상 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_53` / `Ⅰ.15`: “범행의 수단인 과도가 길이 19㎝, 칼날 길이 8.5 ㎝의 날카로운 흉기로서 그 사용방법에 따라 사람을 살해하기에 충분한 도구이 고, 피해자의 목 부위는 경동맥이 지나고 있어 이러한 칼에 찔릴 경우 치명적인 상처를 입고 사망에 이를 가능성이 다분한 부위”

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

## 59. `art250_sec1_15.no_murder_intent_no_murder`

- proposition: 살인의 고의 없이 사람을 사망에 이르게 한 경우 과실치사죄·상해치사죄 또는 폭행치사죄가 성립할 수 있어도 살인죄는 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살인의 고의가 없는 경우에 관한 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_52` / `Ⅰ.15`: “살인의 고의 없이 사람을 사망에 이르게 한 때에는 과실치사죄나”
  - `comm_001692_제250조_Ⅰ.15_52` / `Ⅰ.15`: “상해치사죄 또는 폭행치사죄가 성립할 수 있어도 살인죄는 성”
  - `comm_001692_제250조_Ⅰ.15_52` / `Ⅰ.15`: “립하지 않는다.”

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

## 60. `art250_sec1_15.no_parricide_intent_indiscriminate_stabbing`

- proposition: 피고인이 무차별적으로 칼을 휘두르던 중 만류하던 아버지를 한 차례 찔러 사망하게 한 경우, 아버지를 살해하기로 결의할 동기나 이유를 인정할 자료가 없으면 존속살해로 의율할 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 무차별 칼 휘두름 중 부친 사망 사안의 존속살해 제한 판단이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.15_63` / `Ⅰ.15`: “그의 아버지를 살해하기로 결의할 만한 동기나 이유 있음을 인정할 만한 자료가 없으면 존속살해로 의율할 수는 없다.”

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
