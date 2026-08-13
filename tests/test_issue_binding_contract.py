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


def test_call15_contract_separates_actor_action_and_context_without_legal_edges() -> None:
    schema = issue_binding_schema(seed_count=2)
    result = schema["properties"]["seed_results"]["items"]["properties"]
    fields = set(result["bindings"]["items"]["properties"])
    assert fields == {
        "episode_index",
        "actor_id",
        "actor_action_quotes",
        "context_quotes",
        "factual_targets",
    }
    assert not {"dependency", "participation_mode", "truth", "binding_id"} & fields


def test_full_case_quote_validation_and_host_identity() -> None:
    raw = {
        "factual_episodes": [
            {"episode_index": 0, "source_quotes": [CASE_TEXT], "participants": ["甲", "丙", "丁"]}
        ],
        "seed_results": [
            {"seed_index": 0, "bindings": [{
                "episode_index": 0, "actor_id": "甲",
                "actor_action_quotes": ["甲은 丙에게 돈을 전달해 달라고 부탁했다."],
                "context_quotes": ["丁은 돈 일부를 사용했다."], "factual_targets": ["丙"],
            }]},
            {"seed_index": 1, "bindings": []},
        ]
    }
    result = validate_issue_binding_output(raw, seeds=SEEDS, case_text=CASE_TEXT)
    assert len(result.seed_results) == len(SEEDS)
    assert not result.seed_results[1].bindings
    value = result.bindings[0]
    assert value.binding_id == "binding:001"
    assert value.factual_episode_id == "factual_episode:001"
    assert value.offense_ref == "offense.bribe_giving"
    assert value.actor_action_fragments[0].fragment_id == (
        "binding:001:actor_action:001"
    )
    assert value.context_fragments[0].fragment_kind == "context"


def test_call15_rejects_synthetic_or_repeated_quote() -> None:
    raw = {
        "factual_episodes": [{"episode_index": 0, "source_quotes": [CASE_TEXT], "participants": ["丁"]}],
        "seed_results": [
            {"seed_index": 0, "bindings": []},
            {"seed_index": 1, "bindings": [{
                "episode_index": 0,
                "actor_id": "丁",
                "actor_action_quotes": ["丁은 ... 돈을 사용했다."],
                "context_quotes": [],
                "factual_targets": [],
            }]},
        ]
    }
    with pytest.raises(IssueBindingContractError):
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


def test_call15_rejects_quote_from_another_numbered_fact_scope() -> None:
    full_case = "(1) 甲은 A를 때렸다.\n\n(2) 乙은 B의 돈을 가져갔다."
    raw = {
        "factual_episodes": [{"episode_index": 0, "source_quotes": ["(2) 乙은 B의 돈을 가져갔다."], "participants": ["乙", "B"]}],
        "seed_results": [
            {"seed_index": 0, "bindings": [{
                "episode_index": 0,
                "actor_id": "乙",
                "actor_action_quotes": ["乙은 B의 돈을 가져갔다."],
                "context_quotes": [],
                "factual_targets": ["B"],
            }]},
            {"seed_index": 1, "bindings": []},
        ]
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
        "factual_episodes": [{"episode_index": 0, "source_quotes": [CASE_TEXT], "participants": ["甲", "丁"]}],
        "seed_results": [
            {"seed_index": 0, "bindings": []},
            {"seed_index": 1, "bindings": [{
                "episode_index": 0,
                "actor_id": "丁",
                "actor_action_quotes": ["丁은 돈 일부를 사용했다."],
                "context_quotes": [],
                "factual_targets": [],
            }]},
        ]
    }
    with pytest.raises(IssueBindingContractError, match="responsibility actors"):
        validate_issue_binding_output(
            raw,
            seeds=SEEDS,
            case_text=CASE_TEXT,
            candidate_actor_ids=("甲",),
        )


def test_host_normalizes_only_unique_copy_error_and_episode_scope() -> None:
    case_text = "甲은 A를 밀었다. A는 넘어져 발목을 다쳤다."
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": ["甲은 A를 밀었다."],
                "participants": ["甲", "A"],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "actor_action_quotes": ["甲은 A를 밀었."],
                        "context_quotes": ["A는 넘어져 발목을 다쳤다."],
                        "factual_targets": ["A"],
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
        "binding_quote_added_to_declared_episode_scope",
    }


def test_host_splits_only_uniquely_elided_context_quote() -> None:
    case_text = (
        "甲은 창고의 잠긴 출입문을 열어 두었고, 乙은 주변에서 망을 보았으며, "
        "丙은 창고 안의 물건을 가져갔다."
    )
    raw = {
        "factual_episodes": [
            {
                "episode_index": 0,
                "source_quotes": [case_text],
                "participants": ["甲", "乙", "丙"],
            }
        ],
        "seed_results": [
            {
                "seed_index": 0,
                "bindings": [
                    {
                        "episode_index": 0,
                        "actor_id": "甲",
                        "actor_action_quotes": ["甲은 창고의 잠긴 출입문을 열어 두었고"],
                        "context_quotes": [
                            (
                                "甲은 창고의 잠긴 출입문을 열어 두었고, "
                                "丙은 창고 안의 물건을 가져갔다."
                            )
                        ],
                        "factual_targets": ["丙"],
                    }
                ],
            },
            {"seed_index": 1, "bindings": []},
        ],
    }
    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)
    validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)
    assert changes[0]["reason"] == "unique_single_elision_split"


def test_host_replaces_invalid_episode_copy_with_its_exact_binding_quotes() -> None:
    case_text = "甲은 <u>A를 밀었다.</u> A는 넘어졌다."
    raw = {
        "factual_episodes": [{
            "episode_index": 0,
            "source_quotes": ["甲은 A를 밀었. A는 넘어졌다."],
            "participants": ["甲", "A"],
        }],
        "seed_results": [
            {"seed_index": 0, "bindings": [{
                "episode_index": 0,
                "actor_id": "甲",
                "actor_action_quotes": ["A를 밀었다."],
                "context_quotes": ["A는 넘어졌다."],
                "factual_targets": ["A"],
            }]},
            {"seed_index": 1, "bindings": []},
        ],
    }

    normalized, changes = normalize_issue_binding_output(raw, case_text=case_text)
    validate_issue_binding_output(normalized, seeds=SEEDS, case_text=case_text)

    assert normalized["factual_episodes"][0]["source_quotes"] == [
        "A를 밀었다.",
        "A는 넘어졌다.",
    ]
    assert any(
        change["reason"] == "invalid_episode_source_replaced_by_binding_quotes"
        for change in changes
    )
