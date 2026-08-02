"""Legacy fraud-pilot planning contracts retained for experiment reproduction."""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = PROJECT_ROOT / "docs/contracts"
DEFAULT_REGISTRY_PATH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_m5_reasoning_plan_registry.json"
)
FRAUD_ROLES = (
    "defendant",
    "deceived_person",
    "disposer",
    "property_owner",
    "beneficiary",
)


class FraudPlanningError(ValueError):
    """Raised when a case or host reasoning plan is not safe to compile."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("Invalid fraud planning artifact:\n- " + "\n- ".join(self.errors))


@lru_cache(maxsize=None)
def _schema(filename: str) -> dict[str, Any]:
    return json.loads((CONTRACT_ROOT / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def load_fraud_plan_registry(
    path: Path = DEFAULT_REGISTRY_PATH,
) -> dict[str, Any]:
    registry = json.loads(path.read_text(encoding="utf-8"))
    validate_fraud_plan_registry(registry)
    return registry


def validate_fraud_plan_registry(registry: Mapping[str, Any]) -> None:
    errors = _schema_errors(registry, "fraud_reasoning_plan_registry.schema.json")
    core = registry.get("core", {})
    unit_ids: set[str] = set()
    card_units: dict[str, str] = {}
    for unit_index, unit in enumerate(core.get("units", [])):
        unit_id = str(unit.get("unit_id", ""))
        if unit_id in unit_ids:
            errors.append(f"core contains duplicate unit {unit_id}")
        unit_ids.add(unit_id)
        _validate_card_specs(
            unit.get("cards", []),
            label=f"core.units[{unit_index}]",
            unit_id=unit_id,
            card_units=card_units,
            errors=errors,
        )

    profile_ids: set[str] = set()
    for profile_index, profile in enumerate(registry.get("profiles", [])):
        profile_id = str(profile.get("profile_id", ""))
        if profile_id in profile_ids:
            errors.append(f"duplicate profile_id {profile_id}")
        profile_ids.add(profile_id)
        addition_units: set[str] = set()
        local_card_units: dict[str, str] = {}
        for addition_index, addition in enumerate(profile.get("unit_additions", [])):
            unit_id = str(addition.get("unit_id", ""))
            if unit_id not in unit_ids:
                errors.append(
                    f"profiles[{profile_index}].unit_additions[{addition_index}] "
                    f"references unknown core unit {unit_id}"
                )
            if unit_id in addition_units:
                errors.append(f"profile {profile_id} repeats unit addition {unit_id}")
            addition_units.add(unit_id)
            _validate_card_specs(
                addition.get("cards", []),
                label=(
                    f"profiles[{profile_index}].unit_additions[{addition_index}]"
                ),
                unit_id=unit_id,
                card_units=local_card_units,
                errors=errors,
            )

    referenced_profiles = {
        profile_id
        for unit in core.get("units", [])
        for card in unit.get("cards", [])
        for field in ("requires_profiles", "unless_profiles")
        for profile_id in card.get(field, [])
    }
    unknown_references = sorted(referenced_profiles - profile_ids)
    if unknown_references:
        errors.append(
            f"core cards reference unregistered profiles: {unknown_references}"
        )
    if errors:
        raise FraudPlanningError(errors)


def _validate_card_specs(
    cards: Sequence[Mapping[str, Any]],
    *,
    label: str,
    unit_id: str,
    card_units: dict[str, str],
    errors: list[str],
) -> None:
    for card_index, card in enumerate(cards):
        card_id = str(card.get("card_id", ""))
        previous_unit = card_units.get(card_id)
        if previous_unit is not None:
            errors.append(
                f"{label}.cards[{card_index}] repeats card {card_id} "
                f"already assigned to {previous_unit}"
            )
        card_units[card_id] = unit_id
        required = set(card.get("requires_profiles", []))
        excluded = set(card.get("unless_profiles", []))
        overlap = sorted(required & excluded)
        if overlap:
            errors.append(
                f"{label}.cards[{card_index}] both requires and excludes {overlap}"
            )


def validate_fraud_case(
    case: Mapping[str, Any], registry: Mapping[str, Any] | None = None
) -> None:
    errors = _schema_errors(case, "fraud_case.schema.json")
    allowed_profiles = set(case.get("allowed_profiles", []))
    required_profiles = set(case.get("required_profiles", []))
    if not required_profiles <= allowed_profiles:
        errors.append(
            "required_profiles must be a subset of allowed_profiles: "
            f"{sorted(required_profiles - allowed_profiles)}"
        )
    role_hints = case.get("target", {}).get("role_hints", {})
    case_text = str(case.get("case_text", ""))
    for role in FRAUD_ROLES:
        hint = role_hints.get(role, "")
        if hint and hint not in case_text:
            errors.append(f"target.role_hints.{role} is not present in case_text: {hint}")

    active_registry = registry or load_fraud_plan_registry()
    if case.get("rule_set_id") != active_registry.get("rule_set_id"):
        errors.append("case rule_set_id differs from reasoning-plan registry")
    registered_profiles = {
        profile["profile_id"] for profile in active_registry.get("profiles", [])
    }
    unsupported_required = sorted(required_profiles - registered_profiles)
    if unsupported_required:
        errors.append(
            f"required_profiles are not implemented by the registry: {unsupported_required}"
        )
    if errors:
        raise FraudPlanningError(errors)


def fraud_case_role_hints(case: Mapping[str, Any]) -> dict[str, str]:
    """Return canonical target role hints, with legacy-case fallbacks."""

    target = case.get("target", {})
    configured = target.get("role_hints", {})
    if configured:
        return {role: str(configured.get(role, "")) for role in FRAUD_ROLES}

    transaction = target.get("target_transaction", {})
    counterparty = str(target.get("counterparty_hint", ""))
    return {
        "defendant": str(target.get("defendant_hint", "")),
        "deceived_person": counterparty,
        "disposer": str(transaction.get("transferor_hint", counterparty)),
        "property_owner": counterparty,
        "beneficiary": str(transaction.get("immediate_recipient_hint", "")),
    }


def fraud_case_answer_subject(case: Mapping[str, Any]) -> str:
    target = case.get("target", {})
    configured = str(target.get("answer_subject", "")).strip()
    if configured:
        return configured
    roles = fraud_case_role_hints(case)
    counterparty = str(target.get("counterparty_hint", roles["deceived_person"]))
    return f"{roles['defendant']}의 {counterparty}에 대한 사기죄"


def select_fraud_reasoning_plan(
    fact_graph: Mapping[str, Any],
    *,
    case: Mapping[str, Any] | None = None,
    registry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose the always-on fraud core with zero or more active profiles."""

    active_registry = registry or load_fraud_plan_registry()
    profile_names = list(dict.fromkeys(fact_graph.get("profiles", [])))
    profile_set = set(profile_names)
    registered = {
        profile["profile_id"]: profile
        for profile in active_registry.get("profiles", [])
    }

    if case is not None:
        validate_fraud_case(case, active_registry)
        unexpected_profiles = profile_set - set(case.get("allowed_profiles", []))
        if unexpected_profiles:
            raise FraudPlanningError(
                [
                    "fact graph profiles are outside case contract: "
                    f"{sorted(unexpected_profiles)}"
                ]
            )
        missing_required = set(case.get("required_profiles", [])) - profile_set
        if missing_required:
            raise FraudPlanningError(
                [f"fact graph omitted required profiles: {sorted(missing_required)}"]
            )

    unsupported = sorted(profile_set - set(registered))
    if unsupported:
        raise FraudPlanningError(
            [f"no reviewed profile additions for active profiles: {unsupported}"]
        )

    core = copy.deepcopy(active_registry["core"])
    units = core["units"]
    units_by_id = {unit["unit_id"]: unit for unit in units}
    for unit in units:
        unit["cards"] = [
            _strip_card_routing(card)
            for card in unit["cards"]
            if _card_is_active(card, profile_set)
        ]

    queries = list(core["retrieval_query_templates"])
    applied_profiles: list[str] = []
    for profile_spec in active_registry["profiles"]:
        profile_id = profile_spec["profile_id"]
        if profile_id not in profile_set:
            continue
        applied_profiles.append(profile_id)
        queries.extend(profile_spec["retrieval_query_templates"])
        for addition in profile_spec["unit_additions"]:
            target_unit = units_by_id[addition["unit_id"]]
            existing = {
                card["card_id"]: card for card in target_unit.get("cards", [])
            }
            for card in addition["cards"]:
                if not _card_is_active(card, profile_set):
                    continue
                normalized = _strip_card_routing(card)
                previous = existing.get(normalized["card_id"])
                if previous is not None and previous != normalized:
                    raise FraudPlanningError(
                        [
                            f"profile {profile_id} conflicts on card "
                            f"{normalized['card_id']}"
                        ]
                    )
                if previous is None:
                    target_unit["cards"].append(normalized)
                    existing[normalized["card_id"]] = normalized

    plan_id = "fraud_core"
    if applied_profiles:
        plan_id += "__" + "__".join(applied_profiles)
    plan = {
        "plan_id": plan_id,
        "description": core["description"],
        "active_profiles": applied_profiles,
        "retrieval_query_templates": list(dict.fromkeys(queries)),
        "units": units,
    }
    _validate_composed_plan(plan)
    return plan


