# 강제추행 RuleIR 카드 검수 3

- unit: `indecent_assault`
- articles: art298
- cards: 31–33 / 33
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #26 `art298_sec3_2.indecent_act_scope`: `art298_sec3_2.indecent_act_no_body_part_distinction` (status=`valid`)

## 31. `art298_sec8.forcible_indecency_followed_by_rape`

- proposition: 동일 피해자에 대해 강제로 추행한 뒤 이어 강간한 경우에는 포괄하여 강간죄만 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일 피해자에 대한 선행 강제추행과 이어진 강간의 포괄관계를 다룬다.
- bounded sources:

  - `comm_001692_제298조_Ⅷ_19` / `Ⅷ`: “동일한 피해자에 대하여 강제로 추행하고 이어 강간까지 한 경우에는 포괄하여 강간죄만 성립한다.”

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

## 32. `art298_sec8.special_forcible_indecency`

- proposition: 흉기 기타 위험한 물건을 지니거나 2인 이상이 합동하여 강제추행한 경우에는 강제추행죄가 아니라 특수강제추행죄가 성립하여 가중처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위험한 물건 휴대 또는 2인 이상 합동이라는 조건이 충족된 경우의 죄명 전환 및 가중처벌 관계를 다룬다.
- bounded sources:

  - `comm_001692_제298조_Ⅷ_19` / `Ⅷ`: “‘흉기 그 밖의 위험한 물건을 지니거나 2인 이상이 합동하여’ 강제추행한 경우에 는 본죄가 아니라 [후론 1]에서 살펴볼 성폭력범죄의 처벌 등에 관한 특례법 제4 조 제1항의 특수강제추행죄가 성립하여 가중처벌된다.”

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

## 33. `art298_sec3_2.indecent_act_no_body_part_distinction`

- proposition: 추행 평가는 행위 당시 당사자의 의사·감정·주위사정을 고려하므로 신체 부위에 본질적 차이를 두지 않고, 은밀한 부위가 아니어도 상황에 따라 강제추행죄가 될 수 있다는 견해가 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 신체 부위가 아닌 당사자 의사·감정 및 주위사정을 중시하는 견해의 채택 여부를 검토해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_8` / `Ⅲ.2`: “추행으로 평가하기 위해서는 추행이 행해진 때 의 당사자의 의사, 감정 또는 주위사정이 감안되어야 하므로 신체 부위에 따라 본질적인 차이를 두지 않는 것이 바람직하고 반드시 신체의 은밀한 부분이 아 니더라도 상황에 따라 본죄에 해당할 수 있다는 견해도 있다.”

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
