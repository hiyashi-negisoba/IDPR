# Phase 3 착수 문서 — 콜 2(카드 일괄 판정) + 심볼릭 판단

> **2026-08-02 적재 구조 갱신:** 아래의 카드 전량 일괄 판정 계획은 실측 결과 폐기했다.
> 조문을 고르면 같은 slot의 일반법리·세부기준·판례 사안까지 모두 `core` 질문이 되는 것이
> 품질 저하의 원인이었다. 현재 Phase 3 진입점은 `idpr.candidates.candidate_issues()`이며,
> 적재 단위는 `조문 → 쟁점 → 일반법리 anchor → unknown일 때 하위카드 최대 2장 검색`이다.
> `candidate_articles()`와 flat-card 스모크는 Phase 2 산출물 재현·비교용으로만 보존한다.
> 선택 조문의 원본 카드가 정확히 한 issue에 배치된다는 무손실 불변식은 유지하지만, 그
> 1,848장을 모두 모델 질문으로 노출한다는 뜻은 더 이상 아니다. 상세 설계와 전수 통계는
> `docs/card_loading_v2.md` 및 `data/rulebase/issue_catalog_v2_review.md`를 따른다.

> **Phase 3 완료 기록 (2026-08-02):** 전체 1,848장을 383개 issue로 무손실
> 재배치했고, 첫 호출은 169개 구성요건 issue만 평가한다. 스모크 범위는 193개 독립 카드
> 질문에서 14개 issue·24개 anchor로 줄었다. 이후 live 조문에 대해서만 조각·미수·공범·
> 죄수 후속 쟁점을 열고 Scallop을 재실행한다. 최신 PRO6000 1장 통합 실행(Slurm 218151)은
> 29개 쟁점을 15 satisfied / 3 not_satisfied / 11 unknown으로 판정한 뒤, 작성에 필요한
> 20개 쟁점을 Call 3에 전달해 4개 죄명의 IRAC를 생성했다. 제298조·제301조의 성립,
> 제297조의 기수 차단 및 미수 검토, 제319조 핵심요건 미확정이 최종 답안까지 보존됐다.
> 최종 작성 스모크(Slurm 218154)는 내부적으로 20개 쟁점 분석을 유지하면서 최종 표현을
> 죄명별 하나의 통합 IRAC로 렌더링했다. 전체 회귀 테스트는 487개가 통과했다.
> 실제 런타임은 `candidate_issues()` → `issue_status`를 사용한다. 아래의 flat-card 작업
> 순서는 역사적 계획 및 회귀 비교 자료다.

2026-08-01. 데드라인 **2026-08-11** (NLLP 워크샵). 브랜치 `rulegen-campaign-pilot`.
테스트 415 passed. Phase 0~2 완료.

## 먼저 읽을 것 — 이 순서로, 건너뛰지 말 것

직전에 두 번, 요약만 읽고 착수해서 전량 롤백했다. 1~2를 읽지 않고 시작하면 같은 일이 난다.

| # | 무엇 | 왜 |
|---|---|---|
| 1 | `~/.claude/plans/gentle-zooming-twilight.md` **전문** | 확정 결정표·§콜 2·§심볼릭 판단·검증 10항목이 여기에만 있다 |
| 2 | `.agents/AGENTS.md` 11개 + `AGENT_MISTAKES_REFLECTION.md`(레포 루트) | 하드코딩 금지·추측 금지·허위보고 금지 |
| 3 | 이 문서 | Phase 3의 작업 순서와 이미 있는 것/없는 것 |
| 4 | `docs/phase2_handoff.md` · `docs/article_selection_analysis.md` | L0가 무엇을 내는지. **주의: phase2_handoff 본문에는 뒤집힌 결론이 남아 있다**(갱신 주석 참조) |
| 5 | `docs/phase1_handoff.md` | 카드 코퍼스·요건 스켈레톤·게이트 설계. 콜 2가 여기 얹힌다 |

