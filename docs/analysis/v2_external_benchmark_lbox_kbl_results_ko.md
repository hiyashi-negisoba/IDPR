# LBOX / KBL 외부 벤치마크 결과

브랜치 `agent/external-benchmark-takeover`. 생성 백본 `idpr-gemma-4-26b-a4b`
(local vLLM, snapshot `.../models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75`).
**최종본 (2026-08-22 확정).** baseline 7종 전부 완료됐고 아래 표는 최종값이다
(`experiments/external/runs/baselines/*/scores/`). 8/17에 living draft로 멈춰 있던
"진행 중" 칸을 채운 것 외에 방법론·수치 해석은 바꾸지 않았다.

## 1. 목적과 설계

KCL-26 judge가 전체 파이프라인의 최종 답안 품질(E2E 롱폼)을 재는 것과 달리, 이 두 외부
벤치마크는 컴포넌트 단위 능력을 잰다:

- **LBOX Call 1** (`lbox/lbox_open`, `statute_classification_plus`) — production Call 1
  라우터를 그대로 통과시켜, 사실관계에서 **쟁점(죄명) 추출** 능력만 분리해서 본다.
- **KBL Call 2** (`lbox/kbl`, `reasoning/kbl_causal_reasoning_qa_v0.1.json`) — production
  `legal_element.result_causation` predicate 평가를 그대로 통과시켜, **주어진 쟁점에 대한
  법적 평가** 능력만 분리해서 본다.

두 경로 모두 production routing/binding/grounding/prompt/legal definition semantics를
전혀 수정하지 않고 그대로 재사용한다 (`src/idpr/v2/benchmarks/external.py`,
`external_data.py`, `scripts/{prepare,run,evaluate}_v2_external_benchmark*.py` — 이번
세션에서 정본 검증만 하고 코드는 freeze).

## 2. Baseline 비교 방법론

7개 비교 baseline(`src/idpr/baselines/*`)은 전부 `client.complete_text`만 쓰는 자유서술
essay 생성기라, production Call1/Call2가 요구하는 닫힌 구조 출력(JSON seed 목록, TRUE/FALSE
label)을 직접 낼 수 없다. 두 가지 선택지 중:

- (a) baseline에게 새 closed-schema 프롬프트를 준다 → 그 baseline만의 메커니즘(ACAL 논증,
  RAG 검색, FOL 정리증명 등)이 발동하지 않고 "백본이 JSON을 얼마나 잘 따르는가"만 재게 됨
- (b) **공식 repo 코드(`run_case()`) 완전 무수정**으로 자유서술 답을 받고, 별도
  결정론적 매칭으로 채점

KCL 때와 동일하게 (b)를 택했다. 신규 코드는 다음 세 개뿐이고, production 스코어러
(`evaluate_call1`/`evaluate_call2`)와 baseline 클래스는 전혀 건드리지 않는다:

- `scripts/build_v2_external_baseline_dataset.py` — 무수정 `model_inputs.jsonl`(gold 없음)을
  `run_baselines_experiment.py`가 쓰는 `sub_question_id/question_text/question_prompt` 스키마로
  변환만 함
- `scripts/run_baselines_experiment.py` — **완전 무수정**, 공식 CLI 그대로 호출
- `scripts/score_v2_external_benchmark_baseline.py` (신규) — 결정론적 키워드 매칭
  - LBOX: catalog 69개 죄명 canonical display_name이 답변 텍스트에 substring으로
    등장하면 "언급"으로 카운트
  - KBL: 고정 결론 문구(`결론: 인과관계 인정`/`결론: 인과관계 부정`)를 baseline에게
    명시적으로 요구하는 프롬프트를 준 뒤, 못 찾으면 긍정/부정 키워드 정규식 폴백
    (부정 패턴을 먼저 검사 — "인정되지 않는다"가 "인정" 부분문자열을 포함하기 때문)

로컬 단위 테스트(8개 KBL 케이스, LBOX 1케이스)로 매칭 로직 자체는 검증했다.

## 3. N — 왜 방법마다 다른가

