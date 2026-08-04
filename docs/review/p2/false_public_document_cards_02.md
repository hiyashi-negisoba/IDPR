# 허위공문서작성 RuleIR 카드 검수 2

- unit: `false_public_document`
- articles: art227
- cards: 16–30 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #6 `art227_sec3_2.assistant_indirect_perpetration`: `art227_sec3_2.assistant_indirect_perpetration_affirmative` (status=`valid`)

## 16. `art227_sec2_1.false_public_document`

- proposition: 허위공문서는 작성권한 있는 공무원이 내용이 허위임을 인식하면서 진실에 반하는 기재를 하여 작성한 공문서이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 작성권한, 기재 내용의 진실성 및 허위 인식은 기록에 따른 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅱ.1_1` / `Ⅱ.1`: “허위공문서라 함은 문서를 작성할 권한이 있는 공무원이 그 내용이 허위 라는 사실을 인식하면서 진실에 반하는 기재를 하여 작성한 공문서”

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

## 17. `art227_sec2_1.improper_purpose_without_false_content`

- proposition: 공문서 작성의도나 목적이 부정하더라도 기재 내용에 거짓이 없으면 허위공문서작성죄는 성립할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 부정한 작성 목적만으로는 부족하며, 기재 내용의 거짓 여부는 별도로 평가한다.
- bounded sources:

  - `comm_001692_제227조_Ⅱ.1_1` / `Ⅱ.1`: “그 공문서의 작성 의도 내지 목적이 부정한 것이었다 하더라도 거기에 기재된 내 용에 거짓이 없다면 허위공문서작성죄가 성립될 수 없다.”

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

## 18. `art227_sec2_1.inferable_author_public_document`

- proposition: 작성명의인이 명시되지 않아도 문서의 형식·내용 등 문서 자체로 작성자를 추지할 수 있으면 본죄의 객체인 문서가 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서 자체의 형식과 내용으로 작성자를 추지할 수 있는지는 개별 문서에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제227조_Ⅱ.1_1` / `Ⅱ.1`: “작성명의인이 명시되어 있지 아니하더라도 문서의 형식, 내용 등 그 문서 자체에 의하여 누가 작성하였는지를 추지할 수 있을 정도의 것이면 된다.”

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

## 19. `art227_sec2_1.public_document_or_drawing`

- proposition: 본죄의 객체는 공문서 또는 공도화이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공문서 또는 공도화 여부는 본죄 객체의 기본 분류 요소로 검토한다.
- bounded sources:

  - `comm_001692_제227조_Ⅱ.1_1` / `Ⅱ.1`: “본죄의 객체가 되는 문서는 공문서 또는 공도화”

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

## 20. `art227_sec2_2.internal_document_and_nonstatutory_authority`

- proposition: 직무에 관한 문서는 대외적·내부적인지를 구별하지 않고, 직무권한은 법률상 근거뿐 아니라 명령·내규·관례에 따른 직무집행 권한도 포함한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직무 관련성 및 명령·내규·관례에 따른 직무집행 권한의 해당 여부는 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅱ.2_2` / `Ⅱ.2`: “그 문서는 대외 적인 것이거나 내부적인 것을 구별하지 아니하며, 그 직무권한이 반드시 법률상 근거가 있음을 필요로 하는 것이 아니고 명령, 내규 또는 관례에 의한 직무집행의 권한으로 작성하는 경우라도 포함”

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

## 21. `art227_sec3_2.assistant_no_approval_forgery`

- proposition: 작성권한 있는 공무원의 결재를 받지 않고 보조공무원이 임의로 허위 내용의 공문서를 작성권한자 명의로 작성한 때에는 허위공문서작성죄가 아니라 공문서위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 결재의 부재와 작성권한자 명의의 임의 작성 여부에 관한 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.2_7` / `Ⅲ.2`: “작성권한을 가진 공무원의 결재도 받지 아니하고 임의로 허위내용의 공문서를 작성권한자 명의로 작성한 때에는 공문서위조죄가 성립한다.”

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

## 22. `art227_sec3_2.nonofficial_indirect_perpetration_exception`

- proposition: 공무원이 아닌 사람이 공문서 작성권자를 도구로 이용하여 허위 공문서를 작성하게 하더라도 허위공문서작성죄의 간접정범은 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 비공무자가 작성권자를 이용한 경우의 간접정범 배제에 관한 명시적 예외 규칙이다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.2_8` / `Ⅲ.2`: “본죄는 문서의 작성 권자인 공무원만 범할 수 있는 진정신분범으로, 공무원 아닌 사람이 공문서 작 성권자를 생명 있는 도구로 이용하여 허위 공문서를 작성하더라도 본죄의 간접 정범은 성립하지 않는다는 것이다.”

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

## 23. `art227_sec4.execution_act`

- proposition: 본죄는 작성권한 있는 공무원이 행사할 목적으로 직무에 관하여 문서를 허위로 작성하거나 변개할 때 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 작성권한자, 행사 목적, 직무 관련성, 허위 작성 또는 변개라는 열거된 성립요건을 정리한 카드다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ_10` / `Ⅳ`: “본죄는 작성권한 있는 공무원이 행사할 목적으로 그 직무에 관하여 문서를 허 위로 작성하거나 변개할 때 성립한다.”

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

## 24. `art227_sec4_1.alteration`

