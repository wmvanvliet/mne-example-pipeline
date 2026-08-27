"""Compute statistics."""

import mne
import pandas as pd

import config
from config import fname

metadata = list()
for task in config.tasks:
    print("Processing task:", task)
    for session in config.sessions:
        print("Processing session:", session)
        for condition in config.conditions.keys():
            print("Processing condition:", condition)
            for subject in config.subjects:
                print("Reading subject:", subject)
                evoked = mne.read_evokeds(
                    fname.evokeds(subject=subject, session=session, task=task),
                    condition=condition,
                )
                metadata.append(
                    dict(
                        evoked=evoked,
                        task=task,
                        session=session,
                        condition=condition,
                        subject=subject,
                    )
                )
df = pd.DataFrame(metadata)
print(df)

results_session = mne.stats.cluster_test(
    df, "evoked ~ condition", within_id="subject", n_jobs=-1
)
print(results_session)
