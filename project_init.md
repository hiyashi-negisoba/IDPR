# IDPR — In Dubio Pro Reo
## Logic-Verified Long-form Legal Document Generation

> 프로젝트 초기화 문서 (v0.1, 2026-07-14)
> 작성: 정재훈 / 대상: 파이프라인 개발 담당자
> **최종 마감: 2026-08-11 (NLLP @ EMNLP 2026, non-archival long paper)**

---

## 0. 한 문단 요약

LLM이 법률 사례형 답안(IRAC 롱폼)을 쓸 때 "논증은 맞는데 결론이 틀리는" self-consistency 실패가 발생한다.
본 프로젝트는 **결론과 논리 경로를 생성 이전에 symbolic layer(Scallop/Datalog)에서 확정**하고,
LLM은 확정된 derivation을 **언어화**만 하게 한 뒤, 생성물을 다시 predicate로 파싱해
derivation과 대조하는 **symbolic verification**으로 rerank/edit 한다.
결론이 논증에 논리적으로 결박(bind)되므로 논증-결론 불일치가 구조적으로 불가능해진다.

핵심 슬로건: **"결론은 논리가 계산하고, 문장은 모델이 쓴다."**

---

## 1. 용어 정의 (코드/문서 전체에서 이 의미로 통일)

| 용어 | 정의 |
|---|---|
| **predicate** | 법리적 판단의 최소 단위. 예: `deception(D, V)` (D가 V를 기망함). `kind: rule` 또는 `kind: standard` 속성을 가짐 |
| **rule형 규범** | 요건이 열거 가능한 규범 → Scallop rule로 인코딩 (예: 전문법칙 예외의 법정 요건, 사기죄 구성요건) |
| **standard형 규범** | 형량·종합판단이 필요한 규범 → LLM sub-call로 위임하고 결과를 **flag와 함께** derivation에 주입 (예: 절차 위반의 '중대성', 자백의 '임의성' 종합판단) |
| **derivation** | Scallop이 계산한 결론 + proof tree + 발화된 rule 목록. 생성의 조건이자 검증의 기준 |
| **evidence gating** | 절차 레이어(증거능력)가 실체 레이어(구성요건)로 전파되는 인터페이스. `admissible(E)`가 거짓이면 그 증거에 의존하는 사실은 `provable`이 될 수 없음 |
| **consistency score** | 생성 문서에서 역추출한 predicate 집합과 derivation의 정합도. 누락/모순/무근거/배제증거사용을 문단 단위로 판정 |
| **설문(sub-question)** | 변시 사례형 1문항을 쪼갠 평가 단위. 평가는 설문 단위로 수행 |

---

## 2. 파이프라인 아키텍처 (5 stages)

```
 [S0 입력]        [S1 추출]           [S2 추론]            [S3 생성]           [S4 검증/개선]
 사실관계 ──→ LLM: predicate ──→ Scallop: derivation ──→ LLM: IRAC ──→ back-parse → 대조
 (설문 원문)   추출 + confidence    (rule DB, KR)          언어화        → violations
                                        │                    ↑              │
                                        │                    └── rerank / ──┘
                                        │                        문단 edit
                                   standard형은
                                   LLM sub-call로
                                   위임 + flag
```

각 스테이지의 입출력은 **`docs/contracts/`의 JSON 스키마가 유일한 계약**이다.
스키마를 바꾸려면 반드시 정재훈 승인 후 contracts부터 갱신할 것 (스키마 = API).

### S1. Predicate Extraction (`src/idpr/extraction/`)
- 입력: 설문 원문(사실관계 + 물음)
- 출력: `PredicateInstance[]` — predicate_id, args, confidence(0~1), evidence_span(원문 인용 위치)
- 스키마에 정의된 predicate만 추출 가능 (자유 생성 금지). 스키마 밖 개념은 `unknown_issue`로 리포트
- confidence는 로짓 기반이 아닌 structured output의 self-report로 시작 (calibration은 Open Q2)

