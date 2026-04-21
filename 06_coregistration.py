"""
Coordinate frame alignment using a GUI.

In terminal, before starting e.g. spyder:
ml freesurfer
export FREESURFER_HOME=/work/modules/Ubuntu/14.04/amd64/t314/freesurfer/6.0.0
"""

import mne

from config import fname

subject = 1
freesurfer_subject = "sub-01"

## Coregistration

mne.gui.coregistration(
    subject=freesurfer_subject,
    inst=fname.raw(subject=subject, session=1, task="audvis", run=1),
)

# 1. Load digitalization source (head shape source) from any tsss file
# 2. Edit Fiducaials (left side panel)
# 3. Save fiducials (default)
# 4. Fit fiducials
# 5. Fit ICP (head shape)
# 6. Omit outliers and fit ICP again
# 7. When happy with co-registation, save into the forward folder (sub-01_ses-01_coreg-transfile.fif)
# 8. Run separately for each HPI digitalization (ses-01, ses-02)


## Check coregistration

# info = mne.io.read_info(test_data)
# ## surfaces: 'head-dense' = high resolution, 'head' = low reso, 'brain' = pial
# mne.viz.plot_alignment(info, coreg, subject=subject, dig=True, meg=['helmet', 'sensors'], subjects_dir=subjects_dir, surfaces='head-dense')
