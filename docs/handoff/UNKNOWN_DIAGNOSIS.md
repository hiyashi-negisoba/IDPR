# residual UNKNOWN 진단 (수정 없음)

기준 실행: `experiments/v2_rulebase_regen_26/` · 2026-08-16 · 브랜치 `deadline_v2_0808`
재현: `python scripts/audit_v2_unknown_failure_modes.py --run experiments/v2_rulebase_regen_26`

이 문서는 **진단이다.** 정의·프롬프트는 한 줄도 바꾸지 않았고, 구조 baseline과 A1~A4는
건드리지 않았다. 변경안은 아래 판단이 승인된 뒤 별도 문안으로 올린다.

## 0. 제약과 재료

사례 본문은 열지 않았다. 열 필요도 없었다 — Call 2 산출물에는 rationale도 사건 텍스트도
없고 `instance_key` · `predicate_ref` · `truth` 세 필드뿐이다. 그래서 이 진단의 재료는
target metadata(요건 자리·소유 죄명·저작 표면)와 **같은 instance 안에서 동시에 답해진 다른
predicate의 상태**뿐이다. 사례 이름이 노출되는 줄은 승인된 dev 2건에 한정했다.

baseline 재현: `planned 635 / asked 595 / TRUE 286 / FALSE 21 / UNKNOWN 288 (48.4%)`.
instance 141개, case 25개. frozen baseline과 일치한다.

## 1. 288개 UNKNOWN의 분해

우선순위를 두어 배타적으로 나눴다(A → C → B → D).

| mode | 수 | 비중 | 정체 |
|---|---:|---:|---|
| **A. instance 전멸** | 46 | 16.0% | 그 instance의 target이 **하나도** 답해지지 않음 |
| **B. 주관적 요건** | 64 | 22.2% | mental slot(고의·목적)에서 물어진 것 |
| **C. 불능미수 계열** | 34 | 11.8% | `means_or_object_defect` · `dangerousness` |
| **D. 나머지** | 144 | 50.0% | 개별 predicate 산재 |

D 상위: `possession` 18 · `taking_conduct` 18 · `aggravated_result_attribution` 10 ·
`injury_result` 6 · `dangerous_weapon_carriage` 6.

## 2. 사전 가설 ①과 실측이 어긋난다

`START_HERE.md` §5①은 `legal_element.intent`의 병목을 **결과적 가중범에서 고의의 대상이
기본범죄인지 중한 결과인지 모호한 것**으로 지목했다. 실측은 그 가설을 지지하지 않는다.

```
intent 전체            asked 42  T 14  F 0  U 28  (66.7%)
  결과적 가중범 소유      asked  9  T  3  F 0  U  6  (66.7%)
  일반 고의 사용처        asked 33  T 11  F 0  U 22  (66.7%)
```

두 갈래가 소수점까지 같다. 결과적 가중범이라는 사실은 UNKNOWN을 **전혀 가르지 않는다.**
가르는 것은 다른 축이다.

**축 1 — 자리(slot).** `mental` 자리는 asked 100 · UNKNOWN 69(69.0%)로 전 자리 중 최악이고,
`causation` 75.0%가 그 다음이다. 반면 `object` 31.6% · `result` 31.0%다.
그리고 `mental` 자리에서 나온 **FALSE는 100건 중 0건이다.** 이 실행 전체에서 고의가
부정된 적이 한 번도 없다. `intent`뿐 아니라 `unlawful_appropriation_intent`(20/33 U),
`knowledge_of_bribery_destination`(6/6 U), `purpose_to_*` 계열이 모두 같은 모양이다.

**축 2 — 같은 instance의 행위 판단과의 괴리.**

```
intent TRUE     × conduct TRUE      13
intent UNKNOWN  × conduct TRUE      23   ←
intent UNKNOWN  × conduct UNKNOWN    5
```

23건에서 Call 2는 **행위는 TRUE로 확정하고 그 행위에 대한 고의만 기권했다.** 사실이 부족해
기권한 것이 아니다. 극단은 `offense.assault`로, `assault_conduct`는 17/17 TRUE인데 같은
instance의 `intent`는 9건 중 8건이 UNKNOWN이다.

