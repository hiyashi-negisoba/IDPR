# 공문서등위조·변조 RuleIR 카드 검수 3

- unit: `public_document_forgery`
- articles: art225
- cards: 31–43 / 43
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art225_sec3_2.unexplained_dotted_lines`

- proposition: 인낙조서에 첨부된 도면 및 사본에 임의로 그은 점선이 본문이나 도면에서 설명되지 않아 특정한 의미 내용이 없는 단순 도형에 그치는 경우, 새로운 증명력이 작출되지 않으므로 공도화변조죄에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 점선이 본문 또는 도면과의 관계에서 특정한 의미를 가지는지와 새로운 증명력 작출 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제225조_Ⅲ.2_12` / `Ⅲ.2`: “인낙조서 본문이나 도면에서 그에 대한 설명이 없는 이상 특정한 의미 내 용을 갖지 아니한 단순한 도형에 불과하여 그 자체로서 새로운 증명력이 작출 된다고 할 수 없으므로, 그와 같은 점선을 그은 행위가 문서의 손괴에 해당할 수 있음은 별론으로 하고, 공도화로서의 공공적 신용을 해할 위험이 있는 공도 화변조죄에 해당한다고 할 수 없다.”

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

## 32. `art225_sec4_1.abstract_intent_to_use`

- proposition: 행사할 목적은 특정된 사실에 관한 것일 필요가 없고 추상적으로 문서를 사용하고자 하는 의도만 있으면 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 추상적 사용 의도의 인정은 행위 전후 사정에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.1_14` / `Ⅳ.1`: “반드시 특정된 사실에 대한 것임을 요하지 않고 단지 추상적으로 문서를 사용하고자 하는 의도만 있으면 인정된다.”

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

## 33. `art225_sec4_1.altered_document_use_not_limited`

- proposition: 공문서변조죄의 행사할 목적은 변조 문서를 진정한 문서처럼 사용하여 상대방에게 문서 진정에 관한 착오를 일으킬 목적이면 충분하고, 변조 전 문서의 본래 용도에 사용할 목적에 한정되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 공문서변조죄에 한정된 행사할 목적의 범위를 다룬다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.1_14` / `Ⅳ.1`: “공문 서변조죄에서 행사할 목적이란 변조된 공문서를 진정한 문서인 것처럼 사용할 목적, 즉 행사의 상대방이 누구이든지간에 그 상대방에게 문서의 진정에 대한 착오를 일으킬 목적이면 충분한 것이지 반드시 변조 전의 그 문서의 본래의 용 도에 사용할 목적에 한정되는 것은 아니다.”

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

## 34. `art225_sec4_1.intent_to_use_definition`

- proposition: 행사할 목적은 타인으로 하여금 위조·변조된 문서를 진정한 것처럼 오신하게 하는 데 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 문서의 진정에 관한 타인의 오신을 초래하려는 목적은 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.1_14` / `Ⅳ.1`: “행사할 목적은 타인으로 하여금 위조·변조된 문서를 진정한 것처럼 오신하게 하는 데 있고”

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

## 35. `art225_sec4_1.intent_to_use_requirement`

- proposition: 공문서등의 위조·변조죄가 성립하려면 행사할 목적을 가지고 공문서를 위조·변조하여야 하며, 이 죄는 목적범이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행사할 목적의 존재 여부는 개별 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.1_14` / `Ⅳ.1`: “본죄가 성립하기 위해서는 행사할 목적으로 공문서를 위조·변조하여야 한다. 따 라서 본죄는 목적범이다.”

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

## 36. `art225_sec4_1.intent_to_use_time_of_act`

- proposition: 행사할 목적은 행위 당시 존재하여야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 목적의 판단 시점을 위조·변조 행위 당시로 특정하는 시간 관계다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.1_14` / `Ⅳ.1`: “행사할 목적은 (故意) 행위 당시에 존재하여야”

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

## 37. `art225_sec4_2.intent-for-forgery`

- proposition: 본죄의 고의는 작성권한 없는 자가 공무소 또는 공무원 명의의 문서·도화를 작성한다는 사실을 인식하고 용인하는 것을 뜻한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 고의의 인식·용인 여부는 개별 사실관계에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.2_15` / `Ⅳ.2`: “본죄의 고의는 문서의 작성권한이 없는 자가 공무소, 공무원 명의의 문서, 도화를 작성 하는 것을 인식하고 용인하는 것을 말한다.”

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