| 조건 | LBOX N | KBL N | 사유 |
|---|---:|---:|---|
| ours (production) | 3375 | 93 | 정본, 전체 |
| ours 300-subset | 300 | — | baseline과의 매칭 비교용, 아래 참조 |
| baseline 7종 전체(vanilla_zero_shot/chain_of_thought/acal/leprec/legal_chain_reasoner/fol_autoformalizer_solver/standard_rag) | 300 | 93 | `max_num_seqs=1` 순차 처리에서 baseline 자유서술 생성이 production 구조화 출력보다 훨씬 느려(§5) LBOX 3375 전부 돌리면 wall time이 과도해짐. vanilla/CoT는 최초 job(225195)이 이미 361건까지 진행됐었으나, 남은 vanilla ~5시간 + CoT 3375건 ~7.5시간이 더 드는 것이 낭비라 취소하고 나머지와 동일하게 300-subset으로 재제출(job 225242) |

LBOX 300-subset은 전체 materialization의 **처음 300행**(`lbox:test:15720` ~
`lbox:test:17579`, test split 앞부분) — `experiments/external/runs/full/materialized_lbox300/`.
gold/model_inputs id 순서가 원본과 완전히 일치함을 확인했고, ours의 300-subset 점수는
**기존 3375-case 예측을 그대로 슬라이스**해 production 스코어러로 재채점한 것이라(재실행
아님) production 답변 자체는 손대지 않았다.

## 4. 결과

### 4.1 LBOX Call 1

ours의 "raw"(닫힌 seed 집합, closure 컴파일 이전)와 baseline의 "언급"(mentioned, catalog
이름이 텍스트에 등장)은 둘 다 "gold 죄명이 그 방법의 1차 예측 집합에 들어있는가"라는 같은
질문이라 recall/case full-hit/precision/F1 네 열을 그대로 통일해서 한 표로 비교한다.
ours만 갖는 closure(정적 컴파일로 후보를 넓힌 뒤의 집합, 이 데이터셋에선 0건 recovery라
recall/full-hit은 raw와 동일하고 precision만 떨어짐 — §4.1 하단 참조)는 baseline에
대응 개념이 없어 별도로만 표기한다.

| method | N | recall(=survival/mention) | case full-hit | precision | F1 |
|---|---:|---:|---:|---:|---:|
| **ours (production, 전체, raw)** | 3375 | 0.952 | 0.943 | 0.456 | 0.617 |
| **ours (production, 300-subset, raw)** | 300 | 0.994 | 0.993 | 0.431 | 0.601 |
| vanilla_zero_shot | 300 | 0.962 | 0.957 | 0.638 | 0.767 |
| chain_of_thought | 300 | 0.968 | 0.963 | 0.648 | 0.776 |
| acal | 300 | 0.956 | 0.950 | 0.399 | 0.563 |
| leprec | 300 | 0.971 | 0.967 | **0.743** | **0.842** |
| legal_chain_reasoner | 300 | 0.977 | 0.973 | 0.655 | 0.784 |
| fol_autoformalizer_solver | 300 | 0.898 | 0.900 | 0.762 | 0.824 |
| standard_rag | 300 | 0.971 | 0.967 | 0.423 | 0.590 |

**읽는 법.** recall은 ours가 1위(300-subset 0.994, 전체 0.952)이고 precision은 하위권이다.
넓게 열고 하류(Call 1.5/Call 2)가 거르는 설계가 그대로 나온 것이라 이 축만으로 우열을
말할 수 없다 — 다만 **fol_autoformalizer_solver만 recall이 0.898로 뚜렷이 낮다**(유일하게
0.95 미만). 형식화 단계가 죄명 후보를 좁힌다는 뜻이고, 우리와 가장 가까운 계열의 baseline
에서 반대 방향의 실패가 난 지점이라 기록해 둔다.

**closure(참고, baseline 대응 없음):** 전체 closure recall/full-hit = raw와 동일(0.952/0.943,
closure_recoveries 0건), closure precision/F1 = 0.194/0.322 (raw 0.456/0.617보다 낮음 — 정적
컴파일이 후보를 넓히며 정밀도를 희생). 300-subset도 동일 패턴(closure recall/full-hit
0.994/0.993, precision/F1 0.185/0.312).

