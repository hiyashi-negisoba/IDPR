# Predicate 사전 확장 — 배치 ⑧ 방화·문서 (제164·225·227·231·234·239조) v0

배치⑦(공무원·사법 범죄, 4라운드) 종료 시 확정한
[`predicate-authoring-self-check-checklist`](메모리)를 이번 배치는 제출 **전**에 직접 대입해
적용했다 — 문서 끝 "self-check 적용 메모" 절에 항목별 적용 결과를 남긴다. 방법론은 배치⑦과
동일(카드 1차, 원문 주석은 모호할 때만 보조 인용).

6개 조문은 두 군으로 갈린다 — **방화군**(164, 단독)과 **문서죄군**(225 공문서위조·변조 /
227 허위공문서작성 / 231 사문서위조·변조 / 234 위조사문서행사 / 239 사인등의 위조·부정사용,
보호법익=문서·인장의 진정성에 대한 공공의 신용 공유). 문서죄군 5개 조문은 재산죄 pilot 이후
처음 다루는 "문서에 관한 죄" 범주라 선례가 없다 — 위조(무형위조 아닌 유형위조)/변조/허위작성
(무형위조)/행사 4개 행위태양이 조문마다 다르게 조합되므로, 이번 배치의 핵심은 그 4개 개념을
predicate 층에서 어떻게 분리·공유할지 결정하는 것이다.

---

