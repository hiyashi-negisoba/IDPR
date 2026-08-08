# v2.1.0 Definition Schema — implementation notes

이 문서는 `docs/contracts/v2/*.schema.json`(step 1, Definition schema)을 작성하며
`IDPR_v2.1.0_DESIGN_PROPOSAL.md`가 문장/의사코드로만 남겨두고 실제 문법을 정하지
않은 지점들을 어떻게 메꿨는지 기록한다. 전부 **검토 대상** — 사용자가 다르게
정하고 싶으면 여기 나열된 판단 하나하나를 뒤집으면 된다.

## 레이아웃

- `docs/contracts/v2/*.schema.json` — JSON Schema(draft 2020-12), 구조 검증기.
  v1의 `docs/contracts/rule_ir.schema.json` 관례(엄격한 `additionalProperties: false`,
  id 패턴, `$defs` 재사용)를 그대로 따랐다.
- `docs/contracts/v2/common.schema.json` — 다른 모든 스키마가 `$ref`로 끌어쓰는
  공유 `$defs`(element_expression 트리, DEFEAT/MODIFY/EXEMPT effect algebra, stage
  enum, source_ref/authority_ref, participation enum 등). 각 파일의 `$id`는
  **absolute URI** `https://schemas.idpr.local/v2/<Name>` 형태이고(2026-08-08
  재검토로 상대 경로 `idpr/v2/<Name>`에서 전환 — 아래 "확정 B" 참고),
  cross-file `$ref`는 파일명이 아니라 이 `$id`를 기준으로 한다(예:
  `"$ref": "https://schemas.idpr.local/v2/common#/$defs/id"`) — 실제로
  네트워크에서 fetch하지 않고, validator가 이 URI를 로컬 스키마 파일에
  매핑하는 registry/store로 등록해야 relative resolve가 된다. 실제 등록/검증
  예시는 아래 "검증" 절 참고.
- `docs/contracts/v2/examples/*.yaml` — 사람이 직접 저작하는 실제 정의 파일은
  **YAML**(사용자 결정, JSON보다 중첩된 ALL/ANY/QUALIFY/COMPOSE 구조를 읽고 쓰기
  편함). 확장자만 다를 뿐 파싱하면 JSON Schema와 동일한 구조이므로 스키마
  검증기는 그대로 재사용된다.

## 판단이 필요했던 지점 (문서에 문법이 없어 여기서 확정)

1. **`element_expression`을 모든 "요건 목록" 자리에 통일해서 씀.** 8절은
   `OffenseDef` slot에 ALL/ANY/NOT/ONE_OF 트리를 요구하는데, 7절(`negligence_bundle`
   등)과 11절(`self_defense` 등)의 예시는 단순 나열(flat list)로 보인다. 이걸
   "번들/doctrine은 더 단순한 별도 문법"으로 읽지 않고, **flat list를 같은
   `element_expression` 문법의 암묵적 ALL 축약형**으로 통일했다 — `ElementBundleDef.
   requires`, `DoctrineDef.requires`, `OffenseDef.elements.*`, `QualifierDef.
   additions.*`가 전부 같은 트리 문법을 쓴다. 요건 표현 문법이 레이어마다 갈라지는
   것보다 하나로 통일하는 쪽이 컴파일러(step 4) 입장에서도 유리하다고 판단.
2. **`PrimitiveDef`의 모양.** 9.2절이 `ComponentDef := PrimitiveDef | ElementBundleDef
   | ExportedComponentDef | OffenseDef`라고만 하고 `PrimitiveDef` 자체는 정의하지
   않는다. `COMPOSE`의 `components` 목록에서 "단일 atomic predicate를 그대로
   쓰는 경우"의 태그된 참조로 해석해 `{id, ref, ref_kind: ground_fact|legal_element}`
   로 정의했다. `OffenseDef` slot 내부의 `element_expression.ref`는 이 래퍼를
   거치지 않고 `GroundFactDef`/`LegalElementDef` id를 직접 참조한다 — `PrimitiveDef`는
   오직 `COMPOSE` component 목록 안에서만 쓰인다.
