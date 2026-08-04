# 위계공무집행방해 RuleIR 카드 검수 3

- unit: `deceptive_obstruction_of_official_duty`
- articles: art137
- cards: 31–45 / 50
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art137_sec4_3.attorney_visitation_nonlegal_purpose`

- proposition: 변호인 접견이 외관상 변호활동이나 실질적으로 다른 주된 목적을 위한 것으로서 접견교통권 행사의 한계를 일탈할 수 있더라도, 그것이 위계에 해당하거나 교도관의 구체적·현실적 직무집행을 방해했다고 보기 어려운 경우 위계에 의한 공무집행방해죄로 처벌할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 접견교통권의 한계 일탈과 위계성 및 구체적·현실적 직무집행 방해는 별도로 판단해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_19` / `Ⅳ.3`: “피고인이 접견 변호사들에게 지시한 접견이 변 호인에 의한 변호활동이라는 외관만을 갖추었을 뿐 실질적으로는 형사사건의 방어권 행사가 아닌 다른 주된 목적이나 의도를 위한 행위로서 접견교통권 행 사의 한계를 일탈한 경우에 해당할 수는 있겠지만, 그 행위가 위계에 해당한다 거나 그로 인하여 교도관의 구체적이고 현실적인 직무집행이 방해되었다고 보 기 어렵다고 판단하였다.”

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

## 32. `art137_sec4_3.attorney_visitation_smuggling`

- proposition: 변호사 접견의 신뢰와 구치소 감시 여건을 악용하여 수용자의 외부 통화 및 물품 수수를 은폐하고 적발을 회피한 경우, 교도관의 통상적 업무처리로 적발하기 어려운 위계를 사용하여 직무집행을 방해한 것으로 본 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 접견호실 통제업무의 구체성, 통상적 업무처리상 적발 곤란성 및 직무집행의 지장 또는 곤란을 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_20` / `Ⅳ.3`: “구체적·현실적으로 접견호실 통제업무를 담당하는 교도관들 에 대하여 그들의 통상적인 업무처리과정 하에서는 사실상 적발이 어려운 위계 를 사용하여 그 직무집행에 지장을 주거나 곤란하게 하는 행위임이 명백하다는 이유로, 본죄의 성립을 인정하였다.”

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

## 33. `art137_sec4_3.prison_monitoring_undetectable_deception`

- proposition: 구체적·현실적으로 감시·단속업무를 수행하는 교도관에 대하여, 충실한 직무수행에도 통상적 업무처리과정에서 적발하기 어려운 위계를 적극적으로 사용하여 업무집행을 못하게 한 경우 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적·현실적 담당 직무, 적극적 위계, 통상적 업무처리상 적발 곤란성 및 업무집행 불능의 관계를 사실관계별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_19` / `Ⅳ.3`: “구체적이고 현실적으로 감시·단속업무를 수행하는 교도관에 대하여 그가 충실히 직무를 수행한다고 하더라도 통상적인 업무처리과정하에서는 사실상 적발이 어려운 위계를 적극적으로 사용하여 그 업무집행을 하지 못 하게 하였다면 이에 대하여는 본죄가 성립한다고 보았다.”

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

## 34. `art137_sec4_3.prison_tobacco_concealed_body`

- proposition: 수용자가 항문에 담배를 숨겨 반입한 행위는 검신 담당 교도관의 감시·단속을 피한 금지규정 위반에 그치며, 교도관이 신체검사를 통한 단속 권한과 의무를 행사하지 않은 경우 그 행위가 감시·단속업무 방해의 원인이라고 보기 어려워 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 검신 권한·의무의 존재와 실제 행사의 부재가 원인관계 판단에 미치는 범위를 사례별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_18` / `Ⅳ.3`: “피고인이 자신의 신체의 은밀한 부위인 항문에 담배를 숨겨 반입한 행위가 비난받아 마땅한 것이기는 하나, 이는 검신 담당 교도관의 감시·단속을 피하여 금지규정에 위반하는 행위를 한 것에 불과하고, 검신 담당 교도관에게 위와 같 이 피고인의 신체를 검사하여 반입금지 물품을 단속하여야 할 권한과 의무가 주어져 있음에도 이를 행하지 아니한 이상, 피고인의 행위가 원인이 되어 교도 관의 감시·단속 업무가 방해되었다고 보기 어렵다고 판단하였다.”

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

## 35. `art137_sec4_3.prison_tobacco_concealed_book`

- proposition: 교도소 반입금지 담배를 두꺼운 책 표지 안쪽의 은닉공간에 숨겨 반입한 행위는 영치물 담당 공무원의 감시·단속을 피한 금지규정 위반에 그치며, 그 위계가 감시·단속업무 방해의 원인이라고 인정할 수 없어 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 영치물 담당 공무원에게 합리적 의심에 따른 검사 의무가 있었다는 사례 한정의 보고된 판단으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_17` / `Ⅳ.3`: “교도소 내 반입금지 물품인 담배를 이례적으로 두꺼운 표지를 가진 책의 표 지 안쪽을 칼로 도려내어 만든 공간에 은닉하여 영치하는 방법으로 교도소에 반입시킨 피고인의 행위는 그 책의 표지에 마약이나 담배 또는 칼날 등의 흉기 와 같이 교도소 반입금지 물품이 숨겨져 있을지도 모른다는 합리적인 의심을 가지고 검사에 임하여야 하는 영치물 담당 공무원의 감시·단속을 피하여 금지 규정에 위반하는 행위를 한 것에 불과하고, 그와 같은 위계가 원인이 되어 교도 관의 감시·단속업무가 방해되었다고 인정할 수 없으므로, 본죄가 성립하지 아니 한다고 판”
  - `comm_001692_제137조_Ⅳ.3_17` / `Ⅳ.3`: “단하였다.”

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

