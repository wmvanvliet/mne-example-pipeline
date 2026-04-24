"""
Calculate the MNE inverse operator and use it to perform source estimation.
"""

import mne

for subject in ["sub01", "sub02"]:
    # Read noise covariance matrix.
    noise_cov = mne.read_cov(f"./data/processed/{subject}/{subject}_cov.fif")

    # Read the forward model.
    fwd = mne.read_forward_solution(f"./data/processed/{subject}/{subject}_fwd.fif")

    # Read the info
    info = mne.io.read_info(f"./data/processed/{subject}/{subject}_epo.fif")

    # Compute inverse operator.
    inverse_operator = mne.minimum_norm.make_inverse_operator(
        info=info, forward=fwd, noise_cov=noise_cov, loose=0.3, depth=0.8
    )
    mne.minimum_norm.write_inverse_operator(
        f"./data/processed/{subject}/{subject}_inv.fif",
        inverse_operator,
        overwrite=True,
    )

    # Calculate morph matrix from the subject-specific brain to a template (fsaverage).
    morph = mne.compute_source_morph(
        fwd["src"],
        subject_from=subject,
        subject_to="fsaverage",
        subjects_dir="./data/freesurfer",
        spacing=5,
        smooth=10,
    )

    # Compute inverse for all conditions.
    pick_ori = None  # 'normal' or None
    snr = 3.0
    lambda2 = 1.0 / snr**2
    method = "dSPM"

    for condition in ["aud_l", "aud_r", "vis_l", "vis_r"]:
        evoked = mne.read_evokeds(
            f"./data/processed/{subject}/{subject}_ave.fif",
            baseline=(-0.2, 0),
            condition=condition,
        )
        stc = mne.minimum_norm.apply_inverse(
            evoked, inverse_operator, lambda2, method, pick_ori=pick_ori
        )
        stc.save(
            f"./data/processed/{subject}/{subject}_{condition}_stc", overwrite=True
        )

        # Also create a version that is morphed to the template brain.
        stc_morphed = morph.apply(stc)
        stc_morphed.save(
            f"./data/processed/{subject}/{subject}_{condition}_morphed_stc",
            overwrite=True,
        )
