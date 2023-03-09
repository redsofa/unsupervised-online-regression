#!/bin/bash

# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --input_stream_file ~/data/UCI/pp_gas_emission/gt_2015.csv \
    --stream_parameter_file ~/data/UCI/pp_gas_emission/gt_2015.params \
    --output_csv_file ~/data/UCI/pp_gas_emission/gt_2015_out.csv \
    --output_stats_file ~/data/UCI/pp_gas_emission/gt_2015_stats.txt \
    --train_samples 100 \
    --test_samples 40 \
    --buffer_size 40 \
    --delta_threshold 2
    #--delta_threshold 5

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --input_results_file ~/data/UCI/pp_gas_emission/gt_2015_out.csv \
    --output_plots_file ~/data/UCI/pp_gas_emission/gt_2015_plots.png
