"""L0 retrieval, the call-1 contract, and the issue-recall gold.

Everything here runs on CPU with no model loaded: the dense encoder and reranker are
injected, so the invariants are testable without a GPU queue.
"""

from __future__ import annotations

import pytest

from idpr.eval.issue_recall import (
    NO_GOLD_NO_OFFENCE,
    SCORABLE,
    bucket_counts,
    crime_articles,
    gold_status,
    load_crime_map,
    load_issue_gold,
    recall,
    summarise_paths,
)
from idpr.neural.fact_graph import (
    MAX_ISSUE_CANDIDATES,
    FactGraphError,
    act_id,
    admit_fact_graph,
    fact_derived_queries,
    fact_graph_schema,
    fact_tuples,
    proposed_articles,
    quote_is_grounded,
    retrieval_queries,
    validate_fact_graph,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.facts import ACT_LABELS, VOCABULARIES
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.retrieval import (
    LexicalIndex,
    issue_index_documents,
    issue_retrieval_queries,
    reciprocal_rank_fusion,
    retrieve_candidate_articles,
    retrieve_candidate_articles_via_issues,
    retrieve_candidate_issues,
    retrieve_candidate_issues_from_cards,
    retrieve_issue_cards,
)

CASE_TEXT = (
    "甲은 A와 영상 통화를 하면서 A에게 시키는 대로 하지 않으면 신체 사진을 유포하겠다고 "
    "A를 협박하여 이에 겁을 먹은 A로 하여금 가슴과 음부를 스스로 만지게 하였다. "
    "그 후 甲은 A가 거주하는 아파트 1층 현관 부근에 숨어 있다가 귀가하는 A를 발견하고 "
    "주먹으로 A의 얼굴을 2회 때려 발목이 골절되는 상해를 입혔다."
)


def _payload(**overrides):
    payload = {
        "version": "2.0.0",
        "case_id": "case_x",
        "entities": [
            {"entity_id": "gap", "mentions": ["甲"]},
            {"entity_id": "a", "mentions": ["A"]},
        ],
        "acts": [
            {
                "actor": "gap",
                "act_label": "해악고지",
                "source_quote": "신체 사진을 유포하겠다고",
                "epistemic_status": "given",
                "targets": ["a"],
                "objects": ["사진"],
            },
            {
                "actor": "gap",
                "act_label": "유형력행사",
                "source_quote": "주먹으로 A의 얼굴을 2회 때려",
                "epistemic_status": "given",
                "targets": ["a"],
                "place": "공동주택공용부",
                "circumstances": ["단독"],
                "after": 0,
            },
        ],
        "results": [
            {
                "result_label": "신체손상",
                "entity": "a",
                "source_quote": "발목이 골절되는 상해를 입혔다",
                "epistemic_status": "given",
                "causation": [{"act": 1, "attribution": "확정"}],
            }
        ],
        "roles": [
            {"entity": "a", "role_label": "피해자", "source_quote": "A를 협박하여"}
        ],
        "relations": [],
        "holdings": [],
        "issue_candidates": [
            {
                "label": "강제추행",
                "article": "제298조",
                "source_quote": "가슴과 음부를 스스로 만지게 하였다",
            }
        ],
        "retrieval_queries": ["협박에 의한 추행", "주거침입의 위요지"],
        "unresolved_questions": [],
    }
    payload.update(overrides)
    return payload


# --------------------------------------------------------------------------- #
# Call 1 schema
# --------------------------------------------------------------------------- #


def test_the_model_never_mints_an_identifier():
    """The regression that broke 52 of 61 questions on the first run.

    Dangling act references and duplicate ids are impossible when the only cross-reference
    the model can emit is an array index the schema bounds.
    """
    schema = fact_graph_schema()
    act = schema["properties"]["acts"]["items"]["properties"]
    assert "act_id" not in act and "actId" not in act
    assert act["after"]["type"] == "integer"
    result = schema["properties"]["results"]["items"]["properties"]
    assert result["causation"]["items"]["properties"]["act"]["type"] == "integer"


def test_label_fields_are_closed_to_their_vocabulary():
    """Guided decoding must make an unlisted label impossible, not merely detectable."""
    schema = fact_graph_schema()
    act = schema["properties"]["acts"]["items"]["properties"]
    assert act["act_label"]["enum"] == list(VOCABULARIES["ACT_LABELS"])
    assert act["place"]["enum"] == list(VOCABULARIES["PLACE_LABELS"])
    assert act["objects"]["items"]["enum"] == list(VOCABULARIES["OBJECT_LABELS"])
    assert act["purposes"]["items"]["enum"] == list(VOCABULARIES["PURPOSE_LABELS"])
    holding = schema["properties"]["holdings"]["items"]["properties"]
    assert holding["hold_label"]["enum"] == list(VOCABULARIES["HOLD_LABELS"])


def test_every_independently_asserted_group_carries_a_quote():
    """Attributes ride on their act's quote; independent assertions carry their own."""
    schema = fact_graph_schema()["properties"]
    for group in ("acts", "results", "roles", "relations", "holdings", "issue_candidates"):
        assert "source_quote" in schema[group]["items"]["required"], group


def test_issue_candidates_are_capped():
    """Every proposed article drags its whole card set into call 2."""
    assert fact_graph_schema()["properties"]["issue_candidates"]["maxItems"] == (
        MAX_ISSUE_CANDIDATES
    )


# --------------------------------------------------------------------------- #
# Call 1 host validation
# --------------------------------------------------------------------------- #


def test_valid_payload_passes():
    validate_fact_graph(_payload(), case_id="case_x", question_text=CASE_TEXT)


def test_source_quote_must_be_an_exact_substring():
    payload = _payload()
    payload["acts"][0]["source_quote"] = "신체 사진을 유포하겠다고 말하였다"
    with pytest.raises(FactGraphError, match="source_quote"):
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_entity_mention_must_appear_in_the_case():
    payload = _payload()
    payload["entities"].append({"entity_id": "eul", "mentions": ["乙"]})
    with pytest.raises(FactGraphError, match="mention is not in question_text"):
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_acts_must_reference_declared_entities():
    payload = _payload()
    payload["acts"][0]["targets"] = ["ghost"]
    with pytest.raises(FactGraphError, match="undeclared entity"):
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_ordering_must_point_at_a_strictly_earlier_act():
    payload = _payload()
    payload["acts"][1]["after"] = 1
    with pytest.raises(FactGraphError, match="must be the index of an earlier act"):
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_causation_must_point_at_an_existing_act():
    payload = _payload()
    payload["results"][0]["causation"] = [{"act": 7, "attribution": "확정"}]
    with pytest.raises(FactGraphError, match="out of range"):
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_errors_are_reported_together():
    """One call is one GPU round trip, so all violations come back at once."""
    payload = _payload()
    payload["acts"][0]["source_quote"] = "없는 인용"
    payload["roles"][0]["entity"] = "ghost"
    with pytest.raises(FactGraphError) as raised:
        validate_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)
    assert len(raised.value.errors) == 2


