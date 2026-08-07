"""Lean registry-native path from raw case text to committed Scallop programs.

The neural boundary has two structured responsibilities: select registered units and
assess every predicate of each selected unit against exact spans of the case text.  The
host owns the registry, role contract, completeness checks, SCL asset, execution, and
conclusion.  No retrieval, generic FactGraph, projected rulebase, or model-written
Scallop program is part of this path.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.rulegen.registry import (
    PROJECT_ROOT,
    PredicateIRMissing,
    RuleIRRegistryEntry,
    build_registry,
    resolve_unit,
)
from idpr.rulegen.scallop_runtime import (
    ScallopFactValidationError,
    run_scenario,
    sha256_file,
)


DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
# A 3-state {satisfied, not_satisfied, unknown} grammar let the assessor collapse
# every inferential element (intent, foreseeability, causation) into "unknown"
# whenever the case text lacked a sentence naming the mental state outright — which
# is always, since exam fact patterns narrate conduct, not inner states (see r10/r14
# in docs/handoff/CURRENT.md). Splitting "satisfied" into an explicit and an
# inferential path forces the model to notice the difference instead of defaulting
# past it; both normalize to the same Scallop fact, so the split costs nothing
# downstream.
ASSESSMENT_STATUSES = frozenset(
    {
        "explicitly_supported",
        "inferentially_supported",
        "contradicted",
        "genuinely_unresolved",
    }
)
_ASSESSMENT_STATUS_NORMALIZATION = {
    "explicitly_supported": "satisfied",
    "inferentially_supported": "satisfied",
    "contradicted": "not_satisfied",
    "genuinely_unresolved": "unknown",
}


UNSUPPORTED_BASIS_VALUES = frozenset(
    {
        "not_applicable",
        "no_matching_unit",
        "participation_form_or_classification_uncertainty_only",
    }
)
PARTICIPATION_FORM_BASIS = "participation_form_or_classification_uncertainty_only"


class NativeHostError(ValueError):
    """A closed host contract was violated before symbolic execution."""


def normalize_assessment_status(status: str) -> str:
    """Collapse the 4-state evidentiary-basis grammar to the 3-state Scallop fact.

    Scallop and every legacy consumer of ``evidence[...]['status']`` only know
    satisfied/not_satisfied/unknown; the explicit/inferential distinction exists to
    change what the assessor writes, not what the symbolic layer runs on.
    """

    try:
        return _ASSESSMENT_STATUS_NORMALIZATION[status]
    except KeyError:
        raise NativeHostError(f"unrecognized assessment status: {status!r}") from None


# role_definition (from data/rulegen/p2/p2_native_role_signatures.json) only
# describes the role-tuple shape ("증뢰자 또는 전달자, 이익, 상대 공무원, 전달
# 제3자의 역할 tuple"), never the Korean crime name outright. A router matching
# reported_label against the catalog by name can fail to connect a case fact
# pattern to a unit whose role_definition never says the doctrine's name, even
# though every element of that doctrine is fully carded under it — confirmed
# for bribe_giving, whose role_definition never says "증뢰물전달죄" even though
# assess_art133_sec1_2_* cards cover it completely (job 220007 r14_p1_q2,
# docs/handoff/CURRENT.md "라우팅 정확도"). This is populated only where a
# routing miss has actually confirmed the gap — do not backfill every unit
# speculatively; extend it as the routing regression set below surfaces more.
_LEGAL_LABELS: dict[str, tuple[str, ...]] = {
    "bribe_giving": ("뇌물공여죄", "증뢰물전달죄", "증뢰물취득죄"),
    "third_party_bribery": ("제3자뇌물제공죄", "제3자뇌물요구죄", "제3자뇌물수수죄"),
}


def closed_unit_catalog(*, root: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    """Expose the complete executable allowlist without retrieval or ranking."""

    return [
        {
            "unit_id": entry.unit_id,
            "article_ids": list(entry.article_ids),
            "role_arguments": [
                argument["name"]
                for argument in entry.role_predicate["arguments"]
                if argument["name"] != "case_id"
            ],
            "role_definition": str(entry.role_predicate.get("definition", "")),
            "legal_labels": list(_LEGAL_LABELS.get(entry.unit_id, ())),
            "shared_module": entry.shared_module,
        }
        for entry in build_registry(root).values()
    ]


def closed_issue_selection_schema(
    *, case_id: str, root: Path = PROJECT_ROOT, min_items: int = 1
) -> dict[str, Any]:
    """Return the registry-enumerated issue-selection grammar.

    ``min_items`` is 1 for the model's raw output — it must always name at
    least one issue. It is 0 when the same schema re-validates a selection
    after per-issue rejection has already filtered it: every issue in the
    case can legitimately end up rejected, and that is a degraded case, not
    a payload unusable as a whole.
    """

    unit_ids = sorted(build_registry(root))
    unit_id_enum = {"enum": [*unit_ids, "unsupported"]}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/RuleIRNativeIssueSelection",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "version",
            "case_id",
            "issues",
            "required_subissues",
            "conclusion_sensitive_facts",
            "unresolved_branch_points",
            "alternative_legal_routes",
            "required_issue_labels",
        ],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "issues": {
                "type": "array",
                "minItems": min_items,
                "maxItems": 24,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "issue_id",
                        "reported_label",
                        "source_quote",
                        "candidate_fit_notes",
                        "unit_id",
                        "role_candidates",
                        "depends_on_issue_ids",
                        "closest_allowed_unit_ids",
                        "unsupported_reason",
                        "unsupported_basis",
                    ],
                    "properties": {
                        "issue_id": {
                            "type": "string",
                            "pattern": "^[a-z0-9][a-z0-9_.-]*$",
                        },
                        "reported_label": {"type": "string", "minLength": 1},
                        "source_quote": {"type": "string", "minLength": 1},
                        # Generated *before* unit_id — key order in this dict is
                        # generation order under guided decoding (confirmed:
                        # 01_issue_selection.json field order matches this
                        # dict's declaration order exactly, job 220284). Before
                        # this field existed, unit_id was the second key
                        # emitted, so the model committed to it with zero
                        # comparison tokens in context; unsupported_reason/
                        # unsupported_basis then had to be generated *after*
                        # that commitment, conditioned on it. That is the
                        # mechanism behind the r14_p1_q2 bribe_giving miss: its
                        # own unsupported_reason wrote "bribe_giving을 선택해야
                        # 함" while unit_id, already fixed two fields earlier,
                        # still said "unsupported" (docs/handoff/CURRENT.md
                        # routing-override investigation, job 220254). Diagnosed
                        # by capturing reasoning_content (idpr.neural.vllm_client)
                        # and confirming it was empty for this call — no hidden
                        # thinking phase preceded the JSON, so the JSON's own key
                        # order *is* the only sequence the model reasons in.
                        # candidate_fit_notes forces the comparison against
                        # allowed_units onto the token sequence ahead of
                        # unit_id, for every issue (not just ones that end up
                        # unsupported), so unit_id is now conditioned on
                        # generated comparison tokens instead of preceding them.
                        "candidate_fit_notes": {"type": "string", "minLength": 1},
                        "unit_id": unit_id_enum,
                        "role_candidates": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string",
                                "minLength": 1,
                            },
                        },
                        "depends_on_issue_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        # closest_allowed_unit_ids/unsupported_reason are
                        # diagnostic-only routing trace — the host's symbolic
                        # execution and evaluation never read them. Populated
                        # only when unit_id is "unsupported"
                        # (validate_closed_issue_selection enforces the
                        # contract in both directions: non-empty
                        # unsupported_reason and a real candidate list when
                        # unsupported, both empty otherwise — kept in Python
                        # rather than JSON Schema if/then, which the guidance
                        # backend does not support, see ASSESSMENT_STATUSES
                        # note above). A non-empty closest_allowed_unit_ids next
                        # to unit_id="unsupported" is a routing-accuracy defect
                        # (a real candidate was seen and passed over); an empty
                        # one is either a genuine coverage gap or a catalog/
                        # prompt comprehension problem — see
                        # docs/handoff/CURRENT.md "라우팅 정확도".
                        #
                        # unsupported_basis is NOT diagnostic-only: it is read
                        # by apply_routing_overrides. Three prompt-worded
                        # revisions to make the router commit to a candidate
                        # it already named (docs/handoff/CURRENT.md "decision
                        # 단계 프롬프트 수정 시도") all failed the same way —
                        # the model rephrased the same avoidance each time in
                        # free text. A closed enum cannot be reworded around:
                        # to pick "no_matching_unit" the model has to claim
                        # the candidate's role_definition/legal_labels
                        # genuinely do not cover this fact pattern, not just
                        # gesture at unease. "participation_form_or_
                        # classification_uncertainty_only" means the
                        # candidate's substantive elements are satisfied and
                        # only the participation form (direct/indirect
                        # perpetrator, co-principal, instigator/accessory) or
                        # a sub-classification within the same unit is
                        # unresolved — exactly the doubt legal doctrine treats
                        # as an issue to argue, not a reason to withhold the
                        # base charge. "not_applicable" is the only value
                        # allowed when unit_id != "unsupported" (mirrors the
                        # closest_allowed_unit_ids/unsupported_reason leak
                        # check).
                        "closest_allowed_unit_ids": {
                            "type": "array",
                            "maxItems": 3,
                            "uniqueItems": True,
                            "items": {"enum": unit_ids},
                        },
                        "unsupported_reason": {"type": "string"},
                        "unsupported_basis": {
                            "enum": [
                                "not_applicable",
                                "no_matching_unit",
                                "participation_form_or_classification_uncertainty_only",
                            ]
                        },
                    },
                },
            },
            # The following five arrays let the router declare structure that a
            # flat issue list cannot: which sub-issues a selected issue pulls in,
            # which facts change the applicable doctrine, which unresolved facts
            # must keep an alternative reading of the *same* issue alive, which
            # issues are mutually exclusive alternatives, and which issue must
            # keep its precise legal label rather than being generalized to its
            # parent category (docs/handoff/CURRENT.md "라우팅 출력 확장",
            # diagnosis #1/#2/#3/#5/#6/#7).
            #
            # Every relationship here is expressed as an issue_id, never a
            # unit_id: the same unit_id can legitimately appear on several
            # issues (different actors, different acts), and several issues can
            # legitimately be unit_id="unsupported" — a unit_id reference could
            # not tell those apart, but an issue_id always resolves to exactly
            # one entry in ``issues``. Every issue_id named here (other than
            # ``unsupported``-tolerant fields, which there are none of anymore)
            # still has to appear as its own entry in ``issues`` — these fields
            # do not materialize new issues by themselves, they only let a
            # later pass (assess_routing_completeness) detect when the router
            # named a requirement it did not fulfil, the same "degrade and log,
            # never silently patch" discipline the per-issue rejection path
            # already follows.
            "required_subissues": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "parent_issue_id",
                        "subissue_issue_id",
                        "trigger_source_quote",
                        "reason",
                    ],
                    "properties": {
                        "parent_issue_id": {"type": "string"},
                        "subissue_issue_id": {"type": "string"},
                        "trigger_source_quote": {"type": "string", "minLength": 1},
                        "reason": {"type": "string", "minLength": 1},
                    },
                },
            },
            "conclusion_sensitive_facts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["fact_source_quote", "affects_issue_ids", "reason"],
                    "properties": {
                        "fact_source_quote": {"type": "string", "minLength": 1},
                        "affects_issue_ids": {
                            "type": "array",
                            "minItems": 1,
                            "items": {"type": "string"},
                        },
                        "reason": {"type": "string", "minLength": 1},
                    },
                },
            },
            # A fact staying unresolved does not always require a different
            # unit — the same issue (e.g. a single 특수강도치사 charge) can
            # resolve to different objective-attribution outcomes depending on
            # how one fact (ordinary negligence vs. an independent, serious
            # medical error) is read. ``branch_conditions`` names those
            # readings in prose; it is not a set of units to route.
            "unresolved_branch_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "branch_trigger_quote",
                        "affects_issue_ids",
                        "branch_conditions",
                        "reason",
                    ],
                    "properties": {
                        "branch_trigger_quote": {"type": "string", "minLength": 1},
                        "affects_issue_ids": {
                            "type": "array",
                            "minItems": 1,
                            "items": {"type": "string"},
                        },
                        "branch_conditions": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "reason": {"type": "string", "minLength": 1},
                    },
                },
            },
            "alternative_legal_routes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "primary_issue_id",
                        "alternative_issue_id",
                        "condition",
                        "reason",
                    ],
                    "properties": {
                        "primary_issue_id": {"type": "string"},
                        "alternative_issue_id": {"type": "string"},
                        "condition": {"type": "string", "minLength": 1},
                        "reason": {"type": "string", "minLength": 1},
                    },
                },
            },
            # Named "labels", not "conclusions" — the router never decides a
            # verdict; this only preserves the precise charge/doctrine name
            # (e.g. "특수강도(흉기휴대)") against being generalized to its
            # parent category (e.g. "강도") on the way to the writer.
            "required_issue_labels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["issue_id", "exact_label"],
                    "properties": {
                        "issue_id": {"type": "string"},
                        "exact_label": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def validate_closed_issue_selection(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    case_text: str,
    root: Path = PROJECT_ROOT,
    min_items: int = 1,
) -> list[dict[str, str]]:
    """Reject invented units, invalid roles, forward dependencies, and fake quotes.

    A defect in one issue used to abort the whole case, and on a 26-item sweep
    that lost 15 of them — not because the law was hard but because the router
    named a role the unit does not take, or paraphrased its own quote.  The
    other five or six issues in those cases were fine.  So a per-issue defect
    now demotes that issue: it is returned here and reaches the writer through
    the same path as an issue the symbolic layer could not decide, to be argued
    without symbolic support.  Only a payload that is unusable as a whole —
    schema violations, duplicate issue ids — still raises.
    """

    errors = _schema_errors(
        closed_issue_selection_schema(case_id=case_id, root=root, min_items=min_items),
        payload,
    )
    rejected: list[dict[str, str]] = []
    registry = build_registry(root)
    issues = payload.get("issues", [])
    if isinstance(issues, list):
        issue_ids = [
            item.get("issue_id") for item in issues if isinstance(item, Mapping)
        ]
        if len(issue_ids) != len(set(issue_ids)):
            errors.append("issue_id values must be unique")
        seen: set[str] = set()
        for item in issues:
            if not isinstance(item, Mapping):
                continue
            issue_id = str(item.get("issue_id", ""))
            unit_id = str(item.get("unit_id", ""))
            reported_label = str(item.get("reported_label", "")).strip()
            # (degraded_reason 코드, 사람이 읽을 사유).  The code is what a later
            # analysis groups by; a free sentence alone cannot be counted.
            faults: list[tuple[str, str]] = []
            if not reported_label or reported_label.casefold() == "unsupported":
                faults.append(("missing_label", "쟁점의 죄명이 기재되지 않았다"))
            if item.get("source_quote") not in case_text:
                faults.append(
                    ("quote_not_grounded", "근거로 든 사실관계 인용이 문제 지문에 없다"))
            dependencies = item.get("depends_on_issue_ids", [])
            if isinstance(dependencies, list):
                invalid_dependencies = sorted(set(dependencies) - seen)
                if invalid_dependencies:
                    faults.append((
                        "missing_dependency",
                        f"앞선 쟁점이 아닌 것에 의존한다: {invalid_dependencies}",
                    ))
            entry = registry.get(unit_id)
            if unit_id == "unsupported" and dependencies:
                faults.append((
                    "missing_dependency",
                    "적재되지 않은 쟁점이 다른 쟁점에 의존한다",
                ))
            # closest_allowed_unit_ids/unsupported_reason are diagnostic-only
            # (never read by symbolic execution, the writer, or evaluation),
            # but the contract runs both directions: unsupported must explain
            # itself, and a supported issue must not carry unsupported's
            # diagnostic trace (docs/handoff/CURRENT.md "라우팅 정확도").
            closest_candidates = item.get("closest_allowed_unit_ids", [])
            unsupported_reason = str(item.get("unsupported_reason", "")).strip()
            unsupported_basis = str(item.get("unsupported_basis", "")).strip()
            if unit_id == "unsupported":
                if not unsupported_reason:
                    faults.append((
                        "missing_unsupported_reason",
                        "unsupported를 선택했는데 unsupported_reason이 비어 있다",
                    ))
                if unsupported_basis not in UNSUPPORTED_BASIS_VALUES - {"not_applicable"}:
                    faults.append((
                        "missing_unsupported_basis",
                        "unsupported를 선택했는데 unsupported_basis가 not_applicable이거나 비어 있다",
                    ))
            else:
                if isinstance(closest_candidates, list) and closest_candidates:
                    faults.append((
                        "unsupported_diagnostic_leak",
                        "지원 unit을 선택했는데도 closest_allowed_unit_ids를 채웠다",
                    ))
                if unsupported_reason:
                    faults.append((
                        "unsupported_diagnostic_leak",
                        "지원 unit을 선택했는데도 unsupported_reason을 채웠다",
                    ))
                if unsupported_basis and unsupported_basis != "not_applicable":
                    faults.append((
                        "unsupported_diagnostic_leak",
                        "지원 unit을 선택했는데도 unsupported_basis를 not_applicable이 아닌 값으로 채웠다",
                    ))
            # A participation-form-only issue names exactly one real candidate
            # it believes already covers the substance — apply_routing_overrides
            # promotes it to that candidate's unit_id, so it must carry that
            # candidate's role_candidates now, not the empty {} unsupported
            # issues otherwise carry (docs/handoff/CURRENT.md "decision 단계
            # 프롬프트 수정 시도" — three free-text-only fixes failed because
            # the model could reword its way around a rule with no
            # verifiable side effect; this makes the claim load-bearing:
            # claiming this basis without the roles to back it up degrades
            # the issue instead of promoting it).
            if (
                unit_id == "unsupported"
                and unsupported_basis == PARTICIPATION_FORM_BASIS
                and isinstance(closest_candidates, list)
                and len(closest_candidates) == 1
            ):
                candidate_entry = registry.get(closest_candidates[0])
                if candidate_entry is not None:
                    candidate_roles = {
                        argument["name"]
                        for argument in candidate_entry.role_predicate["arguments"]
                        if argument["name"] != "case_id"
                    }
                    role_candidates = item.get("role_candidates", {})
                    if isinstance(role_candidates, Mapping):
                        unknown_roles = sorted(set(role_candidates) - candidate_roles)
                        missing_roles = sorted(candidate_roles - set(role_candidates))
                        if unknown_roles:
                            faults.append((
                                "unsupported_role",
                                f"참여형태 불확실 후보({closest_candidates[0]})가 받지 않는 "
                                f"당사자 역할을 지정했다: {unknown_roles}",
                            ))
                        if missing_roles:
                            faults.append((
                                "missing_required_role",
                                f"참여형태 불확실 후보({closest_candidates[0]})에 필요한 "
                                f"당사자 역할이 빠졌다: {missing_roles}",
                            ))
            if entry is not None:
                allowed_roles = {
                    argument["name"]
                    for argument in entry.role_predicate["arguments"]
                    if argument["name"] != "case_id"
                }
                role_candidates = item.get("role_candidates", {})
                if isinstance(role_candidates, Mapping):
                    unknown_roles = sorted(set(role_candidates) - allowed_roles)
                    missing_roles = sorted(allowed_roles - set(role_candidates))
                    if unknown_roles:
                        faults.append((
                            "unsupported_role",
                            f"이 죄가 받지 않는 당사자 역할을 지정했다: {unknown_roles}",
                        ))
                    if missing_roles:
                        faults.append((
                            "missing_required_role",
                            f"이 죄에 필요한 당사자 역할이 빠졌다: {missing_roles}",
                        ))
            if faults:
                rejected.append({
                    "issue_id": issue_id,
                    "unit_id": unit_id,
                    "reported_label": reported_label,
                    # The writer must not present a degraded issue's reasoning as
                    # though the symbolic layer stood behind it.
                    "issue_status": "contract_degraded",
                    "symbolic_verdict": "unavailable",
                    "generation_mode": "nonbinding_fallback",
                    "degraded_reason": sorted({code for code, _ in faults}),
                    "reason": "; ".join(text for _, text in faults),
                    # 원문을 남겨야 어느 역할·어느 인용이 틀렸는지 나중에 확인할 수 있다.
                    "reported_selection": dict(item),
                })
            seen.add(issue_id)
    if errors:
        raise NativeHostError("; ".join(errors))
    return rejected


def apply_routing_overrides(
    selection: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Promote a router-named candidate the model declined only over participation form.

    Three prompt-worded attempts to stop the router from naming the exact
    right unit in ``closest_allowed_unit_ids`` and then still writing
    ``unit_id="unsupported"`` all failed the same way (job 220070/220071/
    220074, docs/handoff/CURRENT.md "decision 단계 프롬프트 수정 시도 — 2회
    실패, 롤백"): free text has no verifiable side effect, so the model
    reworded the same avoidance three different ways. ``unsupported_basis``
    replaces that free-text hedge with a closed claim the host can act on:
    declaring ``participation_form_or_classification_uncertainty_only`` with
    exactly one candidate only survives ``validate_closed_issue_selection``
    if ``role_candidates`` already resolves against that candidate's role
    schema — so by the time an issue reaches here, the claim is already
    backed by usable role data, not just a label.

    Call this on the post-rejection-filtered selection (a role mismatch for
    the sole candidate already demoted the issue to ``contract_degraded``
    upstream, so it will not appear here as an override candidate).

    Never fires for ``no_matching_unit`` (a genuine coverage gap, e.g.
    강도상해/강도치상 결합범 — no unit exists to promote to) or for zero or
    more than one candidate (nothing to promote to, or genuinely ambiguous
    — this only resolves the case the model itself narrowed to exactly one).
    Those issues pass through unit_id="unsupported" unchanged and still
    reach the writer as autonomous reasoning via ``_render_verdict_brief``'s
    unsupported tier. The residual participation-form doubt this overrides
    is not discarded — the caller is expected to carry the returned override
    records into the writer's checklist (docs/handoff/CURRENT.md "라우팅
    출력 확장") so the answer still argues direct/indirect perpetrator,
    co-principal, etc. explicitly rather than presenting the promoted charge
    as if participation form were never in question.
    """

    overrides: list[dict[str, Any]] = []
    promoted_issues: list[Any] = []
    for item in selection.get("issues", []):
        if not isinstance(item, Mapping):
            promoted_issues.append(item)
            continue
        unit_id = str(item.get("unit_id", ""))
        basis = str(item.get("unsupported_basis", ""))
        closest = item.get("closest_allowed_unit_ids", [])
        eligible = (
            unit_id == "unsupported"
            and basis == PARTICIPATION_FORM_BASIS
            and isinstance(closest, list)
            and len(closest) == 1
        )
        if not eligible:
            promoted_issues.append(item)
            continue
        promoted_unit_id = str(closest[0])
        overrides.append(
            {
                "issue_id": str(item.get("issue_id", "")),
                "reported_label": str(item.get("reported_label", "")),
                "promoted_unit_id": promoted_unit_id,
                "unsupported_reason": str(item.get("unsupported_reason", "")),
            }
        )
        promoted_issues.append(
            {
                **item,
                "unit_id": promoted_unit_id,
                "closest_allowed_unit_ids": [],
                "unsupported_reason": "",
                "unsupported_basis": "not_applicable",
            }
        )
    return {**selection, "issues": promoted_issues}, overrides


