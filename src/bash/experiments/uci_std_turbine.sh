##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --input_csv_file gt_2015_std.csv \
    --input_csv_param_file gt_2015.params \
    --output_predictions_file gt_2015_std_predictions.csv \
    --output_drifts_csv_file gt_2015_std_drifts.csv \
    --output_stats_file gt_2015_std_stats.txt \
    --train_samples 100 \
    --test_samples 40 \
    --buffer_size 40 \
    --delta_threshold 0.02
    #--delta_threshold 2e-10
    #--delta_threshold 3

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --predictions_file gt_2015_std_predictions.csv \
    --drift_file gt_2015_std_drifts.csv \
    --stats_file gt_2015_std_stats.txt \
    --plot_file gt_2015_std.png
