# Predicate 사전 확장 — 배치 ⑫ 절도·강도 나머지 (제330·331·332·334·335·337·338·342·343·344·356·360조) v0

[`predicate-authoring-self-check-checklist`](메모리, 7항목 + 배치⑧-⑪이 추가한 원칙들)를
제출 **전**에 직접 대입했다 — 문서 끝 "self-check 적용 메모" 절에 항목별 결과를 남긴다.
방법론은 배치⑦-⑪과 동일(카드 1차, 원문 주석은 모호할 때만 보조).

**이번 배치의 특징 — 12개 조문 전부가 재산죄 pilot(329 절도·333 강도·355 횡령)의
가중유형·결합범·참조조문이라 신규 legal_element보다 "base offense를 어떻게 재사용하는
DerivedOffenseDef로 조립하는가"가 핵심 쟁점이다.** 순서대로: D(절도 가중유형군,
329 재사용) → E(강도 가중유형군, 333 재사용) → F(준강도, 절도+강도 결합) →
G(강도 결합범군, 강도+상해/살인) → H(미수·예비 참조조문) → I(친족범행 준용,
population 대상 아님) → J(횡령 가중·독립유형, 355 재사용).

---

## D. 절도 가중유형군 (제330·331·332조) — 329(절도) 재사용

### D-0. 재사용 대상 확인 (재산죄 pilot v0/v2, `predicate_dictionary_draft_v{0,2}.md`)

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.possession`(329) | 형법상 점유는 사실상 지배(물리적 요소) + 점유의사(정신적 요소)로 성립한다 | pilot A-2 |
| `ground_fact.taking_conduct`(329) | 타인 점유 재물을 그 점유자의 의사에 반해 자기(제3자) 점유로 옮겼다 | pilot A-2 |
| `legal_element.unlawful_appropriation_intent`(전역, 절도·강도·횡령 공유) | 권리자를 배제하고 경제적 용법에 따라 이용·처분할 의사(불법영득의사)가 인정된다 | pilot A-1, draft_v1 §1 |
| `legal_element.commencement_of_execution`(25조, 전역) | 구성요건적 행위(또는 그 직접적 행위)를 개시하였다(실행의 착수) | draft_v1 §4 |
| `legal_element.intent`(13조, 전역) | — | 배치② 확정 |
| `legal_element.dwelling_or_managed_premises_object`(319조, 배치⑪) | 사람의 주거, 관리하는 건조물·선박·항공기 또는 점유하는 방실에 해당한다 | 배치⑪ A절 |

**검수 필요 D-0-1 — 329조 자체에 취거(taking_conduct) 외에 "재물"(객체) predicate가
pilot 표에 명시적으로 없다.** pilot A-2가 `legal_element.possession`(점유 성립요건)만
등재하고 "타인 소유·타인 점유의 재물"이라는 객체 predicate 자체는 별도 id로 확정해두지
않은 것으로 보인다 — 배치⑫는 이 공백을 새로 메우지 않고(재산죄 pilot 확정 사항은
불변), 330·331·332가 329의 객체 요건을 그대로 물려받는다는 사실만 authoring 메모로
남긴다(2패스에서 329 자체를 조립할 때 명시적으로 확정될 사항).

### D-1. 제330조 야간주거침입절도 — 결합범(319 주거침입 + 329 절도 + 야간)

**구조 판단 — `DerivedOffenseDef`, base 없이 세 요소의 COMPOSE.** 판례(2011도300)가
확정한 대로 "주거침입"이 주간이면 성립 자체가 안 되므로(부분적 재구성이 아니라
전면 불성립), 319의 `trespass_entry`(배치⑪ A-1)를 그대로 요건으로 흡수한다.

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.nighttime`(신규) | 일몰 후부터 일출 전까지의 시간대에 해당한다(천문학적 해석 — 통설·판례) | art330_Ⅱ(원문, 대응 카드 없음) |
| `legal_element.dwelling_or_managed_premises_object`(319 재사용) | — | art330_Ⅲ |
| `legal_element.trespass_entry`(319 재사용) | — | art330_Ⅲ |
| `ground_fact.taking_conduct`(329 재사용) | — | art330_sec5.completion-at-theft-completion |
| `legal_element.unlawful_appropriation_intent`(전역 재사용) | — | (329 재사용) |
| `legal_element.intent`(13조 재사용) | — | (전역 재사용) |

**야간의 판정 시점 — 침입 기준(주거침입기준설), authoring 메모로 확정.** 원문
Ⅰ이 소개하는 세 학설(주거침입기준설/절도기준설/양자모두요구설) 중 판례(2011도300)가
채택한 주거침입기준설을 그대로 따른다 — `nighttime`은 `trespass_entry`(침입행위)의
시점에 걸리는 조건으로 `requires`에 결합하고, `taking_conduct`(절취)의 시점과는
무관하다. 이건 신규 predicate 관계가 아니라 `ElementExpression`에서
`ALL(nighttime AT trespass_entry, trespass_entry, taking_conduct, ...)`처럼 같은
predicate가 서로 다른 시점에 결합되는 문제라, 시점 바인딩 방식은 2패스에서
확인한다(구조 선택 문제 — 아래 HOLD 목록 참고).

**CompletionPolicy — 착수는 침입시, 기수는 절취완료시(카드 정면 확정).**

```text
ATTEMPTED.when  = commencement_of_execution(trespass_entry 기준)
COMPLETED.when  = taking_conduct(절취행위 완료)
```

침입이 미수에 그쳐도(침입 자체가 미완성) 절취가 기수에 이르면 330조 기수가 된다는
카드(art330_sec5)와 원문 Ⅴ의 서술을 그대로 반영 — 침입의 기수·미수는 330조
자신의 완성 여부와 무관하다(침입은 "착수 판단"에만 쓰이고 "완성 판단"에는 관여하지
않는 비대칭 구조). 미수 처벌은 342조(H절) 참조.

### D-2. 제331조 특수절도 — 1항(손괴+D-1) / 2항(흉기·합동+329)

**1항 — D-1(야간주거침입절도) + 손괴, `DerivedOffenseDef` 가중.**

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.damage_to_entry_barrier`(신규) | 문이나 담 그 밖의 건조물의 일부(잠금장치·통상의 방법으로 열 수 없도록 장치한 시설물 포함, 위장 목적의 도랑 등 포함)를 물리적으로 훼손하여 그 효용을 상실시켰다(단순히 넘어가거나 창틀에서 분리하는 등 물리적 훼손 없이 효용만 해하는 경우, 또는 열쇠로 통상의 용법에 따라 여는 경우는 제외된다) | art331_Ⅱ.1, Ⅱ.2(원문, 대응 카드 없음) |

```text
331_para1.requires = ALL(damage_to_entry_barrier, dwelling_or_managed_premises_object,
                          trespass_entry, taking_conduct, unlawful_appropriation_intent,
                          intent)
