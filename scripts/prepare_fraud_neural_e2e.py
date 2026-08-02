from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.legacy.fraud_neural import (  # noqa: E402
    build_authority_packet,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
    validate_fraud_fact_graph,
)


TARGET_ITEM_ID = "kcl_criminal_r14_p1_q2"
INVENTORY_PATH = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
NORM_CARD_PATH = PROJECT_ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
OUTPUT_ROOT = PROJECT_ROOT / "data/e2e/fraud"
CASE_PATH = OUTPUT_ROOT / "kcl_r14_p1_q2_case.json"
REPLAY_PATH = OUTPUT_ROOT / "kcl_r14_p1_q2_replay_neural.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_target_row() -> dict[str, Any]:
    matches = []
    for line in INVENTORY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("sub_question_id") == TARGET_ITEM_ID:
            matches.append(row)
    if len(matches) != 1:
        raise RuntimeError(f"expected one {TARGET_ITEM_ID} row, found {len(matches)}")
    return matches[0]


def extract_part_two(question_text: str) -> str:
    match = re.search(r"(?ms)^\(2\) 乙은 .*?(?=\n\(3\) )", question_text)
    if match is None:
        raise RuntimeError("cannot isolate the (2) fact paragraph")
    case_text = match.group(0).strip()
    required = (
        "자신의 딸의 수술비 명목인 것처럼 말하여 3천만 원을 빌렸다",
        "B에게서 빌린 3천만 원",
    )
    if not all(fragment in case_text for fragment in required):
        raise RuntimeError("isolated paragraph does not contain the fraud target facts")
    return case_text


def build_case() -> dict[str, Any]:
    row = read_target_row()
    case_text = extract_part_two(row["question_text"])
    return {
        "version": "1.0.0",
        "case_id": "kcl_r14_p1_q2_eul_fraud",
        "source": {
            "dataset": row["source"]["dataset"],
            "inventory_path": str(INVENTORY_PATH.relative_to(PROJECT_ROOT)),
            "sub_question_id": row["sub_question_id"],
            "source_row_index": row["source"]["source_row_index"],
            "full_question_sha256": hashlib.sha256(
                row["question_text"].encode("utf-8")
            ).hexdigest(),
            "case_text_sha256": hashlib.sha256(case_text.encode("utf-8")).hexdigest(),
        },
        "case_text": case_text,
        "question_prompt": "(2)에서 乙의 B에 대한 사기죄 성부를 검토하시오.",
        "reasoning_plan_id": "loan_purpose",
        "required_profiles": ["loan_purpose"],
        "generation_instructions": [
            "乙의 B에 대한 사기죄만 검토한다.",
            "사건 사실은 case_text 밖에서 보충하지 않는다.",
            "본문에는 내부 provenance ID를 쓰지 않는다.",
        ],
        "target": {
            "issue_id": "fraud",
            "defendant_hint": "乙",
            "counterparty_hint": "B",
            "answer_subject": "乙의 B에 대한 사기죄",
            "role_hints": {
                "defendant": "乙",
                "deceived_person": "B",
                "disposer": "B",
                "property_owner": "B",
                "beneficiary": "乙",
            },
            "target_transaction": {
                "description": "B가 乙에게 3천만 원을 빌려준 차용 거래",
                "transferor_hint": "B",
                "immediate_recipient_hint": "乙",
            },
        },
        "allowed_profiles": ["loan_purpose"],
        "rule_set_id": "kr.fraud.article347.full.v1_candidate",
        "scope_note": (
            "원 문항의 뇌물공여·횡령 쟁점은 현재 사기죄 RuleIR 범위 밖이므로 "
            "乙의 B에 대한 사기죄만 판정한다. 평가 rubric은 모델 입력에 포함하지 않는다."
        ),
    }


