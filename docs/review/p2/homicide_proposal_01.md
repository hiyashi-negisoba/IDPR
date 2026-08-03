# 살인 RuleIR 제안 01 — track 어휘와 객체·행위·부작위 (Ⅰ.1~Ⅰ.4, Ⅰ.10)

대상: `docs/review/p2/homicide_cards_01.md` 이하 17개 패킷, 총 242장.
이 문서는 track 어휘를 먼저 정하고 22장을 판정한다.

## 이 unit이 상해와 다른 점 — 242장 중 76장이 성립 밖이다

읽어 보니 살인 주석은 구성요건보다 **증명·양형·총칙**에 지면을 더 쓴다.

| 영역 | 절 | 장수 | 성격 |
|---|---|---:|---|
| 증거·사실인정 | Ⅰ.5~Ⅰ.9 | 16 | 간접증거, 과학적 증거, 시신 없는 살인, 부검 |
| 양형 | Ⅰ.21 | 25 | 사형 선택 기준, 재범위험성, 부정기형, 몰수 |
| 책임능력 | Ⅰ.18 | 11 | 심신장애, 원인에 있어서 자유로운 행위, 기대가능성 |
| 공범 | Ⅰ.19 | 24 | 공동정범·교사·방조·공모관계 이탈 |
| **합계** | | **76** | |

증거와 양형은 성립 결론을 바꾸지 않으므로 `context_only`로 제안한다. 책임능력과 공범은
성립에 영향을 주지만 **총칙(제10조, 제30~34조)이고 모든 죄명이 공유한다.** 상해에서
경과규정(제1조 제2항)을 총칙 영역으로 보아 제외한 것과 같은 이유로, 이 unit의 RuleIR에
넣지 않고 별도 문서(제안 04·05)에서 처리 방식을 묻는다.

## track 어휘 제안

| track | 의미 | 상속 |
|---|---|---|
| `base` | 제250조 제1항 보통살인 기본 구성요건 | - |
| `attempt` | 제254조 미수 — 착수·장애미수·중지미수·불능미수 | - |
| `parricide` | 제250조 제2항 존속살해 가중 | `base` |
| `preparation` | 제255조 예비·음모 | - |
| `complicity` | 총칙 공범. 역할 tuple이 달라 이번 회차 미컴파일 | - |

존속살해는 상해의 `ancestral`과 같은 구조다 — 보통살인 요건을 그대로 요구하고 직계존속
신분만 더한다. 어제 넣은 `inherits_from`이 그대로 쓰인다.

## 역할 tuple 제안

```text
homicide_case_roles(case_id, defendant_id, victim_id)
```

살인은 재산죄의 owner/possessor도, 방화의 structure/occupant도 쓰지 않는다. 피고인과
피해자 둘이면 충분하다. 공범 track만 `accomplice_id`가 더 필요하다.

## 초안 — 객체 (Ⅰ.3, 11장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 168 | rewrite | component | person_begins / alternative_any | base | 메타 래퍼 제거. 규칙적 진통을 동반한 분만개시 때가 사람의 시기 |
| 169 | rewrite | bar | person_begins / not_applicable | base | 메타 래퍼 제거. 규칙적 진통이 없는 제왕절개 단계의 태아는 사람이 아님 |
| 170 | approve | component | person_ends / mandatory_all | base | 사람의 종기는 의학적 판단만이 아니라 생명보호 입법취지를 종합 |
| 171 | approve | component | person_begins / mandatory_all | base | 분만개시 시점에 태아가 생명을 가지고 있을 것 |
| 172 | approve | component | object_scope / mandatory_all | base | 객체는 살아 있는 자연인. 생존능력 유무 불문 |
| 173 | approve | bar | object_scope / not_applicable | base | 출생 후 생명유지 능력을 요구하지 않는다는 차단규칙 |
| 174 | rewrite | component | person_begins / alternative_any | base | 메타 래퍼 제거. 낙태 후 살아서 출생한 미숙아도 살인죄의 객체 |
| 175 | approve | bar | object_scope / not_applicable | base | 자기 자신은 객체가 아니며 자살은 살인죄가 아님 |
| 234 | approve | component | person_begins / alternative_any | base | 결정 C가 선택한 진통설. #168과 같은 규칙의 학설 provenance |
| 235 | approve | component | person_ends / mandatory_all | base | 결정 C가 선택한 맥박종지설. 뇌사자는 아직 사람 |
| 236 | approve | bar | person_ends / not_applicable | base | 장기이식법만으로 종기를 뇌사로 볼 수 없다는 차단규칙 |

