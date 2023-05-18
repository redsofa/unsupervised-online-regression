##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Adaptive Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --input_csv_file gt_2015_std.csv \
    --input_csv_param_file gt_2015.params \
    --output_predictions_file online_lr_gt_2015_std_predictions.csv \
    --output_drifts_csv_file online_lr_gt_2015_std_drifts.csv \
    --output_stats_file online_lr_gt_2015_std_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --buffer_size 100 \
    --delta_threshold 0.2
    #--delta_threshold 0.02
    #--delta_threshold 2e-10
    #--delta_threshold 3

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --predictions_file online_lr_gt_2015_std_predictions.csv \
    --drift_file online_lr_gt_2015_std_drifts.csv \
    --stats_file online_lr_gt_2015_std_stats.txt \
    --plot_file online_lr_gt_2015_std.png \
    --plot_drifts True

echo '\n'

echo 'Launching baseline regression model'
# Command to start model
python ../../python/baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --input_csv_file gt_2015_std.csv \
    --output_predictions_file baseline_lr_gt_2015_std_predictions.csv \
    --output_stats_file baseline_lr_gt_2015_std_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 0,1,2,3,4,5,6,7,8,9 \
    --y_col_index 10

echo '\n'

echo 'Launching baseline regression model evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/turbine/$NOW \
    --predictions_file baseline_lr_gt_2015_std_predictions.csv \
    --drift_file online_lr_gt_2015_std_drifts.csv \
    --stats_file baseline_lr_gt_2015_std_stats.txt \
    --plot_file baseline_lr_gt_2015_std.png \
    --plot_drifts False
