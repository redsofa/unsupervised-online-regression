##!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/energy \
    --output_dir ~/data/usup_reg/work/uci/energy \
    --input_csv_file energydata_complete.csv \
    --input_csv_param_file energydata_complete.params \
    --output_predictions_file energydata_complete_predictions.csv \
    --output_stats_file energydata_complete_stats.txt \
    --train_samples 500 \
    --test_samples 100 \
    --buffer_size 100 \
    --delta_threshold 200
    #--delta_threshold 2

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/energy \
    --predictions_file energydata_complete_predictions.csv \
    --stats_file energydata_complete_stats.txt \
    --plot_file energydata_complete.png
