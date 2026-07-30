# Phase 1 인수 문서 — 룰베이스 완료, Phase 2 착수 지점

2026-07-30 작성. 승인된 계획은 `~/.claude/plans/gentle-zooming-twilight.md`.
데드라인 2026-08-11 (NLLP 워크샵). Phase 0~1을 Day 1에 완주했으므로 계획보다 이틀 앞서 있다.

## 지금 상태

브랜치 `rulegen-campaign-pilot`. 테스트 **345 passed**. 워킹트리 클린.

```
767b163  아키텍처 A 폐기 + property rulegen 증적 복원
b38e3d6  베이스라인 하니스 7종 + rubric 채점 + 공정성 통제
757c5a3  카드 코퓨스 1,848장 + 요건 스켈레톤 402슬롯
7e3234d  LePREC 2단계화 + 검수 문서에 카드 내용 수록
441923a  검수 문서에 역할별 예시
0a9dc22  서술적 사실층 13술어 + 카드 라우팅 트리아지
3792f23  카드 단위 역할 검수 결과 파싱
d633f0b  SCL 컴파일러 (23술어 / 26규칙 / 8,060튜플) + 골든 40
e71b383  죄수·미수 수기 표 + 로드 검증 + 검수 문서
```

### 산출물

| 파일 | 내용 |
|---|---|
| `data/rulebase/kcl_rulebase.scl` | 컴파일된 룰베이스 8,200줄. 23 type / 26 rel / 11 query |
| `data/rulebase/fact_layer.scl` | 사실층 13술어 (콜 1이 채운다) |
| `data/rulebase/card_routing.json` | 카드 1,848장의 라우팅 판정 + 명제 |
| `data/rulebase/role_review.json` | 검수된 카드 역할 86건 + 미응답 큐 15건 |
| `data/rulebase/element_skeleton_review.md` | **검수자 주석 보유. 절대 덮어쓰지 말 것** |
| `data/rulebase/concurrence.yaml` / `stage.yaml` | 죄수·미수 수기 표 (검수 대기) |
| `data/rulebase/doctrine_review.md` | **사용자 검수 대기 중** |

재생성: `PYTHONPATH=src python scripts/build_rulebase.py`
(`element_skeleton_review.md`는 `> comment:`가 있으면 건너뛴다. `--rewrite-review`로만 덮어쓴다.)

파이썬은 `/data5/jaehoonjeong/miniconda3/bin/python`. 레포 `.venv`는 빈 껍데기다.

## 계획에서 벗어난 세 가지

### 1. 사실층 어휘는 서술적이다 (계획: 통칙 술어 9개)

계획의 술어 목록에는 `폭행`·`협박`·`추행`·`기망` 같은 법정 동사가 들어 있었다. 스모크
케이스를 손으로 인코딩해 보니 **그건 사실이 아니라 카드가 내릴 결론**이었다. 콜 1이
"甲이 A를 협박했다"를 사실로 쓰면 규범 판단이 추출 단계에서 끝나고, 콜 2의 카드 평가는
검수된 명제 없이 내려진 판단을 채점하게 된다.

그래서 전부 서술층으로 내렸다: `유형력행사`(→폭행인가), `해악고지`(→협박인가),
`신체접촉`(→추행인가), `공동주택공용부`(→주거인가), `신체손상`(→상해인가).
`tests/test_rulebase_facts.py::test_fact_labels_are_descriptive_not_normative`가 강제한다.

술어는 9 → 13개. 추가 넷은 각각 코퓨스의 사례가 강제했다: `party_relation`(친족상도례·
신분범), `holds`(절도·횡령), `purpose`(목적범), `causation`. 마지막 것이 중요하다 —
제263조 동시범은 **인과관계 "불명"이라는 것 자체가 사실**이라, 사실을 비워두면 "아무도
안 다친 사건"과 구별되지 않는다.

### 2. `deterministic_rule` 385규칙은 만들 수 없다 (계획의 Phase 1d 항목)

412장의 Datalog **바디가 자산 어디에도 없다**. 한국어 명제만 있고 기계가 읽을 조건이 없다.
그리고 412장은 한 종류가 아니다 — 죄의 정의 57, 요건 불요 37, 죄수 22, 기수·미수 20,
객체 범위 34, 프레임 0개 **152**.

바디 없이 규칙 형태만 뽑는 것이 이전 에이전트가 한 일이다(3,487 규칙 / 8종 바디,
1,592개가 `actor ∧ action_committed` 동어반복). 동어반복 규칙은 규칙이 없는 것보다 나쁘다 —
요건을 조용히, 반증 불가능하게 충족시킨다.

대신 카드를 **내용이 실제로 무엇을 구동할 수 있는지**로 라우팅했다:

| 라우트 | 카드 | 무엇이 되는가 |
|---|---:|---|
| `model_assess` | 1,555 | 콜 2가 판정 → `card_status` |
| `skeleton_meta` | 114 | "X는 필요하지 않다" → 스켈레톤 |
| `concurrence_seed` | 83 | 죄수 → `concurrence.yaml` |
| `stage_seed` | 59 | 기수·미수 → `stage.yaml` |
| `narrative` | 37 | 정의 — Rule 문단 서술 재료 |

`formalization` 필드는 라우팅을 예측하지 못한다: `deterministic_rule` 412장 중 282장(68%)이
아무 심볼릭 내용도 못 내놓고, 반대로 `standard_input` 139장이 씨앗이 된다. 테스트로 고정했다.

### 3. 요건 게이트는 모든 요건 슬롯을 요구하지 않는다

