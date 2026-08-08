"""Axis 6: derivation graph integrity.

A COMPOSE component tagged kind=offense may resolve to another DerivedOffenseDef (axis 1
deliberately allows this, since the schema's `offense` tag doesn't distinguish OffenseDef from
DerivedOffenseDef) -- which can form a cycle. QUALIFY can never contribute an edge here: axis 1
pins qualify.base to kind=offense strictly, which is never a DerivedOffenseDef, so QUALIFY chains
are acyclic by construction.
"""

from __future__ import annotations

from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "derivation"

_WHITE, _GRAY, _BLACK = 0, 1, 2


def check_derivation_graph(registry: DefinitionRegistry) -> list[Finding]:
    edges: dict[str, list[str]] = {}
    for entry in registry.by_kind.get("derived_offense", ()):
        derivation = entry.payload["derivation"]
        targets: list[str] = []
        if derivation["kind"] == "compose":
            for component in derivation["components"]:
                if component["kind"] == "offense":
                    target = registry.get(component["ref"])
                    if target is not None and target.kind == "derived_offense":
                        targets.append(component["ref"])
        edges[entry.id] = targets

    findings: list[Finding] = []
    color = {node: _WHITE for node in edges}
    reported_cycles: set[frozenset[str]] = set()

    def visit(node: str, stack: list[str]) -> None:
        color[node] = _GRAY
        stack.append(node)
        for neighbor in edges.get(node, ()):
            if color.get(neighbor) == _GRAY:
                cycle_start = stack.index(neighbor)
                cycle_nodes = stack[cycle_start:]
                key = frozenset(cycle_nodes)
                if key not in reported_cycles:
                    reported_cycles.add(key)
                    findings.append(Finding(
                        _AXIS,
                        "derivation_cycle",
                        node,
                        "derivation.components",
                        "COMPOSE derivation cycle: " + " -> ".join([*cycle_nodes, neighbor]),
                    ))
            elif color.get(neighbor, _WHITE) == _WHITE:
                visit(neighbor, stack)
        stack.pop()
        color[node] = _BLACK

    for node in edges:
        if color[node] == _WHITE:
            visit(node, [])

    return findings
