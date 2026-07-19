# 사기죄 Paraphrase 5건 카드별 적용 검토표

## 검토 방법

이 표는 이미 승인된 법리 카드의 문구를 다시 검수하는 표가 아니라, 각 사건 사실에
그 카드가 어떻게 적용되는지를 정하는 표다. `성립 경로 요구`는 사기죄 성립 branch가
통과하려면 필요한 상태일 뿐 사건의 정답을 미리 표시한 것이 아니다.

`사용자 판정`에는 `S`(충족), `NS`(불충족), `U`(미확인), `EDIT`(카드·계획 수정 필요)
중 하나를 적는다. `U`가 하나라도 남으면 닫힌 사건에서 Scallop은 성립을 확정하지 않는다.

4번 사건은 ‘아직 생산하지 않았다’는 객관적 사실과 ‘이미 생산하고 있다’는 A의 말을
명시적으로 대비하도록 수정했다. 1번 사건 문구는 변경하지 않았다.

## 1. 차용 당시 변제 의사·능력

- 사건 ID: `manual_fraud_046_01_loan_repayment`
- 계획: `loan_repayment_property`
- 사건 사실: A는 일정한 직업과 정기적인 수입이 없었고, 당시 2천만 원 상당의 채무를 부담하고 있었으며 별도로 확인되는 재산도 없었다. A는 2021년 어느 날 B의 집에서 B에게 1천만 원을 빌려주면 매월 3%의 이자를 지급하고 두 달 뒤 원금을 갚겠다고 말했다. B는 그 말을 듣고 같은 자리에서 A에게 1천만 원을 건넸다.

### 사기죄의 객체와 대상 거래의 역할 구조

검토 질문: B가 A에게 1천만 원을 빌려준 차용 거래에서 재물 객체와 역할 구조가 충족되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C1-01 | `general_object.fraud.element.object-other-possessed-other-property` | 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. | 충족 |  |  |
| C1-02 | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. | 충족 |  |  |

### 차용 당시 변제 의사·능력에 관한 기망

검토 질문: A의 차용 당시 변제 의사 또는 능력에 관한 표시가 처분의 판단 기초를 왜곡했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C1-03 | `deception.fraud.element.loan-no-repayment-intent-or-ability` | 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. | 충족 |  |  |

### 착오와 재산적 처분행위

검토 질문: 변제 가능성에 관한 착오가 B의 재산적 처분을 유발했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C1-04 | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. | 충족 |  |  |
| C1-05 | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | 충족 |  |  |
| C1-06 | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | 충족 |  |  |

### 인과관계, 재물 취득과 기수

검토 질문: 기망·착오·처분·교부가 순차적으로 이어져 취득과 기수가 인정되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C1-07 | `fraud_damage_acquisition.delivery_of_property` | 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. | 충족 |  |  |
| C1-08 | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | 충족 |  |  |
| C1-09 | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | 충족 |  |  |

### 편취의 범의와 재산적 이득 목적

검토 질문: 객관적 사정을 종합할 때 A의 행위 당시 편취 범의와 처분 유도 의사가 인정되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C1-10 | `deception.fraud.standard.intent-to-defraud-loan-inference` | 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. | 충족 |  |  |
| C1-11 | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. | 충족 |  |  |
| C1-12 | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | 충족 |  |  |
| C1-13 | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | 불충족 |  |  |

**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`

**사건 메모:**

## 2. 변제기 연장과 재산상 이익

- 사건 ID: `manual_fraud_047_01_loan_extension`
- 계획: `loan_extension_benefit`
- 사건 사실: A는 3년 전 B에게서 연 8%의 이자로 5천만 원을 빌렸다. 변제기가 다가왔을 때 A는 직업과 별다른 수입이 없었고 가족의 채무 때문에 매월 100만 원 이상을 지출하고 있었다. A는 2020년 8월 3일 B에게 변제기를 6개월 미뤄주면 이자를 포함해 갚겠다고 말했다. B는 이를 받아들여 원금의 변제기를 6개월 연장하였다.

### 구체적 재산상 이익과 역할 구조

검토 질문: B가 A의 5천만 원 채무 변제기를 6개월 연장한 거래가 구체적인 재산상 이익을 부여하는 처분인가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C2-01 | `general_object.fraud.definition.property-benefit` | 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. | 충족 |  |  |
| C2-02 | `general_object.fraud.element.property-benefit-concrete` | 재산상 이익은 구체적인 이익이어야 한다. | 충족 |  |  |
| C2-03 | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. | 충족 |  |  |

### 변제 의사·능력에 관한 기망

검토 질문: 변제기 연장을 요청할 당시의 변제 의사 또는 능력에 관한 표시가 기망에 해당하는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C2-04 | `deception.fraud.element.loan-no-repayment-intent-or-ability` | 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. | 충족 |  |  |

### 착오와 이익 부여 처분

검토 질문: 착오가 B의 변제기 연장 처분을 유발했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C2-05 | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. | 충족 |  |  |
| C2-06 | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | 충족 |  |  |
| C2-07 | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | 충족 |  |  |

### 재산상 이익 취득, 인과관계와 기수

검토 질문: 기망에서 변제기 연장과 이익 취득까지 순차적 인과관계가 인정되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C2-08 | `fraud_damage_acquisition.property_concept_reported_precedent` | 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. | 충족 |  |  |
| C2-09 | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | 충족 |  |  |
| C2-10 | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | 충족 |  |  |

### 편취의 범의와 재산적 이득 목적

검토 질문: A에게 연장 처분을 유도해 재산상 이익을 얻을 목적과 범의가 있었는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C2-11 | `deception.fraud.standard.intent-to-defraud-loan-inference` | 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. | 충족 |  |  |
| C2-12 | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. | 충족 |  |  |
| C2-13 | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | 충족 |  |  |
| C2-14 | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | 불충족 |  |  |

**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`

