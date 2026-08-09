# Predicate 사전 확장 — 배치 ⑪ 주거·권리행사 (제319·323·328조) v0

[`predicate-authoring-self-check-checklist`](메모리, 7항목)와
[`shared-predicate-canonical-meaning-is-immutable`](메모리, 4항목)를 제출 **전**에
직접 대입했다 — 문서 끝 "self-check 적용 메모" 절에 항목별 결과를 남긴다. 방법론은
배치⑦-⑩과 동일(카드 1차, 원문 주석은 모호할 때만 보조).

3개 조문은 성격이 서로 다르다 — **319조**(주거침입·퇴거불응)는 한 조문 안에 **작위범
(주거침입)과 진정부작위범(퇴거불응)이 별개의 conduct로 병존**하는 첫 사례, **323조**
(권리행사방해)는 **진정신분범**(자기 물건의 소유자만 정범이 될 수 있음, 판례가 명시)의
첫 사례, **328조**(친족간의 범행)는 카드가 조문 핵심 규정(형면제/친고죄) 자체를 담고
있지 않아 **원문에서 직접 그 구조를 끌어와야 하는 조문**이자 배치⑦ 151조가 이미
"328조와 같은 계보"라고 참조해둔 인적 처벌조각사유의 **원본 조문**이다.

---

## A. 제319조 주거침입·퇴거불응

**구조 판단 — 하나의 조문, 두 개의 별개 OffenseDef.** 1항(주거침입, 작위)과 2항
(퇴거불응, 부작위)은 객체는 공유하지만 conduct·completion 구조가 전혀 달라 250(살인/
존속살해)처럼 "같은 조문 안 변형"이 아니라 **처음부터 독립된 두 OffenseDef**로
다룬다 — 아래 A-1/A-2.

### 공유 객체 predicate

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.dwelling_or_managed_premises_object`(신규) | 사람의 주거, 관리하는 건조물·선박·항공기 또는 점유하는 방실에 해당한다(건조물은 벽·기둥·지붕·천정 등을 갖추어 사람의 기거·출입에 사용할 수 있는 구조를 이루어야 하고, 미완성 건축물은 제외된다; "관리"는 사실상의 지배·관리 상태를 요하며 단순히 출입금지 표지를 해둔 것만으로는 부족하다; 계절적으로 전혀 사용하지 않는 기간의 별장은 "주거"가 아니라 "관리하는 건조물"로 재분류되어 관리 요건을 별도로 충족해야 한다) | art319_sec2_1.seasonally_unused_villa, art319_sec2_2.management_notice_insufficient, art319_sec2_2.incomplete_construction_not_building |

**검수 필요 1 — 계절적 미사용 별장의 "주거→건조물" 재분류가 하나의 legal_element
안에서 legal_standard로 표현 가능한지, 아니면 별도 서브타입 predicate가 필요한지.**
"관리" 요건은 문언상 "건조물"에만 걸리고 "주거"에는 별도로 요구되지 않는다 — 계절적
미사용 별장처럼 두 서브타입 사이의 재분류가 실제로 결과(관리 요건 충족 여부)를
바꾸는 사례가 카드에 등장하므로, 이걸 하나의 `dwelling_or_managed_premises_object`
predicate의 legal_standard 서술만으로 충분히 담아내는지 v0은 확정하지 않는다(단일
predicate로 시도하되, 2패스 실제 저작 시 사실관계 대입이 막히면 서브타입 분리로
승격).

`art319_sec2_2.unmanaged_empty_house`(관리 안 된 빈집 무단출입은 경범죄처벌법
위반이지 주거침입죄가 아님)와 `art319_sec2_2.joint_occupier_entry`(공동관리 중
건조물에 공동점유자 1인의 임의 출입은 건조물침입죄 불성립)는 신규 predicate가
아니라 위 predicate의 legal_standard 경계(각각 "관리" 요건 미충족, "관리하는" 주체가
공동점유자 자신도 포함되어 침입 상대방이 없는 경우)를 보여주는 authoring 메모로
남긴다.

### A-1. 주거침입 (작위)

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.dwelling_or_managed_premises_object`(위 공유 predicate 재사용) | — | art319_Ⅰ |
| `legal_element.trespass_entry`(신규) | 거주자·관리자·점유자가 누리는 사실상의 평온상태를 해치는 행위태양으로 그 신체가 주거 등에 들어갔다(신체 전부가 들어가야 하는 것은 아니고 일부만 들어가도 사실상 평온을 해할 정도면 기수에 이른다; 해당 여부는 출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 출입 경위·방법, 주거 등의 형태·용도·통제관리 방식을 종합적으로 고려해 판단한다; 거주자 등의 명시적·묵시적·추정적 동의가 있으면 침입이 아니지만 강박에 의한 동의는 무효이고, 일반인의 출입이 허용된 공개장소에 통상적 출입방법으로 들어간 경우 개별 자격이나 사후에 생긴 불법한 목적은 침입 여부에 영향을 주지 않는다) | art319_sec3_1.bodily_entry_required, art319_sec3_1.consent_and_coerced_consent, art319_sec3_1.open_public_place_entry |
| `legal_element.intent`(총칙13조 재사용) | — | art319_sec4.intent_against_resident_will |

