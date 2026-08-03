# 살인 RuleIR 제안 03 — 인과관계와 미수 (Ⅰ.14, Ⅰ.11~Ⅰ.13, 제254조)

track 어휘는 제안 01을 따르되, 미수 부분에서 **제안 01의 `attempt` 하나로는 부족하다는
것이 드러났다.** 아래에서 track 2개 추가를 제안한다.

## 제안 01의 `attempt` track 수정 제안

중지미수(제26조)와 불능미수(제27조)는 미수의 **하위 유형**이지 별개의 미수가 아니다.
자의성 카드를 `attempt`의 필수 component로 두면 **장애미수 사건이 성립하지 않는다.**

어제 상해에서 넣은 track 상속이 여기에 그대로 맞는다.

| track | 의미 | 상속 |
|---|---|---|
| `attempt` | 실행 착수 + 기수 미달 + 미수범 처벌규정 | - |
| `voluntary_desistance` | 제26조 중지미수 — 자의성이 더해진다 | `attempt` |
| `impossible_attempt` | 제27조 불능미수 — 수단·대상 착오와 위험성이 더해진다 | `attempt` |

`voluntary_desistance_established`는 `attempt_elements_satisfied`를 그대로 요구하고
자의성만 더한다. 존속살해가 보통살인을 상속하는 것과 같은 구조다.

## 초안 — 인과관계 (Ⅰ.14, 9장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 29 | approve | component | causation / mandatory_all | base | 실행행위로 사망이 발생하고 인과관계가 있을 것. 없으면 미수 |
| 28 | approve | component | causation_attribution / alternative_any | base | 예상과 실제의 차이가 일반 생활경험상 예견 범위 내인 경우 |
| 30 | approve | component | causation_attribution / alternative_any | base | 개재 사실이 통상 예견 가능하면 인과관계 인정 |
| 31 | approve | component | causation_attribution / alternative_any | base | 폭행이 유력한 원인이면 의사의 과실이 공동원인이어도 인과관계 인정 |
| 36 | approve | component | causation_attribution / alternative_any | base | 피해자 과실이 개재해도 통상 예견 가능하면 인과관계 인정 |
| 35 | approve | bar | causation / not_applicable | base | 사망까지 수일·수개월이 걸렸다는 사정만으로는 인과관계를 부정할 수 없음 |
| 32 | approve | component | omission_causation / mandatory_all | omission | 작위를 하였다면 결과가 없었을 관계. #10과 같은 요건의 provenance |
| 34 | approve | component | guarantor_status / alternative_any | omission | 조난 시 선장의 작위의무. #8과 같은 규칙의 provenance |
| 33 | approve | component | aiding_causation / mandatory_all | complicity | 회복 가능성이 전혀 없지 않았다면 방조와 사망 사이 인과관계 인정 |

`causation`(필수 요건)과 `causation_attribution`(귀속 인정 경로)을 나눴다. 상해의
`result_causation`에서 필수와 택일이 섞여 조립이 막힌 것과 같은 구조를 피한다.

## 초안 — 실행 착수와 기수 (Ⅰ.11, 4장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 13 | approve | component | attempt_commencement / mandatory_all | attempt | 살의를 가지고 생명을 위태롭게 하는 행위를 직접 개시한 때 |
| 15 | rewrite | component | attempt_commencement / alternative_any | attempt | 메타 래퍼 제거. 살인 고의로 흉기를 들고 접근한 경우 착수 인정 |
| 230 | approve | component | attempt_commencement / alternative_any | attempt | 결정 C 선택. 간접정범은 이용행위 개시 시 착수 |
| 14 | approve | component | death_result / mandatory_all | base | 결과범·침해범. 피해자가 사망하면 기수 |

## 초안 — 불능미수 (Ⅰ.12, 5장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 17 | approve | component | impossibility_danger / mandatory_all | impossible_attempt | 결과 발생이 불가능해도 위험성이 있으면 불능미수 |
| 18 | approve | component | impossibility_danger / mandatory_all | impossible_attempt | 위험성은 행위 당시 인식 사정을 바탕으로 일반인 기준으로 판단 |
| 16 | rewrite | component | impossibility_danger / alternative_any | impossible_attempt | 메타 래퍼 제거. 초우뿌리·부자 달인 물을 마시게 한 경우 |
| 19 | approve | bar | impossibility_danger / not_applicable | impossible_attempt | 위험성이 없으면 살의가 있어도 불능범으로 불벌 |
| 20 | context_only | context_only | - | - | 치사량을 더 심리해야 한다는 심리 지침이며 사실심리 영역 |

## 초안 — 중지미수 (Ⅰ.13, 7장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 26 | approve | component | voluntary_desistance / mandatory_all | voluntary_desistance | 자의로 중지하거나 결과 발생을 자의로 방지한 경우 |
| 27 | approve | component | voluntary_desistance / mandatory_all | voluntary_desistance | 중지가 사회통념상 범죄 완수의 장애 사정에 의한 것이 아닐 것 |
| 21 | approve | bar | voluntary_desistance / not_applicable | voluntary_desistance | 다량의 출혈에 놀란 것은 장애 사정 |
| 22 | approve | bar | voluntary_desistance / not_applicable | voluntary_desistance | 출혈에 놀라 신고·후송 후 체포가 두려워 도주한 경우 |
| 23 | approve | bar | voluntary_desistance / not_applicable | voluntary_desistance | 불길·신체 위해·처벌에 대한 두려움은 장애 사정 |
| 24 | approve | bar | voluntary_desistance / not_applicable | voluntary_desistance | 기절에 놀라 끈을 푼 뒤 도주하는 피해자를 쫓아간 경우 |
| 25 | approve | bar | voluntary_desistance / not_applicable | voluntary_desistance | 피해자의 임기응변과 과다출혈에 대한 두려움이 이유인 경우 |

자의성 부정 판례 5장이 전부 `bar`다. 중지미수 track만 저지하고 `attempt` 자체는 그대로
성립한다 — 자의성이 부정되면 장애미수로 남는다는 법리가 track 구조로 그대로 표현된다.

## 초안 — 제254조 (3장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 211 | approve | component | attempt_punishability / mandatory_all | attempt | 제250조·제252조·제253조의 미수범 처벌 |
| 210 | context_only | context_only | - | - | 미수범 형의 임의적 감경은 양형 사항 |
| 212 | context_only | context_only | - | - | 전자장치 부착명령은 특별법 영역이며 성립 결론과 무관 |

## Human decision H-H03

1. 위 28장 초안을 일괄 승인하는가?
2. **제안 01의 `attempt` 하나를 `attempt` / `voluntary_desistance` / `impossible_attempt`
   세 track으로 나누고 뒤 둘이 `attempt`를 상속하게 하는 데 동의하는가?** 이 문서의 핵심 질문이다.
3. `causation`(필수)과 `causation_attribution`(귀속 인정 경로)을 분리하는가?
4. #35(시간 간격 무관)를 `bar`로 두는 데 동의하는가? 인과관계를 시간 경과만으로 부정하려는
   주장을 차단하는 규칙으로 읽었다.
