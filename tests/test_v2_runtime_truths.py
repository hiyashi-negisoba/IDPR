"""build-order step 6A -- idpr.v2.runtime.truths: the case/definition boundary adapter."""

from __future__ import annotations

from idpr.v2 import evaluate
from idpr.v2.expressions import canonicalize
from idpr.v2.relations import RelationInstanceKey, evaluate_relation
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.truths import CaseTruths

TRUE = evaluate.TRUE
FALSE = evaluate.FALSE
UNKNOWN = evaluate.UNKNOWN

_A = OffenseInstanceKey("C1", "甲", "offense.robbery", "o1")
_B = OffenseInstanceKey("C1", "乙", "offense.robbery", "o1")

_KEY = RelationInstanceKey(
    occurrence_path=("derived_offense.robbery_causing_injury",),
    relation_ref="relation.causal_nexus",
    left_local_key="base",
    right_local_key="agg",
)


def test_predicate_view_is_scoped_to_one_instance():
    truths = CaseTruths(
        predicate={
            (_A, "ground_fact.property_taking"): TRUE,
            (_B, "ground_fact.property_taking"): FALSE,
        }
    )

    assert truths.predicate_view(_A)["ground_fact.property_taking"] == TRUE
    assert truths.predicate_view(_B)["ground_fact.property_taking"] == FALSE


def test_predicate_view_is_what_evaluate_already_takes():
    """No v2.1 signature changes: the view goes straight into evaluate()."""
    truths = CaseTruths(predicate={(_A, "ground_fact.violence_used"): TRUE})
    expr = canonicalize({"op": "ref", "ref": "ground_fact.violence_used"})

    assert evaluate.evaluate(expr, truths.predicate_view(_A)) == TRUE
    assert evaluate.evaluate(expr, truths.predicate_view(_B)) == UNKNOWN


def test_relation_view_is_what_evaluate_relation_already_takes():
    truths = CaseTruths(
        relation={RuntimeRelationKey(instance=_A, definition_key=_KEY): TRUE}
    )

    assert evaluate_relation(_KEY, truths.relation_view(_A)) == TRUE
    assert evaluate_relation(_KEY, truths.relation_view(_B)) == UNKNOWN


def test_truths_key_is_form_independent():
    """One stored fact answers for every form of the same instance.

    Facts are keyed by OffenseInstanceKey, which has no form, so evaluating the completed and the
    attempted program of the same occurrence reads the same store rather than two parallel copies.
    """
    truths = CaseTruths(predicate={(_A, "ground_fact.injury_occurred"): FALSE})
    view = truths.predicate_view(_A)

    # Nothing in the lookup path mentions a form; the same view serves any program built for _A.
    assert view["ground_fact.injury_occurred"] == FALSE
    assert len(truths.predicate) == 1


def test_views_are_lazy_not_copies():
    """Mutating the backing store shows through -- the view holds a reference, not a snapshot."""
    backing: dict = {}
    truths = CaseTruths(predicate=backing)
    view = truths.predicate_view(_A)

    assert view.get("ground_fact.property_taking", UNKNOWN) == UNKNOWN
    backing[(_A, "ground_fact.property_taking")] = TRUE
    assert view["ground_fact.property_taking"] == TRUE


def test_view_iteration_only_yields_this_instances_keys():
    truths = CaseTruths(
        predicate={
            (_A, "ground_fact.property_taking"): TRUE,
            (_A, "ground_fact.violence_used"): TRUE,
            (_B, "ground_fact.property_taking"): TRUE,
        }
    )

    assert set(truths.predicate_view(_A)) == {
        "ground_fact.property_taking",
        "ground_fact.violence_used",
    }
    assert len(truths.predicate_view(_B)) == 1
