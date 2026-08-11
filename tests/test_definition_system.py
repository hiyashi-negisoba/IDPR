from __future__ import annotations
from pathlib import Path

from idpr.v2.checks import run_type_checks
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.registry import load_definitions

ROOT = Path(__file__).resolve().parents[1]


def test_production_registry_has_no_type_findings() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    assert run_type_checks(registry) == []


def test_every_production_offense_compiles_totally() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    offenses = (*registry.by_kind["offense"], *registry.by_kind["derived_offense"])
    assert offenses
    failures = {
        entry.id: result
        for entry in offenses
        if not isinstance((result := compile_offense(registry, entry.id)), CompiledOffense)
    }
    assert failures == {}