**사건 메모:**

## 3. 무전취식과 묵시적 기망

- 사건 ID: `manual_fraud_050_01_unpaid_dining`
- 계획: `implicit_service_benefit`
- 사건 사실: A는 일정한 직업이나 별다른 재산이 없었고, 현금·신용카드 등 결제수단을 가지고 있지 않았다. A는 2008년 11월 9일 저녁 B가 운영하는 주점에 들어가 술과 안주를 주문하였다. B는 A의 주문에 따라 5만 2천 원 상당의 술과 안주를 제공했고, A는 이를 먹은 뒤 대금을 지급하지 않았다.

### 서비스 이용 이익과 역할 구조

검토 질문: 제공받은 서비스가 구체적 재산상 이익이고 역할 구조가 충족되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C3-01 | `general_object.fraud.definition.property-benefit` | 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. | 충족 |  |  |
| C3-02 | `general_object.fraud.element.property-benefit-concrete` | 재산상 이익은 구체적인 이익이어야 한다. | 충족 |  |  |
| C3-03 | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. | 충족 |  |  |

### 행동에 의한 묵시적 기망

검토 질문: A의 주문·이용 행동이 대금을 지급할 의사가 있다는 표시로 이해될 설명가치를 가지는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C3-04 | `deception.fraud.standard.implicit-deception-explanatory-value` | 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. | 충족 |  |  |

### 착오와 서비스 제공 처분

검토 질문: 대금 지급에 관한 착오가 B의 서비스 제공을 유발했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C3-05 | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. | 충족 |  |  |
| C3-06 | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | 충족 |  |  |
| C3-07 | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | 충족 |  |  |

### 서비스 이익 취득, 인과관계와 기수

검토 질문: 묵시적 표시에서 서비스 제공과 이익 취득까지 인과관계가 이어지는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C3-08 | `fraud_damage_acquisition.property_concept_reported_precedent` | 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. | 충족 |  |  |
| C3-09 | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | 충족 |  |  |
| C3-10 | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | 충족 |  |  |

### 편취의 범의와 재산적 이득 목적

검토 질문: 서비스를 제공받을 당시 A에게 대금을 지급할 의사가 없었고, 그 상태에서 B의 제공 처분을 유도할 의사가 있었는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C3-11 | `fraud_intent.contract_breach_distinction` | 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. | 충족 |  |  |
| C3-12 | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. | 충족 |  |  |
| C3-13 | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | 충족 |  |  |
| C3-14 | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | 불충족 |  |  |

