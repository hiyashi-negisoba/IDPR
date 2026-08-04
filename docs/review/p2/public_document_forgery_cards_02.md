# 공문서등위조·변조 RuleIR 카드 검수 2

- unit: `public_document_forgery`
- articles: art225
- cards: 16–30 / 43
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art225_sec3_1.assistant_completion_without_approval`

- proposition: 보조공무원이 결재 없이 임의로 허위내용의 공문서를 완성하면 공문서위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 보조공무원의 결재 절차 및 임의 완성 여부를 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_9` / `Ⅲ.1`: “이러한 결재를 거치지 않고 임의로 허위내용의 공문서를 완성한 때에”
  - `comm_001692_제225조_Ⅲ.1_9` / `Ⅲ.1`: “는 공문서위조죄가 성립한다.”

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

## 17. `art225_sec3_1.author_instruction_or_consent`

- proposition: 공문서 작성권자가 직접 서명하지 않고 타인에게 자신의 서명을 대신 하도록 지시하거나 승낙한 경우, 그 타인의 기안문서 작성행위는 공문서위조죄 구성요건 해당성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 작성권자의 지시 또는 승낙이 있었는지와 그 범위를 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_9` / `Ⅲ.1`: “한 피고인의 기안문서 작성행위는 작성권자의 지시 또는 승낙에 의한 것으로서 공문서위조죄의 구성요건 해당성이 조각된다.”

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

## 18. `art225_sec3_1.deceived_official_genuine_document`

- proposition: 작성권한 있는 공무원이 문서 기재사항을 인식하고 작성 의사로 서명날인했다면, 타인의 기망으로 허위임을 알지 못했더라도 문서는 진정 성립하며 명의모용이 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공무원의 기재사항 인식 및 작성 의사의 존재를 별도로 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_8` / `Ⅲ.1`: “어느 문서의 작”
  - `comm_001692_제225조_Ⅲ.1_8` / `Ⅲ.1`: “성권한을 갖는 공무원이 그 문서의 기재사항을 인식하고 그 문서를 작성할 의”
  - `comm_001692_제225조_Ⅲ.1_8` / `Ⅲ.1`: “사로 이에 서명날인하였다면, 설령 그 서명날인이 타인의 기망으로 착오에 빠진 결과 그 문서의 기재사항이 진실에 반함을 알지 못한 데 기인한다고 하여도, 그 문서의 성립은 진정하며 여기에 하등 작성명의를 모용한 사실이 있다고 할 수 없다.”

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

## 19. `art225_sec3_1.deceived_official_no_indirect_perpetration`

- proposition: 공무원이 아닌 자가 허위 증명원을 제출하여 허위임을 모르는 담당공무원으로부터 같은 내용의 증명서를 발급받은 경우 공문서위조죄의 간접정범으로 처벌할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 증명원 제출, 담당공무원의 불인지, 동일 내용 증명서 발급 여부를 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_8` / `Ⅲ.1`: “공무원 아닌 자가 관공서에 허위 내용의 증명원을 제출하여 그 내”
  - `comm_001692_제225조_Ⅲ.1_8` / `Ⅲ.1`: “용이 허위인 정을 모르는 담당공무원으로부터 그 증명원 내용과 같은 증명서를 발급받은 경우 공문서위조죄의 간접정범으로 의율할 수는 없다.”

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

## 20. `art225_sec3_1.forgery_apparent_authority`

- proposition: 위조문서가 일반인에게 공무소 또는 공무원의 직무권한 내 작성 문서로 믿게 할 형식·외관을 갖추면, 명의인에게 실제 권한이 없어도 공문서위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인을 기준으로 한 형식·외관의 충족 여부는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “위조문서가 일반인에게 공무소 또는 공무원의 직무권한 내에서 작성된 것으로 믿게 할 만한 형식이나 외관을 구비하고 있는 한 그 문서 작성명의인인 공무소”
  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “나 공무원에게 그러한 권한이 없는 경우에도 공문서위조죄는 성립한다.”

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

## 21. `art225_sec3_1.forgery_definition`

- proposition: 공문서 위조는 작성권한 없는 사람이 공무소 또는 공무원의 명의를 이용하여 문서를 작성하는 것이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 작성권한 및 명의 이용의 관계를 검토 가능한 정의 카드로 유지한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “공문서의 위조라 함은 작성권한 없는 사람이 공무소, 공무원의 명의를 이용하여 문서를 작성하는 것을 말한다.”

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

## 22. `art225_sec3_1.new_content_is_forgery`

- proposition: 기존 문서에 가필·변경을 하여 전혀 새로운 내용의 증명을 가지게 한 경우는 변조가 아니라 위조이다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 변경 결과가 전혀 새로운 내용의 증명을 갖는지의 평가는 검토가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.1_7` / `Ⅲ.1`: “기존의 문서에 가필·변경을 가함으로써 전혀 새로운 내용의 증명을 가지게 되는 경우는 변조가 아니고 위조가 된다.”

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