## 지금 상태 — Phase 3이 받는 것

L0가 닫혔다. **입력은 `data/eval/l0_candidates.jsonl`(61문항 전부)이고, 진입점은
`idpr.candidates.candidate_articles()`다.**

```
합집합 리콜        0.9272   전량회수 22/31   (모델 선정 0.727 + 검색 top-18 0.877)
계획서 검증 #5     스모크 체크 전항목 통과
콜 2 페이로드      카드 중위 668 최대 923 | 입력 중위 51.1k 최대 70.0k
                   +출력 30토큰/장 → 총 중위 71.1k 최대 97.7k
콜 2 대상 카드     1,436장 (context 261장 제외 후)
```

읽는 순서로 코드:

| 순서 | 파일 | 무엇을 알 수 있나 |
|---|---|---|
| 1 | `src/idpr/candidates.py` | L0 진입점 · 카드 무손실 불변식 · context 제외 조건 |
| 2 | `src/idpr/rulebase/scallop.py` | **새 룰베이스 런타임(이미 있다)** — 상태 렌더 · 실행 · 출력 파싱 |
| 3 | `data/rulebase/kcl_rulebase.scl` 8174행 이하 | 추론 규칙 12개와 `query` 선언 12개 |
| 4 | `src/idpr/neural/__init__.py` L376 `validate_fraud_assessment_bundle` | 콜 2 검증기의 원형. 일반화 대상 |
| 5 | `prompts/fraud_standard_assess.md` | 콜 2 프롬프트의 원형(86줄). 일반화 대상 |

## 이미 있는 것 / 없는 것 — 감사 결과

**있다(새로 만들지 말 것):**

- `rulebase/scallop.py` — `render_card_statuses()`(모델 출력이 프로그램 문법이 되지 않게
  호스트가 인용부호로 렌더), `run_program()`(1회 호출로 전 관계 출력, 선언 안 된 관계는
  raise), `parse_query_output()`(관계 부재와 빈 결과를 구분해서 raise).
- `data/rulebase/kcl_rulebase.scl` — 규칙과 `query` 12개가 이미 선언돼 있다:
  `element_supported` · `element_refuted` · `element_excluded` · `element_unaddressed` ·
  `offense_defeated` · `offense_established` · `offense_undetermined` · `is_absorbed` ·
  `final_offense` · `concurrent_offenses` · `attempt_to_consider` · `contradiction`.
- `neural/fact_graph.py:554 fact_tuples()` — 사실 그래프 → `(relation, args)` 행.
  `idpr.rulebase.facts.validate_fact`를 통과시킨다.
- Phase 1 골든 시나리오 44건 + 회귀 테스트.

**없다(Phase 3이 만든다):**

- **사실층 SCL 렌더러.** `fact_tuples()`의 행을 `rel person = {...}` 블록으로 찍는 함수.
  `render_card_statuses()`의 짝인데 아직 없다. 같은 파일에 같은 인용 규율로 넣을 것.
- **콜 2 스키마·검증기·프롬프트**(아래 작업 순서 3).
- **콜 2 러너와 sbatch.**

## 작업 순서

의존관계가 있는 것만 순서가 강제된다. 0번은 언제든 병렬로 진행한다.

### 0. 콜 2 프롬프트 승인 — **차단 요인이자 유일한 대기 항목**

`prompts/fraud_standard_assess.md`(86줄)를 일반화한다. 프롬프트 전문은 **사용자 승인 후에만**
설치한다. 원형과 달라지는 지점 셋:

- `rationale` 제거(계획서 line 75). 근거는 `basis_fact_ids`가 구조적으로 담고 산문은 콜 3이
  쓴다. 출력 토큰이 장당 ~80 → ~30으로 줄어야 일괄 처리가 성립한다.
- `authority_comment_ids` 제거. 카드 페이로드가 `id` + `proposition`뿐이라 모델에게 인용
  ID가 가지 않는다(계획서 확정 결정표).
