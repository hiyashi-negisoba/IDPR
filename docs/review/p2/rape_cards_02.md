# 강간 RuleIR 카드 검수 2

- unit: `rape`
- articles: art297
- cards: 16–30 / 56
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art297_sec4_1.extramarital_exposure_threat`

- proposition: 유부녀에게 혼인 외 성관계 사실 폭로를 협박하여 간음 또는 추행한 경우, 협박 정도는 폭로의 상대방·범위·방법, 협박 경위, 당사자 신분·사회적 지위와 관계, 당시 및 이후 정황, 심리적 압박 등을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 혼인 외 성관계 폭로 협박 맥락의 제한된 종합판단 기준이다. 폭로 상대방·범위·방법에 관한 구체적 원문 근거는 현 인용 범위에서 확인되지 않는다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_14` / `Ⅳ.1`: “히 협박의 내용만으로 그 정도를 단정할 수는 없고, 그 밖에도 협박의 경위, 가 해자 및 피해자의 신분이나 사회적 지위, 피해자와의 관계, 간음 또는 추행 당시 와 그 후의 정황, 그 협박이 피해자에게 미칠 수 있는 심리적 압박의 내용과 정 도 등 모든 사정을 종합하여 신중하게 판단하여야 한다.”

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

## 17. `art297_sec4_1.force_threat_temporal_gap`

- proposition: 폭행·협박이 선행된 경우 폭행·협박과 간음 사이에는 시간적 간격이 있을 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 선행 폭행·협박과 간음 사이의 시간 간격을 허용하는 commentary-reported authority다. 인과적 관련성의 구체적 한계는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_10` / `Ⅳ.1`: “폭행·협박이 선행된 경우 간음과 사이에 시간적 간격이 있을 수 있다.”

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

## 18. `art297_sec4_1.force_threat_timing_before_completion`

- proposition: 폭행·협박은 반드시 간음행위보다 선행할 필요는 없고, 간음행위 종료 전까지 있으면 충분하다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행·협박과 간음 사이의 시간적 관계에 관한 명시적 설명이다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_9` / `Ⅳ.1`: “폭행·협박이 반드시 간음행위보다 선행되어야 하는 것은 아니고 간음행위 종료 전에 있으면 충분하다.”

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

## 19. `art297_sec4_1.gender_sensitive_limit`

- proposition: 성인지적 관점을 유지하더라도 성범죄 피해자 진술의 합리성·타당성 및 객관적 정황 등에 비추어 증명력을 인정할 수 없는 경우는 있을 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 성인지적 관점이 진술 증명력을 자동적으로 인정하게 하는 것은 아니라는 제한이다. 구체적 증명력 평가는 전체 증거관계에 따라 이루어져야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_13` / `Ⅳ.1`: “성범죄 피해자 진술에 대하여 성인지적 관점을 유지하여 보더라도, 진술 내용 자체의 합리성·타당성뿐만 아니라 객관적 정황, 다른 경험칙 등에 비추어 증명력을 인정할 수 없는 경우가 있을 수 있다.”

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

## 20. `art297_sec4_1.gender_sensitive_testimony`

- proposition: 성폭력 피해자 진술의 신빙성을 판단할 때 성인지 감수성을 잃지 않아야 하며, 피해자에게 특정한 피해자다움을 요구하거나 그와 다른 반응만으로 진술을 함부로 배척해서는 안 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특정한 피해자 반응을 요구하여 신빙성을 배척하는 것을 금지하는 제한이다. 보고된 판례의 원문과 증명력 판단 전체 구조를 확인해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_10` / `Ⅳ.1`: “의 신빙성 판단 시 ‘성인지 감수성’을 잃지 않아야 하고, 피해자에게 ‘피해자다 움’을 요구하여 피해자가 ‘마땅히 그러한 반응을 보여야만 하는 피해자’로 보이 지 않는다는 이유만으로 피해자 진술의 신빙성을 함부로 배척할 수 없음을 강 조하고 있다.”

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

