"""Contract tests for the fact layer and the card routing triage.

Two properties are load-bearing and neither is obvious from reading the tables:

*The fact layer's labels are closed.* A fact carrying an unlisted label can match no
rule, so accepting it would drop the fact from the reasoning while appearing to have
recorded it. That silent-drop path is why the previous rulebase could not be falsified.

*A card's ``formalization`` field does not decide where its content goes.* The routing is
derived from the proposition, and these tests pin that the two are measurably different --
if they ever coincide, the triage has stopped doing work and the simpler field should be
used instead.
"""

from __future__ import annotations

import pytest

from idpr.rulebase.cards import Card, load_card_corpus
from idpr.rulebase.facts import (
    ACT,
    ACT_CIRCUMSTANCE,
    ACT_LABELS,
    ACT_OBJECT,
    ACT_PLACE,
    ACT_TARGET,
    CAUSATION,
    FACT_PREDICATES,
    FACT_PREDICATES_BY_NAME,
    HOLDS,
    NORMATIVE_TERMS,
    OBJECT_LABELS,
    PERSON,
    PLACE_LABELS,
    PRECEDES,
    PURPOSE,
    RELATION,
    RESULT,
    RESULT_LABELS,
    ROLE,
    ROLE_LABELS,
    VOCABULARIES,
    FactLabelError,
    scl_fact_layer,
    validate_fact,
)
from idpr.rulebase.formalization import (
    CONCURRENCE_SEED,
    MODEL_ASSESS,
    NARRATIVE,
    OPEN_TEXTURE_MARKERS,
    ROUTES,
    SKELETON_META,
    STAGE_SEED,
    matched_frames,
    open_texture_markers,
    route_card,
    route_corpus,
    routing_summary,
)


@pytest.fixture(scope="module")
def corpus():
    return load_card_corpus()


@pytest.fixture(scope="module")
def routings(corpus):
    return route_corpus(corpus)


# --------------------------------------------------------------------------- #
# Fact layer
# --------------------------------------------------------------------------- #


def test_every_predicate_declares_a_name_per_argument():
    for predicate in FACT_PREDICATES:
        assert predicate.args, predicate.name
        assert predicate.arity == len(predicate.args)
        assert predicate.doc.strip()


def test_label_checked_arguments_point_at_a_real_vocabulary():
    for predicate in FACT_PREDICATES:
        indices = [index for index, _ in predicate.label_args]
        assert len(indices) == len(set(indices)), predicate.name
        for index, vocabulary_name in predicate.label_args:
            assert vocabulary_name in VOCABULARIES, predicate.name
            assert 0 <= index < predicate.arity, predicate.name


def test_every_vocabulary_is_actually_used_by_a_predicate():
    """An unused vocabulary is a label set nothing can ever carry."""
    used = {
        vocabulary_name
        for predicate in FACT_PREDICATES
        for _, vocabulary_name in predicate.label_args
    }
    assert used == set(VOCABULARIES)


def test_every_argument_of_a_fact_carries_the_case_id_first():
    """Facts are per-case; a rule that forgot the case key would join across cases."""
    for predicate in FACT_PREDICATES:
        assert predicate.args[0] == "case", predicate.name


def test_vocabularies_hold_no_duplicates():
    for name, labels in VOCABULARIES.items():
        assert len(labels) == len(set(labels)), name


def test_validate_fact_accepts_a_well_formed_fact():
    validate_fact(PERSON, ("case1", "甲"))
    validate_fact(ACT, ("case1", "a1", "甲", "해악고지"))
    validate_fact(ROLE, ("case1", "丙", "사법경찰관"))
    validate_fact(RELATION, ("case1", "B", "A", "직계혈족"))
    validate_fact(HOLDS, ("case1", "A", "동산", "소유"))
    validate_fact(CAUSATION, ("case1", "a7", "사망", "불명"))


def test_validate_fact_rejects_a_free_text_label():
    """The failure the closed vocabulary exists to prevent."""
    with pytest.raises(FactLabelError, match="ACT_LABELS"):
        validate_fact(ACT, ("case1", "a1", "甲", "협박하여 재물을 교부받음"))


def test_validate_fact_checks_every_label_argument():
    """``holds`` and ``causation`` constrain two arguments each; both must be checked."""
    with pytest.raises(FactLabelError, match="OBJECT_LABELS"):
        validate_fact(HOLDS, ("case1", "A", "타인의 재물", "소유"))
    with pytest.raises(FactLabelError, match="HOLD_LABELS"):
        validate_fact(HOLDS, ("case1", "A", "동산", "사실상 지배"))
    with pytest.raises(FactLabelError, match="CAUSATION_LABELS"):
        validate_fact(CAUSATION, ("case1", "a7", "사망", "판명되지 않음"))


