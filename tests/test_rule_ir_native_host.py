from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from idpr.generation.native_rule_ir_answer import (
    NativeGenerationError,
    build_native_section_requests,
    finalize_native_answer,
    render_native_answer,
)
from idpr.rulegen.native_host import (
    DEFAULT_SCLI,
    NativeHostError,
    apply_routing_overrides,
    assess_routing_completeness,
    check_verdict_consistency,
    classify_symbolic_trust,
    closed_issue_selection_schema,
    closed_unit_catalog,
    diagnose_unsupported_issues,
    execute_native_case,
    execute_native_unit,
    normalize_assessment_status,
    parse_verdict_manifest,
    predicate_assessment_request,
    selected_predicate_requests,
    strip_verdict_manifest,
    validate_closed_issue_selection,
    validate_predicate_assessment,
)
from idpr.rulegen.registry import build_registry
from scripts.run_p2_native_scallop_golden import UnitScenarios
from scripts.run_property_scallop_golden import scenarios_for


ROOT = Path(__file__).resolve().parents[1]
CASE_TEXT = "피고인이 피해자에게 행위하였다."


def _roles(unit_id: str, scenario: dict, **overrides: str) -> dict[str, str]:
    entry = build_registry()[unit_id]
    values = {
        argument["name"]: scenario[argument["name"]]
        for argument in entry.role_predicate["arguments"]
    }
    values.update(overrides)
    values["case_id"] = "case-1"
    return values


# Golden scenarios (UnitScenarios/scenarios_for) speak the legacy 3-state Scallop
# vocabulary; the live predicate_assessment schema now speaks the 4-state
# evidentiary-basis grammar (see native_host.ASSESSMENT_STATUSES). This is the
# boundary translation, kept local to these tests rather than touching the
# shared golden-scenario data used well beyond this schema.
_LEGACY_TO_ASSESSMENT_STATUS = {
    "satisfied": "explicitly_supported",
    "not_satisfied": "contradicted",
    "unknown": "genuinely_unresolved",
}


def _assessment(unit_id: str, scenario: dict, *, issue_id: str) -> dict:
    entry = build_registry()[unit_id]
    status_by_card = {
        item["card_id"]: item["status"] for item in scenario["assessments"]
    }
    assessments = {}
    for predicate in entry.commentary_inputs:
        card_id = predicate["norm_card_ids"][0]
        legacy_status = status_by_card.get(card_id, "unknown")
        status = _LEGACY_TO_ASSESSMENT_STATUS[legacy_status]
        assessments[predicate["id"]] = {
            "status": status,
            "source_quotes": [CASE_TEXT] if legacy_status != "unknown" else [],
            "missing_facts": ["판단에 필요한 구체적 사실"] if legacy_status == "unknown" else [],
            "inference_rationale": "",
        }
    return {
        "version": "1.0.0",
        "case_id": "case-1",
        "issue_id": issue_id,
        "unit_id": unit_id,
        "role_values": _roles(unit_id, scenario),
        "distinct_entities": scenario.get("distinct_entities", []),
        "assessments": assessments,
    }


def _issue(
    issue_id: str,
    unit_id: str,
    *,
    dependencies: list[str] | None = None,
    closest_allowed_unit_ids: list[str] | None = None,
    unsupported_basis: str | None = None,
    role_candidates: dict[str, str] | None = None,
) -> dict:
    entry = build_registry().get(unit_id)
    roles = (
        {
            argument["name"]: f"{argument['name']}-1"
            for argument in entry.role_predicate["arguments"]
            if argument["name"] != "case_id"
        }
        if entry is not None
        else {}
    )
    if role_candidates is not None:
        roles = role_candidates
    if unsupported_basis is None:
        unsupported_basis = "no_matching_unit" if unit_id == "unsupported" else "not_applicable"
    return {
        "issue_id": issue_id,
        "unit_id": unit_id,
        "reported_label": "미지원 쟁점" if unit_id == "unsupported" else unit_id,
        "source_quote": CASE_TEXT,
        "candidate_fit_notes": "테스트 픽스처: 대조 결과",
        "role_candidates": roles,
        "depends_on_issue_ids": dependencies or [],
        "closest_allowed_unit_ids": closest_allowed_unit_ids or [],
        "unsupported_reason": "테스트 픽스처: 등록된 unit 없음" if unit_id == "unsupported" else "",
        "unsupported_basis": unsupported_basis,
    }


