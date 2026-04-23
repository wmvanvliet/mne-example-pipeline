# Standard MNE source estimation pipeline

A standard pipeline for source localization of evoked responses using MNE. This is meant as a jumping-off point for your own data analysis pipeline.


## Getting started

#### 1. Have access to a scientific Python environment

To run this analysis pipeline, you need access to a Python enviroment with has the
MNE-Python package installed.

- On Triton, you can load one with: `module load neuroimaging-env`
- On Aalto workstations, you can load one with:
  `module load scibuilder-mamba-dev neuroimaging-env`  

#### 2. Have access to MegIn's maxfilter™ program and [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)

- On Triton, you can load them with: `module load maxfilter freesurfer`
- On Aalto workstations, you can load them with: `module load neuromag freesurfer`

Loading the FreeSurfer module will give some additional instructions for you, namely that you should execute `source` on a specific file.

#### 3. Create the example data

For this example pipeline, we take the MNE-Sample dataset, which is a single recording on a single subject, and cut it into 8 pieces to simulate data coming from 2 subjects, performing 2 sessions, and having 2 runs within each session. Do do this, execute the python script `make_example_data.py`.


## Running the analysis

Run all the numbered scripts one by one.

The `05_freesurfer.py` script will take a few hours per subject, keep this in mind.

The `06_coregistration.py` script can be used to co-register the FreeSurfer surfaces with the MEG data. This is best done in an interactive python environment (an IPython terminal) by running `%run 07_coregistration.py -sub <subject-number>`. It will open a GUI you can use for co-registration and save the resulting transformation when you close the GUI. Edit the script to set the subject to process.


## Authors

This example analysis pipeline was created by Mia Liljeström and Marijn van Vliet.
