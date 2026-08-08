"""build-order step 6A -- idpr.v2.runtime.pipeline: stage execution, gates, decisive obligations."""

from __future__ import annotations

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2 import relations
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.pipeline import resolve_liability
from idpr.v2.runtime.stages import (
    FormProgram,
    RelationObligation,
    SlotObligation,
    completed_program,
)
from idpr.v2.runtime.truths import CaseTruths

_ROBBERY = OffenseInstanceKey("C1", "甲", "offense.robbery", "o1")
_AGGRAVATED = OffenseInstanceKey("C1", "甲", "derived_offense.robbery_causing_injury", "o1")

_ROBBERY_REFS = (
    "ground_fact.property_taking",
    "legal_element.robbery_level_violence",
    "legal_element.appropriation_intent",
)
_AGGRAVATED_REFS = _ROBBERY_REFS + (
    "ground_fact.injury_occurred",
    "legal_element.aggravated_result_attribution",
)


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, []).append(
        DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>")
    )
    by_id: dict[str, DefinitionEntry] = {}
    frozen = {}
    for k, entries in by_kind.items():
        frozen[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen)


def _doctrine(registry, doctrine_id, stage, effect, ref, modifier_ref=None):
    payload = {
        "id": doctrine_id,
        "stage": stage,
        "requires": {"op": "ref", "ref": ref},
        "effect": {"effect": effect, "stage": stage},
    }
    if modifier_ref is not None:
        payload["effect"]["modifier_ref"] = modifier_ref
    return _add(registry, "doctrine", payload)


def _registry():
    registry = load_definitions()
    registry = _doctrine(registry, "doctrine.t_defense", "unlawfulness", "DEFEAT", "gf.attack")
    registry = _doctrine(registry, "doctrine.t_insanity", "culpability", "DEFEAT", "gf.insane")
    registry = _doctrine(registry, "doctrine.t_kinship", "punishability", "EXEMPT", "gf.kin")
    return registry


def _compiled(registry, ref):
    compiled = compilemod.compile_offense(registry, ref)
    assert isinstance(compiled, compilemod.CompiledOffense), compiled
    return compiled


def _truths(instance, refs, *, relation=None, **overrides) -> CaseTruths:
    predicate = {(instance, ref): TRUE for ref in refs}
    predicate.update({(instance, ref): value for ref, value in overrides.items()})
    relation_truths = {}
    if relation is not None:
        compiled = _compiled(_registry(), instance.offense_ref)
        for key, _binding in relations.iter_relation_instances(compiled):
            relation_truths[RuntimeRelationKey(instance=instance, definition_key=key)] = relation
    return CaseTruths(predicate=predicate, relation=relation_truths)


def _run(instance, truths, active=frozenset(), program=None):
    registry = _registry()
    return resolve_liability(
        registry,
        _compiled(registry, instance.offense_ref),
        instance,
        program or completed_program(),
        active,
        truths,
    )


# --------------------------------------------------------------------------------------------
# trace / conclusion separation
# --------------------------------------------------------------------------------------------


def test_failed_elements_produce_no_offense_realization_object():
    """An unrealized offense must not be described by an `OffenseRealization`.

    Making the conclusion mandatory would force `OffenseRealization(elements=failed, ...)` -- an
    object whose name asserts the opposite of its contents.
    """
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"legal_element.appropriation_intent": FALSE}),
    )

    assert evaluation.elements.legal_state == "failed"
    assert evaluation.realization is None
    assert evaluation.establishment is None
    assert evaluation.liability_result is None
    assert evaluation.decisive_stage == "elements"


def test_stages_after_the_stopping_point_are_not_reached():
    """No speculative execution past a closed gate (v2.2.0 section 24)."""
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"legal_element.appropriation_intent": FALSE}),
    )

    for stage in (evaluation.unlawfulness, evaluation.culpability, evaluation.punishability):
        assert stage.evaluation_state == "not_reached"
        assert stage.legal_state is None and stage.gate_state is None


def test_defeated_unlawfulness_keeps_no_realization_but_records_the_doctrine():
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"gf.attack": TRUE}),
        active=frozenset({"doctrine.t_defense"}),
    )

    assert evaluation.elements.legal_state == "satisfied"
    assert evaluation.unlawfulness.legal_state == "defeated"
    assert evaluation.realization is None
    assert evaluation.decisive_stage == "unlawfulness"
    assert evaluation.decisive_doctrine == "doctrine.t_defense"


def test_defeated_culpability_keeps_realization_but_drops_establishment():
    """The offense WAS realized; only establishment fails. Both facts must survive."""
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"gf.insane": TRUE}),
        active=frozenset({"doctrine.t_insanity"}),
    )

    assert evaluation.realization is not None
    assert evaluation.realization.unlawfulness.legal_state == "preserved"
    assert evaluation.establishment is None
    assert evaluation.liability_result is None
    assert evaluation.decisive_stage == "culpability"


def test_exempted_punishability_keeps_establishment_but_drops_liability_result():
    """Section 4.5 separates establishment from punishability at the result level too."""
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"gf.kin": TRUE}),
        active=frozenset({"doctrine.t_kinship"}),
    )

    assert evaluation.establishment is not None
    assert evaluation.punishability.legal_state == "exempted"
    assert evaluation.liability_result is None
    assert evaluation.decisive_stage == "punishability"
    assert evaluation.decisive_doctrine == "doctrine.t_kinship"


