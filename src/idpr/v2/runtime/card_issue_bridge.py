"""Instance-scoped bridge from v2 offenses to the reviewed card issue hierarchy.

Cards do not become legal conclusions merely because their article matches an offense.
This module performs only two host-safe operations:

* project an offense with an *authored* statutory identity to Criminal Act article keys;
* restrict the reviewed issue hierarchy to those articles and rank issue candidates with
  the already-existing retrieval layer using one factual episode as the query.

Derived offenses without their own identity are deliberately left unmapped.  Following a
base offense would silently turn, for example, a special or combined offense into the
base article and is therefore legal authoring rather than identity normalization.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from idpr.retrieval import (
    LexicalIndex,
    retrieve_candidate_issues_from_cards,
    retrieve_issue_cards,
)
from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.issue_catalog_v2 import IssuePacket, compile_issue_catalog_v2
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey

EXACT_AUTHORED_IDENTITY = "EXACT_AUTHORED_IDENTITY"
UNMAPPED_DERIVED_ARTICLE = "UNMAPPED_DERIVED_ARTICLE"
UNMAPPED_OFFENSE_ARTICLE = "UNMAPPED_OFFENSE_ARTICLE"

_CRIMINAL_ACT_ARTICLE = re.compile(r"^형법\s+제0*(\d+)조(?:의0*(\d+))?")


def criminal_act_article_key(statutory_ref: str) -> str | None:
    """Normalize an authored Criminal Act citation to the card corpus article key."""
    match = _CRIMINAL_ACT_ARTICLE.match(statutory_ref.strip())
    if match is None:
        return None
    base, sub = match.groups()
    return f"art{int(base)}" if sub is None else f"art{int(base)}{int(sub)}_{int(sub)}"


@dataclass(frozen=True, slots=True)
class OffenseArticleProjection:
    offense_ref: str
    status: str
    article_keys: tuple[str, ...]
    statutory_refs: tuple[str, ...]


def project_offense_articles(
    registry: DefinitionRegistry, offense_ref: str
) -> OffenseArticleProjection:
    """Project only an explicitly authored offense identity; never infer derived law."""
    entry = registry.get(offense_ref)
    if entry is None or entry.kind not in {"offense", "derived_offense"}:
        raise ValueError(f"unknown offense definition: {offense_ref!r}")
    identity = entry.payload.get("identity")
    if not isinstance(identity, Mapping):
        status = (
            UNMAPPED_DERIVED_ARTICLE
            if entry.kind == "derived_offense"
            else UNMAPPED_OFFENSE_ARTICLE
        )
        return OffenseArticleProjection(offense_ref, status, (), ())
    raw_refs = identity.get("statutory_refs")
    if not isinstance(raw_refs, Sequence) or isinstance(raw_refs, (str, bytes)):
        return OffenseArticleProjection(
            offense_ref, UNMAPPED_OFFENSE_ARTICLE, (), ()
        )
    statutory_refs = tuple(value for value in raw_refs if isinstance(value, str))
    article_keys = tuple(
        dict.fromkeys(
            key
            for value in statutory_refs
            if (key := criminal_act_article_key(value)) is not None
        )
    )
    return OffenseArticleProjection(
        offense_ref,
        EXACT_AUTHORED_IDENTITY if article_keys else UNMAPPED_OFFENSE_ARTICLE,
        article_keys,
        statutory_refs,
    )


#: 죄명에서 갈래를 가리키는 어간만 남긴다. "횡령죄" -> "횡령".
_OFFENSE_SUFFIX = re.compile(r"죄$")


def _offense_stem(registry: DefinitionRegistry, offense_ref: str) -> str:
    entry = registry.get(offense_ref)
    identity = entry.payload.get("identity") if entry is not None else None
    name = identity.get("name") if isinstance(identity, Mapping) else None
    return _OFFENSE_SUFFIX.sub("", str(name)) if name else ""


def paragraph_sibling_stems(
    registry: DefinitionRegistry, offense_ref: str
) -> tuple[str, ...]:
    """같은 조문을 쓰지만 **다른 항**에 있는 죄의 이름 어간.

    카드 코퍼스의 장(章)은 주석서를 그대로 따라와서 제355조가 "횡령·배임" 하나로 묶여 있다.
    조문 키(`art355`)만으로 issue family를 잡으면 횡령죄 논증에 배임죄 판시가 붙는다 --
    26문항 payload에서 실제로 그랬다. 항이 다르면 다른 죄이므로, 그 죄의 이름을 여기서
    돌려주고 회수 범위에서 뺀다.

    항 정보가 없어 두 죄의 `statutory_refs`가 완전히 같으면 형제로 보지 않는다. 그런
    조문에서는 갈래를 나눌 근거가 저작에 없고, 억지로 나누면 공통 판시까지 잃는다.
    """
    projection = project_offense_articles(registry, offense_ref)
    if not projection.article_keys:
        return ()
    own_refs = set(projection.statutory_refs)
    own_stem = _offense_stem(registry, offense_ref)
    stems: list[str] = []
    for entry in registry.by_id.values():
        if entry.id == offense_ref or entry.kind not in {"offense", "derived_offense"}:
            continue
        try:
            sibling = project_offense_articles(registry, entry.id)
        except ValueError:
            continue
        if not set(sibling.article_keys) & set(projection.article_keys):
            continue
        if set(sibling.statutory_refs) & own_refs:
            continue
        stem = _offense_stem(registry, entry.id)
        if stem and stem != own_stem and stem not in own_stem and own_stem not in stem:
            stems.append(stem)
    return tuple(dict.fromkeys(stems))


def names_other_paragraph(text: str, own_stem: str, sibling_stems: Sequence[str]) -> bool:
    """이 문장이 형제 죄만 이름으로 부르고 이 죄는 부르지 않는가."""
    if own_stem and own_stem in text:
        return False
    return any(stem in text for stem in sibling_stems)


@dataclass(frozen=True, slots=True)
class InstanceIssueCandidate:
    instance: OffenseInstanceKey
    issue_id: str
    article: str
    function: str
    runtime: str
    score: float
    anchor_card_ids: tuple[str, ...]
    retrieval_card_ids: tuple[str, ...]
    selected_detail_card_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InstanceIssuePlan:
    instance: OffenseInstanceKey
    projection: OffenseArticleProjection
    episode_query: str
    candidates: tuple[InstanceIssueCandidate, ...]


def plan_instance_issue_candidates(
    registry: DefinitionRegistry,
    instance: OffenseInstanceKey,
    *,
    episode_quotes: Iterable[str],
    corpus: CardCorpus | None = None,
    issues: Sequence[IssuePacket] | None = None,
    top_k_issues: int = 3,
    top_k_detail_cards: int = 2,
    detail_lexical: LexicalIndex | None = None,
) -> InstanceIssuePlan:
    """Rank reviewed issues inside the instance's exact authored article scope.

    Retrieval is a candidate producer only.  The result contains no issue truth, card
    truth, doctrine activation, completion state, or concurrence effect.
    """
    if top_k_issues < 1:
        raise ValueError("top_k_issues must be at least 1")
    if top_k_detail_cards < 1:
        raise ValueError("top_k_detail_cards must be at least 1")
    projection = project_offense_articles(registry, instance.offense_ref)
    episode_quotes = tuple(episode_quotes)
    query = " ".join(
        dict.fromkeys(value.strip() for value in episode_quotes if value.strip())
    )
    if not query or not projection.article_keys:
        return InstanceIssuePlan(instance, projection, query, ())

    corpus = corpus or card_corpus()
    if issues is None:
        issues = compile_issue_catalog_v2(corpus)[0]
    scoped = tuple(issue for issue in issues if issue.article in projection.article_keys)
    if not scoped:
        return InstanceIssuePlan(instance, projection, query, ())
    result = retrieve_candidate_issues_from_cards(
        (query,),
        corpus=corpus,
        issues=scoped,
        top_k_issues=min(top_k_issues, len(scoped)),
    )
    issue_by_id = {issue.issue_id: issue for issue in scoped}
    selected_issues = tuple(issue_by_id[value] for value in result.retrieved_issue_ids)
    detail_result = retrieve_issue_cards(
        selected_issues,
        tuple({"assertion": {"source_quote": value}} for value in episode_quotes),
        corpus=corpus,
        top_k_per_issue=top_k_detail_cards,
        lexical=detail_lexical,
    )
    details_by_issue = detail_result.by_issue
    candidates = tuple(
        InstanceIssueCandidate(
            instance=instance,
            issue_id=issue_id,
            article=issue_by_id[issue_id].article,
            function=issue_by_id[issue_id].function,
            runtime=issue_by_id[issue_id].runtime,
            score=result.issue_scores[issue_id],
            anchor_card_ids=issue_by_id[issue_id].anchor_card_ids,
            retrieval_card_ids=issue_by_id[issue_id].retrieval_card_ids,
            selected_detail_card_ids=details_by_issue[issue_id].card_ids,
        )
        for issue_id in result.retrieved_issue_ids
    )
    return InstanceIssuePlan(instance, projection, query, candidates)


__all__ = [
    "EXACT_AUTHORED_IDENTITY",
    "UNMAPPED_DERIVED_ARTICLE",
    "UNMAPPED_OFFENSE_ARTICLE",
    "InstanceIssueCandidate",
    "InstanceIssuePlan",
    "OffenseArticleProjection",
    "criminal_act_article_key",
    "plan_instance_issue_candidates",
    "project_offense_articles",
]
