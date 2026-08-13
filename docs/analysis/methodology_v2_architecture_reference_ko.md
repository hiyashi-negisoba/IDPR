# IDPR v2 방법론 구조 정리 — 논문 Methodology 작성 참고자료

## 1. 한 문장 요약

IDPR v2는 형사법 지식을 전용 DSL로 형식화하고 컴파일한 뒤, 언어모델에는 사건별 후보 탐색·
사실 결박·최소 명제 판정만 맡기고, 최종 법적 조립과 책임 판단은 typed symbolic runtime이
수행하도록 설계한 compiler-mediated neuro-symbolic architecture이다.

논문에서 가장 간결하게 나타내면 다음과 같다.

```text
Criminal-law DSL and compiler
              ↓
Neural candidate routing (Call 1)
              ↓
Neural fact-to-issue binding (Call 1.5)
              ↓
Symbolic instance materialization and query compilation
              ↓
Neural atomic proposition assessment (Call 2)
              ↓
Symbolic legal evaluation (Scallop-based runtime)
              ↓
Typed answer representation
              ↓
Neural IRAC realization (Call 3)
```

이를 한국어로 압축하면 다음과 같다.

> 형사법 DSL/컴파일러를 기반으로 사건의 법적 후보를 탐색하고(Call 1), 후보를 사건의 구체적
> 행위자와 사실 episode에 결박한 뒤(Call 1.5), host compiler가 유한한 판단 instance와 최소
> 질문을 생성한다. 언어모델은 각 명제의 사실상·법률상 진릿값만 판정하고(Call 2), Scallop 기반
> symbolic runtime이 이를 형사법 구조에 따라 결합하여 책임 결론을 산출한다. 마지막 Call 3는
> 이 typed 결과를 IRAC 형식의 자연어 답안으로 실현한다.

---

## 2. v1에서 v2로의 핵심 변화

### 기존의 단순한 구도

초기 버전은 대체로 다음과 같은 세 단계로 설명할 수 있었다.

```text
Neural analysis (Call 1, Call 2)
        ↓
Symbolic reasoning
        ↓
Neural answer generation (Call 3)
```

이 표현은 전체적인 neuro-symbolic 구도는 보여주지만, 다음 사항을 충분히 설명하지 못한다.

- 법률 지식이 어떤 형식으로 표현되는가
- 사건에서 평가해야 할 symbolic instance를 누가 만드는가
- 동일 죄명 후보가 여러 행위자·여러 행위에 대응할 때 identity를 어떻게 보존하는가
- 파생범죄, 미수, 공범, 위법성·책임, 법률효과를 어떻게 구조적으로 조립하는가
- 언어모델의 판단과 symbolic legal inference의 경계가 어디인가

### v2의 구도

v2의 핵심 변화는 symbolic 단계 앞에 **형사법 전용 Definition Layer, DSL compiler, 그리고
case-time instance compiler**를 명시적으로 둔 것이다. 따라서 v2는 단순히 “LLM 결과를 규칙에
넣는 구조”가 아니라, 다음의 세 층을 분리한다.

1. **법률 지식의 형식화와 컴파일**
2. **사건별 factual grounding과 atomic assessment**
3. **컴파일된 법률구조의 symbolic execution**

| 구분 | v1의 추상적 설명 | v2의 설명 |
|---|---|---|
| 법률 지식 | symbolic rules | typed criminal-law DSL |
| 사건 후보 | neural output | Call 1 seed와 compiler-derived closure |
| 사건 identity | 암묵적 | actor–offense–episode/binding instance |
| 사실 결박 | Call 2에 혼재 | 독립된 Call 1.5 |
| 모델 질문 | 비교적 넓은 판단 | compiler가 생성한 atomic target |
| symbolic 단계 | 결과 결합 | compiled Elements–Completion–Stage–Participation evaluation |
| 최종 생성 | 자유로운 답안 생성 | typed result에 근거한 IRAC realization |

---

## 3. 형사법 전용 DSL

### 3.1 DSL의 목적

DSL은 개별 사건의 결론을 저장하는 규칙 모음이 아니다. 형사법상 판단에 필요한 **법률 개념의
종류, 구성관계, 의존관계와 평가 순서**를 기계가 검사하고 실행할 수 있는 형태로 표현한다.

즉 DSL은 다음 질문에 답한다.

