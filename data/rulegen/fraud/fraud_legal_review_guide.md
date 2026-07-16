# 사기죄 NormCard 법률 검수 가이드

## 현재 상태

- 범위: 형법 제347조 사기죄 주석서 13개 배치만 포함한다.
- 검증 후보 662개가 NormCard 636개에 중복 없이 연결되어 있다.
- Sol 최종 비평은 17개 묶음 전부 계약 검증을 통과했다.
- 검토 지적은 67개이며, 모든 산출물은 draft/legal_review=pending이다.
- 주석서가 보고한 판례로 추정되는 카드는 원판례 확인 전 context_only로 격리했다.

## 검수 순서

1. 출처 의미: source_entailment, overgeneralization, missing_norm, source_scope를 먼저 본다.
2. 권위: commentary_reported_precedent 여부와 원판례의 실제 법리를 판례 인덱스로 확인한다.
3. 형식화: deterministic_rule, standard_input, context_only 구분을 확인한다.
4. 학설 대립: 같은 쟁점의 variant_group을 묶고 실무상 판례 입장을 선택한다.
5. 승인된 카드만 RuleIR로 내린다. 미확인 사실이나 반대사실은 unknown으로 유지한다.

## 결정값

`fraud_human_review_decisions.jsonl`에서 각 review_id의 status를 completed로 바꾸고 decision을 기록한다.
허용 결정 예시는 approve_as_is, narrow_proposition, reclassify_authority, set_context_only, group_variant, select_precedent_variant, reject_card, needs_more_source이다.
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
| general_object | 45 | 6 | 10 | 9 |
| deception | 211 | 25 | 54 | 18 |
| mistake_disposition | 66 | 5 | 10 | 9 |
| damage_acquisition | 56 | 8 | 2 | 18 |
| intent | 42 | 5 | 22 | 4 |
| special_forms | 101 | 8 | 64 | 5 |
| stages_participation | 49 | 3 | 9 | 0 |
| concurrence | 66 | 7 | 8 | 4 |

## RuleIR 게이트

- critic_pending: 168
- context_only_excluded: 127
- policy_choice_pending: 43
- human_review_pending: 237
- provisional_rule_ir_ready: 61

현재 전체 RuleIR 생성은 차단되어 있다. 기존 8장짜리 사기죄 모범 NormCard/RuleIR/Scallop은 구조 예시로만 유지하며, 636장 전체에 대한 법적 승인으로 간주하지 않는다.

## 파일

- 상세 검수 큐: `data/rulegen/fraud/fraud_norm_card_review_queue.json`
- 결정 입력: `data/rulegen/fraud/fraud_human_review_decisions.jsonl`
- RuleIR readiness: `data/rulegen/fraud/fraud_rule_ir_readiness.json`
- Sol 원보고서: `data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final/`
