# Current handoff (v1 최종본, archived)

> 이 문서는 2026-08-08 v2 DSL 개편(`deadline_v2_0808` 브랜치) 착수 시점에
> `docs/handoff/CURRENT.md`를 그대로 옮겨 보존한 것이다. v1(article/unit-centric
> RuleIR + neural-visible `bar`/`waiver`/`boundary`/`component` role)의 마지막 상태와
> 디버깅 경위 전량이 여기 담겨 있다. v1은 `main`/`antigravity-0804`(커밋 `0268635`)에
> reproducible baseline으로 동결되어 있다 — 이 문서가 기록한 문제의식(극성 버그,
> predicate 중복, string 기반 dependency 등)이 `docs/v2_plan/IDPR_v2.1.0_DESIGN_PROPOSAL.md`
> 21절 "Migration Principles from v1"의 직접적 근거다. 현재 작업은
> [`CURRENT.md`](../../handoff/CURRENT.md)를 우선한다.

기준: 2026-08-07 · 브랜치 `antigravity-0804`

## assess 프롬프트 bar/boundary/waiver 극성 버그 수정 — A+B+C 성공 확정 (2026-08-07, 새 세션)

바로 아래 "Consistency/coverage 저하 포렌식" 절이 남긴 B버킷(negative-polarity
카드 오적용, harboring_offender 최우선)을 이번 세션에 고쳤다. **결론: 성공,
freeze.** 다음 세션은 이 프롬프트를 또 건드리지 말고 아래 "다음 트랙"으로
진행할 것.

### 세 가지 변경 (전부 설치·재빌드·pytest 통과 완료)

**A — 스키마 필드 순서**: `native_host.py`의 `predicate_assessment_schema()`에서
`status`가 `assessment_rationale`(구 `inference_rationale`)보다 먼저 나오던
걸 뒤집었다. guided decoding은 property 선언 순서대로 토큰을 생성하므로,
모델이 근거를 한 글자도 안 쓰고 `status`부터 확정하던 게 원인 — 같은 세션
앞부분에서 고친 라우팅 버그(`candidate_fit_notes`를 `unit_id` 앞으로)와 동일
메커니즘. `assessment_rationale`을 전 predicate·전 status 필수(빈 문자열
불가)로 승격.

**B — card_role 배선**: 카드의 극성(`bar`/`boundary`/`waiver`/`component`/
`assessment_standard`/`requirement_waived`/`proof_standard`/`subtype_outcome`/
`post_outcome`)이 원장(`*_approved_decisions.json`)에만 있고 RuleIR predicate로
컴파일되며 사라지던 걸, `scripts/build_p2_native_rule_ir.py`의
`card_predicates()`/`emit_cards()`에서 `add_predicate(..., card_role=...)`로
보존해 `native_host.py`의 `predicate_assessment_request()`가 모델 payload에
포함하도록 배선했다. **p2-native 25개 유닛에만 적용** — fraud/property 11개
유닛은 별도 생성 스크립트라 이번엔 안 건드림(아래 "다음 트랙" 참고).
`docs/contracts/rule_ir.schema.json`의 `$defs.predicate`에 `card_role` optional
필드 추가(재산죄 파이프라인의 `fraud_rule_ir_generation_prep_manifest.json`
artifact-hash 게이트가 이 스키마 파일도 감시하고 있어서, 순수 additive 변경임을
사유로 남기고 `artifact_rehash_log`에 재해시 — 사기 계약 자체는 불변).

**C — 프롬프트 재작성**: `prompts/rule_ir_native_predicate_assess.md`에
"먼저 쓰고 나서 정한다"(A 반영) 절과 "card_role" 절 신설. 핵심 불변식(사용자
확정 문구): **"각 predicate의 사실관계 대조 기준과 증명 수준은 card_role과
무관하게 동일하다"** — bar라서 기준을 더 까다롭게 적용하는 게 아니라 bar
predicate의 정의 자체가 좁게 쓰여 있으니 그 정의를 정확히 대조한다는 뜻.
`bar`/`boundary`/`waiver` 셋 다 satisfied면 track을 defeat하는 동일 권한을
가짐(waiver도 blocking — 정당방위·사회상규 등 법적 성격은 다르지만 defeat력은
bar와 동일, `build_p2_native_rule_ir.py`의 `BLOCKING_ROLES` 참고). **다른
predicate와의 동시 satisfied를 금지하는 문구는 넣지 않음** — component와
bar/boundary/waiver가 반대 방향 법적 효과를 가진다는 이유만으로 동시satisfied를
막으면 predicate assessment가 symbolic outcome을 미리 알고 사실판단을 왜곡하는
outcome leakage가 된다(사용자 지적). 승인 게이트 준수, 전문 검토 후 설치.

### 26개(curated_26.txt) before/after 재검증 — 방법론과 결과

**중요한 용어 구분(사용자 지시)**: `scripts/check_assess_self_contradiction.py`
(신규, API 호출 0건)는 card_role 기반 negation-proximity 정규식 휴리스틱이라
**heuristic candidates**(자동 플래그)와 **confirmed contradictions**(직접
판독해 확정한 것)를 분리해서만 보고한다 — 휴리스틱 출력 자체를 "자기모순율"로
부르면 안 됨. before(오늘 이전 61개 산출물 중 겹치는 26개, 옛 필드명
`inference_rationale`)과 after(오늘 A/B/C 적용 후 26개 재생성, 25/26 성공·
1개는 JSON truncation으로 생성 자체 실패)를 **같은 26개 케이스**로만 비교.

| | before | after |
|---|---|---|
| heuristic candidates | 19 | 28 |
| confirmed contradictions(직접 판독) | 11 | 8 |
| heuristic false positives | 8 | 20 |
| symbolic-writer inconsistencies(`06_verdict_consistency.json`, 기존 무료 산출물) | 0 | 2 |

confirmed를 trust_status로 쪼개면: before는 11/11이 전부 `verified`. after는
`verified` 3건(homicide `method_error_precedent`×2, bribe_giving
`independent_third_party`×1) + `rejected`(`contract_degraded`, host 검증기가
이미 걸러 writer에 안 감) 5건(전부 `r14_p1_q2`/fraud 한 이슈에 몰림) — `verified`
confirmed가 **11→3, 73% 감소**. `provisional`은 두 run 다 0건.

원래 동기가 된 `r10_p2_q2`/harboring_offender 직접 대조: before는 제가 읽은
9개 bar/waiver 전부 확정 모순(`omission_concealment_general_citizen`
"부작위가 아니라 적극적 작위"인데 satisfied, `relative_cohabiting_family`
"친족이나 동거 가족이 아니다"인데 satisfied 등 — CURRENT.md 원 기록과 정확히
일치). after는 같은 케이스·같은 issue에서 satisfied된 predicate 17개 전부
`component`(15)/`post_outcome`(2)뿐, **bar/boundary/waiver는 0건** — 결론도
`established`로 정상.

**최종 판정(사용자 확정)**:
- A+B+C → **성공**. 다만 "파이프라인 전체 문제 해결"이 아니라 "assessment
  polarity 버그를 상당 부분 고쳤다"로 범위를 한정한다.
- harboring_offender blocking polarity bug → **fixed**.
- p2-native 일반 blocking polarity bug → **substantially mitigated**.
- 잔여 p2-native 오류 → predicate-specific defect backlog(아래).
- fraud/property blocking polarity → **별개의 미해결 파이프라인 이슈**(card_role
  미배선). fraud 5건을 "A+B+C 실패"의 근거로 넣지 않는다 — 이번 fix의 핵심
  입력(card_role) 자체가 그 파이프라인에 안 들어갔으므로 동일 조건의 after가
  아니다. 오히려 card_role 있는/없는 두 파이프라인의 confirmed 격차(p2-native
  3건 vs fraud/property 5건, 둘 다 candidates 기준으로도 22 vs 6로 fraud 쪽이
  훨씬 많음)가 card_role 가설을 뒷받침하는 좋은 진단 근거가 됐다.

### symbolic-writer inconsistency 2건 — 직접 읽어 분류 완료(사용자 지시)

두 건 다 `06_verdict_consistency.json`은 "symbolic-writer inconsistency"로만
부르고 **"writer error"라고 부르지 않는다** — 1번처럼 symbolic이 틀리고
writer가 맞을 수 있기 때문(사용자 지적).

1. **`r11_p2_q1_da`/quasi_sexual_offense issue_1** — **기존 predicate
   assessment defect**(오늘 A/B/C 이전부터 있던 별개 버그,
   `assess_art299_sec3_1_object_incapacitated_person` 과다충족). symbolic
   verdict(`established`, verified)가 잘못됐고, writer가 본문에서 "C는
   반항 불가능할 정도로 취하지 않았다"는 사실관계를 스스로 논증해 정확하게
   `not_established`로 거부했다. **A/B/C로 인한 writer regression 아님.**
2. **`r14_p2_q1`/obstruction_of_official_duty issue_6** — **writer
   completeness defect**. 답안 전문(2,611자)에 "공무집행방해"/"공무원"/
   "체포"/"경찰관"이 단 한 번도 안 나옴 — issue_6 본문 논의가 통째로
   누락됐는데 `VERDICT_MANIFEST` 트레일러에는 `not_established`가 기계적으로
   채워짐. **verified-directive refusal이 아니라 body-manifest coverage
   mismatch** — 5개 이슈(절도·절도미수·상해·강도·공무집행방해)를 한 답안에
   담아야 했는데 하나가 빠진 것. 다음에 열 때 참고할 별도 후보로 기록만.

### 다음 트랙 (프롬프트는 또 건드리지 말 것)

1. **fraud/property 11개 유닛 card_role 배선** — 별도 생성 스크립트
   (`build_fraud_full_rule_ir_candidate.py` 등)에 A/B와 같은 원리로 card_role을
   태워야 함. `card_role` 있음/없음 두 파이프라인의 confirmed 격차가 이미
   증거이므로 우선순위 높음. 배선 후엔 다시 26개(또는 D버킷 사례)로 before/after
   재검증할 것 — 이번 26개 after 수치와 섞지 말 것(동일 조건 비교 아님).
2. **predicate-specific defect backlog**(국소 조사, 프롬프트 재설계 아님):
   - `homicide.assess_art250_sec1_15_method_error_precedent`(bar) — rationale이
     "이 사건은 방법의 착오가 아니라 객체의 착오"라고 쓰면서도 satisfied.
   - `bribe_giving.assess_art133_sec1_2_independent_third_party`(bar) —
     rationale이 "독립된 제3자에 해당한다"(bar의 부정 조건 미충족 방향)라고
     쓰면서도 satisfied.
3. **부수 발견 — `exception_polarity_gate.json` quarantine**:
   harboring_offender의 `art151_sec2_2.relative_cohabiting_family`/
   `art151_sec2_4.family_support_social_adequacy`(둘 다 waiver, "친족특례"
   계열)가 극성 미검수로 quarantine 상태라 satisfied돼도 컴파일된 결론에
   영향을 못 준다(`build_p2_native_rule_ir.py`의 `quarantined_cards()`).
   이번 세션 dev case 설계 중 우연히 발견 — 이번 fix와 무관, 검수 백로그로만
   기록.
4. **1/26 생성 실패**(`kcl_criminal_r12_p1_q1`, JSON truncation): predicate당
   `assessment_rationale` 필드가 늘면서 큰 유닛(theft/robbery 등, predicate
   90개 이상)의 출력 토큰이 늘어난 게 원인일 가능성 — 자기모순과 무관, 기록만.

### 운영 메모(재발 방지용 코드 수정, 이번 세션)

- `scripts/run_rule_ir_native_lean.py`의 `_git_commit()`이 compute 노드에
  `git` 자체가 없을 때(`FileNotFoundError`, non-zero exit과 다른 케이스)
  전체 케이스를 실패시키던 것을 fail-soft로 수정 — provenance 메타데이터만
  `null`, 케이스 결과물은 그대로 저장됨.
- `scripts/slurm/run_rule_ir_native_lean_batch.sh`에 `IDPR_INVENTORY`
  env var 추가 — 합성 dev case를 실제 시험 인벤토리에 안 섞고 별도 jsonl로
  돌릴 수 있음(`.cache/dev_case_lists/harboring_offender_regression.jsonl`).
- sbatch 환경변수 3종(`IDPR_HF_HOME`/`IDPR_PYTHON`/`IDPR_VLLM_BIN`) 필수 —
  [[sbatch-must-set-idpr-hf-home]] 메모리에 이번에 반영.

## Consistency/coverage 저하 포렌식 + 구조 버그 2건 수정 (2026-08-07, 새 세션)

바로 아래 "라우팅 decision-avoidance 버그" 절이 남긴 4가지 "다음 세션 판단용 이슈"
중 1번(consistency 자기모순)·4번(coverage "쟁점은 잡았는데 결론 반대")을 파고들어
**두 개의 서로 다른 구조적 Scallop 컴파일 버그를 확정·수정**했다. 3번(narrow
hallucination)은 후처리 스크립트까지 만들었으나 대기 상태.

### 포렌식 방법과 결론 — "모델 강제-불이행" 아니라 상위 단계 결함

consistency 최저점 3건(`r11_p2_q1_da`, `r12_p2_q1_da`, `r13_p1_q3`)을 `03_native_report.json`
(symbolic_conclusion/trust_status) → predicate assessment evidence → 컴파일된 `.scl`
룰 정의까지 코드 레벨로 직접 대조. **3건 다 "모델이 강제 지시를 어긴 것"이 아니라
강제 지시 자체가 상위 단계 결함으로 틀린 값을 만들어놓고 모델에게 그대로 따르라고
시킨 것**이었다 — writer는 스스로 논증하면 매번 정답을 냈다가 지시 때문에 뒤집혔다.

- **r13_p1_q3(丁의 살인미수)**: **Scallop 구조 버그.** `homicide_attempt_elements_satisfied`가
  미수 전용 요건(실행착수·미수처벌)뿐 아니라 base(기수) 전용 요건인
  `homicide_base_person_ends_satisfied`(사망의 법적 확정)까지 그대로 상속하고 있어,
  피해자가 생존한 진짜 미수 사안에서 `homicide_attempt_established`가 정의상 영원히
  발화 불가능했다. predicate assessment는 정확했다(실행착수·미수처벌 전부 satisfied).
- **r11_p2_q1_da(준강간)**: assess 단계 카드 오적용. `assess_art299_sec3_1_object_incapacitated_person`
  (피해자가 실제 심신상실 상태였다)를 근거 인용문 "C와 함께 술을 마시던 중"만으로
  `explicitly_supported` 처리 — 사실관계 본문은 "C는 반항 불가능할 정도로 취하지
  않았다"고 명시.
- **r12_p2_q1_da(사문서행사죄)**: assess 단계 카드 오적용. `art234.forged_license_
  possession_and_driving_not_utterance`("위조 운전면허증 소지·운전은 행사 아님" —
  이 사건과 무관한 판례) 카드를 "주민센터 담당 직원에게 제출하여"라는, 운전면허·운전과
  전혀 무관한 인용문으로 satisfied 처리해 bar 발화 → 전체 불성립.

### 26개(실체법 전용) 세트 전체로 영향 범위 산정

`trust_status=verified` 지시 42건(26개 세트) 전부를 위와 같은 방식으로 대조.

| 버킷 | 건수 | 유닛 | 성격 |
|---|---|---|---|
| A. 구조(Scallop 컴파일) 버그 | 6/42 | homicide 4, obstruction_of_official_duty 2 | 확정, **이번 세션에 수정** |
| B. 프롬프트/assess 오적용 | 7/42 | use_of_forged_private_document 2, harboring_offender 3, intentional_bodily_injury 1, quasi_sexual_offense 1 | 확정, 미착수 — 다음 세션 대상 |
| C. 기존에 이미 알려진/보류된 결함 | 4/42 | robbery 4 | B등급(강도상해 결합범 트랙 부재), 신규 아님 |
| D. 미확정 | 4/42 | fraud 3, theft 1 | 핵심요건 unresolved — 진짜 불명확 사실관계인지 assess 저평가인지 미판정 |
| 미검증(문제없어 보임) | ~21/42 | — | 개별 확인 안 함 |

