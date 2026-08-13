from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.article263_grounding import (
    ARTICLE263_PREDICATE_REFS,
    ARTICLE263_SHARED_RESULT_REFS,
    Article263GroundingError,
    Article263OccurrencePair,
    Article263PairAssessment,
    add_article263_truths,
    article263_request_payload,
    validate_article263_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.scallop_backend import run_article_263_liability_parity_program
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]


def _scallop_runner_module():
    path = ROOT / "scripts/run_v2_scallop_e2e.py"
    spec = importlib.util.spec_from_file_location("run_v2_scallop_e2e", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_article263_truths_are_projected_to_both_case_truth_instances() -> None:
    left = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.injury", "gocc:002")
    truths = ("TRUE", "TRUE", "FALSE")
    assessment = Article263PairAssessment(
        Article263OccurrencePair("article263-pair:0001", left, right),
        tuple(zip(ARTICLE263_PREDICATE_REFS, truths, strict=True)),
    )

    projected = add_article263_truths(CaseTruths(), (assessment,))

    assert projected.predicate == {
        (instance, ref): truth
        for instance in (left, right)
        for ref, truth in zip(ARTICLE263_PREDICATE_REFS, truths, strict=True)
    }


def test_article263_request_keeps_pair_level_relation_evidence() -> None:
    left = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.injury", "gocc:002")
    relation = "부검결과 어느 행위로 사망하였는지 판명되지 않았다."
    pair = Article263OccurrencePair(
        "article263-pair:0001", left, right, relation, 20, 20 + len(relation)
    )
    occurrences = (
        GoldOccurrence("gocc:001", "甲", "甲이 B를 때렸다.", 0, 10),
        GoldOccurrence("gocc:002", "乙", "乙이 B를 때렸다.", 11, 21),
    )

    payload = article263_request_payload(occurrences=occurrences, pairs=(pair,))

    assert payload["article263_pairs"][0]["relation_evidence"] == {
        "source_text": relation,
        "source_span": {"start": 20, "end": 20 + len(relation)},
    }
    assert payload["statutory_predicate_refs"] == list(ARTICLE263_PREDICATE_REFS)
    assert payload["shared_result_predicate_refs"] == list(ARTICLE263_SHARED_RESULT_REFS)


def test_article263_validator_separates_statutory_and_shared_result_truths() -> None:
    left = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.injury", "gocc:002")
    pair = Article263OccurrencePair("article263-pair:0001", left, right)
    raw = {
        "pair_assessments": [
            {
                "pair_id": pair.pair_id,
                "statutory_truths": [
                    {"predicate_ref": ref, "truth": "TRUE"}
                    for ref in ARTICLE263_PREDICATE_REFS
                ],
                "shared_result_truths": [
                    {"predicate_ref": "legal_element.injury_result", "truth": "TRUE"}
                ],
            }
        ]
    }

    assessment = validate_article263_output(raw, pairs=(pair,))[0]

    assert dict(assessment.truths) == {ref: "TRUE" for ref in ARTICLE263_PREDICATE_REFS}
    assert dict(assessment.shared_result_truths) == {
        "legal_element.injury_result": "TRUE"
    }


def test_scallop_runner_extracts_both_dedicated_article263_endpoints() -> None:
    runner = _scallop_runner_module()
    row = {
        "article263_assessments": [
            {
                "pair": {
                    "left_instance_key": {
                        "case_id": "case",
                        "actor_id": "甲",
                        "offense_ref": "offense.injury",
                        "occurrence_id": "gocc:001",
                    },
                    "right_instance_key": {
                        "case_id": "case",
                        "actor_id": "乙",
                        "offense_ref": "offense.injury",
                        "occurrence_id": "gocc:002",
                    },
                }
            }
        ]
    }

    instances = runner._article263_instances(row)

    assert tuple(value.actor_id for value in instances) == ("甲", "乙")


def test_pair_level_known_result_refines_occurrence_local_unknown_only() -> None:
    left = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.injury", "gocc:002")
    pair = Article263OccurrencePair("article263-pair:0001", left, right)
    base = CaseTruths(
        predicate={
            (left, "legal_element.injury_result"): "UNKNOWN",
            (right, "legal_element.injury_result"): "UNKNOWN",
        }
    )
    assessment = Article263PairAssessment(
        pair,
        tuple((ref, "TRUE") for ref in ARTICLE263_PREDICATE_REFS),
        (("legal_element.injury_result", "TRUE"),),
    )

    projected = add_article263_truths(base, (assessment,))

    assert projected.predicate[(left, "legal_element.injury_result")] == "TRUE"
    assert projected.predicate[(right, "legal_element.injury_result")] == "TRUE"


def test_pair_level_result_does_not_repair_known_truth_conflict() -> None:
    left = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.injury", "gocc:002")
    pair = Article263OccurrencePair("article263-pair:0001", left, right)
    base = CaseTruths(predicate={(left, "legal_element.injury_result"): "FALSE"})
    assessment = Article263PairAssessment(
        pair,
        tuple((ref, "TRUE") for ref in ARTICLE263_PREDICATE_REFS),
        (("legal_element.injury_result", "TRUE"),),
    )

    with pytest.raises(Article263GroundingError, match="conflicting Article 263 truth"):
        add_article263_truths(base, (assessment,))


def test_dedicated_article263_backend_scopes_case_truths_and_establishes_liability(
    tmp_path: Path,
) -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    compiled = compile_offense(registry, "offense.injury")
    assert isinstance(compiled, CompiledOffense)
    target = OffenseInstanceKey("case", "甲", "offense.injury", "gocc:001")
    unrelated = OffenseInstanceKey("case", "乙", "offense.theft", "gocc:002")
    true_refs = (
        "legal_element.natural_person_victim_status",
        "ground_fact.injury_conduct",
        "legal_element.injury_result",
        "legal_element.intent",
        *ARTICLE263_PREDICATE_REFS,
    )
    truths = CaseTruths(
        predicate={
            **{(target, ref): "TRUE" for ref in true_refs},
            (unrelated, "ground_fact.taking_conduct"): "TRUE",
        }
    )

    result = run_article_263_liability_parity_program(
        registry,
        compiled,
        target,
        truths,
        work_dir=tmp_path,
    )

    assert result.completion is not None and result.completion.state == "completed"
    assert result.elements.gate_state == "passes"
    assert result.liability_result is not None
