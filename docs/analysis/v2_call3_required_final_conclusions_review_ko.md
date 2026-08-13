# 검수 요청: `required_final_conclusions` closed list 도입

2026-08-13. 후속 순서 3번(`docs/handoff/NEXT_SESSION.md` "2026-08-13 (5)" 절). 목적은 F4
(`r14_p1_q2`, 乙 전체가 최종 결론 문단에서 통째로 누락된 사례) 재발 방지다.

**프롬프트는 아직 고치지 않았다.** host 쪽(`answer_plan.py`, `build_v2_answer_plan.py`,
`run_v2_call3.py`)은 이미 구현·테스트했고, 이 문서가 승인되면 프롬프트 두 파일만 설치한다.

## 배경 -- F4가 드러낸 것

F1/F2 수정(최종 결론 문단에서도 `analysis`가 준 상태를 그대로 재진술하라는 지시 추가) 이후
재실행에서 새로 나타난 실패다. 지시가 "각 죄의 결론을 그대로 다시 말한다"였는데, 결론 문장이
`analysis` 산문 안에 섞여 있어 모델이 **어떤 죄를 언급할지 스스로 골랐다** -- 잘못 말한 게
아니라 아예 빠뜨렸다. 지금 있는 지시는 "말할 때 정확히 말하라"고만 하지 "무엇을 말해야
하는지"를 닫힌 목록으로 주지 않는다.

## 이미 구현한 것 (host, 프롬프트 아님)

- `AnswerPlan.required_final_conclusions`: `anchored_issues` 하나당 정확히 하나씩,
  `(actor, offense_label, state, completion_state?, participation_mode?)`. `state`는
  `analysis` 본문과 동일한 `_STATE_PROSE` 어휘를 그대로 재사용한다 -- 앵커와 본문이 서로 다른
  말로 갈라지면 이 목록이 막으려는 drift를 다른 자리로 옮기는 것일 뿐이기 때문이다.
- `serialize_required_final_conclusions`: `· 행위자 — 죄명: 상태 (기수여부) [가담형태]` 한 줄씩.
  기존 lock(`assert_no_internal_markers`, `assert_no_rubric_fields`)을 그대로 통과해야 한다.
- `missing_required_final_conclusions(answer_text, plan)`: **최종 결론 구간만** 대상으로
  행위자·죄명 문자열이 둘 다 등장하는지 보는 기계적 presence 검사. **상태가 맞는지는 보지
  않는다** -- 그건 fidelity 계약(F1/F2)의 몫이고, 이 함수는 "결론 문단에서 언급했는가"만 본다.
  답안을 고치지 않는다. 오프라인 audit 전용.
- `extract_final_conclusion_section`: 위 검사가 볼 구간을 기계적으로 자른다. 검수 지적대로
  답안 **전체**를 보면 F4를 놓친다 -- F4는 본문에서 이미 논한 죄를 결론 문단에서만 빠뜨린
  실패였으므로, 전체 검사는 본문 언급만으로 통과시킨다. 절 제목 줄을 기준으로 자르며, 마침표로
  끝나지 않는 줄만 제목으로 본다("최종 죄책"이 결론 **문장** 안에도 나오기 때문에 마지막 문자열
  일치로 자르면 그 위 행위자들이 거짓 누락으로 보고된다). 제목이 없으면 마지막 문단.
- `build_v2_answer_plan.py`: 출력 JSONL에 `required_final_conclusions`(직렬화 문자열)과
  `required_final_conclusion_count` 추가.
- `run_v2_call3.py`: `{{REQUIRED_FINAL_CONCLUSIONS}}` 치환과 경계 lock 재검사 추가. 프롬프트가
  아직 이 플레이스홀더를 갖지 않으므로 지금은 no-op이고, 하위호환이다.
- 유닛 테스트 6개(`test_answer_plan_required_conclusions.py`), 전체 스위트 305 passed / 16
  skipped, 회귀 없음.

### 검수 결과 반영 (2026-08-13)

카드 1·2 모두 승인. 지적된 두 가지를 고쳤다.

1. 입력 설명이 실제 payload와 달랐다("행위자, 죄명, 그 결론 상태만 준다"). 직렬화에 기수
   여부·가담 형태가 들어가므로 문언을 payload에 맞게 수정했다. 아래 카드 1 수정안이 정본이다.
2. `missing_required_conclusions`가 답안 전체를 보고 있어 **F4를 검출하지 못했다.** 최종 결론
   구간만 보도록 고치고 이름도 `missing_required_final_conclusions`로 바꿨다. 구간 자르기를
   구현하며 실제 버그도 하나 잡았다 -- 마지막 문자열 일치로 자르면 "丙의 최종 죄책은
   횡령죄이다" 문장 중간에서 잘려 丙이 거짓 누락으로 보고된다. 제목 줄 기준으로 바꿨고 그
   회귀 테스트를 넣었다.

## 카드 1 -- 시스템 프롬프트에 새 입력과 지시 추가

### 현재 (`prompts/v2_call3_irac.md` 3~9행, 입력 목록)

```text
입력은 다음과 같다.

- `case_text`: 사건 원문 전문
- `question`: 이 답안이 답해야 할 문제
- `analysis`: 이 사건에 대해 이미 확정된 법적 분석
- `open_points`: 위 분석이 다루지 않은 영역
```

### 수정안

