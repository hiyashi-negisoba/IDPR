# 과실치사·업무상과실치사상 RuleIR 제안 02 — 업무상과실치사상

제268조 업무상과실의 업무성·주의의무·허용된 위험·분업 카드를 판정한다.

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 15 | `art268.adequate_causation` | approve | component | causation / mandatory_all | occupational | - | 업무상 과실과 사망·상해 결과 사이 상당인과관계·객관적 귀속 |
| 16 | `art268.business_definition` | approve | component | business_status / alternative_any | occupational | - | 계속적 사무와 생명·신체 위험방지 의무라는 업무의 기본 정의 |
| 17 | `art268.business_no_license_requirement` | approve | component | business_status / alternative_any | occupational | - | 면허·영리성 없이도 반복·계속 의사나 사실로 업무성을 인정하는 경로 |
| 18 | `art268.child_near_road_duty` | approve | component | duty_breach / alternative_any | occupational | - | 어린이 돌발진입을 인식한 운전자의 감속·주시·경음 의무 |
| 19 | `art268.crossing_guard_safe_opening` | approve | component | duty_breach / alternative_any | occupational | - | 복선 건널목 안전확인 없이 개방한 안내원의 과실 인정경로 |
| 20 | `art268.crosswalk_green_signal_stop` | approve | component | duty_breach / alternative_any | occupational | - | 녹색 보행신호 횡단자 보호를 위한 일시정지 의무 |
| 21 | `art268.crosswalk_signal_transition` | approve | component | duty_breach / alternative_any | occupational | - | 신호 전환 무렵 기존 보행자의 동태 확인·서행 의무 |
| 22 | `art268.duty_scope` | approve | component | duty_breach / alternative_any | occupational | - | 법령뿐 아니라 관습·조리상 주의의무를 포함하는 일반 인정경로 |
| 23 | `art268.emergency_treatment_risk_balance` | approve | bar | permitted_risk / not_applicable | occupational | - | 긴급치료 이익이 준비 부족 위험보다 큰 경우 책임을 제한 |
| 24 | `art268.forward_observation` | approve | component | duty_breach / alternative_any | occupational | - | 사전 전방·좌우 주시로 미리 사고를 방지할 수 있었던 경우 |
| 25 | `art268.general_requirements` | rewrite | component | general_requirements / mandatory_all | occupational | - | 제268조 전체에 공통되는 과실·타인 결과·인과관계로 언래핑하여 gross가 선택 상속 |
| 26 | `art268.horizontal_medical_division` | approve | bar | duty_scope / not_applicable | occupational | - | 대등한 수평적 분업에서 다른 의사의 전적인 과실은 책임범위를 차단 |
| 27 | `art268.industrial_safety_general_duty` | approve | component | duty_breach / alternative_any | occupational | - | 산업안전법 위반 또는 별도 일반 주의의무 위반의 인정경로 |
| 28 | `art268.medical_allowed_risk` | approve | bar | permitted_risk / not_applicable | occupational | - | 구체적 의료위험과 치유가능성 비교 후 허용된 위험이면 과실을 차단 |
| 29 | `art268.medical_negligence_test` | approve | component | duty_breach / alternative_any | occupational | - | 당시 통상 의료수준·환경을 기준으로 한 예견·회피 가능성 |
| 30 | `art268.medical_transfer_duty` | approve | component | duty_breach / alternative_any | occupational | - | 자체 치료가 어려운 경우 협진·신속 전원의무 |
| 31 | `art268.multiple_victims_imaginary_concurrence` | approve | post_outcome | offense_count / not_applicable | occupational | - | 업무상·중과실의 다수 피해 결과는 성립 후 상상적 경합 |
| 32 | `art268.nonperiodic_owner_not_work` | approve | bar | business_status / not_applicable | occupational | - | 비정기 수리·일부 임대만으로 안전관리 업무의 계속성이 없음 |
| 33 | `art268.occupational_negligence_definition` | approve | component | duty_breach / alternative_any | occupational | - | 업무상 요구되는 주의의무 태만이라는 일반 인정경로 |
| 34 | `art268.pedestrian_reliance_limited` | context_only | context_only | - | - | 보행자 사고에서 신뢰원칙이 철저히 적용되지 않는다는 경향 소개만으로 사건별 의무위반을 확정할 수 없음 |
| 35 | `art268.permitted_risk` | approve | bar | permitted_risk / not_applicable | occupational | - | 사회적으로 허용된 위험이면 결과예견·회피의무 위반을 이유로 과실을 인정하지 않음 |
| 36 | `art268.personal_capacity_no_exemption` | context_only | context_only | - | - | 개인적 주의능력 부족이 면책되지 않는다는 규범은 사실상 duty breach 자체가 아님 |
| 37 | `art268.professional_benchmark` | approve | component | duty_breach / alternative_any | occupational | - | 해당 직업·생활영역의 일반적 보통인을 기준으로 하는 인정경로 |
| 38 | `art268.rail_engineer_crossing_person` | approve | component | duty_breach / alternative_any | occupational | - | 구체적 위험 인식 후 열차의 정차·감속·경적 의무 |
| 39 | `art268.rail_worker_reliance` | rewrite | bar | duty_breach / not_applicable | occupational | - | 특별사정 없는 숙련 철도작업자에 대한 신뢰가 허용되는 부분만 차단규칙으로 분리 |
| 40 | `art268.red_crosswalk_reliance` | approve | bar | duty_breach / not_applicable | occupational | - | 적색 보행신호와 특별사정 부재 시 돌발진입까지 예견할 의무가 없음 |
| 41 | `art268.reliance_known_or_unreliable_other` | approve | component | duty_breach / alternative_any | occupational | - | 위반 인식·취약자·위험장소에서는 신뢰원칙을 원용할 수 없음 |
| 42 | `art268.reliance_principle_general` | approve | bar | duty_breach / not_applicable | occupational | - | 자신이 의무를 다하고 타인의 준수를 신뢰하는 것이 상당하면 책임을 차단 |
| 43 | `art268.road_reliance_principle` | approve | bar | duty_breach / not_applicable | occupational | - | 특별사정 없는 교통규칙 준수 운전자에게 상대방 위반 예견의무가 없음 |
| 44 | `art268.secondary_rail_accident_prevention` | approve | component | duty_breach / alternative_any | occupational | - | 제2사고 방지조치를 할 수 있었는데도 하지 않은 부작위 |
| 45 | `art268.ship_collision_other_fault` | approve | component | duty_breach / alternative_any | occupational | - | 상대 선박 과실을 인식하고도 회피조치를 하지 않은 경우 |
| 46 | `art268.train_signal_confirmation` | approve | component | duty_breach / alternative_any | occupational | - | 열차 신호 확인이라는 기본의무 위반 |
| 47 | `art268.vertical_medical_division_supervision` | approve | component | duty_breach / alternative_any | occupational | - | 수직적 의료분업에서 주된 의사의 확인·감독 의무 |
| 48 | `art268.victim_negligence_no_exemption` | context_only | context_only | - | - | 피해자 과실 경합만으로 면책되지 않지만 피고인의 독립된 과실을 대신 증명하지는 않음 |
| 49 | `art268_sec1_1.medical_negligence_professional_benchmark` | approve | component | duty_breach / alternative_any | occupational | - | #29와 동일한 판례기준의 추가 provenance |
| 50 | `art268_sec1_1.non_punishable_against_victim_intent` | approve | post_outcome | prosecution_condition / not_applicable | occupational | - | 상해 결과도 반의사불벌죄가 아니라는 소추효과 |
| 51 | `art268_sec1_1.objective_duty_in_risky_work` | approve | component | duty_breach / alternative_any | occupational | - | 위험업무 참여자에게 요구되는 고도의 객관적 주의의무 |
| 52 | `art268_sec1_1.offense_overview` | approve | component | occupational_offense / mandatory_all | occupational | - | 업무상 과실로 타인을 사망·상해에 이르게 한 기본 구성요건 |
| 53 | `art268_sec1_1.status_aggravated_offense` | context_only | context_only | - | - | 신분적 가중유형이라는 법적 성격 설명은 별도 사건요건이 아님 |

## 정확한 rewrite

- **#25**: 형법 제268조의 죄가 성립하려면 과실, 행위자 이외의 다른 사람의 사망 또는
  신체상 상해 결과, 그리고 과실과 결과 사이의 인과관계가 충족되어야 한다.
- **#39**: 철도 공사관계자 등이 위험성과 합리적 피양방법을 숙지하고 열차 접근 시
  피양하도록 정해져 있으며 달리 피양을 기대할 수 없는 특별한 사정이 없다면, 승무원은
  그들이 피양할 것을 신뢰할 수 있다.

#25의 원문은 제268조 해설에서 “본죄”라고 하므로 업무상과실과 중과실에 공통되는
일반요건으로 한정하여 언래핑한다. #39의 후반부 예외까지 한 bar에 넣으면 예외사실이
있는데도 면책이 발화할 수 있으므로 신뢰가 허용되는 적극 조건만 남긴다.
