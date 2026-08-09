# Predicate 사전 확장 — 배치 ⑤ 총칙 공범과 신분·간접정범 (제33·34조) v1

[predicate_dictionary_ext_batch05_v0.md](predicate_dictionary_ext_batch05_v0.md)에 대한 사용자
검수 6건 반영. v0의 결론이 전반적으로 과하게 확정돼 있었다 — 33조 공동정범과 34조
전체를 "이미 지원됨/확정된 gap"으로 너무 빨리 못박았다. v1은 결론을 낮추고, 코드를
다시 읽어 실제로 확인 가능한 것과 아닌 것을 구분한다.

---

## 정정 1 — 33조 본문 공동정범: `attributable_slots`로 신분 predicate를 넘기면 안 된다

**v0 오류**: "신분 predicate를 `attributable_slots`에 넣으면 `fold_any`로 비신분자에게도
TRUE가 전이돼 해결된다"고 적었다. 이건 **법률효과(비신분자를 신분범의 공동정범으로
처벌한다)를 사실 predicate의 진실값 변경(비신분자가 공무원이 된다)으로 표현**한
것이다 — 33조가 "비신분자도 공무원이 된다"고 말하는 게 아닌데 그렇게 구현하면 semantic
contamination이다. `apply_attribution`의 `fold_any`는 공동정범 사이에 **귀속 가능한
행위요소**(누구든 그 slot의 실행에 기여하면 충족)를 공유하는 메커니즘이지, **행위자
고유의 신분** 자체를 참가자 사이에 전이시키는 용도가 아니다.

**v1(수정)**:

```text
33조 본문 교사·방조
    principal_realization_truth(principal)에 의존하는 기존 derivative 경로가 이미
    지원할 가능성이 높다(v0의 이 부분 결론은 유지) — 정범이 신분범을 실현했다는
    사실 하나만 확인하고, 비신분자 교사·방조자의 파생책임은 신분을 재검토하지 않는
    구조이기 때문.

33조 본문 공동정범
    "attributable_slots로 해결됐다"는 v0의 결론을 철회한다 — 2패스 compatibility
    확인 대상으로 낮춘다. 실제로 필요한 건 신분 predicate의 진실값 전이가 아니라
    "그 offense가 신분범임에도 비신분자가 공동정범이 될 수 있다"는 법률효과 자체를
    표현하는 다른 메커니즘(예: `ATTRIBUTE`와 무관하게 Elements 단계에서 신분
    predicate를 아예 요구하지 않는 별도 slot 구성, 또는 DerivedOffenseDef 수준의
    처리)인데, 이게 기존 구조로 되는지 확인이 안 됐다.
```

**"의무범은 attributable_slots에서 빼면 자동 해결된다"도 같은 이유로 철회.** 방금 부정한
메커니즘(신분 predicate를 attributable_slots로 다루는 것) 위에 세워진 결론이라 함께
무너진다 — 의무범(비신분자 공동정범 불성립)도 공동정범 자체가 2패스 compatibility
확인 대상이 된 이상 별도로 미리 답할 수 없다. **자수범** 부분(mode 자체를 저작하지
않는 패턴)은 이 문제와 무관하므로 그대로 유지.

---

## 정정 2 — 33조 단서: "architecture-compatibility"는 맞되, 확인할 구체적 질문을 명시

**v1(수정 방향은 v0과 동일, 확인 항목을 구체화)**: 직접 코드를 다시 읽었다 —
`resolve_derivative_liability(registry, policy, mode, principal, instance, active, truths)`에서
`principal`(정범의 `LiabilityEvaluation`, 자체 `.instance`를 가짐)과 `instance`(accessory
자신이 평가받을 `OffenseInstanceKey`)는 **파라미터상 서로 독립**이다 — 함수 어디에도
`principal.instance.offense_ref == instance`의 offense_ref를 강제하는 코드가 없다.
`_resolve_derivative_elements`는 `principal_realization_truth(principal)`(정범 쪽)과
`mode_payload["requires"]`를 **accessory 자신의** predicate view(`truths.predicate_view
(instance)`)로 평가한 것을 `AND`할 뿐이고, 그 뒤 `pipeline.resolve_from_elements(...,
instance, ...)`도 `instance` 하나만 갖고 Unlawfulness부터 진행한다 — `principal`을
다시 참조하지 않는다.

