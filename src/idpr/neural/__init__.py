"""Source-grounded neural contracts for the fraud-to-Scallop pipeline."""

from __future__ import annotations

import json
import struct
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = PROJECT_ROOT / "docs/contracts"
REQUIRED_ROLES = (
    "defendant",
    "deceived_person",
    "disposer",
    "property_owner",
    "beneficiary",
)
ALLOWED_ASSESSMENT_STATUSES = {"satisfied", "not_satisfied", "unknown"}

# This is one reviewed legal path, not a prediction by the router. Other profiles
# receive their own explicit plans instead of silently dropping common components.
LOAN_PURPOSE_CARD_PLAN = (
    "general_object.fraud.element.object-other-possessed-other-property",
    "deception.fraud.standard.loan-purpose-materiality",
    "fraud_mistake.error_definition",
    "fraud_mistake.error_disposition_motivation",
    "fraud_mistake.disposition_definition",
    "fraud_damage_acquisition.delivery_of_property",
    "fraud_mistake.sequential_causation",
    "fraud_stages_participation.completion_deception_disposition_transfer",
    "deception.fraud.standard.intent-to-defraud-loan-inference",
    "fraud_intent.time_of_conduct",
    "fraud_mistake.gain_purpose",
    "fraud_intent.no_disposition_inducement_intent",
    "fraud_mistake.deceived_disposer_identity",
)


