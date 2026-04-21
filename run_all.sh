# Step 01: Convert everything to BIDS
python 01_convert_to_BIDS

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
