from __future__ import annotations

import os
from pathlib import Path

import pytest

from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    predicate_definitions,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    participation_request_payload,
    participation_route_targets,
    participation_schema,
    validate_participation_output,
)
from idpr.v2.runtime.relation_grounding import (
    relation_assessment_targets,
    relation_definitions,
    relation_request_payload,
    relation_schema,
    validate_relation_output,
)

ROOT = Path(__file__).resolve().parents[2]


def _run_gate(
    *,
    case_id: str,
    actor_id: str,
    occurrence_id: str,
    source: str,
    specs: tuple[tuple[str, str, str], ...],
) -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    occurrence = GoldOccurrence(occurrence_id, actor_id, source, 0, len(source))
    targets = tuple(
        AssessmentTarget(
            OffenseInstanceKey(case_id, actor_id, offense, occurrence_id),
            predicate,
        )
        for offense, predicate, _ in specs
    )
    registry = load_definitions(ROOT / "data/v2/definitions")
    predicates = predicate_definitions(registry, (predicate for _, predicate, _ in specs))
    payload = call2_request_payload(
        evidence_occurrence=occurrence, predicates=predicates, targets=targets
    )
    client = VLLMClient(base_url, model)
    raw, metadata = client.complete_json(
        system_prompt=load_prompt("v2_call2_grounding"),
        user_template=load_prompt("v2_call2_grounding_user"),
        payload=payload,
        schema_name="v2_call2_semantic_gate",
        schema=call2_schema(targets),
        max_tokens=512,
        temperature=0.0,
        seed=17,
    )
    assessments = validate_call2_output(raw, targets=targets)
    actual = tuple(value.truth for value in assessments)
    expected = tuple(expected for _, _, expected in specs)
    assert metadata.get("finish_reason") == "stop"
    assert actual == expected


def test_real_gemma_respects_occurrence_evidence_firewall() -> None:
    source = (
        "A가 엘리베이터를 타자 따라 들어가 주먹으로 A의 얼굴을 2회 때리고 5층에서 "
        "내린 다음 계단으로 끌고 가 미리 준비한 청테이프로 A의 양손을 묶어 반항을 "
        "억압한 후 A를 간음하려 하였으나 A가 그만두라고 애원하자 자신의 행동을 "
        "뉘우치고 범행을 단념하였다."
    )
    _run_gate(
        case_id="kcl_criminal_r10_p1_q1_ga",
        actor_id="甲",
        occurrence_id="gocc:002",
        source=source,
        specs=(
            ("offense.rape", "ground_fact.vaginal_intercourse_conduct", "FALSE"),
            ("offense.bribe_giving", "ground_fact.bribe_acceptance", "UNKNOWN"),
            ("offense.robbery", "ground_fact.taking_conduct", "UNKNOWN"),
            ("offense.injury", "ground_fact.injury_conduct", "TRUE"),
        ),
    )


def test_real_gemma_keeps_right_exercise_case_inside_its_factual_paragraph() -> None:
    source = (
        "한편, X시(市)에 살고 있는 甲은 자신이 단독으로 소유한 Y시(市) 소재 빌라에 "
        "거주 중인 임차인 C와 집수리 문제로 갈등이 발생하자 C를 쫓아내기로 마음먹었다. "
        "이에 甲은 乙에게 위 빌라 현관문에 자신이 구입하여 설치해 준 도어락의 비밀번호를 "
        "변경해 달라고 요청하였고, 그 사정을 알고 있던 乙은 이를 이행하였다."
    )
    _run_gate(
        case_id="kcl_criminal_r14_p1_q3",
        actor_id="甲",
        occurrence_id="gocc:001",
        source=source,
        specs=(
            ("offense.obstruction_of_right_exercise", "legal_element.own_property_object", "TRUE"),
            (
                "offense.obstruction_of_right_exercise",
                "legal_element.third_party_possession_or_right_object",
                "TRUE",
            ),
            (
                "offense.obstruction_of_right_exercise",
                "legal_element.obstruction_of_right_exercise",
                "TRUE",
            ),
            ("offense.arson_of_occupied_structure", "legal_element.burning_result", "UNKNOWN"),
            ("offense.bribe_giving", "ground_fact.bribe_acceptance", "UNKNOWN"),
        ),
    )


