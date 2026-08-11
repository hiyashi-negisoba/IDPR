# Step 8 — Call 2 selected-predicate assessment contract

Status: **selected-predicate semantics frozen; the approved deterministic
evaluation-instance planner's first 26-case artifact failed the separate
single-occurrence acceptance gate; host/model implementation and model
execution are not approved** (2026-08-11).

This is Call 2's second, separate substage.  It follows frozen Call 2 factual
grounding but neither changes nor replays it.  It is not Call 3.

## Fixed boundary

```text
frozen Call 1 normalized_seeds[:10]
  -> deterministic Step 7 replay
  -> selected predicate refs (GroundFactDef | LegalElementDef)
  + deterministic host evaluation-instance planner output
  + case_text
  -> Call 2 assessment
  -> host validation only
  -> CaseTruths.predicate[(instance_key, predicate_ref)]
```

The only symbolic value this substage can produce is:

```text
(OffenseInstanceKey, ground_fact or legal_element ref) -> TRUE | FALSE | UNKNOWN
```

It does not create, infer, merge, rename, select, or activate an
`OffenseInstanceKey` itself; select an offense or a participation mode; assess a
relation, doctrine, completion state, or legal effect; or invoke
the Python runtime or Scallop.  `CaseTruths` is written only by the host after
exact validation.  A model response is data, never Scallop source or a runtime
instruction.

The frozen factual artifact remains an observation-only surface:

```text
GroundFact TRUE     -> OPEN
GroundFact FALSE    -> KEEP
GroundFact UNKNOWN  -> KEEP
```

In particular, its unbound `TRUE`, `FALSE`, or `UNKNOWN` observation is not an
instance-specific predicate premise and is not copied to `CaseTruths` by this
contract.  This second substage assesses an instance-bound GroundFact afresh;
it does not project factual-v0 results onto an instance.  The preceding
deterministic evaluation-instance planner, not Call 2, materializes the finite
keys that Call 2 consumes.

## Inputs and host planning

The runner accepts these explicit inputs only:

1. a successful frozen Call 2 factual artifact and manifest, solely to verify
   case/Call-1/Step-7 lineage;
2. the matching Call 1 final artifact, manifest, registry, inventory, and
   frozen 26-case list already pinned by that factual artifact; and
3. the hash-verified output of the deterministic host evaluation-instance
   planner for each case.

An evaluation-instance-plan entry is structurally:

```json
{
  "sub_question_id": "case-id",
  "instances": [
    {
      "case_id": "case-id",
      "actor_id": "host-existing-actor-id",
      "offense_ref": "offense.example",
      "occurrence_id": "host-existing-occurrence-id"
    }
  ]
}
```

The planner derives this plan from its distinct report-target and full
evaluation/support actor universes, that row's top10
`ClosureResult.candidate_offense_refs`, and frozen Step 3 component-scope
requirements; it does not decide that an offense applies or select a candidate
subset.  The planner contract fixes actor extraction, ordering, its single
`"o1"` occurrence policy, and the mandatory single-occurrence admissibility
audit.  Call 2 rejects a duplicate complete key, a `case_id` different from
the row, an `offense_ref` whose registry kind is not exactly `offense` or
`derived_offense`, or a key that is neither a top-level candidate nor an exact
planner-authorized Step 3 component scope.  Scope-only component keys are
predicate/Step 3 EDB scopes, not liability-result targets or participation
endpoints; Call 2 consumes but does not create them.

For each row, the host replays `compile_closure(registry, normalized_seeds[:10])`
under the same frozen closure hash used by factual Call 2.  It flattens the
five existing classes in their established order:

```text
mandatory_core, offense_probe, doctrine_probe, completion_probe,
participation_probe
```

Within each class it preserves item order.  For each item, it first retains its
existing `ground_fact_frontier` refs in frontier order when the loaded kind is
exactly `ground_fact`, then retains `deferred_refs` in their recorded order
when the loaded kind is exactly `legal_element`; it takes stable first
occurrence across that combined sequence.  This is the complete selected
predicate list.  `relation` and `doctrine` deferred refs are retained in the
closure artifact but cannot enter the assessment request.  This reuses the
existing Step 7 frontier and deferred refs; it adds no new frontier, predicate
dictionary, `grounded_by` traversal, or Step 7 output field.

