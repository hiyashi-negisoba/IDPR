"""build-order step 6A -- idpr.v2.runtime.effects: activated doctrine set + stage-level fold."""

from __future__ import annotations

import pytest

from idpr.v2.evaluate import FALSE, TRUE
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime.effects import StageEffectError, resolve_stage
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

_INSTANCE = OffenseInstanceKey("C1", "甲", "offense.embezzlement", "o1")


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, []).append(
        DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>")
    )
    by_id: dict[str, DefinitionEntry] = {}
    frozen = {}
    for k, entries in by_kind.items():
        frozen[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen)


def _doctrine(registry, doctrine_id, stage, effect, ref, modifier_ref=None):
    payload = {
        "id": doctrine_id,
        "stage": stage,
        "requires": {"op": "ref", "ref": ref},
        "effect": {"effect": effect, "stage": stage},
    }
    if modifier_ref is not None:
        payload["effect"]["modifier_ref"] = modifier_ref
    return _add(registry, "doctrine", payload)


def _truths(**refs) -> CaseTruths:
    return CaseTruths(predicate={(_INSTANCE, ref): value for ref, value in refs.items()})


def _registry():
    registry = load_definitions()
    registry = _doctrine(
        registry, "doctrine.t_self_defense", "unlawfulness", "DEFEAT", "gf.attack"
    )
    registry = _doctrine(registry, "doctrine.t_necessity", "unlawfulness", "DEFEAT", "gf.peril")
    registry = _doctrine(registry, "doctrine.t_insanity", "culpability", "DEFEAT", "gf.insane")
    registry = _doctrine(
        registry,
        "doctrine.t_diminished",
        "culpability",
        "MODIFY",
        "gf.impaired",
        modifier_ref="modifier.culpability.diminished",
    )
    registry = _doctrine(registry, "doctrine.t_kinship", "punishability", "EXEMPT", "gf.kin")
    return registry


def test_unrelated_unknown_doctrines_do_not_collapse_stage_to_unresolved():
    """The runtime consumes an activated set, not the whole registry.

    The registry holds every justification/excuse doctrine in the General Part. If the runtime
    evaluated all of them, each unprobed one would be UNKNOWN and a single UNKNOWN DEFEAT drags the
    stage to unresolved -- so a plain theft case would report unresolved Unlawfulness because
    nobody disproved 긴급피난.
    """
    registry = _registry()
    assert len(registry.by_kind["doctrine"]) >= 5

    stage = resolve_stage("unlawfulness", frozenset(), registry, _INSTANCE, _truths())

    assert stage.legal_state == "preserved"
    assert stage.gate_state == "passes"


