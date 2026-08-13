from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.v2.gold_factual_identity import (
    GoldFactualIdentityError,
    load_gold_factual_participants,
)
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"


def _inventory() -> dict[str, dict]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in INVENTORY.read_text(encoding="utf-8").splitlines()
            if line
        )
    }


def test_reviewed_factual_participants_are_sparse_source_local_and_legally_untyped() -> None:
    inventory = _inventory()
    values = load_gold_factual_participants(
        ROOT / "data/v2/gold_factual_participants.jsonl",
        case_text_by_id={key: row["question_text"] for key, row in inventory.items()},
    )
    assert len(values) == 6
    assert sum(len(value.participants) for value in values.values()) == 6
    assert {value.participants[0].participant_label for value in values.values()} == {
        "A", "B", "C", "乙", "丙", "결재권자"
    }
    for participant_set in values.values():
        rendered = participant_set.as_dict()
        participant = rendered["participants"][0]
        assert set(participant) == {
            "participant_id", "participant_label", "source_text", "source_span"
        }
        assert not ({"offense_ref", "mode", "role", "truth"} & set(participant))


def test_factual_participant_namespace_cannot_equal_liability_instance_namespace() -> None:
    participant = FactualParticipantKey("case", "fpart:001")
    liability = OffenseInstanceKey("case", "A", "offense.test", "gocc:001")
    assert participant != liability
    assert not hasattr(participant, "offense_ref")
    assert not hasattr(participant, "actor_id")


def test_factual_participant_loader_rejects_legal_labels(tmp_path: Path) -> None:
    path = tmp_path / "participants.jsonl"
    path.write_text(
        json.dumps({
            "sub_question_id": "case",
            "participants": [{
                "participant_id": "fpart:001",
                "participant_label": "A",
                "source_text": "A acted",
                "role": "indirect_tool",
            }],
        }),
        encoding="utf-8",
    )
    with pytest.raises(GoldFactualIdentityError, match="allowed fields"):
        load_gold_factual_participants(path, case_text_by_id={"case": "A acted"})
