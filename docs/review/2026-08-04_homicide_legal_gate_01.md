# 살인 RuleIR 일괄 법률검수 게이트 01

대상은 현재 카드 자산의 제250조·제254조·제255조 242장 전부다. 카드별 판정은 다음 7개
문서에 있으며, 고유 카드 242/242, 누락 0, 중복 0이다.

- `homicide_proposal_01.md`: 객체·행위·부작위 22장
- `homicide_proposal_02.md`: 살인의 고의 37장
- `homicide_proposal_03.md`: 인과관계·미수 28장
- `homicide_proposal_04.md`: 위법성·책임 29장
- `homicide_proposal_05.md`: 공범 24장
- `homicide_proposal_06.md`: 죄수·양형·증거 59장
- `homicide_proposal_07.md`: 존속살해·예비음모 43장

이 게이트는 앞 문서 사이의 시간차로 생긴 모순을 제거한 최종안이다. 승인 전에는 승인 원장,
RuleIR 또는 SCL에 편입하지 않는다.

## G-H01 — 카드별 판정

242장 표의 `decision / role / component / join / track / refers_to`를 일괄 승인하는가?
수정할 카드 번호만 제시해도 된다.

## G-H02 — track과 역할 tuple

다음 구조를 승인하는가?

| track | 처리 | 상속 |
|---|---|---|
| `base` | 컴파일 | - |
| `omission` | 컴파일. 작위 base에 보증인지위를 강제하지 않도록 별도 분리 | - |
| `attempt` | 컴파일 | - |
| `voluntary_desistance` | 컴파일 | `attempt` |
| `impossible_attempt` | 컴파일 | `attempt` |
| `parricide` | 컴파일 | `base` |
| `preparation` | 컴파일 | - |
| `complicity` | 선언하되 이번 회차 미컴파일. 공유 총칙 module 이관 | - |

- 일반 track 역할 tuple: `homicide_case_roles(case_id, defendant_id, victim_id)`
- 공범 역할 tuple: `homicide_complicity_case_roles(case_id, defendant_id, victim_id, accomplice_id)`

## G-H03 — 요건 분해와 차단

다음을 하나의 구조 묶음으로 승인하는가?

- 사람의 시기·종기: `person_begins` / `person_ends` / `object_scope` 분리
- 살해행위: `killing_conduct` / `killing_method` 분리
- 고의: `murder_intent` / `murder_intent_indicia` 분리
- 인과관계: `causation` / `causation_attribution` 분리
- 존속관계: `ancestral_relation` / `_basis` / `_timing` 분리
- #42 고의 인정 신중론, #35 시간 간격만의 인과관계 부정, #207 존속신분 불인식을 각각
  해당 track만 저지하는 `bar`로 처리

## G-H04 — 범위 밖과 보존 방식

다음을 승인하는가?

- 양형 24장, 증거 16장, 특정강력범죄법 2장: `context_only`
- 정당방위 한계 7장, 안락사 한계 2장, 책임능력 한계·심리 7장: `context_only`
- 책임능력 4장(#99·#97·#101·#92)은 base에 편입하되 `mental_incapacity` bar는
  **심신상실에만** 적용
- 공범 24장은 폐기하지 않고 별도 역할 tuple과 함께 `declared_not_compiled`
- 죄수·감면 등 `post_outcome`은 카드와 판정을 보존하되 outcome bridge 전까지 미컴파일
- 제252조 촉탁·승낙살인 등 현재 51조문 밖 참조는 가짜 결론 없이 `predicate_ir_missing`

## G-H05 — 결정 C #20 복원

예비·음모의 자발적 포기에 관한 #242는 기존 결정 C가 선택한 긍정설로 다음처럼 언래핑한다.

> 예비·음모 단계에서도 자발적으로 실행 착수를 포기한 경우 중지미수의 감면 혜택을 부여할
> 수 있다.

이는 예비·음모죄의 성립을 배제하는 `bar`가 아니라 감면을 기록하는 `post_outcome`으로 둔다.

## 응답 형식

전부 동의하면 `G-H01~H05 승인`으로 충분하다. 수정이 있으면 `G-H03: #42 context_only`처럼
게이트와 카드 번호만 적어도 된다.
