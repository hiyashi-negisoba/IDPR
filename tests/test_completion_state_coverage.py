"""Whole-axis closure for completion states.

This is not a sample of interesting cases.  It sweeps every truth assignment over every
predicate each policy reads and asserts two structural properties for all of them:

1. every declared state is reachable -- a state no assignment can confirm is dead authoring,
   which is how `attempted` sat at zero firings across all 26 questions while looking correct
   in the YAML;
2. any two states that can hold at once have an authored `defeated_by_state`, since an
   undeclared collision resolves to `unresolved` forever.

Once this passes, a wrong completion state on a real question is a model error, not a
structural one, and the axis does not get reopened for it.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
from typing import Any

import pytest
import yaml

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import (
    completion_policy_for,
    component_instance_for,
    resolve_completion,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
POLICIES = yaml.safe_load((ROOT / "data/v2/definitions/completion_policies.yaml").read_text())
TRUTH_VALUES = (TRUE, FALSE, UNKNOWN)


def _predicate_refs(node: Any, acc: set[str]) -> set[str]:
    if isinstance(node, dict):
        if node.get("op") == "ref":
            acc.add(str(node["ref"]))
        for value in node.values():
            _predicate_refs(value, acc)
    elif isinstance(node, list):
        for value in node:
            _predicate_refs(value, acc)
    return acc


def _scoped_instances(
    policy: dict[str, Any], compiled: CompiledOffense, instance: OffenseInstanceKey
) -> set[OffenseInstanceKey]:
    """Every instance key this policy's conditions are evaluated against.

    A `when_component` state reads its component's predicate view, so truths keyed only on the
    top-level instance would leave it permanently unknown and every state falsely unreachable.
    """
    targets = {instance}
    for state in policy["states"].values():
        scope = state.get("when_component")
        if scope:
            targets.add(
                component_instance_for(compiled, instance, scope["local_key"], scope["offense"])
            )
    return targets


def _sweep(policy: dict[str, Any]) -> tuple[set[str], list[tuple[str, ...]]]:
    """Return the states reached, and the confirmed-state collisions with no authored yield."""
    offense_ref = policy["offense"]
    compiled = compile_offense(REGISTRY, offense_ref)
    assert isinstance(compiled, CompiledOffense), offense_ref
    entry = completion_policy_for(REGISTRY, offense_ref)
    instance = OffenseInstanceKey("case", "actor", offense_ref, "occurrence")
    targets = _scoped_instances(policy, compiled, instance)
    refs = sorted(_predicate_refs(policy["states"], set()))

    reached: set[str] = set()
    collisions: list[tuple[str, ...]] = []
    for combination in product(TRUTH_VALUES, repeat=len(refs)):
        assignment = dict(zip(refs, combination))
        truths = CaseTruths(
            predicate={
                (target, ref): truth
                for target in targets
                for ref, truth in assignment.items()
            }
        )
        result = resolve_completion(entry, compiled, instance, truths)
        reached.add(result.state)
        if result.state != "unresolved":
            continue
        confirmed = tuple(
            sorted(
                outcome.state for outcome in result.provenance if outcome.truth == TRUE
            )
        )
        if len(confirmed) >= 2 and confirmed not in collisions:
            collisions.append(confirmed)
    return reached, collisions


@pytest.mark.parametrize("policy", POLICIES, ids=lambda value: value["offense"])
def test_every_declared_completion_state_is_reachable(policy: dict[str, Any]) -> None:
    reached, _ = _sweep(policy)
    unreachable = sorted(set(policy["states"]) - reached)
    assert not unreachable, (
        f"{policy['offense']}: {unreachable} can never be confirmed by any truth assignment"
    )


@pytest.mark.parametrize("policy", POLICIES, ids=lambda value: value["offense"])
def test_simultaneous_completion_states_have_an_authored_yield(policy: dict[str, Any]) -> None:
    _, collisions = _sweep(policy)
    assert not collisions, (
        f"{policy['offense']}: {collisions} can hold at once with no defeated_by_state -- "
        "the instance would stay unresolved forever"
    )
