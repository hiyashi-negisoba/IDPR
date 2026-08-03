# 주거침입·퇴거불응 RuleIR 카드 검수 5

- unit: `dwelling_intrusion`
- articles: art319
- cards: 61–75 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 61. `art319_sec3_2.completion_minimal_partial_entry_attempt`

- proposition: 신체의 극히 일부분이 주거 안에 들어갔더라도 사실상 주거의 평온을 해하는 정도에 이르지 않으면 주거침입죄는 미수에 그친다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판시의 원문과 신체 일부 출입의 정도를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_42` / `Ⅲ.2`: “신체의 극히 일부분이 주거 안으로 들어갔지만 사실상 주거의 평온을 해하는 정도에 이르지 아니하였다면 미수에 그친다고 판시하였다.”

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

## 62. `art319_sec3_2.continuing_offense`

- proposition: 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이며, 침입행위는 퇴거하거나 새 체류승낙이 있을 때까지 계속된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 퇴거와 새 체류승낙은 계속 상태의 종료를 구분하는 열거 가능한 사건으로 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “사실상 주거의 평온”
  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “에 대한 침해가 계속되는 동안 주거침입죄가 계속 성립한다. 침입행위는 퇴거하”
  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “든가 새로이 체류의 승낙이 있을 때까지 계속된다.”

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

## 63. `art319_sec3_2.no_refusal_to_leave_after_trespass`

- proposition: 무단침입이 완성된 뒤 퇴거요구에 불응하여도, 적법하게 주거에 들어간 경우를 전제로 하는 퇴거불응죄는 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 이 예외는 무단침입이 완성된 후의 퇴거요구 불응에 한정된다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “침입이 완성된 이상 그 후 퇴거시키더라도 주거침입죄 이외에 적법하게 주거에 들어간 경우를 전제로 하는 퇴거불응죄는 성립하지 않는다. 즉 기수 이후에 퇴거요구에 불응한 경우에도 별도로 퇴거불응죄가 성립하지 않는다.”

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

## 64. `art319_sec3_2.post_conviction_continued_occupation`

- proposition: 무단침입으로 유죄판결을 받은 사람이 판결 확정 후에도 퇴거하지 않고 해당 주택에 계속 거주한 경우, 확정 이후 행위는 별도의 주거침입죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례의 원문 및 유죄판결 확정 이후 행위의 범위를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “그 판결이 확정된 후에도 퇴거하지 않은 채 계속하여 당해 주택에 거주”
  - `comm_001692_제319조_Ⅲ.2_43` / `Ⅲ.2`: “한 경우에는, 그 판결 확정 이후의 행위는 별도의 주거침입죄를 구성한다고 한”

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

## 65. `art319_sec4.intent_against_resident_will`

- proposition: 통설에 따르면 주거침입죄의 고의에는 거주자·관리자·점유자의 의사 또는 추정적 의사에 반하여 타인의 주거 등에 들어간다는 인식과 의사가 필요하며, 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 통설로 소개된 고의 요건이다. 개별 사실관계에서 인식과 의사의 존재는 평가가 필요하므로 standard input으로 유지한다.
- bounded sources:

  - `comm_001692_제319조_Ⅳ_44` / `Ⅳ`: “통설은 주거침입죄의 고의는 거주자, 관리자, 점유자의 의사 내지 추정적 의”
  - `comm_001692_제319조_Ⅳ_44` / `Ⅳ`: “사에 반하여 타인의 주거 등에 들어가는 점에 대한 인식과 의사가 있어야 하고 미필적 고의로도 충분하다고 한다.”

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

## 66. `art319_sec4.intent_factual_peace_entry`

- proposition: 전원합의체 판결 취지에 따르면 주거침입의 고의는 사실상 평온을 해치는 행위태양으로 타인의 주거에 들어간다는 점을 인식하고 용인하는 것이며, 고의 여부는 주거 등의 형태·용도·성질, 외부인 출입의 통제·관리 방식과 상태, 행위자의 출입 경위와 방법 등을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 전원합의체 판결로 보고된 기준이므로, 적용 전 사용자 제공 1차 판례 색인에서 해당 판결의 원문과 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅳ_44` / `Ⅳ`: “주거침입의 고의는 사실상 평온을 해치는 행위태양으로 타인의 주거에 들어간다는 점을 인식하고 용인하는 것이라고 볼 수 있고, 침입”
  - `comm_001692_제319조_Ⅳ_44` / `Ⅳ`: “의 고의가 있었는지 여부는 출입하려는 주거 등의 형태와 용도·성질, 외부인에 대한 출입의 통제·관리방식과 상태, 행위자의 출입 경위와 방법 등을 종합적으”
  - `comm_001692_제319조_Ⅳ_44` / `Ⅳ`: “로 고려하여 판단하여야 할 것이다.”

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

## 67. `art319_sec5_2.labor_dispute_exclusive_occupation`

- proposition: 사업장 시설을 전면적·배타적으로 점거하여 조합원 외 출입을 저지하거나 사용자 관리지배를 배제해 업무 중단·혼란을 야기하는 행위는 정당한 쟁의행위 한계를 벗어나 위법성조각 없이 건조물침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 점거의 전면성·배타성, 관리지배 배제 및 업무상 영향에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “직장 또는 사업장시설을 전면적·배타적으로 점거하여 조합원 이외의 자의 출입을 저지하거나, 사용자 측의 관리지배를 배제”
  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “하여 업무의 중단 또는 혼란을 야기하게 하는 것과 같은 행위는 정당성의 한계”
  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “를 벗어난 것이라고 볼 수밖에 없고”

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

