"""Project the finished symbolic run into the input representation Call 3 reads.

The plan computes no new legal judgment.  Every conclusion in it already exists in
``LiabilityEvaluation``, ``FinalResponsibilityView`` or the Call 2 assessments; this module
rearranges them deterministically and attaches the authored norm each finding is about.
Two fields are not direct projections -- ``contested_points`` looks up authored doctrine
branches, and ``rule_statements`` is filled by the card retrieval of ANSWERPLAN_SPEC 5.5 --
and both carry an explicit origin so the distinction survives into the audit.

Three locks keep the evaluation material out of what we produce, because without them the
rule-base contribution we report would be a reflection of the grading key rather than a
measurement of it:

* the dataset ``supporting_precedents`` column is never read;
* no field derives from per-question rubric item counts or scores;
* contested points come only from authored doctrine or reviewed cards.

The rubric statistics that motivated the schema stay in the design document.  They do not
enter the artifact.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from idpr.v2.registry import DefinitionRegistry

#: Internal vocabulary that must never survive serialization into the Call 3 payload.
#: A leak here does not merely look untidy -- it teaches the writer to quote machine state
#: back into a legal answer.
_INTERNAL_MARKERS = (
    "binding:",
    "factual_episode:",
    "offense.",
    "derived_offense.",
    "legal_element.",
    "ground_fact.",
    "relation.",
    "doctrine.",
    "condition.",
    "concurrence-pair:",
    "UNKNOWN",
    "stage=",
    "source_run=",
    "Scallop",
    "Call 2",
)

_ALLOWED_CONTESTED_ORIGINS = ("authored_doctrine", "reviewed_card")

#: Final states, in the vocabulary the answer writer sees rendered as prose.
ESTABLISHED = "ESTABLISHED"
NOT_ESTABLISHED = "NOT_ESTABLISHED"
UNRESOLVED = "UNRESOLVED"
NOT_ATTRIBUTABLE = "NOT_ATTRIBUTABLE"
ABSORBED = "ABSORBED"


class AnswerPlanError(RuntimeError):
    """A plan that would mislead the writer is not built."""


@dataclass(frozen=True, slots=True)
class RuleStatement:
    """One norm sentence the answer may state, copied verbatim from its source."""

    statement: str
    origin: str
    source_id: str

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise AnswerPlanError("rule statement is empty")
        if not self.source_id:
            raise AnswerPlanError(f"rule statement without source id: {self.statement[:40]}")


@dataclass(frozen=True, slots=True)
class Finding:
    """A decisive element of one instance, with the norm it was measured against."""

    label: str
    truth: str
    legal_standard: str | None = None
    governing_provision: str | None = None
    rule_statements: tuple[RuleStatement, ...] = ()
    supporting_quotes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ParticipationRoute:
    mode: str
    principal_actor: str | None
    principal_offense: str | None
    principal_realization: str | None
    relation: str | None = None


@dataclass(frozen=True, slots=True)
class ContestedPoint:
    """A doctrinal split the answer should present before adopting one side.

    ``origin`` is mandatory and closed.  A contested point invented from the grading
    rubric would hand back the very thing the rubric is testing.
    """

    label: str
    positions: tuple[str, ...]
    adopted: str
    why_adopted: str
    origin: str
    source_id: str

    def __post_init__(self) -> None:
        if self.origin not in _ALLOWED_CONTESTED_ORIGINS:
            raise AnswerPlanError(
                f"contested point origin {self.origin!r} is not one of {_ALLOWED_CONTESTED_ORIGINS}"
            )
        if not self.source_id:
            raise AnswerPlanError(f"contested point without source id: {self.label!r}")


@dataclass(frozen=True, slots=True)
class AnchoredIssue:
    issue_id: str
    actor: str
    offense_label: str
    governing_provision: str | None
    episode_quotes: tuple[str, ...]
    final_state: str
    completion_state: str | None
    completion_why: str | None
    participation: ParticipationRoute | None
    decisive_stage: str | None
    satisfied: tuple[Finding, ...]
    failed: tuple[Finding, ...]
    blocking: tuple[Finding, ...]
    doctrines: tuple[Mapping[str, Any], ...]
    contested_points: tuple[ContestedPoint, ...]
    #: True when a stage gate actually failed in the run.  This is the symbolic fact the
    #: no-acquittal-from-UNKNOWN contract is about; the predicate lists cannot stand in for
    #: it, because a gate can fail on a relation obligation that is not a predicate at all.
    gate_failed: bool = False
    absorbed_into: str | None = None
    absorption_relation: str | None = None
    absorption_reason: str | None = None
    not_attributable_reason: str | None = None


@dataclass(frozen=True, slots=True)
class FinalResponsibility:
    retained: tuple[Mapping[str, str], ...]
    absorbed: tuple[Mapping[str, Any], ...]
    imaginative_pairs: tuple[Mapping[str, Any], ...]
    excess_attributions: tuple[Mapping[str, Any], ...]
    status_redirections: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class RequiredFinalConclusion:
    """One anchor the closing paragraph must restate, in the model's own words.

    This is not a sentence to hand the writer -- it is the smallest closed set of facts a
    closing paragraph cannot omit or invert: which actor, which offence, and the one
    conclusion word already fixed for it elsewhere in the plan.  Wording, ordering, and
    connective prose stay the model's to compose; only the presence and polarity of each
    of these anchors is required, one per anchored issue.
    """

    actor: str
    offense_label: str
    state: str
    completion_state: str | None = None
    participation_mode: str | None = None


@dataclass(frozen=True, slots=True)
class AnswerPlan:
    case_id: str
    case_text: str
    question: str
    discussion_order: tuple[str, ...]
    anchored_issues: tuple[AnchoredIssue, ...]
    final_responsibility: FinalResponsibility
    required_final_conclusions: tuple[RequiredFinalConclusion, ...] = ()
    representation_gaps: tuple[str, ...] = ()
    unmapped_instances: tuple[str, ...] = ()


# --------------------------------------------------------------------------------------
# identity and labels
# --------------------------------------------------------------------------------------


def instance_ref(instance: Mapping[str, Any]) -> str:
    """Stable internal key for one liability instance.  Never serialized to the model."""
    return "|".join(
        (
            str(instance.get("case_id", "")),
            str(instance.get("actor_id", "")),
            str(instance.get("offense_ref", "")),
            str(instance.get("occurrence_id", "")),
        )
    )


def offense_label(
    registry: DefinitionRegistry,
    offense_ref: str,
    labels: Mapping[str, str] | None = None,
) -> str:
    """The Korean offence name, from authored sources only.

    Two sources carry it: the offence's own ``identity.name``, and the reviewed seed-cue
    catalogue that Call 1.5 already routes with.  Derived offences have no ``identity`` at
    all, so the catalogue is the only name they have.  When neither has one we refuse
    rather than fall back to the ref -- an answer that names a crime ``special_theft``
    would be worse than one that fails to build.
    """
    entry = registry.by_id.get(offense_ref)
    if entry is not None:
        name = (entry.payload.get("identity") or {}).get("name")
        if name:
            return str(name)
    if labels and offense_ref in labels:
        return str(labels[offense_ref])
    raise AnswerPlanError(
        f"no authored Korean name for {offense_ref}; "
        "author it in data/v2/binding_seed_cues.yaml before building the plan"
    )


def governing_provision(registry: DefinitionRegistry, offense_ref: str) -> str | None:
    entry = registry.by_id.get(offense_ref)
    if entry is None:
        return None
    identity = entry.payload.get("identity") or {}
    refs = identity.get("statutory_refs") or []
    return "; ".join(str(ref) for ref in refs) if refs else None


#: Latin script inside a ``canonical_meaning`` marks an authoring note rather than a legal
#: term -- "death-agnostic 패턴", "(+NOT())", "아래 B-7".  Five predicates carry one.
_AUTHORING_NOTE = re.compile(r"[A-Za-z]")


def predicate_label(registry: DefinitionRegistry, predicate_ref: str) -> str:
    """What a lawyer calls this element.

    ``canonical_meaning`` is the authored short name and is usually exactly right.  Where
    it still carries a worksheet annotation, the authored ``legal_standard`` is used
    instead: it is a full sentence rather than a label, but it is written in law rather
    than in modelling vocabulary.
    """
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return predicate_ref.rsplit(".", 1)[-1].replace("_", " ")
    meaning = entry.payload.get("canonical_meaning")
    if meaning and not _AUTHORING_NOTE.search(str(meaning)):
        return str(meaning)
    standard = entry.payload.get("legal_standard")
    if standard:
        return str(standard)
    if meaning:
        return _AUTHORING_NOTE.sub("", str(meaning)).strip()
    return predicate_ref.rsplit(".", 1)[-1].replace("_", " ")


def predicate_standard(registry: DefinitionRegistry, predicate_ref: str) -> str | None:
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return None
    standard = entry.payload.get("legal_standard")
    return str(standard) if standard else None


def predicate_provision(registry: DefinitionRegistry, predicate_ref: str) -> str | None:
    """The statutory citation authored on the predicate, if any."""
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return None
    for ref in entry.payload.get("authority_refs") or []:
        if not isinstance(ref, Mapping):
            continue
        if ref.get("authority_basis") == "statute_text" and ref.get("citation"):
            return str(ref["citation"])
    return None


def authored_precedent_statements(
    registry: DefinitionRegistry, predicate_ref: str
) -> tuple[RuleStatement, ...]:
    """Precedent-based authority already authored on the predicate itself.

    Only twelve predicates carry one, which is exactly why the card channel exists.  The
    two sources stay distinguishable by ``origin`` rather than being merged.
    """
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return ()
    statements: list[RuleStatement] = []
    for ref in entry.payload.get("authority_refs") or []:
        if not isinstance(ref, Mapping):
            continue
        basis = str(ref.get("authority_basis", ""))
        if "precedent" not in basis:
            continue
        citation = str(ref.get("citation", "")).strip()
        if not citation:
            continue
        statements.append(
            RuleStatement(statement=citation, origin="authored_doctrine", source_id=predicate_ref)
        )
    return tuple(statements)


# --------------------------------------------------------------------------------------
# projection
# --------------------------------------------------------------------------------------


def _findings_for_instance(
    registry: DefinitionRegistry,
    truths: Sequence[Mapping[str, Any]],
    ref: str,
    quotes_by_predicate: Mapping[str, tuple[str, ...]],
) -> tuple[tuple[Finding, ...], tuple[Finding, ...], tuple[Finding, ...]]:
    """Findings for one already-selected instance, from the authoritative truth store.

    `truths` is `case_truths`: what the symbolic layer actually consumed to reach the
    conclusion this issue states.  The raw `assessments` of a single Call 2 run is a subset
    of it -- merged participation and doctrine truths land only in `case_truths` -- and
    projecting from the subset silently drops the grounds for conclusions the plan is
    simultaneously asserting.

    This does not widen the issue universe.  Every finding still has to match a `ref` that
    came from the run's liability results, so a truth about an instance no legal conclusion
    was reached for contributes nothing here, exactly as before.
    """
    satisfied: list[Finding] = []
    failed: list[Finding] = []
    blocking: list[Finding] = []
    for row in truths:
        instance = row.get("instance_key") or {}
        if instance_ref(instance) != ref:
            continue
        predicate_ref = str(row.get("predicate_ref", ""))
        if not predicate_ref:
            continue
        finding = Finding(
            label=predicate_label(registry, predicate_ref),
            truth=str(row.get("truth", "")),
            legal_standard=predicate_standard(registry, predicate_ref),
            governing_provision=predicate_provision(registry, predicate_ref),
            rule_statements=authored_precedent_statements(registry, predicate_ref),
            supporting_quotes=quotes_by_predicate.get(predicate_ref, ()),
        )
        if finding.truth == "TRUE":
            satisfied.append(finding)
        elif finding.truth == "FALSE":
            failed.append(finding)
        else:
            blocking.append(finding)
    return tuple(satisfied), tuple(failed), tuple(blocking)


def _gate_failed(result: Mapping[str, Any]) -> bool:
    return any(
        (result.get(stage) or {}).get("gate_state") == "fails"
        for stage in ("elements", "unlawfulness", "culpability", "punishability")
    )


def _final_state(
    result: Mapping[str, Any],
    ref: str,
    retained: frozenset[str],
    absorbed: frozenset[str],
    withheld: frozenset[str],
    has_blocking: bool,
) -> str:
    if ref in absorbed:
        return ABSORBED
    if ref in withheld:
        return NOT_ATTRIBUTABLE
    if ref in retained:
        return ESTABLISHED
    # An instance whose decisive stage never resolved is not an acquittal.  UNKNOWN is not
    # FALSE, and the writer must be able to tell the two apart.
    if _gate_failed(result):
        return NOT_ESTABLISHED
    # Nothing decided against this instance and nothing established it either.  Falling
    # through to "not established" here would turn every instance the run simply never
    # reached into an acquittal -- the exact conversion the contract exists to prevent.
    return UNRESOLVED


def _episode_quotes(binding_row: Mapping[str, Any], occurrence_id: str) -> tuple[str, ...]:
    """Exact source spans behind one occurrence, as Call 1.5 recorded them."""
    quotes: list[str] = []
    for seed in binding_row.get("seed_results") or []:
        for binding in seed.get("bindings") or []:
            if binding.get("binding_id") != occurrence_id:
                continue
            for key in ("actor_action_fragments", "context_fragments"):
                for fragment in binding.get(key) or []:
                    quote = str(fragment.get("source_quote", "")).strip()
                    if quote and quote not in quotes:
                        quotes.append(quote)
    return tuple(quotes)


def _participation_route(
    registry: DefinitionRegistry, result: Mapping[str, Any]
) -> ParticipationRoute | None:
    """Recover the accessory route from the stage provenance.

    Losing this turns an instigator into a principal in the written answer, so a mode
    without its principal is refused rather than emitted half-formed.
    """
    mode: str | None = None
    for stage_name in ("elements", "unlawfulness", "culpability", "punishability"):
        stage = result.get(stage_name) or {}
        for outcome in stage.get("provenance") or []:
            obligation = outcome.get("obligation") or {}
            if "mode" in obligation:
                mode = str(obligation["mode"])
    if mode is None:
        return None
    return ParticipationRoute(
        mode=mode,
        principal_actor=None,
        principal_offense=None,
        principal_realization=None,
    )


def _ground_fact_episode_map(
    binding_row: Mapping[str, Any],
    plan_row: Mapping[str, Any] | None,
) -> dict[str, str]:
    """occurrence_id -> factual_episode_id, the identity Call 2 canonicalizes GroundFacts on.

    A real Call 1.5 binding carries its episode directly on itself in `binding_row`.  A
    binding the planner derived (a `derived_binding:*` occurrence_id) has no entry there;
    its episode only exists in the planner's `InstanceProvenance`, which is why `plan_row`
    is accepted and, where given, is authoritative -- it is exactly what generated the Call 2
    request. An occurrence absent from both stays unmapped rather than guessed.
    """
    mapping: dict[str, str] = {}
    for seed in binding_row.get("seed_results") or []:
        for binding in seed.get("bindings") or []:
            binding_id = binding.get("binding_id")
            episode_id = binding.get("factual_episode_id")
            if binding_id and episode_id:
                mapping[str(binding_id)] = str(episode_id)
    if plan_row:
        for entry in plan_row.get("instance_provenance") or []:
            occurrence_id = (entry.get("instance_key") or {}).get("occurrence_id")
            episode_id = entry.get("factual_episode_id")
            if occurrence_id and episode_id:
                mapping[str(occurrence_id)] = str(episode_id)
    return mapping


def _check_ground_fact_canonicalization(
    registry: DefinitionRegistry,
    truth_rows: Sequence[Mapping[str, Any]],
    episode_by_occurrence: Mapping[str, str],
) -> None:
    """Refuse a plan built on a GroundFact that disagrees with itself about one episode.

    `truth_rows` is both carriers concatenated -- `case_truths` and `assessments`.  Rows
    repeated across the two agree and cost nothing; a disagreement between them is itself a
    conflict worth refusing, since the two feed different downstream stages.

    This is a corruption detector, not a repair path.  A well-formed Call 2 artifact cannot
    trip it, because occurrence-level GroundFact canonicalization already asks each
    (case, actor, factual_episode, ground_predicate) once and projects the single answer to
    every consuming offense instance.  Firing here means that guarantee did not hold for the
    artifact the plan was built from -- an older run, or a defect in a newer one -- and the
    plan does not get to pick a side by majority, polarity, or UNKNOWN downgrade.  An
    occurrence this guard cannot place in an episode is not evidence either way, so it is
    skipped rather than treated as a conflict.
    """
    seen: dict[tuple[str, str, str, str], tuple[str, str]] = {}
    conflicts: list[str] = []
    for row in truth_rows:
        predicate_ref = str(row.get("predicate_ref", ""))
        if not predicate_ref or registry.kind_of(predicate_ref) != "ground_fact":
            continue
        instance = row.get("instance_key") or {}
        occurrence_id = str(instance.get("occurrence_id", ""))
        episode_id = episode_by_occurrence.get(occurrence_id)
        if episode_id is None:
            continue
        case_id = str(instance.get("case_id", ""))
        actor_id = str(instance.get("actor_id", ""))
        truth = str(row.get("truth", ""))
        key = (case_id, actor_id, episode_id, predicate_ref)
        if key in seen:
            prior_truth, prior_occurrence = seen[key]
            if prior_truth != truth:
                conflicts.append(
                    f"{predicate_ref} @ {episode_id} ({actor_id}): "
                    f"{prior_occurrence}={prior_truth} vs {occurrence_id}={truth}"
                )
        else:
            seen[key] = (truth, occurrence_id)
    if conflicts:
        raise AnswerPlanError(
            "CROSS_INSTANCE_GROUND_FACT_CONFLICT: " + "; ".join(sorted(conflicts))
        )


def build_answer_plan(
    *,
    case_id: str,
    case_text: str,
    question: str,
    binding_row: Mapping[str, Any],
    call2_row: Mapping[str, Any],
    e2e_row: Mapping[str, Any],
    registry: DefinitionRegistry,
    offense_labels: Mapping[str, str] | None = None,
    representation_gaps: Sequence[str] = (),
    contested_points: Mapping[str, Sequence[ContestedPoint]] | None = None,
    rule_statements: Mapping[str, Sequence[RuleStatement]] | None = None,
    plan_row: Mapping[str, Any] | None = None,
) -> AnswerPlan:
    """Assemble one case's plan from the three canonical artifacts.

    ``contested_points`` and ``rule_statements`` are injected by the caller keyed on
    ``issue_id`` so their provenance is decided outside this projection.  Nothing is
    invented here when they are absent -- an empty slot means the answer simply will not
    be prompted for that discussion.  ``plan_row`` is the optional Step 8 planner artifact
    row; it extends the GroundFact conflict guard's episode identity to derived bindings.
    """
    contested_points = contested_points or {}
    rule_statements = rule_statements or {}

    final = e2e_row.get("final_responsibility") or {}
    retained = frozenset(instance_ref(i) for i in final.get("retained_instances") or [])
    absorbed_records = final.get("absorbed_instances") or []
    absorbed = frozenset(
        instance_ref(record.get("instance", record)) for record in absorbed_records
    )
    withheld = frozenset(
        instance_ref(i) for i in final.get("attribution_withheld_instances") or []
    )
    # `case_truths` is the authority: it is what Scallop and the final-responsibility stage
    # consumed to reach the conclusions this plan restates.  `assessments` is the raw output
    # of one Call 2 run and stays available as a secondary carrier for neural provenance --
    # exact quotes and per-request evidence -- which no truth is invented from.
    truths = call2_row.get("case_truths") or []
    assessments = call2_row.get("assessments") or []
    episodes = _ground_fact_episode_map(binding_row, plan_row)
    _check_ground_fact_canonicalization(registry, (*truths, *assessments), episodes)

    issues: list[AnchoredIssue] = []
    for entry in e2e_row.get("liability_results") or []:
        instance = entry.get("instance_key") or {}
        result = entry.get("result") or {}
        ref = instance_ref(instance)
        offense_ref = str(instance.get("offense_ref", ""))
        satisfied, failed, blocking = _findings_for_instance(registry, truths, ref, {})
        state = _final_state(result, ref, retained, absorbed, withheld, bool(blocking))
        completion = result.get("completion") or {}
        route = _participation_route(registry, result)
        issue = AnchoredIssue(
            issue_id=ref,
            actor=str(instance.get("actor_id", "")),
            offense_label=offense_label(registry, offense_ref, offense_labels),
            governing_provision=governing_provision(registry, offense_ref),
            episode_quotes=_episode_quotes(binding_row, str(instance.get("occurrence_id", ""))),
            final_state=state,
            completion_state=completion.get("state"),
            completion_why=None,
            participation=route,
            decisive_stage=result.get("decisive_stage"),
            satisfied=tuple(
                _with_rule_statements(f, rule_statements.get(ref, ())) for f in satisfied
            ),
            failed=failed,
            blocking=blocking,
            doctrines=tuple(_doctrines_for(e2e_row, ref)),
            contested_points=tuple(contested_points.get(ref, ())),
            gate_failed=_gate_failed(result),
        )
        issues.append(issue)

    plan = AnswerPlan(
        case_id=case_id,
        case_text=case_text,
        question=question,
        discussion_order=tuple(_discussion_order(issues, absorbed_records)),
        anchored_issues=tuple(issues),
        required_final_conclusions=tuple(_required_final_conclusions(issues)),
        final_responsibility=FinalResponsibility(
            retained=tuple(
                {
                    "actor": str(i.get("actor_id", "")),
                    "offense": offense_label(
                        registry, str(i.get("offense_ref", "")), offense_labels
                    ),
                }
                for i in final.get("retained_instances") or []
            ),
            absorbed=tuple(_absorption_records(registry, absorbed_records, offense_labels)),
            imaginative_pairs=tuple(
                _pair_records(registry, final.get("imaginative_concurrence_pairs") or [], offense_labels)
            ),
            excess_attributions=tuple(
                _excess_records(registry, final.get("excess_attributions") or [], offense_labels)
            ),
            status_redirections=tuple(
                _redirection_records(registry, final.get("status_redirections") or [], offense_labels)
            ),
        ),
        representation_gaps=tuple(representation_gaps),
        unmapped_instances=(),
    )
    check_contracts(plan)
    return plan


def _with_rule_statements(finding: Finding, extra: Sequence[RuleStatement]) -> Finding:
    if not extra:
        return finding
    return Finding(
        label=finding.label,
        truth=finding.truth,
        legal_standard=finding.legal_standard,
        governing_provision=finding.governing_provision,
        rule_statements=tuple(finding.rule_statements) + tuple(extra),
        supporting_quotes=finding.supporting_quotes,
    )


def _doctrines_for(e2e_row: Mapping[str, Any], ref: str) -> list[Mapping[str, Any]]:
    """Active doctrines only.  A doctrine that was raised but never fired is not law here."""
    out: list[Mapping[str, Any]] = []
    for doctrine in e2e_row.get("active_doctrines") or []:
        instance = doctrine.get("instance") or doctrine.get("instance_key") or {}
        if instance and instance_ref(instance) != ref:
            continue
        out.append(doctrine)
    return out


def _absorption_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None = None,
) -> list[Mapping[str, Any]]:
    """Both sides of every absorbed pair.

    Dropping the absorbed offence from the plan would make it disappear from the answer,
    and an answer that never says why the lesser offence does not stand separately has
    simply omitted a point it was supposed to make.
    """
    out: list[Mapping[str, Any]] = []
    for record in records:
        absorbed_instance = record.get("instance") or record.get("absorbed") or {}
        absorbing_instance = record.get("absorbed_by") or record.get("absorbing") or {}
        out.append(
            {
                "absorbed_offense": offense_label(
                    registry, str(absorbed_instance.get("offense_ref", "")), offense_labels
                ),
                "absorbing_offense": offense_label(
                    registry, str(absorbing_instance.get("offense_ref", "")), offense_labels
                )
                if absorbing_instance
                else None,
                "relation": record.get("relation") or record.get("kind"),
                "condition_statement": record.get("condition_statement"),
                "legal_standard": record.get("legal_standard"),
            }
        )
    return out


def _excess_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    """Say who is not answerable for what, in offence names rather than in refs."""
    out: list[Mapping[str, Any]] = []
    for record in records:
        accessory = record.get("accessory_instance") or {}
        out.append(
            {
                "actor": str(accessory.get("actor_id", "")),
                "accessory_offense": offense_label(
                    registry, str(accessory.get("offense_ref", "")), offense_labels
                ),
                "excess_offense": offense_label(
                    registry, str(record.get("excess_offense_ref", "")), offense_labels
                ),
                "effect": str(record.get("effect", "")),
            }
        )
    return out


def _pair_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    out: list[Mapping[str, Any]] = []
    for record in records:
        first = record.get("first") or record.get("left") or {}
        second = record.get("second") or record.get("right") or {}
        out.append(
            {
                "first_offense": offense_label(
                    registry, str(first.get("offense_ref", "")), offense_labels
                ),
                "second_offense": offense_label(
                    registry, str(second.get("offense_ref", "")), offense_labels
                ),
            }
        )
    return out


def _redirection_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    """Article 33 proviso: the participant answers under a different offence."""
    out: list[Mapping[str, Any]] = []
    for record in records:
        instance = record.get("instance") or record.get("participant_instance") or {}
        out.append(
            {
                "actor": str(instance.get("actor_id", "")),
                "from_offense": offense_label(
                    registry, str(instance.get("offense_ref", "")), offense_labels
                ),
                "to_offense": offense_label(
                    registry, str(record.get("redirected_offense_ref", "")), offense_labels
                )
                if record.get("redirected_offense_ref")
                else None,
            }
        )
    return out


def _discussion_order(
    issues: Sequence[AnchoredIssue], absorbed_records: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Order issues so a prerequisite is never discussed after what depends on it.

    Only one dependency is representable today: an absorbed offence has to be settled
    before the offence that absorbs it can be stated as the final one.
    """
    order = [issue.issue_id for issue in issues]
    absorbed_first = {
        instance_ref(record.get("instance") or {}): instance_ref(record.get("absorbed_by") or {})
        for record in absorbed_records
    }
    for absorbed_ref, absorbing_ref in absorbed_first.items():
        if absorbed_ref not in order or absorbing_ref not in order:
            continue
        if order.index(absorbed_ref) > order.index(absorbing_ref):
            order.remove(absorbed_ref)
            order.insert(order.index(absorbing_ref), absorbed_ref)
    return order