3. **`ExportedComponentDef`의 모양.** `PROJECT`는 "구조적 유틸리티"(9.3절)일
   뿐이지만 22절이 이걸 별도 Definition Layer 객체로 나열해서, 계산 결과를
   `{id, source_offense, export_key, resolved_ref}`로 명시적으로 직렬화했다 —
   18절의 provenance 보존 원칙을 이 객체에도 적용.
4. **`DerivedOffenseDef.flattened_elements`는 캐시, `derivation`이 provenance.**
   18절 예시가 `derivation`과 `flattened_elements`를 나란히 보여주는데,
   `derivation`이 이미 컴포넌트를 id로 참조하므로 그 자체가 provenance path다.
   `flattened_elements`는 컴파일러(step 4)가 `derivation`에서 재생성하는 산출물로
   취급 — 두 필드가 독립된 진실 소스가 아니다.
5. **`ParticipationPolicyDef`의 모양.** ~~22절이 이 이름만 나열하고 15절은
   런타임 객체(`ParticipationResult`, 15.4)만 상세히 설명한다. 15.4의 typed
   dependency 개념을 정의 시점 정책으로 그대로 옮겨
   `{id, offense, modes: {...}}`로 설계했었다.~~ **2026-08-08 재검토로 뒤집힘 —
   아래 "2026-08-08 재검토" 절 참고.** 이제 `{id, modes}`(offense 필드 없음, 공유
   General Part 정의)이고, `requires_conclusion`은 자유 enum이 아니라
   `offense_realization` 고정.
