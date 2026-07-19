from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import compile_rule_ir, validate_norm_card_set, validate_rule_ir  # noqa: E402


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
CARD_MANIFEST = FRAUD_ROOT / "fraud_norm_card_manifest.json"
CORE_QUEUE = FRAUD_ROOT / "fraud_core_rule_review_queue.json"
CORE_DECISIONS = FRAUD_ROOT / "fraud_core_rule_review_decisions.jsonl"
CORE_AUDIT = FRAUD_ROOT / "fraud_core_rule_human_review_audit.json"
CORE_SET = FRAUD_ROOT / "fraud_core_norm_card_set.json"
FEWSHOT = FRAUD_ROOT / "fraud_rule_ir_generation_fewshot.json"
FEWSHOT_SCALLOP = PROJECT_ROOT / "rules/exemplars/fraud_rule_ir_generation_fewshot.scl"
GENERATION_REQUEST = FRAUD_ROOT / "fraud_full_rule_ir_generation_request.json"
PREP_MANIFEST = FRAUD_ROOT / "fraud_rule_ir_generation_prep_manifest.json"
PREP_REVIEW_QUEUE = FRAUD_ROOT / "fraud_rule_ir_generation_prep_review_queue.json"
PREP_REVIEW_DECISIONS = FRAUD_ROOT / "fraud_rule_ir_generation_prep_review_decisions.jsonl"
PREP_REVIEW_GUIDE = FRAUD_ROOT / "fraud_rule_ir_generation_prep_review_guide.md"
PROMPT = PROJECT_ROOT / "prompts/rulegen_merge_rule_ir.md"
RULE_IR_SCHEMA = PROJECT_ROOT / "docs/contracts/rule_ir.schema.json"
NORM_CARD_SCHEMA = PROJECT_ROOT / "docs/contracts/norm_card_set.schema.json"
RULEGEN_VALIDATOR = PROJECT_ROOT / "src/idpr/rulegen/__init__.py"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_union(cards: list[dict[str, Any]]) -> list[dict[str, str]]:
    refs = {
        (ref["comment_id"], ref["section_path"], ref["quote"]): ref
        for card in cards
        for ref in card["source_refs"]
    }
    return [refs[key] for key in sorted(refs)]


