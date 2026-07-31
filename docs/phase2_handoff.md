# Phase 2 인수 문서 — L0 검색 + 콜 1, Phase 3 착수 지점

2026-08-01. 승인된 계획은 `~/.claude/plans/gentle-zooming-twilight.md`. **요약만 읽고 착수하지
말 것** — 직전 세션이 그렇게 해서 Phase 2를 두 번 전량 롤백했다.
데드라인 2026-08-11 (NLLP 워크샵).

## 먼저 읽을 것 — 이 순서로

이 문서만 읽고 착수하면 직전 세션과 같은 실수를 한다. 착수 전 1~3은 건너뛰지 말 것.

| # | 무엇 | 왜 |
|---|---|---|
| 1 | `~/.claude/plans/gentle-zooming-twilight.md` **전문** (34KB) | 확정 결정표(3콜·2층 술어·카드 페이로드), §검색, 공정성 8항목, 검증 10항목이 여기만 있다. 요약본에는 없다 |
| 2 | `.agents/AGENTS.md` 11개 규칙 + `AGENT_MISTAKES_REFLECTION.md` | 하드코딩 금지·추측 금지·허위보고 금지. 반복 위반 이력이 적혀 있다 |
| 3 | 이 문서 | Phase 2가 계획에서 벗어난 5가지와 그 실측 근거 |
| 4 | `docs/phase1_handoff.md` | 카드 코퍼스·요건 스켈레톤·심볼릭 게이트가 어떻게 생겼는지. 콜 2는 여기 위에 얹힌다 |

코드는 이 순서로 읽으면 위에서 아래로 이어진다:

| 순서 | 파일 | 무엇을 알 수 있나 |
|---|---|---|
| 1 | `src/idpr/rulebase/facts.py` | 사실층 13술어와 **닫힌 서술 어휘**. 왜 `폭행`이 아니라 `유형력행사`인지가 여기 적혀 있다 |
| 2 | `src/idpr/neural/fact_graph.py` | 콜 1 계약 전체 — 스키마 생성, 항목 단위 채택, 사실→튜플, 질의 도출 |
| 3 | `src/idpr/retrieval/__init__.py` | 검색 3신호·RRF·**조문 무손실 불변식**(하중 부재다) |
| 4 | `src/idpr/eval/issue_recall.py` | 루브릭 골드가 어떻게 만들어지는지, 버킷이 왜 필요한지 |
| 5 | `src/idpr/rulebase/compile_scl.py` 도입부 + `data/rulebase/kcl_rulebase.scl` 8174행 이하 | 심볼릭 게이트. Phase 3에서 열어야 할 지점 |

실측을 다시 볼 때 쓰는 자산:

| 파일 | 쓸 곳 |
|---|---|
| `data/eval/retrieval_l0_recall_report.json` | **문항별 후보·골드가 다 들어 있다.** 미스 원인은 GPU 없이 여기서 읽는다 |
| `data/eval/fact_graphs.jsonl` | 콜 1 산출 + `admission.dropped` + 거부된 원본 payload |
| `data/eval/rubric_crime_article_map.json` | 죄명→조문 골드, `coverage_gap` 절에 커버리지 갭 |
| `docs/rubric_crime_article_review.md` | 검수자 주석 보유. **덮어쓰지 말 것**(빌더가 거부하지만 `--rewrite`가 있다) |

**믿지 말 것**: `issue_tags` 기반 수치 전부(직전 세션의 0.758@18, 채점가능 23문항),
`docs/research/idpr_remaining_work.md`의 완료 여부 서술(코드 감사가 우선).

## 지금 상태

브랜치 `rulegen-campaign-pilot`. 테스트 **392 passed** (Phase 1 356 + 신규 36). 워킹트리에
Phase 2 산출물이 커밋 대기 중이다.

Phase 2 = 계획서 단계표의 `src/idpr/retrieval/` + 콜 1(사실+쟁점). 둘 다 동작하고 61문항
실측이 끝났다.

## 이 Phase에서 골드가 바뀌었다 — 먼저 읽을 것

계획서는 쟁점 리콜의 gold를 `issue_tags`로 정했다. **그 전제가 거짓이다.**

- KCL parquet 컬럼은 `meta / question / rubrics / score / supporting_precedents` 다섯 개뿐.
  `issue_tags` 컬럼은 **없다.**
- 태그는 `scripts/build_kcl_criminal_inventory.py`의 `CURATED_TAGS`에 **이전 에이전트가 손으로
  써넣은 것**이다(문항당 4~5개). `legal_area`도 같은 딕셔너리에서 나온다.

