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
args = parser.parse_args()

subject = args.sub
session = args.ses
task = args.task

fname.fill_placeholder("subject", subject)
fname.fill_placeholder("session", session)
fname.fill_placeholder("task", task)

print("Run ICA on subject:", subject)
print("Session:", session)
print("Task:", task)

if config.enable_maxfilter:
    proc = "tsss"
else:
    proc = "raw"

# Concatenate across all the runs.
raws = list()
for run in config.runs_per_task[task]:
    # Do not pre-load the data into memory. We will load the data after concatenation.
    raws.append(mne.io.read_raw(fname.raw(run=run, proc=proc), preload=False))
raw = mne.concatenate_raws(raws).load_data()

# First bandpass filter the data with a lower bound of 1 Hz. This ensures the data is
# reasonably centered around zero at all times. Note that the lower bound of 1 Hz. is
# only used for fitting the ICA, we use a different filter for the analysis of evoked
# responses.
raw.filter(1, config.bandpass[1], n_jobs=config.n_jobs)

# Obtain the mixing and unmixing matrices of the Independant Component Analysis.
ica = mne.preprocessing.ICA(
    n_components=0.95 if config.enable_maxfilter else 0.9,
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
# channel. We can create a "virtual" one, but this has to be done on the non-tSSS data,
# as the tSSS algorithm will have removed much of the heartbeat.
if not config.enable_maxfilter:
    # tSSS processing was disabled already.
    raw_non_tsss = raw
else:
    # Read non-tSSS processed data.
    raw_non_tsss = mne.concatenate_raws(
        [
            mne.io.read_raw(fname.raw(run=run, proc="raw"), preload=False)
            for run in config.runs_per_task[task]
        ]
    ).load_data()
# Find the onsets of the heartbeats on the non-tSSS data, then cut epochs around them
# on the tSSS data.
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
ica.save(fname.ica, overwrite=True)

# Write figures to the HTML report
with mne.open_report(fname.report) as report:
    report.add_ica(
        ica,
        title=f"ICA ses-{session:02d} task-{task}",
        inst=raw,
        picks=ica.exclude,
        eog_scores=eog_scores,
        ecg_scores=ecg_scores,
        replace=True,
    )
    report.save(fname.report_html, open_browser=False, overwrite=True)
