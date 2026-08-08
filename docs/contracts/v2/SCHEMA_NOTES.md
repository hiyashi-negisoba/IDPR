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
  `idpr/v2/<Name>` 형태이고, cross-file `$ref`는 파일명이 아니라 이 `$id`를
  기준으로 한다(예: `"$ref": "idpr/v2/common#/$defs/id"`) — validator에 각
  스키마를 `$id`로 등록해야 relative resolve가 된다. 실제 등록/검증 예시는
  아래 "검증" 절 참고.
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
5. **`ParticipationPolicyDef`의 모양.** 22절이 이 이름만 나열하고 15절은 런타임
   객체(`ParticipationResult`, 15.4)만 상세히 설명한다. 15.4의 typed dependency
   개념("교사는 `OffenseRealization<X>`을 요구하지 `LiabilityResult<X>`를
   요구하지 않는다")을 정의 시점 정책으로 그대로 옮겨
   `{id, offense, modes: {principal, co_principal, instigator, aider}}`로
   설계 — `instigator`/`aider`는 `requires_conclusion`(offense_realization /
   offense_establishment / liability_result 중 하나)을 명시해야 하고, 실제
   타입체크(15.4의 TYPE ERROR)는 이후 step 2(Type checker)가 수행한다.
6. **provisional로 남긴 필드(문서가 스스로 미해결이라고 밝힌 부분, 25절)**:
   `authority_ref.authority_basis` enum(open question #10), `MODIFY.modification`을
   자유 문자열로(open question #4), `CompletionPolicyDef`의
   `punishability_note`를 자유 문자열로(open question #5). 전부 스키마
   설명(description)에 어느 open question에 걸려 있는지 명시해뒀다.
7. **`DoctrineDef.stage`와 `effect.stage` 일치 강제.** 문서엔 명시적 언급이
   없지만 12절 stage별 effect 표(DEFEAT는 unlawfulness/culpability만, MODIFY는
   culpability/punishability만, EXEMPT는 punishability만)를 실제로 지키게
   `if/then`으로 스키마 레벨에서 강제했다.
8. **`OffenseDef.composition_metadata`는 의도적으로 미확정(빈 object 허용).**
   22절이 필드 이름만 나열, 아직 컴파일러가 없어 실제로 뭐가 필요한지 모른다 —
   억지로 타입을 지어내지 않았다.

## v1과의 핵심 차이 — 구조로 강제됨

`bar`/`waiver`/`boundary`/`component` 같은 neural-visible role 필드는 어떤 v2
스키마에도 없다. `additionalProperties: false`라서 그런 필드를 끼워넣으면
구조 검증에서 즉시 거부된다 — 실제로 아래 검증에서 `role: "bar"`를
`DoctrineDef`에 넣어봤더니 `Additional properties are not allowed ('role' was
unexpected)`로 막혔다. v1에서 반복된 극성 버그의 재발을 스키마 단계에서부터
구조적으로 막는 게 이번 작업의 핵심 목표였다.

## 검증

`docs/contracts/v2/examples/*.yaml` 12개 파일, 26개 인스턴스 전부 대응하는
스키마에 대해 `jsonschema`(Draft 2020-12)로 검증 통과. section 20의 validation
case 중 20.2(부진정신분범, QUALIFY), 20.3(결과적 가중범, COMPOSE), 20.5(미수범,
CompletionPolicy), 20.6/20.7(공동정범/교사범, ParticipationPolicy)을 실제
fixture로 exercising한다(20.1/20.4는 이번 fixture 세트엔 없음 — 필요시 추가).

부정 케이스 3개로 스키마가 실제로 뭔가를 거부하는지도 확인:
- `DoctrineDef`에 v1식 `role: "bar"` 필드 추가 → 거부(`additionalProperties: false`).
- `DoctrineDef.stage="unlawfulness"`인데 `effect.stage="punishability"` →
  거부(if/then 일치 강제).
- `OffenseDef`에 v1식 `card_role: "bar"` 필드 추가 → 거부.

## 다음 단계

section 26 순서의 2번, Type checker. 이 스키마가 잡아주는 건 구조(모양)뿐이고,
15.4의 typed dependency 검증("instigation requires `OffenseRealization<X>`인데
`ElementsResult<X>`만 있으면 TYPE ERROR") 같은 **의미 타입체크**는 별도 코드가
필요하다 — 그게 다음 단계다.
