"""
Use Independant Component Analysis to remove eye (EOG) and heart (ECG) artifacts.

# Note: Automatic selection of ICA components does not work very well.
# CHECK EVERY SUBJECT MANUALLY!
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
parser.add_argument("-run", required=True, type=int, help="The run to process")
args = parser.parse_args()

subject = args.sub
session = args.ses
task = args.task
run = args.run
print("Run ICA on subject:", subject)
print("Session:", session)
print("Task:", task)
print("Run:", run)

raw = mne.io.read_raw(
    fname.raw(subject=subject, session=session, task=task, run=run, proc=config.proc),
    preload=True,
)

# First bandpass filter the data with a lower bound of 1 Hz. This ensures the data is
# reasonably centered around zero at all times. Note that the lower bound of 1 Hz. is
# only used for fitting the ICA, we use a different filter for the analysis of evoked
# responses.
raw.filter(1, config.bandpass[1])

# Obtain the mixing and unmixing matrices of the Independant Component Analysis.
ica = mne.preprocessing.ICA(
    n_components=0.95,
    method="picard",
    fit_params=dict(extended=True),
    random_state=0,  # this is important to produce the exact same solution every time
)
ica.fit(raw, decim=3)  # decim=3 means "take every 3rd sample", to speed things up

# Compute the correlation between each ICA component and the EOG channels.
# Flag any component with a correlation more than 0.2 as "bad".
eog_bads, eog_scores = ica.find_bads_eog(
    raw, threshold=config.reject_eog_correlation, measure="correlation"
)

# Do the same with the ECG channels. However, this example data does not have an ECG
# channel. We can create a "virtual" one, but this has to be done on the non-TSSS data,
# as the TSSS algorithm will have removed much of the heartbeat.
if config.proc == "raw":
    # TSSS processing was disabled already.
    raw_non_tsss = raw
else:
    # Read non-TSSS processed data.
    raw_non_tsss = mne.io.read_raw(
        fname.raw(subject=subject, session=session, task=task, run=run, proc="raw")
    )
# Find the onsets of the heartbeats on the non-TSSS data, then cut epochs around them
# on the TSSS data.
ecg_events = mne.preprocessing.find_ecg_events(raw_non_tsss)[0]
ecg_epochs = mne.Epochs(raw, ecg_events, tmin=-0.2, tmax=0.5, preload=True)
ecg_bads, ecg_scores = ica.find_bads_ecg(
    ecg_epochs, threshold=config.reject_ecg_correlation, measure="correlation"
)

# If you have an ECG channel, things are easier and you can just do this:
# ecg_bads, ecg_scores = ica.find_bads_ecg(
#     raw, threshold=config.reject_ecg_correlation, measure="correlation"
# )

# If you have EMG channels, you can also flag components that correlate with those:
# emg_bads, emg_scores = ica.find_bads_emg(
#     raw, threshold=config.reject_emg_correlation, measure="correlation"
# )

# Inform the ICA object of which components we wish to exclude.
# If you have any `emg_bads`, don't forget to add them.
ica.exclude = eog_bads + ecg_bads

# Save the ICA solution.
ica.save(
    fname.ica(subject=subject, session=session, task=task, run=run), overwrite=True
)
