from __future__ import annotations

import json
from pathlib import Path

from scripts.build_p2_native_review_packets import (
    MANIFEST,
    SOURCE_DIR,
    build_queue,
    cards_for_unit,
    read_json,
    unit_definition,
)


def test_native_unit_manifest_assigns_every_p2_card_exactly_once() -> None:
    manifest = read_json(MANIFEST)
    assigned: list[str] = []
    for unit in manifest["units"]:
        assigned.extend(card["id"] for card in cards_for_unit(unit))

    source_cards = {
        card["id"]
        for path in SOURCE_DIR.glob("*_unit.json")
        for card in json.loads(path.read_text(encoding="utf-8"))["cards"]
    }
    assert len(assigned) == len(set(assigned))
    assert set(assigned) == source_cards


def test_review_queue_preserves_every_bounded_source_and_requires_human_fields() -> None:
    manifest = read_json(MANIFEST)
    unit = manifest["units"][0]
    queue = build_queue(manifest, unit_definition(manifest, unit["unit_id"]))
    assert queue["card_count"] == queue["unit_core_card_count"] + queue["doctrine_overlay_card_count"]
    required = set(manifest["review_contract"]["required_human_fields"])
    assert all(set(card["human"]) == required for card in queue["cards"])
    assert all(card["source_refs"] for card in queue["cards"])


def test_all_units_have_unique_ids_and_declared_source_bundles() -> None:
    manifest = read_json(MANIFEST)
    unit_ids = [unit["unit_id"] for unit in manifest["units"]]
    assert len(unit_ids) == len(set(unit_ids))
    for unit in manifest["units"]:
        assert unit["articles"]
        assert unit["source_bundles"]
        for bundle in unit["source_bundles"]:
            assert (SOURCE_DIR / f"{bundle}_unit.json").is_file()


def test_arson_packet_inherits_prior_doctrine_choices() -> None:
    manifest = read_json(MANIFEST)
    unit = unit_definition(manifest, "arson_of_occupied_structure")
    queue = build_queue(manifest, unit)
    choices = {
        item["variant_group"]: item["selected_card_ids"]
        for item in queue["inherited_doctrine_decisions"]
    }
    assert choices["art164_sec2_1.completion"] == [
        "art164_sec2_1.completion_independent_combustion_variant"
    ]
    assert choices["art250_sec2_10.arson_death_parricide_concurrence"] == [
        "art250_sec2_10.arson_death_parricide_specialty_precedent"
    ]
    overlay_ids = {
        card["card_id"] for card in queue["cards"]
        if card["source_track"] == "doctrine_overlay"
    }
    assert overlay_ids == {
        card_id
        for card_ids in choices.values()
        for card_id in card_ids
    }
