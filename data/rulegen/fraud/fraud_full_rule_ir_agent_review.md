# 사기죄 full RuleIR 에이전트 검토

## 판정

**Sol 지적 수동 정정 및 에이전트 재검토 완료, 사용자 재검수 대기.** Terra의 원본 부분 출력은 candidate로 사용하지 않았고, 승인된 88장만으로 수동·결정적으로 재구성했다.

## 자동 검증

- NormCard scope: 88/88
- commentary input: 88개
- predicate: 201개
- rule: 342개
- 모든 input의 provable pairing: 통과
- case variable isolation: 통과
- negation: 완결 게이트 뒤 최종 outcome stratum의 2개 검사로 제한
- active_policy 부재: 통과
- 피기망자=처분자 성립 head: 통과
- module ownership: 15개 모듈, 88/88, 중복 0
- profile activation: 기본 OFF, 사건별 0개 이상 선택, 비망라적 registry
- 최종 fraud_established rule: 1개
- established/not_established/undetermined/conflict 구현: 통과

## 법리 검토

1. 피기망자와 처분행위자는 최종 성립 rule에서 같은 변수다. 역할 슬롯을 분리했지만 별개의 사람으로 강제하지 않았다.
2. 일반형과 삼각사기는 역할 adapter가 분리한다. 삼각사기는 별도 재산소유자, 삼각사기 관련성 및 94도1575 계열의 처분 권능·지위를 요구한다.
3. 본인취득과 제3자취득은 수익 귀속 adapter가 분리한다. 제3자취득은 의사·도구·대리 관계를 추가 gate로 요구한다.
4. 현실적 재산상 손해는 재물 교부 또는 이익 취득과 별개의 공통 gate로 두지 않았다.
5. 불법영득의사 카드는 보존·소비하지만 모든 사기 유형의 최종 공통 gate로 강제하지 않았다.
6. 사기미수·절도·횡령·정당행위가 문제되는 bar는 현재 fraud_not_established의 issue_id로 노출한다. 후속 죄명 결론은 아직 만들지 않았다.
7. 차용금·광고·부작위·묵시적 기망·권리행사 기준은 각각 profile 소유다. 공통 core는 이들의 세부 카드 대신 canonical component만 소비한다.
8. 재물과 재산상 이익 모듈은 실행상 분리되어 있지만 법학적 상위 분류에서는 모두 공통 객관적 구성요건 코어에 속한다. 변제 의사·능력은 차용금 profile이 기망·고의 component로 변환한다.
9. 사실유형 profile은 항상 켜지지 않는다. 관련 profile의 assess relation과 provable이 함께 있을 때만 작동하며, 목록은 비망라적이다.

## 남은 위험

- 88개 assessment는 한 사건에서 전부 호출한다는 뜻이 아니다. 사건 관련성 routing 후 필요한 항목만 평가해야 한다.
- deterministic 28개 입력은 법적 standard 판단이 아니라 규칙 antecedent의 구조화된 rule fact로 추출해야 한다.
- profile router가 관련 모듈을 먼저 골라야 한다. 단순한 정의 카드와 실제 적용 충족을 혼동하지 않도록 feature schema와 RAG 근거가 필요하다.
- `case_assessment_complete`는 router가 관련 profile을 확정하고 모든 선택 쟁점의 평가를 수집한 뒤에만 공급해야 한다.
