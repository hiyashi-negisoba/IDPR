# 에이전트 작업 오류 사후분석 및 반성

작성일: 2026-07-16

## 요약

이번 대화에서 가장 큰 문제는 연구 목표를 충분히 고정하지 않은 채 구현 세부로 먼저
들어간 점과, API 산출물의 완전성을 보장할 계약을 처음부터 설계하지 않아 비용이 큰
재실행을 만든 점이다. 사용자가 직접 바로잡은 방향과 실행 중 발견된 오류를 아래에
구분해 기록한다.

## 목표 이해 오류

### KCL 61개 long-form보다 DCDE 연결을 앞세움

사용자의 main task는 한국 형사법 61개 설문에 대한 long-form generation과 문서 내부
self-consistency였다. 그런데 초기 연구 정리에서 이전 DCDE/OBJECTION 연구와의 연결을
과도하게 전면에 두었다. 사용자가 “자꾸 DCDE쪽으로 간다”고 지적한 뒤에야 KCL 61개를
주 태스크로 다시 명시했다.

원인은 관련 선행연구를 논문의 중심으로 착각한 것이다. 이후에는 연구 문서 첫머리에
main task, evaluation unit, output을 고정하고 DCDE는 동기와 secondary study로만
배치했다.

### “준비물”의 의미를 바로 고정하지 못함

사용자가 준비물을 말했을 때 NormCard와 RuleIR을 즉시 작업 단위로 확정하지 못했다.
대화의 가까운 문맥보다 넓은 연구 계획을 먼저 해석한 것이 원인이다. 이후에는
NormCandidate -> NormCard -> RuleIR -> Scallop 계약을 명시하고, 사기죄를 구조 예시로
완성하는 범위로 좁혔다.

### 검수 표에서 `covered=false`를 명시하지 않음

초기 KCL 검수표에는 사용자가 coverage를 육안 확인할 수 있는 `covered=false` 표시가
없었다. 내부 데이터에 값이 있다는 것과 사람이 검수표에서 볼 수 있다는 것을 혼동했다.
이후 표에 coverage 열을 추가하고 표시 여부를 테스트로 고정했다.

## 데이터 및 계약 설계 오류

### NormCard에 후보 계보를 처음부터 강제하지 않음

NormCard 1.0에는 어떤 NormCandidate가 어떤 카드로 병합됐는지 나타내는 필수 계보가
없었다. 그 결과 Terra가 기망 후보 211개 중 181개를 조용히 누락하고, 특수유형
101개를 4개 카드로 과도 병합해도 기본 스키마는 이를 잡지 못했다. v1과 v2 재생성에
큰 비용이 들었다.

수정:

- NormCardSet 1.1에 `candidate_refs` 필수화
- 입력 후보 전수 coverage 검사
- 카드 source가 연결 후보 source 합집합을 벗어나지 못하게 제한
- 다른 `norm_kind` 또는 `polarity` 후보의 병합 거부

앞으로 merge 단계에는 생성 품질보다 먼저 conservation invariant를 둔다.

### 사례 결과와 일반 규범의 경계를 늦게 강화함

주석서의 “본 사안”, 판시 내용, 개별 판결 결과가 standard_input이나 deterministic
rule로 올라갈 수 있었다. 이는 판례 적용례를 일반 법리로 과도하게 승격할 위험이다.
최종화 단계에서 판례 보고 표지를 탐지해 원판례 확인 전 `context_only`로 격리했다.

앞으로 primary authority가 확인되지 않은 사례 결과는 기본적으로 실행 규칙이 아니라
RAG context로 취급한다.

## API 실행 오류

### 분할 critic에 잘못된 전체 source scope를 제공함

카드 50개씩 분할해 Sol에 보내면서 target의 `source_scope`, 검토 질문, coverage gap은
모듈 전체 값을 유지했다. Sol은 제공되지 않은 나머지 출처를 당연히 out-of-scope로
판정했고, 26개의 가짜 source-scope 지적과 3개의 reject가 발생했다. 이 v1 감사에
399,052 tokens를 사용했다.

수정:

- 각 partial target의 source scope를 포함 카드의 source_refs로 재계산
- 검토 질문도 포함 카드 ID에 한정해 생성
- partition test에서 target source scope와 실제 카드 source ID의 동일성 검사

이 오류는 실행 전 payload conservation test를 만들었으면 막을 수 있었다.

### 비평 스키마에 `missing_variant`가 없었음

