# Step 8 — Case-Level Factual Grounding Contract

**Status: draft for review.**
이 contract는 실패한 Unified Call 1 factual-grounding 경로를 대체한다. **Call 1 offense routing, Step 7 DSL closure, Call 2 truth assessment, DSL/Scallop runtime은 변경하지 않는다.**

26-case 실패의 직접 원인은 question-dependent factual inventory, 잘못된 entity/coreference, 과도한 occurrence split이었다. 실제 accepted packet에서도 non-mention이 entity에 들어가고, 동일 narrative가 sub-question에 따라 다른 occurrence universe를 만들었다.

---

## 0. Architecture / call count

Occurrence grounding은 **Call 1과 분리된 case-level preprocessing inference**다.

```text
Immutable Case Text
        ↓
G0 — Case-Level Factual Grounding
     once per unique case_text
        ↓
GroundingArtifact
     entities
     factual occurrences
        ↓ cache by case_text hash

Question + Case Text + GroundingArtifact
        ↓
Call 1 — offense routing + report-target linking
        ↓
Step 7 DSL Closure
        ↓
Occurrence-aware Instance Planner
        ↓
Call 2 — predicate assessment
        ↓
CaseTruths
        ↓
DSL / Scallop
        ↓
LiabilityResult
        ↓
Call 3 — IRAC
```

**Neural call 증가는 명시적으로 +1이다.**

```text
first use of a unique case narrative:
G0 + Call1 + Call2 + Call3

another sub-question sharing the same case narrative:
cached G0 + Call1 + Call2 + Call3
```

따라서 추가 physical grounding inference 수는 **26이 아니라 unique `case_text` hash 수**다. 실행 전에 manifest에 `unique_case_count`, cache hit 수, 실제 G0 request 수를 보고해야 한다.

---

# 1. G0 fixed boundary

입력:

```text
whole immutable case_text
```

입력 금지:

```text
question_prompt
sub_question_id의 의미
Call 1 seeds
Step 7 closure
offense refs
predicate refs
legal standards
Article 263
participation
factual-v0
gold answer
```

따라서 동일 `case_text`는 어느 sub-question에서 사용되든 **동일 GroundingArtifact 하나만** 가진다.

G0는 다음을 판단하지 않는다.

```text
죄명
구성요건
위법성
책임
미수/기수
공범
Article 263 성립
법조경합/상상적 경합/실체적 경합
최종 죄책
```

---

# 2. Source-address ledger

Host는 모델 호출 전에 `case_text`를 lossless source-address surface로 변환한다.

각 unit은:

```text
u0001
u0002
...
```

를 가진다.

Host 내부에는:

```text
unit_id
original start/end offset
surface text
```

만 보존한다.

### 요구사항

* line ending 이외 원문 변경 금지
* 모든 non-whitespace character가 정확히 source surface에 보존
* 법률 cue 기반 segmentation 금지
* 이름 regex 금지
* event regex 금지
* benchmark-specific `(1)/(2)` parser 금지
* victim parser 금지

모델 request에는 token 절약을 위해 **compact ledger rendering**만 보낸다.

```text
[u0001] ...
[u0002] ...
```

offset 등 host-only metadata를 반복 전송하지 않는다.

G0 request가 모델 context limit을 넘으면 **preflight failure**다. 이 contract에서는 grounding sharding을 자동 도입하지 않는다.

---

# 3. Entity semantics

기존처럼 모든 mention을 exhaustively 뽑게 하지 않는다.

Packet에서 `A` entity에 `같다는`, `B` entity에 `가`가 들어가는 문제가 실제 발생했다.

따라서 G0가 만드는 것은 **occurrence에서 실제로 참조되는 discourse entities만**이다.

개념 schema:

```json
{
  "entities": [
    {
      "anchor_source_unit_ids": ["u0017"]
    }
  ]
}
```

`anchor_source_unit_ids`는 그 entity를 명시적으로 지칭하는 **하나의 실제 source anchor**다.

모델은 persistent ID를 만들지 않는다.

Host가 earliest source anchor 순으로:

```text
ent:0001
ent:0002
...
```

를 발급한다.