# --------------------------------------------------------------------------- #
# Call 1 admission
# --------------------------------------------------------------------------- #


def test_whitespace_is_the_only_normalisation_when_matching_a_quote():
    """Spacing varies in the source; characters do not get to."""
    assert quote_is_grounded("주먹으로 A의 얼굴을 2회 때려", CASE_TEXT)
    assert quote_is_grounded("주먹으로A의얼굴을2회때려", CASE_TEXT)
    assert not quote_is_grounded("주먹으로 B의 얼굴을 2회 때려", CASE_TEXT)


def test_one_bad_item_costs_that_item_and_not_the_case():
    """The failure that lost 57 of 61 questions: whole-payload rejection.

    An ungrounded fact still never reaches the symbolic layer -- it is refused. What
    changes is that refusing it no longer discards the other twenty-nine grounded ones.
    """
    payload = _payload()
    payload["roles"][0]["source_quote"] = "원문에 없는 인용"
    admission = admit_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)
    assert admission.payload["roles"] == []
    assert admission.dropped == {"roles": 1}
    assert len(admission.payload["acts"]) == 2


def test_dropping_an_act_remaps_the_references_that_point_past_it():
    """Indices are positional, so a dropped act must not silently re-point the rest."""
    payload = _payload()
    payload["acts"][0]["source_quote"] = "원문에 없는 인용"
    admission = admit_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)
    acts = admission.payload["acts"]
    assert len(acts) == 1 and acts[0]["act_label"] == "유형력행사"
    # ``after`` pointed at the dropped act, so the ordering edge goes rather than dangle.
    assert "after" not in acts[0]
    # Causation pointed at index 1, which is now index 0.
    assert admission.payload["results"][0]["causation"] == [
        {"act": 0, "attribution": "확정"}
    ]


