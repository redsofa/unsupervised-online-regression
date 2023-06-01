##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/wine \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/wine/$NOW \
    --input_csv_file winequality_white.csv \
    --input_csv_param_file winequality_white.params \
    --output_predictions_file online_winequality_white_predictions.csv \
    --output_drifts_csv_file online_winequality_white_drifts.csv \
    --output_stats_file online_winequality_white_stats.txt \
    --algorithm sklearn_svr_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --retrain_at_every_sample_count 100

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/wine/$NOW \
    --predictions_file online_winequality_white_predictions.csv \
    --drift_file online_winequality_white_drifts.csv \
    --stats_file online_winequality_white_stats.txt \
    --plot_file online_winequality_white.png \
    --plot_drifts True
