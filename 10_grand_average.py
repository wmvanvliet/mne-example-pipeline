"""
Compute average of the power maps of morphed source estimates.
"""

import mne
import numpy as np

import config
from config import fname

for task in config.tasks:
    print("Processing task:", task)

    for session in config.sessions:
        print("Processing session:", session)
        ga_evokeds = list()
        for condition in config.conditions.keys():
            print("Processing condition:", condition)

            evokeds = list()
            stcs = list()
            for subject in config.subjects:
                print("Reading subject:", subject)
                evoked = mne.read_evokeds(
                    fname.evokeds(subject=subject, session=session, task=task),
                    condition=condition,
                )
                evokeds.append(evoked)
                stc_fsaverage = mne.read_source_estimate(
                    fname.stc_morphed(
                        subject=subject, session=session, task=task, condition=condition
                    )
                )
                stcs.append(stc_fsaverage)

            # Average evokeds across subjects.
            ga_ev = mne.grand_average(evokeds)
            ga_ev.comment = condition
            ga_evokeds.append(ga_ev)

            # Average STCs across subjects.
            ga_stc = np.mean(stcs)
            ga_stc.save(
                fname.ga_stc(session=session, task=task, condition=condition),
                overwrite=True,
            )

            # Add a figure of the source estimate to the HTML report.
            with mne.open_report(fname.ga_report) as report:
                report.add_stc(
                    ga_stc,
                    subject="fsaverage",
                    title=f"STC: ses-{session:02d} cond-{condition}",
                    replace=True,
                )

        mne.write_evokeds(
            fname.ga_evokeds(session=session, task=task), ga_evokeds, overwrite=True
        )

        # Add a figure of the evokeds to the HTML report.
        with mne.open_report(fname.ga_report) as report:
            fig = mne.viz.plot_evoked_topo(ga_evokeds, show=False)
            fig.set_size_inches((20, 20))
            report.add_figure(fig, title=f"Evokeds: ses-{session:02d}", replace=True)

report.save(fname.ga_report_html, open_browser=False, overwrite=True)
