# 축별 구조 감사 (axis closure)

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 데드라인 2026-08-19 21:00

이 문서가 현재 상태의 정본이다. `NEXT_SESSION.md`는 append-only 역사 로그이며 그 안의
"다음 작업" 지시는 이 문서가 대체한다.

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

## 재실행 시점 (2026-08-15 확정)

축마다 GPU를 돌리지 않는다. 남은 축에서 구조 결함이 나오면 1.5 계열·plan·Call 2 artifact가
다시 바뀌어 중간 checkpoint가 하나 더 생긴다. 순서는:

> participation 감사 완료 → doctrine 감사 완료 → **concurrence 감사** → 구조 수정 전부 동결
> → Call 1.5-P(episode 스코프) · Call 1.5-D 재생성 → 최종 plan → Call 2 한 번

재실행 체인에 doctrine 단계를 넣어야 한다. 현재 26문항 체인에는 Call 1.5-D와
`build_v2_doctrine_target_plan.py`가 없어서 13개 doctrine 전부가 잠들어 있다.

지금 GPU로 확인해야 할 긴급 회귀는 없다. reachability와 mode resolution은 계약 테스트로
고정되어 있고, 기존 Call 2 산출물에 대한 symbolic 회귀는 26/26 동일하다.

## 남은 축 순서

### 1. Concurrence / final resolution

- absorption, specialty, imaginative concurrence, 이번에 추가한 `definitional_resolution`
- occurrence / same-realization 정합, established liability 사이 최종 중복·배제
- `definitional_resolution` 3규칙은 단위 테스트로 발화를 고정했으나 26문항에서는 아직
  발동하지 않았다(두 죄가 모두 established여야 한다). doctrine 축이 열리면 발동 여지가 생긴다

### 2. AnswerPlan / Call 3 E2E handoff

축이 아니라 전달 감사다. LiabilityResult → AnswerPlan → Call 3에서 symbolic conclusion 누락,
authority·dispute 전달, 내부 status/ID 유출, final conclusion completeness를 본다.

## 현재 실행 상태

정본 artifact 루트: `experiments/v2_action_realization_26_e2e/`

| 단계 | 산출물 |
|---|---|
| Call 1.5 binding | `call15_action_bindings_26.jsonl` (26/26, binding 95, action 215) |
| Call 1.5 interaction | `call15_factual_interaction.jsonl` |
| plan | `plan_ckpt_participation/` (instance 108, final target 660) |
| Call 2 | `call2_ckpt/` |
| symbolic | `scallop_ckpt/` |

현재 수치: establishment 확정 18 / elements satisfied 18 · failed 8 · unresolved 60 /
completion completed 80 · attempted 3 · unresolved 27.

기존 frozen-before는 `experiments/v2_call15_directscope_26_causal/`이며, occurrence id 체계가
바뀌어 exact target join이 불가능하다. 비교는 (사건·actor·죄명·predicate) 근사 키로만 가능하다.

## 측정할 때 유의점

동일 입력·동일 프롬프트에서도 Call 2 결과가 약 9% 흔들린다. 따라서 20~30건 규모의 총계
변화는 노이즈와 구분되지 않는다. 판단은 deterministic한 symbolic 단계 출력으로 한다.
