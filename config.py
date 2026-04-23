"""
===========
Config file
===========

Configuration parameters for the study.
"""

import os

import pandas as pd
from filename_templates import FileNames

########################################################################################
# Data folders. SET THESE TO MATCH YOUR OWN SYSTEM.
########################################################################################

# Folder containing the original data recorded during the project.
orig_data_path = "./data/orig"

# Folder containing the BIDS version of the data.
bids_path = "./data/bids"

# Folder to write the processed MEG data to.
processed_data_path = "./data/processed"

# Folder for the MRIs that have been processed with FreeSurfer (SUBJECTS_DIR).
subjects_dir = "./data/bids/derivatives/freesurfer"

########################################################################################
# Experiment design: subjects, session, runs, tasks, event codes, etc.
########################################################################################

# The subjects to include in the analysis pipeline. You can comment-out subjects to
# remove them from the analysis if there was some problem with the data.
subjects = [
    1,
    2,
    # 3,  metal present in body causing too many artifacts
]

# "Sessions" are different recording days for the same participant.
sessions = [1, 2]

# "Runs" are blocks of trials, run during the same session. For example, all the trials
# before the participant took a break could be a "run". "Tasks" are different
# experimental paradigms. We often have a different number of runs per task.
tasks = ["audvis"]
runs_per_task = {
    "audvis": [1, 2],
}

# Events and their trigger-codes.
# "description of the event": trigger-code
event_id = {
    "auditory/left": 1,
    "auditory/right": 2,
    "visual/left": 3,
    "visual/right": 4,
    "smiley": 5,
    "buttonpress": 32,
}

# Names for the experimental conditions (don't use "/" in condition names) and the
# events to use for each condition.
conditions = {
    "vis_l": "visual/left",
    "vis_r": "visual/right",
    "aud_l": "auditory/left",
    "aud_r": "auditory/right",
}

# Manually defined bad channels.
bad_channels = [
    dict(subject=1, session=1, task="audvis", run=1, channels=["MEG 2443", "EEG 053"]),
    dict(subject=1, session=1, task="audvis", run=2, channels=["MEG 2443", "EEG 053"]),
    dict(subject=1, session=2, task="audvis", run=1, channels=["MEG 2443", "EEG 053"]),
    dict(subject=1, session=2, task="audvis", run=2, channels=["MEG 2443", "EEG 053"]),
    dict(subject=2, session=1, task="audvis", run=1, channels=["MEG 2443", "EEG 053"]),
    dict(subject=2, session=1, task="audvis", run=2, channels=["MEG 2443", "EEG 053"]),
    dict(subject=2, session=2, task="audvis", run=1, channels=["MEG 2443", "EEG 053"]),
    dict(subject=2, session=2, task="audvis", run=2, channels=["MEG 2443", "EEG 053"]),
]
bad_channels = pd.DataFrame(bad_channels).explode("channels")


########################################################################################
# Common parameters used in multiple analysis scripts.
########################################################################################
proc = "tsss"  # Set to `proc = "raw"` to disable maxfilter TSSS

# Bandpass filter to apply.
bandpass = (0.05, 40)

# The baseline window for the epochs.
epochs_window = (-0.2, 1.0)  # in seconds relative to stimulus onset
baseline = (-0.2, 0)  # in seconds relative to stimulus onset

# The rejection thresholds for various artifacts.
reject_eog_correlation = 0.2  # reject ICA components that correlate with EOG
reject_ecg_correlation = 0.5  # reject ICA components that correlate with ECG
reject_epochs = dict(mag=4e-12, grad=3000e-13)  # reject epochs with too large signals

# Source "spacing" controlling the resolution of the source estimate.
# Common choices fow a "low" resolution are: "ico4" or "oct5"
# Common choices fow a "high" resolution are: "ico5" or "oct6"
spacing = "ico4"

########################################################################################
# Templates for filenames.
#
# These are all the filenames used in the analysis in one place. Try to be consistent
# and always define your filenames here, instead of in individual analysis scripts.
# See here for documentation on how these templates work:
# https://github.com/wmvanvliet/filename-templates#filename-templates
#
# In short:
#  - Placeholders, such as `{subject}`, become parameters for the filename function.
#  - Placeholders that already exist as a filename alias, such as `{orig_path}`, are
#    filled automatically.
#  - Placeholders follow Python's string formatting syntax.
#    For example: `{subject:02d}` means a zero-padded number.
#    See: https://docs.python.org/3/library/string.html#format-examples
########################################################################################

fname = FileNames()
# fmt: off
# ruff: disable[E501]

