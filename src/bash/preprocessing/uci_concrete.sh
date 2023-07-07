#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI concrete'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/concrete \
    --input_file concrete_data.csv \
    --output_dir ~/data/usup_reg/raw/uci/concrete \
    --output_file std_concrete_data.csv \
    --x_col_indices 0,1,2,3,4,5,6,7
