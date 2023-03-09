#!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'

# Command to start the model
python ../../python/main.py \
    --input_stream_file ~/data/UCI/energy/energydata_complete.csv \
    --stream_parameter_file ~/data/UCI/energy/energydata_complete.params \
    --output_csv_file ~/data/UCI/energy/energydata_complete_out.csv \
    --output_stats_file ~/data/UCI/energy/energydata_complete_stats.txt \
    --train_samples 4000 \
    --test_samples 800 \
    --buffer_size 2000 \
    --delta_threshold 1e-15

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --input_results_file ~/data/UCI/energy/energydata_complete_out.csv \
    --output_plots_file ~/data/UCI/energy/energydata_complete_plots.png
