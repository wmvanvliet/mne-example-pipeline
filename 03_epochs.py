"""
Create epochs and evoked responses from your raw data.
We concanenate epochs across runs.
"""

import mne

for subject in ["sub01", "sub02"]:
    raw = mne.io.read_raw(
        f"./data/processed/{subject}/{subject}_tsss_raw.fif", preload=True
    )

    # Bandpass filter.
    raw.filter(0.05, 40)

    # Apply the ICA we constructed in the previous step.
    ica = mne.preprocessing.read_ica(f"./data/processed/{subject}/{subject}_ica.fif")
    raw = ica.apply(raw)

    # Make epochs and average
    events = mne.find_events(raw, min_duration=2 / raw.info["sfreq"])
    epochs = mne.Epochs(
        raw,
        events,
        event_id={"aud_l": 1, "aud_r": 2, "vis_l": 3, "vis_r": 4},  # event names
        tmin=-0.2,
        tmax=1.0,
        baseline=(-0.2, 0),
        reject=dict(mag=4e-12, grad=3000e-13),  # reject epochs with too large signals
        preload=True,
    )

    # Save epochs.
    epochs.save(f"./data/processed/{subject}/{subject}_epo.fif", overwrite=True)

    # Calculate and save evoked responses for each experimental condition.
    evokeds = [
        epochs["aud_l"].average(),
        epochs["aud_r"].average(),
        epochs["vis_l"].average(),
        epochs["vis_r"].average(),
    ]

    # Save evoked responses
    mne.write_evokeds(
        f"./data/processed/{subject}/{subject}_ave.fif", evokeds, overwrite=True
    )
