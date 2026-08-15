from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.v2.issue_binding import (
    IssueBindingContractError,
    binding_seed_cues,
    issue_binding_request_payload,
    issue_binding_schema,
    load_binding_seed_cue_catalog,
    normalize_issue_binding_output,
    validate_issue_binding_output,
)
from idpr.v2.registry import load_definitions

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
CUE_CATALOG = load_binding_seed_cue_catalog(ROOT / "data/v2/binding_seed_cues.yaml")
SEEDS = ("offense.bribe_giving", "offense.embezzlement")
CASE_TEXT = "甲은 丙에게 돈을 전달해 달라고 부탁했다. 丁은 돈 일부를 사용했다."


def test_call15_contract_separates_actions_from_seed_bindings_without_legal_edges() -> None:
    schema = issue_binding_schema(seed_count=2)
    episode = schema["properties"]["factual_episodes"]["items"]["properties"]
    action_fields = set(episode["actions"]["items"]["properties"])
    binding_fields = set(
        schema["properties"]["seed_results"]["items"]["properties"]["bindings"]
        ["items"]["properties"]
    )

    assert set(episode) == {"episode_index", "source_quotes", "participants", "actions"}
    assert action_fields == {
        "action_index",
        "source_actor_id",
        "participant_ids",
        "action_quotes",
    }
    assert binding_fields == {
        "episode_index",
        "actor_id",
        "focal_action_index",
        "supporting_action_indexes",
        "factual_targets",
        "directed_action_target",
        "actual_result_bearer",
        "linked_offender",
    }
    assert not {
        "dependency",
        "participation_mode",
        "truth",
        "binding_id",
        "realization_id",
    } & (action_fields | binding_fields)


def test_full_case_quote_validation_materializes_action_references_not_evidence_bindings() -> None:
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [CASE_TEXT],
                "participants": ["甲", "丙", "丁"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "丙"],
                        "action_quotes": ["甲은 丙에게 돈을 전달해 달라고 부탁했다."],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "丁",
                        "participant_ids": ["丁"],
                        "action_quotes": ["丁은 돈 일부를 사용했다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": ["丙"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    result = validate_issue_binding_output(raw, seeds=SEEDS, case_text=CASE_TEXT)

    assert len(result.seed_results) == len(SEEDS)
    assert not result.seed_results[1].bindings
    binding = result.bindings[0]
    assert binding.binding_id == "binding:001"
    assert binding.factual_episode_id == "factual_episode:001"
    assert binding.offense_ref == "offense.bribe_giving"
    assert binding.focal_action_id == "factual_action:001:001"
    assert binding.supporting_action_ids == ()
    assert result.factual_episodes[0].factual_actions[0].factual_action_id == (
        "factual_action:001:001"
    )
    assert result.factual_episodes[0].factual_actions[0].source_actor_id == "甲"


def test_call15_rejects_synthetic_action_quote() -> None:
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [CASE_TEXT],
                "participants": ["丁"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "丁",
                        "participant_ids": ["丁"],
                        "action_quotes": ["丁은 ... 돈을 사용했다."],
                    }
                ],
            }
        ],
        "seed_results": [
            {"seed_index": 0, "bindings": []},
            {
                "seed_index": 1,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "丁",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": [],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
        ],
    }

    with pytest.raises(IssueBindingContractError):
        validate_issue_binding_output(raw, seeds=SEEDS, case_text=CASE_TEXT)


def test_call15_rejects_overlapping_actions_that_reuse_a_broad_episode_quote() -> None:
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [CASE_TEXT],
                "participants": ["甲", "丙", "丁"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "丙"],
                        "action_quotes": [CASE_TEXT],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "丁",
                        "participant_ids": ["丁"],
                        "action_quotes": ["丁은 돈 일부를 사용했다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {"seed_index": 0, "bindings": []},
            {
                "seed_index": 1,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "丁",
                        "focal_action_index": 1,
                        "supporting_action_indexes": [],
                        "factual_targets": [],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
        ],
    }

    with pytest.raises(IssueBindingContractError, match="must not overlap"):
        validate_issue_binding_output(raw, seeds=SEEDS, case_text=CASE_TEXT)