# --------------------------------------------------------------------------------------
# contracts
# --------------------------------------------------------------------------------------


def check_contracts(plan: AnswerPlan) -> None:
    """Refuse a plan that would mislead the writer.  ANSWERPLAN_SPEC section 4."""
    for issue in plan.anchored_issues:
        if issue.participation is not None and not issue.participation.mode:
            raise AnswerPlanError(f"{issue.issue_id}: participation without a mode")
        if issue.final_state == NOT_ESTABLISHED and not issue.gate_failed:
            # The run deciding against an instance is what makes an acquittal sayable.  A
            # gate can fail on a relation obligation rather than on a predicate, so the
            # predicate lists are not evidence either way -- only the gate is.
            raise AnswerPlanError(
                f"{issue.issue_id}: unresolved elements reported as not established"
            )
        for point in issue.contested_points:
            if point.origin not in _ALLOWED_CONTESTED_ORIGINS:
                raise AnswerPlanError(f"{issue.issue_id}: contested point from {point.origin!r}")
    for record in plan.final_responsibility.absorbed:
        if not record.get("absorbed_offense") or not record.get("absorbing_offense"):
            raise AnswerPlanError("absorbed pair is missing one of its two sides")


def assert_no_internal_markers(payload: str) -> None:
    """The serialized analysis must read as law, not as machine state."""
    found = [marker for marker in _INTERNAL_MARKERS if marker in payload]
    if found:
        raise AnswerPlanError(f"internal markers leaked into the Call 3 payload: {found}")