그래서 골드를 **루브릭**으로 바꿨다. `rubrics`는 parquet 원본이고 `rubric_score`의 채점 기준
자체이며, 항목이 죄명을 그대로 말한다("특수절도죄 성부를 논하고 있는지"). 죄명 → 조문 번역만
하면 되고 그건 법률 사실 조회다.

- 자산: `data/eval/rubric_crime_article_map.json` (`status: reviewed`)
- 검수 문서: `docs/rubric_crime_article_review.md` — 죄명 124종 중 36종을 사용자가 답했고,
  71종은 무응답 승인, 17종은 죄명 아님으로 제외. 미수 준용조문 포함도 확정.
- **채점 가능 31문항** / 죄명을 아예 안 부르는 절차 문항 30 / 코퍼스 밖만 부르는 문항 0.

교차검증: 스모크 케이스의 루브릭 골드가 `art297·298·300·301·319`로 나오는데, 이는 계획서
검증 #5가 **손으로 지목한 4항목**(간접정범·위요지·중지미수·결합범)과 독립적으로 일치한다.

`data/eval/issue_tag_article_map.json`과 그 빌더는 폐기했다. 태그 기반 수치(직전 세션의
0.758@18, 채점가능 23문항)는 **인용하지 말 것.**

## 실측 (잡 217519, top-18 기준)

채점 가능 31문항, 검색 = dense(embeddinggemma-300m) + 문자 bigram BM25 + rerank
(bge-reranker-v2-m3), RRF k=60, 쿼리 간 max 융합.

| top_k | 검색 | 콜1 제안 | 합집합 | 준용조문 제외 |
|---:|---:|---:|---:|---:|
| 12 | 0.593 | 0.000 | 0.593 | 0.616 |
| **18** | **0.814** | 0.000 | **0.814** | **0.863** |
| 24 | 0.848 | 0.000 | 0.848 | 0.901 |

전량 회수 17/31. 스모크 케이스는 코퍼스 내 4개 항목 **전부 회수**(art298·art319·art300 +
결합범 art319·297·301), art254는 놓침, 체포죄(art276)는 코퍼스 밖으로 분류.

미회수 상위: `art254`(4), `art342`(4) — 둘 다 미수 준용조문. 그 다음 `art136`·`art257`·
`art329`·`art331`(각 2).

### 콜 1의 제안 경로는 0이다 — 그리고 그게 좋은 소식이다

쟁점 후보 258개 중 `article`이 채워진 건 36개뿐이고 **코퍼스 조문으로 매칭되는 건 0개**다
(나머지는 특별법이거나 쉼표 한 글자짜리 쓰레기). 모델은 쟁점 이름은 대지만 조문 번호는 못
댄다 — 프롬프트가 "아는 경우에만, 지어내지 말라"고 했고 실제로 안 지어냈다.

**따라서 합집합 = 검색이고, 조문을 찾는 일은 전부 검색이 한다.** "모델 제안이 리콜을 다
가져가서 검색이 무의미해진다"는 우려는 실측상 발생하지 않았다. 콜 1이 기여하는 지점은
조문이 아니라 **질의**다.

## 계획에서 벗어난 것

### 1. 골드가 `issue_tags`가 아니라 루브릭이다
위 절 참조. 계획서 검증 #5의 전제가 데이터와 다르다.

### 2. 콜 1의 계약은 모델이 식별자를 만들지 않는 형태다
첫 구현은 평면 구조였고 위성 사실이 부모 행위를 문자열 `actId`로 참조했다. 61문항 실측에서
**52건 실패** — dangling act 참조 48, 중복 fact_id 180. 유도 디코딩은 값을 강제할 수 있어도
상호참조를 강제하지 못한다. 그래서 위성을 `act` 안에 넣고 호스트가 `act_001…`을 발급하며,
순서·인과는 스키마가 범위를 강제하는 **배열 인덱스**로만 참조한다.

### 3. 거부는 페이로드가 아니라 항목 단위다 (계획서는 "호스트가 raise로 강제")
근거 없는 사실은 여전히 심볼릭 레이어에 못 들어간다. 바뀐 것은 **그것 하나 때문에 나머지를
같이 버리지 않는다**는 것뿐이다. 문항당 인용 대상 항목이 30개 안팎인데 항목 정확도 ~95%가
문항 성공률 7%로 바뀌던 것이 이 설계의 결과였다.

드롭은 절대 조용하지 않다 — `admission.dropped`에 집계되어 산출물에 실린다. 다른 사건이거나
행위의 절반 이상이 근거 없으면 페이로드 전체를 거부한다(`MIN_ADMITTED_ACT_FRACTION`).

