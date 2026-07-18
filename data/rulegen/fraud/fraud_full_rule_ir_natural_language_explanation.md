# 사기죄 전체 RuleIR 자연어 설명

## 먼저 읽을 결론

이 RuleIR은 사실관계를 곧바로 유죄·무죄 문장으로 생성하지 않는다. neural/RAG 단계가 승인된 88개 NormCard별로 사건의 긍정사실, 반대사실, 미확인사실과 근거를 평가하고, Scallop은 그중 `provable`을 통과한 평가만 결합한다.

역할 인자는 법적 기능을 분리하기 위한 슬롯이다. 서로 다른 사람이라는 뜻이 아니므로 동일인이 여러 역할을 맡으면 같은 entity ID를 쓴다. 모든 성립 rule에서 피기망자와 처분자는 같은 변수다. 일반형은 재산소유자도 같은 변수이고, 삼각사기는 재산소유자를 별도 변수로 두면서 처분 권능 또는 지위를 추가로 요구한다.

## 런타임 입력

각 `assess_*` predicate는 `(case_id, assessment_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, status)`를 받는다. `status`는 `satisfied`, `not_satisfied`, `unknown`뿐이다. 모델이 사실을 찾지 못했다는 이유로 `not_satisfied`를 만들면 안 된다.

60개 `kind=standard` 입력은 기망의 신의칙 위반, 고의, 인과의 실질성처럼 개방형 법적 기준을 사건에 적용한 판단이다. 28개 `kind=rule` 입력은 모델이 법적 결론을 대신 내리는 것이 아니라 동일인 여부, 이전·지배취득, 순서 같은 결정규칙의 사실적 전제를 구조화한 rule fact다.

88개 relation을 모든 사건에 전부 생성하지 않는다. 사건 유형 routing에서 관련 없는 카드는 relation을 만들지 않는다. 관련 쟁점이지만 자료가 부족할 때만 `unknown` 행을 명시적으로 만들며, relation 부재는 false도 unknown도 아니다.

모든 substantive 경로는 같은 사건과 평가 ID의 `provable(case_id, assessment_id)`를 요구한다. 따라서 증거능력·신빙성 검토를 통과하지 않은 진술은 구성요건 판단에 들어가지 않는다.

## 모듈 구조

법학적 구성요건 코어는 주체, 객체, 객관적 행위·결과·인과관계, 주관적 요건으로 구성한다. 재물과 재산상 이익 모듈도 이 상위 코어에 속한다. 주체는 `defendant_id` 역할로 표현하고 책임능력 등은 형법총칙 gate에서 처리한다.

15개는 이 법학적 상위 구조 아래의 실행 모듈이다. 각 NormCard에는 하나의 주 소유 모듈만 있다. 차용금·광고·부작위·묵시적 기망·권리행사는 grounding profile, 삼각사기·제3자취득은 structural profile, 죄명 경계·미수/기수는 boundary 또는 stage module로 분리했다.

profile과 adapter는 `fraud_deception_satisfied`, `fraud_role_structure_satisfied` 같은 canonical interface만 출력한다. 최종 core는 차용금이나 삼각사기 같은 세부 유형명을 알지 않고 이 interface들을 한 번만 AND 결합한다. 현재는 검수를 위해 하나의 RuleIR 파일 안에서 논리적으로 분리했으며, Scallop 물리 파일 분리는 Sol·사용자 검수 뒤에 확정한다.

- 공통 기망 (`core.deception`, constitutive_core, 16장): 모든 사기 유형에 공통되는 기망의 정의, 한계 및 판단 기준
- 공통 주관적 요건 (`core.intent`, constitutive_core, 6장): 편취 범의, 재산적 이득 목적 및 행위시 판단 기준
- 공통 착오·처분행위 (`core.mistake_disposition`, constitutive_core, 14장): 착오, 처분행위, 직접성 및 순차적 인과관계의 공통 규칙
- 차용금 사기 (`profile.loan`, type_profile, 6장): 차용금 사기의 변제능력·의사, 용도, 위험인식 및 범의 추론
- 광고 사기 (`profile.advertising`, type_profile, 3장): 광고 상대방과 허용되는 과장·허위의 경계
- 부작위 기망 (`profile.omission`, type_profile, 9장): 기존 착오 이용, 고지의무 및 부작위 처분행위
- 묵시적 기망 (`profile.implicit_deception`, type_profile, 3장): 행동·태도의 설명가치에 의한 묵시적 기망과 부작위 기망의 구별
- 권리행사형 사기 (`profile.rights_exercise`, type_profile, 2장): 권리행사에 사용된 기망수단의 사회통념상 허용 범위
- 삼각사기 역할 구조 (`structure.triangular`, structural_profile, 3장): 피기망자·처분자와 재산소유자가 다른 삼각사기 역할 구조
- 제3자 취득 구조 (`structure.third_party_acquisition`, structural_profile, 1장): 제3자 취득을 피고인에게 귀속하는 의사·도구·대리 관계
- 절도·횡령과의 경계 (`boundary.other_offenses`, boundary, 3장): 처분능력·직접성·점유에 따른 절도 및 횡령과의 죄명 경계
- 재물의 객체·교부 (`object.property_delivery`, constitutive_core, 6장): 타인의 재물, 교부, 사실상 지배 및 금원 편취액
- 재산상 이익의 객체·취득 (`object.property_benefit`, constitutive_core, 6장): 재물 외 구체적 재산상 이익과 그 취득·처분 형태
- 공공적 법익과 재산권의 경계 (`object.public_interest`, boundary, 2장): 공공적 법익 침해를 재산권 침해와 동일하게 평가할 수 있는지의 경계
- 미수·기수 및 사후사정 (`stage.attempt_completion`, stage, 8장): 실행의 착수, 인과관계 단절에 따른 미수, 기수 및 사후사정

## 최종 성립의 AND gate와 손해 불요 규칙

최종 성립은 1번부터 10번까지의 사실·법적 component가 모두 있어야 한다. 11번은 별도 사실요건이 아니라 취득 component에서 자동으로 파생되는 compilation 규칙이다.

1. 사기죄의 객체인 타인의 재물 또는 구체적 재산상 이익
2. 신의칙에 반하여 착오를 일으키는 기망 또는 승인된 구체 유형의 기망
3. 사실과 다른 인식인 착오
4. 착오에 기한 재산적 처분행위
5. 재물 교부 또는 재산상 이익 취득
6. 기망·착오·처분·취득의 순차적 인과관계
7. 단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적
8. 미수를 넘어선 이전 또는 사실상 지배 취득
9. 피기망자=처분자를 포함한 일반형 또는 삼각사기의 역할 구조
10. 본인취득 또는 제3자취득의 피고인 귀속 구조
11. 취득 외에 현실적 재산상 손해를 별도 gate로 중복 요구하지 않는 판례 기준

불법영득의사 평가는 별도 support predicate로 보존하지만 모든 사기 유형의 공통 AND gate로 강제하지 않았다. 이는 사용자가 앞서 정한 실무지향 정책을 반영한다.

## 역할·취득 adapter와 단일 최종 규칙

- 일반형 역할 adapter: 피기망자=처분자=재산소유자
- 삼각사기 역할 adapter: 피기망자=처분자, 별도 재산소유자, 처분 권능·지위
- 본인취득 귀속 adapter: 수익자=피고인
- 제3자취득 귀속 adapter: 제3자의 도구·대리 관계 또는 제3자 취득 의사

위 두 축은 독립적으로 canonical relation을 만든다. `fraud.core.outcome.established` 하나가 나머지 구성요건과 두 relation을 결합하므로 네 조합을 최종 core에 반복하지 않는다.

## 부정·미확인·충돌

명시적 불성립 카드가 satisfied이거나 필수 positive 카드가 not_satisfied이면 `fraud_not_established`가 쟁점 ID와 함께 나온다. 관련 평가가 unknown이면 `fraud_undetermined`, 같은 카드에 satisfied와 not_satisfied가 모두 provable이면 `fraud_conflict`가 나온다. 부재를 부정으로 간주하는 negation은 사용하지 않는다.

`fraud_established`와 `fraud_not_established`가 동시에 나오면 `fraud_conflict(..., established_and_not_established)`도 도출한다. 후속 long-form generator는 conflict와 undetermined를 먼저 해소하거나 양측 논거로 표시해야 하며, established만 선택해 유죄 결론을 써서는 안 된다.

## 88개 입력의 의미와 논리적 사용

| No. | NormCard | 소유 모듈 | 형식 | 극성 | 논리적 사용 |
|---:|---|---|---|---|---|
| 1 | `deception.fraud.causal-link.deception-property-disposition`<br>사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 2 | `deception.fraud.causal-link.loan-purpose-not-sole-trigger`<br>차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. | `profile.loan` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 3 | `deception.fraud.causal-link.no-disposition-no-deception`<br>상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. | `core.deception` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 4 | `deception.fraud.definition.deceived-person-unspecified`<br>광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. | `profile.advertising` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 5 | `deception.fraud.definition.deceived-person-victim-distinct`<br>기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. | `structure.triangular` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 6 | `deception.fraud.definition.deception-content-basis-fact`<br>기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. | `core.deception` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 7 | `deception.fraud.definition.deception-counterparty-is-other`<br>사기죄에서 기망의 상대방은 타인이다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 8 | `deception.fraud.definition.deception-good-faith-mistake`<br>기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. | `core.deception` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 9 | `deception.fraud.definition.deception-means-unrestricted`<br>기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 10 | `deception.fraud.definition.deception-object-facts`<br>재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. | `core.deception` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 11 | `deception.fraud.definition.deception-target-human`<br>사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. | `core.deception` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 12 | `deception.fraud.definition.exploitation-existing-mistake`<br>이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. | `profile.omission` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 13 | `deception.fraud.definition.implicit-deception`<br>묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. | `profile.implicit_deception` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 14 | `deception.fraud.definition.notice-duty-violation-omission`<br>고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. | `profile.omission` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 15 | `deception.fraud.definition.other-includes-corporation`<br>사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 16 | `deception.fraud.element.deception-must-create-false-belief`<br>기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. | `core.deception` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 17 | `deception.fraud.element.deception-not-legal-act-important-part`<br>사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 18 | `deception.fraud.element.loan-no-repayment-intent-or-ability`<br>변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. | `profile.loan` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 19 | `deception.fraud.element.omission-deception-guarantor-equivalence`<br>부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. | `profile.omission` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 20 | `deception.fraud.element.omission-deception-independent-error`<br>부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. | `profile.omission` | `deterministic_rule` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 21 | `deception.fraud.element.omission-deception-legal-notice-duty`<br>법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. | `profile.omission` | `deterministic_rule` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 22 | `deception.fraud.element.transaction-purpose-no-impairment`<br>상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. | `core.deception` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 23 | `deception.fraud.element.victim-negligence-no-bar`<br>착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. | `core.deception` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 24 | `deception.fraud.standard.advertising-important-concrete-falsehood`<br>거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. | `profile.advertising` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 25 | `deception.fraud.standard.advertising-tolerable-exaggeration`<br>상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. | `profile.advertising` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 26 | `deception.fraud.standard.deception-concrete-circumstances`<br>행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. | `core.deception` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 27 | `deception.fraud.standard.easily-detectable-lie`<br>구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. | `core.deception` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 28 | `deception.fraud.standard.implicit-deception-explanatory-value`<br>묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. | `profile.implicit_deception` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 29 | `deception.fraud.standard.implicit-omission-deception-distinction`<br>행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. | `profile.implicit_deception` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 30 | `deception.fraud.standard.intent-to-defraud-loan-inference`<br>차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. | `profile.loan` | `standard_input` | `positive` | 연결 output: fraud_intent_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 31 | `deception.fraud.standard.loan-lender-anticipated-risk`<br>대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. | `profile.loan` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 32 | `deception.fraud.standard.loan-purpose-materiality`<br>용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. | `profile.loan` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 33 | `deception.fraud.standard.loan-subsequent-default`<br>소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. | `profile.loan` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 34 | `deception.fraud.standard.precedent-notice-duty-materiality`<br>판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. | `profile.omission` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 35 | `deception.fraud.standard.vague-opinion-not-deception`<br>땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. | `core.deception` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 36 | `fraud_damage_acquisition.delivery_factual_control`<br>재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. | `object.property_delivery` | `standard_input` | `positive` | 연결 output: fraud_acquisition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 37 | `fraud_damage_acquisition.delivery_of_property`<br>사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. | `object.property_delivery` | `standard_input` | `positive` | 연결 output: fraud_acquisition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 38 | `fraud_damage_acquisition.money_delivery_full_amount`<br>금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. | `object.property_delivery` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 39 | `fraud_damage_acquisition.property_concept_reported_precedent`<br>사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. | `object.property_benefit` | `deterministic_rule` | `positive` | 연결 output: fraud_acquisition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 40 | `fraud_damage_acquisition.property_disposition_types`<br>재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. | `object.property_benefit` | `standard_input` | `positive` | 연결 output: fraud_acquisition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 41 | `fraud_damage_acquisition.property_loss_negative_view`<br>사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. | `stage.attempt_completion` | `deterministic_rule` | `negative` | 연결 output: fraud_no_separate_loss_gate; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 42 | `fraud_damage_acquisition.protected_economic_interest`<br>사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. | `object.property_benefit` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 43 | `fraud_damage_acquisition.right_exercise_unacceptable_deception`<br>기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. | `profile.rights_exercise` | `standard_input` | `positive` | 연결 output: fraud_deception_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 44 | `fraud_damage_acquisition.subsequent_return_irrelevant`<br>기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. | `object.property_delivery` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 45 | `fraud_general_object.causation_required`<br>객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. | `stage.attempt_completion` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 46 | `fraud_general_object.deception_error_causation`<br>기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. | `stage.attempt_completion` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 47 | `fraud_intent.contract_breach_distinction`<br>고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. | `core.intent` | `standard_input` | `positive` | 연결 output: fraud_beneficiary_attribution_satisfied, fraud_intent_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 48 | `fraud_intent.illegal_appropriation_definition`<br>사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. | `core.intent` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 49 | `fraud_intent.no_disposition_inducement_intent`<br>피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. | `core.intent` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 50 | `fraud_intent.precedent_illegal_appropriation_intent`<br>판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. | `core.intent` | `standard_input` | `positive` | 연결 output: fraud_unlawful_appropriation_intent_supported; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 51 | `fraud_intent.third_party_acquisition`<br>행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. | `structure.third_party_acquisition` | `standard_input` | `positive` | 연결 output: fraud_beneficiary_attribution_satisfied, fraud_third_party_acquisition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 52 | `fraud_intent.time_of_conduct`<br>편취의 범의는 행위 당시를 기준으로 판단한다. | `core.intent` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 53 | `fraud_mistake.conscious_nonexercise`<br>피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. | `profile.omission` | `standard_input` | `positive` | 연결 output: fraud_disposition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 54 | `fraud_mistake.deceived_disposer_identity`<br>피기망자와 처분행위자는 동일인이어야 한다. | `core.mistake_disposition` | `deterministic_rule` | `positive` | 연결 output: fraud_deceived_disposer_identity_satisfied, fraud_not_established, fraud_role_structure_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 55 | `fraud_mistake.disposition_definition`<br>처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. | `core.mistake_disposition` | `standard_input` | `positive` | 연결 output: fraud_disposition_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 56 | `fraud_mistake.disposition_directness`<br>재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. | `core.mistake_disposition` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 57 | `fraud_mistake.disposition_intent_act_awareness`<br>피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. | `core.mistake_disposition` | `standard_input` | `positive` | 연결 output: fraud_disposition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 58 | `fraud_mistake.disposition_omission`<br>직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. | `profile.omission` | `standard_input` | `positive` | 연결 output: fraud_disposition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 59 | `fraud_mistake.error_definition`<br>착오란 사실과 일치하지 않는 인식을 의미한다. | `core.mistake_disposition` | `standard_input` | `positive` | 연결 output: fraud_mistake_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 60 | `fraud_mistake.error_disposition_motivation`<br>착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. | `core.mistake_disposition` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 61 | `fraud_mistake.error_doubt_ignorance`<br>사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. | `core.mistake_disposition` | `standard_input` | `positive` | 연결 output: fraud_mistake_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 62 | `fraud_mistake.factual_act_disposition`<br>피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. | `core.mistake_disposition` | `deterministic_rule` | `positive` | 연결 output: fraud_disposition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 63 | `fraud_mistake.gain_purpose`<br>사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. | `core.intent` | `standard_input` | `positive` | 연결 output: fraud_beneficiary_attribution_satisfied, fraud_intent_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 64 | `fraud_mistake.invalid_act_disposition`<br>착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. | `core.mistake_disposition` | `deterministic_rule` | `positive` | 연결 output: fraud_disposition_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 65 | `fraud_mistake.no_capacity_theft`<br>구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. | `boundary.other_offenses` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 66 | `fraud_mistake.no_thought_no_error`<br>어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. | `core.mistake_disposition` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 67 | `fraud_mistake.omission_not_all_nonclaims`<br>채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. | `profile.omission` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 68 | `fraud_mistake.property_disposition_element`<br>사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. | `core.mistake_disposition` | `deterministic_rule` | `positive` | 연결 output: fraud_acquisition_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 69 | `fraud_mistake.property_limited_disposition`<br>처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. | `core.mistake_disposition` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 70 | `fraud_mistake.sequential_causation`<br>사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. | `core.mistake_disposition` | `deterministic_rule` | `positive` | 연결 output: fraud_causal_chain_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 71 | `fraud_mistake.triangular_fraud_definition`<br>피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. | `structure.triangular` | `deterministic_rule` | `positive` | 연결 output: fraud_role_structure_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 72 | `fraud_mistake.trick_theft_directness`<br>기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. | `boundary.other_offenses` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 73 | `fraud_mistake.unaware_error`<br>피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. | `core.mistake_disposition` | `standard_input` | `positive` | 연결 output: fraud_mistake_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 74 | `fraud_stages_participation.attempt_deceptive_act`<br>사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. | `stage.attempt_completion` | `deterministic_rule` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 75 | `fraud_stages_participation.completion_deception_disposition_transfer`<br>행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. | `stage.attempt_completion` | `deterministic_rule` | `positive` | 연결 output: fraud_completion_satisfied, fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 76 | `fraud_stages_participation.no_causation_attempt`<br>기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. | `stage.attempt_completion` | `deterministic_rule` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 77 | `fraud_stages_participation.property_fraud_completion_control`<br>재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. | `stage.attempt_completion` | `deterministic_rule` | `positive` | 연결 output: fraud_completion_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 78 | `general_object.fraud.definition.property-benefit`<br>재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. | `object.property_benefit` | `standard_input` | `positive` | 연결 output: fraud_object_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 79 | `general_object.fraud.definition.property-benefit-not-numerically-limited`<br>재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. | `object.property_benefit` | `standard_input` | `positive` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 80 | `general_object.fraud.element.object-other-possessed-other-property`<br>사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. | `object.property_delivery` | `standard_input` | `positive` | 연결 output: fraud_not_established, fraud_object_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 81 | `general_object.fraud.element.property-benefit-concrete`<br>재산상 이익은 구체적인 이익이어야 한다. | `object.property_benefit` | `standard_input` | `positive` | 연결 output: fraud_object_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 82 | `general_object.fraud.exception.public-interest-property-equivalence`<br>기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. | `object.public_interest` | `standard_input` | `exception` | 연결 output: fraud_object_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 83 | `general_object.fraud.standard.later-cancellation-no-effect`<br>사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. | `stage.attempt_completion` | `standard_input` | `negative` | 개별 쟁점의 증명 가능한 support fact; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 84 | `general_object.fraud.standard.own-possession-other-property-embezzlement`<br>자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. | `boundary.other_offenses` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 85 | `general_object.fraud.standard.own-property-not-object`<br>타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. | `object.property_delivery` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 86 | `general_object.fraud.standard.public-interest-only-no-fraud`<br>기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. | `object.public_interest` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 87 | `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`<br>피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. | `structure.triangular` | `standard_input` | `positive` | 연결 output: fraud_role_structure_satisfied, fraud_triangular_authority_satisfied; unknown이면 undetermined; 상반된 두 평가면 conflict |
| 88 | `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`<br>기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. | `profile.rights_exercise` | `standard_input` | `negative` | 연결 output: fraud_not_established; unknown이면 undetermined; 상반된 두 평가면 conflict |

