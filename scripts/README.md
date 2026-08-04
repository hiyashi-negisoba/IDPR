# Script entry points

## Active pipeline

- `run_rule_ir_native_lean.py`: the only active one-case runtime entry point
- `slurm/run_rule_ir_native_lean_smoke.sh`: job-local `inv_ass_env`/vLLM smoke
- `audit_rule_ir_native_prompts.py`: active prompt and structured-output audit
- `audit_rule_ir_registry.py`: registered RuleIR/SCL asset audit

The active path is closed unit selection -> complete predicate assessment -> committed
Scallop execution -> section prose with a host-owned conclusion. See
`docs/handoff/CURRENT.md` for the defects that remain.

## RuleIR asset builders and goldens

- `build_property_rule_ir.py`, `build_p2_native_rule_ir.py`: deterministic candidate
  builders; these are asset-generation tools, not runtime routers
- `run_property_scallop_golden.py`, `run_p2_native_scallop_golden.py`: native Scallop
  regression campaigns
- other `rulegen`, `fraud`, `property`, and review scripts: provenance/reproduction tools

## Historical comparison paths

`run_call1_fact_graphs.py`, `run_article_select.py`, `run_l0_candidates.py`,
`run_issue_assessment.py`, `run_issue_answer.py`, and `run_issue_pipeline_batch.py`
belong to the superseded issue-search/FactGraph pipeline. They remain for experiments
and comparison only. Do not use them as the active pipeline and do not import them from
`run_rule_ir_native_lean.py`.

Fixed-case checks and old comparisons live under `diagnostics/` and
`slurm/diagnostics/` and are never production entry points.
