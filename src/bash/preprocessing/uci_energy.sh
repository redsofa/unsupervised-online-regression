#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Energy'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/energy \
    --input_file energydata_complete.csv \
    --output_dir ~/data/usup_reg/raw/uci/energy \
    --output_file std_energydata_complete.csv \
    --x_col_indices 3,4,7,8
