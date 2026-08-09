# Predicate 사전 확장 — 배치 ⑩ 성적 자유 (제297·298·299·300·301조) v0

배치⑨(생명·신체) 종료 시 확정한
[`predicate-authoring-self-check-checklist`](메모리, 7항목)와
[`shared-predicate-canonical-meaning-is-immutable`](메모리, 4항목)를 제출 **전**에
직접 대입했다 — 문서 끝 "self-check 적용 메모" 절에 항목별 결과를 남긴다. 방법론은
배치⑦-⑨와 동일(카드 1차, 원문 주석은 모호할 때만 보조).

5개 조문은 세 군으로 갈린다 — **강간·추행군**(297 강간 / 298 강제추행 / 299
준강간·준강제추행), **미수 참조군**(300, 독자 predicate 없이 297·298·299의 미수
처벌범위만 확정), **가중결과군**(301 강간등 상해·치상, 297·298·299·300을 base로 하는
COMPOSE). 이 배치가 처음으로 다루는 법익(성적 자유)이지만, 배치⑨가 생명·신체 장에서
확립한 두 원칙 — **인과관계 이층 모델**(단일 offense 내부는 `LegalElementDef`, COMPOSE
간은 `RelationDef`)과 **death-agnostic 패턴**(268 `result_causation`처럼 결과를 구체
지정하지 않고 offense instance의 실제 사실로 판단) — 이 배치에도 그대로 적용된다.

---

## 공유 predicate 후보 (성적 자유 장 전체, 297·298 최초 정의 → 299·301 재사용)

| id (가칭) | canonical_meaning | 근거 카드 | 비고 |
|---|---|---|---|
| `legal_element.natural_person_victim_status`(배치⑨ 250·257 재사용, **정의 불변**) | — (기존 정의: 출생하여 아직 사망하지 아니한 자연인으로서 행위자 이외의 타인) | art297_Ⅲ.1, art298_Ⅱ | 297/298/299 객체("사람", 남녀불문)가 배치⑨의 정의와 정확히 일치 — "자기 자신 제외"는 자상 배제와 동일 논리, "법인·동물·사체 제외"도 그대로 적용된다. **배우자도 객체가 될 수 있다는 판례(2012도14788 전합)조차 이 정의와 충돌하지 않는다** — 정의가 배제하는 건 "자기 자신"뿐이고 배우자는 애초에 "타인"이므로 손댈 필요가 없다(self-check6, 인접 대조 확인). 연령·장애 등에 따른 가중은 전부 성폭력처벌법·청소년성보호법(특별법) 사항 — 범위 밖(배치⑨ 250과 동일 패턴) |
| `legal_element.coercive_conduct`(신규, GroundFact 아님) | 행위자가 피해자 또는 제3자에 대하여 폭행(유형력의 행사) 또는 협박(공포심을 일으킬 수 있는 해악의 고지)을 하였다(폭행·협박의 대상이 반드시 피해자 본인의 신체에 한정되지 않는다) | art297_Ⅳ.1, art298_Ⅲ.1 | canonical_meaning 자체에 "폭행 또는 협박에 해당한다"는 구성요건 평가가 이미 들어 있어 GroundFact가 아니다 — 배치⑦ 정정6에서 `violence_or_threat_against_official`을 동일 이유로 GroundFact→LegalElement 재분류한 것과 같은 typing 오류(v0에서 바로 legal_element로 정정). "폭행 또는 협박"은 OR이지만 두 갈래가 서로 다른 completion 시점이나 서로 다른 downstream legal_element를 요구하지 않으므로(둘 다 같은 degree-sufficiency 판단으로 수렴) 분해하지 않는다(self-check1 적용 결과 — 분해 불필요로 판단) |
| `legal_element.directness_of_coercion_by_offender`(신규) | 그 폭행·협박은 행위자 본인이 직접 가한 것이다 | art297_sec4_1 | 이 predicate가 FALSE면 297/298 Elements는 그 자체로 불성립한다 — 그 이상의 의미(예: "그러므로 299가 성립한다")를 부여하지 않는다. 299는 `mental_incapacity_or_physical_helplessness_status`·`exploitation_of_incapacity`·성적 행위 conduct 등 **자신의 Elements를 독립적으로 충족해야** 성립하는 별개의 offense이지, 297/298 실패를 조건으로 발동하는 대체 경로가 아니다(cross-offense transition 금지 원칙 재확인 — 아래 299절 참고) |
| `legal_element.coercion_induced_sexual_act_causation`(신규, death-agnostic 패턴) | 그 폭행·협박으로 인하여 간음·유사간음 또는 추행이 이루어졌다(폭행·협박과 간음·추행 사이에 시간적 간격이 있더라도 인과관계가 인정되는 한 무방하며, 간음·추행 행위 종료 전이면 폭행·협박이 간음·추행보다 선행할 필요는 없다) | art297_Ⅳ.2, art298_Ⅲ.1 | 배치⑨ v3가 정정한 `result_causation` 패턴(어느 결과인지는 legal assessment에서 offense instance의 실제 사실과 함께 판단)을 그대로 적용 — 297(간음)·298(추행)·향후 297조의2(유사간음)가 전부 이 하나의 causation predicate를 공유하고, 어느 성적 행위와 연결되는지는 offense instance가 결정한다. 297/298 두 offense 모두 **단일 base OffenseDef 내부의 conduct→result 인과관계**이므로 `LegalElementDef`(elements.causation)로 표현 — RelationDef 아님(배치⑨ 인과관계 이층 모델의 "층1" 그대로 적용) |