**A(구조) 신규 발견 — obstruction_of_official_duty**: `art136_sec2_4.active_conduct_requirement`
카드가 소스 norm card set에는 `polarity: positive`로 등록돼 있는데, 검수 원장
(`obstruction_of_official_duty_approved_decisions.json`)엔 `role: bar`로 배선돼 있어
모델이 "적극적 폭행이 있었다"고 정확히 판정할수록 오히려 `track_not_established`가
발화해 불성립으로 뒤집혔다. 같은 component(`violence_or_threat`)에 이미 사실유형별
bar 카드 5장(`passive_resistance_not_assault`/`preplaced_obstacles_not_assault`/
`self_harm_not_assault_or_threat`/`vehicle_departure_not_assault`/
`assault_not_against_officer_exception`)이 정확한 극성으로 존재해 이 카드는 그
일반원칙의 중복 재진술일 뿐이었다.

**B(프롬프트) 쪽 새 패턴**: harboring_offender 한 사례(`r10_p2_q2`)에서 **21개 bar
카드가 동시에 satisfied로 발화**했는데, 다수가 자기 rationale에서 "이건 아니다"라고
쓰면서도(예: `omission_concealment_general_citizen` rationale="부작위가 아니라
적극적 작위") status는 satisfied로 남겼다. negative-polarity 카드의 assess
프롬프트가 "이 카드 내용이 사건과 관련은 있다"와 "이 카드의 좁은 요건이 실제로
충족된다"를 구분 못 시키고 있다는 뜻 — 개별 카드 문제가 아니라 assess 프롬프트
설계 문제로 보인다.

### 구조 버그 2건 수정 완료 (이번 세션)

**homicide**: `data/rulegen/p2/native_review/homicide_approved_decisions.json`의
`track_vocabulary` → `attempt` track `inherits_placements`에서 `"person_ends"`
제거(`death_result`는 원래부터 미포함이라 그대로). `voluntary_desistance`/
`impossible_attempt`는 `inherits_from: attempt` 체인이라 자동으로 같이 고쳐졌다.
이 원장은 `authority: human_legal_review`(2026-08-04 승인)인데, 원 승인 문서
(`docs/review/2026-08-04_homicide_legal_gate_01.md` G-H02)는 attempt를 "상속: -"
(추가 상속 없음)로 표만 적었을 뿐 person_ends 포함을 명시한 적이 없다 — 기술
구현 단계에서 생긴 전사 오류로 판단, 승인 취지를 벗어나지 않는다고 보고 수정.

**obstruction_of_official_duty**: `obstruction_of_official_duty_approved_decisions.json`의
`art136_sec2_4.active_conduct_requirement` 카드 `role`을 `bar` → `context_only`로 변경
(위 5개 bar 카드가 이미 같은 내용을 올바른 극성으로 구현하므로 컴파일에서 완전히
제외해도 정보 손실 없음).

**재빌드**: 두 유닛 다 `build_p2_native_decision_ledger.py` → `build_p2_native_rule_ir.py`
→ `build_p2_native_scallop.py` 체인으로 재생성(미니콘다 `base` env, 시스템
`/usr/bin/python3`은 `dataclass(slots=True)`가 3.10+ 전용이라 실패 — 반드시
`/data5/jaehoonjeong/miniconda3/bin/python3` 사용). 컴파일된 `.scl`에서 버그 패턴
소멸 확인(`homicide_attempt_elements_satisfied`에서 `person_ends` 사라짐,
`active_conduct_requirement`가 obstruction `.scl`에 아예 안 나옴).

**검증(sealed-59 안 건드림)**: `scripts/run_p2_native_scallop_golden.py` — 승인
원장의 per-card placement에서 직접 유도한 합성 시나리오(실제 시험 문제 아님)로
검증하는 기존 스크립트. **homicide 35/35 통과**, **obstruction_of_official_duty
9/10 통과**(실패 1건 `official_coercion.bar_blocks`은 수정 전 원본에서도 동일하게
실패함을 git stash로 직접 재현·확인 — **내 수정과 무관한 기존 결함**, 다른 bar 카드
`art136_sec3_4.nonofficial_act_coercion` 문제로 보임, 다음에 열 후보로만 기록).
전체 pytest: **653 passed, 11 failed** — 실패 11건 전부 기존 문서화된 결함(재산죄
golden `card_conflict_blocks` 10건 + `test_section_writer_cannot_supply_host_conclusion`)
그대로, 회귀 없음.

### narrow hallucination 후처리 — 스크립트는 만들었으나 효과는 제한적, 대기

`scripts/check_article_citation_consistency.py`(신규) — 각 유닛의 `source_scope.
target_paths`에서 등록 조문을 뽑아, 답안이 인용한 조문이 라우팅된 유닛의 등록
범위 밖(+총칙 1~86조 아님)이면 플래그. 26개 답안 전체에 실행.

**실측 결과가 기대만큼 깨끗하지 않다.** 지난 세션이 "조문 번호 인용 실수라 기계적
검증으로 상당수 잡힐 가능성"이라 낙관했던 6건의 `statutory_error` 중 **딱 1건만
순수 번호 오타로 확인**(`r10_p1_q1_ga`: 강간미수에 제300조 대신 제302조 인용 —
스크립트가 정확히 잡음). 나머지 5건은 조문 항 구분(제164조 1항/2항), 총칙 조문이라
애초에 범위 밖 판정이 안 되는 경우(제30조), 유닛 범위 안에 있는 다른 카드를 못 골라
쓴 경우(제331조 제2항 vs 제329조), 조문 자체가 아니라 통째로 누락된 경우(제263조),
조문이 아니라 판례 취지 왜곡(fabricated_case) — 전부 실제 법리 판단을 요구해 기계적
치환으로 안 잡힌다. `narrow_hallucination_score_macro` 실측 -0.5(26개, 총
severity 13) → 위 1건만 고치면 -0.462로 소폭 개선에 그친다. **자동 치환은
안 함**(위양성 다수 — 정당한 대안죄명 논의를 오탐하는 경우 많음, 예:
`r10_p2_q2`의 "제347조" 플래그는 사기를 검토했다가 배제한 정당한 논증일 수 있음).
사람이 훑어볼 후보 생성 용도로만 사용. **다음 조치 안 함 — 위 A/B 버그를 고치면
부수적으로 줄어들 걸로 보고 대기.**

### 다음 세션 시작점 — assess 프롬프트 대대적 작업 (준비만, 미착수)

B버킷(7건, 4개 유닛)이 전부 같은 성격의 결함이다: negative-polarity(bar) 카드의
assess 판정이 "이 카드가 사건과 관련 있어 보인다"와 "이 카드가 정의하는 좁은
예외/배제 요건이 실제로 충족된다"를 구분 못 한다. 손대야 할 범위:

1. **harboring_offender 최우선** — 한 사례에서 21개 bar가 동시 발화, 다수가 자기
   rationale과 모순(스스로 "아니다"라고 쓰고 satisfied). 카드 하나가 아니라
   유닛 전체의 bar 카드 assess 결과를 다시 훑어야 할 가능성.
2. **use_of_forged_private_document** — `forged_license_possession_and_driving_not_utterance`
   카드(운전면허 관련, 이 유닛의 실제 사실관계 대부분과 무관)가 반복적으로
   오발화(`r12_p1_q1`, `r12_p2_q1_da` 둘 다). 카드 자체가 이 유닛에 있을 필요가
   있는지부터 재검토.
3. **intentional_bodily_injury** — `art257.minor_injury_exclusion`(경미상해 제외)가
   "3주 치료 요하는 상해"에도 발화, rationale은 "경미한 상처로 보기 어렵다"고 반대로
   서술.
4. **quasi_sexual_offense** — r11_p2_q1_da와 같은 패턴(약한 인용문으로 positive
   요건 과다 인정) 재확인 필요.
5. **fraud/theft(D버킷, 4건)** — 핵심요건이 genuinely_unresolved로 남는 것 자체가
   맞는지(사실관계상 정말 불명확) 저평가 버그인지 사례별로 먼저 판정한 뒤 B와
   같은 트랙으로 볼지 결정.

원장을 한 카드씩 손으로 고치는 homicide/obstruction 방식과 달리, 이건 카드 개별
문제가 아니라 **assess 프롬프트(`prompts/rule_ir_native_predicate_assess.md`)의
negative-polarity 카드 판정 지침 자체**를 다시 설계해야 할 가능성이 높다 — 프롬프트
승인 게이트 대상이므로 착수 전 설계안을 먼저 제시할 것. 착수 전 규모를 한 번 더
정량화할 것(현재 26개 세트 기준 7/42=17%로 추정했지만 harboring_offender처럼 한
사례에서 21개가 몰려 나온 사례가 더 있는지 61개 전체로도 확인 필요할 수 있음).

## 라우팅 decision-avoidance 버그 — 근본원인 특정 + 해결 (2026-08-07, 이번 세션)

**결론: 버그는 해결됐다 — 회피가 아니라 JSON 필드 순서 문제였다.** 아래 "다음 세션
시작점" 절이 다음 과제로 남겨둔 그 버그(모델이 `closest_allowed_unit_ids`에 정확한
후보를 스스로 적어놓고도 `unit_id=unsupported`를 고집하는 현상, 자유문구 수정
시도 3회 모두 실패·롤백)를 이번 세션에 해결했다. 지금부터 61개 전체 재생성+
재평가로 실제 coverage/precision 개선을 실측하는 중이다 — 진행 중인 job은 이 절
끝에 기록.

**2단계 방어선으로 접근했다:**

1. **Tier 1 (구조적 게이트, 안전망으로 유지)**: `native_host.py`에 닫힌 enum
   `unsupported_basis`(`no_matching_unit` / `participation_form_or_classification_
   uncertainty_only` / `not_applicable`) 추가 + `apply_routing_overrides()` —
   후보가 정확히 1개이고 참여형태 불확실성만이 이유일 때 host가 그 후보로
   자동 승격(role_candidates 완전성 검증을 통과해야만). dev case 스모크(job
   220254)에서 안전성은 확인(오탐 없음, 회귀 없음)했지만 **표적 사례(r14_p1_q2의
   `bribe_giving`)는 못 고쳤다** — 모델이 `unsupported_basis`를 `no_matching_unit`
   으로 잘못 골랐고(자기 `unsupported_reason` 문장은 "bribe_giving을 선택해야
   함"이라고 쓰면서), `role_candidates`도 비웠다.
2. **근본원인 진단**: `idpr.neural.vllm_client.VLLMClient.complete_json`이
   성공 경로에서 `reasoning_content`를 버리고 있던 것을 고쳐 캡처했다(job
   220279/220284). 결과: **이 호출엔 사고 단계 자체가 없었다** — `--reasoning-
   parser gemma4`가 서버에 켜져 있어도 이 호출은 `chat_template_kwargs`로
   thinking을 요청하지 않으므로 `message["reasoning"]`이 완전히 빈 값이었다.
   즉 모델이 숨은 사고 과정에서 먼저 결론을 내리고 감추는 게 아니라, **생각할
   기회 자체가 없었다** — 스키마의 per-issue 필드 순서(`issue_id → unit_id →
   ... → closest_allowed_unit_ids → unsupported_reason → unsupported_basis`)에서
   `unit_id`가 두 번째로 나오는 토큰이라, 자기회귀 생성상 모델은 이 쟁점에 대해
   비교 문장을 한 글자도 쓰기 전에 `unit_id`를 이미 확정한다. `unsupported_reason`
   에 나중에 옳은 결론("bribe_giving을 선택해야 함")을 써도 이미 지나간 토큰은
   못 바꾼다 — 이게 자유문구 프롬프트 수정 3회가 매번 다른 표현으로 똑같이
   실패한 이유다(프롬프트는 생성 시작 *전* 텍스트라 이 순서 문제를 못 건드림).
3. **근본 수정**: `closed_issue_selection_schema`에 새 필드
   `candidate_fit_notes`(자유 텍스트, 모든 issue에서 필수)를 `unit_id` **앞**에
   추가 — guided decoding 하에서 키 생성 순서가 스키마 property 선언 순서와
   정확히 일치함을 raw JSON 출력으로 직접 확인한 뒤(job 220284) 반영했다.
   `prompts/rule_ir_native_issue_select.md`에 "unit_id를 정하기 전에
   candidate_fit_notes를 먼저 쓴다"는 도입문 + 필드 설명 추가(승인 게이트
   준수, 전문 제시 후 설치). `scripts/audit_rule_ir_native_prompts.py` 계약
   문구 검사 추가, 테스트 픽스처 갱신, 전체 스위트 653 passed/11 failed(기존
   문서화 결함과 동일, 회귀 없음) 재확인.

**검증 (job 220292, dev case 2개, 재배열된 스키마)**: `r14_p1_q2`의 `issue_2`가
**자체적으로** `bribe_giving`을 정확히 선택(override 메커니즘 발동 없이 근본
수정만으로 해결) — `candidate_fit_notes`가 "...bribe_giving unit의 role_definition
...과 부합한다"를 먼저 쓰고 그 뒤 `unit_id`가 따라옴. `role_candidates` 4개 전부
정확히 채워짐 → symbolic execution 정상 실행(`established`) → **최종 답안이
처음으로 정확한 법리(증뢰물전달죄, 제133조 제2항)를 냄** — 이전 4번의 시도(자유
문구 3회 + Tier 1 enum)에서 매번 나오던 "일반 뇌물공여죄 방조/공동정범" 즉석
창작 오답이 사라졌다. 같은 사례의 `issue_3`(횡령)도 부수적으로 함께 고쳐짐.
`r10_p1_q1_ga`는 회귀 없음(issue_6 강도치상은 여전히 정확하게 `unsupported`/
`no_matching_unit` — 진짜 커버리지 공백, 후보 2개 다 실제로 안 맞음).

**일반화 판단(사용자 질문에 대한 답)**: 근본원인이 이 사례 특정이 아니라 모든
issue에 공통되는 생성 순서 구조이므로 낙관적으로 볼 근거가 있다 — 같은 사례
안에서 issue_3(횡령)도 같이 고쳐진 게 그 증거다. 다만 n=2 dev case만 확인된
상태라 61개 전체로 실측이 필요 — 그래서 바로 61개 전체 재생성+재평가로
넘어간다.

**61개 전체 재생성+재평가 완료 (2026-08-07, 같은 세션)**: sealed-59 오염
정책상 이 검증 자체는 디버깅이 아니라 최종 재평가이므로 sealed-59 전체를
다시 썼다(이전 61개 전체 재평가 때와 동일한 예외). SLURM
`--dependency=afterok`로 3단 체인 제출: 1) job 220293 `run_rule_ir_native_lean_batch.sh`
로 61개 전체를 candidate_fit_notes 반영 코드로 재생성(61/61 성공) 2) job
220294, 신규 `scripts/collect_rule_ir_native_lean_outputs.py`(이번에 작성 —
이전 세션엔 이 collector가 스크립트로 안 남고 즉석으로 처리됐던 구멍)로
run_dir → outputs.jsonl 변환, `data/eval/phase3_method_outputs.json`에
`idpr_nsn_lean_61_routing_fix` 등록 3) job 220295, `run_phase3_llm_judge.py`
(`--backend sonnet`, 새 judge 프롬프트, 61개 계약)로 재평가 — 1차 61/58건
(3건 API 오류로 실패: r13_p1_q3/r14_p1_q3/r14_p1_q5_2), `--overwrite` 없이
동일 명령 재제출(job 220445)해 기존 58건은 그대로 두고 실패 3건만 재시도 →
61/61 완결.

**서브셋 재구성 — `proc_kw` 정규식은 폐기, 정확한 카테고리 필드로 교체**: 지난
세션이 "28개 proc_kw 정규식 밀도<=10% 필터"라고 적었던 걸 재구성 시도했으나
직접 짠 키워드 목록으로는 전 사례가 4% 미만이라 필터링 효과가 전혀 없었다.
대신 `data/inventory/kcl_criminal_v1_draft.jsonl`에 이미 정확한 카테고리
필드 `legal_area`(`substantive`/`procedure`/`mixed`)가 있다는 걸 발견 —
`legal_area=="substantive"`가 job 219779 캐시에서 뽑은 26-curated 세트와
**정확히 일치**(집합 동등, 오차 없음), `substantive`+`mixed`가 정확히 28건.
`scripts/summarize_phase3_substantive_law_subsets.py`(이번에 작성)가 이
필드로 61/59/28/26 네 서브셋을 나누고, judge의 `aggregate_records`를 그대로
재사용해 이미 나온 `judgments.jsonl`에서 새 judge 호출 없이 서브셋별 macro/
micro 지표를 재계산한다.

