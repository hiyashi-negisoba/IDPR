# 재산죄 RuleIR 생성 단위 설계 (승인용)

작성일: 2026-07-25 · 상태: **단위 확정 · preflight 대기** · 입력: 검토완료 core **480장**
(재산죄 422 + 보강 3조문 58, 결정 B-3 병합 반영)

사용자 결정(2026-07-25): **RuleIR 단위는 죄명이다.** 횡령·배임처럼 같은 조문의 항으로 갈리는
것도 분리한다. 친족상도례처럼 독립 죄명이 아닌 것의 처리를 함께 정한다.

---

## 1. 왜 조문이 단위가 될 수 없는가

계약이 막는다. `validate_full_rule_ir_generation`은 RuleIR과 NormCardSet의 `issue_tag` 일치를
요구하고(`src/idpr/rulegen/__init__.py:701`), M5 라우터는 쟁점 태그로 규칙집합을 고른다. 조문을
단위로 잡으면 제355조 하나가 횡령과 배임이라는 **두 죄명의 규칙을 한 규칙집합에** 담게 되고,
라우터가 "횡령 쟁점"으로 부른 규칙집합 안에서 배임 요건이 함께 발화한다.

카드셋을 조문별로 조립한 것(`data/rulegen/property/core_norm_card_sets/art*.json`)은 검증을
그 조문의 후보·commentary에 대해 걸기 위한 것이고, RuleIR 입력은 여기서 죄명 단위로 재집계한다.

## 2. 분할 신호는 데이터에 이미 있다

**제355조 (93장)** — `comment_id`에 항이 박혀 있다(`comm_001692_제355조_1항_Ⅲ.2_36`).
**1항(횡령) 60장 / 2항(배임) 33장, 혼합 0장.** 항을 걸치는 카드가 하나도 없어 기계적 분할이 된다.

**제356조 (17장)** — 항 표시가 없다. 대신 절 구조가 갈라 준다.

| 절 | 내용 | 장수 | 귀속 |
|---|---|---:|---|
| Ⅲ.1 | 업무상 보관 | 3 | 업무상횡령 |
| Ⅱ.2 `unrelated_possession` | 업무 무관 보관은 업무상횡령 불성립 | 1 | 업무상횡령 |
| Ⅲ.2 | 업무상 타인의 사무 처리 | 3 | 업무상배임 |
| Ⅰ, Ⅱ.1, Ⅱ.2(나머지), Ⅲ.3 | 업무자 신분·업무 개념·지위 인식 | 10 | **양쪽 공유** |

제356조는 독립 죄명이 아니라 **가중신분(업무자)** 을 정하는 조문이다. 업무 개념 카드 10장은
업무상횡령과 업무상배임이 똑같이 쓴다. 한쪽에 넣으면 다른 쪽이 비고, 양쪽에 복제하면 두 벌이
갈라진다 — 친족상도례와 같은 문제다(§4).

## 3. 제안 단위 (죄명 9 + 공유 모듈 2)

| # | `issue_tag` | 죄명 | 구성 | 카드 |
|---|---|---|---|---:|
| 1 | `theft` | 절도(야간주거침입·특수·상습 포함) | art329 40 + art330 7 + art331 9 + art332 9 + art342 1 | 66 |
| 2 | `robbery` | 강도류(기본·특수·준강도·상해치상·살인치사·예비음모) | art333 42 + art334 7 + art335 26 + art337 7 + art338 10 + art343 6 | 98 |
| 3 | `extortion` | 공갈 | art350 41 | 41 |
| 4 | `embezzlement` | 횡령·업무상횡령 | art355 1항 60 + art356 Ⅲ.1·`unrelated_possession` 4 | 64 |
| 5 | `breach_of_trust` | 배임·업무상배임 | art355 2항 33 + art356 Ⅲ.2 3 | 36 |
| 6 | `breach_of_trust_bribe` | 배임수증재 | art357 41 | 41 |
| 7 | `lost_property_embezzlement` | 점유이탈물횡령 | art360 14 | 14 |
| 8 | `property_damage` | 재물손괴 | art366 53 | 53 |
| 9 | `interference_with_exercise_of_right` | 권리행사방해 | art323 32 | 32 |
| S1 | `occupational_status` | (공유) 업무자 가중신분 | art356 Ⅰ·Ⅱ·Ⅲ.3 10 | 10 |
| S2 | `relative_property_crime_exception` | (공유) 친족상도례 | art328 25 | 25 |
| | | | **합계** | **480** |

