# -*- coding: utf-8 -*-
"""

Create epochs and evoked responses from your raw data
Currently, this version uses PCA to remove blinks and artefacts

You can also apply ICA here: create an ICA decomposition that identifies 
artefacts before running this code and change ica to True


"""
import argparse
import mne
import os
import numpy as np

from config import (fname, proc, reject)


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', help='The subject to process')
parser.add_argument('-ses', help='The session to process. ')
parser.add_argument('-task', help='The task to process. ')
args = parser.parse_args()
subject = args.subject
ses = args.ses
task = args.task

print('Processing subject: ', subject)
print('Processing session: ', ses)
print('Processing task: ', task)

# The current example uses PCA/SSP to remove eye blinks and heartbeat artefacts. This is good in the piloting stage.
# In the final pipeline, you may want to use ica to remove artefacts. Change ica to True to switch to a (precomputed) ica solution.
ica=False # UPDATE ME ONCE ICA IS IMPLEMENTED


if task=='audvis':
    from settings_sample import (bandpass_fmin, bandpass_fmax, runs, event_ids,  epoch_tmin, epoch_tmax, conditions, baseline)
#elif task=='xxxxx': # other tasks in your experiment
#    from settings_xxxx import (bandpass_fmin, bandpass_fmax, runs, event_ids, epoch_tmin, epoch_tmax, conditions, baseline)
else:
    print('Undefined task')


raws = list()
for run in runs:
    # Read the raw data
    print('Processing run: ', run)

    raw = mne.io.read_raw_fif(fname.raw(subject=subject,
                                        ses=ses,
                                        task=task,
                                        run=run,
                                        proc=proc, 
                                        preload = True))
    raw.load_data()
    raws.append(raw)

# Concatenate raw data, check that data has been transformed to the same position
raw=mne.concatenate_raws(raws)
#delete to save memory
del raws


#################################################
# Remove artefacts, currently using PCA/SSP. You will probably want to change this to ICA (set ica to True)
if ica==False:
    projs_ecg, _ = mne.preprocessing.compute_proj_ecg(raw, n_grad=2, n_mag=2, no_proj = True)
    # change n_grad and n_mag to 2 if you want to remove more than 1 eye movement component
    projs_eog, _ = mne.preprocessing.compute_proj_eog(raw, n_grad=1, n_mag=1, no_proj = True, reject = None)

    raw.add_proj(projs_ecg, remove_existing=False)    
    raw.add_proj(projs_eog, remove_existing=False) 

    raw.apply_proj()
#################################################

# Filter
raw.filter(bandpass_fmin, bandpass_fmax) # check default filtering
raw.notch_filter(freqs=np.arange(50, 251, 50))

# Get epochs and average
events =  mne.find_events(raw, min_duration = 2/raw.info['sfreq'])
epochs = mne.Epochs(raw, events, event_ids, epoch_tmin, epoch_tmax, baseline = baseline, 
                    preload=True, reject=reject, proj=False) 


# Apply precomputed ICA, choose filename according to your config file
if ica==True:
    ica= mne.preprocessing.read_ica(fname.ica(subject=subject, method='infomax', ses=ses, task=task))

    ica.apply(epochs, exclude=ica.exclude)

# Save epochs
if not os.path.exists(fname.megprocessed_dir(subject=subject, ses=ses) + 'epochs/'):    
    os.makedirs(fname.megprocessed_dir(subject=subject,ses=ses) + 'epochs/')
epochs.save(fname.epochs(subject=subject,ses=ses,task=task),overwrite=True)
     
# Calculate and save evoked responses
if not os.path.exists(fname.megprocessed_dir(subject=subject, ses=ses) + 'evoked/'):    
    os.makedirs(fname.megprocessed_dir(subject=subject,ses=ses) + 'evoked/')
    
evokeds=list()
for cond in conditions:
    evoked = epochs[cond].average()
    evokeds.append(evoked)

# Save evoked responses 
mne.write_evokeds(fname.evoked(subject=subject,ses=ses,task=task),evokeds)