**결과 — coverage와 precision이 둘 다 개선, 트레이드오프 없음**:

| method | 28개 cov | 28개 prec | 26개 cov | 26개 prec |
|---|---|---|---|---|
| chain_of_thought | 0.212 | 0.510 | 0.211 | 0.522 |
| **idpr_nsn_lean_61_routing_fix (이번)** | **0.199 (2위)** | **0.550 (1위)** | **0.209 (2위, 거의 동률)** | **0.582 (1위)** |
| idpr_nsn_lean_61 (지난 세션, 버그 있던 버전) | 0.168 | 0.524 | 0.179 | 0.560 |
| acal | 0.161 | 0.443 | 0.168 | 0.456 |
| legal_chain_reasoner | 0.157 | 0.455 | 0.166 | 0.476 |
| vanilla_zero_shot | 0.139 | 0.449 | 0.151 | 0.478 |
| standard_rag | 0.138 | 0.476 | 0.149 | 0.503 |
| leprec | 0.131 | 0.412 | 0.140 | 0.435 |
| fol_autoformalizer_solver | 0.094 | 0.371 | 0.101 | 0.394 |

나머지 7개 baseline은 이번 세션에 재채점하지 않았다 — IDPR 자체 생성만
바뀌었고 judge/backend는 지난 세션과 동일해서 그 숫자는 그대로 유효.
coverage 28개 0.168→0.199(+18%)/26개 0.179→0.209(+17%, 1위 chain_of_thought
0.211과 거의 동률), precision 28개 0.524→0.550(+5%)/26개 0.560→0.582(+4%,
이미 1위였던 격차를 더 벌림). "과다 커밋으로 precision을 깎을 수 있다"는
우려(위 일반화 판단 절)는 실측 결과 나타나지 않았다.

**라우팅 통계 (61개 전체, 226개 issue)**: unsupported 30.1%(68/226), 그 중
67개가 `no_matching_unit`(진짜 커버리지 공백 — 9월 이관 대상 총칙 공범 등),
1개만 `participation_form_or_classification_uncertainty_only`인데
`closest_allowed_unit_ids`가 0개(후보 자체가 없음, 마찬가지로 진짜 공백)라
승격 대상이 아니었다. **`apply_routing_overrides` 발동 0건** — 61개 전체에서
이번 개선은 전부 `candidate_fit_notes` 자체가 만든 것이고 Tier 1(구조적
게이트)은 이번 배치에서 안전망으로만 남아 있었다(오탐 위험 없음, 동시에
실효도 없었음). 답안 길이 평균 2961자(최단 1600~최장 4626자) — 붕괴 없음.

**교차 검증 — 알려진 두 라우팅 회피 사례가 61개 전체에서도 둘 다 자체
해결됨**: `r14_p1_q2` issue_2(bribe_giving, dev case 스모크에서 이미 확인)
외에, **`r12_p1_q1`의 issue_2/issue_3(사문서위조/위조사문서행사)도 자체적으로
`private_document_forgery`/`use_of_forged_private_document`로 정확히 라우팅**
됐다 — 이건 job 220070/220071/220074에서 자유문구 수정 3회로도 못 고쳤던
바로 그 사문서위조 사례다. 서로 다른 두 사례가 독립적으로 고쳐진 게 일반화
근거로 뒷받침된다.

**남은 진짜 공백(이번엔 손대지 않음)**: B등급(강도상해·강도치상 결합범 unit
부재, `r10_p1_q1_ga`의 issue_6이 계속 `unsupported`로 남는 원인) — 사용자
판단: 특정 sealed case를 겨냥한 카드 추가라 "치팅"에 가까울 위험이 있어
보류, 필요하면 art337/338 코퍼스·판례만 참고해서 착수([[sept-general-part-
restructure-design]]과는 별개 트랙, 각칙 결과적 가중범 문제). 9월 형총
재구조화(구성요건/위법성/책임 3단 분리)는 사용자가 별도 설계 중, 착수 안 함.

### 이번 세션에 발견, 착수는 안 함 — 다음 세션 판단용 이슈 4건

61개 결과를 사용자와 같이 훑어보다 발견. 전부 **기록만, 이번 세션엔 수정하지
않는다.**