def test_fully_successful_path_has_decisive_stage_none():
    """A path that ran to the end has no stage that decisively stopped it."""
    evaluation = _run(_ROBBERY, _truths(_ROBBERY, _ROBBERY_REFS))

    assert evaluation.liability_result is not None
    assert evaluation.liability_result.establishment is evaluation.establishment
    assert evaluation.decisive_stage is None
    assert evaluation.decisive_obligation is None


def test_form_key_is_preserved_through_evaluation_and_conclusions():
    evaluation = _run(_ROBBERY, _truths(_ROBBERY, _ROBBERY_REFS))

    assert evaluation.form_key.instance == _ROBBERY
    assert evaluation.form_key.form == "completed"
    assert evaluation.realization.form_key == evaluation.form_key
    assert evaluation.establishment.form_key == evaluation.form_key
    assert evaluation.liability_result.form_key == evaluation.form_key


# --------------------------------------------------------------------------------------------
# decisive obligation
# --------------------------------------------------------------------------------------------


def test_single_false_slot_names_itself_decisive():
    evaluation = _run(
        _ROBBERY,
        _truths(_ROBBERY, _ROBBERY_REFS, **{"legal_element.appropriation_intent": FALSE}),
    )

    assert evaluation.decisive_obligation == SlotObligation(slot="mental")


def test_several_false_obligations_name_none_but_all_stay_in_provenance():
    """No ranking is introduced to break a tie (v2.2.0 section 14)."""
    evaluation = _run(
        _ROBBERY,
        _truths(
            _ROBBERY,
            _ROBBERY_REFS,
            **{"legal_element.appropriation_intent": FALSE, "ground_fact.property_taking": FALSE},
        ),
    )

    failed = [o.obligation for o in evaluation.elements.provenance if o.truth == FALSE]
    assert evaluation.decisive_obligation is None
    assert len(failed) >= 2


def test_relation_only_failure_yields_a_relation_obligation():
    """Every predicate TRUE, the relation FALSE -- Elements fails with no FALSE leaf anywhere.

    This is why `decisive_element` was too narrow: the thing that failed is a relation obligation,
    not an element.
    """
    evaluation = _run(
        _AGGRAVATED, _truths(_AGGRAVATED, _AGGRAVATED_REFS, relation=FALSE)
    )

    assert evaluation.elements.legal_state == "failed"
    assert isinstance(evaluation.decisive_obligation, RelationObligation)
    assert (
        evaluation.decisive_obligation.key.definition_key.relation_ref == "relation.causal_nexus"
    )


def test_not_expression_failure_does_not_invent_a_predicate_obligation():
    """`NOT(A)` with `A=TRUE` is FALSE while containing no FALSE leaf.

    The decisive unit stays the slot whose expression evaluated FALSE; the pipeline never walks the
    tree looking for a "decisive leaf" that does not exist.
    """
    registry = _add(
        _registry(),
        "offense",
        {
            "id": "offense.t_negated",
            "identity": {"name": "부정 슬롯 테스트", "statutory_refs": ["n/a"]},
            "elements": {
                "conduct": {"op": "not", "arg": {"op": "ref", "ref": "ground_fact.violence_used"}}
            },
        },
    )
    instance = OffenseInstanceKey("C1", "甲", "offense.t_negated", "o1")
    evaluation = resolve_liability(
        registry,
        _compiled(registry, "offense.t_negated"),
        instance,
        completed_program(),
        frozenset(),
        CaseTruths(predicate={(instance, "ground_fact.violence_used"): TRUE}),
    )

    assert evaluation.elements.legal_state == "failed"
    assert evaluation.decisive_obligation == SlotObligation(slot="conduct")


# --------------------------------------------------------------------------------------------
# consistency with v2.1 and refusal of unimplemented forms
# --------------------------------------------------------------------------------------------


def test_elements_truth_matches_evaluate_compiled_offense():
    """Per-obligation evaluation is for naming a decisive one, not a second semantics.

    The fold must agree with v2.1's `evaluate_compiled_offense` on every combination.
    """
    registry = _registry()
    compiled = _compiled(registry, "derived_offense.robbery_causing_injury")
    expected_state = {TRUE: "satisfied", FALSE: "failed", UNKNOWN: "unresolved"}

    for intent in (TRUE, FALSE, UNKNOWN):
        for relation_truth in (TRUE, FALSE, UNKNOWN):
            truths = _truths(
                _AGGRAVATED,
                _AGGRAVATED_REFS,
                relation=relation_truth,
                **{"legal_element.appropriation_intent": intent},
            )
            reference = relations.evaluate_compiled_offense(
                compiled,
                truths.predicate_view(_AGGRAVATED),
                truths.relation_view(_AGGRAVATED),
            )
            evaluation = _run(_AGGRAVATED, truths)

            assert evaluation.elements.legal_state == expected_state[reference], (
                intent,
                relation_truth,
            )


def test_non_completed_form_program_is_rejected_until_6b():
    """A suspension the pipeline cannot honour must fail loudly, never be silently ignored."""
    truths = _truths(_ROBBERY, _ROBBERY_REFS)

    for program in (
        FormProgram(form="attempt", punishable=True),
        FormProgram(
            form="completed", punishable=True, suspended_slots=frozenset({"result"})
        ),
        FormProgram(
            form="completed", punishable=True, extra=("ref", "ground_fact.attempt_commencement")
        ),
    ):
        with pytest.raises(NotImplementedError):
            _run(_ROBBERY, truths, program=program)