## 방화군 (제164조 현주건조물등방화·현주건조물등방화치사상)

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.arson_target_status` | 객체(건조물·기차·전차·자동차·선박·항공기·지하채굴시설)가 행위 당시 범인 이외의 자가 주거로 사용하거나 범인 이외의 자가 현존하는 것이다 | art164_sec2_1.temporal_residence_or_presence |
| `legal_element.burning_result` | 화력이 매개물을 떠나 목적물 스스로 연소를 계속할 수 있는 상태(독립연소)에 이르러 화력에 의한 건조물 등의 훼손·손괴 결과가 발생하였다 | art164_sec2_1.burning_result, .independent_combustion_completion_precedent(동일 개념 중복 — 하나로 합침) |

**`commencement_of_execution` 재사용**(15개 파일럿에서 이미 확정된 predicate, 신규 아님):
canonical_meaning을 164에 맞게 특화 — "목적물 또는 그 도화물체에 직접 점화하거나 매개물을
이용하여 목적물에 도화시켰다(단순히 방화 목적으로 주거에 침입하거나 점화하지 않은 준비행위는
포함되지 않는다)". 근거: art164_sec2_1.attempt_commencement_ignition,
.no_attempt_before_ignition(NOT 조건으로 흡수), .entry_for_arson_not_attempt(NOT 조건으로 흡수).

**`legal_element.intent`(총칙 13조) 재사용** — 164 전용 신규 predicate 대신 재사용(164 카드에
독자 고의 카드가 없어 원문 Ⅱ.1 후반부로 보조 확인). legal_standard에 "주거사용·현존 인식은
미필적 고의로 족하고, 목적물의 법적 성질(건조물·선박 등)에 대한 착오는 고의를 조각하지
않는다"를 흡수.

**결과적가중범(제3항) — 신규 구조 결정 없음, 기존 패턴 재사용**: 164 제2항(치사상)은
`derived_offense.robbery_causing_injury`/`robbery_homicide`(fixture 기존)와 동일한
COMPOSE + `primitive.aggravated_result_attribution` 구조로 그대로 대응된다
(`derived_offense.arson_causing_death_or_injury` 후보). `legal_element.aggravated_
result_attribution`의 기존 legal_standard("결과에 대한 예견가능성과 상당인과관계")가
art164_sec3_1.{fire_death_injury, fire_death_injury_foreseeability}와
art164_sec3_2.unforeseeable_firefighting_injury(부정적 한계 사례, NOT 조건 아니라
legal_standard 예시로 흡수)를 그대로 커버한다 — 새 predicate 불필요.

**검수 필요 1 — 부진정결과적가중범 표시.** 164 판례(96도485)는 중한 결과에 고의가 있는
경우도 본죄로 포함한다(부진정결과적가중범) — `aggravated_result_attribution`의
canonical_meaning이 "과실"만 전제하는 것으로 읽히지 않는지 재확인 필요. 재산죄 core의
강도살인/치상 fixture가 같은 성격인지 확인 후 필요하면 canonical_meaning에 "고의로 인한
경우도 포함"을 명시.

**검수 필요 2 — 공동정범 예견가능성(art164_sec3_5.accomplice_aggravated_result_
foreseeability), 잠정 판단 = gap 아님.** 집단방화 중 일부가 고의로 살상을 가해도 **다른
공동정범에게 그 결과의 예견가능성이 있으면** 그 공동정범도 치사상 책임을 진다는 카드다.
언뜻 33/34조식 architecture-compatibility 후보로 보이지만, 예견가능성은 본질적으로
행위자 개별적 심리상태이므로 각 공동정범이 **자신의** case truths로
`aggravated_result_attribution`을 평가하면 그대로 성립한다 — ATTRIBUTE(predicate-level
truth 전이)가 필요한 사안이 아니다(전이할 대상 자체가 "그 사람 본인의 예견가능성"이라 전이
개념이 성립하지 않음). **gap 아님으로 잠정 결론, 2패스 착수 시 재확인**.

**교사·방조 예견가능성(art164_sec3_5.aider_aggravated_result_foreseeability)은 이미
스키마에 있다.** 8차 addendum `derivative_mode.requires`가 정확히 이 요건("기본범죄
교사·방조 외에 중한 결과에 대한 예견가능성")을 위한 필드 — 신규 predicate나 스키마 변경
불필요, 저작 시 그대로 채워 넣으면 된다.

**범위 밖(predicate 아님, 참고주석만)**: `art164.pre_claim_insurance_fraud_no_attempt`
(보험금 청구 전 방화는 보험사기방지특별법위반죄의 실행착수 불인정) — 164조 자체의
구성요건이 아니라 다른 특별법 조문과의 경계(배치⑦ 129 sec2_4·137 sec6과 같은 패턴).

---

## 문서죄군 (225 공문서위조·변조 / 227 허위공문서작성 / 231 사문서위조·변조 / 234
위조사문서행사 / 239 사인등의 위조·부정사용)

### A. 공유 predicate 후보 (dedup)

| id (가칭) | canonical_meaning | 근거 카드 | 검수 필요 |
|---|---|---|---|
| `legal_element.forgery_without_authority` | 작성(또는 인장·서명 현출) 권한 없는 자가 타인의 명의를 사용하여 문서·도화 또는 인장·서명·기명·기호를 작성·현출하였다(명의자의 명시적·묵시적 승낙·위임이 있으면 이 요건은 충족되지 않는다; 대표·대리 등 권한 있는 자가 그 권한 범위 **내에서** 자기·제3자 이익을 위해 작성한 경우도 권한남용일 뿐 위조가 아니다; 다만 위임된 권한의 범위를 초과하여 작성하면 위조다) | art225.author_instruction_or_consent, art231_sec3_2.{authorized_creation, comprehensive_delegation, authority_abuse}, art239_sec1_3.authorized_manifestation_not_forgery | 225(공문서)·231(사문서)·239(인장)에 걸친 재사용이 배치⑦의 "같은 개념·다른 actor 방향"(122/136) 문제처럼 실은 object 타입이 달라(문서 vs 인장) 안전하지 않을 수 있음 — `aggravated_result_attribution`처럼 인자를 `entity`로 다형화하면 재사용 가능해 보이나 확정 전 재확인 |
| `legal_element.alteration_of_genuine_document` | 권한 없는 자가 이미 진정하게 성립되어 완성된 타인 명의 문서의 내용을 그 동일성을 해하지 않는 범위에서 변경하여 새로운 증명력을 만들었다(대상은 반드시 기존에 완성되어 진정하게 성립한 문서여야 하고, 이미 허위이거나 미완성인 서면에 가필·완성하는 것, 동일성을 해할 정도로 전혀 새로운 내용을 만드는 것은 변조가 아니라 위조다) | art225.false_original_not_alteration_object, art225_sec3_1.{alteration_requirements, new_content_is_forgery}, art231_sec3_3.genuine_document_requirement | 239에는 대응 개념이 없음(239는 "부정사용"이지 "변조"가 아니다 — 아래 239절 HOLD 참고) |
| `legal_element.purpose_to_use_as_genuine` | 위조·변조·허위작성된 문서·도화 또는 인장·서명을 진정한 것처럼 사용할 목적이 있다(적극적 의욕·확정적 인식은 불요, 미필적 인식으로 족함; 행위 당시 존재해야 하나 특정 용도에 한정될 필요는 없음) | art225_sec4_1.{intent_to_use_requirement, intent_to_use_time_of_act}, art227_sec4(문장 중 목적 부분만 분해), art231_sec4.purpose_of_use, art239_sec1_4.purpose_of_use | **234에는 배치하지 않음** — 234 조문 주석이 "본죄는 구성요건으로 행사할 목적을 요하지 않는다"고 명시(자기 행위 자체가 행사이므로 목적범 아님). 239의 "타인의 의사에 반하여 위법하게 사용"이 나머지 3개 조문의 "진정한 것처럼 사용"과 실질이 같은지도 재확인(239는 위조·부정사용 양쪽에 걸친 서술이라 부정사용 쪽 뉘앙스가 섞여 있을 가능성) |
| `legal_element.utterance_conduct` | 위조·변조·허위작성된 문서·도화 또는 인장·서명을 진정한 것처럼 상대방이 인식할 수 있는 상태에 두었다(제시·교부·송부·비치·열람 등 방법 불문; 상대방은 그 문서·인장에 이해관계가 있고 위조 등의 정을 모르는 자여야 하며, 정을 아는 공범자에 대한 제시·교부는 제외; 단순 소지·휴대나 상대방에게 기회가 되면 제공하기 위해 소지하는 것, 사자·사환에게 교부하는 것만으로는 부족; 원본을 사용해야 하고 필사본은 제외되나 기계적 복사본은 그 자체가 문서로 간주되어 포함) | art234_sec2_1 전체 카드군, art239_sec2.exposure_as_use | — |

### 제225조 공문서위조·변조 (조문 고유)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.public_document_object` | 공무소 또는 공무원이 그 명의로 직무권한 내에서 소정 형식에 따라 작성한 문서·도화이다(계약 등으로 공무 관련 업무를 대행하는 자는 법률·특별법상 공무원 의제 규정이 없는 한 제외; 중요한 형식을 결여한 문서는 제외; 우리나라 공무소·공무원이 작성한 것이 아닌 외국 공문서는 원칙적으로 제외) | art225.{contractual_delegate_not_official, essential_form_defect, foreign_official_document} |

