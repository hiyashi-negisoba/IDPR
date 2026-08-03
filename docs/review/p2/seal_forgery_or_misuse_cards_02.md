# 사인등위조·부정사용 RuleIR 카드 검수 2

- unit: `seal_forgery_or_misuse`
- articles: art239
- cards: 16–19 / 19
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art239_sec2.delivery_of_forged_seal_not_use`

- proposition: 위조된 인과 자체를 타인에게 교부한 것만으로는 위조사인행사죄가 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위조된 인과 자체의 단순 교부를 행사로 보지 않는 명시적 예외 카드이다.
- bounded sources:

  - `comm_001692_제239조_Ⅱ_6` / `Ⅱ`: “다만 위조된 인과 자체를 타인에게 교부한 것만으로 는 위조사인행사죄가 되지 아니한다.”

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

## 17. `art239_sec2.exposure_as_use`

- proposition: 위조된 인영은 일반인이 열람할 수 있는 상태에 두면, 위조된 인과는 날인하여 일반인이 열람할 수 있는 상태에 두면 행사가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 인영 및 인과의 행사 시점을 일반인이 열람할 수 있는 상태를 기준으로 정리한 카드이다.
- bounded sources:

  - `comm_001692_제239조_Ⅱ_6` / `Ⅱ`: “위조된 인영은 이를 일반인이 열람할 수 있는 상태에 두면, 위조된 인과는 날인하여 이를 일반인이 열람할 수 있는 상태에 두 면 그것으로 행사가 된다.”

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

## 18. `art239_sec2.signature_immediate_exposure_holding`

- proposition: 서명 직후 타인이 열람하게 된 경우에는 타인이 열람하기 전에 즉시 파기한 사정이 없는 한, 서명 기재와 동시에 사서명위조죄 및 위조사서명행사죄가 성립하며 이후 타인이 위조 사실을 알게 되어도 행사죄 성립에는 영향이 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 소개된 판례의 구체적 사실관계와 원문 판결의 확인이 필요하다.
- bounded sources:

  - `comm_001692_제239조_Ⅱ_6` / `Ⅱ`: “서명에 바로 이어서 타인이 열람하게 된 때에는 타인이 열람하기 전에 즉시 파기하였다는 사정이 없는 이상 서명의 기 재와 동시에 사서명위조죄와 함께 위조사서명행사죄가 성립하고, 그와 같이 위 조사서명행사죄가 성립된 직후에 타인이 그 서명의 위조사실을 알게 되었다고 하더라도 이미 성립한 위조사서명행사죄의 성립에 아무런 지장이 없다.”

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

## 19. `art239_sec2.use_of_forged_private_sign`

- proposition: 위조 또는 부정사용한 사인 등을 행사하면 위조·부정행사 사인 등 행사죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 위조 또는 부정사용한 사인 등의 행사와 범죄 성립의 연결을 정리한 카드이다.
- bounded sources:

  - `comm_001692_제239조_Ⅱ_6` / `Ⅱ`: “위조 또는 부정사용한 사인 등을 행사함으로써 성립하는 범죄이다.”

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
