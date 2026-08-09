# Predicate 사전 확장 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외) v1

[predicate_dictionary_ext_art339_v0.md](predicate_dictionary_ext_art339_v0.md)에 대한
사용자 검수 3건을 반영한다. v0는 그대로 둔다 — 이력 추적용. 세 정정 모두 v0가
"fixture가 이미 증명해뒀다"는 확인에 안심해 그 이상을 조급하게 확정해버린 오류라는
점에서 같은 계열이다 — fixture가 실제로 증명한 범위와 내가 확정한 범위 사이의 간격을
정확히 재지 않았다.

---

## 정정 1 — Completion selector는 causation이 아니라 vaginal_intercourse_conduct

**v0 오류**: `COMPLETED.when = coercion_induced_sexual_act_causation`(강제수단과
intercourse의 인과관계까지 포함하는 predicate)을 completion selector로 썼다. 6B
원칙상 `when`은 완성상태 selector이고 substantive element requirement(causation)를
대신하면 안 되는데, causation predicate를 selector로 쓰면 **간음은 발생했으나
강제수단과의 인과관계가 FALSE인 사건**(예: 강도 현장에서 우연히 발생한 별개의
합의된 성관계)이 `NOT(causation)=TRUE`가 되어 `ATTEMPTED`로 잘못 분류된다 — 실제로는
297 자체의 Elements(causation)가 불성립하는 사건이지 339의 미수가 아니다. 338 fixture
(`completion_policy.robbery_homicide`)가 이미 `COMPLETED.when = ground_fact.death_
of_victim`(causation predicate인 `death_causation`이 아니라 bare occurrence fact)를
쓰고 있었는데, v0는 그 정확한 선례를 두고도 339에서만 causation predicate를 selector로
잘못 골랐다.

**v1(정정) — completion selector는 bare occurrence fact, causation은 elements에서만
평가.**

```text
robbery_rape.COMPLETED.when = vaginal_intercourse_conduct
    (강도의 기수·미수 무관)

robbery_rape.ATTEMPTED.when = ALL(
    legal_element.commencement_of_execution (강간행위 착수, 25조 재사용),
    NOT(vaginal_intercourse_conduct)
)
robbery_rape.ATTEMPTED.punishable = true (원문 Ⅴ, 342조 재사용)
```

`coercion_induced_sexual_act_causation`(강제수단-intercourse 인과관계)은 completion
selector에서 완전히 빠지고, rape_part(297) component의 `elements.causation`에서
그대로 평가된다 — **intercourse 발생 여부 → Completion, 강제수단과 intercourse의
연결 → Elements**로 층을 분리한다(배치⑨ 인과관계 이층 모델을 completion selector
설계에도 다시 적용한 것 — "결과 발생"과 "그 결과의 원인 귀속"을 같은 predicate로
뭉치면 안 된다는 원칙이 여기서는 "완성 여부"와 "그 완성의 원인 귀속"의 혼동으로
재발했다).

---

## 정정 2 — fixture는 ANY(333/334/335/336)까지 증명한 게 아니다

**v0 오류**: fixture(`derived_offense.robbery_rape`)가 증명한 건 **고정된 OffenseDef
2개**(`offense.robbery`, `offense.rape`)를 COMPOSE할 수 있다는 것뿐인데, v0는 이를
근거로 `base_offense = ANY(333, 334, 335, 336)`까지 최종 확정해버렸다. `ANY`는
`ElementExpression` 연산자이지 offense-ref union 문법이 아니다 — fixture가 실제로
지원을 증명한 범위를 벗어난 주장이었다.

**v1(정정) — predicate 사전 단계에서는 candidate 목록만 확정, 실제 COMPOSE 구조는
2-pass로 이월.**

```text
339 robbery-side candidate refs (population 대상):
- offense.robbery[333]
- offense.robbery[334]
- offense.robbery[335]
- offense.robbery[336] (coverage reference only — 51개 조문 워크시트 범위 밖,
  실제 definition에 unresolved offense_ref로 넣지 않는다. 원문 Ⅱ가 336을 주체
  범위에 포함시킨다는 사실만 authoring 메모로 남긴다)
```

실제 COMPOSE를 (a) base 유형별로 고정 component ref를 쓰는 `DerivedOffenseDef`
여러 개(333용/334용/335용 각각)로 나눌지, (b) 기존 `derivation`이 이미 지원하는
공통 base 재사용 메커니즘으로 하나의 definition 안에서 표현할지는 predicate
사전으로 결정할 문제가 아니다 — **2-pass에서 스키마에 직접 대입해보고 결정한다.**
**새 primitive HOLD는 아니다** — G-1(337조)이 이미 같은 형태(`ANY(333 강도, 334
특수강도, 335 준강도, 336 인질강도)`)로 서술해둔 것도 같은 종류의 조급한 확정일
가능성이 있으나, 배치⑫는 이미 확정·커밋된 문서라 이번 정정에서 소급 수정하지 않고
이 사실만 기록한다(2-pass 착수 시 337·338·339 셋을 함께 재확인할 사항으로 남긴다).

---

## 정정 3 — 297 predicate를 "7개 복사"하지 않는다, component ref로 참조

**v0 오류**: 구조 판단 절에서는 정확히 "COMPOSE(robbery offense component, rape
offense component)"라고 썼으면서, B절에서는 297의 predicate 7개를
`legal_element.coercive_conduct`부터 `legal_element.intent`까지 표로 다시 나열해
마치 339가 그 leaf들을 수동으로 재조립하는 것처럼 서술했다 — v2.1 원칙상 authoring
source of truth는 `OffenseDef` component ref여야 하는데, 표 형식이 사실상 수동
복제였다.