def assess_routing_completeness(selection: Mapping[str, Any]) -> dict[str, Any]:
    """Cross-check the router's declared sub-issue/branch/alternative structure.

    ``required_subissues`` and ``alternative_legal_routes`` let the router
    *name* a doctrine it believes is required without the host guessing at
    role_candidates on its behalf — the router still has to add that doctrine
    as its own sibling entry in ``issues`` and reference it here by issue_id
    (never by unit_id: the same unit_id can recur across several issues, and
    several issues can share unit_id="unsupported", so only an issue_id
    resolves unambiguously). This function only measures whether the router
    followed through. An issue_id named here but absent from ``issues`` is a
    live routing gap (docs/handoff/CURRENT.md diagnosis #1/#2: required cards
    silently dropped, upstream cards not auto-expanding downstream). Gaps are
    returned for logging and later analysis, never used to fail the case and
    never silently patched — the same discipline
    ``validate_closed_issue_selection`` already applies to a defective issue.

    ``unresolved_branch_points`` names alternative factual *readings* of the
    same already-routed issue(s) (``branch_conditions``, prose) rather than
    alternative units to route, so it only needs its ``affects_issue_ids``
    references checked, not a materialization gap.

    Call this on the *final* (post-rejection-filtering) selection, since a
    subissue/alternative that only survived as a since-rejected issue is,
    correctly, still a gap.
    """

    issues = [item for item in selection.get("issues", []) if isinstance(item, Mapping)]
    issue_ids = {str(item.get("issue_id", "")) for item in issues}

    gaps: list[dict[str, Any]] = []

    def _dangling(field: str, ref: Any, record: Mapping[str, Any]) -> bool:
        if str(ref) and str(ref) not in issue_ids:
            gaps.append(
                {
                    "gap_type": "dangling_issue_reference",
                    "field": field,
                    "value": ref,
                    "record": dict(record),
                }
            )
            return True
        return False

    for record in selection.get("required_subissues", []):
        if not isinstance(record, Mapping):
            continue
        if _dangling("parent_issue_id", record.get("parent_issue_id"), record):
            continue
        subissue_issue_id = str(record.get("subissue_issue_id", ""))
        if subissue_issue_id not in issue_ids:
            gaps.append(
                {
                    "gap_type": "required_subissue_missing",
                    "parent_issue_id": record.get("parent_issue_id"),
                    "subissue_issue_id": subissue_issue_id,
                    "reason": record.get("reason"),
                }
            )

    for record in selection.get("alternative_legal_routes", []):
        if not isinstance(record, Mapping):
            continue
        if _dangling("primary_issue_id", record.get("primary_issue_id"), record):
            continue
        alternative_issue_id = str(record.get("alternative_issue_id", ""))
        if alternative_issue_id not in issue_ids:
            gaps.append(
                {
                    "gap_type": "alternative_route_missing",
                    "primary_issue_id": record.get("primary_issue_id"),
                    "alternative_issue_id": alternative_issue_id,
                    "reason": record.get("reason"),
                }
            )

    for record in selection.get("unresolved_branch_points", []):
        if not isinstance(record, Mapping):
            continue
        affects = record.get("affects_issue_ids", [])
        if isinstance(affects, list):
            for ref in affects:
                _dangling("affects_issue_ids", ref, record)

    for record in selection.get("conclusion_sensitive_facts", []):
        if not isinstance(record, Mapping):
            continue
        affects = record.get("affects_issue_ids", [])
        if isinstance(affects, list):
            for ref in affects:
                _dangling("affects_issue_ids", ref, record)

    exact_labels: dict[str, str] = {}
    for record in selection.get("required_issue_labels", []):
        if not isinstance(record, Mapping):
            continue
        issue_id = str(record.get("issue_id", ""))
        label = str(record.get("exact_label", "")).strip()
        if _dangling("issue_id", issue_id, record):
            continue
        if label:
            exact_labels[issue_id] = label

    return {
        "gaps": gaps,
        "exact_labels": exact_labels,
        "required_subissues": list(selection.get("required_subissues", [])),
        "conclusion_sensitive_facts": list(selection.get("conclusion_sensitive_facts", [])),
        "unresolved_branch_points": list(selection.get("unresolved_branch_points", [])),
        "alternative_legal_routes": list(selection.get("alternative_legal_routes", [])),
    }


