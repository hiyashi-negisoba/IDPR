# Predicate 사전 초안 v0 — 검수 게이트 ①

**범위**: 각칙 재산죄 core 7개 조문(329·333·347·350·355·357·366) + 총칙 우선순위 8개 조문
(10·21·25·26·27·30·31·32). Track 2 마스터플랜의 "predicate-first 1패스" — 이 사전이
승인되기 전에는 2패스 조립(`data/v2/definitions/` 실제 저작)에 들어가지 않는다.

**표기 규칙**: `id`는 확정 아님(작업용 가칭). `grounded_by`는 legal_element가 어느
ground_fact에서 도출되는지의 제안. "근거"란은 워크시트의 카드 id 또는 총칙 조문의
section_path — 스크립트가 자동으로 이 chunk가 근거라고 판정한 게 아니라 내가 지금
읽고 직접 연결한 것이다. "검수 필요"란은 그대로 승인 대상이 아니라 사용자가 먼저
판단해야 하는 지점.

---

## A. 각칙 재산죄 core — predicate 후보

7개 조문 119장 카드(필터 통과분)를 근거로 정리. v1의 폭발을 재현하지 않기 위해 **조문마다
새 predicate를 만들지 않고, 여러 조문에 걸쳐 쓰이는 개념은 공유 predicate로 묶었다.**

### A-1. 조문 간 공유되는 predicate (dedup 후보)

| id (가칭) | canonical_meaning | 근거 카드 | 검수 필요 |
|---|---|---|---|
| `legal_element.unlawful_appropriation_intent` | 권리자를 배제하고 경제적 용법에 따라 이용·처분할 의사(불법영득의사)가 인정된다 | art329_sec5_1, art333_sec5(불법영득/이득의사) | 절도·강도는 "의사" 자체, 횡령(art355)은 "**객관적으로 표현**된" 의사를 별도로 요구(`art355_sec3_3.objective_manifestation`) — 같은 predicate로 묶을지, 횡령 전용 legal_element를 하나 더 둘지 판단 필요 |
| `legal_element.property_disposition` | 피해자(또는 처분권한자)가 재물 또는 재산상 이익을 이전하는 처분행위를 하였다 | art350_sec1(공갈), fraud_mistake.property_disposition_element(사기) | 사기는 "착오에 기한" 처분, 공갈은 "하자 있는 의사에 기한" 처분 — 원인 predicate가 다르므로 relation으로 연결(causal_nexus류)할지 검토 |
| `legal_element.disposer_identity_match` | 기망/공갈을 당한 자와 처분행위자가 동일인이어야 한다 | fraud_mistake.deceived_disposer_identity, art350_sec4_4.separate_victim_disposition_authority | 사기·공갈 공통이지만 공갈 쪽은 "제3자 처분권한" 예외가 별도로 있어(art350_sec4_4) 완전 동일 predicate로 묶일지 검수 필요 |
| `doctrine.right_exercise_defense` | 행위자가 정당한 권리 범위 안에서 행사한 경우 재산범죄 성립이 부정되거나 위법성이 조각된다 | art333_sec8(강도→폭행/협박죄로 전환), art350_sec8_2(공갈 위법성조각) | **중요한 검수 포인트**: 강도는 "권리 있는 이익=애초에 불법이득 아님"이라 **구성요건 자체가 부정**(canonical_element 층), 공갈은 "위법성이 조각될 수 있다"는 **defeater**(Unlawfulness 층)다. 같은 "권리행사" 개념이 두 조문에서 서로 다른 stage에 걸리므로 절대 하나의 DoctrineDef로 합치면 안 된다 |

### A-2. 조문별 핵심 legal_element (canonical_element 카드 기반)

