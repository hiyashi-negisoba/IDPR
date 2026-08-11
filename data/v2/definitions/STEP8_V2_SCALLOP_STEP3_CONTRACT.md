# Step 8 — v2-only Scallop backend Step 3: completion policy lowering

Status: **implemented and parity-validated; no model request is authorized**
(2026-08-11).

Steps 1 and 2 are frozen parity-validated lowerings of independent expressions
and ordinary `CompiledOffense` elements.  Step 3 closes the existing
completion surface only:

```text
CompletionPolicyDef + CompiledOffense + CaseTruths
    -> completion candidate truths
    -> CompletionResult
    -> completion-adjusted raw elements truth, where evaluation is reached
```

The Python parity sources are `resolve_completion()` for candidate/state/result
semantics and `runtime.pipeline._iter_obligations()` for the selected state's
adjusted elements fold.  This is one completion lowering, but these are two
different existing runtime responsibilities: `resolve_completion()` selects and
describes a state; it does not itself recalculate Elements.

Step 3 does not lower doctrine effects, participation, attribution, statutory
routes, stage objects, `LiabilityResult`, Call 2 predicate assessment, or the
Call 3 writer.

## 1. Static policy and case-time facts

The static compiler consumes only a checked `CompletionPolicyDef` and its
successful governing `CompiledOffense`, or a successful `CompiledOffense` with
no policy.  A present policy's `offense` must equal the compiled root id;
finding lists, cycles, partial compilations, duplicate policies, unresolved
component scope, or unchecked relation dispositions are pre-execution
failures.

```text
DefinitionRegistry
    -> checked CompletionPolicyDef + CompiledOffense
    -> static v2 .scl policy program and static manifest
```

The host supplies only existing case-time identities and validated `CaseTruths`
facts:

```text
OffenseInstanceKey + CaseTruths
    -> v2 predicate/relation EDB
```

No completion state is added to `OffenseInstanceKey`, and a fact is never
duplicated per completion form.  A completion state is a legal judgement about
one existing instance, not a new instance identity.

### 1.1 Evaluation-scope instances

The ordinary target is the supplied top-level `OffenseInstanceKey`.  A policy
with `when_component` (or its selected state's component-scoped requirement or
slot evaluation) uses the already-existing runtime projection:

```text
component_instance_for(compiled, target_instance, local_key, offense_ref)
```

It preserves `case_id`, `actor_id`, and `occurrence_id`, changing only the
already-authored direct offense-family component's `offense_ref`.  The host
does not extract an actor/event or let a model select the component.

For this static program, `v2_instance` is the finite universe of every target
and deterministic component scope that an emitted Step 3 expression evaluates.
The host additionally emits:

```text
v2_completion_target_instance(case_id, actor_id, offense_ref, occurrence_id)
```

for top-level outputs only.  Component scope rows in `v2_instance` are not
independent offense results and must not appear in any Step 3 result query.
They exist solely so an absent predicate in that existing scope has the same
`UNKNOWN` fallback as Python's `CaseTruths.predicate_view()`.

In Step 3, Step 2's compiled-root-match requirement applies only to
`v2_completion_target_instance`.  A manifest-authorized component-scope
`OffenseInstanceKey` may occur in the broader `v2_instance` universe when it
is deterministically derived from a compiled direct offense-family component.
It cannot be a completion-query output target and is used only as a predicate
evaluation scope.  The host validates the exact target and scope sets from the
static manifest; it rejects a missing, duplicate, or unrelated scope instance.
This is an EDB representation of existing `OffenseInstanceKey` values, not a
new case-instance binding stage.

## 2. Candidate-state lowering and selection

For every declared member of `DERIVABLE_STATES` in a policy, the compiler
canonicalizes and evaluates its `states[state].when` with the approved Step 1
three-valued expression lowering.  The evaluation scope is the target instance
unless that state has `when_component`, in which case it is the exact component
instance from section 1.1.

Candidate state conditions are independent.  A state never reads another
state's element result, and there is no ordering, fallback, or priority rule.
The selected result follows the existing cardinality rule:

```text
exactly one TRUE candidate                 -> that state
two or more TRUE candidates                -> unresolved
no TRUE and one or more UNKNOWN candidates -> unresolved
all declared candidates FALSE              -> not_applicable
```

