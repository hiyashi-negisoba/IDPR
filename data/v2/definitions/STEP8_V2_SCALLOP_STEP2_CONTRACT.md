# Step 8 — v2-only Scallop backend Step 2: `CompiledOffense` and relation lowering

Status: **implemented and parity-validated; no model request is authorized**
(2026-08-11).

Step 1 closed three-valued evaluation of an independent, non-`None`
`CanonicalExpr`.  Step 2 closes the next and only next symbolic surface:

```text
checked DefinitionRegistry
    -> CompiledOffense (slots + required relation bindings)
    -> static v2 .scl program

OffenseInstanceKey + validated CaseTruths
    -> v2 EDB facts

static program + EDB
    -> offense-elements truth
```

The parity oracle is `idpr.v2.relations.evaluate_compiled_offense()`.  This
step is an elements-level conjunction only.  It does not add a legal rule,
make a liability result, select a completion state, or activate an offense.

## 1. Inputs and static/case-time boundary

The static compiler consumes only checked, successful `CompiledOffense` values
from the existing v2 compiler.  It must reject a finding list, a cycle
sentinel, or any partial/unresolved compilation result.

```text
DefinitionRegistry
    -> compile_offense()
    -> CompiledOffense
    -> static v2 .scl
```

The host supplies existing runtime instances and validated facts separately:

```text
OffenseInstanceKey + CaseTruths
    -> Step 1 v2_instance / predicate / relation EDB
```

For every supplied `OffenseInstanceKey`, `offense_ref` must exactly equal one
compiled static offense root.  A root is identified by its existing
`CompiledOffense.id`; no model, Call 2 result, or case payload names a static
program relation.  The host rejects an instance with no matching compiled
offense before execution.

`CaseTruths` remains input-only.  Step 2 neither creates an
`OffenseInstanceKey` nor writes a predicate or relation truth back to
`CaseTruths`.

## 2. Required relation-instance universe

`CompiledOffense` is **slots plus required relation bindings**, never slots
alone.  For each instance `I` of a compiled offense `C`, the host derives the
complete relation-key set:

```text
{ RuntimeRelationKey(I, key)
  | (key, binding) in iter_relation_instances(C) }
```

It supplies every member of that set as a `v2_relation_key` EDB fact, whether
or not `CaseTruths.relation` contains an explicit observation.  A supplied
`v2_relation_truth` must correspond to one of those keys.  The host rejects a
missing required key, a duplicate key/truth, a key for another compiled
offense occurrence, or an extra relation key outside the expected set.

The key is exactly the existing `RuntimeRelationKey` identity:

```text
(instance_key,
 RelationInstanceKey(occurrence_path, relation_ref,
                     left_local_key, right_local_key))
```

`occurrence_path` is preserved verbatim through the Step 1 canonical JSON
string representation.  It is not collapsed to a relation ref or a defining
offense id.  Consequently, two nested occurrences of the same derived offense
still require two distinct relation facts.

Missing relation observation is `UNKNOWN`, not `FALSE`.  The generated
relation helper for one required key has the same lookup semantics as Python:

```text
TRUE     iff v2_relation_truth(instance, exact_key, "TRUE")
FALSE    iff v2_relation_truth(instance, exact_key, "FALSE")
UNKNOWN  iff explicit "UNKNOWN" or no TRUE/FALSE observation is present,
           guarded by that exact v2_relation_key
```

## 3. Slot and relation lowering

For one `CompiledOffense C`, the static compiler lowers every named slot in
the existing fixed `SLOT_NAMES` order.  A non-`None` slot expression reuses
the approved Step 1 three-valued expression lowering.

`None` retains its existing, narrow meaning: it is an absent offense slot and
is vacuously `TRUE` in this offense-level fold.  The compiler may omit it from
the conjunction; it must not manufacture an independent `None -> TRUE`
expression root.  Completion suspension is deliberately different and is not
considered in Step 2.

```text
slot_truth(C, I)
  = ALL(evaluate(C.slots[slot], predicate_view(I)) for slot in SLOT_NAMES)

relation_truth(C, I)
  = ALL(lookup(key, relation_view(I))
        for key in iter_relation_instances(C))

offense_elements_truth(C, I)
  = ALL(slot_truth(C, I), relation_truth(C, I))
```

