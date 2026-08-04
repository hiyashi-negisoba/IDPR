# 위계공무집행방해 RuleIR 카드 검수 2

- unit: `deceptive_obstruction_of_official_duty`
- articles: art137
- cards: 16–30 / 50
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art137.provisional_order_no_concrete_obstruction_exception`

- proposition: 허위 매매계약서와 영수증을 첨부한 가처분신청으로 잘못된 가처분결정이 내려졌더라도, 법원의 구체적·현실적 직무집행 방해가 없다면 본죄는 바로 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 가처분절차에서의 구체적·현실적 직무집행 방해 여부를 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_11` / `Ⅳ.2`: “법원의 구체적이고 현실적인 어떤 직무집행이 방해되었다고 할 수는 없 으므로, 피고인들의 기만적인 행위로 인하여 잘못된 가처분결정이 내려졌다는 이유만으로 바로 본죄가 성립하지는 아니한다고 판단하였다.”

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

## 17. `art137.sec5.da.false_taxi_report_intent`

- proposition: 영업용택시를 운전하다가 사고를 내었다고 허위신고한 사실만으로는 공무원의 직무집행을 방해할 의사가 있었다고 단정하기 어려워 본죄가 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위신고 사실만으로 공무집행 방해 의사를 단정할 수 없다는 좁은 범위의 commentary-reported precedent이며, 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅴ.다_31` / `Ⅴ.다`: “영업 용택시를 운전하다가 사고를 내었다고 허위신고를 하였더라도, 이 사실만으로 공무원의 직무집행을 방해할 의사가 있었다고 단정하기 어려우므로 본죄가 성 립하지 아니한다고 보았다.”

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

## 18. `art137.urine_evidence_substitution`

- proposition: 타인의 소변을 자신의 소변처럼 제출하여 필로폰 음성반응이 나오게 한 행위는 수사기관 착오를 이용한 적극적 증거조작이므로 본죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소변 대체 제출이 단순 허위진술·증거은닉을 넘어 적극적 증거조작인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_13` / `Ⅳ.2`: “피고인이 타인의 소변을 마치 자신의 소변인 것처럼 건네주어 필로폰 음성반 응이 나오게 한 행위는, 단순히 피의자가 수사기관에 대하여 허위사실을 진술하 거나 자신에게 불리한 증거를 은닉하는 데 그친 것이 아니라 수사기관의 착오 를 이용하여 적극적으로 피의사실에 관한 증거를 조작한 것이므로 본죄가 성립 한다고 판단하였다.”

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

## 19. `art137_sec2.unrestricted_subject`

- proposition: 위계에 의한 공무집행방해죄의 주체에는 제한이 없고, 공무원도 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 본 카드의 범위는 본죄의 주체 제한 부존재와 공무원의 주체 가능성에 한정된다.
- bounded sources:

  - `comm_001692_제137조_Ⅱ_1` / `Ⅱ`: “본죄의 주체에는 제한이 없다. 공무원도 본죄의 주체가 될 수 있다.”

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

## 20. `art137_sec3.deception_causing_mistaken_official_act`

- proposition: 행위목적을 위해 상대방에게 오인·착각·부지를 일으켜 이를 이용함으로써 법령상 위임된 공무원의 적법한 직무에 관해 그릇된 행위 또는 처분을 하게 한 경우 본죄가 성립한다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 오인·착각·부지의 발생, 이용, 그리고 그릇된 행위 또는 처분의 관계는 사실관계에 대한 평가가 필요하다. 소개된 대법원 판시는 primary precedent index로 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅲ_2` / `Ⅲ`: “대법원은 위계에 의한 공무집행방해죄는 행위목적을 이루기 위하여 상대방에게 오인, 착각 또는 부지를 일으키게 하여 이를 이용함으로써 법령에 의하여 위임 된 공무원의 적법한 직무에 관하여 그릇된 행위나 처분을 하게 하는 경우에 성 립하고”

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

## 21. `art137_sec3.duty_includes_future_execution`

- proposition: 본죄의 직무집행은 현재의 직무집행뿐 아니라 장래의 직무집행도 포함한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현재 또는 장래의 직무집행인지 여부를 구별하는 범위 규칙으로 검토한다.
- bounded sources:

  - `comm_001692_제137조_Ⅲ_2` / `Ⅲ`: “본죄의 직무집행은 협의의 공무집행방해죄에서의 직무 집행과 달리 현재의 직무집행뿐만 아니라 장래의 직무집행을 포함하는 개념이다.”

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

## 22. `art137_sec3.non_authoritative_official_activity`

- proposition: 적법한 공무집행에는 공권력 행사를 내용으로 하는 권력적 작용뿐 아니라 사경제 주체로서의 활동 등 비권력적 작용도 포함된다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 문제된 활동이 공무원의 적법한 직무에 해당하는지는 활동의 성격과 법령상 위임을 검토해야 한다. 소개된 대법원 판시는 primary precedent index로 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅲ_2` / `Ⅲ`: “공권력의 행사를 내용으로 하는 권력적 작용뿐만 아니라 사경제 주체로서의 활동을 비롯한 비권력적 작용도 포함되는 것으로 보아야 한다고 판 시하였다.”

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

## 23. `art137_sec4_1.definition.deception_causing_mistake`

