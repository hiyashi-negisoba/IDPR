# negligent_bodily_harm RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/negligent_bodily_harm_approved_decisions.json`
- approval SHA-256: `678c20f48db5c3466a7d75ee76c218de4e76eccffdd3e10fea95d372950926cf`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 85
- components: 20
- context_only 제외: 5
- 미해결 unit 참조: 14

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art267_sec4.death_and_injury_single_negligent_act` → `negligent_bodily_injury` (predicate_ir_missing)
- `art268_sec3_2.dangerous_driving_inclusion` → `dangerous_driving` (predicate_ir_missing)
- `art268_sec3_2.drunk_driving_negligent_injury` → `drunk_driving` (predicate_ir_missing)
- `art268_sec3_2.failure_to_rescue_after_accident` → `failure_to_rescue_after_accident` (predicate_ir_missing)
- `art268_sec3_2.hit_and_run_inclusion` → `hit_and_run` (predicate_ir_missing)
- `art268_sec3_2.industrial_safety_negligent_death` → `industrial_safety` (predicate_ir_missing)
- `art268_sec3_2.safety_duty_complete_overlap` → `safety_regulation_offense` (predicate_ir_missing)
- `art268_sec3_2.safety_duty_partial_overlap` → `safety_regulation_offense` (predicate_ir_missing)
- `art268_sec3_2.safety_duty_unrelated` → `safety_regulation_offense` (predicate_ir_missing)
- `art268_sec3_2.safety_regulation_duty_distinction` → `safety_regulation_offense` (predicate_ir_missing)
- `art268_sec3_2.serious_disaster_industrial_safety_negligent_death` → `serious_disaster_industrial_safety` (predicate_ir_missing)
- `art268_sec3_2.traffic_special_act_inclusion` → `traffic_special_act` (predicate_ir_missing)
- `art268_sec3_2.unlicensed_driving_negligent_injury` → `unlicensed_driving` (predicate_ir_missing)
- `art268.illicit_work_excluded` → `negligent_bodily_injury` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `gross` | `gross_degree` | bar, component | alternative_any | 16 | - |
| `occupational` | `business_status` | bar, component | alternative_any | 4 | negligent_bodily_injury |
| `occupational` | `causation` | component | mandatory_all | 1 | - |
| `occupational` | `concurrence` | post_outcome |  | 11 | dangerous_driving, drunk_driving, failure_to_rescue_after_accident, hit_and_run, industrial_safety, safety_regulation_offense, serious_disaster_industrial_safety, traffic_special_act, unlicensed_driving |
| `occupational` | `concurrence_standard` | post_outcome |  | 2 | safety_regulation_offense |
| `occupational` | `duty_breach` | bar, component | alternative_any | 23 | - |
| `occupational` | `duty_scope` | bar |  | 1 | - |
| `occupational` | `general_requirements` | component | mandatory_all | 1 | - |
| `occupational` | `occupational_offense` | component | mandatory_all | 1 | - |
| `occupational` | `offense_count` | post_outcome |  | 1 | - |
| `occupational` | `permitted_risk` | bar |  | 3 | - |
| `occupational` | `prosecution_condition` | post_outcome |  | 1 | - |
| `ordinary` | `absence_of_intent` | component | alternative_any | 2 | - |
| `ordinary` | `causation` | component | alternative_any | 2 | - |
| `ordinary` | `concurrence` | post_outcome |  | 1 | negligent_bodily_injury |
| `ordinary` | `death_result` | component | mandatory_all | 1 | - |
| `ordinary` | `duty_breach` | bar, component | alternative_any | 6 | - |
| `ordinary` | `offense_count` | post_outcome |  | 1 | - |
| `ordinary` | `person_begins` | component | mandatory_all | 1 | - |
| `ordinary` | `pre_person_exclusion` | bar |  | 1 | - |

## RuleIR에서 제외된 카드

- `art268.pedestrian_reliance_limited`: 보행자 사고에서 신뢰원칙이 철저히 적용되지 않는다는 경향 소개만으로 사건별 의무위반을 확정할 수 없음
- `art268.personal_capacity_no_exemption`: 개인적 주의능력 부족이 면책되지 않는다는 규범은 사실상 duty breach 자체가 아님
- `art268.victim_negligence_no_exemption`: 피해자 과실 경합만으로 면책되지 않지만 피고인의 독립된 과실을 대신 증명하지는 않음
- `art268_sec1_1.status_aggravated_offense`: 신분적 가중유형이라는 법적 성격 설명은 별도 사건요건이 아님
- `art268_sec3_2.vehicle_accident_conditional_intent`: 살인·상해 고의를 한 카드로 묶어 단일 boundary로 실행하면 두 경계를 동시에 발화시키므로 라우터 문맥으로 보존