# The five routing-extension arrays are unconditionally required by the
# schema (docs/handoff/CURRENT.md "라우팅 출력 확장") so the router always has
# to think about them, but most fixtures below have nothing to declare.
_EMPTY_ROUTING_EXTENSIONS = {
    "required_subissues": [],
    "conclusion_sensitive_facts": [],
    "unresolved_branch_points": [],
    "alternative_legal_routes": [],
    "required_issue_labels": [],
}


def _selection(issues: list[dict], **extensions: Any) -> dict:
    payload: dict[str, Any] = {
        "version": "1.0.0",
        "case_id": "case-1",
        "issues": issues,
        **_EMPTY_ROUTING_EXTENSIONS,
    }
    payload.update(extensions)
    return payload


def test_request_loads_every_registered_predicate_without_fact_graph() -> None:
    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    issue = _issue("issue-1", "rape")
    request = predicate_assessment_request(
        case=case, issue=issue, unit_id="rape"
    )
    assert request["all_registered_predicates_loaded"] is True
    assert len(request["predicates"]) == len(
        build_registry()["rape"].commentary_inputs
    )
    assert request["case_text"] == CASE_TEXT
    assert "facts" not in request

    missing = predicate_assessment_request(
        case=case, issue=issue, unit_id="criminal_procedure"
    )
    assert missing["status"] == "predicate_ir_missing"


def test_closed_selection_uses_registry_enum_and_validates_dependencies() -> None:
    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    selection = _selection(
        [
            _issue("issue-1", "rape"),
            _issue("issue-2", "unsupported"),
        ]
    )
    result = selected_predicate_requests(case=case, selection=selection)
    assert result["selection_mode"] == "closed_registry_enum"
    assert result["semantic_search_used"] is False
    assert result["requests"][0]["assessment_request"][
        "all_registered_predicates_loaded"
    ] is True
    assert result["requests"][1]["status"] == "predicate_ir_missing"

    selection["issues"][0]["unit_id"] = "invented_crime"
    with pytest.raises(NativeHostError):
        validate_closed_issue_selection(
            selection,
            case_id="case-1",
            case_text=CASE_TEXT,
        )


def test_closed_selection_demotes_bad_label_dependency_and_missing_role() -> None:
    """A defective issue is handed back, not thrown — the case keeps its others.

    These three defects used to abort the whole run.  On the 26-item sweep that
    discarded 15 cases whose remaining issues were well formed, so each defect
    now names one issue for the writer to argue without symbolic support.
    """

    selection = _selection([_issue("issue-1", "rape")])
    selection["issues"][0]["reported_label"] = "unsupported"
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    assert [item["issue_id"] for item in rejected] == ["issue-1"]
    assert "죄명" in rejected[0]["reason"]

    unsupported = _issue("issue-2", "unsupported", dependencies=["issue-1"])
    selection["issues"] = [_issue("issue-1", "rape"), unsupported]
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    # The well-formed issue survives; only the dependent one is dropped.
    assert [item["issue_id"] for item in rejected] == ["issue-2"]

    supported = _issue("issue-1", "rape")
    supported["role_candidates"].pop(next(iter(supported["role_candidates"])))
    selection["issues"] = [supported]
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    assert "당사자 역할이 빠졌다" in rejected[0]["reason"]

    # A payload that is unusable as a whole still raises.
    selection["issues"] = [_issue("issue-1", "rape"), _issue("issue-1", "rape")]
    with pytest.raises(NativeHostError, match="unique"):
        validate_closed_issue_selection(
            selection, case_id="case-1", case_text=CASE_TEXT
        )


def test_unsupported_basis_leak_check_runs_both_directions() -> None:
    """``unsupported_basis`` mirrors the closest_allowed_unit_ids/unsupported_reason
    leak contract: real answer for unit_id="unsupported", "not_applicable"
    otherwise — a free-text hedge could be reworded around (docs/handoff/
    CURRENT.md "decision 단계 프롬프트 수정 시도", three failed attempts); a
    closed enum with an enforced-both-ways contract cannot be."""

    missing_basis = _issue("issue-1", "unsupported", unsupported_basis="not_applicable")
    rejected = validate_closed_issue_selection(
        _selection([missing_basis]), case_id="case-1", case_text=CASE_TEXT
    )
    assert rejected and "missing_unsupported_basis" in rejected[0]["degraded_reason"]

    leaked_basis = _issue(
        "issue-1", "rape", unsupported_basis="no_matching_unit"
    )
    rejected = validate_closed_issue_selection(
        _selection([leaked_basis]), case_id="case-1", case_text=CASE_TEXT
    )
    assert rejected and "unsupported_diagnostic_leak" in rejected[0]["degraded_reason"]


