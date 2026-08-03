# 공무상비밀누설 RuleIR 카드 검수 1

- unit: `official_secret_disclosure`
- articles: art127
- cards: 1–15 / 27
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art127_sec2.subject.current_or_former_public_official`

- proposition: 공무상 비밀누설죄의 주체는 공무원 또는 공무원이었던 자이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체 범위만을 기재한 카드이며, 비밀의 범위 및 그 실질적 보호가치는 이 카드의 근거에 포함되지 않는다.
- bounded sources:

  - `comm_001692_제127조_Ⅱ_1` / `Ⅱ`: “공무원 또는 공무원이었던 자이다.”

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

## 2. `art127_sec3_1.confidentiality_requirements`

- proposition: 비밀이 되려면 일반적으로 비공지성과 보호필요성을 충족해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 비공지성과 보호필요성의 충족 여부는 개별 정보와 사안에 따라 검토한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “일반적으로 비밀이 되기 위해서는 비공지성과 보호필요성이라는 요건을 충족하”

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

## 3. `art127_sec3_1.illegally_obtained_job_secret`

- proposition: 공무원이 직무수행 중 불법적인 방식으로 지득한 비밀도 직무상 비밀에 해당한다는 하급심 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 하급심 판결의 원문과 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “공무원이 직무수행 중 불법적 인 방식을 사용하여 지득한 비밀도 직무상 비밀에 해당한다는 하급심 판결이 있다.”

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

## 4. `art127_sec3_1.job_related_secret_definition`

- proposition: 직무상 비밀은 공무원 또는 전직 공무원이 지위나 자격에 기초하여 직무집행 과정에서 알게 된, 직무와 관련된 비밀을 뜻한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 직무 관련성 및 직무집행 과정에서의 지득 여부는 개별 사실관계에 따라 확인한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “직무상의 비밀이란 직무와 관련하여 알게 된 비밀을 의미한다. 즉 공무원 또는 공무원이었던 자가 그 지위 내지 자격에 기초하여 직무집행 과정에서 알게 된 비밀을 말한다.”

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

## 5. `art127_sec3_1.non_job_related_private_secret_exception`

- proposition: 직무와 무관하게 알게 된 단순한 비밀 및 공무원이 직무를 취급하면서 지득한 사인의 비밀은 직무상 비밀에 포함되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 직무 관련성 및 사인의 비밀 해당 여부를 구체적 지득 경위와 정보 성격에 따라 검토한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “따라서 직무와 무관하게 알게 된 단순한 비밀은 여기에 포함되지 아니한다. 공무원이 직무를 취급하면서 지득하게 된 사인의 비밀은 직무상 비밀에 포함되지 않는다.”

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

## 6. `art127_sec3_1.political_interest_administrative_convenience_exception`

- proposition: 정부의 정치적 이익 또는 행정편의를 위한 사항은 비밀로 보호받을 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 정치적 이익 또는 행정편의를 위한 사항인지는 정보의 실질적 보호이익과 구별하여 검토한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “단순히 정부의 정치적 이”
  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “익 또는 행정편의를 위한 사항은 비밀로서 보호받을 수 없다.”

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

## 7. `art127_sec3_1.protection_need_state_function`

- proposition: 누설 시 국가안보에 실질적 위협이 발생하거나 공무의 민주적·능률적 운영 보장이 어려워질 위험이 있는 등 기능적으로 비밀로 할 필요성이 있는 사항은 보호필요성이 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 국가안보 위협, 공무 운영 보장 곤란 및 기능적 보호필요성은 사안별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.1_3` / `Ⅲ.1`: “설되는 경우 국가의 안보에 실질적 위협을 가져오거나 공무의 민주적, 눙률적 운영을 국민에게 보장할 수 없게 될 위험이 존재하게 되는 경우 등 기능적으로 보아 비밀로 할 필요성이 인정되는 사항이어야 한다.”

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

## 8. `art127_sec3_3.exam_questions`

- proposition: 학업성취도평가 시험위원들이 출제한 시험문제는 평가 목적 달성을 위해 평가대상자에게 비밀로 유지될 필요가 있어 직무상 비밀에 해당한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 원심 유지 사안의 시험 유형, 공개 시점 및 평가 목적과의 관계를 원판결로 확인해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.3_10` / `Ⅲ.3`: “시험위원들이 출제한 시험문제는 형법 제127조가 정하는 직무상의 비밀에 해당한다고 판단한 원심을 유지한 사안.”

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

## 9. `art127_sec3_3.fta_negotiation_strategy`

- proposition: 한미 자유무역협정 체결 협상의 전략과 분야별 쟁점 대응방향을 담은 문건 중 공개 시 상대방에게 협상상 우위를 주고 우리나라의 협상목표 달성을 어렵게 할 우려가 있는 부분은 실질적으로 보호할 가치가 있는 직무상 비밀에 해당한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 판시된 문건의 특정 기재 부분에 한정된 소개이므로 문서 제목이나 협상 문건이라는 성격만으로 일반화해서는 안 되며, 실질적 보호가치를 원판결로 확인해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.3_9` / `Ⅲ.3`: “적어도 이 사건 문건 중 그 판시와 같은 기재 부분은 정부나 공무소 또는 국민이 객관적, 일반적인 입장 에서 외부에 알려지지 않는 것에 상당한 이익이 있는 사항으로서, 실질적으로 비밀로서 보호할 가치가 있는 직무상 비밀에 해당한다.”

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

