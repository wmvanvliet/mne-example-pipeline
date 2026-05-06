#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=04_source_level
#SBATCH --array=1-2  # do this for all 2 subjects
#SBATCH --output=out/04_source_level_sub-%a.out

# The subject we are currently processing.
sub=$SLURM_ARRAY_TASK_ID

# Load required software.
module load neuroimaging-env

sessions=1 2

# Perform the entire source-level analysis (after FreeSurfer).
for ses in $sessions
do
	srun python ../07_coregistration.py -sub $sub -ses $ses
done

srun python ../08_forward.py -sub $sub

for ses in $sessions
do
	srun python ../09_inverse.py -sub $sub -ses $ses
done