**검수 필요 2 — 승낙(동의)을 24조 `doctrine.victim_consent_defeat`(Unlawfulness
DEFEAT)로 별도 재사용하지 않고 `trespass_entry` 자체의 legal_standard에 접어
넣었다.** 통설·판례(사실상평온설)는 주거침입에서 동의를 "양해"(구성요건해당성
조각)로 보고 24조 "승낙"(위법성조각)과 다른 층위로 취급한다 — 진정한 동의가 있으면
애초에 "사실상 평온을 해치는 태양"이 아니므로 `trespass_entry` 자체가 성립하지
않는다는 것. 배치⑩ 297조 검수 필요1(피해자 승낙="양해", 24조와 다른 층위)과 **정확히
같은 구조**의 두 번째 사례다(self-check6, 인접 대조).

**실행의 착수** — `legal_element.commencement_of_execution`(25조 재사용), "주거침입
고의로 문을 열거나 시정장치를 부순 때"(art319_sec3_2.attempt_door_opening, 긍정
standard) / "담장과 경비가 있는 공사현장 외곽에 들어간 것만으로는 부정"
(art319_sec3_2.attempt_construction_site_negative, 부정 standard) — 둘 다 canonical_
meaning을 손대지 않고 legal_standard 경계 사례로만 authoring 메모에 남긴다(불변성
원칙, 배치⑨-⑩과 동일 패턴).

**내부 이동 예외 — 별도 predicate 아님, A-2와의 경계 authoring 메모로 처리.**
"침입은 원칙적으로 외부로부터의 침입에 한정되어 이미 내부에 있는 사람은 퇴거불응죄만
문제되지만, 적법하게 들어간 뒤 독립적으로 구획되고 무상출입이 가능한 공간이 아닌 다른
공간으로 옮겨가면 침입이 될 수 있다"(art319_sec3_1.external_entry_and_partition_
exception)는 `trespass_entry`의 새로운 요건이 아니라 **A-1(주거침입)과 A-2(퇴거불응)
중 어느 OffenseDef가 적용되는지를 가르는 경계** — 독립 구획된 새 공간으로 이동하면
A-1(그 공간에 대한 신규 침입), 아니면 A-2(기존 공간에서의 퇴거불응)라는 authoring
메모로 두 offense 절 사이에 남긴다.

**위법성조각 — 신규 predicate 없음, 전부 20-23조 재사용 + 경계 확정.**

| 카드 | 재사용 predicate/doctrine | 비고 |
|---|---|---|
| lawful_authority_entry | `legal_element.act_pursuant_to_law`(20조) | 공법상·사법상 권한 불문 |
| socially_acceptable_entry, water_tank_repair_entry | `legal_element.act_not_against_social_norms`(20조) | 물탱크·수도관 수리 등 구체 사례는 legal_standard 경계 |
| lawful_labor_dispute_entry, labor_dispute_incidental_act | `legal_element.act_not_against_social_norms`(20조) | 적법 쟁의행위 및 그 부수행위 |
| labor_dispute_exclusive_occupation, labor_dispute_plant_occupation, labor_dispute_explicit_denial_entry (defeater 라벨) | 위 predicate의 **legal_standard 부정 경계**(전면적·배타적 점거, 구조조정 저지 목적 점거파업, 명시적 불허에도 불구한 출입) | 별도 DoctrineDef 아님(self-check2 — 이미 `act_not_against_social_norms`의 불충족으로 결론이 나는 사례, defeater 카드 라벨을 그대로 새 doctrine으로 승격하지 않는다) |
| justification.general | `doctrine.self_defense`(21조)/`doctrine.necessity_defeat`(22조) 원론적 재사용 | — |
| justification.emergency_escape, justification.fire_suppression | `doctrine.necessity_defeat`(22조) 구체 적용례 | 맹견·강도 회피, 화재 진화 |
| **self_help.right_holder_negative** | **`doctrine.self_help_defeat`(23조)를 319에는 적용하지 않는다는 명시적 배제 메모** | 아래 별도 설명 |

