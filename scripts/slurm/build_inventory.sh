#!/bin/bash
#SBATCH --job-name=idpr-inventory
#SBATCH --output=logs/idpr_inventory_%j.out
#SBATCH --error=logs/idpr_inventory_%j.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"

"$CLIENT_PYTHON" scripts/build_kcl_criminal_inventory.py
