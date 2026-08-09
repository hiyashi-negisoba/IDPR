# Predicate 사전 확장 — 배치 ⑨ 생명·신체 (제250·254·255·257·259·263·267·268·258의2조) v1

[predicate_dictionary_ext_batch09_v0.md](predicate_dictionary_ext_batch09_v0.md)에 대한
사용자 검수 7건 반영. v0의 표 구조·나머지 조문은 특별히 언급하지 않는 한 그대로 유지 —
아래는 정정 사항만 다룬다.

---

## 정정 1 — 인과관계: COMPOSE는 `relation.causal_nexus`, base OffenseDef는 여전히
legal_element leaf(스키마 확인 결과) — 다만 death_causation을 조문마다 새로 만들지 않는다

**v0 오류**: `legal_element.death_causation`(fixture)을 250·259·267·268이 공유
재사용할 후보로 두고 "검수 필요"로만 남겼는데, 사용자 지적대로 Step5 이후
`relation.causal_nexus`가 conduct→result 인과관계의 first-class 판정이라는 점을
반영하지 않았다.

**스키마 확인(v1에서 직접 검증)**: `offense_def.schema.json`의 top-level 필드는
`id/identity/elements/element_modules/exports/qualifiers/participation_constraints`
뿐이고 **`relations` 필드 자체가 없다**. `elements.causation`은 `element_expression`
(leaf는 `ground_fact`/`legal_element`만, `common.schema.json` `element_ref_expr` +
axis 1 참조검사 관행)이라 `relation.causal_nexus`를 직접 참조할 수 없다.
`derived_offense_def.schema.json`은 `derivation`(COMPOSE + relations가 실제로 사는 곳,
robbery_causing_injury/robbery_homicide fixture의 `{relation: relation.causal_nexus,
left: ..., right: ...}` 패턴)만 있고 base `offense_def`엔 대응 필드가 없다.

**v1(수정) — 두 층으로 나눠 확정**:

```text
COMPOSE(파생 offense, 두 event/offense 컴포넌트를 잇는 인과관계)
    → relation.causal_nexus 확정
    → 259(base=offense.injury + 가중결과=death_of_victim)가 이 경우 — v0가 이미
      맞게 썼다(robbery_causing_injury와 동일 패턴), 재확인만.

base OffenseDef 자신의 elements.causation slot(단일 offense 내부 conduct→result)
    → 구조적으로 legal_element leaf가 필요(relation 직접 참조 불가)
    → 250·267·268이 여기 해당. 다만 사용자가 지적한 진짜 문제(조문마다 별도
      canonical_meaning의 causation predicate를 새로 만드는 중복)는 유효하다 —
      **death_causation을 250 전용으로 가두지 않고, 267·268도 같은 predicate를
      재사용한다**(canonical_meaning이 "행위와 결과 사이 상당인과관계"로 이미
      conduct-neutral하므로 250의 "살해행위" 한정 서술을 걷어내고 재사용 가능한지
      2패스에서 확정).
```

