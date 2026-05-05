#!/bin/bash
# This is not an SBATCH job, it only launches SBATCH jobs.
jid01=$(sbatch sbatch/01_convert_to_BIDS.sh | awk '{print $4}')
jid02=$(sbatch --dependency=afterok:$jid01 sbatch/02_tsss.sh | awk '{print $4}')
jid03=$(sbatch --dependency=afterok:$jid02 sbatch/03_ica.sh | awk '{print $4}')
jid04=$(sbatch --dependency=afterok:$jid03 sbatch/04_epochs.sh | awk '{print $4}')
jid05=$(sbatch --dependency=afterok:$jid04 sbatch/05_noise_cov.sh | awk '{print $4}')
jid06=$(sbatch --dependency=afterok:$jid05 sbatch/06_freesurfer.sh | awk '{print $4}')
jid07=$(sbatch --dependency=afterok:$jid06 sbatch/07_coregistration.sh | awk '{print $4}')
jid08=$(sbatch --dependency=afterok:$jid07 sbatch/08_forward.sh | awk '{print $4}')
jid09=$(sbatch --dependency=afterok:$jid01 sbatch/09_inverse.sh | awk '{print $4}')
jid10=$(sbatch --dependency=afterok:$jid01 sbatch/10_grand_average.sh | awk '{print $4}')