---

## A. 제297조 강간

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.natural_person_victim_status`(위 공유 predicate 재사용) | — | art297_Ⅲ.1 |
| `legal_element.coercive_conduct`(위 공유 predicate 재사용) | — | art297.conduct.violence-threat-rape |
| `legal_element.directness_of_coercion_by_offender`(위 공유 predicate 재사용) | — | art297_sec4_1 |
| `legal_element.coercion_sufficiency_for_rape`(신규) | 그 폭행·협박이 피해자의 항거를 불가능하게 하거나 현저히 곤란하게 할 정도에 이르렀다(폭행·협박의 내용과 정도, 유형력을 행사하게 된 경위, 피해자와의 관계, 성교 당시와 그 후의 정황 등 모든 사정을 종합하여 피해자가 처하였던 구체적 상황을 기준으로 판단하며, 사후적으로 피해자가 현장을 벗어날 수 있었다거나 사력을 다해 반항하지 않았다는 사정만으로 부정하지 않는다) | art297_sec4_3, Ⅳ.1 |
| `ground_fact.vaginal_intercourse_conduct`(신규) | 남성 성기의 여성 성기에의 삽입 내지 남성 성기와 여성 성기의 결합이 있었다(완전한 삽입·결합이나 사정은 요하지 않는다; 구강성교·항문성교 등은 이에 해당하지 않고 유사강간죄(297조의2, 범위 밖) 대상이다) | art297_Ⅲ.4, Ⅳ.2, Ⅳ.3 |
| `legal_element.coercion_induced_sexual_act_causation`(위 공유 predicate 재사용) | — | art297_Ⅳ.2 |
| `legal_element.intent`(총칙13조 재사용) | — | art297_sec6 |

**검수 필요 1 — 피해자 승낙("양해")이 별도 predicate가 필요한지, 아니면 이미 다른
predicate의 negative로 흡수되는지.** art297_sec5 카드군(valid_consent,
withdrawn_consent, consent_assessment)은 "피해자 승낙은 구성요건 해당성을 조각하는
양해"라고 명시한다 — 이건 24조 `doctrine.victim_consent_defeat`(Unlawfulness DEFEAT,
257의 스포츠규칙준수·위험감수동승에서 재사용한 것)와 **다른 층위**다. 257의 승낙은
"상해라는 결과 자체는 발생했으나 위법성이 조각되는" 구조인 반면, 297의 승낙(양해)은
진정한 합의가 있으면 애초에 `coercion_sufficiency_for_rape`나
`coercion_induced_sexual_act_causation`이 성립하지 않는다는 것 — 즉 Elements 층위에서
이미 결론이 나온다(self-check2, 다른 predicate의 negative가 결론을 구조적으로
만들어낸다). v0 판단은 **신규 predicate 불필요, 24조 doctrine도 재사용하지 않는다**는
것이나, 승낙 번복(withdrawn_consent)·오상승낙(mistake_of_consent, 고의조각) 같은
세부 판단이 정말 위 두 predicate의 legal_standard만으로 다 흡수되는지는 2패스 실제
저작 시 재확인 필요.

**미수·중지미수·불능미수** — `legal_element.commencement_of_execution`(25조)/
`voluntary_cessation_or_prevention`(26조)/`means_or_object_defect`+`dangerousness`(27조)
전부 정의를 손대지 않고 재사용한다(배치⑨ 250과 동일 패턴). "강간의 수단으로서
피해자의 반항을 불가능하게 하거나 현저히 곤란하게 할 정도의 폭행·협박이 개시된 때"
(art297_sec4_3)는 297이 이 predicate에 대응하는 사실관계일 뿐 canonical_meaning에
넣지 않는다(불변성 원칙). 남성이 남성을 여성으로 오인하고 간음 목적 폭행·협박한
경우(불능미수, art299_Ⅴ 카드가 원문에서 언급)는 27조 재사용.

**간접정범** — 자수범 아님(art297_Ⅱ), 34조의 일반적 간접정범 구조(도구의 책임·고의
결여)로 충분히 커버되고 배치⑨ 257·298(아래)의 "34조 gap"(피이용자=피해자 본인,
방향 반대) 유형과는 다르다 — 297 자체에는 그 유형의 사례가 카드에 없다.

**정당방위(피해자의 방어행위, art297_sec10)는 297의 predicate가 아니다.** 이건
피해자가 가해자에게 반격하여 발생시킨 별도 결과(예: 상해)에 대한 **피해자 자신의
책임 판단**이지 297 Elements의 일부가 아니다 — 21조 `doctrine.self_defense`는 그
별도 사건(피해자가 피고인이 되는 상해 등 사건)에서 재사용될 항목이지 297 predicate
사전에 올릴 대상이 아니다(범위 밖으로 명시 배제).

**범위 밖(predicate 아님)**: 흉기·합동에 의한 특수강간(art297_sec9)은
성폭력처벌법(특별법) 가중 — 258의2(형법 내부 조문)와 달리 형법전 밖이라 predicate
사전 대상 아님(배치⑨ "특정강력범죄 가중은 특별법" 원칙 재적용). 강도강간(art297_sec9,
art339)은 art339 저작 시 처리(51개 조문 워크시트 범위 밖, CURRENT.md가 이미
별도 항목으로 이월). 죄수(간음행위마다 별죄, 피해자별 별죄, art297_sec7)는 occurrence
단위 판단(9조 검수2 패턴). 친고죄 폐지·양형기준·상해·감금죄와의 경합 등은 형사소송법·
cross-offense 경계 사항(배치⑥/⑨ 원칙 재적용).

---

## B. 제298조 강제추행

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.natural_person_victim_status`(위 공유 predicate 재사용) | — | art298_Ⅱ |
| `legal_element.coercive_conduct`(위 공유 predicate 재사용) | — | art298_Ⅲ |
| `legal_element.directness_of_coercion_by_offender`(위 공유 predicate 재사용) | — | art298_Ⅲ (297과 동일 법리, 명시 카드는 없으나 원문이 준강간과의 구별로 전제) |
| `legal_element.coercion_sufficiency_for_forcible_indecency`(신규) | 그 폭행은 상대방의 신체에 대한 불법한 유형력의 행사이고, 그 협박은 일반적으로 상대방으로 하여금 공포심을 일으킬 수 있는 정도의 해악을 고지하는 것이다(2023. 9. 21. 선고 2018도13877 전원합의체 판결로 "항거를 곤란하게 할 정도로 강력할 것"을 요구하던 종전 법리 폐기 — 강간죄의 `coercion_sufficiency_for_rape`보다 낮은 기준) | art298_Ⅲ.1 |
| `legal_element.indecent_act`(신규, GroundFact 아님) | 객관적으로 일반인에게 성적 수치심이나 혐오감을 일으키게 하고 선량한 성적 도덕관념에 반하는 행위로서 피해자의 성적 자유를 침해하는 것이다(신체 접촉이 필수는 아니며, 신체 부위에 따른 본질적 차이는 없고, 행위자의 성욕 자극·만족 목적은 요건이 아니며, 피해자가 실제로 수치심·혐오감을 느꼈을 것도 요건이 아니다) | art298_Ⅲ.2 |
| `legal_element.coercion_induced_sexual_act_causation`(위 공유 predicate 재사용) | — | art298_Ⅲ.1 |
| `legal_element.intent`(총칙13조 재사용) | — | art298_sec4 |

