##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Adaptive Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_dir ~/data/usup_reg/work/uci/parkinsons/$NOW \
    --input_csv_file parkinsons_updrs.data \
    --input_csv_param_file parkinsons_updrs.params \
    --output_predictions_file online_lr_parkinsons_updrs_predictions.csv \
    --output_drifts_csv_file online_lr_parkinsons_updrs_drifts.csv \
    --output_stats_file online_lr_parkinsons_updrs_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --buffer_size 100 \
    --delta_threshold 1e-06

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/parkinsons/$NOW \
    --predictions_file online_lr_parkinsons_updrs_predictions.csv \
    --drift_file online_lr_parkinsons_updrs_drifts.csv \
    --stats_file online_lr_parkinsons_updrs_stats.txt \
    --plot_file online_lr_parkinsons_updrs.png \
    --plot_drifts True

echo '\n'

echo 'Launching baseline regression model'
# Command to start model
python ../../python/baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_dir ~/data/usup_reg/work/uci/parkinsons/$NOW \
    --input_csv_file parkinsons_updrs.data \
    --output_predictions_file baseline_lr_parkinsons_updrs_predictions.csv \
    --output_stats_file baseline_lr_parkinsons_updrs_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 \
    --y_col_index 5

echo '\n'

echo 'Launching baseline regression model evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/parkinsons/$NOW \
    --predictions_file baseline_lr_parkinsons_updrs_predictions.csv \
    --drift_file online_lr_parkinsons_updrs_drifts.csv \
    --stats_file baseline_lr_parkinsons_updrs_stats.txt \
    --plot_file baseline_lr_parkinsons_updrs.png \
    --plot_drifts False
