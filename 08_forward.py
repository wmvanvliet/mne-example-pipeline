"""Setup the source space and compute the forward solution."""

import argparse

import mne

import config
from config import fname

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-sub", required=True, type=int, help="The subject to process")
args = parser.parse_args()

subject = args.sub
fname.fill_placeholder("subject", subject)
# Convert the number into the corresponding FreeSurfer subject: 1 -> sub-01
freesurfer_subject = f"sub-{subject:02d}"
print("Computing forward solution for subject: ", subject)

# Setup source space.
src = mne.setup_source_space(
    subject=freesurfer_subject,
    spacing=config.spacing,
    subjects_dir=fname.subjects_dir,
    n_jobs=config.n_jobs,
    add_dist=True,
)
mne.write_source_spaces(fname.src(), src, overwrite=True)

# Create BEM model
bem = mne.make_bem_model(
    subject=freesurfer_subject,
    ico=4 if config.spacing in ("ico4", "oct5") else 5,
    subjects_dir=fname.subjects_dir,
    conductivity=(0.3,),  # one-layer model, use (0.3, 0.006, 0.3) for three layers
)
bem_sol = mne.make_bem_solution(bem)
mne.write_bem_solution(fname.bem_sol(), bem_sol, overwrite=True)

# Add a figure of the BEM to the HTML report
with mne.open_report(fname.report()) as report:
    report.add_bem(subject=freesurfer_subject, title="BEM", replace=True)

for session in config.sessions:
    print("Processing session: ", session)
    for task in config.tasks:
        print("Processing task: ", task)

        # Create the forward model, co-registration required (trans_file)
        # Use first run in one of the tasks for forward model
        info = mne.io.read_info(
            fname.raw(session=session, task=task, run=1, proc="tsss")
        )
        fwd = mne.make_forward_solution(
            info,
            trans=fname.trans(session=session),
            src=src,
            bem=bem_sol,
            meg=True,
            eeg=False,  # turn this on for a combined MEG+EEG head model
            mindist=0,
            n_jobs=config.n_jobs,
        )
        mne.write_forward_solution(
            fname.fwd(session=session, task=task),
            fwd,
            overwrite=True,
        )

    # Add a figure of the head model to the HTML report
    with mne.open_report(fname.report()) as report:
        report.add_trans(
            fname.trans(session=session),
            info=info,
            subject=freesurfer_subject,
            plot_kwargs=dict(src=src),
            title=f"Head model: ses-{session:02d}",
            replace=True,
        )

report.save(fname.report_html(), open_browser=False, overwrite=True)
