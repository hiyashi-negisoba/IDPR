# 위증·모해위증 RuleIR 카드 검수 2

- unit: `perjury`
- articles: art152
- cards: 16–30 / 36
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #1 `art152_sec1_6.perjury_evidence_destruction_relation`: `art152_sec1_6.perjury_evidence_destruction_special_relation` (status=`valid`)

## 16. `art152_sec1_3.correction_before_examination_end`

- proposition: 선서한 증인이 허위진술을 하였더라도 신문이 끝나기 전에 이를 철회하거나 시정한 경우 위증죄는 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 동일 증인신문절차가 종료되기 전의 철회·시정에 관한 명시적 예외다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “선서한 증인이 허 위의 진술을 하였다고 하더라도 신문이 끝나기 전에 그 진술을 철회하거나 시 정한 경우에는 위증죄가 성립하지 않는다고 한다.”

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

## 17. `art152_sec1_3.correction_through_other_examiner`

- proposition: 동일한 증인신문절차에서 허위진술이 다른 신문자의 질문에 대한 답변을 통해 철회·시정된 경우, 앞선 진술만을 분리하여 위증으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 후속 답변이 앞선 허위진술의 철회·시정에 해당하는지는 동일 신문절차 및 답변 내용에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “진술의 철회·시정은 다른 신문자의 질문에 대한 답변을 통해서도 이루어져도 무방하다”
  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “원고 대리인의 신문 시에 한 증언을 피고 대리인과 재판장 의 신문 시에 철회·시정한 경우 앞의 증언만을 따로 떼어 위증이라고 볼 수 없 다는 것이다.”

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

## 18. `art152_sec1_3.later_proceeding_correction_no_effect`

- proposition: 허위진술이 철회·시정되지 않은 채 증인신문절차가 종료하여 위증죄가 기수에 이른 후 별도 증인신문절차에서 이를 철회·시정하더라도, 이미 종결된 절차에서의 위증죄 성립에는 영향이 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 별도 증인신문절차에서의 후속 철회·시정은 종전 절차에서 이미 성립한 위증죄에는 영향을 주지 않는다는 소개된 입장이다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “별도의 증인 신청 및 채택 절차를 거쳐 그 증인이 다시 신문을 받는 과정에서 종전 신 문절차에서의 진술을 철회·시정하였다고 하더라도, 이러한 사정은 형법 제153조 가 정한 형의 감면사유에 해당할 수 있을 뿐 이미 종결된 종전 증인 신문절차에 서 행한 위증죄의 성립에 어떠한 영향을 주는 것은 아니다.”

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

## 19. `art152_sec1_3.post_oath_completion`

- proposition: 증인이 신문을 마친 후에 비로소 선서하는 사후선서에서는 선서를 마친 때 위증죄가 기수에 이른다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사후선서의 기수 시점을 선서 완료 시점으로 정리한 카드다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_25` / `Ⅰ.3`: “사후 선서의 경우에는 그 선서를 마쳤을 때 위증죄가 기수에 이르게 된다.”

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

## 20. `art152_sec1_3.preparation_not_punishable`

- proposition: 법정 출석 전에 허위진술 내용을 정리하는 등 위증 준비행위를 하였으나 법정에서 사실대로 진술한 경우, 위증 예비·음모 처벌규정이 없으므로 처벌할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 준비행위만 있고 법정에서 사실대로 진술한 경우의 명시적 불처벌 범위다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “위증을 위한 준비행위를 하였으나 막상 법정에서는 사 실대로 진술한 경우 위증죄의 예비 또는 음모를 처벌하는 규정이 없으므로 처 벌할 수 없음”

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

## 21. `art152_sec1_4.instigation_and_aiding_possible`

- proposition: 위증죄는 자수범이어서 공동정범이나 간접정범은 성립할 수 없지만, 형법 제33조 본문에 따라 교사범 또는 종범은 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 교사범 또는 종범의 성립 가능성을 별도로 제시한 commentary synthesis이며, 공동정범 부정 부분은 관련 학설 대립과 함께 검토가 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.4_26` / `Ⅰ.4`: “위증죄는 자수범이므로 공동정범이나 간접정범은 성립할 수 없으나 형법 제33 조 본문에 따라 교사범 또는 종범은 성립할 수 있다.”

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

## 22. `art152_sec1_4.perjury_self_committed_offense`

- proposition: 위증죄는 법률에 따라 선서한 증인이 허위진술을 해야 성립하는 자수범이다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 자수범성 및 법률상 선서한 증인의 허위진술 요건을 설명하는 commentary synthesis이다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.4_26` / `Ⅰ.4`: “위증죄는 ‘법률에 의하여 선서한 증인’이 주체가 되는 신분범일 뿐 아니라 범죄 의 성립을 위해서 그 증인이 허위의 진술을 할 것이 요구되는 자수범이다.”

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

## 23. `art152_sec1_5.perjury_different_dates_same_oath`

- proposition: 같은 사건·같은 심급에서 서로 다른 변론기일에 허위진술하더라도 최초 선서의 효력이 유지된 상태에서 증언하였다면 1개의 위증죄만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 최초 선서의 효력 유지 여부와 사건·심급의 동일성은 사실관계 및 보고된 판례 원문으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.5_28` / `Ⅰ.5`: “같은 사건의 같은 심급에서 서로 다른 변론기일에 여러 개의 허위진술을 하더라도 최초에 한 선서의 효력을 유지시킨 후 증언한 이상 1개의 위증죄를 구성함에 그친다.”

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