def diagnose_unsupported_issues(selection: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Split ``unsupported`` issues into routing misses vs. genuine coverage gaps.

    Every issue carries a diagnostic-only ``closest_allowed_unit_ids``/
    ``unsupported_reason`` pair (schema, not an execution contract — nothing
    downstream reads it to change what runs). This turns that trace into one
    finding per ``unsupported`` issue:

    - ``likely_routing_miss`` (``closest_allowed_unit_ids`` non-empty): the
      router itself named a real registered candidate and still declined it —
      this is a routing-accuracy defect (job 220007 r14_p1_q2: ``bribe_giving``
      fully carded the fact pattern and was still passed over), not a rule-base
      gap. Adding more RuleIR coverage will not fix it.
    - otherwise: either a genuine coverage gap (no candidate exists) or the
      catalog/prompt failed to surface a real candidate at all — these are the
      cases worth checking the catalog's ``role_definition``/``legal_labels``
      for (docs/handoff/CURRENT.md "라우팅 정확도").

    This never changes execution — it is read-only trace for the routing
    regression set, same as ``assess_routing_completeness``'s gaps.
    """

    findings: list[dict[str, Any]] = []
    for item in selection.get("issues", []):
        if not isinstance(item, Mapping) or str(item.get("unit_id", "")) != "unsupported":
            continue
        closest = [
            str(unit_id)
            for unit_id in item.get("closest_allowed_unit_ids", [])
            if isinstance(unit_id, str)
        ]
        findings.append(
            {
                "issue_id": str(item.get("issue_id", "")),
                "reported_label": str(item.get("reported_label", "")),
                "closest_allowed_unit_ids": closest,
                "unsupported_reason": str(item.get("unsupported_reason", "")),
                "likely_routing_miss": bool(closest),
            }
        )
    return findings


def selected_predicate_requests(
    *,
    case: Mapping[str, Any],
    selection: Mapping[str, Any],
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Resolve a closed selection into complete raw-text predicate requests."""

    case_id = str(case.get("sub_question_id", ""))
    case_text = str(case.get("question_text", ""))
    # The caller already ran validate_closed_issue_selection on the model's raw
    # output and stripped every issue that failed it; an empty result here is
    # a case where all issues were rejected, not a malformed payload.
    validate_closed_issue_selection(
        selection,
        case_id=case_id,
        case_text=case_text,
        root=root,
        min_items=0,
    )
    requests: list[dict[str, Any]] = []
    for issue in selection["issues"]:
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            requests.append(
                {
                    "issue_id": issue["issue_id"],
                    "unit_id": unit_id,
                    "reported_label": issue["reported_label"],
                    "status": "predicate_ir_missing",
                    "detail": "No registered and audited RuleIR asset exists for this unit.",
                }
            )
            continue
        requests.append(
            {
                "issue_id": issue["issue_id"],
                "unit_id": unit_id,
                "reported_label": issue["reported_label"],
                "depends_on_issue_ids": list(issue["depends_on_issue_ids"]),
                "assessment_request": predicate_assessment_request(
                    case=case,
                    issue=issue,
                    unit_id=unit_id,
                    root=root,
                ),
            }
        )
    return {
        "case_id": case_id,
        "selection_mode": "closed_registry_enum",
        "semantic_search_used": False,
        "requests": requests,
    }


def predicate_assessment_request(
    *,
    case: Mapping[str, Any],
    issue: Mapping[str, Any],
    unit_id: str,
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Load every registered predicate and the raw case text for one unit."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    return {
        "version": "1.0.0",
        "case_id": str(case.get("sub_question_id", "")),
        "case_text": str(case.get("question_text", "")),
        "question_prompt": str(case.get("question_prompt", "")),
        "issue": {
            "issue_id": issue["issue_id"],
            "reported_label": issue["reported_label"],
            "source_quote": issue["source_quote"],
            "role_candidates": dict(issue["role_candidates"]),
        },
        "unit_id": unit_id,
        "role_contract": {
            "predicate": entry.role_predicate["id"],
            "arguments": [
                argument["name"] for argument in entry.role_predicate["arguments"]
            ],
            "definition": str(entry.role_predicate.get("definition", "")),
        },
        "predicates": [
            {
                "predicate_id": predicate["id"],
                "definition": str(predicate.get("definition", predicate["id"])),
                "card_role": predicate.get("card_role"),
                "norm_card_ids": list(predicate.get("norm_card_ids", [])),
                "authority_quotes": [
                    str(source["quote"])
                    for source in predicate.get("source_refs", [])
                    if isinstance(source, Mapping) and source.get("quote")
                ],
            }
            for predicate in entry.commentary_inputs
        ],
        "all_registered_predicates_loaded": True,
    }


def predicate_assessment_schema(
    *, case_id: str, issue_id: str, entry: RuleIRRegistryEntry
) -> dict[str, Any]:
    """Build a strict grammar containing every predicate and every role."""

    role_names = [
        argument["name"] for argument in entry.role_predicate["arguments"]
    ]
    predicate_ids = [predicate["id"] for predicate in entry.commentary_inputs]
    assessment = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "assessment_rationale",
            "status",
            "source_quotes",
            "missing_facts",
        ],
        "properties": {
            # Declared first: under guided decoding, key generation order follows
            # property declaration order, so this has to precede "status" or the
            # model commits to a verdict before writing a single token of
            # reasoning — the same generation-order bug fixed for
            # closed_issue_selection_schema's candidate_fit_notes (docs/handoff/
            # CURRENT.md, job 220284). Unlike the old inference_rationale, this is
            # required non-empty for every status, not just inferentially_
            # supported: a bar/boundary card needs the same "compare definition
            # against case text first" discipline as an inferential element does.
            "assessment_rationale": {"type": "string", "minLength": 1},
            "status": {"enum": sorted(ASSESSMENT_STATUSES)},
            "source_quotes": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "missing_facts": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/RuleIRNativePredicateAssessment",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "version",
            "case_id",
            "issue_id",
            "unit_id",
            "role_values",
            "distinct_entities",
            "assessments",
        ],
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": case_id},
            "issue_id": {"const": issue_id},
            "unit_id": {"const": entry.unit_id},
            "role_values": {
                "type": "object",
                "additionalProperties": False,
                "required": role_names,
                "properties": {
                    role_name: (
                        {"const": case_id}
                        if role_name == "case_id"
                        else {"type": "string", "minLength": 1}
                    )
                    for role_name in role_names
                },
            },
            "distinct_entities": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "string", "minLength": 1},
                },
            },
            "assessments": {
                "type": "object",
                "additionalProperties": False,
                "required": predicate_ids,
                "properties": {
                    predicate_id: assessment for predicate_id in predicate_ids
                },
            },
        },
    }