**검수 필요 2 — "기습추행"은 `coercive_conduct`와 `indecent_act`가 사실상 동일
행위로 융합되는 경우인데, 두 predicate를 여전히 분리 유지해도 되는가.**
기습추행형(폭행행위 자체가 곧 추행에 해당, 예: 뒤에서 갑자기 껴안으며 신체 접촉)은
"폭행"과 "추행"이 물리적으로 같은 한 개의 행위다. 2023년 전합 판결 이후 대법원 스스로
"기습추행과 폭행·협박 선행형을 나누는 실익이 사실상 적어졌다"고 밝히고 있어(art298_Ⅲ.1
말미), 구조적으로 별도 completion 갈래를 만들 필요는 없어 보이나(self-check5 반례
대입 결과 — 두 유형이 겹치는 사건이 오히려 표준적이라 CompletionPolicy state로 나누면
곧바로 exact-one을 깨뜨린다), predicate 두 개(coercive_conduct/indecent_act)를
"같은 사실에 대한 두 개의 서로 다른 법적 평가"로 유지할지 "기습추행의 경우 하나로
합칠지"는 2패스 실제 저작 시 재확인 필요 — v0은 결정하지 않는다.

**실행의 착수** — "폭행·협박이 개시된 때, 기습추행의 경우 상대방 의사에 반하는
유형력 행사가 있는 때"(art298_sec3_3) — 25조 `commencement_of_execution` 재사용,
두 개시 시점(선행형/기습형)은 297과 마찬가지로 authoring 메모로만 남긴다(불변성 원칙).

**간접정범 — architecture-compatibility 신규 발견, 배치⑨ 257과 동일 유형.**
art298 Ⅲ.2 원문: "피고인이 피해자들을 협박하여 겁을 먹은 피해자들로 하여금 어쩔 수
없이 나체가 되게 하여 스스로를 촬영하게 하거나, 성기에 이물질을 삽입하거나 자위를
하는 등의 행위를 하게 하였다면 강제추행죄의 간접정범에 해당할 수 있다." 이건 배치⑨가
257(강요·기망에 의한 자상)에서 발견한 "피이용자(=피해자 본인)가 강요로 도구가 되고,
배후자가 간접정범으로 전체 책임을 지는" 구조와 **정확히 같은 유형**이다(34조가
미해결로 남긴 "방향 반대" 문제 — `principal_realization_truth`는 정범 성공을
조건으로 하는데 간접정범은 피이용자 불처벌을 조건으로 함). **새로 결정하지 않고,
33조 단서·34조·257 자상 간접정범과 함께 2패스 착수 전 확인 목록에 298을 추가**한다
(같은 유형의 두 번째 사례 — 신규 종류의 gap이 아니라 동일 gap의 재확인).

