# Call 3 dev 재실행 -- v4, case_truths 권위 전환 후

2026-08-13. `call3_dev_v3`에 대한 전후 대조다. 프롬프트는 바뀌지 않았고(fingerprint 동일),
바뀐 것은 **AnswerPlan이 findings를 읽는 출처**다 -- `assessments`(한 run의 원출력)에서
`case_truths`(심볼릭 층이 실제로 소비한 정본)로 전환했다.

plan 정본은 `answer_plan_v3_case_truths/answer_plans.jsonl`이다.

## 결과

| | `call3_dev_v3` | `call3_dev_v4` |
| --- | --- | --- |
| **F1** 미확정을 불성립으로 단정 | 0 | **0** |
| **F2** 불성립을 유보로 완화 | 0 | **0** |
| **F3** 인용 변조 | 0 | **판단 필요 -- 아래** |
| **F4** 결론에서 죄 누락 | 0 | **0** |
| `missing_required_final_conclusions` | `[]` (10/10) | **`[]` (10/10)** |
| 내부 식별자 누출 | 0 | **0** |

분량 1,934 -> 1,996 / 1,963 -> 1,974자. 후처리 0.

## F3 -- 사건번호는 지켰고 표기 순서는 바꿨다

```text
plan   : 대법원 2018도13877 전원합의체
v3 답안: 대법원 2018도13877 전원합의체          -- 문자열 그대로
v4 답안: 대법원 전원합의체 판결(2018도13877)     -- 순서 재배열
```

**F3이 이름 붙였던 해악은 발생하지 않았다.** v1의 실패는 사건번호가 `2017도16488`이라는 다른
번호로 바뀐 것이었다. v4 답안에 등장하는 사건번호는 `2018도13877` 하나뿐이고, 선고일자를
덧붙이지도 않았다.

다만 프롬프트 문언은 "그 문자열을 있는 그대로 옮긴다"이고 v4는 어순을 바꿨으므로 **문언
그대로는 지키지 않았다.** v3는 지켰다. 프롬프트가 같으므로 이것은 회귀가 아니라
temperature 0.7 표집 변동이다.

N 동결 전에 판정이 필요하다 -- `verbatim`을 문자열 동일성으로 볼 것인가, 식별정보 보존으로
볼 것인가. 후자면 F3 = 0이고, 전자면 이 run은 F3에서 실패다.

## 48건 -- handoff universe 진입 확인

`case_truths`에만 있던 48건 중:

| | 건수 | 처리 |
| --- | --- | --- |
| 성립 판단이 있는 instance에 귀속 | **30** | plan에 도달 |
| 참가 후보(`participation_binding:*`, 링크 미성립) | **18** | issue universe 밖 유지 |
| 귀속돼야 하는데 누락 | **0** | -- |

issue 승격은 일어나지 않았다. anchored issue 수와 required conclusion 수가 26문항 전부
`answer_plan_v2`와 **동일**하다(총 issue 105). doctrine leaf는 `방위행위`, `침해상황`,
`상당성`, `위법성 불인식`, `불인식에 정당한 이유` 등이 0문항 -> 1~2문항으로 처음 등장한다.
analysis 분량 66,795 -> 69,943자.

## 이번 라운드에서 고친 audit 결함

첫 실행에서 `total_missing = 3`이 나왔으나 **답안이 아니라 검사 도구의 오탐이었다.**
`r14_p1_q2`가 결론 제목을 `IV. 결론`으로 썼는데(v3는 `III. 최종 결론`) 마커 목록이 "최종 결론"
같은 완성 제목만 알고 있어 매칭에 실패했고, 마지막 문단으로 폴백해 丙 블록을 통째로 놓쳤다.

키워드(`결론`/`최종 죄책`/`죄수`) + 제목 판별(문장 종결로 끝나지 않는 줄)로 바꿨다. 제목 형태
4종과 "키워드를 포함한 결론 문장은 제목이 아니다"를 회귀 테스트로 고정했다. 수정 후
v3/v4 양쪽 모두 `total_missing = 0`이다.

이 결함은 **완성된 답안을 미완성으로 보고하는** 방향이었다. 반대 방향(누락을 놓치는)이 아니어서
v3의 판정은 영향받지 않았고, 재검사에서도 0이 유지됐다.

## 재현

```text
Call 2      call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl
E2E         final_responsibility_v13_gf_rebase/results.jsonl
AnswerPlan  answer_plan_v3_case_truths/answer_plans.jsonl
Call 3      서비스 222907, 문항당 1회, max_tokens 8192, temperature 0.7
프롬프트     v2_call3_irac 2c53770081f3df35, v2_call3_irac_user ed444401b5606c52 (v3와 동일)
```
