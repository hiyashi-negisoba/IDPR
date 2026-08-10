# Step 7 — Closure / Probe Compiler plan

Status: **COMPLETE — approved checkpoint 2026-08-10**. The pre-implementation
decisions below are accepted and the source-derived compiler is implemented.
This remains work that follows the Phase 6 whole-registry audit: it does not
author a new predicate, change a canonical meaning, or add legal knowledge
outside the frozen production Definition Layer.

## Fixed scope

```text
INPUT
  frozen Rulebase checkpoint
  + canonical offense seed set

Step 7
  Closure / Probe Compiler

OUTPUT
  mandatory core
  offense probes
  doctrine probes
  completion probes
  participation probes

  each item carries deferred legal evaluations in deferred_refs
```

The **293-object** registry in this directory is the sole legal source of
truth. Step 7 derives graph structure and factual frontiers from that registry;
it must not add a statute-specific activation table, an exception list, a new
predicate, or a manually authored legal rule. The sealed Gate① sources and the
80-article coverage boundary remain unchanged.

## Input and output contract

The first implementation accepts only a loaded `DefinitionRegistry` and a
deduplicated set of canonical `offense.*` or `derived_offense.*` seed refs.
Unknown refs or refs of another kind are contract errors, not candidates for
best-effort interpretation.

Each emitted result item must retain the following source-derived data:

| Field | Meaning |
|---|---|
| `definition_ref` | Registry definition that owns the item |
| `classification` | One of `mandatory_core`, `offense_probe`, `doctrine_probe`, `completion_probe`, or `participation_probe` |
| `source_path` | Ordered registry graph path that derived the item from a seed |
| `ground_fact_frontier` | Occurrence-preserving minimum GroundFact refs that Call 2 may ground for this item |
| `deferred_refs` | Legal-element, relation, doctrine, or other legal evaluation refs left for later stages |

The compiler is deterministic: output order is canonical by ref/path. Frontier
deduplication applies only within the same structural occurrence and source
path; it is never a global GroundFact-ref set.

`deferred_refs` is not an independently emitted output category. It is the
only representation of deferred legal evaluations: each classified item carries
the legal-element, relation, doctrine, or other later-stage refs deferred by
that item's own source-derived structure. This follows the v2.2 `DEFERRED`
state as later Call 3 work, not a separate legal branch.

### Activation vocabulary

- `mandatory_offense_refs` are **active** structural obligations.
- An `offense_probe` merely puts its derived offense in
  `candidate_offense_refs`. Candidate compilation is mechanical and does not
  legally activate the branch.
- Only after later factual evaluation establishes a probe does the caller place
  its ref in `conditionally_active_offense_refs`. Orchestration accepts that
  ref only if it was previously a discovered candidate.

No Step 7 output equates probe discovery or compilation with activation.

## Accepted pre-implementation decisions

### A. Frontier traversal

When expression traversal reaches a `LegalElementDef`, the legal-element ref
itself is emitted to `deferred_refs`. Its existing `grounded_by` GroundFact
refs are emitted to the `ground_fact_frontier`. The compiler does not evaluate
either proposition at this point.

The same rule applies when a `PrimitiveDef` or `ExportedComponentDef` resolves
to a legal element. An exported component is resolved only through the existing
`DefinitionRegistry.resolve_export()` resolver; Step 7 must not reimplement or
hand-author export resolution.

### B. Occurrence preservation

Frontier identity is `(component occurrence, source_path, ground_fact_ref)`,
not `ground_fact_ref` alone. A duplicate may be removed only when all three
values are the same.

```text
(component local_key A, ground_fact.X)
!=
(component local_key B, ground_fact.X)
```

This rule applies equally to nested `COMPOSE` components and to any direct
seed-level occurrence. It preserves the existing local-key invariant rather
than flattening component facts into one global set.

### C. Doctrine scope

`DoctrineDef` gains optional `offense_scope`.

