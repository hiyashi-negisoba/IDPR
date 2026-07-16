# IDPR 작업 보고

작성일: 2026-07-14

## 요청

- 프로젝트 초기화
- red-green TDD 전략으로 검증
- 단순 확인 외에는 직접 실행 대신 `sbatch` 사용
- 기존 `.sh` 파일의 SLURM 환경 참고
- 반복 사이에 `project_init.md`를 확인해 종료 조건 판단
- 막히거나 유효 경로가 없으면 수행 내역 보고

## 수행 요약

`IDPR` 프로젝트는 초기 상태에서 `project_init.md`와 `idpr_scaffold.zip`만 있는 상태였다.
아카이브 내용을 확인한 뒤, 실제 파일 기반 scaffold와 최소 동작 모듈을 생성했다.

이번 작업은 `project_init.md`의 W1 전체 Definition of Done 중 다음 초기화 범위에 해당한다.

- 프로젝트 scaffold 생성
- `docs/contracts/` JSON schema 4종 생성
- predicate schema 초안 생성
- fraud 및 evidence gating rule 초안 생성
- rulegen draft writer 생성
- fraud golden case 3종 테스트 생성
- inadmissible_use 검출 테스트 생성
- SLURM 기반 red-green TDD 검증

다음 W1 항목은 완료하지 않았다.

- 쟁점 인벤토리 v1 전체 작성 및 검수
- 사기죄 rule의 법률적 `verified` 승격

사기죄 rule은 법률 검수 전이므로 명시적으로 `draft` 상태로 유지했다.

## Red-Green TDD 기록

### Red

- Job ID: `207646`
- 실행: `sbatch scripts/slurm/run_tests.sh`
- 결과: 실패
- 로그:
  - `logs/idpr_tdd_207646.out`
  - `logs/idpr_tdd_207646.err`
- 실패 내용:
  - scaffold 누락
  - contract schema 누락
  - `idpr` package import 실패
  - reasoning, verification, rulegen 모듈 부재

### Green

- Job ID: `207647`
- 실행: `sbatch scripts/slurm/run_tests.sh`
- 결과: 성공
- 로그:
  - `logs/idpr_tdd_207647.out`
  - `logs/idpr_tdd_207647.err`
- 테스트 결과: `5 passed`

### Final Green

라인 길이 정리 후 최종 상태를 다시 SLURM으로 검증했다.

- Job ID: `207649`
- 실행: `sbatch scripts/slurm/run_tests.sh`
- 결과: 성공
- 로그:
  - `logs/idpr_tdd_207649.out`
  - `logs/idpr_tdd_207649.err`
- 테스트 결과: `5 passed`
- SLURM accounting: `COMPLETED 0:0`

## 주요 생성 파일

- `README.md`
- `PROJECT_INIT.md`
- `pyproject.toml`
- `.env.example`
- `.gitignore`
- `configs/pipeline.yaml`
- `data/README.md`
- `docs/contracts/predicate_instance.schema.json`
- `docs/contracts/derivation.schema.json`
- `docs/contracts/inventory_item.schema.json`
- `docs/contracts/verification_report.schema.json`
- `rules/schema/predicates.yaml`
- `rules/kr/gates.scl`
- `rules/kr/substantive/fraud.scl`
- `rules/kr/procedural/hearsay.scl`
- `scripts/slurm/run_tests.sh`
- `tests/test_project_initialization.py`
- `src/idpr/__init__.py`
- `src/idpr/reasoning/__init__.py`
- `src/idpr/verification/__init__.py`
- `src/idpr/rulegen/__init__.py`
- `src/idpr/extraction/__init__.py`
- `src/idpr/generation/__init__.py`
- `src/idpr/refine/__init__.py`
- `src/idpr/llm/__init__.py`
- `src/idpr/eval/__init__.py`

## 구현 내용

### Contracts

`docs/contracts/` 아래에 stage 간 API 경계가 되는 JSON schema 4종을 추가했다.

- `PredicateInstance`
- `Derivation`
- `InventoryItem`
- `VerificationReport`

### Reasoning

`src/idpr/reasoning/__init__.py`에 bootstrap reasoning 구현을 추가했다.

포함된 타입:

- `Fact`
- `Evidence`
- `StandardJudgment`
- `FraudInputs`
- `Derivation`

포함된 동작:

