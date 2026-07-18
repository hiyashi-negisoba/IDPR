# 사기죄 IRACPlan 장문생성 6방법 비교보고서

> 이 문서는 사람이 읽는 최종 보고서다. 수치·토큰·해시의 기계 기록은
> [`fraud_irac_matrix_report.json`](../../data/e2e/fraud/irac_matrix/fraud_irac_matrix_report.json),
> 각 방법의 실제 답안은 같은 디렉터리의 `m1`~`m6` Markdown에서 확인할 수 있다.

## 결론

- 동일한 KCL 사기죄 사례에 대해 직접생성부터 ClaimGraph 검증까지 6개 방법을 실제
  `google/gemma-4-26B-A4B-it`와 Scallop으로 모두 실행했다. 최종 Slurm job `210075`는
  `COMPLETED (0:0)`, 총 경과시간은 6분 18초다.
- 법리적 정확성과 장문 내적 일관성은 실제로 별도 문제였다. Scallop 결론을 넣은 방법 4도
  법적 결론은 안정화했지만, 단락 구성·근거 완전성을 직접 강제하지는 않았다.
- RAG-only인 방법 2는 본문과 summary에서는 사기죄 성립이라고 쓰면서 JSON의
  `overall_conclusion`은 `undetermined`로 냈다. 장문 생성의 내적 불일치를 보여주는 가장
  명확한 사례다.
- IRACPlan을 넣은 방법 5는 5개 쟁점 단위를 모두 작성했지만 카드 ID 오기와 필수 카드 누락
  4개가 남았다. 계획이 coverage를 높여도 생성 문자열의 정확성을 자동 보장하지는 않았다.
- 방법 6은 ClaimGraph가 찾은 6개 위반을 `객체·역할`, `고의` 두 단락으로 국소화해 그 둘만
  재생성했다. 나머지 3단락의 해시는 그대로 보존됐고, 재검증 위반은 0개가 됐다.
- 병목은 모델 호출이다. RAG는 0.03~0.04초, IRACPlan 컴파일은 약 0.004초다. Scallop은
  약 4.46초로 문자 그대로 zero latency는 아니지만, 방법 4~6의 대부분은 FactGraph,
  카드평가, 장문생성, ClaimGraph 호출 시간이다.

## 실험 대상과 통제

대상은 `kcl_criminal_r14_p1_q2`의 전체 죄책 중 **乙의 B에 대한 사기죄**만 잘라낸 사례다.
乙은 P1에게 줄 금품을 마련하려고 B에게 딸의 수술비라고 말하여 3천만 원을 빌렸다.

- 모든 방법은 같은 사건 원문과 질문을 사용했다.
- 방법별로 필요한 FactGraph와 카드평가를 다시 호출했다. 앞 방법의 neural 결과를 다음
  방법이 재사용하지 않았다.
- vLLM prefix cache를 실제로 `False`로 설정했다.
- 5개 structured schema는 측정 전에 한 번씩 워밍업했다. 서버 startup과 schema 워밍업은
  아래 warm latency에서 제외했다.
- temperature는 0이다.
- KCL rubric과 모범답안은 모델에 제공하지 않았다. rubric은 모든 생성이 끝난 뒤 질적
  평가에만 사용했다.
- 모델 실행은 외부 API가 아니라 Slurm 계산노드의 로컬 vLLM에서만 수행했다.

## 6방법 매트릭스

| 방법 | 구성 | 모델 호출 | Warm E2E | 구조화 결론 | 검증 상태 | 핵심 관찰 |
|---:|---|---:|---:|---|---|---|
| 1 | 직접생성 | 1 | 4.952초 | established | 통과 | 빠르고 결론도 맞지만 주관적 요건 논증이 얕다. |
| 2 | RAG | 1 | 7.038초 | undetermined | 계약 통과, 내용 불일치 | 본문·summary는 성립인데 overall만 미확정이다. |
| 3 | FactGraph + RAG | 2 | 16.879초 | established | 통과 | 사실-법리 연결과 인과관계가 선명해졌지만 고의 논증은 빠졌다. |
| 4 | FactGraph + 카드평가 + Scallop | 3 | 41.767초 | established | 통과 | 객체부터 주관적 요건까지 가장 균형 있게 커버한다. |
| 5 | 방법 4 + IRACPlan | 3 | 47.250초 | established | 4개 위반 | 5단위 coverage는 가장 좋지만 ID 오기·필수 카드 누락이 있다. |
| 6 | 방법 5 + ClaimGraph + 부분재생성 | 6 | 124.561초 | established | 최종 0개 위반 | 2단락만 고쳐 3단락을 보존했다. 품질은 가장 안정적이나 가장 느리다. |

