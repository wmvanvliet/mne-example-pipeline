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

fname.fill_placeholder("subject", subject)
fname.fill_placeholder("session", session)
fname.fill_placeholder("task", task)
fname.fill_placeholder("run", run)

print("Run tSSS on subject:", subject)
print("Session:", session)
print("Task:", task)
print("Run:", run)

# Use the manually pre-selected bad channels in the config file.
# Alternatively, we can use automatic detection of bad channels.
current_bads = config.bad_channels.query(
    f"subject=={subject} and session=={session} and task=='{task}' and run=={run}"
).channels.tolist()

if config.use_megin_maxfilter:
    # Args to be used in maxfilter
    # fmt: off
    # ruff: disable[E501]
    subprocess.run(
        args = [
            "maxfilter",

            # Input file.
            "-f", fname.raw(proc="raw"),

            # Output file.
            "-o", fname.raw(proc="tsss"),

            # Virtually move the head position to the location in this file.
            "-trans",
            fname.raw(session=1, run=1, proc="raw"),

            # Write the continuous head position to a file.
            "-hp", fname.pos(),

            # Uncomment this to enable continuous head movement compensation.
            # "-movecomp", "inter",

            "-st", "60",
            "-v",
            "-hpicons",
            "-origin", "fit",
            "-frame", "head",
            "-in", "8",
            "-out", "3",

            # Site-specific calibration files.
            "-cal", fname.calibration(),
            "-ctc", fname.crosstalk(),

            # Whether to use manually pre-selected bad channels or automatic detection.
            "-autobad", "off",  # alternatively: "-autobad", "on"
            "-bad",  # value will be the `current_bads` below
        ] + [f"'{ch}'" for ch in current_bads]  # wrap the channel names in ' ' quotes.
    )
    # fmt: on
    # ruff: enable[E501]
else:
    # Use MNE-Python's maxfilter implementation.
    raw = mne.io.read_raw(fname.raw(proc="raw"))

    # Set bad channels so maxfilter can ignore them.
    raw.info["bads"] = current_bads

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
        head_pos=head_pos,
        st_duration=min(60, int(raw.duration)),
        destination=fname.raw(session=1, run=1, proc="raw"),
        calibration=fname.calibration(),
        cross_talk=fname.crosstalk(),
    )
    raw_tsss.save(fname.raw(proc="tsss"), overwrite=True)

# Write figures to the HTML report
with mne.open_report(fname.report()) as report:
    if config.use_megin_maxfilter:
        # If we used MNE-Python's maxfilter, these are already loaded,
        # but when using MEGIn's maxfilter, we need to load them now.
        raw = mne.io.read_raw(fname.raw(proc="raw"))
        raw_tsss = mne.io.read_raw(fname.raw(proc="tsss"))
    report.add_raw(
        raw,
        title=f"Original data ses-{session:02d} task-{task} run-{run:02d}",
        replace=True,
    )
    report.add_raw(
        raw_tsss,
        title=f"After maxfilter ses-{session:02d} task-{task} run-{run:02d}",
        replace=True,
    )
    report.save(fname.report_html(), open_browser=False, overwrite=True)