## Rule별 자연어 해설

아래 목록은 모든 rule의 head와 body를 빠짐없이 펼친 것이다. body의 각 항목이 모두 참일 때만 head가 도출된다.

### `fraud.core_deception.card.001.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다.** (`satisfied_deception_fraud_causal_link_deception_property_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. (`assess_deception_fraud_causal_link_deception_property_disposition(case_id, assessment_001, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_001)`)

근거 NormCard: `deception.fraud.causal-link.deception-property-disposition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.002.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다.** (`satisfied_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. (`assess_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, assessment_002, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_002)`)

근거 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.003.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다.** (`satisfied_deception_fraud_causal_link_no_disposition_no_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. (`assess_deception_fraud_causal_link_no_disposition_no_deception(case_id, assessment_003, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_003)`)

근거 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.004.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다.** (`satisfied_deception_fraud_definition_deceived_person_unspecified(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. (`assess_deception_fraud_definition_deceived_person_unspecified(case_id, assessment_004, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_004)`)

근거 NormCard: `deception.fraud.definition.deceived-person-unspecified`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.005.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다.** (`satisfied_deception_fraud_definition_deceived_person_victim_distinct(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. (`assess_deception_fraud_definition_deceived_person_victim_distinct(case_id, assessment_005, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_005)`)

근거 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.006.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다.** (`satisfied_deception_fraud_definition_deception_content_basis_fact(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. (`assess_deception_fraud_definition_deception_content_basis_fact(case_id, assessment_006, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_006)`)

근거 NormCard: `deception.fraud.definition.deception-content-basis-fact`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.007.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 기망의 상대방은 타인이다.** (`satisfied_deception_fraud_definition_deception_counterparty_is_other(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다. (`assess_deception_fraud_definition_deception_counterparty_is_other(case_id, assessment_007, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_007)`)

근거 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.008.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다.** (`satisfied_deception_fraud_definition_deception_good_faith_mistake(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`assess_deception_fraud_definition_deception_good_faith_mistake(case_id, assessment_008, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_008)`)

근거 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.009.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다.** (`satisfied_deception_fraud_definition_deception_means_unrestricted(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. (`assess_deception_fraud_definition_deception_means_unrestricted(case_id, assessment_009, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_009)`)

근거 NormCard: `deception.fraud.definition.deception-means-unrestricted`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.010.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다.** (`satisfied_deception_fraud_definition_deception_object_facts(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. (`assess_deception_fraud_definition_deception_object_facts(case_id, assessment_010, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_010)`)

근거 NormCard: `deception.fraud.definition.deception-object-facts`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.011.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다.** (`satisfied_deception_fraud_definition_deception_target_human(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. (`assess_deception_fraud_definition_deception_target_human(case_id, assessment_011, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_011)`)

근거 NormCard: `deception.fraud.definition.deception-target-human`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.012.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다.** (`satisfied_deception_fraud_definition_exploitation_existing_mistake(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. (`assess_deception_fraud_definition_exploitation_existing_mistake(case_id, assessment_012, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_012)`)

근거 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.013.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다.** (`satisfied_deception_fraud_definition_implicit_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. (`assess_deception_fraud_definition_implicit_deception(case_id, assessment_013, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_013)`)

근거 NormCard: `deception.fraud.definition.implicit-deception`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.014.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다.** (`satisfied_deception_fraud_definition_notice_duty_violation_omission(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. (`assess_deception_fraud_definition_notice_duty_violation_omission(case_id, assessment_014, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_014)`)

근거 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.015.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다.** (`satisfied_deception_fraud_definition_other_includes_corporation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. (`assess_deception_fraud_definition_other_includes_corporation(case_id, assessment_015, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_015)`)

근거 NormCard: `deception.fraud.definition.other-includes-corporation`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.016.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다.** (`satisfied_deception_fraud_element_deception_must_create_false_belief(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. (`assess_deception_fraud_element_deception_must_create_false_belief(case_id, assessment_016, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_016)`)

근거 NormCard: `deception.fraud.element.deception-must-create-false-belief`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.017.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다.** (`satisfied_deception_fraud_element_deception_not_legal_act_important_part(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. (`assess_deception_fraud_element_deception_not_legal_act_important_part(case_id, assessment_017, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_017)`)

근거 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.018.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다.** (`satisfied_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. (`assess_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, assessment_018, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_018)`)

근거 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.019.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다.** (`satisfied_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. (`assess_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, assessment_019, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_019)`)

근거 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.020.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다.** (`satisfied_deception_fraud_element_omission_deception_independent_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. (`assess_deception_fraud_element_omission_deception_independent_error(case_id, assessment_020, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_020)`)

근거 NormCard: `deception.fraud.element.omission-deception-independent-error`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.021.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다.** (`satisfied_deception_fraud_element_omission_deception_legal_notice_duty(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. (`assess_deception_fraud_element_omission_deception_legal_notice_duty(case_id, assessment_021, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_021)`)

근거 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.022.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다.** (`satisfied_deception_fraud_element_transaction_purpose_no_impairment(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. (`assess_deception_fraud_element_transaction_purpose_no_impairment(case_id, assessment_022, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_022)`)

근거 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.023.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다.** (`satisfied_deception_fraud_element_victim_negligence_no_bar(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. (`assess_deception_fraud_element_victim_negligence_no_bar(case_id, assessment_023, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_023)`)

근거 NormCard: `deception.fraud.element.victim-negligence-no-bar`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.024.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다.** (`satisfied_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. (`assess_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, assessment_024, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_024)`)

근거 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_advertising.card.025.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다.** (`satisfied_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. (`assess_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, assessment_025, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_025)`)

근거 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.026.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다.** (`satisfied_deception_fraud_standard_deception_concrete_circumstances(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. (`assess_deception_fraud_standard_deception_concrete_circumstances(case_id, assessment_026, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_026)`)

근거 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.027.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다.** (`satisfied_deception_fraud_standard_easily_detectable_lie(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. (`assess_deception_fraud_standard_easily_detectable_lie(case_id, assessment_027, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_027)`)

근거 NormCard: `deception.fraud.standard.easily-detectable-lie`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.028.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다.** (`satisfied_deception_fraud_standard_implicit_deception_explanatory_value(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. (`assess_deception_fraud_standard_implicit_deception_explanatory_value(case_id, assessment_028, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_028)`)

근거 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_implicit_deception.card.029.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다.** (`satisfied_deception_fraud_standard_implicit_omission_deception_distinction(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. (`assess_deception_fraud_standard_implicit_omission_deception_distinction(case_id, assessment_029, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_029)`)

근거 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.030.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다.** (`satisfied_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. (`assess_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, assessment_030, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_030)`)

근거 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.031.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다.** (`satisfied_deception_fraud_standard_loan_lender_anticipated_risk(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. (`assess_deception_fraud_standard_loan_lender_anticipated_risk(case_id, assessment_031, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_031)`)

근거 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.032.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다.** (`satisfied_deception_fraud_standard_loan_purpose_materiality(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. (`assess_deception_fraud_standard_loan_purpose_materiality(case_id, assessment_032, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_032)`)

근거 NormCard: `deception.fraud.standard.loan-purpose-materiality`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_loan.card.033.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다.** (`satisfied_deception_fraud_standard_loan_subsequent_default(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. (`assess_deception_fraud_standard_loan_subsequent_default(case_id, assessment_033, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_033)`)

근거 NormCard: `deception.fraud.standard.loan-subsequent-default`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.034.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다.** (`satisfied_deception_fraud_standard_precedent_notice_duty_materiality(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. (`assess_deception_fraud_standard_precedent_notice_duty_materiality(case_id, assessment_034, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_034)`)

근거 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_deception.card.035.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다.** (`satisfied_deception_fraud_standard_vague_opinion_not_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. (`assess_deception_fraud_standard_vague_opinion_not_deception(case_id, assessment_035, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_035)`)

근거 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.036.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다.** (`satisfied_fraud_damage_acquisition_delivery_factual_control(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. (`assess_fraud_damage_acquisition_delivery_factual_control(case_id, assessment_036, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_036)`)

근거 NormCard: `fraud_damage_acquisition.delivery_factual_control`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.037.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다.** (`satisfied_fraud_damage_acquisition_delivery_of_property(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. (`assess_fraud_damage_acquisition_delivery_of_property(case_id, assessment_037, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_037)`)

근거 NormCard: `fraud_damage_acquisition.delivery_of_property`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.038.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다.** (`satisfied_fraud_damage_acquisition_money_delivery_full_amount(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. (`assess_fraud_damage_acquisition_money_delivery_full_amount(case_id, assessment_038, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_038)`)

근거 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.039.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다.** (`satisfied_fraud_damage_acquisition_property_concept_reported_precedent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. (`assess_fraud_damage_acquisition_property_concept_reported_precedent(case_id, assessment_039, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_039)`)

근거 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.040.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다.** (`satisfied_fraud_damage_acquisition_property_disposition_types(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. (`assess_fraud_damage_acquisition_property_disposition_types(case_id, assessment_040, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_040)`)

근거 NormCard: `fraud_damage_acquisition.property_disposition_types`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.041.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다.** (`satisfied_fraud_damage_acquisition_property_loss_negative_view(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. (`assess_fraud_damage_acquisition_property_loss_negative_view(case_id, assessment_041, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_041)`)

근거 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.042.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다.** (`satisfied_fraud_damage_acquisition_protected_economic_interest(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. (`assess_fraud_damage_acquisition_protected_economic_interest(case_id, assessment_042, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_042)`)

근거 NormCard: `fraud_damage_acquisition.protected_economic_interest`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_rights_exercise.card.043.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다.** (`satisfied_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. (`assess_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, assessment_043, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_043)`)

근거 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.044.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다.** (`satisfied_fraud_damage_acquisition_subsequent_return_irrelevant(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. (`assess_fraud_damage_acquisition_subsequent_return_irrelevant(case_id, assessment_044, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_044)`)

근거 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.045.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다.** (`satisfied_fraud_general_object_causation_required(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. (`assess_fraud_general_object_causation_required(case_id, assessment_045, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_045)`)

근거 NormCard: `fraud_general_object.causation_required`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.046.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다.** (`satisfied_fraud_general_object_deception_error_causation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. (`assess_fraud_general_object_deception_error_causation(case_id, assessment_046, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_046)`)

근거 NormCard: `fraud_general_object.deception_error_causation`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.047.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다.** (`satisfied_fraud_intent_contract_breach_distinction(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`assess_fraud_intent_contract_breach_distinction(case_id, assessment_047, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_047)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.048.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다.** (`satisfied_fraud_intent_illegal_appropriation_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. (`assess_fraud_intent_illegal_appropriation_definition(case_id, assessment_048, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_048)`)

근거 NormCard: `fraud_intent.illegal_appropriation_definition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.049.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.** (`satisfied_fraud_intent_no_disposition_inducement_intent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. (`assess_fraud_intent_no_disposition_inducement_intent(case_id, assessment_049, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_049)`)

근거 NormCard: `fraud_intent.no_disposition_inducement_intent`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.050.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다.** (`satisfied_fraud_intent_precedent_illegal_appropriation_intent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. (`assess_fraud_intent_precedent_illegal_appropriation_intent(case_id, assessment_050, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_050)`)

근거 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_third_party_acquisition.card.051.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다.** (`satisfied_fraud_intent_third_party_acquisition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. (`assess_fraud_intent_third_party_acquisition(case_id, assessment_051, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_051)`)

근거 NormCard: `fraud_intent.third_party_acquisition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.052.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 편취의 범의는 행위 당시를 기준으로 판단한다.** (`satisfied_fraud_intent_time_of_conduct(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 편취의 범의는 행위 당시를 기준으로 판단한다. (`assess_fraud_intent_time_of_conduct(case_id, assessment_052, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_052)`)

근거 NormCard: `fraud_intent.time_of_conduct`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.053.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다.** (`satisfied_fraud_mistake_conscious_nonexercise(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. (`assess_fraud_mistake_conscious_nonexercise(case_id, assessment_053, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_053)`)

근거 NormCard: `fraud_mistake.conscious_nonexercise`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.054.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 처분행위자는 동일인이어야 한다.** (`satisfied_fraud_mistake_deceived_disposer_identity(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다. (`assess_fraud_mistake_deceived_disposer_identity(case_id, assessment_054, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_054)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.055.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다.** (`satisfied_fraud_mistake_disposition_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`assess_fraud_mistake_disposition_definition(case_id, assessment_055, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_055)`)

근거 NormCard: `fraud_mistake.disposition_definition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.056.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다.** (`satisfied_fraud_mistake_disposition_directness(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. (`assess_fraud_mistake_disposition_directness(case_id, assessment_056, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_056)`)

근거 NormCard: `fraud_mistake.disposition_directness`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.057.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다.** (`satisfied_fraud_mistake_disposition_intent_act_awareness(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. (`assess_fraud_mistake_disposition_intent_act_awareness(case_id, assessment_057, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_057)`)

근거 NormCard: `fraud_mistake.disposition_intent_act_awareness`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.058.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다.** (`satisfied_fraud_mistake_disposition_omission(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. (`assess_fraud_mistake_disposition_omission(case_id, assessment_058, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_058)`)

근거 NormCard: `fraud_mistake.disposition_omission`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.059.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 착오란 사실과 일치하지 않는 인식을 의미한다.** (`satisfied_fraud_mistake_error_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오란 사실과 일치하지 않는 인식을 의미한다. (`assess_fraud_mistake_error_definition(case_id, assessment_059, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_059)`)

근거 NormCard: `fraud_mistake.error_definition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.060.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다.** (`satisfied_fraud_mistake_error_disposition_motivation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. (`assess_fraud_mistake_error_disposition_motivation(case_id, assessment_060, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_060)`)

근거 NormCard: `fraud_mistake.error_disposition_motivation`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.061.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다.** (`satisfied_fraud_mistake_error_doubt_ignorance(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. (`assess_fraud_mistake_error_doubt_ignorance(case_id, assessment_061, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_061)`)

근거 NormCard: `fraud_mistake.error_doubt_ignorance`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.062.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다.** (`satisfied_fraud_mistake_factual_act_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. (`assess_fraud_mistake_factual_act_disposition(case_id, assessment_062, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_062)`)

근거 NormCard: `fraud_mistake.factual_act_disposition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_intent.card.063.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다.** (`satisfied_fraud_mistake_gain_purpose(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`assess_fraud_mistake_gain_purpose(case_id, assessment_063, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_063)`)

근거 NormCard: `fraud_mistake.gain_purpose`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.064.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다.** (`satisfied_fraud_mistake_invalid_act_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. (`assess_fraud_mistake_invalid_act_disposition(case_id, assessment_064, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_064)`)

근거 NormCard: `fraud_mistake.invalid_act_disposition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.065.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다.** (`satisfied_fraud_mistake_no_capacity_theft(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_no_capacity_theft(case_id, assessment_065, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_065)`)

근거 NormCard: `fraud_mistake.no_capacity_theft`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.066.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다.** (`satisfied_fraud_mistake_no_thought_no_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. (`assess_fraud_mistake_no_thought_no_error(case_id, assessment_066, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_066)`)

근거 NormCard: `fraud_mistake.no_thought_no_error`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_omission.card.067.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다.** (`satisfied_fraud_mistake_omission_not_all_nonclaims(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. (`assess_fraud_mistake_omission_not_all_nonclaims(case_id, assessment_067, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_067)`)

근거 NormCard: `fraud_mistake.omission_not_all_nonclaims`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.068.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다.** (`satisfied_fraud_mistake_property_disposition_element(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`assess_fraud_mistake_property_disposition_element(case_id, assessment_068, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_068)`)

근거 NormCard: `fraud_mistake.property_disposition_element`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.069.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다.** (`satisfied_fraud_mistake_property_limited_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. (`assess_fraud_mistake_property_limited_disposition(case_id, assessment_069, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_069)`)

근거 NormCard: `fraud_mistake.property_limited_disposition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.070.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다.** (`satisfied_fraud_mistake_sequential_causation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`assess_fraud_mistake_sequential_causation(case_id, assessment_070, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_070)`)

근거 NormCard: `fraud_mistake.sequential_causation`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.071.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다.** (`satisfied_fraud_mistake_triangular_fraud_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. (`assess_fraud_mistake_triangular_fraud_definition(case_id, assessment_071, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_071)`)

근거 NormCard: `fraud_mistake.triangular_fraud_definition`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.072.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다.** (`satisfied_fraud_mistake_trick_theft_directness(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_trick_theft_directness(case_id, assessment_072, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_072)`)

근거 NormCard: `fraud_mistake.trick_theft_directness`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.core_mistake_disposition.card.073.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다.** (`satisfied_fraud_mistake_unaware_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. (`assess_fraud_mistake_unaware_error(case_id, assessment_073, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_073)`)

근거 NormCard: `fraud_mistake.unaware_error`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.074.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다.** (`satisfied_fraud_stages_participation_attempt_deceptive_act(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. (`assess_fraud_stages_participation_attempt_deceptive_act(case_id, assessment_074, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_074)`)

근거 NormCard: `fraud_stages_participation.attempt_deceptive_act`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.075.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다.** (`satisfied_fraud_stages_participation_completion_deception_disposition_transfer(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id, assessment_075, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_075)`)

근거 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.076.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다.** (`satisfied_fraud_stages_participation_no_causation_attempt(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. (`assess_fraud_stages_participation_no_causation_attempt(case_id, assessment_076, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_076)`)

근거 NormCard: `fraud_stages_participation.no_causation_attempt`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.077.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다.** (`satisfied_fraud_stages_participation_property_fraud_completion_control(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. (`assess_fraud_stages_participation_property_fraud_completion_control(case_id, assessment_077, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_077)`)

근거 NormCard: `fraud_stages_participation.property_fraud_completion_control`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.078.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다.** (`satisfied_general_object_fraud_definition_property_benefit(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. (`assess_general_object_fraud_definition_property_benefit(case_id, assessment_078, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_078)`)

근거 NormCard: `general_object.fraud.definition.property-benefit`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.079.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다.** (`satisfied_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. (`assess_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id, assessment_079, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_079)`)

근거 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.080.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다.** (`satisfied_general_object_fraud_element_object_other_possessed_other_property(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`assess_general_object_fraud_element_object_other_possessed_other_property(case_id, assessment_080, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_080)`)

근거 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_benefit.card.081.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 구체적인 이익이어야 한다.** (`satisfied_general_object_fraud_element_property_benefit_concrete(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다. (`assess_general_object_fraud_element_property_benefit_concrete(case_id, assessment_081, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_081)`)

근거 NormCard: `general_object.fraud.element.property-benefit-concrete`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_public_interest.card.082.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다.** (`satisfied_general_object_fraud_exception_public_interest_property_equivalence(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. (`assess_general_object_fraud_exception_public_interest_property_equivalence(case_id, assessment_082, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_082)`)

근거 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.stage_attempt_completion.card.083.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다.** (`satisfied_general_object_fraud_standard_later_cancellation_no_effect(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. (`assess_general_object_fraud_standard_later_cancellation_no_effect(case_id, assessment_083, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_083)`)

근거 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.boundary_other_offenses.card.084.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.** (`satisfied_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. (`assess_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, assessment_084, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_084)`)

근거 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.card.085.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다.** (`satisfied_general_object_fraud_standard_own_property_not_object(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. (`assess_general_object_fraud_standard_own_property_not_object(case_id, assessment_085, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_085)`)

근거 NormCard: `general_object.fraud.standard.own-property-not-object`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_public_interest.card.086.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다.** (`satisfied_general_object_fraud_standard_public_interest_only_no_fraud(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. (`assess_general_object_fraud_standard_public_interest_only_no_fraud(case_id, assessment_086, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_086)`)

근거 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.structure_triangular.card.087.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다.** (`satisfied_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. (`assess_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, assessment_087, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_087)`)

근거 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.profile_rights_exercise.card.088.satisfied`

결론: **증명 가능한 평가에서 다음 조건이 충족됨: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다.** (`satisfied_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. (`assess_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, assessment_088, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, assessment_088)`)

근거 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

해석 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `fraud.object_property_delivery.component.fraud_object_satisfied.01`

결론: **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨** (`fraud_object_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`satisfied_general_object_fraud_element_object_other_possessed_other_property(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_public_interest.component.fraud_object_satisfied.02`

결론: **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨** (`fraud_object_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. (`satisfied_general_object_fraud_exception_public_interest_property_equivalence(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_deception.component.fraud_deception_satisfied.01`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`satisfied_deception_fraud_definition_deception_good_faith_mistake(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_deception_satisfied.02`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. (`satisfied_deception_fraud_definition_exploitation_existing_mistake(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_loan.component.fraud_deception_satisfied.03`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. (`satisfied_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_advertising.component.fraud_deception_satisfied.04`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. (`satisfied_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_implicit_deception.component.fraud_deception_satisfied.05`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. (`satisfied_deception_fraud_standard_implicit_deception_explanatory_value(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_loan.component.fraud_deception_satisfied.06`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. (`satisfied_deception_fraud_standard_loan_purpose_materiality(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.loan-purpose-materiality`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_rights_exercise.component.fraud_deception_satisfied.07`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. (`satisfied_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.01`

결론: **피기망자에게 법적 의미의 착오가 인정됨** (`fraud_mistake_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 착오란 사실과 일치하지 않는 인식을 의미한다. (`satisfied_fraud_mistake_error_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.error_definition`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.02`

결론: **피기망자에게 법적 의미의 착오가 인정됨** (`fraud_mistake_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. (`satisfied_fraud_mistake_error_doubt_ignorance(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.error_doubt_ignorance`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_mistake_satisfied.03`

결론: **피기망자에게 법적 의미의 착오가 인정됨** (`fraud_mistake_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. (`satisfied_fraud_mistake_unaware_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.unaware_error`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.01`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`satisfied_fraud_mistake_disposition_definition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.disposition_definition`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_disposition_satisfied.02`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. (`satisfied_fraud_mistake_conscious_nonexercise(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.conscious_nonexercise`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.03`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. (`satisfied_fraud_mistake_disposition_intent_act_awareness(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.disposition_intent_act_awareness`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_disposition_satisfied.04`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. (`satisfied_fraud_mistake_disposition_omission(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.disposition_omission`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.05`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. (`satisfied_fraud_mistake_factual_act_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.factual_act_disposition`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_disposition_satisfied.06`

결론: **착오에 기한 재산적 처분행위가 인정됨** (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. (`satisfied_fraud_mistake_invalid_act_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.invalid_act_disposition`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_delivery.component.fraud_acquisition_satisfied.01`

결론: **재물 교부 또는 재산상 이익의 취득이 인정됨** (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. (`satisfied_fraud_damage_acquisition_delivery_factual_control(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.delivery_factual_control`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_delivery.component.fraud_acquisition_satisfied.02`

결론: **재물 교부 또는 재산상 이익의 취득이 인정됨** (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. (`satisfied_fraud_damage_acquisition_delivery_of_property(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.delivery_of_property`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_benefit.component.fraud_acquisition_satisfied.03`

결론: **재물 교부 또는 재산상 이익의 취득이 인정됨** (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. (`satisfied_fraud_damage_acquisition_property_concept_reported_precedent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.object_property_benefit.component.fraud_acquisition_satisfied.04`

결론: **재물 교부 또는 재산상 이익의 취득이 인정됨** (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. (`satisfied_fraud_damage_acquisition_property_disposition_types(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.property_disposition_types`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_acquisition_satisfied.05`

결론: **재물 교부 또는 재산상 이익의 취득이 인정됨** (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`satisfied_fraud_mistake_property_disposition_element(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.property_disposition_element`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_causal_chain_satisfied.01`

결론: **기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨** (`fraud_causal_chain_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`satisfied_fraud_mistake_sequential_causation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.sequential_causation`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_mistake_disposition.component.fraud_deceived_disposer_identity_satisfied.01`

결론: **피기망자와 처분행위자가 동일한 행위주체임** (`fraud_deceived_disposer_identity_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 처분행위자는 동일인이어야 한다. (`satisfied_fraud_mistake_deceived_disposer_identity(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.stage_attempt_completion.component.fraud_completion_satisfied.01`

결론: **사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨** (`fraud_completion_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`satisfied_fraud_stages_participation_completion_deception_disposition_transfer(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.stage_attempt_completion.component.fraud_completion_satisfied.02`

결론: **사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨** (`fraud_completion_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. (`satisfied_fraud_stages_participation_property_fraud_completion_control(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_stages_participation.property_fraud_completion_control`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.structure_third_party_acquisition.component.fraud_third_party_acquisition_satisfied.01`

결론: **제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨** (`fraud_third_party_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. (`satisfied_fraud_intent_third_party_acquisition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_intent.third_party_acquisition`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.structure_triangular.component.fraud_triangular_authority_satisfied.01`

결론: **피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨** (`fraud_triangular_authority_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. (`satisfied_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.core_intent.component.fraud_unlawful_appropriation_intent_supported.01`

결론: **불법영득의사가 요구되는 유형에서 그 의사가 인정됨** (`fraud_unlawful_appropriation_intent_supported(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. (`satisfied_fraud_intent_precedent_illegal_appropriation_intent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

해석 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `fraud.profile_omission.component.fraud_deception_satisfied`

결론: **사건에 적용되는 기망 기준이 충족됨** (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. (`satisfied_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. (`satisfied_deception_fraud_element_omission_deception_independent_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. (`satisfied_deception_fraud_element_omission_deception_legal_notice_duty(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`

해석 메모: 부작위 기망은 보증인적 지위·독립 착오·법률상 고지의무가 함께 확인된 경로다.

### `fraud.object_property_benefit.component.fraud_object_satisfied`

결론: **사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨** (`fraud_object_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. (`satisfied_general_object_fraud_definition_property_benefit(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 재산상 이익은 구체적인 이익이어야 한다. (`satisfied_general_object_fraud_element_property_benefit_concrete(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.definition.property-benefit`, `general_object.fraud.element.property-benefit-concrete`

해석 메모: 재물 외 재산상 이익 branch는 경제적 가치 증가와 구체성을 함께 요구한다.

### `fraud.core_intent.component.fraud_intent_satisfied`

결론: **고의의 기망과 재산적 이득 목적이 함께 인정됨** (`fraud_intent_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`satisfied_fraud_intent_contract_breach_distinction(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`satisfied_fraud_mistake_gain_purpose(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_mistake.gain_purpose`

해석 메모: 단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적을 함께 요구한다.

### `fraud.profile_loan.component.fraud_intent_satisfied`

결론: **고의의 기망과 재산적 이득 목적이 함께 인정됨** (`fraud_intent_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. (`satisfied_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`satisfied_fraud_mistake_gain_purpose(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`, `fraud_mistake.gain_purpose`

해석 메모: 차용금 사건에서는 객관적 사정으로 추론한 편취 범의와 재산적 이득 목적을 결합한다.

### `fraud.stage_attempt_completion.component.no_separate_loss_gate`

결론: **재물 교부 또는 이익 취득 외에 현실적 재산상 손해를 별도 요건으로 요구하지 않음** (`fraud_no_separate_loss_gate(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 재물 교부 또는 재산상 이익의 취득이 인정됨 (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

해석 메모: 취득이 인정되면 현실적 손해를 별도 입력 gate로 다시 요구하지 않는다.

### `fraud.core_deception.card.001.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.causal-link.deception-property-disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. (`assess_deception_fraud_causal_link_deception_property_disposition(case_id, unknown_assessment_001, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_001)`)

근거 NormCard: `deception.fraud.causal-link.deception-property-disposition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.001.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.causal-link.deception-property-disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. (`assess_deception_fraud_causal_link_deception_property_disposition(case_id, positive_assessment_001, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_001)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망은 피기망자의 재산적 처분행위를 하게 하는 행위여야 한다. (`assess_deception_fraud_causal_link_deception_property_disposition(case_id, negative_assessment_001, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_001)`)

근거 NormCard: `deception.fraud.causal-link.deception-property-disposition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.002.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.causal-link.loan-purpose-not-sole-trigger)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. (`assess_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, unknown_assessment_002, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_002)`)

근거 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.002.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.causal-link.loan-purpose-not-sole-trigger)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. (`assess_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, positive_assessment_002, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_002)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. (`assess_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, negative_assessment_002, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_002)`)

근거 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.003.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.causal-link.no-disposition-no-deception)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. (`assess_deception_fraud_causal_link_no_disposition_no_deception(case_id, unknown_assessment_003, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_003)`)

근거 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.003.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.causal-link.no-disposition-no-deception)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. (`assess_deception_fraud_causal_link_no_disposition_no_deception(case_id, positive_assessment_003, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_003)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. (`assess_deception_fraud_causal_link_no_disposition_no_deception(case_id, negative_assessment_003, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_003)`)

근거 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.004.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deceived-person-unspecified)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. (`assess_deception_fraud_definition_deceived_person_unspecified(case_id, unknown_assessment_004, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_004)`)

근거 NormCard: `deception.fraud.definition.deceived-person-unspecified`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.004.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deceived-person-unspecified)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. (`assess_deception_fraud_definition_deceived_person_unspecified(case_id, positive_assessment_004, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_004)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 광고사기와 같이 기망행위의 상대방은 불특정인일 수 있다. (`assess_deception_fraud_definition_deceived_person_unspecified(case_id, negative_assessment_004, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_004)`)

근거 NormCard: `deception.fraud.definition.deceived-person-unspecified`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.005.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deceived-person-victim-distinct)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. (`assess_deception_fraud_definition_deceived_person_victim_distinct(case_id, unknown_assessment_005, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_005)`)

근거 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.005.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deceived-person-victim-distinct)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. (`assess_deception_fraud_definition_deceived_person_victim_distinct(case_id, positive_assessment_005, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_005)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망의 상대방과 재산상 피해자는 동일인일 것을 요하지 않는다. (`assess_deception_fraud_definition_deceived_person_victim_distinct(case_id, negative_assessment_005, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_005)`)

근거 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.006.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-content-basis-fact)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. (`assess_deception_fraud_definition_deception_content_basis_fact(case_id, unknown_assessment_006, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_006)`)

근거 NormCard: `deception.fraud.definition.deception-content-basis-fact`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.006.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-content-basis-fact)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. (`assess_deception_fraud_definition_deception_content_basis_fact(case_id, positive_assessment_006, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_006)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망의 내용은 재산적 처분행위를 하는 데 판단의 기초가 되는 사실이며, 외부적·객관적 사실과 내부적·심리적 사실을 포함한다. (`assess_deception_fraud_definition_deception_content_basis_fact(case_id, negative_assessment_006, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_006)`)

근거 NormCard: `deception.fraud.definition.deception-content-basis-fact`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.007.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-counterparty-is-other)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다. (`assess_deception_fraud_definition_deception_counterparty_is_other(case_id, unknown_assessment_007, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_007)`)

근거 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.007.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-counterparty-is-other)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다. (`assess_deception_fraud_definition_deception_counterparty_is_other(case_id, positive_assessment_007, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_007)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 기망의 상대방은 타인이다. (`assess_deception_fraud_definition_deception_counterparty_is_other(case_id, negative_assessment_007, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_007)`)

근거 NormCard: `deception.fraud.definition.deception-counterparty-is-other`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.008.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-good-faith-mistake)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`assess_deception_fraud_definition_deception_good_faith_mistake(case_id, unknown_assessment_008, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_008)`)

근거 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.008.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-good-faith-mistake)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`assess_deception_fraud_definition_deception_good_faith_mistake(case_id, positive_assessment_008, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_008)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`assess_deception_fraud_definition_deception_good_faith_mistake(case_id, negative_assessment_008, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_008)`)

근거 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.009.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-means-unrestricted)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. (`assess_deception_fraud_definition_deception_means_unrestricted(case_id, unknown_assessment_009, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_009)`)

근거 NormCard: `deception.fraud.definition.deception-means-unrestricted`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.009.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-means-unrestricted)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. (`assess_deception_fraud_definition_deception_means_unrestricted(case_id, positive_assessment_009, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_009)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망 수단에는 제한이 없으며, 언어·문서·거동, 적극적 주장·묵비, 작위·부작위 및 명시적·묵시적 방식 모두가 문제될 수 있다. (`assess_deception_fraud_definition_deception_means_unrestricted(case_id, negative_assessment_009, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_009)`)

근거 NormCard: `deception.fraud.definition.deception-means-unrestricted`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.010.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-object-facts)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. (`assess_deception_fraud_definition_deception_object_facts(case_id, unknown_assessment_010, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_010)`)

근거 NormCard: `deception.fraud.definition.deception-object-facts`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.010.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-object-facts)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. (`assess_deception_fraud_definition_deception_object_facts(case_id, positive_assessment_010, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_010)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산적 처분의 판단 기초사실이면 물건의 성질·품질 등 객관적 사실, 대금지급 의사 등 심리적 사실, 법률효력 등 법률적 사실 또는 민법상 무효인 법률행위에 관한 사실도 기망 대상이 될 수 있다. (`assess_deception_fraud_definition_deception_object_facts(case_id, negative_assessment_010, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_010)`)

근거 NormCard: `deception.fraud.definition.deception-object-facts`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.011.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.deception-target-human)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. (`assess_deception_fraud_definition_deception_target_human(case_id, unknown_assessment_011, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_011)`)

근거 NormCard: `deception.fraud.definition.deception-target-human`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.011.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.deception-target-human)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. (`assess_deception_fraud_definition_deception_target_human(case_id, positive_assessment_011, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_011)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. (`assess_deception_fraud_definition_deception_target_human(case_id, negative_assessment_011, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_011)`)

근거 NormCard: `deception.fraud.definition.deception-target-human`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.012.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.exploitation-existing-mistake)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. (`assess_deception_fraud_definition_exploitation_existing_mistake(case_id, unknown_assessment_012, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_012)`)

근거 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.012.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.exploitation-existing-mistake)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. (`assess_deception_fraud_definition_exploitation_existing_mistake(case_id, positive_assessment_012, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_012)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 이미 착오에 빠진 상태를 이용하는 행위가 신의칙 위반의 작위 또는 고지의무 있는 부작위로 평가되는 경우 기망행위가 될 수 있다. (`assess_deception_fraud_definition_exploitation_existing_mistake(case_id, negative_assessment_012, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_012)`)

근거 NormCard: `deception.fraud.definition.exploitation-existing-mistake`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.013.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.implicit-deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. (`assess_deception_fraud_definition_implicit_deception(case_id, unknown_assessment_013, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_013)`)

근거 NormCard: `deception.fraud.definition.implicit-deception`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.013.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.implicit-deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. (`assess_deception_fraud_definition_implicit_deception(case_id, positive_assessment_013, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_013)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 언어나 문서가 아니라 행동 또는 태도로 일정 사항에 관한 허위 외관을 표시하는 것을 의미한다. (`assess_deception_fraud_definition_implicit_deception(case_id, negative_assessment_013, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_013)`)

근거 NormCard: `deception.fraud.definition.implicit-deception`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.014.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.notice-duty-violation-omission)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. (`assess_deception_fraud_definition_notice_duty_violation_omission(case_id, unknown_assessment_014, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_014)`)

근거 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.014.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.notice-duty-violation-omission)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. (`assess_deception_fraud_definition_notice_duty_violation_omission(case_id, positive_assessment_014, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_014)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 고지의무를 위반하여 사실을 묵비하는 것은 작위에 의한 기망이 아니라 부작위에 의한 기망행위에 해당한다. (`assess_deception_fraud_definition_notice_duty_violation_omission(case_id, negative_assessment_014, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_014)`)

근거 NormCard: `deception.fraud.definition.notice-duty-violation-omission`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.015.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.definition.other-includes-corporation)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. (`assess_deception_fraud_definition_other_includes_corporation(case_id, unknown_assessment_015, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_015)`)

근거 NormCard: `deception.fraud.definition.other-includes-corporation`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.015.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.definition.other-includes-corporation)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. (`assess_deception_fraud_definition_other_includes_corporation(case_id, positive_assessment_015, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_015)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄에서 ‘타인’에는 법인이 포함되며, 법인도 사기죄의 피해자가 될 수 있다. (`assess_deception_fraud_definition_other_includes_corporation(case_id, negative_assessment_015, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_015)`)

근거 NormCard: `deception.fraud.definition.other-includes-corporation`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.016.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.deception-must-create-false-belief)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. (`assess_deception_fraud_element_deception_must_create_false_belief(case_id, unknown_assessment_016, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_016)`)

근거 NormCard: `deception.fraud.element.deception-must-create-false-belief`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.016.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.deception-must-create-false-belief)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. (`assess_deception_fraud_element_deception_must_create_false_belief(case_id, positive_assessment_016, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_016)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. (`assess_deception_fraud_element_deception_must_create_false_belief(case_id, negative_assessment_016, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_016)`)

근거 NormCard: `deception.fraud.element.deception-must-create-false-belief`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.017.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.deception-not-legal-act-important-part)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. (`assess_deception_fraud_element_deception_not_legal_act_important_part(case_id, unknown_assessment_017, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_017)`)

근거 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.017.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.deception-not-legal-act-important-part)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. (`assess_deception_fraud_element_deception_not_legal_act_important_part(case_id, positive_assessment_017, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_017)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 실행행위로서의 기망은 법률행위의 중요부분에 관한 것일 필요 없이 상대방의 재산적 처분을 위한 판단의 기초사실에 관한 기망이면 충분하다. (`assess_deception_fraud_element_deception_not_legal_act_important_part(case_id, negative_assessment_017, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_017)`)

근거 NormCard: `deception.fraud.element.deception-not-legal-act-important-part`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.018.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.loan-no-repayment-intent-or-ability)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. (`assess_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, unknown_assessment_018, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_018)`)

근거 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.018.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.loan-no-repayment-intent-or-ability)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. (`assess_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, positive_assessment_018, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_018)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 변제할 의사나 능력이 없는데도 금원을 차용하면 사기죄에 해당한다. (`assess_deception_fraud_element_loan_no_repayment_intent_or_ability(case_id, negative_assessment_018, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_018)`)

근거 NormCard: `deception.fraud.element.loan-no-repayment-intent-or-ability`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.019.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.omission-deception-guarantor-equivalence)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. (`assess_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, unknown_assessment_019, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_019)`)

근거 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.019.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.omission-deception-guarantor-equivalence)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. (`assess_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, positive_assessment_019, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_019)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 부작위에 의한 기망행위에서는 행위자가 상대방 착오를 제거할 보증인적 지위에 있고, 부작위가 작위에 의한 기망행위와 동가치를 가져야 한다. (`assess_deception_fraud_element_omission_deception_guarantor_equivalence(case_id, negative_assessment_019, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_019)`)

근거 NormCard: `deception.fraud.element.omission-deception-guarantor-equivalence`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.020.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.omission-deception-independent-error)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. (`assess_deception_fraud_element_omission_deception_independent_error(case_id, unknown_assessment_020, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_020)`)

근거 NormCard: `deception.fraud.element.omission-deception-independent-error`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.020.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.omission-deception-independent-error)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. (`assess_deception_fraud_element_omission_deception_independent_error(case_id, positive_assessment_020, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_020)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 부작위에 의한 기망행위에서는 상대방이 행위자와 관계없이 스스로 착오에 빠져 있어야 한다. (`assess_deception_fraud_element_omission_deception_independent_error(case_id, negative_assessment_020, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_020)`)

근거 NormCard: `deception.fraud.element.omission-deception-independent-error`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.021.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.omission-deception-legal-notice-duty)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. (`assess_deception_fraud_element_omission_deception_legal_notice_duty(case_id, unknown_assessment_021, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_021)`)

근거 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.021.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.omission-deception-legal-notice-duty)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. (`assess_deception_fraud_element_omission_deception_legal_notice_duty(case_id, positive_assessment_021, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_021)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 법률상 고지의무가 있는 자가 일정 사실을 고지하지 않아 상대방의 착오 상태를 계속시키고 이를 이용한 경우, 부작위에 의한 기망행위가 성립한다. (`assess_deception_fraud_element_omission_deception_legal_notice_duty(case_id, negative_assessment_021, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_021)`)

근거 NormCard: `deception.fraud.element.omission-deception-legal-notice-duty`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.022.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.transaction-purpose-no-impairment)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. (`assess_deception_fraud_element_transaction_purpose_no_impairment(case_id, unknown_assessment_022, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_022)`)

근거 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.022.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.transaction-purpose-no-impairment)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. (`assess_deception_fraud_element_transaction_purpose_no_impairment(case_id, positive_assessment_022, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_022)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. (`assess_deception_fraud_element_transaction_purpose_no_impairment(case_id, negative_assessment_022, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_022)`)

근거 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.023.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.element.victim-negligence-no-bar)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. (`assess_deception_fraud_element_victim_negligence_no_bar(case_id, unknown_assessment_023, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_023)`)

근거 NormCard: `deception.fraud.element.victim-negligence-no-bar`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.023.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.element.victim-negligence-no-bar)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. (`assess_deception_fraud_element_victim_negligence_no_bar(case_id, positive_assessment_023, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_023)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오가 상대방의 과실과 경합하더라도 사기죄는 성립할 수 있다. (`assess_deception_fraud_element_victim_negligence_no_bar(case_id, negative_assessment_023, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_023)`)

근거 NormCard: `deception.fraud.element.victim-negligence-no-bar`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.024.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.advertising-important-concrete-falsehood)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. (`assess_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, unknown_assessment_024, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_024)`)

근거 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.024.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.advertising-important-concrete-falsehood)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. (`assess_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, positive_assessment_024, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_024)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 거래의 중요한 사항에 관한 구체적 사실을 거래상 신의성실의무에 비추어 비난받을 정도의 방법으로 허위 고지한 경우, 과장·허위광고의 한계를 넘어 사기죄의 기망행위에 해당한다. (`assess_deception_fraud_standard_advertising_important_concrete_falsehood(case_id, negative_assessment_024, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_024)`)

근거 NormCard: `deception.fraud.standard.advertising-important-concrete-falsehood`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_advertising.card.025.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.advertising-tolerable-exaggeration)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. (`assess_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, unknown_assessment_025, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_025)`)

근거 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_advertising.card.025.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.advertising-tolerable-exaggeration)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. (`assess_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, positive_assessment_025, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_025)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. (`assess_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, negative_assessment_025, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_025)`)

근거 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.026.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.deception-concrete-circumstances)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. (`assess_deception_fraud_standard_deception_concrete_circumstances(case_id, unknown_assessment_026, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_026)`)

근거 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.026.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.deception-concrete-circumstances)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. (`assess_deception_fraud_standard_deception_concrete_circumstances(case_id, positive_assessment_026, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_026)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위가 상대방을 착오에 빠지게 한 기망인지 여부는 거래 상황, 상대방의 지식·경험·직업 등 행위 당시 구체적 사정을 고려하여 일반적·객관적으로 판단한다. (`assess_deception_fraud_standard_deception_concrete_circumstances(case_id, negative_assessment_026, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_026)`)

근거 NormCard: `deception.fraud.standard.deception-concrete-circumstances`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.027.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.easily-detectable-lie)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. (`assess_deception_fraud_standard_easily_detectable_lie(case_id, unknown_assessment_027, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_027)`)

근거 NormCard: `deception.fraud.standard.easily-detectable-lie`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.027.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.easily-detectable-lie)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. (`assess_deception_fraud_standard_easily_detectable_lie(case_id, positive_assessment_027, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_027)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. (`assess_deception_fraud_standard_easily_detectable_lie(case_id, negative_assessment_027, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_027)`)

근거 NormCard: `deception.fraud.standard.easily-detectable-lie`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.028.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.implicit-deception-explanatory-value)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. (`assess_deception_fraud_standard_implicit_deception_explanatory_value(case_id, unknown_assessment_028, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_028)`)

근거 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.028.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.implicit-deception-explanatory-value)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. (`assess_deception_fraud_standard_implicit_deception_explanatory_value(case_id, positive_assessment_028, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_028)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 묵시적 기망행위는 행위자 전체행위가 설명가치를 가질 때 인정되며, 그 설명가치는 거래관행과 사회통념으로 결정된다. (`assess_deception_fraud_standard_implicit_deception_explanatory_value(case_id, negative_assessment_028, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_028)`)

근거 NormCard: `deception.fraud.standard.implicit-deception-explanatory-value`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_implicit_deception.card.029.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.implicit-omission-deception-distinction)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. (`assess_deception_fraud_standard_implicit_omission_deception_distinction(case_id, unknown_assessment_029, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_029)`)

근거 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_implicit_deception.card.029.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.implicit-omission-deception-distinction)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. (`assess_deception_fraud_standard_implicit_omission_deception_distinction(case_id, positive_assessment_029, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_029)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자의 침묵이 거래관행·사회통념상 일정 사항을 표시하는 설명가치를 가져 묵시적 기망으로 평가되는지를 먼저 검토하고, 그렇지 않은 침묵은 보증인적 지위와 고지의무가 있는 경우에 한하여 부작위 기망이 될 수 있다. (`assess_deception_fraud_standard_implicit_omission_deception_distinction(case_id, negative_assessment_029, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_029)`)

근거 NormCard: `deception.fraud.standard.implicit-omission-deception-distinction`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.030.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.intent-to-defraud-loan-inference)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. (`assess_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, unknown_assessment_030, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_030)`)

근거 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.030.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.intent-to-defraud-loan-inference)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. (`assess_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, positive_assessment_030, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_030)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 차용금 사기에서 편취의 범의는 피고인의 자백이 없으면 범행 전후 재력, 환경, 범행 내용, 거래 이행과정, 피해자와의 관계 등 객관적 사정을 종합하여 판단한다. (`assess_deception_fraud_standard_intent_to_defraud_loan_inference(case_id, negative_assessment_030, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_030)`)

근거 NormCard: `deception.fraud.standard.intent-to-defraud-loan-inference`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.031.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.loan-lender-anticipated-risk)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. (`assess_deception_fraud_standard_loan_lender_anticipated_risk(case_id, unknown_assessment_031, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_031)`)

근거 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.031.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.loan-lender-anticipated-risk)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. (`assess_deception_fraud_standard_loan_lender_anticipated_risk(case_id, positive_assessment_031, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_031)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. (`assess_deception_fraud_standard_loan_lender_anticipated_risk(case_id, negative_assessment_031, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_031)`)

근거 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.032.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.loan-purpose-materiality)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. (`assess_deception_fraud_standard_loan_purpose_materiality(case_id, unknown_assessment_032, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_032)`)

근거 NormCard: `deception.fraud.standard.loan-purpose-materiality`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.032.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.loan-purpose-materiality)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. (`assess_deception_fraud_standard_loan_purpose_materiality(case_id, positive_assessment_032, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_032)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 용도를 속여 돈을 빌린 경우, 진정한 용도를 고지했더라면 상대방이 대여하지 않았을 관계에 있으면 사기죄가 성립한다. (`assess_deception_fraud_standard_loan_purpose_materiality(case_id, negative_assessment_032, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_032)`)

근거 NormCard: `deception.fraud.standard.loan-purpose-materiality`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.card.033.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.loan-subsequent-default)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. (`assess_deception_fraud_standard_loan_subsequent_default(case_id, unknown_assessment_033, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_033)`)

근거 NormCard: `deception.fraud.standard.loan-subsequent-default`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_loan.card.033.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.loan-subsequent-default)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. (`assess_deception_fraud_standard_loan_subsequent_default(case_id, positive_assessment_033, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_033)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. (`assess_deception_fraud_standard_loan_subsequent_default(case_id, negative_assessment_033, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_033)`)

근거 NormCard: `deception.fraud.standard.loan-subsequent-default`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.034.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.precedent-notice-duty-materiality)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. (`assess_deception_fraud_standard_precedent_notice_duty_materiality(case_id, unknown_assessment_034, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_034)`)

근거 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.034.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.precedent-notice-duty-materiality)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. (`assess_deception_fraud_standard_precedent_notice_duty_materiality(case_id, positive_assessment_034, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_034)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 고지의무가 인정된다고 본다. (`assess_deception_fraud_standard_precedent_notice_duty_materiality(case_id, negative_assessment_034, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_034)`)

근거 NormCard: `deception.fraud.standard.precedent-notice-duty-materiality`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_deception.card.035.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, deception.fraud.standard.vague-opinion-not-deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. (`assess_deception_fraud_standard_vague_opinion_not_deception(case_id, unknown_assessment_035, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_035)`)

근거 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_deception.card.035.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, deception.fraud.standard.vague-opinion-not-deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. (`assess_deception_fraud_standard_vague_opinion_not_deception(case_id, positive_assessment_035, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_035)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. (`assess_deception_fraud_standard_vague_opinion_not_deception(case_id, negative_assessment_035, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_035)`)

근거 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.036.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.delivery_factual_control)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. (`assess_fraud_damage_acquisition_delivery_factual_control(case_id, unknown_assessment_036, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_036)`)

근거 NormCard: `fraud_damage_acquisition.delivery_factual_control`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.036.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.delivery_factual_control)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. (`assess_fraud_damage_acquisition_delivery_factual_control(case_id, positive_assessment_036, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_036)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재물의 현실 인도가 없더라도 재물이 범인의 사실상 지배 아래 들어가 자유로운 처분이 가능한 상태가 되면 재물의 교부가 있다. (`assess_fraud_damage_acquisition_delivery_factual_control(case_id, negative_assessment_036, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_036)`)

근거 NormCard: `fraud_damage_acquisition.delivery_factual_control`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.037.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.delivery_of_property)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. (`assess_fraud_damage_acquisition_delivery_of_property(case_id, unknown_assessment_037, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_037)`)

근거 NormCard: `fraud_damage_acquisition.delivery_of_property`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.037.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.delivery_of_property)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. (`assess_fraud_damage_acquisition_delivery_of_property(case_id, positive_assessment_037, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_037)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에서 재물의 교부는 범인의 기망에 따라 피해자가 착오로 재물에 대한 사실상 지배를 범인에게 이전하는 것이다. (`assess_fraud_damage_acquisition_delivery_of_property(case_id, negative_assessment_037, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_037)`)

근거 NormCard: `fraud_damage_acquisition.delivery_of_property`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.038.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.money_delivery_full_amount)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. (`assess_fraud_damage_acquisition_money_delivery_full_amount(case_id, unknown_assessment_038, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_038)`)

근거 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.038.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.money_delivery_full_amount)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. (`assess_fraud_damage_acquisition_money_delivery_full_amount(case_id, positive_assessment_038, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_038)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 금원 편취 사기에서 피해자가 기망으로 교부한 금원과 관련하여 상당한 대가가 일부 지급되었더라도 이를 공제하지 않고, 편취액은 교부받은 금원 전부로 본다. (`assess_fraud_damage_acquisition_money_delivery_full_amount(case_id, negative_assessment_038, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_038)`)

근거 NormCard: `fraud_damage_acquisition.money_delivery_full_amount`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.039.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.property_concept_reported_precedent)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. (`assess_fraud_damage_acquisition_property_concept_reported_precedent(case_id, unknown_assessment_039, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_039)`)

근거 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.039.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.property_concept_reported_precedent)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. (`assess_fraud_damage_acquisition_property_concept_reported_precedent(case_id, positive_assessment_039, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_039)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 외형상 재산상 이익을 취득하면 족하다. (`assess_fraud_damage_acquisition_property_concept_reported_precedent(case_id, negative_assessment_039, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_039)`)

근거 NormCard: `fraud_damage_acquisition.property_concept_reported_precedent`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.040.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.property_disposition_types)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. (`assess_fraud_damage_acquisition_property_disposition_types(case_id, unknown_assessment_040, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_040)`)

근거 NormCard: `fraud_damage_acquisition.property_disposition_types`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.040.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.property_disposition_types)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. (`assess_fraud_damage_acquisition_property_disposition_types(case_id, positive_assessment_040, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_040)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익에 대한 처분행위에는 계약 체결, 노무 제공, 채무면제 의사표시 등 이익을 취득하게 하는 일체의 행위가 포함된다. (`assess_fraud_damage_acquisition_property_disposition_types(case_id, negative_assessment_040, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_040)`)

근거 NormCard: `fraud_damage_acquisition.property_disposition_types`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.041.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.property_loss_negative_view)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. (`assess_fraud_damage_acquisition_property_loss_negative_view(case_id, unknown_assessment_041, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_041)`)

근거 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.041.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.property_loss_negative_view)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. (`assess_fraud_damage_acquisition_property_loss_negative_view(case_id, positive_assessment_041, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_041)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, 상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다. (`assess_fraud_damage_acquisition_property_loss_negative_view(case_id, negative_assessment_041, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_041)`)

근거 NormCard: `fraud_damage_acquisition.property_loss_negative_view`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.042.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.protected_economic_interest)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. (`assess_fraud_damage_acquisition_protected_economic_interest(case_id, unknown_assessment_042, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_042)`)

근거 NormCard: `fraud_damage_acquisition.protected_economic_interest`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.042.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.protected_economic_interest)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. (`assess_fraud_damage_acquisition_protected_economic_interest(case_id, positive_assessment_042, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_042)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체인 재산상 이익은 사법상 보호되는 경제적 이익에 한정되지 않고, 사법상 보호되지 않는 경제적 이익도 경제적 이익이면 포함된다. (`assess_fraud_damage_acquisition_protected_economic_interest(case_id, negative_assessment_042, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_042)`)

근거 NormCard: `fraud_damage_acquisition.protected_economic_interest`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_rights_exercise.card.043.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.right_exercise_unacceptable_deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. (`assess_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, unknown_assessment_043, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_043)`)

근거 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_rights_exercise.card.043.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.right_exercise_unacceptable_deception)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. (`assess_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, positive_assessment_043, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_043)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망을 수단으로 한 권리행사라도 그 수단이 사회통념상 권리행사 수단으로 용인될 정도를 넘어서는 경우 권리행사에 속하는 행위도 사기죄에 해당한다. (`assess_fraud_damage_acquisition_right_exercise_unacceptable_deception(case_id, negative_assessment_043, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_043)`)

근거 NormCard: `fraud_damage_acquisition.right_exercise_unacceptable_deception`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.044.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_damage_acquisition.subsequent_return_irrelevant)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. (`assess_fraud_damage_acquisition_subsequent_return_irrelevant(case_id, unknown_assessment_044, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_044)`)

근거 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.044.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_damage_acquisition.subsequent_return_irrelevant)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. (`assess_fraud_damage_acquisition_subsequent_return_irrelevant(case_id, positive_assessment_044, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_044)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 재물을 편취한 경우 상당한 대가 제공, 사후 반환·변상, 전체 재산 손해 부재 또는 사후 합의는 사기죄 성립에 영향을 주지 않는다. (`assess_fraud_damage_acquisition_subsequent_return_irrelevant(case_id, negative_assessment_044, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_044)`)

근거 NormCard: `fraud_damage_acquisition.subsequent_return_irrelevant`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.045.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_general_object.causation_required)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. (`assess_fraud_general_object_causation_required(case_id, unknown_assessment_045, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_045)`)

근거 NormCard: `fraud_general_object.causation_required`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.045.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_general_object.causation_required)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. (`assess_fraud_general_object_causation_required(case_id, positive_assessment_045, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_045)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. (`assess_fraud_general_object_causation_required(case_id, negative_assessment_045, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_045)`)

근거 NormCard: `fraud_general_object.causation_required`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.046.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_general_object.deception_error_causation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. (`assess_fraud_general_object_deception_error_causation(case_id, unknown_assessment_046, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_046)`)

근거 NormCard: `fraud_general_object.deception_error_causation`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.046.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_general_object.deception_error_causation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. (`assess_fraud_general_object_deception_error_causation(case_id, positive_assessment_046, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_046)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. (`assess_fraud_general_object_deception_error_causation(case_id, negative_assessment_046, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_046)`)

근거 NormCard: `fraud_general_object.deception_error_causation`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.047.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.contract_breach_distinction)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`assess_fraud_intent_contract_breach_distinction(case_id, unknown_assessment_047, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_047)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.047.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.contract_breach_distinction)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`assess_fraud_intent_contract_breach_distinction(case_id, positive_assessment_047, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_047)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`assess_fraud_intent_contract_breach_distinction(case_id, negative_assessment_047, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_047)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.048.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.illegal_appropriation_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. (`assess_fraud_intent_illegal_appropriation_definition(case_id, unknown_assessment_048, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_048)`)

근거 NormCard: `fraud_intent.illegal_appropriation_definition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.048.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.illegal_appropriation_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. (`assess_fraud_intent_illegal_appropriation_definition(case_id, positive_assessment_048, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_048)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 불법영득의사는 타인의 물건을 자기 것으로 삼으려는 의사뿐 아니라 그 경제적 용법에 따라 일시적으로 이용 또는 처분하려는 의사도 포함하며, 영구 보유 의사가 반드시 필요한 것은 아니다. (`assess_fraud_intent_illegal_appropriation_definition(case_id, negative_assessment_048, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_048)`)

근거 NormCard: `fraud_intent.illegal_appropriation_definition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.049.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.no_disposition_inducement_intent)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. (`assess_fraud_intent_no_disposition_inducement_intent(case_id, unknown_assessment_049, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_049)`)

근거 NormCard: `fraud_intent.no_disposition_inducement_intent`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.049.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.no_disposition_inducement_intent)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. (`assess_fraud_intent_no_disposition_inducement_intent(case_id, positive_assessment_049, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_049)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. (`assess_fraud_intent_no_disposition_inducement_intent(case_id, negative_assessment_049, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_049)`)

근거 NormCard: `fraud_intent.no_disposition_inducement_intent`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.050.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.precedent_illegal_appropriation_intent)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. (`assess_fraud_intent_precedent_illegal_appropriation_intent(case_id, unknown_assessment_050, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_050)`)

근거 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.050.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.precedent_illegal_appropriation_intent)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. (`assess_fraud_intent_precedent_illegal_appropriation_intent(case_id, positive_assessment_050, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_050)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 판례는 사기죄의 주관적 요건으로 고의 외에 불법영득의사가 필요하다는 입장이다. (`assess_fraud_intent_precedent_illegal_appropriation_intent(case_id, negative_assessment_050, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_050)`)

근거 NormCard: `fraud_intent.precedent_illegal_appropriation_intent`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_third_party_acquisition.card.051.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.third_party_acquisition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. (`assess_fraud_intent_third_party_acquisition(case_id, unknown_assessment_051, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_051)`)

근거 NormCard: `fraud_intent.third_party_acquisition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_third_party_acquisition.card.051.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.third_party_acquisition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. (`assess_fraud_intent_third_party_acquisition(case_id, positive_assessment_051, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_051)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 행위자가 기망으로 스스로 재물을 취득하지 않고 제3자로 하여금 교부받게 한 경우 사기죄가 성립하려면, 제3자가 정을 모르는 도구 또는 범인의 이익을 위해 행동하는 대리인이거나, 적어도 행위자에게 제3자로 하여금 재물을 취득하게 할 의사가 있어야 한다. (`assess_fraud_intent_third_party_acquisition(case_id, negative_assessment_051, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_051)`)

근거 NormCard: `fraud_intent.third_party_acquisition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.052.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_intent.time_of_conduct)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 편취의 범의는 행위 당시를 기준으로 판단한다. (`assess_fraud_intent_time_of_conduct(case_id, unknown_assessment_052, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_052)`)

근거 NormCard: `fraud_intent.time_of_conduct`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.052.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_intent.time_of_conduct)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 편취의 범의는 행위 당시를 기준으로 판단한다. (`assess_fraud_intent_time_of_conduct(case_id, positive_assessment_052, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_052)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 편취의 범의는 행위 당시를 기준으로 판단한다. (`assess_fraud_intent_time_of_conduct(case_id, negative_assessment_052, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_052)`)

근거 NormCard: `fraud_intent.time_of_conduct`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.053.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.conscious_nonexercise)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. (`assess_fraud_mistake_conscious_nonexercise(case_id, unknown_assessment_053, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_053)`)

근거 NormCard: `fraud_mistake.conscious_nonexercise`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.053.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.conscious_nonexercise)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. (`assess_fraud_mistake_conscious_nonexercise(case_id, positive_assessment_053, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_053)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 착오 때문에 채권을 의식적으로 행사하지 않았고 그 부작위가 행위자에게 직접 재산상 이익을 부여한 경우, 그 부작위는 재산적 처분행위가 될 수 있다. (`assess_fraud_mistake_conscious_nonexercise(case_id, negative_assessment_053, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_053)`)

근거 NormCard: `fraud_mistake.conscious_nonexercise`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.054.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.deceived_disposer_identity)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다. (`assess_fraud_mistake_deceived_disposer_identity(case_id, unknown_assessment_054, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_054)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.054.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.deceived_disposer_identity)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다. (`assess_fraud_mistake_deceived_disposer_identity(case_id, positive_assessment_054, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_054)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다. (`assess_fraud_mistake_deceived_disposer_identity(case_id, negative_assessment_054, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_054)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.055.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.disposition_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`assess_fraud_mistake_disposition_definition(case_id, unknown_assessment_055, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_055)`)

근거 NormCard: `fraud_mistake.disposition_definition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.055.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.disposition_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`assess_fraud_mistake_disposition_definition(case_id, positive_assessment_055, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_055)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`assess_fraud_mistake_disposition_definition(case_id, negative_assessment_055, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_055)`)

근거 NormCard: `fraud_mistake.disposition_definition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.056.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.disposition_directness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. (`assess_fraud_mistake_disposition_directness(case_id, unknown_assessment_056, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_056)`)

근거 NormCard: `fraud_mistake.disposition_directness`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.056.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.disposition_directness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. (`assess_fraud_mistake_disposition_directness(case_id, positive_assessment_056, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_056)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산의 감소는 처분행위로부터 직접 야기되어야 하며, 처분행위의 직접성은 기망행위가 최후 처분행위자에게까지 미치면 인정된다. (`assess_fraud_mistake_disposition_directness(case_id, negative_assessment_056, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_056)`)

근거 NormCard: `fraud_mistake.disposition_directness`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.057.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.disposition_intent_act_awareness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. (`assess_fraud_mistake_disposition_intent_act_awareness(case_id, unknown_assessment_057, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_057)`)

근거 NormCard: `fraud_mistake.disposition_intent_act_awareness`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.057.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.disposition_intent_act_awareness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. (`assess_fraud_mistake_disposition_intent_act_awareness(case_id, positive_assessment_057, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_057)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 처분행위의 의미나 내용을 인식하지 못했더라도, 그 작위 또는 부작위가 직접 재산상 손해를 초래하는 재산적 처분행위로 평가되고 피기망자가 그 행위를 인식하여 한 경우에는 처분행위에 상응하는 처분의사가 인정된다. (`assess_fraud_mistake_disposition_intent_act_awareness(case_id, negative_assessment_057, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_057)`)

근거 NormCard: `fraud_mistake.disposition_intent_act_awareness`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.058.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.disposition_omission)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. (`assess_fraud_mistake_disposition_omission(case_id, unknown_assessment_058, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_058)`)

근거 NormCard: `fraud_mistake.disposition_omission`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.058.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.disposition_omission)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. (`assess_fraud_mistake_disposition_omission(case_id, positive_assessment_058, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_058)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 직접 재산상 손해를 초래하는 부작위도 처분행위가 될 수 있다. (`assess_fraud_mistake_disposition_omission(case_id, negative_assessment_058, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_058)`)

근거 NormCard: `fraud_mistake.disposition_omission`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.059.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.error_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오란 사실과 일치하지 않는 인식을 의미한다. (`assess_fraud_mistake_error_definition(case_id, unknown_assessment_059, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_059)`)

근거 NormCard: `fraud_mistake.error_definition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.059.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.error_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오란 사실과 일치하지 않는 인식을 의미한다. (`assess_fraud_mistake_error_definition(case_id, positive_assessment_059, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_059)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오란 사실과 일치하지 않는 인식을 의미한다. (`assess_fraud_mistake_error_definition(case_id, negative_assessment_059, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_059)`)

근거 NormCard: `fraud_mistake.error_definition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.060.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.error_disposition_motivation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. (`assess_fraud_mistake_error_disposition_motivation(case_id, unknown_assessment_060, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_060)`)

근거 NormCard: `fraud_mistake.error_disposition_motivation`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.060.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.error_disposition_motivation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. (`assess_fraud_mistake_error_disposition_motivation(case_id, positive_assessment_060, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_060)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오는 재산적 처분행위를 하도록 동기를 확정하게 하는 것으로 충분하며, 법률행위 내용에 관한 착오인지 동기에 관한 착오인지는 묻지 않는다. (`assess_fraud_mistake_error_disposition_motivation(case_id, negative_assessment_060, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_060)`)

근거 NormCard: `fraud_mistake.error_disposition_motivation`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.061.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.error_doubt_ignorance)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. (`assess_fraud_mistake_error_doubt_ignorance(case_id, unknown_assessment_061, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_061)`)

근거 NormCard: `fraud_mistake.error_doubt_ignorance`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.061.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.error_doubt_ignorance)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. (`assess_fraud_mistake_error_doubt_ignorance(case_id, positive_assessment_061, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_061)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사실을 잘못 확신하는 경우뿐 아니라 어느 것이 맞는지 의심하는 경우에도 착오가 인정될 수 있고, 사실의 부지도 착오에 해당한다. (`assess_fraud_mistake_error_doubt_ignorance(case_id, negative_assessment_061, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_061)`)

근거 NormCard: `fraud_mistake.error_doubt_ignorance`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.062.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.factual_act_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. (`assess_fraud_mistake_factual_act_disposition(case_id, unknown_assessment_062, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_062)`)

근거 NormCard: `fraud_mistake.factual_act_disposition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.062.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.factual_act_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. (`assess_fraud_mistake_factual_act_disposition(case_id, positive_assessment_062, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_062)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자의 의사에 기초한 사실행위가 행위자 등에게 재물 또는 재산상 이익을 직접 이전하는 경우, 그 사실행위도 처분행위가 될 수 있다. (`assess_fraud_mistake_factual_act_disposition(case_id, negative_assessment_062, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_062)`)

근거 NormCard: `fraud_mistake.factual_act_disposition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_intent.card.063.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.gain_purpose)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`assess_fraud_mistake_gain_purpose(case_id, unknown_assessment_063, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_063)`)

근거 NormCard: `fraud_mistake.gain_purpose`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_intent.card.063.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.gain_purpose)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`assess_fraud_mistake_gain_purpose(case_id, positive_assessment_063, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_063)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`assess_fraud_mistake_gain_purpose(case_id, negative_assessment_063, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_063)`)

근거 NormCard: `fraud_mistake.gain_purpose`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.064.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.invalid_act_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. (`assess_fraud_mistake_invalid_act_disposition(case_id, unknown_assessment_064, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_064)`)

근거 NormCard: `fraud_mistake.invalid_act_disposition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.064.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.invalid_act_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. (`assess_fraud_mistake_invalid_act_disposition(case_id, positive_assessment_064, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_064)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 착오에 의한 재산적 처분행위가 민법상 취소 가능하거나 그 법률행위가 무효여도 사기죄의 처분행위 성립에는 영향이 없다. (`assess_fraud_mistake_invalid_act_disposition(case_id, negative_assessment_064, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_064)`)

근거 NormCard: `fraud_mistake.invalid_act_disposition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.065.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.no_capacity_theft)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_no_capacity_theft(case_id, unknown_assessment_065, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_065)`)

근거 NormCard: `fraud_mistake.no_capacity_theft`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.065.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.no_capacity_theft)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_no_capacity_theft(case_id, positive_assessment_065, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_065)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_no_capacity_theft(case_id, negative_assessment_065, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_065)`)

근거 NormCard: `fraud_mistake.no_capacity_theft`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.066.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.no_thought_no_error)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. (`assess_fraud_mistake_no_thought_no_error(case_id, unknown_assessment_066, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_066)`)

근거 NormCard: `fraud_mistake.no_thought_no_error`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.066.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.no_thought_no_error)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. (`assess_fraud_mistake_no_thought_no_error(case_id, positive_assessment_066, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_066)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. (`assess_fraud_mistake_no_thought_no_error(case_id, negative_assessment_066, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_066)`)

근거 NormCard: `fraud_mistake.no_thought_no_error`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_omission.card.067.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.omission_not_all_nonclaims)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. (`assess_fraud_mistake_omission_not_all_nonclaims(case_id, unknown_assessment_067, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_067)`)

근거 NormCard: `fraud_mistake.omission_not_all_nonclaims`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_omission.card.067.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.omission_not_all_nonclaims)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. (`assess_fraud_mistake_omission_not_all_nonclaims(case_id, positive_assessment_067, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_067)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. (`assess_fraud_mistake_omission_not_all_nonclaims(case_id, negative_assessment_067, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_067)`)

근거 NormCard: `fraud_mistake.omission_not_all_nonclaims`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.068.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.property_disposition_element)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`assess_fraud_mistake_property_disposition_element(case_id, unknown_assessment_068, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_068)`)

근거 NormCard: `fraud_mistake.property_disposition_element`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.068.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.property_disposition_element)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`assess_fraud_mistake_property_disposition_element(case_id, positive_assessment_068, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_068)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`assess_fraud_mistake_property_disposition_element(case_id, negative_assessment_068, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_068)`)

근거 NormCard: `fraud_mistake.property_disposition_element`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.069.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.property_limited_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. (`assess_fraud_mistake_property_limited_disposition(case_id, unknown_assessment_069, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_069)`)

근거 NormCard: `fraud_mistake.property_limited_disposition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.069.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.property_limited_disposition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. (`assess_fraud_mistake_property_limited_disposition(case_id, positive_assessment_069, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_069)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. (`assess_fraud_mistake_property_limited_disposition(case_id, negative_assessment_069, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_069)`)

근거 NormCard: `fraud_mistake.property_limited_disposition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.070.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.sequential_causation)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`assess_fraud_mistake_sequential_causation(case_id, unknown_assessment_070, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_070)`)

근거 NormCard: `fraud_mistake.sequential_causation`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.070.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.sequential_causation)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`assess_fraud_mistake_sequential_causation(case_id, positive_assessment_070, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_070)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`assess_fraud_mistake_sequential_causation(case_id, negative_assessment_070, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_070)`)

근거 NormCard: `fraud_mistake.sequential_causation`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.071.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.triangular_fraud_definition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. (`assess_fraud_mistake_triangular_fraud_definition(case_id, unknown_assessment_071, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_071)`)

근거 NormCard: `fraud_mistake.triangular_fraud_definition`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.071.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.triangular_fraud_definition)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. (`assess_fraud_mistake_triangular_fraud_definition(case_id, positive_assessment_071, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_071)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. (`assess_fraud_mistake_triangular_fraud_definition(case_id, negative_assessment_071, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_071)`)

근거 NormCard: `fraud_mistake.triangular_fraud_definition`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.072.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.trick_theft_directness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_trick_theft_directness(case_id, unknown_assessment_072, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_072)`)

근거 NormCard: `fraud_mistake.trick_theft_directness`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.072.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.trick_theft_directness)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_trick_theft_directness(case_id, positive_assessment_072, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_072)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. (`assess_fraud_mistake_trick_theft_directness(case_id, negative_assessment_072, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_072)`)

근거 NormCard: `fraud_mistake.trick_theft_directness`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.core_mistake_disposition.card.073.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_mistake.unaware_error)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. (`assess_fraud_mistake_unaware_error(case_id, unknown_assessment_073, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_073)`)

근거 NormCard: `fraud_mistake.unaware_error`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.core_mistake_disposition.card.073.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_mistake.unaware_error)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. (`assess_fraud_mistake_unaware_error(case_id, positive_assessment_073, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_073)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자가 진실을 알고 있어 허위임을 인식한 경우에는 착오가 아니지만, 어느 것이 진실인지 의심하는 데 그친 경우에는 착오가 인정될 수 있다. (`assess_fraud_mistake_unaware_error(case_id, negative_assessment_073, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_073)`)

근거 NormCard: `fraud_mistake.unaware_error`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.074.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_stages_participation.attempt_deceptive_act)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. (`assess_fraud_stages_participation_attempt_deceptive_act(case_id, unknown_assessment_074, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_074)`)

근거 NormCard: `fraud_stages_participation.attempt_deceptive_act`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.074.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_stages_participation.attempt_deceptive_act)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. (`assess_fraud_stages_participation_attempt_deceptive_act(case_id, positive_assessment_074, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_074)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사람을 기망하는 행위가 착수되면 사기죄의 실행의 착수가 있으며, 상대방이 실제 착오에 빠질 필요는 없다. (`assess_fraud_stages_participation_attempt_deceptive_act(case_id, negative_assessment_074, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_074)`)

근거 NormCard: `fraud_stages_participation.attempt_deceptive_act`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.075.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_stages_participation.completion_deception_disposition_transfer)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id, unknown_assessment_075, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_075)`)

근거 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.075.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_stages_participation.completion_deception_disposition_transfer)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id, positive_assessment_075, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_075)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id, negative_assessment_075, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_075)`)

근거 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.076.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_stages_participation.no_causation_attempt)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. (`assess_fraud_stages_participation_no_causation_attempt(case_id, unknown_assessment_076, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_076)`)

근거 NormCard: `fraud_stages_participation.no_causation_attempt`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.076.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_stages_participation.no_causation_attempt)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. (`assess_fraud_stages_participation_no_causation_attempt(case_id, positive_assessment_076, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_076)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. (`assess_fraud_stages_participation_no_causation_attempt(case_id, negative_assessment_076, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_076)`)

근거 NormCard: `fraud_stages_participation.no_causation_attempt`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.077.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, fraud_stages_participation.property_fraud_completion_control)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. (`assess_fraud_stages_participation_property_fraud_completion_control(case_id, unknown_assessment_077, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_077)`)

근거 NormCard: `fraud_stages_participation.property_fraud_completion_control`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.077.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, fraud_stages_participation.property_fraud_completion_control)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. (`assess_fraud_stages_participation_property_fraud_completion_control(case_id, positive_assessment_077, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_077)`)
- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 재물 편취는 피해자의 지배를 배제하고 자기 또는 제3자의 지배를 인정한 때 기수에 이른다. (`assess_fraud_stages_participation_property_fraud_completion_control(case_id, negative_assessment_077, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_077)`)

근거 NormCard: `fraud_stages_participation.property_fraud_completion_control`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.078.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.definition.property-benefit)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. (`assess_general_object_fraud_definition_property_benefit(case_id, unknown_assessment_078, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_078)`)

근거 NormCard: `general_object.fraud.definition.property-benefit`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.078.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.definition.property-benefit)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. (`assess_general_object_fraud_definition_property_benefit(case_id, positive_assessment_078, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_078)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 재물 이외의 것으로서 재산의 경제적 가치 증가를 의미하며, 적극적·소극적, 일시적·영구적 이익을 모두 포함한다. (`assess_general_object_fraud_definition_property_benefit(case_id, negative_assessment_078, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_078)`)

근거 NormCard: `general_object.fraud.definition.property-benefit`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.079.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.definition.property-benefit-not-numerically-limited)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. (`assess_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id, unknown_assessment_079, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_079)`)

근거 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.079.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.definition.property-benefit-not-numerically-limited)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. (`assess_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id, positive_assessment_079, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_079)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 숫자로 산출할 수 있는 이익에 한정되지 않는다. (`assess_general_object_fraud_definition_property_benefit_not_numerically_limited(case_id, negative_assessment_079, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_079)`)

근거 NormCard: `general_object.fraud.definition.property-benefit-not-numerically-limited`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.080.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.element.object-other-possessed-other-property)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`assess_general_object_fraud_element_object_other_possessed_other_property(case_id, unknown_assessment_080, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_080)`)

근거 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.080.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.element.object-other-possessed-other-property)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`assess_general_object_fraud_element_object_other_possessed_other_property(case_id, positive_assessment_080, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_080)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`assess_general_object_fraud_element_object_other_possessed_other_property(case_id, negative_assessment_080, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_080)`)

근거 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_benefit.card.081.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.element.property-benefit-concrete)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다. (`assess_general_object_fraud_element_property_benefit_concrete(case_id, unknown_assessment_081, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_081)`)

근거 NormCard: `general_object.fraud.element.property-benefit-concrete`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_benefit.card.081.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.element.property-benefit-concrete)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다. (`assess_general_object_fraud_element_property_benefit_concrete(case_id, positive_assessment_081, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_081)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 재산상 이익은 구체적인 이익이어야 한다. (`assess_general_object_fraud_element_property_benefit_concrete(case_id, negative_assessment_081, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_081)`)

근거 NormCard: `general_object.fraud.element.property-benefit-concrete`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_public_interest.card.082.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.exception.public-interest-property-equivalence)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. (`assess_general_object_fraud_exception_public_interest_property_equivalence(case_id, unknown_assessment_082, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_082)`)

근거 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_public_interest.card.082.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.exception.public-interest-property-equivalence)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. (`assess_general_object_fraud_exception_public_interest_property_equivalence(case_id, positive_assessment_082, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_082)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망으로 국가적·공공적 법익을 침해한 경우에도 그 침해가 동시에 재산권 침해와 동일하게 평가되고 해당 행위를 사기죄보다 특별하게 처벌하는 별도 규정이 없는 때에 한하여 사기죄가 성립할 수 있다. (`assess_general_object_fraud_exception_public_interest_property_equivalence(case_id, negative_assessment_082, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_082)`)

근거 NormCard: `general_object.fraud.exception.public-interest-property-equivalence`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.stage_attempt_completion.card.083.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.standard.later-cancellation-no-effect)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. (`assess_general_object_fraud_standard_later_cancellation_no_effect(case_id, unknown_assessment_083, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_083)`)

근거 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.stage_attempt_completion.card.083.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.standard.later-cancellation-no-effect)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. (`assess_general_object_fraud_standard_later_cancellation_no_effect(case_id, positive_assessment_083, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_083)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기로 인한 재산 처분이 처분시점에 기수에 이른 경우, 사후에 이루어진 의사표시 취소는 범죄성립에 영향을 미칠 수 없다. (`assess_general_object_fraud_standard_later_cancellation_no_effect(case_id, negative_assessment_083, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_083)`)

근거 NormCard: `general_object.fraud.standard.later-cancellation-no-effect`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.boundary_other_offenses.card.084.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.standard.own-possession-other-property-embezzlement)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. (`assess_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, unknown_assessment_084, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_084)`)

근거 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.boundary_other_offenses.card.084.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.standard.own-possession-other-property-embezzlement)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. (`assess_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, positive_assessment_084, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_084)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. (`assess_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, negative_assessment_084, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_084)`)

근거 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_property_delivery.card.085.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.standard.own-property-not-object)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. (`assess_general_object_fraud_standard_own_property_not_object(case_id, unknown_assessment_085, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_085)`)

근거 NormCard: `general_object.fraud.standard.own-property-not-object`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_property_delivery.card.085.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.standard.own-property-not-object)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. (`assess_general_object_fraud_standard_own_property_not_object(case_id, positive_assessment_085, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_085)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. (`assess_general_object_fraud_standard_own_property_not_object(case_id, negative_assessment_085, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_085)`)

근거 NormCard: `general_object.fraud.standard.own-property-not-object`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.object_public_interest.card.086.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, general_object.fraud.standard.public-interest-only-no-fraud)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. (`assess_general_object_fraud_standard_public_interest_only_no_fraud(case_id, unknown_assessment_086, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_086)`)

근거 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.object_public_interest.card.086.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, general_object.fraud.standard.public-interest-only-no-fraud)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. (`assess_general_object_fraud_standard_public_interest_only_no_fraud(case_id, positive_assessment_086, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_086)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. (`assess_general_object_fraud_standard_public_interest_only_no_fraud(case_id, negative_assessment_086, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_086)`)

근거 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.structure_triangular.card.087.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. (`assess_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, unknown_assessment_087, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_087)`)

근거 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.structure_triangular.card.087.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. (`assess_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, positive_assessment_087, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_087)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 경우에도 인정될 수 있다. (`assess_mistake_disposition_fraud_variant_triangular_fraud_94do1575_factual_position_interpretation(case_id, negative_assessment_087, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_087)`)

근거 NormCard: `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_rights_exercise.card.088.undetermined`

결론: **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음** (`fraud_undetermined(case_id, defendant_id, special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. (`assess_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, unknown_assessment_088, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, unknown)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, unknown_assessment_088)`)

근거 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

해석 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `fraud.profile_rights_exercise.card.088.conflict`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. (`assess_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, positive_assessment_088, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, positive_assessment_088)`)
- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. (`assess_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, negative_assessment_088, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, negative_assessment_088)`)

근거 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

해석 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `fraud.profile_loan.bar.001`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.causal-link.loan-purpose-not-sole-trigger)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 차주가 밝힌 차용금 용도의 진실 여부가 대차 성립의 유일한 계기가 아닌 경우에는 기망행위와 재산적 처분행위 사이의 인과관계가 인정되지 않아 사기죄가 성립하지 않는다. (`satisfied_deception_fraud_causal_link_loan_purpose_not_sole_trigger(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.causal-link.loan-purpose-not-sole-trigger`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.002`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.causal-link.no-disposition-no-deception)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠지게 하였더라도 그 착오에 기하여 재산적 처분행위를 하게 한 행위가 아니면 사기죄의 실행행위로서 기망이 아니다. (`satisfied_deception_fraud_causal_link_no_disposition_no_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.causal-link.no-disposition-no-deception`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.003`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.definition.deception-target-human)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사실과 다른 관념을 형성하고 재산적 처분행위를 할 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 착오에 빠질 수 없어 기망행위의 대상이 될 수 없다. (`satisfied_deception_fraud_definition_deception_target_human(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.definition.deception-target-human`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.004`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.element.deception-must-create-false-belief)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단을 사용하였더라도 상대방에게 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 사기죄 실행행위로서의 기망이 아니다. (`satisfied_deception_fraud_element_deception_must_create_false_belief(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.element.deception-must-create-false-belief`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.005`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.element.transaction-purpose-no-impairment)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상대방을 착오에 빠뜨렸더라도 거래 목적 달성에 지장이 없으면 신의칙 위반의 기망행위가 있었다고 보기 어렵다. (`satisfied_deception_fraud_element_transaction_purpose_no_impairment(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.element.transaction-purpose-no-impairment`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_advertising.bar.006`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.standard.advertising-tolerable-exaggeration)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 상품 광고·선전에 수반된 과장이나 허위가 일반 상거래 관행과 신의칙상 시인될 수 있는 정도이면 기망행위를 인정하기 어려워 사기죄가 성립하지 않는다. (`satisfied_deception_fraud_standard_advertising_tolerable_exaggeration(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.advertising-tolerable-exaggeration`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.007`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.standard.easily-detectable-lie)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 구체적 사정에서 누구나 쉽게 허위를 간파할 수 있는 단순한 거짓말은 기망에 해당하지 않는다. (`satisfied_deception_fraud_standard_easily_detectable_lie(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.easily-detectable-lie`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_loan.bar.008`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.standard.loan-lender-anticipated-risk)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 대주가 인적·계속적 거래관계로 차주의 신용상태를 알고 변제지체·변제불능 위험을 예상했거나 충분히 예상할 수 있었고, 차주가 차용 당시 중요한 사항에 허위사실을 말한 등의 사정이 없다면 이후 미변제만으로 기망이나 편취 범의를 단정할 수 없다. (`satisfied_deception_fraud_standard_loan_lender_anticipated_risk(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.loan-lender-anticipated-risk`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_loan.bar.009`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.standard.loan-subsequent-default)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소비대차에서 차주가 차용 당시 변제 의사와 능력이 있었다면, 이후 변제하지 않더라도 민사상 채무불이행일 뿐 사기죄는 성립하지 않는다. (`satisfied_deception_fraud_standard_loan_subsequent_default(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.loan-subsequent-default`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.bar.010`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.standard.vague-opinion-not-deception)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 땅값이나 주가가 오를 것 같다는 식의 막연한 추측이나 의견 제시는 기망이 될 수 없다. (`satisfied_deception_fraud_standard_vague_opinion_not_deception(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.standard.vague-opinion-not-deception`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.011`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_general_object.causation_required)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 객관적 구성요건 요소 사이의 인과관계가 인정되지 않으면 사기죄는 기수로 성립하지 않는다. (`satisfied_fraud_general_object_causation_required(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_general_object.causation_required`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.012`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_general_object.deception_error_causation)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망수단으로 재물을 교부받았더라도 상대방이 그 기망으로 착오에 빠진 것이 아니라 다른 동기나 이유로 교부한 경우 사기미수죄만 성립한다. (`satisfied_fraud_general_object_deception_error_causation(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_general_object.deception_error_causation`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_intent.bar.013`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_intent.no_disposition_inducement_intent)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다. (`satisfied_fraud_intent_no_disposition_inducement_intent(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_intent.no_disposition_inducement_intent`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.014`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.no_capacity_theft)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 구체적으로 재산적 처분행위를 할 의사능력이 없는 사람이 기망적 수단에 반응하여 재물을 넘긴 경우에는 그 사람의 처분행위를 인정할 수 없어 사기죄가 아니라 절도죄가 문제된다. (`satisfied_fraud_mistake_no_capacity_theft(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.no_capacity_theft`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_mistake_disposition.bar.015`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.no_thought_no_error)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 어떠한 생각도 갖지 않는 경우에는 착오가 인정되지 않는다. (`satisfied_fraud_mistake_no_thought_no_error(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.no_thought_no_error`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_omission.bar.016`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.omission_not_all_nonclaims)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 채권자가 일시적으로 이행을 독촉하거나 청구하지 않았다는 사정만으로는 부족하고, 착오에 기한 의식적 불행사와 그로 인한 직접 재산상 이익 부여가 있어야 부작위 처분행위가 될 수 있다. (`satisfied_fraud_mistake_omission_not_all_nonclaims(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.omission_not_all_nonclaims`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_mistake_disposition.bar.017`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.property_limited_disposition)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 처분행위는 재산상 처분행위에 한정되므로, 재산상 처분행위가 아닌 행위는 사기죄의 처분행위로 인정되지 않는다. (`satisfied_fraud_mistake_property_limited_disposition(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.property_limited_disposition`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.018`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.trick_theft_directness)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망적 수단이 사용됐더라도 피해자의 행위가 재물 지배 이전을 직접 초래하지 않고 행위자가 탈취한 경우에는 처분행위의 직접성이 없어 사기죄가 아니라 절도죄가 문제된다. (`satisfied_fraud_mistake_trick_theft_directness(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.trick_theft_directness`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.stage_attempt_completion.bar.019`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_stages_participation.no_causation_attempt)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망·착오·재산적 처분행위 사이의 인과관계가 인정되지 않으면 사기죄는 미수이다. (`satisfied_fraud_stages_participation_no_causation_attempt(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_stages_participation.no_causation_attempt`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.boundary_other_offenses.bar.020`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, general_object.fraud.standard.own-possession-other-property-embezzlement)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 자기 점유의 타인 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다. (`satisfied_general_object_fraud_standard_own_possession_other_property_embezzlement(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.standard.own-possession-other-property-embezzlement`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.object_property_delivery.bar.021`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, general_object.fraud.standard.own-property-not-object)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인이 점유하는 자기소유 재물은 사기죄의 객체가 되지 않는다. (`satisfied_general_object_fraud_standard_own_property_not_object(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.standard.own-property-not-object`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.object_public_interest.bar.022`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, general_object.fraud.standard.public-interest-only-no-fraud)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망이 국가적·공공적 법익만 침해하고 그 침해를 재산권 침해와 동일하게 평가할 수 없는 경우에는 사기죄가 성립하지 않는다. (`satisfied_general_object_fraud_standard_public_interest_only_no_fraud(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `general_object.fraud.standard.public-interest-only-no-fraud`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.profile_rights_exercise.bar.023`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime)`)

필요조건:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기망수단을 사용한 권리행사라도 그 기망수단이 사회통념상 권리행사의 수단으로 용인될 수 있으면 권리행사 자체에 속하는 행위는 범죄를 구성하지 않는 정당행위가 된다. (`satisfied_special_forms_fraud_standard_right_exercise_socially_acceptable_no_crime(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

해석 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.

### `fraud.core_deception.mandatory_negative.001`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, deception.fraud.definition.deception-good-faith-mistake)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 기망은 거래관계에서 지켜야 할 신의칙에 반하여 사람으로 하여금 착오를 일으키게 하는 행위이다. (`assess_deception_fraud_definition_deception_good_faith_mistake(case_id, mandatory_negative_001, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_001)`)

근거 NormCard: `deception.fraud.definition.deception-good-faith-mistake`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_intent.mandatory_negative.002`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_intent.contract_breach_distinction)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 고의에 의한 기망은 단순채무불이행과 사기죄를 구별하는 표준이 된다. (`assess_fraud_intent_contract_breach_distinction(case_id, mandatory_negative_002, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_002)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.003`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.deceived_disposer_identity)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 피기망자와 처분행위자는 동일인이어야 한다. (`assess_fraud_mistake_deceived_disposer_identity(case_id, mandatory_negative_003, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_003)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.004`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.disposition_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 처분행위란 범인 등에게 재물을 교부하거나 재산상 이익을 부여하는 재산적 처분행위이며, 피기망자가 처분의사를 가지고 그 의사에 지배된 행위를 해야 한다. (`assess_fraud_mistake_disposition_definition(case_id, mandatory_negative_004, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_004)`)

근거 NormCard: `fraud_mistake.disposition_definition`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.005`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.error_definition)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 착오란 사실과 일치하지 않는 인식을 의미한다. (`assess_fraud_mistake_error_definition(case_id, mandatory_negative_005, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_005)`)

근거 NormCard: `fraud_mistake.error_definition`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_intent.mandatory_negative.006`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.gain_purpose)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄에는 범인이 타인을 기망하여 재산적 이득을 취한다는 목적의사가 있어야 한다. (`assess_fraud_mistake_gain_purpose(case_id, mandatory_negative_006, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_006)`)

근거 NormCard: `fraud_mistake.gain_purpose`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.007`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.property_disposition_element)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄는 피기망자의 착오에 기한 재산적 처분행위로 본인 또는 제3자가 재물을 교부받거나 재산상 이익을 취득함으로써 성립한다. (`assess_fraud_mistake_property_disposition_element(case_id, mandatory_negative_007, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_007)`)

근거 NormCard: `fraud_mistake.property_disposition_element`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.core_mistake_disposition.mandatory_negative.008`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_mistake.sequential_causation)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 사기죄 성립에는 기망행위, 상대방의 착오 및 재물 교부 또는 재산상 이익 공여 사이의 순차적 인과관계가 필요하며, 재산적 처분행위는 착오에 의한 것이어야 한다. (`assess_fraud_mistake_sequential_causation(case_id, mandatory_negative_008, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_008)`)

근거 NormCard: `fraud_mistake.sequential_causation`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.stage_attempt_completion.mandatory_negative.009`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, fraud_stages_participation.completion_deception_disposition_transfer)`)

필요조건:

- 다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 충족되는지에 대한 명시적 3상태 rule fact: 행위자의 기망으로 상대방이 착오에 빠지고, 그 착오에 기초한 재산적 처분행위로 재물 또는 재산상 이익이 이전되면 사기죄는 기수에 이른다. (`assess_fraud_stages_participation_completion_deception_disposition_transfer(case_id, mandatory_negative_009, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_009)`)

근거 NormCard: `fraud_stages_participation.completion_deception_disposition_transfer`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.object_property_delivery.mandatory_negative.010`

결론: **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함** (`fraud_not_established(case_id, defendant_id, general_object.fraud.element.object-other-possessed-other-property)`)

필요조건:

- 현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: 사기죄의 객체는 타인이 점유하는 타인의 재물 또는 재산상 이익이다. (`assess_general_object_fraud_element_object_other_possessed_other_property(case_id, mandatory_negative_010, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, not_satisfied)`)
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음 (`provable(case_id, mandatory_negative_010)`)

근거 NormCard: `general_object.fraud.element.object-other-possessed-other-property`

해석 메모: 필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.

### `fraud.structure_ordinary.role_structure`

결론: **일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨** (`fraud_role_structure_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, deceived_person_id, subject_id, beneficiary_id)`)

필요조건:

- 피기망자와 처분행위자가 동일한 행위주체임 (`fraud_deceived_disposer_identity_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, deceived_person_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`

해석 메모: 일반형은 피기망자·처분자·재산소유자에 같은 entity ID를 사용한다.

### `fraud.structure_triangular.role_structure`

결론: **일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨** (`fraud_role_structure_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 피기망자와 처분행위자가 동일한 행위주체임 (`fraud_deceived_disposer_identity_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 증명 가능한 평가에서 다음 조건이 충족됨: 피기망자와 재산상 피해자는 동일인일 필요가 없고, 피해자와 처분행위자가 다른 경우를 삼각사기라고 한다. (`satisfied_fraud_mistake_triangular_fraud_definition(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨 (`fraud_triangular_authority_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.triangular_fraud_definition`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 삼각사기는 피기망자=처분자를 유지하면서 별도 재산소유자와 그 재산을 처분할 권능 또는 지위를 요구한다.

### `fraud.structure_self_acquisition.beneficiary_attribution`

결론: **본인 또는 제3자에게 귀속되는 취득 구조가 충족됨** (`fraud_beneficiary_attribution_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, defendant_id)`)

필요조건:

- 고의의 기망과 재산적 이득 목적이 함께 인정됨 (`fraud_intent_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, defendant_id)`)

근거 NormCard: `fraud_intent.contract_breach_distinction`, `fraud_mistake.gain_purpose`

해석 메모: 피고인과 수익자에 같은 entity ID를 쓰는 본인취득 경로다.

### `fraud.structure_third_party_acquisition.beneficiary_attribution`

결론: **본인 또는 제3자에게 귀속되는 취득 구조가 충족됨** (`fraud_beneficiary_attribution_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨 (`fraud_third_party_acquisition_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `fraud_intent.third_party_acquisition`

해석 메모: 제3자취득은 도구·대리 관계 또는 제3자 취득 의사를 별도 귀속 gate로 요구한다.

### `fraud.core.outcome.established`

결론: **승인된 사기죄 core 구성요건과 역할·인과·기수 조건이 모두 충족됨** (`fraud_established(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

필요조건:

- 사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨 (`fraud_object_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 사건에 적용되는 기망 기준이 충족됨 (`fraud_deception_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 피기망자에게 법적 의미의 착오가 인정됨 (`fraud_mistake_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 착오에 기한 재산적 처분행위가 인정됨 (`fraud_disposition_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 재물 교부 또는 재산상 이익의 취득이 인정됨 (`fraud_acquisition_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨 (`fraud_causal_chain_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨 (`fraud_completion_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 고의의 기망과 재산적 이득 목적이 함께 인정됨 (`fraud_intent_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 재물 교부 또는 이익 취득 외에 현실적 재산상 손해를 별도 요건으로 요구하지 않음 (`fraud_no_separate_loss_gate(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨 (`fraud_role_structure_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)
- 본인 또는 제3자에게 귀속되는 취득 구조가 충족됨 (`fraud_beneficiary_attribution_satisfied(case_id, defendant_id, deceived_person_id, deceived_person_id, property_owner_id, subject_id, beneficiary_id)`)

근거 NormCard: `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.loan-purpose-materiality`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_intent.contract_breach_distinction`, `fraud_intent.third_party_acquisition`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.property_disposition_element`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.unaware_error`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.exception.public-interest-property-equivalence`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`

해석 메모: 공통 core는 세부 사기유형을 직접 분기하지 않는다. profile과 adapter가 채운 canonical component, 역할 구조 및 수익 귀속 interface만 AND 결합한다.

### `fraud.core.outcome.conflict.established_and_not_established`

결론: **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨** (`fraud_conflict(case_id, defendant_id, established_and_not_established)`)

필요조건:

- 승인된 사기죄 core 구성요건과 역할·인과·기수 조건이 모두 충족됨 (`fraud_established(case_id, defendant_id, deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id)`)
- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함 (`fraud_not_established(case_id, defendant_id, negative_issue_id)`)

근거 NormCard: `deception.fraud.causal-link.deception-property-disposition`, `deception.fraud.causal-link.loan-purpose-not-sole-trigger`, `deception.fraud.causal-link.no-disposition-no-deception`, `deception.fraud.definition.deceived-person-unspecified`, `deception.fraud.definition.deceived-person-victim-distinct`, `deception.fraud.definition.deception-content-basis-fact`, `deception.fraud.definition.deception-counterparty-is-other`, `deception.fraud.definition.deception-good-faith-mistake`, `deception.fraud.definition.deception-means-unrestricted`, `deception.fraud.definition.deception-object-facts`, `deception.fraud.definition.deception-target-human`, `deception.fraud.definition.exploitation-existing-mistake`, `deception.fraud.definition.implicit-deception`, `deception.fraud.definition.notice-duty-violation-omission`, `deception.fraud.definition.other-includes-corporation`, `deception.fraud.element.deception-must-create-false-belief`, `deception.fraud.element.deception-not-legal-act-important-part`, `deception.fraud.element.loan-no-repayment-intent-or-ability`, `deception.fraud.element.omission-deception-guarantor-equivalence`, `deception.fraud.element.omission-deception-independent-error`, `deception.fraud.element.omission-deception-legal-notice-duty`, `deception.fraud.element.transaction-purpose-no-impairment`, `deception.fraud.element.victim-negligence-no-bar`, `deception.fraud.standard.advertising-important-concrete-falsehood`, `deception.fraud.standard.advertising-tolerable-exaggeration`, `deception.fraud.standard.deception-concrete-circumstances`, `deception.fraud.standard.easily-detectable-lie`, `deception.fraud.standard.implicit-deception-explanatory-value`, `deception.fraud.standard.implicit-omission-deception-distinction`, `deception.fraud.standard.intent-to-defraud-loan-inference`, `deception.fraud.standard.loan-lender-anticipated-risk`, `deception.fraud.standard.loan-purpose-materiality`, `deception.fraud.standard.loan-subsequent-default`, `deception.fraud.standard.precedent-notice-duty-materiality`, `deception.fraud.standard.vague-opinion-not-deception`, `fraud_damage_acquisition.delivery_factual_control`, `fraud_damage_acquisition.delivery_of_property`, `fraud_damage_acquisition.money_delivery_full_amount`, `fraud_damage_acquisition.property_concept_reported_precedent`, `fraud_damage_acquisition.property_disposition_types`, `fraud_damage_acquisition.property_loss_negative_view`, `fraud_damage_acquisition.protected_economic_interest`, `fraud_damage_acquisition.right_exercise_unacceptable_deception`, `fraud_damage_acquisition.subsequent_return_irrelevant`, `fraud_general_object.causation_required`, `fraud_general_object.deception_error_causation`, `fraud_intent.contract_breach_distinction`, `fraud_intent.illegal_appropriation_definition`, `fraud_intent.no_disposition_inducement_intent`, `fraud_intent.precedent_illegal_appropriation_intent`, `fraud_intent.third_party_acquisition`, `fraud_intent.time_of_conduct`, `fraud_mistake.conscious_nonexercise`, `fraud_mistake.deceived_disposer_identity`, `fraud_mistake.disposition_definition`, `fraud_mistake.disposition_directness`, `fraud_mistake.disposition_intent_act_awareness`, `fraud_mistake.disposition_omission`, `fraud_mistake.error_definition`, `fraud_mistake.error_disposition_motivation`, `fraud_mistake.error_doubt_ignorance`, `fraud_mistake.factual_act_disposition`, `fraud_mistake.gain_purpose`, `fraud_mistake.invalid_act_disposition`, `fraud_mistake.no_capacity_theft`, `fraud_mistake.no_thought_no_error`, `fraud_mistake.omission_not_all_nonclaims`, `fraud_mistake.property_disposition_element`, `fraud_mistake.property_limited_disposition`, `fraud_mistake.sequential_causation`, `fraud_mistake.triangular_fraud_definition`, `fraud_mistake.trick_theft_directness`, `fraud_mistake.unaware_error`, `fraud_stages_participation.attempt_deceptive_act`, `fraud_stages_participation.completion_deception_disposition_transfer`, `fraud_stages_participation.no_causation_attempt`, `fraud_stages_participation.property_fraud_completion_control`, `general_object.fraud.definition.property-benefit`, `general_object.fraud.definition.property-benefit-not-numerically-limited`, `general_object.fraud.element.object-other-possessed-other-property`, `general_object.fraud.element.property-benefit-concrete`, `general_object.fraud.exception.public-interest-property-equivalence`, `general_object.fraud.standard.later-cancellation-no-effect`, `general_object.fraud.standard.own-possession-other-property-embezzlement`, `general_object.fraud.standard.own-property-not-object`, `general_object.fraud.standard.public-interest-only-no-fraud`, `mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation`, `special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime`

해석 메모: 최종 성립과 명시적 불성립 사유가 함께 도출되면 상위 conflict를 노출한다.

## RAG와의 경계

이 RuleIR은 558개 구체 판례·희귀 유형을 실행 rule로 복제하지 않는다. 사건이 소송사기, 보험사기, 특정 거래관행처럼 세부 적용례를 요구하면 RAG가 관련 판례를 검색하고, 그 판례를 근거로 현재 사건의 `assess_*` 값을 만든다. 검색된 판례의 결론 자체를 Scallop fact로 넣어서는 안 된다.

## 사람이 중점적으로 볼 세 항목

1. 불법영득의사를 특정 재물 편취 branch에만 추가할 범위
2. 불성립 결과를 사기미수·절도·횡령·정당행위로 별도 분기할지
3. 공통 actor tuple을 predicate별 최소 인자로 축소할지