## 68. `art319_sec5_2.labor_dispute_explicit_denial_entry`

- proposition: 대회 개최를 위한 장소사용 허가를 명시적으로 불허받았음에도 대회 개최를 위해 대학에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명시적 불허통보의 내용, 상대방 및 출입 목적을 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_49` / `Ⅴ.2`: “특정 대학교 총장에게 전국노동자대회 등 (4) 개최를 위한 장소사용 허가를 요청하였다가 명시적으로 불허통보를 받았음에도 대회 개최를 위하여 각 대학교에 들어간 경우”

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

## 69. `art319_sec5_2.labor_dispute_incidental_act`

- proposition: 적법하게 개시된 쟁의행위의 목적을 공지·준비하기 위한 부수행위가 관행적 방식에 편승하여 이루어졌고 전체적으로 수단·방법의 적정성을 벗어나지 않으면 형법상 정당행위에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 쟁의행위의 적법한 개시, 부수행위성 및 수단·방법의 적정성을 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_49` / `Ⅴ.2`: “주체와 목적의 정당성이 인정되고 절차적 요건을 갖추어 적법하게 개시된 쟁의행위의 목적을 공지하고 이를 ‘준비하기 위한 부수적 행위이자 그와 관련한 절차적 요건의 준수 없이 관행적으로 실시되던 방식에 편승하여 이루어진 행위’ 로서 전체적으로 수단과 방법의 적정성을 벗어난 것으로 보이지 않는 경우”

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

## 70. `art319_sec5_2.labor_dispute_plant_occupation`

- proposition: 회사의 시설관리권을 배제한 전면 점거파업이 구조조정 저지를 목적으로 하여 정당한 쟁의행위로 볼 수 없고, 퇴거요구를 알면서도 공장에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 전면 점거, 시설관리권 배제, 점거 목적 및 퇴거요구 인식의 사실관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_49` / `Ⅴ.2`: “평택공장을 전면적으로 점 거하여 회사 측의 시설관리권을 배제한 채 점거파업이 진행되었고, 그 점거의 목적이 회사의 구조조정 추진을 저지하는 데 있어 정당한 쟁의행위로 볼 수 없 는 경우”

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

## 71. `art319_sec5_2.lawful_authority_entry`

- proposition: 적법한 권한에 따라 주거에 들어가는 행위는 공법상 또는 사법상 권한인지와 관계없이 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 권한의 적법성과 해당 출입의 범위가 사실관계상 확인되어야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_46` / `Ⅴ.2`: “적법한 권한에 의하여 주거에 들어가는 것은 위법하다고 할 수 없다. 그것이 공법상의 권한이든 사법상의 권한이든 묻지 않는다.”

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

## 72. `art319_sec5_2.lawful_labor_dispute_entry`

- proposition: 노동조합법상 쟁의행위를 위해 승낙 없이 사업장에 들어가더라도 권리남용에 해당하지 않으면 건조물침입죄가 성립하지 않지만, 쟁의행위 자체가 위법하면 위법성조각의 여지가 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 쟁의행위의 적법성 및 권리남용 여부를 구체적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “노동조합법상의 쟁의행위를 위해 승낙을 받지 않고 사업장에 들어가는 것은 그”
  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “것이 권리남용에 해당되지 않으면 건조물침입죄가 성립하지 않는다. 하지만 쟁의행위 자체가 위법하게 되면 위법성조각의 여지가 없다.”

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

## 73. `art319_sec5_2.right_holder_entry_without_procedure`

- proposition: 권리자가 자신의 권리를 실행하기 위한 경우라도 법정절차에 따르지 않고 주거에 침입하면 주거침입죄가 성립한다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 판례 입장은 사용 전 사용자 제공 1차 판례 색인으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_48` / `Ⅴ.2`: “판례는 권리자가 자신의 권리를 실행하기 위한 것일지라도 법정절차에 의하지 않고 주거에 침입하면 주거침입죄가 성립한다고 한다.”

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

## 74. `art319_sec5_2.socially_acceptable_entry`

- proposition: 사회상규에 반하지 않는 주거침입은 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사회상규 위반 여부에는 구체적 사정에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_46` / `Ⅴ.2`: “사회상규에 반하지 않는 주거침입은 위법하다고 할 수 없다.”

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

## 75. `art319_sec5_2.water_tank_repair_entry`

- proposition: 물탱크·수도관 밸브의 점검 또는 수리를 위해 반드시 건물의 거실과 부엌을 통과해야 하고 주거 평온을 심하게 침해하지 않는 경우, 특별한 사정이 없으면 해당 출입은 허용되어 사회상규에 위배되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 출입의 필요성, 주거 평온 침해 정도 및 특별한 사정을 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅴ.2_47` / `Ⅴ.2`: “그 물탱크 등의 이상 유무의 확인이나 고장의 수리를 위한 이 사건 건물”
  - `comm_001692_제319조_Ⅴ.2_47` / `Ⅴ.2`: “의 2층 거실과 부엌의 출입은 그로 인하여 주거의 평온을 심하게 침해하는 것이 아”
  - `comm_001692_제319조_Ⅴ.2_47` / `Ⅴ.2`: “닌 경우에는 특별한 사정이 없으면 허용되어야 한다고 보는 것이 타당하다”

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
