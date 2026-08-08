from __future__ import annotations

import copy

from idpr.v2.checks.exports import check_exports
from idpr.v2.checks.references import check_references
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


def _mutate(registry: DefinitionRegistry, kind: str, entry_id: str, mutator) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    for index, entry in enumerate(by_kind[kind]):
        if entry.id == entry_id:
            payload = copy.deepcopy(dict(entry.payload))
            mutator(payload)
            by_kind[kind][index] = DefinitionEntry(
                id=payload.get("id", entry.id), kind=kind, payload=payload, source_file=entry.source_file,
            )
            break
    else:
        raise KeyError(entry_id)
    by_id = {}
    frozen_by_kind = {}
    for k, entries in by_kind.items():
        frozen_by_kind[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def test_real_corpus_has_no_export_findings() -> None:
    assert check_exports(load_definitions()) == []


def test_source_offense_kind_mismatch_caught_by_axis_one_not_axis_four() -> None:
    registry = _mutate(
        load_definitions(), "exported_component", "exported_component.injury_result",
        lambda p: p.__setitem__("source_offense", "derived_offense.robbery_rape"),
    )
    reference_findings = check_references(registry)
    export_findings = check_exports(registry)
    assert any(f.code == "kind_mismatch" for f in reference_findings)
    assert export_findings == []  # axis 4 assumes source_offense already resolved; no double-report


def test_unknown_export_key_reported() -> None:
    registry = _mutate(
        load_definitions(), "exported_component", "exported_component.injury_result",
        lambda p: p.__setitem__("export_key", "nonexistent_key"),
    )
    findings = check_exports(registry)
    assert any(f.code == "unknown_export_key" for f in findings)
