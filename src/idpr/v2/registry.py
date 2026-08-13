"""Definition Layer registry: schema-validated instance loading + a flat id index."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml

from idpr.v2.schema import PROJECT_ROOT, SCHEMA_DIR, schema_errors

EXAMPLES_DIR = PROJECT_ROOT / "docs/contracts/v2/examples"

KIND_TO_EXAMPLE_FILE: Mapping[str, str] = {
    "ground_fact": "ground_facts.yaml",
    "legal_element": "legal_elements.yaml",
    "primitive": "primitives.yaml",
    "element_bundle": "element_bundles.yaml",
    "exported_component": "exported_components.yaml",
    "offense": "offenses.yaml",
    "derived_offense": "derived_offenses.yaml",
    "doctrine": "doctrines.yaml",
    "qualifier": "qualifiers.yaml",
    "relation": "relations.yaml",
    "completion_policy": "completion_policies.yaml",
    "participation_policy": "participation_policies.yaml",
    "mistake_policy": "mistake_policies.yaml",
    "excess_policy": "excess_policies.yaml",
}


class RegistryError(ValueError):
    """Fatal Definition Layer loading error: a schema-invalid instance, or a duplicate id across
    any of the 12 kinds (nothing in the *.schema.json files enforces one shared id namespace
    across all kinds -- this is the single enforcement point, same role as
    src/idpr/rulegen/registry.py's manifest-fatal ValueErrors)."""


@dataclass(frozen=True)
class DefinitionEntry:
    id: str
    kind: str
    payload: Mapping[str, object]
    source_file: str


@dataclass(frozen=True)
class DefinitionRegistry:
    by_id: Mapping[str, DefinitionEntry]
    by_kind: Mapping[str, tuple[DefinitionEntry, ...]]

    def get(self, ref: str) -> DefinitionEntry | None:
        return self.by_id.get(ref)

    def kind_of(self, ref: str) -> str | None:
        entry = self.by_id.get(ref)
        return entry.kind if entry is not None else None

    def resolve_export(self, exported_component_ref: str) -> str | None:
        """ExportedComponentDef -> source_offense -> exports[export_key] -> concrete predicate id.

        2026-08-08 review: an earlier draft treated this as unknowable at the Definition Layer
        ("_ExportUnresolved") -- wrong. Removing ExportedComponentDef.resolved_ref from the
        *authored* schema only meant "don't hand-author a derived value," not "this value is
        unknowable." Both source_offense and exports[export_key] already exist in the registry, so
        this resolves fully and deterministically -- the future compiler should reuse this exact
        resolver rather than reimplementing the lookup.

        Returns None only if the chain is already broken in a way axis 1 (unresolved
        source_offense / wrong kind) or axis 4 (export_key not declared) independently report --
        callers that already gate on those checks passing should never actually observe None here.
        """
        component = self.by_id.get(exported_component_ref)
        if component is None or component.kind != "exported_component":
            return None
        source_offense = self.by_id.get(component.payload["source_offense"])
        if source_offense is None or source_offense.kind != "offense":
            return None
        exports = source_offense.payload.get("exports") or {}
        return exports.get(component.payload["export_key"])


def load_definitions(
    definitions_dir: Path = EXAMPLES_DIR,
    schema_dir: Path = SCHEMA_DIR,
    kind_to_file: Mapping[str, str] = KIND_TO_EXAMPLE_FILE,
) -> DefinitionRegistry:
    by_id: dict[str, DefinitionEntry] = {}
    by_kind: dict[str, list[DefinitionEntry]] = {kind: [] for kind in kind_to_file}

    for kind, filename in kind_to_file.items():
        path = definitions_dir / filename
        instances = yaml.safe_load(path.read_text()) or []
        if not isinstance(instances, list):
            raise RegistryError(f"{path}: expected a YAML list of instances")
        for index, payload in enumerate(instances):
            errors = schema_errors(kind, payload, schema_dir)
            if errors:
                raise RegistryError(f"{path}[{index}]: " + "; ".join(errors))
            instance_id = payload["id"]
            if instance_id in by_id:
                existing = by_id[instance_id]
                raise RegistryError(
                    f"{path}: duplicate id {instance_id!r} (already defined as "
                    f"kind={existing.kind!r} in {existing.source_file!r})"
                )
            entry = DefinitionEntry(id=instance_id, kind=kind, payload=payload, source_file=str(path))
            by_id[instance_id] = entry
            by_kind[kind].append(entry)

    return DefinitionRegistry(
        by_id=by_id,
        by_kind={kind: tuple(entries) for kind, entries in by_kind.items()},
    )
