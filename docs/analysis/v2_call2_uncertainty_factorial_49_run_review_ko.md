# Call 2 UNKNOWN 49-target prompt × evidence 2×2 진단

2026-08-14. "초literal prompt"와 "한 문장 evidence"를 별개 추측으로 두지 않고 같은 target
universe에서 2×2로 분리했다. production prompt와 production Call 2는 변경하지 않았다.

## 실험 계약

target은 두 집합의 합집합 49개다.

- `C_OVERLITERAL` 17: 원문에 필요한 사실이 있다고 검수한 C_HIGH 10 + C_PROBABLE 7
- `B_SAFE_EPISODE` 32: occurrence UNKNOWN -> episode/full 동일 known이며, 같은 predicate를
  소비하는 다른 actor binding이 없는 B-confirmed subset

네 arm은 exact target, evidence group, batching, schema, model, temperature를 공유한다.

| arm | prompt | B evidence | C evidence |
| --- | --- | --- | --- |
| current occurrence | 현행 | occurrence | occurrence |
| candidate occurrence | 초literal 수정안 | occurrence | occurrence |
| current mixed | 현행 | factual episode | occurrence |
| candidate mixed | 초literal 수정안 | factual episode | occurrence |

정본:

- review: `diagnostics/uncertainty_policy_factorial_49_v1.json`
- raw run: `diagnostics/uncertainty_policy_factorial_49_run_v1.json`
- analysis: `diagnostics/uncertainty_policy_factorial_49_analysis_v1.json`
- review sha: `30d56079976fcdfd7da917342d217493b55f01853ce8ee35645101654bf516bd`
- raw sha: `270a5faf558fc24079b30f03a1fbd581c7bf2e13406ecffa8466c338ad95f179`
- analysis sha: `f1060b410624a961ac6e96714a022a97d3527822878cd2ea218380b0aed28765`
- model: `idpr-gemma-4-26b-a4b`, temperature 0
- 사용량: 193,758 tokens

## 결론 1 -- 초literal prompt 수정안은 기각

C 17개에서 intended-direction agreement는 다음과 같다.

| | 현행 prompt | candidate prompt |
| --- | ---: | ---: |
| occurrence evidence | **1/17** | **1/17** |
| mixed evidence | **1/17** | **2/17** |

occurrence evidence에서는 17개 truth가 candidate 문언으로 **하나도 바뀌지 않았다**. 즉
"법적 결론어가 없어도 통상적 포섭을 하라"는 일반 지시만으로 모델의 UNKNOWN policy가 움직이지
않는다.

부작용도 있다.

- occurrence에서 `RU-088 quid_pro_quo`가 TRUE -> UNKNOWN으로 후퇴했다.
- mixed evidence에서 `RU-093 solicitation_received`가 TRUE -> FALSE로 직접 역전했다.

candidate mixed는 B agreement를 25 -> 26으로 하나 늘리지만 TRUE -> FALSE 오류 한 건을 같이
만든다. 이 trade는 받을 이유가 없다. `prompts/candidates/v2_call2_grounding_overliteral_v1.md`는
재현용 rejected candidate로만 보존하고 production prompt에 설치하지 않는다.

## 결론 2 -- 두 번째 큰 문제의 본체는 evidence packaging

현행 prompt에서 B_SAFE 32개를 occurrence -> factual episode로 바꾼 결과:

- 검수한 known 값과 일치: **25/32 (78.1%)**
- 반대 known 값: **0**
- 여전히 UNKNOWN: 7

UNKNOWN -> known은 TRUE 14 / FALSE 1이다. occurrence 재호출에서 이미 known이던 값까지 포함하면
25개가 과거 episode/full의 동일 known 값과 다시 일치했다. 이는 한 번의 stochastic gain이 아니다.
앞선 진단의 episode arm과 full-case arm이 같은 값을 냈고, 이번 독립 current-mixed arm도 같은
값을 재현했다.

대표 복구:

- 군수·경찰관 등 공무원성, 뇌물 대가관계
- 위조 목적·권한 없는 위조
- 상해 고의
- 제3자 점유 또는 권리의 객체
- 빈 금고의 수단·대상 결함

따라서 dead branch 79 다음의 큰 UNKNOWN 원인은 "모델에게 offense-level predicate를
actor-action 한 문장만 주고 판단시킨 것"이다. prompt의 어조보다 carrier가 지배적이다.

## downstream 실측

현행 prompt + safe episode에서 새로 known이 된 25개만 link counterfactual 기준선에 채웠다.
나머지 truth는 그대로다.

- symbolic output 변화: **8문항**
- final responsibility 변화: **3문항**
  - `r12_p2_q1_da`: 사인등의위조·부정사용죄 final instance 추가
  - `r13_p1_q1`: 甲 상해죄 final instance 추가
  - `r13_p2_q1`: 甲 상해죄 final instance 추가
- AnswerPlan analysis 변화: **8문항**
- required-final conclusion 변화: **4문항**
  - `r10_p1_q3_ga`
  - `r10_p2_q2`
  - `r12_p2_q1_da`
  - `r13_p2_q1`

즉 evidence carrier는 UNKNOWN 숫자만 줄인 것이 아니라 실제 최종 책임과 답안 결론을 움직였다.
이는 지금까지의 Call 2 품질 수정 중 guard-aware scheduling 다음으로 큰 downstream 효과다.

## 아직 production에 바로 넣지 않는 이유

B 32는 결과를 본 뒤 고른 benchmark-specific whitelist다. 이를 그대로 production rule로 쓰면
안 된다. 또한 `r13_p1_q1`에서는 새 `means_or_object_defect=TRUE`와 형제 instance의 기존 UNKNOWN이
GroundFact conflict를 만들어 AnswerPlan이 계속 실패한다. 같은 actor의 direct/derived projection도
함께 정규화해야 한다.

다음 production 설계는 "모든 legal element에 episode 전문"이 아니다.

1. actor-bound GroundFact는 local/exact source 유지
2. offense-level LegalElement와 non-actor GroundFact는 actor-aware realization evidence 사용
3. 다른 actor의 action fragment는 기본 제외하고 필요한 관계만 typed context로 제공
4. 동일 realization의 direct/derived GroundFact는 한 번 평가해 projection하여 conflict 방지
5. 이 구조 규칙을 232 residual 전체 paired arm에서 검증한 뒤 final Call 2에 채택

현재 판단은 **candidate prompt 기각 / actor-aware realization carrier 트랙 승인**이다. N/P는 계속
동결한다.

> 2026-08-14 후속 정정: B packet에는 원문·rubric과 불일치하는 counterfactual label이 최소
> 2개(`RU-049`, `RU-093`) 있었다. 따라서 이 문서의 25/32 agreement는 packet 재현값이지
> 법적 정확도 수치가 아니다. 32-target whitelist와 그 counterfactual downstream 수치는
> production 채택 근거로 사용하지 않는다. 구조적 결론—한 문장 carrier가 부족하고 full-case
> 확대는 위험하다는 점—만 유지한다.
# 후속 인간 검수 확정

`RU-097 unlawful_appropriation_intent`는 검수 packet의 TRUE를 유지한다. 처분권자의 동의가
있다고 착오한 경우에도 경제적 이용·처분 의사 자체는 TRUE이며, 착오의 법적 효과는 기존
mistake/doctrine route에서 별도로 처리한다. 이 구별을 Definition Layer의
`semantic_exclusions`로 고정했다.
