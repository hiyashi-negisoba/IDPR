# IDPR 연구 잠정안

> 상태: working draft
>
> 작성일: 2026-07-15
>
> 주 태스크: KCL 한국 형사법 61개 설문의 long-form answer generation
>
> 핵심 목표: 생성 문서의 사실, 법적 논증, symbolic derivation과 결론 사이의 정합성

## 0. 핵심 결정

IDPR의 주 연구 대상은 **한국 형사법 사례형 61개 설문에 대한 long-form generation**이다.
IRAC은 기본 출력 형식 후보이지만, 논문의 본질은 특정 문서 형식이 아니라 다음
self-consistency를 보장하는 데 있다.

```text
사실관계
  <-> 구성요건·절차요건 판단
  <-> 법적 논증 경로
  <-> 최종 결론
```

여기서 self-consistency는 여러 응답을 샘플링해 다수결하는 방법을 뜻하지 않는다.
한 문서 안의 argument, derivation, conclusion이 서로 모순되지 않는
**argument-derivation-conclusion consistency**를 뜻한다.

FactGraph, 판례·주석 RAG, standard assessment와 Scallop은 별도 최종 태스크가 아니다.
KCL long-form 답안을 안정적으로 생성하기 위한 내부 파이프라인이다.

```text
KCL 사례형 설문
  -> FactGraph extraction
  -> commentary/precedent RAG
  -> predicate-level standard assessment
  -> Scallop derivation
  -> derivation-conditioned long-form generation
  -> back-parse verification and refinement
```

워크샵 논문도 이 long-form generation 태스크를 중심으로 한다. 이전 DCDE/OBJECTION과는
연구 동기와 failure analysis를 계승하지만, 데이터와 주 태스크는 별개다.

## 1. 장기 프로젝트와 워크샵 논문의 관계

### 워크샵 논문

- 데이터: KCL 한국 형사법 설문 61개
- 출력: 설문별 IRAC 또는 구조화된 long-form 법률 답안
- 방법: RAG-grounded neuro-symbolic generation and verification
- 핵심 평가: 법률 정답성뿐 아니라 논증-결론 정합성
- 범위: 현재 commentary·판례·rule coverage 안에서 실체법과 절차법을 함께 다룸

### 장기 IDPR

- 더 많은 죄종, 형법총칙, 특별법, 판례 corpus로 확장
- 실제 수사기록처럼 출처와 당사자 주장이 충돌하는 입력으로 확장
- paragraph-level verification과 targeted edit 고도화
- Natural Innocent 중 죄명 정렬이 가능한 사례를 실체법 중심 외부 전이·LJP 평가로 확장
- 한국법 외 법역 또는 다른 법률 long-form task로 확장

따라서 워크샵 논문은 장기 프로젝트의 주변 실험이 아니라 **첫 번째 완결된 IDPR
long-form 실험**이다.

## 2. DCDE/OBJECTION과의 연결

### 2.1 계승하는 문제의식

DCDE의 OBJECTION 연구는 공소사실 중심 입력의 guilty bias와 LLM의 Doctrinal
Hierarchy Gap을 다뤘다. 구성요건 해당성, 위법성, 책임의 세 단계마다 asymmetric
Lawyer agent가 피고인에게 유리한 사실 기반 반론을 제시하고 Judge가 판단을 수정했다.

이 연구는 다음을 보여줬다.

- 단순 direct prompting과 일반 Self-Refine은 guilty bias를 충분히 교정하지 못함
- 법률적 단계 구조와 역할 비대칭이 False Guilty Rate 감소에 기여함
- 일반 critic보다 법률 domain-specific defense가 중요함
- 입력 사실의 유리·불리 정보와 사실 근거 critique가 필요함

### 2.2 IDPR의 직접 동기

DCDE의 내부 rebuttal 분석에서 false-acquittal 404건 중 약 68%는 단계별 reasoning이
구성요건 성립을 인정하면서 최종 label이 무죄로 뒤집히는 verdict-reasoning
inconsistency를 보였다. 약 26%는 사기·횡령의 주관적 구성요건을 반증 없이 부정했다.

