# V2 verification strategy
Status: rebuilt from zero on 2026-08-11.

The previous `tests/` suite was deleted in full. Its historical pass counts are not
acceptance evidence for the current pipeline.

## Gates

### Gate A — deterministic semantics

This gate may prove only host-owned behavior:

- the full three-valued DSL truth tables;
- Definition Layer schema, type checks, and total compilation;
- factual-only gold shape and exact source provenance;
- planner identity/cardinality/uniqueness;
- request evidence isolation;
- response order/cardinality and exact-key reconstruction.

Gate A cannot approve factual or legal accuracy.

### Gate B — real backbone semantics

This gate must execute the backbone model served by job `221593`. It contains reviewed
positive, negative, and UNKNOWN expectations over real KCL factual spans. No full Call 2
run is permitted unless every Gate B case passes with the production prompt, schema, and
payload builder.

The minimum regression set covers:

- an attempted sexual offense that must not become completed intercourse;
- unrelated bribery and taking predicates that must remain UNKNOWN;
- a directly stated injury conduct that must remain TRUE;
- the right-exercise-obstruction paragraph, including its positive elements and unrelated
  arson/bribery negatives.

### Gate C — symbolic and rubric acceptance

The 26-case run must be compared with the reviewed per-question rubric. Structural
correspondence is reported separately from semantic acceptance. The following are hard
failures:

- any CaseTruth key outside the planner;
- any established offense outside reviewed candidate scope without an explicit review;
- a required rubric theory with no evaluated route;
- a participation fact pattern for which the planner supplies no participation route;
- Call 3 changing or inventing a symbolic conclusion;
- a truncated model response.

## Current results

- Gate A: 69 passed.
- Gate B: 2 passed against the real Gemma service after occurrence evidence isolation and
  reviewed few-shot examples.
- Gate C: blocked. The runner does not currently supply the Scallop backend's existing
  `derivative_links` or `co_principal_sources`, so participation-heavy questions cannot be
  accepted yet.
