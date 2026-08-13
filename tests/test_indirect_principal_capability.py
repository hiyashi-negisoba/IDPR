from __future__ import annotations

from pathlib import Path

from idpr.v2.indirect_principal import has_authored_indirect_principal_capability
from idpr.v2.registry import load_definitions

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def test_kcl_indirect_principal_capability_slice_is_explicitly_authored() -> None:
    expected = {
        "offense.forcible_indecency",
        "offense.false_public_document_creation",
        "offense.private_document_forgery",
        "derived_offense.fraud",
        "offense.obstruction_of_right_exercise",
    }
    authored = {
        entry.id
        for kind in ("offense", "derived_offense")
        for entry in REGISTRY.by_kind[kind]
        if has_authored_indirect_principal_capability(REGISTRY, entry.id)
    }
    assert authored == expected


def test_capability_is_exact_offense_metadata_without_derivation_inheritance() -> None:
    assert has_authored_indirect_principal_capability(REGISTRY, "offense.forcible_indecency")
    assert not has_authored_indirect_principal_capability(REGISTRY, "offense.rape")
    assert not has_authored_indirect_principal_capability(
        REGISTRY, "derived_offense.rape_causing_intentional_injury"
    )


def test_absence_is_not_stored_as_a_negative_legal_conclusion() -> None:
    rape = REGISTRY.get("offense.rape")
    assert rape is not None
    assert "indirect_principal_capability" not in rape.payload
    assert not has_authored_indirect_principal_capability(REGISTRY, "offense.rape")
    assert not has_authored_indirect_principal_capability(REGISTRY, "card.art298")
