"""Contract tests for the live card corpus and the derived element skeleton.

These pin the two properties the symbolic layer depends on: that every reviewed card
loads with usable structural keys, and that only reviewed propositions are ever exposed
to a model.
"""

from __future__ import annotations

import json

import pytest

from idpr.rulebase.cards import (
    CardCorpusError,
    load_card_corpus,
    split_card_id,
)
from idpr.rulebase.skeleton import (
    CORE,
    ELEMENT_ROLES,
    PRESUMED,
    UNCLASSIFIED,
    classify_title,
    commentary_section_titles,
    derive_skeleton,
    example_slot_for_role,
    looks_like_parse_artifact,
    skeleton_summary,
    strip_outline_numbering,
)


@pytest.fixture(scope="module")
def corpus():
    return load_card_corpus()


@pytest.fixture(scope="module")
def skeleton(corpus):
    return derive_skeleton(corpus)


# --------------------------------------------------------------------------- #
# Card id -> (article, slot)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "card_id,expected",
    [
        # The common shape: article plus commentary section.
        ("art298_sec3_1.deception_degree", ("art298", "art298_sec3_1")),
        # Article-level slot, no section component.
        ("art225.contractual_delegate_not_official", ("art225", "art225")),
        # 제258조의2: the article token itself contains an underscore.
        ("art2582_2_sec1.group_or_multiple_force", ("art2582_2", "art2582_2_sec1")),
        # PDF-fallback provenance marker is not part of the article key.
        ("art344_x_raw_pdf.relative_scope", ("art344", "art344")),
        # Non-numeric section suffixes are preserved verbatim in the slot.
        ("art130_sec3-na.third_party_benefit", ("art130", "art130_sec3-na")),
        ("art130_sec3_가.example", ("art130", "art130_sec3_가")),
        # Fraud cards predate the artNNN convention; the leading module names the slot.
        (
            "deception.fraud.causal-link.deception-property-disposition",
            ("art347", "deception"),
        ),
    ],
)
def test_split_card_id_handles_every_observed_id_shape(card_id, expected):
    override = "art347" if not card_id.startswith("art") else None
    assert split_card_id(card_id, article_override=override) == expected


def test_nonstandard_card_id_requires_manifest_article_override():
    with pytest.raises(ValueError, match="source override"):
        split_card_id("legacy.module.card")


def test_card_sources_are_selected_by_manifest(tmp_path):
    manifest = tmp_path / "sources.json"
    manifest.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "id": "legacy-fraud-fixture",
                        "glob": "data/rulegen/fraud/fraud_core_norm_card_set.json",
                        "article_override": "art347",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    selected = load_card_corpus(manifest)
    assert selected.cards
    assert {card.article for card in selected.cards} == {"art347"}
    assert {card.unit.split("/", 1)[0] for card in selected.cards} == {"legacy-fraud-fixture"}


def test_card_source_manifest_rejects_unsafe_globs(tmp_path):
    manifest = tmp_path / "sources.json"
    manifest.write_text(
        json.dumps({"sources": [{"id": "unsafe", "glob": "../outside/*.json"}]}),
        encoding="utf-8",
    )
    with pytest.raises(CardCorpusError, match="unsafe or missing relative glob"):
        load_card_corpus(manifest)


# --------------------------------------------------------------------------- #
# Corpus
# --------------------------------------------------------------------------- #


def test_corpus_loads_every_live_card_from_all_three_sources(corpus):
    units = {card.unit.split("/", 1)[0] for card in corpus.cards}
    assert units == {"p2", "property", "fraud"}
    # The corpus is the union of the promoted units only; rejected NormCards that exist
    # solely in card_case_metadata_map.json must not appear.
    assert len(corpus.cards) == len(corpus.by_id)


def test_corpus_partitions_cleanly_by_formalization(corpus):
    standard_input = corpus.standard_input_cards()
    deterministic = corpus.deterministic_cards()
    assert len(standard_input) + len(deterministic) == len(corpus.cards)
    assert all(card.is_standard_input for card in standard_input)
    assert not any(card.is_standard_input for card in deterministic)
    # Open-textured standards dominate; that is the asset's own labelling and the
    # reason the assessment step exists at all.
    assert len(standard_input) > len(deterministic)


def test_every_card_carries_provenance(corpus):
    for card in corpus.cards:
        assert card.source_comment_ids, f"{card.id} has no comment_id"
        assert card.source_quotes, f"{card.id} has no verbatim quote"
        assert card.source_section_paths, f"{card.id} has no section_path"
        assert card.authority_basis, f"{card.id} has no authority_basis"
        assert card.review_notes, f"{card.id} has no review_notes"
        assert len(card.source_comment_ids) == len(card.source_quotes)
        assert len(card.source_comment_ids) == len(card.source_section_paths)


def test_every_card_resolves_to_an_article_and_slot(corpus):
    for card in corpus.cards:
        assert card.article.startswith("art"), card.id
        assert card.slot, card.id
        assert card.id.startswith(card.slot) or card.unit.startswith("fraud/")


def test_slots_never_straddle_two_articles(corpus):
    for slot, cards in corpus.by_slot().items():
        articles = {card.article for card in cards}
        assert len(articles) == 1, f"slot {slot} spans {articles}"


def test_cards_for_articles_filters_to_the_requested_articles(corpus):
    subset = corpus.cards_for_articles(["art298", "art319"])
    assert subset
    assert {card.article for card in subset} == {"art298", "art319"}


# --------------------------------------------------------------------------- #
# The invariant that matters most: the model sees only reviewed propositions
# --------------------------------------------------------------------------- #