| 조문 | id (가칭) | canonical_meaning | 근거 |
|---|---|---|---|
| 329 절도 | `legal_element.possession` | 형법상 점유는 사실상 지배(물리적 요소) + 점유의사(정신적 요소)로 성립한다 | art329_sec2_2 |
| 329 절도 | `ground_fact.taking_conduct` | 타인 점유 재물을 그 점유자의 의사에 반해 자기(제3자) 점유로 옮겼다 | art329_sec5_1(반대해석) |
| 333 강도 | `legal_element.robbery_level_violence` | 폭행·협박이 재물탈취의 수단으로 반항을 억압할 정도에 이르렀다 | art333_sec2_1 |
| 333 강도 | `doctrine.quasi_robbery` | 절도 기수 후 탈환방지·체포면탈·증거인멸 목적으로 폭행·협박하면 준강도가 된다 | art333_sec3_3 |
| 347 사기 | `legal_element.deception` | 기망행위가 상대방에게 진실과 합치하지 않는 관념(착오)을 발생시켰다 | deception.fraud.element.deception-must-create-false-belief |
| 347 사기 | `relation.deception_error_disposition_causal_nexus` | 기망→착오→처분행위 사이에 인과관계가 있다(없으면 미수) | fraud_stages_participation.no_causation_attempt |
| 350 공갈 | `legal_element.fear_inducement` | 협박(또는 폭행)이 상대방에게 외포심을 일으켰다 | art350_sec7_2 |
| 350 공갈 | `doctrine.complete_suppression_becomes_robbery` | 의사가 완전히 억압되면 형식은 교부라도 강도죄가 된다(공갈과의 경계) | art350_sec5_3 |
| 355 횡령/배임 | `legal_element.duty_of_other_affairs` | 행위자가 타인의 사무를 처리하는 자의 지위에 있다 | art355_sec3(배임), art357_sec3_1(배임수재) — **355와 357 공유 후보** |
| 355 횡령 | `legal_element.entrustment_relationship` | 보관자·소유자 사이에 형법상 보호가치 있는 위탁관계가 있다(규범적 판단) | art355.embezzlement_protectable_entrustment |
| 357 배임수재/증재 | `legal_element.improper_solicitation` | 임무에 관한 부정한 청탁이 있었다 | art357_sec1_3 |
| 357 배임수재/증재 | `ground_fact.actual_acquisition` | 재물 또는 재산상 이익을 현실적으로 취득했다(요구·약속만으로는 부족) | art357_sec3_3 |
| 366 재물손괴 | `legal_element.utility_impairment` | 손괴·은닉·기타 방법으로 재물의 이용가치·효용을 침해했다 | art366_sec3_2 (하위 4개 카드로 세분: 손괴/은닉/기타방법/일시적 이용불능 포함) |
| 366 재물손괴 | `ground_fact.object_ownership_other` | 객체가 타인 소유물이다(무주물·사체·전송중 정보 등은 제외) | art366.other_person_ownership + exception 4장 |

### A-3. Completion(기수/미수) 후보 — 조문별 상이함, 공유 불가

| 조문 | 기수 시점 후보 | 미수 조건 후보 |
|---|---|---|
| 329 절도 | 배타적 지배 이전(사회통념상 종합판단) | (미수범 카드 없음 — 총칙 25조가 공급) |
| 333 강도 | 재물: 배타적 지배 이전 / 이득: 외관상 이익 이전 | 폭행·협박 착수 + 미수 성립(art333_sec6.attempt_unattained_objective) |
| 347 사기 | 지배 배제 + 자기(제3자) 지배 인정 | 인과관계 불성립 시 미수 |
| 350 공갈 | 재물 교부 / 이익 취득 시(계좌송금은 입금시) | 외포 없이 다른 이유로 교부 시 미수 |
| 355 횡령 | 불법영득의사의 **객관적 표현** 시 | (착수 개념 자체가 특수 — 별도 검수) |
| 357 배임수재 | 현실적 취득 시 | 요구·약속·공여의사표시만 한 경우 미수 |
| 366 손괴 | 효용의 감소·훼손 발생 시 | (미수 처벌규정 없음 — 카드에도 없음, 확인 필요) |

**검수 필요**: 이 표는 총칙 25-27조(Completion 축)와 각칙 개별 조문의 `CompletionPolicy.states`가
만나는 지점이다 — 총칙 predicate(범죄실현의사/실행의착수/미완성)가 "일반형"이고 위 표가 그
조문별 구체화라는 관계를 predicate 사전에 명시해야 한다.

---

## B. 총칙 8개 조문 — predicate 후보

카드가 없으므로 조문 절 구조(`Ⅱ. 성립요건` 등)에서 직접 도출. 각 항목에 어느 v2.2.0
runtime 축(Elements/Unlawfulness/Culpability/Completion/Participation)에 대응하는지 표시.

