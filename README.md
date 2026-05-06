# A minimal MNE source estimation pipeline

A minimal pipeline for source localization of evoked responses using MNE. This is meant as a clear example of how to perform all the steps needed.

## Other versions of this pipeline

There are multiple branches in this repository. You are currently on the `minimal` branch:
- **`minimal`** The most basic version of the pipeline, handling one data file per subject.
- `advanced` A more powerful version of the pipeline, handling multiple subjects, sessions and runs. Adds more bells and whistles to the code to make it portable and reproducible. 
- `expert` An even more powerful version, adding a build system, and HTML reports.

## Getting started

#### 1. Have access to a scientific Python environment

To run this analysis pipeline, you need access to a Python environment with has the MNE-Python package installed.

- On Triton, you can load one with: `module load neuroimaging-env`
- On Aalto workstations, you can load one with:
  `module load scibuilder-mamba-dev neuroimaging-env`  

#### 2. Have access to MegIn's maxfilter™ program and [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)

- On Triton, you can load it with: `module load maxfilter freesurfer`
- On Aalto workstations, you can load it with: `module load neuromag freesurfer`

Loading the FreeSurfer module will give some additional instructions for you, namely that you should execute `source` on a specific file.

You can run FreeSurfer on your own machine, if it's Linux or a Mac.
You can download FreeSurfer from their website: https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall 
It will not run on Windows (instead, run it remotely either on a workstation or on Triton).

#### 3. Create the example data

For this example pipeline, we take the MNE-Sample dataset, which is a single recording on a single subject, and cut it into 2 pieces to simulate data coming from 2 subjects. Do do this, execute the python script `make_example_data.py`.


## Running the analysis

Run all the numbered scripts one by one.

The `05_freesurfer.py` script will take a few hours per subject, keep this in mind.

The `06_coregistration.py` script can be used to co-register the FreeSurfer surfaces with the MEG data. This is best done in an interactive python environment (an IPython terminal) by editing the file to set the subject number, and than doing `%run 06_coregistration.py` inside the python terminal. It will open a GUI you can use for co-registration and save the resulting transformation when you close the GUI.


## Authors

This example analysis pipeline was created by Mia Liljeström and Marijn van Vliet.
