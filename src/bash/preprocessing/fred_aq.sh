#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching standardization Fredericton Air Quality'
# Command to start the model
python standardize.py \
    --input_dir ~/data/usup_reg/raw/city_of_fredericton/air_quality \
    --input_file aq_sensor.csv \
    --output_dir ~/data/usup_reg/raw/city_of_fredericton/air_quality \
    --output_file std_aq_sensor.csv \
    --x_col_indices 1,2,3,4,5,11