def assert_no_rubric_fields(payload: Mapping[str, Any] | str) -> None:
    """No field may carry this question's rubric item count or score.

    Hiding the rubric text is not enough.  "37 items, 30 points" is a per-question gold
    annotation, and handing it to the generator would make the answer length a function of
    the grading key rather than of the analysis.
    """
    blob = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    for marker in ("rubric_item_count", "rubric_count", "rubric_summary", "\"score\""):
        if marker in blob:
            raise AnswerPlanError(f"rubric-derived field {marker!r} reached the answer plan")


# --------------------------------------------------------------------------------------
# serialization for the model
# --------------------------------------------------------------------------------------

_STATE_PROSE = {
    ESTABLISHED: "성립한다.",
    NOT_ESTABLISHED: "성립하지 않는다.",
    UNRESOLVED: "주어진 사실만으로는 성부를 확정하기 어렵다.",
    NOT_ATTRIBUTABLE: "이 행위자에게 귀속되지 않는다.",
    ABSORBED: "따로 성립하지 않는다. 다른 죄에 흡수된다.",
}

#: Participation modes in the words a Korean criminal-law answer uses for them.
_MODE_PROSE = {
    "co_principal": "공동정범",
    "instigator": "교사범",
    "aider": "방조범",
}

_COMPLETION_PROSE = {
    "completed": "기수",
    "attempt": "미수",
    "abandonment": "중지미수",
    "preparation": "예비",
}


