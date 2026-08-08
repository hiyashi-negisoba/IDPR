"""Axis 2: operator typing.

flattened_elements must be exactly what `derivation` implies -- full semantic equality via
recursive replay, not a leaf-ref superset check (a superset check can't distinguish ALL(A,B) from
ANY(A,B), which have the same leaf-ref set but very different truth conditions).

The single invariant this whole module protects: `flattened_elements` is read in exactly ONE
place -- as the `actual` side of the top-level equality check in check_operators(). It is NEVER
used as an input when computing some OTHER entry's expected value, even when that other entry
composes a DerivedOffenseDef as one of its own components. Using a stored flattened_elements as an
input would let a corrupted cache silently launder itself into "ground truth" for everything that
composes it -- replay_slot() re-derives every contribution from authored data (elements,
element_modules, derivation, qualifier.additions) instead, recursively, all the way down.
"""

from __future__ import annotations

from typing import Any, Mapping

from idpr.v2 import expressions
from idpr.v2.expressions import CanonicalExpr
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

_AXIS = "operator"

_CYCLE = object()  # sentinel: this (ref, slot) is already being computed higher up the call
                    # stack -- part of a derivation cycle. Axis 6 (check_derivation_graph) owns
                    # reporting the cycle itself; this only has to avoid infinite recursion when
                    # called on its own (each axis module is independently callable).


class _NotDecomposable(Exception):
    def __init__(self, subtree: CanonicalExpr, spanning_slots: frozenset[str]) -> None:
        self.subtree = subtree
        self.spanning_slots = spanning_slots


