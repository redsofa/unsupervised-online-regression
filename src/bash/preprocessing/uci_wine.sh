#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Wine'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/wine \
    --input_file winequality_white.csv \
    --output_dir ~/data/usup_reg/raw/uci/wine \
    --output_file std_winequality_white.csv \
    --x_col_indices 0,1,2,3,4,5,6,7,8,9,10
