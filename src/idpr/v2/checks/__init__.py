"""The v2 Definition Layer Type checker: 8 independent semantic axes over a DefinitionRegistry.

Each axis module is independently callable (imports only registry/findings/expressions/compile,
never another axis module) -- no axis assumes another has already run.
"""

from __future__ import annotations

from idpr.v2.checks.completion import check_completion
from idpr.v2.checks.derivation import check_derivation_graph
from idpr.v2.checks.exports import check_exports
from idpr.v2.checks.operators import check_operators
from idpr.v2.checks.participation import check_participation
from idpr.v2.checks.references import check_references
from idpr.v2.checks.relation_types import check_relation_types
from idpr.v2.checks.stage_effect import check_stage_effect
from idpr.v2.findings import Finding, TypeCheckError
from idpr.v2.registry import DefinitionRegistry


def run_type_checks(registry: DefinitionRegistry) -> list[Finding]:
    """Never raises -- collects findings from all 8 axes, in axis order."""
    findings: list[Finding] = []
    findings.extend(check_references(registry))
    findings.extend(check_operators(registry))
    findings.extend(check_relation_types(registry))
    findings.extend(check_stage_effect(registry))
    findings.extend(check_exports(registry))
    findings.extend(check_participation(registry))
    findings.extend(check_derivation_graph(registry))
    findings.extend(check_completion(registry))
    return findings


def check_or_raise(registry: DefinitionRegistry) -> None:
    findings = run_type_checks(registry)
    if findings:
        raise TypeCheckError(findings)
