# Call 2 UNKNOWN은 어디서 오는가 — 진단 체크포인트

2026-08-14. rubric은 확정 결론(성립/불성립, 견해 대립의 서술)을 요구하는데 N·P 답안은
앵커 105개 중 81개(73%)를 미확정으로 남겼다. 채점에 돈을 쓰기 전에 상류를 봤다.

이 문서는 **진단만** 기록한다. production planner·프롬프트는 아직 건드리지 않았다.

## 진단기 둘

| 스크립트 | 하는 일 | 모델 호출 |
| --- | --- | --- |
| `scripts/diagnose_v2_call2_evidence_scope.py` | 동결된 타깃을 두 번 재생. 프롬프트·스키마·타깃 전부 동일하고 `evidence_occurrence.source_text`만 occurrence 인용문 / 사실관계 전문으로 다르다 | 로컬 vLLM, 무료 |
| `scripts/diagnose_v2_call2_target_necessity.py` | 동결된 truth로 completion policy를 Kleene 부분평가. 그 predicate 값을 바꿔도 결과가 안 변하면 moot | 없음 |

necessity 판정은 **3치 반사실**이다. `{TRUE, FALSE, UNKNOWN}` 전부를 대입해 결과가 하나로
고정되는지 본다. UNKNOWN은 빠진 답이 아니라 의미값이므로, TRUE/FALSE만 뒤집어 비교하면
"어느 쪽이어도 가드가 UNKNOWN"인 predicate를 moot로 잘못 지우게 된다. 이 데이터에서는
2치와 3치의 결과가 같았지만(317/164/72), 판정 근거는 3치가 맞다.

## denominator -- 어느 plan인지부터

이 실행에는 **evaluation instance plan이 두 개** 있고, 처음에 잘못된 쪽을 봤다.

| artifact | 타깃 | 쓰인 곳 |
| --- | --- | --- |
| `evaluation_instance_plan.jsonl` (sha `a025da…`) | **531** | 26문항 Call 2 본실행 |
| `call15d_v4/evaluation_instance_plan.jsonl` (sha `1a10c5…`) | 553 | 이후 3문항 delta 실행 |

아래 숫자는 **본실행이 쓴 531 타깃 기준**이다. 두 plan의 차이 22건은 **전부 moot·정의없음
버킷**이고 live는 317로 동일하므로, 어느 쪽을 보든 결론은 같다. 그래도 인용할 수치는
본실행 쪽이어야 한다.

| bucket | 계획 531 |
| --- | --- |
| live | **317** |
| moot | **148** |
| 정의 없음 | **66** |

Call 2는 GroundFact를 factual episode당 한 번만 평가하므로, 형제 occurrence에 걸린 같은
GroundFact는 자기 키로 돌아오지 않는다(46건, 전부 `ground_fact`).
`kcl_criminal_r12_p2_q1_na`는 assessment target이 0이다.

**미결:** 증거창 진단(507 키)은 `call15d_v4` 타깃으로 돌렸으므로 531 plan과 키 집합이
어긋난다. 아래 UNKNOWN 3분할은 그래서 근사치이고, 두 진단을 같은 plan으로 맞춰
재계산해야 확정된다.

## UNKNOWN 275건의 3분할 (평가된 507 기준, 근사)

| 원인 | 건수 | 비중 |
| --- | --- | --- |
| moot·정의없음 타깃에서 나온 UNKNOWN | 130 | 47% |
| 증거 창 — 사실관계 전문을 주면 풀림 | 71 | 26% |
| 창을 넓혀도 안 풀림 (정의·판정) | 74 | 27% |

### 증거 창 실측 (25문항 507 타깃)

| | occurrence 인용문 | 사실관계 전문 |
| --- | --- | --- |
| UNKNOWN | 275 (54.2%) | 201 (39.6%) |
| TRUE | 205 | 289 |
| FALSE | 27 | 17 |

이동: UNKNOWN→TRUE 107, TRUE→UNKNOWN 28, FALSE→UNKNOWN 13, UNKNOWN→FALSE 8,
**FALSE→TRUE 5(정면 모순)**. 넓은 창은 다른 occurrence의 사실을 끌어와 오귀속한다.
증거를 occurrence로 좁힌 원래 설계 이유가 실측으로 확인된 셈이므로, 전면 교체는 답이
아니다.