방법 4~6의 “카드평가”는 13개 카드를 한 번의 structured call에서 함께 평가한다. 따라서
모델 호출 수 3은 FactGraph 1회, 카드평가 1회, 장문생성 1회를 뜻한다. 방법 6은 여기에
ClaimGraph 2회와 단락 재생성 1회가 추가됐다.

## Latency 분해

| 방법 | FactGraph | 카드평가 | Scallop | RAG / Plan | 답안생성 | ClaimGraph | 부분재생성 | 합계 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | - | - | - | - | 4.950 | - | - | 4.952 |
| 2 | - | - | - | RAG 0.0416 | 6.995 | - | - | 7.038 |
| 3 | 7.442 | - | - | RAG 0.0314 | 9.389 | - | - | 16.879 |
| 4 | 7.432 | 14.551 | 4.471 | - | 15.293 | - | - | 41.767 |
| 5 | 7.428 | 14.538 | 4.473 | Plan 0.0041 | 20.793 | - | - | 47.250 |
| 6 | 7.427 | 14.539 | 4.459 | Plan 0.0037 | 21.716 | 33.195 + 34.456 | 8.732 | 124.561 |

단위는 초다. 작은 파일 기록·호스트 검증 시간이 있어 반올림한 단계 합과 E2E가 완전히
같지는 않다.

방법 4의 모델 호출 합은 약 37.28초이고 Scallop은 4.47초다. 방법 5에서 IRACPlan 자체는
4ms에 불과하며 방법 4보다 느려진 이유는 더 긴 계획을 조건으로 장문을 생성했기 때문이다.
방법 6의 추가 비용은 거의 전부 두 번의 ClaimGraph 역파싱이다. 현재 하드웨어에서 장문
일관성 검증은 symbolic host가 아니라 neural back-parser가 병목이다.

## 질적 비교

| 방법 | 법리 coverage | 사실 적용 | 문서 내 결론 일치 | 근거 무결성 | 사람이 읽는 품질 |
|---:|---|---|---|---|---|
| 1 | 중간 | 타당 | 일치 | 내부 지식, 명시 authority 없음 | 간결하고 깨끗함 |
| 2 | 중간 | 타당 | **불일치** | 핵심 RAG 1건은 적절, 나머지는 잡음 | 본문만 읽으면 자연스러움 |
| 3 | 중간~높음 | FactGraph로 선명 | 일치 | 출처 선택에 일부 잡음 | 자연스러움 |
| 4 | 높음 | 구성요건별 구체적 | 일치 | 13개 검토 카드 + Scallop | 가장 좋은 비용/품질 균형 |
| 5 | 높음 | 5개 IRAC 단위 | 일치 | metadata 4개 위반 | 원출력 ID 노출은 renderer가 숨김 |
| 6 | 높음 | 5개 IRAC 단위 | 일치 | 최종 위반 0 | 최종 사람이 읽는 답안이 가장 완결적 |

### 방법 1: 직접생성

기망-착오-처분-인과-성립이라는 기본 구조를 641자로 정확히 썼다. 실제 뇌물 자금 목적과
수술비 표시를 구별했고, “진정한 목적을 알았다면 B가 빌려주지 않았을 것”이라는 적용도
했다. 다만 객체, 행위시 편취의 범의, 처분 유도 의사 등은 독립 쟁점으로 전개하지 않았다.
직접생성 baseline으로는 준수하지만 모범 사례형 답안으로는 얕다.

### 방법 2: RAG

558개 retrieval-only 카드에서 `fraud_mistake.false_loan_purpose`가 1위로 검색됐고, 모델은
실제로 이 카드만 핵심 법리로 사용했다. 하지만 나머지 상위 결과에는 은행장 승인 대출,
명의상 허가자 경매, 군용물 제재 등이 섞였다. 검색 corpus가 넓고 한 사례 질의만으로는
상위 6개 중 5개가 사실상 distractor였다.

본문의 법리·적용·결론은 모두 사기죄 성립인데 각 단락 metadata는 대부분 `unknown`, 문서
overall은 `undetermined`였다. RAG는 법리 재료를 공급했지만 문서 수준 결론 합치를 보장하지
못했다.

### 방법 3: FactGraph + RAG

대상 거래의 fact ID를 이용하면서 기망, 착오, 3천만 원 대여, 乙의 직접 수령을 더 명확히
연결했다. overall도 본문과 같은 `established`로 돌아왔다. 다만 RAG 상위 결과에는 여전히
자동차 명의신탁, 전대차 보증금 등 좁은 사안이 들어갔고, 모델은 전대차 카드의 source까지
일반 법리에 인용했다. 검색 결과의 proposition과 source attribution을 별도로 검증할
필요가 있다. 주관적 구성요건을 독립적으로 논증하지 않은 점도 남는다.

