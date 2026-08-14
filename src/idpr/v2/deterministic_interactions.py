"""Conservative exact-text recovery for explicit coordination formulae."""

from __future__ import annotations

import re
from collections.abc import Sequence


def explicit_conspiracy_interactions(
    *,
    episode_source_quotes: Sequence[str],
    episode_participant_ids: Sequence[str],
    responsibility_actor_ids: Sequence[str],
) -> list[dict[str, object]]:
    """Recover only the literal Korean ``X ... Y와 공모하여 ...`` construction.

    This is factual coordination, not a legal 공동정범 conclusion.  The function is
    intentionally narrow and returns the exact clause; every other interaction remains
    the model contract's responsibility.
    """
    participants = set(episode_participant_ids)
    responsibility = set(responsibility_actor_ids)
    output: list[dict[str, object]] = []
    for text in episode_source_quotes:
        for marker in re.finditer(r"([甲乙丙丁戊己庚辛壬癸])(?:과|와)\s*공모하여", text):
            counterpart = marker.group(1)
            if counterpart not in participants:
                continue
            prefix = text[: marker.start()]
            sources = [
                (prefix.rfind(actor), actor)
                for actor in responsibility
                if actor != counterpart and prefix.rfind(actor) >= 0
            ]
            if not sources:
                continue
            start, source = max(sources)
            end_match = re.search(r"(?:마음먹었다|하였다|했다)\.", text[marker.end() :])
            end = (
                marker.end() + end_match.end()
                if end_match is not None
                else len(text)
            )
            quote = text[start:end].strip()
            output.append(
                {
                    "interaction_type": "agreement_or_coordinated_conduct",
                    "source_actor_id": source,
                    "target_actor_ids": [counterpart],
                    "evidence_quotes": [quote],
                }
            )
        for agreement in re.finditer(
            r"([甲乙丙丁戊己庚辛壬癸])(?:과|와)\s*"
            r"([甲乙丙丁戊己庚辛壬癸])(?:은|는)\s*([^.!?]{1,40}?하기로)",
            text,
        ):
            source, counterpart = agreement.group(1), agreement.group(2)
            if (
                source not in responsibility
                or counterpart not in responsibility
                or source not in participants
                or counterpart not in participants
            ):
                continue
            output.append(
                {
                    "interaction_type": "agreement_or_coordinated_conduct",
                    "source_actor_id": source,
                    "target_actor_ids": [counterpart],
                    "evidence_quotes": [agreement.group(0)],
                }
            )
    return output


__all__ = ["explicit_conspiracy_interactions"]
