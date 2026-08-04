# 범인은닉·도피 RuleIR 카드 검수 2

- unit: `harboring_offender`
- articles: art151
- cards: 16–30 / 58
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art151_sec2_2.false_identification_no_evasion_intent`

- proposition: 참고인이 실제 범인을 정확히 모르는 상태에서 실제 범인이 아닐 수도 있는 사람을 범인으로 지목하는 허위진술을 하여 실제 범인이 쉽게 도피하는 결과가 발생해도, 적극적으로 실제 범인을 도피시켜 형사사법작용을 곤란하게 할 의사가 없으면 범인도피죄로 처벌할 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 실제 범인 도피 의사 부재에 관한 제한된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_22` / `Ⅱ.2`: “그것만으로는 그 참고인에게 적극적으로 실제의 범인을 도피시켜 국가의 형 사사법의 작용을 곤란하게 할 의사가 있었다고 볼 수 없어 그 참고인을 범인도 피죄로 처벌할 수는 없다”

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

## 17. `art151_sec2_2.false_statement_threshold`

- proposition: 참고인 또는 피의자가 수사기관에서 범인 또는 공범에 관하여 묵비하거나 허위진술하더라도, 적극적으로 수사기관을 기망하여 착오에 빠뜨림으로써 범인의 발견·체포를 곤란 또는 불가능하게 할 정도가 아니면 범인도피죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 참고인과 피의자에 공통되는 적극적 기망 및 발견·체포 곤란성 기준이다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_11` / `Ⅱ.2`: “참고인이 수사기관에서 범인에 관하여 조사를 받으면서 그가 알고 있는 사 실을 묵비하거나 허위로 진술하였다고 하더라도, 그것이 적극적으로 수사기관을 기만하여 착오에 빠지게 함으로써 범인의 발견 또는 체포를 곤란 내지 불가능 하게 할 정도의 것이 아니라면 범인도피죄를 구성하지 않는다.”
  - `comm_001692_제151조_Ⅱ.2_11` / `Ⅱ.2`: “그리고 이러한 법리를 피의자가 수사기관에서 공범에 관하여 묵비하거나 허위 로 진술한 경우에도 그대로 적용하고 있다.”

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

## 18. `art151_sec2_2.indirect_reassurance`

- proposition: 그 자체로 범인을 직접 도피시키는 목적이라고 보기 어려운 행위의 결과 간접적으로 범인이 안심하여 도피할 수 있게 된 경우는 범인도피죄의 도피행위에 포함되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 간접적 안심 효과와 직접 도피조력의 구별이 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “그 자체로는 도피시키는 것을 직접적인 목적으로 하였다고 보기 어려운 어떤 행위의 결과, 즉 간접적으로 범인이 안심 하고 도피할 수 있게 한 경우까지 포함되는 것은 아니다.”

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

## 19. `art151_sec2_2.intent_awareness_will`

- proposition: 범인은닉죄의 고의는 상대방이 벌금 이상의 형에 해당하는 죄를 저지른 사람이라는 점 및 그를 은닉·도피시켜 국가 형사사법작용을 곤란 또는 불가능하게 한다는 점에 대한 인식과 의사이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위자의 인식과 의사는 사실관계상 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_21` / `Ⅱ.2`: “게 하는 상대방이 벌금 이상의 형에 해당하는 죄를 저지른 사람이라는 점과 ⅱ) 그 사람을 은닉 또는 도피하게 하여 국가의 형사사법작용을 곤란 또는 불가능하 게 한다는 점에 대한 인식과 의사를 뜻한다.”

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

## 20. `art151_sec2_2.knowledge_of_crime`

