# Step 8 — v2-only Scallop backend Step 1: minimum contract

Status: **approved for Step 1 implementation and local Scallop parity tests;
no model request is authorized by this contract** (2026-08-11).

This is Step 1 of the frozen v2 Scallop backend plan. It closes only the
minimum three-valued extensional-data and expression-evaluation surface:

```text
DefinitionRegistry / compiled Typed Legal IR
-> static v2 .scl program

CaseTruths
-> validated extensional facts

static program + extensional facts
-> query result
```

It does not lower completion, participation, attribution, doctrine effects,
stage gates, `LiabilityResult`, Call 2 predicate assessment, or the Call 3
writer. It does not alter Call 1, Step 7, frozen Call 2 factual v0, the
Definition Layer, or the Python runtime reference semantics.

## Static program versus case-time facts

The compiler creates a static program only from checked DefinitionRegistry data
and existing compiled Typed Legal IR:

```text
DefinitionRegistry
    ↓
CanonicalExpr roots from compiled IR
    ↓
v2 .scl program
```

The orchestration host separately supplies case-time data:

```text
validated CaseTruths + already-existing OffenseInstanceKey values
    ↓
v2 EDB facts
```

No neural output is compiled as Scallop syntax. Model-produced strings are data
only after host validation.

## 1. Extensional fact vocabulary

Every fact argument is a quoted Scallop `String`. The static program declares
the following v2-only relations. Relation names, arity, and value labels are
fixed; no legacy `card_status` or card id appears.

```text
v2_instance(
  case_id, actor_id, offense_ref, occurrence_id
)

v2_predicate_truth(
  case_id, actor_id, offense_ref, occurrence_id,
  predicate_ref, truth
)

v2_relation_key(
  case_id, actor_id, offense_ref, occurrence_id,
  definition_occurrence_path, relation_ref, left_local_key, right_local_key
)

v2_relation_truth(
  case_id, actor_id, offense_ref, occurrence_id,
  definition_occurrence_path, relation_ref, left_local_key, right_local_key,
  truth
)
```

`v2_instance` is the finite evaluation universe for the program. The
orchestration host emits exactly the existing `OffenseInstanceKey` values it
intends to evaluate, even when their `CaseTruths` mapping has no explicit
predicate entry. This makes Python's missing-ref default (`UNKNOWN`) expressible
in closed-world Datalog without inventing an instance.

`definition_occurrence_path` is the host's canonical JSON serialization of the
existing `RelationInstanceKey.occurrence_path` tuple. It is an opaque data key,
not a model-visible legal identity and not a new runtime abstraction.

### 1.1 Validation rules

The host validates all EDB facts before serializing them:

1. each `v2_instance` is an already-existing `OffenseInstanceKey`; Call 2 and
   Scallop do not create, extract, or choose one;
2. every predicate fact has a registered instance, a loaded predicate ref of
   kind `ground_fact` or `legal_element`, and one of `TRUE`, `FALSE`,
   `UNKNOWN`;
3. there is at most one explicit predicate truth for a
   `(instance_key, predicate_ref)` pair;
4. every relation key/truth is an existing `RuntimeRelationKey` generated from
   a compiled relation obligation, and there is at most one explicit truth per
   such key;
5. every truth label is exactly one of `TRUE`, `FALSE`, `UNKNOWN`; and
6. no value is emitted as source text, relation name, query name, or an
   unquoted Scallop token.

An explicitly stored `UNKNOWN` and an absent `CaseTruths` entry have the same
Step 1 truth semantics. The host may retain the explicit observation for audit,
but no absence is converted to `FALSE`.

### 1.2 Relation scope in Step 1

`v2_relation_key` and `v2_relation_truth` are part of the minimum EDB contract
because `CaseTruths` already has relation truth keyed by
`RuntimeRelationKey`. Step 1 does not yet lower relation obligations into an
offense result. It only preserves their three-valued identity for the later
offense/relation step.

## 2. Static expression-root contract

Step 1 compiles a finite list of host-generated canonical expression roots:

```text
ExpressionRoot {
  expression_id: deterministic compiler-private id
  expression: non-None CanonicalExpr
}
```

`expression_id` is generated from checked compiled IR, not supplied by a model
or case payload. It identifies a static query target only; it is not a new
legal predicate or DSL construct. The compiler must retain a manifest mapping
each id to its canonical expression and DefinitionRegistry/compiled-IR source.

`None` is not a Step 1 expression root. In the existing v2 runtime it means an
absent offense slot and evaluates vacuously only in that slot context. The
Step 1 root planner must omit it rather than emit a synthetic `None -> TRUE`
expression. Its distinction from a completion-suspended slot remains owned by
the later offense-slot/completion lowering, where Python-runtime parity will be
tested.

