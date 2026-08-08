# Current handoff

기준: 2026-08-08 · 브랜치 `deadline_v2_0808` · 데드라인 **2026-08-19 21:00**(1주 연장)

## Step 3 (Expression evaluator) 완료 — `src/idpr/v2/evaluate.py` + 23개 테스트 통과 (2026-08-08, 같은 세션)

26절 구현 순서 3번 "Expression evaluator"를 끝냈다. **다음 세션 시작점은 이제 4번
"QUALIFY / COMPOSE compiler"다.** 승인된 구현 계획서는
[`/home/jaehoonjeong/.claude/plans/polished-conjuring-turing.md`](file:///home/jaehoonjeong/.claude/plans/polished-conjuring-turing.md).

**스키마 변경 없음** — step 2(5차 addendum)와 달리 이번 단계는 `element_expression`
문법을 건드리지 않았다. `SCHEMA_NOTES.md` 업데이트 없음.

`src/idpr/v2/evaluate.py`: `TruthValue = Literal["TRUE","FALSE","UNKNOWN"]` +
`evaluate(expr: CanonicalExpr, truths: Mapping[str, TruthValue]) -> TruthValue`.
`expressions.py`의 `CanonicalExpr`(step 2에서 이미 구현된 canonicalize 출력)를 그대로
입력으로 받는다 — 두 번째 tree-walker를 새로 만들지 않고 step 2가 이미 세운 계약
(`replay_slot`이 `CanonicalExpr`를 반환, `check_operators`가 비교 전 `canonicalize` 호출)을
재사용. `None`(빈 slot) → `TRUE`(vacuous truth), 누락된 ref → `UNKNOWN`(4.3 invariant —
missing evidence is not negation). ALL/ANY/NOT은 v2.2.0 문서 12절의 3치 진리표를 그대로
구현.

**ONE_OF의 3치 의미론 — 문서에 없어 이번에 확정한 설계 결정** (v2.1.0/v2.2.0 어디에도
ONE_OF의 truth table이 없음, 사용자에게 명시적으로 질의 후 확정):

```text
true_count = TRUE인 자식 수
unknown_count = UNKNOWN인 자식 수

true_count >= 2      → FALSE   (이미 2개 이상 참이면 어떤 completion으로도 못 고침)
unknown_count == 0   → true_count == 1이면 TRUE, 아니면 FALSE
그 외                 → UNKNOWN
```

ALL/ANY/NOT과 동일한 원리("모든 completion에서 같은 결론이면 확정, 아니면 UNKNOWN")를
ONE_OF의 "정확히 하나"(8.3절) 명제에 그대로 적용한 것 — "자식 중 UNKNOWN이 하나라도 있으면
무조건 UNKNOWN"이라는 더 무딘 규칙보다 정밀함(예: `ONE_OF(TRUE, TRUE, UNKNOWN)`은 이미 2개
참이라 세 번째 값과 무관하게 `FALSE`로 확정).

**중요한 경계 — truth-functional, leaf-joint 아님**: 이 completion은 각 자식의 *이미
평가된* `TruthValue`에 대한 completion이지, 그 자식들이 참조하는 leaf ref 자체에 대한 joint
completion이 아니다. `evaluate()`는 각 자식을 독립적으로 평가한 뒤 그 결과값만 보고 fold한다
— 형제 자식들이 같은 leaf ref를 공유하는지 들여다보지 않는다(ALL/ANY/NOT도 동일한 원칙).
결과: `ONE_OF(A, NOT(A))`에서 `A = UNKNOWN`이면 `UNKNOWN`으로 평가된다(leaf-joint 분석을
했다면 `A`의 모든 completion에서 `A`/`NOT(A)` 중 정확히 하나가 참이므로 `TRUE`라고 판단했을
것과 다름). 사용자가 직접 지정한 경계이며, `test_v2_evaluate.py::
test_one_of_is_truth_functional_not_leaf_joint`로 회귀 고정.

