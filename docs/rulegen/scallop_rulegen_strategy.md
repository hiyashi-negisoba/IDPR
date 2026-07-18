# Commentary-to-Scallop rule generation strategy

## 결정

API 모델이 주석서 원문에서 `.scl`을 바로 생성하게 하지 않는다. 모델은 먼저 출처가
붙은 규범 후보를 추출한다. 검증된 후보를 독립 검수 단위인 NormCard로 병합한 다음
NormCard에만 근거한 RuleIR을 생성하고, 로컬 compiler가 이를 Scallop으로 변환한다.

```text
issue_tag
  -> explicit (law_id, article_no) target
  -> section-preserving commentary batches
  -> API: NormCandidateBatch[]
  -> deterministic candidate provenance validation
  -> API: advisory legal critic
  -> source-bounded finding adjudication
  -> validated minimal candidate patch
  -> API: NormCardSet merge
  -> deterministic NormCard validation
  -> human-approved aggregate core
  -> API: RuleIR draft
  -> deterministic RuleIR + full-generation-contract validator
  -> agent rule-by-rule audit + long-form natural-language explanation
  -> human legal review
  -> API: advisory Sol critic
  -> human re-review
  -> deterministic Scallop compiler + runtime/golden tests
```

의미검색, embedding, reranker, KCL `rubric_summary`는 rule source와 target 선택에
사용하지 않는다. KCL 문항은 rule 완성 후 평가와 golden-case 설계의 독립성 확인에만
사용한다.

## 대상 pool

전체 KCL pool은 `data/commentary/kcl_criminal_v1_commentary_pool.json`이 단일 진실
원천이다. 사기죄 exemplar는 정확히 `commentary://001692/제347조` 아래 127개 chunk,
약 14.4만 자를 사용한다. `section_path`를 보존하면서 요청당 최대 12,000자로 묶는다.
생성된 실제 요청은 `data/rulegen/fraud/fraud_rulegen_requests.jsonl`에 있다.

제347조의 핵심 section은 다음처럼 역할이 다르다.

| section | 역할 | 처리 |
|---|---|---|
| `Ⅰ` | 전체 구성요건과 인과 사슬 | rule skeleton |
| `Ⅳ.1` | 기망 | open-textured standard |
| `Ⅳ.2` | 착오 및 기망→착오 인과 | standard + causal link |
| `Ⅳ.3` | 처분행위 및 착오→처분 인과 | standard + causal link |
| `Ⅳ.4` | 재산상 손해와 학설 대립 | named policy variant |
| `Ⅳ.5` | 재물 교부·이익 취득 | rule fact, beneficiary 분리 |
| `Ⅴ.1` | 고의 | standard judgment |
| `Ⅴ.2` | 불법영득·이득의사 대립 | named policy variant |
| `Ⅶ.1` | 실행의 착수 | 별도 attempt rule set |
| `Ⅷ` | 공범 | 형법총칙 corpus 확보 후 별도 rule set |

## NormCard와 RuleIR의 경계

`NormCandidateBatch`는 한 API batch 안에서 추출한 원시 후보다. 중복 후보나 서로 다른
학설이 섞일 수 있어 RuleIR이 직접 소비하지 않는다. `NormCardSet`은 후보를 병합하되
다음 정보를 보존하는 법률 검수 checkpoint다.

NormCandidate의 `norm_kind`와 `polarity`는 독립 차원이다. `norm_kind`는 element,
standard, variant, exception 같은 기능을 나타내고, `polarity`는 positive, negative,
exception을 나타낸다. 일반적 불성립 규범을 전부 exception으로 분류하지 않는다.

- 독립적으로 검토 가능한 하나의 proposition
- exact commentary quote와 이를 공급한 API request ID
- `deterministic_rule`, `standard_input`, `policy_variant`, `context_only` 구분
- 주석서 종합, 주석서가 보고한 판례·학설, 주석서에 인용된 법문이라는 권위 성격
- 학설 대립 여부, variant group, 사람 검수 필요 여부

NormCardSet 1.1은 모든 카드에 `candidate_refs(request_id, candidate_id)`를 강제한다.
따라서 병합 단계가 후보를 조용히 누락할 수 없고, 카드의 exact quote도 연결 후보의
source_refs 합집합 안에 있어야 한다. 서로 다른 `norm_kind` 또는 `polarity`를 가진
후보를 한 카드에 병합하면 validator가 실패한다.

RuleIR 1.1의 모든 commentary-origin predicate와 rule은 `norm_card_ids`를 가져야 한다.
RuleIR의 인용은 연결된 카드가 가진 exact source reference의 합집합을 벗어날 수 없다.
판례를 우선하는 정책도 주석서의 판례 설명만으로 확정하지 않고, 사용자 판례 index의
원문을 대조한 후 활성화한다.