`commencement_of_execution` 재사용(위조·변조 의사를 확정적으로 문서에 표시하는 행위),
완성 기준은 legal_standard로 "일반인이 진정한 것으로 오신할 정도의 형식·외관을 구비" —
근거 art225_sec5 카드군 전부, `waste_bag_film_preparation_only`는 NOT 조건으로 흡수(문안
필름 제조만으로는 착수 아님, 예비 단계).

**검수 필요 3 — `deceived_official_no_indirect_perpetration`는 별도 predicate가 아니라
`forgery_without_authority`의 canonical_meaning 경계로 흡수.** 공무원 아닌 자가 허위
증명원을 제출해 정을 모르는 담당공무원이 자신의 진정한 권한으로 그 신청 내용대로 증명서를
발급한 경우, 발급된 문서 자체가 진정성립이므로 애초에 forgery_without_authority 요건
(권한없는 작성)이 충족되지 않는다 — doctrine이 아니라 요건 부존재. 아래 227절의 대조와
혼동하지 말 것.

### 제227조 허위공문서작성 (조문 고유)

`legal_element.public_document_object`(225와 **동일 predicate 재사용** — 227 원문이
"공문서 또는 공도화... 앞서 살펴본 바와 같다"고 225 논의를 직접 인용해 교차 확인됨).

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.official_with_writing_authority` | 행위자가 해당 문서를 작성할 직무상 권한이 있는 공무원이다(작성권한 없는 공무원이 허위작성 시에는 227이 아니라 225·226 문제가 된다; 국가사무를 수행하거나 소속 기관의 행정기관성이 인정된다는 사정만으로는 부족하고, 신분상 공무원이어야 하며 그렇지 않은 사람을 처벌하려면 별도 특별규정이 필요하다) | art227.{authority_bearing_public_official, no_writing_authority_exception, nonpublic_status_exception} |
| `legal_element.content_falsity_by_authorized_official` | 작성권한 있는 공무원이 그 권한 범위 내에서 진실에 반하는 기재를 하거나(허위작성), 이미 작성된 진정 문서의 내용에 허위의 변경을 가하였다(변개)(고의로 법령을 잘못 적용하였더라도 그 적용의 전제가 된 사실관계 자체에 거짓이 없으면 허위가 아니다; 진술자가 허위 진술한 것을 알면서도 그 진술대로 조서에 기재한 것은 진술 그대로의 적법한 조서 작성이므로 허위가 아니다) | art227_sec4.execution_act(문장 중 허위작성·변개 부분만 분해), art227_sec4_3.legal_misapplication_true_facts, art227.recording_statement_as_stated_exception |

**검수 필요 4(v0 잠정 오류 가능성 자체 표시) — `nonofficial_indirect_perpetration_
exception`을 doctrine으로 둘지 재검토.** v0은 일단 `doctrine.nonofficial_cannot_be_
indirect_perpetrator_of_status_offense`(공무원 아닌 사람이 작성권자를 도구로 이용해도
227은 진정신분범이라 그 간접정범이 성립하지 않는다, 근거 art227_sec3_2.nonofficial_
indirect_perpetration_exception)로 표에 올렸으나, self-check 2번("범죄가 완성된 뒤에도
법률효과가 붙는가?")을 적용하면 답은 "아니오 — 애초에 신분이 없어 227의 정범적격 자체가
없다"이므로 doctrine이 아니라 **`official_with_writing_authority`의 정의 자체(신분 있는
공무원만 정범)에서 이미 커버되는 사안**일 가능성이 높다. 33조(공범과 신분, 배치⑤)의
"진정신분범은 비신분자의 간접정범 불성립"이라는 총칙 일반원칙의 단순 적용 사례라 227
고유 predicate 자체가 불필요할 수도 있음 — v1에서 결정.

**대조 — 225의 `deceived_official_no_indirect_perpetration`과 227의 위 항목은 같은
"간접정범 불성립" 결론이지만 근거가 다르므로 하나로 합치면 안 된다.** 225 쪽은 발급된
문서 자체가 **진정성립**이라 위조 요건(forgery_without_authority) 자체가 없는 사안이고,
227 쪽은 227이 **진정신분범**이라 비신분자에게 애초에 정범적격이 없는 사안이다 —
checklist 6번(일반원칙 서술 전 인접 대조) 적용 결과.

`purpose_to_use_as_genuine` 재사용, 고의 부인 사유(`legal_element.intent`, 총칙13조
재사용)의 canonical_meaning에 "단순 오기·부주의에 의한 기재 누락·선례나 업무상 관행에
따른 기재·통상 있을 수 있는 사소한 차이는 고의를 부인한다" 흡수 — 근거 art227.no_intent_
clerical_or_customary_entry.

### 제231조 사문서위조·변조 (조문 고유)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.private_document_object` | 권리·의무의 발생·변경·소멸에 관한 사항, 또는 그 이외에 거래상 중요한 사실을 증명하는 사항을 기재한 타인 명의의 문서·도화이다(단순히 개인적·집단적 의견의 표현에 그치는 문서는 제외되고, 적어도 실체법 또는 절차법이 정한 구체적 권리·의무와의 관련성이 인정되어야 한다) | art231_sec1.element.object_and_purpose(문장 중 object 부분만 분해) |