def validate_predicate_assessment(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    issue_id: str,
    unit_id: str,
    case_text: str,
    root: Path = PROJECT_ROOT,
) -> None:
    """Validate exact predicate coverage and evidence directly against the source."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        raise NativeHostError(entry.detail)
    errors = _schema_errors(
        predicate_assessment_schema(
            case_id=case_id, issue_id=issue_id, entry=entry
        ),
        payload,
    )
    assessments = payload.get("assessments", {})
    if isinstance(assessments, Mapping):
        for predicate_id, item in assessments.items():
            if not isinstance(item, Mapping):
                continue
            status = item.get("status")
            quotes = item.get("source_quotes", [])
            missing = item.get("missing_facts", [])
            if isinstance(quotes, list):
                for quote in quotes:
                    if isinstance(quote, str):
                        parts = [p.strip() for p in re.split(r"[\s\.]+", quote) if len(p.strip()) >= 2]
                        if parts and not any(part in case_text for part in parts):
                            errors.append(
                                f"{predicate_id}: source quote is not in case text: {quote!r}"
                            )
            if status in {"explicitly_supported", "inferentially_supported", "contradicted"}:
                if not quotes:
                    errors.append(
                        f"{predicate_id}: {status} requires at least one source quote"
                    )
                if missing:
                    errors.append(
                        f"{predicate_id}: {status} cannot declare missing facts"
                    )
            # assessment_rationale non-emptiness is already enforced for every
            # status by the schema's minLength (it precedes "status" in
            # generation order — see predicate_assessment_schema).
            if status == "genuinely_unresolved" and not missing:
                errors.append(
                    f"{predicate_id}: genuinely_unresolved requires at least one missing fact"
                )
    if errors:
        raise NativeHostError("; ".join(errors))


def execute_native_unit(
    *,
    issue_id: str,
    unit_id: str,
    case_id: str,
    case_text: str,
    assessment_payload: Mapping[str, Any],
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Run the registered committed SCL after direct raw-text assessment."""

    entry = resolve_unit(unit_id, root=root)
    if isinstance(entry, PredicateIRMissing):
        return entry.to_dict()
    validate_predicate_assessment(
        assessment_payload,
        case_id=case_id,
        issue_id=issue_id,
        unit_id=unit_id,
        case_text=case_text,
        root=root,
    )
    card_by_predicate: dict[str, str] = {}
    for predicate in entry.commentary_inputs:
        cards = predicate.get("norm_card_ids", [])
        if len(cards) != 1:
            raise NativeHostError(
                f"{unit_id}:{predicate['id']} must map to exactly one NormCard"
            )
        card_by_predicate[predicate["id"]] = cards[0]

    scenario_assessments = []
    evidence: dict[str, Any] = {}
    for index, predicate in enumerate(entry.commentary_inputs, 1):
        predicate_id = predicate["id"]
        item = assessment_payload["assessments"][predicate_id]
        normalized_status = normalize_assessment_status(item["status"])
        scenario_assessments.append(
            {
                "assessment_id": f"assessment_{index:04d}",
                "card_id": card_by_predicate[predicate_id],
                "status": normalized_status,
                "provable": True,
            }
        )
        evidence[predicate_id] = {
            "definition": str(predicate.get("definition", predicate_id)),
            "norm_card_id": card_by_predicate[predicate_id],
            # Both the 4-state claim the assessor actually made and what it
            # collapses to for Scallop are kept, on purpose: if a rerun's
            # outcome changes, this is what lets later analysis tell whether
            # the change came from a plain new fact or from now allowing an
            # inference that wasn't allowed before.
            "raw_status": item["status"],
            "normalized_status": normalized_status,
            "assessment_rationale": item.get("assessment_rationale", ""),
            "source_quotes": list(item["source_quotes"]),
            "missing_facts": list(item["missing_facts"]),
        }

    scenario = {
        "scenario_id": f"{case_id}.{issue_id}",
        **dict(assessment_payload["role_values"]),
        "selected_card_ids": list(card_by_predicate.values()),
        "assessments": scenario_assessments,
        "distinct_entities": [
            list(pair) for pair in assessment_payload["distinct_entities"]
        ],
        "close_case": True,
    }
    rule_ir = json.loads((root / entry.rule_ir_path).read_text(encoding="utf-8"))
    compiled_path = root / entry.compiled_scl_path
    compiled = compiled_path.read_text(encoding="utf-8")
    raw = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled,
        scenario=scenario,
        query_relations=entry.query_relations,
        scli_path=scli_path,
        work_dir=work_dir,
    )
    observed = {relation: result["nonempty"] for relation, result in raw.items() if not relation.startswith("_")}
    established = [
        relation
        for relation, nonempty in observed.items()
        if nonempty
        and relation.endswith("_established")
        and not relation.endswith("_not_established")
    ]
    if observed.get(f"{unit_id}_conflict"):
        conclusion = "conflict"
    elif established:
        conclusion = "established"
    elif observed.get(f"{unit_id}_not_established"):
        conclusion = "not_established"
    elif observed.get(f"{unit_id}_undetermined"):
        conclusion = "undetermined"
    else:
        conclusion = "no_derived_outcome"
    # A boundary card rules "not this offence but that one".  The destination
    # is the operative half of that holding, so carry it forward instead of
    # letting the answer stop at 불성립.
    referred_crimes = sorted({
        tuple(row)[-1]
        for row in raw.get(f"{unit_id}_refers_to_crime", {}).get("proven_tuples", [])
        if row
    })
    waived_requirements = sorted({
        tuple(row)[-1]
        for row in raw.get(f"{unit_id}_requirement_waived", {}).get("proven_tuples", [])
        if row
    })
    # Roles that report beside the conclusion rather than inside it.  They are
    # kept apart from ``established_relations`` on purpose: a judging standard
    # and a post-offence 죄수 effect must reach the reader without either of
    # them having decided whether the offence stands.
    annotations = {
        name: sorted({tuple(row)[-1]
                      for row in raw.get(f"{unit_id}_{name}", {}).get("proven_tuples", [])
                      if row})
        for name in ("assessment_standard", "proof_standard",
                     "subtype_outcome", "post_outcome")
    }
    annotations = {name: values for name, values in annotations.items() if values}
    outcome_details = sorted({
        (str(tuple(row)[-2]), str(tuple(row)[-1]))
        for row in raw.get(f"{unit_id}_outcome_detail", {}).get("proven_tuples", [])
        if len(tuple(row)) >= 2
    })
    # A card whose polarity was never reviewed still gets evaluated; what is held
    # back is its effect on the verdict.  Recording which ones fired is how the
    # review queue learns what to look at first (검수 003 I, 우선순위 1번).
    quarantined_fired = sorted({
        str(tuple(row)[2]) if len(tuple(row)) > 2 else str(tuple(row)[-1])
        for row in raw.get(f"{unit_id}_quarantined_effect", {}).get("proven_tuples", [])
        if row
    })
    # Name the requirement that stopped the conclusion.  A unit whose commentary
    # only records marginal fact patterns for one element can never complete it,
    # and the answer would otherwise report a bare 미확정 with no explanation.
    # A derived predicate's own definition reads "'injury_conduct' 요건이 충족됨
    # (base track, alternative_any)" — an internal identifier plus a sentence
    # asserting the opposite of what an unmet requirement means.  What the
    # writer can actually use is the Korean proposition of the cards that would
    # satisfy the requirement.
    card_text = {
        str(item["norm_card_id"]): str(item["definition"])
        for item in evidence.values()
        if item.get("norm_card_id")
    }
    satisfying_cards = {
        str(item.get("id")): [
            card_text[card_id]
            for card_id in item.get("norm_card_ids", [])
            if card_id in card_text
        ]
        for item in rule_ir.get("predicates", [])
        if isinstance(item, dict)
    }
    proof_dag = raw.get("_proof_dag") or {}
    candidates = [
        (head, names)
        for head, names in (proof_dag.get("blocked_conclusions") or {}).items()
        if head.startswith(unit_id) and head.endswith("_elements_satisfied")
    ]
    # Report only the conclusion that came closest.  A unit with several tracks
    # blocks all of them at once, and listing every unmet element of 상해치사,
    # 미수 and 존속 buries the one requirement that actually mattered.
    unmet_requirements: list[dict[str, str]] = []
    if candidates:
        _, nearest = min(candidates, key=lambda item: (len(item[1]), item[0]))
        unmet_requirements = [
            {"relation": name, "satisfying_cards": satisfying_cards.get(name, [])}
            for name in nearest
        ]
    return {
        "status": "executed",
        "issue_id": issue_id,
        "unit_id": unit_id,
        "symbolic_conclusion": conclusion,
        "established_relations": established,
        "referred_crimes": referred_crimes,
        "waived_requirements": waived_requirements,
        "annotations": annotations,
        "outcome_details": [{"key": key, "value": value}
                            for key, value in outcome_details],
        "quarantined_effect_cards": quarantined_fired,
        "unmet_requirements": unmet_requirements,
        "query_results": observed,
        "proof_dag": raw.get("_proof_dag"),
        "raw_scallop_output": getattr(raw, "raw_output", ""),
        "assessment_evidence": evidence,
        "runtime": "scallop_scli_committed_rule_ir",
        "rule_ir_path": entry.rule_ir_path,
        "compiled_scl_path": entry.compiled_scl_path,
        "compiled_scl_sha256": sha256_file(compiled_path),
    }