### S2. Symbolic Reasoning (`src/idpr/reasoning/`)
- scallopy 래퍼. `rules/kr/**/*.scl` 로드 → S1의 facts 주입 → derivation 산출
- **네임스페이스 2개 + 게이트**:
  - `procedural/`: 증거능력 (전문법칙 예외, 위법수집증거, 자백배제 등) → `admissible(E)`
  - `gates.scl`: `provable(F) = supports(E, F) and admissible(E)` — 증거로 뒷받침되는 사실은 적법한 증거가 있어야만 provable
  - `substantive/`: 구성요건 → `provable`한 사실만 소비
- standard형 predicate를 만나면 LLM sub-call → 결과를 fact로 주입하되 `standard_flags[]`에 기록
- 출력: `Derivation` — verdict(설문별 결론), proof_tree, fired_rules, gated_out(배제로 탈락한 사실), standard_flags

### S3. Derivation-conditioned Generation (`src/idpr/generation/`)
- derivation을 구조화 프롬프트로 변환 → 문단 계획(문단 ↔ predicate 대응 명시) → IRAC 문서 생성
- 문단마다 어떤 predicate/rule을 다루는지 메타데이터로 함께 출력 (검증 비용 절감)
- 1차 구현은 derivation-conditioned **prompting**. constrained decoding은 stretch goal (Open Q3)

### S4. Verification & Refinement (`src/idpr/verification/`, `src/idpr/refine/`)
- back-parser: 생성 문서 → 문단별 주장 predicate 재추출 (S1 추출기 재사용, 모드만 다름)
- 대조기: derivation 대비 4종 위반 판정
  - `missing`: derivation에 있는데 문서에 없음
  - `contradiction`: derivation과 반대 주장
  - `unsupported`: derivation에 없는 법리 주장 (rule hallucination 후보)
  - `inadmissible_use`: **배제된 증거를 논증에 사용** (evidence gating 위반 — 본 논문의 킬러 케이스)
- refine: (a) best-of-N rerank — graded score, (b) violation-targeted edit — 위반 문단만 국소 재생성, hard-fail 우선순위
- **모든 LLM 호출은 캐시 필수** (§5)

---

## 3. 디렉토리 구조

```
idpr/
├── PROJECT_INIT.md          ← 이 문서. 온보딩 시작점
├── README.md                ← 퀵스타트 (설치/실행 3줄)
├── pyproject.toml           ← Python 3.11+, uv 사용
├── .env.example             ← API 키 템플릿 (실제 키는 절대 커밋 금지)
├── configs/
│   ├── pipeline.yaml        ← 스테이지별 모델/파라미터 (단일 진실 원천)
│   └── experiments/         ← 실험별 오버라이드 (베이스라인, ablation)
├── data/
│   ├── raw/                 ← 변시 원문, LBox 루브릭 (gitignore, 라이선스 확인 전 외부 공유 금지)
│   ├── inventory/           ← 쟁점 인벤토리: 설문 단위 분해 + 태깅 결과 (jsonl)
│   ├── processed/           ← 평가용 최종 아이템 (커버리지 필터 적용본)
│   └── README.md            ← 데이터 출처/라이선스/변환 이력 기록 (반드시 유지)
├── rules/
│   ├── schema/predicates.yaml   ← predicate 스키마 (id, arity, kind, 한국어 정의, 근거 주석서 조문)
│   ├── kr/substantive/*.scl     ← 재산범죄부터: fraud.scl, embezzlement.scl, breach_of_trust.scl
│   ├── kr/procedural/*.scl      ← hearsay.scl, illegally_obtained.scl, confession.scl
│   ├── kr/gates.scl             ← evidence gating
│   ├── cn/                      ← (2차) JUREX-4E 기반
│   └── tests/                   ← rule별 golden test (§6 — 없으면 머지 불가)
├── src/idpr/
│   ├── extraction/  reasoning/  generation/  verification/  refine/
│   ├── rulegen/     ← 주석서 → rule 초안 반자동 추출 도구 (LLM). 산출물은 항상 사람 검수 대기 상태
│   ├── llm/         ← provider 클라이언트 + 디스크 캐시 + 호출 로깅
│   └── eval/        ← 메트릭, 루브릭 채점, 베이스라인 러너
├── docs/contracts/  ← JSON 스키마 (PredicateInstance, Derivation, VerificationReport, InventoryItem)
├── scripts/         ← CLI: tag_inventory.py, build_rules.py, run_pipeline.py, run_eval.py
├── experiments/     ← 실행 산출물 (gitignore) + runs.jsonl 레지스트리
├── notebooks/       ← 탐색용 (파이프라인 로직 두지 말 것)
├── paper/           ← ACL 템플릿, figure 생성 스크립트
└── tests/           ← 파이프라인 유닛/통합 테스트
```