이 failure는 prompt 안에서 legal structure를 설명하는 것만으로는 결론을 reasoning에
완전히 결박할 수 없음을 보여준다.

```text
DCDE/OBJECTION:
  structured critique improves model reasoning and reduces false guilty predictions

IDPR:
  compute an explicit derivation before generation,
  bind each paragraph and conclusion to that derivation,
  and verify the generated document against it
```

### 2.3 별개 논문인 이유

| DCDE/OBJECTION | IDPR workshop paper |
|---|---|
| Legal Judgment Prediction | KCL long-form answer generation |
| Natural Innocent 사실관계 기반 LJP | 한국 변호사시험 형사법 61개 설문 |
| OUC label과 verdict | 구성요건·절차요건 derivation과 IRAC 문서 |
| Multi-agent defense intervention | RAG + Scallop + generation verification |
| FGR/FNR 중심 | legal score + consistency violations 중심 |
| 모델이 단계 판단과 label 생성 | symbolic layer가 결론을 계산 |

DCDE 데이터는 IDPR의 main experiment에 합치지 않는다. 다만 Natural Innocent에서
KCL inventory 또는 IDPR rule DB의 죄명과 정렬되는 사례를 찾을 수 있다면, 다음 단계의
별도 태스크로 재구성할 수 있다.

- 입력 사실에서 FactGraph와 실체법 predicate를 추출하는 외부 전이 평가
- 동일 죄명의 commentary·판례 RAG와 Scallop rule을 재사용하는 LJP
- reasoning과 verdict의 정합성을 검사하는 DCDE-style diagnostic

Natural Innocent 입력은 기본적으로 사실관계 중심이므로, 기록의 증거능력·수집 절차와
같은 정보가 별도로 확인되지 않는 한 형사절차 gate의 성능 근거로 사용하지 않는다.
따라서 이 확장은 **실체법 중심 secondary study**이며, KCL 61개 long-form main
experiment와 결과를 합산하지 않는다.

## 3. 문제 정의

### 3.1 입력

각 평가 단위는 KCL 형사법 사례형의 설문 하나다.

- 공통 사실관계
- 설문별 질문
- 해당 설문의 issue tags
- 실체법, 절차법 또는 mixed 구분

KCL rubric은 평가에만 사용한다. Rule이나 RAG source로 사용하지 않는다. Commentary와
판례에서 rule을 만들고 KCL은 독립 평가셋으로 유지한다.

### 3.2 출력

기본 출력은 설문에 답하는 long-form 법률 문서다. 형식은 다음을 포함해야 한다.

1. Issue: 검토할 법적 쟁점
2. Rule: 적용 법리와 출처
3. Application: 유리·불리 사실을 고려한 포섭
4. Conclusion: derivation과 일치하는 설문별 결론

문단마다 다음 내부 metadata를 함께 유지한다.

- `paragraph_id`
- `predicate_ids`
- `rule_ids`
- `fact_ids`
- `authority_refs`
- `required_conclusion`

사용자에게 보이는 최종 문서는 자연스러운 long-form이지만, 생성·검증 과정은 이
구조화 metadata를 사용한다.

### 3.3 목표 정합성

IDPR이 줄이려는 오류는 다음과 같다.

- 필수 구성요건을 논증에서 누락
- 본문에서 인정한 요건과 반대되는 결론
- Rule DB나 판례 근거가 없는 법리 주장
- 사실관계에 없는 사실 추가
- 배제된 증거를 실체법 논증에 사용
- 학설을 판례처럼 사용
- 미확인 사실을 부존재로 단정
- 설문별 결론과 전체 결론의 불일치

## 4. 제안 파이프라인

### 4.1 Stage 0: Inventory-guided issue routing

61개 설문의 승인된 `issue_tags`와 `legal_area`를 이용해 필요한 commentary, 판례,
predicate schema와 rule set을 선택한다.

