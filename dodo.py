"""
Do-it script to execute the entire pipeline using the doit tool:
http://pydoit.org

All the filenames are defined in config.py
"""
# fmt: off
# ruff:disable[E501]

import config
from config import conditions, fname, runs_per_task, sessions, subjects, tasks

# Configuration for the "doit" tool.
DOIT_CONFIG = dict(
    # While running scripts, output everything the script is printing to the
    # screen.
    verbosity=2,
    # When the user executes "doit list", list the tasks in the order they are
    # defined in this file, instead of alphabetically.
    sort="definition",
)

def task_check():
    """Step 00: Check the system for python dependencies and the presence of data."""
    return dict(
        file_dep=["check_system.py"],
        targets=[fname.system_check],
        actions=["python check_system.py"],
    )


def task_bids():
    """Step 01: Convert the original data to the BIDS format."""
    # If any of these files change, the script needs to be re-run. Make
    # sure that the script itself is part of this list!
    file_dep = list()

    # The files produced by the script
    targets = list()

    # This step consumes and produces a LOT of files!
    for sub in subjects:
        file_dep.append(fname.orig_mri(subject=sub))
        targets.append(fname.mri(subject=sub))
        for ses in sessions:
            targets.append(fname.calibration(subject=sub, session=ses))
            targets.append(fname.crosstalk(subject=sub, session=ses))
            for task in tasks:
                for run in runs_per_task[task]:
                    file_dep.append(fname.orig_meg(subject=sub, session=ses, task=task, run=run))
                    targets.append(fname.raw(subject=sub, session=ses, task=task, run=run, proc="raw"))
    file_dep.append(fname.orig_calibration)
    file_dep.append(fname.orig_crosstalk)
    file_dep.append("01_convert_to_BIDS.py")
    return dict(
        file_dep=file_dep,
        targets=targets,
        # How the script needs to be called.
        actions=["python 01_convert_to_BIDS.py"],
    )


def task_tsss():
    """Step 02: Run maxfilter™ on the data to perform tSSS filtering."""
    for sub in subjects:
        for ses in sessions:
            for task in tasks:
                for run in runs_per_task[task]:
                    yield dict(
                        # Give the sub-task a name.
                        name=f"sub-{sub:02d}:ses-{ses:02d}:task-{task}:run-{run:02d}",
                        file_dep=[
                            fname.raw(subject=sub, session=ses, task=task, run=run, proc="raw"),
                            fname.calibration(subject=sub, session=ses, task=task),
                            fname.crosstalk(subject=sub, session=ses, task=task),
                            "02_tsss.py",
                        ],
                        targets=[
                            fname.raw(subject=sub, session=ses, task=task, run=run, proc="tsss"),
                        ],
                        actions=[
                            f"python 02_tsss.py -sub={sub} -ses={ses} -task={task} -run={run}"
                        ],
                    )

def task_ica():
    """Step 03: Use ICA to remove eye blinks and heart beat."""
    for sub in subjects:
        for ses in sessions:
            for task in tasks:
                yield dict(
                    # Give the sub-task a name.
                    name=f"sub-{sub:02d}:ses-{ses:02d}:task-{task}",
                    file_dep=[
                        fname.raw(subject=sub, session=ses, task=task, run=run, proc="raw")
                        for run in runs_per_task[task]
                    ] + [
                        fname.raw(subject=sub, session=ses, task=task, run=run, proc="tsss")
                        for run in runs_per_task[task]
                    ] + [
                        "03_ica.py",
                    ],
                    targets=[
                        fname.ica(subject=sub, session=ses, task=task),
                    ],
                    actions=[
                        f"python 03_ica.py -sub={sub} -ses={ses} -task={task}"
                    ],
                )

def task_epochs():
    """Step 04: Create epochs and evoked responses."""
    for sub in subjects:
        for ses in sessions:
            for task in tasks:
                yield dict(
                    # Give the sub-task a name.
                    name=f"sub-{sub:02d}:ses-{ses:02d}:task-{task}",
                    file_dep=[
                        fname.raw(subject=sub, session=ses, task=task, run=run, proc="tsss" if config.enable_maxfilter else "raw")
                        for run in runs_per_task[task]
                    ] + [
                        fname.ica(subject=sub, session=ses, task=task, run=run)
                        for run in runs_per_task[task]
                    ] + [
                        "04_epochs.py",
                    ],
                    targets=[
                        fname.epochs(subject=sub, session=ses, task=task),
                        fname.evokeds(subject=sub, session=ses, task=task),
                    ],
                    actions=[
                        f"python 04_epochs.py -sub={sub} -ses={ses} -task={task}"
                    ],
                )