def test_participation_form_basis_requires_candidate_roles_to_resolve() -> None:
    """Claiming participation_form_or_classification_uncertainty_only with an
    empty (or wrong) role_candidates degrades the issue instead of promoting
    it — the claim only survives if it is already backed by usable role data
    for the one candidate it names."""

    empty_roles = _issue(
        "issue-1",
        "unsupported",
        closest_allowed_unit_ids=["private_document_forgery"],
        unsupported_basis="participation_form_or_classification_uncertainty_only",
    )
    rejected = validate_closed_issue_selection(
        _selection([empty_roles]), case_id="case-1", case_text=CASE_TEXT
    )
    assert rejected and "missing_required_role" in rejected[0]["degraded_reason"]

    filled_roles = _issue(
        "issue-1",
        "unsupported",
        closest_allowed_unit_ids=["private_document_forgery"],
        unsupported_basis="participation_form_or_classification_uncertainty_only",
        role_candidates={
            "defendant_id": "defendant_id-1",
            "document_id": "document_id-1",
            "nominal_author_id": "nominal_author_id-1",
        },
    )
    rejected = validate_closed_issue_selection(
        _selection([filled_roles]), case_id="case-1", case_text=CASE_TEXT
    )
    assert rejected == []


def test_apply_routing_overrides_promotes_single_participation_form_candidate() -> None:
    """The router named exactly the right unit in ``closest_allowed_unit_ids``
    and still wrote unit_id="unsupported" over participation form alone — the
    host promotes it rather than relying on a fourth prompt-wording attempt
    (docs/handoff/CURRENT.md: three tries at this in free text all failed the
    same way, job 220070/220071/220074)."""

    issue = _issue(
        "issue-1",
        "unsupported",
        closest_allowed_unit_ids=["private_document_forgery"],
        unsupported_basis="participation_form_or_classification_uncertainty_only",
        role_candidates={
            "defendant_id": "defendant_id-1",
            "document_id": "document_id-1",
            "nominal_author_id": "nominal_author_id-1",
        },
    )
    issue["unsupported_reason"] = "직접정범인지 간접정범인지 불확실함"
    promoted, overrides = apply_routing_overrides(_selection([issue]))
    assert overrides == [
        {
            "issue_id": "issue-1",
            "reported_label": "미지원 쟁점",
            "promoted_unit_id": "private_document_forgery",
            "unsupported_reason": "직접정범인지 간접정범인지 불확실함",
        }
    ]
    promoted_issue = promoted["issues"][0]
    assert promoted_issue["unit_id"] == "private_document_forgery"
    assert promoted_issue["closest_allowed_unit_ids"] == []
    assert promoted_issue["unsupported_reason"] == ""
    assert promoted_issue["unsupported_basis"] == "not_applicable"
    # The promoted issue must itself still clear the ordinary contract (its
    # role_candidates already had to, to survive validation upstream — this
    # confirms selected_predicate_requests's second validation pass will not
    # re-reject what was just promoted).
    assert (
        validate_closed_issue_selection(promoted, case_id="case-1", case_text=CASE_TEXT)
        == []
    )


def test_apply_routing_overrides_leaves_genuine_gaps_and_ambiguous_candidates_alone() -> None:
    """A genuine coverage gap (``no_matching_unit``) and an unresolved
    multi-candidate decline (2-3 names) are not promotable — the model itself
    never narrowed either to one applicable unit, so there is nothing safe to
    promote to (docs/handoff/CURRENT.md: 강도상해/강도치상 결합범 and 살인교사
    both correctly stayed unsupported in job 220070 after naming candidates
    that do not actually cover the fact pattern)."""

    genuine_gap = _issue(
        "issue-1", "unsupported", unsupported_basis="no_matching_unit"
    )
    ambiguous = _issue(
        "issue-2",
        "unsupported",
        closest_allowed_unit_ids=["rape", "indecent_assault"],
        unsupported_basis="participation_form_or_classification_uncertainty_only",
    )
    promoted, overrides = apply_routing_overrides(_selection([genuine_gap, ambiguous]))
    assert overrides == []
    assert promoted["issues"][0]["unit_id"] == "unsupported"
    assert promoted["issues"][1]["unit_id"] == "unsupported"


