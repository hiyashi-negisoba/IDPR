# Phase 3 완료선과 남은 작업

## `4cca547`에서 완료된 것

- Call 1 FactGraph 추출과 host admission
- Call 1.5 전체 법조문 catalog 선택
- 현행 L0 검색과 선택 결과의 union, issue-first 후보 생성
- Call 2의 쟁점별 `satisfied/not_satisfied/unknown` 판단 및 증거 결합 계약
- Scallop rulebase 실행과 후속 쟁점 배선
- Call 3의 구조화 IRAC 생성, host provenance·결론 결박·내부 ID 비노출 검증
- 문항 scope 보존, 스모크/런타임 하드코딩 제거, 유효 FactGraph 재사용 경로

## Phase 3 종료 시점에 실제로 남은 작업

1. 허용된 두 스모크로 전 경로를 새로 실행하여 단계별 JSON 계약과 case ID 연속성을
   검증한다. 이전 산출물 fallback으로 실패를 숨기지 않는다.
2. 전체 회귀 테스트와 Scallop 골든 테스트가 통과한 동일 코드로 E2E를 실행한다.
3. 모델·프롬프트·파라미터·Scallop·Slurm job·토큰·시간·산출물 hash를 manifest에
   고정하고, 통과 상태를 커밋과 annotated tag로 동결한다.
4. 동결 이후에만 두 답안과 두 루브릭을 직접 대조하여 오류가 발생한 단계를 분류한다.
5. 그중 검색 미회수가 실제 원인인 항목만 변경 후보로 보고하고 사용자 승인을 기다린다.
6. 승인 시 목표 성능, 후보 수, 시간·토큰 예산, 반복 상한과 중단 조건 안에서 별도
   실험 브랜치로 최적화한다.
7. 최종 동결 파이프라인 평가 때까지 나머지 59문항을 열지 않는다.

따라서 무기한 검색 후보 축소·프롬프트 튜닝은 Phase 3 종료 시점의 남은 작업이 아니었다.
검색 변경 여부 자체가 동결 출력의 원인 분석과 사용자 승인을 거쳐 결정될 후속 단계다.
