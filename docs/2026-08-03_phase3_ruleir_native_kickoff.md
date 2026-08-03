# Phase 3 RuleIR-native 트랙 킥오프

## 1. 목적과 작업 경계

이 트랙의 목적은 기존 Phase 3 파이프라인에 예외 규칙을 더 붙이는 것이 아니다. 처음 의도한
다음 실행 순서를, 현재 저장소에 실제로 존재하는 RuleIR 자산부터 다시 구현하는 것이다.

```text
사건 원문
  → 폐쇄형 죄종·쟁점 식별
  → 호스트가 해당 RuleIR의 요구 predicate를 결정론적으로 전량 로드
  → predicate별 사실·역할·상태와 원문 근거 추출
  → Scallop 실행
  → derivation과 원문 근거를 생성기에 전달
  → 법률 답안 작성
```

- 작업 브랜치: `experiment/phase3-ruleir-native-20260803`
- 작업 worktree: `.worktrees/phase3_ruleir_native`
- 기준 커밋: `7313316`
- 종전 경량 실험: `experiment/phase3-special-part-light-20260803`에서 동결한다.
- 종전 경량 실험의 smoke 결과는 진단 자료일 뿐, 이 트랙의 구현 기반이나 성능 근거로 쓰지
  않는다.
- 진행 중인 V2 생성·채점 잡은 독립된 평가 실행이므로 변경하지 않는다.

장기 브랜치는 당장 수정하지 않는다. 이 트랙에서 계약, 회귀 테스트, 실제 Scallop smoke가
통과한 구성요소만 나중에 별도 커밋 단위로 이식한다.

## 2. 이번 리셋의 핵심 판단

### 2.1 첫 단계의 의미 검색을 제거한다

죄종 집합은 이미 유한하고 RuleIR 단위도 이름이 정해져 있다. 따라서 첫 단계에서 embedding,
BM25, top-k 카드 검색으로 죄종을 발견할 이유가 없다. 모델은 허용된 죄종·쟁점 enum 안에서
복수 쟁점을 식별하고, 호스트가 선택된 단위의 predicate를 로드한다.

검색은 필요하다면 죄종과 predicate가 정해진 뒤 판례 세부 근거를 보충하는 하류 단계에서만
사용한다. 검색 결과가 다음을 결정하게 하지 않는다.

- 어떤 죄종을 검토할지
- 해당 죄종의 필수 predicate 중 무엇을 생략할지
- Scallop에 공급할 predicate의 의미

### 2.2 모델이 predicate 목록을 자유 생성하거나 검색하지 않는다

모델의 책임은 두 가지로 제한한다.

1. 폐쇄형 목록에서 사건의 죄종·쟁점을 식별하고 당사자 역할 후보를 결박한다.
2. 호스트가 제시한 predicate 각각에 대해 사건 원문에 근거한 상태와 근거 구간을 반환한다.

필요한 predicate 집합은 RuleIR 파일이 유일한 기준이다. 모델이 이름을 새로 만들거나 일부만
선택해서는 안 된다. 상태가 불명확한 predicate도 누락하지 않고 `unknown`과 부족한 사실을
기록한다.

### 2.3 coverage를 가시성 휴리스틱으로 복구하지 않는다

이 트랙에서 coverage는 검색 후보 수나 답안 section 수가 아니라 다음 연결의 완전성으로
관리한다.

```text
선택된 죄종
  → RuleIR 요구 predicate 100% 열거
  → predicate별 assessment 100% 존재
  → Scallop 입력 또는 명시적 unknown으로 100% 변환
  → 결론 derivation과 사용 근거가 생성기에 전달
```

## 3. 현재 실제 자산과 지원 범위

저장소를 기준으로 보면 모든 형사법 영역에 동일한 수준의 predicate 자산이 있는 것은 아니다.
이 차이를 프롬프트로 감추지 않고 실행 계약에 드러낸다.

| 영역 | 현재 자산 | 초기 상태 |
|---|---|---|
| 사기 | `fraud_full_rule_ir_candidate_unreviewed.json`, 컴파일된 SCL, 실제 neural-to-Scallop 실행 선례 | 지원 후보 |
| 재산죄 각칙 | 10개 RuleIR candidate와 컴파일된 SCL | 지원 후보 |
| 친족상도례 | manifest에는 있으나 독립 RuleIR candidate가 없고 공유 후단 모듈로 설계됨 | 초기 지원 제외 |
| P2 생명·신체 등 | 카드 단위 자료는 있으나 현재 `p2_full.scl`은 6개 일반 predicate와 테스트 사실 중심 | RuleIR 미구현 |
| 총칙·절차법 | 현재 죄종별 고유 predicate RuleIR가 이 경로에 연결되어 있지 않음 | 범위 밖 |

