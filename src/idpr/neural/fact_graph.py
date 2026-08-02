"""Call 1: the fact graph contract.

Call 1 reads the case once and emits two things -- descriptive facts in the closed
vocabulary of :mod:`idpr.rulebase.facts`, and a list of offences the facts point at. The
first feeds the symbolic layer; the second is a second entrance into retrieval's article
shortlist. Neither decides anything: the cards decide, in call 2.

The model does not mint identifiers
-----------------------------------
The first version of this contract was flat: one row per fact, each naming its predicate,
and satellite rows (target, place, purpose) referring to their parent act by a string
``actId`` the model had to invent and keep consistent. Measured over 61 questions, 52
failed validation -- 48 dangling act references (the model numbered acts after the fact
that mentioned them) and 180 duplicate fact ids. Guided decoding can constrain a value; it
cannot enforce a cross-reference, so the schema was asking for something it could not hold
the model to.

So acts now carry their satellites inline and the host assigns ``act_001…`` by position.
Ordering and causation refer to acts by **array index**, which is bounded by the schema and
cannot dangle. The 13 fact-layer predicates are unchanged -- only the shape the model fills
in is, and :func:`fact_tuples` still emits exactly those relations.

One quote per assertion, not per attribute
------------------------------------------
The same run produced 120 ``source_quote`` violations. Requiring an exact contiguous quote
for every satellite was the cause: an act's place and circumstance are attributes of one
event, and the case text usually has no separate span for them, so the model had to invent
one. A quote is now required per act, result, role, relation and holding -- the units that
are independently asserted -- and attributes ride on their act's quote.

Grounding itself is not relaxed: every quote is still checked as an exact substring of
``question_text``, and the host raises rather than repairs. That gate is the only thing
standing between a hallucinated fact and the symbolic layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.compile_scl import ArticleLabelError, article_label
from idpr.rulebase.facts import VOCABULARIES, validate_fact

SCHEMA_VERSION = "2.0.0"

_ENTITY_ID = r"^[a-z][a-z0-9_]*$"

EPISTEMIC_STATUSES = ("given", "asserted_by_actor", "disputed", "unknown")

#: Upper bounds. Generous rather than tight -- a truncated fact graph loses evidence
#: silently, which is worse than a long one.
MAX_ENTITIES = 12
MAX_ACTS = 40
MAX_RESULTS = 20
MAX_ISSUE_CANDIDATES = 8


class FactGraphError(ValueError):
    """Raised with every contract violation found, not just the first.

    One call is one GPU round trip; reporting a single error at a time would cost a re-run
    per mistake.
    """

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def _enum(vocabulary: str) -> dict[str, Any]:
    return {"enum": list(VOCABULARIES[vocabulary])}


def _labels(vocabulary: str, *, max_items: int) -> dict[str, Any]:
    return {
        "type": "array",
        "maxItems": max_items,
        "uniqueItems": True,
        "items": _enum(vocabulary),
    }


def _entity_ref() -> dict[str, Any]:
    return {"type": "string", "pattern": _ENTITY_ID}


def _act_index() -> dict[str, Any]:
    """An earlier act, by position. Bounded by the schema; cannot dangle."""
    return {"type": "integer", "minimum": 0, "maximum": MAX_ACTS - 1}


def fact_graph_schema() -> dict[str, Any]:
    """The JSON schema for call 1. Label vocabularies come from the fact-layer registry."""
    return {
        "$id": "idpr/FactGraph",
        "description": "Call 1 output: descriptive facts plus proposed offences.",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "version",
            "case_id",
            "entities",
            "acts",
            "results",
            "roles",
            "relations",
            "holdings",
            "issue_candidates",
            "retrieval_queries",
            "unresolved_questions",
        ],
        "properties": {
            "version": {"const": SCHEMA_VERSION},
            "case_id": {"type": "string", "minLength": 1},
            "entities": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_ENTITIES,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["entity_id", "mentions"],
                    "properties": {
                        "entity_id": _entity_ref(),
                        "mentions": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 4,
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                    },
                },
            },
            "acts": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_ACTS,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["actor", "act_label", "source_quote", "epistemic_status"],
                    "properties": {
                        "actor": _entity_ref(),
                        "act_label": _enum("ACT_LABELS"),
                        "source_quote": {"type": "string", "minLength": 1},
                        "epistemic_status": {"enum": list(EPISTEMIC_STATUSES)},
                        "targets": {
                            "type": "array",
                            "maxItems": 5,
                            "uniqueItems": True,
                            "items": _entity_ref(),
                        },
                        "objects": _labels("OBJECT_LABELS", max_items=4),
                        "place": _enum("PLACE_LABELS"),
                        "circumstances": _labels("ACT_CIRCUMSTANCES", max_items=6),
                        "purposes": _labels("PURPOSE_LABELS", max_items=3),
                        "after": _act_index(),
                    },
                },
            },
            "results": {
                "type": "array",
                "maxItems": MAX_RESULTS,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "result_label",
                        "entity",
                        "source_quote",
                        "epistemic_status",
                    ],
                    "properties": {
                        "result_label": _enum("RESULT_LABELS"),
                        "entity": _entity_ref(),
                        "source_quote": {"type": "string", "minLength": 1},
                        "epistemic_status": {"enum": list(EPISTEMIC_STATUSES)},
                        "causation": {
                            "type": "array",
                            "maxItems": 5,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["act", "attribution"],
                                "properties": {
                                    "act": _act_index(),
                                    "attribution": _enum("CAUSATION_LABELS"),
                                },
                            },
                        },
                    },
                },
            },
            "roles": {
                "type": "array",
                "maxItems": 20,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["entity", "role_label", "source_quote"],
                    "properties": {
                        "entity": _entity_ref(),
                        "role_label": _enum("ROLE_LABELS"),
                        "source_quote": {"type": "string", "minLength": 1},
                    },
                },
            },
            "relations": {
                "type": "array",
                "maxItems": 20,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["entity_a", "entity_b", "relation_label", "source_quote"],
                    "properties": {
                        "entity_a": _entity_ref(),
                        "entity_b": _entity_ref(),
                        "relation_label": _enum("RELATION_LABELS"),
                        "source_quote": {"type": "string", "minLength": 1},
                    },
                },
            },
            "holdings": {
                "type": "array",
                "maxItems": 20,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["entity", "object_label", "hold_label", "source_quote"],
                    "properties": {
                        "entity": _entity_ref(),
                        "object_label": _enum("OBJECT_LABELS"),
                        "hold_label": _enum("HOLD_LABELS"),
                        "source_quote": {"type": "string", "minLength": 1},
                    },
                },
            },
            "issue_candidates": {
                "type": "array",
                "minItems": 1,
                # Capped: every proposed article drags its whole card set into call 2,
                # because retrieval never drops cards inside a selected article.
                "maxItems": MAX_ISSUE_CANDIDATES,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "source_quote"],
                    "properties": {
                        "label": {"type": "string", "minLength": 1},
                        "article": {"type": "string"},
                        "source_quote": {"type": "string", "minLength": 1},
                    },
                },
            },
            "retrieval_queries": {
                "type": "array",
                "minItems": 1,
                "maxItems": 12,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
            "unresolved_questions": {
                "type": "array",
                "maxItems": 12,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
        },
    }


# --------------------------------------------------------------------------- #
# Host validation
# --------------------------------------------------------------------------- #


def act_id(index: int) -> str:
    """``act_001``. Assigned by the host, never by the model."""
    return f"act_{index + 1:03d}"


_WHITESPACE = re.compile(r"\s+")


def quote_is_grounded(quote: str, question_text: str) -> bool:
    """Whether a quote is a contiguous span of the case, ignoring whitespace.

    Whitespace only. Measured over 61 questions, 23 of 114 rejected quotes differed from
    the source by a single space ("간음하려 하였으나" -> "간음하려하였으나") -- the commentary
    and exam text carry inconsistent spacing and the model normalises it. Collapsing
    whitespace on both sides before comparing keeps the guarantee that matters (the span
    exists in the source, verbatim, in order) and drops a distinction that carries no
    meaning in Korean prose.

    Nothing else is normalised. A quote that changes a character -- "A를" for "A가", 25 of
    the 114 -- is a transcription error and must still fail: that is the gate working.
    """
    if quote in question_text:
        return True
    return _WHITESPACE.sub("", quote) in _WHITESPACE.sub("", question_text)


def validate_fact_graph(
    payload: Mapping[str, Any], *, case_id: str, question_text: str
) -> None:
    """Check one call-1 payload against the case it claims to describe.

    The schema has already fixed shape and vocabulary by the time this runs (guided
    decoding), so everything here is a cross-reference the schema cannot express: quotes
    against the source, entities against their declarations, act indices against position.
    """
    errors: list[str] = []

    if payload.get("case_id") != case_id:
        errors.append(
            f"case_id {payload.get('case_id')!r} does not match the requested case {case_id!r}"
        )

    entity_ids: set[str] = set()
    mention_owners: dict[str, list[str]] = {}
    for index, entity in enumerate(payload.get("entities", [])):
        entity_id = str(entity.get("entity_id", ""))
        if entity_id in entity_ids:
            errors.append(f"duplicate entity_id {entity_id!r}")
        entity_ids.add(entity_id)
        for mention in entity.get("mentions", []):
            if str(mention) not in question_text:
                errors.append(
                    f"entities[{index}] mention is not in question_text: {mention!r}"
                )
            mention_owners.setdefault(str(mention), []).append(entity_id)
    for mention, owners in mention_owners.items():
        unique = list(dict.fromkeys(owners))
        if len(unique) > 1:
            errors.append(f"mention {mention!r} resolves to multiple entities: {unique}")

    def check_quote(where: str, item: Mapping[str, Any]) -> None:
        if not quote_is_grounded(str(item.get("source_quote", "")), question_text):
            errors.append(f"{where} source_quote is not an exact question_text substring")

    def check_entity(where: str, value: Any) -> None:
        if str(value) not in entity_ids:
            errors.append(f"{where} references undeclared entity {value!r}")

    acts = payload.get("acts", [])
    for index, act in enumerate(acts):
        where = f"acts[{index}]"
        check_quote(where, act)
        check_entity(where, act.get("actor"))
        for target in act.get("targets", []):
            check_entity(f"{where}.targets", target)
        after = act.get("after")
        if after is not None and not 0 <= int(after) < index:
            # Strictly earlier: an act cannot follow itself or something not yet narrated,
            # and the pair becomes a ``precedes`` tuple the symbolic layer reasons over.
            errors.append(
                f"{where}.after={after} must be the index of an earlier act (< {index})"
            )

    for index, result in enumerate(payload.get("results", [])):
        where = f"results[{index}]"
        check_quote(where, result)
        check_entity(where, result.get("entity"))
        for position, link in enumerate(result.get("causation", [])):
            act_index = int(link.get("act", -1))
            if not 0 <= act_index < len(acts):
                errors.append(f"{where}.causation[{position}] act index {act_index} is out of range")

    for group, entity_fields in (
        ("roles", ("entity",)),
        ("relations", ("entity_a", "entity_b")),
        ("holdings", ("entity",)),
    ):
        for index, item in enumerate(payload.get(group, [])):
            where = f"{group}[{index}]"
            check_quote(where, item)
            for field in entity_fields:
                check_entity(where, item.get(field))

    for index, candidate in enumerate(payload.get("issue_candidates", [])):
        check_quote(f"issue_candidates[{index}]", candidate)

    if errors:
        raise FactGraphError(errors)


# --------------------------------------------------------------------------- #
# Admission: keep the grounded facts, drop the rest, and say what was dropped
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Admission:
    """What survived call 1, and what did not.

    Rejecting the whole payload on any violation was the wrong unit. A question carries
    roughly 30 quoted items; at a measured ~95% per-item accuracy that is one or two bad
    items per question, and whole-payload rejection turned that into 57 of 61 questions
    lost. The grounding guarantee is per fact -- an ungrounded fact must never reach the
    symbolic layer -- and it is fully kept by refusing that fact, not the case.

    Dropping is never silent: every rejection is counted here and written to the run
    artifact, so the extraction quality is a reported number rather than an assumption.
    """

    payload: dict[str, Any]
    dropped: dict[str, int]
    reasons: list[str]

    @property
    def dropped_total(self) -> int:
        return sum(self.dropped.values())

    def as_dict(self) -> dict[str, Any]:
        return {
            "dropped": dict(self.dropped),
            "dropped_total": self.dropped_total,
            "reasons": self.reasons,
        }


#: A payload this degraded is not a partially imperfect extraction, it is a failed one.
MIN_ADMITTED_ACT_FRACTION = 0.5


def admit_fact_graph(
    payload: Mapping[str, Any], *, case_id: str, question_text: str
) -> Admission:
    """Return the payload with every ungrounded or dangling item removed.

    Raises :class:`FactGraphError` only for damage no subset can repair: a payload
    describing another case, or one where too little of the extraction survived to be worth
    reasoning over.
    """
    if payload.get("case_id") != case_id:
        raise FactGraphError(
            [f"case_id {payload.get('case_id')!r} does not match requested {case_id!r}"]
        )

    dropped: dict[str, int] = {}
    reasons: list[str] = []

    def drop(group: str, why: str) -> None:
        dropped[group] = dropped.get(group, 0) + 1
        if len(reasons) < 40:
            reasons.append(why)

    entities: list[dict[str, Any]] = []
    entity_ids: set[str] = set()
    for index, entity in enumerate(payload.get("entities", [])):
        entity_id = str(entity.get("entity_id", ""))
        mentions = [m for m in entity.get("mentions", []) if str(m) in question_text]
        if not mentions or entity_id in entity_ids:
            drop("entities", f"entities[{index}] {entity_id!r}: no mention found in the case")
            continue
        entity_ids.add(entity_id)
        entities.append({"entity_id": entity_id, "mentions": mentions})

    if not entities:
        raise FactGraphError(["no entity survived: none of the mentions are in the case"])

    raw_acts = payload.get("acts", [])
    acts: list[dict[str, Any]] = []
    # Old index -> new index, so ``after`` and ``causation`` keep pointing at the right act.
    remap: dict[int, int] = {}
    for index, act in enumerate(raw_acts):
        if not quote_is_grounded(str(act.get("source_quote", "")), question_text):
            drop("acts", f"acts[{index}]: quote is not a span of the case")
            continue
        if str(act.get("actor", "")) not in entity_ids:
            drop("acts", f"acts[{index}]: actor {act.get('actor')!r} was not declared")
            continue
        kept = dict(act)
        kept["targets"] = [t for t in act.get("targets", []) if str(t) in entity_ids]
        after = act.get("after")
        # 61 of 742 uses pointed at the act's own index -- the model read ``after`` as an
        # identifier. One bad edge is not a reason to lose the act.
        if after is None or int(after) not in remap:
            kept.pop("after", None)
            if after is not None:
                drop("act_ordering", f"acts[{index}]: after={after} is not an earlier act")
        else:
            kept["after"] = remap[int(after)]
        remap[index] = len(acts)
        acts.append(kept)

    if raw_acts and len(acts) < MIN_ADMITTED_ACT_FRACTION * len(raw_acts):
        raise FactGraphError(
            [f"only {len(acts)} of {len(raw_acts)} acts are grounded; treating as a failure"]
        )

    results: list[dict[str, Any]] = []
    for index, result in enumerate(payload.get("results", [])):
        if not quote_is_grounded(str(result.get("source_quote", "")), question_text):
            drop("results", f"results[{index}]: quote is not a span of the case")
            continue
        if str(result.get("entity", "")) not in entity_ids:
            drop("results", f"results[{index}]: entity was not declared")
            continue
        kept = dict(result)
        links = []
        for link in result.get("causation", []):
            mapped = remap.get(int(link.get("act", -1)))
            if mapped is None:
                drop("causation", f"results[{index}]: causation points at a dropped act")
                continue
            links.append({"act": mapped, "attribution": link["attribution"]})
        kept["causation"] = links
        results.append(kept)

    def admit_simple(group: str, entity_fields: tuple[str, ...]) -> list[dict[str, Any]]:
        kept_items: list[dict[str, Any]] = []
        for index, item in enumerate(payload.get(group, [])):
            if not quote_is_grounded(str(item.get("source_quote", "")), question_text):
                drop(group, f"{group}[{index}]: quote is not a span of the case")
                continue
            if any(str(item.get(field, "")) not in entity_ids for field in entity_fields):
                drop(group, f"{group}[{index}]: references an undeclared entity")
                continue
            kept_items.append(dict(item))
        return kept_items

    candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(payload.get("issue_candidates", [])):
        if quote_is_grounded(str(candidate.get("source_quote", "")), question_text):
            candidates.append(dict(candidate))
        else:
            drop("issue_candidates", f"issue_candidates[{index}]: quote is not a span")

    admitted = {
        "version": payload.get("version"),
        "case_id": case_id,
        "entities": entities,
        "acts": acts,
        "results": results,
        "roles": admit_simple("roles", ("entity",)),
        "relations": admit_simple("relations", ("entity_a", "entity_b")),
        "holdings": admit_simple("holdings", ("entity",)),
        "issue_candidates": candidates,
        "retrieval_queries": list(payload.get("retrieval_queries", [])),
        "unresolved_questions": list(payload.get("unresolved_questions", [])),
    }
    return Admission(payload=admitted, dropped=dropped, reasons=reasons)


# --------------------------------------------------------------------------- #
# Accessors -- what the rest of the pipeline takes from a validated payload
# --------------------------------------------------------------------------- #


def fact_tuples(
    payload: Mapping[str, Any], *, case_id: str
) -> list[tuple[str, tuple[str, ...]]]:
    """``(relation, arguments)`` rows for the Scallop fact layer.

    Every row is passed through :func:`idpr.rulebase.facts.validate_fact`, so a label the
    schema somehow let through still cannot reach the symbolic layer.
    """
    rows: list[tuple[str, tuple[str, ...]]] = [
        ("person", (case_id, str(entity["entity_id"])))
        for entity in payload.get("entities", [])
    ]

    for item in payload.get("roles", []):
        rows.append(("role", (case_id, str(item["entity"]), str(item["role_label"]))))

    for index, act in enumerate(payload.get("acts", [])):
        identifier = act_id(index)
        rows.append(("act", (case_id, identifier, str(act["actor"]), str(act["act_label"]))))
        for target in act.get("targets", []):
            rows.append(("act_target", (case_id, identifier, str(target))))
        for label in act.get("objects", []):
            rows.append(("act_object", (case_id, identifier, str(label))))
        if act.get("place"):
            rows.append(("act_place", (case_id, identifier, str(act["place"]))))
        for label in act.get("circumstances", []):
            rows.append(("act_circumstance", (case_id, identifier, str(label))))
        for label in act.get("purposes", []):
            rows.append(("purpose", (case_id, identifier, str(label))))
        after = act.get("after")
        if after is not None:
            rows.append(("precedes", (case_id, act_id(int(after)), identifier)))

    for result in payload.get("results", []):
        rows.append(
            ("result", (case_id, str(result["result_label"]), str(result["entity"])))
        )
        for link in result.get("causation", []):
            rows.append(
                (
                    "causation",
                    (
                        case_id,
                        act_id(int(link["act"])),
                        str(result["result_label"]),
                        str(link["attribution"]),
                    ),
                )
            )

    for item in payload.get("relations", []):
        rows.append(
            (
                "party_relation",
                (
                    case_id,
                    str(item["entity_a"]),
                    str(item["entity_b"]),
                    str(item["relation_label"]),
                ),
            )
        )

    for item in payload.get("holdings", []):
        rows.append(
            (
                "holds",
                (
                    case_id,
                    str(item["entity"]),
                    str(item["object_label"]),
                    str(item["hold_label"]),
                ),
            )
        )

    for name, arguments in rows:
        validate_fact(name, arguments)
    return rows


def assessment_facts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Give each grounded assertion a stable host-owned id for call 2.

    The extraction contract deliberately makes one grounding decision per act, result,
    role, relation, or holding; attributes such as an act's place ride on that assertion.
    Call 2 uses the same granularity, so it can cite evidence without inventing identifiers
    or pretending that an inline attribute had an independent source quote.
    """
    facts: list[dict[str, Any]] = []
    for kind, group in (
        ("act", "acts"),
        ("result", "results"),
        ("role", "roles"),
        ("relation", "relations"),
        ("holding", "holdings"),
    ):
        for item in payload.get(group, []):
            facts.append(
                {
                    "fact_id": f"fact_{len(facts) + 1:03d}",
                    "kind": kind,
                    "assertion": dict(item),
                }
            )
    return facts


