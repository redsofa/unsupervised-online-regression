#!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/city_of_fredericton/air_quality \
    --output_dir ~/data/usup_reg/work/pagehinkley/rf/city_of_fredericton/air_quality/$NOW \
    --input_csv_file aq_sensor.csv \
    --input_csv_param_file aq_sensor.params \
    --output_predictions_file online_aq_sensors_predictions.csv \
    --output_drifts_csv_file online_aq_sensors_drifts.csv \
    --output_stats_file online_aq_sensors_stats.txt \
    --algorithm sklearn_randomforest_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --drift_detector PAGEHINKLEY

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/pagehinkley/rf/city_of_fredericton/air_quality/$NOW \
    --predictions_file online_aq_sensors_predictions.csv \
    --drift_file online_aq_sensors_drifts.csv \
    --stats_file online_aq_sensors_stats.txt \
    --plot_file online_aq_sensors.png \
    --plot_drifts True