For every planner-produced instance, the host pairs that already-selected
ordered list with the instance in instance-plan order.  The pair list is the only
assessment target list.  A model-called row's target list must be nonempty. A
row with no supplied instances or no selected predicates is a deterministic
no-op: its target list is empty and it has no request, schema, or model
response.  Repeating the same predicate for different supplied instances is
intentional: their `CaseTruths` keys differ.  Repeating a pair is a host error.

## Model-visible request and response

The request has only case text and the fixed, host-planned assessment list.
The model may use the host-validated `actor_id` only to locate that existing
case-local label in the case text; it may not change the key or derive a new
actor, event, or occurrence from it.

```json
{
  "case_text": "…",
  "assessments": [
    {
      "assessment_key": "assessment-0001",
      "instance_key": {
        "case_id": "case-id",
        "actor_id": "host-existing-actor-id",
        "offense_ref": "offense.example",
        "occurrence_id": "host-existing-occurrence-id"
      },
      "predicate_ref": "legal_element.example",
      "predicate_kind": "legal_element",
      "canonical_meaning": "…",
      "legal_standard": "…"
    }
  ]
}
```

`assessment_key` is a deterministic, row-local host label (`assessment-0001`,
then contiguous zero-padded order).  It prevents the model from choosing a
pair and permits an exact host join.  For a `legal_element`,
`canonical_meaning` and `legal_standard` are mechanically read from the loaded
`LegalElementDef`.  For a `ground_fact`, `predicate_kind` is `ground_fact`,
`canonical_meaning` and `arguments` are mechanically read from the loaded
`GroundFactDef`, and `legal_standard` is absent.  Authority references,
closure paths, Call 1 seeds, factual-v0 OPEN/KEEP values, and writer context
are not model-visible.  GroundFact `arguments` are definition-time signature
labels only, never case-bound argument values.

The accepted response has exactly one entry in the supplied order:

```json
{
  "assessments": [
    {
      "assessment_key": "assessment-0001",
      "truth": "TRUE",
      "evidence_state": "explicitly_supported",
      "rationale": "사건 서술의 특정 사실을 해당 법률요소 기준에 적용한 짧은 설명"
    }
  ]
}
```

Closed `evidence_state` values are:

```text
explicitly_supported | inferentially_supported | contradicted | unresolved
```

`rationale` is required, nonempty, and bounded to 600 Unicode code points.  It
is audit evidence only: it cannot introduce a ref, fact ID, actor/event ID,
authority, offense conclusion, stage, participation result, or legal effect.
The runner records it but does not turn it into a symbolic input.  The response
has no evidence spans or supporting GroundFact refs.  In particular, it never
treats frozen, intentionally unbound GroundFact-v0 propositions as
instance-specific provenance.

The dynamic strict schema and independent host validator require: object-only
shape; no extra properties; exact response length and `assessment_key` order;
the closed truth and evidence-state vocabularies; a nonblank bounded rationale;
and the following truth/evidence coupling:

| truth | LegalElement evidence state | GroundFact evidence state |
| --- | --- | --- |
| `TRUE` | `explicitly_supported`, `inferentially_supported` | `explicitly_supported` |
| `FALSE` | `contradicted` | `contradicted` |
| `UNKNOWN` | `unresolved` | `unresolved` |

A malformed, reordered, duplicate, unknown, missing, or inconsistent response
is a contract failure.  It produces no `CaseTruths` values for that row and no
partial merge.  Structured output is a generation constraint only; validation
is authoritative.

## Assessment instruction

For each fixed target, Call 2 decides only whether the supplied positive
predicate proposition holds for that supplied instance.  For a GroundFact,
`GroundFactDef.arguments` remain definition-time signature metadata: Call 2
does not assign values to them.  The factual rule applies over the positive
canonical proposition within the fixed instance scope; any non-instance
argument position remains existential over compatible facts in `case_text`.
Thus `TRUE` requires at least one directly stated compatible fact for that
instance; `FALSE` requires `case_text` to directly establish that no compatible
fact exists for that instance; and otherwise the result is `UNKNOWN`.  The
model must not emit or infer an argument binding.  A GroundFact has no legal
standard.