@pytest.mark.parametrize(
    "vocabulary",
    [ACT_LABELS, ROLE_LABELS, OBJECT_LABELS, PLACE_LABELS, RESULT_LABELS],
)
def test_fact_labels_are_descriptive_not_normative(vocabulary):
    """The constraint the whole two-layer split rests on.

    If 폭행 or 추행 or 주거 could be a fact label, call 1 would settle the normative
    question during extraction and call 2's card assessment would be scoring a judgment
    already made -- with no reviewed proposition behind it. Facts describe; cards classify.
    """
    for label in vocabulary:
        offenders = [term for term in NORMATIVE_TERMS if term in label]
        assert not offenders, f"{label!r} contains normative term(s) {offenders}"


def test_a_conclusion_cannot_be_asserted_as_a_fact():
    """The concrete form of the rule above, at the call site."""
    for conclusion in ("추행", "기망", "절취", "횡령"):
        with pytest.raises(FactLabelError):
            validate_fact(ACT, ("case1", "a1", "甲", conclusion))
    with pytest.raises(FactLabelError):
        validate_fact(ACT_PLACE, ("case1", "a1", "주거"))
    with pytest.raises(FactLabelError):
        validate_fact(RESULT, ("case1", "상해", "A"))


def test_validate_fact_rejects_unknown_predicates_and_wrong_arity():
    with pytest.raises(FactLabelError, match="unknown fact predicate"):
        validate_fact("action_committed", ("case1", "甲"))
    with pytest.raises(FactLabelError, match="takes 4 arguments"):
        validate_fact(ACT, ("case1", "a1", "甲"))


def test_act_labels_are_statutory_verbs_not_descriptions():
    """Every act label must be short enough to be a verb stem rather than a clause."""
    assert all(len(label) <= 8 for label in ACT_LABELS)


#: The smoke case ``kcl_criminal_r10_p1_q1_ga``, encoded by hand in the fact layer.
#: Kept as a test rather than as a fixture because its purpose is to prove the
#: vocabularies are expressive enough for a real bar-exam fact pattern -- the one all
#: seven baselines were measured on. Every entry traces to a numbered sentence of the
#: fact pattern; nothing here classifies the conduct.
SMOKE_CASE_FACTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    # (1) 甲이 A로부터 신체 사진을 전송받았다
    (PERSON, ("c", "甲")),
    (PERSON, ("c", "A")),
    (PERSON, ("c", "B")),
    (PERSON, ("c", "乙")),
    (PERSON, ("c", "丙")),
    (PERSON, ("c", "丁")),
    (ROLE, ("c", "A", "피해자")),
    (ROLE, ("c", "丙", "사법경찰관")),
    (RELATION, ("c", "B", "A", "직계혈족")),
    (ACT, ("c", "a0", "甲", "물건수령")),
    (ACT_OBJECT, ("c", "a0", "사진")),
    # (2) 사진을 유포하겠다고 고지하여 A가 스스로 신체를 만지게 하였다
    (ACT, ("c", "a1", "甲", "유포고지")),
    (ACT_TARGET, ("c", "a1", "A")),
    (ACT, ("c", "a2", "A", "신체접촉")),
    (ACT_TARGET, ("c", "a2", "A")),  # actor and target coincide: 피해자를 도구로 사용
    (ACT_OBJECT, ("c", "a2", "신체")),
    (PRECEDES, ("c", "a1", "a2")),
    # (3) 아파트 1층 현관에 숨어 있다가 엘리베이터에 따라 들어가 얼굴을 때리고
    #     계단으로 끌고 가 손을 묶은 뒤 간음하려 하였으나 스스로 단념하였다
    (ACT, ("c", "a3", "甲", "은신")),
    (ACT_PLACE, ("c", "a3", "공동주택공용부")),
    (ACT, ("c", "a4", "甲", "출입")),
    (ACT_PLACE, ("c", "a4", "엘리베이터")),
    (ACT, ("c", "a5", "甲", "유형력행사")),
    (ACT_TARGET, ("c", "a5", "A")),
    (ACT, ("c", "a6", "甲", "연행")),
    (ACT_PLACE, ("c", "a6", "계단")),
    (ACT, ("c", "a7", "甲", "신체구속")),
    (ACT_TARGET, ("c", "a7", "A")),
    (ACT, ("c", "a8", "甲", "성기삽입")),
    (ACT_TARGET, ("c", "a8", "A")),
    (PURPOSE, ("c", "a8", "성관계목적")),
    (ACT_CIRCUMSTANCE, ("c", "a8", "피해자애원")),
    (ACT_CIRCUMSTANCE, ("c", "a8", "자발적중단")),
    (RESULT, ("c", "결과미발생", "A")),
    (PRECEDES, ("c", "a5", "a8")),
    # (4) 끌려가는 과정에서 발목이 골절되었다
    (RESULT, ("c", "신체손상", "A")),
    (CAUSATION, ("c", "a6", "신체손상", "확정")),
    # (5) 체포될까 두려워 도망치다가 B에게 잡히자 B를 때려눕혔다
    (ACT, ("c", "a9", "甲", "도주")),
    (PURPOSE, ("c", "a9", "체포회피목적")),
    (ACT, ("c", "a10", "甲", "유형력행사")),
    (ACT_TARGET, ("c", "a10", "B")),
    (ACT_PLACE, ("c", "a10", "노상")),
    # (6)(7) 2시간 후 乙도 B를 걷어찼고, 누구의 행위로 사망했는지 판명되지 않았다
    (ACT, ("c", "a11", "乙", "유형력행사")),
    (ACT_TARGET, ("c", "a11", "B")),
    (PRECEDES, ("c", "a10", "a11")),
    (RESULT, ("c", "사망", "B")),
    (CAUSATION, ("c", "a10", "사망", "불명")),
    (CAUSATION, ("c", "a11", "사망", "불명")),
    # (8)-(13) 丁을 통해 丙에게 4,000만 원을 전달하게 하였고 丁이 1,000만 원을 썼으며
    #          丙은 乙을 입건하지 않았다
    (HOLDS, ("c", "甲", "금전", "소유")),
    (ACT, ("c", "a12", "甲", "금전교부")),
    (ACT_TARGET, ("c", "a12", "丁")),
    (ACT_OBJECT, ("c", "a12", "금전")),
    (HOLDS, ("c", "丁", "금전", "보관")),
    (ACT, ("c", "a13", "丁", "금전사용")),
    (ACT_OBJECT, ("c", "a13", "금전")),
    (ACT, ("c", "a14", "丁", "금전교부")),
    (ACT_TARGET, ("c", "a14", "丙")),
    (ACT, ("c", "a15", "丙", "직무불이행")),
    (RESULT, ("c", "직무불수행", "丙")),
    (PRECEDES, ("c", "a12", "a14")),
)


