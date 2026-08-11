from __future__ import annotations

import pytest

from idpr.rulebase.scallop import run_probabilistic_program


def test_pinned_scallop_propagates_probabilistic_conjunction(tmp_path) -> None:
    output = run_probabilistic_program(
        "rel 0.8::a()\nrel 0.7::b()\nrel c() = a() and b()\nquery c\n",
        ("c",),
        tmp_path,
        top_k=3,
    )
    assert output["c"] == ((pytest.approx(0.56), ()),)
