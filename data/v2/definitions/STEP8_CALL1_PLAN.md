# Step 8 — Call 1 neural-to-symbolic router pilot

Status: **Call 1 frozen at cap=10; Call 2 contract/prompt review is next**
(2026-08-10).

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
structured interface.  The production raw output list is ordered and contains
1–10 closed refs.  Its schema still declares `uniqueItems: true` as a generation hint, but
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
Definition-level seed information, so downstream compilation uses
`normalized_seeds`.  The completed pilot retains its original ordered 15-cap
responses only as calibration evidence for the frozen 10-cap choice.

## Execution and audit

`scripts/run_v2_call1_pilot.py` accepts exactly the 26 IDs in
`data/eval/kcl_substantive_case_ids.txt`, calls the approved router prompt, then
hard-validates and normalizes the response before invoking `compile_closure()` and
`compile_candidate_offenses()`.  It records all five Step 7 classification
collections, occurrence-preserving frontiers, candidate compilation, raw model
response, usage, and source/prompt/registry/case-list/gold-parquet/
DefinitionRef-gold hashes under
ignored `experiments/`.  The manifest also pins the model snapshot/revision and
sampling/vLLM settings.
It requires explicit `--prompt-approved`; no first model execution is authorised
until the prompt is separately reviewed.

`scripts/report_v2_call1_pilot.py` reads that artifact and uses the reviewed
26-case closed-catalog DefinitionRef gold annotation in
`data/eval/v2_call1_definition_gold_draft.json`.  KCL rubric article gold is
retained there as source context, but is not automatically projected: an
identity-only article projection under-represents derived offenses (for example
Article 347 / `derived_offense.fraud`).  The final metric is:

```text
gold DefinitionRef d

raw success     iff d ∈ normalized_seeds
closure success iff d ∈ candidate_offense_refs
```

This is **closed-catalog DefinitionRef recall**.  A reviewed special-law or
otherwise out-of-catalog row has an explicit empty gold list plus scope note;
it is reported as out of scope and excluded from the recall denominator.
Attempt and preparation are not separate Call 1 labels: later completion/fact
assessment resolves them from the selected offense.

For ordered calibration:

```text
prefix10 = normalized_seeds[:10]
full15   = normalized_seeds[:15]
additional_recovery = survives(full15) and not survives(prefix10)
```

There is no padding for a response shorter than ten normalized seeds.  Raw seed
count remains a model-behavior diagnostic only.  The runner always finishes all
26 artifact rows and the report always includes failure rows.  If a router
contract or transport failure occurs, the report sets `run_status = FAILED` and
`calibration_valid = false`; artifacts remain available for diagnosis but Call 1
cannot be approved.

## Frozen result and next boundary

The final amended 26-case artifact has 26/26 valid router rows and a valid
DefinitionRef report.  It records raw survival 57/86 (66.28%), closure survival
68/86 (79.07%), and eleven closure recoveries.  The 15-cap calibration had no
gold `additional_recovery`; its two beyond-prefix10 rows added only
annotation-gold-external candidate/frontier paths.  The post-run topology audit
found no selected-entrypoint closure failure (15 direct-only router misses and
three missed closure-entrypoint router misses).  Therefore the operational
schema/validator cap is frozen at **10**; no cap-decision rerun is authorized.

The prompt, model/configuration, stable-unique normalization, ordered canonical
DefinitionRef output, and Step 7 connection are frozen.  Call 2 GroundFact
grounding may now begin its separate contract and prompt review.  It may ground
only Step 7 frontier facts as TRUE/FALSE/UNKNOWN and use FALSE for
path-local impossibility pruning; it may not decide offenses, legal elements,
doctrines, participation, or legal effects.