def test_the_smoke_case_is_expressible_in_the_fact_layer():
    """Every fact of the measured bar-exam case validates against the closed vocabularies.

    This is the expressiveness check. A vocabulary that cannot state the case it will be
    run on is not a fact layer, and the failure would otherwise surface only at call 1.
    """
    for name, args in SMOKE_CASE_FACTS:
        validate_fact(name, args)


def test_the_smoke_case_encoding_classifies_nothing():
    """The encoding must not smuggle in the answers.

    The case turns on 강제추행 간접정범, 주거침입, 중지미수, 강간상해, 동시범 and 뇌물.
    None of those words may appear in the facts -- if one did, the fact layer would be
    handing call 2 its conclusion.
    """
    encoded = " ".join(arg for _, args in SMOKE_CASE_FACTS for arg in args)
    for conclusion in ("추행", "주거", "미수", "상해", "동시범", "뇌물", "협박", "강간"):
        assert conclusion not in encoded, conclusion


def test_the_smoke_case_records_undetermined_causation():
    """제263조 동시범 is the issue the baselines handled worst, and it exists only if the
    fact layer can say 'the cause was not determined' as a positive fact."""
    attributions = {
        args[3] for name, args in SMOKE_CASE_FACTS if name == CAUSATION
    }
    assert "불명" in attributions


def test_scl_fact_layer_declares_every_predicate_once():
    scl = scl_fact_layer()
    for predicate in FACT_PREDICATES:
        assert scl.count(f"type {predicate.name}(") == 1, predicate.name
        assert f"({', '.join('String' for _ in predicate.args)})" in scl


def test_predicate_index_is_complete():
    assert set(FACT_PREDICATES_BY_NAME) == {p.name for p in FACT_PREDICATES}


# --------------------------------------------------------------------------- #
# Routing
# --------------------------------------------------------------------------- #


def test_every_card_gets_exactly_one_known_route(corpus, routings):
    assert len(routings) == len(corpus.cards)
    assert {r.route for r in routings} <= set(ROUTES)


