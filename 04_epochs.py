"""
Create epochs and evoked responses from your raw data.
We concanenate epochs across runs.
"""

import argparse
import os

import mne
import numpy as np

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
print("Cut epochs for subject:", subject)
print("Session:", session)
print("Task:", task)

raws = list()
for run in config.runs_per_task[task]:
    # Read the tSSS-filtered data and clean it with the ICA computed during the previous
    # step.
    print("Processing run: ", run)
    raw = mne.io.read_raw(
        fname.raw(
            subject=subject,
            session=session,
            task=task,
            run=run,
            proc=config.proc,
        ),
        preload=True,
    )

    # Clean the data. First by bandpass filtering, then by applying the ICA to it.
    raw.filter(*config.bandpass)
    ica = mne.preprocessing.read_ica(
        fname.ica(subject=subject, session=session, task=task, run=run)
    )

    # Collect the `raw` objects from all the runs into a list.
    raws.append(ica.apply(raw))

# Concatenate raw data across runs. This only works if the data has been transformed to
# the same head position during the maxfilter step.
raw = mne.concatenate_raws(raws)

# Delete this to save memory.
del raws

# Get epochs and average
events = mne.find_events(raw, min_duration=2 / raw.info["sfreq"])
epochs = mne.Epochs(
    raw,
    events,
    config.event_id,
    tmin=-0.2,
    tmax=1.0,
    baseline=config.baseline,
    reject=config.reject_epochs,
    preload=True,
)

# Save epochs.
epochs.save(fname.epochs(subject=subject, session=session, task=task), overwrite=True)

# Calculate and save evoked responses for each experimental codition.
evokeds = list()
for cond, event in config.conditions.items():
    evoked = epochs[event].average()
    evoked.comment = cond
    evokeds.append(evoked)

# Save evoked responses
mne.write_evokeds(
    fname.evokeds(subject=subject, session=session, task=task), evokeds, overwrite=True
)