1. **Consistency 하락(0.833→0.731, 26개 기준)은 judge 오독이 아니라 진짜
   자기모순이다.** 최저점(1점) 3건(`r11_p2_q1_da`, `r12_p2_q1_da`,
   `r13_p1_q3`) 전부 같은 패턴: 모델이 스스로 "성립한다"고 옳게 쓴 문장 바로
   옆에 "확정 결론의 지시에 따라 불성립"이라며 뒤집는다(`r13_p1_q3` 예:
   "B가 생존하였으므로 살인미수죄가 성립한다... 확정 결론의 지시에 따라
   살인미수죄는 불성립하는 것으로 결론 내린다"). 호스트의
   `check_verdict_consistency()`는 이 세 건 전부 통과시켰다(`06_verdict_
   consistency.json` 미생성) — 그 함수는 답안 끝 `VERDICT_MANIFEST` 트레일러가
   `verified` 상징 결론과 일치하는지만 보고, **트레일러에 도달하기 전 본문에서
   모델이 스스로 반대 결론을 먼저 서술했는지는 안 본다.** 이번 세션에 라우팅이
   더 많은 unit을 정확히 잡으면서 `verified`(반드시 그대로 따른다) 등급
   issue가 늘었을 것이고, 그만큼 이 노출 표면도 늘었을 가능성이 있다 — 인과
   관계는 추정, 확인 안 함. 기존에 이미 미결정으로 남겨둔 "자기모순 발견 시
   정책(현재는 기록만)"이 실제로 대가를 치른 사례. 다음에 다시 열 때: 트레일러
   일치 여부가 아니라 **본문 전체에서 강제 지시와 반대되는 서술이 등장하는지**
   검사하는 쪽으로 검증기를 확장할지, 아니면 writer 프롬프트에 "강제 지시와
   다른 결론에 먼저 도달했더라도 그 과정을 답안에 노출하지 말라"는 지시를
   추가할지 판단 필요.
   **규모를 텍스트 매칭으로 무료 정량화**(`확정.{0,4}(결론|판정)` 정규식으로
   답안 본문·judge 인용문 대조, 새 API 호출 없음): 26개 중 4점 미만(감점)
   18건 중 이 마커가 judge 인용문에 실제로 들어간 건 **정확히 3건 — 전부
   최저점(1점) 사례**. 나머지 15건은 이 패턴과 무관한 별개의 논증 오류
   (예: `r14_p1_q1`의 "살인교사 불성립"이라 해놓고 다음 문단에서 존속살해
   교사 책임을 인정하는 논리 비약, `r11_p1_q1`의 준강도/공갈미수 관련
   법리 오적용). 이 3건만 회복돼도(1점→3~4점 추정) consistency_macro가
   0.731→~0.80 근처까지 오를 걸로 추산 — legal_chain_reasoner(0.933),
   standard_rag(0.885)보단 낮지만 최하위는 벗어나는 규모. 실제로 다른
   점수를 얻으려면 (a) 답안을 고쳐 재생성 후 재채점 또는 (b) judge의
   consistency 채점기준 자체를 수정 후 재채점 — 둘 다 새 API 비용 발생,
   이번 세션엔 안 함.
2. **hallucination_score_macro라는 이름이 실제 측정 내용과 어긋난다.** 26개
   IDPR 답안의 사건 44건을 종류별로 까보니 `doctrinal_error`(법리 오적용)
   34건(77%), `statutory_error`(조문오기) 6건, `other` 3건, `fabricated_case`
   (허위 판례) **1건**, `nonexistent_offense`(없는 죄 창작) **0건**. 즉 지금
   이름이 암시하는 "지어낸 것"(없는 판례·없는 죄)은 26개 중 1건뿐이고, 나머지
   압도적 다수는 일반적인 법리 실수다 — 사실상 precision/rubric 정확도와
   개념이 겹치는 별도 지표를 "hallucination"이라는 이름으로 부르고 있다.
3. **좁은 정의(조문오기+허위판례만)로 재채점하면 IDPR 순위가 뒤집힌다.**
   신규 `scripts/compute_narrow_hallucination_score.py`(이번에 작성, 기존
   judgments.jsonl 재사용 — 새 API 호출 없음)로 8개 방법 전부 `statutory_error`
   +`fabricated_case`만 남겨 재계산:

   | method | narrow score(0=최선) | free_rate | 사건수 |
   |---|---|---|---|
   | fol_autoformalizer_solver | 0.00 | 100%(25/25) | 0 |
   | standard_rag | -0.231 | 84.6% | 4 |
   | chain_of_thought | -0.269 | 84.6% | 4 |
   | vanilla_zero_shot | -0.292 | 83.3%(24) | 4 |
   | acal | -0.385 | 76.9% | 6 |
   | **idpr_nsn_lean_61_routing_fix** | **-0.500** | 76.9% | **7** |
   | leprec | -0.538 | 76.9% | 7 |
   | legal_chain_reasoner | -0.654 | 80.8% | 10 |

   넓은 지표에서 IDPR이 상위권(공동 2위)으로 보였던 건 doctrinal_error가
   적어서였고, 좁은 지표(조문오기·허위판례)에서는 8개 중 **6위**로 떨어진다
   (표본 26개, 사건 수 4~10건대라 순위는 크게 신뢰 구간이 넓다는 점은 감안).
   IDPR의 narrow 사건 7건 중 6건이 `statutory_error`(조문 번호 오인용:
   미수범 조문 제300조 대신 제302조, 합동절도 제331조 제2항 대신 단순절도
   제329조, 현주건조물방화 제164조 제1항 대신 제2항, 합동범을 공동정범 조항
   제30조로 오인 등), 1건이 `fabricated_case`(동산 이중양도 배임죄 판례 취지를
   반대로 서술). **전부 조문 번호 인용 실수**라는 공통점 — 각 RuleIR unit이
   이미 `article_ids`를 갖고 있으니, writer가 인용한 조문을 그 unit의 등록된
   `article_ids`와 대조하는 기계적 검증(또는 자동 치환) 정도로 상당수가 잡힐
   가능성이 있다. 다음 세션 판단용 후보.
4. **coverage 채점의 공정성은 확인 완료 — 부당한 채점은 없었다.** 사용자
   요청으로 26개 전체 rubric item 735개 중 "judge가 답안에서 관련 문구를
   찾았는데도 not_met" 처리한 65건(오독 가능성이 가장 높은 부류) 전부를
   직접 읽었다. 65건 전부 진짜 실체법 불일치였다 — judge의 인용문·설명이
   답안 내용과 정확히 일치했고, IDPR이 그 쟁점을 다루긴 했는데 정반대
   결론(성립↔불성립, 미수↔기수, 실체적 경합↔상상적 경합, 단순절도↔특수절도,
   교사범↔공동정범 등)을 낸 경우들이었다. **다만 이 과정에서 새 패턴을
   발견**: 이 65건은 "쟁점을 놓친 것"(라우팅 문제, 이번 세션에 고침)이
   아니라 "쟁점은 잡았는데 결론이 반대로 나온 것"이다 — 전체 735개 rubric
   item의 8.8%. 이건 라우팅도 writer의 부수쟁점 서술 밀도도 아닌 **술어평가/
   규칙베이스 정확성**(symbolic 결론 또는 모델 자율판단이 어느 방향으로
   떨어지는가) 문제로 보이고, 이번 세션엔 손대지 않은 영역이다. 일부(`r12_
   p2_q1_da` idx19, `r14_p1_q2` idx5·18)는 위 1번(자기모순) 사례와 겹친다 —
   `verified` 강제 지시가 하필 틀린 결론이었던 경우라, 1번을 고치면
   consistency와 coverage가 동시에 개선될 여지가 있다.

### 채점 비용 절감 — 앞으로 judge는 26개(실체법 전용)가 기본 (2026-08-07, 사용자 결정)

**사용자 결정: "앞으로는 채점도 이 26개 셋으로만 하게 해줘" — API 비용
절감.** 절차법 33개는 IDPR이 원래 다루지 않는 스코프라 채점할 이유가 없다는
게 이미 확인된 사실([[idpr-paper-deadline]], 위 "방법론 결함 발견·정정"
절)이므로, 61개를 채점한 뒤 사후에 26/28로 잘라보는 대신 **처음부터 26개만
judge에 보낸다** — API 호출 수를 61/26≈2.3배 줄인다.

구현: `scripts/run_phase3_llm_judge.py`에 `--case-id-file`(신규) 추가 — 파일의
줄마다 하나씩 `--case-id`로 취급, 26개를 매번 손으로 나열하지 않아도 됨.
`scripts/slurm/run_phase3_llm_judge_sonnet.sh`/`run_phase3_llm_judge_sonnet_idpr.sh`
가 기본으로 `.cache/phase3_substantive_law_case_lists/curated_26.txt`를
쓰도록 변경(둘 다 `IDPR_JUDGE_CASE_LIST` 환경변수로 다른 목록 지정 가능,
필요하면 61개 전체도 여전히 가능). 출력 경로도 `phase3_judge_sonnet_26/`
등으로 새로 분리 — 기존 61개 전체 산출물(`phase3_judge_sonnet/`,
`phase3_judge_sonnet_idpr_routing_fix/` 등)은 그대로 보존, 절대 덮어쓰지
않는다(`--overwrite`가 `--out` 파일 전체를 선택된 case만으로 다시 쓰므로,
26개 파일로 `--overwrite`하면서 기존 61개 파일 경로를 그대로 쓰면 나머지
35개 결과가 통째로 사라진다 — 그래서 반드시 출력 경로를 분리했다). IDPR
쪽 스크립트는 `IDPR_JUDGE_METHOD_ID` 필수 지정으로 바꿔 매 세션 새 산출물
method-id를 하드코딩하지 않게 했다(예:
`IDPR_JUDGE_METHOD_ID=idpr_nsn_lean_61_routing_fix sbatch ...`).

## 지금 최우선 — 평가(judge)와 라우팅 구조 문제

**사용자 결정: 장물죄 원장 적재 작업은 잠시 보류. 이 문제부터 해결하고 원래 궤도로
복귀한다.** 26문항 Gemini 채점(아래)을 사용자가 직접 검토한 뒤 "말이 안 된다"고 판단,
FOL 답안 하나를 반례로 지목했다. 다음 세션은 여기서 시작할 것.

**다음 세션 시작점 (2026-08-07 갱신, 3번째): 라우팅 decision-avoidance 버그
해결.** 4단계(라우팅 출력 확장) → decision 단계 프롬프트 수정 시도 2회 실패·롤백
→ 5단계는 A등급(총칙 공범)이 9월로 이관되며 B등급 하나만 남아 보류 → 6단계
(judge 재설계 + 61개 전체 재평가, 완료) 순으로 진행한 뒤, **재평가에서 실체법
전용(26/28개) 기준으로 다시 봤더니 IDPR이 precision 1위·coverage 2위로
잘하고 있다는 게 확인됐다** — 아래 "재평가 완료" 절 참고. 남은 진짜 걸림돌은
이 라우팅 버그 하나뿐이라는 게 이번 재평가로 재확인됐다(coverage가 절반쯤
`unsupported`로 새는 것과 직결). **사용자 지시: 다음 세션은 이 버그 해결부터
시작한다.**

이전 시도 2회(참여형태 negative carve-out → 회피 사유 금지 목록으로 강화)는
프롬프트 문구 조정만으로는 안 뚫렸고("모델이 스스로 정답을 알면서도 확정을
거부"), 매번 다른 표현으로 같은 회피를 반복했다 — 상세와 세 번의 스모크 결과는
아래 "decision 단계 프롬프트 수정 시도 — 2회 실패, 롤백" 절 참고. 그 절 끝의
결론: **다음 시도는 프롬프트가 아니라 구조적 게이트**(`closest_allowed_unit_ids`가
비어있지 않은 채 `unit_id=unsupported`가 나오면 계약 위반으로 강등하거나 host-side
재검증 콜 추가 등)를 고려할 것 — M5 3콜 원칙을 벗어나는 설계 변경이므로 착수 전
사용자 승인 필요. 디버깅은 sealed-59 오염 정책(dev case 2개만) 준수할 것 —
이번 세션 61개 재평가는 이 정책의 명시적 일회성 예외였다.

**5단계 후보 — 출처 등급을 나눠서 볼 것 (아래 "sealed-59 오염 정책" 절 참고)**:
- **A등급(범위 제외, 9월로 이관): 살인교사·공모관계.** `declared_not_compiled`로
  2026-08-04자 `docs/review/2026-08-04_homicide_legal_gate_01.md` 등에 이번 세션 전에
  이미 문서화된 공백 — sealed case를 읽어서 발견한 게 아니라 출처 자체는 정당했다.
  다만 조사 결과 이건 살인 단일 unit 카드 몇 장으로 끝나는 게 아니라 **형법 총칙
  공범(30~34조: 공동정범/교사/방조) 자체를 다루는 shared module 설계**가 필요한
  작업임이 드러났다(같은 파일의 `intentional_bodily_injury.concurrent_offenders`,
  제263조 동시범 특례도 같은 이유로 `declared_not_compiled` — 공범 총칙 문제는
  살인 하나에 국한되지 않는다). **사용자 결정(2026-08-06): 총칙 쟁점·절차법은
  8/11 NLLP 스코프가 아니다. 9월 프로젝트로 이관, 이번엔 손대지 않는다.** 별도
  코드 변경 불필요 — `rule_ir_native_issue_select.md`가 이미 "독립 등록 unit이
  없으면 `unit_id=unsupported`로 별도 issue를 만들고 writer가 자율 논증"하도록
  설계돼 있어, 이 쟁점들은 계속 그 기존 경로(모델의 자유 서술)로 처리된다 —
  이번 결정은 "만들지 않는다"는 것이지 "답안에서 빠진다"는 게 아니다.
- **B등급(8/11 스코프 내, 유일한 활성 후보): 강도상해·강도치상 결합범.** 총칙이
  아니라 각칙(강도죄) unit의 결과적 가중 트랙이므로 위 이관 대상이 아니다.
  `data/rulegen/property/rule_ir_units/robbery.json`에 art337/338 norm card가 이미
  추출돼 있고, `data/rulegen/rule_ir_registry_manifest.json`의 `robbery` unit
  `query_relations`엔 `robbery_established/not_established/...`만 있고 상해·사망
  결과 트랙이 없다 — 이 자체는 사례 내용과 무관하게 레지스트리 vs 코퍼스 대조만으로
  확인되는 진짜 구조적 공백. 다만 **이번 세션에 이걸 1순위로 콕 집은 계기는
  sealed-59 소속 `kcl_criminal_r11_p1_q1`의 답안을 읽다가 실패를 본 것** — 착수할 때
  카드는 r11의 구체적 사실관계가 아니라 art337/338 코퍼스와 판례만 참고해서 짤 것.

**주의(5단계 착수 전에 반드시 읽을 것)**: 5단계는 라우팅 정확도 문제(라우터가
이미 있는 unit을 회피하는 결함)의 해법이 **아니다** — 서로 다른 결함 범주다.
5단계는 레지스트리에 아예 없는 unit을 새로 만드는 작업이고, 롤백한 시도는 레지스트리에
"이미 있는" unit을 라우터가 스스로 정확히 짚어놓고도 거부하는 결정 단계 문제였다.
5단계로 새 unit을 추가해도 이 회피 휴리스틱이 그 새 unit에 대해서도 똑같이 나타날
위험이 있다 — 두 문제를 하나로 섞어 "5단계가 끝나면 라우팅 정확도도 좋아졌겠지"라고
가정하지 말 것.

### sealed-59 오염 정책 (2026-08-06, 사용자 결정)

라우팅 정확도 회귀 배치(job 220070/220071/220074)가 쓴 6사례 중 4개
(`kcl_criminal_r11_p1_q1`, `r12_p1_q1`, `r13_p1_q1`, `r14_p1_q1`)는 승인된 dev
case 2개(`r10_p1_q1_ga`, `r14_p1_q2`, `scripts/build_phase3_final_eval_inventory.py`의
`DEVELOPMENT_CASES`)에 안 들고 **sealed-59 최종 평가셋 소속**이다. 디버깅 목적으로
이 4개의 답안·이슈선택 결과를 반복해서 읽은 것 자체가 이미 노출이고, 그 중 하나
(강도상해 결합범 공백)는 실제로 5단계 우선순위 판단에 영향을 줬다(위 "B등급" 참고).

**사용자 결정: 지금부터는 (a) — 라우팅/decision 단계 디버깅용 스모크는 승인된 dev
case 2개로만 제한한다.** sealed-59 소속 사례를 채점(최종 평가) 목적이 아니라
규칙·프롬프트 튜닝 디버깅 목적으로 다시 열어보지 않는다. 이미 노출된 두 사례
(r11_p1_q1 강도상해, r14_p1_q1 살인교사)는 소급해서 되돌릴 수 없으므로, 그 공백을
고치는 작업 자체는 위 A/B 등급 구분대로 진행하되(코퍼스 기반으로만 작성), 앞으로
새로운 디버깅 배치를 짤 때 sealed-59 case_id를 케이스 리스트에 넣지 않도록 주의.
필요하면 dev case를 승인 절차를 거쳐 추가하는 것을 고려(현재는 2개뿐).

### 26문항 채점 결과 (job 219790, `gemini/gemini-2.5-flash`)

`/data5/jaehoonjeong/IDPR/.cache/phase3_judge_219779/summary.json` (method
`idpr_nsn_native_lean_219779`, 26/26 완료):

| 지표 | 값 |
|---|---|
| coverage_macro | 0.246 |
| consistency_macro | 0.692 |
| precision_macro | 0.838 / precision_micro 0.821 |
| hallucination_free_rate | 0.346 (hallucination_score_macro -3.27) |

**주의**: 이 26문항 안에 phase3 sealed-59에서 의도적으로 제외한 dev case 2개
(`kcl_criminal_r10_p1_q1_ga`, `kcl_criminal_r14_p1_q2`, `scripts/build_phase3_final_eval_inventory.py`의
`DEVELOPMENT_CASES`)가 섞여 있다. 다른 방법(baseline)들의 기존 결과는 61문항 대상이라
이 26문항 숫자와 그대로 비교하면 안 된다 — 재정리 필요.

사용자가 특히 의심한 비교: FOL Autoformalizer+Solver의 consistency 85.96 > IDPR
69.23. `experiments/results/fol_autoformalizer_solver_outputs.jsonl`의 `kcl_criminal_r10_p1_q1_ga`
답안을 열어 보면 Z3 코드에 `s.add(Guilty(甲, Death))`로 **결론을 사실로 먼저 주입한 뒤**
같은 결론을 satisfiability 결과로 재출력하는 패턴이 보인다 — 이건 검증이 아니라 반복이다.
그런데도 이 답안이 높은 consistency 점수를 받았다면, 현재 judge가 코드/symbolic trace의
의미를 읽지 않고 **자연어 결론이 처음부터 끝까지 반복되는지**만 보고 있을 가능성이 높다.

### 사용자 진단: judge 문제

- 현재 Outcome Consistency judge가 실제로 측정하는 것은 "중간 서술과 최종 결론의
  표면적 반복 일관성"이지, 원하는 "중간 쟁점 판단 — 적용 법리 — 상징 결과 — 최종 죄책"
  간의 정합성이 아니다.
- FOL 답안은 결론을 여러 형식(FOL facts / Z3 output / legal conclusion / summary)으로
  반복하므로 전제가 틀려도 형식적 일관성 점수를 얻기 쉽다.
- IDPR 답안의 정상적인 법률 논증 어투("...성립 가능성이 매우 높다", "...인정된다면
  최종적으로 성립한다" 같은 조건부 서술 후 단정적 결론)를 judge가 충돌로 오인할 수 있다.
- 다음 세션 작업: judge 프롬프트가 코드/symbolic trace를 실제로 평가 입력에 포함하는지부터
  확인. 그 다음 평가기준을 다시 설계하고 **judge 백본을 `anthropic/claude-sonnet-4-6`로
  교체**해 전체 재평가. IDPR을 제외한 나머지 baseline들은 새 judge로 미리 돌려둘 수 있다.

### 사용자 진단: 파이프라인(라우팅) 자체의 구조적 결함

judge 문제와는 별개로, 실제 두 사례(kcl_criminal_r10_p1_q1_ga, r14_p1_q2)를 검토한 결과
라우팅이 죄명 수준에서 멈추고 시험이 요구하는 법리 단위까지 못 내려가는 것으로 보인다.

1. **핵심 하위 법리 카드가 라우팅 안 됨** — 예: 제263조(동시범 특례)와 제19조(독립행위
   경합)의 관계, 특수강도(흉기휴대)와 단순강도의 구별이 답안에서 사라짐. 대표 죄명
   (강도치사, 인과관계)만 잡히고 그 아래 단위(비유형적 인과관계, 개입원인, 객관적 귀속,
   위험창출/위험실현, 규범의 보호목적, 기본범죄 기수/미수와 결과적 가중범의 관계)가
   안 잡힌다.
2. **상위 카드가 선택돼도 필수 하위 쟁점이 자동 확장되지 않는다** — 카드를 독립적으로
   검색하는 구조에 가까워서, 상위 죄명은 나오는데 그 아래 요구되는 법리가 누락된다.
3. **불확정 사실이 대안 법리를 호출하지 못한다** — `unresolved`가 새 분기를 여는 대신
   사실상 `not_satisfied`처럼 처리돼, 인과관계 불명 → 상해치사 불성립 → 상해죄 성립으로
   바로 가버린다. 원래는 인과관계 불명 → 독립행위 경합 검토 → 263조 적용 가능성 → 19조
   적용 여부까지 이어져야 한다.
4. **symbolic 결과가 결론만 주고 논증 의무는 안 준다** — 생성 단계에 결론(성립/불성립,
   인과관계 인정/부정)만 전달되고, 반드시 다뤄야 할 학설·요건(조건설/상당인과관계설/
   합법칙적 조건설, 위험창출/실현, 규범의 보호목적 등)이 체크리스트로 전달되지 않는다.
5. **정확한 죄명/유형이 생성 과정에서 단순화된다** — 특수강도로 라우팅/평가됐어도
   답안에는 그냥 "강도"로 나오는 사례. 어느 단계(라우팅 미선택 / predicate 미충족 /
   생성 단순화 / 표시명·법적명 미분리)에서 없어졌는지 로그 확인 필요.
6. **생성 모델이 라우팅 안 된 쟁점을 임의로 추가한다** — 예: 살인 고의를 불필요하게
   검토하면서 정작 필요한 특수강도·결과적 가중범 미수는 빠뜨림.
7. **불확정 사실을 조건부 분기로 유지하지 못한다** — 의료과실 정도가 불명확하면 통상
   과실/중대한 과오 두 경우로 나눠 각각의 객관적 귀속 결론을 내야 하는데, 지금은 생성
   모델이 하나로 임의 확정해버린다.

**핵심 진단(사용자 문구)**: "IDPR은 죄명 수준의 결론을 계산하지만 장문 답안에서 필요한
법리 수준의 쟁점 구조를 충분히 계산하지 못한다." "Judge를 고쳐도 이 구조적 누락은
그대로 남는다" — 즉 이건 judge 교체로 해결되는 문제가 아니라 라우팅/상징 출력 설계
자체를 손봐야 하는 문제.

### 다음 세션 작업 순서 (사용자 지시)

1. **결함 위치를 로그로 구분** — ✅ **완료 (이번 세션)**, 상세는 아래
   "1단계 결과: r10/r14 결함 위치 특정" 절 참고. 4가지 범주 모두 실제 사례로 확인됐고,
   지시에 없던 **5번째 범주(술어평가 오류)**가 가장 파급력 큰 결함으로 드러났다.
2. **라우팅 출력 확장**: `selected_issues` 외에 `required_subissues`,
   `conclusion_sensitive_facts`, `unresolved_branch_points`, `alternative_legal_routes`,
   `required_conclusions` 반환. 단, 모든 불확실성을 분기하면 precision이 떨어지므로
   **사실 판단에 따라 적용 법리나 최종 죄책이 달라지는 지점만** 분기.
3. **symbolic 출력 확장**: 결론뿐 아니라 `activated_rules`, `required_issues`,
   `required_doctrines`, `alternative_branches`도 반환해 생성 단계로 넘김.
   `required_issues`는 문장 순서를 통제하지 않고 최종 생성에서 반드시 다뤄야 할
   체크리스트로만 쓴다 — 자유 장문 생성이라는 현재 설계는 유지.
4. **judge 재설계 + 백본 교체**: 위 judge 절 참고. 코드/trace가 실제로 평가 입력에
   들어가는지 확인 → 프롬프트/기준 재설계 → `anthropic/claude-sonnet-4-6`로 전량
   재평가. 우리 파이프라인 외 baseline들은 새 judge로 미리 돌려둘 수 있다.
5. 이 네 가지가 끝나면 **원래 궤도(장물죄 146장 원장 적재)로 복귀**.

### 1단계 결과: r10/r14 결함 위치 특정 (이번 세션, job 219779 산출물 대조)

`experiments/results/rule_ir_native_lean_batch_219779/{kcl_criminal_r10_p1_q1_ga,
kcl_criminal_r14_p1_q2}/`의 `01_issue_selection.json` / `01_rejected_issues.json` /
`02_assessment_*.json` / `03_native_report.json` / `04_write_prompt.md` / `05_answer.md`를
골드 rubric(`data/inventory/kcl_criminal_v1_draft.jsonl`)과 대조. 두 사례 모두 4가지
범주가 각각 실제로 발생했고, 지시에 없던 5번째 범주가 새로 드러났다.

**r10_p1_q1_ga (성범죄 사례, 甲의 죄책):**

| 쟁점 | 범주 | 내용 |
|---|---|---|
| issue_1 (강제추행 간접정범) | **라우팅 오류** | `indecent_assault`가 활성 레지스트리에 있는데도 router가 `extortion`(공갈)을 골라 role 계약 위반으로 `contract_degraded`. 골드 rubric 36개 중 결론 항목(#11, #36)에 들어가는 죄명이 답안에서 통째로 사라지고, 대신 rubric에 없는 "성폭력처벌법상 촬영물등이용협박"을 답안이 즉석 창작. |
| issue_3 (강도로 오분류) | **라우팅 오류(중복)** | 강간을 위한 폭행·감금 사실을 `robbery` 유닛에 태워 art333~343 술어 ~100개를 돌렸으나 전부 근거 없이 `not_satisfied`라 계약 위반으로 폐기 — 18k 토큰 낭비, 원래 필요한 인과관계 분석에 갈 자원을 소모. |
| issue_6 (중지미수) | **규칙베이스 범위 오류** | 형법 제25·26조 장애미수/중지미수/불능미수라는 총론 법리가 어떤 유닛에도 술어로 존재하지 않음. router가 "unsupported"라고 한 것 자체는 맞다 — 정말 없다. |
| issue_2 (주거침입) | **술어평가 오류 (신규 범주)** | 술어 ~90개가 거의 전부 "unknown". "아파트 공용현관·엘리베이터에 따라 들어간 것 자체가 판례상 기수"라는, 사실관계에 그대로 적힌 카드(`apartment_common_areas`)조차 "확인되지 않음" 처리 → `dwelling_intrusion_undetermined`. |
| issue_4→issue_5 (강간치상) | **상징/구조 오류** | `sexual_offense_attempt`가 `shared_module_missing_dependency`로 강등(의존하는 shared module이 별도 이슈로 라우팅되지 않아 미공급) → issue_5가 `prerequisite_not_established`로 연쇄 붕괴. 사건에서 두 번째로 중요한 결론(강간치상)이 통째로 상징 근거 없이 생성됨. |
| 종합 | **생성 단계** | 상징 결과가 사실상 전무하니 writer가 헤지형 자유 서술로 전체를 메움("성립 가능성이 높으나…"). rubric 필수 죄명 3개 중 2개(강제추행 간접정범, 체포죄)가 최종 답안에서 빠짐. |

**r14_p1_q2 (사기·뇌물·횡령 사례, 乙·丙의 죄책):**

| 쟁점 | 범주 | 내용 |
|---|---|---|
| issue_2, issue_3 (증뢰물전달죄) | **라우팅 오류** | `third_party_bribery`가 router에게 주어진 것과 동일한 closed enum 안에 활성 상태로 존재하는데도 router가 두 쟁점 다 `unit_id: "unsupported"`로 출력. 乙·丙 각각의 핵심 결론(제3자뇌물교부죄/취득죄, rubric #6~14)이 통째로 즉석 창작으로 대체("일반 뇌물공여죄 공동정범"— 오답). |
| issue_1 (사기) | **술어평가 오류** | `fraud_intent_no_disposition_inducement_intent` 등 고의 관련 술어가 전부 "unknown". 대차 용도를 구체적으로 속인 사실 자체가 고의를 강하게 추단시키는 전형적 사안인데도, 평가 모델이 "명시적 진술이 없으면 unknown" 식으로 처리 → `symbolic_conclusion: not_established` (골드 결론과 정반대). |
| issue_1 답안 반영 | **생성 단계 (가장 심각)** | `04_write_prompt.md`가 "확정 결론: 불성립 … 이 결론은 검증된 규칙 추론의 산물이므로 반드시 그대로 따른다"고 강제. 결과 `05_answer.md`는 자체 논증으로 "사기죄의 구성요건을 충족한다고 봄이 타당하다"고 쓴 바로 다음 문장에서 "확정 판정에 따라 사기죄 불성립"으로 뒤집는 **자기모순 답안**을 그대로 출력. |
| issue_4 (횡령) | **규칙베이스 범위 오류 (조용한 오답)** | `embezzlement` 유닛에 불법원인급여물 항변(대법원 판례, 뇌물 자금처럼 불법 목적 급여물은 위탁물 보호대상이 아니라 횡령죄 객체가 아니라는 법리) 카드가 없음 → `symbolic_conclusion: established`(골드는 불성립). 답안도 아무 모순 없이 확신을 갖고 "횡령죄 성립"이라 서술 — r14 사기 사례처럼 표면에 흠이 드러나지 않아 rubric 대조 없이는 못 잡아낸다. |

**교차 사례 종합 — 5번째 범주가 최우선 레버리지 지점**

지시받은 4범주(라우팅/규칙베이스/상징규칙/생성)가 전부 실제로, 그것도 사례 하나당
여러 번 겹쳐서 확인됐다. 그런데 그 위에 **범주 5: 술어평가(predicate assessment)
오류**가 새로 드러났다 — 고의·인과관계·예견가능성처럼 사실관계에서 **추론**해야
하는 요건을 평가 모델이 "명시적 문장으로 서술돼 있지 않으면 unknown" 식으로
과도하게 문자적으로 처리한다. 변호사시험 사실관계는 애초에 내심의 의사를 직접
서술하지 않고 행위로만 암시하는 서술 관행이므로, 이 결함은 이 두 사례에 국한되지
않고 **레지스트리 전역에서 "established" 판정을 광범위하게 억누르고 있을 가능성이
높다** — 라우팅과 규칙베이스를 아무리 고쳐도 평가 단계가 이 모양이면 상징 결론은
계속 `undetermined`/`not_established`로 새고, 결과적으로 4번(생성 단계)의
"반드시 그대로 따른다" 강제 지시가 잘못된 결론을 확신에 찬 답안으로 그대로
찍어낸다. 즉 **평가 단계(범주 5) → 생성 단계 강제 지시(범주 4)**의 조합이 지금
가장 위험한 경로로 보인다: 잘못된 결론이 (a) 자기모순으로 드러나거나(사기 사례,
그나마 육안 검출 가능) (b) 아무 흔적 없이 확신에 찬 오답으로 나간다(횡령 사례,
rubric 없이는 검출 불가).

**다음 결정 필요**: 2~4단계(라우팅/symbolic 출력 확장, judge 재설계)로 바로
넘어가기 전에, 이 술어평가 문제와 "반드시 그대로 따른다" 강제 지시부터 먼저
겨냥할지 사용자 판단 필요 — 활성 프롬프트 변경은 승인 게이트 대상.

**사용자 결정 (같은 세션): 술어평가 오류(범주 5) + 생성 강제 지시(범주 4)부터
먼저 고친다.** 이유: 라우팅 오류는 coverage를 깎지만, 술어평가 오류는 카드를
정확히 골랐어도 결론 자체를 뒤집는다. 사용자가 제시한 순서: 1) predicate
assessment 4-state화 2) symbolic outcome에 신뢰 상태(verified/provisional/
unsupported/invalid) 부여 3) 생성 강제 지시와 충돌 처리 4) 라우팅/하위쟁점 확장
5) rule-base 범위 보완 6) judge 재설계 7) 전체 재실험. 1~3단계를 이번 세션에
구현 완료 — 아래 절 참고. 4~7단계는 미착수.

