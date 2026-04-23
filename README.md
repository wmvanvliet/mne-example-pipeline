# Standard MNE source estimation pipeline

A standard pipeline for source localization of evoked responses using MNE. This is meant as a jumping-off point for your own data analysis pipeline.

## Getting started

### 1. Have access to a scientific Python environment

To run this analysis pipeline, you need access to a Python enviroment with has the
MNE-Python package installed.

On Triton, you can load one with: `module load neuroimaging-env`  
On Aalto workstations, you can load one with:
`module load scibuilder-mamba-dev neuroimaging-env`  
On a laptop of your own, follow the instructions on the
[MNE-Python installation page](https://mne.tools/stable/install/index.html)


### 2. Creating the example data

For this example pipeline, we take the MNE-Sample dataset, which is a single recording
on a single subject, and cut it into 8 pieces to simulate data coming from 2 subjects,
performing 2 sessions, and having 2 runs within each session. Do do this, execute the
python script `make_example_data.py -d <data_path>`, where `<data_path>` is the folder you
want the data to be stored in (it defaults to `./data/orig` if you omit it).

### 3. Ru
