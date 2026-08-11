# Step 8 — v2-only Scallop backend Step 4: participation and stage effects

Status: **implemented and parity-validated; no model request is authorized**
(2026-08-11).

Steps 1–3 are frozen, parity-validated case-time lowering surfaces.  Step 4
lowers two existing Python runtime surfaces only:

```text
Participation
  co-principal predicate attribution
  + constitutive-status aggregation
  + principal-realization dependency and instigator/aider requires

Stage effects
  active DoctrineDef conditions
  -> DEFEAT | MODIFY | EXEMPT stage fold
```

It does not select a participation mode, a target/source/principal instance, a
doctrine activation set, or a statutory route.  Those remain validated
orchestration inputs.  It does not yet connect the full stage chain or create a
`LiabilityResult`; that is Step 5.

## 1. Case-time identity and input boundary

All participation identities are already-existing `OffenseInstanceKey` values.
The host supplies every target, source, accessory, and principal link it intends
to evaluate.  No model and no Scallop rule chooses an actor, event, source,
mode, or linked offense.

```text
v2_participation_target(target_instance)
v2_co_principal_source(target_instance, source_instance)
v2_derivative_link(accessory_instance, principal_instance, mode)
v2_principal_realization_truth(principal_instance, truth)
```

`v2_participation_target(target_instance)` is a co-principal attribution
target anchor.  Every `v2_co_principal_source(target_instance, source_instance)`
requires the corresponding target anchor.

The host validates caller-selected participation inputs against the checked
static policy and the endpoint offense's participation constraints:

```text
v2_participation_target(T):
  co_principal is enabled for T's offense

v2_derivative_link(A, P, mode):
  mode exists in ParticipationPolicyDef and is not disabled for A's offense
```

This validates a caller choice against existing DSL semantics; neither the
host nor Scallop selects a participation mode.

`mode` is closed to `instigator | aider`.  `v2_principal_realization_truth` is
a validated case-time adapter input at Step 4.  It is the existing three-valued
`principal_realization_truth()` read of a supplied principal evaluation; Step 5
will connect the complete symbolic stage chain that produces that evaluation.
Step 4 does not reimplement or guess a principal's completion/stage result.
For every distinct `principal_instance` appearing in
`v2_derivative_link`, the host supplies exactly one
`v2_principal_realization_truth` row.  A missing realization row is not
defaulted to `UNKNOWN`, and a realization row for an instance outside the
derivative-link principal set is rejected.

The ordinary `v2_instance`, `v2_predicate_truth`, and relation EDB vocabulary
continues to carry all case facts.  Every participation link endpoint must be
in the supplied `v2_instance` universe, but that membership is necessary and
not sufficient.  Every participation target, source, accessory, and principal
must also be a caller/orchestration-authorized, independently evaluable
`OffenseInstanceKey` from the activated/compiled candidate set.  A Step 3
component-scope-only `v2_instance` cannot be a participation endpoint.
Missing predicate facts remain `UNKNOWN`, never `FALSE`.

## 2. Co-principal attribution

For an explicitly caller-selected co-principal target and source set, the
static compiler reads the existing `ParticipationPolicyDef` and
`effective_attributable_slots()`.  For every leaf ref in those compiled target
slots it derives:

```text
attributed(target, ref)
  = ANY(target's original predicate truth,
        every declared source's predicate truth for ref)
```

Only the registered attributable leaf set is emitted.  Unattributable target
predicate facts and every relation truth remain untouched.  The result is a
new case-time predicate view for subsequent lowering, exactly as
`apply_attribution()` returns a new `CaseTruths` rather than mutating input.
`v2_attributed_predicate_truth` is a sparse override relation, not a complete
`CaseTruths` predicate dump.  The effective attributed predicate view is the
original predicate view with exactly those emitted attributable refs replaced
by their derived truths.  No emitted row means no override for that ref.

For every participation target `T`, the static manifest and validated
caller-supplied source EDB determine:

```text
A(T) = static leaf refs of effective_attributable_slots(T)
C(T) = static authored constitutive_status_refs(T)
S(T) = caller-declared co-principal sources
M(T) = {T} union S(T)
```

When no `ParticipationPolicyDef` exists, the underlying attribution semantic is
a no-op: there are no participation target/source rows, all
attributed/constitutive query key sets are empty, and the effective predicate
view is the original view.  A `v2_participation_target` is invalid because
co-principal is not enabled, and a `v2_derivative_link` is invalid because no
static derivative mode or `requires` expression exists.

