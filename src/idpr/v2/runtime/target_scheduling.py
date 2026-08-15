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

Both rules narrow the planner's own target set and never widen it, and narrowing needs a
reason this module can state.  Predicates it has no expression for -- doctrine leaves,
participation mode requirements -- are not moot, they are unmodelled, and they pass
through untouched.  Neither is a predicate this offence *does* model when some other
producer opened it too: liveness then speaks only for the offence.  See `unprunable_refs`,
and `target_openers` for how a target's openers are read.

The caller loops: ask the frontier, add the answers, recompute, stop when the frontier is
empty.  Because every round either learns a truth or terminates, the loop reaches a
fixpoint; `next_round_targets` takes the set already asked so that an instance Call 2
declined to answer cannot spin it.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping, Sequence
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
            # A blocker is a predicate like any other: it only defeats a state once it is
            # TRUE, which is a thing this case has to be asked about.  Leaving it out of
            # the search space made every `blocked_when` permanently UNKNOWN, and an
            # UNKNOWN blocker blocks nothing -- fail-open, silently.
            add(sorted(expressions.leaf_refs(state.get("blocked_when"))))
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
            if evaluate(guard, truths) == FALSE:
                continue
            if state.get("requires") is not None:
                values.append(expressions.canonicalize(state["requires"]))
            if state.get("blocked_when") is not None:
                values.append(expressions.canonicalize(state["blocked_when"]))
    return tuple(values)


#: `opened_by` values whose targets are ordinary offence elements -- the need they express
#: *is* the offence's slots and completion policy, which is exactly what this module reads.
#: Only these may be pruned for non-decisiveness.
#:
#: The empty entries are the base evaluation planner, which writes no `opened_by` at all.
#: Every other opener, **including one that does not exist yet**, is presumed to carry a
#: requirement this module cannot see.  That default is the point: a new producer is
#: protected before anyone remembers to add it here, and the failure mode of the old code
#: was precisely a producer this module had never heard of.
ELEMENT_DERIVED_OPENERS = frozenset(
    {"", "unspecified", "post_participation_derived_group"}
)

#: 이미 있는 target을 재사용하는 producer가 자기 이름을 덧붙이는 자리.
#:
#: `opened_by` 하나로는 겹침을 표현할 수 없다. doctrine이 필요로 하는 leaf가 마침 그 죄의
#: 일반 요소이기도 하면 doctrine 빌더는 새 target을 만들지 않고 기존 것을 쓰는데, 그러면
#: 행에는 `unspecified` 하나만 남아 doctrine이 그것을 필요로 한다는 사실이 사라진다. 그 뒤
#: scheduler는 죄 쪽 사정만 보고 지워도 된다고 판단한다 -- 개방 이유를 넘기기로 한 수정이
#: producer 쪽에서 무효가 되는 자리다.
ALSO_OPENED_BY_KEY = "also_opened_by"


def target_openers(raw_target: Mapping[str, Any]) -> frozenset[str]:
    """이 target을 연 producer 전부. 하나를 골라 쓰지 않는다."""
    openers = {str(raw_target.get("opened_by") or "unspecified")}
    extra = raw_target.get(ALSO_OPENED_BY_KEY) or ()
    if isinstance(extra, (list, tuple)):
        openers |= {str(value) for value in extra if value}
    return frozenset(openers)


def is_externally_opened(raw_target: Mapping[str, Any]) -> bool:
    """이 target을 연 producer 중 하나라도 이 모듈이 모르는 요구를 싣고 있는가."""
    return bool(target_openers(raw_target) - ELEMENT_DERIVED_OPENERS)


def merge_target_opener(raw_target: MutableMapping[str, Any], opener: str) -> bool:
    """이 target을 연 producer를 하나 더 기록한다. 새로 기록했으면 참.

    producer가 이미 있는 `(instance, predicate_ref)`를 재사용할 때 부른다. 행을 새로 만들지
    않는 것과 그 이유를 남기지 않는 것은 다르다 -- 남기지 않으면 그 target은 하류에서 죄의
    일반 요소로만 보이고, 이 죄가 더 이상 그것을 필요로 하지 않게 된 순간 지워진다. 재사용을
    `continue` 한 줄로 처리한 producer가 둘 있었고 둘 다 같은 구멍이었다.
    """
    if opener == str(raw_target.get("opened_by") or "unspecified"):
        return False
    openers = list(raw_target.get(ALSO_OPENED_BY_KEY) or ())
    if opener in openers:
        return False
    openers.append(opener)
    raw_target[ALSO_OPENED_BY_KEY] = openers
    return True