Issue routing에는 의미검색을 사용하지 않는다. Inventory의 명시적 tag와
`(law_id, article_no)` mapping을 사용한다. 의미검색은 선택된 법률 범위 안에서
구체적 판례를 찾는 Stage 2에만 사용한다.

### 4.2 Stage 1: FactGraph extraction

Neural extractor는 사례 사실을 풍부한 typed feature로 변환한다. 최종 법률 결론은
출력하지 않는다.

#### 사실 상태

KCL 사례형의 서술자는 일반적으로 주어진 사실을 제시하므로 기본 상태는 `given`이다.
다만 사례 안의 진술·주장·부인과 증거관계는 별도로 표현한다.

- `given`
- `asserted_by_actor`
- `disputed`
- `unknown`

#### 증명·절차 상태

- `supported_by(evidence_id)`
- `admissibility_pending`
- `provable`
- `excluded`
- `insufficient`

#### 쟁점별 방향

- `supports(issue_id)`
- `rebuts(issue_id)`
- `neutral(issue_id)`

유리·불리 여부는 fact의 고정 label로 두지 않는다. 같은 사실이 고의에는 불리하고
위법성 인식에는 유리할 수 있으므로 issue-relative edge로 표현한다.

예시:

```text
fact(f17, "A는 계약 체결 당시 변제 자력이 없었다")
given(f17)
supports(f17, deception)
supports(f17, intent_to_defraud)

fact(f18, "A는 계약 후 일부 금액을 변제하였다")
given(f18)
rebuts(f18, intent_to_defraud)
```

Extractor는 긍정 사실뿐 아니라 반대 사실과 missing fact를 함께 출력한다. 이것이
Application 문단에서 양방향 논증을 만들고 standard 판단의 과신을 줄이는 기반이다.

### 4.3 Stage 2A: Offline norm compilation

Commentary와 판례 index에서 issue별 NormCard와 RuleIR을 미리 구축한다.

NormCard는 다음을 포함한다.

- 적용 조문
- 구성요건과 정의
- 인과관계
- 예외와 절차 요건
- 평가가 필요한 standard
- 판례가 채택한 법리와 적용 범위
- 판례가 채택하지 않은 학설 variant
- 인정·부정 판례의 구별 사실
- 원문 citation과 기준 시점

API 모델이 `.scl`을 직접 만들지는 않는다. Source-grounded NormCandidate를 먼저
추출하고, 이를 독립 검수 단위인 NormCard로 병합한다. RuleIR의 각 predicate와 rule은
근거 NormCard를 명시해야 하며, 로컬 validator와 deterministic compiler가 Scallop
candidate를 만든다.

실무 지향 원칙은 다음과 같다.

```text
현행 법령과 현재 대법원 판례
  > 판례가 채택하지 않은 학설
```

현재 제347조 준비 실행은 13개 주석서 배치의 후보 661개와 최종 NormCard 646개까지
완료했다. 이 실행은 offline norm compilation의 실제 설계·실패 양상을
확인하기 위한 사기죄 exemplar이며, KCL 61개 long-form generation이라는 main task를
대체하지 않는다. Sol의 최종 지적 67개와 원래 core 후보 118개에 대한 사람 검수를
완료하여, 28개 deterministic rule과 60개 standard input의 전체 RuleIR 생성 게이트가
열렸다. 기존 8장짜리 RuleIR/Scallop은 전수 생성 전까지 구조 예시로 사용한다.

646개 카드를 모두 규칙으로 컴파일하지 않는다. 구조적 구성요건과 검증된 예외만
Scallop core rule 후보로 두고, 개방형 standard는 neural grounding predicate의 사양으로,
구체 판례 적용례는 precedent RAG context로 사용한다.

학설은 설명과 audit를 위해 `alternative_only`로 보존한다. Canonical conclusion에는
현재 판례를 연결한다.

### 4.4 Stage 2B: Precedent/commentary RAG

FactGraph에서 활성화된 issue와 standard에 대해 관련 법리를 검색한다.

1. 조문, issue tag, 법원, 선고일, 판례번호로 metadata filter
2. Filter 안에서 semantic retrieval
3. 유사 사실관계 reranking
4. 판례 권위, 최신성, 적용 범위 확인

