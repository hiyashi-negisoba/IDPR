# 사기죄 NormCard 법률 검수 가이드

## 현재 상태

- 범위: 형법 제347조 사기죄 주석서 13개 배치만 포함한다.
- 검증 후보 661개가 NormCard 646개에 연결되어 있다.
- Sol 최종 비평은 17개 묶음 전부 계약 검증을 통과했다.
- 검토 지적 67개는 모두 판정·remediation 완료되었고, core 법률검수만 pending이다.
- 사용자 판정은 completed 67개, pending 0개다.
- 정책 쟁점에 직접 관련된 로컬 원판례 15건은 확인했고, 나머지 구체 적용례는 RAG context로 격리했다.

## 지적-카드 매핑

- Sol 보고서의 `target_path` 숫자 인덱스는 제출 배열과 일관되게 대응하지 않아 검수 대상으로 직접 사용하지 않는다.
- 숫자 경로가 있던 40개 지적은 지적 문구, source_refs, 카드 proposition을 대조하여 카드 ID로 고정했다.
- 검수할 실제 대상은 각 항목의 `impacted_card_ids`와 `impacted_cards`이며, 매핑 근거는 `card_mapping`에 기록했다.
- `legal_review_questions` 지적은 질문을 생성한 카드와 원 질문을 `card_mapping.review_question`에 표시한다.
- 이후 미등록 숫자 경로가 추가되면 큐 생성은 추측하지 않고 실패한다.

## Source entailment 판정

- 카드의 source quote는 provenance용 정확 인용구이지 해당 chunk의 유일한 의미 범위가 아니다.
- source_entailment 지적은 같은 comment_id의 전체 document_text까지 대조한다.
- 이번 8건 중 7건은 전체 chunk가 해당 문구를 명시하여 기각했고, 제3자 취득형 번역 오류 1건만 수정했다.

## 검수 순서

1. 출처 의미: source_entailment, overgeneralization, missing_norm, source_scope를 먼저 본다.
2. 권위: commentary_reported_precedent 여부와 원판례의 실제 법리를 판례 인덱스로 확인한다.
3. 형식화: deterministic_rule, standard_input, context_only 구분을 확인한다.
4. 학설 대립: 같은 쟁점의 variant_group을 묶고 실무상 판례 입장을 선택한다.
5. 승인된 카드만 RuleIR로 내린다. 미확인 사실이나 반대사실은 unknown으로 유지한다.

## Critic 결정 기록

`fraud_human_review_decisions.jsonl`의 67개 행은 완료된 critic 판정 기록이므로 추가 입력 대상이 아니다. 현재 사용자 검수는 `fraud_core_rule_review_decisions.jsonl`에서 수행한다.

## 지적 분포

| 유형 | 건수 |
|---|---:|
| authority_mismatch | 25 |
| collapsed_variant | 17 |
| formalization_error | 9 |
| missing_variant | 1 |
| other | 3 |
| overgeneralization | 3 |
| source_entailment | 8 |
| source_scope | 1 |

## 모듈별 우선순위

| 모듈 | 카드 | 지적 | context_only | policy_variant |
|---|---:|---:|---:|---:|
| general_object | 51 | 6 | 40 | 0 |
| deception | 211 | 25 | 173 | 0 |
| mistake_disposition | 70 | 5 | 46 | 0 |
| damage_acquisition | 56 | 8 | 47 | 0 |
| intent | 42 | 5 | 34 | 0 |
| special_forms | 101 | 8 | 84 | 0 |
| stages_participation | 49 | 3 | 38 | 0 |
| concurrence | 66 | 7 | 66 | 0 |

## RuleIR 게이트

- critic_pending: 0
- context_only_excluded: 528
- policy_choice_pending: 0
- neural_grounding_spec_candidate: 89
- provisional_rule_ir_candidate: 29
- core_rule_review_pending: 118

승인된 critic 지적과 판례 우선 정책 정리는 모두 반영되었다. 다만 deterministic rule과 standard input 후보 전부에 대한 사용자 검수 전에는 전체 RuleIR 생성을 차단한다. 기존 8장짜리 모범 NormCard/RuleIR/Scallop은 구조 예시로만 유지한다.

## 파일

- 상세 검수 큐: `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- 결정 입력: `data/rulegen/fraud/fraud_human_review_decisions.jsonl`
- RuleIR readiness: `data/rulegen/fraud/fraud_rule_ir_readiness.json`
- core 검수 큐: `data/rulegen/fraud/fraud_core_rule_review_queue.json`
- core 결정 입력: `data/rulegen/fraud/fraud_core_rule_review_decisions.jsonl`
- Sol 원보고서: `data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final/`