def _card_is_active(card: Mapping[str, Any], profiles: set[str]) -> bool:
    required = set(card.get("requires_profiles", []))
    excluded = set(card.get("unless_profiles", []))
    return required <= profiles and not (excluded & profiles)


def _strip_card_routing(card: Mapping[str, Any]) -> dict[str, Any]:
    stripped: dict[str, Any] = {
        "card_id": str(card["card_id"]),
        "satisfied_when": str(card["satisfied_when"]),
    }
    query = card.get("neural_query")
    if query is not None:
        stripped["neural_query"] = {
            "proposition": str(query["proposition"]),
            "card_status_when_query_satisfied": str(
                query["card_status_when_query_satisfied"]
            ),
        }
    return stripped


def _validate_composed_plan(plan: Mapping[str, Any]) -> None:
    errors: list[str] = []
    card_units: dict[str, str] = {}
    for unit in plan.get("units", []):
        unit_id = str(unit.get("unit_id", ""))
        if not unit.get("cards"):
            errors.append(f"composed unit {unit_id} has no cards")
        for card in unit.get("cards", []):
            card_id = str(card.get("card_id", ""))
            previous = card_units.get(card_id)
            if previous is not None and previous != unit_id:
                errors.append(
                    f"composed card {card_id} appears in {previous} and {unit_id}"
                )
            card_units[card_id] = unit_id
    if errors:
        raise FraudPlanningError(errors)


