"""v2-only Scallop backend Steps 1–5: expressions through liability-chain gates.

The module lowers validated ``CaseTruths`` through non-``None`` expressions,
``CompiledOffense`` elements, existing completion-policy semantics,
participation adapters, active doctrine effects, and the generic liability
chain.  Article 263 and the other dedicated statutory routes remain outside
the generic Step 5 lowering.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from idpr.rulebase.scallop import run_program
from idpr.v2 import expressions
from idpr.v2 import participation as participation_mod
from idpr.v2 import relations as relation_mod
from idpr.v2.compile import CompiledOffense
from idpr.v2.evaluate import TruthValue, fold_all
from idpr.v2.expressions import SLOT_NAMES, CanonicalExpr, canonical_leaf_refs
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.runtime import completion as completion_mod
from idpr.v2.runtime import pipeline
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.stages import (
    AppliedEffect,
    CompletionRequirementObligation,
    ComponentSlotObligation,
    CoPrincipalConstitutiveStatusObligation,
    LiabilityEvaluation,
    LiabilityResult,
    ObligationOutcome,
    OffenseEstablishment,
    OffenseRealization,
    ParticipationDependencyObligation,
    ParticipationRequirementObligation,
    RelationObligation,
    SlotObligation,
    StageResult,
    StatutoryDeemingObligation,
    not_reached,
)
from idpr.v2.runtime.truths import CaseTruths

QUERY_RELATION = "v2_expression_truth"
OFFENSE_ELEMENTS_QUERY_RELATION = "v2_offense_elements_truth"
COMPLETION_CANDIDATE_QUERY_RELATION = "v2_completion_candidate_truth"
COMPLETION_RESULT_QUERY_RELATION = "v2_completion_result"
COMPLETION_ELEMENTS_QUERY_RELATION = "v2_completion_elements_truth"
ATTRIBUTED_PREDICATE_QUERY_RELATION = "v2_attributed_predicate_truth"
CONSTITUTIVE_STATUS_QUERY_RELATION = "v2_constitutive_status_truth"
CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION = "v2_constitutive_status_true_instance"
DERIVATIVE_ELEMENTS_QUERY_RELATION = "v2_derivative_elements_truth"
DERIVATIVE_REQUIREMENT_QUERY_RELATION = "v2_derivative_requirement_truth"
STAGE_EFFECT_TRUTH_QUERY_RELATION = "v2_stage_effect_truth"
STAGE_EFFECT_RESULT_QUERY_RELATION = "v2_stage_effect_result"
ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION = "v2_elements_slot_obligation_truth"
ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION = "v2_elements_component_slot_obligation_truth"
ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION = "v2_elements_relation_obligation_truth"
COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION = "v2_completion_requirement_obligation_truth"
ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION = "v2_article_263_statutory_deeming_truth"
_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})
_DERIVATIVE_MODES = frozenset({"instigator", "aider"})
_ARTICLE_263_PROBE_REFS = frozenset({
    "legal_element.concurrent_independent_acts",
    "legal_element.same_object_of_result",
    "legal_element.causal_origin_unascertained",
})
_ARTICLE_263_RESULT_REF = "legal_element.injury_result"
_STAGE_NAMES = ("unlawfulness", "culpability", "punishability")
_STAGE_LEGAL_STATES = {
    "unlawfulness": frozenset({"preserved", "defeated", "unresolved"}),
    "culpability": frozenset({"preserved", "defeated", "diminished", "unresolved"}),
    "punishability": frozenset({"punishable", "exempted", "modified", "unresolved"}),
}
_GATE_STATES = frozenset({"passes", "fails", "unresolved"})
_EXPRESSION_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


class ScallopBackendContractError(ValueError):
    """Raised before invalid v2 data can become a Scallop program or EDB fact."""


@dataclass(frozen=True)
class ExpressionRoot:
    """A host-generated, static non-None canonical expression query target."""

    expression_id: str
    expression: CanonicalExpr


@dataclass(frozen=True)
class OffenseElementsProgram:
    """Static Step 2 program plus definition-time lowering provenance.

    ``relation_helper_manifest`` deliberately contains ``RelationInstanceKey``,
    not a case-time ``RuntimeRelationKey``.  The host combines each static key
    with an existing ``OffenseInstanceKey`` when it renders EDB facts.
    """

    program: str
    offense_helper_manifest: tuple[tuple[str, CompiledOffense], ...]
    relation_helper_manifest: tuple[
        tuple[str, CompiledOffense, relation_mod.RelationInstanceKey], ...
    ]


@dataclass(frozen=True)
class CompletionProgram:
    """Static Step 3 program and its checked policy/root inputs."""

    program: str
    roots: tuple[tuple[CompiledOffense, DefinitionEntry | None], ...]


@dataclass(frozen=True)
class ParticipationStageProgram:
    """Static Step 4 program plus checked participation/doctrine provenance."""

    program: str
    roots: tuple[CompiledOffense, ...]
    participation_policy: DefinitionEntry | None
    doctrine_manifest: tuple[DefinitionEntry, ...]


@dataclass(frozen=True)
class ParticipationStageQueryResults:
    """Host-validated, unordered Step 4 query outputs."""

    attributed_predicates: Mapping[tuple[OffenseInstanceKey, str], TruthValue]
    constitutive_statuses: Mapping[tuple[OffenseInstanceKey, str], TruthValue]
    constitutive_true_members: frozenset[tuple[OffenseInstanceKey, str, OffenseInstanceKey]]
    derivative_requirements: Mapping[tuple[OffenseInstanceKey, OffenseInstanceKey, str], TruthValue]
    derivative_elements: Mapping[tuple[OffenseInstanceKey, OffenseInstanceKey, str], TruthValue]
    stage_effects: Mapping[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]]
    stage_results: Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]]


@dataclass(frozen=True)
class LiabilityChainInputs:
    """Closed Step 5 result universe and caller-authored route inputs.

    ``completion_targets`` are the direct/co-principal result instances.  Each
    derivative accessory is supplied by exactly one link and deliberately has
    no completion target of its own.  This is a host-side boundary object only;
    it does not introduce a new runtime result carrier.
    """

    completion_targets: tuple[OffenseInstanceKey, ...]
    co_principal_sources: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...] = ()
    derivative_links: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...] = ()
    active_doctrines: tuple[tuple[OffenseInstanceKey, str], ...] = ()


def canonical_expression_serialization(expression: CanonicalExpr) -> str:
    """Return a hash-seed-independent canonical serialization for a non-None expression."""
    if expression is None:
        raise ScallopBackendContractError("Step 1 ExpressionRoot.expression must be non-None")
    return json.dumps(_expression_data(expression), ensure_ascii=True, separators=(",", ":"))


def compile_expression_program(
    registry: DefinitionRegistry, roots: Iterable[ExpressionRoot]
) -> str:
    """Compile static three-valued expression roots into a v2-only Scallop program.

    Both root normalization and nested child emission use canonical sorted
    serialization.  No iteration over a ``frozenset`` influences helper names
    or emitted rule order.
    """
    normalized = _normalize_roots(registry, roots)
    lines = [
        "// v2 Step 1 static three-valued expression program",
        "type v2_instance(String, String, String, String)",
        "type v2_predicate_truth(String, String, String, String, String, String)",
        "type v2_relation_key(String, String, String, String, String, String, String, String)",
        "type v2_relation_truth(String, String, String, String, String, String, String, String, String)",
        "type v2_expression_truth(String, String, String, String, String, String)",
        "",
    ]
    emitted: set[str] = set()
    for root in normalized:
        helper = _emit_expression(root.expression, lines, emitted)
        root_literal = _scl_string(root.expression_id)
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {QUERY_RELATION}(c, a, o, i, {root_literal}, {_scl_string(truth)}) = "
                f"{helper}_{suffix}(c, a, o, i)"
            )
        lines.append("")
    lines.append(f"query {QUERY_RELATION}")
    return "\n".join(lines) + "\n"


def render_case_truths_edb(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    relation_keys: Iterable[RuntimeRelationKey] = (),
) -> str:
    """Render validated CaseTruths entries as deterministic v2 Scallop EDB blocks."""
    normalized_instances = _normalize_instances(instances)
    instance_set = set(normalized_instances)
    normalized_relation_keys = _normalize_relation_keys(registry, relation_keys, instance_set)

    predicate_rows: list[tuple[str, ...]] = []
    for raw_key, truth in truths.predicate.items():
        if not isinstance(raw_key, tuple) or len(raw_key) != 2:
            raise ScallopBackendContractError("CaseTruths predicate key must be (OffenseInstanceKey, ref)")
        instance, ref = raw_key
        if not isinstance(instance, OffenseInstanceKey) or instance not in instance_set:
            raise ScallopBackendContractError("CaseTruths predicate entry has an unregistered instance")
        _validate_predicate_ref(registry, ref)
        _validate_truth(truth, "predicate")
        predicate_rows.append((*_instance_fields(instance), ref, truth))

    relation_set = set(normalized_relation_keys)
    relation_rows: list[tuple[str, ...]] = []
    for key, truth in truths.relation.items():
        if not isinstance(key, RuntimeRelationKey) or key not in relation_set:
            raise ScallopBackendContractError("CaseTruths relation entry has an unregistered relation key")
        _validate_truth(truth, "relation")
        relation_rows.append((*_relation_fields(key), truth))

    return _render_edb_relation("v2_instance", [_instance_fields(item) for item in normalized_instances]) + _render_edb_relation(
        "v2_predicate_truth", predicate_rows
    ) + _render_edb_relation("v2_relation_key", [_relation_fields(item) for item in normalized_relation_keys]) + _render_edb_relation(
        "v2_relation_truth", relation_rows
    )


def validate_expression_query_rows(
    rows: Iterable[Sequence[str]],
    *,
    instances: Iterable[OffenseInstanceKey],
    roots: Iterable[ExpressionRoot],
) -> Mapping[tuple[OffenseInstanceKey, str], TruthValue]:
    """Validate unordered query output against the exact instances x root-id key set."""
    normalized_instances = _normalize_instances(instances)
    normalized_roots = _normalize_root_ids(roots)
    instances_by_fields = {_instance_fields(instance): instance for instance in normalized_instances}
    root_ids = {root.expression_id for root in normalized_roots}
    expected = {(instance, root.expression_id) for instance in normalized_instances for root in normalized_roots}
    actual: dict[tuple[OffenseInstanceKey, str], TruthValue] = {}

    for index, row in enumerate(rows):
        values = tuple(row)
        if len(values) != 6:
            raise ScallopBackendContractError(
                f"{QUERY_RELATION}[{index}] must contain 6 strings, got {values!r}"
            )
        instance = instances_by_fields.get(values[:4])
        if instance is None:
            raise ScallopBackendContractError(f"{QUERY_RELATION}[{index}] has unexpected instance {values[:4]!r}")
        expression_id, truth = values[4:]
        if expression_id not in root_ids:
            raise ScallopBackendContractError(
                f"{QUERY_RELATION}[{index}] has unknown expression_id {expression_id!r}"
            )
        _validate_truth(truth, f"{QUERY_RELATION}[{index}]")
        key = (instance, expression_id)
        if key in actual:
            raise ScallopBackendContractError(f"duplicate {QUERY_RELATION} key: {key!r}")
        actual[key] = truth

    missing = expected - set(actual)
    if missing:
        raise ScallopBackendContractError(f"missing {QUERY_RELATION} keys: {sorted(missing, key=_result_key)!r}")
    unexpected = set(actual) - expected
    if unexpected:  # defensive: the row-level checks above should make this unreachable.
        raise ScallopBackendContractError(f"unexpected {QUERY_RELATION} keys: {unexpected!r}")
    return actual


def run_expression_parity_program(
    registry: DefinitionRegistry,
    roots: Iterable[ExpressionRoot],
    instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    work_dir: Path,
    relation_keys: Iterable[RuntimeRelationKey] = (),
) -> Mapping[tuple[OffenseInstanceKey, str], TruthValue]:
    """Run one locally generated Step 1 program and validate its unordered result."""
    root_values = tuple(roots)
    instance_values = tuple(instances)
    program = compile_expression_program(registry, root_values)
    edb = render_case_truths_edb(
        registry, instance_values, truths, relation_keys=relation_keys
    )
    output = run_program(
        program + edb,
        (QUERY_RELATION,),
        work_dir,
        name="v2_step1_expression",
    )
    decoded_rows = tuple(
        tuple(_decode_query_string(value) for value in row)
        for row in output[QUERY_RELATION]
    )
    return validate_expression_query_rows(
        decoded_rows, instances=instance_values, roots=root_values
    )


def compile_offense_elements_program(
    registry: DefinitionRegistry, compiled_offenses: Iterable[CompiledOffense]
) -> OffenseElementsProgram:
    """Lower checked v2 offenses to their Step 2 elements-level query program.

    This is deliberately narrower than the Python runtime pipeline: it folds
    top-level slots and every recursively preserved relation obligation, but
    does not lower completion, participation, effects, or liability stages.
    """
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    lines = [
        "// v2 Step 2 CompiledOffense elements program",
        *_edb_type_declarations(),
        f"type {OFFENSE_ELEMENTS_QUERY_RELATION}(String, String, String, String, String)",
        "",
    ]
    expression_emitted: set[str] = set()
    offense_manifest: list[tuple[str, CompiledOffense]] = []
    relation_manifest: list[tuple[str, CompiledOffense, relation_mod.RelationInstanceKey]] = []

    for compiled in roots:
        helper = _offense_helper_name(compiled.id)
        offense_manifest.append((helper, compiled))
        children: list[str] = []
        for slot in SLOT_NAMES:
            expression = compiled.slots[slot]
            if expression is not None:
                children.append(_emit_expression(expression, lines, expression_emitted))
        for relation_key, _binding in _ordered_relation_instances(compiled):
            relation_helper = _relation_helper_name(compiled.id, relation_key)
            relation_manifest.append((relation_helper, compiled, relation_key))
            _emit_relation_lookup(relation_helper, relation_key, lines)
            children.append(relation_helper)
        _emit_offense_all(helper, compiled.id, children, lines)
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {OFFENSE_ELEMENTS_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(truth)}) = "
                f"{helper}_{suffix}(c, a, i)"
            )
        lines.append("")

    lines.append(f"query {OFFENSE_ELEMENTS_QUERY_RELATION}")
    return OffenseElementsProgram(
        program="\n".join(lines) + "\n",
        offense_helper_manifest=tuple(offense_manifest),
        relation_helper_manifest=tuple(relation_manifest),
    )


def render_offense_elements_edb(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
) -> str:
    """Render exact Step 2 facts, including all required relation-key rows."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    instance_values = _normalize_instances(instances)
    relation_keys = _expected_runtime_relation_keys(roots, instance_values)
    return render_case_truths_edb(
        registry,
        instance_values,
        truths,
        relation_keys=relation_keys,
    )


def validate_offense_elements_query_rows(
    rows: Iterable[Sequence[str]],
    *,
    instances: Iterable[OffenseInstanceKey],
    compiled_offenses: Iterable[CompiledOffense],
) -> Mapping[OffenseInstanceKey, TruthValue]:
    """Validate unordered Step 2 query output against the exact instance key set."""
    roots = _normalize_compiled_offenses_unchecked(compiled_offenses)
    normalized_instances = _normalize_instances(instances)
    _validate_instance_roots(roots, normalized_instances)
    instances_by_fields = {_instance_fields(instance): instance for instance in normalized_instances}
    actual: dict[OffenseInstanceKey, TruthValue] = {}

    for index, row in enumerate(rows):
        values = tuple(row)
        if len(values) != 5:
            raise ScallopBackendContractError(
                f"{OFFENSE_ELEMENTS_QUERY_RELATION}[{index}] must contain 5 strings, got {values!r}"
            )
        instance = instances_by_fields.get(values[:4])
        if instance is None:
            raise ScallopBackendContractError(
                f"{OFFENSE_ELEMENTS_QUERY_RELATION}[{index}] has unexpected instance {values[:4]!r}"
            )
        truth = values[4]
        _validate_truth(truth, f"{OFFENSE_ELEMENTS_QUERY_RELATION}[{index}]")
        if instance in actual:
            raise ScallopBackendContractError(
                f"duplicate {OFFENSE_ELEMENTS_QUERY_RELATION} key: {instance!r}"
            )
        actual[instance] = truth

    expected = set(normalized_instances)
    missing = expected - set(actual)
    if missing:
        raise ScallopBackendContractError(
            f"missing {OFFENSE_ELEMENTS_QUERY_RELATION} keys: "
            f"{sorted(missing, key=_instance_fields)!r}"
        )
    unexpected = set(actual) - expected
    if unexpected:  # defensive: row-level instance validation makes this unreachable.
        raise ScallopBackendContractError(
            f"unexpected {OFFENSE_ELEMENTS_QUERY_RELATION} keys: {unexpected!r}"
        )
    return actual


def run_offense_elements_parity_program(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    work_dir: Path,
) -> Mapping[OffenseInstanceKey, TruthValue]:
    """Run locally generated Step 2 code and validate the elements-result key set."""
    root_values = tuple(compiled_offenses)
    instance_values = tuple(instances)
    static_program = compile_offense_elements_program(registry, root_values)
    edb = render_offense_elements_edb(registry, root_values, instance_values, truths)
    output = run_program(
        static_program.program + edb,
        (OFFENSE_ELEMENTS_QUERY_RELATION,),
        work_dir,
        name="v2_step2_offense_elements",
    )
    decoded_rows = tuple(
        tuple(_decode_query_string(value) for value in row)
        for row in output[OFFENSE_ELEMENTS_QUERY_RELATION]
    )
    return validate_offense_elements_query_rows(
        decoded_rows,
        instances=instance_values,
        compiled_offenses=root_values,
    )


def compile_completion_program(
    registry: DefinitionRegistry, compiled_offenses: Iterable[CompiledOffense]
) -> CompletionProgram:
    """Lower existing completion candidates, selection, and eligible Elements only."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    policies = tuple((compiled, completion_mod.completion_policy_for(registry, compiled.id)) for compiled in roots)
    lines = [
        "// v2 Step 3 completion policy program",
        *_edb_type_declarations(),
        "type v2_completion_target_instance(String, String, String, String)",
        f"type {COMPLETION_CANDIDATE_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {COMPLETION_RESULT_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {COMPLETION_ELEMENTS_QUERY_RELATION}(String, String, String, String, String)",
        "",
    ]
    emitted: set[str] = set()
    for compiled, policy in policies:
        if policy is None:
            _emit_no_policy_completion(compiled, lines, emitted)
        else:
            _emit_policy_completion(compiled, policy, lines, emitted)
    lines.extend((
        f"query {COMPLETION_CANDIDATE_QUERY_RELATION}",
        f"query {COMPLETION_RESULT_QUERY_RELATION}",
        f"query {COMPLETION_ELEMENTS_QUERY_RELATION}",
    ))
    return CompletionProgram(program="\n".join(lines) + "\n", roots=policies)


def render_completion_edb(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    targets: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
) -> str:
    """Render target identities plus deterministic component predicate scopes."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    target_values = _normalize_instances(targets)
    _validate_instance_roots(roots, target_values)
    policies = {compiled.id: completion_mod.completion_policy_for(registry, compiled.id) for compiled in roots}
    scopes = _completion_scope_instances(roots, policies, target_values)
    edb = render_case_truths_edb(
        registry, scopes, truths, relation_keys=_expected_runtime_relation_keys(roots, target_values)
    )
    return edb + _render_edb_relation(
        "v2_completion_target_instance", [_instance_fields(target) for target in target_values]
    )


