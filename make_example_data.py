"""
Create an example dataset for testing the pipeline.
This script is not part of the data analysis pipeline itself.

The example data somes from the MNE-sample dataset:
https://mne.tools/stable/documentation/datasets.html#sample

It contains the recording of a single subject, which this script will split to
simulate the situation in which we have multiple subjects, with multiple sessions
and multiple runs within a session.
"""

import os
import shutil
from datetime import UTC, datetime, timedelta

import mne
import mne_bids

# Don't print all of the standard MNE-Python output, just warnings and errors.
mne.set_log_level("WARNING")

# Where to store the MNE-sample data.
sample_data_path = None  # use the default chosen by MNE-Python

# Where to store the testing data we produce in this script.
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

# Load an empty room recording.
empty_room = mne.io.read_raw(
    sample_data_path / "MEG/sample/ernoise_raw.fif", preload=True
)

# Cut data into "subjects", "sessions" and "runs".
subjects = ["sub01", "sub02"]
sessions = ["session1", "session2"]
runs = ["run1", "run2"]

for subj_num, subj in enumerate(subjects, 1):
    # Copy anatomical MRI.
    shutil.copyfile(
        f"{sample_data_path}/subjects/sample/mri/orig/001.mgz",
        f"{target_data_path}/mri/{subj}.mgz",
    )

    time_window = (0, 30)  # in seconds
    for sess_num, sess in enumerate(sessions):
        # Create a fake measurement date for this session. Each subject and session was
        # recorded on a different day.
        meas_date = datetime(2026, 4, subj_num * len(sessions) + subj_num, tzinfo=UTC)

        # Pretend that the empty room recording was recorded first, at 10:00.
        er_meas_date = meas_date + timedelta(days=sess_num, hours=10)
        this_empty_room = empty_room.copy()
        this_empty_room.set_meas_date(er_meas_date)
        this_empty_room.save(
            f"{target_data_path}/meg/{subj}_{sess}_emptyroom_raw.fif", overwrite=True
        )

        # Create MEG files for each run.
        for run_num, run in enumerate(runs):
            raw_snippet = raw.copy().crop(*time_window)
            # Offset the measurement times for the different runs.
            run_meas_date = er_meas_date + timedelta(hours=1, minutes=15 * run_num)
            raw_snippet.set_meas_date(run_meas_date)
            raw_snippet.save(
                f"{target_data_path}/meg/{subj}_{sess}_{run}_raw.fif", overwrite=True
            )
            time_window = (time_window[0] + 30, time_window[1] + 30)

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
