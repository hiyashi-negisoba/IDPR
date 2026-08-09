# Predicate 사전 확장 — 배치 ⑥ 총칙 누범 (제35·36조) v1

[predicate_dictionary_ext_batch06_v0.md](predicate_dictionary_ext_batch06_v0.md)에 대한 사용자
검수 2건 반영. 35조의 5개 predicate·`recidivism_modify` 구조, 36조의 범위 밖 판정은
그대로 — `effect` 표기 방식과 "법정형 속성" 주장 두 곳만 고친다.

---

## 정정 1 — `punishability_note`는 존재가 확인된 필드가 아니다. `effect.note`를 쓴다

**v0 오류**: `doctrine.recidivism_modify`에 `punishability_note` 필드를 달았는데, 이건
`CompletionPolicyDef.states.*.punishability_note`에서만 확인된 필드다.
`doctrine_def.schema.json`을 직접 확인: `DoctrineDef`는 `id`/`stage`/`requires`/`effect`
**넷뿐**이고(`additionalProperties: false`), `punishability_note` 같은 필드가 없다.

**그런데 "새 필드를 만들면 안 된다"에서 한 걸음 더 정확히 갈 수 있다** —
`common.schema.json`의 `modify_effect`를 확인하니 **이미 `note` 필드가 있다**:

```text
modify_effect = {
    effect: "MODIFY",
    stage: "culpability" | "punishability",
    modifier_ref: <symbolic id, 필수>,
    note: <string, 선택 — "Free-text explanation for readers... Never consumed by
           the symbolic runtime">
}
```

즉 자유텍스트 설명은 `DoctrineDef` 레벨이 아니라 **`effect` 객체 자신의 `note`**에
넣는 게 스키마가 이미 지원하는 정확한 자리다. **v1(수정)**:

```text
doctrine.recidivism_modify
    stage = punishability
    requires = ALL(
        prior_sentence_of_imprisonment_or_greater,
        prior_sentence_still_effective,
        prior_sentence_execution_completed_or_exempted,
        subsequent_offense_within_recidivism_period
    )
    effect = {
        effect: MODIFY,
        stage: punishability,
        modifier_ref: modifier.punishability.recidivism_aggravated,  (가칭, 2패스에서
            실제 modifier 분류체계 확정 시 정함 — Open Question #4 미해결 상태이므로
            이번 배치에서 확정하지 않는다)
        note: "필요적 가중, 법정형 장기의 2배까지(특별법상 단기까지 가중되는 경우는
               별도)"
    }
```

`modifier_ref`가 가리킬 실제 modifier 분류체계(ModifierDef)는 v2.1.0 Open Question
#4로 아직 미설계 상태(`common.schema.json` 주석에 명시)라, 이번 predicate 사전
단계에서는 `modifier_ref`의 정확한 값까지 확정하지 않는다 — `note`의 존재와 위치만
정정하고, 실제 modifier id는 2패스(또는 그 설계가 닫힌 뒤)에 채운다.

---

## 정정 2 — "후범의 법정형 속성이 offense_ref에 내재한다"는 확인되지 않은 주장이었다

**v0 오류**: "'후범이 금고 이상에 해당하는 죄'는 offense_ref 자체의 법정형 속성(이미
정의에 내재)"이라고 썼는데, 직접 확인하니 근거가 없다. `offense_def.schema.json`에는
`statutory_refs`(예: `["형법 제347조 제1항"]`) 필드만 있고, 그 설명 자체가 "이 필드는
참조만 기록할 뿐 법적 효과를 갖지 않는다"고 명시한다 — 구조화된 법정형(최소/최대 형량)
메타데이터는 이 DSL 어디에도 없다. `Punishability` stage도 구체적 형량 계산기가 아니라
`punishable`/`modified`/`exempted` 같은 법적 **상태**만 다룬다.

**v1(수정)**:

```text
후범의 누범 적용대상 적격성("금고 이상에 해당하는 선고형의 죄")
    → 새 case-time predicate로 만들지 않는다(v0의 "만들지 않는다" 결론은 유지).
    → 대신: 이 doctrine(recidivism_modify)을 2패스에서 어느 offense에 저작·부착할지
      자체를 법률 기준(그 죄의 법정형이 금고 이상인지)에 따라 저작자가 제한한다 —
      즉 "판정 predicate"가 아니라 "저작 시 doctrine을 붙일지 말지의 범위 제한"으로
      처리한다.
    → 이 DSL에 실제 법정형 메타데이터가 나중에 추가되면(현재는 없음) 그때 정적
      속성으로 전환할 수 있다는 점만 기록.
```

---

## 정정 확인 — 35조/36조 나머지 판정은 그대로

```text
35조 — Punishability MODIFY로 표현 가능(architecture gap 아님), 전과 관련 사실/법적
       상태를 requires로 평가(cross-actor dependency 문제 아님) — 유지.
36조 — 현재 liability runtime(resolve_liability 파이프라인)의 대상 밖, HOLD가 아니라
       out-of-scope로 분류 — 유지. "형이 얼마인가"까지 현재 Punishability가 계산한다는
       투로 읽히지 않도록 재확인: 이 DSL의 Punishability는 구체적 형량 계산기가 아니라
       `punishable`/MODIFY(modifier_ref)/EXEMPT라는 법적 상태만 다룬다 — 36조가 그 밖의
       "구체적 형을 다시 정하는" 절차라는 배치 결론과 정확히 부합.
```

---

## 배치⑥ v1 요약 — 총칙 트랙 최종 종료

`effect.note` 자리 정정 + "법정형 속성 내재" 주장 철회(대신 저작 시 적용범위 제한으로
처리) 2건만 반영, 나머지 구조·판정은 v0 그대로. 총칙 26개 Band A-core + Band B(35-36조)
predicate 후보 제시 전체가 이걸로 끝난다.
