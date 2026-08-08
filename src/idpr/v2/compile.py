"""QUALIFY / COMPOSE compiler (build-order step 4).

Produces `CompiledOffense` from Definition Layer data: fully resolved per-slot element
requirements (the same computation Type checker axis 2 already needed to verify
`flattened_elements`) AND resolved relation bindings (COMPOSE's `derivation.relations`,
local_key -> the specific component *occurrence* it names -- never collapsed to a global ref,
since the same ref can appear twice under different local_keys within one composition, and a
relation must still be able to tell those two occurrences apart).

THE single invariant this module protects: a successful `CompiledOffense` is never partial. If
any component or relation binding in a derivation fails to resolve, `compile_offense()` returns
the accumulated `list[Finding]` for the WHOLE entry instead of a `CompiledOffense` with a hole in
it -- never "the good slots are filled in, the broken one is just missing." Cycles are a separate
case: `DerivationCycle` is propagated immediately (no finding accumulation), mirroring axis 6
(`check_derivation_graph`) owning cycle *reporting* -- this module only has to not infinite-recurse
when called standalone.

`CompiledOffense = Slots + Required Relation Bindings`, never `Slots` alone: a COMPOSE-derived
offense's `relations` encode load-bearing legal conditions (statutory/causal nexus -- v2.1.0
section 9.2, "COMPOSE is not naive Boolean conjunction"), not optional metadata. Downstream
runtime code must never decide Elements from `.slots` while silently ignoring a non-empty
`.relations`.

Scope boundary (build-order step 4 vs step 5, "Relation evaluator"): this module resolves *which*
component occurrence a relation binds to (structural), defensively confirms `relation_ref` names an
actual `RelationDef`, and carries each binding's authored `left_view`/`right_view` through verbatim
-- it does **not** check whether those views match the `RelationDef`'s `left_type`/`right_type`, nor
whether the bound endpoint can actually provide the declared view. That lowering lives in step 5
(`checks/relation_types.py`), so a definition that is merely mis-typed still compiles here and is
reported by exactly one axis instead of two.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from idpr.v2 import expressions
from idpr.v2.expressions import SLOT_NAMES, CanonicalExpr
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

_AXIS = "operator"

_COMPONENT_KIND_EXPECTATIONS: Mapping[str, frozenset[str]] = {
    "primitive": frozenset({"primitive"}),
    "bundle": frozenset({"element_bundle"}),
    "exported_component": frozenset({"exported_component"}),
    "offense": frozenset({"offense", "derived_offense"}),
}


class DerivationCycle:
    """Sentinel distinct from Finding -- axis 6 (check_derivation_graph) owns *reporting* a
    cycle; compile_offense only needs to not infinite-recurse when called standalone. Never
    stored in `memo`: cycle-ness depends on the traversal path (`in_progress` at the moment of
    re-entry), not on any inherent property of the ref, so memoizing it would poison later
    traversals that reach the same ref by a different, cycle-free path."""

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return "DerivationCycle()"


class _NotDecomposable(Exception):
    def __init__(self, subtree: CanonicalExpr, spanning_slots: frozenset[str]) -> None:
        self.subtree = subtree
        self.spanning_slots = spanning_slots


@dataclass(frozen=True)
class CompiledComponentInstance:
    """One COMPOSE component *occurrence*. `local_key` is always present -- instances only
    exist for COMPOSE components; the top-level offense itself is a `CompiledOffense`, never
    wrapped in an instance."""

    local_key: str
    component_kind: str  # authored category: "primitive" | "bundle" | "exported_component" | "offense"
    resolved_kind: str  # registry.get(source_ref).kind -- "offense"/"derived_offense" only differ
    #                      when component_kind == "offense"; the other three categories are 1:1.
    source_ref: str  # component_ref["ref"] -- NOT unique per composition; local_key is.
    compiled_content: "CompiledOffense | CanonicalExpr"
    # component_kind="offense"            -> nested CompiledOffense (recursive compile of source_ref)
    # component_kind="primitive"          -> ("ref", primitive.payload["ref"])
    # component_kind="exported_component" -> ("ref", registry.resolve_export(source_ref))
    # component_kind="bundle"             -> canonicalize(bundle.payload["requires"])  (undistributed --
    #                                         per-slot distribution happens during slot assembly)
    # Never a Finding, never a DerivationCycle -- see module docstring's invariant.


@dataclass(frozen=True)
class CompiledRelationBinding:
    relation_ref: str  # RelationDef id
    left: CompiledComponentInstance
    right: CompiledComponentInstance
    left_view: str  # authored semantic view (projection) this relation uses each endpoint through --
    right_view: str  # carried through verbatim, never inferred from RelationDef.left_type/right_type.
    # No type-validity judgement here -- whether relation_ref's left_type/right_type actually fits
    # left/right's declared view (and whether the endpoint can even provide that view) is step 5's
    # job (relation lowering, checks/relation_types.py).


@dataclass(frozen=True)
class CompiledOffense:
    id: str
    slots: Mapping[str, CanonicalExpr]  # every SLOT_NAMES entry, same shape as flattened_elements
    components: tuple[CompiledComponentInstance, ...]  # () for a plain OffenseDef or a QUALIFY-derived offense
    relations: tuple[CompiledRelationBinding, ...]  # () unless this entry's derivation.kind == "compose"
    # CompiledOffense = Slots + Required Relation Bindings, not Slots alone -- see module docstring.


def compile_offense(
    registry: DefinitionRegistry,
    ref: str,
    *,
    memo: "dict[str, CompiledOffense | list[Finding]] | None" = None,
    in_progress: "set[str] | None" = None,
) -> "CompiledOffense | list[Finding] | DerivationCycle | None":
    """None if ref doesn't exist or isn't kind offense/derived_offense (axis 1 already reports
    this). Pass a shared memo/in_progress across multiple calls (e.g. one per derived_offense in
    a registry) to reuse work the way axis 2 does across a whole check_operators() run; a fresh
    pair is created per call otherwise."""
    if memo is None:
        memo = {}
    if in_progress is None:
        in_progress = set()
    if ref in memo:
        return memo[ref]
    if ref in in_progress:
        return DerivationCycle()

    entry = registry.get(ref)
    if entry is None or entry.kind not in ("offense", "derived_offense"):
        return None

    in_progress.add(ref)
    try:
        if entry.kind == "offense":
            result = _compile_plain_offense(registry, entry)
        else:
            derivation = entry.payload["derivation"]
            if derivation["kind"] == "qualify":
                result = _compile_qualify(registry, entry, derivation, memo=memo, in_progress=in_progress)
            else:
                result = _compile_compose(registry, entry, derivation, memo=memo, in_progress=in_progress)
    finally:
        in_progress.discard(ref)

    if not isinstance(result, DerivationCycle):
        memo[ref] = result
    return result


def _compile_plain_offense(registry: DefinitionRegistry, entry: DefinitionEntry) -> "CompiledOffense | list[Finding]":
    findings: list[Finding] = []
    elements = entry.payload.get("elements") or {}
    modules = entry.payload.get("element_modules") or []

    bundle_distributions: dict[int, dict[str, CanonicalExpr]] = {}
    for index, module in enumerate(modules):
        bundle = registry.get(module["ref"])
        if bundle is None or bundle.kind != "element_bundle":
            findings.append(Finding(
                _AXIS, "component_unresolved", entry.id, f"element_modules[{index}]",
                f"{module['ref']!r} does not resolve to an element_bundle",
            ))
            continue
        placement = module.get("placement") or {}
        try:
            bundle_distributions[index] = _distribute(expressions.canonicalize(bundle.payload["requires"]), placement)
        except _NotDecomposable as exc:
            findings.append(Finding(
                _AXIS, "bundle_placement_not_decomposable", entry.id, f"element_modules[{index}]",
                f"bundle {module['ref']!r}'s subtree {exc.subtree!r} spans slots "
                f"{sorted(exc.spanning_slots)}, but its operator does not permit splitting across "
                "slots (only ALL does)",
            ))

    if findings:
        return findings

    slots: dict[str, CanonicalExpr] = {}
    for slot in SLOT_NAMES:
        contributions: list[CanonicalExpr] = [expressions.canonicalize(elements.get(slot))]
        for index, module in enumerate(modules):
            placement = module.get("placement") or {}
            if slot in placement.values():
                contributions.append(bundle_distributions[index].get(slot))
        slots[slot] = expressions.combine_all(*contributions)

    return CompiledOffense(entry.id, slots, (), ())


def _compile_qualify(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    derivation: Mapping[str, object],
    *,
    memo: dict,
    in_progress: set,
) -> "CompiledOffense | list[Finding] | DerivationCycle":
    base_ref = derivation["base"]
    base_entry = registry.get(base_ref)
    if base_entry is None or base_entry.kind != "offense":
        return [Finding(
            _AXIS, "component_unresolved", entry.id, "derivation.base",
            f"{base_ref!r} does not resolve to an offense",
        )]

    base_result = compile_offense(registry, base_ref, memo=memo, in_progress=in_progress)
    if isinstance(base_result, DerivationCycle):
        return base_result
    if isinstance(base_result, list):
        return base_result
    assert base_result is not None  # base_entry.kind == "offense" already confirmed above

    qualifier_entry = registry.get(derivation["qualifier"])
    if qualifier_entry is None or qualifier_entry.kind != "qualifier":
        return [Finding(
            _AXIS, "component_unresolved", entry.id, "derivation.qualifier",
            f"{derivation['qualifier']!r} does not resolve to a qualifier",
        )]

    additions = qualifier_entry.payload.get("additions") or {}
    slots = {
        slot: expressions.combine_all(base_result.slots.get(slot), expressions.canonicalize(additions.get(slot)))
        for slot in SLOT_NAMES
    }
    return CompiledOffense(entry.id, slots, (), ())


def _compile_compose(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    derivation: Mapping[str, object],
    *,
    memo: dict,
    in_progress: set,
) -> "CompiledOffense | list[Finding] | DerivationCycle":
    findings: list[Finding] = []
    instances: dict[str, CompiledComponentInstance] = {}

    for index, component in enumerate(derivation["components"]):
        field_path = f"derivation.components[{index}]"
        outcome = _compile_component(registry, entry, field_path, component, memo=memo, in_progress=in_progress)
        if isinstance(outcome, DerivationCycle):
            return outcome
        if isinstance(outcome, list):
            findings.extend(outcome)
            continue
        local_key = component["local_key"]
        if local_key in instances:
            findings.append(Finding(
                _AXIS, "duplicate_local_key", entry.id, field_path,
                f"local_key {local_key!r} already used earlier in this derivation",
            ))
            continue
        instances[local_key] = outcome

    if findings:
        return findings

    bundle_distributions: dict[str, dict[str, CanonicalExpr]] = {}
    for component in derivation["components"]:
        if component["kind"] != "bundle":
            continue
        local_key = component["local_key"]
        instance = instances[local_key]
        placement = component.get("placement") or {}
        try:
            bundle_distributions[local_key] = _distribute(instance.compiled_content, placement)
        except _NotDecomposable as exc:
            findings.append(Finding(
                _AXIS, "bundle_placement_not_decomposable", entry.id,
                f"derivation.components (local_key={local_key!r})",
                f"bundle {instance.source_ref!r}'s subtree {exc.subtree!r} spans slots "
                f"{sorted(exc.spanning_slots)}, but its operator does not permit splitting across "
                "slots (only ALL does)",
            ))

    if findings:
        return findings

    slots: dict[str, CanonicalExpr] = {}
    for slot in SLOT_NAMES:
        contributions: list[CanonicalExpr] = []
        for component in derivation["components"]:
            instance = instances[component["local_key"]]
            if component["kind"] == "offense":
                contributions.append(instance.compiled_content.slots.get(slot))
            elif component["kind"] in ("primitive", "exported_component") and component.get("slot") == slot:
                contributions.append(instance.compiled_content)
            elif component["kind"] == "bundle":
                contributions.append(bundle_distributions[component["local_key"]].get(slot))
        slots[slot] = expressions.combine_all(*contributions)

    relations: list[CompiledRelationBinding] = []
    for index, binding in enumerate(derivation["relations"]):
        field_path = f"derivation.relations[{index}]"
        relation_entry = registry.get(binding["relation"])
        if relation_entry is None or relation_entry.kind != "relation":
            findings.append(Finding(
                _AXIS, "relation_ref_unresolved", entry.id, field_path,
                f"{binding['relation']!r} does not resolve to a relation",
            ))
            continue
        left = instances.get(binding["left"])
        right = instances.get(binding["right"])
        if left is None or right is None:
            findings.append(Finding(
                _AXIS, "relation_binding_unresolved_local_key", entry.id, field_path,
                f"left={binding['left']!r} right={binding['right']!r} must both be local_keys "
                "declared in this derivation's components",
            ))
            continue
        left_view = binding.get("left_view")
        right_view = binding.get("right_view")
        if not left_view or not right_view:
            findings.append(Finding(
                _AXIS, "relation_binding_missing_view", entry.id, field_path,
                "relation binding must declare both left_view and right_view (the semantic "
                "projection each endpoint is used through); they are never inferred from the "
                "RelationDef's left_type/right_type",
            ))
            continue
        relations.append(CompiledRelationBinding(binding["relation"], left, right, left_view, right_view))

    if findings:
        return findings

    ordered_instances = tuple(instances[c["local_key"]] for c in derivation["components"])
    return CompiledOffense(entry.id, slots, ordered_instances, tuple(relations))


def _compile_component(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    field_path: str,
    component: Mapping[str, object],
    *,
    memo: dict,
    in_progress: set,
) -> "CompiledComponentInstance | list[Finding] | DerivationCycle":
    kind = component["kind"]
    ref = component["ref"]
    resolved = registry.get(ref)
    if resolved is None or resolved.kind not in _COMPONENT_KIND_EXPECTATIONS[kind]:
        return [Finding(
            _AXIS, "component_unresolved", entry.id, field_path,
            f"{ref!r} does not resolve to an expected kind for component kind={kind!r}",
        )]

    if kind == "offense":
        nested = compile_offense(registry, ref, memo=memo, in_progress=in_progress)
        if isinstance(nested, DerivationCycle):
            return nested
        if isinstance(nested, list):
            return nested
        assert nested is not None  # resolved.kind already confirmed offense/derived_offense above
        content: "CompiledOffense | CanonicalExpr" = nested
    elif kind == "primitive":
        content = ("ref", resolved.payload["ref"])
    elif kind == "exported_component":
        target = registry.resolve_export(ref)
        if target is None:
            return [Finding(
                _AXIS, "exported_component_unresolved", entry.id, field_path,
                f"{ref!r} could not be resolved via source_offense.exports",
            )]
        content = ("ref", target)
    elif kind == "bundle":
        content = expressions.canonicalize(resolved.payload["requires"])
    else:  # pragma: no cover - schema restricts component.kind to the four handled above
        raise ValueError(f"unknown component kind {kind!r}")

    return CompiledComponentInstance(component["local_key"], kind, resolved.kind, ref, content)


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
