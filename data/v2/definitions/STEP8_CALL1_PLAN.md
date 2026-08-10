# Step 8 — Call 1 neural-to-symbolic router pilot

Status: **implementation complete; prompt review required before the first model
run** (2026-08-10).

This is the bounded follow-on to the completed Step 7 Closure / Probe compiler.
It does not change the 293-object production registry, the sealed Gate① sources,
the coverage boundary, or any recorded HOLD.  It is a Call 1 router pilot only:
Call 2 GroundFact grounding, Call 3 legal-element assessment, and legal-effect or
liability decisions remain out of scope.

## Closed contract

```text
INPUT
  case_text
  + closed offense catalog generated from the loaded DefinitionRegistry

OUTPUT
  { "seeds": ["offense.*" | "derived_offense.*", ...] }
```

The catalog contains every loaded `offense` and `derived_offense` ref.  It has no
case-specific legal mapping.  An `OffenseDef` exposes its authored identity name
and statutory references; a `DerivedOffenseDef` currently has no authored
identity, so it uses its canonical ref as display text and has no invented statute
metadata.

The structured contract has no actor, event, fact-span, confidence, rationale,
doctrine, legal-element, participation-mode, or verdict field.  Case text may,
of course, describe actors and events; the restriction is on the router's
structured interface.  The output list is ordered, contains 1–15 closed refs,
and declares `uniqueItems: true`.  Duplicate refs are a validation failure, not
a host-side deduplication: preserving the model-emitted rank/count is necessary
for the 10-vs-15 measurement.  The raw response remains in the artifact on any
failure.

## Execution and audit

`scripts/run_v2_call1_pilot.py` accepts exactly the 26 IDs in
`data/eval/kcl_substantive_case_ids.txt`, calls the approved router prompt, then
validates the response and invokes `compile_closure()` and
`compile_candidate_offenses()`.  It records all five Step 7 classification
collections, occurrence-preserving frontiers, candidate compilation, raw model
response, usage, and source/prompt/registry/case-list/gold-parquet hashes under
ignored `experiments/`.  The manifest also pins the model snapshot/revision and
sampling/vLLM settings.
It requires explicit `--prompt-approved`; no first model execution is authorised
until the prompt is separately reviewed.

`scripts/report_v2_call1_pilot.py` reads that artifact and uses the reviewed
rubric article gold without attempt-article expansion.  Article projection uses
only authored `OffenseDef.identity.statutory_refs`:

```text
gold article a → mapped_refs(a)

raw success     iff mapped_refs(a) ∩ router_seeds != ∅
closure success iff mapped_refs(a) ∩ candidate_offense_refs != ∅
```

One surviving ref is sufficient for article-level survival.  The complete
`mapped_refs(a)` list is retained per case so same-article ambiguity and possible
over-crediting remain auditable.  Empty projections are reported as
`out_of_registry`, not as router misses.

For ordered calibration:

```text
prefix10 = seeds[:10]
full15   = seeds[:15]
additional_recovery = survives(full15) and not survives(prefix10)
```

There is no padding for a response shorter than ten seeds.  The runner always
finishes all 26 artifact rows and the report always includes failure rows.  If a
router contract or transport failure occurs, the report sets
`run_status = FAILED` and `calibration_valid = false`; artifacts remain available
for diagnosis but Call 1 cannot be approved.  After the first run,
the report must be reviewed for seed/closure survival, miss classes, frontier
size, and `additional_recovery`; only one prompt/cap calibration is permitted
before choosing a frozen cap of 10 or 15.  Call 2 remains blocked until that
choice is explicitly recorded.
