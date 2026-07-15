#!/bin/bash
#SBATCH --job-name=idpr-tdd
#SBATCH --output=logs/idpr_tdd_%j.out
#SBATCH --error=logs/idpr_tdd_%j.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

set -euo pipefail

source /data5/jaehoonjeong/miniconda3/etc/profile.d/conda.sh
conda activate base
cd /home/jaehoonjeong/data/IDPR

export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
python -m pytest -q tests
