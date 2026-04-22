#! /bin/sh

# Step 01: Convert everything to BIDS
python 01_convert_to_BIDS.py

# Step 02: run maxfilter
python 02_tsss.py -sub=1 -ses=1 -task=audvis -run=1
python 02_tsss.py -sub=1 -ses=1 -task=audvis -run=2
python 02_tsss.py -sub=1 -ses=2 -task=audvis -run=1
python 02_tsss.py -sub=1 -ses=2 -task=audvis -run=2
python 02_tsss.py -sub=2 -ses=1 -task=audvis -run=1
python 02_tsss.py -sub=2 -ses=1 -task=audvis -run=2
python 02_tsss.py -sub=2 -ses=2 -task=audvis -run=1
python 02_tsss.py -sub=2 -ses=2 -task=audvis -run=2

# Step 03: Fit ICA and detect components related to eye and heart artifacts
python 03_ica.py -sub=1 -ses=1 -task=audvis -run=1
python 03_ica.py -sub=1 -ses=1 -task=audvis -run=2
python 03_ica.py -sub=1 -ses=2 -task=audvis -run=1
python 03_ica.py -sub=1 -ses=2 -task=audvis -run=2
python 03_ica.py -sub=2 -ses=1 -task=audvis -run=1
python 03_ica.py -sub=2 -ses=1 -task=audvis -run=2
python 03_ica.py -sub=2 -ses=2 -task=audvis -run=1
python 03_ica.py -sub=2 -ses=2 -task=audvis -run=2

# Step 04: Cut epochs and average them as evokeds
python 04_epochs.py -sub=1 -ses=1 -task=audvis
python 04_epochs.py -sub=1 -ses=2 -task=audvis
python 04_epochs.py -sub=2 -ses=1 -task=audvis
python 04_epochs.py -sub=2 -ses=2 -task=audvis

# Step 05: Compute noise covariance matrices
python 05_noise_cov.py -sub=1 -ses=1 -task=audvis
python 05_noise_cov.py -sub=1 -ses=2 -task=audvis
python 05_noise_cov.py -sub=2 -ses=1 -task=audvis
python 05_noise_cov.py -sub=2 -ses=2 -task=audvis

# Step 05: Run FreeSurfer
python 05_freesurfer.py -sub=1
python 05_freesurfer.py -sub=2

# Step 07: Co-registration
# You need to run this manually

# Step 08: Source space and forward solution
python 08_forward.py -sub=1
python 08_forward.py -sub=2

# Step 09: Compute inverse solution and perform source estimation
python 09_inverse.py -sub=1 -ses=1 -task=audvis
python 09_inverse.py -sub=1 -ses=2 -task=audvis
python 09_inverse.py -sub=2 -ses=1 -task=audvis
python 09_inverse.py -sub=2 -ses=2 -task=audvis

# Step 10: Compute the grand-average across subjects
python 10_grand_average.py
