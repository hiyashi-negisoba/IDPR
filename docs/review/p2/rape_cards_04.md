# 강간 RuleIR 카드 검수 4

- unit: `rape`
- articles: art297
- cards: 46–56 / 56
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art297_sec9.continued_confinement_after_rape`

- proposition: 감금행위가 강간의 수단에 그치지 않고 강간 범행이 끝난 뒤에도 계속된 경우 감금죄와 강간죄는 실체적 경합범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 감금이 강간 종료 후에도 계속되었는지에 대한 사실인정이 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_26` / `Ⅸ`: “감금행위가 단순히 강간 범행의 수단이 되는 데 그치지 아니하고 강 간의 범행이 끝난 뒤에도 계속된 경우에는 감금죄와 강간죄는 실체적 경합범이 성립한다.”

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

## 47. `art297_sec9.means_violence_absorption`

- proposition: 강간죄 수단으로 행해진 폭행·협박은 강간죄에 흡수되어 별도로 폭행죄나 협박죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행·협박이 강간죄의 수단으로 행해진 경우에 한정된 흡수 규범이다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_24` / `Ⅸ`: “본죄의 수단으로 행해진 폭행·협박은 본죄가 성립하면 이에 흡수되어 법조경합 의 관계에 있게 되므로, 따로 폭행죄나 협박죄 등을 구성하지 않는다.”

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

## 48. `art297_sec9.nonprosecution_not_false_report_proof`

- proposition: 성폭행 등 피해 신고에 관하여 증거불충분 등의 불기소처분이나 무죄판결이 내려졌다는 사정만으로 신고내용을 허위라고 단정하여 무고의 적극적 근거로 삼아서는 안 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 불기소처분 또는 무죄판결이라는 사정만으로 신고 허위를 추론하지 않는 제한 규범이다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_26` / `Ⅸ`: “성폭행 등의 피해를 입었다는 신고사실에 관하여 불기소처분 내지 무죄판결이 내려졌다고 하여, 그 자체를 무고를 하였다는 적극 적인 근거로 삼아 신고내용을 허위라고 단정하여서는 아니 된다.”

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

## 49. `art297_sec9.rape_injury_death`

- proposition: 강간 범행 과정에서 피해자가 상해를 입으면 강간상해죄나 강간치상죄가, 피해자가 사망하면 강간살인죄나 강간치사죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 상해·사망 결과 및 고의·인과관계에 따라 각 죄명 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: “강간 범행의 과정에서 피해자가 상해를 입은 경우에는 강간상해죄나 강간치상 죄가 성립하고, 피해자가 사망한 경우에는 강간살인죄나 강간치사 (형법 제301조) 죄가 성립한다.”

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

## 50. `art297_sec9.residence_intrusion_rape`

- proposition: 주거침입죄를 범한 자가 강간죄를 범한 때에는 성폭력범죄의 처벌 등에 관한 특례법상 주거침입강간죄가 단순일죄로 성립하여 가중처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 주거침입죄 및 강간죄의 성립과 특례법상 가중유형 적용을 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: “이제 주거침입죄를 범한 자가 강간죄를 범한 때에는 단순일죄인 성폭력범죄의 처벌 등에 관한 특례법상의 주 거침입강간죄가 성립되어 가중처 (성폭력범죄의 처벌 등에 관한 특례법 제3조 제1항) 벌된다.”

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

## 51. `art297_sec9.robbery_rape`

- proposition: 강도죄를 범한 자가 그 기회에 동일 피해자를 강간하면 강도강간죄의 단순일죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강도죄와 동일 피해자에 대한 강간이 결합된 경우의 특례 범죄유형이다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_24` / `Ⅸ`: “강도죄를 범한 자가 그 기회에 동일한 피해자를 강간한 경 (형법 제333조) 우에는 강도강간죄의 단순일죄가 성립한다.”

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

## 52. `art297_sec9.separate_confinement_rape_violence`

- proposition: 감금 중 강간의 고의가 생겨 별도의 폭행·협박을 통해 강간한 경우 감금죄와 강간죄는 실체적 경합범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 감금 당시 강간 고의의 부재와 이후 별도 폭행·협박의 존재를 각각 검토해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_26` / `Ⅸ`: “감금 중 강간의 고의가 생겨 별도의 폭행·협박을 통해 강간한 경 우에는 실체적 경합범이 성립한다.”

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

## 53. `art297_sec9.special_rape`

- proposition: 흉기 등 위험한 물건을 지니거나 2인 이상이 합동하여 강간한 경우에는 강간죄가 아니라 특수강간죄가 성립하여 가중처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위험한 물건 소지 또는 2인 이상 합동이라는 가중유형의 적용요건을 별도 확인한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_24` / `Ⅸ`: “‘흉기 그 밖의 위험한 물건을 지니거나 2인 이상이 합동하여’ 강간한 경우에는 본죄가 아니라 [후론 1]에서 살펴볼 성폭력범죄의 처벌 등에 관한 특례법 제4조 제1항의 특수강간죄가 성립하여 가중 처벌된다.”

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

## 54. `art297_sec9.special_robbery_rape`

- proposition: 특수강도죄를 범한 자가 강간죄를 범한 때에는 성폭력범죄의 처벌 등에 관한 특례법상 특수강도강간죄가 단순일죄로 성립하여 가중처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 특수강도죄 및 강간죄의 성립 여부와 특례법 적용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: “특수강도죄를 (제334조) 범한 자가 강간죄를 범한 때에도 단순일죄인 성폭력범죄의 처벌 등에 관한 특 례법상 특수강도강간죄가 성립되 (성폭력범죄의 처벌 등에 관한 특례법 제3조 제2항) 어 가중된 형으로 처벌된다.”

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

## 55. `art297_sec9.special_theft_rape`

- proposition: 야간주거침입절도죄 또는 특수절도죄를 범한 자가 강간죄를 범한 경우 성폭력범죄의 처벌 등에 관한 특례법상 특수절도강간 등의 죄가 단순일죄로 성립하여 가중처벌된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 선행 범죄가 야간주거침입절도죄 또는 특수절도죄에 해당하는지와 특례법상 죄명을 확인한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: “야간주거침입절도죄 또는 (제330조) 특수절도죄를 범한 자가 강간죄를 범한 경우에는 단순일죄인 성폭력범 (제331조) 죄의 처벌 등에 관한 특례법상의 특수절도강간 등의 죄 (성폭력범죄의 처벌 등에 가 성립되어 가중처벌된다.”

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

## 56. `art297_sec9.theft_rape_concurrence`

- proposition: 절도죄를 범한 자가 피해자를 강간한 경우 절도죄와 강간죄는 실체적 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 선행 절도와 피해자에 대한 강간의 관계가 해당 서술의 범위에 드는지 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅸ_25` / `Ⅸ`: “절도죄를 범한 자가 그 피해자를 강간한 경우에는 절도죄와 강간죄의 실체적 경합범이 되지만”

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