이 모양과 정의를 함께 보면 원인이 좁혀진다. `legal_element.intent`의 canonical_meaning은
"객관적 구성요건요소 인식+실현 용인"이고 legal_standard는 "구성요건적 사실을 인식하고 그
실현을 의욕하거나 용인하였는지"다. **어느 구성요건인지가 문안 어디에도 없다.** 인자는
`(actor, act)`뿐이라 대상 요건이 인자로도 들어오지 않는다. 즉 병목은 "기본범죄냐 중한
결과냐"의 양자택일이 아니라, 그 물음이 애초에 **어떤 사실이 답이 되는지 지정하지 않는 것**이다.
결과적 가중범은 그 일반 결함이 드러나는 여러 자리 중 하나일 뿐이다.

> 단, §3에 적힌 위험(폭행치상에서 중한 결과 고의로 읽히면 성립이 뒤집힌다)은 UNKNOWN이
> 아니라 **잘못된 방향의 TRUE**로 나타나므로 이 통계로는 확인도 반증도 되지 않는다.
> 결과적 가중범 instance에서 intent가 TRUE로 답해진 3건이 그 후보다.

## 3. means_or_object_defect → dangerousness: 문안 문제가 아니다

```
means_or_object_defect (upstream)   asked 31  T 5  F 1  U 25  (80.6%)
dangerousness          (downstream) asked 14  T 1  F 0  U 13  (92.9%)
```

lineage를 분리하면 downstream이 먼저 답한다.

```
dangerousness TRUE     × upstream defect UNKNOWN    1
dangerousness UNKNOWN  × upstream defect UNKNOWN   13
```

**14건 전부 upstream이 미확정인 상태에서 열렸다.** `dangerousness`는 형법 제27조의 위험성,
즉 *수단·대상 착오가 인정된 뒤에* 비로소 의미가 생기는 물음인데, 그 전제가 확정되지 않은
instance에서 물어지고 있다. 문안을 아무리 고쳐도 이 14건은 답할 수 없다.