```

`nighttime`은 1항 요건에서 제외한다 — 원문 Ⅳ.2가 "제1항의 죄는 주거침입과 절도의
결합범이며 손괴는 주거침입의 유형적 방법"이라고 명시하되, 야간·주간 구분 없이
손괴+침입+절취이면 1항이 성립한다고 서술한다(주간 손괴침입절도도 1항 대상 —
D-1과 달리 야간이 구성요건이 아니라 별도 가중경로임에 주의, self-check6 인접 대조).

**2항 — 흉기휴대 또는 2인 이상 합동, D-1(야간)과 무관하게 329(단순절도) 가중.**

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.dangerous_weapon_carriage`(신규, 배치⑨ 258의2 `dangerous_object_carriage`와 별개 확정 — 아래 검수 필요 D-2-1) | 본래 살상·파괴용으로 만들어졌거나 이에 준할 정도의 위험성을 가진 물건을 몸 가까이 소지하여 즉시 사용할 수 있는 상태에 두었다(용도·크기·모양·개조 여부·구체적 사용 방법 등을 종합해 사회통념상 객관적으로 판단하며, 고체뿐 아니라 액체·기체도 포함될 수 있으나 개조되지 않은 통상의 공구는 제외될 수 있다; 상대방이 이를 인식하거나 제시할 것을 요하지 않는다) | art331_sec3_1.toy_gun_not_weapon_exception, art331_Ⅲ.1, Ⅲ.2 |
| `legal_element.joint_commission_by_two_or_more`(합동범, 신규) | 2명 이상이 시간적·장소적으로 협동관계를 이루면서 절취의 실행행위를 분담하였다(현장에서 직접 실행행위를 분담한 자는 물론, 3명 이상이 공모한 후 그중 2명 이상이 현장에서 협동관계를 이루며 실행행위를 분담한 경우에는 현장에 없는 공모자도 그 실행정범의 행위를 자기 의사 실현수단으로 하였다고 평가할 정범성 표지를 갖추면 포함된다 — 현장적 공동정범설, 98도321 전합) | art331_Ⅲ.3 |