def check_operators(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    memo: dict[tuple[str, str], Any] = {}
    in_progress: set[tuple[str, str]] = set()

    for entry in registry.by_kind.get("derived_offense", ()):
        for slot in expressions.SLOT_NAMES:
            expected = replay_slot(registry, entry.id, slot, memo=memo, in_progress=in_progress)
            if expected is _CYCLE:
                continue
            if isinstance(expected, Finding):
                findings.append(expected)
                continue

            actual = expressions.canonicalize((entry.payload.get("flattened_elements") or {}).get(slot))
            if expected is None and actual is None:
                continue
            if expected is None:
                findings.append(Finding(
                    _AXIS, "flattened_elements_unexpected_slot", entry.id, f"flattened_elements.{slot}",
                    "no contributor implies this slot, but flattened_elements sets it",
                ))
            elif actual is None:
                findings.append(Finding(
                    _AXIS, "flattened_elements_missing_slot", entry.id, f"flattened_elements.{slot}",
                    "a contributor implies this slot, but flattened_elements omits it",
                ))
            elif expected != actual:
                findings.append(Finding(
                    _AXIS, "flattened_elements_semantic_mismatch", entry.id, f"flattened_elements.{slot}",
                    f"expected {expected!r}, got {actual!r}",
                ))
    return findings


def replay_slot(
    registry: DefinitionRegistry,
    ref: str,
    slot: str,
    *,
    memo: dict[tuple[str, str], Any],
    in_progress: set[tuple[str, str]],
) -> CanonicalExpr | Finding | Any:
    """THE single recursive source-of-truth for 'what should <ref> require for <slot>', derived
    entirely from authored data -- never from a stored flattened_elements, even when <ref> is
    itself a DerivedOffenseDef. Memoized per (ref, slot) across one whole check_operators() run,
    since the same base/derived offense can be composed into many ancestors."""
    key = (ref, slot)
    if key in memo:
        return memo[key]
    if key in in_progress:
        return _CYCLE
    in_progress.add(key)
    try:
        result = _replay_slot_uncached(registry, ref, slot, memo=memo, in_progress=in_progress)
    finally:
        in_progress.discard(key)
    if result is not _CYCLE:
        memo[key] = result
    return result


def _replay_slot_uncached(registry, ref, slot, *, memo, in_progress):
    entry = registry.get(ref)
    if entry is None:
        return None  # dangling ref -- axis 1 already reports this
    if entry.kind == "offense":
        return _offense_slot(registry, entry, slot)
    if entry.kind == "derived_offense":
        derivation = entry.payload["derivation"]
        if derivation["kind"] == "qualify":
            return _qualify_slot(registry, entry, derivation, slot, memo=memo, in_progress=in_progress)
        return _compose_slot(registry, entry, derivation, slot, memo=memo, in_progress=in_progress)
    return None  # wrong kind -- axis 1 already reports this


def _combine_contributions(*items: CanonicalExpr | Finding | None) -> CanonicalExpr | Finding:
    for item in items:
        if isinstance(item, Finding):
            return item
    return expressions.combine_all(*items)


def _offense_slot(registry: DefinitionRegistry, entry: DefinitionEntry, slot: str) -> CanonicalExpr | Finding:
    """An OffenseDef is a LEAF of the recursion -- authored data, nothing further to replay. Its
    true per-slot requirement is elements.<slot> combined with every element_modules entry's
    contribution to <slot>."""
    contributions: list[Any] = [expressions.canonicalize((entry.payload.get("elements") or {}).get(slot))]
    for index, module in enumerate(entry.payload.get("element_modules") or []):
        placement = module.get("placement") or {}
        if slot in placement.values():
            contributions.append(_bundle_slot_contribution(
                registry, entry, f"element_modules[{index}]", module["ref"], placement, slot,
            ))
    return _combine_contributions(*contributions)


def _qualify_slot(registry, entry, derivation, slot, *, memo, in_progress):
    base_contribution = replay_slot(registry, derivation["base"], slot, memo=memo, in_progress=in_progress)
    if base_contribution is _CYCLE:
        return _CYCLE
    qualifier = registry.get(derivation["qualifier"])
    addition = None
    if qualifier is not None and qualifier.kind == "qualifier":
        addition = expressions.canonicalize((qualifier.payload.get("additions") or {}).get(slot))
    return _combine_contributions(base_contribution, addition)


def _compose_slot(registry, entry, derivation, slot, *, memo, in_progress):
    contributions: list[Any] = []
    for index, component in enumerate(derivation["components"]):
        kind = component["kind"]
        if kind == "offense":
            contribution = replay_slot(registry, component["ref"], slot, memo=memo, in_progress=in_progress)
            if contribution is _CYCLE:
                return _CYCLE
            contributions.append(contribution)
        elif kind == "primitive" and component.get("slot") == slot:
            primitive = registry.get(component["ref"])
            if primitive is not None and primitive.kind == "primitive":
                contributions.append(("ref", primitive.payload["ref"]))
            # else: axis 1 already reports the dangling/kind-mismatch ref
        elif kind == "exported_component" and component.get("slot") == slot:
            resolved = registry.resolve_export(component["ref"])
            if resolved is not None:
                contributions.append(("ref", resolved))
            # else: axis 1/4 already report the broken export chain; nothing to contribute here
        elif kind == "bundle":
            placement = component.get("placement") or {}
            if slot in placement.values():
                field_path = f"derivation.components (local_key={component['local_key']!r})"
                contributions.append(_bundle_slot_contribution(
                    registry, entry, field_path, component["ref"], placement, slot,
                ))
    return _combine_contributions(*contributions)


def _bundle_slot_contribution(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    field_path: str,
    bundle_ref: str,
    placement: Mapping[str, str],
    slot: str,
) -> CanonicalExpr | Finding | None:
    bundle = registry.get(bundle_ref)
    if bundle is None or bundle.kind != "element_bundle":
        return None  # axis 1 already reports this
    canonical_requires = expressions.canonicalize(bundle.payload["requires"])
    try:
        distribution = _distribute(canonical_requires, placement)
    except _NotDecomposable as exc:
        return Finding(
            _AXIS,
            "bundle_placement_not_decomposable",
            entry.id,
            field_path,
            f"bundle {bundle_ref!r}'s subtree {exc.subtree!r} spans slots {sorted(exc.spanning_slots)}, "
            "but its operator does not permit splitting across slots (only ALL does)",
        )
    return distribution.get(slot)


def _distribute(canon: CanonicalExpr, placement: Mapping[str, str]) -> dict[str, CanonicalExpr]:
    """Recursively partitions a bundle's canonical requires tree into one contribution per slot.

    If an entire subtree's leaves all map to the SAME slot, that whole subtree -- regardless of
    its own root operator, ALL/ANY/ONE_OF/NOT alike -- becomes that slot's atomic contribution
    as-is. Only when a subtree's leaves span MULTIPLE slots does splitting even come up, and only
    an ALL node may be split (recursing into each child); a non-ALL node (ANY/ONE_OF/NOT) whose
    leaves span multiple slots cannot be split, since the coupling between its branches is
    semantically load-bearing (the same reason ONE_OF/ANY aren't associative under canonicalize).
    """
    leaves = _canonical_leaf_ids(canon)
    slots_needed = {placement[leaf] for leaf in leaves if leaf in placement}
    if len(slots_needed) <= 1:
        slot = next(iter(slots_needed), None)
        return {slot: canon} if slot is not None else {}
    if isinstance(canon, tuple) and canon[0] == "all":
        merged: dict[str, CanonicalExpr] = {}
        for child in canon[1]:
            for child_slot, contribution in _distribute(child, placement).items():
                merged[child_slot] = expressions.combine_all(merged.get(child_slot), contribution)
        return merged
    raise _NotDecomposable(canon, frozenset(slots_needed))


def _canonical_leaf_ids(canon: CanonicalExpr) -> frozenset[str]:
    if canon is None:
        return frozenset()
    op, payload = canon
    if op == "ref":
        return frozenset({payload})
    if op in ("all", "any", "one_of"):
        if not payload:
            return frozenset()
        return frozenset().union(*(_canonical_leaf_ids(child) for child in payload))
    if op == "not":
        return _canonical_leaf_ids(payload)
    raise ValueError(f"unknown canonical op {op!r}")