커버리지로 나눠도 갈리지 않는다 — 커버리지 <0.5 (191타깃) 53.4%→36.1%,
≥0.5 (316타깃) 54.7%→41.8%. **증거를 사실관계의 80% 넘게 주는 문항도 UNKNOWN이 55%다.**
"증거를 33%만 보여줘서"라는 초기 가설은 전수 데이터가 지지하지 않는다.

## (b) 죽은 가지 타깃 — 가장 큰 몫

플래너가 completion policy에 등장하는 predicate를 평면으로 펼쳐 전부 요청한다. 가드가
연언인데 앞 항이 이미 FALSE인지 보지 않는다.

```yaml
impossible_attempt:
  when:
    op: all
    args:
      - {op: ref, ref: legal_element.commencement_of_execution}
      - {op: not, arg: {op: ref, ref: ground_fact.death_of_victim}}
      - {op: ref, ref: ground_fact.means_or_object_defect}
      - {op: ref, ref: legal_element.dangerousness}
```

`legal_element.dangerousness`는 33개 instance에 걸렸고 그중 14개는
`ground_fact.means_or_object_defect`가 이미 FALSE다. 불능미수가 성립할 여지가 없는데
위험성을 묻고, UNKNOWN을 받고, 그 UNKNOWN이 답안까지 올라간다.

죽은 가지가 그대로 올라간 상위 항목 (instance 수):

| | |
| --- | --- |
| `offense.injury::attempted` / `::impossible_attempt` | 8 / 8 |
| `offense.homicide::abandoned_attempt` / `::impossible_attempt` / `::preparation` | 6 / 6 / 6 |
| `offense.theft::attempted` / `::impossible_attempt` | 6 / 5 |

**DSL은 가드를 정확히 적어뒀고, 플래너가 그 논리구조를 평탄화했다.** 정의 결함이 아니다.

### 이 수치를 논문에 쓸 때

`moot = 148`은 **회고적**이다. 어떤 항이 blocker인지 알려면 그 항을 먼저 물어야 하므로,
prospective 실행에서 148개를 처음부터 전부 생략할 수 있다는 뜻이 아니다. 정확한 표현은
"148 targets were retrospectively non-influential"이다.

동결 truth를 오라클로 삼아 새 스케줄러를 시뮬레이션하면 **531 → 436 (17.9% 감소)**이고,
생략된 95건의 동결 truth는 UNKNOWN 62 / FALSE 23 / TRUE 10이다. 회고적 148과 실제 95의
차이가 정확히 "blocker를 알기 위해 물어야 했던 몫"이다. 26문항 중 21개가 1라운드,
3개가 2라운드, 1개가 3라운드에 수렴한다.

절감보다 중요한 것은 품질이다: **성립 가능성이 이미 죽은 completion branch의 UNKNOWN을
최종 AnswerPlan에 legal uncertainty처럼 흘려보내지 않는다.** 살인예비·불능미수 같은 죽은
쟁점이 미확정으로 줄줄이 서술되는 것이 사라진다.

## (a) 정의·판정 — live 297 중 UNKNOWN 145 (48.8%)

창을 넓혀도 안 풀리는 74건. live UNKNOWN 상위:

| predicate | live | UNKNOWN | 비율 | 뜻 |
| --- | --- | --- | --- | --- |
| `ground_fact.taking_conduct` | 19 | 12 | 63% | 타인 점유 재물을 자기 점유로 |
| `legal_element.intent` | 25 | 11 | 44% | 고의 |
| `legal_element.unlawful_appropriation_intent` | 16 | 11 | 69% | 불법영득의사 |
| `legal_element.possession` | 12 | 11 | 92% | 사실상 지배+점유의사 |
| `legal_element.official_or_arbitrator_status` | 4 | 4 | 100% | 공무원·중재인 |
| `legal_element.job_relatedness` | 4 | 4 | 100% | 직무관련성 |
| `legal_element.trespass_entry` | 5 | 5 | 100% | 평온을 해하는 침입 |

실제 사례를 열어보면 성격이 셋으로 갈린다.

**① 초literal 판정.** `official_or_arbitrator_status`, `r11_p2_q1_ga` 甲:

> 증거: "甲은 丙을 **군수집무실**로 불러 A군(郡)이 둘레길 조성사업을 계획하고 있는데…"

