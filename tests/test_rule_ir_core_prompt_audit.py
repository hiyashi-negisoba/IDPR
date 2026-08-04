from __future__ import annotations

from scripts.audit_rule_ir_core_prompts import audit


def test_normalized_prompt_preflight_seals_the_small_contract() -> None:
    report = audit()
    assert report["status"] == "pass"
    assert report["api_calls"] == 0
    assert report["predicate_boundary"] == {
        "units": 36,
        "detailed_card_predicates": 1652,
        "core_model_predicates": 245,
        "fraud": [88, 10],
        "theft": [66, 6],
    }
    assert report["schemas"]["unsupported_guidance_keywords_present"] == []
    assert report["search_contract"]["initial_issue_search"] is False
    assert report["search_contract"]["predicate_conditioned_context"] is True
