from __future__ import annotations

from scripts.build_p2_native_decision_ledger import build_ledger
from scripts.build_p2_native_rule_ir import UnitAssembler, commentary_index

from idpr.rulegen import compile_rule_ir


UNIT = "arson_of_occupied_structure"


def assembled() -> tuple[dict, dict]:
    return UnitAssembler(UNIT, None).build()


def test_only_the_gate_approved_tracks_are_compiled() -> None:
    assembler = UnitAssembler(UNIT, None)
    rule_ir, _ = assembler.build()
    assert set(assembler.tracks) == {"base", "attempt", "completed"}
    deferred = [gap for gap in rule_ir["coverage_gaps"] if gap.startswith("track_deferred")]
    assert deferred, "the deferred aggravated-result track must stay visible"


def test_a_bar_card_never_joins_the_element_it_qualifies() -> None:
    """A component may hold a defining card, a bar and a boundary at once."""
    compiled = set(UnitAssembler(UNIT, None).tracks)
    ledger = build_ledger(UNIT)
    rows = [row for row in ledger["placements"] if row["track_id"] in compiled]
    by_component: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        key = (row["track_id"], row["component_id"])
        by_component.setdefault(key, set()).add(row["role"])
    mixed = [key for key, roles in by_component.items() if len(roles) > 1]
    assert mixed, "the arson approval mixes roles on at least one element"

    rule_ir, _ = assembled()
    blocked_cards = {
        rule["norm_card_ids"][0]
        for rule in rule_ir["rules"]
        if rule["head"]["predicate"].endswith("_not_established")
    }
    component_cards = {row["card_id"] for row in rows if row["role"] == "component"}
    bar_cards = {row["card_id"] for row in rows if row["role"] in ("bar", "boundary")}
    assert blocked_cards == bar_cards
    assert not (blocked_cards & (component_cards - bar_cards))


def test_every_rule_names_the_cards_it_came_from() -> None:
    rule_ir, _ = assembled()
    for rule in rule_ir["rules"]:
        assert rule["norm_card_ids"], rule["id"]
        assert rule["source_refs"], rule["id"]


def test_the_repository_unit_compiles_to_scallop() -> None:
    rule_ir, card_set = assembled()
    program = compile_rule_ir(rule_ir, commentary_index(["art164", "art250"]), card_set)
    for track in ("base", "attempt", "completed"):
        assert f"type {UNIT}_{track}_established(" in program
    assert f"type {UNIT}_not_established(" in program


def test_role_tuple_comes_from_the_declared_signature_not_from_code() -> None:
    assembler = UnitAssembler(UNIT, None)
    assert assembler.roles[0] == "case_id"
    rule_ir, _ = assembler.build()
    roles = next(
        item for item in rule_ir["predicates"]
        if item["id"] == assembler.signature["predicate"]
    )
    assert [argument["name"] for argument in roles["arguments"]] == assembler.roles
