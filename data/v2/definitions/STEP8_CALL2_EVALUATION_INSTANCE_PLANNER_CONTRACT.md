# Step 8 — deterministic evaluation-instance planner contract

Status: **historical first-planner contract: its mechanical artifact and
offline audit passed, but its `"o1"`-only 26-case cohort failed.  It is
superseded as the prospective instance source by
`STEP8_GENERAL_OCCURRENCE_GROUNDING_CONTRACT.md`; no Call 2 host
implementation or model execution is approved** (2026-08-11).

## Purpose and correction

There is no upstream `OffenseInstanceKey` artifact for the frozen 26-case
cohort.  The selected-predicate contract therefore cannot truthfully require a
manual plan of “already-existing” keys.  This bounded host planner supplies the
missing producer before Call 2:

```text
frozen Call 1 normalized_seeds[:10]
  -> deterministic Step 7 ClosureResult
  + question_prompt report targets and case_text evaluation/support actors
  -> finite OffenseInstanceKey evaluation universe
  -> Call 2 selected-predicate assessment
```

The planner does **not** decide that a candidate offense applies, choose a
subset of candidates, determine a participation role, bind an event/object/
GroundFact argument, or call a model.  It materializes every candidate and
required Step 3 predicate scope for the full case-local actor label universe.
Call 2 merely consumes these keys and still may not create or select an
instance.

## Inputs and pinned lineage

The planner accepts only the final frozen Call 1 artifact/manifest, production
registry, substantive inventory, and `kcl_substantive_case_ids.txt`.  It
requires exact 26-case order and verifies the Call 1 registry, inventory, and
case-list hashes plus the frozen Step 7 closure commit/hash.  Per row its sole
seed lineage is:

```text
top10_seeds = normalized_seeds[:10]
closure = compile_closure(registry, top10_seeds)
```

It does not use Call 1 raw seeds, full15 closure evidence, or a factual-v0
artifact.  It neither starts a service nor has network/model configuration.

## Report-target and evaluation actor universes

The planner retains two distinct, ordered label sets.  `report_target_actor_ids`
are the stable first occurrence of the Korean legal-person labels matching:

```text
[甲乙丙丁戊己庚辛壬癸]
```

in the inventory row's `question_prompt`, in textual order.  This is a
mechanical reporting-target extraction, not entity resolution from `case_text`.

In the frozen inventory, the immutable narrative field is named
`question_text`; it is passed verbatim as this contract's `case_text`.  This is
a field-name adaptation only, not a second extraction or text rewrite.

`evaluation_actor_ids` are instead the stable first occurrence of the same
label grammar across the entire `case_text`, in textual order.  This is the
finite support universe needed for a later co-principal or derivative
dependency even when the question asks only about a different actor.  It is
label-universe materialization, not a role, victim, official, or offense
inference.

The planner rejects a row if either set is empty, if a report-target label is
not present in `case_text`, or if `report_target_actor_ids` is not an ordered
subset of `evaluation_actor_ids`.  It never extracts Latin labels or a person
from narrative semantics.  Downstream reporting may use only
`report_target_actor_ids`; symbolic/Call 2 assessment uses the full
`evaluation_actor_ids`.

This limited grammar is valid only for the frozen 26-case cohort.  A future
cohort or a question whose target actor is not expressible by this grammar
requires a new planner-contract review rather than a fallback model/manual
selection rule.

## Top-level, predicate-scope, and assessment instances

For each row, top-level candidate offense refs are exactly:

```python
tuple(sorted(closure.candidate_offense_refs))
```

Every ref must resolve to registry kind `offense` or `derived_offense`.  The
planner creates `top_level_instances` in this order:

```text
case-list order
  -> evaluation_actor_ids in case_text first-occurrence order
    -> candidate_offense_refs lexicographic order
      -> occurrence_id "o1"
```

Every top-level key is therefore:

```python
OffenseInstanceKey(
    case_id=sub_question_id,
    actor_id=extracted_actor_label,
    offense_ref=candidate_ref,
    occurrence_id="o1",
)
```

For every top-level instance, the planner then derives
`predicate_scope_instances` with the same deterministic rule frozen in Scallop
Step 3.  For its successfully compiled top-level root and completion policy:

- each state with `when_component` adds exactly
  `component_instance_for(compiled, target, local_key, offense)`;
- if a state has `component_suspends`, it adds
  `component_instance_for(...)` for every direct offense-family component of
  that compiled root; and
- it adds no other component scope.

The implementation must share this rule with, or prove exact focused-test
parity against, `scallop_backend._completion_scope_instances()`.  A scope-only
key preserves the parent `case_id`, `actor_id`, and `occurrence_id`, changing
only the authored direct component offense ref.  It is used for predicate
assessment/Step 3 EDB evaluation only: it is not a `LiabilityResult` target, a
completion target, or a participation endpoint.

