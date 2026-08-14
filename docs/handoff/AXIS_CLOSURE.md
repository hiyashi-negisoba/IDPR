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
| `blocked_when` | completion policy | 사실조건이 **확정**되면 그 상태 배제 |
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

## 남은 축 순서

### 1. Participation / attribution

- 공범 target reachability, direct/derived participation
- 교사·방조 우선관계, principal realization dependency
- relation carrier 정합 — evidence carrier 축에서 예외로 남긴 participation 14건이 여기 속한다
- **미해결 회귀**: participation target이 frozen-B 60 → 32로 줄었다. action 단위에서 중복이
  제거된 것인지 회수가 후퇴한 것인지 아직 판정하지 않았다
- Scallop이 Call 2가 확정한 공범 관계의 endpoint를 instance universe에 없다는 이유로 거부하던
  결함은 runner에서 막아 두었으나, 계약상 소유자는 이 축이다

### 2. Doctrine / stage-effect

- 착오, 간접정범, 제33조, excess, doctrine activation/effect
- 감사 질문: trigger는 존재하는데 effect가 symbolic liability까지 실제 도달 가능한가

### 3. Concurrence / final resolution

- absorption, specialty, imaginative concurrence, 이번에 추가한 `definitional_resolution`
- occurrence / same-realization 정합, established liability 사이 최종 중복·배제
- `definitional_resolution` 3규칙은 단위 테스트로 발화를 고정했으나 26문항에서는 아직
  발동하지 않았다(두 죄가 모두 established여야 한다). doctrine 축이 열리면 발동 여지가 생긴다

### 4. AnswerPlan / Call 3 E2E handoff

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
