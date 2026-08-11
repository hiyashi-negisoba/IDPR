# Step 8 — Call 2 to symbolic interface audit

Status: **code audit complete; no implementation or model execution approved**
(2026-08-11).

## Architecture invariant

```text
Call 1 neural offense routing
-> Step 7 DSL/compiler narrowing
-> Call 2 neural factual grounding + selected predicate assessment
-> DSL / Scallop symbolic execution
-> Call 3 neural final IRAC writer
```

Call 2 is one architectural neural assessment stage with two host-visible
parts:

```text
Call 2 factual grounding       (frozen v0)
Call 2 selected-predicate assessment  (missing)
```

The latter is not a new Call 3. It assesses only the predicates/cards selected
by Step 7 and supplies validated state to symbolic execution. Call 3 is the
final writer, not a LegalElement assessor.

## Decision recorded (2026-08-11)

The canonical v2 symbolic handoff is **Call 2 -> `CaseTruths`**. This does
not select the current Python runtime as the final symbolic backend.

```text
DefinitionRegistry -> Typed Legal IR -> v2 .scl program
                                             ↘
                                               Scallop -> typed result adapter -> LiabilityResult
                                             ↗
Call 2 -> CaseTruths -> extensional facts
```

The repository's legacy `card_status(case_id, card_id, satisfied |
not_satisfied | unknown)` contract is not part of the v2 production path. Its
safe native-Scallop process infrastructure may be reused, but its card-id
semantics and legacy RuleIR mapping may not be imported into v2.

## Audit scope and non-changes

This audit read the current v2 closure, frozen Call 2 runner/artifact code, v2
runtime, and the repository's native Scallop boundary. It did not call a model,
start a service, run Call 1/2, modify Step 7 or Definition Layer data, or alter
the frozen Call 2 artifacts.

## A. What Step 7 already selects

`compile_closure()` emits five ordered classes: `mandatory_core`,
`offense_probe`, `doctrine_probe`, `completion_probe`, and
`participation_probe`. Every `ClosureItem` carries both:

- `ground_fact_frontier`: occurrence-preserving GroundFact requests; and
- `deferred_refs`: sorted, de-duplicated deferred legal refs.

When traversal reaches a `legal_element`, it adds the ref to `deferred_refs`.
Relations and doctrines may also appear there. Thus Step 7 already narrows the
LegalElement vocabulary needed by the selected top10 closure, without a new
registry table or a LegalElement occurrence frontier.

The frozen Call 2 runner uses only `ground_fact_frontier`:

```text
top10 normalized seeds
-> deterministic compile_closure replay
-> flatten_ground_fact_frontier
-> unique GroundFact proposition request
```

It currently never reads `deferred_refs` to make a model request. Therefore
selected LegalElements are available from Step 7 but are not yet assessed.

## B. What frozen Call 2 supplies

The frozen runner (`scripts/run_v2_call2_pilot.py`) writes, for each successful
row:

```text
top10 seeds
occurrence_frontier
proposition_projection
model_request and raw_response
validated_proposition_groundings: GroundFact ref -> TRUE | FALSE | UNKNOWN
projected_occurrence_groundings: same truth + OPEN | KEEP
```

This satisfies factual grounding only. It has no LegalElement request or result,
no predicate/card truth for a symbolic engine, no relation truth, no
`CaseTruths` construction, and no Scallop invocation. Its `OPEN`/`KEEP` action
is non-destructive observation metadata, not a symbolic truth.

## C. What the v2 symbolic runtime actually requires

The active v2 symbolic implementation is the Python runtime, not native
Scallop. `CaseTruths` accepts:

```text
predicate[(OffenseInstanceKey, predicate_ref)] -> TRUE | FALSE | UNKNOWN
relation[RuntimeRelationKey]                  -> TRUE | FALSE | UNKNOWN
```

`OffenseInstanceKey` contains `case_id`, `actor_id`, `offense_ref`, and
`occurrence_id`. The runtime then evaluates existing DSL expressions with
`ALL`/`ANY`/`NOT`/`ONE_OF`, completion, doctrine effects, participation, and
stages. It defaults an absent predicate/ref to `UNKNOWN`.

There is no production host that builds `CaseTruths` from a Call 2 artifact:
the present constructions are test fixtures or runtime-internal attribution
copies. There is likewise no v2 production adapter that passes Call 2 output to
native Scallop.

## D. The repository's existing Scallop boundary is distinct

The legacy/native Scallop module (`src/idpr/rulebase/scallop.py`) accepts a
different contract:

```text
card_status(case_id, card_id, satisfied | not_satisfied | unknown)
```

It is keyed only by `case_id` and card id. It is not wired to v2
`OffenseInstanceKey`, v2 `LegalElementDef`, v2 `CaseTruths`, or the frozen Call
2 GroundFact artifact. The current codebase therefore has two symbolic
interfaces, not one existing Call 2-to-Scallop adapter.

## Interface-gap table

| Boundary | Present | Missing |
|---|---|---|
| Step 7 -> Call 2 factual grounding | Top10 replay and occurrence-preserving GroundFact frontier | Nothing for frozen factual v0 |
| Step 7 -> Call 2 selected predicate assessment | `deferred_refs` contains LegalElement refs | Stable LegalElement request projection and request/response schema |
| Call 2 -> CaseTruths | Runtime accepts three-valued predicate/relation maps | Host adapter, evaluation instance keys, LegalElement truth mapping, and relation inputs |
| CaseTruths -> v2 Scallop | Target architecture is documented | v2 Typed Legal IR-to-Scallop compiler and result/proof adapter |
| Legacy native Scallop | Safe process/serialization infrastructure exists | Deliberately excluded card-id semantics; no v2-to-card mapping is permitted |
| Symbolic result -> Call 3 writer | `LiabilityEvaluation` types exist | A final-writer request/response contract and runner |

## Minimal-diff direction

The smallest next implementation target is a **Call 2 predicate-assessment
substage** that consumes a successful frozen Call 2 factual artifact and the
same deterministic top10 Step 7 replay. It is not a Call 3 runner and does not
rerun frozen factual grounding.

Its host planner can derive the model-visible target list by flattening the
same five closure classes in their existing order, retaining only refs whose
loaded registry kind is `legal_element`, and taking stable first occurrence.
It must not modify Step 7, create a LegalElement occurrence frontier, add
`grounded_by`, or create an independent binding architecture.

The remaining contract work is not a CaseTruths-versus-Scallop choice.
`CaseTruths` is the v2 extensional input interface and Scallop remains the
target backend. The next engineering audit is which Python runtime semantics
already have a v2 Scallop compilation and which remain Python-only; see
`STEP8_V2_SCALLOP_BACKEND_AUDIT.md`.

The later Call 2 host adapter validates a three-valued predicate truth and
attaches it only to caller-supplied existing `OffenseInstanceKey` values in
`CaseTruths`. This is not a new binding stage; it is the required input key for
the existing case runtime and eventual Scallop backend. Call 2 never creates,
extracts, or chooses an `OffenseInstanceKey`; the orchestration host supplies
it per assessment request, and only the host writes validated results to
`CaseTruths`.

For either target, the likely Call 2 assessment result needs both a closed
symbolic value and non-symbolic audit evidence, for example:

```json
{
  "predicate_ref": "legal_element.example",
  "truth": "TRUE | FALSE | UNKNOWN",
  "evidence_state": "explicitly_supported | inferentially_supported | contradicted | unresolved",
  "supporting_ground_fact_refs": ["ground_fact.example"],
  "rationale": "short element-specific application"
}
```

This is an audit recommendation, not an approved wire contract. A later review
must define the truth/evidence-state relationship, provenance rules, relation
assessment scope, and host projection. In particular, frozen unbound Call 2
GroundFact `FALSE`/`UNKNOWN` observations must not silently become a negative
LegalElement assessment.

## Consequences for later work

- Keep frozen factual Call 2 v0 artifacts and their `TRUE -> OPEN`,
  `FALSE/UNKNOWN -> KEEP` adapter unchanged.
- Move `canonical LegalElement`, `legal_standard`, rationale-first,
  evidence-state, and constrained provenance ideas into the new Call 2
  predicate-assessment review.
- Do not create `Call 3 LegalElement assessment`, a new case-instance binding
  stage, a Step 7 change, a `grounded_by` expansion, or a model run.
- Start final-writer Call 3 only after a symbolic-result handoff contract is
  separately reviewed.
