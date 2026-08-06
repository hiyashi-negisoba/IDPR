# Current handoff

기준: 2026-08-05 · 브랜치 `antigravity-0804` · 최신 커밋 `fd2af1b`

## 먼저 읽을 것

활성 경로는 lean RuleIR-native입니다. 닫힌 레지스트리에서 유닛을 고르고, 등록된 주석
술어를 전량 적재하고, 원문 대조로 평가를 검증하고, 커밋된 Scallop 프로그램을 실행한 뒤,
모델은 법리·포섭 산문만 씁니다. **최종 심볼릭 결론은 호스트가 소유합니다.**

```text
사건과 문제
  -> 닫힌 유닛·쟁점·역할 선택
  -> 원문 대조 전량 술어 평가
  -> 커밋된 RuleIR SCL을 고정 Scallop으로 실행
  -> 호스트가 소유하는 심볼릭 결론
  -> 실행된 쟁점 전체를 한 번에 쓰는 IRAC 답안 1콜
```

진입점: `scripts/run_rule_ir_native_lean.py` · 표준 실행: **219371**(루브릭 7.0/27 = 25.9%)

이 경로에 semantic search, article top-k, 범용 FactGraph, 245-core projection,
모델이 쓰는 SCL, 모델 단독 fallback을 되살리지 마십시오. 없는 유닛은 `predicate_ir_missing`
그대로 둡니다.

## 역할 어휘 (검수 001~003으로 확정)

카드가 결론에 무엇을 하는지가 역할입니다. 이 구분이 무너져 상해죄·방화죄가 실제로
불성립했습니다 — "요건이 필요 없다"는 확인 법리가 `bar`에 앉아 있었습니다.

| 역할 | 결론 영향 | 뜻 |
|---|---|---|
| `component` | 만든다 | 요건 인정 경로 |
| `bar` | 막는다 | 요건 결여·배제 |
| `boundary` | 막는다 + 이동 | 이 죄가 아니라 다른 죄 (`refers_to`) |
| `waiver` (P2) | 막는다 | 위법성·책임 조각 |
| `waiver` (재산죄) | **없음** | 요건 불요 |
| `requirement_waived` (P2) | 없음 | 필수요건 오인분을 AND 목록에서 제거 |
| `assessment_standard` | 없음 | 판단기준·정의 — 요건을 **어떻게 재는지**만 |
| `proof_standard` | 없음 | 증명·특정 요건 |
| `subtype_outcome` | 없음 | 같은 죄 안의 의율유형 |
| `post_outcome` | 없음 | 죄수·처벌 효과 |

**P2와 재산죄의 `waiver`는 뜻이 반대입니다.** 이름을 공유하지만 같은 것이 아닙니다.

보고 역할은 **답안에 나갈 우리말 값을 원장에 반드시 적어야** 배출됩니다. 비면 카드 ID가
답안에 새기 때문에, 값 없는 카드는 조용히 빠지고 coverage gap으로만 남습니다.

## 이번 세션에 들어간 것

- 보고 역할 4종 신설 + `post_outcome` 배출(P2 빌더는 그동안 아무것도 안 만들었음)
- `{unit}_outcome_detail` — 죄수 payload를 자연어가 아닌 사실로 (`preserved_units`,
  `concurrence_type=real_concurrence` 등)
- 검수 002 C-02, D-01~D-07 원장 반영
- `effect_scope` (unit/track/component) — 기본값 `track`은 기존 25개 유닛에 무영향
- `variant_status` 5상태 + `variant_group` 배타 감사(둘 채택 시 컴파일 거부)
- `polarity=exception` 게이트 + **quarantine** — 유닛을 멈추지 않고 결론에 닿는 선만 절단
- 쟁점 단위 강등 — 계약 결함 하나가 사건 전체를 폐기하던 것 제거

## 남은 작업

### 1. 장물죄 146장 적재 — 다음 세션 1순위

카드는 이미 있습니다: `.cache/llm/runs/rulegen_downstream/stolen_property/20260804T144124Z/norm_cards/`
(146장, 머지·크리틱 완료, API 추가 지출 없음). 배치 002 E절에 **역할 재분류 전량 확정**.

**승인된 모델링**: 5개 행위태양(취득·양도·운반·보관·알선)을 **component가 아니라 track**으로
둡니다. 주체·장물성·고의는 공통 track에서 상속받습니다. 이래야 취득 track의 bar가
보관 track에 닿지 않는 것이 구조적으로 보장됩니다. (`effect_scope: component`만으로는
`elements_satisfied`가 component들의 AND라 결과가 같아집니다.)

착수 전 확인할 것:

- 역할 2종이 아직 없습니다 — `evidentiary_standard`(판례 사례형 증거판단,
  `assessment_standard`의 subtype), `procedural_outcome`(공소장변경 없이 인정 가능한
  죄명 범위 등). 배치 002 E-01/E-05에서 지시.
