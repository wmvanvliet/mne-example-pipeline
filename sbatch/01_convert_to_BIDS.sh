#!/bin/bash
#SBATCH --time=5:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4  # set this to config.n_jobs
#SBATCH --job-name=01_convert_to_BIDS
#SBATCH --output=out/01_convert_to_BIDS.out

# Since we are using relative paths, we need to make sure the current working
# directory (pwd) is the directory containing this script.
cd $(dirname $0)

module load neuroimaging-env
srun python ../01_convert_to_BIDS.py
