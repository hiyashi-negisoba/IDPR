# External benchmark evaluation

This directory is the artifact root for the frozen v2 external evaluation harness.
It does not modify production routing, binding, grounding semantics, symbolic evaluation, or prompts.

## Benchmarks

- `lbox_call1`: `lbox/lbox_open`, `statute_classification_plus` → production Call 1.
- `kbl_call2`: `lbox/kbl`, `reasoning/kbl_causal_reasoning_qa_v0.1.json` → production
  `legal_element.result_causation` Call 2.

The source dataset size is never used as the reported evaluation N. Preparation first normalizes
and coverage-filters the external annotations against `data/v2/definitions`. The resulting
`manifest.json` records `source_N`, `normalizable_N`, `fully_covered_N`, exclusions by reason,
registry/catalog fingerprints, prompt hashes, and source-content hashes.

## Materialized contract

Each benchmark directory contains:

- `manifest.json`: pinned source, coverage, prompt, and registry lineage.
- `gold.jsonl`: scorer-only labels.
- `model_inputs.jsonl`: exact production-compatible model inputs with gold removed.
- `excluded.jsonl`: every source item excluded before model execution and its reason.

LBOX includes a case only when every gold statute resolves uniquely to a directly authored
`OffenseDef.identity.statutory_refs`. Shared provisions are disambiguated only when the source
`casename` identifies exactly one authored offense; otherwise the case is excluded. Derived
offenses are never guessed from statute labels.

KBL converts the selected A/B option by option meaning rather than by fixed letter position:
`인과관계있음` → `TRUE`, `인과관계없음` → `FALSE`. The external instance key exists only to satisfy
the production typed Call 2 boundary; it is not added to the registry and is never passed to the
symbolic runtime. The assessed predicate itself is the authored
`legal_element.result_causation` definition.

## Execution

The SLURM entrypoint performs preparation before starting vLLM, then runs both benchmarks against
one job-local server:

```bash
IDPR_EXTERNAL_MODEL_SNAPSHOT=/path/to/model \
sbatch scripts/slurm/run_v2_external_benchmarks.sh
```

`IDPR_EXTERNAL_BENCHMARK` may be `all`, `lbox_call1`, or `kbl_call2`. The default is `all`.
`IDPR_EXTERNAL_SERVED_MODEL` and `IDPR_EXTERNAL_REASONING_PARSER` are execution-only settings.
If local benchmark files are preferred, set `IDPR_EXTERNAL_LBOX_SOURCE_DIR` to a directory
containing `train.jsonl`, `valid.jsonl`, and `test.jsonl`, and/or set `IDPR_EXTERNAL_KBL_SOURCE`
to the causal-reasoning JSON file. Without local paths, the prepare step downloads the pinned raw
JSON/JSONL files directly from Hugging Face with the Python standard library and caches them under
the run materialization root.

The job runs `tests/test_v2_external_benchmarks.py` before downloading data unless
`IDPR_EXTERNAL_SKIP_TESTS=1`. At completion it prints the exact scoring commands. Scoring rejects
failed model calls, gold/prediction ID mismatch, prediction/materialization lineage mismatch, and
any drift in the materialized gold or prediction artifacts.
