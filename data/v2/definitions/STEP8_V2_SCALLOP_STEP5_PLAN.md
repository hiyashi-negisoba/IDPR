# Step 8 — v2 Scallop backend Step 5 계획서

상태: **generic Step 5 및 Article 263 backend-completion gate freeze 완료.**
Call 2 selected predicate assessment가 다음 작업이며, 모델 호출·Definition Layer 변경은
이 문서의 범위 밖이다 (2026-08-11).

## 1. 목적과 고정 경계

Step 5의 목적은 이미 동결·검증된 Step 2/3/4의 결과를 기존 Python runtime의
순서대로 연결하여, 기존 타입인 `LiabilityEvaluation` 및 조건부
`LiabilityResult`를 재구성하는 것이다.

```text
CaseTruths
  -> Step 3 Completion / 조정된 Elements
  -> Step 4 participation 및 doctrine stage-effect 결과
  -> Step 5 비가설적 stage chain gate
  -> 기존 typed StageResult / LiabilityEvaluation / LiabilityResult adapter
```

이 단계는 새 법적 추상화, 새 instance/binding carrier, 새 predicate, legacy
`card_status`/card id 매핑을 만들지 않는다. `OffenseInstanceKey`,
`RuntimeRelationKey`, `CompletionResult`, `StageResult`, `AppliedEffect`,
`LiabilityEvaluation`, `LiabilityResult`가 유일한 런타임 모델이다.

Call 1, Step 7, 동결된 Call 2 factual v0, Definition Layer 및 Call 3 writer는
범위 밖이다. 모델 요청이나 vLLM 서비스 조작도 승인되지 않는다.

## 2. Python parity 기준

유일한 의미론 oracle은 다음 기존 구현이다.

| 표면 | 기준 구현 |
|---|---|
| Completion 중단 및 Elements provenance | `runtime.pipeline.resolve_liability()` / `_resolve_elements()` |
| Elements 이후 chain | `runtime.pipeline.resolve_from_elements()` |
| doctrine stage fold | `runtime.effects.resolve_stage()` |
| co-principal attribution | `runtime.participation.apply_attribution()` / `resolve_co_principal_liability()` |
| derivative principal read | `runtime.participation.principal_realization_truth()` |
| derivative Elements | `runtime.participation._resolve_derivative_elements()` |
| 결과 타입 불변식 | `runtime.stages` |

Scallop 결과가 Python과 다르면 backend 결함이다. Python 의미론을 맞추기 위해
Definition Layer나 Call 2 사실 상태를 바꾸지 않는다.

## 3. 확정해야 할 실행 순서

직접 및 co-principal route는 아래 순서를 정확히 지킨다.

```text
ATTRIBUTE (해당 target만)
  -> Completion
  -> completion-adjusted Elements
  -> Unlawfulness
  -> OffenseRealization
  -> Culpability
  -> OffenseEstablishment
  -> Punishability
  -> LiabilityResult
```

derivative (`instigator` / `aider`) route는 Completion을 만들지 않는다.
Step 4의 `derivative_elements_truth`를 기존 derivative Elements 결과로 삼고,
그 뒤의 Unlawfulness → Culpability → Punishability tail만 같은 규칙으로 연결한다.

### 3.1 비가설적 정지 규칙

아래 중 하나가 발생하면 뒤 stage는 실행하지 않고 각각
`StageResult(evaluation_state="not_reached", legal_state=None, gate_state=None)`로
복원한다.

| 첫 정지 지점 | 조건 | 이후 결과 |
|---|---|---|
| completion | `unresolved`, `not_applicable`, 또는 `punishable=False` | Elements부터 전부 not_reached |
| elements | `fails` 또는 `unresolved` | 세 doctrine stage not_reached |
| unlawfulness | `fails` 또는 `unresolved` | Culpability/Punishability not_reached |
| culpability | `fails` 또는 `unresolved` | Punishability not_reached |
| punishability | `fails` 또는 `unresolved` | `LiabilityResult` 없음 |

