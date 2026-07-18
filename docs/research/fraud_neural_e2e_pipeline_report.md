# 사기죄 Neural-to-Scallop 파이프라인 구축보고서

> 이 문서는 사람이 읽는 구축보고서다. `data/e2e/fraud/fraud_neural_e2e_vllm_report.json`은
> 해시와 토큰 수 등을 재현하는 기계용 기록이다.

## 결론

- KCL 형사법 문항의 사기죄 사실관계를 로컬 `google/gemma-4-26B-A4B-it`가 읽고,
  FactGraph와 13개 NormCard 판단을 생성한 뒤 네이티브 Scallop이 최종 결론을 내리는
  end-to-end 파이프라인을 구축했다.
- 최종 Slurm 작업 `210061`은 `COMPLETED (0:0)`였고, Scallop은
  `fraud_elements_satisfied=true`, `fraud_established=true`를 출력했다.
- 모델에는 KCL rubric이나 모범답안을 주지 않았다. 모델의 두 번째 호출에는 호스트가 고른
  NormCard의 명제와 주석서 인용만 authority packet으로 제공했다.
- 이 결과는 **한 사례에서 인터페이스가 끝까지 연결됐다는 증명**이다. 모델의 일반적 법률
  정확도나 전체 KCL 성능을 증명하는 실험은 아니다.

## 실제 입력

대상은 `kcl_criminal_r14_p1_q2`의 (2) 문단 중 **乙의 B에 대한 사기죄**다.

> 乙은 형사처벌을 면하기 위한 금품 자금을 마련하려고 친구 B에게 딸의 수술비 명목인
> 것처럼 말하여 3천만 원을 빌렸다. 이후 그 돈을 丙에게 주어 P1에게 전달하게 했다.

원문 전체 문단은 모델에 제공했지만, 문제 라우터가 다음 대상 거래를 별도로 지정했다.

| 항목 | 값 |
|---|---|
| 피고인 힌트 | 乙 |
| 상대방 힌트 | B |
| 대상 처분행위 | B가 乙에게 3천만 원을 빌려준 차용 거래 |
| 대상 거래의 이전자 | B |
| 대상 거래의 직접 취득자 | 乙 |
| 허용 사실유형 | 일반형, 차용 목적 기망형 |

이 경계가 없으면 모델이 후속 뇌물 전달과 丙의 소비까지 대상 사기의 취득 구조로 섞는 문제가
실제 실행에서 발생했다.

## 전체 흐름

```text
KCL 사실관계와 질문
  -> 문제 라우터가 사기 쟁점·대상 거래 지정
  -> Gemma: 출처 문구가 붙은 FactGraph 추출
  -> 호스트: 스키마·인용·동일인·역할·프로파일 검증
  -> 호스트: 대상 거래의 피고인·처분자·직접 취득자 역할 앵커링
  -> 호스트: loan_purpose용 검토 완료 NormCard 13개 선택
  -> 호스트: NormCard와 주석서 인용 14개로 authority packet 구성
  -> Gemma: 각 카드에 satisfied / not_satisfied / unknown 판단
  -> 호스트: 사실 ID·출처 ID·증거 방향·카드 완전성 검증
  -> 검증된 판단만 provable=true인 Scallop fact로 변환
  -> scli 0.2.4: RuleIR에서 컴파일된 342개 규칙 실행
  -> 사기죄 성립 / 불성립 / 미확인 / 충돌 relation 출력
```

## 책임 분리

| 단계 | 담당 | 하는 일 | 하지 않는 일 |
|---|---|---|---|
| 쟁점 라우팅 | 호스트 | 대상 죄명과 거래 경계를 정함 | 유무죄 결론을 넣지 않음 |
| FactGraph | Gemma | 원문 인용, 원자적 사실, 행위자, 후보 역할, 프로파일, 검색 질의 추출 | 판례·rubric을 보지 않음 |
| 역할 앵커 | 호스트 | 라우터가 정한 대상 거래의 3개 역할만 결정론적으로 고정 | 신경망 사실이나 법적 평가를 수정하지 않음 |
| 카드 선택 | 호스트 | 검토 완료된 차용 목적 기망용 카드 13개를 정확히 선택 | 모델이 규칙을 임의 추가·삭제하지 못함 |
| authority RAG | 호스트 | 선택 카드의 명제와 승인된 주석서 인용만 제공 | 사건 사실을 검색 결과로 보충하지 않음 |
| 카드 평가 | Gemma | FactGraph와 authority를 연결해 3상태 판단 | 최종 AND gate를 직접 계산하지 않음 |
| 안전 검증 | 호스트 | 인용·ID·완전성·증거 방향을 검사하고 provable을 부여 | 검증 실패 출력을 Scallop에 넣지 않음 |
| 최종 추론 | Scallop | 검토된 RuleIR 규칙으로 결정론적 결론 계산 | 자연어를 직접 읽지 않음 |

## 첫 번째 모델 호출: FactGraph

최종 실행에서 모델은 9개 사실을 추출했다. 핵심 내용은 다음과 같다.