**가중유형을 기본죄와 한 단위에 두는 이유.** 특수절도는 절도의 가중유형이고 절취·불법영득의사
요건을 그대로 쓴다. 별도 규칙집합으로 쪼개면 기본 요건 카드를 복제해야 하고 두 벌이 갈라진다.
같은 단위 안에서 `special_theft_established :- theft_established, <야간·흉기·합동 요건>` 형태의
**가중 스트라텀**으로 얹는 것이 안전하다. 강도류도 같다.

**KCL 문항 태그와의 대응.** 문항 태그(`theft`, `special_theft`, `extortion`, `embezzlement`,
`breach_of_trust`, `damage`, `relative_property_crime_exception`, `offense_subject_to_complaint`…)는
이 단위 위에 그대로 얹힌다. `special_theft`처럼 가중유형 태그는 단위 안의 스트라텀을 가리킨다.

**강도 기본조문 누락 — 자산 부재가 아니라 선별 누락이었다(2026-07-25 정정).** `robbery` 단위에
"폭행·협박으로 반항을 억압하고 재물을 강취한다"는 기본 요건이 없는 것은 사실이다. 그 원인을
처음에 "주석서 코퍼스 부재"로 적었으나 **오독이었다.** 원천 파싱본
(`sp_qwen/data/serve/commentary_chunks/docs.parquet`, 형법 4,011 chunks / 251 조문)에 제333조
[강도] **51 chunks가 절 구조까지 온전히** 들어 있고(Ⅱ.3 피해자의 반항억압 6 chunks가 핵심),
원본 PDF도 있다(`sp/commentary_criminal.zip → casenote_pdfs/044_제333조 [강도].pdf`, 373개 PDF).
IDPR 번들(3,108 chunks / 96 조문)이 KCL 태그 매핑에서 빠뜨린 것이다.

보강 대상은 기존 카드가 이미 전제하는 조문으로 한정했다 —
`scripts/extend_commentary_bundle.py`, 산출 `kcl_criminal_v1_commentary_supplement.jsonl` +
요청 JSONL 3개, 매니페스트 `data/rulegen/campaign/kcl_supplement_manifest.json`.

| 조문 | chunks | 배치 | 추정 | 보강 근거 |
|---|---:|---:|---:|---|
| 제333조 [강도] | 51 | 4 | $2.60 | robbery 단위의 기본 구성요건 |
| 제332조 [상습범] | 15 | 2 | $0.76 | `art329_sec8_3` 상습절도 카드가 전제 |
| 제330조 [야간주거침입절도] | 5 | 1 | $0.25 | `art328_sec4_1`·`art329_sec8_3`이 전제 |
| | **71** | **7** | **$3.61** | 실측 $0.0508/chunk 적용 |

제336·339·340조(인질강도·강도강간·해상강도)는 KCL 61문항이 묻지 않아 제외했다. 친족 준용
조문(제344·354·361·365조)은 §4.2의 결정에 따라 절차 레이어와 함께 다룬다.

**실적(2026-07-25, job 213426)**: 9분 17초, 실지출 **$4.87**(견적의 135%). 다운스트림 비용이
chunk가 아니라 **모듈 수 고정비**(스키마+gold exemplar 프롬프트)에 지배된다 — 제330조는 5 chunks에
5 모듈로 $0.102/chunk, 제333조는 51 chunks에 28 모듈로 $0.0525/chunk. 소규모 조문 견적은 모듈 수로
잡는다. 카드 145장 → 전수 판독 후 core 59장이 합류해 `robbery` 99장 / `theft` 66장이 됐다.

## 3.1 가중유형은 기본범과 분리해 on/off로 판정한다 (사용자 요청 2026-07-25)

가중유형을 기본죄와 같은 **단위**에 두는 것과, 규칙에서 **구별되게** 판정하는 것은 다른 문제다.
사용자 요청은 후자다 — 상습절도·야간주거침입절도·강도치상·강도치사가 기본범과 구별되어 켜졌다
꺼지게 하라는 것. 출력 술어를 세 층으로 나눈다.

```
// 1층 — 기본범 성립 (단위마다 하나)
theft_established(case_id, defendant_id, victim_id)
robbery_established(case_id, defendant_id, victim_id)

// 2층 — 가중유형 플래그 (열거된 kind만)
theft_aggravation(case_id, defendant_id, kind)      // nighttime_residential | special | habitual
robbery_aggravation(case_id, defendant_id, kind)    // special | quasi | injury | death | preparation
embezzlement_aggravation(case_id, defendant_id, occupational)   // 제356조 공유 모듈이 배출

// 3층 — 죄명 확정
charge(case_id, defendant_id, label) :- <crime>_established(...), <가중 조합>.
```

이 구조를 택하는 이유가 넷이다.