## 38. `art225_sec4_2.unauthorized-addition-approved-document-intent`

- proposition: 기안담당자가 누락 토지를 사후에 일치시킬 생각으로 재산명세서에 추가 기재하였더라도, 적법한 절차 없이 결재된 원문서에 없는 사항을 임의로 추가한 이상 공문서변조의 범의를 인정하기에 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 사실관계 및 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.2_15` / `Ⅳ.2`: “사후에 이를 일치시킨다는 생각에서 위 재산명세서상에 그 누락된 토지들을 추가 기재하였더라도 그 과정 에서 적법한 절차를 거침이 없이 임의로 결재된 원문서에 없는 사항을 추가 기 재한 이상 그러한 행위에 대하여는 공문서변조의 범의를 인정하기에 충분하다.”

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

## 39. `art225_sec4_2.unauthorized-substitution-map-intent`

- proposition: 도시계획 담당 공무원이 적법한 절차 없이 당초 도면을 정정도면으로 바꿔치기한 경우, 도면에 간인이 없거나 시장 승인이 예상된다는 사정만으로 공문서변조 및 변조공문서행사의 범의를 부정할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 적용 범위와 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅳ.2_15` / `Ⅳ.2`: “시에서 도시계획 업무를 담당한 공무원이 적법한 절차를 거치지 않은 채 임의로 당초의 도면을 정정도면과 바꿔 치기 한 행위에 대하여는 공문서변조, 변조공문서행사의 범의를 넉넉히 인정할 수 있고, 도면에 간인이 없다거나 시장의 승인이 예상된다 하여 그 범의를 부정 할 수는 없다.”

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

## 40. `art225_sec5.attempt_commencement`

- proposition: 위조·변조 의사를 확정적으로 문서에 표시하는 행위가 있으면 실행의 착수가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 문서에 위조·변조 의사가 확정적으로 표시되었는지는 개별 행위의 내용에 따라 평가한다.
- bounded sources:

  - `comm_001692_제225조_Ⅴ_16` / `Ⅴ`: “실행의 착수는 위조·변조의 의사를 확”
  - `comm_001692_제225조_Ⅴ_16` / `Ⅴ`: “정적으로 문서에 표시하는 행위가 있으면 성립하고”

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

## 41. `art225_sec5.attempt_document_not_deceptive`

- proposition: 작성된 문서가 일반인이 진정한 것이라고 오신할 정도에 이르지 못한 때에는 미수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인이 진정한 문서로 오신할 정도에 이르렀는지는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제225조_Ⅴ_16` / `Ⅴ`: “작성된 문서가 일반인이 진 정한 것이라고 오신할 정도에 이르지 못한 때에 미수죄가 성립한다.”

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

## 42. `art225_sec5.attempt_punishable`

- proposition: 본죄의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 미수범 처벌 여부에 관한 직접적 서술이다.
- bounded sources:

  - `comm_001692_제225조_Ⅴ_16` / `Ⅴ`: “본죄는 미수범을 처벌한다.”

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

## 43. `art225_sec5.waste_bag_film_preparation_only`

- proposition: 종량제 쓰레기봉투에 인쇄할 시장 명의 문안이 새겨진 필름 제조에 그친 경우에는 시장 명의 공문서인 쓰레기봉투 위조의 실행 착수에 이르지 못한 준비단계에 불과하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 필름 제조에 그친 구체적 경우에 한정된 실행 착수 부정 서술로 검토한다.
- bounded sources:

  - `comm_001692_제225조_Ⅴ_16` / `Ⅴ`: “종량제 쓰레기봉투에 인쇄할 시장 명의의 문안이 새겨진 필름을 제조하 는 행위에 그친 경우에는 아직 위 시장 명의의 공문서인 종량제 쓰레기봉투를 위조하는 범행의 실행의 착수에 이르지 아니한 것으로서 그 준비단계에 불과하다.”

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