6. **provisional로 남긴 필드(문서가 스스로 미해결이라고 밝힌 부분, 25절)**:
   `authority_ref.authority_basis` enum(open question #10, 여전히 provisional
   — 아래 재검토에서 유지 결정), ~~`MODIFY.modification`을 자유 문자열로~~
   **2026-08-08 재검토로 `modifier_ref`(참조) + `note`(설명)로 분리** (open
   question #4), `CompletionPolicyDef`의 `punishability_note`를 자유 문자열로
   (open question #5, 재검토에서 그대로 유지 — 이유는 아래).
7. **`DoctrineDef.stage`와 `effect.stage` 일치 강제.** 문서엔 명시적 언급이
   없지만 12절 stage별 effect 표(DEFEAT는 unlawfulness/culpability만, MODIFY는
   culpability/punishability만, EXEMPT는 punishability만)를 실제로 지키게
   `if/then`으로 스키마 레벨에서 강제했다.
8. **`OffenseDef.composition_metadata`는 의도적으로 미확정(빈 object 허용).**
   ~~22절이 필드 이름만 나열, 아직 컴파일러가 없어 실제로 뭐가 필요한지 모른다 —
   억지로 타입을 지어내지 않았다.~~ **2026-08-08 재검토로 필드 자체를 스키마에서
   제거** — 아래 참고.

## 2026-08-08 재검토 (Type checker 착수 전 4개 수정 + 3개 명시적 확정)

사용자가 이 문서를 검토하고 Type checker(section 26 순서 2번)로 넘어가기 전에
아래 4개를 고치고 3개를 명시적으로 확정하기로 결정. 근거는 각 항목에 남긴다.
전부 `docs/contracts/v2/*.schema.json` + `docs/contracts/v2/examples/*.yaml`에
반영 완료, 재검증 통과(아래 "검증" 절 갱신본 참고).

### 수정 1 — `ParticipationPolicyDef`를 offense-keyed에서 shared/global로

기존 `{id, offense, modes}`는 범죄마다 공범구조를 반복 연결하게 만들어, 애초
"공범론을 shared General Part structure로 둔다"는 의도와 어긋난다. 지금은
`{id, modes}`(offense 필드 없음)로 바꾸고, 정말 특정 범죄가 공범형태에 제한을
갖는 경우에만 `OffenseDef.participation_constraints`(옵션, `disabled_modes`/
`attributable_slots` 두 필드만)로 좁게 override하게 했다. 보통의 범죄는 아무
것도 안 씀 — `examples/participation_policies.yaml`의
`participation_policy.standard`가 이 기본 정책이고, `offense.robbery`는
override 없이 그대로 쓴다.

또한 `derivative_mode.requires_conclusion`을 `conclusion_type`(3개 값 중
자유 선택) enum에서 **`offense_realization` const로 고정**했다. 15.3이 명시하는
"교사/방조는 정범의 개인적 책임조각과 무관하게 offense_realization만 요구한다"는
불변식을 type checker가 나중에 검증할 대상이 아니라, definition language
자체에서 틀리게 쓸 수 없게 만드는 쪽을 택했다 — 자유 enum으로 뒀으면
`instigator requires liability_result`처럼 15.4가 TYPE ERROR로 잡아야 할
바로 그 실수를 스키마가 "정상 definition"으로 승인해버렸을 것이다. 실제
反례가 나오면 이건 그때 가서 v2.1.0 grammar 변경(새 open question)으로 다룬다.

### 수정 2 — `MODIFY.modification`(자유 문자열) → `modifier_ref` + `note`

`MODIFY<S, "책임이 다소 줄어듦">`류가 구조적으로 valid하면 symbolic runtime이
해석할 방법이 없다 — DEFEAT/MODIFY/EXEMPT를 executable typed effect로 만들려던
목적 자체를 깨뜨린다. `common.schema.json`의 `modify_effect`를
`{effect, stage, modifier_ref, note?}`로 바꿨다 — `modifier_ref`는
`modifier.culpability.diminished` 같은 symbolic id(다른 id들과 동일한
`$defs/id` 패턴), `note`는 사람이 읽을 설명(예: 법조문 인용)이고 런타임은
`note`를 절대 소비하지 않는다. `ModifierDef`의 세부 타입(파라미터 등)은 여전히
Open Question #4로 남겨둔다 — 지금 고정한 건 "MODIFY는 참조를 갖는다"는 것뿐,
그 참조가 가리키는 대상의 스키마는 아직 안 만들었다.
`examples/doctrines.yaml`에 `doctrine.diminished_capacity`(심신미약, 형법
제10조 제2항)를 새로 추가해 이 모양을 실제로 exercising한다 — 이전 fixture
세트엔 MODIFY 사례가 아예 없었다.

### 수정 3 — `ExportedComponentDef.resolved_ref` 제거 (컴파일 IR 전용으로)

`source_offense` + `export_key`가 실제 source of truth이고, `resolved_ref`는
`DerivedOffenseDef.flattened_elements`와 같은 성격의 컴파일러 산출물(캐시)이다.
Definition YAML에 사람이 `resolved_ref`까지 손으로 쓰게 두면 캐시가 사실상
두 번째 진실 소스가 된다. `exported_component_def.schema.json`에서
`resolved_ref` 필드를 완전히 제거했다(옵션으로 남기지 않고 아예 뺌 — 있으면
`additionalProperties: false`가 거부한다, 아래 부정 케이스 확인). 해당 값은
step 4(QUALIFY/COMPOSE compiler)가 만드는 Compiled IR에만 존재하게 된다.
`examples/exported_components.yaml`에서 `resolved_ref: ground_fact.injury_occurred`
줄 삭제.

### 수정 4 — `OffenseDef.composition_metadata` 제거

이미 스키마상 required는 아니었지만(선택 필드), `type: object`에
`additionalProperties`/`properties` 제약이 전혀 없어 다른 곳의 엄격한 스타일과
어긋났고 어차피 fixture 12개 어디에도 쓰인 적이 없었다 — 컴파일러가 소비하지
않는 placeholder를 스키마에 남겨둘 이유가 없어 필드 자체를 제거했다. 나중에
semantics가 정해지는 버전(컴파일러 설계 시점)에서 다시 추가한다.

### 확정 A — `element_expression`은 canonical schema에서 문법이 하나뿐임을 재확인

7절/11절의 flat-list 예시("implicit ALL")를 JSON Schema 레벨에서 별도 array
branch로 받아주는 게 아니라, YAML 저작 시에도 항상 `{op: all, args: [...]}`
트리 형태로 쓰게 되어 있다는 걸 재확인했다(`element_bundle_def.schema.json`,
`doctrine_def.schema.json` 등 어디에도 flat-array oneOf branch가 없음).
`common.schema.json#/$defs/element_expression`의 `oneOf`는 ref/all/any/not/one_of
5개뿐 — canonical AST는 이미 단일 문법이다. 향후 사람이 편의상
`requires: [a, b, c]` 같은 shorthand를 쓰고 싶다면 그건 **저작 단계의 normalize
전처리**(YAML 파싱 후 canonical AST로 변환, JSON Schema 검증은 변환 결과에만
적용)로 처리하고, JSON Schema 자체에 두 번째 문법 branch를 추가하지 않는다 —
컴파일러(step 4)가 두 AST 형태를 처리할 필요가 없도록.

### 확정 B — `$id`를 absolute URI로 전환

`idpr/v2/<Name>` 형태였던 모든 `$id`/cross-file `$ref`를
`https://schemas.idpr.local/v2/<Name>` 형태로 바꿨다(예:
`https://schemas.idpr.local/v2/common#/$defs/id`). 실제로 네트워크 fetch는
하지 않고, validator가 이 절대 URI를 로컬 스키마 파일에 매핑하는 registry/store를
그대로 쓴다(검증 스크립트에서는 `jsonschema.RefResolver(store=...)`로 구현).
Draft 2020-12 reference resolution이 상대 `$id` 조합에서 나중에 꼬이는 걸
미리 피하기 위함 — 13개 스키마 파일 전체에 일괄 적용.

### 확정 C — `authority_basis` enum은 provisional 유지, semantics 미확정 상태로 고정

재검토 결과 지금 컴파일러/타입체커가 `authority_basis` 값에 따라 다른 실행을
하지 않으므로(citation 표시용 metadata) 굳이 스키마를 더 열어두거나 잠글
필요는 없다고 판단 — enum 자체는 그대로 두되(이미 `description`에 "Open
Question #10, provisional" 명시가 되어 있었음), **이 값이 metadata 수준을
벗어나 compiler semantics에 영향을 주게 되는 순간(예: authority_basis에 따라
weight/우선순위가 갈리는 설계가 생기면) 반드시 별도 설계 절을 먼저 연다**는
원칙만 이 문서에 명시적으로 기록해둔다. 스키마 변경 없음.

## v1과의 핵심 차이 — 구조로 강제됨

`bar`/`waiver`/`boundary`/`component` 같은 neural-visible role 필드는 어떤 v2
스키마에도 없다. `additionalProperties: false`라서 그런 필드를 끼워넣으면
구조 검증에서 즉시 거부된다 — 실제로 아래 검증에서 `role: "bar"`를
`DoctrineDef`에 넣어봤더니 `Additional properties are not allowed ('role' was
unexpected)`로 막혔다. v1에서 반복된 극성 버그의 재발을 스키마 단계에서부터
구조적으로 막는 게 이번 작업의 핵심 목표였다.

## 검증

`docs/contracts/v2/examples/*.yaml` 12개 파일, **36개 인스턴스**(2026-08-08
재검토 전 26개 + 10개 추가: 20.1/20.4 fixture 5개 신규 predicate + 20.1/20.4
본체 2개 + MODIFY fixture용 predicate 2개 + `doctrine.diminished_capacity`
1개) 전부 대응하는 스키마에 대해 `jsonschema`(Draft 2020-12, `RefResolver` +
absolute `$id` store)로 검증 통과. section 20의 validation case 중
**20.1(진정신분범, `offense.bribery_taking`의 `elements.subject`가
QUALIFY 없이 base offense 자체에 status requirement를 바로 갖는 경우)**,
20.2(부진정신분범, QUALIFY), 20.3(결과적 가중범, COMPOSE), **20.4(composite
offense + statutory nexus, `derived_offense.robbery_rape` — 두 개의 완결된
OffenseDef를 causal_nexus가 아닌 `relation.occasion_identity`로 묶는 COMPOSE)**,
20.5(미수범, CompletionPolicy), 20.6/20.7(공동정범/교사범, ParticipationPolicy)을
실제 fixture로 exercising한다 — **20.1/20.4 모두 이번에 추가 완료**.

부정 케이스로 스키마가 실제로 뭔가를 거부하는지도 확인(총 8개, 기존 3개 +
2026-08-08 재검토분 5개):
- `DoctrineDef`에 v1식 `role: "bar"` 필드 추가 → 거부(`additionalProperties: false`).
- `DoctrineDef.stage="unlawfulness"`인데 `effect.stage="punishability"` →
  거부(if/then 일치 강제).
- `OffenseDef`에 v1식 `card_role: "bar"` 필드 추가 → 거부.
- `DoctrineDef` MODIFY effect에 옛 자유 문자열 `modification` 필드 → 거부
  (`modifier_ref`로 교체됐으므로).
- `ExportedComponentDef`에 손저작 `resolved_ref` → 거부(스키마에서 제거됨).
- `ParticipationPolicyDef`에 옛 `offense` 필드 → 거부(shared/global 모양으로
  교체됨).
- `ParticipationPolicyDef`의 `instigator`가 `requires_conclusion:
  liability_result`를 선택 → 거부(`offense_realization` const로 고정).
- `OffenseDef`에 제거된 `composition_metadata` 필드 → 거부.

## 2026-08-08 Type checker 설계 중 발견된 추가 스키마 결함 (5차 수정)

Type checker(section 26 순서 2번) 설계를 시작하자마자 스키마가 아직 완전하지
않다는 게 드러났다 — 검토가 총 5라운드 거쳐 아래 5개를 확정했다. 전부
`docs/contracts/v2/*.schema.json` + `examples/derived_offenses.yaml`에 반영,
재검증 통과(36개 인스턴스 그대로, 부정 케이스 스키마 레벨 11개 추가 확인).

1. **`component_ref`에 `local_key` 필수 추가 + kind별 placement 분리.** `COMPOSE`의
   `primitive`/`bundle`/`exported_component` 컴포넌트가 `flattened_elements`의
   어느 slot으로 가는지 기록할 방법이 없었다. `primitive`/`exported_component`는
   단일 predicate/expression으로 귀결되므로 `slot`(단수) 하나면 충분하지만,
   `ElementBundleDef`는 여러 predicate를 combine한 tree라 slot 하나로 못 박으면
   틀리다 — `placement`(맵: bundle 자신의 leaf-ref → slot)로 분리했다.
   `common.schema.json#/$defs/placement_map` 신설, `offense`-kind 컴포넌트는
   둘 다 금지(자기 slot 구조를 이미 가짐).
2. **`local_key`는 composition-local, `relation_binding`은 그걸로 참조.**
   처음엔 `relations`를 `RelationDef` id 평문 배열로 뒀는데 "어떤 두 컴포넌트를
   잇는 relation인지" 기록이 없었다. 1차 수정은 endpoint를 컴포넌트의 전역
   `ref`로 걸었는데, 이건 "이 조합 안에서 어느 occurrence인지"(composition-local
   개념)를 "전역적으로 어떤 객체인지"(global id)와 섞는 실수였다 — `component_ref`에
   `local_key`(이 derivation의 `components` 배열 안에서만 유효한 이름, 전역
   dereference 대상 아님)를 신설하고 `relations`를
   `[{relation, left, right}]`(`left`/`right`는 `local_key`) 형태로 재구성했다.
3. **`OffenseDef.element_modules`에 실행 의미 부여.** `element_expression` leaf가
   `ElementBundleDef`를 직접 가리키는 경로(`op:ref`)를 폐기하면서(4번 참고)
   `element_modules`가 "이 bundle을 쓴다"는 정보만 있고 "이 bundle의 predicate들이
   이 offense의 어느 slot에 어떻게 붙는지"를 말할 방법이 없는 죽은 metadata가
   될 뻔했다 — v2.1.0 7절의 "shared element module"(negligence_bundle 등) 설계
   의도를 살리려면 이건 안 됨. `COMPOSE`의 bundle-placement 메커니즘을 그대로
   재사용해 `element_modules`를 `[{ref, placement}]`로 재정의했다 — base
   `OffenseDef`의 실제 slot 요건은 이제 `elements.<slot>`과
   `element_modules[].placement`가 그 slot에 기여하는 부분의 **결합**이다.
   현재 fixture 어디서도 `element_modules`를 안 쓰고 있어 마이그레이션 대상은
   없음 — 실 사용 예시는 legally-forced 조작 없이 Type checker 테스트(합성
   fixture)에서 다루기로 결정.
4. **`ExportedComponentDef`는 완전히 resolve 가능 — compiler-only 아님.**
   `resolved_ref`를 스키마에서 뺀 의미(직전 재검토, "compiler가 만드는 캐시라
   사람이 authoring하면 안 됨")를 "그래서 Definition Layer에서는 알 수 없다"로
   잘못 해석한 순간이 있었다 — 틀렸다. `ExportedComponentDef{source_offense,
   export_key}` + `OffenseDef.exports[export_key]`만 있으면 결정론적으로
   resolve된다. 이 자체는 스키마 변경이 아니라 Type checker(`registry.py`의
   `resolve_export`)가 그 사실을 실제로 활용하도록 설계를 고친 것.
5. **`element_expression` leaf 허용 kind, `grounded_by` 허용 kind 축소.**
   `element_expression` leaf는 `GroundFactDef | LegalElementDef`만(`ElementBundleDef`는
   `COMPOSE`/`element_modules`를 통해서만 쓰임), `LegalElementDef.grounded_by`는
   `GroundFactDef`만 — 둘 다 어느 fixture도 실제로 쓴 적 없는 미검증
   allowance였어서 baseline에서 뺐다. 실제로 필요해지면 그때 다시 연다.

## 다음 단계

section 26 순서의 2번, Type checker — 위 스키마 addendum이 끝났으니 이제
`src/idpr/v2/` 패키지 구현에 들어간다. 15.4의 typed dependency 검증 같은
**의미 타입체크**는 6개 축(reference/operator/stage-effect/export/participation/
derivation typing)으로 나눠 구현 — 상세 설계는 승인된 계획서
(`/home/jaehoonjeong/.claude/plans/modular-seeking-glade.md`, 2026-08-08) 참고.
특히 axis 2(operator typing)는 `flattened_elements`를 leaf-ref superset이
아니라 `derivation`을 재귀적으로 replay한 canonical expression과의 **의미
동등성**으로 검증한다 — `flattened_elements`는 최종 top-level 비교(actual
side)에서만 읽고, 다른 entry의 기대값을 계산할 때는 (그 entry가
`DerivedOffenseDef`이더라도) 항상 그 entry 자신의 `derivation`을 재귀적으로
다시 replay한다. 저장된 `flattened_elements`를 "다른 계산의 입력"으로 쓰는
순간 "derivation = source of truth" 원칙이 깨지기 때문.

**(위 절은 역사적 기록 — Type checker는 이미 완료됐고, 그 axis 2의 replay 로직은
2026-08-08 Step 4(QUALIFY / COMPOSE compiler, `src/idpr/v2/compile.py`)로 옮겨져
공개 API `compile_offense()`가 됐다. Step 4는 이번 문서의 스키마(`*.schema.json`)를
전혀 건드리지 않았다 — `docs/handoff/CURRENT.md`의 "Step 4 완료" 절 참고.)**

## 2026-08-08 Step 5(Relation evaluator) 착수 시 스키마 수정 (6차 수정)

Step 2에서 "**DEFERRED BY DESIGN**"으로 유예했던 항목 —
`RelationDef.left_type`/`right_type` ↔ bound component의 semantic type 일치 검증 —
을 이번에 닫았다. Step 4 완료 시점에도 "vocabulary 부재로 여전히 못 함"이라
판단했었으나, 실제로 부족했던 건 vocabulary가 아니라 **타입을 어디에 붙일
것인가에 대한 모델**이었다.

### 왜 정의 객체에 고정 semantic type을 붙이면 안 되는가 (핵심)

가장 자연스러운 첫 설계는 각 정의 객체에 intrinsic type 하나를 주는 것이다.
그런데 기존 fixture 두 개가 이걸 바로 반증한다 — 같은 `offense.robbery`가:

- `derived_offense.robbery_causing_injury`에서 `relation.causal_nexus`
  (event × event)의 **left = event**로,
- `derived_offense.robbery_rape`에서 `relation.occasion_identity`
  (conduct × conduct)의 **left = conduct**로

쓰인다. 둘 다 법적으로 올바른 저작이다(인과관계는 사건 사이의 관계, 기회의
동일성은 행위 사이의 관계). `OffenseDef`에 고정 타입 하나를 박으면 이 중 하나는
반드시 거부된다. 반대로 `semantic_types: [conduct, event]`처럼 집합을 주는 건
타입 시스템을 약화시키는 방향이라 채택하지 않았다(어떤 조합이든 통과하게 됨).

→ 채택: **relation-scoped typed endpoint projection**. 타입은 정의 객체가 아니라
**relation binding이 선언**한다.

```text
global definition  →  local component occurrence  →  typed relation endpoint
   offense.robbery         robbery_part                 .as(conduct)
   offense.robbery         base_robbery                 .as(event)
```

### 수정 1 — `relation_binding`에 `left_view`/`right_view` 필수 추가

`derived_offense_def.schema.json`의 `$defs/relation_binding`이 이제
`{relation, left, right, left_view, right_view}`. `left_type`/`right_type`과 같은
자유 문자열 vocabulary를 공유한다.

**view를 `RelationDef.left_type`에서 추론하지 않는다**는 게 중요한 제약이다 —
추론하면 "view가 relation type과 일치하는가"라는 검사가 항상 참이 되어(vacuous)
검사 자체가 무의미해진다. 저작이 명시하고, Step 5가 검사한다.

### 수정 2 — `GroundFactDef`/`LegalElementDef`에 옵션 `semantic_sort` 추가

Structured/atomic을 다르게 다룬다. `OffenseDef`와 달리 **atomic predicate는 진짜로
고유한 sort 하나를 갖는다** — `ground_fact.injury_occurred`는 event다. 그래서:

```text
Offense / DerivedOffense  → intrinsic type 없음 → relation-scoped view
                             (현재 지원: conduct / event)
Primitive                 → 감싼 predicate의 semantic_sort를 따라감
ExportedComponent         → resolve_export 대상 predicate의 semantic_sort를 따라감
GroundFact / LegalElement → semantic_sort를 직접 선언
ElementBundle             → 단일 endpoint sort 없음 → baseline에서 항상 unsupported
```

`semantic_sort`는 optional이다(실제로 relation endpoint에 도달하는 predicate만
채우면 됨). 다만 **미선언을 "통과"로 처리하지 않는다** — 선언이 없으면
`relation_endpoint_untyped`로 명시적으로 보고한다. 미검증 allowance를 조용히
남겨두지 않는다는 5차 수정 때와 같은 원칙.

`ElementBundleDef`가 relation endpoint인 경우 Step 4(compiler)는 여전히 그
occurrence를 **보존**하고, Step 5(lowering)에서 거부한다 — 계층이 다르므로 Step 4의
"거부 없음" 결정과 충돌하지 않는다.

### fixture 변경

- `derived_offenses.yaml`: 두 relation binding에 view 추가(위 event/conduct 대비 사례
  그대로).
- `ground_facts.yaml`: `ground_fact.injury_occurred`에 `semantic_sort: event`
  (`exported_component.injury_result` → `offense.injury.exports.result` 경로로
  relation endpoint에 도달하는 유일한 predicate).

인스턴스 수는 36개 그대로. 검증 통과.

**이로써 Step 2의 "DEFERRED BY DESIGN" 2개 중 첫 번째는 종료.** 남은 하나
(`modifier_ref` → 실제 `ModifierDef` 존재 확인)는 `ModifierDef` 객체 자체가 아직
설계되지 않았으므로(Open Question #4) 여전히 열려 있다.
