from scripts.run_l0_candidates import retrieval_admission_issues
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import ELEMENT_ISSUE, compile_issue_catalog_v2


def test_element_admission_filters_ranking_only_to_element_packets():
    issues, _ = compile_issue_catalog_v2(card_corpus())
    filtered = retrieval_admission_issues(issues, mode="elements")
    assert filtered
    assert len(filtered) < len(issues)
    assert {issue.function for issue in filtered} == {ELEMENT_ISSUE}


def test_all_admission_preserves_the_frozen_default():
    issues, _ = compile_issue_catalog_v2(card_corpus())
    assert retrieval_admission_issues(issues, mode="all") is issues
