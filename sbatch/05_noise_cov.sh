#!/bin/bash
#SBATCH --time=5:00  # in this example, processing a subject takes less than 5 minutes
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=05_noise_cov
#SBATCH --array=1-2
#SBATCH --output=out/05_noise_cov_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID

module load neuroimaging-env

srun python ../05_noise_cov.py -sub $sub -ses 1
srun python ../05_noise_cov.py -sub $sub -ses 2
