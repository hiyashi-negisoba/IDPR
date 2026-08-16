from __future__ import annotations

import pytest

from idpr.v2.routing import (
    MAX_RAW_SEED_ITEMS,
    MAX_SEEDS_PER_CASE,
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

WIDE_CATALOG = tuple(
    RouterCatalogEntry(f"offense.{index:02d}", "A", f"offense {index}", ())
    for index in range(MAX_SEEDS_PER_CASE + 2)
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


def test_repeated_refs_do_not_consume_the_routing_budget() -> None:
    """The observed Call 1 failure: six of ten slots were one repeated ref.

    Under a raw-length cap that response silently cut the case's budget to
    four distinct candidates. The budget is spent on distinct refs, so a
    duplicate-heavy array stays valid and keeps room for real candidates.
    """
    seeds = ["offense.a"] + ["offense.b"] * MAX_SEEDS_PER_CASE
    assert len(seeds) > MAX_SEEDS_PER_CASE
    validated = validate_router_output({"seeds": seeds}, catalog=CATALOG)
    assert validated == tuple(seeds)
    assert normalize_router_seeds(validated).normalized_seeds == (
        "offense.a",
        "offense.b",
    )


def test_schema_bounds_the_raw_array_not_the_budget() -> None:
    seeds = router_schema(CATALOG)["properties"]["seeds"]
    assert seeds["maxItems"] == MAX_RAW_SEED_ITEMS
    assert MAX_RAW_SEED_ITEMS > MAX_SEEDS_PER_CASE
    # uniqueItems stays a generation hint; the host must not depend on it.
    assert seeds["uniqueItems"] is True


def test_router_rejects_more_distinct_refs_than_the_budget() -> None:
    ids = [entry.definition_id for entry in WIDE_CATALOG]
    with pytest.raises(RouterContractError) as excinfo:
        validate_router_output({"seeds": ids}, catalog=WIDE_CATALOG)
    assert "distinct" in str(excinfo.value)
    within = ids[:MAX_SEEDS_PER_CASE]
    assert validate_router_output({"seeds": within}, catalog=WIDE_CATALOG) == tuple(within)


def test_router_rejects_a_degenerate_unbounded_array() -> None:
    with pytest.raises(RouterContractError):
        validate_router_output(
            {"seeds": ["offense.a"] * (MAX_RAW_SEED_ITEMS + 1)}, catalog=CATALOG
        )


def test_unknown_ids_do_not_inflate_the_distinct_budget() -> None:
    """An unknown ref is already its own error and must not add a second one."""
    with pytest.raises(RouterContractError) as excinfo:
        validate_router_output(
            {"seeds": ["offense.a", "offense.unknown"]}, catalog=CATALOG
        )
    assert "distinct" not in str(excinfo.value)
