"""Contract tests for reading the legal reviewer's verdicts out of the review document.

The review document is hand-annotated legal work. Two things must hold: the parse must be
faithful (a misread annotation silently relabels an element of an offence), and the build
must never overwrite the annotations.
"""

from __future__ import annotations

import pytest

from idpr.rulebase.cards import load_card_corpus
from idpr.rulebase.review import (
    REVIEW_PATH,
    ReviewParseError,
    parse_review,
    parse_role_assignments,
    review_summary,
    verdict_map,
)
from idpr.rulebase.skeleton import (
    CONCURRENCE,
    CONTEXT,
    CORE,
    DEFEATER,
    STAGE,
    derive_skeleton,
)


@pytest.fixture(scope="module")
def corpus():
    return load_card_corpus()


@pytest.fixture(scope="module")
def verdicts(corpus):
    return parse_review(corpus=corpus)


# --------------------------------------------------------------------------- #
# Annotation grammar
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "comment,expected",
    [
        ("1번 stage, 2번 context", {1: STAGE, 2: CONTEXT}),
        ("1, 2, 3 context", {1: CONTEXT, 2: CONTEXT, 3: CONTEXT}),
        ("2, 3번은 context", {2: CONTEXT, 3: CONTEXT}),
        ("1번 core, 2번 context, 3, 4번 concurrence",
         {1: CORE, 2: CONTEXT, 3: CONCURRENCE, 4: CONCURRENCE}),
        # A typo, and a hybrid the reviewer wrote for the standard governing a defeater.
        ("1,2번 core, 3번 context, 4번 defeater, 5번 defeater-context, 6번 coree",
         {1: CORE, 2: CORE, 3: CONTEXT, 4: DEFEATER, 5: DEFEATER, 6: CORE}),
    ],
)
def test_numbered_annotations_map_cards_to_roles(comment, expected):
    assignments, whole_slot = parse_role_assignments(comment)
    assert assignments == expected
    assert whole_slot is None


@pytest.mark.parametrize(
    "comment,expected",
    [
        ("all context", CONTEXT),
        ("core", CORE),
        ("all core", CORE),
        # The verdict is stated first; the discarded alternative follows in parentheses.
        ("context (만약 수뢰죄에서 구성요건 다루는 카드가 없다면 core)", CONTEXT),
        ("core - 준강도에 대하여 한정되는 카드지?", CORE),
    ],
)
def test_unnumbered_annotations_apply_to_the_whole_slot(comment, expected):
    assignments, whole_slot = parse_role_assignments(comment)
    assert assignments == {}
    assert whole_slot == expected


def test_an_annotation_naming_no_role_is_an_error():
    with pytest.raises(ReviewParseError, match="no role found"):
        parse_role_assignments("이건 잘 모르겠어")


def test_the_eighteen_card_slot_parses_into_its_three_roles(verdicts):
    """제355조 총설 is the item that forced roles to be per-card rather than per-slot."""
    total = [v for v in verdicts if v.slot == "art355_sec4_1"]
    assert len(total) == 18
    by_role = {}
    for verdict in total:
        by_role.setdefault(verdict.role, []).append(verdict.card_index)
    assert sorted(by_role[CORE]) == [1, 2, 3, 5, 7, 9, 16]
    assert sorted(by_role[DEFEATER]) == [4, 6, 12, 15]
    assert sorted(by_role[CONTEXT]) == [8, 10, 11, 13, 14, 17, 18]


# --------------------------------------------------------------------------- #
# The finding: roles are a property of cards
# --------------------------------------------------------------------------- #


def test_the_review_split_slots_across_roles(verdicts):
    """If every slot had come back unanimous, a slot-level role would have sufficed.

    Pinned as a property because it is the reason the skeleton's slot role is a default
    rather than an answer.
    """
    summary = review_summary(verdicts)
    assert len(summary["slots_split_across_roles"]) >= 5


def test_reviewed_roles_disagree_with_the_automatic_slot_role(verdicts, corpus):
    """The queue existed because the derivation could not settle these slots.

    A queue that the reviewer merely rubber-stamped would mean the derivation already knew
    the answers and the review was wasted; this measures that it was not.
    """
    automatic = {c.slot: c.role for c in derive_skeleton(corpus)}
    changed = [v for v in verdicts if automatic[v.slot] != v.role]
    assert len(changed) / len(verdicts) > 0.3


def test_every_verdict_resolves_to_a_real_card(verdicts, corpus):
    by_id = corpus.by_id
    for verdict in verdicts:
        assert verdict.card_id in by_id
        assert by_id[verdict.card_id].slot == verdict.slot


def test_verdict_map_is_one_role_per_card(verdicts):
    mapping = verdict_map(verdicts)
    assert len(mapping) == len(verdicts), "a card was assigned two roles"


def test_qualified_verdicts_are_flagged_not_dropped(verdicts):
    """A tentative or conditional verdict is still a verdict; the qualification is
    recorded so it can be revisited rather than silently treated as certain."""
    summary = review_summary(verdicts)
    assert summary["tentative"], "the tentative annotation lost its flag"
    assert summary["questions"], "the annotation asking a question lost its flag"


# --------------------------------------------------------------------------- #
# The annotations must survive a rebuild
# --------------------------------------------------------------------------- #


def test_the_checked_in_review_document_still_carries_annotations():
    """A rebuild that regenerated the document would erase the legal review, and the
    only symptom would be this file quietly returning zero verdicts."""
    assert "> comment:" in REVIEW_PATH.read_text(encoding="utf-8")


def test_the_build_script_refuses_to_overwrite_annotations():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "build_rulebase", REVIEW_PATH.parents[2] / "scripts/build_rulebase.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module._review_is_annotated() is True
