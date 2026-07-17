# 사기죄 정책 선택 검수 가이드

## 상태

- API 사용: 0회
- 전체 NormCard: 646개
- 자동 확정된 deterministic rule: 51개
- 자동 확정된 standard input: 285개
- RAG 전용: 274개
- 사용자 정책 선택: 12개 그룹, 36개 카드

기존 67개 critic finding은 모두 판정·수정 완료되었다. 아래에는 현재 corpus만으로 판례 우선 선택을 확정할 수 없는 쟁점만 남겼다.
각 결정은 `fraud_policy_review_decisions.jsonl`의 같은 review_id 행에 기록한다.
원판례 인덱스에서 확인한 식별자는 `verified_authority_refs`에 넣는다.

## 1. fraud_damage_acquisition.property_concept

- review_id: `fraud.policy.fraud_damage_acquisition.property_concept`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_damage_acquisition.property_concept_economic` | 경제적 재산개념은 재산의 법적 측면이 아닌 경제적 교환가치를 재산으로 파악한다. |
| `fraud_damage_acquisition.property_concept_legal` | 법률적 재산개념은 민법상 개인이 갖는 모든 권리와 의무를 재산으로 파악한다. |
| `fraud_damage_acquisition.property_concept_legal_economic` | 법률적·경제적 재산개념은 법익질서가 승인한 범위에서 개인이 가진 경제적 가치 있는 모든 재화를 재산으로 파악한다. |

## 2. fraud_damage_acquisition.property_loss_requirement

- review_id: `fraud.policy.fraud_damage_acquisition.property_loss_requirement`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_damage_acquisition.property_loss_affirmative_view` | 긍정설은 재물편취죄에서도 전체재산의 감소를 필요로 하고 손해와 이익 사이에 범인의 표상에 따른 소재의 동질성이 있어야 한다고 본다. |
| `fraud_damage_acquisition.property_loss_completion_view` | 긍정설에서도 재산상 손해 발생을 사기죄 성립요건보다 기수와 미수를 가르는 기준으로 이해해야 한다는 견해가 있다. |
| `fraud_damage_acquisition.property_loss_limited_affirmative_view` | 제한적 긍정설은 재물편취죄에서는 손해 발생을 요구하지 않지만 불법이득죄에서는 손해 발생을 요구한다고 본다. |
| `fraud_damage_acquisition.property_loss_negative_view` | 부정설은 재물편취와 불법이득의 모든 경우 재물의 교부 또는 재산상 이익 취득이 있으면 충분하고 피해자 손해 발생은 요구하지 않는다고 본다. |

## 3. fraud_damage_acquisition.property_risk_as_loss

- review_id: `fraud.policy.fraud_damage_acquisition.property_risk_as_loss`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_damage_acquisition.property_risk_card_property_negative` | 재산 위험을 재산상 손해로 보지 않는 견해 중에는 신용카드 자체가 형법상 재물에 해당하므로 그 편취 자체를 재산상 손해의 대상으로 보아야 한다는 견해가 있다. |
| `fraud_damage_acquisition.property_risk_credit_card_affirmative` | 재산 위험을 재산상 손해로 보는 긍정설은 지급 의사와 능력 없이 신용카드를 발급받으면 카드회사의 대금과 이자청구권이 위태로워져 재산상 손해가 된다고 본다. |
| `fraud_damage_acquisition.property_risk_prohibited_analogy_negative` | 재산 위험을 재산상 손해로 보는 해석은 법익 침해 또는 결과발생 요건을 해석으로 삭제하는 금지된 유추해석이라는 견해가 있다. |
| `fraud_damage_acquisition.property_risk_subsidiarity_negative` | 형법의 보충성을 중시하여 재산 위험만으로는 사기죄 성립을 부정하는 견해가 있다. |

## 4. fraud_deception.future_fact_scope

- review_id: `fraud.policy.fraud_deception.future_fact_scope`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `deception.fraud.variant.future-facts-limited` | 제한설은 순전히 장래에 속하는 상태나 사건은 기망 내용이 될 수 없으나, 과거 또는 현재 사실을 속여 장래 발생 사실의 판단을 그르치게 한 경우에는 장래 사실도 기망 내용이 될 수 있다고 본다. |
| `deception.fraud.variant.future-facts-negative` | 부정설은 기망 대상 사실은 존재 증명이 가능한 과거와 현재의 사실이므로 미래 사실은 포함될 수 없다고 본다. |
| `deception.fraud.variant.future-facts-unlimited` | 무제한설은 사실에 관한 착오이면 과거·현재 사실뿐 아니라 장래 사실도 기망의 내용이 될 수 있다고 본다. |

## 5. fraud_deception.omission_notice_duty_scope

- review_id: `fraud.policy.fraud_deception.omission_notice_duty_scope`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `deception.fraud.variant.guarantee-status-bases` | 상대방 착오를 방지해야 할 보증인적 지위의 발생근거로 법령ㆍ계약ㆍ선행행위를 드는 견해가 있다. |
| `deception.fraud.variant.notice-duty-good-faith-transaction` | 법률상 고지의무는 거래관념에 따라 신의성실 원칙으로 판단하고, 법령ㆍ계약ㆍ관습ㆍ조리에 의해 인정되며 구체적 사례의 거래실정과 신의성실 원칙에 따라 결정된다는 종래 다수설이 있다. |
| `deception.fraud.variant.notice-duty-special-trust-factors` | 계약만으로 보증인적 지위가 생기는 것은 아니고, 일정 사유 고지가 계약 내용이 된 경우 또는 특수한 신뢰관계를 전제로 한 신의칙상 고지의무가 있는 경우에 한정하며, 현저한 손해ㆍ상대방에게의 중요성ㆍ상대방의 무경험을 종합하여 판단한다는 견해가 있다. |
| `deception.fraud.variant.prior-conduct-notice-duty` | 고의적이지 않은 선행행위로 착오가 유발되고, 그 착오를 통해 피기망자의 재산상 처분행위에 위험이 야기되는 경우 선행행위로 인한 고지의무가 인정된다는 견해가 있다. |
| `deception.fraud.variant.real-estate-notice-duty-explicit-duty` | 부동산거래에서는 법률이나 계약에 신의성실을 넘는 명시적 작위의무 규정이 있어야 사기죄가 성립한다는 견해가 있다. |

## 6. fraud_deception.opinion_statement

- review_id: `fraud.policy.fraud_deception.opinion_statement`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `deception.fraud.variant.opinion-statement-affirmative` | 적극설은 사실에 관한 기망에는 가치판단에 관한 기망도 포함되며 의견 진술도 기망의 내용이 된다고 본다. |
| `deception.fraud.variant.opinion-statement-mistake-sufficiency` | 제3설은 사실표시와 가치판단·의견표시를 구별하지 않고, 허위 표시가 타인을 착오에 빠지게 하기에 충분한지에 따라 기망 여부를 판단한다. |
| `deception.fraud.variant.opinion-statement-negative` | 소극설은 가치판단이나 기타 의견의 표시는 사실에 관한 거짓말이 아니므로 사기죄 구성요건으로서의 기망에 해당하지 않는다고 본다. |

## 7. fraud_general_object.property_value

- review_id: `fraud.policy.fraud_general_object.property_value`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_general_object.property_value_exchange_required` | 사기죄의 객체인 재물은 교환가치가 있는 재물에 한정된다는 견해가 있다. |
| `fraud_general_object.property_value_subjective_sufficient` | 행위자에게 주관적 가치만 있는 물건도 사기죄의 객체인 재물이 될 수 있다는 견해가 있다. |

