"""
Segment the MRI using Freesurfer.

This takes a pretty long time (hours!).

Make sure that Freesurfer is properly configured before running this script:

module load freesurfer
source /work/modules/Ubuntu/20.04/amd64/t314/freesurfer/7.3.2/FreeSurferEnv.sh
"""

import os
import subprocess

import mne.bem

# Where to store the FreeSurfer output
os.environ["SUBJECTS_DIR"] = "./data/freesurfer"

# Make sure the SUBJECTS_DIR exists.
os.makedirs("./data/freesurfer", exist_ok=True)

for subject in ["sub01", "sub02"]:
    print("Running FreeSurfer on subject:", subject)

    # fmt: off
    subprocess.run(
        args = [
            "recon-all", "-all",
            "-s", subject,
            "-i", f"./data/orig/mri/{subject}.mgz",
        ]
    )
    # fmt: on

    # Set up MRI-images for analysis with MNE-python>
    mne.bem.make_watershed_bem(subject, overwrite=True)

    # Produce high-resolution head surface.
    # fmt: off
    subprocess.run(
        args=[
            "mne", "make_scalp_surfaces",
            "-s", subject,
            "--overwrite",
            "--force"
        ]
    )
    # fmt: on
