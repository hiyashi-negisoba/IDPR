# SKI-ML rulegen API integration

## Current decision

The pilot uses LiteLLM Chat Completions through the lab Gateway with model names
prefixed by `openai/`. Terra performs extraction and bounded revision; Sol performs
advisory critique. The local process owns schema validation, provenance checks,
adjudication, caching, and usage manifests.

Environment variables are documented in `.env.example`. The real `.env` is ignored by
Git and should remain mode `600`. The client never serializes the API key, hidden model
reasoning, or request headers into cache artifacts.

## Official API findings

- OpenAI recommends the Responses API for new reasoning workflows, but Chat Completions
  remains supported. The lab Gateway OpenAPI also exposes Chat Completions and an
  OpenAI-compatible Responses route. The current pilot keeps Chat until the same JSON
  contracts and usage accounting pass through the Gateway Responses route.
- Reasoning tokens and visible output share `max_completion_tokens`. Sol therefore uses
  `reasoning_effort=low` and a bounded 25,000-token ceiling. Actual pilot outputs used far
  less than that ceiling.
- GPT-5-family requests omit `temperature`; the first test confirmed that forcing `0.0`
  is rejected by this Gateway/model combination.
- `merge_reasoning_content_in_choices=false` is correct for this pipeline. Hidden reasoning
  is never parsed as final JSON or stored as a substitute for an empty answer.
- Native Structured Outputs are desirable, but the current compatibility path supplies the
  exact schema in the prompt and runs `jsonschema` plus semantic provenance validation
  locally. `IDPR_LLM_JSON_RESPONSE_FORMAT` remains off until Gateway-native schema mode is
  tested end to end.
- LiteLLM asynchronous calls are concurrent online requests, not OpenAI Batch API jobs.
  Batch is a separate JSONL workflow with delayed completion and discounted official
  pricing. It should be added only after one-batch quality is stable.

Official references:

- [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)
- [Responses migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Batch API guide](https://developers.openai.com/api/docs/guides/batch)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [LiteLLM Responses API](https://docs.litellm.ai/docs/response_api)
- [LiteLLM JSON mode](https://docs.litellm.ai/docs/completion/json_mode)
- [LiteLLM reasoning content](https://docs.litellm.ai/docs/reasoning_content)

## Pilot evidence

The successful first extraction produced 21 candidates. After source-bounded criticism,
adjudication, polarity separation, and minimal patching, the tracked exemplar contains 62
candidates and 8 unresolved questions. Every candidate quote is an exact substring of its
declared commentary chunk.

Across the cached Terra/Sol pilot responses available on 2026-07-16, response-ID
deduplication found 7 Terra and 10 Sol responses:

| role | prompt tokens | completion tokens | reasoning tokens | total tokens |
|---|---:|---:|---:|---:|
| Terra | 116,037 | 56,432 | 1,127 | 172,469 |
| Sol | 161,661 | 18,717 | 4,684 | 180,378 |

At OpenAI's published standard list rates for these models, this is approximately $2.51.
The lab Gateway's actual budget accounting may differ, so its usage dashboard remains the
billing authority.

## Retry and stopping policy

The default retry count is zero. A deterministic 400 response must be fixed, not repeated.
Transient retry policy can be added later for 429 and 5xx responses only.

Correction does not continue until Sol returns zero findings. Findings are adjudicated
against the bounded source. Unsupported opposing views and enumerated case illustrations
remain unresolved questions or RAG context. Accepted changes use a validated minimal patch;
legal verification still requires human review and primary precedent comparison.