**"흉기·2인 이상 합동" 특수강제추행(art298_sec8)은 297과 동일 이유로 범위 밖**
(성폭력처벌법). "강제추행 후 이어 강간하면 강간죄만 성립"(art298_sec8)은 cross-offense
전환 서술(self-check2, doctrine 아님). 죄수(간음행위마다 별죄 등, art298_sec6)는
297과 동일 occurrence 판단, 범위 밖.

---

## C. 제299조 준강간·준강제추행

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.natural_person_victim_status`(위 공유 predicate 재사용) | — | art299_Ⅲ.1 |
| `legal_element.mental_incapacity_or_physical_helplessness_status`(신규) | 피해자가 심신상실(정신기능의 장애로 인하여 성적 행위에 대한 정상적인 판단능력이 없는 상태 — 원인이 생물학적 심신장애에 한정되지 않고 수면·음주·약물 등도 포함) 또는 항거불능(심신상실 이외의 원인으로 심리적 또는 물리적으로 반항이 절대적으로 불가능하거나 현저히 곤란한 상태)의 상태에 있다(그 원인은 불문하며, 심신미약(302조, 범위 밖)은 포함하지 않는다) | art299_Ⅲ.2, sec3_2 |
| `legal_element.exploitation_of_incapacity`(신규) | 행위자가 피해자의 심신상실 또는 항거불능 상태를 이용하여 간음·유사간음 또는 추행을 용이하게 하였다(객관적 이용관계) | art299.use_awareness_and_facilitation |
| `ground_fact.vaginal_intercourse_conduct`(297과 공유 재사용) / `legal_element.indecent_act`(298과 공유 재사용) | — | art299_Ⅳ |
| `legal_element.intent`(총칙13조 재사용) | — | art299_sec6, art299.use_awareness_and_facilitation |

`exploitation_of_incapacity`는 "그 상태를 이용해 성적 행위가 용이해졌다"는 객관적
이용관계만 담고, 그 상태에 대한 **인식**은 별도 predicate로 만들지 않고
`legal_element.intent`(총칙13조, 객관적 구성요건 사실에 대한 인식·용인)가 그대로
포괄한다 — 심신상실·항거불능 상태의 인식도 "구성요건적 사실"의 일부이므로 전역
intent 재사용 원칙(배치⑦이 129/130/133/136/151에 확장 적용한 것과 동일)에서
벗어날 이유가 없다. 별도 `awareness_of_incapacity` 같은 predicate를 만들지 않는다
(불변성 원칙 — intent를 조문마다 쪼개지 않는다).

**exploitation_of_incapacity가 297/298의 `directness_of_coercion_by_offender`와
대응 관계에 있지만, 이는 두 offense가 서로 배타적 사실관계를 요구한다는 뜻이지
한쪽의 불성립이 다른 쪽의 성립을 의미하는 게 아니다.** 297/298은 행위자 본인이
직접 폭행·협박을 가할 것을 요구하는 반면, 299는 그 상태를 **누가, 어떻게
발생시켰는지 불문**하고(이미 존재하던 상태 포함) 행위자가 그 상태를 이용하기만
하면 된다. 원인이 된 폭행·협박이 행위자 본인의 것이면(art299_sec3_2
`drug_administration_violence_exception`) 그 사실관계는 애초에
`exploitation_of_incapacity`가 요구하는 "이용"이 아니라 297/298의
`coercive_conduct`에 해당하므로 299 Elements 자체가 성립하지 않는다 — 이건
299가 **자신의 Elements를 독립적으로 평가한 결과** 불성립하는 것이지, 297/298의
성립 여부를 참조해서 판단하는 게 아니다(위 공유 predicate 절의 directness 비고와
동일 원칙, self-check6 297/298 절과 대조 완료).

**미수 — 27조 재사용, 준강간 불능미수(2018도16002 전합)가 27조의 정석적 적용
사례다.** 피고인이 피해자가 심신상실·항거불능 상태에 있다고 인식하고 이용할 의사로
간음했으나 실제로는 그 상태가 아니었던 경우 — 이건 27조 `means_or_object_defect`
(대상의 착오)의 교과서적 사례이지 신규 구조가 아니다. 실행의 착수는 "심신상실·항거불능
상태를 이용한 간음·추행의 수단이 되는 구체적 행위를 개시한 때"(art299_Ⅳ) — 25조
재사용, authoring 메모.

**예비·음모(305조의3, 2020년 신설) — 28·29조 재사용 후보이나, "간음 갈래에만
적용"을 authoring 메모로 처리하기엔 부족한 concrete authoring 확인사항으로
승격한다(HOLD).** 카드(art299_sec8.attempt_preparation_punishment)가 "준강간죄의
미수범과 예비·음모범 및 준유사강간·준강제추행죄의 미수범은 처벌한다"고 명시한다 —
**예비·음모는 간음(준강간) 갈래에만 적용되고, 추행·유사간음 갈래에는 적용되지
않는다.** 문제는 `PREPARATION_OR_CONSPIRACY.punishable`이 고정된 bool이라는 점이다
— 133①(배치⑦)의 conduct 갈래 분기는 이미 실행행위가 존재하는 completed/attempted
state 사이의 `when` 분기였지만, 예비·음모는 **아직 어떤 conduct(간음/추행/유사간음
중 무엇)로도 나아가기 전 단계**라 "간음 conduct 갈래에만 when이 충족되도록
저작한다"는 표현 자체가 성립하지 않을 수 있다(아직 conduct가 없으므로 conduct
갈래를 참조할 predicate가 없다). 2-pass에서 실제로 확인해야 할 두 후보:

- **A. 준강간/준강제추행을 별도 OffenseDef로 분리** — 그러면 각 OffenseDef가
  독립된 `PREPARATION_OR_CONSPIRACY.punishable`을 가지므로 준강간=true,
  준강제추행=false로 자연히 표현된다.
- **B. 단일 offense 안에서 예비 단계의 "목적한 죄"를 predicate로 명시** — 28·29조의
  `legal_element.purpose_to_commit_target_offense`(255 살인예비와 동일 패턴)가
  "간음을 목적으로 한 예비인가"까지 구별해낼 수 있는지 확인.

이건 새 primitive를 만들자는 제안이 아니라 **현재 CompletionPolicy/PREPARATION_OR_
CONSPIRACY 스키마가 이 조합을 표현할 수 있는지를 2-pass 실제 저작 시 직접 대입해
확인해야 하는 concrete authoring issue**다 — predicate 사전 v0 단계에서는 결론을
내리지 않는다.

**승계적 공동정범 불성립·준강간만 성립(art299_Ⅳ 원문)은 cross-offense 전환
서술이다(self-check2)** — 6C `apply_attribution`이 요구하는 "공동가공의 의사에 기한
기능적 행위지배"가 후행자에게 없다는 게 이미 6C 계약 자체에서 도출되는 결론이지
299의 별도 doctrine이 아니다.

**범위 밖**: 친고죄 폐지·양형기준(art299_sec8 일부)·강간죄와의 죄수 견해대립은
297과 동일 사유로 범위 밖.

---

## D. 제300조 강간등의 미수범 — 참조 전용, 독자 predicate 없음

CompletionPolicy 재사용 범위를 확정하는 조문이다 — **297·297조의2(유사강간, 범위
밖)·298·299의 미수범만 처벌하고, 301(상해·치상)·301조의2(살인·치사)·302·303의
미수범에는 적용되지 않는다**는 명시적 배제 목록(art300_x_raw_pdf.
other_offenses_exclusion)이 이번 배치의 핵심 확인사항 — **297/298/299는
`attempted.punishable = true`, 301은 `attempted.punishable = false`**로 표현한다는
걸 이 조문이 직접 근거짓는다(아래 301절, 카드 `no_general_attempt_punishment`와
정확히 합치 — 133①이 이미 세운 "미수가 불처벌인 것과 completion state 자체가
없는 것은 다른 문제"라는 원칙 그대로 적용, state 자체를 제거하지 않는다). 305조
(16세 미만 의제강간)에 대한
미수 적용 여부 해석(art300_x_raw_pdf.art305_under_sixteen_attempt_interpretation)은
305조 자체가 51개 조문 워크시트 범위 밖이라 참고만(HOLD 아님, 애초에 대상 아님 —
배치⑨ 36조 분류와 같은 패턴).

---

## E. 제301조 강간등 상해·치상

**구조 후보 — 결합범(상해)과 결과적가중범(치상)이 같은 조문에 병존하는 첫 사례,
2패스 이전 구조 결정 필요(HOLD).** base = `ANY(offense.rape, offense.forcible_
indecency, offense.quasi_rape)`(297/298/299, 그 미수 포함) + 가중결과 =
`legal_element.injury_result`(배치⑨ v1 재분류 반영, 아래 검수 필요 3) — 배치⑨ 259
(상해→사망)의 COMPOSE 패턴을 그대로 한 단계 확장한 것이지만, 259와 달리 **같은
조문 안에 "상해"(고의, 결합범)와 "치상"(과실, 결과적가중범) 두 변형이 병존**한다는
점이 새롭다:

- **강간등 상해**(art301_sec5_1, 고의범): base offense Elements(base 자신의
  `legal_element.intent` 포함, 297/298/299의 강간·추행 등에 대한 고의) +
  `legal_element.injury_intent`(신규, 상해 결과에 대한 **별도** 고의) +
  `relation.causal_nexus`(259 재사용, base 수단행위와 상해 결과의 인과관계) —
  133①/②(배치⑦, 별도 OffenseDef)와 달리 객체·행위자 위치는 base와 동일하므로
  별도 OffenseDef가 아니라 COMPOSE 변형일 가능성이 높지만, 259(순수 결과적가중범,
  intent 불요)와 달리 **intent가 추가된 COMPOSE**라 기존 COMPOSE 스키마가 이
  조합을 그대로 지원하는지 확인 필요. `injury_intent`를 base offense의
  `legal_element.intent`와 같은 predicate로 쓰지 않는다 — base intent는 "강간·
  추행 등에 대한 고의"만 담당하고 상해에 대한 고의는 별개의 heightened
  legal_element다(하나의 predicate id로 두 종류의 고의를 표현하면 구별이
  안 된다).
- **강간등 치상**(결과적가중범): base offense Elements + `primitive.aggravated_
  result_attribution`(259 재사용, 예견가능성·상당인과관계) — 259와 동일 패턴.
- **두 변형의 배타성**: 고의가 있으면 "상해", 없이 예견가능성만 있으면 "치상" —
  고의가 있는 사건은 예견가능성도 당연히 충족되므로 `치상`(과실) 변형에
  `NOT(injury_intent)`를 추가해야 두 변형이 겹치지 않는다(self-check5, 6B
  exact-one 원칙 그대로 적용 — 133① completed/attempted 겹침 제거 때와 동일 패턴).

이 구조 결정(별도 DerivedOffenseDef 2개 vs 단일 DerivedOffenseDef 내 두 갈래) 자체는
v0에서 내리지 않는다 — 후보만 제시하고 2패스 실제 저작 시점에 스키마를 직접 대입해
확정한다.

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.injury_result`(배치⑨ v1이 이미 `injury_occurred`→`injury_result`로 재분류 예정해둔 것, 257 재사용) | — | art301_Ⅳ.1, Ⅳ.2 |
| `legal_element.injury_intent`(신규, "상해" 변형 전용) | 상해의 결과에 대한 고의(미필적 고의로 족하다) — base offense 자신의 `legal_element.intent`(강간·추행 등에 대한 고의)와는 별개의 predicate다 | art301_sec5_1 |
| `primitive.aggravated_result_attribution`(259 재사용, "치상" 변형 전용) | — | art301_Ⅴ.2 |
| `relation.causal_nexus`(259 재사용) | base 수단행위와 상해 결과 사이의 인과관계 | art301_Ⅴ.2 |
| `relation.occasion_identity`(6B 재사용, 아래 별도 절) | 상해 결과가 base offense의 "기회"에 발생한 것이다 | art301_Ⅲ |

