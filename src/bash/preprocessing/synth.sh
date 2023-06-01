#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization Synthetic'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/synth \
    --input_file synth.csv \
    --output_dir ~/data/usup_reg/raw/synth \
    --output_file std_synth.csv \
    --x_col_indices 0,1,2,3
