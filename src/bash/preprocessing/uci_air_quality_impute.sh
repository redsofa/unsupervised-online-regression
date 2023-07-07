#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization UCI turbine'
# Command to start the model
python impute.py \
    --input_dir ~/data/usup_reg/raw/uci/air_quality \
    --input_file AirQualityUCI.csv \
    --output_dir ~/data/usup_reg/raw/uci/air_quality \
    --output_file imp_AirQualityUCI.csv \
    --x_col_indices 2,3,4,5,6,7,8,9,10,11,12,13,14
