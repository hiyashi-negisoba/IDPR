from __future__ import annotations

import pytest

from idpr.v2.registry import (
    EXAMPLES_DIR,
    KIND_TO_EXAMPLE_FILE,
    RegistryError,
    load_definitions,
)


def test_real_corpus_loads_43_entries_12_kinds(tmp_path) -> None:
    registry = load_definitions()
    assert len(registry.by_id) == 43
    assert len(registry.by_kind) == 12


def test_resolve_export_on_real_fixture() -> None:
    registry = load_definitions()
    assert registry.resolve_export("exported_component.injury_result") == "ground_fact.injury_occurred"


def test_duplicate_id_across_kinds_raises(tmp_path) -> None:
    for filename in KIND_TO_EXAMPLE_FILE.values():
        (tmp_path / filename).write_text((EXAMPLES_DIR / filename).read_text())
    # Inject a duplicate: reuse ground_fact.property_taking's id as a legal_element too.
    legal_elements_path = tmp_path / KIND_TO_EXAMPLE_FILE["legal_element"]
    text = legal_elements_path.read_text()
    text += (
        "\n- id: ground_fact.property_taking\n"
        "  arguments: []\n"
        "  canonical_meaning: \"duplicate id smoke test\"\n"
        "  legal_standard: \"n/a\"\n"
        "  authority_refs: []\n"
    )
    legal_elements_path.write_text(text)

    with pytest.raises(RegistryError, match="duplicate id"):
        load_definitions(definitions_dir=tmp_path)


def test_structurally_broken_instance_raises_with_field_path(tmp_path) -> None:
    for filename in KIND_TO_EXAMPLE_FILE.values():
        (tmp_path / filename).write_text((EXAMPLES_DIR / filename).read_text())
    offenses_path = tmp_path / KIND_TO_EXAMPLE_FILE["offense"]
    offenses_path.write_text('- id: offense.broken\n  identity:\n    name: "broken"\n')  # missing elements

    with pytest.raises(RegistryError, match="elements"):
        load_definitions(definitions_dir=tmp_path)