1. **기본 요건 카드가 한 벌만 존재한다.** 절취·불법영득의사 카드를 야간주거침입절도용으로 복제하지
   않는다. 가중유형은 기본범이 성립한 위에 조건을 얹는다.
2. **문항이 묻는 형태와 같다.** KCL은 "야간주거침입절도인가 절도인가"를 묻는다. 플래그가 꺼지면
   자동으로 기본범으로 내려가므로 결론이 비지 않는다.
3. **어느 카드가 어느 플래그를 켜는지 추적된다.** 제332조 습벽 카드들이 `habitual`을 켜고,
   `different_offense_types`처럼 근거를 제한하는 카드가 그 플래그를 끈다.
4. **결과적 가중범의 전제를 명시할 수 있다.** `injury`·`death`는 `art337_sec3.injury_result_violence_intent`
   (상해의 고의는 없어도 폭행의 고의는 있어야 한다)를 전제조건으로 요구한다. 이 층 분리가 없으면
   그 요건이 기본범 요건과 섞인다.

preflight 10항목에 "단위별 가중유형 열거와 플래그 전제조건"을 정식 항목으로 넣는다.

## 4. 친족상도례를 어떻게 담을 것인가

### 4.1 성질 — 층이 다르다

주석서 카드가 직접 말해 준다: "제328조 제1항의 형 면제는 **범죄 성립에는 영향이 없고 형벌만
면제하는 인적 처벌조각사유**이다." 2항은 친고죄(소추조건)다. 즉 친족상도례는 구성요건·위법성·
책임 어디에도 들어가지 않고 **성립 판단이 끝난 뒤의 처벌·소추 층**에서 작동한다.

준용 범위도 죄명마다 다르다(제344조 절도, 제354조 사기·횡령·배임, 제361조 장물, 손괴는 제외).
즉 "어느 죄명에 적용되는가" 자체가 규칙이다.

### 4.2 세 가지 안

**A안 — 죄명 규칙집합마다 복제.** 9개 RuleIR에 친족 규칙을 각각 넣는다. 준용 범위가 죄명별로
다른 것을 각 규칙집합이 따로 표현하게 되고, 개정·헌재 결정 반영을 9곳에 해야 한다. 카드 25장을
9번 복제하면 검증기의 "RuleIR omits approved cards" 대조도 단위마다 갈린다. **비권장.**

**B안 — 독립 규칙집합 + 브리지 술어. (권장)** 친족상도례를 자체 `issue_tag`
(`relative_property_crime_exception`)를 가진 NormCardSet/RuleIR로 만들고, 죄명 규칙집합은 성립
결론을 **공통 브리지 술어**로 배출한다. 친족 규칙집합은 그 술어와 신분관계 사실만 입력으로 받는다.

```
// 죄명 규칙집합이 공통으로 배출 (9개 단위 모두 같은 시그니처)
property_crime_established(case_id, crime_id, defendant_id, owner_id, possessor_id)

// 친족 규칙집합 (issue_tag = relative_property_crime_exception)
kinship_applicable_crime(crime_id)                        // 준용조문이 정한 죄명 화이트리스트
kinship_relation(case_id, person_a, person_b, relation)    // 민법 기준 신분관계 사실
exempt_relation(case_id, defendant_id)                     // 제328조 1항 대상 관계
complaint_relation(case_id, defendant_id)                  // 제328조 2항 대상 관계
complaint_filed(case_id, defendant_id)

punishment_exempt(case_id, defendant_id, crime_id) :-
    property_crime_established(case_id, crime_id, defendant_id, owner_id, possessor_id),
    kinship_applicable_crime(crime_id),
    exempt_relation(case_id, defendant_id).                // 소유자·점유자 모두 요구되는지는 카드가 정함

punishable(case_id, defendant_id, crime_id) :-             // 부정을 쓰므로 최종 스트라텀
    property_crime_established(...), case_assessment_complete(case_id, defendant_id),
    not punishment_exempt(...), (not complaint_relation(...) ; complaint_filed(...)).
```

이 구조의 이점이 네 가지다. ① 준용 범위를 `kinship_applicable_crime` 한 곳에서 관리한다.
② 헌재 2024.6.27. 결정(제328조 1항 적용중지)이나 장애인복지법 연계(2022.1.28 시행) 같은
**시행일 조건**을 한 곳에만 넣는다 — 이미 그런 카드가 있다
(`art328_sec6_3.disabled_victim_abuse_crimes_no_application`). ③ 성립과 처벌을 분리해 두면
"죄는 되지만 처벌되지 않는다"를 IRAC 결론에서 정확히 쓸 수 있다(무죄와 구별). ④ KCL 문항 태그가
이미 `relative_property_crime_exception`·`offense_subject_to_complaint`로 **별개 쟁점으로 분리해
묻고 있다** — 라우터가 그 태그를 보고 두 규칙집합을 함께 로드하면 된다.