def test_model_payload_exposes_only_the_reviewed_proposition(corpus):
    for card in corpus.cards[:200]:
        payload = card.model_payload()
        assert set(payload) == {"id", "proposition"}
        assert payload["proposition"] == card.proposition


def test_model_payload_never_leaks_comment_ids(corpus):
    """Quotes and their ``comment_id`` back-pointers are host-side: they back citation
    rendering and the audit trail, not model input.

    Only the identifiers are asserted absent. A proposition is a reviewed restatement of
    its own source quote, so the two legitimately share Korean phrasing -- asserting that
    no quote substring appears would fail on that overlap rather than on a real leak. The
    structural guarantee is that ``model_payload`` is built from exactly two fields,
    which :func:`test_model_payload_exposes_only_the_reviewed_proposition` pins.
    """
    for card in corpus.cards[:200]:
        serialised = repr(card.model_payload())
        for comment_id in card.source_comment_ids:
            assert comment_id not in serialised


def test_corpus_error_reports_all_defects_at_once():
    error = CardCorpusError(["first defect", "second defect"])
    assert error.errors == ["first defect", "second defect"]
    assert "first defect" in str(error)
    assert "second defect" in str(error)


# --------------------------------------------------------------------------- #
# Element skeleton
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "title,expected",
    [
        ("Ⅲ. 1. 폭행·협박", "폭행·협박"),
        ("Ⅱ. 주체 및 객체", "주체 및 객체"),
        ("1. 의의", "의의"),
        ("Ⅳ. 고의", "고의"),
        ("3. 죄수", "죄수"),
    ],
)
def test_strip_outline_numbering(title, expected):
    assert strip_outline_numbering(title) == expected


@pytest.mark.parametrize(
    "title,expected_role",
    [
        ("Ⅲ. 행위", CORE),
        ("Ⅳ. 고의", CORE),
        ("Ⅱ. 주체", PRESUMED),
        ("2. 객체", PRESUMED),
        # Longer keys win: 주관적 구성요건 and 미수범의 처벌 must not fall to
        # 구성요건 / 처벌 respectively in a way that changes the role.
        ("Ⅲ. 주관적 구성요건", CORE),
    ],
)
def test_classify_title_buckets_element_sections(title, expected_role):
    assert classify_title(title) == expected_role


def test_classify_title_returns_unclassified_for_unknown_headings():
    assert classify_title("전혀 알 수 없는 제목 xyz") == UNCLASSIFIED


@pytest.mark.parametrize(
    "title",
    [
        "(예컨대 산",
        "또는 그 배우자",
        "공무소의 보관명령으로 타인이 관리하는 자기의 물건을 은닉, 손괴한 때에는",
        "",
    ],
)
def test_parse_artifacts_are_detected(title):
    assert looks_like_parse_artifact(title)


@pytest.mark.parametrize("title", ["주체", "폭행·협박", "죄수", "주체 및 객체"])
def test_real_headings_are_not_flagged_as_artifacts(title):
    assert not looks_like_parse_artifact(title)


def test_every_card_joins_to_a_commentary_section_title(corpus):
    """The skeleton derivation rests on this join; a regression here silently
    degrades every slot role to the fallback."""
    titles = commentary_section_titles()
    unjoined = [
        card.id
        for card in corpus.cards
        if not any(titles.get(cid) for cid in card.source_comment_ids)
    ]
    assert unjoined == []


def test_skeleton_classifies_every_slot(corpus, skeleton):
    assert len(skeleton) == len(corpus.by_slot())
    assert {c.slot for c in skeleton} == set(corpus.by_slot())


def test_skeleton_review_queue_stays_small(skeleton):
    """A large queue means the title table has drifted from the corpus.

    The derivation is only worth having if it classifies most slots unaided; this
    guards the property rather than a specific count.
    """
    summary = skeleton_summary(skeleton)
    assert summary["needs_review"] / summary["slots"] < 0.20


def test_skeleton_separates_core_from_presumed(skeleton):
    """Both element kinds must be populated.

    If everything landed in one bucket the offence gate would either never fire
    (all core) or never discriminate (all presumed).
    """
    roles = skeleton_summary(skeleton)["by_role"]
    assert roles.get(CORE, 0) > 0
    assert roles.get(PRESUMED, 0) > 0
    assert set(ELEMENT_ROLES) <= set(roles)


def test_articles_without_a_core_slot_are_element_free_by_design(skeleton):
    """Only attempt provisions and the relative-property-crime exemption may lack a
    core element slot. Anything else appearing here is a skeleton gap."""
    element_free = {
        "art254",  # 살인 미수범
        "art300",  # 강간 등 미수범
        "art342",  # 미수범
        "art328",  # 친족간의 범행 특례
        "art344",  # 친족간의 범행 준용
    }
    without_core = set(skeleton_summary(skeleton)["articles_without_core_slot"])
    assert without_core <= element_free, f"unexpected gap: {without_core - element_free}"


@pytest.mark.parametrize(
    "role",
    [CORE, PRESUMED, "stage", "defeater", "concurrence", "participation", "context"],
)
def test_every_role_has_a_settled_example_slot(skeleton, role):
    """The review document explains each role by example, so each must have one.

    Examples must come from slots the derivation settled unaided: an item whose own role
    is still in question cannot demonstrate what that role means.
    """
    example = example_slot_for_role(role, skeleton)
    assert example is not None, f"no example available for {role}"
    assert example.role == role
    assert not example.needs_review


def test_example_selection_is_deterministic(skeleton):
    assert example_slot_for_role(CORE, skeleton) == example_slot_for_role(CORE, skeleton)
