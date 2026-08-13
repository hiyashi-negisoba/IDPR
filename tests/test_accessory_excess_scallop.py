"""Scallop parity for 공범의 초과. Host classifies; Scallop re-derives; the two must agree."""

from pathlib import Path

import pytest

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.excess import classify_excess
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.scallop_backend import (
    ScallopBackendContractError,
    run_accessory_excess_program,
    validate_accessory_excess_rows,
)

ACCESSORY = OffenseInstanceKey("case", "甲", "derived_offense.special_theft", "binding:001")


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


@pytest.fixture(scope="module")
def policy(registry):
    return registry.get("excess_policy.korean_law_standard")


def _row(registry, policy, instigated, realized, foreseeability=UNKNOWN, actor="甲"):
    instance = OffenseInstanceKey("case", actor, realized, "binding:001")
    assessment = classify_excess(
        registry,
        policy,
        instigated_offense_ref=instigated,
        realized_offense_ref=realized,
        participant_foreseeability=foreseeability,
    )
    return (instance, instigated, assessment, foreseeability)


def test_every_classification_lowers_and_agrees_with_the_host(registry, policy, tmp_path) -> None:
    rows = (
        _row(registry, policy, "offense.theft", "derived_offense.special_theft", actor="甲"),
        _row(
            registry, policy, "offense.robbery",
            "derived_offense.robbery_causing_death_by_aggravated_result", TRUE, actor="乙",
        ),
        _row(
            registry, policy, "offense.robbery",
            "derived_offense.robbery_causing_death_by_aggravated_result", FALSE, actor="丙",
        ),
        _row(
            registry, policy, "offense.robbery",
            "derived_offense.robbery_causing_death_by_aggravated_result", UNKNOWN, actor="丁",
        ),
        _row(registry, policy, "offense.theft", "offense.injury", actor="戊"),
        _row(registry, policy, "offense.theft", "offense.dwelling_intrusion", actor="己"),
    )
    result = run_accessory_excess_program(rows, work_dir=tmp_path)

    effects = {
        (instance.actor_id, instigated): result[(instance, instigated)]
        for instance, instigated, _, _ in rows
    }
    assert effects[("甲", "offense.theft")] == "liable_for_instigated_scope"
    assert effects[("乙", "offense.robbery")] == "liable_for_aggravated_result"
    assert effects[("丙", "offense.robbery")] == "liable_for_instigated_scope"
    assert effects[("丁", "offense.robbery")] == "unresolved"
    assert effects[("戊", "offense.theft")] == "no_liability_for_excess"
    # 검수 ③-a: 저작되지 않은 관계는 Scallop에서도 질적 초과가 아니라 미해결이다.
    assert effects[("己", "offense.theft")] == "unresolved"


def test_a_scallop_effect_disagreeing_with_the_host_is_fatal(registry, policy) -> None:
    """The parity check must not accept whichever side answered -- it exists to catch drift."""
    rows = (_row(registry, policy, "offense.theft", "derived_offense.special_theft"),)
    forged = ((*[f for f in ("case", "甲", "derived_offense.special_theft", "binding:001")],
               "offense.theft", "no_liability_for_excess"),)
    with pytest.raises(ScallopBackendContractError, match="disagrees with host classifier"):
        validate_accessory_excess_rows(forged, rows)


def test_a_missing_row_is_incomplete_rather_than_no_excess(registry, policy) -> None:
    rows = (_row(registry, policy, "offense.theft", "derived_offense.special_theft"),)
    with pytest.raises(ScallopBackendContractError, match="incomplete"):
        validate_accessory_excess_rows((), rows)
