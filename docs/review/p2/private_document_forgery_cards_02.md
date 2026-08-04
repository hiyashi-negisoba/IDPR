# 사문서등위조·변조 RuleIR 카드 검수 2

- unit: `private_document_forgery`
- articles: art231
- cards: 16–30 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art231_sec3_2.excess_of_delegated_authority`

- proposition: 타인 명의 문서 작성을 위임받았더라도 위임된 권한을 초월하여 내용을 기재함으로써 명의자의 의사에 반하는 사문서를 작성하면 작성권한을 일탈한 것으로 본죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 위임 범위, 기재 내용 및 명의자의 의사에 반하는지 여부를 개별적으로 평가한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_9` / `Ⅲ.2`: “타인으로부터 그 명의의 문서 작성을 위임받은 경우에도 위임된 권한을 초월하여 내용을 기재함으로써 명의자의 의사에 반하는 사문서를 작성 하는 것은 작성권한을 일탈한 것으로서 본죄에 해당한다.”

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

## 17. `art231_sec3_2.genuineness_misapprehension`

- proposition: 위조는 일반인에게 타인 명의의 진정한 문서라고 오신하게 할 정도이면 족하며, 그 정도는 문서의 형식·외관, 작성경위, 종류·내용 및 일반거래에서의 기능을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 진정한 문서라는 오신 가능성은 열거된 사정을 종합하는 평가 판단으로 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_7` / `Ⅲ.2`: “위조는 일반인에게 타인 명의의 진정한 문서 라는 것을 오신케 할 정도이면 그것으로 족하며 그 형식요건 등에 다소 불비한 점이 있더라도 위조죄가 성립한다.”
  - `comm_001692_제231조_Ⅲ.2_7` / `Ⅲ.2`: “일반인이 명의자의 진정한 사문서로 오신하 기에 충분한 정도인지 여부는 그 문서의 형식과 외관은 물론 그 문서의 작성경 위, 종류, 내용 및 일반거래에서 그 문서가 가지는 기능 등 여러 가지 사정을 종 합적으로 고려하여 판단한다.”

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

## 18. `art231_sec3_2.no_property_damage`

- proposition: 문서위조의 성립에 타인에 대한 재산상 손해 발생은 필요하지 않다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 재산상 손해의 발생은 문서위조 성립의 필수요건으로 추가하지 않는다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_8` / `Ⅲ.2`: “즉 위조가 성립하기 위해 타인에게 재산상의 손해가 발 생해야 하는 것은 아니다.”

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

## 19. `art231_sec3_2.presumed_consent`

- proposition: 행위 당시 현실적 승낙이 없더라도 모든 객관적 사정을 종합하여 명의자가 그 사실을 알았다면 당연히 승낙했을 것으로 추정되는 경우 사문서 위·변조죄는 성립하지 않지만, 단순한 기대나 예측만으로 승낙이 추정되는 것은 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 추정승낙은 행위 당시의 객관적 사정에 근거해야 하며, 작성자의 주관적 기대나 예측만으로는 인정하지 않는다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_9` / `Ⅲ.2`: “행위 당시 명의자의 현실적 승낙은 없었지만 행위 당시의 모든 객관적 사 정을 종합하여 명의자가 행위 당시 그 사실을 알았다면 당연히 승낙했을 것이 라고 추정되는 경우 역시 사문서의 위·변조죄가 성립하지 않는다.”
  - `comm_001692_제231조_Ⅲ.2_9` / `Ⅲ.2`: “의자의 명시적 승낙이나 동의가 없다는 것을 알고 있으면서도 명의자가 문서작 성 사실을 알았다면 승낙하였을 것이라고 기대하거나 예측한 것만으로는 그 승 낙이 추정된다고 단정할 수 없다.”

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

## 20. `art231_sec3_3.alias_name_addition_no_new_evidentiary_force`

- proposition: 일상거래상 통용된 이름으로 작성된 영수증에서 본명 일부를 덧붙인 행위가 영수증 내용에 영향을 미치지 않아 새로운 증명력을 작출하지 않은 경우 사문서변조죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 명칭 추가가 영수증 내용과 증명력에 미친 영향을 평가해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_14` / `Ⅲ.3`: “이는 위 영수증의 내용에 영향을 미쳤다고 보이지 않고, 따라서 새로운 증명력을 작출한 것이 아니므로 사문서변조죄를 구성하지 않는다.”

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

## 21. `art231_sec3_3.alteration_completion_new_evidentiary_force`

- proposition: 문서의 비본질적 부분을 불법으로 변개하여 일반인으로 하여금 이전과 다른 증명력이 있는 문서로 오신하게 할 상태에 도달하면 변조는 완성되어 기수가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인이 이전과 다른 증명력을 가진 문서로 오신할 상태에 도달했는지 평가해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “변조는 문서의 비본질적 부분을 불법으로 변개하여 일반인으로 하여금 이 (變改) 전과는 다른 증명력이 있는 문서로 오신케 할 상태에 도달한 때에 완성되어 기 수에 이른다.”

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

## 22. `art231_sec3_3.alteration_definition`

