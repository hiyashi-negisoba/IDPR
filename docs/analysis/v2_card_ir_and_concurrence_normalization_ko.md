# V2 카드 증강·doctrine 트랙 재정립 스펙

## 1. 정정

이 문서는 저장소의 실제 카드 schema, issue hierarchy, retrieval 구현과 v2 runtime을 다시
감사한 결과다. 앞선 초안의 다음 내용은 폐기한다.

- 카드에 독립된 `학설` taxonomy가 있다는 설명
- BM25-only 결과를 기존 검색기의 결과처럼 취급한 197-target plan
- 같은 조문 안에서 검색으로 parent issue를 고른 뒤 Call 2 판단에 사용하는 방식

현재 생성된 `card_reassessment_plan_v1`은 production 또는 성능 근거로 사용하지 않는다.

## 2. 실제 카드 분류

live corpus는 51개 조문의 검수 카드 1,848장이다. 하나의 단일 taxonomy가 아니라 다음 축을
동시에 가진다.

### 2.1 원천 카드 metadata

| 축 | 실제 값 |
|---|---|
| `norm_kind` | `standard`, `element`, `exception`, `definition`, `causal_link`, `variant` |
| `doctrinal_status` | `descriptive`, `precedent_position`, `settled`, `disputed` |
| `formalization` | `standard_input`, `deterministic_rule` |
| `polarity` | `positive`, `negative`, `exception` |
| `authority_basis` | 주석서 종합, 주석서 수록 판례, 주석서 수록 학설, 주석서 내 법문 |

`authority_basis=commentary_reported_doctrine`인 live 카드는 60장이지만, 이는 **자료의 권위
출처**이지 pipeline 효과나 별도 학설 분류가 아니다. `norm_kind=variant` 52장도 학설 카드와
동일한 집합이 아니다.

### 2.2 compiled card axes

| 축 | 실제 값 |
|---|---|
| `function` | `canonical_element`, `application_standard`, `exception`, `defeater`, `stage`, `concurrence`, `participation`, `narrative`, `skeleton_meta` |
| `form` | `abstract_rule`, `precedent_rule`, `precedent_pattern` |
| `runtime` | `always_assess`, `retrieve_assess`, `retrieve_only`, `relation_condition`, `static` |
| `gate_effect` | `support`, `refute`, `exclude`, `block`, `none` |

### 2.3 reviewed issue hierarchy

1,848장은 검수된 383개 parent issue에 정확히 한 번씩 배치되어 있다.

| issue function | 수 | 현재 의미 |
|---|---:|---|
| `element_issue` | 170 | 구성요건 판단 단위 |
| `support_issue` | 87 | 설명·법리 문맥 |
| `concurrence_issue` | 51 | 죄수 관계 조건 |
| `stage_issue` | 46 | 실행착수·기수·미수 등 |
| `guard_issue` | 18 | 조각·배제 후보 |
| `participation_issue` | 11 | 공범 관계 조건 |

카드 load policy는 `anchor_context`, `retrieve_candidate`, `symbolic_only`, `support_only`다.
판례 사안형 카드는 anchor가 될 수 없고, detail 검색은 같은 parent issue 안에서만 허용된다.

## 3. 실제 검색 계약

기존 검색기는 BM25-only가 아니다.

```text
BM25 character-bigram ranking
  + embeddinggemma-300m bi-encoder ranking
  -> RRF(k=60)
  -> query당 최대 100개 shortlist
  -> bge-reranker-v2-m3 cross-encoder reranking
  -> 여러 query 결과는 max fusion
```

- BE와 CE snapshot은 `/data5/jaehoonjeong/.cache/huggingface/hub`에 존재한다.
- 1,848장 document embedding cache는
  `data/eval/cache/cards_embeddinggemma-300m_7512d150955707d6.json`이다.
- CE 점수는 query-dependent라 document cache 대상이 아니다.
- retrieval 함수에 encoder/reranker를 주입하지 않으면 BM25-only로 동작한다. 앞선 v2 bridge와
  197-target plan은 이 주입을 하지 않았으므로 기존 검색을 재사용한 것이 아니다.
