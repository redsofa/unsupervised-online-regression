##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/uci/turbine/$NOW \
    --input_csv_file gt_2015_std.csv \
    --input_csv_param_file gt_2015.params \
    --output_predictions_file online_gt_2015_std_predictions.csv \
    --output_drifts_csv_file online_gt_2015_std_drifts.csv \
    --output_stats_file online_gt_2015_std_stats.txt \
    --algorithm sklearn_svr_regression_model \
    --train_samples 100 \
    --test_samples 20

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/uci/turbine/$NOW \
    --predictions_file online_gt_2015_std_predictions.csv \
    --drift_file online_gt_2015_std_drifts.csv \
    --stats_file online_gt_2015_std_stats.txt \
    --plot_file online_gt_2015_std.png \
    --plot_drifts False