- proposition: 범인이 실제로 저지른 죄에 대한 인식이 있으면 충분하고, 그 죄의 법정형이 벌금 이상이라는 점까지 알 필요는 없다는 통설 및 대법원 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 입장은 원문 판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_21` / `Ⅱ.2`: “‘벌금 이상의 형에 해당하는 자에 대한 인식은 실제로 벌금 이상의 형에 해당하는 범죄를 범한 자라는 것을 인식함으로써 충분하고 그 법정형이 벌금 이상이라는 것까지 알 필요는 없다.’고 판시하여 같은 입장이다.”

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

## 21. `art151_sec2_2.known_warrant_notification`

- proposition: 체포영장 발부자 명단을 전달받은 사람이 그 명단에 있는 특정 조직원들에게만 체포영장 발부 사실을 알린 경우, 그 사실을 통지받은 조직원들에 대해서는 범인도피죄 책임을 진다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 통지를 실제로 받은 특정 대상자에 한정된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “피 고인이 甲, ⼄, 丙, 丁을 위한 범인도피죄의 죄책을 부담”

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

## 22. `art151_sec2_2.lending_identification_documents`

- proposition: 지명수배 사실을 알면서 범인에게 자신의 운전면허증·신용카드를 빌려주고 자기 명의로 차량을 구입해 준 행위는 범인도피죄의 도피하게 하는 행위에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적 보고 판례의 제한된 사실관계에 관한 카드다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “피고인이 甲이 지명수배 중이라는 사실을 알고도 甲에게 자신의 운전면허증, 신용카드 등을 빌려주고 자신의 명의로 승용차를 구입하여 준 경우는 범인도피죄에서의 ‘도피하게 하는 행위’에 해당”

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

## 23. `art151_sec2_2.mistake_underlying_crime`

- proposition: 객체인 범인이 실제로 벌금 이상의 형에 해당하는 죄를 저질렀더라도 행위자가 벌금 미만의 형에 해당하는 다른 죄를 저질렀다고 인식한 경우에는 고의가 조각된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 기초 범죄에 관한 행위자 인식의 착오를 평가해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_22` / `Ⅱ.2`: “범인이 저지른 범죄 자체에 대하여 착오를 일으켜 실 제로는 범인이 벌금 이상의 형에 해당하는 죄를 저질렀음에도 불구하고 벌금 미만의 형에 해당하는 다른 죄를 저질렀다고 인식한 경우에는 본죄의 고의가 조각되어 처벌할 수 없다.”

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

## 24. `art151_sec2_2.no_indictment_conviction_required`

- proposition: 범인은닉죄의 객체인 죄를 저지른 사람에 해당하기 위하여 공소제기나 유죄판결의 선고·확정은 필요하지 않으며, 아직 수사가 개시되기 전이라도 진범이면 객체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공소제기나 유죄 확정의 불요를 명시한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_4` / `Ⅱ.2`: “‘죄를 저지른 사람’에 해당하기 위해서 반드시 공소가 제기되거나 유죄 판결 (4) 이 선고 또는 확정될 것이 요구되지는 않는다. 범죄혐의를 받아 수사를 받고 있 는 사람은 물론이고, 아직 수사가 개시되기 전이어도 진범인 이상 본죄의 객체 가 될 수 있다.”

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

## 25. `art151_sec2_2.nominee_business_owner`

- proposition: 게임장 등의 종업원이 실제 업주를 숨기고 대신 처벌받는 역할을 맡아 운영 경위·자금 출처·임대차계약 경위까지 적극적으로 허위진술하거나 허위자료를 제시하여 실제 업주 발견·체포를 곤란 또는 불가능하게 한 경우 범인도피죄를 구성할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 단순 명의 대여가 아닌 적극적 허위진술·자료 제시의 정도를 평가해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_15` / `Ⅱ.2`: “실제 업주라고 진술하는 것에서 나아가 게임장 등의 운영 경위, 자금 출처, 게임기 등의 구입 경위, 점포의 임대차계약 체결 경위 등에 관해서까지 적극적으로 허위로 진술하거나 허위 자료를 제시하여 그 결과 수사기관이 실제 업주를 발견 또는 체포 하는 것이 곤란 내지 불가능하게 될 정도에까지 이른 것으로 평가되는 경우 등에는 범인도피죄를 구성할 수 있다.”

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

## 26. `art151_sec2_2.nominee_lease_fugitive`