def task_noise_cov():
    """Step 05: Compute the noise covariance."""
    for sub in subjects:
        for ses in sessions:
            for task in tasks:
                yield dict(
                    # Give the sub-task a name.
                    name=f"sub-{sub:02d}:ses-{ses:02d}:task-{task}",
                    file_dep=[
                        fname.epochs(subject=sub, session=ses, task=task),
                        "05_noise_cov.py",
                    ],
                    targets=[
                        fname.noise_cov(subject=sub, session=ses, task=task),
                    ],
                    actions=[
                        f"python 05_noise_cov.py -sub={sub} -ses={ses} -task={task}"
                    ],
                )

def task_freesurfer():
    """Step 06: Run FreeSurfer segmentation of the MRIs."""
    for sub in subjects:
        yield dict(
            # Give the sub-task a name.
            name=f"sub-{sub:02d}",
            file_dep=[
                fname.mri(subject=sub),
                "06_freesurfer.py",
            ],
            targets=[
                fname.head_surf(subject=sub),
            ],
            actions=[f"python 06_freesurfer.py -sub {sub}"],
        )

def task_coreg():
    """Step 07: Co-register the MRI with the MEG."""
    for sub in subjects:
        for ses in sessions:
            yield dict(
                # Give the sub-task a name.
                name=f"sub-{sub:02d}:ses-{ses:02d}",
                file_dep=[
                    fname.head_surf(subject=sub),
                    fname.fid(subject=sub),
                    "07_coregistration.py",
                ],
                targets=[
                    fname.trans(subject=sub, session=ses),
                ],
                actions=[
                    f"python 07_coregistration.py -sub={sub} -ses={ses}"
                ],
            )

def task_forward():
    """Step 08: Compute the forward model."""
    for sub in subjects:
        yield dict(
            # Give the sub-task a name.
            name=f"sub-{sub:02d}",
            file_dep=[fname.trans(subject=sub, session=ses) for ses in sessions]
            + [
                fname.head_surf(subject=sub),
                "08_forward.py",
            ],
            targets=[
                fname.fwd(subject=sub, session=ses, task=task)
                for ses in sessions for task in tasks
            ] + [
                fname.src(subject=sub)
            ],
            actions=[
                f"python 08_forward.py -sub={sub}"
            ],
        )

def task_inverse():
    """Step 09: Compute the inverse (source estimates)."""
    for sub in subjects:
        for ses in sessions:
            for task in tasks:
                yield dict(
                    # Give the sub-task a name.
                    name=f"sub-{sub:02d}:ses-{ses:02d}:task-{task}",
                    file_dep=[
                        fname.fwd(subject=sub, session=ses, task=task),
                        "09_inverse.py",
                    ],
                    targets=[
                        fname.stc_hemi(subject=sub, session=ses, task=task, condition=cond, hemi=hemi)
                        for cond in conditions.keys() for hemi in ["lh", "rh"]
                    ] + [
                        fname.stc_morphed_hemi(subject=sub, session=ses, task=task, condition=cond, hemi=hemi)
                        for cond in conditions.keys() for hemi in ["lh", "rh"]
                    ] + [
                        fname.inv(subject=sub, session=ses, task=task),
                    ],
                    actions=[
                        f"python 09_inverse.py -sub={sub} -ses={ses} -task={task}"
                    ],
                )

def task_ga():
    """Step 10: Compute the grand-average across subjects."""
    return dict(
        file_dep= [
            fname.stc_morphed_hemi(subject=sub, session=ses, task=task, condition=cond, hemi=hemi)
            for sub in subjects
            for ses in sessions
            for task in tasks
            for cond in conditions
            for hemi in ["lh", "rh"]
        ] + [
            "10_grand_average.py",
        ],
        targets=[
            fname.ga_stc_hemi(session=ses, condition=cond, hemi=hemi)
            for ses in sessions for cond in conditions.keys() for hemi in ["lh", "rh"]
        ],
        actions=[
            "python 10_grand_average.py"
        ],
    )


# Finally we define some meta-tasks that run portions of the pipeline.
def task_sensor():
    """Run all sensor-level analysis steps."""
    return dict(
        actions=None,
        task_dep=["bids", "tsss", "ica", "epochs"],
    )

def task_source():
    """Run all source-level analysis steps."""
    return dict(
        actions=None,
        task_dep=["forward", "inverse", "ga"],
    )