| 사실군 | 모델이 구조화한 내용 |
|---|---|
| 범행 목적 | 乙은 P1에게 금품을 주어 형사처벌을 면하려 했다. |
| 표시한 용도 | 乙은 B에게 딸의 수술비 명목이라고 말했다. |
| 대상 처분 | B가 乙에게 3천만 원을 빌려주었다. |
| 직접 수령 | 乙이 B로부터 3천만 원을 수령했다. |
| 사후 행위 | 乙이 丙에게 전달을 부탁했고, 丙은 일부를 소비하고 나머지를 P1에게 전달했다. |

각 사실에는 원문에서 그대로 복사한 `source_quote`, 참여자 ID, 인식 상태, 쟁점 방향이 붙는다.
호스트는 인용문이 원문 연속 부분문자열인지 확인하며, 존재하지 않는 인용이나 참여자 ID는
즉시 거부한다.

### 역할 오추출과 앵커링

모델 원출력은 乙을 피고인, B를 피기망자·처분자·재산소유자로 맞게 잡았지만, 후속 전달자
丙을 대상 사기의 `beneficiary`로 잘못 지정했다. 호스트는 라우터가 미리 정한 대상 거래
`B -> 乙`에 따라 다음 한 건만 교정했다.

| 역할 | 모델 원출력 | 앵커 적용 후 |
|---|---|---|
| 피고인 | 乙 | 乙 |
| 피기망자 | B | B |
| 처분자 | B | B |
| 재산소유자 | B | B |
| 대상 거래의 직접 취득자 | 丙 | 乙 |

감사기록에는 `beneficiary: actor_byeong -> actor_eul, changed=true`가 남는다. FactGraph의
9개 사실은 수정하지 않았다. 같은 표기 乙 또는 B를 역할별로 여러 entity로 분리하는 출력도
별도 동일인 검증으로 거부한다.

## 두 번째 모델 호출: NormCard 평가

`loan_purpose` 프로파일에 대해 호스트가 고른 13개 카드와 14개 주석서 인용을 모델에
제공했다. 결과는 다음과 같다.

| 번호 | 사람이 읽는 쟁점 | 모델 판단 |
|---:|---|---|
| 1 | 3천만 원이 사기죄의 재물 객체인가 | 충족 |
| 2 | 차용 목적 기망이 대여 여부를 좌우할 정도로 중요한가 | 충족 |
| 3 | B에게 사실과 다른 인식인 착오가 있었는가 | 충족 |
| 4 | 용도에 관한 동기의 착오도 처분 동기가 되는가 | 충족 |
| 5 | B의 대여가 재산적 처분행위인가 | 충족 |
| 6 | 3천만 원의 사실상 지배가 乙에게 이전됐는가 | 충족 |
| 7 | 기망-착오-처분-교부의 순차적 인과관계가 있는가 | 충족 |
| 8 | 재물 이전으로 기수에 이르렀는가 | 충족 |
| 9 | 객관적 사정상 차용금 편취의 범의를 추단할 수 있는가 | 충족 |
| 10 | 차용 당시 편취의 범의가 있었는가 | 충족 |
| 11 | 재산적 이득을 취할 목적의사가 있었는가 | 충족 |
| 12 | '처분 유도 의사가 없으면 불성립'이라는 부정요건이 해당하는가 | 불충족: 처분 유도 의사는 있었음 |
| 13 | 피기망자와 처분행위자가 동일인인가 | 충족 |

여기서 12번의 `not_satisfied`는 사기죄를 부정한다는 뜻이 아니다. 카드 문장 자체가
"처분하게 할 의사가 없으면 성립하지 않는다"라는 부정형이므로, 乙에게 처분 유도 의사가
있다는 사실이 그 문장을 반증한 것이다. 이 경우 반증 사실은 `counter_fact_ids`에 들어간다.

## Scallop 입력과 출력

호스트는 검증을 모두 통과한 13개 판단에만 `provable=true`를 붙였다. 모델은 이 값을 직접
출력할 수 없다. 역할 ID는 앵커 적용 후 乙과 B 두 entity로 정리됐고, 동일인이 아닌 두 사람의
상이성 fact도 생성됐다.

| Scallop relation | 실제 출력 | 의미 |
|---|---:|---|
| `fraud_elements_satisfied` | true | 구성요건 component가 모두 연결됨 |
| `fraud_established` | true | 최종 사기죄 성립 |
| `fraud_not_established` | false | 명시적 불성립 사유 없음 |
| `fraud_undetermined` | false | 필수 미확인 쟁점 없음 |
| `fraud_conflict` | false | 상충 평가 없음 |

RuleIR은 검토된 사기죄 NormCard 88개를 바탕으로 predicate 201개, rule 342개로 구성되어 있다.
이번 사례에서는 그중 라우터가 선택한 13개 카드의 평가만 사건 fact로 주입했다.

## 실행 환경과 재현 기록