## 21. `art297_sec4_1.no_retrospective_inference`

- proposition: 피해자가 사후적으로 범행 현장을 벗어날 수 있었거나 사력을 다해 반항하지 않았다는 사정만으로 폭행·협박이 항거를 현저히 곤란하게 할 정도가 아니었다고 섣불리 단정해서는 안 된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사후 탈출 가능성 또는 적극적 반항 부재만으로 부정 결론을 내리지 말라는 제한이다. primary precedent 확인이 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_10` / `Ⅳ.1`: “사후적으로 보아 피해자가 범행 현장을 벗어날 수 있었 다거나 피해자가 사력을 다하여 반항하지 않았다는 사정만으로 가해자의 폭행· 협박이 피해자의 항거를 현저히 곤란하게 할 정도에 이르지 않았다고 섣불리 단정하여서는 안 된다.”

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

## 22. `art297_sec4_1.third_party_or_property_threat`

- proposition: 제3자에 대한 폭행, 피해자 소유 기물 파괴 또는 피해자 가족 위협 등의 방법으로 피해자의 저항 의지를 꺾은 뒤 간음한 경우에도 강간죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자 신체에 직접 향하지 않은 행위가 저항 의지를 꺾었는지와 폭행·협박의 정도는 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_8` / `Ⅳ.1`: “피해자 소유의 기물을 파괴하거나 피해자의 가족을 위협하는 등의 방법 으로 피해자의 저항 의지를 꺾은 다음 간음하는 경우에도 강간죄가 성립할 수 있다.”

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

## 23. `art297_sec4_1.threat_alone`

- proposition: 폭행 없이 협박만으로 피해자를 간음한 경우에도 그 협박이 항거를 불가능하게 하거나 현저히 곤란하게 할 정도이면 강간죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 협박만으로도 충족될 수 있다는 좁은 상황의 commentary-reported precedent이다. 협박 정도와 원문 판례를 확인해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_14` / `Ⅳ.1`: “폭행을 수반함이 없이 오직 협박만을 수단으로 피해자를 간음한 경우에도 그 협박의 정도가 항거를 불가능하게 하거나 현저히 곤란하게 할 정도의 것이 면 강간죄가 성립한다.”

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

## 24. `art297_sec4_1.victim_testimony_reliability`

- proposition: 성폭력 사건에서 피해자 진술이 유일한 직접증거인 경우, 주요 부분의 일관성·구체성, 논리와 경험칙상 합리성, 객관적 사실과의 모순 여부 및 허위 불리진술 동기 등을 종합하여 신빙성을 신중히 판단해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자 진술의 증명력 판단 기준으로 보고된 내용이다. 직접증거의 유무와 각 신빙성 요소는 구체적 증거기록에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_10` / `Ⅳ.1`: “피해자의 진술이 합리 적인 의심을 배제할 만한 신빙성이 있는지 여부는 그 진술 내용의 주요한 부분 이 일관되고 구체적인지, 진술 내용이 논리와 경험칙에 비추어 합리적이고, 진 술 자체로 모순되거나 객관적으로 확인된 사실이나 사정과 모순되지는 않는지, 또는 허위로 피고인에게 불리한 진술을 할 만한 동기나 이유가 있는지 등을 종 합적으로 고려하여 신중하게 판단하여야 한다.”

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

## 25. `art297_sec4_1.violence_threat_definition`

