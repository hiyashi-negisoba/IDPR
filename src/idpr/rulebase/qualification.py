"""Reviewed minimum prerequisites used by the answer-visibility layer.

This is deliberately smaller than an offence element skeleton.  Commentary headings are
not conjunctive elements, so requiring all of them would destroy recall.  The table only
records compound/result offences whose legal identity depends on a separately identified
base offence.  It controls whether Call 3 may *present* a symbolic candidate as an
independent established offence; it does not delete Call-2 assessments or Scallop traces.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Mapping

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]
QUALIFICATION_PATH = PROJECT_ROOT / "data/rulebase/answer_qualification.yaml"


class QualificationError(ValueError):
    """Raised when the reviewed qualification asset is malformed."""


@lru_cache(maxsize=1)
def required_base_offenses() -> Mapping[str, frozenset[str]]:
    payload = yaml.safe_load(QUALIFICATION_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise QualificationError("qualification asset must be an object")
    entries = payload.get("required_base_offenses")
    if not isinstance(entries, list):
        raise QualificationError("required_base_offenses must be an array")
    result: dict[str, frozenset[str]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise QualificationError(f"required_base_offenses[{index}] must be an object")
        offense = entry.get("offense")
        bases = entry.get("any_of")
        if not isinstance(offense, str) or not offense:
            raise QualificationError(f"required_base_offenses[{index}].offense is invalid")
        if offense in result:
            raise QualificationError(f"duplicate qualification for {offense}")
        if (
            not isinstance(bases, list)
            or not bases
            or any(not isinstance(base, str) or not base for base in bases)
        ):
            raise QualificationError(f"{offense}.any_of must be a non-empty string array")
        result[offense] = frozenset(bases)
    return result


def missing_required_base(
    article: str, *, established_without_gaps: set[str]
) -> frozenset[str]:
    """Return the acceptable bases when none has a gap-free established signal."""
    bases = required_base_offenses().get(article, frozenset())
    if not bases or bases & established_without_gaps:
        return frozenset()
    return bases