**"사법상 권리자라도 주거침입에는 자구행위를 할 수 없다"는 23조 doctrine의 새로운
requires가 아니라 319 offense 절에 남기는 배제 메모다.** 23조 `legal_element.
necessity_of_self_help`(이중의 보충성)가 주거침입 상황에서는 구조적으로 충족되기
어렵다는 판례의 반복된 결론을 predicate 자체의 정의를 바꾸지 않고 authoring 메모로
기록한다(23조 canonical_meaning 불변).

**범위 밖**: 죄수(주거마다 별죄 등)는 occurrence 단위 판단(9조 검수2 패턴 재적용).

### A-2. 퇴거불응 (부작위 — **진정부작위범, 18조 `omission_bundle` 미적용**)

**architecture 확인 — 18조 `bundle.omission_bundle`(배치② 확정, `ALL(duty_to_act,
possibility_to_act, failure_to_act, equivalence_to_commission)`)을 재사용하지
않는다.** 18조는 조문 문언("위험발생을 방지할 의무가 있는 자가 그 발생을 방지하지
아니한 때에는 그 발생된 결과에 의하여 처벌한다") 자체가 **부진정부작위범**(작위로
규정된 구성요건을 부작위로 실현하는 경우, 예: 부작위에 의한 살인)을 전제하고,
`equivalence_to_commission`(부작위가 작위와 동가치라는 평가)이 그 핵심 4번째
constituent다. 퇴거불응죄는 애초에 조문 자체가 "퇴거요구에 응하지 않음"이라는
부작위를 **1차 구성요건 행위로 직접 규정**한 **진정부작위범**이라 비교할 "작위
버전"이 없다 — `equivalence_to_commission`을 요구할 대상 자체가 없으므로 18조
bundle을 그대로 붙이면 채울 수 없는 slot이 생긴다. 이건 architecture gap이 아니라
**형법 도그마틱상 18조가 원래 진정부작위범에는 적용되지 않는다는 통설의 구조를
그대로 반영한 것**(자기 조문의 Elements를 직접 authoring, 배치③ "22·23조는 21조
구조를 복제" 같은 관계가 아니라 아예 별도 authoring) — 2패스에서 유기죄(271조)·
집합명령위반죄(145조) 등 다른 진정부작위범을 만나면 같은 원칙(18조 미적용, 독자
Elements)이 반복 적용될 것으로 예상한다(현재 배치 범위 밖, 참고 표시만).

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.dwelling_or_managed_premises_object`(위 공유 predicate 재사용) | — | art319_sec7_1 |
| `legal_element.retreat_demand_by_authorized_person`(신규) | 거주자·관리자 또는 점유자로부터 정당한 퇴거요구를 받았다(요구의 주체·절차가 적법해야 하며, 정당하지 않은 퇴거요구에 불응하더라도 퇴거불응죄는 성립하지 않는다) | art319_sec7_1.refusal_to_leave_elements, art319_sec7_3.justified_demand |
| `legal_element.no_justifiable_reason_for_refusal`(신규) | 그 퇴거요구에 불응할 정당한 사유가 행위자에게 없다 | art319_sec7_3.no_justifiable_reason |
| `legal_element.ability_to_comply_with_retreat_demand`(신규) | 행위자에게 퇴거요구에 응할 일반적·개별적 행위가능성이 있었다(객관적·주관적으로 응할 수 없거나 인간 일반 또는 행위자 개인에게 실현이 불가능하면 부정된다) | art319_sec7_3.ability_to_leave, art319_sec7_3.impossible_leaving(negative) |
| `legal_element.failure_to_comply_without_delay`(신규) | 퇴거요구를 받고도 유책하게 지체하며 즉시 퇴거하지 아니하였다 | art319_sec7_3.refusal_delay |
| `legal_element.intent`(총칙13조 재사용) | — | art319_sec7_4.intent |

**최초 진입의 적법성(art319.refusal_to_leave.lawful_or_mistaken_entry)은 퇴거불응
Elements의 항목이 아니라 A-1/A-2 사이의 offense 선택 경계다.** "처음에 적법하게 또는
과실로 들어간 사람"이라는 서술은 조문이 요구하는 별도 요건이 아니라, 애초에
불법하게(고의로 침입해) 들어간 사람이 그대로 남아 있는 것은 A-1(주거침입)로 이미
완전히 평가되고 A-2가 별죄로 추가되지 않는다는 죄수 설명이다(불가벌적 사후행위류
경계 — 9조 검수2/19조 패턴과 같은 occurrence-boundary 판단이지 퇴거불응 자신의
Elements가 아니다).

**범위 밖**: 미수(322조, 51개 조문 워크시트 범위 밖 — 300조와 달리 이번 배치
목록에도 없어 참조조차 하지 않는다).

---

## B. 제323조 권리행사방해

**구조 판단 — 진정신분범, 자기 소유물의 소유자만 정범이 될 수 있다(판례 명시,
Ⅱ.1 원문).** 이 조문이 각칙 predicate 사전에서 처음 다루는 **명시적 진정신분범**
사례라 33조(공범과 신분) architecture-compatibility 목록에 구체 사례를 추가한다(아래
HOLD절).

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.own_property_object`(신규) | 취거·은닉·손괴의 대상이 행위자 자신의 소유에 속하는 물건 또는 전자기록등 특수매체기록이다(동산·부동산을 모두 포함하고, 소유권 귀속은 민법상 물권변동 원칙에 따라 판정한다 — 부동산은 등기, 동산은 인도, 자동차·중기·건설기계 등 등록으로 소유권이 이전되는 물건은 등록 여부가 기준이며, 대금완납시까지 소유권을 유보하는 특약이 있어도 등기·등록이 마쳐지면 매수인 소유가 된다; 자기와 타인의 공유물, 공무소로부터 보관명령을 받았거나 공무소 명령으로 타인이 관리하는 자기의 물건, 소유·소지가 모두 금지된 금제품은 여기에 해당하지 않는다; 법인의 대표기관이 그 직무집행으로 취거 등 행위를 한 경우 및 대표기관이 아닌 대리인·지배인이 직무권한 범위 내에서 한 경우에는 법인 소유물도 "자기의 물건"으로 본다) | art323_sec2_2.coowned_property_excluded, prohibited_gold_products_excluded, property_movables_real_estate, registered_sale_seller_not_subject, official_custody_exception |
| `legal_element.third_party_possession_or_right_object`(신규) | 그 물건 또는 특수매체기록이 타인의 점유의 목적이 되어 있거나 타인의 권리(점유를 수반하지 않는 채권 포함, 제한물권 또는 채권)의 목적이 되어 있다(공동점유물도 포함하고, 법인이 설치·운영하는 전산망 시스템의 전자기록등은 그 법인의 임직원과의 관계에서 "타인"의 것에 해당한다; 절도범인의 점유처럼 점유할 권리 없음이 외관상 명백한 점유는 여기의 "타인의 점유"에 포함되지 않으나, 적법한 원유에 기해 점유를 개시한 이상 그 후 점유권원을 상실하거나 권원 존부가 법정절차로 밝혀질 때까지의 점유, 동시이행항변권에 기한 점유는 포함된다) | art323_sec2_2.joint_possession_object, corporate_system_records_other, manifestly_no_right_possession_excluded |
| `legal_element.taking_conduct`(취거, 신규) | 점유자의 의사에 반하여 목적물을 그 지배로부터 자기 또는 제3자의 지배로 옮겼다(점유자의 의사 또는 하자 있는 의사에 기하여 점유가 이전된 경우는 여기에 해당하지 않으나, 기망으로 상대방이 착오에 빠진 틈을 타 가져가는 책략취거는 포함되고, 부동산에 대한 취거도 인정된다; 불법영득의사를 요하지 않는다는 점에서 절도죄의 절취와 구별된다) | art323_sec2_3.consensual_transfer_not_taking |
| `legal_element.concealment_conduct`(은닉, 신규) | 타인의 점유 또는 권리의 목적이 된 자기 물건 등의 소재를 발견하기 불가능하게 하거나 현저히 곤란한 상태에 두었다(자기가 점유하는 물건을 권리자의 지배영역에서 반출해 가는 행위도 포함될 수 있다) | (원문, Ⅱ.3 — 대응 카드 없음) |
| `legal_element.damage_conduct`(손괴, 신규) | 물건의 전부 또는 일부에 대하여 그 용익적 또는 가치적 효용을 해하였다(물리적 훼손은 물론 기타 방법으로 효용을 해하는 것도 포함한다) | (원문, Ⅱ.3 — 대응 카드 없음) |
| `legal_element.obstruction_of_right_exercise`(신규) | 위 행위로 인하여 타인의 권리행사가 방해될 우려가 있는 상태에 이르렀다(현실로 권리행사가 방해되었을 것을 요하지 않는 추상적 위험범이다) | (원문, Ⅰ.3, Ⅱ.3 — 대응 카드 없음) |
| `legal_element.intent`(총칙13조 재사용) | — | art323_sec3.subjective_awareness |

**검수 필요 3 — `concealment_conduct`/`damage_conduct`를 366조(재물손괴)의
`legal_element.utility_impairment`와 같은 predicate로 재사용하지 않고 신규로
만들었다.** 323 원문 스스로 "은닉이란... 손괴죄에서 행위 태양 중 하나로 규정하고
있는 은닉과 **유사한** 개념이다", "손괴는... 손괴죄의 손괴와 **유사한** 개념이다"라고
서술한다 — "동일"이 아니라 "유사"라는 표현 자체가 판례 문언 수준에서는 겹치되,
소속된 legal effect가 다르다는 신호다: 366의 `utility_impairment`는 **타인 소유
재물**에 대한 효용침해 자체가 결과(재물손괴죄)인 반면, 323의 은닉·손괴는 **자기
소유물**에 대한 행위이고 결과도 "효용침해"가 아니라 "타인의 권리행사방해"(위험범)다.
`shared-predicate-canonical-meaning-is-immutable` 원칙에 따라 겉보기 유사성만으로
366 predicate를 재사용하지 않는다(self-check6, 인접 대조 결과 — 재사용 아님으로
확정, 366의 판례 정의를 참고 자료로만 인용).

**검수 필요 4 — 취거/은닉/손괴 3갈래를 분해하지 않고 병합할지 여부.** 원문
Ⅵ.1은 "하나의 객체를 취거하여 은닉하거나 손괴해도 포괄하여 단순 일죄"라고 해
세 행위가 같은 결과에 대한 대체 수단임을 시사하지만, 배치⑦의 뇌물 5행위태양
분해 선례(수수/요구/약속/공여/의사표시를 별도 leaf로)를 따라 **3개를 별도
legal_element로 분해**했다(v0 판단) — coercive_conduct(폭행/협박)처럼 병합한
사례와 달리, 취거(점유이전)·은닉(소재불명화)·손괴(물리적 효용침해)는 서로 다른
사실관계를 요구하고 공통된 "정도 판단"(degree-sufficiency test)으로 수렴하지
않기 때문(self-check1 적용 결과, coercive_conduct와 반대 결론).

**공범 — architecture-compatibility 신규 발견, 33조 본문 목록에 구체 사례 추가.**
"물건의 소유자가 아닌 사람은 형법 제33조 본문에 따라 소유자의 권리행사방해 범행에
가담한 경우에 한하여 공범이 될 수 있다"(원문 Ⅴ, 2022도5827·2017도4578)와 "권리행사
방해죄의 공범으로 기소된 물건의 소유자에게 고의가 없는 등으로 범죄가 성립하지
않는다면 공동정범이 성립할 여지가 없다"(2017도4578 — 정범인 소유자가 무죄면
비신분자는 단독으로도 공동정범이 될 수 없다)는 배치⑤(33조) v1 정정1이 이미 철회한
"attributable_slots로 신분 predicate를 전이시켜 해결"이 왜 안 되는지의 **구체
offense 사례**다: 소유자 무죄 → 비신분자도 자동으로 무죄가 되는 구조는 신분
predicate의 진실값을 전이시키는 방식으로는 표현할 수 없고(전이시키면 오히려 반대
방향, 즉 비신분자도 "소유자"가 되어버리는 오류), 정범의 성립 자체에 종속되는 별도
경로가 필요하다는 걸 재확인한다. 33조 본문 공동정범 항목(기존 HOLD)에 두 번째 구체
사례로 추가한다(신규 유형 아님).