각 standard에는 한쪽 결론의 판례만 제공하지 않는다.

- 요건을 인정한 판례
- 요건을 부정한 판례
- 사실은 유사하지만 결론이 다른 판례
- 현재 사안을 구별하는 핵심 사실

Commentary는 법리 구조와 판례 index 연결에 사용하고, canonical 판단은 실제 판례
원문을 우선한다.

### 4.5 Stage 2C: Standard assessment

기망, 처분행위, 고의, 중대한 절차 위반처럼 평가가 필요한 predicate는 모델이
FactGraph와 authority packet을 바탕으로 판단한다.

```text
StandardAssessment:
  predicate_id
  status: satisfied | not_satisfied | unknown
  supporting_fact_ids[]
  opposing_fact_ids[]
  missing_fact_ids[]
  authority_refs[]
  distinguishing_facts[]
  review_required
```

모델은 죄 전체의 최종 성립 여부를 직접 출력하지 않는다. 각 standard의 성부와 근거만
출력한다. 한 설문에서 관련 standard들을 하나의 structured call로 평가할 수 있으므로
구성요건마다 별도 API call을 만들 필요는 없다.

### 4.6 Stage 3: Scallop derivation

Scallop은 검증된 fact와 standard assessment를 rule graph로 조합한다.

사기죄 예시:

```text
fraud_established =
  proven_deception
  AND proven_mistake
  AND proven_deception_mistake_causal
  AND proven_disposition
  AND proven_mistake_disposition_causal
  AND proven_acquisition
  AND proven_intent
```

Scallop의 역할은 다음과 같다.

- AND/OR 및 인과관계 조합
- 실체법과 절차법 rule 연결
- 판례 policy와 예외 branch 적용
- missing fact 전파
- proof tree와 fired rule 기록
- 설문별 결론 계산

`unknown`을 false로 collapse하지 않는다. 필요한 positive fact가 없으면 요건은
통과하지 않지만, 부존재가 확인되지 않았다면 `undetermined` 원인을 남긴다.

#### 절차법 positive gating

```text
개별 절차 준수·위반
  -> 위반의 중대성·치유·인과 단절 standard
  -> 증거별 positive gate
  -> admissible(e)
  -> provable(f)
  -> 실체법 rule
```

배제 사실이 검색되지 않았다는 이유만으로 적법성을 인정하지 않는다. 필요한 검토가
완료되고 positive gate가 충족되어야 그 증거가 실체법 fact를 활성화한다.

### 4.7 Stage 4: Derivation-conditioned long-form generation

Derivation을 먼저 paragraph plan으로 변환한다.

```text
ParagraphPlan:
  issue
  governing_rules[]
  supporting_facts[]
  opposing_facts[]
  standard_assessments[]
  required_conclusion
  source_refs[]
```

Generator는 plan에 없는 결론을 새로 선택하지 않는다. 각 문단은 어떤 predicate와
rule을 설명하는지 metadata로 남긴다.

긴 답안에서는 다음 순서를 기본으로 한다.

1. 설문별 쟁점과 검토 순서
2. 판례 중심 법리
3. 인정 방향 사실과 반대 방향 사실
4. 해당 standard의 판단
5. derivation과 동일한 소결론
6. 설문 전체 결론

IRAC은 이 정보를 표현하는 기본 template이지만, 문단 수와 세부 구조는 설문의 복잡도에
따라 달라질 수 있다.

### 4.8 Stage 5: Back-parse verification and refinement

생성 문서를 문단별로 다시 predicate로 파싱하고 원 derivation과 비교한다.

- `missing`: derivation에 있는 필수 판단이 문서에 없음
- `contradiction`: 문서의 판단이 derivation과 반대
- `unsupported`: derivation 또는 authority에 없는 주장
- `fact_hallucination`: 입력에 없는 사실 추가
- `inadmissible_use`: 배제증거에 의존
- `authority_mismatch`: 학설·하급심을 canonical 판례처럼 사용

