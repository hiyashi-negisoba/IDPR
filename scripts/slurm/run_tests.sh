#!/bin/bash
#SBATCH --job-name=idpr-tdd
#SBATCH --output=logs/idpr_tdd_%j.out
#SBATCH --error=logs/idpr_tdd_%j.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
cd "$PROJECT_ROOT"

export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
"$CLIENT_PYTHON" -m pytest -q tests
