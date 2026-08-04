# 범인은닉·도피 RuleIR 카드 검수 3

- unit: `harboring_offender`
- articles: art151
- cards: 31–45 / 58
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art151_sec2_2.omission_concealment_general_citizen`

- proposition: 범인 신고의무가 없는 일반인에게는 부작위에 의한 범인은닉이 인정될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 일반인의 단순 부작위는 은닉행위가 아니라는 한계다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “범인에 대한 신고의무가 없는 일반인의 경우 부작위에 의한 은닉이 인정될 수 없다.”

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

## 32. `art151_sec2_2.omission_escape_guarantor`

- proposition: 부작위로 범인을 도피하게 한 행위를 인정하려면 경찰관 등 범인을 체포해야 할 보증인적 지위가 필요하며, 그러한 지위가 없는 일반인이 범인임을 알면서 수사기관에 인계하지 않은 것만으로는 부작위 범인도피죄가 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 보증인적 지위는 부작위 도피조력의 필요 조건으로 정리한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “부작위에 의하여 도피하게 하는 것도 가능하다. 다만 그 인정을 위해서는 경찰 관 등과 같이 범인을 체포하여야 할 보증인적 지위가 있을 것이 필요하다.”
  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “그러한 보증인적 지위가 있지 않은 일반인이 범인이라는 사정을 알면서 그 범인을 수사기관에 인계하지 않았다고 하여 부작위에 의한 범인도피죄가 성 립하지는 않는다.”

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

## 33. `art151_sec2_2.passive_false_confession`

- proposition: 실제 범행자를 대신하여 자신이 양도소득세 포탈을 한 것처럼 허위진술하였더라도, 적극적 기만수단 없이 소극적으로 혐의를 인정한 데 그치고 추가조사로 실제 주도자를 밝힐 수 있는 경우 범인도피죄가 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소극적 혐의 인정 및 추가 조사 가능성에 한정된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_19` / `Ⅱ.2`: “피고인이 적극적으로 수사기관을 기만하여 착오에 빠지게 함으로써 범인의 발견 또는 체포를 곤란 내지 불가능하게 한 것으로 볼 수 없다 할 것이므로, 원심의 이유 설시에 다소 부적절한 점이 없지 아니하나 피고인에게 무죄를 선고한 원심의 결론은 정당하다.”

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

## 34. `art151_sec2_2.preparatory_conduct`

- proposition: 현실적으로 형사사법작용 방해 위험이 초래되지 않은 행위는 처벌규정 없는 범인도피의 예비에 불과하여 범인도피죄로 처벌할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위험 발생 전의 예비행위와 기수 행위를 구별한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_16` / `Ⅱ.2`: “아직 형사사 법작용을 방해하는 위험을 초래한 데에까지 이른 것은 아니어서 현행법상 처벌규정 이 없는 범인도피의 예비에 불과하므로 범인도피죄로 처벌할 수는 없다.”

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

## 35. `art151_sec2_2.qualifying_offense`

- proposition: 범인은닉죄의 객체인 벌금 이상의 형에 해당하는 죄는 법정형에 벌금 또는 그보다 무거운 형이 포함된 범죄이며, 선고형이 아니라 법정형을 기준으로 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법정형 기준의 객관적 범위다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_3` / `Ⅱ.2`: “법정형에 벌금 또는 그보다 무거운 형이 포함되어 있는 범죄를 말한다. 선고형 이 아니라 법정형이라는 점에 유의하여야 한다.”

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

## 36. `art151_sec2_2.relative_cohabiting_family`

- proposition: 범인의 친족 또는 동거의 가족이 범인을 위하여 은닉하거나 도피하게 한 경우에는 친족간 특례로 책임이 조각되어 처벌되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 친족 또는 동거가족에 관한 특별 취급을 별도 예외로 둔다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “범인의 친족 또는 동거의 가족이 범인을 위하여 범인을 은닉하거나 도피하게 하는 경우에도 처벌되지 않”

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

## 37. `art151_sec2_2.routine_greeting`

- proposition: 범인의 안부를 묻거나 통상적인 인사말을 나누는 정도만으로는 범인을 도피하게 한 것으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 통상적 인사에 한정된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “단순히 범인 의 안부를 묻거나 통상적인 인사말을 나누는 정도만으로는 범인을 도피하였다 고 볼 수 없다고 판단하였다.”

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

## 38. `art151_sec2_2.self_concealment`

- proposition: 범인이 자신을 은닉하거나 도피하게 하는 행위는 범인은닉죄의 구성요건에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 자기은닉·자기도피의 구성요건 비해당을 명시한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “범인이 자기 자신을 은닉 또는 도피하게”
  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “하는 행위는 본죄의 구성요건에 해당하지 않아 처벌되지 않는다.”

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