# A unit result's own ``status``/``symbolic_conclusion`` already say everything the
# writer needs to know about how much weight a conclusion deserves; this is just
# naming that distinction so the write-stage prompt can stop giving every executed
# result — established, not_established, or undetermined alike — the same
# "반드시 그대로 따른다" force (docs/handoff/CURRENT.md, r14 사기/횡령 사례).
_PROVISIONAL_CONCLUSIONS = frozenset({"undetermined", "conflict", "no_derived_outcome"})
_DECISIVE_CONCLUSIONS = frozenset({"established", "not_established"})


def _collect_critical_predicates(
    proof_dag: Mapping[str, Any] | None, start_relations: Sequence[str]
) -> set[str]:
    """Walk the Scallop proof tree from a fired relation down to its ``assess_*`` leaves.

    Every registered predicate for a unit is assessed regardless of whether the
    facts implicate it at all — that is the completeness contract in
    prompts/rule_ir_native_predicate_assess.md — so a unit with dozens of
    predicates usually has several that are legitimately
    ``genuinely_unresolved`` and have nothing to do with why a given conclusion
    fired. Only the predicates the derivation actually used are verdict-critical.
    """

    proof_tree = (proof_dag or {}).get("proof_tree") or {}
    critical: set[str] = set()
    seen: set[str] = set()

    def visit(relation: str) -> None:
        if relation in seen:
            return
        seen.add(relation)
        entries = proof_tree.get(relation)
        if entries is None:
            if relation.startswith("assess_"):
                critical.add(relation)
            return
        for entry in entries:
            for antecedent in entry.get("antecedents", []):
                visit(str(antecedent))

    for relation in start_relations:
        visit(relation)
    return critical