- 어떤 범죄가 어떤 구성요건 slot으로 이루어지는가
- 단순범죄와 파생범죄는 어떤 구조적 관계를 가지는가
- 여러 범죄 구성요소가 결합되는 경우 각각의 occurrence identity를 어떻게 보존하는가
- 기수·미수·중지·예비 같은 completion state는 어떤 조건을 요구하는가
- 공동정범·교사범·방조범 등 participation은 누구의 어떤 realization에 의존하는가
- 위법성, 책임, 처벌조건 및 doctrine effect는 어느 단계에 작용하는가
- 최종적으로 어떤 typed legal result를 산출해야 하는가

### 3.2 주요 추상 객체

논문 본문에서는 구현 클래스명보다 아래 정도의 범주로 소개하면 충분하다.

- **Offense definitions**: 개별 범죄와 그 구성요건 구조
- **Derived-offense definitions**: 기본범죄의 가중·결합·특수 형태
- **Ground facts and legal elements**: 사실 명제와 법적 평가 명제
- **Relations**: 구성요소나 occurrence 사이의 인과적·구조적 관계
- **Completion policies**: 기수, 미수, 중지미수, 불능미수, 예비 등 실행단계
- **Participation policies**: 정범, 공동정범, 교사범, 방조범의 귀속과 종속관계
- **Doctrines and effects**: 위법성·책임·처벌 및 특수 법리의 작동 조건과 효과

중요한 점은 각 객체가 단순 문자열 label이 아니라 **typed object**라는 것이다. 컴파일러는
참조 대상의 종류, 구성요소 identity, 허용된 결합, 누락된 정의와 순환 등을 실행 전에 검사한다.

### 3.3 구조 조합

범죄 구조는 개념적으로 두 종류의 조합으로 설명할 수 있다.

- **Qualification**: 기본범죄에 가중·특수 조건을 부가하는 구조
- **Composition**: 여러 범죄 구성요소와 그 사이의 relation을 결합하는 구조

이 구분 덕분에 파생범죄를 평면적인 predicate 목록으로 환원하지 않고, 어떤 기본범죄와
구성요소가 어떤 경로로 결합되었는지 provenance를 유지할 수 있다.

### 3.4 컴파일러의 역할

DSL compiler는 법적 결론을 미리 정하지 않는다. 대신 다음을 생성한다.

- seed로부터 반드시 검토할 구조적 core
- 사실에 따라 열릴 수 있는 파생범죄·completion·participation·doctrine probe
- 각 candidate를 판단하는 데 필요한 최소 factual/legal proposition frontier
- symbolic runtime이 실행할 typed obligations와 dependency structure

따라서 compiler의 역할은 “정답 추론”이 아니라 **법적으로 유효한 판단 공간을 생성하고 그
공간의 타입과 의존성을 보장하는 것**이다.

---

## 4. 전체 추론 파이프라인

### 4.1 Call 1 — high-recall legal candidate routing

Call 1은 사건과 질문을 보고 검토할 가치가 있는 offense seed를 고른다. 이 단계의 목적은
최종 죄명을 확정하는 것이 아니라, 후속 compiler가 탐색할 법적 구조의 출발점을 제공하는 것이다.

```text
case and question
      ↓
candidate offense seeds
```

Call 1의 성격은 다음과 같다.

- **high recall 지향**
- actor-level 책임이나 범죄 성립 여부를 판단하지 않음
- 구성요건 진릿값을 판정하지 않음
- DSL catalog에 존재하는 canonical definition을 선택

Call 1 seed는 compiler에 의해 구조적 closure로 확장된다. 다만 closure에 존재한다는 사실은 그
범죄가 실제 사건에서 성립하거나 심지어 case-time candidate로 materialize되었다는 뜻이 아니다.

### 4.2 Call 1.5 — fact-to-issue binding

Call 1.5는 Call 1이 선택한 추상적인 legal seed를 사건 원문의 구체적 factual episode에
결박한다.

개념적으로 다음 identity를 만든다.

```text
legal seed
  + responsible actor candidate
  + actor's conduct evidence
  + relevant contextual evidence
  + case-time factual episode
```

Call 1.5의 출력은 아직 법적 realization이나 책임 결론이 아니다. 이 단계는 다음만 정한다.

- 어느 actor의 책임 후보인지
- 그 actor의 어떤 행위가 후보의 중심인지
- 같은 판단에서 함께 보아야 할 결과·상대방 행위·후속 사실은 무엇인지
- 해당 factual episode를 원문의 어느 span이 뒷받침하는지

