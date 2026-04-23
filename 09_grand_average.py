"""
Compute average of the power maps of morphed source estimates.
"""

import os

import mne
import numpy as np

# Make sure the GA folder exists.
os.makedirs("./data/processed/GA", exist_ok=True)

ga_evokeds = list()
for condition in ["aud_l", "aud_r", "vis_l", "vis_r"]:
    evokeds = list()
    stcs = list()
    for subject in ["sub01", "sub02"]:
        evoked = mne.read_evokeds(
            f"./data/processed/{subject}/{subject}_ave.fif", condition=condition
        )
        evokeds.append(evoked)
        stc_fsaverage = mne.read_source_estimate(
            f"./data/processed/{subject}/{subject}_{condition}_morphed_stc"
        )
        stcs.append(stc_fsaverage)

        # Average evokeds across subjects.
        ga_ev = mne.grand_average(evokeds)
        ga_ev.comment = condition
        ga_evokeds.append(ga_ev)

        # Average STCs across subjects.
        ga_stc = np.mean(stcs)
        ga_stc.save(f"./data/processed/GA/GA_{condition}_stc", overwrite=True)

mne.write_evokeds("./data/processed/GA/GA_ave.fif", ga_evokeds)