## 36. `art137_sec4_3.prohibited_act_evasion_monitoring`

- proposition: 금지규정 위반을 감시·단속할 권한과 의무가 있는 공무원의 감시·단속을 피하여 금지행위를 한 것만으로는, 별도의 벌칙 적용과 별개로 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 단순 금지규정 위반 회피와 통상적 업무처리로 적발하기 어려운 적극적 위계를 구별하여 적용할 필요가 있다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.3_17` / `Ⅳ.3`: “단순히 공무원의 감시나 단속을 피하여 금지규정에 위반하는 행위를 한 것에 불과하다면 그에 대하여 벌칙을 적용하는 것은 별론”
  - `comm_001692_제137조_Ⅳ.3_17` / `Ⅳ.3`: “으로 하더라도 그 행위가 본죄에 해당하는 것이라고는 할 수 없다.”

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

## 37. `art137_sec4_4.auction_price_disclosure`

- proposition: 경매 입찰가격 정보를 알아내어 더 높은 가격으로 입찰한 행위가 입찰의 공정만 해할 뿐 집행관의 구체적 직무집행을 저지하거나 현실적으로 곤란하게 하지 않은 경우에는 본죄에 해당하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 입찰 공정 침해와 구체적 직무집행 방해의 구별 범위를 원판례로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_23` / `Ⅳ.4`: “피고인들의 행위가 법원경매업무를 담당하는 집행관의 구체적인 직무집행을 저지하거나 현 실적으로 곤란하게 하는 데까지는 이르지 아니하고 입찰의 공정을 해하는 정도 에만 이르렀으므로, 이러한 행위는 형법 제315조의 경매·입찰방해죄에만 해당될 뿐 본죄에는 해당되지 아니한다고 판단하였다.”

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

## 38. `art137_sec4_4.evaluation_committee_list_disclosure`

- proposition: 입찰 제안공모 심사평가위원 명단을 외부인에게 알려준 것만으로는 조직위원회 공무원에게 오인·착각·부지를 일으키거나 그릇된 행위·처분을 하게 한 것으로 보기 어려워 위계에 해당하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 명단 제공 외의 추가 행위 여부와 공무원의 오인·착각·부지 여부를 구체적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_25` / `Ⅳ.4`: “피고인이 갑과 을에게 심사평가위원 명단”
  - `comm_001692_제137조_Ⅳ.4_25` / `Ⅳ.4`: “을 알려준 것만으로는 본죄의 위계에 해당한다고 할 수 없을 뿐만 아니라, 조직 위원회가 피고인의 위와 같은 행위에 따라 그릇된 행위나 처분을 하였다고 보 기 어렵다고 판단하였다.”

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

## 39. `art137_sec4_4.false_address_service`

- proposition: 민사소송에서 상대방 주소를 허위로 기재하여 재판관계서류가 송달되게 한 행위는 송달업무의 적정성을 침해하더라도 송달업무나 재판업무 자체를 방해한 것으로 보기 어렵다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 주소 기재 및 송달의 사실관계가 소개된 판례와 실질적으로 같은지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_23` / `Ⅳ.4`: “피고인이 소송 상대방의 주소를 허위”
  - `comm_001692_제137조_Ⅳ.4_23` / `Ⅳ.4`: “로 기재하여 그 주소로 재판 관계서류를 송달하게 한 행위는 송달업무의 적정 성을 침해하기는 하였지만 이로써 송달업무 또는 재판업무 그 자체를 방해하였 다고 볼 수 없다고 보았다.”

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

## 40. `art137_sec4_4.false_vehicle_theft_report`

