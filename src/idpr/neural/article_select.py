"""Call 1.5: which offence families does this case actually put in issue?

Complements similarity retrieval in the article decision. The corpus covers 51 articles;
the model sees the 48 substantive/base provisions, while three generic attempt provisions
are host-derived. Retrieval supplies a bounded recall-oriented shortlist; selection reviews
every member and may add an independently discovered article from the catalog.

That relation is not similarity. "가슴과 음부를 스스로 만지게 하였다" and the card's
"피해자를 도구로 삼아 …추행행위를 한 경우" share no terms and are not near each other in
any general-purpose embedding space; what connects them is that the first *instantiates*
the second. Nothing in the retrieval stack was trained on that mapping and there is no
corpus here to train it on. A model that read Korean criminal law in pretraining already
has it. All it lacks is the article-number vocabulary, and the catalog supplies exactly
that.

The selector is the precision lane, while retrieval is the recall lane.  This distinction
matters after the issue-first migration: a spare article no longer costs a few flat card
statuses; it can wake an entire issue hierarchy and make the final answer discuss a crime
that the facts never raised.  The prompt therefore asks for a minimal fact-linked set,
so a retrieved article is never activated merely because it was similar.

Two things the host keeps, both for the same reason -- the model must not mint identifiers:

* ``article`` is a JSON-schema enum over the selectable catalog keys, so guided decoding
  makes an invented article number ungrammatical. Call 1 measured the alternative: asked to recall
  article numbers from memory it matched 0 of 258 issue candidates. Selection from a
  presented list is a different task, and that 0.000 is not evidence against it.
* attempt articles (제254·300·342조) are not selectable model labels.  They are appended
  deterministically from ``stage.yaml`` after a base offence is selected.  This prevents
  the model from selecting only a generic attempt provision while omitting the offence
  whose attempted commission the facts actually describe.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from idpr.rulebase.doctrine import CATALOG_PATH, STAGE_PATH

#: Bumped when the request contract changes in a way that invalidates cached outputs.
SCHEMA_VERSION = "1.7.0"
NO_SUBSTANTIVE_OFFENSE = "no_substantive_offense"
SUBSTANTIVE_DOMAIN = "substantive_criminal_law"
NON_SUBSTANTIVE_DOMAIN = "non_substantive_question"

#: Structural ceiling, not a target. The prompt asks for a minimal fact-linked set; this
#: additionally prevents a degenerate response from selecting the whole corpus.
MAX_SELECTED = 24


class ArticleSelectError(ValueError):
    """Raised when a selection response violates the contract.

    Carries every problem rather than the first, so one GPU run reports all of them.
    """

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def load_catalog(path: Path | None = None) -> tuple[dict[str, str], ...]:
    """The article catalog, in statute order. One entry per article the corpus covers."""
    payload = _read_json(path or CATALOG_PATH)
    return tuple(dict(entry) for entry in payload["articles"])


def _read_json(path: Path) -> Mapping[str, Any]:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def catalog_keys(catalog: Iterable[Mapping[str, str]] | None = None) -> tuple[str, ...]:
    return tuple(entry["key"] for entry in (catalog or load_catalog()))


def selectable_catalog(
    catalog: Iterable[Mapping[str, str]] | None = None,
    *,
    attempt_mapping: Mapping[str, str] | None = None,
) -> tuple[dict[str, str], ...]:
    """Return substantive provisions that Call 1.5 may emit.

    Generic attempt provisions are host-derived dependencies, not independent offence
    hypotheses. Keeping them out of the enum makes that ownership boundary structural.
    """
    entries = tuple(dict(entry) for entry in (catalog or load_catalog()))
    mapping = attempt_article_map() if attempt_mapping is None else attempt_mapping
    derived = set(mapping.values())
    return tuple(entry for entry in entries if entry["key"] not in derived)


def catalog_lines(catalog: Iterable[Mapping[str, str]] | None = None) -> list[str]:
    """``art298 제298조 강제추행`` -- one line per selectable article, key first.

    The key leads because the key is what the model must emit. Putting the human-readable
    label first would invite it to answer with the label. General rules are deliberately
    not repeated across the full catalog: the measured all-core variant diluted routing,
    while Call 1's grounded issue hints provide case-specific focus.
    """
    return [
        f"{entry['key']} {entry['label']} {entry['offense']}"
        for entry in (catalog or selectable_catalog())
    ]


def article_select_schema(
    catalog: Iterable[Mapping[str, str]] | None = None,
    *,
    retrieval_hints: Sequence[str] = (),
) -> dict[str, Any]:
    """Response schema with one mandatory decision per retrieved candidate.

    Candidate article identifiers stay in the host-owned input order.  The model emits only
    a boolean and reason for each position, so it cannot silently skip a difficult candidate
    or attach a decision to an invented identifier.
    """
    hint_keys = set(map(str, retrieval_hints))
    keys = [
        *(key for key in catalog_keys(catalog or selectable_catalog()) if key not in hint_keys),
        NO_SUBSTANTIVE_OFFENSE,
    ]
    retrieval_hint_count = len(tuple(retrieval_hints))
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["question_domain", "candidate_decisions", "selected"],
        "properties": {
            "question_domain": {
                "type": "string",
                "enum": [SUBSTANTIVE_DOMAIN, NON_SUBSTANTIVE_DOMAIN],
            },
            "candidate_decisions": {
                "type": "array",
                "minItems": retrieval_hint_count,
                "maxItems": retrieval_hint_count,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["relevant", "reason"],
                    "properties": {
                        "relevant": {"type": "boolean"},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 160},
                    },
                },
            },
            "selected": {
                "type": "array",
                "minItems": 0,
                "maxItems": MAX_SELECTED,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["article", "reason"],
                    "properties": {
                        "article": {"type": "string", "enum": keys},
                        "reason": {"type": "string", "minLength": 1, "maxLength": 200},
                    },
                },
            }
        },
    }


def selection_payload(
    *,
    case_id: str,
    question_text: str,
    question_prompt: str,
    issue_hints: Sequence[Mapping[str, str]] = (),
    retrieval_hints: Sequence[str] = (),
    catalog: Iterable[Mapping[str, str]] | None = None,
) -> dict[str, Any]:
    """The request payload. Whitelisted fields only -- the catalog is a host asset.

    ``question_prompt`` is included on purpose. It scopes the selection to the sub-question
    being asked, which is the defect Phase 2 recorded as debt #3: a three-paragraph
    ``question_text`` whose sub-question asks about one paragraph had retrieval hauling in
    the other two paragraphs' articles. Selection can read the sub-question; ranking could
    not.
    """
    catalog_entries = tuple(catalog or selectable_catalog())
    catalog_by_key = {entry["key"]: entry for entry in catalog_entries}
    hint_keys = tuple(dict.fromkeys(map(str, retrieval_hints)))
    rendered_hints = []
    for key in hint_keys:
        entry = catalog_by_key.get(key)
        rendered_hints.append(
            f"{key} {entry['label']} {entry['offense']}" if entry else key
        )

    return {
        "case_id": case_id,
        "case_text": question_text,
        "question_prompt": question_prompt,
        "issue_hints": [
            {
                "label": str(hint.get("label", "")),
                "source_quote": str(hint.get("source_quote", "")),
            }
            for hint in issue_hints
            if hint.get("label")
        ],
        "retrieval_hints": rendered_hints,
        "article_catalog": catalog_lines(catalog_entries),
    }


def attempt_article_map(path: Path | None = None) -> dict[str, str]:
    """``art250 -> art254``: base offence to the article punishing its attempt.

    Only entries whose attempt article is itself in the corpus carry the field; the rest
    (문서죄 제235조, 특수상해 제258조의2 제4항) are outside it and would expand to nothing.
    """
    payload = yaml.safe_load((path or STAGE_PATH).read_text(encoding="utf-8")) or {}
    mapping: dict[str, str] = {}
    for entry in payload.get("attempt_punishable") or ():
        attempt = entry.get("attempt_article")
        if attempt:
            mapping[entry["offense"]] = attempt
    return mapping


def expand_attempt_articles(
    articles: Sequence[str], *, mapping: Mapping[str, str] | None = None
) -> tuple[str, ...]:
    """Append the attempt article of every selected base offence, order preserved."""
    mapping = attempt_article_map() if mapping is None else mapping
    selected = list(dict.fromkeys(articles))
    known = set(selected)
    for article in list(selected):
        attempt = mapping.get(article)
        if attempt and attempt not in known:
            selected.append(attempt)
            known.add(attempt)
    return tuple(selected)


def validate_selection(
    payload: Mapping[str, Any],
    *,
    catalog: Iterable[Mapping[str, str]] | None = None,
    retrieval_hints: Sequence[str] = (),
) -> tuple[tuple[str, ...], tuple[dict[str, str], ...]]:
    """Check a response and return ``(articles, entries)``.

    Duplicates are dropped rather than raised on: the same article named twice is a
    redundant response, not a contract violation, and the second reason is discarded so the
    audit record keeps one reason per article.
    """
    errors: list[str] = []
    keys = {*catalog_keys(catalog or selectable_catalog()), NO_SUBSTANTIVE_OFFENSE}
    domain = payload.get("question_domain")
    if domain not in {SUBSTANTIVE_DOMAIN, NON_SUBSTANTIVE_DOMAIN}:
        errors.append("question_domain is invalid")
    raw_decisions = payload.get("candidate_decisions")
    if not isinstance(raw_decisions, list):
        errors.append("candidate_decisions must be an array")
        raw_decisions = []
    elif len(raw_decisions) != len(retrieval_hints):
        errors.append(
            "candidate_decisions must contain exactly "
            f"{len(retrieval_hints)} entries"
        )

    reviewed: dict[str, dict[str, str]] = {}
    for index, item in enumerate(raw_decisions):
        where = f"candidate_decisions[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{where}: not an object")
            continue
        relevant = item.get("relevant")
        reason = item.get("reason")
        if not isinstance(relevant, bool):
            errors.append(f"{where}: relevant must be boolean")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where}: reason is required")
        if (
            relevant is True
            and isinstance(reason, str)
            and reason.strip()
            and index < len(retrieval_hints)
        ):
            article = str(retrieval_hints[index])
            if article not in keys or article == NO_SUBSTANTIVE_OFFENSE:
                errors.append(f"{where}: {article!r} is not a selectable article")
            else:
                reviewed.setdefault(
                    article, {"article": article, "reason": reason.strip()}
                )

    raw = payload.get("selected")
    if not isinstance(raw, list):
        errors.append("selected must be an array")
        raw = []

    seen: dict[str, dict[str, str]] = {}
    for index, item in enumerate(raw):
        where = f"selected[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{where}: not an object")
            continue
        article = item.get("article")
        reason = item.get("reason")
        if article not in keys:
            errors.append(f"{where}: {article!r} is not a catalog article")
            continue
        if article in set(map(str, retrieval_hints)):
            errors.append(f"{where}: retrieved candidates must be decided positionally")
            continue
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where}: reason is required")
            continue
        seen.setdefault(article, {"article": article, "reason": reason.strip()})

    if errors:
        raise ArticleSelectError(errors)
    if NO_SUBSTANTIVE_OFFENSE in seen:
        if len(seen) != 1:
            raise ArticleSelectError(
                ["no_substantive_offense cannot be combined with an article"]
            )
        if domain != NON_SUBSTANTIVE_DOMAIN:
            raise ArticleSelectError(
                ["no_substantive_offense requires non_substantive_question"]
            )
        # Domain routing owns the scope. Candidate decisions remain in the audit artifact,
        # but background offences cannot activate a substantive hierarchy after the model
        # has classified the actual question as procedural.
        return (), ()
    if domain == NON_SUBSTANTIVE_DOMAIN:
        raise ArticleSelectError(
            ["non_substantive_question requires no_substantive_offense"]
        )
    if domain != SUBSTANTIVE_DOMAIN:
        raise ArticleSelectError(["article selections require substantive_criminal_law"])
    for article, entry in reviewed.items():
        seen.setdefault(article, entry)
    if not seen:
        raise ArticleSelectError(
            ["substantive_criminal_law requires at least one accepted or selected article"]
        )
    entries = tuple(seen.values())
    return tuple(entry["article"] for entry in entries), entries
