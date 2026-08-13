"""저작된 참가 정책 -> Call 2 target. 제33조 단서의 dead loop를 닫는 join."""

from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import ParticipationLocalTarget
from idpr.v2.runtime.policy_probe_targets import (
    participation_candidate_probe_targets,
    unreachable_mode_findings,
)

STATUS = "legal_element.lineal_ascendant_of_self_or_spouse_status"


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def _instance(actor: str, offense: str, occurrence: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", actor, offense, occurrence)


def test_the_status_leaf_is_opened_on_the_accessory_of_a_homicide_candidate(registry) -> None:
    accessory = _instance("甲", "offense.homicide", "participation_binding:001")
    principal = _instance("乙", "offense.homicide", "binding:001")
    targets = participation_candidate_probe_targets(
        registry, (ParticipationLocalTarget("instigation", (accessory, principal)),)
    )
    assert targets == ((accessory, STATUS),)


def test_an_unrelated_offense_candidate_opens_nothing(registry) -> None:
    accessory = _instance("甲", "offense.theft", "participation_binding:001")
    principal = _instance("乙", "offense.theft", "binding:001")
    assert (
        participation_candidate_probe_targets(
            registry, (ParticipationLocalTarget("instigation", (accessory, principal)),)
        )
        == ()
    )


def test_a_co_principal_group_opens_no_target_but_is_reported(registry) -> None:
    """저작은 공동정범을 허용하는데 전환 런타임이 derivative link만 걷는다."""
    first = _instance("丁", "offense.homicide", "participation_binding:001")
    second = _instance("戊", "offense.homicide", "binding:001")
    target = ParticipationLocalTarget("co_principal_group", (first, second))
    assert participation_candidate_probe_targets(registry, (target,)) == ()
    findings = unreachable_mode_findings(registry, (target,))
    assert findings == (("offense.ancestral_homicide", "co_principal", "co_principal_group"),)


def test_a_policy_without_an_authored_mode_is_not_reported_as_unreachable(registry) -> None:
    """mode 제한이 없다는 것은 공동정범까지 발화한다는 주장이 아니다."""
    first = _instance("甲", "offense.theft", "participation_binding:001")
    second = _instance("乙", "offense.theft", "binding:001")
    findings = unreachable_mode_findings(
        registry, (ParticipationLocalTarget("co_principal_group", (first, second)),)
    )
    assert findings == ()