- `confidence` 유지 여부는 열린 결정(아래 D2).

### 1. 사실층 SCL 렌더러 (선행 없음)

`rulebase/scallop.py`에 `render_fact_layer(case_id, rows)`를 추가한다. 인용·식별자 규율은
`render_card_statuses()`와 동일하게. **모델 문자열이 프로그램 문법이 되는 경로가 생기지
않게 하는 것이 이 함수의 존재 이유다**(아키텍처 A의 인젝션 경로가 그것이었다).
테스트: 라벨이 닫힌 어휘 밖이면 raise, 따옴표·역슬래시가 들어오면 raise.

### 2. 심볼릭 E2E를 콜 2 없이 먼저 관통 (1 필요)

골든 시나리오의 `card_status`를 넣어 `run_program`이 12개 관계를 전부 내는지 확인한다.
**콜 2 이전에 이걸 통과시켜 두면 나중에 이상한 결과가 나왔을 때 원인이 모델인지 룰베이스인지
가른다.** 여기서 막히면 콜 2를 만들지 말고 룰베이스를 먼저 고칠 것.

### 3. 콜 2 스키마 + 검증기 (선행 없음, 0과 병렬)

- **동적 JSON 스키마**: 후보 카드 전량을 필수 필드로 만든다(`build_fraud_irac_slot_schema`
  패턴 일반화). 카드 누락이 문법적으로 불가능해진다.
- **검증기**: `validate_fraud_assessment_bundle`을 일반화한다. **status↔evidence 결합 검증이
  과생성의 구조적 브레이크**다 — `satisfied`는 basis fact ≥1, `not_satisfied`는 counter
  fact ≥1, `unknown`은 `missing_facts` 필수. 엉뚱하게 끌려온 조문은 인용할 사실이 없어
  `unknown`으로 강제된다. 다만 후속 전체범위 E2E에서 `unknown` 조문도 Call 3 작성량을
  크게 늘리는 것이 확인되었으므로, 이것만으로 top-18의 잉여 조문을 감당할 수 있다는
  가정은 폐기했다. 현재는 Call 1.5를 정밀도 경로, 검색을 재현율 경로로 분리한다.
- `polarity` 반전은 **호스트가 결정론적으로** 한다(계획서 line 79).

### 4. 콜 2 러너 + sbatch (0·1·3 필요)

- **스모크 케이스 1문항을 먼저 관통시킨다.** 61문항을 돌리기 전에.
- **조문 경계 2분할 + `--max-model-len 65,536`.** 근거는 실측이다: 총량 최대 97.7k이므로
  단일콜은 131,072가 필요하고, 2분할이면 콜당 최대 ~49k다. 단일콜은 출력 20k에 필수 필드
  700개짜리 유도 디코딩이 되어 계획서가 별도 리스크로 적은 "일괄 판정 품질 희석"과 같은
  지점이다. **분할은 반드시 조문 경계에서** — 조문 내 카드가 일부만 들어오면 게이트는
  **성립하는 쪽으로 실패한다**(안 본 카드는 아무것도 반증하지 못한다).
- 65,536이 GPU 1장에 실제로 올라가는지는 이 단계에서 한 번 확인한다. 계획서가 Phase 3
  최우선으로 지목한 항목이며, 상향 폭만 실측으로 줄었을 뿐 확인 자체는 남아 있다.

### 5. 게이트 강도 스윕 (4 필요)

`offense_supported = 요건 카드 하나라도 satisfied`는 약하다. 후보 21조문이 들어오고 콜 2가
관대하면 `established`가 무더기로 나온다. **`element_supported`/`refuted`/`unaddressed`가
전부 `query`로 나오므로 재컴파일 없이 호스트에서 스윕할 수 있다.** 첫 실행 결과가 나온
직후에 열 것 — `card_status` 실측 없이는 판단이 불가능하다.

### 6. 61문항 전량 + 산출물 (5 필요)