def _required_final_conclusions(
    issues: Sequence[AnchoredIssue],
) -> tuple[RequiredFinalConclusion, ...]:
    """One anchor per anchored issue, reusing the exact vocabulary `analysis` is written in.

    Anchor and analysis body share `_STATE_PROSE`/`_COMPLETION_PROSE`/`_MODE_PROSE` on
    purpose -- an anchor list in different words than the body would just relocate the
    drift this list exists to prevent, rather than remove it.
    """
    out: list[RequiredFinalConclusion] = []
    for issue in issues:
        out.append(
            RequiredFinalConclusion(
                actor=issue.actor,
                offense_label=issue.offense_label,
                state=_STATE_PROSE.get(issue.final_state, issue.final_state),
                completion_state=_COMPLETION_PROSE.get(issue.completion_state)
                if issue.completion_state in _COMPLETION_PROSE
                else None,
                participation_mode=(
                    _MODE_PROSE.get(issue.participation.mode, issue.participation.mode)
                    if issue.participation is not None
                    else None
                ),
            )
        )
    return tuple(out)


def serialize_analysis(plan: AnswerPlan) -> str:
    """Render the plan as the prose block the prompt calls ``analysis``.

    Field names do not reach the model.  What reaches it is a lawyer's reading of the same
    content, in the discussion order the plan fixed.
    """
    by_id = {issue.issue_id: issue for issue in plan.anchored_issues}
    lines: list[str] = []
    for position, issue_id in enumerate(plan.discussion_order, start=1):
        issue = by_id.get(issue_id)
        if issue is None:
            continue
        lines.extend(_serialize_issue(position, issue))
        lines.append("")
    lines.extend(_serialize_final(plan.final_responsibility))
    payload = "\n".join(lines).strip() + "\n"
    assert_no_internal_markers(payload)
    assert_no_rubric_fields(payload)
    return payload