def test_selected_predicate_requests_tolerates_every_issue_rejected() -> None:
    """A case where per-issue rejection empties ``issues`` is a degraded case,
    not a malformed payload.

    219740 crashed two cases this way: the raw selection had issues, but every
    one of them failed the role/quote contract, and ``selected_predicate_requests``
    re-ran the same schema — with its ``minItems: 1`` for raw model output —
    against the now-empty, already-filtered selection.
    """

    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    filtered = _selection([])
    result = selected_predicate_requests(case=case, selection=filtered)
    assert result["requests"] == []

    # The model's raw output must still name at least one issue — this path
    # is unchanged.
    with pytest.raises(NativeHostError, match="non-empty"):
        validate_closed_issue_selection(
            filtered, case_id="case-1", case_text=CASE_TEXT
        )


def test_direct_assessment_requires_exact_source_quotes() -> None:
    scenario = UnitScenarios("rape").build()[0]
    payload = _assessment("rape", scenario, issue_id="issue-1")
    predicate_id = next(iter(payload["assessments"]))
    payload["assessments"][predicate_id] = {
        "status": "explicitly_supported",
        "source_quotes": ["원문에 없는 문장"],
        "missing_facts": [],
    }
    with pytest.raises(NativeHostError, match="not in case text"):
        validate_predicate_assessment(
            payload,
            case_id="case-1",
            issue_id="issue-1",
            unit_id="rape",
            case_text=CASE_TEXT,
        )


def test_inferentially_supported_requires_inference_rationale() -> None:
    """Without a mandatory rationale, an inference can't be audited afterward."""

    scenario = UnitScenarios("rape").build()[0]
    payload = _assessment("rape", scenario, issue_id="issue-1")
    predicate_id = next(iter(payload["assessments"]))
    payload["assessments"][predicate_id] = {
        "status": "inferentially_supported",
        "source_quotes": [CASE_TEXT],
        "missing_facts": [],
    }
    with pytest.raises(NativeHostError, match="inference_rationale"):
        validate_predicate_assessment(
            payload,
            case_id="case-1",
            issue_id="issue-1",
            unit_id="rape",
            case_text=CASE_TEXT,
        )

    payload["assessments"][predicate_id]["inference_rationale"] = (
        "행위·정황상 다른 해석의 여지가 없어 추론함"
    )
    validate_predicate_assessment(
        payload,
        case_id="case-1",
        issue_id="issue-1",
        unit_id="rape",
        case_text=CASE_TEXT,
    )


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_host_executes_committed_nonproperty_rule_ir(tmp_path: Path) -> None:
    scenario = UnitScenarios("rape").build()[0]
    result = execute_native_unit(
        issue_id="issue-1",
        unit_id="rape",
        case_id="case-1",
        case_text=CASE_TEXT,
        assessment_payload=_assessment("rape", scenario, issue_id="issue-1"),
        work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli_committed_rule_ir"
    assert result["compiled_scl_path"] == "rules/generated/p2_rape_v1_candidate.scl"
    assert len(result["compiled_scl_sha256"]) == 64
    assert result["symbolic_conclusion"] == "established"
    assert "rape_base_established" in result["established_relations"]


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_execute_native_case_degrades_single_symbolic_execution_failure(
    tmp_path: Path,
) -> None:
    """A Scallop-fact-level defect in one issue must not discard its siblings.

    ``distinct_entities`` naming an id outside the actor tuple passes
    ``validate_predicate_assessment``'s own quote/missing-facts contract but
    fails later, at scenario rendering — a case in the 219740 sweep hit
    exactly this and lost every issue, not just the broken one.
    """

    scenario = UnitScenarios("rape").build()[0]
    good = _assessment("rape", scenario, issue_id="issue-1")
    bad = _assessment("rape", scenario, issue_id="issue-2")
    bad["distinct_entities"] = [[bad["role_values"]["defendant_id"], "no-such-entity"]]

    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-1",
                "unit_id": "rape",
                "depends_on_issue_ids": [],
                "assessment_payload": good,
            },
            {
                "issue_id": "issue-2",
                "unit_id": "rape",
                "depends_on_issue_ids": [],
                "assessment_payload": bad,
            },
        ],
        work_dir=tmp_path,
    )

    contract = report["generation_contract"]
    assert {d["issue_id"] for d in contract["conclusion_directives"]} == {"issue-1"}
    assert report["unit_results"]["issue-2"]["status"] == "symbolic_execution_failed"
    assert any(
        item["issue_id"] == "issue-2" for item in contract["skipped_directives"]
    )


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_property_outcome_bridges_into_shared_module(tmp_path: Path) -> None:
    theft_rule_ir = json.loads(
        (ROOT / "data/rulegen/property/rule_ir/theft_rule_ir_candidate.json").read_text()
    )
    theft = scenarios_for(theft_rule_ir, "theft")[0]
    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    relative_payload = _assessment(
        "relative_property_crime_exception", relative, issue_id="issue-relative"
    )
    relative_payload["role_values"]["predicate_offense_id"] = "theft"
    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-theft",
                "unit_id": "theft",
                "assessment_payload": _assessment(
                    "theft", theft, issue_id="issue-theft"
                ),
            },
            {
                "issue_id": "issue-relative",
                "unit_id": "relative_property_crime_exception",
                "depends_on_issue_ids": ["issue-theft"],
                "assessment_payload": relative_payload,
            },
        ],
        work_dir=tmp_path,
    )
    assert report["unit_results"]["issue-theft"]["symbolic_conclusion"] == "established"
    assert report["unit_results"]["issue-relative"]["symbolic_conclusion"] == "established"
    contract = report["generation_contract"]
    assert contract["source"] == "committed_rule_ir_scallop_only"
    assert contract["model_may_override_symbolic_conclusion"] is False


