# 상해 RuleIR 제안 01 — 상해 개념과 객체 (1–28번)

대상 source packet: `docs/review/p2/intentional_bodily_injury_cards_01.md`, `_02.md`

패킷의 proposition과 bounded quote만 직접 대조한 초안이다. 주석 전체나 판례 원문을 전수
검토했다는 뜻이 아니며, human approval 전에는 RuleIR에 반영하지 않는다.

## track 어휘 제안

이 unit은 제257조·제258조의2·제259조·제263조를 한 죄명 아래 묶는다(D4 승인). 방화보다
단계가 많아 track을 여섯 개로 나눈다.

| track | 의미 |
|---|---|
| `base` | 제257조 제1항 상해 기본 구성요건 |
| `attempt` | 제257조 제3항 미수 |
| `ancestral` | 제257조 제2항 존속상해 가중 |
| `special` | 제258조의2 특수상해 가중 |
| `aggravated_result` | 제259조 상해치사 |
| `concurrent_offenders` | 제263조 동시범 특례 |

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 1 | rewrite | bar | injury_concept / not_applicable | base | - | 메타 래퍼 제거. 음모 외관 변형만으로는 상해 아님. #14와 같은 규칙의 사례 |
| 2 | context_only | context_only | - | - | - | 상해진단서 증명력은 증거법이며 구성요건이 아님 |
| 3 | approve | component | injury_indicia / alternative_any | base | - | 약물 투약으로 건강상태 불량 변경·생활기능 장애 |
| 4 | approve | component | injury_indicia / alternative_any | base | - | 외관 상처 없어도 기능장해로 상해 인정 |
| 5 | approve | bar | injury_concept / not_applicable | base | - | 두발·손톱 등 절단은 상해가 아님 |
| 6 | rewrite | bar | injury_concept / not_applicable | base | - | 메타 래퍼 제거. 통증·자각증상 없는 반상출혈은 상해 아님 |
| 7 | approve | component | injury_indicia / alternative_any | base | - | 일상·합의성교에서 통상 생길 정도를 넘는 상처 |
| 8 | approve | component | injury_conduct / alternative_any | base | - | 수단 무제한. 무형적 방법에 의한 상해 경로 |
| 9 | rewrite | bar | injury_concept / not_applicable | base | - | 메타 래퍼 제거. 치료 불요·2~3일 자연치유 찰과상은 상해 아님 |
| 10 | approve | bar | injury_concept / not_applicable | base | - | 극히 경미하여 자연치유되고 일상생활 지장 없으면 상해 아님. 이 군의 핵심 규칙 |
| 11 | rewrite | bar | injury_concept / not_applicable | base | - | 메타 래퍼 제거. 당일 통증 소멸한 2cm 긁힌 상처는 상해 아님 |
| 12 | approve | component | injury_conduct / alternative_any | base | - | 부작위에 의한 상해 경로 |
| 13 | approve | component | injury_concept / mandatory_all | base | - | 생리적 기능 훼손설. 건강상태 불량 변경과 생활기능 장애라는 상해 정의 |
| 14 | approve | bar | injury_concept / not_applicable | base | - | 외관 변형만으로는 병리적 악화나 기능장애가 없어 상해 아님 |
| 15 | rewrite | component | injury_indicia / alternative_any | base | - | 메타 래퍼 제거. 보행불능·수면장해·식욕감퇴 |
| 16 | rewrite | component | injury_indicia / alternative_any | base | - | 메타 래퍼 제거. 1개월 이상 정신과 치료를 요하는 급성 스트레스 반응·우울장애 |
| 17 | rewrite | component | injury_indicia / alternative_any | base | - | 메타 래퍼 제거. 성병 감염 |
| 18 | context_only | context_only | - | - | - | 상해진단서 증명력 판단 기준이며 증거법 영역 |
| 19 | rewrite | component | injury_indicia / alternative_any | base | - | 메타 래퍼 제거. 졸피뎀 투약에 의한 의식상실 |
| 20 | approve | component | offense_definition / mandatory_all | base | - | 고의로 사람의 신체를 상해하는 기본 구성요건 |
| 21 | approve | bar | object_scope / not_applicable | base | - | 동물은 객체가 아님 |
| 22 | rewrite | component | injury_conduct / alternative_any | base | - | 메타 래퍼 제거. 의사결정 자유를 상실시킬 협박으로 자상케 한 경우 |
| 23 | approve | bar | object_scope / not_applicable | base | - | 법인은 객체가 아님 |
| 24 | approve | bar | object_scope / not_applicable | base | - | 사체는 객체가 아님 |
| 25 | approve | bar | object_scope / not_applicable | base | - | 태아는 객체가 아님 |
| 26 | approve | component | injury_conduct / alternative_any | base | - | 강요·기망을 이용한 간접정범 경로 |
| 27 | approve | component | object_scope / mandatory_all | base | - | 객체는 자연인인 타인의 신체 |
| 28 | approve | bar | object_scope / not_applicable | base | - | 자상은 원칙적으로 죄가 되지 않음 |

## 메타 래퍼 카드 8건

`~사례가 소개되어 있다`, `~판례 설명이 있다`는 주석의 소개 문언이지 실체법 규칙 문장이 아니다.
1·6·9·11·15·16·17·19·22번은 사실관계와 법리결론만 남긴 완결 문장으로 언래핑한 뒤 RuleIR에
넣는 것을 제안한다. 문언은 승인 후 원장에 확정한다.

## Human decision H-B01

1. 위 1–28번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. 여섯 개 track 어휘를 승인하는가?
3. 상해진단서 증명력 카드 2건(#2·#18)을 증거법으로 보아 `context_only`로 두는 데 동의하는가?
4. `injury_concept`(정의·배제)와 `injury_indicia`(인정 경로)를 분리하는 구조를 승인하는가?
   방화에서 하나의 component에 필수 요건과 택일 경로를 섞었다가 컴파일이 막힌 전례를 피한 것이다.