def unprunable_refs(
    allowed: set[str] | None,
    modelled: Sequence[str],
    external_refs: Iterable[str] = (),
) -> tuple[str, ...]:
    """Planned targets this module may not drop, in stable order.

    Scheduling may only *remove* a planned target, and only for a reason it can state: an
    expression of this offence that says the same thing whatever the answer.  Two kinds of
    target are outside that reason.

    A predicate that appears in no such expression is not moot -- it is outside what this
    module models.  The doctrine leaves and the `participation_mode_requirement` targets
    are exactly that: opened from a DoctrineDef or a participation mode, neither reachable
    from an offence's slots or its completion policy.  Dropping them was the participation
    defect all over again -- `instigator_intent` had a target and a carrier, the scheduler
    intersected it away, and Kleene left every accessory permanently UNKNOWN.

    `external_refs` is the subtler half.  A predicate can be opened by an external producer
    **and** appear in this offence's own expressions.  Then it is modelled, so liveness has
    an opinion about it -- but that opinion is only about the offence.  The doctrine that
    also needs it may still need it once the offence stops caring, and pruning on the
    offence's say-so silently answers for a producer that was never asked.  Whoever knows
    the opener tells us; here we only refuse to drop it.
    """
    if allowed is None:
        return ()
    external = allowed & set(external_refs)
    return tuple(sorted((allowed - set(modelled)) | external))


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
    external_refs: Iterable[str] = (),
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
    modelled = _candidate_refs(registry, compiled, policy)
    return tuple(
        ref
        for ref in modelled
        if (allowed is None or ref in allowed)
        and any(is_decisive(expr, ref, truths) for expr in live)
    ) + unprunable_refs(allowed, modelled, external_refs)


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
            # 이 conjunct는 물어봤는데 UNKNOWN으로 왔다. 논리적으로는 뒤 conjunct가 FALSE로
            # 와서 ALL을 죽일 수 있으므로 예전에는 계속 걸어갔다. 2026-08-16 측정은 그
            # 가능성이 실현되지 않는다고 답했다 -- `dangerousness`는 upstream
            # `means_or_object_defect`가 UNKNOWN인 채로 14번 열렸고 FALSE는 0번,
            # UNKNOWN이 13번, TRUE가 1번(그나마 defect 없이는 불능미수에 쓸 수 없는 값)이었다.
            # 답할 수 없는 질문을 묻는 대가로 UNKNOWN만 얻는다. 여기서 멈춘다.
            return frozenset()
    return frozenset()


def frontier_predicate_refs(
    registry: DefinitionRegistry,
    instance: OffenseInstanceKey,
    truths: Mapping[str, TruthValue] = {},
    *,
    candidate_refs: Iterable[str] | None = None,
    settled_refs: Iterable[str] = (),
    external_refs: Iterable[str] = (),
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
            if evaluate(guard, truths) == FALSE:
                continue
            if state.get("requires") is not None:
                ready |= _frontier_of_raw(
                    state["requires"], truths, settled_refs=settled_refs
                )
            # A blocker is not laddered behind `requires`: it defeats the state on its own
            # and is asked as soon as the state is live at all.
            if state.get("blocked_when") is not None:
                ready |= _frontier_of_raw(
                    state["blocked_when"], truths, settled_refs=settled_refs
                )

    allowed = None if candidate_refs is None else set(candidate_refs)
    modelled = _candidate_refs(registry, compiled, policy)
    return tuple(
        ref
        for ref in modelled
        if ref in ready
        and (allowed is None or ref in allowed)
        and any(is_decisive(expr, ref, truths) for expr in live)
    ) + unprunable_refs(allowed, modelled, external_refs)


def next_round_targets(
    registry: DefinitionRegistry,
    instances: Sequence[OffenseInstanceKey],
    truths: Mapping[OffenseInstanceKey, Mapping[str, TruthValue]],
    *,
    already_asked: Mapping[OffenseInstanceKey, Iterable[str]] = {},
    candidate_refs: Mapping[OffenseInstanceKey, Iterable[str]] | None = None,
    external_refs: Mapping[OffenseInstanceKey, Iterable[str]] = {},
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """One round's worth of (instance, predicate) targets, or empty at the fixpoint.

    `already_asked` is what makes the loop safe rather than merely convergent.  Normally a
    round's answers land in `truths` and the next frontier moves past them, but Call 2 can
    decline a target -- a schema failure, a dropped shard -- and without this the same
    unanswered predicate would be requested forever.

    `candidate_refs` carries the planner's own per-instance scope; see
    `live_predicate_refs`.  Scheduling only ever removes targets from it.

    `external_refs` names, per instance, the refs some producer other than the offence's
    own elements opened.  Those are never pruned -- see `unprunable_refs`.
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
            external_refs=external_refs.get(instance) or (),
        ):
            if ref not in known and ref not in asked:
                targets.append((instance, ref))
    return tuple(targets)


__all__ = [
    "ALSO_OPENED_BY_KEY",
    "TargetSchedulingError",
    "frontier_predicate_refs",
    "is_decisive",
    "live_predicate_refs",
    "ELEMENT_DERIVED_OPENERS",
    "is_externally_opened",
    "merge_target_opener",
    "next_round_targets",
    "target_openers",
    "unprunable_refs",
]