def test_shared_module_without_dependency_degrades_instead_of_crashing(
    tmp_path: Path,
) -> None:
    """A shared module selected with no dependency has nothing to bridge from,
    but that must demote only this one issue, not the whole case.

    219774's remaining failure (after the other three per-issue defects were
    fixed) was exactly this: the model selected a bridge-only unit as if it
    stood on its own, and the host used to raise out of the case loop for it.
    """

    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-relative",
                "unit_id": "relative_property_crime_exception",
                "assessment_payload": _assessment(
                    "relative_property_crime_exception",
                    relative,
                    issue_id="issue-relative",
                ),
            }
        ],
        work_dir=tmp_path,
    )
    assert (
        report["unit_results"]["issue-relative"]["status"]
        == "shared_module_missing_dependency"
    )
    assert any(
        item["issue_id"] == "issue-relative"
        for item in report["generation_contract"]["skipped_directives"]
    )


def test_section_writer_cannot_supply_host_conclusion() -> None:
    selection = {
        "issues": [
            {
                "issue_id": "issue-1",
                "unit_id": "rape",
                "reported_label": "강간죄",
            }
        ]
    }
    report = {
        "case_id": "case-1",
        "generation_contract": {
            "source": "committed_rule_ir_scallop_only",
            "conclusion_directives": [
                {
                    "issue_id": "issue-1",
                    "unit_id": "rape",
                    "symbolic_conclusion": "established",
                    "established_relations": ["rape_base_established"],
                    "evidence": {},
                    "compiled_scl_path": "rules/generated/p2_rape_v1_candidate.scl",
                    "compiled_scl_sha256": "0" * 64,
                }
            ],
        },
    }
    requests = build_native_section_requests(
        case={"question_text": CASE_TEXT, "question_prompt": "죄책"},
        selection=selection,
        native_report=report,
    )
    prose = "### 법리\n\n법리 설명\n\n### 사안의 적용\n\n사실 적용"
    answer = finalize_native_answer(
        section_requests=requests, prose_by_issue={"issue-1": prose}
    )
    assert answer["sections"][0]["conclusion"] == "성립"
    assert render_native_answer(answer).endswith("### 결론\n\n성립\n")

    with pytest.raises(NativeGenerationError, match="host-owned"):
        finalize_native_answer(
            section_requests=requests,
            prose_by_issue={"issue-1": prose + "\n\n### 결론\n\n불성립"},
        )


def test_normalize_assessment_status_collapses_evidentiary_basis_to_scallop_facts() -> None:
    """Both satisfied-like states must reach Scallop identically.

    The split exists to stop the assessor defaulting inferable elements (intent,
    causation) to unknown, not to teach the symbolic layer a fourth state.
    """

    assert normalize_assessment_status("explicitly_supported") == "satisfied"
    assert normalize_assessment_status("inferentially_supported") == "satisfied"
    assert normalize_assessment_status("contradicted") == "not_satisfied"
    assert normalize_assessment_status("genuinely_unresolved") == "unknown"
    with pytest.raises(NativeHostError):
        normalize_assessment_status("satisfied")


