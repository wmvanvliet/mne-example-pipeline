"""
Maxfilter the raw MEG data

Using the GUI instead to maxfilter your data is in many ways still
recommended and helps with troubleshooting.

On Aalto machines, you first need to run "module load neuromag" to enable the maxfilter
program.

TODO: Update defaults to BioMag standard parameters.
"""

import os
import subprocess

for subject in ["sub01", "sub02"]:
    print("Run tSSS on subject:", subject)

    # Make sure the output folder exists.
    os.makedirs(f"./data/processed/{subject}", exist_ok=True)

    # Use manually pre-selected bad channels.
    if subject == "sub01":
        bad_channels = "'MEG 2443' 'EEG 053'"
    elif subject == "sub02":
        bad_channels = "'MEG 2443' 'EEG 053'"

    # Args to be used in maxfilter
    # fmt: off
    # ruff: disable[E501]
    subprocess.run(
        args = [
            "maxfilter",

            # Input file.
            "-f", f"./data/orig/meg/{subject}_raw.fif",

            # Output file.
            "-o", f"./data/processed/{subject}/{subject}_tsss_raw.fif",

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
            "-cal", "./data/orig/sss_cal_biomag_triux.dat",
            "-ctc", "./data/orig/ct_sparse_biomag_triux.fif",

            # Whether to use manually pre-selected bad channels or automatic detection.
            "-autobad", "off",  # alternatively: "-autobad", "on"
            "-bad", bad_channels
        ]
    )
    # fmt: on
    # ruff: enable[E501]
