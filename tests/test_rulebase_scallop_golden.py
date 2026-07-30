"""Run every reasoning path of the compiled rulebase through the native Scallop CLI.

These are the tests that decide whether the symbolic layer works. Everything else in this
suite checks the data going in; this checks what comes out of ``scli``.

One program is compiled per scenario and evaluated in a single invocation, because the
program declares its queries. A relation missing from the output raises rather than reading
as empty -- "the rule never ran" and "the rule concluded nothing" must not look alike.
"""

from __future__ import annotations

import pytest

from idpr.rulebase.cards import load_card_corpus
from idpr.rulebase.compile_scl import (
    QUERY_RELATIONS,
    ArticleLabelError,
    article_label,
    compile_rulebase,
)
from idpr.rulebase.golden import (
    SCENARIOS,
    GoldenSelectionError,
    Scenario,
    expected_relations,
    select_cards,
)
from idpr.rulebase.roles import resolve_card_roles
from idpr.rulebase.scallop import (
    DEFAULT_SCLI,
    ScallopError,
    StatusFactError,
    parse_query_output,
    render_card_statuses,
    run_program,
)

pytestmark = pytest.mark.skipif(
    not DEFAULT_SCLI.is_file(), reason="pinned scli binary is not present"
)


@pytest.fixture(scope="module")
def corpus():
    return load_card_corpus()


@pytest.fixture(scope="module")
def roles(corpus):
    return resolve_card_roles(corpus)


def _run(scenario: Scenario, corpus, roles, work_dir):
    statuses = list(select_cards(scenario, corpus, roles))
    if scenario.conflicting:
        statuses.append((statuses[0][0], "not_satisfied"))
    program = compile_rulebase(
        corpus,
        roles,
        absorbed_by=scenario.absorbed_by,
        imaginative_concurrence=scenario.imaginative_concurrence,
    ) + render_card_statuses(scenario.scenario_id.replace("_", "-"), statuses)
    return run_program(
        program, QUERY_RELATIONS, work_dir, name=scenario.scenario_id
    )


def _offences(results, relation: str) -> frozenset[tuple[str, ...]]:
    """Drop the leading case argument: scenarios assert on doctrine, not on the case id."""
    return frozenset(row[1:] for row in results[relation])


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda s: s.scenario_id)
def test_scenario(scenario, corpus, roles, tmp_path):
    results = _run(scenario, corpus, roles, tmp_path)
    for relation, expected in expected_relations(scenario).items():
        assert _offences(results, relation) == expected, (
            f"{scenario.scenario_id}: {relation}\n{scenario.describes}"
        )


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda s: s.scenario_id)
def test_unaddressed_elements_are_reported_but_never_block(
    scenario, corpus, roles, tmp_path
):
    """The design decision that keeps the pipeline alive.

    An exam answer never briefs every element slot of an offence, so an unargued element
    must be reported rather than treated as a failed requirement. Where a scenario
    establishes an offence, ``element_unaddressed`` is expected to be non-empty at the same
    time -- proving the gate fired *despite* unargued elements.
    """
    results = _run(scenario, corpus, roles, tmp_path)
    unaddressed = results["element_unaddressed"]
    if scenario.expects_unaddressed_elements:
        assert unaddressed, "no unaddressed element slot was reported"
        assert _offences(results, "offense_established") == frozenset(
            (off,) for off in scenario.established
        )


def test_the_contradiction_guard_fires_only_on_conflicting_statuses(
    corpus, roles, tmp_path
):
    conflicting = next(s for s in SCENARIOS if s.conflicting)
    clean = next(s for s in SCENARIOS if not s.conflicting and s.established)
    assert _run(conflicting, corpus, roles, tmp_path)["contradiction"]
    assert not _run(clean, corpus, roles, tmp_path)["contradiction"]


def test_the_scenarios_cover_every_queried_relation(corpus, roles, tmp_path):
    """A relation no scenario ever populates is a rule nobody has seen work."""
    populated: set[str] = set()
    for scenario in SCENARIOS:
        results = _run(scenario, corpus, roles, tmp_path)
        populated |= {relation for relation, rows in results.items() if rows}
    assert set(QUERY_RELATIONS) - populated == set()


# --------------------------------------------------------------------------- #
# Compiler and runtime contracts
# --------------------------------------------------------------------------- #


def test_the_compiled_program_adds_no_predicate_per_card(corpus, roles):
    """The inversion from the previous rulebase, stated as a property.

    3,487 relations for 3,487 cards was the defect. Here the relation count is fixed by
    the doctrine being modelled and does not grow with the corpus.
    """
    program = compile_rulebase(corpus, roles)
    declared_types = program.count("\ntype ")
    assert declared_types < 30, declared_types
    assert len(corpus.cards) > 1000
    # No card id may appear as a relation name.
    for card in corpus.cards[:200]:
        assert f"\ntype {card.id}" not in program
        assert f"\nrel {card.id}" not in program


def test_every_article_gets_a_statute_label(corpus):
    for article in corpus.by_article():
        label = article_label(article)
        assert label.startswith("제") and label.endswith(("조", "2"))


def test_an_underivable_article_key_raises():
    with pytest.raises(ArticleLabelError):
        article_label("art999_9_9")


def test_status_facts_reject_unsafe_input():
    with pytest.raises(StatusFactError, match="safe identifier"):
        render_card_statuses("bad id", [("x", "satisfied")])
    with pytest.raises(StatusFactError, match="not one of"):
        render_card_statuses("c1", [("x", "maybe")])
    with pytest.raises(StatusFactError, match="bare identifier"):
        render_card_statuses("c1", [('x") , ("injected', "satisfied")])


def test_requesting_an_undeclared_relation_raises(corpus, roles, tmp_path):
    program = compile_rulebase(corpus, roles)
    with pytest.raises(ScallopError, match="not declared as queries"):
        run_program(program, ["offense_established", "nonexistent"], tmp_path)


def test_a_missing_relation_in_the_output_raises_rather_than_reading_empty():
    with pytest.raises(ScallopError, match="missing from the scli output"):
        parse_query_output("other_relation: {}", "offense_established")
    assert parse_query_output("offense_established: {}", "offense_established") == ()


def test_scenario_card_selection_never_reuses_a_card(corpus, roles):
    for scenario in SCENARIOS:
        selected = select_cards(scenario, corpus, roles)
        ids = [card_id for card_id, _ in selected]
        assert len(ids) == len(set(ids)), scenario.scenario_id


def test_a_scenario_needing_an_absent_card_fails_loudly(corpus, roles):
    from idpr.rulebase.golden import CardSlot

    impossible = Scenario(
        scenario_id="impossible",
        describes="",
        cards=(CardSlot("art999", "core", "positive", "satisfied"),),
    )
    with pytest.raises(GoldenSelectionError):
        select_cards(impossible, corpus, roles)