### 1~3단계 구현 완료 (이번 세션) — 술어평가 4-state + 신뢰 상태 + 충돌 검출

**변경 범위**: `src/idpr/rulegen/native_host.py`, `scripts/run_rule_ir_native_lean.py`,
`prompts/rule_ir_native_predicate_assess.md`, `prompts/rule_ir_native_write.md`,
`scripts/audit_rule_ir_native_prompts.py`, 관련 테스트. **아직 실제 API로 실행한
적 없음 — 스키마/유닛 테스트만 통과 확인.** 1차 구현 후 사용자가 3가지 구멍을
지적해 같은 세션에서 수정 완료(아래 "1차 검수 반영" 참고). 전체 스위트:
**637 passed**(신규 테스트 5건), 실패 11건은 전부 이전부터 문서화된 기존 결함
(재산죄 golden `card_conflict_blocks` 10건 + `test_section_writer_cannot_supply_host_conclusion`)
그대로 — 이번 변경이 만든 회귀 없음. `python scripts/audit_rule_ir_native_prompts.py`
도 pass.

1. **predicate assessment 4-state화** (`native_host.py`
   `ASSESSMENT_STATUSES`/`normalize_assessment_status`) — 스키마 enum을
   `satisfied/not_satisfied/unknown`에서
   `explicitly_supported/inferentially_supported/contradicted/genuinely_unresolved`로
   교체(구조화 출력 자체를 이 네 값으로 강제, validator도 이 네 값 기준으로
   재작성). Scallop 실행 직전 `normalize_assessment_status()`로 `explicitly_supported`·
   `inferentially_supported`→`satisfied`, `contradicted`→`not_satisfied`,
   `genuinely_unresolved`→`unknown`으로 정규화 — symbolic 실행 로직 자체는
   무변경. `inferentially_supported`에는 `inference_rationale`(추론 근거 1~2문장)을
   JSON Schema `if/then`으로 조건부 필수화 — 명시적 사실 없이 결론을 낸 이유를
   사후 검수할 수 있게. `prompts/rule_ir_native_predicate_assess.md`에 "내심적·
   규범적 요건의 추론" 절을 신설해 사기 고의 예시를 넣고, "문장으로 서술돼 있지
   않다"는 사실 자체는 `genuinely_unresolved`의 근거가 아니라고 명시.
2. **symbolic outcome 신뢰 상태** (`native_host.py` `classify_symbolic_trust`) —
   `execute_native_case`가 만드는 `conclusion_directives`/`skipped_directives`
   각 항목에 `trust_status` 필드 부여:
   - `verified`: 실행 완료 + established/not_established **그리고** 그 결론이
     실제로 발화(fire)한 Scallop 증명 경로(`proof_dag.proof_tree`를
     `_collect_critical_predicates()`로 추적)에 포함된 술어 중
     `genuinely_unresolved`가 하나도 없음. `inferentially_supported`가
     섞여 있다는 사실 자체는 verified를 막지 않는다 — 정규화하면 explicit과
     동등하기 때문. 이 조건이 1차 구현에서 빠져 있었다: unit 하나에 보통
     수십~백여 개 술어가 있고 그중 사실관계와 무관해 정당하게
     `genuinely_unresolved`로 남는 것이 항상 있는데, "unit 전체에 unresolved가
     하나라도 있으면 provisional"로 잡으면 verified가 사실상 한 번도 안 뜨고,
     반대로 아무 검사도 안 하면 특정 카드가 "반증되지 않으면 인정"식으로
     설계돼 있을 때 unresolved 술어가 조용히 통과해 established로 확정되는
     반대 방향 오류가 생긴다 — 증명 경로 추적으로 이 둘을 다 피한다.
   - `provisional`: 실행 완료했지만 undetermined/conflict/no_derived_outcome,
     또는 established/not_established가 떴어도 위 조건을 못 만족(발화 경로에
     unresolved 술어 포함, 또는 증명 경로 자체를 못 찾음 — 후자는 방어적으로
     "확인 불가 = provisional" 처리)
   - `unsupported`: 해당 unit의 RuleIR 자체가 없음(`predicate_ir_missing`)
   - `invalid`: contract_degraded/shared_module_missing_dependency/
     prerequisite_not_established/symbolic_execution_failed — 시스템 내부 실패,
     법리적 신호 없음
3. **생성 강제 지시 분기 + 자기모순 검출** (`run_rule_ir_native_lean.py`
   `_render_verdict_brief`/`_render_directive_block`, `prompts/rule_ir_native_write.md`) —
   기존에는 실행된 결론이면 established든 undetermined든 전부 "확정 결론 …
   반드시 그대로 따른다"로 동일하게 강제했다(이게 r14 사기/횡령 사례의 핵심
   원인). 이제 4단으로 분기: `verified`만 "확정 결론"으로 절대 준수, `provisional`은
   "잠정 결론"으로 제시하되 근거가 있으면 대안 논증 허용, `unsupported`/`invalid`는
   각각 "규칙베이스 범위 밖"/"규칙 추론이 완료되지 못한 쟁점"으로 분리해 아무 힌트
   없이 자율 논증(둘 다 자율 논증이지만 이후 결함 분석에서 "커버리지 부족"과
   "파이프라인 버그"를 구분할 수 있게 라벨은 남긴다).
   자기모순 검출: writer가 답안 맨 끝에 `<!--VERDICT_MANIFEST\nissue_id: established
   또는 not_established\n-->` 트레일러를 출력하도록 지시(`native_host.py`
   `parse_verdict_manifest`/`strip_verdict_manifest`). `check_verdict_consistency()`가
   이 트레일러를 `verified` 쟁점의 `symbolic_conclusion`과 대조 — 불일치하면
   `06_verdict_consistency.json`에 **기록만 하고 재생성/중단은 하지 않는다**
   (사용자 확인: 이번 최소 실험은 원 답안 보존·트레일러 대조·불일치 기록·재시도
   없음으로 고정 — repair를 넣으려면 API 호출 횟수·추론 예산·답안 선택 절차·
   baseline 비교 조건이 다 바뀌므로 별도 후처리 단계나 ablation으로 분리할 것).
   트레일러는 `05_answer_raw.md`에만 남고 `05_answer.md`(채점/사람이 읽는 파일)
   에서는 제거된다. `generation_contract.model_may_override_symbolic_conclusion:
   False` 필드는 원래부터 있었지만 아무도 검사하지 않던 죽은 계약이었다 —
   이 체크가 그걸 실제로 강제하는 첫 코드.

### 1차 구현 검수 반영 (같은 세션) — 사용자가 지적한 3가지 구멍

1. **스키마/validator가 실제로 4-state를 강제하는지** — 프롬프트만 바꾸고
   스키마를 안 바꾸면 출력이 자체 validation에서 탈락한다는 지적. 확인 결과
   스키마(`predicate_assessment_schema`의 `ASSESSMENT_STATUSES` enum)는 처음부터
   같이 바꿔뒀었고, 이번에 `inferentially_supported`→`inference_rationale`
   조건부 필수(`if/then`)를 추가로 넣었다.
2. **raw/normalized 상태를 둘 다 보존** — `assessment_evidence`의 필드를
   `raw_status`(원래 4-state 그대로)와 `normalized_status`(Scallop용 3-state)
   두 개로 분리(이전엔 `status`+`assessment_basis`로 이름이 불명확했다).
   재실행 결과가 개선됐을 때 "새 사실 때문"과 "추론 허용 때문"을 구분할 수 있게
   됐다. `_render_verdict_brief`의 인정/부정/미확인 요건 목록도
   `normalized_status` 기준으로 수정.
3. **verified 기준 강화** — 위 2번 "symbolic outcome 신뢰 상태" 절 참고. Scallop
   proof tree를 실제로 역추적해 검증하는 `_collect_critical_predicates`/
   `_is_cleanly_derived`를 추가(경험적으로 rape 골든 시나리오의 proof_tree
   구조를 직접 실행해 확인한 뒤 작성 — established 관계에서 `assess_*` 술어
   리프까지의 경로가 실제로 추적 가능함을 확인).

**미해결/다음 세션 판단 필요**:
- `inferentially_supported` 허용이 precision을 깎을 위험(과다추론) — r10/r14뿐
  아니라 "고의가 명확히 추론되는 사례"와 "고의가 실제로 불명확해 unresolved가
  맞는 사례" 음성 대조까지 최소 4~6건으로 소규모 재실행해 확인. 답안 점수보다
  먼저 볼 것: predicate별 old_status→new_raw_status, new_raw_status→
  normalized_status, symbolic_conclusion 변화, trust_status, 생성 결론,
  VERDICT_MANIFEST 일치 여부.
- 자기모순 발견 시 정책(현재는 기록만) — 이번 최소 실험 범위에서는 이대로 유지,
  repair를 넣을지는 별도 결정.
- 4단계(라우팅/하위쟁점 확장) 이후는 미착수.

### 이번 세션 완료 — predassess 스모크 검증 통과 (job 219900 재제출부터 시작해 완결)

**job 219900은 실패했다 (코드 문제 아님).** vLLM 엔진 초기화 중 `IDPR_HF_HOME`을
안 넘긴 채 제출해 `HF_HOME`이 홈 디렉터리 기본 경로(비어있음/불완전)로 새고,
거기서 실시간 재다운로드를 시도하다 `RuntimeError: Internal error: Internal
Writer Error: Background writer channel closed`로 끊겨 죽었다. 진짜 캐시는
`/data5/jaehoonjeong/.cache/huggingface`(49G, 완전함, `~/.bashrc`의 `HF_HOME`이
가리키는 곳)에 있었다 — `scripts/slurm/_env.sh`는 `IDPR_HF_HOME`이 명시적으로
안 오면 기본 폴백 없이 그냥 넘어가므로, 이후 이 모델을 쓰는 모든 sbatch 제출은
`IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface`를 반드시 명시해야 한다.