`MODIFY=UNKNOWN`로 인해 legal state가 `unresolved`여도 gate가 `passes`인
Culpability/Punishability는 정지가 아니다. 이는 현재 `resolve_stage()`의
legal-state/gate-state 분리를 그대로 보존한다.

## 4. Step 2/3/4 연결 계약 초안

### 4.1 ResultUniverse, route와 endpoint

Step 5의 결과 대상은 넓은 `v2_instance` universe가 아니라 아래의 닫힌 집합이다.
`v2_instance`에는 Step 3의 `when_component` 및 component-scoped completion 평가를
위한 보조 instance도 포함될 수 있고, 그 보조 instance는 독립 결과가 아니다.

```text
C       = Step 3 top-level completion-target instances
Co      = co-principal target instances
D       = derivative accessory instances
Direct  = C - Co
ResultUniverse = C ∪ D

require Co ⊆ C
require C ∩ D = ∅
require component-scope-only v2_instance ∉ ResultUniverse
require ResultUniverse = Direct ⊎ Co ⊎ D
```

따라서 한 `ResultUniverse` instance는 정확히 하나의 route를 가진다.

- direct: 원래 predicate view + Step 3 completion 경로
- co-principal: caller가 이미 승인한 target/source 입력 + sparse attribution 경로
- derivative: 정확히 하나의 `(accessory, principal, mode)` link + completion 없음

동일 accessory에 두 개 이상의 derivative link가 있거나, 동일 instance에
co-principal 및 derivative route가 함께 있으면 하나의 기존 `LiabilityEvaluation`로
축약할 수 없다. Step 5는 mode/route를 추론하거나 임의 선택하지 않고 해당 입력을
거부해야 한다. Step 4 단독 surface의 per-link 출력 계약은 그대로 유지한다.

모든 derivative principal은 단순히 `v2_instance`에 존재하는 것이 아니라
`ResultUniverse`의 독립 평가 대상이어야 한다. derivative→derivative를 허용하면
dependency graph는 self-loop와 cycle이 없는 DAG여야 하며 principal이 accessory보다
먼저 결정되는 topological order를 가져야 한다. 현재 Python API는 이미 계산된
principal `LiabilityEvaluation`을 받으며 cycle의 fixed-point 의미론을 정의하지
않기 때문이다.

### 4.2 integration-only effective predicate view

standalone Step 3/4 emitter 및 validator는 frozen이다. Step 5 integrated lowering만
다음 accessor를 사용한다.

```text
effective_predicate(I, ref):
  I가 co-principal TOP-LEVEL target이고 sparse override(ref)가 있으면
    attributed truth
  그 밖에는
    original predicate truth; missing -> UNKNOWN
```

이 view는 target scope에서 평가되는 모든 expression에 사용한다.

- completion candidate `when`
- top-level completion-adjusted Elements slot
- selected-state `additional_requirements` 중 evaluation scope가 target인 경우
- doctrine `requires`

반대로 `when_component`, component-scoped slot, component-scoped additional
requirement는 original component view를 사용한다. 이 제한은 `apply_attribution()`이
target key만 바꾸고 `component_instance_for()`가 별도 `OffenseInstanceKey`를 만드는
현재 Python 동작과 일치한다. relation truth 및 derivative `requires`도 각각 원래
view를 유지한다.

Article 33 constitutive status는 attributed CaseTruths 사실이 아니라 기존
`CoPrincipalConstitutiveStatusObligation` 및 true-member provenance로 복원한다.

### 4.3 Step 4 standalone / Step 5 integrated producer 분리

Step 4 standalone 계약은 바꾸지 않는다.

```text
Standalone Step 4:
  v2_active_doctrine       = caller/orchestration EDB
  v2_stage_effect_target   = caller EDB
  v2_principal_realization_truth = caller EDB
  기존 compile/render/validate surface 그대로 동결
```

