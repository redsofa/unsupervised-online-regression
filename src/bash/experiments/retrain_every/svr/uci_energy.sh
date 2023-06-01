##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/energy \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/energy/$NOW \
    --input_csv_file energydata_complete.csv \
    --input_csv_param_file energydata_complete.params \
    --output_predictions_file online_energydata_complete_predictions.csv \
    --output_drifts_csv_file online_energydata_complete_drifts.csv \
    --output_stats_file online_energydata_complete_stats.txt \
    --algorithm sklearn_svr_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --retrain_at_every_sample_count 100

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/energy/$NOW \
    --predictions_file online_energydata_complete_predictions.csv \
    --drift_file online_energydata_complete_drifts.csv \
    --stats_file online_energydata_complete_stats.txt \
    --plot_file online_energydata_complete.png \
    --plot_drifts True

echo '\n'

echo 'Launching baseline regression model'
# Command to start model
python baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/energy \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/energy/$NOW \
    --input_csv_file energydata_complete.csv \
    --output_predictions_file baseline_energydata_complete_predictions.csv \
    --output_stats_file baseline_energydata_complete_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 3,4,7,8 \
    --y_col_index 1

echo '\n'

echo 'Launching baseline regression model evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/retrain_every/svr/uci/energy/$NOW \
    --predictions_file baseline_energydata_complete_predictions.csv \
    --drift_file online_energydata_complete_drifts.csv \
    --stats_file baseline_energydata_complete_stats.txt \
    --plot_file baseline_energydata_complete.png \
    --plot_drifts False
