#!/bin/bash
#SBATCH --time=12:00:00  # FreeSurfer takes a long time
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1  # FreeSurfer is single-core
#SBATCH --job-name=06_freesurfer
#SBATCH --array=1-2
#SBATCH --output=sbatch/out/06_freesurfer_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID
module load neuroimaging-env
module load triton/2024.1-gcc
module load freesurfer
srun python 06_freesurfer.py -sub $sub