Hard failure가 있으면 전체 문서를 다시 쓰지 않고 해당 문단만 targeted edit한다.
Best-of-N을 사용하는 경우에도 LLM judge만으로 rerank하지 않고 consistency violation을
우선한다.

## 5. 데이터와 현재 scope

### 5.1 KCL 형사법 61개 설문

현재 inventory는 KCL essay parquet의 형사법 61개 row를 설문 단위로 정규화했다.

- 전체 설문: 61개
- 실체법: 26개
- 절차법: 33개
- mixed: 2개
- unique issue tags: 165개
- 전체 tag assignment: 207개
- 설문 분리, issue tag, legal area: 사용자 승인 완료
- rule coverage: 61개 모두 현재 `covered=false`, 검토 대기

61개 전부가 main evaluation universe다. Rule coverage가 부족한 문항을 조용히 제외하지
않는다.

### 5.2 Coverage tier

모든 issue가 같은 정도로 symbolic하게 구현되지는 않는다. 이를 숨기지 않고 tier로
보고한다.

- `Tier A`: 구성요건과 예외가 verified Scallop rule로 구현됨
- `Tier B`: rule skeleton과 RAG-grounded standard가 결합됨
- `Tier C`: 직접 rule이 부족해 coarse standard assessment와 `review_required`를 사용
- `Tier U`: 필요한 법령·판례 source가 없어 unknown 또는 unsupported

전체 61개 성능과 함께 tier별 성능, coverage-consistency curve를 보고한다. Coverage는
평가 결과를 좋게 만들기 위한 사후 filter가 아니라 실험 변수다.

### 5.3 Commentary pool

현재 commentary source 9,384개 중 inventory tag와 명시적으로 연결된 102개 조문,
3,108개 unique chunk를 대상 pool로 확정했다.

- 형법각칙과 형사소송법 commentary
- parquet chunk 3,103개
- raw PDF fallback 5개
- 의미검색 없이 metadata로 target 확정
- comment ID, 조문, section path, source path 보존

기존 non-mapped 33개를 수동 검토한 결과:

- 현재 corpus에서 완전 해결: 5개
- 범죄 조문은 있으나 형법총칙 gap: 21개
- 특별법 등 필요한 corpus 없음: 7개

형법총칙과 수집 중인 특별법은 future work로 명시한다. Source가 없는 법리를 모델의
기억으로 채우지 않는다.

### 5.4 사기죄 exemplar의 역할

KCL에서 `fraud` tag가 있는 설문은 3개지만, 사기죄는 전체 방법을 설계하는 모범답안으로
사용한다.

- 제347조 commentary 127개
- section-preserving API batch 13개
- 기망 -> 착오 -> 처분 -> 취득 인과 사슬
- 피고인·피기망자·피해자·수익자 역할 분리
- fact와 `provable` evidence bridge
- RAG standard와 Scallop rule의 경계
- 판례와 학설 variant 처리

사기 3개만으로 main result를 만들지는 않는다. 사기 exemplar로 pipeline을 고정한 뒤
61개 설문의 고빈도·공통 predicate와 절차 gate로 확장한다.

## 6. 연구 질문

### RQ1. Derivation conditioning

생성 전에 symbolic derivation을 확정하고 문단 plan을 조건화하면 direct IRAC 또는
plan-then-write보다 argument-conclusion inconsistency가 감소하는가?

**H1:** Derivation-conditioned generation은 contradiction과 missing conclusion을
감소시킨다.

### RQ2. Retrieval-grounded standards

Commentary·판례 RAG에 근거한 standard assessment가 모델 내부 지식만 사용한 판단보다
법률적 정확성과 source faithfulness를 높이는가?

**H2:** Contrastive precedent retrieval은 rubric score와 citation correctness를 높이고
unsupported rule을 줄인다.

### RQ3. Fact representation

인정 방향, 반대 방향, 미확인 사실을 issue별로 분리한 FactGraph가 flat extraction보다
Application의 균형과 standard 판단을 개선하는가?