### Coreference

Occurrence가 주어 생략, 대명사, 직책 등으로 동일 인물을 가리키는 경우 모델은 이미 존재하는 response-local entity index를 참조할 수 있다.

즉:

```text
"김민수는 ..."
"... 그는 ..."
"... 다시 폭행하였다."
```

가 하나의 `ent:0001`로 연결될 수 있다.

하지만 모델이 새 이름이나 source에 없는 entity를 만들 수는 없다.

---

# 4. FactualOccurrence semantics

`FactualOccurrence`는 법률상 행위 수가 아니다.

정의:

> **서로 다른 행위의 사실을 하나의 `OffenseInstanceKey`에서 혼합하지 않도록 하는 최소 factual conduct scope.**

Occurrence의 중심은 **누군가의 conduct 또는 omission**이다.

포함 가능:

```text
폭행
교부
전달
취거
기망 발언
문서 작성
신고
교사/요청 행위
침입
운전
제거
점유/소지 등 서술된 행위상태
명시된 부작위
```

Occurrence로 독립 생성하지 않는 것:

```text
단순한 범의/마음먹음
피해 결과만 서술된 문장
사람의 신분/관계
순수 background fact
법적 평가
수사기관/법원의 법률적 결론
```

실패 artifact에서 `B가 며칠 후 사망하였다`가 B 자신의 occurrence처럼 생성된 사례가 있었는데, 이런 **non-agentive result-only record는 금지**한다.

그 결과는 Call 2가 전체 case background에서 해당 focal occurrence와의 관계를 판단한다.

---

# 5. Occurrence output

G0 response:

```json
{
  "entities": [
    {
      "anchor_source_unit_ids": ["u0010"]
    },
    {
      "anchor_source_unit_ids": ["u0014"]
    }
  ],
  "occurrences": [
    {
      "focal_source_unit_ids": ["u0030", "u0031", "u0032"],
      "agent_entity_indices": [0],
      "participant_entity_indices": [1]
    }
  ]
}
```

필드는 이것만 허용한다.

### `focal_source_unit_ids`

해당 conduct를 직접 서술하는 source anchor.

* nonempty
* ledger order
* source에 실제 존재
* 여러 occurrence가 source unit을 공유하는 것 허용

즉 source overlap은 **정상**이다.

### `agent_entity_indices`

해당 occurrence에서 행위자로 factual하게 등장하는 entity.

* nonempty
* existing entity만 참조
* 여러 agent 허용

```text
甲과 乙이 함께 A를 붙잡았다
→ agents = [甲, 乙]
```

여기서 공동정범이라는 뜻은 아니다.

### `participant_entity_indices`

그 conduct의 직접적인 상대방·대상·수령인 등 **인적 factual participant**.

법률상:

```text
피해자
범죄객체
피해법익
공범
```

이라는 뜻이 아니다.

이 필드는 occurrence discrimination과 cross-occurrence factual joins를 위한 것이다.

empty 허용.

---

# 6. Split / merge rule

다음은 별개 occurrence다.

```text
same actor + different direct participant
same actor + same participant + separated later conduct
different agent conduct
명시적으로 구분되는 독립 행동
```

예:

```text
甲이 A를 때리고 B를 때렸다

occ1: agent=甲 participant=A
occ2: agent=甲 participant=B
```

같은 sentence와 같은 verb surface를 공유해도 두 record가 가능하다.

```text
甲이 A를 때렸다.
한 달 후 다시 A를 때렸다.

→ occ1, occ2
```

반대로 하나의 연속 factual conduct를 predicate/절 단위로 쪼개지 않는다.

```text
甲이 A를 붙잡아 넘어뜨리고 수차례 발로 찼다
```

는 특별한 factual break가 없다면 하나의 occurrence로 둘 수 있다.

**법률적으로 몇 개의 행위인지 판단해서 split하는 것은 금지**한다.

---

# 7. Host canonical identity

Entity:

```text
earliest explicit anchor
→ ent:0001, ent:0002, ...
```

Occurrence:

```text
earliest focal source position
→ agent entity tuple
→ participant entity tuple
→ focal source signature
```

