# Predicate 사전 확장 — 배치 ② 총칙 고의·과실·사실의착오·인과관계·부작위·동시범 (제13·14·15·17·18·19조) v1

[predicate_dictionary_ext_batch02_v0.md](predicate_dictionary_ext_batch02_v0.md)에 대한 사용자
검수 4건 반영. v0는 그대로 둔다 — 이력 추적용. 13·17조는 v0 그대로(변경 없음), 14·15·18·19조가
바뀐다.

**이번 정정의 공통 원인**: v0가 `IDPR_v2.1.0_DESIGN_PROPOSAL.md` 7절("Shared Element
Modules")이 이미 예정해둔 `negligence_bundle`/`omission_bundle`/mistake 전용 구조를
확인하지 않고 13조 `intent`와 같은 "단일 legal_element" 패턴을 14·15·18조에도 그대로
복제했다. 7절은 명시적으로 "과실, 부작위, 착오처럼 복합 법리를 단순 slot 하나로 축약하지
않는다"고 못박아뒀고, 이를 위해 `ElementBundleDef`(`docs/contracts/v2/
element_bundle_def.schema.json`)라는 스키마 타입이 **이미 존재한다** — 다만 지금까지
`element_bundles.yaml`의 검증용 fixture 1개(`bundle.robbery_conduct_bundle`) 말고는
어떤 offense에도 실사용된 적이 없다(`SCHEMA_NOTES.md` 확인: "현재 fixture 어디서도
element_modules를 안 쓰고 있어 마이그레이션 대상은 아니다"). **이 배치가 `ElementBundleDef`의
첫 실사용 사례가 된다** — 13조가 신규 predicate의 첫 실사용이었던 것과 같은 종류의 이정표.

---

## 정정 1 — 제14조 과실: `negligence` 단일 legal_element → `bundle.negligence_bundle`

**v0 오류**: 객관적 주의의무·예견가능성·회피가능성·의무위반을 `legal_element.negligence`
하나에 뭉쳤다 — 설계 문서 7절이 미리 금지해둔 정확히 그 패턴("과실 자체를 하나의
LegalElement로 뭉개지 않는다").

**v1(수정)** — 설계 문서 7절의 4-constituent 구조를 그대로 채운다:

```text
legal_element.duty_of_care
    행위자에게 사회생활상 요구되는 객관적 주의의무가 있었다(허용된 위험·신뢰의
    원칙에 따른 한계를 legal_standard에 포함 — Ⅱ.1의 방대한 교통사고 판례군이 전부
    이 predicate 하나의 기준을 채우는 재료다)

legal_element.foreseeability
    행위자가 통상의 주의를 기울였다면 구성요건적 결과 발생을 예견할 수 있었다

legal_element.avoidability
    행위자가 요구되는 조치를 취하였다면 결과 발생을 회피할 수 있었다

legal_element.breach_of_duty
    행위자가 위 주의의무를 위반하였다(예견 또는 회피를 위한 조치를 게을리하였다)

bundle.negligence_bundle (ElementBundleDef)
    requires = ALL(duty_of_care, foreseeability, avoidability, breach_of_duty)
```

과실범 offense는 `element_modules`에 `{ref: bundle.negligence_bundle, placement: ...}`로
붙인다(`SCHEMA_NOTES.md`가 설명하는 COMPOSE의 bundle-placement 메커니즘 재사용, 신규
스키마 불필요). `professional_negligence`/`gross_negligence`(업무상과실/중과실)는
이 bundle과 **별개 문제**로 남긴다 — 각칙 특유 가중요건이므로 art268 카드가 다루고,
이번 배치는 결정하지 않는다(v0의 판단 유지).

**366조(재물손괴) 언급 삭제**: v0가 과실범 예시에 art366을 넣었는데, 손괴죄는 원칙적으로
고의범만 처벌하고 과실손괴는 처벌규정이 없다 — 잘못된 예시였다. `negligence_bundle`을
쓰는 이번 트랙 조문은 art267(과실치사)·art268(업무상과실·중과실치사상)뿐이다.

---

## 정정 2 — 제15조 사실의 착오: `intent`/`causal_nexus` legal_standard 흡수 폐기, 별도 mistake 구조로

**v0 오류**: 구성요건적 착오를 `intent`의 legal_standard로, 인과관계의 착오를 `causal_nexus`의
legal_standard로 흡수한다고 적었다. 설계 문서 7절이 이미 예정해둔 구조(`perceived_fact` /
`actual_fact` → mistake doctrine/module → mental element에 대한 효과)를 확인하지 않고
기존 predicate에 억지로 끼워 넣은 것 — 특히 인과관계의 착오 쪽이 심각한 오류였다:
`causal_nexus`는 **행위와 결과 사이에 객관적으로 인과관계가 있는가**를 판단하는
relation인데, 인과관계의 착오는 "객관적 인과관계는 TRUE인데 행위자가 예상한 인과경과와
실제 경과가 다르다"는 **주관적 착오** 문제라 `causal_nexus`의 legal_standard에 넣으면
객관적 relation 판단과 주관적 mens rea 판단이 섞인다.

**v1(수정) — mistake를 별도 구조로 저작한다**:

```text
ground_fact.perceived_fact
    행위자가 행위 당시 인식·의욕한 구성요건적 사실(객체·방법·인과과정 등)

ground_fact.actual_fact
    실제로 발생한 구성요건적 사실(객체·방법·인과과정 등)

legal_element.mistake_within_same_construct
    perceived_fact와 actual_fact가 (판례의 법정적 부합설 기준으로) 동일한
    구성요건에 해당한다 — 구체적 사실의 착오
```

**구조 결정이 아직 안 남아 있다 — 검수 필요.** 설계 문서 7절 원문은 이 흐름을
"Elements-stage shared doctrine 또는 module"이라고 적었는데, 지금 스키마
(`doctrine_def.schema.json`)는 `DoctrineDef.stage`에서 **"elements"를 명시적으로
제외**한다("a doctrine cannot attach at the Elements stage, only defeat/modify/exempt
what comes after it" — 스키마 주석 원문). 즉 설계 문서가 쓰인 시점 이후 스키마가
더 좁아졌고, "mistake doctrine"이라는 7절의 표현을 문자 그대로 구현할 방법이 지금 없다.
두 가지 후보:

```text
(a) bundle.mistake_bundle (ElementBundleDef)
    requires = ALL(perceived_fact, actual_fact, mistake_within_same_construct)
    → intent(13조)의 element_modules에 붙여, "perceived_fact 기준으로 인식한
    구성요건의 고의가 actual_fact에 대해서도 인정된다"는 걸 표현

(b) intent 자체의 legal_standard 안에서 이 판단기준만 서술로 남기고
    별도 predicate/bundle을 만들지 않는다(v0의 접근, 이번에 기각)
```

(a)가 7절의 "shared module" 취지에 더 가깝고, `intent`(13조)와 `mistake_bundle`을
분리해두면 **인과과정의 착오**(같은 15조, `causal_nexus`는 TRUE 유지하되
`perceived_fact`/`actual_fact`의 인과경과 서술이 다름)도 같은 구조로 표현 가능하다 —
`causal_nexus` relation 자체는 손대지 않는다(v0가 잘못 흡수했던 지점을 여기서 바로잡음).
**2패스 저작 시 (a)로 확정할 것을 제안**하되, `doctrine.stage`가 elements를 배제하는 이유
자체가 이번에 처음 실제로 부딪힌 제약이라 사용자 확인을 받는다.

**Ⅲ.1(제1항, 신분 등 가중요건 착오)**과 **부진정 결과적가중범(Ⅴ-Ⅵ)**에 대한 v0의 판단은
유지(변경 없음): 전자는 art250의 `intent_knowledge_lineal_status` 카드가 실증하는 기존
패턴이라 새 predicate 불필요, 후자는 offense별 개별 판단으로 이월.

---

## 정정 3 — 제18조 부작위범: `failure_to_act`(실제 부작위 자체) 누락, 4-constituent bundle로

**v0 오류**: `guarantor_status`/`capacity_to_perform_required_act`/`act_equivalence` 3개만
제시했는데, 이 셋이 전부 TRUE라도 "행위자가 실제로 요구된 작위를 하지 않았다"는 raw
factual conduct가 없으면 부작위 자체가 성립하지 않는다 — 설계 문서 7절의
`omission_bundle` 4-constituent(`duty_to_act`/`possibility_to_act`/`failure_to_act`/
`equivalence_to_commission`) 중 `failure_to_act`가 빠져 있었다.

**v1(수정)** — 명칭을 설계 문서 7절 용어에 맞춰 정리하고 누락분을 채운다:

```text
legal_element.duty_to_act              (v0의 guarantor_status와 동일 개념, 명칭만 통일)
    행위자가 법령·계약(사무관리 포함)·선행행위·신의칙(조리)에 의하여 결과발생을
    방지할 보증인적 지위(작위의무)에 있었다

ground_fact.possibility_to_act         (v0의 capacity_to_perform_required_act, 명칭만 통일)
    행위자가 그 구체적 상황에서 요구되는 행위를 현실적·물리적으로 행할 수 있었다

ground_fact.failure_to_act             (신규 — v0 누락분)
    행위자가 요구되는 그 작위를 실제로 하지 않았다

legal_element.equivalence_to_commission  (v0의 act_equivalence, 명칭만 통일)
    부작위에 의한 구성요건실현이 그 구성요건이 요구하는 수단·방법에 의한 실현과
    동등하게 평가된다(작위와의 동가치성)

bundle.omission_bundle (ElementBundleDef)
    requires = ALL(duty_to_act, possibility_to_act, failure_to_act,
                    equivalence_to_commission)
```

`equivalence_to_commission`을 특정 행위태양 요구 offense에서만 선택적으로 요구한다는
v0의 판단(단순결과범은 거의 문제되지 않음)은 유지 — 다만 이건 "이 predicate를 bundle에
넣을지"가 아니라 "bundle 자체를 그 offense에 element_modules로 붙일지"의 문제로 정리한다
(부진정부작위범이 아닌 offense는 애초에 이 bundle을 안 쓴다).

`causal_nexus` relation을 그대로 재사용한다는 v0 판단도 유지 — 부작위-결과 인과관계는
"반전된 조건공식"(요구된 행위가 있었다면 결과가 발생하지 않았을 것)이라는 다른
legal_standard가 필요하지만, 이건 기존 relation의 legal_standard 확장이지 새 relation이
아니다.

---

## 정정 4 — 제19조 동시범: **runtime UNKNOWN ≠ "원인 판명 불능"(legal indeterminacy)**

**v0의 가장 중요한 오류.** v0는 `causal_origin_unascertained`를 "causal_nexus가 각
행위자에 대해 UNKNOWN"으로 읽고, 이걸 근거로 "지금 런타임(Completion, `|T|==0,U≠∅ →
unresolved`)이 19조를 못 담는다"며 19조 전체를 33/34/35-36조와 같은
architecture-compatibility 검수 대상으로 재분류했다. **이 등식 자체가 틀렸다.**

```text
runtime UNKNOWN
    시스템이 아직 법적 판단을 확정하지 못한 상태(증거·저작 불충분 등, 우리 시스템의
    3치 논리 내부 사정)

causal_origin_unascertained = TRUE
    "충분히 심리하였으나 어느 독립행위가 결과의 원인인지 판명할 수 없다"는, 법원이
    적극적으로 확정하는 하나의 법적 결론 — 형사소송에서 사실관계가 확정된 상태다
```

후자는 그 자체로 **TRUE/FALSE 판정이 가능한 legal_element**이지, 전자(엔진의 3치 미해결
상태)가 아니다. 즉 19조는 기존 `CompletionPolicyDef`로 바로 표현 가능하다 — 신규
runtime semantics나 구조 검토가 필요 없다:

```text
ground_fact.concurrent_independent_acts
    2인 이상이 의사연락 없이 각자 별개의 행위(구성요건적 실행행위)를 하였다

ground_fact.same_object_of_result
    그 행위들이 동일한 객체(사회적·규범적 의미)에 결과를 발생시켰다

legal_element.causal_origin_unascertained
    결과 발생의 원인이 된 행위가 어느 것인지 판명되지 않았다(법원이 심리 후
    확정하는 상태 — 엔진의 UNKNOWN이 아니다)

CompletionPolicy state (기존 CompletionPolicyDef, 신규 스키마 불필요):
    when = ALL(
        concurrent_independent_acts,
        same_object_of_result,
        causal_origin_unascertained
    )
    → attempted
```

**263조 특례만 별도 검토 대상으로 남긴다.** "원인불명이면 공동정범의 예에 의한다"는
6C Participation이 전제하는 실제 공동가공 의사·귀속 없이 **법률상 의제만으로** co-principal
취급을 발생시키라는 요구라, `apply_attribution`이 지금 그런 경로를 지원하는지는 별도
검토가 필요하다 — 이건 진짜 architecture 질문이다. 다만 263조는 총칙이 아니라
**각칙 art263(생명·신체, 배치⑨) 소관**이므로, 배치⑨에서 33/34(배치⑤)의
Participation 구조 검토와 묶어 다룬다. **19조 본문 자체는 architecture gap이 아니다** —
이번 정정으로 마스터플랜의 원래 분류("17-19조는 Elements 유형")가 맞았던 것으로 확인된다.

---

## 배치② v1 요약 — 신규 스키마·DSL primitive 필요 여부

**여전히 없음.** 다만 이번에 처음으로 `ElementBundleDef`(negligence_bundle,
omission_bundle, mistake_bundle 후보)를 실제로 채운다 — 스키마는 이미 있었으므로
추가·변경은 없고, **최초 실사용**이라는 의미가 있다. 19조는 v0가 제기했던
architecture 우려가 정정으로 해소됐다.