`forgery_without_authority` / `alteration_of_genuine_document` / `purpose_to_use_as_
genuine` 재사용(위 A절). `legal_element.intent`(총칙13조) 재사용 —
art231_sec4_1.intent_awareness_and_realization 흡수(타인 명의 문서라는 인식 + 위조·변조
한다는 인식과 실현의사). `commencement_of_execution` 재사용 — art231_sec5 카드군.

### 제234조 위조사문서행사 (조문 고유)

독자 predicate 없음 — `utterance_conduct`(위 A절)로 전부 흡수된다. 234는 231이 만든
위조문서를 "행사"하는 별개 offense이지만, 234 자체 카드가 정의하는 개념(무엇이 행사인가,
무엇이 행사가 아닌가)이 A절 predicate의 canonical_meaning 그 자체다.

**검수 필요 5(HOLD) — 234의 착수(attempt) 기준.** art234.attempt_punishable 카드는
미수범 처벌만 명시하고, 착수 시점을 정하는 별도 카드가 없다(`completion_by_placement_or_
mail_delivery`는 **기수** 기준). `commencement_of_execution`을 그대로 재사용해도 되는지,
아니면 "행사 착수"라는 234 고유 기준(예: 제시를 위해 문서를 꺼내는 행위 등)이 필요한지
원문에 명시가 없어 판단 보류 — 2패스 전 원문 재확인 대상.

