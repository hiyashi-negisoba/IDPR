"""Neural stage contracts for the offence-agnostic IDPR pipeline.

Legacy fraud-pilot symbols remain available through lazy attribute lookup so archived
experiment scripts keep working without loading pilot code on the production path.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any
from warnings import warn


def __getattr__(name: str) -> Any:
    legacy = import_module("idpr.legacy.fraud_neural")
    try:
        value = getattr(legacy, name)
    except AttributeError as error:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from error
    warn(
        f"idpr.neural.{name} is a legacy fraud-pilot API; "
        "import it from idpr.legacy.fraud_neural for reproduction code",
        DeprecationWarning,
        stacklevel=2,
    )
    globals()[name] = value
    return value
