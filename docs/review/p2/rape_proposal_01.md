# 강간 RuleIR 제안 01 — 기본 구조·객체·배우자·증거

대상은 `rape_review_queue.json` 56장 중 기본 정의, 객체·주체, 배우자 강간, 피해자 방어와
증거 문맥 18장이다. 번호는 검토 큐의 1-based 순번이다.

## 구조와 역할 tuple

- 컴파일 track: `base` — 제297조 강간 기수
- 역할 tuple: `rape_case_roles(case_id, defendant_id, victim_id)`
- 제300조 미수는 별도 `sexual_offense_attempt` unit으로 연결한다.
- 간접정범은 intermediary 역할이 필요한 공유 총칙 module 전까지 문맥으로 보존한다.

## 카드별 제안

| # | card | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|---|
| 1 | `art297.conduct.violence-threat-rape` | approve | component | offense_definition / alternative_any | base | - | 폭행·협박으로 사람을 강간하는 제297조 기본 정의 |
| 2 | `art297.indirect_perpetration` | context_only | context_only | - | - | - | 간접정범은 intermediary 역할과 총칙 module 없이 단독 피고인 tuple로 실행할 수 없음 |
| 3 | `art297.object-person` | approve | component | object_scope / mandatory_all | base | - | 성별·연령·혼인·성경험·성교능력과 무관한 사람이라는 객체범위 |
| 4 | `art297.relative_special_act` | approve | post_outcome | special_statute / not_applicable | base | `relative_sexual_offense` | 친족관계 가중 특별법 적용은 성립 후 법조효과 |
| 5 | `art297.special-protection-statutes` | approve | post_outcome | special_statute / not_applicable | base | `protected_victim_sexual_offense` | 13세 미만·장애인·아동청소년 특별법은 현재 외부 단위 |
| 6 | `art297.unrestricted_principal` | context_only | context_only | - | - | - | 주체 무제한 설명만으로 구체적 강간행위나 간접정범 형태를 증명하지 않음 |
| 7 | `art297_sec1.rape_definition` | approve | component | offense_definition / alternative_any | base | - | #1과 동일한 기본 구성요건의 추가 provenance |
| 8 | `art297_sec10.planned_killing_after_rape_no_self_defense` | context_only | context_only | - | - | - | 강간 피해자의 사후 계획살인에 관한 살인·정당방위 문맥이지 피고인의 강간 성립요건이 아님 |
| 9 | `art297_sec10.self_defense_against_rape` | context_only | context_only | - | - | - | 피해자의 방어행위 위법성 조각은 별도 정당방위 문제 |
| 10 | `art297_sec10.tongue_biting_self_defense` | context_only | context_only | - | - | - | 피해자의 혀 절단 반격에 관한 정당방위 사례 |
| 11 | `art297_sec3_2.spouse_rape_holding` | approve | component | coercive_degree / alternative_any | base | - | 혼인 중에도 최협의 폭행·협박이면 강간이 성립하는 인정경로 |
| 12 | `art297_sec3_2.spouse_violence_assessment` | approve | component | coercive_degree / alternative_any | base | - | 배우자 관계와 혼인생활 정황을 포함한 폭행·협박 정도 판단경로 |
| 13 | `art297_sec3_4.intercourse_opposite_sex` | approve | component | sex_pair / mandatory_all | base | - | 단독정범의 질성교 구조상 행위주체와 객체가 서로 다른 성일 것 |
| 14 | `art297_sec3_4.sex_classification` | approve | component | sex_classification / mandatory_all | base | - | 성염색체만이 아니라 성귀속감·사회규범·일반인 평가를 종합하는 성별 판단기준 |
| 19 | `art297_sec4_1.gender_sensitive_limit` | context_only | context_only | - | - | - | 성인지 관점에도 증명력 한계가 있다는 증거평가 문맥 |
| 20 | `art297_sec4_1.gender_sensitive_testimony` | context_only | context_only | - | - | - | 피해자다움을 요구하지 않는 진술 신빙성 평가기준 |
| 24 | `art297_sec4_1.victim_testimony_reliability` | context_only | context_only | - | - | - | 유일한 직접증거인 피해자 진술의 증명력 판단기준 |
| 48 | `art297_sec9.nonprosecution_not_false_report_proof` | context_only | context_only | - | - | - | 불기소·무죄만으로 무고를 증명할 수 없다는 절차·증거 문맥 |

#14는 현행 카드 자산이 제시하는 규범적 견해를 실행기준으로 채택하는 제안이다. 생물학적
성별만으로 고정하지 않되, 피해자와 행위자의 자기진술 하나만으로 결론내리지 않고 카드가
열거한 요소를 종합평가한다.
