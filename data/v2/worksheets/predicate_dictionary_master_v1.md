# Predicate 사전 전체 통합 검수 게이트 — Master v1

[predicate_dictionary_master_v0.md](predicate_dictionary_master_v0.md)에 대한 사용자
검수 6건을 반영한다. v0는 그대로 둔다 — 이력 추적용.

---

## 정정 1 — 258의2→258 의존성은 기록사항이 아니라 Gate① Blocker

**v0 오류**: §1-C에 "부수 커버리지 의존성(HOLD 아님, 기록용)"으로만 적었다. 그러나
258(중상해·존속중상해)이 아직 어느 배치에서도 저작되지 않은 채로 258의2의 QUALIFY
대상 4개 중 2개가 허공을 참조하는 상태로 Gate①을 통과시키면, 2-pass 착수 즉시 "새
predicate 저작이 필요한 조문"이 튀어나온다 — 이 게이트가 막으려는 바로 그 상황이다.

**확인**: `data/rulebase/article_catalog.json`(KCL 평가가 대응하는 51개 조문의
근거 목록)에 258(단독)은 애초에 포함되어 있지 않다(258의2만 `art2582_2`로 포함).
즉 258은 처음부터 이번 트랙의 80개 population 목표에 든 적이 없다 — "누락된 조문"이
아니라 "애초에 범위 밖인 조문에 QUALIFY가 걸쳐 있는" 문제다.

**v1(결정)**: 258의2를 **257 연동 2갈래(상해·존속상해 가중)만으로 이번 게이트를
통과**시킨다. 258 연동 2갈래(중상해·존속중상해 가중)는 258 자체가 population 대상에
추가되기 전까지 QUALIFY 확장을 명시적으로 보류한다 — 258의2 최종 조립
(`data/v2/definitions/`)도 2-pass에서 257 갈래만 먼저 확정하고, 258 갈래는 258이
별도로 저작된 뒤 QUALIFY를 추가하는 후속 작업으로 남긴다. 아래 §4-0에 Gate① Blocker
항목으로 명시하고 "결정됨(RESOLVED)"으로 닫는다 — 해소 방식(258을 언제 저작할지)은
설계하지 않고, "지금 258 갈래를 descope한다"는 결정만 확정한다.

---

## 정정 2 — 액티브 인벤토리에 남은 폐기·재분류 대상 predicate 3건 정리

**v0 오류**: §2.8이 pilot 시점 정보를 그대로 옮기면서 이미 폐기됐거나 이번 게이트에서
새로 재분류해야 할 predicate 3건을 액티브 표에 남겨뒀다.

1. **`doctrine.quasi_robbery`** — 표 자체가 "(→335 DerivedOffenseDef로 확정)"이라고
   써놓고도 여전히 액티브 doctrine 행으로 존재하는 자기모순. 배치⑫ 최종본(335절)을
   재확인한 결과 335의 최종 구조는 `purpose_to_resist_recapture`/`purpose_to_avoid_
   arrest`/`purpose_to_conceal_evidence` 3개 legal_element + `DerivedOffenseDef`
   뿐이고 `doctrine.quasi_robbery` 자체는 최종 predicate 세트에 없다.
2. **`doctrine.complete_suppression_becomes_robbery`**(350) — "공갈이 불성립하고
   강도로 평가된다"는 cross-offense 전환 서술이다. 배치⑦ 이후 이 프로젝트가 반복
   확정해온 원칙("다른 죄로 전환/구성요건 불해당을 doctrine으로 만들지 않는다" —
   130의 `third_party_recharacterized_as_direct_bribery`, 136의 `illegal_duty_
   act_reduces_to_general_offense` 등 동종 5건이 이미 이 원칙으로 삭제됨)을 이
   predicate에는 소급 적용한 적이 없었다. 이번 게이트에서 같은 원칙을 적용해
   재분류한다.
3. **`legal_element.property_of_another`**(360) — 아래 정정4(A-3)에서 `object_
   ownership_other`(366)로 canonical 통합이 확정되면서 폐기.

**v1(수정)**: 세 항목 모두 §2.8 액티브 표에서 제거하고 §6 부록에 "이번 게이트에서
새로 재분류/폐기"로 옮긴다(기존 배치가 이미 삭제한 목록과 구분).

---

## 정정 3 — A-3(360↔366)은 canonical ID까지 이번 게이트에서 확정

**v0 오류**: A-3을 "재사용 확정"이라 판정하면서도 "object_ownership_other를 쓸지
공통 id로 통합할지는 2-pass에서 결정"이라고 남겨뒀다. Gate①은 predicate ID freeze
단계이므로 이 자체가 모순이다.

**v1(수정)**: **canonical id = `legal_element.object_ownership_other`**(366, pilot
draft 소속 — 배치⑫ 360보다 먼저 확정된 선행 id). `legal_element.property_of_another`
(360)는 폐기하고, 360은 `object_ownership_other`를 직접 재사용한다.

---

## 정정 4 — §3-2 ID 문제 2건을 지금 확정, `violence_used`는 명시적 B 항목으로 승격

**v1(수정)**:
- `legal_element.injury_result`(구 `injury_occurred`) — **canonical id 확정**(제안이
  아니라 확정). 배치⑨ 원본 워크시트 파일 자체는 이력 보존을 위해 고치지 않지만, 이
  마스터 문서와 2-pass 저작은 이 이름을 쓴다.
- 323의 `legal_element.taking_conduct` → **`legal_element.taking_of_own_property_
  conduct`로 개명 확정**(329의 `ground_fact.taking_conduct`와 완전히 분리, 접두사
  근접 충돌 해소).
- `ground_fact.violence_used`(257) — v0가 "미확정"이라고만 인벤토리에 적어두고
  HOLD 목록에는 안 올렸던 누락을 정정. 배치⑨ 저자 자신도 v0·v1 두 라운드 모두 "결정
  하지 않음"으로 유지한 항목이라 이번 게이트에서 임의로 이름을 정하지 않고, **명시적
  B그룹 HOLD로 승격**한다(아래 §4 B-8).

---

## 정정 5 — 21·22·23조 "과잉" doctrine의 stage 미확정을 B그룹에 명시

**v0 오류**: §2.4 표에 "구체 stage 2-pass 미확정"이라고만 흘려 적고 HOLD 목록에는
올리지 않았다 — 액티브 최종 doctrine인데 stage(Unlawfulness/Culpability/
Punishability 중 어디인지)가 없는 상태로 방치됐다.

**원문 재확인**(`predicate_dictionary_draft_v0~v2.md`의 21조, `predicate_dictionary_
ext_batch03_v0/v1.md`의 22·23조를 직접 열람): 21조 `doctrine.excessive_defense`는
pilot v0-v2 내내 "정황에 따라 형 감면·불벌"이라는 canonical_meaning만 있고 formal
stage가 배정된 적이 없다. 배치③ v1이 22·23조의 `excessive_necessity`/`excessive_
self_help`를 Unlawfulness DEFEAT에서 downstream(MODIFY/EXEMPT)으로 재분류하면서
저자 스스로 다음과 같이 명시했다: **"정확한 stage(culpability vs punishability)는
아직 확정된 적이 없다... 22·23조가 21조를 따라갈 것이 아니라 셋을 동시에 정한다(21조도
아직 미정이므로)."** 즉 이건 마스터 v0가 놓친 게 아니라 원본 배치들이 처음부터
미확정으로 명시해둔 항목이다 — 복원할 확정본이 없다.

