#!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --input_stream_file ~/data/UCI/parkinsons/parkinsons_updrs.data \
    --stream_parameter_file ~/data/UCI/parkinsons/parkinsons_updrs.params \
    --output_csv_file ~/data/UCI/parkinsons/parkinsons_updrs_out.csv \
    --output_stats_file ~/data/UCI/parkinsons/parkinsons_updrs_stats.txt \
    --train_samples 700 \
    --test_samples 200 \
    --buffer_size 900 \
    --delta_threshold 3

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --input_results_file ~/data/UCI/parkinsons/parkinsons_updrs_out.csv \
    --output_plots_file ~/data/UCI/parkinsons/parkinsons_updrs_plots.png