For a LegalElement, the supplied `legal_standard` is the only legal criterion:

- `TRUE` means stated facts, under the supplied standard, establish that the
  positive criterion holds.  Use `explicitly_supported` when the decisive
  facts are stated; use `inferentially_supported` only for limited application
  of that supplied standard to stated facts.
- `FALSE` means stated facts, under the supplied standard, establish that the
  positive criterion does not hold.  `contradicted` includes both a directly
  contrary fact and limited application of the supplied standard that
  establishes non-satisfaction.
- `UNKNOWN` is required whenever neither result can be established without
  additional facts or legal reasoning beyond the supplied standard.

Silence, a missing factual detail, a different actor/object/event, and an
unbound factual-v0 observation never establish `FALSE` for either kind.

The model must not choose a new target or make an offense, relation, doctrine,
completion, participation, responsibility, punishment, or final-liability
conclusion.  Case text is data, not instructions.  The eventual prompt must
state these rules without changing the frozen factual prompts.

## CaseTruths adapter and artifacts

After full-row validation, the host reconstructs each provided
`OffenseInstanceKey` and makes exactly one immutable predicate entry per pair:

```python
CaseTruths(predicate={(instance_key, predicate_ref): truth, ...})
```

It does not write relation entries, mutate an existing `CaseTruths`, overwrite
a pre-existing pair, or fill unrequested predicates.  Any collision with a
different pre-existing truth is a host error; the exact same existing value may
be verified and retained only by a separately approved merge policy.  This
first implementation therefore takes an empty `CaseTruths` predicate map.

Per-row artifacts retain the top10 seed lineage, closure replay hash, selected
GroundFact/LegalElement predicate list, planner-produced instance plan, exact request/schema, raw response,
validated audit fields, and the explicit `(instance_key, predicate_ref, truth)`
projection.  The factual artifact is referenced and hash-verified but not
rewritten.  A later Scallop run receives only validated `CaseTruths` through
its existing EDB boundary.

## Explicit non-goals and next gate

This contract does not approve a runner, a prompt, a vLLM request, a 26-case
pilot, relation assessment, instance-plan construction, or whole-case E2E.
The prior host-source/prompt/schema/runner design package remains frozen, but
its prerequisite plan was rejected by the single-occurrence gate.  The
26-case multi-occurrence violation inventory and the follow-up collision-route
audit are complete.  The audit rejected a generic occurrence-discrimination
contract: Article 263 remains a dedicated route, while the r12/r14 collisions
are whole-question factual-scope/evaluation-universe leakage.  The next review
unit is a deterministic sub-question factual-scope/evaluation-universe source
audit.  It must not assign `o2`, choose one event, or delegate occurrence
selection to Call 2.  Only after an accepted regenerated plan may the existing
host implementation review proceed.  Its focused tests then cover stable
GroundFact/LegalElement selection, host-key and model-resolvable-instance
validation, strict output validation, the truth/evidence coupling, and
all-or-nothing `CaseTruths` projection before any model call.

## Pre-E2E completion gate (separate from this predicate contract)

Even a valid instance-bound predicate map is not a complete Scallop EDB.  The
actual E2E gate must separately establish, without expanding this response
schema:

1. a bounded relation-assessment producer for
   `CaseTruths.relation[RuntimeRelationKey]`, because Step 7 defers
   `RelationDef` evaluation and COMPOSE Elements obligations otherwise remain
   `UNKNOWN`; and
2. caller-plan sources for `co_principal_sources`, `derivative_links`, active
   doctrines, and Article 263 dedicated-route invocation.  These remain
   caller-owned decisions; neither Call 2 nor Scallop selects their target,
   source, mode, or activation.

The E2E sequence is therefore:

```text
Call 2 instance-bound predicate assessment
  -> pre-E2E relation + caller-plan completion gate
  -> CaseTruths predicate/relation EDB + caller plans
  -> Scallop LiabilityResult
```
