from __future__ import annotations

import dataclasses
from pathlib import Path

from idpr.v2.issue_binding import (
    BindingFragment,
    FactualAction,
    FactualEpisode,
    IssueBinding,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import (
    OccurrenceAwareEvaluationInstancePlan,
    plan_binding_scoped_evaluation_instances,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _fragment(owner: str, kind: str, number: int, quote: str, start: int = 0) -> BindingFragment:
    return BindingFragment(
        f"{owner}:{kind}:{number:03d}",
        kind,  # type: ignore[arg-type]
        quote,
        start,
        start + len(quote),
    )


def _episode(
    episode_id: str,
    *,
    participants: tuple[str, ...],
    actions: tuple[tuple[str, tuple[str, ...], str, int], ...],
) -> FactualEpisode:
    episode_number = episode_id.rsplit(":", maxsplit=1)[1]
    factual_actions = tuple(
        FactualAction(
            f"factual_action:{episode_number}:{index:03d}",
            episode_id,
            source_actor_id,
            action_participants,
            (
                _fragment(
                    f"factual_action:{episode_number}:{index:03d}",
                    "factual_action",
                    1,
                    quote,
                    start,
                ),
            ),
            index - 1,
        )
        for index, (source_actor_id, action_participants, quote, start) in enumerate(
            actions, 1
        )
    )
    return FactualEpisode(
        episode_id,
        (
            _fragment(
                episode_id,
                "episode_source",
                1,
                "\n".join(action.evidence_text for action in factual_actions),
            ),
        ),
        participants,
        factual_actions,
    )


def _binding(
    number: int,
    *,
    episode: FactualEpisode,
    seed_index: int,
    offense_ref: str,
    actor_id: str,
    focal_action_index: int,
    supporting_action_indexes: tuple[int, ...] = (),
    factual_targets: tuple[str, ...] = (),
) -> IssueBinding:
    return IssueBinding(
        f"binding:{number:03d}",
        episode.factual_episode_id,
        seed_index,
        offense_ref,
        actor_id,
        episode.factual_actions[focal_action_index].factual_action_id,
        tuple(
            episode.factual_actions[index].factual_action_id
            for index in supporting_action_indexes
        ),
        factual_targets,
    )


def _occurrence_text(
    plan: OccurrenceAwareEvaluationInstancePlan, occurrence_id: str
) -> str:
    return next(
        value.source_text
        for value in plan.occurrences
        if value.occurrence_id == occurrence_id
    )


def test_one_binding_materializes_one_realization_without_closure_cartesian() -> None:
    theft_episode = _episode(
        "factual_episode:001",
        participants=("甲", "A"),
        actions=(("甲", ("甲", "A"), "甲이 물건을 가져갔다.", 0),),
    )
    injury_episode = _episode(
        "factual_episode:002",
        participants=("乙", "B"),
        actions=(("乙", ("乙", "B"), "乙이 B를 때렸다.", 30),),
    )
    bindings = (
        _binding(
            1,
            episode=theft_episode,
            seed_index=0,
            offense_ref="offense.theft",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("A",),
        ),
        _binding(
            2,
            episode=injury_episode,
            seed_index=1,
            offense_ref="offense.injury",
            actor_id="乙",
            focal_action_index=0,
            factual_targets=("B",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(theft_episode, injury_episode),
    )

    assert len(plan.top_level_instances) == 2
    assert [value.occurrence_id for value in plan.top_level_instances] == [
        "realization:001",
        "realization:002",
    ]
    assert [value.source_binding_ids for value in plan.legal_realizations] == [
        ("binding:001",),
        ("binding:002",),
    ]
    assert all(
        not value.occurrence_id.startswith("binding:")
        for value in plan.top_level_instances
    )
    assert _occurrence_text(plan, "realization:001") == "甲이 물건을 가져갔다."
    assert not plan.participation_local_targets
    assert len(plan.top_level_instances) != len(plan.occurrences) * len(
        plan.candidate_offense_refs
    )


def test_focal_anchor_excludes_later_supported_action_from_receipt_time_element() -> None:
    """`temporal_anchor` fixes the moment judged; `evidence_scope` fixes the width.

    증뢰 목적 인식 is authored `offense_realization`, so it keeps the realization carrier and
    only loses what happens after the focal action.  Collapsing it to the focal action
    instead satisfied the anchor but starved the scope, which is why the receipt-time
    element of 제133조 제2항 sat at 100% UNKNOWN.
    """
    episode = _episode(
        "factual_episode:001",
        participants=("乙", "丙"),
        actions=(
            ("乙", ("乙", "丙"), "乙은 丙에게 전달할 3천만 원을 교부하였다.", 0),
            ("丙", ("丙",), "丙은 그중 2천만 원을 소비하였다.", 30),
        ),
    )
    binding = _binding(
        1,
        episode=episode,
        seed_index=0,
        offense_ref="offense.bribe_delivery_receipt",
        actor_id="丙",
        focal_action_index=0,
        supporting_action_indexes=(1,),
        factual_targets=("乙",),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(binding,),
        factual_episodes=(episode,),
    )

    realization = plan.legal_realizations[0]
    assert realization.realization_id == "realization:001"
    assert realization.focal_action_id == "factual_action:001:001"
    assert realization.supporting_action_ids == ("factual_action:001:002",)
    assert _occurrence_text(plan, realization.realization_id) == (
        "乙은 丙에게 전달할 3천만 원을 교부하였다.\n"
        "丙은 그중 2천만 원을 소비하였다."
    )

    carrier_by_predicate = {
        value.target.predicate_ref: value for value in plan.assessment_carriers
    }
    knowledge = carrier_by_predicate["legal_element.knowledge_of_bribery_destination"]
    receipt = carrier_by_predicate[
        "ground_fact.intermediary_delivery_receipt_conduct"
    ]
    assert knowledge.carrier_kind == "realization_at_focal"
    assert receipt.carrier_kind == "focal_action"
    assert _occurrence_text(plan, knowledge.carrier_id) == (
        "乙은 丙에게 전달할 3천만 원을 교부하였다."
    )
    assert _occurrence_text(plan, receipt.carrier_id) == (
        "乙은 丙에게 전달할 3천만 원을 교부하였다."
    )


def test_dependency_context_binding_cannot_become_top_level_liability() -> None:
    context_episode = _episode(
        "factual_episode:001",
        participants=("乙", "B"),
        actions=(("乙", ("乙", "B"), "乙이 B를 살해했다.", 0),),
    )
    target_episode = _episode(
        "factual_episode:002",
        participants=("乙",),
        actions=(("乙", ("乙",), "乙이 물건을 숨겼다.", 20),),
    )
    context = _binding(
        1,
        episode=context_episode,
        seed_index=0,
        offense_ref="offense.homicide",
        actor_id="乙",
        focal_action_index=0,
        factual_targets=("B",),
    )
    target = _binding(
        2,
        episode=target_episode,
        seed_index=1,
        offense_ref="offense.theft",
        actor_id="乙",
        focal_action_index=0,
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(context, target),
        factual_episodes=(context_episode, target_episode),
        liability_source_spans=((20, 40),),
    )

    assert [value.occurrence_id for value in plan.top_level_instances] == [
        "realization:001"
    ]
    assert plan.context_only_binding_ids == ("binding:001",)
    assert plan.legal_realizations[0].source_binding_ids == ("binding:002",)


def test_registry_authored_derived_candidate_requires_two_same_episode_realizations() -> None:
    episode = _episode(
        "factual_episode:001",
        participants=("乙", "A"),
        actions=(
            ("乙", ("乙", "A"), "乙이 가방을 가져갔다.", 0),
            ("乙", ("乙", "A"), "乙이 A를 밀쳤다.", 20),
        ),
    )
    theft_binding = _binding(
        1,
        episode=episode,
        seed_index=0,
        offense_ref="offense.theft",
        actor_id="乙",
        focal_action_index=0,
        factual_targets=("A",),
    )
    injury_binding = _binding(
        2,
        episode=episode,
        seed_index=1,
        offense_ref="offense.injury",
        actor_id="乙",
        focal_action_index=1,
        factual_targets=("A",),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(theft_binding, injury_binding),
        factual_episodes=(episode,),
        allowed_candidate_offense_refs=("offense.theft", "derived_offense.quasi_robbery"),
    )

    assert len(plan.top_level_instances) == 3
    candidate = plan.derived_binding_candidates[0]
    assert candidate.offense_ref == "derived_offense.quasi_robbery"
    assert candidate.factual_episode_id == "factual_episode:001"
    assert candidate.required_binding_refs == ("offense.theft", "offense.injury")
    assert candidate.source_binding_ids == ("binding:001", "binding:002")
    assert candidate.source_realization_ids == ("realization:001", "realization:002")
    assert candidate.realization_id == "realization:derived:001"
    assert candidate.supporting_actor_ids == ("乙",)
    assert candidate.as_dict()["semantic_effect"] == "candidate_construction_only"


def test_base_binding_alone_never_materializes_closure_child() -> None:
    episode = _episode(
        "factual_episode:001",
        participants=("乙", "A"),
        actions=(("乙", ("乙", "A"), "乙이 가방을 가져갔다.", 0),),
    )
    binding = _binding(
        1,
        episode=episode,
        seed_index=0,
        offense_ref="offense.theft",
        actor_id="乙",
        focal_action_index=0,
        factual_targets=("A",),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(binding,),
        factual_episodes=(episode,),
        allowed_candidate_offense_refs=("offense.theft", "derived_offense.quasi_robbery"),
    )

    assert len(plan.top_level_instances) == 1
    assert not plan.derived_binding_candidates


def test_distinct_actor_same_episode_bindings_can_open_authored_candidate() -> None:
    episode = _episode(
        "factual_episode:001",
        participants=("甲", "乙", "A"),
        actions=(
            ("甲", ("甲", "A"), "甲이 절도 행위에 관여했다.", 0),
            ("乙", ("乙", "A"), "乙이 절도 행위에 관여했다.", 20),
        ),
    )
    bindings = (
        _binding(
            1,
            episode=episode,
            seed_index=0,
            offense_ref="offense.theft",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("A",),
        ),
        _binding(
            2,
            episode=episode,
            seed_index=0,
            offense_ref="offense.theft",
            actor_id="乙",
            focal_action_index=1,
            factual_targets=("A",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(episode,),
        allowed_candidate_offense_refs=(
            "offense.theft",
            "derived_offense.special_theft",
        ),
    )

    assert len(plan.derived_binding_candidates) == 2
    assert {
        candidate.supporting_actor_ids for candidate in plan.derived_binding_candidates
    } == {("甲", "乙"), ("乙", "甲")}
    assert {
        candidate.source_realization_ids
        for candidate in plan.derived_binding_candidates
    } == {
        ("realization:001", "realization:002"),
        ("realization:002", "realization:001"),
    }


def test_same_action_across_offenses_reuses_factual_ground_fact_carrier() -> None:
    episode = _episode(
        "factual_episode:001",
        participants=("甲", "A"),
        actions=(("甲", ("甲", "A"), "甲이 A의 가방을 가져갔다.", 0),),
    )
    bindings = (
        _binding(
            1,
            episode=episode,
            seed_index=0,
            offense_ref="offense.theft",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("A",),
        ),
        _binding(
            2,
            episode=episode,
            seed_index=1,
            offense_ref="offense.robbery",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("A",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(episode,),
    )

    taking = [
        value
        for value in plan.assessment_carriers
        if value.target.predicate_ref == "ground_fact.taking_conduct"
        and value.target.instance_key.offense_ref in {"offense.theft", "offense.robbery"}
    ]
    assert len(taking) == 2
    assert {value.carrier_id for value in taking} == {
        "carrier:focal_action:甲:factual_action:001:001"
    }


def test_zero_bindings_emit_unbound_seed_diagnostics() -> None:
    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(),
        unbound_seed_refs=("offense.homicide",),
    )
    assert not plan.top_level_instances
    assert plan.as_dict()["unbound_seeds"] == [
        {"offense_ref": "offense.homicide", "status": "UNBOUND_SEED"}
    ]


def test_distinct_actor_injury_realizations_open_only_factual_article263_pair() -> None:
    episode = _episode(
        "factual_episode:001",
        participants=("甲", "乙", "B"),
        actions=(
            ("甲", ("甲", "B"), "甲이 B를 때렸다.", 0),
            ("乙", ("乙", "B"), "乙이 B를 때렸다.", 20),
        ),
    )
    bindings = (
        _binding(
            1,
            episode=episode,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("B",),
        ),
        _binding(
            2,
            episode=episode,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="乙",
            focal_action_index=1,
            factual_targets=("B",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(episode,),
    )

    assert len(plan.article263_pair_candidates) == 1
    pair = plan.article263_pair_candidates[0]
    assert (pair.left.occurrence_id, pair.right.occurrence_id) == (
        "realization:001",
        "realization:002",
    )
    assert plan.as_dict()["article263_pair_candidate_count"] == 1


def test_article263_pairs_across_episodes_because_the_article_allows_이시_행위() -> None:
    """제263조는 시간적 동시성을 요구하지 않는다.

    조문은 "독립행위가 경합하여 상해의 결과를 발생하게 한 경우에 있어서 원인된 행위가
    판명되지 아니한 때"라고만 하고, 대법원 80도3321은 약 3시간 간격의 이시 독립 상해행위에도
    이를 적용했다. episode 경계는 Call 1.5가 서사를 나눈 결과일 뿐이므로 join 조건이 될 수
    없다 -- `r10_p1_q2`에서 2시간 간격의 두 폭행이 서로 다른 episode로 나뉘며 pair가 0이 된
    것이 이 테스트의 배경이다.
    """
    first = _episode(
        "factual_episode:001",
        participants=("甲", "B"),
        actions=(("甲", ("甲", "B"), "甲이 B를 때렸다.", 0),),
    )
    second = _episode(
        "factual_episode:002",
        participants=("乙", "B"),
        actions=(("乙", ("乙", "B"), "두 시간 뒤 乙이 B를 때렸다.", 40),),
    )
    bindings = (
        _binding(
            1,
            episode=first,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("B",),
        ),
        _binding(
            2,
            episode=second,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="乙",
            focal_action_index=0,
            factual_targets=("B",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(first, second),
    )

    assert len(plan.article263_pair_candidates) == 1
    pair = plan.article263_pair_candidates[0]
    # 증거는 두 episode를 아울러야 한다. 한쪽만 주면 다른 쪽 행위가 증거에서 빠진다.
    assert "甲이 B를 때렸다." in pair.relation_source_text
    assert "두 시간 뒤 乙이 B를 때렸다." in pair.relation_source_text


def test_same_actor_injury_realizations_never_pair_even_across_episodes() -> None:
    """제거된 것은 episode 조건뿐이다. 동일인의 두 상해는 여전히 동시범이 아니다."""
    first = _episode(
        "factual_episode:001",
        participants=("甲", "B"),
        actions=(("甲", ("甲", "B"), "甲이 B를 때렸다.", 0),),
    )
    second = _episode(
        "factual_episode:002",
        participants=("甲", "B"),
        actions=(("甲", ("甲", "B"), "두 시간 뒤 甲이 B를 다시 때렸다.", 40),),
    )
    bindings = (
        _binding(
            1,
            episode=first,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("B",),
        ),
        _binding(
            2,
            episode=second,
            seed_index=0,
            offense_ref="offense.injury",
            actor_id="甲",
            focal_action_index=0,
            factual_targets=("B",),
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(first, second),
    )

    assert plan.article263_pair_candidates == ()


def test_the_bound_result_bearer_also_opens_an_article263_pair() -> None:
    """제263조가 묻는 것은 결과가 같은 사람에게 발생한 두 독립행위다.

    `factual_targets`만 보면 모델이 그 배열을 비운 사건에서 후보가 열리지 않는다.
    `r10_p1_q2`의 두 상해 binding이 정확히 그랬고, 대신 양쪽 다 결과 귀속 대상으로 B를
    적고 있었다. 후보를 여는 것까지가 host의 몫이고 `same_object_of_result`가 참인지는
    여전히 Call 2가 답한다.
    """
    first = _episode(
        "factual_episode:001",
        participants=("甲", "B"),
        actions=(("甲", ("甲", "B"), "甲이 B를 때렸다.", 0),),
    )
    second = _episode(
        "factual_episode:002",
        participants=("乙", "B"),
        actions=(("乙", ("乙", "B"), "두 시간 뒤 乙이 B를 때렸다.", 40),),
    )
    bindings = (
        dataclasses.replace(
            _binding(
                1,
                episode=first,
                seed_index=0,
                offense_ref="offense.injury",
                actor_id="甲",
                focal_action_index=0,
                factual_targets=(),
            ),
            actual_result_bearer="B",
        ),
        dataclasses.replace(
            _binding(
                2,
                episode=second,
                seed_index=0,
                offense_ref="offense.injury",
                actor_id="乙",
                focal_action_index=0,
                factual_targets=(),
            ),
            actual_result_bearer="B",
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(first, second),
    )

    assert len(plan.article263_pair_candidates) == 1


def test_a_different_result_bearer_does_not_open_a_pair() -> None:
    first = _episode(
        "factual_episode:001",
        participants=("甲", "B"),
        actions=(("甲", ("甲", "B"), "甲이 B를 때렸다.", 0),),
    )
    second = _episode(
        "factual_episode:002",
        participants=("乙", "C"),
        actions=(("乙", ("乙", "C"), "乙이 C를 때렸다.", 40),),
    )
    bindings = (
        dataclasses.replace(
            _binding(
                1,
                episode=first,
                seed_index=0,
                offense_ref="offense.injury",
                actor_id="甲",
                focal_action_index=0,
                factual_targets=(),
            ),
            actual_result_bearer="B",
        ),
        dataclasses.replace(
            _binding(
                2,
                episode=second,
                seed_index=0,
                offense_ref="offense.injury",
                actor_id="乙",
                focal_action_index=0,
                factual_targets=(),
            ),
            actual_result_bearer="C",
        ),
    )

    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=bindings,
        factual_episodes=(first, second),
    )

    assert plan.article263_pair_candidates == ()
