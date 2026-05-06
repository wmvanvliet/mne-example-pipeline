# Standard MNE source estimation pipeline

A standard pipeline for source localization of evoked responses using MNE. This is meant as a jumping-off point for your own data analysis pipeline.


## Other versions of this pipeline

There are multiple branches in this repository. You are currently on the `advanced` branch:
- `minimal` The most basic version of the pipeline, handling one data file per subject.
- **`advanced`** A more powerful version of the pipeline, handling multiple subjects, sessions and runs. Adds more bells and whistles to the code to make it portable and reproducible. 
- `expert` An even more powerful version, adding a build system, and HTML reports.


## Getting started

#### 1. Have access to a scientific Python environment

To run this analysis pipeline, you need access to a Python environment with has the
MNE-Python package installed.

- On Triton, you can load one with: `module load neuroimaging-env`
- On Aalto workstations, you can load one with:
  `module load scibuilder-mamba-dev neuroimaging-env`  

#### 2. Have access to MegIn's maxfilter™ program and [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)

- On Triton, you can load it with: `module load maxfilter freesurfer`
- On Aalto workstations, you can load it with: `module load neuromag freesurfer`

Loading the FreeSurfer module will give some additional instructions for you, namely that you should execute `source` on a specific file.

If you don't have access to MegIn's maxfilter™, then you can use the MNE-Python version by setting `use_megin_maxfilter = False` in `config.py`.

You can run FreeSurfer on your own machine, if it's Linux or a Mac.
You can download FreeSurfer from their website: https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall 
It will not run on Windows (instead, run it remotely either on a workstation or on Triton).

#### 3. Create the example data

For this example pipeline, we take the MNE-Sample dataset, which is a single recording on a single subject, and cut it into 8 pieces to simulate data coming from 2 subjects, performing 2 sessions, and having 2 runs within each session. Do do this, execute the python script `make_example_data.py -d <data_path>`, where `<data_path>` is the folder you want the data to be stored in (it defaults to `./data/orig` if you omit it).

#### 4. Configure the pipeline

Edit the `config.py` file to configure the location of the data folders. For example, you will need to set the `orig_data_path` to the location where you put the example data during the previous step.


## Running the analysis

#### 1. Run the sensor level analysis
You can perform the first steps of the analysis pipeline, that deal with sensor-level data, by executing: `make sensor`.

#### 2. Perform the manual steps required for source level analysis
Before we can move on to source level analysis, there are some manual steps to be performed.

First, FreeSurfer needs to be run, which takes a few hours per subject. This is why this step is not performed automatically. You can execute it by running `make freesurfer`.

Second, the FreeSurfer MRI surfaces need to be co-registered with the MEG data. This is best done in an interactive python environment (an IPython terminal) by running `%run 07_coregistration.py -sub <subject-number> -ses <session-number>`. It will open a GUI you can use for co-registration and save the resulting transformation when you close the GUI.

#### 3. Run the source level analysis
You can now perform the final steps of the analysis pipeline, that deal with source-level data, by executing: `make source`.


## Building on this example pipeline

This repository can serve as a template for your own analysis pipeline. Generally we recommend splitting each analysis step into its own script, and number them. In addition, we recommend having a single `config.py` file that contains all the parameters that are shared between analysis scripts. For more information and ideas, see: https://doi.org/10.1371/journal.pcbi.1007358


## Authors

This example analysis pipeline was created by Mia Liljeström and Marijn van Vliet.
