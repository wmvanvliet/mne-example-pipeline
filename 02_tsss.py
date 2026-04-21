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

import config
from config import fname

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
parser.add_argument("-ses", required=True, type=int, help="The session to process")
parser.add_argument(
    "-task", required=False, default="audvis", help="The task to process"
)
parser.add_argument("-run", required=True, type=int, help="The run to process")
args = parser.parse_args()

subject = args.sub
session = args.ses
task = args.task
run = args.run

print("Run tSSS on subject:", subject)
print("Running session:", session)
print("Running task:", task)
print("Running run:", run)

# Use the manually pre-selected bad channels in the config file.
# Alternatively, we can use automatic detection of bad channels.
current_bads = config.bad_channels.query(
    f"subject=={subject} and session=={session} and task=='{task}' and run=={run}"
).channels.tolist()

# Args to be used in maxfilter
# fmt: off
maxfilter_args = [
    "maxfilter",

    # The site where the data was recorded (biomag, Aalto_TRIUXneo)
    "-site", "biomag",

    # Input file.
    "-f", fname.raw(subject=subject, session=session, task=task, run=run),

    # Output file.
    "-o", fname.raw_tsss(subject=subject, session=session, task=task, run=run),

    # Virtually move the head position within the helmet to the location in this file.
    "-trans", fname.raw(subject=subject, session=1, task=task, run=1),

    # Write the continuous head position to a file.
    "-hp", fname.pos(subject=subject, session=session, task=task, run=run),

    # Uncomment this to enable continuous head movement compensation.
    # "-movecomp", "inter",

    "-st", "60",
    "-v",
    "-hpicons",
    "-origin", "fit",
    "-frame", "head",
    "-in", "8",
    "-out", "3",

    # Whether to use manually pre-selected bad channels or automatic detection.
    "-autobad", "off",  # alternatively: "-autobad", "on"
    "-bad",  # value will be the `current_bads` below
] + current_bads
# fmt: on

# Save the log and errors produced by the maxfilter program to this file.
log_output = open(
    fname.tsss_log(subject=subject, run=run, session=session, task=task), "w"
)

# Run maxfilter.
subprocess.run(args=maxfilter_args, stdout=log_output, stderr=log_output)
