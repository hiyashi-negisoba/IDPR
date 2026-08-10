from __future__ import annotations

import json
from pathlib import Path

from idpr.v2.registry import load_definitions
from idpr.v2.routing import router_catalog


ROOT = Path(__file__).resolve().parents[1]
GOLD_PATH = ROOT / "data/eval/v2_call1_definition_gold_draft.json"
CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"


def test_definition_gold_draft_is_exactly_the_closed_26_case_cohort() -> None:
    payload = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    listed_cases = [row["case_id"] for row in payload["cases"]]
    expected_cases = [
        line.strip() for line in CASE_LIST.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    assert payload["status"] == "approved_user_reviewed_for_step8_call1_v0"
    assert listed_cases == expected_cases


def test_definition_gold_draft_uses_only_closed_catalog_refs_without_duplicates() -> None:
    payload = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    registry = load_definitions(ROOT / "data/v2/definitions")
    allowed = {entry.definition_id for entry in router_catalog(registry)}
    for row in payload["cases"]:
        refs = row["gold_definition_refs"]
        if not refs:
            assert any("outside the closed catalog" in note for note in row["scope_notes"]), row["case_id"]
        assert len(refs) == len(set(refs)), row["case_id"]
        assert set(refs) <= allowed, row["case_id"]
