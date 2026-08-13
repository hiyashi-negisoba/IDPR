from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.article263_grounding import (
    Article263OccurrencePair,
    article263_request_payload,
    article263_schema,
    validate_article263_output,
)
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    predicate_definitions,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationLocalTarget,
    participation_local_targets,
    participation_request_payload,
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
from idpr.v2.runtime.utilized_participant_outcome import (
    utilized_participant_outcome_targets,
    utilized_participant_predicate_targets,
    utilized_participant_request_payload,
    utilized_participant_schema,
    validate_utilized_participant_output,
)

ROOT = Path(__file__).resolve().parents[2]


def _factual_participant_source(case_id: str, participant_label: str) -> str:
    rows = (
        json.loads(line)
        for line in (ROOT / "data/v2/gold_factual_participants.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    )
    matches = [
        participant["source_text"]
        for row in rows
        if row["sub_question_id"] == case_id
        for participant in row["participants"]
        if participant["participant_label"] == participant_label
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one factual participant source for {case_id}/{participant_label}"
        )
    return matches[0]


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


def test_real_gemma_prefers_explicit_actual_incapacity_status_over_actor_mistake() -> None:
    source = (
        "丙은 자신의 집에서 C와 함께 술을 마시던 중, 술에 취해 누워 있는 C의 하의를 "
        "벗긴 후 C를 1회 간음하였다. 당시 丙은 C가 만취하여 심신상실 상태에 있다고 "
        "생각하고 이를 이용한 것이었는데, 실제로 C는 반항이 불가능할 정도로 술에 "
        "취하지는 않았다."
    )
    _run_gate(
        case_id="kcl_criminal_r11_p2_q1_da",
        actor_id="丙",
        occurrence_id="gocc:001",
        source=source,
        specs=(
            (
                "offense.quasi_rape",
                "legal_element.mental_incapacity_or_physical_helplessness_status",
                "FALSE",
            ),
        ),
    )


@pytest.mark.parametrize(
    ("case_id", "participant_label", "source", "offense_ref", "expected"),
    (
        (
            "kcl_criminal_r11_p2_q1_na",
            "결재권자",
            _factual_participant_source("kcl_criminal_r11_p2_q1_na", "결재권자"),
            "offense.false_public_document_creation",
            {"legal_element.intent": "FALSE"},
        ),
        (
            "kcl_criminal_r12_p1_q1",
            "B",
            _factual_participant_source("kcl_criminal_r12_p1_q1", "B"),
            "offense.private_document_forgery",
            {"legal_element.forgery_without_authority": "FALSE"},
        ),
        (
            "kcl_criminal_r14_p1_q3",
            "乙",
            _factual_participant_source("kcl_criminal_r14_p1_q3", "乙"),
            "offense.obstruction_of_right_exercise",
            {"legal_element.own_property_object": "FALSE"},
        ),
    ),
)
def test_real_gemma_assesses_utilized_participant_predicates_without_liability_label(
    case_id: str,
    participant_label: str,
    source: str,
    offense_ref: str,
    expected: dict[str, str],
) -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    registry = load_definitions(ROOT / "data/v2/definitions")
    participant = GoldFactualParticipant("fpart:001", participant_label, source, 0, len(source))
    instance = OffenseInstanceKey(case_id, "utilizer", offense_ref, "gocc:001")
    outcome_target = utilized_participant_outcome_targets(registry, (instance,), (participant,))[0]
    predicate_targets = utilized_participant_predicate_targets(registry, (outcome_target,))
    raw, metadata = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call2_utilized_participant_outcome"),
        user_template=load_prompt("v2_call2_utilized_participant_outcome_user"),
        payload=utilized_participant_request_payload(
            registry,
            participant=participant,
            outcome_target=outcome_target,
            predicate_targets=predicate_targets,
        ),
        schema_name="v2_call2_utilized_participant_gate",
        schema=utilized_participant_schema(predicate_targets),
        max_tokens=512,
        temperature=0.0,
        seed=17,
    )
    assessments = validate_utilized_participant_output(
        raw, predicate_targets=predicate_targets
    )
    actual = {value.target.predicate_ref: value.truth for value in assessments}
    assert metadata.get("finish_reason") == "stop"
    assert {ref: actual[ref] for ref in expected} == expected


@pytest.mark.xfail(
    strict=False,
    reason=(
        "known Gemma instability: repeated seed-17 calls alternate between false content "
        "and unauthorized nominee use even with the reviewed general legal standard"
    ),
)
def test_real_gemma_known_instability_false_content_vs_forgery_authority() -> None:
    source = (
        "甲은 이 글의 신빙성을 높이기 위해 관리사무소 직원 B에게 부탁하여 ‘A가 "
        "혼외자와 함께 있는 것을 보았다’는 허위 내용이 기재된 B 명의의 사실확인서를 "
        "받아 위 게시물에 첨부하였다."
    )
    _run_gate(
        case_id="kcl_criminal_r12_p1_q1",
        actor_id="甲",
        occurrence_id="gocc:002",
        source=source,
        specs=(
            (
                "offense.private_document_forgery",
                "legal_element.forgery_without_authority",
                "FALSE",
            ),
        ),
    )


def test_real_gemma_reads_article263_pair_level_relation_evidence() -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    sources = (
        "甲은 B를 때려눕히고 발로 복부를 수 회 걷어찬 다음 도망갔다.",
        "약 2시간 후 乙은 쓰러진 B의 복부를 수 회 걷어찼다.",
    )
    occurrences = tuple(
        GoldOccurrence(f"gocc:{index:03d}", actor, source, 0, len(source))
        for index, (actor, source) in enumerate(zip(("甲", "乙"), sources, strict=True), 1)
    )
    left = OffenseInstanceKey("article263-gate", "甲", "offense.injury", "gocc:001")
    right = OffenseInstanceKey("article263-gate", "乙", "offense.injury", "gocc:002")
    relation = "부검결과 甲과 乙 중 누구의 행위로 사망하였는지 판명되지 않았다."
    pair = Article263OccurrencePair("article263-pair:0001", left, right, relation, 0, len(relation))
    raw, metadata = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call2_article263"),
        user_template=load_prompt("v2_call2_article263_user"),
        payload=article263_request_payload(occurrences=occurrences, pairs=(pair,)),
        schema_name="v2_call2_article263_gate",
        schema=article263_schema((pair,)),
        max_tokens=256,
        temperature=0.0,
        seed=17,
    )
    assessment = validate_article263_output(raw, pairs=(pair,))[0]
    assert metadata.get("finish_reason") == "stop"
    assert dict(assessment.truths)["legal_element.causal_origin_unascertained"] == "TRUE"
    assert dict(assessment.shared_result_truths)["legal_element.injury_result"] == "TRUE"


