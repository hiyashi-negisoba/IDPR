# Call 3 dev 재실행 -- diagnostic checkpoint

2026-08-13. baseline `call3_dev_v1`에 대한 전후 대조다. 프롬프트 두 줄만 바꿨고
(최종 결론에서 anchored state 그대로 재진술 / 인용 verbatim), plan·서비스·temperature는 동일하다.

**이것은 N 조건 baseline이 아니다.** F2가 남아 있고 새 실패가 하나 관측됐다. diagnostic
checkpoint로만 고정한다.

## 전후

| | `call3_dev_v1` | `call3_dev_v2` |
| --- | --- | --- |
| **F3** 인용 변조 | `대법원 2018. 4. 12. 선고 2017도16488 전원합의체` | **`대법원 2018도13877 전원합의체`** -- 해소 |
| **F1** 미확정을 불성립으로 단정 | "丙 … 사기죄는 성립하지 않는다" | 단정 소멸 -- 해소 |
| **F2** 불성립을 유보로 완화 | "확정할 수 없다" | "확정할 수 없다" -- **미해소** |
| **F4** 최종 결론에서 죄 누락 | 없음 | **신규 관측** |

분량 2,146 -> 1,808 / 2,171 -> 2,111자.

## F2는 프롬프트 실패가 아니다 -- plan이 모순된 anchor를 줬다

`r10_p1_q1_ga`, 같은 사건·같은 행위자인데 predicate truth가 instance마다 다르다.

```text
ground_fact.vaginal_intercourse_conduct
  derived_offense.rape_causing_injury_by_aggravated_result -> FALSE    (gate 실패 -> "성립하지 않는다")
  offense.rape                                             -> UNKNOWN  ("확정하기 어렵다")
```

plan은 "간음이 없었으므로 강간치상죄 불성립"과 "간음 여부는 미확정"을 **동시에** 넘겼다. 모델은
이를 유보 쪽으로 조화시켰다. 간음 여부가 미확정인데 간음이 없다고 단정할 수 없으므로 법률가의
서술로는 오히려 옳다. **프롬프트를 더 조여도 잡히지 않고, 잡히면 답안이 이상해진다.**

즉 이 plan은 애초에 생성되어서는 안 됐다.

## 전수 -- 국소 사고가 아니다

`(case, actor, predicate)`가 같은데 truth가 갈리는 쌍:

- **10 / 26 문항**에서 발생
- ground fact **12쌍**, legal element **32쌍**
- TRUE vs FALSE 정면 충돌 **2건**
- 최다: `ground_fact.means_or_object_defect` 7, `ground_fact.taking_conduct` 4,
  `ground_fact.vaginal_intercourse_conduct` 1

ground fact가 갈리는 것이 특히 심각하다. GroundFact는 offense instance의 속성이 아니라
**occurrence-level의 사건 세계에 대한 사실**로 설계했는데, 같은 사실이 죄명마다 다른 값을 갖고
있다. Call 2의 atomic assessment가 다시 offense context에 오염됐다는 신호다.

**두 종류를 한 문제로 처리하지 않는다.** legal element는 offense-instance-local 평가일 수
있으므로 같은 ref라는 이유만으로 같은 truth를 요구할 수 없다.

## F4 -- 카드 1 수정의 부작용

`r14_p1_q2`의 최종 결론이 "丙의 최종 죄책은 횡령죄이다"로 끝난다. 乙 전체와 丙의 미확정 죄
2건이 결론에서 빠졌다. F1의 잘못된 단정은 사라졌지만, "각 죄의 결론을 그대로 다시 말한다"는
요구를 **누락으로 회피**했다.

원인은 plan이 결론 문장을 산문에 섞어 넘겨 모델이 취사선택할 수 있다는 것이다.

## 다음 (승인된 방향)

1. 모델 호출 없이 26개 AnswerPlan consistency audit -- GroundFact 충돌 전건의 정확한 key와
   source instance, LegalElement divergence는 semantic fingerprint 기준 분류.
2. GroundFact 충돌은 **upstream에서 canonicalize**한다. occurrence-level truth 하나만
   소비하도록 복구하며, 사후 vote/repair는 금지한다.
3. AnswerPlan에 hard guard: 같은 GroundFactKey에 다른 truth가 오면
   `CROSS_INSTANCE_GROUND_FACT_CONFLICT`로 **생성 실패**. 값을 고르지 않는다 -- FALSE 우선,
   TRUE 우선, UNKNOWN 강등, majority vote 전부 금지. 감지하고 멈추기만 한다.
   LegalElement는 `CROSS_INSTANCE_LEGAL_ELEMENT_DIVERGENCE`로 audit에만 잡고, predicate·
   legal standard·actor·episode·factual scope가 모두 같은 경우에만 hard-fail한다.
4. `required_final_conclusions` 슬롯을 `analysis` 산문과 분리해 closed list로 전달한다.
   host는 여전히 답안에 손대지 않는다 -- 결론문을 삽입하는 것이 아니라 회수해야 할 anchor를
   넘기는 것이다. 호출 뒤 누락 검사는 기계적으로 하되 수정하지 않는다.
5. AnswerPlan 26/26 재확인 -> 같은 dev 2건 재실행 -> F1/F2/F3/F4 = 0.

**26문항 Call 3 실행은 보류한다.** 지금 돌리면 이미 아는 상류 모순이 출력에 번지는 양상만
측정하게 되어 N 조건 산출물로서 의미가 없다.