**H3:** 양방향 fact representation은 반대 사실 누락과 subjective-element 과신을
감소시킨다.

### RQ4. Verification and refinement

Back-parse한 predicate를 derivation과 대조하는 consistency verifier가 LLM judge보다
오류를 잘 찾고, targeted edit가 오류를 줄이면서 정상 문단을 보존하는가?

**H4:** Symbolic verifier 기반 rerank/edit는 동일한 generation budget에서 direct
best-of-N과 Self-Refine보다 consistency score를 높인다.

### RQ5. Evidence gating

절차법 positive gate가 없는 시스템과 비교해 배제증거 사용과 절차·실체 결론 모순이
감소하는가?

**H5:** Evidence gating은 rubric 점수를 해치지 않으면서 inadmissible-use violation을
유의하게 줄인다.

## 7. 실험 설계

### 7.1 비교 시스템

1. `Direct IRAC`: 사실관계와 질문에서 바로 답안 생성
2. `Few-shot IRAC`: 형식과 예시를 제공
3. `Plan-then-write`: 쟁점·결론 plan 후 답안 생성
4. `RAG-only`: commentary·판례를 제공하고 모델이 직접 답안 생성
5. `Self-Refine`: direct 답안을 일반 critique로 수정
6. `Best-of-N + LLM judge`
7. `Doctrinal critique`: DCDE의 법적 단계·방어 critique를 long-form에 맞게 적용
8. `IDPR generate`: FactGraph + RAG + Scallop + conditioned generation
9. `IDPR verify`: IDPR generate + symbolic rerank/targeted edit

DCDE/OBJECTION은 동일 prediction task 결과를 합치는 것이 아니라 long-form baseline의
설계 아이디어로만 공정하게 재구현한다.

### 7.2 핵심 ablation

- Scallop derivation 없이 paragraph plan만 사용
- RAG 없이 모델 내부 지식만 사용
- 판례 없이 commentary만 사용
- opposing facts 제거
- `unknown`을 false로 collapse
- evidence gating 제거
- back-parse verifier 제거
- rerank only vs rerank + targeted edit
- format-only IRAC constraint

### 7.3 평가 protocol

- 동일한 61개 설문을 모든 시스템에 사용
- 동일한 모델·temperature·generation budget을 맞춤
- 모든 API 호출을 prompt hash와 config로 cache
- 각 설문에서 복수 seed 또는 sample을 생성해 run-to-run 변동도 보고
- paired test를 사용하고 61개라는 작은 sample size를 명시
- rubric은 평가에만 사용하며 prompt, RAG, rulegen에 노출하지 않음
- Coverage tier별 결과와 전체 결과를 모두 보고

## 8. 평가 지표

### 8.1 Long-form legal quality

- KCL rubric score
- expert legal score
- issue spotting recall
- rule statement correctness
- application quality
- conclusion correctness

### 8.2 Internal consistency

- argument-conclusion consistency rate
- predicate coverage
- contradiction rate
- unsupported rule rate
- fact hallucination rate
- conclusion flip rate
- paragraph-to-predicate alignment

### 8.3 Procedure-substance consistency

- inadmissible-use rate
- gated fact leakage
- procedure conclusion/substantive conclusion contradiction
- incomplete admissibility review rate

### 8.4 Retrieval and standard quality

- citation correctness
- precedent authority correctness
- supporting/opposing precedent balance
- source quote exactness
- standard assessment accuracy on expert-audit sample
- unknown calibration

### 8.5 Refinement effectiveness

- violations before/after edit
- rubric score before/after edit
- unaffected paragraph preservation
- API token cost per corrected violation
- LLM judge score와 symbolic consistency score의 human correlation

## 9. 잠정 contribution

실험 전에는 아래를 후보 주장으로만 취급한다.

1. 한국 형사법 사례형 long-form generation을 위한 RAG-grounded neuro-symbolic pipeline
2. FactGraph와 판례 기반 standard assessment를 deterministic legal derivation에 연결하는
   interface
