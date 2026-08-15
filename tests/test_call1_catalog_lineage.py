from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.routing import RouterCatalogEntry, router_catalog, router_catalog_fingerprint

ROOT = Path(__file__).resolve().parents[1]


def _planner_module():
    path = ROOT / "scripts/run_v2_evaluation_instance_planner.py"
    spec = importlib.util.spec_from_file_location("run_v2_evaluation_instance_planner", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_router_catalog_fingerprint_owns_visible_metadata_only() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    catalog = router_catalog(registry)
    original = router_catalog_fingerprint(catalog)
    first = catalog[0]
    changed = (
        RouterCatalogEntry(
            first.definition_id,
            first.kind,
            first.display_name + " changed",
            first.statutory_refs,
        ),
        *catalog[1:],
    )
    assert router_catalog_fingerprint(changed) != original


def test_a_new_offense_family_invalidates_an_old_call1_manifest() -> None:
    """routing universe가 바뀌면 옛 Call 1 산출물은 더 이상 lineage를 통과하면 안 된다.

    이 테스트는 원래 반대를 지켰다 -- downstream이 바뀌어도 catalog id가 같으면 옛 manifest를
    그대로 쓸 수 있다는 것. 2026-08-15에 폭행죄 family가 저작되면서 catalog 자체가 바뀌었고,
    그때는 재사용이 아니라 **재실행**이 맞다. 통과해 버리면 없는 죄로 라우팅된 seed 위에
    새 rulebase를 얹게 된다.
    """
    planner = _planner_module()
    manifest = json.loads(
        (ROOT / "experiments/v2_restart_rebuild/call1/router_output.manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["registry_sha256"] != planner._registry_sha256(
        ROOT / "data/v2/definitions"
    )

    with pytest.raises(ValueError, match="catalog"):
        planner._verify_lineage(
            manifest,
            ROOT / "data/v2/definitions",
            ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
            ROOT / "data/eval/kcl_substantive_case_ids.txt",
        )


def test_legacy_call1_manifest_rejects_catalog_universe_change() -> None:
    planner = _planner_module()
    manifest = json.loads(
        (ROOT / "experiments/v2_restart_rebuild/call1/router_output.manifest.json").read_text(
            encoding="utf-8"
        )
    )
    manifest["catalog_definition_ids"] = manifest["catalog_definition_ids"][:-1]
    with pytest.raises(ValueError, match="catalog_definition_ids"):
        planner._verify_lineage(
            manifest,
            ROOT / "data/v2/definitions",
            ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
            ROOT / "data/eval/kcl_substantive_case_ids.txt",
        )
