# 직무유기 RuleIR 카드 검수 1

- unit: `dereliction_of_duty`
- articles: art122
- cards: 1–15 / 49
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art122.disaster_review_omission`

- proposition: 사전재해영향성검토가 필요한 사업에서 담당자가 관련 검토 항목을 삭제하여 검토를 거치지 않게 한 행위는 정당한 사유 없는 의식적 직무 방임·포기로서 직무유기에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 검토 대상 사업 여부, 항목 삭제의 관여 및 정당한 사유를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “사전재해영향성 검토를 거치지 아니한 것은 피고인이 정당한 사유 없이 직무를 의식적으로 방”
  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “임 내지 포기하여 수행하지 아니한 경우에 해당한다.”

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

## 2. `art122.disciplinary_demand_objection`

- proposition: 교육기관 등의 장이 징계요구 직무이행명령에 대하여 이의소송을 제기한 경우, 징계사유가 객관적으로 명백한 특별한 사정이 없는 한 통보일부터 1개월 내 징계요구를 하지 않았다는 사정만으로 곧바로 직무유기에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이의소송의 제기, 징계사유의 객관적 명백성 및 특별한 사정의 유무를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_16` / `Ⅱ.4`: “특별한 사정이 없는 한 징계사유를 통보받은 날로부터 1개월 내에 징계요구”
  - `comm_001692_제122조_Ⅱ.4_16` / `Ⅱ.4`: “를 하지 않았다는 것만으로 곧바로 직무를 유기한 것에 해당한다고 볼 수는 없다.”

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

## 3. `art122.disciplinary_partial_measures`

- proposition: 지방자치단체장이 파업참가 공무원 일부에 대해서는 징계의결을 요구하고 나머지에 대해서는 훈계를 지시한 경우, 그 조치가 위법할 수 있어도 의식적 직무포기에 준하는 것으로 평가할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 징계 조치의 위법성과 직무의 의식적 포기 상당성을 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_16` / `Ⅱ.4`: “직장의 무단이탈이나 직무의 의식적인 포기에 준하는 것으로 평가할 수는 없을 뿐 아니라”

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

## 4. `art122.election_ballot_nonreport_noninvestigation`

- proposition: 경찰관이 투표용지 유출 사실을 상사에게 보고하지 않고 그 경위에 관한 수사에 착수하지 않으면 직무유기죄가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고 및 수사 착수 의무가 구체적으로 부과되었는지 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “경찰관이 투표용지의 유출사실에 대하여 상사에게 보고를 하지 않고 그 경”
  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “위에 대하여 수사에 착수하지 아니한 것은 직무유기죄가 된다.”

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

## 5. `art122.fugitive_assistance_nonreporting`

- proposition: 수배자 체포라는 구체적 임무를 받은 경찰관이 수배자를 돕고 관련 사실을 보고하지 않은 경우 직무유기죄 성립이 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수배자 체포의 구체적 임무 부여 및 지원·미보고 행위의 관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “B를 위하여 서류를 전달해 주는 한편 그의 예금통장까지 개설해 주고서도 그와 같은 사실을 보고”
  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “하지 아니한 경우 직무유기죄의 성립을 인정하였다.”

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

## 6. `art122.investigation_abandonment_release`

- proposition: 현행범인을 충분히 조사하지 않고 석방한 뒤 보고·기록작성·압수절차·추가조사 등을 하지 않은 수사경찰관의 행위가 정당한 사유 없는 수사업무의 의도적 방임 또는 포기로 평가되면 직무유기죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수사업무의 방임 또는 포기와 단순한 수사 부실의 구별이 필요하다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “이는 단순히 업무를 소홀히 수행한 것이 아니라 정당한 사유 없이 의도적으로 수사업무를 방임 내지 포기한 것이라고 봄이 상당하다는 이유로 직무유기죄의 성립을 인정하였다.”

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

## 7. `art122.lost_property_disposal`

- proposition: 경찰관이 습득물을 장기간 상회 운영자에게 보관하게 하고 반환 여부를 확인하지 않으며 처분대가를 받은 경우, 상회 운영자에게 임의처분을 용인하여 습득물 처리 직무를 의식적으로 방임·포기한 것으로 평가되면 직무유기죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 습득물 보관·확인·처분대가 수령의 결합 사실을 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “경찰관의 위와 같”
  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “은 행위는 상회 운영자에게 그 습득물에 대한 임의적 처분까지 용인한 것으로”
  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “서 습득물 처리지침에 따른 직무를 의식적으로 방임 내지 포기하고 정당한 사”
  - `comm_001692_제122조_Ⅱ.4_11` / `Ⅱ.4`: “유 없이 직무를 수행하지 아니한 경우에 해당한다.”

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

## 8. `art122.no_report_weekend`

- proposition: 공무원이 공금횡령 사실을 알고도 토요일 오후 상사 퇴청 후여서 선후책을 강구할 수 없는 상황에서 보고·처리하지 않은 것은 직무유기에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고·처리의 현실적 가능성과 당시 가능한 선후책을 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_15` / `Ⅱ.4`: “그에 대한 선후책을 강구할 수 없었던 이상 이를 처리하지 아니한 것이 직무유기에 해당한다 할 수 없다.”

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

