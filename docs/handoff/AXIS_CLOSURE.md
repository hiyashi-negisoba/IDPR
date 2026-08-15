# 축별 구조 감사 (axis closure)

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00

이 문서가 구조 감사의 정본이다. `NEXT_SESSION.md`는 append-only 역사 로그이며 그 안의
"다음 작업" 지시는 이 문서가 대체한다.

다음 세션의 시작점은 [`START_HERE.md`](START_HERE.md)이고, 다음 작업 지시서는
[`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md)다. 이 문서는 "지금까지 무엇이 닫혔는가"를 담는다.

## 왜 이 방식인가

26문항 E2E에서 결론 미확정이 82%였다. 지난 세션들은 답안 하나가 이상할 때마다 아래층을
열었고, 그때마다 새 진단 트랙이 생겨 원인은 늘어나는데 닫히지는 않았다.

그래서 작업 단위를 **답안이 아니라 축**으로 바꿨다. 축마다 룰베이스 구조를 전수로 훑어
구조적 결함만 고치고, 종료 테스트를 남기고 닫는다. 26문항 실행은 구조 결함 중 무엇이
실제로 물리는지 걸러내는 필터로만 쓴다.

## 종료 기준

**버그로 보고 고치는 것**

1. **발화 불가능성** — 어떤 진리값 배정으로도 참이 될 수 없는 상태·요소
2. **배타·우선관계 미정의** — 두 상태가 동시에 참일 수 있는데 양보 관계가 없어 영구 unresolved
3. **carrier 타입 불일치** — predicate가 요구하는 종류의 사실을 그 carrier가 구조적으로 담을 수 없음

**성능으로 남기는 것**

위 셋에 해당하지 않는 모든 오판. target·carrier·정의가 정상인데 모델이 UNKNOWN을 내거나
틀린 경우가 여기 속한다. 이걸로 다시 구조를 열지 않는다.

축마다 위 항목을 전수 검사하는 테스트를 남긴다. 그 테스트가 그 축의 종료 증명이다.

## 원칙: UNKNOWN은 부정이 아니다

세 축을 닫으면서 반복해서 나온 결함이 하나였다. **예외의 부존재를 원칙의 성립요건으로
요구하는 저작**이다. 자의적 중지, 수단·대상의 착오, 살인의 고의 — 이런 사실은 있었을 때만
사건에 서술되고 없었다고 적히지 않는다. Kleene `NOT`은 그것을 UNKNOWN으로 남기므로 원칙
쪽이 영구히 성립 불가능해진다.

그래서 도입한 네 가지는 모두 "확정되었을 때만 작동한다"는 의미를 갖는다.

| 장치 | 위치 | 의미 |
|---|---|---|
| `defeated_by_state` | completion policy | 형제 상태가 **확정**되면 양보 |
| `blocked_when` | completion policy · doctrine | 예외가 **확정**되면 그 상태·법리 배제 |
| `definitional_resolution` | concurrence rule | 밀어내는 죄가 **성립**하면 밀려남 |
| `same_realization` | concurrence rule | episode가 아니라 실현된 행위 단위로 결합 |

UNKNOWN을 FALSE로 바꾸는 장치는 하나도 없다. 다음 축에서도 이 선을 넘지 않는다.

## 닫은 축

### completion (2026-08-15)

| 결함 | 유형 |
|---|---|
| 장애미수가 중지미수의 부존재를 요구 (살인·존속살해·강간·준강간) | 2 |
| 준강간이 선언하지도 않은 `abandoned_attempt`의 부존재를 요구 | 1 |
| 예비와 기수가 동시 성립 가능한데 양보 미선언 (살인·강도) | 2 |
| 장애미수가 불능미수의 부존재를 요구 (10개 상태) | 2 |

종료 테스트: [`tests/test_completion_state_coverage.py`](../../tests/test_completion_state_coverage.py)
— 14개 policy × 모든 진리값 조합 전수. 결과: `attempted` 0 → 3 발화.

### evidence carrier (2026-08-15)

선언 가능한 `evidence_scope` 4종 중 `same_actor_episode`가 한 번도 공급되지 않았고,
`temporal_anchor`가 폭까지 좁혀 자기이득 목적이 UNKNOWN 100%였다. 타입 불일치 241건 → 0건.
`temporal_anchor`는 시점 cutoff로 재정의했다.

종료 테스트: [`tests/test_evidence_scope_carrier_contract.py`](../../tests/test_evidence_scope_carrier_contract.py)

### elements (2026-08-15)

negative intent gate 4곳(상해치사·강간치상·강도치상·강도치사)과 증뢰물전달죄의 주관적
구성요건 누락. 후자는 mental slot 전체가 `NOT(자기이득목적)`이었고, 이는 저작 형식만이 아니라
법적 구별기준 자체가 틀린 것이었다 — 증뢰 목적을 알면서 받았다면 자기가 가질 생각이었어도
성립한다. `knowledge_of_bribery_destination`으로 교체했다.

reachability 전수: 정의 누락 0 · 미질문 predicate 0 · carrier 누락 0.
live blocker 184건 중 구조 결함 0, 성능 174건.

종료 테스트: [`tests/test_definitional_resolution.py`](../../tests/test_definitional_resolution.py)

### participation (2026-08-15)

| 결함 | 유형 |
|---|---|
| 교사·방조가 요구하는 가담자 고의가 target으로 열리지 않음 (26문항 전체 0건) | 1 |
| 관계의 endpoint universe를 action 참여자로 좁혀 사주·승낙이 표현 불가능 | 3 |
| 두 행위의 병렬로만 서술되는 공동행동이 어느 action 스코프에도 담기지 않음 | 3 |
| 공동정범과 종범이 동시에 참일 때 양보 관계가 없어 사건 전체가 예외로 중단 | 2 |
| 가담자 후보 instance가 assessment universe 밖이라 자기 target을 받을 자리가 없음 | 1 |

**60 → 32 회귀 판정: 회수 후퇴다, 중복 제거가 아니다.** 원인은 상위 단계에 있었다.
interaction 추출이 action 단위로 내려가면서 factual_interaction이 37 → 26으로 줄었고,
잃은 것은 정확히 교사·승낙 쌍이었다. 26문항 215개 action 중 32개가 자기 인용문 안에 이름이
나오는 참여자를 `participant_ids`에서 빠뜨리고 있었고(15개 사건), 관계의 상대방은 그 행위의
참여자로 기록되지 않는 것이 원칙에 가깝다. 행위 원자화는 죄의 실현 단위를 자르기 위한
것이고 `factual_action_id`는 participation planner 어디에서도 읽히지 않는다 — action 스코프는
회수만 깎고 얻는 것이 없었다. 관계 추출을 episode 스코프로 되돌리고(`--interaction-scope`,
기본 `episode`), endpoint universe는 episode가, evidence 범위는 anchor가 있을 때만 action이
소유하도록 나눴다. action 스코프를 쓸 때는 관계가 그 행위의 행위자를 한쪽 끝으로 가져야 한다.

가장 큰 것은 첫 줄이다. `co_principal`은 `establishes_predicate_refs`로 관계가 사실을
*공급*받지만 derivative mode는 `requires`로 사실을 *요구*하는데, 그 predicate를 아무도 묻지
않았다. Kleene에서 묻지 않은 사실은 UNKNOWN이므로 **교사범·방조범은 어떤 사건에서도 성립할
수 없었다.** 26문항 plan에서 `instigator_intent`·`aiding_intent` target은 각각 0개였고,
`joint_commission_by_two_or_more`만 12개 열려 있었다. planner가 이제 derivative 후보마다
mode의 `requires`를 target으로 연다 (`opened_by: participation_mode_requirement`, 17개).

가담자 후보는 assessment universe에 들어오되 top_level에는 들어가지 않는다 (125 vs 108).
자기 고의를 스스로 답해야 하지만, 관계가 참으로 확정되기 전에는 책임 결론이 아니기 때문이다.
Scallop runner의 endpoint 승격은 이제 없는 instance를 만들어 내는 것이 아니라 이미 있는
instance를 top_level로 올리는 일이 된다.

공동정범과 종범의 우선관계는 저작에 추가했고 검수를 통과했다(`co_principal` ⊃ `instigator`,
`aider`). 저작 문구는 "정범성이 종범을 흡수한다"가 아니라 **동일 범죄 realization에 대한
participation-role resolution**이다 — 법조경합상 흡수로 이름 붙이지 않는 이유는 교사행위와
공동실행 사실이 함께 존재할 수 있고 교사범이 독자의 성립구조를 갖기 때문이다. 원 관계·증거·
provenance는 보존하고 최종 책임에서만 derivative mode를 내린다. 런타임은 저작된 양보만
적용하고, 선언이 없으면 종전대로 계약 위반으로 올린다.

종료 테스트: [`tests/test_participation_axis_contract.py`](../../tests/test_participation_axis_contract.py)
— 저작된 derivative mode의 `requires` 전수, 동시 성립 가능한 mode 쌍의 우선관계 전수,
사주·승낙 최소 사례의 endpoint·carrier 정합.

미측정: 위 수정은 Call 1.5-P 재실행(episode 스코프)과 Call 2 재실행(677 target)을 거쳐야
숫자로 나타난다. symbolic 단계는 기존 Call 2 산출물에 대해 변화 없음을 확인했다(비의미적
정렬 차이 1건 외 26/26 동일).

### doctrine (2026-08-15)

| 결함 | 유형 |
|---|---|
| 예외의 부존재를 성립요건으로 요구해 13개 중 5개가 발화 불가 | 1 |
| `statutory_bar_on_consent`의 뜻이 이름·사용처의 반대로 적혀 이중부정 | 1 |
| doctrine 단계 자체가 26문항 파이프라인에 없음 | 파이프라인 |

**발화 불가 5개**: 심신상실(원인에 있어서 자유로운 행위), 강요된행위(자초한 강제상태),
긴급피난(위난감수의무), 피해자승낙·추정적승낙(승낙배제 특별규정). 모두 예외가 있었을 때만
사건에 적히는 사실인데 `requires` 안에 `NOT(...)`으로 들어 있었다. completion 축에서 쓴
`blocked_when`을 DoctrineDef로 이식했다 — 예외가 **확정**될 때만 배제하고, UNKNOWN인 예외는
아무것도 막지 않는다. Scallop lowering, 활성화 게이트, leaf target opener 모두 통과시켰다.
결과: 발화 불가 5 → 0.

**이중부정**: `legal_element.statutory_bar_on_consent`는 이름이 "승낙배제 규정이 있다"인데
`canonical_meaning`이 "특례규정 없음", `legal_standard`가 "…특별법규가 **없는지** 여부"로
적혀 있었고 사용처는 `NOT(...)`이었다. 그대로 두면 승낙이 유효할 때 오히려 위법성조각이
부정된다. 이름·사용처에 맞춰 긍정형으로 되돌렸다. **법률 검수 필요.**

**파이프라인 공백**: 13개 doctrine이 25개 사건에서 후보로 열려 있는데 그 leaf는 한 번도
Call 2 target이 아니었고 `active_doctrines`는 26/26 전부 비어 있다. 규칙베이스 결함이 아니라
Call 1.5-D와 `build_v2_doctrine_target_plan.py`가 현재 체인에 없어서다. frozen root에서는
동작했다(cue 13개 production, leaf target 19개, 제기 3개). 재실행 때 체인에 넣는다.

**공백으로 남기는 것**: `UNRESOLVED_MISTAKE_BINDING` 25건과
`doctrine.mistaken_justifying_circumstance`의 비활성화는 둘 다
`gap.intended_object_identity`의 하류다. `factual_targets`를 intended_object로 재해석하는
우회는 2026-08-13 검수에서 명시적으로 거부되었고, `data/v2/representation_gaps.yaml`에
사유·미래 설계와 함께 기록되어 있다. 이 축에서 열지 않는다.

종료 테스트: [`tests/test_doctrine_axis_contract.py`](../../tests/test_doctrine_axis_contract.py)
— 13개 doctrine × "예외 미서술 시 발화 가능" 전수, blocker의 확정/UNKNOWN 구분, blocker
predicate의 긍정형 저작, 제기 경로 또는 공백 기록의 존재.

### concurrence (2026-08-15)

| 결함 | 유형 |
|---|---|
| 파생실현에 초점행위가 없어 `same_realization` 규칙이 후보조차 못 엶 | 1 |
| 정범에서 밀려난 죄가 가담자 쪽에 그대로 남음 | 최종 중복 |
| 흡수조건 단계가 26문항 파이프라인에 없음 | 파이프라인 |

**`same_realization` 발화 불가**: host가 두 개 이상의 source realization에서 조립한 파생죄
(`realization:derived:*`)에는 초점행위가 없다. 강도치상은 강도와 상해에 걸쳐 있어 어느 하나를
초점으로 고를 수 없기 때문이고 그 결정 자체는 옳다 — 증거 폭을 한 행위로 좁히면 안 되는
죄다. 그런데 `same_realization`을 초점행위 동일성으로만 보면 결과적 가중범(초점 없음)과
고의범(초점 있음)을 짝지으라고 저작된 규칙 3개가 후보를 하나도 열지 못한다. `r14_p2_q1`의
乙 강도치상 대 강도상해가 정확히 그 상태였다. 파생실현의 실현 식별자는 그 source들이 **한
초점행위에 모일 때** 그 행위로 읽도록 했다 — 원문 재해석이 아니라 host 자신의 조립 기록을
되읽는 것이고, source들이 어긋나면 식별자를 만들지 않는다. 그 사건에서 막혀 있던 짝이
`factual_action:001:007`로 이어졌다.

**가담자 쪽 잔류**: 가담자 후보는 정범 realization 하나마다 따로 만들어진다. 甲의 절도가
특수절도에 밀려도 乙의 절도방조는 남아 乙에게 절도방조와 특수절도방조가 함께 선다.
정범 단계의 결정을 그 정범을 향한 가담 관계로 옮기되, **대체가 실제로 존재할 때만** 옮긴다
(乙이 밀어낸 죄 쪽 정범에게도 같은 mode로 연결되어 있어야 한다). 대체 없이 밀어내면 책임을
지우는 일이 되고 그것은 경합이 하는 일이 아니다. **법률 검수 필요** — "가담자의 죄명은
정범의 죄명을 따른다"를 최종 해소 단계로 옮긴 것이다.

**파이프라인 공백**: 저작된 흡수규칙 1개(인장위조←사문서위조)는 조건 평가가 필요한데
`run_v2_absorption_condition_pairs.py` 산출물이 현재 체인에 없어 조건이 영구 UNKNOWN이다.
doctrine 단계와 같은 성격이고 재실행 때 함께 넣는다.

**공백으로 남기는 것**: 상상적 경합은 저작된 규칙이 0개다. legacy 4개가 포팅되지 못한 이유는
v2 죄명 쪽 결손이고, `gap.assault_offense_family`·`gap.stolen_property_offense_family`로 이미
기록되어 있다. 경합 축의 결함이 아니므로 여기서 열지 않는다.

종료 테스트: [`tests/test_concurrence_axis_contract.py`](../../tests/test_concurrence_axis_contract.py)
— 저작 규칙 전수의 endpoint 실재·후보 개방, 파생실현 실현 식별자의 해소와 모호할 때의 침묵,
가담자 흡수 전파의 대체 조건, 두 부모 충돌 시 자식 잔류.

### AnswerPlan / Call 3 handoff (2026-08-15)

축이 아니라 전달 감사였다. 결함은 전부 "모르는 것을 아는 것처럼 넘긴다" 한 방향이었다.

| 결함 | 조치 |
|---|---|
| `open_points`가 비었을 때 "없다"를 적어 완결성을 적극 선언 | 빈 값이면 항목 자체를 생략 (26 → 0) |
| Call 3가 조문을 스스로 짜맞추도록 방치 | 쟁점 단위 정규화 authority를 typed로 공급 (202 → 115행, 맨숫자 30 → 0, 중복 28 → 0) |
| unresolved 전량을 넘겨 답안이 미확정 나열로 채워짐 | live frontier만 (799 → 687행, 살인죄 10 → 2) |
| 내부 작업 메모가 `canonical_meaning`을 타고 답안까지 노출 | detector가 아니라 **정의 본문**에서 제거 |
| governing provision 없는 쟁점 | 114 → 0 |

파생죄 25개 중 17개에 `identity`(죄명·조문)를 저작했다. 특수강도강간은 형법이 아니라
**성폭력처벌법 제3조 제2항**이다. 특수존속중상해는 제258조의2 제2항이 "제258조의 죄"를
통째로 인용하므로 유지한다.

Call 3 프롬프트는 두 곳을 조인 상태로 설치했다 — 새 죄명·공범형태·법률효과·최종 죄수관계를
스스로 제기하지 않는다(놓친 죄는 upstream recall error로 남긴다), 검토 범위는 `analysis`가
제시한 죄로 한정한다. 실경합은 후보로만 서술한다.

종료 테스트: [`tests/test_answer_plan_handoff_contract.py`](../../tests/test_answer_plan_handoff_contract.py)

## 코드베이스 전수 감사 조치 (2026-08-15)

`CODEBASE_AUDIT.md`가 축별 감사로는 잡히지 않는 결함 10건을 보고했다. 전부 **모듈 안에서는
계약이 초록인데 단계 사이에서 그 계약이 소비되지 않는** 한 가지 모양이었다. 아래가 조치
결과이고, 각 줄의 종료 증명은 옆의 테스트다.

| 감사 | 조치 | 종료 테스트 |
|---|---|---|
| P0-A Call 2 scheduler가 planner target을 탈락 | scheduler는 자기 표현식으로 이유를 댈 수 있을 때만 target을 뺀다. 표현식이 없는 것도, 외부 producer가 함께 연 것도 빼지 않는다(`opened_by` 보존). `blocked_when`도 후보·frontier에 넣었다 | [`tests/test_planned_target_reaches_call2.py`](../../tests/test_planned_target_reaches_call2.py) |
| P0-B doctrine plan에서 lineage hard fail | 이미 `b46637c`에서 계보 방식으로 해소 | `test_plan_lineage_contract.py` |
| P1 `evidence_scope` 기본값이 planner와 Call 2에서 다름 | 폭의 권위를 `carrier_contract.effective_evidence_scope` 하나로 모으고 두 직렬화가 모두 그것을 쓴다 | `test_evidence_scope_carrier_contract.py` |
| P1 참가 group identity가 행위자 집합뿐 | 관계의 신원을 `(행위자, realization)`로. 후보 occurrence는 증거 식별자라 신원이 되지 않는다(`identity.realization_identity`) | `test_participation_axis_contract.py` |
| P1 중앙 carrier validator가 Call 2에 없음 | `run_v2_call2_pilot`이 진입에서 `validate_plan_carriers`를 부른다 | `test_carrier_contract.py` |
| P1 temporal anchor가 조용히 넓어짐 | `resolve_carrier`의 unanchored fallback 제거, planner의 `ensure_carrier`도 좁힐 수 없으면 hard fail | `test_carrier_contract.py` |
| P1 `blocked_when`이 type check 밖 | completion·doctrine 양쪽 checker가 `when`/`requires`와 똑같이 순회한다 | `test_definition_system.py` |
| P1 excess join이 별개 실현까지 연결 | 닫지 않는다 -- 닫으면 질적 초과(r11)가 함께 죽는다. `same_execution`으로 근거를 싣고 아닌 것은 분류·귀속·symbolic 효과 없이 `EXCESS_ACROSS_EXECUTIONS`로만 남긴다 | `test_excess_candidates.py`·`test_final_responsibility.py` |
| P1 chain이 stale 조합을 만들 수 있음 | manifest가 **읽은 입력 전부**의 내용 해시를 적고, Call 2·symbolic 진입에서 검증한다. 규칙베이스 변경은 경고로만 남긴다 | `test_plan_lineage_contract.py` |
| P1 Call 3 완결성 감사 함수를 아무도 안 부름 | runner가 부르고 manifest·행에 기록하며 어긋나면 종료코드 2. 오프라인 감사도 같은 함수를 쓴다 | `test_answer_plan_required_conclusions.py` |
| P1-eval LCR baseline 명칭 | "공식 구현 무수정 실행" 주장을 걷고 **LCR-inspired prompting baseline**으로 정정. `baseline_id`는 조인 키라 유지 | — |
| P2 정리 | 참가 빌더의 carrier 복사본 제거, `rubric_evaluator`의 침묵 파싱 실패를 예외로, 옛 `v2`·Phase-3·수기 gold 모듈에 정향 헤더 | — |

**재검토에서 마저 닫은 세 곳(2026-08-15).** 위 조치가 계약을 세웠지만 그 계약을 끝까지
일관되게 적용하지 못한 자리가 셋 남아 있었다. 셋 다 새 법리가 아니라 이미 정한 계약의
적용 범위 문제다.

* scheduler가 `opened_by`를 버리고 ref만 받았다. 한 predicate를 이 죄의 요소로도 쓰고
  doctrine이 따로 열기도 하면 같은 ref 하나로 보이고, 이 죄가 그것을 더 이상 필요로 하지
  않게 된 순간 지워진다. 그 판단은 이 죄에 대해서만 옳다. 개방 이유를 함께 넘기고, 기본
  요소 opener(`ELEMENT_DERIVED_OPENERS`)만 pruning 대상으로 둔다 -- 목록에 없는 opener는
  등록되기 전부터 보호된다. 같은 결함의 producer 쪽 절반도 함께 닫았다 -- doctrine이
  필요로 하는 leaf가 마침 그 죄의 일반 요소이면 빌더가 기존 target을 재사용하면서 이유를
  버렸고, 그러면 행에는 `unspecified` 하나만 남아 runner가 그것을 element-derived로 읽는다.
  재사용도 결과에서 빼지 않고 `also_opened_by`로 합친다. 참가 빌더의 probe·mode 요건도
  같은 자리에 같은 구멍이 있었고, 병합 규칙은 `target_scheduling.merge_target_opener` 하나가
  소유한다. `post_participation_derived_group`만 합치지 않는다 -- 파생 group 위의 일반
  구성요건이라 offense/completion 표현식이 그 필요를 그대로 표현한다.
* 참가 빌더가 읽는 상호작용·inventory·case list가 `plan_inputs` 밖에 있어 기록만 되고
  freshness 검증에서는 빠졌다. 기록하는 목록과 검증하는 목록을 하나로 맞췄고, 빌더가 읽는
  Path 인자가 전부 그 안에 있는지 테스트가 확인한다.
* `same_execution=False`인 초과 후보에 unresolved marker와 확정된 분류·귀속이 동시에 붙었다.
  모른다고 적으면서 효과를 확정하면 그 unresolved는 아무것도 막지 못하는 장식이다. 이제
  후보와 provenance만 남기고 `classify_excess`·귀속·symbolic parity 행은 만들지 않는다.

**측정된 사실 하나.** 완주한 Call 2(`experiments/v2_axis_closure_26_e2e/call2/`)에서
`doctrine_raising_cue` 39개, `participation_mode_requirement` 27개, `participation_candidate_probe`
4개가 **한 건도 질문되지 않았다**(planned 39/27/4 → asked 0/0/0). doctrine 축과 participation
축에서 살렸다고 판단한 경로는 그 실행에서 실제로는 닫혀 있었다. 따라서 그 Call 2 산출물은
두 축의 검증 artifact로 쓸 수 없고, symbolic부터 이어 돌리는 것으로는 확인되지 않는다.
같은 사고가 다시 조용히 지나가지 않도록 Call 2 산출물이 `target_scheduling.asked_by_opened_by`·
`skipped_by_opened_by`를 producer 단위로 기록한다.

## 반복된 결함 클래스: producer마다 흩어진 불변식

축과 무관하게 **같은 모양의 결함이 세 번 반복**됐다. 축별 감사로는 잡히지 않는 종류이므로
따로 기록한다.

> 하나의 불변식을 각 producer가 자기 코드로 따로 구현하면, 한 곳을 고쳐도 다른 producer로
> 전달되지 않는다. 결함은 producer 수만큼 나뉘어 하나씩 터진다.

**(1) target → carrier.** ordinary element는 planner가, participation target은 참가 빌더가
carrier를 붙였고, doctrine leaf는 **아무도 붙이지 않았다**. `evidence_scope` 계약을 고쳐도
다른 producer에 전달되지 않았고, doctrine 단계를 체인에 넣자 Call 2가 `missing=3`으로 처음
알려 줬다. 여기서 realization carrier를 일괄로 붙이는 대증 수정을 한 번 했고, 이는 검수에서
**같은 결함을 세 번째 푸는 중**이라고 지적받아 되돌렸다.

정본 수정: [`src/idpr/v2/runtime/carrier_contract.py`](../../src/idpr/v2/runtime/carrier_contract.py)가
계약을 단독 소유하고, 세 producer 전부 이것을 쓰며, 각 빌더는 `validate_plan_carriers`로
끝난다. 중앙화하자 두 결함이 더 드러났다 — 참가 예외가 predicate 성질이 아니라 instance
성질이라는 것, provenance identity가 `occurrence_id` 하나가 아니라
`(actor, offense_ref, occurrence_id)`라는 것(절도와 특수절도가 `realization:001`을 공유한다).

종료 테스트: [`tests/test_carrier_contract.py`](../../tests/test_carrier_contract.py)

**(2) plan lineage.** 같은 클래스가 네 번째로 나왔다. symbolic 가드가 plan manifest의 `step`
**이름 하나**를 하드코딩해 참가 병합 여부를 확인했는데, plan은 증강되는 파일이라 그 위에
doctrine target이 얹히면 마지막 이름이 당연히 달라진다. 그래서 **실제로 참가 병합을 거친**
plan이 거부되며 2026-08-15 체인이 symbolic에서 끊겼다.

이름을 하나 더 허용하는 수정은 다음 증강 단계에서 또 끊긴다. 확인해야 하는 것은 마지막
단계의 이름이 아니라 **거쳐 온 단계의 집합**이다.
[`src/idpr/v2/runtime/plan_lineage.py`](../../src/idpr/v2/runtime/plan_lineage.py)가 계보를
소유하고, 증강 단계는 입력 plan의 계보를 이어받아 기록하며, 소비자는 계보로 확인한다.
계보를 이어받지 않는 새 증강 단계는 그 자리에서 걸린다.

같은 자리에서 재현성 결함도 하나 나왔다. doctrine 빌더가 `expressions.leaf_refs`(frozenset)를
그대로 반복해 leaf 순서가 해시 시드마다 달라졌다. plan manifest는 sha256을 provenance로
남기므로 순서 비결정성은 그 기록을 무의미하게 만든다. 정렬로 고정했다.

종료 테스트: [`tests/test_plan_lineage_contract.py`](../../tests/test_plan_lineage_contract.py)

**다음 세션에 대한 함의**: plan을 증강하는 단계나 target을 여는 모듈을 새로 만들면, 그
모듈 안에 불변식을 다시 구현하지 말고 위 두 계약 모듈을 쓴다. 새 불변식이 필요하면 그것도
producer가 아니라 별도 계약 모듈이 소유해야 한다.

## 재실행 시점 (2026-08-15 확정)

축마다 GPU를 돌리지 않는다. 남은 축에서 구조 결함이 나오면 1.5 계열·plan·Call 2 artifact가
다시 바뀌어 중간 checkpoint가 하나 더 생긴다. 순서는:

> 네 축 감사 완료 → 구조 수정 전부 동결 → Call 1.5-P(episode 스코프) · Call 1.5-D 재생성
> → doctrine target plan → 흡수조건 pair 평가 → 최종 plan → Call 2 한 번

체인에 빠져 있는 단계가 둘이다. Call 1.5-D + `build_v2_doctrine_target_plan.py`가 없어 13개
doctrine 전부가 잠들어 있고, `run_v2_absorption_condition_pairs.py`가 없어 흡수규칙 1개의
조건이 영구 UNKNOWN이다. 둘 다 frozen root에서는 동작했다.

지금 GPU로 확인해야 할 긴급 회귀는 없다. reachability와 mode resolution은 계약 테스트로
고정되어 있고, 기존 Call 2 산출물에 대한 symbolic 회귀는 26/26 동일하다.

## 현재 실행 상태 (2026-08-15 11:47 기준)

네 축을 닫은 뒤의 첫 전체 관통. 실행 루트: `experiments/v2_axis_closure_26_e2e/`
체인 정의: [`scripts/slurm/run_v2_axis_closure_e2e.sh`](../../scripts/slurm/run_v2_axis_closure_e2e.sh)
(9단계, `IDPR_AXIS_SKIP`으로 이어 돌린다). 기존 vLLM allocation 안에서 CPU job step으로만 돈다.

| 단계 | 상태 |
|---|---|
| call15p (episode 스코프) | 완료 — interaction 46, 후보 23 |
| call15d | 완료 — cue 13 |
| plan_participation | 완료 — participation local target 52 |
| plan_doctrine | 완료 — doctrine target 39, final target 758 |
| **call2** | **26/26 완료 — 그러나 doctrine 39·participation 27 target을 하나도 묻지 않았다(P0-A). 재실행 필요** |
| absorption | 완료 |
| **symbolic** | **미실행 — lineage 가드는 해소됐으나 Call 2 재실행이 먼저다** |
| answer_plan · call3 | 미실행 |

체인 도중 발견되어 고친 경로 단절은 셋이다. doctrine leaf의 carrier 누락, 공동정범 그룹
중복(甲·乙 특수절도가 두 interaction에서 각각 확정되어 같은 행위자 집합의 그룹이 둘 생김 —
행위자 집합이 같은 그룹을 병합), plan lineage 가드. 앞의 둘은 Call 2를 통과시켰고 세 번째가
symbolic을 막았다.

이 실행의 판단 기준은 하나다 — **경로 단절만 본다.** 개별 UNKNOWN이나 모델 오판은 이 실행의
판단 대상이 아니다.

직전 정본 루트는 `experiments/v2_action_realization_26_e2e/`이며(Call 1.5 binding 95·action
215는 이 실행에서도 그대로 입력으로 쓴다), frozen-before
`experiments/v2_call15_directscope_26_causal/`는 occurrence id 체계가 바뀌어 exact join이
불가능하다. 비교는 (사건·actor·죄명·predicate) 근사 키로만 가능하다.

## 다음 작업

> 이 절과 위의 「현재 실행 상태(11:47)」는 아래 「production E2E 관통 (2026-08-15 06:00)」
> 절이 대체한다. 세 항목 모두 그 절에서 실행·확인되었다.

1. **Call 2부터 다시 돌린다.** symbolic 재개가 아니다 -- 위 감사에서 확인된 대로 기존 Call 2는
   doctrine·participation target을 하나도 묻지 않았고, 그 산출물로는 두 축이 관통했는지
   알 수 없다. `IDPR_AXIS_SKIP="call15p call15d"`로 plan부터 다시 만든다(plan 단계는 CPU만
   쓰고 결과가 재현된다 -- 758 target 동일 확인). Call 2 완료 후 산출물의
   `target_scheduling.asked_by_opened_by`에서 `doctrine_raising_cue`와
   `participation_mode_requirement`가 0이 아닌 것을 먼저 확인한다.
2. **경로 관통 확인.** leaf 진리값 → `active_doctrine` → doctrine effect → derivative
   participation/link → 최종 책임 → AnswerPlan → Call 3. 끊긴 지점만 구조 수정 대상이다.
3. **UNKNOWN 문제** — 관통 이후로 미룬 항목. 발화하지 않은 규칙과 활성화되지 않은 지점을
   실제 답안에서 찾는다.

## 검수가 남은 항목

- `statutory_bar_on_consent` 긍정형 전환 (doctrine 축)
- 가담자 흡수 전파 = "가담자의 죄명은 정범의 죄명을 따른다"의 최종 해소 단계 이동 (concurrence 축)
- 초점행위 근사가 행위 단일성 판단으로 충분한가
- 상상적 경합 저작 0개 — KCL 루브릭이 죄수관계를 직접 배점하므로 공백이 곧 실점이다
- 초과 후보의 `same_execution=False` 처리 — 교사받은 실행이 더 나아간 것과 정범의 별개
  범행을 상류 provenance로 가를 수 없어 unresolved로 올린다. 그 선이 맞는지

## 측정할 때 유의점

동일 입력·동일 프롬프트에서도 Call 2 결과가 약 9% 흔들린다. 따라서 20~30건 규모의 총계
변화는 노이즈와 구분되지 않는다. 판단은 deterministic한 symbolic 단계 출력으로 한다.

---

## production E2E 관통 (2026-08-15 06:00)

실행 루트 `experiments/v2_final_e2e_26/`. 위의 「현재 실행 상태(11:47)」와 「다음 작업」은
이 절이 대체한다. 코드베이스 감사 10건 + 재검수 3+1건을 모두 닫은 뒤의 첫 전체 관통이다.

| 단계 | 결과 |
|---|---|
| plan 재생성 | 758 target 재현 (결정론 확인) |
| call2 | 26/26, planned 758 중 asked 691 |
| absorption · symbolic | 26/26 |
| answer_plan | 26/26 |
| call3 | 26/26 |

**P0-A는 실측으로 닫혔다.** 직전 산출물에서 0이던 external opener가 전부 질문되었다.

| opener | planned | asked |
|---|---:|---:|
| `doctrine_raising_cue` | 39 | 39 |
| `participation_mode_requirement` | 27 | 27 |
| `participation_candidate_probe` | 4 | 4 |

downstream 계보 추적 결과 **경로 손실 0**이다. participation TRUE relation 17건은
정상 소멸 / 정상 반영으로 전부 설명되고, active doctrine 5건(정당방위 4 · 법률의 착오 1)은
raised → leaf truth → active → 최종 책임 → AnswerPlan → Call 3까지 끊긴 지점이 없다.
공동정범 3건의 답안 서술 누락은 구조 경로 손실이 아니라 generation/evaluation exposure
문제로 분리했다.

측정값: offense instance 122 중 성립 21(17%), elements 단계 정지 69, completion 단계 정지 32,
AnswerPlan unresolved anchor 93/122(76%), Call 2 UNKNOWN 418/691(약 60%).

### completion semantics — 검수 완료, 구조 유지

`attempted.when = commencement AND NOT(completion)`을 결함으로 의심했으나 **법률 검수에서
현행 저작이 맞다고 확정**되었다.

- 형법 제25조 제1항이 비기수성을 **미수범의 구성요건 요소**로 규정한다. 중지미수(제26조)·
  불능미수(제27조)는 별개 조문이므로 그쪽을 `defeated_by_state`로 모델링한 것은 옳고,
  같은 장치를 미수 일반에 쓰면 안 된다.
- 이를 바꾸면 법정 요소가 미확정인 상태에서 시스템이 "미수 성립"을 적극 출력하게 되어
  비단조적 잠정 상태가 된다.
- 따라서 `commencement=TRUE + completion UNKNOWN` 16건은 결함이 아니라 **정당한 3-valued
  unresolved state**다. 그 UNKNOWN의 원인이 사실관계의 진짜 모호성인지 Call 2 판독 실패인지는
  sealed-59를 열지 않는 한 미측정으로 남는다.

completion 축은 이로써 다시 닫는다.

### 0-TRUE predicate 사례비의존 감사

sealed 사례의 사실판단 없이 definition이 답변 가능한 형태인지만 정적으로 검사했다.
두 건이 나왔고 둘 다 성격이 다르다.

1. **`legal_element.offender_status_of_object` — 파이프라인 공백 (구조 결함).**
   `legal_standard`가 스스로 "caller가 명시한 linked OffenseInstanceKey의 qualifying
   liability result로만 판단"한다고 선언한다. 즉 neural predicate가 아니다. 호스트 경로
   `resolve_article_151_liability()`는 [`statutory.py:42`](../../src/idpr/v2/runtime/statutory.py#L42)에
   구현되어 있으나 **레포 전체에 호출부가 없다**. 그 결과 Call 2에 6번 질문되어 6/6 UNKNOWN이고,
   범인은닉도피죄 object 슬롯은 어떤 사건에서도 확정될 수 없다. 제263조 경로는 연결되어 있고
   제151조만 빠졌다. → `RULEBASE_AUDIT.md` P0-R1.
2. **`ground_fact.means_or_object_defect` — 법률/저작 검수 대상 (구조 결함 아님).**
   45 asked / TRUE 1 · UNKNOWN 44 · **FALSE 0**. `legal_standard`가 없고 semantic exclusion
   둘이 각각 흔한 FALSE 경로와 흔한 TRUE 경로를 막는다. `GroundFactDef`는 `legal_standard`가
   필수가 아니므로 schema 위반은 아니다. 파급은 작지 않다 — 이것이 FALSE로 확정되면 불능미수
   분기가 죽고 `dangerousness`(24/25 UNKNOWN)가 정당하게 잘린다. 지금은 70건을 물어 1건을
   얻는다. **승인 없이 정의·프롬프트를 수정하지 않았다.**

나머지 0-TRUE predicate(`bribe_promise` 0/10 등)는 **미측정**으로 남긴다. 같은 형식의 형제
predicate가 TRUE를 받으므로(`bribe_acceptance` 3, `bribe_request` 1) 저작 형식만으로 설명되지
않고, 사실 부재냐 판독 실패냐는 sealed-59를 열지 않는 한 갈리지 않는다.

### 판정

pipeline stage 간 연결이라는 축은 닫혔다. 남은 위험은 **저작했다고 믿는 규칙이 실제 runtime에
존재하는가**로 이동했고, 그 축의 전수감사가 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md)다.
structural freeze는 그 문서의 Phase A를 닫은 뒤에 선언한다.
