#!/bin/bash
# This is not an SBATCH job, it only launches SBATCH jobs.

# Since we are using relative paths, we need to make sure the current working
# directory (pwd) is the directory containing this script.
cd $(dirname $0)

# Running `sbatch` will output: "Submitted batch job JOB_ID".
# We use "awk '{print $4}'" to get the JOB_ID number.
jid01=$(sbatch 01_convert_to_BIDS.sh | awk '{print $4}')
jid02=$(sbatch --dependency=afterok:$jid01 02_sensor_level.sh | awk '{print $4}')
jid03=$(sbatch --dependency=afterok:$jid02 03_freesurfer.sh | awk '{print $4}')
jid04=$(sbatch --dependency=afterok:$jid03 04_source_level.sh | awk '{print $4}')
jid05=$(sbatch --dependency=afterok:$jid04 05_grand_average.sh | awk '{print $4}')
