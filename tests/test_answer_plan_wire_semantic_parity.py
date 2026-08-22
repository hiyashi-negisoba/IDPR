from __future__ import annotations

from pathlib import Path

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.aggravating_status import AggravatingStatusRedirection
from idpr.v2.runtime.answer_plan import (
    _COMPLETION_PROSE,
    _absorption_records,
    _pair_records,
    _redirection_records,
)
from idpr.v2.runtime.completion import DERIVABLE_STATES
from idpr.v2.runtime.concurrence import ConcurrenceResolution
from idpr.v2.runtime.final_responsibility import FinalResponsibilityView
from idpr.v2.runtime.identity import OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / 'data/v2/definitions')


def _instance(actor: str, offense_ref: str, occurrence: str) -> OffenseInstanceKey:
    return OffenseInstanceKey('case', actor, offense_ref, occurrence)


def _view() -> FinalResponsibilityView:
    injury = _instance('甲', 'offense.injury', 'occ-1')
    homicide = _instance('甲', 'offense.homicide', 'occ-1')
    base = _instance('乙', 'offense.homicide', 'occ-2')
    aggravated = _instance('乙', 'offense.ancestral_homicide', 'occ-2')
    resolution = ConcurrenceResolution(
        retained_instances=frozenset({homicide, aggravated}),
        absorbed_instances=frozenset({injury}),
        imaginative_pairs=((homicide, aggravated),),
        unresolved_candidates=(),
        rejected_conflicts=(),
        absorbed_into=((injury, homicide),),
    )
    return FinalResponsibilityView(
        case_id='case',
        established_instances=(injury, homicide, aggravated),
        concurrence=resolution,
        specialty_candidates=(),
        authored_candidates=(),
        excess_findings=(),
        excess_attributions=(),
        attribution_withheld_instances=frozenset(),
        status_redirections=(
            AggravatingStatusRedirection(
                accessory_instance=aggravated,
                base_offense_ref=base.offense_ref,
                aggravated_offense_ref=aggravated.offense_ref,
                status_ref='legal_element.lineal_descendant_status',
                mode='instigator',
            ),
        ),
        unresolved=(),
    )


def test_final_responsibility_wire_preserves_both_absorption_sides() -> None:
    wire = _view().as_dict()
    record = wire['absorbed_instances'][0]
    assert record['instance']['offense_ref'] == 'offense.injury'
    assert record['absorbed_by']['offense_ref'] == 'offense.homicide'
    projected = _absorption_records(REGISTRY, wire['absorbed_instances'])
    assert projected[0]['absorbed_offense']
    assert projected[0]['absorbing_offense']


def test_final_responsibility_pair_wire_is_directly_consumable() -> None:
    wire = _view().as_dict()
    record = wire['imaginative_concurrence_pairs'][0]
    assert set(record) == {'first_instance', 'second_instance'}
    projected = _pair_records(REGISTRY, wire['imaginative_concurrence_pairs'], None)
    assert projected[0]['first_offense']
    assert projected[0]['second_offense']


def test_article33_redirection_wire_is_directly_consumable() -> None:
    wire = _view().as_dict()
    record = wire['status_redirections'][0]
    assert record['base_offense_ref'] == 'offense.homicide'
    assert record['aggravated_offense_ref'] == 'offense.ancestral_homicide'
    projected = _redirection_records(REGISTRY, wire['status_redirections'], None)
    assert projected == [
        {
            'actor': '乙',
            'from_offense': '살인죄',
            'to_offense': '존속살해죄',
        }
    ]


def test_answer_plan_completion_vocabulary_is_exhaustive_for_derivable_states() -> None:
    assert set(_COMPLETION_PROSE) == set(DERIVABLE_STATES)
    assert _COMPLETION_PROSE['attempted'] == '미수'
    assert _COMPLETION_PROSE['abandoned_attempt'] == '중지미수'
    assert _COMPLETION_PROSE['impossible_attempt'] == '불능미수'