The participation query relations preserve their full input identity and are
validated as unordered keyed sets:

```text
v2_attributed_predicate_truth(
  target_instance, predicate_ref, truth
)

v2_constitutive_status_truth(
  target_instance, predicate_ref, truth
)

v2_constitutive_status_true_instance(
  target_instance, predicate_ref, member_instance
)

v2_derivative_elements_truth(
  accessory_instance, principal_instance, mode, truth
)

v2_derivative_requirement_truth(
  accessory_instance, principal_instance, mode, truth
)
```

Thus a caller-provided derivative link round-trips through its output; two
links for the same accessory cannot collapse merely because they share that
accessory instance.

The host validates each query as an unordered keyed set with these exact
expected keys:

```text
v2_attributed_predicate_truth:
  { (T, ref) | T is a participation target, ref in A(T) }

v2_constitutive_status_truth:
  { (T, ref) | T is a participation target, ref in C(T) }

v2_constitutive_status_true_instance:
  { (T, ref, member)
    | ref in C(T), member in M(T),
      original predicate truth(member, ref) == TRUE }

v2_derivative_elements_truth:
  { (accessory, principal, mode) | exact v2_derivative_link exists }

v2_derivative_requirement_truth:
  { (accessory, principal, mode) | exact v2_derivative_link exists }
```

Article 33 `constitutive_status_refs` are not written into that attributed
predicate view.  For each authored ref, the backend separately derives its
three-valued `ANY` over target plus sources and records the exact subset of
instances with `TRUE`.  This remains an Elements override/provenance input,
not an assertion that the target personally has the status fact.

The host validates that source lists are finite, deduplicated, case-compatible,
and caller-supplied; a source cannot become a target output by inference.

## 3. Derivative participation elements

For each validated `v2_derivative_link`, the static policy supplies the
canonical `requires` expression for its selected `instigator` or `aider` mode.
`mode.requires` is evaluated against the accessory's original case-time
predicate view supplied to the derivative route.  The co-principal sparse
attribution override from section 2 is not implicitly applied to a derivative
link.  The backend derives both distinct existing obligation truths and their
aggregate:

```text
v2_derivative_requirement_truth(accessory, principal, mode)
  = evaluate(mode.requires, accessory original predicate view)

derivative_elements_truth(accessory, principal, mode)
  = ALL(principal_realization_truth(principal),
        v2_derivative_requirement_truth(accessory, principal, mode))
```

The accessory does not rerun the principal `CompiledOffense`, does not derive a
completion state, and does not receive the principal's case facts.  The
principal dependency is the validated
`v2_principal_realization_truth(principal)` input, and the separately queried
requirement truth is the accessory's second provenance obligation.  The host
reconstructs those two `ObligationOutcome` values before it records the
aggregate raw derivative Elements truth.  Step 4 emits no derivative
`StageResult`, stage progression, or liability result.

Step 4 does not rerun or change Completion.  For a co-principal route, Step 5
must feed the effective attributed predicate view from section 2 into the
frozen Step 3 completion lowering before completion-adjusted Elements and
stage evaluation.  The direct/non-co-principal route continues to use the
original predicate view.

## 4. Active doctrine effects

The host supplies an explicit, validated active doctrine set per instance:

```text
v2_active_doctrine(instance_key, doctrine_ref)
v2_stage_effect_target(instance_key, stage)
```

Each ref must resolve to a loaded `DoctrineDef`; its authored stage and effect
must agree.  `stage` is closed to `unlawfulness | culpability | punishability`.
Every instance in `v2_active_doctrine` or `v2_stage_effect_target` must be a
caller/orchestration-authorized, independently evaluable `OffenseInstanceKey`
from the activated/compiled candidate set.  Membership in `v2_instance` alone
is insufficient: a Step 3 component-scope-only instance cannot be a doctrine
activation or stage-result target.
All checked doctrine helpers may exist in the static program.  Only doctrines
joined through `v2_active_doctrine(instance, doctrine_ref)` enter the
case-time effect fold.  An unactivated doctrine derives no effect row and has
no influence on the stage result.

For every `v2_active_doctrine(instance, doctrine_ref)`, the host requires
`v2_stage_effect_target(instance, authored_stage(doctrine_ref))`.  A stage
target may have zero active doctrines, but an active doctrine may not exist
without its corresponding stage target.

Static lowering evaluates a doctrine's canonical `requires` against the
instance predicate view.  For a co-principal target, this is the attributed
predicate view derived in section 2; otherwise it is the original predicate
view.