재제출(219978) 이후 실제 API 실행으로만 드러나는 버그를 2개 발견·수정했다
(둘 다 지난 세션의 1~3단계 구현이 "스키마/유닛 테스트만 통과, 실제 API로는
미실행"이라고 남겨뒀던 그 구멍):

1. **스키마 `if`/`then`은 vLLM guidance backend가 미지원** (job 219978, 6/6
   전부 `Grammar error: Unimplemented keys: ["if","then"]`로 즉시 실패) —
   `inference_rationale` 조건부 필수화를 JSON Schema `if`/`then`으로 구현한
   게 생성 요청 자체를 막았다. `native_host.py`의 `predicate_assessment_schema()`
   에서 `if`/`then` 제거, `inference_rationale`을 무조건 `required`로(단
   `minLength` 없이, 빈 문자열 허용) 바꿔 grammar가 키 존재는 강제하되 내용은
   강제하지 않게 하고, "`inferentially_supported`면 비어있으면 안 된다"는
   조건은 `validate_predicate_assessment()`의 Python 쪽 상태별 체크로 옮겼다.
2. **`genuinely_unresolved`의 `missing_facts` 누락이 쟁점 전체를 폐기** (job
   219989 재제출 직후, r14_p1_q2 사기 88개 술어 중 44개가 `missing_facts`를
   비운 채 `genuinely_unresolved`로만 남아 쟁점 전체가 `predicate_assessment_invalid`
   로 강등). 비운 술어 대부분이 이 사건과 무관한 경계/예외 법리(광고 기망,
   공익목적 예외, 삼각사기 판례 등) — 판정 자체는 맞고 `missing_facts` 생성
   계약만 깨진 사례(사용자 분류상 B 유형)로 확인. `prompts/rule_ir_native_predicate_assess.md`
   에 "이 predicate가 사건과 무관해 보이더라도 `missing_facts`를 비우지 말고
   어떤 사실이 추가로 확인돼야 하는지 적으라"는 한 줄만 추가. 단독 재실행
   (job 219993, `r14_p1_q2` 1건)으로 검증: 44개 전부 `missing_facts` 채워짐,
   `issue_1`(사기)이 더 이상 강등되지 않고 `not_established`+`verified`로
   정상 실행. 구조적 완화(`assessment_validity` 필드 분리)는 이 한 줄로
   불필요해졌다 — 도입 안 함.

6-case 배치(job 219992, gemma 백본)는 최종 **6/6 성공**. 종료조건 확인:
**추론 가능한 술어는 `inferentially_supported`로 판정되고, 실제 불확정
술어는 쟁점을 폐기하지 않은 채 provisional/verified 경로로 정상 전달된다.**
(**목표를 `established`+`verified`로 두지 않았다** — 사용자 지시: 그렇게
튜닝하면 과다추론으로 precision을 깎는다. `r14_p1_q2` 사기의 최종 결론은
여전히 `not_established`이고, 그 결론 자체가 골드와 맞는지는 이번 스모크
범위 밖.)

**사고 기록 — RUN_DIR 재사용 함정**: 같은 `IDPR_RUN_DIR`로 여러 job을 연달아
제출하면 실패한 이전 job이 남긴 `01_rejected_issues.json` 등이 안 지워진 채
남아 최신 성공 결과와 섞여 보인다. 이번 세션에서 `r10_p2_q1`의 사기 쟁점이
실제로는(fresh `03_native_report.json` 기준) 정상 실행됐는데, 이전 job의
잔존 `01_rejected_issues.json`(mtime이 새 job 시작 시각보다 이전) 때문에
한 번 강등된 것으로 오판할 뻔했다. 다음에 이 디렉터리를 다시 볼 때 파일
mtime을 job 시작 시각과 대조할 것.

**사용자 결정: 26문항 전체 재실행은 생략(필수 아님).** 원래 계획된 4번
(전체 재실행·219779 비교)은 건너뛰고 바로 아래 4~6단계로 진행한다.

**다음 세션 시작점: 4단계 — 라우팅 출력 확장.** 이 문서 맨 위 "다음 세션 작업
순서" 목록의 2번(`required_subissues`/`conclusion_sensitive_facts`/
`unresolved_branch_points`/`alternative_legal_routes`/`required_conclusions`
반환) 참고. 1~3단계(술어평가 4-state, trust_status, 강제지시 분기)는 API
실행까지 검증 완료됐으니 여기서부터.

### 4단계 구현 완료 (이번 세션) — 라우팅 출력 확장, API 스모크는 GPU 대기 중

`closed_issue_selection_schema()`(`src/idpr/rulegen/native_host.py`)에 `issues`
외 다섯 개 배열을 전부 **무조건 필수**로 추가했다: `required_subissues`,
`conclusion_sensitive_facts`, `unresolved_branch_points`,
`alternative_legal_routes`, `required_issue_labels`(원래 이름
`required_conclusions`였으나 검수에서 지적받아 개명 — 아래 참고). 값은 매번
빈 배열이라도 키 자체는 항상 나와야 한다 — `inference_rationale`에 썼던 것과
같은 "무조건 필수 키 + 내용은 Python 쪽에서 조건부 검사" 패턴이다.

**1차 구현 후 사용자 검수에서 세 가지 지적을 받아 설치 전에 수정**:

1. **관계는 `unit_id`가 아니라 `issue_id`로만 참조한다.** 1차안은
   `subissue_unit_id`/`branch_unit_ids`/`alternative_unit_id`처럼 unit_id로
   연결했는데, 같은 unit_id가 서로 다른 행위자·행위에 여러 번 등장할 수 있고
   `unit_id=unsupported`인 issue도 한 사건에 여러 개 있을 수 있어 unit_id로는
   어느 issue를 가리키는지 특정할 수 없다는 지적. `subissue_issue_id`/
   `alternative_issue_id`로 개명하고, 호스트가 참조된 issue의 `unit_id`를
   조회하는 방식으로 바꿨다.
2. **`unresolved_branch_points`는 서로 다른 unit 두 개를 요구하면 안 된다.**
   같은 unit(예: 특수강도치사) 안에서도 사실 판단(예: 의료과실이 통상적
   과실인지 독립적 중대 과오인지)에 따라 결론이 갈릴 수 있기 때문. 구조를
   `branch_unit_ids`(unit 2개 이상)에서 `affects_issue_ids` + `branch_conditions`
   (갈릴 수 있는 사실 판단을 서술한 문장, 2개 이상)로 교체 — 새 unit을
   요구하지 않고 이미 라우팅된 같은 issue의 조건부 분기를 서술한다.
3. **`required_conclusions`라는 이름이 "라우팅 단계는 결론을 내리지 않는다"는
   앞부분 규칙과 충돌한다.** 실제 의미는 결론이 아니라 정확한 법적 명칭 보존이므로
   `required_issue_labels`로 개명.

호스트에 `assess_routing_completeness()`(신규 함수)를 추가해 이 다섯 배열이
실제로 `issues`에 반영됐는지 대조한다 — 라우터가 하위쟁점/대안을 "이름만
적고" `issues`에 별도 항목으로 안 넣으면 `gap_type`이 붙은 기록으로 남는다
(`required_subissue_missing`/`alternative_route_missing`/
`dangling_issue_reference`). 케이스를 실패시키거나 자동으로 채워 넣지 않는다
— 기존 `01_rejected_issues.json`과 같은 "강등·기록만, 조용히 패치하지 않는다"
원칙. `scripts/run_rule_ir_native_lean.py`가 이 결과를 `01b_routing_completeness.json`
으로 저장하고, `required_issue_labels`는 writer에게 넘기는 죄명 라벨을
정확한 명칭으로 덮어쓰며(`특수강도`가 `강도`로 뭉개지는 것 방지), 나머지
네 배열은 새 "하위쟁점/분기/대안/정확한 죄명" 체크리스트 절로 렌더링돼
`04_write_prompt.md`에 추가된다. **두 번째 라우팅 호출은 없다** — M5 3콜
아키텍처([[m5-standard-architecture]] 참고)를 유지하기 위해 분기의 양쪽
unit 모두 같은 라우팅 호출 한 번 안에서 `issues`에 등재돼야 한다는 전제다.

프롬프트 승인 게이트에 따라 스키마·코드를 먼저 구현하고 전문을 채팅으로
제시해 위 세 가지 수정 지시를 받은 뒤에만 `prompts/rule_ir_native_issue_select.md`
에 새 절("하위 쟁점·분기·대안·정확한 죄명")을 설치했다. `scripts/audit_rule_ir_native_prompts.py`
에 다섯 필드가 schema의 `required`와 `properties`에 모두 있는지 검사하는
로직과 새 계약 문구(다섯 필드명 + precision guard 문구 "적용되는 법리나")를
추가 — 감사 통과 확인(`pass: 3 stages, 0 errors`). 신규 유닛테스트 5건
(`tests/test_rule_ir_native_host.py`) 통과, 기존 두 파일 타깃 재실행에서
회귀 없음 확인. **아직 실제 API/vLLM 실행으로는 검증 못함** — job 220007
(r10_p1_q1_ga + r14_p1_q2, `scripts/slurm/run_rule_ir_native_lean_batch.sh`,
로컬 vLLM gemma, `IDPR_HF_HOME` 명시)을 제출했으나 GPU 자원 부족으로
`PD (Resources)` 대기 중 — 완료되면 다섯 필드가 실제 guided-decoding 출력에서
스키마대로 채워지는지, `assess_routing_completeness`가 실제 gap을 잡아내는지
확인 필요. 전체 pytest 스위트도 이번 리네임 반영 후 재실행 중(직전 확인 시점
기준 642 passed / 11 failed, 전부 문서화된 기존 결함 — 리네임 이후 재확인은
다음 세션 또는 잡 완료 후 결과 참고).

**다음 세션(또는 잡 220007 완료 시) 할 일**: (1) job 220007 결과로 다섯 배열이
실제로 채워지는지, precision guard(모든 불확실성이 아니라 결론이 갈리는
지점만)가 지켜지는지, `01b_routing_completeness.json`의 `gaps`가 r10/r14에서
실제로 뭘 잡아내는지 확인. (2) 문제없으면 5단계(rule-base 범위 보완)로 진행.

### job 220007 스모크 결과 (같은 세션, GPU 대기 후 완료) — 구조는 작동, 정확도는 별개 문제

2건 모두 성공(`cases=2 failed=0`). 확인된 것:

- **precision guard가 실제로 지켜졌다.** 두 사례 모두 다섯 배열을 과다하게
  채우지 않았다(r10: `conclusion_sensitive_facts` 1건 + `alternative_legal_routes`
  1건만, 나머지 0건; r14: 다섯 배열 전부 0건). 우려했던 "모든 불확실성을
  분기"하는 과다분기는 관찰되지 않았다.
- **`unresolved_branch_points`/`unsupported` role_candidates 규칙은 정상
  준수**됐다 — r10의 `unit_id=unsupported` issue(`issue_6`, "강도치상")가
  `role_candidates: {}`, `depends_on_issue_ids: []`로 정확히 비어 있다.
- **`assess_routing_completeness`가 실제 gap을 잡아냈다.** r10에서
  `conclusion_sensitive_facts`가 `affects_issue_ids: ["issue_4"]`를 참조했는데,
  issue_4(강간미수)는 `source_quote`가 원문에 없어(`quote_not_grounded`)
  per-issue 강등으로 이미 `issues`에서 빠진 상태였다. 라우터가 참조를
  갱신하지 않아 생긴 진짜 dangling reference를 정확히 잡아 `01b_routing_completeness.json`
  의 `gaps`에 기록했다 — 설계 의도대로 동작.
- **`alternative_legal_routes`가 실제 법리 신호를 실어 날랐다.** r10에서
  "강도(issue_3) 폭행과 상해의 인과관계가 단절되면 강도치상이 아니라 강도+상해
  경합범"이라는 대안을 issue_5(상해)로 정확히 연결했고, writer가 이걸 받아
  최종 답안에서 "재물 탈취 의사가 없었으므로 강도치상 불성립 → 강간치상 검토"로
  실제로 활용해 이전 세션 진단(자기모순·헤지형 서술)보다 더 정확한 결론에
  도달했다(`05_answer.md`).
- **라우팅 정확도 자체는 이번 단계로 고쳐지지 않는다 — 예상된 결과.** r14에서
  `third_party_bribery`(증뢰물전달죄)가 활성 레지스트리에 있는데도 issue_2/
  issue_3이 여전히 `unit_id: unsupported`로 나왔다(문서화된 기존 결함 재현).
  다섯 배열 중 어느 것도 이 결함을 스스로 감지하거나 우회하지 못했다 —
  `required_subissues`/`alternative_legal_routes`는 라우터가 최소한 issue_id로
  "이게 필요하다"는 걸 알고 있을 때만 신호를 만든다. 애초에 유닛을 잘못
  판단(활성 유닛을 unsupported로 오분류)하는 문제는 구조 확장이 아니라
  라우터 자체의 유닛 판별 정확도 문제이므로 별도로 다뤄야 한다. writer는
  기존과 같이 "뇌물공여의 전달자"라는 개념을 즉석 창작했다.

**결론**: 4단계 구조(스키마·검증·writer 배선)는 설계대로 작동하고 실제로
답안 품질에 기여하는 사례(r10)를 만들어냈다. 다만 이 구조는 "라우터가 이미
알고 있는 관계"를 명시화하는 것이지 "라우터가 애초에 틀리게 고른 유닛"을
고치지 못한다 — r14의 유닛 누락은 5단계(rule-base 범위 보완)가 아니라 라우팅
정확도 자체의 문제로, 별도 이슈로 남겨둔다. **정정(같은 세션 후속 조사)**: 아래
절에서 밝혀지듯 실제 누락 대상은 `third_party_bribery`가 아니라 `bribe_giving`
이었다 — 사용자 지시로 다시 판 결과 확인.

### 라우팅 정확도 — third_party_bribery 오진단 정정 + 진단 필드 도입 + 회귀 배치 (같은 세션, 사용자 지시)

**사용자 결정: rule-base 범위 보완(5단계)보다 라우팅 정확도(활성 unit을
`unsupported`로 잘못 보내는 문제)를 먼저 고친다.** 이유: 카드를 더 추가해도
라우터가 그 카드를 고르지 않으면 그 사례는 계속 실행되지 않는다 — "진짜
미지원"과 "지원되는데 라우터가 놓침"을 섞으면 논문에서 서로 다른 실패
유형을 하나로 잘못 계상하게 된다.

**오진단 발견**: job 220007에서 `third_party_bribery`가 라우팅 정확도 문제의
사례로 지목됐으나, 등록 카드(`assess_art130_*`)를 직접 열어보니 전부 "공무원이
직무에 관하여 제3자에게 뇌물을 공여하게 하는" 제130조 제3자뇌물제공죄만
다룬다 — 사인(乙)이 사인(丙)에게 공무원(P1)에게 전달할 돈을 맡긴 r14의
사실관계와는 아예 다른 범죄다. 실제로 정확히 맞는 유닛은 `bribe_giving`
(제133조) — `assess_art133_sec1_2_*` 카드 세트가 증뢰물전달죄(제133조 제2항)
요건(교부·인식·독립된 제3자·완성시점 등)을 전부 담고 있고, role_predicate에
`intermediary_id`(전달자 역할)까지 이미 있다. 라우터가 이 유닛도 놓쳤다 — 즉
진짜 라우팅 누락은 있었지만 대상이 바뀐다.

**진단 필드 추가** (`native_host.py`): 각 issue에 `closest_allowed_unit_ids`
(최종 선택 전 비교한 후보, 최대 3개, `unsupported`가 아닐 때는 반드시 빈 배열)
`unsupported_reason`(선택 이유, `unsupported`일 때만 채움) 두 필드를
스키마에 무조건 필수로 추가하고, `validate_closed_issue_selection`이 양방향
계약(unsupported면 이유 필수, 아니면 두 필드 다 비어 있어야 함)을 강제한다.
호스트의 symbolic execution·writer 입력·평가에는 이 두 필드를 전혀 쓰지
않는다 — 순수 진단 trace. `diagnose_unsupported_issues()`가 이 trace로
"라우터가 실제 후보를 이름 붙이고도 거부함(`likely_routing_miss`)" 여부를
계산해 `01c_unsupported_diagnostics.json`으로 남긴다.

