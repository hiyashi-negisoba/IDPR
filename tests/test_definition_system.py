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


def _mutated(registry, entry_id: str, payload):
    """한 정의만 갈아 끼운 registry. 저작을 건드리지 않고 checker를 시험한다."""
    from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

    original = registry.get(entry_id)
    assert original is not None
    patched = DefinitionEntry(original.id, original.kind, payload, original.source_file)
    return DefinitionRegistry(
        {**registry.by_id, patched.id: patched},
        {
            kind: tuple(patched if value.id == patched.id else value for value in values)
            for kind, values in registry.by_kind.items()
        },
    )


def test_a_malformed_blocker_is_rejected_like_any_other_expression() -> None:
    """`blocked_when`은 fail-open이라 checker가 유일한 방어선이다.

    blocker는 TRUE일 때만 막는다. 그래서 ref가 해소되지 않으면 런타임은 UNKNOWN을 받고
    아무것도 막지 않는다 -- 오타가 "이 사건에는 예외가 없다"로 읽힌다. 예외로 터지지 않으니
    저작 시점에 잡지 못하면 아무도 알려 주지 않는다.
    """
    registry = load_definitions(ROOT / "data/v2/definitions")
    doctrine = next(
        entry for entry in registry.by_kind["doctrine"] if entry.payload.get("blocked_when")
    )
    findings = run_type_checks(
        _mutated(
            registry,
            doctrine.id,
            {**doctrine.payload, "blocked_when": {"op": "ref", "ref": "legal_element.nope"}},
        )
    )
    assert any(
        value.code == "missing_reference" and value.field_path == "blocked_when"
        for value in findings
    ), findings

    policy = next(
        entry
        for entry in registry.by_kind["completion_policy"]
        if any(state.get("blocked_when") for state in entry.payload["states"].values())
    )
    state_name = next(
        name for name, state in policy.payload["states"].items() if state.get("blocked_when")
    )
    states = {
        name: (
            {**state, "blocked_when": {"op": "ref", "ref": "offense.homicide"}}
            if name == state_name
            else state
        )
        for name, state in policy.payload["states"].items()
    }
    findings = run_type_checks(
        _mutated(registry, policy.id, {**policy.payload, "states": states})
    )
    assert any(
        value.code == "kind_mismatch"
        and value.field_path == f"states.{state_name}.blocked_when"
        for value in findings
    ), findings
