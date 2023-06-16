#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization on wetlab sensor dataset'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/wetlab/ \
    --input_file wetlab.csv \
    --output_dir ~/data/usup_reg/raw/wetlab/ \
    --output_file std_wetlab.csv \
    --x_col_indices 3,5,7,9,11,13,15,17,19,21,23,27
