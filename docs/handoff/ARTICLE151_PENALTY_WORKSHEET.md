# 제151조 「벌금 이상의 형에 해당하는 죄」 분류 워크시트 — 검수 요청

기준: 2026-08-15 · 대상: v2 registry의 offense 38 + derived_offense 25 = **63개**
설치 대상 필드: `article151_penalty_threshold.class` ∈ {`fine_or_greater`, `below_fine`}

## 이 문서의 지위 — review evidence이지 runtime metadata가 아니다

DSL에 들어가는 것은 **한 비트뿐**이다.

```yaml
article151_penalty_threshold:
  class: fine_or_greater
  authority_refs: [...]
```

아래 표의 「법정형(초안)」 열은 그 한 비트를 **법률검수하기 위한 근거**이고, 징역 몇 년·벌금
몇 만원 같은 숫자는 runtime에 들어가지 않는다. 형량 데이터베이스를 만드는 것이 아니다 —
runtime이 묻는 질문은 오직 "선행범죄가 제151조의 threshold를 통과하는가" 하나다.

새 offense가 이 필드 없이 추가되면 fail-closed로 UNKNOWN이 맞다.

## 이 워크시트가 판정을 요구하는 것

형법 제151조 제1항은 은닉·도피의 **대상자**가 "벌금 이상의 형에 해당하는 죄를 범한 자"일 것을
요구한다. 여기서 기준은 **법정형**이고, 선택형 중 가장 무거운 형이 벌금 이상이면 해당한다.
따라서 실무상 형법각칙의 죄는 사실상 전부 `fine_or_greater`다.

**그래도 일괄 TRUE로 처리하지 않는 이유**는 검수 ④에서 합의한 그대로다 — 가정이 틀린 단 한
자리가 보이지 않게 되기 때문이다. 미저작은 UNKNOWN이고, 지금 제151조 status leaf는 실제로
UNKNOWN이다.

## 검수 방법

아래 초안은 **제가 조문별 법정형을 적어 넣은 것이고, 검증이 필요합니다.**
전부 맞으면 "일괄 승인"만 적어 주시고, 틀린 행이 있으면 그 행에만 `> comment:`를 달아 주세요.
숫자(형기·벌금액)는 개정이 잦은 부분이라 특히 확인이 필요한 곳에 ⚠를 붙였습니다.

판정이 갈릴 여지가 있는 행은 표 아래 「판정 주의」에 따로 모았습니다.

---

## A. 재산죄

