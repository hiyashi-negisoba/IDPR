"""build-order step 6A -- idpr.v2.runtime.identity: case-time keys and the layering they protect."""

from __future__ import annotations

import pathlib

from idpr.v2.relations import RelationInstanceKey
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey

_SRC = pathlib.Path(__file__).resolve().parents[1] / "src/idpr/v2"


def _instance(**overrides) -> OffenseInstanceKey:
    fields = dict(case_id="C1", actor_id="甲", offense_ref="offense.robbery", occurrence_id="o1")
    fields.update(overrides)
    return OffenseInstanceKey(**fields)


def test_runtime_key_embeds_definition_key_verbatim():
    """The v2.1 key is carried, not rebuilt -- runtime identity wraps definition identity."""
    definition_key = RelationInstanceKey(
        occurrence_path=("derived_offense.robbery_causing_injury", "agg"),
        relation_ref="relation.causal_nexus",
        left_local_key="base",
        right_local_key="agg",
    )
    runtime_key = RuntimeRelationKey(instance=_instance(), definition_key=definition_key)

    assert runtime_key.definition_key is definition_key
    assert runtime_key.definition_key.occurrence_path == (
        "derived_offense.robbery_causing_injury",
        "agg",
    )


def test_same_actor_same_offense_two_occurrences_stay_distinct():
    """甲 stealing from A and separately from B are two instances, not one.

    Without occurrence_id both realizations collapse to a single key and one set of facts would
    answer for both. This is upstream of 죄수론, which reasons *about* separately identified
    occurrences.
    """
    first = _instance(offense_ref="offense.embezzlement", occurrence_id="o1")
    second = _instance(offense_ref="offense.embezzlement", occurrence_id="o2")

    assert first != second
    assert len({first, second}) == 2


def test_instance_key_has_no_form_or_completion_field():
    """Guards the circularity fix AND the 7th addendum's removal of the form layer.

    Facts must be storable before any completion judgement exists, since deriving that judgement
    reads them. A completion state is concluded ABOUT an occurrence; it does not identify one, so
    it belongs in `LiabilityEvaluation.completion`, not here.
    """
    assert "form" not in OffenseInstanceKey.__dataclass_fields__
    assert set(OffenseInstanceKey.__dataclass_fields__) == {
        "case_id",
        "actor_id",
        "offense_ref",
        "occurrence_id",
    }


def test_definition_layer_never_imports_the_runtime():
    """Mechanical layering guard: idpr.v2.* must stay case-blind.

    A definition-layer module importing idpr.v2.runtime would mean case identity had leaked
    downward, which is the exact split step 6A exists to preserve.
    """
    offenders = [
        path.relative_to(_SRC).as_posix()
        for path in _SRC.rglob("*.py")
        if "runtime/" not in path.relative_to(_SRC).as_posix()
        and "idpr.v2.runtime" in path.read_text()
    ]
    assert offenders == []
