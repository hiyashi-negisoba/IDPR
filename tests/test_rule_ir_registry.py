from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from idpr.rulegen.registry import (
    DEFAULT_MANIFEST_PATH,
    PROJECT_ROOT,
    PredicateIRMissing,
    audit_rule_ir_assets,
    build_registry,
    load_asset_specs,
    load_registry_manifest,
    resolve_unit,
)
from scripts.audit_rule_ir_registry import render_markdown


def _copy_manifest(root: Path) -> None:
    target = root / DEFAULT_MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((PROJECT_ROOT / DEFAULT_MANIFEST_PATH).read_bytes())


def test_registry_is_derived_from_manifest_and_rule_ir_assets() -> None:
    manifest = load_registry_manifest()
    registry = build_registry()
    assert set(registry) == {spec.unit_id for spec in load_asset_specs()}
    assert len(registry) == len(load_asset_specs())
    assert len(registry) == 36

    for spec in load_asset_specs():
        entry = registry[spec.unit_id]
        payload = json.loads((PROJECT_ROOT / spec.rule_ir_path).read_text(encoding="utf-8"))
        predicate_ids = {item["id"] for item in payload["predicates"]}
        assert entry.role_predicate["id"] == spec.role_predicate
        # The entry adds boundary/waiver reports on top of the manifest's fixed
        # outcome queries, but only where the unit's cards actually declare them.
        assert set(spec.query_relations) <= set(entry.query_relations)
        assert set(entry.query_relations) <= predicate_ids
        for relation in set(entry.query_relations) - set(spec.query_relations):
            assert relation.startswith(f"{spec.unit_id}_")
            assert relation.endswith(
                ("_refers_to_crime", "_boundary_shift", "_requirement_waived",
                 "_assessment_standard", "_proof_standard", "_subtype_outcome",
                 "_post_outcome", "_outcome_detail")
            )
        assert entry.article_ids


def test_unregistered_unit_is_explicitly_missing_without_fallback() -> None:
    registered = build_registry()
    unit_id = f"{next(iter(registered))}_unregistered"
    result = resolve_unit(unit_id)
    assert isinstance(result, PredicateIRMissing)
    assert result.status == load_registry_manifest()["missing_unit"]["status"]


def test_committed_assets_pass_audit_and_markdown_is_deterministic() -> None:
    report = audit_rule_ir_assets()
    assert report["status"] == "pass"
    assert not report["errors"]
    assert load_registry_manifest()["missing_unit"]["status"] in report["scope"]
    assert render_markdown(report).startswith("# RuleIR registry audit\n")


def test_audit_rejects_duplicate_card_mapping_and_missing_scl(tmp_path: Path) -> None:
    _copy_manifest(tmp_path)
    spec = load_asset_specs()[0]
    payload = json.loads((PROJECT_ROOT / spec.rule_ir_path).read_text(encoding="utf-8"))
    selector = load_registry_manifest()["predicate_groups"]["commentary_inputs"]
    inputs = [
        item for item in payload["predicates"]
        if all(item.get(key) == value for key, value in selector.items())
    ]
    inputs[1]["norm_card_ids"] = list(inputs[1]["norm_card_ids"]) + [
        inputs[0]["norm_card_ids"][0]
    ]
    rule_path = tmp_path / Path(spec.rule_ir_path).name
    rule_path.write_text(json.dumps(payload), encoding="utf-8")
    broken_spec = replace(
        spec,
        rule_ir_path=rule_path.name,
        compiled_scl_path=f"missing/{Path(spec.compiled_scl_path).name}",
    )
    report = audit_rule_ir_assets(tmp_path, (broken_spec,))
    assert report["status"] == "fail"
    assert any("duplicate norm_card_id" in item for item in report["errors"])
    assert any("missing compiled SCL" in item for item in report["errors"])


def test_failed_audit_can_still_render_a_report(tmp_path: Path) -> None:
    _copy_manifest(tmp_path)
    spec = load_asset_specs()[0]
    report = audit_rule_ir_assets(
        tmp_path,
        (replace(spec, rule_ir_path=Path(spec.rule_ir_path).name),),
    )
    assert "missing RuleIR" in render_markdown(report)
