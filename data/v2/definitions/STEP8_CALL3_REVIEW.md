# Step 8 — superseded Call 3 LegalElement assessment review

Status: **superseded by architecture correction** (2026-08-11).

This document previously started an independent "Call 3 LegalElement
assessment" design. That decomposition was incorrect. LegalElement/predicate
assessment is part of **Call 2**, after Step 7 narrows the relevant predicate
set. It must not be built as another numbered neural stage.

The intended architecture is now:

```text
Call 1 neural offense routing
-> Step 7 DSL/compiler narrowing
-> Call 2 neural factual grounding + selected predicate assessment
-> DSL / Scallop symbolic execution
-> Call 3 neural final IRAC writer
```

## What remains frozen

Call 1, its top10 rule, Step 7, the Definition Layer, and Call 2 factual
grounding remain untouched. In particular, frozen Call 2 keeps:

```text
TRUE    -> OPEN
FALSE   -> KEEP
UNKNOWN -> KEEP
```

Neither `FALSE` nor `KEEP` prunes a path. There is no further Call 2 prompt
tuning or pruning-recovery work, and no model execution is authorized by this
supersession record.

## Recovered design material

The following ideas are retained as input to the **Call 2 selected-predicate
assessment** contract, not as a Call 3 contract:

- canonical `LegalElementDef` / predicate identity;
- supplied `canonical_meaning` and `legal_standard`;
- rationale-first evaluation;
- closed evidence-state vocabulary; and
- constrained factual provenance.

They do not authorize a case-instance binding stage, new DSL abstraction,
offense conclusion, legal effect, pruning, or direct `CaseTruths` mutation by
the model. Any runtime identity needed by the existing symbolic adapter is a
host-side connection concern to be audited separately.

## Call 3 restored boundary

Call 3 is the final neural writer only. It receives the case, symbolic
conclusion/proof, and separately approved legal context to produce the final
free-form IRAC answer. It does not select or assess LegalElement predicates,
repair symbolic execution, or determine liability itself.

The initial interface audit and the next Call 2 schema decision are recorded in
`STEP8_CALL2_SYMBOLIC_INTERFACE_AUDIT.md`.