**즉 코드상으로는 accessory가 정범과 다른 offense/DerivedOffenseDef(존속살해)에
대해 평가되는 것을 막는 장치가 안 보인다** — 다만 이걸 실제로 그렇게 호출하는
caller(step 7/8 orchestrator)가 아직 없으므로, "가능해 보인다"이지 "확인됐다"는 아니다.

```text
확인할 구체적 질문(2패스 또는 Step 7에서):
  principal = 보통살인으로 평가된 어머니의 LiabilityEvaluation
  instance  = 존속살해(DerivedOffenseDef)로 평가될 아들의 교사자 instance
  이 조합으로 resolve_derivative_liability(mode="instigator", principal=..., instance=...)를
  실제로 호출했을 때, 아들의 존속살해교사 파생책임이 의미대로 산출되는가?
```

**architecture-compatibility 분류 유지, 결론은 "gap"도 "이미 지원"도 아니고 순수
확인 대상.**

---

## 정정 3·4 — 34조: "confirmed gap" 판정 철회, `OffenseRealization`은 Culpability 이전에 결정된다

**v0 오류**: "피이용자가 책임무능력 등으로 처벌되지 않으면 `principal_realization_truth`가
FALSE"라고 썼는데 틀렸다. `stages.py`를 확인: `OffenseRealization`은 **"Elements
satisfied AND Unlawfulness preserved"**로 정의되고 Culpability는 그 다음 단계다.
즉 피이용자가 **Elements 충족 + Unlawfulness 유지 + Culpability만 조각(책임무능력 등)**된
경우, `principal.realization is not None` → TRUE다. "34조는 항상 피이용자 실패 →
이용자 성공의 역방향 구조"라는 v0의 단정은 틀렸다 — 피이용자 실패의 **원인**에 따라
다르다:

```text
피이용자가 책임무능력/책임조각(형사미성년자·심신상실·강요된행위 등)
    Elements+Unlawfulness는 유지 → realization = TRUE
    → 기존 instigator/aider derivative 경로가 이미 도달 가능할 수 있다(제한적
      종속형식과 일치하는 방향). 34조 문언상으로는 이 경우도 "간접정범"(정범의
      예)으로 분류하지만, 처벌 결과("교사의 예" → 정범과 동일한 형)가 기존 경로의
      결과와 실질적으로 같을 가능성이 있다 — 2패스에서 실제로 겹치는지 확인 대상.

피이용자에게 고의/목적/신분이 결여(구성요건 자체 불충족)
    Elements 자체가 fail → realization = None, principal_realization_truth = FALSE
    → 기존 instigator/aider 경로는 이 경우 도달 불가(FALSE가 AND로 전체를 막는다).
      34조가 실제로 필요한 지점은 여기다.

피이용자에게 위법성조각사유(정당방위 등)
    Unlawfulness gate가 fails → realization = None → FALSE
    → 위와 같은 이유로 기존 경로 도달 불가.

피이용자가 과실범으로만 처벌
    피이용자의 evaluation은 그 과실범(예: 과실치사) offense_ref에 대한 것이라,
    이용자가 원하는 고의범죄(예: 살인)의 realization과 별개다 — cross-offense-type
    문제(정정 2의 33조 단서 질문과 성격이 비슷하다).
```

**정정 4 — 진짜 architecture 질문은 "새 mode 신설 여부"가 아니라 "cross-actor
symbolic dependency"다.** `resolve_derivative_liability`가 이미 "accessory가 다른
actor(principal)의 `LiabilityEvaluation`을 조건으로 참조"하는 cross-actor dependency를
정상적으로 수행하고 있다(instigator/aider가 원래 이 메커니즘이다) — 34조에 필요한 건
**이 메커니즘 자체가 새로 필요한 게 아니라 방향을 뒤집은 버전**이다:
`principal_realization_truth`의 "성공 조건"이 아니라 "피이용자가 확정적으로 불처벌
(또는 과실범으로만 처벌)"이라는 반대 조건을 읽는 함수 하나가 필요할 수 있다는
가설이다 — 이게 확인되면 v0가 제안했던 "완전히 새로운 participation mode"보다 훨씬
작은 변경(기존 파이프라인 재사용 + 조건 함수 하나 추가)으로 34조가 표현될 가능성이
있다. **이번 배치는 이 가설을 세우는 데까지만 하고, 검증은 2패스/Step 7로 이월한다.**