Step 5 integrated lowering은 Step 4의 법적 effect helper/fold를 재사용할 수 있으나,
frozen `render_participation_stage_edb()`와 `validate_participation_stage_query_rows()`를
그대로 호출하는 구조가 아니다. 두 relation의 producer만 아래처럼 바뀐다.

```text
Integrated Step 5:
  v2_active_doctrine       = 여전히 caller/orchestration EDB
  v2_stage_effect_target   = 이전 gate의 내부 derivation
  v2_principal_realization_truth = full chain의 내부 derivation
```

active doctrine activation 자체를 Step 5가 추론하지 않는다. host가 뒤 stage를 미리
target으로 선언해서도 안 되며, backend가 이전 gate로 다음 target을 내부 생성한다.

```text
eligible Elements TRUE       -> Unlawfulness target
Unlawfulness gate passes     -> Culpability target
Culpability gate passes      -> Punishability target
```

integrated effect truth의 exact expected-key는 다음과 같다.

```text
{ (instance, doctrine_ref)
  | doctrine_ref is caller-active
    AND authored_stage(doctrine_ref) is internally reached }
```

기존 `v2_stage_effect_result`는 실제로 도달한 target에 대해서만 한 행을 낸다.
host adapter는 이 정확한 reached-key 집합과 이전 gate를 대조하여 누락 stage를
`not_reached`로만 복원한다. `not_reached`를 legal state 문자열로 Scallop에 새로
넣지 않는다.

### 4.4 derivative principal truth

통합 실행에서는 Step 4의 EDB `v2_principal_realization_truth`를 caller가 다시
제공하지 않는다. 이는 full chain 결과에서 기존 `principal_realization_truth()`
규칙대로 derivation한다.

```text
TRUE     principal OffenseRealization이 존재
FALSE    completion=not_applicable, 또는 Elements/Unlawfulness gate=fails
UNKNOWN  completion=unresolved, non-punishable completion,
         Elements/Unlawfulness gate=unresolved, 또는 그 밖의 미확정 경우
```

derivative Elements provenance는 기존 두 항목만 사용한다:
`ParticipationDependencyObligation(mode)`와
`ParticipationRequirementObligation(mode)`.

## 5. typed adapter와 provenance 최소 계약

Step 5 adapter는 새 `ScallopResult` 같은 carrier를 만들지 않고, 검증된 query map을
기존 dataclass로 직접 재구성한다.

- Step 3 candidate/result row + static policy로 `CompletionResult`와
  `CompletionCandidateOutcome`을 복원한다.
- Elements stage는 기존 aggregate truth뿐 아니라 실제 fold에 포함된 각 obligation의
  truth를 받아 `ObligationOutcome`을 복원한다.
- Step 4 doctrine truth row에서 `truth != FALSE`인 것만 `AppliedEffect`로 복원하고,
  `modifier_ref`는 checked DoctrineDef manifest에서 join한다.
- 최초로 gate가 닫힌 지점만 `decisive_stage`로 기록한다.
- Elements의 FALSE obligation이 정확히 하나일 때만 `decisive_obligation`으로
  기록한다. 여러 개면 `None`이며 모든 항목은 provenance에 남긴다.
- `decisive_doctrine`을 위한 별도 판정 규칙은 만들지 않는다. UNKNOWN blocking을
  포함한 현재 Python `pipeline` reconstruction과 field-by-field parity를 요구한다.

### 5.1 폐쇄된 per-obligation truth query schema

현재 Step 2/3 aggregate query만으로는 `ObligationOutcome`을 재구성할 수 없다.
Step 5는 새 법적 abstraction이 아니라 기존 obligation의 injective 직렬화인 다음
closed query surface를 계약한다. `truth`는 모두 `TRUE | FALSE | UNKNOWN`이다.

```text
v2_elements_slot_obligation_truth(
  target_instance, slot, truth)

v2_elements_component_slot_obligation_truth(
  target_instance, component_local_key, slot, truth)

v2_elements_relation_obligation_truth(
  target_instance, occurrence_path, relation_ref, left_local_key, right_local_key, truth)

v2_completion_requirement_obligation_truth(
  target_instance, selected_completion_state, truth)
```

