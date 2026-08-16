from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import AnswerPlanError, _participation_route
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import ParticipationDependencyObligation

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / 'data/v2/definitions')


def _principal() -> OffenseInstanceKey:
    return OffenseInstanceKey('case', '乙', 'offense.theft', 'binding:principal')


def test_typed_participation_dependency_preserves_exact_principal_instance() -> None:
    principal = _principal()
    obligation = ParticipationDependencyObligation(
        mode='instigator', principal_instance=principal
    )
    wire = dataclasses.asdict(obligation)
    assert wire['mode'] == 'instigator'
    assert wire['principal_instance'] == {
        'case_id': 'case',
        'actor_id': '乙',
        'offense_ref': 'offense.theft',
        'occurrence_id': 'binding:principal',
    }


def test_answer_plan_reads_principal_identity_from_dependency_obligation() -> None:
    principal = dataclasses.asdict(_principal())
    result = {
        'elements': {
            'provenance': [
                {
                    'obligation': {
                        'mode': 'instigator',
                        'principal_instance': principal,
                    },
                    'truth': 'TRUE',
                },
                {'obligation': {'mode': 'instigator'}, 'truth': 'TRUE'},
            ]
        }
    }
    route = _participation_route(REGISTRY, result)
    assert route is not None
    assert route.mode == 'instigator'
    assert route.principal_actor == '乙'
    assert route.principal_offense == '절도죄'
    assert route.principal_realization == 'binding:principal'


def test_answer_plan_rejects_old_mode_only_derivative_provenance() -> None:
    result = {
        'elements': {
            'provenance': [
                {'obligation': {'mode': 'aider'}, 'truth': 'TRUE'},
            ]
        }
    }
    with pytest.raises(AnswerPlanError, match='missing its principal instance'):
        _participation_route(REGISTRY, result)
