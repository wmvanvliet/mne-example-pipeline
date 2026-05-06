#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=03_source_level
#SBATCH --array=1-2  # do this for all 2 subjects
#SBATCH --output=out/03_source_level_sub-%a.out

# The subject we are currently processing.
sub=$SLURM_ARRAY_TASK_ID

# Load required software.
module load neuroimaging-env

# Perform the entire sourse-level analysis (after FreeSurfer).
for ses in 1 2
do
	srun python ../07_coregistration.py -sub $sub -ses $ses
done
srun python ../08_forward.py -sub $sub
srun python ../09_inverse.py -sub $sub
