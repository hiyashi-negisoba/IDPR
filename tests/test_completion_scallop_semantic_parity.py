from __future__ import annotations

from pathlib import Path

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import completion_policy_for
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.scallop_backend import (
    _completion_helper_name,
    compile_completion_program,
    validate_completion_query_rows,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / 'data/v2/definitions')


def _compiled(offense_ref: str) -> CompiledOffense:
    compiled = compile_offense(REGISTRY, offense_ref)
    assert isinstance(compiled, CompiledOffense)
    return compiled


def test_compiler_emits_confirmed_blocker_semantics() -> None:
    offense_ref = 'offense.theft'
    compiled = _compiled(offense_ref)
    policy = completion_policy_for(REGISTRY, offense_ref)
    assert policy is not None
    assert policy.payload['states']['attempted'].get('blocked_when') is not None

    lines = compile_completion_program(REGISTRY, [compiled]).program.splitlines()
    candidate = _completion_helper_name('candidate', offense_ref, 'attempted')
    true_lines = [line for line in lines if line.startswith(f'rel {candidate}_true(')]
    false_lines = [line for line in lines if line.startswith(f'rel {candidate}_false(')]
    unknown_lines = [line for line in lines if line.startswith(f'rel {candidate}_unknown(')]

    assert len(true_lines) == 1 and ' and not ' in true_lines[0]
    assert len(false_lines) == 2
    assert len(unknown_lines) == 1 and ' and not ' in unknown_lines[0]


def test_compiler_emits_authored_defeated_by_state_yield() -> None:
    offense_ref = 'offense.homicide'
    compiled = _compiled(offense_ref)
    policy = completion_policy_for(REGISTRY, offense_ref)
    assert policy is not None
    states = policy.payload['states']
    assert 'abandoned_attempt' in (states['attempted'].get('defeated_by_state') or ())

    lines = compile_completion_program(REGISTRY, [compiled]).program.splitlines()
    attempted = _completion_helper_name('candidate', offense_ref, 'attempted')
    abandoned = _completion_helper_name('candidate', offense_ref, 'abandoned_attempt')
    surviving = _completion_helper_name('surviving', offense_ref, 'attempted')
    rule = next(line for line in lines if line.startswith(f'rel {surviving}('))

    assert f'{attempted}_true(c, a, i)' in rule
    assert f'not {abandoned}_true(c, a, i)' in rule


def test_validator_uses_authored_yield_semantics() -> None:
    offense_ref = 'offense.homicide'
    compiled = _compiled(offense_ref)
    policy = completion_policy_for(REGISTRY, offense_ref)
    assert policy is not None
    states = policy.payload['states']
    target = OffenseInstanceKey('case', 'actor', offense_ref, 'occurrence')
    fields = ('case', 'actor', offense_ref, 'occurrence')

    truth_by_state = {name: 'FALSE' for name in states}
    truth_by_state['attempted'] = 'TRUE'
    truth_by_state['abandoned_attempt'] = 'TRUE'
    candidate_rows = [(*fields, name, truth_by_state[name]) for name in states]

    selected = 'abandoned_attempt'
    label = 'TRUE' if states[selected]['punishable'] else 'FALSE'
    result_rows = [(*fields, selected, label)]
    element_rows = [(*fields, 'TRUE')] if label == 'TRUE' else []

    _, results, _ = validate_completion_query_rows(
        candidate_rows,
        result_rows,
        element_rows,
        registry=REGISTRY,
        compiled_offenses=[compiled],
        targets=[target],
    )
    assert results[target] == (selected, label)
