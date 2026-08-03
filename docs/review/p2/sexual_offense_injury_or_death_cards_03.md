# 강간등상해·치상 RuleIR 카드 검수 3

- unit: `sexual_offense_injury_or_death`
- articles: art301
- cards: 31–34 / 34
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #28 `art301_sec4_6.pregnancy_injury`: `art301_sec4_6.unwanted_pregnancy_not_injury_holding` (status=`valid`)
- #29 `art301_sec7.special_rape_attempt_result`: `art301_sec7.special_rape_injury_completed` (status=`valid`)

## 31. `art301_sec6.pre_execution_withdrawal`

- proposition: 강간 등을 공모한 공범이 다른 공범자의 실행착수 전, 즉 폭행·협박 전 공범관계에서 이탈한 경우 다른 공범자의 행위에 대해 공동정범 책임을 지지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 이탈 시점이 실행착수 전인지, 즉 폭행·협박 전인지에 한정된 예외로 검토한다.
- bounded sources:

  - `comm_001692_제301조_Ⅵ_19` / `Ⅵ`: “강간 등을 공모한 후 그 공범자 중 일부가 강간 등 범죄의 실행에 착수하기 전, 즉 폭행·협박을 가하기 전에 공범관계에서 이탈한 경우에는 다른 공범자의 행 위에 대하여 공동정범으로서 책임을 지지 않는다.”

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

## 32. `art301_sec7.no_general_attempt_punishment`

- proposition: 형법상 강간 등 상해·치상죄에는 미수범 처벌규정이 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 형법상 강간 등 상해·치상죄에 관한 미수범 처벌규정 부재를 명시한 예외 카드다.
- bounded sources:

  - `comm_001692_제301조_Ⅶ_20` / `Ⅶ`: “형법상 강간 등 상해·치상죄에 대하여는 미수범 처벌규정이 없다.”

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

## 33. `art301_sec4_6.unwanted_pregnancy_not_injury_holding`

- proposition: 대법원은 원하지 않는 임신 그 자체를 상해로 보기 어렵다고 판단한 원심을 수긍하였다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 댓글에 보고된 좁은 판례 입장이다. 원하지 않는 임신 그 자체라는 범위를 넘겨 일반화하지 말고, 사용자 제공 1차 판례 인덱스에서 원문을 확인한 뒤 정책 선택을 검토해야 한다.
- bounded sources:

  - `comm_001692_제301조_Ⅳ.6_14` / `Ⅳ.6`: “원 하지 않는 임신 그 자체를 상해라고 보기는 어렵다고 판단한 원심을 수긍하였다.”

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

## 34. `art301_sec7.special_rape_injury_completed`

- proposition: 특수강간이 미수에 그쳤더라도 그로 인해 피해자가 상해를 입으면 특수강간치상죄의 기수범이 성립하고, 미수범 처벌규정은 상해 고의로 상해를 입히려다 미수에 그친 특수강간상해죄 등에 적용된다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 결과적 가중범 미수 인정 여부에 관한 견해와 긴장 관계에 있는 commentary-reported precedent 입장이다. 사용자 primary precedent index로 보고된 판례를 확인하기 전에는 선택하지 않는다.
- bounded sources:

  - `comm_001692_제301조_Ⅶ_21` / `Ⅶ`: “‘특수강간이 미수에 그쳤더라도 그로 인하여 피해자가 상해를 입었으면 특 수강간치상죄의 기수범이 성립하는 것이고, 미수범 처벌규정은 특수강간치상죄 와 함께 규정된 특수강간상해죄의 미수에 그친 경우”

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
