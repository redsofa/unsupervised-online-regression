##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/energy \
    --output_dir ~/data/usup_reg/work/uci/energy/$NOW \
    --input_csv_file energydata_complete.csv \
    --input_csv_param_file energydata_complete.params \
    --output_predictions_file energydata_complete_predictions.csv \
    --output_drifts_csv_file energydata_complete_drifts.csv \
    --output_stats_file energydata_complete_stats.txt \
    --train_samples 500 \
    --test_samples 100 \
    --buffer_size 100 \
    --delta_threshold 2
    #--delta_threshold 200

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/energy/$NOW \
    --predictions_file energydata_complete_predictions.csv \
    --drift_file energydata_complete_drifts.csv \
    --stats_file energydata_complete_stats.txt \
    --plot_file energydata_complete.png
