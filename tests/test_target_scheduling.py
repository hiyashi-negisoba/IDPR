"""The scheduler must never ask a question whose answer cannot matter.

The regression these guard is concrete: on 14 instances in the frozen 26-question run,
`legal_element.dangerousness` was assessed where `ground_fact.means_or_object_defect` was
already FALSE, and the resulting UNKNOWN was written into the answer as legal uncertainty.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import expressions
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, evaluate
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.target_scheduling import (
    frontier_predicate_refs,
    is_decisive,
    live_predicate_refs,
    next_round_targets,
)
from scripts.run_v2_call2_pilot import _recorded_request_counts

DEFINITIONS = Path(__file__).resolve().parents[1] / "data/v2/definitions"

DANGEROUSNESS = "legal_element.dangerousness"
DEFECT = "ground_fact.means_or_object_defect"
COMMENCEMENT = "legal_element.commencement_of_execution"
DEATH = "ground_fact.death_of_victim"


@pytest.fixture(scope="module")
def registry():
    return load_definitions(DEFINITIONS)


def instance(offense_ref: str = "offense.homicide") -> OffenseInstanceKey:
    return OffenseInstanceKey(
        case_id="case", actor_id="甲", offense_ref=offense_ref, occurrence_id="binding:001"
    )


def test_dangerousness_dies_with_the_defect_that_gates_it(registry):
    settled = {COMMENCEMENT: TRUE, DEATH: FALSE, DEFECT: FALSE}
    assert DANGEROUSNESS not in live_predicate_refs(registry, instance(), settled)
    assert DANGEROUSNESS not in frontier_predicate_refs(registry, instance(), settled)


def test_dangerousness_is_asked_once_the_defect_is_established(registry):
    settled = {COMMENCEMENT: TRUE, DEATH: FALSE, DEFECT: TRUE}
    assert DANGEROUSNESS in live_predicate_refs(registry, instance(), settled)
    assert DANGEROUSNESS in frontier_predicate_refs(registry, instance(), settled)


def test_a_later_conjunct_waits_for_the_one_before_it(registry):
    """Live and ready are different questions: nothing is skipped, only deferred."""
    nothing_known: dict[str, str] = {}
    live = live_predicate_refs(registry, instance(), nothing_known)
    frontier = frontier_predicate_refs(registry, instance(), nothing_known)
    assert DANGEROUSNESS in live
    assert DANGEROUSNESS not in frontier
    assert set(frontier) <= set(live)


def test_three_valued_substitution_is_not_a_binary_flip():
    """A predicate can matter even when TRUE and FALSE agree on the answer.

    `ONE_OF(A, NOT(A))` is exactly one of its branches whichever way A lands, so both
    settings evaluate TRUE -- but leaving A unasked leaves it UNKNOWN, because ONE_OF is
    truth-functional over each child's own value and two UNKNOWNs cannot be counted.  A
    TRUE/FALSE comparison sees no difference here and would drop the target, stranding the
    expression at UNKNOWN forever.  The three-valued rule keeps it.
    """
    expr = expressions.canonicalize(
        {
            "op": "one_of",
            "args": [
                {"op": "ref", "ref": "a"},
                {"op": "not", "arg": {"op": "ref", "ref": "a"}},
            ],
        }
    )
    truths = {"a": UNKNOWN}
    assert evaluate(expr, truths) == UNKNOWN
    assert {evaluate(expr, {"a": value}) for value in (TRUE, FALSE)} == {TRUE}
    assert is_decisive(expr, "a", truths)


def test_the_loop_reaches_a_fixpoint_and_covers_the_live_set(registry):
    """Rounds converge, and laddering defers work without losing it.

    The scenario is an attempted killing on facts carrying no mistake of means or object:
    the victim does not die and the defect is absent, so the impossible-attempt branch
    dies and its remaining conjunct must never be requested -- while the branch that is
    still open goes on to ask its own later conjuncts.
    """
    target = instance()
    answers = {DEATH: FALSE, DEFECT: FALSE}
    truths: dict[str, str] = {}
    asked: set[str] = set()
    rounds = 0
    while True:
        batch = next_round_targets(
            registry, [target], {target: truths}, already_asked={target: asked}
        )
        if not batch:
            break
        rounds += 1
        assert rounds < 20, "scheduler did not converge"
        for _, ref in batch:
            asked.add(ref)
            truths[ref] = answers.get(ref, TRUE)
    assert rounds > 1, "a single round means the ladder never engaged"
    assert DEFECT in asked, "the gating conjunct itself must still be asked"
    assert DANGEROUSNESS not in asked, "asked a question behind a guard that had died"
    # Nothing live is left unasked when the loop stops.
    assert not set(live_predicate_refs(registry, target, truths)) - asked


def test_an_unanswered_target_cannot_spin_the_loop(registry):
    """Call 2 declining a target must end the round, not repeat it."""
    target = instance()
    batch = next_round_targets(registry, [target], {target: {}})
    assert batch
    asked = {ref for _, ref in batch}
    again = next_round_targets(registry, [target], {target: {}}, already_asked={target: asked})
    assert all(ref not in asked for _, ref in again)


def test_an_assessed_unknown_stops_the_ladder(registry):
    """UNKNOWN이 논리적으로 ALL을 죽이지는 않지만, 그 뒤를 묻는 값은 실측에 없었다.

    예전에는 뒤 conjunct가 FALSE로 와서 guard를 죽일 수 있다는 이유로 계속 걸어갔다.
    2026-08-16 측정에서 `dangerousness`는 upstream `means_or_object_defect`가 UNKNOWN인
    채로 14번 열렸고 FALSE는 0번이었다. 얻은 것은 UNKNOWN 13건이고, TRUE 1건은 defect
    없이는 불능미수 판정에 쓸 수 없는 값이었다. 그래서 여기서 멈춘다.
    """
    target = instance()
    known = {COMMENCEMENT: TRUE, DEATH: FALSE, DEFECT: UNKNOWN}
    batch = next_round_targets(
        registry,
        [target],
        {target: known},
        already_asked={target: set(known)},
        candidate_refs={target: {COMMENCEMENT, DEATH, DEFECT, DANGEROUSNESS}},
    )
    assert batch == ()


def test_scheduling_does_not_depend_on_the_blocker_being_a_ground_fact(registry):
    """The blocker here is `commencement_of_execution`, a legal_element.

    Nothing in the scheduler knows that ground facts tend to gate legal elements.  With no
    commencement of execution, all three attempt states die at once and every predicate
    reachable only through them stops being asked -- including `voluntary_cessation_or_
    prevention`, which is itself a legal_element and which stays live while those states
    are open.
    """
    cessation = "legal_element.voluntary_cessation_or_prevention"
    open_states = live_predicate_refs(registry, instance(), {DEATH: FALSE})
    assert cessation in open_states
    assert DEFECT in open_states

    blocked = live_predicate_refs(registry, instance(), {DEATH: FALSE, COMMENCEMENT: FALSE})
    assert cessation not in blocked
    assert DEFECT not in blocked
    assert DANGEROUSNESS not in blocked


def test_request_counts_cover_every_scheduling_round():
    shards = [
        {"shard_kind": "predicate", "scheduling_round": 1, "target_count": 7},
        {"shard_kind": "predicate", "scheduling_round": 2, "target_count": 2},
        {"shard_kind": "relation", "target_count": 3},
    ]
    assert _recorded_request_counts(shards, article263_requested=True) == (4, 9)