실제 candidate JSON의 현재 규모는 다음과 같다. `commentary input`은 모델 평가 대상인
predicate 수이며, 각 파일은 현재 `draft`와 `legal_review: pending`이다.

| RuleIR 단위 | commentary input | 전체 predicate | rule |
|---|---:|---:|---:|
| fraud | 88 | 202 | 349 |
| theft | 66 | 154 | 309 |
| robbery | 98 | 222 | 443 |
| extortion | 41 | 102 | 204 |
| embezzlement | 64 | 147 | 304 |
| breach_of_trust | 36 | 90 | 173 |
| breach_of_trust_bribe | 41 | 99 | 198 |
| lost_property_embezzlement | 14 | 45 | 77 |
| property_damage | 53 | 124 | 257 |
| interference_with_exercise_of_right | 32 | 81 | 154 |
| occupational_status (공유) | 10 | 32 | 53 |

`지원 후보`는 법리 완성을 뜻하지 않는다. 현재 RuleIR에는 다음 알려진 한계가 있다.

- candidate 파일의 법률 검토 상태가 아직 pending이다.
- 일부 재산죄 component가 넓게 묶여 있어, 대체 카드 하나의 충족이 구성요건 전체 충족처럼
  전파될 가능성이 있다.
- deterministic card에 필요한 사건 입력과 `provable`, `case_assessment_complete`, 역할 tuple은
  호스트가 공급해야 한다.
- 일부 단위는 최종 죄명 relation을 호스트에서 성립·가중 결과와 조합해야 한다.

따라서 첫 구현은 자산의 존재와 실행 가능성을 검증하는 것이며, 법리적으로 미검토된 구조를
완성품이라고 간주하지 않는다.

## 4. 실행 계약

### 4.1 Stage A — 폐쇄형 issue splitter

입력은 사건 원문 전체다. 출력은 다음 필드만 허용한다.

- `issue_id`
- `unit_id`: 레지스트리에 등록된 값 또는 `unsupported`
- 행위자와 해당 RuleIR이 요구하는 역할 후보
- 해당 쟁점을 식별한 원문 인용
- 짧은 선택 근거

복수 죄종은 복수 issue로 분리한다. 단일 top-1으로 압축하지 않는다. enum 밖의 죄명이나
predicate를 생성하면 계약 실패다.

### 4.2 Stage B — 결정론적 predicate loader

호스트는 `unit_id`로 RuleIR 레지스트리를 조회해 다음을 제공한다.

- role predicate와 argument schema
- 모든 commentary input predicate
- 각 predicate의 정의와 `norm_card_id`
- system input predicate
- 실행할 compiled SCL과 query relation
- 공유 모듈과 알려진 제한

여기에는 검색과 LLM 선택이 개입하지 않는다. 초기 구현은 선택된 단위의 commentary input을
전량 평가해 누락으로 인한 recall 손실을 우선 막는다. 이후 비용 최적화는 동일 coverage를
자동 증명할 수 있을 때만 허용한다.

### 4.3 Stage C — predicate-grounded extraction

모델은 predicate마다 다음을 구조화해 반환한다.

- `status`: `satisfied`, `not_satisfied`, `unknown`
- 정확한 원문 근거 구간
- predicate argument에 대응하는 entity binding
- 판단 근거
- `unknown`이면 필요한 추가 사실

일반 FactGraph를 먼저 만든 뒤 predicate에 억지로 매핑하지 않는다. predicate 정의를 본 상태로
관련 사실을 추출하되, 원문에 없는 사실과 법률 결론을 사실처럼 보충하지 않는다.

### 4.4 Stage D — Scallop와 생성

호스트 검증을 통과한 assessment만 Scallop fact로 변환한다. 실행 결과는 단순 최종 label이
아니라 사용된 relation, derivation, 충돌·미확정 상태를 함께 보존한다.

생성기에는 최소한 다음을 전달한다.

- 분리된 쟁점과 역할
- predicate별 상태와 원문 근거
- Scallop 결론과 derivation
- unknown 및 충돌
- RuleIR 자체의 알려진 coverage gap

생성기는 이를 법률 답안으로 정리하지만 새로운 죄종, predicate, 판례를 발명할 수 없다.

## 5. 구현 순서

### M0. 자산 감사와 레지스트리