## 10. `art127_sec3_3.investigation_directive_pre_final_decision`

- proposition: 수사지휘서의 기재 내용과 관련 수사상황은 해당 사건의 종국적 결정 전까지 외부에 누설되어서는 안 되는 수사기관 내부 비밀에 해당한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대법원 판단이 commentary를 통해 소개된 자료이므로 원판결을 확인해야 하며, 종국적 결정 전이라는 시간적 범위와 해당 사건 관련성의 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.3_10` / `Ⅲ.3`: “그러므로 수사지휘서의 기재 내용과 이에 관계된 수사상황은 해당 사 건에 대한 종국적인 결정을 하기 전까지는 외부에 누설되어서는 안 될 수사기 관 내부의 비밀에 해당한다.”

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

## 11. `art127_sec3_3.preannouncement_admission_results`

- proposition: 대학 입시 합격자 선정 내용은 공식 발표 전에는 외부 비공개에 상당한 이익이 있는 사항으로서 공무상 비밀누설죄의 직무상 비밀에 해당한다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공식 발표 전이라는 한정과 외부 비공개에 상당한 이익의 존재를 개별 사안에서 평가해야 하며, 소개된 대법원 판결 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.3_10` / `Ⅲ.3`: “합격자 선정의 내용은 공식적인 발표 전에는 외부에 알려 지지 않는 것에 상당한 이익이 있는 사항이라고 할 것이고”

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

## 12. `art127_sec3_3.urban_planning_decision_before_publication`

- proposition: 도시계획시설결정은 법정 절차에 따른 공고·고시 등으로 공개되기 전에 특정인에게 누설하면 투기와 부당한 이익·피해를 초래할 우려가 있는 경우 실질적 비밀성이 인정된다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공개 전 상태, 특정인에 대한 사전 누설 및 투기·부당한 이익 또는 피해 우려를 사안별로 평가해야 하며, 소개된 판결의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.3_7` / `Ⅲ.3`: “도시계획시설결정은 그것이 법 소정의 절차를 거쳐 일반에게 공고 또는 고 시 등에 의하여 공개되기 전에 관계공무원이 이를 미리 특정인에게 누설하는 경우, 부동산투기를 조장하여 특정인에게 부당한 이익을 줄 염려가 있는 한편, 선량한 시민에게 부당한 피해를 주어”

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

## 13. `art127_sec3_4.internal_investigation_report_no_protectable_secret`

- proposition: 첩보 내용에 국가안전보장·질서유지·공공복리를 침해하는 요소가 없고 수사 목적이나 이해관계인의 기본권 침해 우려도 없는 경우, 내사결과보고서 내용은 비공지 사실이더라도 실질적으로 비밀로서 보호할 가치가 없다고 본 사안이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 비공지성은 보호가치와 구별되며, 국가안전보장·질서유지·공공복리, 수사목적 및 기본권 침해 관련 사정을 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_13` / `Ⅲ.4`: “내사결과보고서의 내용은 비공지의 사 실이기는 하나 실질적으로 비밀로서 보호할 가치가 있는 것이라고 인정할 수 없고”

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

## 14. `art127_sec3_4.internal_report_no_official_secret`

- proposition: 기업의 비업무용 부동산 보유실태 보고서는 공개가 국민 전체 이익에 이바지하고 국가기능을 위협한다고 볼 수 없는 경우 공무상 비밀에 해당하지 않으며, 행정기관 내부 처리과정의 중간문서라는 사정만으로 달리 볼 수 없다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고서의 내용, 공개 이익 및 국가기능 관련 위험을 사안별로 평가해야 하며, 중간문서성만으로 비밀성을 인정하지 않는다고 소개된 대법원 판단이다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_11` / `Ⅲ.4`: “보고서의 내용은 공 무상 비밀에 해당한다고 할 수 없으며, 행정기관 내부에서 처리과정 중에 있는 중간문서라는 사유만으로 그 내용이 당연히 공무상 비밀에 해당한다고 볼 수도 없다고 본 원심을 유지한 사안.”

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

## 15. `art127_sec3_4.nis_inspection_information_no_secret_value`

- proposition: 국가정보원 감찰조사 개시시점, 감찰대상자의 소속 및 인적 사항은 당시 정치상황, 여론, 감찰의 동기·목적·전파 상황 및 국가정보원의 직무 등을 종합할 때 비밀로서의 가치가 없다고 본 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 감찰정보의 비밀가치는 당시 정치상황, 여론, 감찰의 동기·목적·전파 상황 및 기관 직무를 종합하여 평가하는 것으로 소개되어 있다.
- bounded sources:

  - `comm_001692_제127조_Ⅲ.4_12` / `Ⅲ.4`: “시점, 감찰대상자의 소속 및 인적 사항은 비밀로서의 가치가 없다고 판단하였다.”

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
