"""
Use Independant Component Analysis to remove eye (EOG) and heart (ECG) artifacts.

# Note: Automatic selection of ICA components does not work very well.
# CHECK EVERY SUBJECT MANUALLY!
"""

import mne

for subject in ["sub01", "sub02"]:
    raw = mne.io.read_raw(
        f"./data/processed/{subject}/{subject}_tsss_raw.fif", preload=True
    )

    # First bandpass filter the data with a lower bound of 1 Hz. This ensures the data
    # is reasonably centered around zero at all times. Note that the lower bound of 1
    # Hz. is only used for fitting the ICA, we use a different filter for the analysis
    # of evoked responses.
    raw.filter(1, 40)

    # Obtain the mixing and unmixing matrices of the Independant Component Analysis.
    ica = mne.preprocessing.ICA(
        n_components=0.95,
        method="picard",
        fit_params=dict(extended=True),
        random_state=0,  # this is important to produce the same solution every time
    )
    ica.fit(raw, decim=3)  # decim=3 means "take every 3rd sample", to speed things up

    # Compute the correlation between each ICA component and the EOG channels.
    # Flag any component with a correlation more than 0.2 as "bad".
    eog_bads, eog_scores = ica.find_bads_eog(raw, threshold=0.2, measure="correlation")

    # Do the same with the ECG channels. However, this example data does not have an ECG
    # channel. We can create a "virtual" one, but this has to be done on the non-TSSS
    # data, as the TSSS algorithm will have removed much of the heartbeat.
    raw_non_tsss = mne.io.read_raw(f"./data/orig/meg/{subject}_raw.fif")
    # Find the onsets of the heartbeats on the non-TSSS data, then cut epochs around
    # them on the TSSS data.
    ecg_events = mne.preprocessing.find_ecg_events(raw_non_tsss)[0]
    ecg_epochs = mne.Epochs(raw, ecg_events, tmin=-0.2, tmax=0.5, preload=True)
    ecg_bads, ecg_scores = ica.find_bads_ecg(
        ecg_epochs, threshold=0.5, measure="correlation"
    )

    # If you have an ECG channel, things are easier and you can just do this:
    # ecg_bads, ecg_scores = ica.find_bads_ecg(
    #     raw, threshold=0.5, measure="correlation"
    # )

    # If you have EMG channels, you can also flag components that correlate with those:
    # emg_bads, emg_scores = ica.find_bads_emg(
    #     raw, threshold=0.2, measure="correlation"
    # )

    # Inform the ICA object of which components we wish to exclude.
    # If you have any `emg_bads`, don't forget to add them.
    ica.exclude = eog_bads + ecg_bads

    # Save the ICA solution.
    ica.save(f"./data/processed/{subject}/{subject}_ica.fif", overwrite=True)
