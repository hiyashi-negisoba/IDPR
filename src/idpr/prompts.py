"""Prompt registry.

Every prompt sent to a model is loaded through here rather than by an ad-hoc
``read_text`` at the call site. Two reasons, both operational:

* prompts are experiment conditions in this project and carry a user approval gate, so
  there has to be one list of what exists and one place that reads it;
* a missing prompt must fail at load with the name it was asked for, not with a bare
  ``FileNotFoundError`` deep inside a runner that has already started a GPU job.

The registry does not template. ``render_user`` substitutes exactly one placeholder,
``{{INPUT_JSON}}``, because that is the convention the approved fraud prompts already use
and a second mechanism would be a second thing to audit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

PROMPT_ROOT = Path(__file__).resolve().parents[2] / "prompts"

#: Placeholder in ``*_user.md`` prompts. Single, literal, and not a format spec -- case
#: text contains braces often enough that ``str.format`` would raise on real input.
INPUT_PLACEHOLDER = "{{INPUT_JSON}}"


class PromptError(KeyError):
    """Raised when a prompt name has no file, or a user prompt lacks its placeholder."""


def prompt_path(name: str) -> Path:
    return PROMPT_ROOT / f"{name}.md"


def load_prompt(name: str) -> str:
    path = prompt_path(name)
    if not path.is_file():
        available = sorted(p.stem for p in PROMPT_ROOT.glob("*.md"))
        raise PromptError(f"no prompt named {name!r}; available: {available}")
    return path.read_text(encoding="utf-8")


def render_user(name: str, payload: Mapping[str, Any]) -> str:
    """Load a user prompt and substitute the input payload.

    ``ensure_ascii=False`` matters: the payload is Korean case text, and escaping it to
    ``\\uXXXX`` would triple the token count of the largest field in the request.
    """
    template = load_prompt(name)
    if INPUT_PLACEHOLDER not in template:
        raise PromptError(f"user prompt {name!r} has no {INPUT_PLACEHOLDER} placeholder")
    return template.replace(
        INPUT_PLACEHOLDER, json.dumps(payload, ensure_ascii=False, indent=2)
    )