def reasoning_plan_card_ids(plan: Mapping[str, Any]) -> list[str]:
    return [
        card["card_id"]
        for unit in plan.get("units", [])
        for card in unit.get("cards", [])
    ]


def reasoning_plan_neural_queries(
    plan: Mapping[str, Any],
) -> dict[str, dict[str, str]]:
    """Return the affirmative proposition the model judges in place of each
    card whose own wording runs opposite to the status it must report."""

    return {
        card["card_id"]: dict(card["neural_query"])
        for unit in plan.get("units", [])
        for card in unit.get("cards", [])
        if card.get("neural_query")
    }


def build_fraud_assessment_context(
    fact_graph: Mapping[str, Any],
    *,
    case: Mapping[str, Any],
    selected_card_ids: Sequence[str] | None = None,
    registry: Mapping[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Return IRAC grouping metadata, not card-specific adjudication questions."""

    plan = select_fraud_reasoning_plan(fact_graph, case=case, registry=registry)
    contexts: dict[str, dict[str, str]] = {}
    for unit in plan["units"]:
        issue = render_reasoning_plan_text(unit["issue_template"], case)
        for card in unit["cards"]:
            contexts[card["card_id"]] = {
                "card_id": card["card_id"],
                "unit_id": unit["unit_id"],
                "unit_issue": issue,
            }
    ordered_ids = (
        list(selected_card_ids)
        if selected_card_ids is not None
        else reasoning_plan_card_ids(plan)
    )
    missing = [card_id for card_id in ordered_ids if card_id not in contexts]
    if missing:
        raise FraudPlanningError(
            [f"assessment context requested cards outside composed plan: {missing}"]
        )
    return [contexts[card_id] for card_id in ordered_ids]


def render_reasoning_plan_text(template: str, case: Mapping[str, Any]) -> str:
    roles = fraud_case_role_hints(case)
    target = case.get("target", {})
    transaction = target.get("target_transaction", {})
    context = {
        **roles,
        "counterparty": str(target.get("counterparty_hint", roles["deceived_person"])),
        "transaction_description": str(transaction.get("description", "대상 거래")),
        "answer_subject": fraud_case_answer_subject(case),
    }
    try:
        return template.format_map(context)
    except KeyError as exc:
        raise FraudPlanningError(
            [f"unknown reasoning-plan template variable: {exc.args[0]}"]
        ) from exc


def _schema_errors(payload: Mapping[str, Any], filename: str) -> list[str]:
    validator = Draft202012Validator(_schema(filename))
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(
            validator.iter_errors(payload),
            key=lambda item: tuple(str(part) for part in item.path),
        )
    ]