## 39. `art151_sec2_2.subject_other_than_offender`

- proposition: 범인은닉죄의 주체는 벌금 이상의 형에 해당하는 죄를 저지른 사람인 범인을 제외한 사람이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 범인 본인을 제외하는 주체 범위를 독립적으로 정리한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “본죄의 주체는 ‘벌금 이상의 형에 해당하는 죄를 저지른 사람’ (다음부터 ‘범인’ 을 제외한 나머지 사람이다.”

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

## 40. `art151_sec2_2.supporting_fugitive_family`

- proposition: 범인의 가족을 돕는 행위는 다른 특별한 사정이 없는 한 사회적 상당성이 있어 범인도피죄에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 특별한 사정의 존재 및 사회상당성은 개별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_16` / `Ⅱ.2`: “범인의 가족을 돕는 행위는 다른 특별한 사정이 없는 한 사회적 상당성이 있다.”

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

## 41. `art151_sec2_2.unknown_warrant_targets`

- proposition: 체포영장 발부 사실이 알려지지 않은 나머지 조직원들에 대해서는 형사사법작용 방해 위험이 초래되었다고 보기 어려워 범인도피죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 영장 발부 사실을 알지 못한 대상자에 관한 제한된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “체포영장 발부 사 실이 알려지지 않은 나머지 49명의 조직원에 대해서는 형사사법작용을 방해하 는 위험이 초래되었다고 보기 어려우므로 범인도피죄가 성립하지 않는다”

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

## 42. `art151_sec2_3.attempt_commencement`

- proposition: 범인을 은닉 또는 도피하게 하는 행위를 시작한 때에 범인도피죄의 실행의 착수가 인정되고, 준비행위를 시작한 것만으로는 실행의 착수가 인정되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실행행위의 시작과 준비행위를 구별하는 시간적 경계에 관한 카드다. 구체적 행위가 은닉 또는 도피 행위의 시작인지 여부는 사실관계 검토가 필요할 수 있다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.3_23` / `Ⅱ.3`: “범인을 은닉 또는 도피하게 하는 행위를 시작한 때에 본죄의 실행의 착수가 인 정된다. 범인을 은닉 또는 도피하게 하기 위한 준비행위를 시작한 것만으로는 본죄의 실행의 착수를 인정할 수 없다.”

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

## 43. `art151_sec2_3.completion_continuing_offense`

- proposition: 범인도피죄는 범인을 은닉 또는 도피하게 함으로써 기수에 이르고, 범인의 은닉 또는 도피 상태가 계속되는 동안 범죄행위도 계속되며 그 상태가 끝날 때 범죄행위가 종료된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 기수 시점과 계속 상태의 종료 시점을 구별하는 카드다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.3_23` / `Ⅱ.3`: “본죄는 범인을 은닉 또는 도피하게 함으로써 기 수에 이르지만 범인의 은닉 또는 도피 상태가 계속되는 동안에는 범죄행위도 계속 되고 범인의 은닉 또는 도피 상태가 끝날 때 비로소 범죄행위가 종료된다.”

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

## 44. `art151_sec2_3.no_attempt_punishment`

- proposition: 범인도피죄에는 미수범 처벌규정이 없으므로, 범인을 은닉하거나 도피하게 하는 행위가 기수에 이르기 전에 발각된 경우 처벌할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 기수 전 발각 상황에 대한 명시적 미수 처벌 배제 카드다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.3_23` / `Ⅱ.3`: “본죄의 경우 미수범에 관한 처벌규정이 없으므로, 범인을 은닉하거나 도피하 게 하는 행위가 기수에 이르기 전에 범행이 발각된 경우 처벌할 수 없다.”

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

## 45. `art151_sec2_3.preparation_remittance_holding`

- proposition: 외국으로 도피한 범인에게 송금해 달라는 부탁을 받고 자기앞수표를 가명으로 예금해 두었을 뿐 아직 송금하지 않은 사안은 범인도피의 예비에 불과하여 범인도피죄로 처벌할 수 없다고 한 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 대법원 판단이며, 원판결의 사건번호·사실관계·판단 범위를 사용자 제공 1차 판례 색인으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.3_23` / `Ⅱ.3`: “자기앞수표를 받아 이를 가명으로 예금하여 두었을 뿐 아직 범인에게 송금하지는 않은 사안에서 범인도피의 예비에 불과하여 범인 도피죄로 처벌할 수 없다고 판단하였다.”

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