계획은 `slot_core` 전부의 적극적 충족을 요구했다. 요건 슬롯은 주석서 목차에서 오는데
**목차는 연언이 아니다** — 제298조의 `sec3_1 폭행`·`sec3_2 협박`·`sec3_3 추행`은 **하나의**
행위 요건의 부분이다. 조문당 요건 슬롯이 평균 4.5개, 최대 12개(제333조)라 전부 요구하면
`offense_established`가 영구히 발화하지 않는다.

그래서 차단을 적극적으로 정의했다: 요건 카드가 반증되거나, 예외 카드가 충족되거나,
조각사유가 충족될 때만 막는다. 논증되지 않은 요건은 `element_unaddressed`로 **보고**되고
게이트에 들어가지 않는다. 더 엄격한 게이트를 나중에 재컴파일 없이 측정할 수 있다.

**따라서 심볼릭 레이어가 실제로 결정하는 것**: 위법성·책임 조각, 명시적 반증, 죄수 흡수,
미수 검토 필요, 모순 검출. 계획의 "기여의 소재" 절이 측정한 conclusion+application 몫과
일치한다. 과대주장하지 않는다.

## 검수자와 일하는 방식 (중요)

사용자는 법률 검수자다. 검수는 **마크다운 문서에 `> comment:` 줄을 직접 달아** 돌려준다.
`src/idpr/rulebase/review.py`가 그걸 파싱한다 — 판정을 별도 파일로 전사하면 법적 판단이
저장소에 두 벌 생겨 갈라진다.

1차 검수에서 배운 것: **판정은 카드 단위로 온다.** 25개 슬롯 중 9개가 한 슬롯 안에서
역할이 갈렸다(제355조 총설 18장 = core 7 / defeater 4 / context 7). 그래서 역할은 카드의
속성이고 슬롯 역할은 카드 역할에서 파생된다.

검수 문서를 만들 때: 카드 **명제 전문**을 넣고, 역할별 **실제 예시**를 넣고, 무엇을 어떤
기준으로 고르면 되는지 명시한다. 슬롯 제목과 카드 개수만으로는 판단할 수 없다(1차에
그렇게 만들어 지적받았다).

## 지금 사용자 검수 대기 중

`data/rulebase/doctrine_review.md`. 핵심은 §3의 **의도적 충돌 2건**이다 — 조문 쌍만으로는
구별할 수 없는 구분(결과 발생 여부, 실행의 착수 여부)에 걸려 있어 어느 쪽으로 둘지
골라야 한다. 검수가 오면 `concurrence.yaml`/`stage.yaml`을 고치고 `status`를
`awaiting_legal_review`에서 바꾼다(`test_the_tables_are_flagged_as_awaiting_review`도 함께).

검수를 기다리며 Phase 2를 진행해도 된다. 죄수 표는 최종 죄명 선별에만 쓰이고 검색·평가에는
영향이 없다.

## Phase 2 착수 지점

`src/idpr/retrieval/` — dense(`embeddinggemma-300m`) + 문자 bigram BM25 + rerank
(`bge-reranker-v2-m3`). 검색 대상은 카드 1,848장의 `proposition`, 집계는 **조문 단위**.
조문은 넉넉하게 뽑고 **선택된 조문 안에서는 카드를 버리지 않는다** — 그게 rubric 항목을
잃는 경로다.

L0의 자체 지표는 **쟁점 리콜**이고, gold는 `issue_tags`다 — **평가 측 전용, 모델 입력
금지**. 스모크 케이스에서 간접정범·주거침입 위요지·중지미수·체포죄 대응 카드가 후보에
들어가는지 개별 확인한다. 7/7 베이스라인이 놓친 지점이다. **이 수치가 낮으면 하류 작업을
진행하지 않고 L0를 먼저 고친다.**

이어서 콜 1(사실 추출 + 쟁점 제안). 모든 fact는 `source_quote`가 `question_text`의 정확한
부분문자열이어야 하고 호스트가 raise로 강제한다. 사실층 라벨 검증은
`idpr.rulebase.facts.validate_fact`가 이미 한다.

### 먼저 확인할 것 (Phase 3 최우선이지만 미리 잡아두면 좋다)

`--max-model-len` 32,768 → 131,072 상향이 GPU 1장에서 실제로 되는지. 3콜 설계의 전제다.
안 되면 카드셋을 좁히거나 조문군 2~3개로 분할 후퇴.

## 잊지 말 것

- 긴 잡은 `sbatch`로. `nohup`은 고아 프로세스를 남긴다. sbatch 진행상황을 백그라운드에서
  반복 확인하지 말라(사용자 명시 금지).
- judge 프롬프트 전문은 **사용자 승인 후에만** 설치한다.
- 모델 입력 화이트리스트는 `question_text` + `question_prompt`뿐이다.
  `idpr.eval.input_formatter.assert_no_leaked_fields`가 게이트다.
- `supporting_precedents`(gold 판례 277개)를 검색 코퓨스로 쓰지 말 것. 평가 측 인용
  지표에만 쓴다.
- API 총예산 $100. Phase 1은 $0을 썼다(전부 결정론적 컴파일).

## 남은 빚

- `paper/03_methodology.md`, `paper/appendix_spec_statistics.md`가 폐기된 아키텍처 A를
  서술하고 있다(3,487 규칙, 7,084줄을 성과로 기술). Phase 6에서 재작성.
- `docs/KCL_1730_RULEBASE_SPECIFICATION.md`도 같은 문제.
- 검수 큐 미응답 15건은 전부 advisory이고, 침묵이 제목 기준 역할 승인이다(설계대로).
- `narrative` 37장의 Rule 문단 배선은 Phase 4.
