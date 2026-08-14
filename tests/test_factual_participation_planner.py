from __future__ import annotations

from pathlib import Path

from idpr.v2.factual_interaction import (
    FactualInteraction,
    InteractionEvidence,
)
from idpr.v2.issue_binding import (
    BindingFragment,
    FactualEpisode,
    IssueBinding,
    IssueBindingResult,
    SeedBindingResult,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.factual_participation import (
    derived_co_principal_targets,
    materialize_factual_participation_candidates,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import ParticipationLocalTarget

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")

CASE_ID = "case-1"
TEXT = "甲은 乙에게 A를 밀라고 부탁했다. 乙은 A를 밀었다."
EPISODE = FactualEpisode(
    "factual_episode:001",
    (
        BindingFragment(
            "factual_episode:001:episode_source:001",
            "episode_source",
            TEXT,
            0,
            len(TEXT),
        ),
    ),
    ("甲", "乙", "A"),
)
ACTION = BindingFragment(
    "binding:001:actor_action:001",
    "actor_action",
    "乙은 A를 밀었다.",
    20,
    len(TEXT),
)
BINDING = IssueBinding(
    "binding:001",
    EPISODE.factual_episode_id,
    0,
    "offense.injury",
    "乙",
    (ACTION,),
    (),
    ("A",),
)
BINDING_RESULT = IssueBindingResult(
    (EPISODE,),
    (SeedBindingResult(0, "offense.injury", (BINDING,)),),
)
PLAN = {
    "occurrences": [
        {
            "occurrence_id": "binding:001",
            "actor_id": "乙",
            "source_text": "乙은 A를 밀었다.",
            "source_span": {"start": 20, "end": len(TEXT)},
        }
    ],
    "top_level_instances": [
        {
            "case_id": CASE_ID,
            "actor_id": "乙",
            "offense_ref": "offense.injury",
            "occurrence_id": "binding:001",
        }
    ],
    "derived_binding_candidates": [],
    "participation_local_targets": [],
}


def interaction(kind: str = "request_or_instruction") -> FactualInteraction:
    return FactualInteraction(
        "finteraction:001:001",
        EPISODE.factual_episode_id,
        kind,
        "甲",
        ("乙",),
        (
            InteractionEvidence(
                "finteraction:001:001:evidence:001",
                "甲은 乙에게 A를 밀라고 부탁했다.",
                0,
                19,
            ),
        ),
    )


def test_directed_interaction_opens_one_exact_offense_probe() -> None:
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=PLAN,
        binding_result=BINDING_RESULT,
        interactions=(interaction(),),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert len(result.targets) == 1
    target = result.targets[0]
    assert target.kind == "instigation"
    assert target.actor.actor_id == "甲"
    assert target.principal == target.members[1]
    assert target.offense_ref == "offense.injury"
    assert len(result.evidence_occurrences) == 1
    assert result.evidence_occurrences[0].actor_id == "甲"


def test_non_responsibility_source_does_not_open_candidate() -> None:
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=PLAN,
        binding_result=BINDING_RESULT,
        interactions=(interaction(),),
        responsibility_actor_ids=("乙",),
        registry=REGISTRY,
    )
    assert not result.targets
    assert result.skipped_interaction_ids == ("finteraction:001:001",)


def test_coordination_uses_bound_member_as_offense_anchor() -> None:
    coordinated = FactualInteraction(
        "finteraction:001:002",
        EPISODE.factual_episode_id,
        "agreement_or_coordinated_conduct",
        "乙",
        ("甲",),
        (
            InteractionEvidence(
                "finteraction:001:002:evidence:001",
                "甲은 乙에게 A를 밀라고 부탁했다.",
                0,
                19,
            ),
        ),
    )
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=PLAN,
        binding_result=BINDING_RESULT,
        interactions=(coordinated,),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert len(result.targets) == 1
    assert result.targets[0].kind == "co_principal_group"
    assert {value.actor_id for value in result.targets[0].members} == {"甲", "乙"}


def test_directed_interaction_can_reach_target_actor_later_episode() -> None:
    later = FactualEpisode(
        "factual_episode:002", EPISODE.source_fragments, EPISODE.participants
    )
    later_binding = IssueBinding(
        "binding:001",
        later.factual_episode_id,
        0,
        "offense.injury",
        "乙",
        (ACTION,),
        (),
        ("A",),
    )
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=PLAN,
        binding_result=IssueBindingResult(
            (EPISODE, later),
            (SeedBindingResult(0, "offense.injury", (later_binding,)),),
        ),
        interactions=(interaction(),),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert len(result.targets) == 1
    assert result.targets[0].principal.occurrence_id == "binding:001"


def test_directed_interaction_does_not_expand_beyond_nearest_later_episode() -> None:
    middle = FactualEpisode(
        "factual_episode:002", EPISODE.source_fragments, EPISODE.participants
    )
    later = FactualEpisode(
        "factual_episode:003", EPISODE.source_fragments, EPISODE.participants
    )
    middle_binding = IssueBinding(
        "binding:001",
        middle.factual_episode_id,
        0,
        "offense.injury",
        "乙",
        (ACTION,),
        (),
        ("A",),
    )
    later_binding = IssueBinding(
        "binding:002",
        later.factual_episode_id,
        1,
        "offense.robbery",
        "乙",
        (ACTION,),
        (),
        ("A",),
    )
    plan = {
        **PLAN,
        "occurrences": [
            *PLAN["occurrences"],
            {
                "occurrence_id": "binding:002",
                "actor_id": "乙",
                "source_text": "乙은 A를 밀었다.",
                "source_span": {"start": 20, "end": len(TEXT)},
            },
        ],
        "top_level_instances": [
            *PLAN["top_level_instances"],
            {
                "case_id": CASE_ID,
                "actor_id": "乙",
                "offense_ref": "offense.robbery",
                "occurrence_id": "binding:002",
            },
        ],
    }
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=plan,
        binding_result=IssueBindingResult(
            (EPISODE, middle, later),
            (
                SeedBindingResult(0, "offense.injury", (middle_binding,)),
                SeedBindingResult(1, "offense.robbery", (later_binding,)),
            ),
        ),
        interactions=(interaction(),),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert len(result.targets) == 1
    assert result.targets[0].offense_ref == "offense.injury"


def test_necessary_counterpart_metadata_suppresses_ordinary_probe() -> None:
    giver = IssueBinding(
        "binding:giver",
        EPISODE.factual_episode_id,
        0,
        "offense.bribe_giving",
        "甲",
        (ACTION,),
        (),
        ("乙",),
    )
    taker = IssueBinding(
        "binding:taker",
        EPISODE.factual_episode_id,
        1,
        "offense.bribery_taking",
        "乙",
        (ACTION,),
        (),
        ("甲",),
    )
    plan = {
        **PLAN,
        "occurrences": [
            {
                "occurrence_id": binding.binding_id,
                "actor_id": binding.actor_id,
                "source_text": "乙은 A를 밀었다.",
                "source_span": {"start": 20, "end": len(TEXT)},
            }
            for binding in (giver, taker)
        ],
        "top_level_instances": [
            {
                "case_id": CASE_ID,
                "actor_id": binding.actor_id,
                "offense_ref": binding.offense_ref,
                "occurrence_id": binding.binding_id,
            }
            for binding in (giver, taker)
        ],
    }
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=plan,
        binding_result=IssueBindingResult(
            (EPISODE,),
            (
                SeedBindingResult(0, giver.offense_ref, (giver,)),
                SeedBindingResult(1, taker.offense_ref, (taker,)),
            ),
        ),
        interactions=(interaction(),),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert result.targets == ()


def test_base_co_group_opens_authored_special_theft_group_after_participation() -> None:
    base = ParticipationLocalTarget(
        "co_principal_group",
        (
            OffenseInstanceKey(CASE_ID, "甲", "offense.theft", "binding:甲"),
            OffenseInstanceKey(CASE_ID, "乙", "offense.theft", "binding:乙"),
        ),
    )
    expanded = derived_co_principal_targets(REGISTRY, (base,))
    assert len(expanded) == 1
    assert expanded[0].offense_ref == "derived_offense.special_theft"
    assert [value.occurrence_id for value in expanded[0].members] == [
        "binding:甲",
        "binding:乙",
    ]