**간접정범 — 신규 없음, 34조 일반원칙으로 커버.** "피고인이 아들에게 도어락 비밀번호
변경을 지시했으나 아들 자신도 소유자가 아니어서 아들의 정범 성립 자체가 안 되고,
따라서 교사자인 피고인도 권리행사방해교사죄가 성립할 수 없다"(2022도5827, 원문
Ⅱ.1)는 297/298 유형(피이용자=피해자, 방향 반대)과 다르다 — 이건 그냥 "정범(피이용자)
불성립 → 교사범도 불성립"이라는 **파생책임의 표준 종속 구조**(33조 본문 교사·방조
경로, `principal_realization_truth` 3치 판정이 이미 지원)이지 34조가 미해결로 남긴
"방향 반대" 문제가 아니다 — 298/257과 혼동하지 않는다(self-check6).

**범위 밖**: 공무상보관물무효죄(142조)·준점유강취죄(325조 2항)·강요죄 흡수(법조경합)·
장물죄 본범 해당 여부는 전부 cross-offense 경계, 51개 조문 범위 밖(142·325는 워크시트
대상 아님, 365는 328절에서 준용조문으로만 언급). 죄수(권리자별 별죄, 상상적 경합,
art323_Ⅵ.2)는 occurrence 단위 판단 — 328절의 "수인 소유자 전원 기준" 카드와 바로
연결되므로 아래 C절에서 다시 인용.

