# 상해·특수상해·상해치사 RuleIR 카드 검수 1

- unit: `intentional_bodily_injury`
- articles: art257, art2582_2, art259, art263
- cards: 1–15 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #21 `art257_sec1_2.prenatal_injury_postnatal_result`: `art257_sec1_2.prenatal_injury_postnatal_result_negative` (status=`valid`)
- #22 `art257.pregnancy_injury`: `art257.pregnancy_not_injury` (status=`valid`)
- #23 `art257.drug_method`: `art257.drug_intangible_method` (status=`valid`)
- #24 `art259_sec1_1.second_act_liability`: `art259_sec1_1.second_act.single_offense_holding` (status=`valid`)

## 1. `art257.cosmetic_pubic_hair_change_case_negative`

- proposition: 음모 모근은 남기고 모간 일부만 잘라 전체 외관에 변형만 생긴 경우 상해 성립을 부정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 외관 변형만이 확인된 특정 음모 절단 사례의 소개에 한정된다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_15` / `Ⅰ.3`: “피해자의 음모 모근 부분을 남기고 모간 부분만을 일부 잘라냄으로써 음모의 전체적인 외관에 변형만이 생긴 경우”

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

## 2. `art257.diagnosis_evidentiary_value`

- proposition: 피해자의 상해진단서는 특별한 사정이 없으면 피해자 진술과 함께 상해 사실의 유력한 증거가 되며 합리적 근거 없이 증명력을 배척할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 상해진단서의 증명력은 개별 사건의 특별한 사정과 다른 증거를 함께 평가해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_10` / `Ⅰ.3`: “피해자가 제출한 상해진단서는 특별한 사정이 없는 한 피해자의 진술과 더불어 피고인의 상해 사실에 대한 유력한 증거가 되고, 합리적인 근거 없이 그 증명력을 함부로 배척할 수 없다.”

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

## 3. `art257.drug_induced_unconsciousness`

- proposition: 수면제와 같은 약물 투약으로 건강상태가 불량하게 변경되고 생활기능 장애가 초래되면, 자연 회복하거나 외부 상처가 없더라도 강간치상죄 또는 강제추행치상죄의 상해에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 약물 투여의 방법론적 분류에 관한 별도 견해 대립과는 구별하여, 결과적 상해 해당성을 검토한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “수면제와 같은 약물을 투약하여 피해자를 일시적으로 수면 또는 의식불명 상태에 이”
  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “르게 한 경우에도 약물로 인하여 피해자의 건강상태가 불량하게 변경되고 생활기능”
  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “에 장애가 초래되었다면 자연적으로 의식을 회복하거나 외부적으로 드러난 상처가 없더라도 이는 강간치상죄나 강제추행치상죄에서 말하는 상해에 해당한다.”

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

## 4. `art257.external_injury_not_required`

