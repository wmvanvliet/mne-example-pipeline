"""
Create an example dataset for testing the pipeline.
This script is not part of the data analysis pipeline itself.

The example data somes from the MNE-sample dataset:
https://mne.tools/stable/documentation/datasets.html#sample
"""

import os
import shutil

import mne
import mne_bids

# Don't print all of the standard MNE-Python output, just warnings and errors.
mne.set_log_level("WARNING")

# Where to store the MNE-sample data.
sample_data_path = None  # use the default chosen by MNE-Python

# Where to store the example data.
target_data_path = "./data/orig"

# Make the data folders we're doing to need.
os.makedirs(f"{target_data_path}/meg", exist_ok=True)
os.makedirs(f"{target_data_path}/mri", exist_ok=True)

# Downloads the data (1.5GB) and sets `sample_data_path` to the path the data was
# downloaded to.
sample_data_path = mne.datasets.sample.data_path(path=sample_data_path, verbose=True)

# Load the data into memory.
raw = mne.io.read_raw(
    sample_data_path / "MEG/sample/sample_audvis_raw.fif", preload=True
)

# Cut data into "subjects"
subjects = ["sub01", "sub02"]

# Create MEG and MRI files for each subject.
time_window = (0, 60)  # in seconds
for subj in subjects:
    # Copy anatomical MRI.
    shutil.copyfile(
        f"{sample_data_path}/subjects/sample/mri/orig/001.mgz",
        f"{target_data_path}/mri/{subj}.mgz",
    )

    # Cut out a piece of MEG data for the subject.
    raw_snippet = raw.copy().crop(*time_window)
    raw_snippet.save(
        f"{target_data_path}/meg/{subj}_raw.fif", overwrite=True
    )

    # Next piece will need a later piece of MEG data.
    time_window = (time_window[0] + 60, time_window[1] + 60)

# Scanner-specific calibration files. Pretend the data was recorded at BioMag.
shutil.copyfile(
    f"{sample_data_path}/SSS/sss_cal_mgh.dat",
    f"{target_data_path}/sss_cal_biomag_triux.dat",
)
shutil.copyfile(
    f"{sample_data_path}/SSS/ct_sparse_mgh.fif",
    f"{target_data_path}/ct_sparse_biomag_triux.fif",
)

# Print a listing of the created files.
print("Created the following files:")
mne_bids.print_dir_tree(target_data_path)
