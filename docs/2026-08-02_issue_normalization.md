# 2026-08-02 카드 적재 정상화·Phase 3·총배선 기록

## 결론

일반법리 카드가 없었던 것이 아니다. slot 단위 역할 상속 때문에 일반법리, 세부 판단기준,
판례 사안이 모두 독립 core 질문으로 적재된 것이 문제였다. 전체 1,848장을 다시 쓰지 않고
383개 법적 issue로 무손실 재배치했다. 운영 파이프라인의 단위는 이제 다음과 같다.

    검색 신호 카드
      → 부모 issue
      → 후보 조문
      → initial issue + anchor 일반법리
      → unknown일 때 같은 issue의 detail 최대 2장 검색·재판정
      → 첫 Scallop으로 live 조문 선별
      → stage·participation·concurrence·guard 후속 판정
      → 최종 Scallop → issue reasoning packet → IRAC Call 3

Phase 3 결과는 커밋 444aec5에 먼저 고정했다. 이후 이 문서가 설명하는 총배선과 검색
재평가를 별도 작업으로 진행했다.

## 전수 재분류

- 원본 카드 1,848장, 조문 51개, issue 383개
- 첫 평가 대상 element issue 169개
- 기존 카드 anchor 364장 + 별도 provenance를 갖는 검수 Rule 3개
- 조건부 retrieval 후보 1,223장
- symbolic-only 207장, support-only 54장
- 판례 사안형 605장은 anchor가 될 수 없음
- 승인된 deferred 법률 검수를 반영해 review flag 0개
- 모든 원본 카드는 정확히 한 issue에 배치됨

절도죄와 같은 조문은 더 이상 소유·점유 판례 수십 장을 각각 질문하지 않는다. 타인의
재물성, 취거, 고의, 불법영득의사 같은 구성요건 issue를 먼저 판단하고, 구체 사실 때문에
판단이 안 되는 issue에서만 그 하위 기준을 검색한다.

## Phase 3 스모크

모델은 google/gemma-4-26B-A4B-it이며 PRO6000 1장, CPU 2개, RAM 32GB, 제한 48시간으로
실행했다.

| 항목 | flat-card | issue-first |
|---|---:|---:|
| 독립 판정 단위 | 193 cards | 14 issues |
| 최초 적재 규칙 | 다수의 case card 포함 | 24 anchors |
| 최초 제외 detail | 없음 | 84 cards |
| 최종 판정 | 거의 전부 unknown | 10 satisfied / 1 not_satisfied / 3 unknown |

Slurm 217909는 강제 문구 재시도 없이 한 번에 통과했다. 남은 unknown 3개는 제319조
공동현관의 관리·출입통제·반대의사 인식이 사실관계에 없기 때문이다. 세부 판례를 추가해도
사실 자체가 생기지 않으므로 unknown 유지가 타당하다.

Slurm 217929에서 같은 issue_status를 Scallop에 재생했다.

- 제298조·제301조: offense_established
- 제297조: 기수 요건 반증, offense_undetermined, attempt_to_consider
- 제319조: element_unaddressed 3개

초기 bridge가 legacy 전체 슬롯까지 깨워 element_unaddressed 218개를 만들던 누수는
card_assessed_case로 격리했다. 수정 후 실제 unknown 3개만 남았다.

## 전체 파이프라인 총배선

- L0 산출기는 candidate_issues를 사용하고 card_ids를 쓰지 않는다.
- data/eval/l0_candidates.jsonl 61행은 기존 조문 배열을 그대로 보존한 채 issue_ids,
  initial_issue_ids, deferred_issue_ids 구조로 마이그레이션했다.
- 운영 검색은 카드 문장을 검색 신호로 쓸 수 있지만, hit를 부모 issue로 투영한 뒤 조문
  점수로 접는다. 검색된 판례 카드는 최초 모델 입력이 아니다.
- Call 2는 issue_assessment 스키마와 issue_status만 사용한다.
- Scallop은 issue_offense와 issue_function으로 요소 지지·반증·조각을 계산한다.
- issue_pipeline 모듈이 L0 재수화, 모델 payload, Scallop 실행, 후속 generation용
  issue reasoning packet을 하나의 계약으로 묶는다.
- flat candidate_articles, card_assessment, render_card_statuses는 Phase 1/2 골든 및
  비교 실험 재현용으로만 남겼다. 일반 실행 스크립트의 재수입은 테스트가 막는다.

## 공개 실행경로 정상화

