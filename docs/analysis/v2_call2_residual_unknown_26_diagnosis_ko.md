# Call 2 residual UNKNOWN 232개 진단

2026-08-14. guard-aware scheduling 정본
`call2_guard_sched_26_v2`의 assessment 452개 중 UNKNOWN 232개만 다시 진단했다. 목표는 UNKNOWN을
줄이는 것이 아니라 다음 원인을 분리하는 것이다.

- A: occurrence가 잘못 붙음
- B: occurrence는 맞지만 evidence window가 좁음
- C: evidence는 충분하지만 지나치게 literal한 판정
- D: 실제 법적 불확실성

## 실험 계약

동일한 232 exact target을 같은 모델·프롬프트·스키마·question assumptions로 세 번 평가했다.
달라진 것은 `evidence_occurrence.source_text`뿐이다.

1. `occurrence_span`: production과 같은 binding span
2. `factual_episode`: Call 1.5가 기록한 동일 factual episode의 source span
3. `full_case_text`: 사실관계 전문

정본 artifact:

- `diagnostics/residual_unknown_evidence_scope_26_v1.json`
- `diagnostics/residual_unknown_review_26_v1.{json,md}`
- plan sha: `a025da3aa22764bef9ab6033a6afdd94568c8b61ee98c3c8d4f1cc855fbc4122`
- Call 2 sha: `3d002f3b53388cef4771d53b3d1c563039ba433a6869c150d8cb6db6ff1982c6`
- 3-arm 사용량: 441,248 tokens
- 검증: `332 passed, 16 skipped`, focused Ruff, `git diff --check` 통과

## 먼저 분리해야 하는 재호출 drift

232개는 정본에서 전부 UNKNOWN이지만 occurrence span을 그대로 재생했을 때 206 UNKNOWN / 21 TRUE /
5 FALSE였다. **26개(11.2%)가 evidence 변경 없이 움직였다.** 따라서 정본 truth와 새 arm을 직접
빼서 evidence 효과라고 부를 수 없다. evidence 효과는 같은 진단 실행 안의 paired arm끼리만 본다.

## operational bucket

| bucket | 수 | 비중 | 관찰 |
| --- | ---: | ---: | --- |
| B episode-scope confirmed | **44** | 19.0% | occurrence U -> episode/full 동일 known |
| A 또는 case-context 검토 | **50** | 21.6% | occurrence/episode U -> full known |
| C 또는 D 지속 UNKNOWN 검토 | **93** | 40.1% | 세 arm 모두 U |
| unstable/drift | **45** | 19.4% | 비단조 전이·재호출 변동 |

이는 아직 A/B/C/D의 최종 숫자가 아니다. **B 44만 evidence-scope 효과로 강하게 확인**된다. full
case에서만 풀린 50개에는 occurrence 오배치, 정당한 case context, 다른 행위자 사실의 오귀속이
섞여 있다. 세 arm 모두 UNKNOWN인 93개에도 C와 D가 섞여 있다.

## B -- factual episode가 실제로 복구한 것

occurrence -> episode paired transition은 다음과 같다.

- UNKNOWN -> TRUE 55, UNKNOWN -> FALSE 8
- TRUE -> TRUE 19, FALSE -> FALSE 3
- TRUE/FALSE -> UNKNOWN 4
- **TRUE <-> FALSE 직접 역전 0**

그중 full case에서도 같은 known 값을 유지한 44개만 B-confirmed로 보수적으로 잡았다. 예:

- `r10_p1_q1_ga` 강간: `vaginal_intercourse_conduct` UNKNOWN -> FALSE -> FALSE
- `r10_p1_q3_ga`, `r11_p2_q1_ga` 수뢰: 공무원성·직무관련성 UNKNOWN -> TRUE -> TRUE
- `r13_p1_q1` 빈 금고: `means_or_object_defect` UNKNOWN -> TRUE -> TRUE,
  `taking_conduct` UNKNOWN -> FALSE -> FALSE
- `r13_p1_q1` 주거침입: 관리 주거 객체와 침입이 episode에서 TRUE로 해소

이는 occurrence의 actor-action 조각만으로는 그 법적 predicate가 필요로 하는 같은 사건의 context가
잘린다는 실측이다. 다만 44개를 보고 production evidence를 즉시 episode 전체로 바꾸지는 않는다.
episode 안에도 여러 actor/action이 있을 수 있으므로 A 검토와 함께 attribution 안전성을 봐야 한다.

