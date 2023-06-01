#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Parkinsons'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/parkinsons \
    --input_file parkinsons_updrs.data \
    --output_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_file std_parkinsons_updrs.data \
    --x_col_indices 1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