### 제10조 심신장애 (Culpability)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `ground_fact.mental_disorder_at_act_time` | 행위 당시 정신적 장애 상태에 있었다 | Ⅱ.2 |
| `legal_element.discrimination_capacity` | 사물을 변별할 능력(위법성 인식 능력)이 있었다 | Ⅱ.1.나 |
| `legal_element.control_capacity` | 변별에 따라 행위를 제어할 능력이 있었다 | Ⅱ.1.나 |
| `doctrine.insanity_defeat` | 변별능력·제어능력이 모두 없으면(심신상실) 책임이 조각된다 | Ⅱ.3.가, Ⅱ.4.가 |
| `doctrine.diminished_capacity_modify` | 변별능력·제어능력이 미약하면(심신미약) 형을 감경한다(MODIFY) | Ⅱ.3.가, Ⅱ.4.가 |
| `doctrine.actio_libera_in_causa_exception` | 스스로 자의로 심신장애 상태를 야기하고 그 상태에서 범행하면 책임감면이 배제된다 | Ⅲ.1~Ⅲ.3 |

**검수 필요**: `doctrine.actio_libera_in_causa_exception`은 위 두 doctrine에 대한
**exception의 exception**(심신장애 DEFEAT/MODIFY를 다시 무력화)이라 DoctrineDef 하나로
표현 가능한지, 아니면 심신장애 doctrine의 `requires`에 부정 조건으로 넣어야 하는지 구조
검토가 필요하다.

### 제21조 정당방위 (Unlawfulness)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `ground_fact.infringement_situation` | 자기 또는 타인의 법익에 대한 현재의 부당한 침해가 있었다(정당방위상황) | Ⅱ.1 |
| `ground_fact.defensive_act` | 침해를 방위하기 위한 행위(방위의사 포함)를 하였다 | Ⅱ.2 |
| `legal_element.reasonable_grounds` | 방위행위에 상당한 이유가 있었다 | Ⅱ.3 |
| `doctrine.self_defense` | 위 세 요건이 모두 갖춰지면 위법성이 조각된다(DEFEAT) | Ⅲ |
| `doctrine.excessive_defense` | 상당성을 넘은 방위(과잉방위)는 정황에 따라 형 감면·불벌이 가능하다 | Ⅴ.1 |

**검수 필요**: 오상방위(Ⅴ.2)·오상과잉방위(Ⅴ.3)는 "침해가 실제로는 없었는데 있다고
오인"한 경우라 **착오론**(16조 법률의 착오 또는 사실의 착오 계열)과 연결되는 논점이다 —
정당방위 DoctrineDef 하나로 다 담을지, 16조 predicate와 합성할지 검수 필요.

### 제25조 미수범 / 제26조 중지범 / 제27조 불능범 (Completion)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.criminal_realization_intent` | 범죄를 실현하려는 의사(고의)가 있었다 | 25조 Ⅲ.1 |
| `ground_fact.commencement_of_execution` | 구성요건적 행위(또는 그 직접적 행위)를 개시하였다(실행의 착수) | 25조 Ⅲ.2 |
| `ground_fact.result_not_occurred` | 범죄가 완성(기수)에 이르지 못했다 | 25조 Ⅲ.3 |
| `ground_fact.voluntary_cessation_or_prevention` | 자의로 실행을 중지하거나 결과발생을 방지하였다 | 26조 Ⅳ.1, Ⅳ.3 |
| `ground_fact.means_or_object_defect` | 실행의 수단 또는 대상의 착오로 애초에 결과발생이 불가능했다 | 27조 Ⅲ.2 |
| `legal_element.dangerousness` | (결과발생은 불가능했지만) 행위에 위험성이 인정된다 | 27조 Ⅲ.3 |

**대응 관계**: 이 6개가 위 A-3 표의 "총칙 일반형"이다 — 각칙 `CompletionPolicy.states`의
`attempted`/`abandoned_attempt`/`impossible_attempt`가 이 predicate들을 `requires`로
참조하고, 조문별 `suspends`(예: 결과·인과 slot 제외)와 결합해 구체 program이 된다.

