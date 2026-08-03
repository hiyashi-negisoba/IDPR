"""Generate a labeled lightweight direct answer for non-special-part diagnostic cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.eval.input_formatter import scoped_question_text
from idpr.eval.issue_recall import INVENTORY_PATH
from idpr.neural.vllm_client import VLLMClient


SYSTEM_PROMPT = (
    "당신은 대한민국 형사법 사례형 시험 답안을 작성한다. 설문이 요구하는 핵심 쟁점만 선별하여 "
    "관련 법리, 사실 적용, 결론을 짧고 일관되게 작성하라. 존재하지 않는 조문이나 판례를 만들지 말라."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    args = parser.parse_args()
    rows = {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in args.inventory.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    case = rows[args.case_id]
    prompt = str(case.get("question_prompt", ""))
    text = scoped_question_text(str(case.get("question_text", "")), prompt)
    user_prompt = f"[사실관계]\n{text}\n\n[설문]\n{prompt}"
    client = VLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=args.timeout_seconds,
    )
    answer = client.complete_text(
        system_prompt=SYSTEM_PROMPT,
        user_template=user_prompt,
        max_tokens=args.max_tokens,
        temperature=0.0,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(answer.strip() + "\n", encoding="utf-8")
    temporary.replace(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