---

## 4. 데이터 취급 원칙

1. **평가는 퍼블릭 데이터셋 전용, 신규 구축 없음.** 변시 형사법 사례형(61~64문항)이 1차 평가셋.
2. 문항은 **설문 단위로 분해**해 평가 (n이 150~200 규모로 확대될 것으로 예상).
3. 쟁점 인벤토리(`data/inventory/`)가 스코프의 단일 진실 원천: 설문마다 쟁점 태그(죄명/절차 쟁점) + `rule|standard` 판정 + 커버 여부.
4. 순수 지식형 설문("판례의 태도는?")은 제외, **포섭(application)형만** 평가 대상.
5. LBox 루브릭은 **평가 전용** (rule 소스로 사용 금지 — circularity 방지). rule의 원천은 주석서만.
6. raw 데이터는 커밋 금지. 재현은 `data/README.md`의 취득 절차 문서로 갈음.

---

## 5. 엔지니어링 규칙

- **LLM 호출 캐시**: 모든 호출은 (model, prompt_hash, params) 키로 디스크 캐시. 실험 재실행 시 API 비용이 0에 수렴해야 정상. 캐시 우회는 명시적 플래그로만.
- **실험 재현성**: 모든 run은 config 스냅샷 + git commit hash + seed를 `experiments/runs.jsonl`에 기록. "어떤 숫자가 어떤 코드에서 나왔는지" 추적 불가능한 결과는 논문에 못 쓴다.
- **결정론 우선**: Scallop은 inference-time discrete 모드로 시작 (미분 가능 provenance는 본 논문 범위 밖).
- **스키마 우선 개발**: contracts의 JSON 스키마 변경 → 관련 모듈 수정 순서. 역방향 금지.
- 타입 힌트 필수, ruff + pytest. 커밋 컨벤션은 conventional commits.

---

## 6. Rule 개발 프로토콜 (법률 검수 게이트)

rule은 코드이자 **법리 주장**이다. 아래 게이트 없이는 머지하지 않는다.

1. `rulegen/`으로 주석서에서 초안 추출 (LLM) → `draft` 상태
2. 정재훈 검수: 조문/주석서 근거 대조, 요건 누락/과잉 확인 → `verified` 상태로 승격
3. **golden test 필수**: rule마다 `rules/tests/`에 최소 3케이스 — 성립 / 불성립 / 경계(gating 관련이면 배제증거 케이스)
4. predicate 추가·변경은 `rules/schema/predicates.yaml` 갱신 + 스키마 버전 bump

역할 분담: **rule의 정확성 = 정재훈 책임, rule의 실행 가능성 = 개발자 책임.**
개발자는 법리 판단을 하지 않는다. 애매하면 `draft`로 두고 이슈 태그.

---

## 7. 평가 설계 (eval/ 구현 스펙)

