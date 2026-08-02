from __future__ import annotations

import pytest

from idpr.eval.e2e_contract import (
    E2EContractError,
    SMOKE_CASE_IDS,
    index_exact,
    validate_smoke_inventory,
    validate_symbolic_relations,
)
from idpr.rulebase.compile_scl import QUERY_RELATIONS
from scripts.run_l0_candidates import gold_for_inventory


def _inventory():
    return [
        {
            "sub_question_id": case_id,
            "question_text": f"{case_id} 사실",
            "question_prompt": "죄책을 논하시오.",
        }
        for case_id in SMOKE_CASE_IDS
    ]


def test_smoke_inventory_is_exactly_two_whitelisted_model_inputs():
    indexed = validate_smoke_inventory(_inventory())
    assert tuple(indexed) == SMOKE_CASE_IDS

    leaking = _inventory()
    leaking[0]["rubric_summary"] = "정답"
    with pytest.raises(E2EContractError, match="whitelist mismatch"):
        validate_smoke_inventory(leaking)


def test_smoke_inventory_rejects_missing_extra_and_duplicate_cases():
    with pytest.raises(E2EContractError, match="expected exactly"):
        validate_smoke_inventory(_inventory()[:1])
    with pytest.raises(E2EContractError, match="duplicate"):
        index_exact(
            [*_inventory(), _inventory()[0]],
            source="test",
            expected_ids=SMOKE_CASE_IDS,
        )


def test_symbolic_contract_requires_every_query_and_matching_case_ids():
    case_id = SMOKE_CASE_IDS[1]
    relations = {relation: [] for relation in QUERY_RELATIONS}
    relations["final_offense"] = [[case_id, "art347"]]
    validate_symbolic_relations(relations, case_id=case_id)

    del relations["contradiction"]
    with pytest.raises(E2EContractError, match="missing"):
        validate_symbolic_relations(relations, case_id=case_id)

    relations["contradiction"] = [["another-case", "conflict"]]
    with pytest.raises(E2EContractError, match="mismatched case id"):
        validate_symbolic_relations(relations, case_id=case_id)


def test_l0_report_gold_is_limited_to_the_invocation_inventory():
    gold = {"case-a": object(), "case-b": object(), "case-c": object()}
    inventory = {"case-b": {}, "custom-case": {}}
    assert gold_for_inventory(gold, inventory) == {"case-b": gold["case-b"]}