def test_real_gemma_grounds_fixed_relation_endpoints_from_the_same_occurrence() -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    source = (
        "甲은 A를 강간하기 위해 얼굴을 때리고 계단으로 끌고 가 양손을 묶었다. "
        "A는 그 손을 뿌리치다가 계단에서 넘어져 발목 골절상을 입었다."
    )
    occurrence = GoldOccurrence("gocc:001", "甲", source, 0, len(source))
    instance = OffenseInstanceKey(
        "relation-gate", "甲", "derived_offense.rape_causing_intentional_injury", "gocc:001"
    )
    registry = load_definitions(ROOT / "data/v2/definitions")
    targets = relation_assessment_targets(registry, (instance,))
    assert {target.key.definition_key.relation_ref for target in targets} == {
        "relation.causal_nexus",
        "relation.occasion_identity",
    }
    assert all(target.left_endpoint_ref and target.right_endpoint_ref for target in targets)
    definitions = relation_definitions(
        registry, (target.key.definition_key.relation_ref for target in targets)
    )
    raw, metadata = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call2_relation"),
        user_template=load_prompt("v2_call2_relation_user"),
        payload=relation_request_payload(
            evidence_occurrence=occurrence,
            definitions=definitions,
            targets=targets,
        ),
        schema_name="v2_call2_relation_gate",
        schema=relation_schema(targets),
        max_tokens=256,
        temperature=0.0,
        seed=17,
    )
    assessments = validate_relation_output(raw, targets=targets)
    assert metadata.get("finish_reason") == "stop"
    assert tuple(value.truth for value in assessments) == ("TRUE", "TRUE")


def test_real_gemma_binds_instigation_without_duplicate_aiding_route() -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    sources = (
        "甲은 범의가 없던 乙을 설득하여 X의 지갑을 훔치기로 결의하게 하였다.",
        "乙은 甲의 설득으로 절도를 결의한 뒤 X의 지갑을 가져갔다.",
    )
    occurrences = tuple(
        GoldOccurrence(f"gocc:{index:03d}", actor, source, 0, len(source))
        for index, (actor, source) in enumerate(zip(("甲", "乙"), sources, strict=True), 1)
    )
    registry = load_definitions(ROOT / "data/v2/definitions")
    instances = (
        OffenseInstanceKey("participation-gate", "甲", "offense.theft", "gocc:001"),
        OffenseInstanceKey("participation-gate", "乙", "offense.theft", "gocc:002"),
    )
    targets = participation_route_targets(registry, instances)[:1]
    raw, metadata = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call2_participation"),
        user_template=load_prompt("v2_call2_participation_user"),
        payload=participation_request_payload(
            registry=registry, occurrences=occurrences, targets=targets
        ),
        schema_name="v2_call2_participation_gate",
        schema=participation_schema(targets),
        max_tokens=256,
        temperature=0.0,
        seed=17,
    )
    assessments = validate_participation_output(raw, targets=targets)
    assert metadata.get("finish_reason") == "stop"
    assert tuple(value.option_id for value in assessments) == ("instigator:0001",)

    unrelated_instances = tuple(
        OffenseInstanceKey(
            "participation-gate", actor, "offense.injury", f"gocc:{index:03d}"
        )
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    unrelated_targets = participation_route_targets(registry, unrelated_instances)[:1]
    unrelated_raw, _ = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call2_participation"),
        user_template=load_prompt("v2_call2_participation_user"),
        payload=participation_request_payload(
            registry=registry,
            occurrences=occurrences,
            targets=unrelated_targets,
        ),
        schema_name="v2_call2_participation_negative_gate",
        schema=participation_schema(unrelated_targets),
        max_tokens=256,
        temperature=0.0,
        seed=17,
    )
    unrelated = validate_participation_output(
        unrelated_raw, targets=unrelated_targets
    )
    assert tuple(value.option_id for value in unrelated) == ("none",)
