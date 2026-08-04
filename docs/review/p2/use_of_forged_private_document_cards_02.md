# 위조사문서등행사 RuleIR 카드 검수 2

- unit: `use_of_forged_private_document`
- articles: art234
- cards: 16–22 / 22
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art234_sec2_1.transcript_not_exercise`

- proposition: 위조·변조·허위작성된 문서 자체인 원본을 직접 사용해야 하므로, 필사본 사용은 행사가 아니다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 필사본 사용을 행사에서 제외하는 원본 직접 사용 요건이다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “행사는 위조·변조·허위작성된 문서 자체, 즉 원본을 직접 사용할 것을 요한다. 따라서 필사본의 사용은 행사가 아니다.”

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

## 17. `art234_sec2_1.unrestricted_principal`

- proposition: 위조 등 사문서행사죄의 주체에는 제한이 없고, 위조·변조한 자가 스스로 행사할 필요는 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행사 주체의 제한 및 위조·변조자 본인의 행사 필요 여부에 관한 서술이다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “위조 등 사문서행사죄의 주체는 제한이 없다. 반드시 위조·변조한 자가 스스로 행사함을 요하지 않는다.”

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

## 18. `art234_sec2_1.use_as_forgery_not_exercise`

- proposition: 위조문서를 위조문서로 또는 허위문서를 허위문서로 사용하는 행위는 행사에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위조 또는 허위임을 전제로 사용하는 경우를 행사 개념에서 제외한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “따라서 위조문서를 위조문서로, 허위문서를 허위문서로 사용하는 행위는 행사라 할 수 없다.”

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

## 19. `art234_sec2_2.intent_no_purpose`

- proposition: 위조·변조·위작·변작·작성된 문서 또는 허위작성된 진단서 등에 대한 인식과 이를 행사한다는 고의가 필요하며, 행사할 목적은 구성요건상 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행사 대상 문서 등에 대한 인식 및 행사 고의의 필요성과 행사 목적 불요를 함께 기술한 단일 후보를 그대로 반영한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.2_3` / `Ⅱ.2`: “위조·변조·위작·변작·작성된 문서 또는 허위작성된 진단서 등에 대한 인식과 이를 행사한다는 점에 대한 고의가 있어야 한다. 본죄는 구성요건으로 행사할 목적을 요하지 않는다.”

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

## 20. `art234_sec4.company_agreement_breach_ideal_concurrence`

- proposition: 회사 명의 합의서를 임의로 작성·교부한 행위로 인한 사문서위조 및 위조사문서행사죄와, 그로 인한 회사 재산상 손해의 업무상배임죄는 하나의 행위로서 상상적 경합관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 회사 명의 합의서의 임의 작성·교부 및 회사 재산상 손해라는 보고된 사실관계에 한정된 상상적 경합 입장이다.
- bounded sources:

  - `comm_001692_제234조_Ⅳ_5` / `Ⅳ`: “회사 명의의 합의서를 임의로 작성·교부한 행위로 인한 사문서위조 및 위조사 문서행사죄와 그로 인하여 회사에 재산상 손해를 가하였다는 업무상 배임죄는 그 객관적 사실관계가 하나의 행위라 할 것이어서 형법 제40조에 정한 상상적 경합관계에 있다”

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

## 21. `art234_sec4.forger_and_exercise_real_concurrence`

- proposition: 위조·변조한 사문서를 행사한 경우 다수설과 판례는 사문서위조·변조죄와 행사죄가 실체적 경합관계라고 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 판례가 보고된 실체적 경합 입장으로, 원전 판례 확인 전에는 commentary-reported precedent로 유지한다.
- bounded sources:

  - `comm_001692_제234조_Ⅳ_5` / `Ⅳ`: “위조·변조한 사문서를 행사한 경우 다수설과 판 례는 사문서위조·변조죄와 행사죄는 실체적 경합관계에 있다고 본다.”

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

## 22. `art234_sec4.multiple_documents_ideal_concurrence`

- proposition: 수개의 문서를 한꺼번에 행사한 경우 문서 명의인이 서로 달라도 각 행사죄는 상상적 경합관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 수개의 문서 행사와 각 행사죄의 상상적 경합 관계에 관한 서술이다.
- bounded sources:

  - `comm_001692_제234조_Ⅳ_5` / `Ⅳ`: “수개의 문서를 한꺼번에 행사한 경우 그 문서 명의인이 다르더라도 각 행사죄 는 상상적 경합관계에 있다.”

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