## Scallop 승격과 판례 검색의 경계

NormCard를 모두 Scallop 규칙으로 컴파일하지 않는다. 역할을 다음 네 층으로 분리한다.

| 층 | 대상 | 런타임 역할 |
|---|---|---|
| core rule | 구성요건 연결, 정의, 명시적 인과관계, 검증된 예외 | Scallop의 AND gate와 파생 규칙 |
| grounding standard | 기망, 고의, 실질적 인과관계처럼 평가가 필요한 기준 | neural/RAG 판단이 positive, negative, unknown fact를 생성 |
| policy variant | 학설 대립 또는 판례 선택이 필요한 규범 | 이름 있는 policy branch로 유지하고 승인 후 활성화 |
| retrieval case | 구체적 당사자, 거래, 절차와 결론을 담은 판례 적용례 | 판례 index에서 검색하여 grounding 모델의 판단 근거로만 사용 |

`deterministic_rule`만 core rule 승격 후보가 된다. `standard_input`은 RuleIR에서 입력
predicate의 의미와 판단 질문을 정의할 수 있지만, 그 자체를 결론 도출 규칙으로
컴파일하지 않는다. `context_only`인 판례 카드는 `.scl`에 들어가지 않는다. 검색된
판례의 구체 사실도 Scallop fact로 그대로 주입하지 않고, 현재 사건에 대한 grounding
결과와 근거 인용을 생성하는 데만 사용한다.

판례 카드에서 일반 규칙을 승격하려면 다음을 모두 만족해야 한다.

1. 특정 사건의 고유명사와 우연한 사실을 제거해도 법적 조건과 결론이 유지된다.
2. 조건을 현재 사건에서 관찰하거나 neural standard로 판단할 predicate로 표현할 수 있다.
3. 원판례 또는 현행 법령으로 권위와 적용 범위를 확인했다.
4. 반대 판례, 예외 및 학설 대립을 확인해 policy 선택을 숨기지 않았다.
5. 성립, 불성립, 경계 및 unknown golden case를 만들 수 있다.

따라서 세부 판례가 많다는 이유로 600여 개의 사건별 규칙을 만드는 것이 목표가 아니다.
소수의 구조적 core rule이 일관성을 담당하고, 판례 검색과 neural grounding이 개방형
요건의 사실평가를 담당한다. Scallop은 검색 결과 자체가 아니라 검증 가능한 구조화
판단을 소비한다.

## Predicate 설계

법률 요건과 사건 사실을 같은 predicate로 합치지 않는다. 현재 사기죄 계약에서 neural
grounding은 사건별 `StandardAssessment`를 만들고, commentary-origin 입력은
`(case_id, assessment_id, ..., status)` 구조를 갖는다. `status`는 `satisfied`,
`not_satisfied`, `unknown` 중 하나다. 실체법 rule은 같은 사건·평가 ID의
`provable(case_id, assessment_id)`가 함께 있을 때만 이를 소비한다. 이 구조가
위법수집증거·전문증거처럼 절차 게이트를 통과하지 않은 판단이 사기죄 결론에 곧바로
들어가는 것을 막는다.

행위자 역할도 분리한다. 최소한 `defendant`, `deceived`, `owner`, `asset`,
`beneficiary`를 유지해야 피기망자와 재산상 피해자가 다른 삼각사기를 잘못 합치지
않는다. 처분권한 또는 재산상 근접성은 법률 검수 후 별도 predicate로 추가한다.

`rule`과 `standard`의 경계는 다음과 같다.

- `rule`: 관계가 명시적으로 열거되고 boolean 조합으로 계산 가능한 경우
- `standard`: 신의칙 위반인 기망, 실질적 인과관계, 재산상 손해, 고의처럼 평가가 필요한 경우
- standard는 API sub-call의 판단값·근거·confidence를 입력 fact로 받을 뿐 Scallop이
  스스로 도출하지 않는다.

## 부정과 미확인 사실

closed-world assumption으로 “추출되지 않음”을 “요건 없음”으로 처리하면 안 된다.
각 필수요건은 `true`, `false`, `unknown` 중 하나로 관리하거나, 최소 구현에서는
긍정·부정 predicate를 별도로 두고 둘 다 없으면 결론을 `undetermined`로 유지한다.
Scallop negation은 완전성이 선언된 relation에만 허용한다.

절차법은 범죄 구성요건처럼 한 줄의 AND 목록으로 만들면 안 된다. `event_id`, 집행
주체와 권한, 영장 또는 예외 근거, 대상·범위·관련성, 통지·참여, 사후영장, 시간적
선후관계를 먼저 fact로 만들고 다음 세 층을 분리한다.

