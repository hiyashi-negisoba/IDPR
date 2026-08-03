# 범인은닉·도피 RuleIR 카드 검수 4

- unit: `harboring_offender`
- articles: art151
- cards: 46–58 / 58
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art151_sec2_4.clergy_active_assistance_not_justified`

- proposition: 성직자가 범인에게 적극적으로 은신처를 마련하거나 도피자금을 제공하는 행위는 정당한 직무 범위를 넘어 사회상규상 정당행위로 위법성이 조각되지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 성직자의 직무 범위 및 적극적 지원의 사실적 경계를 평가해야 하며, 소개된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.4_24` / `Ⅱ.4`: “적극적으로 은신처를 마련하여 주고 도피자금을 제공하는 따위의 일은 이미 그 정당한 직무의 범위를 넘는 것이며 이를 가리켜 사회상규에 반하지 아니하여 위법성이 조각되는 정당행위라고 할 수 없다.”

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

## 47. `art151_sec2_4.family_support_social_adequacy`

- proposition: 미국으로 도피한 범인의 가족에게 생활비를 지급하거나 범인의 자녀를 미국으로 보내기 위해 공항까지 안내한 행위는 사회적 상당성이 있어 위법성이 조각된다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판단의 구체적 사실관계와 원문 판결을 확인한 뒤 사회적 상당성 예외의 적용 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.4_24` / `Ⅱ.4`: “미국으로 도피한 범인의 가족들에게 생활 비를 지급하거나 범인의 자녀들을 미국으로 보내기 위하여 공항까지 안내한 행 위에 대하여 사회적 상당성이 있어 위법성이 조각된다는 취지로 판단하였다.”

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

## 48. `art151_sec2_5.self_escape_instigation_abuse_of_defense_precedent`

- proposition: 범인이 타인에게 허위자백을 하게 하는 등 방어권 남용으로 범인도피죄를 범하게 한 경우에는 범인도피교사죄가 성립할 수 있고, 방어권 남용 여부는 행위 태양·내용, 관계, 구체적 상황 및 형사사법작용에 미칠 위험 정도를 종합해 판단한다는 대법원 법리가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글이 소개한 대법원 법리이다. 원판례를 사용자 primary precedent index에서 확인하기 전에는 방어권 남용 기준을 확정 정책으로 채택하지 않는다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.5_26` / `Ⅱ.5`: “범인이 타인으로 하여 금 허위의 자백을 하게 하는 등으로 범인도피죄를 범하게 하는 경우와 같이 그것이 방어권의 남용으로 볼 수 있을 때에는 범인도피교사죄에 해당할 수 있다.”
  - `comm_001692_제151조_Ⅱ.5_26` / `Ⅱ.5`: “방어권의 남용이라고 볼 수 있는지 여부는, 범인을 도피하게 하는 것 이라고 지목된 행위의 태양과 내용, 범인과 행위자의 관계, 행위 당시의 구체 적인 상황, 형사사법의 작용에 영향을 미칠 수 있는 위험성의 정도 등을 종합 하여 판단하여야 할 것이다.”

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

## 49. `art151_sec2_6.duty_officer_escape_only`

- proposition: 범인을 알고 적절한 조치를 취할 직무상 의무가 있는 사람이 범인을 도피하게 하여 직무를 유기한 경우, 원칙적으로 범인도피죄만 성립하고 직무유기죄는 별도로 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 직무상 의무, 도피행위 및 직무유기 사이의 사실관계 판단과 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.6_27` / `Ⅱ.6`: “범인을 알고 적절한 조치를 취하여야 할 직무상 의무가 있는 사람이 범인을 도피하게 하여 직무를 유기한 경우에는 원칙적으로 범인도피죄만 성립하고 직무 유기죄는 별도로 성립하지 않는다는 것이 판례이다.”

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

## 50. `art151_sec2_6.fabricated_evidence_obstruction`

- proposition: 허위 진술에 그치지 않고 적극적으로 조작한 허위 증거를 제출하여, 수사기관이 충실히 수사해도 그 허위성을 발견하지 못할 정도에 이르면 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 조작 증거의 적극성 및 충실한 수사에도 허위성을 발견하지 못할 정도인지는 개별 사실에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.6_28` / `Ⅱ.6`: “그러나 허위 진술을 하는 데 그치지 않고 적극적으로 조작된 허위의 증거를 제출하고 그 증거 조작의 결과 수사기관이 그 진위에 관하여 나름대로 충실한 수사를 하더라도 제출된 증거가 허위임을 발 견하지 못할 정도에 이르렀다면 위계에 의한 공무집행방해죄가 성립한다.”

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

## 51. `art151_sec2_6.false_confession_by_suspect`