- An absent `offense_scope` means an unrestricted stage-level candidate.
- A present `offense_scope` makes the doctrine a candidate only when that
  offense ref occurs in mandatory structural closure.
- Scope controls candidate eligibility only. It does not assert a doctrine's
  truth, activate its effect, or decide its applicability in the case.

When its frozen condition expression is available, the first production
consumer is `doctrine.relative_cohabiting_family_exemption` scoped to
`offense.harboring_or_escape`. That doctrine is not currently in the
293-object Rulebase: the Phase 5.1 record expressly retains its missing frozen
condition expression as a boundary. Step 7 supplies the generic schema and
scope behavior, but does not invent the absent definition. No
`activation_signature`, `OffenseDef.doctrines`, or manual activation table is
permitted.

### D. Article 263 statutory deeming

`OffenseDef.participation_constraints` gains optional `statutory_deeming`.
The first and only initial opt-in is `offense.injury`, with:

```text
requires = ALL(
  legal_element.concurrent_independent_acts,
  legal_element.same_object_of_result,
  legal_element.causal_origin_unascertained
)
```

`injury_result` is not repeated because the base offense Elements already
requires it. Step 7 emits this structure as a `participation_probe`; after the
probe survives, orchestration invokes the existing dedicated Article 263
runtime path. It never invokes `apply_attribution()`, introduces a new
participation mode, or authors an `offense_ref=263` identity.

### E. C-33b cross-offense derivative route

The caller/orchestration adapter requires no structural edge from principal
offense to target offense. It validates only that the caller-selected principal
offense and target offense are each mandatory-active or conditionally active
after a discovered probe survives, and that each is compiled. It then passes
their distinct refs unchanged to
`resolve_derivative_liability()`.

### F. Narrow typing and root occurrence rules

`DoctrineDef.offense_scope`, when present, must resolve only to an `offense` or
`derived_offense`. The type checker rejects every other ref kind.

A direct seed's frontier uses the existing occurrence-path root (the empty/root
path). Step 7 must not introduce a synthetic root occurrence type merely to
represent an uncomposed seed.

## Execution plan

| Step | Work | Output | Completion check |
|---|---|---|---|
| 7.0 | Freeze the public data contract, the two approved optional schema fields, and source-trace invariants in code and tests. | Step 7 request/result types, schema changes, and this plan. | No input may name a non-offense ref; every emitted item has a source path and occurrence identity, and deferred evaluations occur only in `deferred_refs`. |
| 7.1 | Build the Definition Layer structural graph. | Forward and reverse edges derived from `QUALIFY`, `COMPOSE`, components, relations, completion policies, participation constraints, and the shared participation policy. | No manually maintained offense-family or statute map exists. |
| 7.2 | Restore mandatory structural closure for every seed. | `mandatory_core`. | `QUALIFY` includes its base and qualifier; `COMPOSE` includes every component occurrence and relation; cycles and duplicates are handled deterministically. |
| 7.3 | Discover conditional structural branches and calculate their factual boundary. | `offense_probes`, `completion_probes`, `participation_probes`, and occurrence-preserving per-item frontiers. | Reverse derived-offense edges become probes, not silently mandatory expansion; only GroundFact refs, including a legal element's `grounded_by` refs, enter a Call 2 frontier. |
| 7.4 | Derive General Part candidate probes without inventing applicability metadata. | `doctrine_probes` and their stage/deferred data. | Existing `DoctrineDef.stage`, effect, `requires`, and optional `offense_scope` are preserved; Step 7 does not decide that a doctrine applies. |
| 7.5 | Connect the approved C-33b caller route. | A caller/orchestration adapter for cross-offense derivative evaluation. | The caller-selected principal and target are each mandatory-active or caller-reported conditionally active survivors, are compiled candidates, and retain different `offense_ref` values through `resolve_derivative_liability()`. |
| 7.6 | Run production integration tests and record the checkpoint. | Step 7 test report and handoff update. | Focused Step 7 tests plus the complete v2 suite pass; no sealed-source or unapproved production change occurs (the approved `offense.injury` Article 263 opt-in is the sole exception). |

