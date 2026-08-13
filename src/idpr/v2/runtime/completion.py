"""Completion resolution (build-order step 6B) -- v2.1.0 section 14, v2.2.0 section 19.

Completion answers one question about one offense instance:

    CompletionPolicyDef + case truths  ->  CompletionResult

It is NOT a chooser among programs. An earlier draft modelled each completion form as a separate
executable program (`FormProgram`) and left "which form is selected?" as an open problem; the 7th
addendum removed that layer. The reason it had to go is not tidiness -- it was unsound. An attempt
program has no result/causation obligation, so it *also* passes on a completed case, which means
any selection rule would have to break the tie, and every natural tie-break ("check completed
first, fall back to attempt") is precisely the `completed failed -> attach attempt label` pattern
section 14 forbids.

What replaces it: every state declares its own `when` condition over case truths, and the state is
derived from the SET of conditions that hold. Two properties follow by construction:

1. `attempted.when` never reads `completed`'s evaluation result -- both read only case truths --
   so no state can ever be reached as a fallback from another state's failure.
2. There is no ordering anywhere in this module. `_derive_state` looks at set cardinalities, and
   the states are symmetric under permutation.

Exclusivity between states is an authoring obligation (see the fixture: 상해미수 and 불능범 are
kept disjoint by an explicit `NOT(impossibility_without_danger)` conjunct, not by ranking). When
authoring fails and two conditions hold at once, the runtime says `unresolved` and records both in
provenance -- it does not pick a winner.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from idpr.v2 import expressions
from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import TRUE, UNKNOWN, TruthValue, evaluate
from idpr.v2.expressions import CanonicalExpr
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.relations import RelationInstanceKey, iter_relation_instances
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

CompletionState = Literal[
    "completed",
    "attempted",
    "abandoned_attempt",
    "impossible_attempt",
    "preparation",
    "unresolved",
    "not_applicable",
]

DERIVABLE_STATES: tuple[str, ...] = (
    "completed",
    "attempted",
    "abandoned_attempt",
    "impossible_attempt",
    "preparation",
)
"""The five states a CompletionPolicyDef can declare (schema `states` keys). `unresolved` and
`not_applicable` are runtime outcomes of the derivation, never authored."""

RelationDisposition = Literal["retain", "suspend"]


@dataclass(frozen=True)
class CompletionCandidateOutcome:
    """One declared state's `when` condition and how it evaluated.

    Section 14.2's `decisive_conditions`. Every declared state appears, including the FALSE ones:
    "why is this unresolved?" is answerable only if the conditions that did *not* hold are on the
    record too.
    """

    state: str
    truth: TruthValue
    component_instance: OffenseInstanceKey | None = None
    """The component predicate view used by `when_component`, if this state has one."""


@dataclass(frozen=True)
class CompletionResult:
    """The completion judgement for one offense instance.

    Note what is absent: any reference to a "selected" program, and any alternative that was
    considered and rejected. This is a legal result, not a search trace.
    """

    state: CompletionState

    punishable: bool | None = None
    """Whether this completion state is a punishable legal shape at all (형태의 문제). `None` when
    no state was derived. Distinct from the Punishability stage's EXEMPT (효과의 문제): that asks
    whether an established offense carries an exemption."""

    suspended_slots: frozenset[str] = frozenset()
    """Slots whose obligation does not exist in this state. The runtime drops them from the fold --
    it never substitutes TRUE, so a FALSE result is never laundered into a satisfied element."""

    component_suspended_slots: Mapping[str, frozenset[str]] = field(default_factory=dict)
    """Article 339-only removals keyed by top-level component local_key.

    Unlike `suspended_slots`, these remove only that occurrence's contribution while retaining
    sibling contributions to the same flattened slot.
    """

    relation_dispositions: Mapping[RelationInstanceKey, RelationDisposition] = field(
        default_factory=dict
    )
    """Keyed by the DEFINITION-occurrence key, not the runtime one: this mapping comes from
    `CompletionPolicyDef + CompiledOffense` and knows nothing about the case. Only the resulting
    `RelationObligation` is case-scoped."""

    additional_requirements: CanonicalExpr = None
    """This state's own `requires`, canonicalized. Added to the fold; never replaces anything."""

    additional_requirements_instance: OffenseInstanceKey | None = None
    """The direct component view for `requires` when the state has `when_component`."""

    provenance: tuple[CompletionCandidateOutcome, ...] = ()

    def __post_init__(self) -> None:
        """A state that was not derived cannot carry a program.

        Without this, `CompletionResult("unresolved", suspended_slots={"result"})` constructs
        happily and the pipeline would suspend obligations on the authority of a judgement that was
        never reached -- an attempt program for an attempt nobody established. Same discipline as
        `StageResult.__post_init__`: the invariant is enforced, not commented.
        """
        if self.state in ("unresolved", "not_applicable"):
            carried = (
                self.punishable is not None
                or self.suspended_slots
                or self.component_suspended_slots
                or self.relation_dispositions
                or self.additional_requirements is not None
                or self.additional_requirements_instance is not None
            )
            if carried:
                raise ValueError(
                    f"CompletionResult invariant violated: state={self.state!r} carries a program "
                    f"(punishable={self.punishable!r}, suspended_slots={set(self.suspended_slots)!r}, "
                    f"component_suspended_slots={dict(self.component_suspended_slots)!r}, "
                    f"relation_dispositions={dict(self.relation_dispositions)!r}, "
                    f"additional_requirements={self.additional_requirements!r}, "
                    f"additional_requirements_instance={self.additional_requirements_instance!r}) -- no state was "
                    "derived, so there are no obligations to suspend or add"
                )
        elif self.punishable is None:
            raise ValueError(
                f"CompletionResult invariant violated: derived state {self.state!r} has "
                "punishable=None -- every declared state authors `punishable`"
            )


