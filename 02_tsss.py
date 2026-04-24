"""
Maxfilter the raw MEG data

Using the GUI instead to maxfilter your data is in many ways still
recommended and helps with troubleshooting.

On Aalto machines, you first need to run "module load neuromag" to enable the maxfilter
program.

TODO: Update defaults to BioMag standard parameters.
"""

import argparse
import subprocess
import sys

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

subject, session, task, run = args.sub, args.ses, args.task, args.run
print("Run tSSS on subject:", subject)
print("Session:", session)
print("Task:", task)
print("Run:", run)

if not config.enable_maxfilter:
    print("Maxfilter disabled. Nothing to be done.")
    sys.exit(0)

# Use the manually pre-selected bad channels in the config file.
# Alternatively, we can use automatic detection of bad channels.
current_bads = config.bad_channels.query(
    f"subject=={subject} and session=={session} and task=='{task}' and run=={run}"
).channels.tolist()

if config.use_megin_maxfilter:
    # Args to be used in maxfilter
    # fmt: off
    # ruff: disable[E501]
    args = [
        "maxfilter",

        # Input file.
        "-f", fname.raw(subject=subject, session=session, task=task, run=run, proc="raw"),

        # Output file.
        "-o", fname.raw(subject=subject, session=session, task=task, run=run, proc="tsss"),

        # Uncomment this to enable continuous head movement compensation.
        # "-movecomp", "inter",

        "-v",
        "-in", "8",
        "-out", "3",

        # Site-specific calibration files.
        "-cal", fname.calibration(subject=subject, session=session),
        "-ctc", fname.crosstalk(subject=subject, session=session),

        # Whether to use manually pre-selected bad channels or automatic detection.
        "-autobad", "off",  # alternatively: "-autobad", "on"
        "-bad",  # value will be the `current_bads` below
    ] + current_bads

    if task != "emptyroom":
        args.extend([
            # Virtually move the head position to the location in this file.
            "-trans",
            fname.raw(subject=subject, session=1, task=task, run=1, proc="raw"),

            # Write the continuous head position to a file.
            "-hp", fname.pos(subject=subject, session=session, task=task, run=run),

            "-frame", "head",
            "-st", "60",
            "-hpicons",
            "-origin", "fit",

        ])

    subprocess.run(args)
else:
    # Use MNE-Python's maxfilter implementation.
    raw = mne.io.read_raw(
        fname.raw(subject=subject, session=session, task=task, run=run, proc="raw")
    )

    # Set bad channels so maxfilter can ignore them.
    raw.info["bads"] = current_bads

    if task == "emptyroom":
        coord_frame = "meg"
        st_duration = None
        destination = None
        head_pos = None
    else:
        coord_frame = "head"
        st_duration = min(60, int(raw.duration))
        destination = fname.raw(
            subject=subject, session=1, task=task, run=1, proc="raw"
        )
        # Compute head position from the cHPI channels.
        try:
            chpi_amps = mne.chpi.compute_chpi_amplitudes(raw)
            chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amps)
            head_pos = mne.chpi.compute_head_pos(raw.info, chpi_locs)
        except ValueError:
            head_pos = None

    # Perform the maxfilter.
    raw_tsss = mne.preprocessing.maxwell_filter(
        raw,
        coord_frame=coord_frame,
        head_pos=head_pos,
        destination=destination,
        st_duration=st_duration,
        calibration=fname.calibration(subject=subject, session=session),
        cross_talk=fname.crosstalk(subject=subject, session=session),
    )
    raw_tsss.save(
        fname.raw(subject=subject, session=session, task=task, run=run, proc="tsss"),
        overwrite=True,
    )
# fmt: on
# ruff: enable[E501]
