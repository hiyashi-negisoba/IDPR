from __future__ import annotations

from idpr.v2.checks import run_type_checks
from idpr.v2.registry import load_definitions


def test_real_corpus_is_fully_type_clean() -> None:
    registry = load_definitions()
    assert len(registry.by_id) == 43
    assert len(registry.by_kind) == 12
    assert run_type_checks(registry) == []