- 증거능력 gating
- 전문증거 배제
- 위법수집증거 배제
- 사기죄 성립 여부 계산
- `gated_out` 기록
- `standard_flags` 기록

### Verification

`src/idpr/verification/__init__.py`에 claim verifier를 추가했다.

포함된 타입:

- `ParagraphClaim`
- `VerificationReport`

포함된 동작:

- derivation의 `gated_out`과 생성 문단 claim을 비교
- 배제된 증거 사용 시 `inadmissible_use` violation 생성

### Rulegen

`src/idpr/rulegen/__init__.py`에 rule draft writer를 추가했다.

포함된 타입:

- `RuleDraft`

포함된 동작:

- `.scl` draft rule 파일 생성
- `status: draft` 명시
- 법률 검수 완료 또는 `verified` 표현은 쓰지 않음

## 테스트 범위

`tests/test_project_initialization.py`는 다음을 검증한다.

- 프로젝트 scaffold 필수 파일 존재
- contract schema가 load 가능하고 required field를 포함
- 사기죄 golden case
  - 성립
  - intent 누락으로 불성립
  - 전문증거 배제로 gating 불성립
- `inadmissible_use` 검출
- rulegen이 draft rule만 작성하고 legal verification을 주장하지 않음

## 종료 판단

`project_init.md`를 반복 중 재확인했다.

이번 작업은 프로젝트 초기화와 rule 실행 가능성의 bootstrap 검증까지 완료했다.
다만 W1 전체 완료 조건 중 인벤토리 v1 및 법률 검수는 사람 검수와 별도 데이터 작업이 필요하므로 남겨두었다.

## 초기화 당시 남은 작업 (과거 기록)

아래 목록은 프로젝트 초기화 직후의 기록이며, 2026-07-15 최종 갱신 현황으로
대체되었다. 현재 잔여 검토는 문서 하단의 "사용자 검토 잔여분"을 기준으로 한다.

- 변시 사례형 설문 단위 inventory v1 작성
- issue tag 및 `rule|standard` 판정
- 정재훈 검수 반영
- 사기죄 rule 법률 검수 후 `verified` 승격
- 실제 Scallop 연동
- S1 extraction 구현
- S3 generation 구현
- S4 back-parse 기반 verification 확장

---

## 추가 작업: KCL 형사법 설문 inventory 초안

작성일: 2026-07-14

### 요청

- KCL essay 데이터셋에서 형사법만 사용
- 전 문항을 설문 단위로 분해
- 각 설문에 issue tag 부여
- 문제 수가 적으므로 전체를 육안 확인
- 분리 결과를 정재훈 검수 대상으로 전달

### 입력 데이터

- Source: `/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet`
- 전체 행 수: 169
- 형사법 행 수: 61
- 회차별 형사법 행 수:
  - 10회: 13
  - 11회: 11
  - 12회: 13
  - 13회: 10
  - 14회: 14

### 산출물

- `data/inventory/kcl_criminal_v1_draft.jsonl`
- `data/inventory/kcl_criminal_v1_review.md`
- `scripts/build_kcl_criminal_inventory.py`
- `scripts/slurm/build_inventory.sh`
- `tests/test_kcl_criminal_inventory.py`

### 분해 기준

KCL essay parquet의 각 형사법 row가 이미 변호사시험 설문 단위로 분리되어 있어,
이번 초안에서는 row 1개를 sub-question 1개로 정규화했다.

각 item에는 다음 정보를 포함했다.

- `sub_question_id`
- `source`
- `exam_round`
- `paper`
- `question_number`
- `subpart`
- `question_text`
- `question_prompt`
- `legal_area`
- `issue_tags`
- `norm_types`
- `covered`
- `coverage_candidate`
- `review_status`
- `rubric_summary`

### 태깅 상태 (초안 생성 당시)

- 초안 생성 당시 전체 61개 item은 `review_status=needs_review`였음
- 전체 61개 item 모두 `covered=false`
- 이유: 현재 rule DB는 bootstrap draft 수준이므로, 법률 검수 및 rule 구현 전에는 coverage를 주장하지 않음

분포:

- `procedure`: 33
- `substantive`: 26
- `mixed`: 2

Coverage candidate:

- `procedure_gating_candidate`: 17
- `property_crime_candidate`: 11
- `out_of_current_rule_scope`: 33

### SLURM 실행 기록

Inventory 생성:

- Job ID: `207668`
- 결과: `COMPLETED 0:0`
- 산출: 61 items

Prompt 추출 보정 후 재생성:

- Job ID: `207669`
- 결과: `COMPLETED 0:0`
- 산출: 61 items

검증:

- Job ID: `207670`
- 실행: `sbatch scripts/slurm/run_tests.sh`
- 결과: `8 passed`
- SLURM accounting: `COMPLETED 0:0`

### 검수 요청

검수 대상 파일은 `data/inventory/kcl_criminal_v1_review.md`이다.

검수 시 확인할 항목:

1. 설문 단위가 맞는지
2. `issue_tags`가 과소/과대 태깅되지 않았는지
3. `legal_area`가 실체법/절차법/혼합 중 맞는지
4. 1차 구현 scope로 `covered`를 올릴 항목이 있는지

### 검수본 coverage 표시 및 태그 빈도 보완

- 검수 표에 `covered` 열을 추가해 61개 항목의 `false` 값을 명시
- `data/inventory/kcl_criminal_v1_tag_counts.md` 추가
- 고유 태그: 165개
- 전체 태그 할당: 207회
- 2회 이상 출현 태그: 30개
- 1회 출현 태그: 135개

SLURM red/green 기록:

- Job `207681`: coverage 표시 테스트 red (`1 failed, 8 passed`)
- Job `207682`: coverage 열 반영 후 inventory 재생성 (`COMPLETED 0:0`)
- Job `207683`: coverage 표시 green (`9 passed`)
- Job `207684`: 태그 빈도 보고서 테스트 red (`1 failed, 9 passed`)
- Job `207685`: 태그 빈도 보고서 생성 (`COMPLETED 0:0`)
- Job `207686`: 최종 green (`10 passed`)

---

## 추가 작업: KCL 형사법 commentary metadata bundle

작성일: 2026-07-15

### 요청

- 이전 의미검색/embedding/reranker 방식은 폐기
- `rubric_summary`가 아니라 165개 `issue_tags`를 기준으로 commentary를 연결
- commentary metadata의 `law_id`, `article_no`, `section_path`, `comment_id`만 사용
- 대상 조문 chunk를 전량 수집하고 전역 중복 제거
- 현재 corpus에 없는 형법총칙·특별법 쟁점은 누락시키지 말고 unavailable로 명시

### 산출물

- `scripts/build_kcl_criminal_commentary_bundle.py`
- `tests/test_kcl_criminal_commentary_bundle.py`
- `data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl`
- `data/commentary/kcl_criminal_v1_commentary_chunks.jsonl`
- `data/commentary/kcl_criminal_v1_commentary_review.md`
- `AGENT_MISTAKES_REFLECTION.md`

### 결과 (초기 bundle 스냅샷)

아래 수치는 33개 non-mapped tag 수동 검토 및 raw PDF fallback 반영 전 기록이다.
현재 수치는 문서 하단의 최종 갱신 현황을 기준으로 한다.

- 기준 tag: 165개
- unique commentary chunks: 3,085개
- `mapped`: 132개
- `mapped_with_corpus_gap`: 12개
- `unavailable_in_current_commentary`: 21개
- `target_missing_in_docs`: 0개

이번 bundle은 의미검색 점수나 top-k 후보를 쓰지 않는다. 각 tag를 사람이 검수 가능한
조문 metadata target에 연결하고, 해당 `(law_id, article_no)`에 속한 chunk를 전부 복사한다.

현재 commentary corpus는 `형법각칙`과 `형사소송법`뿐이다. 따라서 `joint_principal`,
`voluntary_abandonment`, `mistake_of_object` 같은 형법총칙 쟁점과
정보통신망법·아청법·경찰관직무집행법 쟁점은 `unavailable_in_current_commentary`로 남겼다.

### 직접 검증

- 실행: `/data5/jaehoonjeong/miniconda3/bin/python scripts/build_kcl_criminal_commentary_bundle.py`
- 테스트:
  `/data5/jaehoonjeong/miniconda3/bin/python -m pytest tests/test_kcl_criminal_commentary_bundle.py`
- 결과: `4 passed`

이 단계에서는 사용자의 정정에 맞춰 SLURM job을 제출하지 않았다. metadata 기반 파일 생성과 구조 검증만 직접 수행했다.

---

## 최종 갱신: commentary pool 및 Scallop rulegen 준비

작성일: 2026-07-15

