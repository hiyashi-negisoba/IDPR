"""Guard-aware scheduling of Call 2 predicate targets.

The planner used to hand Call 2 every predicate reachable from an offense's slots and its
completion policy, all at once.  A completion policy is not a flat bag of predicates: its
states are guarded by conjunctions, and once one conjunct is FALSE the rest of that guard
cannot matter.  Flattening it meant `dangerousness` was assessed on instances whose
`means_or_object_defect` was already FALSE -- an impossible attempt on facts that carry no
mistake of means or object.  The assessor answered UNKNOWN because there was nothing to
answer, and that UNKNOWN travelled all the way into the written answer as if the law were
undecided.  See docs/analysis/v2_call2_unknown_causes_ko.md.

Two separable things live here.

`live_predicate_refs` is the correctness rule: a predicate is live for an instance when
some slot expression, some state guard, or some live state's `requires` would say
something different depending on its value.  The substitution ranges over all three truth
values, not just TRUE and FALSE -- UNKNOWN is a meaning in this system, and a predicate
whose TRUE and FALSE both leave a guard UNKNOWN can still be the reason that guard is
undecided.  Asking a non-live predicate cannot change any outcome, so it is never asked.

`frontier_predicate_refs` is the scheduling rule: which of the live predicates to ask in
*this* round.  Conjuncts are read in authored order and the frontier stops at the first
one that is not yet settled, so a later conjunct is only reached once the earlier ones
have failed to kill the guard.  This is ordinary lazy conjunction, driven by the DSL's own
structure -- nothing here knows that `means_or_object_defect` gates `dangerousness`, or
that ground facts tend to come before legal elements.  A policy whose blocker is a
`legal_element` schedules identically.

The caller loops: ask the frontier, add the answers, recompute, stop when the frontier is
empty.  Because every round either learns a truth or terminates, the loop reaches a
fixpoint; `next_round_targets` takes the set already asked so that an instance Call 2
declined to answer cannot spin it.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from idpr.v2 import expressions
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue, evaluate
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime import completion as completion_mod
from idpr.v2.runtime.identity import OffenseInstanceKey

_TRUTH_VALUES: tuple[TruthValue, ...] = (TRUE, FALSE, UNKNOWN)


class TargetSchedulingError(ValueError):
    pass


def is_decisive(
    expr: expressions.CanonicalExpr, predicate_ref: str, truths: Mapping[str, TruthValue]
) -> bool:
    """Would this expression say something different if this predicate's value changed?

    Everything else in the case is held fixed and only this predicate varies, across all
    three truth values.  A two-point TRUE/FALSE comparison would call a predicate moot
    whenever both settings leave the expression UNKNOWN, which is exactly the case where
    the predicate is the reason the expression is undecided.
    """
    if predicate_ref not in expressions.canonical_leaf_refs(expr):
        return False
    outcomes = {
        evaluate(expr, {**truths, predicate_ref: value}) for value in _TRUTH_VALUES
    }
    return len(outcomes) > 1


def _candidate_refs(registry: DefinitionRegistry, compiled: CompiledOffense, policy: Any) -> tuple[str, ...]:
    """Every assessable predicate the instance could ever need, in a stable order.

    This is the old flat set.  It is the search space the two rules below narrow, not a
    plan: nothing is asked because it appears here.
    """
    refs: list[str] = []
    seen: set[str] = set()

    def add(values: Iterable[str]) -> None:
        for ref in values:
            if registry.kind_of(ref) in {"ground_fact", "legal_element"} and ref not in seen:
                seen.add(ref)
                refs.append(ref)

    for slot in expressions.SLOT_NAMES:
        add(sorted(expressions.canonical_leaf_refs(compiled.slots[slot])))
    if policy is not None:
        for state in policy.payload["states"].values():
            add(sorted(expressions.leaf_refs(state.get("when"))))
            add(sorted(expressions.leaf_refs(state.get("requires"))))
    return tuple(refs)


def _live_expressions(
    compiled: CompiledOffense, policy: Any, truths: Mapping[str, TruthValue]
) -> tuple[expressions.CanonicalExpr, ...]:
    """Expressions whose value is still capable of mattering for this instance.

    A state's `requires` is included only while that state's guard has not already gone
    FALSE: what a dead state additionally demands is not a question about this case.  The
    guards themselves always count, since they are what decides which state applies.
    """
    values: list[expressions.CanonicalExpr] = [compiled.slots[slot] for slot in expressions.SLOT_NAMES]
    if policy is not None:
        for state in policy.payload["states"].values():
            guard = expressions.canonicalize(state.get("when"))
            values.append(guard)
            if state.get("requires") is not None and evaluate(guard, truths) != FALSE:
                values.append(expressions.canonicalize(state["requires"]))
    return tuple(values)


def _compiled_and_policy(
    registry: DefinitionRegistry, offense_ref: str
) -> tuple[CompiledOffense, Any]:
    compiled = compile_offense(registry, offense_ref)
    if not isinstance(compiled, CompiledOffense):
        raise TargetSchedulingError(f"cannot compile offense {offense_ref!r}")
    return compiled, completion_mod.completion_policy_for(registry, offense_ref)


def live_predicate_refs(
    registry: DefinitionRegistry,
    instance: OffenseInstanceKey,
    truths: Mapping[str, TruthValue] = {},
    *,
    candidate_refs: Iterable[str] | None = None,
) -> tuple[str, ...]:
    """Predicates whose answer could still change something for this instance.

    `candidate_refs` restricts the search space to what the caller already decided this
    instance is in scope for.  The planner narrows targets for reasons this module has no
    view of -- predicate scoping, doctrine raising, participation -- so scheduling must
    subtract from its set, never widen it.  Left None the whole reachable set is used.
    """
    compiled, policy = _compiled_and_policy(registry, instance.offense_ref)
    live = _live_expressions(compiled, policy, truths)
    allowed = None if candidate_refs is None else set(candidate_refs)
    return tuple(
        ref
        for ref in _candidate_refs(registry, compiled, policy)
        if (allowed is None or ref in allowed)
        and any(is_decisive(expr, ref, truths) for expr in live)
    )


def _frontier_of_raw(
    expr: Mapping[str, Any] | None,
    truths: Mapping[str, TruthValue],
    *,
    settled_refs: Iterable[str] = (),
) -> frozenset[str]:
    """Refs an ALL-rooted authored expression is ready to ask about right now.

    Canonicalization holds ALL's children in a frozenset, so authored order survives only
    in the raw tree -- which is why this reads the raw form.  Conjuncts already TRUE are
    settled and contribute nothing; the walk stops after the first unsettled one, because
    a conjunct behind it cannot matter if that one turns FALSE.  A guard that is already
    FALSE contributes nothing at all.
    """
    if expr is None:
        return frozenset()
    settled = set(truths) | set(settled_refs)
    if expr["op"] != "all":
        return expressions.leaf_refs(expr) - settled
    for child in expr["args"]:
        value = evaluate(expressions.canonicalize(child), truths)
        if value == FALSE:
            return frozenset()
        if value != TRUE:
            pending = expressions.leaf_refs(child) - settled
            if pending:
                return pending
            # An assessed UNKNOWN is settled for scheduling even though it is not
            # logically TRUE.  A later conjunct can still force ALL to FALSE, so keep
            # walking instead of stranding the frontier on an unaskable value.
    return frozenset()


def frontier_predicate_refs(
    registry: DefinitionRegistry,
    instance: OffenseInstanceKey,
    truths: Mapping[str, TruthValue] = {},
    *,
    candidate_refs: Iterable[str] | None = None,
    settled_refs: Iterable[str] = (),
) -> tuple[str, ...]:
    """The live predicates worth asking in this round, in stable order.

    Slot expressions are asked in full: their leaves are the offense's own elements, and
    the compiled form carries no authored order to ladder through.  Policy guards are
    laddered, so a guard's later conjunct waits until the earlier ones have not killed it.
    """
    compiled, policy = _compiled_and_policy(registry, instance.offense_ref)
    live = _live_expressions(compiled, policy, truths)

    ready: set[str] = set()
    for slot in expressions.SLOT_NAMES:
        ready |= expressions.canonical_leaf_refs(compiled.slots[slot])
    if policy is not None:
        for state in policy.payload["states"].values():
            ready |= _frontier_of_raw(
                state.get("when"), truths, settled_refs=settled_refs
            )
            guard = expressions.canonicalize(state.get("when"))
            if state.get("requires") is not None and evaluate(guard, truths) != FALSE:
                ready |= _frontier_of_raw(
                    state["requires"], truths, settled_refs=settled_refs
                )

    allowed = None if candidate_refs is None else set(candidate_refs)
    return tuple(
        ref
        for ref in _candidate_refs(registry, compiled, policy)
        if ref in ready
        and (allowed is None or ref in allowed)
        and any(is_decisive(expr, ref, truths) for expr in live)
    )


def next_round_targets(
    registry: DefinitionRegistry,
    instances: Sequence[OffenseInstanceKey],
    truths: Mapping[OffenseInstanceKey, Mapping[str, TruthValue]],
    *,
    already_asked: Mapping[OffenseInstanceKey, Iterable[str]] = {},
    candidate_refs: Mapping[OffenseInstanceKey, Iterable[str]] | None = None,
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """One round's worth of (instance, predicate) targets, or empty at the fixpoint.

    `already_asked` is what makes the loop safe rather than merely convergent.  Normally a
    round's answers land in `truths` and the next frontier moves past them, but Call 2 can
    decline a target -- a schema failure, a dropped shard -- and without this the same
    unanswered predicate would be requested forever.

    `candidate_refs` carries the planner's own per-instance scope; see
    `live_predicate_refs`.  Scheduling only ever removes targets from it.
    """
    targets: list[tuple[OffenseInstanceKey, str]] = []
    for instance in instances:
        known = truths.get(instance) or {}
        asked = set(already_asked.get(instance) or ())
        allowed = None if candidate_refs is None else (candidate_refs.get(instance) or ())
        for ref in frontier_predicate_refs(
            registry,
            instance,
            known,
            candidate_refs=allowed,
            settled_refs=asked,
        ):
            if ref not in known and ref not in asked:
                targets.append((instance, ref))
    return tuple(targets)


__all__ = [
    "TargetSchedulingError",
    "frontier_predicate_refs",
    "is_decisive",
    "live_predicate_refs",
    "next_round_targets",
]
