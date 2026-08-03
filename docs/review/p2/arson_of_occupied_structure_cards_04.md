# 현주건조물등방화 RuleIR 카드 검수 4

- unit: `arson_of_occupied_structure`
- articles: art164
- cards: 46–47 / 47
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

## 46. `art164_sec3_6.parricide_fire_death_concurrence`

- proposition: 존속 사망의 경우 존속살인죄와 현주건조물방화치사죄는 상상적 경합 관계라는 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
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