**흉기 정의 exception — 별도 predicate 아님, canonical_meaning에 이미 반영.**
카드(toy_gun_not_weapon_exception, "객관적으로 흉기의 성질을 가져야 하므로 장난감
권총을 흉기처럼 가장한 경우에는 흉기가 아니다")는 `dangerous_weapon_carriage`의
정의를 부정하는 반례가 아니라 그 정의 자체("객관적으로 위험성을 가진 물건")의
경계 사례다 — positive-predicate 원칙(다른 predicate의 논리적 부정인지 확인)에
따라 별도 exception legal_element를 만들지 않는다.

**검수 필요 D-2-1 — `dangerous_weapon_carriage`를 배치⑨ 258의2(특수상해)
`dangerous_object_carriage`와 같은 predicate로 재사용할지, 별도로 둘지.**
CURRENT.md(배치⑨ 절)는 258의2의 `dangerous_object_carriage`를 "전역 재사용
후보"로 명시해뒀다. 331조 2항의 "흉기"("살상용·파괴용으로 만들어진 것이거나
이에 준할 정도의 위험성")와 258의2의 "위험한 물건"이 canonical_meaning 수준에서
동일한 법적 판단인지(판례 문언·심사기준이 겹치는지) 확인이 필요하다 — v0은
안전하게 별도 id로 잠정 등재하되, 두 조문의 판례 기준 문구를 대조하면 결론이
날 수 있는 성격의 질문이라 신규 architecture 이슈로 승격하지 않는다(배치⑧
"재사용 가능성을 없는 schema typing 문제로 격상하지 않는다" 원칙 재적용, 확인만
필요).

**합동범의 본질 — 현장설(통설·구 판례) vs 현장적 공동정범설(현 판례) 중 후자로 확정,
HOLD 아님.** `joint_commission_by_two_or_more`의 canonical_meaning에 이미 98도321
전합의 "현장에 없는 공모자도 정범성 표지를 갖추면 포함"을 반영해뒀다 — 이건 30조
공동정범의 일반 법리(`joint_execution_intent`/`joint_execution_conduct`, 배치②
확정)의 특수 적용이지 새 participation mode가 아니다. 다만 **이 predicate가 30조
predicate와 재사용 관계인지, 아니면 "현장성"이라는 331조 2항 고유 요건이 추가된
독립 legal_element인지는 아래 HOLD 목록에 architecture-compatibility 후보로
추가한다** — 판례가 "공동정범의 일반 이론에 비추어"라고 명시하면서도 "현장에서
협동관계"라는 331조 2항 특유의 제한을 요구하는 이중 구조라, 30조 predicate를
그대로 가져다 쓰기엔 부족하고 완전히 새 predicate로 두기엔 30조와 무관하다고
말하기도 어렵다.

**CompletionPolicy — 1항은 손괴 개시시 착수·절취완료시 기수(카드 정면 확정), 2항은
물색행위시 착수(원문 Ⅳ.2).**

```text
331_para1: ATTEMPTED.when = commencement_of_execution(damage_to_entry_barrier 기준)
           COMPLETED.when = taking_conduct
331_para2: ATTEMPTED.when = commencement_of_execution(taking_conduct 착수, 즉 물색행위)
           COMPLETED.when = taking_conduct(완료)
```

1항·2항 요건을 함께 사용한 경우(흉기 휴대 + 야간 손괴침입) 포괄일죄로 하나의
특수절도만 성립한다는 원문 Ⅳ.1은 죄수 판단(occurrence 단위)이라 predicate 사전
범위 밖(9조 검수2 패턴 재적용).

### D-3. 제332조 상습절도 — 329/330/331의 신분 가중(부진정신분범), `DerivedOffenseDef`

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.habitual_theft_propensity`(상습성, 신규) | 행위자의 연령·성격·직업·환경·전과, 범행의 동기·수단·방법·장소, 전과와의 시간적 간격, 범행 내용의 유사성 등을 종합할 때 동종의 절도 행위(단순절도·야간주거침입절도·특수절도 및 그 미수, 자동차등불법사용을 포함)를 반복누행하는 습벽이 인정된다(죄종을 달리하는 강도·사기 등의 전력은 절도 습성의 근거가 되지 못하고, 수회의 전과·범행이 있어도 그것이 모두 우발적 동기 또는 급박한 경제사정에서 비롯된 것으로서 습벽의 발현으로 보기 어려우면 인정되지 않으며, 반대로 단 1회의 범행이라도 과거 범행경력에 비추어 습벽이 인정되면 상습범이 성립한다) | art332_sec1_1.different_offense_types, art332_sec1_2.incidental-or-economic-theft-exception, art332_Ⅰ.2 |

```text
332.base_offense = ANY(329 절도, 330 야간주거침입절도, 331 특수절도)
332.requires = ALL(base_offense.requires, habitual_theft_propensity)
```

**구조 판단 — base offense 종류에 따라 법정형·offense_ref가 분기하는 첫 사례
(335 준강도와 같은 급의 architecture 확인사항, 아래 HOLD).** 329/330/331 중
가장 법정형이 중한 죄의 상습범(예: 특수절도와 단순절도를 함께 반복했으면 상습
"특수"절도 하나의 포괄일죄, 원문 Ⅳ.5)으로 수렴한다는 판례를 그대로 반영하려면
`DerivedOffenseDef`가 여러 base offense 후보 중 사실관계에 따라 하나를 선택하고
그 선택이 법정형(적용 조문)을 결정하는 구조가 필요하다 — 이게 기존 8차 addendum
`derivative_mode`로 표현 가능한지, 아니면 orchestrator(Step 7) 수준의 별도 로직이
필요한지는 v0에서 확정하지 않는다(D-2-1과 별개로 335조 절에서 다시 다룬 뒤 종합
정리, 아래 HOLD 목록 참고).

**공범 — 상습범 신분은 "행위자 정형" 요소, 33조 통설/판례 대립 그대로 이월.**
원문 Ⅲ이 소개하는 대로 판례는 33조 본문으로 비상습자에게도 공범 성립을
인정하되 단서로 처단형만 낮추는 입장이다 — 이건 33조 본문/단서의 기존 일반
구조(배치⑤ 확정)를 그대로 적용하는 사례이지 신규 architecture 문제가 아니다.

**CompletionPolicy — base offense의 completion을 그대로 따른다(가중 요소가
completion 자체를 바꾸지 않음).**

**범위 밖**: 특정범죄가중처벌법 제5조의4(2016.1.6. 삭제) 관련 서술은 형법전
51개 조문 범위 밖(배치⑨·⑩·⑪이 반복 확인한 "특별법은 predicate 사전 대상 아님"
원칙 재적용).

---

## E. 강도 가중유형군 (제334조) — 333(강도) 재사용

### E-0. 재사용 대상 확인

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.robbery_level_violence`(333) | 폭행·협박이 재물탈취의 수단으로 반항을 억압할 정도에 이르렀다 | pilot A-2 |
| `legal_element.unlawful_appropriation_intent`(전역 재사용) | — | pilot A-1 |

**검수 필요 E-0-1 — 333조 predicate 표에 "재물 또는 재산상 이익 취득" 자체의
객체 predicate가 D-0-1과 마찬가지로 명시돼 있지 않다.** 같은 공백, 같은 처리
(2패스에서 333 조립 시 확정).

### E-1. 제334조 특수강도 — 1항(야간주거침입강도) / 2항(흉기·합동강도)

**1항 — 319(주거침입) + 333(강도), D-1과 대응 구조.**

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.nighttime`(D-1 재사용) | — | art334_Ⅰ |
| `legal_element.dwelling_or_managed_premises_object`(319 재사용) | — | art334_Ⅰ |
| `legal_element.trespass_entry`(319 재사용) | — | art334_Ⅰ |
| `legal_element.robbery_level_violence`(333 재사용) | — | art334_Ⅰ |

**2항 — 흉기휴대·합동, D-2 재사용.**

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.dangerous_weapon_carriage`(D-2 재사용) | — | art334_Ⅱ.1 |
| `legal_element.joint_commission_by_two_or_more`(D-2 재사용) | — | art334_Ⅱ.3 |
| `legal_element.robbery_level_violence`(333 재사용) | — | art334_Ⅱ.1 |

**CompletionPolicy — 착수시기는 카드가 채택한 결론을 그대로 predicate화(학설
대립은 authoring 메모로만 기록, 카드 우선 원칙).**

```text
334_para1(야간주거침입강도):        ATTEMPTED.when = commencement_of_execution(trespass_entry 기준)
334_para2, 주간(흉기휴대·합동강도): ATTEMPTED.when = commencement_of_execution(robbery_level_violence 착수, 즉 폭행·협박 개시)
334_para2, 야간:                    ATTEMPTED.when = commencement_of_execution(trespass_entry 기준)
COMPLETED.when(공통)                = property_disposition류(333 재사용, 재물·이익 취득)
```

카드 2장(daytime_weapon_or_joint_robbery_attempt_on_violence_threat,
nighttime_home_intrusion_attempt_on_intrusion)이 정확히 이 두 결론을 명시한다 —
원문 Ⅲ이 소개하는 "주거침입시설/폭행협박시설" 학설 대립과 판례가 갈린다는 서술은
카드가 이미 채택한 결론(다수설=폭행협박시설이지만 **야간 요소가 있으면 침입시설**)에
대한 배경 설명으로만 authoring 메모에 남긴다 — 카드를 1차 자료로 삼는 방법론
(배치⑦ 이래 확정)에 따라 v0은 이 두 카드 명제를 그대로 채택하고 별도 HOLD로
올리지 않는다.

**범위 밖**: 총포·도검·화약류법 위반죄와의 경합(특별법), 특정범죄가중처벌법·
특정강력범죄법 누범가중(절차/특별법)은 기존 원칙대로 범위 밖.

---

## F. 제335조 준강도 — 절도(329/330/331)의 `DerivedOffenseDef`, 강도(333/334)로 처단

**구조 판단 — pilot v1이 HOLD로 남긴 "Doctrine vs `DerivedOffenseDef` 분류
미정"(draft_v1 §추가③, `doctrine.quasi_robbery`)을 이번 배치에서 실제로
확정한다: `DerivedOffenseDef`.** 준강도는 "강도죄의 예에 의하여 처벌"되며(카드가
증명하듯) 강도상해·치사(337·338조, G절)의 기본범죄가 될 수 있고 그 자체의
CompletionPolicy(기수·미수 판단 기준)까지 독자적으로 확립돼 있다 — 이건 Culpability/
Unlawfulness 층의 stage effect(DEFEAT/MODIFY/EXEMPT)로 표현되는 doctrine이 아니라,
base offense(절도) 위에 추가 요건(목적을 가진 폭행·협박)이 QUALIFY되어 별도
법정형·별도 completion을 갖는 파생 범죄유형이라는 게 이번 배치가 도달한 판단이다.

### F-1. 주체·객체 — base offense 자체가 이미 구조적으로 표현(별도 predicate 불필요)

| 카드 | 처리 |
|---|---|
| art335_sec2.preparation_stage_exclusion(절취행위 미착수면 준강도 아님) | 별도 exclusion predicate 불필요 — base offense(절도)의 `commencement_of_execution` 이상이 요구되는 구조 자체가 이미 이 배제를 표현한다(배치⑧ "구조적으로 이미 커버된 결론은 doctrine을 별도로 만들지 않는다" 원칙의 exclusion predicate 버전) |
| art335_sec2.property_interest_exclusion(재산상 이익 목적이면 준강도 불가) | 별도 exclusion predicate 불필요 — base offense가 절도(재물 객체)로 고정되므로 재산상 이익은 애초에 base offense 자체가 성립하지 않는다 |

### F-2. 목적 요건 — 3갈래, ANY로 결합(병합 아님)

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.purpose_to_resist_recapture`(신규) | 절도가 재물을 이미 자신의 배타적 지배 아래로 옮긴 뒤, 피해자 측으로부터 그 재물을 탈환당하지 않기 위하여 대항할 목적을 가지고 있다(아직 배타적 지배가 확립되지 않은 상태에서 지배를 확보할 목적으로 폭행·협박을 한 경우는 여기에 해당하지 않고 본래의 강도이다) | art335_sec3_1.pre_control_violence_is_robbery_exception, art335_sec3_1.recapture_resistance_after_exclusive_control |
| `legal_element.purpose_to_avoid_arrest`(신규) | 자기 또는 공범자가 체포되는 상황을 막을 목적을 가지고 있다(재물에 대한 지배 취득을 요건으로 하지 않는다) | art335_Ⅲ.2 |
| `legal_element.purpose_to_conceal_evidence`(신규) | 범행의 증명자료가 되는 증거를 소멸시킬 목적을 가지고 있다(재물에 대한 지배 취득을 요건으로 하지 않는다) | art335_Ⅲ.3 |

```text
quasi_robbery.requires 中 목적요건 = ANY(purpose_to_resist_recapture,
                                         purpose_to_avoid_arrest,
                                         purpose_to_conceal_evidence)
```

카드(art335_sec3.special_purpose, "목적범")·art335_sec3_4.purpose_achievement_
irrelevant(목적 달성 여부는 기수·미수와 무관)는 목적범 일반 법리 — 별도
predicate 없이 목적 요건이 주관적 구성요소로서 완성 여부와 독립적이라는 authoring
메모로만 남긴다(29조·genocide 등 다른 목적범과 같은 처리, 신규 없음).

**`purpose_to_resist_recapture` 하나에 "배타적 지배 확립"이라는 gating을 내장한
이유 — 별도 predicate로 분리하지 않는다(positive-predicate 원칙).**
"배타적 지배 미확립 + 폭행"은 `purpose_to_resist_recapture`가 아니라 애초에
본래의 강도(333/334조)로 별개 offense가 성립하는 사례(카드가 정면으로 "본래의
강도이며 준강도가 아니다"라고 함) — 이건 335조 Elements의 negative 조건이
아니라 offense 선택의 경계이므로, 별도 `NOT(exclusive_control_established)`
게이팅을 두지 않고 `purpose_to_resist_recapture`의 canonical_meaning 자체에
"이미 배타적 지배 확립 후"를 포함시켰다(배치⑪ A-1 "내부 이동 예외"와 동일한
offense-선택-경계 처리 방식).

### F-3. 절도의 기회 — `relation.occasion_identity`(6B fixture, 재사용)

| id | canonical_meaning | 근거 카드 |
|---|---|---|
| `relation.occasion_identity`(6B 강도살인미수 fixture 재사용) | 폭행·협박이 재물탈취와 시간적·장소적으로 밀접한 관련성이 있는 절도의 기회에 행하여졌다(절도범과 피해자 측이 절도 현장에 있는 경우, 절도에 잇달아 또는 시간·장소에 접착하여 피해자 측이 범인을 체포할 수 있는 상황, 범인이 범죄 흔적 인멸에 나올 가능성이 높은 상황을 포함하며, 범인이 원래의 범행현장으로부터 안전하게 도피하여 더는 추적이나 체포위협을 느끼지 않을 정도로 시간적·장소적 경과가 있었다면 인정되지 않는다) | art335_sec6_1.opportunity_temporal_spatial_proximity, art335_Ⅵ.1, Ⅵ.2 |

**검수 필요 F-3-1 — `occasion_identity`가 배치⑨·⑩에서 확정된 "6B 강도살인미수
fixture 재사용, base가 미수일 때 causal_nexus는 suspend될 수 있어도 occasion_
identity는 RETAIN"이라는 원래 맥락(강도상해·치상/강도살인·치사의 "강도의 기회")과
335조의 "절도의 기회"가 canonical_meaning 수준에서 완전히 같은 개념인지 확인이
필요하다.** 카드·원문 문언("절도의 기회")과 6B/G절("강도의 기회")의 시간적·장소적
밀접성 판단 기준이 동일한 심사방식(현장성/접착성/도피 완료 여부)을 쓴다는 점에서
재사용이 타당해 보이나, 335조는 base offense가 절도이고 G절(337·338)은 base가
강도(및 준강도 자신)라는 차이가 있다 — canonical_meaning을 "OO의 기회"의 "OO"를
파라미터화한 것으로 볼지, 아니면 335조 전용으로 별도 명명(`theft_occasion_
identity`)할지는 2패스에서 재사용 시도 후 확정한다(shared-predicate-canonical-
meaning-is-immutable 원칙에 따라, 재사용하려면 정의 자체를 조문별로 재정의하지
않아야 하므로 신중히 검토).

### F-4. 폭행·협박의 정도 — 333(강도) `robbery_level_violence` 재사용

| id | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.robbery_level_violence`(333 재사용) | 사회통념상 체포를 기도하는 자의 체포수행 의사나 재물탈환을 의도하는 자의 탈환 의사를 제압할 정도(반항을 억압할 정도)에 이르렀다(현실적으로 제압하였을 것을 요하지 않고 일반적·객관적으로 그 정도라고 인정되면 충분하며, 상대방이 절도의 피해자에 한정되지 않고 체포·추적·증거인멸 방해에 관계된 모든 사람을 포함한다) | art335_Ⅳ, Ⅴ |

카드 자체(art335_sec3_2, Ⅳ, Ⅴ 원문)가 "형법 제333조의 폭행·협박과 같이"라고
명시적으로 동일시하므로 재사용 확정 — 상대방 범위가 넓다는 점(경찰관·방범대원
등 포함)도 333조 predicate의 canonical_meaning이 이미 특정 상대방으로 좁혀져
있지 않으므로 별도 확장 없이 그대로 적용된다.

### F-5. Completion — base offense(절도)의 completion이 파생 offense의 completion을 결정

```text
quasi_robbery.completion:
    base_offense(theft).state = COMPLETED  → quasi_robbery.COMPLETED
    base_offense(theft).state = ATTEMPTED  → quasi_robbery.ATTEMPTED
    ATTEMPTED.punishable = true (342조 재사용, H절)
```

카드(art335_sec7.attempt_punishable, art335_sec7_1.attempt_theft_act_standard)와
2004도5074 전합(폭행·협박 기준설→절취행위 기준설 변경)이 정확히 이 구조를
확정한다 — **폭행·협박 자체의 기수·미수가 아니라 base offense(절도)의 기수·미수가
파생 offense(준강도)의 기수·미수를 그대로 결정**하는 첫 사례다.

**architecture-compatibility 확인 필요 F-5-1 — "base offense의 completion이
derived offense의 completion을 결정한다"는 링크가 8차 addendum
`derivative_mode.requires`로 표현 가능한지, 아니면 새로운 completion-linkage
메커니즘이 필요한지.** 배치⑨ 259(강도치상)·301(강간등 상해치상)의 COMPOSE
패턴은 "base offense가 완성된 뒤 그 결과로 가중결과가 발생"하는 구조였지 "base
offense의 completion state 자체가 derived offense의 completion state를 그대로
결정"하는 구조는 아니었다(6B의 QUALIFY도 마찬가지) — 335조가 이 패턴의 첫
사례이므로, 기존 `derivative_mode`가 이미 이걸 커버하는지 v0은 확정하지 않고
아래 HOLD 목록에 architecture-compatibility 신규 발견으로 올린다.

### F-6. 법정형 참조 — base offense 종류에 따라 333조(강도)/334조(특수강도) 중 선택

원문 Ⅷ("제333조 및 제334조의 예에 의한다")과 D-3(상습절도)의 base offense 선택
문제가 **정확히 같은 구조**다 — base가 단순절도(329)면 335는 333조(강도)로,
base가 야간주거침입절도·특수절도(330/331)면 335는 334조(특수강도)로 처단한다.
판례(단순절도범이 폭행 시에 비로소 흉기를 휴대해도 특수강도의 준강도가 된다는
법리, 원문 Ⅷ)까지 고려하면 이 선택은 base offense 자체의 성립 요건이 아니라
**폭행·협박 시점의 사실관계(흉기 휴대 여부·합동 여부)까지 함께 참조**해야 하므로
D-3보다 한 단계 더 복잡하다 — v0은 이 법정형 선택 로직을 predicate 사전 범위
밖(2패스 조립·Step 7 오케스트레이션 문제)으로 authoring 메모에만 남긴다.

### F-7. 죄수·공범 — 기존 원칙 재적용, 신규 없음

원문 Ⅸ.1(포괄일죄)·Ⅸ.3(강도치상·치사에 흡수)은 occurrence/cross-offense 경계
(범위 밖). 공범자 사이 폭행·협박의 예견가능성 귀속(원문 Ⅸ.1 후반)은 배치⑨
164 방화치사상 절이 이미 "ATTRIBUTE는 conduct 전용, intent·목적은 각자 자기
CaseTruths로 개별 평가"로 확정한 원칙의 재적용 — 목적 요건(F-2)은 폭행·협박을
직접 행한 공범자 본인의 CaseTruths로 평가하고, 다른 공범자에게는 30조 일반
공동정범 법리(예견가능성)로 별도 판단한다(신규 없음).

---

## G. 강도 결합범군 (제337·338조) — 강도(333/334/335) + 상해/살인

### G-0. 재사용 대상 확인

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.injury_result`(배치⑨ 재분류, 257/301 재사용) | 상해의 결과가 발생하였다(신체의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래됨 — 극히 경미하여 자연치유되고 일상생활에 지장이 없는 상처는 제외) | 배치⑨·⑩ |
| `legal_element.injury_intent`(배치⑨ 신규, 257 재사용) | 상해에 대한 고의가 있다 | 배치⑨ |
| `legal_element.result_causation`(배치⑨ 신규, death-agnostic) | conduct와 result(사망 또는 상해) 사이에 인과관계가 있다 | 배치⑨ |
| `relation.causal_nexus`(6B 재사용) | base offense(강도)의 수단·기회 행위와 결과 사이에 인과관계가 있다 | 배치⑨·⑩ |
| `relation.occasion_identity`(6B 재사용) | 결과가 base offense의 "기회"에 발생하였다 | 배치⑨·⑩ |

### G-1. 제337조 강도상해·치상

**주체 — base offense 범위, 별도 predicate 아님(offense_ref 선택지 서술).**

카드(art337_sec2.subject_robber_and_attempted_robber, "단순강도·특수강도·준강도·
인질강도의 강도범... 기수·미수 불문... 실행착수 있으면 주체")가 이미 base offense
후보 목록을 확정했다 — `base_offense = ANY(333 강도, 334 특수강도, 335 준강도,
336 인질강도)`. **336조(인질강도)는 51개 조문 워크시트 범위 밖**이라 그 자체를
population하지 않지만, 337·338의 "강도" 개념이 336까지 포함한다는 사실은
authoring 메모로 남긴다(328·344 준용조문과 같은 처리 — governing provision은
목록 소속 여부와 무관하게 참조는 하되 population은 안 함, 배치⑪이 확정한 원칙의
재적용). 강도 예비·음모(343조)의 범인은 제외된다(원문 Ⅱ, "실행착수 있어야").

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.injury_result`(재사용) | — | art337_Ⅲ.2 |
| `legal_element.injury_intent`(재사용, 상해=고의) | — | art337_Ⅲ.1 |
| `legal_element.result_causation`(재사용, 치상=death-agnostic 인과관계 그대로 상해에도 적용) | — | art337_Ⅲ.1 |
| `relation.causal_nexus`(6B 재사용) | — | art337_Ⅲ.3 |
| `relation.occasion_identity`(6B 재사용) | — | art337_sec3_2.robbery_occasion_ended(exception 카드는 occasion_identity의 legal_standard 부정 경계로 처리 — 별도 predicate 아님) |

**구조 — 결합범(고의 상해)/결과적가중범(과실 또는 무관 치상) 병존, 259·301과 동일
COMPOSE 패턴.** 배치⑨ 259(상해치사)·배치⑩ 301(강간등 상해치상)이 이미 확정한
"base offense(강도) + injury_result/injury_intent + causal_nexus + occasion_
identity" COMPOSE 패턴을 그대로 재사용한다 — 신규 구조 없음. 배치⑨·⑩의 HOLD
"결합범+결과적가중범을 별도 DerivedOffenseDef 2개로 할지 단일 DerivedOffenseDef
내 두 갈래로 할지"가 여기서도 동일하게 적용되므로 별도 신규 HOLD로 올리지 않고
기존 HOLD 항목에 세 번째 사례로 추가한다(아래 종합 목록).

**CompletionPolicy — 상해의 결과 발생으로 기수, 재물탈취 목적 달성 불요(카드 밖,
원문 Ⅳ 확정).**

```text
337.COMPLETED.when = injury_result (재물탈취 완료 여부 무관)
337.ATTEMPTED.when = 상해가 미수인 경우(상해미수 기준 — 강도의 기수·미수 불문,
                      통설·판례 취지)
337_후단(치상).ATTEMPTED.punishable = false (결과적가중범 미수 불가, 133①·301
                      과 동일 원칙 재적용)
```

### G-2. 제338조 강도살인·치사 — G-1과 완전히 같은 구조, 상해→사망

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.result_causation`(배치⑨ 250/267/268 재사용, death-agnostic) | — | art338_Ⅲ |
| `legal_element.intent`(13조 재사용, 살인의 고의) | — | art338_sec4.robbery_murder_attempt |
| `relation.causal_nexus`(6B 재사용) | — | art338_Ⅲ |
| `relation.occasion_identity`(6B 재사용) | — | art338_Ⅲ |

**CompletionPolicy — 살인의 기수·미수가 그대로 338조의 기수·미수(카드 3장이 정면
확정).**

```text
338(강도살인).COMPLETED.when = result_causation(사망) AND intent(살인의 고의)
338(강도살인).ATTEMPTED.when = commencement_of_execution(살인행위 착수) AND
                                 NOT(result_causation) — 강도의 기수·미수 불문
338(강도치사, 결과적가중범).ATTEMPTED.punishable = false (G-1과 동일 원칙)
```

카드(art338_sec4.murder_completion_controls_attempt, robbery_death_attempt_
excluded, robbery_murder_attempt)가 이 세 갈래를 정확히 대응시킨다 — 신규 판단
없음, G-1의 상해를 사망으로 치환한 것과 동형.

**공범 귀속 — F-7과 동일 원칙(ATTRIBUTE는 conduct 전용, intent는 개별 평가),
신규 없음.** 원문 Ⅴ가 소개하는 "고의의 공동이 있으면 강도살인, 없으면 강도치사"
구분은 살인의 고의(intent)를 공범자별로 개별 CaseTruths로 평가하는 배치⑨ 250
원칙의 재적용이다.

---

## H. 미수·예비 참조조문 (제342·343조)

### H-1. 제342조 절도·강도의 미수범 — 참조 전용, 독자 predicate 없음(300조·133①과 동일 처리)

카드 1장(art342.attempts_punishable, "329~341조의 미수범은 처벌된다")은 D·E·F·G절
전체(329~341조)의 `CompletionPolicy.states.attempted.punishable`을 일괄 `true`로
설정하는 근거 조문 그 자체다 — 25조(미수범, 전역)의 각칙 구체화이자 이번 배치
D-1·D-2·D-3·E-1·F-5·G-1·G-2가 이미 개별적으로 `ATTEMPTED.punishable`을 저작할
때 인용하는 근거일 뿐, 342조 자신은 predicate 사전에 population할 대상이 없다
(art300·133①과 같은 처리, 배치⑦·⑩ 원칙 재적용). 결과적가중범(강도치상·치사)의
미수가 없다는 것도 342조가 아니라 각 조문의 성질(결과적 가중범 일반 원칙)에서
나오는 결론이므로 342조 자체의 predicate로 표현하지 않는다.

### H-2. 제343조 강도의 예비·음모 — 28조(예비음모, 배치④ 확정) 재사용 + 목적 대상 한정

**base — `PREPARATION_OR_CONSPIRACY` CompletionPolicy state(배치④ 확정) 재사용.**

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.preparatory_conduct`(28조, 배치④ 확정 legal_element) | 죄를 범할 의사로 이를 실현하기 위한 준비행위를 하였다 | 배치④ |
| `legal_element.conspiracy_agreement`(28조, 배치④ 확정) | 2인 이상이 범죄실행에 관하여 상호 합의하였다 | 배치④ |
| `legal_element.intent`(13조 재사용, 강도의 목적) | 강도(단순강도·특수강도·약취강도·해상강도 — 준강도는 제외)를 범할 목적이 있다(미필적 인식으로도 충분하다) | art343_Ⅱ.1(원문) |

```text
343.requires = ALL(
    ANY(preparatory_conduct, conspiracy_agreement),
    intent(강도의 목적 — target offense 한정)
)
```

**"준강도할 목적만으로는 부족하다"(2004도6432, 원문 Ⅰ) — base offense 종류를
제한하는 서술, 별도 exclusion predicate 아님.** F절이 확정한 대로 준강도(335)는
절도(329/330/331)의 파생 offense이지 333/334조의 하위분류가 아니므로, "강도의
목적"이라는 이 predicate의 canonical_meaning이 애초에 333/334/336(및 해상강도,
51개 범위 밖)만을 가리키고 335(파생 절도)를 가리키지 않는다는 것 자체로 이미
구조적 배제가 성립한다(F-1과 동일한 positive-predicate 처리 방식).

