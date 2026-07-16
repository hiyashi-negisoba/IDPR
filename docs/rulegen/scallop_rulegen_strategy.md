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
  -> API: RuleIR draft
  -> deterministic RuleIR + NormCard-link validator
  -> deterministic Scallop compiler
  -> golden tests
  -> human legal review
  -> active policy + verified promotion
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

## Predicate 설계

법률 요건과 사건 사실을 같은 predicate로 합치지 않는다. 원문에서 추출한
`*_fact(fact_id, ...)`와 증거능력 판단 결과인 `provable(fact_id)`를 결합해
`proven_*`을 만든 뒤에만 실체법 rule이 소비한다. 이 구조가 위법수집증거·전문증거가
사기죄 결론에 곧바로 들어가는 것을 막는다.

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
`data/rulegen/fraud/fraud_rule_ir_exemplar.json`은 다음을 보여 주는 모범 초안이다.

- 모든 실체법 사실이 `provable(fact_id)`를 통과하는 bridge
- 기망→착오→처분→취득의 인과 사슬
- 피고인·피기망자·소유자·수익자 역할 분리
- `재산상 손해`와 `불법영득의사`를 묵시적으로 확정하지 않는 policy variant
- `active_policy("kr_fraud_damage_and_unlawful_intent")`가 있어야만 최종 결론 도출
- source quote가 실제 commentary substring인지 검사하는 provenance gate
- predicate/rule의 source quote가 연결 NormCard 범위를 벗어나지 못하는 provenance gate

현재 exemplar는 일부러 `draft/pending`이다. 제347조 주석 자체가 재산상 손해와
불법영득의사의 독립요건성에 견해 대립을 기록하므로, 이 선택을 모델이나 개발자가
임의로 `verified`로 승격할 수 없다.

### 제347조 전체 준비 현황

2026-07-16 기준 사기죄 주석서 13개 배치에서 검증 후보 662개를 확보했고, 후보 계보를
보존한 NormCard 636개로 정규화했다. 주석서가 보고한 판례로 추정되는 카드는 원판례
확인 전 `context_only`로 제한했다. Sol 최종 비평 17개 묶음은 모두 계약 검증을
통과했으며 67개 검토 지적을 남겼다.

상세 상태는 다음 파일이 단일 진실 원천이다.

- `data/rulegen/fraud/fraud_norm_candidate_manifest.json`
- `data/rulegen/fraud/fraud_norm_card_manifest.json`
- `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- `data/rulegen/fraud/fraud_rule_ir_readiness.json`

전체 RuleIR 생성은 사람 법률 검수 전까지 차단한다. 형식상 61개 카드가 잠정 진입
가능하지만, 사기죄 전체 AND gate를 구성하는 핵심 법리의 출처·권위·정책 선택이
승인되지 않았으므로 부분 카드 수만으로 coverage를 주장하지 않는다.

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
7. 검증된 카드와 `prompts/rulegen_merge_rule_ir.md`로 RuleIR 1.1을 생성한다.
8. `rule_ir.schema.json`과 `idpr.rulegen.validate_rule_ir`로 predicate 및 NormCard 연결을
   검증한다.
9. `idpr.rulegen.compile_rule_ir`로 `.scl`을 생성한다.
10. 성립·불성립·unknown·증거배제·정책 variant별 golden test를 실행한다.
11. 사람이 조문·주석서·판례 원문과 variant를 승인한 뒤에만 canonical predicate와
   `verified` rule로 승격한다.

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
- 법리 대립을 하나의 사실처럼 병합
- `status=verified` 또는 `legal_review=complete` 주장

## 사용자 법률 검수 항목

1. 재산상 손해를 독립한 필수요건으로 둘지
2. 불법영득의사·불법이득의사를 요구하는 사기 유형을 판례 기준으로 어떻게 나눌지
3. 삼각사기의 처분권한·재산상 근접성 predicate 정의
4. 기망·처분·손해·고의 중 standard sub-call 범위
5. strict policy의 이름과 canonical rule 승격 여부

Scallop 문법과 Python 연동은 공식 저장소의
[language examples](https://github.com/scallop-lang/scallop#scallop-language)와
[`ScallopContext` example](https://github.com/scallop-lang/scallop#using-scallopy)을
기준으로 했다. 현재 workspace에는 `scallopy`/`scli` runtime이 설치되어 있지 않아
이번 산출물은 schema·provenance·정적 compiler 테스트까지 검증한다.
