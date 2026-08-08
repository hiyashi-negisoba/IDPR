"""Relation evaluator (build-order step 5, second half) -- the last piece of v2.1.0 execution.

What this module does and does NOT do, because the name invites the wrong reading:

    evaluate_relation() does NOT decide whether causal_nexus holds in some case. It LOOKS UP an
    already-supplied relation truth, defaulting to UNKNOWN.

Producing those truths is v2.2.0's job: structural relations (same_actor, temporal_order --
section 10.1) get resolved from entity/event binding by the case runtime, evaluative ones
(causal_nexus, foreseeability -- section 10.2) get routed to neural LegalElementAssessment. What
v2.1.0 completes here is the executable program those truths feed:

    predicate truths + relation truths + CompiledOffense  ->  TRUE / FALSE / UNKNOWN

Deliberately absent: ElementsState / OffenseRealization / any stage object (sections 12-13). Those
are runtime stage objects, build-order step 6. This layer returns a bare TruthValue.

Two structural points that are easy to get wrong, both fixed here by construction:

1. Relation identity carries the full occurrence PATH, not just the defining offense's id. Step 4
   went to real trouble to keep two occurrences of the same definition distinct (same ref, two
   local_keys -> two CompiledComponentInstances). Keying relation truths by
   (defining offense id, relation, left local_key, right local_key) would throw that away again:
   compose the same DerivedX twice, and both occurrences' internal relation collapses to one key,
   so one supplied truth would silently answer for both. RelationInstanceKey.occurrence_path
   distinguishes them. Note this is *definition*-occurrence identity only -- case/actor namespacing
   is step 6+.

2. Slots are evaluated exactly once, at the top. A nested offense component's slots were already
   folded into the parent's `slots` by the compiler, so re-entering the nested CompiledOffense to
   evaluate it whole would evaluate those slots a second time. What the nested component does still
   own -- and what the parent's flattened slots genuinely lose -- is its own relation obligations.
   So: slots once, relations recursively.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Mapping

from idpr.v2 import evaluate as evaluate_mod
from idpr.v2.compile import CompiledOffense, CompiledRelationBinding
from idpr.v2.evaluate import UNKNOWN, TruthValue
from idpr.v2.expressions import SLOT_NAMES

_OFFENSE_KINDS = ("offense", "derived_offense")


@dataclass(frozen=True)
class RelationInstanceKey:
    """Identifies one relation obligation at one place in a compiled derivation tree.

    Hashable by construction (frozen, only str/tuple fields), so it is used directly as a mapping
    key -- no string formatting, no separator-collision surface.
    """

    occurrence_path: tuple[str, ...]
    """(top-level CompiledOffense.id, *local_keys traversed) down to the offense whose OWN
    `relations` this binding belongs to. The local_key chain -- not the definition ids -- is what
    keeps two occurrences of the same definition apart."""

    relation_ref: str
    left_local_key: str
    right_local_key: str


def iter_relation_instances(
    compiled: CompiledOffense,
) -> Iterator[tuple[RelationInstanceKey, CompiledRelationBinding]]:
    """Every relation obligation `compiled` carries: its own, plus those preserved inside nested
    offense-kind components, each paired with its path-qualified key.

    Plain recursion, no cycle guard: a cyclic derivation never yields a CompiledOffense in the first
    place (compile_offense returns DerivationCycle), so any tree reachable here is finite.
    """
    yield from _walk(compiled, (compiled.id,))


def _walk(
    compiled: CompiledOffense, path: tuple[str, ...],
) -> Iterator[tuple[RelationInstanceKey, CompiledRelationBinding]]:
    for binding in compiled.relations:
        key = RelationInstanceKey(
            occurrence_path=path,
            relation_ref=binding.relation_ref,
            left_local_key=binding.left.local_key,
            right_local_key=binding.right.local_key,
        )
        yield key, binding
    for component in compiled.components:
        if component.resolved_kind in _OFFENSE_KINDS:
            yield from _walk(component.compiled_content, path + (component.local_key,))


def evaluate_relation(
    key: RelationInstanceKey, relation_truths: Mapping[RelationInstanceKey, TruthValue],
) -> TruthValue:
    """Look up one relation obligation's supplied truth. Absent -> UNKNOWN, per section 4.3:
    missing evidence is not negation. This is a lookup, not a judgement -- see module docstring."""
    return relation_truths.get(key, UNKNOWN)


def evaluate_compiled_offense(
    compiled: CompiledOffense,
    truths: Mapping[str, TruthValue],
    relation_truths: Mapping[RelationInstanceKey, TruthValue],
) -> TruthValue:
    """Whether this compiled offense's element requirements are met: all slots AND every relation
    obligation in the derivation tree.

    Assumes an already type-checked registry (checks.run_type_checks clean), exactly as
    evaluate.evaluate() assumes axis 1 has guaranteed structural soundness -- no re-validation of
    relation lowering happens here.
    """
    return evaluate_mod.fold_all([
        _evaluate_all_slots(compiled, truths),
        evaluate_mod.fold_all(
            evaluate_relation(key, relation_truths) for key, _ in iter_relation_instances(compiled)
        ),
    ])


def _evaluate_all_slots(compiled: CompiledOffense, truths: Mapping[str, TruthValue]) -> TruthValue:
    return evaluate_mod.fold_all(
        evaluate_mod.evaluate(compiled.slots.get(slot), truths) for slot in SLOT_NAMES
    )
