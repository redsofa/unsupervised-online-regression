#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI turbine'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/turbine \
    --input_file gt_all.csv \
    --output_dir ~/data/usup_reg/raw/uci/turbine \
    --output_file std_gt_all.csv \
    --x_col_indices 0,1,2,3,4,5,6,8,9,10
