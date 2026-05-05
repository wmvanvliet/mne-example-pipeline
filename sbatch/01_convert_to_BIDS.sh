#!/bin/bash
#SBATCH --time=5:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=01_convert_to_BIDS
#SBATCH --output=out/01_convert_to_BIDS.out

module load neuroimaging-env
srun python ../01_convert_to_BIDS.py
