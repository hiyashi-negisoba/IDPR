from __future__ import annotations

from pathlib import Path

from idpr.v2.issue_binding import BindingFragment, FactualEpisode, IssueBinding
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import (
    plan_binding_scoped_evaluation_instances,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _fragment(binding: str, kind: str, number: int, quote: str) -> BindingFragment:
    return BindingFragment(
        f"{binding}:{kind}:{number:03d}", kind, quote, 0, len(quote)  # type: ignore[arg-type]
    )


def test_one_binding_is_one_top_level_context_without_closure_cartesian() -> None:
    bindings = (
        IssueBinding(
            "binding:001",
            "factual_episode:001",
            0,
            "offense.theft",
            "甲",
            (_fragment("binding:001", "actor_action", 1, "甲이 물건을 가져갔다."),),
            (_fragment("binding:001", "context", 1, "A의 물건이 없어졌다."),),
            ("A",),
        ),
        IssueBinding(
            "binding:002",
            "factual_episode:002",
            1,
            "offense.injury",
            "乙",
            (_fragment("binding:002", "actor_action", 1, "乙이 B를 때렸다."),),
            (),
            ("B",),
        ),
    )
    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY, case_id="case", bindings=bindings
    )
    assert len(plan.top_level_instances) == len(bindings) == 2
    assert [value.occurrence_id for value in plan.top_level_instances] == [
        "binding:001",
        "binding:002",
    ]
    assert "\n" in plan.occurrences[0].source_text
    assert not plan.participation_local_targets
    assert len(plan.top_level_instances) != len(plan.occurrences) * len(
        plan.candidate_offense_refs
    )


def test_dependency_context_binding_cannot_become_top_level_liability() -> None:
    context = IssueBinding(
        "binding:001",
        "factual_episode:001",
        0,
        "offense.homicide",
        "乙",
        (
            BindingFragment(
                "binding:001:actor_action:001",
                "actor_action",
                "乙이 B를 살해했다.",
                0,
                11,
            ),
        ),
        (),
        ("B",),
    )
    target = IssueBinding(
        "binding:002",
        "factual_episode:002",
        1,
        "offense.theft",
        "乙",
        (
            BindingFragment(
                "binding:002:actor_action:001",
                "actor_action",
                "乙이 물건을 숨겼다.",
                20,
                31,
            ),
        ),
        (),
        (),
    )
    plan = plan_binding_scoped_evaluation_instances(
        REGISTRY,
        case_id="case",
        bindings=(context, target),
        liability_source_spans=((20, 40),),
    )
    assert [value.occurrence_id for value in plan.top_level_instances] == ["binding:002"]
    assert plan.context_only_binding_ids == ("binding:001",)


def test_registry_authored_derived_candidate_requires_two_same_episode_bindings() -> None:
    theft_binding = IssueBinding(
        "binding:001",
        "factual_episode:001",
        0,
        "offense.theft",
        "乙",
        (_fragment("binding:001", "actor_action", 1, "乙이 가방을 가져갔다."),),
        (),
        ("A",),
    )
    injury_binding = IssueBinding(
        "binding:002",
        "factual_episode:001",
        1,
        "offense.injury",
        "乙",
        (_fragment("binding:002", "actor_action", 1, "乙이 A를 밀쳤다."),),
        (),
        ("A",),
    )
    episode = FactualEpisode(
        "factual_episode:001",
        (_fragment("factual_episode:001", "episode_source", 1, "乙이 가방을 가져간 뒤 A를 밀쳤다."),),
        ("乙", "A"),
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
    assert candidate.supporting_actor_ids == ("乙",)
    assert candidate.as_dict()["semantic_effect"] == "candidate_construction_only"


def test_base_binding_alone_never_materializes_closure_child() -> None:
    binding = IssueBinding(
        "binding:001",
        "factual_episode:001",
        0,
        "offense.theft",
        "乙",
        (_fragment("binding:001", "actor_action", 1, "乙이 가방을 가져갔다."),),
        (),
        ("A",),
    )
    episode = FactualEpisode(
        "factual_episode:001",
        (_fragment("factual_episode:001", "episode_source", 1, "乙이 가방을 가져간 뒤 A를 밀쳤다."),),
        ("乙", "A"),
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
    bindings = tuple(
        IssueBinding(
            f"binding:{index:03d}",
            "factual_episode:001",
            0,
            "offense.theft",
            actor,
            (
                _fragment(
                    f"binding:{index:03d}",
                    "actor_action",
                    1,
                    f"{actor}이 절도 행위에 관여했다.",
                ),
            ),
            (),
            ("A",),
        )
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    episode = FactualEpisode(
        "factual_episode:001",
        (
            _fragment(
                "factual_episode:001",
                "episode_source",
                1,
                "甲과 乙이 절도 행위에 관여했다.",
            ),
        ),
        ("甲", "乙", "A"),
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


def test_distinct_actor_injury_bindings_open_only_factual_article263_pair() -> None:
    bindings = tuple(
        IssueBinding(
            f"binding:{index:03d}",
            "factual_episode:001",
            0,
            "offense.injury",
            actor,
            (_fragment(f"binding:{index:03d}", "actor_action", 1, quote),),
            (),
            ("B",),
        )
        for index, (actor, quote) in enumerate(
            (("甲", "甲이 B를 때렸다."), ("乙", "乙이 B를 때렸다.")), 1
        )
    )
    episode = FactualEpisode(
        "factual_episode:001",
        (
            _fragment(
                "factual_episode:001",
                "episode_source",
                1,
                "甲과 乙이 각각 B를 때렸고 원인은 밝혀지지 않았다.",
            ),
        ),
        ("甲", "乙", "B"),
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
        "binding:001",
        "binding:002",
    )
    assert plan.as_dict()["article263_pair_candidate_count"] == 1