def predicate(
    predicate_id: str,
    arguments: list[tuple[str, str]],
    *,
    kind: str,
    role: str,
    origin: str,
    definition: str,
    cards: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    linked = cards or []
    return {
        "id": predicate_id,
        "arguments": [
            {"name": name, "type": argument_type}
            for name, argument_type in arguments
        ],
        "kind": kind,
        "role": role,
        "origin": origin,
        "definition": definition,
        "source_refs": source_union(linked),
        "norm_card_ids": sorted(card["id"] for card in linked),
    }


def variable(value: str) -> dict[str, str]:
    return {"kind": "variable", "value": value}


def string(value: str) -> dict[str, str]:
    return {"kind": "string", "value": value}


def atom(
    predicate_id: str,
    *arguments: dict[str, str],
    negated: bool = False,
) -> dict[str, Any]:
    return {
        "predicate": predicate_id,
        "arguments": list(arguments),
        "negated": negated,
    }


def rule(
    rule_id: str,
    head: dict[str, Any],
    body: list[dict[str, Any]],
    cards: list[dict[str, Any]],
    review_notes: str,
) -> dict[str, Any]:
    return {
        "id": rule_id,
        "head": head,
        "body": body,
        "source_refs": source_union(cards),
        "norm_card_ids": sorted(card["id"] for card in cards),
        "review_notes": review_notes,
    }


def build_fewshot(cards_by_id: dict[str, dict[str, Any]], card_set_id: str) -> dict[str, Any]:
    deception_card = cards_by_id[
        "deception.fraud.definition.deception-good-faith-mistake"
    ]
    false_belief_card = cards_by_id[
        "deception.fraud.element.deception-must-create-false-belief"
    ]
    linked_cards = [deception_card, false_belief_card]
    assessment_args = [
        ("case_id", "String"),
        ("assessment_id", "String"),
        ("defendant_id", "String"),
        ("deceived_person_id", "String"),
        ("status", "String"),
    ]
    result_args = [
        ("case_id", "String"),
        ("defendant_id", "String"),
        ("deceived_person_id", "String"),
    ]
    predicates = [
        predicate(
            "provable",
            [("case_id", "String"), ("assessment_id", "String")],
            kind="rule",
            role="input",
            origin="system",
            definition="The assessment may be consumed by substantive rules.",
        ),
        predicate(
            "deception_good_faith_assessment",
            assessment_args,
            kind="standard",
            role="input",
            origin="commentary",
            definition=(
                "신의칙에 반하여 상대방에게 착오를 일으키는 기망인지에 대한 명시적 평가"
            ),
            cards=[deception_card],
        ),
        predicate(
            "false_belief_created_assessment",
            assessment_args,
            kind="standard",
            role="input",
            origin="commentary",
            definition="기망적 수단으로 진실과 다른 관념이 실제 형성되었는지에 대한 평가",
            cards=[false_belief_card],
        ),
        predicate(
            "deception_supported",
            result_args,
            kind="rule",
            role="derived",
            origin="commentary",
            definition="기망행위 요건이 명시적으로 충족된 상태",
            cards=linked_cards,
        ),
        predicate(
            "deception_not_satisfied",
            result_args,
            kind="rule",
            role="derived",
            origin="commentary",
            definition="기망행위 요건이 명시적으로 충족되지 않은 상태",
            cards=linked_cards,
        ),
        predicate(
            "deception_undetermined",
            result_args,
            kind="rule",
            role="derived",
            origin="commentary",
            definition="기망행위 요건 판단에 필요한 평가가 미확인인 상태",
            cards=linked_cards,
        ),
    ]
    c = variable("case_id")
    d = variable("defendant_id")
    v = variable("deceived_person_id")
    a1 = variable("assessment_1")
    a2 = variable("assessment_2")
    rules = [
        rule(
            "fraud.example.deception_supported",
            atom("deception_supported", c, d, v),
            [
                atom(
                    "deception_good_faith_assessment",
                    c,
                    a1,
                    d,
                    v,
                    string("satisfied"),
                ),
                atom("provable", c, a1),
                atom(
                    "false_belief_created_assessment",
                    c,
                    a2,
                    d,
                    v,
                    string("satisfied"),
                ),
                atom("provable", c, a2),
            ],
            linked_cards,
            "두 평가가 모두 satisfied인 경우에만 기망 충족을 도출한다.",
        ),
        rule(
            "fraud.example.deception_not_satisfied",
            atom("deception_not_satisfied", c, d, v),
            [
                atom(
                    "false_belief_created_assessment",
                    c,
                    a1,
                    d,
                    v,
                    string("not_satisfied"),
                ),
                atom("provable", c, a1),
            ],
            [false_belief_card],
            "진실과 다른 관념 형성이 명시적으로 부정된 경우를 불성립 경로로 보낸다.",
        ),
        rule(
            "fraud.example.deception_unknown",
            atom("deception_undetermined", c, d, v),
            [
                atom(
                    "deception_good_faith_assessment",
                    c,
                    a1,
                    d,
                    v,
                    string("unknown"),
                ),
                atom("provable", c, a1),
            ],
            [deception_card],
            "기망 standard가 unknown이면 부정으로 접지 않고 미확인 상태를 보존한다.",
        ),
    ]
    return {
        "version": "1.1.0",
        "rule_set_id": "kr.fraud.article347.rule_ir_generation_fewshot",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "source_scope": {
            "target_paths": ["commentary://001692/제347조"],
            "comment_ids": sorted(
                {ref["comment_id"] for ref in source_union(linked_cards)}
            ),
        },
        "norm_card_scope": {
            "card_set_id": card_set_id,
            "card_ids": sorted(card["id"] for card in linked_cards),
        },
        "predicates": predicates,
        "rules": rules,
        "legal_review_questions": [],
        "coverage_gaps": [
            "기망 쟁점의 상태·증거게이트 구조만 보여 주며 사기죄 전체 결론은 도출하지 않는다."
        ],
    }


REVIEW_ITEMS = [
    {
        "review_id": "fraud.rule_ir.prep.scope",
        "topic": "core_scope",
        "agent_recommendation": "approve",
        "proposal": "사용자 검수 완료된 88개만 RuleIR 입력으로 사용하고 558개 RAG는 제외한다.",
        "rationale": "구체 유형·판례·학설을 실행 core로 재유입시키지 않는다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.single_call",
        "topic": "generation_unit",
        "agent_recommendation": "approve",
        "proposal": "aggregate NormCardSet 전체를 Terra 단일 호출로 생성한다.",
        "rationale": "모듈 분할 시 card_set_id와 교차 predicate 병합 오류가 발생한다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.standard_state",
        "topic": "standard_assessment_state",
        "agent_recommendation": "approve",
        "proposal": "standard 결과를 satisfied, not_satisfied, unknown의 명시적 3상태로 받는다.",
        "rationale": "미추출 사실을 false로 취급하지 않고 양방향 사실과 미확인을 보존한다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.evidence_gate",
        "topic": "evidence_gate",
        "agent_recommendation": "approve",
        "proposal": "모든 commentary input은 같은 case_id와 assessment_id의 provable을 함께 요구한다.",
        "rationale": "절차·증명 게이트를 통과하지 않은 판단이 실체법 rule에 들어가지 못하게 한다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.actor_roles",
        "topic": "actor_role_signature",
        "agent_recommendation": "approve",
        "proposal": (
            "피고인, 피기망자, 처분자, 재산소유자, 객체, 수익자를 별도 역할 인자로 "
            "유지하되 서로 다른 사람이라고 가정하지 않는다. 성립 rule에서는 피기망자와 "
            "처분자에 같은 ID 변수를 사용한다."
        ),
        "rationale": (
            "피기망자와 처분행위자의 동일성을 보존하면서, 삼각사기에서 그 사람과 "
            "재산소유자가 다른 경우의 처분 권능·지위를 별도로 심사하기 위함이다."
        ),
    },
    {
        "review_id": "fraud.rule_ir.prep.outputs",
        "topic": "result_interface",
        "agent_recommendation": "approve",
        "proposal": "성립, 불성립, undetermined, conflict를 별도 derived predicate로 출력한다.",
        "rationale": "부정과 미확인을 성립 실패 하나로 접지 않고 모순도 노출한다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.open_world",
        "topic": "open_world_policy",
        "agent_recommendation": "approve",
        "proposal": "생성 RuleIR에서는 negation을 금지하고 negative·exception을 명시적 조건으로 표현한다.",
        "rationale": "관계 부재를 법적 사실 부존재로 오인하지 않는다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.fewshot",
        "topic": "fewshot_policy",
        "agent_recommendation": "approve",
        "proposal": "기존 8장 법리 대신 현재 상태·증거게이트 계약만 보여 주는 2장 구조 예시를 제공한다.",
        "rationale": "과거 손해·불법영득의사 policy가 새 출력으로 누출되는 것을 막는다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.review_sequence",
        "topic": "review_sequence",
        "agent_recommendation": "approve",
        "proposal": "Terra 후 에이전트 검토·장문 자연어 설명, 사용자 검토, Sol, 사용자 재검토, Scallop 순서로 진행한다.",
        "rationale": "모델 출력과 critic 지적을 자동 정답으로 취급하지 않는다.",
    },
    {
        "review_id": "fraud.rule_ir.prep.api_ceiling",
        "topic": "api_execution_ceiling",
        "agent_recommendation": "approve",
        "proposal": "Terra 1회, 동시성 1, retry 0, max completion 64000으로 제한한다.",
        "rationale": "전체 출력을 한 번에 받되 자동 재호출과 비용 확산을 차단한다.",
    },
]


def preserve_review_decisions() -> list[dict[str, Any]]:
    existing_rows = read_jsonl(PREP_REVIEW_DECISIONS) if PREP_REVIEW_DECISIONS.exists() else []
    existing = {row["review_id"]: row for row in existing_rows}
    if len(existing) != len(existing_rows):
        raise ValueError("Duplicate RuleIR prep review decision")
    expected_ids = {item["review_id"] for item in REVIEW_ITEMS}
    if set(existing) - expected_ids:
        raise ValueError("Unknown RuleIR prep review decision")
    return [
        existing.get(
            item["review_id"],
            {
                "review_id": item["review_id"],
                "status": "pending",
                "decision": None,
                "notes": "",
            },
        )
        for item in REVIEW_ITEMS
    ]


def main() -> None:
    queue = read_json(CORE_QUEUE)
    decisions = read_jsonl(CORE_DECISIONS)
    if queue.get("api_calls") != 0 or queue.get("unresolved") != 0:
        raise ValueError("Core human review must be complete without API calls")
    if len(decisions) != queue.get("cards") or not all(
        row.get("status") == "completed" and row.get("decision") == "approve"
        for row in decisions
    ):
        raise ValueError("Every active core card must be approved")

    manifest = read_json(CARD_MANIFEST)
    cards_by_id: dict[str, dict[str, Any]] = {}
    module_by_id: dict[str, str] = {}
    for module in manifest["modules"]:
        card_set = read_json(PROJECT_ROOT / module["path"])
        for card in card_set["cards"]:
            cards_by_id[card["id"]] = card
            module_by_id[card["id"]] = module["module"]
    core_ids = [item["card_id"] for item in queue["items"]]
    if len(core_ids) != 88 or len(core_ids) != len(set(core_ids)):
        raise ValueError("Core queue must contain 88 unique cards")
    core_cards = [cards_by_id[card_id] for card_id in core_ids]
    if any(card["review_required"] for card in core_cards):
        raise ValueError("Approved aggregate contains review_required cards")
    if {card["formalization"] for card in core_cards} != {
        "deterministic_rule",
        "standard_input",
    }:
        raise ValueError("Approved aggregate contains a non-core formalization")

    comment_ids = sorted(
        {ref["comment_id"] for card in core_cards for ref in card["source_refs"]}
    )
    aggregate = {
        "version": "1.1.0",
        "card_set_id": "kr.fraud.article347.core.norms.v1",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "complete",
        "construction": "reviewed_aggregate",
        "source_scope": {
            "target_paths": ["commentary://001692/제347조"],
            "comment_ids": comment_ids,
        },
        "cards": core_cards,
        "legal_review_questions": [],
        "coverage_gaps": [
            "사용자 검수로 context_only가 된 558개 카드와 형법총칙 future work는 실행 core 밖이다."
        ],
    }
    commentary = {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY)
        if row["comment_id"] in set(comment_ids)
    }
    validate_norm_card_set(aggregate, commentary)
    write_json(CORE_SET, aggregate)

    fewshot = build_fewshot(cards_by_id, aggregate["card_set_id"])
    validate_rule_ir(fewshot, commentary, aggregate)
    write_json(FEWSHOT, fewshot)
    FEWSHOT_SCALLOP.write_text(
        compile_rule_ir(fewshot, commentary, aggregate), encoding="utf-8"
    )

    formalization_counts = dict(
        sorted(Counter(card["formalization"] for card in core_cards).items())
    )
    module_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for card in core_cards:
        module_counts[module_by_id[card["id"]]][card["formalization"]] += 1
    output_signatures = [
        {
            "id": "fraud_established",
            "arguments": [
                "case_id",
                "defendant_id",
                "deceived_person_id",
                "disposer_id",
                "property_owner_id",
                "beneficiary_id",
            ],
        }
    ] + [
        {
            "id": output_id,
            "arguments": ["case_id", "defendant_id", "issue_id"],
        }
        for output_id in (
            "fraud_not_established",
            "fraud_undetermined",
            "fraud_conflict",
        )
    ]
    request = {
        "version": "1.0.0",
        "request_id": "fraud.article347.rule_ir.full.v1",
        "stage": "rule_ir",
        "target": {
            "rule_set_id": "kr.fraud.article347.full.v1_candidate",
            "issue_tag": "fraud",
            "status": "draft",
            "legal_review": "pending",
        },
        "bounded_source_material": {"approved_norm_card_set": aggregate},
        "architecture_contract": {
            "generation_unit": "single_complete_rule_ir",
            "case_isolation": "Every non-system predicate starts with case_id: String.",
            "standard_assessment": {
                "statuses": ["satisfied", "not_satisfied", "unknown"],
                "input_prefix": ["case_id", "assessment_id"],
                "input_suffix": ["status"],
                "missing_is_false": False,
            },
            "evidence_gate": {
                "predicate": "provable",
                "arguments": ["case_id", "assessment_id"],
                "required_for_every_commentary_input": True,
            },
            "closed_case_gate": {
                "predicate": "case_assessment_complete",
                "arguments": ["case_id", "defendant_id"],
                "meaning": (
                    "The router-selected assessment bundle is finite and complete; "
                    "only the final outcome stratum may use negation after this gate."
                ),
            },
            "actor_roles": [
                "defendant_id",
                "deceived_person_id",
                "disposer_id",
                "property_owner_id",
                "beneficiary_id",
            ],
            "role_identity": {
                "separate_slots_imply_distinct_people": False,
                "same_entity_id_may_fill_multiple_roles": True,
                "fraud_established_requires_same_variable": [
                    "deceived_person_id",
                    "disposer_id",
                ],
                "property_owner_may_differ_from_deceived_disposer": True,
                "different_owner_requires_triangular_fraud_authority_assessment": True,
            },
            "required_output_predicates": output_signatures,
            "negation_allowed": "final_outcome_stratum_only_after_closed_case_gate",
            "active_policy_allowed": False,
        },
        "coverage_contract": {
            "cards": len(core_cards),
            "formalizations": formalization_counts,
            "card_ids": sorted(core_ids),
            "standard_input_requires_input_standard": True,
            "deterministic_rule_requires_implementing_rule": True,
        },
        "excluded_context": {
            "cards": 558,
            "audit_path": "data/rulegen/fraud/fraud_core_rule_human_review_audit.json",
            "instruction": "Do not recreate excluded case-specific or rejected rules.",
        },
        "review_workflow": [
            "local_schema_provenance_and_generation_contract_validation",
            "agent_rule_ir_review",
            "agent_long_form_natural_language_explanation",
            "human_review",
            "sol_critic",
            "human_re_review",
            "scallop_compile_and_runtime_tests",
        ],
    }
    write_json(GENERATION_REQUEST, request)

    prep_decisions = preserve_review_decisions()
    PREP_REVIEW_DECISIONS.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in prep_decisions
        ),
        encoding="utf-8",
    )
    decision_by_id = {row["review_id"]: row for row in prep_decisions}
    review_queue = {
        "version": "1.0.0",
        "issue_tag": "fraud",
        "status": (
            "complete"
            if all(
                row.get("status") == "completed"
                and row.get("decision") == "approve"
                for row in prep_decisions
            )
            else "pending"
        ),
        "method": "agent_rule_ir_generation_preflight_no_api",
        "api_calls": 0,
        "items": [
            {**item, "human_review": decision_by_id[item["review_id"]]}
            for item in REVIEW_ITEMS
        ],
    }
    write_json(PREP_REVIEW_QUEUE, review_queue)

    system_chars = sum(
        len(path.read_text(encoding="utf-8"))
        for path in (PROMPT, RULE_IR_SCHEMA, FEWSHOT)
    )
    payload_chars = len(
        json.dumps(request, ensure_ascii=False, sort_keys=True)
    )
    total_chars = system_chars + payload_chars
    manifest_payload = {
        "version": "1.0.0",
        "issue_tag": "fraud",
        "status": "agent_review_complete_human_review_pending",
        "method": "single_call_full_rule_ir_preparation_no_api",
        "api_calls": 0,
        "planned_api_calls": {"terra_generation": 1, "sol_critic_later": 1},
        "execution_limits": {
            "terra_max_completion_tokens": 64000,
            "max_concurrency": 1,
            "max_retries": 0,
        },
        "input_counts": {
            "cards": len(core_cards),
            "comment_ids": len(comment_ids),
            "modules": len(module_counts),
            **formalization_counts,
        },
        "module_counts": {
            module: dict(sorted(counts.items()))
            for module, counts in sorted(module_counts.items())
        },
        "prompt_size": {
            "system_chars": system_chars,
            "payload_chars": payload_chars,
            "total_chars": total_chars,
            "estimated_prompt_tokens_low": math.ceil(total_chars / 4),
            "estimated_prompt_tokens_high": math.ceil(total_chars / 1.5),
            "expected_completion_tokens_low": 25000,
            "expected_completion_tokens_high": 50000,
            "note": (
                "Korean tokenization and model output density make this a planning "
                "range, not billing data."
            ),
        },
        "artifacts": {
            str(path.relative_to(PROJECT_ROOT)): sha256(path)
            for path in (
                CORE_SET,
                FEWSHOT,
                FEWSHOT_SCALLOP,
                GENERATION_REQUEST,
                COMMENTARY,
                PROMPT,
                RULE_IR_SCHEMA,
                NORM_CARD_SCHEMA,
                RULEGEN_VALIDATOR,
            )
        },
        "gates": {
            "core_human_review_complete": True,
            "agent_preflight_review_complete": True,
            "human_preflight_review_complete": review_queue["status"] == "complete",
            "terra_execution_allowed": review_queue["status"] == "complete",
            "agent_natural_language_explanation_required_after_terra": True,
            "sol_allowed_before_agent_and_human_review": False,
            "scallop_runtime_allowed_before_sol_and_human_re_review": False,
        },
        "source_audits": [
            str(CORE_AUDIT.relative_to(PROJECT_ROOT)),
            str(CORE_QUEUE.relative_to(PROJECT_ROOT)),
        ],
    }
    write_json(PREP_MANIFEST, manifest_payload)

    lines = [
        "# 사기죄 전체 RuleIR 생성 준비 검수",
        "",
        "## 현재 상태",
        "",
        "- 준비 단계 API 사용: 0회",
        "- agent preflight: 완료",
        "- 사용자 결정: "
        + ", ".join(
            f"{status}={count}"
            for status, count in sorted(
                Counter(row["status"] for row in prep_decisions).items()
            )
        ),
        (
            "- Terra 실행 게이트: 승인 완료"
            if review_queue["status"] == "complete"
            else "- Terra 실행 게이트: 사용자 승인 전 차단"
        ),
        f"- 입력 core: deterministic {formalization_counts['deterministic_rule']}개 + "
        f"standard {formalization_counts['standard_input']}개 = 88개",
        "- 제외 context: 558개",
        "- 생성 단위: 전체 RuleIR 단일 호출 1회",
        "",
        "## 에이전트 검토 결론",
        "",
        "1. 모듈 분할은 서로 다른 card_set_id와 교차 predicate 병합 오류를 만들므로 단일 호출이 낫다.",
        "2. 기존 8장 exemplar의 손해·불법영득의사 policy는 현재 결정과 달라 법리 few-shot에서 제외했다.",
        "3. 현재 2장 few-shot은 status, provable, actor role 구조만 보여 준다.",
        f"4. {formalization_counts['standard_input']}개 standard는 "
        "satisfied/not_satisfied/unknown을 명시적으로 입력받는다.",
        f"5. {formalization_counts['deterministic_rule']}개 deterministic 카드는 "
        "최소 한 개의 실제 rule에서 소비되어야 한다.",
        "6. RuleIR 생성 후 제가 전 규칙을 검토하고 장문 자연어 설명을 작성하기 전에는 사용자 검수로 넘기지 않는다.",
        "7. 그 사용자 검수 뒤에만 Sol을 호출하고, Sol 지적도 다시 사람에게 공개한다.",
        "",
        "## 사용자 검수 항목",
        "",
        "| ID | 주제 | 제안 | 에이전트 의견 |",
        "|---|---|---|---|",
    ]
    for item in REVIEW_ITEMS:
        lines.append(
            f"| `{item['review_id']}` | {item['topic']} | {item['proposal']} | "
            f"{item['agent_recommendation']} |"
        )
    lines.extend(
        [
            "",
            "승인·수정 의견은 이 가이드의 항목 ID 기준으로 전달하면 에이전트가 "
            "`fraud_rule_ir_generation_prep_review_decisions.jsonl`에 반영한다.",
            "",
            "## 생성 후 사용자에게 제공할 묶음",
            "",
            "- 원본 전체 RuleIR JSON",
            "- 로컬 validator 결과와 88장 coverage 표",
            "- 에이전트의 규칙별 장문 자연어 설명",
            "- 성립·불성립·unknown·conflict 도출 경로",
            "- 남은 구조·법률 질문",
            "- 각 standard에 필요한 positive·opposing·missing feature와 RAG 검색 시점",
            "- 삼각사기 역할 인자와 일반 사기에서 동일 인물 ID를 재사용하는 방식",
            "- 피기망자와 처분자에 동일 변수를 쓰고 재산소유자와의 관계를 나누는 방식",
            "",
            "## 파일",
            "",
            "- aggregate core: `data/rulegen/fraud/fraud_core_norm_card_set.json`",
            "- Terra payload: `data/rulegen/fraud/fraud_full_rule_ir_generation_request.json`",
            "- 구조 few-shot: `data/rulegen/fraud/fraud_rule_ir_generation_fewshot.json`",
            "- 준비 manifest: `data/rulegen/fraud/fraud_rule_ir_generation_prep_manifest.json`",
            "- 결정 파일: `data/rulegen/fraud/fraud_rule_ir_generation_prep_review_decisions.jsonl`",
            "",
        ]
    )
    PREP_REVIEW_GUIDE.write_text("\n".join(lines), encoding="utf-8")

    print(
        json.dumps(
            {
                "api_calls": 0,
                "cards": len(core_cards),
                "comment_ids": len(comment_ids),
                "formalizations": formalization_counts,
                "review_items": len(REVIEW_ITEMS),
                "human_review_status": review_queue["status"],
                "prompt_chars": total_chars,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
