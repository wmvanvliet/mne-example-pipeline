"""
Create an example dataset for testing the pipeline.
This script is not part of the data analysis pipeline itself.

The example data somes from the MNE-sample dataset:
https://mne.tools/stable/documentation/datasets.html#sample

It contains the recording of a single subject, which this script will split to
simulate the situation in which we have multiple subjects, with multiple sessions
and multiple runs within a session.
"""

import argparse
import os
import shutil
from datetime import datetime, timedelta, timezone

import mne
import mne_bids

# Handle command-line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-d",
    "--data_path",
    required=False,
    default="./data/orig",
    help="The folder you want to data to be stored in.",
)
args = parser.parse_args()

# Don't print all of the standard MNE-Python output, just warnings and errors.
mne.set_log_level("WARNING")

# Where to store the MNE-sample data.
sample_data_path = None  # use the default chosen by MNE-Python

# Make the data folders we're doing to need.
os.makedirs(f"{args.data_path}/meg", exist_ok=True)
os.makedirs(f"{args.data_path}/mri", exist_ok=True)

# Downloads the data (1.5GB) and sets `sample_data_path` to the path the data was
# downloaded to.
sample_data_path = mne.datasets.sample.data_path(path=sample_data_path, verbose=True)

# Load the data into memory.
raw = mne.io.read_raw(
    sample_data_path / "MEG/sample/sample_audvis_raw.fif", preload=True
)

# Load empty room recording into memory.
emptyroom = mne.io.read_raw(
    sample_data_path / "MEG/sample/ernoise_raw.fif", preload=True
)

# Cut data into "subjects", "sessions" and "runs".
subjects = ["sub01", "sub02"]
sessions = ["session1", "session2"]
runs = ["run1", "run2"]

for subj_num, subj in enumerate(subjects, 1):
    # Measurement date for this subject.
    meas_date = datetime(2026, 4, subj_num * 4, tzinfo=timezone.utc)

    # Copy anatomical MRI.
    shutil.copyfile(
        f"{sample_data_path}/subjects/sample/mri/orig/001.mgz",
        f"{args.data_path}/mri/{subj}.mgz",
    )

    time_window = (0, 30)  # in seconds
    for sess_num, sess in enumerate(sessions):
        # Empty room was recorded at 10:00.
        meas_date += timedelta(days=sess_num, hours=10)

        emptyroom.set_meas_date(meas_date)
        emptyroom.save(
            f"{args.data_path}/meg/{subj}_{sess}_emptyroom_raw.fif", overwrite=True
        )

        # Session with subject started at 11:00.
        meas_date += timedelta(hours=1)

        # Create MEG files for each run.
        for run_num, run in enumerate(runs):
            meas_date += timedelta(minutes=15 * run_num)
            raw_snippet = raw.copy().crop(*time_window)
            raw_snippet.set_meas_date(meas_date)
            raw_snippet.save(
                f"{args.data_path}/meg/{subj}_{sess}_{run}_raw.fif", overwrite=True
            )
            time_window = (time_window[0] + 30, time_window[1] + 30)

# Scanner-specific calibration files. Pretend the data was recorded at BioMag.
shutil.copyfile(
    f"{sample_data_path}/SSS/sss_cal_mgh.dat",
    f"{args.data_path}/sss_cal_biomag_triux.dat",
)
shutil.copyfile(
    f"{sample_data_path}/SSS/ct_sparse_mgh.fif",
    f"{args.data_path}/ct_sparse_biomag_triux.fif",
)

# Print a listing of the created files.
print("Created the following files:")
mne_bids.print_dir_tree(args.data_path)
