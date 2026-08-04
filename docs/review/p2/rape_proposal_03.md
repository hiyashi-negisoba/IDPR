# 강간 RuleIR 제안 03 — 죄수·가중유형·외부 unit 연결

성립 후 죄수와 특별법 가중유형은 전부 `post_outcome`으로 보존한다. 해당 외부 unit이
없으면 `predicate_ir_missing`이고, 강간 기수 성립을 임의로 대체하지 않는다.

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 41 | `art297_sec7.continuous_acts_single_offense` | approve | post_outcome | offense_count / not_applicable | base | - | 동일 강제상태·단일계속 범의의 수회 간음은 포괄일죄 |
| 42 | `art297_sec7.multiple_victims_multiple_offenses` | approve | post_outcome | offense_count / not_applicable | base | - | 피해자별 성적 자기결정권 침해에 따른 수죄 |
| 43 | `art297_sec7.new_violence_separate_offense` | approve | post_outcome | offense_count / not_applicable | base | - | 강제상태 종료 뒤 새로운 폭행·협박이면 별죄 |
| 44 | `art297_sec9.abduction_for_marriage_rape` | approve | post_outcome | concurrence / not_applicable | base | `abduction_for_marriage` | 결혼목적 약취죄와 강간죄의 실체적 경합 |
| 45 | `art297_sec9.confinement_rape_attempted_case` | approve | post_outcome | concurrence / not_applicable | base | `confinement` | 동일 협박이 감금과 강간미수 착수에 해당하면 상상적 경합 |
| 46 | `art297_sec9.continued_confinement_after_rape` | approve | post_outcome | concurrence / not_applicable | base | `confinement` | 강간 종료 뒤 계속된 감금은 실체적 경합 |
| 47 | `art297_sec9.means_violence_absorption` | approve | post_outcome | concurrence / not_applicable | base | `assault_or_threat` | 강간 수단 폭행·협박은 강간죄에 흡수 |
| 49 | `art297_sec9.rape_injury_death` | approve | post_outcome | aggravated_result / not_applicable | base | `sexual_offense_injury_or_death` | 강간상해·치상·살인·치사의 결과가중 연결 |
| 50 | `art297_sec9.residence_intrusion_rape` | approve | post_outcome | offense_scope / not_applicable | base | `dwelling_intrusion` | 주거침입강간 특별법 단순일죄 |
| 51 | `art297_sec9.robbery_rape` | approve | post_outcome | offense_scope / not_applicable | base | `robbery` | 강도 기회의 동일 피해자 강간은 강도강간 단순일죄 |
| 52 | `art297_sec9.separate_confinement_rape_violence` | approve | post_outcome | concurrence / not_applicable | base | `confinement` | 감금 중 새 강간고의·별도 폭행협박이면 실체적 경합 |
| 53 | `art297_sec9.special_rape` | approve | post_outcome | offense_scope / not_applicable | base | `special_rape` | 흉기휴대·2인 이상 합동의 특수강간 가중유형 |
| 54 | `art297_sec9.special_robbery_rape` | approve | post_outcome | offense_scope / not_applicable | base | `special_robbery_rape` | 특수강도강간 특별법 단순일죄 |
| 55 | `art297_sec9.special_theft_rape` | approve | post_outcome | offense_scope / not_applicable | base | `special_theft_rape` | 야간주거침입절도·특수절도 뒤 강간의 특별법 가중유형 |
| 56 | `art297_sec9.theft_rape_concurrence` | approve | post_outcome | concurrence / not_applicable | base | `theft` | 단순 절도 뒤 강간은 실체적 경합 |

현재 레지스트리에 이미 있는 `robbery`, `theft`, `dwelling_intrusion`과 P2의
`sexual_offense_attempt`, `quasi_sexual_offense`, `sexual_offense_injury_or_death`는
resolved reference로 남는다. 특별법·감금·총칙 공범 등 미등록 단위만
`predicate_ir_missing`으로 보고한다.
