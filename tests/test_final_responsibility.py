"""최종 책임 뷰. 인스턴스별 liability chain이 끝난 뒤 한 번 도는 심볼릭 단계."""

from pathlib import Path

import pytest
import yaml

from idpr.v2.evaluate import TRUE
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.concurrence import APPROVED, load_concurrence_rules
from idpr.v2.runtime.excess import (
    LIABLE_FOR_INSTIGATED_SCOPE,
    QUANTITATIVE_ORDINARY,
    UNRESOLVED_EXCESS_RELATION,
)
from idpr.v2.runtime.final_responsibility import (
    MULTIPLE_EXCESS_CANDIDATES,
    UNRESOLVED_EXCESS_EPISODE_SCOPE,
    UNRESOLVED_STATUS_REDIRECTION_TARGET,
    excess_parity_rows,
    plan_status_redirections,
    resolve_final_responsibility,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import (
    LiabilityEvaluation,
    OffenseEstablishment,
    OffenseRealization,
    not_reached,
)
from idpr.v2.runtime.truths import CaseTruths

CASE = "case"
ASCENDANT_STATUS = "legal_element.lineal_ascendant_of_self_or_spouse_status"


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def _instance(offense: str, occurrence: str, actor: str = "甲") -> OffenseInstanceKey:
    return OffenseInstanceKey(CASE, actor, offense, occurrence)


def _established(instance: OffenseInstanceKey) -> LiabilityEvaluation:
    """성립까지 간 평가. 이 모듈이 읽는 것은 `establishment`가 있는지 뿐이다."""
    stage = not_reached()
    realization = OffenseRealization(instance=instance, elements=stage, unlawfulness=stage)
    return LiabilityEvaluation(
        instance=instance,
        completion=None,
        elements=stage,
        unlawfulness=stage,
        culpability=stage,
        punishability=stage,
        realization=realization,
        establishment=OffenseEstablishment(
            instance=instance, realization=realization, culpability=stage
        ),
    )


def _stopped(instance: OffenseInstanceKey) -> LiabilityEvaluation:
    stage = not_reached()
    return LiabilityEvaluation(
        instance=instance,
        completion=None,
        elements=stage,
        unlawfulness=stage,
        culpability=stage,
        punishability=stage,
        decisive_stage="elements",
    )


def _view(registry, *, results, provenance, links=(), truths=None, rules=()):
    return resolve_final_responsibility(
        registry,
        case_id=CASE,
        results=results,
        episode_by_instance={key: value[0] for key, value in provenance.items()},
        source_bindings_by_instance={key: value[1] for key, value in provenance.items()},
        derivative_links=links,
        truths=truths if truths is not None else CaseTruths(),
        concurrence_rules=rules,
    )


def test_special_theft_absorbs_the_theft_it_was_materialized_from(registry) -> None:
    theft = _instance("offense.theft", "binding:001")
    special = _instance("derived_offense.special_theft", "derived_binding:001")
    view = _view(
        registry,
        results={theft: _established(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.concurrence.absorbed_instances == frozenset({theft})
    assert view.concurrence.retained_instances == frozenset({special})
    assert len(view.specialty_candidates) == 1


def test_absorption_does_not_cross_actors_in_one_episode(registry) -> None:
    """한 episode에 甲乙丙의 절도가 모두 있을 수 있다. 甲의 특수절도가 乙의 절도를
    삼키면 안 된다."""
    theft = _instance("offense.theft", "binding:001", actor="乙")
    special = _instance("derived_offense.special_theft", "derived_binding:001", actor="甲")
    view = _view(
        registry,
        results={theft: _established(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.concurrence.absorbed_instances == frozenset()
    assert view.specialty_candidates == ()


def test_an_unestablished_offense_never_enters_the_final_view(registry) -> None:
    theft = _instance("offense.theft", "binding:001")
    special = _instance("derived_offense.special_theft", "derived_binding:001")
    view = _view(
        registry,
        results={theft: _stopped(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.established_instances == (special,)
    assert view.concurrence.absorbed_instances == frozenset()


def test_instigated_theft_realized_as_special_theft_is_quantitative_excess(registry) -> None:
    accessory = _instance("offense.theft", "binding:001", actor="甲")
    principal = _instance("derived_offense.special_theft", "binding:002", actor="乙")
    view = _view(
        registry,
        results={accessory: _established(accessory), principal: _established(principal)},
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:001", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert len(view.excess_findings) == 1
    finding = view.excess_findings[0]
    assert finding.assessment.classification == QUANTITATIVE_ORDINARY
    assert finding.assessment.effect == LIABLE_FOR_INSTIGATED_SCOPE
    rows = excess_parity_rows(view, None, foreseeability_ref="legal_element.foreseeability")
    assert [row[0] for row in rows] == [accessory]


def test_an_unauthored_offense_relation_stays_unresolved_not_qualitative(registry) -> None:
    accessory = _instance("offense.theft", "binding:001", actor="甲")
    principal = _instance("offense.dwelling_intrusion", "binding:002", actor="乙")
    view = _view(
        registry,
        results={accessory: _established(accessory), principal: _established(principal)},
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:001", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert view.excess_findings[0].assessment.classification == UNRESOLVED_EXCESS_RELATION


def test_two_realized_offenses_for_one_accessory_are_not_folded(registry) -> None:
    accessory = _instance("offense.theft", "binding:001", actor="甲")
    first = _instance("derived_offense.special_theft", "binding:002", actor="乙")
    second = _instance("offense.dwelling_intrusion", "binding:003", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            first: _established(first),
            second: _established(second),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            first: ("factual_episode:001", ()),
            second: ("factual_episode:001", ()),
        },
        links=((accessory, first, "instigator"),),
    )
    assert len(view.excess_findings) == 2
    markers = {finding.marker for finding in view.unresolved}
    assert MULTIPLE_EXCESS_CANDIDATES in markers
    # 접을 수 없으면 Scallop에도 내리지 않는다.
    assert excess_parity_rows(view, None, foreseeability_ref="x") == ()


def test_the_mistake_policy_reports_its_missing_inputs_instead_of_going_silent(registry) -> None:
    """doctrine activation 0을 몇 주 동안 못 본 이유가 이것이다. 침묵과 부적용이 같아 보였다."""
    theft = _instance("offense.theft", "binding:001")
    view = _view(
        registry,
        results={theft: _established(theft)},
        provenance={theft: ("factual_episode:001", ())},
    )
    gaps = [
        finding
        for finding in view.unresolved
        if finding.policy_id == "mistake_policy.korean_law_concrete_fact"
    ]
    assert len(gaps) == 1
    assert gaps[0].marker == "UNRESOLVED_MISTAKE_BINDING"
    assert "relation.intended_object_divergence" in gaps[0].missing_refs


def test_the_excess_provenance_inputs_are_not_reported_as_a_gap(registry) -> None:
    accessory = _instance("offense.theft", "binding:001", actor="甲")
    principal = _instance("derived_offense.special_theft", "binding:002", actor="乙")
    view = _view(
        registry,
        results={accessory: _established(accessory), principal: _established(principal)},
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:001", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    missing = {ref for finding in view.unresolved for ref in finding.missing_refs}
    assert "provenance.instigated_offense_ref" not in missing


def test_article_33_proviso_redirects_only_into_a_planned_instance(registry) -> None:
    accessory = _instance("offense.homicide", "binding:001", actor="甲")
    principal = _instance("offense.homicide", "binding:002", actor="乙")
    redirected = _instance("offense.ancestral_homicide", "binding:001", actor="甲")
    truths = CaseTruths(predicate={(accessory, ASCENDANT_STATUS): TRUE})
    links = ((accessory, principal, "instigator"),)

    applied, unresolved = plan_status_redirections(
        registry, links, truths, known_instances=(accessory, principal)
    )
    assert applied == ()
    assert [finding.marker for finding in unresolved] == [
        UNRESOLVED_STATUS_REDIRECTION_TARGET
    ]

    applied, unresolved = plan_status_redirections(
        registry, links, truths, known_instances=(accessory, principal, redirected)
    )
    assert unresolved == ()
    assert [value.accessory_instance for value in applied] == [redirected]


def test_only_approved_concurrence_rules_reach_the_runtime() -> None:
    """검수 전 규칙은 저작되어 보이되 발화하지 않는다."""
    path = Path("data/v2/concurrence_rules.yaml")
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    approved = {
        entry["rule_id"]
        for entry in document["rules"]
        if entry.get("status") == APPROVED
    }
    assert load_concurrence_rules(path, include_unapproved=True), "rule file is empty"
    assert {rule.rule_id for rule in load_concurrence_rules(path)} == approved


def test_a_realized_offense_in_another_episode_is_recorded_not_dropped(registry) -> None:
    """r11_p1_q1 형태. 교사는 앞 episode에서, 실현은 뒤 episode에서 일어난다."""
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    other = _instance("offense.injury", "binding:003", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            other: _established(other),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:004", ()),
            other: ("factual_episode:005", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert view.excess_findings == ()
    blocked = [
        finding
        for finding in view.unresolved
        if finding.marker == UNRESOLVED_EXCESS_EPISODE_SCOPE
    ]
    assert len(blocked) == 1
    assert "offense.injury" in blocked[0].detail