def _is_cleanly_derived(result: Mapping[str, Any], relation: str) -> bool:
    """True if no predicate the derivation of ``relation`` actually used was left unresolved."""

    critical = _collect_critical_predicates(result.get("proof_dag"), [relation])
    if not critical:
        # No traceable proof structure reached this relation — this is a gap in
        # what the committed Scallop program records, not evidence of cleanliness.
        return False
    evidence = result.get("assessment_evidence") or {}
    return not any(
        evidence.get(predicate_id, {}).get("raw_status") == "genuinely_unresolved"
        for predicate_id in critical
    )


def classify_symbolic_trust(result: Mapping[str, Any]) -> str:
    """Rate how much weight a unit's outcome deserves in the generation prompt.

    - ``verified``: executed to a decisive established/not_established, and at
      least one derivation of it used no predicate that was left
      ``genuinely_unresolved``. Allowing ``inferentially_supported`` predicates
      is not by itself disqualifying — normalized, they carry the same weight
      as an explicit quote — but a conclusion that only goes through on the
      back of an unresolved element cannot be trusted just because Scallop
      happened to fire it; some RuleIR cards gate on "not proven otherwise"
      rather than requiring an affirmative fact, so an unresolved predicate can
      silently pass.
    - ``provisional``: executed, but a required element stayed unresolved
      (undetermined/conflict/no_derived_outcome), or a decisive conclusion did
      fire but not through a cleanly-derived path — a legitimate open
      question, not a broken pipeline.
    - ``unsupported``: no registered RuleIR exists for the unit at all — a
      coverage gap, not a pipeline defect.
    - ``invalid``: the run never produced a real answer for any other reason — a
      missing dependency or a symbolic-execution failure. This carries no legal
      signal at all and must not be handed to the writer as if it did.
    """

    if result.get("status") == "predicate_ir_missing":
        return "unsupported"
    if result.get("status") != "executed":
        return "invalid"
    conclusion = result.get("symbolic_conclusion")
    if conclusion not in _DECISIVE_CONCLUSIONS:
        return "provisional"
    if conclusion == "established":
        clean = any(
            _is_cleanly_derived(result, relation)
            for relation in result.get("established_relations") or []
        )
    else:
        unit_id = str(result.get("unit_id", ""))
        clean = _is_cleanly_derived(result, f"{unit_id}_not_established")
    return "verified" if clean else "provisional"


