# 친족상도례 준용 RuleIR 카드 검수 1

- unit: `relative_property_crime_exception`
- articles: art344
- cards: 1–5 / 5
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art344_x_raw_pdf.article328_theft_offenses_scope`

- proposition: 형법 제328조의 친족상도례 규정은 절도·야간주거침입절도·특수절도·자동차등불법사용 및 상습범과 그 미수범에 한하여 준용된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 준용 대상 범죄와 미수범의 범위를 열거하는 카드다.
- bounded sources:

  - `raw_001692_제344조_p001` / `raw_pdf.page_1`: “형의 절도죄(절도·야간주거침입절도·특수절도·자동차등불법사용   및 상습범)와 그  미          
           수범에 한하여  준용될 뿐”

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

## 2. `art344_x_raw_pdf.kinship_only_one_holder_no_application`

- proposition: 범인이 목적물의 소유자 또는 점유자 중 어느 일방과만 친족관계에 있는 경우에는 절도죄에 형법 제328조가 적용되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 소유자 또는 점유자 일방과의 친족관계만 존재하는 실제 부정 요건을 명시한다.
- bounded sources:

  - `raw_001692_제344조_p001` / `raw_pdf.page_1`: “범인이 목적물의  소유자나           
           점유자의  어느 일방과  사이에서만  친족관계가  있는  경우에는  형법 제328조가          
           적용되지  않는다.”

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

## 3. `art344_x_raw_pdf.kinship_with_owner_and_possessor`

- proposition: 절도죄에서 형법 제328조가 적용되려면 범인과 목적물의 소유자 및 점유자 모두 사이에 친족관계가 있어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 소유자와 점유자가 모두 있는 경우의 친족관계 요건으로 검토한다.
- bounded sources:

  - `raw_001692_제344조_p001` / `raw_pdf.page_1`: “모두 사이에 친족관계가  있는  경우이어야”

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

## 4. `art344_x_raw_pdf.reported_kinship_classifications`

- proposition: 주석은 범인이 피해자의 부의 외사촌 동생인 경우, 피해자가 범인의 친할머니의 동생인 경우 및 피해자와 외사촌남매간인 경우에 관한 판례를 소개한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인용문이 문장 중간에서 끝나므로, 소개된 판례의 정확한 결론과 추가 친족관계 유형은 원문 및 primary precedent index로 확인해야 한다.
- bounded sources:

  - `raw_001692_제344조_p001` / `raw_pdf.page_1`: “범인이 피해자의  부의 외사촌 동생(즉 피해자가 범인의  고종사촌 형수)인          
                                                                    
           경우 및 피해자가  범인의 친할머니의  동생이라든지   피해자와  외사촌남매간이라”

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

## 5. `art344_x_raw_pdf.robbery_no_family_benefit`

- proposition: 각종 강도죄 및 그 미수범에는 범인과 피해자 사이에 가까운 친족관계가 있더라도 형법 제328조에 따른 형면제 또는 친고죄 등의 혜택이 적용되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강도죄 및 그 미수범에 대한 친족상도례 배제 예외를 별도로 보존한다.
- bounded sources:

  - `raw_001692_제344조_p001` / `raw_pdf.page_1`: “강도죄에는  준용되지  않는다. 다시 말하면  각종 강도           
           죄와 그 미수범에  관하여는  범인과  피해자 사이에  아무리  가까운 친족관계가            
                                                                    
           있다 하더라도  형법 제328조에 의한 형면제 또는 친고죄  등의 혜택이  주어지지”

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
