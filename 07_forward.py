"""Setup the source space and compute the forward solution."""

import mne

for subject in ["sub01", "sub02"]:
    # Setup souce space.
    src = mne.setup_source_space(
        subject=subject,
        spacing="ico4",
        subjects_dir="./data/freesurfer",
        n_jobs=-1,
        add_dist=True,
    )
    mne.write_source_spaces(
        f"./data/processed/{subject}/{subject}_src.fif", src, overwrite=True
    )

    # Create BEM model
    bem = mne.make_bem_model(
        subject=subject,
        ico=4,
        subjects_dir="./data/freesurfer",
        conductivity=(0.3,),  # one-layer model, use (0.3, 0.006, 0.3) for three layers
    )
    bem_sol = mne.make_bem_solution(bem)
    mne.write_bem_solution(
        f"./data/processed/{subject}/{subject}_bem-sol.fif", bem_sol, overwrite=True
    )

    # Create the forward model, coregistration required (trans_file)
    info = mne.io.read_info(f"./data/orig/meg/{subject}_raw.fif")
    fwd = mne.make_forward_solution(
        info,
        trans=f"./data/processed/{subject}/{subject}_trans.fif",
        src=src,
        bem=bem_sol,
        meg=True,
        eeg=False,  # turn this on for a combined MEG+EEG head model
        mindist=0,
        n_jobs=-1,
    )
    mne.write_forward_solution(
        f"./data/processed/{subject}/{subject}_fwd.fif", fwd, overwrite=True
    )