순으로 canonical sort한 후:

```text
occ:0001
occ:0002
...
```

를 host가 발급한다.

모델은 다음을 출력할 수 없다.

```text
event_1
o1
o2
victim:A
occurrence_id
actor_id
```

---

# 8. GroundingArtifact

최종 host artifact:

```text
GroundingArtifact
  case_text_hash
  source_ledger_hash

  entities:
    ent:0001
      anchor source
    ...

  occurrences:
    occ:0001
      focal_source
      agents
      participants
    ...
```

Cache key는 최소:

```text
case_text_hash
grounding_prompt_hash
schema_hash
ledger_version_hash
model/runtime fingerprint
decoding configuration
```

이다.

**question_prompt hash는 cache key에 들어가지 않는다.**

---

# 9. Call 1

기존 Call 1의 핵심 역할은 다시:

```text
Question + Case
→ canonical offense seeds
```

이다.

G0 factual inventory를 생성하지 않는다.

필요하다면 이미 host canonicalized된 entity catalog를 입력받아:

```text
report_target_entity_ids
```

만 추가로 연결할 수 있다.

이 값은:

```text
reporting metadata
```

이며 occurrence/candidate 제거에는 쓰지 않는다.

Offense routing과 report-target linking 외의 factual segmentation을 Call 1에서 다시 하지 않는다.

---

# 10. Occurrence-aware planner

기존:

```text
all case actors
× all Step7 candidates
× o1
```

은 영구 폐기한다.

새 universe:

```text
for occurrence in GroundingArtifact:
    for actor in occurrence.agents:
        for candidate in Step7.candidate_offense_refs:
            emit OffenseInstanceKey
```

즉:

```text
Occurrence
× factual agents of that occurrence
× frozen Step7 candidates
```

이다.

```python
OffenseInstanceKey(
    case_id=sub_question_id,
    actor_id="ent:....",
    offense_ref=candidate_ref,
    occurrence_id="occ:....",
)
```

Grounder는 candidate를 모른다.

Planner도 candidate applicability를 판단하지 않는다.

---

# 11. Step 3 / DSL identity

기존 runtime identity는 변경하지 않는다.

Component scope는 parent의:

```text
case_id
actor_id
occurrence_id
```

를 그대로 상속하고 `offense_ref`만 기존 규칙대로 변경한다.

즉 occurrence 때문에:

```text
new DSL identity
new RuleIR
new Scallop identity relation
```

을 만들지 않는다.

---

# 12. Call 2

Call 2는 다음만 평가한다.

```text
(instance_key, predicate_ref)
→ TRUE | FALSE | UNKNOWN
```

그리고 row-level로 다음 catalog를 볼 수 있다.

```text
entity_catalog
occurrence_catalog
full case_text
```

평가 규칙:

```text
focal occurrence-specific facts
+
그 occurrence와 양립 가능한 case-global/background facts
-
다른 occurrence에만 고유한 facts
```

예:

```text
김민수는 공무원이다        ← global/background, 사용 가능
occ1에서 A를 폭행했다      ← occ1에서 사용
occ2에서 B가 사망했다      ← occ1에 무조건 섞지 않음
```

Call 2가 occurrence를 생성·병합·변경할 수 없다.

---

# 13. Cross-occurrence route

Ordinary predicates는 한 occurrence를 focal scope로 한다.

둘 이상의 occurrence 관계 자체가 법적 조건인 경우에만 dedicated route가 cross-occurrence 평가를 요청한다.

```text
ordinary offense predicate
→ one occurrence

explicit legal cross-occurrence route
→ specified occurrence tuple
```

모델이 스스로 multi-occurrence mode를 선택할 수 없다.

---

# 14. Article 263

Article 263은 special occurrence producer가 아니다.

예:

```text
occ1: 甲의 B에 대한 injury conduct
occ2: 乙의 B에 대한 injury conduct
```

는 G0에서 일반 factual occurrences로 존재한다.

기존 Article263 orchestration이 이 occurrence catalog 위에서 필요한 injury-occurrence pair를 구성하고:

```text
concurrent_independent_acts
same_object_of_result
causal_origin_unascertained
```