def _serialize_issue(position: int, issue: AnchoredIssue) -> list[str]:
    head = f"[{position}] {issue.actor} — {issue.offense_label}"
    if issue.governing_provision:
        head += f" ({issue.governing_provision})"
    lines = [head, f"    결론: {_STATE_PROSE.get(issue.final_state, issue.final_state)}"]
    if issue.absorbed_into:
        lines.append(f"        흡수되는 죄: {issue.absorbed_into}")
        if issue.absorption_reason:
            lines.append(f"        흡수 근거: {issue.absorption_reason}")
    if issue.not_attributable_reason:
        lines.append(f"        귀속되지 않는 이유: {issue.not_attributable_reason}")
    if issue.participation is not None:
        mode = issue.participation.mode
        lines.append(f"    가담 형태: {_MODE_PROSE.get(mode, mode)}")
        if issue.participation.principal_actor:
            lines.append(f"        정범: {issue.participation.principal_actor}")
        if issue.participation.principal_offense:
            lines.append(f"        정범의 죄: {issue.participation.principal_offense}")
    if issue.completion_state in _COMPLETION_PROSE:
        lines.append(f"    기수 여부: {_COMPLETION_PROSE[issue.completion_state]}")
    elif issue.completion_state:
        # An unresolved completion is not a stage word to be echoed at the writer.  It is
        # one more thing the facts did not settle, and it is said that way or not at all.
        lines.append("    기수 여부: 주어진 사실만으로는 확정하기 어렵다.")
    if issue.episode_quotes:
        lines.append("    관련 사실")
        for quote in issue.episode_quotes:
            lines.append(f"      · \"{quote}\"")
    lines.extend(_serialize_findings("인정된 요건", issue.satisfied))
    lines.extend(_serialize_findings("인정되지 않은 요건", issue.failed))
    lines.extend(_serialize_findings("확정되지 않은 요건", issue.blocking))
    for point in issue.contested_points:
        lines.append(f"    견해가 갈리는 지점: {point.label}")
        for stance in point.positions:
            lines.append(f"        · {stance}")
        lines.append(f"        채택: {point.adopted} — {point.why_adopted}")
    for doctrine in issue.doctrines:
        label = doctrine.get("display_name") or doctrine.get("label")
        if label:
            lines.append(f"    적용되는 법리: {label}")
    return lines


