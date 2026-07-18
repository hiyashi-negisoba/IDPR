# 사기죄 full RuleIR 사용자 검수 가이드

JSON 소유권표는 기계 검증용이므로 읽을 필요가 없다. 먼저 `fraud_rule_ir_module_human_review.md`를 읽는다. 이 문서에는 15개 모듈의 한국어 이름·기능·경계와 포함 카드 88장의 원문이 모듈별로 붙어 있다.

1. 인간 검수본의 15개 모듈과 각 모듈의 굵은 글씨 검수 질문을 확인한다.
2. 이동·분리·RAG·삭제가 필요한 카드는 인간 검수본의 `원본 N번`으로 지적한다.
3. 그 다음 `fraud_full_rule_ir_natural_language_explanation.md`의 최종 AND gate와 역할·취득 adapter 부분만 확인한다.
4. 개별 rule까지 확인할 필요가 있을 때만 자연어 설명의 Rule별 해설이나 JSON을 본다.

현재 predicate 196개, rule 338개다. 사용자 검수는 승인됐고 다음 gate는 Sol이다. Sol API 실행은 별도 사용자 승인이 필요하며 Scallop compile/runtime은 Sol과 후속 사용자 검수 전까지 차단한다.