3. 실체법과 형사절차를 positive evidence gating으로 연결하는 generation architecture
4. 생성 문서를 derivation으로 back-parse하여 contradiction, omission, unsupported rule,
   inadmissible evidence use를 검출하는 verifier
5. KCL 61개 전 문항에서 legal quality와 internal consistency를 함께 평가하는 실험

실험이 뒷받침하지 않는 항목은 abstract와 contribution list에서 제거한다.

## 10. 논문에서 주장하지 않을 것

- Scallop rule이 자동으로 법적 진실을 보장한다는 주장
- 61개 설문이 한국 형사법 전체를 대표한다는 주장
- Coverage가 없는 특별법·형법총칙 issue를 해결했다는 주장
- LLM standard assessment가 사람의 법률 판단을 대체한다는 주장
- KCL rubric을 rule source로 사용했다는 주장
- DCDE Natural Innocent에서 long-form 또는 절차법 효과를 검증했다는 주장
- 현재 draft fraud rule이 legally verified라는 주장

`logic-verified`는 주어진 rule DB와 derivation에 대한 실행·문서 정합성을 의미한다.
Rule 자체의 법률적 정확성은 판례 원문, commentary, 사람 검수와 golden test에 의존한다.

## 11. 현재 준비된 자산

### 완료 또는 재현 가능

- KCL 형사법 61개 inventory와 사용자 승인 tag
- Commentary target pool 3,108개
- 기존 non-mapped 33개 수동 audit
- 사기죄 API request 13개, NormCard 8개와 RuleIR 1.1 exemplar
- Rulegen input/output JSON contracts
- NormCandidate·NormCard·RuleIR provenance validator와 deterministic compiler
- Procedural positive-gate candidate
- Bootstrap reasoning과 consistency verifier 일부
- 전체 테스트 25개

### 아직 구현·평가 필요

- FactGraph contract와 extractor
- 사용자가 보유한 판례 index adapter
- NormCard와 StandardAssessment contract
- 실제 OpenAI Batch API envelope와 cache runner
- 판례 우선 canonical fraud rule
- KCL 61개 coverage tier 확정
- 실제 `scallopy` runtime integration
- Derivation-to-paragraph planner
- Long-form generator
- Paragraph back-parser
- End-to-end consistency rerank와 targeted edit
- Baseline runner와 main experiment

## 12. 주요 위험

### 12.1 작은 평가셋

평가 단위는 61개다. 과도한 세부 subgroup 분석을 피하고 paired evaluation, bootstrap,
case study와 전 문항 human review 가능성을 장점으로 활용한다.

### 12.2 Rule coverage

165개 unique tag를 제출 전 모두 완전한 rule로 만들기 어렵다. Coverage tier를 명시하고
full 61 result와 covered-tier result를 함께 보고한다. Uncovered issue를 사후 제외해
headline 성능을 높이지 않는다.

### 12.3 형법총칙·특별법 gap

21개 tag는 형법각칙 맥락만 있고 총칙 source가 부족하며, 7개는 현재 corpus 밖
특별법이 필요하다. 해당 source가 수집되기 전에는 `unknown/review_required`로 처리한다.

### 12.4 Standard model 의존

기망, 고의, 중대한 절차 위반 같은 standard는 여전히 neural 오류에 노출된다. 양방향
사실, contrastive precedent RAG, source citation, unknown과 expert audit으로 오류를
드러낸다.

### 12.5 Circularity

KCL rubric을 rulegen, retrieval, prompt construction에 사용하면 평가가 오염된다.
Rubric은 모든 generation 완료 후 scoring에만 사용한다.

### 12.6 Consistency와 correctness의 차이

논리적으로 일관된 답안도 잘못된 rule에 근거할 수 있다. Consistency와 legal quality를
별도 지표로 보고하고 둘 중 하나만으로 우월성을 주장하지 않는다.

## 13. 제출 일정 잠정안

`project_init.md`의 2026-08-11 제출일을 기준으로 한다.

### 7/15-7/19: research and contract freeze

- 이 잠정안 검토
- FactGraph, NormCard, StandardAssessment schema 확정
- 판례 index inventory
- 61개 coverage tier 초안
- 사기죄 E2E generation 1건

