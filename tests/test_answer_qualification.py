from __future__ import annotations

from idpr.rulebase.qualification import (
    missing_required_base,
    required_base_offenses,
)


def test_reviewed_result_offenses_have_general_base_dependencies():
    dependencies = required_base_offenses()
    assert dependencies["art301"] == frozenset({"art297", "art298", "art299"})
    assert dependencies["art337"] == frozenset({"art333", "art334", "art335"})


def test_result_offense_is_qualified_by_any_gap_free_base():
    assert not missing_required_base(
        "art301", established_without_gaps={"art298"}
    )
    assert missing_required_base(
        "art337", established_without_gaps={"art334"} - {"art334"}
    ) == frozenset({"art333", "art334", "art335"})


def test_simple_offense_has_no_cross_offense_qualification():
    assert not missing_required_base("art347", established_without_gaps=set())
