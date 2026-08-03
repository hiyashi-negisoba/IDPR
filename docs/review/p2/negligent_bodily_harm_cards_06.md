# 과실치사·업무상과실치사상 RuleIR 카드 검수 6

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 76–85 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 76. `art268_sec3_2.safety_duty_complete_overlap`

- proposition: 단속법규상 안전의무가 구체적 주의의무 내용과 완전히 일치하는 경우 단속법규위반죄는 업무상과실치사상죄에 흡수되어 업무상과실치사상죄 1죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 흡수 관계는 두 의무의 내용이 완전히 일치한다는 전제에서만 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “단속법규상의 안전의무가 구체적인 주의의무의 내용과 완전히 일치하는 경우에 있어서는 단속법규위반의 죄는 업무상과실치사상죄에 흡수되어 업무상과실치사상 죄 1죄만 성립하고”

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

## 77. `art268_sec3_2.safety_duty_partial_overlap`

- proposition: 법규위반이 주의의무의 일부에 불과하고 별도 조치로 결과회피가 가능했던 경우 단속법규상 의무와 주의의무는 일치하지 않으며, 하나의 행위가 두 죄에 해당하는 상상적 경합관계가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 별도 조치에 의한 결과회피 가능성과 행위 단일성의 판단이 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “법규위반이 있어도 그로써 바로 사고가 발생한 것이 아니고 별도의 조치에 의하여 결과를 회피하는 것이 가능한 때는 단속법규상의 의무와 주의의무는 일치하지 아니하고 이 경우에는 1개의 행위가 2개의 죄에 해 당하는 상상적 경합관계에 있다고 보아야 할 것이다.”

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

## 78. `art268_sec3_2.safety_duty_unrelated`

- proposition: 단속법규상 안전의무와 업무상 주의의무가 전혀 관계없는 경우에는 별개의 죄가 성립하고 실체적 경합이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 안전의무와 업무상 주의의무가 전혀 관계없는지 여부를 사안별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “그러나 양자가 전혀 관계없 는 경우에는 별개의 죄가 성립하고 그 관계는 실체적 경합으로 된다고 할 것이다.”

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

## 79. `art268_sec3_2.safety_regulation_duty_distinction`

- proposition: 업무상과실치사상죄의 구체적 주의의무와 단속법규상 안전의무는 사고회피 목적에서 공통되지만, 전자는 구체적 사안의 결과발생 위험 방지조치이고 후자는 일반적·정형적 위험상태 회피조치이므로 항상 일치하지는 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 두 의무의 일치 여부는 적용 사안의 구체적 위험과 요구 조치를 비교하여 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_108` / `Ⅲ.2`: “전자는 구체적인 사안에 서 결과발생의 위험을 방지하기 위해 취하여 할 적절하고 마땅한 조치임에 대하 여 후자는 일반적·정형적인 위험상태를 회피함을 목적으로 필요한 조치를 규정한 것이므로 때로는 일치하는 경우도 있으나 항상 양자가 일치되는 것은 아니다.”

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

## 80. `art268_sec3_2.serious_disaster_industrial_safety_negligent_death`

- proposition: 같은 일시·장소에서 동일 피해자의 사망 방지에 실패한 부작위에 의한 중대재해처벌법위반, 산업안전보건법위반 및 업무상과실치사죄는 사회관념상 하나의 행위로서 상상적 경합 관계가 될 수 있다는 대법원 판결이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글이 소개한 대법원 판결의 원문 및 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “모두 같은 일 시·장소에서 같은 피해자의 사망이라는 결과 발생을 방지하지 못 한 부작위에 의한 범행에 해당하여 각 그 법적 평가를 떠나 사회관념상 1개의 행위로 평가할 수 있다.”
  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “따라서 중대재해처벌법위반죄와 근로자 사망으로 인한 산업안전보건 (산업재해치사) 법위반죄는 상상적 경합 관계에 있다.”
  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “중대재해처벌법위반(죄와 업무상과실치사죄 역시 행위의 동 산업재해치사) 일성이 인정되어 상상적 경합 관계에 있다.”

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

## 81. `art268_sec3_2.traffic_special_act_inclusion`

- proposition: 교통사고처리특례법 제3조 제1항의 죄가 성립하는 경우 업무상과실치사상죄는 그 죄에 포함되어 별죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 교통사고처리특례법 제3조 제1항의 죄 성립이 전제되는 포함 관계 카드다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “교통사고처리특례법 제3조 제1항의 죄는 차의 운전자가 교통사고로 인하여 형법 제268조를 범한 경우에 성립하는 것으로서 업무상과실치사 (업무상과실치사상죄) 상죄는 위 죄에 포함하여 별죄를 구성하지 아니한다.”

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

## 82. `art268_sec3_2.unlicensed_driving_negligent_injury`

- proposition: 무면허운전 중 과실치사상죄를 범한 경우 도로교통법위반죄와 업무상과실치사상죄는 실체적 경합이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 무면허운전 중 과실치사상죄가 성립한 경우의 죄수 관계를 정리한 카드다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “무면허운전 도중 과실치사상죄를 범한 때에는 도로교통법위반죄와 (무면허운전) 업무상과실치사상죄의 실체적 경합이 된다.”

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

## 83. `art268_sec3_2.vehicle_accident_conditional_intent`

- proposition: 교통사고에서 피해자에 대한 살인 또는 상해의 미필적 고의가 인정되면 살인죄·상해죄·상해치사죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 미필적 고의 인정은 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_108` / `Ⅲ.2`: “교통사고에 의해 사람이 사망하거나 상해가 발생하였는데, 만약 행위자에게 피 해자에 대한 살인 내지 상해의 미필적 고의를 인정할 수 있다면 살인죄, 상해죄, 상해치사죄가 성립한다.”

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

## 84. `art268_sec3_2.vehicle_avoidance_effort_negligence`

- proposition: 운전 중 다른 사람이나 차량과 충돌해도 상관없다고 생각했더라도, 현실적으로 상대방을 직면하여 감속·서행 등 사고회피 노력을 한 경우에는 충돌사고가 발생하더라도 폭행의 실행이 아니라 과실에 그친다고 보아야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사고회피 노력과 폭행 실행 여부는 구체적 운전 상황의 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_108` / `Ⅲ.2`: “현실적으로 다른 사람이나 차를 직면하여 순식간에 감속이나 서행하는 등 사고 를 피하기 위한 노력을 한 때에는 그것이 주효하지 않아서 충돌사고를 발생시 켰다고 하더라도 폭행의 실행이 있다고는 할 수 없고 과실이 있음에 그친다고 보아야 할 것이다.”

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

## 85. `art268.illicit_work_excluded`

- proposition: 소매치기, 밀수, 성매매와 같이 사회적으로 용인할 수 없는 불법한 일은 형법상 업무에 해당하는 사무가 될 수 없고, 절도범이 범행 중 과실로 타인을 상해한 경우 업무상과실치상죄가 아니라 과실치상죄가 성립할 수 있다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 무면허 위험업무에 이 명제를 적용할 수 있는지는 반대 카드 및 판례 소개를 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_6` / `Ⅰ.2`: “소매치기(절도), 밀수, 성매매 등과 같이 사회적으로 용인할 수 없는 불법한 일은 형법상 업무에 해당하는 사무가 될 수 없다.”
  - `comm_001692_제268조_Ⅰ.2_6` / `Ⅰ.2`: “절도범이 범행 중 과실로 주인에게 상처를 입힌 경우 업무상과실치상죄가 아닌 과실치상죄가 성립할 수 있을 뿐이다.”

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
