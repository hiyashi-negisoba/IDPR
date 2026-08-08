"""Findings produced by the v2 Definition Layer's 6 semantic type-checking axes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Finding:
    axis: str  # reference | operator | stage_effect | export | participation | derivation
    code: str
    object_id: str
    field_path: str
    message: str

    def __str__(self) -> str:
        return f"{self.axis}/{self.code} {self.object_id}.{self.field_path}: {self.message}"


class TypeCheckError(ValueError):
    def __init__(self, findings: Sequence[Finding]) -> None:
        self.findings = tuple(findings)
        super().__init__("\n".join(str(finding) for finding in self.findings))