## 24. `art152_sec1_5.perjury_res_judicata_inclusive_offense`

- proposition: 포괄일죄 관계의 위증 일부에 관하여 확정판결이 있으면, 종전 공소사실과 다른 허위진술 부분이라도 그 기판력이 미쳐 후속 위증죄 부분은 면소되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 포괄일죄 범위와 기판력의 범위를 적용하기 전에 보고된 판례 원문 및 종전 공소사실을 확인해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.5_28` / `Ⅰ.5`: “종전 사건의 확정판결의 기판력은 당해 사건에도 미치게 되어 당해 사건의 위 증죄 부분은 형사소송법 제326조에 따라 면소되어야 한다.”

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

## 25. `art152_sec1_5.separate_instigation_multiple_persons`

- proposition: 하나의 사건에서 여러 사람에게 각각 개별적으로 위증을 교사한 경우 위증교사죄는 경합범이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 개별 교사행위와 각 피교사자의 위증이 확인되는 경우에 한정한 죄수 분류 카드다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.5_28` / `Ⅰ.5`: “하나의 사건이라도 하더라도 여러 사람에 대하여 각각 개별적으로 교사 행위를 하여 위증하게 한 경우에는 위증교사죄의 경합범이 될 것이다.”

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

## 26. `art152_sec1_5.single_perjury_same_hearing`

- proposition: 하나의 사건에서 한 번 선서한 증인이 같은 기일에 여러 사실에 관하여 기억에 반하는 허위진술을 계속한 경우 포괄하여 1개의 위증죄가 성립하고, 각 허위진술별 경합범이 되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 포괄일죄 및 경합범 배제의 보고된 판례 기준에 대한 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.5_28` / `Ⅰ.5`: “하나의 사건에서 한 번 선서한 증인이 같은 기일에 여러 가지 사실에 관하여 기 억에 반하는 허위의 진술을 한 경우 이는 하나의 범죄의사에 의하여 계속하여 허위의 진술을 한 것으로서 포괄하여 1개의 위증죄를 구성하고, 각 허위 진술마 다 별개의 위증죄가 성립하여 경합범이 되는 것은 아니다.”

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

## 27. `art152_sec1_6.false_accusation_perjury_concurrence`

- proposition: 타인에게 형사처분을 받게 할 목적으로 허위신고한 자가 그 사람이 기소된 뒤 증인으로서 신고 내용과 같은 진술을 하면 무고죄와 위증죄가 각각 성립하고 실체적 경합범 관계에 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인용문에 괄호로 모해위증죄가 병기되어 있어, 무고죄·위증죄의 실체적 경합범 부분과의 관계를 원문 및 관련 판례로 확인해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.6_29` / `Ⅰ.6`: “다른 사람으로 하여금 형사처분을 받게 할 목적으로 허위신고를 한 후 그 사람 이 기소되어 재판을 받게 되자 증인으로서 허위신고 내용과 같은 진술을 한 경 우 무고죄와 위증죄가 각각 성립하고 두 죄는 실체적 경합범의 (또는 모해위증죄) 관계에 있다.”

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

## 28. `art152_sec1_6.malicious_perjury_after_false_accusation`

- proposition: 무고행위자가 증인으로서 허위신고와 같은 허위진술을 하면서 피무고자를 모해할 목적을 가진 경우 대체로 위증죄보다 모해위증죄가 성립하는 것으로 서술되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 모해 목적의 인정은 사실관계 평가가 필요하며, 이 서술이 확정적 판례 기준인지 확인이 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.6_29` / `Ⅰ.6`: “위증 당시 피무고자를 모해하고자 하는 목적을 갖고 있는 경우가 대부분일 것이므로, 대체로 위증죄보다는 모해위증죄가 성립할 것으로 보인다.”

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

## 29. `art152_sec1_6.oath_incompetent_false_testimony_not_evidence_fabrication`

- proposition: 선서무능력자가 범죄현장을 목격한 것처럼 형사법정에서 허위증언하게 하였더라도 증거위조죄에는 해당하지 않는다는 대법원 판시가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 대법원 판시이므로, 적용 전 사용자 제공 1차 판례 색인에서 판결 원문과 사실관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.6_30` / `Ⅰ.6`: “선서무능력자로서 범죄 현장을 목격하지도 못한 사람으로 하 여금 형사법정에서 범죄 현장을 목격한 것처럼 허위의 증언을 하도록 하였더라도 증거위조죄에는 해당하지 않는다고 판시하였다.”

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

## 30. `art152_sec2_1.malicious_perjury_definition`

- proposition: 모해위증죄는 피고인·피의자·징계혐의자를 모해할 목적으로 허위진술한 경우 성립하는 목적범이며, 위증죄의 가중적 구성요건이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 모해 목적 및 허위진술의 사실관계 포섭은 평가적 판단을 필요로 한다. 주체 범위와 관련 쟁점은 현재 source scope에서 확인되지 않는다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.1_33` / `Ⅱ.1`: “피고인이나 피의자 또는 징계혐의자를 모해할 목적으로 허위의 진술을 한 경우에 성립하는 목적범으로서 형법 제152조 제1항에 규정된 위증죄의 가중적 구성요건에 해당한다.”

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