실측 채택률: **61/61 문항 채택**, 드롭 183건(문항당 3개, 항목 채택률 ~90%).
내역 — `act_ordering` 83 · `issue_candidates` 44 · `acts` 24 · `roles` 20 · `causation` 5 ·
`results` 4 · `relations` 3.

### 4. 인용 대조는 공백만 정규화한다
실측 114건의 인용 실패 중 **23건이 공백 차이뿐**이었다("간음하려 하였으나" ↔
"간음하려하였으나"). 원문 띄어쓰기가 불규칙해서 생기는 것이고 의미를 담지 않는다. 글자가
바뀐 것(25건, "A를"→"A가")은 그대로 실패한다 — 그게 게이트가 일하는 것이다.

### 5. 질의는 모델 문장만이 아니라 사실층에서도 나온다
계획서 §검색은 fact graph를 쿼리 소스로 지정하는데(`m3_factgraph_rag` 패턴) 첫 구현은 모델이
쓴 `retrieval_queries`만 썼다. 스모크 케이스에서 **행위 8개짜리 사건에 질의가 5개**였고 그중
2개를 소문항 밖 단락(뇌물)에 써서 주거침입 에피소드에는 질의가 하나도 없었다 — 사실층에는
`출입 @ 공동주택공용부`가 기록돼 있는데도 art319를 놓쳤다.

그래서 `fact_derived_queries()`가 **행위·결과·보유·관계마다 질의를 하나씩** 만든다. 질의
개수가 모델의 예산이 아니라 사건의 사건 수를 따른다. 라벨·조문별 분기는 없다.

**대가가 있고 숨기지 않는다.** 이 변경으로 스모크의 art319는 회수됐고 전량회수는 16→17이
됐지만, **총계 리콜은 전 구간에서 내려갔다**:

| top_k | 모델 질의만 (217473) | +사실 유래 (217519) |
|---:|---:|---:|
| 12 | 0.712 | 0.593 |
| 18 | 0.821 | 0.814 |
| 24 | 0.868 | 0.848 |

질의가 5개 → 25개로 늘면서 누락 에피소드는 덮였지만 소문항 밖 조문도 함께 끌려온다. top-18
차이 0.007은 n=31에서 노이즈, top-12의 0.119는 실질이다. **유지한 이유는 점수가 아니라
계획서가 지정한 설계이기 때문이다.** 뒤집으려면 점수가 아닌 근거로 뒤집을 것.

## 산출물

| 파일 | 내용 |
|---|---|
| `prompts/fact_graph_extract{,_user}.md` | 콜 1 프롬프트 (사용자 승인본, v2) |
| `src/idpr/prompts.py` | 프롬프트 레지스트리 |
| `src/idpr/neural/fact_graph.py` | 콜 1 스키마(사실층 레지스트리에서 생성) · 항목 단위 채택 · 사실→튜플 · 질의 도출 |
| `src/idpr/retrieval/__init__.py` | 다중쿼리 RRF + BM25/dense/CE, **조문 무손실 불변식** |
| `src/idpr/retrieval/models.py` | embeddinggemma-300m + bge-reranker-v2-m3 래퍼 |
| `src/idpr/eval/issue_recall.py` | 루브릭 골드, 버킷, 경로 3분해 |
| `data/eval/rubric_crime_article_map.json` | 죄명→조문 (검수 완료) |
| `data/eval/smoke_checks.json` | 계획서 검증 #5 체크리스트 |
| `data/eval/fact_graphs.jsonl` | 61문항 콜 1 산출 + 채택 내역 + 거부 payload |
| `data/eval/retrieval_l0_recall_report.json` | 리콜 3경로 · 문항별 후보 · 미회수 조문 |
| `docs/rubric_crime_article_review.md` | 검수 완료 문서 (**주석 보유, 덮어쓰지 말 것**) |

