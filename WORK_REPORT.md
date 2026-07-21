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

---

## 사기죄 제347조 전체 NormCandidate/NormCard 준비 실행

작성일: 2026-07-16

### 범위와 결과

이번 API 실행 범위는 형법 제347조 사기죄 주석서 13개 배치로 한정했다. 다른 죄명,
형법총칙, 특별법, 형사소송법에는 API 호출을 확장하지 않았다.

- 최종 NormCandidate: 661개, unresolved question 37개
- 최종 NormCard: 636개
- 후보 계보: 661개가 카드에 연결
- 형식화: standard_input 334, context_only 179, policy_variant 67,
  deterministic_rule 56
- 법률검토 필요: 551개
- Sol 최종 비평: 17개 보고서 모두 계약 검증 통과
- 최종 지적: 67개, pass 2개 묶음, revise 15개 묶음

NormCardSet 계약을 1.1로 올려 모든 카드가 `candidate_refs`를 갖게 했다. 카드가 후보를
누락하거나 알 수 없는 후보·출처를 참조하면 실패한다. 서로 다른 `norm_kind` 또는
`polarity`를 한 카드에 병합하는 것도 실패하도록 validator를 강화했다.

Terra merge가 기망 후보 211개 중 181개를 누락하고 특수유형 101개를 4개 카드로
과도 병합한 실행을 확인했다. 이 두 모듈은 API 병합 결과를 폐기하고 후보별 카드로
복원했다. 다른 모듈도 반대 polarity나 다른 authority class를 섞은 병합은 자동
분리했다. 주석서가 보고한 판례로 추정되는 카드 179개는 원판례 확인 전
`context_only`로 제한했다.

### RuleIR 게이트

형식상 55개 카드는 잠정 RuleIR 진입 가능하지만, 사기죄 전체 결론을 구성할 핵심
법리의 출처·권위·학설 선택이 승인되지 않았다. 따라서 636개 전체 RuleIR 생성은
의도적으로 차단했다. 기존 8장짜리 NormCard/RuleIR/Scallop은 API에 제공할 구조적
모범답안이며 전체 사기죄 법리 승인본이 아니다.

사용자 검수 시작점:

