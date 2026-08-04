# IDPR

IDPR's active path is a lean Neural–Symbolic–Neural pipeline for source-grounded
Korean criminal-law reasoning.

```text
case and question
  → closed RuleIR unit and actor/action selection
  → direct assessment of every predicate and role in each selected unit
  → execution of the selected unit's committed Scallop program
  → one short law/application section per issue
  → host-owned heading, conclusion, and asset hashes
```

The runtime registry contains 36 executable RuleIR units and 1,652 input predicates.
The model cannot invent a unit, omit predicates from a selected unit, substitute a
generic FactGraph, or write the symbolic conclusion. An issue outside the registry is
reported as `predicate_ir_missing`; it is never sent through a model-only fallback.

This is a recovered execution path, not a finished proof-producing system. It currently
reduces public Scallop query relations to booleans and does not emit a case-specific proof
tree or fired RuleIR rules. Read [`docs/handoff/CURRENT.md`](docs/handoff/CURRENT.md)
before changing the pipeline.

## Active implementation

- `src/idpr/rulegen/registry.py`: manifest-driven allowlist and asset audit
- `src/idpr/rulegen/native_host.py`: closed selection, full assessment validation,
  committed Scallop execution, and dependency bridges
- `src/idpr/generation/native_rule_ir_answer.py`: section writer contract and
  host-owned conclusion/provenance assembly
- `scripts/run_rule_ir_native_lean.py`: the only lean one-case entry point
- `scripts/audit_rule_ir_native_prompts.py`: three-stage prompt and schema gate
- `scripts/slurm/run_rule_ir_native_lean_smoke.sh`: job-local Gemma/vLLM smoke
- `data/rulegen/rule_ir_registry_manifest.json`: executable unit allowlist
- `docs/README.md`: documentation map and authority levels
- `docs/handoff/CURRENT.md`: known defects and required repair order

The older issue-search, generic FactGraph, core-projection, and batch runners remain in
the repository only as research history and comparison code. They are not imported by
the active entry point.

## Validate

Python 3.11 or later and the pinned Scallop CLI are required.

```bash
python scripts/audit_rule_ir_native_prompts.py
python -m pytest -q
```

The pinned runtime can be installed with:

```bash
bash scripts/install_scallop_runtime.sh
```

## Run one case

Start an OpenAI-compatible model server, then run:

```bash
python scripts/run_rule_ir_native_lean.py \
  --base-url http://127.0.0.1:8000 \
  --model MODEL_NAME \
  --case-id CASE_ID \
  --out-dir experiments/results/rule_ir_native_lean
```

The output directory records selection, complete predicate assessments, raw committed
Scallop reports, per-issue prose, the host-assembled answer, prompt hashes, and the Git
commit. There are no hidden retries or fallback inference paths.

On Slurm, supply deployment paths through `IDPR_*` variables and submit:

```bash
IDPR_CASE_ID=CASE_ID sbatch scripts/slurm/run_rule_ir_native_lean_smoke.sh
```

Raw benchmark and commentary sources are not committed. Copy `.env.example` to `.env`
and configure local paths where needed. Generated model outputs and caches are ignored
by Git; RuleIR/SCL candidates, schemas, legal-review ledgers, and audits remain versioned.
