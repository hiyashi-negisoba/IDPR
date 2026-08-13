# Call 3 dev 재실행 -- v3, F1~F4 전부 해소

2026-08-13. `call3_dev_v2`에 대한 전후 대조다. 이번에는 **프롬프트만 바꾼 것이 아니라 상류
truth가 바뀌었다** -- occurrence-level GroundFact canonicalization(`d910532`)과 그에 따른
canonical rebase(`29fb82b`)가 plan의 anchor 자체를 고쳤다.

## 전후

| | `call3_dev_v1` | `call3_dev_v2` | `call3_dev_v3` |
| --- | --- | --- | --- |
| **F1** 미확정을 불성립으로 단정 | 발생 | 해소 | **해소 유지** |
| **F2** 불성립을 유보로 완화 | 발생 | 미해소 | **해소** |
| **F3** 인용 변조 | 발생 | 해소 | **해소 유지** |
| **F4** 결론에서 죄 누락 | 없음 | 신규 발생 | **해소** |
| `missing_required_final_conclusions` | -- | -- | **`[]` (10/10)** |

분량 1,808 -> 1,934 / 2,111 -> 1,963자. 내부 식별자 누출 0. 후처리 0.

## F2는 프롬프트가 아니라 anchor가 고쳐져서 해소됐다

`call3_dev_v2`의 진단이 맞았다. plan이 `강간치상죄 = 성립하지 않는다`와 `간음 여부 = 미확정`을
동시에 넘겼고, 모델은 유보 쪽으로 조화시켰다. 그것이 F2로 기록됐지만 **법률가의 서술로는 모델이
옳았다.**

canonicalization 이후 `ground_fact.vaginal_intercourse_conduct`가 두 instance에서 UNKNOWN 하나로
수렴했고, elements gate가 `fails` -> `unresolved`로 바뀌었다. 그래서 plan의 anchor가
`주어진 사실만으로는 성부를 확정하기 어렵다`가 됐고, 답안이 그것을 그대로 재진술했다.

```text
call3_dev_v2:  anchor="성립하지 않는다"  답안="확정할 수 없다"   -> F2 (답안이 옳았다)
call3_dev_v3:  anchor="확정하기 어렵다"  답안="확정하기 어렵다"  -> 일치
```

**모델 행동이 바뀌어서 해소된 것이 아니다.** 같은 답을 계속 쓰고 있고, plan이 그것과 어긋나지
않게 됐다. 프롬프트를 더 조여 F2를 "잡았다면" 오히려 틀린 답안을 강제했을 것이다.

## F4 -- closed list가 누락을 막았다

`r14_p1_q2`에서 v2는 결론이 "丙의 최종 죄책은 횡령죄이다" 한 줄로 끝나 乙 전체가 빠졌다.
v3는 6개 anchor를 전부 재진술한다.

```text
1. 丙의 죄책: 사기죄는 ... 확정하기 어려우며(기수), 증뢰물전달죄 또한 ... 어렵다(기수).
   다만, 횡령죄는 기수에 이른 것으로 성립한다.
2. 乙의 죄책: 사기죄, 뇌물공여죄, 횡령죄 모두 ... 확정하기 어렵다(각 기수).
```

문장 구성은 모델이 정했다 -- 행위자별로 묶고 세 죄를 한 문장에 담았다. host는 무엇을 말할지만
정했고 어떻게 말할지는 정하지 않았다는 것이 이 출력에서 확인된다.

## F3 -- verbatim 유지

plan이 준 문자열은 `대법원 2018도13877 전원합의체` 하나이고 답안도 그대로 옮겼다. 선고일자
보완도, 사건번호 변경도 없다. 별도로 "대법원 전원합의체는 ...라고 판시하여"처럼 번호 없이 법리를
서술한 대목이 있는데, 이는 사건번호를 지어내지 않은 정상 서술이다.

## 본문과 결론의 일관성

F1/F2가 원래 **본문은 맞는데 결론에서 이탈**하거나 그 반대인 실패였으므로 둘을 따로 봤다.
`r10_p1_q1_ga`에서 본문은 "주어진 사실만으로는 강간치상죄의 성부를 확정하기 어렵다"로 끝나고
결론도 같다. 네 죄 전부 본문 결론과 최종 결론이 같은 상태어를 쓴다.

## 기계 검사

`scripts/audit_v2_call3_conclusion_completeness.py`. 최종 결론 구간만 잘라(`extract_final_
conclusion_section`) anchor의 행위자·죄명이 그 구간에 있는지만 센다. 상태가 맞는지는 보지 않고
답안을 고치지도 않는다.

```text
cases 2 / total_required 10 / total_missing 0 / cases_with_missing 0
```

**답안 전체를 봤다면 이 검사는 F4도 통과시켰을 것이다** -- v2에서 누락된 乙은 본문에서 길게
논의됐기 때문이다. 구간을 자르는 것이 이 검사의 전부다.

## 이번 run으로 검증되지 않은 것

- 흡수 pair: 26문항 전체에서 0건. dev 2건에도 없다. 계약은 unit test가 진다.
- participation: dev 2건에 없다. 4문항 전부 sealed이므로 26문항 run의 자동 fidelity check로 본다.
- 카드 회수(SPEC 5.5)는 여전히 붙이지 않았다. 근거 빈약은 이 run의 결함이 아니다.

## 재현

```text
Call 2      call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl
E2E         final_responsibility_v13_gf_rebase/results.jsonl
AnswerPlan  answer_plan_v2_gf_rebase/answer_plans.jsonl
Call 3      서비스 222907, 문항당 1회, max_tokens 8192, temperature 0.7
프롬프트     v2_call3_irac 2c53770081f3df35, v2_call3_irac_user ed444401b5606c52
```
