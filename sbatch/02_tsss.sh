#!/bin/bash
#SBATCH --time=5:00  # in this example, processing a subject takes less than 5 minutes
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=02_tsss
#SBATCH --array=1-2
#SBATCH --output=out/02_tsss_sub-%a.out

sub=$SLURM_ARRAY_TASK_ID

module load neuroimaging-env
module load maxfilter

srun python ../02_tsss.py -sub $sub -ses 1 -run 1
srun python ../02_tsss.py -sub $sub -ses 1 -run 2
srun python ../02_tsss.py -sub $sub -ses 2 -run 1
srun python ../02_tsss.py -sub $sub -ses 2 -run 2