@pytest.mark.parametrize(
    ("actor_id", "occurrence_id", "source"),
    (
        (
            "甲",
            "gocc:001",
            ("甲은 마침 현장에 도착한 A의 아버지 B를 발견하고 체포될까 두려워 "
            "도망치다가 아파트 후문 노상에서 B에게 잡히자 B를 때려눕히고 발로 복부를 "
            "수 회 걷어찬 다음 도망갔다."),
        ),
        (
            "乙",
            "gocc:002",
            ("약 2시간 후 甲의 친구 乙이 평소에 감정이 좋지 않던 B가 쓰러진 것을 "
            "우연히 발견하고 화가 나서 발로 B의 복부를 수 회 걷어찼다."),
        ),
    ),
)
def test_real_gemma_article263_underlying_natural_person_when_focused(
    actor_id: str, occurrence_id: str, source: str
) -> None:
    _run_gate(
        case_id="kcl_criminal_r10_p1_q2",
        actor_id=actor_id,
        occurrence_id=occurrence_id,
        source=source,
        specs=(("offense.injury", "legal_element.natural_person_victim_status", "TRUE"),),
    )


@pytest.mark.xfail(
    strict=False,
    reason=(
        "known Gemma undercall: deliberate repeated kicks to the victim's abdomen remain "
        "UNKNOWN for generic injury intent even in a focused request"
    ),
)
@pytest.mark.parametrize(
    ("actor_id", "occurrence_id", "source"),
    (
        (
            "甲",
            "gocc:001",
            ("甲은 마침 현장에 도착한 A의 아버지 B를 발견하고 체포될까 두려워 "
            "도망치다가 아파트 후문 노상에서 B에게 잡히자 B를 때려눕히고 발로 복부를 "
            "수 회 걷어찬 다음 도망갔다."),
        ),
        (
            "乙",
            "gocc:002",
            ("약 2시간 후 甲의 친구 乙이 평소에 감정이 좋지 않던 B가 쓰러진 것을 "
            "우연히 발견하고 화가 나서 발로 B의 복부를 수 회 걷어찼다."),
        ),
    ),
)
def test_real_gemma_known_undercall_article263_underlying_injury_intent(
    actor_id: str, occurrence_id: str, source: str
) -> None:
    _run_gate(
        case_id="kcl_criminal_r10_p1_q2",
        actor_id=actor_id,
        occurrence_id=occurrence_id,
        source=source,
        specs=(("offense.injury", "legal_element.intent", "TRUE"),),
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

    def find_target(
        candidates: tuple[ParticipationLocalTarget, ...],
        kind: str,
        actor: str,
        principal: str,
    ) -> ParticipationLocalTarget:
        matches = tuple(
            target
            for target in candidates
            if target.kind == kind
            and target.members[0].actor_id == actor
            and target.members[1].actor_id == principal
        )
        assert len(matches) == 1
        return matches[0]

    def assess(
        target: ParticipationLocalTarget,
        evidence: tuple[GoldOccurrence, ...],
    ) -> tuple[str, dict[str, object]]:
        raw, metadata = VLLMClient(base_url, model).complete_json(
            system_prompt=load_prompt("v2_call2_participation"),
            user_template=load_prompt("v2_call2_participation_user"),
            payload=participation_request_payload(
                registry=registry,
                occurrences=evidence,
                targets=(target,),
            ),
            schema_name="v2_call2_participation_gate",
            schema=participation_schema((target,)),
            max_tokens=256,
            temperature=0.0,
            seed=17,
        )
        return validate_participation_output(raw, targets=(target,)).truth, metadata

    targets = participation_local_targets(registry, instances)
    forward = find_target(targets, "instigation", "甲", "乙")
    forward_aiding = find_target(targets, "aiding", "甲", "乙")
    reverse = find_target(targets, "instigation", "乙", "甲")
    derivative_as_co = find_target(targets, "co_principal_group", "甲", "乙")
    forward_truth, metadata = assess(forward, occurrences)
    forward_aiding_truth, _ = assess(forward_aiding, occurrences)
    reverse_truth, _ = assess(reverse, occurrences)
    derivative_as_co_truth, _ = assess(derivative_as_co, occurrences)
    assert metadata.get("finish_reason") == "stop"
    assert forward_truth == "TRUE"
    assert forward_aiding_truth == "FALSE"
    assert reverse_truth == "FALSE"
    assert derivative_as_co_truth == "FALSE"

    joint_source = (
        "甲과 乙은 X의 지갑을 함께 훔치기로 공모하고, 甲이 망을 보는 동안 乙이 지갑을 가져갔다."
    )
    joint_occurrences = tuple(
        GoldOccurrence(f"joint:{index:03d}", actor, joint_source, 0, len(joint_source))
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    joint_instances = tuple(
        OffenseInstanceKey(
            "participation-joint-gate",
            actor,
            "offense.theft",
            f"joint:{index:03d}",
        )
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    joint_targets = participation_local_targets(registry, joint_instances)
    joint_co = find_target(joint_targets, "co_principal_group", "甲", "乙")
    joint_truth, _ = assess(joint_co, joint_occurrences)
    assert joint_truth == "TRUE"

    unrelated_instances = tuple(
        OffenseInstanceKey("participation-gate", actor, "offense.injury", f"gocc:{index:03d}")
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    unrelated_targets = participation_local_targets(registry, unrelated_instances)
    unrelated = find_target(unrelated_targets, "instigation", "甲", "乙")
    unrelated_truth, _ = assess(
        unrelated,
        occurrences,
    )
    assert unrelated_truth == "FALSE"

    derived_instances = tuple(
        OffenseInstanceKey(
            "participation-gate",
            actor,
            "derived_offense.aggravated_injury",
            f"gocc:{index:03d}",
        )
        for index, actor in enumerate(("甲", "乙"), 1)
    )
    derived_targets = participation_local_targets(registry, derived_instances)
    base_only_instigation = find_target(derived_targets, "instigation", "甲", "乙")
    base_only_truth, _ = assess(base_only_instigation, occurrences)
    assert base_only_truth == "FALSE"