---

## 정정 5 — `legal_element.agent_unpunished_or_negligent`를 LegalElement로 만들지 않는다

**v0 오류**: "피이용자가 불처벌이거나 과실범으로만 처벌된다"를 LegalElement로
제안했는데, 이건 **symbolic runtime이 이미 계산해야 할 법적 결론**(피이용자 자신의
`LiabilityEvaluation`/`OffenseRealization` 판정 결과)이지, neural assessment(Call3)가
새로 판정할 사실이 아니다 — LegalElement로 만들면 "피이용자는 불처벌이다"를 Call3에게
다시 묻게 되어 v2의 핵심 원칙(symbolic이 이미 계산 가능한 걸 neural에 위임하지 않는다)을
깬다.

**v1(수정)**: 이 predicate를 **candidate에서 제거**한다. 34조가 필요로 하는 건
predicate가 아니라 정정 4의 "symbolic dependency" 메커니즘(다른 actor의
`LiabilityEvaluation`을 읽는 함수) — 그 결과가 확정되면 함수 형태로 runtime에 들어갈
것이지, predicate 사전에 legal_element로 등재될 대상이 아니다.

**`legal_element.instrumentalization_of_agent`도 신설을 보류한다.** canonical_meaning에
"처벌되지 않는 자를 도구로 이용 + 교사/방조 형태의 이용행위"를 한꺼번에 담아 이미
존재하는 `ground_fact.instigation_conduct`/`ground_fact.aiding_conduct`(Step 6C 8차
addendum, 이미 fixture에서 `instigator`/`aider` mode의 `requires`로 쓰이고 있음)와
상당 부분 중복된다. 34조의 "이용행위"(다수설: 사주 또는 이용, 34조 문언: 교사 또는
방조)가 이 기존 predicate로 표현 가능한지부터 확인하고, 정말 부족한 부분만 최소
추가한다 — 이번 배치에서는 신설 여부를 열어두고 확정하지 않는다.

---

## 정정 6 — 34조 2항 `supervisory_relationship`: 관계·인식·행위를 다시 분리

**v0 오류**: "지휘·감독을 받는 자임을 인식하고 그 자를 교사 또는 방조하였다"에 관계·
인식·교사방조행위 세 가지가 섞여 있었다 — 배치②(mistake_bundle 정정)에서 이미 확인한
원칙(한 predicate에 여러 종류의 사실을 합치지 않는다)과 같은 문제.

**v1(수정)**:

```text
legal_element.supervisory_relationship
    피이용자가 이용자의 지휘·감독을 받는 관계에 있었다
```

인식·교사/방조 행위 자체는 기존 `instigation_conduct`/`aiding_conduct`/34조 1항 구조
(정정 3·4가 아직 미확정)를 재사용한다. 관계 자체를 `RelationDef`로 올릴지는 2패스에서
실제로 필요할 때 판단 — 이번 배치에서 미리 결정하지 않는다.

---

## 배치⑤ v1 요약

**이번 배치에서 진짜로 드러난 architecture 질문은 하나로 수렴한다**: "actor A의
symbolic legal state(`LiabilityEvaluation`/`OffenseRealization`)를 actor B의 liability
조건으로 참조하는 cross-actor dependency"가 기존 구조(이미 instigator/aider가 이
패턴을 쓰고 있다)를 어디까지 확장해 재사용할 수 있는가 — 33조 단서(같은 사실관계를
참가자마다 다른 offense로 평가)와 34조(참조 방향을 뒤집어 "실패"를 조건으로 함) 둘 다
이 하나의 질문의 변형이다. 33조 본문 교사·방조는 기존 구조로 지원될 가능성이 높고,
33조 본문 공동정범과 33조 단서·34조는 전부 2패스 compatibility 확인 대상으로 낮춘다.
predicate 사전 차원에서는 신규 legal_element를 최소화했다(`agent_unpunished_or_
negligent` 철회, `instrumentalization_of_agent` 보류, `supervisory_relationship`만
좁혀서 유지).
