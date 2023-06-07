#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Energy'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/bike \
    --input_file seoul_bike.csv \
    --output_dir ~/data/usup_reg/raw/uci/bike \
    --output_file std_seoul_bike.csv \
    --x_col_indices 2,3,4,5,6,7,8,9,10