- proposition: 강간죄의 수단인 폭행은 사람의 신체에 대한 유형력 행사 등 일체의 불법적 공격이고, 협박은 일반적으로 사람에게 공포심을 일으킬 수 있는 정도의 해악 고지이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행·협박의 일반적 개념을 제시한 commentary synthesis이며, 제297조 수단요건 충족 여부의 개별 판단은 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_8` / `Ⅳ.1`: “일반적으로 ‘폭행’이란 사람의 신체에 대한 유형력의 행사 등 일체의 불법적인 공격을 말하고, ‘협박’은 (有形力) 일반적으로 보아 사람으로 하여금 공포심을 일으킬 수 있을 정도의 해악을 고 지하는 것을 말한다”

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

## 26. `art297_sec4_2.non_vaginal_acts_exception`

- proposition: 구강성교나 항문성교 등은 강간죄의 간음에 해당하지 않으며, 이 경우 유사강간죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강간죄의 간음 범위에 대한 명시적 제외를 기록하며, 유사강간죄 성립 여부는 해당 구성요건의 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.2_15` / `Ⅳ.2`: “이와 다른 형태의 행위, 구강성교나 항문성교 등은 ‘간음’이라고 할 수 없고 이러한 경우에 는 유사강간죄가 성립할 수 있다.”

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

## 27. `art297_sec4_2.rape_and_penetration`

- proposition: 강간은 폭행·협박으로 상대방 반항을 불가능하거나 현저히 곤란하게 하여 간음하는 것이며, 간음은 다수설상 남성 성기의 여성 성기에 삽입 또는 양 성기의 결합을 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박의 요구 정도와 간음의 범위에 관한 다수설 및 대법원 기준을 별도 확인해야 하며, 사실관계 포섭에는 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.2_15` / `Ⅳ.2`: “강간이란 폭행·협박에 의하여 상대방의 반항을 불가능하게 하거나 현저히 곤란 하게 하여 그 사람을 간음하는 것을 말한다.”
  - `comm_001692_제297조_Ⅳ.2_15` / `Ⅳ.2`: “남성 성기의 여성 성기에 삽입 내지 남성의 성기와 여성의 성기의 결합을 말한다는 것이 다수설이다.”

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

## 28. `art297_sec4_2.violence_intercourse_causation`

- proposition: 강간죄에서는 폭행·협박과 간음 사이에 인과관계가 있어야 하며, 시간적 간격이 있어도 폭행·협박에 의해 간음이 이루어진 것으로 인정되면 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시간적 간격만으로 인과관계를 부정하지 않으며, 폭행·협박이 간음에 영향을 미쳤는지는 개별 사실관계에서 평가해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.2_15` / `Ⅳ.2`: “폭행·협박을 이용하여 상대방의 반항을 불가능하게 하거나 현저히 곤란 하게 하여 간음하는 것을 의미하므로, 폭행·협박과 간음 사이에는 인과관계가 존재하여야 한다.”
  - `comm_001692_제297조_Ⅳ.2_15` / `Ⅳ.2`: “폭행·협박과 간음 사이에 어느 정도 시간적 간격이 있더라도, 폭행·협박에 의하 여 간음이 이루어진 것으로 인정될 수 있는 한 본죄가 성립한다.”

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

## 29. `art297_sec4_3.attempt_commencement`

- proposition: 강간 수단으로 피해자 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박이 개시되면 실행의 착수가 인정되며, 속옷을 벗기거나 간음에 나아갈 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박이 반항을 불가능하거나 현저히 곤란하게 할 정도인지의 적용에는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.3_16` / `Ⅳ.3`: “강간의 수단으로 서 피해자의 반항을 불가능하게 하거나 현저히 곤란하게 할 정도의 폭행·협박 이 개시된 때에 실행의 착수가 있다고 보아야 하고 사람의 속옷을 벗기거나 간 음에 나아가야 하는 것은 아니다.”

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

## 30. `art297_sec4_3.attempt_commencement_context`

- proposition: 강간죄 실행의 착수에 필요한 폭행·협박 정도는 행위자의 언행·행동 및 당시 주변 정황을 종합하여 개별 사안마다 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 실행의 착수 판단은 행위자의 언행·행동과 주변 정황을 종합하는 개별적 평가를 요구한다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.3_16` / `Ⅳ.3`: “구체적으로 어느 정도의 폭행·협박이 있어야 실행의 착수로 인정할 수 있을 것인지는 일률적으로 말하기 어렵고, 개별적인 사안마다 행위자의 언행이나 행동, 당시의 주변 정황 등을 종합하여 판단할 수밖에 없다.”

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
