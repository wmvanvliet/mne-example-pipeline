#!/bin/bash
#SBATCH --time=10:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=10_grand_average
#SBATCH --output=out/10_grand_average.out

module load neuroimaging-env
srun python ../10_grand_average.py
