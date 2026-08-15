"""ROUTE는 stage가 아니라 재호출 가능한 operation이다.

제151조는 첫 사례일 뿐이고, dependency planner는 조문을 알지 못한다. 아는 것은 "저작이
linked_offender_dependency를 선언했고 사실이 결박되었다"뿐이다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.issue_binding import BindingFragment, FactualAction, IssueBinding
from idpr.v2.registry import load_definitions
from idpr.v2.routing import (
    LINKED_OFFENDER_ROUTING,
    QUESTION_ROUTING,
    RouteRequest,
    RouterContractError,
    route_request_payload,
    router_catalog,
)
from idpr.v2.runtime.identity import FactualParticipantKey
from idpr.v2.runtime.linked_offender import linked_offender_dependencies

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
CASE = "case"
CASE_TEXT = "丙은 乙에게 도피자금을 건넸다. 乙은 그 돈으로 잠적했다."


def _action(action_id: str, quote: str, index: int) -> FactualAction:
    start = CASE_TEXT.find(quote)
    return FactualAction(
        action_id,
        "factual_episode:001",
        "丙",
        ("丙", "乙"),
        (BindingFragment(f"{action_id}:f", "factual_action", quote, start, start + len(quote)),),
        index,
    )


ACTIONS = (
    _action("factual_action:001:001", "丙은 乙에게 도피자금을 건넸다.", 0),
    _action("factual_action:001:002", "乙은 그 돈으로 잠적했다.", 1),
)


def _binding(offense_ref: str, linked: str | None) -> IssueBinding:
    return IssueBinding(
        "binding:001",
        "factual_episode:001",
        0,
        offense_ref,
        "丙",
        "factual_action:001:001",
        ("factual_action:001:002",),
        ("乙",),
        None,
        None,
        linked,
    )


def _dependencies(offense_ref: str, linked: str | None):
    return linked_offender_dependencies(
        REGISTRY,
        case_id=CASE,
        realizations=(("realization:001", "丙", offense_ref, ("binding:001",)),),
        bindings=(_binding(offense_ref, linked),),
        factual_actions=ACTIONS,
    )


def test_an_authored_dependency_with_a_bound_person_produces_a_route_invocation() -> None:
    dependency = _dependencies("offense.harboring_or_escape", "乙")[0]

    assert dependency.participant == FactualParticipantKey(CASE, "乙")
    assert dependency.resolved_element == "legal_element.offender_status_of_object"
    request = dependency.route_request()
    assert request.routed_actor_ids == ("乙",)
    assert request.routing_basis == LINKED_OFFENDER_ROUTING


def test_the_dependency_scope_is_what_the_binding_carries_not_the_episode() -> None:
    """episode로 넓히면 그 서사의 모든 사건이 선행범죄 후보로 열린다.

    좁게 결박한 사실을 다시 넓은 범위로 되돌리는 셈이라, `factual_targets` 재해석을 거부한
    것과 같은 종류의 후퇴가 된다.
    """
    scope = _dependencies("offense.harboring_or_escape", "乙")[0].factual_scope_text

    assert "丙은 乙에게 도피자금을 건넸다." in scope
    assert "乙은 그 돈으로 잠적했다." in scope


def test_no_authored_declaration_means_no_dependency() -> None:
    assert _dependencies("offense.theft", "乙") == ()


def test_an_unnamed_offender_is_not_chosen_by_the_host() -> None:
    """원문이 대상자를 지목하지 않았으면 host가 사람을 고르지 않는다."""
    assert _dependencies("offense.harboring_or_escape", None) == ()


def test_dependency_routing_refuses_to_carry_the_question() -> None:
    """질문을 함께 주면 범위가 질문받은 행위자로 다시 끌려간다."""
    catalog = router_catalog(REGISTRY)
    request = RouteRequest(
        routed_actor_ids=("乙",),
        factual_scope_text="乙은 그 돈으로 잠적했다.",
        routing_basis=LINKED_OFFENDER_ROUTING,
        question_prompt="丙의 죄책을 논하라.",
    )

    with pytest.raises(RouterContractError, match="question_prompt"):
        route_request_payload(request, case_text=CASE_TEXT, catalog=catalog)


def test_the_first_invocation_is_the_same_operation() -> None:
    """최초 routing도 같은 operation이다 -- 다른 것은 누구를, 어느 범위로 라우팅하는가뿐이다."""
    catalog = router_catalog(REGISTRY)
    payload = route_request_payload(
        RouteRequest(
            routed_actor_ids=("丙",),
            factual_scope_text=CASE_TEXT,
            routing_basis=QUESTION_ROUTING,
            question_prompt="丙의 죄책을 논하라.",
        ),
        case_text=CASE_TEXT,
        catalog=catalog,
    )

    assert payload["routing_basis"] == QUESTION_ROUTING
    assert payload["question_prompt"] == "丙의 죄책을 논하라."
    assert payload["offense_catalog"]


def test_the_static_threshold_gates_before_any_neural_evaluation() -> None:
    """threshold는 사건 사실이 아니라 저작된 metadata다. Call 2 앞에서 물을 수 있다.

    어차피 제151조 대상이 될 수 없는 죄를 먼저 neural하게 평가할 이유가 없다.
    """
    from idpr.v2.runtime.linked_offender import gate_predecessor_candidates

    dependency = _dependencies("offense.harboring_or_escape", "乙")[0]
    gate = gate_predecessor_candidates(
        REGISTRY, dependency, ("offense.theft", "offense.nope")
    )

    assert gate.qualifying == ("offense.theft",)
    assert gate.unauthored == ("offense.nope",)


def test_an_unauthored_threshold_is_not_folded_into_non_qualifying() -> None:
    """미저작을 "자격 없음"과 합치면 저작 누락이 결정론적 부정으로 둔갑한다."""
    from idpr.v2.runtime.linked_offender import gate_predecessor_candidates

    dependency = _dependencies("offense.harboring_or_escape", "乙")[0]
    gate = gate_predecessor_candidates(REGISTRY, dependency, ("offense.nope",))

    assert gate.non_qualifying == ()
    assert gate.unauthored == ("offense.nope",)
