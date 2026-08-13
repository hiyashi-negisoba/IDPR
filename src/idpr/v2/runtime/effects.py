"""Doctrine effect application at one stage (build-order step 6A).

Two things this module deliberately does NOT do:

1. **It does not consume the whole doctrine registry.** `DoctrineDef` is not hard-linked from
   `OffenseDef` (that is intentional -- justification and excuse doctrines are General Part, shared
   across offenses), but "not hard-linked" is a different claim from "evaluate all of them at case
   time". Evaluating every unprobed doctrine would leave most of them UNKNOWN, and a single UNKNOWN
   DEFEAT drags the stage to `unresolved` -- so a plain theft case would come out with unresolved
   Unlawfulness because nobody proved 긴급피난 false. The caller supplies an activated set instead;
   step 7 (closure/probe) will be what computes it.

2. **It does not decide per doctrine.** The stage's state is a fold over the whole active pool. A
   confirmed DEFEAT settles the stage regardless of how many other justifications remain UNKNOWN --
   `self_defense=TRUE, necessity=UNKNOWN` is `defeated`, not `unresolved`. That is exactly
   three-valued ANY, so `evaluate.fold_any` is reused rather than rewritten here.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from idpr.v2 import expressions
from idpr.v2.evaluate import FALSE, TRUE, TruthValue, evaluate, fold_any
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import AppliedEffect, GateState, StageResult
from idpr.v2.runtime.truths import CaseTruths

ActiveDoctrineRefs = frozenset
"""The doctrine ids activated for this case. Step 6A callers build it explicitly; step 7's closure
/probe compiler will produce it from the seeded offenses' structure."""

_BLOCKING_EFFECT: Mapping[str, str] = {
    "unlawfulness": "DEFEAT",
    "culpability": "DEFEAT",
    "punishability": "EXEMPT",
}

_BLOCKED_STATE: Mapping[str, str] = {
    "unlawfulness": "defeated",
    "culpability": "defeated",
    "punishability": "exempted",
}

_OPEN_STATE: Mapping[str, str] = {
    "unlawfulness": "preserved",
    "culpability": "preserved",
    "punishability": "punishable",
}

_MODIFIED_STATE: Mapping[str, str] = {
    "culpability": "diminished",
    "punishability": "modified",
}


class StageEffectError(ValueError):
    """A doctrine was applied at a stage it does not belong to, or an active ref is not a doctrine.

    Raised rather than asserted: v2.1.0 section 24 requires a stage effect landing on the wrong
    stage to be an error, and an `assert` disappears under `python -O`.
    """


def resolve_stage(
    stage: str,
    active: ActiveDoctrineRefs,
    registry: DefinitionRegistry,
    instance: OffenseInstanceKey,
    truths: CaseTruths,
) -> StageResult:
    """Evaluate one doctrine-bearing stage against the activated doctrine set."""
    return resolve_stage_from_predicate_view(
        stage,
        active,
        registry,
        truths.predicate_view(instance),
    )


def resolve_stage_from_predicate_view(
    stage: str,
    active: ActiveDoctrineRefs,
    registry: DefinitionRegistry,
    predicate_view: Mapping[str, TruthValue],
) -> StageResult:
    """Evaluate a stage from an explicitly supplied predicate namespace.

    The ordinary liability path supplies an ``OffenseInstanceKey``-scoped ``CaseTruths`` view via
    :func:`resolve_stage`.  Internal factual-participant evaluation has no liable-actor instance
    and must not fabricate one, so it uses this identity-neutral entry point.  Both paths share the
    same doctrine fold and stage truth table.
    """
    if stage not in _BLOCKING_EFFECT:
        raise StageEffectError(
            f"{stage!r} is not a doctrine-bearing stage; doctrines attach only to "
            f"{sorted(_BLOCKING_EFFECT)} (section 12.1 excludes elements)"
        )

    applied = tuple(_evaluate_active(stage, active, registry, predicate_view))
    blocking_kind = _BLOCKING_EFFECT[stage]

    blocking = fold_any(e.truth for e in applied if e.effect == blocking_kind)
    legal_state, gate_state = _fold_stage(stage, blocking, applied)

    return StageResult(
        evaluation_state="evaluated",
        legal_state=legal_state,
        gate_state=gate_state,
        effects=tuple(e for e in applied if e.truth != FALSE),
    )


def _fold_stage(
    stage: str, blocking: TruthValue, applied: tuple[AppliedEffect, ...]
) -> tuple[str, GateState]:
    """The one place the legal-state x gate-state table lives.

    The MODIFY row is the subtle one: an UNKNOWN MODIFY leaves the legal state genuinely unknown
    (preserved or diminished -- unresolved), but does NOT close the gate, because section 13.2
    treats preserved and diminished identically for establishment. An UNKNOWN blocking effect
    (DEFEAT/EXEMPT) does close it, because that one would change the outcome.
    """
    if blocking == TRUE:
        return _BLOCKED_STATE[stage], "fails"
    if blocking != FALSE:
        return "unresolved", "unresolved"

    if stage not in _MODIFIED_STATE:
        return _OPEN_STATE[stage], "passes"

    modify = fold_any(e.truth for e in applied if e.effect == "MODIFY")
    if modify == TRUE:
        return _MODIFIED_STATE[stage], "passes"
    if modify == FALSE:
        return _OPEN_STATE[stage], "passes"
    return "unresolved", "passes"


def _evaluate_active(
    stage: str,
    active: ActiveDoctrineRefs,
    registry: DefinitionRegistry,
    predicate_view: Mapping[str, TruthValue],
) -> Iterable[AppliedEffect]:
    for ref in sorted(active):
        entry = registry.get(ref)
        if entry is None or entry.kind != "doctrine":
            raise StageEffectError(
                f"active doctrine ref {ref!r} does not resolve to a DoctrineDef "
                f"(got kind={None if entry is None else entry.kind!r})"
            )
        if entry.payload["stage"] != stage:
            continue

        effect = entry.payload["effect"]
        if effect["stage"] != entry.payload["stage"]:
            raise StageEffectError(
                f"doctrine {ref!r} declares stage={entry.payload['stage']!r} but its effect "
                f"targets stage={effect['stage']!r}"
            )

        yield AppliedEffect(
            doctrine_ref=ref,
            effect=effect["effect"],
            stage=stage,
            modifier_ref=effect.get("modifier_ref"),
            truth=evaluate(expressions.canonicalize(entry.payload["requires"]), predicate_view),
        )