def test_self_referential_ordering_is_dropped_not_fatal():
    """61 of 742 uses read ``after`` as the act's own id."""
    payload = _payload()
    payload["acts"][1]["after"] = 1
    admission = admit_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)
    assert "after" not in admission.payload["acts"][1]
    assert admission.dropped == {"act_ordering": 1}


def test_a_payload_for_another_case_is_refused_outright():
    with pytest.raises(FactGraphError, match="does not match"):
        admit_fact_graph(_payload(), case_id="other", question_text=CASE_TEXT)


def test_a_mostly_ungrounded_payload_is_refused():
    """Partial imperfection is admitted; a failed extraction is not."""
    payload = _payload()
    for act in payload["acts"]:
        act["source_quote"] = "원문에 없는 인용"
    with pytest.raises(FactGraphError, match="grounded"):
        admit_fact_graph(payload, case_id="case_x", question_text=CASE_TEXT)


def test_admitted_payloads_produce_valid_fact_tuples():
    admission = admit_fact_graph(_payload(), case_id="case_x", question_text=CASE_TEXT)
    rows = fact_tuples(admission.payload, case_id="case_x")
    assert ("precedes", ("case_x", "act_001", "act_002")) in rows


# --------------------------------------------------------------------------- #
# Call 1 accessors
# --------------------------------------------------------------------------- #


def test_fact_tuples_emit_the_fact_layer_relations():
    rows = fact_tuples(_payload(), case_id="case_x")
    emitted = {name for name, _ in rows}
    assert {"person", "role", "act", "act_target", "act_place", "result", "causation"} <= emitted
    assert ("act", ("case_x", "act_001", "gap", "해악고지")) in rows
    assert ("precedes", ("case_x", "act_001", "act_002")) in rows
    assert ("causation", ("case_x", "act_002", "신체손상", "확정")) in rows
    assert all(arguments[0] == "case_x" for _, arguments in rows)


def test_act_ids_are_assigned_by_position():
    assert act_id(0) == "act_001"
    assert act_id(11) == "act_012"


def test_normative_labels_cannot_reach_the_fact_layer():
    """협박 is a card's conclusion, never a fact -- and the vocabulary is the guard."""
    assert "협박" not in ACT_LABELS
    payload = _payload()
    payload["acts"][0]["act_label"] = "협박"
    with pytest.raises(Exception, match="not in ACT_LABELS"):
        fact_tuples(payload, case_id="case_x")


def test_query_coverage_follows_the_case_not_the_model_budget():
    """Every asserted event contributes a query, however many the model chose to write.

    The smoke case is why: an eight-act narrative got five model queries, two of them on a
    paragraph the sub-question does not ask about, and the intrusion episode got none --
    so its article was missed although ``출입 @ 공동주택공용부`` had been extracted.
    """
    payload = _payload()
    derived = fact_derived_queries(payload)
    assert len(derived) >= len(payload["acts"])
    assert any("공동주택공용부" in query for query in derived)
    # Attributes are concatenated as they appear; no label is special-cased.
    assert "유형력행사 공동주택공용부 단독" in derived


def test_retrieval_queries_include_candidate_labels():
    """A candidate the model can name but not number still needs to reach its article."""
    queries = retrieval_queries(_payload())
    assert "강제추행" in queries
    assert "협박에 의한 추행" in queries


def test_proposed_articles_normalise_statute_labels():
    assert proposed_articles(_payload()) == ["art298"]


# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #


def test_rrf_rewards_agreement():
    fused = reciprocal_rank_fusion([[1, 0, 2], [1, 2, 0]])
    assert max(fused, key=lambda index: fused[index]) == 1


def test_rrf_ignores_documents_absent_from_a_ranking():
    fused = reciprocal_rank_fusion([[0], [0, 1]])
    assert set(fused) == {0, 1}
    assert fused[0] > fused[1]


