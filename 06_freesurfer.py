"""
Segment the MRI using Freesurfer.

This takes a pretty long time (hours!).

Make sure that Freesurfer is properly configured before running this script:

module load freesurfer
source /work/modules/Ubuntu/20.04/amd64/t314/freesurfer/7.3.2/FreeSurferEnv.sh
"""

import argparse
import subprocess

import mne

from config import fname

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
args = parser.parse_args()

subject = args.sub
# Convert the number into the corresponding FreeSurfer subject: 1 -> sub-01
freesurfer_subject = f"sub-{subject:02d}"
print("Running FreeSurfer on subject:", subject)

# fmt: off
subprocess.run(
    args = [
        "recon-all", "-all",
        "-s", freesurfer_subject,
        "-sd", fname.subjects_dir,
        "-i", fname.mri(subject=subject),
        "-openmp", "X",  # use all available CPUs
    ]
)
# fmt: on

# Set up MRI-images for analysis with MNE-python
mne.bem.make_watershed_bem(freesurfer_subject, overwrite=True)

# High-resolution surfaces
# fmt: off
subprocess.run(
    args=[
        "mne", "make_scalp_surfaces",
        "-s", freesurfer_subject,
        "-sd", fname.subjects_dir,
        "--overwrite",
        "--force"
    ]
)
# fmt: on
