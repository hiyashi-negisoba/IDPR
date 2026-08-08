"""Axis 7: relation lowering (build-order step 5, first half).

Checks that every COMPOSE relation binding is *well-typed*, which is two independent obligations
per endpoint -- passing one never excuses the other:

  A. the authored view matches the RelationDef's declared type
     (binding.left_view == RelationDef.left_type, same for right)
  B. the bound endpoint can actually PROVIDE that view

Obligation B is why this axis exists at all rather than being folded into the compiler. The natural
first design -- give each definition object one intrinsic semantic type -- does not survive contact
with the corpus: `offense.robbery` is bound as a *conduct* endpoint of `relation.occasion_identity`
(기회의 동일성 relates two courses of conduct) and as an *event* endpoint of
`relation.causal_nexus` (which relates a causing event to a caused one). A single fixed type on
OffenseDef would have to reject one of those two perfectly valid fixtures. So the *structured*
kinds get a relation-scoped projection (the authored view, checked against a fixed set of aspects
an offense can be viewed through) while *atomic* predicates -- which genuinely do have one
intrinsic sort -- declare `semantic_sort` and are checked against it exactly.

The view is always read from the authored binding, never inferred from RelationDef.left_type. An
inferred view would make obligation A vacuously true and silently reduce this axis to a no-op.

Independence: like every other axis this one assumes no other axis has run. It calls
compile.compile_offense() itself, and when compilation *fails* it skips that entry rather than
forwarding the compiler's findings -- axis 2 (operators) already reports those, and forwarding here
would duplicate every compile diagnostic in run_type_checks() output.
"""

from __future__ import annotations

from idpr.v2 import compile
from idpr.v2.compile import CompiledComponentInstance, CompiledOffense, CompiledRelationBinding
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "relation_type"

_OFFENSE_VIEWS = frozenset({"conduct", "event"})
"""The aspects a whole offense can currently be related through. Deliberately narrow and aligned
with the existing RelationDef type vocabulary -- an unsupported combination fails loudly here
instead of being guessed. Widen only alongside a relation that actually needs it."""


def check_relation_types(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    memo: dict = {}
    in_progress: set = set()

    for entry in registry.by_kind.get("derived_offense", ()):
        compiled = compile.compile_offense(registry, entry.id, memo=memo, in_progress=in_progress)
        if not isinstance(compiled, CompiledOffense):
            continue  # cycle or compile failure -- owned by axes 2/6, not re-reported here
        for index, binding in enumerate(compiled.relations):
            findings.extend(_check_binding(registry, entry.id, index, binding))
    return findings


def _check_binding(
    registry: DefinitionRegistry, object_id: str, index: int, binding: CompiledRelationBinding,
) -> list[Finding]:
    relation = registry.get(binding.relation_ref)
    if relation is None or relation.kind != "relation":
        return []  # compile_offense already guarantees this resolves; unreachable via that path

    findings: list[Finding] = []
    for side, view, declared_type, instance in (
        ("left", binding.left_view, relation.payload["left_type"], binding.left),
        ("right", binding.right_view, relation.payload["right_type"], binding.right),
    ):
        field_path = f"derivation.relations[{index}].{side}_view"
        if view != declared_type:
            findings.append(Finding(
                _AXIS, "relation_view_type_mismatch", object_id, field_path,
                f"binds {instance.local_key!r} through view {view!r}, but "
                f"{binding.relation_ref!r} declares {side}_type={declared_type!r}",
            ))
        providable = _endpoint_views(registry, instance)
        if not providable:
            findings.append(Finding(
                _AXIS, "relation_endpoint_untyped", object_id, field_path,
                f"{instance.local_key!r} ({instance.source_ref!r}, resolved kind "
                f"{instance.resolved_kind!r}) declares no semantic typing at all, so its view "
                f"{view!r} cannot be verified",
            ))
        elif view not in providable:
            findings.append(Finding(
                _AXIS, "relation_view_unsupported_by_component_kind", object_id, field_path,
                f"{instance.local_key!r} ({instance.source_ref!r}) cannot be viewed as {view!r}; "
                f"it provides {sorted(providable)}",
            ))
    return findings


def _endpoint_views(registry: DefinitionRegistry, instance: CompiledComponentInstance) -> frozenset[str]:
    """The views this endpoint occurrence can actually be projected through.

    An empty result means "no declared semantic typing exists for this endpoint" -- reported as
    relation_endpoint_untyped rather than silently passing. Two distinct causes:
      - element_bundle: a bundle is a *tree* of predicates across possibly several slots, so it has
        no single endpoint sort to project. Always unsupported at this baseline. (Step 4 still
        preserves bundle endpoints in the IR -- different layer, no conflict: the compiler records
        what was authored, this axis judges whether it is well-typed.)
      - primitive / exported_component whose resolved atomic predicate declares no semantic_sort.
    """
    if instance.resolved_kind in ("offense", "derived_offense"):
        return _OFFENSE_VIEWS
    if instance.resolved_kind == "element_bundle":
        return frozenset()

    if instance.resolved_kind == "primitive":
        source = registry.get(instance.source_ref)
        target_id = source.payload["ref"] if source is not None else None
    else:  # exported_component
        target_id = registry.resolve_export(instance.source_ref)

    target = registry.get(target_id) if target_id is not None else None
    sort = target.payload.get("semantic_sort") if target is not None else None
    return frozenset({sort}) if sort else frozenset()
