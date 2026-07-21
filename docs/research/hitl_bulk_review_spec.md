# 전 죄명 rulegen — 통합 벌크 검토 스펙 + authority 정규화 정책 (초안)

작성일: 2026-07-21 · 상태: 초안(사용자 검토용)

사용자 결정(2026-07-21): 죄명별 왕복이 아니라 **전 죄명을 한 캠페인으로 생성한 뒤
단일 벌크 검토**를 한 번에 한다. 이 문서는 (A) 그 통합 검토 큐의 구조와 (B) 검토량을
줄이는 authority 정규화 정책을 규정한다. 근거 포렌식은 §3.

---

## A. 통합 검토 큐 (죄명 가로지르기, 법률-결정 유형별 정렬)

`fraud_norm_card_review_queue.json` 패턴(guide + queue + decisions ledger)을 전 죄명으로
합치되, **죄명별이 아니라 법률-결정 유형별로 정렬**한다. 전문가는 유형 단위로 일괄 판단한다.

큐 진입 **전** 기계·정책이 거르는 것 (전문가 미도달):

| 필터 | 처리 | 근거 |
|---|---|---|
| provenance (quote ⊆ source) | deterministic validator (실패 시 차단) | 전략문서 계약 |
| 스키마·계약 | deterministic validator | RuleIR 1.1 계약 |
| **authority_mismatch** | **§B 결정론 정규화 (자동)** | §3 포렌식: 라벨 문제, 결론 무관 |
| polarity 재발 | A6 host 극성분리 자동 | `neural/__init__.py` |
| 문법·컴파일·runtime | scallop compiler + golden test | — |

전문가가 **한 번에** 보는 유형 (큐의 실제 내용):

| 순위 | 유형 | 전문가 작업 | 정책 |
|---|---|---|---|
| 1 | **학설 대립 / variant_group** | 판례·실무 입장이 맞게 식별됐는지 confirm | **무조건 판례·실무 우선**(3.1). 매건 판단 아님, confirm |
| 2 | **overgeneralization / source_scope** | 카드가 주석 범위 넘었는지 판정 | 사람(3.3) |
| 3 | **negative 카드 질의문** | 긍정형 `neural_query` 초안 승인 | A6 극성분리, prompt-approval-gate |
| 4 | **golden-case 결론 라벨** | 사실관계→성립/불성립 정답 부여 | 데이터에 gold 결론 없음 → **유일 정답원천** |

- **front-load**: 1(학설 confirm)·4(golden 라벨)은 데이터에 정답이 없어 전문가만 채울 수
  있으므로 먼저 비운다.
- 각 큐 항목은 사기와 동일하게 `message`(무엇이) + `impacted_cards`(명제·인용) +
  `recommended_action`(기계 추천) + `human_review.{decision,notes}` 구조. 전문가 동작 =
  **confirm/override + notes** (백지 검토 아님).
- 정렬 키: `finding_type` → `module` → `priority`. 죄명은 2차 그룹.

## B. authority 정규화 정책 (검토량 ~37% 자동 제거)

### 포렌식 결론 (§3)
사기 67 지적 중 authority_mismatch **25건(37%)**은 전부 `authority_basis`·`doctrinal_status`
**라벨이 bounded source보다 과/부족**하다는 지적이다. critic 스스로 *"명제는 지지되나 'settled'는
아님"*이라고 인정 — **틀린 법리가 아니라 provenance 라벨 강도** 문제다. 그리고 두 필드는
`rules/`(컴파일된 Scallop)에 **0회 등장** → 성립/불성립 결론에 흘러들지 않는다.

### 정책 (결정론, 전문가 미개입)
NormCard validation 단계에 다음 정규화를 추가하고, 위반은 자동 하향(큐로 escalate 안 함):

1. **doctrinal_status = bounded source가 지지하는 최약값.** source가 판례를 명시(사건·법원
   식별)하지 않으면 `settled`/`precedent_position` 금지 → `descriptive`/`reported_doctrine`.
2. **authority_basis 분류 규칙:**
   - source가 특정 판례 결과를 서술 → `commentary_reported_precedent`
   - source가 작성자 '사견'·'견해' → `commentary_reported_doctrine` (판례 아님)
   - source가 법문 정의 인용 → `statute`
   - 그 외 종합 → `commentary_synthesis`
3. **'settled' 승격은 사용자 판례 index 대조 후에만** (전략문서 원칙 유지).
4. 정규화 결과는 `authority_normalization_ledger`에 자동 기록(감사 가능). 결론 무관이므로
   전문가 검토 불요.

### 잔여 예외 (여전히 사람)
- 정규화가 `commentary_reported_precedent`로 올린 카드가 실제 논지의 핵심 권위일 때 →
  판례 index 대조는 사람(§A 순위 1과 병합).

## C. 파이프라인 배선 지점

- authority 정규화: `finalize_fraud_norm_cards.py` 계열의 NormCard validation 직후 삽입
  (신규 죄명 finalize에 공통 적용).
- 통합 큐 생성: 죄명별 `<crime>_norm_card_review_queue.json`을 유형키로 merge하는 집계
  스크립트 1개 신설(사기 큐 스키마 재사용).
- golden-case 라벨: 죄명별 `<crime>_scallop_golden_cases.json`의 `scenarios`를 전문가
  라벨 큐로 노출.

---

## §3. authority_mismatch 포렌식 근거 (2026-07-21)

- 출처: `fraud_norm_card_review_queue.json` 25 항목 + `fraud_human_review_decisions.jsonl`.
- 25건 전부 결정 `accept_finding_pending_remediation`, remediation = 라벨 강등/재분류.
- 유형 본질: `commentary_synthesis`↔`reported_precedent`↔작성자 견해 오분류, `settled` 과표시.
- 다운스트림: `grep doctrinal_status|authority_basis|settled rules/` = **0 hit**. 두 필드는
  답안 출처표시와 rulegen review-routing 게이트(`doctrinal_status=="disputed"`)에만 쓰이고
  Scallop 규칙엔 부재 → 결론 불변.
- 결론: 전문가 검토 대상 아님, 결정론 정규화로 이관 가능. → 검토량 25/67 = 37% 감소.

관련: A3·A6(극성)·`idpr_remaining_work.md` · [[prompt-approval-gate]]
