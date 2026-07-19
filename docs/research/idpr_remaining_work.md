# IDPR 잔여 작업 목록

작성일: 2026-07-19 (프롬프트-계약 정합 세션 종료 시점 기준)

우선순위 순. 각 항목에 결정 주체를 표시한다.

## 1. 5건 paraphrase 2강 비교 후속 (에이전트 + 사용자)

- job `210499`(thinking off + greedy), `210500`(thinking off + 권장샘플링 1.0/0.95/64)의
  결과 분석은 완료 보고를 참조 (`WORK_REPORT.md` 말미).
- 다음 단계: 사용자가 5건의 카드별 gold 판정과 허용 결론을 확정해야 neural 정확도를
  채점할 수 있다 (`fraud_manual_card_review.md`가 검수 시작점).
- confidence 분산이 여전히 1.0 편중이면 프롬프트 보정 또는 후처리 재검토.

## 2. materiality 경계의 법률 검수 (사용자)

- `deception.fraud.standard.loan-purpose-materiality`가 사건에 따라 satisfied/unknown을
  오간다. 판례상 용도 기망의 중요성 추정 법리를 core 카드로 보강할지 결정 필요.
  보강하면 KCL형 차용 사건의 undetermined 위험이 줄어든다.

## 3. thinking 재도전 조건 (사용자 결정)

- 현재 thinking off가 기본 (greedy+thinking은 비종결 루프, 샘플링+thinking은 인용 전사
  오탈자 1자로 차단된 이력).
- 재도전하려면 인용 전사 오류의 재시도 정책이 필요한데, 이는 "host가 모델 출력을
  보정하지 않는다" 원칙과 상충하므로 사용자 결정 사항.

## 4. 전역 RuleIR 호환 코드 정리 (에이전트)

- 88-card RuleIR에 남은 구 `assess_*` 입력 관계는 활성 경로에서 미사용. 기존 실험
  artifact·테스트와 함께 이관하는 별도 정리 작업
  (`fraud_reasoning_plan_prompt_reset_v2_review.md` §9).

## 5. RAG 확장 설계 (에이전트 + 사용자)

- RAG/future-work 카드 558장을 장문 생성에 활용하는 설계 미착수.
- Gemma 4 26B A4B의 장문맥 회상 한계(MRCR 44.1%)와 vLLM `--max-model-len 32768`을
  함께 고려해 소수 정선 주입을 유지할 것.

## 6. 논문 갱신 (에이전트 + 사용자)

- `idpr_research_draft.md`에 core+profile 구조, thinking off 결정, 샘플링 ablation 반영.
- KCL 기출은 모델 학습 컷오프(2025-01)와 겹칠 수 있으므로 수동 paraphrase 5건을
  주 평가축으로 서술 (오염 통제).

## 7. M6 evaluator/fallback 경로 이관 (에이전트)

- M6을 whole-IRAC 4구획 계약으로 다시 쓰려면 ClaimGraph·section repair 계약 이관 필요
  (고정 5단락/15 claim 가정 제거, `idpr_prompt_reset_v2_review.md` §17-5).

## 8. 사기 외 죄명 확장 (사용자 승인 후)

- inventory 61건 중 사기 외 영역은 rulegen 미착수. 착수 시 형법총칙·특별법 commentary
  corpus 부재 항목은 unavailable로 유지하는 기존 원칙 준수.
