#!/bin/bash
#SBATCH --time=5:00  # in this example, processing a subject takes less than 5 minutes
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=04_epochs
#SBATCH --array=1-2
#SBATCH --output=sbatch/out/04_epochs_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID

module load neuroimaging-env

srun python 04_epochs.py -sub $sub -ses 1
srun python 04_epochs.py -sub $sub -ses 2