만 dedicated assessment한다.

Grounding에서:

```text
Article263=true
공동정범
offense_ref=263
manual victim map
```

은 만들지 않는다.

---

# 15. Participation / Completion / Concurrence

G0의:

```text
agents=[甲,乙]
```

는 공동정범 판단이 아니다.

Participation은 기존 DSL/runtime가 소유한다.

Completion 역시:

```text
completed
attempt
impossibility
abandonment
```

등을 G0가 출력하지 않는다.

그리고 반드시:

```text
multiple factual occurrences
≠
multiple crimes
```

이다.

법조경합·상상적 경합·실체적 경합 등 **legal concurrence는 DSL 영역**이다.

G0는 그 판단이 가능하도록 factual identity만 보존한다.

---

# 16. Host hard validation

다음은 row/case artifact 전체 failure다.

```text
source에 없는 entity anchor
duplicate canonical entity anchor
invalid entity index
unknown source unit
unordered focal anchors
empty agent set
exact duplicate factual occurrence
model-generated persistent ID
legal/offense field
malformed schema
```

Host는 semantic repair를 하지 않는다.

모델 contract failure 후 다른 answer를 얻기 위한 semantic retry도 하지 않는다.

네트워크/transport failure에 대한 **동일 request 재전송**만 별도로 허용할 수 있다.

---

# 17. Offline factual acceptance

모델 실행 후 host-valid만으로 승인하지 않는다.

각 unique case artifact에 대해 다음만 검수한다.

```text
A. 실제 factual agent가 잘못 연결됐는가?
B. coreference가 잘못됐는가?
C. 서로 다른 conduct가 부당하게 merge됐는가?
D. 하나의 conduct가 불필요하게 split됐는가?
E. same actor / same participant 반복행위가 구분되는가?
F. 동일 case를 사용하는 모든 sub-question이 동일 artifact를 재사용하는가?
G. 서로 다른 occurrence의 evidence가 같은 runtime key로 재결합할 수 있는가?
```

법률상 유무죄는 검수하지 않는다.

Full 26-case experiment를 열려면 **26 sub-question이 참조하는 모든 unique case-level grounding artifact가 PASS**해야 한다.

부분 cohort를 실행하려면 별도 `PARTIAL` 실험이라고 명시한다.

---

# 18. Acceptance 이후 순서

```text
1. Case-Level Factual Grounding prompt/schema/validator 구현
2. unique case_text 수 + exact G0 call count 사전 보고
3. G0 실행
4. case-level factual acceptance
5. occurrence-aware planner regeneration
6. collision audit
7. Call 2 exact target cardinality 재측정
8. token / physical shard count 보고
9. full Call 2
10. CaseTruths
11. DSL → Scallop
12. LiabilityResult validation
13. Call 3
14. 26-case final evaluation
```

기존 `92,098`이나 smoke의 `1,420`은 **새 case-level plan의 최종 cardinality가 아니다.** 새 planner가 생성된 후 다시 측정한다. Smoke가 `CaseTruths → Scallop`까지 실제 연결될 수 있다는 점만은 별도 positive evidence로 유지한다.

---

# 19. 폐기 목록

```text
Unified Call1 factual grounding
question-conditioned occurrence inventory
separate sub-question occurrence artifacts
[甲乙丙丁...] actor regex
all actors × candidates × o1
victim:A
regex event patterns
manual occurrence map
manual Article263 target map
query_relevant filtering
exhaustive entity mention enumeration
result-only occurrence
```

---

## Frozen target architecture

```text
Case-Level G0
  factual entity + occurrence identity
        ↓
cached GroundingArtifact
        ↓
Call 1
  legal routing only
        ↓
Step 7
  DSL closure
        ↓
Occurrence × factual agent × candidate
        ↓
Call 2
  predicate truth
        ↓
CaseTruths
        ↓
DSL / Scallop
        ↓
LiabilityResult
        ↓
Call 3
```

이 스펙의 핵심은 **질문과 무관한 factual identity를 case당 한 번만 만들고, 법률적 의미는 전부 기존 DSL/Scallop 쪽에 남기는 것**이다.