최종 실험 전에 고정 사례 스모크가 운영 코드처럼 남아 있던 구조를 제거했다. 단일 사례
실행기는 이제 `run_issue_assessment.py`와 `run_issue_answer.py`이며, case ID와 출력 경로를
명시적으로 받는다. 조문 목록을 생략하면 해당 사례의 L0 산출물 전체를 읽고, `--articles`는
운영 기본값이 아니라 진단용 범위 축소로만 제공한다. 61문항 실행은
`run_issue_pipeline_batch.py`가 사례별 원자적 산출물과 재시작 상태를 관리하고, 최종적으로
baseline과 같은 JSONL 계약을 만든다.

- 고정 사례·고정 조문 비교기는 `scripts/diagnostics/`와
  `scripts/slurm/diagnostics/`로 격리했다.
- 과거 사기 파일럿 API는 `src/idpr/legacy/`로 옮겼고, 현행 neural·generation import가
  legacy 구현을 자동 로드하지 않도록 했다.
- 카드 원천은 `data/rulebase/card_sources.json` manifest가 결정한다. 새 검수 카드 묶음을
  추가할 때 Python의 디렉터리·조문 상수를 수정할 필요가 없다.
- Slurm과 외부 데이터 경로는 저장소 상대경로 또는 `IDPR_*` 환경변수만 사용한다. 개인
  사용자명, 모델 snapshot hash, 서버 경로는 실행 스크립트에 들어가지 않는다.
- 고정 회귀 체크리스트는 `data/eval/diagnostic_checks.json`으로 이름을 바꾸고 L0 실행기의
  선택적 `--checks` 입력으로 분리했다.
- Rule 역할별 문서 예시는 특정 조문 preference table 대신, 검토가 끝난 가장 작은 slot을
  자료에서 결정론적으로 선택한다.

카탈로그를 다시 적재한 61문항 plan-only 검증 결과는 조문 중위 21개(최대 26), initial issue
중위 76개(최대 104), anchor 중위 93개(최대 128)다. 구조적으로는 전 사례가 실행 가능하지만,
Phase 3 고정 사례의 14개 initial issue보다 현저히 넓다. 따라서 이 상태로 전체 GPU 잡을 바로
제출하지 않고 issue 검색 평가와 입력 예산 결정을 먼저 한다.

## 법률 검수와 심볼릭 조건 정상화

사용자가 승인한 deferred review A–F를 두 개의 별도 자산으로 기록했다.

- 기존 일반법리 카드의 anchor 승격
- 위계공무집행방해의 고의, 범인도피지원의 사회상규, 상해치사의 예견가능성에
  대한 reviewed Rule 3개
- 심신미약을 범죄 조각 guard가 아닌 support로 교정
- 횟령과 배임의 주관적 요건 부정 카드 분리

실제 doctrine table에서 쓰는 흡수·상상적 경합 조건 12개를 전수 감사했다.
기존에는 9개가 자신보다 넓은 상위 issue의 판정을 공유했다. 이를 조건별 독립
issue로 분리했고, 조건 카드가 정확히 그 issue의 단일 anchor가 되도록 했다.
두 죄명의 관계는 두 조문이 모두 live일 때만 Call 2 후속 판정에 들어간다.

첫 통합 스모크에서 제298조의 승낙 부정 기준을 `satisfied`로 읽어 오히려
강제추행죄를 조각하는 방향성 오류가 발견됐다. 이에 전체 guard 20개를 감사하고,
피해자 행위의 정당방위와 심신미약을 support로 이동했다. 배임죄의 `타인의 사무`
카드도 guard에서 요건 issue로 분리했다. 현재 guard는 18개며, 모든 issue 질문은
요건·조각·단계·가담·죄수의 결론 방향을 문장에 명시한다.

## Scallop → Call 3 IRAC

Call 3는 마지막 모델 호출이다. 그 전에 호스트가 원시 Scallop relation을 성립,
미확정, 미수 검토, 성립 후 흡수, 경합으로 번역한다. 각 죄명 section은 하나의 통합
IRAC를 쓰고, Application 안에서 구성요건뿐 아니라 stage·participation·concurrence·guard
issue를 쟁점별로 포섭한다. 내부 JSON은 issue별 analysis를 정확한 수·순서로 유지하여
누락과 provenance를 검증하되, 최종 답안에서는 소형 IRAC를 반복하지 않는다.
rubric·모범답·원시 relation 배열은 모델에 주지 않는다.

핵심 요건이 `element_unaddressed`이면 원시 `offense_established`가 함께 있어도 작성
결론은 `undetermined`로 제한한다. 이 우선순위는 회귀 테스트로 고정했다. Pilot
rubric에서 살릴 구조와 corpus gap은 `docs/pilot_irac_handoff.md`에 별도 기록했다.
근거 없이 unknown인 deferred 공범·죄수·guard는 Call 3에서 제외하되, 초기 요건,
stage, 실제 판정된 후속 issue와 정확한 symbolic condition은 보존한다.