def test_multi_query_beats_one_concatenated_query():
    """The regression that the first Phase 2 attempt failed.

    A case narrating two unrelated offences in two paragraphs must not have the
    second-paragraph article averaged away by the first. Concatenating the paragraphs into
    one query does exactly that; ranking them separately and fusing by max does not.
    """
    corpus = card_corpus()
    paragraphs = ["타인의 재물을 절취하였다", "현주건조물에 불을 놓아 소훼하였다"]
    split = retrieve_candidate_articles(paragraphs, corpus=corpus, top_k_articles=8)
    joined = retrieve_candidate_articles(
        [" ".join(paragraphs)], corpus=corpus, top_k_articles=8
    )
    assert split.articles != joined.articles
    assert "art164" in split.articles


def test_selected_articles_keep_every_card():
    """The load-bearing invariant: the gate only blocks on cards it was given."""
    corpus = card_corpus()
    result = retrieve_candidate_articles(
        ["재물을 절취하였다"], corpus=corpus, top_k_articles=5
    )
    by_article = corpus.by_article()
    expected = sum(len(by_article[article]) for article in result.articles)
    assert len(result.cards) == expected
    assert {card.article for card in result.cards} == set(result.articles)


def test_proposals_are_unioned_and_kept_distinguishable():
    corpus = card_corpus()
    result = retrieve_candidate_articles(
        ["재물을 절취하였다"], corpus=corpus, top_k_articles=3, proposed=["art164"]
    )
    assert "art164" in result.articles
    assert result.provenance()["art164"] in {"proposed", "both"}
    assert set(result.retrieved) <= set(result.articles)


def test_lexical_index_scores_the_matching_card_higher():
    index = LexicalIndex.build(["타인의 재물을 절취한 경우", "불을 놓아 건조물을 소훼한 경우"])
    scores = index.scores("재물을 절취")
    assert scores[0] > scores[1]


def test_issue_retrieval_never_crosses_the_parent_or_reloads_anchors():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue = next(item for item in issues if item.issue_id == "art319.Ⅲ.element_issue")
    facts = [
        {
            "fact_id": "fact_1",
            "kind": "act",
            "assertion": {
                "act_label": "출입",
                "place": "공동주택공용부",
                "source_quote": "아파트 1층 현관 부근에 숨어 있다가",
            },
        }
    ]
    result = retrieve_issue_cards([issue], facts, corpus=corpus, top_k_per_issue=3)
    selected = result.results[0]
    assert selected.card_ids
    assert len(selected.card_ids) <= 3
    assert set(selected.card_ids) <= set(issue.retrieval_card_ids)
    assert not set(selected.card_ids) & set(issue.anchor_card_ids)
    assert {card.article for card in selected.cards} == {"art319"}


def test_l0_issue_documents_contain_only_titles_and_anchor_rules():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    indexed, documents = issue_index_documents(issues, corpus=corpus)
    assert indexed
    assert len(indexed) == len(documents)
    for issue, document in zip(indexed, documents):
        assert issue.offense in document
        assert issue.title in document
        assert all(
            corpus.by_id[card_id].proposition in document
            for card_id in issue.anchor_card_ids
        )
        assert not set(issue.case_pattern_card_ids) & set(issue.anchor_card_ids)


def test_l0_issue_retrieval_projects_ranked_issues_to_unique_articles():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    indexed, documents = issue_index_documents(issues, corpus=corpus)
    result = retrieve_candidate_issues(
        ["타인의 재물을 절취하였다"],
        corpus=corpus,
        issues=indexed,
        top_k_issues=8,
        lexical=LexicalIndex.build(documents),
        proposed=["art298"],
    )
    assert len(result.retrieved_issue_ids) == 8
    assert len(result.retrieved_articles) <= 8
    assert result.articles[-1] == "art298"
    assert set(result.retrieved_articles) <= {issue.article for issue in indexed}


def test_l0_issue_retrieval_rejects_invalid_k():
    corpus = card_corpus()
    with pytest.raises(ValueError, match="top_k_issues"):
        retrieve_candidate_issues(["절도"], corpus=corpus, top_k_issues=0)


def test_card_search_hits_are_projected_to_issues_not_returned_as_cards():
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    result = retrieve_candidate_issues_from_cards(
        ["타인의 재물을 절취하였다"],
        corpus=corpus,
        issues=issues,
        top_k_issues=8,
    )
    assert len(result.retrieved_issue_ids) == 8
    assert all(issue_id in {issue.issue_id for issue in issues} for issue_id in result.retrieved_issue_ids)
    assert not hasattr(result, "cards")


