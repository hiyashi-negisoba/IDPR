# 범인은닉·도피 RuleIR 카드 검수 1

- unit: `harboring_offender`
- articles: art151
- cards: 1–15 / 58
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art151.abstract_danger_offense`

- proposition: 범인은닉·도피죄는 국가의 형사사법작용을 방해하는 추상적 위험범이므로, 국가의 형사사법작용 방해 결과가 현실적으로 발생할 필요 없이 그 위험이 있으면 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현실적 방해 결과의 발생이 아니라 국가의 형사사법작용 방해 위험의 존재가 문제되는 추상적 위험범이라는 설명이다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.1_1` / `Ⅱ.1`: “추상적 위험범이 다. 따라서 범죄의 성립을 위해 국가의 형사사법작용을 방해하는 결과가 현실 적으로 발생할 것을 필요로 하지 않고, 그 위험이 있으면 충분하다.”

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

## 2. `art151.continuing_offense_completion`

- proposition: 범인은닉·도피죄는 은닉 또는 도피하게 하는 행위로 기수에 이르며, 그 행위가 계속되는 동안 범죄가 종료되지 않는 계속범이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 은닉 또는 도피하게 하는 행위에 따른 기수 시점 및 계속 중인 행위에 따른 범죄 종료 여부를 설명하는 카드다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.1_1` / `Ⅱ.1`: “본죄는 벌 금 이상의 형에 해당하는 죄를 저지른 사람을 은닉 또는 도피하게 함으로써 기수 에 이르지만, 은닉하는 행위 또는 도피하게 하는 행위가 계속되는 한 범죄가 종료 되지 않는 계속범이다.”

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

## 3. `art151_sec2_2.accomplice_defense_right`

- proposition: 공범이 다른 공범의 교사에 따라 자신의 범행 관련 사실관계에 관하여 허위진술·허위자료 제출을 한 경우, 방어권 행사의 범위를 벗어나지 않으면 다른 공범 도피 결과가 있어도 범인도피죄 및 범인도피교사죄가 성립하지 않을 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문과 방어권 범위 기준을 확인해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_3` / `Ⅱ.2`: “공범 중 1명의 행위가 다른 공범을 도피하게 하는 결과를 초래하 더라도 자신의 방어권 행사의 범위를 벗어나지 않는 한 범인도피죄의 구성요건 에 해당하지 않을 수 있음을 분명히 하였다.”

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

## 4. `art151_sec2_2.accomplice_other_accomplice`

- proposition: 공범 중 1명이 자신이 아닌 다른 공범을 은닉하거나 도피하게 한 경우 범인은닉죄가 성립할 수 있으나, 자기은닉 불처벌 취지와 공범관계를 고려하여 성립 여부를 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 다른 공범에 대한 행위와 실질적 자기방어의 경계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “범인이 자기 자신을 은닉 또는 도피하게 하는 행위에 한하여 구성요건 해당 나) 성이 부정되므로, 공범 중 1명이 자기 자신이 아니라 다른 공범을 은닉 또는 도 피하게 한 때에는 본죄가 성립할 수 있다.”

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

## 5. `art151_sec2_2.accomplice_substantively_self_defense`

- proposition: 공범의 행위가 외형상 다른 공범을 은닉·도피시키는 결과를 내더라도 본질적으로 자기 은닉·도피와 다르지 않다고 평가되면 구성요건 해당성이 부정된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 본질적으로 자기은닉·도피와 같은지에 관한 평가 기준이 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_2` / `Ⅱ.2`: “그 행위가 본질적으로 범인의 자 기 은닉 또는 도피와 다르지 않다고 평가되는 경우에는 구성요건 해당성이 부정 되어 본죄가 성립하지 않는다고 할 것이다.”

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

## 6. `art151_sec2_2.attorney_false_statements`

- proposition: 변호인의 의뢰인 이익 대변은 법적으로 보호할 가치가 있는 정당한 이익에 한정되며, 변론행위 명목으로 수사기관이나 법원에 적극적 허위진술을 하거나 의뢰인에게 허위진술을 하게 하는 것은 허용되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 적극적 허위진술 여부와 정당한 조력의 한계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_11` / `Ⅱ.2`: “변호인이 의뢰인의 요청 에 따른 변론행위라는 명목으로 수사기관이나 법원에 대하여 적극적으로 허위 의 진술을 하거나 피고인 또는 피의자로 하여금 허위진술을 하도록 하는 것까 지 허용되지는 않는다.”

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

## 7. `art151_sec2_2.attorney_rights_advice`

- proposition: 변호사가 증언거부권자에게 증언거부를, 피의자·피고인에게 진술거부를 권유하는 것은 허용된 권리 행사를 권유하는 통상적 조력의 범위로서 범인도피죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 허용된 권리 행사의 권유인지 여부에 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “변호사가 증언거부권자 에게 증언을 거부하도록 하거나 피의자 또는 피고인으로 하여금 진술을 거부하 도록 권유하더라도 이는 소송관계인에게 허용된 권리를 행사하도록 권유한 것 에 불과하여 통상적인 조력의 범위를 벗어났다고 보기 어려우므로 범인도피죄 가 성립하지 않는다고 봄이 옳다.”

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

## 8. `art151_sec2_2.backdated_agreement_no_risk`

