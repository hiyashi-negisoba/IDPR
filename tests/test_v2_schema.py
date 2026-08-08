from __future__ import annotations

from idpr.v2.schema import build_schema_registry, load_schema_documents, schema_errors


def test_schema_registry_loads_all_thirteen_ids() -> None:
    documents = load_schema_documents()
    assert len(documents) == 13
    assert "https://schemas.idpr.local/v2/common" in documents
    assert "https://schemas.idpr.local/v2/OffenseDef" in documents
    registry = build_schema_registry()
    assert registry is not None


def test_offense_with_nested_all_tree_validates() -> None:
    payload = {
        "id": "offense.smoke_test",
        "identity": {"name": "smoke test"},
        "elements": {
            "conduct": {
                "op": "all",
                "args": [
                    {"op": "ref", "ref": "ground_fact.a"},
                    {"op": "ref", "ref": "legal_element.b"},
                ],
            }
        },
    }
    assert schema_errors("offense", payload) == []


def test_missing_required_field_reports_path() -> None:
    payload = {"id": "offense.x", "identity": {"name": "x"}}  # missing 'elements'
    errors = schema_errors("offense", payload)
    assert errors
    assert any("elements" in message for message in errors)


def test_v1_style_role_field_rejected() -> None:
    payload = {
        "id": "offense.x",
        "identity": {"name": "x"},
        "elements": {},
        "role": "bar",
    }
    errors = schema_errors("offense", payload)
    assert any("role" in message for message in errors)


def test_compose_offense_component_with_slot_rejected() -> None:
    payload = {
        "id": "derived_offense.x",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.a", "local_key": "a", "slot": "conduct"},
                {"kind": "offense", "ref": "offense.b", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.x", "left": "a", "right": "b", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    assert schema_errors("derived_offense", payload) != []


def test_compose_primitive_component_missing_slot_rejected() -> None:
    payload = {
        "id": "derived_offense.x",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.a", "local_key": "a"},
                {"kind": "primitive", "ref": "primitive.p", "local_key": "p"},
            ],
            "relations": [{"relation": "relation.x", "left": "a", "right": "p", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    assert schema_errors("derived_offense", payload) != []


def test_compose_bundle_component_missing_placement_rejected() -> None:
    payload = {
        "id": "derived_offense.x",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.a", "local_key": "a"},
                {"kind": "bundle", "ref": "bundle.b", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.x", "left": "a", "right": "b", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    assert schema_errors("derived_offense", payload) != []


def test_element_modules_entry_missing_placement_rejected() -> None:
    payload = {
        "id": "offense.x",
        "identity": {"name": "x"},
        "elements": {},
        "element_modules": [{"ref": "bundle.b"}],
    }
    assert schema_errors("offense", payload) != []


def test_element_modules_new_shape_accepted() -> None:
    payload = {
        "id": "offense.x",
        "identity": {"name": "x"},
        "elements": {},
        "element_modules": [{"ref": "bundle.b", "placement": {"ground_fact.x": "conduct"}}],
    }
    assert schema_errors("offense", payload) == []