- production 실험에서는 BE 또는 CE를 로드하지 못했을 때 BM25로 조용히 강등하지 않고
  `RETRIEVAL_UNAVAILABLE`로 실패시킨다.

## 4. V2에서 검색이 허용되는 위치

Call 1과 Call 1.5가 이미 offense, actor, factual episode를 정한다. 따라서 과거 L0처럼 카드
검색으로 조문이나 offense를 다시 발견하지 않는다.

또한 같은 조문 안에서도 semantic search로 parent issue를 선택하지 않는다. 긴 사건 사실이나
포괄적인 predicate 설명이 같은 조문의 다른 쟁점을 끌어오면 카드가 Call 2를 오염시킬 수 있다.

```text
typed v2 target
  -> authored statutory identity
  -> reviewed explicit target-to-issue bridge
  -> 이미 활성화된 parent issue
  -> 그 issue의 retrieval_card_ids 안에서만 hybrid detail retrieval
  -> 최대 2장
```

명시적 bridge가 없으면 검색으로 보충하지 않고 `UNMAPPED_TARGET_ISSUE`로 남긴다. 검색은 이미
정해진 법적 판단 단위에 자료를 공급할 뿐, 판단 단위를 만드는 producer가 아니다.

## 5. 카드 소비 지점

카드의 소비 지점은 가상의 새 taxonomy가 아니라 reviewed issue의 `function/runtime`과 현재
typed target이 함께 결정한다.

| 활성 target | 허용 issue | 소비 지점 | 금지 |
|---|---|---|---|
| offense predicate | `element_issue` | primary Call 2의 카드 유무 A/B 또는 별도 atomic reassessment | 새 predicate/offense 생성 |
| 열린 공범 probe | `participation_issue` | 같은 Call 2 boundary의 공범 atomic 판단 | interaction·공범 후보 생성 |
| completion unresolved | `stage_issue` | completion condition 판단 | 카드만으로 form 확정 |
| authored doctrine branch | `guard_issue` 또는 명시 support | branch의 typed requires 판단 | card hit로 DoctrineDef 생성·활성화 |
| exact occurrence-aware offense pair | `concurrence_issue` | pair condition 판단 | 카드로 pair 생성 |
| 확정·미해결 reasoning item | `support_issue` 및 사용된 issue 자료 | Call 3 reasoning packet | symbolic truth 변경 |

Call 2의 element와 participation은 서로 다른 pipeline 단계가 아니다. 둘 다 같은 neural legal
assessment boundary 안의 서로 다른 typed target family다.

## 6. Doctrine 트랙의 정확한 의미

카드 corpus에는 `학설`이라는 runtime function이 없다. 따라서 doctrine 트랙은 두 층으로
분리한다.

### 6.1 결론에 영향을 주는 doctrine branch

Scallop에 영향을 주려면 카드 metadata가 아니라 다음 authored object가 먼저 있어야 한다.

```text
stable branch/DoctrineDef id
+ offense-instance activation scope
+ typed requires
+ effect와 liability stage
+ source card provenance
+ review status
```

카드는 이 branch의 법적 기준과 provenance를 제공할 수 있지만 branch를 자동 생성하거나
TRUE로 만들지 않는다. stage별 전역 doctrine pool도 금지한다. 현재 KCL-26에서 요구되는 여러
branch는 authored universe에 없고 active doctrine은 0이므로, 이는 retrieval 문제가 아니라
representation/authoring gap이다.

### 6.2 Call 3에서 설명할 학설·판례 자료

`authority_basis`, `doctrinal_status`, `norm_kind`, issue placement를 함께 사용해 설명 자료를
구성한다. 어느 한 필드만으로 “학설 카드”라고 판정하지 않는다.

live 1,848장은 rejected doctrine을 제외한 실행 corpus다. KCL 답안이 요구하는 대립 학설의 양쪽
견해가 모두 live corpus에 남아 있다고 전제할 수 없다. 따라서 Call 3 연결 전 다음을 별도로
감사한다.