### 4.2 KBL Call 2

baseline은 전부 unknown_rate 0.0이라(§4.2 하단) `accuracy`/`macro-F1` 자체가 이미 "답한
것만으로 잰" 수치다. ours는 UNKNOWN을 정직하게 반환하므로 전체-93 기준(UNKNOWN을 오답
취급)과, UNKNOWN을 제외하고 답한 61건만으로 잰 기준을 별도 행으로 둔다 — 후자가 baseline과
비교 가능한 값이다. UNKNOWN 제외 macro-F1은 production 스코어러가 출력하는 `cases`
배열(id/gold/prediction)에서 `prediction != UNKNOWN`인 61건만 추려 다시 계산한 것으로,
`evaluate_call2` 자체는 건드리지 않았다.

| method | N | accuracy | macro-F1 (TRUE/FALSE) | coverage | unknown rate |
|---|---:|---:|---:|---:|---:|
| **ours (production, 전체 93건, UNKNOWN=오답)** | 93 | 0.581 | 0.489 | 0.656 | 0.344 |
| **ours (production, UNKNOWN 제외 61건만)** | 61 | 0.885 | 0.650 | 1.0 | 0.0 |
| vanilla_zero_shot | 93 | 0.860 | **0.844** | 1.0 | 0.0 |
| chain_of_thought | 93 | 0.828 | 0.803 | 1.0 | 0.0 |
| acal | 93 | 0.817 | 0.796 | 1.0 | 0.0 |
| leprec | 93 | 0.849 | 0.833 | 1.0 | 0.0 |
| legal_chain_reasoner | 93 | 0.849 | 0.833 | 1.0 | 0.0 |
| fol_autoformalizer_solver | 93 | 0.839 | 0.823 | 1.0 | 0.0 |
| standard_rag | 93 | 0.860 | 0.844 | 1.0 | 0.0 |

### 4.3 이 벤치마크의 실제 발견 — UNKNOWN은 부정 사례에 몰려 있다

ours의 per-class 성적이 위 표보다 중요하다.

```
TRUE  (gold n=65): precision 0.912  recall 0.800  f1 0.852
FALSE (gold n=28): precision 0.500  recall 0.071  f1 0.125
confusion:  TRUE  -> TRUE 52 / FALSE  2 / UNKNOWN 11
            FALSE -> TRUE  5 / FALSE  2 / UNKNOWN 21
```

**UNKNOWN 32건 중 21건이 gold FALSE다.** 기권이 균등하게 흩어진 것이 아니라 부정 사례에
집중돼 있다. 즉 우리 grounding은 "인과관계가 인정된다"는 확인은 하지만 **"인정되지
않는다"는 확인을 못 한다** — 근거 부족(epistemic)과 사실의 부존재(ontic)를 같은 값으로
접어 버린다. 전체-93 accuracy 0.581과 baseline 0.82~0.86의 격차는 대부분 이 한 축에서
나온다.

미완의 `prompts/v2_call2_grounding_binary*.md`(candidates, 미승인)와 `wip/kbl-binary-grounding`
브랜치가 이 문제를 겨냥한 것이다. 다만 "UNKNOWN을 없애고 FALSE로 강제한다"는 **판단 보류를
버리는 것**이므로, 폐쇄세계 부정을 제대로 다루는 설계와는 구분해야 한다.

baseline의 unknown_rate 0.0은 실제 확신이 아니라 "고정 결론 문구를 강제한 프롬프트를
잘 따랐다"는 것뿐이다 — production의 UNKNOWN은 근거 부족을 스스로 판단해 반환하는 정직한
답이고, baseline은 애초에 abstain(판단 보류) 옵션 자체가 없다. 그래서 위 "UNKNOWN 제외
61건" 행은 ours가 답을 낸 부분집합만의 실력이지, ours가 baseline만큼 확신을 갖고 답한다는
뜻은 아니다.

## 5. 레이턴시

