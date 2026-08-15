"""Participation 축의 종료 증명.

세 가지 구조 결함만 본다. 어느 진리값 배정으로도 참이 될 수 없는 상태, 동시에 참일 수
있는데 양보 관계가 없는 상태, predicate가 요구하는 종류의 사실을 담을 수 없는 carrier.
모델이 틀리는 것은 여기서 다루지 않는다.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import pytest

from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    factual_interaction_request_payload,
    validate_factual_interaction_output,
)
from idpr.v2.issue_binding import BindingFragment, FactualAction, FactualEpisode
from idpr.v2.participation import (
    derivative_mode_required_predicate_refs,
    derivative_mode_subsumptions,
    participation_policy_for,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationLocalAssessment,
    ParticipationLocalTarget,
    compile_participation_bindings,
    participation_local_targets,
)
from idpr.v2.runtime.policy_probe_targets import (
    MODE_BY_RELATION_KIND,
    participation_mode_requirement_targets,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _instance(actor: str, number: int) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", actor, "offense.theft", f"gocc:{number:03d}")


# --------------------------------------------------------------------------
# 1. 발화 불가능성
# --------------------------------------------------------------------------


def test_every_derivative_mode_requirement_is_opened_as_a_target() -> None:
    """교사·방조가 요구하는 가담자 자신의 요소는 반드시 질문된다.

    저작은 derivative mode를 `requires`로 정의하는데, 그 predicate를 planner가 열지 않으면
    Call 2가 묻지 않는다. Kleene에서 묻지 않은 사실은 UNKNOWN이므로, 교사범·방조범은 어떤
    사건에서도 성립할 수 없게 된다. 실제로 26문항 plan에서 두 요소 모두 target이 0이었다.
    """
    policy = participation_policy_for(REGISTRY)
    assert policy is not None
    required = derivative_mode_required_predicate_refs(policy)
    assert required, "derivative mode가 요구하는 요소가 하나도 저작되지 않았다"

    instances = (_instance("甲", 1), _instance("乙", 2))
    targets = participation_local_targets(REGISTRY, instances)
    derivative = tuple(
        value for value in targets if value.kind in MODE_BY_RELATION_KIND
        and MODE_BY_RELATION_KIND[value.kind] in required
    )
    assert derivative, "derivative participation 후보가 생성되지 않았다"

    opened = set(participation_mode_requirement_targets(REGISTRY, derivative))
    for target in derivative:
        accessory = target.members[0]
        for ref in required[MODE_BY_RELATION_KIND[target.kind]]:
            assert (accessory, ref) in opened, (target.kind, accessory, ref)


def test_mode_requirements_land_on_the_accessory_not_the_principal() -> None:
    """교사의 고의는 교사자의 것이다. 정범에게 물으면 답이 와도 쓸 수 없다."""
    accessory, principal = _instance("甲", 1), _instance("乙", 2)
    targets = participation_local_targets(REGISTRY, (accessory, principal))
    derivative = tuple(
        value
        for value in targets
        if value.kind in {"instigation", "aiding"} and value.members[0] == accessory
    )
    assert derivative
    for instance, _ref in participation_mode_requirement_targets(REGISTRY, derivative):
        assert instance == accessory


# --------------------------------------------------------------------------
# 2. 배타·우선관계
# --------------------------------------------------------------------------


def test_every_co_satisfiable_mode_pair_has_an_authored_precedence() -> None:
    """한 가담자에게 동시에 참일 수 있는 mode 쌍에는 양보 관계가 저작되어 있다.

    양보 관계가 없으면 compile이 예외로 사건 전체를 중단시킨다. unresolved보다 나쁜 결과다.
    """
    policy = participation_policy_for(REGISTRY)
    assert policy is not None
    subsumptions = derivative_mode_subsumptions(policy)
    # `principal`은 직접정범이라 가담 후보로 열리지 않는다. 나머지는 한 사람에게 동시에
    # 참으로 평가될 수 있고, 그래서 서로 우선관계를 가져야 한다.
    participation_modes = sorted(
        mode
        for mode, payload in (policy.payload.get("modes") or {}).items()
        if payload.get("basis") != "direct"
    )
    for left, right in combinations(participation_modes, 2):
        assert right in subsumptions.get(left, frozenset()) or left in subsumptions.get(
            right, frozenset()
        ), f"{left}와 {right}의 우선관계가 저작되지 않았다"


def test_co_principal_and_derivative_on_one_participant_resolve_without_aborting() -> None:
    """정범 경로와 종범 경로가 함께 참이어도 사건이 중단되지 않는다."""
    accessory, principal = _instance("甲", 1), _instance("乙", 2)
    targets = participation_local_targets(REGISTRY, (accessory, principal))
    group = next(
        value
        for value in targets
        if value.kind == "co_principal_group"
        and set(value.members) == {accessory, principal}
    )
    aiding = next(
        value
        for value in targets
        if value.kind == "aiding"
        and value.members[0] == accessory
        and value.principal == principal
    )
    assessments = tuple(
        ParticipationLocalAssessment(
            value, "TRUE" if value in {group, aiding} else "FALSE"
        )
        for value in targets
    )
    bindings = compile_participation_bindings(assessments, registry=REGISTRY)
    assert bindings.derivative_links == (), "정범이 확정된 가담자에게 종범 링크가 남았다"
    assert any(
        resolution["dominant_mode"] == "co_principal"
        and resolution["subsumed_mode"] == "aider"
        for resolution in bindings.mode_resolutions
    ), "양보가 기록되지 않았다"
    assert bindings.co_principal_sources, "공동정범 관계가 사라졌다"


def test_two_realizations_of_one_offense_by_one_pair_stay_two_relations() -> None:
    """상호작용 중복과 법적 중복은 다르다.

    같은 관계가 두 상호작용에서 확인되면 후보 instance가 상호작용마다 따로 만들어지고, 그
    둘은 하나로 접어야 한다. 그러나 甲·乙이 함께 절도를 두 번 저지르면 그것은 두 개의 관계다.
    행위자 구성만으로 접으면 뒤의 절도가 앞의 절도에 흡수되어 사라진다.
    """
    first = (_instance("甲", 1), _instance("乙", 1))
    second = (_instance("甲", 2), _instance("乙", 2))
    bindings = compile_participation_bindings(
        tuple(
            ParticipationLocalAssessment(
                ParticipationLocalTarget("co_principal_group", members), "TRUE"
            )
            for members in (first, second)
        ),
        registry=REGISTRY,
    )
    sources = set(bindings.co_principal_sources)
    assert {(first[0], first[1]), (first[1], first[0])} <= sources
    assert {(second[0], second[1]), (second[1], second[0])} <= sources


def test_one_relation_seen_in_two_interactions_is_still_one_relation() -> None:
    """반대 방향. 후보의 occurrence는 증거 식별자이므로 관계의 신원이 되지 못한다."""
    seen_once = (
        OffenseInstanceKey("case", "甲", "offense.theft", "participation_realization:001:甲:a"),
        OffenseInstanceKey("case", "乙", "offense.theft", "participation_realization:001:乙:a"),
    )
    seen_twice = (
        OffenseInstanceKey("case", "甲", "offense.theft", "participation_realization:002:甲:b"),
        OffenseInstanceKey("case", "乙", "offense.theft", "participation_realization:002:乙:b"),
    )
    bindings = compile_participation_bindings(
        tuple(
            ParticipationLocalAssessment(
                ParticipationLocalTarget("co_principal_group", members), "TRUE"
            )
            for members in (seen_once, seen_twice)
        ),
        registry=REGISTRY,
    )
    actors = {
        tuple(sorted((left.actor_id, right.actor_id)))
        for left, right in bindings.co_principal_sources
    }
    assert actors == {("乙", "甲")}
    assert len(bindings.co_principal_sources) == 2


# --------------------------------------------------------------------------
# 3. relation carrier 정합
# --------------------------------------------------------------------------

_CASE_TEXT = "甲은 후배 乙에게 A의 집에 불을 질러 달라고 사주하였다. 이를 승낙한 乙은 불을 질렀다."


def _fragment(kind: str, fragment_id: str, quote: str) -> BindingFragment:
    start = _CASE_TEXT.index(quote)
    return BindingFragment(fragment_id, kind, quote, start, start + len(quote))


def _instigation_episode() -> FactualEpisode:
    """행위 원자화가 사주자와 승낙자를 서로 다른 행위로 가르는 최소 사례."""
    episode_id = "factual_episode:001"
    instigation = "甲은 후배 乙에게 A의 집에 불을 질러 달라고 사주하였다."
    acceptance = "이를 승낙한 乙은 불을 질렀다."
    return FactualEpisode(
        episode_id,
        (_fragment("episode_source", f"{episode_id}:episode_source:001", _CASE_TEXT),),
        ("甲", "乙", "A"),
        (
            FactualAction(
                "factual_action:001:001",
                episode_id,
                "甲",
                # 사주받은 乙이 이 행위의 참여자로 기록되지 않는다. Call 1.5가 행위를
                # "누가 했고 누구에게 결과가 미쳤나"로 적기 때문이다.
                ("甲", "A"),
                (_fragment("factual_action", "factual_action:001:001:f:001", instigation),),
                0,
            ),
            FactualAction(
                "factual_action:001:002",
                episode_id,
                "乙",
                ("乙",),
                (_fragment("factual_action", "factual_action:001:002:f:001", acceptance),),
                1,
            ),
        ),
    )


def test_relation_endpoints_range_over_the_episode_not_the_action() -> None:
    """관계의 상대방이 그 행위의 참여자가 아니어도 결박할 수 있다.

    사주·승낙은 상대방이 행위 참여자로 기록되지 않는 전형이다. endpoint universe를 행위로
    좁히면 교사 관계 자체가 표현 불가능해진다 -- 26문항에서 15개 사건, 32개 행위가 자기
    인용문 안에 이름이 나오는 참여자를 참여자 목록에서 빠뜨리고 있었다.
    """
    episode = _instigation_episode()
    action = episode.factual_actions[0]
    payload = factual_interaction_request_payload(
        case_id="case",
        question_prompt="甲과 乙의 죄책은?",
        responsibility_actor_ids=("甲", "乙"),
        episode=episode,
        action=action,
    )
    assert "乙" not in payload["action_participant_ids"]
    assert "乙" in payload["episode_participant_ids"]

    parsed = validate_factual_interaction_output(
        {
            "interactions": [
                {
                    "interaction_type": "request_or_instruction",
                    "source_actor_id": "甲",
                    "target_actor_ids": ["乙"],
                    "evidence_quotes": ["후배 乙에게 A의 집에 불을 질러 달라고 사주하였다"],
                }
            ]
        },
        case_text=_CASE_TEXT,
        episode=episode,
        action=action,
    )
    assert parsed[0].target_actor_ids == ("乙",)


def test_action_scoped_relation_must_involve_that_action_actor() -> None:
    """endpoint를 넓힌 대가로, 관계는 그 행위를 한 사람을 한쪽 끝으로 가져야 한다."""
    episode = _instigation_episode()
    with pytest.raises(FactualInteractionContractError):
        validate_factual_interaction_output(
            {
                "interactions": [
                    {
                        "interaction_type": "request_or_instruction",
                        "source_actor_id": "乙",
                        "target_actor_ids": ["A"],
                        "evidence_quotes": [
                            "후배 乙에게 A의 집에 불을 질러 달라고 사주하였다"
                        ],
                    }
                ]
            },
            case_text=_CASE_TEXT,
            episode=episode,
            action=episode.factual_actions[0],
        )


def test_episode_scope_carries_relations_no_single_action_contains() -> None:
    """공동행동처럼 두 행위의 병렬로만 서술되는 관계는 episode 스코프에서만 읽힌다."""
    episode = _instigation_episode()
    quote = "甲은 후배 乙에게 A의 집에 불을 질러 달라고 사주하였다. 이를 승낙한 乙은"
    payload = factual_interaction_request_payload(
        case_id="case",
        question_prompt="甲과 乙의 죄책은?",
        responsibility_actor_ids=("甲", "乙"),
        episode=episode,
    )
    assert "episode_source_quotes" in payload
    parsed = validate_factual_interaction_output(
        {
            "interactions": [
                {
                    "interaction_type": "agreement_or_coordinated_conduct",
                    "source_actor_id": "甲",
                    "target_actor_ids": ["乙"],
                    "evidence_quotes": [quote],
                }
            ]
        },
        case_text=_CASE_TEXT,
        episode=episode,
    )
    assert parsed[0].factual_action_id is None
    for action in episode.factual_actions:
        with pytest.raises(FactualInteractionContractError):
            validate_factual_interaction_output(
                {
                    "interactions": [
                        {
                            "interaction_type": "agreement_or_coordinated_conduct",
                            "source_actor_id": "甲",
                            "target_actor_ids": ["乙"],
                            "evidence_quotes": [quote],
                        }
                    ]
                },
                case_text=_CASE_TEXT,
                episode=episode,
                action=action,
            )
