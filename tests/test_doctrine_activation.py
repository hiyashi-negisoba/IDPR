from __future__ import annotations
from pathlib import Path

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.doctrine_activation import raised_active_doctrines
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
INSTANCE = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")


def test_wholly_unmentioned_doctrine_is_not_activated() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    assert raised_active_doctrines(
        registry, (INSTANCE,), ("doctrine.self_defense",), CaseTruths()
    ) == ()


def test_partially_grounded_doctrine_is_routed_and_left_three_valued() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    truths = CaseTruths(
        predicate={(INSTANCE, "legal_element.infringement_situation"): "TRUE"}
    )
    assert raised_active_doctrines(
        registry, (INSTANCE,), ("doctrine.self_defense",), truths
    ) == ((INSTANCE, "doctrine.self_defense"),)


def test_explicitly_defeated_doctrine_is_not_activated() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    truths = CaseTruths(
        predicate={(INSTANCE, "legal_element.infringement_situation"): "FALSE"}
    )
    assert raised_active_doctrines(
        registry, (INSTANCE,), ("doctrine.self_defense",), truths
    ) == ()