production Call1/Call2는 닫힌 구조 출력(짧은 JSON)이고, baseline은 최대 4096토큰
자유서술 essay라 속도 차이가 크다. 같은 job(`max_num_seqs=1`, `idpr-gemma-4-26b-a4b`
동일 백본) 안에서 측정한 case당 평균 생성 시간:

| method | 초/case | 근거 |
|---|---:|---|
| **ours (production Call1+Call2)** | **~0.36** | job 225092 구간 측정(1637→3468건 사이 marginal rate) |
| vanilla_zero_shot | ~5.8 | 취소된 job 225195 실측(250건 평균). 225242는 두 방식이 한 job이라 분리 불가 |
| chain_of_thought | ~8.0 | smoke job 225159 실측(LBOX 5건). 225242 전체 평균은 두 방식 합산 786건 기준 ~6.8 |
| leprec | 7.85 | job 225238 실측(393건, LBOX 300+KBL 93 전체 평균) |
| acal | 8.51 | job 225237 실측(393건, 전체 평균) |
| legal_chain_reasoner | 8.82 | job 225239 실측(393건, 전체 평균) |
| fol_autoformalizer_solver | ~8.8 | job 225240 elapsed 60:14에서 서비스 기동분 차감, 393건 기준 추정 |
| standard_rag | ~5.1 | job 225241 elapsed 35:52에서 서비스 기동분 차감, 393건 기준 추정 |

fol/rag 두 값은 실측 로그가 아니라 **job elapsed에서 서비스 기동시간(~2.5분)을 뺀 추정**
이다(같은 방식으로 계산한 leprec 추정이 실측 7.85와 일치함을 확인했다).

**production 구조화 출력이 자유서술 baseline보다 약 15~40배 빠르다.** 이건 이번 벤치마크의
부차 소득이지 목적은 아니었지만, LBOX 300-subset 절단 판단(§3)의 직접적 근거이기도 하다.

## 6. 알려진 한계

- **결정론적 키워드 매칭은 LLM judge가 아니다.** KBL의 긍정/부정 키워드 폴백은 자연어
  뉘앙스(이중부정, 조건부 서술)에서 오분류 가능성이 있다 — 사용자 승인 하에 API 비용 없는
  이 방식을 선택했고(§2), 정확도보다 "baseline이 뭘 말하는지"의 기계적 근사임을 명시한다.
- baseline 7종은 모두 LBOX N=300으로 맞췄지만, **ours(production)는 300-subset과 전체
  3375 두 버전이 공존**한다(§4.1) — baseline과 직접 비교할 땐 300-subset 행을 쓸 것.
- production Call1/Call2는 LBOX/KBL 전용 튜닝이 전혀 없다 — 두 벤치마크 모두 저작
  당시 존재하지 않았던 외부 데이터셋이라, 여기 수치는 순수 일반화 능력이다.

## 7. 아티팩트

```
experiments/external/runs/full/materialized/{lbox_call1,kbl_call2}/          # ours 정본, N=3375/93
experiments/external/runs/full/materialized_lbox300/{lbox_call1,kbl_call2}/  # LBOX 300-subset(+KBL 93 복사)
experiments/external/runs/full/{lbox_call1,kbl_call2}/{predictions,scores}.json*   # ours 결과
experiments/external/runs/full/lbox_call1_300subset/{predictions,scores}.json*     # ours 300-subset 재채점
experiments/external/runs/baselines/225242/                                  # vanilla+CoT, 300-subset(취소된 225195 대체)
experiments/external/runs/baselines/{225237,225238,225239,225240,225241}/    # acal/leprec/legal_chain_reasoner/fol/standard_rag, 300-subset
```

신규 코드: `scripts/build_v2_external_baseline_dataset.py`,
`scripts/score_v2_external_benchmark_baseline.py`,
`scripts/slurm/run_v2_external_benchmark_baselines.sh`. 테스트 수정:
`tests/test_v2_external_benchmarks.py`(존재 불가능한 leakage 단언 수정, §부록 없음 — 별도
커밋 메시지 참조).