_CLEAN_PROOF_DAG = {
    "proof_tree": {
        "unit_established": [
            {"rule_id": "unit.outcome.established", "antecedents": ["unit_elements_satisfied"]}
        ],
        "unit_elements_satisfied": [
            {"rule_id": "unit.elements", "antecedents": ["satisfied_card_a", "provable"]}
        ],
        "satisfied_card_a": [
            {"rule_id": "card_a.satisfied", "antecedents": ["assess_card_a", "provable"]}
        ],
    }
}


def test_classify_symbolic_trust_separates_decisive_from_broken() -> None:
    """established/not_established only earn absolute force via a clean derivation."""

    clean_established = {
        "status": "executed",
        "symbolic_conclusion": "established",
        "established_relations": ["unit_established"],
        "proof_dag": _CLEAN_PROOF_DAG,
        "assessment_evidence": {"assess_card_a": {"raw_status": "explicitly_supported"}},
    }
    assert classify_symbolic_trust(clean_established) == "verified"

    # inferentially_supported normalizes the same as explicitly_supported — it
    # is not, on its own, a reason to distrust an otherwise clean derivation.
    inferred = {**clean_established, "assessment_evidence": {
        "assess_card_a": {"raw_status": "inferentially_supported"}
    }}
    assert classify_symbolic_trust(inferred) == "verified"

    # The predicate the derivation actually used stayed unresolved — Scallop
    # still fired (e.g. a card gated on "not proven otherwise"), but nothing
    # here should be trusted as a decisive answer.
    unresolved_critical = {**clean_established, "assessment_evidence": {
        "assess_card_a": {"raw_status": "genuinely_unresolved"}
    }}
    assert classify_symbolic_trust(unresolved_critical) == "provisional"

    # A conclusion with no traceable proof structure at all cannot be
    # confirmed clean either.
    untraceable = {**clean_established, "proof_dag": {"proof_tree": {}}}
    assert classify_symbolic_trust(untraceable) == "provisional"

    not_established = {
        "status": "executed",
        "symbolic_conclusion": "not_established",
        "unit_id": "unit",
        "proof_dag": {
            "proof_tree": {
                "unit_not_established": [
                    {"rule_id": "unit.outcome.not_established", "antecedents": ["assess_card_b"]}
                ]
            }
        },
        "assessment_evidence": {"assess_card_b": {"raw_status": "contradicted"}},
    }
    assert classify_symbolic_trust(not_established) == "verified"

    assert classify_symbolic_trust({"status": "executed", "symbolic_conclusion": "undetermined"}) == "provisional"
    assert classify_symbolic_trust({"status": "executed", "symbolic_conclusion": "conflict"}) == "provisional"
    assert classify_symbolic_trust({"status": "executed", "symbolic_conclusion": "no_derived_outcome"}) == "provisional"
    assert classify_symbolic_trust({"status": "shared_module_missing_dependency"}) == "invalid"
    assert classify_symbolic_trust({"status": "prerequisite_not_established"}) == "invalid"
    assert classify_symbolic_trust({"status": "symbolic_execution_failed"}) == "invalid"
    assert classify_symbolic_trust({"status": "predicate_ir_missing"}) == "unsupported"


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_execute_native_case_tags_directives_and_skips_with_trust_status(
    tmp_path: Path,
) -> None:
    scenario = UnitScenarios("rape").build()[0]
    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-1",
                "unit_id": "rape",
                "assessment_payload": _assessment("rape", scenario, issue_id="issue-1"),
            },
            {
                "issue_id": "issue-relative",
                "unit_id": "relative_property_crime_exception",
                "assessment_payload": _assessment(
                    "relative_property_crime_exception",
                    UnitScenarios("relative_property_crime_exception").build()[0],
                    issue_id="issue-relative",
                ),
            },
        ],
        work_dir=tmp_path,
    )
    contract = report["generation_contract"]
    [rape_directive] = [
        d for d in contract["conclusion_directives"] if d["issue_id"] == "issue-1"
    ]
    assert rape_directive["trust_status"] == "verified"
    [relative_skip] = contract["skipped_directives"]
    assert relative_skip["issue_id"] == "issue-relative"
    assert relative_skip["trust_status"] == "invalid"


