# N configuration freeze

2026-08-13. commit `e7b61119d324bdba42bf70689126da2153c63245`.

N은 **카드 회수 없이** 상징층 산출만으로 답안을 쓰는 조건이다. P는 여기에
`ANSWERPLAN_SPEC` 5.5의 카드 회수를 더한 조건이고, 논문이 보고하는 rule-base 기여도는 P−N이다.
그러므로 N이 흔들리면 그 차이가 무엇의 차이인지 말할 수 없다. 이 문서가 N의 정본이다.

동결한다는 것은 **아래 지문을 바꾸지 않은 채로 26문항을 실행한다**는 뜻이다. 프롬프트, plan,
상류 artifact 중 하나라도 바뀌면 그 실행은 N이 아니라 새 조건이며, 이 문서를 갱신하고
dev 2건 검증을 다시 통과해야 한다.

## 동결 대상

| 단계 | 정본 | sha256 (앞 16자) |
| --- | --- | --- |
| Call 1.5 binding | `.../issue_bindings.jsonl` | `5d3ca5296cf04a9d` |
| planner | `.../call15d_v4/evaluation_instance_plan.jsonl` | `1a10c5dd1bac2145` |
| 참가 병합 plan | `.../final_responsibility_v10/participation_plan.jsonl` | `2fc38a4aa1afdc42` |
| Call 2 | `.../call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl` | `8ff234e12d432f3a` |
| E2E / 최종책임 | `.../final_responsibility_v13_gf_rebase/results.jsonl` | `59578f9a6b35ba9c` |
| AnswerPlan | `.../answer_plan_v3_case_truths/answer_plans.jsonl` | `d573d6d9fb39553b` |
| Call 3 system | `prompts/v2_call3_irac.md` | `2c53770081f3df35` |
| Call 3 user | `prompts/v2_call3_irac_user.md` | `ed444401b5606c52` |

경로 접두사는 전부 `experiments/v2_call15_directscope_26_causal/`다.

생성 파라미터: 서비스 222907, `idpr-gemma-4-26b-a4b`, 문항당 1회, `max_tokens 8192`,
`temperature 0.7`, 후처리 없음.

AnswerPlan 규모: 26문항 / anchored issue 105 / required conclusion 105 / analysis 69,943자.

## 이 조건이 통과한 것 -- dev 2건 (`call3_dev_v4`)

| | 결과 |
| --- | --- |
| F1 미확정을 불성립으로 단정 | 0 |
| F2 불성립을 유보로 완화 | 0 |
| F3 인용 변조 | **판정으로 통과** (아래) |
| F4 결론에서 죄 누락 | 0 |
| `missing_required_final_conclusions` | `[]` (10/10) |
| 내부 식별자 누출 | 0 |
| cross-instance GroundFact conflict | 0 (26문항 전수) |

### F3 판정 -- 기록

v4 답안은 plan이 준 `대법원 2018도13877 전원합의체`를
`대법원 전원합의체 판결(2018도13877)`로 **어순을 바꿔** 썼다. 프롬프트 문언이
"그 문자열을 있는 그대로 옮긴다"이므로 **문언 그대로는 위반이다.**

검수 판정은 통과다. 인용의 법적 기능은 어느 판결인지 특정하는 것이고 사건번호
`2018도13877`은 정확히 보존됐다. F3이 원래 이름 붙인 해악 -- 번호가 `2017도16488`이라는 다른
사건으로 바뀌고 없는 선고일자가 붙는 것 -- 은 발생하지 않았다. 어순까지 강제하면 답안 문체를
데이터 형식에 종속시키는 정도가 카드 2에서 감수하기로 한 선을 넘는다.

**따라서 N에서 `verbatim`은 문자열 동일성이 아니라 식별정보 보존을 뜻한다.** 사건번호가
바뀌거나 주어지지 않은 판례에 번호가 붙으면 여전히 실패다. 이 판정은 P에도 그대로 적용한다 --
두 조건이 다른 자로 재면 P−N이 인용 규칙의 차이를 섞어 담는다.

`call3_dev_v3`는 문자열까지 그대로 지켰고 프롬프트가 동일하므로, 이 차이는 회귀가 아니라
`temperature 0.7` 표집 변동이다.

## 이 데이터셋에서 검증할 수 없는 것

- **흡수 pair 0건.** 26문항 전체에 없다. "흡수된 죄를 명시적으로 논하라"는 계약은 unit test가
  지고 논문에는 `live-unverified / unit-tested`로 적는다. synthetic live case는 만들지 않는다.
- **participation은 4문항**(`r10_p1_q3_ga`, `r11_p1_q1`, `r12_p1_q4`, `r14_p1_q1`)이고 전부
  sealed다. 사람이 답안을 읽으면 오염이므로 26문항 run에 자동 fidelity check로만 붙인다.

## 동결하지 않은 것

- **카드 회수(SPEC 5.5).** 이것이 P와 N을 가르는 축이므로 N에는 붙이지 않는다. N 답안의 근거가
  빈약한 것은 결함이 아니라 조건의 정의다.
- **26문항 Call 3 실행 자체.** 아직 하지 않았다. 위 지문 그대로 실행하는 것이 다음 단계다.
