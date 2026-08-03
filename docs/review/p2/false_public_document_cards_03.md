# 허위공문서작성 RuleIR 카드 검수 3

- unit: `false_public_document`
- articles: art227
- cards: 31–44 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #6 `art227_sec3_2.assistant_indirect_perpetration`: `art227_sec3_2.assistant_indirect_perpetration_affirmative` (status=`valid`)

## 31. `art227_sec4_2.inadequate_completion_inspection_report`

- proposition: 담당공무원이 설계도면대로 시공되지 않은 연립주택에 관하여 세밀한 조사 없이 적합 여부를 알지 못하면서 준공검사보고서에 ‘적합’이라고 기재하고 서명날인한 경우, 그 보고서는 허위공문서작성죄의 객체가 되는 문서에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 불충분한 조사 아래 적합 기재가 이루어진 준공검사보고서에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “연립주택이 당초의 설계 도면대로 공사되지 않은 것을 담당공무원이 세밀하게 조사하지 않아 적합여부 를 제대로 알지 못하면서도 준공검사보고서 용지에 함부로 ‘적합’이라고 기재하 고 서명날인하여 허위의 내용을 기재한 경우 이러한 준공검사보고서는 허위공 문서작성죄의 객체가 되는 문서에 해당한다.”

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

## 32. `art227_sec4_2.known_unfinished_buried_parts`

- proposition: 매몰된 부분의 공사가 완성되지 않았음을 알면서 준공검사조서를 작성한 경우 허위공문서작성죄의 책임을 면하지 못한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 매몰 부분 미완성을 인식한 상태에서의 준공검사조서 작성에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “매몰된 부분의 공 사가 완성되지 않았다는 것을 알면서도 준공검사조서를 작성한 경우에는 허위 공문서작성죄의 죄책을 면하지 못한다.”

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

## 33. `art227_sec4_2.omitted_mortgage_registry_copy`

- proposition: 등기부등본 교부신청이 있었는데도 고의로 근저당권설정등기를 누락하고 소유권이전등기만 기입하여 발급한 경우 본죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 등기부등본 발급 시 근저당권설정등기를 고의로 누락한 경우에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “등본의 교부신청이 있었음에도 고의로 일부를 누락하여 소유권이전등기만 기입 하고 근저당권설정등기는 기입하지 않은 채 등기부등본을 발급한 경우 본죄가 성립한다.”

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

## 34. `art227_sec4_2.original_copy_certification`

- proposition: 직무상 사문서 사본에 원본대조필이라고 기재·날인한 경우 실제 원본과 대조하지 않았다면, 전화 확인이나 사본과 원본의 객관적 일치 여부와 무관하게 본죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 원본 대조라는 직무상 확인행위의 실제 이행 여부와 허위 기재의 관계에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_12` / `Ⅳ.2`: “피고인이 실제로 원 본과 대조함이 없이 “원본 대조필”이라고 기재한 이상 그것만으로 곧 허위공문 서작성죄가 성립하고, 피고인이 위 문서작성자에게 전화로 원본과 다르지 않다 는 사실을 확인하였다거나 객관적으로 사본이 원본과 다르지 않더라도 허위공 문서작성죄의 성립에는 지장이 없다.”

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

## 35. `art227_sec4_2.proxy_application_indication`

- proposition: 인감증명서에 대리인 신청을 본인이 직접 출두하여 신청한 것으로 기재하면, 인적사항·인감·용도가 일치하더라도 그 사항에 관하여 허위 기재가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인감증명서 신청 주체에 관한 기재가 허위인지에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_12` / `Ⅳ.2`: “인감증명서를 발행하는데 인감증명서의 인적사항과 인감 및 그 용도를 일치하게 기재하였어도 대리인에 의한 것을 본인이 직접 출두하여 신청 한 것으로 기재하였다면 그 사항에 관하여는 허위 기재하였다고 보아야 한다.”

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

## 36. `art227_sec4_2.superior_acquiescence_intent`

- proposition: 유용 예산 지출 내역에 관한 허위 증빙서류 작성에서 부득이한 사정으로 상사나 군수의 양해가 있었더라도, 허위공문서작성 및 그 행사에 관한 범의가 부정되지는 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 상사 또는 군수의 양해가 허위공문서작성 및 행사 범의를 부정하지 않는다는 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “부득이한 사정으로 상사인 건설과장이나 군수의 양해가 있었더라도 허위공문서 작성과 그 행사에 관한 범의를 부정할 사유는 될 수 없다.”

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

## 37. `art227_sec4_2.uninspected_buried_parts`

- proposition: 시공 후 매몰된 부분을 공사감독관의 감독조서에 근거하여 검사할 수 있는 경우, 실제 검사 없이 준공조서를 작성하였더라도 허위 준공검사조서 작성이라고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 매몰 부분에 관한 감독조서 근거 검사라는 제한된 사정에서의 예외적 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “수중, 지하 또는 구조물의 내부 등 시공 후 매몰된 부분은 공사감독관의 감독조서를 근거로 검사하면 되고, 실제로 검사하지 않은 채 준공조서를 작성하 였더라도 허위로 준공검사조서를 작성하였다고 할 수 없으나”

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

## 38. `art227_sec4_2.unverified_completion_inspection`