def test_verdict_manifest_parse_strip_and_consistency_check() -> None:
    answer = (
        "### 1. 甲의 죄책\n\n본문 서술...\n\n"
        "<!--VERDICT_MANIFEST\n"
        "issue-1: established\n"
        "issue-2: not_established\n"
        "-->\n"
    )
    assert parse_verdict_manifest(answer) == {
        "issue-1": "established",
        "issue-2": "not_established",
    }
    stripped = strip_verdict_manifest(answer)
    assert "VERDICT_MANIFEST" not in stripped
    assert stripped.startswith("### 1. 甲의 죄책")

    directives = [
        {"issue_id": "issue-1", "trust_status": "verified", "symbolic_conclusion": "established"},
        {"issue_id": "issue-2", "trust_status": "verified", "symbolic_conclusion": "established"},
        # A provisional directive is never checked for contradiction — the
        # writer is explicitly allowed to argue past it.
        {"issue_id": "issue-3", "trust_status": "provisional", "symbolic_conclusion": "undetermined"},
    ]
    contradictions = check_verdict_consistency(answer_markdown=answer, directives=directives)
    assert contradictions == [
        {"issue_id": "issue-2", "expected": "established", "stated": "not_established"}
    ]

    no_manifest = "### 1. 甲의 죄책\n\n본문만 있고 트레일러가 없다.\n"
    missing = check_verdict_consistency(
        answer_markdown=no_manifest,
        directives=[
            {"issue_id": "issue-1", "trust_status": "verified", "symbolic_conclusion": "established"},
        ],
    )
    assert missing == [{"issue_id": "issue-1", "expected": "established", "stated": "missing"}]


def test_issue_selection_schema_requires_five_routing_extension_fields() -> None:
    """The router always has to think about the five extension arrays.

    They can legitimately be empty, but a payload that omits one of them
    outright must fail validation the same way an omitted ``issues`` key
    would — this is what forces the guided-decoding grammar to always emit
    them (docs/handoff/CURRENT.md "라우팅 출력 확장").
    """

    schema = closed_issue_selection_schema(case_id="case-1")
    assert set(schema["required"]) >= {
        "required_subissues",
        "conclusion_sensitive_facts",
        "unresolved_branch_points",
        "alternative_legal_routes",
        "required_issue_labels",
    }

    incomplete = _selection([_issue("issue-1", "rape")])
    del incomplete["required_subissues"]
    with pytest.raises(NativeHostError):
        validate_closed_issue_selection(
            incomplete, case_id="case-1", case_text=CASE_TEXT
        )


def test_assess_routing_completeness_flags_missing_required_subissue() -> None:
    """A subissue named but never routed as its own issue is a live gap.

    This is the router promising a doctrine (e.g. 263조 동시범 특례 once
    causation goes unresolved) and then dropping it — diagnosis #1/#2 in
    docs/handoff/CURRENT.md. The relationship is expressed by issue_id, not
    unit_id, because the same unit_id can recur across several issues.
    """

    selection = _selection(
        [_issue("issue-1", "rape")],
        required_subissues=[
            {
                "parent_issue_id": "issue-1",
                "subissue_issue_id": "issue-2",
                "trigger_source_quote": CASE_TEXT,
                "reason": "협박을 수반한 재산 취득 여부를 별도로 검토해야 한다",
            }
        ],
    )
    report = assess_routing_completeness(selection)
    assert report["gaps"] == [
        {
            "gap_type": "required_subissue_missing",
            "parent_issue_id": "issue-1",
            "subissue_issue_id": "issue-2",
            "reason": "협박을 수반한 재산 취득 여부를 별도로 검토해야 한다",
        }
    ]


def test_assess_routing_completeness_accepts_fulfilled_subissue_and_labels() -> None:
    """No gap when the named subissue was actually routed, and
    ``required_issue_labels`` surfaces as an exact-label override."""

    selection = _selection(
        [_issue("issue-1", "rape"), _issue("issue-2", "extortion")],
        required_subissues=[
            {
                "parent_issue_id": "issue-1",
                "subissue_issue_id": "issue-2",
                "trigger_source_quote": CASE_TEXT,
                "reason": "협박을 수반한 재산 취득 여부를 별도로 검토해야 한다",
            }
        ],
        required_issue_labels=[
            {"issue_id": "issue-2", "exact_label": "공갈죄(재산상 이익 취득)"}
        ],
    )
    report = assess_routing_completeness(selection)
    assert report["gaps"] == []
    assert report["exact_labels"] == {"issue-2": "공갈죄(재산상 이익 취득)"}