- proposition: 존재하지 않는 차량도난을 허위 신고하여 불필요한 수사가 진행된 사정만으로는 경찰관에게 그릇된 행위나 처분을 하게 하였거나 구체적 공무집행을 저지 또는 현실적으로 곤란하게 한 것으로 보기 어렵다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 신고와 수사 진행의 구체적 내용이 소개된 판례의 한계를 넘는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_24` / `Ⅳ.4`: “피고인이 경찰공무원에게 있지도 아니한 차량도난 사실을 허위로 신고하여 불필요하게 수사를 진행하게 하였다는 점만으로는 경찰공무원의 적법한 수사직 무에 관하여 그릇된 행위나 처분을 하게 하였다거나 경찰공무원의 구체적인 공 무집행을 저지하거나 현실적으로 곤란하게 하는 데 이르렀다고 보기는 어렵다 고 판단하였다.”

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

## 41. `art137_sec4_4.invalid_notice_known_to_official`

- proposition: 입찰심사 업무를 방해할 가능성이 있는 통보서를 제출하더라도, 제출 전에 그 무효가 담당공무원에게 통보되어 오인·착각·부지 상태가 될 가능성이 전혀 없으면 본죄로 처벌할 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 담당공무원의 인식과 구체적 공무집행 방해 가능성은 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_23` / `Ⅳ.4`: “시 청 담당공무원으로서는 오인, 착각, 부지 상태가 될 가능성이 전혀 없었으므로, 이 사건 통보서를 제출하였다고 하더라도 시청의 구체적인 공무집행을 저지하 거나 현실적으로 곤란하게 하는 데까지 이른 적이 없다고 할 것이어서 본죄로 처벌할 수 없다고 판단하였다.”

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

## 42. `art137_sec4_4.invalid_oral_driving_test_rule`

- proposition: 상위법 위임범위를 벗어나 무효인 학력 제한 규정에 따라 초등학교 중퇴 이하라는 허위 인우보증서를 내고 구술시험에 응시한 사실만으로는 적법한 직무집행 방해가 아니.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 학력 제한 규정의 무효 및 적법한 직무집행 여부를 포함한 소개된 판례의 전제를 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_24` / `Ⅳ.4`: “피고인이 초등학교를 졸업하였음에도 초등학교 중 퇴 이하의 학력자라는 허위 내용의 인우보증서를 첨부하여 구술시험에 응시하였 다는 사실만으로는 적법한 직무집행을 방해하였다고 볼 수 없다고 판단하였다.”

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

## 43. `art137_sec4_4.procurement_evaluator_manipulation`

- proposition: 입찰 심사위원 선정과 작품 심사의 익명성을 조작하여 친분 있는 심사위원들이 특정 업체를 높은 점수로 평가하게 하고 그 업체가 사업자로 선정된 경우, 적정한 심사업무를 기대할 수 없게 할 정도로 담당공무원의 직무집행을 위계로 방해한 것으로 본 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 심사위원 선정 및 심사 익명성 조작의 구체적 정도가 적정한 심사업무를 기대할 수 없게 한 수준인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_27` / `Ⅳ.4`: “사업자 선 정을 담당하는 공무원으로 하여금 더 이상 사업자 선정에 대한 적정한 심사업 무를 기대할 수 없게 할 정도로 위계로써 담당공무원의 직무집행을 방해한 것 이라고 판단하였다.”

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

## 44. `art137_sec4_4.reported_holding_actual_obstruction`

- proposition: 위계로 상대방에게 오인·착각·부지를 일으키고 이를 이용하여 상대방이 그릇된 행위나 처분을 하며, 구체적 직무집행을 저지하거나 현실적으로 곤란하게 하여야 본죄가 성립한다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판시의 원문과 적용 범위를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_22` / `Ⅳ.4`: “상대방이 이에 따라 그릇된 행위나 처분을 하여야만 죄가 성립하고, 만약 그러한 행위가 구체적인 직무집행을 저지하거나 현실적으로 곤란하게 하 는 데까지는 이르지 아니한 경우에는 본죄로 처벌할 수 없다고 판시하였다.”

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

## 45. `art137_sec4_4.reported_holding_specific_duty_and_method`

- proposition: 본죄가 성립하려면 공무원의 구체적 직무집행을 현실적으로 방해하여야 하고, 그 직무집행 내용 및 현실적 방해방법을 심리하여 명시하여야 한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문 및 구체적 직무집행과 현실적 방해방법의 심리 요건을 확인해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.4_22` / `Ⅳ.4`: “본죄가 성립하려면 공무원의 구체적인 직무집행을 현실적으로 방해하여야 할 것이므로 당해 공무원의 구체적인 직무집행의 내용과 그에 대한 현실적인 방해방법 등에 관하여 심리하여 명시하여야 한다고 판시하기도 하였다.”

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
