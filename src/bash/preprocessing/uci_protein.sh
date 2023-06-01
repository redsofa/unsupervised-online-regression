#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Protein'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/protein \
    --input_file CASP.csv \
    --output_dir ~/data/usup_reg/raw/uci/protein \
    --output_file std_CASP.csv \
    --x_col_indices 1,2,3,4,5,6,7,8,9