def test_hierarchical_article_ranking_matches_legacy_max_card_ranking():
    corpus = card_corpus()
    documents = [card.proposition for card in corpus.cards]
    lexical = LexicalIndex.build(documents)
    queries = ["타인의 재물을 절취하였다", "아파트 공동현관에 들어갔다"]
    legacy = retrieve_candidate_articles(
        queries,
        corpus=corpus,
        top_k_articles=12,
        lexical=lexical,
    )
    hierarchical = retrieve_candidate_articles_via_issues(
        queries,
        corpus=corpus,
        top_k_articles=12,
        lexical=lexical,
    )
    assert hierarchical.retrieved_articles == legacy.retrieved


def test_issue_queries_keep_facts_separate_and_prefer_missing_fact_focus():
    issues, _ = compile_issue_catalog_v2()
    issue = next(item for item in issues if item.issue_id == "art319.Ⅲ.element_issue")
    facts = [
        {"assertion": {"source_quote": "공동현관에 들어갔다"}},
        {"assertion": {"source_quote": "피해자를 폭행하였다"}},
    ]
    queries = issue_retrieval_queries(
        issue, facts, focus_texts=["공동현관의 출입통제 상태"]
    )
    assert len(queries) == 1
    assert "공동현관의 출입통제 상태" in queries[0]
    assert "공동현관에 들어갔다" in queries[0]
    assert all("피해자를 폭행하였다" not in query for query in queries)


# --------------------------------------------------------------------------- #
# Issue-recall gold
# --------------------------------------------------------------------------- #


def test_every_rubric_crime_name_is_in_the_map():
    """A crime name with no entry would silently drop that question's gold."""
    crime_map = load_crime_map()
    gold = load_issue_gold()
    unknown = {
        crime
        for item in gold.values()
        for crime in item.crimes
        if crime not in crime_map["crimes"]
    }
    assert unknown == set()


def test_the_gold_is_reviewed():
    """Recall is only reportable against a signed-off 죄명 -> 조문 map.

    Pinned so that editing the map without re-reviewing it breaks the suite rather than
    quietly changing what the gate measures.
    """
    assert gold_status() == "reviewed"


def test_buckets_cover_every_question():
    gold = load_issue_gold()
    counts = bucket_counts(gold)
    assert sum(counts.values()) == len(gold) == 61
    assert counts[SCORABLE] >= 29


def test_questions_naming_no_offence_are_not_scored_as_misses():
    """Procedural questions have no substantive article by construction."""
    gold = load_issue_gold()
    without = [item for item in gold.values() if item.bucket == NO_GOLD_NO_OFFENCE]
    assert without
    assert all(recall(item.articles, ["art250"]) is None for item in without)


def test_attempt_articles_ride_along_with_the_base_offence():
    """제254조 punishes the attempt of 제250조 -- a reading of the code, not of the misses."""
    assert set(crime_articles("살인중지미수죄")) == {"art250", "art254"}
    assert set(crime_articles("살인중지미수죄", with_attempt=False)) == {"art250"}


def test_the_smoke_case_gold_matches_the_plans_checklist():
    """Verification #5 names 간접정범·위요지·중지미수 by hand; the rubric gold reproduces
    them independently, which is the cross-check that the gold is the right one."""
    gold = load_issue_gold()["kcl_criminal_r10_p1_q1_ga"]
    assert {"art298", "art319", "art300", "art297", "art301"} <= set(gold.articles)
    # 체포죄 is 제276조, outside the 51-article corpus: a coverage gap, not a gold article.
    assert "art276" not in gold.articles


def test_paths_are_summarised_separately():
    """A union number alone cannot say whether retrieval contributed anything."""
    gold = load_issue_gold()
    scorable = [item for item in gold.values() if item.bucket == SCORABLE]
    perfect = {item.sub_question_id: item.articles for item in scorable}
    empty = {item.sub_question_id: () for item in scorable}
    summary = summarise_paths(
        gold, {"retrieval": empty, "proposals": perfect, "union": perfect}
    )
    assert summary["retrieval"]["macro_recall"] == 0.0
    assert summary["proposals"]["macro_recall"] == 1.0
    assert summary["union"]["questions"] == len(scorable)