- proposition: 변개는 해당 공문서의 작성권한자인 공무원이 이미 작성된 문서·도화에 허위 내용을 기재하거나 가필하는 행위이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 작성권한자 여부, 문서의 선행 작성 여부 및 기재·가필 내용의 허위 여부를 구체적으로 확인한다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.1_11` / `Ⅳ.1`: “변개는 당해 공문서의 작성권한자인 공무원이 이미 작성된 문서·도화에”
  - `comm_001692_제227조_Ⅳ.1_11` / `Ⅳ.1`: “대해 허위내용을 기재·가필하는 것을 말한다.”

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

## 25. `art227_sec4_1.false_entry`

- proposition: 본죄에서 허위란 표시된 내용과 진실이 부합하지 않아 문서에 대한 공공의 신용을 위태롭게 하는 경우를 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 표시 내용과 진실의 부합 여부 및 공공의 신용 위험은 구체적 문서 내용에 따라 평가한다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.1_11` / `Ⅳ.1`: “허위공문서작성죄에서 ‘허위’는 표시된 내용과 진실이 부합하지 아니하여 그 문서에 대한 공공의 신용을 위태롭게 하는 경우 를 말한다.”

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

## 26. `art227_sec4_1.legal_error_without_false_facts`

- proposition: 공문서 작성 과정에서 법령을 잘못 적용하거나 적용할 법령을 적용하지 않았더라도, 그 전제가 된 사실관계에 거짓 기재가 없으면 본죄는 성립할 수 없으며 그 잘못이 고의에 기한 경우도 같다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 법령 적용 오류와 그 전제가 된 사실관계의 거짓 기재를 구별하여 검토한다. 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.1_11` / `Ⅳ.1`: “공문서 작성 과정에서 법령 등을 잘못 적용하거나 적용해야 할 법령 등 을 적용하지 않은 잘못이 있더라도 그 적용의 전제가 된 사실관계에 대해 거짓 된 기재가 없다면 허위공문서작성죄가 성립할 수 없고, 그와 같은 잘못이 공무 원의 고의에 기한 것이라도 달라지지 않는다고 한다.”

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

## 27. `art227_sec4_2.false_arrest_notice_documents`

- proposition: 경찰관이 체포사유 및 변호인선임권을 고지하지 않았음에도 이를 고지한 것처럼 허위 현행범인체포서와 확인서를 작성한 경우 허위공문서작성죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 체포 관련 고지 미이행을 고지한 것처럼 기재한 현행범인체포서 및 확인서에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_13` / `Ⅳ.2`: “체포사유 및 변호인선임권을 고지하지 아니하였음에도 불구하고, ‘체포의 사유 및 변호인 선임권 등을 고지 후 현행범인 체포한 것임’이 라는 내용의 허위의 현행범인체포서 4장과”

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

## 28. `art227_sec4_2.false_nis_press_release`

- proposition: 국가정보원 대변인이 직원들의 정치관여 및 선거개입 행위를 은폐하기 위하여 그러한 위법행위가 없었다는 보도자료를 작성·배포한 경우 허위공문서작성죄 및 허위작성공문서행사죄가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 국가정보원 직원들의 위법행위가 없었다는 보도자료 작성·배포 사례에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_14` / `Ⅳ.2`: “국가정보원 심리전단 소속 직원들의 조직적인 정치관여 및 선거개입 행위를 은 폐하기 위하여 그러한 위법행위가 없었다는 내용의 보도자료를 작성하여 배포 한 경우 허위공문서작성죄 및 허위작성공문서행사죄가 인정된다고 한 사례”

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

## 29. `art227_sec4_2.false_reinvestigation_statements`

- proposition: 사법경찰관이 피해자 진술을 청취하지 않고 독자적 의견이나 추측을 마치 직접 들은 피해자 진술처럼 재수사 결과서에 기재한 경우, 일부 내용이 결과적으로 사실과 부합하거나 재조사 방식에 재량이 있어도 허위공문서작성죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자에게서 직접 듣지 않은 독자적 의견 또는 추측을 피해자 진술로 기재한 재수사 결과서에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_14` / `Ⅳ.2`: “피고인은 피해자들로부터 진술을 청취하지 않았고, 특히 피해자들이 진술한 바 없는 내용으로 자신의 독자적인 의견이나 추측에 불과한 것을 마치 피해자들로부터 직접 들은 진술인 것처럼 기재하였으므로”
  - `comm_001692_제227조_Ⅳ.2_14` / `Ⅳ.2`: “피고인 의 행위는 허위공문서작성죄를 구성한다.”

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

## 30. `art227_sec4_2.false_special_tax_report`

- proposition: 감세지시에 따라 추징세액을 맞추기 위하여 확실한 탈루세액을 고의로 누락한 특별조사종결보고서는 객관적 진실에 반하는 허위 공문서이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 확실한 탈루세액을 고의로 누락한 특별조사종결보고서에 관한 보고된 판례 입장이다.
- bounded sources:

  - `comm_001692_제227조_Ⅳ.2_14` / `Ⅳ.2`: “각종 증빙자료 등을 통하여 탈루세액임이 확실한 추징세액 약 55억 7,300만 원을 고의로 누락시킨 채 작성 된 것으로서, 객관적 진실에 반하여 작성된 허위의 공문서이다.”

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
