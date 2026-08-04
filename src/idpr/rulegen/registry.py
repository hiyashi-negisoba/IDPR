"""Manifest-driven RuleIR registry and deterministic asset audit."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST_PATH = Path("data/rulegen/rule_ir_registry_manifest.json")
_ARTICLE_RE = re.compile(r"/(?:art(?P<english>\d+)|제(?P<korean>\d+)조)(?:[/#]|$)")
_SCL_RELATION_RE = re.compile(r"^\s*rel\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.MULTILINE)


@dataclass(frozen=True)
class RuleIRAssetSpec:
    unit_id: str
    rule_ir_path: str
    compiled_scl_path: str
    role_predicate: str
    query_relations: tuple[str, ...]
    shared_module: bool
    known_limitations: tuple[str, ...]


@dataclass(frozen=True)
class RuleIRRegistryEntry:
    unit_id: str
    article_ids: tuple[str, ...]
    role_predicate: dict[str, Any]
    commentary_inputs: tuple[dict[str, Any], ...]
    system_inputs: tuple[dict[str, Any], ...]
    query_relations: tuple[str, ...]
    compiled_scl_path: str
    rule_ir_path: str
    shared_module: bool
    known_limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PredicateIRMissing:
    unit_id: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def load_registry_manifest(
    root: Path = PROJECT_ROOT,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any]:
    manifest = _read_json(root / manifest_path)
    required = {"version", "scope", "missing_unit", "predicate_groups", "units"}
    missing = sorted(required - set(manifest))
    if missing:
        raise ValueError(f"{manifest_path}: missing manifest fields: {missing}")
    if not isinstance(manifest["units"], list):
        raise ValueError(f"{manifest_path}: units must be a list")
    return manifest


def load_asset_specs(
    root: Path = PROJECT_ROOT,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> tuple[RuleIRAssetSpec, ...]:
    manifest = load_registry_manifest(root, manifest_path)
    specs: list[RuleIRAssetSpec] = []
    unit_ids: set[str] = set()
    for index, item in enumerate(manifest["units"]):
        if not isinstance(item, dict):
            raise ValueError(f"{manifest_path}: units[{index}] must be an object")
        required = {
            "unit_id", "rule_ir_path", "compiled_scl_path", "role_predicate",
            "query_relations", "shared_module", "known_limitations",
        }
        missing = sorted(required - set(item))
        if missing:
            raise ValueError(f"{manifest_path}: units[{index}] missing fields: {missing}")
        unit_id = item["unit_id"]
        if not isinstance(unit_id, str) or not unit_id:
            raise ValueError(f"{manifest_path}: units[{index}].unit_id must be non-empty")
        if unit_id in unit_ids:
            raise ValueError(f"{manifest_path}: duplicate unit_id {unit_id}")
        unit_ids.add(unit_id)
        queries = item["query_relations"]
        if not isinstance(queries, list) or not queries or not all(
            isinstance(value, str) and value for value in queries
        ):
            raise ValueError(f"{manifest_path}: {unit_id}.query_relations must be non-empty")
        specs.append(RuleIRAssetSpec(
            unit_id=unit_id,
            rule_ir_path=item["rule_ir_path"],
            compiled_scl_path=item["compiled_scl_path"],
            role_predicate=item["role_predicate"],
            query_relations=tuple(queries),
            shared_module=item["shared_module"],
            known_limitations=tuple(item["known_limitations"]),
        ))
    for source_index, source in enumerate(manifest.get("unit_sources", [])):
        if not isinstance(source, dict):
            raise ValueError(
                f"{manifest_path}: unit_sources[{source_index}] must be an object"
            )
        source_manifest = _read_json(root / source["manifest_path"])
        role_signatures = _read_json(root / source["role_signatures_path"])
        signature_units = role_signatures.get("units", {})
        shared_kinds = set(source.get("shared_module_kinds", []))
        for unit in source_manifest.get("units", []):
            unit_id = unit["unit_id"]
            if unit_id in unit_ids:
                raise ValueError(f"{manifest_path}: duplicate unit_id {unit_id}")
            signature = signature_units.get(unit_id, {}).get("default", {})
            role_predicate = signature.get("predicate")
            tracks = signature.get("applies_to_tracks", [])
            if not role_predicate or not tracks:
                raise ValueError(
                    f"{source['role_signatures_path']}: incomplete default signature "
                    f"for {unit_id}"
                )
            queries = [
                f"{unit_id}_not_established",
                f"{unit_id}_undetermined",
                f"{unit_id}_conflict",
                *(f"{unit_id}_{track}_established" for track in tracks),
            ]
            unit_ids.add(unit_id)
            specs.append(RuleIRAssetSpec(
                unit_id=unit_id,
                rule_ir_path=source["rule_ir_path_template"].format(unit_id=unit_id),
                compiled_scl_path=source["compiled_scl_path_template"].format(
                    unit_id=unit_id
                ),
                role_predicate=role_predicate,
                query_relations=tuple(queries),
                shared_module=unit.get("kind") in shared_kinds,
                known_limitations=tuple(source.get("known_limitations", [])),
            ))
    return tuple(specs)


def _OPTIONAL_QUERY_RELATIONS(unit_id: str) -> tuple[str, ...]:
    """Relations a unit reports only when its cards produce them.

    Boundary and waiver rulings were compiled into the SCL but never queried,
    so "not this offence but that one" reached the answer as a bare 불성립 and
    the destination offence was lost.  A unit without such cards simply does not
    declare these predicates, hence the presence check at the call site.
    """
    return (
        f"{unit_id}_refers_to_crime",
        f"{unit_id}_boundary_shift",
        f"{unit_id}_requirement_waived",
    )


def build_registry(
    root: Path = PROJECT_ROOT,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, RuleIRRegistryEntry]:
    """Load registered assets without crime-specific code branches."""

    manifest = load_registry_manifest(root, manifest_path)
    selectors = manifest["predicate_groups"]
    entries: dict[str, RuleIRRegistryEntry] = {}
    for spec in load_asset_specs(root, manifest_path):
        payload = _read_json(root / spec.rule_ir_path)
        if payload.get("issue_tag") != spec.unit_id:
            raise ValueError(f"{spec.rule_ir_path}: issue_tag does not match {spec.unit_id}")
        predicates = payload.get("predicates", [])
        if not isinstance(predicates, list):
            raise ValueError(f"{spec.rule_ir_path}: predicates must be a list")
        by_id = {item.get("id"): item for item in predicates if isinstance(item, dict)}
        role_predicate = by_id.get(spec.role_predicate)
        if not isinstance(role_predicate, dict):
            raise ValueError(
                f"{spec.rule_ir_path}: missing role predicate {spec.role_predicate}"
            )
        entries[spec.unit_id] = RuleIRRegistryEntry(
            unit_id=spec.unit_id,
            article_ids=_article_ids(payload),
            role_predicate=role_predicate,
            commentary_inputs=_selected_predicates(predicates, selectors["commentary_inputs"]),
            system_inputs=_selected_predicates(predicates, selectors["system_inputs"]),
            query_relations=spec.query_relations + tuple(
                relation
                for relation in _OPTIONAL_QUERY_RELATIONS(spec.unit_id)
                if relation in by_id and relation not in spec.query_relations
            ),
            compiled_scl_path=spec.compiled_scl_path,
            rule_ir_path=spec.rule_ir_path,
            shared_module=spec.shared_module,
            known_limitations=spec.known_limitations,
        )
    return entries


def resolve_unit(
    unit_id: str,
    root: Path = PROJECT_ROOT,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> RuleIRRegistryEntry | PredicateIRMissing:
    manifest = load_registry_manifest(root, manifest_path)
    entry = build_registry(root, manifest_path).get(unit_id)
    if entry is not None:
        return entry
    missing = manifest["missing_unit"]
    return PredicateIRMissing(unit_id, missing["status"], missing["detail"])


def audit_rule_ir_assets(
    root: Path = PROJECT_ROOT,
    asset_specs: Iterable[RuleIRAssetSpec] | None = None,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any]:
    """Audit manifest declarations against RuleIR and compiled SCL assets."""

    manifest = load_registry_manifest(root, manifest_path)
    specs = tuple(asset_specs) if asset_specs is not None else load_asset_specs(root, manifest_path)
    selectors = manifest["predicate_groups"]
    report_units: list[dict[str, Any]] = []
    errors: list[str] = []
    for spec in specs:
        rule_ir_path = root / spec.rule_ir_path
        scl_path = root / spec.compiled_scl_path
        unit_errors: list[str] = []
        if not rule_ir_path.is_file():
            unit_errors.append(f"missing RuleIR: {spec.rule_ir_path}")
            report_units.append({"unit_id": spec.unit_id, "errors": unit_errors})
            errors.extend(f"{spec.unit_id}: {item}" for item in unit_errors)
            continue
        payload = _read_json(rule_ir_path)
        predicates = payload.get("predicates", [])
        if payload.get("issue_tag") != spec.unit_id:
            unit_errors.append("RuleIR issue_tag does not match registry unit_id")
        if not isinstance(predicates, list):
            unit_errors.append("RuleIR predicates is not a list")
            predicates = []
        predicate_ids = {
            item.get("id") for item in predicates if isinstance(item, dict) and item.get("id")
        }
        commentary_inputs = _selected_predicates(predicates, selectors["commentary_inputs"])
        system_inputs = _selected_predicates(predicates, selectors["system_inputs"])
        role = next(
            (item for item in predicates if isinstance(item, dict)
             and item.get("id") == spec.role_predicate),
            None,
        )
        if role is None:
            unit_errors.append(f"undeclared role predicate: {spec.role_predicate}")
        card_to_predicates: dict[str, list[str]] = {}
        for predicate in commentary_inputs:
            for card_id in predicate.get("norm_card_ids", []):
                if isinstance(card_id, str):
                    card_to_predicates.setdefault(card_id, []).append(str(predicate.get("id")))
        duplicates = {
            card_id: sorted(set(ids)) for card_id, ids in card_to_predicates.items()
            if len(set(ids)) != 1
        }
        if duplicates:
            unit_errors.append(f"duplicate norm_card_id to input predicate: {duplicates}")
        undeclared_queries = sorted(set(spec.query_relations) - predicate_ids)
        if undeclared_queries:
            unit_errors.append(f"undeclared query relation: {undeclared_queries}")
        if not scl_path.is_file():
            unit_errors.append(f"missing compiled SCL: {spec.compiled_scl_path}")
            scl_relations: set[str] = set()
        else:
            scl_relations = set(_SCL_RELATION_RE.findall(scl_path.read_text(encoding="utf-8")))
            missing_from_scl = sorted(set(spec.query_relations) - scl_relations)
            if missing_from_scl:
                unit_errors.append(f"query absent from compiled SCL: {missing_from_scl}")
        report_units.append({
            "unit_id": spec.unit_id,
            "article_ids": _article_ids(payload),
            "rule_ir_path": spec.rule_ir_path,
            "compiled_scl_path": spec.compiled_scl_path,
            "role_predicate": spec.role_predicate,
            "commentary_input_count": len(commentary_inputs),
            "system_input_count": len(system_inputs),
            "predicate_count": len(predicates),
            "query_relations": list(spec.query_relations),
            "compiled_relation_count": len(scl_relations),
            "errors": unit_errors,
        })
        errors.extend(f"{spec.unit_id}: {item}" for item in unit_errors)
    return {
        "version": manifest["version"],
        "scope": manifest["scope"],
        "status": "pass" if not errors else "fail",
        "units": report_units,
        "errors": errors,
    }


def _selected_predicates(
    predicates: Iterable[object], selector: Mapping[str, Any]
) -> tuple[dict[str, Any], ...]:
    return tuple(
        item for item in predicates if isinstance(item, dict)
        and all(item.get(key) == value for key, value in selector.items())
    )


def _article_ids(payload: Mapping[str, Any]) -> tuple[str, ...]:
    paths = payload.get("source_scope", {}).get("target_paths", [])
    return tuple(sorted({
        f"art{match.group('english') or match.group('korean')}"
        for path in paths if isinstance(path, str)
        for match in _ARTICLE_RE.finditer(path)
    }))


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload
