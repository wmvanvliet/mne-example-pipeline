"""Create the noise covariance matrix for the inverse solution."""

import argparse

import mne

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
print("Computing noise covariance for subject:", subject)
print("Session:", session)
print("Task:", task)

# Get epochs
epochs = mne.read_epochs(
    fname.epochs(subject=subject, session=session, task=task), preload=True
)

# Calculate noise covariance on baseline time period
# Check rank estimation!!!!
noise_cov = mne.compute_covariance(epochs, tmin=None, tmax=0, rank="info")
noise_cov = mne.cov.regularize(noise_cov, epochs.info, mag=0.05, grad=0.05)

# Save noise covariance matrix
mne.write_cov(
    fname.noise_cov(subject=subject, session=session, task=task),
    noise_cov,
    overwrite=True,
)
