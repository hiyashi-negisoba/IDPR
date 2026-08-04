# 강간 RuleIR 제안 02 — 폭행·협박·간음·동의·고의·미수경계

강간 기수의 실행 component와 제300조·준강간·유사강간 경계를 판정한다.

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 15 | `art297_sec4_1.direct_violence_threat` | rewrite | boundary | coercion_attribution / not_applicable | base | `quasi_sexual_offense` | 타인이 만든 폭행·협박 상태를 이용했을 뿐이면 직접 강간이 아니라 준강간 경계 |
| 16 | `art297_sec4_1.extramarital_exposure_threat` | approve | component | coercive_degree / alternative_any | base | - | 불륜 폭로 협박의 내용·범위·관계·압박을 종합하는 인정경로 |
| 17 | `art297_sec4_1.force_threat_temporal_gap` | approve | component | coercion_timing / alternative_any | base | - | 폭행·협박과 간음 사이 시간간격이 있어도 되는 경로 |
| 18 | `art297_sec4_1.force_threat_timing_before_completion` | approve | component | coercion_timing / alternative_any | base | - | 폭행·협박이 간음 종료 전까지 존재하면 되는 일반 시간경계 |
| 21 | `art297_sec4_1.no_retrospective_inference` | context_only | context_only | - | - | - | 사후 이탈·불충분한 반항만으로 강제성을 부정하지 말라는 증거평가 한계 |
| 22 | `art297_sec4_1.third_party_or_property_threat` | approve | component | coercive_degree / alternative_any | base | - | 제3자 폭행·기물파괴·가족위협으로 피해자 저항의지를 제압한 경로 |
| 23 | `art297_sec4_1.threat_alone` | approve | component | coercive_degree / alternative_any | base | - | 항거불능·현저한 곤란 정도의 협박만으로도 성립 |
| 25 | `art297_sec4_1.violence_threat_definition` | approve | component | coercive_means / mandatory_all | base | - | 유형력 행사 또는 공포심을 일으킬 해악고지라는 수단요건 |
| 26 | `art297_sec4_2.non_vaginal_acts_exception` | approve | bar | penetration / not_applicable | base | `quasi_rape` | 구강·항문성교 등 비질성교는 제297조 강간을 차단하고 유사강간으로 이동 |
| 27 | `art297_sec4_2.rape_and_penetration` | approve | component | coercive_degree / alternative_any | base | - | 상대방 반항을 불가능·현저히 곤란하게 하는 최협의 폭행·협박 기준 |
| 28 | `art297_sec4_2.violence_intercourse_causation` | approve | component | causation / mandatory_all | base | - | 폭행·협박에 의하여 간음이 이루어진 인과관계 |
| 29 | `art297_sec4_3.attempt_commencement` | approve | post_outcome | attempt_commencement / not_applicable | base | `sexual_offense_attempt` | 최협의 폭행·협박 개시 시 실행착수. 제300조 unit에서 사용 |
| 30 | `art297_sec4_3.attempt_commencement_context` | approve | post_outcome | attempt_commencement_standard / not_applicable | base | `sexual_offense_attempt` | 언행·행동·주변정황을 종합하는 착수 판단기준 |
| 31 | `art297_sec4_3.completion` | approve | component | penetration / mandatory_all | base | - | 성기 삽입·결합 순간 기수이며 완전삽입·사정은 불필요 |
| 32 | `art297_sec4_3.voluntary_abandonment` | approve | post_outcome | attempt_outcome / not_applicable | base | `sexual_offense_attempt` | 자의적 실행중지는 제300조·제26조 중지미수 효과 |
| 33 | `art297_sec4_4.successive_co_perpetration_negative` | approve | post_outcome | participation_form / not_applicable | base | `complicity` | 기능적 행위지배 없는 후행자의 승계적 공동정범 부정 |
| 34 | `art297_sec4_4.successive_perpetrator_quasi_rape` | approve | post_outcome | participation_form / not_applicable | base | `quasi_sexual_offense` | 선행자가 만든 상태를 이용한 후행자는 준강간 경계 |
| 35 | `art297_sec5.consent_assessment` | approve | component | absence_of_consent / alternative_any | base | - | 성적 자기결정권 침해 여부에 따른 동의 판단의 일반경로 |
| 36 | `art297_sec5.prior_communications_not_consent` | approve | component | absence_of_consent / alternative_any | base | - | 연락·호감 정황만으로 성관계 동의가 되지 않음 |
| 37 | `art297_sec5.valid_consent` | approve | bar | absence_of_consent / not_applicable | base | - | 피해자 본인의 유효한 동의는 구성요건 해당성을 차단 |
| 38 | `art297_sec5.withdrawn_consent` | approve | component | absence_of_consent / alternative_any | base | - | 사전 동의를 번복한 뒤에는 동의가 없음 |
| 39 | `art297_sec6.intent` | approve | component | intent / mandatory_all | base | - | 폭행·협박으로 강간한다는 인식·의사, 미필적 고의 포함 |
| 40 | `art297_sec6.mistake_of_consent` | approve | bar | intent / not_applicable | base | - | 피해자 동의가 있다고 오인하면 강간의 고의를 차단 |

## 정확한 rewrite

- **#15**: 행위자가 타인이 가한 폭행·협박 상태를 이용하여 피해자를 간음했을 뿐 자신이
  폭행·협박을 가하지 않은 경우에는 강간죄가 아니라 준강간죄가 성립할 수 있다.

원문의 “폭행·협박은 행위자가 직접 가한 것이어야 한다”를 모든 사건에서 별도 필수
component로 만들면 #22의 제3자·가족 위해 협박과 충돌한다. 따라서 행위자가 타인의 기존
강제상태를 단순 이용한 경우만 강간을 차단하는 boundary로 언래핑한다.
