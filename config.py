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

# Folder containing the raw data recorded during the project.
raw_data_path = "./data/raw"

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
tasks = ["audvis", "emptyroom"]
runs_per_task = {
    "audvis": [1, 2],
    "emptyroom": [1],
}

# Events and their trigger-codes.
# "description of the event": trigger-code
event_id = {
    "visual/left": 1,
    "visual/right": 2,
    "auditory/left": 3,
    "auditory/right": 4,
    "smiley": 5,
    "buttonpress": 32,
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

# Preprocessing with maxfilter
proc = "tsss"

# Rejection limits
reject = dict(mag=4e-12, grad=3000e-13)  # , eog=150e-6)

# Default baseline window
default_baseline = (-0.2, 0)

# Source spacing
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
#  - Placeholders that already exist as a filename alias, such as `{raw_path}`, are
#    filled automatically.
#  - Placeholders follow Python's string formatting syntax.
#    For example: `{subject:02d}` means a zero-padded number.
#    See: https://docs.python.org/3/library/string.html#format-examples
########################################################################################

fname = FileNames()
# fmt: off
# ruff: disable[E501]

# These are the folders specified at the top of this config file.
fname.add("raw_path", raw_data_path)
fname.add("bids_path", bids_path)
fname.add("processed_path", processed_data_path)
fname.add("subjects_dir", subjects_dir)

# Add these so we can use them in the filenames.
fname.add("spacing", spacing)
fname.add("task", "audvis")  # the task is always "audvis" this example experiment

# Original raw data, before BIDS conversion.
fname.add("raw_meg", "{raw_path}/meg/sub{subject:02d}_session{session}_run{run}_raw.fif")
fname.add("raw_mri", "{raw_path}/mri/sub{subject:02d}.mgz")

# Raw data, after BIDS conversion.
fname.add("raw", "{bids_path}/sub-{subject:02d}/ses-{session:02d}/meg/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run:02d}_proc-raw_meg.fif")

# Manually annotated bad channels.
fname.add("bad_channels", "bad_channels.csv")

# Files produced by Maxfilter.
# `mkdir=True` means that the folder will be created if it doesn't exist yet.
fname.add("pos", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run}_movecomp.pos", mkdir=True)
fname.add("tsss_log", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run}_tsss_log.log", mkdir=True)

# Sensor-level files
fname.add("raw_tsss", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run}_proc-tsss_meg.fif", mkdir=True)
fname.add("epochs", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_epo.fif", mkdir=True)
fname.add("evoked", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_ave.fif", mkdir=True)

# Artefact removal
fname.add("ica", "{processed_path}/sub-{subject:02d}/sub-{subject:02d}_ses-{session:02d}_task-{task}_run-{run}_ica.fif", mkdir=True)

# Files produced by FreeSurfer
fname.add("freesurfer_log", "{processed_path}/sub-{subject:02d}/freesurfer_log.log", mkdir=True)

# Coregistration files (WIP)
fname.add("fid", "{subjects_dir}/{subject}/bem/{subject}-fiducials.fif")
fname.add("trans_file", "{megbids_dir}/{subject}_ses-{ses}_coreg-transfile.fif")
fname.add(
    "trans_file_old", "{subjects_dir}/{subject}/mri/T1-neuromag/sets/COR-transfile.fif"
)
fname.add(
    "coreg_log", "{megprocessed_dir}/forward/coreg_log_{subject}_ses-{ses}_hs.csv"
)

# Source space and forward model
fname.add("bem_sol", "{megprocessed_dir}/forward/{subject}-{ntri}-bem-sol.fif")
fname.add(
    "fwd",
    "{megprocessed_dir}/forward/{subject}_ses-{ses}_task-{task}_run-{run}-{spacing}-fwd.fif",
)
fname.add("src", "{megprocessed_dir}/forward/{subject}-{spacing}-src.fif")

# Inverse solution
fname.add(
    "noise_cov", "{megprocessed_dir}/noise_cov/{subject}_ses-{ses}_task-{task}_cov.fif"
)
fname.add(
    "inv",
    "{megprocessed_dir}/inverse/{subject}_ses-{ses}_task-{task}-{spacing}-inv.fif",
)

# STC-files
fname.add(
    "stc_hemi",
    "{megprocessed_dir}/stcs/{subject}_ses-{ses}_task-{task}-{condition}-{hemi}.stc",
)
fname.add("stc", "{megprocessed_dir}/stcs/{subject}_ses-{ses}_task-{task}-{condition}")

# Add `subjects_dir` as an environment variable for convenience. This way, you don't
# have to specify `subjects_dir=subjects_dir` all the time when using MNE-Python
# functions.
os.environ["SUBJECTS_DIR"] = subjects_dir