| offense_ref | 죄명 | 조문 | 법정형(초안) | 판정 |
|---|---|---|---|---|
| `offense.theft` | 절도죄 | 제329조 | 6년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |
| `derived_offense.nighttime_dwelling_theft` | 야간주거침입절도죄 | 제330조 | 10년 이하 징역 | fine_or_greater |
| `derived_offense.special_theft` | 특수절도죄 | 제331조 | 1년 이상 10년 이하 징역 | fine_or_greater |
| `offense.robbery` | 강도죄 | 제333조 | 3년 이상 유기징역 | fine_or_greater |
| `derived_offense.special_robbery` | 특수강도죄 | 제334조 | 5년 이상 유기징역 | fine_or_greater |
| `derived_offense.quasi_robbery` | 준강도죄 | 제335조 | 제333조·제334조의 예에 따름 | fine_or_greater |
| `derived_offense.robbery_causing_intentional_injury` | 강도상해죄 | 제337조 | 무기 또는 7년 이상 징역 | fine_or_greater |
| `derived_offense.robbery_causing_injury_by_aggravated_result` | 강도치상죄 | 제337조 | 무기 또는 7년 이상 징역 | fine_or_greater |
| `derived_offense.robbery_causing_intentional_homicide` | 강도살인죄 | 제338조 | 사형 또는 무기징역 | fine_or_greater |
| `derived_offense.robbery_causing_death_by_aggravated_result` | 강도치사죄 | 제338조 | 무기 또는 10년 이상 징역 | fine_or_greater |
| `derived_offense.robbery_rape` | 강도강간죄 | 제339조 | 무기 또는 10년 이상 징역 | fine_or_greater |
| `derived_offense.quasi_robbery_rape` | 준강도강간죄 | 제339조 | 무기 또는 10년 이상 징역 | fine_or_greater |
| `derived_offense.special_robbery_rape` | 특수강도강간죄 | 성폭력처벌법 제3조 제2항 ⚠ | 사형·무기 또는 10년 이상 징역 | fine_or_greater |
| `derived_offense.fraud` | 사기죄 | 제347조 | 20년 이하 징역 또는 5천만원 이하 벌금 (2025-12-23 개정) | fine_or_greater |
| `offense.extortion` | 공갈죄 | 제350조 제1항 | 10년 이하 징역 또는 2천만원 이하 벌금 | fine_or_greater |
| `offense.embezzlement` | 횡령죄 | 제355조 제1항 | 5년 이하 징역 또는 1천500만원 이하 벌금 ⚠ | fine_or_greater |
| `offense.breach_of_trust` | 배임죄 | 제355조 제2항 | 5년 이하 징역 또는 1천500만원 이하 벌금 ⚠ | fine_or_greater |
| `derived_offense.occupational_embezzlement` | 업무상횡령죄 | 제356조 | 10년 이하 징역 또는 3천만원 이하 벌금 ⚠ | fine_or_greater |
| `derived_offense.occupational_breach_of_trust` | 업무상배임죄 | 제356조 | 10년 이하 징역 또는 3천만원 이하 벌금 ⚠ | fine_or_greater |
| `offense.lost_property_embezzlement` | 점유이탈물횡령죄 | 제360조 | 1년 이하 징역, 300만원 이하 벌금 **또는 과료** | fine_or_greater ※1 |
| `offense.property_damage` | 재물손괴죄 | 제366조 | 3년 이하 징역 또는 700만원 이하 벌금 | fine_or_greater |
| `offense.obstruction_of_right_exercise` | 권리행사방해죄 | 제323조 | 5년 이하 징역 또는 700만원 이하 벌금 | fine_or_greater |

## B. 생명·신체

| offense_ref | 죄명 | 조문 | 법정형(초안) | 판정 |
|---|---|---|---|---|
| `offense.homicide` | 살인죄 | 제250조 제1항 | 사형·무기 또는 5년 이상 징역 | fine_or_greater |
| `offense.ancestral_homicide` | 존속살해죄 | 제250조 제2항 | 사형·무기 또는 7년 이상 징역 | fine_or_greater |
| `offense.injury` | 상해죄 | 제257조 제1항 | 7년 이하 징역, 10년 이하 자격정지 또는 1천만원 이하 벌금 | fine_or_greater |
| `offense.ancestral_injury` | 존속상해죄 | 제257조 제2항 | 10년 이하 징역 또는 1천500만원 이하 벌금 | fine_or_greater |
| `derived_offense.aggravated_injury` | 중상해죄 | 제258조 제1·2항 | 1년 이상 10년 이하 징역 | fine_or_greater |
| `derived_offense.aggravated_ancestral_injury` | 존속중상해죄 | 제258조 제3항 | 2년 이상 15년 이하 징역 | fine_or_greater |
| `derived_offense.special_injury` | 특수상해죄 | 제258조의2 제1항 ⚠ | 1년 이상 10년 이하 징역 | fine_or_greater |
| `derived_offense.special_ancestral_injury` | 특수존속상해죄 | 제258조의2 제1항 ⚠ | 1년 이상 10년 이하 징역 | fine_or_greater |
| `derived_offense.special_aggravated_injury` | 특수중상해죄 | 제258조의2 제2항 ⚠ | 2년 이상 20년 이하 징역 | fine_or_greater |
| `derived_offense.special_aggravated_ancestral_injury` | 특수존속중상해죄 | 제258조의2 제2항 ⚠ | 2년 이상 20년 이하 징역 | fine_or_greater |
| `derived_offense.injury_causing_death` | 상해치사죄 | 제259조 제1항 | 3년 이상 유기징역 | fine_or_greater |
| `offense.negligent_homicide` | 과실치사죄 | 제267조 | 2년 이하 **금고** 또는 700만원 이하 벌금 | fine_or_greater ※2 |
| `offense.occupational_or_gross_negligence_injury_or_homicide` | 업무상과실·중과실치사상죄 | 제268조 | 5년 이하 금고 또는 2천만원 이하 벌금 | fine_or_greater ※2 |