**base offense가 미수여도 COMPOSE가 성립한다 — 신규 gap 아니라 6B 기존 메커니즘의
재확인.** art301_sec2 카드(subject_predicate_offenses, attempt_injury)가 명시하듯
"그 미수에 그친 자"도 301의 주체다 — 강간 등이 미수에 그쳤더라도 그 수단(폭행·협박)
때문에 상해가 발생했으면 301이 성립한다. 이건 **Step 6B가 이미 확정한 "강도살인미수는
result·causation을 suspend하지만 occasion_identity는 RETAIN한다"는 정확히 같은
구조**(CURRENT.md 6B절 참고) — base offense의 Completion state가 `attempted`여도
가중결과와의 "기회 동일성"(occasion identity)이 유지되는 한 COMPOSE가 작동한다는 게
이미 fixture로 실증돼 있다. 신규 architecture 결정이 아니라 **기존 메커니즘의 두
번째 실사용 사례**로 문서화한다 — 정확한 필드명(occasion_identity의 실제 스키마
표현)은 2패스에서 그 fixture를 다시 열어 재확인.

**"강간등의 기회" 요건(art301_Ⅲ) — `relation.causal_nexus`에 흡수하지 않고
`relation.occasion_identity`(6B 재사용)로 별도 유지한다.** 이 문서 위 절에서 이미
"base offense가 attempted여도 COMPOSE가 성립하는 건 6B의 강도살인미수 fixture가
확정한 occasion_identity RETAIN 메커니즘과 같다"고 정리해뒀다 — causal_nexus(수단
행위와 상해 결과 사이의 인과관계)와 occasion_identity("그 상해가 강간 등의
기회에 발생했는가")를 하나의 relation으로 합치면, 바로 그 RETAIN/suspend 구분
자체가 표현 불가능해진다(causation은 base가 미수일 때 suspend될 수 있어도
occasion_identity는 RETAIN해야 한다는 게 6B의 핵심이었다). 두 obligation은
**별도로 유지한다**:

- `relation.causal_nexus` — base의 수단행위(폭행·협박 등)와 상해 결과 사이의
  인과관계 그 자체.
- `relation.occasion_identity` — 그 상해가 범행 실행 중·직후·범의 포기 직후 등
  "사회통념상 범죄행위가 완료되지 않았다고 볼 수 있는 단계"에서 발생했는가(범행
  기회 요건). 강간 등의 기회가 아닌 다른 사정(예: 술값 시비로 인한 별도 폭행)으로
  발생한 상해는 causal_nexus가 아니라 **occasion_identity가 먼저 FALSE**가 되는
  사례다(self-check2 — 다른 predicate가 결론을 만들어내는 게 아니라, 여기서는
  애초에 두 predicate가 각자의 역할을 지킨다).

**공범 — 배치⑨ 250·164 원칙 그대로 적용, 신규 없음.** "치상"(결과적가중범) 변형은
공모자의 예견가능성만으로 공동정범 책임(8차 addendum/aggravated_result_attribution,
164·259와 동일). "상해"(고의범) 변형은 공모자 각자에게 상해의 고의가 별도로
필요하다(art301_sec6) — 배치⑨가 250 강도살인 공동정범에서 확정한 "ATTRIBUTE는
conduct만, intent는 actor-specific으로 각자 평가"(6C 계약) 원칙의 재확인이지 새
구조가 아니다. 실행착수 전 이탈 시 공동정범 불성립(art301_sec6)은 30조 이탈 법리
일반원칙 재사용.

**미수범 처벌규정 없음 — `attempted` state 자체는 유지하되 `punishable = false`로
표현한다.** 카드 `no_general_attempt_punishment`와 300조가 명시하는 배제 목록이
정확히 합치한다. "상해"(고의)·"치상"(결과적가중범) 두 변형 모두 미수범 규정이
없다(art301_Ⅶ 원문 — 입법 불비로 평가되지만 predicate 사전은 현행 법 그대로
반영). **133①(배치⑦)이 이미 확정한 "미수가 불처벌인 것과 completion state 자체가
존재하지 않는 것은 다른 문제"라는 원칙을 그대로 적용** — state를 삭제하면
"실행에 착수했으나 상해에 이르지 못한" 사건이 CompletionPolicy 어느 state에도
속하지 못해 `unresolved`로 새는 반면, `attempted.punishable = false`로 두면
그 사건은 정확히 attempted state로 도출되되 처벌만 되지 않는다는 걸 명시적으로
표현한다. 진정결과적가중범에 미수가 없다는 원칙(259와 동일)은 "치상"에는 자연히
부합하지만, "상해"(고의, 결합범)에 미수가 없는 건 별도 입법 공백이다 — 어느 쪽이든
`punishable = false`로 표현은 동일하다.

**검수 필요 3 — `injury_result`의 canonical_meaning("신체의 생리적 기능 훼손")이
정신적 기능 훼손(외상후 스트레스 장애 등)까지 명시적으로 포함하는지 재확인 필요.**
art301_Ⅳ.5 원문은 수면장애·외상후스트레스장애 등도 상해에 해당한다고 명시한다.
배치⑨가 정의한 `injury_result`("신체의 생리적 기능 훼손 등 상해의 결과")가 이미
포괄한다고 볼 여지가 크지만("등"이 정신적 기능까지 넓히는 표현인지), 명시적으로
검증된 적은 없다(257 v0에서도 이 쟁점은 다루지 않았다) — 2패스 이전 확정 필요. 음모
절단(모근 보존 시 상해 아님, 모근째 뽑으면 상해)·경미한 상처(자연치유, 특별 치료
불요) 한계사례는 배치⑨ 257에서 이미 legal_standard로 흡수하기로 한 것의 연장선 —
신규 없음.

**범위 밖**: 강간등 살인·치사(301조의2, 이번 배치 범위 밖 — 배치 목록에 없음, 향후
배치 대상), 특정강력범죄 가중(art301_Ⅷ)은 배치⑥/⑨ 원칙 재적용. 유기죄 불성립·
상해죄와의 실체적 경합·강도강간과의 상상적 경합 등 "다른 죄와의 관계"(art301_Ⅸ)는
cross-offense 경계, 범위 밖.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**아직 확정 못함 — 301의 "고의 상해 + COMPOSE" 조합과 299의 예비·음모 conduct
갈래 제한이 기존 스키마로 표현 가능한지가 이번 배치의 열린 구조 질문이다.**
나머지는 전부 기존 `LegalElementDef`/`GroundFactDef`/25-27조/6C ATTRIBUTE/8차
addendum으로 표현되고 신규 없음. 301/299는:

1. **base offense가 `attempted` completion state여도 COMPOSE가 작동하는 메커니즘**과
   **`attempted.punishable = false`로 미수 불처벌을 표현하는 것**은 각각 6B의
   강도살인미수 fixture, 133①이 이미 실증한 메커니즘의 재사용이다(신규 아님,
   확인만 필요) — 위 301절. `relation.causal_nexus`/`relation.occasion_identity`를
   별도 obligation으로 유지하는 것도 같은 6B 설계의 직접 적용(신규 아님).
2. **결합범(고의)과 결과적가중범(과실)이 같은 조문에 병존**하는 구조를 별도
   DerivedOffenseDef 2개로 할지 단일 DerivedOffenseDef 내 두 갈래로 할지는 2패스로
   이월(HOLD) — 위 301절.
3. **299 예비·음모가 conduct 갈래(간음)에만 적용되는 구조**를 별도 OffenseDef
   분리로 표현할지, 예비 단계 predicate 자체에 목적 대상을 명시할지도 2패스로
   이월(HOLD) — 위 299절.
4. `legal_element.natural_person_victim_status`/`death_causation`류의 사망 전용
   predicate와 달리, 이번 배치의 `coercion_induced_sexual_act_causation`은 처음부터
   death-agnostic 패턴(배치⑨ v3 정정)을 그대로 적용해 설계했다 — 268처럼 뒤늦게
   정정할 필요가 없었다는 뜻이고, 이건 이 원칙이 이제 배치 착수 시점에 기본값으로
   자리잡았다는 신호(self-check 적용 결과로 기록).

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입 결과)

