# Predicate 사전 초안 v2 — Gate ① 최종 (v1 피드백 3건 반영)

v1([predicate_dictionary_draft_v1.md](predicate_dictionary_draft_v1.md))에 대한 재검토
피드백([predicate_dictionary_draft_v1_feedback.md](predicate_dictionary_draft_v1_feedback.md))에서
"**Gate ①의 방향을 충족한다**"는 판정을 받았고, freeze 전 수정 3건만 남았다. v0/v1은
그대로 둔다 — 이력 추적용.

이 3건 외에는 v1을 전부 유지한다(횡령 불법영득의사/manifestation 분리, property_
disposition 공유, 권리행사 분리, result_not_occurred 삭제, commencement_of_execution
legal_element 재분류, 심신미약 임의적 감경 표현, 오상방위 HOLD, 준강도류 DerivedOffenseDef
우선 검토 — 전부 그대로).

---

## 수정 1 — CompletionPolicy: `punishable`은 state별 bool, case-time expression 아님

**v1 오류**: `IMPOSSIBLE_ATTEMPT punishable = dangerousness(...)`처럼 `punishable`
필드에 expression을 넣는 것으로 읽히게 적었다. **v2(수정)**: `punishable`은 각 state에
저작 시점에 붙는 bool이고, 사건마다 달라지는 조건(`dangerousness` 같은)은 `punishable`이
아니라 **state를 나누고 그 state의 `when`에** 둔다.

```text
offense A — 미수처벌 규정 있음
    ATTEMPTED
        punishable = true
    ABANDONED_ATTEMPT
        punishable = true
        punishability_note = "처벌되는 경우 필요적 감경 또는 면제"

offense B — 미수처벌 규정 없음
    ATTEMPTED
        punishable = false

불능미수 — 위험성은 case-time 조건이므로 state를 분리:
    IMPOSSIBLE_ATTEMPT_DANGEROUS
        when = (수단·대상 착오로 결과불가능) AND dangerousness
        punishable = true
    IMPOSSIBLE_ATTEMPT_NON_DANGEROUS
        when = (수단·대상 착오로 결과불가능) AND NOT(dangerousness)
        punishable = false
```

실제 state 명칭·분해는 각 offense 저작 시 결정한다. 제29조 반영은 필요하지만 신규
authorization predicate/gate는 만들지 않는다는 v1의 결론 자체는 유지 — `punishable`을
bool로 정확히 쓰는 것만 고쳤다.

---

## 수정 2 — 횡령: `entrustment_relationship`을 삭제하지 않고 둘 다 보존, 조합은 `ElementExpression`

**v1 오류**: `custody_of_anothers_property`가 `entrustment_relationship`을 "대체"한다고
적었다. **v2(수정)**: 둘을 성급히 동의어로 삭제하지 않고 **둘 다 보존**한다.

```text
legal_element.entrustment_relationship          (유지, 삭제 안 함)
legal_element.custody_of_anothers_property       (유지)

embezzlement.requires =
    ALL(
        custody_of_anothers_property,
        entrustment_relationship,
        ...
    )
```

`LegalElementDef` 자체에 다른 LegalElement를 `requires`시켜 작은 rule program처럼
만드는 것(`custody_of_anothers_property.requires = ...`)은 이 DSL의 composition 방식이
아니다 — 조합은 항상 offense/doctrine 쪽 `ElementExpression`에서 한다. 법률 검수 결과
`custody_of_anothers_property`의 legal_standard 안에 위탁신임관계 판단이 완전히
포함되는 것으로 확정되면 그때 하나로 합칠 수 있지만, **이번 단계에서 확정하는 건
"성급히 삭제하지 않는다"까지다.**

---

## 수정 3 — 15개 pilot predicate 전체 typing pass (`canonical_meaning` 기준)

기준: **"사건에서 관찰·추출되는 사실" → GroundFact / "그 사실을 법적 기준에 포섭한
판단" → LegalElement.** 이름이 아니라 canonical_meaning으로 재판정했다.

