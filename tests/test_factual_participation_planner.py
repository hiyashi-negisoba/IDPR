from __future__ import annotations

from pathlib import Path

from idpr.v2.factual_interaction import FactualInteraction, InteractionEvidence
from idpr.v2.issue_binding import (
    BindingFragment,
    FactualAction,
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


def _episode(episode_id: str) -> FactualEpisode:
    number = episode_id.rsplit(":", maxsplit=1)[1]
    action_id = f"factual_action:{number}:001"
    action_quote = "乙은 A를 밀었다."
    start = TEXT.index(action_quote)
    action = FactualAction(
        action_id,
        episode_id,
        "乙",
        ("乙", "A"),
        (
            BindingFragment(
                f"{action_id}:factual_action:001",
                "factual_action",
                action_quote,
                start,
                start + len(action_quote),
            ),
        ),
        0,
    )
    return FactualEpisode(
        episode_id,
        (
            BindingFragment(
                f"{episode_id}:episode_source:001",
                "episode_source",
                TEXT,
                0,
                len(TEXT),
            ),
        ),
        ("甲", "乙", "A"),
        (action,),
    )


def _binding(
    number: int,
    *,
    episode: FactualEpisode,
    seed_index: int,
    offense_ref: str,
    actor_id: str = "乙",
    factual_targets: tuple[str, ...] = ("A",),
) -> IssueBinding:
    return IssueBinding(
        f"binding:{number:03d}",
        episode.factual_episode_id,
        seed_index,
        offense_ref,
        actor_id,
        episode.factual_actions[0].factual_action_id,
        (),
        factual_targets,
    )


def _plan_row(
    *instances: tuple[str, str, str, str],
) -> dict[str, object]:
    """Create a planner row carrying realization, not binding, identity."""
    return {
        "occurrences": [
            {
                "occurrence_id": realization_id,
                "actor_id": actor_id,
                "source_text": "乙은 A를 밀었다.",
                "source_span": {"start": TEXT.index("乙은 A를 밀었다."), "end": len(TEXT)},
            }
            for actor_id, offense_ref, realization_id, _ in instances
        ],
        "top_level_instances": [
            {
                "case_id": CASE_ID,
                "actor_id": actor_id,
                "offense_ref": offense_ref,
                "occurrence_id": realization_id,
            }
            for actor_id, offense_ref, realization_id, _ in instances
        ],
        "instance_provenance": [
            {
                "instance_key": {
                    "case_id": CASE_ID,
                    "actor_id": actor_id,
                    "offense_ref": offense_ref,
                    "occurrence_id": realization_id,
                },
                "factual_episode_id": episode_id,
                "source_binding_ids": [],
                "realization_id": realization_id,
            }
            for actor_id, offense_ref, realization_id, episode_id in instances
        ],
        "derived_binding_candidates": [],
        "participation_local_targets": [],
    }


EPISODE = _episode("factual_episode:001")
BINDING = _binding(
    1,
    episode=EPISODE,
    seed_index=0,
    offense_ref="offense.injury",
)
BINDING_RESULT = IssueBindingResult(
    (EPISODE,),
    (SeedBindingResult(0, "offense.injury", (BINDING,)),),
)
PLAN = _plan_row(("乙", "offense.injury", "realization:001", EPISODE.factual_episode_id))


def interaction(kind: str = "request_or_instruction") -> FactualInteraction:
    return FactualInteraction(
        "finteraction:001:001",
        EPISODE.factual_episode_id,
        kind,  # type: ignore[arg-type]
        "甲",
        ("乙",),
        (
            InteractionEvidence(
                "finteraction:001:001:evidence:001",
                "甲은 乙에게 A를 밀라고 부탁했다.",
                0,
                TEXT.index("乙은 A를 밀었다."),
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
    assert target.principal.occurrence_id == "realization:001"
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


def test_coordination_uses_realization_member_as_offense_anchor() -> None:
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
                TEXT.index("乙은 A를 밀었다."),
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
    assert any(
        value.occurrence_id == "realization:001" for value in result.targets[0].members
    )


def test_directed_interaction_can_reach_target_actor_later_episode() -> None:
    later = _episode("factual_episode:002")
    later_binding = _binding(
        1,
        episode=later,
        seed_index=0,
        offense_ref="offense.injury",
    )
    plan = _plan_row(
        ("乙", "offense.injury", "realization:001", later.factual_episode_id)
    )
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=plan,
        binding_result=IssueBindingResult(
            (EPISODE, later),
            (SeedBindingResult(0, "offense.injury", (later_binding,)),),
        ),
        interactions=(interaction(),),
        responsibility_actor_ids=("甲", "乙"),
        registry=REGISTRY,
    )
    assert len(result.targets) == 1
    assert result.targets[0].principal.occurrence_id == "realization:001"


def test_directed_interaction_does_not_expand_beyond_nearest_later_episode() -> None:
    middle = _episode("factual_episode:002")
    later = _episode("factual_episode:003")
    middle_binding = _binding(
        1,
        episode=middle,
        seed_index=0,
        offense_ref="offense.injury",
    )
    later_binding = _binding(
        2,
        episode=later,
        seed_index=1,
        offense_ref="offense.robbery",
    )
    plan = _plan_row(
        ("乙", "offense.injury", "realization:001", middle.factual_episode_id),
        ("乙", "offense.robbery", "realization:002", later.factual_episode_id),
    )
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
    episode = _episode("factual_episode:001")
    giver = _binding(
        1,
        episode=episode,
        seed_index=0,
        offense_ref="offense.bribe_giving",
        actor_id="甲",
        factual_targets=("乙",),
    )
    taker = _binding(
        2,
        episode=episode,
        seed_index=1,
        offense_ref="offense.bribery_taking",
        actor_id="乙",
        factual_targets=("甲",),
    )
    plan = _plan_row(
        ("甲", giver.offense_ref, "realization:001", episode.factual_episode_id),
        ("乙", taker.offense_ref, "realization:002", episode.factual_episode_id),
    )
    result = materialize_factual_participation_candidates(
        case_id=CASE_ID,
        plan_row=plan,
        binding_result=IssueBindingResult(
            (episode,),
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
            OffenseInstanceKey(CASE_ID, "甲", "offense.theft", "realization:001"),
            OffenseInstanceKey(CASE_ID, "乙", "offense.theft", "realization:002"),
        ),
    )
    expanded = derived_co_principal_targets(REGISTRY, (base,))
    assert len(expanded) == 1
    assert expanded[0].offense_ref == "derived_offense.special_theft"
    assert [value.occurrence_id for value in expanded[0].members] == [
        "realization:001",
        "realization:002",
    ]
