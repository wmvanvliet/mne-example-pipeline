#!/bin/bash
#SBATCH --time=5:00  # in this example, processing a subject takes less than 5 minutes
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=09_inverse
#SBATCH --array=1-2
#SBATCH --output=sbatch/out/09_inverse_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID

module load neuroimaging-env

srun python 09_inverse.py -sub $sub -ses 1
srun python 09_inverse.py -sub $sub -ses 2
