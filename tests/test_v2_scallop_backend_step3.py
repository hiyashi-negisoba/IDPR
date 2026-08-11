"""Step 3 completion lowering parity tests."""

from pathlib import Path

from idpr.rulebase.scallop import run_program
from idpr.v2 import compile as compilemod
from idpr.v2 import evaluate
from idpr.v2.registry import load_definitions
from idpr.v2.runtime import completion, pipeline
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.runtime.scallop_backend import (
    COMPLETION_CANDIDATE_QUERY_RELATION,
    COMPLETION_ELEMENTS_QUERY_RELATION,
    COMPLETION_RESULT_QUERY_RELATION,
    compile_completion_program,
    render_completion_edb,
    validate_completion_query_rows,
)


def _compiled(registry, ref):
    value = compilemod.compile_offense(registry, ref)
    assert isinstance(value, compilemod.CompiledOffense)
    return value


def _run(tmp_path: Path, registry, compiled, instance, truths):
    static = compile_completion_program(registry, [compiled])
    output = run_program(
        static.program + render_completion_edb(registry, [compiled], [instance], truths),
        (COMPLETION_CANDIDATE_QUERY_RELATION, COMPLETION_RESULT_QUERY_RELATION, COMPLETION_ELEMENTS_QUERY_RELATION),
        tmp_path,
        name="step3_parity",
    )
    return validate_completion_query_rows(
        output[COMPLETION_CANDIDATE_QUERY_RELATION],
        output[COMPLETION_RESULT_QUERY_RELATION],
        output[COMPLETION_ELEMENTS_QUERY_RELATION],
        registry=registry,
        compiled_offenses=[compiled],
        targets=[instance],
    )


def test_no_policy_completed_emits_step2_equivalent_elements(tmp_path: Path):
    registry = load_definitions()
    compiled = _compiled(registry, "offense.embezzlement")
    instance = OffenseInstanceKey("C1", "actor", compiled.id, "o1")
    candidates, results, elements = _run(tmp_path, registry, compiled, instance, CaseTruths())
    assert candidates == {}
    assert results == {instance: ("completed", "TRUE")}
    assert elements[instance] == evaluate.UNKNOWN


def test_attempted_selection_and_adjusted_elements_match_python(tmp_path: Path):
    registry = load_definitions()
    compiled = _compiled(registry, "offense.injury")
    instance = OffenseInstanceKey("C1", "actor", compiled.id, "o1")
    truths = CaseTruths(predicate={
        (instance, "ground_fact.injury_occurred"): evaluate.FALSE,
        (instance, "ground_fact.attempt_commencement"): evaluate.TRUE,
        (instance, "legal_element.impossibility_without_danger"): evaluate.FALSE,
    })
    candidates, results, elements = _run(tmp_path, registry, compiled, instance, truths)
    expected_completion = completion.resolve_completion(
        completion.completion_policy_for(registry, compiled.id), compiled, instance, truths
    )
    expected = evaluate.fold_all(outcome.truth for outcome in pipeline._iter_obligations(compiled, instance, expected_completion, truths))
    assert candidates[(instance, "attempted")] == evaluate.TRUE
    assert results == {instance: ("attempted", "TRUE")}
    assert elements == {instance: expected}


def test_non_punishable_state_has_no_adjusted_elements_row(tmp_path: Path):
    registry = load_definitions()
    compiled = _compiled(registry, "offense.injury")
    instance = OffenseInstanceKey("C1", "actor", compiled.id, "o1")
    truths = CaseTruths(predicate={
        (instance, "ground_fact.injury_occurred"): evaluate.FALSE,
        (instance, "ground_fact.attempt_commencement"): evaluate.TRUE,
        (instance, "legal_element.impossibility_without_danger"): evaluate.TRUE,
    })
    _candidates, results, elements = _run(tmp_path, registry, compiled, instance, truths)
    assert results == {instance: ("impossible_attempt", "FALSE")}
    assert elements == {}


def test_component_scope_is_edb_universe_not_output_target(tmp_path: Path):
    registry = load_definitions(Path(__file__).resolve().parents[1] / "data/v2/definitions")
    compiled = _compiled(registry, "derived_offense.robbery_rape")
    instance = OffenseInstanceKey("C1", "actor", compiled.id, "o1")
    rape_instance = OffenseInstanceKey("C1", "actor", "offense.rape", "o1")
    truths = CaseTruths(predicate={
        (rape_instance, "legal_element.commencement_of_execution"): evaluate.TRUE,
        (rape_instance, "ground_fact.vaginal_intercourse_conduct"): evaluate.FALSE,
    })
    edb = render_completion_edb(registry, [compiled], [instance], truths)
    assert '"offense.rape"' in edb
    candidates, results, elements = _run(tmp_path, registry, compiled, instance, truths)
    assert candidates[(instance, "attempted")] == evaluate.TRUE
    assert results == {instance: ("attempted", "TRUE")}
    assert set(elements) == {instance}