**catalog에 `legal_labels` 추가**: `closed_unit_catalog()`가 각 unit의
`role_definition`(예: `bribe_giving`="증뢰자 또는 전달자, 이익, 상대 공무원,
전달 제3자의 역할 tuple")이 죄명 자체(증뢰물전달죄)를 전혀 언급하지 않는다는
사실을 확인 — 이게 라우터가 이름으로 매칭 못 하는 근본 원인 중 하나로
보인다. 확인된 두 유닛(`bribe_giving`, `third_party_bribery`)에만 검증된
법률명을 채워 넣었다 — 36개 유닛 전체를 추측으로 채우지 않는다.

**프롬프트 개정**: `rule_ir_native_issue_select.md`에 "unsupported 판단
절차와 진단 근거" 절 신설 — (1) `allowed_units` 전부를 `role_definition`·
`legal_labels`와 사실관계 대조 (2) 죄명이 문자 그대로 안 적혀 있어도 행위·
대상·상대방 구조가 부합하면 선택 (3) 대조를 마친 뒤에도 안 맞으면
`unsupported` — 라는 3단계 절차와 위 두 진단 필드의 채움 규칙을 명시. 감사
스크립트(`audit_rule_ir_native_prompts.py`)에 계약 문구 검사와 5개 확장
배열의 schema `required`/`properties` 존재 검사를 추가, 통과 확인. 전체
스위트 재확인: **645 passed, 11 failed**(전부 기존 문서화된 결함, 회귀 없음).

**회귀 배치 결과 (job 220070, 6사례: r10_p1_q1_ga·r11_p1_q1·r12_p1_q1·
r13_p1_q1·r14_p1_q1·r14_p1_q2, `scripts/summarize_routing_regression.py`)**:

- **자동 지표(`unsupported_false_positive_rate` 등)는 신뢰할 수 없다.** 새
  프롬프트가 "unsupported를 고르면 후보를 반드시 적으라"고 지시하므로 모델이
  거의 항상 후보를 채운다 — `closest_allowed_unit_ids` 비어있지 않음 = 실제
  라우팅 누락이 아니다. 강도치상/강도상해(결합범 unit 자체가 없음), 살인교사·
  공모관계(레지스트리에 `declared_not_compiled`로 이미 문서화된 진짜 공백)도
  전부 후보를 채운 채 정당하게 `unsupported`로 남았다. 12건 중 9건을
  `likely_routing_miss=True`로 잘못 표시했다 — 이 숫자 자체를 논문 지표로 쓰면
  안 된다.
- **손으로 읽었을 때는 지표보다 훨씬 값진 것이 나왔다.** 두 건이 진짜 라우팅
  누락으로 확인됐고, **둘 다 같은 실패 모양**을 보였다: 모델이
  `closest_allowed_unit_ids`에 정확히 맞는 unit을 스스로 짚어내고도, 참여형태·
  분류 문제를 이유로 그 unit을 통째로 버렸다.
  - r12_p1_q1 "사문서위조": 후보 `['private_document_forgery']`(정확히 맞음,
    art231/232), 이유 "명확히 매칭되지 않음"(근거 없는 회피).
  - r14_p1_q2 issue_2(뇌물공여): 후보에 `bribe_giving`이 **이번에 처음
    등장**(legal_labels 추가가 recall 자체는 실제로 개선시켰다는 증거) — 그런데도
    "乙의 행위가 丙을 도구로 한 간접정범인지... 구체적 죄명 분류를 위해
    unsupported로 처리함"이라며 회피. `known_target_recall`에서 여전히
    `bribe_giving`이 `issues`에 없음(found: false) — 최종 선택 단계는 아직
    못 고쳤다.
- **결론**: 이번 세션 수정은 recall 단계(후보를 찾아내는 것)는 개선했지만
  decision 단계(찾은 후보를 실제로 쓰는 것)는 아직이다. 다음 수정은 더
  구체적이어야 한다 — "참여형태·가담정도(간접정범/공동정범 등)가 불확실하다는
  이유로 이미 부합하는 base unit 선택을 보류하지 마라. base unit은 선택하고
  그 불확실성은 `required_subissues`나 writer 체크리스트로 넘겨라"는 지시를
  추가해야 할 것으로 보인다. **미착수 — 다음 세션 시작점.**
- 산출물: `experiments/results/rule_ir_native_lean_routing_regression/`(6사례
  전체), `.cache/routing_expansion_smoke/regression_summary.json`(위 지표·
  사례별 원본 trace).

### decision 단계 프롬프트 수정 시도 — 2회 실패, 롤백 (다음 세션, 사용자 지시)

위 절 마지막에 미착수로 남겨둔 "참여형태 불확실성을 이유로 이미 부합하는 base unit
선택을 보류하지 마라"는 수정을 시도했으나, **두 번 다 실패해 롤백했다.**

1. **1차 시도(negative carve-out, commit `7b7656f`)**: "참여형태(직접정범/간접정범/
   공동정범 등)의 확정 여부는 unsupported 사유가 아니다"라는 4번째 절차를 추가.
   job 220071(같은 6사례 재실행, `rule_ir_native_lean_routing_regression_v2`)로 검증:
   `bribe_giving`/`private_document_forgery` 둘 다 여전히 `found: false`(전혀 무변화,
   unsupported 총계도 12→13으로 사실상 동일). `unsupported_reason` 원문 대조 결과, 모델이
   금지된 표현("간접정범인지... 구체적 죄명 분류를 위해")만 피하고 **똑같은 결론을 다른
   말("행위 유형을 가장 정확히 특정할 수 있는 단독 unit이 부족함")로 재포장**했다.