## Structural derivation rules

### Mandatory core

- A plain `OffenseDef` seed is mandatory together with the structure needed to
  evaluate its compiled slots and relation obligations.
- For `QUALIFY(base, qualifier)`, the derived offense, its `base`, and its
  `qualifier` are mandatory structural dependencies.
- For `COMPOSE(components, relations)`, the derived offense, every component
  occurrence (including its local key), and every relation binding are
  mandatory structural dependencies. Nested derivations are followed
  recursively.
- The compiler preserves component occurrence identity. It never collapses two
  components merely because their global refs match.

### Conditional offense probes

The reverse derivation graph is the only source of neighboring offense
candidates. A derived offense that names a mandatory offense as a `QUALIFY`
base or a `COMPOSE` offense component is emitted as an `offense_probe`; it is
not promoted to mandatory merely because it is adjacent. This preserves the
v2.2 rule that a branch is removed only after a factual impossibility proof.

### Completion and participation probes

- A `CompletionPolicyDef` associated with a mandatory or conditional offense
  contributes its state `when` and `requires` expressions as completion
  probes. State selection remains later runtime work.
- The sole shared `ParticipationPolicyDef` contributes mode-specific `requires`
  expressions and applicable offense constraints as participation probes. An
  opted-in `statutory_deeming` constraint follows the Article 263 rule above.
  Step 7 does not decide actors, modes, or participation facts.

### Doctrine probes

The registry has deliberately no offense-to-doctrine activation mapping. The
first implementation emits every loaded unrestricted `DoctrineDef` as a
stage-labelled doctrine candidate. A doctrine with `offense_scope` is emitted
only when its scoped offense ref appears in mandatory structural closure. The
compiler derives each candidate's frontier from its existing `requires`
expression, never claims that the doctrine applies, and treats `UNKNOWN` as
available rather than prunable.

## GroundFact frontier and deferred evaluations

Step 7 traverses existing expressions without evaluating their legal meaning.

```text
GroundFactDef ref                 → Call 2 factual frontier
LegalElementDef ref               → deferred legal evaluation + its `grounded_by` GroundFact frontier
RelationDef ref                   → deferred legal evaluation
DoctrineDef / effect / stage      → doctrine probe metadata, never a verdict
Completion state selection        → completion probe metadata, never a form decision
Participation mode selection      → participation probe metadata, never an actor decision
```

The frontier is minimal **per emitted branch occurrence**: it contains only
GroundFact refs reachable from that occurrence's existing structural
expression(s), including `grounded_by` refs. It does not add neighboring facts
for relevance, evidentiary convenience, or an unstated legal theory.
Legal-element assessment, relation evaluation, completion resolution,
participation resolution, and stage effects remain deferred to their existing
later layers.

## C-33b caller/orchestration boundary

C-33b is an approved Step 7 item because the core already accepts a realized
principal and a derivative target with distinct offense refs. The Rulebase does
not encode who is a principal, who is an instigator/aider, or which
actor-specific target offense is selected. Step 7 must not invent that missing
case-time fact or turn it into a new Article 33 rule.

The adapter therefore accepts explicit caller-supplied values after actor and
participation grounding:

```text
principal: LiabilityEvaluation       # e.g. offense.homicide
mode: instigator | aider
target: OffenseInstanceKey           # e.g. offense.ancestral_homicide
active doctrines + CaseTruths
```

It validates only that the supplied principal and target are each
mandatory-active or caller-reported conditionally active survivors and are in
the compiled candidate set, and delegates to:

```text
resolve_derivative_liability(
  principal=principal,
  instance=target,
  mode=mode,
)
```

The adapter preserves `principal.instance.offense_ref != target.offense_ref`
when that is what the caller selected. It does not choose either ref, infer an
actor relationship, or modify the participation runtime.

## Test matrix