- proposition: 문서변조는 권한 없는 자가 이미 진정하게 성립한 타인 명의 문서의 내용에 동일성을 해하지 않는 정도의 변경을 가하고, 새로운 증명력을 작출하여 공공적 신용을 해할 위험성이 있을 때 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 변경의 동일성 훼손 여부, 새로운 증명력 및 공공적 신용 침해 위험은 개별 사실관계에 대한 평가를 요구한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_12` / `Ⅲ.3`: “문서의 변조는 권한 없는 자가 이미 진정하게 성립된 타인 명의의 문서내용에 그 동일성을 해하지 않는 정도의 변경을 가하는 것을 말하고, 새로운 증명력을 작출케 하여 공공적 신용을 해할 위험성이 있을 때 성립한다.”

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

## 23. `art231_sec3_3.alteration_method_deletion_addition`

- proposition: 행위자에게 불리한 기존 문자를 삭제하고 유리한 문자를 가필하거나 기입하는 행위도 변조 방법에 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 삭제 후 가필 또는 기입이라는 행위 유형을 변조 방법으로 분류한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “변조의 방법에는 행위자에게 불리한 기존의 문자를 삭제하고 유리한 문자를 가 필하거나 기입하는 행위도 포함된다.”

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

## 24. `art231_sec3_3.authorized_writer_alteration_no_offense`

- proposition: 부동산 처분권한을 위임받아 매매계약서 작성권한이 있는 사람이 매도인의 대리인 표시를 삽입한 경우, 명의인의 승낙이 없더라도 작성권한 있는 사람의 변경행위에 불과하여 사문서변조죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 처분권한 위임 및 매매계약서 작성권한의 존재를 확인해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_14` / `Ⅲ.3`: “이는 부동산의 처분권 한을 위임받아 매매계약서 작성 권한 있는 사람이 한 변경행위에 불과하고, 비 록 명의인의 승낙을 받지 않았더라도 사문서변조죄가 성립하는 것은 아니다.”

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

## 25. `art231_sec3_3.concealing_name_not_alteration`

- proposition: 재직증명서와 소득세원천징수확인서에서 법인명 부분을 흰색 수정테이프로 가린 행위만으로 일반인이 기존 문서와 다른 새 문서로 오신할 정도에 이르지 않은 경우 사문서변조죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 가림 행위가 일반인에게 기존 문서와 다른 새 문서라는 오신을 유발하는지 평가해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_14` / `Ⅲ.3`: “‘A’ 부분을 흰색 수정테이프로 가린 행위만으로는 객관적으로 보아 일반인으로 하여금 이를 기존 문서와 다른 새로운 문서로 오신하게 할 정도에 이르렀다고 보기 어려우므로 사문서변조죄가 성립하지 않는다.”

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

## 26. `art231_sec3_3.digital_file_image_not_document`

- proposition: 컴퓨터 모니터에 실행된 파일의 수정 이미지는 문서에 관한 죄에서 문서에 해당하지 않으며, 이를 변경하여 출력하여도 타인 명의 문서의 존재를 전제로 하는 사문서변조죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수정 대상이 전자파일 이미지인지 및 기존 타인 명의 문서의 존재 여부를 확인하고, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “컴퓨터 모니터에 실행된 경영정상화 이행 계획서 파일의 이 (수정) 미지는 형법상 문서에 관한 죄에서 문서에 해당하지 않고, 그러한 이미지를 변 경하여 출력하였더라도 타인 명의의 문서의 존재를 전제로 하는 사문서변조죄 가 성립하지 않는다.”

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

## 27. `art231_sec3_3.genuine_document_requirement`

- proposition: 사문서변조죄의 객체는 이미 진정하게 성립한 타인 명의 문서이므로, 그러한 문서가 존재하지 않으면 사문서변조죄는 성립할 수 없고, 미완성 서면에 가필하여 문서를 완성하는 행위는 변조가 아니라 위조이다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 변조의 객체가 이미 진정하게 성립한 타인 명의 문서인지 여부를 별도 요소로 확인한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_12` / `Ⅲ.3`: “변조의 객체는 이미 진정으로 성립된 타인 명의의 문서이다. 따라서 이미 진 정하게 성립된 타인 명의의 문서가 존재하지 않는다면 사문서변조죄가 성립할 수 없다. 또한 미완성의 서면에 가필하여 문서를 완성하는 것은 위조이지 변조 는 아니다.”

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

## 28. `art231_sec3_3.immaterial_character_change_exception`

- proposition: 문서 내용에 전혀 영향을 미치지 않을 정도로 문자만 변경한 경우에는 변조죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 문자 변경이 문서 내용에 영향을 미쳤는지 평가해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “그 내용에 전혀 영향을 미치지 않을 정도로 문자를 변경한 것에 불과한 때 에는 변조죄를 구성하지 않는다.”

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

## 29. `art231_sec3_3.multiple_nominees_contract_alteration`

- proposition: 2인 이상이 작성명의인인 문서에서는 각 명의자마다 하나의 문서가 성립하므로, 피고인이 명의자 중 한 사람이어도 다른 명의자와 합의 없이 행사할 목적으로 내용을 변경하면 사문서변조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 복수 명의자, 다른 명의자와의 합의 부재 및 행사할 목적을 확인해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “부동산 매매계약서와 같이 문서에 2인 이상의 작성명의인이 있는 때에는 각 나) 명의자마다 1개의 문서가 성립되고, 피고인이 명의자의 한사람이더라도 타 명의 자와 합의 없이 행사할 목적으로 문서의 내용을 변경하였을 때에는 사문서변조 죄가 성립한다.”

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

## 30. `art231_sec3_3.no_consent_despite_benefit`

- proposition: 명의인의 명시적·묵시적 승낙 없이 문서를 변조한 경우, 변조 문서가 명의인에게 유리하고 결과적으로 그 의사에 합치하더라도 사문서변조죄의 구성요건을 충족한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 명의인의 명시적 또는 묵시적 승낙 유무를 검토해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “명의인의 명시적·묵시적 승낙 없이 한 것이면 변조된 문서가 명의인에게 유리하여 결과적으로 그 의사에 합치하더라도 사문 서변조죄의 구성요건을 충족한다.”

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