`person_begins`와 `person_ends`를 `object_scope`에서 분리했다. 시기·종기는 객체 해당성의
**시간적 경계**이고, 자연인·자살 배제는 **인적 경계**다. 한 component에 섞으면 상해에서
겪은 join 충돌이 그대로 재발한다.

## 초안 — 살해행위와 부작위 (Ⅰ.1, Ⅰ.2, Ⅰ.4, Ⅰ.10)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 5 | approve | component | offense_definition / mandatory_all | base | 고의로 사람을 살해하여 생명을 끊는 기본 구성요건 |
| 6 | context_only | context_only | - | - | 보통살인·존속살해의 구분 서술이며 track 어휘가 이미 담고 있음 |
| 176 | approve | component | killing_conduct / mandatory_all | base | 자연적 사기에 앞서 생명을 단절시키는 것이 살해 |
| 177 | approve | component | killing_conduct / alternative_any | base | 수단 무제한. 무형적 방법도 포함 |
| 125 | approve | component | guarantor_status / mandatory_all | base | 부작위 살인은 보증인적 지위를 요구하는 진정신분범 |
| 12 | approve | component | guarantor_status / mandatory_all | base | 생명을 보호할 보증인적 지위. #125와 같은 요건의 provenance |
| 11 | approve | component | omission_equivalence / mandatory_all | base | 부작위가 작위와 동등한 형법적 가치를 가질 것 |
| 8 | approve | component | guarantor_status / alternative_any | base | 조난 상황의 선장·선원에게 구호 작위의무가 있다는 발생근거 |
| 7 | rewrite | component | omission_equivalence / alternative_any | base | 메타 래퍼 제거. 선장의 퇴선조치 불이행은 작위 살인과 동일 평가 |
| 9 | approve | component | omission_equivalence / alternative_any | base | 감금 중 살의로 방치한 부작위도 구성요건적 행위 |
| 10 | approve | component | omission_causation / mandatory_all | base | 의무를 이행했다면 결과가 발생하지 않았을 관계 |

### #176과 #177이 같은 component에서 join이 갈리는 문제

#176은 살해의 정의(필수), #177은 수단 무제한(택일 경로)이다. 상해의 `intent`에서 같은
충돌을 겪었으므로 여기서는 미리 나눈다 — 위 표는 둘 다 `killing_conduct`에 두었으나
조립 단계에서 **#176 `mandatory_all`, #177은 `killing_method` component로 분리**한다.
아래 H-H01 제4문에서 확인을 구한다.

### 부작위 살인을 base track에 넣는 것의 문제

`guarantor_status`·`omission_equivalence`·`omission_causation`을 base의 필수 component로
두면 **모든 작위 살인 사건이 보증인적 지위를 주장해야 성립한다.** 이건 명백히 틀렸다.

부작위 살인은 base의 대안 실행형태이므로, 조립 시에는 `killing_conduct`를
`alternative_any`로 두고 그 안에 작위 경로(#177)와 부작위 경로를 나란히 두는 것이 맞다.
부작위 3요건은 그 경로 안에서만 필요한 조건이라 현재 어휘로는 표현이 안 된다.

대안 두 가지:
- **(A)** 부작위를 별도 track `omission`으로 분리하고 `base`를 상속시키지 않는다.
  깔끔하지만 base와 요건 대부분이 겹쳐 중복이 생긴다.
- **(B)** 부작위 3장을 `context_only`로 버린다. 손실이 크다. 세월호·아동학대 유형이 통째로 빠진다.

**(A)를 제안한다.** 위 표의 track은 승인 시 `omission`으로 바꾼다.

## Human decision H-H01

1. 다섯 개 track 어휘(`base`/`attempt`/`parricide`/`preparation`/`complicity`)를 승인하는가?
2. 증거 16장·양형 25장을 `context_only`로, 책임능력 11장·공범 24장을 총칙 영역으로 보아
   이 unit의 RuleIR에서 제외하는 데 동의하는가? (제외해도 카드는 폐기하지 않는다)
3. 사람의 시기·종기를 `object_scope`에서 분리하여 `person_begins`·`person_ends`로 두는가?
4. #176을 `killing_conduct`(필수), #177을 `killing_method`(택일)로 나누는가?
5. 부작위 살인을 별도 track `omission`으로 분리하는 (A)안을 승인하는가?