```text
입력은 다음과 같다.

- `case_text`: 사건 원문 전문
- `question`: 이 답안이 답해야 할 문제
- `analysis`: 이 사건에 대해 이미 확정된 법적 분석
- `open_points`: 위 분석이 다루지 않은 영역
- `required_final_conclusions`: 답안 끝 결론 문단이 반드시 언급해야 할 항목의 닫힌 목록.
  각 항목에는 행위자, 죄명, 결론 상태와 필요한 경우 기수 여부·가담 형태가 주어진다.
  이 목록은 결론의 의미적 앵커만 정하며, 실제 문장은 당신이 쓴다.
```

### 현재 (38~41행, "답안이 갖춰야 할 것" 마지막 항목)

```text
- 답안 끝에서 각 행위자의 최종 죄책과 죄수관계를 정리한다. 이때 각 죄의 결론은 `analysis`가
  준 상태를 그대로 다시 말한다. 성립한 죄는 성립한다고, 성립하지 않는 죄는 성립하지 않는다고,
  확정하기 어려운 죄는 확정하기 어렵다고 쓴다. 본문에서 유보한 것을 결론에서 단정하거나,
  본문에서 단정한 것을 결론에서 유보로 물리지 않는다.
```

### 수정안

```text
- 답안 끝에서 각 행위자의 최종 죄책과 죄수관계를 정리한다. `required_final_conclusions`는
  이 결론 문단이 빠뜨려서는 안 되는 항목의 닫힌 목록이다 -- 목록에 있는 행위자·죄명을 하나도
  빠뜨리지 않고 모두 언급한다. 각 죄의 결론 상태는 그 목록이 준 것을 그대로 다시 말한다.
  성립한 죄는 성립한다고, 성립하지 않는 죄는 성립하지 않는다고, 확정하기 어려운 죄는
  확정하기 어렵다고 쓴다. 본문에서 유보한 것을 결론에서 단정하거나, 본문에서 단정한 것을
  결론에서 유보로 물리지 않는다. 문장을 어떻게 구성하고 몇 개 죄를 한 문장에 묶을지는
  당신이 정한다 -- 목록은 무엇을 말해야 하는지를 정할 뿐 어떻게 말할지는 정하지 않는다.
```

### 판단이 필요한 지점

"하나도 빠뜨리지 않고"라는 강한 표현이 과잉 지시인가. F4가 정확히 누락 실패였으므로 완곡한
표현("가능한 한 모두" 등)은 재발 위험이 있다고 본다. **강한 표현 쪽을 권한다.**

> comment:

---

## 카드 2 -- 사용자 프롬프트 템플릿에 새 태그 추가

### 현재 (`prompts/v2_call3_irac_user.md` 전문)

```text
아래 사건에 대한 형사법 답안을 작성하라.

<CASE>
{{CASE_TEXT}}
</CASE>

<QUESTION>
{{QUESTION}}
</QUESTION>

<ANALYSIS>
{{ANALYSIS}}
</ANALYSIS>

<OPEN_POINTS>
{{OPEN_POINTS}}
</OPEN_POINTS>

`ANALYSIS`의 결론은 확정된 것이다. 그 결론을 전제로, 법리를 세우고 사실을 포섭하여 하나의
완성된 답안을 쓰라. 성립하지 않는 죄와 흡수되는 죄도 그 이유와 함께 다루라.
답안 본문만 출력하고 다른 말을 덧붙이지 말라.
```

### 수정안

```text
아래 사건에 대한 형사법 답안을 작성하라.

<CASE>
{{CASE_TEXT}}
</CASE>

<QUESTION>
{{QUESTION}}
</QUESTION>

<ANALYSIS>
{{ANALYSIS}}
</ANALYSIS>

<OPEN_POINTS>
{{OPEN_POINTS}}
</OPEN_POINTS>

<REQUIRED_FINAL_CONCLUSIONS>
{{REQUIRED_FINAL_CONCLUSIONS}}
</REQUIRED_FINAL_CONCLUSIONS>

`ANALYSIS`의 결론은 확정된 것이다. 그 결론을 전제로, 법리를 세우고 사실을 포섭하여 하나의
완성된 답안을 쓰라. 성립하지 않는 죄와 흡수되는 죄도 그 이유와 함께 다루라.
`REQUIRED_FINAL_CONCLUSIONS`에 있는 항목은 답안 끝 결론 문단에서 하나도 빠뜨리지 말라.
답안 본문만 출력하고 다른 말을 덧붙이지 말라.
```

### 판단이 필요한 지점

없음 -- 카드 1과 같은 결정을 따라가는 기계적 반영이다.

> comment:

---

## 실행 계획

1. 승인 → 위 두 파일 설치.
2. **같은 dev 2건** 재실행(`call3_dev_v3`). 같은 서비스·같은 plan(단, `answer_plans.jsonl`을
   `required_final_conclusions` 필드 포함해 재생성해야 한다 -- 현재 git에 있는 `answer_plan_v1`은
   이 필드가 없다).
3. F1/F2/F3 + F4(결론 누락) = 0 확인. `missing_required_conclusions`로 기계적 사후 검사도 함께
   돌려 기록한다(수정하지 않음).
4. 전부 0이면 N 조건 동결. 그 전까지는 동결하지 않는다.

## 이번 카드가 다루지 않는 것

F2의 근본 원인(occurrence-level GroundFact 모순)은 이미 별도 커밋(`d910532`,
`7976aa7`)으로 처리했다. 이 카드가 승인되고 재실행해도 F2가 실제로 사라지는지는 아직
**라이브로 검증하지 않았다** -- 그 확인은 카드 승인 후 26/26 replan + dev 2건 재실행에서
처음 이루어진다.
