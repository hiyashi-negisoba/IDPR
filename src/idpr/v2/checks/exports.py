"""Axis 4: export/projection typing.

export_key must be a key present in the resolved source_offense's exports map. The mapped
concrete predicate id is resolved by DefinitionRegistry.resolve_export and consumed elsewhere
(axis 2); this axis only checks the key's presence.
"""

from __future__ import annotations

from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "export"


def check_exports(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    for entry in registry.by_kind.get("exported_component", ()):
        source = registry.get(entry.payload["source_offense"])
        if source is None or source.kind != "offense":
            continue  # axis 1 already reports this
        exports = source.payload.get("exports") or {}
        export_key = entry.payload["export_key"]
        if export_key not in exports:
            findings.append(Finding(
                _AXIS,
                "unknown_export_key",
                entry.id,
                "export_key",
                f"{export_key!r} is not declared in {entry.payload['source_offense']!r}'s exports map "
                f"(keys: {sorted(exports)})",
            ))
    return findings