원인은 저작이 아니라 계약이다. [`evaluation_instance_planner.py:461-468`](../../src/idpr/v2/runtime/evaluation_instance_planner.py#L461-L468)은
completion policy의 모든 state에서 `when` · `requires` · `blocked_when` leaf를 무조건 수집한다.
주석이 그 이유를 명시한다 — 묻지 않으면 UNKNOWN으로 남아 아무것도 막지 못하고, 수집 누락이
"이 사건에는 예외가 없다"로 읽힌다. 그래서 `impossible_attempt` state를 가진 죄면 기수든
아니든 `defect`와 `dangerousness`가 함께 열린다.

upstream도 같은 모양이다. `defect` UNKNOWN 25건 중 20건이 `commencement_of_execution = TRUE`인
instance에서 나왔고, 소유 죄명은 `offense.injury` 9 · `offense.theft` 8 ·
`derived_offense.special_theft` 8로 **기수가 문제되는 사건**에 몰려 있다. result slot이 이미
TRUE인 instance에서 물어진 것도 6건이다.

`semantic_exclusions`가 TRUE·FALSE 양쪽을 과하게 막는다는 §5②의 의심은, 이 실행 데이터로는
분리되지 않는다. exclusion 보유 target 82건 중 64건이 `defect`(31)와
`unlawful_appropriation_intent`(33) 둘뿐이라 "exclusion 때문"과 "이 두 predicate 때문"이
공변한다. 반대 방향 증거도 있다 — `alteration_of_genuine_document`(excl=2)는 3/3 FALSE,
`solicitation_received`(excl=1)는 2/2 FALSE다. exclusion 자체가 기권을 유발한다고 말할 수 없다.

## 4. FALSE 희소성(③): 비율이 아니라 위치를 보면 패턴이 있다

FALSE 21건이 나온 자리를 보면 규칙이 하나 보인다. **FALSE는 저작이 "무엇이면 아니다"를 명시한
predicate에서만 나온다** — `alteration_of_genuine_document` 3/3, `solicitation_received` 2/2,
`vaginal_intercourse_conduct` 3/5, `voluntary_cessation_or_prevention` 1/2. 대부분 asked가 5
이하인 소량 predicate다.

반대로 **대량으로 물어지는 predicate에서 FALSE는 구조적으로 0이다.** asked≥6이면서 FALSE 0인
predicate가 16개이고, 그 중 `intent`(42) · `unlawful_appropriation_intent`(33) ·
`possession`(27) · `taking_conduct`(27) · `injury_result`(21) · `assault_conduct`(17)가 상위다.
`assault_conduct`는 17/17 TRUE로 **긍정 아니면 침묵**이라는 이 모드의 순수한 형태다.

찾던 systematic pattern은 이것이다: **부정형 판단 경로가 저작된 predicate에서만 FALSE가 나오고,
그 경로가 없는 predicate는 TRUE 아니면 UNKNOWN 둘로만 답한다.** 특히 mental 자리는 100건
전부가 그 상태다. 이는 FALSE 비율을 목표로 삼는 것과 무관하다 — 정답 분포는 여전히 모르고,
여기서 말하는 것은 "반증이 가능한 물음의 형태를 갖췄는가"뿐이다.

## 5. 저작 표면과의 상관 — confound 포함해서 적는다

| 축 | 결과 | 읽을 때 주의 |
|---|---|---|
| `semantic_exclusions>0` | 65.9% U vs 45.6% | 82건 중 64건이 predicate 2개. 공변 — 인과로 읽지 말 것 |
| `temporal_anchor` 있음 | 6/6 U (100%) | **전부 `knowledge_of_bribery_destination` 하나**. 표본 1 |
| arity 2 | 51.4% vs arity 1 40.7% | 인자가 늘면 지시 대상이 늘어 기권이 는다는 방향과 일치 |
| `ground_fact` | 56.7% vs `legal_element` 46.3% | `legal_standard` 유무와 완전 공변(ground_fact는 전부 미보유) |
| non-focal actor | 60.3% vs focal 45.4% | 초점 행위 밖 행위자 |
| derived offense | 61.2% vs base 42.1% | A3/A4 신규 죄가 포함된 층 |

## 6. mode A(instance 전멸) — 저작으로 닿지 않는 층

141개 instance 중 **23개가 100% UNKNOWN**이고 UNKNOWN 46건을 삼킨다. 죄명은
`embezzlement` 3/6 · `stolen_property_acquisition` 3/4 · `bribe_giving` 2/4 등으로 흩어져 있다.
한 instance의 모든 요건이 동시에 기권됐다면 개별 predicate 문안의 문제로 보기 어렵다.
그 instance가 사건에 실재하지 않는 후보(라우팅·바인딩이 연 가설적 instance)일 가능성이 높고,
그렇다면 UNKNOWN은 오답이 아니라 정상 동작이다. **이 46건을 저작으로 줄이려 하면 안 된다** —
줄이는 순간 없는 범죄를 인정하게 된다.

즉 288 중 실제 저작 개선의 사정거리는 46건을 뺀 **242건**이고, 그 중 확인된 계약 산물
(§3의 defect·dangerousness)을 더 빼면 더 줄어든다.

## 7. 판단을 구한다

문안을 올리기 전에 방향 하나를 정해야 한다.

1. **mode B(주관적 요건 64건)를 먼저 연다.** 사정거리가 가장 크고 원인이 특정됐다 —
   `intent` 계열이 어느 구성요건에 대한 고의인지를 저작이 소유하지 않는다. 다만 이는
   `legal_element.intent` 한 건의 수정이 아니라 **공유 predicate의 정본 의미를 건드리는
   일**이라, 조문별 재정의 금지 원칙과 정면으로 만난다. 설계 판단이 먼저 필요하다.
2. **mode C(불능미수 34건)는 저작 대상이 아니다.** planner 계약이 원인이므로, 고치려면
   구조를 건드려야 하고 그것은 이번 범위 밖이다. 진단만 기록하고 넘긴다.
3. **mode D(144건)는 아직 원인이 하나로 모이지 않았다.** `possession` 18 · `taking_conduct` 18이
   같은 절도 family에 몰려 있어 predicate별이 아니라 **죄 단위로 한 번 더 분해**해야 보인다.

## 8. 비교 규약 (다음 실행에서 반드시 지킨다)

UNKNOWN 감소만 보고 개선을 선언하지 않는다. 저작 변경 후 재실행 시 최소한 다음을 확인한다.

* frozen baseline `595 / 286 / 21 / 288` 대비 **TRUE·FALSE의 감소**를 먼저 본다.
  UNKNOWN → TRUE 전환과 TRUE → UNKNOWN 후퇴가 상쇄되면 총계는 개선처럼 보인다.
* asked 분모가 변했는지 확인한다. rulebase가 바뀌면 planned가 변해 비율 비교가 무의미해진다.
* 손대지 않은 predicate의 분포가 함께 움직였는지 본다. 움직였다면 저작이 아니라 다른
  것이 바뀐 것이다.