def test_confirmed_defeat_wins_over_other_unknown_justification():
    """self_defense=TRUE with necessity=UNKNOWN is defeated, not unresolved.

    Deciding per doctrine instead of folding the pool would let an unrelated open question undo a
    settled one.
    """
    stage = resolve_stage(
        "unlawfulness",
        frozenset({"doctrine.t_self_defense", "doctrine.t_necessity"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.attack": TRUE}),
    )

    assert stage.legal_state == "defeated"
    assert stage.gate_state == "fails"


def test_unknown_defeat_blocks_the_gate():
    stage = resolve_stage(
        "unlawfulness",
        frozenset({"doctrine.t_self_defense"}),
        _registry(),
        _INSTANCE,
        _truths(),
    )

    assert stage.legal_state == "unresolved"
    assert stage.gate_state == "unresolved"


def test_all_false_defeats_leave_the_stage_preserved():
    stage = resolve_stage(
        "unlawfulness",
        frozenset({"doctrine.t_self_defense", "doctrine.t_necessity"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.attack": FALSE, "gf.peril": FALSE}),
    )

    assert (stage.legal_state, stage.gate_state) == ("preserved", "passes")


def test_unknown_modify_does_not_claim_preserved():
    """With MODIFY unresolved the culpability state is genuinely unknown, not preserved.

    Reporting `preserved` would assert a stronger legal conclusion than the evidence supports.
    """
    stage = resolve_stage(
        "culpability",
        frozenset({"doctrine.t_insanity", "doctrine.t_diminished"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.insane": FALSE}),
    )

    assert stage.legal_state == "unresolved"


def test_unknown_modify_still_passes_the_establishment_gate():
    """Section 13.2 admits both preserved and diminished, so an open MODIFY cannot close the gate."""
    stage = resolve_stage(
        "culpability",
        frozenset({"doctrine.t_insanity", "doctrine.t_diminished"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.insane": FALSE}),
    )

    assert stage.gate_state == "passes"


def test_confirmed_modify_yields_diminished_and_still_passes():
    stage = resolve_stage(
        "culpability",
        frozenset({"doctrine.t_insanity", "doctrine.t_diminished"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.insane": FALSE, "gf.impaired": TRUE}),
    )

    assert (stage.legal_state, stage.gate_state) == ("diminished", "passes")


def test_defeat_outranks_modify_at_the_same_stage():
    """If culpability is defeated, whether it was also diminished is moot."""
    stage = resolve_stage(
        "culpability",
        frozenset({"doctrine.t_insanity", "doctrine.t_diminished"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.insane": TRUE, "gf.impaired": TRUE}),
    )

    assert (stage.legal_state, stage.gate_state) == ("defeated", "fails")


def test_unknown_exempt_blocks_the_gate_unlike_unknown_modify():
    """EXEMPT changes the outcome, so leaving it open leaves the gate open too."""
    stage = resolve_stage(
        "punishability",
        frozenset({"doctrine.t_kinship"}),
        _registry(),
        _INSTANCE,
        _truths(),
    )

    assert (stage.legal_state, stage.gate_state) == ("unresolved", "unresolved")


def test_modifier_ref_survives_in_applied_effects():
    """The only carrier of MODIFY's payload past the stage boundary."""
    stage = resolve_stage(
        "culpability",
        frozenset({"doctrine.t_diminished"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.impaired": TRUE}),
    )

    modifiers = [e.modifier_ref for e in stage.effects]
    assert modifiers == ["modifier.culpability.diminished"]


def test_unresolved_effects_are_kept_but_false_ones_are_not():
    """`effects` explains the stage: a potential effect matters, a disproved one is noise."""
    stage = resolve_stage(
        "unlawfulness",
        frozenset({"doctrine.t_self_defense", "doctrine.t_necessity"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.attack": FALSE}),
    )

    assert [e.doctrine_ref for e in stage.effects] == ["doctrine.t_necessity"]


def test_doctrine_of_another_stage_is_ignored_not_misapplied():
    stage = resolve_stage(
        "unlawfulness",
        frozenset({"doctrine.t_insanity"}),
        _registry(),
        _INSTANCE,
        _truths(**{"gf.insane": TRUE}),
    )

    assert (stage.legal_state, stage.effects) == ("preserved", ())


def test_elements_is_not_a_doctrine_bearing_stage():
    with pytest.raises(StageEffectError):
        resolve_stage("elements", frozenset(), _registry(), _INSTANCE, _truths())


def test_active_ref_that_is_not_a_doctrine_is_rejected():
    with pytest.raises(StageEffectError):
        resolve_stage(
            "unlawfulness",
            frozenset({"offense.robbery"}),
            _registry(),
            _INSTANCE,
            _truths(),
        )


def test_doctrine_whose_effect_targets_another_stage_is_rejected():
    """Section 24: a stage effect landing on the wrong stage is an error, not a silent no-op."""
    registry = _add(
        load_definitions(),
        "doctrine",
        {
            "id": "doctrine.t_broken",
            "stage": "unlawfulness",
            "requires": {"op": "ref", "ref": "gf.x"},
            "effect": {"effect": "DEFEAT", "stage": "culpability"},
        },
    )

    with pytest.raises(StageEffectError):
        resolve_stage(
            "unlawfulness", frozenset({"doctrine.t_broken"}), registry, _INSTANCE, _truths()
        )
