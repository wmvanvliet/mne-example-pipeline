"""
Download example data for testing the pipeline.

The example data somes from the MNE-sample dataset:
https://mne.tools/stable/documentation/datasets.html#sample

It contains the recording of a single subject, which this script will split to
simulate the situation in which we have multiple subjects, with multiple sessions
and multiple runs within a session.
"""

import os
import shutil
import itertools

import mne
import mne_bids

# Don't print all of the standard MNE-Python output, just warnings and errors.
mne.set_log_level("WARNING")

# Where to store the MNE-sample data.
sample_data_path = None  # use the default chosen by MNE-Python

# Where to store the testing data we produce in this script.
target_data_path = "./data/raw"

# Make the data folders we're doing to need.
os.makedirs(f"{target_data_path}/meg", exist_ok=True)
os.makedirs(f"{target_data_path}/mri", exist_ok=True)

# Downloads the data (1.5GB) and sets `sample_data_path` to the path the data was
# downloaded to.
sample_data_path = mne.datasets.sample.data_path(path=sample_data_path, verbose=True)

# Load the data into memory.
raw = mne.io.read_raw(sample_data_path / "MEG/sample/sample_audvis_raw.fif")

# Cut data into "subjects", "sessions" and "runs".
subjects = ["sub01", "sub02"]
sessions = ["session1", "session2"]
runs = ["run1", "run2"]

time_window = (0, 30)  # in seconds
for subj, sess, run in itertools.product(subjects, sessions, runs):
    raw_snippet = raw.copy().crop(*time_window)
    raw_snippet.save(
        f"{target_data_path}/meg/{subj}_{sess}_{run}_raw.fif", overwrite=True
    )
    time_window = (time_window[0] + 30, time_window[1] + 30)  # (0, 30)->(30, 60) etc.

# Copy MRI files.
for subj in subjects:
    shutil.copyfile(
        f"{sample_data_path}/subjects/sample/mri/orig/001.mgz",
        f"{target_data_path}/mri/{subj}.mgz",
    )

# Print a listing of the created files.
print("Created the following files:")
mne_bids.print_dir_tree(target_data_path)