def build_replay(case: dict[str, Any]) -> dict[str, Any]:
    fact_graph = {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "target_issue_id": "fraud",
        "actors": [
            {
                "entity_id": "eul",
                "mentions": ["乙"],
                "roles": ["defendant", "beneficiary"],
            },
            {
                "entity_id": "b",
                "mentions": ["B"],
                "roles": ["deceived_person", "disposer", "property_owner"],
            },
        ],
        "facts": [
            {
                "fact_id": "fact_001",
                "fact_kind": "true_purpose",
                "statement": "乙은 형사처벌을 피하기 위한 금품 자금을 마련하려 했다.",
                "source_quote": (
                    "乙은 위 (1) 사건으로 수사를 받게 되자 사법경찰관 P1에게 "
                    "금품을 주어 형사처벌을 면하기로 마음먹고, 그 자금을 마련하기 위해"
                ),
                "participants": ["eul"],
                "epistemic_status": "given",
                "issue_effects": [{"issue_id": "fraud_intent", "direction": "supports"}],
            },
            {
                "fact_id": "fact_002",
                "fact_kind": "representation",
                "statement": "乙은 B에게 돈이 딸의 수술비에 쓰일 것처럼 말했다.",
                "source_quote": "친구 B에게 자신의 딸의 수술비 명목인 것처럼 말하여",
                "participants": ["eul", "b"],
                "epistemic_status": "given",
                "issue_effects": [{"issue_id": "deception", "direction": "supports"}],
            },
            {
                "fact_id": "fact_003",
                "fact_kind": "disposition",
                "statement": "B는 乙에게 3천만 원을 빌려주었다.",
                "source_quote": "3천만 원을 빌렸다",
                "participants": ["eul", "b"],
                "epistemic_status": "given",
                "issue_effects": [
                    {"issue_id": "disposition", "direction": "supports"},
                    {"issue_id": "acquisition", "direction": "supports"},
                ],
            },
            {
                "fact_id": "fact_004",
                "fact_kind": "transfer",
                "statement": "乙은 B에게서 빌린 돈을 실제 수술비가 아닌 용도로 넘겼다.",
                "source_quote": "B에게서 빌린 3천만 원을 주면서 그 돈을 P1에게 전해 달라고 부탁하였다",
                "participants": ["eul", "b"],
                "epistemic_status": "given",
                "issue_effects": [{"issue_id": "deception", "direction": "supports"}],
            },
        ],
        "profiles": ["loan_purpose"],
        "retrieval_queries": [
            "차용금 용도기망의 중요성",
            "용도기망과 편취의 범의 판단",
        ],
        "unresolved_questions": [],
    }
    validate_fraud_fact_graph(fact_graph, case)

    selected_card_ids = select_fraud_card_plan(fact_graph, case=case)
    norm_cards = read_json(NORM_CARD_PATH)
    authority_packet = build_authority_packet(selected_card_ids, norm_cards)
    fact_basis = {
        "general_object.fraud.element.object-other-possessed-other-property": [
            "fact_003"
        ],
        "deception.fraud.definition.deception-good-faith-mistake": [
            "fact_001",
            "fact_002",
            "fact_003",
        ],
        "deception.fraud.standard.loan-purpose-materiality": [
            "fact_001",
            "fact_002",
            "fact_003",
            "fact_004",
        ],
        "fraud_mistake.error_definition": ["fact_002", "fact_003"],
        "fraud_mistake.error_disposition_motivation": ["fact_002", "fact_003"],
        "fraud_mistake.disposition_definition": ["fact_003"],
        "fraud_damage_acquisition.delivery_of_property": ["fact_003"],
        "fraud_intent.time_of_conduct": ["fact_001", "fact_002", "fact_004"],
        "fraud_mistake.gain_purpose": ["fact_001", "fact_002", "fact_003"],
        "fraud_intent.no_disposition_inducement_intent": [
            "fact_002",
            "fact_003",
        ],
        "deception.fraud.standard.intent-to-defraud-loan-inference": [
            "fact_001",
            "fact_002",
            "fact_004",
        ],
    }
    missing_basis = sorted(set(selected_card_ids) - set(fact_basis))
    if missing_basis:
        raise RuntimeError(f"synthetic replay lacks fact basis for {missing_basis}")
    assessments = []
    for index, card in enumerate(authority_packet, start=1):
        card_id = card["card_id"]
        status = (
            "not_satisfied"
            if card_id == "fraud_intent.no_disposition_inducement_intent"
            else "satisfied"
        )
        assessments.append(
            {
                "assessment_id": f"assessment_{index:03d}",
                "card_id": card_id,
                "status": status,
                "basis_fact_ids": (
                    [] if status == "not_satisfied" else fact_basis[card_id]
                ),
                "counter_fact_ids": (
                    fact_basis[card_id] if status == "not_satisfied" else []
                ),
                "missing_facts": [],
                "authority_comment_ids": [card["sources"][0]["comment_id"]],
                "rationale": (
                    "사례 원문 사실과 해당 NormCard의 명제를 함께 적용한 합성 replay 판단이다."
                ),
                "confidence": 1.0,
            }
        )
    assessment_bundle = {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "selected_card_ids": selected_card_ids,
        "assessments": assessments,
    }
    validate_fraud_assessment_bundle(
        assessment_bundle,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected_card_ids,
        authority_packet=authority_packet,
    )
    return {
        "version": "1.0.0",
        "artifact_type": "synthetic_contract_replay",
        "warning": "모델 성능 결과가 아니라 인터페이스와 Scallop 연결을 검증하는 고정 fixture이다.",
        "fact_graph": fact_graph,
        "assessment_bundle": assessment_bundle,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    case = build_case()
    replay = build_replay(case)
    write_json(CASE_PATH, case)
    write_json(REPLAY_PATH, replay)
    print(f"wrote {CASE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"wrote {REPLAY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