def _serialize_findings(title: str, findings: Sequence[Finding]) -> list[str]:
    if not findings:
        return []
    lines = [f"    {title}"]
    for finding in findings:
        lines.append(f"      · {finding.label}")
        if finding.legal_standard and finding.legal_standard != finding.label:
            lines.append(f"        판단 기준: {finding.legal_standard}")
        if finding.governing_provision:
            lines.append(f"        근거 조문: {finding.governing_provision}")
        for statement in finding.rule_statements:
            mark = "[판례 법리]" if statement.origin == "reviewed_card" else "[법리]"
            lines.append(f"        {mark} {statement.statement}")
        for quote in finding.supporting_quotes:
            lines.append(f"        근거 사실: \"{quote}\"")
    return lines


def _serialize_final(final: FinalResponsibility) -> list[str]:
    lines = ["최종 죄책"]
    if final.retained:
        # Grouped by actor: two actors answering for theft is not one conclusion said
        # twice, and an answer that loses the actor loses the conclusion.
        by_actor: dict[str, list[str]] = {}
        for record in final.retained:
            by_actor.setdefault(record["actor"], []).append(record["offense"])
        for actor, offenses in by_actor.items():
            lines.append(f"    {actor}: {', '.join(offenses)}")
    else:
        lines.append("    성립이 확정된 죄가 없다.")
    for record in final.absorbed:
        relation = record.get("relation") or "흡수"
        lines.append(
            f"    {record['absorbed_offense']}는 {record['absorbing_offense']}에 "
            f"{relation} 관계로 흡수되어 따로 성립하지 않는다."
        )
        if record.get("condition_statement"):
            lines.append(f"        흡수 근거: {record['condition_statement']}")
    for pair in final.imaginative_pairs:
        lines.append(
            f"    {pair['first_offense']}와 {pair['second_offense']}는 상상적 경합 관계다."
        )
    for attribution in final.excess_attributions:
        lines.append(
            f"    {attribution['actor']}의 {attribution['accessory_offense']} 가담 범위를 "
            f"넘는 {attribution['excess_offense']} 부분은 그에게 귀속되지 않는다."
        )
    for redirection in final.status_redirections:
        target = redirection.get("to_offense")
        if target:
            lines.append(
                f"    {redirection['actor']}는 신분에 따라 {redirection['from_offense']}가 "
                f"아니라 {target}의 죄책을 진다."
            )
    return lines