이 절은 위의 inventory 초안 및 commentary 초기 bundle 스냅샷을 대체한다.

### Inventory 승인 상태

- 전체 61개 item의 설문 분리, `issue_tags`, `legal_area`는 사용자 승인 반영
- 전체 61개 item: `review_status=reviewed`
- 전체 61개 item: `covered=false`
- 전체 61개 item: `coverage_review_status=needs_review`
- 따라서 사용자가 아직 확인하지 않은 값은 rule coverage 판정뿐이며, 다른 승인 상태와 분리해 표시됨

### 확정 commentary pool

Primary source `docs.parquet`의 전체 9,384개 row는 형법각칙 4,011개와
형사소송법 5,373개로 구성된다. Issue tag에 명시적으로 연결한 102개
`(law_id, article_no)` target만 포함하고, `comment_id` 기준으로 전역 중복을 제거했다.

- parquet commentary chunk: 3,103개
- raw PDF fallback chunk: 5개
- 최종 unique commentary chunk: 3,108개
- 제외된 primary source row: 6,281개
- fallback 대상: 형법 제254조 1쪽, 제300조 2쪽, 제342조 1쪽, 제344조 1쪽
- 각 chunk는 `comment_id`, `law_id`, `article_no`, `section_path`, `source_kind`, `source_path`를 보존

최종 165개 issue tag 상태:

- `mapped`: 137개
- `mapped_with_corpus_gap`: 21개
- `unavailable_in_current_commentary`: 7개
- `target_missing_in_docs`: 0개

기존 non-mapped 33개를 전부 수동 검토한 결과는 다음과 같다.

- 현재 corpus에서 완전 해결: 5개
- 관련 범죄 맥락은 연결했으나 형법총칙 등 직접 근거가 부족: 21개
- 현재 corpus에 필요한 법령이 없어 unavailable 유지: 7개

재현 및 검토 기준 파일:

- `data/commentary/kcl_criminal_v1_commentary_pool.json`
- `data/commentary/kcl_criminal_v1_non_mapped_audit.md`
- `data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl`
- `data/commentary/kcl_criminal_v1_commentary_chunks.jsonl`
- `data/commentary/kcl_criminal_v1_commentary_review.md`

이 과정에는 embedding, reranker, 의미검색, GPU 또는 SLURM을 사용하지 않았다.

### 사기죄 API rulegen 모범답안

형법 제347조 commentary 127개를 순서와 section 경계를 보존한 13개 API batch로
분할했다. 각 batch의 commentary 본문은 최대 12,000자이며, 합집합은 원본 127개와
정확히 일치한다.

- 입력 계약: `docs/contracts/rulegen_request.schema.json`
- 1차 출력 계약: `docs/contracts/norm_candidate_batch.schema.json`
- 병합 RuleIR 계약: `docs/contracts/rule_ir.schema.json`
- 추출 prompt: `prompts/rulegen_extract_norm_candidates.md`
- 병합 prompt: `prompts/rulegen_merge_rule_ir.md`
- API 요청: `data/rulegen/fraud/fraud_rulegen_requests.jsonl`
- provenance index: `data/rulegen/fraud/fraud_commentary_index.json`
- 모범 RuleIR: `data/rulegen/fraud/fraud_rule_ir_exemplar.json`
- 사기죄 후보 규칙: `rules/exemplars/fraud_v1_candidate.scl`
- 절차법 positive gate 후보: `rules/exemplars/procedural_gate_v1_candidate.scl`
- 전체 전략: `docs/rulegen/scallop_rulegen_strategy.md`

모델은 commentary에서 근거 후보를 추출하고 RuleIR만 반환한다. 로컬 validator가
인용문 일치, source scope, predicate 선언/arity/type, head 및 negation 변수 안전성,
`rule`과 `standard` 분리를 검사한 뒤 deterministic compiler가 `.scl`을 생성한다.
모델이 반환한 임의 Scallop 코드를 직접 실행하지 않는다.

사기죄 후보는 기망, 착오, 처분행위, 재산 취득의 연결과 각 인과관계를 분리하고,
사실은 `fact_id`와 `provable(f)`를 통해서만 구성요건에 투입한다. 재산상 손해 및
불법영득의사는 법률 견해 대립을 숨기지 않고 명시적 policy를 요구하는 strict
variant로 분리했다. 절차법 후보는 `not excluded`를 적법성으로 간주하지 않고,
적법성 검토 완료와 각 positive gate 충족을 요구한다.

