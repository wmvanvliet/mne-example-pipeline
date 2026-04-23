# Standard MNE source estimation pipeline

A standard pipeline for source localization of evoked responses using MNE. This is meant as a jumping-off point for your own data analysis pipeline.

## Getting started

### 1. Have access to a scientific Python environment

To run this analysis pipeline, you need access to a Python enviroment with has the
MNE-Python package installed.

- On Triton, you can load one with: `module load neuroimaging-env`
- On Aalto workstations, you can load one with:
  `module load scibuilder-mamba-dev neuroimaging-env`  

### 2. Have access to MegIn's maxfilter™ program and [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)

- On Triton, you can load them with: `module load maxfilter freesurfer`
- On Aalto workstations, you can load them with: `module load neuromag freesurfer`

Loading the FreeSurfer module will give some additional instructions for you, namely that you should execute `source` on a specific file.

### 3. Configure the pipeline

Edit the `config.py` file and make sure the data folders are set to where you
want them to be.

### 4. Create the example data

For this example pipeline, we take the MNE-Sample dataset, which is a single recording
on a single subject, and cut it into 8 pieces to simulate data coming from 2 subjects,
performing 2 sessions, and having 2 runs within each session. Do do this, execute the
python script `make_example_data.py -d <data_path>`, where `<data_path>` is the folder you
want the data to be stored in (it defaults to `./data/orig` if you omit it).

## Running the analysis

### 1. Run the sensor level analysis
You can perform the first steps of the analysis pipeline, that deal with sensor-level data, by executing: `make sensor`.

### 2. Perform the manual steps required for source level analysis
Before we can move on to source level analysis, there are some manual steps to be performed first.

### 3. Run the source level analysis
You can now perform the final steps of the analysis pipeline, that deal with source-level data, by executing: `make source`.

## Building on this example pipeline