**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`

**사건 메모:**

## 4. 전선 공급계약의 계약금

- 사건 ID: `manual_fraud_052_01_supply_deposit`
- 계획: `ordinary_contract_property`
- 사건 사실: A는 전선 회사의 대표이사였다. 회사는 당시 공급 대상 전선을 아직 생산하지 않은 상태였다. A는 2021년 어느 날 회사 사무실에서 B에게 회사가 해저케이블용 전선을 이미 생산하고 있고, 그 전선은 해저케이블 분야에서 세계 최고 수준이며 공급 요청도 많다고 말했다. 또한 계약금을 먼저 지급하면 B에게 우선 공급하겠다고 말했다. B는 그 말을 듣고 전선 공급계약의 계약금으로 A 측에 1억 원을 지급하였다.

### 계약금의 재물 객체와 역할 구조

검토 질문: B가 A 측에 전선 공급계약금 1억 원을 지급한 거래에서 계약금 교부와 역할 구조가 충족되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C4-01 | `general_object.fraud.element.object-other-possessed-other-property` | 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. | 충족 |  |  |
| C4-02 | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. | 충족 |  |  |

### 계약 이행 의사·능력에 관한 기망

검토 질문: 장래 급부의 이행 의사 또는 능력에 관한 표시가 계약금 처분을 유발한 기망인가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C4-03 | `deception.fraud.definition.deception-good-faith-mistake` | 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. | 충족 |  |  |
| C4-04 | `deception.fraud.causal-link.deception-property-disposition` | 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. | 충족 |  |  |

### 착오와 계약금 교부 처분

검토 질문: 이행 가능성에 관한 착오가 B의 계약금 교부를 유발했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C4-05 | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. | 충족 |  |  |
| C4-06 | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | 충족 |  |  |
| C4-07 | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | 충족 |  |  |

### 계약금 취득, 인과관계와 기수

검토 질문: 계약상 표시에서 계약금 교부와 취득까지 순차적 인과관계가 인정되는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C4-08 | `fraud_damage_acquisition.delivery_of_property` | 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. | 충족 |  |  |
| C4-09 | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | 충족 |  |  |
| C4-10 | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | 충족 |  |  |

### 계약 당시 편취의 범의

검토 질문: 계약 당시 A의 고의가 단순한 사후 채무불이행을 넘어서는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C4-11 | `fraud_intent.contract_breach_distinction` | 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. | 충족 |  |  |
| C4-12 | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. | 충족 |  |  |
| C4-13 | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | 충족 |  |  |
| C4-14 | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | 불충족 |  |  |

**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`

**사건 메모:**

## 5. 택배물 삼각사기

- 사건 ID: `manual_fraud_063_01_parcel_triangular`
- 계획: `triangular_property_delivery`
- 사건 사실: A와 B는 서로 모르는 사이였다. 건물 경비원 C는 2019년 12월 10일 안내데스크에서 B 앞으로 온 택배물을 보관하고 있었다. A는 C에게 B가 자신의 직원인 것처럼 말하면서 B 앞으로 온 택배물을 달라고 요청하였다. C는 그 말을 듣고 10만 원 상당의 의류와 장신구가 들어 있는 B의 택배물을 A에게 건넸다.

### 삼각사기의 객체와 역할 구조

검토 질문: C의 처분 지위와 B의 재산 피해를 연결할 수 있는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C5-01 | `general_object.fraud.element.object-other-possessed-other-property` | 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. | 충족 |  |  |
| C5-02 | `fraud_mistake.deceived_disposer_identity` | 피기망자와 처분행위자는 동일인이어야 한다. | 충족 |  |  |
| C5-03 | `deception.fraud.definition.deceived-person-victim-distinct` | 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. | 충족 |  |  |
| C5-04 | `fraud_mistake.triangular_fraud_definition` | 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. | 충족 |  |  |
| C5-05 | `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation` | 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. | 충족 |  |  |

### 처분자를 향한 기망

검토 질문: A의 표시가 C의 재산적 처분판단을 향한 기망인가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C5-06 | `deception.fraud.definition.deception-good-faith-mistake` | 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. | 충족 |  |  |
| C5-07 | `deception.fraud.causal-link.deception-property-disposition` | 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. | 충족 |  |  |

### 피기망자의 착오와 재산적 처분행위

검토 질문: 착오가 C의 재물 교부를 유발했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C5-08 | `fraud_mistake.error_definition` | 착오란 사실과 일치하지 않는 인식을 의미한다. | 충족 |  |  |
| C5-09 | `fraud_mistake.error_disposition_motivation` | 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | 충족 |  |  |
| C5-10 | `fraud_mistake.disposition_definition` | 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | 충족 |  |  |

### 재물 취득, 인과관계와 기수

검토 질문: 기망·착오·처분·교부가 이어져 A가 재물을 취득했는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C5-11 | `fraud_damage_acquisition.delivery_of_property` | 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. | 충족 |  |  |
| C5-12 | `fraud_mistake.sequential_causation` | 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | 충족 |  |  |
| C5-13 | `fraud_stages_participation.completion_deception_disposition_transfer` | 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | 충족 |  |  |

### 편취의 범의와 재산적 이득 목적

검토 질문: A에게 C의 처분을 유도해 재물을 취득할 의사와 목적이 있었는가?

| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |
|---|---|---|---|---|---|
| C5-14 | `fraud_intent.contract_breach_distinction` | 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. | 충족 |  |  |
| C5-15 | `fraud_intent.time_of_conduct` | 편취의 범의는 행위 당시를 기준으로 판단한다. | 충족 |  |  |
| C5-16 | `fraud_mistake.gain_purpose` | 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | 충족 |  |  |
| C5-17 | `fraud_intent.no_disposition_inducement_intent` | 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | 불충족 |  |  |

**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`

**사건 메모:**