반대로 Call 1.5는 다음을 판단하지 않는다.

- 구성요건 충족 여부
- 정범·공동정범·교사범·방조범
- 법적 인과관계 또는 dependency
- 범죄 성립과 최종 책임

이 분리는 동일한 죄명 하나를 모든 actor와 모든 사실 occurrence에 곱하는 Cartesian expansion을
막고, 뒤 단계의 판단 단위를 사건 원문에 고정한다.

### 4.3 Symbolic case-time materialization

Call 1과 Call 1.5 사이의 결과를 host compiler가 결합하여 유한한
`actor–offense–episode` evaluation instance를 만든다.

이 단계가 v2에서 특히 중요한 이유는, Call 2가 스스로 “누구의 어떤 범죄를 판단할지” 선택하지
않도록 하기 때문이다. Call 2는 compiler가 이미 정한 instance와 proposition만 받는다.

Host compiler는 개념적으로 다음을 수행한다.

1. Call 1 seed의 DSL closure를 계산한다.
2. Call 1.5 binding으로 direct case-time instance를 만든다.
3. 같은 factual episode에 필요한 독립 evidence가 존재하는 경우에만 파생 candidate를 연다.
4. 각 instance의 DSL 구조에서 평가에 필요한 최소 proposition을 수집한다.
5. relation, participation, completion 등 별도 평가가 필요한 typed target을 생성한다.

여기서 중요한 원칙은 다음과 같다.

> 구조적으로 가능하다는 이유만으로 candidate를 확장하지 않고, 그 candidate를 질문할 최소
> factual ingredients가 동일 사건 episode에 확보되었을 때만 materialize한다.

Host는 이 evidence의 존재 여부만 검사하며, 그 evidence가 법률요건을 실제로 충족하는지는
판정하지 않는다.

### 4.4 Call 2 — atomic factual and legal proposition assessment

Call 2는 v2의 실질적 neural 판단 경계다. 입력은 compiler가 고정한 instance와 최소 명제이며,
출력은 각 명제에 대한 제한된 진릿값이다.

```text
(fixed instance, fixed proposition)
              ↓
       TRUE / FALSE / UNKNOWN
```

Call 2가 판단할 수 있는 것은 다음과 같다.

- 원문이 특정 factual proposition을 명시적으로 지지하는가
- 고정된 instance에 대해 특정 legal element가 충족되는가
- 별도로 고정된 두 instance 사이의 relation이 성립하는가

Call 2는 다음을 할 수 없다.

- 새로운 offense나 actor를 추가
- instance identity를 변경
- participation mode나 completion state를 최종 선택
- symbolic edge 또는 DAG를 생성
- 최종 죄책을 선언

모델의 응답은 host validation을 거쳐 typed `CaseTruths`로 변환된다. `UNKNOWN`은 누락된
FALSE가 아니라 증거 또는 평가가 해결되지 않았다는 독립 상태로 보존된다.

### 실질적 neural boundary와 Call 3의 구분

Call 3도 언어모델을 사용하지만, 방법론적으로 새로운 법률판단을 수행하는 inference stage로
보지 않는 것이 깔끔하다.

- **Call 2까지**: 사건에 관한 새로운 factual/legal truth를 산출하는 neural inference
- **Call 3**: 이미 확정된 typed legal result를 자연어로 표현하는 controlled realization

따라서 “substantive neural decision boundary ends at Call 2”라고 표현할 수 있다.

### 4.5 Scallop-based symbolic legal evaluation

Call 2가 만든 원자적 truth는 그 자체로 범죄 성립 결론이 아니다. Scallop 기반 symbolic
runtime은 컴파일된 DSL 구조와 CaseTruths를 결합하여 법적 평가를 실행한다.

개념적인 평가 순서는 다음과 같다.

```text
predicate truths
      ↓
completion and offense realization
      ↓
elements
      ↓
unlawfulness
      ↓
culpability
      ↓
punishability and special effects
      ↓
typed liability result
```

필요한 경우 participation dependency, 다른 actor의 realization, statutory deeming, component
relation 등이 이 과정에 연결된다.

Symbolic runtime의 장점은 다음과 같다.