| id | v1 분류 | v2 분류 | 판정 근거 |
|---|---|---|---|
| `instigator_intent` | ground_fact | **legal_element** | canonical_meaning이 "교사자에게 교사의 고의가 있었다"— 그대로 "교사의 고의가 있다"류(법적 평가) 예시와 일치 |
| `aiding_intent` | ground_fact | **legal_element** | 같은 논리, "방조의 고의" |
| `valid_claim_exists` | ground_fact | **legal_element** | "유효한 채권이 존재한다"는 채권의 유효성(법적 판단)을 포섭한 명제 |
| `claim_scope` | ground_fact | **legal_element** | 권리의 범위 확정은 `valid_claim_exists`와 같은 성격의 법적 판단 |
| `infringement_situation` | ground_fact | **legal_element** | canonical_meaning이 "현재의 **부당한** 침해가 있었다"— 부당성 평가를 이미 포함 |
| `defensive_act` | ground_fact | **legal_element** | "침해를 **방위하기 위한** 행위"— 방위 목적성 평가가 canonical_meaning에 포함되어 단순 행위 관찰이 아님 |
| `voluntary_cessation_or_prevention` | ground_fact | **legal_element** | canonical_meaning의 "**자의로**" 중지가 자의성(규범적 쟁점, 26조 Ⅳ.1의 학설 대립 지점)을 포섭 — "행위자가 공격을 중단했다"류 bare fact와 다름 |
| `means_or_object_defect` | ground_fact | **ground_fact 유지** | "수단·대상의 착오"는 관찰 가능한 사실 요소가 중심 — 결과발생 불가능성이라는 평가와 혼재돼 있어 강제 이동하지 않고 2패스 실제 저작 시 다시 확인 |

**재분류 7건, 유지 1건.** 나머지(각칙 A절 전체, 총칙 `mental_disorder_at_act_time`/
`discrimination_capacity`/`control_capacity`/`taking_conduct`/`actual_acquisition`/
`instigation_conduct`/`aiding_conduct` 등)는 이번 typing pass에서 다시 봐도 canonical_
meaning이 raw fact 또는 이미 legal_element로 분류돼 있어 변경 없음.

---

## 그대로 유지(v1 확정 사항, 재론 안 함)

1. 불법영득의사/횡령 manifestation 구조 — 별도 mens rea hierarchy 없음
2. `property_disposition` 공유 + 죄별 causal structure — `disposer_identity_match`는
   2패스에서 `RelationDef` 먼저 시도, 새 role type system 없음
3. 강도·공갈 권리행사 분리(`same concept ≠ same legal effect`) — `valid_claim_exists`/
   `claim_scope`는 위 typing pass로 legal_element 확정
4. `result_not_occurred` 삭제, `commencement_of_execution` legal_element 재분류 유지
5. 심신미약 = `Culpability: MODIFY → diminished` + `punishability_note: "임의적 감경"`,
   신규 `MAY_REDUCE` 없음
6. 오상방위·오상과잉방위 HOLD — MistakeDef/variant state/신규 effect 없음, 구체 반례
   확인 시에만 architecture issue로 승격
7. 준강도류 — `DerivedOffenseDef`/`QUALIFY`/`COMPOSE` 우선 시도, `RECLASSIFY`/`REDIRECT`
   같은 신규 effect 없음
8. ALIC의 `offense_committed_in_resulting_impairment` — relational하게 "보인다"는 이유만으로
   미리 `RelationDef`로 옮기지 않는다. `LegalElementDef`로 충분한지 vs 실제 두 component
   사이 relation binding이 필요한지는 **2패스에서 직접 표현해보고 결정**(이번 게이트의
   필수 수정 아님, 확인사항으로만 이월).

---

## Gate ① 완료

세 가지 수정 전부 반영, 신규 스키마 변경 없음. `predicate-first 방식`과 `신규 DSL
primitive를 만들지 않는다`는 원칙이 15개 조문 pilot에서 실제로 지켜졌음을 이 세 라운드
(v0→v1→v2)가 실증한다.

**다음 단계**: 같은 방식(워크시트 생성 → predicate 후보 제안 → 사용자 검수 → 수정)을
승인된 최종 범위(각칙 51개 조문 + 총칙 선별 범위 전체)로 확장한다 — 계획 문서
([mossy-doodling-breeze.md](file:///home/jaehoonjeong/.claude/plans/mossy-doodling-breeze.md))의
"후속 적재 대상" 절이 그 범위를 규정한다. predicate 사전이 그 전체 범위를 커버하고
다시 한번 검수를 통과해야 2패스 조립(`data/v2/definitions/` 실제 저작)에 들어간다 —
이번 15개 pilot의 gate ① 통과가 곧 전체 트랙의 완료를 뜻하지 않는다.
