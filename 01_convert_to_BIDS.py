"""
Convert the original data to the BIDS format.
"""

import mne
import mne_bids

import config
from config import fname

# In this experiment, we only have a single task.
# If you have more tasks, you can create another loop over them.
task = "audvis"

# Loop over all subjects, sessions, and runs.
for subject in config.subjects:
    for session in config.sessions:
        for run in config.runs_per_task[task]:  # each task can have different runs
            # By setting preload=False, we only read the information about the recording
            # (sensors, samplerate, etc.) and not the actual MEG data. This saves a lot
            # of time.
            raw = mne.io.read_raw(
                fname.orig_meg(subject=subject, session=session, run=run), preload=False
            )
            events = mne.find_events(raw, min_duration=0.002)

            # In BIDS filenames, it is common to add leading zeros to `subject`,
            # `session`, and `run`. So instead of 1, we use "01".
            # This conversion is done below using Python's "f-strings" functionality.
            # For example: `:02d` means to add zeros until the string has a length of 2.
            bids_path = mne_bids.BIDSPath(
                subject=f"{subject:02d}",
                session=f"{session:02d}",
                task=task,
                run=f"{run:02d}",
                processing="raw",
                root=fname.bids_path,
            )

            mne_bids.write_raw_bids(
                raw,
                bids_path,
                events=events,
                event_id=config.event_id,
                overwrite=True,
            )

            # Write the fine calibration and crosstalk information of the scanner.
            mne_bids.write_meg_calibration(fname.orig_calibration, bids_path)
            mne_bids.write_meg_crosstalk(fname.orig_crosstalk, bids_path)

# Convert anatomical MRIs to BIDS.
for subject in config.subjects:
    bids_path = mne_bids.BIDSPath(
        subject=f"{subject:02d}",
        root=fname.bids_path,
    )
    mne_bids.write_anat(fname.orig_mri(subject=subject), bids_path, overwrite=True)

print("Done! Here are all the files that were produced:")
mne_bids.print_dir_tree(fname.bids_path)
