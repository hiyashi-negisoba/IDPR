# 사기죄 full RuleIR 에이전트 검토

## 판정

**구조 검증 통과, 사용자 법률 검수 필요.** Terra의 원본 부분 출력은 candidate로 사용하지 않았고, 승인된 88장만으로 수동·결정적으로 재구성했다.

## 자동 검증

- NormCard scope: 88/88
- commentary input: 88개
- predicate: 194개
- rule: 337개
- 모든 input의 provable pairing: 통과
- case variable isolation: 통과
- negation 및 active_policy 부재: 통과
- 피기망자=처분자 성립 head: 통과
- established/not_established/undetermined/conflict 구현: 통과

## 법리 검토

1. 피기망자와 처분행위자는 모든 성립 branch에서 같은 변수다. 역할 슬롯을 분리했지만 별개의 사람으로 강제하지 않았다.
2. 삼각사기는 재산소유자를 별도 변수로 두고 94도1575 계열의 처분 권능 또는 지위 assessment를 추가했다.
3. 제3자 취득은 수익자를 별도 변수로 두고 제3자 취득 의사·도구·대리 관계를 추가 gate로 요구했다.
4. 현실적 재산상 손해는 재물 교부 또는 이익 취득과 별개의 공통 gate로 두지 않았다.
5. 불법영득의사 카드는 보존·소비하지만 모든 사기 유형의 최종 공통 gate로 강제하지 않았다.
6. 사기미수·절도·횡령·정당행위가 문제되는 bar는 현재 fraud_not_established의 issue_id로 노출한다. 후속 죄명 결론은 아직 만들지 않았다.

## 남은 위험

- 88개 assessment는 한 사건에서 전부 호출한다는 뜻이 아니다. 사건 관련성 routing 후 필요한 항목만 평가해야 한다.
- deterministic 28개 입력은 법적 standard 판단이 아니라 규칙 antecedent의 구조화된 rule fact로 추출해야 한다.
- 여러 구체 기망 branch를 OR로 연결했으므로 grounding 모델이 단순한 정의 카드와 실제 적용 충족을 혼동하지 않도록 feature schema와 RAG 근거가 필요하다.
- established와 not_established가 동시에 나올 수 있다. long-form 생성 전 conflict resolution 정책을 반드시 적용해야 한다.