## C. 성범죄

| offense_ref | 죄명 | 조문 | 법정형(초안) | 판정 |
|---|---|---|---|---|
| `offense.rape` | 강간죄 | 제297조 | 3년 이상 유기징역 | fine_or_greater |
| `offense.forcible_indecency` | 강제추행죄 | 제298조 | 10년 이하 징역 또는 1천500만원 이하 벌금 | fine_or_greater |
| `offense.quasi_rape` | 준강간죄 | 제299조 | 제297조의 예에 의함 | fine_or_greater |
| `offense.quasi_forcible_indecency` | 준강제추행죄 | 제299조 | 제298조의 예에 의함 | fine_or_greater |
| `derived_offense.rape_causing_intentional_injury` | 강간상해죄 | 제301조 | 무기 또는 5년 이상 징역 | fine_or_greater |
| `derived_offense.rape_causing_injury_by_aggravated_result` | 강간치상죄 | 제301조 | 무기 또는 5년 이상 징역 | fine_or_greater |

## D. 국가적 법익

| offense_ref | 죄명 | 조문 | 법정형(초안) | 판정 |
|---|---|---|---|---|
| `offense.dereliction_of_duty` | 직무유기죄 | 제122조 | 1년 이하 징역이나 금고 또는 3년 이하 자격정지 | fine_or_greater ※3 |
| `offense.official_secret_disclosure` | 공무상비밀누설죄 | 제127조 | 2년 이하 징역이나 금고 또는 5년 이하 자격정지 | fine_or_greater ※3 |
| `offense.bribery_taking` | 수뢰죄 | 제129조 제1항 | 5년 이하 징역 또는 10년 이하 자격정지 | fine_or_greater ※3 |
| `offense.prospective_bribery_taking` | 사전수뢰죄 | 제129조 제2항 | 3년 이하 징역 또는 7년 이하 자격정지 | fine_or_greater ※3 |
| `offense.third_party_bribery` | 제3자뇌물제공죄 | 제130조 | 5년 이하 징역 또는 10년 이하 자격정지 | fine_or_greater ※3 |
| `offense.bribe_giving` | 뇌물공여죄 | 제133조 제1항 | 5년 이하 징역 또는 2천만원 이하 벌금 | fine_or_greater |
| `offense.bribe_delivery_receipt` | 증뢰물전달죄 | 제133조 제2항 | 제1항의 형과 같음 | fine_or_greater |
| `offense.obstruction_of_official_duty` | 공무집행방해죄 | 제136조 제1항 | 5년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |
| `offense.coercion_of_official_duty_or_resignation` | 직무·사직강요죄 | 제136조 제2항 | 5년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |
| `offense.deceptive_obstruction_of_official_duty` | 위계공무집행방해죄 | 제137조 | 5년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |
| `offense.harboring_or_escape` | 범인은닉·도피죄 | 제151조 제1항 | 3년 이하 징역 또는 500만원 이하 벌금 | fine_or_greater ※4 |
| `offense.perjury` | 위증죄 | 제152조 제1항 | 5년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |

## E. 문서·인장·방화·주거