**Metrics** (설문 단위):
- argument–conclusion consistency rate (문서 내 논증↔결론 일치)
- predicate coverage / contradiction rate (derivation 대비)
- rule hallucination rate (rule DB 밖 법리 인용)
- inadmissible-use rate (배제증거 사용 — 별도 보고)
- 루브릭 기반 채점 점수 + **meta-eval: consistency score ↔ 루브릭 채점 상관 (vs LLM-judge 상관)**

**Baselines**: IRAC zero/few-shot prompting · plan-then-write(CoT+결론 선언) · Self-Refine · Best-of-N w/ LLM-judge
**Ablations**: rerank only vs rerank+edit · derivation 조건화 유무 · format-only(rule 없이 IRAC 구조 제약만) · evidence gating on/off

---

## 8. 마일스톤 (역산: 8/11 제출)

| 주차 | 기간 | Definition of Done |
|---|---|---|
| **W1** | 7/14–7/20 | 쟁점 인벤토리 v1 (전 문항 설문 분해+태깅, 정재훈 검수 완료) · predicate 스키마 v1 · rulegen 파이프라인 동작 · 사기죄 rule `verified` + golden tests 통과 |
| **W2** | 7/21–7/27 | S1–S4 E2E가 사기 단일쟁점 설문 5개에서 동작 · 절차 레이어(전문법칙·위수증) + gates 동작 · inadmissible_use 검출 데모 1건 |
| **W3** | 7/28–8/3 | 커버 설문 전체 본 실험 (ours + 베이스라인 4종 + ablation) · 커버리지 곡선 figure · 루브릭 meta-eval |
| **W4** | 8/4–8/11 | 집필 (paper/) · 교수님 리뷰 1회전 반영 · 8/11 제출 |

주간 싱크는 W1 종료 시점에 1회 필수 (스키마 freeze 결정).

---

## 9. 결정된 것 / 열린 것

**결정 (변경하려면 정재훈 승인):**
- 결론은 생성 전 Scallop에서 확정. LLM은 추출·언어화·standard 판단만
- rule 원천 = 주석서. 루브릭·기타 데이터셋 = 평가 전용
- rule형/standard형 구분이 symbolic/LLM 위임의 기준선 (실체/절차 구분이 아님)
- 절차법 + 실체법 모두 포함, evidence gating으로 연결
- 1차 스코프: 재산범죄 클러스터(사기→횡령→배임 순) + 고빈도 절차 쟁점
- inference-time only (provenance 학습 없음)
- NLLP non-archival long paper

**열림 (구현 중 함께 결정):**
- Q1. consistency score 세부 — rerank용 graded 가중합의 가중치, edit 트리거의 hard-fail 목록
- Q2. S1 confidence의 calibration 방법 (초기: self-report, 후보: verbalized confidence·앙상블)
- Q3. constrained decoding 도입 여부 (stretch)
- Q4. 미커버 쟁점 포함 설문의 처리 원칙 (부분 평가 vs 제외 — 인벤토리 통계 본 후 결정)

---

## 10. 배경 자료 (읽는 순서)

1. 이 문서 → `docs/contracts/` 스키마 4종
2. `rules/kr/substantive/fraud.scl` + `rules/kr/gates.scl` (구조 감 잡기용 초안 — 법리 검수 전)
3. Scallop: scallop-lang.org 튜토리얼, scallopy Python API
4. 선행연구 (차별화 포인트): LeGen (Xu et al. 2024 — verifier-generator이지만 verifier가 학습 모듈), Court View Generation 계열 (C3VG/LCVG/CCVG — 2차 중국 확장 시 평가셋), JUREX-4E (중국 4요소 rule 소스)
5. OBJECTION 논문 (사내 공유본) — 본 프로젝트의 motivation이 된 failure mode 실측 출처

## 11. 추가 코멘트
- 필요한 데이터중 변시 문제는 `/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay` 에서 확인할 수 있음
- 주석서 데이터는 `/home/jaehoonjeong/data/sp_qwen/data/serve/commentary_chunks` 에서 확인할 수 있음.