- fraud/property RuleIR와 compiled SCL을 하나의 레지스트리로 노출한다.
- article, unit, role predicate, commentary input, system input, query relation을 자동 추출한다.
- 중복 `norm_card_id → input predicate`, 누락된 compiled SCL, 선언되지 않은 query를 실패시킨다.
- P2·총칙·절차법은 조용한 fallback이 아니라 `predicate_ir_missing`으로 명시한다.
- JSON/Markdown 감사 보고서를 재현 가능하게 생성한다.

### M1. no-search issue splitter

- 레지스트리에서 enum을 생성한다.
- 복수 죄종과 역할 후보를 구조화 출력한다.
- 검색기와 article top-k를 호출하지 않았음을 manifest로 검증한다.

### M2. predicate assessment와 runtime adapter

- 선택 단위의 모든 commentary input을 전량 공급한다.
- predicate별 상태·근거·binding을 schema와 호스트 검증기로 결박한다.
- 기존 `scallop_runtime.py`가 요구하는 role tuple, assessment, `provable`, close-case 입력으로
  손실 없이 변환한다.

### M3. derivation-conditioned generator

- 성립·불성립·미확정·충돌을 구분해 전달한다.
- 생성 문장의 핵심 법리마다 predicate 또는 derivation provenance를 남긴다.
- unsupported 영역을 아는 척 생성하지 않는다.

### M4. 실제 RuleIR smoke

- 먼저 fraud와 property 개발 사례에서만 실행한다.
- 실제 compiled SCL을 실행하며 Python 조건문으로 결과를 흉내 내지 않는다.
- predicate completeness, grounding, runtime closure, derivation 전달을 자동 검증한다.
- 이 smoke가 통과하기 전에는 59문항 전체 생성이나 새 평가 잡을 제출하지 않는다.

## 6. 불변식과 중단 조건

다음은 구현 중 타협하지 않는다.

1. 초기 죄종 식별에 의미 검색을 사용하지 않는다.
2. 선택된 단위의 요구 predicate를 top-k로 잘라내지 않는다.
3. 모델이 enum 밖 죄종이나 predicate를 만들 수 없다.
4. 모든 predicate는 assessment 또는 명시적 계약 오류를 가져야 한다.
5. 사실 판정은 사건 원문의 인용 근거와 결박한다.
6. Scallop을 실행하지 않은 결과를 symbolic 결과라고 부르지 않는다.
7. RuleIR 미구현 영역은 기존 generic six-predicate 경로로 몰래 대체하지 않는다.
8. holdout 결과를 보고 predicate 정의나 라우팅을 문항별로 고치지 않는다.

다음 상황에서는 full run 대신 멈추고 자산 문제로 보고한다.

- 선택된 죄종에 RuleIR candidate 또는 compiled SCL이 없음
- 한 카드가 서로 다른 commentary predicate로 모호하게 중복 연결됨
- 필수 역할을 원문 entity에 결박할 수 없음
- assessment 수와 요구 predicate 수가 다름
- runtime query가 선언된 결론 relation을 배출하지 못함

## 7. 장기 브랜치 합류 조건

이 트랙이 장기 브랜치를 개선하는 방식은 전체 파이프라인 교체가 아니라 검증된 계층의 단계적
이식이다. 다음 조건을 모두 만족한 커밋만 합류 후보로 삼는다.

- 레지스트리와 감사 보고서가 재현 가능하고 테스트를 통과함
- issue splitter가 검색 없이 폐쇄형 복수 쟁점을 안정적으로 출력함
- 선택 단위의 predicate completeness가 100%임
- 실제 Scallop 실행과 derivation 보존이 검증됨
- 기존 장기 브랜치의 총칙·절차법 확장 지점을 막지 않음
- 경량판의 article-local 휴리스틱이나 사건별 예외가 섞이지 않음

초기 합류 후보는 `RuleIR registry/audit`, `predicate assessment schema`, `runtime adapter` 세
계층이다. 장기 브랜치의 기존 검색·FactGraph·가시성 로직을 한 번에 제거하는 결정은 별도 비교
실험 뒤에 한다.

## 8. 첫 산출물

킥오프 직후 구현할 첫 산출물은 모델 실행이 아니라 다음 세 가지다.

1. 코드에서 사용할 RuleIR 레지스트리
2. predicate·카드·컴파일·query 연결을 검증하는 감사 스크립트
3. 정상/중복/누락 자산을 다루는 집중 회귀 테스트

이 기반이 통과하면 issue splitter와 predicate-first neural extraction으로 넘어간다.