**`aggravated_result_attribution`의 legal_standard("결과에 대한 예견가능성과
상당인과관계")가 `causal_nexus`와 실질적으로 중복되는지는 primitive 차원의 확인
사항으로 남긴다** — 이 배치가 결정할 사안이 아니라 그 primitive를 다루는 별도 결정
지점의 일(24조 canonical_meaning 수정 금지 원칙과 같은 이유로, 이번 배치에서 손대지
않는다).

---

## 정정 2 — 255: `preparatory_conduct`/`conspiracy_agreement`는 `legal_element`,
`ground_fact`가 아니다 — typing 오류 복원

**v0 오류**: 배치④(v0/v1/v2 전부)가 이미 `legal_element.preparatory_conduct`/
`legal_element.conspiracy_agreement`로 확정해뒀는데, 이번 v0가 `ground_fact.*`로
잘못 적었다.

**v1(수정)**: 255절 표를 `legal_element.preparatory_conduct`/`legal_element.
conspiracy_agreement`로 되돌린다 — canonical_meaning·근거는 v0 그대로, kind만 정정.

---

## 정정 3 — 255: 예비죄의 종범 불성립을 32조 legal_standard로 "흡수"하면 안 된다 —
2패스 compatibility 확인사항으로 복원

**v0 오류**: "예비의 방조 불인정(판례)은 32조 종범 predicate의 legal_standard에
'예비죄에는 적용되지 않는다'는 한계로 흡수 — 신규 없음"이라고 썼는데, 이건 배치④가
v1에서 이미 명시적으로 거부한 해법이다. 배치④ v0는 처음에 "그 offense/state에
`aider` mode를 아예 저작하지 않으면 된다"고 썼다가, v1에서 스스로 정정했다 —
`ParticipationPolicyDef`는 **offense 단위**로 mode를 저작하지 Completion state별로
켜고 끄는 구조가 아니라서, 같은 offense가 `ATTEMPTED`에서는 방조 가능하고
`PREPARATION_OR_CONSPIRACY`에서는 불가능해야 하는 요구를 "mode를 안 붙인다"로
표현할 수 없다(붙이면 전체 state에서 방조가 가능해지고, 안 붙이면 기수·미수에서도
막힌다). legal_standard 텍스트로 흡수하는 것도 같은 문제다 — 텍스트 서술이 실제
runtime 가용성을 바꾸지 못한다.

**v1(수정)** — 배치④ v1의 표현을 그대로 가져온다:

```text
예비죄 종범 불성립(판례 확립)
    → Completion state별로 participation mode 가용성이 달라져야 하는 요구인데,
      현재 6C 구조(offense 단위 ParticipationPolicyDef)가 이를 자연히 지원하는지
      확정되지 않았다 — 2패스에서 실제 예비·음모 처벌 죄(살인예비 포함)를 저작하며
      확인한다. 표현 불가로 판정되면 architecture-compatibility issue로 승격
      (33/34/35-36/19조-263조 특례와 같은 그룹).
```

이 항목은 predicate 사전으로 닫히지 않는다 — 문서 하단 "HOLD/architecture-
compatibility 종합" 목록에 4번째 항목으로 추가한다(아래 정정 요약 참고).

---

## 정정 4 — 268: `negligence_bundle` 정의 자체를 건드리지 않는다 — offense-level
`ALL`로 병렬 결합

**v0 오류**: "`ANY(occupational_duty_of_care, gross_negligence)`를 `negligence_
bundle`에 추가 요건으로 얹는다"고 썼는데, 이렇게 읽히면 공유 `ElementBundleDef` 자체의
`requires`를 268에 맞게 수정하는 것처럼 보인다 — `negligence_bundle`은 14조가 확정한
전역 공유 정의라 offense별로 변형하면 안 된다(불변성 원칙, 배치⑧이 이미 확정한 원칙과
동일).

**v1(수정)**:

```text
offense.negligent_homicide_by_occupation(가칭, 268)의 elements.mental(또는 해당 slot) =
    ALL(
        {element_modules: bundle.negligence_bundle}    -- 4요소 그대로, 수정 없음
        ANY(occupational_duty_of_care, gross_negligence)
    )
```

`negligence_bundle`은 `element_modules`로 placement되고, 268 고유 가중요건은
offense-level expression에서 **병렬로** 결합한다 — bundle 정의 자체는 그대로 둔 채
267(가중요건 없음)과 268(가중요건 있음)이 같은 bundle을 서로 다른 조합으로
재사용하는 구조.

---

## 정정 5 — 268: `gross_negligence` canonical_meaning이 bundle과 중복된다 — 좁힌다

**v0 오류**: `legal_element.gross_negligence`의 canonical_meaning에 "조금만 주의를
기울였다면 결과 발생을 쉽게 예견·회피할 수 있었음에도"라고 써서 `negligence_bundle`의
`foreseeability`/`avoidability`를 다시 서술했다.

**v1(수정)**:

```text
legal_element.gross_negligence
    주의의무 위반의 정도가 현저하다
    (예견가능성·회피가능성 자체는 negligence_bundle의 foreseeability/avoidability가
    이미 담당 — 이 predicate는 그 위반의 "정도"만 판단한다)
```

---

## 정정 6 — 268: "반의사불벌 아님" HOLD 삭제 — 특별한 처벌조건이 없다는 뜻일 뿐

**v0 오류**: art268_sec1_1.non_punishable_against_victim_intent를 "이 DSL의 어느 축에
대응하는지 미확인"이라며 HOLD로 남겼는데, 이 카드의 실제 의미는 "268에는 반의사불벌
같은 특별한 처벌조건이 **없다**"는 것뿐이다 — 부재를 표현하려고 스키마에 새 필드를
찾을 필요가 없다.

**v1(수정)**: predicate 불필요, Punishability 조건 없음, 스키마 확인도 불필요.
authoring 메모로만 남긴다 — "268은 처벌조건부(반의사불벌) offense가 아니다"라는
확인 사실이지, 표현할 대상이 있는 미해결 항목이 아니다. HOLD 목록에서 제거.

---

## 정정 7 — fixture predicate("(예시)")를 real typing 근거로 그대로 쓰지 않는다 —
250·257 conduct/result 재검토

**v0 오류**: `ground_fact.killing_conduct`/`ground_fact.violence_used`/`ground_fact.
injury_occurred`를 "fixture에 있으니 그대로 재사용"이라고 전제했는데, 그 fixture는
Step 6B/6C가 스키마·컴파일러를 검증하려고 만든 "(예시)" 플레이스홀더이지 실제 250·257
저작 결과가 아니다 — 이름이 같다고 typing까지 자동으로 맞는 게 아니다.

**v1(재검토 결과)**:

```text
ground_fact.death_of_victim         유지(ground_fact) — 사망은 생물학적 사실 관찰,
                                     규범적 다툼이 크지 않음(사람의 시기는 별도
                                     natural_person_victim_status가 이미 흡수)

ground_fact.killing_conduct         유지(ground_fact) — "행위를 하였다"는 관찰
                                     사실(이 프로젝트 관행상 conduct slot은 대체로
                                     ground_fact — property_taking/appropriation_
                                     conduct/forcible_intercourse와 동일 패턴)

ground_fact.injury_occurred         legal_element로 재분류
                                     — art257 원문(Ⅰ.3)이 "찰과상 인정 여부",
                                     "히스테리증 인정", "모발절단은 상해 아님" 등
                                     방대한 경계사례를 다루는 것 자체가, "관찰된
                                     신체 변화가 '상해'라는 법적 기준을 충족하는가"
                                     라는 포섭판단이라는 뜻 — 배치②가 세운 typing
                                     기준("사실 관찰" vs "법적 기준 포섭")을 그대로
                                     적용하면 legal_element다.
                                     → legal_element.injury_result(가칭)로 재명명,
                                     2패스에서 확정

ground_fact.violence_used           결정하지 않음(v0 검수 필요 2 유지) — "폭행"에
                                     한정된 이름을 억지로 넓히지 않고, 실제
                                     injury conduct를 표현할 별도 predicate가
                                     필요한지 2패스에서 결정
```

`injury_occurred`가 legal_element로 바뀌면 259(COMPOSE의 가중결과 slot)·263(상해
결과 요건)·268(ANY 결과 slot)도 전부 이 재분류를 따라간다 — 별도 표기 없이 이 문서
전체에서 `legal_element.injury_occurred`(재명명 전 임시로는 기존 이름 유지, 2패스에서
`injury_result`로 개명) 참조로 갱신된 것으로 본다.

---

## 정정 8 — 250: 공동정범 ATTRIBUTE와 고의를 동일시하지 않는다 — mental state는
actor-specific

**v0 오류**: "강도살인 공동정범에 살인 부분 고의의 공동까지 필요하다는 카드가 6C
ATTRIBUTE 계약과 정확히 일치한다"고 썼는데, 서술이 잘못됐다 — `fold_any`로 상대방의
predicate truth를 병합하는 ATTRIBUTE는 **conduct 귀속**에 쓰는 것이지, 고의 같은
actor-specific mental state를 병합하는 데 쓰면 안 된다. A에게 살인의 고의가 TRUE이고
B에게 FALSE일 때 `fold_any`를 적용해 B의 고의를 TRUE로 만드는 것은 164 배치⑧이 이미
정리한 원칙(공동정범의 결과 예견가능성은 "각자 자기 case truths로 평가"하지 전이
대상이 아님)을 정면으로 어긴다.

**v1(수정)**:

```text
공동정범 conduct(실행행위 분담)   → ATTRIBUTE 대상(slot-scoped, fold_any) 가능
각 행위자의 intent/예견가능성     → ATTRIBUTE 대상 아님, 각자 자기 CaseTruths로
                                    개별 평가(164 배치⑧·259 상해치사 공동정범과
                                    동일 원칙)
```

"강도살인 공동정범엔 살인 부분 고의의 공동이 필요하다"는 카드는 바로 이 원칙의
확인 사례다 — 강도의 conduct는 ATTRIBUTE로 공유되더라도, 살인의 intent는 각
공동정범이 개별적으로 갖춰야 한다는 뜻이지 ATTRIBUTE가 mental slot까지 다룬다는
뜻이 아니다.

---

## 정정 9(사소) — 258의2 범위 밖 설명에서 `punishability_note` 표현 삭제

**v0 오류**: 상습범·누범 가중을 "Punishability MODIFY, `punishability_note` 자유텍스트로
흡수"라고 썼는데, `punishability_note`는 CompletionPolicy state 전용 필드(11조
필요적 감경 표기 등)이고, DoctrineDef MODIFY effect의 자유텍스트는 35조 누범이 이미
확정한 `modify_effect.note`다 — 두 필드를 혼동했다.

**v1(수정)**: 258의2의 상습범·누범 가중은 애초에 이번 배치 범위 밖이므로 구체적 필드명
언급 자체를 삭제한다 — "Punishability MODIFY 후보, 구조화된 법정형 메타데이터는 이
DSL 범위 밖(배치⑥ 원칙)"까지만 남기고 필드명은 실제로 35조·258의2를 함께 저작할 때
정한다.

---

## HOLD/architecture-compatibility 종합 — v1 갱신

v0의 3항목(art263↔19조, art257↔34조, art250↔33조 단서)에 **4번째 항목을 추가**한다
(정정 3):

4. **art255 예비죄 종범 불성립 ↔ 6C `ParticipationPolicyDef`가 offense 단위인 것과의
   불일치**(위 정정 3) — 배치④가 이미 이월해둔 항목의 재확인, 2패스에서 살인예비를
   실제로 저작하며 표현 가능 여부를 확인한다.

---

## 배치⑨ v1 요약

인과관계는 COMPOSE(259)=`relation.causal_nexus`/base offense(250·267·268)=legal_element
leaf(구조상 불가피, 스키마 확인 완료)로 확정하되 후자는 조문마다 새로 만들지 않고
재사용을 원칙으로 한다(정정 1). 255의 typing 오류(정정 2)와 종범 호환성 오도(정정 3)를
복원했다. 268의 negligence_bundle 불변성(정정 4)·gross_negligence 중복 제거(정정 5)·
반의사불벌 HOLD 해제(정정 6)를 반영했다. fixture predicate 3개 중 `injury_occurred`를
legal_element로 재분류했고 `violence_used`는 여전히 결정하지 않는다(정정 7). 250의
ATTRIBUTE 서술을 conduct 전용으로 정정했다(정정 8). 신규 스키마·DSL primitive는
여전히 없음 — 이번 정정 전부 기존 primitive의 올바른 적용 문제였다.
