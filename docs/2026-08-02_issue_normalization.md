# 2026-08-02 카드 적재 정상화·Phase 3·총배선 기록

## 결론

일반법리 카드가 없었던 것이 아니다. slot 단위 역할 상속 때문에 일반법리, 세부 판단기준,
판례 사안이 모두 독립 core 질문으로 적재된 것이 문제였다. 전체 1,848장을 다시 쓰지 않고
372개 법적 issue로 무손실 재배치했다. 운영 파이프라인의 단위는 이제 다음과 같다.

    검색 신호 카드
      → 부모 issue
      → 후보 조문
      → initial issue + anchor 일반법리
      → unknown일 때 같은 issue의 detail 최대 2장
      → issue_status
      → Scallop
      → issue reasoning packet

Phase 3 결과는 커밋 444aec5에 먼저 고정했다. 이후 이 문서가 설명하는 총배선과 검색
재평가를 별도 작업으로 진행했다.

## 전수 재분류

- 원본 카드 1,848장, 조문 51개, issue 372개
- 첫 평가 대상 element issue 159개
- anchor 일반법리 334장
- 조건부 retrieval 후보 1,246장
- symbolic-only 214장, support-only 54장
- 판례 사안형 629장은 anchor가 될 수 없음
- review flag 19개는 비판례 anchor가 없는 deferred issue이며 initial 평가에는 없음
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

1,848장은 검색 신호로만 유지하고 점수를 372개 parent issue로 접었다. 최초 프롬프트에는
anchor만 적재한다.

| top-k issue | retrieval recall | model union recall | runtime 조문 중위 | initial issue 중위 |
|---:|---:|---:|---:|---:|
| 18 | 0.598 | 0.814 | 12 | 38 |
| 36 | 0.752 | 0.867 | 20 | 66 |
| 48 | 0.844 | 0.935 | 24 | 77 |
| 60 | 0.853 | 0.935 | 28 | 95 |
| 72 | 0.882 | 0.952 | 31 | 105 |

현행 model ∪ top-18 article은 recall 0.927, runtime 조문 중위 21, initial issue 중위
71이다. top-48 issue는 recall이 0.008 높지만 조문과 issue 적재량이 모두 더 크다.

따라서 운영 기본값은 top-18 article을 유지한다. 단, 점수 경로는 card→issue→article로
명시해 새 계층을 통과시킨다. 이 집계는 기존 max-card article 점수와 수학적으로 같으며
회귀 테스트로 동일 순위를 고정했다. top-48/72 issue는 accuracy-first 실험 옵션이다.

## 검증 기록

- Phase 3 관련: 123 passed
- 총배선 핵심: 102 passed
- L0 마이그레이션: 61문항 조문 배열 동일, flat card_ids 0행
- Phase 3 커밋 전 전체: 464 passed
- 총배선 완료 후 전체: 474 passed
- Python compileall 및 git diff --check 통과
- 검색 평가: PRO6000 잡 217961(anchor-only), 217972(card→issue)

## 남은 비차단 작업

1. 비판례 anchor가 없는 deferred issue 19개는 법률 검수 후 병합 또는 일반법리 보강 가능.
2. stage·participation의 독자 결론 규칙은 법리 매핑 전까지 범죄 성립 gate에 넣지 않음.
3. 61문항 전체 Call 2 모델 실행은 비용·시간을 정해 별도 수행. 구조와 산출물 계약은 준비됨.
4. 진짜 issue-level 검색 recall을 채점하려면 rubric 항목→issue ID 법률 검수 자산이 필요.
   자동 semantic 매핑 결과를 gold로 쓰지 않음.
