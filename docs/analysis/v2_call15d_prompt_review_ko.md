# 검수 요청: Call 1.5-D 프롬프트 전문

2026-08-13. **아직 설치하지도, 실행하지도 않았다.** 승인 후에만 `prompts/`에 넣고 43회 실행한다.
설계는 [v2_call15d_doctrine_activation_design_ko.md](v2_call15d_doctrine_activation_design_ko.md),
반영된 cue 카탈로그는 `data/v2/doctrine_raising_cues.yaml`(v2, 14개)이다.

## 이 프롬프트가 지켜야 하는 것

- doctrine id, 조문, 법리 이름("정당방위", "심신장애")이 입력에도 지시문에도 없다.
- cue의 `scope`도 넣지 않는다. 어떤 단서가 사건 전체에 미치는지는 법적 효과 범위의 문제이고
  모델은 그 문장이 원문에 있는지만 답한다.
- 단서 부재는 부정이 아니라 미제기다. FALSE를 "그 법리 없음"으로 쓰지 않는다.
- TRUE에는 반드시 episode 본문의 exact substring 인용과 주체 표지가 붙는다.

---

## 시스템 프롬프트 (`prompts/v2_call15d_doctrine_cue.md` 예정)

```text
당신은 한 factual episode를 읽고, 주어진 사실 단서 문장이 그 원문에 적혀 있는지만 답하는
Call 1.5-D다. 법적 판단을 하지 않는다.

입력은 factual episode 하나와 `cues` 배열이다. 각 cue의 `factual_cue`는 "원문에 이런 사실이
적혀 있는가"라는 사실 질문이다. 그 사실이 어떤 법적 의미를 가지는지, 어떤 항변이 되는지,
어떤 죄가 성립하는지는 판단하지 않는다.

`cues`에 있는 모든 cue를 입력에 나온 순서 그대로 정확히 한 번씩 답한다. 빠뜨리거나 추가하거나
순서를 바꾸지 않는다. 각 cue마다 다음 넷을 출력한다.

- `cue_id`: 입력에 있는 그대로
- `truth`: TRUE | FALSE | UNKNOWN
  - TRUE  = 그 사실이 episode_text에 적혀 있다
  - FALSE = 그 사실이 적혀 있지 않다
  - UNKNOWN = 적혀 있는지 원문만으로 판단할 수 없다
- `subject_actor_ids`: 그 사실이 누구에 관한 것인지. `actor_labels`에 있는 표지만 사용한다.
  단서 문장이 "행위자"를 가리키면 그 사실의 주체가 된 사람을, 피해자의 승낙처럼 상대방의
  행동을 말하면 그 행동으로 자기 행위가 영향받는 사람을 넣는다. TRUE인데 누구에 관한 것인지
  원문에서 특정할 수 없으면 빈 배열을 출력한다.
- `source_quote`: TRUE일 때 그 사실을 직접 보여 주는 episode_text의 정확한 연속 부분문자열.
  TRUE가 아니면 빈 문자열을 출력한다.

`source_quote`는 요약하거나 합성하지 않는다. `...`을 넣지 않는다. episode_text에 그대로
존재하지 않는 문자열은 계약 위반이다. 원문에 없는 사실을 추론해 TRUE로 만들지 않는다.

FALSE는 "그런 사정이 없었다"는 판단이 아니라 "이 episode 원문에 그렇게 적혀 있지 않다"는
관찰이다. 확신이 서지 않으면 TRUE로 밀지 말고 UNKNOWN을 쓴다.

다음은 판단하거나 출력하지 않는다: 죄명, 조문, 구성요건, 위법성, 책임, 항변의 성부, 고의,
과실, 정당한 이유, 상당성, 위법성조각사유나 책임조각사유의 이름, 최종 죄책.

설명 없이 schema에 맞는 JSON 객체 하나만 출력한다.
```

## 사용자 템플릿 (`prompts/v2_call15d_doctrine_cue_user.md` 예정)