Sol이 정확히 “변형 누락”을 지적했지만 계약 enum에는 `collapsed_variant`만 있었다.
응답을 폐기하고 재호출했으나 모델은 같은 `missing_variant`를 다시 사용했다. 재호출
29,501 tokens가 불필요하게 들었다.

수정:

- `missing_variant`를 정식 finding type으로 추가
- 내용상 유효한 기존 응답을 로컬에서 재검증

앞으로 계약 실패가 의미 실패인지 표현 어휘의 계약 누락인지 먼저 판단하고, 같은
프롬프트 재호출 전에 schema repair 가능성을 확인한다.

### 같은 run ID 재사용으로 사용량 manifest를 덮어씀

실패한 한 요청만 재개하려고 같은 run ID를 사용했지만 runner가 `run.json`과
`sol_usage.jsonl`을 덮어썼다. 캐시는 유효 응답을 재사용했으나 최초 17건 실행의 사용량
manifest가 보존되지 않았다.

수정:

- 콘솔에 남은 두 실행 요약을 합산한 cumulative usage를 최종 audit manifest에 기록
- 최종화 스크립트가 현재 17개 보고서를 다시 계약 검증

향후 retry는 새 attempt ID를 사용하고 parent run을 참조하거나, usage manifest를
append-only로 기록해야 한다.

## 판단 및 진행 방식의 문제

### critic finding 0을 목표로 삼은 표현

초기 전략 문서에는 finding이 0이 될 때까지 반복 호출한다는 취지의 문장이 있었다.
법률 critic은 새로운 오탐이나 관점 차이를 계속 만들 수 있으므로 이 목표는 비용을
통제하지 못하고 모델 비평을 정답으로 오인하게 한다.

수정 후에는 finding을 자동 구조 수정, 사람 검수, 기각으로 adjudicate하고, 미해결
항목은 RuleIR gate에서 차단한다. 최종 사기죄 draft도 67개 지적을 숨기지 않고 검수
큐로 보존했다.

### RuleIR을 법률 승인 전 전수 생성하려 한 경향

NormCard merge가 불안정한 상태에서도 전체 RuleIR 생성으로 빨리 넘어가려는 계획을
세웠다. 이는 잘못된 권위와 과도한 일반화를 실행 규칙으로 굳힐 수 있다. 최종적으로
636개 중 61개만 형식상 잠정 진입 가능하다고 분류하고, 핵심 법리 승인이 끝날 때까지
전체 RuleIR 생성을 차단했다.

## 비용 영향

기록된 사기죄 전체 준비 실행은 약 2,885,006 tokens, 122 API calls다. 그중 명확한
실행기 실수로 발생한 최소 낭비는 428,553 tokens다. 모델 탐색과 정상적인 교정 비용을
실수 비용에 섞지 않고, 직접 원인이 확인되는 두 실행만 계산했다.

## 재발 방지 원칙

1. main task, 현재 scope, 종료 gate를 문서와 실행기에 함께 고정한다.
2. 생성 단계마다 입력 보존 invariant를 먼저 만들고 API를 호출한다.
3. partial payload는 source scope와 검토 질문도 같은 범위로 투영한다.
4. 계약 실패 시 재호출 전에 schema·validator 결함을 먼저 검사한다.
5. run artifact와 usage는 append-only 또는 attempt별로 보존한다.
6. critic은 조언자이며 수정 권한이나 법률 승인 권한을 주지 않는다.
7. primary authority 미확인 판례 적용례는 `context_only`로 둔다.
8. 사람 검수 전에는 RuleIR과 Scallop coverage를 주장하지 않는다.

## 반성

이번 작업에서 비용이 큰 오류들은 모델의 성능 부족만으로 설명할 수 없다. 후보 계보,
분할 범위, retry 기록처럼 로컬 코드로 통제할 수 있는 부분을 API 호출 전에 충분히
검증하지 않은 책임이 있다. 특히 첫 분할 critic 오류는 입력과 선언 범위가 같은지
확인하는 단순한 테스트로 방지할 수 있었다.

앞으로는 “모델이 잘할 것”을 전제로 진행하지 않고, 누락·과병합·권위 상승·범위 누출이
발생해도 자동으로 멈추는 계약을 먼저 만든다. 법적 판단이 필요한 부분은 모델 출력으로
덮지 않고 사용자가 판례 인덱스와 실무 기준으로 결정할 검수 항목으로 남긴다.