def validate_completion_query_rows(candidate_rows: Iterable[Sequence[str]], result_rows: Iterable[Sequence[str]], element_rows: Iterable[Sequence[str]], *, registry: DefinitionRegistry, compiled_offenses: Iterable[CompiledOffense], targets: Iterable[OffenseInstanceKey]) -> tuple[Mapping[tuple[OffenseInstanceKey, str], TruthValue], Mapping[OffenseInstanceKey, tuple[str, str]], Mapping[OffenseInstanceKey, TruthValue]]:
    """Validate exact unordered Step 3 candidate/result/eligible-elements keys."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    target_values = _normalize_instances(targets)
    _validate_instance_roots(roots, target_values)
    by_fields = {_instance_fields(target): target for target in target_values}
    policies = {root.id: completion_mod.completion_policy_for(registry, root.id) for root in roots}
    expected_candidates = {(target, state) for target in target_values for state in (policies[target.offense_ref].payload["states"] if policies[target.offense_ref] else {})}
    candidates: dict[tuple[OffenseInstanceKey, str], TruthValue] = {}
    for row in candidate_rows:
        value = tuple(row)
        target = by_fields.get(value[:4]) if len(value) == 6 else None
        key = (target, value[4]) if target is not None else None
        if key not in expected_candidates or key in candidates:
            raise ScallopBackendContractError("unexpected or duplicate completion candidate key")
        _validate_truth(value[5], "completion candidate")
        candidates[key] = value[5]
    if set(candidates) != expected_candidates:
        raise ScallopBackendContractError("incomplete completion candidate key set")
    results: dict[OffenseInstanceKey, tuple[str, str]] = {}
    valid_states = set(completion_mod.DERIVABLE_STATES) | {"unresolved", "not_applicable"}
    for row in result_rows:
        value = tuple(row)
        target = by_fields.get(value[:4]) if len(value) == 6 else None
        if target is None or target in results or value[4] not in valid_states or value[5] not in {"TRUE", "FALSE", "NONE"}:
            raise ScallopBackendContractError("invalid or duplicate completion result row")
        results[target] = (value[4], value[5])
    if set(results) != set(target_values):
        raise ScallopBackendContractError("incomplete completion result key set")
    for target in target_values:
        policy = policies[target.offense_ref]
        if policy is None:
            expected = ("completed", "TRUE")
        else:
            outcomes = tuple(
                completion_mod.CompletionCandidateOutcome(state=name, truth=candidates[(target, name)])
                for name in completion_mod.DERIVABLE_STATES
                if name in policy.payload["states"]
            )
            state = completion_mod._derive_state(outcomes)
            expected = (state, "NONE") if state in {"unresolved", "not_applicable"} else (
                state,
                "TRUE" if policy.payload["states"][state]["punishable"] else "FALSE",
            )
        if results[target] != expected:
            raise ScallopBackendContractError("completion result disagrees with validated candidate cardinality")
    eligible = {target for target, (state, punishability) in results.items() if state not in {"unresolved", "not_applicable"} and punishability == "TRUE"}
    elements: dict[OffenseInstanceKey, TruthValue] = {}
    for row in element_rows:
        value = tuple(row)
        target = by_fields.get(value[:4]) if len(value) == 5 else None
        if target not in eligible or target in elements:
            raise ScallopBackendContractError("unexpected or duplicate completion elements key")
        _validate_truth(value[4], "completion elements")
        elements[target] = value[4]
    if set(elements) != eligible:
        raise ScallopBackendContractError("incomplete completion elements key set")
    return candidates, results, elements


def compile_participation_stage_program(
    registry: DefinitionRegistry, compiled_offenses: Iterable[CompiledOffense]
) -> ParticipationStageProgram:
    """Compile only the approved Step 4 participation and doctrine-effect surface."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    policy = participation_mod.participation_policy_for(registry)
    doctrines = _checked_doctrines(registry)
    lines = [
        "// v2 Step 4 participation and stage-effects program",
        *_edb_type_declarations(),
        "type v2_participation_target(String, String, String, String)",
        "type v2_co_principal_source(String, String, String, String, String, String, String, String)",
        "type v2_derivative_link(String, String, String, String, String, String, String, String, String)",
        "type v2_principal_realization_truth(String, String, String, String, String)",
        "type v2_active_doctrine(String, String, String, String, String)",
        "type v2_stage_effect_target(String, String, String, String, String)",
        f"type {ATTRIBUTED_PREDICATE_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {CONSTITUTIVE_STATUS_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION}(String, String, String, String, String, String, String, String, String)",
        f"type {DERIVATIVE_REQUIREMENT_QUERY_RELATION}(String, String, String, String, String, String, String, String, String, String)",
        f"type {DERIVATIVE_ELEMENTS_QUERY_RELATION}(String, String, String, String, String, String, String, String, String, String)",
        f"type {STAGE_EFFECT_TRUTH_QUERY_RELATION}(String, String, String, String, String, String, String)",
        f"type {STAGE_EFFECT_RESULT_QUERY_RELATION}(String, String, String, String, String, String, String)",
        "type v2_attributed_override(String, String, String, String, String)",
        "",
    ]
    emitted: set[str] = set()
    if policy is not None:
        for compiled in roots:
            _emit_co_principal_outputs(registry, compiled, policy, lines, emitted)
        _emit_derivative_outputs(policy, lines, emitted)
    for doctrine in doctrines:
        _emit_doctrine_effect(doctrine, lines, emitted)
    for stage in _STAGE_NAMES:
        _emit_stage_result(stage, doctrines, lines)
    lines.extend((
        f"query {ATTRIBUTED_PREDICATE_QUERY_RELATION}",
        f"query {CONSTITUTIVE_STATUS_QUERY_RELATION}",
        f"query {CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION}",
        f"query {DERIVATIVE_REQUIREMENT_QUERY_RELATION}",
        f"query {DERIVATIVE_ELEMENTS_QUERY_RELATION}",
        f"query {STAGE_EFFECT_TRUTH_QUERY_RELATION}",
        f"query {STAGE_EFFECT_RESULT_QUERY_RELATION}",
    ))
    return ParticipationStageProgram(
        program="\n".join(lines) + "\n",
        roots=roots,
        participation_policy=policy,
        doctrine_manifest=doctrines,
    )