**중지미수 불인정 — 별도 predicate 아님, 28조 일반원칙의 재확인(배치④가 이미
확정).** 카드(art343_sec3.abandonment_before_execution_denied, "예비·음모죄는
예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다")는
`PREPARATION_OR_CONSPIRACY` state 자체에 26조(중지범) variant state가 없다는
배치④의 기존 설계를 재확인하는 것 — 신규 없음.

**종범 불인정 — 32조(종범) 일반원칙 재확인, 신규 없음.** 원문 Ⅳ("정범이 실행의
착수에 이르지 아니한 예비의 단계에 그친 경우... 종범으로 처벌할 수 없다")는
32조 predicate(`aiding_conduct`)의 canonical_meaning이 애초에 "정범의 실행행위"를
전제한다는 것 — 예비죄에는 그 전제 자체가 없으므로 구조적으로 이미 배제된다
(D-3·F-1과 같은 처리 방식의 세 번째 사례).

**범위 밖**: 특정범죄가중처벌법(구 제5조의4③, 2016.1.6. 삭제), 총포·도검·화약류법
위반죄와의 관계는 특별법(범위 밖).

---

## I. 제344조 친족간의 범행 (준용조문) — population 대상 아님

**CURRENT.md가 이미 확정한 대로, 328조(친족상도례)와 같은 이유로 predicate 사전
population 대상이 아니다(procedure scope 밖, HOLD 아님 — 애초에 대상 아님).**
344조는 328조의 규정(형면제·친고죄, 소추조건)을 329~332조(및 그 미수범)에
그대로 준용하는 지시 조문일 뿐 자체 구성요건이 없다.

카드 4장(article328_theft_offenses_scope, robbery_no_family_benefit,
kinship_with_owner_and_possessor, kinship_only_one_holder_no_application)은
전부 328조 predicate(`legal_element.kinship_status_within_statutory_range`,
`doctrine.close_kin_property_offense_exemption`, 배치⑪ C절 확정)의 "누구와의
관계에 바인딩되는가"를 329~332조에 대해 구체화하는 authoring 메모로 남긴다 —
배치⑪이 이미 "330조 저작 시 재확인 필요"라고 예고해둔 지점이 바로 이것이다.

**330조(야간주거침입절도) 재확인 결과 — 주거자-행위자 관계는 328조 predicate에
불요, D-1에 이미 반영 완료.** 배치⑪ C절의 "night_burglary_resident_kinship_
exception"이 예고한 내용을 실제로 확인하면: 330조의 "피해자"는 재물의 소유자·
점유자이고(카드 kinship_with_owner_and_possessor의 "소유자 및 점유자 쌍방" 요건이
그대로 적용), 침입당한 주거의 거주자가 소유자·점유자와 다른 사람이더라도
`kinship_status_within_statutory_range`는 그 거주자가 아니라 재물의 소유자·
점유자를 기준으로 판정한다 — D-1 절에 별도 predicate를 추가하지 않고 이 확인
사실만 여기 authoring 메모로 남긴다(D-1의 predicate 정의 자체는 이미 완결돼
있어 변경 없음).

**강도죄(333·334·335·337·338)에는 준용되지 않는다(카드 robbery_no_family_
benefit, 원문 확정) — E·F·G절 전체에 328조 predicate가 등장하지 않는 이유를
여기서 교차 확인한다.** D·E·F·G절 위 표 어디에도 `kinship_status_within_
statutory_range`나 `close_kin_property_offense_exemption`을 등재하지 않은 것은
누락이 아니라 이 344조(및 328조 자신)의 준용 범위 확정에 따른 의도된 결과다.

**328조① 헌법불합치·개선입법 반영 상태 — 배치⑪ HOLD 그대로 유지, 이번 배치에서
새로 확인하지 않는다.** 328조 자체의 predicate(`close_kin_property_offense_
exemption`)를 344조가 그대로 준용하므로, 배치⑪이 이미 올려둔 HOLD("2025.12.31.
개선입법 반영 여부 확인 필요")가 330~332조에도 동일하게 적용된다 — 344조
저작으로 새로 발생하는 이슈가 아니라 328조 HOLD의 파급 범위 확인.

**범위 밖**: 354·361·365조(장물죄 관련 조문, 328조가 준용 대상으로 언급하지만
51개 조문 워크시트 범위 밖)는 배치⑪이 이미 명시한 대로 여전히 범위 밖.

---

## J. 횡령 가중·독립유형군 (제356·360조) — 355(횡령·배임) 재사용

### J-0. 재사용 대상 확인

| id | canonical_meaning | 출처 |
|---|---|---|
| `legal_element.duty_of_other_affairs`(배임, 355·357 공유) | 행위자가 타인의 사무를 처리하는 자의 지위에 있다 | pilot A-2, draft_v1 §추가② |
| `legal_element.entrustment_relationship`(횡령) | 보관자·소유자 사이에 형법상 보호가치 있는 위탁관계가 있다 | pilot A-2, draft_v2 수정2(둘 다 보존 확정) |
| `legal_element.custody_of_anothers_property`(횡령) | 행위자가 타인의 재물을 보관하는 자의 지위에 있다 | draft_v1 §추가② |
| `legal_element.unlawful_appropriation_intent`(전역 재사용) | — | pilot A-1 |
| `legal_element.embezzlement_manifestation`(횡령 전용, 신규 확정) | 불법영득의사를 외부에 표현하는 객관적 행위(고의를 현실화한 실행행위) | draft_v1 §1 |

### J-1. 제356조 업무상횡령·업무상배임 — 355의 QUALIFY(이중신분, 부진정신분범)

**구조 판단 — `DerivedOffenseDef`, QUALIFY 관계(배치⑦ 152 위증/모해위증·배치⑨
258의2와 같은 급, "신분요건이 base 완성 위에 얹히는 구조").** 카드
(art356.dual_status, "단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여
업무자 신분이 요구된다")가 이 구조를 정면으로 확정한다 — COMPOSE(base+가중결과)가
아니라 QUALIFY(base+가중신분)다.

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.business_status`(업무자 지위, 신규) | 사회생활상의 지위에 기하여 계속적으로 행하는 사무를 수행하는 자로서, 그 업무의 수행으로서 문제된 재물을 보관하거나 사무를 처리하고 있다(법령·계약뿐 아니라 관례·사실상의 것을 포함하고, 본래 사무에 부수하여 편의상 수행하는 사무도 본래 사무와 밀접한 관련성이 있으면 포함되며, 업무 내용 자체가 위법하지 않은 한 면허·인가 미취득 같은 행정절차상 불법이 있어도 반복·계속되고 있다면 업무에 해당한다; 사회질서에 반하거나 강행법규를 위반하는 등 법이 절대적으로 금지하는 행위는 업무의 의사로 반복하더라도 업무가 되지 못하고, 업무와 무관하게 타인의 재물을 보관·처리하게 된 경우에는 이 predicate가 성립하지 않는다) | art356_sec2_1.business_continuity_status, art356_sec2_1.incidental_business_relation, art356_sec2_2.administrative_illegality, art356_sec2_2.illegal_business, art356_sec2_2.unrelated_possession |

```text
356.base_offense = ANY(355 횡령[custody_of_anothers_property + entrustment_
                        relationship + unlawful_appropriation_intent +
                        embezzlement_manifestation],
                        355 배임[duty_of_other_affairs + ...])
356.requires = ALL(base_offense.requires, business_status)
```

**exception 카드 3장 — 별도 predicate 아님, `business_status` 정의 안에 이미
반영(위 표 참고).** unrelated_possession(업무 무관 보관은 불성립)·
administrative_illegality(행정절차 불법은 업무성 인정)·illegal_business(절대적
금지행위는 업무 아님)는 서로 다른 방향의 세 exception이지만 셋 다 "업무"라는
하나의 legal_element의 legal_standard 경계이지 별도 doctrine이나 defeater가
아니다 — 카드 라벨(defeater/exception)을 그대로 새 구조로 승격하지 않는다는
배치⑧·⑪ 원칙 재적용.

**status_awareness(업무자 지위 인식은 미필적 인식으로 충분) — 별도 predicate
아님, 13조 재사용.** 고의(13조)의 일반 법리(미필적 고의 포함)가 이미 이 인식
요건을 커버한다 — 신규 legal_element 불필요.

**공범 — 33조 본문/단서 기존 구조 재적용, 신규 없음.** 원문 Ⅳ(단순 보관자·
비신분자가 업무상 보관자의 범행에 가공)가 소개하는 판례 입장(33조 본문으로
공동정범 성립, 단서로 단순횡령죄 처단형)은 D-3(상습절도)·323조(배치⑪ B절)와
같은 33조 일반 구조의 세 번째 재확인 사례 — 신규 architecture 이슈 아님.

**CompletionPolicy — base offense(355)의 completion을 그대로 따른다(J-1 자체가
가중신분일 뿐 completion을 바꾸지 않음, D-3과 동일 처리).**

### J-2. 제360조 점유이탈물횡령 — 355와 별개의 독립 구성요건(위탁관계 불요)

**구조 판단 — `OffenseDef` 독립(base offense 없음), 355와 canonical_meaning
일부만 재사용.** 원문 Ⅰ.2가 통설 입장(위탁물횡령죄와 법적 성질을 달리하는
독립된 별개 범죄, 위탁신임관계를 요건으로 하지 않음)을 확정한다 — F절(준강도)
처럼 base offense가 있는 파생 구조가 아니라, 355의 일부 요소(불법영득의사 +
그 객관적 표현)만 재사용하고 신분요건(custody_of_anothers_property/
entrustment_relationship/duty_of_other_affairs)은 전혀 요구하지 않는 별도
offense다.

| id (가칭) | canonical_meaning | 근거 카드/원문 |
|---|---|---|
| `legal_element.property_of_another`(신규 — 366조 `object_ownership_other`와 재사용 관계, 아래 검수 필요 J-2-1) | 객체가 타인 소유의 재물이다(무주물은 제외된다) | art360_sec2_2.ownerless_property_exclusion |
| `legal_element.lost_or_stray_property_status`(신규) | 유실물·표류물·매장물이거나 그 밖에 원점유자의 의사에 기하지 않고 그 점유를 벗어났으나(우연히 행위자의 점유 하에 들어온 경우를 포함) 아직 누구의 점유에도 속하지 않거나 행위자의 점유에 속하게 된 재물이다(타인의 간수·관리 등 실력적 지배가 미치는 장소 내에서 방치·유류된 물건, 원점유자가 소재를 알고 다시 찾을 가능성이 있는 물건, 이미 타인에 의하여 새로운 점유가 개시된 물건은 제외된다) | art360_Ⅱ.2(원문, 대응 카드 없음) |
| `legal_element.unlawful_appropriation_intent`(전역 재사용) | — | (355 재사용) |
| `legal_element.embezzlement_manifestation`(355 재사용, 아래 검수 필요 J-2-2) | — | art360_sec2_3.later_appropriation_intent |

**검수 필요 J-2-1 — `property_of_another`를 366조(재물손괴)
`legal_element.object_ownership_other`와 같은 predicate로 재사용할지, 별도로
둘지.** 배치⑪ B절 검수 필요 3이 366의 `utility_impairment`(효용침해 판단)를
323조와 "canonical_meaning 불공유"로 확정한 것과 달리, 이번 건은 "타인 소유"라는
소유권 귀속 판단 자체를 묻는 것이라 성격이 다르다 — 366(objective_ownership_
other, "무주물·사체·전송중 정보 등은 제외")과 360(ownerless_property_exclusion,
"무주물은 제외")이 같은 법적 판단(민법상 소유권 귀속)을 가리킬 가능성이 높다.
v0은 신규 id로 잠정 등재하되, 재사용 여부는 두 조문의 판례 정의를 대조하면
확정 가능한 성격의 질문이라 architecture 이슈로 승격하지 않는다(D-2-1과 같은
처리).

**검수 필요 J-2-2 — `embezzlement_manifestation`(355 전용으로 확정된 이름)을
360에 재사용하는 것이 "shared-predicate-canonical-meaning-is-immutable" 원칙에
어긋나지 않는지.** 355의 canonical_meaning은 "불법영득의사를 현실화한 객관적
실행행위"이고, 360의 카드(later_appropriation_intent, "처음에는 불법영득의사
없이 습득했더라도 후에 영득의사를 일으켜 그 표현행위를 하면 그 시점에 기수")도
동일하게 "영득의사의 객관적 표현"을 요구한다 — 355는 위탁관계를 전제로 한
"보관 중인 재물"에 대한 표현행위이고 360은 위탁관계 없는 "점유이탈물"에 대한
표현행위라는 차이가 있지만, canonical_meaning 자체("불법영득의사를 객관적으로
표현하는 행위")는 위탁관계 유무와 무관하게 동일해 보인다 — 배치⑧ "동일한 법적
판단인가만 확인하면 충분" 원칙에 따라 v0은 재사용으로 잠정 제안하되, 356(J-1)도
같은 predicate를 쓰게 되므로 355/356/360 세 조문이 공유하는 형태가 된다는 점을
명시해 확정 검수를 요청한다.

**reporting_noncompliance_alone(신고절차 미이행만으로는 불성립) — 별도 predicate
아님, `embezzlement_manifestation`의 legal_standard 부정 경계.** 유실물법 등이
정한 절차를 밟지 않았다는 사정만으로는 "객관적 표현행위"에 이르지 못한다는
카드(art360_sec2_3.reporting_noncompliance_alone)는 `embezzlement_
manifestation`이 요구하는 정도(부작위로도 성립 가능하나 "상당 기간" 등 추가
사정이 필요)의 경계 사례 — 신규 predicate 없음.

**CompletionPolicy — 표현행위 시 기수, 미수범 없음(359조, 카드에도 반영).**

```text
360.COMPLETED.when = embezzlement_manifestation
360.ATTEMPTED — state 자체를 두지 않거나 punishable = false
  (133①·301·G-1·G-2가 이미 확정한 "미수 불처벌은 punishable=false로 표현,
  completion state 삭제 아님" 원칙 재적용 — 다만 360은 원문 스스로 "위법한
  점유취득이 영득행위와 동시에 행하여지는 경우가 대부분이므로 미수 단계의
  설정은 큰 의미를 갖지 못한다"고 하여 미수 state 자체의 실익이 거의 없다는
  점만 authoring 메모로 남긴다 — state를 아예 없앨지 punishable=false만
  둘지는 2패스에서 확정)
```

**친족상도례 — 328조가 준용되나 위탁관계 불요이므로 "행위자-소유자"만 필요(원문
확정, I절과 대조).** 355(위탁관계 기반)와 달리 360은 신분관계 요건이 없으므로
328조 predicate(`kinship_status_within_statutory_range`)를 "행위자-소유자"
쌍방향으로만 바인딩한다 — 이것도 I절과 마찬가지로 328조 predicate 자체의
재정의가 아니라 360조가 그 predicate를 바인딩하는 방식에 대한 authoring
메모다(population 대상은 아니지만 356·360이 준용 대상이라는 점은 328조와의
관계에서 I절과 함께 기록).

**범위 밖**: 죄수(손괴한 경우 불가벌적 사후행위, 자기앞수표 환금은 별도 사기죄
불성립 등)는 occurrence/cross-offense 경계.

---

## HOLD/architecture-compatibility 종합 (2패스 착수 전 확인 목록에 추가)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례, 257·298조
자상·도구 간접정범, 250조 비신분자 존속살해 가담, 301조 결합범+결과적가중범 병존,
299조 예비음모 conduct 갈래 제한, art323 소유자 아닌 자의 가담↔33조 본문 공동정범,
art328① 헌법불합치·시행중지 상태 확인, art319 계절적 미사용 별장 서브타입 재분류)에
이번 배치로 다음이 추가된다:

1. **art335(준강도) "base offense의 completion state가 derived offense의
   completion state를 그대로 결정"하는 링크가 8차 addendum
   `derivative_mode.requires`로 표현 가능한지 확인(F-5-1)** — 이 배치 전체에서
   가장 중요한 신규 발견. 기존 COMPOSE(259·301)·QUALIFY(152·356)는 모두 "base
   완성 + 추가 요건"이었지 "base의 completion 값 자체가 derived의 completion
   값이 되는" 구조가 아니었다.
2. **art332(상습절도)·art335(준강도)의 "base offense 종류(329/330/331 또는
   333/334)에 따라 적용 법정형·offense_ref가 분기"하는 구조가 predicate 사전
   층위 문제인지 Step 7 오케스트레이션 문제인지 확인(D-3, F-6)** — 두 조문이
   같은 구조를 공유하므로 하나의 확인사항으로 묶는다.
3. **art331 2항 `joint_commission_by_two_or_more`(합동범)가 30조 공동정범
   predicate의 특수 적용인지, 331조 2항 고유의 "현장성" 요건이 추가된 독립
   legal_element인지 확인(D-2)** — 판례가 "공동정범의 일반 이론"과 "현장성
   제한"을 함께 요구하는 이중 구조.
4. **art335 `occasion_identity`("절도의 기회")를 337·338(G절, "강도의 기회")과
   같은 predicate로 재사용할지, 별도 명명할지 확인(F-3-1)** — canonical_
   meaning 불변 원칙에 따라 신중히 검토 필요.

**구조 선택 문제(gap 아님, 순수 판단)**: art330 `nighttime`이 `trespass_entry`
시점에 결합되는 시점 바인딩 표현 방식(D-1), art331 `dangerous_weapon_carriage`와
배치⑨ 258의2 `dangerous_object_carriage`의 재사용 여부(D-2-1), art360
`property_of_another`와 366 `object_ownership_other`의 재사용 여부(J-2-1),
art360 `embezzlement_manifestation`을 355/356/360 세 조문이 공유하는 것의 확정
여부(J-2-2) — 넷 다 "같은 법적 판단인가"만 확인하면 되는 성격이라 architecture
이슈로 승격하지 않고 이 배치 v0 제출 시 함께 검수 요청한다.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**미확정 — F-5-1(준강도 completion-linkage)에 달려 있다.** 나머지는 전부 기존
`LegalElementDef`/`GroundFactDef`/`DerivedOffenseDef`(COMPOSE·QUALIFY 재사용)/
6B `RelationDef`(causal_nexus·occasion_identity 재사용)/8차 addendum
`derivative_mode`/25조 Completion predicate로 표현된다. F-5-1이 기존
`derivative_mode.requires`로 커버되는 것으로 확인되면 이번 배치도 "신규 없음"으로
마무리되고, 커버되지 않는 것으로 확인되면 이 배치 전체에서 유일한 신규
architecture 발견이 된다 — 어느 쪽이든 v0 제출 시점에는 확정하지 않는다(2패스
착수 전 확인 대상).

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입 결과)

1. **카드 분해**: 335조 목적요건(재물탈환/체포면탈/증거인멸)을 배치⑦ 뇌물
   5행위태양·배치⑪ 323조 취거/은닉/손괴 선례를 따라 3개 별도 leaf로
   분해(F-2) — 재물탈환만 "배타적 지배 확립"이라는 별도 gating을 내장해야
   해서 세 목적의 요건 강도 자체가 다르므로 병합하지 않는 것이 맞다고 판단.
   331/334조의 흉기휴대·합동은 이미 배치⑨ 258의2 선례가 있어 그대로 분리
   유지.
2. **doctrine 자격 검사**: pilot v1이 HOLD로 남긴 `doctrine.quasi_robbery`를
   이번에 실제로 `DerivedOffenseDef`로 확정(F절 전체) — "다른 죄로 전환"처럼
   보이는 카드를 doctrine으로 만들지 않는다는 배치⑦ 원칙의 적용이지만, 이번엔
   반대로 "정말 doctrine이 아니라 완전한 별도 파생 offense"라는 결론이라
   배치⑦·⑧과는 다른 방향의 판단이다(자기모순 아님 — quasi_robbery는애초부터
   "다른 죄로의 전환"이 아니라 "그 자체로 강도죄의 예에 의해 처벌되는 독자
   범죄유형"이기 때문).
3. **긍정형 이름**: 이번 배치 신규 predicate id 중 `not_`/`no_`/`non_` 접두는
   없다. `purpose_to_resist_recapture`에 "배타적 지배 확립 후"라는 조건을
   내장한 것이 다른 predicate의 논리적 부정을 긍정형으로 위장한 것이 아닌지
   재확인했다 — "배타적 지배 미확립 상태의 폭행"은 이 predicate의 부정이
   아니라 **애초에 다른 offense(본래의 강도)로 판정되는 사실관계**이므로,
   positive-predicate 원칙(배치⑪ `no_justifiable_reason_for_refusal`
   처리와 동일 논리)에 어긋나지 않는다고 확인.
4. **`ONE_OF` 사용 전 배타성 증명**: 이번 배치에서 `ONE_OF`를 쓴 곳이 없다.
   D-3·F-6의 "base offense 종류에 따른 법정형 분기"도 `ONE_OF`가 아니라
   Step 7/오케스트레이션 문제로 명시적으로 이월했다(exact-one 검증 대상이
   아님을 확인).
5. **CompletionPolicy state 반례 대입**: F-5(준강도 completion-linkage)에
   "base offense가 ATTEMPTED인데 목적요건이 없는 경우"(예: 절도미수 후
   아무 폭행도 없이 체포됨)를 대입 — 이 경우 quasi_robbery 자체가
   `requires`(ANY 목적요건)를 충족하지 못하므로 애초에 quasi_robbery
   offense_ref가 성립하지 않고 절도미수(base offense) 그대로 남는다는 걸
   확인(F-5의 링크는 quasi_robbery가 성립함을 전제로 한 completion 값
   전달이지, quasi_robbery 성립 자체를 만들어내지 않는다).
6. **일반원칙 서술 전 인접 대조**: 335 `purpose_to_resist_recapture` ↔ 333
   강도(폭행이 먼저)를 대조해 배타적 지배 확립 전/후로 offense가 갈리는 경계를
   확인(F-2). 335 `occasion_identity`("절도의 기회") ↔ G절 `occasion_
   identity`("강도의 기회")를 대조해 재사용 여부를 확인사항으로 이월(F-3-1,
   확정하지 않고 검수 요청). 360 `property_of_another` ↔ 366
   `object_ownership_other`를 대조해 배치⑪ 323/366 "유사≠동일" 사례와 달리
   이번엔 재사용 후보로 판단(J-2-1, 배치⑪과 반대 결론이 나온 이유를 명시).
7. **stage 라벨-설명 일치**: `legal_element.business_status`(356)를
   doctrine이 아니라 legal_element로 확정 — "업무자 지위"는 stage effect
   (DEFEAT/MODIFY/EXEMPT)를 발생시키는 것이 아니라 Elements 층의 신분요건
   그 자체이므로 355의 다른 legal_element(duty_of_other_affairs 등)와 같은
   층위에 둔 것이 카드 설명(canonical_element 라벨)과 일치함을 재확인.

---

## 다음 세션 시작점 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외)

마스터플랜이 정의한 각칙 최종 범위(51개 조문)에서 배치⑦-⑫가 다루지 않은 마지막
하나가 art339다 — 워크시트 스크립트 대상이 아니므로(카드 자체가 없음) 원본
주석서를 직접 열람해 predicate를 authoring해야 한다. 337·338(G절)이 이미 확정한
"강도(333/334/335/336)+상해/살인" COMPOSE 패턴을 그대로 재사용해 "강도+간음"
구조로 확장할 수 있을 것으로 예상되나, 실제 열람 전에는 확정하지 않는다. art339
완료 후 각칙 51개 조문 + art339 전체가 끝나면 **predicate 사전 전체(각칙 + 총칙
34개 조문)에 대한 최종 통합 검수 게이트**로 넘어간다(CURRENT.md가 이미 예고한
"그 다음" 단계).
