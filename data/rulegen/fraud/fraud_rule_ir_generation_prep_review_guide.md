# 사기죄 전체 RuleIR 생성 준비 검수

## 현재 상태

- API 사용: 0회
- agent preflight: 완료
- 사용자 결정: pending=10
- Terra 실행: 사용자 승인 전 차단
- 입력 core: deterministic 28개 + standard 60개 = 88개
- 제외 context: 558개
- 생성 단위: 전체 RuleIR 단일 호출 1회

## 에이전트 검토 결론

1. 모듈 분할은 서로 다른 card_set_id와 교차 predicate 병합 오류를 만들므로 단일 호출이 낫다.
2. 기존 8장 exemplar의 손해·불법영득의사 policy는 현재 결정과 달라 법리 few-shot에서 제외했다.
3. 현재 2장 few-shot은 status, provable, actor role 구조만 보여 준다.
4. 60개 standard는 satisfied/not_satisfied/unknown을 명시적으로 입력받는다.
5. 28개 deterministic 카드는 최소 한 개의 실제 rule에서 소비되어야 한다.
6. RuleIR 생성 후 제가 전 규칙을 검토하고 장문 자연어 설명을 작성하기 전에는 사용자 검수로 넘기지 않는다.
7. 그 사용자 검수 뒤에만 Sol을 호출하고, Sol 지적도 다시 사람에게 공개한다.

## 사용자 검수 항목

| ID | 주제 | 제안 | 에이전트 의견 |
|---|---|---|---|
| `fraud.rule_ir.prep.scope` | core_scope | 사용자 검수 완료된 88개만 RuleIR 입력으로 사용하고 558개 RAG는 제외한다. | approve |
| `fraud.rule_ir.prep.single_call` | generation_unit | aggregate NormCardSet 전체를 Terra 단일 호출로 생성한다. | approve |
| `fraud.rule_ir.prep.standard_state` | standard_assessment_state | standard 결과를 satisfied, not_satisfied, unknown의 명시적 3상태로 받는다. | approve |
| `fraud.rule_ir.prep.evidence_gate` | evidence_gate | 모든 commentary input은 같은 case_id와 assessment_id의 provable을 함께 요구한다. | approve |
| `fraud.rule_ir.prep.actor_roles` | actor_role_signature | 피고인, 피기망자, 처분자, 재산소유자, 객체, 수익자를 별도 인자로 유지한다. | approve |
| `fraud.rule_ir.prep.outputs` | result_interface | 성립, 불성립, undetermined, conflict를 별도 derived predicate로 출력한다. | approve |
| `fraud.rule_ir.prep.open_world` | open_world_policy | 생성 RuleIR에서는 negation을 금지하고 negative·exception을 명시적 조건으로 표현한다. | approve |
| `fraud.rule_ir.prep.fewshot` | fewshot_policy | 기존 8장 법리 대신 현재 상태·증거게이트 계약만 보여 주는 2장 구조 예시를 제공한다. | approve |
| `fraud.rule_ir.prep.review_sequence` | review_sequence | Terra 후 에이전트 검토·장문 자연어 설명, 사용자 검토, Sol, 사용자 재검토, Scallop 순서로 진행한다. | approve |
| `fraud.rule_ir.prep.api_ceiling` | api_execution_ceiling | Terra 1회, 동시성 1, retry 0, max completion 64000으로 제한한다. | approve |

승인·수정 의견은 이 가이드의 항목 ID 기준으로 전달하면 에이전트가 `fraud_rule_ir_generation_prep_review_decisions.jsonl`에 반영한다.

## 생성 후 사용자에게 제공할 묶음

- 원본 전체 RuleIR JSON
- 로컬 validator 결과와 88장 coverage 표
- 에이전트의 규칙별 장문 자연어 설명
- 성립·불성립·unknown·conflict 도출 경로
- 남은 구조·법률 질문
- 각 standard에 필요한 positive·opposing·missing feature와 RAG 검색 시점
- 삼각사기 역할 인자와 일반 사기에서 동일 인물 ID를 재사용하는 방식

## 파일

- aggregate core: `data/rulegen/fraud/fraud_core_norm_card_set.json`
- Terra payload: `data/rulegen/fraud/fraud_full_rule_ir_generation_request.json`
- 구조 few-shot: `data/rulegen/fraud/fraud_rule_ir_generation_fewshot.json`
- 준비 manifest: `data/rulegen/fraud/fraud_rule_ir_generation_prep_manifest.json`
- 결정 파일: `data/rulegen/fraud/fraud_rule_ir_generation_prep_review_decisions.jsonl`