## 8. fraud_general_object.sex_work_contract

- review_id: `fraud.policy.fraud_general_object.sex_work_contract`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `general_object.fraud.variant.sex-work-contract-fraud-affirmative` | 성매매 계약이 민법상 무효라도 성매매 의사 또는 금전 지급 의사 없이 상대방을 기망한 경우 사기죄가 성립한다는 긍정설이 있다. |
| `general_object.fraud.variant.sex-work-contract-fraud-negative` | 성매매 관련 사취 이익은 법률상 보호받을 수 없어 재산 침해가 없으므로 사기죄가 성립하지 않는다는 부정설이 있다. |

## 9. fraud_intent.illegal_appropriation_requirement

- review_id: `fraud.policy.fraud_intent.illegal_appropriation_requirement`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_intent.illegal_appropriation_not_required` | 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하지 않다는 견해가 있다. |
| `fraud_intent.illegal_appropriation_required_all` | 재물편취죄와 불법이득죄를 구별하지 않고 모두 불법영득의사가 필요하다는 견해가 있다. |
| `fraud_intent.illegal_appropriation_required_property_only` | 재물편취죄와 불법이득죄를 구별하여 재물편취죄에는 불법영득의사가 필요하지만 불법이득죄에는 필요하지 않다는 견해가 있다. |

## 10. fraud_mistake.disposition_intent_requirement

- review_id: `fraud.policy.fraud_mistake.disposition_intent_requirement`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `mistake_disposition.fraud.variant.disposition-intent-compromise` | 절충설은 재산상 이익 취득의 경우 처분의사가 필요 없지만, 재물 교부의 경우에는 절도죄와 구별하기 위하여 처분의사가 필요하다고 본다. |
| `mistake_disposition.fraud.variant.disposition-intent-unnecessary` | 소극설은 객관적으로 손해를 초래할 수 있는 행위이면 충분하고 처분의사는 필요하지 않다고 본다. |

## 11. fraud_mistake.triangular_fraud_authority

- review_id: `fraud.policy.fraud_mistake.triangular_fraud_authority`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_mistake.triangular_fraud_causation_theory` | 인과관계설은 삼각사기에서 피기망자의 처분과 행위자의 이득 사이에 인과관계가 있으면 충분하다고 본다. |
| `fraud_mistake.triangular_fraud_contractual_authority` | 계약관계설은 처분행위자가 계약관계에 따라 피해자의 재산을 처분할 권한을 가져야 한다고 본다. |
| `fraud_mistake.triangular_fraud_factual_position` | 사실상 지위설은 처분행위자가 타인의 재산을 사실상 처분할 수 있는 지위에 있으면 충분하다고 본다. |
| `fraud_mistake.triangular_fraud_legal_authority` | 법적 권한설은 처분행위자에게 법률·계약 또는 최소한 묵시적 위임에 따른 피해자 재산 처분권한이 있어야 한다고 본다. |

## 12. fraud_stages_participation.completion_threshold

- review_id: `fraud.policy.fraud_stages_participation.completion_threshold`
- 현재 corpus의 직접 판례 근거: 없음
- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재

| card_id | 선택지 |
|---|---|
| `fraud_stages_participation.victim_loss_completion_view` | 피해자에게 재산상 손해가 발생하면 행위자가 불법이득을 취득하지 않았더라도 사기죄가 기수에 이른다는 견해가 있다. |
