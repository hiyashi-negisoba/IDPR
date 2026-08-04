from __future__ import annotations

from pathlib import Path

from scripts.build_p2_native_decision_ledger import (
    P2_MANIFEST,
    QUEUE_DIR,
    build_ledger,
    declared_unit_ids,
    read_json,
    validate,
)


UNIT = "arson_of_occupied_structure"


def approval() -> dict:
    return read_json(QUEUE_DIR / f"{UNIT}_approved_decisions.json")


def queue() -> dict:
    return read_json(QUEUE_DIR / f"{UNIT}_review_queue.json")


def contract() -> dict:
    return read_json(P2_MANIFEST)["review_contract"]


def test_repository_unit_ledger_satisfies_the_review_contract() -> None:
    ledger = build_ledger(UNIT)
    assert ledger["problems"] == []
    assert ledger["status"] == "ready_for_rule_ir"
    assert ledger["stats"]["queue_cards"] == len(queue()["cards"])


def test_every_queue_card_receives_exactly_one_decision() -> None:
    queue_ids = [card["card_id"] for card in queue()["cards"]]
    decided = [card["card_id"] for card in approval()["cards"]]
    assert sorted(decided) == sorted(queue_ids)


def test_a_missing_decision_blocks_the_ledger_instead_of_defaulting() -> None:
    payload = approval()
    payload["cards"] = payload["cards"][:-1]
    problems, _ = validate(payload, queue(), contract(), declared_unit_ids())
    assert any("decision missing for queue card" in item for item in problems)


def test_unknown_track_is_rejected() -> None:
    payload = approval()
    target = next(card for card in payload["cards"] if card.get("track_id"))
    target["track_id"] = "track_that_was_never_declared"
    problems, _ = validate(payload, queue(), contract(), declared_unit_ids())
    assert any("track not declared" in item for item in problems)


def test_role_outside_the_contract_is_rejected() -> None:
    payload = approval()
    payload["cards"][0]["role"] = "invented_role"
    problems, _ = validate(payload, queue(), contract(), declared_unit_ids())
    assert any("role not allowed" in item for item in problems)


def test_reference_to_an_undeclared_unit_is_reported_not_silently_dropped() -> None:
    ledger = build_ledger(UNIT)
    unresolved = ledger["unresolved_unit_references"]
    assert unresolved, "boundary cards point outside the current article scope"
    assert all(item["status"] == "predicate_ir_missing" for item in unresolved)
    known = declared_unit_ids()
    assert all(item["refers_to_unit"] not in known for item in unresolved)


def test_resolved_references_stay_out_of_the_missing_list() -> None:
    ledger = build_ledger(UNIT)
    missing = {item["refers_to_unit"] for item in ledger["unresolved_unit_references"]}
    referenced = {
        target
        for component in ledger["components"]
        for target in component["refers_to_units"]
    }
    assert referenced - missing <= declared_unit_ids()


def test_split_card_contributes_every_part_as_its_own_placement() -> None:
    payload = approval()
    splits = [card for card in payload["cards"] if card["decision"] == "split"]
    assert splits, "the reviewer split at least one card"
    ledger = build_ledger(UNIT)
    placed = {
        card_id
        for component in ledger["components"]
        for card_id in component["norm_card_ids"]
    }
    for card in splits:
        assert len(card["parts"]) >= 2
        assert card["card_id"] in placed


def test_one_component_cannot_be_both_conjunctive_and_alternative() -> None:
    ledger = build_ledger(UNIT)
    for component in ledger["components"]:
        assert len(component["joins"]) <= 1, component


def test_context_only_cards_are_excluded_from_components() -> None:
    ledger = build_ledger(UNIT)
    excluded = {item["card_id"] for item in ledger["excluded_cards"]}
    placed = {
        card_id
        for component in ledger["components"]
        for card_id in component["norm_card_ids"]
    }
    assert excluded
    assert not (excluded & placed)


def test_ledger_pins_the_approval_hash_so_edits_cannot_pass_unnoticed() -> None:
    ledger = build_ledger(UNIT)
    path = Path(ledger["approval_document"])
    assert path.name.endswith("_approved_decisions.json")
    assert len(ledger["approval_sha256"]) == 64