An empty relation-obligation set folds to `TRUE`.  The generated program
evaluates slots **once for the top-level `CompiledOffense` only**.  It does not
re-evaluate a nested offense as a component: nested offense slots were already
folded into the parent's compiled slots.  It does, however, lower every
relation key produced recursively by `iter_relation_instances(C)`, including
the nested offense's own obligations.

This covers all current compilation forms without a separate semantic route:

- plain `OffenseDef`: compiled slots and no relation obligations;
- `QUALIFY`: its already-combined compiled slots and no new components;
- `COMPOSE`: its flattened top-level slots plus own and nested
  occurrence-preserving relation obligations.

## 4. Query contract

The static program exposes exactly one query relation:

```text
v2_offense_elements_truth(
  case_id, actor_id, offense_ref, occurrence_id, truth
)
```

It derives one row only when `v2_instance` has that exact instance and its
`offense_ref` matches the compiled offense root.  For a valid host input, the
expected result key set is exactly the supplied `OffenseInstanceKey` set:

```text
{ instance_key | instance_key in supplied_instances }
```

The host validates rows as an unordered map:

```text
instance_key -> TRUE | FALSE | UNKNOWN
```

It rejects a missing key, duplicate, unexpected instance, instance whose
offense ref has no compiled root, invalid arity, or truth outside the closed
vocabulary.  Query row order has no semantic effect.

The resulting truth is only the raw symbolic elements-level output.  In
particular, `TRUE` is not an offense activation or a `LiabilityResult`, and
`FALSE` has no pruning or legal-effect consequence in this step.

## 5. Determinism and provenance

Static roots are ordered by `CompiledOffense.id`.  Slot traversal uses fixed
`SLOT_NAMES` order.  Recursive relation obligations are ordered by canonical
serialization of their full `RelationInstanceKey` fields:

```text
(occurrence_path JSON, relation_ref, left_local_key, right_local_key)
```

Helper relation names and emitted rules use those canonical orderings, never a
set/frozenset iteration order.  The compiler retains a static manifest from
each lowered offense root and relation helper to its checked compiled source
and exact definition-time `RelationInstanceKey`:

```text
relation helper
    -> RelationInstanceKey(occurrence_path, relation_ref,
                           left_local_key, right_local_key)
```

The case-time host combines that static key with its existing
`OffenseInstanceKey` to form the `RuntimeRelationKey` used in EDB facts:

```text
OffenseInstanceKey + RelationInstanceKey -> RuntimeRelationKey
```

Case/model text remains EDB data only.

## 6. Mandatory parity matrix

Every Step 2 result is compared to:

```python
evaluate_compiled_offense(
    compiled,
    case_truths.predicate_view(instance),
    case_truths.relation_view(instance),
)
```

At minimum, focused parity tests cover:

| Surface | Required parity cases |
|---|---|
| plain offense | all slots TRUE; one predicate FALSE; missing predicate -> UNKNOWN |
| absent slot | `None` slot is vacuous TRUE without an independent expression root |
| QUALIFY | qualifier slot addition contributes to the same top-level fold |
| flat COMPOSE | all slots/relations TRUE; a required relation FALSE; missing relation -> UNKNOWN |
| nested COMPOSE | a nested relation FALSE/UNKNOWN propagates to the parent result |
| occurrence identity | reused derived-offense components with identical local relation names require distinct occurrence-path facts |
| slot recursion | slots are folded once at the top, while nested relation obligations remain included |
| query contract | expected instance-key set is complete and unordered validation rejects duplicate/missing/unexpected/invalid rows |

A difference from `evaluate_compiled_offense()` is a Scallop backend defect;
it is never grounds to change existing Python semantics.

## 7. Explicit non-goals

This contract does not authorize:

- completion selection, completion requirements, slot or relation suspension;
- participation, attribution, statutory routes, doctrine/stage effects, or
  `LiabilityResult` construction;
- Call 2 predicate-model requests or any change to frozen Call 2 factual v0;
- Call 3 writer work;
- actor/event extraction, a binding stage, a new DSL abstraction, or a legacy
  `card_status` mapping.

## Review-completion condition

Step 2 is ready for implementation only after approval of the exact
instance-to-compiled-root rule, total occurrence-preserving relation-key
universe, `None` slot treatment, query cardinality, and parity matrix.  The
subsequent implementation may extend only the v2 Scallop backend emitter/EDB
validator/query parser and add focused parity tests for this contract.
