"""Long-form realization for the offence-agnostic IDPR pipeline.

The active API is ``idpr.generation.issue_answer``. Legacy fraud-pilot symbols are
resolved lazily for compatibility with archived experiment scripts.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any
from warnings import warn


def __getattr__(name: str) -> Any:
    legacy = import_module("idpr.legacy.fraud_generation")
    try:
        value = getattr(legacy, name)
    except AttributeError as error:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from error
    warn(
        f"idpr.generation.{name} is a legacy fraud-pilot API; "
        "import it from idpr.legacy.fraud_generation for reproduction code",
        DeprecationWarning,
        stacklevel=2,
    )
    globals()[name] = value
    return value
