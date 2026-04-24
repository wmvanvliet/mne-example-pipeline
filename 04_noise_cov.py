"""Create the noise covariance matrix for the inverse solution."""

import mne

for subject in ["sub01", "sub02"]:
    # Get epochs
    epochs = mne.read_epochs(f"./data/processed/{subject}/{subject}_epo.fif")

    # Calculate noise covariance on baseline time period
    # Check rank estimation!!!!
    noise_cov = mne.compute_covariance(epochs, tmin=None, tmax=0, rank="info")
    noise_cov = mne.cov.regularize(noise_cov, epochs.info, mag=0.05, grad=0.05)

    # Save noise covariance matrix
    mne.write_cov(
        f"./data/processed/{subject}/{subject}_cov.fif", noise_cov, overwrite=True
    )
