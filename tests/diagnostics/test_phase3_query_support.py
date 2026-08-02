from scripts.diagnostics.run_phase3_query_support import aggregate_rankings


def test_rrf_rewards_repeated_cross_query_support():
    rankings = [
        ["single", "supported", "tail"],
        ["supported", "other", "tail"],
    ]
    assert aggregate_rankings(rankings, mode="rrf")[0] == "supported"


def test_cutoff_does_not_give_support_credit_to_deep_matches():
    rankings = [
        ["a", "b", "deep"],
        ["b", "a", "deep"],
    ]
    result = aggregate_rankings(
        rankings, mode="support_then_best", cutoff=2
    )
    assert result[:2] == ["a", "b"]
    assert result[-1] == "deep"
