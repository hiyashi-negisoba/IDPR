# IDPR

IDPR is a Neural–Symbolic–Neural pipeline for source-grounded, long-form Korean
criminal-law reasoning.

```text
case text
  → neural fact graph and candidate scope
  → issue-level three-valued assessment
  → Scallop symbolic composition
  → constrained offence-level IRAC answer
```

The active rulebase contains 1,848 source-grounded cards organized under 383 legal
issues across 51 Criminal Act articles. General rules are loaded as issue anchors;
case-specific standards and precedents remain searchable details instead of becoming
independent constituent elements.

## Repository layout

- `src/idpr/neural/`: generic fact, article, and issue assessment contracts
- `src/idpr/rulebase/`: card/issue catalogs and Scallop compilation/runtime
- `src/idpr/issue_pipeline.py`: generic symbolic stage boundaries
- `src/idpr/generation/issue_answer.py`: constrained IRAC realization
- `scripts/run_issue_assessment.py`: one-case issue assessment and symbolic execution
- `scripts/run_issue_answer.py`: one-case IRAC realization
- `scripts/run_issue_pipeline_batch.py`: resumable dataset runner
- `src/idpr/legacy/`: archived fraud-pilot implementations kept for reproduction only
- `scripts/diagnostics/`: fixed diagnostic and historical comparison runners

No active pipeline module imports the legacy pilot packages.

## Development

Python 3.11 or later is required.

```bash
uv sync
uv run pytest
```

The pinned Scallop runtime is installed separately:

```bash
bash scripts/install_scallop_runtime.sh
```

Raw benchmark and commentary sources are not committed. Copy `.env.example` to `.env`
and configure local paths as needed. In particular, rubric-based evaluation requires
`IDPR_KCL_PARQUET` when the source path recorded in the inventory is unavailable.

## Validate the full stage boundary without a model

```bash
python scripts/refresh_l0_issue_catalog.py
python scripts/run_issue_pipeline_batch.py --plan-only
```

The refresh command does not rerun retrieval or change candidate articles. It only
rebuilds fields deterministically derived from the current issue catalog and refuses to
write if the article boundary has changed.

## Run inference

Start an OpenAI-compatible model server, then run one case:

```bash
python scripts/run_issue_assessment.py \
  --base-url http://127.0.0.1:8000 \
  --model MODEL_NAME \
  --case-id CASE_ID \
  --out experiments/results/idpr_nsn/CASE_ID/issue_assessment.json

python scripts/run_issue_answer.py \
  --base-url http://127.0.0.1:8000 \
  --model MODEL_NAME \
  --call2 experiments/results/idpr_nsn/CASE_ID/issue_assessment.json \
  --out experiments/results/idpr_nsn/CASE_ID/answer.json
```

For a resumable inventory sweep:

```bash
python scripts/run_issue_pipeline_batch.py \
  --base-url http://127.0.0.1:8000 \
  --model MODEL_NAME
```

On Slurm, `scripts/slurm/run_issue_pipeline_batch.sh` requests one PRO6000 GPU, two
CPUs, 32 GB RAM, and 48 hours. Cluster-specific paths are supplied through the
`IDPR_*` environment variables documented in `.env.example`; none are embedded in the
production runner.

Generated model outputs and caches are ignored by Git. Reviewed rulebase, candidate,
schema, and evaluation-definition assets remain versioned.
