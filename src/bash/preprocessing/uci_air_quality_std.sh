#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI Air Quality'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/uci/air_quality \
    --input_file imp_AirQualityUCI.csv \
    --output_dir ~/data/usup_reg/raw/uci/air_quality \
    --output_file std_AirQualityUCI.csv \
    --x_col_indices 3,6,8,10,11,12,13,14 