### 검증 결과

- 전체 테스트: `22 passed`
- 변경 Python 파일 `py_compile`: 통과
- JSON 산출물 load 및 schema/provenance 정합성: 통과
- line length 검사: 통과
- 로컬 환경에 `ruff`가 없어 lint 실행은 생략
- 로컬 환경에 `scallopy`/`scli`가 없어 실제 Scallop runtime 실행은 하지 못했으며,
  schema, validator, deterministic compiler 및 정적 규칙 검증으로 확인

### 사용자 검토 잔여분

에이전트가 로컬에서 수행할 수 있는 생성, 매핑 감사, 계약 작성, 정적 검증 및
테스트는 완료했다. 남은 항목은 법률적·내용적 승인 두 종류다.

1. Inventory 61개 각각의 `covered=false`를 유지할지, 구현 범위에 따라 `true`로 올릴지 결정
2. 사기죄 RuleIR의 4개 legal review question, strict variant 정책 및
   `rule|standard` 판정을 검토한 뒤 `draft/pending`을 승격할지 결정

---

## NormCard와 RuleIR 1.1 준비물

작성일: 2026-07-15

### Git 기준선

- `IDPR`을 독립 Git 저장소로 초기화하고 기본 브랜치를 `main`으로 설정
- 기존 연구 자산 65개 파일을 baseline commit `d70a8be`로 기록
- 실제 `.env`, cache, 실행 log는 `.gitignore`로 제외

### 새 rulegen 경계

기존 `NormCandidateBatch -> RuleIR` 직접 병합 사이에 `NormCardSet`을 추가했다.

```text
NormCandidateBatch[]
  -> candidate provenance validation
  -> NormCardSet merge and validation
  -> RuleIR 1.1 with norm_card_ids
  -> deterministic Scallop compilation
```

NormCard는 하나의 독립 proposition, exact commentary quote, 해당 quote를 공급한 API
request, 형식화 방식, 권위 성격, 학설 대립과 검수 상태를 함께 보존한다. RuleIR 1.1의
모든 commentary-origin predicate와 rule은 `norm_card_ids`를 가져야 하며, RuleIR 인용은
연결된 NormCard의 source 범위를 벗어날 수 없다.

추가·변경된 핵심 파일:

- `docs/contracts/norm_card_set.schema.json`
- `docs/contracts/rule_ir.schema.json` (`version=1.1.0`)
- `prompts/rulegen_merge_norm_cards.md`
- `prompts/rulegen_merge_rule_ir.md`
- `src/idpr/rulegen/__init__.py`
- `data/rulegen/fraud/fraud_norm_card_set_exemplar.json`
- `data/rulegen/fraud/fraud_rule_ir_exemplar.json`

### 사기죄 exemplar

- 형법 제347조 핵심 근거를 8개 `human_exemplar` NormCard로 구성
- 각 카드의 source가 13개 extraction request 중 어디에서 왔는지 역추적 가능
- `deterministic_rule`, `standard_input`, `policy_variant`를 분리
- 재산상 손해와 불법영득·이득의사 대립은 `policy_variant`와 `review_required=true` 유지
- 판례 관련 카드는 `commentary_reported_precedent`로 표시하여 판례 원문 검증 전
  primary authority처럼 취급하지 않음
- 모든 RuleIR predicate와 rule에 카드 링크를 부여하고 Scallop 주석에도 카드 ID 보존

### 검증 결과

- 전체 테스트: `25 passed`
- Python `py_compile`: 통과
- JSON 파일 구문 검사: 통과
- `git diff --check`: 통과
- 로컬에 `jsonschema`, `ruff`, `scallopy`/`scli`가 없어 각각 일반 JSON Schema runtime
  검증, lint, Scallop runtime 실행은 아직 수행하지 않음

### 법률 검수 잔여분

1. 재산상 손해 독립요건에 관한 판례 기준 확인
2. 불법영득·이득의사를 요구하는 사기 유형의 판례 기준 분류
3. 삼각사기의 처분권한·재산상 근접성 predicate 확정
4. 주석서가 보고한 판례 법리를 사용자 판례 index 원문과 대조

---

## SKI-ML fraud rulegen pilot 및 correction exemplar

작성일: 2026-07-16

### Gateway와 계약

