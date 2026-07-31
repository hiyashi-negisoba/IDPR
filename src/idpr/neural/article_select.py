"""Call 1.5: which articles does this case put in issue?

Replaces similarity retrieval in the article decision. The reason is the corpus size: it
covers 51 articles, so handing the model *all* of them costs 575 tokens and lifts the
recall ceiling from retrieval's measured 0.848 to 1.0. Picking 18 of 51 was a 35% filter
paid for with a dense encoder, a BM25 index and a cross-encoder -- and, more to the point,
none of those three learned the relation the task actually needs.

That relation is not similarity. "가슴과 음부를 스스로 만지게 하였다" and the card's
"피해자를 도구로 삼아 …추행행위를 한 경우" share no terms and are not near each other in
any general-purpose embedding space; what connects them is that the first *instantiates*
the second. Nothing in the retrieval stack was trained on that mapping and there is no
corpus here to train it on. A model that read Korean criminal law in pretraining already
has it. All it lacks is the article-number vocabulary, and the catalog supplies exactly
that.

Two things the host keeps, both for the same reason -- the model must not mint identifiers:

* ``article`` is a JSON-schema enum over the 51 catalog keys, so guided decoding makes an
  invented article number ungrammatical. Call 1 measured the alternative: asked to recall
  article numbers from memory it matched 0 of 258 issue candidates. Selection from a
  presented list is a different task, and that 0.000 is not evidence against it.
* attempt articles (제254·300·342조) are appended deterministically from ``stage.yaml``.
  Their statute text is "제329조 내지 제341조의 미수범은 처벌한다" and nothing else, so
  they share no vocabulary with any fact pattern and are unreachable by similarity *and*
  by the model. The statute states the reference; expanding it is not reverse-engineering
  the gold.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from idpr.rulebase.doctrine import CATALOG_PATH, STAGE_PATH

#: Bumped when the request contract changes in a way that invalidates cached outputs.
SCHEMA_VERSION = "1.0.0"

#: Upper bound on selected articles. Not a target -- the prompt asks for recall, and the
#: cost of a spare article is card statuses, not a wrong answer. It exists only so a
#: degenerate response cannot select the whole corpus and silently undo the step.
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


def catalog_lines(catalog: Iterable[Mapping[str, str]] | None = None) -> list[str]:
    """``art298 제298조 강제추행`` -- one line per article, key first.

    The key leads because the key is what the model must emit. Putting the human-readable
    label first would invite it to answer with the label.
    """
    return [
        f"{entry['key']} {entry['label']} {entry['offense']}"
        for entry in (catalog or load_catalog())
    ]


def article_select_schema(catalog: Iterable[Mapping[str, str]] | None = None) -> dict[str, Any]:
    """Response schema. ``article`` is an enum, so the article set is closed by decoding."""
    keys = list(catalog_keys(catalog))
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["selected"],
        "properties": {
            "selected": {
                "type": "array",
                "minItems": 1,
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
    catalog: Iterable[Mapping[str, str]] | None = None,
) -> dict[str, Any]:
    """The request payload. Whitelisted fields only -- the catalog is a host asset.

    ``question_prompt`` is included on purpose. It scopes the selection to the sub-question
    being asked, which is the defect Phase 2 recorded as debt #3: a three-paragraph
    ``question_text`` whose sub-question asks about one paragraph had retrieval hauling in
    the other two paragraphs' articles. Selection can read the sub-question; ranking could
    not.
    """
    return {
        "case_id": case_id,
        "case_text": question_text,
        "question_prompt": question_prompt,
        "article_catalog": catalog_lines(catalog),
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
    payload: Mapping[str, Any], *, catalog: Iterable[Mapping[str, str]] | None = None
) -> tuple[tuple[str, ...], tuple[dict[str, str], ...]]:
    """Check a response and return ``(articles, entries)``.

    Duplicates are dropped rather than raised on: the same article named twice is a
    redundant response, not a contract violation, and the second reason is discarded so the
    audit record keeps one reason per article.
    """
    errors: list[str] = []
    keys = set(catalog_keys(catalog))
    raw = payload.get("selected")
    if not isinstance(raw, list) or not raw:
        raise ArticleSelectError(["selected must be a non-empty array"])

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
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where}: reason is required")
            continue
        seen.setdefault(article, {"article": article, "reason": reason.strip()})

    if errors:
        raise ArticleSelectError(errors)
    entries = tuple(seen.values())
    return tuple(entry["article"] for entry in entries), entries