def fact_derived_queries(payload: Mapping[str, Any]) -> list[str]:
    """One query per asserted event, built from the fact layer itself.

    The plan puts the fact graph -- not the model's prose -- at the head of retrieval, and
    this is the part of that the first implementation left out. It matters because the
    model writes as many queries as it feels like: measured on a multi-episode case, an
    eight-act narrative got five, two of which were spent on a paragraph the sub-question does not
    ask about, and the intrusion episode got none at all. Its article was then missed even
    though the extraction had recorded ``출입 @ 공동주택공용부``.

    So query coverage becomes a function of how many events the case has, not of the
    model's budget. Nothing here inspects labels or articles: each event contributes
    whatever attributes it happens to carry, in registry order, for every case alike.
    """
    queries: list[str] = []

    for act in payload.get("acts", []):
        parts = [str(act.get("act_label", ""))]
        parts.extend(str(value) for value in act.get("objects", []))
        if act.get("place"):
            parts.append(str(act["place"]))
        parts.extend(str(value) for value in act.get("circumstances", []))
        parts.extend(str(value) for value in act.get("purposes", []))
        queries.append(" ".join(part for part in parts if part))

    for result in payload.get("results", []):
        parts = [str(result.get("result_label", ""))]
        parts.extend(
            str(link.get("attribution", "")) for link in result.get("causation", [])
        )
        queries.append(" ".join(part for part in parts if part))

    for holding in payload.get("holdings", []):
        queries.append(
            f"{holding.get('object_label', '')} {holding.get('hold_label', '')}".strip()
        )

    for relation in payload.get("relations", []):
        queries.append(str(relation.get("relation_label", "")))

    return [query for query in dict.fromkeys(queries) if query]


