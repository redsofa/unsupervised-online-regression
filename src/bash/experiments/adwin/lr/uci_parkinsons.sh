##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/parkinsons/$NOW \
    --input_csv_file parkinsons_updrs.data \
    --input_csv_param_file parkinsons_updrs.params \
    --output_predictions_file online_parkinsons_updrs_predictions.csv \
    --output_drifts_csv_file online_parkinsons_updrs_drifts.csv \
    --output_stats_file online_parkinsons_updrs_stats.txt \
    --algorithm sklearn_linear_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --drift_detector ADWIN

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/parkinsons/$NOW \
    --predictions_file online_parkinsons_updrs_predictions.csv \
    --drift_file online_parkinsons_updrs_drifts.csv \
    --stats_file online_parkinsons_updrs_stats.txt \
    --plot_file online_parkinsons_updrs.png \
    --plot_drifts True

echo '\n'

echo 'Launching baseline regression model'
# Command to start model
python baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/parkinsons/$NOW \
    --input_csv_file parkinsons_updrs.data \
    --output_predictions_file baseline_parkinsons_updrs_predictions.csv \
    --output_stats_file baseline_parkinsons_updrs_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 \
    --y_col_index 5

echo '\n'

echo 'Launching baseline regression model evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/parkinsons/$NOW \
    --predictions_file baseline_parkinsons_updrs_predictions.csv \
    --drift_file online_parkinsons_updrs_drifts.csv \
    --stats_file baseline_parkinsons_updrs_stats.txt \
    --plot_file baseline_parkinsons_updrs.png \
    --plot_drifts False