`assessment_instances` are stable-unique
`top_level_instances + predicate_scope_instances`, preserving that order.  The
planner records all three sets separately.  A downstream Call 2 validator must
accept a key only if it is either a top-level candidate instance or an exact
planner-authorized Step 3 component scope; it must not require every scope-only
offense ref to be in `candidate_offense_refs`.

`"o1"` is the sole first-implementation occurrence value.  The planner
rejects duplicate keys and does not accept an input occurrence list.  Before a
generated plan can be accepted, a separate read-only cohort audit must establish
for every emitted `(case_id, actor_id, offense_ref)` that no separately
material factual occurrences would need distinct keys to avoid combining their
predicate truths as one offense occurrence.  A single violation rejects that
case from this first planner cohort; it does not permit a silent key split or
an occurrence resolver fallback.

## Generated artifact and audit

The generated JSONL preserves the 26-case order.  Each row contains enough
host evidence to reproduce the product:

```json
{
  "sub_question_id": "kcl_criminal_…",
  "top10_seeds": ["offense.example"],
  "report_target_actor_ids": ["甲"],
  "evaluation_actor_ids": ["甲", "乙"],
  "candidate_offense_refs": ["derived_offense.example", "offense.example"],
  "top_level_instances": [
    {
      "case_id": "kcl_criminal_…",
      "actor_id": "甲",
      "offense_ref": "derived_offense.example",
      "occurrence_id": "o1"
    }
  ],
  "predicate_scope_instances": [],
  "assessment_instances": [
    {
      "case_id": "kcl_criminal_…",
      "actor_id": "甲",
      "offense_ref": "derived_offense.example",
      "occurrence_id": "o1"
    }
  ],
  "instances": [
    {
      "case_id": "kcl_criminal_…",
      "actor_id": "甲",
      "offense_ref": "derived_offense.example",
      "occurrence_id": "o1"
    }
  ]
}
```

`instances` is an alias of `assessment_instances` for the downstream Call 2
consumer.  Its manifest pins all input hashes, frozen closure source hash,
planner source fingerprint, both actor-universe grammars, candidate ordering
rule, Step 3 component-scope rule, fixed occurrence rule, complete case order,
and per-run aggregate counts.  The companion audit recomputes every row from
inputs and rejects an order/product/key mismatch, missing/extra row, invalid
actor label, invalid candidate/component scope, non-`"o1"` occurrence, or
duplicate key.

For every row, the audit additionally records:

```text
top_level_instance_count
predicate_scope_instance_count
assessment_instance_count
selected_predicate_count
final_assessment_target_count
```

`selected_predicate_count` is the frozen Call 2 stable-first GroundFact plus
LegalElement list; `final_assessment_target_count` is its product with
`assessment_instance_count`.  The generated-plan acceptance review must
compare every row's count and serialized request/schema size with the reviewed
model/context/completion budget.  No batching or sharding is implied.  If a row
does not fit, the planner/Call 2 run is rejected until a separate deterministic
sharding contract is approved.  The generated plan remains an orchestration
artifact, not a legal conclusion or a `CaseTruths` value.

## Acceptance and downstream boundary

The planner must first be implemented with focused tests for both actor
universes, candidate coverage/order, Step 3 component-scope parity, full
product, duplicate prevention, and all lineage failures.  A generated 26-case
plan, single-occurrence admissibility review, cardinality/budget evidence, and
offline audit are then reviewed as their own acceptance gate.

Only a plan that passes that gate may be supplied to the selected-predicate
Call 2 host runner.  The first plan did not pass: its `"o1"` policy has a
recorded 26-case counterexample.  The completed 26-case multi-occurrence
violation inventory is recorded in
`experiments/v2_call2_evaluation_instance_planner/multi_occurrence_violation_inventory.md`.
It identifies three collision families and literal case-text distinguishers;
it is not a manual `o2` assignment or a change to Call 2.  The subsequent
collision-route audit found no established generic same-actor multi-instance
need: Article 263 remains dedicated, while r12/r14 arise from whole-question
factual-scope leakage and expanded candidates.  The negative source audits
then ruled out manual factual-scope recovery and an Article 263 caller target
map.  The prospective path is the general occurrence-grounding contract, not
a revision of this `"o1"` planner.

That later runner may validate/hash an accepted plan but cannot alter it, add
an instance, or reduce its universe.  Relation assessment and caller-owned
participation/doctrine/Article 263 plans remain outside this planner and inside
the existing pre-E2E completion gate.
