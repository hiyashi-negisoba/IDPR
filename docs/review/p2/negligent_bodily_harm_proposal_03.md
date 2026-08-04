# 과실치사·업무상과실치사상 RuleIR 제안 03 — 중과실과 죄수

중과실 판단은 `gross` track으로 분리한다. 업무자 지위는 요구하지 않고, 제268조 공통
일반요건과 고의부재·고의경계만 선택 상속한다.

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 54 | `art268_sec2_1.gross_negligence_definition` | approve | component | gross_degree / alternative_any | gross | - | 주의의무 위반이 매우 크고 약간의 주의로 결과를 피할 수 있었던 경우 |
| 55 | `art268_sec2_1.gross_negligence_social_notion` | approve | component | gross_degree / alternative_any | gross | - | 구체적 사건의 사회통념에 따른 경과실 구별기준 |
| 56 | `art268_sec2_1.high_risk_situation_gross_negligence` | approve | component | gross_degree / alternative_any | gross | - | 고도 위험을 인식·용이하게 인식한 상황의 특별한 신중의무 위반 |
| 57 | `art268_sec2_1.nonprofessional_dangerous_work_gross_negligence` | approve | component | gross_degree / alternative_any | gross | - | 비업무자가 위험사무 유형을 수행하며 위험억제 의무를 크게 위반한 경우 |
| 58 | `art268_sec2_2.candle_in_warehouse` | approve | bar | gross_degree / not_applicable | gross | - | 인화물질 없는 창고의 촛불 방치는 경과실에 불과 |
| 59 | `art268_sec2_2.cigarette_fire_inn` | approve | component | gross_degree / alternative_any | gross | - | 인화성 물건이 많은 좁은 여관방의 담뱃불 미소화 |
| 60 | `art268_sec2_2.cigarette_fire_motel` | approve | component | gross_degree / alternative_any | gross | - | 불붙기 쉬운 휴지를 재떨이에 버리고 잠든 경우 |
| 61 | `art268_sec2_2.gross_negligence_definition` | approve | component | gross_degree / alternative_any | gross | - | 극히 근소한 주의로 결과를 인식할 수 있었던 중과실 정의 |
| 62 | `art268_sec2_2.landlord_coal_gas_death` | approve | bar | gross_degree / not_applicable | gross | - | 임차인의 통상 수선·관리 범위인 결함은 임대인의 중과실을 차단 |
| 63 | `art268_sec2_2.parking_entrance_collapse` | approve | component | gross_degree / alternative_any | gross | - | 도괴 위험을 알면서 임시지지·접근차단을 하지 않은 경우 |
| 64 | `art268_sec2_2.pesticide_disguised_storage` | approve | component | gross_degree / alternative_any | gross | - | 식품과 같은 포장으로 농약을 방치하고 가족에게 알리지 않은 경우 |
| 65 | `art268_sec2_2.pesticide_poisoning_home_treatment` | approve | bar | gross_degree / not_applicable | gross | - | 제시된 자가치료 사정만으로 중과실을 인정할 수 없음 |
| 66 | `art268_sec2_2.prayer_physical_force_death` | approve | component | gross_degree / alternative_any | gross | - | 취약자의 배·가슴을 반복 강타·압박해 치명적 결과를 쉽게 예견한 경우 |
| 67 | `art268_sec2_2.russian_roulette_failure_to_stop` | approve | bar | gross_degree / not_applicable | gross | - | 말로 만류하고 즉시 물리력으로 막지 못한 사정만으로 중과실이 아님 |
| 68 | `art268_sec2_2.unextinguished_match_trash` | approve | component | gross_degree / alternative_any | gross | - | 성냥불 소화를 확인하지 않고 휴지통에 버린 경우 |
| 69 | `art268_sec2_2.unqualified_electrician_fire` | approve | bar | gross_degree / not_applicable | gross | - | 전문지식 없는 영업자가 합선화재를 쉽게 예견하기 어려웠던 경우 |
| 70 | `art268_sec3_2.dangerous_driving_inclusion` | approve | post_outcome | concurrence / not_applicable | occupational | `dangerous_driving` | 위험운전치사상 성립 시 교통사고처리특례법죄 흡수 |
| 71 | `art268_sec3_2.drunk_driving_negligent_injury` | approve | post_outcome | concurrence / not_applicable | occupational | `drunk_driving` | 음주운전죄와 업무상과실치사상죄의 실체적 경합 |
| 72 | `art268_sec3_2.failure_to_rescue_after_accident` | approve | post_outcome | concurrence / not_applicable | occupational | `failure_to_rescue_after_accident` | 사고후 조치의무위반죄와의 실체적 경합 |
| 73 | `art268_sec3_2.hit_and_run_inclusion` | approve | post_outcome | concurrence / not_applicable | occupational | `hit_and_run` | 도주차량 가중처벌죄 성립 시 제268조 죄 흡수 |
| 74 | `art268_sec3_2.imaginary_concurrence_single_act` | approve | post_outcome | concurrence_standard / not_applicable | occupational | - | 사회관념상 하나의 행위라는 상상적 경합 판단기준 |
| 75 | `art268_sec3_2.industrial_safety_negligent_death` | approve | post_outcome | concurrence / not_applicable | occupational | `industrial_safety` | 동일한 의무위반인 산업안전법죄와 상상적 경합 |
| 76 | `art268_sec3_2.safety_duty_complete_overlap` | approve | post_outcome | concurrence / not_applicable | occupational | `safety_regulation_offense` | 안전의무가 완전히 일치하면 단속법규위반죄 흡수 |
| 77 | `art268_sec3_2.safety_duty_partial_overlap` | approve | post_outcome | concurrence / not_applicable | occupational | `safety_regulation_offense` | 의무 일부만 겹치면 상상적 경합 |
| 78 | `art268_sec3_2.safety_duty_unrelated` | approve | post_outcome | concurrence / not_applicable | occupational | `safety_regulation_offense` | 의무가 무관하면 실체적 경합 |
| 79 | `art268_sec3_2.safety_regulation_duty_distinction` | approve | post_outcome | concurrence_standard / not_applicable | occupational | `safety_regulation_offense` | 구체적 주의의무와 일반·정형적 안전의무의 구별기준 |
| 80 | `art268_sec3_2.serious_disaster_industrial_safety_negligent_death` | approve | post_outcome | concurrence / not_applicable | occupational | `serious_disaster_industrial_safety` | 동일 피해자·동일 부작위의 중대재해·산안법·과실치사 상상적 경합 |
| 81 | `art268_sec3_2.traffic_special_act_inclusion` | approve | post_outcome | concurrence / not_applicable | occupational | `traffic_special_act` | 교통사고처리특례법죄 성립 시 업무상과실치사상 흡수 |
| 82 | `art268_sec3_2.unlicensed_driving_negligent_injury` | approve | post_outcome | concurrence / not_applicable | occupational | `unlicensed_driving` | 무면허운전죄와 업무상과실치사상죄의 실체적 경합 |

죄수 카드는 모두 `post_outcome`으로 보존한다. 외부 단위가 현재 레지스트리에 없으면
가짜 흡수·경합 결론을 내지 않고 해당 참조를 `predicate_ir_missing`으로 남긴다. #31과
#70~82는 명제상 중과실에도 적용되는 범위가 있으므로, `gross`가 `offense_count`와
`concurrence` placement를 선택 상속하도록 제안한다.