For Step 1, a `ref` leaf must resolve to a loaded `ground_fact` or
`legal_element`. Completion-policy expressions, doctrine effects, participation
and relation obligation aggregation are later lowering steps even when they
reuse the same expression grammar.

## 3. Three-valued expression lowering

For each static expression root `E`, the generated program derives exactly one
of these relations for every `v2_instance`:

```text
E_true(case_id, actor_id, offense_ref, occurrence_id)
E_false(case_id, actor_id, offense_ref, occurrence_id)
E_unknown(case_id, actor_id, offense_ref, occurrence_id)
```

The compiler then exposes the single query relation:

```text
v2_expression_truth(
  case_id, actor_id, offense_ref, occurrence_id, expression_id, truth
)
```

The static program declares `query v2_expression_truth`. A successful result
must contain exactly one row for every Cartesian pair of supplied
`v2_instance` and compiled `expression_id`, with a closed `truth` label. The
host rejects a missing, duplicated, unknown-id, or out-of-vocabulary row.

The following lowerings are semantic requirements. Generated helper relation
names are compiler-private, deterministic, and never depend on case/model text.

### `ref(predicate_ref)`

```text
TRUE     iff v2_predicate_truth(instance, predicate_ref, "TRUE")
FALSE    iff v2_predicate_truth(instance, predicate_ref, "FALSE")
UNKNOWN  iff explicit "UNKNOWN" OR neither TRUE nor FALSE is present
```

The `UNKNOWN` fallback is guarded by `v2_instance`, so a nonexistent instance
never materializes a result.

### `ALL(children)`

```text
TRUE     iff every child is TRUE
FALSE    iff any child is FALSE
UNKNOWN  otherwise
```

The compiler emits one FALSE rule per child, one TRUE conjunction rule, and an
`UNKNOWN` fallback guarded by the instance universe and absence of derived TRUE
and FALSE.

### `ANY(children)`

```text
TRUE     iff any child is TRUE
FALSE    iff every child is FALSE
UNKNOWN  otherwise
```

The compiler emits one TRUE rule per child, one FALSE conjunction rule, and the
same guarded `UNKNOWN` fallback.

### `NOT(child)`

```text
TRUE     iff child is FALSE
FALSE    iff child is TRUE
UNKNOWN  iff child is UNKNOWN
```

### `ONE_OF(children)`

This is the existing Python evaluator's Kleene exactly-one rule, not a
completion-state choice:

```text
TRUE     iff exactly one child is TRUE and every other child is FALSE
FALSE    iff at least two children are TRUE, or every child is FALSE
UNKNOWN  otherwise
```

The compiler does not need an aggregate/count feature. It emits:

- one TRUE conjunction for each possible sole TRUE child;
- one FALSE conjunction for the all-FALSE case; and
- one FALSE conjunction for every unordered pair of TRUE children.

The guarded default covers all remaining combinations, including one TRUE plus
an UNKNOWN child and all-UNKNOWN children.

## 4. Mandatory parity matrix

Each generated program is tested against `idpr.v2.evaluate.evaluate()` with the
same non-`None` `CanonicalExpr` and `CaseTruths`-derived EDB input. At minimum,
tests cover all `TRUE`/`FALSE`/`UNKNOWN` combinations needed to prove:

| Construct | Required parity cases |
|---|---|
| `ref` | explicit TRUE, FALSE, UNKNOWN, and missing entry -> UNKNOWN |
| `ALL` | all TRUE; one FALSE with UNKNOWN siblings; no FALSE with an UNKNOWN |
| `ANY` | one TRUE with UNKNOWN siblings; all FALSE; no TRUE with an UNKNOWN |
| `NOT` | each of the three child values |
| `ONE_OF` | exactly one TRUE/all remaining FALSE; all FALSE; two TRUE; one TRUE plus UNKNOWN; all UNKNOWN |
| universe | an empty CaseTruths mapping over a supplied instance yields UNKNOWN, while no supplied instance yields no query row |

The test oracle is the existing Python implementation; a Scallop result that
differs is a backend defect, not a reason to alter Python truth semantics.

## 5. Explicit non-goals

This contract does not authorize:

- lowering `CompiledOffense` slots, QUALIFY/COMPOSE, or relation obligations
  into offense results;
- completion selection or suspension;
- doctrine/stage effects, participation/attribution, statutory routes, or
  `LiabilityResult` construction;
- Call 2 predicate-model requests or a change to frozen factual Call 2 v0;
- Call 3 writer work; or
- any actor/event extraction, binding stage, or legacy card mapping.

## Review-completion condition

The fact vocabulary, instance-universe rule, non-`None` root policy, query
cardinality, `ONE_OF` lowering, and parity matrix are approved. Implementation
creates only a v2-only static program emitter, validated EDB renderer, query
parser, and focused parity tests.