- live card에 남은 주석서 수록 학설 60장의 issue·견해 coverage
- `context_only`로 강등된 비채택·설명 자료의 검수 원장과 재사용 가능성
- 사용자 선택이 끝난 학설 그룹과 단순 소개 자료의 구분
- KCL의 총칙 학설 중 현재 각론 corpus에 없는 21개 corpus-gap tag

Call 3에는 확정 symbolic 결론, unresolved branch, 판례·실무 기준, 학설 대립 자료를 provenance와
함께 분리해 준다. 구체 계약은 사용자가 제공할 Call 3 spec을 받은 뒤 정한다.

## 7. 재실행 계획

### Gate 0 — 현 상태 동결

- Call 1/1.5/1.5-P/primary Call 2 결과를 baseline으로 보존한다.
- `card_reassessment_plan_v1`의 197개 및 BM25-only 수치는 무효화한다.
- 기존 prompt를 수정하지 않는다.

### Gate 1 — bridge authoring 범위 확정

다음을 별도 reviewed metadata로 만든다.

1. `predicate_ref -> issue_id` exact bridge
2. `derived DefinitionRef -> statutory article/issue` bridge
3. authored doctrine branch와 source issue/card bridge
4. exact concurrence DefinitionRef pair와 condition issue bridge

검색으로 이 bridge를 대신 만들지 않는다.

### Gate 2 — hybrid retrieval 재배선 검증

- exact parent issue 내부에서 BM25+BE RRF+CE를 실제로 사용한다.
- cache fingerprint, 모델 ID, query, shortlist, CE score, 최종 card id를 artifact에 기록한다.
- BM25-only와 hybrid 결과 차이는 진단으로 남기되 BM25-only를 production 결과로 사용하지 않는다.

### Gate 3 — Call 2 카드 A/B

exact bridge가 있는 element target만 전수 대상으로 삼는다.

```text
A: 현재 atomic input
B: 동일 input + 같은 parent issue의 hybrid top-2 detail
```

기존 TRUE/FALSE/UNKNOWN, exact evidence, rubric 정합성, 카드 사례를 사건 사실로 오인한 오류를
모두 비교한다. UNKNOWN 감소만으로 성공으로 보지 않고 `A correct -> B wrong` backfire를 별도
보고한다. route 채택은 gold 행별 cherry-pick이 아니라 reviewed bridge 단위로 결정한다.

### Gate 4 — Call 2 이후 doctrine/stage/concurrence

- authored branch가 있는 doctrine만 atomic requires assessment에 연다.
- completion unresolved만 stage issue에 연결한다.
- exact pair와 same episode가 있는 concurrence만 condition assessment에 연다.
- UNKNOWN 또는 conflict는 host가 고르지 않고 unresolved로 유지한다.

### Gate 5 — Scallop 및 Call 3 준비

허용된 typed delta만 Scallop에 추가해 establishment/unresolved/backfire를 비교한다. 그 뒤 Call 3
spec을 받아 판례·학설·support 자료가 symbolic 결론을 넘지 않는 reasoning packet을 설계한다.

## 8. Gate 3 실행 결과

job 222907에서 exact bridge가 있는 기존 UNKNOWN LegalElement 88개를 paired A/B로 실행했다.

- A 카드 없음: TRUE 31 / FALSE 9 / UNKNOWN 48
- B 카드 있음: TRUE 35 / FALSE 8 / UNKNOWN 45
- 카드 순증분: UNKNOWN 3개 감소
- A/B 변경 14개 중 카드 적용이 보고된 변경: 6개
- reviewed decisive partial gold 개선: 0/3

원래 88개가 모두 UNKNOWN이었으므로 가장 큰 효과는 카드가 아니라 atomic decomposition이었다.
카드 적용 변경에는 명확한 개선 3개가 있었지만 occurrence identity 위험 1개와 evidence
provenance 불충분 2개도 있었다. 따라서 B 결과는 canonical Call 2나 Scallop에 합치지 않는다.
세부 감사는 `card_call2_ab_v1/qualitative_audit.md`에 기록했다.

다음 승인 단위는 카드 범위를 넓히는 것이 아니라 occurrence identity와 evidence sufficiency
gate를 보강한 뒤 exact route 단위로 재검증하는 것이다.
