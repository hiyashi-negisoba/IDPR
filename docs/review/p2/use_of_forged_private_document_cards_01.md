# 위조사문서등행사 RuleIR 카드 검수 1

- unit: `use_of_forged_private_document`
- articles: art234
- cards: 1–15 / 22
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art234.attempt_punishable`

- proposition: 위조사문서등의 행사죄의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 주석이 인용한 형법 제235조의 미수범 처벌 규정에 관한 카드이며, 원문 법조문 확인 전까지는 commentary 내 인용으로 취급한다.
- bounded sources:

  - `comm_001692_제234조_Ⅲ_4` / `Ⅲ`: “본죄의 미수범은 처벌한다. (형법 제235조)”

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

## 2. `art234.completion_by_placement_or_mail_delivery`

- proposition: 일반적으로 상대방이 열람할 수 있도록 비치하면 행사의 기수가 되고, 위조문서를 우송한 경우에는 상대방에게 도달한 때 기수가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 비치가 상대방의 열람 가능 상태에 이르렀는지 및 우송 문서가 상대방에게 도달했는지는 구체적 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅲ_4` / `Ⅲ`: “일반적으로 상대방이 열람할 수 있도록 비치해 두는 것에 의해 행사의 기수가 된다. 위조된 문서를 우송한 경우에는 그 문서가 상대방에게 도달한 때에 기수가 되고”

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

## 3. `art234.forged_license_possession_and_driving_not_utterance`

