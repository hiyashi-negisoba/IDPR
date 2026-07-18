# 사기죄 full RuleIR 사용자 검수 가이드

이번에는 88개 카드와 15개 모듈을 처음부터 다시 읽을 필요가 없다. 먼저 `fraud_full_rule_ir_sol_adjudication.md`의 항목별 판정표와 마지막 사용자 재검수 포인트 3개를 읽는다.

1. Sol 지적 13개 중 11개 수용·수정수용, 2개 불수용 판단을 확인한다.
2. 일반형/삼각사기 역할 정책, 주관적 요건 묶음, 완결 게이트에 동의하는지 본다.
3. 더 자세한 논리가 필요할 때만 `fraud_full_rule_ir_natural_language_explanation.md`의 최종 AND gate와 역할·취득 adapter 부분을 확인한다.
4. JSON과 342개 rule별 해설은 특정 구현을 추적할 때만 보면 된다.

최종 승인본은 predicate 201개, rule 342개다. Sol 검토, 에이전트 수동 정정, 사용자 재검수가 모두 끝났으며 별도 승인 기록 뒤 deterministic compile과 공식 scli golden test를 실행했다.

Scallop 실행 결과를 검토할 때는 JSON이 아니라 `fraud_scallop_runtime_human_report.md`를 읽는다. 이 문서에는 실제로 수동 입력한 14개 판단값, 역할 구조, 9개 사례별 변경점과 출력 결과, 아직 검증하지 않은 LLM/RAG 단계를 한국어로 설명했다.