---

## C. 제328조 친족간의 범행 (친족상도례)

**카드가 조문의 핵심 규정(1항 형면제·2항 친고죄) 자체를 담고 있지 않다 — 원문에서
직접 authoring한다(배치⑧ 239조가 238조를 직접 열람한 것과 같은 3단계 방법론).**
카드 6개는 전부 세부 적용 경계(인적 범위·시적 범위·특별법 배제)이고, 핵심 규정
자체는 원문(Ⅰ-Ⅱ절)에만 있다.

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.kinship_status_within_statutory_range`(신규) | 행위자와 재산범죄의 피해자(재산범죄 유형에 따라 소유자·점유자·위탁자 등으로 세분, 아래 별도 설명) 사이에 직계혈족·배우자·동거친족·동거가족 또는 그 배우자, 혹은 그 밖의 친족관계가 민법이 정한 친족의 범위(8촌 이내의 혈족, 4촌 이내의 인척, 배우자) 내에서 존재한다(친족관계의 존부는 행위 시를 기준으로 판단하되 인지의 소급효 등 민법상 효과를 그대로 반영하며, 행위자가 그 친족관계를 인식하였는지는 묻지 않는다) | art328_sec3_1.kinship_effective_range, 원문 Ⅲ-Ⅴ |
| `doctrine.close_kin_property_offense_exemption`(신규, Punishability EXEMPT) | 위 predicate가 "직계혈족·배우자·동거친족·동거가족 또는 그 배우자"(328조 1항 범위)에 해당하고 적용대상 재산범죄(절도·사기·공갈·횡령·배임 및 그 미수 — 강도·손괴 제외)이면 형을 면제한다 | 원문 Ⅰ.1, Ⅱ.1 |

**필수 확인 — `close_kin_property_offense_exemption`(328조 1항)은 현재 헌법불합치로
시행이 중지된 상태다(2025.12.31.까지 개선입법 요구, 그 시한까지 적용 중지 — 헌재
2024.6.27. 2020헌마468 등).** 이 배치를 저작하는 시점(2026-08-09)은 이미 그 시한을
지났으나, 개선 입법이 실제로 어떤 내용으로 시행되었는지(그대로 폐지/범위 축소/절차
추가 등)는 이 워크시트의 원천 주석서(작성 시점 기준 자료)에 반영되어 있지 않다.
predicate 자체(신분관계 기반 EXEMPT 구조)는 헌재 결정이 지적한 문제(형사피해자
재판절차진술권 침해)가 "일률적 강제 EXEMPT" 자체에 있었다는 점에서 구조적으로는
유지될 가능성이 높지만, **v0은 이 조문의 현재 유효 범위를 확정하지 않고 사용자
확인이 필요한 HOLD로 명시한다**(2패스 착수 전 확정 필요 — 실정법 상태 확인 문제이지
DSL 구조 문제가 아니다).

**328조 2항(먼 친족 — 친고죄)은 predicate 사전 범위 밖이다.** 소추조건(고소)은
형사소송법 사항으로, 36조(누범 절차규정)·300조(성폭력처벌법 특별법 가중)와 같은
이유로 이미 확립된 "이 DSL은 법적 상태만 다루고 소송절차·소추요건은 다루지
않는다" 원칙을 그대로 적용한다(HOLD 아님, 애초에 대상 아님).

**"피해자" 식별은 재산범죄 유형마다 달라진다 — `kinship_status_within_statutory_
range`는 조문 재사용 시 파라미터가 필요한 정의다.**

- 절도: 재물의 소유자 및 점유자 **쌍방**과 친족관계 필요(art328_sec4_1.multiple_
  owners_all_kinship이 "소유자가 수인이면 전원과" 요건도 함께 규정).
- 횡령·배임: 소유자·위탁자 **쌍방**과 친족관계 필요(art328_sec4_1.embezzlement_
  breach_trust_owner_entrustor).
- 사기: 재물을 편취당한 피해자와만 필요, 피기망자(법원 등)와는 불요.
- 공갈: 피공갈자·재물교부자 **양자** 모두와 필요(통설).
- 장물(365조, 51개 조문 범위 밖): 장물범과 피해자 사이(1항), 장물범과 본범 사이(2항)
  각각 별도 신분관계.
- 323조(권리행사방해) 자체는 328조가 준용되지 않는다(강도·손괴와 함께 준용 배제
  목록에 있음, 원문 Ⅰ.1) — B절의 "권리자별 별죄, 상상적 경합"(art323_Ⅵ.2)은
  **친족상도례가 적용되지 않는 채로** 그대로 유지되는 죄수 판단이라는 뜻이지, 328과
  결합되는 사례가 아니다(오분류 주의 — self-check6).

이 갈래별 "피해자 식별" 차이는 328조 자신의 predicate를 조문마다 다시 정의하는 게
아니라(canonical_meaning 불변), **2패스에서 344·354·361·365조(모두 51개 조문
워크시트 범위 밖 — 재산죄 core pilot의 329·333·347·350·355·357·366과도 다른
조문임에 주의)를 실제로 저작할 때 이 predicate를 어떤 "피해자" 슬롯에 바인딩할지
결정하는 문제**로 authoring 메모에 남긴다.

**night_burglary_resident_kinship_exception — 330조(51개 조문 범위 밖, 배치⑫
대상) 저작 시 재확인 필요.** 야간주거침입절도죄에서 주거자도 피해자이지만
`kinship_status_within_statutory_range`는 재물의 소유자·점유자 차원에만 적용되고
주거자-행위자 관계에는 적용되지 않는다는 카드다 — 328 자신의 predicate 정의를
바꾸는 내용이 아니라 330조가 이 predicate를 "누구와의 관계에" 바인딩하는지에 대한
경계이므로, 배치⑫에서 330조를 저작할 때 다시 열어 확인한다(HOLD 아님, 지금은
참고 표시만 — 정의는 이미 명확하다).

**disabled_victim_abuse_crimes_no_application — `NOT()` 게이팅으로 표현, 신규
doctrine 아님.**

```text
ground_fact.disabled_victim_abuse_property_crime_status(신규)
    2022. 1. 28. 이후 범하여진 장애인복지법 제2조 제4항 제11호·제12호의
    장애인학대관련범죄(형법 제347·347의2·348·350·350의2·352조, 제355·356·357조)에
    해당한다(사실 확인 — 시행일자·특정 조문 해당 여부는 법적 평가라기보다 시점·
    분류 확인에 가까워 ground_fact로 분류한다)

