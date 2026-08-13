import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _audit_module():
    path = ROOT / "scripts/audit_v2_doctrine_card_bridge.py"
    spec = importlib.util.spec_from_file_location("audit_v2_doctrine_card_bridge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_article_join_is_law_aware_and_preserves_subarticle() -> None:
    audit = _audit_module()
    assert audit._article_key("001692", "제329조") == "art329"
    assert audit._article_key("001692", "제258조의2") == "art2582_2"
    assert audit._article_key("001671", "제329조") is None


def test_kcl26_card_audit_does_not_claim_symbolic_activation() -> None:
    module = _audit_module()
    audit = module.build_audit(
        gold_path=ROOT / "data/v2/gold_occurrences.jsonl",
        manifest_path=ROOT
        / "data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl",
        cards_path=ROOT / "data/rulebase/card_catalog_v2.json",
    )

    assert audit["scope"]["case_count"] == 26
    assert audit["scope"]["runtime_use_of_kcl_issue_tags"] is False
    assert audit["summary"]["explicit_symbolic_bridge_count"] == 0
    assert all(
        row["symbolic_bridge_status"] == "NOT_AUTHORED"
        for row in audit["issue_tags"]
    )
