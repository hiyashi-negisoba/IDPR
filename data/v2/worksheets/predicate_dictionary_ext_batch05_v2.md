# Predicate 사전 확장 — 배치 ⑤ 총칙 공범과 신분·간접정범 (제33·34조) v2

[predicate_dictionary_ext_batch05_v1.md](predicate_dictionary_ext_batch05_v1.md)에 대한 사용자
검수 2건 반영 — 33조 단서의 위치 재조정, 34조의 "역방향 함수" 설명 정교화. 정정 1·3·5·6은
v1 그대로 유지.

---

## 정정 — 33조 단서: core runtime gap이 아니라 orchestration compatibility 문제로 재분류

**v1의 미진한 부분**: v1이 "코드상 principal과 accessory의 offense_ref를 강제로 같게
만드는 장치가 없다"까지 확인해놓고도, 여전히 "architecture-compatibility"라는 같은
등급으로 34조와 나란히 묶어뒀다. 그런데 이 확인 결과 자체가 이미 **6C core(participation.py
의 `resolve_derivative_liability`)는 필요한 표현력을 상당 부분 갖고 있다**는 뜻이다 —
남은 문제는 runtime 로직이 아니라 **그 조합(principal offense ≠ accessory target
offense)을 실제로 만들어 호출하는 caller가 아직 없다**는 것뿐이다.

```text
33조 단서 = cross-offense derivative evaluation
    6C core: 지원 가능성 높음(v1의 코드 확인 결과 그대로)
    남은 확인: Step 7/8 orchestrator가 "principal은 A offense로, accessory는 그와
              다른 B offense(DerivedOffenseDef)로 평가한다"는 조합을 실제로
              생성·호출할 수 있는가 — 이건 Participation runtime을 뜯는 문제가
              아니라 routing/orchestration 문제일 가능성이 크다.
```

**분류를 낮춘다**: "architecture-compatibility"(코드 구조 자체의 문제일 수 있음) 등급에서
"orchestrator 확인 대상"(runtime은 이미 준비돼 있고, 이를 실제로 사용하는 호출부만
아직 없음)으로 내려 34조와 구분한다.

---

## 정정 — 34조: "역방향 함수 하나"는 과도한 단순화

**v1의 오류**: "`principal_realization_truth`의 반대 조건을 읽는 함수 하나가 필요할 수
있다"고 적었는데, v1 스스로 나열한 4가지 경우(책임무능력→realization TRUE, Elements
불충족→realization 없음, Unlawfulness defeated→realization 없음, 과실범만 성립→다른
offense의 realization)는 **하나의 `NOT principal_realization_truth(...)`로 묶이지
않는다** — 뒤의 세 경우는 서로 다른 이유로 "실패"하고, 첫 번째는 애초에 실패가 아니다
(TRUE다). 불리언 하나를 뒤집는 걸로는 34조가 요구하는 구별을 표현할 수 없다.

**v1(수정)** — 질문을 다시 정의:

```text
34조 compatibility question:
    피이용자의 symbolic evaluation(LiabilityEvaluation)에서 34조가 구별해야 하는
    특정 법적 상태를 accessory(이용자) 쪽 조건으로 읽어올 수 있는가?
        - culpability가 defeated인가(책임무능력 등)
        - target offense의 Elements 자체가 fail인가(고의/목적/신분 결여)
        - unlawfulness가 defeated인가(위법성조각)
        - 다른(과실범) offense_ref로 realization이 성립했는가

    즉 필요한 건 단일 불리언 반전이 아니라, 기존 `LiabilityEvaluation`이 이미 갖고
    있는 stage별 결과(`elements`/`unlawfulness`/`culpability`의 `gate_state` 등)를
    accessory 쪽에서 더 세밀하게 참조하는 symbolic dependency다. 새 participation
    mode가 필요한지는 여전히 미정이지만, 필요하다면 "성공/실패 반전"보다 "어느
    stage에서 어떻게 멈췄는지를 구별해서 읽는" 형태에 가까울 것이다.
```

---

## 배치⑤ v2 요약 — 남은 compatibility는 2축, 성격이 다르다

**cross-actor dependency 자체는 이미 6C가 지원한다** — instigator/aider가 원래 이
메커니즘이다(v1 정정 4의 이 부분은 정확했다). 남은 건 그 메커니즘을 어느 방향으로,
얼마나 세밀하게 확장하느냐는 서로 다른 두 질문이다:

```text
A. 33조 단서 — cross-actor + cross-offense derivative target
   6C core는 가능성 높음, Step 7/8 orchestrator가 실제로 그 조합을 호출하는지만
   확인하면 된다(runtime 변경 가능성 낮음).

B. 34조 — cross-actor symbolic-state dependency
   기존의 "principal_realization_truth 하나(성공 여부)"보다 더 세밀한 stage별
   결과 참조가 필요할 수 있다(runtime 확장 가능성이 A보다 크다).
```

나머지(33조 본문 공동정범의 `attributable_slots` 오용 철회, `agent_unpunished_or_
negligent` LegalElement 제거, `instrumentalization_of_agent` 보류, `supervisory_
relationship` 축소)는 v1 그대로 유지. 배치⑤ 종료.