1. **카드 분해**: "폭행 또는 협박으로 강간"을 conduct(coercive_conduct)/degree
   (coercion_sufficiency_for_rape)/directness/intercourse conduct/causation
   5개로 분해(297·298 동일 구조). "폭행 또는 협박"의 OR은 분해가 불필요하다고
   판단한 근거를 명시(검수 필요 항목 자체가 아니라 위 공유 predicate 절에 결론 기록).
2. **doctrine 자격 검사**: 피해자 승낙("양해")을 doctrine 후보로 먼저 검토했으나
   "범죄가 완성된 뒤에도 이 효과가 붙는가?"에 답이 "아니오 — 애초에 coercion 요건
   자체가 미충족"이므로 doctrine이 아니라 Elements negative로 정리(297절 검수
   필요 1). 297/298/299 상호 cross-offense 전환 서술(art299 승계적 공동정범 불성립
   등)도 doctrine으로 만들지 않았다.
3. **긍정형 이름**: 이번 배치 신규 predicate id 중 `not_`/`no_`/`non_` 접두는 없다
   (`directness_of_coercion_by_offender`처럼 배제 대상은 서술로 담고 이름은 긍정형).
4. **`ONE_OF` 사용 전 배타성 증명**: 이번 배치에서 `ONE_OF`를 쓴 곳이 없다 —
   301의 "상해"/"치상" 두 변형이 겹칠 수 있다는 반례를 직접 대입해(고의 있으면
   예견가능성도 항상 충족) `NOT()` 게이팅이 필요함을 미리 표시해뒀다(위 301절).
