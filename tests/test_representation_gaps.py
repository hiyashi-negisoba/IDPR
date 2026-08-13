"""Known gaps must stay honest in both directions.

A gap recorded here and then quietly closed is as bad as one that is never recorded: the next
person reads the file, believes 폭행죄 is still missing, and works around an absence that no longer
exists. So these tests fail when a listed offense *appears*, which is the moment someone should
come back and delete the entry.
"""

from pathlib import Path

import pytest
import yaml

from idpr.v2.policy_probes import probe_requirements, unsatisfied_requirements
from idpr.v2.registry import load_definitions

GAPS = Path("data/v2/representation_gaps.yaml")


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


@pytest.fixture(scope="module")
def gaps():
    return yaml.safe_load(GAPS.read_text())["gaps"]


def test_every_unauthored_offense_family_is_still_unauthored(registry, gaps) -> None:
    for gap in gaps:
        for ref in gap.get("absent_offense_refs") or ():
            assert registry.get(ref) is None, (
                f"{ref!r} now exists -- close {gap['id']!r} in {GAPS} and revisit "
                f"whatever it was blocking"
            )


def test_the_assault_and_stolen_property_families_are_both_recorded(gaps) -> None:
    recorded = {gap["id"] for gap in gaps}
    assert "gap.assault_offense_family" in recorded
    assert "gap.stolen_property_offense_family" in recorded


def test_the_intended_object_gap_is_still_open_and_still_unblocked_by_reinterpretation(
    registry, gaps
) -> None:
    """2026-08-13: reading Call 1.5's `factual_targets` as the intended object was refused.

    That field admits counterparts, recipients and merely-related participants, so treating it as
    "the object the actor aimed at" would have the host manufacture meaning. The gap is the honest
    answer until a narrower factual representation exists.
    """
    gap = next(item for item in gaps if item["id"] == "gap.intended_object_identity")
    assert gap["marker"] == "UNRESOLVED_MISTAKE_BINDING"

    blocked = set(gap["blocks"])
    outstanding = {
        requirement.ref
        for requirement in unsatisfied_requirements(
            registry,
            available_refs=_supplied_refs(registry),
        )
        if requirement.policy_id in blocked
    }
    assert "relation.intended_object_divergence" in outstanding


def _supplied_refs(registry) -> set[str]:
    """Everything except the divergence relation, which is exactly what the gap withholds."""
    return {
        requirement.ref
        for requirement in probe_requirements(registry)
        if requirement.ref != "relation.intended_object_divergence"
    }


def test_every_gap_names_a_typed_marker(gaps) -> None:
    """A gap without a marker degrades into silence at runtime."""
    for gap in gaps:
        assert gap.get("marker"), f"{gap['id']} has no typed marker"
        assert gap.get("summary"), f"{gap['id']} has no summary"