### 7/20-7/26: scoped E2E

- 사기죄 3개 설문 full pipeline
- 고빈도 실체법과 절차법 issue 확장
- Scallop runtime과 paragraph planner
- Direct, RAG-only, plan-then-write baseline

### 7/27-8/2: all-61 run

- 61개 전 문항 generation
- IDPR generate와 verify 실행
- Self-Refine, Best-of-N, doctrinal critique baseline
- Core ablation

### 8/3-8/7: analysis

- Rubric 및 consistency scoring
- Coverage-tier 분석
- 절차 gating case study
- Human legal review와 통계 검정

### 8/8-8/11: writing

- Main paper와 appendix
- Claim-evidence audit
- Artifact manifest와 reproducibility commands
- 최종 법률·통계 검수

## 14. 잠정 논문 구성

1. Introduction
   - Long-form legal generation의 argument-conclusion inconsistency
   - DCDE가 보여준 prompt-only structural alignment의 한계
2. Task and Dataset
   - KCL 형사법 61개 설문, inventory와 non-circular evaluation
3. Method
   - FactGraph, RAG standard, Scallop, conditioned generation, verifier
4. Rule and Commentary Construction
   - Metadata pool, RuleIR, legal review protocol
5. Experiments
   - Baselines, ablations, coverage tiers
6. Results
   - Legal quality, consistency, evidence gating
7. Analysis
   - Failure cases, standard errors, procedure-substance interaction
8. Related Work
   - Long-form legal generation, neuro-symbolic reasoning, RAG, DCDE
9. Limitations and Ethics

## 15. 제목 후보

1. **IDPR: Logic-Verified Long-form Generation for Korean Criminal Law**
2. **Binding Legal Arguments to Conclusions: Neuro-Symbolic Long-form Generation for
   Korean Criminal Cases**
3. **In Dubio Pro Reo: Retrieval-Grounded and Symbolically Verified Legal Answer
   Generation**

## 16. 아직 결정할 항목

1. 최종 출력 형식을 엄격한 IRAC으로 고정할지 flexible issue-based answer로 둘지
2. 61개 coverage tier 판정 기준과 Tier C/U 처리
3. 판례 index의 schema, license, source date와 원문 citation 방식
4. FactGraph의 유리·불리 annotation을 모델 출력만 사용할지 일부 human gold를 만들지
5. StandardAssessment expert audit 표본 크기
6. Procedure gating을 main quantitative claim으로 둘 수 있는 문항 수
7. Rerank와 targeted edit 중 어느 것을 primary refinement로 둘지
8. 모델·API budget과 sample 수
9. Workshop page limit에 맞춘 main table 수
10. Natural Innocent와 KCL/rule DB 사이의 죄명 매핑률 및 별도 LJP subset 구성 가능성

## 17. 내부 근거 문서

### IDPR

- `README.md`
- `project_init.md`
- `WORK_REPORT.md`
- `docs/rulegen/scallop_rulegen_strategy.md`
- `data/inventory/kcl_criminal_v1_review.md`
- `data/commentary/kcl_criminal_v1_commentary_pool.json`
- `data/commentary/kcl_criminal_v1_non_mapped_audit.md`
- `data/rulegen/fraud/fraud_rule_ir_exemplar.json`

### DCDE/OBJECTION

- `/home/jaehoonjeong/data/DCDE/desc/DCDE_pipeline.md`
- `/home/jaehoonjeong/data/DCDE/desc/DCDE_progress.md`
- `/home/jaehoonjeong/data/DCDE/desc/DCDE_roadmap.md`
- `/home/jaehoonjeong/data/DCDE/eval/260709_significance/ARR_may_Rebuttal.md`
- `/home/jaehoonjeong/data/DCDE/eval/260709_significance/RESULTS.md`

DCDE 수치는 IDPR의 main result가 아니다. Prompt-only doctrinal alignment가 남긴 failure와
연구 계보를 설명하는 내부 근거로만 사용한다.
