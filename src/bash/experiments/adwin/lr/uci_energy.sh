##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/energy \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/energy/$NOW \
    --input_csv_file energydata_complete.csv \
    --input_csv_param_file energydata_complete.params \
    --output_predictions_file online_energydata_complete_predictions.csv \
    --output_drifts_csv_file online_energydata_complete_drifts.csv \
    --output_stats_file online_energydata_complete_stats.txt \
    --algorithm sklearn_linear_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --drift_detector ADWIN

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/adwin/lr/uci/energy/$NOW \
    --predictions_file online_energydata_complete_predictions.csv \
    --drift_file online_energydata_complete_drifts.csv \
    --stats_file online_energydata_complete_stats.txt \
    --plot_file online_energydata_complete.png \
    --plot_drifts True
