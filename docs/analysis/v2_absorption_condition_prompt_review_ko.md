# 검수 요청: 흡수 조건 pair 프롬프트 전문

2026-08-13. 설계는 승인됐고(카드 A/B/C + 조건문 정정) 런타임·planner는 구현·테스트 완료다.
**프롬프트는 아직 설치하지 않았다.** 이 문서가 승인되면 설치하고 pair 1건을 실행한다.

실행 규모: 요청 1회(`r12_p2_q1_da`, `concurrence-pair:0001`). ordinary predicate 증분 0.

## 1. system 프롬프트 (`prompts/v2_absorption_condition_pair.md` 예정)

```text
당신은 하나의 사건 서술을 읽고, 그 안의 두 행위 사이에 **하나의 사실 관계**가 있는지만 답한다.

입력은 다음과 같다.

- `condition_statement`: 답해야 할 관계 질문. 이것 하나만 답한다.
- `legal_standard`: 그 관계를 어떤 기준으로 보는지. 질문의 범위를 넓히거나 좁히는 데 쓰지 않고,
  무엇을 보라는 지시로만 읽는다.
- `first_conduct`, `second_conduct`: 관계의 두 끝이 되는 행위.
- `episode_text`: 두 행위가 있었던 사건 서술 전체.

다음은 판단하지 않는다: 각 행위가 죄가 되는지, 어떤 죄인지, 행위자에게 권한이나 자격이
있었는지, 고의가 있었는지, 두 행위가 법적으로 어떤 관계인지, 최종 죄책. 이 판단들은 다른
단계가 이미 하거나 앞으로 한다. 당신이 답할 것은 `condition_statement` 하나다.

출력은 셋이다.

- `pair_id`: 입력에 있는 그대로
- `truth`: TRUE | FALSE | UNKNOWN
  - TRUE    = `condition_statement`가 묻는 관계가 원문에 나타나 있다
  - FALSE   = 원문이 그 관계가 아님을 보여 준다
  - UNKNOWN = 원문만으로는 그 관계가 있는지 결정되지 않는다
- `supporting_quotes`: TRUE일 때, 그 관계를 직접 보여 주는 정확한 연속 부분문자열 1개 이상.
  `episode_text`, `first_conduct`, `second_conduct` 중 어느 하나에 그대로 존재해야 한다.
  TRUE가 아니면 빈 배열을 출력한다.

인용은 요약하거나 합성하지 않는다. `...`을 넣지 않는다. 보낸 문자열에 그대로 존재하지 않는
인용은 계약 위반이다. 원문에 없는 사실을 지어내 TRUE로 만들지 않는다.

UNKNOWN은 **사실이 원문상 결정되지 않을 때만** 쓴다. 그 관계가 법적으로 어떤 결과를 낳는지가
불확실하다는 이유로 UNKNOWN을 쓰지 않는다.

설명 없이 schema에 맞는 JSON 객체 하나만 출력한다.
```

## 2. user 프롬프트 (`prompts/v2_absorption_condition_pair_user.md` 예정)

```text
아래 INPUT_JSON의 사건 서술을 읽고 `condition_statement`가 묻는 관계 하나만 답하라.

두 행위가 각각 죄가 되는지, 행위자에게 권한이 있었는지는 판단하지 말라. 그 관계가 원문에
나타나면 TRUE, 원문이 그 관계가 아님을 보여 주면 FALSE, 원문만으로 결정되지 않으면 UNKNOWN이다.

TRUE에는 반드시 보낸 문자열의 정확한 부분문자열 인용을 붙이라.
`retry_contract_feedback`가 있으면 판단을 바꾸지 말고 지적된 계약 오류만 고쳐 전체 JSON을
다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
```

## 3. 실제로 나가는 payload 전문 (호스트가 생성한 그대로)