## 23. `art225_sec3_2.alteration_requirements`

- proposition: 공문서·공도화 변조죄는 권한 없는 자가 이미 작성된 문서·도화 내용을 동일성을 해하지 않을 정도로 변경하여 새로운 증명력을 만들고 공공적 신용을 해할 위험성이 있을 때 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 동일성 침해 여부, 새로운 증명력 및 공공적 신용 침해 위험은 구체적 문서와 변경 내용에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_10` / `Ⅲ.2`: “공문서·공도화 변조죄는 권한 없는 자가 공무소 또는 공무원이 이미 작성한 문”
  - `comm_001692_제225조_Ⅲ.2_10` / `Ⅲ.2`: “서·도화 내용에 대하여 동일성을 해하지 않을 정도로 변경을 가하여 새로운 증”
  - `comm_001692_제225조_Ⅲ.2_10` / `Ⅲ.2`: “명력을 작출케 함으로써 공공적 신용을 해할 위험성이 있을 때 성립한다.”

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

## 24. `art225_sec3_2.apparent_official_document`

- proposition: 일반인이 공무원 또는 공무소 권한 내 작성 문서라고 믿을 수 있는지 여부는 문서 형식·외관, 작성 경위, 종류, 내용 및 일반거래상 기능을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 문서의 공문서성 외관은 열거된 사정을 종합하는 평가 문제이며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_10` / `Ⅲ.2`: “일반인으로 하여금 공무원 또는 공무소의 권한 내에서 작성된 문서라고 믿게 할 수 있는지 여부는 그 문서의 형식과 외관은 물론 그 문서의 작성 경위, 종류, 내용 및 일반거래에 있어서 그 문서가 가지는 기능 등 여러 가지 사정을 종합적으로 고려하여 판단하여야 한다.”

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

## 25. `art225_sec3_2.divorce_report_not_confirmation_copy_part`

- proposition: 이혼의사확인서등본 교부 시 이혼신고서를 뒤에 첨부하여 간인하였다는 사정만으로 이혼신고서가 공문서인 이혼의사확인서등본의 일부가 되는 것은 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간인 및 첨부 외에 이혼신고서가 이혼의사확인서등본의 일부로 편입되었다고 볼 수 있는 사정이 있는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_12` / `Ⅲ.2`: “그러한 사정만으로 이혼신고서가 공문서인 이혼의사확인서 등본의 일부가 되었다고 볼 수 없다.”

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

## 26. `art225_sec3_2.id_cover_alteration`

- proposition: 주민등록증 비닐커버 위에 주민등록번호를 덧기재하고 테이프를 붙여 출생연도를 고친 경우, 변경이 공문서 자체에 가해진 것이 아니고 공공의 위험을 초래할 정도의 조잡하지 않은 방법이면 공문서변조죄에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 변경이 공문서 자체에 가해졌는지와 공공의 위험을 초래할 정도인지는 구체적 변조 방법에 따라 판단해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_12` / `Ⅲ.2`: “변조행위가 공문서 자체에 변경을 가한 것이 아니며 그 변조방법이 조 잡하여 공문서에 대한 공공의 위험을 초래할 정도에 이르지 못하였으면 공문서 변조죄에 해당한다고 할 수 없다.”

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

