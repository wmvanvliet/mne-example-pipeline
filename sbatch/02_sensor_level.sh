#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=02_sensor_level
#SBATCH --array=1-2  # do this for all 2 subjects
#SBATCH --output=out/02_sensor_level_sub-%a.out

# The subject we are currently processing.
sub=$SLURM_ARRAY_TASK_ID

# Load required software.
module load neuroimaging-env
module load maxfilter

# Perform the entire sensor-level analysis.
for ses in 1 2
do
	for run in 1 2
	do
		srun python ../02_tsss.py -sub $sub -ses $ses -run $run
	done
	srun python ../03_ica.py -sub $sub -ses $ses
	srun python ../04_epochs.py -sub $sub -ses $ses
	srun python ../05_noise_cov.py -sub $sub -ses $ses
done
