"""Axis 1: reference typing -- every id reference in the Definition Layer must exist AND have
the expected object kind. 'missing_reference' (doesn't exist) and 'kind_mismatch' (exists, wrong
kind) are always distinguished, never conflated into one generic error.
"""

from __future__ import annotations

from typing import Any, Mapping

from idpr.v2 import expressions
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

_AXIS = "reference"

_EXPRESSION_LEAF_KINDS = frozenset({"ground_fact", "legal_element"})


def check_references(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    for entry in registry.by_id.values():
        handler = _HANDLERS.get(entry.kind)
        if handler is not None:
            findings.extend(handler(registry, entry))
    return findings


def _check_ref(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    field_path: str,
    ref: str,
    expected_kinds: frozenset[str],
) -> list[Finding]:
    actual_kind = registry.kind_of(ref)
    if actual_kind is None:
        return [Finding(_AXIS, "missing_reference", entry.id, field_path, f"{ref!r} does not exist in the registry")]
    if actual_kind not in expected_kinds:
        return [Finding(
            _AXIS,
            "kind_mismatch",
            entry.id,
            field_path,
            f"{ref!r} resolves to kind={actual_kind!r}, expected one of {sorted(expected_kinds)}",
        )]
    return []


def _check_expression(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    field_path: str,
    expr: Mapping[str, Any] | None,
) -> list[Finding]:
    """Walks an element_expression tree once, both checking every leaf ref's kind and detecting
    ONE_OF branches that canonicalize identically (always an authoring mistake -- section 8.3
    reserves ONE_OF for genuinely exclusive alternatives, never a place to intentionally repeat a
    branch)."""
    if expr is None:
        return []
    findings: list[Finding] = []
    op = expr["op"]
    if op == "ref":
        findings.extend(_check_ref(registry, entry, field_path, expr["ref"], _EXPRESSION_LEAF_KINDS))
    elif op in ("all", "any"):
        for index, child in enumerate(expr["args"]):
            findings.extend(_check_expression(registry, entry, f"{field_path}[{index}]", child))
    elif op == "one_of":
        seen_canonical: set[Any] = set()
        for index, child in enumerate(expr["args"]):
            canonical_child = expressions.canonicalize(child)
            if canonical_child in seen_canonical:
                findings.append(Finding(
                    _AXIS,
                    "duplicate_one_of_branch",
                    entry.id,
                    f"{field_path}[{index}]",
                    "ONE_OF branch duplicates an earlier branch in the same ONE_OF",
                ))
            seen_canonical.add(canonical_child)
            findings.extend(_check_expression(registry, entry, f"{field_path}[{index}]", child))
    elif op == "not":
        findings.extend(_check_expression(registry, entry, f"{field_path}.NOT", expr["arg"]))
    return findings


def _check_bundle_attachment(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    field_path: str,
    attachment: Mapping[str, Any],
) -> list[Finding]:
    """Shared between OffenseDef.element_modules entries and COMPOSE component_ref(kind=bundle)
    entries -- both are {ref, placement}. placement's keys must be exactly the referenced bundle's
    own leaf-refs: no missing, no extra."""
    findings: list[Finding] = []
    ref = attachment["ref"]
    findings.extend(_check_ref(registry, entry, f"{field_path}.ref", ref, frozenset({"element_bundle"})))
    bundle = registry.get(ref)
    if bundle is None or bundle.kind != "element_bundle":
        return findings
    bundle_leaves = expressions.leaf_refs(bundle.payload["requires"])
    placement_keys = frozenset(attachment["placement"].keys())
    missing = bundle_leaves - placement_keys
    extra = placement_keys - bundle_leaves
    if missing:
        findings.append(Finding(
            _AXIS, "placement_missing_leaves", entry.id, f"{field_path}.placement",
            f"placement is missing an entry for bundle leaves: {sorted(missing)}",
        ))
    if extra:
        findings.append(Finding(
            _AXIS, "placement_extra_leaves", entry.id, f"{field_path}.placement",
            f"placement names leaves that are not in the bundle's own requires: {sorted(extra)}",
        ))
    return findings


def _check_legal_element(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    findings: list[Finding] = []
    for index, ref in enumerate(entry.payload.get("grounded_by") or []):
        findings.extend(_check_ref(registry, entry, f"grounded_by[{index}]", ref, frozenset({"ground_fact"})))
    return findings


def _check_primitive(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    ref_kind = entry.payload["ref_kind"]
    return _check_ref(registry, entry, "ref", entry.payload["ref"], frozenset({ref_kind}))


def _check_element_bundle(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    return _check_expression(registry, entry, "requires", entry.payload["requires"])


def _check_exported_component(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    return _check_ref(registry, entry, "source_offense", entry.payload["source_offense"], frozenset({"offense"}))


def _check_offense(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    findings: list[Finding] = []
    elements = entry.payload.get("elements") or {}
    for slot in expressions.SLOT_NAMES:
        findings.extend(_check_expression(registry, entry, f"elements.{slot}", elements.get(slot)))
    for index, ref in enumerate(entry.payload.get("qualifiers") or []):
        findings.extend(_check_ref(registry, entry, f"qualifiers[{index}]", ref, frozenset({"qualifier"})))
    for key, ref in (entry.payload.get("exports") or {}).items():
        findings.extend(_check_ref(registry, entry, f"exports.{key}", ref, _EXPRESSION_LEAF_KINDS))
    for index, module in enumerate(entry.payload.get("element_modules") or []):
        findings.extend(_check_bundle_attachment(registry, entry, f"element_modules[{index}]", module))
    return findings


def _check_derived_offense(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    findings: list[Finding] = []
    flattened = entry.payload.get("flattened_elements") or {}
    for slot in expressions.SLOT_NAMES:
        findings.extend(_check_expression(registry, entry, f"flattened_elements.{slot}", flattened.get(slot)))

    derivation = entry.payload["derivation"]
    if derivation["kind"] == "qualify":
        findings.extend(_check_ref(registry, entry, "derivation.base", derivation["base"], frozenset({"offense"})))
        findings.extend(_check_ref(registry, entry, "derivation.qualifier", derivation["qualifier"], frozenset({"qualifier"})))
        return findings

    # compose
    component_kind_expectations = {
        "primitive": frozenset({"primitive"}),
        "bundle": frozenset({"element_bundle"}),
        "exported_component": frozenset({"exported_component"}),
        "offense": frozenset({"offense", "derived_offense"}),
    }
    local_keys_seen: dict[str, int] = {}
    for index, component in enumerate(derivation["components"]):
        findings.extend(_check_ref(
            registry, entry, f"derivation.components[{index}].ref",
            component["ref"], component_kind_expectations[component["kind"]],
        ))
        local_key = component["local_key"]
        if local_key in local_keys_seen:
            findings.append(Finding(
                _AXIS, "duplicate_local_key", entry.id, f"derivation.components[{index}].local_key",
                f"local_key {local_key!r} already used at components[{local_keys_seen[local_key]}]",
            ))
        else:
            local_keys_seen[local_key] = index
        if component["kind"] == "bundle":
            findings.extend(_check_bundle_attachment(registry, entry, f"derivation.components[{index}]", component))

    valid_local_keys = frozenset(local_keys_seen)
    for index, binding in enumerate(derivation["relations"]):
        findings.extend(_check_ref(registry, entry, f"derivation.relations[{index}].relation", binding["relation"], frozenset({"relation"})))
        left, right = binding["left"], binding["right"]
        for side_name, side_value in (("left", left), ("right", right)):
            if side_value not in valid_local_keys:
                findings.append(Finding(
                    _AXIS, "unresolved_local_key", entry.id, f"derivation.relations[{index}].{side_name}",
                    f"{side_value!r} is not a local_key declared in this derivation's components",
                ))
        if left == right:
            findings.append(Finding(
                _AXIS, "relation_binding_self_loop", entry.id, f"derivation.relations[{index}]",
                f"left and right both refer to {left!r} -- a relation must connect two different components",
            ))
    return findings


def _check_doctrine(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    return _check_expression(registry, entry, "requires", entry.payload["requires"])


def _check_qualifier(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    findings: list[Finding] = []
    additions = entry.payload.get("additions") or {}
    for slot in expressions.SLOT_NAMES:
        findings.extend(_check_expression(registry, entry, f"additions.{slot}", additions.get(slot)))
    return findings


def _check_completion_policy(registry: DefinitionRegistry, entry: DefinitionEntry) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_ref(registry, entry, "offense", entry.payload["offense"], frozenset({"offense", "derived_offense"})))
    for state_name, state in (entry.payload.get("states") or {}).items():
        # `when` is checked like any other expression: its leaves are ordinary predicate refs, and
        # they must be, since Completion runs before Elements and cannot read slot results.
        findings.extend(_check_expression(registry, entry, f"states.{state_name}.when", state.get("when")))
        if "requires" in state:
            findings.extend(_check_expression(registry, entry, f"states.{state_name}.requires", state["requires"]))
        for index, disposition in enumerate(state.get("relations") or ()):
            findings.extend(_check_ref(registry, entry, f"states.{state_name}.relations[{index}].relation", disposition["relation"], frozenset({"relation"})))
    return findings


_HANDLERS = {
    "legal_element": _check_legal_element,
    "primitive": _check_primitive,
    "element_bundle": _check_element_bundle,
    "exported_component": _check_exported_component,
    "offense": _check_offense,
    "derived_offense": _check_derived_offense,
    "doctrine": _check_doctrine,
    "qualifier": _check_qualifier,
    "completion_policy": _check_completion_policy,
}