1. `procedure_satisfied(event)` 또는 구체적 위반을 도출하는 절차 rule
2. 위반의 중대성·인과 단절 같은 standard 판단
3. `hearsay_gate_satisfied`, `collection_gate_satisfied` 등 증거별 positive gate

모든 필요한 검토가 끝났다는 `admissibility_review_complete(e)`가 있고 각 positive
gate가 충족된 경우에만 `admissible(e)`를 만든다. 참고 구현은
`rules/exemplars/procedural_gate_v1_candidate.scl`이며, 기존 bootstrap처럼 “배제 사실이
발견되지 않았으므로 admissible”이라고 추론하지 않는다.

## 사기죄 exemplar

`data/rulegen/fraud/fraud_norm_card_set_exemplar.json`과
`data/rulegen/fraud/fraud_rule_ir_exemplar.json`은 초기 8장 역사적 초안이다. 다음
구조를 탐색하는 데 사용했지만, 현재 88장 생성의 substantive few-shot으로는 쓰지 않는다.

- 모든 실체법 사실이 `provable(fact_id)`를 통과하는 bridge
- 기망→착오→처분→취득의 인과 사슬
- 피고인·피기망자·소유자·수익자 역할 분리
- `재산상 손해`와 `불법영득의사`를 묵시적으로 확정하지 않는 policy variant
- `active_policy("kr_fraud_damage_and_unlawful_intent")`가 있어야만 최종 결론 도출
- source quote가 실제 commentary substring인지 검사하는 provenance gate
- predicate/rule의 source quote가 연결 NormCard 범위를 벗어나지 못하는 provenance gate

현재 생성에는 사용자 검수를 마친
`data/rulegen/fraud/fraud_core_norm_card_set.json`을 사용한다. 이전 초안의 손해 및
불법영득의사 policy를 복사하지 않도록, API에는 두 카드만 사용한
`fraud_rule_ir_generation_fewshot.json`을 구조 예시로 제공한다. 이 예시는 3상태,
`provable`, 역할 인자, 출처 연결만 가르치며 사기죄 법리 전체를 대표하지 않는다.

### 제347조 전체 준비 현황

2026-07-18 기준 사기죄 주석서 13개 배치에서 검증 후보 661개를 확보했고, 합쳐진 학설
카드를 분리하여 후보 계보를 보존한 NormCard 646개로 정규화했다. Sol 최종 비평
17개 묶음의 67개 지적은 원문과 대조하여 57개를 직접 수정하고 10개를 기각했다.
이 정정에는 API를 사용하지 않았다.

상세 상태는 다음 파일이 단일 진실 원천이다.

