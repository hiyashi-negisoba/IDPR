"""Unit tests for Scallop Proof DAG Extractor and relation parser."""

from __future__ import annotations

from idpr.rulegen.scallop_runtime import parse_scallop_relations, extract_proof_dag


def test_parse_scallop_relations_empty_and_tuples() -> None:
    sample_output = """
    theft_object_ownership_satisfied: {("case_001", "def_001", "owner_001", "poss_001")}
    theft_not_established: {}
    theft_established: {("case_001", "def_001", "owner_001", "poss_001")}
    """

    results = parse_scallop_relations(sample_output)

    assert "theft_object_ownership_satisfied" in results
    assert len(results["theft_object_ownership_satisfied"]) == 1
    assert ("case_001", "def_001", "owner_001", "poss_001") in results["theft_object_ownership_satisfied"]

    assert "theft_not_established" in results
    assert len(results["theft_not_established"]) == 0

    assert "theft_established" in results
    assert len(results["theft_established"]) == 1


def test_extract_proof_dag_fired_rules() -> None:
    rule_ir = {
        "rules": [
            {
                "id": "theft.rule.001",
                "head": {"name": "theft_object_ownership_satisfied"},
                "body": [{"name": "satisfied_card_001"}],
                "description": "Rule 1 satisfied",
            },
            {
                "id": "theft.rule.002",
                "head": {"name": "theft_not_established"},
                "body": [{"name": "satisfied_card_002"}],
                "description": "Rule 2 not satisfied",
            },
        ]
    }

    relations_tuples = {
        "satisfied_card_001": {("case_001",)},
        "theft_object_ownership_satisfied": {("case_001",)},
        "satisfied_card_002": set(),
        "theft_not_established": set(),
    }

    dag = extract_proof_dag(
        rule_ir=rule_ir,
        relations_tuples=relations_tuples,
        query_relations=["theft_object_ownership_satisfied", "theft_not_established"],
    )

    assert "theft.rule.001" in dag["fired_rules"]
    assert "theft.rule.002" not in dag["fired_rules"]
    assert "theft_object_ownership_satisfied" in dag["proof_tree"]
    assert dag["proof_tree"]["theft_object_ownership_satisfied"][0]["rule_id"] == "theft.rule.001"
