# Phase 3 E2E 동결 기록

## 검증 결과

- 최종 코드 전체 회귀: `511 passed in 187.26s`
- pinned Scallop 골든: `51 passed in 29.14s`
- E2E 대상: 전용 inventory의 두 문항만 사용
- 실제 경로: Call 1 → Call 1.5 → 현행 L0 → Call 2 → Scallop → Call 3
- fallback: 0건
- 결정론적 E2E 계약 검증: `passed`

## 실행 이력

- job `218221`: 사용자 문항 Call 2가 `satisfied`와 빈 `basis_fact_ids`를 결합하여
  host 계약 검사에서 실패했다. 실패 산출물은 별도 디렉터리에 보존했고 재사용하지 않았다.
- 상태별 증거 결합을 guided JSON schema에서 직접 강제한 뒤 전체 회귀를 재검증했다.
- job `218223`: 두 문항의 Call 1부터 Call 3까지 새로 생성하고 각 host 검증을 통과했다.
  마지막 manifest 작성에서 workspace 별칭(`/home` 대 `/data5`) 처리 오류가 발생했다.
- 경로를 물리 경로로 정규화하도록 검증기를 수정하고, job `218223`의 완성된 산출물에
  결정론적 검증을 다시 적용하여 `freeze_manifest.json`을 생성했다.

Manifest는 실제 모델 산출물 생성 커밋 `62171e9`, 경로 수정 후 검증기 커밋 `0e7c9bc`,
Slurm job ID와 scheduler 종료 상태를 분리해 기록한다. 따라서 scheduler의 최종 `FAILED`를
E2E 생성 실패로 오인하거나, 반대로 manifest 후처리 실패를 숨기지 않는다.

루브릭 점수와 검색 품질은 이 동결의 통과 조건이 아니다. 최종 답안과 루브릭의 내용 대조는
tag 생성 이후 별도 분석 브랜치에서 수행한다.