def test_assess_routing_completeness_flags_dangling_issue_reference() -> None:
    """A reference to an issue_id that was never selected (or was dropped by
    per-issue rejection) is a payload defect, not silently ignored."""

    selection = _selection(
        [_issue("issue-1", "rape")],
        alternative_legal_routes=[
            {
                "primary_issue_id": "issue-does-not-exist",
                "alternative_issue_id": "issue-2",
                "condition": "협박의 정도가 낮게 인정되는 경우",
                "reason": "폭행·협박의 정도에 따라 강간이 아니라 공갈로 평가될 수 있다",
            }
        ],
    )
    report = assess_routing_completeness(selection)
    assert report["gaps"] == [
        {
            "gap_type": "dangling_issue_reference",
            "field": "primary_issue_id",
            "value": "issue-does-not-exist",
            "record": selection["alternative_legal_routes"][0],
        }
    ]


def test_assess_routing_completeness_flags_missing_branch_issue_reference() -> None:
    """An unresolved-fact branch names factual *readings* of an already-routed
    issue (``branch_conditions``, prose) — not separate units — but its
    ``affects_issue_ids`` still has to reference a real issue."""

    selection = _selection(
        [_issue("issue-1", "fraud")],
        unresolved_branch_points=[
            {
                "branch_trigger_quote": CASE_TEXT,
                "affects_issue_ids": ["issue-1", "issue-does-not-exist"],
                "branch_conditions": [
                    "통상적인 치료상 과실로 평가되는 경우",
                    "독립적인 중대한 의료과오로 평가되는 경우",
                ],
                "reason": "평가에 따라 사망 결과의 객관적 귀속 여부가 달라진다",
            }
        ],
    )
    report = assess_routing_completeness(selection)
    assert report["gaps"] == [
        {
            "gap_type": "dangling_issue_reference",
            "field": "affects_issue_ids",
            "value": "issue-does-not-exist",
            "record": selection["unresolved_branch_points"][0],
        }
    ]


def test_diagnose_unsupported_issues_flags_named_candidate_as_routing_miss() -> None:
    """A ``closest_allowed_unit_ids`` next to unit_id="unsupported" means the
    router itself saw a real candidate and still declined it — a routing
    defect, not a coverage gap (job 220007 r14_p1_q2: ``bribe_giving`` was
    fully carded for 증뢰물전달 and still passed over)."""

    selection = _selection(
        [
            {
                "issue_id": "issue-1",
                "unit_id": "unsupported",
                "reported_label": "뇌물공여의 간접정범 또는 전달",
                "source_quote": CASE_TEXT,
                "role_candidates": {},
                "depends_on_issue_ids": [],
                "closest_allowed_unit_ids": ["bribe_giving"],
                "unsupported_reason": "명칭이 정확히 일치하지 않아 확신할 수 없었다",
            },
            _issue("issue-2", "rape"),
        ]
    )
    findings = diagnose_unsupported_issues(selection)
    assert findings == [
        {
            "issue_id": "issue-1",
            "reported_label": "뇌물공여의 간접정범 또는 전달",
            "closest_allowed_unit_ids": ["bribe_giving"],
            "unsupported_reason": "명칭이 정확히 일치하지 않아 확신할 수 없었다",
            "likely_routing_miss": True,
        }
    ]


def test_diagnose_unsupported_issues_treats_empty_candidates_as_true_gap() -> None:
    """No candidate named at all is either a genuine coverage gap or a
    catalog/prompt comprehension failure — not flagged as a routing miss."""

    selection = _selection(
        [
            {
                "issue_id": "issue-1",
                "unit_id": "unsupported",
                "reported_label": "중지미수",
                "source_quote": CASE_TEXT,
                "role_candidates": {},
                "depends_on_issue_ids": [],
                "closest_allowed_unit_ids": [],
                "unsupported_reason": "형법 총칙 미수 감면 법리를 표현하는 unit이 없다",
            }
        ]
    )
    findings = diagnose_unsupported_issues(selection)
    assert findings[0]["likely_routing_miss"] is False


def test_catalog_exposes_verified_legal_labels_for_confirmed_routing_misses() -> None:
    """``legal_labels`` is populated only for units a real routing miss
    confirmed need it — not backfilled speculatively across the registry."""

    catalog = {entry["unit_id"]: entry for entry in closed_unit_catalog()}
    assert "증뢰물전달죄" in catalog["bribe_giving"]["legal_labels"]
    assert catalog["rape"]["legal_labels"] == []
