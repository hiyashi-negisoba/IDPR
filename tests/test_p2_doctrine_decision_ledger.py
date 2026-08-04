from __future__ import annotations

from scripts.build_p2_doctrine_decision_ledger import (
    apply_override,
    build_ledger,
    override_index,
    parse_decisions,
)


def test_parser_resolves_option_number_without_guessing() -> None:
    markdown = """### 1. `art1` / `sec1` - 경쟁 학설 그룹 (group.one)

- **`card.one`**
- **`card.two`**

**선택할 카드 ID (또는 모두유지 / 모두강등):** (2)
"""
    decision = parse_decisions(markdown)[0]
    assert decision["status"] == "valid"
    assert decision["selected_card_ids"] == ["card.two"]


def test_parser_preserves_out_of_range_answer_as_invalid() -> None:
    markdown = """### 1. `art1` / `sec1` - 경쟁 학설 그룹 (group.one)

- **`card.one`**
- **`card.two`**

**선택할 카드 ID (또는 모두유지 / 모두강등):** (3)
"""
    decision = parse_decisions(markdown)[0]
    assert decision["status"] == "option_out_of_range"
    assert decision["selected_card_ids"] == []


def test_repository_ledger_preserves_all_prior_decisions() -> None:
    ledger = build_ledger()
    assert len(ledger["decisions"]) == 31
    assert ledger["stats"]["valid"] == 31
    assert "option_out_of_range" not in ledger["stats"]
    assert ledger["stats"]["reconciled_from_legacy_queue"] == 3
    assert ledger["stats"]["all_demoted"] == 1
    assert ledger["stats"]["card_catalog_issue_groups"] == 2


def test_independent_combustion_choice_is_inherited() -> None:
    ledger = build_ledger()
    decision = next(
        item for item in ledger["decisions"]
        if item["variant_group"] == "art164_sec2_1.completion"
    )
    assert decision["status"] == "valid"
    assert decision["selected_card_ids"] == [
        "art164_sec2_1.completion_independent_combustion_variant"
    ]


def test_expert_override_supersedes_selection_without_erasing_the_original() -> None:
    ledger = build_ledger()
    overridden = [item for item in ledger["decisions"] if item.get("override")]
    assert overridden, "override document declares no applied override"
    assert ledger["stats"]["expert_overrides"] == len(overridden)
    for item in overridden:
        assert item["resolution"] == "expert_override"
        assert item["status"] == "valid"
        assert item["superseded_card_ids"], "original selection must be preserved"
        assert item["selected_card_ids"] != item["superseded_card_ids"]
        assert set(item["selected_card_ids"]) <= set(item["options"])
        assert item["override"]["principle"]["principle_id"]
        assert item["override"]["ground"]


def test_override_outside_its_variant_group_is_rejected_not_applied() -> None:
    decision = {
        "options": ["card.one", "card.two"],
        "selected_card_ids": ["card.one"],
        "resolution": "selected",
        "status": "valid",
        "issue": None,
    }
    apply_override(decision, {"override_id": "x", "selected_card_ids": ["card.three"]})
    assert decision["status"] == "override_option_out_of_group"
    assert decision["selected_card_ids"] == ["card.one"]
    assert "override" not in decision


def test_every_declared_override_targets_an_existing_decision_group() -> None:
    ledger = build_ledger()
    groups = {item["variant_group"] for item in ledger["decisions"]}
    assert set(override_index()) <= groups


def test_truncated_markdown_options_recover_original_human_choice() -> None:
    ledger = build_ledger()
    selected = {
        item["variant_group"]: item["selected_card_ids"]
        for item in ledger["decisions"]
    }
    assert selected["art250_sec1_3.death_onset"] == [
        "art250_sec1_3.pulse_cessation_organ_removal"
    ]
    assert selected["art250_sec2_6.adoptee_biological_parent_offense"] == [
        "art250_sec2_6.adoption_type_determines_offense"
    ]
    assert selected["art301_sec4_6.pregnancy_injury"] == [
        "art301_sec4_6.unwanted_pregnancy_not_injury_holding"
    ]
