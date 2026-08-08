# Current handoff

기준: 2026-08-08 · 브랜치 `deadline_v2_0808` · 데드라인 **2026-08-19 21:00**(1주 연장)

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
  근거와 함께 기록** — 다음 세션 시작 전에 검토할 것. 사용자가 다르게 정하고
  싶은 항목이 있으면 여기서부터 뒤집으면 된다.

### 다음 세션 시작점 — Type checker (26절 2번)

`docs/contracts/v2/*.schema.json`이 잡아주는 건 **구조(모양)뿐**이다. 아직
검증되지 않은 것: 15.4가 요구하는 typed dependency 체크("교사는
`OffenseRealization<X>`을 요구하는데 실제로는 `ElementsResult<X>`만 있으면
TYPE ERROR"), `NOT`이 unresolved/missing evidence를 satisfaction으로 바꾸지
않는다는 4.3의 invariant, id 참조 무결성(예: `OffenseDef.qualifiers`에 적힌
id가 실제 존재하는 `QualifierDef`인지) 등 — 전부 구조 스키마가 아니라 별도
Python 코드가 담당해야 하는 **의미 타입체크**다. `src/idpr/v2/`(신규 패키지,
v1 코드는 그대로 둔다) 아래에 구현할 것으로 예상되나 구체 설계는 다음 세션
시작 시 `SCHEMA_NOTES.md`를 먼저 검토한 뒤 진행.

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

### 구현 순서 (26절) — 1번 완료, 지금은 2번부터

v2.1.0 문서 26절 "Proposed Implementation Boundary"의 권장 순서를 그대로 따른다.
**1번(Definition schema)은 완료 — 위 "Step 1 완료" 절과 `docs/contracts/v2/
SCHEMA_NOTES.md` 참고. 다음은 2번(Type checker)부터.**

```text
1. Definition schema   ← 여기부터 시작
2. Type checker
3. Expression evaluator
4. QUALIFY / COMPOSE compiler
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
