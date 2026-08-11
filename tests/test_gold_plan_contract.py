from __future__ import annotations

import json
from pathlib import Path

from idpr.v2.gold_factual_identity import load_gold_article263_pairs, load_gold_occurrences

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "experiments/v2_gold_restart_26/evaluation_instance_plan.jsonl"
INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_gold_is_exact_factual_identity_for_all_frozen_cases() -> None:
    plans = _rows(PLAN)
    inventory = {row["sub_question_id"]: row for row in _rows(INVENTORY)}
    case_ids = tuple(row["sub_question_id"] for row in plans)
    gold = load_gold_occurrences(
        ROOT / "data/v2/gold_occurrences.jsonl",
        case_text_by_id={key: value["question_text"] for key, value in inventory.items()},
        required_case_ids=case_ids,
    )
    assert len(gold) == 26
    assert sum(len(value.occurrences) for value in gold.values()) == 67
    pairs = load_gold_article263_pairs(
        ROOT / "data/v2/gold_article263_pairs.jsonl", occurrences_by_id=gold
    )
    assert len(pairs) == 1


def test_plan_top_level_is_exact_occurrence_actor_offense_product() -> None:
    for row in _rows(PLAN):
        case_id = row["sub_question_id"]
        expected = [
            (case_id, occurrence["actor_id"], offense, occurrence["occurrence_id"])
            for occurrence in row["occurrences"]
            for offense in row["candidate_offense_refs"]
        ]
        actual = [
            (key["case_id"], key["actor_id"], key["offense_ref"], key["occurrence_id"])
            for key in row["top_level_instances"]
        ]
        assert actual == expected
        targets = [
            (
                value["instance_key"]["case_id"],
                value["instance_key"]["actor_id"],
                value["instance_key"]["offense_ref"],
                value["instance_key"]["occurrence_id"],
                value["predicate_ref"],
            )
            for value in row["assessment_targets"]
        ]
        assert len(targets) == len(set(targets))
