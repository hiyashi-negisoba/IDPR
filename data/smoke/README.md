# Phase 3 E2E smoke assets

This directory is the only development-time case pool for the Phase 3 freeze.

- `phase3_e2e_inventory.jsonl` contains exactly two model-facing records and only the
  input whitelist fields: `sub_question_id`, `question_text`, and `question_prompt`.
- `phase3_e2e_rubrics.json` is evaluation-only. Pipeline runners do not read it.
- The reviewed KCL rubric row is copied into the evaluation-only rubric asset, with source
  provenance, so reviewing this smoke never requires opening the other 59 cases.
- The second case is the user-provided case that was formerly named
  `CASE_KCL1730_2026_BRIBERY_FRAUD_002`. Only its input and the old review checklist are
  recovered; none of the deleted keyword-matching/Gemini pipeline is restored.

The remaining 59 KCL questions are final-evaluation data and must not be used for
development, smoke testing, prompt tuning, or retrieval tuning.

The freeze runner is `scripts/slurm/run_phase3_e2e_smoke.sh`. It never accepts the rubric
as a pipeline argument; only the final deterministic verifier reads the rubric asset to
confirm that its two IDs match the smoke inventory.
