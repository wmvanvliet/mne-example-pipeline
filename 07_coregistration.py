"""
Coordinate frame alignment using a GUI.

In terminal, before starting e.g. spyder:
ml freesurfer
export FREESURFER_HOME=/work/modules/Ubuntu/14.04/amd64/t314/freesurfer/6.0.0
"""

import argparse

import mne

from config import fname

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
args = parser.parse_args()

subject = args.sub
# Convert the number into the corresponding FreeSurfer subject: 1 -> sub-01
freesurfer_subject = f"sub-{subject:02d}"

## Coregistration
gui = mne.gui.coregistration(
    subject=freesurfer_subject,
    inst=fname.raw(subject=subject, session=1, task="audvis", run=1, proc="raw"),
)

mne.write_trans(fname.trans(subject=subject), gui.coreg.trans)

# ruff: disable[E501]

# 1. Load digitalization source (head shape source) from any tsss file
# 2. Edit Fiducials (left side panel)
# 3. Save fiducials (default)
# 4. Fit fiducials
# 5. Fit ICP (head shape)
# 6. Omit outliers and fit ICP again
# 7. When happy with co-registation, save into the processed data folder (sub-01/sub-01_ses-01_trans.fif)
# 8. Run separately for each HPI digitalization (ses-01, ses-02)


## Check coregistration

# info = mne.io.read_info(test_data)
# ## surfaces: 'head-dense' = high resolution, 'head' = low reso, 'brain' = pial
# mne.viz.plot_alignment(info, coreg, subject=subject, dig=True, meg=['helmet', 'sensors'], subjects_dir=subjects_dir, surfaces='head-dense')