```json
{
  "case_id": "kcl_criminal_r12_p2_q1_da",
  "pair_id": "concurrence-pair:0001",
  "condition_statement": "첫 번째 행위와 관련하여 문제되는 인영이 두 번째 행위의 그 문서에 현출되어 그 문서의 구성부분을 이루는가.",
  "legal_standard": "그 인영이 바로 그 문서에 찍혀 그 문서의 기명·날인 부분을 이루었는지만 본다. 그 인영을 얻거나 사용할 권한이 있었는지는 여기서 판단하지 않는다. 인장 자체의 제작·보유와 해당 문서에 인영이 현출된 것은 구별한다. 원문이 인영의 현출 여부를 밝히지 않으면 제작·보유 사실만으로 현출 또는 비현출을 추론하지 않는다.",
  "actor_id": "甲",
  "factual_episode_id": "factual_episode:001",
  "episode_text": "甲은 A를 살해한 직후 병실에 보관되어 있던 A의 인감도장을 가지고 나온 다음 ‘A가 甲에게 인감증명서 발급을 위임한다’는 취지의 A명의 위임장 1장을 작성하고 같은 날 주민센터 담당 직원 C에게 제출하여 A의 인감증명서를 발급받았다.",
  "first_conduct": "甲은 A를 살해한 직후 병실에 보관되어 있던 A의 인감도장을 가지고 나온",
  "second_conduct": "‘A가 甲에게 인감증명서 발급을 위임한다’는 취지의 A명의 위임장 1장을 작성"
}
```

죄명(`offense.seal_forgery_or_misuse`, `offense.private_document_forgery`), 조문, `rule_id`,
`흡수`/`absorption`, binding id는 payload에 없다. 테스트가 이 부재를 잠근다
(`test_the_payload_carries_no_offense_or_absorption_vocabulary`).

출력 schema는 `pair_id`를 `const`로 못 박는다 -- Call 1.5-D 1차 실행 43/43 계약 실패의 원인이
자유 문자열 식별자였다.

## 4. 이 payload로 나올 답에 대한 예측 -- 미리 적어 둔다

`episode_text`는 **인감도장으로 위임장에 날인했다고 명시하지 않는다.** "인감도장을 가지고 나온"과
"A명의 위임장 1장을 작성"만 있다.

그래서 정직한 답은 UNKNOWN이거나, 인감증명서 발급 위임장이라는 문서 성격에서 날인을 읽어 낸
TRUE다. 어느 쪽이든 **최종 liability는 변하지 않는다.** 그 문항에서 두 위조죄는 모두 elements에서
멈추므로 흡수할 대상이 성립하지 않는다. 이번 실행에서 확인할 것은 live path가 구조적으로 닫히는지,
즉 pair 후보 -> 모델 -> 계약 검증 -> `condition_truths` -> `resolve_concurrence` -> 최종 책임
뷰까지 값이 한 번 흐르는지뿐이다.

**FALSE와 UNKNOWN의 하류 효과는 같다**(두 죄 유지, UNKNOWN만 unresolved에 기록). 그래서 이 구분은
감사 기록의 문제이고 결론을 흔들지 않는다. 그럼에도 프롬프트가 둘을 구분해 정의하는 이유는, 원문이
관계를 부정하는 경우와 아무 말도 하지 않는 경우가 artifact에서 구별되어야 다음 저작이 어디를 봐야
하는지 알 수 있기 때문이다.

## 5. 승인 후 실행 순서

1. 두 프롬프트 설치.
2. `srun --jobid=<vllm job>`으로 pair 1건 실행 -> `concurrence_condition_assessments.jsonl`.
3. 별도 pair carrier로 append-only 병합(키 공간은 `pair_id`, 계약은 additive delta와 동일).
4. `run_v2_scallop_e2e.py`에 조건 truth 주입 -> `resolve_concurrence` -> 최종 책임 뷰 확인.
5. audit 기록.

## 검수 카드

### 카드 D. `legal_standard`를 payload에 그대로 싣는 것이 맞는가

`legal_standard`는 "인장 자체를 별도로 제작·보유하였을 뿐 그 인영이 해당 문서에 현출되지 않았다면
해당하지 않는다"는 **음성 사례**를 포함한다. 이것이 모델에게 판단 기준을 주는 저작인지, 아니면
답을 유도하는 힌트인지가 갈릴 수 있다.

