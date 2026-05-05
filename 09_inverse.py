"""
Calculate the MNE inverse operator and use it to perform source estimation.
"""

import argparse

import mne

import config
from config import fname

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
parser.add_argument("-ses", required=True, type=int, help="The session to process")
parser.add_argument("-task", default="audvis", help="The task to process")
args = parser.parse_args()

subject = args.sub
session = args.ses
task = args.task

fname.fill_placeholder("subject", subject)
fname.fill_placeholder("session", session)
fname.fill_placeholder("task", task)

print("Processing subject:", subject)
print("Processing session:", session)
print("Processing task:", task)

# Calculate noise covariance on baseline time period.

# Read noise covariance matrix
noise_cov = mne.read_cov(fname.noise_cov())

# Read the forward model, one model has been created for each session
fwd = mne.read_forward_solution(fname.fwd())

# Read the info
info = mne.io.read_info(fname.epochs())

# Compute inverse operator.
inverse_operator = mne.minimum_norm.make_inverse_operator(
    info=info, forward=fwd, noise_cov=noise_cov, loose=0.3, depth=0.8
)
mne.minimum_norm.write_inverse_operator(fname.inv(), inverse_operator, overwrite=True)

# Calculate morph matrix from the subject-specific brain to a template (fsaverage).
morph = mne.compute_source_morph(
    fwd["src"],
    subject_from=f"sub-{subject:02d}",
    subject_to="fsaverage",
    subjects_dir=fname.subjects_dir,
    spacing=5,
    smooth=10,
)

# Compute inverse for all conditions.
pick_ori = None  # 'normal' or None
snr = 3.0
lambda2 = 1.0 / snr**2
method = "dSPM"

for condition in config.conditions.keys():
    print("Computing stc for condition:", condition)
    evoked = mne.read_evokeds(
        fname.evokeds(),
        proj=config.enable_projections,
        baseline=config.baseline,
        condition=condition,
    )
    stc = mne.minimum_norm.apply_inverse(
        evoked, inverse_operator, lambda2, method, pick_ori=pick_ori
    )
    stc.save(fname.stc(condition=condition), overwrite=True)

    # Also create a version that is morphed to the template brain.
    stc_morphed = morph.apply(stc)
    stc_morphed.save(
        fname.stc_morphed(condition=condition),
        overwrite=True,
    )

    with mne.open_report(fname.report()) as report:
        report.add_stc(
            stc,
            title=f"STC: ses-{session:02d} cond-{condition}",
            replace=True,
        )

report.save(fname.report_html(), open_browser=False, overwrite=True)
