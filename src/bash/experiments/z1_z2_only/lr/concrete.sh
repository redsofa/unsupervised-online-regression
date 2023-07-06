##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/concrete \
    --output_dir ~/data/usup_reg/work/z1_z2_only/lr/concrete/$NOW \
    --input_csv_file concrete_data.csv \
    --input_csv_param_file concrete_data.params \
    --output_predictions_file concrete_predictions.csv \
    --output_stats_file concrete_stats.txt \
    --working_data_points 120 \
    --max_samples None \
    --output_drifts_csv_file concrete_drifts.csv \
    --algorithm sklearn_linear_regression_model \
    --drift_detector_config '{"detector": "NA"}' \
    --delta_threshold 0.3 \
    --is_baseline_run False \
    --loglevel DEBUG

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/z1_z2_only/lr/concrete/$NOW \
    --predictions_file concrete_predictions.csv \
    --drift_file concrete_drifts.csv \
    --stats_file concrete_stats.txt \
    --plot_file concrete.png \
    --plot_drifts True