5. **CompletionPolicy state 반례 대입**: 299의 예비·음모(305조의3)가 간음 갈래에만
   적용되고 추행·유사간음 갈래에는 적용되지 않는다는 반례를 직접 확인했고, 예비
   단계에는 아직 conduct 자체가 없어 "conduct 갈래에서만 when"이라는 단순 authoring
   메모로는 부족하다고 판단해 2-pass concrete authoring 확인사항(HOLD)으로
   승격했다(299절). 301은 300조 배제 목록을 근거로 두 변형 모두 `attempted.
   punishable = false`가 되어야 함을 확인 — state 자체를 없애면 133①의 기존
   설계(state 유지 + punishable로 불처벌 표현)와 충돌한다는 반례를 직접 대입해
   바로잡았다.
6. **일반원칙 서술 전 인접 대조**: 297/298의 `directness_of_coercion_by_offender`와
   299의 `exploitation_of_incapacity`를 나란히 놓고 "행위자가 직접 가했는가 vs
   이미 존재하는 상태를 이용했는가"가 서로 배타적 사실관계에 대응함을 확인(299절).
   298의 간접정범(피해자를 도구로)을 257의 자상 간접정범과 대조해 "같은 유형의
   두 번째 사례"로 명시하고, 새로운 gap으로 오분류하지 않았다.