- proposition: 위계란 행위목적을 위해 상대방에게 오인·착각 또는 부지를 일으키고 이를 이용하는 것을 의미한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 오인·착각·부지의 발생 및 이용 여부는 구체적 사실관계에 대한 평가를 요한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_3` / `Ⅳ.1`: “‘위계’란 행위자가 어떠한 행위목적을 이루기 위하여 상대방에 대하여 오인이나 착각 또는 부지를 일으키게 하여 이를 이용하는 것을 의미한다.”

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

## 24. `art137_sec4_1.element.third_party_deception`

- proposition: 직무담당 공무원이 아닌 제3자를 기망하여 공무원의 직무집행을 방해하는 경우도 본죄를 구성한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 기망 상대방이 직무담당 공무원인지 제3자인지는 열거 가능한 관계로 기록한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_3` / `Ⅳ.1`: “직무를 담당하 는 공무원뿐만 아니라 제3자를 기망하여 공무원의 직무집행을 방해하는 것도 본죄를 구성한다.”

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

## 25. `art137_sec4_1.exception.false_literacy_guaranty`

- proposition: 초등학교 졸업자가 중퇴 이하 학력자라는 허위 인우보증서를 첨부하여 운전면허 구술시험에 응시한 사실만으로는 본죄가 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 예외적 판례 판단으로, 해당 허위 보증서가 시험감독 직무에 미친 법적 의미를 원판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_6` / `Ⅳ.1`: “피고인이 초등학교를 졸업하였음에도 초등학교 중퇴 이하 의 학력자라는 허위 내용의 인우보증서를 첨부하여 운전면허 구술시험에 응시 하였다는 사실만으로는 본죄가 성립하지 아니한다고 판단하였다.”

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

## 26. `art137_sec4_1.exception.rightful_possession_enforcement_resistance`

- proposition: 명도집행을 저지할 정당한 권능이 있는 점유자가 점유 증명을 위해 실효된 임대차계약서 사본을 제시하고 실효 사실을 알리지 않은 경우에도 위계에 해당하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 예외적 판례 판단으로, 명도집행 저지 권능 및 계약서 제시의 구체적 맥락을 원판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_6` / `Ⅳ.1`: “점유사실을 증명하기 위한 수단으로 이미 실효된 임대차계약서의 사본을 제시하면서 가사 그 실효 사실을 고지하지 아니하고 자신이 정당한 임차인인 것처럼 주장하였더라도 이를 위계에 해당한 다고는 볼 수 없다고 판단하였다.”

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

## 27. `art137_sec4_1.precedent.anonymous_ballot_marking`

- proposition: 지방의회 의장 선거 감표위원이 사전 날인을 기화로 투표자를 구별할 표시를 하고 그 용지로 투표가 이루어진 경우, 그 자체로 비밀선거에 의한 의장 선출 및 투표사무 감독 직무를 위계로 방해한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 개별 판례 판단이며, 사전 표시의 방식과 투표 실시 사실을 포함한 원판례 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_5` / `Ⅳ.1`: “그 후에 그 용지에 의하여 투표가 행하여졌다면 그 자체만으로 의 원들의 비밀선거에 의한 의장 선출 직무와 의장의 투표사무 감독 직무를 위계 로써 방해하는 행위에 해당한다고 판단하였다.”

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

## 28. `art137_sec4_1.precedent.exam_answer_note_delivery`

- proposition: 시험장 안에서 감독관 감시의 틈을 타 답안 해답 쪽지를 전달한 경우, 수험생의 행위 여하와 관계없이 시험감독 직무집행을 위계로 방해한 경우에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 개별 판례 판단이며, 원판례 확인 전까지는 공모 및 쪽지 전달의 사실관계에 한정한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_3` / `Ⅳ.1`: “피고인과 갑이 공모하여 피고인이 시험장소 내에서 시험감독관의 감시의 틈 을 타서 시험답안지의 해답이 적힌 쪽지를 갑에게 전달한 이상 갑의 행위 여하 에 불구하고 공무원의 시험감독에 관한 직무집행을 위계로서 방해한 경우에 해 당한다고 보았다.”

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

## 29. `art137_sec4_1.precedent.exam_question_prior_acquisition`

- proposition: 입학고사 담당공무원이 모르게 부정한 방법으로 시험문제를 사전 입수하여 내용을 알고 응시한 행위는 공무원의 부지를 이용한 위계에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 개별 판례 판단이며, 원판례 확인 전까지는 해당 사실관계에 한정한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_3` / `Ⅳ.1`: “입학고사 실시 직무를 담당하는 공무원이 모르게 시험문제를 부정한 방법으 로 사전에 입수하여 출제되는 시험문제의 내용을 미리 안 후 시험에 응시하는 행위는 공무원의 부지를 이용하는 행위로서 본죄의 위계에 해당한다고 보았다.”

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

## 30. `art137_sec4_1.precedent.false_certificate_exam_qualification`

- proposition: 허위 작성한 간호보조원 교육과정 수료증명서를 진정한 문서처럼 시험관리 당국에 제출하여 응시자격을 인정받아 응시한 경우, 시험관리 공무집행방해에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 개별 판례 판단이며, 허위 문서 제출과 응시자격 인정의 연결을 원판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.1_3` / `Ⅳ.1`: “간호보조원 교육과정 이수에 관한 사문서인 수료증명서를 허위 작성한 후 이 를 진정한 문서인 것처럼 시험관리 당국에 제출하여 응시자격을 인정받아 응시 하였다면 위계로써 시험관리에 관한 공무집행을 방해한 것이라고 보았다.”

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