def serialize_open_points(plan: AnswerPlan) -> str:
    """What the analysis did not cover, stated as areas rather than as answers."""
    lines: list[str] = []
    for gap in plan.representation_gaps:
        lines.append(f"· {gap}")
    for instance in plan.unmapped_instances:
        lines.append(f"· {instance}")
    if not lines:
        return "위 분석이 다루지 않은 영역으로 특정된 것은 없다."
    return "\n".join(lines)


def serialize_required_final_conclusions(plan: AnswerPlan) -> str:
    """The closed list the closing paragraph must restate -- anchors, not sentences.

    Each line names an actor, an offence, and the one conclusion word for it.  The model
    still composes the sentence; this only fixes what the sentence has to say, so a
    closing paragraph that drops or inverts one of these is checkably wrong rather than
    merely a stylistic choice.
    """
    lines: list[str] = []
    for item in plan.required_final_conclusions:
        line = f"· {item.actor} — {item.offense_label}: {item.state}"
        if item.completion_state:
            line += f" ({item.completion_state})"
        if item.participation_mode:
            line += f" [{item.participation_mode}]"
        lines.append(line)
    payload = "\n".join(lines) if lines else "없음"
    assert_no_internal_markers(payload)
    assert_no_rubric_fields(payload)
    return payload


