#!/bin/bash
#SBATCH --job-name=idpr-inventory
#SBATCH --output=logs/idpr_inventory_%j.out
#SBATCH --error=logs/idpr_inventory_%j.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

set -euo pipefail

source /data5/jaehoonjeong/miniconda3/etc/profile.d/conda.sh
conda activate base
cd /home/jaehoonjeong/data/IDPR

/data5/jaehoonjeong/miniconda3/bin/python scripts/build_kcl_criminal_inventory.py
