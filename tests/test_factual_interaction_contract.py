from __future__ import annotations

import pytest

from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    factual_interaction_request_payload,
    factual_interaction_schema,
    validate_factual_interaction_output,
)
from idpr.v2.issue_binding import BindingFragment, FactualEpisode

CASE_TEXT = "甲은 乙에게 A를 밀라고 부탁했다. 乙은 A를 밀었다."
EPISODE = FactualEpisode(
    "factual_episode:001",
    (
        BindingFragment(
            "factual_episode:001:episode_source:001",
            "episode_source",
            CASE_TEXT,
            0,
            len(CASE_TEXT),
        ),
    ),
    ("甲", "乙", "A"),
)


def test_factual_interaction_contract_is_offense_free() -> None:
    schema = factual_interaction_schema()
    fields = set(
        schema["properties"]["interactions"]["items"]["properties"]
    )
    assert fields == {
        "interaction_type",
        "source_actor_id",
        "target_actor_ids",
        "evidence_quotes",
    }
    assert not {"offense_ref", "participation_mode", "truth"} & fields


def test_request_payload_contains_one_episode_and_no_legal_seed() -> None:
    payload = factual_interaction_request_payload(
        case_id="case-1",
        question_prompt="甲과 乙의 죄책은?",
        responsibility_actor_ids=("甲", "乙"),
        episode=EPISODE,
    )
    assert payload["factual_episode_id"] == "factual_episode:001"
    assert payload["episode_participant_ids"] == ["甲", "乙", "A"]
    assert "offense" not in str(payload).lower()


def test_validator_assigns_stable_identity_and_exact_span() -> None:
    values = validate_factual_interaction_output(
        {
            "interactions": [
                {
                    "interaction_type": "request_or_instruction",
                    "source_actor_id": "甲",
                    "target_actor_ids": ["乙"],
                    "evidence_quotes": ["甲은 乙에게 A를 밀라고 부탁했다."],
                }
            ]
        },
        case_text=CASE_TEXT,
        episode=EPISODE,
    )
    assert values[0].interaction_id == "finteraction:001:001"
    assert values[0].evidence[0].source_start == 0
    assert values[0].target_actor_ids == ("乙",)


def test_validator_accepts_explicit_empty_interactions() -> None:
    assert not validate_factual_interaction_output(
        {"interactions": []}, case_text=CASE_TEXT, episode=EPISODE
    )


@pytest.mark.parametrize(
    "payload, message",
    [
        (
            {
                "interactions": [
                    {
                        "interaction_type": "request_or_instruction",
                        "source_actor_id": "甲",
                        "target_actor_ids": ["甲"],
                        "evidence_quotes": ["甲은 乙에게 A를 밀라고 부탁했다."],
                    }
                ]
            },
            "self-link",
        ),
        (
            {
                "interactions": [
                    {
                        "interaction_type": "instigation",
                        "source_actor_id": "甲",
                        "target_actor_ids": ["乙"],
                        "evidence_quotes": ["甲은 乙에게 A를 밀라고 부탁했다."],
                    }
                ]
            },
            "interaction_type",
        ),
        (
            {
                "interactions": [
                    {
                        "interaction_type": "request_or_instruction",
                        "source_actor_id": "甲",
                        "target_actor_ids": ["乙"],
                        "evidence_quotes": ["甲은 乙에게 ... 부탁했다."],
                    }
                ]
            },
            "exactly once",
        ),
    ],
)
def test_validator_rejects_legal_type_self_link_and_synthetic_quote(
    payload: dict[str, object], message: str
) -> None:
    with pytest.raises(FactualInteractionContractError, match=message):
        validate_factual_interaction_output(
            payload, case_text=CASE_TEXT, episode=EPISODE
        )