7. **stage 라벨-설명 일치**: 이번 배치에 신규 DEFEAT/MODIFY/EXEMPT stage를 가진
   doctrine 후보가 없다(21·24조 doctrine을 사실은 재사용하지 않기로 결정했다 —
   297절 검수 필요 1) — 별도 배정 없음.

---

## HOLD/architecture-compatibility 종합 (2패스 착수 전 확인 목록에 추가)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례, 257조 자상
간접정범, 250조 비신분자 존속살해 가담)에 이번 배치로 다음이 추가된다:

1. **art298 피해자를 도구로 삼은 간접정범 ↔ 34조 gap** — 257과 **동일 유형**의
   두 번째 사례(신규 종류 아님, 위 298절).
2. **art301 결합범(고의 상해)+결과적가중범(과실 치상) 병존 구조** — 별도
   DerivedOffenseDef 2개 vs 단일 갈래 여부, predicate 사전으로는 결정하지 않고
   2패스 실제 스키마 대입 시 확정(위 301절, gap이 아니라 순수 구조 선택 문제라는
   점에서 33/34조류와는 성격이 다름 — 별도로 표시).
3. **art299 예비·음모(305조의3)의 conduct 갈래 제한** — `PREPARATION_OR_
   CONSPIRACY.punishable`이 고정 bool이라 "간음 갈래에만 적용"을 표현하려면
   별도 OffenseDef 분리 또는 예비 단계 predicate에 목적 대상 명시가 필요할 수
   있음, 2패스 실제 스키마 대입 시 확정(위 299절, 이것도 gap이 아니라 구조 선택
   문제).

art301의 "base offense attempted 상태에서도 COMPOSE 작동"·"attempted.punishable
= false로 미수 불처벌 표현"·"causal_nexus/occasion_identity 별도 유지"는 전부 6B·
133①이 이미 해결한 메커니즘의 재확인이므로 이 목록에 올리지 않는다(신규 gap 아님,
위 301절에 근거만 기록).
