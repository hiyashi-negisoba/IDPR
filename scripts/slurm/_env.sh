#!/bin/bash

# Shared, machine-independent defaults for Slurm entry points.  A deployment may set
# these variables in its scheduler environment; no workstation or model-cache path is
# encoded in the repository.
IDPR_SLURM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$(cd "$IDPR_SLURM_DIR/../.." && pwd)}}"
CLIENT_PYTHON="${IDPR_PYTHON:-python}"
PYTHON_BIN="${IDPR_PYTHON:-python}"
VLLM_BIN="${IDPR_VLLM_BIN:-vllm}"
MODEL_SNAPSHOT="${IDPR_MODEL_SOURCE:-google/gemma-4-26B-A4B-it}"
SERVED_MODEL="${IDPR_SERVED_MODEL:-google/gemma-4-26B-A4B-it}"
LOCAL_API_KEY="${IDPR_API_KEY:-local-idpr}"

if [ -n "${IDPR_HF_HOME:-}" ]; then
    export HF_HOME="$IDPR_HF_HOME"
fi