- 같은 입력 truth에 대해 결정론적으로 재실행 가능
- 어떤 obligation에서 결론이 성립·실패·미해결되었는지 추적 가능
- actor, offense, occurrence identity를 끝까지 보존
- 법률효과를 factual truth로 위조하지 않고 별도 provenance로 기록
- 미해결 정보가 있는 경우 임의의 결론 대신 unresolved 상태를 유지

### 4.6 Typed answer representation과 Call 3

Scallop 결과는 곧바로 자유서술 답안으로 전달하기보다, 먼저 답안에 필요한 구조로 정리한다.

예를 들면 다음 정보가 포함될 수 있다.

- 검토된 issue와 actor
- 적용되는 offense 및 participation mode
- completion state
- 충족·실패·미해결된 핵심 obligation
- 적용된 doctrine과 법률효과
- 최종 realization/liability 상태
- 결론의 provenance

Call 3는 이 typed answer representation을 입력받아 IRAC 형식으로 자연어화한다.

```text
Issue
  → applicable Rule
  → Application grounded in typed findings
  → Conclusion
```

Call 3의 역할은 설명 구성, 논증 순서, 표현과 가독성이다. 앞 단계 결과에 없는 새로운 죄명,
사실, participation relation 또는 법률효과를 추가해서는 안 된다.

---

## 5. v2의 핵심 설계 원칙

### 5.1 Atomic neural tasks

각 neural call에는 필요한 최소 작업만 부여한다.

- Call 1: legal seed routing
- Call 1.5: seed–fact binding
- Call 2: fixed proposition truth assessment
- Call 3: typed result realization

모델 한 번에 사건 DAG, 모든 구성요건, 공범관계와 최종 책임을 동시에 생성하게 하지 않는다.

### 5.2 Identity preservation

v2의 판단 단위는 단순한 `actor + offense`가 아니다. 동일 actor가 동일 offense에 해당할 수 있는
행위를 여러 번 할 수 있으므로 factual episode/binding identity를 포함한다.

```text
case + actor + offense + occurrence/binding
```

이 identity는 Call 1.5, Call 2, symbolic runtime과 최종 provenance까지 유지된다.

### 5.3 Candidate generation과 legal judgment의 분리

Candidate compiler는 무엇을 물어볼지 결정하지만, 그 법적 명제의 참·거짓을 결정하지 않는다.
반대로 Call 2는 고정된 명제를 평가하지만 무엇을 평가할지 스스로 선택하지 않는다.

이 양방향 제한이 host를 작은 법률추론 모델로 만드는 문제와 LLM의 자유로운 candidate expansion을
동시에 방지한다.

### 5.4 Evidence-gated closure

DSL의 구조적 closure는 탐색 가능성을 제공한다. 그러나 base offense가 존재한다는 이유만으로
모든 파생범죄를 실제 instance로 만들지 않는다. 필요한 factual components가 같은 episode에
존재할 때만 candidate를 열고, 실제 충족 여부는 Call 2와 symbolic runtime에 남긴다.

### 5.5 Three-valued semantics

사건 서술이 명제를 지지하지 않는다는 사실과 명제를 반박한다는 사실은 다르다. 따라서 v2는
`TRUE`, `FALSE`, `UNKNOWN`을 구별한다. Symbolic runtime도 UNKNOWN을 임의의 FALSE로 바꾸지
않고 unresolved legal state로 전파한다.

### 5.6 Provenance and auditability

각 단계는 다음 lineage를 보존한다.

```text
DSL definition
→ compiler path
→ factual binding and source span
→ atomic assessment
→ symbolic obligation
→ legal result
→ answer statement
```

이를 통해 최종 오류가 후보 누락, binding 오류, model undercall, compiler coverage, symbolic rule,
또는 answer realization 중 어디에서 발생했는지 분리할 수 있다.

---

## 6. 방법론의 추상적 기여로 제시할 수 있는 점

논문에서는 다음을 핵심 기여 후보로 정리할 수 있다.

1. **형사법 전용 typed DSL**
   - 범죄구성, 파생범죄, completion, participation과 단계별 법률효과를 하나의 검사 가능한
     Definition Layer로 표현한다.

2. **Compiler-mediated neural grounding**
   - LLM이 logic program을 직접 생성하는 대신, compiler가 DSL에서 사건별 유한 평가 공간과
     atomic query를 생성한다.

3. **별도의 fact-to-issue binding 단계**
   - 추상적 legal candidate와 원문의 actor-specific factual episode를 분리해 결박한다.

