"""build-order step 6A -- idpr.v2.runtime.stages: stage invariants and the trace/conclusion split."""

from __future__ import annotations

import pytest

from idpr.v2.evaluate import TRUE, UNKNOWN
from idpr.v2.runtime.stages import (
    AppliedEffect,
    CulpabilityState,
    FormProgram,
    StageResult,
    completed_program,
    not_reached,
)


def _effect(truth=TRUE) -> AppliedEffect:
    return AppliedEffect(
        doctrine_ref="doctrine.self_defense",
        effect="DEFEAT",
        stage="unlawfulness",
        modifier_ref=None,
        truth=truth,
    )


def test_not_reached_has_no_legal_state_gate_state_or_effects():
    stage = not_reached()

    assert stage.evaluation_state == "not_reached"
    assert stage.legal_state is None
    assert stage.gate_state is None
    assert stage.effects == ()


def test_evaluated_stage_requires_both_legal_and_gate_state():
    """Type annotations permit `evaluated` with None fields; __post_init__ does not."""
    with pytest.raises(ValueError):
        StageResult(evaluation_state="evaluated", legal_state=None, gate_state=None)
    with pytest.raises(ValueError):
        StageResult(evaluation_state="evaluated", legal_state="preserved", gate_state=None)
    with pytest.raises(ValueError):
        StageResult(evaluation_state="evaluated", legal_state=None, gate_state="passes")


def test_not_reached_stage_may_not_carry_legal_state():
    with pytest.raises(ValueError):
        StageResult(
            evaluation_state="not_reached", legal_state="preserved", gate_state="passes"
        )


def test_not_reached_stage_may_not_carry_effects():
    """An effect on an unreached stage is a hypothetical ("self-defense *would have* applied").

    v2.2.0 section 24 keeps hypothetical reasoning out of symbolic state entirely.
    """
    with pytest.raises(ValueError):
        StageResult(
            evaluation_state="not_reached",
            legal_state=None,
            gate_state=None,
            effects=(_effect(),),
        )


def test_not_reached_is_never_a_legal_state():
    """Section 4.4: no legal state enum admits `not_reached` as a value."""
    for state_type in (CulpabilityState,):
        assert "not_reached" not in state_type.__args__


def test_evaluated_stage_may_carry_unknown_effects():
    """A potential-but-unresolved effect must survive so the result explains its own unresolved."""
    stage = StageResult(
        evaluation_state="evaluated",
        legal_state="unresolved",
        gate_state="unresolved",
        effects=(_effect(truth=UNKNOWN),),
    )

    assert stage.effects[0].truth == UNKNOWN


def test_completed_program_is_the_only_6a_shape():
    program = completed_program()

    assert program.form == "completed"
    assert program.punishable is True
    assert program.suspended_slots == frozenset()
    assert program.extra is None
    assert program.relation_dispositions == {}


def test_form_program_carries_punishability_of_the_form():
    """CompletionPolicy.punishable must survive compilation into the executable program.

    Distinct from the Punishability stage's EXEMPT: this says whether the incomplete *form* is a
    punishable legal shape at all, not whether an established offense is exempted.
    """
    program = FormProgram(form="preparation", punishable=False)

    assert program.punishable is False
    assert "punishable" in FormProgram.__dataclass_fields__