최신 전체 스모크 218151은 29개 Call 2 쟁점(15 satisfied / 3 not_satisfied /
11 unknown)을 거쳐 4개 죄명의 작성 대상 20개 쟁점을 모두 생성했다. 이후 표현 계약을
죄명별 통합 IRAC로 바꾼 Call 3 재실행 218152도 같은 20개 쟁점을 누락 없이 작성했다.
이 과정에서 제297조의 `attempt_review`와 제319조의 미확인 출입통제 사실을 산문에서 더
정확히 제한할 필요가 있음을 확인했다. 최종 계약에서는 모델이 Issue·Rule·Application과
쟁점별 소결만 작성하고, 죄명별 Conclusion과 종합 Conclusion은 동일한 symbolic directive에서
호스트가 결정론적으로 생성한다. 이는 문구 검증 게이트가 아니라 추론과 작성의 소유권
경계다. 최종 재실행 218155에서 이 계약과 20개 쟁점의 누락 없는 통합 IRAC를 확인했다.

## 향후 확률형 확장

현재는 `satisfied / not_satisfied / unknown` 3값 논리다. 향후 Call 1의 사실 추출
confidence를 보정하고 probabilistic provenance를 사용하면 구성요건별 지지·반증
신뢰도와 죄명 단위 신뢰구간을 산출할 수 있다. 특정 사실을 제거·반전했을 때의
결론 변화량을 계산하면 검사 측 보강점과 변호인 측 공격점을 정렬할 수 있다.
이 숫자는 법적 유죄확률이 아니라 모델 신뢰도·증거 민감도로 보고해야 한다.

## 검색 재평가

법률 검수된 rubric→조문 gold 31문항을 유지했다. rubric 문장을 issue ID로 자동 매핑하면
retriever로 gold를 만드는 순환 평가가 되므로 하지 않았다.

### 1. anchor-only issue 문서

검색 문서를 죄명 + issue 제목 + anchor 일반법리로만 만들었다. 판례 사안 노이즈는
사라졌지만 사건 사실과 가까운 어휘도 함께 사라졌다.

| top-k issue | retrieval recall | model union recall |
|---:|---:|---:|
| 18 | 0.537 | 0.777 |
| 36 | 0.721 | 0.882 |

운영 대안으로 부적합하다.

### 2. member card 검색 후 parent issue 투영

1,848장은 검색 신호로만 유지하고 당시 372개 parent issue로 접었다. 최초 프롬프트에는
anchor만 적재한다.

| top-k issue | retrieval recall | model union recall | runtime 조문 중위 | initial issue 중위 |
|---:|---:|---:|---:|---:|
| 18 | 0.598 | 0.814 | 12 | 38 |
| 36 | 0.752 | 0.867 | 20 | 66 |
| 48 | 0.844 | 0.935 | 24 | 77 |
| 60 | 0.853 | 0.935 | 28 | 95 |
| 72 | 0.882 | 0.952 | 31 | 105 |

현행 model ∪ top-18 article은 recall 0.927, runtime 조문 중위 21이며 최신 카탈로그 기준
initial issue 중위는 76이다. top-48 issue는 recall이 0.008 높지만 조문과 issue 적재량이
모두 더 크다.

따라서 운영 기본값은 top-18 article을 유지한다. 단, 점수 경로는 card→issue→article로
명시해 새 계층을 통과시킨다. 이 집계는 기존 max-card article 점수와 수학적으로 같으며
회귀 테스트로 동일 순위를 고정했다. top-48/72 issue는 accuracy-first 실험 옵션이다.

## 검증 기록

- Phase 3 관련: 123 passed
- 총배선 핵심: 102 passed
- L0 마이그레이션: 61문항 조문 배열 동일, flat card_ids 0행
- Phase 3 커밋 전 전체: 464 passed
- 총배선 완료 후 전체: 474 passed
- deferred review·조건별 심볼릭·Call 3 IRAC 추가 후: 481 passed
- 최종 통합 IRAC·작성 의미 보존 후: 487 passed
- 공개 실행경로·배치·확장 설정 정상화 후: 493 passed
- Python compileall 및 git diff --check 통과
- 검색 평가: PRO6000 잡 217961(anchor-only), 217972(card→issue)
- 최신 E2E: PRO6000 잡 218151(Call 2→Scallop→Call 3), 218155(통합 IRAC·호스트 결론)

## 남은 비차단 작업

1. stage·participation의 독자 결론 규칙은 법리 매핑 전까지 범죄 성립 gate에 넣지 않음.
2. 61문항 전체 Call 2 모델 실행은 비용·시간을 정해 별도 수행. 구조와 산출물 계약은 준비됨.
3. 진짜 issue-level 검색 recall을 채점하려면 rubric 항목→issue ID 법률 검수 자산이 필요.
   자동 semantic 매핑 결과를 gold로 쓰지 않음.
