# 사기죄 full RuleIR 사용자 검수 가이드

검수 순서는 자연어 설명을 먼저 읽고, 필요한 경우 원본 JSON의 rule ID를 대조하는 방식이 가장 효율적이다.

1. 최종 9개 사실·법적 AND gate와 자동 손해불요 규칙이 적절한지
2. 네 성립 branch의 인물 동일성·상이성 처리가 맞는지
3. BAR_CARD_IDS의 각 항목이 일반 불성립인지 특정 경로 불성립인지
4. mandatory positive 10개가 명시적 부정 시 불성립으로 가도 되는지
5. 불법영득의사를 공통 gate에서 제외한 현재 정책이 맞는지
6. 사기미수·절도·횡령·정당행위 output을 지금 분리할지
7. standard assessment의 공통 actor tuple이 실제 feature extraction에 적합한지

현재 predicate 194개, rule 337개다. 사용자 승인 전 Sol과 Scallop compile/runtime은 차단한다.
