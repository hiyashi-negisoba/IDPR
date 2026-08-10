# Phase 5.1 — proven architecture gaps, minimum-change design

Status: **Phase 5.1 PASS — Phase 6 may begin on instruction** (2026-08-10).

This document is the bounded follow-on to Phase 5. It does not reopen predicate
authoring, alter the sealed Gate① Master v3, or create a general cross-actor
framework. Each item below is a separately proven runtime/contract failure and
has a separately bounded change. A synthetic Phase 5 probe is evidence only;
it is never a production definition.

## Non-goals and sequencing

- Do not add a generic actor-query language, a general stage-query expression,
  or a reusable "all statutory exceptions" framework.
- Do not change a frozen predicate ID or canonical meaning. In particular, do
  not fabricate a 34조 instrumentalization predicate or use an inferred 151
  offender-status fact.
- Implement and test one concrete failure at a time. Only then assemble its
  affected production object(s).
- C-33b is **not** an architecture item: the 6C core already accepts a
  principal and derivative target with different `offense_ref`s. Its remaining
  work is a Step 7 caller/orchestration route.

```text
Phase 5 PASS
  → Phase 5.1: each proven minimum change + focused runtime test
  → affected 33 / 34 / 151 / 263 / 339 assembly
  → Phase 6: whole-registry audit
```

## C-33a — constitutive-status co-principal, without truth propagation

**Failure proved:** `apply_attribution()` performs leaf-wise `fold_any` on
every selected slot. Selecting `subject` changed the non-official target's own
`official_or_arbitrator_status` from `FALSE` to `TRUE`. That is a prohibited
claim about the target actor, not Article 33's legal effect.

**Minimum change:** add an explicit *per-offense* opt-in under
`OffenseDef.participation_constraints`, limited to listed existing
constitutive-status refs. The co-principal runtime path evaluates each listed
status as a separate `CoPrincipalConstitutiveStatusObligation` over the target
and declared co-principal instances. It records the satisfying actor in stage
provenance; it must not write the target actor's predicate truth.

- Ordinary `attributable_slots` remains conduct-only and unchanged.
- No status ref is inferred from a slot. Each affected offense must name its
  already-frozen status ref explicitly.
- When evaluating the co-principal's Elements, a status ref explicitly named
  in `participation_constraints` takes its satisfaction value from the matching
  `CoPrincipalConstitutiveStatusObligation`, not from
  `target.predicate_view`. `CaseTruths` itself remains unchanged. This is the
  required Elements junction: otherwise the target's own `FALSE` status leaf
  would still fail the slot while a separate obligation merely succeeds.
- Initial assembly target: the concrete Article 33a / Article 323 case only.
  Expanding to another status offense requires a new affected-offense decision,
  not a default policy change.

## C-34 — indirect principal, distinct from derivative participation

**Failure proved:** `instigator`/`aider` require a positive
`principal_realization_truth`. Article 34 needs a differentiated reading of the
agent's non-punishment or other-offense outcome. The policy schema has no
`indirect_principal` mode.

**Minimum change:** introduce one explicit `indirect_principal` runtime path,
not a variant flag on `resolve_derivative_liability`. Its input is the
utilised actor's `LiabilityEvaluation` (and, where applicable, the identified
other-offense evaluation), and its output is the user's direct-principal
evaluation with distinct indirect-participation provenance.

- The path must distinguish the Phase 5 cases instead of negating one Boolean:
  culpability defeat after realization; target-elements failure; unlawfulness
  defeat; and realization of a different negligence offense.
- `supervisory_relationship` is only the already-frozen Article 34(2)
  additional condition; it cannot be substituted for the un-frozen general
  utilization/instrumentality condition.
- Therefore Phase 5.1 may add and test the runtime/contract path, but may not
  author a production 34 policy until its own-condition source is separately
  traced or authorised as a canonical erratum. No new predicate is implied by
  this architecture design.

## C-151 — other actor's qualifying offense result

**Failure proved:** a Definition Layer expression is evaluated against one
`CaseTruths.predicate_view(instance)`. It has no handle to another actor's
`OffenseRealization`/`LiabilityEvaluation`.

**Minimum change:** define a dedicated Article 151 cross-instance result
obligation, keyed by the concrete person targeted by the existing
`offender_status_of_object` leaf. The runtime reads a linked other-actor
evaluation and records that linked instance/result in provenance. It is not a
new ordinary expression operator and is not available to unrelated legal
elements. During Article 151 Elements evaluation, this obligation is the truth
source for `offender_status_of_object`; leaving that leaf `UNKNOWN` and merely
adding a separately successful requirement is not permitted.

The statutory “벌금 이상” qualification cannot be inferred from the current
`statutory_refs` strings: the registry has no structured penalty metadata.
Phase 5.1 must therefore make that qualifying-offense selection an explicit
caller-supplied Article 151 input, with its legal classification recorded by
the caller. The input preserves the linked `OffenseInstanceKey` and
qualification provenance. Neither a neural/model decision nor a missing caller
qualification may become an inferred qualification: when it is absent, the
leaf remains unresolved rather than becoming `FALSE`.

## C-263 — statutory deeming without fake 공동가공

**Failure proved:** `co_principal` means actual attributable conduct and
requires participant sources; Article 263 instead requires independent acts
without mutual intent and creates a statutory deemed effect.

