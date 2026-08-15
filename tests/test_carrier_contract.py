"""target -> carrier 계약. producer를 가리지 않는다.

같은 불변식이 세 번 깨졌다. ordinary elements는 planner가, participation target은 참가
빌더가, doctrine leaf는 아무도 carrier를 붙이지 않았다. target을 만드는 모듈이 carrier도
알아서 붙이는 구조였기 때문이고, 그래서 한 곳을 고쳐도 다른 producer로 전달되지 않았다.

이 파일이 검사하는 것은 하나다 -- **누가 열었든 모든 Call 2 target은 의미적으로 맞는
carrier를 정확히 하나 갖는다.**
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.carrier_contract import (
    PARTICIPATION_CARRIER,
    CarrierContractError,
    carrier_kind_for,
    resolve_carrier,
    validate_plan_carriers,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _row(targets, carriers, provenance):
    return {
        "sub_question_id": "case",
        "assessment_targets": targets,
        "assessment_carriers": carriers,
        "instance_provenance": provenance,
    }


def _instance(offense_ref: str = "offense.theft", occurrence: str = "realization:001"):
    return {
        "case_id": "case",
        "actor_id": "甲",
        "offense_ref": offense_ref,
        "occurrence_id": occurrence,
    }


def _provenance(offense_ref="offense.theft", occurrence="realization:001", **kwargs):
    return {
        "instance_key": _instance(offense_ref, occurrence),
        "actor_in_focal_action": kwargs.get("actor_in_focal_action", True),
        "carrier_ids": kwargs.get(
            "carrier_ids",
            {
                "actor_episode": "carrier:actor_episode:甲",
                "focal_action": "carrier:focal_action:甲",
                "realization": "carrier:realization:甲",
            },
        ),
    }


# --------------------------------------------------------------------------
# 계약 자체
# --------------------------------------------------------------------------


def test_authored_evidence_scope_decides_the_carrier_kind() -> None:
    """폭은 정의의 몫이다. host가 다시 고르지 않는다."""
    # `same_actor_episode`가 저작된 요소.
    assert carrier_kind_for(
        REGISTRY, "legal_element.unlawful_appropriation_intent", actor_in_focal=True
    ) == ("actor_episode", False)
    # 저작이 없는 행위자 결박 ground fact는 일반 규칙이 초점행위로 좁힌다.
    assert carrier_kind_for(
        REGISTRY, "ground_fact.taking_conduct", actor_in_focal=True
    ) == ("focal_action", False)


def test_an_accessory_never_gets_a_focal_only_carrier() -> None:
    """가담자의 초점행위는 정범의 실행이다. 그리로 좁히면 없는 행위자를 두고 묻게 된다."""
    assert carrier_kind_for(
        REGISTRY, "ground_fact.taking_conduct", actor_in_focal=False
    ) == ("realization", False)


def test_a_participation_candidate_carries_its_own_interaction() -> None:
    """참가 후보는 planner realization이 아니다. 고를 carrier가 없고 occurrence가 곧 carrier다."""
    carrier_id, kind = resolve_carrier(
        REGISTRY,
        "legal_element.unlawful_appropriation_intent",
        provenance={"carrier_ids": {}},
        occurrence_id="participation_realization:001:002:甲:abc",
    )
    assert kind == PARTICIPATION_CARRIER
    assert carrier_id == "participation_realization:001:002:甲:abc"


def test_a_missing_carrier_kind_fails_instead_of_silently_widening() -> None:
    with pytest.raises(CarrierContractError, match="actor_episode carrier"):
        resolve_carrier(
            REGISTRY,
            "legal_element.unlawful_appropriation_intent",
            provenance={"carrier_ids": {"focal_action": "carrier:focal_action:甲"}},
            occurrence_id="realization:001",
        )


def test_an_anchored_predicate_is_never_given_an_unanchored_carrier() -> None:
    """`@focal` variant가 없을 때 고정되지 않은 carrier로 대신하지 않는다.

    대신하면 물리적으로는 초점 이후의 사실까지 들어간 carrier가 `_at_focal` label을 달고
    나간다. 모델은 label을 읽고 "초점시점 기준"으로 판단하는데 본문에는 그 뒤의 사실이
    들어 있으니, 계약은 이름만 남고 깨진다. 좁힐 수 없으면 넓히지 말고 멈춘다.
    """
    anchored = "legal_element.knowledge_of_bribery_destination"
    assert carrier_kind_for(REGISTRY, anchored, actor_in_focal=True)[1] is True
    with pytest.raises(CarrierContractError, match="realization carrier"):
        resolve_carrier(
            REGISTRY,
            anchored,
            provenance={"carrier_ids": {"realization": "carrier:realization:甲"}},
            occurrence_id="realization:001",
        )


def test_an_anchored_predicate_takes_the_anchored_carrier_when_it_exists() -> None:
    carrier_id, label = resolve_carrier(
        REGISTRY,
        "legal_element.knowledge_of_bribery_destination",
        provenance={
            "carrier_ids": {
                "realization": "carrier:realization:甲",
                "realization@focal": "carrier:realization_at_focal:甲",
            }
        },
        occurrence_id="realization:001",
    )
    assert (carrier_id, label) == ("carrier:realization_at_focal:甲", "realization_at_focal")


# --------------------------------------------------------------------------
# plan 불변식
# --------------------------------------------------------------------------


def test_a_target_without_a_carrier_fails_at_plan_time() -> None:
    """Call 2까지 가서 `missing=3`으로 알게 되지 않는다."""
    row = _row(
        [{"instance_key": _instance(), "predicate_ref": "ground_fact.taking_conduct"}],
        [],
        [_provenance()],
    )
    with pytest.raises(CarrierContractError, match="target without carrier"):
        validate_plan_carriers(REGISTRY, row)


def test_a_carrier_of_the_wrong_kind_fails_even_when_the_count_matches() -> None:
    """수량 정합만 맞고 의미적 타입이 틀린 상태를 잡는다.

    doctrine leaf 39개에 realization을 일괄로 붙였던 첫 구현이 정확히 이 모양이었다.
    """
    row = _row(
        [
            {
                "instance_key": _instance(),
                "predicate_ref": "legal_element.unlawful_appropriation_intent",
                "opened_by": "doctrine_raising_cue",
            }
        ],
        [
            {
                "instance_key": _instance(),
                "predicate_ref": "legal_element.unlawful_appropriation_intent",
                "carrier_id": "carrier:realization:甲",
                "carrier_kind": "realization",
            }
        ],
        [_provenance()],
    )
    with pytest.raises(CarrierContractError, match="does not match the authored contract"):
        validate_plan_carriers(REGISTRY, row)


def test_provenance_identity_is_the_whole_instance_not_the_occurrence() -> None:
    """절도와 특수절도가 같은 realization을 공유하고 carrier 사정이 다를 수 있다.

    occurrence_id만으로 provenance를 찾으면 뒤에 온 쪽이 앞을 덮어써서, 맞게 배정된
    carrier가 틀렸다고 보고된다.
    """
    theft = _instance("offense.theft", "realization:001")
    special = _instance("derived_offense.special_theft", "realization:001")
    row = _row(
        [{"instance_key": theft, "predicate_ref": "ground_fact.taking_conduct"}],
        [
            {
                "instance_key": theft,
                "predicate_ref": "ground_fact.taking_conduct",
                "carrier_id": "carrier:focal_action:甲",
                "carrier_kind": "focal_action",
            }
        ],
        [
            _provenance("offense.theft", "realization:001", actor_in_focal_action=True),
            # 같은 occurrence를 쓰지만 초점행위 사정이 다른 이웃.
            _provenance(
                "derived_offense.special_theft",
                "realization:001",
                actor_in_focal_action=False,
            ),
        ],
    )
    validate_plan_carriers(REGISTRY, row)


def test_a_participation_carrier_is_the_one_named_exception() -> None:
    row = _row(
        [
            {
                "instance_key": _instance(occurrence="participation_realization:a"),
                "predicate_ref": "legal_element.instigator_intent",
                "opened_by": "participation_mode_requirement",
            }
        ],
        [
            {
                "instance_key": _instance(occurrence="participation_realization:a"),
                "predicate_ref": "legal_element.instigator_intent",
                "carrier_id": "participation_realization:a",
                "carrier_kind": PARTICIPATION_CARRIER,
            }
        ],
        [_provenance(occurrence="participation_realization:a", carrier_ids={})],
    )
    validate_plan_carriers(REGISTRY, row)


def test_a_carrier_without_a_target_is_also_a_break() -> None:
    row = _row(
        [],
        [
            {
                "instance_key": _instance(),
                "predicate_ref": "ground_fact.taking_conduct",
                "carrier_id": "carrier:focal_action:甲",
                "carrier_kind": "focal_action",
            }
        ],
        [_provenance()],
    )
    with pytest.raises(CarrierContractError, match="carrier without target"):
        validate_plan_carriers(REGISTRY, row)


# --------------------------------------------------------------------------
# 실제 산출물
# --------------------------------------------------------------------------


_PRODUCED_PLAN = ROOT / "experiments/v2_axis_closure_26_e2e/plan_doctrine/evaluation_instance_plan.jsonl"


@pytest.mark.skipif(not _PRODUCED_PLAN.exists(), reason="no produced plan in the tree")
def test_the_produced_plan_satisfies_the_contract_for_every_producer() -> None:
    """ordinary·participation·doctrine target이 한 파일에 모인 뒤에도 계약이 성립한다."""
    import json

    for line in _PRODUCED_PLAN.read_text(encoding="utf-8").splitlines():
        if line.strip():
            validate_plan_carriers(REGISTRY, json.loads(line))