**C안 — 총칙 수정요소(modifier) 레이어로 일반화.** 친족상도례·미수·공범·절차 gating을 모두
"성립 판단 뒤에 얹히는 수정요소" 한 층으로 추상화한다.

### 4.3 사용자 결정 (2026-07-25) — 친족상도례는 절차 레이어에서

**친족상도례 배선은 A4 절차 레이어 작업으로 넘긴다.** 형 면제(1항)와 친고죄(2항)는 성립이 아니라
처벌·소추 층이고, 이는 절차 레이어가 다루는 층과 같다. 소추조건은 특히 절차 쟁점 그대로다
(고소의 존재·고소기간·고소취소). 성립 층에서 억지로 배선하지 않고 절차 레이어의 수정요소로
붙이는 것이 층 구분에 맞다 — 실질적으로 C안을 절차 트랙에서 실현하는 것이다.

지금 재산죄 트랙에서 할 일은 **카드를 독립 모듈로 떼어 두는 것까지**다
(`rule_ir_units/relative_property_crime_exception.json` 25장, 계약 통과). 브리지 술어
`property_crime_established`는 죄명 RuleIR이 배출하도록 preflight에 넣어 두고, 그것을 받는 쪽
규칙은 A4에서 작성한다. 친족 준용 조문(제344·354·361·365조) 주석서 보강도 그때 함께 한다.

### 4.3 같은 처리가 필요한 나머지

- **업무자 가중신분(제356조 공유 10장)** = S1. 친족상도례와 같은 브리지 구조로, 업무상횡령·
  업무상배임 두 단위가 `occupational_status_established(case_id, defendant_id)`를 참조한다.
  다만 이쪽은 처벌 층이 아니라 **가중 스트라텀**이므로 성립 판단 안에서 작동한다.
- **제342조 미수(1장, "제329조 내지 제341조의 미수범은 처벌된다")** — 독립 단위가 아니라 각
  죄명 단위의 `attempt` 스트라텀이 참조하는 처벌근거다. `theft`에 넣고 `robbery`에서도 같은
  술어를 쓴다(카드는 한 장이므로 복제하지 않고 단위 간 공유 술어로 둔다).
- **제343조 강도예비·음모(6장)** — `robbery` 단위 안의 예비 스트라텀.

## 5. 비용 — 사기 실측 기준

사기 RuleIR 1회 실측(88장): terra 생성 prompt 40,366 + completion 4,606 = **$0.17**,
sol 비평 prompt 66,754 + completion 3,322 = **$0.43** → 죄명당 **$0.60**.

재산죄는 단위당 평균 38장(사기의 43%)이라 프롬프트가 그만큼 작다. 단위 11개 × 약 $0.30 →
**$3.3 내외**. 기존 견적($3.2)과 일치한다. 잔여 예산에 영향이 없는 규모다.

## 6. 착수 순서

1. ~~단위 표 승인~~ · ~~죄명 단위 재집계~~ — 완료(2026-07-25). 단위 11개 / 422장 계약 통과
   (`data/rulegen/property/rule_ir_units/`, 매니페스트 `rule_ir_unit_manifest.json`).
   친족상도례는 모듈로 떼어만 두고 배선은 A4 절차 레이어로 이월(§4.3).
2. **보강 추출 착수 승인** — 제333·332·330조 71 chunks, **$3.61**. requests 생성 완료
   (`kcl_supplement_manifest.json`, status `requests_ready_pending_budget_approval`).
   `run_property_campaign.py` 경로를 재사용하고 **sbatch로 제출**한다. 산출 카드는 재산죄와 같은
   축으로 core 판정 후 `robbery`·`theft` 단위에 합류한다(HITL 1회 추가).
3. ~~보강 추출~~ — 완료(job 213426, $4.87). core **480장** / 단위 11개 계약 통과
   (`robbery` 99 · `theft` 66). 결정 B-3까지 반영해 질의문 13 + 면제 6 확정.
4. preflight 10항목 승인 — 단위별 출력 술어·**가중유형 열거와 플래그 전제조건(§3.1)**·행위자
   역할·증거 게이트·브리지 술어 시그니처.
5. RuleIR 생성 + sol 비평 (~$3.5, 예산 게이트, sbatch).

**순서 주의(해소됨)**: 보강 추출을 RuleIR보다 먼저 끝냈으므로 `robbery` 규칙집합은 한 번만 만든다.

관련: `idpr_remaining_work.md` A3 · `rulegen_sweep_cost_estimate.md` §9 ·
`data/rulegen/property/core_norm_card_set_ledger.json`
