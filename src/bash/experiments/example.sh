##!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ../../../datasets \
    --output_dir ../../../datasets \
    --input_csv_file small.csv \
    --input_csv_param_file small.parameters \
    --output_predictions_file small_predictions.csv \
    --output_drifts_csv_file small_drifts.csv \
    --output_stats_file small_stats.txt \
    --train_samples 8 \
    --test_samples 2 \

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ../../../datasets \
    --predictions_file small_predictions.csv \
    --drift_file small_drifts.csv \
    --stats_file small_stats.txt \
    --plot_file small.png