```text
아래 INPUT_JSON의 factual episode 하나만 읽고, `cues`의 각 사실 단서가 그 원문에 적혀 있는지
답하라.

법적 평가를 하지 말고, 적혀 있지 않으면 FALSE, 원문만으로 판단할 수 없으면 UNKNOWN을 쓰라.
TRUE에는 반드시 episode_text의 정확한 부분문자열 인용과 주체 표지를 붙이라.
`retry_contract_feedback`가 있으면 의미를 확장하지 말고 지적된 cue 집합, exact quote, actor
표지 오류만 고쳐 전체 JSON을 다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
```

## 실제로 나갈 입력 예시

`kcl_criminal_r11_p1_q1` `factual_episode:002`의 실제 payload 형태다(cue 14개 중 2개만 표시).

```json
{
  "case_id": "kcl_criminal_r11_p1_q1",
  "factual_episode_id": "factual_episode:002",
  "episode_text": "(2) 乙은 A의 집 주변을 사전 답사하면서 집 안을 엿보던 중 A가 현관문 옆 화분 아래에 비상용 열쇠를 둔다는 사실을 알게 되었고, 경제적으로 어려움을 겪는 후배 丙에게 범행을 함께할 것을 제안하여, 丙의 승낙을 받고 丙과 역할 분담을 공모하였는데, 甲에게는 범행을 丙과 함께 할 예정이라고 알리지 않았다.",
  "actor_labels": ["乙", "A", "丙", "甲"],
  "cues": [
    {"cue_id": "cue.actor_age_stated",
     "factual_cue": "행위자의 나이 또는 출생 시점이 사건 사실에 적혀 있다"},
    {"cue_id": "cue.victim_permission_stated",
     "factual_cue": "피해자가 그 행위를 허락하거나 동의하였다는 사실이 적혀 있다"}
  ]
}
```

이 예시는 `victim_permission_stated`의 위험을 그대로 보여 준다. 원문에 "丙의 승낙을 받고"가
있지만 그 승낙은 **피해자의 승낙이 아니라 공범의 승낙**이다. cue 문장이 "피해자가"로 시작하므로
FALSE가 옳고, 모델이 "승낙" 낱말만 보고 TRUE를 내면 실행 결과에서 그것이 드러난다
(`subject_actor_ids`와 인용이 함께 남으므로 사후 감사로 잡을 수 있다).

## 카드 F. 위 문구를 승인하는가

특히 보실 것:

1. **`subject_actor_ids` 지시문.** "행위자"와 "상대방"을 구분해 설명했지만, 피해자 승낙처럼
   문장의 문법적 주어와 doctrine이 붙는 사람이 다른 cue에서 모델이 헷갈릴 수 있다. 지금
   문구는 "그 행동으로 자기 행위가 영향받는 사람"으로 유도한다. 더 좁히려면 cue마다 주체를
   저작해 두는 방법이 있으나(예: `subject_role: actor | counterpart`), 그러면 카탈로그가
   커진다.
2. **UNKNOWN 사용 지침.** "확신이 서지 않으면 TRUE로 밀지 말고 UNKNOWN"으로 두었다. 이것은
   miss를 늘리고 false raise를 줄이는 쪽이다. 반대 균형을 원하시면 알려 주십시오.
3. **금지 목록에 법리 이름을 열거한 것.** "위법성조각사유나 책임조각사유의 이름"이라고만
   적고 개별 법리명(정당방위 등)은 쓰지 않았다. 열거하면 오히려 그 단어를 주입하게 된다.

> comment:

---

## 다음 단계 (승인 후)

1. `prompts/v2_call15d_doctrine_cue.md` / `_user.md` 설치.
2. `scripts/run_v2_call15_doctrine_cues.py` 작성 -- 기존 Call 1.5-P 러너와 같은 구조
   (episode 단위, contract retry, `--prompt-approved` 게이트).
3. 43회 실행 -> raised set과 exact 증분 target 목록·수 보고.
4. `Δtarget ≤ 300`이면 audit 후 Call 2 증분 실행, 초과하면 cue별 발화 수를 먼저 재검수.