def test_payload_uses_full_case_and_minimal_closed_seed_cues() -> None:
    cues = binding_seed_cues(REGISTRY, SEEDS, cue_catalog=CUE_CATALOG)
    payload = issue_binding_request_payload(
        question_prompt="甲과 丁의 죄책은?",
        case_text=CASE_TEXT,
        factual_scope_text=CASE_TEXT,
        seed_cues=cues,
    )
    assert set(payload) == {
        "question_prompt",
        "candidate_actor_ids",
        "case_text",
        "factual_scope_text",
        "seeds",
    }
    assert payload["seeds"][0]["display_name"] == "뇌물공여죄"
    assert payload["candidate_actor_ids"] == ["甲", "丁"]
    assert payload["seeds"][0]["minimal_conduct_description"]
    assert "predicate" not in str(payload["seeds"][0]).lower()
    assert ";" not in payload["seeds"][0]["minimal_conduct_description"]


def test_authored_cues_cover_every_frozen_call1_seed() -> None:
    artifact = ROOT / "experiments/v2_restart_rebuild/call1/router_output.jsonl"
    seeds = {
        seed
        for line in artifact.read_text(encoding="utf-8").splitlines()
        for seed in json.loads(line)["normalized_seeds"]
    }
    assert seeds <= set(CUE_CATALOG)


def test_call15_rejects_action_quote_from_another_numbered_fact_scope() -> None:
    full_case = "(1) 甲은 A를 때렸다.\n\n(2) 乙은 B의 돈을 가져갔다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": ["(2) 乙은 B의 돈을 가져갔다."],
                "participants": ["乙", "B"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "乙",
                        "participant_ids": ["乙", "B"],
                        "action_quotes": ["乙은 B의 돈을 가져갔다."],
                    }
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "乙",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": ["B"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    with pytest.raises(IssueBindingContractError, match="outside"):
        validate_issue_binding_output(
            raw,
            seeds=SEEDS,
            case_text=full_case,
            factual_scope_text="(1) 甲은 A를 때렸다.",
        )


def test_call15_rejects_actor_outside_question_responsibility_scope() -> None:
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [CASE_TEXT],
                "participants": ["甲", "丁"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "丁",
                        "participant_ids": ["丁"],
                        "action_quotes": ["丁은 돈 일부를 사용했다."],
                    }
                ],
            }
        ],
        "seed_results": [
            {"seed_index": 0, "bindings": []},
            {
                "seed_index": 1,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "丁",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": [],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
        ],
    }
    with pytest.raises(IssueBindingContractError, match="responsibility actors"):
        validate_issue_binding_output(
            raw,
            seeds=SEEDS,
            case_text=CASE_TEXT,
            candidate_actor_ids=("甲",),
        )


def test_host_normalizes_only_unique_action_copy_error_and_episode_scope() -> None:
    case_text = "甲은 A를 밀었다. A는 넘어져 발목을 다쳤다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": ["甲은 A를 밀었다."],
                "participants": ["甲", "A"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "A"],
                        "action_quotes": ["甲은 A를 밀었."],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "A",
                        "participant_ids": ["A"],
                        "action_quotes": ["A는 넘어져 발목을 다쳤다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [1],
                        "factual_targets": ["A"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)
    result = validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)

    assert len(result.bindings) == 1
    assert {value["reason"] for value in changes} == {
        "unique_single_edit_source_quote",
        "action_quote_added_to_declared_episode_scope",
    }


def test_host_does_not_invent_or_split_a_mixed_action_boundary() -> None:
    case_text = (
        "甲은 창고의 잠긴 출입문을 열어 두었고, 乙은 주변에서 망을 보았으며, "
        "丙은 창고 안의 물건을 가져갔다."
    )
    mixed_quote = "甲은 창고의 잠긴 출입문을 열어 두었고, 丙은 창고 안의 물건을 가져갔다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [case_text],
                "participants": ["甲", "乙", "丙"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "丙"],
                        "action_quotes": [mixed_quote],
                    }
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": ["丙"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)

    assert not changes
    with pytest.raises(IssueBindingContractError):
        validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)


def test_host_replaces_invalid_episode_copy_with_its_exact_action_quotes() -> None:
    case_text = "甲은 <u>A를 밀었다.</u> A는 넘어졌다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": ["甲은 A를 밀었. A는 넘어졌다."],
                "participants": ["甲", "A"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "A"],
                        "action_quotes": ["A를 밀었다."],
                    }
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": ["A"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)
    validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)

    assert normalized["factual_episodes"][0]["source_quotes"] == ["A를 밀었다."]
    assert any(
        change["reason"] == "invalid_episode_source_replaced_by_action_quotes"
        for change in changes
    )


