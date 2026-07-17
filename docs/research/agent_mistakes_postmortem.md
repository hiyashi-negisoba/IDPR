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

### finding 검수 큐를 전체 카드 검수처럼 설명함

`fraud_norm_card_review_queue.json`의 67개 항목은 카드 목록이 아니라 Sol finding
목록이었다. 하나의 finding이 여러 카드에 영향을 주고, 반대로 finding이 없는 카드도
`review_required=true`일 수 있는데 이 차이를 사용자에게 먼저 설명하지 않았다. 그
결과 사용자는 약 50여 개 finding을 검수하면 나머지 카드가 승인되는 것으로 이해할
수밖에 없었다.

더 큰 문제는 57개 finding에 대해 사용자가 “지적이 타당하다”고 판정한 뒤에도 실제
NormCard 수정은 하지 않은 채 `status=pending`으로 남겨 두고 RuleIR 진입 가능 카드
53개만 추렸다는 점이다. 검수 결과를 적용하는 것보다 다음 단계를 먼저 진행하려 한
잘못이다.

수정:

- 57개 accepted finding을 API 없이 카드·전체 source chunk와 직접 대조해 모두 반영
- 196개 카드 수정과 finding별 변경을 remediation ledger에 기록
- 67개 finding 모두 `resolved=true`, 57개 `remediation_status=applied`로 검증
- 결정 완료와 remediation 완료를 별도 상태로 검사하도록 queue builder 수정

### `critic_pending`의 의미를 잘못 설명함

사용자에게 187개를 “critic 자체가 끝나지 않은 카드”라고 설명했으나 실제로는 기존
critic finding의 영향 대상으로 계산된 카드였다. 코드의 bucket 이름을 사실 확인 없이
자연어로 확대 해석한 오류다. 게다가 당시 readiness와 최신 queue의 영향 카드 수도
서로 일치하지 않았다.

수정 후 readiness는 `critic_pending`과 포괄적인 `human_review_pending`을 제거하고,
실행 역할에 따라 deterministic rule, standard input, policy choice, RAG context로
전수 분류한다. 모든 수의 합이 전체 카드 수와 같지 않으면 테스트가 실패한다.

### neural grounding과 사람의 법률검토를 혼동함

`standard_input`은 사실관계에 대한 모델 판단이 필요하다는 뜻인데, 이를 곧바로
`review_required=true`와 동일시했다. 그 결과 source-bounded standard까지 232개
`human_review_pending`처럼 보였고, 사용자가 실제로 무엇을 검토해야 하는지 알 수
없었다.

수정 후 `standard_input`은 RuleIR의 neural input predicate로 승인할 수 있고,
사람이 선택해야 하는 법적 불확실성은 `policy_variant`에만 남긴다. 사례 판례와 현행법
미확인 내용은 `context_only`로 내려 RAG에서만 사용한다.

### 경쟁 견해를 한 카드에 합친 채 사용자에게 선택을 요구함

삼각사기 네 학설, 전체재산설·개별재산설, 재물 가치 기준, 보호법익 대립이 한 카드에
합쳐져 있었다. 이 상태에서 policy 선택을 요청하면 선택 가능한 단위가 존재하지 않는다.
또 판례 설명과 보충 논거까지 selectable policy로 포함한 그룹도 있었다.

수정:

- 합쳐진 네 쟁점에서 10개 독립 policy card를 source/candidate별로 분리
- 중복 요약, 판례 설명, 보충 논거는 `context_only`로 재분류
- corpus 안에서 판례 방향이 확인되는 보호법익·경합·불법원인급여·권리행사는 실무
  규칙으로 확정
- 단순 분류 차이나 사실조건 차이는 policy가 아니라 RAG 또는 standard input으로 정리

### 사용자의 비용으로 remediation을 시도하려 함

위 57개 수정을 직접 해야 하는 상황에서 Terra patch runner와 prompt/schema를 먼저
작성했다. 실제 API 호출 전 사용자가 중단시켜 비용은 발생하지 않았지만, 에이전트의
작업 오류를 사용자의 API 예산으로 고치려 한 판단 자체가 잘못이었다. 추가 파일은 즉시
제거했고 worktree가 clean인 것을 확인한 뒤 모든 remediation을 직접 수행했다.

현재 remediation ledger, 전체 audit, policy queue에는 `api_calls: 0`을 명시하고
테스트로 고정했다. 앞으로 사용자가 명시적으로 승인하지 않은 remediation·재시도에는
API를 사용하지 않는다.

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
9. finding 판정, 실제 artifact 수정, 법률 정책 선택을 서로 다른 상태로 기록한다.
10. neural judgment 필요성과 사람의 법률검토 필요성을 같은 flag로 표현하지 않는다.
11. 에이전트의 오류 remediation 비용을 사용자 API 예산에 전가하지 않는다.

## 반성

이번 작업에서 비용이 큰 오류들은 모델의 성능 부족만으로 설명할 수 없다. 후보 계보,
분할 범위, retry 기록처럼 로컬 코드로 통제할 수 있는 부분을 API 호출 전에 충분히
검증하지 않은 책임이 있다. 특히 첫 분할 critic 오류는 입력과 선언 범위가 같은지
확인하는 단순한 테스트로 방지할 수 있었다.

앞으로는 “모델이 잘할 것”을 전제로 진행하지 않고, 누락·과병합·권위 상승·범위 누출이
발생해도 자동으로 멈추는 계약을 먼저 만든다. 법적 판단이 필요한 부분은 모델 출력으로
덮지 않고 사용자가 판례 인덱스와 실무 기준으로 결정할 검수 항목으로 남긴다.

이번 추가 오류는 계약이 있어도 상태의 의미를 정확히 설명하지 않고 다음 단계로
서두르면 사용자가 검수 범위를 오인한다는 점을 보여 주었다. 앞으로는 단계 전환 전에
`전체 대상 수 = 완료 + 제외 + 사용자 결정 필요`가 성립하는 표를 먼저 제시하고,
사용자 결정 필요 항목을 숨긴 채 일부 ready subset으로 다음 단계를 시작하지 않는다.