- proposition: 횡령 피의사실을 적극 부인하기 위한 보강자료로 작성일자를 소급한 약정서만으로는 수사기관을 착오에 빠뜨려 실제 범인을 도피시킬 위험이 있는 행위라고 보기 어렵다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소급 약정서만 있는 구체적 보고 판례로 한정한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_18` / `Ⅱ.2`: “피고인의 이러한 행위만으로는 객관적인 제반 증거를 수 집·조사하여 피의사실을 증명하여야 할 의무를 부담하는 수사기관을 기만하여 착오 에 빠지게 하였다고 볼 수는 없으므로 실제로 범인을 도피시킬 위험이 있는 행위에 해당한다고 할 수 없고”

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

## 9. `art151_sec2_2.complaint_possible`

- proposition: 친고죄의 고소가 아직 제기되지 않았더라도 고소기간이 지나지 않아 소추 또는 처벌 가능성이 남아 있으면 그 범인은 범인은닉죄의 객체에 포함된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 장래의 고소·소추 가능성 판단을 사실관계에 적용해야 한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_4` / `Ⅱ.2`: “친고죄를 저지른 범 인을 은닉하거나 도피하게 하였을 당시 그 친고죄에 대한 고소가 아직 제기되 지 않았다고 하더라도 고소기간이 경과하지 않아 형사 소추 또는 처벌의 가능 성이 남아 있었던 때에는 그 범인은 본죄의 객체에 포함된다.”

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

## 10. `art151_sec2_2.concealment_place`

- proposition: 은닉은 관계 공무원의 범인 발견·체포를 불가능하거나 곤란하게 할 목적으로 범인에게 장소를 제공하여 숨겨주는 것이며, 장소 제공 후 별도 행위는 요구되지 않고 그 장소에는 부동산뿐 아니라 자동차와 같은 동산도 포함될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 장소 제공형 은닉의 범위를 정리한다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_8` / `Ⅱ.2`: “범인에게 장소를 제공하는 방법으로 범인을 숨겨주는 것을 말한다. 범인에게 장소를 제공하였으면 이로써 충분하 고, 장소를 제공한 후 일정 기간 동안 수사기관에 출석하지 말라고 권유하는 말 을 하는 등 별도의 행위를 할 것이 요구되지는 않는다.”
  - `comm_001692_제151조_Ⅱ.2_8` / `Ⅱ.2`: “이때의 장소에는 건물 과 같은 부동산은 물론이고 자동차와 같은 동산도 포함될 수 있다.”

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

## 11. `art151_sec2_2.conditional_intent`

- proposition: 범인은닉죄의 고의는 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 미필적 고의 해당 여부는 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_21` / `Ⅱ.2`: “본죄의 고의는 미필적 고의로도 충분하다.”

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

## 12. `art151_sec2_2.direct_escape_assistance_assessment`

- proposition: 어떤 행위가 직접 범인을 도피시키거나 도피를 직접적으로 용이하게 하는지 판단할 때에는 행위의 외형뿐 아니라 피고인의 범인 처지·의도에 대한 인식 및 은닉·도피 의사를 함께 고려해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 외형과 주관적 인식·의사를 함께 평가하는 보고된 판례 기준이다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_10` / `Ⅱ.2`: “피고인이 범인의 처지나 의도에 대하여 인식하고 있 었는지, 그에게 범인을 은닉 내지 도피시키려는 의사가 있었는지를 함께 고려하 여 살펴보아야 한다. 단순히 피고인이 한 행위의 밖으로 드러난 태양만 살펴보 는 것만으로는 부족하다.”

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

## 13. `art151_sec2_2.escape_assistance_definition`

- proposition: 도피하게 하는 행위는 은닉 외의 방법으로 범인에 대한 수사·재판·형 집행 등 형사사법작용을 곤란하거나 불가능하게 하는 모든 행위이고, 장소적 관련성이 없다는 점에서 은닉과 구별된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 은닉과 구별되는 도피조력의 일반적 정의다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “은닉 이외의 방법으로 범인에 대한 수사, 재판 및 형의 집행 등 형사사법의 작용을 곤란 또는 불가능하게 하는 일체의 행위를 말하는 것으로서 그 수단과 방법에 어떠한 제한이 없다. 장소적 관련성이 없다는 점에서 은닉과 다르다.”

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

## 14. `art151_sec2_2.escape_directness`

- proposition: 범인도피죄는 현실적 형사사법 방해 결과가 필요 없는 위험범이지만, 도피하게 하는 행위는 은닉에 비견할 정도로 수사기관의 발견·체포를 곤란하게 하는 직접 도피행위 또는 도피를 직접 용이하게 하는 행위에 한정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직접성 및 발견·체포 곤란성은 평가가 필요하다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_9` / `Ⅱ.2`: “범인도피죄는 위험범 으로서 현실적으로 형사사법의 작용을 방해하는 결과를 초래할 필요는 없으나, 적어도 함께 규정되어 있는 은닉행위에 비견될 정도로 수사기관의 발견·체포를 곤란하게 하는 행위, 즉 직접 범인을 도피시키는 행위 또는 도피를 직접적으로 용이하게 하는 행위에 한정된다.”

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

## 15. `art151_sec2_2.false_confession_not_concealment`

- proposition: 다른 사람의 허위 고소에 맞추어 자신이 수표를 위조했다는 취지로 허위 자백한 행위가 고소인에 대한 범죄 입증을 곤란하게 할 뿐 범죄 주체에 관한 혼돈으로 범인 발견을 곤란하게 하지 않는 경우, 은닉행위에 비견될 정도의 직접적 도피행위가 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 범죄 입증 곤란과 범인 발견 곤란을 구별하는 제한된 보고 판례다.
- bounded sources:

  - `comm_001692_제151조_Ⅱ.2_17` / `Ⅱ.2`: “수사기관의 甲에 대한 부정수표단속법위반의 점 등에 대한 입증을 곤란하게 하는 것일 뿐 그로 인하여 범죄의 주체가 누구인지에 관하여 혼돈을 초래함으로써 범인의 발견을 곤란하게 하는 것이라고 할 수는 없으므로”

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