def test_open_texture_markers_are_reported_in_table_order():
    proposition = "제반 사정을 종합하여 사회통념에 따라 판단하며 인정할 수 있다."
    markers = open_texture_markers(proposition)
    assert "종합하여" in markers
    assert "사회통념" in markers
    assert list(markers) == sorted(
        markers,
        key=lambda m: [
            marker for group in OPEN_TEXTURE_MARKERS.values() for marker in group
        ].index(m),
    )


def test_a_degree_judgment_goes_to_the_model(corpus):
    """The card that no symbolic procedure can decide."""
    card = next(
        c for c in corpus.cards
        if "반항을 억압할 정도" in c.proposition
    )
    assert route_card(card).route == MODEL_ASSESS
    assert route_card(card).is_open_textured


def test_a_requirement_negation_reaches_the_skeleton_despite_a_marker(corpus):
    """``skeleton_meta`` must beat open texture: the marker sits inside the negation.

    "손해 발생 우려 … 를 요구하지 않는다" carries 우려 while asserting that the thing 우려
    names is not an element. Routing it to the model would ask for an assessment of a
    requirement that the card says does not exist.
    """
    card = next(
        c for c in corpus.cards
        if "손해 발생 우려" in c.proposition and "요구하지 않는다" in c.proposition
    )
    assert card.proposition  # guard against an empty match masking the assertion
    routed = route_card(card)
    assert routed.is_open_textured
    assert routed.route == SKELETON_META


def _synthetic_card(proposition: str) -> Card:
    return Card(
        id="artTEST.synthetic",
        article="artTEST",
        slot="artTEST",
        proposition=proposition,
        polarity="positive",
        norm_kind="element",
        formalization="deterministic_rule",
        doctrinal_status="settled",
        source_comment_ids=("c1",),
        source_quotes=("q1",),
        unit="test",
    )


def test_concurrence_beats_stage_when_both_frames_match():
    """A proposition speaking to both 기수 and 죄수 is a 죄수 rule.

    Tested on a constructed proposition rather than a corpus card, because the precedence
    is a property of the frame ordering and must hold whether or not today's corpus
    happens to contain a card that triggers both.
    """
    proposition = (
        "선행 절도가 기수에 이른다고 하더라도 그 후의 폭행은 준강도죄에 흡수되어 "
        "별개의 죄가 되지 않는다."
    )
    frames = matched_frames(proposition)
    assert CONCURRENCE_SEED in frames and STAGE_SEED in frames
    assert route_card(_synthetic_card(proposition)).route == CONCURRENCE_SEED


def test_formalization_does_not_predict_routing(routings):
    """The measurement that justifies this module existing at all.

    If ``deterministic_rule`` already meant "drives the symbolic layer", the triage would
    be redundant. Most of those cards yield no symbolic content, and many
    ``standard_input`` cards do.
    """
    deterministic = [r for r in routings if r.corpus_formalization == "deterministic_rule"]
    standard = [r for r in routings if r.corpus_formalization == "standard_input"]
    seeds = {SKELETON_META, STAGE_SEED, CONCURRENCE_SEED}

    deterministic_without_rule = [r for r in deterministic if r.route == MODEL_ASSESS]
    standard_with_rule = [r for r in standard if r.route in seeds]

    assert len(deterministic_without_rule) / len(deterministic) > 0.5
    assert len(standard_with_rule) > 100


def test_open_texture_markers_almost_never_hit_deterministic_cards(routings):
    """The detector's precision, stated as a property rather than a number.

    Markers are near-conclusive evidence of open texture; their absence proves nothing.
    This pins the first half -- if marker noise grew, the triage would start routing
    genuinely computable cards to the model.
    """
    summary = routing_summary(routings)
    by_label = summary["open_textured_by_corpus_label"]
    assert by_label["deterministic_rule"] / summary["open_textured"] < 0.05


def test_narrative_cards_carry_no_condition(corpus, routings):
    """A definition has nothing to test, so it must not become a rule or an assessment."""
    narratives = [r for r in routings if r.route == NARRATIVE]
    assert narratives
    for routing in narratives:
        proposition = corpus.by_id[routing.card_id].proposition
        assert any(
            tail in proposition
            for tail in ("범죄이다", "말한다", "뜻한다", "라 한다", "이라고 한다")
        ), routing.card_id


def test_symbolic_seeds_span_most_of_the_corpus_articles(corpus, routings):
    """A seed set concentrated in a few articles would not support the offence gate."""
    summary = routing_summary(routings)
    assert summary["symbolic_seed_articles"] / len(corpus.by_article()) > 0.8