군수집무실에서 군정을 논하는 甲이 공무원인지가 UNKNOWN이다. `possession`,
`r12_p1_q2` 甲: "약혼녀인 **C의 지갑**에서 수표를 꺼내 가져갔다"에서 C의 점유가
UNKNOWN이다. 시스템 프롬프트의 *"문항의 다른 부분, 일반적인 사건 추측, 상식으로 보충한
사실은 사용하지 않는다"*가 **통상의 법적 포섭까지 금지하는 것으로 읽히고 있다.**
금지해야 하는 것은 새 사실의 창작이지 명시된 사실로부터의 통상적 추론이 아니다.

**② occurrence 오배치.** `possession`, `r11_p1_q1` 乙 강도죄의 증거는 폭행 문장뿐이고
재물이 등장하지 않는다. 절취는 다른 occurrence에서 일어났다. UNKNOWN이 정직한 답이고,
물어본 자리가 틀렸다.

**③ 진짜 논점.** `possession`, `r12_p2_q1_ga` 乙: "살해를 한 직후 A 소유의 명품 시계를
가지고 나왔다" — 사자의 점유 문제다. UNKNOWN이 법적으로 옳다. 문제는 AnswerPlan이 이걸
논점이 아니라 미확정으로 흘려버린다는 것이다. rubric이 요구하는 것은 바로 이 대립이다.

## (b) 구현 -- `src/idpr/v2/runtime/target_scheduling.py`

두 규칙을 분리했다.

- `live_predicate_refs` = **정합성 규칙.** 어떤 slot 식·state 가드·살아 있는 state의
  `requires`가 그 predicate 값에 따라 다른 말을 하면 live다. 대입은 3치 전부에 대해 한다.
- `frontier_predicate_refs` = **일정 규칙.** 연언은 저작 순서로 읽고 아직 정해지지 않은
  첫 항에서 멈춘다. 뒤의 항은 앞의 항이 가드를 죽이지 못한 뒤에야 도달한다.

**predicate 종류를 보는 규칙은 어디에도 없다.** `means_or_object_defect`가
`dangerousness`를 막는다는 지식도 없다. blocker가 `legal_element`인 경우
(`commencement_of_execution`가 세 attempt state를 한꺼번에 죽이는 경우)도 동일하게 처리되고,
그것이 `tests/test_target_scheduling.py`의 검사 항목이다.

`live`와 `frontier`가 다른 것이 핵심이다. 아무것도 모르는 상태에서 `dangerousness`는
live지만 frontier가 아니다 — 생략이 아니라 유예다.

스케줄링은 플래너의 후보 집합에서 **빼기만 한다**(`candidate_refs`). 플래너는 predicate
scoping·doctrine raising·participation 때문에 타깃을 좁히는데, 그 이유를 이 모듈은 모른다.

실행기(`scripts/run_v2_call2_pilot.py`)가 라운드를 돌린다. 각 라운드의 답은
`expand_ground_fact_assessments`를 거쳐 되먹임되므로, episode 단위 GroundFact 하나가
그 episode를 쓰는 모든 instance의 가드를 함께 죽인다. `--flat-targets`로 이전 동작을
그대로 재현할 수 있고, 케이스마다 `target_scheduling`(모드·라운드·planned/asked/skipped)이
artifact에 남는다.

dev 2문항 실제 실행 결과:

| 문항 | planned → asked | 라운드 | 결과 |
| --- | --- | --- | --- |
| `r13_p1_q3` | 12 → 9 | 7, 2 | TRUE 6 / FALSE 2 / UNKNOWN 1 |
| `r14_p2_q2` | 28 → 21 | 21 | TRUE 6 / FALSE 2 / **UNKNOWN 13** (동결 22) |

## 순서

1. ~~**(b) guard-aware iterative planner.**~~ 완료.
2. 두 진단을 같은 plan으로 재계산(위 미결 항목).
3. 26문항 재실행 → residual UNKNOWN 재진단.
4. 증거 스코프.
5. 마지막에 초literal 프롬프트 문언. **활성 프롬프트 변경이므로 승인 게이트 대상.**

③의 "진짜 논점을 미확정이 아니라 쟁점으로 승격"도 나머지가 정리된 뒤 검토한다.

## 산출물

- `experiments/v2_call15_directscope_26_causal/diagnostics/call2_evidence_scope_26.json`
- `experiments/v2_call15_directscope_26_causal/diagnostics/call2_target_necessity.json`