One `TRUE` selects its state even if another candidate is `UNKNOWN`.  This
ranks confirmation, not named states, and is symmetric under source-state
permutation.

An offense with no `CompletionPolicyDef` deterministically yields:

```text
state = completed
punishable = true
candidate provenance = ()
```

It does not synthesize an authored candidate condition.

## 3. CompletionResult query and static metadata

The generated program exposes these ordered-by-key, not row-order-dependent,
query relations:

```text
v2_completion_candidate_truth(
  case_id, actor_id, offense_ref, occurrence_id, state, truth
)

v2_completion_result(
  case_id, actor_id, offense_ref, occurrence_id, state, punishability
)
```

`state` is one of:

```text
completed | attempted | abandoned_attempt | impossible_attempt |
preparation | unresolved | not_applicable
```

`truth` is `TRUE | FALSE | UNKNOWN`.  `punishability` is `TRUE | FALSE | NONE`:
`NONE` is required only for `unresolved` and `not_applicable`; a derived
declared state must have `TRUE` or `FALSE` exactly as authored.

For each policy-governed target, candidate rows contain every and only its
declared states.  `v2_completion_result` contains exactly one row per target.
The host validates both key sets and the closed vocabularies before it builds a
`CompletionResult`.

The compiler's static manifest maps each `(policy, state)` to its checked,
definition-time metadata:

```text
punishable
suspended_slots
component_suspended_slots
relation dispositions keyed by RelationInstanceKey
canonical additional_requirements
when_component scope, if any
```

After validating the selected result row, the host joins only that selected
state's static metadata.  For `unresolved` and `not_applicable`, it joins no
program metadata at all.  This preserves `CompletionResult.__post_init__`:
neither non-derived outcome can suspend an obligation, retain/suspend a
relation, add a requirement, or carry a punishability value.

The `CompletionCandidateOutcome` provenance is reconstructed from all validated
candidate rows in the static state set, including `FALSE` candidates.  Its
`component_instance` is the static `when_component` scope when present.

## 4. Selected-state adjusted elements

Completion changes the Elements fold after, and only after, a completion result
is validated.  The following query exists exactly when:

```text
completion.state not in {unresolved, not_applicable}
and completion.punishable == TRUE
```

This includes a no-policy offense's deterministic `completed / TRUE` result.

```text
v2_completion_elements_truth(
  case_id, actor_id, offense_ref, occurrence_id, truth
)
```

It contains exactly one row for every eligible target; it has no row for
`unresolved`, `not_applicable`, or a derived non-punishable state.  The host
must not interpret an absent row as a truth.  For a no-policy offense, this
row is the ordinary Step 2 offense-elements truth.  This remains raw symbolic
elements truth, not a `StageResult`, offense activation, or `LiabilityResult`.

For an eligible completion result, the Scallop fold must be exactly the current Python
obligation semantics:

```text
active slot obligations
+ retained relation obligations
+ selected-state additional_requirements, if authored
-> ALL -> TRUE | FALSE | UNKNOWN
```

### 4.1 Global slot and relation dispositions

Without component-scoped suspension, the compiler evaluates the top-level
compiled slot expressions once, omitting only `suspended_slots`.  Omission
means the obligation does not exist in this state; it is not a replacement
`TRUE` fact.

Every recursively enumerated `RelationInstanceKey` is retained unless the
selected policy's authored disposition for that exact definition key is
`suspend`.  Static completion checks already require full explicit disposition
coverage whenever the state suspends anything; the backend must not infer a
relation disposition from touched slots, endpoint types, or predicate overlap.

### 4.2 Component-scoped suspension

When `component_suspended_slots` is nonempty, Step 3 follows the narrow
existing Article 339 branch rather than evaluating flattened top-level slots:

```text
for every direct offense-family component:
    evaluate that component's slots in its deterministic component instance
    omit global suspended slots and that component's selected suspended slots
```

It still folds the top-level offense's complete recursive relation-obligation
set under the selected relation dispositions.  The static checker already
limits this branch to its approved direct-COMPOSE, offense-family scope; Step 3
does not generalize it into a component-program language.