def render_participation_stage_edb(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    participation_targets: Iterable[OffenseInstanceKey] = (),
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]] = (),
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = (),
    principal_realization_truths: Mapping[OffenseInstanceKey, TruthValue] = {},
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]] = (),
    stage_effect_targets: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> str:
    """Render validated Step 4 EDB input; evaluation instances authorize all endpoints."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    inputs = _normalize_step4_inputs(
        registry, roots, evaluation_instances, participation_targets, co_principal_sources,
        derivative_links, principal_realization_truths, active_doctrines, stage_effect_targets,
    )
    instances, targets, sources, links, realization_rows, active_rows, stage_targets = inputs
    edb = render_case_truths_edb(
        registry, instances, truths,
        relation_keys=_expected_runtime_relation_keys(roots, instances),
    )
    return edb + _render_edb_relation(
        "v2_participation_target", [_instance_fields(value) for value in targets]
    ) + _render_edb_relation(
        "v2_co_principal_source", [(*_instance_fields(target), *_instance_fields(source)) for target, source in sources]
    ) + _render_edb_relation(
        "v2_derivative_link", [(*_instance_fields(accessory), *_instance_fields(principal), mode) for accessory, principal, mode in links]
    ) + _render_edb_relation(
        "v2_principal_realization_truth", [(*_instance_fields(instance), truth) for instance, truth in realization_rows]
    ) + _render_edb_relation(
        "v2_active_doctrine", [(*_instance_fields(instance), doctrine_ref) for instance, doctrine_ref in active_rows]
    ) + _render_edb_relation(
        "v2_stage_effect_target", [(*_instance_fields(instance), stage) for instance, stage in stage_targets]
    )


def validate_participation_stage_query_rows(
    attributed_rows: Iterable[Sequence[str]],
    constitutive_rows: Iterable[Sequence[str]],
    member_rows: Iterable[Sequence[str]],
    requirement_rows: Iterable[Sequence[str]],
    derivative_rows: Iterable[Sequence[str]],
    effect_rows: Iterable[Sequence[str]],
    result_rows: Iterable[Sequence[str]],
    *,
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    participation_targets: Iterable[OffenseInstanceKey] = (),
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]] = (),
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = (),
    principal_realization_truths: Mapping[OffenseInstanceKey, TruthValue] = {},
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]] = (),
    stage_effect_targets: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> ParticipationStageQueryResults:
    """Validate every Step 4 query as an unordered exact-key map or set."""
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    inputs = _normalize_step4_inputs(
        registry, roots, evaluation_instances, participation_targets, co_principal_sources,
        derivative_links, principal_realization_truths, active_doctrines, stage_effect_targets,
    )
    instances, targets, sources, links, _realization_rows, active_rows, stage_targets = inputs
    by_fields = {_instance_fields(instance): instance for instance in instances}
    policy = participation_mod.participation_policy_for(registry)
    roots_by_id = {root.id: root for root in roots}
    source_map: dict[OffenseInstanceKey, tuple[OffenseInstanceKey, ...]] = {
        target: tuple(sorted((source for listed_target, source in sources if listed_target == target), key=_instance_fields))
        for target in targets
    }
    attributable: set[tuple[OffenseInstanceKey, str]] = set()
    constitutive: set[tuple[OffenseInstanceKey, str]] = set()
    members: set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]] = set()
    if policy is not None:
        for target in targets:
            compiled = roots_by_id[target.offense_ref]
            offense = registry.get(compiled.id)
            assert offense is not None
            slots = participation_mod.effective_attributable_slots(policy, offense)
            refs = set().union(*(canonical_leaf_refs(compiled.slots[slot]) for slot in slots))
            attributable.update((target, ref) for ref in refs)
            status_refs = participation_mod.constitutive_status_refs(offense)
            constitutive.update((target, ref) for ref in status_refs)
            for ref in status_refs:
                for member in (target, *source_map[target]):
                    if truths.predicate.get((member, ref), "UNKNOWN") == "TRUE":
                        members.add((target, ref, member))
    attributed = _validate_predicate_output_rows(
        attributed_rows, ATTRIBUTED_PREDICATE_QUERY_RELATION, attributable, by_fields
    )
    statuses = _validate_predicate_output_rows(
        constitutive_rows, CONSTITUTIVE_STATUS_QUERY_RELATION, constitutive, by_fields
    )
    actual_members = _validate_member_rows(member_rows, members, by_fields)
    expected_links = set(links)
    requirements = _validate_derivative_rows(
        requirement_rows, DERIVATIVE_REQUIREMENT_QUERY_RELATION, expected_links, by_fields
    )
    derivatives = _validate_derivative_rows(
        derivative_rows, DERIVATIVE_ELEMENTS_QUERY_RELATION, expected_links, by_fields
    )
    doctrine_by_ref = {entry.id: entry for entry in _checked_doctrines(registry)}
    expected_effects = {(instance, doctrine_ref) for instance, doctrine_ref in active_rows}
    effects = _validate_stage_effect_rows(effect_rows, expected_effects, doctrine_by_ref, by_fields)
    expected_stage_results = set(stage_targets)
    stage_results = _validate_stage_result_rows(result_rows, expected_stage_results, by_fields)
    return ParticipationStageQueryResults(
        attributed_predicates=attributed,
        constitutive_statuses=statuses,
        constitutive_true_members=frozenset(actual_members),
        derivative_requirements=requirements,
        derivative_elements=derivatives,
        stage_effects=effects,
        stage_results=stage_results,
    )


def run_participation_stage_parity_program(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    work_dir: Path,
    participation_targets: Iterable[OffenseInstanceKey] = (),
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]] = (),
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = (),
    principal_realization_truths: Mapping[OffenseInstanceKey, TruthValue] = {},
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]] = (),
    stage_effect_targets: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> ParticipationStageQueryResults:
    """Run the Step 4 static program locally and enforce its query contract."""
    roots = tuple(compiled_offenses)
    instances = tuple(evaluation_instances)
    targets = tuple(participation_targets)
    sources = tuple(co_principal_sources)
    links = tuple(derivative_links)
    active = tuple(active_doctrines)
    stage_targets = tuple(stage_effect_targets)
    static = compile_participation_stage_program(registry, roots)
    edb = render_participation_stage_edb(
        registry, roots, instances, truths,
        participation_targets=targets,
        co_principal_sources=sources,
        derivative_links=links,
        principal_realization_truths=principal_realization_truths,
        active_doctrines=active,
        stage_effect_targets=stage_targets,
    )
    queries = (
        ATTRIBUTED_PREDICATE_QUERY_RELATION,
        CONSTITUTIVE_STATUS_QUERY_RELATION,
        CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION,
        DERIVATIVE_REQUIREMENT_QUERY_RELATION,
        DERIVATIVE_ELEMENTS_QUERY_RELATION,
        STAGE_EFFECT_TRUTH_QUERY_RELATION,
        STAGE_EFFECT_RESULT_QUERY_RELATION,
    )
    output = run_program(static.program + edb, queries, work_dir, name="v2_step4_participation_stage")
    decoded = {
        query: tuple(tuple(_decode_query_string(value) for value in row) for row in output[query])
        for query in queries
    }
    return validate_participation_stage_query_rows(
        decoded[ATTRIBUTED_PREDICATE_QUERY_RELATION],
        decoded[CONSTITUTIVE_STATUS_QUERY_RELATION],
        decoded[CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION],
        decoded[DERIVATIVE_REQUIREMENT_QUERY_RELATION],
        decoded[DERIVATIVE_ELEMENTS_QUERY_RELATION],
        decoded[STAGE_EFFECT_TRUTH_QUERY_RELATION],
        decoded[STAGE_EFFECT_RESULT_QUERY_RELATION],
        registry=registry,
        compiled_offenses=roots,
        evaluation_instances=instances,
        truths=truths,
        participation_targets=targets,
        co_principal_sources=sources,
        derivative_links=links,
        principal_realization_truths=principal_realization_truths,
        active_doctrines=active,
        stage_effect_targets=stage_targets,
    )


def _emit_co_principal_outputs(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    policy: DefinitionEntry,
    lines: list[str],
    emitted: set[str],
) -> None:
    offense = registry.get(compiled.id)
    assert offense is not None
    slots = participation_mod.effective_attributable_slots(policy, offense)
    refs = sorted(set().union(*(canonical_leaf_refs(compiled.slots[slot]) for slot in slots)))
    for ref in refs:
        helper = _step4_helper_name("attributed", compiled.id, ref)
        _emit_target_source_any(
            helper, compiled.id, ref, ATTRIBUTED_PREDICATE_QUERY_RELATION, lines, emitted
        )
        lines.append(
            f"rel v2_attributed_override(c, a, {_scl_string(compiled.id)}, i, {_scl_string(ref)}) = "
            f"{ATTRIBUTED_PREDICATE_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(ref)}, t)"
        )
    for ref in sorted(participation_mod.constitutive_status_refs(offense)):
        helper = _step4_helper_name("constitutive", compiled.id, ref)
        _emit_target_source_any(
            helper, compiled.id, ref, CONSTITUTIVE_STATUS_QUERY_RELATION, lines, emitted
        )
        ref_literal = _scl_string(ref)
        target = f"v2_participation_target(c, a, {_scl_string(compiled.id)}, i)"
        leaf = _emit_expression(("ref", ref), lines, emitted)
        lines.append(
            f"rel {CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {ref_literal}, c, a, {_scl_string(compiled.id)}, i) = "
            f"{target} and {leaf}_true(c, a, {_scl_string(compiled.id)}, i)"
        )
        lines.append(
            f"rel {CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {ref_literal}, sc, sa, so, si) = "
            f"{target} and v2_co_principal_source(c, a, {_scl_string(compiled.id)}, i, sc, sa, so, si) and {leaf}_true(sc, sa, so, si)"
        )
    lines.append("")


def _emit_target_source_any(
    helper: str,
    offense_ref: str,
    ref: str,
    query: str,
    lines: list[str],
    emitted: set[str],
) -> None:
    for suffix in ("true", "false", "unknown", "source_unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String)")
    target = f"v2_participation_target(c, a, {_scl_string(offense_ref)}, i)"
    leaf = _emit_expression(("ref", ref), lines, emitted)
    source = f"v2_co_principal_source(c, a, {_scl_string(offense_ref)}, i, sc, sa, so, si)"
    lines.append(f"rel {helper}_true(c, a, i) = {target} and {leaf}_true(c, a, {_scl_string(offense_ref)}, i)")
    lines.append(f"rel {helper}_true(c, a, i) = {target} and {source} and {leaf}_true(sc, sa, so, si)")
    lines.append(f"rel {helper}_source_unknown(c, a, i) = {target} and {source} and {leaf}_unknown(sc, sa, so, si)")
    lines.append(
        f"rel {helper}_false(c, a, i) = {target} and {leaf}_false(c, a, {_scl_string(offense_ref)}, i) and "
        f"not {helper}_true(c, a, i) and not {helper}_source_unknown(c, a, i)"
    )
    lines.append(
        f"rel {helper}_unknown(c, a, i) = {target} and not {helper}_true(c, a, i) and not {helper}_false(c, a, i)"
    )
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(
            f"rel {query}(c, a, {_scl_string(offense_ref)}, i, {_scl_string(ref)}, {_scl_string(truth)}) = {helper}_{suffix}(c, a, i)"
        )
    lines.append("")


def _emit_derivative_outputs(policy: DefinitionEntry, lines: list[str], emitted: set[str]) -> None:
    modes = policy.payload.get("modes") or {}
    for mode in sorted(_DERIVATIVE_MODES & set(modes)):
        requires = expressions.canonicalize(modes[mode]["requires"])
        assert requires is not None
        helper = _emit_expression(requires, lines, emitted)
        mode_literal = _scl_string(mode)
        link = f"v2_derivative_link(c, a, o, i, pc, pa, po, pi, {mode_literal})"
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {DERIVATIVE_REQUIREMENT_QUERY_RELATION}(c, a, o, i, pc, pa, po, pi, {mode_literal}, {_scl_string(truth)}) = "
                f"{link} and {helper}_{suffix}(c, a, o, i)"
            )
        aggregate = _step4_helper_name("derivative_elements", mode)
        for suffix in ("true", "false", "unknown"):
            lines.append(f"type {aggregate}_{suffix}(String, String, String, String, String, String, String, String)")
        lines.append(
            f"rel {aggregate}_true(c, a, o, i, pc, pa, po, pi) = "
            f"{link} and v2_principal_realization_truth(pc, pa, po, pi, \"TRUE\") and "
            f"{DERIVATIVE_REQUIREMENT_QUERY_RELATION}(c, a, o, i, pc, pa, po, pi, {mode_literal}, \"TRUE\")"
        )
        lines.append(
            f"rel {aggregate}_false(c, a, o, i, pc, pa, po, pi) = "
            f"{link} and v2_principal_realization_truth(pc, pa, po, pi, \"FALSE\")"
        )
        lines.append(
            f"rel {aggregate}_false(c, a, o, i, pc, pa, po, pi) = "
            f"{link} and {DERIVATIVE_REQUIREMENT_QUERY_RELATION}(c, a, o, i, pc, pa, po, pi, {mode_literal}, \"FALSE\")"
        )
        lines.append(
            f"rel {aggregate}_unknown(c, a, o, i, pc, pa, po, pi) = "
            f"{link} and not {aggregate}_true(c, a, o, i, pc, pa, po, pi) and not {aggregate}_false(c, a, o, i, pc, pa, po, pi)"
        )
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {DERIVATIVE_ELEMENTS_QUERY_RELATION}(c, a, o, i, pc, pa, po, pi, {mode_literal}, {_scl_string(truth)}) = "
                f"{aggregate}_{suffix}(c, a, o, i, pc, pa, po, pi)"
            )
    lines.append("")


def _emit_doctrine_effect(doctrine: DefinitionEntry, lines: list[str], emitted: set[str]) -> None:
    effect_data = doctrine.payload["effect"]
    stage = doctrine.payload["stage"]
    effect = effect_data["effect"]
    expression = expressions.canonicalize(doctrine.payload["requires"])
    assert expression is not None
    helper = _emit_attribution_aware_expression(expression, lines, emitted)
    effect_helper = _step4_helper_name("doctrine_effect", doctrine.id)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {effect_helper}_{suffix}(String, String, String, String)")
    gate = (
        f"v2_stage_effect_target(c, a, o, i, {_scl_string(stage)}) and "
        f"v2_active_doctrine(c, a, o, i, {_scl_string(doctrine.id)})"
    )
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(f"rel {effect_helper}_{suffix}(c, a, o, i) = {gate} and {helper}_{suffix}(c, a, o, i)")
        lines.append(
            f"rel {STAGE_EFFECT_TRUTH_QUERY_RELATION}(c, a, o, i, {_scl_string(doctrine.id)}, {_scl_string(effect)}, {_scl_string(truth)}) = "
            f"{effect_helper}_{suffix}(c, a, o, i)"
        )
    lines.append("")


def _emit_stage_result(stage: str, doctrines: Sequence[DefinitionEntry], lines: list[str]) -> None:
    blocking = {"unlawfulness": "DEFEAT", "culpability": "DEFEAT", "punishability": "EXEMPT"}[stage]
    target = f"v2_stage_effect_target(c, a, o, i, {_scl_string(stage)})"
    helpers: dict[tuple[str, str], str] = {}
    for effect in ("DEFEAT", "EXEMPT", "MODIFY"):
        aggregate = _step4_helper_name("stage_effect", stage, effect)
        helpers[(effect, "true")] = f"{aggregate}_true(c, a, o, i)"
        helpers[(effect, "unknown")] = f"{aggregate}_unknown(c, a, o, i)"
        for suffix in ("true", "unknown"):
            lines.append(f"type {aggregate}_{suffix}(String, String, String, String)")
        for doctrine in doctrines:
            if doctrine.payload["stage"] == stage and doctrine.payload["effect"]["effect"] == effect:
                doctrine_helper = _step4_helper_name("doctrine_effect", doctrine.id)
                lines.append(f"rel {aggregate}_true(c, a, o, i) = {doctrine_helper}_true(c, a, o, i)")
                lines.append(f"rel {aggregate}_unknown(c, a, o, i) = {doctrine_helper}_unknown(c, a, o, i)")
    block_true = helpers[(blocking, "true")]
    block_unknown = helpers[(blocking, "unknown")]
    modifier_true = helpers[("MODIFY", "true")]
    modifier_unknown = helpers[("MODIFY", "unknown")]
    blocked_state = {"unlawfulness": "defeated", "culpability": "defeated", "punishability": "exempted"}[stage]
    open_state = {"unlawfulness": "preserved", "culpability": "preserved", "punishability": "punishable"}[stage]
    lines.append(
        f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, {_scl_string(blocked_state)}, \"fails\") = {target} and {block_true}"
    )
    lines.append(
        f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, \"unresolved\", \"unresolved\") = {target} and not {block_true} and {block_unknown}"
    )
    no_block = f"not {block_true} and not {block_unknown}"
    if stage == "unlawfulness":
        lines.append(
            f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, {_scl_string(open_state)}, \"passes\") = {target} and {no_block}"
        )
    else:
        modified_state = "diminished" if stage == "culpability" else "modified"
        lines.append(
            f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, {_scl_string(modified_state)}, \"passes\") = {target} and {no_block} and {modifier_true}"
        )
        lines.append(
            f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, \"unresolved\", \"passes\") = {target} and {no_block} and not {modifier_true} and {modifier_unknown}"
        )
        lines.append(
            f"rel {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, {_scl_string(stage)}, {_scl_string(open_state)}, \"passes\") = {target} and {no_block} and not {modifier_true} and not {modifier_unknown}"
        )
    lines.append("")


def _normalize_step4_inputs(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    participation_targets: Iterable[OffenseInstanceKey],
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]],
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    principal_realization_truths: Mapping[OffenseInstanceKey, TruthValue],
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]],
    stage_effect_targets: Iterable[tuple[OffenseInstanceKey, str]],
) -> tuple[
    tuple[OffenseInstanceKey, ...],
    tuple[OffenseInstanceKey, ...],
    tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...],
    tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...],
    tuple[tuple[OffenseInstanceKey, TruthValue], ...],
    tuple[tuple[OffenseInstanceKey, str], ...],
    tuple[tuple[OffenseInstanceKey, str], ...],
]:
    instances = _normalize_instances(evaluation_instances)
    _validate_instance_roots(roots, instances)
    instance_set = set(instances)
    policy = participation_mod.participation_policy_for(registry)

    targets = _normalize_instances(participation_targets)
    for target in targets:
        _validate_step4_endpoint(target, instance_set, "participation target")
        offense = registry.get(target.offense_ref)
        if policy is None or offense is None or not _co_principal_enabled(policy, offense):
            raise ScallopBackendContractError("participation target has no enabled co_principal mode")

    source_values = tuple(co_principal_sources)
    if len(set(source_values)) != len(source_values):
        raise ScallopBackendContractError("co-principal sources must be deduplicated")
    sources: list[tuple[OffenseInstanceKey, OffenseInstanceKey]] = []
    for value in source_values:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ScallopBackendContractError("co-principal source must be (target, source)")
        target, source = value
        if target not in targets:
            raise ScallopBackendContractError("co-principal source lacks a participation target anchor")
        _validate_step4_endpoint(source, instance_set, "co-principal source")
        if source.case_id != target.case_id:
            raise ScallopBackendContractError("co-principal source is not case-compatible with its target")
        sources.append((target, source))

    link_values = tuple(derivative_links)
    if len(set(link_values)) != len(link_values):
        raise ScallopBackendContractError("derivative links must be deduplicated")
    links: list[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = []
    modes = {} if policy is None else (policy.payload.get("modes") or {})
    for value in link_values:
        if not isinstance(value, tuple) or len(value) != 3:
            raise ScallopBackendContractError("derivative link must be (accessory, principal, mode)")
        accessory, principal, mode = value
        _validate_step4_endpoint(accessory, instance_set, "derivative accessory")
        _validate_step4_endpoint(principal, instance_set, "derivative principal")
        if accessory.case_id != principal.case_id:
            raise ScallopBackendContractError("derivative endpoints are not case-compatible")
        offense = registry.get(accessory.offense_ref)
        if mode not in _DERIVATIVE_MODES or mode not in modes or offense is None or _mode_disabled(offense, mode):
            raise ScallopBackendContractError("derivative link mode is absent or disabled for accessory offense")
        links.append((accessory, principal, mode))

    principal_set = {principal for _accessory, principal, _mode in links}
    realization_items = tuple(principal_realization_truths.items())
    if len(realization_items) != len(principal_realization_truths):  # defensive Mapping check
        raise ScallopBackendContractError("duplicate principal realization input")
    realization_map = dict(realization_items)
    if set(realization_map) != principal_set:
        raise ScallopBackendContractError("principal realization rows must exactly match derivative principals")
    for principal, truth in realization_map.items():
        _validate_step4_endpoint(principal, instance_set, "principal realization")
        _validate_truth(truth, "principal realization")

    stage_values = tuple(stage_effect_targets)
    if len(set(stage_values)) != len(stage_values):
        raise ScallopBackendContractError("stage-effect targets must be deduplicated")
    stages: list[tuple[OffenseInstanceKey, str]] = []
    for value in stage_values:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ScallopBackendContractError("stage-effect target must be (instance, stage)")
        instance, stage = value
        _validate_step4_endpoint(instance, instance_set, "stage-effect target")
        if stage not in _STAGE_NAMES:
            raise ScallopBackendContractError("invalid doctrine stage target")
        stages.append((instance, stage))
    stage_set = set(stages)

    active_values = tuple(active_doctrines)
    if len(set(active_values)) != len(active_values):
        raise ScallopBackendContractError("active doctrines must be deduplicated")
    active: list[tuple[OffenseInstanceKey, str]] = []
    for value in active_values:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ScallopBackendContractError("active doctrine must be (instance, doctrine_ref)")
        instance, doctrine_ref = value
        _validate_step4_endpoint(instance, instance_set, "active doctrine")
        doctrine = registry.get(doctrine_ref)
        if doctrine is None or doctrine.kind != "doctrine":
            raise ScallopBackendContractError("active doctrine ref is not a loaded DoctrineDef")
        stage = doctrine.payload["stage"]
        effect = doctrine.payload["effect"]
        if stage not in _STAGE_NAMES or effect.get("stage") != stage or effect.get("effect") not in {"DEFEAT", "MODIFY", "EXEMPT"}:
            raise ScallopBackendContractError("active doctrine has invalid checked stage/effect")
        if (instance, stage) not in stage_set:
            raise ScallopBackendContractError("active doctrine lacks its authored stage-effect target")
        active.append((instance, doctrine_ref))

    return (
        instances,
        targets,
        tuple(sorted(sources, key=lambda value: (*_instance_fields(value[0]), *_instance_fields(value[1])))),
        tuple(sorted(links, key=lambda value: (*_instance_fields(value[0]), *_instance_fields(value[1]), value[2]))),
        tuple(sorted(realization_map.items(), key=lambda value: _instance_fields(value[0]))),
        tuple(sorted(active, key=lambda value: (*_instance_fields(value[0]), value[1]))),
        tuple(sorted(stage_set, key=lambda value: (*_instance_fields(value[0]), value[1]))),
    )


def _validate_step4_endpoint(
    instance: object, evaluation_instances: set[OffenseInstanceKey], label: str
) -> None:
    if not isinstance(instance, OffenseInstanceKey) or instance not in evaluation_instances:
        raise ScallopBackendContractError(
            f"{label} must be an independently evaluable, authorized OffenseInstanceKey"
        )


def _co_principal_enabled(policy: DefinitionEntry, offense: DefinitionEntry) -> bool:
    modes = policy.payload.get("modes") or {}
    return "co_principal" in modes and not _mode_disabled(offense, "co_principal")


def _mode_disabled(offense: DefinitionEntry, mode: str) -> bool:
    constraints = offense.payload.get("participation_constraints") or {}
    return mode in frozenset(constraints.get("disabled_modes") or ())


def _checked_doctrines(registry: DefinitionRegistry) -> tuple[DefinitionEntry, ...]:
    doctrines = tuple(sorted(registry.by_kind.get("doctrine", ()), key=lambda entry: entry.id))
    for doctrine in doctrines:
        stage = doctrine.payload.get("stage")
        effect = doctrine.payload.get("effect") or {}
        if stage not in _STAGE_NAMES or effect.get("stage") != stage or effect.get("effect") not in {"DEFEAT", "MODIFY", "EXEMPT"}:
            raise ScallopBackendContractError(f"DoctrineDef {doctrine.id!r} has invalid stage/effect")
        expression = expressions.canonicalize(doctrine.payload.get("requires"))
        if expression is None:
            raise ScallopBackendContractError(f"DoctrineDef {doctrine.id!r} requires a non-None expression")
    return doctrines


def _validate_predicate_output_rows(
    rows: Iterable[Sequence[str]],
    query: str,
    expected: set[tuple[OffenseInstanceKey, str]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> Mapping[tuple[OffenseInstanceKey, str], TruthValue]:
    actual: dict[tuple[OffenseInstanceKey, str], TruthValue] = {}
    for row in rows:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == 6 else None
        key = (instance, value[4]) if instance is not None else None
        if key not in expected or key in actual:
            raise ScallopBackendContractError(f"unexpected or duplicate {query} key")
        _validate_truth(value[5], query)
        actual[key] = value[5]
    if set(actual) != expected:
        raise ScallopBackendContractError(f"incomplete {query} key set")
    return actual


def _validate_member_rows(
    rows: Iterable[Sequence[str]],
    expected: set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]]:
    actual: set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]] = set()
    for row in rows:
        value = tuple(row)
        target = by_fields.get(value[:4]) if len(value) == 9 else None
        member = by_fields.get(value[5:]) if len(value) == 9 else None
        key = (target, value[4], member) if target is not None and member is not None else None
        if key not in expected or key in actual:
            raise ScallopBackendContractError("unexpected or duplicate constitutive status member key")
        actual.add(key)
    if actual != expected:
        raise ScallopBackendContractError("incomplete constitutive status member key set")
    return actual


def _validate_derivative_rows(
    rows: Iterable[Sequence[str]],
    query: str,
    expected: set[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> Mapping[tuple[OffenseInstanceKey, OffenseInstanceKey, str], TruthValue]:
    actual: dict[tuple[OffenseInstanceKey, OffenseInstanceKey, str], TruthValue] = {}
    for row in rows:
        value = tuple(row)
        accessory = by_fields.get(value[:4]) if len(value) == 10 else None
        principal = by_fields.get(value[4:8]) if len(value) == 10 else None
        key = (accessory, principal, value[8]) if accessory is not None and principal is not None else None
        if key not in expected or key in actual:
            raise ScallopBackendContractError(f"unexpected or duplicate {query} key")
        _validate_truth(value[9], query)
        actual[key] = value[9]
    if set(actual) != expected:
        raise ScallopBackendContractError(f"incomplete {query} key set")
    return actual


def _validate_stage_effect_rows(
    rows: Iterable[Sequence[str]],
    expected: set[tuple[OffenseInstanceKey, str]],
    doctrines: Mapping[str, DefinitionEntry],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> Mapping[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]]:
    actual: dict[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]] = {}
    for row in rows:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == 7 else None
        key = (instance, value[4]) if instance is not None else None
        doctrine = doctrines.get(value[4]) if len(value) == 7 else None
        if key not in expected or key in actual or doctrine is None:
            raise ScallopBackendContractError("unexpected or duplicate stage-effect truth key")
        effect = doctrine.payload["effect"]["effect"]
        if value[5] != effect:
            raise ScallopBackendContractError("stage-effect row disagrees with DoctrineDef effect")
        _validate_truth(value[6], "stage effect")
        actual[key] = (value[5], value[6])
    if set(actual) != expected:
        raise ScallopBackendContractError("incomplete stage-effect truth key set")
    return actual


def _validate_stage_result_rows(
    rows: Iterable[Sequence[str]],
    expected: set[tuple[OffenseInstanceKey, str]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]]:
    actual: dict[tuple[OffenseInstanceKey, str], tuple[str, str]] = {}
    for row in rows:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == 7 else None
        key = (instance, value[4]) if instance is not None else None
        if key not in expected or key in actual:
            raise ScallopBackendContractError("unexpected or duplicate stage-effect result key")
        stage, legal_state, gate_state = value[4:]
        if legal_state not in _STAGE_LEGAL_STATES[stage] or gate_state not in _GATE_STATES:
            raise ScallopBackendContractError("stage-effect result has invalid legal/gate state")
        actual[key] = (legal_state, gate_state)
    if set(actual) != expected:
        raise ScallopBackendContractError("incomplete stage-effect result key set")
    return actual


def _edb_type_declarations() -> tuple[str, ...]:
    return (
        "type v2_instance(String, String, String, String)",
        "type v2_predicate_truth(String, String, String, String, String, String)",
        "type v2_relation_key(String, String, String, String, String, String, String, String)",
        "type v2_relation_truth(String, String, String, String, String, String, String, String, String)",
    )


def _emit_no_policy_completion(
    compiled: CompiledOffense, lines: list[str], emitted: set[str]
) -> None:
    helper = _completion_helper_name("elements", compiled.id, "default")
    children = _completion_children(compiled, {}, (), None, lines, emitted)
    _emit_completion_all(helper, compiled.id, None, children, lines)
    target = f"v2_completion_target_instance(c, a, {_scl_string(compiled.id)}, i)"
    lines.append(
        f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, \"completed\", \"TRUE\") = {target}"
    )
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(
            f"rel {COMPLETION_ELEMENTS_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(truth)}) = {helper}_{suffix}(c, a, i)"
        )
    lines.append("")


def _emit_policy_completion(
    compiled: CompiledOffense, policy: DefinitionEntry, lines: list[str], emitted: set[str]
) -> None:
    states = policy.payload["states"]
    names = tuple(sorted(name for name in completion_mod.DERIVABLE_STATES if name in states))
    candidates: dict[str, str] = {}
    for name in names:
        state = states[name]
        expression = expressions.canonicalize(state["when"])
        assert expression is not None
        expression_helper = _emit_expression(expression, lines, emitted)
        helper = _completion_helper_name("candidate", compiled.id, name)
        _emit_completion_candidate(helper, compiled.id, _state_scope_ref(compiled, state), expression_helper, lines)
        candidates[name] = helper
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {COMPLETION_CANDIDATE_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(name)}, {_scl_string(truth)}) = {helper}_{suffix}(c, a, i)"
            )
    selected = _emit_completion_selection(compiled.id, names, candidates, lines)
    for name in names:
        state = states[name]
        label = "TRUE" if state["punishable"] else "FALSE"
        lines.append(
            f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(name)}, {_scl_string(label)}) = {selected[name]}(c, a, i)"
        )
        if state["punishable"]:
            helper = _completion_helper_name("elements", compiled.id, name)
            children = _completion_children(
                compiled, _state_relation_dispositions(compiled, state), tuple(state.get("suspends") or ()), state, lines, emitted
            )
            _emit_completion_all(helper, compiled.id, selected[name], children, lines)
            for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
                lines.append(
                    f"rel {COMPLETION_ELEMENTS_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(truth)}) = {helper}_{suffix}(c, a, i)"
                )
    for state in ("unresolved", "not_applicable"):
        helper = _completion_helper_name("selected", compiled.id, state)
        lines.append(
            f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(state)}, \"NONE\") = {helper}(c, a, i)"
        )
    lines.append("")


def _emit_completion_candidate(helper: str, target_ref: str, scope_ref: str, expression_helper: str, lines: list[str]) -> None:
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String)")
        lines.append(
            f"rel {helper}_{suffix}(c, a, i) = v2_completion_target_instance(c, a, {_scl_string(target_ref)}, i) and {expression_helper}_{suffix}(c, a, {_scl_string(scope_ref)}, i)"
        )
    lines.append("")


def _emit_completion_selection(offense_id: str, names: Sequence[str], candidates: Mapping[str, str], lines: list[str]) -> Mapping[str, str]:
    target = f"v2_completion_target_instance(c, a, {_scl_string(offense_id)}, i)"
    selected: dict[str, str] = {}
    for name in names:
        helper = _completion_helper_name("selected", offense_id, name)
        selected[name] = helper
        negative = [f"not {candidates[other]}_true(c, a, i)" for other in names if other != name]
        lines.append(f"type {helper}(String, String, String)")
        lines.append(f"rel {helper}(c, a, i) = {' and '.join([target, f'{candidates[name]}_true(c, a, i)', *negative])}")
    no_true = [f"not {candidates[name]}_true(c, a, i)" for name in names]
    unresolved = _completion_helper_name("selected", offense_id, "unresolved")
    lines.append(f"type {unresolved}(String, String, String)")
    for left, right in combinations(names, 2):
        lines.append(f"rel {unresolved}(c, a, i) = {target} and {candidates[left]}_true(c, a, i) and {candidates[right]}_true(c, a, i)")
    for name in names:
        lines.append(f"rel {unresolved}(c, a, i) = {' and '.join([target, *no_true, f'{candidates[name]}_unknown(c, a, i)'])}")
    not_applicable = _completion_helper_name("selected", offense_id, "not_applicable")
    lines.append(f"type {not_applicable}(String, String, String)")
    no_unknown = [f"not {candidates[name]}_unknown(c, a, i)" for name in names]
    lines.append(f"rel {not_applicable}(c, a, i) = {' and '.join([target, *no_true, *no_unknown])}")
    return selected


def _emit_completion_all(helper: str, offense_id: str, selected: str | None, children: Sequence[tuple[str, str]], lines: list[str]) -> None:
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String)")
    gate = f"v2_completion_target_instance(c, a, {_scl_string(offense_id)}, i)"
    if selected is not None:
        gate = f"{gate} and {selected}(c, a, i)"
    lines.append(f"rel {helper}_true(c, a, i) = {' and '.join([gate, *(f'{child}_true(c, a, {_scl_string(scope)}, i)' for child, scope in children)])}")
    for child, scope in children:
        lines.append(f"rel {helper}_false(c, a, i) = {gate} and {child}_false(c, a, {_scl_string(scope)}, i)")
    lines.append(f"rel {helper}_unknown(c, a, i) = {gate} and not {helper}_true(c, a, i) and not {helper}_false(c, a, i)")
    lines.append("")


def _completion_helper_name(kind: str, offense_id: str, state: str) -> str:
    token = hashlib.sha256(f"{kind}:{offense_id}:{state}".encode()).hexdigest()
    return f"v2_completion_{kind}_{token}"


def _state_scope_ref(compiled: CompiledOffense, state: Mapping[str, object]) -> str:
    scope = state.get("when_component")
    if not scope:
        return compiled.id
    component = next((item for item in compiled.components if item.local_key == scope["local_key"]), None)
    if component is None or component.source_ref != scope["offense"]:
        raise ScallopBackendContractError("completion component scope is not a compiled direct component")
    return scope["offense"]


def _state_relation_dispositions(compiled: CompiledOffense, state: Mapping[str, object]) -> Mapping[relation_mod.RelationInstanceKey, str]:
    known = {(key.occurrence_path[1:], key.relation_ref, key.left_local_key, key.right_local_key): key for key, _ in _ordered_relation_instances(compiled)}
    output: dict[relation_mod.RelationInstanceKey, str] = {}
    for item in state.get("relations") or ():
        signature = (tuple(item.get("path") or ()), item["relation"], item["left"], item["right"])
        if signature not in known:
            raise ScallopBackendContractError("completion disposition does not match compiled relation")
        output[known[signature]] = item["disposition"]
    return output


def _completion_scope_instances(roots: Sequence[CompiledOffense], policies: Mapping[str, DefinitionEntry | None], targets: Sequence[OffenseInstanceKey]) -> tuple[OffenseInstanceKey, ...]:
    by_id = {compiled.id: compiled for compiled in roots}
    scopes: set[OffenseInstanceKey] = set(targets)
    for target in targets:
        compiled, policy = by_id[target.offense_ref], policies[target.offense_ref]
        if policy is None:
            continue
        wanted: set[tuple[str, str]] = set()
        for state in policy.payload["states"].values():
            scope = state.get("when_component")
            if scope:
                wanted.add((scope["local_key"], scope["offense"]))
            if state.get("component_suspends"):
                wanted.update((component.local_key, component.source_ref) for component in compiled.components)
        for local_key, offense_ref in wanted:
            scopes.add(completion_mod.component_instance_for(compiled, target, local_key, offense_ref))
    return _normalize_instances(scopes)


def _completion_children(compiled: CompiledOffense, dispositions: Mapping[relation_mod.RelationInstanceKey, str], suspended_slots: Sequence[str], state: Mapping[str, object] | None, lines: list[str], emitted: set[str]) -> list[tuple[str, str]]:
    children: list[tuple[str, str]] = []
    global_suspended = frozenset(suspended_slots)
    component_suspensions = state.get("component_suspends") if state else None
    if component_suspensions:
        by_local = {item["local_key"]: frozenset(item["slots"]) for item in component_suspensions}
        for component in compiled.components:
            if component.component_kind != "offense" or component.resolved_kind not in {"offense", "derived_offense"}:
                raise ScallopBackendContractError("component-scoped completion requires direct offense-family components")
            for slot in SLOT_NAMES:
                expression = component.compiled_content.slots[slot]
                if slot not in global_suspended and slot not in by_local.get(component.local_key, frozenset()) and expression is not None:
                    children.append((_emit_expression(expression, lines, emitted), component.source_ref))
    else:
        for slot in SLOT_NAMES:
            expression = compiled.slots[slot]
            if slot not in global_suspended and expression is not None:
                children.append((_emit_expression(expression, lines, emitted), compiled.id))
    for key, _binding in _ordered_relation_instances(compiled):
        if dispositions.get(key) != "suspend":
            helper = _relation_helper_name(compiled.id, key)
            if helper not in emitted:
                _emit_relation_lookup(helper, key, lines)
                emitted.add(helper)
            children.append((helper, compiled.id))
    if state and state.get("requires") is not None:
        expression = expressions.canonicalize(state["requires"])
        assert expression is not None
        children.append((_emit_expression(expression, lines, emitted), _state_scope_ref(compiled, state)))
    return children


def _normalize_compiled_offenses(
    registry: DefinitionRegistry, compiled_offenses: Iterable[CompiledOffense]
) -> tuple[CompiledOffense, ...]:
    values = _normalize_compiled_offenses_unchecked(compiled_offenses)
    for compiled in values:
        entry = registry.get(compiled.id)
        if entry is None or entry.kind not in {"offense", "derived_offense"}:
            raise ScallopBackendContractError(
                f"CompiledOffense id is not a loaded offense root: {compiled.id!r}"
            )
        if set(compiled.slots) != set(SLOT_NAMES):
            raise ScallopBackendContractError(
                f"CompiledOffense {compiled.id!r} must contain exactly the fixed slot set"
            )
        for slot in SLOT_NAMES:
            expression = compiled.slots[slot]
            if expression is None:
                continue
            for ref in canonical_leaf_refs(expression):
                _validate_predicate_ref(registry, ref)
        for key, _binding in _ordered_relation_instances(compiled):
            relation = registry.get(key.relation_ref)
            if relation is None or relation.kind != "relation":
                raise ScallopBackendContractError(
                    f"CompiledOffense {compiled.id!r} has non-RelationDef obligation {key.relation_ref!r}"
                )
    return values


def _normalize_compiled_offenses_unchecked(
    compiled_offenses: Iterable[CompiledOffense],
) -> tuple[CompiledOffense, ...]:
    values = tuple(compiled_offenses)
    if not values:
        raise ScallopBackendContractError("Step 2 requires at least one CompiledOffense")
    ids: set[str] = set()
    for compiled in values:
        if not isinstance(compiled, CompiledOffense):
            raise ScallopBackendContractError("Step 2 roots must be successful CompiledOffense values")
        if compiled.id in ids:
            raise ScallopBackendContractError(f"duplicate CompiledOffense id: {compiled.id!r}")
        ids.add(compiled.id)
    return tuple(sorted(values, key=lambda compiled: compiled.id))


def _validate_instance_roots(
    roots: Sequence[CompiledOffense], instances: Sequence[OffenseInstanceKey]
) -> None:
    roots_by_id = {compiled.id: compiled for compiled in roots}
    for instance in instances:
        if instance.offense_ref not in roots_by_id:
            raise ScallopBackendContractError(
                f"v2_instance has no matching CompiledOffense root: {instance.offense_ref!r}"
            )


def _expected_runtime_relation_keys(
    roots: Sequence[CompiledOffense], instances: Sequence[OffenseInstanceKey]
) -> tuple[RuntimeRelationKey, ...]:
    roots_by_id = {compiled.id: compiled for compiled in roots}
    _validate_instance_roots(roots, instances)
    keys = tuple(
        RuntimeRelationKey(instance=instance, definition_key=relation_key)
        for instance in instances
        for relation_key, _binding in _ordered_relation_instances(roots_by_id[instance.offense_ref])
    )
    if len(set(keys)) != len(keys):
        raise ScallopBackendContractError("CompiledOffense produced duplicate Step 2 relation keys")
    return tuple(sorted(keys, key=_relation_fields))


def _ordered_relation_instances(
    compiled: CompiledOffense,
) -> tuple[tuple[relation_mod.RelationInstanceKey, object], ...]:
    items = tuple(relation_mod.iter_relation_instances(compiled))
    keys = [key for key, _binding in items]
    if len(set(keys)) != len(keys):
        raise ScallopBackendContractError(
            f"CompiledOffense {compiled.id!r} has duplicate definition-time relation obligations"
        )
    return tuple(sorted(items, key=lambda item: _definition_relation_fields(item[0])))


def _emit_relation_lookup(
    helper: str, key: relation_mod.RelationInstanceKey, lines: list[str]
) -> None:
    lines.extend(
        f"type {helper}_{suffix}(String, String, String, String)"
        for suffix in ("true", "false", "unknown")
    )
    variables = "c, a, o, i"
    path, relation_ref, left, right = (_scl_string(value) for value in _definition_relation_fields(key))
    terms = f"{variables}, {path}, {relation_ref}, {left}, {right}"
    lines.append(f"rel {helper}_true({variables}) = v2_relation_truth({terms}, \"TRUE\")")
    lines.append(f"rel {helper}_false({variables}) = v2_relation_truth({terms}, \"FALSE\")")
    lines.append(
        f"rel {helper}_unknown({variables}) = v2_relation_key({terms}), "
        f"not {helper}_true({variables}), not {helper}_false({variables})"
    )
    lines.append("")


def _emit_offense_all(helper: str, offense_id: str, children: Sequence[str], lines: list[str]) -> None:
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String)")
    variables = "c, a, i"
    child_variables = f"c, a, {_scl_string(offense_id)}, i"
    universe = f"v2_instance(c, a, {_scl_string(offense_id)}, i)"
    if children:
        lines.append(
            f"rel {helper}_true({variables}) = {universe} and "
            f"{_conjunction(children, 'true', child_variables)}"
        )
        for child in children:
            lines.append(
                f"rel {helper}_false({variables}) = {universe} and "
                f"{child}_false({child_variables})"
            )
    else:
        lines.append(f"rel {helper}_true({variables}) = {universe}")
    lines.append(
        f"rel {helper}_unknown({variables}) = {universe}, "
        f"not {helper}_true({variables}), not {helper}_false({variables})"
    )
    lines.append("")


def _offense_helper_name(offense_id: str) -> str:
    token = hashlib.sha256(offense_id.encode("utf-8")).hexdigest()
    return f"v2_offense_{token}"


def _relation_helper_name(offense_id: str, key: relation_mod.RelationInstanceKey) -> str:
    payload = json.dumps(
        [offense_id, *_definition_relation_fields(key)],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    token = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"v2_relation_{token}"


def run_liability_chain_parity_program(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    work_dir: Path,
    completion_targets: Iterable[OffenseInstanceKey],
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]] = (),
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = (),
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> Mapping[OffenseInstanceKey, LiabilityEvaluation]:
    """Run the approved generic Step 5 liability chain and return typed evaluations.

    The frozen Step 3 and Step 4 programs remain their own public surfaces.
    Step 5 invokes those local Scallop lowerings for the completion, attribution,
    and doctrine-stage boundaries, reconstructs their existing runtime dataclasses,
    and then enforces the existing non-hypothetical chain.  It intentionally does
    not lower Article 263, Article 34, or Article 151 statutory routes.
    """
    return _run_integrated_liability_chain_program(
        registry,
        compiled_offenses,
        evaluation_instances,
        truths,
        work_dir=work_dir,
        completion_targets=completion_targets,
        co_principal_sources=co_principal_sources,
        derivative_links=derivative_links,
        active_doctrines=active_doctrines,
    )


def run_article_263_liability_parity_program(
    registry: DefinitionRegistry,
    compiled_offense: CompiledOffense,
    instance: OffenseInstanceKey,
    truths: CaseTruths,
    *,
    work_dir: Path,
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> LiabilityEvaluation:
    """Run the dedicated Article 263 path without reopening Step 7 orchestration.

    The caller owns the already-surviving Step 7 probe. This backend evaluates
    the route's fourth, frozen injury-result leaf and folds its single existing
    ``StatutoryDeemingObligation`` into direct Elements before scheduling any
    doctrine stage.
    """
    roots = _normalize_compiled_offenses(registry, (compiled_offense,))
    instances = _normalize_instances((instance,))
    _validate_instance_roots(roots, instances)
    if instance.offense_ref != compiled_offense.id:
        raise ScallopBackendContractError("Article 263 instance must match its CompiledOffense")
    statutory_expression = _article_263_expression(registry, compiled_offense)
    inputs, order = _normalize_liability_chain_inputs(
        registry, roots, instances, (instance,), (), (), active_doctrines
    )

    # Completion and direct, completion-adjusted obligations are the frozen
    # Step 5 pre-stage surface. It deliberately has no doctrine target.
    program = _compile_liability_chain_program(registry, roots)
    edb = _render_integrated_liability_chain_edb(registry, roots, instances, truths, inputs)
    queries = _integrated_prestage_queries()
    output = run_program(program + edb, queries, work_dir, name="v2_article_263_prestage")
    rows = {
        query: tuple(tuple(_decode_query_string(value) for value in row) for row in output[query])
        for query in queries
    }
    completion, base_elements = _adapt_article_263_prestage(
        registry, roots, instances, truths, inputs, rows
    )
    statutory_truth = _run_article_263_statutory_truth(
        statutory_expression, instance, registry, truths, work_dir
    )
    if base_elements.evaluation_state == "not_reached":
        return LiabilityEvaluation(
            instance, completion, not_reached(), not_reached(), not_reached(), not_reached(),
            decisive_stage="completion",
        )

    outcomes = (
        ObligationOutcome(StatutoryDeemingObligation(underlying_instance=instance), statutory_truth),
        *base_elements.provenance,
    )
    elements = _elements_stage(fold_all(outcome.truth for outcome in outcomes), outcomes)
    if elements.gate_state != "passes":
        return LiabilityEvaluation(
            instance, completion, elements, not_reached(), not_reached(), not_reached(),
            decisive_stage="elements",
            decisive_obligation=pipeline.decisive_obligation(
                [outcome.obligation for outcome in outcomes if outcome.truth == "FALSE"]
            ),
        )

    stages: dict[tuple[OffenseInstanceKey, str], tuple[str, str]] = {}
    effects: dict[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]] = {}
    active = tuple(doctrine for target, doctrine in inputs.active_doctrines if target == instance)
    _run_one_symbolic_stage(
        registry, roots, instances, truths, inputs, instance, "unlawfulness", active,
        stages, effects, work_dir,
    )
    if stages[(instance, "unlawfulness")][1] == "passes":
        _run_one_symbolic_stage(
            registry, roots, instances, truths, inputs, instance, "culpability", active,
            stages, effects, work_dir,
        )
        if stages[(instance, "culpability")][1] == "passes":
            _run_one_symbolic_stage(
                registry, roots, instances, truths, inputs, instance, "punishability", active,
                stages, effects, work_dir,
            )
    return _adapt_symbolic_chain(
        registry, order, {instance: completion}, {instance: elements}, stages, effects
    )[instance]


def _article_263_expression(
    registry: DefinitionRegistry, compiled: CompiledOffense
) -> CanonicalExpr:
    offense = registry.get(compiled.id)
    constraints = (offense.payload.get("participation_constraints") or {}) if offense else {}
    statutory = constraints.get("statutory_deeming")
    if statutory is None:
        raise ScallopBackendContractError(
            f"{compiled.id!r} has no approved Article 263 statutory_deeming constraint"
        )
    requires = expressions.canonicalize(statutory.get("requires"))
    if requires is None or canonical_leaf_refs(requires) != _ARTICLE_263_PROBE_REFS:
        raise ScallopBackendContractError("Article 263 statutory_deeming constraint is not the checked probe")
    return expressions.combine_all(requires, ("ref", _ARTICLE_263_RESULT_REF))


def _integrated_prestage_queries() -> tuple[str, ...]:
    return (
        COMPLETION_CANDIDATE_QUERY_RELATION,
        COMPLETION_RESULT_QUERY_RELATION,
        COMPLETION_ELEMENTS_QUERY_RELATION,
        ATTRIBUTED_PREDICATE_QUERY_RELATION,
        CONSTITUTIVE_STATUS_QUERY_RELATION,
        CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION,
        ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION,
        ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION,
        ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION,
        COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION,
    )


def _adapt_article_263_prestage(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    inputs: LiabilityChainInputs,
    rows: Mapping[str, Iterable[Sequence[str]]],
) -> tuple[completion_mod.CompletionResult, StageResult]:
    """Rebuild the direct Step 5 prefix without evaluating any doctrine stage."""
    instance = inputs.completion_targets[0]
    roots_by_id = {root.id: root for root in roots}
    by_fields = {_instance_fields(value): value for value in instances}
    candidates, completion_results, completion_elements = validate_completion_query_rows(
        rows[COMPLETION_CANDIDATE_QUERY_RELATION],
        rows[COMPLETION_RESULT_QUERY_RELATION],
        rows[COMPLETION_ELEMENTS_QUERY_RELATION],
        registry=registry,
        compiled_offenses=roots,
        targets=inputs.completion_targets,
    )
    completion = _reconstruct_completion_result(
        registry, roots_by_id[instance.offense_ref], instance, candidates, completion_results
    )
    _attributed, statuses, members = _validate_integrated_participation_rows(
        registry, roots_by_id, instances, truths, inputs, rows
    )
    slot_truths, component_truths, relation_truths, requirement_truths = _validate_obligation_rows(
        rows, roots_by_id, inputs.completion_targets, {instance: completion}, by_fields
    )
    if completion.state in {"unresolved", "not_applicable"} or completion.punishable is False:
        if instance in completion_elements:
            raise ScallopBackendContractError("completion-stopped Article 263 target emitted Elements")
        return completion, not_reached()
    outcomes = _direct_obligation_outcomes(
        roots_by_id[instance.offense_ref], instance, completion, slot_truths, component_truths,
        relation_truths, requirement_truths, statuses, members, False,
    )
    aggregate = fold_all(outcome.truth for outcome in outcomes)
    if completion_elements[instance] != aggregate:
        raise ScallopBackendContractError("Article 263 pre-stage obligation fold disagrees with Elements")
    return completion, _elements_stage(aggregate, outcomes)


def _run_article_263_statutory_truth(
    expression: CanonicalExpr,
    instance: OffenseInstanceKey,
    registry: DefinitionRegistry,
    truths: CaseTruths,
    work_dir: Path,
) -> TruthValue:
    """Run and validate the one-row Article 263 statutory-deeming query."""
    lines = [
        "// v2 Article 263 statutory-deeming truth",
        *_edb_type_declarations(),
        f"type {ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION}(String, String, String, String, String)",
        "",
    ]
    helper = _emit_expression(expression, lines, set())
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(
            f"rel {ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION}(c, a, o, i, {_scl_string(truth)}) = "
            f"{helper}_{suffix}(c, a, o, i)"
        )
    lines.append(f"query {ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION}")
    output = run_program(
        "\n".join(lines) + "\n" + render_case_truths_edb(registry, (instance,), truths),
        (ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION,),
        work_dir,
        name="v2_article_263_statutory",
    )
    rows = tuple(
        tuple(_decode_query_string(value) for value in row)
        for row in output[ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION]
    )
    if len(rows) != 1 or len(rows[0]) != 5 or rows[0][:4] != _instance_fields(instance):
        raise ScallopBackendContractError("Article 263 statutory query must return one authorized row")
    _validate_truth(rows[0][4], "Article 263 statutory deeming")
    return rows[0][4]


def _run_completion_rows(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    targets: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    work_dir: Path,
) -> tuple[
    Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    Mapping[OffenseInstanceKey, tuple[str, str]],
    Mapping[OffenseInstanceKey, TruthValue],
]:
    static = compile_completion_program(registry, roots)
    policies = {root.id: completion_mod.completion_policy_for(registry, root.id) for root in roots}
    scope_set = set(_completion_scope_instances(roots, policies, targets))
    scoped_truths = CaseTruths(
        predicate={key: value for key, value in truths.predicate.items() if key[0] in scope_set},
        relation={key: value for key, value in truths.relation.items() if key.instance in scope_set},
    )
    output = run_program(
        static.program + render_completion_edb(registry, roots, targets, scoped_truths),
        (COMPLETION_CANDIDATE_QUERY_RELATION, COMPLETION_RESULT_QUERY_RELATION, COMPLETION_ELEMENTS_QUERY_RELATION),
        work_dir,
        name="v2_step5_completion",
    )
    decoded = {
        query: tuple(tuple(_decode_query_string(value) for value in row) for row in output[query])
        for query in (COMPLETION_CANDIDATE_QUERY_RELATION, COMPLETION_RESULT_QUERY_RELATION, COMPLETION_ELEMENTS_QUERY_RELATION)
    }
    return validate_completion_query_rows(
        decoded[COMPLETION_CANDIDATE_QUERY_RELATION],
        decoded[COMPLETION_RESULT_QUERY_RELATION],
        decoded[COMPLETION_ELEMENTS_QUERY_RELATION],
        registry=registry,
        compiled_offenses=roots,
        targets=targets,
    )


def _reconstruct_completion_result(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    target: OffenseInstanceKey,
    candidates: Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    results: Mapping[OffenseInstanceKey, tuple[str, str]],
) -> completion_mod.CompletionResult:
    policy = completion_mod.completion_policy_for(registry, compiled.id)
    state, punishability = results[target]
    if policy is None:
        if (state, punishability) != ("completed", "TRUE"):
            raise ScallopBackendContractError("no-policy completion result is not completed/TRUE")
        return completion_mod.CompletionResult(state="completed", punishable=True)
    provenance = tuple(
        completion_mod.CompletionCandidateOutcome(
            state=name,
            truth=candidates[(target, name)],
            component_instance=(
                completion_mod.component_instance_for(
                    compiled, target, policy.payload["states"][name]["when_component"]["local_key"],
                    policy.payload["states"][name]["when_component"]["offense"],
                )
                if policy.payload["states"][name].get("when_component") else None
            ),
        )
        for name in completion_mod.DERIVABLE_STATES if name in policy.payload["states"]
    )
    if state in {"unresolved", "not_applicable"}:
        return completion_mod.CompletionResult(state=state, provenance=provenance)
    policy_state = policy.payload["states"].get(state)
    if policy_state is None or punishability not in {"TRUE", "FALSE"}:
        raise ScallopBackendContractError("completion result is not an authored derived state")
    scope = policy_state.get("when_component")
    return completion_mod.CompletionResult(
        state=state,
        punishable=punishability == "TRUE",
        suspended_slots=frozenset(policy_state.get("suspends") or ()),
        component_suspended_slots={
            item["local_key"]: frozenset(item["slots"])
            for item in policy_state.get("component_suspends") or ()
        },
        relation_dispositions=_state_relation_dispositions(compiled, policy_state),
        additional_requirements=expressions.canonicalize(policy_state.get("requires")),
        additional_requirements_instance=(
            completion_mod.component_instance_for(compiled, target, scope["local_key"], scope["offense"])
            if scope else None
        ),
        provenance=provenance,
    )


def _normalize_liability_chain_inputs(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    completion_targets: Iterable[OffenseInstanceKey],
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]],
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]],
) -> tuple[LiabilityChainInputs, tuple[OffenseInstanceKey, ...]]:
    targets = _normalize_instances(completion_targets)
    instance_set = set(instances)
    if not set(targets) <= instance_set:
        raise ScallopBackendContractError("completion target must be an authorized evaluation instance")
    policy = participation_mod.participation_policy_for(registry)
    source_values = tuple(co_principal_sources)
    if len(set(source_values)) != len(source_values):
        raise ScallopBackendContractError("co-principal sources must be deduplicated")
    for value in source_values:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ScallopBackendContractError("co-principal source must be (target, source)")
        target, source = value
        if target not in targets or source not in instance_set or target.case_id != source.case_id:
            raise ScallopBackendContractError("co-principal source has an unauthorized or incompatible endpoint")
        offense = registry.get(target.offense_ref)
        if policy is None or offense is None or not _co_principal_enabled(policy, offense):
            raise ScallopBackendContractError("co-principal target has no enabled co_principal mode")

    links = tuple(derivative_links)
    if not targets and not links:
        raise ScallopBackendContractError("Step 5 requires at least one completion target or derivative accessory")
    if len(set(links)) != len(links):
        raise ScallopBackendContractError("derivative links must be deduplicated")
    accessory_links: dict[OffenseInstanceKey, tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = {}
    for value in links:
        if not isinstance(value, tuple) or len(value) != 3:
            raise ScallopBackendContractError("derivative link must be (accessory, principal, mode)")
        accessory, principal, mode = value
        if accessory in accessory_links:
            raise ScallopBackendContractError("derivative accessory must have exactly one link")
        if accessory not in instance_set or principal not in instance_set or accessory.case_id != principal.case_id:
            raise ScallopBackendContractError("derivative link has an unauthorized or incompatible endpoint")
        offense = registry.get(accessory.offense_ref)
        modes = {} if policy is None else policy.payload.get("modes") or {}
        if mode not in _DERIVATIVE_MODES or mode not in modes or offense is None or _mode_disabled(offense, mode):
            raise ScallopBackendContractError("derivative link mode is absent or disabled for accessory offense")
        accessory_links[accessory] = value
    if set(targets) & set(accessory_links):
        raise ScallopBackendContractError("an instance cannot be both completion and derivative route")
    universe = set(targets) | set(accessory_links)
    if any(principal not in universe for _accessory, principal, _mode in links):
        raise ScallopBackendContractError("derivative principal must be an independent Step 5 result instance")

    active = tuple(active_doctrines)
    if len(set(active)) != len(active):
        raise ScallopBackendContractError("active doctrines must be deduplicated")
    for value in active:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ScallopBackendContractError("active doctrine must be (instance, doctrine_ref)")
        instance, doctrine_ref = value
        doctrine = registry.get(doctrine_ref)
        if instance not in universe or doctrine is None or doctrine.kind != "doctrine":
            raise ScallopBackendContractError("active doctrine must target a Step 5 result instance")
        if doctrine.payload.get("stage") not in _STAGE_NAMES:
            raise ScallopBackendContractError("active doctrine has invalid checked stage")

    # Principal-before-accessory is the only available semantics.  Reject cycles
    # rather than silently choosing a fixed point that the Python runtime lacks.
    ordered: list[OffenseInstanceKey] = []
    visiting: set[OffenseInstanceKey] = set()
    visited: set[OffenseInstanceKey] = set()
    def visit(instance: OffenseInstanceKey) -> None:
        if instance in visited:
            return
        if instance in visiting:
            raise ScallopBackendContractError("derivative links must form an acyclic DAG")
        visiting.add(instance)
        if instance in accessory_links:
            visit(accessory_links[instance][1])
        visiting.remove(instance)
        visited.add(instance)
        ordered.append(instance)
    for instance in sorted(universe, key=_instance_fields):
        visit(instance)
    return (
        LiabilityChainInputs(
            completion_targets=targets,
            co_principal_sources=tuple(sorted(source_values, key=lambda value: (*_instance_fields(value[0]), *_instance_fields(value[1])))),
            derivative_links=tuple(sorted(links, key=lambda value: (*_instance_fields(value[0]), *_instance_fields(value[1]), value[2]))),
            active_doctrines=tuple(sorted(active, key=lambda value: (*_instance_fields(value[0]), value[1]))),
        ),
        tuple(ordered),
    )


def _stage_truth(stage: StageResult) -> TruthValue:
    if stage.gate_state == "passes":
        return "TRUE"
    if stage.gate_state == "fails":
        return "FALSE"
    return "UNKNOWN"


def _reached_stage_results(evaluation: LiabilityEvaluation) -> tuple[tuple[str, StageResult], ...]:
    return (
        ("unlawfulness", evaluation.unlawfulness),
        ("culpability", evaluation.culpability),
        ("punishability", evaluation.punishability),
    )


def _reconstruct_liability_evaluation(
    evaluation: LiabilityEvaluation,
    staged: ParticipationStageQueryResults,
    active: frozenset[str],
    registry: DefinitionRegistry,
) -> LiabilityEvaluation:
    rebuilt: dict[str, StageResult] = {}
    for stage, original in _reached_stage_results(evaluation):
        if original.evaluation_state == "not_reached":
            rebuilt[stage] = not_reached()
            continue
        legal_state, gate_state = staged.stage_results[(evaluation.instance, stage)]
        effects = tuple(
            _reconstruct_applied_effect(registry, doctrine, effect, truth)
            for (instance, doctrine), (effect, truth) in sorted(staged.stage_effects.items(), key=lambda item: item[0][1])
            if instance == evaluation.instance and doctrine in active and registry.get(doctrine).payload["stage"] == stage and truth != "FALSE"
        )
        rebuilt[stage] = StageResult(
            evaluation_state="evaluated", legal_state=legal_state, gate_state=gate_state, effects=effects
        )
    elements = evaluation.elements
    unlawfulness = rebuilt["unlawfulness"]
    culpability = rebuilt["culpability"]
    punishability = rebuilt["punishability"]
    realization = None
    establishment = None
    liability_result = None
    decisive_stage = evaluation.decisive_stage
    decisive_doctrine = None
    if elements.gate_state == "passes" and unlawfulness.gate_state == "passes":
        realization = OffenseRealization(evaluation.instance, elements, unlawfulness)
        if culpability.gate_state == "passes":
            establishment = OffenseEstablishment(evaluation.instance, realization, culpability)
            if punishability.gate_state == "passes":
                liability_result = LiabilityResult(evaluation.instance, establishment, punishability)
                decisive_stage = None
            else:
                decisive_stage = "punishability"
                decisive_doctrine = _single_true_doctrine(punishability)
        else:
            decisive_stage = "culpability"
            decisive_doctrine = _single_true_doctrine(culpability)
    elif elements.gate_state == "passes":
        decisive_stage = "unlawfulness"
        decisive_doctrine = _single_true_doctrine(unlawfulness)
    elif evaluation.completion is None or evaluation.completion.state not in {"unresolved", "not_applicable"}:
        if evaluation.completion is None or evaluation.completion.punishable is not False:
            decisive_stage = "elements"
    return LiabilityEvaluation(
        instance=evaluation.instance,
        completion=evaluation.completion,
        elements=elements,
        unlawfulness=unlawfulness,
        culpability=culpability,
        punishability=punishability,
        realization=realization,
        establishment=establishment,
        liability_result=liability_result,
        decisive_stage=decisive_stage,
        decisive_obligation=evaluation.decisive_obligation,
        decisive_doctrine=decisive_doctrine,
    )


def _reconstruct_applied_effect(
    registry: DefinitionRegistry, doctrine_ref: str, effect: str, truth: TruthValue
) -> AppliedEffect:
    doctrine = registry.get(doctrine_ref)
    if doctrine is None:
        raise ScallopBackendContractError("validated doctrine disappeared during Step 5 reconstruction")
    return AppliedEffect(
        doctrine_ref=doctrine_ref,
        effect=effect,
        stage=doctrine.payload["stage"],
        modifier_ref=doctrine.payload["effect"].get("modifier_ref"),
        truth=truth,
    )


def _single_true_doctrine(stage: StageResult) -> str | None:
    firing = [effect.doctrine_ref for effect in stage.effects if effect.truth == "TRUE"]
    return firing[0] if len(firing) == 1 else None


# --------------------------------------------------------------------------------------------
# Step 5 integrated lowering
# --------------------------------------------------------------------------------------------


def _compile_liability_chain_program(
    registry: DefinitionRegistry, roots: Sequence[CompiledOffense]
) -> str:
    """Compile the integrated Step 5 surface without changing Steps 3/4.

    The standalone Step 4 EDB relations are deliberately *not* rendered here:
    active doctrine remains host input, while stage targets and principal
    realization are produced by this program's preceding symbolic gates.
    """
    lines = [
        "// v2 Step 5 integrated liability-chain program",
        *_edb_type_declarations(),
        "type v2_completion_target_instance(String, String, String, String)",
        "type v2_participation_target(String, String, String, String)",
        "type v2_co_principal_source(String, String, String, String, String, String, String, String)",
        "type v2_derivative_link(String, String, String, String, String, String, String, String, String)",
        "type v2_active_doctrine(String, String, String, String, String)",
        "type v2_stage_effect_target(String, String, String, String, String)",
        "type v2_principal_realization_truth(String, String, String, String, String)",
        "type v2_principal_realization_target(String, String, String, String)",
        "type v2_principal_realization_known_true(String, String, String, String)",
        "type v2_principal_realization_known_false(String, String, String, String)",
        "type v2_attributed_override(String, String, String, String, String)",
        "type v2_constitutive_override(String, String, String, String, String)",
        f"type {COMPLETION_CANDIDATE_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {COMPLETION_RESULT_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {COMPLETION_ELEMENTS_QUERY_RELATION}(String, String, String, String, String)",
        f"type {ATTRIBUTED_PREDICATE_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {CONSTITUTIVE_STATUS_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION}(String, String, String, String, String, String, String, String, String)",
        f"type {DERIVATIVE_REQUIREMENT_QUERY_RELATION}(String, String, String, String, String, String, String, String, String, String)",
        f"type {DERIVATIVE_ELEMENTS_QUERY_RELATION}(String, String, String, String, String, String, String, String, String, String)",
        f"type {STAGE_EFFECT_TRUTH_QUERY_RELATION}(String, String, String, String, String, String, String)",
        f"type {STAGE_EFFECT_RESULT_QUERY_RELATION}(String, String, String, String, String, String, String)",
        f"type {ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION}(String, String, String, String, String, String)",
        f"type {ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION}(String, String, String, String, String, String, String)",
        f"type {ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION}(String, String, String, String, String, String, String, String, String)",
        f"type {COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION}(String, String, String, String, String, String)",
        "",
    ]
    emitted: set[str] = set()
    policy = participation_mod.participation_policy_for(registry)
    if policy is not None:
        for compiled in roots:
            _emit_co_principal_outputs(registry, compiled, policy, lines, emitted)
    lines.append(
        f"rel v2_constitutive_override(c, a, o, i, ref) = "
        f"{CONSTITUTIVE_STATUS_QUERY_RELATION}(c, a, o, i, ref, t)"
    )
    lines.append("")

    for compiled in roots:
        completion_policy = completion_mod.completion_policy_for(registry, compiled.id)
        offense = registry.get(compiled.id)
        status_refs = (
            tuple(sorted(participation_mod.constitutive_status_refs(offense)))
            if policy is not None and offense is not None else ()
        )
        _emit_integrated_completion(compiled, completion_policy, status_refs, lines, emitted)

    lines.extend(
        f"query {query}"
        for query in (
            COMPLETION_CANDIDATE_QUERY_RELATION,
            COMPLETION_RESULT_QUERY_RELATION,
            COMPLETION_ELEMENTS_QUERY_RELATION,
            ATTRIBUTED_PREDICATE_QUERY_RELATION,
            CONSTITUTIVE_STATUS_QUERY_RELATION,
            CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION,
            ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION,
            ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION,
            ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION,
            COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION,
        )
    )
    return "\n".join(lines) + "\n"


def _emit_integrated_completion(
    compiled: CompiledOffense,
    policy: DefinitionEntry | None,
    status_refs: Sequence[str],
    lines: list[str],
    emitted: set[str],
) -> None:
    if policy is None:
        target = f"v2_completion_target_instance(c, a, {_scl_string(compiled.id)}, i)"
        lines.append(
            f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, \"completed\", \"TRUE\") = {target}"
        )
        _emit_integrated_elements(
            compiled, None, None, "completed", status_refs, lines, emitted
        )
        return

    states = policy.payload["states"]
    names = tuple(sorted(name for name in completion_mod.DERIVABLE_STATES if name in states))
    candidates: dict[str, str] = {}
    for name in names:
        state = states[name]
        expression = expressions.canonicalize(state["when"])
        assert expression is not None
        helper = _emit_attribution_aware_expression(expression, lines, emitted)
        candidate = _completion_helper_name("candidate", compiled.id, name)
        _emit_completion_candidate(
            candidate, compiled.id, _state_scope_ref(compiled, state), helper, lines
        )
        candidates[name] = candidate
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {COMPLETION_CANDIDATE_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(name)}, {_scl_string(truth)}) = {candidate}_{suffix}(c, a, i)"
            )
    selected = _emit_completion_selection(compiled.id, names, candidates, lines)
    for name in names:
        state = states[name]
        label = "TRUE" if state["punishable"] else "FALSE"
        lines.append(
            f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(name)}, {_scl_string(label)}) = {selected[name]}(c, a, i)"
        )
        if state["punishable"]:
            _emit_integrated_elements(compiled, state, selected[name], name, status_refs, lines, emitted)
    for state in ("unresolved", "not_applicable"):
        helper = _completion_helper_name("selected", compiled.id, state)
        lines.append(
            f"rel {COMPLETION_RESULT_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(state)}, \"NONE\") = {helper}(c, a, i)"
        )
    lines.append("")


def _emit_integrated_elements(
    compiled: CompiledOffense,
    state: Mapping[str, object] | None,
    selected: str | None,
    state_name: str,
    status_refs: Sequence[str],
    lines: list[str],
    emitted: set[str],
) -> None:
    """Emit selected Elements plus its exact existing-obligation proof rows."""
    helper = _completion_helper_name("integrated_elements", compiled.id, state_name)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String)")
    target = f"v2_completion_target_instance(c, a, {_scl_string(compiled.id)}, i)"
    gate = target if selected is None else f"{target} and {selected}(c, a, i)"
    children: list[tuple[str, str]] = []
    suspended = frozenset((state or {}).get("suspends") or ())
    component_suspensions = (state or {}).get("component_suspends")
    if component_suspensions:
        by_local = {item["local_key"]: frozenset(item["slots"]) for item in component_suspensions}
        for component in compiled.components:
            if component.component_kind != "offense" or component.resolved_kind not in {"offense", "derived_offense"}:
                raise ScallopBackendContractError("component-scoped completion requires direct offense-family components")
            scope = f"c, a, {_scl_string(component.source_ref)}, i"
            for slot in SLOT_NAMES:
                if slot in suspended or slot in by_local.get(component.local_key, frozenset()):
                    continue
                expression = component.compiled_content.slots[slot]
                _emit_component_slot_proof(
                    compiled.id, component.local_key, slot, expression, scope, gate, lines, emitted
                )
                if expression is not None:
                    children.append((_emit_expression(expression, lines, emitted), scope))
    else:
        scope = f"c, a, {_scl_string(compiled.id)}, i"
        for slot in SLOT_NAMES:
            if slot in suspended:
                continue
            expression = compiled.slots[slot]
            _emit_slot_proof(compiled.id, slot, expression, scope, gate, lines, emitted)
            if expression is not None:
                children.append((_emit_elements_aware_expression(expression, lines, emitted), scope))

    dispositions = {} if state is None else _state_relation_dispositions(compiled, state)
    for key, _binding in _ordered_relation_instances(compiled):
        if dispositions.get(key) == "suspend":
            continue
        relation_helper = _relation_helper_name(compiled.id, key)
        if relation_helper not in emitted:
            _emit_relation_lookup(relation_helper, key, lines)
            emitted.add(relation_helper)
        fields = ", ".join(_scl_string(value) for value in _definition_relation_fields(key))
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {fields}, {_scl_string(truth)}) = {gate} and {relation_helper}_{suffix}(c, a, {_scl_string(compiled.id)}, i)"
            )
        children.append((relation_helper, f"c, a, {_scl_string(compiled.id)}, i"))

    if state is not None and state.get("requires") is not None:
        scope_ref = _state_scope_ref(compiled, state)
        scope = f"c, a, {_scl_string(scope_ref)}, i"
        expression = expressions.canonicalize(state["requires"])
        assert expression is not None
        expr_helper = (
            _emit_elements_aware_expression(expression, lines, emitted)
            if scope_ref == compiled.id else _emit_expression(expression, lines, emitted)
        )
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(
                f"rel {COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(state_name)}, {_scl_string(truth)}) = {gate} and {expr_helper}_{suffix}({scope})"
            )
        children.append((expr_helper, scope))

    for ref in status_refs:
        children.append((_emit_optional_constitutive_child(compiled.id, ref, lines), f"c, a, {_scl_string(compiled.id)}, i"))

    if children:
        lines.append(
            f"rel {helper}_true(c, a, i) = {gate} and " + " and ".join(
                f"{child}_true({scope})" for child, scope in children
            )
        )
        for child, scope in children:
            lines.append(f"rel {helper}_false(c, a, i) = {gate} and {child}_false({scope})")
    else:
        lines.append(f"rel {helper}_true(c, a, i) = {gate}")
    lines.append(f"rel {helper}_unknown(c, a, i) = {gate} and not {helper}_true(c, a, i) and not {helper}_false(c, a, i)")
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(
            f"rel {COMPLETION_ELEMENTS_QUERY_RELATION}(c, a, {_scl_string(compiled.id)}, i, {_scl_string(truth)}) = {helper}_{suffix}(c, a, i)"
        )
    lines.append("")


def _emit_slot_proof(
    offense_id: str, slot: str, expression: CanonicalExpr, scope: str, gate: str,
    lines: list[str], emitted: set[str],
) -> None:
    if expression is None:
        lines.append(f"rel {ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(offense_id)}, i, {_scl_string(slot)}, \"TRUE\") = {gate}")
        return
    helper = _emit_elements_aware_expression(expression, lines, emitted)
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(f"rel {ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(offense_id)}, i, {_scl_string(slot)}, {_scl_string(truth)}) = {gate} and {helper}_{suffix}({scope})")


def _emit_component_slot_proof(
    offense_id: str, local_key: str, slot: str, expression: CanonicalExpr, scope: str,
    gate: str, lines: list[str], emitted: set[str],
) -> None:
    if expression is None:
        lines.append(f"rel {ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(offense_id)}, i, {_scl_string(local_key)}, {_scl_string(slot)}, \"TRUE\") = {gate}")
        return
    helper = _emit_expression(expression, lines, emitted)
    for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
        lines.append(f"rel {ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION}(c, a, {_scl_string(offense_id)}, i, {_scl_string(local_key)}, {_scl_string(slot)}, {_scl_string(truth)}) = {gate} and {helper}_{suffix}({scope})")


def _emit_optional_constitutive_child(offense_id: str, ref: str, lines: list[str]) -> str:
    helper = _step4_helper_name("integrated_constitutive", offense_id, ref)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String, String)")
    target = f"v2_participation_target(c, a, {_scl_string(offense_id)}, i)"
    lines.append(f"rel {helper}_true(c, a, o, i) = v2_instance(c, a, o, i) and not {target}")
    lines.append(f"rel {helper}_true(c, a, o, i) = {CONSTITUTIVE_STATUS_QUERY_RELATION}(c, a, o, i, {_scl_string(ref)}, \"TRUE\")")
    lines.append(f"rel {helper}_false(c, a, o, i) = {CONSTITUTIVE_STATUS_QUERY_RELATION}(c, a, o, i, {_scl_string(ref)}, \"FALSE\")")
    lines.append(f"rel {helper}_unknown(c, a, o, i) = {CONSTITUTIVE_STATUS_QUERY_RELATION}(c, a, o, i, {_scl_string(ref)}, \"UNKNOWN\")")
    return helper


def _emit_integrated_stage_targets(lines: list[str]) -> None:
    lines.append(f"rel v2_stage_effect_target(c, a, o, i, \"unlawfulness\") = {COMPLETION_ELEMENTS_QUERY_RELATION}(c, a, o, i, \"TRUE\")")
    lines.append(f"rel v2_stage_effect_target(c, a, o, i, \"unlawfulness\") = {DERIVATIVE_ELEMENTS_QUERY_RELATION}(c, a, o, i, pc, pa, po, pi, mode, \"TRUE\")")
    lines.append(f"rel v2_stage_effect_target(c, a, o, i, \"culpability\") = {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, \"unlawfulness\", state, \"passes\")")
    lines.append(f"rel v2_stage_effect_target(c, a, o, i, \"punishability\") = {STAGE_EFFECT_RESULT_QUERY_RELATION}(c, a, o, i, \"culpability\", state, \"passes\")")
    lines.append("")


def _emit_integrated_principal_realization(lines: list[str]) -> None:
    lines.append("rel v2_principal_realization_target(pc, pa, po, pi) = v2_derivative_link(c, a, o, i, pc, pa, po, pi, mode)")
    lines.append("rel v2_principal_realization_known_true(c, a, o, i) = v2_stage_effect_result(c, a, o, i, \"unlawfulness\", state, \"passes\")")
    lines.append("rel v2_principal_realization_known_false(c, a, o, i) = v2_completion_result(c, a, o, i, \"not_applicable\", \"NONE\")")
    lines.append("rel v2_principal_realization_known_false(c, a, o, i) = v2_completion_elements_truth(c, a, o, i, \"FALSE\")")
    lines.append("rel v2_principal_realization_known_false(c, a, o, i) = v2_derivative_elements_truth(c, a, o, i, pc, pa, po, pi, mode, \"FALSE\")")
    lines.append("rel v2_principal_realization_known_false(c, a, o, i) = v2_stage_effect_result(c, a, o, i, \"unlawfulness\", state, \"fails\")")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"TRUE\") = v2_principal_realization_target(c, a, o, i) and v2_principal_realization_known_true(c, a, o, i)")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"FALSE\") = v2_principal_realization_target(c, a, o, i) and v2_principal_realization_known_false(c, a, o, i)")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"UNKNOWN\") = v2_principal_realization_target(c, a, o, i) and v2_completion_result(c, a, o, i, \"unresolved\", \"NONE\")")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"UNKNOWN\") = v2_principal_realization_target(c, a, o, i) and v2_completion_result(c, a, o, i, state, \"FALSE\")")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"UNKNOWN\") = v2_principal_realization_target(c, a, o, i) and v2_completion_elements_truth(c, a, o, i, \"UNKNOWN\")")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"UNKNOWN\") = v2_principal_realization_target(c, a, o, i) and v2_derivative_elements_truth(c, a, o, i, pc, pa, po, pi, mode, \"UNKNOWN\")")
    lines.append("rel v2_principal_realization_truth(c, a, o, i, \"UNKNOWN\") = v2_principal_realization_target(c, a, o, i) and v2_stage_effect_result(c, a, o, i, \"unlawfulness\", state, \"unresolved\")")
    lines.append("")


def _emit_elements_aware_expression(
    expression: CanonicalExpr, lines: list[str], emitted: set[str]
) -> str:
    """Expression lowering for direct/co Elements only.

    Constitutive status has priority over sparse attribution exactly where the
    Python pipeline installs its pre-Elements override.  Completion candidates
    and doctrine conditions intentionally use `_emit_attribution_aware_expression`
    instead.
    """
    serialized = canonical_expression_serialization(expression)
    helper = f"v2_elements_expr_{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}"
    if helper in emitted:
        return helper
    op, payload = expression
    children = _ordered_children(op, payload)
    child_helpers = [_emit_elements_aware_expression(child, lines, emitted) for child in children]
    emitted.add(helper)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String, String)")
    variables = "c, a, o, i"
    if op == "ref":
        ref = _scl_string(payload)
        constitutive = f"v2_constitutive_override({variables}, {ref})"
        attributed = f"v2_attributed_override({variables}, {ref})"
        for truth, suffix in (("TRUE", "true"), ("FALSE", "false"), ("UNKNOWN", "unknown")):
            lines.append(f"rel {helper}_{suffix}({variables}) = {CONSTITUTIVE_STATUS_QUERY_RELATION}({variables}, {ref}, {_scl_string(truth)})")
            lines.append(f"rel {helper}_{suffix}({variables}) = v2_instance({variables}) and not {constitutive} and {ATTRIBUTED_PREDICATE_QUERY_RELATION}({variables}, {ref}, {_scl_string(truth)})")
        lines.append(f"rel {helper}_true({variables}) = v2_instance({variables}) and not {constitutive} and not {attributed} and v2_predicate_truth({variables}, {ref}, \"TRUE\")")
        lines.append(f"rel {helper}_false({variables}) = v2_instance({variables}) and not {constitutive} and not {attributed} and v2_predicate_truth({variables}, {ref}, \"FALSE\")")
        lines.append(f"rel {helper}_unknown({variables}) = v2_instance({variables}) and not {constitutive} and not {attributed} and not v2_predicate_truth({variables}, {ref}, \"TRUE\") and not v2_predicate_truth({variables}, {ref}, \"FALSE\")")
    elif op == "all":
        lines.append(f"rel {helper}_true({variables}) = {_conjunction(child_helpers, 'true', variables)}")
        for child in child_helpers:
            lines.append(f"rel {helper}_false({variables}) = {child}_false({variables})")
        lines.append(f"rel {helper}_unknown({variables}) = v2_instance({variables}) and not {helper}_true({variables}) and not {helper}_false({variables})")
    elif op == "any":
        for child in child_helpers:
            lines.append(f"rel {helper}_true({variables}) = {child}_true({variables})")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
        lines.append(f"rel {helper}_unknown({variables}) = v2_instance({variables}) and not {helper}_true({variables}) and not {helper}_false({variables})")
    elif op == "not":
        child = child_helpers[0]
        lines.append(f"rel {helper}_true({variables}) = {child}_false({variables})")
        lines.append(f"rel {helper}_false({variables}) = {child}_true({variables})")
        lines.append(f"rel {helper}_unknown({variables}) = {child}_unknown({variables})")
    elif op == "one_of":
        for index, child in enumerate(child_helpers):
            terms = [f"{child}_true({variables})"] + [
                f"{other}_false({variables})" for other_index, other in enumerate(child_helpers)
                if other_index != index
            ]
            lines.append(f"rel {helper}_true({variables}) = {' and '.join(terms)}")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
        for left, right in combinations(child_helpers, 2):
            lines.append(f"rel {helper}_false({variables}) = {left}_true({variables}) and {right}_true({variables})")
        lines.append(f"rel {helper}_unknown({variables}) = v2_instance({variables}) and not {helper}_true({variables}) and not {helper}_false({variables})")
    else:
        raise ScallopBackendContractError(f"unknown CanonicalExpr operator: {op!r}")
    lines.append("")
    return helper


def _run_integrated_liability_chain_program(
    registry: DefinitionRegistry,
    compiled_offenses: Iterable[CompiledOffense],
    evaluation_instances: Iterable[OffenseInstanceKey],
    truths: CaseTruths,
    *,
    work_dir: Path,
    completion_targets: Iterable[OffenseInstanceKey],
    co_principal_sources: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]],
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    active_doctrines: Iterable[tuple[OffenseInstanceKey, str]],
) -> Mapping[OffenseInstanceKey, LiabilityEvaluation]:
    roots = _normalize_compiled_offenses(registry, compiled_offenses)
    instances = _normalize_instances(evaluation_instances)
    _validate_instance_roots(roots, instances)
    inputs, order = _normalize_liability_chain_inputs(
        registry, roots, instances, completion_targets, co_principal_sources,
        derivative_links, active_doctrines,
    )
    program = _compile_liability_chain_program(registry, roots)
    edb = _render_integrated_liability_chain_edb(registry, roots, instances, truths, inputs)
    queries = (
        COMPLETION_CANDIDATE_QUERY_RELATION, COMPLETION_RESULT_QUERY_RELATION,
        COMPLETION_ELEMENTS_QUERY_RELATION, ATTRIBUTED_PREDICATE_QUERY_RELATION,
        CONSTITUTIVE_STATUS_QUERY_RELATION, CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION,
        ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION, ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION,
        ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION, COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION,
    )
    output = run_program(program + edb, queries, work_dir, name="v2_step5_liability_chain")
    decoded = {
        query: tuple(tuple(_decode_query_string(value) for value in row) for row in output[query])
        for query in queries
    }
    return _adapt_phased_symbolic_chain(
        registry, roots, instances, truths, inputs, order, decoded, work_dir
    )


def _render_integrated_liability_chain_edb(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    inputs: LiabilityChainInputs,
) -> str:
    policies = {root.id: completion_mod.completion_policy_for(registry, root.id) for root in roots}
    scopes = _completion_scope_instances(roots, policies, inputs.completion_targets)
    all_instances = _normalize_instances(set(instances) | set(scopes))
    relation_keys = _expected_runtime_relation_keys(roots, instances)
    co_targets = tuple(sorted({target for target, _source in inputs.co_principal_sources}, key=_instance_fields))
    return render_case_truths_edb(registry, all_instances, truths, relation_keys=relation_keys) + _render_edb_relation(
        "v2_completion_target_instance", [_instance_fields(item) for item in inputs.completion_targets]
    ) + _render_edb_relation(
        "v2_participation_target", [_instance_fields(item) for item in co_targets]
    ) + _render_edb_relation(
        "v2_co_principal_source", [(*_instance_fields(target), *_instance_fields(source)) for target, source in inputs.co_principal_sources]
    ) + _render_edb_relation(
        "v2_derivative_link", [(*_instance_fields(accessory), *_instance_fields(principal), mode) for accessory, principal, mode in inputs.derivative_links]
    ) + _render_edb_relation(
        "v2_active_doctrine", [(*_instance_fields(instance), doctrine) for instance, doctrine in inputs.active_doctrines]
    )


def _adapt_phased_symbolic_chain(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    inputs: LiabilityChainInputs,
    order: Sequence[OffenseInstanceKey],
    rows: Mapping[str, Iterable[Sequence[str]]],
    work_dir: Path,
) -> Mapping[OffenseInstanceKey, LiabilityEvaluation]:
    """Adapt the integrated pre-stage program and symbolic stage phases.

    Scallop determines every gate.  The host only schedules the next frozen
    Step 4 invocation from the preceding validated Scallop result; it never
    asks the Python pipeline to determine reachability.
    """
    by_fields = {_instance_fields(instance): instance for instance in instances}
    roots_by_id = {root.id: root for root in roots}
    candidates, completion_results, completion_elements = validate_completion_query_rows(
        rows[COMPLETION_CANDIDATE_QUERY_RELATION], rows[COMPLETION_RESULT_QUERY_RELATION],
        rows[COMPLETION_ELEMENTS_QUERY_RELATION], registry=registry,
        compiled_offenses=roots, targets=inputs.completion_targets,
    )
    completions = {
        target: _reconstruct_completion_result(registry, roots_by_id[target.offense_ref], target, candidates, completion_results)
        for target in inputs.completion_targets
    }
    _attributed, statuses, members = _validate_integrated_participation_rows(
        registry, roots_by_id, instances, truths, inputs, rows
    )
    slot_truths, component_truths, relation_truths, requirement_truths = _validate_obligation_rows(
        rows, roots_by_id, inputs.completion_targets, completions, by_fields
    )
    co_sources = {
        target: tuple(source for anchored, source in inputs.co_principal_sources if anchored == target)
        for target in inputs.completion_targets
    }
    elements: dict[OffenseInstanceKey, StageResult] = {}
    for target in inputs.completion_targets:
        completion = completions[target]
        if completion.state in {"unresolved", "not_applicable"} or completion.punishable is False:
            if target in completion_elements:
                raise ScallopBackendContractError("completion-stopped target emitted an Elements row")
            elements[target] = not_reached()
            continue
        outcomes = _direct_obligation_outcomes(
            roots_by_id[target.offense_ref], target, completion, slot_truths, component_truths,
            relation_truths, requirement_truths, statuses, members, bool(co_sources[target]),
        )
        aggregate = fold_all(item.truth for item in outcomes)
        if completion_elements[target] != aggregate:
            raise ScallopBackendContractError("per-obligation fold disagrees with completion Elements truth")
        elements[target] = _elements_stage(aggregate, outcomes)

    active_by_instance = {
        instance: tuple(doctrine for anchored, doctrine in inputs.active_doctrines if anchored == instance)
        for instance in order
    }
    stages: dict[tuple[OffenseInstanceKey, str], tuple[str, str]] = {}
    effects: dict[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]] = {}
    evaluations: dict[OffenseInstanceKey, LiabilityEvaluation] = {}
    links_by_accessory = {accessory: (accessory, principal, mode) for accessory, principal, mode in inputs.derivative_links}
    for instance in order:
        if instance in links_by_accessory:
            _accessory, principal, mode = links_by_accessory[instance]
            principal_truth = _principal_realization_from_symbolic(evaluations[principal])
            derivative = run_participation_stage_parity_program(
                registry, roots, instances, truths, work_dir=work_dir,
                derivative_links=[(instance, principal, mode)],
                principal_realization_truths={principal: principal_truth},
            )
            requirement = derivative.derivative_requirements[(instance, principal, mode)]
            aggregate = derivative.derivative_elements[(instance, principal, mode)]
            if aggregate != fold_all((principal_truth, requirement)):
                raise ScallopBackendContractError("derivative obligation fold disagrees with derivative Elements truth")
            elements[instance] = _elements_stage(aggregate, (
                ObligationOutcome(ParticipationDependencyObligation(mode), principal_truth),
                ObligationOutcome(ParticipationRequirementObligation(mode), requirement),
            ))
        element = elements[instance]
        if element.gate_state == "passes":
            _run_one_symbolic_stage(registry, roots, instances, truths, inputs, instance, "unlawfulness", active_by_instance[instance], stages, effects, work_dir)
            if stages[(instance, "unlawfulness")][1] == "passes":
                _run_one_symbolic_stage(registry, roots, instances, truths, inputs, instance, "culpability", active_by_instance[instance], stages, effects, work_dir)
                if stages[(instance, "culpability")][1] == "passes":
                    _run_one_symbolic_stage(registry, roots, instances, truths, inputs, instance, "punishability", active_by_instance[instance], stages, effects, work_dir)
        evaluations[instance] = _adapt_symbolic_chain(
            registry, (instance,), {instance: completions[instance]} if instance in completions else {},
            {instance: elements[instance]},
            {key: value for key, value in stages.items() if key[0] == instance},
            {key: value for key, value in effects.items() if key[0] == instance},
        )[instance]
    return evaluations


def _run_one_symbolic_stage(
    registry: DefinitionRegistry, roots: Sequence[CompiledOffense], instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths, inputs: LiabilityChainInputs, instance: OffenseInstanceKey, stage: str,
    active: Sequence[str], stages: dict[tuple[OffenseInstanceKey, str], tuple[str, str]],
    effects: dict[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]], work_dir: Path,
) -> None:
    source_pairs = tuple(pair for pair in inputs.co_principal_sources if pair[0] == instance)
    active_stage = tuple(
        (instance, doctrine) for doctrine in active
        if registry.get(doctrine).payload["stage"] == stage
    )
    output = run_participation_stage_parity_program(
        registry, roots, instances, truths, work_dir=work_dir,
        participation_targets=[instance] if source_pairs else (),
        co_principal_sources=source_pairs,
        active_doctrines=active_stage,
        stage_effect_targets=[(instance, stage)],
    )
    stages[(instance, stage)] = output.stage_results[(instance, stage)]
    effects.update(output.stage_effects)


def _principal_realization_from_symbolic(principal: LiabilityEvaluation) -> TruthValue:
    if principal.realization is not None:
        return "TRUE"
    if principal.completion is not None:
        if principal.completion.state == "not_applicable":
            return "FALSE"
        if principal.completion.state == "unresolved" or principal.completion.punishable is False:
            return "UNKNOWN"
    if principal.elements.gate_state == "fails" or principal.unlawfulness.gate_state == "fails":
        return "FALSE"
    return "UNKNOWN"


def _validate_and_adapt_integrated_chain(
    registry: DefinitionRegistry,
    roots: Sequence[CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    inputs: LiabilityChainInputs,
    order: Sequence[OffenseInstanceKey],
    rows: Mapping[str, Iterable[Sequence[str]]],
) -> Mapping[OffenseInstanceKey, LiabilityEvaluation]:
    by_fields = {_instance_fields(instance): instance for instance in instances}
    roots_by_id = {root.id: root for root in roots}
    candidates, completion_results, completion_elements = validate_completion_query_rows(
        rows[COMPLETION_CANDIDATE_QUERY_RELATION], rows[COMPLETION_RESULT_QUERY_RELATION],
        rows[COMPLETION_ELEMENTS_QUERY_RELATION], registry=registry,
        compiled_offenses=roots, targets=inputs.completion_targets,
    )
    completions = {
        target: _reconstruct_completion_result(registry, roots_by_id[target.offense_ref], target, candidates, completion_results)
        for target in inputs.completion_targets
    }
    _attributed, statuses, members = _validate_integrated_participation_rows(
        registry, roots_by_id, instances, truths, inputs, rows
    )
    slot_truths, component_truths, relation_truths, requirement_truths = _validate_obligation_rows(
        rows, roots_by_id, inputs.completion_targets, completions, by_fields
    )
    co_sources = {
        target: tuple(sorted((source for anchored, source in inputs.co_principal_sources if anchored == target), key=_instance_fields))
        for target in inputs.completion_targets
    }
    elements: dict[OffenseInstanceKey, StageResult] = {}
    for target in inputs.completion_targets:
        completion = completions[target]
        if completion.state in {"unresolved", "not_applicable"} or completion.punishable is False:
            if target in completion_elements:
                raise ScallopBackendContractError("completion-stopped target emitted an Elements row")
            elements[target] = not_reached()
            continue
        outcomes = _direct_obligation_outcomes(
            roots_by_id[target.offense_ref], target, completion, slot_truths, component_truths,
            relation_truths, requirement_truths, statuses, members, bool(co_sources[target]),
        )
        truth = fold_all(item.truth for item in outcomes)
        if completion_elements[target] != truth:
            raise ScallopBackendContractError("per-obligation fold disagrees with completion Elements truth")
        elements[target] = _elements_stage(truth, outcomes)

    links = set(inputs.derivative_links)
    derivative_requirements = _validate_derivative_rows(
        rows[DERIVATIVE_REQUIREMENT_QUERY_RELATION], DERIVATIVE_REQUIREMENT_QUERY_RELATION, links, by_fields
    )
    derivative_elements = _validate_derivative_rows(
        rows[DERIVATIVE_ELEMENTS_QUERY_RELATION], DERIVATIVE_ELEMENTS_QUERY_RELATION, links, by_fields
    )
    for accessory, principal, mode in inputs.derivative_links:
        # Principal truth is validated after the symbolic stage chain below; the
        # aggregate row is retained now so its gate controls Unlawfulness.
        elements[accessory] = _elements_stage(derivative_elements[(accessory, principal, mode)], ())

    stage_results, effects = _validate_integrated_stage_rows(
        registry, inputs, elements, rows, by_fields
    )
    principal_truths = _validate_integrated_principal_rows(
        rows["v2_principal_realization_truth"], inputs.derivative_links, completions,
        elements, stage_results, by_fields,
    )
    for accessory, principal, mode in inputs.derivative_links:
        dependency = principal_truths[principal]
        requirement = derivative_requirements[(accessory, principal, mode)]
        aggregate = fold_all((dependency, requirement))
        if derivative_elements[(accessory, principal, mode)] != aggregate:
            raise ScallopBackendContractError("derivative obligation fold disagrees with derivative Elements truth")
        outcomes = (
            ObligationOutcome(ParticipationDependencyObligation(mode=mode), dependency),
            ObligationOutcome(ParticipationRequirementObligation(mode=mode), requirement),
        )
        elements[accessory] = _elements_stage(aggregate, outcomes)

    return _adapt_symbolic_chain(
        registry, order, completions, elements, stage_results, effects
    )


def _validate_integrated_participation_rows(
    registry: DefinitionRegistry,
    roots_by_id: Mapping[str, CompiledOffense],
    instances: Sequence[OffenseInstanceKey],
    truths: CaseTruths,
    inputs: LiabilityChainInputs,
    rows: Mapping[str, Iterable[Sequence[str]]],
) -> tuple[
    Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]],
]:
    by_fields = {_instance_fields(instance): instance for instance in instances}
    targets = {target for target, _source in inputs.co_principal_sources}
    sources = {
        target: tuple(source for anchored, source in inputs.co_principal_sources if anchored == target)
        for target in targets
    }
    policy = participation_mod.participation_policy_for(registry)
    attributable: set[tuple[OffenseInstanceKey, str]] = set()
    constitutive: set[tuple[OffenseInstanceKey, str]] = set()
    member_expected: set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]] = set()
    if policy is not None:
        for target in targets:
            compiled = roots_by_id[target.offense_ref]
            offense = registry.get(compiled.id)
            assert offense is not None
            slots = participation_mod.effective_attributable_slots(policy, offense)
            refs = set().union(*(canonical_leaf_refs(compiled.slots[slot]) for slot in slots))
            attributable.update((target, ref) for ref in refs)
            for ref in participation_mod.constitutive_status_refs(offense):
                constitutive.add((target, ref))
                for member in (target, *sources[target]):
                    if truths.predicate.get((member, ref), "UNKNOWN") == "TRUE":
                        member_expected.add((target, ref, member))
    attributed = _validate_predicate_output_rows(
        rows[ATTRIBUTED_PREDICATE_QUERY_RELATION], ATTRIBUTED_PREDICATE_QUERY_RELATION,
        attributable, by_fields,
    )
    statuses = _validate_predicate_output_rows(
        rows[CONSTITUTIVE_STATUS_QUERY_RELATION], CONSTITUTIVE_STATUS_QUERY_RELATION,
        constitutive, by_fields,
    )
    members = _validate_member_rows(rows[CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION], member_expected, by_fields)
    return attributed, statuses, members


def _validate_obligation_rows(
    rows: Mapping[str, Iterable[Sequence[str]]],
    roots_by_id: Mapping[str, CompiledOffense],
    targets: Sequence[OffenseInstanceKey],
    completions: Mapping[OffenseInstanceKey, completion_mod.CompletionResult],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> tuple[
    Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    Mapping[tuple[OffenseInstanceKey, str, str], TruthValue],
    Mapping[RuntimeRelationKey, TruthValue],
    Mapping[tuple[OffenseInstanceKey, str], TruthValue],
]:
    expected_slots: set[tuple[OffenseInstanceKey, str]] = set()
    expected_components: set[tuple[OffenseInstanceKey, str, str]] = set()
    expected_relations: set[RuntimeRelationKey] = set()
    expected_requirements: set[tuple[OffenseInstanceKey, str]] = set()
    for target in targets:
        completion = completions[target]
        if completion.state in {"unresolved", "not_applicable"} or completion.punishable is False:
            continue
        compiled = roots_by_id[target.offense_ref]
        if completion.component_suspended_slots:
            for component in compiled.components:
                suspended = completion.component_suspended_slots.get(component.local_key, frozenset())
                for slot in SLOT_NAMES:
                    if slot not in completion.suspended_slots and slot not in suspended:
                        expected_components.add((target, component.local_key, slot))
        else:
            expected_slots.update((target, slot) for slot in SLOT_NAMES if slot not in completion.suspended_slots)
        for key, _binding in relation_mod.iter_relation_instances(compiled):
            if completion.relation_dispositions.get(key) != "suspend":
                expected_relations.add(RuntimeRelationKey(target, key))
        if completion.additional_requirements is not None:
            expected_requirements.add((target, completion.state))
    slots = _validate_simple_obligation_rows(rows[ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION], expected_slots, by_fields, 6)
    components = _validate_simple_obligation_rows(rows[ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION], expected_components, by_fields, 7)
    requirements = _validate_simple_obligation_rows(rows[COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION], expected_requirements, by_fields, 6)
    relations: dict[RuntimeRelationKey, TruthValue] = {}
    for row in rows[ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION]:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == 9 else None
        key = None
        if instance is not None:
            fields = value[4:8]
            key = next((candidate for candidate in expected_relations if candidate.instance == instance and _definition_relation_fields(candidate.definition_key) == fields), None)
        if key is None or key in relations:
            raise ScallopBackendContractError("unexpected or duplicate relation obligation key")
        _validate_truth(value[8], "relation obligation")
        relations[key] = value[8]
    if set(relations) != expected_relations:
        raise ScallopBackendContractError("incomplete relation obligation key set")
    return slots, components, relations, requirements


def _validate_simple_obligation_rows(
    rows: Iterable[Sequence[str]], expected: set[tuple],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey], length: int,
) -> Mapping[tuple, TruthValue]:
    actual: dict[tuple, TruthValue] = {}
    for row in rows:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == length else None
        key = (instance, *value[4:-1]) if instance is not None else None
        if key not in expected or key in actual:
            raise ScallopBackendContractError("unexpected or duplicate obligation key")
        _validate_truth(value[-1], "obligation")
        actual[key] = value[-1]
    if set(actual) != expected:
        raise ScallopBackendContractError("incomplete obligation key set")
    return actual


def _direct_obligation_outcomes(
    compiled: CompiledOffense,
    target: OffenseInstanceKey,
    completion: completion_mod.CompletionResult,
    slots: Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    components: Mapping[tuple[OffenseInstanceKey, str, str], TruthValue],
    relations: Mapping[RuntimeRelationKey, TruthValue],
    requirements: Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    statuses: Mapping[tuple[OffenseInstanceKey, str], TruthValue],
    members: set[tuple[OffenseInstanceKey, str, OffenseInstanceKey]],
    is_co_principal: bool,
) -> tuple[ObligationOutcome, ...]:
    outcomes: list[ObligationOutcome] = []
    if is_co_principal:
        for ref in sorted(ref for instance, ref in statuses if instance == target):
            satisfying = tuple(sorted((member for instance, member_ref, member in members if instance == target and member_ref == ref), key=_instance_fields))
            outcomes.append(ObligationOutcome(CoPrincipalConstitutiveStatusObligation(ref, satisfying), statuses[(target, ref)]))
    if completion.component_suspended_slots:
        for component in compiled.components:
            for slot in SLOT_NAMES:
                key = (target, component.local_key, slot)
                if key in components:
                    outcomes.append(ObligationOutcome(ComponentSlotObligation(component.local_key, slot), components[key]))
    else:
        for slot in SLOT_NAMES:
            key = (target, slot)
            if key in slots:
                outcomes.append(ObligationOutcome(SlotObligation(slot), slots[key]))
    for key, _binding in relation_mod.iter_relation_instances(compiled):
        runtime = RuntimeRelationKey(target, key)
        if runtime in relations:
            outcomes.append(ObligationOutcome(RelationObligation(runtime), relations[runtime]))
    requirement = (target, completion.state)
    if requirement in requirements:
        outcomes.append(ObligationOutcome(CompletionRequirementObligation(completion.state), requirements[requirement]))
    return tuple(outcomes)


def _elements_stage(truth: TruthValue, outcomes: Sequence[ObligationOutcome]) -> StageResult:
    return StageResult(
        evaluation_state="evaluated",
        legal_state=pipeline.ELEMENTS_STATE.get(truth, "unresolved"),
        gate_state=pipeline.ELEMENTS_GATE.get(truth, "unresolved"),
        provenance=tuple(outcomes),
    )


def _validate_integrated_stage_rows(
    registry: DefinitionRegistry,
    inputs: LiabilityChainInputs,
    elements: Mapping[OffenseInstanceKey, StageResult],
    rows: Mapping[str, Iterable[Sequence[str]]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> tuple[
    Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]],
    Mapping[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]],
]:
    raw = tuple(tuple(row) for row in rows[STAGE_EFFECT_RESULT_QUERY_RELATION])
    grouped = {stage: tuple(row for row in raw if len(row) == 7 and row[4] == stage) for stage in _STAGE_NAMES}
    expected_u = {(instance, "unlawfulness") for instance, result in elements.items() if result.gate_state == "passes"}
    validated: dict[tuple[OffenseInstanceKey, str], tuple[str, str]] = {}
    validated.update(_validate_stage_result_rows(grouped["unlawfulness"], expected_u, by_fields))
    expected_c = {(instance, "culpability") for (instance, _stage), (_legal, gate) in validated.items() if _stage == "unlawfulness" and gate == "passes"}
    validated.update(_validate_stage_result_rows(grouped["culpability"], expected_c, by_fields))
    expected_p = {(instance, "punishability") for (instance, _stage), (_legal, gate) in validated.items() if _stage == "culpability" and gate == "passes"}
    validated.update(_validate_stage_result_rows(grouped["punishability"], expected_p, by_fields))
    if sum(len(value) for value in grouped.values()) != len(raw):
        raise ScallopBackendContractError("stage-result row has invalid stage")
    doctrine_by_ref = {entry.id: entry for entry in _checked_doctrines(registry)}
    expected_effects = {
        (instance, doctrine)
        for instance, doctrine in inputs.active_doctrines
        if (instance, doctrine_by_ref[doctrine].payload["stage"]) in set(validated)
    }
    effects = _validate_stage_effect_rows(
        rows[STAGE_EFFECT_TRUTH_QUERY_RELATION], expected_effects, doctrine_by_ref, by_fields
    )
    return validated, effects


def _validate_integrated_principal_rows(
    rows: Iterable[Sequence[str]],
    links: Sequence[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    completions: Mapping[OffenseInstanceKey, completion_mod.CompletionResult],
    elements: Mapping[OffenseInstanceKey, StageResult],
    stages: Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]],
    by_fields: Mapping[tuple[str, str, str, str], OffenseInstanceKey],
) -> Mapping[OffenseInstanceKey, TruthValue]:
    expected = {principal for _accessory, principal, _mode in links}
    actual: dict[OffenseInstanceKey, TruthValue] = {}
    for row in rows:
        value = tuple(row)
        instance = by_fields.get(value[:4]) if len(value) == 5 else None
        if instance not in expected or instance in actual:
            raise ScallopBackendContractError("unexpected or duplicate principal realization key")
        _validate_truth(value[4], "principal realization")
        actual[instance] = value[4]
    if set(actual) != expected:
        raise ScallopBackendContractError("incomplete principal realization key set")
    for principal in expected:
        completion = completions.get(principal)
        elements_result = elements[principal]
        u_gate = stages.get((principal, "unlawfulness"), (None, None))[1]
        expected_truth: TruthValue
        if u_gate == "passes":
            expected_truth = "TRUE"
        elif completion is not None and completion.state == "not_applicable" or elements_result.gate_state == "fails" or u_gate == "fails":
            expected_truth = "FALSE"
        else:
            expected_truth = "UNKNOWN"
        if actual[principal] != expected_truth:
            raise ScallopBackendContractError("principal realization row disagrees with symbolic chain")
    return actual


def _adapt_symbolic_chain(
    registry: DefinitionRegistry,
    order: Sequence[OffenseInstanceKey],
    completions: Mapping[OffenseInstanceKey, completion_mod.CompletionResult],
    elements: Mapping[OffenseInstanceKey, StageResult],
    stage_results: Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]],
    effects: Mapping[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]],
) -> Mapping[OffenseInstanceKey, LiabilityEvaluation]:
    result: dict[OffenseInstanceKey, LiabilityEvaluation] = {}
    for instance in order:
        completion = completions.get(instance)
        element = elements[instance]
        if element.evaluation_state == "not_reached":
            result[instance] = LiabilityEvaluation(
                instance, completion, element, not_reached(), not_reached(), not_reached(),
                decisive_stage="completion",
            )
            continue
        if element.gate_state != "passes":
            result[instance] = LiabilityEvaluation(
                instance, completion, element, not_reached(), not_reached(), not_reached(),
                decisive_stage="elements", decisive_obligation=pipeline.decisive_obligation(
                    [item.obligation for item in element.provenance if item.truth == "FALSE"]
                ),
            )
            continue
        unlawfulness = _adapt_stage(instance, "unlawfulness", stage_results, effects, registry)
        if unlawfulness.gate_state != "passes":
            result[instance] = LiabilityEvaluation(
                instance, completion, element, unlawfulness, not_reached(), not_reached(),
                decisive_stage="unlawfulness", decisive_doctrine=pipeline._decisive_doctrine(unlawfulness),
            )
            continue
        realization = OffenseRealization(instance, element, unlawfulness)
        culpability = _adapt_stage(instance, "culpability", stage_results, effects, registry)
        if culpability.gate_state != "passes":
            result[instance] = LiabilityEvaluation(
                instance, completion, element, unlawfulness, culpability, not_reached(),
                realization=realization, decisive_stage="culpability",
                decisive_doctrine=pipeline._decisive_doctrine(culpability),
            )
            continue
        establishment = OffenseEstablishment(instance, realization, culpability)
        punishability = _adapt_stage(instance, "punishability", stage_results, effects, registry)
        if punishability.gate_state != "passes":
            result[instance] = LiabilityEvaluation(
                instance, completion, element, unlawfulness, culpability, punishability,
                realization=realization, establishment=establishment, decisive_stage="punishability",
                decisive_doctrine=pipeline._decisive_doctrine(punishability),
            )
            continue
        result[instance] = LiabilityEvaluation(
            instance, completion, element, unlawfulness, culpability, punishability,
            realization=realization, establishment=establishment,
            liability_result=LiabilityResult(instance, establishment, punishability),
        )
    return result


def _adapt_stage(
    instance: OffenseInstanceKey,
    stage: str,
    results: Mapping[tuple[OffenseInstanceKey, str], tuple[str, str]],
    effects: Mapping[tuple[OffenseInstanceKey, str], tuple[str, TruthValue]],
    registry: DefinitionRegistry,
) -> StageResult:
    legal_state, gate_state = results[(instance, stage)]
    applied = tuple(
        _reconstruct_applied_effect(registry, doctrine, effect, truth)
        for (anchored, doctrine), (effect, truth) in sorted(effects.items(), key=lambda item: item[0][1])
        if anchored == instance and registry.get(doctrine).payload["stage"] == stage and truth != "FALSE"
    )
    return StageResult("evaluated", legal_state, gate_state, effects=applied)


def _normalize_roots(
    registry: DefinitionRegistry, roots: Iterable[ExpressionRoot]
) -> tuple[ExpressionRoot, ...]:
    values = _normalize_root_ids(roots)
    for root in values:
        if root.expression is None:
            raise ScallopBackendContractError("Step 1 ExpressionRoot.expression must be non-None")
        for ref in canonical_leaf_refs(root.expression):
            _validate_predicate_ref(registry, ref)
    return values


def _normalize_root_ids(roots: Iterable[ExpressionRoot]) -> tuple[ExpressionRoot, ...]:
    values = tuple(roots)
    if not values:
        raise ScallopBackendContractError("Step 1 requires at least one ExpressionRoot")
    ids: set[str] = set()
    for root in values:
        if not isinstance(root, ExpressionRoot):
            raise ScallopBackendContractError("roots must contain ExpressionRoot values")
        if not _EXPRESSION_ID.fullmatch(root.expression_id):
            raise ScallopBackendContractError(f"invalid compiler-private expression_id: {root.expression_id!r}")
        if root.expression_id in ids:
            raise ScallopBackendContractError(f"duplicate expression_id: {root.expression_id!r}")
        ids.add(root.expression_id)
    return tuple(sorted(values, key=lambda root: (root.expression_id, canonical_expression_serialization(root.expression))))


def _normalize_instances(instances: Iterable[OffenseInstanceKey]) -> tuple[OffenseInstanceKey, ...]:
    values = tuple(instances)
    if len(set(values)) != len(values):
        raise ScallopBackendContractError("v2_instance values must be unique")
    if not all(isinstance(instance, OffenseInstanceKey) for instance in values):
        raise ScallopBackendContractError("v2_instance values must be OffenseInstanceKey")
    return tuple(sorted(values, key=_instance_fields))


def _normalize_relation_keys(
    registry: DefinitionRegistry,
    keys: Iterable[RuntimeRelationKey],
    instances: set[OffenseInstanceKey],
) -> tuple[RuntimeRelationKey, ...]:
    values = tuple(keys)
    if len(set(values)) != len(values):
        raise ScallopBackendContractError("v2_relation_key values must be unique")
    for key in values:
        if not isinstance(key, RuntimeRelationKey) or key.instance not in instances:
            raise ScallopBackendContractError("relation key must use a registered runtime instance")
        entry = registry.get(key.definition_key.relation_ref)
        if entry is None or entry.kind != "relation":
            raise ScallopBackendContractError(
                f"relation key has non-RelationDef ref: {key.definition_key.relation_ref!r}"
            )
    return tuple(sorted(values, key=_relation_fields))


def _emit_expression(expression: CanonicalExpr, lines: list[str], emitted: set[str]) -> str:
    serialized = canonical_expression_serialization(expression)
    token = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    helper = f"v2_expr_{token}"
    if helper in emitted:
        return helper

    op, payload = expression
    children = _ordered_children(op, payload)
    child_helpers = [_emit_expression(child, lines, emitted) for child in children]
    emitted.add(helper)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String, String)")

    variables = "c, a, o, i"
    if op == "ref":
        ref = _scl_string(payload)
        lines.append(f"rel {helper}_true({variables}) = v2_predicate_truth({variables}, {ref}, \"TRUE\")")
        lines.append(f"rel {helper}_false({variables}) = v2_predicate_truth({variables}, {ref}, \"FALSE\")")
    elif op == "all":
        lines.append(f"rel {helper}_true({variables}) = {_conjunction(child_helpers, 'true', variables)}")
        for child in child_helpers:
            lines.append(f"rel {helper}_false({variables}) = {child}_false({variables})")
    elif op == "any":
        for child in child_helpers:
            lines.append(f"rel {helper}_true({variables}) = {child}_true({variables})")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
    elif op == "not":
        child = child_helpers[0]
        lines.append(f"rel {helper}_true({variables}) = {child}_false({variables})")
        lines.append(f"rel {helper}_false({variables}) = {child}_true({variables})")
    elif op == "one_of":
        for index, child in enumerate(child_helpers):
            terms = [f"{child}_true({variables})"] + [
                f"{other}_false({variables})" for other_index, other in enumerate(child_helpers) if other_index != index
            ]
            lines.append(f"rel {helper}_true({variables}) = {' and '.join(terms)}")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
        for left, right in combinations(child_helpers, 2):
            lines.append(
                f"rel {helper}_false({variables}) = {left}_true({variables}) and {right}_true({variables})"
            )
    else:
        raise ScallopBackendContractError(f"unknown CanonicalExpr operator: {op!r}")

    lines.append(
        f"rel {helper}_unknown({variables}) = v2_instance({variables}), "
        f"not {helper}_true({variables}), not {helper}_false({variables})"
    )
    lines.append("")
    return helper


def _emit_attribution_aware_expression(
    expression: CanonicalExpr, lines: list[str], emitted: set[str]
) -> str:
    """Emit an expression whose leaves read the sparse co-principal override if present."""
    serialized = canonical_expression_serialization(expression)
    helper = f"v2_attributed_expr_{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}"
    if helper in emitted:
        return helper
    op, payload = expression
    children = _ordered_children(op, payload)
    child_helpers = [_emit_attribution_aware_expression(child, lines, emitted) for child in children]
    emitted.add(helper)
    for suffix in ("true", "false", "unknown"):
        lines.append(f"type {helper}_{suffix}(String, String, String, String)")
    variables = "c, a, o, i"
    if op == "ref":
        ref = _scl_string(payload)
        override = f"v2_attributed_override({variables}, {ref})"
        lines.append(
            f"rel {helper}_true({variables}) = {ATTRIBUTED_PREDICATE_QUERY_RELATION}({variables}, {ref}, \"TRUE\")"
        )
        lines.append(
            f"rel {helper}_true({variables}) = v2_instance({variables}) and not {override} and v2_predicate_truth({variables}, {ref}, \"TRUE\")"
        )
        lines.append(
            f"rel {helper}_false({variables}) = {ATTRIBUTED_PREDICATE_QUERY_RELATION}({variables}, {ref}, \"FALSE\")"
        )
        lines.append(
            f"rel {helper}_false({variables}) = v2_instance({variables}) and not {override} and v2_predicate_truth({variables}, {ref}, \"FALSE\")"
        )
        lines.append(
            f"rel {helper}_unknown({variables}) = {ATTRIBUTED_PREDICATE_QUERY_RELATION}({variables}, {ref}, \"UNKNOWN\")"
        )
        lines.append(
            f"rel {helper}_unknown({variables}) = v2_instance({variables}) and not {override} and "
            f"not v2_predicate_truth({variables}, {ref}, \"TRUE\") and not v2_predicate_truth({variables}, {ref}, \"FALSE\")"
        )
    elif op == "all":
        lines.append(f"rel {helper}_true({variables}) = {_conjunction(child_helpers, 'true', variables)}")
        for child in child_helpers:
            lines.append(f"rel {helper}_false({variables}) = {child}_false({variables})")
        lines.append(
            f"rel {helper}_unknown({variables}) = v2_instance({variables}), not {helper}_true({variables}), not {helper}_false({variables})"
        )
    elif op == "any":
        for child in child_helpers:
            lines.append(f"rel {helper}_true({variables}) = {child}_true({variables})")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
        lines.append(
            f"rel {helper}_unknown({variables}) = v2_instance({variables}), not {helper}_true({variables}), not {helper}_false({variables})"
        )
    elif op == "not":
        child = child_helpers[0]
        lines.append(f"rel {helper}_true({variables}) = {child}_false({variables})")
        lines.append(f"rel {helper}_false({variables}) = {child}_true({variables})")
        lines.append(f"rel {helper}_unknown({variables}) = {child}_unknown({variables})")
    elif op == "one_of":
        for index, child in enumerate(child_helpers):
            terms = [f"{child}_true({variables})"] + [
                f"{other}_false({variables})" for other_index, other in enumerate(child_helpers) if other_index != index
            ]
            lines.append(f"rel {helper}_true({variables}) = {' and '.join(terms)}")
        lines.append(f"rel {helper}_false({variables}) = {_conjunction(child_helpers, 'false', variables)}")
        for left, right in combinations(child_helpers, 2):
            lines.append(
                f"rel {helper}_false({variables}) = {left}_true({variables}) and {right}_true({variables})"
            )
        lines.append(
            f"rel {helper}_unknown({variables}) = v2_instance({variables}), not {helper}_true({variables}), not {helper}_false({variables})"
        )
    else:
        raise ScallopBackendContractError(f"unknown CanonicalExpr operator: {op!r}")
    lines.append("")
    return helper


def _step4_helper_name(kind: str, *parts: str) -> str:
    payload = json.dumps([kind, *parts], ensure_ascii=True, separators=(",", ":"))
    return f"v2_step4_{kind}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def _ordered_children(op: str, payload: object) -> tuple[CanonicalExpr, ...]:
    if op == "ref":
        return ()
    if op == "not":
        return (payload,)
    if op in {"all", "any", "one_of"}:
        return tuple(sorted(payload, key=canonical_expression_serialization))
    raise ScallopBackendContractError(f"unknown CanonicalExpr operator: {op!r}")


def _conjunction(children: Sequence[str], suffix: str, variables: str) -> str:
    return " and ".join(f"{child}_{suffix}({variables})" for child in children)


def _expression_data(expression: CanonicalExpr) -> object:
    if expression is None:
        raise ScallopBackendContractError("Step 1 ExpressionRoot.expression must be non-None")
    op, payload = expression
    if op == "ref":
        if not isinstance(payload, str):
            raise ScallopBackendContractError("CanonicalExpr ref payload must be a string")
        return ["ref", payload]
    if op == "not":
        return ["not", _expression_data(payload)]
    if op in {"all", "any", "one_of"}:
        children = tuple(sorted(payload, key=canonical_expression_serialization))
        return [op, [_expression_data(child) for child in children]]
    raise ScallopBackendContractError(f"unknown CanonicalExpr operator: {op!r}")


def _validate_predicate_ref(registry: DefinitionRegistry, ref: object) -> None:
    if not isinstance(ref, str):
        raise ScallopBackendContractError("predicate ref must be a string")
    entry = registry.get(ref)
    if entry is None or entry.kind not in {"ground_fact", "legal_element"}:
        raise ScallopBackendContractError(f"non-predicate ref in Step 1 expression/EDB: {ref!r}")


def _validate_truth(value: object, label: str) -> None:
    if value not in _TRUTHS:
        raise ScallopBackendContractError(f"{label} truth must be one of {sorted(_TRUTHS)}, got {value!r}")


def _instance_fields(instance: OffenseInstanceKey) -> tuple[str, str, str, str]:
    return (instance.case_id, instance.actor_id, instance.offense_ref, instance.occurrence_id)


def _relation_fields(key: RuntimeRelationKey) -> tuple[str, str, str, str, str, str, str, str]:
    relation = key.definition_key
    return (
        *_instance_fields(key.instance),
        *_definition_relation_fields(relation),
    )


def _definition_relation_fields(
    key: relation_mod.RelationInstanceKey,
) -> tuple[str, str, str, str]:
    return (
        json.dumps(list(key.occurrence_path), ensure_ascii=False, separators=(",", ":")),
        key.relation_ref,
        key.left_local_key,
        key.right_local_key,
    )


def _render_edb_relation(name: str, rows: Iterable[Sequence[str]]) -> str:
    ordered = sorted({tuple(row) for row in rows})
    if not ordered:
        return ""
    return "\n".join([
        "",
        f"rel {name} = {{",
        *(f"  ({', '.join(_scl_string(value) for value in row)})," for row in ordered),
        "}",
        "",
    ])


def _scl_string(value: str) -> str:
    if not isinstance(value, str):
        raise ScallopBackendContractError(f"Scallop string value must be str, got {value!r}")
    return json.dumps(value, ensure_ascii=False)


def _decode_query_string(value: str) -> str:
    """Decode the native runner's escaped string capture before key validation."""
    if not isinstance(value, str):
        raise ScallopBackendContractError(f"Scallop query value must be str, got {value!r}")
    try:
        decoded = json.loads(f'"{value}"')
    except json.JSONDecodeError as error:
        raise ScallopBackendContractError(f"invalid escaped Scallop query string: {value!r}") from error
    if not isinstance(decoded, str):  # defensive: JSON string wrapper guarantees this.
        raise ScallopBackendContractError(f"decoded Scallop query value is not a string: {value!r}")
    return decoded