**v1(정정) — rape_part는 component ref로만 표기, leaf resolve는 compiler 책임.**

```text
rape_part = offense.rape[297]
```

297의 element/slot은 compiler가 이 component ref를 통해 resolve한다 — predicate
사전이 그 leaf들을 다시 나열할 필요가 없다(fixture의 `{kind: offense, ref:
offense.rape, local_key: rape_part}`가 이미 이 참조 방식을 보여준다).

**"강도 주체이므로 directness_of_coercion_by_offender가 자동 충족된다"는 v0
서술도 삭제한다.** 강도 신분과 그 predicate의 진실값을 연결하는 별도 규칙은 현재
스키마에 없다 — 297 component의 기존 element(`coercive_conduct`/`directness_of_
coercion_by_offender`/`coercion_sufficiency_for_rape`/`coercion_induced_sexual_
act_causation` 등)는 339에서도 297에서와 **완전히 동일하게, 별도 가정 없이** 그대로
평가된다. "강도의 폭행·협박과 동일한 conduct 인스턴스가 두 offense의 서로 다른
leaf를 동시에 충족할 수 있다"(v0 B절 후반)는 서술 자체는 유지한다 — 이건 진실값
자동연결 주장이 아니라, 하나의 사실관계(conduct)가 두 component에서 각각 독립적으로
평가된 결과 우연히 둘 다 TRUE가 될 수 있다는 사실관계 서술일 뿐이다.

유사강간(297조의2)·준강간(299) 제외 판단(v0 B절 후반)은 component ref 선택
자체("`offense.rape[297]`이지 297조의2·299가 아니다")의 근거이므로 그대로 유지한다.

---

## 갱신된 구조 판단 (v1 최종)

```text
derived_offense.robbery_rape:
  derivation:
    kind: compose
    components:
      - {kind: offense, ref: offense.robbery, local_key: robbery_part}
          # 실제 ref 해소(333/334/335 중 어느 것, 336 coverage 문제 포함)는
          # 정정2에 따라 2-pass authoring 확인사항
      - {kind: offense, ref: offense.rape, local_key: rape_part}
          # ref 자체는 offense.rape[297]로 고정(정정3) — 유사강간·준강간 아님
    relations:
      - {relation: relation.occasion_identity, left: robbery_part, right: rape_part,
         left_view: conduct, right_view: conduct}

completion_policy.robbery_rape:
  states:
    completed:
      when: {op: ref, ref: ground_fact.vaginal_intercourse_conduct}  # 정정1
      punishable: true
    attempted:
      when:
        op: all
        args:
          - {op: ref, ref: legal_element.commencement_of_execution}
          - {op: not, arg: {op: ref, ref: ground_fact.vaginal_intercourse_conduct}}
      punishable: true
      relations:
        - {relation: relation.occasion_identity, left: robbery_part, right: rape_part,
           disposition: retain}
```

(정정1에 따라 `vaginal_intercourse_conduct`는 여기서 `ground_fact`로 표기했다 —
v0 B절 표에서는 `ground_fact.vaginal_intercourse_conduct`로 이미 그렇게 typing돼
있었으므로 이번 정정과 충돌 없음, 재확인만.)

---

## self-check 체크리스트 재적용 메모 (v1)

- **completion selector와 substantive requirement 혼동 금지**(신규 항목, 정정1에서
  얻음): "완성되었는가"를 묻는 predicate와 "그 완성의 원인이 특정 행위에 귀속되는가"를
  묻는 predicate는 별개다 — 후자를 completion selector로 쓰면 원인 귀속이 실패한
  사건이 통째로 잘못된 completion state로 떨어진다. 배치⑨ 인과관계 이층 모델의
  completion-policy 버전으로 메모리에 남길 만한 원칙.
- **fixture가 증명한 범위를 정확히 재기**(신규 항목, 정정2에서 얻음): fixture는
  "가능함을 보여준 것"과 "이 조문에 대해 이 특정 구조가 맞다고 확정한 것" 사이에
  간격이 있다 — fixture 존재를 확인 근거로 그 이상(offense-ref union 같은 새 문법)을
  섣불리 확정하면 안 된다.
- **authoring source of truth는 component ref**(정정3에서 재확인): 이미 완결된
  다른 offense를 재사용할 땐 그 leaf를 다시 나열하지 않고 component ref로만
  가리킨다 — F/G절이 `base_offense.requires`를 참조 형태로만 쓰고 재나열하지
  않았던 것과 같은 원칙을 297 재사용에도 지켰어야 했는데 B절에서 표 형식 때문에
  놓쳤다.

---

## 최종 확정 predicate (v1)

339 = COMPOSE(`robbery_part`=`offense.robbery`[333/334/335 candidate, 336 coverage
참조만], `rape_part`=`offense.rape[297]`, component ref로만 표기) +
`relations=[occasion_identity]`(G 재사용, "강도의 기회") + CompletionPolicy(정정1
반영, `vaginal_intercourse_conduct`가 selector). 신규 predicate 0건·신규 스키마
0건 그대로 유지, 다만 **2-pass authoring 확인사항 1건**(정정2, robbery-side COMPOSE를
component ref 여러 개로 나눌지 공통 base 재사용으로 표현할지 — 337·338과 함께
재확인) 추가. 이건 architecture-compatibility HOLD 목록에 올리는 게 아니라 —
predicate/구조 자체는 이미 확정됐고 단지 "어느 필드 형식으로 정확히 쓸지"의 문제이므로
2-pass 착수 메모로만 남긴다.
