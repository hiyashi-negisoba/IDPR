"""Host routing of raised doctrine candidates into the existing Scallop stage gates."""

from __future__ import annotations

from collections.abc import Iterable

from idpr.v2 import expressions
from idpr.v2.evaluate import FALSE, UNKNOWN, evaluate
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths


class DoctrineActivationError(ValueError):
    pass


def raised_active_doctrines(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
    candidate_doctrine_refs: Iterable[str],
    truths: CaseTruths,
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """Activate a candidate only when its authored requires has some grounded evidence.

    This does not decide the doctrine. Scallop still evaluates the full three-valued
    expression. It prevents a wholly unmentioned defense (all leaves UNKNOWN) from
    blocking every liability stage merely because Step 7 enumerated it structurally.
    """
    doctrine_refs = tuple(dict.fromkeys(candidate_doctrine_refs))
    doctrines = []
    for ref in doctrine_refs:
        entry = registry.get(ref)
        if entry is None or entry.kind != "doctrine":
            raise DoctrineActivationError(f"invalid doctrine candidate: {ref!r}")
        doctrines.append(entry)
    output: list[tuple[OffenseInstanceKey, str]] = []
    for instance in instances:
        view = truths.predicate_view(instance)
        for doctrine in doctrines:
            raw = doctrine.payload["requires"]
            leaf_refs = expressions.leaf_refs(raw)
            known = any(view.get(ref, UNKNOWN) != UNKNOWN for ref in leaf_refs)
            if not known:
                continue
            result = evaluate(expressions.canonicalize(raw), view)
            if result != FALSE:
                output.append((instance, doctrine.id))
    return tuple(output)


__all__ = ["DoctrineActivationError", "raised_active_doctrines"]