- 카드 분리 필요분 11장은 `excluded_pending_split`으로: E-01 3장(`sec3_2.foreign_offense`,
  `sec3_3.transport.knowledge_midway`, `sec3_3.custody.knowledge`), E-02 3장
  (`good_faith_acquisition`, `accession_processing`, `breach_of_trust_bribe`),
  E-03 1장(`resale_fraud_nonabsorption`), E-04 4장
- `sec3_2.object_movable_property` — ID와 명제 불일치(부동산도 일부 행위태양의 객체가 됨)
- variant 22장 전량 `variant_status: unselected`. 판례 견해가 명확한 3장만
  `authority_default` 후보이나, 배치 002 E-04에서 **판례번호·판시사항을 직접 결박한 뒤**
  선택하라고 지시.
- polarity/norm_kind 혼동 16장은 적재 **전에** 교정 (배치 002 F-03)

### 2. F-01 shared module `post_offense_absorption`

장물보관 후 임의처분이 불가벌적 사후행위라 별도 횡령죄가 성립하지 않는다는 죄수 효과.
배치 002 F-01에 bridge relation 8종과 출력 4종이 확정돼 있습니다.

**절대 어기면 안 되는 것**: shared module은 각 유닛의 구성요건 verdict를 소급 변경하지
않습니다. `embezzlement_not_established`로 덮어쓰면 구성요건 불성립과 불가벌적 사후행위를
혼동합니다. `elements_satisfied=true` + `separately_punishable=false` +
`reason=nonpunishable_post_offense`로 구분합니다. 호스트는 bridge fact 직렬화·실행·병합만
하고 법률 규칙을 Python `if`로 계산하지 않습니다.

현재 호스트는 쟁점별로 유닛을 독립 실행하고 유닛 간 사실을 주고받지 않습니다 —
bridge 경로를 새로 만들어야 합니다.

### 3. 사기 룰베이스 (검수 003 G절, 판정 완료)

사기는 배치 001에도 002에도 들어간 적이 없는 **세 번째 룰베이스**입니다
(`scripts/build_fraud_full_rule_ir_candidate.py`의 `BAR_CARD_IDS` 23장).
26문항 실행에서 불성립을 만든 6장 중 3장이 여기서 나왔습니다.

- **G-01**: 미수를 불성립으로 컴파일하는 3장. *"기수 부정·미수 성립을 한 묶음으로 고정하지
  말 것"* — `completed_offense=false` / `attempt_review_required=true` /
  `attempt_established`는 실행의 착수와 고의가 별도로 인정될 때만.
- **G-02**: 3장 → `boundary` (절도/절도/횡령) + `target_verdict=pending_separate_evaluation`.
  boundary가 발화해도 target 죄가 곧바로 성립하는 것이 아닙니다.
- **G-03**: `deception-target-human` → `assessment_standard`, 단 기준 predicate와
  사건사실 predicate(`actual_target_lacks_human_cognition`)를 **분리**해야 차단 가능.
  나머지 2장은 부정형 bar가 아니라 **긍정형 필수 component로 재작성**.
  `no-disposition-no-deception`은 "처분행위 없음 → 기망 없음"으로 컴파일하면 안 됩니다
  (기망은 있으나 처분에 이르지 않아 미수인 경우가 있음).
- **G-04**: 14장 일괄 bar 유지 **불승인**. 5장 bar 유지(2장은 조건부), 9장
  `assessment_standard`/`evidentiary_standard`, 1장 분리.

### 4. `polarity=exception` 88장 극성 복구 (검수 003 I)

`data/rulegen/exception_polarity_gate.json`. 현재 `enforce: false` + quarantine.
**무기한 유지 금지.** 지정된 처리 순서:

1. 실제 26문항에서 발화한 카드 → 2. `bar` → 3. `boundary` → 4. P2 차단형 `waiver`
→ 5. 도달 가능하나 미발화 → 6. 비활성

교정한 카드를 `approved`에 넣으면 정상 컴파일로 돌아갑니다. 88장 전량 처리 후
`enforce: true`. 발화 카드는 실행 기록의 `quarantined_effect_cards`에 남습니다.

`norm_kind=exception`은 규범의 성질이므로 건드리지 않습니다 — 고치는 것은 `polarity`뿐.

### 5. 평가 단계 재설계 (검수 003 H-01, 가장 큰 항목)

26문항 실행에서 카드 평가 **1,253장 중 85.5%가 `unknown`**이었습니다. 성립이 난 유닛은
예외 없이 satisfied 비율이 높고(방화 17/34), 미확정 유닛은 3~7장뿐입니다(살인 4/141).
**미확정의 원인은 규칙 부족이 아니라 평가 단계입니다.**

top-k 검색으로 풀지 말라는 지시가 명시돼 있습니다. 대신 **계층형 전량평가**:

1. 필수 component skeleton 먼저(객체·행위·고의·인과관계·기수미수·위법성책임)
2. 각 component와 연결된 카드만 그 단계에서 평가 — 검색으로 삭제하지 않음
3. `assessment_standard`는 사실평가 대상에서 제외, 법리로만 제공
4. variant는 선택된 견해만 결론 평가
5. 선행 component가 쟁점화된 경우에만 예외·bar 평가
6. 미확정 원인을 구조화(`fact_missing` / `role_binding_failed` /
   `standard_only_no_application_result` / `conflicting_assessments` /
   `required_component_unknown`)

H-02의 `component_status` 6분류와 측정치(component recall, fact-supported unknown rate 등)도
같은 작업입니다.

### 6. 이전부터 열려 있는 결함

- **Stage 1 / Stage 2 역할 결박 대조 없음 (P0)** — `role_candidates`와 `role_values`가
  각각 스키마 검증만 받고 서로 비교되지 않습니다. Stage 2가 Stage 1이 고른 행위자·객체를
  조용히 바꿀 수 있습니다. 코드에 비교 지점이 없음을 확인했습니다.
- **재산죄 golden 10건 실패** — `card_conflict_blocks`. 커밋 `2c4e75e`가
  `mandatory_component_negative`를 좁히면서 conflict 경로가 무장 해제됐습니다.
- **`test_section_writer_cannot_supply_host_conclusion` 실패** — 이제 죽은
  호스트 조립 경로를 지키는 가드입니다. 경로를 지울지 가드를 옮길지 결정 필요.
- **25개 P2 RuleIR이 `status=draft` / `legal_review=pending`** — 레지스트리 활성화가
  승인된 원장과 해시에 결박돼 있지 않습니다.
- **back-parse 검증 없음** — 답안이 derivation과 모순되는지 대조하는 단계가 없습니다.
- **`post_outcome` 191장이 `outcome_subtype` 미지정**이라 조용히 빠져 있습니다
  (coverage gap `unclassified_annotation`으로 노출). F-02의 7종 subtype으로 분류 필요.

## 진행 중

**배치 219740** — 26문항 전량, 쟁점 단위 강등이 들어간 첫 실행.
`experiments/results/rule_ir_native_lean_batch_219740/batch_status.tsv`.
직전 실행(219401)에서 15/26이 계약 위반으로 답안조차 못 냈으므로, 이번에 그 15건이
살아나는지가 확인 지점입니다.

집계에 쓸 것:
- `batch_status.tsv` — ok/failed
- 각 케이스의 `01_rejected_issues.json` — 강등된 쟁점과 `degraded_reason`
- `03_native_report.json`의 `quarantined_effect_cards` — 격리된 카드 중 실제 발화분
- `run_manifest.json`의 `rejected_issue_count`

## 실행 환경

- 추론 환경: `inv_ass_env`. **sbatch 설정은 건드리지 말고 전례대로만.**
- 셸에 conda가 활성화돼 있지 않으면 `IDPR_PYTHON` / `IDPR_VLLM_BIN` /
  `IDPR_MODEL_SOURCE`를 명시해 제출해야 합니다(219450이 이것 때문에 즉사).
- GPU를 만지는 작업은 길이와 무관하게 항상 sbatch. `nohup` 금지.
- 고정 심볼릭 런타임: `tools/scallop/scli-0.2.4-linux-x86_64`
- 레지스트리 매니페스트: `data/rulegen/rule_ir_registry_manifest.json` (36 유닛)
- 테스트: `python -m pytest` (레포 `.venv`는 빈 껍데기, 실제 파이썬은 miniconda)

## 검수 문서

| 배치 | 내용 | 상태 |
|---|---|---|
| [001](../reviews/review_batch_001_roles_and_stolen_property.md) | 역할 배치 36건 + 장물죄 4건 | 답변 완료·반영 완료 |
| [002](../reviews/review_batch_002_assessment_standard_and_stolen_property.md) | `assessment_standard` 설계 + 장물죄 146장 | 답변 완료·C/D절 반영, E/F절 미반영 |
| [003](../reviews/review_batch_003_fraud_bars_and_sweep_findings.md) | 사기 BAR 23장 + 26문항 실행 발견 | 답변 완료·H-03/I 반영, G/H-01 미반영 |

검수는 카드 단위로 판정하며, **검수 문서는 그 자리에서 답할 수 있어야** 합니다 —
재료만 나열하면 안 됩니다.

이어서 읽을 것: [`DESIGN.md`](DESIGN.md), [`RECOVERY.md`](RECOVERY.md),
[`../../project_init.md`](../../project_init.md). RuleIR 시그니처나 법률적 구성을
바꿀 때는 [`RULEIR_RISKS.md`](RULEIR_RISKS.md).