| 항목 | 실제 값 |
|---|---|
| 최종 Slurm job | `210061` |
| 상태 / 종료코드 | `COMPLETED` / `0:0` |
| 경과시간 | 2분 27초 |
| GPU | NVIDIA RTX PRO 6000 Blackwell Max-Q, 97,887 MiB |
| 자원 | GPU 1, CPU 2, RAM 32G, 제한시간 48시간 |
| node 지정 | 없음 |
| 모델 | `google/gemma-4-26B-A4B-it` 로컬 snapshot |
| 모델 tensor bytes | 51,611,872,412, index와 정확히 일치 |
| vLLM / Torch | 0.22.0 / 2.11.0+cu130 |
| 모델 서버 | 계산노드의 `127.0.0.1`, 외부 API·다운로드 없음 |
| 구조화 출력 | guidance backend, JSON Schema, 공백 없는 decoding |
| FactGraph 토큰 | prompt 992 + completion 1,076 = 2,068 |
| 카드 평가 토큰 | prompt 4,290 + completion 1,972 = 6,262 |
| Scallop | 고정 `scli 0.2.4` |
| 전체 테스트 | 89 passed in 43.42s |

재현 명령은 다음과 같다. 모델 실행은 반드시 Slurm을 거친다.

```bash
sbatch scripts/slurm/run_fraud_neural_e2e.sh
/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q
```

## 실패하면서 고친 인터페이스

| 단계 | 발견한 문제 | 현재 처리 |
|---|---|---|
| vLLM 기동 | Blackwell 환경에서 간헐적 사전 로그 segfault | 최대 3회 기동 재시도 |
| CLI 호환 | 설치된 vLLM에 없는 옵션 사용 | 0.22.0 실제 CLI에 맞춤 |
| 구조화 출력 | guidance가 JSON Schema의 `uniqueItems`를 지원하지 않음 | decoding용 호환 schema에서만 제거, 호스트 원본 schema로 재검증 |
| 출력 길이 | 공백이 과도해 토큰 한도 전에 JSON이 끊김 | 배열 상한과 공백 없는 guidance backend 사용 |
| 대상 거래 | P1·丙을 대상 사기의 수익자로 혼입 | 문제 라우터의 target transaction 도입 |
| 동일인 해소 | 같은 B와 乙을 역할별 entity로 분리 | 같은 mention의 복수 entity를 거부 |
| 역할 판단 | 모델이 후속 전달자 丙을 직접 취득자로 오판 | 원출력 보존 후 대상 거래 3개 역할만 감사 가능한 앵커 적용 |
| 증거 방향 | `not_satisfied`의 반증 사실을 basis로 요구 | satisfied=basis, not_satisfied=counter, unknown=missing으로 정정 |
| 무결론 | 모든 최종 relation이 비어도 pass로 기록 | `blocked_without_final_conclusion`은 작업 실패 처리 |

이 과정에서 검증 실패 모델 출력은 다음 단계나 Scallop으로 넘기지 않았다. 마지막 성공 작업만
추적 보고서로 채택했다.

## 이번 결과가 증명하지 않은 것

1. 사기죄 전체 사실유형에 대한 정확도는 측정하지 않았다. 현재 실제 E2E는 차용 목적 기망형
   하나와 검토된 13개 카드 경로만 대상으로 한다.
2. 역할 앵커는 upstream 문제 라우터가 대상 거래의 이전자와 직접 취득자를 특정할 수 있다는
   전제를 둔다. 서술형 수사자료에서 이 거래 경계를 자동으로 찾는 성능은 별도 과제다.
3. 모델은 카드 2에서 "진정한 용도를 알았다면 B가 대여하지 않았을 관계"를 인정하는 등
   원문 사실과 법적 평가를 연결했다. 한 사례에서 타당해 보여도 일반화 정확도는 사람의 gold
   annotation과 다수 사례 평가로 검증해야 한다.
4. FactGraph의 일부 `fact_kind`는 실제 목적이나 동의 사실을 `mistake`로 분류했다. 현재 핵심
   판단에는 영향을 주지 않았지만, feature 품질 개선 대상이다.
5. 처리량, 동시성, 비용, calibration, 장문 답안 생성 성능은 이번 종료조건 밖이다.

## 주요 산출물

| 용도 | 파일 |
|---|---|
| 사람이 읽는 본 보고서 | `docs/research/fraud_neural_e2e_pipeline_report.md` |
| KCL 사례 계약 | `data/e2e/fraud/kcl_r14_p1_q2_case.json` |
| FactGraph 계약 | `docs/contracts/fraud_fact_graph.schema.json` |
| 카드 평가 계약 | `docs/contracts/fraud_assessment_bundle.schema.json` |
| neural 검증·변환 코드 | `src/idpr/neural/__init__.py` |
| vLLM 호출 코드 | `src/idpr/neural/vllm_client.py` |
| 전체 orchestrator | `scripts/run_fraud_neural_e2e.py` |
| Slurm 실행 스크립트 | `scripts/slurm/run_fraud_neural_e2e.sh` |
| 최종 기계 보고서 | `data/e2e/fraud/fraud_neural_e2e_vllm_report.json` |
| 최종 원출력·중간 산출물 | `.cache/e2e/fraud/210061/` |
| 컴파일된 규칙 | `rules/generated/fraud_article347_full_v1.scl` |
