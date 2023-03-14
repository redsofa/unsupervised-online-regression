#!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/city_of_fredericton/air_quality \
    --output_dir ~/data/usup_reg/work/city_of_fredericton/air_quality \
    --input_csv_file aq_sensor.csv \
    --input_csv_param_file aq_sensor.params \
    --output_predictions_file aq_sensors_predictions.csv \
    --output_stats_file aq_sensors_stats.txt \
    --train_samples 120 \
    --test_samples 30 \
    --buffer_size 200 \
    --delta_threshold 10
    #--delta_threshold 1e-10

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/city_of_fredericton/air_quality \
    --predictions_file aq_sensors_predictions.csv \
    --stats_file aq_sensors_stats.txt \
    --plot_file aq_sensors_plot.png