ordinary slot의 exact key set은 선택된 state에서 suspend되지 않은 고정 `SLOT_NAMES`
전체다. Art.339 component slot의 exact key set은 선택된 state의
`component_suspended_slots`와 global suspension을 제외한 각 direct offense-family
component의 `(local_key, SLOT_NAMES)` 전체다. 따라서 un-authored expression의
vacuous truth도 현재 Python provenance와 동일하게 행으로 남는다.

relation query의 key는 기존 `RuntimeRelationKey`를 손실 없이 직렬화하며 selected
state에서 `retain`된 obligation에만 존재한다. completion requirement row는 selected
state가 `additional_requirements`를 가질 때만 존재한다. suspended slot/relation은
TRUE로 대체하지 않으며 어떤 obligation row도 내지 않는다.

Article 33 constitutive-status obligation은 새 generic query로 중복하지 않는다.
기존 `v2_constitutive_status_truth(target, ref, truth)` 및
`v2_constitutive_status_true_instance(target, ref, member)`가 정확한 직렬화다.
그 exact key set은 co-principal target의 checked `constitutive_status_refs`이며,
true-member rows는 그 truth의 provenance다. status truth는 target의 새 `CaseTruths`
fact가 아니라 Python oracle과 동일하게 pre-Elements override 및
`CoPrincipalConstitutiveStatusObligation`으로 fold에 포함한다.

derivative는 generic query를 사용하지 않는다. 이미 존재하는
`v2_derivative_requirement_truth`와 내부 derived principal-realization truth가
각각 `ParticipationRequirementObligation`과
`ParticipationDependencyObligation`을 정확히 복원한다.

### 5.2 aggregate/provenance parity와 conclusion existence

host는 exact-key 검증 뒤 반드시 다음을 검증한다.

```text
direct/co-principal:
  fold_all(validated ordinary/component slot, retained relation,
           completion requirement, constitutive-status obligation truths)
  == validated completion-adjusted Elements truth

derivative:
  fold_all(validated principal-realization truth,
           validated derivative requirement truth)
  == validated derivative_elements_truth
```

결론 존재 조건도 기존 typed runtime과 정확히 묶는다.

```text
OffenseRealization exists
  iff Elements gate == passes AND Unlawfulness gate == passes

OffenseEstablishment exists
  iff OffenseRealization exists AND Culpability gate == passes

LiabilityResult exists
  iff OffenseEstablishment exists AND Punishability gate == passes
```

derivative의 `LiabilityEvaluation.completion`은 반드시 `None`이고, direct/co의
`completion`은 실제 `CompletionResult`다. 별도 liability verdict row나 새 carrier는
만들지 않는다. adapter는 현재 `runtime.stages.LiabilityResult`의 정확한 기존 fields로
구성하며, 기존 타입의 생성자 모양을 독자 계약으로 재정의하지 않는다.

## 6. 출력 검증

모든 query는 순서 없는 exact-key 집합으로 검증한다.

1. `ResultUniverse = Direct ⊎ Co ⊎ D`를 먼저 검증한다. component-scope-only instance는
   result row, participation endpoint, derivative principal이 될 수 없다.
2. direct/co 대상은 completion result 정확히 1개 및 candidate 완전 집합을 가진다.
   derivative 대상의 completion row는 없다.
3. eligible direct/co 대상 또는 derivative 대상은 evaluated Elements 결과 정확히 1개를
   가진다. completion에서 정지한 대상은 Elements row가 없다.
4. per-obligation row의 exact key set과 suspended-obligation 부재를 검증한 뒤 §5.2의
   `fold_all` invariant를 확인한다.
5. doctrine result/effect rows의 key 집합은 내부 stage gate가 만든 reached target과
   caller-active same-stage doctrine 집합에 정확히 일치한다.
