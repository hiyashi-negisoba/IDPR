"""Minimal neural-input profiles projected from reviewed RuleIR outcome rules.

Norm cards remain the provenance and interpretation layer.  The model assesses only
the component relations that an ``*_elements_satisfied`` rule actually consumes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from idpr.rulegen.registry import PROJECT_ROOT, build_registry


DEFAULT_CORE_PROFILE_PATH = Path("data/rulegen/rule_ir_core_profiles.json")


class CoreProfileError(ValueError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _track_id(unit_id: str, relation: str) -> str:
    if relation == f"{unit_id}_elements_satisfied":
        return "base"
    prefix = f"{unit_id}_"
    suffix = "_elements_satisfied"
    if not relation.startswith(prefix) or not relation.endswith(suffix):
        raise CoreProfileError(f"{unit_id}: invalid elements relation {relation}")
    return relation[len(prefix):-len(suffix)]


def build_core_profiles(root: Path = PROJECT_ROOT) -> dict[str, Any]:
    units: dict[str, Any] = {}
    for unit_id, entry in sorted(build_registry(root).items()):
        rule_ir_path = root / entry.rule_ir_path
        rule_ir = _read_json(rule_ir_path)
        predicates = {
            item["id"]: item
            for item in rule_ir.get("predicates", [])
            if isinstance(item, Mapping) and isinstance(item.get("id"), str)
        }
        rules = [item for item in rule_ir.get("rules", []) if isinstance(item, Mapping)]
        outcome_rules: dict[str, list[Mapping[str, Any]]] = {}
        for rule in rules:
            head = rule.get("head", {})
            relation = head.get("predicate") if isinstance(head, Mapping) else None
            if isinstance(relation, str) and relation.endswith("elements_satisfied"):
                outcome_rules.setdefault(relation, []).append(rule)
        if not outcome_rules:
            raise CoreProfileError(f"{unit_id}: no elements_satisfied outcome rule")

        component_ids: set[str] = set()
        tracks = []
        for relation, relation_rules in outcome_rules.items():
            paths = []
            for rule in relation_rules:
                components: list[str] = []
                dependencies: list[str] = []
                for atom in rule.get("body", []):
                    predicate_id = atom.get("predicate")
                    predicate = predicates.get(predicate_id, {})
                    if (
                        predicate.get("origin") == "commentary"
                        and predicate.get("role") == "derived"
                    ):
                        components.append(predicate_id)
                        component_ids.add(predicate_id)
                    elif (
                        isinstance(predicate_id, str)
                        and predicate_id.endswith("elements_satisfied")
                    ):
                        dependencies.append(predicate_id)
                    else:
                        raise CoreProfileError(
                            f"{unit_id}:{rule.get('id')}: outcome body contains "
                            f"non-component atom {predicate_id}"
                        )
                if not components and not dependencies:
                    raise CoreProfileError(
                        f"{unit_id}:{rule.get('id')}: empty core outcome path"
                    )
                paths.append({
                    "rule_id": rule.get("id"),
                    "components": components,
                    "depends_on_elements": dependencies,
                })
            tracks.append({
                "track_id": _track_id(unit_id, relation),
                "elements_relation": relation,
                "paths": paths,
            })

        model_inputs = []
        for component_id in sorted(component_ids):
            predicate = predicates[component_id]
            implementing = [
                rule for rule in rules
                if rule.get("head", {}).get("predicate") == component_id
            ]
            source_refs: list[dict[str, Any]] = []
            norm_card_ids: list[str] = []
            for rule in implementing:
                source_refs.extend(
                    dict(item) for item in rule.get("source_refs", [])
                    if isinstance(item, Mapping)
                )
                norm_card_ids.extend(
                    str(item) for item in rule.get("norm_card_ids", [])
                    if isinstance(item, str)
                )
            model_inputs.append({
                "predicate_id": component_id,
                "definition": str(predicate.get("definition", component_id)),
                "arguments": [dict(item) for item in predicate.get("arguments", [])],
                "authority_card_ids": list(dict.fromkeys(norm_card_ids)),
                "source_refs": list({
                    json.dumps(item, ensure_ascii=False, sort_keys=True): item
                    for item in source_refs
                }.values()),
            })

        units[unit_id] = {
            "unit_id": unit_id,
            "article_ids": list(entry.article_ids),
            "role_contract": {
                "predicate": entry.role_predicate["id"],
                "definition": str(entry.role_predicate.get("definition", "")),
                "arguments": [dict(item) for item in entry.role_predicate["arguments"]],
            },
            "tracks": sorted(tracks, key=lambda item: item["track_id"]),
            "model_input_predicates": model_inputs,
            "detailed_card_predicates": {
                "classification": "context_and_provenance_not_model_input",
                "count": len(entry.commentary_inputs),
            },
            "rule_ir_path": entry.rule_ir_path,
            "rule_ir_sha256": _sha256(rule_ir_path),
            "compiled_scl_path": entry.compiled_scl_path,
            "shared_module": entry.shared_module,
        }
    return {
        "version": "1.0.0",
        "contract": {
            "model_assesses": "core_component_predicates_only",
            "norm_cards": "context_and_provenance",
            "derived_relations": "host_and_scallop_only",
            "profile_source": "committed_rule_ir_elements_satisfied_rules",
        },
        "units": units,
    }


def load_core_profiles(
    root: Path = PROJECT_ROOT,
    path: Path = DEFAULT_CORE_PROFILE_PATH,
    *,
    verify_sources: bool = True,
) -> dict[str, Any]:
    payload = _read_json(root / path)
    if payload.get("version") != "1.0.0" or not isinstance(payload.get("units"), dict):
        raise CoreProfileError(f"{path}: invalid core profile registry")
    if verify_sources:
        for unit_id, profile in payload["units"].items():
            source = root / profile["rule_ir_path"]
            if _sha256(source) != profile["rule_ir_sha256"]:
                raise CoreProfileError(f"{unit_id}: core profile source hash drift")
    return payload