## A -- full case는 오배치 탐지기이지 해결책이 아니다

명확한 occurrence 오배치 사례가 다시 보였다.

- `r11_p1_q1` 乙 robbery의 `taking_conduct`는 폭행 occurrence에 붙었다. full case가 다른 절취
  사실을 읽고 TRUE로 바꾼다.
- `r13_p1_q1` 丙 theft의 `taking_conduct`는 문을 열고 망을 본 occurrence에 붙었다. 실제 금고를
  연 actor는 甲이다.
- 같은 문항의 乙 theft `taking_conduct`는 범행 제안·정보 제공 occurrence에 붙었다. 실행행위
  occurrence가 아니다.
- `r13_p2_q1` 乙 theft `taking_conduct`는 길을 묻는 distraction occurrence에 붙었는데, full
  case는 甲의 지갑 절취를 끌어와 乙 target도 TRUE로 만든다. 이것은 **복구가 아니라 오귀속**이다.

따라서 `occurrence/episode U -> full known` 50개를 evidence 부족 50개로 세면 안 된다. 이 bucket은
A와 case-global B를 사람이 분리할 review queue다.

full case arm 자체도 production 대안이 아니다. episode -> full에서 TRUE -> UNKNOWN 19,
FALSE -> UNKNOWN 6, **FALSE -> TRUE 1**이 생겼다. 넓은 문맥이 정보를 늘리면서 attribution을
망가뜨린다는 과거 진단을 residual subset에서도 재현했다.

## C와 D -- UNKNOWN 지속성으로 구별할 수 없다

세 arm 모두 UNKNOWN인 93개에는 `possession` 9, `bribe_promise` 7, `dangerousness` 7,
`means_or_object_defect` 5, `intent` 4 등이 있다. 여기에는 다음이 함께 있다.

- 명시 사실에서 통상적으로 포섭할 수 있는데 prompt의 “보충 금지”를 지나치게 literal하게 읽는 C
- 잘못된 actor/occurrence에 물어 evidence를 아무리 넓혀도 안전하게 답할 수 없는 A
- 학설·판례 대립을 AnswerPlan이 쟁점으로 올려야 하는 D

더 중요한 반례는 `r12_p2_q1_ga` 사자의 점유다. 정본에서 `possession=UNKNOWN`이었고 법적으로
D가 맞지만, 이번 재생은 occurrence/episode/full 모두 TRUE였다. 즉 **D는 persistent UNKNOWN으로
검출되지 않는다.** 모델이 우연히 단정하면 진짜 논점이 사라져 버린다.

D는 Call 2 truth와 독립된 authored dispute/rubric bridge로 검출하고, AnswerPlan에서
`미확정`이 아니라 견해 대립으로 렌더링해야 한다. C는 A/B를 제거한 뒤 남은 명시사실 포섭 실패를
별도 검수해야 한다. 활성 프롬프트 문언 변경은 그 뒤의 승인 게이트다.

## 현재 결론

1. guard-aware scheduling 트랙은 닫힌다.
2. full-case evidence 전면 교체는 다시 기각한다.
3. same factual episode는 B 44개를 안정적으로 복구한 유력한 evidence carrier지만 attribution
   검증 전 production 채택하지 않는다.
4. A는 target placement/actor attribution 문제이며 evidence 확대와 분리해 고친다.
5. D는 UNKNOWN 값이 아니라 authored legal-dispute route로 승격한다.
6. 기존 N/P는 계속 동결하며 final Call 2 뒤 한 번만 재생성한다.

## 다음 작업

검수 packet의 50개 `A_OR_CASE_CONTEXT_REVIEW`와 93개 `C_OR_D_PERSISTENT_REVIEW`를 먼저
target-placement 관점에서 줄인다. 특히 ground fact는 actor-action episode에, legal element는
그 offense realization에 붙어 있는지 확인한다. 그 뒤 남은 명시사실 포섭 실패만 C prompt-policy
후보로 올리고, rubric이 요구하는 견해 대립은 D dispute registry/AnswerPlan 트랙으로 분리한다.

후속 provenance 감사 결과는
`docs/analysis/v2_call2_target_placement_audit_ko.md`에 기록했다. 50+93의 143개 중 actor-bound
GroundFact는 25개였고 나머지 118개는 realization-scope predicate였다. B-confirmed 44개도
same-predicate 다른-actor collision 기준으로 32개 무충돌 / 12개 검수 필요로 갈렸다.