Step 4 exposes, for each supplied `(instance, stage)` where stage is one of
`unlawfulness | culpability | punishability`:

```text
v2_stage_effect_truth(instance, doctrine_ref, effect, truth)
v2_stage_effect_result(instance, stage, legal_state, gate_state)
```

`v2_stage_effect_result` has exactly the `v2_stage_effect_target` key set,
including targets with zero active same-stage doctrines.  This anchor is what
produces Python's ordinary preserved/passes or punishable/passes default
result rather than treating an empty active set as no stage result.
`v2_stage_effect_truth` contains exactly one `TRUE`, `FALSE`, or `UNKNOWN`
row for every active doctrine whose authored stage equals that target stage:

```text
{
  (instance, doctrine_ref)
  | v2_active_doctrine(instance, doctrine_ref)
    AND authored_stage(doctrine_ref) == target_stage
}
```

The stage fold uses every such truth.  When constructing `AppliedEffect`
provenance, the host retains only rows whose truth is not `FALSE`; this does
not suppress the required query row for a `FALSE` doctrine.
For every such row, the host also requires
`row.effect == checked DoctrineDef.effect` and verifies that the doctrine's
authored stage equals the enclosing target stage; a merely closed effect label
is not enough.

`modifier_ref` is not a case-time effect-row column.  The host joins it from
the static checked `doctrine_ref -> modifier_ref` manifest when it constructs
`AppliedEffect`; it is `None` for non-`MODIFY` effects.

The result fold is exactly
`resolve_stage()`:

```text
unlawfulness: blocking DEFEAT
culpability:  blocking DEFEAT, then MODIFY if no blocking effect
punishability:blocking EXEMPT, then MODIFY if no blocking effect
```

`ANY` over blocking effects has priority over unknown/non-blocking effects.
An `UNKNOWN` blocking effect yields `legal_state=unresolved` and
`gate_state=unresolved`.  With blocking FALSE, an `UNKNOWN MODIFY` yields
`legal_state=unresolved` but `gate_state=passes`; this legal/gate distinction
must not be collapsed.  The result vocabulary is closed exactly as follows:

```text
unlawfulness legal_state: preserved | defeated | unresolved
culpability legal_state:  preserved | defeated | diminished | unresolved
punishability legal_state: punishable | exempted | modified | unresolved
gate_state: passes | fails | unresolved
```

Step 4 has no `not_reached` state; Step 5 owns stage-chain gating.

## 5. Determinism, output validation, and parity

Static policy/doctrine refs, attributable refs, and active-set query results
are emitted in canonical sorted order.  The host validates output as unordered
keyed maps and rejects missing, duplicate, unexpected, wrong-stage, unknown
ref, or out-of-vocabulary rows.  In particular, each stage-effect-truth key
set is exactly the active, same-stage doctrine set defined in section 4, and
each row's effect equals its checked doctrine's authored effect.

Parity oracles are unchanged Python runtime functions:

| Surface | Oracle | Required cases |
|---|---|---|
| co-principal attribution | `apply_attribution()` | target/source TRUE/FALSE/UNKNOWN combinations; disabled/no-policy target rejection; no attributable slots; relation untouched |
| constitutive status | `resolve_co_principal_liability()` pre-Elements overrides | target/source ANY and exact TRUE-instance provenance |
| derivative mode | `_resolve_derivative_elements()` | principal TRUE/FALSE/UNKNOWN × own requirement TRUE/FALSE/UNKNOWN; exact per-link requirement and aggregate query keys; two-obligation provenance; original accessory view |
| stage effects | `resolve_stage()` | DEFEAT/EXEMPT TRUE and UNKNOWN; MODIFY TRUE/FALSE/UNKNOWN; blocking priority; no active doctrine |

A Scallop difference is a backend defect, not authority to alter the v2 Python
semantics.

## 6. Explicit non-goals

This contract does not authorize completion changes, a full principal stage
chain, indirect-principal Article 34 lowering, doctrine/participation
orchestration choices, `LiabilityResult`, Call 2 model work, Call 3 writer
work, a new binding abstraction, or legacy `card_status` mapping.

## Review-completion condition

Step 4 is ready for implementation only after approval of host-owned link and
active-doctrine inputs, co-principal attribution/constitutive-status boundary,
derivative dependency adapter and round-trip output identity, stage evaluation
target/effect-gate fold, the Step 5 co-principal completion-handoff invariant,
exact query contracts, and parity matrix.