`data/eval/card_status.jsonl` + `data/eval/symbolic_results.jsonl`. 콜 수·토큰을 기록한다
(계획서 검증 #10, `vllm_client.complete_text`가 `usage`를 버리는 문제 포함).

## 사용자 결정 대기

| # | 무엇 | 추천 | 안 정하면 |
|---|---|---|---|
| **D1** | 콜 2 프롬프트 전문 | 위 0번 초안 | **차단됨** |
| **D2** | `confidence` 필드를 유지할까 | **제거.** 심볼릭 레이어가 읽지 않고 장당 출력 토큰만 늘린다. 유지하면 판정 신뢰도 분석은 가능 | 제거하고 진행 |
| **D3** | `stage`·`concurrence`·`participation` 카드 254장 | **규칙을 마저 쓴다.** 지금 콜 2가 판정하지만 어떤 규칙도 읽지 않는다. 빼면 루브릭 죄수 항목 140개(12%)와 미수 논점을 포기 | 판정은 하되 안 읽히는 상태 유지 |
| **D4** | 죄명 계열 확장(제297조 → 제298·299·301조) | Phase 3 이후. **계열의 경계가 법적 판단이라 검수 필요** | 안 함(합집합이 이미 0.927) |
| D5 | `data/rulebase/doctrine_review.md` D1~D3 (Phase 1 이월) | 셋 다 현상 유지 | 현상 유지 |

## 검증 — 계획서 10항목 대비 Phase 3 몫

| # | 항목 | 상태 |
|---|---|---|
| 2 | Scallop 골든 재통과 | Phase 1에서 44건 통과. 새 상태 렌더러로 재확인 |
| **4** | **콜 2 프롬프트에 `source_refs`/`quote`/`comment_id`가 등장하지 않음** | **테스트로 강제할 것.** `Card.model_payload()`가 이미 그것만 내지만 프롬프트·러너 경로에서 재확인 |
| 7 | 입력 화이트리스트 | `assert_no_leaked_fields`를 콜 2 페이로드에도 걸 것 |
| 9 | 채점 | Phase 5 |
| **10** | **콜/토큰 회계** | 콜 1·1.5·2를 각각 기록. 베이스라인 1콜과 병기해 공개 |

## 리스크

- **일괄 판정 품질 희석.** 668장 한 콜의 장당 판정이 조문별 분할 대비 열화되는지 스모크
  케이스로 A/B 확인. 계획서가 명시한 리스크다.
- **게이트가 관대한 쪽으로 실패한다.** 침묵은 절대 막지 않는다. 그래서 조문 무손실이
  장식이 아니라 하중 부재이고, 분할을 조문 경계에서만 해야 한다.
- **GPU 1장에 26B와 31B 동시 적재 불가** — 생성 잡과 채점 잡은 순차 sbatch로 분리.

## 잊지 말 것

- **승인 계획서 전문을 먼저 읽는다.** 이 문서는 착수 순서이지 설계서가 아니다.
- 긴 잡·GPU 잡은 예외 없이 `sbatch`. 진행상황을 백그라운드에서 반복 확인하지 말 것.
  자원값은 `run_l0_union.sh`를 그대로 복사한다 — `JE_ARROW_MALLOC_CONF`를 빼먹으면 vLLM이
  로그 0바이트로 세그폴트한다.
- `HF_HUB_OFFLINE`은 vLLM 단계에만. 검색 모델 단계에서는 **설정하지 않는다**.
- 프롬프트 전문은 **사용자 승인 후에만** 설치한다.
- 모델 입력 화이트리스트는 `question_text` + `question_prompt`뿐. 카드는 `id` +
  `proposition`만.
- `supporting_precedents`(gold 판례 277개)를 검색 코퍼스로 쓰지 말 것.
- 하드코딩 금지 — 조문·죄명·검증 목록은 전부 `data/` 자산으로.
- 파이썬은 `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기다.
- API 총예산 $100. Phase 0~2는 **$0**을 썼다(전부 로컬 GPU와 결정론적 컴파일).
