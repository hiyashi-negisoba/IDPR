# Current handoff

## Read this first

The active implementation is the lean RuleIR-native path. It selects a unit from a
closed registry, loads every registered commentary predicate, validates raw-case
assessments, executes the unit's committed Scallop program, and lets the model write
only the law/application prose. The host owns the final symbolic conclusion.

```text
case and question
  -> closed unit, issue, and role selection
  -> complete predicate assessment against exact source text
  -> committed RuleIR SCL executed by pinned Scallop
  -> host-owned symbolic conclusion
  -> one model-written law/application section per executed issue
```

Active entry point: `scripts/run_rule_ir_native_lean.py`.

Do not reactivate semantic search, article top-k, generic FactGraph, 245-core projection,
model-written SCL, or model-only fallback in this path. An unavailable unit remains
`predicate_ir_missing`.

## What is genuinely recovered

- The active runner does not import retrieval, FactGraph, or core projection code.
- It executes committed RuleIR SCL through the pinned native Scallop CLI.
- Registered units and query relations are closed by the host registry.
- A selected unit's commentary predicates cannot be omitted by the assessment model.
- The writer cannot supply or override the final symbolic conclusion.
- The current registry contains 36 executable units and 1,652 commentary inputs.

These guarantees do not mean that the full intended architecture is complete.

## Blocking implementation defects

### P0: no case-specific derivation

`run_scenario` invokes `scli --output-all` and reduces public query relations to
non-empty booleans. `execute_native_unit` records the booleans and raw output, but does
not produce tuple lineage, a proof tree, fired RuleIR rule IDs, gated-out evidence, or
standard flags. The static SCL dependency graph exists; the case-specific proof does not.

This violates the S2 `Derivation` contract in `project_init.md` and
`docs/contracts/derivation.schema.json`.

### P0: generation is not derivation-conditioned or semantically verified

The writer receives the conclusion, all predicate evidence, and any established public
relations, but not the rules and tuples that caused the conclusion. For
`not_established`, `undetermined`, and `conflict`, it receives no structured proof of the
cause. Post-generation validation checks Markdown shape only. There is no active
back-parser or `missing` / `contradiction` / `unsupported` comparison against a
derivation.

### P0: property-rule OR/negative asymmetry

Within a property component, multiple positive cards are alternative recognition paths.
However, the builder also treats every positive card outside explicit tracks as
mandatory: an explicitly `not_satisfied` alternative emits `<unit>_not_established` and
blocks the whole offence even when another alternative satisfies the component. A theft
counterexample produced `elements_satisfied=true`, `not_established=true`, and
`established=false` without a conflict. The property builder and its cross-alternative
tests must be corrected before relying on legal outcomes.

### P0: role binding can change between model stages

Stage 1 `role_candidates` and Stage 2 `role_values` are independently schema-validated,
but their values are never compared. Stage 2 can silently change the actor/object tuple
selected by Stage 1.

### P1: incomplete result preservation

- A shared downstream module marked `prerequisite_not_established` is omitted from the
  generation directives and disappears from the final answer.
- An unsupported-only case has no section request, so finalization records `case_id=null`.
- The same complete `--output-all` text is duplicated once per query relation.

### P1: activation and reproducibility gaps

- All 36 canonical RuleIR JSON files still say `status=draft` and
  `legal_review=pending`; the registry audit does not bind executable assets to approved
  ledgers and hashes.
- The existing Derivation schema does not admit current runtime outcomes such as
  `undetermined`, `conflict`, or `no_derived_outcome`.
- The active vLLM client has no request cache even though the original engineering
  contract requires caching.

## Required repair order

1. Define a Derivation v2 contract covering every runtime outcome.
2. Emit a case-specific proof DAG with RuleIR rule IDs and supporting tuples.
3. Feed only the relevant proof, unknown causes, and blockers to the writer.
4. Add back-parse verification and hard-fail contradictions/unsupported claims.
5. Fix property component alternatives versus mandatory negative rules and add
   counterexample tests.
6. Enforce Stage 1/Stage 2 role identity and preserve skipped/unsupported issues.
7. Bind registry activation to reviewed ledgers plus exact RuleIR/SCL hashes.
8. Store raw Scallop output once and add deterministic LLM caching/run metadata.

## Working boundaries

- Inference environment: `inv_ass_env`.
- Pinned symbolic runtime: `tools/scallop/scli-0.2.4-linux-x86_64`.
- Registry manifest: `data/rulegen/rule_ir_registry_manifest.json`.
- Current private origin: `https://github.com/hiyashi-negisoba/IDPR`.
- Historical recovery branch: `recovery/ruleir-native-lean-20260804`.
- Archived incomplete core rewrite: `archive/pre-normalization-core-rewrite-20260804`.

Read next: [`DESIGN.md`](DESIGN.md), [`RECOVERY.md`](RECOVERY.md), and
[`../../project_init.md`](../../project_init.md). Use [`RULEIR_RISKS.md`](RULEIR_RISKS.md)
when changing RuleIR signatures or legal composition.
