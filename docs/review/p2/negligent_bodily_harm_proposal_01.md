# 과실치사·업무상과실치사상 RuleIR 제안 01 — track과 보통과실치사

대상은 `negligent_bodily_harm_review_queue.json` 85장 중 제267조 기본 카드 14장과
고의 경계·결정 C 카드 3장이다. 번호는 검토 큐의 1-based 순번이다.

## 구조 제안

| track | 의미 | 다른 track에서 가져오는 placement |
|---|---|---|
| `ordinary` | 제267조 과실치사 | - |
| `occupational` | 제268조 업무상과실치사상 | `ordinary`의 고의부재·고의경계·태아배제 |
| `gross` | 제268조 중과실치사상 | 위 공통 placement와 제268조 일반요건 |

역할 tuple은 세 track 모두
`negligent_bodily_harm_case_roles(case_id, defendant_id, victim_id)`를 쓴다.

## 카드별 제안

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 1 | `art267_sec1.negligent_homicide_definition` | approve | component | death_result / mandatory_all | ordinary | - | 과실로 사람을 사망하게 한 제267조 결과요건 |
| 2 | `art267_sec1.no_intent_to_kill_injure_or_assault` | approve | component | absence_of_intent / alternative_any | ordinary | - | 살해·상해·폭행 고의가 없어야 하는 과실범 경계 |
| 3 | `art267_sec2.causal_link.negligent_act_and_result` | approve | component | causation / alternative_any | ordinary | - | 과실행위와 사망 결과 사이 인과관계 |
| 4 | `art267_sec2.causal_link.prank_throwing_at_sea` | approve | component | causation / alternative_any | ordinary | - | 헹가래 행위와 익사 결과의 인과관계 인정경로 |
| 5 | `art267_sec2.definition.person_begins_regular_labor` | approve | component | person_begins / mandatory_all | ordinary | - | 규칙적 진통을 동반한 분만개시라는 사람의 시기 |
| 6 | `art267_sec2.elements.negligent_breach_and_death` | approve | component | duty_breach / alternative_any | ordinary | - | 주의의무위반 과실행위의 일반 인정경로 |
| 7 | `art267_sec2.standard.bus_driver_instant_wheel_entry` | rewrite | bar | duty_breach / not_applicable | ordinary | - | 갑작스러운 진입으로 발견·회피가 불가능한 경우만 차단규칙으로 언래핑 |
| 8 | `art267_sec2.standard.fetus_before_regular_labor_not_person` | approve | bar | pre_person_exclusion / not_applicable | ordinary | - | 규칙적 진통 전 태아는 사람인 객체가 아니라는 차단규칙 |
| 9 | `art267_sec2.standard.landlord_failure_gas_warning` | approve | component | duty_breach / alternative_any | ordinary | - | 반복된 경고 뒤 조사·대책을 하지 않은 임대인의 과실 인정경로 |
| 10 | `art267_sec2.standard.landlord_negligence_assessment_factors` | approve | component | duty_breach / alternative_any | ordinary | - | 구조·노후화·대수선 필요성을 종합하는 과실 판단경로 |
| 11 | `art267_sec2.standard.landlord_no_negligence_minor_defect` | approve | bar | duty_breach / not_applicable | ordinary | - | 임차인의 통상 수선·관리 범위인 경미한 하자는 임대인 과실을 차단 |
| 12 | `art267_sec2.standard.prank_throwing_foreseeability` | approve | component | duty_breach / alternative_any | ordinary | - | 폭풍주의보·미끄러운 바위에서의 결과 예견가능성 |
| 13 | `art267_sec4.death_and_injury_single_negligent_act` | approve | post_outcome | concurrence / not_applicable | ordinary | `negligent_bodily_injury` | 사망·상해 피해자가 다른 경우 상상적 경합. 제266조 단위 필요 |
| 14 | `art267_sec4.multiple_deaths_single_negligent_act` | approve | post_outcome | offense_count / not_applicable | ordinary | - | 피해자별 수죄와 상상적 경합은 성립 후 죄수효과 |
| 83 | `art268_sec3_2.vehicle_accident_conditional_intent` | context_only | context_only | - | - | - | 살인·상해 고의를 한 카드로 묶어 단일 boundary로 실행하면 두 경계를 동시에 발화시키므로 라우터 문맥으로 보존 |
| 84 | `art268_sec3_2.vehicle_avoidance_effort_negligence` | approve | component | absence_of_intent / alternative_any | ordinary | - | 실제 감속·서행 등 회피노력은 폭행 실행이 아니라 과실이라는 인정경로 |
| 85 | `art268.illicit_work_excluded` | approve | bar | business_status / not_applicable | occupational | `negligent_bodily_injury` | 결정 C가 선택한 불법업무 배제. 상해 결과의 제266조는 현재 미지원 |

## 정확한 rewrite

- **#7**: 피해자가 버스 발차 순간 바퀴 밑으로 갑자기 들어가 운전자가 이를 발견하거나
  회피할 수 없었던 경우에는 운전자의 과실을 인정할 수 없다.

원문 두 번째 문장의 “더 일찍 들어갔는지가 밝혀지지 않으면 과실 유무를 가릴 수 없다”는
증명도 판단이다. 이를 동일한 bar에 넣으면 불명확하다는 사실만으로 불성립이 확정되므로
제외한다. 그 상태는 호스트의 `unknown` 평가가 담당한다.
