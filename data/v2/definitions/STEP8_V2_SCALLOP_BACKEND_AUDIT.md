# Step 8 — v2 Scallop backend audit

Status: **frozen architecture audit; Steps 1–4 are implemented and
parity-validated; Step 5 remains** (2026-08-11).

## Decision and scope

The static compilation path and case-time input path are separate:

```text
DefinitionRegistry
    ↓
Typed Legal IR
    ↓
v2 .scl program
        ↘
          Scallop
        ↗
CaseTruths
    ↓
extensional facts

Scallop
    ↓
typed symbolic result adapter
    ↓
LiabilityResult
    ↓
Call 3 final writer
```

`CaseTruths` is the case-time extensional truth interface. It is not a rival
to Scallop and it is not the final symbolic backend. The legacy RuleIR/card
`card_status` interface is excluded from this path.

## Fixed runtime-key handoff rule

The next Call 2 selected-predicate-assessment contract must fix this boundary:

```text
Call 2 does not create or infer OffenseInstanceKey.

For each assessment request, the orchestration host supplies an already-existing
evaluation instance key.

Call 2 returns only:
    (instance_key, predicate_ref) -> TRUE | FALSE | UNKNOWN

The host alone validates and loads that result into CaseTruths.
```

This is an existing-runtime-key handoff, not a new case-instance binding stage.
It forbids actor/event extraction and model-selected instances. The model may
not write `CaseTruths` directly.

This audit is read-only. It did not run native Scallop, call a model, start a
service, edit the Definition Layer, or implement a compiler.

## Post-audit implementation record

The preceding audit statements describe the pre-implementation gap.  The
approved v2-only backend contracts then closed and locally parity-validated:

1. non-`None` `CanonicalExpr` three-valued lowering;
2. `CompiledOffense` slots and occurrence-preserving relation obligations;
3. completion candidate selection, dispositions, and adjusted Elements; and
4. co-principal attribution/constitutive provenance, derivative obligations,
   and active doctrine stage-effect folds.

The implementation is `runtime/scallop_backend.py`, with focused parity tests
in `test_v2_scallop_backend*.py`.  It is v2-only, preserves `CaseTruths` as
the EDB boundary, and does not use legacy `card_status`.  No model request was
made.  The remaining backend scope is Step 5: connect the existing lowered
surfaces into the full gated stage chain and typed `LiabilityResult` adapter.

## Design-source confirmation

Both v2 proposals name Scallop as the target backend:

- `IDPR_v2.1.0_DESIGN_PROPOSAL.md` describes `Definition Language -> Typed
  Legal IR -> Scallop Program -> Neuro-Symbolic Runtime` and places
  **Scallop compilation** before neural-grounding adapters and writer
  integration in its proposed implementation order.
- `IDPR_v2.2.0_DECISION_RUNTIME_PROPOSAL.md` also names Scallop as target
  backend. Its three-call wording is superseded for Call 2/3 decomposition by
  the Step 8 architecture record, but not for the backend target.

## What is already available

| Surface | Existing implementation | Reusable for v2 backend |
|---|---|---|
| Definition loading and validation | `registry.py`, schema/check modules | Yes; compiler input is already typed and checked. |
| Expression representation | canonical `ref`, `all`, `any`, `not`, `one_of` expressions | Yes; needs a Scallop lowering that preserves three-valued semantics. |
| Derived-offense lowering | Python `compile_offense()` resolves `QUALIFY`/`COMPOSE`, components, and relation bindings | Yes as typed-IR source; no `.scl` emission exists. |
| Case-time truth boundary | `CaseTruths` keyed by `OffenseInstanceKey` and `RuntimeRelationKey` | Yes; this is the canonical extensional input shape. |
| Native Scallop process boundary | `rulebase.scallop.run_program()` validates queries, writes `.scl`, invokes pinned `scli`, and parses output | Yes; reuse only process/serialization discipline. |
| Existing `.scl` compiler | `rulebase.compile_scl.py` | No semantic reuse: it compiles legacy issue/card RuleIR and `card_status`, not v2 definitions. |

## What is Python-only today

There is no Scallop import, `.scl` emitter, or compiled v2 program under
`src/idpr/v2/`. Every v2 legal semantic below is currently executed only in
Python:

| Python surface | Semantics a v2 Scallop compiler must preserve |
|---|---|
| `evaluate.py` | `TRUE/FALSE/UNKNOWN` leaf default and `ALL`/`ANY`/`NOT`/`ONE_OF` truth tables. |
| `relations.py` | Relation obligations keyed by definition occurrence path and case runtime key. |
| `runtime/completion.py` | Symmetric completion-state derivation, suspension, additional requirements, and component-local Article 339 rules. |
| `runtime/participation.py` | Co-principal attribution, constitutive-status exception, and typed derivative participation. |
| `runtime/effects.py` | Stage-specific `DEFEAT`, `MODIFY`, and `EXEMPT` resolution. |
| `runtime/pipeline.py` | Completion -> Elements -> Unlawfulness -> Culpability -> Punishability gates, non-speculative `not_reached`, provenance, and `LiabilityResult`. |
| `runtime/orchestration.py` / `statutory.py` | Caller-selected conditional candidates, Article 263 statutory route, and cross-offense checks. |

The native Scallop executable is present, but no v2 legal program is currently
compiled or executed by it. Existing native-Scallop assets are v1 RuleIR/card
programs and cannot demonstrate v2 backend coverage.

## Backend-connection gap

The exact missing implementation is a v2 compiler/backend adapter with three
separate responsibilities:

```text
loaded checked DefinitionRegistry + compiled v2 IR
-> generated v2 .scl program and queries

validated CaseTruths
-> case/instance/relation extensional Scallop facts

Scallop query/proof output
-> existing typed CompletionResult / StageResult / LiabilityResult provenance
```

This adapter must preserve `OffenseInstanceKey` and `RuntimeRelationKey` as
data. It must not translate LegalElement refs into legacy card ids or let a
neural result write Scallop source syntax.

## Recommended implementation sequence

1. Define a v2-only Scallop backend contract and `.scl` fact vocabulary for
   the existing `CaseTruths` predicate and relation keys. Reuse the native
   runner's validation/escaping mechanics, not legacy card semantics.
2. Lower and test the already-implemented three-valued expression evaluator
   against Scallop for `ref`, `ALL`, `ANY`, `NOT`, and `ONE_OF`.
3. Lower plain/QUALIFY/COMPOSE offense elements and relation obligations,
   preserving occurrence paths.
4. Lower completion state selection and suspension; prove parity with the
   current Python completion tests.
5. Lower stage effects and participation/attribution, then typed derivative
   routes and statutory special paths; prove parity with the Python runtime
   test matrix.
6. Only after the backend accepts `CaseTruths` and returns typed symbolic
   results, finalize the Call 2 selected-predicate assessment schema and its
   host adapter to populate the required existing keys.
7. Design Call 3 final-writer handoff from Scallop proof/result output.

Steps 1-5 are compiler/backend work, not a new legal abstraction. They retain
the existing Definition Layer, runtime identities, and legal semantics as the
reference behavior. The Python runtime is the immediate executable oracle for
parity tests while Scallop backend coverage is built.

## Acceptance criteria for a future backend patch

- no v2 production import or output path uses legacy `card_status` or card ids;
- every emitted Scallop fact is host-validated data, not model-produced code;
- v2 `CaseTruths` predicate and relation identities round-trip without loss;
- each lowered construct has Python-runtime parity tests for TRUE, FALSE, and
  UNKNOWN, including missing-truth behavior;
- completion, stage, participation, and derivative-result provenance remain
  reconstructible; and
- no Call 1/Step 7/Call 2 model run is needed to compile or test the backend.

## Freeze record

This audit is frozen with these decisions:

```text
legacy card_status                 excluded from v2 production
v2 CaseTruths                      canonical EDB boundary
Python runtime                     construct-level parity oracle
v2 DSL -> Scallop compiler         next implementation
Call 2 factual v0                  frozen unchanged
Call 2 predicate assessment        later substage of the same Call 2
Call 3                              final free-form IRAC writer
```

The next work is the v2-only Scallop backend Step 5 contract: full stage-chain
gating and the typed `LiabilityResult` adapter. It remains independent of
model-server availability.
