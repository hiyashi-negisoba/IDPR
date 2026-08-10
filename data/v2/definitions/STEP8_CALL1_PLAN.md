# Step 8 — Call 1 neural-to-symbolic router pilot

Status: **stable-unique contract amendment approved; derived-gold projection
audit pending before the final amended rerun** (2026-08-10).

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
structured interface.  The raw output list is ordered and contains 1–15 closed
refs.  Its schema still declares `uniqueItems: true` as a generation hint, but
host correctness does not depend on a structured-output backend enforcing it.
The host first hard-validates JSON shape, raw count, strings, and canonical
offense membership.  Malformed, empty, over-limit, unknown, and non-offense
refs remain failures.

Only after validation, repeated canonical refs are explicitly normalized by
stable first occurrence:

```text
raw_seeds → stable_unique(first occurrence) → normalized_seeds → Step 7
```

This is not silent deduplication.  The artifact retains `raw_seeds`,
`normalized_seeds`, `duplicate_refs`, and `normalization_applied`; the raw model
response remains intact.  Repetition is occurrence-level behavior with no new
Definition-level seed information, so downstream compilation and ordered
10-vs-15 measurement use `normalized_seeds`.

## Execution and audit

`scripts/run_v2_call1_pilot.py` accepts exactly the 26 IDs in
`data/eval/kcl_substantive_case_ids.txt`, calls the approved router prompt, then
hard-validates and normalizes the response before invoking `compile_closure()` and
`compile_candidate_offenses()`.  It records all five Step 7 classification
collections, occurrence-preserving frontiers, candidate compilation, raw model
response, usage, and source/prompt/registry/case-list/gold-parquet hashes under
ignored `experiments/`.  The manifest also pins the model snapshot/revision and
sampling/vLLM settings.
It requires explicit `--prompt-approved`; no first model execution is authorised
until the prompt is separately reviewed.

`scripts/report_v2_call1_pilot.py` reads that artifact and uses the reviewed
rubric article gold without attempt-article expansion.  Its original
identity-only article projection is known to under-project derived offenses
(for example Article 347 / `derived_offense.fraud`); derived-gold projection
must be audited before the final rerun's survival rates are used for a freeze.
The direct authored-identity projection is:

```text
gold article a → mapped_refs(a)

raw success     iff mapped_refs(a) ∩ normalized_seeds != ∅
closure success iff mapped_refs(a) ∩ candidate_offense_refs != ∅
```

One surviving ref is sufficient for article-level survival.  The complete
`mapped_refs(a)` list is retained per case so same-article ambiguity and possible
over-crediting remain auditable.  Empty projections are reported as
`out_of_registry`, not as router misses.

For ordered calibration:

```text
prefix10 = normalized_seeds[:10]
full15   = normalized_seeds[:15]
additional_recovery = survives(full15) and not survives(prefix10)
```

There is no padding for a response shorter than ten normalized seeds.  Raw seed
count remains a model-behavior diagnostic only.  The runner always
finishes all 26 artifact rows and the report always includes failure rows.  If a
router contract or transport failure occurs, the report sets
`run_status = FAILED` and `calibration_valid = false`; artifacts remain available
for diagnosis but Call 1 cannot be approved.  After the first run,
the report must be reviewed for seed/closure survival, miss classes, frontier
size, and `additional_recovery`; only one prompt/cap calibration is permitted
before choosing a frozen cap of 10 or 15.  Call 2 remains blocked until that
choice is explicitly recorded.
