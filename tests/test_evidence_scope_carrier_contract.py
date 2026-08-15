"""Whole-axis closure for evidence carrier typing.

The planner decides how much factual record each predicate is asked about.  When that
decision ignores the predicate's authored `evidence_scope`, the target is structurally
unanswerable however good the model is: `same_actor_episode` predicates were receiving a
carrier that held roughly half the actor's episode, and 자기이득 목적 was collapsed to a
single action against its own `offense_realization` declaration.

These tests pin the contract itself rather than any one run:

* an explicitly authored scope always wins, including over the generic actor-bound
  GroundFact narrowing, because `actor_episode` is already actor-filtered;
* an unauthored predicate gets `offense_realization` -- the realization's own actions;
* `temporal_anchor` narrows *when*, never *how much*;
* participation targets are outside this contract by design and carry a typed relation
  carrier, audited on the participation axis instead.

With this green, a wrong truth on a real question is a model error, not evidence
starvation, and the axis is not reopened for it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import predicate_definitions
from idpr.v2.runtime.grounding_evidence import actor_bound_ground_fact

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
PLAN = (
    ROOT
    / "experiments/v2_unknown_reduction_26/plan_doctrine"
    / "evaluation_instance_plan.jsonl"
)

DEFAULT_SCOPE = "offense_realization"
CARRIER_FOR_SCOPE = {
    "exact_actor_action": "focal_action",
    "offense_realization": "realization",
    "same_actor_episode": "actor_episode",
    "typed_relation": "realization",
}
PARTICIPATION_CARRIER = "participation_action_or_realization"


def _authored_scope(predicate_ref: str) -> str:
    entry = REGISTRY.get(predicate_ref)
    if entry is None:
        return DEFAULT_SCOPE
    return str(entry.payload.get("evidence_scope") or DEFAULT_SCOPE)


def _expected_carrier(predicate_ref: str) -> str:
    """The carrier the contract owes this predicate.

    An authored scope decides outright.  Only an unauthored predicate falls through to
    the generic actor-bound narrowing, which keeps a bare actor-local GroundFact on its
    own action so no peer's conduct is read as this actor's.
    """
    entry = REGISTRY.get(predicate_ref)
    if entry is not None and entry.payload.get("evidence_scope"):
        return CARRIER_FOR_SCOPE[str(entry.payload["evidence_scope"])]
    if (
        entry is not None
        and entry.kind == "ground_fact"
        and actor_bound_ground_fact(REGISTRY, predicate_ref)
    ):
        return "focal_action"
    return CARRIER_FOR_SCOPE[DEFAULT_SCOPE]


def _carriers():
    if not PLAN.exists():  # pragma: no cover - guarded by the skip below
        return []
    rows = [json.loads(line) for line in PLAN.read_text(encoding="utf-8").splitlines() if line]
    return [
        (row["sub_question_id"], carrier)
        for row in rows
        for carrier in row.get("assessment_carriers") or []
    ]


def _actor_in_focal():
    """Per occurrence, whether the liable actor takes part in its focal action.

    An accessory's focal action is the principal's execution, so a focal-only carrier
    would name an actor it never mentions.  Those widen to the realization by contract.
    """
    if not PLAN.exists():  # pragma: no cover - guarded by the skip below
        return {}
    rows = [json.loads(line) for line in PLAN.read_text(encoding="utf-8").splitlines() if line]
    # One occurrence can carry several provenance rows -- the participation builder
    # appends its own, focal-less entry alongside the planner's.  A focal carrier is
    # legitimate as soon as any row records the actor inside the focal action.
    resolved: dict[tuple[str, str], bool] = {}
    for row in rows:
        for value in row.get("instance_provenance") or []:
            key = (row["sub_question_id"], value["instance_key"]["occurrence_id"])
            resolved[key] = resolved.get(key, False) or bool(
                value.get("actor_in_focal_action")
            )
    return resolved


pytestmark = pytest.mark.skipif(
    not PLAN.exists(), reason="26-question plan artifact is not built in this checkout"
)


def test_every_predicate_is_carried_at_its_authored_scope() -> None:
    mismatches = []
    actor_in_focal = _actor_in_focal()
    for case_id, carrier in _carriers():
        kind = str(carrier["carrier_kind"])
        base = kind.removesuffix("_at_focal")
        if base == PARTICIPATION_CARRIER:
            continue
        expected = _expected_carrier(str(carrier["predicate_ref"]))
        if expected == "focal_action" and not actor_in_focal.get(
            (case_id, carrier["instance_key"]["occurrence_id"]), True
        ):
            expected = "realization"
        if base != expected:
            mismatches.append((case_id, carrier["predicate_ref"], expected, kind))
    assert not mismatches, (
        f"{len(mismatches)} targets are carried at a width their definition did not "
        f"authorize, e.g. {mismatches[:5]}"
    )


def test_authored_scope_outranks_the_generic_actor_bound_narrowing() -> None:
    """The safety rule may only decide predicates that authored no scope of their own."""
    offenders = [
        (case_id, carrier["predicate_ref"])
        for case_id, carrier in _carriers()
        if str(carrier["carrier_kind"]).removesuffix("_at_focal") != PARTICIPATION_CARRIER
        and (REGISTRY.get(str(carrier["predicate_ref"])) or None) is not None
        and REGISTRY.get(str(carrier["predicate_ref"])).payload.get("evidence_scope")
        == "same_actor_episode"
        and actor_bound_ground_fact(REGISTRY, str(carrier["predicate_ref"]))
        and str(carrier["carrier_kind"]).removesuffix("_at_focal") != "actor_episode"
    ]
    assert not offenders, (
        f"actor-bound narrowing overrode an explicit same_actor_episode scope: {offenders[:5]}"
    )


def test_temporal_anchor_narrows_time_without_narrowing_scope() -> None:
    """A `temporal_anchor` predicate keeps its authored width and only loses later actions."""
    anchored = [
        carrier
        for _case_id, carrier in _carriers()
        if (REGISTRY.get(str(carrier["predicate_ref"])) or None) is not None
        and REGISTRY.get(str(carrier["predicate_ref"])).payload.get("temporal_anchor")
        == "focal_action"
    ]
    assert anchored, "no temporal_anchor predicate is exercised by the 26-question plan"
    for carrier in anchored:
        kind = str(carrier["carrier_kind"])
        assert kind.endswith("_at_focal"), carrier
        assert kind.removesuffix("_at_focal") == _expected_carrier(
            str(carrier["predicate_ref"])
        ), carrier


def test_participation_targets_use_their_own_typed_carrier() -> None:
    """Participation is a relation judgement, not an actor-local fact, and is audited apart."""
    for case_id, carrier in _carriers():
        kind = str(carrier["carrier_kind"]).removesuffix("_at_focal")
        if kind != PARTICIPATION_CARRIER:
            continue
        assert str(carrier["carrier_id"]), (case_id, carrier)


def test_the_scope_told_to_the_model_is_the_scope_it_is_carried_at() -> None:
    """축 테스트가 초록인데 neural 경계에서 split-brain이던 자리.

    planner는 미저작 predicate에 realization carrier를 붙이면서, Call 2 payload의 predicate
    정의에는 옛 기본값 `exact_actor_action`을 적어 보냈다. 모델은 realization 전체를 받고
    "그 행위만 보고 판단하라"는 지시를 함께 받는다 -- 사실이 있어도 UNKNOWN이 나올 수 있는
    모순된 요청이다. 두 값은 한 계약에서 나와야 한다.
    """
    refs = sorted(
        entry.id
        for kind in ("ground_fact", "legal_element")
        for entry in REGISTRY.by_kind.get(kind, ())
    )
    serialized = {
        value.predicate_ref: value.evidence_scope
        for value in predicate_definitions(REGISTRY, refs)
    }
    mismatches = [
        (ref, serialized[ref], _expected_carrier(ref))
        for ref in refs
        if CARRIER_FOR_SCOPE[serialized[ref]] != _expected_carrier(ref)
    ]
    assert not mismatches, mismatches
