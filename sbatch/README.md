# SBATCH scripts for running on Triton

## Usage

Start the pipeline by running (on the login node) the `run_all.sh` script. That script submits all the jobs to run the entire pipeline. Take a look at that script to see how job dependencies are handled.

The individual steps are in their own SBATCH scripts:
```
01_convert_to_BIDS.sh
02_sensor_level.sh
03_freesurfer.sh
04_source_level.sh
05_grand_average.sh
```
Note that some of the steps that are in separate python scripts are bundled here (e.g. `02_sensor_level.sh` runs all sensor-level python scripts), because otherwise the jobs would be too short. This may be different in your own analysis.