- proposition: 범인이 아닌 피의자가 수사기관에서 자신이 범죄를 저지른 것처럼 허위 자백한 경우, 위계에 의한 공무집행방해죄는 성립하지 않는다는 판례 법리가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 제공된 인용문은 보고된 사안의 도입부이므로, 불성립 결론과 적용 범위는 판례 원문 및 인접 원문으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.6_28` / `Ⅱ.6`: “대 법원은 일찍이 범인이 아닌 피의자가 수사기관에서 자신이 범죄를 저지른 것처 럼 허위의 자백을 한 사안에서”

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

## 52. `art151_sec2_6.false_statement_by_witness`

- proposition: 참고인이 수사기관에서 허위 진술을 한 경우에도, 피의자의 허위 자백에 관한 법리가 마찬가지로 적용된다고 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 참고인 허위 진술에 적용되는 법리의 내용과 한계는 피의자 허위 자백 관련 판례 원문과 함께 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.6_28` / `Ⅱ.6`: “그리고 이와 같은 법리는 참고인이 수사기관에서 허위 진술을 한 경우에도 마찬가지로 적용된다.”

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

## 53. `art151_sec2_6.military_deserter_harboring_special_law`

- proposition: 범인은닉죄와 군형법상 이탈자비호죄의 구성요건을 모두 충족하는 행위는 특별관계에 따라 군형법상 이탈자비호죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 두 구성요건이 모두 충족된 경우에 한정된 특별관계 예외로 검토한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.6_28` / `Ⅱ.6`: “군형법 제32조에서 규정하 는 이탈자비호죄는 본죄에 대하여 특별관계에 있으므로 본죄와 군형법 제32조 의 구성요건을 모두 충족시키는 행위의 경우 군형법상 이탈자비호죄만 성립한 다.”

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

## 54. `art151_sec3_2.covered_relatives`

- proposition: 형법 제151조 제2항의 적용 대상인 혈족은 8촌 이내의 혈족이고, 인척은 4촌 이내의 인척이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 혈족 및 인척의 촌수 범위를 열거하는 정의 카드다.
- bounded sources:

  - `comm_001692_제151조_Ⅲ.2_33` / `Ⅲ.2`: “따라서 형법 제151조 제2 (제777조) 항의 적용 대상인 혈족은 ‘8촌 이내의 혈족’을, 인척은 ‘4촌 이내의 인척’을 각각 의미한다.”

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

## 55. `art151_sec3_2.criminal_benefit_objective_test`

- proposition: 행위가 본인의 형사상 이익을 위한 것인지는 행위자의 주관적 의사가 아니라 객관적 사정을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 형사상 이익 여부는 객관적 사정의 종합평가를 요구한다.
- bounded sources:

  - `comm_001692_제151조_Ⅲ.2_34` / `Ⅲ.2`: “형사상 이익이 되는지 여부는 행위자의 주관 적 의사에 따를 것이 아니고 객관적인 사정을 종합하여 판단하여야 한다.”

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

## 56. `art151_sec3_2.for_benefit_of_principal`

- proposition: 제151조 제2항의 ‘본인을 위하여’란 범죄 인지·공소제기·유죄판결·형집행의 회피 또는 수사·재판에서의 불구속 상태 유지 등 국가 형사사법작용 전반에서 본인의 절차적 또는 실체적 형사상 이익을 위한 경우를 뜻한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 본인의 형사상 이익 여부는 구체적 절차상 이익에 대한 포섭이 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅲ.2_34` / `Ⅲ.2`: “이때 ‘본 인을 위하여’는 범죄의 인지, 공소 제기, 유죄 판결의 선고, 형 집행 등을 면하는 것, 수사 및 재판 과정에서 불구속 상태를 유지하는 것 등 국가의 형사사법작용 전반에 있어서 본인의 절차적 또는 실체적 이익”

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

## 57. `art151_sec3_2.non_criminal_benefit_exclusion`

- proposition: 오로지 공범의 이익을 위한 경우, 본인에게 불이익한 경우 및 본인에게 이익이 있어도 재산상 이익이나 명예 유지 등 형사상 이익이 아닌 경우는 ‘본인을 위하여’에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: ‘본인을 위하여’ 요건에서 명시적으로 제외되는 경우를 별도 예외로 보존한다.
- bounded sources:

  - `comm_001692_제151조_Ⅲ.2_34` / `Ⅲ.2`: “따라서 오로지 공범의 이익을 위한 경우나 본인”
  - `comm_001692_제151조_Ⅲ.2_34` / `Ⅲ.2`: “에게 이익이 되지 않고 오히려 불이익한 경우가 제외됨은 물론이고, 설령 본인 에게 이익이 되더라도 형사상 이익이 아닌 경우”

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

## 58. `art151_sec3_3.nonrelative_accomplice`

- proposition: 친족과 비친족이 공모하거나 실행행위를 분담하여 범인은닉죄를 저지른 경우, 친족은 제151조 제2항에 따라 처벌되지 않지만 비친족은 본죄로 처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 친족과 비친족의 공모 또는 실행행위 분담의 범위와 각자의 처벌 여부를 사실관계에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅲ.3_36` / `Ⅲ.3`: “따라서 친족과 비친족이 공모하거나 실행 행위를 분담하여 본 죄를 저지른 경우 친족은 형법 제151조 제2항이 적용되어 처벌할 수 없으나 (따라 비친족은 본죄로 처벌된다.”

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