def _result_key(value: tuple[OffenseInstanceKey, str]) -> tuple[str, str, str, str, str]:
    return (*_instance_fields(value[0]), value[1])


__all__ = [
    "ARTICLE_263_STATUTORY_DEEMING_QUERY_RELATION",
    "ATTRIBUTED_PREDICATE_QUERY_RELATION",
    "COMPLETION_CANDIDATE_QUERY_RELATION",
    "COMPLETION_ELEMENTS_QUERY_RELATION",
    "COMPLETION_REQUIREMENT_OBLIGATION_QUERY_RELATION",
    "COMPLETION_RESULT_QUERY_RELATION",
    "CONSTITUTIVE_STATUS_MEMBER_QUERY_RELATION",
    "CONSTITUTIVE_STATUS_QUERY_RELATION",
    "DERIVATIVE_ELEMENTS_QUERY_RELATION",
    "DERIVATIVE_REQUIREMENT_QUERY_RELATION",
    "ELEMENTS_COMPONENT_SLOT_OBLIGATION_QUERY_RELATION",
    "ELEMENTS_RELATION_OBLIGATION_QUERY_RELATION",
    "ELEMENTS_SLOT_OBLIGATION_QUERY_RELATION",
    "OFFENSE_ELEMENTS_QUERY_RELATION",
    "QUERY_RELATION",
    "STAGE_EFFECT_RESULT_QUERY_RELATION",
    "STAGE_EFFECT_TRUTH_QUERY_RELATION",
    "CompletionProgram",
    "ExpressionRoot",
    "LiabilityChainInputs",
    "OffenseElementsProgram",
    "ParticipationStageProgram",
    "ParticipationStageQueryResults",
    "ScallopBackendContractError",
    "canonical_expression_serialization",
    "compile_completion_program",
    "compile_expression_program",
    "compile_offense_elements_program",
    "compile_participation_stage_program",
    "render_case_truths_edb",
    "render_completion_edb",
    "render_offense_elements_edb",
    "render_participation_stage_edb",
    "run_article_263_liability_parity_program",
    "run_expression_parity_program",
    "run_liability_chain_parity_program",
    "run_offense_elements_parity_program",
    "run_participation_stage_parity_program",
    "validate_completion_query_rows",
    "validate_expression_query_rows",
    "validate_offense_elements_query_rows",
    "validate_participation_stage_query_rows",
]