- LiteLLM 기반 SKI-ML Gateway client, deterministic cache, usage manifest 구현
- Terra extraction/revision과 Sol advisory critic 역할 분리
- `max_completion_tokens`와 reasoning token 기록, API key 및 hidden reasoning 비저장
- NormCandidate/NormCard/Critique/RuleIR에 JSON Schema runtime 검증 적용
- critic locator는 `comment_id + section_path`, 후보 provenance는 exact quote 유지
- 4xx 반복 방지를 위해 기본 retry를 0으로 설정

### 품질 교정 결과

첫 Terra 출력은 21개 후보였고 exact quote 검증은 통과했지만 핵심 규범 누락이 있었다.
Sol critic의 quote 금지 지시가 검토 대상 quote까지 금지하는 것으로 오해된 문제를
수정한 뒤 오탐이 제거되었다. 두 Sol 실행과 수동 source 대조의 유효 finding을
`fraud_pass1_001_review_addendum.json`으로 고정했다.

전체 batch 재생성 correction은 누락을 보완하는 동시에 새 사례 누락을 계속 만들었다.
이에 따라 다음 경계를 확정했다.

1. `norm_kind`와 `polarity`를 분리해 positive, negative, exception을 명시
2. OCR이 문장 중간을 끊은 경우 높은 일치율의 exact fragment로만 provenance 보정
3. critic finding은 원문 대조 후 수용·기각·RAG context 유보
4. 수용 finding은 전체 재생성 대신 검증된 `NormCandidatePatch`로 최소 적용
5. 구체 내용 없는 반대설은 발명하지 않고 unresolved question으로 유지
6. 열거된 사례는 독립 규범이 없으면 후보가 아니라 후속 RAG context로 유지

최종 tracked exemplar:

- `data/rulegen/fraud/fraud_norm_candidate_batch_pass1_001_exemplar.json`
- 후보 62개
- unresolved question 8개
- polarity 분포: positive 36개, negative 24개, exception 2개
- exact source/provenance 및 스키마 검증 통과
- extraction-stage final adjudication은 pass이지만 법률검토 완료를 의미하지 않음

### API 사용량

2026-07-16 현재 cache와 failure metadata의 response ID를 중복 제거하면 Terra 7회,
Sol 10회 응답이 기록되어 있다. 합계는 Terra 172,469 tokens, Sol 180,378 tokens이며,
공식 standard list rate 단순 환산은 약 $2.51이다. 실제 차감액은 연구실 Gateway
dashboard를 기준으로 확인해야 한다.

### 검증

- 전체 테스트: `38 passed`
- Python `py_compile`: 통과
- `git diff --check`: 통과
- 현재 Python 환경에 `ruff`가 설치되어 있지 않아 lint는 실행하지 못함
- 실제 Scallop runtime 검증과 판례 원문 대조는 아직 수행하지 않음

---

## Compact gold few-shot과 전체 풀 예산 계획

작성일: 2026-07-16

62개 후보 전체를 매 요청에 첨부하지 않고, 학설 대립과 판례의 좁은 적용범위를 함께
보존하는 3개 후보를 `fraud_norm_candidate_fewshot_gold.json`으로 선별했다. 이 예시는
성매매 관련 긍정설·부정설을 별도 variant로 유지하면서 지급면탈형 판례 입장을 별도
standard로 표현한다. Terra는 이 source-to-structure 변환만 학습하며 사기죄 법리,
식별자, 후보 수 또는 결론을 다른 요청에 복사해서는 안 된다.

- 기본 extraction: compact few-shot 사용
- 논문 ablation: `--no-fewshot`
- exemplar 크기: 4,467 characters
- 테스트: `39 passed`

현재 commentary pool은 3,108 chunks, 2,654,246 characters, 102 article targets이다.
12,000 characters 단순 packing의 이론적 최소치는 222 requests이고, 조문·절 경계를
보존하면 더 늘어난다. Terra와 Sol을 모든 batch에서 반복하는 방식은 예산에 맞지 않는다.
Terra는 전수 실행하되 Sol은 층화표본, high-risk batch, 검증 실패 batch에 집중한다.
NormCard merge, RuleIR 생성과 여유분을 포함한 실무 예산은 약 $60-$80으로 잡는다.
따라서 잔액이 $97.5라면 전체 범위를 진행할 수 있지만, 문자 그대로 $7.5라면 불가능하다.