def test_accessory_binds_to_the_principal_execution_action_it_supported() -> None:
    """An accessory's own conduct is a supporting action, not the focal one.

    Requiring the responsibility actor to participate in the focal action would
    make every accessory, instigator, and co-principal binding unrepresentable,
    which is how three of the 26 KCL questions were failing outright.
    """

    case_text = "丙이 문을 열어주고 망을 보는 사이 甲은 금고를 열었다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [case_text],
                "participants": ["甲", "丙"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "丙",
                        "participant_ids": ["丙"],
                        "action_quotes": ["丙이 문을 열어주고 망을 보는 사이"],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲"],
                        "action_quotes": ["甲은 금고를 열었다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "丙",
                        "focal_action_index": 1,
                        "supporting_action_indexes": [0],
                        "factual_targets": [],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    result = validate_issue_binding_output(raw, seeds=SEEDS, case_text=case_text)

    binding = result.seed_results[0].bindings[0]
    assert binding.actor_id == "丙"
    assert binding.focal_action_id == "factual_action:001:002"
    assert binding.supporting_action_ids == ("factual_action:001:001",)


def test_actor_absent_from_every_carried_action_is_still_rejected() -> None:
    case_text = "丙이 문을 열어주고 망을 보는 사이 甲은 금고를 열었다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [case_text],
                "participants": ["甲", "丙"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "丙",
                        "participant_ids": ["丙"],
                        "action_quotes": ["丙이 문을 열어주고 망을 보는 사이"],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲"],
                        "action_quotes": ["甲은 금고를 열었다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "丙",
                        "focal_action_index": 1,
                        "supporting_action_indexes": [],
                        "factual_targets": [],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    with pytest.raises(IssueBindingContractError):
        validate_issue_binding_output(raw, seeds=SEEDS, case_text=case_text)


def test_incidental_source_actor_is_registered_instead_of_failing_the_case() -> None:
    """A rescue crew the model used but never declared is a naming slip.

    The label is already in the case text and the action is already authored, so
    the host registers it rather than discarding a whole question over it.
    """

    case_text = "甲은 A를 밀었다. 출동한 구조대에 의해 이송된 A는 목숨을 건졌다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [case_text],
                "participants": ["甲", "A"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "A"],
                        "action_quotes": ["甲은 A를 밀었다."],
                    },
                    {
                        "action_index": 1,
                        "source_actor_id": "구조대",
                        "participant_ids": ["A"],
                        "action_quotes": ["출동한 구조대에 의해 이송된 A는 목숨을 건졌다."],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [1],
                        "factual_targets": ["A"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }

    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)
    result = validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)

    assert "구조대" in normalized["factual_episodes"][0]["participants"]
    assert any(
        change["reason"] == "action_source_actor_added_to_episode_participants"
        for change in changes
    )
    assert result.seed_results[0].bindings[0].actor_id == "甲"


_MISTAKE_CASE_TEXT = (
    "甲은 어두운 골목에서 乙인 줄 알고 C의 머리를 각목으로 내리쳤다. "
    "C는 전치 4주의 상해를 입었다."
)


def _mistake_payload(**binding: object) -> dict[str, object]:
    return {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [_MISTAKE_CASE_TEXT],
                "participants": ["甲", "乙", "C"],
                "actions": [
                    {
                        "action_index": 0,
                        "source_actor_id": "甲",
                        "participant_ids": ["甲", "乙", "C"],
                        "action_quotes": [
                            "甲은 어두운 골목에서 乙인 줄 알고 C의 머리를 각목으로 내리쳤다."
                        ],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "focal_action_index": 0,
                        "supporting_action_indexes": [],
                        "factual_targets": ["C"],
                        "directed_action_target": None,
                        "actual_result_bearer": None,
                        "linked_offender": None,
                        **binding,
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }


def test_directed_target_and_result_bearer_are_bound_as_separate_identities() -> None:
    """객체착오는 두 대상이 각각 사실로 결박되어야 표현된다.

    `factual_targets`는 상대방·수령자까지 담는 넓은 집합이라 "겨냥한 대상"을 여기서 읽으면
    host가 원문에 없는 의미를 만들게 된다. 그래서 좁은 필드를 따로 둔다.
    """
    result = validate_issue_binding_output(
        _mistake_payload(directed_action_target="乙", actual_result_bearer="C"),
        seeds=SEEDS,
        case_text=_MISTAKE_CASE_TEXT,
    )
    binding = result.bindings[0]

    assert binding.directed_action_target == "乙"
    assert binding.actual_result_bearer == "C"
    assert binding.factual_targets == ("C",)
    assert binding.linked_offender is None


def test_narrow_identities_are_scoped_to_the_evidence_the_binding_carries() -> None:
    """episode participant가 아니라 focal/supporting action의 participant여야 한다.

    episode는 의도적으로 넓은 서사 맥락이다. episode 범위로 검사하면 이 행위와 무관한
    사람이 "이 행위가 겨냥한 대상"으로 들어올 수 있다.
    """
    # 乙은 episode participant지만 이 focal action이 carry하는 사람은 아니다.
    payload = _mistake_payload(directed_action_target="乙")
    payload["factual_episodes"][0]["actions"][0]["participant_ids"] = ["甲", "C"]

    with pytest.raises(IssueBindingContractError, match="directed_action_target"):
        validate_issue_binding_output(
            payload, seeds=SEEDS, case_text=_MISTAKE_CASE_TEXT
        )


def test_linked_offender_is_refused_on_a_seed_the_host_did_not_mark() -> None:
    """어떤 죄가 타인의 범죄를 전제로 하는지는 저작된 법적 성질이지 모델의 판단이 아니다."""
    with pytest.raises(IssueBindingContractError, match="linked_offender"):
        validate_issue_binding_output(
            _mistake_payload(linked_offender="乙"),
            seeds=SEEDS,
            case_text=_MISTAKE_CASE_TEXT,
            linked_offender_seed_refs=(),
        )


def test_linked_offender_is_accepted_on_the_authored_dependency_seed() -> None:
    from idpr.v2.issue_binding import linked_offender_role, linked_offender_seed_refs

    seeds = ("offense.harboring_or_escape", "offense.embezzlement")
    assert linked_offender_role(REGISTRY, "offense.harboring_or_escape") == "article151_offender"
    assert linked_offender_role(REGISTRY, "offense.embezzlement") is None
    assert linked_offender_seed_refs(REGISTRY, seeds) == ("offense.harboring_or_escape",)

    result = validate_issue_binding_output(
        _mistake_payload(linked_offender="乙"),
        seeds=seeds,
        case_text=_MISTAKE_CASE_TEXT,
        linked_offender_seed_refs=linked_offender_seed_refs(REGISTRY, seeds),
    )

    assert result.bindings[0].linked_offender == "乙"


def test_seed_cue_tells_the_model_which_seed_may_bind_a_linked_offender() -> None:
    cues = binding_seed_cues(
        REGISTRY,
        ("offense.harboring_or_escape", "offense.embezzlement"),
        cue_catalog=CUE_CATALOG,
    )

    assert cues[0].as_dict()["requires_linked_offender"] == "article151_offender"
    assert "requires_linked_offender" not in cues[1].as_dict()


def test_the_binding_prompt_states_a_non_partition_contract() -> None:
    """"참조할 수 있다"는 모델에게 permission으로 읽힌다 -- 그리고 permission은 쓰이지 않았다.

    `r10_p1_q2`에서 모델은 구타 action을 폭행죄 seed에만 배분하고 상해죄에는 결과만 남겼다.
    행위자가 자기 realization의 증거에 없으니 계약이 거부했고, 온도를 올려 6회를 돌려도 같은
    배분을 반복했다. 고칠 자리는 그 사안이나 폭행 cue가 아니라, seed 사이에 증거를 나누어
    갖는 행동 자체를 금지하는 계약이다. 그 문구가 프롬프트에서 사라지면 같은 회귀가 조용히
    돌아온다.
    """
    prompt = (ROOT / "prompts/v2_call15_issue_binding.md").read_text(encoding="utf-8")

    assert "seed result는 서로 독립이며 배타적이지 않다" in prompt
    assert "나누어 배분하지" in prompt
    assert "소모하지도" in prompt