6. not-reached stage에는 effect, legal state, gate state, stage-result row가 없다.
7. 모든 ResultUniverse instance는 하나의 `LiabilityEvaluation`으로 복원되며,
   conclusion optionality, decisive metadata, `LiabilityResult` 존재 여부는 현재 Python
   runtime과 field-by-field로 일치해야 한다.

중복, 누락, 예기치 않은 instance/route/stage/doctrine/obligation key, 잘못된 truth,
route 충돌, circular derivative link는 `ScallopBackendContractError`로 거부한다.

## 7. parity 검토 행렬

계약 승인 뒤 구현 전에 아래를 독립 test로 고정한다.

| 구간 | 필수 경우 |
|---|---|
| Completion stop | unresolved / not_applicable / punishable=False; 네 stage 모두 not_reached |
| Elements | TRUE/FALSE/UNKNOWN; 단일·복수 FALSE obligation 및 suspended obligation 부재 provenance |
| Unlawfulness | preserved, DEFEAT TRUE, DEFEAT UNKNOWN; 뒤 stage 정지 |
| Culpability | DEFEAT TRUE/UNKNOWN, MODIFY TRUE/FALSE/UNKNOWN; UNKNOWN MODIFY의 passes 유지 |
| Punishability | EXEMPT TRUE/UNKNOWN, MODIFY TRUE/FALSE/UNKNOWN; LiabilityResult 존재 조건 |
| Co-principal | target-scope `when`/slot/additional requirement/doctrine에 attribution 반영; component scope/relation에는 비전파 |
| Constitutive status | target/source TRUE-member provenance, pre-Elements override, aggregate fold 포함, target CaseTruths 비변형 |
| Derivative | principal TRUE/FALSE/UNKNOWN × own requires TRUE/FALSE/UNKNOWN; DAG 순서 및 full tail parity |
| Adapter | 모든 `not_reached`/결론 optionality/decisive metadata/provenance가 Python `LiabilityEvaluation`과 동일 |
| Determinism | 입력 순서·hash seed와 무관한 static program/EDB 및 unordered output validation |

## 8. 구현 전 승인 항목

다음 항목을 승인하기 전에는 `scallop_backend.py` 구현을 시작하지 않는다.

1. standalone Step 4 EDB contract와 integrated Step 5의 relation producer 분리.
2. `ResultUniverse = C ∪ D` partition, route exclusivity, derivative principal DAG.
3. Step 4 principal-realization EDB를 Step 5 derived relation으로 대체하는 경계.
4. 내부 stage-effect target gate, caller-active doctrine expected key, reached-row /
   `not_reached` 복원 방식.
5. target-only `effective_predicate`와 target-scoped additional requirement를 포함한
   co-principal attribution 범위.
6. injective closed per-obligation query schema, constitutive-status fold 및 aggregate
   Elements parity invariant.
7. 기존 runtime dataclass만 쓰는 typed adapter, conclusion existence, decisive metadata
   field parity 및 아래 Article 263 backend-completion gate.

## 9. Article 263 backend-completion gate와 명시적 비목표

이번 Step 5는 **generic liability-chain backend**로 한정한다. Step 7이 이미
고정한 Article 263 dedicated route는 Step 5에 억지로 포함하지 않는다.

별도 **backend-completion contract/step**은 Article 263 dedicated runtime path를
Scallop backend에 이행했고, 그 gate도 통과했다. 계약과 acceptance evidence는
[`STEP8_V2_SCALLOP_ARTICLE263_CONTRACT.md`](STEP8_V2_SCALLOP_ARTICLE263_CONTRACT.md)에
고정했다. 이 선택은 새 participation mode, 새 `offense_ref=263`, co-principal
attribution, 또는 새 legal abstraction을 허용하지 않으며 Step 7의 기존 route 계약만
보존한다.

Article 34 indirect principal 및 Article 151의 별도 statutory route lowering은 계속
Step 5 비목표다. 구현, native Scallop 실행, 모델 호출, Call 2 factual v0 변경,
Step 7 재검토, Definition Layer 수정, Call 3 writer 연결도 포함하지 않는다.