## 9. `art122.officer_sleeping_ready_to_respond`

- proposition: 일직사관이 순찰·검사를 하지 않고 잠을 잤더라도 유사시에 즉시 깨어 직무수행에 임할 수 있는 상황이면 고의로 직무를 포기하거나 직장을 이탈한 것으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 유사시 즉시 직무수행이 가능한 상태였는지와 고의적 포기 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_15` / `Ⅱ.4`: “피고인이 고의로 일직 사관으로서의 직”
  - `comm_001692_제122조_Ⅱ.4_15` / `Ⅱ.4`: “무를 포기하거나 직장을 이탈한 것이라고는 볼 수 없다.”

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

## 10. `art122.permit_without_review`

- proposition: 허가 담당자가 신청 목적의 편법적 사용을 알면서도 허가요건을 자세히 검토하지 않고 허가한 경우, 의식적 직무 방임 또는 포기로서 직무유기죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 편법적 사용에 대한 인식, 검토의무 및 허가행위의 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “자신의 직무를 의식적으로 방임하거나 포기한 것으로”
  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “서 직무유기죄에 해당한다.”

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

## 11. `art122.plate_reissuance_duty`

- proposition: 자동차 사용정지 처분이 된 경우 특별한 사정이 없으면 번호판을 재교부해서는 안 되는 의무가 있는 담당직원이 이를 재교부하면 직무유기죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사용정지 처분, 담당자의 직무상 의무 및 특별한 사정의 존재를 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “분에 의하여 자동차의 사용이 정지된 경우에는 특별한 사정이 없는 한 그 번호”
  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “판을 재교부하여서는 안되는 직무상의 의무가 있음에도 번호판을 재교부한 경”
  - `comm_001692_제122조_Ⅱ.4_12` / `Ⅱ.4`: “우 직무유기죄를 구성한다.”

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

## 12. `art122.poor_performance_not_abandonment`

- proposition: 직무집행 의사로 직무집행행위를 하였으나 그 내용이 형식적·소홀하거나 부실한 경우, 그 부실만으로는 직무유기에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 실제 직무집행 의사와 행위가 있었는지, 단순 부실을 넘는 포기가 있었는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “직무집행의사로서의 직무집행행위를 한 점에는 변함이 없다고 할 것이고 그 내용이 부실하다 하여 직무유기에 해당”
  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “되지는 아니한다.”

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

## 13. `art122.prison_officer_tobacco`

- proposition: 교도관이 수용자의 금지물품 소지를 발견하고도 회수·보고 등 필요한 조치를 하지 않고 담배를 제공한 경우 직무유기 유죄가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 금지물품 인식, 회수·보고 등 구체적 조치의무 및 담배 제공 행위를 함께 검토해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “이를 회수하거나 지체없이 상관에게 보고하는 등 직무상 필요한 조치를 취하지 아니함으로써 직무를 유기하는 한편, A에게 3”
  - `comm_001692_제122조_Ⅱ.4_13` / `Ⅱ.4`: “회에 걸쳐 담배를 제공함으로써 정당한 이유 없이 교도관으로서의 직무수행을 거부하였다는 이 사건 범죄사실을 유죄로 인정한 원심의 조치는 정당하다.”

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

## 14. `art122.procedural_violation_only`

- proposition: 직무 수행에 필요한 법적 절차를 이행하지 않은 데 그치는 경우에는 직무유기죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 절차 위반만 있는 경우와 직무 자체의 의식적 방임·포기가 있는 경우를 구별해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “그 직무를 수행”
  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “함에 있어 필요로 하는 법적절차를 이행하지 아니함에 불과한 경우로서 직무유”
  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “기죄를 구성하지 아니한다.”

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

## 15. `art122.school_violence_response_insufficient`

- proposition: 중학교 담임교사가 학교폭력 대처를 소홀히 하였더라도 담당한 구체적 직무를 의식적으로 방임·포기하였다고 보기 어려우면 직무유기죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 학교폭력 대처의 부실과 구체적 직무의 의식적 방임·포기를 구별해야 한다.
- bounded sources:

  - `comm_001692_제122조_Ⅱ.4_14` / `Ⅱ.4`: “자신이 담당하는 구체적인 직무를 의식적으로 방임 내지 포기하였다고 보기 어려우므로 직무유기죄는 성립하지 아니한다.”

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