2. **2차 시도(affirmative rule + 회피 사유 금지 목록, commit `e913783`)**: "구조 부합
   판정을 내린 후보는 반드시 선택한다"는 단정 규칙으로 교체하고, 그때까지 관찰된 회피
   표현 4종(참여형태 불확실, 단독 unit 아님, 결합 구조 특정 필요, 완전 포괄 못함)을
   명시적으로 금지. job 220074(`rule_ir_native_lean_routing_regression_v3`)로 재검증:
   **역시 무변화** — 두 known-target 다시 `found: false`, `unsupported_reason`이 세
   번째 다른 표현("전달을 부탁한 주체로서의 성격이 강하고... 결합된 구조를 표현할
   적절한 unit이 부족함")으로 또 우회.
3. **사용자 결정: 강하게 강제해도 안 되면 롤백하고 다음 단계로.** `git revert -n
   e913783 7b7656f`로 두 커밋을 되돌려 `prompts/rule_ir_native_issue_select.md`/
   `scripts/audit_rule_ir_native_prompts.py`를 job 220070 시점 상태로 복원(감사·테스트
   재확인 완료, 회귀 없음). 산출물은 보존:
   `experiments/results/rule_ir_native_lean_routing_regression_v2/`,
   `..._v3/`, `.cache/routing_expansion_smoke/regression_summary_v{2,3}.json`.

**결론(중요, 다음 세션에 이 문제를 다시 열 때 참고)**: 이 특정 회피 패턴(구조가
부합한다고 스스로 서술해놓고도 완벽한 사실관계 일치를 요구하며 unsupported로
후퇴)은 **프롬프트 문구 수정만으로는 안 뚫린다** — 세 번(220070/220071/220074)
연속으로 같은 두 사례에서 매번 다른 표현으로 같은 결론을 냈다. 이건 26B 로컬
모델의 특정 문구 회피가 아니라 더 근본적인 결정 휴리스틱으로 보인다. 다음에
다시 시도한다면 프롬프트 문구가 아니라 **구조적 게이트**(예: `closest_allowed_unit_ids`가
비어있지 않은 채 `unit_id=unsupported`가 나오면 그 자체를 계약 위반으로 강등하거나,
1차 host-side 재검증 콜을 추가)를 고려할 것 — M5 3콜 원칙 이탈이므로 별도 승인 필요.

**다음 세션 시작점: 5단계 — rule-base 범위 보완.** job 220070에서 이미 확인된 진짜
공백(강도치상/강도상해 결합범 unit 부재, 살인교사·공모관계 `declared_not_compiled`)이
1순위 후보.

**이번 세션에 새로 만들었지만 아직 안 쓰는 것**: SKI-ML 게이트웨이 경유 Sonnet
클라이언트(`src/idpr/neural/skiml_litellm_client.py`,
`scripts/run_rule_ir_native_lean_sonnet.py`,
`scripts/slurm/run_rule_ir_native_lean_sonnet_smoke.sh`). 연결은
`anthropic/claude-sonnet-4-6` 모델 문자열로 확인 완료(`custom_llm_provider="openai"`
로 호출해야 인증됨 — litellm이 "anthropic/" 접두어만 보고 자체 판단하면
Anthropic 네이티브 인증 경로로 새서 401). **judge 백본 교체(6단계) 전까지는
쓰지 않는다** — IDPR 생성 파이프라인에는 절대 쓰지 않는다.

### judge 재설계 6단계 + 61개 전체 재평가 착수 (같은 세션 후속, 2026-08-07)

**judge 프롬프트/하니스 변경 (전부 커밋 완료)**:
- `prompts/phase3_kcl_pointwise_judge.md` Consistency 절에 순환논증 방지 규칙
  추가(`c4d4e69`) — 형식논리(Z3/FOL/Scallop 등)가 결론과 같은 명제를 전제로
  먼저 넣고 그 전제 성립을 결론 검증인 것처럼 재서술하면 4점 불가. FOL
  r10_p1_q1_ga 답안(dev case)으로 Sonnet 스모크 테스트: consistency
  85.96(Gemini 구버전 평균) 상당의 사례가 새 judge+백본에서는 0.5/4점대로
  나오고, 위반 사유가 실제 Z3 `s.add(...)` 코드를 인용해 대조하기 시작함.
- Coverage에 `partially_met`(0.5) 추가(`bacd211`) — schema, 프롬프트,
  `rubric.py`(`Verdict` "P", `apply_safeguards`/`score_answer`를 0/0.5/1
  float로 일반화, 근거인용·조문게이트 세이프가드는 O와 동일 적용),
  `phase3_judge.py`. sp_qwen 원본은 순수 이진이라 포팅 대상이 아니라 IDPR
  신규 확장.
- `scripts/run_phase3_llm_judge.py`에 `--backend {gemini,sonnet}` 추가(`7537d68`,
  `e70c744`) — sonnet은 기존 범용 `LLMGateway`(SKI-ML/LiteLLM,
  `custom_llm_provider="openai"`)를 그대로 재사용, 새 클라이언트 없음.
  `LLMGateway.transport` 클래스 속성 추가로 "이미 채점됨" 재사용 판정이
  백본별로 정확히 갈림(Gemini 결과가 Sonnet 전환 시 자동으로 재채점 대상이
  됨). 스모크(FOL×r10) 실제 API로 end-to-end 검증 완료, `partially_met`가
  실제 채점에서 살아있게 쓰임을 확인.

**5단계 스코프 조정(`913a404`)**: 살인교사·공모관계(총칙 공범)가 shared
module 설계를 요구하는 큰 작업임이 드러나 9월 프로젝트로 이관 — 사용자
결정. 절차법도 마찬가지로 이번 스코프 아님(`data/rulegen/procedure/`엔
스코프 견적만 있고 카드 코퍼스 없음, 착수 전 상태 확인함). 8/11 스코프에는
손대지 않는다 — 기존 설계(`unit_id=unsupported` → writer 자율 논증)로 계속
처리.

**재평가 대상 확정: 26개도 sealed-59도 아니라 61개 전체.** 사용자 결정
순서: 처음엔 26개(실체법 전용 curated set, job 219779) 제안 → sealed-59로
돌리면 26 중 24개는 자동 커버된다는 지적 → **아예 61개(sealed-59 + dev
case 2개) 전체를 풀기로 최종 결정**. dev case를 이 재평가에 포함하는 것도
이번 세션 명시적 사용자 결정 — 평소의 "디버깅만 dev case, 채점은 sealed"
구분과 다르게, 이번 61개 전체 평가는 예외로 취급.

**진행 중인 job 2개(2026-08-07 제출)**:
1. **job 220075** (`scripts/slurm/run_phase3_llm_judge_sonnet.sh`) — 기존
   baseline 7개(idpr_nsn 제외 — 기존 산출물이 59개뿐이라 61개 계약을 못
   채움) 산출물을 새 judge 프롬프트 + `anthropic/claude-sonnet-4-6`로
   재채점. `--reasoning-effort low --max-tokens 16384`(terra/sol 기존
   비용통제 관행 그대로 적용 — 사용자가 토큰비용 절감 요청). 출력:
   `experiments/results/phase3_judge_sonnet/`.
2. **job 220076** (`scripts/slurm/run_rule_ir_native_lean_batch.sh`,
   `IDPR_CASE_LIST=.cache/rule_ir_native_lean_61/case_list.txt`) — IDPR
   자체 답안을 현재 코드 버전(4단계 라우팅 확장까지 반영, decision-avoidance
   버그는 미해결 채로)으로 61개 전체 재생성. 완료 후 결과 경로는
   `IDPR_RUN_DIR=experiments/results/rule_ir_native_lean_61_<제출일>`.

**220076 완료 후 남은 작업(다음 세션 또는 job 완료 후)**: idpr_nsn만 별도로
`run_phase3_llm_judge_sonnet.sh`와 같은 설정(backend=sonnet, 61개, 새
프롬프트)으로 채점 — 새로 생성된 61개 답안을 baseline judge 산출물과 합쳐야
전체 8-method 비교표가 완성된다. 이 답안을 `data/eval/phase3_method_outputs.json`의
`idpr_nsn` 경로에 연결하거나 별도 methods manifest로 채점할지 결정 필요.

**사용자 방침(진행 중 확인)**: 기존 baseline 산출물 중 일부는 파이프라인
오류로 답안이 잘려서 일부만 남아있는 게 있음 — 이건 그대로 두고 판정
결과에서 자연스럽게 페널티로 반영되게 둔다. 별도로 고치거나 제외하지 않음.

### 재평가 완료 — 결과, 방법론 결함 발견·정정, writer 프롬프트 개선 (같은 세션, 2026-08-07)

**job 4개 전부 완료**:
- job 220076(IDPR 61개 재생성) — 61/61 성공.
- job 220075→220077(온도 버그로 220075는 427/427 전멸, 원인·수정은 아래
  "온도 버그" 절)→220223(재시도) — baseline 7개, 최종 424/427(99.3%).
- job 220224(IDPR 신규 답안 `idpr_nsn_lean_61` 채점) — 59/61(96.7%).
  `data/eval/phase3_method_outputs.json`에 `idpr_nsn`(구, 보존)과 별도로
  `idpr_nsn_lean_61`(신) 등록. baseline과 같은 `--out`에 동시에 안 쓰도록
  `experiments/results/phase3_judge_sonnet_idpr/`로 출력 분리.

**온도 버그(수정 완료, `3757333`)**: job 220075가 427/427 전부
`BadRequestError`로 실패 — `--reasoning-effort low`를 켰는데 Anthropic은
extended thinking 켜진 상태에서 `temperature`가 1이 아니면 거부한다. 스크립트가
`--temperature 0.0` 기본값을 항상 같이 보내던 게 원인. `reasoning_effort`가
설정되면 sonnet 백본에서는 temperature를 아예 안 보내도록 수정. **스모크
테스트가 이 조합(`--reasoning-effort` 켠 상태)을 커버 안 하고 있다가 실전
배치에서 처음 걸림** — 앞으로 sbatch 제출 직전에 CLI 인자를 바꿨다면 그
정확한 조합으로 다시 스모크할 것.

**방법론 결함 발견·정정 — 61개 그대로 쓰면 안 됐다.** 61개 중
23~36개(37~59%, 절차법 키워드 밀도 기준)가 **형사소송법/증거법/영장·구속·
증거개시 등 절차법 문제**였다. IDPR 프롬프트는 애초에 "절차법 쟁점은 범위
밖, 이슈 자체를 안 만든다"고 명시돼 있는데 baseline 7개는 이런 제약이
없어 그냥 아는 대로 답을 쓴다 — 그러니 61개 그대로 채점하면 IDPR이
구조적으로 손해 보는 불공정 비교가 된다(실제로 IDPR이 8개 중 5위로 나왔던
게 이 때문). `kcl_criminal_r10_p2_q5`(항소심 조치), `r11_p2_q5`(증거개시
신청) 등 5개 사례가 IDPR coverage 0.0(전 rubric `not_met`)으로 나온 게
결정적 단서였음.

**정정된 비교 — 실체법만 걸러서(26개 job219779 curated, 28개
`proc_kw` 정규식 밀도<=10% 필터, 둘 다 확인 결과 사실상 순수 실체법) 재계산**:

| method | 28개 cov | 28개 prec | 26개 cov | 26개 prec |
|---|---|---|---|---|
| chain_of_thought | 0.212 | 0.510 | 0.211 | 0.522 |
| **idpr_nsn_lean_61** | 0.168 (2위) | **0.524 (1위)** | 0.179 (2위) | **0.560 (1위)** |
| acal | 0.161 | 0.443 | 0.168 | 0.456 |
| legal_chain_reasoner | 0.157 | 0.455 | 0.166 | 0.476 |
| vanilla_zero_shot | 0.139 | 0.449 | 0.151 | 0.478 |
| standard_rag | 0.138 | 0.476 | 0.149 | 0.503 |
| leprec | 0.131 | 0.412 | 0.140 | 0.435 |
| fol_autoformalizer_solver | 0.094 | 0.371 | 0.101 | 0.394 |

**IDPR은 실체법 기준 precision 8개 중 1위, coverage 2위.** 61개 그대로
봤을 때의 "중위권" 인상은 절차법 스코프 불일치가 만든 착시였다 — 파이프라인
자체가 나빠진 게 아니었다.

**남은 진짜 격차 — chain_of_thought 대비 coverage(0.168 vs 0.212)**.
`r12_p1_q1` 사례를 직접 대조(IDPR coverage 0.385/precision **1.0** vs CoT
coverage 0.538/precision 0.636)해서 원인을 찾음: IDPR이 놓친 rubric
항목들은 오답이 아니라 **기수시기, 반복행위의 죄수(포괄일죄 vs 실체적
경합), 간접정범 등 참여형태의 정확한 법률용어 명시** 같은 부수 쟁점이었다
— 성립여부 자체(핵심 쟁점)는 이미 다 맞혔는데(그래서 precision 1.0) 그
주변부를 안 썼을 뿐. CoT는 이 부수 쟁점까지 넓게 쓰지만 정확도는 떨어짐
(precision 0.636) — 진짜 트레이드오프지 CoT가 rubric을 게임한 게 아님을
`r10_p1_q2`(CoT도 IDPR 초기 버전과 똑같이 형법 263조를 놓쳐 오답, Sonnet이
정확히 잡아냄: coverage 0.038)로 교차 확인함.

**대응(커밋 완료, `3ad3eef`)**: `prompts/rule_ir_native_write.md` 4번
"논거의 밀도" 규칙에 기수시기·죄수(포괄일죄 여부)·참여형태 정확한 법률용어
명시를 추가 지시. 낮은 리스크(이미 precision 1위라 정확도 훼손 위험 적음).
**아직 실제 배치로 효과 검증 안 함 — 감사·pytest만 통과.** 다음 세션에서
급하면 dev case 2개로 소규모 재확인 가능.

**참고 — 61개 전체 채점 관행에 대한 정정**: 위 sealed-59 오염 정책의
"이번 61개 평가는 예외"라는 결정 자체는 유효하지만, 앞으로 진짜 최종
숫자(논문에 쓸 숫자)는 **26개 또는 28개(실체법 전용) 기준으로 잡아야 한다**
— 61개/59개는 IDPR이 애초에 시도하지 않는 절차법을 섞어서 방법론적으로
깨끗하지 않다. 다음 재평가부터는 처음부터 실체법 전용 서브셋으로 돌릴 것.

### 향후 과제 (9월말 타겟, 지금 착수 안 함 — 사용자 결정 2026-08-07)

26개 unsupported 43건 원인 분해(위 표): 라우팅 회피 53%(다음 세션 대상) >
**형총 공백 42%** > 각칙 카드 공백 5%.

- **형총 카드 재설계.** 사용자 확인: "구조가 문제"라는 지적이 맞다 — 단순
  카드 이식이 아니라 구성요건/위법성/책임 단계별 판단이 가능하도록 카드
  자체를 재구조화해서 적재해야 한다(계층 구분 여부는 미정). shared module
  아키텍처 문제(위 5단계 A등급 절 참고)와 맞물려 있다. **사용자가 직접 설계를
  더 고민한 뒤 별도로 가져올 예정** — 이번 세션에서는 방향 확인만, 착수는
  안 함.
- **절차법.** 지금 26/28개(실체법 전용) 채점 스코프에는 영향이 없다 — 순수
  future work, **9월말 타겟으로 전체 스코프(수사지원 등 장기목표) 확장을
  대비하는 사전 작업**이라는 성격. 지금 당장 할 필요 없음, 카드 코퍼스도
  아직 없음(위 "5단계 스코프 조정" 절 참고: `data/rulegen/procedure/`엔
  스코프 견적만 존재).

두 작업 모두 **지금 착수하지 않는다** — 형총은 사용자가 설계를 정리해서
가져올 때, 절차법은 9월 스코프 확장 논의가 실제로 시작될 때 재개.

---

## 이 세션에 반영된 것 (커밋 대상, 미완료 항목은 아래 "장물죄" 절 참고)

### 쟁점 단위 강등 — 단일 결함이 사건 전체를 폐기하던 4곳 수정

이전에는 계약 위반 하나가 케이스 전체를 크래시시켰다. 전부 "그 쟁점만
`contract_degraded`/`symbolic_execution_failed`로 강등하고 나머지는 계속 실행"으로
바꿨다 (`src/idpr/rulegen/native_host.py`, `scripts/run_rule_ir_native_lean.py`):

1. 쟁점 선택 후 재검증(`selected_predicate_requests`)이 전량 기각된 케이스에서
   기본 `min_items=1`로 재검증해 크래시 — `min_items` 파라미터화.
2. predicate assessment 계약(인용문/누락사실) 위반 — try/except로 감싸
   `01_rejected_issues.json`에 `degraded_reason: predicate_assessment_invalid`로 기록.
3. Scallop scenario fact 검증 실패(`ScallopFactValidationError`, 예: `distinct_entities`가
   행위자 튜플 밖의 엔티티를 참조) — `symbolic_execution_failed` 상태로 강등.
4. `shared_module` 역할 유닛이 의존성 없이 선택된 경우 `raise NativeHostError` —
   `shared_module_missing_dependency` 상태로 강등.

각각 회귀 테스트 추가(`tests/test_rule_ir_native_host.py`,
`tests/test_rule_ir_native_lean_runner.py`). sbatch 219774(25/26) → 219779(26/26) 두 번의
전량 재실행으로 검증.

### track-coverage gate — 빈 track이 공유 요건만으로 성립 판정 나던 결함 선제 차단

`scripts/build_property_rule_ir.py`: track별 positive component가 하나도 없는 track이
공유 컴포넌트만으로 `established`를 도출할 수 있던 건전성 구멍. 이제 그런 track은
`core.outcome.track.{name}` / `elements_satisfied.{name}` 규칙 자체를 안 만들어
`track_pred`를 도달 불가능하게 하고, `coverage_gaps`에
`track_positive_path_missing: {name}`을 기록한다. 로버리 4개 track으로 회귀 테스트 작성
(`tests/test_property_rule_ir.py::test_track_without_positive_components_never_derives_established`).

### 검수 004 J-06 반영 — LEVEL과 role의 L6 결합 제거

기존에는 "역할 등록이 필요한가"를 `LEVEL == BAR_LEVEL("L6")`로 판단해서, LEVEL(요건
단계)과 role(카드 기능)이 부적절하게 묶여 있었다. `build_property_rule_ir.py`의
`negative_kind()`를 role 조회가 레벨과 무관하게 이뤄지도록 재작성 — 카드가
`card_roles.json`에 어떤 값으로든 있으면 그 역할을 쓰고, negative/exception 극성 카드가
등록 없이 들어오면 `SystemExit`. `build_rule_ir_card_roles.py`도 `LEVEL==L6` 필터 대신
"negative/exception 극성 전량"을 필수 등록 대상으로 바꿨다. `evidentiary_standard`,
`procedural_outcome` 역할 신설, `outcome_subtype` 정합성 검증(`POST_OUTCOME_SUBTYPES`
7종 대조) 추가.

정합성 검증: 로버리 재조립 후 `robbery_rule_ir_candidate.json` / `property_robbery_v1_candidate.scl`
해시가 이전과 바이트 단위로 동일 — 이번 리팩터가 기존 산출물을 바꾸지 않았음을 확인.

**사고 기록**: `build_rule_ir_card_roles.py` 실행이 그 스크립트의 불완전한 스키마로
`card_roles.json` 전체를 재생성하면서, 우발적으로 로버리 카드 하나의 `outcome_subtype`
필드를 지울 뻔했다 (테스트 `KeyError`로 검출, 원인 규명 후 `OUTCOME_SUBTYPES` 딕셔너리로
재생성 가능한 방식으로 복구, 해시 대조로 무결성 확인). 앞으로 데이터 재생성 스크립트를
돌리기 전에 그 스크립트의 소스 스키마가 현재 파일의 모든 필드를 커버하는지 먼저 확인할 것.

전체 스위트: **632 passed, 11 failed** — 실패 11건은 전부 기존 문서화된 결함(재산죄
golden `card_conflict_blocks` 10건 + `test_section_writer_cannot_supply_host_conclusion`).
이번 변경이 만든 회귀 없음.

## 장물죄 146장 적재 — 검수 004 접수 완료, 반영은 판단 문제 해결 후 재개

`docs/reviews/review_batch_004_stolen_property_level_design.md`에 사용자가 J-01~J-06
판정을 직접 기입 완료:

| 항목 | 판정 |
|---|---|
| J-01 (빈 track + coverage gap 감사) | O |
| J-02 (shared 레벨 분해) | X — 재분해 필요 (주체 component, 장물성/출처 분리, intent/timing AND 아닌 OR로 잘못 묶임 등) |
| J-03 (분리 원칙) | 수정 후 O — `acquisition.knowledge_at_delivery`, `custody.knowledge` 둘 다 3장으로 분리 |
| J-04 (`transport.consent_and_delivery`) | X — 3장 분리 필수 (부분 컴파일 방식 불승인) |
| J-05 (LEVEL 코드) | X — `L0a` 류 단순 코드 대신 `SP_` 네임스페이스 시맨틱 코드 |
| J-06 (LEVEL/role 결합) | 구조 수정 필요 — **이 세션에서 반영 완료** (위 절 참고) |

지시된 작업 순서: 1. LEVEL-role L6 결합 제거 → 2. component-scoped bar/variant 상태 기능
확인 → 3. 카드 분리 → 4. coverage gap 등록 → 5. namespaced LEVEL 확정 → 6. 원장 적재 →
7. SCL 생성 → 8. track별 golden test.

**진행 상황**: 1, 2 완료(위 절). 3~8은 미착수 — 지금 판단할 문제(judge/라우팅)를 먼저
정리한 뒤 재개.

카드 분리 대상 최종 13장 (기존 배치 002의 11장 + 배치 004가 추가한 2장):
```
sec3_2.foreign_offense, sec3_3.transport.knowledge_midway, sec3_3.custody.knowledge,
good_faith_acquisition, accession_processing, breach_of_trust_bribe,
resale_fraud_nonabsorption, acquisition.food_consumption,
transfer.knowledge_and_subsequent_transfer, brokering.completion_doctrines,
acquisition_brokering_relationship,
acquisition.knowledge_at_delivery (신규, J-03),
transport.consent_and_delivery (신규, J-04)
```

신규 coverage gap 3종 (배치 004가 추가 지적, 기존 카드로 못 채움):
```
missing_card_slot: 일반 주체 eligibility component (instigator_aider_subject 단독으로는 부족/부적절)
missing_card_slot: 운반 track 고의시점 component (acquisition/custody와 분리 필요)
missing_card_slot: "장물임을 실제로 인식했다"는 사실 component (intent_and_knowledge의 추상적 고의범 서술과 별개)
```

146장 역할 재분류 대조 결과(검수 002 E절 대조, 이번 세션에 수행): 이름으로 명시 판정된
건 124장, E-04 일괄방침("학설군 일괄 미채택")으로 커버되는 건 19장(개별 재검토 불요),
어디에도 안 걸리는 진짜 미검토 카드는 2장 — `sec3_2.copied_media`,
`sec3_2.victim_consent_gift_inheritance` (둘 다 polarity=exception, exception-polarity
게이트로 자동 격리되므로 잠정 배정해도 결론엔 영향 없음, 다만 최종 역할은 사용자 확인
필요).

데이터 이슈 발견(미해결): 카드 ID `stolen_property_sec3_2.stolen_property_used_to_defraud`에
`stolen_property_` 접두사가 중복 포함돼 있다(146장 중 유일 사례, 추출 파이프라인
아티팩트로 추정). 원장 적재 시 이 ID를 그대로 쓸지 정정할지 결정 필요 — 임의로
바꾸지 않고 다음 세션에서 확인.

## 이전부터 열려 있는 결함 (미착수)

- **F-01 shared module `post_offense_absorption`** — 장물보관 후 임의처분 불가벌적
  사후행위. 배치 002 F-01에 bridge relation 8종·출력 4종 확정. 호스트가 쟁점별 유닛을
  독립 실행하고 유닛 간 사실을 안 주고받는 구조라 bridge 경로 신설 필요.
- **사기 룰베이스 재작업(검수 003 G절, 판정 완료·미반영)** — `BAR_CARD_IDS` 23장 중
  미수/기수 혼동 3장, boundary 재분류 3장, `assessment_standard` 재작성 등.
- **`polarity=exception` 88장 극성 복구(검수 003 I)** — 현재 `enforce: false` + quarantine.
  처리 순서: 실발화 카드 → bar → boundary → P2 waiver → 도달가능 미발화 → 비활성.
- **Stage 1/2 역할 결박 대조 없음(P0)** — `role_candidates`/`role_values`가 서로 비교되지
  않아 Stage 2가 Stage 1의 행위자·객체 선택을 조용히 바꿀 수 있음.
- **재산죄 golden 10건 실패** — `card_conflict_blocks`, 커밋 `2c4e75e`가 무장 해제.
- **`test_section_writer_cannot_supply_host_conclusion`** — 죽은 경로를 지키는 가드,
  경로를 지울지 가드를 옮길지 결정 필요.
- **25개 P2 RuleIR이 `status=draft`** — 레지스트리 활성화가 승인 원장/해시에 안 묶임.
- **back-parse 검증 없음** — 답안과 derivation 모순 대조 단계 없음.
- **`post_outcome` 191장 `outcome_subtype` 미지정** — coverage gap으로만 노출 중.

## 실행 환경

- 추론 환경: `inv_ass_env`. **sbatch 설정은 건드리지 말고 전례대로만.**
- 원격 API(judge 등) 작업도 **항상 sbatch** — raw 백그라운드 프로세스 금지. 스크래치
  파일은 compute node가 못 보는 세션 `/tmp/...`가 아니라 `/data5/jaehoonjeong/IDPR/.cache/...`
  같은 공유 스토리지에 둘 것 (job 219789가 이 실수로 실패, 219790으로 정정).
- 셸에 conda가 활성화돼 있지 않으면 `IDPR_PYTHON` / `IDPR_VLLM_BIN` / `IDPR_MODEL_SOURCE`를
  명시해 제출해야 한다.
- GPU를 만지는 작업은 길이와 무관하게 항상 sbatch. `nohup` 금지.
- 고정 심볼릭 런타임: `tools/scallop/scli-0.2.4-linux-x86_64`
- 레지스트리 매니페스트: `data/rulegen/rule_ir_registry_manifest.json` (36 유닛)
- 테스트: `python -m pytest` — miniconda **base** 환경 (레포 `.venv`는 빈 껍데기,
  `inv_ass_env`도 아님).

## 검수 문서

| 배치 | 내용 | 상태 |
|---|---|---|
| [001](../reviews/review_batch_001_roles_and_stolen_property.md) | 역할 배치 36건 + 장물죄 4건 | 답변 완료·반영 완료 |
| [002](../reviews/review_batch_002_assessment_standard_and_stolen_property.md) | `assessment_standard` 설계 + 장물죄 146장 | 답변 완료·C/D절 반영, E/F절 미반영 |
| [003](../reviews/review_batch_003_fraud_bars_and_sweep_findings.md) | 사기 BAR 23장 + 26문항 실행 발견 | 답변 완료·H-03/I 반영, G/H-01 미반영 |
| [004](../reviews/review_batch_004_stolen_property_level_design.md) | 장물죄 track/LEVEL/role 설계 6건 | 답변 완료·1~2단계 반영, 3~8단계 미반영(위 절 참고) |

검수는 카드 단위로 판정하며, **검수 문서는 그 자리에서 답할 수 있어야** 한다 —
재료만 나열하면 안 된다.

이어서 읽을 것: [`DESIGN.md`](DESIGN.md), [`RECOVERY.md`](RECOVERY.md),
[`../../project_init.md`](../../project_init.md). RuleIR 시그니처나 법률적 구성을
바꿀 때는 [`RULEIR_RISKS.md`](RULEIR_RISKS.md).