- proposition: 위조된 운전면허증을 소지하고 자동차를 운전한 것만으로는 행사가 있다고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 위조 운전면허증의 소지와 자동차 운전만으로는 행사로 평가되지 않는다는 제한된 부정 명제이다. 제시·교부 등 추가 행위의 효과는 이 출처만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제234조_Ⅲ_4` / `Ⅲ`: “그러나 위조된 운 전면허증을 소지하고 자동차를 운전한 것만으로는 행사가 있다고 할 수 없다.”

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

## 4. `art234.offense_character`

- proposition: 위조사문서등의 행사죄는 형법 제231조부터 제233조까지의 죄로 만들어진 문서·도화 또는 전자기록 등 특수매체기록을 행사함으로써 성립하는 범죄이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제231조부터 제233조까지의 죄로 만들어진 대상과 그 행사라는 구성 범위를 기술한다.
- bounded sources:

  - `comm_001692_제234조_Ⅰ_0` / `Ⅰ`: “본죄는 형법 제231조 내지 제233조의 죄에 의하여 만들어진 문서·도화 또는 전 자기록 등 특수매체기록 등을 행사함으로써 성립하는 범죄이다.”

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

## 5. `art234_sec2_1.copies_and_electronic_transmission`

- proposition: 위조문서를 기계적으로 복사한 복사본의 제시, 모사전송, 스캐너로 이미지화한 뒤 전송하여 컴퓨터 화면에서 보게 하는 방법도 행사에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 복사·전송 방식이 열거된 방식과 실질적으로 같은 제시인지 검토가 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “위조된 문서 그 자체를 직접 상대방에게 제시하거나 이를 기계적인 방법으로 복사하여 그 복사본을 제시하는 경우는 물 론, 위조된 문서를 모사전송의 방법으로 제시하거나 컴퓨터에 연결된 스캐너 로 읽어 들여 이미지화한 다음 이를 전송하여 컴퓨터 화면상에서 보게 (Scanner) 하는 경우도 행사가 된다.”

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

## 6. `art234_sec2_1.counterparty_interest_and_lack_of_knowledge`

- proposition: 행사의 상대방은 문서에 이해관계가 있어야 하며, 위조 등의 사실을 모르는 자여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상대방의 문서상 이해관계 및 위조 등 사실에 관한 인식 여부를 함께 확인한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “행사의 상대방은 그 문서에 대해서 이해관계가 있어야 한다.”
  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “다만 행사의 상대방은 위조 등의 사실을 모르는 자 일 것을 요한다.”

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

## 7. `art234_sec2_1.exercise_of_document`

- proposition: 문서의 행사는 위조·변조 또는 자격모용으로 작성된 사문서를 진정하게 작성된 진실한 내용의 문서인 것처럼 사용하는 것이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 개별 사용 행위가 진정한 문서인 것처럼 사용된 것인지는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “문서의 ‘행사’란 위조·변조 또는 자격모용에 의하여 작성된 사문서를 진정하게 작성된 진실한 내용의 문서인 것처럼 사용하는 것을 말한다.”

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

## 8. `art234_sec2_1.exercise_of_special_media_record`

- proposition: 특수매체기록의 행사는 위작·변작된 기록을 진정한 기록으로 정보처리할 수 있는 상태에 두는 것이며, 입력·출력·수정 가능한 상태에 두어도 행사가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 정보처리 가능한 상태인지의 적용에는 기술적·사실적 확인이 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “특수매체기록의 행 사는 위작·변작된 기록을 진정한 기록으로 정보처리 할 수 있는 상태에 두는 것 이며, 입력·출력·수정할 수 있는 상태에 두면 행사가 된다.”

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

## 9. `art234_sec2_1.indirect_perpetration_tool_holder`

- proposition: 간접정범을 통한 위조문서행사에서 도구로 이용된 자라도 문서가 위조된 사실을 모르는 자에게 행사하면 위조문서행사죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 간접정범 구조, 도구 이용 및 상대방의 위조 사실 불인식 여부를 검토한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “그러나 간접정범을 통한 위조문서행사범행에서 도구로 이용된 자라고 하더라고 문서가 위조된 것임을 알지 못하는 자에게 행사한 경우에는 위조문서행사죄가 성립한다.”

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

## 10. `art234_sec2_1.methods_of_exercise`

- proposition: 제시·교부·송부·비치·열람 등 상대방이 문서 내용의 인식이 가능한 상태에 두는 방법이면 행사 방법에 제한이 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방이 내용 인식이 가능한 상태였는지는 구체적 전달·접근 상황에 따라 평가한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “행사의 방법에는 제한이 없다. 제시·교부·송부·비치·열람 등 상대방이 그 내용 을 인식할 수 있는 상태에 두는 것이면 된다.”

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

## 11. `art234_sec2_1.no_actual_harm_required`

- proposition: 행사죄는 실제 손해나 손해 발생 우려, 현실적 법익침해 또는 법익침해 위험, 상대방의 재산상 손해를 요구하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실제 손해, 손해 우려, 법익침해·위험 및 상대방 재산상 손해를 별도 요건으로 요구하지 않는다는 제한이다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “행사의 결과 실제 손해가 발생함을 요하지 않고 또는 발생할 우려가 있음을 필 요로 하지 않는다. 즉 현실적인 법익 침해나 법익을 침해할 위험이 있음을 요하 지 않는다. 또한 위조문서 행사의 상대방에 대해 재산상 손해가 발생함을 요하 지도 않는다.”

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

## 12. `art234_sec2_1.no_actual_recognition_or_harm_risk_required`

- proposition: 상대방이 문서 내용을 실제로 알았거나 실해 발생 위험이 있을 필요는 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 실제 내용 인식 및 실해 발생 위험을 별도 요구요건으로 두지 않는다는 제한이다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “상대방이 문서의 내용을 인식할 수 있는 상태에 있으면 되고, 반드시 그 내용을 알았거나 실해가 발생할 위험 등은 필요하지 않다.”

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

## 13. `art234_sec2_1.object_covered_documents`

- proposition: 행사죄의 객체에는 위조·변조된 사문서·사도화, 자격모용으로 작성된 사문서·사도화, 의사 등이 작성한 허위 진단서 등 및 위작·변작된 전자기록 등 특수매체기록이 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 행사죄 객체의 범위를 그대로 반영한다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “본죄의 객체는 위조·변조된 사문서, 사도화 및 자격모용에 의하여 작성된 사문 서·사도화 그리고 의사 등이 작성한 허위진단서·허위검안서·생사에 관한 허위 증명서, 위작·변작된 전자기록 등 특수매체기록이다.”

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

## 14. `art234_sec2_1.possession_before_offer_not_exercise`

- proposition: 상대방에게 제공할 기회가 생기면 제공하기 위해 문서를 소지하거나 차량에 싣고 다니는 것, 또는 사자·사환에게 교부한 것만으로는 아직 행사에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 소지·운반·사자 또는 사환 교부가 실제 제공 단계에 이르렀는지는 사실관계 검토가 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_1` / `Ⅱ.1`: “상대방에게 기 회가 되면 제공하기 위해 자신이 문서를 소지하거나 승용차에 싣고 다닌 경우 또는 사자·사환에게 교부한 것만으로는 아직 행사라고 할 수 없으나”

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

## 15. `art234_sec2_1.presentation_to_knowing_accomplice`

- proposition: 문서가 위조·변조·허위작성되었음을 아는 공범자 등에게 문서를 제시하거나 교부하는 경우에는 행사죄가 성립할 여지가 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상대방의 공범성 및 위조·변조·허위작성 사실에 대한 인식은 사실관계 검토가 필요하다.
- bounded sources:

  - `comm_001692_제234조_Ⅱ.1_2` / `Ⅱ.1`: “그 문서가 위조, 변조, 허위작 성되었다는 정을 아는 공범자 등에게 제시, 교부하는 경우에는 본죄가 성립할 여지가 없다.”

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
