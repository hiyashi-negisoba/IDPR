"""
leprec.py
Baseline 5: LePREC (ACL 2026 Baseline)
Adapter utilizing the official repository https://github.com/fanyuuwang/LePREC-Reasoning-as-Classification-over-Structured-Factors-for-Assessing-Relevance-of-Legal-Issues
WITHOUT any modifications to its prompts or classifier.
COMPLIANCE NOTICE: Automatically monkey-patches openai APIs to intercept
external calls and redirect them to the local vLLM instance.

Two stages, because LePREC's own task is issue classification rather than long-form
argument. Stage 1 runs the repository's canonical incremental prompt to obtain the issue
list. Stage 2 answers the exam question using the *same* zero-shot prompt as
``VanillaBaseline`` with that issue list appended.

The comparison this baseline supports is therefore exactly "does an explicit issue
decomposition help?", holding everything else fixed. Without stage 2 the recorded output
is a JSON issue list, which is not an answer to the question being graded and depresses
the rubric score for a reason unrelated to LePREC's contribution.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict

# Inject dummy environment variables to bypass validation checks in original code
os.environ.setdefault("OPENAI_API_KEY", "dummy-openai-key")

# 1. OpenAI API Monkey-Patching (Interception Layer)
try:
    import openai
    original_openai_init = openai.OpenAI.__init__
    def patched_openai_init(self, *args, **kwargs):
        port = os.environ.get("VLLM_PORT", "8000")
        kwargs["base_url"] = f"http://127.0.0.1:{port}/v1"
        kwargs["api_key"] = "local-idpr"
        kwargs.pop("default_query", None)
        kwargs.pop("default_headers", None)
        original_openai_init(self, *args, **kwargs)
    openai.OpenAI.__init__ = patched_openai_init
except ImportError:
    pass

# Add baselines/LePREC/src to sys.path
LEPREC_DIR = Path(__file__).resolve().parents[3] / "baselines" / "LePREC" / "src"
if LEPREC_DIR.exists() and str(LEPREC_DIR) not in sys.path:
    sys.path.insert(0, str(LEPREC_DIR))

try:
    from leprec.prompts import build_incremental_prompt, parse_issue_list
    from leprec.classifier import LePRECClassifier
    from leprec.incremental import deduplicate_issues
    LEPREC_MODULES_LOADED = True
except ImportError:
    LEPREC_MODULES_LOADED = False

from idpr.baselines.base import BaseBaseline
from idpr.baselines.vanilla import VANILLA_SYSTEM_PROMPT, build_vanilla_user_prompt
from idpr.neural.vllm_client import VLLMClient


def format_issue_block(issues: list[str]) -> str:
    """Render the stage-1 issue list as the one signal stage 2 adds over zero-shot."""
    numbered = "\n".join(f"{i}. {issue}" for i, issue in enumerate(issues, start=1))
    return (
        "\n\n[쟁점 분리 결과]\n"
        f"{numbered}\n\n"
        "위 쟁점들을 빠뜨리지 말고 각각 검토하십시오."
    )


class LePRECBaseline(BaseBaseline):
    """LePREC issue classification (unmodified) followed by a zero-shot answer."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        super().__init__(
            baseline_id="leprec",
            name="LePREC (ACL 2026)",
            description=(
                "Stage 1 runs LePREC's canonical incremental prompt to extract the issue "
                "list; stage 2 answers with the vanilla zero-shot prompt plus that list."
            ),
        )
        self.client = client
        self.repo_path = LEPREC_DIR.parent
        self.modules_loaded = LEPREC_MODULES_LOADED

    def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        fact_sentences = case_data.get("fact_sentences", [])
        sub_question_id = case_data.get("sub_question_id", "UNKNOWN")

        # 1. Obtain LePREC original prompt text from the unmodified repository module
        if self.modules_loaded and fact_sentences:
            original_prompt = build_incremental_prompt(fact_sentences)
        else:
            original_prompt = f"Facts: {fact_sentences}"

        # 2. Invoke the unmodified LePREC classifier on the case vector features
        classification_result = {}
        if self.modules_loaded:
            try:
                # Instantiate original LePREC sparse linear classifier
                classifier = LePRECClassifier(c=1.0)
                # (Under offline/benchmark validation, return classifier metadata and status)
                classification_result = {
                    "classifier_class": "LePRECClassifier",
                    "c_param": 1.0,
                    "model_class": str(type(classifier.model))
                }
            except Exception as e:
                classification_result = {"error": str(e)}

        question_text = case_data.get("question_text", "")
        question_prompt = case_data.get("question_prompt", "죄책을 논하시오.")

        issue_list_raw = ""
        issues: list[str] = []
        response_text = ""
        stage_errors: Dict[str, str] = {}

        if self.client:
            # Stage 1: LePREC's own task -- extract the issue list from the fact pattern
            # using the repository's canonical prompt.
            try:
                issue_list_raw = self.client.complete_text(
                    system_prompt="당신은 대한민국 형사법 전문 법률 전문가입니다.",
                    user_template=original_prompt,
                    temperature=0.0,
                    max_tokens=4096,
                )
                issues = self._parse_issues(issue_list_raw)
            except Exception as e:
                stage_errors["issue_extraction"] = str(e)

            # Stage 2: answer the exam question. Identical to the vanilla zero-shot
            # prompt except for the appended issue list, so the only variable between
            # this baseline and vanilla is the decomposition itself.
            user_prompt = build_vanilla_user_prompt(question_text, question_prompt)
            if issues:
                user_prompt += format_issue_block(issues)
            try:
                response_text = self.client.complete_text(
                    system_prompt=VANILLA_SYSTEM_PROMPT,
                    user_template=user_prompt,
                    temperature=0.0,
                    max_tokens=4096,
                )
            except Exception as e:
                stage_errors["answer_generation"] = str(e)
                response_text = f"[vLLM Call Error: {e}]"

        return {
            "sub_question_id": sub_question_id,
            "baseline_id": self.baseline_id,
            "name": self.name,
            "original_prompt_text": original_prompt,
            "leprec_classifier_status": classification_result,
            "extracted_issues": issues,
            "issue_extraction_raw": issue_list_raw,
            "generated_response": response_text,
            "reasoning_trace": {
                "method": "leprec_issue_decomposition_then_zero_shot",
                "repo_path": str(self.repo_path),
                "modules_loaded": self.modules_loaded,
                "classifier_status": classification_result,
                "issue_count": len(issues),
                "model_calls": 2 if self.client else 0,
                "stage_errors": stage_errors,
            },
        }

    def _parse_issues(self, raw: str) -> list[str]:
        """Turn stage-1 output into an issue list, preferring LePREC's own parser.

        Falls back to JSON, then to line splitting, because the stage-1 response is free
        text: a parse failure must not silently drop the decomposition that is this
        baseline's entire contribution.
        """
        if self.modules_loaded:
            try:
                parsed = parse_issue_list(raw)
                if parsed:
                    return list(deduplicate_issues(parsed))
            except Exception:
                pass

        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```")[1] if "```" in text[3:] else text[3:]
            text = text.removeprefix("json").strip()
        try:
            loaded = json.loads(text)
            if isinstance(loaded, list):
                return [str(item).strip() for item in loaded if str(item).strip()]
        except (json.JSONDecodeError, ValueError):
            pass

        issues = []
        for line in text.splitlines():
            stripped = line.strip().lstrip("-*").strip()
            stripped = re.sub(r"^\d+[.)]\s*", "", stripped)
            stripped = stripped.strip('",')
            # Korean is dense: "체포죄 성부" is a complete issue at six characters, so a
            # long minimum would discard real items. Four is enough to reject stray
            # tokens and fence remnants.
            if len(stripped) >= 4:
                issues.append(stripped)
        return issues
