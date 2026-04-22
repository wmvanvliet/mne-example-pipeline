"""Setup the source space and compute the forward solution."""

import os
import argparse

import mne

import config
from config import fname, spacing

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
args = parser.parse_args()

subject = args.sub
# Convert the number into the corresponding FreeSurfer subject: 1 -> sub-01
freesurfer_subject = f"sub-{subject:02d}"

print("Computing forward solution for subject: ", subject)

# Setup souce space.
src = mne.setup_source_space(
    subject=subject,
    spacing=spacing,
    subjects_dir=fname.subjects_dir,
    n_jobs=-1,
    add_dist=True,
)
mne.write_source_spaces(
    fname.src(subject=subject, spacing=spacing), src, overwrite=True
)

# Create BEM model
bem = mne.make_bem_model(
    subject=freesurfer_subject,
    ico=4 if spacing == "ico4" else 5,
    subjects_dir=fname.subjects_dir,
    conductivity=(0.3,),
)
bem_sol = mne.make_bem_solution(bem)
mne.write_bem_solution(fname.bem_sol(subject=subject), bem_sol, overwrite=True)

for session in config.sessions:
    print("Processing session: ", session)
    for task in config.tasks:
        print("Processing task: ", task)

        # Create the forward model, coregistration required (trans_file)
        # Use first run in one of the tasks for forward model
        info = mne.io.read_info(
            fname.raw(subject=subject, session=session, task=task, run=1)
        )
        fwd = mne.make_forward_solution(
            info,
            trans=fname.trans(subject=subject, session=session),
            src=src,
            bem=bem_sol,
            meg=True,
            eeg=False,
            mindist=0,
            n_jobs=-1,
        )
        mne.write_forward_solution(
            fname.fwd(subject=subject, session=session, task=task, spacing=spacing),
            fwd,
            overwrite=True,
        )
