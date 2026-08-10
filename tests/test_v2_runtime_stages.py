"""build-order step 6A -- idpr.v2.runtime.stages: stage invariants and the trace/conclusion split."""

from __future__ import annotations

import pytest

from idpr.v2.evaluate import TRUE, UNKNOWN
from idpr.v2.runtime.stages import (
    AppliedEffect,
    Article151OffenderStatusObligation,
    ComponentSlotObligation,
    CoPrincipalConstitutiveStatusObligation,
    CompletionRequirementObligation,
    CulpabilityState,
    IndirectPrincipalDependencyObligation,
    Obligation,
    ParticipationDependencyObligation,
    ParticipationRequirementObligation,
    RelationObligation,
    SlotObligation,
    StageResult,
    StatutoryDeemingObligation,
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


def test_obligation_union_contains_only_explicitly_evaluable_runtime_units():
    """Deliberately no `PredicateObligation(ref)`.

    `evaluate()` returns one TruthValue and an expression can be FALSE with no FALSE leaf in it
    (`NOT(A)` with A=TRUE, `ONE_OF(A, B)` with both TRUE), so a "decisive leaf" would require a
    second, unsound evaluator in the pipeline. The original five are what the evaluator can name
    honestly. `CompletionRequirementObligation` replaced the earlier `FormRequirementObligation`
    when the form abstraction was removed -- the obligation it names now belongs to a completion
    STATE, not to a selected program. `ParticipationDependencyObligation`/
    `ParticipationRequirementObligation` (step 6C) name the two obligations a derivative
    participant's (instigator/aider) Elements folds -- principal-realization gate and own
    `requires`, never a re-evaluation of the principal's `CompiledOffense`. Phase 5.1 adds five
    concrete obligations (Articles 33, 151, 263, 34, and 339); none is a generic predicate trace.
    """
    assert set(Obligation.__args__) == {
        SlotObligation,
        RelationObligation,
        CompletionRequirementObligation,
        ParticipationDependencyObligation,
        ParticipationRequirementObligation,
        CoPrincipalConstitutiveStatusObligation,
        Article151OffenderStatusObligation,
        StatutoryDeemingObligation,
        IndirectPrincipalDependencyObligation,
        ComponentSlotObligation,
    }
    assert set(CompletionRequirementObligation.__dataclass_fields__) == {"state"}
    assert set(ParticipationDependencyObligation.__dataclass_fields__) == {"mode"}
    assert set(ParticipationRequirementObligation.__dataclass_fields__) == {"mode"}
    IndirectPrincipalDependencyObligation,
