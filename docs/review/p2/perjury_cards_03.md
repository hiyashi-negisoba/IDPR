# 위증·모해위증 RuleIR 카드 검수 3

- unit: `perjury`
- articles: art152
- cards: 31–36 / 36
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #1 `art152_sec1_6.perjury_evidence_destruction_relation`: `art152_sec1_6.perjury_evidence_destruction_special_relation` (status=`valid`)

## 31. `art152_sec2_3.noncriminal_case_mohae_exception`

- proposition: 민사·가사·행정·비송 등 형사사건이나 징계사건이 아닌 사건에서 법률에 의하여 선서한 증인이 특정 당사자를 불리하게 할 목적으로 허위진술한 경우, 모해위증죄가 아니라 위증죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사건이 형사사건 또는 징계사건인지와 증인이 법률에 따라 선서하였는지의 확인이 필요하다. 이 카드의 범위에서는 모해 목적이 있어도 비형사·비징계 사건에 관하여 모해위증죄를 적용하지 않는 예외만 다룬다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.3_35` / `Ⅱ.3`: “민사사건, 가사사건, 행정사건, 비송사건 등과 같이 형사사건이나 징계사건이 아닌 사건에서 법률에 의하여 선서한 증인이 특정 당사자를 불리하게 한다는 목적을 가지고 허위의 진술을 하더라도 모해위증죄가 아닌 위증죄가 성립할 뿐 이다.”

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

## 32. `art152_sec2_4.malice_purpose_awareness`

- proposition: 모해 목적은 피고인·피의자·징계혐의자에게 불리하게 될 인식만 있으면 충분하고, 그 결과 발생을 희망하거나 모해 목적이 실제로 달성될 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 불리하게 될 인식의 존재는 개별 사실관계에 대한 평가가 필요하며, 결과 희망 또는 실제 목적 달성의 부재를 반대사실로 추정하지 않는다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.4_36` / `Ⅱ.4`: “에게 불리하게 될 것이라는 인식이 있으면 충분하고, 그 결과의 발생까지 희망 할 필요는 없다. 모해의 목적이 실제로 달성되었는지 여부도 모해위증죄의 성립과는 관계가 없다.”

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

## 33. `art152_sec2_4.proceeding_commenced_requirement`

- proposition: 모해위증죄는 수사절차·재판절차·징계절차가 개시되어 진행 중인 것을 전제로 하며, 수사절차나 징계절차가 개시되지 않은 단계에서는 성립할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 절차 개시 및 진행 여부는 별도의 사실 확인으로 열거 가능하나, 재판절차 미개시의 효과는 인용문에서 명시적으로 설명되지 않아 확대하지 않았다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.4_36` / `Ⅱ.4`: “수사절차나 재판절차 또는 징계절차가 개시되어 진행 중 이라는 사실이 전제되고, 수사절차나 징계절차가 개시되지 않은 단계에서는 모해위증죄가 성립할 수 없다.”

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

## 34. `art152_sec2_6.malicious_perjury.single_offense_same_hearing`

- proposition: 하나의 사건에 관하여 한 번 선서한 증인이 같은 기일에 여러 사실에 관해 기억에 반하는 허위진술을 계속한 경우, 하나의 범죄의사에 따른 계속된 진술로 포괄하여 1개의 모해위증죄가 성립하며 각 진술마다 별개의 모해위증죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 동일 사건, 한 번의 선서, 같은 기일, 기억에 반하는 허위진술의 계속성 및 하나의 범죄의사 여부를 사실관계에 따라 검토해야 한다. commentary에 보고된 판례이므로 원문 판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.6_39` / `Ⅱ.6`: “하나의 사건에 관하여 한 번 선서한 증인이 같은 기일에 여러 가지 사실에 관하여 기억에 반하는 허위의 진술을 한 경우 이는 하나의 범죄의사에 의하여 계속하여 허위의 진술을 한 것으로서 포 괄하여 1개의 모해위증죄가 성립하고, 각 진술마다 여러 개의 모해위증죄가 성 립하는 것은 아니다.”

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

## 35. `art152_sec2_7.special_statute_malicious_perjury_exclusion`

- proposition: 타인에게 형사처분을 받게 할 목적으로 국가보안법상 죄 또는 테러방지법상 죄에 관하여 위증한 경우에는 각 특별법에 따라 처벌되고 모해위증죄는 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 국가보안법 및 테러방지법의 열거된 위증 처벌규정이 적용되는 경우 모해위증죄의 별도 성립을 배제하는 예외로 검토한다.
- bounded sources:

  - `comm_001692_제152조_Ⅱ.7_40` / `Ⅱ.7`: “국가보안법에 규정된 죄에 대하여 위증한 때에는 국가보안법 제12조에 따라, ⅱ) ‘국민보호와 공공안 전을 위한 테러방지법’ 제17조의 죄 (다음부터 ‘테러방지법’이라 한다)(테러단체 구성죄 등)에 대하여 위증을 한 사람은 테러방지법 제18조에 따라 각각 처벌되고, 이 경 우 모해위증죄가 따로 성립하지 않는다.”

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

## 36. `art152_sec1_6.perjury_evidence_destruction_special_relation`

- proposition: 위증죄는 증거인멸죄에 대하여 특별관계에 있으므로, 위증죄가 성립하지 않는 경우에도 증거인멸죄는 성립할 수 있다는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 증거인멸죄와의 관계에 관한 경쟁 견해 중 특별관계설이다. 위증죄 불성립 시 증거인멸죄 성립 가능성의 요건을 별도로 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.6_29` / `Ⅰ.6`: “위증죄가 증거인멸죄에 대하여 법조경합 중 특별관계에 있다는 견해로서, 위증 죄가 성립하지 않는 경우에도 증거인멸죄는 얼마든지 성립할 수 있다고 본다.”

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