**v1(수정)**: 아래 §4 B-9로 명시 등재. §2.4의 세 doctrine 행에 cross-reference 추가.

---

## 정정 6 — `bundle.omission_bundle`의 잘못된 재사용처 표기 삭제

**v0 오류**: §2.1에서 `bundle.omission_bundle`의 재사용처를 "22조 `conflict_of_
duties_defeat`의 전제"라고 적었다. 원문(`predicate_dictionary_ext_batch03_v0/v1.md`)을
재확인한 결과 `conflict_of_duties_defeat.requires`는 `ALL(conflicting_legal_duties,
higher_or_equal_duty_performed)`뿐이고 `omission_bundle`을 requires에 직접 참조하지
않는다 — "그 doctrine이 성립하려면 대상 offense의 Elements(`omission_bundle` 포함)가
먼저 충족돼 있어야 한다"는 것은 stage 파이프라인 순서(Elements→Unlawfulness)의
일반 원리이지, `omission_bundle`을 doctrine이 predicate로 "재사용"하는 관계가
아니다. 이 표기를 그대로 두면 2-pass 저작 시 `requires`에 `omission_bundle`을
중복 삽입하는 오류를 유발할 수 있다.

**v1(수정)**: §2.1에서 해당 재사용처 표기 삭제.

---

## 최종 상태 (v1) — 전체 문서

이하 §1-§6은 v0 전체를 위 6건 정정을 반영해 다시 수록한 것이다(마스터 문서는
diff가 아니라 2-pass 저작의 단일 출처여야 하므로 전문 유지).

---

## 1. 커버리지 체크리스트 (80개 조문)

### 1-A. 총칙 (28개, 9-36조)

| 조문 | 확정 series/버전 | 비고 |
|---|---|---|
| 9 | batch01 | |
| 10 | draft(v0-v2) + **batch01_v1 소급 재작성** | ALIC 구조 전면 대체, 최종본은 batch01_v1 |
| 11 | batch01 | |
| 12 | batch01(v0→v1) | |
| 13 | batch02 | |
| 14 | batch02(v0→v1) | `negligence_bundle` 4분해 |
| 15 | batch02(v0→v1→v2) | `mistake_bundle` 구조 미확정(2-pass 이월, §4 B-5) |
| 16 | batch01 | |
| 17 | batch02 | 신규 predicate 없음 |
| 18 | batch02(v0→v1→v2) | |
| 19 | batch02(v0→v1→v2) | v0의 "architecture gap" 오판을 v1이 철회 |
| 20 | batch03(v0→v1) | |
| 21 | draft(v0→v2) | `excessive_defense` stage 미확정(§4 B-9) |
| 22 | batch03(v0→v1→v2) | `excessive_necessity` stage 미확정(§4 B-9) |
| 23 | batch03(v0→v1) | `excessive_self_help` stage 미확정(§4 B-9) |
| 24 | batch03(v0→v1) | |
| 25 | draft(v0→v2) | |
| 26 | draft(v0→v2) | |
| 27 | draft(v0→v2) | |
| 28 | batch04(v0→v2) | |
| 29 | batch04 | 신규 predicate 없음 |
| 30 | draft(v0→v1) | |
| 31 | draft(v0→v2) | |
| 32 | draft(v0→v2) | |
| 33 | batch05(v0→v3) | 본문·특수문제=확정, 단서=orchestration 확인(HOLD, 아래 C-33b) |
| 34 | batch05(v0→v3) | `supervisory_relationship` 1개만 확정, mode/구조 2-pass 이월(HOLD, 아래 C-34) |
| 35 | batch06(v0→v1) | |
| 36 | batch06 | **population 대상 아님**(순수 절차 조문, HOLD 아님 — 애초에 대상 밖) |

### 1-B. 각칙 (52개 = 재산죄 core 7 + 배치⑦-⑫ 44 + art339 1)

| 조문 | 확정 series/버전 | 비고 |
|---|---|---|
| 329 절도 | draft(v0→v2) | |
| 333 강도 | draft(v0→v2) | |
| 347 사기 | draft(v0→v2) | |
| 350 공갈 | draft(v0→v2) | `complete_suppression_becomes_robbery` 재분류(§6) |
| 355 횡령·배임 | draft(v0→v2) | |
| 357 배임수재·증재 | draft(v0→v2) | |
| 366 재물손괴 | draft(v0→v2) | `object_ownership_other`가 360과 공유하는 canonical id로 확정(A-3) |
| 122 직무유기 | batch07(v1) | |
| 127 공무상비밀누설 | batch07(v1) | |
| 129 수뢰·사전수뢰 | batch07(v1→v3) | |
| 130 제3자뇌물제공 | batch07(v1→v2) | |
| 133 뇌물공여·증뢰물전달 | batch07(v3) | ①②**별도 OffenseDef 2개** 확정 |
| 136 공무집행방해 | batch07(v1) | |
| 137 위계공무집행방해 | batch07(v0) | |
| 151 범인은닉·도피 | batch07(v3) | `offender_status_of_object` HOLD(아래 C-151) |
| 152 위증·모해위증 | batch07(v1→v2) | |
| 164 현주건조물등방화·치사상 | batch08(v0→v1) | |
| 225 공문서위조·변조 | batch08(v0→v1) | |
| 227 허위공문서작성 | batch08(v1) | |
| 231 사문서위조·변조 | batch08(v0) | |
| 234 위조사문서행사 | batch08(v1) | |
| 239 사인등의 위조·부정사용 | batch08(v1) | 238조 원문 직접 열람으로 확정 |
| 250 살인·존속살해 | batch09(v1→v2) | 33조 단서 HOLD 구체 사례(아래 C-33b) |
| 254 살인의 미수범 | batch09(v0) | 독자 predicate 없음 |
| 255 살인의 예비·음모 | batch09(v1) | |
| 257 상해·존속상해 | batch09(v1) | 34조 gap 구체 사례(아래 C-34), `injury_result` canonical 확정(§3-2), `violence_used` 명칭 HOLD(§4 B-8) |
| 259 상해치사 | batch09(v0→v2) | |
| 263 동시범 | batch09(v0) | 19조 participation compatibility(아래 C-263) |
| 267 과실치사 | batch09(v2) | |
| 268 업무상과실·중과실치사상 | batch09(v1) | |
| 258의2 특수상해 | batch09(v0) | **Gate① Blocker 해소**(§4-0) — 257 갈래만으로 게이트 통과, 258 갈래는 후속 |
| 297 강간 | batch10(v1) | |
| 298 강제추행 | batch10(v1) | 34조 gap 구체 사례(아래 C-34) |
| 299 준강간·준강제추행 | batch10(v1) | 예비음모 conduct 갈래 HOLD(아래 B) |
| 300 강간등의 미수범 | batch10(v1) | 독자 predicate 없음(참조 전용) |
| 301 강간등 상해·치상 | batch10(v1) | 결합범 구조 HOLD(아래 B) |
| 319 주거침입·퇴거불응 | batch11(v3) | 별장 subtype·퇴거불응 미수 HOLD(아래 B) |
| 323 권리행사방해 | batch11(v3) | 33조 본문 gap 구체 사례(아래 C-33a), `taking_of_own_property_conduct`로 개명 확정(§3-2) |
| 328 친족간의 범행 | batch11(v1) | **population 대상 아님**(2025.12.31. 개선입법, 순수 소추조건) |
| 330 야간주거침입절도 | batch12(v1→v4) | |
| 331 특수절도 | batch12(v1→v4) | `dangerous_weapon_carriage` 재사용 확인(아래 A-1) |
| 332 상습절도 | batch12(v0→v4) | |
| 334 특수강도 | batch12(v1→v4) | 신규 predicate 없음 |
| 335 준강도 | batch12(v0→v4) | `occasion_identity` 재사용 확인(아래 A-2), `doctrine.quasi_robbery`는 최종 미채택(§6) |
| 337 강도상해·치상 | batch12(v0→v4) | 337/338 구조 선택 HOLD(아래 B) |
| 338 강도살인·치사 | batch12(v0→v4) | 위와 동일 |
| 342 절도·강도의 미수범 | batch12(v0) | 독자 predicate 없음(참조 전용) |
| 343 강도의 예비·음모 | batch12(v0→v1) | |
| 344 친족간의 범행 준용 | batch12(v1) | **population 대상 아님**(328과 동일 사유) |
| 356 업무상횡령·배임 | batch12(v0→v1) | QUALIFY 2개(횡령/배임) 분리 |
| 360 점유이탈물횡령 | batch12(v0→v4) | `property_of_another` 폐기, `object_ownership_other`(366) 직접 재사용 확정(A-3) |
| 339 강도강간 | art339(v0→v4) | CompletionPolicy active HOLD(아래 C-339), 신규 predicate 0건 |

**검산**: 총칙 28 + 각칙 52 = **80**. 빠지거나 두 번 배정된 조문 **없음**. Population
대상 아님으로 확정된 조문은 **36·328·344 세 건**.

### 1-C. 부수 커버리지 의존성 — 258은 §4-0에서 Gate① Blocker로 해소됨
- 300조·342조는 population 대상이지만 독자 predicate가 없다(참조 전용, 커버리지
  결손 아님, HOLD 아님).

---

## 2. Predicate ID 마스터 인벤토리

### 2.1 총칙 전역 재사용 predicate (여러 category에 걸쳐 재사용)

| id | canonical_meaning | 출처 | 이 범위 안 재사용처 |
|---|---|---|---|
| `legal_element.intent` | 객관적 구성요건요소 인식+실현 용인(고의) | 13조 | 전 범위(각칙 전체 offense의 기본 고의) |
| `legal_element.commencement_of_execution` | 구성요건적 행위를 직접 개시함(실행의 착수) | 25조 | 164, 225, 231, 250, 339(D-1 HOLD 원인) 등 |
| `bundle.negligence_bundle` | `ALL(duty_of_care, foreseeability, avoidability, breach_of_duty)` | 14조 | 267, 268 |
| `bundle.omission_bundle` | `ALL(duty_to_act, possibility_to_act, failure_to_act, equivalence_to_commission)` | 18조 | 없음(18조 자체 Elements 전용 — 22조 `conflict_of_duties_defeat`는 파이프라인상 그 뒤 단계에서 평가되나 `requires`에 직접 참조하지 않는다) |
| `bundle.mistake_bundle`(미확정) | `ALL(perceived_fact, actual_fact, mistake_within_same_construct)` | 15조 | — (2-pass 실증 후 확정, 실패 시 (C)로 승격, §4 B-5) |
| `legal_element.preparatory_conduct` | 목적한 범죄를 위한 물적 준비행위 | 28조 | 255, 343 |
| `legal_element.conspiracy_agreement` | 2인 이상 특정 범죄 실행 합의+실질적 위험성 | 28조 | 255, 343 |
| `legal_element.purpose_to_commit_target_offense` | 준비·합의가 특정 범죄 실현 목적으로 이루어짐 | 28조 | 255, 343 |
| `relation.causal_nexus` | base 수단행위와 가중결과 사이 (상당)인과관계(COMPOSE 컴포넌트 간) | 외부(robbery_causing_injury/homicide fixture) | 259, 301, 337, 338 (339는 검토 후 미사용) |
| `relation.occasion_identity` | 본범(base offense) 실행행위와 시간적·장소적으로 근접한 기회 | 외부(6B 강도살인미수 fixture) | 301, 335(A-2 재사용 확정), 337, 338, 339(337·338 경유 재사용) |
| `primitive.aggravated_result_attribution` | 결과적가중범 귀속(예견가능성+상당인과관계) | 외부(fixture) | 164, 259, 301, 337, 338 |
| `legal_element.natural_person_victim_status` | 출생 후 사망하지 않은 자연인, 타인 | 배치⑨(250) | 257, 297, 298, 299 |

### 2.2 책임능력·책임조각 (9-12·16조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `ground_fact.actor_age_under_14_at_act_time` | ground_fact | 행위 당시 만 14세 미만 | 9 |
| `doctrine.juvenile_defeat` | doctrine | 형사미성년자 불벌(DEFEAT) | 9 |
| `legal_element.discrimination_capacity` | legal_element | 사물변별능력 | 10 |
| `legal_element.control_capacity` | legal_element | 변별에 따른 행위제어능력 | 10 |
| `legal_element.self_induced_disorder` | legal_element | 심신장애를 유책하게 자초함 | 10(batch01_v1 소급) |
| `doctrine.insanity_defeat` | doctrine | 책임무능력 → 책임조각(DEFEAT) | 10 |
| `doctrine.diminished_capacity_modify` | doctrine | 한정책임능력 → 임의적 감경(MODIFY), `NOT(self_induced_disorder)` | 10 |
| `legal_element.deaf_mute_status` | legal_element | 농아자(청각+언어기능 모두 결여) | 11 |
| `doctrine.deaf_mute_mandatory_reduction` | doctrine | 필요적 감경(MODIFY) | 11 |
| `ground_fact.coerced_act_performed` | ground_fact | 강제상태 하 특정 행위(raw factual linkage) | 12 |
| `legal_element.irresistible_coercion` | legal_element | 저항불가능한 폭력/방어불가능한 협박 | 12 |
| `legal_element.self_induced_coercion` | legal_element | 강제상태를 유책하게 자초 | 12(v1, 긍정형+NOT) |
| `doctrine.coerced_act_defeat` | doctrine | `ALL(irresistible_coercion, coerced_act_performed, NOT(self_induced_coercion))` → DEFEAT | 12 |
| `legal_element.awareness_of_illegality_lacking` | legal_element | 위법성 불인식 | 16 |
| `legal_element.justifiable_ground_for_mistake` | legal_element | 불인식에 정당한 이유(회피불가능) | 16 |
| `doctrine.mistake_of_law_defeat` | doctrine | 위법성 착오 → 책임조각(DEFEAT) | 16 |

### 2.3 고의·과실·착오·인과관계·부작위·동시범 (13-19조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `legal_element.duty_of_care` | legal_element | 객관적 주의의무 | 14 |
| `legal_element.foreseeability` | legal_element | 결과 예견가능성 | 14 |
| `legal_element.avoidability` | legal_element | 결과 회피가능성 | 14 |
| `legal_element.breach_of_duty` | legal_element | 주의의무 위반 | 14 |
| `ground_fact.perceived_fact` / `ground_fact.actual_fact` | ground_fact | 인식한 사실 / 실제 발생 사실 | 15 |
| `legal_element.mistake_within_same_construct` | legal_element | 법정적 부합(동일 구성요건 내 착오) | 15 |
| `legal_element.foreseeability_of_aggravated_result` | legal_element | 중한 결과 예견가능성(결과적가중범 전용) | 15(80개 범위 안 실사용처 없음) |
| `ground_fact.means_or_object_defect` | ground_fact | 수단·대상 착오로 결과발생 애초 불가능 | 27(불능범) — 15조 착오와 별개 |
| `legal_element.duty_to_act` | legal_element | 보증인적 지위(작위의무) | 18 |
| `ground_fact.possibility_to_act` / `ground_fact.failure_to_act` | ground_fact | 행위가능성 / 부작위 | 18 |
| `legal_element.equivalence_to_commission` | legal_element | 작위와의 동가치성 | 18 |
| `legal_element.concurrent_independent_acts` | legal_element | 의사연락 없는 각자의 별개 실행행위 | 19 |
| `legal_element.same_object_of_result` | legal_element | 동일 객체에 결과 발생 | 19 |
| `legal_element.causal_origin_unascertained` | legal_element | 원인행위 판명 불능(법원이 확정하는 법적 상태) | 19 |

### 2.4 위법성조각 (20-24조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `legal_element.act_pursuant_to_law` / `act_due_to_legitimate_business` | legal_element | 법령에 의한 행위 / 정당업무행위 | 20 |
| `legal_element.act_not_against_social_norms` | legal_element | 사회상규 부적합성 없음(5요소 종합) | 20 |
| `doctrine.justifiable_act_defeat` | doctrine | `ANY(위 3개)` → DEFEAT | 20 |
| `legal_element.infringement_situation` / `defensive_act` / `reasonable_grounds` | legal_element | 침해상황/방위행위/상당성 | 21 |
| `doctrine.self_defense` | doctrine | 정당방위 DEFEAT | 21 |
| `doctrine.excessive_defense` | doctrine | 과잉방위(감면/불벌) — **stage 미확정, §4 B-9** | 21 |
| `legal_element.imminent_danger` / `act_to_avert_danger` / `necessity_of_avoidance` | legal_element | 위난/피난행위/상당성 | 22 |
| `legal_element.duty_bound_to_endure_danger` | legal_element | 위난감수의무자 | 22 |
| `legal_element.conflicting_legal_duties` / `higher_or_equal_duty_performed` | legal_element | 의무충돌/상위·동등의무 이행 | 22 |
| `doctrine.necessity_defeat` | doctrine | 긴급피난 DEFEAT | 22 |
| `doctrine.excessive_necessity` | doctrine | 과잉피난(21조 2·3항 준용) — **stage 미확정, §4 B-9** | 22 |
| `doctrine.conflict_of_duties_defeat` | doctrine | 의무충돌 DEFEAT(`requires=ALL(conflicting_legal_duties, higher_or_equal_duty_performed)`, `omission_bundle`은 requires에 미포함 — §2.1 참고) | 22 |
| `legal_element.claim_unpreservable_by_legal_process` / `act_to_prevent_unenforceability` / `necessity_of_self_help` | legal_element | 청구권보전불능/방지행위/상당성 | 23 |
| `doctrine.self_help_defeat` | doctrine | 자구행위 DEFEAT | 23 |
| `doctrine.excessive_self_help` | doctrine | 과잉자구행위(21조 2항만 준용) — **stage 미확정, §4 B-9** | 23 |
| `legal_element.valid_consent_by_disposer` / `harm_caused_pursuant_to_consent` | legal_element | 유효한 승낙/승낙범위 내 침해 | 24 |
| `legal_element.presumed_consent` / `actual_consent_unobtainable` | legal_element | 추정적 승낙/현실적 승낙 불가능 | 24 |
| `legal_element.statutory_bar_on_consent` / `consent_based_act_not_against_social_norms` | legal_element | 특례규정 없음/사회상규 부합(두 doctrine 공유) | 24 |
| `doctrine.victim_consent_defeat` / `presumed_consent_defeat` | doctrine | 승낙 DEFEAT(현실적/추정적) | 24 |

### 2.5 미수론 (25-29조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `legal_element.voluntary_cessation_or_prevention` | legal_element | 자의에 의한 중지·결과방지(중지범) | 26 |
| `legal_element.dangerousness` | legal_element | 불능미수의 위험성 | 27 |
| `legal_element.voluntary_surrender_before_execution` | legal_element | 실행 전 자수(31조 연결 여부 미확인, 아래 B-7) | 28 |
| `PREPARATION_OR_CONSPIRACY`(CompletionPolicy state) | state | `when=ALL(ANY(preparatory_conduct,conspiracy_agreement),NOT(commencement_of_execution))`, `requires=purpose_to_commit_target_offense` | 28 |

### 2.6 공범론 (30-34조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `legal_element.joint_execution_intent` / `joint_execution_conduct` | legal_element | 공동가공 의사/기능적 행위지배 | 30 |
| `legal_element.instigator_intent` | legal_element | 교사의 고의 | 31 |
| `legal_element.aiding_intent` | legal_element | 방조의 고의 | 32 |
| `legal_element.supervisory_relationship` | legal_element | 피이용자에 대한 지휘·감독 관계 | 34(핵심 predicate만 확정, mode/구조는 2-pass, C-34 참고) |

### 2.7 누범 (35-36조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `ground_fact.prior_sentence_of_imprisonment_or_greater` | ground_fact | 전범 금고 이상 형 선고 | 35 |
| `ground_fact.prior_sentence_execution_completed_or_exempted` | ground_fact | 전범 형집행 종료·면제 | 35 |
| `legal_element.prior_sentence_still_effective` | legal_element | 전범 형선고 효력 유지 | 35 |
| `legal_element.subsequent_offense_within_recidivism_period` | legal_element | 3년 이내 후범 | 35 |
| `doctrine.recidivism_modify` | doctrine | 누범 가중(Punishability MODIFY, 필요적) | 35 |

### 2.8 재산죄 (pilot 7 + 배치⑫ 절도·강도·횡령군)

| id | type | canonical_meaning | 출처 | 재사용 |
|---|---|---|---|---|
| `legal_element.unlawful_appropriation_intent` | legal_element | 불법영득의사 | 329(pilot) | 333, 355, 330, 331, 332, 334, 335, 356, 360 |
| `legal_element.possession` | legal_element | 사실상 지배+점유의사 | 329 | — |
| `ground_fact.taking_conduct` | ground_fact | 타인 점유 재물을 점유자 의사에 반해 자기 점유로 옮김 | 329 | 330, 335 등 |
| `legal_element.robbery_level_violence` | legal_element | 반항억압 정도의 폭행·협박 | 333(pilot) | 334, 335, 337 |
| `legal_element.deception` | legal_element | 기망→착오 | 347 | — |
| `relation.deception_error_disposition_causal_nexus` | relation | 기망→착오→처분 인과관계 | 347 | — |
| `legal_element.fear_inducement` | legal_element | 협박에 의한 외포심 | 350 | — |
| `legal_element.property_disposition` | legal_element | 처분행위 | 347·350 공유(pilot) | — |
| `legal_element.disposition_authority`(미확정) | legal_element | 처분권한(RelationDef 표현 가능성 미확정, §4 B-6) | 347·350(pilot) | — |
| `legal_element.duty_of_other_affairs` | legal_element | 타인 사무 처리자 지위 | 355·357(pilot) | 356 |
| `legal_element.entrustment_relationship` | legal_element | 위탁관계 | 355(pilot) | — |
| `legal_element.custody_of_anothers_property` | legal_element | 타인 재물 보관자 지위 | 355(pilot) | — |
| `legal_element.embezzlement_manifestation` | legal_element | 불법영득의사의 객관적 표현 | 355(pilot) | 356, 360(재사용 확정, A-4) |
| `legal_element.improper_solicitation` | legal_element | 부정한 청탁 | 357(pilot) | — |
| `legal_element.utility_impairment` | legal_element | 효용침해(손괴) | 366(pilot) | — |
| `legal_element.object_ownership_other` | legal_element | 타인 소유물(무주물 제외, 민법상 소유권 귀속 판단) | 366(pilot) | **360이 직접 재사용(canonical 확정, A-3)** |
| `legal_element.valid_claim_exists` / `claim_scope` / `means_socially_acceptable` | legal_element | 유효채권/권리범위/수단상당성 | pilot(333·350 권리행사) | — |
| `legal_element.nighttime_entry` | legal_element | 일몰~일출 사이 침입(시점-내장형) | 330 | 331①, 334 |
| `legal_element.damage_to_entry_barrier` | legal_element | 문·담 등 물리적 훼손 | 331① | — |
| `legal_element.dangerous_weapon_carriage` | legal_element | 흉기(살상·파괴용 또는 준하는 위험성) 소지 | 331② | 334, (258의2 `dangerous_object_carriage`와는 별도 유지, A-1) |
| `legal_element.joint_commission_by_two_or_more` | legal_element | 2인 이상 현장적 협동 | 331② | 334 |
| `legal_element.habitual_theft_propensity` | legal_element | 상습 절도 습벽 | 332 | — |
| `legal_element.purpose_to_resist_recapture` / `purpose_to_avoid_arrest` / `purpose_to_conceal_evidence` | legal_element | 탈환항거/체포면탈/증거인멸 목적 | 335 | — |
| `legal_element.injury_result` | legal_element | 상해 결과(생리적 기능 훼손) — canonical id 확정(§3-2) | 257(배치⑨, 구 `injury_occurred`) | 301, 337 |
| `legal_element.injury_intent` | legal_element | 상해에 대한 별도 고의 | 301(배치⑩) | 337 |
| `legal_element.homicide_intent` | legal_element | 사망 결과에 대한 별도 고의 | 338 | — |
| `legal_element.business_status` | legal_element | 업무상 재물보관·사무처리자 | 356 | — |
| `legal_element.lost_or_stray_property_status` | legal_element | 유실물·표류물 등 점유이탈 재물 | 360 | — |

335의 `doctrine.quasi_robbery`, 350의 `doctrine.complete_suppression_becomes_
robbery`, 360의 `legal_element.property_of_another`는 이번 게이트에서 폐기·재분류
확정 — §6 참고. (334는 신규 predicate 없음. 337·338의 나머지 predicate는
§2.1·§2.11 재사용. 342·343은 §2.5·§2.1 재사용.)

### 2.9 공무원·사법 (122·127·129·130·133·136·137·151·152조)

| id | type | canonical_meaning | 출처 | 재사용 |
|---|---|---|---|---|
| `legal_element.public_official_status` | legal_element | 공무원 지위 | 122 | — |
| `legal_element.duty_has_concrete_lawful_basis` | legal_element | 구체적 법적 근거 있는 직무의무 | 122 | (136의 `lawful_performance_of_duty`와 판단기준 유사하나 actor 방향이 반대라 의도적 분리 유지) |
| `legal_element.concrete_risk_at_time_of_conduct` | legal_element | 행위시 구체적 위험성 | 122 | — |
| `legal_element.duty_abandonment_conduct` / `conscious_abandonment_intent` | legal_element | 직무 방임·포기 / 의식적 방임 고의 | 122 | — |
| `legal_element.current_or_former_public_official` | legal_element | 현직·전직 공무원 | 127 | — |
| `legal_element.job_related_secret_worthy_of_protection` | legal_element | 직무상 보호가치 비밀 | 127 | — |
| `legal_element.disclosure_conduct` | legal_element | 구체적 누설(관공서 간 정상전달 제외 흡수) | 127 | — |
| `doctrine.corruption_report_justified_act` | doctrine | 부패신고 누설 정당행위(DEFEAT) | 127 | — |
| `legal_element.official_or_arbitrator_status` / `job_relatedness` / `quid_pro_quo` / `solicitation_received` | legal_element | 공무원·중재인/직무관련성/대가관계/청탁 | 129 | 130, 133 |
| `ground_fact.bribe_acceptance` / `bribe_request` / `bribe_promise` | ground_fact | 수수/요구/약속 | 129 | `bribe_promise`는 133①의 `completed.when`에도 결합 |
| `legal_element.appropriation_intent_of_bribe` | legal_element | 뇌물 영득의사 | 129 | — |
| `legal_element.prospective_official_probability` | legal_element | 장래 공무원 개연성(사전수뢰) | 129 | — |
| `ground_fact.solicitation_received_before_appointment_timing` | ground_fact | 취임 전 청탁 수령 시점 | 129 | — |
| `legal_element.solicitation_impropriety` | legal_element | 부정한 청탁(130 강화 요건) | 130 | — |
| `ground_fact.third_party_benefit_causation` / `_demand` / `_promise` | ground_fact | 제3자 공여 하게함/요구/약속 | 130 | — |
| `ground_fact.bribe_offer_expression_made` / `_arrived` | ground_fact | 공여 의사표시 발신/도달 | 133① | — |
| `ground_fact.intermediary_delivery_receipt_conduct` | ground_fact | 증뢰물 현실 교부수령 | 133② | — |
| `legal_element.self_benefit_purpose` | legal_element | 제3자 자기이득 목적 수수(+`NOT()`) | 133② | — |
| `legal_element.lawful_performance_of_duty` | legal_element | 적법한 직무집행 | 136 | — |
| `legal_element.violence_or_threat_against_official` | legal_element | 공무원에 대한 폭행·협박 | 136 | — |
| `legal_element.purpose_of_coercing_duty_or_resignation` | legal_element | 직무강요·사직목적(136②) | 136 | — |
| `legal_element.deceptive_scheme_conduct` | legal_element | 위계에 의한 공무집행방해 | 137 | — |
| `ground_fact.concealment_or_escape_conduct` | ground_fact | 은닉·도피(작위·부작위) | 151 | — |
| `legal_element.act_directed_at_another_offender` | legal_element | 타인 지향 은닉·도피 | 151 | — |
| `legal_element.omission_requires_guarantor_status` | legal_element | 부작위 도피의 보증인 지위 | 151 | — |
| `doctrine.relative_cohabiting_family_exemption` | doctrine | 친족비호 처벌면제(**Punishability EXEMPT**) | 151 | — |
| `legal_element.for_the_offenders_benefit` | legal_element | 범인 본인 이익 목적 | 151 | — |
| `legal_element.offender_status_of_object`(**HOLD**) | legal_element | 대상자의 죄질(벌금 이상) — cross-actor dependency | 151 | 아래 §4 C-151 |
| `legal_element.witness_took_lawful_oath` | legal_element | 적법 선서 증인 | 152 | — |
| `ground_fact.false_testimony_conduct` | ground_fact | 허위진술 | 152 | — |
| `ground_fact.correction_before_examination_end` | ground_fact | 신문종료 전 철회·시정 | 152 | — |
| `ground_fact.examination_ended` / `post_oath_completed` | ground_fact | 완료시점(사전/사후선서형) | 152 | — |
| `legal_element.purpose_to_prejudice_specific_party` | legal_element | 모해 목적 | 152 | — |
| `legal_element.proceeding_commenced` | legal_element | 형사·징계절차 개시 중 | 152 | — |

### 2.10 방화·문서 (164·225·227·231·234·239조)

| id | type | canonical_meaning | 출처 | 재사용 |
|---|---|---|---|---|
| `legal_element.arson_target_status` | legal_element | 현주·현존 건조물 등 객체 | 164 | — |
| `legal_element.burning_result` | legal_element | 독립연소 결과 | 164 | — |
| `legal_element.forgery_without_authority` | legal_element | 권한 없는 명의사용 작성·현출 | 225 | 231, 239 |
| `legal_element.alteration_of_genuine_document` | legal_element | 진정문서 내용 변경 | 225 | 231 |
| `legal_element.purpose_to_use_as_genuine` | legal_element | 진정한 것처럼 사용할 목적 | 225 | 227, 231, 239 |
| `legal_element.utterance_conduct` | legal_element | 행사(정을 모르는 자 대상 현출) | 225 | 234, 239 |
| `legal_element.public_document_object` | legal_element | 공문서 객체 | 225 | 227 |
| `legal_element.official_with_writing_authority` | legal_element | 작성권한 있는 공무원 | 227 | — |
| `legal_element.content_falsity_by_authorized_official` | legal_element | 권한자의 허위기재 | 227 | — |
| `legal_element.private_document_object` | legal_element | 사문서 객체 | 231 | — |
| `legal_element.seal_or_signature_object` | legal_element | 인장·서명·기명·기호 | 239 | — |
| `legal_element.improper_use_of_genuine_seal` | legal_element | 진정 인장의 권한 없는/범위 초과 사용 | 239(238조 원문 직접 확인) | — |

### 2.11 생명·신체 (250·254·255·257·259·263·267·268·258의2조)

| id | type | canonical_meaning | 출처 | 재사용 |
|---|---|---|---|---|
| `ground_fact.killing_conduct` | ground_fact | 살해행위(수단불문) | 250 | — |
| `ground_fact.death_of_victim` | ground_fact | 사망 결과 | 250 | 259, 267, 268, 338(외부재사용) |
| `legal_element.result_causation` | legal_element | (death-agnostic 신규) 행위-결과 상당인과관계 | 250 | 267, 268 |
| `legal_element.lineal_ascendant_of_self_or_spouse_status` | legal_element | 자기·배우자 직계존속 | 250 | 257 |
| `legal_element.awareness_of_lineal_ascendant_status` | legal_element | 존속 인식 | 250 | — |
| `legal_element.specific_victim_identified` | legal_element | 살해대상 구체적 확정(예비) | 255 | — |
| `legal_element.injury_result`(§2.8 참고) | legal_element | 상해 결과(생리적 기능 훼손) | 257 | 301, 337 |
| `ground_fact.violence_used`(**HOLD, §4 B-8**) | ground_fact | 상해 수단(유형력/기타 방법) — 이름이 범위보다 좁음 | 257 | — |
| `legal_element.concurrent_independent_acts` / `same_object_of_result` / `causal_origin_unascertained` | legal_element | (19조 재사용) | 외부 | 263 |
| `legal_element.group_or_multiple_force` / `dangerous_object_carriage` | legal_element | 단체·다중 위력 / 위험한 물건 휴대 | 258의2 | `dangerous_object_carriage`는 331 `dangerous_weapon_carriage`와 별도 유지 확정(A-1) |
| `legal_element.occupational_duty_of_care` | legal_element | 업무상 가중 주의의무 | 268 | — |
| `legal_element.gross_negligence` | legal_element | 현저한 주의의무 위반 정도 | 268 | — |

### 2.12 성적 자유 (297·298·299·300·301조)

| id | type | canonical_meaning | 출처 | 재사용 |
|---|---|---|---|---|
| `legal_element.coercive_conduct` | legal_element | 폭행·협박 | 297·298 공유 | — |
| `legal_element.directness_of_coercion_by_offender` | legal_element | 행위자 본인 직접 가함 | 297·298 공유 | — |
| `legal_element.coercion_induced_sexual_act_causation` | legal_element | 폭행·협박→성적행위 인과(death-agnostic 패턴) | 297·298 공유 | — |
| `legal_element.coercion_sufficiency_for_rape` | legal_element | 항거불능/현저곤란 정도 | 297 | — |
| `ground_fact.vaginal_intercourse_conduct` | ground_fact | 성기 삽입·결합 | 297 | 299 |
| `legal_element.coercion_sufficiency_for_forcible_indecency` | legal_element | 낮은 기준(2018도13877 전합) | 298 | — |
| `legal_element.indecent_act` | legal_element | 성적 자유 침해 추행 | 298 | 299 |
| `legal_element.mental_incapacity_or_physical_helplessness_status` | legal_element | 심신상실·항거불능 상태 | 299 | — |
| `legal_element.exploitation_of_incapacity` | legal_element | 그 상태를 이용(객관적 이용관계만) | 299 | — |

### 2.13 주거·권리행사 (319·323조)

| id | type | canonical_meaning | 출처 |
|---|---|---|---|
| `legal_element.dwelling_or_managed_premises_object` | legal_element | 주거·관리 건조물 등 | 319 |
| `legal_element.trespass_entry` | legal_element | 평온을 해하는 침입 | 319 |
| `legal_element.retreat_demand_by_authorized_person` / `justifiable_reason_for_refusal`(+NOT) / `ability_to_comply_with_retreat_demand` / `failure_to_comply_without_delay` | legal_element | 퇴거요구/정당사유/이행가능성/지체 없는 불이행 | 319(퇴거불응) |
| `legal_element.own_property_object` / `third_party_possession_or_right_object` | legal_element | 자기소유물/타인점유·권리객체 | 323 |
| `legal_element.taking_of_own_property_conduct`(개명 확정, §3-2) | legal_element | 자기소유물 취거(불법영득의사 불요) | 323 |
| `legal_element.concealment_conduct` / `damage_conduct` | legal_element | 은닉/손괴 | 323 |
| `legal_element.obstruction_of_right_exercise` | legal_element | 권리행사방해 우려 | 323 |

### 2.14 art339 강도강간

신규 predicate **0건**. 확정된 건 전부 재사용 조합:
- robbery-side candidate refs: `offense.robbery[333/334/335]`(population 대상), `[336]`은 coverage 참조만
- rape_part: `offense.rape[297]`(component ref)
- `relation.occasion_identity`(337·338 경유 재사용)

CompletionPolicy는 **active HOLD**(§4 C-339 참고).

---

## 3. 이상 징후 감사 결과

### 3-1. 같은 id가 두 번 "신규" 선언된 사례
**0건.**

### 3-2. 통합 과정에서 새로 포착·확정한 ID 문제 3건

1. **`legal_element.injury_result`** — canonical id **확정**(배치⑨ 원 워크시트의
   `injury_occurred` 표기는 이력 보존을 위해 고치지 않되, 마스터·2-pass는
   `injury_result`를 쓴다).
2. **`legal_element.taking_of_own_property_conduct`**(323, 개명 확정) — 329의
   `ground_fact.taking_conduct`와의 근접 충돌 해소.
3. **`ground_fact.violence_used`**(257) — 이름 확정을 미루고 명시적 HOLD로 승격
   (§4 B-8), 인벤토리에 방치하지 않는다.

### 3-3. 이번 게이트에서 새로 재분류·폐기한 predicate 3건 (§6 참고)
`doctrine.quasi_robbery`(335, 최종본 미채택 상태를 마스터가 놓쳤던 것 정정),
`doctrine.complete_suppression_becomes_robbery`(350, cross-offense 전환 서술 금지
원칙 소급 적용), `legal_element.property_of_another`(360, A-3 확정으로 폐기).

### 3-4. canonical_meaning drift로 확정된 위반 사례
**0건** (재정의 시도는 있었으나 전부 같은 라운드 안에서 철회됨).

### 3-5. v0에서 있었다가 최종본에서 삭제된 predicate
80개 조문 전체 삭제 목록은 §6 부록.

---

## 4. 통합 HOLD / 2-pass 확인 목록

### §4-0. Gate① Blocker — 결정 완료(RESOLVED)

**258의2(특수상해)의 QUALIFY 대상 4갈래 중 258(중상해·존속중상해) 연동 2갈래는
이번 게이트에서 명시적으로 descope한다.** `data/rulebase/article_catalog.json`
확인 결과 258(단독)은 애초에 KCL 51개 population 목표에 포함된 적이 없다(258의2만
`art2582_2`로 포함). 258의2는 **257 연동 2갈래(상해·존속상해 가중)만으로 이번
게이트를 통과**하고, 258 갈래는 258 자체가 향후 population 대상에 추가된 뒤 QUALIFY를
확장하는 후속 작업으로 명시적으로 이월한다(해소 설계는 하지 않음, "지금 범위에서
뺀다"는 결정만 확정). 2-pass 착수 시 258의2의 `data/v2/definitions/` 조립은 이
descope를 그대로 반영해야 한다.

### (A) predicate/relation 재사용 확인 — 확정

| # | 항목 | canonical_meaning 대조 | 판정 |
|---|---|---|---|
| A-1 | 331 `dangerous_weapon_carriage`(흉기) ↔ 258의2 `dangerous_object_carriage`(위험한 물건) | "흉기"는 판례상 "위험한 물건"의 부분집합(위험한 물건이 더 넓은 개념) | **확정: 별도 유지**(재사용 안 함) |
| A-2 | 335 `occasion_identity`("절도의 기회") ↔ 337·338 `occasion_identity`("강도의 기회") | 둘 다 "본범 실행행위와 시간적·장소적 근접성"이라는 동일한 심사기준 | **확정: 재사용**, canonical_meaning을 "본범(base offense) 실행행위와 시간적·장소적으로 근접한 기회"로 일반화 |
| A-3 | 360 `property_of_another` ↔ 366 `object_ownership_other` | 둘 다 민법상 소유권 귀속(무주물 제외) 판단 | **확정: canonical id = `legal_element.object_ownership_other`**(366, 선행 정의). `property_of_another`는 폐기(§6) |
| A-4 | `embezzlement_manifestation`을 355(원 출처)·356·360이 공유 | "불법영득의사의 객관적 표현행위"로 동일 | **확정: 재사용**, 355 정의 그대로 356·360 재사용 |

**A그룹 전체 확정 완료 — 2-pass 착수 전 predicate/relation 재사용 HOLD는 0건.**

### (B) 순수 구조 선택 — 2-pass 저작 시점 결정 대상 (predicate 사전 문제 아님)

1. **301/337/338 결합범(고의)+결과적가중범(과실) 병존** — 별도 `DerivedOffenseDef`
   2개 vs 단일 definition 내부 두 갈래.
2. **299 예비·음모(305조의3)의 conduct 갈래 제한** — 후보 (A) 준강간/준강제추행
   별도 OffenseDef 분리, (B) 예비 단계 predicate에 목적 대상 명시.
3. **art319 계절적 미사용 별장의 "주거→건조물" subtype 재분류.**
4. **art319 퇴거불응(2항) attempted state 성립 여부**(322조 학설대립).
5. `bundle.mistake_bundle`(15조)이 `ElementBundleDef`로 실제 표현 가능한지 —
   실패 시 (C)로 승격.
6. `legal_element.disposer_identity_match`/`disposition_authority`(347·350
   처분권한)의 `RelationDef` 표현 가능성.
7. 마이너 cross-check(블로킹 아님): `voluntary_surrender_before_execution`(28)과
   31조 연결 여부 / `art137_sec6.non_suspect_impersonation_exception`(137)과
   151조 사실관계 중복 여부 / `avoidability`(negligence_bundle)와 `result_
   causation`의 경계 정리.
8. **`ground_fact.violence_used`(257) 명칭 확정** — 이름이 실제 판례상 범위(유형력
   외 방법 포함)보다 좁아 보이는 문제, 배치⑨ 저자도 두 라운드 모두 미결정. 2-pass
   저작 시 개명 여부(예: `injury_conduct`) 확정.
9. **21·22·23조 "과잉" doctrine(`excessive_defense`/`excessive_necessity`/
   `excessive_self_help`)의 stage(Culpability vs Punishability) 및 concrete
   MODIFY/EXEMPT effect 배정** — 배치③ v1이 명시적으로 "셋을 2-pass에서 동시
   결정"으로 남긴 항목(원문 확인 완료, 마스터가 임의로 만든 gap 아님).

### (C) architecture-compatibility — 코드 확인 필요, predicate 사전으로 못 닫음

| # | axis | concrete 사례 | 문제 성격 |
|---|---|---|---|
| C-33a | 33조 **본문**/신분범 공동정범 | art323(소유자 아닌 자 가담) | co-principal ATTRIBUTE에서 actor-specific 신분 status를 다른 actor에게 전이하면 안 됨 |
| C-33b | 33조 **단서**/책임 개별화 | art250(비신분자 존속살해 가담) | principal offense A ≠ accessory offense B |
| C-34 | 34조 간접정범 | art257(자상 강요·기망), art298(피해자를 도구로) | `principal_realization_truth`가 "정범 성공" 조건, 간접정범은 "피이용자 불처벌"이 조건 — 방향이 반대 |
| C-151 | 151조 `offender_status_of_object` | (151 자체) | cross-actor symbolic dependency |
| C-263 | 263조 동시범 특례 ↔ 19조 | (263 자체) | 법률상 의제 ≠ 6C `apply_attribution`(실제 공동가공 의사 전제) |
| C-339 | art339 CompletionPolicy | (339 자신) | D-1: component별 `commencement_of_execution` 구별 불가 / D-2: component별 slot suspension 불가 — 339 자신의 2-pass assembly 확정 전에만 해소 |

**35-36조는 이 목록에서 제외한다** — art35는 기존 Punishability MODIFY effect로
표현 가능함이 이미 확정됐고, art36은 절차법 조문으로 scope-out이 확정됐다.

### Non-blocking watch

- **art339의 COMPOSE(offense, offense) element-leaf 재사용 충돌 메커니즘** —
  코드로 실재 확인됐으나(`compile.py`의 `_compile_compose`) 339의 확정 predicate
  세트에서는 미발동. 향후 같은 COMPOSE(offense, offense) 패턴 재사용 시 슬롯별
  id 겹침을 매번 확인할 것.

---

## 5. 게이트 판정 요청

이 v1이 승인되면:
1. `docs/handoff/CURRENT.md`에 게이트 통과 기록 + 2-pass(`data/v2/definitions/`
   실제 조립) 시작점을 남긴다.
2. §4-0 Gate① Blocker(258 descope) 결정과 §4 (A)그룹 4건 전부 확정된 상태로
   2-pass에 들어간다.
3. §3-2의 ID 확정 3건(`injury_result`/`taking_of_own_property_conduct`/`violence_
   used`의 HOLD 승격)과 §3-3의 재분류 3건(`quasi_robbery`/`complete_suppression_
   becomes_robbery`/`property_of_another`)을 그대로 반영한다(기존 워크시트 파일
   자체는 이력 보존을 위해 고치지 않는다).
4. (B) 구조 선택 9건 + (C) architecture-compatibility 6건은 목록만 확정하고,
   해소는 2-pass 저작 시점(C는 코드 조사 포함)으로 넘긴다.

---

## 6. 부록 — 삭제·재분류된 predicate 전체 목록

### 6-1. 이번 게이트(v0→v1)에서 새로 재분류·폐기한 predicate

| id | 원 소속 | 재분류 사유 |
|---|---|---|
| `doctrine.quasi_robbery` | 335(pilot v1 HOLD) | 배치⑫ 최종본이 이미 `DerivedOffenseDef`(`purpose_to_resist_recapture`/`purpose_to_avoid_arrest`/`purpose_to_conceal_evidence`)로 완전히 대체했는데 마스터 v0가 pilot 시점 정보로 액티브 표에 남겨뒀던 것을 정정 |
| `doctrine.complete_suppression_becomes_robbery` | 350(pilot) | "공갈 불성립→강도로 평가"라는 cross-offense 전환 서술 — 배치⑦ 이후 확립된 "다른 죄로 전환을 doctrine으로 만들지 않는다" 원칙을 소급 적용, authoring/routing 메모로 강등(별도 predicate 불필요, 333·350 Elements 평가 자체가 이미 이 구분을 만듦) |
| `legal_element.property_of_another` | 360(배치⑫) | A-3 확정(canonical id는 366의 `object_ownership_other`)에 따라 폐기, 360은 그 id를 직접 재사용 |

### 6-2. 기존 배치가 v0 이후 삭제·폐기한 predicate (원 삭제 이력 그대로)

<details>
<summary>펼치기 — 80개 조문에서 v0 이후 삭제·폐기된 predicate 전체(삭제 이유 포함)</summary>

**총칙**
- `ground_fact.criminal_realization_intent`(25조) — 미완성 상태를 predicate로
  역수입하지 않고 각 offense 고유 고의·목적 요소 재사용으로 방향 전환
- `ground_fact.result_not_occurred`(25조) — 개념이 너무 넓어 각 죄의
  `CompletionPolicy.states.*.when`이 직접 미완성 조건을 표현하도록 변경
- `doctrine.actio_libera_in_causa_exception`(10조) — "exception의 exception"
  패턴 대신 `self_induced_disorder`+`NOT()` gating으로 흡수(12조 패턴 소급)
- `legal_element.coercion_not_self_induced`(12조) — 부정형 predicate 이름
  금지 원칙 위반, 긍정형+`NOT()`으로 대체
- `legal_element.consent_not_against_social_norms`(24조) — 추정적 승낙에
  안 맞는 표현이라 일반화·개명
- `legal_element.agent_unpunished_or_negligent`(34조) — symbolic runtime이
  이미 계산 가능한 법적 결론을 LegalElement로 잘못 승격
- `doctrine.right_exercise_defense`(재산죄 pilot) — 강도(구성요건 부정)와
  공갈(위법성조각)을 하나의 DoctrineDef로 합칠 수 없어 조문별 구조로 대체
- `ground_fact.disposer_identity_match`(재산죄 pilot) — `disposition_authority`
  후보로 대체 제시됐으나 끝내 미확정(§4 B-6)
- `PREPARATION`/`CONSPIRACY`(28조 2-state 분리안) — exact-one 규칙 위반,
  단일 `PREPARATION_OR_CONSPIRACY`로 병합
- `doctrine.concurrent_causation_default_attempt`(19조) — 별도 doctrine이
  아니라 기존 CompletionPolicy state로 표현 가능함이 확인됨

**각칙**
- `doctrine.third_party_recharacterized_as_direct_bribery`(130) — cross-offense
  경계는 doctrine 아님
- `doctrine.illegal_duty_act_reduces_to_general_offense`(136) — 동일 이유
- `doctrine.self_benefit_intermediary_excludes_delivery_offense`(133) —
  Elements negative 조건 → 긍정형 legal_element로 재분류
- `doctrine.self_concealment_not_an_offense`(151) — 구성요건 해당성 없음은
  애초에 doctrine 자격 없음
- `doctrine.interofficial_transmission_not_disclosure`(127) — negative 조건
  → `disclosure_conduct`에 흡수
- `doctrine.mohae_requires_criminal_or_disciplinary_case`(152) — QUALIFY의
  자연스러운 결과, 별도 doctrine 불필요
- `doctrine.concrete_risk_required_for_subject`(122) — Elements 흠결로 재분류
- `doctrine.nonofficial_cannot_be_indirect_perpetrator_of_status_offense`(227)
  — 진정신분범 요건 자체가 이미 커버
- `ground_fact.seal_or_signature_object`(239) — legal_element로 재분류
- `ground_fact.coercive_conduct`/`indecent_act_conduct`(297·298) — 구성요건
  평가 포함 → legal_element로 재분류
- `ground_fact.injury_occurred`(301) — 배치⑨ 재분류를 뒤늦게 반영(→`injury_result`)
- 301 "attempted state 자체를 두지 않는다"(v0 설계) — 미수불처벌은 `punishable=
  false`로 표현하는 133① 원칙 재적용
- `legal_element.no_justifiable_reason_for_refusal`(319) — 부정형 → 긍정형+NOT
- `doctrine.close_kin_property_offense_exemption`(328) — 2025.12.31. 개선입법
  시행으로 구조 자체 소멸
- `ground_fact.disabled_victim_abuse_property_crime_status`/`legal_element.
  kinship_status_within_statutory_range`(328) — 위 doctrine 삭제에 연동
- `legal_element.nighttime`(330, 시점-비종속형) — `nighttime_entry`(시점-내장형)로 교체
- 337/338 v1의 구체 완성 공식(variant별) — 301 HOLD 선결 오류, 고의 없는
  강도치사 봉쇄 버그
- 335 Elements의 `taking_conduct` 직접 요구(v1) — 절도미수+폭행 사건 봉쇄 오류
- 335/337/338의 `causal_nexus`/`occasion_identity`를 `elements.requires`에
  포함 — Elements/Relation 층위 혼동 재발
- 343 목적요건 `legal_element.intent` 사용 — 13조 고의를 목적으로 조용히
  재정의, `purpose_to_commit_target_offense`로 대체
- `356.base_offense=ANY(횡령,배임)` 단일구조 — 서로 다른 죄종 identity를
  하나로 뭉갬, QUALIFY 2개로 분리

</details>