**검수 필요**: 미수(임의적 감경)·중지미수(필요적 감면)·불능미수(위험성 있으면 임의적
감면, 없으면 불능범=무죄)의 세 MODIFY/처벌효과 구분이 `CompletionPolicy.states.*.punishable`
+ Punishability MODIFY 조합으로 정확히 표현되는지 확인 필요.

### 제30조 공동정범 / 제31조 교사범 / 제32조 종범 (Participation)

| id (가칭) | canonical_meaning | 근거 | 비고 |
|---|---|---|---|---|
| `ground_fact.joint_execution_intent` | 2인 이상이 공동으로 범행을 실행하려는 의사가 있었다 | 30조 Ⅱ.1 | 신규 |
| `ground_fact.joint_execution_conduct` | 공동의 실행행위(기능적 행위지배)가 있었다 | 30조 Ⅱ.2 | 신규 |
| `ground_fact.instigation_conduct` | 행위자가 타인으로 하여금 범죄 실행을 결의하게 하는 행위를 하였다 | 31조 Ⅱ.1 | **이미 fixture에 존재** (Step 6C, `docs/contracts/v2/examples/ground_facts.yaml:132`) — 새로 안 만들고 재사용 |
| `ground_fact.instigator_intent` | 교사자에게 교사의 고의(피교사자의 범행 결의 및 실행에 대한 인식)가 있었다 | 31조 Ⅱ.2 | 신규 |
| `ground_fact.aiding_conduct` | 행위자가 정범의 범죄 실행을 용이하게 하는 행위를 하였다 | 32조 Ⅱ.1 | **이미 fixture에 존재**(`ground_facts.yaml:140`) — 재사용 |
| `ground_fact.aiding_intent` | 방조자에게 방조의 고의가 있었다 | 32조 Ⅱ.2 | 신규 |

**검수 필요(가장 중요)**: 6C 핸드오프가 "어느 actor가 어느 mode인지 결정하는 오케스트레이터는
Step 7의 일"이라고 명시했다 — 즉 이 predicate들은 이미 **runtime이 소비할 준비가 된 계약**이고,
이번 predicate 사전 확장은 새 개념을 만드는 게 아니라 **기존 계약에 맞춰 나머지(공동정범
predicate, 교사·방조의 고의 predicate)를 채우는 작업**이라는 게 이번에 새로 확인된 사실이다.
33조(공범과 신분)·34조(간접정범)는 이 표에 없다 — 계획서에서 이미 "architecture-compatibility
검수 후 결정"으로 분류했고, 이번 15개 우선순위에도 포함되지 않는다.

---

## 요약 — 이번 15개 조문에서 나온 predicate 후보 수

```text
각칙(A절): 공유 predicate 4 + 조문별 핵심 legal_element/ground_fact 14 + doctrine 3
         = 약 21개 신규 후보 (119장 카드 → dedup 후 약 21개, v1 대비 대폭 압축)
총칙(B절): 10조 6 + 21조 5 + 25/26/27조 6 + 30/31/32조 6(그 중 2개는 이미 존재)
         = 약 23개 후보(신규 21 + 재사용 2)
```

**검수 요청 사항 정리**(위 표에 흩어진 "검수 필요" 전부):
1. 횡령의 불법영득의사(객관적 표현 요구)를 절도·강도와 같은 predicate로 묶을지, 별도로 둘지
2. 사기·공갈의 `property_disposition`/`disposer_identity_match`를 공유할지, relation으로 연결할지
3. 강도(구성요건 부정)와 공갈(위법성조각)의 "권리행사"를 **절대 같은 DoctrineDef로 합치면
   안 된다**는 판단이 맞는지
4. 재산죄 core의 Completion 후보(A-3)와 총칙 25-27조 predicate의 "일반형-구체형" 관계 설계
5. 심신장애(10조)와 원인에 있어서 자유로운 행위의 관계를 DoctrineDef 하나로 표현할지
6. 정당방위 오상방위/오상과잉방위를 16조 착오론과 어떻게 연결할지(16조는 Band A-core지만
   이번 15개 우선순위 밖)
7. 미수/중지미수/불능미수의 처벌효과 차등을 CompletionPolicy + Punishability MODIFY
   조합으로 정확히 표현할 수 있는지