# These are the folders specified at the top of this config file.
# `mkdir=True` means that the folder will be created if it doesn't exist yet.
fname.add("orig_path", orig_data_path)
fname.add("bids_path", bids_path, mkdir=True)
fname.add("processed_path", processed_data_path, mkdir=True)
fname.add("subjects_dir", subjects_dir, mkdir=True)

# Add these so we can use them in the filenames.
fname.add("spacing", spacing)
fname.add("task", "audvis")  # the task is always "audvis" this example experiment

# Original raw data, before BIDS conversion. THESE WILL BE DIFFERENT FOR YOUR OWN STUDY!
fname.add("orig_meg", "{orig_path}/meg/sub{subject:02d}_session{session}_run{run}_raw.fif")
fname.add("orig_mri", "{orig_path}/mri/sub{subject:02d}.mgz")
# Scanner-specific calibration files.
# These depends on whether you recorded the data at BioMag, Aalto, or somewhere else.
fname.add("orig_calibration", "{orig_path}/sss_cal_biomag_triux.dat")
fname.add("orig_crosstalk", "{orig_path}/ct_sparse_biomag_triux.fif")

# Raw data, after BIDS conversion.
fname.add("raw", "{bids_path}/sub-{subject:02d}/ses-{session:02d}/meg/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run:02d}_proc-{proc}_meg.fif")
fname.add("mri", "{bids_path}/sub-{subject:02d}/anat/sub-{subject:02d}_T1w.nii.gz")

# Scanner-specific calibration files, after BIDS conversion.
fname.add("calibration", "{bids_path}/sub-{subject:02d}/ses-{session:02d}/meg/sub-{subject:02d}_ses-{session:02d}_acq-calibration_meg.dat")
fname.add("crosstalk", "{bids_path}/sub-{subject:02d}/ses-{session:02d}/meg/sub-{subject:02d}_ses-{session:02d}_acq-crosstalk_meg.fif")

# Files produced by Maxfilter.
fname.add("pos", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run:02d}_movecomp.pos", mkdir=True)

# Sensor-level files
fname.add("epochs", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_epo.fif", mkdir=True)
fname.add("evokeds", "{processed_path}/evokeds/sub-{subject:02d}_ses-{session:02d}_task-{task}_ave.fif", mkdir=True)

# Artefact removal
fname.add("ica", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run:02d}_ica.fif", mkdir=True)

# Coregistration files (WIP)
fname.add("fid", "{subjects_dir}/sub-{subject:02d}/bem/sub-{subject:02d}_fiducials.fif", mkdir=True)
fname.add("trans", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_trans.fif", mkdir=True)

# Head model
fname.add("src", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_spacing-{spacing}-src.fif", mkdir=True)
fname.add("bem_sol", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_bem-sol.fif", mkdir=True)
fname.add("fwd", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_spacing-{spacing}-fwd.fif", mkdir=True)

# Inverse solution
fname.add("noise_cov", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_cov.fif", mkdir=True)
fname.add("inv", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}-{spacing}-inv.fif", mkdir=True)

# Source estimates
fname.add("stc", "{processed_path}/stcs/sub-{subject:02d}_ses-{session:02d}_task-{task}_cond-{condition}", mkdir=True)
fname.add("stc_hemi", "{processed_path}/stcs/sub-{subject:02d}_ses-{session:02d}_task-{task}_cond-{condition}-{hemi}.stc", mkdir=True)
fname.add("stc_morphed", "{processed_path}/stcs/sub-{subject:02d}_ses-{session:02d}_task-{task}_cond-{condition}_morphed", mkdir=True)
fname.add("stc_morphed_hemi", "{processed_path}/stcs/sub-{subject:02d}_ses-{session:02d}_task-{task}_cond-{condition}_morphed-{hemi}.stc", mkdir=True)

# Grand-average files
fname.add("ga_evokeds", "{processed_path}/evokeds/GA_ses-{session:02d}_task-{task}_ave.fif", mkdir=True)
fname.add("ga_stc", "{processed_path}/stcs/GA_ses-{session:02d}_task-{task}_cond-{condition}", mkdir=True)
fname.add("ga_stc_hemi", "{processed_path}/stcs/GA_ses-{session:02d}_task-{task}_cond-{condition}-{hemi}.stc", mkdir=True)

# fmt: on
# ruff: enable[E501]

# Add `subjects_dir` as an environment variable for convenience. This way, you don't
# have to specify `subjects_dir=subjects_dir` all the time when using MNE-Python
# functions.
os.environ["SUBJECTS_DIR"] = subjects_dir