### 4.3 Additional requirement

`additional_requirements` is conjoined; it never replaces existing obligations.
It is evaluated in the selected candidate's `when_component` instance when
one exists, otherwise in the target instance.  The static manifest retains the
non-`None` canonical expression and context.  A requirement's three-valued
truth is part of the generated fold, but its authored expression is never
read from model or case text.

## 5. Relation identity and EDB rules

The Step 2 identity boundary remains unchanged:

```text
static relation helper
    -> RelationInstanceKey(occurrence_path, relation_ref,
                           left_local_key, right_local_key)

target OffenseInstanceKey + RelationInstanceKey
    -> RuntimeRelationKey / v2_relation_key / v2_relation_truth EDB
```

`v2_relation_key` must contain every and only required runtime key for each
top-level target, even where no relation truth is observed.  Missing or
explicit `UNKNOWN` remains `UNKNOWN`; it is never `FALSE`.  Component scope
does not create a second relation-truth namespace in Step 3.

## 6. Determinism and validation

The compiler orders policy roots by offense ref, candidate states by canonical
state label, slots by fixed `SLOT_NAMES`, direct components by authored
`local_key`, and relation obligations by the Step 2 canonical
`RelationInstanceKey` serialization.  Helper names and `.scl` emission never
depend on mapping/set iteration or policy source ordering.

The host validates query output as keyed maps/sets, never by row position:

- candidate keys: `(target_instance, state)` equal the exact declared-state
  set for that target;
- result key: exactly one `target_instance` row;
- adjusted-elements key: exactly the eligible target set defined in section 4
  (`completion.state not in {unresolved, not_applicable}` and
  `completion.punishable == TRUE`);
- all state/truth/punishability/disposition labels are closed vocabulary; and
- all static policy/compiled-offense, scope-instance, and relation-key joins
  are total and exact.

Malformed, missing, duplicate, unexpected, or cross-scope rows are a backend
contract failure.  No completion program metadata or adjusted-elements signal
is emitted for a failed row.

## 7. Mandatory parity matrix

The backend is checked against the existing Python implementation, not a new
completion interpretation.

| Surface | Required parity cases |
|---|---|
| no policy | `completed`, punishable, empty candidate provenance/no suspensions, and adjusted elements equal the Step 2 offense-elements truth |
| candidate evaluation | TRUE/FALSE/UNKNOWN `when`, including `when_component` predicate view |
| selection | one TRUE with UNKNOWN sibling; two TRUE -> unresolved; no TRUE + UNKNOWN -> unresolved; all FALSE -> not_applicable; source-state permutation |
| result invariant | unresolved/not_applicable carries no program metadata; every derived state carries authored punishability |
| global attempt | selected attempt omits suspended slots, retains/suspends only authored exact relation keys, and conjoins `requires` |
| non-punishable | impossible attempt is selected and named, but emits no adjusted-elements row |
| component scope | Article 339 direct component instance, component suspension, requirement context, and retained relation parity |
| relation identity | nested/reused component relation paths stay distinct under selected disposition |
| adjusted fold | `v2_completion_elements_truth` equals Python's `_iter_obligations()`/`fold_all` result for every eligible selected state |
| query validation | candidate/result/adjusted-elements key sets are complete, unordered, and reject duplicate/missing/unexpected/invalid rows |

Any difference from `resolve_completion()` or the selected-state Python
obligation fold is a backend defect; it is never grounds to change the v2
runtime semantics.

## 8. Explicit non-goals

This contract does not authorize:

- doctrine effects, participation/attribution, statutory routes, stage-object
  construction, offense activation, or `LiabilityResult` construction;
- a change to frozen Calls 1 or 2, any Call 2 model request, or a Call 3 writer
  request;
- actor/event extraction, model-selected instance/component identity, a new
  binding carrier, or a new DSL abstraction; or
- a legacy `card_status` mapping.

## Review-completion condition

Step 3 is ready for implementation only after approval of the scope-instance
rule, cardinality selection lowering, selected-state metadata join, adjusted
elements boundary, component-suspension branch, exact query key sets, and
parity matrix.  Implementation then extends only the v2 Scallop backend,
validated EDB/query adapters, and focused parity tests.