`tests/test_v2_evaluate.py`(23개 테스트, `/data5/jaehoonjeong/miniconda3/bin/python`
미니콘다 base 환경) — ALL/ANY/NOT 진리표, ONE_OF 6가지 조합 + 계획서의
`ONE_OF(A, ONE_OF(B,C))` vs `ONE_OF(A,B,C)` 반례를 evaluation 레벨에서 재확인, 위 경계
회귀 테스트, 누락 ref 기본값, 빈 slot vacuous truth, `canonicalize`의 ALL/ANY flatten이
evaluate 결과를 바꾸지 않음(flatten-safety), nested mixed-operator 통합 테스트. 전체
`tests/test_v2_*.py` 92개 전부 통과(기존 69 + 신규 23).

## Step 2 (Type checker) 완료 — 스키마 addendum 5차 수정 + `src/idpr/v2/` 구현 + 69개 테스트 통과 (2026-08-08, 같은 세션)

26절 구현 순서 2번 "Type checker"를 끝냈다. **다음 세션 시작점은 이제 3번
"Expression evaluator"다.** 승인된 구현 계획서는
[`/home/jaehoonjeong/.claude/plans/modular-seeking-glade.md`](file:///home/jaehoonjeong/.claude/plans/modular-seeking-glade.md)
(총 6라운드 조건부 승인 끝에 확정), 스키마 근거는
[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)의
"Type checker 설계 중 발견된 추가 스키마 결함" 절.

### 스키마 addendum (Phase 0, 5차 수정)

Type checker 설계를 시작하자마자 스키마 자체에 5개 결함이 더 있다는 게
드러나 5라운드 재검토 끝에 확정, 전부 반영·재검증 완료(36개 인스턴스 그대로,
부정 케이스 11개 신규 확인):

- `component_ref`에 composition-local `local_key` 필수 추가, `slot`(단수,
  primitive/exported_component)과 `placement`(맵, bundle — 여러 predicate를
  여러 slot에 나눠 붙일 수 있어야 하므로)를 kind별로 분리.
- `compose.relations`를 bare id 배열에서 `[{relation, left, right}]`(left/right는
  `local_key`)로 재구성 — 어떤 두 컴포넌트를 잇는 relation인지 이제 명시적.
- `OffenseDef.element_modules`를 `[{ref, placement}]`로 재정의 — bare id
  목록(죽은 metadata)이 아니라 실제 실행 의미를 갖는 attachment로.
- `ExportedComponentDef`는 `source_offense.exports[export_key]`로 완전히
  resolve 가능함을 재확인(compiler-only 아님) — Type checker가 이걸 활용하는
  공용 `resolve_export` 리졸버를 `registry.py`에 둔다.
- `element_expression` leaf 허용 kind(`ground_fact|legal_element`만)와
  `LegalElementDef.grounded_by` 허용 kind(`ground_fact`만)를 미검증
  allowance 제거로 축소.

### `src/idpr/v2/` 구현 (Phase 1)

`schema.py`(referencing.Registry 기반 구조 검증), `expressions.py`(element_expression
tree walk + canonicalize/combine_all), `registry.py`(스키마 검증 + id 인덱스 +
`resolve_export`), `findings.py`(`Finding`/`TypeCheckError`), `checks/`
아래 6개 축(`references`/`operators`/`stage_effect`/`exports`/`participation`/
`derivation`). `tests/test_v2_*.py` 9개 파일, **69개 테스트 전부 통과**
(미니콘다 base 환경, `/data5/jaehoonjeong/miniconda3/bin/python` — `.venv`
아님). 실제 36개 인스턴스 corpus는 6축 전부 0 findings.

axis 2(operator typing)의 핵심 불변식: `flattened_elements`는 최종
top-level 비교(`check_operators`의 actual side, `operators.py` 단 한 줄)에서만
읽고, 다른 entry의 기대값을 계산할 때는 (그 entry가 `DerivedOffenseDef`이더라도)
항상 그 entry 자신의 `derivation`을 재귀적으로 다시 replay(`replay_slot`,
memoized + cycle-safe)한다 — 계획서 라운드 4/5/6이 이 지점의 실수를 세 번
교정했고, 구현 중 `grep flattened_elements src/idpr/v2/`로 재확인함(읽는
곳은 `operators.py`의 actual-side 한 줄과 `references.py`가 그 필드 자체의
참조 무결성을 구조적으로 검사하는 한 곳, 총 두 곳뿐 — 후자는 axis1의
독립적인 관심사라 불변식 위반이 아님).

**구현 중 실제로 잡힌 버그**: COMPOSE의 `kind=primitive` 컴포넌트를 replay할
때 처음엔 `PrimitiveDef` 자신의 id를 그대로 leaf ref로 썼는데, 실제로는 그
`PrimitiveDef.ref`(감싸고 있는 실제 predicate)로 resolve해야 했다 — 스키마
상으로는 멀쩡하지만 실행 의미가 틀린 전형적 사례, Type checker가 정확히
이런 걸 compiler 이전에 잡으려고 존재하는 단계라는 걸 보여주는 사례.

### DEFERRED BY DESIGN (버그 아님, 의도적 유예 — 나중에 재발견하지 말 것)

- **`RelationDef.left_type`/`right_type` ↔ bound component의 semantic type
  일치 검증** — `local_key` 덕분에 relation이 "어느 두 컴포넌트를 잇는지"는
  이제 정확히 알지만, 어느 component(`GroundFactDef`/`OffenseDef`/
  `ExportedComponentDef` 등)도 `RelationDef.left_type`/`right_type`과 비교할
  semantic type 자체를 선언하지 않는다. → **compiler/relation evaluator
  (26절 순서 4/5) 설계 시점에 다시 열 것.**
- **`modifier_ref` → 실제 `ModifierDef` 존재 확인** — `ModifierDef` 객체
  자체가 아직 설계되지 않았음(Open Question #4, v2.1.0 문서 25절). 지금은
  `modifier_ref` 재사용 시 stage 일관성만 self-consistency로 검사. →
  **`ModifierDef` 설계 시점에 다시 열 것.**

이 둘은 스키마 결함이 아니라 "아직 그 대상 객체/타입 vocabulary가 존재하지
않아서" 생기는 자연스러운 경계다.

## Step 1 스키마 재검토 반영 완료 — 4개 수정 + 3개 확정 + fixture 26→36개 (2026-08-08, 새 세션)

사용자가 `SCHEMA_NOTES.md`를 검토하고 Type checker(2번) 착수 전에 고칠 지점을
지적 — 전부 반영 완료, 재검증 통과. 상세 근거는
[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)의
"2026-08-08 재검토" 절.

- **수정 1**: `ParticipationPolicyDef`를 offense-keyed(`{id, offense, modes}`)에서
  shared/global(`{id, modes}`)로 바꿈 — 공범론은 범죄마다 반복 연결하는 게 아니라
  General Part로 공유. offense별 제한이 필요할 때만
  `OffenseDef.participation_constraints`(옵션)로 좁게 override. 또한
  `derivative_mode.requires_conclusion`을 자유 enum(3택1)에서
  `offense_realization` const로 고정 — 15.3의 typed dependency 불변식을
  type checker가 아니라 definition language 자체에서 틀리게 쓸 수 없게 함.
- **수정 2**: `MODIFY.modification`(자유 문자열) → `modifier_ref`(symbolic id) +
  `note`(설명, 런타임 비소비)로 분리. 자유 문자열 MODIFY는 symbolic runtime이
  해석 불가능해서 effect algebra의 목적 자체를 깼기 때문.
- **수정 3**: `ExportedComponentDef.resolved_ref` 필드 완전 제거 — 이건
  `DerivedOffenseDef.flattened_elements`와 같은 성격의 컴파일러 캐시라 Definition
  YAML에 사람이 손으로 쓰면 두 번째 진실 소스가 생김. Compiled IR(step 4) 전용.
- **수정 4**: `OffenseDef.composition_metadata` 필드 제거 — 컴파일러 미존재,
  fixture 어디에도 안 쓰임, placeholder를 스키마에 남겨둘 이유 없음.
- **확정 A**: `element_expression`은 canonical schema에서 이미 문법이 하나뿐임을
  재확인(flat-list "implicit ALL"은 JSON Schema branch가 아니라 저작 단계
  normalize로만 처리하기로).
- **확정 B**: 전체 13개 스키마 파일의 `$id`/`$ref`를 `idpr/v2/<Name>`에서
  `https://schemas.idpr.local/v2/<Name>` absolute URI로 전환.
- **확정 C**: `authority_basis` enum은 provisional 유지 — compiler semantics에
  영향을 주게 되는 순간 별도 설계 절을 먼저 연다는 원칙만 기록, 스키마 변경 없음.
- **fixture**: section 20.1(진정신분범, `offense.bribery_taking`)과
  20.4(composite offense + statutory nexus, `derived_offense.robbery_rape` +
  `relation.occasion_identity`)를 신규 추가. MODIFY의 새 모양을 실제로
  exercising하는 `doctrine.diminished_capacity`도 추가(이전엔 MODIFY fixture가
  전무했음). 결과 26 → **36개 인스턴스**, 검증 통과. 부정 케이스도 3개 →
  **8개**로 확장(새 필드 모양들이 실제로 옛 값을 거부하는지 확인).

## Step 1 (Definition schema) 완료 — JSON Schema 12개 + YAML fixture 26개 검증 통과 (2026-08-08, 같은 세션)

26절 구현 순서 1번 "Definition schema"를 끝냈다. **다음 세션 시작점은 이제 2번
"Type checker"다.**

- `docs/contracts/v2/common.schema.json` + Definition Layer 객체별 스키마 12개
  (`ground_fact_def`/`legal_element_def`/`primitive_def`/`element_bundle_def`/
  `exported_component_def`/`offense_def`/`derived_offense_def`/`doctrine_def`/
  `qualifier_def`/`relation_def`/`completion_policy_def`/`participation_policy_def`
  `.schema.json`) 작성 완료. JSON Schema(draft 2020-12)로 구조 검증, `$id`
  기준 cross-file `$ref`.
- 사람이 직접 저작하는 정의 파일은 **YAML**(사용자 결정) — 스키마 파일 자체는
  JSON Schema 그대로.
- `docs/contracts/v2/examples/*.yaml` 12개 파일·26개 인스턴스로 `jsonschema`
  검증 통과. section 20 validation case 중 20.2(부진정신분범)/20.3(결과적
  가중범)/20.5(미수범)/20.6·20.7(공동정범·교사범)을 실제 fixture로 exercising.
  부정 케이스 3개(v1식 `role`/`card_role` 필드 삽입, DoctrineDef stage/effect.stage
  불일치)도 실제로 거부되는 것 확인 — 특히 `role: "bar"`를 아무 v2 스키마에
  넣어도 `additionalProperties: false`가 구조적으로 막는다는 게 핵심 검증
  포인트(v1 극성 버그 재발 방지가 이번 개편의 목적이었으므로).
- 문서에 문법이 없어 이번에 확정한 판단 8가지(`PrimitiveDef`/`ExportedComponentDef`/
  `ParticipationPolicyDef` 모양, `element_expression`을 모든 요건 자리에 통일해서
  쓰기로 한 것 등) 전부 **[`docs/contracts/v2/SCHEMA_NOTES.md`](../contracts/v2/SCHEMA_NOTES.md)에
  근거와 함께 기록**. ~~다음 세션 시작 전에 검토할 것.~~ **이 검토는 끝났다 —
  위 "Step 1 스키마 재검토 반영 완료" 절 참고. `SCHEMA_NOTES.md`는 더 이상
  열린 검토 대상이 아니라 확정된 기록.**

### 다음 세션 시작점 — Type checker (26절 2번) [완료됨 — 위 "Step 2 완료" 절 참고]

**이 절은 역사적 기록이다. 여기서 예고한 Type checker는 같은 세션 안에서
바로 이어서 구현 완료됨 — 다음 세션 시작점은 이제 3번 Expression evaluator
(문서 최상단 절 참고).**

`docs/contracts/v2/*.schema.json`이 잡아주는 건 **구조(모양)뿐**이다. 아직
검증되지 않은 것: 15.4가 요구하는 typed dependency 체크("교사는
`OffenseRealization<X>`을 요구하는데 실제로는 `ElementsResult<X>`만 있으면
TYPE ERROR" — participation_policy_def.schema.json이 `requires_conclusion`을
`offense_realization` const로 고정해뒀지만, 실제 사건에서 정범이 도달한 게
`OffenseRealization`인지 아닌지 판정하는 건 여전히 type checker의 일), `NOT`이
unresolved/missing evidence를 satisfaction으로 바꾸지 않는다는 4.3의 invariant,
id 참조 무결성(예: `OffenseDef.qualifiers`에 적힌 id가 실제 존재하는
`QualifierDef`인지, `ExportedComponentDef.export_key`가 `source_offense`의
`exports` 맵에 실제 존재하는지 등) 등 — 전부 구조 스키마가 아니라 별도 Python
코드가 담당해야 하는 **의미 타입체크**다. `src/idpr/v2/`(신규 패키지, v1
코드는 그대로 둔다) 아래에 구현할 것으로 예상. **스키마 재검토가 끝났으므로
다음 세션은 SCHEMA_NOTES.md를 다시 검토할 필요 없이 바로 Type checker 설계에
착수하면 된다.**

## v2 킥오프 — v1 동결, DSL 대개편 착수 (2026-08-08, 새 세션)

**사용자 결정: v1(article/unit-centric RuleIR)을 reproducible baseline으로 동결하고,
`deadline_v2_0808` 브랜치에서 v2 DSL로 대대적 개편을 시작한다.** 데드라인이 8/11에서
8/19 21:00으로 1주 늘어난 게 계기. 핵심은 v1에서 반복적으로 터진 문제(이 문서 아카이브본
전체가 그 기록이다) 하나하나를 땜질하는 대신, 애초에 그런 버그가 나올 수 없는 **규격화된
형법 DSL**을 만드는 것.

### 브랜치/커밋 상태

- `main`이 `antigravity-0804`를 fast-forward merge해 `0268635`를 가리킴 — v1의 최종
  상태(assess 프롬프트 극성 버그 A+B+C 수정 + homicide art250_sec1_15 카드 role 정정까지
  전부 포함).
- `deadline_v2_0808`는 그 `main`(`0268635`)에서 분기. 지금부터 이 브랜치가 v2 작업 공간.
- `antigravity-0804` 로컬 브랜치는 아직 정리 안 됨(main과 동일 커밋이라 그대로 둬도 무해).
- v1의 이전 `CURRENT.md`(1442줄, 극성 버그 포렌식·라우팅 버그 해결·judge 재설계 등 전체
  경위)는 [`docs/archive/history/2026-08-08_v1_final_handoff_pre_v2_dsl.md`](../archive/history/2026-08-08_v1_final_handoff_pre_v2_dsl.md)에
  그대로 보존. **v1 관련 세부 경위가 필요하면 이 파일을 볼 것 — 지금부터 이 CURRENT.md는
  v2 전용으로 리셋한다.**

### v2 설계 문서 — 필독

- [`docs/v2_plan/IDPR_v2.1.0_DESIGN_PROPOSAL.md`](../v2_plan/IDPR_v2.1.0_DESIGN_PROPOSAL.md)
  — **지금 볼 문서.** Definition Language → Typed Legal IR → Scallop → Case Runtime
  4단 분리, canonical positive predicate, `bar`/`waiver`/`boundary`/`component` 같은
  neural-visible legal-effect role 전면 폐기, `QUALIFY`/`COMPOSE`/`PROJECT` definition-time
  constructor, `DEFEAT`/`MODIFY`/`EXEMPT`/`ATTRIBUTE` runtime effect, Completion/Participation을
  orthogonal runtime axis로 분리하는 게 골자.
- [`docs/v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md`](../v2_plan/IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md)
  — **지금 착수 안 함.** v2.1.0이 정한 typed legal program을 사건에 적용하는 3-call
  runtime(Call1 high-recall routing → Call2 GroundFact grounding → Call3 LegalElement
  assessment → lean symbolic execution). v2.1.0 freeze 이후에 다시 열 것.

핵심 원칙 한 문장(v2.1.0 문서 그대로): **"Neural models may ground facts and evaluative
legal elements. They may not assign legal effects."** — v1에서 반복된 극성 버그(카드
role이 neural assessment에 노출되며 판단이 뒤집히는 문제, 이번 세션 직전까지 homicide/
obstruction/harboring_offender 등에서 손으로 하나씩 잡던 바로 그 패턴)의 근본 원인을
아키텍처 레벨에서 차단하려는 설계다.

### 구현 순서 (26절) — 1~3번 완료, 지금은 4번부터

v2.1.0 문서 26절 "Proposed Implementation Boundary"의 권장 순서를 그대로 따른다.
**1번(Definition schema), 2번(Type checker), 3번(Expression evaluator) 완료 — 위 "Step 3
완료"/"Step 2 완료"/"Step 1 완료" 절과 `docs/contracts/v2/SCHEMA_NOTES.md` 참고. 다음은
4번(QUALIFY / COMPOSE compiler)부터.**

```text
1. Definition schema   [완료]
2. Type checker         [완료]
3. Expression evaluator [완료]
4. QUALIFY / COMPOSE compiler   ← 다음 시작점
5. Relation evaluator
6. Runtime stage objects
7. Completion resolution
8. Participation / attribution
9. Scallop compilation
10. Neural grounding adapters
11. Writer integration
```

**1번 "Definition schema"의 구체 내용**: 22절 "Proposed v2.1.0 Object Inventory"에 나열된
Definition Layer 객체들(`GroundFactDef`, `LegalElementDef`, `PrimitiveDef`,
`ElementBundleDef`, `ExportedComponentDef`, `OffenseDef`, `DerivedOffenseDef`,
`DoctrineDef<S>`, `QualifierDef`, `RelationDef<A,B>`, `CompletionPolicyDef`,
`ParticipationPolicyDef`)의 실제 JSON/YAML 문법을 확정하는 게 첫 작업 — 25절 "Open
Questions After v2.1.0"의 1번("각 schema의 실제 JSON/YAML 문법")과 정확히 같은 항목.
6~8절(Fixed Offense Slots, Shared Element Modules, Element Expression Grammar)과 9절
(QUALIFY/COMPOSE/PROJECT)의 구조를 스키마로 얼마나 정확히 반영하는지가 이후 type
checker/compiler 단계 전체의 기반이 된다.

**착수 전 참고**:
- 24절 "Acceptance Criteria for v2.1.0 Freeze"가 이 트랙 전체의 완료 기준. 스키마
  설계 단계에서부터 이 기준(특히 "Type system"·"Predicate semantics" 항목)을 염두에
  둘 것.
- 21절 "Migration Principles from v1" — v1 카드를 그대로 v2 predicate로 옮기지 않는다.
  `v1 cards → semantic normalization → GroundFactDef/LegalElementDef/DoctrineDef/
  RelationDef → deduplication → shared predicate registry → OffenseDef assembly` 순서를
  지킬 것. 특히 `component`/`bar`/`waiver`/`boundary` role은 v2에서 neural-visible
  semantics로 유지하지 않는다 — 각 카드의 실제 법적 의미를 normalized predicate/element
  module/doctrine/qualifier/relation/completion condition/participation condition/
  punishability effect/post-offense relation 중 하나로 재분류해야 한다.
- v1의 실제 자산(RuleIR unit, norm card set, 승인 원장 등)은 `main`/`antigravity-0804`
  (`0268635`)와 이 브랜치 양쪽에 그대로 남아 있다 — migration 원료로 참고하되, 구조를
  그대로 이식하지 않는다.
- v1 아키텍처 문서(`docs/handoff/DESIGN.md`, `docs/handoff/RECOVERY.md`,
  `docs/handoff/RULEIR_RISKS.md`)는 article/unit-centric RuleIR 시절 기록이라 v2
  설계와 전제가 다르다. 참고는 가능하지만 v2 스키마 설계의 근거로 직접 인용하지 말 것.

### 미해결 (v2.1.0 문서 25절, 설계 진행하며 순차 확정)

스키마 문법(위 1번)을 제외한 나머지 11개는 이후 단계에서 확정한다: `ElementAssessment`
status representation, probability 도입 layer, `MODIFY` payload taxonomy, 양형 포함
범위, 죄수론/post-offense relation algebra, 대향범·집합범·합동범 actor-structure,
상습범·포괄일죄 연결, 예비·음모 CompletionPolicy, 판례/법률 reference authority schema,
routing activation scope 단위, alternative legal trace 포함 여부, 개별 조문·doctrine
법률 검수. **프롬프트 승인 게이트는 v2에서도 동일하게 적용** — 특히 향후 neural grounding
adapter(v2.2.0 대상) 프롬프트는 설치 전 사용자 승인 필요.