### 방법 4: FactGraph + Scallop

객체, 기망·착오, 처분·인과관계, 편취의 범의, 기수 순서로 5개 단락을 구성했다. Scallop이
`fraud_established=true`를 제공해 최종 결론이 흔들리지 않았고, 13개 core 카드의 법리도
대체로 자연스럽게 사용했다. IRACPlan 없이도 결과가 좋았던 이유는 카드 assessment와
authority packet 자체가 풍부한 구조를 제공했기 때문이다.

한 사례 기준으로는 방법 4가 가장 실용적인 지점이다. 방법 3보다 약 25초 느리지만 법적
구성요건 coverage가 크게 좋아지고, 방법 6보다는 약 83초 빠르다.

### 방법 5: IRACPlan

호스트가 13개 카드평가와 Scallop 결론을 다음 5개 micro-IRAC 단위로 컴파일했다.

1. 객체와 역할
2. 차용 목적 기망
3. 착오와 처분
4. 인과관계·취득·기수
5. 편취의 범의와 재산적 이득 목적

출력은 이 순서와 단락 수를 정확히 지켰고 방법 4보다 더 자세했다. 그러나 첫 단락에서
`general_object...` 카드 ID를 `general...`로 잘못 썼고, 존재하지 않는 authority 문자열을
만들었다. 또한 객체 카드와 “처분 유도 의사 없음” 부정형 카드의 metadata가 빠져 총 4개
위반이 생겼다. IRACPlan은 논리적 coverage를 강제하지만 exact provenance copy는 별도
검증이 필요하다는 결과다.

### 방법 6: ClaimGraph와 부분재생성

1차 검증은 다음 6개를 찾았다.

- 객체·역할 단락: 카드 ID 오기 1건, authority ID 오기 1건, 필수 카드 누락 1건
- 고의 단락: 필수 부정형 카드 metadata 누락 1건
- 고의 단락 ClaimGraph: 필수 카드 coverage 누락 1건, 적용 사실 coverage 누락 1건

ClaimGraph raw output의 중복 authority ID 1건은 의미를 바꾸지 않는 순서 보존 dedup으로
정규화했다. `claim_type` 라벨 자체보다 실제 `fact_ids + card_ids` 연결을 적용 주장으로
검사해 back-parser의 라벨 표현 차이가 답안 false positive가 되지 않게 했다.

호스트는 위반이 있는 `irac_object_roles`, `irac_intent`만 repair prompt로 보냈다.
`irac_deception`, `irac_mistake_disposition`, `irac_causation_completion`은 전후 SHA-256이
같다. 재생성된 고의 단락에는 빠졌던 처분 유도 의사가 명시됐고, 2차 ClaimGraph 검증은
0개 위반으로 끝났다.

이 결과는 부분재생성이 실제로 작동한다는 한 사례의 실행 증거다. 다만 ClaimGraph 두 번이
약 67.65초를 차지하므로 매번 전체 답안을 역파싱하는 방식은 비싸다. 다음 실험에서는
단락별 병렬 검증, 하나의 back-parse 결과 재사용, 저비용 verifier 모델을 비교할 가치가 있다.

## KCL rubric 사후 대조

모델 입력에는 rubric을 넣지 않았다. 생성 완료 후 inventory의 rubric summary를 열어
사기죄 부분만 대조했다.

- 모든 방법이 乙의 B에 대한 사기죄와 용도기망을 핵심 쟁점으로 잡았다.
- 모든 방법이 진정한 용도를 알았다면 대여하지 않았을 관계라는 판례형 기준을 사용했다.
- **모든 방법이 형법 제347조 제1항을 명시적으로 인용하지 않았다.** core NormCard/IRACPlan에
  조문 citation을 별도 필수 필드로 넣지 않은 공통 설계 gap이다.
- 방법 1~3은 고의와 목적의사를 독립 단락에서 충분히 논하지 않았다. 방법 4~6은 행위시
  편취의 범의와 재산적 이득 목적을 명시했다.
- KCL rubric은 고의 및 불법영득의사를 요구하지만, 현재 RuleIR 정책은 불법영득의사를 모든
  사기유형의 별도 공통 gate로 강제하지 않는다. 이는 오류라기보다 benchmark scoring과
  실무지향 rule policy의 차이이므로 논문에서 명시해야 한다.
- 모든 방법이 “B가 진정한 용도를 알았다면 빌려주지 않았을 것”을 추론했다. 이 사안에서는
  타당해 보이지만 원문에 직접 적힌 사실은 아니므로, 다수 사례에서 human gold와 비교해야
  일반화 성능을 말할 수 있다.

## 연구적 해석

이번 실험은 다음의 계층 분리가 타당하다는 초기 증거를 준다.