| Test | Required proof |
|---|---|
| QUALIFY closure | A derived seed includes its base and qualifier with exact source paths. |
| Nested COMPOSE closure | Component occurrences and relation bindings remain distinct and recursively traceable. |
| Reverse branch discovery | A neighboring derived offense is an offense probe, not an unproved mandatory expansion. |
| Frontier partition | Legal-element refs remain deferred while their `grounded_by` GroundFact refs are emitted for Call 2; relations remain deferred. |
| Occurrence preservation and determinism | Repeated refs deduplicate only within the same occurrence/source path; distinct local keys retain separate frontier entries and reordered YAML declarations do not alter canonical order. |
| Completion / participation probes | Existing state and mode requirements are traceable to their owning definitions. |
| Doctrine probes | Stage/effect/requirements are preserved without an applicability assertion; `offense_scope` filters candidates only by mandatory closure. |
| Article 263 probe | `offense.injury` emits the three-leaf statutory-deeming participation probe and its surviving path uses the dedicated runtime without attribution or an offense 263 identity. |
| C-33b route | A caller-selected homicide principal and ancestral-homicide target, each mandatory-active (or, for a probe, explicitly conditionally active after survival) and compiled, reach derivative evaluation without a principal→target graph edge or offense-ref substitution. |
| Regression | `tests/test_v2_*.py` remains green after focused Step 7 tests. |

## Non-goals and stop conditions

- Do not alter the sealed Master or participation runtime merely to make a
  probe convenient. The only planned schema/production changes are the
  approved optional `DoctrineDef.offense_scope` and
  `OffenseDef.participation_constraints.statutory_deeming` fields and their
  stated first consumers.
- Do not infer doctrine activation, actor roles, participation mode, target
  offense, legal-element truth, relation truth, completion state, or liability.
- Do not prune on missing support or `UNKNOWN`; only a later explicit `FALSE`
  may establish impossibility.
- Stop and record a contract gap if the frozen registry lacks a structural edge
  needed for one of the five output classifications. Do not patch the gap with
  a new legal map.

## Acceptance gate

Step 7 is ready to implement only after this plan's contract is accepted. Its
first implementation is complete only when every output is mechanically
traceable to the frozen registry, the C-33b caller route is demonstrated
end-to-end, and all focused plus full v2 regressions pass.

## Step 7 completion checkpoint — approved 2026-08-10

The first implementation now provides `idpr.v2.closure` and the small
`idpr.v2.runtime.orchestration` adapters. The compiler derives all five
classified output collections from registry traversal, retains deferred legal
work exclusively in `ClosureItem.deferred_refs`, uses `resolve_export()` for
exported components, and preserves the root occurrence path `()` for a direct
seed. It also exposes mechanical compilation of the structural candidate set;
candidate compilation never activates a probe.

The approved optional schema fields are loaded and type-checked:
`DoctrineDef.offense_scope` accepts only `offense` or `derived_offense`, and
`OffenseDef.participation_constraints.statutory_deeming.requires` is a normal
existing expression. `offense.injury` is the sole production statutory-deeming
opt-in and has exactly the approved three legal-element leaves. Probe survival
delegates to the existing Article 263 runtime; it does not call attribution or
create an Article 263 offense identity.

The C-33b adapter independently requires the caller-supplied principal and
target refs to be mandatory-active or explicitly conditionally active after
probe survival, then checks that they are compiled candidates and passes their
distinct refs unchanged to `resolve_derivative_liability()`. Its test
demonstrates both the homicide → ancestral-homicide path and that a discovered
probe remains rejected until the caller marks it conditionally active. Focused
Step 7 tests and the complete `tests/test_v2_*.py` suite pass (**252 passed**);
registry audit remains 293 objects, 0 type-check findings, 63/63 compiled
offenses, and no production source drift.

**Retained source boundary:** no production doctrine has yet used
`offense_scope`. The named relative/cohabiting-family consumer remains absent
until a frozen Definition Layer condition expression exists; this checkpoint
does not convert its older HOLD into new legal knowledge.

**Next authorized scope:** Step 8 Call 1 pilot begins from this checkpoint.
