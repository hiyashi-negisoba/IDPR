# 사기죄 Scallop core 검수 가이드

## 범위

- API 사용: 0회
- deterministic rule 검수 후보: 28개
- standard input 검수 후보: 60개
- RAG/future-work context: 558개
- 현재 unresolved: 0개

사용자 라벨과 잔여 항목 교차검토가 모두 반영되었다. 원래 118개에 대한 판정·변경 근거는 `fraud_core_rule_human_review_audit.json`에 보존한다.

## Deterministic Rules

| module | card_id | proposition |
|---|---|---|
| deception | `deception.fraud.causal-link.deception-property-disposition` | 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. |
| deception | `deception.fraud.causal-link.no-disposition-no-deception` | 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. |
| deception | `deception.fraud.definition.deceived-person-unspecified` | 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. |
| deception | `deception.fraud.definition.deceived-person-victim-distinct` | 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. |
| deception | `deception.fraud.definition.deception-counterparty-is-other` | 사기죄에서 기망의 상대방은 타인이다. |
| deception | `deception.fraud.definition.deception-means-unrestricted` | 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. |
| deception | `deception.fraud.definition.notice-duty-violation-omission` | 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. |
| deception | `deception.fraud.definition.other-includes-corporation` | 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. |
| deception | `deception.fraud.element.deception-must-create-false-belief` | 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. |
| deception | `deception.fraud.element.deception-not-legal-act-important-part` | 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. |
| deception | `deception.fraud.element.omission-deception-independent-error` | 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. |
| deception | `deception.fraud.element.omission-deception-legal-notice-duty` | 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. |
| deception | `deception.fraud.element.victim-negligence-no-bar` | 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. |
| damage_acquisition | `fraud_damage_acquisition.property_concept_reported_precedent` | 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. |
| damage_acquisition | `fraud_damage_acquisition.property_loss_negative_view` | 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. |
| general_object | `fraud_general_object.causation_required` | 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. |
| intent | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. |
| mistake_disposition | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. |
| mistake_disposition | `fraud_mistake.factual_act_disposition` | 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. |
| mistake_disposition | `fraud_mistake.invalid_act_disposition` | 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. |
| mistake_disposition | `fraud_mistake.property_disposition_element` | 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. |
| mistake_disposition | `fraud_mistake.property_limited_disposition` | 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. |
| mistake_disposition | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. |
| mistake_disposition | `fraud_mistake.triangular_fraud_definition` | 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. |
| stages_participation | `fraud_stages_participation.attempt_deceptive_act` | 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. |
| stages_participation | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. |
| stages_participation | `fraud_stages_participation.no_causation_attempt` | 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. |
| stages_participation | `fraud_stages_participation.property_fraud_completion_control` | 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. |

## Standard Inputs

| module | card_id | proposition |
|---|---|---|
| deception | `deception.fraud.causal-link.loan-purpose-not-sole-trigger` | 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. |
| deception | `deception.fraud.definition.deception-content-basis-fact` | 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. |
| deception | `deception.fraud.definition.deception-good-faith-mistake` | 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. |
| deception | `deception.fraud.definition.deception-object-facts` | 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. |
| deception | `deception.fraud.definition.deception-target-human` | 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. |
| deception | `deception.fraud.definition.exploitation-existing-mistake` | 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. |
| deception | `deception.fraud.definition.implicit-deception` | 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. |
| deception | `deception.fraud.element.loan-no-repayment-intent-or-ability` | 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. |
| deception | `deception.fraud.element.omission-deception-guarantor-equivalence` | 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. |
| deception | `deception.fraud.element.transaction-purpose-no-impairment` | 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. |
| deception | `deception.fraud.standard.advertising-important-concrete-falsehood` | 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. |
| deception | `deception.fraud.standard.advertising-tolerable-exaggeration` | 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. |
| deception | `deception.fraud.standard.deception-concrete-circumstances` | 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. |
| deception | `deception.fraud.standard.easily-detectable-lie` | 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. |
| deception | `deception.fraud.standard.implicit-deception-explanatory-value` | 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. |
| deception | `deception.fraud.standard.implicit-omission-deception-distinction` | 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. |
| deception | `deception.fraud.standard.intent-to-defraud-loan-inference` | 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. |
| deception | `deception.fraud.standard.loan-lender-anticipated-risk` | 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. |
| deception | `deception.fraud.standard.loan-purpose-materiality` | 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. |
| deception | `deception.fraud.standard.loan-subsequent-default` | 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. |
| deception | `deception.fraud.standard.precedent-notice-duty-materiality` | 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. |
| deception | `deception.fraud.standard.vague-opinion-not-deception` | 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. |
| damage_acquisition | `fraud_damage_acquisition.delivery_factual_control` | 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. |
| damage_acquisition | `fraud_damage_acquisition.delivery_of_property` | 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. |
| damage_acquisition | `fraud_damage_acquisition.money_delivery_full_amount` | 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. |
| damage_acquisition | `fraud_damage_acquisition.property_disposition_types` | 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. |
| damage_acquisition | `fraud_damage_acquisition.protected_economic_interest` | 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. |
| damage_acquisition | `fraud_damage_acquisition.right_exercise_unacceptable_deception` | 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. |
| damage_acquisition | `fraud_damage_acquisition.subsequent_return_irrelevant` | 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. |
| general_object | `fraud_general_object.deception_error_causation` | 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. |
| intent | `fraud_intent.contract_breach_distinction` | 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. |
| intent | `fraud_intent.illegal_appropriation_definition` | 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. |
| intent | `fraud_intent.precedent_illegal_appropriation_intent` | 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. |
| intent | `fraud_intent.third_party_acquisition` | 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. |
| intent | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. |
| mistake_disposition | `fraud_mistake.conscious_nonexercise` | 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. |
| mistake_disposition | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. |
| mistake_disposition | `fraud_mistake.disposition_directness` | 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. |
| mistake_disposition | `fraud_mistake.disposition_intent_act_awareness` | 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. |
| mistake_disposition | `fraud_mistake.disposition_omission` | 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. |
| mistake_disposition | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. |
| mistake_disposition | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. |
| mistake_disposition | `fraud_mistake.error_doubt_ignorance` | 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. |
| mistake_disposition | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. |
| mistake_disposition | `fraud_mistake.no_capacity_theft` | 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. |
| mistake_disposition | `fraud_mistake.no_thought_no_error` | 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. |
| mistake_disposition | `fraud_mistake.omission_not_all_nonclaims` | 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. |
| mistake_disposition | `fraud_mistake.trick_theft_directness` | 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. |
| mistake_disposition | `fraud_mistake.unaware_error` | 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. |
| general_object | `general_object.fraud.definition.property-benefit` | 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. |
| general_object | `general_object.fraud.definition.property-benefit-not-numerically-limited` | 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. |
| general_object | `general_object.fraud.element.object-other-possessed-other-property` | 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. |
| general_object | `general_object.fraud.element.property-benefit-concrete` | 재산상 이익은 구체적인 이익이어야 한다. |
| general_object | `general_object.fraud.exception.public-interest-property-equivalence` | 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. |
| general_object | `general_object.fraud.standard.later-cancellation-no-effect` | 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. |
| general_object | `general_object.fraud.standard.own-possession-other-property-embezzlement` | 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. |
| general_object | `general_object.fraud.standard.own-property-not-object` | 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. |
| general_object | `general_object.fraud.standard.public-interest-only-no-fraud` | 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. |
| mistake_disposition | `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation` | 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. |
| special_forms | `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime` | 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. |
