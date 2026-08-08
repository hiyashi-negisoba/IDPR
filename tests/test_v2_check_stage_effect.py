from __future__ import annotations

from idpr.v2.checks.stage_effect import check_stage_effect
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, [])
    by_kind[kind].append(DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>"))
    by_id = {}
    frozen_by_kind = {}
    for k, entries in by_kind.items():
        frozen_by_kind[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def test_real_corpus_has_no_stage_effect_findings() -> None:
    assert check_stage_effect(load_definitions()) == []


def test_defeat_doctrine_never_produces_a_finding_or_crashes() -> None:
    registry = load_definitions()
    findings = check_stage_effect(registry)
    self_defense = [f for f in findings if f.object_id == "doctrine.self_defense"]
    assert self_defense == []


def test_modifier_ref_reused_at_different_stage_is_inconsistent() -> None:
    conflicting = {
        "id": "doctrine.synthetic_conflicting_modifier",
        "stage": "punishability",
        "requires": {"op": "ref", "ref": "ground_fact.injury_occurred"},
        "effect": {"effect": "MODIFY", "stage": "punishability", "modifier_ref": "modifier.culpability.diminished"},
    }
    registry = _add(load_definitions(), "doctrine", conflicting)
    findings = check_stage_effect(registry)
    assert any(f.code == "modifier_ref_stage_inconsistent" for f in findings)