def retrieval_queries(payload: Mapping[str, Any]) -> list[str]:
    """Queries for L0: the model's own, its issue labels, and the facts themselves.

    Candidate labels are included because a candidate the model can name but not number
    still has to reach its article through retrieval -- measured, the model fills
    ``article`` on 36 of 258 candidates and none of them resolve into the corpus, so the
    label is the only usable part.
    """
    queries = [str(query) for query in payload.get("retrieval_queries", [])]
    queries.extend(
        str(candidate["label"]) for candidate in payload.get("issue_candidates", [])
    )
    queries.extend(fact_derived_queries(payload))
    return list(dict.fromkeys(queries))


_LABEL_RE = re.compile(r"제\s*\d+\s*조(?:의\s*\d+)?")


def _article_index(corpus: CardCorpus) -> dict[str, str]:
    """``제298조`` -> ``art298``, built by inverting the compiler's own label function."""
    index: dict[str, str] = {}
    for article in corpus.by_article():
        index[article] = article
        try:
            index[article_label(article)] = article
        except ArticleLabelError:
            continue
    return index


def proposed_articles(
    payload: Mapping[str, Any], *, corpus: CardCorpus | None = None
) -> list[str]:
    """Article keys named in ``issue_candidates``.

    Only articles the card corpus actually covers are returned. A candidate naming an
    article outside the 51 is neither an error nor silently dropped -- it is a coverage gap,
    reported by :func:`unmatched_article_labels`, because the corpus scope is a stated
    limitation and must not read as a retrieval miss.
    """
    corpus = corpus or card_corpus()
    index = _article_index(corpus)
    articles: list[str] = []
    for candidate in payload.get("issue_candidates", []):
        key = _normalise_article(str(candidate.get("article", "")), index)
        if key is not None:
            articles.append(key)
    return list(dict.fromkeys(articles))


def unmatched_article_labels(
    payload: Mapping[str, Any], *, corpus: CardCorpus | None = None
) -> list[str]:
    """Articles the model named that the card corpus does not cover."""
    corpus = corpus or card_corpus()
    index = _article_index(corpus)
    unmatched: list[str] = []
    for candidate in payload.get("issue_candidates", []):
        raw = str(candidate.get("article", "")).strip()
        if raw and _normalise_article(raw, index) is None:
            unmatched.append(raw)
    return list(dict.fromkeys(unmatched))


def _normalise_article(raw: str, index: Mapping[str, str]) -> str | None:
    candidate = raw.strip()
    if not candidate:
        return None
    if candidate in index:
        return index[candidate]
    match = _LABEL_RE.search(candidate)
    if match is None:
        return None
    return index.get(re.sub(r"\s+", "", match.group(0)))
