# v2.2 production assembly plan

Status: approved 2026-08-10. This is the durable repository record of the
post-Gate① assembly plan; it replaces any reliance on a chat-local task plan.

## Fixed boundaries

- The Gate① canonical sources are `predicate_dictionary_master_v3.md` and
  `predicate_dictionary_ext_art258_v0.md`. Do not create or alter a frozen
  predicate ID or canonical meaning during assembly.
- Evaluation coverage remains **80**. Article 258 is a supporting dependency
  for article 258-2, not an additional evaluation target.
- All A-group predicate/relation reuse questions are closed.
- B-group items are resolved only while assembling the affected statute.
- C-group items require code-path verification. Article 339 D-1/D-2 are
  resolved only immediately before article 339's own assembly.

## Dependency order

```text
ground_facts + legal_elements
  → bundles / primitives / relations / qualifiers
  → doctrines + participation policies + base offenses
  → exported components → derived offenses → completion policies
  → full type-check / compile / runtime audit
```

The registry's YAML file iteration is not this build order: it creates a flat
registry first and type-checks the graph afterwards.

## 핵심 의존성과 피드백 지점 (승인본)

```text
facts + legal elements
  → bundles / primitives / relations / qualifiers
  → doctrines + participation + base offenses
  → exported components → derived offenses → completion policies
  → full type-check / compile / runtime audit
```

피드백을 받기 좋은 지점도 명확히 둔다.

- **단계 1 완료**: 전체 적재 범위와 10조 inventory 불일치 처리 방향 검토
- **단계 2 완료**: 총칙 공통 structure·bundle/doctrine expression·participation HOLD 검토
- **단계 3 완료**: 각칙 base offense slot/reuse 배치 검토
- **단계 4 전후**: B그룹 9건의 조문별 구조 선택 검토
- **단계 5**: C그룹 코드 검증 결과 및 art339 접근법 검토
- **단계 6**: 최종 coverage/정합성 검토

모든 phase 종료 시 해당 YAML diff·type-check/compile 결과·HOLD 변동을 기록해
피드백을 받고, 다음 phase의 조립으로 넘어간다.

단계 1의 Gate① inventory↔production 대응표는 완료했다. 10조 문제는 “누락”인지
“의도적 미채택”인지 근거로만 판정하며, 새 ID를 만들지 않는다. 대응표와 Phase 1
피드백 기록은
[`ASSEMBLY_CROSSWALK.md`](ASSEMBLY_CROSSWALK.md)에 남긴다.

## Execution phases

| Phase | Scope and output | Completion check | Feedback point |
|---|---|---|---|
| 0 | Registry contract and first foundation slice (arts. 9, 11, 12, 16) | Done: 8-axis type check 0 findings; v2 tests pass | Baseline completed |
| 1 | Gate① inventory-to-production crosswalk: every canonical ID, definition kind, owner YAML, source, and downstream consumers | No unmatched production entry or unclassified canonical inventory entry | Review overall scope and the Article 10 discrepancy |
| 2 | General Part shared facts/elements/bundles/doctrines and only the participation structure that is independent of C-33/C-34 | Type-check clean for the assembled subset | **Required Phase 2 review**: General Part structures, every unresolved expression boundary, and the participation HOLD |
| 3 | Special Part base `OffenseDef` assembly, grouped by reusable base families | Each non-HOLD base offense schema-loads and type-checks; affected-statute B/C holds are recorded rather than partially authored | **Required Phase 3 review**: base-offense slot/reuse placement and every concrete affected-statute HOLD |
| 4 | `QualifierDef`, `DerivedOffenseDef`, relations, and `CompletionPolicyDef`; assemble 258 then all four 258-2 branches | Compiler replay equals each derived offense's flattened cache; B-group choice logged at its statute | Review B-group structural choices before/after their affected assembly |
| 5 | C-group code-path verification, then only the validated affected assembly | C-33/C-34 participation finalised only after this verification | Review C-group results and the Article 339 approach |
| 5.1 | Proven architecture gaps only: minimum contract/runtime change, focused regression, then affected assembly | No generic framework; each change is tied to C-33a, C-34, C-151, C-263, or C-339 | **PASS.** Art.339 covers the frozen 333/334/335 robbery-side candidates; Phase 6 may begin on instruction |
| 6 | Whole-registry audit | **PASS:** 293 objects, 8-axis 0 findings, 63/63 offenses compile, `tests/test_v2_*.py` 236 passed, coverage stays 80 | Final coverage/integrity review recorded in `ASSEMBLY_CROSSWALK.md` |

## Participation HOLD rule (approved)

Phase 2 may author shared participation predicates and an otherwise-independent
default policy, but it must **not** finalise any participation mode, constraint,
or attribution behaviour needed to answer either of these C-group cases:

- **C-33**: actor-specific status in co-principal participation and the
  differentiated offense identity in the Article 33 proviso.
- **C-34**: indirect perpetration, whose condition is not the current
  derivative `principal_realization_truth` path.

Keep those entries absent or explicitly marked as authoring HOLD material until
Phase 5's code-path result. Do not let a generic participation policy silently
decide either question.

## Current phase boundary

Phase 1 through Phase 5 are accepted. Phase 5 proved four architecture gaps
and one 339-specific completion gap; it also moved C-33b to Step 7 caller
orchestration. Phase 5.1 has now implemented only those five changes and
assembled the affected C-33a/C-151/339 production objects; C-263 has no new
offense identity and C-34 remains runtime-only by approval. Art.339 is now
assembled separately for the sealed robbery-side candidates 333 (`robbery`),
334 (`special_robbery`), and 335 (`quasi_robbery`); 336 remains a coverage
reference only. The implementation record is in
[`ARCHITECTURE_PLAN.md`](ARCHITECTURE_PLAN.md). **Phase 5.1 and Phase 6 PASS:**
the complete production registry is audited. Further work requires an explicit
new scope and retains the documented Step 7/HOLD boundaries.

## Post-assembly checkpoint — Step 7 COMPLETE

The approved Closure / Probe compiler scope is complete. Mandatory structural
closure is active; a reverse branch found as a probe is only a compilable
candidate, and becomes conditionally active only after later factual survival.
The full result, C-33b caller boundary, Article 263 probe delegation, and the
remaining doctrine/HOLD boundary are recorded in
[`STEP7_PLAN.md`](STEP7_PLAN.md) and `ASSEMBLY_CROSSWALK.md`. Verification is
293 registry objects, eight-axis **0 findings**, **63/63** compiles,
`tests/test_v2_*.py` **252 passed**, and no production source drift. The next
authorized scope is the Step 8 Call 1 pilot.