def execute_native_case(
    *,
    case_id: str,
    case_text: str,
    unit_runs: Sequence[Mapping[str, Any]],
    root: Path = PROJECT_ROOT,
    scli_path: Path = DEFAULT_SCLI,
    work_dir: Path,
) -> dict[str, Any]:
    """Execute issues in dependency order and preserve repeated units separately."""

    results: dict[str, dict[str, Any]] = {}
    for run in unit_runs:
        issue_id = str(run["issue_id"])
        unit_id = str(run["unit_id"])
        if issue_id in results:
            raise NativeHostError(f"duplicate issue run {issue_id}")
        entry = resolve_unit(unit_id, root=root)
        if isinstance(entry, PredicateIRMissing):
            results[issue_id] = {"unit_id": unit_id, **entry.to_dict()}
            continue
        dependencies = tuple(
            str(value) for value in run.get("depends_on_issue_ids", [])
        )
        if entry.shared_module:
            if not dependencies:
                # The model selected a bridge-only unit (e.g. a shared 미수/죄수
                # module) as if it stood on its own, with nothing for it to
                # bridge from. That is a defect in this one issue's selection,
                # not grounds to discard every other issue the case ran fine —
                # same per-issue degradation as a rejected issue selection.
                results[issue_id] = {
                    "status": "shared_module_missing_dependency",
                    "issue_id": issue_id,
                    "unit_id": unit_id,
                }
                continue
        else:
            # A non-shared unit is decided on its own facts.  Issue selection
            # may report a narrative link (상해죄 "depends on" 객체의 착오), but
            # that is not a symbolic bridge; honouring it as one silently
            # dropped 상해죄 from the answer whenever the linked 총칙 issue had
            # no RuleIR of its own.
            dependencies = ()
        unavailable = [
            dependency
            for dependency in dependencies
            if results.get(dependency, {}).get("symbolic_conclusion") != "established"
        ]
        if unavailable:
            results[issue_id] = {
                "status": "prerequisite_not_established",
                "issue_id": issue_id,
                "unit_id": unit_id,
                "dependencies": list(dependencies),
                "unavailable": unavailable,
            }
            continue
        try:
            results[issue_id] = execute_native_unit(
                issue_id=issue_id,
                unit_id=unit_id,
                case_id=case_id,
                case_text=case_text,
                assessment_payload=run["assessment_payload"],
                root=root,
                scli_path=scli_path,
                work_dir=work_dir / issue_id,
            )
        except (NativeHostError, ScallopFactValidationError) as exc:
            # The assessment passed its own contract but produced facts the
            # committed Scallop program cannot run on (e.g. entity ids outside
            # the actor tuple). That is a defect in this one issue's symbolic
            # execution, not grounds to discard every other issue in the case.
            results[issue_id] = {
                "status": "symbolic_execution_failed",
                "issue_id": issue_id,
                "unit_id": unit_id,
                "reason": str(exc),
            }
    directives = [
        {
            "issue_id": issue_id,
            "unit_id": result["unit_id"],
            "symbolic_conclusion": result["symbolic_conclusion"],
            "trust_status": classify_symbolic_trust(result),
            "established_relations": result["established_relations"],
            "referred_crimes": result["referred_crimes"],
            "waived_requirements": result["waived_requirements"],
            "annotations": result["annotations"],
            "outcome_details": result["outcome_details"],
            "unmet_requirements": result["unmet_requirements"],
            "evidence": result["assessment_evidence"],
            "compiled_scl_path": result["compiled_scl_path"],
            "compiled_scl_sha256": result["compiled_scl_sha256"],
        }
        for issue_id, result in results.items()
        if result.get("status") == "executed"
    ]
    # Issues the symbolic layer could not decide must still reach the writer,
    # otherwise they vanish from the final answer without any explanation.
    skipped = [
        {
            "issue_id": issue_id,
            "unit_id": result.get("unit_id", ""),
            "status": result.get("status", "unknown"),
            "trust_status": classify_symbolic_trust(result),
            "blocked_by": list(result.get("unavailable", [])),
        }
        for issue_id, result in results.items()
        if result.get("status") != "executed"
    ]
    return {
        "case_id": case_id,
        "unit_results": results,
        "generation_contract": {
            "source": "committed_rule_ir_scallop_only",
            "conclusion_directives": directives,
            "skipped_directives": skipped,
            "model_may_override_symbolic_conclusion": False,
        },
    }