- proposition: 정산설계서 확인 및 준공검사를 하지 않았음에도 하였다고 준공검사용지에 기재한 경우, 조서 내용이 객관적 설계서나 공사현장 상태와 일치하더라도 본죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 실제 확인·검사 없이 이를 하였다고 기재한 준공검사용지 작성에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_12` / `Ⅳ.2`: “정산설계서를 확인하고 준공검사를 한 것이 아님에도 마치 확인한 것처럼 준공검사용지에 “정산설계서에 의하여 준공검사를 하였다”는 내용을 기 입하였다면 허위공문서작성의 범의가 있었음이 명백하여 그것만으로 곧 허위공”
  - `comm_001692_제227조_Ⅳ.2_12` / `Ⅳ.2`: “문서작성죄가 성립하고”

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

## 39. `art227_sec4_3.building_permit_expression_no_falsehood`

- proposition: 건축법상 요건을 갖추지 못한 설계 사실을 알면서 건축허가서를 작성하였더라도, 허가서에 표현된 허가 의사표시 내용 자체에 허위가 없으면 허위공문서작성죄로 처벌할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허가서가 어떠한 사항을 확인·증명하는지와 허가 의사표시 자체의 허위 여부에 대한 평가가 필요하다. 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.3_15` / `Ⅳ.3`: “허가서에 표현된 허가의 의사표시 내용 자체에 어떠한 허위가 있다고 볼 수는 없 으므로, 위 건축허가서를 작성한 행위를 허위공문서작성죄로 처벌할 수는 없다.”

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

## 40. `art227_sec4_3.legal_misapplication_true_facts`

- proposition: 고의로 법령을 잘못 적용하여 공문서를 작성하였더라도 법령 적용의 전제가 된 사실관계 내용에 거짓이 없으면 허위공문서작성죄는 성립할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 법령 적용의 오류와 그 전제가 된 사실관계의 허위를 구별하는 예외 카드다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.3_15` / `Ⅳ.3`: “고의로 법령을 잘 못 적용하여 공문서를 작성하였더라도 그 법령적용의 전제가 된 사실관계에 대 한 내용에 거짓이 없다면 허위공문서작성죄가 성립될 수 없다.”

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

## 41. `art227_sec6.completion`

- proposition: 작성권한자가 허위 내용을 기재하거나 기존 진정 공문서의 내용을 허위로 변경한 때 기수가 되며, 문서 자체로 작성자를 추지할 수 있으면 명의인의 날인 없이도 기수이고 실해 발생은 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 허위 기재·변경, 작성자 추지 가능성, 명의인 날인 불요 및 실해 불요라는 기수 판단 범위를 해당 인용문에 한정해 정리했다.
- bounded sources:

  - `comm_001692_제227조_Ⅵ_19` / `Ⅵ`: “작성권한 있는 자가 허위내용을 기재한 때, 기존의 진정한 공문서 내용을 허위 로 변경한 때에 기수가 된다. 문서의 형식, 내용 등 그 문서자체에 의하여 누가 작성하였는가를 추지할 수 있을 정도라면 명의인의 날인이 없더라도 기수이 고, 이로 인한 실해의 발생 유무도 묻지 않는다.”

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

## 42. `art227_sec7_1.no_direct_concealment_job_abandonment_concurrence`

- proposition: 농지일시전용허가를 해주기 위하여 복명서 및 심사의견서를 허위 작성한 것이 직접적으로 농지불법전용사실을 은폐하기 위한 것이 아니라면, 허위공문서작성·행사죄와 직무유기죄는 실체적 경합범 관계이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 농지일시전용허가를 위한 복명서 및 심사의견서 허위작성이라는 보고된 사실관계에 한정된 판단으로 보존하며, reported holding은 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제227조_Ⅶ.1_22` / `Ⅶ.1`: “위 복명서 및 심사의견서를 허 위 작성한 것이 농지일시전용허가를 신청하자 이를 허가하여 주기 위하여 한 것이라면 직접적으로 농지불법전용사실을 은폐하기 위하여 한 것은 아니므로 위 허위공문서작성, 동행사죄와 직무유기죄는 실체적 경합범의 관계에 있다.”

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

## 43. `art227_sec7_3.bribery_false_official_document_concurrence`

- proposition: 예비군 중대장이 금원을 받고 훈련 불참자를 참석한 것처럼 허위 중대학급편성명부를 작성·행사한 경우, 수뢰후부정처사죄 외에 허위공문서작성 및 동행사죄가 별도로 성립하고, 각 죄는 수뢰후부정처사죄와 각각 상상적 경합관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 개별 사실관계의 경합 판단이다. 공무원인 의사의 허위진단서 작성이나 직무유기와의 관계로 확장하지 않으며, 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅶ.3_24` / `Ⅶ.3`: “수뢰후부정처사죄 외에 별도로 허위공문서작성 및 동행사죄가 성립하고, 이들 죄와 수뢰후부정처사죄는 각각 상상적 경합관계에 있다.”

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

## 44. `art227_sec3_2.assistant_indirect_perpetration_affirmative`

- proposition: 작성권한 있는 공무원을 보좌하여 공문서 기안을 담당하는 공무원이 직위를 이용하여 행사할 목적으로 허위 공문서를 완성한 경우, 보조공무원에게 허위공문서작성죄의 간접정범을 인정하는 긍정설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 보조공무원이 작성권한자를 이용한 경우의 간접정범을 긍정하는 학설이다. 부정설과의 선택은 법률검토가 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.2_6` / `Ⅲ.2`: “긍정설은, 공문서의 작성권한 있는 공무원을 보좌하여 공문서 기안을 담당하 는 공무원이 그 직위를 이용하여 행사할 목적으로 허위 공문서를 완성하는 경 우에 보조공무원에 대하여 허위공문서작성죄의 간접정범을 인정한다.”

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