- `data/rulegen/fraud/fraud_norm_candidate_manifest.json`
- `data/rulegen/fraud/fraud_norm_card_manifest.json`
- `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- `data/rulegen/fraud/fraud_core_rule_review_queue.json`
- `data/rulegen/fraud/fraud_core_rule_selection_audit.json`
- `data/rulegen/fraud/fraud_core_rule_human_review_audit.json`
- `data/rulegen/fraud/fraud_policy_resolution_audit.json`
- `data/rulegen/fraud/fraud_rule_ir_readiness.json`

전수 core 범위 감사와 사용자 검수 결과 28개 `deterministic_rule`과 60개
`standard_input`을 승인된 실행 core로 남기고, 구체 판례 결과·학설·희귀 적용례 등
558개는 RAG 또는 future-work 문맥으로 분리했다. 죄수와 미필적 고의·공범 이탈 등
형법총칙 쟁점은 총칙 corpus 확보 전에는 사기죄 core에 넣지 않는다.
기존 12개 정책 그룹은 주석서와 로컬 원판례 15건을 대조하여 판례 우선 규칙 또는
RAG로 모두 해소했다. 원래 core 후보 118개 중 사용자가 24개를 RAG, 10개를 narrow,
3개를 reject, 1개를 duplicate로 표시했다. 교차검토에서 소송사기 전용 2개를 RAG로
보내고 3개 문구를 추가로 좁혔다. 차용금 편취 범의 판단 규칙은 일반성이 있어 유지하고
중복된 일반형 카드만 RAG로 내렸다. API를 쓰지 않고 88장을 하나의 reviewed aggregate로
묶고, 전체 RuleIR request·구조 few-shot·10항목 사전 검수표·실행 차단 runner를 만들었다.
현재 사용자 사전 검수가 pending이므로 Terra 호출은 0회이며 전수 RuleIR도 아직 생성하지
않았다.

## API 실행 순서

1. `fraud_rulegen_requests.jsonl`의 각 행과
   `prompts/rulegen_extract_norm_candidates.md`를 structured-output API에 전달한다.
2. 응답을 `norm_candidate_batch.schema.json`과
   `idpr.rulegen.validate_norm_candidate_batch`로 검증한다.
3. 검증된 응답만 Sol critic에 보내되 critic은 수정 권한을 갖지 않는다. finding은
   `comment_id`, `section_path` locator 범위 안에서만 반환한다.
4. critic finding을 원문과 대조해 수용, 기각, RAG context 유보로 adjudicate한다.
   수용된 수정은 전체 batch 재생성보다 `NormCandidatePatch`로 최소 적용하고 전체
   provenance를 다시 검증한다.
5. 검증된 응답만 `prompts/rulegen_merge_norm_cards.md`로 NormCardSet에 병합한다.
6. `norm_card_set.schema.json`과 `idpr.rulegen.validate_norm_card_set`으로 exact quote,
   request provenance, variant 표시를 검증한다.
7. 사용자가 88장 scope, 3상태, 증거 게이트, 역할 인자, 결론 인터페이스, open-world,
   few-shot, 실행 순서와 API ceiling을 승인한다.
8. 승인된 aggregate와 `prompts/rulegen_merge_rule_ir.md`를 Terra 단일 호출에 전달한다.
   동시성 1, retry 0이며 이 단계에서 Sol을 호출하지 않는다.
9. `rule_ir.schema.json`, `validate_rule_ir`, `validate_full_rule_ir_generation`으로 exact
   scope, 88장 coverage, predicate closure, case isolation, 명시적 status, 증거 게이트,
   네 결론의 실제 구현을 검증한다.
10. 에이전트가 모든 predicate와 rule을 법리·구조 양쪽에서 검토하고, 각 입력·AND gate,
    성립·불성립·unknown·conflict 경로와 RAG 경계를 설명하는 장문 자연어 해설을 쓴다.
11. 사용자가 원본 RuleIR, coverage 표, 에이전트 해설을 함께 검수한다.
12. 그 승인 뒤에만 Sol critic을 한 번 실행하고, 지적을 사용자가 다시 검수한다.
13. 재검수 완료 뒤에만 `compile_rule_ir`로 `.scl`을 생성하고 runtime/golden test를
    실행한다. 모델의 JSON이나 critic 수정안을 직접 실행하지 않는다.

critic의 finding 수를 억지로 0으로 만들기 위해 재생성하지 않는다. 지적은 출처와
대조해 자동 구조 수정, 사람 법률 검수, 기각으로 adjudicate한다. 열거된 판례 사실과
적용례가 독립 규범을 제공하지 않으면 commentary/precedent RAG context로 남긴다.
critic이 구체 내용을 제시하지 않은 반대설을 요구해도 모델이 이를 발명하지 않고
unresolved question으로 보존한다.

## 자동 실패 조건

- source scope 밖 `comment_id`
- commentary에 존재하지 않는 quote
- `norm_kind=exception`인데 `polarity=exception`이 아닌 후보
- 존재하지 않는 candidate를 제거하거나 기존 ID를 덮어쓰는 patch
- NormCard source가 선언된 extraction request 범위 밖에 있음
- NormCard가 validated candidate를 누락하거나 알 수 없는 candidate를 참조
- 서로 다른 `norm_kind` 또는 `polarity` 후보를 한 NormCard에 병합
- RuleIR source가 연결된 NormCard의 source 범위 밖에 있음
- 선언되지 않은 predicate 또는 arity/type 불일치
- positive body에 바인딩되지 않은 head/negation 변수
- 모델이 standard를 derived rule로 생성
- 증거 gate를 우회하는 실체법 입력
- 한 rule 안에서 서로 다른 case 변수를 결합
- status 변수를 사용하거나 허용된 세 값 밖의 status를 소비
- 입력 predicate 또는 네 결론 predicate를 선언만 하고 rule에서 사용·구현하지 않음
- 법리 대립을 하나의 사실처럼 병합
- RuleIR의 `status=verified` 또는 `legal_review=complete` 주장

## 사용자 법률 검수 항목

현재 생성 전 검수는 `fraud_rule_ir_generation_prep_review_guide.md`의 10개 항목을
기준으로 한다. 핵심은 88장 core/558장 RAG 경계, 단일 호출, 3상태 StandardAssessment,
`provable` 게이트, 삼각사기 역할 인자, 네 결론 인터페이스, open-world, 구조 few-shot,
검수 순서, API ceiling이다. 생성 후에는 별도의 규칙별 장문 해설과 원본 RuleIR을 함께
검수하며, Sol finding은 독립된 두 번째 검수 대상으로 둔다.

Scallop 문법과 Python 연동은 공식 저장소의
[language examples](https://github.com/scallop-lang/scallop#scallop-language)와
[`ScallopContext` example](https://github.com/scallop-lang/scallop#using-scallopy)을
기준으로 했다. 현재 workspace에는 `scallopy`/`scli` runtime이 설치되어 있지 않아
이번 산출물은 schema·provenance·정적 compiler 테스트까지 검증한다.