## 27. `art225_sec3_2.name_change_new_document_forgery`

- proposition: 거주증명서에서 해당자 성명의 중요 부분을 다른 글자로 고쳐 외형상 별개의 자연인을 표시하게 함으로써 전혀 별개의 새로운 공문서를 작성한 경우에는 공문서변조죄가 아니라 공문서위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 변경된 기재가 문서를 특정하는 중요 부분인지와 외형상 별개의 자연인을 표시하는지는 구체적 문서별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_12` / `Ⅲ.2`: “거주증명서의 해당자 성명 기재는 위 증명서를 특정하 는 데 극히 중요한 기재이고, 李鳳基와 李永基는 외형상 별개 자연인을 표명한 것이 분명하므로, 이는 위 증명서가 목적하는 특정인 李鳳基의 이름 석자 중 ‘鳳’자를 ‘永’자로 고침으로써 李永基에 대한 거주증명서로서 전연 별개의 새로운 공문서를 작성한 것이므로 공문서변조죄가 아니라 공문서위조죄가 성립한다.”

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

## 28. `art225_sec3_2.partial_copy_no_new_probative_force`

- proposition: 내사결과보고서의 표지를 제외하고 건의 부분을 가린 복사본이 다른 문서 일부의 복사일 가능성이 예상되고 원본 전체 내용을 오인하게 할 가능성이 없으면, 기존 공문서에 새로운 증명력을 작출한 것으로 볼 수 없어 공문서변조죄에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 복사본이 원본 전체 내용을 오인하게 할 가능성과 새로운 증명력 작출 여부는 원본·복사본의 대비를 통해 평가해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_13` / `Ⅲ.2`: “원본인 내사결과보고서의 표지와 ‘7. 건의’ 부분의 내용이 복사된 내사결과보고서의 내용과 상충하여 원본 전체의 내용을 오인하게 할 가능성이 있다고 보기 어려운 경우, 피고인이 내사결과보고서의 표지를 제외하고 ‘건의’부 분을 가린 채 복사한 행위는 기존 공문서에 새로운 증명력을 작출하는 행위로 볼 수 없어 공문서변조죄에 해당하지 않는다.”

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

## 29. `art225_sec3_2.replaced_divorce_report`

- proposition: 당사자가 이혼의사확인서등본과 간인으로 연결된 이혼신고서를 떼어내고 다른 내용의 이혼신고서를 작성하여 함께 호적관서에 제출하더라도, 공문서인 이혼의사확인서등본을 변조하거나 변조된 등본을 행사한 것으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 이혼의사확인서등본과 이혼신고서의 관계에 관한 보고된 판단으로서, 원문 판례와 절차 규정을 확인해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_12` / `Ⅲ.2`: “따라서 당사자가 이혼의사확인서등본과 간 인으로 연결된 이혼신고서를 떼어내고 원래 이혼신고서의 내용과는 다른 이혼 신고서를 작성하여 이혼의사확인서등본과 함께 호적관서에 제출하였다고 하더 라도, 공문서인 이혼의사확인서등본을 변조하였다거나 변조된 이혼의사확인서등 본을 행사하였다고 할 수 없다.”

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

## 30. `art225_sec3_2.seal_certificate_use_purpose`

- proposition: 현행 인감증명서 발급실무에서 부동산 매수자 등의 경우 외 사용용도란 기재는 증명문구로 증명되는 부분과 관계없어 그 부분의 공문서변조는 문제될 여지가 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인감증명서의 현행 발급실무와 해당 사용용도란이 증명문구의 증명 대상인지 확인이 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_11` / `Ⅲ.2`: “부동산 매수자 등 외의 경우 사용용도”
  - `comm_001692_제225조_Ⅲ.2_11` / `Ⅲ.2`: “란의 기재는 증명청인 동장이 작성한 증명문구에 의하여 증명되는 부분과는 아”
  - `comm_001692_제225조_Ⅲ.2_11` / `Ⅲ.2`: “무런 관계가 없으므로 그 부분에 관하여 공문서 변조가 문제될 여지가 없게 되”

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