| offense_ref | 죄명 | 조문 | 법정형(초안) | 판정 |
|---|---|---|---|---|
| `offense.arson_of_occupied_structure` | 현주건조물등방화죄 | 제164조 제1항 | 무기 또는 3년 이상 징역 | fine_or_greater |
| `derived_offense.arson_causing_injury` | 현주건조물등방화치상죄 | 제164조 제2항 | 무기 또는 5년 이상 징역 | fine_or_greater |
| `derived_offense.arson_causing_death` | 현주건조물등방화치사죄 | 제164조 제2항 | 사형·무기 또는 7년 이상 징역 | fine_or_greater |
| `offense.public_document_forgery` | 공문서위조·변조죄 | 제225조 | 10년 이하 징역 | fine_or_greater |
| `offense.false_public_document_creation` | 허위공문서작성죄 | 제227조 | 7년 이하 징역 또는 2천만원 이하 벌금 | fine_or_greater |
| `offense.private_document_forgery` | 사문서위조·변조죄 | 제231조 | 5년 이하 징역 또는 1천만원 이하 벌금 | fine_or_greater |
| `offense.use_of_forged_private_document` | 위조사문서행사죄 | 제234조 | 제231조의 예에 의함 | fine_or_greater |
| `offense.seal_forgery_or_misuse` | 사인등의위조·부정사용죄 | 제239조 제1항 | 3년 이하 징역 | fine_or_greater |
| `offense.dwelling_intrusion` | 주거침입죄 | 제319조 제1항 | 3년 이하 징역 또는 500만원 이하 벌금 | fine_or_greater |
| `offense.refusal_to_leave` | 퇴거불응죄 | 제319조 제2항 | 3년 이하 징역 또는 500만원 이하 벌금 | fine_or_greater |

---

## 판정 주의 — 여기만 봐 주셔도 됩니다

**※1 점유이탈물횡령죄(제360조)** — 선택형에 **과료**가 들어 있는 유일한 행이다.
법정형에 1년 이하 징역과 300만원 이하 벌금이 함께 있으므로 "벌금 이상의 형에 해당하는 죄"에
해당한다고 보았다. 즉 기준은 **가장 무거운 선택형**이고 과료가 병기되어 있다는 사정은 영향이
없다는 전제다.

> **검수 ㉮** 이 전제가 맞는가? (여기가 이 워크시트에서 유일하게 실질적으로 갈릴 수 있는 자리다.)
>
> **2026-08-15 결재: 승인.** 제360조는 징역·벌금·과료를 선택형으로 두므로 과료가 함께
> 있다는 이유로 threshold에서 빠지지 않는다. 형법 제41조도 징역·금고·자격정지·벌금을
> 구류·과료보다 위에 둔다.

**※2 과실범(제267조·제268조)** — 자유형이 **징역이 아니라 금고**다. 금고는 벌금보다 무거운
형(형법 제41조의 형의 경중)이므로 `fine_or_greater`로 보았다.

> **검수 ㉯** 동의하는가? — **2026-08-15 결재: 승인.**

**※3 자격정지 선택형** — 제122조·제127조·제129조·제130조는 선택형에 자격정지가 있고 벌금이
없다. 그러나 징역·금고가 함께 규정되어 있으므로 벌금 이상이다. 자격정지만 있는 죄가 아니다.

> **검수 ㉰** 동의하는가? — **2026-08-15 결재: 승인** (표현을 「병과형」에서 「선택형」으로 교정).

**※4 제151조 자신** — 범인은닉·도피죄 자체도 벌금 이상이다. 도피시킨 자를 다시 도피시킨 사안
(연쇄 은닉)에서 필요하므로 값을 채운다. 지금 KCL 26문항에 그런 사안은 확인되지 않았다.

---

## 일괄 판정

63개 전부 `fine_or_greater`가 초안이다. `below_fine`은 **0개**다.

이것이 실질적으로 "형법각칙은 다 해당한다"와 같은 결론이라는 점은 인정한다. 그럼에도 값을
저작하는 이유는 host가 그 결론을 **가정하지 않게** 하기 위해서다. 새 죄가 저작되면 값이
없는 상태(UNKNOWN)로 들어오고, 그때 이 표에 한 줄을 추가할지 판단하게 된다.

> **검수 ㉱ — 2026-08-15 결재: 63행 `class: fine_or_greater` 일괄 승인.** 저작 완료.
> 사기죄 법정형과 ※3 표현은 이 결재에서 교정했고, `class` 판정에는 영향이 없다.

승인되면 두 YAML(`offenses.yaml`, `derived_offenses.yaml`)에 다음 형태로 저작한다.

```yaml
article151_penalty_threshold:
  class: fine_or_greater
  authority_refs:
    - {authority_basis: statute_text, citation: "형법 제329조"}
```

`authority_refs`는 각 행의 조문을 그대로 쓴다 — 나중에 개정으로 값이 바뀔 때 어디를 다시
봐야 하는지가 남는다.