4. **Typed neural–symbolic boundary**
   - 모델 출력은 자유로운 추론 trace가 아니라 고정된 key에 대한 3값 truth이며, symbolic
     runtime은 이 값만 소비한다.

5. **Occurrence-preserving legal evaluation**
   - 동일한 actor와 offense라도 서로 다른 행위 episode를 구분하여 잘못된 사실 혼합과
     Cartesian expansion을 줄인다.

6. **Auditable symbolic conclusion and controlled generation**
   - 최종 결론에 obligation-level provenance를 남기고, Call 3를 새로운 추론이 아닌 IRAC
     surface realization으로 제한한다.

---

## 7. 논문에서 사용할 수 있는 단계 명칭 제안

| 내부 명칭 | 논문용 명칭 후보 | 핵심 기능 |
|---|---|---|
| Definition Layer | Criminal-Law Definition Layer | typed legal knowledge representation |
| DSL compiler / Step 7 | Structural Closure and Probe Compiler | candidate structure and minimal frontier compilation |
| Call 1 | Legal Candidate Router | high-recall offense seed selection |
| Call 1.5 | Fact-to-Issue Binder | actor/episode/evidence binding |
| evaluation planner | Case-Time Instance Compiler | finite typed instance materialization |
| Call 2 | Atomic Legal Proposition Assessor | fixed proposition truth assessment |
| CaseTruths | Typed Case Fact Base | validated three-valued neural output |
| Scallop runtime | Symbolic Liability Evaluator | deterministic legal evaluation |
| answer plan/IR | Typed Answer Representation | structured handoff to generation |
| Call 3 | IRAC Realizer | controlled natural-language realization |

전체 시스템 명칭은 다음 중 하나로 표현할 수 있다.

- **Compiler-Mediated Neuro-Symbolic Criminal-Law Reasoning**
- **DSL-Guided Neuro-Symbolic Liability Analysis**
- **Typed Neuro-Symbolic Pipeline for Criminal-Law Reasoning**

---

## 8. Methodology 본문 작성 시 주의할 구분

### 구조적 후보 coverage와 최종 정확도

Call 1 recall, binding recall, Call 2 predicate accuracy, symbolic conclusion accuracy와 최종
IRAC rubric score는 서로 다른 지표다. 하나를 다른 하나의 성능으로 표현하지 않는 것이 좋다.

### Compiler와 symbolic runtime

- compiler: 평가할 구조와 query를 생성
- runtime: truth를 법률구조에 따라 실행·결합

둘을 하나의 “rule engine”으로 뭉뚱그리면 v2의 핵심 경계가 흐려진다.

### Call 1.5와 Call 2

- Call 1.5: 어느 사실 episode가 어느 legal seed와 관련되는지 결박
- Call 2: 그 결박된 instance의 특정 명제가 참인지 평가

Call 1.5를 구성요건 판정 단계로 설명해서는 안 된다.

### Substantive inference와 answer generation

Call 3가 neural call이라는 사실과 substantive neural inference가 Call 2에서 끝난다는 설명은
모순되지 않는다. Call 3는 epistemic decision stage가 아니라 constrained language realization
stage로 정의하면 된다.

### 현재 구현 상태와 목표 architecture

방법론에서는 목표 architecture를 설명하되, 실험 결과에서는 각 경로의 실제 production 연결
여부를 별도로 보고해야 한다. 특히 participation, indirect-principal, doctrine activation,
completion 및 offense competition/absorption은 구조의 존재와 end-to-end coverage를 구분해
기술하는 것이 안전하다.

---

## 9. 가장 짧은 발표용 설명

> 기존 시스템이 LLM 분석–symbolic reasoning–LLM 답안 생성의 3단 구조였다면, v2는 그 사이의
> 인터페이스를 형사법 전용 DSL과 compiler로 명시적으로 재설계했다. 첫 모델은 검토할 법적
> 후보를 고르고, 두 번째 binding 단계는 이를 사건의 특정 actor와 factual episode에 연결한다.
> Compiler는 이 결과로 유한한 법적 instance와 최소 명제 질문을 생성하며, Call 2는 각 명제의
> 3값 truth만 판정한다. Scallop 기반 runtime은 compiled criminal-law structure에 따라 이
> truth들을 결합해 typed liability result를 만들고, 마지막 Call 3는 그 결과를 IRAC 답안으로
> 표현한다.