**Minimum change:** add a dedicated Article 263 statutory-deeming evaluation
path. It evaluates the existing Article 19 leaves
`concurrent_independent_acts`, `same_object_of_result`, and
`causal_origin_unascertained` together with the already-frozen injury result,
then emits a `StatutoryDeemingObligation` provenance record.

- It must not call `apply_attribution()`, merge conduct truths, or mark the
  actors as actual co-principals.
- The Article 263 statutory-deeming rule/path explicitly uses the result to
  produce liability for the underlying injury offense and records
  `StatutoryDeemingObligation` provenance. It does not create an
  `offense_ref=263` identity or hide the deeming in a generic
  participation-policy default.

## C-339 — component-local completion only

**Failures proved:** a completion `when` expression cannot name a COMPOSE
component (D-1), and a whole-slot suspension drops every contributor (D-2).

**Minimum change:** extend only `CompletionPolicyDef` for a direct
offense-component of a `DerivedOffenseDef`:

1. a component-local condition binds an existing `when` expression to the
   component's local-key occurrence; and
2. a component-scoped suspension names that same occurrence and its slot(s),
   leaving sibling component contributions intact.

Runtime truth lookup reuses the existing `OffenseInstanceKey`: the top-level
339 instance, component `local_key`, and component `offense_ref` identify the
component occurrence, and that component instance's `predicate_view` evaluates
`when`. No component-truth store is added, and a global `CaseTruths` predicate
truth is not reinterpreted as two different component truths. A
component-scoped suspension removes only the named `local_key`'s contribution
to its slot(s), leaving sibling contributions intact. The compiler/checker
must reject an unknown local key, a component that does not contribute the
named slot, and a component-scoped suspension outside this explicit completion
feature.

This is intentionally restricted to Art. 339's direct
`COMPOSE(offense, offense)` shape. It is not a general replacement for normal
slot suspension or ordinary completion policies.

## Step 7 handoff — C-33b only

The required future caller route is:

```text
realized principal instance (offense A)
  + actor-specific derivative target instance (offense B)
  + applicable instigator/aider own requirement
  → resolve_derivative_liability(principal=A, instance=B)
```

The Phase 5 probe already proved the core preserves `B`. Step 7 owns creating
this route from case grouping and selecting the actor-specific target; Phase
5.1 must not change `resolve_derivative_liability` for it.

## Accepted Phase 5.1 implementation constraints

- **Article 151:** the caller supplies the linked qualifying evaluation; no
  structured penalty metadata, model decision, or missing-input `FALSE`
  fallback is introduced.
- **Article 34:** implement and regress the dedicated runtime path now, but
  retain its production policy HOLD until the general
  utilization/instrumentality condition has a frozen source. Do not substitute
  `supervisory_relationship` for that condition.

## Phase 5.1 implementation record

| Concrete failure | Minimum implementation and focused proof | Production consequence |
|---|---|---|
| C-33a | `constitutive_status_refs` is an offence-local schema field. `resolve_co_principal_liability()` keeps ATTRIBUTE conduct-only, then supplies each listed subject leaf through `CoPrincipalConstitutiveStatusObligation`; `CaseTruths` is not modified. The focused test keeps the non-owner's own status `FALSE` while the co-principal's status satisfies the Elements slot. | `participation_policy.standard` and art323's `offense.obstruction_of_right_exercise.participation_constraints` are assembled. Only `legal_element.own_property_object` opts in. |
| C-151 | `resolve_article_151_liability()` alone supplies `offender_status_of_object` from a caller-provided `Article151QualifyingLink`. It preserves the linked `OffenseInstanceKey` and qualification provenance; no link or an unestablished link is `UNKNOWN`, never `FALSE`. | The frozen `legal_element.offender_status_of_object` and `offense.harboring_or_escape` are assembled. The separate relative-cohabiting-family doctrine still has no frozen condition expression and is not inferred here. |
| C-263 | `resolve_article_263_deemed_liability()` folds the three frozen Article 19 leaves and `injury_result` as a `StatutoryDeemingObligation`; it never calls ATTRIBUTE. | No `offense_ref=263` is authored. The existing underlying `offense.injury` remains the liability identity, as required. |
| C-34 | `resolve_indirect_principal_liability()` is a distinct runtime path. Its focused tests distinguish Elements failure, Unlawfulness defeat, Culpability defeat, and a caller-selected different negligence evaluation. | **No production indirect-principal policy.** The general utilization/instrumentality condition remains unfrozen; `supervisory_relationship` is not substituted. |
| C-339 | `when_component` evaluates an existing `when` expression through a component's reused `OffenseInstanceKey`. `component_suspends` evaluates/suspends only the named offense-family component contribution, retaining siblings; unknown/local-key/non-contributor/non-339 uses are checker-rejected. | The sealed 333/334/335 robbery-side candidates are assembled separately: `robbery_rape`, `special_robbery_rape`, and `quasi_robbery_rape`, each COMPOSEd with `offense.rape` and carrying its own CompletionPolicy. 336 remains coverage-only. |

Focused regressions include all three Art.339 robbery-side variants; the full
`tests/test_v2_*.py` suite passes. **Phase 5.1 PASS:** Phase 6 may begin on
instruction.