### 제239조 사인등의 위조·부정사용 (조문 고유)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.seal_or_signature_object` | 인장·서명·기명·기호이다(자연인뿐 아니라 법인·법인격 없는 단체 명의도 포함된다) | 조문 주석 Ⅰ.2(카드 없음, 원문 보조 — "타인"의 범위 논의) |

`forgery_without_authority`(인장 현출·서명 버전) / `purpose_to_use_as_genuine` /
`utterance_conduct` 재사용. `legal_element.intent`(총칙13조) 재사용 —
art239_sec1_4.intent_awareness 흡수(타인 명의를 도용하여 인장을 도용한다는 인식).

**검수 필요 6(HOLD) — 239조 "부정사용" 자체의 적극적 정의 카드가 이번 배치에 없다.**
art239 조문 주석은 부정사용 부분을 "[공인 등 위조·부정사용죄]에서 설명한 것과 대체로
같다"고 238조(이번 배치 범위 밖)를 인용하는 방식으로만 서술하고, 카드 목록에도 부정사용
자체를 정의하는 canonical_element가 없다(art239_sec1_3.deceived_nominee_manifestation_
not_improper_use는 부정사용의 **부정적 한계**만 다룬다: 명의자를 기망해 인영·서명을
현출시킨 뒤 이를 사용해도 명의자의 권한을 수여받아 행사한 것이므로 부정사용이 아니다). 지금
단계는 위조·행사 관련 predicate만 확정하고 **"부정사용" conduct predicate 자체는 HOLD** —
필요 시 238조 열람으로 보강.

**`ground_fact.seal_or_signature_object`의 명의 실재성 쟁점도 HOLD.** 대법원은 사자·허무인
명의 인장을 239조 객체에서 제외한다고 보았으나(2002도18 등, 사문서위조죄의 옛 판례와 같은
입장), 225/231 절에서 확인했듯 사문서·공문서 쪽 판례는 이미 허무인·사자 명의도 포함하는
쪽으로 변경되었다 — 239조 인장 관련 판례가 그 변경을 따라갈지는 불확실하다는 것이 조문
주석 자체의 서술(향후 변경 예상). canonical_meaning에 실재성 요건을 넣지 않고 이 쟁점은
그대로 HOLD로 남긴다.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 방화군의 결과적가중범은 기존 `primitive.aggravated_result_attribution` +
COMPOSE 패턴(강도치상/강도살인 fixture)을 그대로 재사용하고, 문서죄군은 전부 기존
`GroundFactDef`/`LegalElementDef`(+ 총칙 13조 `legal_element.intent` 재사용)로 표현된다.
completion 관련해서도 133조식 CompletionPolicy 다중 state 분기가 필요한 조문이 하나도
없었다(164의 미수/기수는 표준 `commencement_of_execution` + 단일 결과 판정 패턴, 234의
기수 시점도 `utterance_conduct`가 성립하는 시점 하나뿐).

