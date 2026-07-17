# 사기죄 NormCard 법률 검수 가이드

## 현재 상태

- 범위: 형법 제347조 사기죄 주석서 13개 배치만 포함한다.
- 검증 후보 661개가 NormCard 646개에 연결되어 있다.
- Sol 최종 비평은 17개 묶음 전부 계약 검증을 통과했다.
- 검토 지적은 67개이며, 모든 산출물은 draft/legal_review=pending이다.
- 사용자 판정은 completed 67개, pending 0개다.
- 주석서가 보고한 판례로 추정되는 카드는 원판례 확인 전 context_only로 격리했다.

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

## 결정값

`fraud_human_review_decisions.jsonl`에서 각 review_id의 status를 completed로 바꾸고 decision을 기록한다.
허용 결정 예시는 approve_as_is, accept_finding_pending_remediation, correct_translation, narrow_proposition, reclassify_authority, set_context_only, group_variant, select_precedent_variant, reject_card, needs_more_source이다.
원판례를 확인한 경우 verified_authority_refs에 사용자의 판례 인덱스 식별자를 넣는다.

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
| general_object | 51 | 6 | 20 | 4 |
| deception | 211 | 25 | 110 | 11 |
| mistake_disposition | 70 | 5 | 15 | 6 |
| damage_acquisition | 56 | 8 | 11 | 11 |
| intent | 42 | 5 | 23 | 3 |
| special_forms | 101 | 8 | 68 | 0 |
| stages_participation | 49 | 3 | 9 | 1 |
| concurrence | 66 | 7 | 18 | 0 |

## RuleIR 게이트

- critic_pending: 0
- context_only_excluded: 274
- policy_choice_pending: 36
- human_review_pending: 0
- neural_grounding_spec_ready: 285
- provisional_rule_ir_ready: 51

승인된 critic 지적은 모두 반영되었지만, policy_variant의 active policy가 선택될 때까지 전체 RuleIR 생성과 최종 사기죄 결론을 모두 차단한다. 기존 8장짜리 모범 NormCard/RuleIR/Scallop은 구조 예시로만 유지한다.

## 파일

- 상세 검수 큐: `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- 결정 입력: `data/rulegen/fraud/fraud_human_review_decisions.jsonl`
- RuleIR readiness: `data/rulegen/fraud/fraud_rule_ir_readiness.json`
- Sol 원보고서: `data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final/`