doctrine.close_kin_property_offense_exemption(및 328조 2항 친고죄 상당 부분, 준용
조문 authoring 시)의 requires에 NOT(disabled_victim_abuse_property_crime_status)를
추가한다 — 배치⑩ 133①의 NOT(bribe_promise) 게이팅 패턴과 동일.
```

**special_property_crime_no_exclusion — 신규 predicate 아님, 범위 확인 메모.**
"재산범죄를 가중처벌하는 특별법에서도 형법상 재산범죄의 성질이 유지되면 명시적
배제 규정이 없는 한 친족상도례가 적용된다"는 이 DSL이 형법전 51개 조문만 모델링하고
특별법 조문 자체를 `offense_ref`로 갖지 않는 이상 predicate 사전에서 별도로 다룰
대상이 없다(배치⑨·⑩의 "특정강력범죄·성폭력처벌법 가중은 특별법, 범위 밖" 원칙
재적용).

---

## HOLD/architecture-compatibility 종합 (2패스 착수 전 확인 목록에 추가)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례, 257·298조
자상·도구 간접정범, 250조 비신분자 존속살해 가담, 301조 결합범+결과적가중범 병존,
299조 예비음모 conduct 갈래 제한)에 이번 배치로 다음이 추가된다:

1. **art323 소유자 아닌 자의 가담 ↔ 33조 본문 공동정범 gap** — 배치⑤ v1 정정1이
   이미 원칙적으로 확인한 "attributable_slots로 신분 predicate를 전이시키는 방식은
   틀렸다"는 결론의 **구체 offense 사례**(2017도4578: 정범인 소유자가 무죄면
   비신분자는 단독으로도 공동정범 성립 불가). 신규 유형 아님, 기존 HOLD 항목의
   구체화.
2. **art328① 헌법불합치·시행중지 상태 확인** — DSL 구조 문제가 아니라 원천
   실정법의 현재 유효 범위 확인 문제. predicate 구조(kinship_status +
   Punishability EXEMPT doctrine)는 그대로 준비해두되, 2패스 착수 전 사용자가
   현재 시행 상태(개선입법 반영 여부)를 확인해야 한다.
3. **art319 계절적 미사용 별장의 "주거→건조물" 서브타입 재분류** — 단일
   `dwelling_or_managed_premises_object`로 표현 가능한지, 아니면 서브타입 분리가
   필요한지 2패스 실제 저작 시 확인(위 검수 필요 1, gap이 아니라 구조 선택 문제).

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 전부 기존 `LegalElementDef`/`GroundFactDef`/`DoctrineDef`(20-24조 재사용)/
25조 Completion predicate/33조 architecture-compatibility 목록(신규 항목 추가일 뿐
스키마 변경 아님)/`NOT()` 게이팅으로 표현된다. 이번 배치의 방법론적 특징은 새
primitive가 아니라 **두 가지 구조 판단**이었다 — (1) 18조 `omission_bundle`이
진정부작위범(퇴거불응)에는 애초에 적용 대상이 아니라는 도그마틱 경계 확인, (2)
366조 `utility_impairment`와 323조 은닉·손괴가 판례 문언은 "유사"하지만 canonical
정의를 공유하지 않는다는 self-check6 결과. 둘 다 기존 스키마로 문제없이 표현되고,
어느 쪽도 새 top-level kind나 필드를 요구하지 않는다.

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입 결과)

1. **카드 분해**: 323조 "취거, 은닉 또는 손괴"를 배치⑦ 뇌물 5행위태양 분해
   선례를 따라 3개 별도 leaf로 분해(검수 필요 4). 319조 "침입"은 신체적 침입·
   객관적 평온침해 기준·동의 경계를 하나의 `trespass_entry`로 유지(폭행/협박
   병합 선례와 같은 근거 — 세 요소가 같은 "사실상 평온 해치는 태양" 판단으로
   수렴).
2. **doctrine 자격 검사**: 319조 승낙(양해)을 24조 doctrine으로 만들지 않고
   Elements negative로 정리(검수 필요 2, 297 검수1과 동일 구조). 323조 labor
   dispute defeater 카드들을 별도 DoctrineDef로 만들지 않고 기존 `act_not_
   against_social_norms`의 legal_standard 경계로 정리.
3. **긍정형 이름**: 이번 배치 신규 predicate id 중 `not_`/`no_`/`non_` 접두는
   없다(`no_justifiable_reason_for_refusal`은 "불응할 정당한 사유가 없다"는
   사실 자체를 긍정 서술한 이름이지 다른 predicate의 부정형이 아니다 — 배치⑦
   `self_benefit_purpose`류와 같은 처리).
4. **`ONE_OF` 사용 전 배타성 증명**: 이번 배치에서 `ONE_OF`를 쓴 곳이 없다.
   319조 A-1/A-2(주거침입/퇴거불응)는 `ONE_OF`가 아니라 별도 OffenseDef이고,
   그 경계(최초 진입의 적법성)는 offense 선택 authoring 메모로 처리했다(cross-
   offense 경계 원칙 재확인, doctrine이나 CompletionPolicy 겹침 문제가 아니므로
   exact-one 검증 대상 자체가 아님을 확인).
5. **CompletionPolicy state 반례 대입**: 이번 배치는 CompletionPolicy 신규
   state가 없다(319 A-1의 미수만 25조 재사용, A-2·323·328은 미수 카드 자체가
   없어 손대지 않았다) — 해당 없음.
6. **일반원칙 서술 전 인접 대조**: 319 승낙(양해) ↔ 297 승낙(양해)을 대조해
   같은 구조 확인(검수 필요 2). 323 은닉·손괴 ↔ 366 손괴를 대조해 canonical_
   meaning 불공유를 확인(검수 필요 3). 323 간접정범(2022도5827) ↔ 257/298
   간접정범을 대조해 **다른 유형**(방향 반대 문제 아니라 표준 종속 구조)임을
   확인하고 34조 HOLD 목록에 잘못 추가하지 않았다.
7. **stage 라벨-설명 일치**: `doctrine.close_kin_property_offense_exemption`을
   151조와 같은 근거(통설상 인적 처벌조각사유)로 처음부터 Punishability EXEMPT로
   확정(Culpability DEFEAT와 혼동한 배치⑦ v1 오류를 반복하지 않았다).

---

## 다음 세션 시작점 — 배치⑫ 절도·강도 나머지 (330·331·332·334·335·337·338·342·343·344·356·360조)

배치⑪의 art323 검토가 이미 짚어둔 대로, 330조(야간주거침입절도) 저작 시 328조
`kinship_status_within_statutory_range`의 "주거자-행위자 관계 불요" 경계(위 C절)를
반드시 재확인할 것. 344·354·361·365조는 이번 12개 목록에 없다 — 328조가 준용을
전제하는 조문들이지만 51개 조문 워크시트 범위 밖이므로, 328조 predicate가 실제
COMPOSE/참조되는 지점은 2패스 정의 조립 단계에서 각 조문을 직접 저작할 때다(배치⑫
목록에도 없으므로 이 예정 사실만 기록).
