# 현주건조물등방화 RuleIR 카드 검수 4

- unit: `arson_of_occupied_structure`
- articles: art164
- cards: 46–52 / 52
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #2 `art164_sec2_1.post_killing_arson`: `art164_sec2_1.post_killing_arson_precedent` (status=`valid`)
- #3 `art164_sec2_1.completion`: `art164_sec2_1.completion_independent_combustion_variant` (status=`valid`)
- #4 `art164_sec3_2.attempted_basic_arson_subject`: `art164_sec3_2.attempted_basic_arson_included` (status=`valid`)
- #5 `art164_sec3_6.intentional_fire_death_murder_concurrence`: `art164_sec3_6.intentional_fire_death_murder_concurrence_affirmative` (status=`valid`)
- #15 `art250_sec2_10.arson_death_parricide_concurrence`: `art250_sec2_10.arson_death_parricide_specialty_precedent` (status=`valid`)

## 46. `art164_sec3_6.parricide_fire_death_concurrence`

- proposition: 존속 사망의 경우 존속살인죄와 현주건조물방화치사죄는 상상적 경합 관계라는 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 입장에 의존하므로, 적용 전 해당 판례의 원문과 사실관계를 사용자 제공 1차 판례 인덱스에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.6_23` / `Ⅲ.6`: “존속 사망의 경우에는 존속살인죄와 현주건조물방화치사죄의 상상적 경합 범이 된다는 입장이다.”

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

## 47. `art164_sec3_6.robbery_murder_fire_death_concurrence`

- proposition: 재물을 강취한 뒤 피해자를 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우, 강도살인죄와 현주건조물방화치사죄는 상상적 경합 관계.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 보고한 구체적 판례 결론이므로, 적용 전 판례 원문에서 강취ㆍ살해 목적ㆍ방화ㆍ사망의 사실관계와 판시 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.6_23` / `Ⅲ.6`: “피고인들의 위 행위는 강도살인죄와 현주건조물방화 치사죄에 모두 해당하고 그 두 죄는 상상적 경합범관계에 있다.”

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

## 48. `art164_sec2_1.post_killing_arson_precedent`

- proposition: 거주자 전원을 살해한 직후 그 가옥에 방화한 경우에도 해당 가옥은 주거용 건조물로 보아 현주건조물등방화죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 보고된 판례의 원문을 사용자 제공 1차 판례 색인으로 확인한 뒤 정책 선택이 필요하다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “범인이 거주자 전원을 살해하고 곧바로 그 가옥에 방화한 경우에 당해 가옥은 사람”
  - `comm_001692_제164조_Ⅱ.1_3` / `Ⅱ.1`: “이 주거로 사용하는 건조물에 해당하므로 현주건조물등방화죄가 성립한다.”

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

## 49. `art164_sec2_1.completion_independent_combustion_variant`

- proposition: 목적물에 불이 옮겨 붙어 독립적으로 계속 탈 수 있는 상태가 되면 방화죄의 기수가 된다는 독립연소설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 기수 시기 선택이 필요한 경쟁 학설이다.
- bounded sources:

  - `comm_001692_제164조_Ⅱ.1_7` / `Ⅱ.1`: “불이 매개물을 떠나 목적물에 옮겨 붙어 독립하여 계속 탈 수 있는 상태가 되면 소훼가 되어 방화죄의 기수가 된다고 보는 견해이다.”

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

## 50. `art164_sec3_2.attempted_basic_arson_included`

- proposition: 현주건조물등방화치사상죄의 주체인 제164조 제1항의 죄를 지은 사람에는 미수범도 포함된다는 긍정설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 제164조 제1항의 미수범을 치사상죄의 주체에 포함하는 견해로서, 반대 견해 및 관련 조문 해석을 검토해야 한다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.2_19` / `Ⅲ.2`: “긍정설은 제 174조에서 제164조 제1항의 미수범을 처벌하고 있고, 제164조의 미수행위로 인하 여도 치사상의 결과가 발생할 수 있다는 것을”

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

## 51. `art164_sec3_6.intentional_fire_death_murder_concurrence_affirmative`

- proposition: 거주자를 살해할 고의로 방화하여 사망을 초래한 경우, 방화치사죄의 불법에 살인의 고의범이 포함되지 않는다는 이유로 살인죄와 현주건조물방화치사죄의 상상적 경합을 인정하는 긍정설이 있다.
- current metadata: formalization=`context_only`, polarity=`positive`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 긍정설로 보고된 견해이며, 부정설 및 관련 판례의 원문 확인 전에는 채택하지 않는다.
- bounded sources:

  - `comm_001692_제164조_Ⅲ.6_23` / `Ⅲ.6`: “긍정 설은 방화치사죄의 불법에 살인의 고의범이 포함되는 것은 아니므로 별도의 고의범이 성립한다는 사실을 명확히 하기 위해서라도 살인좌와 현주건조물방화 치사죄의 상상적 경합범이 된다는 견해”

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

## 52. `art250_sec2_10.arson_death_parricide_specialty_precedent`

- proposition: 서울고등법원 2010노252 판결은 존속살해죄 법정형이 현주건조물방화치사죄보다 중하지 않으므로 현주건조물방화치사죄만 성립하고 존속살해죄는 별도로 죄를 구성하지 않는다고 보았다.
- current metadata: formalization=`context_only`, polarity=`negative`, doctrinal_status=`disputed`, review_required=`True`
- source track: `doctrine_overlay`
- prior note: 학설상 상상적 경합 견해와 충돌하는 commentary-reported precedent position이다. 판결 원문과 개정 형법 적용 여부를 사용자 제공 1차 판례 색인에서 확인한 뒤 정책을 선택해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅱ.10_141` / `Ⅱ.10`: “울고등법원 2010. 6. 3. 선고 2010노252 판결은, 존속살해죄의 법정형이 현”
  - `comm_001692_제250조_Ⅱ.10_141` / `Ⅱ.10`: “주건조물방화치사죄의 법정형과 같을 뿐 그보다 중하지 않으므로 현주건조물방 화치사죄만 성립하고 이와 법조경합 관계에 있는 존속살해죄에 대하여는 별도 로 죄를 구성하지 않는다고 보았다.”

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