#: Headings a closing summary is asked to carry ("최종 죄책과 죄수관계를 정리한다").  The
#: exact wording and structure otherwise stay the writer's choice, so this is a marker
#: search, not a section-name whitelist.
_FINAL_SECTION_MARKERS = ("최종 죄책", "최종 결론", "죄수 및 최종", "최종 정리")


def extract_final_conclusion_section(answer_text: str) -> str:
    """The mechanically-cut tail of the answer the closing-paragraph instruction targets.

    F4 was not an absence from the answer -- the dropped actor's offences were discussed
    in the body -- it was an absence from the *closing* paragraph specifically.  A
    whole-document presence check cannot see that distinction, so this narrows to where
    the closing section begins and takes everything from there onward.

    The cut anchors on a heading line rather than on the last textual match, because
    "최종 죄책" also occurs inside conclusion sentences ("丙의 최종 죄책은 횡령죄이다"):
    cutting there would start the section midway and report the actors named above it as
    missing.  A heading is distinguished from a sentence by not ending in a full stop,
    which is what separates "III. 최종 죄책" from the sentence beneath it.  Absent any
    marker the last paragraph stands in, since an answer that skips the heading still
    ends with some closing block and widening back to the whole document would restore
    the very blind spot this replaces.
    """
    lines = answer_text.splitlines(keepends=True)
    heading_offset: int | None = None
    fallback_offset: int | None = None
    offset = 0
    for line in lines:
        stripped = line.strip()
        if any(marker in stripped for marker in _FINAL_SECTION_MARKERS):
            fallback_offset = offset
            if not stripped.endswith((".", "다", "。")):
                heading_offset = offset
        offset += len(line)
    start = heading_offset if heading_offset is not None else fallback_offset
    if start is not None:
        return answer_text[start:]
    paragraphs = [part for part in answer_text.split("\n\n") if part.strip()]
    return paragraphs[-1] if paragraphs else answer_text


def missing_required_final_conclusions(
    answer_text: str, plan: AnswerPlan
) -> tuple[RequiredFinalConclusion, ...]:
    """Mechanical presence check scoped to the closing section.  Never edits an answer.

    An anchor counts as covered when both the actor and the offence label occur in the
    closing section `extract_final_conclusion_section` isolates -- not anywhere in the
    document, which would pass even when the closing paragraph itself dropped the issue.
    This cannot tell whether the stated state is the *right* one; that is the fidelity
    contract on `analysis` (F1/F2), not this completeness check's job. A finding here is a
    fact for an offline audit, not a repair signal.
    """
    section = extract_final_conclusion_section(answer_text)
    missing: list[RequiredFinalConclusion] = []
    for item in plan.required_final_conclusions:
        if item.actor not in section or item.offense_label not in section:
            missing.append(item)
    return tuple(missing)