재현:
```
sbatch scripts/slurm/run_retrieval_l0.sh                       # 콜 1 + 검색
SKIP_CALL1=1 sbatch --export=ALL,SKIP_CALL1=1 ...              # 검색만 (기존 콜1 재사용)
PYTHONPATH=src python scripts/readmit_fact_graphs.py           # 채택 로직만 바뀐 경우
```
파이썬은 `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기다.

## Phase 3 착수 지점

계획서 Phase 3 = **콜 2(카드 일괄 판정) + Scallop 판단**. 최우선은 계획서가 지목한
`--max-model-len` 32,768 → 131,072 상향이 GPU 1장에서 실제로 되는지다. 3콜 설계의 전제이고,
안 되면 카드셋을 좁히거나 조문군 2~3개로 분할 후퇴한다.

콜 2 입력은 `retrieve_candidate_articles(...).cards` 전량이고, 페이로드는 `id` +
`proposition`만이다(`Card.model_payload()`가 이미 그것만 낸다). 인용문·`comment_id`를 넣으면
검수를 되돌리는 셈이고, 계획서 검증 #4가 그것을 테스트로 강제하라고 한다.

### 심볼릭 게이트를 열어둔 채로 넘긴다

`offense_supported = 요건 카드 하나라도 satisfied`는 약하다. 후보 18조문이 들어오고 콜 2가
관대하면 `established`가 무더기로 나올 수 있다. 브레이크는 계획서 line 78의 status↔evidence
결합 검증(satisfied는 basis fact ≥1)인데, **작동 여부는 `card_status` 실측이 있어야 판단
가능하다.** 게이트 강도는 `element_supported`/`refuted`/`unaddressed`가 전부 `query`로
나오므로 **재컴파일 없이 호스트에서 스윕**할 수 있다. Phase 3 첫 실행에서 열 것.

부분 회수의 위험도 같이 본다 — 조문 안에서 카드가 일부만 들어오면 게이트는 **성립하는 쪽으로
실패한다**(침묵은 절대 막지 않는다). 그래서 "조문 단위로만 절단, 조문 내 카드 무손실"이
장식이 아니라 하중 부재다. 콜 2를 조문군으로 분할해야 한다면 **반드시 조문 경계에서** 쪼갤 것.

## 남은 빚 (우선순위 순)

1. **`art254`·`art342` 미수 준용조문은 검색으로 회수 불가.** 조문 텍스트가 사실관계와 겹칠
   어휘가 원리적으로 0이다. 정공법은 조문의 준용 관계를 결정론적으로 확장하는 것(기본조문이
   뽑히면 그 죄의 미수 조문을 딸려오게). 조문 텍스트에서 나오므로 정답 역산이 아니다.
   **미회수의 절반이 이것이다.**
2. **루브릭이 부르는데 카드가 없는 형법각칙 12조문** — `idpr_remaining_work.md` L5. 301
   chunks ≈ $15.1, 원인은 역시 손으로 쓴 `issue_tags`. Phase 2 리콜을 51조문 기준으로 확정한
   뒤 독립 항목으로, 예산 게이트를 거쳐 실행.
3. **소문항 스코핑.** `question_text`가 3단락인데 소문항은 "사실관계 (1)"만 묻는 경우가 있다.
   콜 1은 원문 전체에서 사실을 기록하도록 승인받았고 그건 맞지만, 검색이 소문항 밖 단락의
   조문까지 후보에 올려 낮은 top_k에서 자리를 잡아먹는다. 5번 이탈 사항의 대가가 여기서 온다.
4. `paper/03_methodology.md`, `docs/KCL_1730_RULEBASE_SPECIFICATION.md`가 폐기된 아키텍처 A를
   서술한다(Phase 1에서 이월).
5. `src/idpr/rulebase/doctrine.py`의 `OFFENSE_NAMES`(조문 51개 표제)가 코드 안에 있다. 표시
   전용이고 완전성 테스트가 붙어 있어 추론에는 안 닿지만, "조문 리터럴은 `data/` 자산으로"
   기준에는 어긋난다. Phase 1 자산이라 이번에 건드리지 않았다.

## 잊지 말 것

- **승인 계획서 전문을 먼저 읽는다.** 이 문서는 요약이다.
- 긴 잡·GPU 잡은 예외 없이 `sbatch`. 진행상황을 백그라운드에서 반복 확인하지 말 것.
  자원값은 `run_fraud_neural_e2e.sh`를 그대로 복사한다 — `JE_ARROW_MALLOC_CONF`를 빼먹으면
  vLLM이 로그 0바이트로 세그폴트한다(이번에 겪음).
- `HF_HUB_OFFLINE`은 vLLM 단계에만. 검색 모델 단계에서는 **설정하지 않는다**
  (`transformers==4.57.3`이 오프라인에서도 `model_info()`를 호출해 죽는다).
- 프롬프트 전문은 **사용자 승인 후에만** 설치한다.
- 모델 입력 화이트리스트는 `question_text` + `question_prompt`뿐. `assert_no_leaked_fields`가
  게이트다.
- `supporting_precedents`(gold 판례 277개)를 검색 코퍼스로 쓰지 말 것.
- 코드베이스에 하드코딩 금지 — 조문·죄명·검증 목록은 전부 `data/` 자산으로.
- API 총예산 $100. Phase 2는 **$0**을 썼다(로컬 GPU만).
