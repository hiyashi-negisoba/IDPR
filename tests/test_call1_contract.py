from __future__ import annotations

import pytest

from idpr.v2.routing import (
    RouterCatalogEntry,
    RouterContractError,
    normalize_router_seeds,
    router_schema,
    validate_router_output,
)

CATALOG = (
    RouterCatalogEntry("offense.a", "A", "A offense", ()),
    RouterCatalogEntry("offense.b", "B", "B offense", ()),
)


def test_router_contract_contains_only_ranked_seed_ids() -> None:
    schema = router_schema(CATALOG)
    assert schema["required"] == ["seeds"]
    assert set(schema["properties"]) == {"seeds"}
    assert validate_router_output({"seeds": ["offense.b", "offense.a"]}, catalog=CATALOG) == (
        "offense.b",
        "offense.a",
    )


def test_router_rejects_telemetry_and_unknown_ids() -> None:
    with pytest.raises(RouterContractError):
        validate_router_output({"seeds": ["offense.a"], "confidences": [0.9]}, catalog=CATALOG)
    with pytest.raises(RouterContractError):
        validate_router_output({"seeds": ["offense.unknown"]}, catalog=CATALOG)


def test_router_normalization_is_stable_unique() -> None:
    normalized = normalize_router_seeds(("offense.b", "offense.a", "offense.b"))
    assert normalized.raw_seeds == ("offense.b", "offense.a", "offense.b")
    assert normalized.normalized_seeds == ("offense.b", "offense.a")
    assert normalized.duplicate_refs == ("offense.b",)
