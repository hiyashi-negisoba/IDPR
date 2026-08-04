# RuleIR-native 비재산죄 확장 경계

## 현재 결론

재산죄 RuleIR의 실행 계약은 비재산죄에도 재사용할 수 있다. 그러나 현재 P2, 형법총칙,
절차법은 같은 단위의 candidate RuleIR과 compiled SCL이 연결돼 있지 않다. 따라서 레지스트리는
이 영역을 지원 단위로 올리지 않고 `predicate_ir_missing`으로 반환한다.

## 재사용 가능한 계약

- unit별 role predicate와 argument schema
- commentary-origin input predicate 전량과 `norm_card_id` 연결
- `provable`, `case_assessment_complete`, entity distinctness 같은 system input
- `*_elements_satisfied`, `*_established`, `*_not_established`, `*_undetermined`,
  `*_conflict` 결과 relation
- candidate JSON → compiled SCL의 1:1 asset audit

이는 범죄 구성요건에 국한되지 않는다. 비재산죄도 **unit별 고유 역할 계약**을 작성할 수 있다면
동일한 assessment/runtime 경계를 쓸 수 있다.

## 비재산죄별 선행 조건

| 영역 | 재사용 | 새로 확보해야 할 것 | 현재 처리 |
|---|---|---|---|
| P2 생명·신체 | assessment 상태, runtime closure | 죄명별 candidate RuleIR, 역할 tuple, compiled SCL, 결론 relation | `predicate_ir_missing` |
| 형법총칙 | system input, conflict/unknown 출력 | 각칙 unit과의 조합 규칙 및 독립 query 계약 | `predicate_ir_missing` |
| 절차법 | source-grounded assessment | 절차 단계·증거 객체 역할, 절차별 compiled SCL | `predicate_ir_missing` |

`p2_full.scl`의 일반 predicate 여섯 개는 죄명별 RuleIR 자산이 아니므로 이 레지스트리의
fallback으로 사용하지 않는다. 다음 확장은 한 영역 전체를 먼저 켜는 방식이 아니라, 하나의
closed unit에 대해 candidate JSON·SCL·golden scenario·이 감사 통과를 함께 추가하는 방식으로 한다.
