from __future__ import annotations

import copy

from idpr.v2.checks.participation import check_participation
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
    return _rebuild(by_kind)


def _remove(registry: DefinitionRegistry, kind: str, entry_id: str) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind[kind] = [entry for entry in by_kind[kind] if entry.id != entry_id]
    return _rebuild(by_kind)


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, [])
    by_kind[kind].append(DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>"))
    return _rebuild(by_kind)


def _rebuild(by_kind: dict) -> DefinitionRegistry:
    by_id = {}
    frozen_by_kind = {}
    for kind, entries in by_kind.items():
        frozen_by_kind[kind] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def _codes(findings) -> set[str]:
    return {finding.code for finding in findings}


def test_real_corpus_has_no_participation_findings() -> None:
    assert check_participation(load_definitions()) == []


def test_two_participation_policies_is_ambiguous() -> None:
    second_policy = {
        "id": "participation_policy.synthetic_second",
        "modes": {"principal": {"basis": "direct"}},
    }
    registry = _add(load_definitions(), "participation_policy", second_policy)
    findings = check_participation(registry)
    assert "multiple_participation_policies" in _codes(findings)


def test_disabled_mode_not_declared_by_policy() -> None:
    def narrow_policy(payload):
        payload["modes"] = {"principal": {"basis": "direct"}, "co_principal": payload["modes"]["co_principal"]}

    registry = _mutate(load_definitions(), "participation_policy", "participation_policy.standard", narrow_policy)
    registry = _mutate(
        registry, "offense", "offense.robbery",
        lambda p: p.__setitem__("participation_constraints", {"disabled_modes": ["instigator"]}),
    )
    findings = check_participation(registry)
    assert "disabled_mode_undeclared" in _codes(findings)


def test_attributable_slot_not_declared_on_offense() -> None:
    registry = _mutate(
        load_definitions(), "offense", "offense.robbery",
        lambda p: p.__setitem__("participation_constraints", {"attributable_slots": ["result"]}),
    )
    findings = check_participation(registry)
    assert "attributable_slot_not_declared" in _codes(findings)


def test_participation_constraints_without_any_policy() -> None:
    registry = _remove(load_definitions(), "participation_policy", "participation_policy.standard")
    registry = _mutate(
        registry, "offense", "offense.robbery",
        lambda p: p.__setitem__("participation_constraints", {"disabled_modes": ["aider"]}),
    )
    findings = check_participation(registry)
    assert "participation_constraints_without_policy" in _codes(findings)