def completion_policy_for(registry: DefinitionRegistry, offense_ref: str) -> DefinitionEntry | None:
    """The CompletionPolicyDef governing `offense_ref`, or None if the offense has none.

    Policies point at offenses (`policy.offense`), not the other way round -- section 14 keeps
    Completion orthogonal, so `OffenseDef` carries no back-reference to hard-link. Two policies
    claiming one offense is an authoring defect that axis 8 reports; this returns the first match
    rather than guessing, since by the time the runtime runs, the checks have passed.
    """
    for entry in registry.by_kind.get("completion_policy", ()):
        if entry.payload["offense"] == offense_ref:
            return entry
    return None


def resolve_completion(
    policy: DefinitionEntry | None,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    truths: CaseTruths,
) -> CompletionResult:
    """Derive this instance's completion state from the policy's conditions and the case truths.

    `policy=None` means the offense has no CompletionPolicyDef at all. That is the ordinary case
    for most offenses, and it resolves to `completed` with no suspensions -- not to
    `not_applicable`. An offense without a completion policy is not an offense with no completion
    state; it is one for which only the completed shape is defined.

    Assumes an already type-checked registry (axis 8 clean), exactly as `evaluate()` and
    `evaluate_compiled_offense()` assume their axes have run.
    """
    if policy is None:
        return CompletionResult(state="completed", punishable=True)

    states = policy.payload["states"]
    outcomes = tuple(
        _resolve_candidate(states[name], name, compiled, instance, truths)
        for name in DERIVABLE_STATES
        if name in states
    )

    state = _derive_state(outcomes)
    if state in ("unresolved", "not_applicable"):
        return CompletionResult(state=state, provenance=outcomes)

    policy_for_state = states[state]
    candidate = next(outcome for outcome in outcomes if outcome.state == state)
    return CompletionResult(
        state=state,
        punishable=policy_for_state["punishable"],
        suspended_slots=frozenset(policy_for_state.get("suspends") or ()),
        component_suspended_slots=_resolve_component_suspensions(policy_for_state),
        relation_dispositions=_resolve_dispositions(compiled, policy_for_state),
        additional_requirements=expressions.canonicalize(policy_for_state.get("requires")),
        additional_requirements_instance=candidate.component_instance,
        provenance=outcomes,
    )


def component_instance_for(
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    local_key: str,
    offense_ref: str,
) -> OffenseInstanceKey:
    """Reuse OffenseInstanceKey for the one approved component occurrence namespace.

    This is deliberately restricted to an offense-family component (an OffenseDef or existing
    DerivedOffenseDef).  The completion checker rejects other shapes before runtime; the
    ValueError remains a defensive boundary for callers that bypass type checking.
    """
    component = next((item for item in compiled.components if item.local_key == local_key), None)
    if (
        component is None
        or component.component_kind != "offense"
        or component.resolved_kind not in ("offense", "derived_offense")
        or component.source_ref != offense_ref
    ):
        raise ValueError(
            f"component scope ({local_key!r}, {offense_ref!r}) is not an offense-family component "
            f"of {compiled.id!r}"
        )
    return OffenseInstanceKey(
        case_id=instance.case_id,
        actor_id=instance.actor_id,
        offense_ref=offense_ref,
        occurrence_id=instance.occurrence_id,
    )


def _resolve_candidate(
    state_policy: Mapping[str, object],
    state: str,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    truths: CaseTruths,
) -> CompletionCandidateOutcome:
    scope = state_policy.get("when_component")
    component_instance = None
    if scope:
        component_instance = component_instance_for(
            compiled, instance, scope["local_key"], scope["offense"]
        )
        predicate_view = truths.predicate_view(component_instance)
    else:
        predicate_view = truths.predicate_view(instance)
    return CompletionCandidateOutcome(
        state=state,
        truth=evaluate(expressions.canonicalize(state_policy["when"]), predicate_view),
        component_instance=component_instance,
    )