- proposition: 기소중지된 범인을 위해 다른 사람 명의로 오피스텔 임대차계약을 체결해 주어 수사기관의 탐문수사나 신고를 통한 범인 발견·체포를 곤란하게 한 행위는 범인을 도피하게 한 행위에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 명의 임대차가 탐문·신고에 의한 발견을 곤란하게 한 구체적 사안이다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_14` / `Ⅱ.2`: “피고인이 위 처를 내세워 그녀의 이름으로 대신 임대차계약을 체 결해 준 행위는 비록 임대차계약서가 공시되는 것은 아니라 하더라도 수사기관이 위 와 같은 탐문수사나 신고를 받아 범인을 발견하고 체포하는 것을 곤란하게 하여 범 인을 도피하게 한 행위에 해당한다고 보아야 할 것이다.”

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

## 27. `art151_sec2_2.nonappearance_discoverable_residence`

- proposition: 범인에게 수사기관 출석을 종용하지 않은 경우라도 범인이 주거지에 정상 거주하여 발견·체포가 가능했다면, 단순히 소환에 불응한 것만으로는 직접 범인을 도피시키거나 도피를 직접 용이하게 한 행위가 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 정상 주거 및 발견 가능성이 있는 구체적 사안에 한정한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_21` / `Ⅱ.2`: “甲 외 2인은 주거지에 정상적으로 거주하면서 단순히 소환에 응하지 않고 있었을 뿐이어서 수사기관으로서는 언제든지 이들에 대한 발견·체포가 가능하였다 할 것이므로, 피고인의 행위가 은닉행위에 비 견될 정도로 수사기관의 발견·체포를 곤란하게 하는 행위, 즉 직접 범인을 도피시키 거나 도피를 직접적으로 용이하게 한 행위에 해당한다고 볼 수 없다.”

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

## 28. `art151_sec2_2.nonprosecution_suspension_holding`

- proposition: 기소중지 불기소처분을 받은 사람의 부탁을 받고 그 사람의 거주 방을 피고인 처 명의로 임차해 준 사안에서, 그 행위가 수사기관의 발견·체포를 곤란하게 하여 범인을 도피하게 한 행위라고 보아 범인도피죄 성립을 인정한 대법원 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 객체성과 행위 요건을 원문으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_8` / `Ⅱ.2`: “피고 인의 행위는 수사기관이 탐문수사나 신고를 받아 범인을 발견하고 체포하게 하 는 것을 곤란하게 하여 범인을 도피하게 한 행위에 해당한다.’고 보아 범인도피 죄의 성립을 인정하였다.”

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

## 29. `art151_sec2_2.offender_participants_attempt`

- proposition: 죄를 저지른 사람에는 정범뿐 아니라 교사범·종범 및 공동정범·간접정범이 포함되고, 처벌규정이 있으며 법정형이 벌금 이상인 미수·예비·음모의 행위자도 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공범 및 처벌 가능한 미수·예비·음모의 포함 범위다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_3` / `Ⅱ.2`: “죄를 저지른 사람은 정범에 한정되지 않고, 교사범, 종 (1)(공동정범, 간접정범 포함) 범을 포함한다. 미수의 범행이나 예비·음모를 한 사람도 그 행위에 대한 처벌 규 정이 있고 법정형이 벌금 이상에 해당하면 본죄의 객체가 된다.”

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

## 30. `art151_sec2_2.offender_unlawful_culpable`

- proposition: 죄를 저지른 사람이란 구성요건에 해당하고 위법하며 유책한 행위를 한 사람을 말하므로, 위법성 또는 책임 조각사유가 있는 사람은 객체에서 제외된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위법성 또는 책임 조각이 있는 사람의 제외를 명시한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_3` / `Ⅱ.2`: “죄를 저지른 사람은 구성요건에 해당하고 위법, 유책한 행위를 한 사람을 말 (2) 한다. 따라서 구성요건에 해당하더라도 위법성 조각사유 또는 책임 조각사유가 있는 경우에는 제외된다.”

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