_VERDICT_MANIFEST_PATTERN = re.compile(r"<!--\s*VERDICT_MANIFEST(.*?)-->", re.DOTALL)
_CHECKABLE_CONCLUSIONS = frozenset({"established", "not_established"})


def parse_verdict_manifest(answer_markdown: str) -> dict[str, str]:
    """Read the writer's own stated verdict per issue from its trailing comment.

    The legal prose above is free-form and unparseable by design; this comment
    block is the one part of the writer's output that is a contract, not an essay.
    """

    match = _VERDICT_MANIFEST_PATTERN.search(answer_markdown)
    if not match:
        return {}
    verdicts: dict[str, str] = {}
    for line in match.group(1).strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        issue_id, verdict = line.split(":", 1)
        verdicts[issue_id.strip()] = verdict.strip()
    return verdicts


def strip_verdict_manifest(answer_markdown: str) -> str:
    """Remove the machine trailer before the prose reaches a reader or a judge."""

    stripped = _VERDICT_MANIFEST_PATTERN.sub("", answer_markdown)
    return stripped.rstrip() + "\n"


def check_verdict_consistency(
    *, answer_markdown: str, directives: Sequence[Mapping[str, Any]]
) -> list[dict[str, str]]:
    """Flag every ``verified`` directive the writer's own stated verdict contradicts.

    ``generation_contract.model_may_override_symbolic_conclusion`` has said False
    since this field existed, but nothing ever checked it — a writer could silently
    disagree with a verified conclusion (or, as in the r14 사기 사례 in
    docs/handoff/CURRENT.md, assert one conclusion in its own reasoning and then
    state the opposite one) and no one would know without reading the prose by
    hand. This does not correct or regenerate anything; it only records the
    mismatch so a case with one is not mistaken for a clean run.
    """

    stated = parse_verdict_manifest(answer_markdown)
    contradictions: list[dict[str, str]] = []
    for directive in directives:
        if directive.get("trust_status") != "verified":
            continue
        expected = str(directive.get("symbolic_conclusion"))
        if expected not in _CHECKABLE_CONCLUSIONS:
            continue
        issue_id = str(directive["issue_id"])
        actual = stated.get(issue_id, "missing")
        if actual != expected:
            contradictions.append(
                {"issue_id": issue_id, "expected": expected, "stated": actual}
            )
    return contradictions


def _schema_errors(
    schema: Mapping[str, Any], payload: Mapping[str, Any]
) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: "
        f"{error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]