def _resolve_component_suspensions(state_policy: Mapping[str, object]) -> dict[str, frozenset[str]]:
    """Turn authored Art.339 component suspensions into the runtime's local-key map."""
    return {
        item["local_key"]: frozenset(item["slots"])
        for item in state_policy.get("component_suspends") or ()
    }


def expression_after_component_suspensions(
    compiled: CompiledOffense,
    slot: str,
    component_suspensions: Mapping[str, frozenset[str]],
) -> CanonicalExpr:
    """Remove explicitly suspended offense-component conjuncts from one merged slot.

    This is used only for mixed direct COMPOSE offenses, where primitive/bundle components do not
    have their own predicate view.  Compilation assembles component contributions with ALL; a
    suspension must therefore match one exact compiled conjunct.  Anything else is rejected rather
    than approximated.
    """

    expression = compiled.slots.get(slot)
    removals: list[CanonicalExpr] = []
    for local_key, slots in component_suspensions.items():
        if slot not in slots:
            continue
        component = next(
            (value for value in compiled.components if value.local_key == local_key), None
        )
        if (
            component is None
            or component.component_kind != "offense"
            or component.resolved_kind not in ("offense", "derived_offense")
        ):
            raise ValueError("component suspension endpoint is not offense-family")
        removal = component.compiled_content.slots.get(slot)
        if removal is None:
            raise ValueError("component suspension has no contribution to its slot")
        removals.append(removal)
    for removal in removals:
        if expression == removal:
            expression = None
            continue
        if not (isinstance(expression, tuple) and expression[0] == "all"):
            raise ValueError("component suspension does not match a merged ALL conjunct")
        children = set(expression[1])
        if removal not in children:
            raise ValueError("component suspension conjunct is absent from merged slot")
        children.remove(removal)
        expression = expressions.combine_all(*children)
    return expression


def _derive_state(outcomes: tuple[CompletionCandidateOutcome, ...]) -> CompletionState:
    """Set cardinalities only -- no ordering, no priority, no fallback.

        |T| == 1          -> that state          (regardless of U: a confirmed state is decided)
        |T| >= 2          -> unresolved          (authoring defect; never broken by ranking)
        |T| == 0, U != {} -> unresolved
        |T| == 0, U == {} -> not_applicable

    `|T| == 1` deciding despite outstanding UNKNOWNs is the same three-valued principle already
    fixed for doctrine pools in step 6A: a confirmed conclusion terminates regardless of what else
    is unresolved. It is not a priority order -- it ranks *confirmation*, not states, and is
    symmetric under permuting them. The conservative alternative (any UNKNOWN -> unresolved) would
    collapse ordinary completed cases to `unresolved` the moment an evaluative predicate like
    위험성 was unassessed, which is the failure mode step 6A's first draft had.
    """
    true_states = [outcome.state for outcome in outcomes if outcome.truth == TRUE]
    if len(true_states) == 1:
        return true_states[0]  # type: ignore[return-value]
    if len(true_states) > 1:
        return "unresolved"
    if any(outcome.truth == UNKNOWN for outcome in outcomes):
        return "unresolved"
    return "not_applicable"


def _resolve_dispositions(
    compiled: CompiledOffense, policy_for_state: Mapping[str, object]
) -> dict[RelationInstanceKey, RelationDisposition]:
    """Match authored dispositions onto this offense's actual relation instances.

    Resolution goes through `iter_relation_instances()` -- the same enumeration Step 5 defined and
    the runtime folds over -- rather than re-walking the derivation tree here. Unmatched or
    ambiguous entries are axis 8's business (`checks/completion.py`); this function assumes the
    policy passed that check and simply keys what it was given. Anything not mentioned is retained,
    which is safe *because* axis 8 requires full coverage whenever `suspends` is non-empty.
    """
    authored = policy_for_state.get("relations") or ()
    if not authored:
        return {}

    by_signature = {
        (key.occurrence_path[1:], key.relation_ref, key.left_local_key, key.right_local_key): key
        for key, _binding in iter_relation_instances(compiled)
    }
    dispositions: dict[RelationInstanceKey, RelationDisposition] = {}
    for entry in authored:  # type: ignore[union-attr]
        signature = (
            tuple(entry.get("path") or ()),
            entry["relation"],
            entry["left"],
            entry["right"],
        )
        key = by_signature.get(signature)
        if key is not None:
            dispositions[key] = entry["disposition"]
    return dispositions


__all__ = [
    "DERIVABLE_STATES",
    "CompletionCandidateOutcome",
    "CompletionResult",
    "CompletionState",
    "RelationDisposition",
    "completion_policy_for",
    "component_instance_for",
    "expression_after_component_suspensions",
    "resolve_completion",
]
