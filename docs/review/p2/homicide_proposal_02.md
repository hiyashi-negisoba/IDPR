# 살인 RuleIR 제안 02 — 살인의 고의 (Ⅰ.15, 37장)

track 어휘는 제안 01을 따른다. 이 절은 242장 중 가장 큰 덩어리이고, 실제 시험문제가
가장 많이 묻는 부분이다.

## 구조 제안 — 상해의 `injury_concept` / `injury_indicia` 분리를 그대로 쓴다

37장은 성격이 넷으로 갈린다.

- **고의의 정의와 판단 방법** (#45·#56·#57): 요건 자체를 진술한다 → `murder_intent`
- **고의를 인정한 판례 사례** 20장: 어느 하나면 충분한 인정 경로 → `murder_intent_indicia`
- **고의를 부정한 판례와 신중론** (#42·#68·#71): 인정을 막는다 → `bar` 또는 `boundary`
- **착오론** (#40·#41·#55·#61): 고의 조각 주장을 차단하거나 한정한다 → `bar` / component

정의와 인정 경로를 한 component에 섞으면 join이 충돌한다. 상해에서 이미 겪었다.

## 초안 — 고의의 정의 (3장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 45 | approve | component | murder_intent / alternative_any | base | 미필적 고의로 충분하다는 인정 경로 |
| 56 | approve | component | murder_intent / alternative_any | base | 객체 인식과 사망 결과의 인식·인용. 인과관계 인식 포함 |
| 57 | approve | component | murder_intent / alternative_any | base | 경위·동기·흉기·공격 부위·반복성 등 객관적 사정의 종합 판단 |

## 초안 — 고의를 인정한 사례 (20장, 전부 `murder_intent_indicia` / `alternative_any` / base)

| # | decision | 이유 |
|---:|---|---|
| 37 | rewrite | 메타 래퍼 제거. 브래지어로 강간 피해자의 목을 조른 경우 |
| 38 | rewrite | 메타 래퍼 제거. 시속 50km 버스를 경찰기동대원을 향해 돌진·조준 |
| 43 | rewrite | 메타 래퍼 제거. 만 6세 여아의 목을 3~4분간 압박 |
| 44 | rewrite | 메타 래퍼 제거. 9세 여아를 스카프로 졸라 실신시키고 유기 |
| 46 | approve | 사경의 피해자를 병원에 옮기지 않고 방치 |
| 47 | rewrite | 메타 래퍼 제거. 쓰러진 뒤에도 각목으로 머리를 계속 강타 |
| 49 | rewrite | 메타 래퍼 제거. 인공호흡기 제거를 지시한 담당의사의 예견·인식 |
| 50 | rewrite | 메타 래퍼 제거. 개괄적 고의 — 매장행위로 사망해도 살인 책임 |
| 51 | approve | 쇠파이프·각목 난타와 낫에 의한 난자 |
| 52 | rewrite | 메타 래퍼 제거. 판단능력 없는 어린 자녀를 익사하게 함 |
| 53 | rewrite | 메타 래퍼 제거. 장전된 엽총을 안전장치 없이 사용 |
| 54 | rewrite | 메타 래퍼 제거. 무술교관이 급소인 울대를 가격 |
| 58 | approve | 과도로 목 부위를 강하게 자상 |
| 64 | rewrite | 메타 래퍼 제거. 베개로 3분간 압박하고 정지 후에도 계속 압박 |
| 65 | rewrite | 메타 래퍼 제거. 7세 아동에 대한 장시간 무차별 폭행 |
| 66 | rewrite | 메타 래퍼 제거. 말목과 돌로 머리를 반복 구타 |
| 67 | approve | 비치명적 부위라도 칼로 약 20회 자상하여 과다실혈 |
| 69 | rewrite | 메타 래퍼 제거. 설골이 부러질 정도로 목을 15~20초 압박 |
| 72 | approve | 과도로 목 부위를 찌른 살인미수에서의 흉기 소지 경위 |
| 73 | rewrite | 메타 래퍼 제거. 7kg·153cm 목재로 머리를 강타 |

메타 래퍼 14장이다. `~대법원 판단이 소개되어 있다`를 걷어내고 사실관계와 법리결론만
남긴 완결 문장으로 언래핑한다. 문언은 승인 후 원장에 확정한다.

## 초안 — 고의를 부정하는 규칙 (3장)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 42 | approve | bar | murder_intent / not_applicable | base | - | 결과의 중대성과 비난가능성만으로 고의를 인정할 수 없다 |
| 68 | rewrite | boundary | murder_intent / not_applicable | base | intentional_bodily_injury | 메타 래퍼 제거. 복부 1회 타격·추락 사망은 상해치사로 경계 이동 |
| 71 | rewrite | bar | murder_intent / not_applicable | base | - | 메타 래퍼 제거. 저속 차량 진행과 비조준 가격은 살해 결의 부정 |

#42를 `context_only`가 아니라 `bar`로 두는 이유를 적어 둔다. 상해에서 "조각의 한계" 7장을
`context_only`로 버렸는데, 이 카드는 성격이 다르다. **한계가 아니라 그 자체로 고의 인정을
막는 규칙**이고, "결과의 중대성만을 근거로 고의를 인정하려는 경우인가"라는 평가가 충족되면
성립을 저지한다. 시험문제가 반복해서 묻는 법리이기도 하다.

## 초안 — 착오론 (4장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 40 | approve | bar | causal_course_error / not_applicable | base | 인식한 인과과정과 실제 사이에 본질적 차이가 있으면 고의에 영향 |
| 41 | approve | component | causal_course_error / mandatory_all | base | 차이가 본질적이지 않으면 고의에 영향이 없어 기수 |
| 55 | rewrite | bar | intent_error / not_applicable | base | 메타 래퍼 제거. 방법의 착오는 살인의 범의 성립을 방해하지 않음 |
| 61 | approve | bar | intent_error / not_applicable | base | 구체적 사실의 착오 중 객체의 착오는 고의 성립에 영향이 없음 |

#40과 #41은 같은 규칙의 양면이다. #41을 요건으로, #40을 차단으로 두면 "본질적 차이가
없을 것"이 요건이 되고 "본질적 차이가 있으면" 저지된다 — 중복이지만 두 카드의 provenance를
모두 살린다.

## 초안 — 다른 track으로 보내는 카드 (7장)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 59 | approve | boundary | murder_intent / not_applicable | base | intentional_bodily_injury | 살인 고의가 없으면 과실치사·상해치사·폭행치사 |
| 60 | rewrite | bar | ancestral_intent / not_applicable | parricide | - | 메타 래퍼 제거. 무차별 난동 중 부를 1회 자상한 경우 존속살해 의율 불가 |
| 62 | approve | component | omission_intent / mandatory_all | omission | - | 부진정부작위범 고의의 추인 방법 |
| 63 | approve | component | omission_intent / mandatory_all | omission | - | 결과발생을 용인·방관하면서 의무를 이행하지 않는다는 인식 |
| 39 | rewrite | component | omission_intent / alternative_any | omission | - | 메타 래퍼 제거. 선장이 퇴선 요청을 묵살하고 먼저 퇴선한 경우 |
| 48 | approve | post_outcome | participation_form / not_applicable | complicity | - | 치료중단 의사들은 고의는 인정되나 방조범의 죄책만 진다 |
| 70 | rewrite | bar | shared_intent / not_applicable | complicity | - | 메타 래퍼 제거. 예기치 못한 공동피고인의 살인은 나머지에게 귀속되지 않음 |

## Human decision H-H02

1. 위 37장 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. `murder_intent`(정의·판단방법)와 `murder_intent_indicia`(인정 사례 20장)를 분리하는가?
3. #42(고의 인정 신중론)를 `context_only`가 아니라 `bar`로 두는 데 동의하는가?
   상해의 "조각의 한계" 처리와 다르게 가는 것이므로 명시적으로 묻는다.
4. #40·#41을 같은 규칙의 양면으로 보아 bar와 component로 함께 두는 데 동의하는가?