class NeuralContractError(ValueError):
    """Raised when a neural output cannot safely enter symbolic reasoning."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("Invalid neural artifact:\n- " + "\n- ".join(self.errors))


class ModelCacheError(RuntimeError):
    """Raised before vLLM starts when a local model snapshot is incomplete."""


def validate_fraud_fact_graph(
    payload: Mapping[str, Any], case: Mapping[str, Any]
) -> None:
    errors = _schema_errors(payload, "fraud_fact_graph.schema.json")
    if payload.get("case_id") != case.get("case_id"):
        errors.append("case_id does not match the requested case")

    actors = payload.get("actors", [])
    entity_ids: set[str] = set()
    mention_owners: dict[str, list[str]] = {}
    role_owners: dict[str, list[str]] = {role: [] for role in REQUIRED_ROLES}
    if payload.get("target_issue_id") != case.get("target", {}).get("issue_id"):
        errors.append("target_issue_id does not match the requested target")

    case_text = str(case.get("case_text", ""))
    for index, actor in enumerate(actors):
        entity_id = actor.get("entity_id", "")
        if entity_id in entity_ids:
            errors.append(f"duplicate actor entity_id {entity_id}")
        entity_ids.add(entity_id)
        for mention in actor.get("mentions", []):
            if mention not in case_text:
                errors.append(f"actors[{index}] mention is not in question_text: {mention}")
            mention_owners.setdefault(mention, []).append(entity_id)
        for role in actor.get("roles", []):
            if role in role_owners:
                role_owners[role].append(entity_id)
    for role, owners in role_owners.items():
        if len(owners) != 1:
            errors.append(f"role {role} must resolve to exactly one entity, got {owners}")
    for mention, owners in mention_owners.items():
        unique_owners = list(dict.fromkeys(owners))
        if len(unique_owners) != 1:
            errors.append(
                f"actor mention {mention} resolves to multiple entities: {unique_owners}"
            )

    defendant_hint = str(case.get("target", {}).get("defendant_hint", ""))
    defendant_ids = role_owners.get("defendant", [])
    if defendant_hint and len(defendant_ids) == 1:
        defendant = next(
            (actor for actor in actors if actor.get("entity_id") == defendant_ids[0]),
            {},
        )
        if defendant_hint not in defendant.get("mentions", []):
            errors.append("resolved defendant does not include defendant_hint")

    target_transaction = case.get("target", {}).get("target_transaction", {})
    transaction_role_hints = {
        "disposer": str(target_transaction.get("transferor_hint", "")),
        "beneficiary": str(
            target_transaction.get("immediate_recipient_hint", "")
        ),
    }
    actors_by_id = {actor.get("entity_id", ""): actor for actor in actors}
    for role, hint in transaction_role_hints.items():
        owners = role_owners.get(role, [])
        if hint and len(owners) == 1:
            owner = actors_by_id.get(owners[0], {})
            if hint not in owner.get("mentions", []):
                errors.append(
                    f"resolved {role} does not match target transaction hint {hint}"
                )

    fact_ids: set[str] = set()
    for index, fact in enumerate(payload.get("facts", [])):
        fact_id = fact.get("fact_id", "")
        if fact_id in fact_ids:
            errors.append(f"duplicate fact_id {fact_id}")
        fact_ids.add(fact_id)
        quote = fact.get("source_quote", "")
        if quote not in case_text:
            errors.append(f"facts[{index}].source_quote is not an exact case substring")
        unknown_participants = sorted(set(fact.get("participants", [])) - entity_ids)
        if unknown_participants:
            errors.append(
                f"facts[{index}] references unknown participants: {unknown_participants}"
            )

    allowed_profiles = set(case.get("allowed_profiles", []))
    unexpected_profiles = sorted(set(payload.get("profiles", [])) - allowed_profiles)
    if unexpected_profiles:
        errors.append(f"profiles are outside the case contract: {unexpected_profiles}")
    if "loan_purpose" in allowed_profiles and "loan_purpose" not in payload.get(
        "profiles", []
    ):
        errors.append("the KCL purpose-deception target must activate loan_purpose")

    if errors:
        raise NeuralContractError(errors)


def select_fraud_card_plan(fact_graph: Mapping[str, Any]) -> list[str]:
    profiles = set(fact_graph.get("profiles", []))
    if "loan_purpose" in profiles:
        return list(LOAN_PURPOSE_CARD_PLAN)
    raise NeuralContractError(
        [f"no reviewed assessment plan for profiles: {sorted(profiles)}"]
    )


def build_authority_packet(
    card_ids: Sequence[str], norm_card_set: Mapping[str, Any]
) -> list[dict[str, Any]]:
    cards_by_id = {
        card.get("id", ""): card for card in norm_card_set.get("cards", [])
    }
    missing = sorted(set(card_ids) - set(cards_by_id))
    if missing:
        raise NeuralContractError([f"unknown NormCards in plan: {missing}"])
    packet: list[dict[str, Any]] = []
    for card_id in card_ids:
        card = cards_by_id[card_id]
        packet.append(
            {
                "card_id": card_id,
                "proposition": card["proposition"],
                "polarity": card["polarity"],
                "formalization": card["formalization"],
                "sources": [
                    {
                        "comment_id": ref["comment_id"],
                        "section_path": ref["section_path"],
                        "quote": ref["quote"],
                    }
                    for ref in card["source_refs"]
                ],
            }
        )
    return packet


def validate_fraud_assessment_bundle(
    payload: Mapping[str, Any],
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    selected_card_ids: Sequence[str],
    authority_packet: Sequence[Mapping[str, Any]],
) -> None:
    errors = _schema_errors(payload, "fraud_assessment_bundle.schema.json")
    if payload.get("case_id") != case.get("case_id"):
        errors.append("case_id does not match the requested case")
    if list(payload.get("selected_card_ids", [])) != list(selected_card_ids):
        errors.append(
            "selected_card_ids must match the host-selected plan in exact order"
        )

    fact_ids = {fact.get("fact_id", "") for fact in fact_graph.get("facts", [])}
    authority_by_card = {
        item["card_id"]: {source["comment_id"] for source in item["sources"]}
        for item in authority_packet
    }
    assessment_ids: set[str] = set()
    assessed_cards: set[str] = set()
    for index, assessment in enumerate(payload.get("assessments", [])):
        assessment_id = assessment.get("assessment_id", "")
        card_id = assessment.get("card_id", "")
        if assessment_id in assessment_ids:
            errors.append(f"duplicate assessment_id {assessment_id}")
        assessment_ids.add(assessment_id)
        if card_id in assessed_cards:
            errors.append(f"duplicate assessment for card {card_id}")
        assessed_cards.add(card_id)
        referenced_facts = set(assessment.get("basis_fact_ids", [])) | set(
            assessment.get("counter_fact_ids", [])
        )
        unknown_facts = sorted(referenced_facts - fact_ids)
        if unknown_facts:
            errors.append(
                f"assessments[{index}] references unknown facts: {unknown_facts}"
            )
        status = assessment.get("status")
        if status in {"satisfied", "not_satisfied"} and not assessment.get(
            "basis_fact_ids"
        ):
            errors.append(
                f"assessments[{index}] {status} requires at least one basis fact"
            )
        if status == "unknown" and not assessment.get("missing_facts"):
            errors.append(f"assessments[{index}] unknown requires missing_facts")
        allowed_authorities = authority_by_card.get(card_id, set())
        supplied_authorities = set(assessment.get("authority_comment_ids", []))
        if not supplied_authorities <= allowed_authorities:
            errors.append(
                f"assessments[{index}] cites authority outside its NormCard sources"
            )

    if assessed_cards != set(selected_card_ids):
        missing = sorted(set(selected_card_ids) - assessed_cards)
        extra = sorted(assessed_cards - set(selected_card_ids))
        errors.append(f"assessment coverage mismatch: missing={missing}, extra={extra}")
    if errors:
        raise NeuralContractError(errors)


def build_scallop_scenario(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    assessment_bundle: Mapping[str, Any],
    selected_card_ids: Sequence[str],
    authority_packet: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validate_fraud_fact_graph(fact_graph, case)
    validate_fraud_assessment_bundle(
        assessment_bundle,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected_card_ids,
        authority_packet=authority_packet,
    )
    role_to_entity = {
        role: actor["entity_id"]
        for actor in fact_graph["actors"]
        for role in actor["roles"]
    }
    case_id = str(fact_graph["case_id"])
    defendant = role_to_entity["defendant"]
    deceived = role_to_entity["deceived_person"]
    owner = role_to_entity["property_owner"]
    beneficiary = role_to_entity["beneficiary"]
    actor_tuple = list(dict.fromkeys(role_to_entity[role] for role in REQUIRED_ROLES))
    distinct_pairs = [
        [left, right]
        for left_index, left in enumerate(actor_tuple)
        for right in actor_tuple[left_index + 1 :]
    ]
    return {
        "scenario_id": case_id,
        "case_id": case_id,
        "defendant_id": defendant,
        "deceived_person_id": deceived,
        "disposer_id": role_to_entity["disposer"],
        "property_owner_id": owner,
        "beneficiary_id": beneficiary,
        "selected_card_ids": list(selected_card_ids),
        "assessments": [
            {
                "assessment_id": assessment["assessment_id"],
                "card_id": assessment["card_id"],
                "status": assessment["status"],
                "provable": True,
            }
            for assessment in assessment_bundle["assessments"]
        ],
        "distinct_entities": distinct_pairs,
        "close_case": True,
    }


def audit_local_model_snapshot(snapshot: Path) -> dict[str, Any]:
    errors: list[str] = []
    config_path = snapshot / "config.json"
    index_path = snapshot / "model.safetensors.index.json"
    if not config_path.is_file():
        errors.append("config.json is missing")
    if not index_path.is_file():
        errors.append("model.safetensors.index.json is missing")
    if errors:
        raise ModelCacheError("; ".join(errors))

    config = json.loads(config_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if config.get("model_type") != "gemma4":
        errors.append(f"expected model_type gemma4, got {config.get('model_type')}")
    architectures = config.get("architectures", [])
    if "Gemma4ForConditionalGeneration" not in architectures:
        errors.append(f"unexpected architectures: {architectures}")
    shards = sorted(set(index.get("weight_map", {}).values()))
    if not shards:
        errors.append("model index contains no weight shards")
    shard_records: list[dict[str, Any]] = []
    actual_tensor_bytes = 0
    for shard in shards:
        path = snapshot / shard
        exists = path.is_file()
        size = path.stat().st_size if exists else 0
        if not exists or size == 0:
            errors.append(f"weight shard is missing or empty: {shard}")
        tensor_bytes = 0
        if exists and size:
            try:
                tensor_bytes = _safetensors_data_bytes(path)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"invalid safetensors shard {shard}: {exc}")
        actual_tensor_bytes += tensor_bytes
        shard_records.append(
            {
                "name": shard,
                "exists": exists,
                "file_bytes": size,
                "tensor_bytes": tensor_bytes,
            }
        )
    expected_bytes = int(index.get("metadata", {}).get("total_size", 0))
    actual_file_bytes = sum(record["file_bytes"] for record in shard_records)
    if expected_bytes and actual_tensor_bytes != expected_bytes:
        errors.append(
            "tensor bytes mismatch: "
            f"expected {expected_bytes}, found {actual_tensor_bytes}"
        )
    for filename in ("tokenizer.json", "tokenizer_config.json"):
        if not (snapshot / filename).is_file():
            errors.append(f"{filename} is missing")
    result = {
        "snapshot": str(snapshot),
        "model_type": config.get("model_type"),
        "architectures": architectures,
        "expected_tensor_bytes": expected_bytes,
        "actual_tensor_bytes": actual_tensor_bytes,
        "actual_file_bytes": actual_file_bytes,
        "shards": shard_records,
        "complete": not errors,
        "errors": errors,
    }
    if errors:
        raise ModelCacheError(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def _safetensors_data_bytes(path: Path) -> int:
    file_size = path.stat().st_size
    with path.open("rb") as handle:
        header_size_bytes = handle.read(8)
        if len(header_size_bytes) != 8:
            raise ValueError("missing 8-byte header length")
        header_size = struct.unpack("<Q", header_size_bytes)[0]
        if header_size <= 0 or header_size > file_size - 8:
            raise ValueError(f"invalid header size {header_size}")
        header = json.loads(handle.read(header_size))
    offsets = [
        value.get("data_offsets")
        for key, value in header.items()
        if key != "__metadata__" and isinstance(value, Mapping)
    ]
    if not offsets or any(
        not isinstance(offset, list)
        or len(offset) != 2
        or not all(isinstance(item, int) for item in offset)
        for offset in offsets
    ):
        raise ValueError("missing or malformed tensor data_offsets")
    data_bytes = max(offset[1] for offset in offsets)
    if file_size != 8 + header_size + data_bytes:
        raise ValueError("file length does not match safetensors header offsets")
    return data_bytes


@lru_cache(maxsize=None)
def contract_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((CONTRACT_ROOT / schema_name).read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _contract_validator(schema_name: str) -> Draft202012Validator:
    schema = contract_schema(schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _schema_errors(payload: Mapping[str, Any], schema_name: str) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        _contract_validator(schema_name).iter_errors(payload),
        key=lambda item: list(item.absolute_path),
    ):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        errors.append(f"{path}: {error.message}")
    return errors