```text
사실 추출
  -> RAG와 카드별 법리 적용
  -> Scallop의 법적 결론
  -> IRACPlan의 담화 구조와 단락별 요구 결론
  -> 장문 생성
  -> ClaimGraph 역파싱
  -> 실패 단락만 재생성
```

Scallop은 구성요건 AND와 최종 법적 결론을 안정화한다. IRACPlan은 어떤 쟁점을 어떤 순서로
써야 하는지 통제한다. ClaimGraph는 생성된 문장이 그 계획의 사실·법리·결론을 실제로
보존했는지 검사한다. 세 층은 대체관계가 아니라 서로 다른 오류를 담당한다.

워크샵 논문의 주된 가설은 “symbolic conclusion만으로는 long-form self-consistency가
보장되지 않으며, derivation-conditioned plan과 post-generation verification이 별도로
필요하다”로 정리할 수 있다. 다만 현재 결과는 단일 사기 사례의 engineering proof다.
KCL 61문항으로 확장하기 전에 복수 사기 사례와 사람 annotation으로 verifier precision과
false-positive rate를 먼저 측정해야 한다.

## 실행 중 발견한 인터페이스 문제

| Job | 결과 | 발견한 문제 | 처리 |
|---|---|---|---|
| `210072` | FAILED 1:0, 3:01 | 직접생성이 원문을 `case_text` provenance로 표기했으나 허용 목록이 없었음 | 원문 기반 방법에 정식 provenance ID 제공 |
| `210073` | FAILED 1:0, 4:24 | 방법 5의 ID 오기를 host가 실험 전체 오류로 처리 | 답안 오류를 품질 위반으로 기록하고 계속 실행 |
| `210074` | COMPLETED 0:0, 6:28 | 중복 ID와 claim label 차이를 과도하게 문서 오류로 판정 | 중복 정규화, provenance 기반 검증으로 수정 |
| `210075` | **COMPLETED 0:0, 6:18** | 최종 재현 실행 | 2단락 patch, 3단락 보존, 최종 위반 0 |

방법 5·6의 raw JSON body는 모델이 내부 ID를 괄호 안에 노출했다. 기계 원본은 감사 목적으로
그대로 보존하되, 사람이 읽는 Markdown renderer는 ID-only 괄호를 숨긴다. 법적 의미가 있는
일반 괄호 문구는 유지한다.

## 한계와 다음 실험

1. 사례가 하나라서 정확도·통계적 유의성·일반화는 평가할 수 없다.
2. 현재 RAG는 결정적 BM25+한글 bigram이며 reranker가 없다. 상위 결과 잡음이 크다.
3. RAG-only 방법은 core 카드가 아닌 558개 retrieval-only 카드만 검색했다. 방법 4~6의
   host-selected core authority와 입력 정보량이 다르므로 순수 component ablation은 아니다.
4. 방법 6은 verifier와 generator가 같은 Gemma 계열이다. 독립 모델 또는 사람 gold와의
   상관을 측정해야 self-verification bias를 평가할 수 있다.
5. 장문 품질 평가는 한 에이전트의 질적 판독이다. 다음 단계에서는 법률가 blind review와
   문항별 rubric scoring이 필요하다.
6. 조문 citation, 학설·판례 충돌, 절차법의 다층 gate는 다음 RuleIR/IRACPlan 계약에서
   별도 필수 단위로 설계해야 한다.

## 주요 산출물

| 용도 | 파일 |
|---|---|
| 본 보고서 | `docs/research/fraud_irac_matrix_human_report.md` |
| 기계 실행 보고서 | `data/e2e/fraud/irac_matrix/fraud_irac_matrix_report.json` |
| 방법 1~6 사람이 읽는 답안 | `data/e2e/fraud/irac_matrix/m*_answer.md` |
| 방법 1~6 machine answer | `data/e2e/fraud/irac_matrix/m*_answer.json` |
| IRACPlan 계약 | `docs/contracts/fraud_irac_plan.schema.json` |
| ClaimGraph 계약 | `docs/contracts/claim_graph.schema.json` |
| 부분 patch 계약 | `docs/contracts/section_patch_bundle.schema.json` |
| host compiler/verifier | `src/idpr/generation/__init__.py` |
| 6방법 orchestrator | `scripts/run_fraud_irac_matrix.py` |
| Slurm 실행 | `scripts/slurm/run_fraud_irac_matrix.sh` |
| 최종 raw/intermediate | `.cache/e2e/fraud_irac_matrix/210075/` |

재현 명령:

```bash
sbatch scripts/slurm/run_fraud_irac_matrix.sh
PYTHONPATH=src /data5/jaehoonjeong/miniconda3/bin/python -m pytest -q
```