다만 다음은 이번에 구조 결정 없이 넘어가면 안 된다:

1. **`legal_element.purpose_to_use_as_genuine`이 code 전역 재사용 가능한 "목적범 공통
   predicate" 후보라는 점** — `legal_element.intent`가 13조에서 전역 재사용되는 것과 같은
   급으로, 위조죄 계열(통화·유가증권 등 이번 배치 범위 밖 조문 포함)이 대부분 "행사할 목적"을
   요구하는 목적범이라는 점에서 이후 배치가 유사 조문을 만날 때 같은 predicate로 계속
   재사용될 가능성이 높다 — 지금 결정하지 않고 반복 사례가 쌓이면 확정.
2. **`forgery_without_authority`의 3개 조문(225·231·239) 교차 재사용 여부**(검수 필요 1) —
   object 타입이 문서/인장으로 다른데 predicate를 하나로 유지할 수 있는지 스키마 arguments
   타이핑 확인 필요.
3. **227의 `nonofficial_indirect_perpetration_exception`을 doctrine으로 유지할지, 아예
   predicate를 만들지 않을지**(검수 필요 4) — self-check 2번 적용 결과 doctrine 자격이
   의심되어 v0 표에 올려두면서도 스스로 오류 가능성을 표시해뒀다.
4. **164 공동정범 예견가능성**(검수 필요 2)이 gap 아님이라는 잠정 판단 — 2패스에서 실제
   저작해보며 재확인.

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입 결과)

1. **카드 분해**: art231_sec1.element.object_and_purpose(object+purpose 결합), art227_
   sec4.execution_act(주체+목적+행위+내용 결합) 등 AND로 묶인 카드를 분해해 별도
   predicate(`private_document_object` / `purpose_to_use_as_genuine`, `official_with_
   writing_authority` / `content_falsity_by_authorized_official`)로 나눴다.
2. **doctrine 자격 검사**: 227의 간접정범 불성립 후보에 실제로 적용해 doctrine이 아닐 수
   있다는 결론에 도달했고(위 검수 필요 4), v0 표에도 그 의심을 그대로 남겨뒀다 — 배치⑦처럼
   "일단 doctrine으로 적어놓고 다음 라운드에 지적받는" 패턴을 피하려 한 것.
3. **긍정형 이름**: 이번 배치 predicate id 중 `not_`/`no_`/`non_` 접두가 붙은 것은 없다
   (모두 긍정형 + canonical_meaning 안에 NOT 조건 서술).
4. **`ONE_OF` 사용 전 배타성 증명**: 이번 배치에는 `ONE_OF` 후보 자체가 없었다(위조/변조/
   허위작성/행사 4개 행위태양이 서로 다른 조문·offense에 배치되어 한 offense 안에서 상호
   배타적 선택지로 나열되는 카드가 없음).
5. **CompletionPolicy state 반례 대입**: 다중 state가 필요한 조문이 없어(위 "신규 스키마"
   절) 이 항목은 해당 없음으로 확인.
6. **일반원칙 서술 전 인접 대조**: 225 vs 227의 "간접정범 불성립" 두 카드를 직접 대조해
   서로 다른 법리임을 명시했다(위 "대조" 절) — 배치⑦의 129/130, 133/130 대조와 같은 방식.
7. **stage 라벨-설명 일치**: 이번 배치에 DEFEAT/MODIFY/EXEMPT stage를 가진 doctrine
   후보가 227의 의심스러운 1건뿐이라 별도 stage 배정을 하지 않았다(legal_element negative
   조건 가능성이 높다고 이미 표시).