- `data/rulegen/fraud/fraud_legal_review_guide.md`
- `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- `data/rulegen/fraud/fraud_human_review_decisions.jsonl`
- `data/rulegen/fraud/fraud_rule_ir_readiness.json`

### API 사용량

사기죄 전체 준비 실행의 기록된 누적 사용량은 약 2,885,006 tokens, 122 API calls다.
여기에는 extraction calibration, 후보 교정, NormCard merge v1/v2, 중간 및 최종 Sol
감사가 포함된다. Gateway가 모델별 실제 청구액을 응답하지 않으므로 USD 비용은
dashboard를 기준으로 확인해야 한다.

직접적인 실행기 실수로 낭비된 사용량은 최소 428,553 tokens다.

- partial critic target에 모듈 전체 source scope를 넣은 v1: 399,052 tokens
- 허용 타입이 없던 `missing_variant` 응답을 같은 run ID로 재호출: 29,501 tokens

두 문제의 원인과 재발 방지는
`docs/research/agent_mistakes_postmortem.md`에 기록했다.

### 검증

- 전체 테스트: `49 passed`
- Python `py_compile`: 통과
- 후보 661개 및 카드 636개 lineage/provenance 검증: 통과
- 최종 Sol 비평 17개 JSON contract 검증: 통과
- `ruff`: 현재 환경에 설치되어 있지 않아 실행하지 못함
- Scallop runtime: 현재 환경에 `scallopy`/`scli`가 없어 실행하지 못함

---

## 사기죄 검수 큐 카드 매핑 정정

작성일: 2026-07-17

Sol 비평의 `target_path` 숫자 인덱스가 제출 카드 배열과 일관되게 대응하지 않는 것을
확인했다. 기존 큐 생성기는 이 숫자를 그대로 사용해 일부 지적을 무관한 카드에
연결했고, 그 결과 검수 큐의 proposition이 이미 지적을 반영한 것처럼 보였다.

이번 정정은 NormCard proposition을 수정한 것이 아니라 지적과 검수 대상 카드의
연결만 바로잡은 것이다. 숫자 경로가 있던 40개 지적은 지적 문구, source_refs,
카드 proposition을 전수 대조하여 명시적 카드 ID로 고정했다. 나머지는 명시 카드 ID
20개, 카드셋 메타데이터 5개, 명시적 전체 파트 2개다. 미등록 숫자 경로는 더 이상
추측하지 않고 큐 생성 단계에서 실패한다.

- 검수 지적: 67개
- 지적 영향 카드: 184개
- 잠정 RuleIR 진입 가능: 55개
- 전체 테스트: `49 passed`
- `git diff --check`: 통과

---

## 사기죄 1차 사용자 검수 반영

작성일: 2026-07-17

빈 `impacted_cards` 5건은 개별 카드가 아니라 critic 실행기가 자동 생성한
`legal_review_questions`에 대한 지적이었다. 질문 인덱스를 재구성하여 질문을 생성한
실제 카드와 원 질문 문구를 큐에 표시했고, 현재 빈 대상 항목은 없다.

`source_entailment` 8건을 source quote가 아니라 같은 comment_id의 전체 commentary
chunk와 대조했다. 7건은 전체 chunk에 문제 삼은 내용이 명시되어 있어 오탐으로
기각했다. critic 입력에 full chunk가 없었던 것이 원인이므로 미래 실행은 참조 chunk의
`document_text`를 함께 전달한다. 제3자 취득형에서 의사의 객체를 제3자로 잘못 옮긴
1건만 유효하여 NormCard 번역을 수정했다.

사용자 지시에 따라 허위기재 여권 후보와 인용을 제거하고, 일반화되어 있던 삼각사기
카드는 법원을 피기망자로 한 구체적 소송사기 판례의 피해자 판단으로 한정했다. 별도
모듈의 삼각사기 일반 정의·처분권한 학설 및 소송사기 정의와 역할을 분리했다.

- 최종 NormCandidate: 661개
- 최종 NormCard: 636개
- 사용자 판정 완료: 10건
- 타당성 수용 후 remediation 대기: 57건
- 잠정 Scallop core 후보: deterministic_rule 28개
- neural grounding specification 준비: standard_input 25개

구체 판례 적용례는 Scallop 규칙으로 전부 컴파일하지 않는다. 판례 index에서 검색한
사례는 grounding 모델의 요건 판단과 근거 인용에 사용하고, Scallop은 구조화된
positive·negative·unknown 판단 및 소수의 검증된 core rule만 소비한다.

### 검증

- candidate/card/review queue 전체 재생성: 통과
- 전체 테스트: `50 passed`

---

## 사기죄 검수 상태 전면 정정 및 remediation

작성일: 2026-07-18

기존 67개 검수 큐는 카드 검수표가 아니라 critic finding 목록인데 이를 전체 검수처럼
설명했고, 사용자가 타당성을 승인한 57개 finding을 카드에 반영하지 않은 채 53개 ready
subset으로 RuleIR 생성을 진행하려 했다. 또한 `critic_pending`을 critic 미완료로 잘못
설명하고 standard input의 neural judgment 필요성을 사람의 법률검토 필요성과 혼동했다.

이번 정정에서는 API를 전혀 사용하지 않았다.

- accepted finding 57개를 source chunk와 직접 대조하여 전부 수동 반영
- 변경 카드 196개, provenance·candidate link·norm kind·polarity 불변
- critic finding 67개 전부 resolved, remediation 57개 applied
- 합쳐진 경쟁 견해 4개 쟁점에서 독립 policy card 10개 추가
- 최종 NormCard 646개 전수 감사
- deterministic rule ready 51개
- standard input ready 285개
- RAG context only 274개
- policy choice pending 36개, 12개 그룹

corpus에서 판례 방향이 드러난 보호법익, 일부 경합, 불법원인급여, 권리행사 쟁점은
판례 우선 원칙으로 직접 실무 규칙화했다. 무전취식의 묵시적 기망/부작위 분류처럼 결론을
바꾸지 않는 차이와 처분 자의성처럼 사실조건이 다른 규칙은 policy 선택에서 제거했다.
현재 남은 12개 그룹은 corpus에 직접적인 판례 선택 근거가 없어 사용자의 판례 인덱스
확인이 필요한 항목만 포함한다.

주요 산출물:

- `data/rulegen/fraud/fraud_norm_card_remediation_ledger.json`
- `data/rulegen/fraud/fraud_norm_card_audit.json`
- `data/rulegen/fraud/fraud_policy_review_queue.json`
- `data/rulegen/fraud/fraud_policy_review_guide.md`
- `data/rulegen/fraud/fraud_policy_review_decisions.jsonl`

검증:

- remediation/audit/policy artifact의 `api_calls`: 모두 0
- NormCardSet 8개 source·request·schema 검증: 통과
- 646개 카드가 네 상태 bucket에 중복·누락 없이 포함
- 전체 테스트: `50 passed`

---

## 사기죄 core 범위·판례 정책 2차 전면 정정

작성일: 2026-07-18

직전 보고의 “deterministic ready 51, standard input ready 285, policy 12개”는 당시 최종
상태가 아니었으며 이 절의 수치로 대체했다. 주석서와 로컬 대법원 판례 DB를 다시 대조한
결과, 직접 판례가 없다고 표시했던 12개 정책 그룹 모두를 판례 우선 실무 규칙 또는
RAG 문맥으로 정리할 수 있었다. 외부 API는 사용하지 않았다.

- NormCard: 646개
- deterministic rule 검수 후보: 29개
- standard input 검수 후보: 89개
- RAG/future-work context: 528개
- 남은 policy choice: 0개
- 로컬 원판례 확인: 15건
- core 사용자 검수: 118개 전부 pending
- 전체 RuleIR 생성: core 검수 완료 전 차단

핵심 수정에는 현실적 재산상 손해를 별도 요건으로 보지 않는 판례 기준, 부작위 기망의
고지의무 기준, 불법영득·편취 범의, 처분의사, 삼각사기의 처분 권능 또는 지위, 기수시기
기준이 포함된다. 구체 판례 결과, 학설 소개, 희귀 적용례, 이득액 계산과 다른 죄명 문맥은
Scallop core에서 제외하고 RAG로 보존했다. 죄수와 미필적 고의·공범 이탈은 형법총칙
corpus가 필요한 future work로 분리했다. “기망자와 처분행위자 동일”이라는 번역 오류는
“피기망자와 처분행위자 동일”로 고쳤다. 손해를 열거한 서론 요약 카드는 출처대로 복원해
RAG로 내리고, 손해 불요는 2003도4914·2017도21196 출처가 연결된 카드만 core 후보로
남겼다.

사용자 검수 파일:

- `data/rulegen/fraud/fraud_core_rule_review_guide.md`
- `data/rulegen/fraud/fraud_core_rule_review_queue.json`
- `data/rulegen/fraud/fraud_core_rule_review_decisions.jsonl`

검증:

- 신규 정정 산출물의 `api_calls`: 0
- policy resolution: 12개 완료, 잔여 0개
- 로컬 parquet의 사건번호·레코드 ID·선고일·법원 15건 자동 대조: 통과
- core 큐/결정 파일: 118개 ID 완전 일치
- readiness: core 미승인 118개로 전체 RuleIR 차단
- 전체 테스트: `50 passed`
- Python `py_compile`: 통과
- `git diff --check`: 통과

---

## 사기죄 core 사용자 검수 반영

작성일: 2026-07-18

사용자가 원래 core 후보 118개를 검토하여 `rag` 24개, `narrow` 10개, `reject` 3개,
`duplicated` 1개로 표시했다. 표시가 없는 80개와 전체 출처를 다시 대조했고, 외부 API는
사용하지 않았다.

- 사용자 분류 직접 반영: RAG 24개, reject 3개, duplicate 1개
- 추가 RAG: 지급명령 신청 및 소장 송달 시점 2개(소송사기 전용)
- 사용자 narrow 직접 수정: 9개
- 추가 문구 축소: 기존 착오 이용, 기망 상대방의 능력, 착오 인식 3개
- 차용금 편취 범의 판단 규칙: core 유지
- 중복된 일반 편취 범의 객관적 사정 카드: RAG 보존
- 최종 실행 core: deterministic rule 28개, standard input 60개
- 최종 RAG/future-work context: 558개
- core 승인: 88/88, unresolved 0
- 전체 RuleIR 생성 게이트: 해제(전수 RuleIR 생성은 아직 미실행)

원래 118개 라벨, 원문과 수정문, 최종 역할 및 변경 사유는
`data/rulegen/fraud/fraud_core_rule_human_review_audit.json`에 보존했다.

---

## 사기죄 전체 RuleIR 생성 사전 준비

작성일: 2026-07-18

사용자 검수를 마친 core 88장을 API 없이 하나의 reviewed aggregate NormCardSet으로
구성했다. Terra 생성 전에 해소해야 할 구조·비용 선택을 10개 항목으로 명시했고, 전부
승인되기 전에는 `--execute`도 Gateway 호출 전에 실패하도록 runner를 차단했다.

- aggregate core: deterministic rule 28개, standard input 60개
- source scope: 제347조 commentary chunk 40개
- 제외 context: RAG/future work 558개
- 생성 단위: Terra 단일 호출 1회
- 실행 ceiling: 동시성 1, retry 0, max completion 64,000 tokens
- 준비 단계 API 호출: 0회
- 사용자 사전 검수: 10/10 승인

현재 계약은 모든 commentary input에
`(case_id, assessment_id, ..., status)`와 같은 평가 ID의
`provable(case_id, assessment_id)`를 요구한다. status는 `satisfied`,
`not_satisfied`, `unknown`의 명시적 값만 허용한다. rule 안의 모든 atom은 head와 같은
case 변수를 사용해야 하며, 선언한 입력은 실제 rule에서 소비되고 성립·불성립·미확인·
충돌 output도 실제 head rule로 구현되어야 한다. negation과 `active_policy`는 금지했다.

생성 후 순서도 강제했다. Terra 응답이 로컬 schema·provenance·88장 coverage 계약을
통과하더라도 바로 Sol이나 Scallop으로 보내지 않는다. 에이전트가 규칙별 검토와 장문
자연어 해설을 먼저 작성하고, 사용자가 원본 RuleIR과 해설을 검수한 뒤에만 Sol critic을
실행한다. Sol finding을 사용자가 다시 검수한 다음에만 deterministic compiler와 Scallop
runtime/golden test를 실행한다.

주요 파일:

- `data/rulegen/fraud/fraud_core_norm_card_set.json`
- `data/rulegen/fraud/fraud_full_rule_ir_generation_request.json`
- `data/rulegen/fraud/fraud_rule_ir_generation_fewshot.json`
- `data/rulegen/fraud/fraud_rule_ir_generation_prep_review_guide.md`
- `data/rulegen/fraud/fraud_rule_ir_generation_prep_review_decisions.jsonl`
- `scripts/prepare_fraud_full_rule_ir_generation.py`
- `scripts/run_fraud_full_rule_ir_generation.py`

검증:

- 준비 스크립트: 88장/40 source/10 review item 재현
- dry-run: API 0회, planned Terra 1회, artifact hash 통과
- `--execute` 차단 시험: pending 10개에서 네트워크 요청 전 종료
- RuleIR 구조·full-generation contract 테스트: 통과
- `tests/test_rulegen_exemplar.py`: `28 passed`
- 전체 테스트: `55 passed`

사용자 승인 시 역할 인자의 의미를 추가로 명확히 했다. 역할 슬롯을 분리하는 것은 각
역할이 별개의 사람이라는 뜻이 아니며 동일인이 여러 역할을 맡으면 같은 entity ID를
사용한다. 사기 성립 rule에서는 피기망자와 처분행위자에 반드시 같은 변수를 사용하고,
그 사람과 재산소유자가 다른 경우 삼각사기의 처분 권능 또는 지위를 별도로 심사한다.
해당 조건은 prompt, generation request, full-generation validator와 부정 테스트에 모두
반영했다. 승인 반영 뒤 dry-run은 `execution_allowed=true`이나 Terra는 아직 호출하지
않았다.

---

## 사기죄 full RuleIR Terra 실행 및 수동 재구성

작성일: 2026-07-18

사용자의 명시적 승인으로 Terra를 정확히 1회 호출했다. 동시성 1, retry 0이었고 Sol은
호출하지 않았다.

- model: `openai/gpt-5.6-terra`
- prompt tokens: 40,366
- completion tokens: 4,606
- reasoning tokens: 1,537
- total tokens: 44,972
- API calls: Terra 1, Sol 0

Terra는 승인된 88장 중 8장만 `fraud_core_assessment` 하나로 합치고 predicate 6개,
rule 4개를 반환했다. 스스로 나머지 카드는 별도 번역이 필요하다고 밝혔으며 source scope도
40개 중 1개만 선언했다. 원본은
`data/rulegen/fraud/fraud_full_rule_ir_terra_partial_output.json`에 보존했고
`fraud_full_rule_ir_terra_failure_audit.json`에 사용량과 실패를 기록했다. 이 응답은
candidate로 승격하지 않았고 추가 API 호출도 하지 않았다.

승인된 88장을 에이전트가 직접 재매핑하는 결정적 builder를 작성했다. 카드별로
3상태 assessment와 `provable` gate를 두고, 객체·기망·착오·처분·취득·인과·고의·기수
component를 결합했다. 일반형/삼각사기와 본인/제3자 취득을 네 branch로 분리했고,
피기망자와 처분자는 모든 성립 head에서 같은 변수다. 현실적 재산상 손해는 별도 사실
gate로 요구하지 않으며 불법영득의사는 모든 유형의 공통 gate로 강제하지 않았다.

- NormCard coverage: 88/88
- commentary input: 88개(standard 60, rule fact 28)
- predicate: 194개
- rule: 337개
- natural-language rule explanation: 337/337
- negation / active_policy: 0 / 0
- full-generation validator: 통과
- 전체 테스트: `59 passed`

현재 `fraud_full_rule_ir_natural_language_explanation.md`와
`fraud_full_rule_ir_agent_review.md`까지 작성했고 사용자 법률 검수 대기 상태다. 사용자
검수 전에는 Sol, 사용자 재검수 전에는 Scallop compile/runtime을 계속 차단한다.

---

## 사기죄 full RuleIR Sol 검토 및 수동 정정

작성일: 2026-07-18

사용자의 명시적 승인으로 정리된 full RuleIR을 Sol에 정확히 1회 보냈다. 동시성 1,
retry 0이었고 이 검토 뒤 추가 API 호출은 하지 않았다.

- model: `openai/gpt-5.6-sol`
- prompt tokens: 66,754
- completion tokens: 3,322
- reasoning tokens: 903
- total tokens: 70,076
- verdict: `reject`
- findings: 13개

에이전트가 13개 지적을 NormCard 원문과 승인 정책에 다시 대조했다. 11개는 수용 또는
수정수용했고 2개는 불수용했다. 전체 판정과 이유는
`data/rulegen/fraud/fraud_full_rule_ir_sol_adjudication.md`에 기록했다.

주요 정정은 다음과 같다.

- 법적 주체인 `defendant_id`와 중복되고 의미가 없던 `subject_id` 삭제
- 현실적 재산상 손해 불요 문구를 최종 AND의 사실 gate와 자동 파생 rule에서 삭제
- 추상적 기망·착오 정의 카드와 취득 예시 카드가 단독으로 구성요건을 충족하던 경로 제거
- 고의를 의도적 기망, 행위시 고의, 처분 유도 의사, 재산적 이득 목적으로 구체화
- 삼각사기의 재산소유자 및 제3자취득 수익자에 `distinct_entity` 검사 추가
- 구성요건 AND를 `fraud_elements_satisfied` 후보로 분리하고, 완결된 사건에서 명시적
  불성립·충돌이 모두 없을 때만 `fraud_established`를 출력하도록 최종 층화 부정 도입

정정본은 NormCard 88장을 그대로 보존하며 commentary input도 standard 60개와 rule fact
28개로 유지한다. predicate는 201개, rule은 342개다. full-generation validator와 전체
테스트 `63 passed`를 확인했다.

현재 상태는 `agent_post_sol_rereview_complete_human_review_pending`이다. 사용자가 Sol
재검토표의 일반형/삼각사기 역할정책, 주관적 요건 묶음, `case_assessment_complete`
실행계약을 승인하기 전까지 Scallop compile/runtime은 차단한다.

---

## 사기죄 full RuleIR 사용자 재승인 및 Scallop 실행 검증

작성일: 2026-07-18

사용자가 Sol 정정본의 세 쟁점을 모두 승인했다. 역할 구조는 실제 모델 입력의 오탐을
후속 실험에서 관찰하는 조건으로 승인했고, 행위시 고의·처분 유도 의사·재산적 이득 목적의
주관적 요건 결합 및 `case_assessment_complete` 안전 게이트에도 동의했다. 결정은
`fraud_full_rule_ir_post_sol_human_decision.json`에 별도로 기록했다.

승인 뒤에만 deterministic compiler를 실행해 88장 전체 RuleIR을
`rules/generated/fraud_article347_full_v1.scl`로 변환했다. 컴파일 산출물은 predicate
201개와 rule 342개를 포함하며, 입력·출력 checksum과 runtime 계약은
`fraud_scallop_compile_manifest.json`에 기록했다. 추가 모델 API 호출은 없었고 모델이
반환한 코드를 직접 실행하지 않았다.

공식 native `scli 0.2.4`를 checksum으로 고정해 실제 runtime test를 수행했다.
프로젝트 Python 3.11/3.12와 공식 `scallopy` CPython 3.10 wheel의 비호환 때문에 native
CLI를 사용하며, 바이너리는 Git에서 제외하고 설치 스크립트만 추적한다.

host fact validator는 다음 입력을 Scallop 전에 차단한다.

- router가 선택하지 않은 카드의 assessment
- 선택된 카드의 provable 평가가 빠진 닫힌 사건
- 동일 ID에 대한 `distinct_entity` 주장과 actor tuple 밖 entity
- 중복 assessment ID, 허용되지 않은 status, unsafe scenario/query identifier

실제 골든 시나리오 9개를 실행했다. 일반형·삼각사기·제3자취득의 정상 성립 3개는
`fraud_established`를 출력했고, 완결 게이트 누락, 삼각사기·제3자취득의 역할 상이성 누락,
명시적 불성립 bar, 상충 assessment, unknown은 모두 최종 성립을 차단했다.

JSON 산출물은 기계 재현용으로만 유지한다. 사용자 검토용
`fraud_scallop_runtime_human_report.md`에는 수동 입력한 기본 판단 14개, 역할 ID, 9개
사례별 변경점과 실제 출력, 아직 LLM/RAG/자연어 추출을 시험하지 않았다는 한계를
한국어로 풀어 썼다.

검증:

- full RuleIR validation 및 deterministic compile: 통과
- official `scli 0.2.4` checksum/version: 통과
- Scallop golden runtime: 9/9 통과
- 신규 compile/runtime/host-validation 테스트: `5 passed`
- 전체 테스트: `68 passed`
- 추가 API 호출: 0

---

## 사기죄 IRACPlan 장문생성 6방법 실제 비교

작성일: 2026-07-18

같은 KCL 사기죄 사례에 대해 직접생성, RAG, FactGraph+RAG,
FactGraph+Scallop, IRACPlan, ClaimGraph 검증·부분재생성의 6개 방법을 실제 로컬
Gemma4-vLLM Slurm 실험으로 완료했다. 최종 job `210075`는 `COMPLETED 0:0`, 총 6분
18초였다. 모델에는 KCL rubric을 제공하지 않았고, 모든 방법은 prefix cache 없이 독립적으로
필요 neural stage를 다시 실행했다.

warm E2E latency는 방법 순서대로 4.952, 7.038, 16.879, 41.767, 47.250, 124.561초다.
RAG는 0.03~0.04초, IRACPlan 컴파일은 약 0.004초, Scallop은 약 4.46초였으며 나머지
대부분은 모델 호출이었다.

RAG-only 답안은 본문에서 사기죄 성립이라고 쓰면서 구조화 overall은 `undetermined`로 내적
불일치를 보였다. IRACPlan 답안은 5개 쟁점을 모두 커버했지만 ID 오기와 필수 카드 누락
4개가 있었다. ClaimGraph는 객체·역할 및 고의 두 단락에서 6개 위반을 찾았고 그 두 단락만
재생성했다. 나머지 3단락의 해시를 보존한 채 최종 위반 0개로 끝났다.

사람용 전체 matrix, 답안별 질적 평가, KCL rubric 사후대조, 시행착오와 한계는
`docs/research/fraud_irac_matrix_human_report.md`에 기록했다. 기계 보고서는
`data/e2e/fraud/irac_matrix/fraud_irac_matrix_report.json`, 실제 6개 답안은 같은
디렉터리의 `m*_answer.md`에 있다.

---

## 개선 M5 확정 및 사기 작성례 확장 조사

작성일: 2026-07-19

job `210098`의 개선 M5를 기본 장문 생성 아키텍처로 확정했다. 카드별 application만
Gemma가 생성하고 검수 법리, provenance, 단락 소결은 host가 컴파일한다. M6은 기본 경로가
아니라 사람 gold 평가와 불확실 사건의 evaluator/fallback으로 사용한다.

기존 검수 완료 매뉴얼 인덱스
`/data5/jaehoonjeong/sp/data/processed/manuals/manual_crimefacts_economic_v2`를 확인했다.
사기 범주는 물리면 55~81의 21개 leaf이며 차용, 변제기 연장, 묵시적 기망, 계약금,
삼각사기, 소송사기 등 서로 다른 실행 경계를 포함한다. 다만 원문에 고의·기망·적용법조와
결론이 이미 들어 있어 성능평가용 raw case가 아니라 positive conformance 자료로 분류했다.

조사 당시 런타임은 `loan_purpose` 13장과 KCL 고정 IRAC 문구만 배선돼 있었다. 이 제약은
아래의 다중 사례 일반화 작업에서 해소했다. 첫 확장 후보와 프로파일별 근거는
`docs/research/fraud_manual_case_inventory.md`에 사람이 읽는 표로 정리했다.

---

## 사기죄 M5 다중 사례 일반화 및 중립 Paraphrase

작성일: 2026-07-19

사용자의 지시에 따라 외부 API와 로컬 LLM 호출 없이 개선 M5를 복수 사건에 재사용할 수 있게
일반화했다. 사건 계약에 필수·허용 프로파일, 검수된 reasoning plan, 5개 역할, 대상 거래와
생성 제한을 명시하고, 카드 순서·IRAC 단위·RAG query를 6개 계획 registry로 분리했다.

기존 KCL 용도기망 13장 경로를 보존하면서 차용금, 변제기 연장, 무전취식, 공급계약금,
택배물 삼각사기의 5개 경로를 추가했다. 각 계획은 5개 IRAC 단위와 13~17장의 검수 카드로
구성된다. 러너는 단일 case JSON뿐 아니라 case set과 `case_id`를 받아 같은 M5 코드를
실행한다.

매뉴얼 작성례 5건은 금액·행위 순서·객관적 사정을 유지하되 기망·편취, 적용법조,
의사·능력 부재의 직접 단정을 제거해 수작업으로 paraphrase했다. 원문은 복제하지 않고
`leaf_id`, 사례 순번, 물리면, 원문 segment 문자 수와 SHA-256을 기록했다. 별도 검증기로
실제 인덱스의 5개 원문 구간과 hash가 모두 일치함을 확인했다.

검증 결과는 다음과 같다.

- 패러프레이즈 provenance: 5/5 일치
- 5개 새 계획의 host-only M5 compile 및 Scallop wiring: 5/5 통과
- 기존 KCL replay를 포함한 전체 테스트: `108 passed`
- `compileall`, `git diff --check`: 통과
- API 호출 및 모델 호출: 0

구조, 산출물, 실행법과 neural 품질평가의 남은 범위는
`docs/research/fraud_m5_generalization_report.md`에 정리했다. 이번 통과는 neural 추출 정확도를
뜻하지 않으며, 실제 실험 전 사람이 5건의 카드별 gold와 허용 결론을 정해야 한다.

---

## 사기죄 수동 Paraphrase 5건 M5·M6 비교

작성일: 2026-07-19

수작업으로 중립화한 사기죄 사례 5건 전부에 대해 로컬 `Gemma-4-26B-A4B-it`로 M5와
M6을 독립 실행했다. 외부 API는 사용하지 않았다. 최종 산출물은 job `210102`의 1번,
job `210105`의 2~4번, job `210106`의 5번이며, 각 사건에 두 답안 JSON·사람용 Markdown과
실행 보고서를 보존했다.

M5는 평균 33.365초, 사건당 모델 3회, 총 72,172 tokens였고 최종 답안 계약 위반은 0건이다.
M6는 평균 120.214초, 사건당 모델 6회, 총 320,343 tokens였으며 ClaimGraph 위반은
repair 전 45건에서 후 40건으로 줄었다. 무전취식에는 ClaimGraph 위반과 중복되는 최종 답안
계약 위반 1건도 남았다. 두 방법의 평균 Scallop 시간은 각각 4.417초와 4.403초로 사실상
동일하므로 M6의 3.60배 latency는 추가 neural stage에서 발생했다.

5건 모두 최종 결론은 `undetermined`였다. 공급계약금 사례는 명시된 허위말과 객관적 상태를
가장 잘 연결했지만, 무전취식은 객관적 사정으로부터 묵시적 기망·행위시 의사를 충분히
추론하지 못했다. 삼각사기는 당사자 역할을 한 문단에서 뒤집고 명시된 인과관계를
`unknown`으로 둔 오류가 M5와 M6 모두에서 확인됐다. 이 결과는 정적 계약 통과와 neural
법률 적용 정확도가 별개임을 보여준다.

사람용 비교표와 사례별 한줄평은
`data/e2e/fraud/manual_paraphrases/experiments/m5_m6_all5/fraud_m5_m6_all5_human_report.md`,
기계 집계는 같은 디렉터리의 `fraud_m5_m6_all5_summary.json`에 기록했다.

최종 검증은 전체 테스트 `112 passed`, 패러프레이즈 provenance 5/5, 사람용·기계 답안
각 10개와 사건 보고서 5개 존재, 사람용 Markdown 내부 ID 노출 0건, 집계 JSON과 원시 보고서
수치 일치, `compileall`, Slurm shell 문법 및 `git diff --check` 통과다.

---

## M5 Neural Prompt 및 전체 IRAC 개편

작성일: 2026-07-19

사용자 검토 결과를 반영해 M5 장문 구조를 구성요건별 독립 IRAC에서 사기죄 성부 전체를
대상으로 한 단일 IRAC으로 변경했다. IRACPlan의 다섯 unit은 출력 단락이 아니라 카드와
구성요건 누락을 막는 내부 coverage ledger로 유지한다. 최종 답안은 Issue, Rule,
Application, Conclusion 네 구획이고, Application 안에서 unit별 적용과 소결을 순서대로
제시한다.

실제 중간 산출물을 추적한 결과 기존 M5는 FactGraph, 카드 assessment, 카드별 적용문 재작성의
3회 호출이었다. 세 번째 호출은 assessment rationale을 거의 그대로 반복하면서 역할 전도와
형식 오류를 추가할 수 있어 제거했다. 현재 M5는 FactGraph와 카드 assessment의 2회 호출만
사용하고, host가 검수 법리·provenance·unit 소결·Scallop 전체 결론을 조립한다.

FactGraph 프롬프트에는 관계를 문법과 전체 맥락에 따라 신중하게 판단하는 규칙과 명시적
인과 접속어 보존, `unresolved_questions`의 비증거성을 추가했다. 특정 사례의 발언·주문을
직접 겨냥한 representation 분류 규칙은 사용자 검토에 따라 제거했다. assessment 프롬프트에는
객관적 사정으로부터의 좁은 추론, 처분 요청에 나타난 처분 유도 의사, causal card 사이의
일관성, 역할관계의 신중한 적용 및 완결문 형식을 추가했다.

또한 추상적 NormCard proposition 자체를 사건에서 참인지 평가하던 인터페이스를 수정했다.
reasoning plan이 각 카드에 `unit_issue`, 사건별 `adjudication_question`,
`unit_satisfied_status`를 붙여 전달하므로 모델은 법리를 사건용 판단 질문으로 번역할 수 있다.
assessment rationale의 선행 세미콜론·콜론·쉼표·하이픈과 종결부호는 host가 결정론적으로
정규화한다.

과거 5건의 IRACPlan을 모델 호출 없이 새 compiler에 재생해 전체 IRAC JSON·Markdown 10개를
생성했다. 이는 구조 검증이며 기존 neural 의미 오류는 그대로 남는다. 새 프롬프트의 정확도는
다음 실제 모델 재실험에서 카드별 사람 gold와 대조해야 한다. M6은 동결 연구 경로로 남겼고,
전체 IRAC으로 다시 사용할 때 ClaimGraph와 repair 계약을 별도로 이관해야 한다.

상세 설계와 5건 답안 링크는
`docs/research/fraud_m5_neural_prompt_and_whole_irac.md`에 정리했다. 전체 테스트 `115 passed`,
5건 whole-IRAC compile과 구조 검증 5/5, 패러프레이즈 provenance 5/5, `compileall`, Slurm shell,
JSON, `git diff --check`가 통과했다. 외부 API 및 로컬 모델 호출은 모두 0회다.

---

## M5 프롬프트 공개·비노출 경계 및 KCL 재실험

작성일: 2026-07-19

현재 M5의 두 system prompt 전문과 실제 runtime payload 구조를
`docs/research/fraud_m5_prompt_full_review.md`에 해시와 함께 기록했다. 관계를 기계적으로
뒤집지 말라는 표현은 원문의 문법·전체 맥락, 주체·객체·소유·지위 귀속을 대조하여 신중히
판단하고 복수 해석은 보류하라는 규칙으로 교체했다. 특정 무전취식 유형을 겨냥한 FactGraph
분류 규칙은 제거했다.

`unknown`은 실패가 아니라 현재 증거에 따른 결론 보류로 정의했고, 해소에 필요한 구체적
사실·증거를 `missing_facts`에 남기게 했다. 반면 `unresolved_questions`, fact ID와 같은 내부
메타데이터는 최종 답안에 노출하지 않는다. host compiler에 비노출 검사를 추가하고 과거 5건을
재생한 결과 사람용 Markdown에서 내부 marker는 0건이었다.

수정된 M5로 KCL `kcl_criminal_r14_p1_q2`를 로컬 Gemma4에서 재실험했다. 첫 job `210278`은
부정형 카드의 `not_satisfied`에 counter fact가 없어 계약 단계에서 중단됐다. 모델 출력을
host가 법적으로 보정하지 않고, 부정형 proposition의 적극적 반증 사실을
`counter_fact_ids`에 넣도록 prompt를 명확히 했다. job `210285`는 같은 문항을 2회 모델
호출로 완료했고, 사기죄 성립 결론과 단일 전체 IRAC을 생성했다.

warm E2E는 26.262초였고 FactGraph 6.695초, assessment 15.057초, Scallop 4.474초,
host IRAC compile은 0.006초 미만이었다. 최종 답안 계약 위반과 내부 marker 노출은 0건이다.
FactGraph의 fact-kind 오분류 1건과 불필요한 미확인 질문 1건, 모든 카드 confidence가 1.0인
점은 후속 다수 사례 평가 대상으로 남겼다. 상세 결과와 사람용 평가는
`docs/research/fraud_m5_whole_irac_kcl_v3_report.md`에 기록했다. 외부 API는 사용하지 않았다.
최종 회귀 검증은 전체 테스트 `116 passed`, 패러프레이즈 provenance 5/5, `compileall`,
Slurm shell 문법과 `git diff --check` 통과다.

---

## 사기죄 Core + 선택적 Profile 전환

작성일: 2026-07-19

이전 절의 완제품 reasoning plan 및 카드별 `adjudication_question` 설계를 폐기했다. 활성 구조는
항상 적용되는 `fraud_core`에 사건별 profile을 0개 이상 더하는 조합형 registry다. 일반,
차용 목적, 변제 의사·능력, 계약 이행, 묵시적 기망, 재산상 이익과 삼각사기를 독립 profile로
두었고 복수 profile을 함께 적용할 수 있다. 과거 case의 `reasoning_plan_id`는 routing에 쓰지 않는다.
일반 사건은 별도 `ordinary` profile 없이 core만 적용한다.

두 번째 모델 호출은 조합된 카드 중 `standard_input`만 평가한다. Unit은 IRAC의 다섯 쟁점을
묶는 목차로만 사용하고 카드 판정 질문으로 전달하지 않는다. 피기망자·처분자 동일성, 삼각사기
역할 구조, 기망과 처분의 연결, 순차적 인과관계와 기수 등 7개 deterministic 규칙은 역할 정보와
standard 평가에서 Scallop이 도출한다. 삼각사기 profile의 비관련
`contract_breach_distinction` 카드는 제거했다.

`generation_instructions`와 중복 `status_semantics`를 활성 모델 payload에서 제거했다. IRACPlan은
neural `card_assessments`와 symbolic `deterministic_rules`를 분리해 기록하며, Rule 단락에는 둘을
모두 반영한다. 현재 사례별 neural 카드 수는 9~12개이고 KCL 차용 목적 replay는 11개다.

실제 `scli 0.2.4` 골든 9건은 9개 기본 standard 판단과 역할 정보만 입력해 전부 예상 결과와
일치했다. KCL replay도 11개 neural 평가에서 `fraud_established=true`를 도출했다. 전체 테스트
116건, `compileall`, `git diff --check`가 통과했다. API와 로컬 LLM 호출은 0회다. 구조와
호환 코드의 범위는 `docs/research/fraud_reasoning_plan_prompt_reset_v2_review.md`에 정리했다.

---

## M5 활성 프롬프트-계약 불일치 전면 정정 및 실기동 복구

작성일: 2026-07-19

### 문제 진단

Core+Profile 전환은 registry 데이터와 라우터 코드만 새 설계로 바꾸고 활성 프롬프트를
직전 설계 기준으로 남겨 두었다. 정적 테스트는 데이터·코드 층만 검사했기 때문에 다음
불일치가 전부 통과 상태로 잠복해 있었다.

1. `fraud_standard_assess.md`가 payload에서 제거된 `assessment_context.adjudication_question`
   과 `unit_satisfied_status`를 판정 기준으로 지시했고, 확정 설계와 반대로 "추상적 법리
   문장 자체가 참인지 평가하지 말라"고 요구했다.
2. `fraud_fact_graph_extract.md`가 registry에 없는 `ordinary` profile을 선택 가능한 축으로
   안내했다. 모델이 이를 출력하면 라우터가 `FraudPlanningError`로 중단된다.
3. 검토 문서의 "FactGraph·카드평가 v2 활성 반영" 주장과 달리 실제 파일은 구 포맷에 부분
   패치만 있었다.
4. 커밋 9dfa6f3의 `disable_any_whitespace:true`가 미커밋 수정에서 삭제되었고, 테스트 단언도
   `"backend":"guidance"`로 약화되어 회귀가 통과되었다.
5. 사용자가 지시한 Gemma 4 권장 sampling(top_p 0.95, top_k 64)이 코드 어디에도 배선되지
   않았다. temp 1.0 실행은 절단 없는 전체 분포 샘플링이었다.
6. 계약 위반으로 파이프라인이 죽으면 리포트 파일을 쓰지 않아, 이전 실행의 성공 리포트가
   최신 결과처럼 남았다. 구 프롬프트 4설정 실행은 실제로 3/4이 실패했으나 보고되지 않았다.

### 정정 내용

- FactGraph·카드평가 활성 프롬프트를 v2 검토본 구조로 재작성하되, 실제 payload와 JSON
  Schema 필드에 전수 대조해 정합화했다. 승인된 기존 규칙(인과 접속어 보존, 관계 신중
  판정, beneficiary 직접취득자 한정, 부정형 counter fact)은 유지했다.
- confidence 보정 규칙(결정적 증거일 때만 1.0), 인용 말줄임 생략 금지, 부정형 proposition의
  추상 평가 금지 및 `counter_fact_ids` 매핑 명시 예시를 추가했다.
- user message를 raw JSON에서 `<INPUT_JSON>` 데이터 블록 템플릿으로 교체했다. vllm_client에
  `user_template`를 추가하고 M5 활성 2개 호출에만 연결했으며 M1-M4/M6 경로는 보존했다.
- `disable_any_whitespace:true`를 복원하고 테스트 단언을 원상복구했다. SLURM 스크립트에
  권장 sampling(case_c/d: temp 1.0, top_p 0.95, top_k 64)을 배선했다.
- thinking 실행의 completion 예산을 fact 12,000, assessment 20,000으로 확대했다.
- 계약 위반 시에도 실패 리포트를 항상 기록하도록 러너를 수정했고, vLLM 실패 진단에
  message 키·reasoning 문자수·finish_reason을 추가했다.
- 재발 방지 가드 테스트: 활성 프롬프트에 `adjudication_question`, `unit_satisfied_status`,
  `ordinary`, `status_semantics`가 재등장하면 실패한다.

사용자가 4개 프롬프트 전문(system 2, user 템플릿 2)을 검토하고 현행대로 승인했다.

### 실행 기록

- job `210477`: 구 설정 오류(공백 가드 부재, 절단 없는 샘플링) 상태로 제출되어 vLLM 로딩
  중 취소. 사례 실행과 리포트 갱신 없음.
- job `210478` (진단 실행): case_a는 부정형 카드 근거를 `basis_fact_ids`에 넣어 계약 위반,
  case_b는 인용 말줄임 생략으로 검증 실패, case_c는 유일하게 완주했으나 부정형 카드를
  추상 명제로 `satisfied` 평가하여 `not_established`로 왜곡, case_d는 reasoning이 5,000
  토큰 예산을 소진해 본문 미생성. 이 결과로 위 프롬프트 보강과 예산 확대를 결정했다.
- job `210480` (승인 프롬프트 정식 실행, `COMPLETED 0:0`, 8분 20초):
  - case_a(greedy): pass, `fraud_established`, 부정형 카드 `not_satisfied`에 counter fact 2개
  - case_b(greedy+thinking): fail, reasoning 29,597자 폭주 후 12,000 토큰 소진. greedy와
    thinking의 조합은 퇴화 루프로 판단
  - case_c(권장 sampling): pass, `fraud_established`, confidence 0.9~1.0 분포
  - case_d(권장+thinking): reasoning은 완료되었으나 인용 전사에서 `B에게서`를 `B에서`로
    적어 정확 인용 검증에서 차단. stale report 수정 덕에 실패가 리포트에 정상 기록됨
- 구 프롬프트 대비: 이전 4설정은 1/4 통과에 결론도 `not_established`로 오답이었다. 현재는
  비-thinking 2설정이 모두 통과하고 기대 결론 `established`를 복원했으며, `loan-purpose-
  materiality`도 satisfied로 판정된다. 전체 IRAC 답안 2건이 정상 컴파일되었다.
- 구 프롬프트 리포트 4건은 `data/e2e/fraud/experiments/m5_kcl_pre_prompt_v2/`에 백업했다.

### 검증

- 전체 테스트: `118 passed` (사용자 템플릿 래핑, 프롬프트-계약 가드 신규 2건 포함)
- `compileall`, `git diff --check`, SLURM shell 문법: 통과
- 외부 API 호출: 0회. 로컬 LLM은 사용자 승인 하에 SLURM job 3회 제출(1회 취소)

### 남은 항목

1. thinking 경로: greedy 조합은 사용하지 않는 것으로 정리하고, 권장 sampling+thinking의
   한 글자 전사 오류는 재시도 정책 또는 인용 검증 완화 없이 재현율을 더 관찰
2. confidence 분포가 여전히 1.0 편중(11개 중 2개만 0.9). 다수 사례에서 재평가 필요
3. `loan-purpose-materiality`의 satisfied/unknown 경계는 판례상 중요성 추정 법리의 카드
   보강 여부와 함께 법률 검수 대상

---

## 5건 Paraphrase thinking-off 2강 비교

작성일: 2026-07-19

사용자 결정에 따라 thinking을 기본 비활성으로 확정하고, 수동 paraphrase 5건 전부를 M5로
greedy(job `210499`)와 Gemma 4 권장 sampling temp 1.0/top_p 0.95/top_k 64(job `210500`)
두 설정에서 독립 실행했다. 두 job 모두 `COMPLETED 0:0`, 각 약 11분이며 사건당 warm latency는
21~23초, 모델 호출은 사건당 2회다. 외부 API는 사용하지 않았다.

### 기계 결과

- 10개 런 전부 neural 2단계와 Scallop, host IRAC 컴파일을 완주했고 답안 10건이 생성됐다.
- 결론 분포: greedy는 undetermined 4, not_established 1(공급계약금). sampling은
  undetermined 3, not_established 2(차용금, 택배삼각). established는 없다.
- confidence는 KCL과 달리 넓게 분산됐다: greedy {0.5:21, 0.6:1, 0.7:4, 0.8:3, 0.9:3,
  1.0:22}, sampling {0.5:18, 0.6:1, 0.7:3, 0.8:3, 0.9:4, 1.0:25}. 1.0 편중 문제는
  paraphrase 사건에서 해소된 것으로 확인했다.
- 삼각사기 역할 구조는 정확했다: 피기망자=처분자(actor_c), 재산귀속자(actor_b),
  피고인=수익자(actor_a). 과거 실험의 역할 전도는 재발하지 않았고, 인과관계 판단은
  deterministic 규칙으로 이관되어 모델 오판 경로 자체가 제거됐다.

### 질적 관찰

- intent 계열 카드(`time_of_conduct`, `gain_purpose`)가 거의 전 사건에서 unknown이다.
  paraphrase가 의사·능력 부재의 직접 단정을 의도적으로 제거했으므로 보수적 보류는
  설계상 예상 범위이나, 성립 gold가 정해지면 객관적 정황 추론의 허용 폭을 재조정해야 한다.
- 부정형 카드 `no_disposition_inducement_intent`는 KCL에서는 교정됐지만 paraphrase에서는
  사건에 따라 satisfied(추상 평가)로 회귀했다: greedy 공급계약금, sampling 차용금·택배삼각의
  not_established는 이 카드 오판이 원인이다. 명시적 처분 요청 사실이 약한 사건에서
  불안정하며, 카드 문언 자체의 조건문 구조가 원인이므로 proposition 재서술 또는 host 극성
  분리를 후속 검토 항목으로 남긴다.

### 검증기 오탐 정정

10개 런 모두 `completed_with_violations`로 기록됐으나, 위반은 전부 matrix 러너의
`run_whole_irac_answer`가 허용 카드 목록을 `card_assessments`에서만 만들고 Core+Profile
전환이 분리한 `deterministic_rules` 카드를 누락한 host 검증기 결함이었다. 허용 provenance를
`whole_irac_allowed_provenance`로 분리해 두 카드군을 모두 포함하도록 수정하고 회귀 테스트를
추가했다. 저장된 답안 10건을 모델 호출 없이 수정된 검증기로 재검증한 결과 위반 0건이며,
각 실험 디렉터리의 `revalidation_after_validator_fix.json`에 기록했다.

### 검증

- 전체 테스트: `119 passed`
- `git diff --check`: 통과
- 잔여 작업 목록: `docs/research/idpr_remaining_work.md`로 분리

---

## 부정형 카드 극성 분리와 수사지원 목표 확정

작성일: 2026-07-20

10런 육안 검토 자료를 만들고 사용자 코멘트를 반영하는 과정에서, 결론이 갈린 원인이
부정형 카드 한 장의 부호 뒤집힘임을 특정하고 수정했다. 아울러 프로젝트의 최종 산출물을
수사지원으로 확정했다. 외부 API 호출 0회, 로컬 vLLM SLURM job 2회(사용자 승인).

### 진단

`fraud_intent.no_disposition_inducement_intent`(명제: "피기망자로 하여금 처분행위를 하게
할 의사가 없으면 사기죄가 성립하지 않는다") 한 장에서 모델이 실질 판단과 반대 부호를
기록했다. 공급계약금 사건에서 greedy와 sampling의 rationale이 모두 "…B로 하여금 계약금을
지급하도록 유도하였다"로 동일한데 status는 `satisfied`와 `not_satisfied`로 갈렸다.
모델이 부호를 확정한 5회 중 3회가 뒤집혔고, 그 3회가 그대로 잘못된 `not_established`
종결이 됐다.

미확인이 원인이라는 초기 가설은 데이터로 반박됐다. `fraud_not_established` 규칙 36개는
전부 "부정형 카드가 `satisfied`"일 때만 발화하므로 unknown에서 불성립이 도출되는 경로는
없다. 3건 모두 `fraud_undetermined`도 동시에 참이었으나 `legal_result()`의 우선순위가
`not_established`를 먼저 반환해 최종 라벨에서 미확인이 사라졌다.

프롬프트 보강은 이미 소진된 상태였다. `fraud_standard_assess.md`는 바로 이 카드를 축자
예시로 들어 `counter_fact_ids` 배치까지 지시하고 출력 전 자체 점검을 요구하는데도 실패했다.

### 문장 구조 분류

사용자 지적("잘하는 카드는 부정어 1개, 못하는 카드는 이중부정")을 88장 전체에서 검증했다.
이중부정 카드 11장은 **전부** negative polarity이고 positive 중 이중부정은 0장이다. 한국
법문에서 불성립 규범이 "…없으면 …않는다"로 쓰이므로 문장의 이중부정과 법적 결론의 방향
역전이 항상 같이 온다. 따라서 "이중부정이 어렵다"와 "라벨 방향이 어긋나면 직관을 따른다"는
두 가설은 현재 데이터에서 교락되어 분리되지 않는다. 분류 결과는
`docs/research/fraud_card_linguistic_difficulty.md`에 정리했다.

### 조치

사용자 승인 하에 두 가지를 적용했다.

1. host 극성 분리. registry에 `neural_query`(긍정 술어 + 카드별 매핑 방향)를 두고,
   모델에게는 긍정 술어만 판정시킨 뒤 host가 부호를 되돌린다. 카드 세트와 Scallop 규칙은
   변경하지 않았고 답안이 인용하는 문언도 원문(부정형)을 유지한다.
2. 구조적 안전망. 부정형 카드가 `satisfied`인데 그 근거 사실이 같은 사건에서 `satisfied`인
   긍정 카드의 근거와 겹치면 `unknown`으로 강등한다.

구현 중 발견: 부호를 역전할 때 `basis_fact_ids`와 `counter_fact_ids`도 함께 swap해야
한다. 긍정 질의를 뒷받침하는 사실이 곧 부정형 카드를 깨는 사실이므로 의미상 맞고,
그렇게 하지 않으면 "`not_satisfied`는 counter_fact 필수" 계약에 걸린다. 결과 번들이 정답
런의 모양과 정확히 같아진다. 또한 매핑이 부정형 카드마다 균일하지 않아(내재 술어가 이미
정렬된 카드는 동일 매핑) 카드별 선언 방식이 필요했다.

승인된 질의문: "행위자에게 피기망자로 하여금 바로 그 재산적 처분행위를 하게 할 의사가
있었다."

### 실행 기록

job `211051`(greedy), `211052`(권장 sampling) 모두 `COMPLETED 0:0`, 각 약 4분 30초.

| 지표 | 적용 전(`210499`/`210500`) | 적용 후(`211051`/`211052`) |
|---|---|---|
| 잘못된 `not_established` | 3건 | 0건 |
| 부호 뒤집힘 | 부호 확정 5회 중 3회 | 부호 확정 8회 중 0회 |
| 두 설정 카드 판정 불일치 | 5 / 54 | 1 / 54 |
| 계약 위반 | 0 | 0 |
| 안전망 발화 | — | 0회 |

10런 전부 `undetermined`로 수렴했고 두 설정이 전 사건에서 일치한다. 남은 불일치 1건은
차용금 사건에서 greedy `not_satisfied` / sampling `unknown`으로, 부호 오류가 아니라
확신도 차이다. 안전망이 한 번도 발화하지 않은 것은 원인을 발생 지점에서 제거했기
때문이며 잔여 사례용 방어선으로만 유지한다.

부수 관측: 모델이 부호를 확정한 횟수가 5회에서 8회로 늘었다. 이중부정 명제일 때 보류하던
사례가 긍정 술어에서는 답을 냈다는 뜻으로, 문장 구조가 판정 회피도 유발했다는 정황이다.

답안은 의도한 형태로 나온다. 법리 구획은 원문("…의사가 없으면 사기죄가 성립하지
않는다")을 인용하고, 적용 구획은 긍정 술어 기준 서술("A는 …B로 하여금 계약금을 지급하도록
유도하였다")이 들어간다.

### 확정된 프로젝트 목표

파이프라인의 최종 산출물을 유무죄 판정이 아니라 **수사지원**으로 확정했다. Scallop이 닫지
못한 구성요건과 카드별 미확인 사유로 확인 항목을 만들고, 유사 판례(사실심·법률심 분리
적재)를 붙여 보강 의견을 낸 뒤 체크리스트 → 수사계획 → 신문 질문지 → 영장 별지로 이어진다.

현재 파이프라인의 약점이 그대로 강점이 된다. 5건 전부 `undetermined`이고 intent 계열이
대부분 `unknown`인데, 수사지원에서는 그 목록이 산출물이다. 이미 산출되는 재료는 FactGraph
`unresolved_questions`(설정별 7개)와 카드별 `missing_facts`(greedy 29 / sampling 26)이며,
후자는 **구성요건 단위에 앵커되어 있다.**

RAG의 용도도 장문 생성 보강이 아니라 미확인 요건의 착안사항 생성으로 재정의했다. 핵심
제약은 판례로 사실인정을 하지 않는 것이다. 판례는 "그 요건이 인정된 사건에서 법원이
무엇을 근거로 삼았는가"를 제공하고 그 근거가 확인 항목 목록으로만 변환된다.

착수 순서: 극성 수정(완료) → 결론 구조화 → 체크리스트 산출 → RAG 판례 → 문서 생성.

### 검증

- 전체 테스트: `124 passed` (신규 5건: 질의 치환·원문 보존 대조, 미등록 부정형 카드 차단,
  역매핑 시 배열 swap, 동일매핑 시 무변경, 안전망 발화/미발화, resolved 번들의 계약 통과)
- `compileall`, `git diff --check`: 통과
- 프롬프트 파일 변경 없음. 부정형 명제가 모델에 도달하지 않으므로 기존 부정형 지침은
  도달 불가 상태로 남되 다른 경로 대비 안전망으로 유지했다.

### 남은 항목

1. `scripts/run_fraud_neural_e2e.py:194`의 구 M1-M4 경로는 여전히 부정형 원문을 모델에
   보낸다. 회귀는 없으나 활성 경로와 갈라졌으므로 레거시 정리에서 함께 처리한다.
2. 나머지 negative 24장은 배선 시점에 질의문 초안을 승인받는다.
3. 결론 구조화(무죄와 미완결의 분리)가 다음 작업이다.

## 장물 rulegen 파일럿 + 실체 캠페인 준비 (2026-07-22)

A3 평가셋 확장을 위해 사기 rulegen 파이프라인을 신규 죄명(장물, 제362조)에 파일럿하고,
실체법 47개 조문 캠페인을 실행 직전까지 준비했다. terra/sol API는 파일럿 4콜(~$0.5)만
실행했고 전량 캠페인은 예산 게이트로 대기시켰다.

### 파일럿 성과 (장물 제362조, job 211617/211619/211635)

- **terra/sol = gpt-5.6 추론 모델 확정.** 추출은 `reasoning_effort=low` + `max_tokens≥16000`가
  필수다. 기본 6000은 reasoning 토큰이 한도를 전부 소진해(`finish_reason=length`) 실패했다
  (job 211617). 사기 시절 terra는 비추론이라 6000으로 됐던 것. `run_fraud_rulegen_pilot.py`에
  `--terra-reasoning-effort` 추가, sbatch 기본값 low/16000으로 교정하니 reasoning이 6000→326/31
  토큰으로 정상화됐다.
- **밀도 = 사기의 0.5×.** 장물 25 candidates/배치 vs 사기 ~51. critic verdict=revise, 31 후보에
  findings 5. card-stage가 비용의 68%이므로 61 견적($251)의 실질 하향 근거다.
- **norm_kind='negative' 이슈.** 모델이 부정형 규범(장물성 소멸 등)에서 polarity 값 'negative'를
  `norm_kind`에 오배치해 batch 2가 스키마 검증 실패했다. A6 계열 이슈다. extract 프롬프트 규칙3을
  norm_kind(기능) vs polarity(방향) 독립 명시로 보강했다(사용자 승인). 다른 추출 동작은 불변.

### 캠페인 준비 (실행 전, 결정론·무지출)

- 실체 P1(재산범 11) + P2(OOS 비재산 16) 형법각칙 **47개 조문** requests 생성:
  `data/rulegen/campaign/art*_rulegen_requests.jsonl` (총 162 배치, 1,531 chunks).
- 신규 스크립트: `scripts/build_rulegen_requests.py`(죄명-불문 requests 빌더),
  `scripts/build_rulegen_campaign.py`(매니페스트+전 조문 생성),
  `scripts/slurm/run_rulegen_pilot.sh`(조문 1개 CPU-only sbatch, GPU 미할당),
  `scripts/slurm/launch_rulegen_campaign.sh`(전 조문 런처, 기본 dry-list).
- 단가 확정: terra $2.5/$15, sol $5/$30 per 1M. 추출+후보비평 파일럿보정 ~$35.5.
- 절차(P3 증거능력 gate / P4 규칙친화)는 A4 별도 트랙.

### 남은 게이트

1. 잔여 예산 확인 후 `launch_rulegen_campaign.sh --confirm`으로 착수(예산 게이트).
2. 다운스트림(merge·normcard critic·RuleIR)은 미파일럿 — 장물로 1회 더 돌려 실단가 확정 권장.
3. 생성 후 검토는 벌크 HITL(`docs/research/hitl_bulk_review_spec.md`)로 유형별 1회.

상세: `docs/research/rulegen_campaign_launch.md`, `rulegen_sweep_cost_estimate.md` §7.
