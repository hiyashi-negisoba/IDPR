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


def test_a_typo_in_candidate_materialization_is_rejected() -> None:
    """저작된 binding_sets ref는 후보를 여는 실행 metadata다.

    ref가 해소되지 않으면 예외가 나지 않는다. materialization이 짝을 못 찾을 뿐이고, 그
    후보는 사건에 애초에 없었던 것처럼 조용히 사라진다. blocked_when과 같은 이유로 checker가
    유일한 방어선이다.
    """
    registry = load_definitions(ROOT / "data/v2/definitions")
    entry = next(
        value
        for value in registry.by_kind["derived_offense"]
        if (value.payload.get("candidate_materialization") or {}).get("binding_sets")
    )
    metadata = dict(entry.payload["candidate_materialization"])
    metadata["binding_sets"] = [["offense.theft", "offense.nope"]]
    findings = run_type_checks(
        _mutated(registry, entry.id, {**entry.payload, "candidate_materialization": metadata})
    )

    assert any(
        value.code == "missing_reference"
        and value.field_path == "candidate_materialization.binding_sets[0][1]"
        for value in findings
    ), findings


def test_candidate_materialization_rejects_a_non_offense_kind() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    entry = next(
        value
        for value in registry.by_kind["derived_offense"]
        if (value.payload.get("candidate_materialization") or {}).get("distinct_actor_binding_sets")
    )
    metadata = dict(entry.payload["candidate_materialization"])
    metadata["distinct_actor_binding_sets"] = [["legal_element.intent"]]
    findings = run_type_checks(
        _mutated(registry, entry.id, {**entry.payload, "candidate_materialization": metadata})
    )

    assert any(
        value.code == "kind_mismatch"
        and value.field_path == "candidate_materialization.distinct_actor_binding_sets[0][0]"
        for value in findings
    ), findings


def test_blocker_only_predicates_enter_the_dependency_closure() -> None:
    """blocked_when leaf도 traversal의 정식 입력이다.

    blocker는 TRUE일 때만 defeat한다. 그 leaf를 closure가 수집하지 않으면 target이 생기지 않고,
    묻지 않았으므로 UNKNOWN이 되며, 결과적으로 예외가 한 번도 발동하지 않는다. traversal의
    누락이 법적 판단을 대신하게 되는 것이다. 실제로 defeat doctrine 5개의 blocker predicate
    (자초한 심신장애·자초한 강요상태·위난감수의무·승낙의 법률상 제한)는 다른 어디에도
    등장하지 않으므로 이 경로가 유일한 입구다.
    """
    from idpr.v2 import expressions
    from idpr.v2.closure import compile_closure

    registry = load_definitions(ROOT / "data/v2/definitions")
    seeds = tuple(
        sorted(entry.id for entry in (*registry.by_kind["offense"], *registry.by_kind["derived_offense"]))
    )
    closure = compile_closure(registry, seeds)
    # ground_fact는 frontier로, legal_element는 deferred로 나간다. blocker leaf는 둘 다
    # 나오므로 어느 한쪽만 보면 통과해 버린다.
    collected = {
        ref
        for group in (closure.items, closure.completion_probes, closure.doctrine_probes)
        for item in group
        for ref in (
            *(fact.ground_fact_ref for fact in item.ground_fact_frontier),
            *item.deferred_refs,
        )
    }

    blocker_leaves = {
        ref
        for entry in registry.by_kind["doctrine"]
        for ref in expressions.leaf_refs(entry.payload.get("blocked_when"))
    }
    for entry in registry.by_kind["completion_policy"]:
        for state in entry.payload["states"].values():
            blocker_leaves |= set(expressions.leaf_refs(state.get("blocked_when")))

    assert blocker_leaves, "저작된 blocker가 없으면 이 테스트는 아무것도 지키지 않는다"
    assert blocker_leaves <= collected, sorted(blocker_leaves - collected)
