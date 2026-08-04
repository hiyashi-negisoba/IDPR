# Phase 3 RuleIR-native 정상화 완료 기록

## 완료 범위

이 문서는 별도 검수 요청서가 아니라, 2026-08-03 킥오프에서 정한 정상화 트랙의 구현 상태와
재현 방법을 기록한다. 여기서 “완비”는 대한민국 형법 전체가 아니라 **현재 저장소가 보유하고
승인 원장으로 확정한 RuleIR 자산 범위**를 뜻한다.

- 등록·감사된 실행 단위: 36개
  - 기존 fraud/property 계열: 11개
  - 이번에 완비한 P2 비재산죄·공유모듈: 25개
- 전량 로드되는 commentary input predicate: 1,652개
  - P2: 1,109개
- P2 RuleIR rule: 6,141개
- P2 실제 Scallop 골든: 25개 단위, 272개 시나리오, 272개 통과
- 전체 저장소 회귀: 611개 통과

P2 25개는 직무유기, 공무상비밀누설, 수뢰·사전수뢰, 제3자뇌물제공, 뇌물공여,
공무집행방해, 위계공무집행방해, 범인은닉·도피, 위증·모해위증, 현주건조물등방화,
공·사문서 위조·변조와 행사, 허위공문서작성, 인장 관련 범죄, 살인, 고의·과실 신체침해,
강간·강제추행·준성범죄, 성범죄 미수·상해/치상 결과모듈, 주거침입·퇴거불응,
친족상도례 공유 처벌모듈이다.

## 최종 실행 경로

```text
사건 원문
  → 모델: 레지스트리가 만든 폐쇄형 unit enum에서 복수 죄종·쟁점 식별
  → 호스트: 선택 unit의 RuleIR commentary predicate 전량 로드
  → 모델: 사건 원문을 직접 보고 predicate별 satisfied / not_satisfied / unknown 반환
  → 호스트: 정확한 predicate 수, 원문 부분문자열 근거, 역할 tuple 검증
  → 호스트: 검증된 assessment만 Scallop EDB fact로 직렬화
  → 실제 scli 0.2.4 실행
  → 호스트: established / not_established / undetermined / conflict 도출
  → 생성기: 법리와 사실 적용만 작성
  → 호스트: Scallop 결론과 established relation을 최종 답안에 주입
```

이 경로에는 최초 의미 검색, article top-k, 카드 선택기가 없다. 모델은 unit이나 predicate 이름을
새로 만들 수 없고, 선택된 unit의 predicate를 줄일 수도 없다. 생성 모델의 출력 grammar에는
`conclusion` 필드 자체가 없으므로 Scallop 결론을 뒤집을 수 없다.

핵심 구현은 다음과 같다.

- `src/idpr/rulegen/registry.py`: manifest 기반 36개 자산 레지스트리와 감사
- `src/idpr/rulegen/native_host.py`: 폐쇄형 issue 선택, 전 predicate assessment, 실제 runtime,
  공유모듈 outcome bridge, 생성 directive
- `src/idpr/generation/native_rule_ir_answer.py`: Scallop 결론을 변경할 수 없는 writer 계약
- `data/rulegen/rule_ir_registry_manifest.json`: 등록 자산의 유일한 실행 allowlist

## 재산죄와 비재산죄의 연결

재산죄와 비재산죄는 별도 파이프라인이 아니라 동일한 `RuleIRRegistryEntry → assessment →
run_scenario → generation directive` 경로를 쓴다. 죄명별 Python 분기는 없다.

공유모듈은 `depends_on` outcome bridge를 반드시 요구한다. 전제 단위가 먼저 실제 Scallop에서
`established`를 내지 않으면 공유모듈은 실행되지 않는다. 실제 런타임 E2E에서 `theft`의 성립
결론을 `relative_property_crime_exception`에 연결하여 두 단위가 순서대로 성립하는 것을
검증했다. 같은 계약으로 성범죄 기수범에서 미수·상해/치상 결과모듈을 연결할 수 있다.

## 실패를 숨기지 않는 경계

레지스트리에 없는 총칙, 형사절차법 및 아직 만들지 않은 실체법 단위는 모델이
`unsupported`로 식별할 수 있지만, generic predicate나 검색 결과로 대체 실행하지 않는다.
호스트는 이를 `predicate_ir_missing`으로 반환한다. 따라서 현재 경로가 내는 symbolic 결론은
등록·감사된 36개 단위에 한정되고, 미지원 쟁점을 아는 척 처리하지 않는다.

RuleIR/NormCard JSON의 `draft`·`legal_review` 필드는 기존 validator가 산출물 형식을 고정하기
위해 유지하는 스키마 상태다. P2 실행 승인 상태의 기준은 각 unit의 승인 결정 원장과
`p2_native_unit_manifest.json`의 `approved_ledger_runtime_verified`, 그리고 아래 실제 런타임
보고서다.

## 검증과 재현

```bash
/data5/jaehoonjeong/miniconda3/bin/python scripts/audit_rule_ir_registry.py
/data5/jaehoonjeong/miniconda3/bin/python -u scripts/run_p2_native_scallop_golden.py
/data5/jaehoonjeong/miniconda3/bin/python -m pytest -q
```

- 레지스트리 감사: `data/rulegen/rule_ir_registry_audit.json` — 36개, 오류 0
- P2 런타임: `data/rulegen/p2/p2_native_scallop_runtime_report.json` — 272/272
- 기존 property 런타임 보고서: 10개 단위, 55/55
- 고정 런타임: `scli 0.2.4`, SHA-256
  `8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a`

주 워크스페이스 병합 후 전체 626개 회귀에는 RuleIR 결정론적 재생성, 계약 검증, registry audit, 기존 fraud/property
runtime, P2 runtime, 폐쇄형 선택, predicate 전량 assessment, 재산죄→공유모듈 bridge,
writer 결론 고정 테스트가 포함된다.

## 다음 단계의 정확한 의미

정상화 이후 실제 실행 진입점은 `scripts/run_rule_ir_native_lean.py` 하나다. 과거의 issue-search,
generic FactGraph, 245개 core projection 경로는 비교·사후분석용으로만 남아 있고 이 진입점에서
import하지 않는다. 이후 데이터셋 평가는 registry, predicate completeness, 실제 committed SCL
실행, 결론 고정이라는 네 불변식을 변경하지 않는 범위에서 수행한다.