- proposition: 보행불능, 수면장해, 식욕감퇴 등 기능장해가 발생하면 외관상 상처가 없더라도 상해에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 기능장해의 존재 및 폭행과의 인과관계는 개별 사실관계에서 판단해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_8` / `Ⅰ.3`: “‘타인의 신체에 폭행을 가하여 보행불능, 수면장해, 식욕감태 등 기능의 장해를 일으킨 때에는 외관상 상처가 없더라도 형법상 상해를 입힌 경우에 해당한다’”

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

## 5. `art257.hair_nails_cutting_not_injury`

- proposition: 두발·수염·액모·음모·눈썹·손톱·발톱의 절단은 경우에 따라 폭행에 해당할 수 있으나 상해라고 할 수 없다는 설명이 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 절단 이외의 건강상태 악화 또는 기능장해가 있는 경우까지 배제하는 규범으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “두발, 수염, 액모(腋⽑, 겨드랑이 털), 음모(陰⽑), 눈썹, 손톱, 발톱 등”
  - `comm_001692_제257조_Ⅰ.3_6` / `Ⅰ.3`: “의 절단은 경우에 따라 폭행에 해당할 수는 있어도 상해라고 할 수는 없을 것이”

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

## 6. `art257.hickey_case_negative`

- proposition: 강간 도중 어깨를 입으로 빨아 생긴 동전 크기 반상출혈이 있으나 통증이나 자각증상이 없었던 경우 상해 성립을 부정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 통증 또는 자각증상이 없던 특정 반상출혈 사례에 한정된다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_14` / `Ⅰ.3`: “강간 도중 흥분하여 피해자의 어깨를 입으로 빨아서 생긴 동전 크기 정도의 반상출혈 상을 입힌 경우(피해자는 별다른 통증이나 자각증상을 느끼지 못하였으나”

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

## 7. `art257.injury_beyond_ordinary_minor_wound`

- proposition: 폭행 없이도 일상생활 중 발생하거나 합의 성교행위에서 통상 발생할 수 있는 상처의 정도를 넘는 상처가 생긴 경우에는 상해에 해당한다는 판례 설명이 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 통상 발생 가능한 상처의 범위와 이를 넘는 정도는 개별 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_9` / `Ⅰ.3`: “그러한 정도를 넘는 상처가 생긴 경우라면 상해에 해당한다고 한다.”

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

## 8. `art257.intangible_methods`

- proposition: 상해의 수단이나 방법에는 제한이 없고, 해악의 통고로 공포·경악하게 하거나 음향 위협으로 정신장애를 일으키는 무형적 방법에 의한 상해도 가능하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 무형적 수단이 실제 건강상태 악화 또는 정신장애를 초래했는지는 개별적으로 판단해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “상해의 수단이나 방법에는 제한이 없다. 통상 폭행 등 유형적 방법을 수단으로 할 것이나, 해악을 통고하여 사람을 공포·경악하게 하거나 음향에 의한 위협”
  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “으로 정신장애를 일으키는 등 무형적 방법에 의한 상해도 있을 수 있다.”

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

## 9. `art257.minor_abrasion_case_negative`

- proposition: 넘어지며 팔꿈치 피부가 직경 약 2cm 벗겨졌으나 치료나 진단서 없이 연고를 바르고 생활 지장 없이 2~3일 후 나은 경우 상해 성립을 부정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 치료 없이 단기간 회복되고 생활상 지장이 없었던 구체적 사례에 한정된다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_15` / `Ⅰ.3`: “피해자가 넘어지면서 오른쪽 팔꿈치가 땅에 닿아 피부가 직경 2㎝ 정도 약간 벗겨져 병원에서 치료를 받거나 진단서를 발급받지 않고 연고를 바른 후 생활에 지장이 없이 2~3일 후 낫게 된 경우”

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

## 10. `art257.minor_injury_exclusion`

- proposition: 상처가 극히 경미하여 치료할 필요 없이 자연치유되고 일상생활에 지장이 없는 경우에는 건강상태의 불량 변경이나 생활기능 장애가 인정되기 어려워 상해에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 경미성, 치료 필요성, 자연치유 및 일상생활 지장 여부를 구체적 사실로 평가해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_9` / `Ⅰ.3`: “‘상처가 극히 경미한 것”
  - `comm_001692_제257조_Ⅰ.3_9` / `Ⅰ.3`: “으로서 굳이 치료할 필요가 없어서 자연적으로 치유되며 일상생활을 하는 데 아무런 지장이 없는 경우’에는 신체의 건강상태가 불량하게 변경되었다거나 생”
  - `comm_001692_제257조_Ⅰ.3_9` / `Ⅰ.3`: “활기능에 장애를 초래한 것으로 보기 어렵다는 이유로 상해에 해당하지 아니한”

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

## 11. `art257.minor_palm_scratch_case_negative`

- proposition: 강간미수 과정에서 손바닥에 약 2cm의 가벼운 긁힌 상처가 생겼으나 당일 통증이 사라진 경우 상해 성립을 부정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 상처의 경미성 및 당일 통증 소실이 확인된 사례에 한정된다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_14` / `Ⅰ.3`: “피해자를 강간하려다가 미수에 그치고 그 과정에서 피해자의 손바닥에 약 2cm 정도 긁힌 가벼운 상처가 발생한 경우”
  - `comm_001692_제257조_Ⅰ.3_14` / `Ⅰ.3`: “그 날 오후 병원에 갈 때는 피도 비치지 않았고, 통증 도 없었으며”

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

## 12. `art257.omission_injury`

- proposition: 상해는 부작위로도 성립할 수 있으며, 부양의무자가 피부양자에게 음식이나 병자에게 의약품을 공급하지 않아 건강을 해친 경우가 예시된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 부작위 책임의 전제가 되는 부양의무 및 건강 침해의 인과관계를 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “상해는 작위뿐만 아니라 부작위에 의해서도 성립한다. 예컨대 부양의무 있는 자”
  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “가 피부양자에게 음식을 주지 아니하거나 병자에게 의약품을 공급하지 아니하”
  - `comm_001692_제257조_Ⅰ.3_17` / `Ⅰ.3`: “여 건강을 해치게 한 경우에는 부작위에 의한 상해죄가 성립할 수 있을 것이다.”

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

## 13. `art257.precedent_health_life_function`

- proposition: 판례의 주류적 입장은 피해자 신체의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래되는 것을 상해로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주류 판례 입장으로 보고되지만, 원판례 확인 전에는 commentary-reported authority로 취급한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_8` / `Ⅰ.3`: “인 판례는 ‘피해자 신체의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래되”
  - `comm_001692_제257조_Ⅰ.3_8` / `Ⅰ.3`: “는 것을 말하는 것’이라고 하여 생리적 기능 훼손설의 입장을 명확히 하고 있다.”

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

## 14. `art257.pubic_hair_appearance_only`

- proposition: 음모 모근을 남기고 모간 일부를 잘라 외관만 변형된 경우, 수치심이 발생하더라도 건강상태의 병리적 악화나 생활기능 장애가 없다면 강제추행치상죄의 상해에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수치심과 건강상태의 병리적 악화 또는 생활기능 장애를 구별하는 사례로 검토한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_7` / `Ⅰ.3`: “피해자의 음모의 모근 부분을 남기”
  - `comm_001692_제257조_Ⅰ.3_7` / `Ⅰ.3`: “고 모간 부분만을 일부 잘라냄으로써 음모의 전체적인 외관에 변형만이 생겼다면, 이로 인”
  - `comm_001692_제257조_Ⅰ.3_7` / `Ⅰ.3`: “하여 피해자에게 수치심을 야기하기는 하겠지만, 병리적으로 보아 피해자의 신체의 건강상”
  - `comm_001692_제257조_Ⅰ.3_7` / `Ⅰ.3`: “태가 불량하게 변경되거나 생활기능에 장애가 초래되었다고 할 수는 없을 것이므로”

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

## 15. `art257.rape_functional_impairment_case`

- proposition: 강간으로 외관상 상처가 없어도 보행불능, 수면장해, 식욕감퇴 등의 장해가 생긴 경우 상해 성립을 긍정한 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 외관상 상처가 없는 기능장해의 발생과 범행 사이의 관계를 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제257조_Ⅰ.3_10` / `Ⅰ.3`: “강간으로 인하여 외관상의 상처는 없지만 보행불능, 수면장해, 식욕감퇴 등 의 장해가 야기된 경우”

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
