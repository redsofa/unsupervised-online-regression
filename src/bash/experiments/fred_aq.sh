#!/bin/bash

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --input_stream_file ~/data/fred_open_data/air_quality/aq_sensor.csv \
    --stream_parameter_file ~/data/fred_open_data/air_quality/aq_sensor.params \
    --output_csv_file ~/data/fred_open_data/air_quality/aq_sensor_out.csv \
    --train_samples 600 \
    --test_samples 200 \
    --buffer_size 800 \
    --delta_threshold 5

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --input_results_file ~/data/fred_open_data/air_quality/aq_sensor_out.csv \
    --output_plots_file ~/data/fred_open_data/air_quality/aq_sensor_plots.png
