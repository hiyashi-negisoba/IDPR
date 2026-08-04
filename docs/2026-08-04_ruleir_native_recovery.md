# RuleIR-native 복구 기록

## 어디서 망가졌는가

전체 커밋과 2026-08-04 Codex 스레드의 마지막 대화를 다시 대조했다. 최초 데이터 손상은
`4b7a031`에서 property provenance request 16개를 삭제한 일이지만, 실행 설계가 처음
결정적으로 바뀐 지점은 `c7af2e5`다. 이 커밋은 1,730개 Scallop rule 통합을 표방했으나
실제 smoke 판단은 Python 조건문이 담당했고, SCL에는 소수 rule만 존재했다. 이후
`52f1c9f`부터 `dd3036b`까지의 generic 33-predicate Architecture A는 이 잘못된 전제를
확장했다. `767b163`의 자체 감사도 3,487 relations 중 body가 있는 rule 8개, tautology
1,592개, query 0개였음을 기록한다.

첫 복구 자산은 유효했다. `1bc6688`부터 `12f912b`까지 36개 RuleIR unit, 1,652개 input
predicate, committed SCL, native host, P2 272/272와 property 55/55를 만들었다. 그러나
`0016591`에서 1,652개 predicate를 245개 core component로 축약한 뒤, committed RuleIR가
아닌 새 AND/OR SCL projection을 실행하기 시작했다. 이것이 두 번째 결정적 파손이다.
당시 미완성 rewrite도 `execute_core_unit`에 의존했으므로 복구 기반으로 사용할 수 없었다.

## 사용자가 요구한 설계

```text
사건·질문 원문
  → 모델 1: 폐쇄형 RuleIR unit + 행위자/행위 + dependency 선택
  → 호스트: 선택 unit의 모든 role과 모든 predicate 로드
  → 모델 2: 원문을 직접 보고 전 predicate/role/status/근거 평가
  → 호스트: schema·완전성·원문 부분문자열 근거 검증
  → 선택 unit에 이미 커밋된 SCL을 실제 Scallop으로 실행
  → 모델 3: issue별 짧은 `법리`/`사안의 적용` Markdown만 작성
  → 호스트: 제목·결론·SCL path/hash·미지원 표지 부착
```

초기 의미검색, article top-k, generic FactGraph, predicate top-k, 245-core projection,
모델-only fallback은 이 경로에 없다. 등록 자산이 없는 쟁점은
`predicate_ir_missing`으로 남긴다. 모델은 symbolic conclusion을 생성하거나 바꿀 수 없다.

## 복구 조치

- 이전 미완성 rewrite는 `archive/pre-normalization-core-rewrite-20260804`의 `15bd09c`에
  보존했다.
- 활성 복구는 `recovery/ruleir-native-lean-20260804`에서 시작했다.
- `native_host.py`를 registry → 전 predicate assessment → committed SCL 실행으로 다시 썼다.
- answer writer를 whole-answer JSON에서 issue별 plain Markdown으로 줄였고 결론은 호스트가
  소유하게 했다.
- fact extraction/hybrid generation prompt를 제거하고 정확히 세 단계 prompt만 남겼다.
- `run_rule_ir_native_lean.py`를 새 단일 진입점으로 만들고 retrieval, FactGraph, core runtime
  import가 없음을 AST test로 고정했다.
- 실제 E2E가 발견한 `reported_label=unsupported`, unsupported dependency, 누락 actor role을
  호스트가 Scallop 전에 거부하도록 보강했다.
- README와 Slurm 진입점을 이 경로로 전환했다.

## 최종 증거

- 최종 복구 커밋: `0f4ff67af24c02b6bef598cda06d89ff713cf559`
- 전체 회귀: 617 passed
- prompt audit: 3 stages, 0 errors
- 실제 Gemma 4 26B + Scallop 잡: `219112`, `COMPLETED`, 2분 23초, exit 0
- 실제 문항: `kcl_criminal_r12_p1_q2`
- 모델 호출: selection 1 + full predicate assessment 1 + section writing 1
- 선택 결과: `theft`와 미지원 `사실의 착오`
- symbolic runtime: `scallop_scli_committed_rule_ir`
- 실행 SCL: `rules/generated/property_theft_v1_candidate.scl`
- SCL SHA-256: `ccf5353fddf085a9c4a491fad5557829e77b4559a4ed0ef1064d20ef15c4b974`
- symbolic conclusion: `undetermined`; 최종 답안에는 호스트가 `성립 여부 미확정`을 부착
- manifest 불변식: semantic search=false, FactGraph=false, core projection=false

실제 산출물은
`experiments/results/rule_ir_native_lean_smoke_219112/kcl_criminal_r12_p1_q2/`에 있으며,
selection, 전 predicate assessment, raw native report, section, host answer, manifest를 각각
보존한다. 생성물은 Git ignore 대상이고 실행 자산·계약·감사 문서만 버전 관리한다.