- (가) 그대로 싣는다. 음성 사례가 없으면 "인영"과 "구성부분"의 경계를 모델이 스스로 정한다. -- 권고.
- (나) 음성 사례 문장을 빼고 긍정 기준만 싣는다.

> comment: (가)의 취지를 유지하되 문구 수정. 현재 음성 사례는 법적 경계 자체는 좋지만 이 payload와
> 너무 닮아 있어서 모델이 **"현출되지 않았다고 쓰여 있지 않음"을 "현출되지 않음"으로 읽어 FALSE**로
> 밀릴 수 있다. 다음으로 바꾼다.
>
> "인장 자체의 제작·보유와 해당 문서에 인영이 현출된 것은 구별한다. 원문이 인영의 현출 여부를
> 밝히지 않으면 제작·보유 사실만으로 현출 또는 비현출을 추론하지 않는다."
>
> 이렇게 하면 법적 경계도 주고 `FALSE ≠ UNKNOWN` 계약도 같이 잠근다.
>
> 그리고 `condition_statement`의 "첫 번째 행위에서 문제된 인영"에도 미세한 presupposition이 있다.
> 첫 번째 conduct는 실제로는 "인감도장을 가지고 나온" 것뿐이므로 **"첫 번째 행위와 관련하여
> 문제되는 인영"**이 더 중립적이다.

**반영.** 두 문구 모두 그대로 저작했다(3번 payload가 수정본이다). 음성 사례를 바꾼 것이 이번
수정에서 제일 중요한 부분이다 -- 원래 문장은 **부재를 부정으로 읽는 경로**를 열어 두었고, 이
사안은 정확히 그 부재가 쟁점인 사안이라 프롬프트가 답을 미리 정할 뻔했다. 새 문장은 그 추론을
양방향으로 막는다. 비현출을 추론하지 말라는 것과 현출을 추론하지 말라는 것을 한 문장이 함께 진다.

### 카드 E. 이번 pair를 실행할 것인가, 구조만 확인하고 멈출 것인가

4번에서 적었듯 이 문항의 답은 최종 liability를 바꾸지 않는다. 실행 비용은 요청 1회로 사실상 0이고,
얻는 것은 "모델 -> 계약 -> reducer" 구간이 실제로 값을 나른다는 확인이다.

- (가) 실행한다. 계약 검증과 lowering이 live로 한 번은 통과해야 채널이 닫힌 것이다. -- 권고.
- (나) 실행하지 않고 합성 assessment로 lowering만 확인한다. 그러면 프롬프트·계약 구간은 미검증으로
      남는다.

> comment: (가) 실행. 결론을 바꾸지 않는 케이스라서 오히려 model -> contract -> condition_truths
> -> resolve_concurrence 채널이 실제로 닫혔는지 검증하기에 적합하다.

**반영.** 문구 수정 후 실행했다. 결과는 아래 6번.

---

## 6. 실행 결과 (2026-08-13)

| pair | truth | 인용 | 재시도 | 토큰 |
| --- | --- | --- | --- | --- |
| `concurrence-pair:0001` | **UNKNOWN** | 없음 | 0회 | 1,046 |

4번의 예측대로다. 그리고 **카드 D의 문구 수정이 여기서 값을 했다** -- 원래 음성 사례는 부재를
부정으로 읽어 FALSE로 밀 여지가 있었고 이 사안은 정확히 그 부재가 쟁점이었다. 바뀐 문구는 현출과
비현출 추론을 양방향으로 막았고 모델은 UNKNOWN을 냈다.

관통은 `condition_truths`가 `resolve_concurrence`에 도착하는 데까지 live로 확인됐다. 흡수 발화
자체는 발화하지 않았고 그 이유는 조건이 아니라 **두 위조죄가 모두 elements에서 멈추기 때문**이다.
즉 reducer 분기(TRUE -> 흡수)는 unit test가 지고 live 데이터가 지지 않는다. 이 구분이 출력에서
보이도록 E2E에 `concurrence_condition_truths` 블록을 추가했다(도착한 truth + 두 instance 성립
여부). 상세는 `experiments/.../absorption_e2e_v12/audit.md`.

26문항 회귀 비교: 새 필드를 제외하면 `doctrine_e2e_v11`과 bit-identical.
