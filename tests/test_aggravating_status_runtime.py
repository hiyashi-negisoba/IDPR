"""형법 제33조 단서. r14_p1_q1 형태: 甲(직계비속)이 乙에게 甲의 아버지 살해를 교사."""

from pathlib import Path

import pytest

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.aggravating_status import (
    AggravatingStatusError,
    redirect_by_aggravating_status,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

STATUS = "legal_element.lineal_ascendant_of_self_or_spouse_status"
ACCESSORY = OffenseInstanceKey("case", "甲", "offense.homicide", "binding:001")


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def _redirect(registry, status_truth, mode="instigator"):
    truths = CaseTruths(predicate={(ACCESSORY, STATUS): status_truth})
    return redirect_by_aggravating_status(
        registry,
        accessory_instance=ACCESSORY,
        principal_offense_ref="offense.homicide",
        mode=mode,
        truths=truths,
    )


def test_a_lineal_descendant_instigator_is_redirected_to_ancestral_homicide(registry) -> None:
    redirection = _redirect(registry, TRUE)
    assert redirection is not None
    assert redirection.aggravated_offense_ref == "offense.ancestral_homicide"
    # identity is preserved except for the offense itself
    assert redirection.accessory_instance == OffenseInstanceKey(
        "case", "甲", "offense.ancestral_homicide", "binding:001"
    )


def test_an_unknown_status_never_upgrades_the_charge(registry) -> None:
    """모르는 신분으로 죄책을 올리는 것은 host가 UNKNOWN을 repair하는 것과 같다."""
    assert _redirect(registry, UNKNOWN) is None
    assert _redirect(registry, FALSE) is None


def test_co_principal_is_in_scope(registry) -> None:
    """검수 ②-b: 제33조는 제30조부터 제32조까지를 대상으로 한다."""
    assert _redirect(registry, TRUE, mode="co_principal") is not None
    assert _redirect(registry, TRUE, mode="aider") is not None


def test_a_mode_outside_applies_to_modes_is_left_alone(registry) -> None:
    assert _redirect(registry, TRUE, mode="principal") is None


def test_an_unrelated_principal_offense_is_left_alone(registry) -> None:
    truths = CaseTruths(predicate={(ACCESSORY, STATUS): TRUE})
    assert (
        redirect_by_aggravating_status(
            registry,
            accessory_instance=ACCESSORY,
            principal_offense_ref="offense.theft",
            mode="instigator",
            truths=truths,
        )
        is None
    )


def test_two_claimants_hard_fail_rather_than_being_ranked(registry) -> None:
    """A second authored offense claiming the same base/mode is an authoring error, and picking
    one by id order would hide it behind a plausible-looking answer."""
    twin = registry.get("offense.ancestral_homicide")
    clone = type(twin)(
        id="offense.ancestral_homicide_twin",
        kind="offense",
        payload=twin.payload,
        source_file=twin.source_file,
    )
    patched = type(registry)(
        by_id={**registry.by_id, clone.id: clone},
        by_kind={**registry.by_kind, "offense": (*registry.by_kind["offense"], clone)},
    )
    truths = CaseTruths(predicate={(ACCESSORY, STATUS): TRUE})
    with pytest.raises(AggravatingStatusError, match="multiple aggravating-status"):
        redirect_by_aggravating_status(
            patched,
            accessory_instance=ACCESSORY,
            principal_offense_ref="offense.homicide",
            mode="instigator",
            truths=truths,
        )
