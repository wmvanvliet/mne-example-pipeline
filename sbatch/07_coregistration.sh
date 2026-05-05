#!/bin/bash
#SBATCH --time=5:00  # in this example, processing a subject takes less than 5 minutes
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=07_coregistration
#SBATCH --array=1-2
#SBATCH --output=out/07_coregistration_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID
module load neuroimaging-env
srun python ../07_coregistration.py -sub $sub
